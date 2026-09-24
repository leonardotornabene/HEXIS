"""HORMATHOS corpus census and encoding. No model fitting or inference."""
import json
import math
from numbers import Integral
import re
from collections import Counter
from pathlib import Path

import pandas as pd

from hormathos import alphabet, conllu_reader
from hormathos.contracts import compare, digest

VARIANTS = ('ud23', 'ud23_oth', 'upos_only')
SENTENCE_KEY = ['doc_id', 'part_order', 'source_ordinal', 'sent_id']
SOURCE_COLUMNS = ['doc_id', 'sent_id', 'source_prefix', 'part_order', 'source_ordinal', 'source_rank']
COORDINATE_COLUMNS = ['variant', 'slot_uid', *SOURCE_COLUMNS, 'raw_token_id',
                      'encoded_index', 'symbol_id', 'available_past', 'eligible',
                      'upos_raw', 'deprel_raw']


def read_corpus(files, registry, *, staged=None):
    """Recompose numeric source order, independent of file and record order."""
    rows = {r['source_prefix']: r for r in registry}
    if len(rows) != len(registry):
        raise ValueError('registry: duplicate source_prefix')
    tokens, sentences, seen, ordinals = [], [], {}, set()
    for path in map(Path, files):
        source = staged[path] if staged else path
        try:
            for sentence in conllu_reader.iter_sentences(source):
                sid = sentence.metadata['sent_id']
                match = re.fullmatch(r'([^@]+)@([0-9]+)', sid)
                if not match:
                    raise ValueError(f'{path}: sent_id={sid!r}: expected prefix@numeric_ordinal')
                prefix, ordinal = match[1], int(match[2])
                if sid in seen or (prefix, ordinal) in ordinals:
                    raise ValueError(f'{path}: sent_id={sid!r}: duplicate identity/ordinal (previous {seen.get(sid)})')
                seen[sid] = str(path)
                ordinals.add((prefix, ordinal))
                if prefix not in rows:
                    raise ValueError(f'{path}: sent_id={sid!r}: unknown registry prefix {prefix!r}')
                declared = sentence.metadata.get('newdoc id')
                if declared is not None and declared != prefix:
                    raise ValueError(f'{path}: sent_id={sid!r}: contradictory newdoc id {declared!r}')
                r = rows[prefix]
                meta = {'language': 'grc', 'doc_id': r['canonical_doc_id'], 'sent_id': sid,
                        'source_prefix': prefix, 'part_order': r['part_order'],
                        'source_ordinal': ordinal, 'regime': r['regime'], 'role': r['role'],
                        'dependence_block': r['dependence_block'],
                        'group': 'PROSE_ALL' if r['regime'] in ('PROSE_CLASS', 'PROSE_POST') else r['regime']}
                sentences.append(meta | {'raw_length': len(sentence)})
                for token in sentence:
                    tokens.append(meta | {'raw_token_id': token['id'], 'token_ord': token['id'],
                                         'upos_raw': token['upos'], 'deprel_raw': token['deprel'],
                                         'lemma_raw': token.get('lemma')})
        except conllu_reader.ParseError as exc:
            raise conllu_reader.ParseError(path, exc.sent_id, exc.token_id, exc.reason) from exc
    if not sentences or not tokens:
        raise ValueError(f'{list(files)}: no syntactic words/sentences')
    s = pd.DataFrame(sentences).sort_values(SENTENCE_KEY).reset_index(drop=True)
    s['source_rank'] = s.groupby('source_prefix', sort=False).cumcount()
    t = pd.DataFrame(tokens).merge(s[['sent_id', 'source_rank']], on='sent_id', validate='many_to_one')
    t = t.sort_values(SENTENCE_KEY + ['raw_token_id']).reset_index(drop=True)
    return t, s


def diagnostic_a(raw, cfg):
    """Each excluded relation separately; denominator includes all raw tokens."""
    rep = cfg['representation']
    eligible_upos = raw['upos_raw'].replace(rep['source_map_before_retention']).isin(rep['source_upos_keep_before_merge'])
    relations = raw['deprel_raw'].str.lower().str.split(':').str[0]
    excluded = raw.loc[eligible_upos & ~relations.isin(rep['deprel_keep'])].copy()
    excluded['deprel_base'] = relations.loc[excluded.index]
    result = []
    for level, key in [('document', 'doc_id'), ('block', 'dependence_block'), ('regime', 'regime')]:
        denominators = raw.groupby(key, observed=True).size()
        for (label, relation), count in excluded.groupby([key, 'deprel_base'], observed=True).size().items():
            total = int(denominators[label]); share = int(count) / total
            result.append({'level': level, 'unit': label, 'deprel_base': relation,
                           'count': int(count), 'raw': total, 'share_of_raw': share,
                           'flagged': share > rep['gate_A']['threshold']})
    return pd.DataFrame(result, columns=['level','unit','deprel_base','count','raw','share_of_raw','flagged'])


