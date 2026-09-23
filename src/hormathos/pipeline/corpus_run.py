"""Shared V1 audit/encode runner, deterministic identity and atomic persistence."""
import argparse
import datetime
import hashlib
import json
import io
import os
import platform
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from hormathos.config import load_v31_config
from hormathos.contracts import ROOT, BUNDLE, canonical_json, compare, digest, load_contracts
from hormathos.corpus import build_corpus, verify_corpus
from hormathos.manifest import sha256_file, _package_versions

AUDIT_FILES = {'documents.csv','alphabets.json','source_audit.json','audit_summary.csv','audit_contingency.csv','audit_A.csv','exclusions.parquet'}


# Moved from the historical audit stage (plan §13.2, "keep the working
# defences"): the immutable-raw destination check and the input staging that
# binds each digest to the bytes actually parsed. Two changes, declared in V3-002:
# the refusal message cites §11.7, and the canonical root is the repository's own,
# not one relative to the working directory.
CANONICAL_DATA_ROOT = ROOT / "data/raw"


def check_output_locations(paths, *, data_root: Path) -> None:
    """Reject every resolved destination inside either immutable raw-data root."""
    roots = (
        ("selected data root", Path(data_root).resolve()),
        ("canonical data root", Path(CANONICAL_DATA_ROOT).resolve()),
    )
    for path in map(Path, paths):
        resolved = path.resolve()
        for label, root in roots:
            if resolved == root or root in resolved.parents:
                raise ValueError(
                    f"output destination {path} resolves to {resolved}, inside the "
                    f"{label} {root}: raw data is immutable"
                )

def _conllu_paths(data_root: Path) -> list[Path]:
    return sorted(Path(data_root).rglob("*.conllu"))

@contextmanager
def staged_inputs(paths):
    """Copy each input's bytes to a private directory and hash **those** bytes.

    Yields ``(snapshot, staged)``: original path -> SHA-256, and original path ->
    the copy to read.

    Hashing a file and then reopening it to parse is not enough, however tight the
    window looks and however carefully the digest is re-checked afterwards. The
    defeating sequence is edit → parse → restore: both digests match the original
    while the parse consumed something else, and the run publishes a report of
    bytes its manifest does not describe. Comparing before and after cannot see
    this, because there is nothing left to compare.

    So the bytes are read once, the digest is taken of what was read, and the
    parse consumes a copy no one else has a path to. Digest and content then
    describe the same bytes by construction rather than by timing.
    """
    with tempfile.TemporaryDirectory(prefix="hormathos-audit-") as tmp:
        staging = Path(tmp)
        snapshot: dict[Path, str] = {}
        staged: dict[Path, Path] = {}
        for index, original in enumerate(map(Path, paths)):
            data = original.read_bytes()
            snapshot[original] = hashlib.sha256(data).hexdigest()
            # Index-prefixed so two inputs sharing a basename cannot collide.
            copy = staging / f"{index:04d}_{original.name}"
            copy.write_bytes(data)
            staged[original] = copy
        yield snapshot, staged

def verify_inputs_unchanged(
    snapshot: dict[Path, str], *, files, data_root: Path
) -> None:
    """Refuse to publish if the inputs moved under us — in any of three ways.

    This is **not** what makes digest and content agree — `staged_inputs` does
    that, by construction. What is left for this check is the operator's question:
    did the corpus move while we were auditing it? A run whose sources were
    **edited** or **removed** underneath it, or whose data root gained a **new**
    `.conllu`, describes a state that no longer exists, and publishing that
    silently would be its own kind of dishonesty.

    So the data root is re-globbed as well as re-hashed. Checked before the first
    write, so a failure publishes nothing.
    """
    problems = []
    appeared = sorted(set(_conllu_paths(data_root)) - set(files))
    if appeared:
        problems.append(f"appeared: {[str(path) for path in appeared]}")
    for path, digest in sorted(snapshot.items()):
        if not path.exists():
            problems.append(f"removed: {path}")
        elif sha256_file(path) != digest:
            problems.append(f"edited: {path}")
    if problems:
        raise RuntimeError(
            "inputs changed while the audit was running — "
            + "; ".join(problems)
            + ". Nothing was written; rerun against a stable data root (§11.7)."
        )


