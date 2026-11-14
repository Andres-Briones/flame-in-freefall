"""Small per-investigation models of PSI test outcomes, and `predict` for the dashboard.

The models are built by `fif.pipeline.build_models`: one card per model in
`data/processed/models.json`, fitted estimators in `data/processed/models/<id>.joblib`,
physics expectations and limits in `docs/models.md`.
"""
import json
import math
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from fif import psi

PROCESSED = psi.PROCESSED
N_NEAREST = 5


def wilson(k, n, z=1.96):
    """Wilson score interval for k successes in n trials."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def transform(X, features):
    """Raw inputs (n x features, in the card's units) to the model's feature space."""
    X = np.asarray(X, dtype=float).copy()
    for j, f in enumerate(features):
        if f["transform"] == "log10":
            X[:, j] = np.log10(X[:, j])
    return X


@lru_cache(maxsize=4)
def _cards(path):
    return {m["id"]: m for m in json.loads(Path(path).read_text())["models"]}


@lru_cache(maxsize=32)
def _bundle(path):
    return joblib.load(path)


def cards():
    return _cards(str(PROCESSED / "models.json"))


def bundle(model_id):
    return _bundle(str(PROCESSED / "models" / f"{model_id}.joblib"))


def _inputs(card, conditions):
    names = [f["name"] for f in card["features"]]
    missing = [n for n in names if n not in conditions]
    unknown = [n for n in conditions if n not in names]
    if missing or unknown:
        raise ValueError(f"{card['id']} needs exactly {names}; missing {missing}, unknown {unknown}")
    x = np.array([[float(conditions[n]) for n in names]])
    problems = []
    for f, v in zip(card["features"], x[0]):
        if not math.isfinite(v):
            problems.append(f"{f['name']} is not a number")
        elif f.get("allowed") and v not in f["allowed"]:
            problems.append(f"{f['name']} must be one of {f['allowed']}, not {v:g}")
    parts = (card.get("constraints") or {}).get("sum_at_most_one")
    if parts:
        total = sum(float(conditions[n]) for n in parts)
        if total > 1 + 1e-9:
            problems.append(f"{' + '.join(parts)} = {total:.3g}: mole fractions cannot sum to more than 1")
    if problems:
        raise ValueError(f"{card['id']}: impossible conditions: " + "; ".join(problems))
    return x


def _outside(card, x):
    out = {}
    for f, v in zip(card["features"], x[0]):
        lo, hi = f["domain"]
        if not lo <= v <= hi:
            out[f["name"]] = {"value": float(v), "min": lo, "max": hi}
        for gap in f.get("untested") or []:
            glo, ghi = gap["range"]
            if glo <= v <= ghi:
                out[f["name"]] = {"value": float(v), "min": lo, "max": hi, "untested": [glo, ghi],
                                  "reason": f"only {gap['n_tests']} training tests between {glo:g} and {ghi:g}"}
    return out


def _nearest(card, b, x):
    feats = card["features"]
    Z = transform(b["X"], feats)
    z = transform(x, feats)
    scale = Z.std(axis=0)
    scale[scale == 0] = 1.0
    dist = np.sqrt((((Z - z) / scale) ** 2).sum(axis=1))
    order = np.argsort(dist, kind="stable")[:N_NEAREST]
    return [
        {
            "test_id": b["test_ids"][i],
            "distance": round(float(dist[i]), 3),
            card["target"]: b["y"][i].item(),
            **{f["name"]: float(b["X"][i, j]) for j, f in enumerate(feats)},
        }
        for i in order
    ]


def predict(model_id, *, allow_extrapolation=False, **conditions):
    """Predict one model's target for one set of conditions.

    Outside the training domain (a feature beyond its training range, or inside a range the card lists as
    untested) the prediction is None unless `allow_extrapolation`; `outside_domain` always names the offending
    features. Impossible conditions (mole fractions summing over 1, a value an indicator cannot take) raise. `nearest_tests` lists the most
    similar real tests (standardised distance in the model's feature space).
    """
    card = cards()[model_id]
    x = _inputs(card, conditions)
    b = bundle(model_id)
    outside = _outside(card, x)
    out = {
        "model_id": model_id,
        "accession": card["accession"],
        "target": card["target"],
        "kind": card["kind"],
        "use": card["use"],
        "in_domain": not outside,
        "outside_domain": outside,
        "n_train": card["n"],
        "cv_metric": card["cv_metric"],
        "prediction": None,
        "nearest_tests": _nearest(card, b, x),
    }
    if card["use"] == "descriptive":
        out["note"] = "descriptive only: no held-out skill or too few rows; see the card's table and caveats"
        if "descriptive_table" in card:
            out["observed"] = card["descriptive_table"]
        return out
    if outside and not allow_extrapolation:
        return out
    z = transform(x, card["features"])
    if card["kind"] == "classifier":
        p = float(b["estimator"].predict_proba(z)[0, 1])
        out["probability"] = p
        out["prediction"] = p >= 0.5
    else:
        y = float(b["estimator"].predict(z)[0])
        lo, hi = card["prediction_interval"]["residual_quantiles"]
        if card.get("target_transform") == "log10":
            y, lo, hi = 10 ** y, 10 ** (y + lo) - 10 ** y, 10 ** (y + hi) - 10 ** y
        out["prediction"] = y
        out["interval"] = [y + lo, y + hi]
    return out
