"""Build the static dashboard demo from data/export/ into demo/dist/.

    uv run python demo/build_demo.py

dist/index.html opens from disk; dist/page.html is the same page without the document wrapper (artifact publish).
Data go to dist/data/*.js as `window.FIF.<name> = ...` so no fetch is needed under file://.
"""
import csv
import json
from pathlib import Path

DEMO = Path(__file__).resolve().parent
ROOT = DEMO.parent
EXPORT = ROOT / "data" / "export"
SRC = DEMO / "src"
DIST = DEMO / "dist"

VIEW_ORDER = ["overview", "scenario", "coverage", "tests", "investigation", "files", "insights", "quality", "models",
              "traces", "search", "ask", "ai", "board", "pipeline", "brief"]
BASE = ["investigations", "synthesis", "coverage", "questions", "discrepancies"]
LAZY = ["relevance", "tests", "records", "models", "tsfeatures", "tsexamples", "files"]

TS_KEEP = [
    "accession", "test_id", "test_point", "duration_s", "sample_hz", "fuel_gas", "oxidizer_gas", "inert_gas",
    "flame_detected", "ignition_time_s", "flameout_time_s", "burn_duration_s", "chamber_pressure_start_kpa",
    "chamber_pressure_max_kpa", "burner_temp_max_c", "rake_a_temp_max_c", "rake_b_temp_max_c", "rake_c_temp_max_c",
    "rake_d_temp_max_c", "chamber_gas_temp_max_c", "oxidizer_flow_mean_burn_slpm", "inert_flow_mean_burn_slpm",
    "fuel_flow_mean_burn_slpm", "radiometer_offset_peak_w_cm2", "pmt1_310nm_max_burn_v", "o2_start_pct",
    "o2_min_pct", "co2_max_pct", "anemometer_start_cm_s", "plume_temp_max_c", "sample_temp_max_c", "droplet_diameter_first_mm",
    "flame_diameter_max_mm", "hot_flame_last_s", "cool_flame_fwhm_max_mm", "cool_flame_last_s", "features_note",
]
RANK_DROP = ("one_line", "pillars", "fuel_phases", "acronym", "platform_kind")
# Where-it-ran fields (location, platform_kind, setting) are for the API and the AI assistant; the demo views do not
# show them, so they are left out to keep the page under its size budget.
TEST_DROP = ("platform_kind",)


def load(name):
    return json.loads((EXPORT / f"{name}.json").read_text())


def compact(row):
    return {k: v for k, v in row.items() if v is not None and v != ""}


def slim(value):
    return {k: v for k, v in value.items() if v is not None and v != []} if isinstance(value, dict) else value


def trimmed():
    out = {name: load(name) for name in BASE + ["records", "models"]}
    for item in [*out["investigations"], *out["records"].values()]:
        item.pop("location", None)
    out["tests"] = [compact({**{k: v for k, v in r.items() if k not in TEST_DROP},
                             "source_file": (r.get("source_file") or "").replace("data/raw/files/", "")})
                    for r in load("tests")]
    out["tsfeatures"] = [compact({k: r.get(k) for k in TS_KEEP}) for r in load("timeseries_features")]
    out["tsexamples"] = load("timeseries_examples")
    rel = load("relevance")
    for entry in rel.values():
        entry.pop("sources", None)
        # empty lists and dicts (no assumption to show) are left out: the view reads them as absent
        entry["data"]["ranking"] = [{k: slim(v) for k, v in r.items() if k not in RANK_DROP and v not in ([], {})}
                                    for r in entry["data"]["ranking"]]
        for key in ("gap", "closest_same_phase_test"):
            if entry["data"].get(key):
                entry["data"][key].pop("setting", None)
        entry["notes"] = [n for n in entry["notes"] if not n.startswith("Setting of the closest")]
    out["relevance"] = rel
    out["files"] = file_catalogue()
    return out


def file_catalogue():
    """Every PSI file as {accession: {category: [[file_name, size_bytes], ...]}}; the page links to PSI, not to us."""
    out = {}
    with open(ROOT / "data" / "processed" / "files.csv", newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["accession"], {}).setdefault(r["category"], []).append(
                [r["file_name"], int(float(r["size_bytes"] or 0))])
    return out


def js(name, value):
    return f"window.FIF=window.FIF||{{}};window.FIF.{name}=" + json.dumps(value, separators=(",", ":")) + ";\n"


def page():
    views = [SRC / "views" / f"{v}.js" for v in VIEW_ORDER]
    scripts = [SRC / "core.js", SRC / "viewer.js"] + [v for v in views if v.exists()] + [SRC / "boot.js"]
    scripts = [p for p in scripts if p.exists()]
    body = (SRC / "shell.html").read_text()
    body = body.replace("/*CSS*/", (SRC / "app.css").read_text())
    return body.replace("/*JS*/", "\n".join(f"// ---- {p.name}\n{p.read_text()}" for p in scripts))


def build():
    data = trimmed()
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    (DIST / "data" / "base.js").write_text("".join(js(n, data[n]) for n in BASE))
    for name in LAZY:
        (DIST / "data" / f"{name}.js").write_text(js(name, data[name]))
    html = page()
    (DIST / "page.html").write_text(html)
    (DIST / "index.html").write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1"></head><body>\n'
        + html + "\n</body></html>\n")
    return {p.name: p.stat().st_size for p in sorted((DIST / "data").iterdir())} | {
        "page.html": (DIST / "page.html").stat().st_size}


if __name__ == "__main__":
    for name, size in build().items():
        print(f"{size / 1e6:6.2f} MB  {name}")
