"""Shared synthetic CoNLL-U fixtures for the reader tests (Spec §3.2; D54).

Built per the P5 brief and the conllu-6.0.0 probe (docs/probe_conllu.md):
a well-formed sentence with an MWT range row, an empty node, a PUNCT token and a
`newdoc id`; a sentence lacking `sent_id`; and a sentence with a malformed
(short) row missing HEAD/DEPREL at a known token id.
"""

import pytest

_T = "\t"


def _row(*cols):
    return _T.join(cols)


_VALID = "\n".join(
    [
        "# newdoc id = alpha",
        "# sent_id = alpha@1",
        "# text = quoque canit .",
        _row("1-2", "quoque", "_", "_", "_", "_", "_", "_", "_", "_"),  # MWT range → dropped
        _row("1", "quo", "quo", "ADV", "_", "_", "3", "advmod", "_", "_"),
        _row("2", "que", "que", "CCONJ", "_", "_", "3", "cc", "_", "_"),
        _row("3", "canit", "cano", "VERB", "_", "_", "0", "root", "_", "_"),
        _row("4", ".", ".", "PUNCT", "_", "_", "3", "punct", "_", "_"),  # kept unchanged (D54 iii)
        _row("4.1", "_", "_", "X", "_", "_", "_", "_", "_", "_"),  # empty node → dropped
        "",
        "# sent_id = alpha@2",
        "# text = arma virum",
        _row("1", "arma", "arma", "NOUN", "_", "_", "2", "obj", "_", "_"),
        _row("2", "virum", "vir", "NOUN", "_", "_", "0", "root", "_", "_"),
        "",
    ]
)

_MISSING_SENT_ID = "\n".join(
    [
        "# newdoc id = beta",
        "# text = no sent id here",
        _row("1", "arma", "arma", "NOUN", "_", "_", "0", "root", "_", "_"),
        "",
    ]
)

# Token id=2 is a short row (4 fields): HEAD and DEPREL absent → the reader must
# raise ParseError located at sent_id gamma@1, token_id 2 (conllu is silent here).
_MALFORMED = "\n".join(
    [
        "# sent_id = gamma@1",
        "# text = arma virum",
        _row("1", "arma", "arma", "NOUN", "_", "_", "0", "root", "_", "_"),
        _row("2", "virum", "virum", "NOUN"),
        "",
    ]
)

_INVALID_UPOS = "\n".join(
    [
        "# sent_id = delta@1",
        _row("1", "arma", "arma", "NOTATAG", "_", "_", "0", "root", "_", "_"),
        "",
    ]
)

_EMPTY_DEPREL = "\n".join(
    [
        "# sent_id = epsilon@1",
        _row("1", "arma", "arma", "NOUN", "_", "_", "0", "", "_", "_"),
        "",
    ]
)

_INVALID_ID = "\n".join(
    [
        "# sent_id = zeta@1",
        _row("x", "arma", "arma", "NOUN", "_", "_", "0", "root", "_", "_"),
        "",
    ]
)

_REPRESENTATION_BLIND = "\n".join(
    [
        "# sent_id = eta@1",
        _row("1", ".", ".", "PUNCT", "_", "_", "4", "punct", "_", "_"),
        _row("2", "ignotum", "ignotum", "X", "_", "_", "4", "discourse", "_", "_"),
        _row("3", "heu", "heu", "INTJ", "_", "_", "4", "vocative", "_", "_"),
        _row("4", "+", "+", "SYM", "_", "_", "0", "dep", "_", "_"),
        "",
    ]
)

_LAZY = "\n".join(
    [
        "# sent_id = theta@1",
        _row("1", "arma", "arma", "NOUN", "_", "_", "0", "root", "_", "_"),
        "",
        "# sent_id = theta@2",
        _row("1", "virum", "virum", "NOUN"),
        "",
    ]
)

_OUT_OF_ORDER = "\n".join(
    [
        "# sent_id = iota@1",
        _row("2", "virum", "vir", "NOUN", "_", "_", "0", "root", "_", "_"),
        _row("1", "arma", "arma", "NOUN", "_", "_", "2", "obj", "_", "_"),
        "",
    ]
)


@pytest.fixture
def conllu_samples(tmp_path):
    def _write(name, content):
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        return path

    return {
        "valid": _write("valid.conllu", _VALID),
        "missing_sent_id": _write("missing_sent_id.conllu", _MISSING_SENT_ID),
        "malformed": _write("malformed.conllu", _MALFORMED),
        "invalid_upos": _write("invalid_upos.conllu", _INVALID_UPOS),
        "empty_deprel": _write("empty_deprel.conllu", _EMPTY_DEPREL),
        "invalid_id": _write("invalid_id.conllu", _INVALID_ID),
        "representation_blind": _write(
            "representation_blind.conllu", _REPRESENTATION_BLIND
        ),
        "lazy": _write("lazy.conllu", _LAZY),
        "out_of_order": _write("out_of_order.conllu", _OUT_OF_ORDER),
    }
