"""The five figures of §11.6, drawn from the verified report tables alone.

Every function takes tables `run_report` has just validated — never a model, a ledger
or a sample — and returns a matplotlib Figure; `render` turns the five into SVG bytes
that are identical for identical tables. No figure computes a quantity of its own: a
per-seed value, a mean or a min–max comes from the tables, or from the one aggregation in
`protocols.scores` and `model.diagnostics`. No inferential interval is drawn: the bars
are the computational min–max across seeds (§1.2, §8.2).
"""

import io
import json

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from hormathos.model import diagnostics
from hormathos.protocols import scores

FIGURES = ('corpus_annotation', 'block_document_profiles', 'sensitivities_two_weights', 'R1',
           'supports_mixture_masses')  # report_contract_v3.1.json `figures`, in order
ARTIFACTS = tuple(f'figure__{name}.svg' for name in FIGURES)
REFERENCE_CELL = 'C0'  # the profiles and the R1 matrix are drawn in C0's representation
PROFILE = (('g_original', 'G original'), ('g_shuffled', 'G shuffled'), ('q', 'Q'))
BITS = 'bits per eligible target'
SUPPORT_CLASSES = ('1', '2to4', '5to9', '10plus')
SVG_SETTINGS = {'svg.hashsalt': 'hormathos', 'svg.fonttype': 'none'}  # stable ids, searchable text
COLORS = {'equal_block': 'tab:blue', 'eligible_token_weighted': 'tab:orange', '4_7': 'tab:blue',
          'ge8': 'tab:green', 'original': 'tab:blue', 'shuffled': 'tab:orange', '1': 'tab:blue',
          '2to4': 'tab:orange', '5to9': 'tab:green', '10plus': 'tab:red'}
GROUP_ORDER = (scores.HEX, scores.PROSE)  # report groups, in the order the profiles show them
NAMED_SYMBOLS = 20  # a small alphabet (upos_only, 11) is named on its axis; 100/105 names are in the tables


def _block_order(blocks, groups):
    """Report groups first (HEX, then PROSE_ALL, then anything undeclared), then the block name."""
    return sorted(blocks, key=lambda block: (GROUP_ORDER.index(groups[block]) if groups.get(block) in
                                              GROUP_ORDER else len(GROUP_ORDER), str(block)))


def _footer(figure, run_id):
    figure.supxlabel(f'HORMATHOS · run_id {run_id}', x=0.99, ha='right', fontsize=6)


def _spread(axis, positions, rows, *, label=None, color='black'):
    """Mean marker and the computational min–max across seeds, read from seed_summaries."""
    means = rows['mean'].to_numpy(dtype=float)
    low, high = means - rows['min'].to_numpy(dtype=float), rows['max'].to_numpy(dtype=float) - means
    axis.errorbar(positions, means, yerr=[low, high], fmt='D', color=color, capsize=3, label=label)


