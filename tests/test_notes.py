"""Every source a function returns can be opened (`url`) and named (`label`); our notes are served at /docs/<key>."""
import re

import pytest

from fif import api, notes, psi

pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "tests.parquet").exists(), reason="processed tables not built")


def _model_call():
    card = next(c for c in api.predict()["data"]["models"] if c["id"] == "flex_burning_rate")
    conditions = {f["name"]: f["allowed"][-1] if f.get("allowed") else (f["domain"][0] + f["domain"][1]) / 2
                  for f in card["features"]}
    return api.predict("flex_burning_rate", **conditions)


def _smoke():
    file = api.table("evidence_files").query("accession == 'PSI-25'")["file_name"].iloc[0]
    calls = [
        api.search_investigations("smoke detector"), api.get_investigation("PSI-25"),
        api.filter_tests(accession="PSI-10", limit=5, sheets=True), api.compare(["PSI-26", "PSI-25"]),
        api.coverage(), api.relevance("moon-habitat", fuel_phase="solid"), api.find_evidence("cool flame", k=3),
        api.insights("gaps"), api.insights("key_messages"), api.predict(), _model_call(),
        api.discrepancies(), api.discrepancies("PSI-10"), api.document_text("PSI-25", file),
    ]
    if (psi.PROCESSED / "timeseries_features.parquet").exists() and (psi.RAW / "files" / "PSI-10").is_dir():
        calls.append(api.timeseries("22024M1", max_points=10))
    return calls


@pytest.fixture(scope="module")
def sources():
    return [s for result in _smoke() for s in result["sources"]]


def test_every_source_has_an_absolute_url_and_a_label(sources):
    assert sources
    for s in sources:
        assert re.match(r"https?://", s.get("url") or ""), s
        assert s.get("label"), s


def test_nasa_files_link_to_their_psi_page_and_name_the_file(sources):
    files = [s for s in sources if s.get("accession") and s.get("file")]
    assert files
    for s in files:
        assert s["url"] == f"https://psi.nasa.gov/physci/repo/data/investigations/{s['accession']}"
        assert s["file"].rsplit("/", 1)[-1] in s["label"]


def test_note_sources_point_at_published_pages_and_existing_anchors(sources):
    docs_pages = pytest.importorskip("demo.docs_pages")
    ours = [s for s in sources if s["url"].startswith(f"{notes.PUBLIC_URL}/docs/")]
    assert any("#" in s["url"] for s in ours)
    assert all(s["label"].startswith("Our notes: ") for s in ours)
    for s in ours:
        name, _, anchor = s["url"].removeprefix(f"{notes.PUBLIC_URL}/docs/").partition("#")
        key = docs_pages.resolve(name)
        assert key, s["url"]
        if anchor:
            assert f'id="{anchor}"' in docs_pages.render(key), s["url"]


def test_doi_sources_link_to_doi_org():
    sources = api.get_investigation("PSI-25")["sources"]
    doi = [s for s in sources if s.get("doi")]
    assert doi and doi[0]["url"] == f"https://doi.org/{doi[0]['doi']}"


def test_every_heading_anchor_of_a_page_is_rendered():
    docs_pages = pytest.importorskip("demo.docs_pages")
    for key in notes.pages():
        page = docs_pages.render(key)
        for _, _, anchor in notes.headings(key):
            assert f'id="{anchor}"' in page, (key, anchor)


def test_working_briefs_are_not_published():
    assert "digest/BRIEF" not in notes.pages() and "review-game-claims" not in notes.pages()
    assert {"methods", "models", "formats", "tests-table", "digest/PSI-25", "digest/PSI-60", "digest/synthesis"} <= set(notes.pages())


@pytest.fixture
def client():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from demo import server
    return TestClient(server.app)


@pytest.mark.parametrize("path", ["/docs", "/docs/methods", "/docs/models", "/docs/formats", "/docs/tests-table",
                                  "/docs/digest/PSI-25", "/docs/digest/PSI-25-bass-ii.md", "/docs/digest/synthesis",
                                  "/docs/corrections"])
def test_docs_pages_are_served_as_html(client, path):
    r = client.get(path)
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/html")
    assert "<h1" in r.text


def test_corrections_page_has_an_anchor_per_investigation_and_patch(client):
    page = client.get("/docs/corrections").text
    assert 'id="PSI-10"' in page and 'id="D01"' in page
    assert client.get("/docs/corrections.json").json()[0]["id"]


@pytest.mark.parametrize("path", ["/docs/nope", "/docs/digest/BRIEF", "/docs/review-game-claims", "/docs/../README.md",
                                  "/docs/%2e%2e/README.md", "/docs/..%2fpyproject.toml", "/docs/digest/../../README.md",
                                  "/docs//etc/passwd", "/docs/question-bank/../../pyproject.toml"])
def test_unknown_names_and_traversal_are_404(client, path):
    r = client.get(path)
    assert r.status_code == 404
    assert "[project]" not in r.text and "root:" not in r.text


def test_raw_html_in_notes_is_escaped():
    docs_pages = pytest.importorskip("demo.docs_pages")
    html = docs_pages._md().render("x <script>alert(1)</script>")
    assert "<script>" not in html
