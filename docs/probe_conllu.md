# `conllu` behaviour probe (P2, discovery only)

Ran 2026-07-26 against the locked environment. **No contract change**; this file
pins the runtime facts D54(ii)–(iv) deferred to "the synthetic fixture test
against the locked `conllu` version". None of the findings contradicts an
invariant of D54(ii)–(iii).

The complete probe is reproducible from the snippet below.

## Environment

- `conllu` version: **6.0.0**
- `conllu.parse_incr` present → streaming, one `TokenList` per sentence (D54(ii)).

## Findings vs D54

| D54 clause | Finding | Verdict |
| --- | --- | --- |
| (ii)(b) `newdoc id` metadata key | stored under key **`'newdoc id'`** (with a space), i.e. `tl.metadata['newdoc id']`; **not** `newdoc_id` | pinned |
| (ii)(c) integer-id tokens only | normal rows → `token['id']` is `int`; MWT range `i-j` → `tuple` `(1, '-', 2)`; empty node `i.1` → `tuple` `(4, '.', 1)`. Selector: `isinstance(token['id'], int)`. `TokenList.filter(id=lambda i: isinstance(i, int))` yields exactly the syntactic-word rows | pinned |
| (ii)(d) required fields | token keys: `id, form, lemma, upos, xpos, feats, head, deprel, deps, misc` — `ID, FORM, UPOS, HEAD, DEPREL` all present on a well-formed row | pinned |
| (ii)(a) `sent_id` | present in `metadata` when the comment exists; **absent from `metadata` entirely** when it does not (no exception from conllu) | reader must raise |
| (iii) UPOS validation | a non-UD UPOS (`NOTATAG`) is read back **untouched**; conllu does not validate the tag set | reader must validate |

## Malformed-row behaviour — TWO distinct cases (GREEN-phase note)

conllu does **not** uniformly fail loud, so the reader (D54(iv)) must handle both:

1. **Structurally short row** (fewer than 10 tab fields): conllu is **silent** and
   returns a truncated token, e.g. `1\tx\tx\tNOUN` → `{'id':1,'form':'x','lemma':'x','upos':'NOUN'}`
   with **no `head`/`deprel`**. The reader must itself check that the required
   fields are present and raise `ParseError`.
2. **Invalid `id` field** (e.g. `x` where an integer/range/empty id is expected):
   conllu **raises** `conllu.exceptions.ParseException: Failed parsing field
   'id': 'x' is not a valid ID.` The reader must catch this and re-raise as
   `ParseError` with location.

No line number is exposed on the raised `ParseException` — consistent with the
D54(iv) declared limitation (no source line number).

## Reproduction

```python
import io

import conllu
from conllu.exceptions import ParseException

doc = (
    "# newdoc id = doc-alpha\n# sent_id = doc-alpha@1\n"
    "1-2\tquoque\t_\t_\t_\t_\t_\t_\t_\t_\n"
    "1\tquo\tquo\tADV\t_\t_\t3\tadvmod\t_\t_\n"
    "4\t.\t.\tPUNCT\t_\t_\t3\tpunct\t_\t_\n"
    "4.1\t_\t_\tX\t_\t_\t_\t_\t_\t_\n\n"
)
tl, = conllu.parse_incr(io.StringIO(doc))
assert tl.metadata["newdoc id"] == "doc-alpha"
assert [type(t["id"]).__name__ for t in tl] == ["tuple", "int", "int", "tuple"]

missing_sent_id = "1\tx\tx\tNOUN\t_\t_\t0\troot\t_\t_\n\n"
missing, = conllu.parse_incr(io.StringIO(missing_sent_id))
assert "sent_id" not in missing.metadata

short_row = "# sent_id = short@1\n1\tx\tx\tNOUN\n\n"
short, = conllu.parse_incr(io.StringIO(short_row))
assert "head" not in short[0] and "deprel" not in short[0]

invalid_upos = "# sent_id = upos@1\n1\tx\tx\tNOTATAG\t_\t_\t0\troot\t_\t_\n\n"
upos, = conllu.parse_incr(io.StringIO(invalid_upos))
assert upos[0]["upos"] == "NOTATAG"

bad_id = "# sent_id = bad@1\nx\tx\tx\tNOUN\t_\t_\t0\troot\t_\t_\n\n"
try:
    next(conllu.parse_incr(io.StringIO(bad_id)))
except ParseException as exc:
    assert "Failed parsing field 'id'" in str(exc)
else:
    raise AssertionError("bad ID unexpectedly accepted")
```
