"""Small reference functions for descriptive aggregation; no inference."""
import math

def jsd(p,q):
    if len(p)!=len(q) or not p:raise ValueError('incompatible probability vectors')
    if any(not math.isfinite(v) or v<0 for v in list(p)+list(q)):raise ValueError('invalid probability')
    if abs(math.fsum(p)-1)>1e-12 or abs(math.fsum(q)-1)>1e-12:raise ValueError('not normalized')
    terms=[]
    for a,b in zip(p,q):
        u=(a+b)/2
        terms.append(.5*((a*math.log2(a/u) if a else 0)+(b*math.log2(b/u) if b else 0)))
    return math.fsum(terms),terms

def pooled_gain(rows):
    n=sum(r['n'] for r in rows)
    if n<=0:raise ValueError('no targets')
    return math.fsum(r['root_sum']-r['ctw_sum'] for r in rows)/n

def contrast(blocks,hex_keys,prose_keys):
    if len(hex_keys)!=2 or len(prose_keys)!=5 or set(hex_keys)&set(prose_keys):raise ValueError('invalid block sets')
    if set(blocks)!=set(hex_keys)|set(prose_keys):raise ValueError('missing or extra block')
    return math.fsum(blocks[k] for k in hex_keys)/2-math.fsum(blocks[k] for k in prose_keys)/5

def token_weighted_contrast(blocks,eligible_counts,hex_keys,prose_keys):
    """Secondary estimand. Counts are eligible targets in the current variant."""
    contrast(blocks,hex_keys,prose_keys) # Enforce the same complete block partition.
    if set(eligible_counts)!=set(blocks):raise ValueError('incompatible counts')
    if any(type(n) is not int or n<=0 for n in eligible_counts.values()):raise ValueError('invalid eligible count')
    if any(not math.isfinite(v) for v in blocks.values()):raise ValueError('nonfinite score')
    def mean(keys):
        return math.fsum(eligible_counts[k]*blocks[k] for k in keys)/sum(eligible_counts[k] for k in keys)
    return mean(hex_keys)-mean(prose_keys)
