"""Stage run_audit (Spec §6.1): the corpus audit whose evidence gate G1 freezes
the registry, alphabet and T* **from** (Spec §3.3–3.4). Real data: counts only
(D30). §6.1 names the stage "corpus audit → registry + alphabet + T* frozen";
this stage produces the audit, and the freeze is a separate, later act — see the
closing note.

Two modes, one code path:

* **canonical (default)** — every sentence must carry a registry assignment, and
  the overrides file must declare ``_status: RATIFIED``; anything else aborts
  (§3.3). This is the mode that produces the evidence for the G1 freeze.
* **``--pre-audit``** — the explicit incomplete mode used before the registry is
  ratified. It stamps the report ``INCOMPLETE / PENDING_REGISTRY``, withholds both
  gate verdicts and computes no T*. Incompleteness is never reached by silent
  degradation: it has to be asked for.

What the mode does **not** excuse, because none of it is registry incompleteness:
a missing overrides file, an override naming a document outside the corpus, an
invalid assignment among the rows that do exist, a configured corpus language with
no data, or a mapping that retains no symbol at all. Those abort in both modes.

The stage never freezes anything: no ``alphabet.json``, no registry, no T*.
"""

import argparse
import datetime
import hashlib
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import yaml

from hexis import alphabet, conllu_reader, registry
from hexis.config import (
    check_against_default,
    config_hash,
    derive_seed,
    resolve_config,
)
from hexis.manifest import (
    build_manifest,
    git_state,
    sha256_file,
    write_manifest,
    write_sidecar,
)

ENTRY_POINT = "hexis.pipeline.run_audit"

RAW_TOKEN_COLUMNS = (
    "language",
    "doc_id",
    "sent_id",
    "token_ord",
    "upos_raw",
    "deprel_raw",
)

PENDING = "INCOMPLETE / PENDING_REGISTRY"


def language_of(path: Path, languages) -> str:
    """UD file names are ``{lang}_{treebank}-ud-{split}.conllu``; the code is the prefix."""
    code = path.name.split("_", 1)[0]
    if code not in languages:
        raise ValueError(
            f"{path}: language code {code!r} is not one of the configured corpus "
            f"languages {sorted(languages)} (§6.3). Narrowing corpus.languages is "
            "not on its own enough to audit one language of a multilingual data "
            "root: point --data-root at that language's treebank as well."
        )
    return code


def _conllu_paths(data_root: Path) -> list[Path]:
    return sorted(Path(data_root).rglob("*.conllu"))


def discover_files(data_root: Path) -> list[Path]:
    """Every ``.conllu`` under ``data_root``, in sorted order.

    Separate from reading so the inputs can be hashed **before** they are parsed:
    the digests that identify a run have to be the digests it computed on.
    """
    files = _conllu_paths(data_root)
    if not files:
        raise FileNotFoundError(f"no .conllu files under {data_root}")
    return files


@contextmanager
def staged_inputs(paths):
    """Copy each input's bytes to a private directory and hash **those** bytes.

    Yields ``(snapshot, staged)``: original path -> SHA-256, and original path ->
    the copy to read.

    Hashing a file and then reopening it to parse is not enough, however tight the
    window looks and however carefully the digest is re-checked afterwards. The
    defeating sequence is edit → parse → restore: both digests match the original
    while the parse consumed something else, and the run publishes a report of
    bytes its manifest does not describe. Comparing before and after cannot see
    this, because there is nothing left to compare.

    So the bytes are read once, the digest is taken of what was read, and the
    parse consumes a copy no one else has a path to. Digest and content then
    describe the same bytes by construction rather than by timing.
    """
    with tempfile.TemporaryDirectory(prefix="hexis-audit-") as tmp:
        staging = Path(tmp)
        snapshot: dict[Path, str] = {}
        staged: dict[Path, Path] = {}
        for index, original in enumerate(map(Path, paths)):
            data = original.read_bytes()
            snapshot[original] = hashlib.sha256(data).hexdigest()
            # Index-prefixed so two inputs sharing a basename cannot collide.
            copy = staging / f"{index:04d}_{original.name}"
            copy.write_bytes(data)
            staged[original] = copy
        yield snapshot, staged


def verify_inputs_unchanged(
    snapshot: dict[Path, str], *, files, data_root: Path
) -> None:
    """Refuse to publish if the inputs moved under us — in any of three ways.

    This is **not** what makes digest and content agree — `staged_inputs` does
    that, by construction. What is left for this check is the operator's question:
    did the corpus move while we were auditing it? A run whose sources were
    **edited** or **removed** underneath it, or whose data root gained a **new**
    `.conllu`, describes a state that no longer exists, and publishing that
    silently would be its own kind of dishonesty.

    So the data root is re-globbed as well as re-hashed. Checked before the first
    write, so a failure publishes nothing.
    """
    problems = []
    appeared = sorted(set(_conllu_paths(data_root)) - set(files))
    if appeared:
        problems.append(f"appeared: {[str(path) for path in appeared]}")
    for path, digest in sorted(snapshot.items()):
        if not path.exists():
            problems.append(f"removed: {path}")
        elif sha256_file(path) != digest:
            problems.append(f"edited: {path}")
    if problems:
        raise RuntimeError(
            "inputs changed while the audit was running — "
            + "; ".join(problems)
            + ". Nothing was written; rerun against a stable data root (§6.4, D46)."
        )


