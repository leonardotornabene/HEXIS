"""Reproducible version comparison: seven original fits and 42 sample/shuffle ledgers."""
from pathlib import Path
import argparse,hashlib,json,platform
import numpy as np
from validate_contract import parse_raw
from protocol_contract import sample,shuffle,ledger,canonical,streams
from ctw_reference import CTW
arg=argparse.ArgumentParser();arg.add_argument('--raw-dir',required=True,type=Path);arg.add_argument('--output',required=True,type=Path);args=arg.parse_args()
c=json.loads(Path(__file__).with_name('hexis_v3_design.json').read_text());b,pr,a=parse_raw(args.raw_dir,c,'ud23');h=hashlib.sha256();nh=hashlib.sha256()
for held in sorted(b):
    train=[]
    for bk,rr in sorted(b.items()):
        if bk==held:continue
        s=sample(rr,8884,0,held,bk);h.update(canonical(ledger(s)))
        sh=shuffle(s,0,held,bk,'train');h.update(canonical([r['permutation'] for r in sh]));train+=streams(s)
    model=CTW(len(a)).fit(train)
    nh.update(model.fingerprint().encode());nh.update(canonical(model.evaluate(streams(b[held]))))
r={'status':'PASS','python':platform.python_version(),'numpy':np.__version__,'folds':7,'training_contributions':42,'ledger_and_shuffle_sha256':h.hexdigest(),'model_and_scores_sha256':nh.hexdigest(),'scope':'C0 seed 0; does not certify the complete dependency stack'}
args.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
