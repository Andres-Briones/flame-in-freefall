import copy
import itertools
import json

import numpy as np
import pandas as pd
import pytest

from fif import api, models
from fif.pipeline import build_models as bm

CARD_KEYS = {
    "id", "accession", "kind", "use", "question", "target", "target_definition", "features", "training_filter",
    "n", "n_groups", "target_summary", "estimator", "coefficients", "cv_scheme", "cv", "comparison_cv",
    "cv_metric", "tree_rules", "interpretation", "caveats", "must_not_be_used_for",
}
FEATURE_KEYS = {"name", "unit", "transform", "expected_sign", "why", "domain"}


@pytest.fixture(scope="module")
def tests_table():
    return bm.load_tests()


@pytest.fixture(scope="module")
def built(tests_table, tmp_path_factory):
    out = tmp_path_factory.mktemp("models")
    doc, bundles = bm.build(tests_table)
    bm.write(doc, bundles, out_dir=out, docs_path=out / "models.md")
    return doc, out


@pytest.fixture
def from_build(built, monkeypatch):
    monkeypatch.setattr(models, "PROCESSED", built[1])
    return built[0]


def card(doc, model_id):
    return next(c for c in doc["models"] if c["id"] == model_id)


def middle(c):
    return {f["name"]: f["allowed"][-1] if f.get("allowed") else (f["domain"][0] + f["domain"][1]) / 2
            for f in c["features"]}


def test_models_json_has_required_keys(built):
    doc, out = built
    on_disk = json.loads((out / "models.json").read_text())
    assert on_disk == doc
    assert doc["dropped"] and all({"id", "accession", "reason"} <= set(d) for d in doc["dropped"])
    for c in doc["models"]:
        assert CARD_KEYS <= set(c), c["id"]
        assert all(FEATURE_KEYS <= set(f) for f in c["features"])
        assert c["n"] == c["training_filter"][-1]["rows"]
        assert {"grouped_by_date", "ungrouped"} == set(c["cv"])
        assert c["caveats"]


def test_one_investigation_per_model(built, tests_table):
    for c in built[0]["models"]:
        assert c["accession"] in set(tests_table["accession"])


def test_predict_flags_out_of_domain_and_withholds_prediction(from_build):
    c = card(from_build, "flex_burning_rate")
    conditions = middle(c)
    inside = models.predict(c["id"], **conditions)
    assert inside["in_domain"] and inside["prediction"] is not None
    lo, hi = inside["interval"]
    assert lo < inside["prediction"] < hi

    conditions["x_o2_ambient"] = c["features"][1]["domain"][1] + 0.01
    outside = models.predict(c["id"], **conditions)
    assert outside["in_domain"] is False
    assert set(outside["outside_domain"]) == {"x_o2_ambient"}
    assert outside["prediction"] is None
    assert models.predict(c["id"], allow_extrapolation=True, **conditions)["prediction"] is not None


def test_predict_classifier_returns_probability(from_build):
    c = card(from_build, "cfig_inverse_self_extinction")
    out = models.predict(c["id"], **middle(c))
    assert 0 <= out["probability"] <= 1
    assert out["prediction"] == (out["probability"] >= 0.5)
    assert out["n_train"] == c["n"] and out["cv_metric"]["name"] == "roc_auc"


def test_descriptive_models_give_no_prediction(from_build):
    c = card(from_build, "cfi_reignition")
    out = models.predict(c["id"], **middle(c))
    assert out["use"] == "descriptive" and out["prediction"] is None
    assert out["observed"] and out["nearest_tests"]


def test_nearest_tests_are_real_ids_of_the_right_accession(from_build, tests_table):
    for c in from_build["models"]:
        out = models.predict(c["id"], **middle(c))
        ids = set(tests_table.loc[tests_table["accession"] == c["accession"], "test_id"].astype(str))
        nearest = out["nearest_tests"]
        assert 3 <= len(nearest) <= 5
        assert all(n["test_id"] in ids for n in nearest), c["id"]
        assert [n["distance"] for n in nearest] == sorted(n["distance"] for n in nearest)


def test_predict_rejects_wrong_inputs(from_build):
    with pytest.raises(ValueError):
        models.predict("flex_burning_rate", x_o2_ambient=0.21)


