"""Reader-facing panels of the five §11.6 figures, one SVG per panel (V3-009).

Presentation only. The script reads the published tables of the final campaign — never a
model, a ledger or a sample — and draws what the frozen figures draw, one panel per file,
full width. The canonical figures stay the five frozen SVGs in
`results/hexis31/v3-seed0-v3006/`: before drawing, the script renders them again from the
same tables with the frozen `hormathos.viz.plots` and stops unless every byte matches. The
seed bars are the computational min–max across seeds, never an inferential interval.

Run from the repository root:  uv run python results/figures/make_figures.py
"""

import io
import json
import os
import textwrap
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MaxNLocator, PercentFormatter

from hormathos.config import load_v31_config
from hormathos.model import diagnostics
from hormathos.protocols import scores
from hormathos.viz import plots

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'results/hexis31/v3-seed0-v3006'
CORPUS = ROOT / 'results/hexis31/v1'
OUT = Path(__file__).resolve().parent
RUN_ID = json.loads((RUN / 'manifest.json').read_text())['run_id']
REF = plots.REFERENCE_CELL

# Colours validated with the dataviz palette checker: categorical slots 1–3 all-pairs,
# an ordinal blue ramp for ordered classes. Text never takes a series colour.
INK, INK2, MUTED, GRID, SURFACE = '#0b0b0b', '#52514e', '#8a8984', '#e6e5e0', '#ffffff'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
RAMP = ('#86b6ef', '#3987e5', '#1c5cab', '#0d366b')
HEAT = LinearSegmentedColormap.from_list('blue', ('#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b'))
GROUP = {scores.HEX: ('Hexameter', BLUE), scores.PROSE: ('Prose', ORANGE)}
WEIGHTING = {'equal_block': ('every block weighs the same', BLUE),
             'eligible_token_weighted': ('every target weighs the same', ORANGE)}
ARM = {'original': ('original order', BLUE), 'shuffled': ('shuffled within each sentence', ORANGE)}
# The six settings and three annotation schemes by what they change, never by their table codes.
CELL = {'C0': 'main setting', 'a_total1': 'weaker prior (0.01 per symbol)',
        'q_half': 'half the training data', 'D12': 'context depth 12 instead of 8',
        'oth': 'other relations kept as one label', 'upos': 'part of speech only'}
VARIANT = {'ud23': 'part of speech + relation', 'ud23_oth': 'part of speech + relation, other relations kept',
           'upos_only': 'part of speech only'}
BITS = 'bits per target'
README_Q = {'HOMERIC_TRADITION': 0.262, 'HESIODIC_TRADITION': 0.253, 'HERODOTUS': 0.393,
            'THUCYDIDES': 0.430, 'ATHENAEUS': 0.452, 'DIODORUS': 0.526, 'PLUTARCH': 0.543}
MARKS = ('Large dot: mean over the seeds (runs repeated with different random samples) · small dots: single seeds '
         '· line: lowest to highest seed.')
SHOWN_SYMBOLS = 15  # larger alphabets: the leading symbols, the rest summed in one bar

WIDTH, WRAP = 10.0, 126  # inches, characters: each panel spans the full reading width
STYLE = {'svg.hashsalt': 'hormathos', 'svg.fonttype': 'path', 'font.family': 'DejaVu Sans',
         'font.size': 10.5, 'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE,
         'axes.edgecolor': MUTED, 'axes.labelcolor': INK2, 'axes.labelsize': 10.5,
         'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
         'axes.axisbelow': True, 'grid.color': GRID, 'grid.linewidth': 0.8,
         'xtick.color': INK2, 'ytick.color': INK, 'xtick.labelsize': 10, 'ytick.labelsize': 10.5,
         'legend.frameon': False, 'legend.fontsize': 10, 'text.color': INK}


def read(path):
    return pd.read_csv(path, float_precision='round_trip')  # the published floats, bit for bit


def block_name(block):
    return block.replace('_', ' ').capitalize()


