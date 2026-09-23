"""The five §11.6 figures (T27): drawn from the verified report tables alone, deterministic SVG."""
import ast
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import PathCollection
from matplotlib.text import Text

from hormathos.contracts import load_contracts
from hormathos.model import diagnostics
from hormathos.protocols import scores
from hormathos.viz import plots
from test_v31_descriptive import campaign, cell, describe, report

pytestmark = pytest.mark.v31
ROOT = Path(__file__).resolve().parents[1]
CELLS = ('C0', 'zeta', 'tiny')  # the declared order, deliberately not the alphabetical one
GROUPS = {'ALPHA': scores.HEX, 'BETA': scores.PROSE}
SWAPPED = {'ALPHA': scores.PROSE, 'BETA': scores.HEX}
TABLES = ('block_pairs.csv', 'document_scores.csv', 'seed_summaries.csv', 'contrasts.csv',
          'sensitivity_pairs.csv', 'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv',
          'model_diagnostics.csv', 'arm_diagnostics.csv', 'aggregation_weights.csv')
LONG = {'a': ('Anonymous', 'Homeric Hymn to Demeter'),
        'b': ('Diodorus Siculus', 'Bibliotheca historica, book 11'),
        'z': ('Sophocles', 'Oedipus Tyrannus')}  # real label lengths for the toy documents


@pytest.fixture(scope='module')
def reported(tmp_path_factory):
    config, corpus, output = campaign(tmp_path_factory.mktemp('figures'),
                                      cells=[cell('C0', q=12, seeds=(0, 1)), cell('zeta', q=6, seeds=(0, 1)),
                                             cell('tiny', q=6, D=3, seeds=(0, 1))])  # two depths, as C0 and D12
    describe(config, corpus, output, '--cell', 'all')
    return corpus, output, report(config, corpus, output)


def read(output, *names):
    return [pd.read_csv(output/name) for name in names]


def labels(axis, which='x'):
    return [label.get_text() for label in (axis.get_xticklabels() if which == 'x' else axis.get_yticklabels())]


def test_report_emits_the_five_contract_figures_as_deterministic_svg(reported):
    corpus, output, manifest = reported
    assert plots.FIGURES == tuple(load_contracts()['report']['figures'])
    assert set(plots.ARTIFACTS) <= set(manifest['artifacts'])
    for name in plots.ARTIFACTS:
        text = (output/name).read_text(encoding='utf-8')
        assert ET.fromstring(text).tag.endswith('svg')
        assert manifest['run_id'] in text and '<dc:date>' not in text
    tables = {name: pd.read_csv(output/name) for name in TABLES}
    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    first = plots.render(tables, documents, contingency, manifest['run_id'], cells=CELLS)
    assert first == plots.render(tables, documents, contingency, manifest['run_id'], cells=CELLS)


def test_plotted_values_are_the_verified_table_values(reported):
    corpus, output, _ = reported
    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    blocks, docs, summaries, contrasts, pairs, centroids, contributions = read(
        output, 'block_pairs.csv', 'document_scores.csv', 'seed_summaries.csv', 'contrasts.csv',
        'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv')

    def scattered(axis):
        return sorted(float(y) for collection in axis.collections if isinstance(collection, PathCollection)
                      for _, y in collection.get_offsets())

    profile = plots.block_document_profiles(blocks, docs, summaries, documents, GROUPS, 'run')
    q = profile.axes[2]  # blocks, Q
    rows = blocks[blocks.cell.eq('C0') & blocks.past_band.eq('all')]
    assert scattered(q) == pytest.approx(sorted(rows['q']), abs=1e-12)
    means = summaries[summaries.cell.eq('C0') & summaries.level.eq('block') & summaries.past_band.eq('all')
                      & summaries.metric.eq('q')].set_index('unit').sort_index()['mean']
    diamonds = [line for line in q.lines if line.get_marker() == 'D']
    assert len(diamonds) == 1 and list(diamonds[0].get_ydata()) == pytest.approx(list(means), abs=1e-12)

    sensitivity = plots.sensitivities_two_weights(contrasts, read(output, 'sensitivity_pairs.csv')[0],
                                                  summaries, CELLS, 'run')
    assert scattered(sensitivity.axes[0]) == pytest.approx(
        sorted(contrasts[contrasts.group.eq('contrast')]['q']), abs=1e-12)

    matrix = plots.R1(pairs, centroids, contributions, 'toy', 'run').axes[0].images[0].get_array()
    names, expected = plots.jsd_matrix(pairs, 'toy')
    assert np.array_equal(np.asarray(matrix), expected) and np.allclose(expected, expected.T)
    assert sorted(expected[np.triu_indices(len(names), 1)]) == pytest.approx(sorted(pairs['jsd']), abs=0)

    corpus_figure = plots.corpus_annotation(documents, contingency, 'toy', GROUPS, 'run')
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
    for node in ast.walk(ast.parse((ROOT/'src/hormathos/viz/plots.py').read_text(encoding='utf-8'))):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.extend(f'{node.module}.{alias.name}' for alias in node.names)
    assert imported
    forbidden = ('context_tree', 'sampling', 'hormathos.pipeline', 'pyplot', 'hormathos.stats', 'candidates')
    assert not [name for name in imported if any(word in name for word in forbidden)]


