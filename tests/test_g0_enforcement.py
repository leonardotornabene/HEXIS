"""Tests for the repository-local G0 gate: enforcement (D45/D52(iii)) and
mandatory-coverage inventory (D52(ii))."""

import ast
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
ROOT_CONFTEST = TESTS_DIR.parent / "conftest.py"
pytestmark = pytest.mark.g0

# D52(ii) minimum mandatory coverage, plus the §7 scoring-boundary case gated at
# G0, mapped onto D52(ii)'s "expected minimum file organization". The clause
# permits tests to be "split, merged or parametrized differently provided the
# mandatory coverage stays explicit and traceable" — reorganizing therefore
# means editing this map, which is what keeps the inventory traceable.
#
# Each area maps to (filename, required g0 test names). A file-level count alone
# left the inventory decorative: an area key names behaviours as fine as "under
# both P-RESET and P-BOUND", but deleting every P-BOUND test kept the gate green
# because the file still held twenty other g0 tests. Where a key enumerates
# behaviours, the named tests are mandatory by exact name; renaming one is a
# deliberate edit here, which is the traceability act D52(ii) asks for. Empty
# required-name tuples are rejected: they recreate the file-level hole.
SEQUENCES_AREA = "sequence construction under both P-RESET and P-BOUND (§3.5, D52(x))"
PERMUTATION_AREA = "exact document-label permutation and sign-flip utilities"

G0_REQUIRED_COVERAGE = {
    "conllu_reader": (
        "test_conllu_reader.py",
        (
            "test_malformed_row_raises_parse_error_with_location",
            "test_missing_sent_id_raises_parse_error",
            "test_id_order_preserved",
            "test_out_of_order_integer_ids_raise_parse_error",
        ),
    ),
    "total alphabet mapping (§3.4)": (
        "test_alphabet.py",
        (
            "test_subtype_stripping_incl_multi_colon",
            "test_propn_maps_to_noun",
            "test_drop_rules",
            "test_upos_rule_precedes_deprel_rule",
            "test_excluded_deprel_dropped_under_primary_policy",
            "test_oth_arm",
            "test_totality_on_any_ud_label",
            "test_upos_only_keeps_the_retention_rules",
            "test_upos_only_alphabet_is_the_twelve_retained_tags",
            "test_inconsistent_alphabet_configuration_raises",
            "test_synthetic_conllu_with_mwt_and_empty_node",
        ),
    ),
    "registry construction and validation": (
        "test_registry.py",
        (
            "test_doc_id_derived_from_sent_id_prefix",
            "test_counts_aggregate_over_gappy_ordinals_and_split_files",
            "test_n_tokens_raw_counts_integer_id_words_before_alphabet",
            "test_newdoc_id_disagreement_raises",
            "test_build_registry_assigns_taxonomy_and_schema",
            "test_regime_labels_are_exactly_the_five_of_d04",
            "test_build_registry_accepts_every_d04_regime",
            "test_overrides_merge_raw_prefixes_into_canonical_document",
            "test_merge_rejects_inconsistent_metadata",
            "test_canonical_doc_id_must_be_a_nonempty_string",
            "test_merge_into_a_canonical_that_is_not_itself_a_raw_prefix",
            "test_merge_requires_explicit_source_urn_on_every_contributor",
            "test_unshared_canonical_target_is_rejected",
            "test_typo_in_a_merge_target_splits_the_group_and_is_rejected",
            "test_unicode_homoglyph_target_is_rejected",
            "test_canonical_target_chain_is_rejected",
            "test_self_targeting_prefix_without_merge_is_allowed",
            "test_n_tokens_retained_is_nullable_until_the_alphabet_is_frozen",
            "test_unassigned_document_raises",
            "test_unknown_override_raises",
            "test_invalid_regime_raises",
            "test_missing_override_field_raises",
        ),
    ),
    SEQUENCES_AREA: (
        "test_sequences.py",
        (
            "test_build_sequences_keeps_retained_symbols_in_token_order",
            "test_all_dropped_sentence_remains_an_empty_row",
            "test_sequences_never_carry_the_boundary_symbol",
            "test_p_reset_returns_one_sequence_per_sentence",
            "test_p_bound_returns_one_stream_with_exactly_n_minus_one_boundaries",
            "test_p_bound_produces_adjacent_boundaries_around_an_all_dropped_sentence",
            "test_extend_alphabet_bound_appends_at_size_and_keeps_ids_stable",
            "test_extend_alphabet_bound_does_not_mutate_the_frozen_alphabet",
            "test_to_model_input_never_spans_documents",
            "test_manifest_records_the_runtime_alphabet_extension",
        ),
    ),
    "sentence-aligned document-safe blocks": (
        "test_blocks.py",
        (
            "test_sentence_aligned_fill",
            "test_tail_kept_iff_at_least_min_frac",
            "test_never_spans_documents",
        ),
    ),
    PERMUTATION_AREA: (
        "test_permutation.py",
        (
            "test_enumeration_counts",
            "test_label_permutation_exact_pvalues",
            "test_sign_flip_exact_pvalues",
            "test_null_synthetic_p_uniform",
            "test_planted_effect_small_p",
            "test_one_two_sided_consistency",
        ),
    ),
    "bootstrap reproducibility and Holm correction": (
        "test_bootstrap_holm.py",
        (
            "test_holm_family_of_two_thresholds",
            "test_holm_step_down_stops_at_first_non_reject",
            "test_holm_boundary_and_order_invariance",
            "test_bootstrap_reproducible_under_fixed_seed",
        ),
    ),
    "seed derivation, resolved-config hash, run manifest, sidecar, overwrite refusal": (
        "test_determinism.py",
        (
            "test_seed_derivation_matches_spec_formula",
            "test_load_config_reads_frozen_defaults",
            "test_config_hash_canonical_and_sensitive",
            "test_resolve_config_deep_merges_without_mutating_base",
            "test_build_manifest_carries_d46_fields_and_artifact_hashes",
            "test_write_manifest_central_path_and_refuses_overwrite",
            "test_write_manifest_refusal_is_atomic",
            "test_write_sidecar_is_minimal_and_refuses_overwrite",
        ),
    ),
    "label-free scoring core signature (§7 scoring-boundary case 1)": (
        "test_scores.py",
        ("test_pooled_score_core_has_label_free_signature",),
    ),
}