def canvas(title, subtitle, source, body):
    """A full-width panel: title and subtitle on top, the source table at the foot."""
    subtitle = '\n'.join(textwrap.fill(line, WRAP) for line in subtitle.split('\n'))
    header = 0.62 + 0.2 * (subtitle.count('\n') + 1)
    figure = Figure(figsize=(WIDTH, header + body), layout='constrained')
    head, main = figure.subfigures(2, 1, height_ratios=(header, body), hspace=0)
    head.text(0.015, 1 - 0.36 / header, title, fontsize=15, fontweight='bold', va='baseline')
    head.text(0.015, 1 - 0.52 / header, subtitle, fontsize=10.5, color=INK2, va='top', linespacing=1.45)
    main.supxlabel(f'Source: {source}', x=0.985, ha='right',
                   fontsize=8.5, color=MUTED)
    return figure, main.subplots()


def legend(axis, handles, columns=None):
    handles = handles or axis.get_legend_handles_labels()[0]
    axis.legend(handles=handles, loc='lower left', bbox_to_anchor=(0, 1.01), borderaxespad=0,
                ncols=columns or len(handles), handletextpad=0.5, columnspacing=1.6)


def dot(color, name):
    return Line2D([], [], marker='o', linestyle='', markersize=8, color=color,
                  markeredgecolor=SURFACE, label=name)


def rows_axis(axis, labels):
    """Units down the y axis, first on top; values read along x."""
    axis.set_yticks(np.arange(len(labels)), labels)
    axis.set_ylim(len(labels) - 0.5, -0.5)
    axis.grid(axis='y', visible=False)
    axis.tick_params(axis='y', length=0)
    axis.spines['left'].set_visible(False)


def dots(axis, y, seeds, summary, color, *, scale=1.0, fmt='{:.3f}'):
    """Seeds, their mean and the computational min–max, as published in seed_summaries."""
    seeds = np.asarray(seeds, dtype=float) * scale
    mean, low, high = (float(summary[key]) * scale for key in ('mean', 'min', 'max'))
    assert int(summary['S']) == len(seeds), 'every seed of the summary is drawn'
    axis.hlines(y, low, high, color=color, linewidth=1.8, zorder=2)
    axis.scatter(seeds, np.full(len(seeds), y), s=16, color=color, alpha=0.35, linewidths=0, zorder=2)
    axis.scatter([mean], [y], s=72, color=color, edgecolors=SURFACE, linewidths=1.5, zorder=3)
    text = fmt.format(mean)
    if mean != 0 and float(text) == 0:
        text = f'{mean:.1e}'  # nonzero below the displayed precision: its magnitude, not a rounded zero
    axis.annotate(text, (max(high, seeds.max()), y), xytext=(9, 0), textcoords='offset points',
                  va='center', fontsize=10, color=INK2)


def zero_line(axis, vertical=True):
    (axis.axvline if vertical else axis.axhline)(0, color=MUTED, linewidth=0.9, zorder=1)


def separate(axis, after, horizontal=True):
    if 0 < after:
        (axis.axhline if horizontal else axis.axvline)(after - 0.5, color=MUTED, linewidth=0.8,
                                                       linestyle=(0, (3, 3)))


def spread(values, gap):
    """Label positions at least `gap` apart, each as close to its value as the others allow."""
    order = np.argsort(values)
    placed = np.array(values, dtype=float)
    for previous, current in zip(order, order[1:]):
        placed[current] = max(placed[current], placed[previous] + gap)
    return placed


# 1 · corpus and annotation --------------------------------------------------------------

