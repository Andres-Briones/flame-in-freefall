import json

import pytest

from fif import api, psi, tools

pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "tests.parquet").exists(), reason="processed tables not built")


def test_every_result_is_json_with_the_four_keys():
    calls = [
        api.search_investigations("smoke detector"), api.get_investigation("BASS", sections=["findings"]),
        api.filter_tests(accession="PSI-69", x_o2=[None, 0.15]), api.compare(["PSI-26", "SAFFIRE-II"]),
        api.coverage(), api.relevance("moon-habitat"), api.find_evidence("cool flame", k=3), api.insights("gaps"),
    ]
    for result in calls:
        assert set(result) == {"data", "chart", "sources", "notes"}
        json.dumps(result, allow_nan=False)


def test_accession_accepts_number_acronym_and_rejects_ambiguous():
    assert api._accession("26") == api._accession("bass") == "PSI-26"
    assert api._accession("FLEX") == "PSI-69"
    with pytest.raises(KeyError):
        api._accession("saffire")


def test_filter_tests_ranges_and_default_row_kind():
    rows = api.filter_tests(accession="PSI-25", x_o2=[None, 0.15])["data"]["rows"]
    assert rows and all(r["x_o2_ambient"] <= 0.15 and r["row_kind"] == "test" for r in rows)
    assert api.filter_tests(fuel_phase="solid", x_o2=[0.25, None])["data"]["n_matching"] == 0


def test_coverage_shows_no_solid_tests_at_moon_habitat():
    refs = {r["id"]: r for r in api.coverage(fuel_phase="solid")["data"]["references"]}
    assert refs["moon-habitat"]["n_tests_in_cell"] == 0
    assert refs["earth-sea-level"]["n_tests_in_cell"] > 0


def test_relevance_scores_and_gap_statement():
    cabin = api.relevance("iss-cabin")["data"]
    assert {"PSI-25", "PSI-26"} & {r["accession"] for r in cabin["ranking"][:4]}
    assert all(0 <= r["score"] <= 100 for r in cabin["ranking"])
    moon = api.relevance("moon-habitat")
    assert "gravity" in moon["data"]["weights"]
    assert any(n.startswith("Gap:") for n in moon["notes"]) and any("partial gravity" in n for n in moon["notes"])
    by_acc = {r["accession"]: r for r in moon["data"]["ranking"]}
    assert by_acc["PSI-25"]["distance_to_scenario"] > 3


def test_relevance_custom_scenario_and_pillar():
    out = api.relevance({"x_o2": 0.21, "pressure_kpa": 101.3}, pillar="detection")["data"]["ranking"]
    assert {"PSI-101", "PSI-102"} & {r["accession"] for r in out[:5]}


def test_find_evidence_cites_findings():
    hit = api.find_evidence("cool flame radiative extinction droplet", k=5, raw=False)["data"]["digest"]
    assert hit and all(h["ref"].startswith("[PSI-") for h in hit)


def test_tool_specs_match_functions():
    import inspect

    assert {t["name"] for t in tools.TOOLS} == set(api.FUNCTIONS)
    for tool in tools.TOOLS:
        signature = inspect.signature(api.FUNCTIONS[tool["name"]])
        takes_kwargs = any(p.kind is p.VAR_KEYWORD for p in signature.parameters.values())
        for name in tool["input_schema"]["properties"]:
            assert takes_kwargs or name in signature.parameters, (tool["name"], name)


def test_discrepancies_lists_raw_conflicts_changed_values_and_removed_files():
    data = api.discrepancies()["data"]
    assert {c["action"] for c in data["raw_data_conflicts"]} == {"replace", "fill", "flag", "note"}
    assert all(c["evidence"] and c["evidence_source"] for c in data["raw_data_conflicts"])
    assert all(f["meaning"] for f in data["flags"])
    assert data["removed_sources"] and {s["accession"] for s in data["removed_sources"]} == {"PSI-142"}
    one = api.discrepancies(test_id="22024M1")["data"]
    assert [c["id"] for c in one["raw_data_conflicts"]] == ["D01", "D02"]
    assert {v["column"] for v in one["values_changed"]} == {"test_id", "date"}



def test_insights_accession_is_an_exact_match():
    for topic in ("key_messages", "lineage", "gaps"):
        for entry in api.insights(topic, "PSI-10")["data"]:
            assert "PSI-10" in json.dumps(entry).replace("PSI-100", "").replace("PSI-101", "").replace(
                "PSI-102", "").replace("PSI-106", "").replace("PSI-107", "")


def test_fuel_filter_matches_whole_names():
    assert {r["fuel"] for r in api.filter_tests(fuel="ethane", limit=5000)["data"]["rows"]} == {"ethane"}
    heptane = {r["fuel"] for r in api.filter_tests(fuel="heptane", limit=5000)["data"]["rows"]}
    assert "n-heptane" in heptane and heptane <= {"n-heptane", "n-heptane/isooctane"}
    assert "isooctane" not in {r["fuel"] for r in api.filter_tests(fuel="octane", limit=5000)["data"]["rows"]}


def test_coverage_puts_edge_values_in_the_upper_bin():
    assert list(api._bin([0.30, 0.2999, 0.32, 0.21], 0.02)) == [15, 14, 16, 10]
    cells = api.coverage(accession="PSI-69")["data"]["cells"]
    at_30 = api.filter_tests(accession="PSI-69", x_o2=[0.30, 0.30], pressure_kpa=[70, 80])["data"]["n_matching"]
    cell = next(c for c in cells if c["x_min"] == 0.30 and c["y_min"] == 70.0)
    assert at_30 > 0 and cell["n"] >= at_30


def test_relevance_unknown_conditions_never_beat_measured_ones():
    for scenario in api.SCENARIOS:
        ranking = api.relevance(scenario)["data"]["ranking"]
        for key in ("x_o2", "pressure_kpa"):
            steps = [(r["distance_per_dimension"][key], key in r["conditions_unknown"]) for r in ranking]
            unknown, known = [s for s, u in steps if u], [s for s, u in steps if not u]
            assert unknown and min(unknown) >= max(known) and min(unknown) >= api.UNKNOWN_STEPS


def test_relevance_rejects_unknown_choices():
    for kwargs in ({"pillar": "foo"}, {"fuel_phase": "aerosol"}, {"fuel_phase": None}, {"scenario": "venus"}):
        with pytest.raises(ValueError, match="must be one of"):
            api.relevance(**kwargs)


def test_values_changed_lists_originals_kept_under_a_source_column_name():
    changed = {(v["accession"], v["test_id"], v["column"]) for v in api.discrepancies()["data"]["values_changed"]}
    assert {("PSI-26", "100", "x_o2_ambient"), ("PSI-26", "72", "x_o2_ambient"),
            ("PSI-107", "PSI-107-r397", "flow_cm_s")} <= changed


def test_filter_tests_note_separates_remarks_from_doubts():
    note = api.filter_tests(accession="PSI-159")["notes"][0]
    assert "a correction or a doubt" in note and "only a remark" in note


def test_every_investigation_card_carries_its_dataset_doi():
    cards = api.search_investigations()["data"]
    assert len(cards) == 24
    for c in cards:
        assert c["doi"].startswith("10.60555/") and c["doi_url"] == "https://doi.org/" + c["doi"] and c["psi_url"].startswith("https://")
    one = api.get_investigation("PSI-25")["data"]
    assert one["card"]["doi"] == "10.60555/4qc4-de67" and len(one["publication_dois"]) > 0
