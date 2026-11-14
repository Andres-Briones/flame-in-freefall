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
    assert body["ok"] is True and "relevance" in body["functions"] and len(body["functions"]) == 11
    assert isinstance(body["raw_on_disk"], bool)


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