def corpus(documents, contingency, variant, groups):
    """The rows of plots.corpus_annotation: primary documents by group and block, then inventory_only."""
    frame = documents[documents['variant'].eq(variant)].copy()
    frame['primary'] = frame['role'].eq('primary')
    order = plots._block_order(set(frame['dependence_block'].dropna()), groups)
    frame['rank'] = frame['dependence_block'].map({b: i for i, b in enumerate(order)}).fillna(len(order))
    frame = frame.sort_values(['primary', 'rank', 'doc_id'], ascending=[False, True, True])
    labels = [f'{row.author_label}, {row.work}' for row in frame.itertuples()]
    primary = int(frame['primary'].sum())
    body = 1.2 + 0.36 * len(frame)
    source = contingency[contingency['level'].eq('document')]
    counts = source.pivot_table(index='unit', columns='upos_raw', values='count', aggfunc='sum', fill_value=0)
    note = ('Below the dashed line: census-only documents, counted when the symbol inventory is built but never '
            'used for training or scoring.')

    def finish(axis):
        rows_axis(axis, labels)
        separate(axis, primary)
        for tick in axis.get_yticklabels()[primary:]:
            tick.set_color(MUTED)

    panels = {}
    figure, axis = canvas('Corpus size per document',
                          'Tokens (words and punctuation) in the source, tokens kept by the encoding, and targets: '
                          'the kept tokens, from the fifth of each sentence on, that the models predict.\n' + note,
                          'results/hexis31/v1/documents.csv', body + 0.6)
    y = np.arange(len(frame))
    for offset, (column, name, color) in enumerate((('raw', 'source tokens', RAMP[0]),
                                                    ('kept', 'kept tokens', RAMP[1]),
                                                    ('eligible', 'targets', RAMP[3]))):
        axis.barh(y + (offset - 1) * 0.26, frame[column], height=0.24, color=color, label=name)
    axis.set(xscale='log', xlabel='count (log scale)')
    axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:,.0f}'))
    finish(axis)
    legend(axis, None)
    panels['corpus__quantities'] = figure

    figure, axis = canvas('Share of tokens kept per document',
                          'Tokens kept by the encoding as a share of the tokens in the source.\n' + note,
                          'results/hexis31/v1/documents.csv', body)
    colors = [BLUE if primary_row else MUTED for primary_row in frame['primary']]
    axis.barh(y, frame['retention'], height=0.62, color=colors)
    for index, value in enumerate(frame['retention']):
        axis.annotate(f'{value:.1%}', (value, index), xytext=(6, 0), textcoords='offset points',
                      va='center', fontsize=9.5, color=INK2)
    axis.set(xlim=(0, 1.08), xlabel='kept tokens / source tokens')
    axis.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    finish(axis)
    legend(axis, [Patch(color=BLUE, label='scored documents'), Patch(color=MUTED, label='census only')])
    panels['corpus__retention'] = figure

    figure, axis = canvas('Particles and adverbs in the source annotation',
                          'Share of source tokens tagged particle (PART) or adverb (ADV). The documents use the two '
                          'tags differently, so the encoding merges them into one class.\n' + note,
                          'results/hexis31/v1/audit_contingency.csv', body + 0.3)
    for offset, (tag, name, color) in enumerate((('PART', 'particle (PART)', BLUE), ('ADV', 'adverb (ADV)', ORANGE))):
        shares = [counts.at[doc, tag] / raw if doc in counts.index and tag in counts.columns else 0.0
                  for doc, raw in zip(frame['doc_id'], frame['raw'])]
        axis.barh(y + (offset - 0.5) * 0.36, shares, height=0.34, color=color, label=name)
    axis.set(xlabel='share of source tokens')
    axis.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    finish(axis)
    legend(axis, None)
    panels['corpus__part_adv'] = figure
    return panels


# 2 · block and document profiles ---------------------------------------------------------