def discover_inputs(data_root, design):
    data_root=Path(data_root)
    files=_conllu_paths(data_root)
    expected={row['file']:row['sha256'] for row in design['source_hashes']}
    names={path.name for path in files}
    if names!=set(expected) or len(files)!=len(expected) or any(p.parent!=data_root for p in files):
        raise ValueError(f'{data_root}: missing {sorted(set(expected)-names)}, extra/nested {sorted(names-set(expected))}; require exact three Greek CoNLL-U files')
    for path in files:
        if sha256_file(path)!=expected[path.name]:
            raise ValueError(f'{path}: hash mismatch')
    return files


def check_destination(output, data_root):
    check_output_locations([output],data_root=Path(data_root))


def run_identity(contract):
    return digest(contract)


def write_artifact(path, value):
    if path.suffix=='.parquet':
        table=pa.Table.from_pandas(value,preserve_index=False)
        for index, field in enumerate(table.schema):
            if pa.types.is_string(field.type) or pa.types.is_large_string(field.type):
                table=table.set_column(index, field.name, table.column(index).dictionary_encode())
        pq.write_table(table,path,compression='zstd',use_dictionary=True)
    elif path.suffix=='.csv':
        value.to_csv(path,index=False,lineterminator='\n')
    elif path.suffix=='.json':
        path.write_bytes(canonical_json(value)+b'\n')
    else:
        raise ValueError(f'{path}: unsupported artifact format')
    with path.open('rb') as handle:
        os.fsync(handle.fileno())


def artifact_record(path):
    """Read every persisted artifact back; record actual schema and cardinality."""
    result={'sha256':sha256_file(path),'bytes':path.stat().st_size,'format':path.suffix[1:]}
    if path.suffix=='.parquet':
        table=pq.read_table(path)
        result.update(rows=table.num_rows,schema=[{'name':f.name,'type':str(f.type),'nullable':f.nullable} for f in table.schema])
    elif path.suffix=='.csv':
        frame=pd.read_csv(path)
        result.update(rows=len(frame),schema=[{'name':name,'type':str(dtype)} for name,dtype in frame.dtypes.items()])
    elif path.suffix=='.json':
        value=json.loads(path.read_bytes())
        result.update(rows=len(value) if isinstance(value,(dict,list)) else 1,
                      schema={'type':type(value).__name__,'keys':sorted(value) if isinstance(value,dict) else None})
    return result


