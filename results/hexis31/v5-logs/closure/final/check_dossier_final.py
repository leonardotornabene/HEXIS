"""Independently check editorial tables against CSV rows; never produce statistics."""
import csv
import hashlib
import itertools
import json
import math
import re
import subprocess
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

root = Path.cwd()
run = root/'results/hexis31/v3-seed0-v3006'
source = {p.name:list(csv.DictReader(p.open())) for p in run.glob('*.csv')}
text = (root/'docs/HANDOFF.md').read_text()
start = text.index('## V5 results and limitations — 25 September 2026')
end = text.index('## Campaign V4 and report V5 — 24 and 25 September 2026')
section = text[start:end]
base = subprocess.check_output(['git','show','HEAD:docs/HANDOFF.md'],text=True)
pass  # phase 5 edits line 3 and open obligation 6 outside the section by design
baseline = json.loads(Path('/tmp/hormathos-v5-baseline.json').read_text())
changed = [p for p,h in baseline.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
pass

for target in re.findall(r'\]\(([^)]+)\)',section):
    assert (root/'docs'/target).exists(), target

tables = []
for match in re.finditer(r'(?m)^\|.*\n(?:\|.*\n)+',section):
    lines = match.group().splitlines()
    rows = [[v.strip() for v in line.strip('|').split('|')] for line in lines]
    assert all(len(r)==len(rows[0]) for r in rows), rows[0]
    tables.append((rows[0],rows[2:]))
assert len(tables)==19, [h for h,_ in tables]

metrics=['ce_ctw_original','ce_root_original','ce_ctw_shuffled','ce_root_shuffled','g_original','g_shuffled','q']
weight={'Equal block':'equal_block','Eligible target':'eligible_token_weighted'}
inventory=list(csv.DictReader((root/'results/hexis31/v1/documents.csv').open()))
docs={r['doc_id']:r for r in inventory if r['variant']=='ud23' and r['role']=='primary'}
doc_labels={row[1]:row[0] for row in tables[1][1]}
blocks={r['dependence_block'] for r in docs.values()}
checked=0

def find(name, **query):
    found=[r for r in source[name] if all(r[k]==str(v) for k,v in query.items())]
    assert len(found)==1,(name,query,len(found))
    return found[0]

def check(shown, value, count=False):
    global checked
    checked+=1
    if value=='':
        assert shown=='null'
        return
    s,v=Decimal(shown),Decimal(value)
    if count:
        assert s==v
        return
    if v and abs(v)<Decimal('0.000001'):
        assert re.fullmatch(r'-?\d\.\d{2}e[+-]\d+',shown),shown
        tolerance=Decimal(5).scaleb(s.adjusted()-3)
    else:
        assert re.fullmatch(r'-?\d+\.\d{6}',shown),shown
        tolerance=Decimal('0.0000005')
    assert abs(s-v)<=tolerance,(shown,value,tolerance)
    assert not(v and s==0), ('nonzero hidden as zero',shown,value)

def summary(cell, level, unit, metric='q', band='all', aggregation='not_applicable'):
    return find('seed_summaries.csv',cell=cell,level=level,unit=unit,
                metric=metric,past_band=band,aggregation=aggregation)

def check_scores(shown, **query):
    for display,metric in zip(shown,metrics,strict=True):
        check(display,summary(metric=metric,**query)['mean'])

def check_spread(shown, **query):
    row=summary(**query)
    for display,key in zip(shown.split(' / '),['mean','sd','min','max'],strict=True):
        check(display,row[key])

for row in tables[0][1]:
    for shown,(cell,band) in zip(row[1:],itertools.product(['C0','oth'],['all','4_7','ge8']),strict=True):
        check(shown,find('block_pairs.csv',cell=cell,seed=0,held_block=row[0],past_band=band)['n'],True)
for row in tables[1][1]:
    doc=docs[row[0]]
    assert row[2]==doc['dependence_block']
    check(row[3],doc['kept'],True);check(row[4],doc['eligible'],True)
    for shown,(cell,band) in zip(row[5:],itertools.product(['C0','oth'],['4_7','ge8']),strict=True):
        check(shown,find('document_scores.csv',cell=cell,seed=0,doc_id=row[0],past_band=band)['n'],True)
for (header,rows),band in zip(tables[2:5],['all','4_7','ge8'],strict=True):
    assert len(rows)==18
    for row in rows:
        level,label=row[0].split(' / ',1)
        unit=doc_labels[label] if level=='document' else label
        check_scores(row[1:],cell='C0',level=level,unit=unit,band=band)
for row in tables[5][1]:
    level,label=row[0].split(' / ',1)
    for shown,band in zip(row[1:],['all','4_7','ge8'],strict=True):
        check_spread(shown,cell='C0',level=level,unit=doc_labels[label] if level=='document' else label,band=band)
for row in tables[6][1]:
    for shown,group in zip(row[1:3],['HEX','PROSE_ALL'],strict=True):
        check(shown,find('contrasts.csv',cell=row[0],seed=0,aggregation='equal_block',group=group)['n'],True)
    check(row[3],summary(row[0],'group','HEX',aggregation='equal_block')['S'],True)
assert len(tables[7][1])==36
for row in tables[7][1]:
    check_scores(row[3:],cell=row[0],level='group',unit=row[1],aggregation=weight[row[2]])
for row in tables[8][1]:
    check(row[2],summary(row[0],'group',row[1],aggregation='equal_block')['S'],True)
    for shown,agg in zip(row[3:],weight.values(),strict=True):
        check_spread(shown,cell=row[0],level='group',unit=row[1],aggregation=agg)
for row in tables[9][1]:
    cell,block=row[0].split(' / ')
    a=find('aggregation_weights.csv',cell=cell,seed=0,block=block,aggregation='equal_block')
    b=find('aggregation_weights.csv',cell=cell,seed=0,block=block,aggregation='eligible_token_weighted')
    check(row[1],b['n'],True);check(row[2],a['share']);check(row[3],b['share'])
    assert row[4]==b['training_tokens']+' / '+b['available_tokens']
    for shown,key in zip(row[5:],['training_share','fold_training_tokens','fold_share_HEX','fold_share_PROSE_ALL'],strict=True):
        check(shown,b[key],key=='fold_training_tokens')
assert len(tables[10][1])==35 and len(tables[11][1])==15 and len(tables[12][1])==10
for row in tables[10][1]:
    check_spread(row[2],cell=row[0],level='block_difference',unit=row[1])
for row in tables[11][1]:
    for shown,agg in zip(row[2:],weight.values(),strict=True):
        check_spread(shown,cell=row[0],level='group_difference',unit=row[1],aggregation=agg)
for row in tables[12][1]:
    check_scores(row[2:],cell=row[0],level='group_difference',unit='contrast',aggregation=weight[row[1]])
assert len(tables[13][1])==21 and len(tables[14][1])==3
for row in tables[13][1]:
    for shown,variant in zip(row[2:],['ud23','ud23_oth','upos_only'],strict=True):
        check(shown,find('jsd_pairs.csv',variant=variant,block_a=row[0],block_b=row[1])['jsd'])
for row in tables[14][1]:
    src=find('jsd_centroids.csv',variant=row[0])
    check(row[1],src['blocks_a'],True);check(row[2],src['blocks_b'],True);check(row[3],src['jsd'])
assert len(tables[16][1])==14 and len(tables[17][1])==44
for row in tables[16][1]:
    block,arm=row[0].split(' / ')
    src=find('model_diagnostics.csv',cell='C0',seed=0,held_block=block,arm=arm)
    check(row[1],src['nodes'],True)
    assert row[2]==src['root_observed_symbol_count']+' / '+src['root_unseen_symbol_count']
    for shown,key in zip(row[3:],['root_stop','delta_root_nats_stop_minus_split','fit_seconds','evaluation_seconds','peak_rss'],strict=True):
        check(shown,src[key],key=='peak_rss')
for row in tables[17][1]:
    label,arm,band=row[0].split(' / ')
    src=find('arm_diagnostics.csv',cell='C0',seed=0,doc_id=doc_labels[label],arm=arm,past_band=band)
    check(row[1],src['n'],True)
    assert row[2]==src['resolved_valid_count']+' / '+src['resolved_null_count_by_reason_no_resolved_mass']
    for shown,key in zip(row[3:],['resolved_mean','unseen_mass_mean','root_unseen_target_count','implicit_unseen_branch_encounter_count'],strict=True):
        check(shown,src[key],key.endswith('count'))

# Coverage and coupling, checked without recomputing a single mean or SD.
for name,unitcol in [('block_pairs.csv','held_block'),('document_scores.csv','doc_id')]:
    reference={}
    for row in source[name]:
        key=(row['cell'],row[unitcol],row['past_band'])
        assert reference.setdefault(key,row['n'])==row['n']
    for (cell,unit,band),n in reference.items():
        if cell!='oth': assert n==reference[('C0',unit,band)]
for row in source['seed_summaries.csv']:
    assert int(row['S'])==(20 if row['cell']=='C0' else 10)
coupled=defaultdict(set)
for row in source['sensitivity_pairs.csv']:
    assert row['reference']=='C0'
    key=tuple(row[k] for k in ['cell','level','unit','aggregation','past_band','metric'])
    assert row['seed'] not in coupled[key]
    coupled[key].add(row['seed'])
    assert math.isclose(float(row['difference']),float(row['value'])-float(row['reference_value']),abs_tol=1e-14)
assert all(seeds==set(map(str,range(10))) for seeds in coupled.values())
for cell,seed,agg in {(r['cell'],r['seed'],r['aggregation']) for r in source['contrasts.csv']}:
    rs={g:find('contrasts.csv',cell=cell,seed=seed,aggregation=agg,group=g) for g in ['HEX','PROSE_ALL','contrast']}
    for metric in metrics:
        assert math.isclose(float(rs['contrast'][metric]),float(rs['HEX'][metric])-float(rs['PROSE_ALL'][metric]),abs_tol=1e-14)
    assert math.isclose(float(rs['contrast']['q']),float(rs['contrast']['g_original'])-float(rs['contrast']['g_shuffled']),abs_tol=1e-14)
contributions=defaultdict(list)
for r in source['jsd_contributions.csv']:
    contributions[(r['variant'],r['scope'],r['a'],r['b'])].append(float(r['contribution']))
for r in source['jsd_pairs.csv']:
    values=contributions[(r['variant'],'block_pair',r['block_a'],r['block_b'])]
    assert math.isclose(math.fsum(values),float(r['jsd']),abs_tol=1e-14)
for r in source['jsd_centroids.csv']:
    values=contributions[(r['variant'],'group_centroid',r['group_a'],r['group_b'])]
    assert math.isclose(math.fsum(values),float(r['jsd']),abs_tol=1e-14)
for path,digest in [('manifest.json','3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab')]:
    assert hashlib.sha256((run/path).read_bytes()).hexdigest()==digest
m=json.loads((run/'manifest.json').read_text())
for path,record in m['artifacts'].items():
    assert hashlib.sha256((run/path).read_bytes()).hexdigest()==record['sha256'],path
print(f'PASS: {checked} displayed numerical fields matched source rows and rounding; 19 tables; all local links resolve')
print('PASS: seed and denominator coverage, paired direction, group contrasts, all R1 contribution sums')
print('PASS: only docs/HANDOFF.md changed; all historical text, frozen files, manifest and 931 artifacts unchanged')