def _counts(series):
    return {str(key): int(value) for key, value in sorted(Counter(series).items())}


def encode_corpus(raw, sentences, cfg, alphabets):
    """One transform for audit and encode; every source sentence is retained."""
    coords, sequences, documents, exclusions, inventories = [], [], [], [], {}
    source_docs = {}
    for doc, group in raw.groupby('doc_id', sort=True):
        source_docs[doc] = {'raw': len(group), 'raw_upos': _counts(group['upos_raw']),
                            'raw_lemma_gar_by_upos': _counts(group.loc[group['lemma_raw'].eq('γάρ'), 'upos_raw'])}
    registry = pd.DataFrame(cfg['registry'])
    for variant in VARIANTS:
        mapped = alphabet.map_tokens(raw, cfg, variant=variant)
        kept = mapped.loc[mapped['kept']].copy()
        symbols = alphabets['alphabets'][variant]['symbols']
        observed = sorted(set(kept['symbol']))
        unknown = set(observed) - set(symbols)
        if unknown:
            bad = kept.loc[kept['symbol'].isin(unknown)].iloc[0]
            raise ValueError(f"alphabet {variant}: unknown {sorted(unknown)} at {bad['sent_id']} token {bad['raw_token_id']}")
        ids = {symbol: i for i, symbol in enumerate(symbols)}
        kept['symbol_id'] = kept['symbol'].map(ids).astype('int64')
        kept['encoded_index'] = kept.groupby('sent_id', sort=False).cumcount()
        kept['available_past'] = kept['encoded_index']
        kept['eligible'] = kept['encoded_index'] >= cfg['min_available_past']
        kept['slot_uid'] = range(len(kept)); kept['variant'] = variant
        coords.append(kept[COORDINATE_COLUMNS])
        dropped = mapped.loc[~mapped['kept'], SOURCE_COLUMNS + ['raw_token_id','upos_raw','deprel_raw','deprel_base','drop_reason']].copy()
        dropped.insert(0, 'variant', variant); exclusions.append(dropped)
        grouped = kept.groupby('sent_id', sort=False)
        symbol_lists = grouped['symbol_id'].agg(list).to_dict()
        id_lists = grouped['raw_token_id'].agg(list).to_dict()
        slots = grouped['slot_uid'].agg(list).to_dict()
        seq = sentences.copy(); seq.insert(0, 'variant', variant)
        seq['symbols'] = [symbol_lists.get(sid, []) for sid in seq['sent_id']]
        seq['raw_token_ids'] = [id_lists.get(sid, []) for sid in seq['sent_id']]
        seq['slot_uids'] = [slots.get(sid, []) for sid in seq['sent_id']]
        seq['boundary'] = 'reset'; seq['encoded_length'] = seq['symbols'].map(len)
        seq['eligible_count'] = (seq['encoded_length'] - cfg['min_available_past']).clip(lower=0)
        sequences.append(seq)
        primary_symbols = set(kept.loc[kept['role'].eq('primary'), 'symbol'])
        exclusive = sorted(set(kept['symbol']) - primary_symbols)
        inventories[variant] = {'m': len(observed), 'symbols': observed,
                                'symbols_canonical_sha256': digest(observed),
                                'inventory_only_exclusive_symbols': exclusive}
        for doc, group in seq.groupby('doc_id', sort=True):
            entries = registry[registry['canonical_doc_id'].eq(doc)].sort_values('part_order')
            r = entries.iloc[0].to_dict(); r.pop('source_prefix'); r.pop('canonical_doc_id'); r.pop('part_order')
            r['flags'] = json.dumps(r['flags'], ensure_ascii=False)
            total = int(group['raw_length'].sum()); n = int(group['encoded_length'].sum())
            documents.append(r | {'variant': variant, 'doc_id': doc,
                'source_prefixes': json.dumps(entries['source_prefix'].tolist()),
                'parts': json.dumps(entries['part_order'].tolist()), 'group': group['group'].iloc[0],
                'raw': total, 'sentences': len(group), 'kept': n,
                'eligible': int(group['eligible_count'].sum()),
                'eligibility_scope': 'potential_census_only' if r['role']=='inventory_only' else 'primary_targets',
                'retention': n/total if total else 0.0, 'eligible_fraction': int(group['eligible_count'].sum())/n if n else 0.0,
                'empty': int(group['encoded_length'].eq(0).sum()),
                'without_target': int(group['eligible_count'].eq(0).sum()),
                'max_sentence': int(group['encoded_length'].max()),
                'length_counts': json.dumps(_counts(group['encoded_length']), sort_keys=True),
                'gate_B_flagged': n/total < cfg['representation']['gate_B']['threshold'] if total else True})
    docs = pd.DataFrame(documents)
    seqs = pd.concat(sequences, ignore_index=True)
    raw_rel_upos = {rel: _counts(group['upos_raw']) for rel, group in raw.groupby('deprel_raw',sort=True)}
    source = {'raw_tokens': len(raw), 'raw_sentences': len(sentences),
              'raw_upos': _counts(raw['upos_raw']), 'raw_relations': _counts(raw['deprel_raw']),
              'raw_relation_upos': raw_rel_upos,
              'base_relation_count': raw['deprel_raw'].str.lower().str.split(':').str[0].nunique(),
              'full_relation_label_count': raw['deprel_raw'].nunique(),
              'source_prefix_sentences': _counts(sentences['source_prefix']), 'documents': source_docs}
    contingency=[]
    summaries=[]
    for level, key in [('document','doc_id'), ('block','dependence_block'), ('regime','regime')]:
        counts = raw.groupby([key,'upos_raw','deprel_raw'], observed=True).size().rename('count').reset_index().rename(columns={key:'unit'})
        counts.insert(0,'level',level); contingency.append(counts)
        for (variant, unit), group in seqs.groupby(['variant',key], observed=True, sort=True):
            n = int(group['encoded_length'].sum()); total=int(group['raw_length'].sum()); eligible=int(group['eligible_count'].sum())
            summaries.append({'variant':variant,'level':level,'unit':unit,'raw':total,'sentences':len(group),
                              'kept':n,'eligible':eligible,'retention':n/total if total else 0.0,
                              'eligible_fraction':eligible/n if n else 0.0,
                              'empty':int(group['encoded_length'].eq(0).sum()),
                              'without_target':int(group['eligible_count'].eq(0).sum()),
                              'length_counts':json.dumps(_counts(group['encoded_length']),sort_keys=True)})
    result = {'documents.csv':docs, 'coordinates.parquet':pd.concat(coords,ignore_index=True),
              'sequences.parquet':seqs, 'exclusions.parquet':pd.concat(exclusions,ignore_index=True),
              'alphabets.json':inventories, 'source_audit.json':source,
              'audit_summary.csv':pd.DataFrame(summaries),
              'audit_contingency.csv':pd.concat(contingency,ignore_index=True),
              'audit_A.csv':diagnostic_a(raw,cfg)}
    return result


