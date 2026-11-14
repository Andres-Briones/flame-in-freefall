import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "data" / "export"


def _build_module():
    spec = importlib.util.spec_from_file_location("build_demo", ROOT / "demo" / "build_demo.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read(path):
    text = path.read_text()
    return json.loads(text[text.index("=", text.index("window.FIF.")) + 1:].rstrip().rstrip(";"))


def test_demo_build_keeps_every_record(tmp_path, monkeypatch):
    build = _build_module()
    monkeypatch.setattr(build, "DIST", tmp_path)
    sizes = build.build()
    data = {name: _read(tmp_path / "data" / f"{name}.js") for name in build.LAZY}

    assert len(data["tests"]) == len(json.loads((EXPORT / "tests.json").read_text()))
    assert len(data["relevance"]) == 60
    assert len(data["records"]) == 24
    assert len(data["tsfeatures"]) == len(json.loads((EXPORT / "timeseries_features.json").read_text()))
    assert len(data["models"]["models"]) == 8
    assert sum(sizes.values()) < 8e6

    # Trimming drops empty cells only: a test keeps its conditions, flags and original columns.
    source = {(r["accession"], r["test_id"], r["source_row"]): r for r in json.loads((EXPORT / "tests.json").read_text())}
    for row in data["tests"][::97]:
        original = source[(row["accession"], row["test_id"], row["source_row"])]
        for key in ("x_o2_ambient", "x_o2_burner", "pressure_kpa", "flags", "extra", "row_kind"):
            assert row.get(key) == original[key]

    ranking = data["relevance"]["moon-habitat|solid|any"]["data"]["ranking"]
    assert len(ranking) == 24 and {"score", "components", "nearest_test"} <= set(ranking[0])


def test_demo_page_has_every_view(tmp_path, monkeypatch):
    build = _build_module()
    monkeypatch.setattr(build, "DIST", tmp_path)
    build.build()
    page = (tmp_path / "page.html").read_text()
    for view in build.VIEW_ORDER:
        assert f"id: '{view}'" in page, view
    assert "<html" not in page and "<!doctype" not in page.lower()
    assert (tmp_path / "index.html").read_text().lower().startswith("<!doctype html>")
