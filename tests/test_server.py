import json

import pytest

from fif import psi

pytest.importorskip("fastapi")
pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "files.csv").exists(), reason="processed tables not built")

from fastapi.testclient import TestClient  # noqa: E402

from demo import server  # noqa: E402

KNOWN = ("PSI-102", "PSI-102_Engineering Documents_60089MFHP0001-C Same Fluids System Schematic.pdf")
S3 = "https://bucket.s3.amazonaws.com/x.pdf?X-Amz-Expires=7200&X-Amz-Signature=abc"


@pytest.fixture
def client():
    return TestClient(server.app)


@pytest.fixture
def fake_psi(monkeypatch):
    """PSI answers every address with the redirect in `answer`; `calls` counts the requests."""
    state = {"answer": (302, S3), "calls": 0}

    def redirect(url):
        state["calls"] += 1
        assert url.startswith("https://psi.nasa.gov/geode-py/ws/studies/")
        return state["answer"]

    monkeypatch.setattr(server, "psi_redirect", redirect)
    monkeypatch.setattr(server, "_resolved", type(server._resolved)())
    return state


def test_health_lists_the_functions(client):
    body = client.get("/api/health").json()
    assert body["ok"] is True and "relevance" in body["functions"] and len(body["functions"]) == 12
    assert isinstance(body["raw_on_disk"], bool)


def test_health_reports_the_data_version(client):
    version = client.get("/api/health").json()["data_version"]
    assert version["commit"] and version["commit_date"]
    assert version["rows"]["investigations"] == len(server.api.table("investigations"))
    assert version["rows"]["evidence_passages"] == len(server.api.table("evidence")) > 0
    assert version["rows"]["tests"] > 0


def test_data_version_prefers_the_build_args_and_survives_a_missing_git(monkeypatch):
    monkeypatch.setenv("FIF_COMMIT", "abc1234")
    monkeypatch.setenv("FIF_COMMIT_DATE", "2026-11-15T10:00:00+00:00")
    assert server._data_version()["commit"] == "abc1234"

    monkeypatch.delenv("FIF_COMMIT")
    monkeypatch.delenv("FIF_COMMIT_DATE")

    def no_git(*args, **kwargs):
        raise FileNotFoundError("git")

    monkeypatch.setattr(server.subprocess, "run", no_git)
    assert server._data_version()["commit"] == "unknown"
    assert server._data_version()["commit_date"] == "unknown"


@pytest.mark.parametrize("args", [
    {"scenario": "moon-habitat"},
    {"scenario": {"x_o2": 0.3, "pressure_kpa": 70, "flow_cm_s": 5, "gravity_g": 0.165}},
])
def test_relevance_call_returns_valid_json(client, args):
    r = client.post("/api/call/relevance", json=args)
    assert r.status_code == 200
    body = json.loads(r.text, parse_constant=lambda c: pytest.fail(f"non-JSON constant {c}"))
    assert set(body) == {"data", "chart", "sources", "notes"} and body["data"]["ranking"]


def test_unknown_function_is_404_and_bad_argument_is_400(client):
    assert client.post("/api/call/os_system", json={}).status_code == 404
    r = client.post("/api/call/relevance", json={"scenario": "atlantis"})
    assert r.status_code == 400 and r.json()["detail"]
    assert client.post("/api/call/relevance", json={"no_such_argument": 1, "fuel_phase": "plasma"}).status_code == 400
    assert client.post("/api/call/relevance", json=[1, 2]).status_code == 400


def test_a_wrong_unit_is_400_with_the_unit_in_the_detail(client):
    r = client.post("/api/call/relevance", json={"scenario": {"x_o2": 34, "pressure_kpa": 57}})
    assert r.status_code == 400 and "mole fraction between 0 and 1: 0.34, not 34" in r.json()["detail"]
    r = client.post("/api/call/relevance", json={"scenario": {"foo": 1}})
    assert r.status_code == 400 and "accepted: x_o2, pressure_kpa" in r.json()["detail"]
    r = client.post("/api/call/filter_tests", json={"x_o2": [30, 40]})
    assert r.status_code == 400 and "0.3, not 30" in r.json()["detail"]


def test_limits_are_capped(client):
    r = client.post("/api/call/filter_tests", json={"limit": 10**9, "row_kind": None})
    assert r.status_code == 200 and len(r.json()["data"]["rows"]) <= 3000


def test_resolve_refuses_files_outside_the_catalogue(client, fake_psi):
    assert client.get("/api/resolve", params={"accession": "PSI-102", "file": "../../etc/passwd"}).status_code == 404
    assert client.get("/api/resolve", params={"accession": "PSI-1", "file": KNOWN[1]}).status_code == 404
    assert fake_psi["calls"] == 0


def test_resolve_refuses_decision_007_files(client, fake_psi):
    for acc, name in server.NOT_INLINE:
        r = client.get("/api/resolve", params={"accession": acc, "file": name})
        assert r.status_code == 403 and r.json()["detail"] == server.NOT_INLINE_DETAIL
    assert fake_psi["calls"] == 0


def test_document_text_returns_no_text_for_files_not_shown_inline(client):
    for acc, name in server.NOT_INLINE:
        for args in ({}, {"page": 1}):
            r = client.post("/api/call/document_text", json={"accession": acc, "file": name, **args})
            if r.status_code == 400:  # not an extracted file of its own (PSI-142's cover page sits inside an archive)
                continue
            assert r.json()["data"]["pages"] == [] and not r.json()["data"].get("passages"), name
    r = client.post("/api/call/document_text", json={"accession": "PSI-10", "file": "nope.pdf"})
    assert r.status_code == 400


