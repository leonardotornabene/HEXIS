"""V1 independent synthetic cases and exact real census (no model fits)."""
import copy
import dataclasses
from pathlib import Path

import pandas as pd
import pytest

from hexis.alphabet import map_token, map_tokens, strip_subtype
from hexis.config import load_v31_config
from hexis.contracts import load_contracts
from hexis.corpus import read_corpus, encode_corpus, build_corpus, verify_corpus, diagnostic_a

pytestmark = pytest.mark.v31


def sentence(sid, tags, ids=None):
    ids = ids or list(range(1,len(tags)+1))
    return '# sent_id = '+sid+'\n'+''.join(f'{i}\tw\tw\t{u}\t_\t_\t0\t{d}\t_\t_\n' for i,(u,d) in zip(ids,tags))+'\n'


def mini(tmp_path):
    cfg = load_v31_config()
    row = cfg['registry'][0]
    prefix = row['source_prefix']
    path = tmp_path/'mini.conllu'
    path.write_text(sentence(prefix+'@10',[('NOUN','nsubj')]*6,[1,3,4,5,8,9])+sentence(prefix+'@2',[('PUNCT','punct')]))
    return cfg, path, prefix


def test_numeric_order_raw_coordinates_empty_reset_and_targets(tmp_path):
    cfg,path,prefix = mini(tmp_path)
    raw, sentences = read_corpus([path], cfg['registry'])
    assert sentences['source_ordinal'].tolist() == [2,10]
    assert sentences['source_rank'].tolist() == [0,1]
    out = encode_corpus(raw,sentences,cfg,load_contracts()['alphabets'])
    seq = out['sequences.parquet'].query("variant == 'ud23'")
    assert seq['symbols'].tolist()[0] == []
    assert seq['boundary'].tolist() == ['reset','reset']
    coords=out['coordinates.parquet'].query("variant == 'ud23'")
    assert coords['raw_token_id'].tolist() == [1,3,4,5,8,9]
    assert coords['slot_uid'].tolist() == list(range(6))
    assert coords['available_past'].tolist() == list(range(6))
    assert coords['eligible'].tolist() == [False]*4+[True]*2
    assert coords['encoded_index'].tolist() == list(range(6))


def test_athenaeus_parts_order_before_ordinal(tmp_path):
    cfg=load_v31_config();rows=[r for r in cfg['registry'] if r['dependence_block']=='ATHENAEUS']
    path=tmp_path/'mini.conllu'
    path.write_text(sentence(rows[1]['source_prefix']+'@1',[('NOUN','root')])+sentence(rows[0]['source_prefix']+'@99',[('NOUN','root')]))
    raw,sents=read_corpus([path],cfg['registry'])
    assert sents['part_order'].tolist()==[12,13]
    assert sents['source_ordinal'].tolist()==[99,1]
    assert sents['doc_id'].nunique()==1
    assert set(raw['regime'])=={'PROSE_POST'}
    assert set(raw['group'])=={'PROSE_ALL'}


@pytest.mark.parametrize('bad', ['duplicate', 'ordinal_collision', 'invalid_ordinal', 'unknown_prefix', 'newdoc'])
def test_ambiguous_identities_fail_with_source(tmp_path,bad):
    cfg,path,prefix=mini(tmp_path)
    sid=prefix+'@1'
    content=sentence(sid,[('NOUN','root')])
    if bad=='duplicate':content*=2
    if bad=='ordinal_collision':content+=sentence(prefix+'@01',[('NOUN','root')])
    if bad=='invalid_ordinal':content=sentence(prefix+'@x',[('NOUN','root')])
    if bad=='unknown_prefix':content=sentence('missing@1',[('NOUN','root')])
    if bad=='newdoc':content='# newdoc id = wrong\n'+content
    path.write_text(content)
    with pytest.raises(ValueError) as exc:read_corpus([path],cfg['registry'])
    assert path.name in str(exc.value)
    assert '@' in str(exc.value)


@pytest.mark.parametrize('tag',['ADV_PART','unknown','',None])
def test_public_mapping_rejects_unknown_source_upos(tag):
    with pytest.raises(ValueError,match='UPOS') as exc:map_token(tag,'root',load_v31_config())
    assert str(exc.value)