def profiles(tables, documents, groups):
    """The data of plots.block_document_profiles, one metric and one level per panel."""
    blocks = tables['block_pairs.csv']
    blocks = blocks[blocks['cell'].eq(REF) & blocks['past_band'].eq('all')].rename(columns={'held_block': 'unit'})
    variant = str(blocks['variant'].iloc[0])
    sums = tables['document_scores.csv']
    sums = sums[sums['cell'].eq(REF)]
    scored = scores.ce_gain_q(scores.roll_up(
        sums, keys=['cell', 'variant', 'held_block', 'held_block_key', 'seed', 'doc_id'])).rename(
        columns={'doc_id': 'unit'})
    block_units = plots._block_order(blocks['unit'].unique(), groups)
    block_of = sums.drop_duplicates('doc_id').set_index('doc_id')['held_block']
    targets = sums[sums['seed'].eq(sums['seed'].min())].groupby('doc_id')['n'].sum()  # fixed across seeds
    names = documents[documents['variant'].eq(variant)].set_index('doc_id')
    label = {doc: f"{names.at[doc, 'author_label']}, {names.at[doc, 'work']} (n={int(targets[doc]):,})"
             for doc in targets.index}
    document_units = sorted(targets.index, key=lambda doc: (block_units.index(block_of[doc]), label[doc]))
    summary = tables['seed_summaries.csv']
    summary = summary[summary['cell'].eq(REF) & summary['past_band'].eq('all')]

    q = summary[summary['level'].eq('block') & summary['metric'].eq('q')].set_index('unit')['mean']
    assert {unit: round(q[unit], 3) for unit in README_Q} == README_Q, 'README table matches seed_summaries'

    metrics = {'q': ('Order advantage Q', 'Q = gain in the original order − gain after shuffling the tokens within '
                     'each sentence. The gain is how much better the trained model predicts each annotation than '
                     'the symbol frequencies alone.', 1.0, '{:.3f}', BITS),
               'g_original': ('Gain in the original order', 'How much better the trained model predicts each '
                              'annotation than the symbol frequencies alone, with the tokens in their original '
                              'order.', 1.0, '{:.3f}', BITS),
               'g_shuffled': ('Gain after shuffling', 'The same gain after shuffling the tokens within each '
                              'sentence: practically zero, so the axis is in units of 10⁻¹⁶ bits.', 1e16,
                              '{:.2f}', f'{BITS} (× 10⁻¹⁶)')}
    levels = {'block': (blocks, block_units, [block_name(u) for u in block_units],
                        [groups[u] for u in block_units],
                        'Each block is scored by a model trained on the other six blocks.'),
              'document': (scored, document_units, [label[u] for u in document_units],
                           [groups[block_of[u]] for u in document_units],
                           'Each document is scored by the model of its block; n = targets scored per seed.')}
    panels = {}
    for metric, (title, meaning, scale, fmt, unit_label) in metrics.items():
        for level, (frame, units, labels, unit_groups, context) in levels.items():
            figure, axis = canvas(f'{title} per {level}, main setting', f'{meaning} {context}\n{MARKS}',
                                  'results/hexis31/v3-seed0-v3006/seed_summaries.csv',
                                  1.3 + (0.42 if level == 'block' else 0.36) * len(units))
            rows = summary[summary['level'].eq(level) & summary['metric'].eq(metric)].set_index('unit')
            for y, (unit, group) in enumerate(zip(units, unit_groups)):
                dots(axis, y, frame.loc[frame['unit'].eq(unit), metric], rows.loc[unit], GROUP[group][1],
                     scale=scale, fmt=fmt)
            rows_axis(axis, labels)
            separate(axis, unit_groups.count(scores.HEX))
            zero_line(axis)
            axis.set_xlim(left=min(axis.get_xlim()[0], 0))
            axis.margins(x=0.06)
            axis.set_xlabel(unit_label)
            legend(axis, [dot(color, name) for name, color in GROUP.values()])
            panels[f'profiles__{metric}_{level}'] = figure
    return panels


# 3 · sensitivities and the two weightings -----------------------------------------------