def test_resolve_returns_the_storage_address_and_caches_it(client, fake_psi):
    params = {"accession": KNOWN[0], "file": KNOWN[1]}
    first = client.get("/api/resolve", params=params).json()
    assert first["url"] == S3 and 0 < first["expires_in_s"] <= 7200
    assert client.get("/api/resolve", params=params).json()["url"] == S3
    assert fake_psi["calls"] == 1


def test_resolve_rejects_other_hosts_and_reports_psi_404(client, fake_psi):
    params = {"accession": KNOWN[0], "file": KNOWN[1]}
    fake_psi["answer"] = (302, "https://evil.example.com/amazonaws.com/x.pdf")
    assert client.get("/api/resolve", params=params).status_code == 502
    fake_psi["answer"] = (404, None)
    r = client.get("/api/resolve", params=params)
    assert r.status_code == 404 and r.json()["detail"] == "PSI no longer serves this file"


def test_raw_cache_evicts_only_files_it_downloaded(tmp_path):
    def fetch(acc, name, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"x" * 600)

    own = tmp_path / "files" / "own.csv"
    own.parent.mkdir(parents=True)
    own.write_bytes(b"y" * 5000)
    cache = server.RawCache(tmp_path, cap_bytes=1000, fetch=fetch)
    a, b = tmp_path / "files" / "a.csv", tmp_path / "files" / "b.csv"
    cache.ensure("PSI-1", "a.csv", a, 600)
    cache.ensure("PSI-1", "own.csv", own, 5000)
    cache.ensure("PSI-1", "b.csv", b, 600)
    assert own.exists() and b.exists() and not a.exists()
    with pytest.raises(ValueError):
        cache.ensure("PSI-1", "huge.csv", tmp_path / "huge.csv", 200 * 2**20)
    assert server.RawCache(tmp_path, cap_bytes=0, fetch=fetch).owned == {str(b): 600}


def test_timeseries_needs_the_cfi_chamber_file_too():
    feats = server.api.table("timeseries_features")
    point = feats.loc[feats["accession"] == "PSI-39", "test_point"].iloc[0]
    names = [name for _, name in server.timeseries_files(point)]
    assert any("_Radiometer_Readings" in n for n in names) and any("_Chamber_Readings" in n for n in names)


def test_get_call_reads_typed_arguments_from_the_query(client):
    posted = client.post("/api/call/filter_tests", json={"accession": "PSI-25", "x_o2": [0.18, 0.21], "limit": 5}).json()
    fetched = client.get("/api/call/filter_tests", params={"accession": "PSI-25", "x_o2": "[0.18,0.21]", "limit": "5"})
    assert fetched.status_code == 200 and fetched.json() == posted
    as_json = client.get("/api/call/filter_tests", params={"args": json.dumps({"accession": "PSI-25", "x_o2": [0.18, 0.21], "limit": 5})})
    assert as_json.json() == posted
    assert client.get("/api/call/filter_tests", params={"limit": "many"}).status_code == 400
    assert client.get("/api/call/nope").status_code == 404


def test_guide_tools_and_openapi_cover_every_function(client):
    text = client.get("/llms.txt").text
    spec = client.get("/openapi.json").json()
    listed = {t["name"] for t in client.get("/api/tools").json()["tools"]}
    assert listed == set(server.api.FUNCTIONS)
    for name in server.api.FUNCTIONS:
        assert f"### {name}" in text and f"/api/call/{name}" in spec["paths"]
    assert "http://testserver/api/call/" in text


def test_discrepancies_compact_fits_under_the_mcp_result_limit(client):
    short = client.get("/api/call/discrepancies", params={"compact": "true"}).json()
    full = client.post("/api/call/discrepancies", json={}).json()
    assert len(json.dumps(short)) < 40000 and len(json.dumps(full)) > 60000
    assert len(short["data"]["raw_data_conflicts"]) == len(full["data"]["raw_data_conflicts"])


def test_every_guide_example_runs(client):
    for tool in server.TOOLS:
        if tool["name"] == "timeseries":  # needs raw files
            continue
        r = client.post(f"/api/call/{tool['name']}", json=server._example(tool))
        assert r.status_code == 200, (tool["name"], r.text[:200])


def test_mcp_lists_and_calls_tools(client):
    def rpc(method, params=None, id=1):
        return client.post("/mcp", json={"jsonrpc": "2.0", "id": id, "method": method, "params": params or {}}).json()

    init = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}})
    assert init["result"]["protocolVersion"] == "2025-03-26" and "tools" in init["result"]["capabilities"]
    assert client.post("/mcp", json={"jsonrpc": "2.0", "method": "notifications/initialized"}).status_code == 202
    assert {t["name"] for t in rpc("tools/list")["result"]["tools"]} == set(server.ALL_FUNCTIONS)
    ok = rpc("tools/call", {"name": "coverage", "arguments": {}})["result"]
    assert not ok.get("isError") and set(json.loads(ok["content"][0]["text"])) >= {"data", "sources", "notes"}
    bad = rpc("tools/call", {"name": "filter_tests", "arguments": {"limit": -1}})["result"]
    assert bad["isError"] and "limit" in bad["content"][0]["text"]
    assert "error" in rpc("nope")


def test_timeseries_fetches_every_reduced_file_of_a_cfi_test():
    names = [name for _, name in server.timeseries_files("1264", test_point="FLEX-1264-reduced")]
    assert sorted(n.split("_")[-1] for n in names) == ["ColorCamData.txt", "CoolFlameData.txt", "DropletData.txt", "RadiometerData.txt"]
