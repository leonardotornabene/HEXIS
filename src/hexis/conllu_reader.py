"""CoNLL-U streaming reader: identity, order and localized errors (§11.1)."""

import re
from pathlib import Path
from typing import Iterator

import conllu
from conllu.exceptions import ParseException

# UPOS is validated against the whole UD tag set — all 17 tags, not the 12 the
# representation retains: the reader is representation-blind, and the source
# audit needs the raw contingency over every syntactic-word row.
UD_UPOS_TAGS = frozenset(
    "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".split()
)

# Required columns, as `conllu` names them.
REQUIRED_FIELDS = ("id", "form", "upos", "head", "deprel")


class ParseError(ValueError):
    """A CoNLL-U source is malformed.

    `sent_id` and `token_id` are nullable: a violation may precede their
    availability. There is no source line number — the parser does not expose
    one, and that limitation is declared rather than faked.
    """

    def __init__(
        self,
        path: Path,
        sent_id: str | None,
        token_id: int | None,
        reason: str,
    ) -> None:
        self.path = path
        self.sent_id = sent_id
        self.token_id = token_id
        self.reason = reason
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"{self.path}: sent_id={self.sent_id} token_id={self.token_id}: {self.reason}"
        )


def iter_sentences(path: Path) -> Iterator[conllu.TokenList]:
    """Yield validated sentences from a CoNLL-U file.

    Streaming, one sentence at a time. Each yielded `TokenList` carries the
    source metadata (`sent_id` mandatory, `newdoc id` when present) and only
    integer-ID rows: MWT ranges `i-j` and empty nodes `i.1` are removed, so the
    retained rows are the syntactic words. Token order is CoNLL-U ID order.

    The reader is representation-blind: it validates UPOS membership in the 17
    UD tags and DEPREL non-emptiness, and nothing else. Retention, deletion,
    subtype stripping and the merge belong to `alphabet.map_token` (§4.1).

    The yielded object is derived and filtered — not a re-serializable image of
    the source sentence.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as handle:
        for block in conllu.parse_sentences(handle):
            metadata = {}
            rows = []
            for line in block.splitlines():
                if line.startswith("#"):
                    key, separator, value = line[1:].partition("=")
                    key, value = key.strip(), value.strip()
                    if separator and key in ("sent_id", "newdoc id"):
                        if key in metadata:
                            raise ParseError(path, metadata.get("sent_id"), None, f"duplicate metadata {key}")
                        metadata[key] = value
                else:
                    rows.append(line)
            sid = metadata.get("sent_id")
            if not sid:
                raise ParseError(path, None, None, "sent_id is mandatory and nonempty")
            for line in rows:
                cols = line.split("\t")
                raw_id = cols[0]
                token_id = int(raw_id) if raw_id.isdigit() else None
                if len(cols) != 10:
                    raise ParseError(path, sid, token_id, f"expected 10 columns, got {len(cols)}")
                if not re.fullmatch(r"[1-9][0-9]*(?:[-.][1-9][0-9]*)?", raw_id):
                    raise ParseError(path, sid, token_id, f"invalid raw ID {raw_id!r}")
                if token_id is not None and (not cols[1] or cols[1] == "_" or not cols[6].isdigit()):
                    raise ParseError(path, sid, token_id, "FORM and nonnegative integer HEAD are required")
            try:
                sentence = conllu.parse(block)[0]
            except ParseException as exc:
                raise ParseError(path, sid, None, f"conllu rejected the source: {exc}") from exc
            yield _validated(path, sentence)


def _validated(path: Path, sentence: conllu.TokenList) -> conllu.TokenList:
    sent_id = sentence.metadata.get("sent_id")
    if sent_id is None:
        raise ParseError(path, None, None, "sent_id is mandatory (Spec §3.2)")

    tokens = sentence.filter(id=lambda value: isinstance(value, int))
    previous_id = None
    for token in tokens:
        token_id = token.get("id")
        if previous_id is not None and token_id <= previous_id:
            raise ParseError(
                path,
                sent_id,
                token_id,
                f"integer token IDs are not in CoNLL-U order after {previous_id}",
            )
        previous_id = token_id
        missing = [field for field in REQUIRED_FIELDS if field not in token]
        if missing:
            raise ParseError(
                path,
                sent_id,
                token_id,
                "missing required column(s): " + ", ".join(f.upper() for f in missing),
            )
        if token["upos"] not in UD_UPOS_TAGS:
            raise ParseError(
                path, sent_id, token_id, f"UPOS {token['upos']!r} is not a UD tag"
            )
        # `_` is CoNLL-U's unspecified marker; §3.2 requires DEPREL non-empty.
        if not token["deprel"] or token["deprel"] == "_":
            raise ParseError(path, sent_id, token_id, "DEPREL is empty")
    return tokens
