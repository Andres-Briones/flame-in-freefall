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


def test_a_file_label_names_no_page_and_the_page_stays_in_the_locator():
    file = "data/raw/files/PSI-25/BASS-II Summary Report.pdf"
    a, b = (api._link({"accession": "PSI-25", "file": file, "locator": loc}) for loc in ("p101", "p96"))
    assert a["label"] == b["label"] == "BASS-II (PSI-25): BASS-II Summary Report.pdf"
    assert (a["locator"], b["locator"]) == ("p101", "p96")
    for s in api.find_evidence("cool flame", k=5)["sources"]:
        if s.get("file") and s.get("locator"):
            assert s["label"].endswith(f": {s['file'].rsplit('/', 1)[-1]}"), s


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


def test_corrections_links_land_on_a_section_and_the_page_lists_every_changed_value():
    docs_pages = pytest.importorskip("demo.docs_pages")
    page = docs_pages.render(notes.CORRECTIONS_KEY)
    anchors = set()
    for acc in api.records():
        url = next(s["url"] for s in api.discrepancies(acc)["sources"] if "/docs/corrections" in s["url"])
        _, _, anchor = url.partition("#")
        assert not anchor or f'id="{anchor}"' in page, url
        anchors.add(anchor)
    assert {"PSI-10", "PSI-26", "PSI-25"} <= anchors and "" in anchors
    values = page.split('id="values-changed"', 1)[1]
    changed = api.discrepancies()["data"]["values_changed"]
    assert changed and values.count("<tr") - 1 == len(changed)
    assert "<td>PSI-26</td><td>85</td><td>x_o2_ambient</td><td>0.21111</td><td>0.168</td>" in values


@pytest.mark.parametrize("path", ["/docs/nope", "/docs/digest/BRIEF", "/docs/review-game-claims", "/docs/../README.md",
                                  "/docs/%2e%2e/README.md", "/docs/..%2fpyproject.toml", "/docs/digest/../../README.md",
                                  "/docs//etc/passwd", "/docs/question-bank/../../pyproject.toml"])
def test_unknown_names_and_traversal_are_404(client, path):
    r = client.get(path)
    assert r.status_code == 404
    assert "[project]" not in r.text and "root:" not in r.text


@pytest.mark.parametrize("public_url, docs", [("http://www.open-poker.ch:5187", "/docs"),
                                              ("https://example.org/fuego", "/fuego/docs"),
                                              ("https://example.org/fuego/", "/fuego/docs")])
def test_links_inside_notes_keep_the_path_of_the_public_address(monkeypatch, public_url, docs):
    docs_pages = pytest.importorskip("demo.docs_pages")
    monkeypatch.setattr(notes, "PUBLIC_URL", public_url.rstrip("/"))
    docs_pages.render.cache_clear()
    try:
        pages = {key: docs_pages.render(key) for key in [None, "digest/PSI-25", "digest/synthesis", "corrections"]}
    finally:
        docs_pages.render.cache_clear()
    for key, page in pages.items():
        local = [h for h in re.findall(r'href="([^"]*)"', page) if not re.match(r"(https?:|mailto:|#)", h)]
        assert local, key
        for href in local:
            assert href == docs or href.startswith(f"{docs}/"), (key, href)
    assert f'href="{docs}"' in pages["digest/PSI-25"]
    assert f'href="{docs}/digest/PSI-26"' in pages["digest/PSI-25"]
    assert f'href="{docs}/corrections.json"' in pages["corrections"]


def test_raw_html_in_notes_is_escaped():
    docs_pages = pytest.importorskip("demo.docs_pages")
    html = docs_pages._md().render("x <script>alert(1)</script>")
    assert "<script>" not in html