def test_global_merge_subtypes_masks_and_frozen_ids(tmp_path):
    cfg,path,prefix=mini(tmp_path)
    tags=[('PART','ADVMOD:emph'),('ADV','advmod'),('PROPN','nsubj'),('NOUN','vocative'),('INTJ','discourse')]
    path.write_text(sentence(prefix+'@1',tags))
    raw,sents=read_corpus([path],cfg['registry'])
    out=encode_corpus(raw,sents,cfg,load_contracts()['alphabets'])
    c=out['coordinates.parquet'];a=load_contracts()['alphabets']['alphabets']
    assert c.query("variant=='ud23'")['raw_token_id'].tolist()==[1,2,3]
    assert c.query("variant=='upos_only'")['raw_token_id'].tolist()==[1,2,3]
    assert c.query("variant=='ud23_oth'")['raw_token_id'].tolist()==[1,2,3,4]
    assert c.query("variant=='ud23'")['symbol_id'].tolist()==[a['ud23']['symbols'].index('ADV_PART:advmod')]*2+[a['ud23']['symbols'].index('NOUN:nsubj')]
    assert len(out['exclusions.parquet'])==5
    with pytest.raises(ValueError,match='alphabet') as exc:
        path.write_text(sentence(prefix+'@1',[('NUM','aux')]))
        raw,sents=read_corpus([path],cfg['registry']);encode_corpus(raw,sents,cfg,load_contracts()['alphabets'])
    assert 'NUM:aux' in str(exc.value)


def test_input_file_order_does_not_change_corpus(tmp_path):
    cfg,path,prefix=mini(tmp_path);other=tmp_path/'other.conllu'
    other.write_text(sentence(prefix+'@3',[('ADV','advmod')]))
    first=read_corpus([path,other],cfg['registry']);second=read_corpus([other,path],cfg['registry'])
    for a,b in zip(first,second):pd.testing.assert_frame_equal(a,b)
    assert first[1]['source_ordinal'].tolist()==[2,3,10]


def test_diagnostic_a_uses_allowed_upos_per_relation_and_raw_denominator():
    raw=pd.DataFrame({'doc_id':['d']*100,'dependence_block':['b']*100,'regime':['HEX']*100,
        'upos_raw':['INTJ']*80+['NOUN']*20,'deprel_raw':['discourse']*80+['vocative']*2+['orphan']*3+['root']*15})
    result=diagnostic_a(raw,load_v31_config())
    regime=result.query("level=='regime'").set_index('deprel_base')
    assert regime.loc['vocative','share_of_raw']==.02
    assert not regime.loc['vocative','flagged']
    assert regime.loc['orphan','share_of_raw']==.03
    assert regime.loc['orphan','flagged']
    assert 'discourse' not in regime.index


@pytest.fixture(scope='module')
def real_corpus():
    cfg=load_v31_config();contracts=load_contracts()
    root=Path(__file__).resolve().parents[1]/'data/raw/UD_Ancient_Greek-Perseus'
    return build_corpus(sorted(root.glob('*.conllu')),cfg,contracts)


def test_real_corpus_exact_expected_counts_keys_and_inventories(real_corpus):
    assert len(real_corpus['documents.csv'])==51
    assert len(real_corpus['sequences.parquet'])==41757
    assert len(real_corpus['coordinates.parquet'])==530720
    coords=real_corpus['coordinates.parquet']
    assert not coords.duplicated(['variant','slot_uid']).any()
    assert not coords.duplicated(['variant','sent_id','raw_token_id']).any()
    keys=['doc_id','sent_id','source_prefix','part_order','source_ordinal','source_rank','raw_token_id','encoded_index','available_past','eligible']
    pd.testing.assert_frame_equal(coords.query("variant=='ud23'")[keys].reset_index(drop=True),coords.query("variant=='upos_only'")[keys].reset_index(drop=True))
    assert real_corpus['source_audit.json']['raw_tokens']==202989
    assert real_corpus['source_audit.json']['raw_sentences']==13919
    for variant,count in [('ud23',9),('ud23_oth',10),('upos_only',0)]:
        assert len(real_corpus['alphabets.json'][variant]['inventory_only_exclusive_symbols'])==count


def test_exact_validator_detects_equal_length_content_and_key_corruption(real_corpus):
    broken=dict(real_corpus);broken['coordinates.parquet']=real_corpus['coordinates.parquet'].copy()
    broken['coordinates.parquet'].loc[0,'symbol_id']=999
    with pytest.raises(ValueError) as exc:verify_corpus(broken,load_contracts())
    assert str(exc.value)
    broken['coordinates.parquet']=real_corpus['coordinates.parquet'].copy()
    broken['coordinates.parquet'].loc[0,'slot_uid']=1
    with pytest.raises(ValueError) as exc:verify_corpus(broken,load_contracts())
    assert str(exc.value)