def _read_json(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:
                raise ValueError(f'{path}: duplicate JSON key {key!r}')
            result[key]=value
        return result
    def nonfinite(value):
        raise ValueError(f'{path}: non-finite JSON value {value}')
    return json.loads(path.read_bytes(),object_pairs_hook=unique,parse_constant=nonfinite)


def validate_run(output, *, locked=False):
    output=Path(output)
    try:
        m=_read_json(output/'manifest.json')
        if set(m)!={'schema_version','run_id','run_contract','completed_stages','corpus_complete','scientific_complete','artifacts','metadata','checks'}:
            raise ValueError('manifest: missing/unknown schema fields')
        types={'schema_version':str,'run_id':str,'run_contract':dict,'completed_stages':list,
               'corpus_complete':bool,'scientific_complete':bool,'artifacts':dict,'metadata':dict,'checks':dict}
        if any(type(m[key]) is not kind for key,kind in types.items()):
            raise ValueError('manifest: incorrect field types')
        if m['run_id']!=run_identity(m['run_contract']):
            raise ValueError('manifest: run identity mismatch')
        names=set(m['artifacts'])|{'manifest.json'}|({'.lock'} if locked else set())
        if {p.name for p in output.iterdir()}!=names:
            raise ValueError('run: missing/extra artifacts or interrupted temporary stage')
        if m['schema_version']!='hexis-corpus-manifest-1' or m['scientific_complete'] is not False:
            raise ValueError('manifest: unsupported schema/scientific status')
        stages=m['completed_stages']
        if stages not in (['audit'],['audit','encode']) or m['corpus_complete']!=('encode' in stages):
            raise ValueError('manifest: invalid corpus stage state')
        if m['run_contract'].get('spec_version')=='HEXIS-3.1':
            expected_files=AUDIT_FILES | ({'coordinates.parquet','sequences.parquet'} if m['corpus_complete'] else set())
            if set(m['artifacts'])!=expected_files:
                raise ValueError('manifest: missing/extra corpus artifact keys')
        for name,record in m['artifacts'].items():
            if Path(name).name!=name or (output/name).is_symlink():
                raise ValueError(f'{name}: unsafe artifact name/symlink')
            compare(artifact_record(output/name),record,f'artifact/{name}')
        if m['run_contract'].get('spec_version')=='HEXIS-3.1' and m['corpus_complete']:
            artifacts={name:(pd.read_parquet(output/name) if name.endswith('.parquet') else pd.read_csv(output/name) if name.endswith('.csv') else json.loads((output/name).read_bytes())) for name in m['artifacts']}
            verify_corpus(artifacts,load_contracts())
        return m
    except (OSError,KeyError,json.JSONDecodeError,pd.errors.ParserError,pa.ArrowException) as exc:
        raise ValueError(f'{output}: unreadable/corrupt run: {exc}') from exc


def publish_stage(output, stage, artifacts, contract, metadata, *, before_publish=None, data_root=None):
    """Exclusive stage reservation; verify temporaries, publish manifest last.

    Atomic hard-link publication refuses destination collisions even between a
    preflight and publication. Only the existing manifest is atomically replaced.
    A killed process leaves an invalid/incomplete run, never a completed stage.
    """
    output=Path(output)
    check_destination(output,data_root if data_root is not None else ROOT/'data/raw')
    if stage not in ('audit','encode'):
        raise ValueError(f'unknown stage {stage}')
    if any(Path(name).name!=name or name in ('manifest.json','.lock') for name in artifacts):
        raise ValueError('unsafe/reserved artifact name')
    output.parent.mkdir(parents=True,exist_ok=True)
    created=False
    try:
        output.mkdir(); created=True
    except FileExistsError:
        pass
    lock=output/'.lock'
    with lock.open('x'):
        pass
    published=[]
    try:
        prior=validate_run(output,locked=True) if not created else None
        if prior:
            compare(contract,prior['run_contract'],'run_contract')
            if stage in prior['completed_stages']:
                raise FileExistsError(f'{output}: {stage} already complete; outputs immutable')
        old_records=dict(prior['artifacts']) if prior else {}
        records=dict(old_records)
        with tempfile.TemporaryDirectory(prefix='.stage-',dir=output) as tmp:
            tmp=Path(tmp)
            for name,value in artifacts.items():
                path=tmp/name
                write_artifact(path,value)
                records[name]=artifact_record(path)
                if name in old_records:
                    compare(records[name],old_records[name],f'existing/{name}')
                # Validate round-trip content, independently of its recorded hash.
                if path.suffix=='.parquet':
                    restored=pd.read_parquet(path)
                    pd.testing.assert_frame_equal(restored,value,check_dtype=False,check_categorical=False)
                elif path.suffix=='.json':
                    compare(json.loads(path.read_bytes()),value,f'roundtrip/{name}')
                elif path.suffix=='.csv':
                    if pd.read_csv(path).to_csv(index=False)!=pd.read_csv(io.StringIO(value.to_csv(index=False))).to_csv(index=False):
                        raise ValueError(f'{name}: CSV round-trip mismatch')
            if before_publish is not None:
                before_publish()
            completed=['audit','encode'] if stage=='encode' else ['audit']
            manifest={'schema_version':'hexis-corpus-manifest-1','run_id':run_identity(contract),
                      'run_contract':contract,'completed_stages':completed,
                      'corpus_complete':stage=='encode','scientific_complete':False,
                      'artifacts':records,'metadata':metadata,
                      'checks':{'stage_artifacts_roundtrip':'passed', 'stage':stage,
                                'contract_and_input_checks':metadata.get('checks',{})}}
            write_artifact(tmp/'manifest.json',manifest)
            for name in artifacts:
                if name not in old_records:
                    os.link(tmp/name,output/name)
                    published.append(output/name)
            os.replace(tmp/'manifest.json',output/'manifest.json')
        return manifest
    except BaseException:
        for path in published:
            path.unlink(missing_ok=True)
        raise
    finally:
        lock.unlink(missing_ok=True)
        if created and not any(output.iterdir()):
            output.rmdir()


def _code_identity():
    # All package sources are identified; local acquisition scripts are not producers.
    files=sorted((ROOT/'src/hormathos').rglob('*.py'))
    return {str(p.relative_to(ROOT)):sha256_file(p) for p in files}


def main(stage, argv=None):
    parser=argparse.ArgumentParser(description=f'HORMATHOS {stage}: corpus only, no model fits')
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--data-root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args(argv)
    check_destination(args.output_dir,args.data_root)
    contracts=load_contracts(); cfg=load_v31_config(args.config)
    files=discover_inputs(args.data_root,contracts['design'])
    registry=ROOT/'config/registry_overrides.yaml'
    provenance_path=ROOT/'data/provenance_v31.json'
    provenance=json.loads(provenance_path.read_bytes())
    compare(provenance['commit'],contracts['design']['source_commit'],'source provenance commit')
    compare(provenance['files'],contracts['design']['source_hashes'],'source provenance files')
    contract_files=[p for p in BUNDLE.iterdir() if p.is_file()]+[BUNDLE.parent/'HEXIS_piano_definitivo_v3.1_2026-09-15.md']
    inputs=list(dict.fromkeys([*files,args.config,registry,provenance_path,ROOT/'uv.lock',*contract_files]))
    source_hashes={r['file']:r['sha256'] for r in contracts['design']['source_hashes']}
    code=_code_identity()
    with staged_inputs(inputs) as (snapshot, staged):
        for path in files:
            compare(snapshot[path],source_hashes[path.name],f'input hash/{path.name}')
        compare(snapshot[ROOT/'uv.lock'],cfg['runtime']['lock_sha256'],'uv.lock')
        compare(json.loads(staged[provenance_path].read_bytes()),provenance,'snapshot.provenance')
        # Re-read configuration from the same staged bytes named by the identity.
        from hormathos.config import load_yaml
        compare(load_yaml(args.config,source=staged[args.config]),cfg,'snapshot.config')
        compare(load_yaml(registry,source=staged[registry]),{'spec_version':'HEXIS-3.1','registry':cfg['registry']},'snapshot.registry')
        for path in contract_files:
            compare(snapshot[path],sha256_file(path),f'snapshot/{path.name}')
        result=build_corpus(files,cfg,contracts,staged=staged)
        run_contract={'spec_version':cfg['spec_version'],'representation_version':cfg['representation']['version'],
                      'analytical_contracts':contracts['lock']['contracts'],'source_commit':contracts['design']['source_commit'],'plan':contracts['lock']['plan']['sha256'],
                      'code':code,'data':source_hashes,'registry':digest(cfg['registry']),
                      'alphabets':digest(result['alphabets.json']),'configuration':digest(cfg),
                      'lock':snapshot[ROOT/'uv.lock'],'rng_version':cfg['rng']['version']}
        def unchanged():
            verify_inputs_unchanged(snapshot,files=files,data_root=args.data_root)
            compare(_code_identity(),code,'code changed during run')
            load_contracts()
        unchanged()
        commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
        metadata={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'machine':platform.platform(),'python':platform.python_version(),'package_versions':_package_versions(),
                  'input_dir':str(args.data_root.resolve()),'output_dir':str(args.output_dir.resolve()),
                  'implementation_commit':commit,
                  'deposit_commit':subprocess.run(['git','log','--diff-filter=A','-1','--format=%H','--','docs/V3-001-deposit.json'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip(),
                  'input_snapshots':{str(p):sha for p,sha in snapshot.items()},
                  'tracked_dirty':bool(subprocess.run(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()),
                  'checks':{'exact_source_hashes':True,'exact_corpus_and_alphabets':True,
                            'coordinate_sequence_content_equality':True,'new_model_fits':0}}
        if stage=='audit':
            result={name:value for name,value in result.items() if name in AUDIT_FILES}
        manifest=publish_stage(args.output_dir,stage,result,run_contract,metadata,before_publish=unchanged,data_root=args.data_root)
    validate_run(args.output_dir)
    return manifest