def corpus_annotation(documents, contingency, variant, groups, run_id) -> Figure:
    """Figure 1: quantities, retention and the PART/ADV discontinuity of every document (§4.2);
    primary documents by report group then block, inventory_only last."""
    frame = documents[documents['variant'].eq(variant)].copy()
    frame['primary'] = frame['role'].eq('primary')
    order = _block_order(set(frame['dependence_block'].dropna()), groups)
    frame['rank'] = frame['dependence_block'].map(
        {block: index for index, block in enumerate(order)}).fillna(len(order))
    frame = frame.sort_values(['primary', 'rank', 'doc_id'], ascending=[False, True, True])
    labels = [f"{row.author_label}, {row.work}{'' if row.primary else ' (inventory only)'}"
              for row in frame.itertuples()]
    source = contingency[contingency['level'].eq('document')]
    counts = source.pivot_table(index='unit', columns='upos_raw', values='count', aggfunc='sum',
                                fill_value=0)
    position = np.arange(len(frame))
    figure = Figure(figsize=(13, 7), layout='constrained')
    quantities, retention, discontinuity = figure.subplots(1, 3, sharey=True)
    for offset, (column, name) in enumerate((('raw', 'raw tokens'), ('kept', 'retained tokens'),
                                             ('eligible', 'eligible targets'))):
        quantities.barh(position + (offset - 1) * 0.27, frame[column], height=0.27, label=name)
    quantities.set(xscale='log', xlabel='count (log scale)', title=f'Quantities ({variant})')
    quantities.set_yticks(position, labels, fontsize=7)
    quantities.invert_yaxis()
    quantities.legend(fontsize=7)
    colors = ['tab:blue' if primary else 'tab:gray' for primary in frame['primary']]
    retention.barh(position, frame['retention'], color=colors)
    retention.set(xlabel='retained / raw tokens', xlim=(0, 1), title='Retention (grey: inventory only)')
    for offset, tag in enumerate(('PART', 'ADV')):
        shares = [counts.at[doc, tag] / raw if doc in counts.index and tag in counts.columns else 0.0
                  for doc, raw in zip(frame['doc_id'], frame['raw'])]
        discontinuity.barh(position + (offset - 0.5) * 0.4, shares, height=0.4, label=f'source {tag}')
    discontinuity.set(xlabel='share of raw tokens', title='Source PART and ADV\n(merged: ADV_PART)')
    discontinuity.legend(fontsize=7)
    _footer(figure, run_id)
    return figure


def _points(axis, frame, units, metric, *, offset=-0.15):
    for index, unit in enumerate(units):
        values = frame.loc[frame['unit'].eq(unit), metric].to_numpy(dtype=float)
        axis.scatter(np.full(len(values), index + offset), values, s=12, alpha=0.7, color='tab:blue')


def block_document_profiles(block_pairs, document_scores, seed_summaries, documents, groups,
                            run_id) -> Figure:
    """Figure 2: G original, G shuffled and Q of the seven blocks and the eleven documents (C0).

    Blocks follow the report groups (HEX first); each document sits under its block, labelled
    «author, work (n=eligible targets)» so the work that dominates a block is visible (§3.3).
    """
    blocks = block_pairs[block_pairs['cell'].eq(REFERENCE_CELL) & block_pairs['past_band'].eq('all')]
    variant = str(blocks['variant'].iloc[0])
    blocks = blocks.rename(columns={'held_block': 'unit'})
    sums = document_scores[document_scores['cell'].eq(REFERENCE_CELL)]
    scored = scores.ce_gain_q(scores.roll_up(
        sums, keys=['cell', 'variant', 'held_block', 'held_block_key', 'seed', 'doc_id'])).rename(
        columns={'doc_id': 'unit'})
    block_units = _block_order(blocks['unit'].unique(), groups)
    block_of = sums.drop_duplicates('doc_id').set_index('doc_id')['held_block']
    targets = sums[sums['seed'].eq(sums['seed'].min())].groupby('doc_id')['n'].sum()  # fixed across seeds
    names = documents[documents['variant'].eq(variant)].set_index('doc_id')
    label = {doc: f"{names.at[doc, 'author_label']}, {names.at[doc, 'work']} (n={int(targets[doc]):,})"
             for doc in targets.index}
    document_units = sorted(targets.index, key=lambda doc: (block_units.index(block_of[doc]), label[doc]))
    summary = seed_summaries[seed_summaries['cell'].eq(REFERENCE_CELL)
                             & seed_summaries['past_band'].eq('all')]
    figure = Figure(figsize=(15, 9), layout='constrained')
    axes = figure.subplots(2, len(PROFILE))
    levels = (('block', blocks, block_units, [f'{unit} ({groups[unit]})' for unit in block_units]),
              ('document', scored, document_units, [label[unit] for unit in document_units]))
    for row, (level, frame, units, ticks) in enumerate(levels):
        for column, (metric, name) in enumerate(PROFILE):
            axis = axes[row, column]
            _points(axis, frame, units, metric)
            rows = summary[summary['level'].eq(level) & summary['metric'].eq(metric)].set_index('unit')
            _spread(axis, np.arange(len(units)) + 0.15, rows.loc[units])
            axis.axhline(0.0, color='grey', linewidth=0.5)
            axis.set_xticks(np.arange(len(units)), ticks, rotation=60, ha='right', fontsize=7)
            axis.set(title=f'{name} per {level} ({REFERENCE_CELL})', ylabel=BITS)
    figure.suptitle('Profiles: points are seeds; diamonds and bars are the mean and the '
                    'computational min–max across seeds')
    _footer(figure, run_id)
    return figure