@pytest.mark.parametrize('fault',['duplicate_metadata','short','long','invalid_id','zero_id','missing_head','empty_sent_id'])
def test_source_parser_rejects_malformed_rows_with_location(tmp_path,fault):
    from hexis.conllu_reader import iter_sentences, ParseError
    sid='alpha@1';content=sentence(sid,[('NOUN','root')])
    if fault=='duplicate_metadata':content='# sent_id = alpha@1\n'+content
    if fault=='short':content=f'# sent_id = {sid}\n1\tw\tw\tNOUN\n\n'
    if fault=='long':content=content.replace('\troot\t_\t_','\troot\t_\t_\textra')
    if fault=='invalid_id':content=content.replace('\n1\t','\nx\t')
    if fault=='zero_id':content=content.replace('\n1\t','\n0\t')
    if fault=='missing_head':content=content.replace('\t0\troot','\t_\troot')
    if fault=='empty_sent_id':content=content.replace(sid,'')
    path=tmp_path/'bad.conllu';path.write_text(content)
    with pytest.raises(ParseError) as exc:list(iter_sentences(path))
    assert path.name in str(exc.value)
    assert exc.value.reason
    if fault!='empty_sent_id':assert exc.value.sent_id==sid


def test_mwt_and_empty_nodes_do_not_change_source_word_ids(tmp_path,conllu_samples):
    from hexis.conllu_reader import iter_sentences
    source=list(iter_sentences(conllu_samples['valid']))[0]
    assert [t['id'] for t in source]==[1,2,3,4]
    assert source.metadata['sent_id']=='alpha@1'


@pytest.mark.parametrize('fault',['extra_variant','source_rank','valid_wrong_symbol','eligibility','exclusion_reason','retention'])
def test_validator_rejects_semantic_corruption_at_unchanged_cardinality(real_corpus,fault):
    broken=dict(real_corpus)
    if fault in ('extra_variant','source_rank','valid_wrong_symbol','eligibility'):
        name='coordinates.parquet';broken[name]=real_corpus[name].copy()
        column,value={'extra_variant':('variant','extra'), 'source_rank':('source_rank',999),
                      'valid_wrong_symbol':('symbol_id',(int(broken[name].loc[0,'symbol_id'])+1)%100),
                      'eligibility':('eligible',True)}[fault]
        broken[name].loc[0,column]=value
    elif fault=='exclusion_reason':
        name='exclusions.parquet';broken[name]=real_corpus[name].copy();broken[name].loc[0,'drop_reason']='wrong'
    else:
        name='documents.csv';broken[name]=real_corpus[name].copy();broken[name].loc[0,'retention']=0.0
    with pytest.raises(ValueError) as exc:verify_corpus(broken,load_contracts())
    assert str(exc.value)


def test_b_is_diagnostic_and_keeps_low_retention_documents(tmp_path):
    cfg,path,prefix=mini(tmp_path)
    raw,sents=read_corpus([path],cfg['registry']);out=encode_corpus(raw,sents,cfg,load_contracts()['alphabets'])
    assert not out['documents.csv']['gate_B_flagged'].any()
    path.write_text(sentence(prefix+'@1',[('PUNCT','punct')]*9+[('NOUN','root')]))
    raw,sents=read_corpus([path],cfg['registry']);out=encode_corpus(raw,sents,cfg,load_contracts()['alphabets'])
    assert out['documents.csv']['gate_B_flagged'].all()
    assert out['documents.csv']['retention'].tolist()==[.1]*3


def test_coordinate_schema_does_not_silently_cast_float_ids(real_corpus):
    broken=dict(real_corpus);broken['coordinates.parquet']=real_corpus['coordinates.parquet'].copy()
    broken['coordinates.parquet']['symbol_id']=broken['coordinates.parquet']['symbol_id'].astype(float)
    with pytest.raises(ValueError,match='integer') as exc:verify_corpus(broken,load_contracts())
    assert str(exc.value)


# --- mapping unit cases carried over from the v2.1 alphabet suite ----------------
# Same properties, restated on the 3.1 rules: three variants, ADV/PART merged after
# retention, unknown source UPOS refused instead of dropped.