def read_tokens(files, languages, *, staged=None) -> pd.DataFrame:
    """Stream the given ``.conllu`` files into one raw token table.

    Files are visited in sorted order and their contents pooled per document: UD
    train/dev/test splits are not analysis splits (D03), and four documents in
    this corpus genuinely span two files.

    `registry.enumerate_prefixes` is not called here — it consumes the same
    sentence stream to produce only the counts, and this pass needs the token rows
    from it. Its two guarantees are kept: `doc_id` comes from
    `registry.doc_id_from_sent_id`, and a `newdoc id` that contradicts the derived
    prefix aborts the run.
    """
    records = []
    seen_sent_ids = {}
    for path in files:
        # Language from the *original* name (the staged copy is index-prefixed),
        # bytes from the staged copy.
        language = language_of(path, languages)
        source = staged[path] if staged else path
        try:
            sentences = list(conllu_reader.iter_sentences(source))
        except conllu_reader.ParseError as exc:
            # Re-point at the file the operator knows about, not the staging copy.
            raise conllu_reader.ParseError(
                path, exc.sent_id, exc.token_id, exc.reason
            ) from exc
        for sentence in sentences:
            sent_id = sentence.metadata["sent_id"]
            # D03 pools the UD splits, so a repeated id is not a duplicate row to
            # drop: it is one sentence counted twice in n_sentences and
            # n_tokens_raw, and in everything derived from them. Keyed on sent_id
            # alone — doc_id is derived from it, so an id shared across languages
            # is the same collision seen one level down.
            if sent_id in seen_sent_ids:
                raise ValueError(
                    f"sent_id {sent_id!r} occurs in both {seen_sent_ids[sent_id]} "
                    f"and {path}: D03 pools the UD splits, so a repeated id is "
                    "counted twice in n_sentences and n_tokens_raw (§3.3)"
                )
            seen_sent_ids[sent_id] = path
            doc_id = registry.doc_id_from_sent_id(sent_id)
            declared = sentence.metadata.get("newdoc id")
            if declared is not None and declared != doc_id:
                raise ValueError(
                    f"newdoc id {declared!r} contradicts the doc_id {doc_id!r} derived "
                    f"from sent_id {sent_id!r}: document identity is ambiguous (§3.3)"
                )
            for token_ord, token in enumerate(sentence, start=1):
                records.append(
                    (
                        language,
                        doc_id,
                        sent_id,
                        token_ord,
                        token["upos"],
                        token["deprel"],
                    )
                )
    if not records:
        raise ValueError(
            f"no sentences read from {len(files)} .conllu file(s): an audit over an "
            "empty corpus would report nothing and pass every gate"
        )

    # The configured languages are the corpus, not an allowlist. A treebank that
    # is simply absent would otherwise yield a complete-looking audit of half the
    # corpus — every count correct for what it saw, and wrong about what it claims
    # to be. Registry gaps are what --pre-audit exists for; a missing treebank is
    # not one.
    missing = sorted(set(languages) - {record[0] for record in records})
    if missing:
        raise ValueError(
            f"no data for configured corpus language(s) {missing}: §2.1 pins both "
            f"treebanks, and corpus.languages is {sorted(languages)}. Restrict "
            "corpus.languages if a single-language audit is intended."
        )
    return pd.DataFrame(records, columns=list(RAW_TOKEN_COLUMNS))