def sensitivities(tables, cells, groups):
    """The data of plots.sensitivities_two_weights; the band panel becomes one panel per band."""
    cells = [REF, *[cell for cell in cells if cell != REF]]
    contrasts, pairs, summary = (tables[name] for name in ('contrasts.csv', 'sensitivity_pairs.csv',
                                                          'seed_summaries.csv'))
    q_of = summary[summary['unit'].eq('contrast') & summary['metric'].eq('q') & summary['past_band'].eq('all')]
    panels = {}
    for name, title, subtitle, shown, level in (
            ('contrast', 'Hexameter minus prose in every setting',
             'Mean Q of the two hexameter blocks minus mean Q of the five prose blocks, averaged so that every '
             'block weighs the same, or so that every target does.',
             cells, 'group'),
            ('paired_difference', 'Change from the main setting',
             'The hexameter-minus-prose difference in each setting minus the same difference in the main '
             'setting, seed by seed on the seeds 0–9 that both share.',
             cells[1:], 'group_difference')):
        figure, axis = canvas(title, f'{subtitle}\n{MARKS}', 'results/hexis31/v3-seed0-v3006/'
                              + ('contrasts.csv' if level == 'group' else 'sensitivity_pairs.csv'),
                              1.4 + 0.62 * len(shown))
        for aggregation, (label, color) in WEIGHTING.items():
            offset = -0.17 if aggregation == 'equal_block' else 0.17
            rows = q_of[q_of['level'].eq(level) & q_of['aggregation'].eq(aggregation)].set_index('cell')
            for y, cell in enumerate(shown):
                if level == 'group':
                    seeds = contrasts.loc[contrasts['group'].eq('contrast') & contrasts['aggregation'].eq(
                        aggregation) & contrasts['cell'].eq(cell), 'q']
                else:
                    seeds = pairs.loc[pairs['level'].eq('group') & pairs['unit'].eq('contrast')
                                      & pairs['aggregation'].eq(aggregation) & pairs['metric'].eq('q')
                                      & pairs['cell'].eq(cell), 'difference']
                dots(axis, y + offset, seeds, rows.loc[cell], color,
                     fmt='{:+.3f}' if level == 'group_difference' else '{:.3f}')
        rows_axis(axis, [CELL[cell] for cell in shown])
        zero_line(axis)
        axis.margins(x=0.08)
        axis.set_xlabel(BITS)
        legend(axis, [dot(color, label) for label, color in WEIGHTING.values()])
        panels[f'sensitivities__{name}'] = figure

    blocks = summary[summary['level'].eq('block') & summary['metric'].eq('q')]
    units = plots._block_order(blocks['unit'].unique(), groups)
    for band, words in (('4_7', '4–7'), ('ge8', '8 or more')):
        figure, axis = canvas(f'Q of each block by setting, targets after {words} tokens',
                              f'Mean Q of each block across its seeds (20 in the main setting, 10 in the others), on '
                              f'targets preceded by {words} kept tokens of the same sentence.\nLines only join the '
                              f'settings of one block; the settings have no order.',
                              'results/hexis31/v3-seed0-v3006/seed_summaries.csv', 5.6)
        rows = blocks[blocks['past_band'].eq(band)].set_index(['unit', 'cell'])['mean']
        starts = []
        for unit in units:
            values = [rows[unit, cell] for cell in cells]
            color = GROUP[groups[unit]][1]
            axis.plot(np.arange(len(cells)), values, color=color, linewidth=1.8, marker='o', markersize=6,
                      markeredgecolor=SURFACE)
            starts.append(values[0])
        low, high = min(rows), max(rows)
        axis.set_ylim(min(0, low), high + 0.06 * (high - min(0, low)))
        placed = spread(starts, 0.05 * np.diff(axis.get_ylim())[0])  # labelled at the main setting
        for unit, value, position in zip(units, starts, placed):
            axis.annotate(block_name(unit), (0, value), xytext=(-0.14, position), textcoords='data',
                          ha='right', va='center', fontsize=10, color=INK,
                          arrowprops={'arrowstyle': '-', 'color': MUTED, 'linewidth': 0.6,
                                      'shrinkA': 0, 'shrinkB': 3})
        axis.set_xlim(-1.35, len(cells) - 1 + 0.25)
        axis.set_xticks(np.arange(len(cells)), [textwrap.fill(CELL[cell], 18) for cell in cells])
        axis.grid(axis='x', visible=False)
        zero_line(axis, vertical=False)
        axis.set_ylabel(BITS)
        legend(axis, [dot(color, name) for name, color in GROUP.values()])
        panels[f'sensitivities__past_band_{band}'] = figure
    return panels