def verify_corpus(artifacts, contracts):
    """Exact census, key and sequence/coordinate content equality; fail loudly."""
    d, expected = contracts['design'], contracts['expected']
    source = artifacts['source_audit.json']
    for key in ('raw_tokens','raw_sentences'):
        compare(source[key],d['expected'][key],key)
    for key in ('raw_upos','raw_relations','raw_relation_upos','base_relation_count','full_relation_label_count','source_prefix_sentences'):
        compare(source[key],expected[key],key)
    compare(artifacts['alphabets.json'],contracts['alphabets']['alphabets'],'alphabets')
    docs, coords, seqs = (artifacts[k] for k in ('documents.csv','coordinates.parquet','sequences.parquet'))
    doc_expected = {r['doc_id']:r for r in expected['documents']}
    wanted={(v,doc) for v in VARIANTS for doc in doc_expected}
    keys=list(docs[['variant','doc_id']].itertuples(index=False,name=None))
    if len(keys)!=len(set(keys)) or set(keys)!=wanted:
        raise ValueError('documents: missing/extra/duplicate variant/doc_id keys')
    for row in docs.to_dict('records'):
        want=doc_expected[row['doc_id']]; v=row['variant']
        for key in ('raw','sentences','regime','role','dependence_block'):
            compare(None if want[key] is None and pd.isna(row[key]) else row[key],want[key],f"{v}/{row['doc_id']}/{key}")
        for key in ('kept','eligible','empty','max_sentence'):
            compare(row[key],want[key][v],f"{v}/{row['doc_id']}/{key}")
        for key,value in {'retention':row['kept']/row['raw'],
                          'eligible_fraction':row['eligible']/row['kept'] if row['kept'] else 0.0,
                          'gate_B_flagged':row['kept']/row['raw'] < d['representation']['gate_B']['threshold']}.items():
            if not math.isclose(row[key],value,rel_tol=0,abs_tol=1e-14):
                raise ValueError(f'documents: {key} mismatch')
        for key in ('raw','raw_upos','raw_lemma_gar_by_upos'):
            compare(source['documents'][row['doc_id']][key],want[key],f"source/{row['doc_id']}/{key}")
    for block in d['blocks']:
        for v in VARIANTS:
            rows=docs[docs['variant'].eq(v)&docs['doc_id'].isin(block['docs'])]
            for key in ('kept','eligible'):
                compare(int(rows[key].sum()),block[key][v],f'{v}/{block["block"]}/{key}')
            compare(int(rows['sentences'].sum()),block['sentences'],f'{v}/{block["block"]}/sentences')
    excluded=artifacts['exclusions.parquet']
    if set(excluded['variant'])!=set(VARIANTS) or excluded.duplicated(['variant','sent_id','raw_token_id']).any():
        raise ValueError('exclusions: variant or key mismatch')
    for variant in VARIANTS:
        dropped=excluded[excluded['variant'].eq(variant)]
        decisions={pair:alphabet.map_token(*pair,d,variant=variant) for pair in set(zip(dropped['upos_raw'],dropped['deprel_raw']))}
        for row in dropped.itertuples(index=False):
            decision=decisions[(row.upos_raw,row.deprel_raw)]
            if decision.kept or row.drop_reason!=decision.drop_reason or row.deprel_base!=decision.deprel_base:
                raise ValueError(f'{variant}/{row.sent_id}: exclusion reason mismatch')
        union=pd.concat([coords[coords['variant'].eq(variant)][SOURCE_COLUMNS+['raw_token_id']],dropped[SOURCE_COLUMNS+['raw_token_id']]])
        if union.duplicated(['sent_id','raw_token_id']).any():
            raise ValueError('retained/excluded overlap')
        s=seqs[seqs['variant'].eq(variant)].set_index('sent_id')
        counts=union.groupby('sent_id',observed=True).size().reindex(s.index,fill_value=0)
        if not counts.eq(s['raw_length']).all() or set(union['sent_id'])-set(s.index):
            raise ValueError('retained/excluded partition mismatch')
    verify_sequences(coords, seqs, d, contracts['alphabets'])
    c0=coords[coords['variant'].eq('ud23')]; upos=coords[coords['variant'].eq('upos_only')]
    columns=SOURCE_COLUMNS+['raw_token_id','encoded_index','available_past','eligible']
    if not c0[columns].reset_index(drop=True).equals(upos[columns].reset_index(drop=True)):
        raise ValueError('C0/UPOS coordinate/mask mismatch')
    for variant in VARIANTS:
        subset=seqs[seqs['variant'].eq(variant)]
        compare(len(subset),d['expected']['raw_sentences'],f'{variant}/sentence count')
        for role,tokenkey,eligiblekey in [('primary','primary_tokens','primary_eligible'),('inventory_only','inventory_only_tokens','inventory_only_potential_eligible')]:
            rows=docs[docs['variant'].eq(variant)&docs['role'].eq(role)]
            compare(int(rows['kept'].sum()),d['expected'][tokenkey][variant],f'{variant}/{role}/kept')
            compare(int(rows['eligible'].sum()),d['expected'][eligiblekey][variant],f'{variant}/{role}/eligible')


