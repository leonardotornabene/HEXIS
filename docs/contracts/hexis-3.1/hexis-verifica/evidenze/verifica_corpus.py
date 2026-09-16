"""Read-only HEXIS corpus audit. No project imports and no model fits.

Run: python3 hexis_corpus_recount.py --repo /path/to/hexis --zip /path/to/HEXIS_allegati_operativi_v3_2026-09-11.zip
The JSON report is printed to standard output. Redirect only to a new file.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--zip', type=Path, required=True)
args = parser.parse_args()
with zipfile.ZipFile(args.zip) as archive:
    design = json.loads(archive.read('HEXIS_v3_allegati/hexis_v3_design.json'))
    expected = json.loads(archive.read('HEXIS_v3_allegati/corpus_atteso.json'))
registry = {r['source_prefix']: r for r in design['registry']}
keep = set('ADJ ADP ADV AUX CCONJ DET NOUN NUM PART PRON SCONJ VERB'.split())
relations = set('root nsubj csubj obj iobj ccomp xcomp obl advcl advmod acl amod appos det nummod nmod case mark aux cop cc conj parataxis'.split())
variants = ['ud23', 'ud23_oth', 'upos_only']
documents = defaultdict(list)
prefixes = Counter()
raw_upos = Counter()
raw_relations = Counter()
raw_relation_upos = defaultdict(Counter)
seen = set()
hashes = {}
for source in design['source_hashes']:
    path = args.repo / 'data/raw/UD_Ancient_Greek-Perseus' / source['file']
    data = path.read_bytes()
    hashes[path.name] = hashlib.sha256(data).hexdigest()
    assert hashes[path.name] == source['sha256'], path
    sid, rows = None, []
    for line_no, line in enumerate(data.decode().splitlines() + [''], 1):
        if line.startswith('# sent_id = '):
            sid = line.split(' = ', 1)[1]
            assert sid not in seen, (path, line_no, sid)
            seen.add(sid)
        elif line and not line.startswith('#'):
            fields = line.split('\t')
            assert len(fields) == 10, (path, line_no)
            if fields[0].isdigit():
                rows.append(fields)
                raw_upos[fields[3]] += 1
                raw_relations[fields[7]] += 1
                raw_relation_upos[fields[7]][fields[3]] += 1
        elif not line and sid:
            prefix = sid.rsplit('@', 1)[0]
            entry = registry[prefix]
            prefixes[prefix] += 1
            documents[entry['canonical_doc_id']].append((entry, rows))
            sid, rows = None, []
assert set(prefixes) == set(registry)
assert not raw_upos['PROPN'] and not raw_upos['SYM']
alphabets = defaultdict(set)
coarse = defaultdict(set)
summary = []
blocks = defaultdict(Counter)
lemma_counts = defaultdict(Counter)
for doc, sentences in sorted(documents.items()):
    entry = sentences[0][0]
    counts = Counter()
    lengths = defaultdict(list)
    for _, rows in sentences:
        counts['raw'] += len(rows)
        sequences = defaultdict(list)
        for f in rows:
            upos = 'NOUN' if f[3] == 'PROPN' else f[3]
            relation = f[7].lower().split(':', 1)[0]
            if entry['role'] == 'primary':
                block = entry['dependence_block']
                blocks[block]['raw_' + f[3]] += 1
                if f[2] in ['γάρ', 'δέ', 'τε', 'μέν', 'οὐ', 'μή', 'καί']:
                    lemma_counts[block + ' | ' + f[2]][f'{upos}:{relation} / {f[4]}'] += 1
            assert upos in keep | {'PUNCT', 'X', 'INTJ', 'SYM'}
            if upos not in keep:
                counts['drop_upos_' + upos] += 1
                continue
            sequences['ud23_oth'].append(upos + ':' + (relation if relation in relations else 'oth'))
            if relation in relations:
                sequences['ud23'].append(upos + ':' + relation)
                sequences['upos_only'].append(upos)
            else:
                counts['drop_rel_' + relation] += 1
        for variant in variants:
            sequence = sequences[variant]
            n = len(sequence)
            lengths[variant].append(n)
            counts['kept_' + variant] += n
            counts['eligible_' + variant] += max(0, n - 4)
            counts['empty_' + variant] += n == 0
            alphabets[variant, entry['role']].update(sequence)
            for symbol in sequence:
                upos, sep, dep = symbol.partition(':')
                upos = 'ADV_PART' if upos in {'ADV', 'PART'} else upos
                coarse[variant, entry['role']].add(upos + sep + dep)
    counts['sentences'] = len(sentences)
    wanted = next(x for x in expected['documents'] if x['doc_id'] == doc)
    for key in ['raw', 'sentences']:
        assert counts[key] == wanted[key], (doc, key)
    for variant in variants:
        for key in ['kept', 'eligible', 'empty']:
            assert counts[key + '_' + variant] == wanted[key][variant], (doc, key, variant)
        assert max(lengths[variant]) == wanted['max_sentence'][variant], (doc, variant)
    summary.append({'doc': doc, 'work': entry['work'], 'role': entry['role'], 'regime': entry['regime'], **counts})
    if entry['role'] == 'primary':
        blocks[entry['dependence_block']].update(counts)
support = {}
for name, inventory in [('original', alphabets), ('ADV_PART', coarse)]:
    support[name] = {}
    for variant in variants:
        primary = inventory[variant, 'primary']
        probe = inventory[variant, 'probe']
        support[name][variant] = {'all': len(primary | probe), 'primary': len(primary), 'probe_exclusive': sorted(probe - primary)}
result = {'hashes': hashes, 'prefixes': dict(prefixes), 'n_documents': len(documents), 'n_sentences': len(seen), 'raw_upos': dict(raw_upos), 'raw_relations': dict(raw_relations), 'raw_relation_upos': dict(raw_relation_upos), 'relation_base_count': len({r.split(':', 1)[0] for r in raw_relations}), 'support': support, 'documents': summary, 'blocks': dict(blocks), 'lemma_counts': dict(lemma_counts), 'expected_document_checks': 'all passed'}
print(json.dumps(result, ensure_ascii=False, indent=2))