# 4 · R1, descriptive divergences ---------------------------------------------------------

def r1(tables, variant, groups):
    """The data of plots.R1: block matrix, group centroids, per-symbol contributions."""
    pairs, centroids, contributions = (tables[name] for name in ('jsd_pairs.csv', 'jsd_centroids.csv',
                                                                 'jsd_contributions.csv'))
    panels = {}
    names, matrix = plots.jsd_matrix(pairs, variant)
    order = [names.index(block) for block in plots._block_order(names, groups)]
    matrix, names = matrix[np.ix_(order, order)], [names[i] for i in order]
    lower = matrix[1:, :-1]
    shown = np.ma.masked_where(np.triu(np.ones_like(lower, dtype=bool), k=1), lower)
    figure, axis = canvas('How different the annotation frequencies of two blocks are',
                          'Jensen–Shannon divergence in bits between the symbol frequencies of two blocks: 0 if '
                          f'identical, at most 1. Symbols: {VARIANT[variant]}.\nComputed from the annotations of '
                          'the texts, not from the models.',
                          'results/hexis31/v3-seed0-v3006/jsd_pairs.csv', 6.2)
    image = axis.imshow(shown, cmap=HEAT, vmin=0.0, vmax=lower.max())
    for (row, column), value in np.ndenumerate(lower):
        if column <= row:
            axis.text(column, row, f'{value:.3f}', ha='center', va='center', fontsize=10.5,
                      color=SURFACE if value > 0.55 * lower.max() else INK)
    wrap = lambda block: block_name(block).replace(' ', '\n')
    axis.set_xticks(np.arange(len(names) - 1), [wrap(b) for b in names[:-1]])
    axis.set_yticks(np.arange(len(names) - 1), [block_name(b) for b in names[1:]])
    axis.tick_params(length=0)
    axis.grid(visible=False)
    for side in axis.spines.values():
        side.set_visible(False)
    figure.colorbar(image, ax=axis, label='Jensen–Shannon divergence (bits)', shrink=0.8).outline.set_visible(False)
    panels[f'r1__matrix_{variant}'] = figure

    variants = sorted(centroids['variant'])
    alphabet = contributions.groupby('variant')['symbol_id'].nunique()
    figure, axis = canvas('Hexameter against prose, by annotation scheme',
                          'Jensen–Shannon divergence in bits between the average symbol frequencies of the hexameter '
                          'blocks and of the prose blocks, every block weighing the same, in each of the three '
                          'annotation schemes.',
                          'results/hexis31/v3-seed0-v3006/jsd_centroids.csv', 2.4)
    values = centroids.set_index('variant').loc[variants, 'jsd']
    axis.barh(np.arange(len(variants)), values, height=0.55, color=BLUE)
    for y, value in enumerate(values):
        axis.annotate(f'{value:.4f}', (value, y), xytext=(6, 0), textcoords='offset points', va='center',
                      fontsize=10, color=INK2)
    rows_axis(axis, [f'{VARIANT[v]} ({alphabet[v]} symbols)' for v in variants])
    axis.set_xlabel('Jensen–Shannon divergence (bits)')
    axis.margins(x=0.1)
    panels['r1__centroids'] = figure

    for variant_name in variants:
        rows = contributions[contributions['variant'].eq(variant_name)
                             & contributions['scope'].eq('group_centroid')].sort_values(
            ['contribution', 'symbol_id'], ascending=[False, True])
        assert np.isclose(rows['contribution'].sum(), values[variant_name], rtol=1e-9, atol=0), variant_name
        head = rows.head(SHOWN_SYMBOLS)
        labels, bars, colors = list(head['symbol']), list(head['contribution']), [BLUE] * len(head)
        rest = rows.iloc[SHOWN_SYMBOLS:]
        if len(rest):
            labels.append(f'the other {len(rest)} symbols, summed')
            bars.append(rest['contribution'].sum())
            colors.append(MUTED)
        figure, axis = canvas(f'Which symbols separate hexameter from prose: {VARIANT[variant_name]}',
                              f'Part of the hexameter–prose divergence of {values[variant_name]:.4f} bits due to '
                              f'each symbol; the parts add up to it.\n'
                              + ('All symbols shown.' if not len(rest) else
                                 f'The {SHOWN_SYMBOLS} largest of {len(rows)} symbols; every value is in '
                                 f'jsd_contributions.csv.'),
                              'results/hexis31/v3-seed0-v3006/jsd_contributions.csv', 1.2 + 0.32 * len(bars))
        axis.barh(np.arange(len(bars)), bars, height=0.66, color=colors)
        for y, value in enumerate(bars):
            axis.annotate(f'{value:.2g}' if value < 1e-4 else f'{value:.4f}', (value, y), xytext=(6, 0),
                          textcoords='offset points', va='center', fontsize=9.5, color=INK2)
        rows_axis(axis, labels)
        axis.set_xlabel('contribution (bits)')
        axis.margins(x=0.1)
        panels[f'r1__contributions_{variant_name}'] = figure
    return panels