def verify_sequences(coords, seqs, cfg, alphabets):
    if list(coords.columns)!=COORDINATE_COLUMNS:
        raise ValueError('coordinates: missing/extra or reordered schema columns')
    integer_columns=['slot_uid','part_order','source_ordinal','source_rank','raw_token_id','encoded_index','symbol_id','available_past']
    for column in integer_columns:
        if not pd.api.types.is_integer_dtype(coords[column]) or coords[column].isna().any():
            raise ValueError(f'coordinates.{column}: non-null integer required')
    if not pd.api.types.is_bool_dtype(coords['eligible']) or coords['eligible'].isna().any():
        raise ValueError('coordinates.eligible: non-null boolean required')
    for column in ['raw_length','source_ordinal','source_rank','part_order','encoded_length','eligible_count']:
        if not pd.api.types.is_integer_dtype(seqs[column]) or seqs[column].isna().any():
            raise ValueError(f'sequences.{column}: non-null integer required')
    for column in ['symbols','raw_token_ids','slot_uids']:
        if any(not isinstance(value,Integral) or isinstance(value,bool) for row in seqs[column] for value in row):
            raise ValueError(f'sequences.{column}: integer elements required')
    if set(coords['variant'])!=set(VARIANTS) or set(seqs['variant'])!=set(VARIANTS):
        raise ValueError('coordinates/sequences: missing or extra variant')
    if coords.duplicated(['variant','slot_uid']).any() or coords.duplicated(['variant','sent_id','raw_token_id']).any():
        raise ValueError('coordinates: duplicate key')
    if seqs.duplicated(['variant','sent_id']).any():
        raise ValueError('sequences: duplicate sentence')
    registry={r['source_prefix']:r for r in cfg['registry']}
    reference_ids=set(seqs.loc[seqs['variant'].eq('ud23'),'sent_id'])
    for variant in VARIANTS:
        c=coords[coords['variant'].eq(variant)].reset_index(drop=True)
        s=seqs[seqs['variant'].eq(variant)].reset_index(drop=True)
        if set(s['sent_id'])!=reference_ids:
            raise ValueError('variant sentence key mismatch')
        if c.assign(doc_id=c['doc_id'].astype(str)).sort_values(
                SENTENCE_KEY+['encoded_index']).index.tolist()!=list(range(len(c))):
            raise ValueError(f'{variant}: noncanonical coordinate order')
        if c['slot_uid'].tolist()!=list(range(len(c))):
            raise ValueError(f'{variant}: nonconsecutive slot_uid')
        if s.assign(doc_id=s['doc_id'].astype(str)).sort_values(
                SENTENCE_KEY).index.tolist()!=list(range(len(s))):
            raise ValueError(f'{variant}: noncanonical sentence order')
        if not s['boundary'].eq('reset').all():
            raise ValueError('sentence boundary must reset')
        if s['source_rank'].tolist()!=s.groupby('source_prefix',sort=False,observed=True).cumcount().tolist():
            raise ValueError('source_rank mismatch')
        for row in s.itertuples(index=False):
            prefix,ordinal=row.sent_id.rsplit('@',1)
            r=registry.get(prefix)
            if not r or prefix!=row.source_prefix or not re.fullmatch(r'[0-9]+',ordinal) or int(ordinal)!=row.source_ordinal or r['canonical_doc_id']!=row.doc_id or r['part_order']!=row.part_order:
                raise ValueError(f'{row.sent_id}: source identity mismatch')
            group='PROSE_ALL' if r['regime'] in ('PROSE_CLASS','PROSE_POST') else r['regime']
            block=None if pd.isna(row.dependence_block) else row.dependence_block
            if row.role!=r['role'] or row.regime!=r['regime'] or row.group!=group or block!=r['dependence_block']:
                raise ValueError(f'{row.sent_id}: role/regime mismatch')
        lengths=s['symbols'].map(len)
        if not lengths.eq(s['encoded_length']).all() or not (lengths-4).clip(lower=0).eq(s['eligible_count']).all():
            raise ValueError('sequence length/eligibility mismatch')
        ranks=c.groupby('sent_id',sort=False,observed=True).cumcount()
        if not ranks.eq(c['encoded_index']).all() or not ranks.eq(c['available_past']).all() or not ranks.ge(4).eq(c['eligible']).all():
            raise ValueError('coordinates: index/history/eligibility mismatch')
        try:
            expected=s.loc[lengths.gt(0),SOURCE_COLUMNS+['symbols','raw_token_ids','slot_uids']].explode(['symbols','raw_token_ids','slot_uids']).rename(columns={'symbols':'symbol_id','raw_token_ids':'raw_token_id','slot_uids':'slot_uid'}).reset_index(drop=True)
            columns=SOURCE_COLUMNS+['symbol_id','raw_token_id','slot_uid']
            pd.testing.assert_frame_equal(c[columns],expected[columns],check_dtype=False,check_categorical=False)
        except (ValueError,AssertionError) as exc:
            raise ValueError(f'{variant}: sequence/coordinate content mismatch: {exc}') from exc
        symbols=alphabets['alphabets'][variant]['symbols']
        if not c['symbol_id'].between(0,len(symbols)-1).all():
            raise ValueError(f'{variant}: symbol outside frozen alphabet')
        mapping={pair:alphabet.map_token(*pair,cfg,variant=variant).symbol for pair in set(zip(c['upos_raw'],c['deprel_raw']))}
        if [symbols[int(i)] for i in c['symbol_id']] != [mapping[pair] for pair in zip(c['upos_raw'],c['deprel_raw'])]:
            raise ValueError(f'{variant}: symbol mismatch')


def build_corpus(files, cfg, contracts, *, staged=None):
    raw, sentences = read_corpus(files,cfg['registry'],staged=staged)
    artifacts = encode_corpus(raw,sentences,cfg,contracts['alphabets'])
    verify_corpus(artifacts,contracts)
    return artifacts