def test_mixture_mass_axis_stops_at_the_reference_depth(reported):
    """§9.2: masses exist for ℓ = 0..D of C0 only; a longer cell's columns are no false zero."""
    _, output, _ = reported
    models, arms = read(output, 'model_diagnostics.csv', 'arm_diagnostics.csv')
    assert arms.filter(like=diagnostics.MASS_PREFIX).shape[1] == 4  # 'tiny' has D=3
    figure = plots.supports_mixture_masses(models, arms, 'run')
    assert len(figure.axes[1].lines) == 2
    for line in figure.axes[1].lines:
        assert list(line.get_xdata()) == [0, 1, 2]  # C0 has D=2


def test_profiles_label_documents_by_author_work_and_targets(reported):
    """§3.3: the profile shows which work dominates its block; blocks follow the report groups."""
    corpus, output, _ = reported
    blocks, docs, summaries = read(output, 'block_pairs.csv', 'document_scores.csv', 'seed_summaries.csv')
    documents = read(corpus, 'documents.csv')[0]
    figure = plots.block_document_profiles(blocks, docs, summaries, documents, SWAPPED, 'run')
    targets = docs[docs.cell.eq('C0') & docs.seed.eq(0)].groupby('doc_id')['n'].sum()
    assert labels(figure.axes[0]) == ['BETA (HEX)', 'ALPHA (PROSE_ALL)']
    assert labels(figure.axes[3]) == [f'Author {doc}, Work {doc} (n={targets[doc]:,})' for doc in ('b', 'a')]


def test_corpus_figure_orders_documents_by_group_then_block(reported):
    corpus, _, _ = reported
    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    figure = plots.corpus_annotation(documents, contingency, 'toy', SWAPPED, 'run')
    assert labels(figure.axes[0], 'y') == [
        'Author b, Work b', 'Author a, Work a', 'Author z, Work z (inventory only)']


def test_r1_tables_and_figure_name_every_symbol(reported):
    corpus, output, _ = reported
    names = json.loads((corpus/'alphabets.json').read_text())['toy']['symbols']
    for table in read(output, 'root_distributions.csv', 'jsd_contributions.csv'):
        assert table['symbol'].tolist() == [names[index] for index in table['symbol_id']]
    figure = plots.R1(*read(output, 'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv'), 'toy', 'run')
    assert labels(figure.axes[-1]) == names  # a small alphabet is named on its axis


def test_sensitivity_figure_follows_the_declared_cell_order(reported):
    _, output, _ = reported
    figure = plots.sensitivities_two_weights(
        *read(output, 'contrasts.csv', 'sensitivity_pairs.csv', 'seed_summaries.csv'), CELLS, 'run')
    assert labels(figure.axes[0]) == list(CELLS)
    assert labels(figure.axes[1]) == list(CELLS[1:])


def test_every_figure_keeps_its_text_inside_the_canvas(reported):
    """At the real label lengths (the seventeen registry documents) no title, tick label or
    legend is cut by the canvas edge."""
    corpus, output, _ = reported
    tables = {name: pd.read_csv(output/name) for name in TABLES}
    for name in ('jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv'):  # three representations, as in R1
        frame = tables[name]
        tables[name] = pd.concat([frame, frame.assign(variant='toy_oth'), frame.assign(variant='toy_upos')],
                                 ignore_index=True)
    documents, contingency = read(corpus, 'documents.csv', 'audit_contingency.csv')
    documents = documents.assign(author_label=documents['doc_id'].map(lambda doc: LONG[doc][0]),
                                 work=documents['doc_id'].map(lambda doc: LONG[doc][1]))
    registry = {}
    for row in sorted(load_contracts()['design']['registry'], key=lambda row: row['part_order']):
        registry.setdefault(row['canonical_doc_id'], row)
    real = pd.DataFrame([{'variant': 'toy', 'doc_id': doc, 'role': row['role'], 'author_label': row['author_label'],
                          'work': row['work'], 'dependence_block': row['dependence_block'], 'raw': 1000,
                          'kept': 880, 'eligible': 640, 'retention': 0.88, 'sentences': 60}
                         for doc, row in registry.items()])
    assert len(real) == 17
    documents = pd.concat([documents, real], ignore_index=True)
    contingency = pd.concat([contingency, pd.DataFrame(
        [{'level': 'document', 'unit': doc, 'upos_raw': tag, 'deprel_raw': 'advmod', 'count': count}
         for doc in real['doc_id'] for tag, count in (('PART', 90), ('ADV', 120))])], ignore_index=True)
    for name, figure in plots.build(tables, documents, contingency, 'run', cells=CELLS).items():
        FigureCanvasAgg(figure)
        figure.canvas.draw()
        renderer, box = figure.canvas.get_renderer(), figure.bbox
        # drawn extents only: matplotlib keeps undrawn out-of-range tick labels as Text objects
        drawn = [(axis.get_title(), axis.get_tightbbox(renderer)) for axis in figure.axes]
        drawn += [(text.get_text(), text.get_window_extent(renderer)) for text in figure.texts
                  if isinstance(text, Text) and text.get_visible() and text.get_text().strip()]
        for label, extent in drawn:
            assert box.x0 - 1 <= extent.x0 and extent.x1 <= box.x1 + 1, (name, label)
            assert box.y0 - 1 <= extent.y0 and extent.y1 <= box.y1 + 1, (name, label)