def test_predict_withholds_a_value_in_an_untested_range(from_build):
    c = card(from_build, "cfig_normal_self_extinction")
    gap = c["features"][0]["untested"][0]
    assert gap["range"] == [0.25, 0.35] and gap["n_tests"] <= 5
    conditions = {**middle(c), "n_carbon": 3}
    for o2 in (0.25, 0.30, 0.35):
        out = models.predict(c["id"], **{**conditions, "x_o2_ambient": o2})
        assert out["in_domain"] is False and out["prediction"] is None
        assert "only" in out["outside_domain"]["x_o2_ambient"]["reason"]
    assert models.predict(c["id"], **{**conditions, "x_o2_ambient": 0.21})["in_domain"]


def test_predict_refuses_impossible_conditions(from_build):
    c = card(from_build, "flex_burning_rate")
    ok = {**middle(c), "is_heptane": 1, "x_co2": 0.0, "x_he": 0.0}
    assert models.predict(c["id"], **ok)["prediction"] is not None
    with pytest.raises(ValueError, match="is_heptane"):
        models.predict(c["id"], **{**ok, "is_heptane": 0.5})
    with pytest.raises(ValueError, match="sum to more than 1"):
        models.predict(c["id"], **{**ok, "x_co2": 0.6, "x_he": 0.4})


def test_log_target_is_returned_in_the_target_unit(from_build, monkeypatch):
    c = card(from_build, "spice_smoke_point_length")
    predictive = {**models.cards(), c["id"]: {**c, "use": "predictive"}}
    monkeypatch.setattr(models, "cards", lambda: predictive)
    out = models.predict(c["id"], **middle(c))
    lo, hi = c["target_summary"]["min"], c["target_summary"]["max"]
    assert lo / 3 < out["prediction"] < hi * 3 and out["interval"][0] < out["prediction"] < out["interval"][1]


def test_headline_metric_carries_its_interval(built):
    for c in built[0]["models"]:
        lo, hi = c["cv_metric"]["grouped_pooled_ci95_days_resampled"]
        assert lo < hi and "folds_without_metric" in c["cv_metric"]
    assert card(built[0], "cfig_inverse_self_extinction")["cv_metric"]["folds_without_metric"] == 1
    s = card(built[0], "flex_burning_rate")["sensitivity"]
    assert s["excluded"] > 0 and abs(s["per_unit"]["log10(pressure_kpa)"]) < 0.05


def test_build_is_reproducible(built, tests_table):
    again, _ = bm.build(tests_table)
    assert json.dumps(again, sort_keys=True) == json.dumps(built[0], sort_keys=True)


def test_wilson_interval():
    lo, hi = models.wilson(0, 26)
    assert lo == 0 and 0.12 < hi < 0.14
    lo, hi = models.wilson(41, 41)
    assert 0.9 < lo < 0.93 and hi == pytest.approx(1)


def test_rows_records_every_exclusion():
    df = pd.DataFrame({"a": [1, 2, None, 4]})
    rows = bm.Rows(df, "start").drop(df["a"].isna(), "missing a")
    assert rows.steps == [{"step": "start", "rows": 4}, {"excluded": 1, "why": "missing a"}]
    assert len(rows.df) == 3


def toy(n_days=12, per_day=6, seed=0):
    import numpy as np
    rng = np.random.default_rng(seed)
    groups = np.repeat([f"d{i:02d}" for i in range(n_days)], per_day)
    X = rng.normal(size=(len(groups), 2)) * [1.0, 50.0]
    return X, groups, rng


def test_score_range_resamples_the_estimator_it_is_given(monkeypatch):
    from sklearn.dummy import DummyRegressor
    monkeypatch.setattr(bm, "N_BOOT_CV", 20)
    X, groups, rng = toy()
    y = 2 * X[:, 0] + 0.1 * rng.normal(size=len(groups))
    good = bm.metric_interval(bm.primary("regressor"), "regressor", X, y, groups)
    assert good["ci95"][0] > 0.9
    mean_only = bm.metric_interval(DummyRegressor(), "regressor", X, y, groups)
    assert mean_only["ci95"][1] <= 0


def test_bootstrap_coefficients_are_per_unit_with_each_resamples_own_scaler(monkeypatch):
    import numpy as np
    monkeypatch.setattr(bm, "N_BOOT", 20)
    X, groups, _ = toy()
    X[:, 1] *= np.repeat(np.arange(1, 13), 6)  # the SD of a resample depends on which days it drew
    y = 2 * X[:, 0] - 0.01 * X[:, 1]
    boot = bm.bootstrap_coefs(bm.primary("regressor"), "regressor", X, y, groups)
    assert np.allclose(boot, [2, -0.01])


