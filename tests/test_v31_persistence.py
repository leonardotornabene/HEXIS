"""V1 run identity, atomic stages and corruption refusal on small fixtures."""
import json
from pathlib import Path

import pandas as pd
import pytest

from hexis.contracts import digest, load_contracts
from hexis.pipeline.corpus_run import discover_inputs, publish_stage, validate_run, run_identity
from hexis.manifest import sha256_file

pytestmark = pytest.mark.v31


def test_exact_three_inputs_and_hashes(tmp_path):
    c=load_contracts();root=Path(__file__).resolve().parents[1]/'data/raw/UD_Ancient_Greek-Perseus'
    files=discover_inputs(root,c['design'])
    assert len(files)==3
    for p in files:
        assert sha256_file(p)==next(r['sha256'] for r in c['design']['source_hashes'] if r['file']==p.name)
    with pytest.raises(ValueError,match='missing') as exc:discover_inputs(tmp_path,c['design'])
    assert str(exc.value)
    for p in files:(tmp_path/p.name).write_bytes(p.read_bytes())
    extra=tmp_path/'extra.conllu';extra.write_text('')
    with pytest.raises(ValueError,match='extra') as exc:discover_inputs(tmp_path,c['design'])
    assert str(exc.value)
    extra.unlink();(tmp_path/files[0].name).write_text('corrupt')
    with pytest.raises(ValueError,match='hash') as exc:discover_inputs(tmp_path,c['design'])
    assert str(exc.value)


def test_identity_excludes_locations_and_is_sensitive_to_components():
    components={'contract':'a','code':'b','data':{'x':'c'},'registry':'d','alphabets':'e','configuration':'f','lock':'g','rng':'h'}
    assert run_identity(components)==digest(components)
    other=dict(components);other['code']='changed'
    assert run_identity(other)!=run_identity(components)


def payload():
    return {'test.csv':pd.DataFrame({'id':[0,1],'value':['x','y']}),
            'test.parquet':pd.DataFrame({'id':[0,1],'values':[[1,2],[]]}),
            'test.json':{'status':'fixture'}}


def test_atomic_roundtrip_and_same_run_in_distinct_directories(tmp_path):
    contract={'fixture':'v1'}
    a=publish_stage(tmp_path/'a','audit',payload(),contract,{'input':'one'})
    b=publish_stage(tmp_path/'b','audit',payload(),contract,{'input':'two'})
    assert a['run_id']==b['run_id']
    assert a['artifacts']==b['artifacts']
    assert a['scientific_complete'] is False
    assert a['corpus_complete'] is False
    assert validate_run(tmp_path/'a')['run_id']==a['run_id']
    pd.testing.assert_frame_equal(pd.read_csv(tmp_path/'a/test.csv'),payload()['test.csv'])
    assert pd.read_parquet(tmp_path/'a/test.parquet')['values'].map(list).tolist()==[[1,2],[]]
    assert a['artifacts']['test.csv']['rows']==2
    assert a['artifacts']['test.parquet']['schema']


def test_encode_updates_one_manifest_without_overwriting_audit(tmp_path):
    out=tmp_path/'run';contract={'fixture':'v1'}
    a=publish_stage(out,'audit',{'a.json':{'x':1}},contract,{})
    b=publish_stage(out,'encode',{'a.json':{'x':1},'b.json':{'x':2}},contract,{})
    assert a['run_id']==b['run_id']
    assert b['completed_stages']==['audit','encode']
    assert b['corpus_complete'] and not b['scientific_complete']
    assert len(list(out.glob('*manifest*')))==1
    before=(out/'manifest.json').read_bytes()
    with pytest.raises(FileExistsError) as exc:publish_stage(out,'encode',{'b.json':{}},contract,{})
    assert str(exc.value)
    assert (out/'manifest.json').read_bytes()==before


@pytest.mark.parametrize('fault',['bytes','extra','missing','schema','rows','identity'])
def test_corruption_prevents_stage_reuse(tmp_path,fault):
    out=tmp_path/'run';publish_stage(out,'audit',payload(),{'fixture':'v1'},{})
    if fault=='bytes':(out/'test.json').write_text('{}')
    if fault=='extra':(out/'extra.json').write_text('{}')
    if fault=='missing':(out/'test.csv').unlink()
    if fault in ('schema','rows','identity'):
        m=json.loads((out/'manifest.json').read_text())
        if fault=='identity':m['run_id']='incorrect'
        else:m['artifacts']['test.csv'][fault]=0 if fault=='rows' else []
        (out/'manifest.json').write_text(json.dumps(m))
    with pytest.raises(ValueError) as exc:validate_run(out)
    assert str(exc.value)


def test_interrupted_write_never_publishes_stage(tmp_path,monkeypatch):
    from hexis.pipeline import corpus_run
    out=tmp_path/'run'
    def fail(path, value):
        path.write_text('partial')
        raise RuntimeError('interrupted')
    monkeypatch.setattr(corpus_run,'write_artifact',fail)
    with pytest.raises(RuntimeError,match='interrupted') as exc:publish_stage(out,'audit',payload(),{'fixture':'v1'},{})
    assert str(exc.value)
    assert not (out/'manifest.json').exists()
    assert not list(out.glob('test.*')) if out.exists() else True


