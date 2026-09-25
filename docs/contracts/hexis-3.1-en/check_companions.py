"""A5 check of the English companions (non-normative): header hash, structure, numbers.
Usage: python check_companions.py <repo root> <pairs.json>; pairs = [[original, translation, slice?]]."""
import hashlib, json, re, sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1]); pairs = json.loads(Path(sys.argv[2]).read_text())

def section(text, spec):
    if not spec: return text
    start, end = spec
    return text[text.index(start):text.index(end)]

def numbers(text, italian):
    text = re.sub(r'`[^`]*`', ' ', text)                      # identifiers, hashes, paths
    text = re.sub(r'\]\([^)]*\)', ']', text)                  # link targets
    text = re.sub(r'\b[0-9a-f]{16,}\b', ' ', text)
    text = re.sub(r'§§?\s?[\d.,–]+', ' ', text)                # section references keep their notation
    text = text.replace('[0,1]', ' ').replace('(0,1)', ' ').replace('{,}', ',')     # LaTeX decimal comma                          # interval notation, identical in both
    out = []
    for tok in re.findall(r'\d[\d.,]*\d|\d', text):
        if italian:
            tok = re.sub(r'\.(?=\d{3}(\D|$))', '', tok).replace(',', '.')
        else:
            tok = re.sub(r',(?=\d{3}(\D|$))', '', tok)
        out.append(tok.rstrip('.'))
    return Counter(out)

def shape(text):
    lines = text.splitlines()
    return {'headings': [len(l) - len(l.lstrip('#')) for l in lines if re.match(r'#{1,6} ', l)],
            'table_rows': sum(1 for l in lines if l.startswith('|')),
            'formula_blocks': text.count('\\['), 'code_fences': text.count('```'),
            'list_items': sum(1 for l in lines if re.match(r'\s*(\d+\.|-) ', l))}

bad = 0
for original, translation, *spec in pairs:
    if '::' in original:                                   # member of a ZIP: 'archive.zip::member'
        import zipfile
        archive, member = original.split('::', 1)
        o_bytes = zipfile.ZipFile(root/archive).read(member)
    else:
        o_bytes = (root/original).read_bytes()
    o = section(o_bytes.decode(), spec[0] if spec else None)
    digest = hashlib.sha256(o.encode()).hexdigest()
    t = (root/translation).read_text()
    head, _, body = t.partition('\n\n')
    problems = []
    if digest not in head or 'Italian original governs' not in head:
        problems.append('header lacks the original SHA-256 or the governance line')
    so, st = shape(o), shape(body)
    for k in so:
        if so[k] != st[k]: problems.append(f'{k}: {so[k] if k!="headings" else len(so[k])} vs {st[k] if k!="headings" else len(st[k])}')
    fence = r'```[a-z]*\n.*?\n```'
    ob, tb = re.findall(fence, o, re.S), re.findall(fence, body, re.S)
    same = [b for b in ob if b in tb]                       # code reproduced verbatim: compared as bytes, not as numbers
    oo, bb = o, body
    for b in same: oo, bb = oo.replace(b, ' '), bb.replace(b, ' ')
    no, nt = numbers(oo, True), numbers(bb, False)
    missing = no - nt
    if missing: problems.append(f'numbers missing in translation: {dict(missing)}')
    status = 'OK ' if not problems else 'FAIL'
    bad += bool(problems)
    print(f'{status} {translation} ({len(body.split())} words; sha {digest[:12]})')
    for p in problems: print('     ', p)
sys.exit(1 if bad else 0)
