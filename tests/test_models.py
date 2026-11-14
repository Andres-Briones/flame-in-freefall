import json

import pandas as pd
import pytest

from fif import models
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