def sensitivities_two_weights(contrasts, sensitivity_pairs, seed_summaries, cells, run_id) -> Figure:
    """Figure 3: D_Q under both weightings, the paired differences on the same C0 seeds, bands;
    cells in the declared order, C0 first."""
    cells = [REFERENCE_CELL, *[cell for cell in cells if cell != REFERENCE_CELL]]
    if set(cells) != set(contrasts['cell']):
        raise ValueError(f"figure 3: reported cells {sorted(set(contrasts['cell']))} are not the declared {cells}")
    figure = Figure(figsize=(15, 5), layout='constrained')
    contrast_axis, paired_axis, band_axis = figure.subplots(1, 3)
    offsets = dict(zip(scores.AGGREGATIONS, (-0.15, 0.15)))
    for aggregation, offset in offsets.items():
        rows = contrasts[contrasts['group'].eq('contrast') & contrasts['aggregation'].eq(aggregation)]
        for index, cell in enumerate(cells):
            values = rows.loc[rows['cell'].eq(cell), 'q'].to_numpy(dtype=float)
            contrast_axis.scatter(np.full(len(values), index + offset - 0.08), values, s=10, alpha=0.7,
                                  color=COLORS[aggregation])
        summary = seed_summaries[seed_summaries['level'].eq('group') & seed_summaries['unit'].eq('contrast')
                                 & seed_summaries['aggregation'].eq(aggregation)
                                 & seed_summaries['metric'].eq('q')].set_index('cell')
        _spread(contrast_axis, np.arange(len(cells)) + offset + 0.08, summary.loc[cells], label=aggregation,
                color=COLORS[aggregation])
        pairs = sensitivity_pairs[sensitivity_pairs['level'].eq('group') & sensitivity_pairs['unit'].eq('contrast')
                                  & sensitivity_pairs['aggregation'].eq(aggregation)
                                  & sensitivity_pairs['metric'].eq('q')]
        for index, cell in enumerate(cells[1:], start=1):
            values = pairs.loc[pairs['cell'].eq(cell), 'difference'].to_numpy(dtype=float)
            paired_axis.scatter(np.full(len(values), index + offset), values, s=10, alpha=0.7,
                                color=COLORS[aggregation], label=aggregation if index == 1 else None)
    for axis, title, shown in ((contrast_axis, 'D_Q = HEX − PROSE_ALL, both weightings', cells),
                               (paired_axis, 'Paired difference from C0 on the same seeds', cells[1:])):
        axis.axhline(0.0, color='grey', linewidth=0.5)
        axis.set_xticks([cells.index(cell) for cell in shown], shown)
        axis.set(title=title, ylabel=BITS)
        axis.legend(fontsize=7)
    blocks = seed_summaries[seed_summaries['level'].eq('block') & seed_summaries['metric'].eq('q')]
    for band, offset in (('4_7', -0.15), ('ge8', 0.15)):
        for index, cell in enumerate(cells):
            values = blocks.loc[blocks['cell'].eq(cell) & blocks['past_band'].eq(band), 'mean']
            band_axis.scatter(np.full(len(values), index + offset), values.to_numpy(dtype=float), s=12,
                              marker='o' if band == '4_7' else 's', color=COLORS[band],
                              label=f'past band {band}' if index == 0 else None)
    band_axis.axhline(0.0, color='grey', linewidth=0.5)
    band_axis.set_xticks(np.arange(len(cells)), cells)
    band_axis.set(title='Block Q by past band (mean across seeds)', ylabel=BITS)
    band_axis.legend(fontsize=7)
    _footer(figure, run_id)
    return figure