def test_coefficient_interval_is_one_interval_on_two_scales(built):
    for c in built[0]["models"]:
        for t in c["coefficients"]["terms"]:
            sd = t["per_sd"] / t["per_unit"]
            for a, b in zip(t["per_sd_ci95_cluster_bootstrap"], t["per_unit_ci95_cluster_bootstrap"]):
                assert a == pytest.approx(b * sd, rel=2e-3, abs=1e-9), (c["id"], t["feature"])
            excludes_zero = t["per_unit_ci95_cluster_bootstrap"][0] > 0 or t["per_unit_ci95_cluster_bootstrap"][1] < 0
            if t["expected_sign"] != "?":
                assert ("includes 0" in t["agreement"]) != excludes_zero


def test_range_coverage_is_counted_on_days_the_range_never_saw():
    import numpy as np
    X, groups, rng = toy(n_days=20, per_day=10)
    y = X[:, 0] + rng.normal(size=len(groups))
    y[groups == "d00"] += 100  # one day far off: its own residuals must not widen its own range
    est = bm.primary("regressor")
    folds = bm.splits("regressor", X, y, groups)["grouped_by_date"]
    oof = bm.cross_validate(est, "regressor", X, y, folds)[1]
    by = ("day", np.where(groups == "d00", "odd", "rest"))
    cov = bm.range_coverage(est, "regressor", X, y, groups, folds, oof, by=by, floor=y.min())
    odd, rest = cov["by"]["levels"]["odd"], cov["by"]["levels"]["rest"]
    assert odd["n_inside"] == 0 and odd["n"] == 10 and odd["verdict"] == "below nominal"
    assert rest["n"] == 190 and 0.8 < rest["fraction"] <= 1
    assert cov["n_inside"] == odd["n_inside"] + rest["n_inside"] and cov["n"] == 200
    assert cov["n_inside"] + cov["n_below"] + cov["n_above"] == cov["n"]
    assert cov["n_clipped_at_floor"] > 0  # the lowest tests have a range that starts under the lowest value seen


def test_regressor_cards_report_measured_coverage_apart_from_the_target(built):
    for c in built[0]["models"]:
        if c["kind"] != "regressor":
            assert "prediction_interval" not in c
            continue
        pi = c["prediction_interval"]
        cov = pi["held_out_coverage"]
        assert pi["nominal"] == 0.9 and 0 < cov["n_inside"] <= cov["n"] == c["n"]
    burn = card(built[0], "flex_burning_rate")["prediction_interval"]["held_out_coverage"]
    levels = burn["by"]["levels"]
    assert set(levels) == {"methanol", "n-heptane"}
    assert sum(v["n"] for v in levels.values()) == burn["n"]
    assert sum(v["n_inside"] for v in levels.values()) == burn["n_inside"]
    assert levels["n-heptane"]["verdict"] == "below nominal"
    assert "too narrow for n-heptane" in (built[1] / "models.md").read_text()
    ext = card(built[0], "flex_methanol_extinction_diameter")["prediction_interval"]
    assert ext["floor"] == 0 and ext["held_out_coverage"]["n_clipped_at_floor"] > 0


def test_predict_never_gives_a_negative_diameter_range_and_says_when_it_cut(from_build):
    c = card(from_build, "flex_methanol_extinction_diameter")
    low = {**middle(c), "d0_mm": c["features"][0]["domain"][0], "x_o2_ambient": 0.21, "x_co2": 0.0, "x_he": 0.0}
    out = models.predict(c["id"], **low)
    lo, hi = out["interval_unclipped"]
    assert lo < 0 < hi and out["interval"] == [0, hi] and out["interval_low_unclipped"] == lo
    assert out["interval_clipped"] is True and out["interval_unavailable"] is None
    assert out["prediction_below_floor"] is False and out["prediction_unavailable"] is None
    assert out["prediction"] == out["prediction_raw"] and 0 <= out["prediction"] <= hi
    mid = models.predict(c["id"], **{**middle(c), "x_co2": 0.0, "x_he": 0.0})
    assert mid["prediction_below_floor"] is False
    assert mid["interval_clipped"] is False and mid["interval_low_unclipped"] == mid["interval"][0] > 0
    assert mid["unit"] == "mm" and mid["interval_nominal"] == 0.9 and mid["interval_method"]
    assert mid["interval_coverage"] == c["prediction_interval"]["held_out_coverage"]


TEAM_CASE = {"d0_mm": 1.61, "x_o2_ambient": 0.30, "x_co2": 0.0, "x_he": 0.0, "pressure_kpa": 101.3}