def _is_pytest_g0_marker(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        node = node.func
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "g0"
        and isinstance(node.value, ast.Attribute)
        and node.value.attr == "mark"
        and isinstance(node.value.value, ast.Name)
        and node.value.value.id == "pytest"
    )


def _contains_pytest_g0_marker(node: ast.AST) -> bool:
    if _is_pytest_g0_marker(node):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return any(_is_pytest_g0_marker(element) for element in node.elts)
    return False


def _g0_test_names(path: Path) -> set:
    """Names of the test functions in `path` carrying the g0 marker."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module_marked = any(
        isinstance(node, ast.Assign)
        and any(getattr(target, "id", None) == "pytestmark" for target in node.targets)
        and _contains_pytest_g0_marker(node.value)
        for node in tree.body
    )
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        and (
            module_marked
            or any(_is_pytest_g0_marker(dec) for dec in node.decorator_list)
        )
    }


def _missing_coverage(tests_dir: Path, inventory: dict) -> dict:
    """Areas of `inventory` not covered by g0 tests under `tests_dir`, mapped to
    the reason: a missing file, no g0 test at all, or absent mandatory names."""
    missing = {}
    for area, (filename, required) in inventory.items():
        path = tests_dir / filename
        if not path.is_file():
            missing[area] = f"tests/{filename} does not exist"
            continue
        if not required:
            missing[area] = f"tests/{filename} has no mandatory test names in inventory"
            continue
        present = _g0_test_names(path)
        if not present:
            missing[area] = f"tests/{filename} declares no g0 test"
            continue
        absent = sorted(set(required) - present)
        if absent:
            missing[area] = f"tests/{filename} is missing {absent}"
    return missing


def test_g0_set_covers_every_mandatory_area():
    """G0 cannot close on a subset: `-m g0` must stay red until every mandatory
    D52(ii) area declares g0 coverage. Without this, deselection makes an
    incomplete set look green (the marker set is a subset by construction), and
    without the per-area names a file could keep its g0 tests while losing the
    behaviour its inventory key promises."""
    missing = _missing_coverage(TESTS_DIR, G0_REQUIRED_COVERAGE)
    assert not missing, "incomplete mandatory D52(ii) coverage: " + "; ".join(
        f"{area}: {reason}" for area, reason in sorted(missing.items())
    )


def test_inventory_rejects_a_tree_that_lost_the_p_bound_test(tmp_path):
    """Regression for the hole this granularity closes: a `test_sequences.py` that
    kept every other g0 test but dropped P-BOUND used to satisfy the inventory,
    leaving D52(x)'s boundary policy unguarded."""
    filename, required = G0_REQUIRED_COVERAGE[SEQUENCES_AREA]
    dropped = "test_p_bound_returns_one_stream_with_exactly_n_minus_one_boundaries"
    assert dropped in required
    (tmp_path / filename).write_text(
        "import pytest\n\npytestmark = pytest.mark.g0\n\n"
        + "".join(
            f"def {name}():\n    assert True\n\n" for name in required if name != dropped
        ),
        encoding="utf-8",
    )

    missing = _missing_coverage(tmp_path, {SEQUENCES_AREA: (filename, required)})

    assert dropped in missing[SEQUENCES_AREA]


