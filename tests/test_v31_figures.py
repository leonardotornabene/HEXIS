"""The five §11.6 figures (T27): drawn from the verified report tables alone, deterministic SVG."""
import ast
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from matplotlib.collections import PathCollection

from hexis.contracts import load_contracts
from hexis.viz import plots
from test_v31_descriptive import campaign, cell, describe, report

pytestmark = pytest.mark.v31
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def reported(tmp_path_factory):
    config, corpus, output = campaign(tmp_path_factory.mktemp('figures'),
                                      cells=[cell('C0', q=12, seeds=(0, 1)), cell('tiny', q=6, seeds=(0, 1))])
    describe(config, corpus, output, '--cell', 'all')
    return corpus, output, report(config, corpus, output)


def read(output, *names):
    return [pd.read_csv(output/name) for name in names]


def test_report_emits_the_five_contract_figures_as_deterministic_svg(reported):
    corpus, output, manifest = reported
    assert plots.FIGURES == tuple(load_contracts()['report']['figures'])
    assert set(plots.ARTIFACTS) <= set(manifest['artifacts'])
    for name in plots.ARTIFACTS:
        text = (output/name).read_text(encoding='utf-8')
        assert ET.fromstring(text).tag.endswith('svg')
        assert manifest['run_id'] in text and '<dc:date>' not in text
    tables = {name: pd.read_csv(output/name) for name in
              ('block_pairs.csv', 'document_scores.csv', 'seed_summaries.csv', 'contrasts.csv',
               'sensitivity_pairs.csv', 'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv',
               'model_diagnostics.csv', 'arm_diagnostics.csv')}
    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    first = plots.render(tables, documents, contingency, manifest['run_id'])
    assert first == plots.render(tables, documents, contingency, manifest['run_id'])


def test_plotted_values_are_the_verified_table_values(reported):
    corpus, output, _ = reported
    blocks, docs, summaries, contrasts, pairs, centroids, contributions = read(
        output, 'block_pairs.csv', 'document_scores.csv', 'seed_summaries.csv', 'contrasts.csv',
        'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv')

    def scattered(axis):
        return sorted(float(y) for collection in axis.collections if isinstance(collection, PathCollection)
                      for _, y in collection.get_offsets())

    profile = plots.block_document_profiles(blocks, docs, summaries, 'run')
    q = profile.axes[2]  # blocks, Q
    rows = blocks[blocks.cell.eq('C0') & blocks.past_band.eq('all')]
    assert scattered(q) == pytest.approx(sorted(rows['q']), abs=1e-12)
    means = summaries[summaries.cell.eq('C0') & summaries.level.eq('block') & summaries.past_band.eq('all')
                      & summaries.metric.eq('q')].set_index('unit').sort_index()['mean']
    diamonds = [line for line in q.lines if line.get_marker() == 'D']
    assert len(diamonds) == 1 and list(diamonds[0].get_ydata()) == pytest.approx(list(means), abs=1e-12)

    sensitivity = plots.sensitivities_two_weights(contrasts, read(output, 'sensitivity_pairs.csv')[0],
                                                  summaries, 'run')
    assert scattered(sensitivity.axes[0]) == pytest.approx(
        sorted(contrasts[contrasts.group.eq('contrast')]['q']), abs=1e-12)

    matrix = plots.R1(pairs, centroids, contributions, 'toy', 'run').axes[0].images[0].get_array()
    names, expected = plots.jsd_matrix(pairs, 'toy')
    assert np.array_equal(np.asarray(matrix), expected) and np.allclose(expected, expected.T)
    assert sorted(expected[np.triu_indices(len(names), 1)]) == pytest.approx(sorted(pairs['jsd']), abs=0)

    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    corpus_figure = plots.corpus_annotation(documents, contingency, 'toy', 'run')
    part = [patch.get_width() for patch in corpus_figure.axes[2].containers[0]]
    assert sorted(part) == pytest.approx(sorted(1 / documents['raw']), abs=1e-12)  # toy: one PART each


def test_structured_model_columns_are_canonical_json(reported):
    _, output, _ = reported
    table = pd.read_csv(output/'model_diagnostics.csv')
    for path in sorted(output.glob('pair__*.json')):
        record = json.loads(path.read_text())
        for arm, model in record['models'].items():
            row = table[table.cell.eq(record['cell']) & table.held_block_key.eq(record['held_block_key'])
                        & table.seed.eq(record['seed']) & table.arm.eq(arm)]
            assert len(row) == 1
            for name in ('node_count_by_structural_depth', 'support_histogram_1_2to4_5to9_10plus_by_depth'):
                assert json.loads(row[name].iloc[0]) == model[name]


def test_figures_read_tables_only():
    """No model, sample, ledger or pipeline reaches the figures; no global pyplot state."""
    imported = []
    for node in ast.walk(ast.parse((ROOT/'src/hexis/viz/plots.py').read_text(encoding='utf-8'))):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.extend(f'{node.module}.{alias.name}' for alias in node.names)
    assert imported
    forbidden = ('context_tree', 'sampling', 'hexis.pipeline', 'pyplot', 'hexis.stats', 'candidates')
    assert not [name for name in imported if any(word in name for word in forbidden)]