def load_overrides(path: Path, source: Path | None = None) -> tuple[dict, dict]:
    """Split an overrides file into ``(assignments, metadata)``.

    Keys beginning with ``_`` are reserved metadata, never document assignments —
    that is what lets a file declare its own ratification status. Everything else
    is a raw `sent_id` prefix.

    A missing file is an error, not an empty registry: silently reading a typo'd
    path as "no assignments yet" would turn a mistake into a label-free report
    that looks deliberate.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"overrides file {path} does not exist; an absent file is not an empty "
            "registry (§3.3)"
        )
    try:
        data = yaml.safe_load((source or path).read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        # PyYAML names the origin "<unicode string>" when it is handed text, and
        # repeats that name inside every error marker — so prefixing the real path
        # leaves the message contradicting itself. Substituting it is enough, and
        # unlike naming a stream it keeps PyYAML's source snippet and caret.
        # The name substituted is the *original* path even when the bytes come
        # from the staging copy: the copy is an implementation detail the operator
        # cannot act on. A future PyYAML that stops emitting the placeholder makes
        # this a no-op, and the prefix still names the file.
        detail = str(exc).replace("<unicode string>", str(path))
        raise ValueError(f"{path}: not valid YAML — {detail}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError(
            f"{path}: an overrides file must be a mapping of `sent_id` prefix -> "
            f"assignment, not {type(data).__name__} (§3.3, D04)"
        )
    metadata, assignments = {}, {}
    for key, value in data.items():
        if not isinstance(key, str):
            raise ValueError(
                f"{path}: key {key!r} is {type(key).__name__}, but keys are `sent_id` "
                "prefixes (strings) or reserved `_`-metadata (§3.3)"
            )
        if key.startswith("_"):
            metadata[key] = value
        elif not isinstance(value, dict):
            raise ValueError(
                f"{path}: assignment for {key!r} is {type(value).__name__}, not a "
                "mapping of registry fields (§2.3, D04)"
            )
        else:
            assignments[key] = value
    return assignments, metadata


def check_ratification(metadata: dict, path: Path, *, pre_audit: bool) -> None:
    """Only an explicitly ratified overrides file may produce a canonical audit.

    Ratification is opt-in, not opt-out: an unmarked file is **not** ratified. The
    inverse rule — refuse only files that declare themselves PROPOSED — would make
    the guarantee depend on the author of a proposal remembering to mark it, and
    §3.3 requires assignments to be human-verified, which is a claim someone has
    to make rather than one to assume from silence.

    The declaration travels inside the file, so the guarantee survives copying and
    renaming.
    """
    if pre_audit:
        return
    status = metadata.get("_status")
    if status == "RATIFIED":
        return
    raise ValueError(
        f"{path} has _status: {status!r}, so it cannot produce a canonical audit. "
        "A canonical audit requires the overrides file to declare "
        "_status: RATIFIED; run with --pre-audit until it does (Spec §3.3, D04)."
    )


def prefix_counts(tokens: pd.DataFrame) -> pd.DataFrame:
    """Per raw `sent_id` prefix: the columns `registry.build_registry` consumes."""
    return (
        tokens.groupby(["language", "doc_id"], sort=True)
        .agg(n_sentences=("sent_id", "nunique"), n_tokens_raw=("sent_id", "size"))
        .reset_index()[list(registry.PREFIX_COLUMNS)]
    )


def resolve_registry(tokens: pd.DataFrame, overrides: dict, *, pre_audit: bool):
    """Build and validate the registry, or explain why that cannot be done.

    Returns ``(registry_frame, canonical_of, unassigned)``.

    The registry is built by `registry.build_registry` in **both** modes, never by
    reading `overrides[doc_id]["regime"]` directly: that shortcut validates
    nothing, so an invalid regime label, a missing required field or a mistyped
    merge target would flow straight into the aggregates. Merges matter in the
    pre-audit too — whether Athenaeus 12+13 is one document or two changes the
    document count, the retained-token column and therefore T*.

    Mode governs exactly one thing: whether **missing** assignments are tolerated
    (pre-audit only, and then the registry is dropped entirely rather than used
    partially). Everything else is an error in both modes:

    * a **stale** override, naming a document absent from the corpus — the file
      describes a different corpus than the one being audited;
    * an **invalid** assignment among the rows that do exist. `--pre-audit`
      tolerates absence, never error, so the rows present are validated even when
      the file is incomplete — otherwise a bad regime label would sit unnoticed in
      the proposal until the day it is ratified.
    """
    counts = prefix_counts(tokens)
    present = set(counts["doc_id"])

    stale = sorted(set(overrides) - present)
    if stale:
        raise ValueError(
            f"registry overrides name documents absent from the corpus: {stale}. "
            "The overrides file describes a different corpus than the one being "
            "audited; --pre-audit does not excuse this."
        )

    unassigned = sorted(present - set(overrides))
    # Validate the assigned rows through the real builder. When the file is
    # complete this *is* the registry; when it is partial the frame is discarded,
    # but regime labels, required fields and merge targets have still been checked.
    frame = (
        registry.build_registry(counts[counts["doc_id"].isin(overrides)], overrides)
        if overrides
        else None
    )

    if unassigned:
        if not pre_audit:
            raise ValueError(
                f"no registry assignment for {unassigned}: the audit fails on any "
                "unassigned sentence (Spec §3.3, D04). Populate the overrides file, "
                "or pass --pre-audit to run the explicitly incomplete pre-audit."
            )
        # A partial map is never returned: regime aggregates over part of the
        # corpus would read like corpus-wide figures.
        return None, None, unassigned

    return frame, registry.canonical_targets(counts, overrides), []


def inputs_fingerprint(snapshot: dict[Path, str]) -> str:
    """SHA-256 over the sorted ``path\\tsha256`` lines of the input snapshot.

    §6.1 names artifacts ``{stage}_{config-hash}_{date}``, which collides when two
    runs share a config and a date and differ only in the overrides file — the
    second would hit the overwrite refusal on the first one's report. Folding the
    inputs into the name keeps distinct runs distinct. Declared extension to §6.1,
    submitted for ratification with D55.

    Takes the snapshot rather than re-hashing, so the identity of a run is derived
    from the same bytes its report is.
    """
    lines = sorted(f"{path}\t{digest}" for path, digest in snapshot.items())
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _table(frame: pd.DataFrame, limit: int | None = None) -> str:
    shown = frame if limit is None else frame.head(limit)
    header = "| " + " | ".join(map(str, shown.columns)) + " |"
    rule = "| " + " | ".join("---" for _ in shown.columns) + " |"
    rows = [
        "| " + " | ".join(_cell(value) for value in record) + " |"
        for record in shown.itertuples(index=False, name=None)
    ]
    body = "\n".join([header, rule, *rows])
    if limit is not None and len(frame) > limit:
        body += f"\n\n*({len(frame) - limit} further rows omitted.)*"
    return body


def _cell(value) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_report(context: dict) -> str:
    """The audit report (§6.1 `audit_report.md`), honest about what it cannot decide."""
    pre_audit = context["pre_audit"]
    parts = [
        "# G1 corpus audit",
        "",
        f"- Status: **{PENDING if pre_audit else 'CANONICAL'}**",
        f"- Entry point: `{context['entry_point']}`",
        f"- Run id: `{context['run_id']}`",
        f"- Config SHA-256: `{context['config_sha256']}`",
        f"- Overrides file: `{context['overrides_path']}`",
        f"- UD release (pinned, D03): {context['ud_release']}",
        "",
    ]

    if pre_audit:
        parts += [
            "> This run is **deliberately incomplete**. It was invoked with",
            "> `--pre-audit`, which is the only way to reach this state: the",
            "> canonical default aborts on any unassigned sentence (§3.3).",
            "> No gate verdict and no T* appear below, and nothing is frozen.",
            "",
        ]
        if context["unassigned"]:
            parts += [
                "Documents without a registry assignment, which is what blocks the",
                "regime aggregates:",
                "",
                *(f"- `{doc_id}`" for doc_id in context["unassigned"]),
                "",
            ]

    parts += [
        "## Declared readings",
        "",
        "Five points of §3.4 admit more than one reading. They are stated here rather",
        "than settled silently in code:",
        "",
        "1. **GATE-A denominator.** All raw syntactic words of the regime — not the",
        "   excluded subtotal, and not a per-document figure. GATE-A is a per-regime",
        "   threshold (§3.4).",
        "2. **GATE-A scope.** Evaluated **per excluded-deprel label**, and over the",
        "   census of retained-UPOS tokens whose `deprel_base` falls outside the 23,",
        "   independently of whether the active policy drops them or maps them to",
        "   `oth`. D06's escalation names a category and offers an alternative policy",
        "   only for excluded deprels; the D05 UPOS deletions have no alternative and",
        "   are outside the gate. Counting drops instead would make the gate unable to",
        "   fire in exactly the `(ud23_oth, ·)` cells D50 makes mandatory to interpret.",
        "3. **Which regimes carry the GATE-A verdict.** The census below covers all",
        "   five D04 labels; the **verdict** is read over the analysed regimes only,",
        f"   excluding {', '.join(f'`{label}`' for label in alphabet.GATE_A_VERDICT_EXCLUDES)}.",
        "   D06 says \"in any regime\" and D04 does list `EXCLUDED` among the five, so",
        "   the literal reading includes it; the substantive one does not, because an",
        "   `EXCLUDED` document enters no estimand. Firing GATE-A is not a precaution",
        "   but a binding change: D50 gives the `(ud23_oth, ·)` cells mandatory-",
        "   interpretation status and puts a declared caveat on **every primary",
        "   conclusion**. Deriving that from material the study does not analyse would",
        "   make the report less accurate, not more cautious. **GATE-B is deliberately",
        "   not narrowed the same way** — §3.4 asks it to *flag a document for",
        "   inspection*, and a flag that names its own document misleads no one, so a",
        "   gate that only asks someone to look may look everywhere.",
        "4. **Exploratory regimes keep their firing power.** The narrowing of reading 3",
        "   stops at D04's disposal label: `OTHER_VERSE` and `PROSE_POST` are analysed",
        "   (§1.4 — specificity check, chronological-robustness set), so an imbalance",
        "   there is evidence about the same annotation the primary contrast reads, and",
        "   D06's category is a property of the annotation rather than of one regime's",
        "   role. This is the reading that can actually bind: the largest share anywhere",
        "   below is in `OTHER_VERSE`, above both primary regimes — tragedy, not the epic",
        "   invocations D06 anticipated, sits nearest the threshold. Under a primary",
        "   contrast that excludes those regimes, a trigger there would still put D50's",
        "   caveat on every primary conclusion; that is accepted deliberately and is a",
        "   ratification question, not a code default.",
        "5. **Language scope.** Shares are computed per `(language, regime)` — |A|, T*",
        "   and the inferential families are per language (§4.1, §4.2, §5.7), and",
        "   pooling would dilute a Latin excess against the far larger Greek tally. The",
        "   **verdict is one per run**: a trigger in either language fires the gate for",
        "   the whole design, because D06 escalates the excluded-deprel *policy*, which",
        "   both languages and every §5.6 cell share.",
        "",
        "## Document inventory",
        "",
        *(
            [
                "One row per **canonical document**: the §2.3 registry schema, with the",
                "declared merges applied and `n_tokens_retained` filled (`build_registry`",
                "leaves that column null and requires it complete before the G1 freeze;",
                "filling it is not freezing it, and nothing here is persisted).",
            ]
            if context["has_registry"]
            else [
                "One row per **raw `sent_id` prefix** (§3.3, D03) — with no registry there",
                "is no document layer yet, so prefixes a registry would merge are counted",
                "apart. UD train/dev/test are concatenated and are not analysis splits.",
            ]
        ),
        "",
        "`n_tokens_retained` is the count under this run's configuration, and is the",
        "column from which T* is derived by hand while `t_star` awaits signature",
        "ratification.",
        "",
        _table(context["inventory"]),
        "",
        "## Retention and drop rates, per document",
        "",
        _table(context["retention"]),
        "",
        "### Excluded-UPOS census (D05), by label",
        "",
        _table(context["excluded_upos"]),
        "",
        "### Excluded-DEPREL census (D06/D09), by label",
        "",
        _table(context["excluded_deprel"]),
        "",
        "## Alphabet inventory (observed, NOT frozen)",
        "",
        "Per (language, variant) — §4.1 defines |A| for that pair, so the two",
        "languages are never pooled. No `alphabet.json` is written by this stage.",
        "",
        _table(context["alphabet_sizes"]),
        "",
        "### Most frequent symbols, per language",
        "",
        _table(context["alphabet_head"]),
        "",
        "The **complete** symbol -> id map, including every tie-break, ships as CSV",
        "beside this report: the top of the list does not let a reader check the",
        "ordering rule, and these are the ids the freeze will later assign.",
        "",
        "## Companion CSVs",
        "",
        "§3.4 pre-registers the **full** raw contingency per document and regime; at",
        "~10² UPOS×DEPREL pairs per document it is unreadable as a table. These files",
        "carry it, each with a sidecar and hashed in the same manifest:",
        "",
        *(f"- `{path.name}`" for path in context["csv_files"]),
        "",
    ]
    if not context["has_registry"]:
        parts += [
            "The **per-regime** half of that contingency is absent from this run, and",
            "cannot be produced: regimes come from the registry, and there is none.",
            "It is emitted as soon as the audit runs against an overrides file.",
            "",
        ]

    if context["by_regime"] is not None:
        ratified = context["registry_status"] == "RATIFIED"
        label = "" if not pre_audit else (
            " (PROVISIONAL — mode suppresses verdicts)"
            if ratified
            else " (PROVISIONAL — unratified registry)"
        )
        parts += [f"## Regime aggregates{label}", ""]
        if pre_audit and ratified:
            parts += [
                "> **PROVISIONAL for one reason only: `--pre-audit` was requested.**",
                "> The registry behind these aggregates *is* ratified"
                f" (`_status: RATIFIED` in {context['overrides_path']}); this mode",
                "> withholds every verdict by construction, so they are reported",
                "> without one. Rerun without `--pre-audit` to obtain the verdicts.",
                "",
            ]
        elif pre_audit:
            parts += [
                "> **PROVISIONAL.** These aggregates come from a *proposed* registry",
                "> that has not been ratified. They are evidence for that ratification,",
                "> never a result: no gate verdict is derived from them here.",
                "",
            ]
        parts += [
            "### Drop rates by rule, per regime (T2, §8)",
            "",
            _table(context["retention_by_regime"]),
            "",
            "### Restricted-position fractions (D35, `available_past >= 4`)",
            "",
            _table(context["restricted_fraction"]),
            "",
        ]
        if context["provisional_shares"] is not None:
            parts += [
                "### Excluded-DEPREL shares per regime — the GATE-A input, without its verdict",
                "",
                "These are the shares GATE-A would be read off. They are published as",
                "evidence for the ratification and carry **no verdict**: a different",
                "ratified merge or regime assignment would change them. The table is the",
                "census over all five D04 labels; declared readings 3-5 govern which of",
                "them a verdict may be read from, once there is one.",
                "",
                _table(context["provisional_shares"]),
                "",
            ]

    parts += ["## Gates", ""]
    gate_a, gate_b = context["gate_a"], context["gate_b"]
    if gate_a["status"] == "evaluated":
        parts += [
            f"**GATE-A: {'FIRED' if gate_a['fired'] else 'not fired'}** "
            f"(threshold {gate_a['threshold']:.2%} of raw tokens per regime, per label).",
            "",
            "The table is the **census** and covers every regime; the **verdict**"
            f" above excludes {', '.join(f'`{label}`' for label in gate_a['excluded_regimes'])}.",
            "Rows in those regimes are reported and cannot fire the gate — declared",
            "reading 3.",
            "",
            _table(gate_a["shares"]),
            "",
        ]
    else:
        parts += [f"**GATE-A: NOT EVALUATED** — {gate_a['reason']}.", ""]
    if gate_b["status"] == "evaluated":
        parts += [
            f"**GATE-B: {'FIRED' if gate_b['fired'] else 'not fired'}** "
            f"(documents below {gate_b['threshold']:.0%} retention).",
            "",
            _table(gate_b["flagged"]) if gate_b["fired"] else "No document is below the threshold.",
            "",
        ]
    else:
        parts += [f"**GATE-B: NOT EVALUATED** — {gate_b['reason']}.", ""]
        if context["has_registry"] and context["registry_status"] == "RATIFIED":
            parts += [
                "Retention above **is** computed over canonical documents, from a",
                "ratified registry. The verdict is withheld solely because",
                "`--pre-audit` was requested.",
                "",
            ]
        elif context["has_registry"]:
            parts += [
                "Retention above **is** computed over canonical documents: the merges",
                "declared in the overrides file have been applied before counting. What",
                "is missing is not the merge but the ratification — a different ratified",
                "merge would regroup these rows, so no verdict is declared from them.",
                "",
            ]
        else:
            parts += [
                "Retention above is a screen over **raw `sent_id` prefixes**, not over",
                "canonical documents: with no registry there is no document layer yet,",
                "so prefixes a registry would merge are still counted apart. The screen",
                "is informative in one direction — a token-weighted mean of values all",
                "above the threshold is itself above the threshold, so no merge can pull",
                "a document under it. It remains a screen, not the GATE-B verdict.",
                "",
            ]

    parts += [
        "## T*",
        "",
        "**T*: not computed.** §4.2/D51 fixes T* at G1, but `t_star` is deliberately",
        "unimplemented: its signature is unspecified in §6.2 and",
        "`protocols/sampling.py` forbids inventing one. The signature is submitted for",
        "ratification with D55; until then T* is derived by hand from the",
        "`n_tokens_retained` column above, and that derivation is shown in the D55",
        "proposal rather than produced here.",
        "",
        "## What this stage did not do",
        "",
        "- No model was fitted to any data (D30 — counts only).",
        "- No `alphabet.json`, no registry and no T* were frozen.",
        "- `config/registry_overrides.yaml` was not written.",
        "",
    ]
    return "\n".join(parts)


def build_context(
    tokens, files, overrides_path, cfg, *, pre_audit: bool, overrides_source=None
) -> dict:
    overrides, metadata = load_overrides(overrides_path, overrides_source)
    registry_frame, canonical_of, unassigned = resolve_registry(
        tokens, overrides, pre_audit=pre_audit
    )
    # After the content checks, not before: ratification is a claim *about*
    # well-formed assignments, and an empty or broken registry should report the
    # work outstanding rather than a missing signature on work not yet done.
    check_ratification(metadata, overrides_path, pre_audit=pre_audit)

    regimes = None
    if registry_frame is not None:
        # Fold merged prefixes into their canonical document BEFORE anything is
        # counted. Every per-document figure downstream — the inventory, GATE-B,
        # the retained-token column T* is derived from — must be about documents,
        # not about the raw prefixes a merge dissolves.
        tokens = tokens.assign(doc_id=tokens["doc_id"].map(canonical_of))
        regimes = dict(zip(registry_frame["doc_id"], registry_frame["regime"]))

    mapped = alphabet.map_tokens(tokens, cfg)
    audit = alphabet.run_audit(mapped, cfg, regimes=regimes)
    inventory = _inventory(tokens, mapped, registry_frame)

    provisional_shares = None
    if pre_audit and regimes is not None:
        # The library evaluates whatever registry it is handed; whether a verdict
        # may be *published* is the stage's call. A proposed registry can support
        # provisional aggregates — it cannot support a gate outcome, because
        # ratifying a different merge or regime would change the aggregate the
        # verdict was read off. So: keep the evidence, withhold the verdict.
        provisional_shares = audit["gate_a"]["shares"]
        # A ratified registry run with --pre-audit is legitimate (a rehearsal), and
        # calling its registry unratified would be a false statement in the report.
        reason = (
            "--pre-audit was requested: this mode withholds every verdict by "
            f"construction, even though {overrides_path} is ratified"
            if metadata.get("_status") == "RATIFIED"
            else f"registry in {overrides_path} is not ratified "
            f"(_status: {metadata.get('_status')!r}): a gate verdict requires a "
            "ratified registry (§3.3); the per-regime shares under *Regime "
            "aggregates* above are provisional"
        )
        audit["gate_a"] = {"status": "not_evaluated", "reason": reason}
        audit["gate_b"] = {"status": "not_evaluated", "reason": reason}

    alphabets = {
        language: alphabet.observed_alphabet(
            mapped[mapped["language"] == language], cfg, language=language
        )
        for language in sorted(mapped["language"].unique())
    }
    emptied = sorted(language for language, ids in alphabets.items() if not ids)
    if emptied:
        raise ValueError(
            f"the configured mapping retains no symbol at all for {emptied}: |A| = 0 "
            "makes the add-β pseudo-mass β·|A| vanish and every downstream "
            "probability undefined (§3.4, §4.1)"
        )
    return {
        "pre_audit": pre_audit,
        "unassigned": unassigned,
        "overrides_path": overrides_path,
        "ud_release": cfg["corpus"]["ud_release"],
        "inventory": inventory,
        "contingency": audit["contingency"],
        "retention": audit["retention"],
        "excluded_upos": audit["excluded_upos_by_label"],
        "excluded_deprel": audit["excluded_deprel_by_label"],
        "by_regime": audit.get("by_regime"),
        "retention_by_regime": audit.get("retention_by_regime"),
        "restricted_fraction": audit.get("restricted_fraction"),
        "provisional_shares": provisional_shares,
        "gate_a": audit["gate_a"],
        "gate_b": audit["gate_b"],
        "alphabet_sizes": _alphabet_sizes(alphabets, cfg),
        "alphabet_head": _alphabet_head(mapped, alphabets),
        "alphabet_full": _alphabet_full(mapped, alphabets, cfg),
        "gates_evaluated": audit["gate_a"]["status"] == "evaluated",
        "has_registry": registry_frame is not None,
        "registry_status": metadata.get("_status"),
        "files": files,
    }


def _inventory(tokens, mapped, registry_frame) -> pd.DataFrame:
    """One row per document, with `n_tokens_retained` filled.

    With a registry this **is** the §2.3 registry schema: `build_registry` leaves
    `n_tokens_retained` null by design and documents that it must be complete
    before the G1 freeze, so filling it here is that step — not the freeze itself,
    which persists nothing and is not performed.

    Without a registry there is no document layer yet, so the rows are raw
    `sent_id` prefixes and the report says so.
    """
    retained = (
        mapped.groupby(["language", "doc_id"], sort=True)["kept"]
        .sum()
        .rename("n_tokens_retained")
    )
    if registry_frame is None:
        out = (
            tokens.groupby(["language", "doc_id"], sort=True)
            .agg(n_sentences=("sent_id", "nunique"), n_tokens_raw=("sent_id", "size"))
            .reset_index()
        )
        return out.merge(retained, on=["language", "doc_id"], how="left")

    out = registry_frame.drop(columns=["n_tokens_retained"]).merge(
        retained, on=["language", "doc_id"], how="left"
    )
    if out["n_tokens_retained"].isna().any():
        missing = sorted(out.loc[out["n_tokens_retained"].isna(), "doc_id"])
        raise ValueError(f"n_tokens_retained is incomplete for {missing}")
    # The drop/merge above appends the refilled column last. §2.3's order is the
    # schema, not a rendering preference, so it is restored rather than described.
    return out[list(registry.REGISTRY_COLUMNS)]


def _frame(rows, columns) -> pd.DataFrame:
    """Build from records but always keep the header: an empty list of dicts
    otherwise yields a column-less frame, and `to_csv` then writes a file with no
    header row at all — unreadable, and indistinguishable from a truncated write."""
    return pd.DataFrame(rows, columns=list(columns))


def _alphabet_sizes(alphabets, cfg) -> pd.DataFrame:
    return _frame(
        [
            {
                "language": language,
                "variant": cfg["alphabet"]["variant"],
                "excluded_deprel_policy": cfg["alphabet"]["excluded_deprel_policy"],
                "alphabet_size": len(ids),
            }
            for language, ids in sorted(alphabets.items())
        ],
        ("language", "variant", "excluded_deprel_policy", "alphabet_size"),
    )


def _alphabet_full(mapped, alphabets, cfg) -> pd.DataFrame:
    """The complete symbol -> id map, so the ordering rule is checkable end to end."""
    rows = []
    for language, ids in sorted(alphabets.items()):
        counts = mapped.loc[
            mapped["kept"] & (mapped["language"] == language), "symbol"
        ].value_counts()
        for symbol, symbol_id in sorted(ids.items(), key=lambda item: item[1]):
            rows.append(
                {
                    "language": language,
                    "variant": cfg["alphabet"]["variant"],
                    "excluded_deprel_policy": cfg["alphabet"]["excluded_deprel_policy"],
                    "symbol_id": symbol_id,
                    "symbol": symbol,
                    "n": int(counts[symbol]),
                    "frozen": False,
                }
            )
    return _frame(
        rows,
        (
            "language",
            "variant",
            "excluded_deprel_policy",
            "symbol_id",
            "symbol",
            "n",
            "frozen",
        ),
    )


def _alphabet_head(mapped, alphabets, per_language: int = 20) -> pd.DataFrame:
    """The top symbols of **each** language — a flat head would show only the first."""
    rows = []
    for language, ids in sorted(alphabets.items()):
        counts = mapped.loc[
            mapped["kept"] & (mapped["language"] == language), "symbol"
        ].value_counts()
        ranked = sorted(ids.items(), key=lambda item: item[1])[:per_language]
        for symbol, symbol_id in ranked:
            rows.append(
                {
                    "language": language,
                    "id": symbol_id,
                    "symbol": symbol,
                    "n": int(counts[symbol]),
                    "share_of_retained": int(counts[symbol]) / int(counts.sum()),
                }
            )
    return _frame(rows, ("language", "id", "symbol", "n", "share_of_retained"))


def main(argv=None) -> dict:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", default="data/raw", type=Path)
    parser.add_argument("--results-root", default="results", type=Path)
    parser.add_argument("--config", default=None, type=Path)
    parser.add_argument("--overrides", default="config/registry_overrides.yaml", type=Path)
    parser.add_argument(
        "--pre-audit",
        action="store_true",
        help="explicit incomplete mode: no gate verdict, no T*, nothing frozen",
    )
    parser.add_argument("--force", action="store_true", help="overwrite existing artifacts")
    args = parser.parse_args(argv)

    # Before git_state and before any write: the corpus is immutable and every
    # input is hashed into the run's identity, so artifacts landing inside it
    # corrupt both the data and the next run's fingerprint. Resolved on both
    # sides, so a symlink cannot walk in.
    data_root = args.data_root.resolve()
    results_root = args.results_root.resolve()
    if results_root == data_root or data_root in results_root.parents:
        raise ValueError(
            f"--results-root {results_root} is inside the data root {data_root}: "
            "the corpus is immutable and is hashed into every run's identity"
        )

    # Sampled before the first write: this stage's own artifacts land inside the
    # worktree, so asking git afterwards would report a dirtiness it just created.
    git = git_state()

    cfg = resolve_config(base=_load_base(args.config))
    check_against_default(cfg)
    files = discover_files(args.data_root)
    if not args.overrides.exists():
        raise FileNotFoundError(
            f"overrides file {args.overrides} does not exist; an absent file is not "
            "an empty registry (§3.3)"
        )

    # Read the bytes once, hash what was read, and parse a private copy of exactly
    # those bytes — so digest and content agree by construction, not by timing.
    with staged_inputs([*files, args.overrides]) as (snapshot, staged):
        tokens = read_tokens(files, set(cfg["corpus"]["languages"]), staged=staged)
        context = build_context(
            tokens,
            files,
            args.overrides,
            cfg,
            pre_audit=args.pre_audit,
            overrides_source=staged[args.overrides],
        )

    verify_inputs_unchanged(snapshot, files=files, data_root=args.data_root)

    sha = config_hash(cfg)
    fingerprint = inputs_fingerprint(snapshot)
    stamp = datetime.date.today().isoformat()

    # The mode is part of the artifact's identity, not a rendering detail: the same
    # data, config and overrides produce a withheld-verdict pre-audit and a
    # decided canonical audit. Sharing a run_id would let --force silently replace
    # one with the other, and would leave the manifest unable to say which it holds.
    mode = "preaudit" if args.pre_audit else "canonical"
    status = "PROVISIONAL" if args.pre_audit else "CANONICAL"
    # `entry_point` is the invocation, so the flag reaches every artifact's sidecar
    # too — a CSV separated from its filename still says which mode produced it.
    entry_point = f"{ENTRY_POINT} --pre-audit" if args.pre_audit else ENTRY_POINT
    # The software is part of the run's identity too: same day, same data, same
    # config and different code otherwise collide on run_id, and --force then
    # replaces evidence a different program produced. Placed before the date so
    # the stem reads mode / config / inputs / code / when.
    stem = f"{mode}_{sha[:12]}_{fingerprint[:12]}_{git['commit'][:12]}_{stamp}"
    run_id = f"audit_{stem}"

    tables = args.results_root / "tables"
    report_path = tables / f"audit_report_{stem}.md"
    csv_frames = {
        tables / f"contingency_by_document_{stem}.csv": context["contingency"],
        tables / f"alphabet_inventory_{stem}.csv": context["alphabet_full"],
    }
    if context["by_regime"] is not None:
        csv_frames[tables / f"contingency_by_regime_{stem}.csv"] = context["by_regime"]

    context |= {
        "run_id": run_id,
        "config_sha256": sha,
        "entry_point": entry_point,
        "csv_files": sorted(csv_frames, key=lambda path: path.name),
    }

    artifacts = [report_path, *sorted(csv_frames, key=lambda path: path.name)]
    # Order matters, and getting it wrong loses data. `_preflight` runs **outside**
    # the try: its own FileExistsError would otherwise fall into the rollback
    # below, which would delete the very pre-existing artifacts the refusal exists
    # to protect. Same for the reservation — the loser of a concurrent race must
    # not clean up the winner's output. Once both have passed, everything the
    # rollback touches is provably this run's own.
    _preflight(artifacts, args.results_root, run_id, args.force)
    log_dir = reserve_run(args.results_root, run_id, args.force)
    try:
        tables.mkdir(parents=True, exist_ok=True)
        for path, frame in csv_frames.items():
            # Every CSV carries its own status: detached from its filename and its
            # sidecar, a provisional table stays unmistakable for a canonical one.
            path.write_text(
                frame.assign(status=status).to_csv(index=False), encoding="utf-8"
            )
        report_path.write_text(render_report(context), encoding="utf-8")

        for artifact in artifacts:
            write_sidecar(artifact, run_id, entry_point, force=True)
        manifest = build_manifest(
            run_id,
            sha,
            derive_seed("audit", cfg["seeds"]["global"]),
            artifacts,
            entry_point,
            input_records=[
                {"path": str(path), "sha256": digest}
                for path, digest in sorted(snapshot.items())
            ],
            git=git,
        )
        # Declared additions to the D46 record (submitted for ratification with
        # D55): the mode as a field, so no consumer has to parse it out of run_id.
        manifest["mode"] = mode
        manifest["status"] = status
        manifest_path = write_manifest(manifest, args.results_root, force=True)
    except BaseException:
        # Roll the run back over the **predetermined destinations**, not over a
        # list of what was observed to succeed: a write that fails partway leaves a
        # truncated file behind and never reaches the line that would have recorded
        # it. `_preflight` has already proved none of these existed, so deleting
        # them destroys nothing but this run's own output, whole or partial.
        #
        # Under --force that proof is absent (a destination may hold a previous
        # run's artifact), so the partial state is left in place rather than
        # deleted — losing someone else's output is worse than leaving a mess.
        if not args.force:
            for path in destinations_of(artifacts, args.results_root, run_id):
                path.unlink(missing_ok=True)
            if log_dir.exists() and not any(log_dir.iterdir()):
                log_dir.rmdir()
        raise

    return {
        "run_id": run_id,
        "mode": mode,
        "report_path": report_path,
        "csv_files": context["csv_files"],
        "manifest_path": manifest_path,
        "gates_evaluated": context["gates_evaluated"],
        "has_registry": context["has_registry"],
        "n_tokens_raw": len(tokens),
    }


def reserve_run(results_root: Path, run_id: str, force: bool) -> Path:
    """Claim ``run_id`` atomically by creating its log directory.

    `_preflight` alone is a check-then-act: two runs with identical inputs can
    both find the destinations free and then both write, because the writers
    themselves are unconditional once the check has passed. A single exclusive
    `mkdir` is indivisible, so exactly one of any number of concurrent runs holds
    the identity and the rest are refused.
    """
    log_dir = Path(results_root) / "logs" / run_id
    if force:
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    try:
        log_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise FileExistsError(
            f"run_id {run_id!r} is already claimed at {log_dir}: a run with "
            "identical inputs holds this identity. Pass --force to replace it (§6.4)."
        ) from None
    return log_dir


def destinations_of(artifacts, results_root: Path, run_id: str) -> list[Path]:
    """Every path a successful run writes: artifacts, their sidecars, the manifest.

    One list, used twice — to refuse the run if any already exists, and to undo the
    run if it fails. Those two have to agree, or the rollback would miss a file the
    preflight had cleared.
    """
    return [
        *artifacts,
        *(path.with_suffix(path.suffix + ".sidecar.json") for path in artifacts),
        Path(results_root) / "logs" / run_id / "manifest.json",
    ]


def _preflight(artifacts, results_root: Path, run_id: str, force: bool) -> None:
    """Refuse the whole run before the first byte is written (§6.4).

    Writing progressively means a collision on a late output leaves the earlier
    ones behind: a failed run would still have replaced the CSVs of a previous one.
    Every destination — artifacts, their sidecars, the manifest — is checked up
    front, so the run is all-or-nothing. `force` still overwrites, but then it does
    so deliberately and completely.
    """
    if force:
        return
    existing = sorted(
        str(path) for path in destinations_of(artifacts, results_root, run_id)
        if path.exists()
    )
    if existing:
        raise FileExistsError(
            f"refusing to overwrite {len(existing)} existing artifact(s) without "
            f"--force (§6.4): {existing}"
        )


def _load_base(path):
    if path is None:
        return None
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