def test_g0_name_scan_rejects_uncollected_and_non_pytest_markers(tmp_path):
    """Only module-level tests carrying pytest.mark.g0 are inventory evidence.

    A nested function is not collected by pytest, and an unrelated decorator
    named ``g0`` does not place a test in the canonical ``-m g0`` selection.
    """
    path = tmp_path / "test_synthetic.py"
    path.write_text(
        "import pytest\n\n"
        "def marker(fn):\n    return fn\n\n"
        "marker.g0 = marker\n\n"
        "@pytest.mark.g0\n"
        "def test_real():\n    assert True\n\n"
        "@marker.g0\n"
        "def test_unrelated_marker():\n    assert True\n\n"
        "def helper():\n"
        "    @pytest.mark.g0\n"
        "    def test_nested():\n"
        "        assert True\n"
        "    return test_nested\n",
        encoding="utf-8",
    )

    assert _g0_test_names(path) == {"test_real"}


def test_inventory_rejects_an_area_without_named_behaviours(tmp_path):
    path = tmp_path / "test_area.py"
    path.write_text(
        "import pytest\n\npytestmark = pytest.mark.g0\n\n"
        "def test_something():\n    assert True\n",
        encoding="utf-8",
    )

    missing = _missing_coverage(tmp_path, {"area": (path.name, ())})

    assert "no mandatory test names" in missing["area"]


def test_inventory_rejects_a_shared_file_that_lost_label_permutation(tmp_path):
    area = PERMUTATION_AREA
    filename, required = G0_REQUIRED_COVERAGE[area]
    dropped = "test_label_permutation_exact_pvalues"
    (tmp_path / filename).write_text(
        "import pytest\n\npytestmark = pytest.mark.g0\n\n"
        "def test_sign_flip_exact_pvalues():\n    assert True\n",
        encoding="utf-8",
    )

    missing = _missing_coverage(tmp_path, {area: (filename, required)})

    assert dropped in missing[area]


def _config(*, assertion_pass=True):
    return (
        '[tool.pytest.ini_options]\n'
        'markers = ["g0: gate"]\n'
        'xfail_strict = true\n'
        f'enable_assertion_pass_hook = {str(assertion_pass).lower()}\n'
        'addopts = "--strict-markers"\n'
    )


def _seed(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(_config())


def _run_g0(pytester):
    return pytester.runpytest_subprocess("-m", "g0", "--strict-markers")


def test_enforcement_fails_on_dynamically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_s():\n    pytest.skip('dynamic')\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_statically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.skip('static')\n"
        "def test_s():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_xpass(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.xfail(reason='but passes')\n"
        "def test_x():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_nonstrict_xpass(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.xfail(reason='but passes', strict=False)\n"
        "def test_x():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_module_marked_assertion_free_test(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\npytestmark = pytest.mark.g0\n\ndef test_x():\n    pass\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_when_assertion_is_dead_code(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_x():\n"
        "    if False:\n        assert False\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_collection_time_skip(pytester):
    _seed(pytester)
    pytester.makepyfile(
        test_ok=(
            "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert True\n"
        ),
        test_skipped=(
            "import pytest\n\npytestmark = pytest.mark.g0\n"
            "pytest.skip('collection skip', allow_module_level=True)\n"
        ),
    )
    assert _run_g0(pytester).ret != 0


def test_collection_skip_in_non_g0_module_is_ignored(pytester):
    _seed(pytester)
    pytester.makepyfile(
        test_ok=(
            "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert True\n"
        ),
        test_skipped=(
            '"""This non-G0 module merely documents ``pytest.mark.g0``."""\n'
            "import pytest\npytest.skip('optional module', allow_module_level=True)\n"
        ),
    )
    assert _run_g0(pytester).ret == 0


def test_enforcement_passes_a_clean_g0_suite(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert 1 == 1\n"
    )
    assert _run_g0(pytester).ret == 0


def test_enforcement_invalidates_pyc_created_without_assertion_hook(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(_config(assertion_pass=False))
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert 1 == 1\n"
    )
    assert _run_g0(pytester).ret != 0

    pytester.makepyprojecttoml(_config(assertion_pass=True))
    assert _run_g0(pytester).ret == 0
