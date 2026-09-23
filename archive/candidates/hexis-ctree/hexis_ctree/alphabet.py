"""Fixed symbolic alphabet for UPOS+DEPREL sequences.

Design rule (HEXIS): the alphabet is fixed *ex ante* over the pooled corpus
(or supplied explicitly from the pre-registered restricted tag set) and is
shared by every model in a comparison. The alphabet size d enters the
smoothing denominator of S&G Eq. (21); comparability of code lengths across
models therefore requires a single, frozen d. Symbols unseen by the alphabet
are a hard error (fail loudly), never silently smoothed in.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

Sentence = Sequence[str]
Document = Sequence[Sentence]


class Alphabet:
    """Immutable, deterministic bidirectional mapping symbol <-> integer id.

    Symbol ids are assigned by lexicographic order of the symbol strings, so
    that the mapping is a pure function of the symbol *set* (independent of
    corpus order); this keeps every downstream computation deterministic.
    """

    __slots__ = ("_symbols", "_index")

    def __init__(self, symbols: Iterable[str]):
        unique = sorted(set(symbols))
        if not unique:
            raise ValueError("Alphabet cannot be empty.")
        for s in unique:
            if not isinstance(s, str) or s == "":
                raise ValueError(f"Alphabet symbols must be non-empty strings (got {s!r}).")
        if len(unique) < 2:
            raise ValueError("Alphabet must contain at least 2 symbols.")
        self._symbols: Tuple[str, ...] = tuple(unique)
        self._index: Dict[str, int] = {s: i for i, s in enumerate(self._symbols)}

    # ------------------------------------------------------------------ #
    @classmethod
    def from_documents(cls, documents: Iterable[Document]) -> "Alphabet":
        """Build the alphabet from the realized symbol set of a corpus."""
        seen: set = set()
        for doc in documents:
            for sentence in doc:
                seen.update(sentence)
        return cls(seen)

    # ------------------------------------------------------------------ #
    @property
    def symbols(self) -> Tuple[str, ...]:
        return self._symbols

    def __len__(self) -> int:
        return len(self._symbols)

    def __contains__(self, symbol: str) -> bool:
        return symbol in self._index

    def id_of(self, symbol: str) -> int:
        try:
            return self._index[symbol]
        except KeyError:
            raise ValueError(
                f"Symbol {symbol!r} is not in the fixed alphabet "
                f"(d={len(self)}). The alphabet is fixed ex ante; "
                "unseen symbols indicate an upstream normalization error."
            ) from None

    def symbol_of(self, symbol_id: int) -> str:
        return self._symbols[symbol_id]

    def encode_sentence(self, sentence: Sentence) -> List[int]:
        """Map a sentence (list of symbol strings) to integer ids.

        Raises
        ------
        ValueError
            If the sentence is empty or contains an out-of-alphabet symbol.
        """
        if len(sentence) == 0:
            raise ValueError(
                "Empty sentence encountered. Post-normalization empty "
                "sentences must be handled (excluded) upstream; refusing to "
                "process them silently."
            )
        return [self.id_of(s) for s in sentence]

    def to_dict(self) -> dict:
        return {"symbols": list(self._symbols)}

    def __repr__(self) -> str:  # pragma: no cover
        return f"Alphabet(d={len(self)})"
