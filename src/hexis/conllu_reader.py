"""CoNLL-U streaming reader (Spec §3.2, §6.2; D54/D54-A1)."""


def iter_sentences(path):
    """Yield validated sentences from a CoNLL-U file (Spec §3.2).

    Per sentence: read sent_id (mandatory — fail loudly if absent) and newdoc id
    if present; skip MWT range lines (i-j), keeping syntactic-word rows (expands
    Latin clitics, §2.2/E3); skip empty nodes (i.1); require ID, FORM, UPOS,
    HEAD, DEPREL; validate UPOS in the UD tag set and DEPREL non-empty; on
    violation raise with file, sent_id, token id. Surface order = CoNLL-U ID
    order. D54/D54-A1 freezes the public Path → Iterator[conllu.TokenList]
    contract; behavior remains unimplemented in this Phase-0 scaffold.
    """
    raise NotImplementedError
