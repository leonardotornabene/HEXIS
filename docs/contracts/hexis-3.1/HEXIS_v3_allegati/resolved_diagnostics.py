"""Diagnostic definition: resolved mass by ordinary-symbol context length.
Interface adapter for ctw_reference. It does not select a single context tree.
"""
from math import fsum

def resolved(model,history):
    if model.nodes[0].n==0:
        return {'mass_by_lexical_length':{},'unseen_mass':1.,'resolved_mean':None}
    edges=list(reversed(history[-model.D:] if model.D else []))+[-1]
    idx=0;remaining=1.;lexical_length=0;mass={};unseen=0.
    for depth in range(model.D+1):
        node=model.nodes[idx];weight=remaining*node.stop
        mass[lexical_length]=mass.get(lexical_length,0.)+weight
        remaining*=1.-node.stop
        if node.terminal:break
        edge=edges[depth]
        if edge not in node.children:
            unseen=remaining;break
        idx=node.children[edge];lexical_length+=int(edge>=0)
    total=fsum(mass.values())
    if abs(total+unseen-1)>1e-12:raise ArithmeticError('diagnostic mass not normalized')
    return {'mass_by_lexical_length':mass,'unseen_mass':unseen,
            'resolved_mean':fsum(k*v for k,v in mass.items())/total if total>0 else None}