def test_predict_gives_no_range_when_the_whole_range_is_below_zero(from_build):
    out = models.predict("flex_methanol_extinction_diameter", **TEAM_CASE)
    low, high = out["interval_unclipped"]
    assert out["in_domain"] and high < 0  # the case a teammate reported: [0, -0.02] before the fix
    assert out["interval"] is None and out["interval_clipped"] is False
    assert out["interval_unavailable"] == "the whole range is below 0, which is impossible"
    assert out["interval_low_unclipped"] == low < high
    assert out["prediction"] is None and out["prediction_below_floor"] is True and low < out["prediction_raw"] < high
    notes = api.predict(model_id="flex_methanol_extinction_diameter", **TEAM_CASE)["notes"]
    assert not any("was cut at 0" in n for n in notes)
    assert any("No estimate is given" in n for n in notes)


NEGATIVE_CASE = {**TEAM_CASE, "d0_mm": 1.7}  # estimate about -0.68 mm, range [-1.32, 0.05] before any cut


def test_predict_withholds_an_estimate_below_zero(from_build):
    out = models.predict("flex_methanol_extinction_diameter", **NEGATIVE_CASE)
    low, high = out["interval_unclipped"]
    assert out["in_domain"] and out["prediction_raw"] < 0 < high
    assert out["prediction"] is None and out["prediction_below_floor"] is True
    assert out["prediction_unavailable"] == "the estimate is below 0, which is impossible"
    assert out["interval"] is None and out["interval_clipped"] is False
    assert out["interval_unavailable"] == "no estimate is given (it is below 0), so no range either"
    assert low < out["prediction_raw"] < high and out["interval_low_unclipped"] == low
    notes = api.predict(model_id="flex_methanol_extinction_diameter", **NEGATIVE_CASE)["notes"]
    assert any("No estimate is given" in n and "nearest_tests" in n for n in notes)
    assert not any("Do not use this value" in n or "No range is available" in n or "targets 90%" in n for n in notes)


def test_predict_withholds_the_range_even_when_its_upper_end_is_exactly_zero(from_build, monkeypatch):
    y = models.predict("flex_methanol_extinction_diameter", **TEAM_CASE)["prediction_raw"]
    doc = copy.deepcopy(models.cards())
    doc["flex_methanol_extinction_diameter"]["prediction_interval"]["residual_quantiles"] = [-1.0, -y]
    monkeypatch.setattr(models, "cards", lambda: doc)
    out = models.predict("flex_methanol_extinction_diameter", **TEAM_CASE)
    assert out["interval_unclipped"][1] == 0 and out["prediction"] is None
    assert out["interval"] is None and out["interval_unavailable"].startswith("no estimate is given")


def test_every_returned_range_is_ordered_and_above_the_floor(from_build):
    withheld = {}
    for c in from_build["models"]:
        if c["kind"] != "regressor":
            continue
        floor = c["prediction_interval"].get("floor")
        axes = [f["allowed"] if f.get("allowed") else np.linspace(*f["domain"], 4) for f in c["features"]]
        names = [f["name"] for f in c["features"]]
        for values in itertools.product(*axes):
            x = dict(zip(names, map(float, values)))
            if sum(x.get(n, 0) for n in (c.get("constraints") or {}).get("sum_at_most_one", [])) > 1:
                continue
            out = models.predict(c["id"], **x)
            if out.get("prediction_below_floor"):
                withheld[c["id"]] = withheld.get(c["id"], 0) + 1
                assert out["prediction"] is None and out["interval"] is None and out["prediction_raw"] < floor
                assert out["prediction_unavailable"] and out["interval_unavailable"]
                continue
            if out["prediction"] is None:
                continue
            assert floor is None or (out["prediction"] >= floor and out["prediction_unavailable"] is None)
            assert out["interval"] is not None, (c["id"], x)
            low, high = out["interval"]
            assert (floor if floor is not None else -np.inf) <= low <= out["prediction"] <= high, (c["id"], x, out)
    assert set(withheld) == {"flex_methanol_extinction_diameter"}  # 41 of its 752 grid points


def test_classifier_headline_carries_brier_next_to_auc(from_build):
    for c in from_build["models"]:
        m = c["cv_metric"]
        if c["kind"] == "classifier":
            assert m["brier_grouped_pooled"] == c["cv"]["grouped_by_date"]["brier"]["pooled"]
            assert 0 <= m["brier_baseline_grouped_pooled"] <= 1
        else:
            assert "brier_grouped_pooled" not in m
    c = card(from_build, "cfig_inverse_self_extinction")
    assert "brier_grouped_pooled" in models.predict(c["id"], **middle(c))["cv_metric"]