def jsd_matrix(jsd_pairs, variant):
    """The symmetric block matrix of one variant, read from its C(n,2) pairs (zero diagonal)."""
    rows = jsd_pairs[jsd_pairs['variant'].eq(variant)]
    names = sorted(set(rows['block_a']) | set(rows['block_b']))
    matrix = np.zeros((len(names), len(names)))
    for row in rows.itertuples():
        a, b = names.index(row.block_a), names.index(row.block_b)
        matrix[a, b] = matrix[b, a] = row.jsd
    return names, matrix


def R1(jsd_pairs, jsd_centroids, jsd_contributions, variant, run_id) -> Figure:  # the contract's name
    """Figure 4: the C0 block matrix, the centroid JSD in the three representations, contributions."""
    variants = sorted(set(jsd_pairs['variant']))
    figure = Figure(figsize=(15, 9), layout='constrained')
    grid = figure.add_gridspec(2, max(2, len(variants)))  # matrix and centroids share the first row
    matrix_axis, centroid_axis = figure.add_subplot(grid[0, :-1]), figure.add_subplot(grid[0, -1])
    names, matrix = jsd_matrix(jsd_pairs, variant)
    image = matrix_axis.imshow(matrix, cmap='viridis', vmin=0.0, aspect='auto')  # fills its two columns
    figure.colorbar(image, ax=matrix_axis, label='JSD (bits)')
    matrix_axis.set_xticks(np.arange(len(names)), names, rotation=60, ha='right', fontsize=7)
    matrix_axis.set_yticks(np.arange(len(names)), names, fontsize=7)
    for (a, b), value in np.ndenumerate(matrix):
        matrix_axis.text(b, a, f'{value:.4f}', ha='center', va='center', fontsize=6,
                         color='black' if value > 0.6 * matrix.max() else 'white')
    matrix_axis.set_title(f'R1: block JSD, {variant} (smoothed complete counts)')
    centroids = jsd_centroids.set_index('variant').loc[variants]
    centroid_axis.bar(variants, centroids['jsd'])
    centroid_axis.set(ylabel='JSD (bits)', title='Equal-block group centroids:\nHEX vs PROSE_ALL')
    for column, variant in enumerate(variants):
        axis = figure.add_subplot(grid[1, column])
        rows = jsd_contributions[jsd_contributions['variant'].eq(variant)
                                 & jsd_contributions['scope'].eq('group_centroid')].sort_values('symbol_id')
        axis.bar(rows['symbol_id'], rows['contribution'], width=0.9)
        named = len(rows) <= NAMED_SYMBOLS
        if named:
            axis.set_xticks(rows['symbol_id'], rows['symbol'], rotation=60, ha='right', fontsize=7)
        axis.set(xlabel='symbol (all symbols)' if named else
                 'symbol id (all symbols; names in jsd_contributions.csv)', ylabel='contribution (bits)',
                 title=f'Centroid JSD contributions, {variant}')
    _footer(figure, run_id)
    return figure