def test_destinations_with_existing_files_are_preserved(tmp_path):
    out=tmp_path/'run';out.mkdir();sentinel=out/'test.csv';sentinel.write_text('keep')
    with pytest.raises((ValueError,FileExistsError)) as exc:publish_stage(out,'audit',payload(),{'fixture':'v1'},{})
    assert str(exc.value)
    assert sentinel.read_text()=='keep'


def test_output_raw_and_symlink_rejected(tmp_path):
    from hexis.pipeline.corpus_run import check_destination
    raw=tmp_path/'raw';raw.mkdir();link=tmp_path/'alias';link.symlink_to(raw,target_is_directory=True)
    for path in [raw/'output',link/'output']:
        with pytest.raises(ValueError,match='raw') as exc:check_destination(path,raw)
        assert str(exc.value)


def test_input_staging_binds_hash_to_processed_bytes_and_detects_changes(tmp_path):
    from hexis.pipeline.legacy_audit import staged_inputs, verify_inputs_unchanged
    path=tmp_path/'one.conllu';path.write_bytes(b'original')
    with staged_inputs([path]) as (snapshot, staged):
        path.write_bytes(b'changed')
        assert staged[path].read_bytes()==b'original'
        assert snapshot[path]==sha256_file(staged[path])
        with pytest.raises(RuntimeError,match='edited') as exc:
            verify_inputs_unchanged(snapshot,files=[path],data_root=tmp_path)
        assert str(exc.value)
        path.write_bytes(b'original')
        extra=tmp_path/'nested'/'extra.conllu';extra.parent.mkdir();extra.write_bytes(b'new')
        with pytest.raises(RuntimeError,match='appeared') as exc:
            verify_inputs_unchanged(snapshot,files=[path],data_root=tmp_path)
        assert str(exc.value)
        extra.unlink();path.unlink()
        with pytest.raises(RuntimeError,match='removed') as exc:
            verify_inputs_unchanged(snapshot,files=[path],data_root=tmp_path)
        assert str(exc.value)


def test_before_publication_input_failure_leaves_prior_stage_intact(tmp_path):
    out=tmp_path/'run';contract={'fixture':'v1'}
    publish_stage(out,'audit',{'a.json':{'x':1}},contract,{})
    before=(out/'manifest.json').read_bytes()
    def changed(): raise RuntimeError('input changed')
    with pytest.raises(RuntimeError,match='input changed') as exc:
        publish_stage(out,'encode',{'a.json':{'x':1},'b.json':{'y':2}},contract,{},before_publish=changed)
    assert str(exc.value)
    assert (out/'manifest.json').read_bytes()==before
    assert not (out/'b.json').exists()
    assert validate_run(out)['completed_stages']==['audit']


def test_concurrent_reservation_refuses_second_writer(tmp_path,monkeypatch):
    from hexis.pipeline import corpus_run
    out=tmp_path/'run';observed=[];real=corpus_run.write_artifact
    def write(path,value):
        if not observed:
            observed.append(True)
            with pytest.raises(FileExistsError):
                publish_stage(out,'audit',{'racer.json':{}},{'fixture':'v1'},{})
        return real(path,value)
    monkeypatch.setattr(corpus_run,'write_artifact',write)
    publish_stage(out,'audit',payload(),{'fixture':'v1'},{})
    assert observed==[True]
    assert not (out/'racer.json').exists()
    assert validate_run(out)['completed_stages']==['audit']


@pytest.mark.parametrize('fault',['duplicate_json_key','nonfinite_json','unknown_manifest_field'])
def test_manifest_schema_rejects_ambiguous_json(tmp_path,fault):
    out=tmp_path/'run';publish_stage(out,'audit',payload(),{'fixture':'v1'},{})
    path=out/'manifest.json';content=path.read_text()
    if fault=='duplicate_json_key':content=content.replace('"scientific_complete":false','"scientific_complete":true,"scientific_complete":false')
    if fault=='nonfinite_json':content=content.replace('"metadata":{}','"metadata":{"bad":NaN}')
    if fault=='unknown_manifest_field':content=content.replace('"metadata":{}','"metadata":{},"unknown":0')
    path.write_text(content)
    with pytest.raises(ValueError) as exc:validate_run(out)
    assert str(exc.value)


# --- input and destination cases carried over from the v2.1 audit suite ----------


def test_sha256_file_is_the_hash_of_the_bytes_on_disk(tmp_path):
    import hashlib
    path=tmp_path/'a.bin';path.write_bytes(b'hello')
    assert sha256_file(path)==hashlib.sha256(b'hello').hexdigest()


def test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root(tmp_path):
    """Both immutable roots are checked, not only the one this run was given."""
    from hexis.pipeline.corpus_run import check_destination
    raw=Path(__file__).resolve().parents[1]/'data/raw'
    for destination in (raw, raw/'UD_Ancient_Greek-Perseus'/'out'):
        with pytest.raises(ValueError,match='raw') as exc:check_destination(destination,tmp_path)
        assert str(exc.value)