# 5 · model supports and mixture masses ---------------------------------------------------

def supports(tables):
    """The data of plots.supports_mixture_masses: C0 pooled over documents, bands and seeds."""
    models = tables['model_diagnostics.csv']
    models = models[models['cell'].eq(REF)]
    # a deeper cell's mass columns are empty for C0: dropped, never summed into false zeros (§9.2)
    arms = tables['arm_diagnostics.csv']
    arms = arms[arms['cell'].eq(REF)].dropna(axis=1, how='all')
    panels = {}
    figure, axis = canvas('Contexts stored by the models, by depth',
                          'Mean number of contexts seen in training (nodes of the context tree) per model, at each '
                          'depth of the tree, split by how many times each was seen; main setting.\nLeft bar of '
                          'each pair: original order; right, hatched: shuffled within each sentence.',
                          'results/hexis31/v3-seed0-v3006/model_diagnostics.csv', 4.8)
    top = 0.0
    for offset, (arm, frame) in zip((-0.2, 0.2), models.groupby('arm', sort=True)):
        histograms = [json.loads(value) for value in frame['support_histogram_1_2to4_5to9_10plus_by_depth']]
        depth = max(len(histogram) for histogram in histograms)
        bottom = np.zeros(depth)
        for name, color in zip(plots.SUPPORT_CLASSES, RAMP):
            mean = np.array([sum(h[d][name] for h in histograms if d < len(h))
                             for d in range(depth)]) / len(histograms)
            axis.bar(np.arange(depth) + offset, mean, width=0.38, bottom=bottom, color=color,
                     hatch=None if arm == 'original' else '////', edgecolor=SURFACE, linewidth=0.6)
            bottom += mean
        top = max(top, bottom.max())
    axis.set_ylim(0, top * 1.06)  # the frozen panel clips depth 5; here the tallest stack fits
    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:,.0f}'))
    axis.grid(axis='x', visible=False)
    axis.set(xlabel='depth in the context tree (the sentence start counts as one step)',
             ylabel='contexts per model (mean)')
    seen = {'1': 'seen once', '2to4': 'seen 2–4 times', '5to9': 'seen 5–9 times', '10plus': 'seen 10+ times'}
    legend(axis, [Patch(color=color, label=seen[name])
                  for name, color in zip(plots.SUPPORT_CLASSES, RAMP)]
           + [Patch(facecolor=MUTED, hatch='////', edgecolor=SURFACE, label='shuffled')], columns=5)
    panels['supports__depth'] = figure

    sums = [column for column in arms.columns if column not in
            ('cell', 'variant', 'held_block', 'held_block_key', 'seed', 'doc_id', 'arm', 'past_band',
             'resolved_mean', 'unseen_mass_mean', 'reason')]
    means, counts = {}, {}
    for arm, frame in arms.groupby('arm', sort=True):
        means[arm] = diagnostics.means(frame[sums].sum())
        counts[arm] = (int(frame['resolved_valid_count'].sum()),
                       int(frame[f'resolved_null_count_by_reason_{diagnostics.NO_RESOLVED_MASS}'].sum()))

    figure, axis = canvas('Weight given to each context length',
                          'Mean share of each prediction that the model draws from contexts of each length (number '
                          'of preceding symbols), main setting,\npooled over documents, targets and seeds.',
                          'results/hexis31/v3-seed0-v3006/arm_diagnostics.csv', 4.4)
    for arm, values in means.items():
        name, color = ARM[arm]
        axis.plot(np.arange(len(values['mass'])), values['mass'], color=color, linewidth=2, marker='o',
                  markersize=7, markeredgecolor=SURFACE, label=name)
    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    axis.set(xlabel='context length (preceding symbols; the sentence start is not counted)',
             ylabel='mean share per target')
    legend(axis, None)
    panels['supports__mass_by_length'] = figure

    arm_labels = [f'{ARM[arm][0]}\n({counts[arm][0]:,} targets with a context length, {counts[arm][1]:,} without)'
                  for arm in means]
    for key, name, title, subtitle, xlabel in (
            ('unseen', 'unseen_mass', 'Weight given to contexts never seen in training',
             'Mean share of each prediction that the model assigns to contexts it never saw in training, '
             'main setting.', 'mean share per target'),
            ('L', 'resolved_length', 'Average context length used',
             'Mean length, in preceding symbols, of the contexts each prediction draws on, main setting. A target '
             'whose prediction draws on no seen context has no length: it is counted apart, never as zero.',
             'mean context length (preceding symbols)')):
        figure, axis = canvas(title, subtitle, 'results/hexis31/v3-seed0-v3006/arm_diagnostics.csv', 2.3)
        values = [np.nan if means[arm][key] is None else means[arm][key] for arm in means]
        axis.barh(np.arange(len(values)), values, height=0.55, color=[ARM[arm][1] for arm in means])
        for y, value in enumerate(values):
            axis.annotate(f'{value:.4g}', (value, y), xytext=(6, 0), textcoords='offset points', va='center',
                          fontsize=10, color=INK2)
        rows_axis(axis, arm_labels)
        axis.set_xlabel(xlabel)
        axis.margins(x=0.1)
        panels[f'supports__{name}'] = figure
    return panels