VERIFIED_SUBTYPES = {'acl:relcl':'acl','advcl:abs':'advcl','advcl:cmp':'advcl','advcl:pred':'advcl',
 'advmod:neg':'advmod','advmod:emph':'advmod','advmod:lmod':'advmod','advmod:tmod':'advmod',
 'aux:pass':'aux','nsubj:pass':'nsubj','nsubj:outer':'nsubj','obl:arg':'obl','obl:cmp':'obl',
 'ccomp:reported':'ccomp','conj:expl':'conj','det:numgov':'det','nummod:gov':'nummod',
 'flat:name':'flat','flat:redup':'flat','csubj:pass':'csubj'}


def test_subtype_stripping_is_total_and_lowercases_every_colon():
    for raw, expected in VERIFIED_SUBTYPES.items():
        assert strip_subtype(raw) == expected
    assert strip_subtype('root') == 'root'
    assert strip_subtype('ADVMOD:EMPH') == 'advmod'
    assert strip_subtype('obl:arg:extra') == 'obl'
    assert strip_subtype('') == ''


def test_propn_is_mapped_to_noun_before_retention():
    cfg = load_v31_config()
    mapped = map_token('PROPN', 'nsubj', cfg, variant='ud23')
    assert (mapped.upos, mapped.symbol, mapped.kept) == ('NOUN', 'NOUN:nsubj', True)
    assert map_token('PROPN', 'nsubj', cfg, variant='upos_only').symbol == 'NOUN'


@pytest.mark.parametrize('variant', ['ud23', 'ud23_oth', 'upos_only'])
@pytest.mark.parametrize('upos', ['PUNCT', 'X', 'INTJ', 'SYM'])
def test_excluded_source_upos_drops_before_any_deprel_rule(variant, upos):
    """Order of operations: an excluded UPOS carrying an excluded deprel is reported
    as upos_excluded, in every variant and under either deprel policy."""
    mapped = map_token(upos, 'vocative', load_v31_config(), variant=variant)
    assert (mapped.kept, mapped.symbol, mapped.drop_reason) == (False, None, 'upos_excluded')


def test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth():
    cfg = load_v31_config()
    dropped = map_token('NOUN', 'vocative', cfg, variant='ud23')
    assert (dropped.kept, dropped.symbol, dropped.drop_reason) == (False, None, 'deprel_excluded:vocative')
    assert map_token('NOUN', 'flat:name', cfg, variant='ud23').drop_reason == 'deprel_excluded:flat'
    absorbed = map_token('NOUN', 'vocative', cfg, variant='ud23_oth')
    assert (absorbed.kept, absorbed.symbol, absorbed.deprel_base) == (True, 'NOUN:oth', 'vocative')
    assert map_token('NOUN', 'nsubj', cfg, variant='ud23_oth').symbol == 'NOUN:nsubj'


def test_the_merge_follows_retention_so_an_excluded_token_keeps_its_source_upos():
    """§4.1: ADV/PART become ADV_PART only where the token is retained. The same
    PART token is ADV_PART under oth and plain PART in the C0 exclusions."""
    cfg = load_v31_config()
    assert map_token('PART', 'advmod', cfg, variant='ud23').symbol == 'ADV_PART:advmod'
    assert map_token('PART', 'discourse', cfg, variant='ud23_oth').symbol == 'ADV_PART:oth'
    excluded = map_token('PART', 'discourse', cfg, variant='ud23')
    assert (excluded.upos, excluded.kept) == ('PART', False)


def test_mapped_token_is_immutable():
    mapped = map_token('NOUN', 'nsubj', load_v31_config(), variant='ud23')
    with pytest.raises(dataclasses.FrozenInstanceError):
        mapped.symbol = 'VERB:root'
    assert mapped.symbol == 'NOUN:nsubj'


def test_map_tokens_keeps_a_boolean_mask_on_an_empty_table():
    """The empty table is a declared case; `kept` must stay a boolean mask and not
    become an object column, which no downstream mask would accept."""
    columns = ['language', 'doc_id', 'sent_id', 'token_ord', 'upos_raw', 'deprel_raw']
    mapped = map_tokens(pd.DataFrame(columns=columns), load_v31_config(), variant='ud23')
    assert len(mapped) == 0
    assert mapped['kept'].dtype == bool


def test_an_unknown_alphabet_variant_is_refused():
    """The three variants are the whole cell space; a fourth name is a mistyped run,
    not a new representation."""
    with pytest.raises(ValueError, match='variant') as exc:
        map_token('NOUN', 'nsubj', load_v31_config(), variant='ud23_bad')
    assert str(exc.value)
