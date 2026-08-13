"""CoNLL-U streaming reader (Spec §3.2, §6.2; D54/D54-A1)."""

from pathlib import Path
from typing import Iterator

import conllu
from conllu.exceptions import ParseException

# Spec §3.2 validates UPOS against the UD tag set — all 17 tags, not the 12
# retained by §3.4: the reader is representation-blind (D54(iii)) and the G1
# audit (T2) needs the raw contingency over every syntactic-word row.
UD_UPOS_TAGS = frozenset(
    "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".split()
)

# Spec §3.2 required columns, as `conllu` names them.
REQUIRED_FIELDS = ("id", "form", "upos", "head", "deprel")


class ParseError(ValueError):
    """A CoNLL-U source violates Spec §3.2 (D54(iv)).

    `sent_id` and `token_id` are nullable: a violation may precede their
    availability. No source line number — `conllu.parse_incr` does not expose
    one (declared limitation, D54(iv)).
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
    """Yield validated sentences from a CoNLL-U file (Spec §3.2; D54(ii)/D54-A1).

    Streaming, one sentence at a time. Each yielded `TokenList` carries the
    source metadata (`sent_id` mandatory, `newdoc id` when present) and only
    integer-ID rows: MWT ranges `i-j` and empty nodes `i.1` are removed, so the
    retained syntactic-word rows *are* the Latin clitic expansion. Token order
    is CoNLL-U ID order.

    The reader is representation-blind (D54(iii)): it validates UPOS membership
    in the 17 UD tags and DEPREL non-emptiness, and nothing else. Retention,
    deletion and subtype stripping belong to `alphabet.map_token` (§3.4).

    The yielded object is derived and filtered — not a re-serializable image of
    the source sentence (D54(ii)(f)).
    """
    with path.open(encoding="utf-8") as handle:
        sentences = conllu.parse_incr(handle)
        while True:
            try:
                sentence = next(sentences)
            except StopIteration:
                return
            except ParseException as exc:
                raise ParseError(path, None, None, f"conllu rejected the source: {exc}") from exc
            yield _validated(path, sentence)


def _validated(path: Path, sentence: conllu.TokenList) -> conllu.TokenList:
    sent_id = sentence.metadata.get("sent_id")
    if sent_id is None:
        raise ParseError(path, None, None, "sent_id is mandatory (Spec §3.2)")

    tokens = sentence.filter(id=lambda value: isinstance(value, int))
    for token in tokens:
        token_id = token.get("id")
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