def main():
    tables = {path.name: read(path) for path in sorted(RUN.glob('*.csv'))}
    documents, contingency = read(CORPUS / 'documents.csv'), read(CORPUS / 'audit_contingency.csv')
    cells = [cell['id'] for cell in load_v31_config()['cells']]
    frozen = plots.render(tables, documents, contingency, RUN_ID, cells=cells)
    for name, content in frozen.items():
        assert content == (RUN / name).read_bytes(), f'{name}: the published tables no longer give the frozen figure'
    variant = str(tables['block_pairs.csv'].loc[tables['block_pairs.csv']['cell'].eq(REF), 'variant'].iloc[0])
    weights = tables['aggregation_weights.csv']
    groups = dict(zip(weights['block'], weights['group']))
    with matplotlib.rc_context(STYLE):
        panels = {**corpus(documents, contingency, variant, groups), **profiles(tables, documents, groups),
                  **sensitivities(tables, cells, groups), **r1(tables, variant, groups), **supports(tables)}
        for name, figure in panels.items():
            buffer = io.BytesIO()
            figure.savefig(buffer, format='svg', metadata={'Date': None})
            temporary = OUT / f'.{name}.svg.tmp'
            temporary.write_bytes(buffer.getvalue())
            os.replace(temporary, OUT / f'{name}.svg')
    print(f'frozen figures reproduced byte for byte: {len(frozen)}; panels written: {len(panels)}')


if __name__ == '__main__':
    main()