def supports_mixture_masses(model_diagnostics, arm_diagnostics, run_id) -> Figure:
    """Figure 5: node supports by depth, observed mass by context length, unseen mass, L_resolved.

    Pooled over C0's documents, bands and seeds through `diagnostics.means` (§9.3): L_resolved
    over its valid targets, the masses over all targets; nulls are counted, never zeroed.
    """
    models = model_diagnostics[model_diagnostics['cell'].eq(REFERENCE_CELL)]
    # a deeper cell's mass columns are empty for C0: dropped, never summed into false zeros (§9.2)
    arms = arm_diagnostics[arm_diagnostics['cell'].eq(REFERENCE_CELL)].dropna(axis=1, how='all')
    figure = Figure(figsize=(17, 5), layout='constrained')
    support_axis, mass_axis, unseen_axis, resolved_axis = figure.subplots(1, 4)
    for offset, (arm, frame) in zip((-0.2, 0.2), models.groupby('arm', sort=True)):
        histograms = [json.loads(value) for value in frame['support_histogram_1_2to4_5to9_10plus_by_depth']]
        depth = max(len(histogram) for histogram in histograms)
        bottom = np.zeros(depth)
        for name in SUPPORT_CLASSES:
            mean = np.array([sum(h[d][name] for h in histograms if d < len(h))
                             for d in range(depth)]) / len(histograms)
            support_axis.bar(np.arange(depth) + offset, mean, width=0.4, bottom=bottom, color=COLORS[name],
                             hatch=None if arm == 'original' else '//', edgecolor='white',
                             label=f'support {name}' if arm == 'original' else None)
            bottom += mean
    support_axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    support_axis.set(xlabel='structural depth (plain: original, hatched: shuffled)',
                     ylabel='observed nodes per model (mean)', title=f'Model supports ({REFERENCE_CELL})')
    support_axis.legend(fontsize=7)
    sums = [column for column in arms.columns if column not in
            ('cell', 'variant', 'held_block', 'held_block_key', 'seed', 'doc_id', 'arm', 'past_band',
             'resolved_mean', 'unseen_mass_mean', 'reason')]
    names, unseen, resolved = [], [], []
    for arm, frame in arms.groupby('arm', sort=True):
        means = diagnostics.means(frame[sums].sum())
        mass_axis.plot(np.arange(len(means['mass'])), means['mass'], marker='o', color=COLORS[arm], label=arm)
        valid = int(frame['resolved_valid_count'].sum())
        null = int(frame[f'resolved_null_count_by_reason_{diagnostics.NO_RESOLVED_MASS}'].sum())
        names.append(f'{arm}\nvalid {valid}, null {null}')
        unseen.append(means['unseen'])
        resolved.append(np.nan if means['L'] is None else means['L'])
    colors = [COLORS[arm] for arm in sorted(set(arms['arm']))]
    mass_axis.set(xlabel='lexical context length ℓ', ylabel='mean observed mass per target',
                  title='Mixture mass by context length')
    mass_axis.legend(fontsize=7)
    unseen_axis.bar(names, unseen, color=colors)
    unseen_axis.set(ylabel='mean unseen mass per target', title='Mass routed to unseen branches')
    resolved_axis.bar(names, resolved, color=colors)
    resolved_axis.set(ylabel='mean L_resolved (context symbols)', title='L_resolved over valid targets (§9.2)')
    _footer(figure, run_id)
    return figure


def build(tables, documents, contingency, run_id, *, cells) -> dict:
    """The five figures as matplotlib Figures, keyed by their artifact names."""
    variant = tables['block_pairs.csv'].loc[tables['block_pairs.csv']['cell'].eq(REFERENCE_CELL), 'variant']
    if variant.nunique() != 1:
        raise ValueError(f'{REFERENCE_CELL}: the figures need exactly one reference representation')
    variant = str(variant.iloc[0])
    weights = tables['aggregation_weights.csv']
    groups = dict(zip(weights['block'], weights['group']))
    figures = (corpus_annotation(documents, contingency, variant, groups, run_id),
               block_document_profiles(tables['block_pairs.csv'], tables['document_scores.csv'],
                                       tables['seed_summaries.csv'], documents, groups, run_id),
               sensitivities_two_weights(tables['contrasts.csv'], tables['sensitivity_pairs.csv'],
                                         tables['seed_summaries.csv'], cells, run_id),
               R1(tables['jsd_pairs.csv'], tables['jsd_centroids.csv'], tables['jsd_contributions.csv'],
                  variant, run_id),
               supports_mixture_masses(tables['model_diagnostics.csv'], tables['arm_diagnostics.csv'],
                                       run_id))
    return dict(zip(ARTIFACTS, figures))


def render(tables, documents, contingency, run_id, *, cells) -> dict:
    """The five figures as SVG bytes, identical for identical tables."""
    rendered = {}
    with matplotlib.rc_context(SVG_SETTINGS):
        for name, figure in build(tables, documents, contingency, run_id, cells=cells).items():
            buffer = io.BytesIO()
            figure.savefig(buffer, format='svg', metadata={'Date': None})
            rendered[name] = buffer.getvalue()
    return rendered
