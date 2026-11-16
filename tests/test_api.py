import json
import math
import re

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


def test_filter_tests_one_test_by_id_and_sorted_extremes():
    one = api.filter_tests(accession="PSI-39", test_id="1246")
    assert one["data"]["n_matching"] == 1 and len(json.dumps(one)) < 3000
    row = one["data"]["rows"][0]
    assert (row["fuel"], row["d0_mm"], row["burn_rate_k_mm2_s"], row["cool_flame"]) == ("n-dodecane", 4.378, 0.356, True)
    assert api.filter_tests(accession="CFI", test_id=["12 46", 1247])["data"]["n_matching"] == 2
    assert api.filter_tests(accession="PSI-98", test_id="s1")["data"]["rows"][0]["test_id"] == "S1"
    low = [r["x_o2_ambient"] for r in api.filter_tests(fuel="pmma", sort_by="x_o2_ambient", limit=3)["data"]["rows"]]
    assert low[0] == 0.136 and low == sorted(low)
    every = api.filter_tests(fuel="pmma", limit=5000)["data"]
    o2 = [r.get("x_o2_ambient") for r in every["rows"]]
    high = api.filter_tests(fuel="pmma", sort_by="-x_o2_ambient", limit=5000)["data"]["rows"]
    assert high[0]["x_o2_ambient"] == max(v for v in o2 if v is not None) and len(high) == every["n_matching"]
    if None in o2:
        assert high[-1].get("x_o2_ambient") is None
    with pytest.raises(ValueError, match="x_o2_ambient"):
        api.filter_tests(sort_by="oxygen")


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


def test_relevance_gap_is_given_as_fields_that_match_the_note():
    moon = api.relevance("moon-habitat")
    gap, note = moon["data"]["gap"], next(n for n in moon["notes"] if n.startswith("Gap:"))
    assert gap["fuel_phase"] == "solid" and gap["distance_to_scenario"] > 1
    assert f"is {gap['accession']} {gap['test_id']} ({gap['fuel']}, O2 {gap['x_o2_ambient']:.3f}" in note
    assert f"{gap['pressure_kpa']:.0f} kPa" in note and f"{gap['distance_to_scenario']} scale steps away" in note
    assert gap["accession"] == moon["data"]["closest_same_phase"]
    for scenario in api.SCENARIOS:
        for phase in api.TRANSFER:
            out = api.relevance(scenario, fuel_phase=phase)
            assert (out["data"]["gap"] is None) == (not any(n.startswith("Gap:") for n in out["notes"]))


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


def test_discrepancies_compact_lists_every_entry_in_a_short_result():
    full, short = api.discrepancies(), api.discrepancies(compact=True)
    assert full == api.discrepancies(compact=False) and "evidence" in full["data"]["raw_data_conflicts"][0]
    for section in ("raw_data_conflicts", "values_changed", "removed_sources", "source_disagreements"):
        assert len(short["data"][section]) == len(full["data"][section]) > 0, section
    assert [c["id"] for c in short["data"]["raw_data_conflicts"]] == [c["id"] for c in full["data"]["raw_data_conflicts"]]
    for key in ("flags", "rows_flagged", "rows_total", "actions"):
        assert short["data"][key] == full["data"][key]
    assert not any("evidence" in c for c in short["data"]["raw_data_conflicts"])
    assert not any("quote" in d or "claim" in d for d in short["data"]["source_disagreements"])
    assert len(json.dumps(short)) < 40000 < len(json.dumps(full))
    assert any("Compact form" in n for n in short["notes"]) and not any("Compact form" in n for n in full["notes"])
    one = api.discrepancies("PSI-69", compact=True)["data"]
    assert one["source_disagreements"] and {d["accession"] for d in one["source_disagreements"]} == {"PSI-69"}
    assert len(one["raw_data_conflicts"]) == len(api.discrepancies("PSI-69")["data"]["raw_data_conflicts"])


@pytest.mark.parametrize("compact", [False, True])
def test_discrepancies_offers_each_disagreeing_paper_once_as_a_source(compact):
    full = api.discrepancies()["data"]["source_disagreements"]
    sources = api.discrepancies(compact=compact)["sources"]
    papers = [s for s in sources if s["url"] in {d["read_url"] for d in full}]
    assert sorted((s["accession"], s["url"]) for s in papers) == sorted({(d["accession"], d["read_url"]) for d in full})
    assert all(s["label"].endswith(next(d["publication"] for d in full if d["read_url"] == s["url"])) for s in papers)
    two_places = "https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf"
    paper = [s for s in api.discrepancies("PSI-69")["sources"] if s["url"] == two_places]
    assert len(paper) == 1 and paper[0]["locator"] == "Extinction Diameter, p4; Fig. 3 caption | Results and Discussion, p2"
    assert not api.discrepancies("PSI-10")["data"]["source_disagreements"]
    assert not {s["url"] for s in api.discrepancies("PSI-10")["sources"]} & {d["read_url"] for d in full}



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


def test_filter_tests_says_which_rows_a_range_left_out_for_having_no_value():
    out = api.filter_tests(fuel_phase="solid", pressure_kpa=[95, 105], limit=5000)
    note = next(n for n in out["notes"] if "no recorded pressure_kpa" in n)
    assert "247 more rows" in note and "PSI-99 SAFFIRE-II 9" in note and "include_unrecorded=true" in note
    assert "PSI-99" not in {r["accession"] for r in out["data"]["rows"]}
    kept = api.filter_tests(fuel_phase="solid", pressure_kpa=[95, 105], include_unrecorded=True, limit=5000)
    assert kept["data"]["n_matching"] == out["data"]["n_matching"] + 247
    assert "PSI-99" in {r["accession"] for r in kept["data"]["rows"]}
    assert any("kept because include_unrecorded" in n for n in kept["notes"])
    assert any("no recorded pressure_kpa" in n for n in api.coverage(fuel_phase="solid", pressure_kpa=[95, 105])["notes"])


def _ranged(out):
    return next((n for n in out["notes"] if n.startswith("Investigations with no matching row")), None)


def test_a_range_filter_names_investigations_whose_conditions_are_only_stated_as_ranges(monkeypatch):
    # ACME BRE kept steady flames at 26.5, 34 and 40 % O2 (test-day rows); FLEX-2 lists 0.17-0.30 O2 and
    # 0.5-3 atm as condition sets only; neither has a single-test row with these values.
    for tool in (api.filter_tests, api.coverage):
        note = _ranged(tool(x_o2=[0.30, None]))
        assert "PSI-20 ACME BRE: x_o2_ambient 0.21-0.4." in note and "PSI-68 FLEX-2: x_o2_ambient 0.14-0.3" in note
        assert "PSI-10 " not in note and "PSI-69 " not in note  # their test rows are returned
    note = _ranged(api.filter_tests(pressure_kpa=[None, 70]))
    assert "PSI-20 ACME BRE: pressure_kpa 56-100" in note and "PSI-68 FLEX-2: pressure_kpa 50.7-304" in note
    assert "get_investigation" in note and "PSI-39" not in note
    assert _ranged(api.filter_tests(x_o2=[0.30, None], fuel_phase="solid")) is None
    assert "PSI-68" not in _ranged(api.filter_tests(x_o2=[0.30, None], fuel="ethylene"))
    assert _ranged(api.filter_tests(x_o2=[0.30, None], accession="PSI-10")) is None
    for call in ({"fuel_phase": "gas"}, {"accession": "PSI-20", "row_kind": None}, {}):
        assert _ranged(api.filter_tests(**call)) is None
        assert _ranged(api.coverage(**call)) is None
    calls = ({"x_o2": [0.30, None]}, {"pressure_kpa": [None, 70], "fuel_phase": "liquid"}, {"fuel_phase": "solid"})
    before = [api.filter_tests(limit=5000, **c)["data"] for c in calls] + [api.coverage(**c)["data"] for c in calls]
    monkeypatch.setattr(api, "_ranged_note", lambda filters, df: None)
    assert before == [api.filter_tests(limit=5000, **c)["data"] for c in calls] + [api.coverage(**c)["data"] for c in calls]


def test_filter_tests_reads_everyday_fuel_names_and_lists_the_real_ones():
    assert sorted(api.table("tests")["fuel"].dropna().unique()) == list(tools.FUELS)
    for alias, (names, _) in api.FUEL_ALIASES.items():
        assert set(names) <= set(tools.FUELS), alias
        assert not api._fuel_mask(api.table("tests")["fuel"], alias).any(), f"{alias} matches a fuel: never used"
    cotton = api.filter_tests(fuel="cotton", limit=5000)
    assert {r["fuel"] for r in cotton["data"]["rows"]} == {"sibal fabric", "lampwick"}
    assert any("named 'cotton'; read as 'sibal fabric' and 'lampwick'" in n for n in cotton["notes"])
    assert api.filter_tests(fuel="Nomex III")["data"]["n_matching"] == api.filter_tests(fuel="nomex")["data"]["n_matching"]
    paper = api.filter_tests(fuel="paper")
    assert paper["data"]["n_matching"] == 0 and any("Fuel names in the table: arizona road dust" in n for n in paper["notes"])


def test_an_empty_filter_result_always_says_why():
    for filters in ({"fuel": "kapton", "x_o2": [0.20, 0.22]}, {"fuel_phase": "solid", "x_o2": [0.25, None]},
                    {"accession": "PSI-39", "test_id": "99999"}, {"fuel": "paper"}, {"fuel": "cotton", "x_o2": [0.3, 0.4]}):
        out = api.filter_tests(**filters)
        assert out["data"]["n_matching"] == 0
        assert any(n.startswith("No row matches all these filters together") for n in out["notes"]), filters
    why = next(n for n in api.filter_tests(accession="PSI-39", test_id="99999")["notes"] if n.startswith("No row"))
    assert "without test_id: 227" in why


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


def test_relevance_nearest_test_is_of_the_requested_phase():
    for phase in api.TRANSFER:
        for row in api.relevance({"x_o2": 0.30, "pressure_kpa": 70.3}, fuel_phase=phase)["data"]["ranking"]:
            near, other = row["nearest_test"], row["nearest_test_other_phase"]
            assert near is None or (near["fuel_phase"] == phase and row["phase_match"] and other is None)
            assert other is None or other["fuel_phase"] != phase
            assert row["phase_match"] == (phase in row["fuel_phases"])


def test_relevance_lists_other_phases_after_the_requested_one():
    out = api.relevance({"x_o2": 0.30, "pressure_kpa": 70.3}, fuel_phase="solid")
    ranking = out["data"]["ranking"]
    assert ranking[0]["phase_match"] and ranking[0]["nearest_test"]["fuel_phase"] == "solid"
    flex = next(r for r in ranking if r["accession"] == "PSI-69")
    assert not flex["phase_match"] and flex["nearest_test"] is None and flex["score"] == max(r["score"] for r in ranking)
    assert flex["nearest_test_other_phase"]["fuel_phase"] == "liquid"
    assert any(n.startswith("Other phases:") and "PSI-69" in n for n in out["notes"])
    closest = out["data"]["closest_same_phase_test"]
    assert closest["fuel_phase"] == "solid" and closest["x_o2_ambient"] < 0.23 and closest["distance_to_scenario"] > 3
    assert closest["accession"] == out["data"]["closest_same_phase"]

    liquid = api.relevance({"x_o2": 0.30, "pressure_kpa": 70.3}, fuel_phase="liquid")
    assert liquid["data"]["ranking"][0]["nearest_test"]["fuel_phase"] == "liquid"
    assert not any(n.startswith("Phase:") for n in liquid["notes"])


def test_relevance_marks_every_condition_not_measured_for_the_nearest_test():
    measured = api.table("tests").set_index(["accession", "test_id"])
    seen = set()
    for scenario in [*api.SCENARIOS, {"x_o2": 0.30, "pressure_kpa": 70.3}]:
        out = api.relevance(scenario)["data"]
        asked = set(out["scenario"]) & set(api.TEST_COLUMN)
        closest = out["closest_same_phase_test"]
        tests = [(r["accession"], r["nearest_test"] or r["nearest_test_other_phase"], r) for r in out["ranking"]]
        for acc, near, row in tests + [(closest["accession"], closest, closest)]:
            marked = set(row.get("conditions_from_range", [])) | set(row.get("conditions_assumed_cabin_air", []))
            if "conditions_unknown" in row:
                assert marked == set(row["condition_ranges"]) and marked | set(row["conditions_unknown"]) <= asked
                assert not set(row["conditions_from_range"]) & set(row["conditions_assumed_cabin_air"])
            if near is None:
                assert marked | set(row["conditions_unknown"]) == asked
                continue
            source = measured.loc[[(acc, near["test_id"])]]
            for key, column in api.TEST_COLUMN.items():
                if column in near["not_measured"]:
                    assert source[column].isna().any()
                    assert near[column] is None or key in row["condition_ranges"]
                    seen.add((acc, key, near[column] is None))
                else:
                    assert near[column] is not None and (source[column] == near[column]).any()
    assert ("PSI-25", "pressure_kpa", False) in seen and ("PSI-99", "pressure_kpa", False) in seen


def test_relevance_gives_the_range_behind_a_midpoint_and_keeps_narrow_ranges_undiscounted():
    out = api.relevance({"x_o2": 0.30, "pressure_kpa": 70.3}, fuel_phase="solid")
    bass2 = next(r for r in out["data"]["ranking"] if r["accession"] == "PSI-25")
    assert bass2["nearest_test"]["not_measured"] == ["pressure_kpa"] and bass2["conditions_from_range"] == ["pressure_kpa"]
    assert bass2["condition_ranges"] == {"pressure_kpa": {
        "min": 99.2, "max": 99.5, "from": "digest", "wide": False, "note": "reported for film tests; about 1 atm overall"}}
    assert bass2["components"]["conditions"] == pytest.approx(math.exp(-bass2["distance_to_scenario"] / 2), abs=0.01)
    wide = next(r for r in out["data"]["ranking"] if r["accession"] == "PSI-20")
    assert all(c["wide"] for c in wide["condition_ranges"].values())
    assert wide["components"]["conditions"] == pytest.approx(
        api.ENVELOPE_DISCOUNT * math.exp(-wide["distance_to_scenario"] / 2), abs=0.01)
    closest = out["data"]["closest_same_phase_test"]
    assert closest["not_measured"] == ["pressure_kpa"]
    assert closest["condition_ranges"]["pressure_kpa"]["from"] == "assumed cabin air"
    assert any(n.startswith("Gap:") and "assumed cabin air" in n for n in out["notes"])


def test_coverage_marks_nearest_tests_placed_from_a_stated_range():
    measured = api.table("tests").set_index(["accession", "test_id"])
    marked = 0
    for phase in (None, "solid"):
        for ref in api.coverage(fuel_phase=phase)["data"]["references"]:
            near = ref["nearest_test"]
            source = measured.loc[[(near["accession"], near["test_id"])]]
            for column in ("x_o2_ambient", "pressure_kpa"):
                assert (column in near["not_measured"]) == bool(source[column].isna().all())
            marked += bool(near["not_measured"])
    assert marked


def test_relevance_rejects_unknown_choices():
    for kwargs in ({"pillar": "foo"}, {"fuel_phase": "aerosol"}, {"fuel_phase": None}, {"scenario": "venus"}):
        with pytest.raises(ValueError, match="must be one of"):
            api.relevance(**kwargs)


def test_relevance_refuses_unknown_conditions_and_wrong_units():
    for scenario, message in (
            ({"x_o2": 34, "pressure_kpa": 57}, "x_o2 is a mole fraction between 0 and 1: 0.34, not 34"),
            ({"foo": 1}, "unknown scenario condition 'foo'; accepted: x_o2, pressure_kpa, flow_cm_s, gravity_g"),
            ({"x_o2": 0.3, "pressure_kpa": -5}, "pressure_kpa is in kPa"),
            ({"x_o2": 0.3, "pressure_kpa": 70300}, "70.3, not 70300 (that is Pa)"),
            ({"x_o2": 0.3, "flow_cm_s": -1}, "flow_cm_s is a speed in cm/s"),
            ({"x_o2": 0.3, "gravity_g": -0.2}, "gravity_g is in Earth gravities"),
            ({"x_o2": "0.3"}, "x_o2 must be a number"),
            ({"gravity_g": 0.165}, "needs at least one of x_o2, pressure_kpa, flow_cm_s")):
        with pytest.raises(ValueError, match=re.escape(message)):
            api.relevance(scenario)
    with pytest.raises(ValueError, match="accepted"):
        api.relevance("iss-cabin", fuelphase="solid")
    with pytest.raises(ValueError, match="x_o2 is a mole fraction"):
        api.relevance("iss-cabin", x_o2=21)
    # limits are inclusive and valid calls are unchanged
    assert api.relevance({"x_o2": 1.0, "pressure_kpa": 29.6, "gravity_g": 0})["data"]["ranking"]
    named = api.relevance("moon-habitat")["data"]["ranking"]
    same = api.relevance({"x_o2": 0.30, "pressure_kpa": 70.3, "gravity_g": 0.165, "label": "x"})["data"]["ranking"]
    assert [(r["accession"], r["score"]) for r in named] == [(r["accession"], r["score"]) for r in same]


def test_filter_tests_refuses_oxygen_in_percent():
    for bounds in ([30, 40], [None, 21], 21, [-0.1, 0.2]):
        with pytest.raises(ValueError, match="x_o2 is a mole fraction between 0 and 1"):
            api.filter_tests(x_o2=bounds)
    with pytest.raises(ValueError, match="0.3, not 30"):
        api.coverage(x_o2=[30, None])
    assert api.filter_tests(x_o2=[0.30, 0.40])["data"]["n_matching"] > 0
    assert api.filter_tests(x_o2=[0, 1])["data"]["n_matching"] == api.filter_tests()["data"]["n_matching"] - int(
        api.table("tests").query("row_kind == 'test'")["x_o2_ambient"].isna().sum())
    # pressure and flow keep any bound: a wrong unit there can still be a real value
    assert api.filter_tests(pressure_kpa=[-10, 50])["data"]["n_matching"] > 0


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


def test_get_investigation_notes_how_many_test_rows_carry_a_doubt():
    for sections in (None, ["findings"]):
        out = api.get_investigation("SAFFIRE-I", sections=sections)
        note = next(n for n in out["notes"] if "carry a correction or a doubt" in n)
        assert note.startswith("2 of 2 rows") and "conflicts_with_raw 2" in note
        assert 'discrepancies(accession="PSI-98")' in note
    assert not any("correction or a doubt" in n for n in api.get_investigation("PSI-102", sections=["findings"])["notes"])


def test_get_investigation_lists_every_publication_of_the_record():
    pubs = api.get_investigation("PSI-25")["data"]["publications"]
    assert len(pubs) == 17 and all(p["title"] for p in pubs)
    with_doi = [p for p in pubs if p["doi"]]
    assert with_doi and all(p["doi_url"] == "https://doi.org/" + p["doi"] for p in with_doi)
    assert all(p["doi_url"] is None for p in pubs if not p["doi"])
    held = {p["held_file"] for p in api.get_investigation("PSI-107")["data"]["publications"]} - {None}
    assert held == {"PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf"}
    assert all(p["held_file"] is None for p in api.get_investigation("PSI-10")["data"]["publications"])


def test_predict_compact_list_is_small_and_enough_to_call_a_model():

    full, short = api.predict()["data"], api.predict(compact=True)
    assert [m["id"] for m in short["data"]["models"]] == [m["id"] for m in full["models"]]
    assert len(json.dumps(short)) < 12000 < len(json.dumps(full))
    for card, m in zip(full["models"], short["data"]["models"]):
        assert [i["name"] for i in m["inputs"]] == [f["name"] for f in card["features"]]
        assert m["use"] == card["use"] and m["accuracy"]["metric"] == card["cv_metric"]["name"]
    assert any(i["untested"] for m in short["data"]["models"] for i in m["inputs"])


def test_predict_from_a_sentence_names_the_fuel_and_assumes_absent_diluents_with_a_note():
    explicit = api.predict(model_id="flex_burning_rate", is_heptane=1, x_o2_ambient=0.21, x_co2=0, x_he=0,
                           pressure_kpa=101.3, d0_mm=3)
    told = api.predict(model_id="flex_burning_rate", fuel="n-heptane", x_o2_ambient=0.21, pressure_kpa=101.3, d0_mm=3)
    assert told["data"] == explicit["data"] and round(told["data"]["prediction"], 2) == 0.52
    assert "fuel 'n-heptane' read as is_heptane = 1." in told["notes"]
    assert any(n.startswith("x_co2 and x_he taken as 0") for n in told["notes"])
    assert not any("taken as 0" in n or "read as" in n for n in explicit["notes"])
    outside = api.predict(model_id="flex_burning_rate", fuel="methanol", x_o2_ambient=0.5, pressure_kpa=101.3, d0_mm=3)
    assert outside["data"]["prediction"] is None and "x_o2_ambient" in outside["data"]["outside_domain"]
    assert "n_carbon = 3" in api.predict(model_id="cfig_inverse_self_extinction", fuel="propane", pressure_kpa=101,
                                         x_o2_burner=0.5, o2_flow_mg_s=3)["notes"][1]
    for bad in ({"model_id": "flex_burning_rate", "fuel": "ethanol"}, {"model_id": "spice_smoke_point_length", "fuel": "ethylene"},
                {"model_id": "flex_burning_rate", "fuel": "methanol", "is_heptane": 1}):
        with pytest.raises(ValueError):
            api.predict(**bad, x_o2_ambient=0.21, pressure_kpa=101.3, d0_mm=3)
    description = next(t for t in tools.TOOLS if t["name"] == "predict")["description"]
    for m in api.predict(compact=True)["data"]["models"]:
        assert f"{m['id']} ({m['accession']}, {m['use']})" in description
        assert all(i["name"] in description for i in m["inputs"])


def test_coverage_references_split_the_cell_count_by_fuel_phase():
    out = api.coverage()
    moon = {r["id"]: r for r in out["data"]["references"]}["moon-habitat"]
    assert moon["n_tests_in_cell"] > 0 and moon["n_tests_in_cell_by_phase"]["solid"] == 0
    assert sum(moon["n_tests_in_cell_by_phase"].values()) <= moon["n_tests_in_cell"]
    assert any("n_tests_in_cell_by_phase" in n for n in out["notes"]) and any("row_kind" in n for n in out["notes"])
    assert sum(c["n_from_stated_range"] for c in out["data"]["cells"]) == 250
    assert not any("n_tests_in_cell_by_phase" in n for n in api.coverage(fuel_phase="solid")["notes"])


def test_every_investigation_card_links_an_existing_digest_page():
    cards = api.search_investigations(limit=50)["data"]
    cards = cards["investigations"] if isinstance(cards, dict) else cards
    assert len(cards) == 24
    for card in cards:
        assert card["page"] and (psi.ROOT / card["page"]).is_file(), card["accession"]


def test_timeseries_serves_reduced_droplet_data_as_a_second_recording():
    feats = api.table("timeseries_features")
    row = feats[feats["test_point"] == "FLEX-1264-reduced"].iloc[0]
    if not psi.raw_file(row["source_file"]).exists():
        pytest.skip("raw data absent")
    first = api.timeseries("1264")
    assert first["data"]["test_point"] == "F139A02" and "-reduced" in first["notes"][0]  # the raw recording stays the default
    out = api.timeseries("1264", test_point="FLEX-1264-reduced", max_points=1500)
    series = out["data"]["series"]
    counts = {c: sum(r.get(c) is not None for r in series) for c in out["chart"]["y"]}
    assert counts["flame_diameter_mm"] == 212  # the short hot-flame curve is not thinned away by the 100 Hz radiometer
    assert counts["droplet_diameter_mm"] > 300 and len(series) <= 1600
    assert not any("wide" in c for c in out["chart"]["y"]) and any("not physical" in n for n in out["notes"])
    assert len([s for s in out["sources"] if s.get("file")]) == 4
    only = api.timeseries("1264", test_point="FLEX-1264-reduced", channels=["droplet_diameter_mm"], max_points=5000)
    assert len(only["data"]["series"]) == 1958 and all(r["droplet_diameter_mm"] is not None for r in only["data"]["series"])


def test_filter_tests_by_the_outcome_read_from_bass_notes():
    rows = api.filter_tests(accession="PSI-25", outcome="extinguished")["data"]["rows"]
    assert len(rows) == 23 and all(r["outcome_quote"] and r["outcome_cause"] for r in rows)
    assert {r["outcome_cause"] for r in rows} == {"blowoff", "low_flow"}
    limits = api.filter_tests(accession=["PSI-25", "PSI-26"], outcome_action="flow_reduced")["data"]["rows"]
    assert len(limits) == 33 and all(r["outcome_cause"] == "low_flow" for r in limits)
    assert sum(r["outcome_setting"] is not None for r in limits) == 25


def test_find_evidence_marks_ai_transcribed_passages(monkeypatch):
    import pandas as pd

    evidence = pd.DataFrame([
        {"accession": "PSI-10", "file_name": "scan.pdf", "locator": "p2", "chunk": 0,
         "text": "soot flame quenched at low flow", "transcribed": True},
        {"accession": "PSI-10", "file_name": "report.pdf", "locator": "p5", "chunk": 0,
         "text": "soot flame quenched near the wall", "transcribed": False},
    ])
    real_table = api.table
    monkeypatch.setattr(api, "table", lambda name: evidence if name == "evidence" else real_table(name))
    api._index.cache_clear()
    try:
        result = api.find_evidence("soot flame quenched", k=5)
    finally:
        api._index.cache_clear()
    marks = {d["file_name"]: d["transcribed"] for d in result["data"]["documents"]}
    assert marks == {"scan.pdf": True, "report.pdf": False}
    assert {s["file"]: s["transcribed"] for s in result["sources"] if "file" in s} == marks
    assert any("AI model's reading of a scanned page" in n for n in result["notes"])
    json.dumps(result, allow_nan=False)


def test_document_text_pages_text_scan_and_empty_file():
    report = "PSI-10_Engineering Documents_ACME Engineering Implementation Rpt..pdf"
    listing = api.document_text("PSI-10", report)
    assert listing["data"]["pages"][:3] == ["p1", "p2", "p3"] and listing["data"]["transcribed_pages"] == []
    page = api.document_text("10", report, page=3)["data"]
    assert page["page"] == "p3" and len(page["passages"]) == 3 and not any(p["transcribed"] for p in page["passages"])
    assert api.document_text("PSI-10", report, page="p3")["data"]["passages"] == page["passages"]

    scan = api.document_text("PSI-10", "PSI-10_Raw Data_19115 test sheets.pdf", page=1)
    assert scan["data"]["passages"][0]["transcribed"] and "ACME test #" in scan["data"]["passages"][0]["text"]
    assert any("AI model's reading of a scanned page" in n for n in scan["notes"])

    empty = api.document_text("PSI-47", "PSI-47_Reports_DAFT_FinalReport.doc")
    assert empty["data"]["pages"] == [] and any("no text" in n for n in empty["notes"])
    assert api.document_text("PSI-10", report, page=9999)["data"]["passages"] == []
    for bad in (("PSI-10", "nope.pdf"), ("PSI-999", report)):
        with pytest.raises(ValueError):
            api.document_text(*bad)
    json.dumps(scan, allow_nan=False)


def test_quotes_carry_their_spanish_translation_where_one_exists(monkeypatch, tmp_path):
    record = api.records()["PSI-10"]
    quotes = [s["quote"] for f in record["findings"] for s in f.get("sources", []) if s.get("quote")]
    known, unknown = quotes[0], next(q for q in quotes if q != quotes[0])
    path = tmp_path / "quotes_es.json"
    path.write_text(json.dumps({"note": "test", "lang": "es", "quotes": {
        api.quote_key(known): {"en": known, "es": "traducción de prueba"}, "0" * 16: {"en": "not a quote", "es": "x"}}}))
    monkeypatch.setattr(api, "QUOTES_ES", path)
    api._quotes_es.cache_clear()
    try:
        result = api.get_investigation("PSI-10")
        sources = [s for f in result["data"]["findings"] for s in f.get("sources", []) if s.get("quote")]
        assert {s["quote"] for s in sources if "quote_es" in s} == {known}
        assert all(s["quote_es"] == "traducción de prueba" for s in sources if s["quote"] == known)
        assert unknown in {s["quote"] for s in sources}  # an untranslated quote stays, without the field
        digest = api.find_evidence(known, accession="PSI-10", k=50, raw=False)["data"]["digest"]
        assert any(s.get("quote_es") for d in digest for s in d.get("sources", []))
        assert "quote_es" not in json.dumps(api.records()["PSI-10"])  # the cached record is not written to
        json.dumps(result, allow_nan=False)

        monkeypatch.setattr(api, "QUOTES_ES", tmp_path / "absent.json")
        api._quotes_es.cache_clear()
        assert "quote_es" not in json.dumps(api.get_investigation("PSI-10"))
        path.write_text('{"quotes": ')  # half-written file
        monkeypatch.setattr(api, "QUOTES_ES", path)
        api._quotes_es.cache_clear()
        assert "quote_es" not in json.dumps(api.get_investigation("PSI-10"))
    finally:
        api._quotes_es.cache_clear()


def test_relevance_never_offers_a_smoke_only_test_as_the_closest_fire_test():
    t = api.table("tests")
    smoke = t[t["accession"].isin(["PSI-101", "PSI-102"])]
    # typed like burns in the table: nothing there says the samples were never ignited
    assert smoke["ignited"].isna().all() and smoke["outcome"].isna().all()
    for acc in ("PSI-101", "PSI-102"):
        assert "below the ignition point" in json.dumps(api.records()[acc])
    for scenario in api.SCENARIOS:
        for phase in ("solid", "liquid", "gas"):
            data = api.relevance(scenario, fuel_phase=phase)["data"]
            closest = data["closest_same_phase_test"]
            if closest:
                assert closest["fire_test"] and closest["accession"] not in api.NOT_A_FIRE, (scenario, phase)
            if data["gap"]:
                assert data["gap"]["accession"] not in api.NOT_A_FIRE

    out = api.relevance("iss-cabin", fuel_phase="solid")
    same_r = next(r for r in out["data"]["ranking"] if r["accession"] == "PSI-101")
    assert same_r["nearest_test"]["fire_test"] is False and "nothing burned" in same_r["nearest_test"]["test_kind"]
    closest = out["data"]["closest_same_phase_test"]
    assert closest["accession"] == "PSI-99" and closest["result"] == {"burn_length_cm": 0.0}
    assert any(n.startswith("Not fire tests: PSI-101") and "below every investigation that burned" in n
               for n in out["notes"])
    assert any(n.startswith("Result of the closest solid-fuel test (PSI-99") and "no flame spread" in n
               for n in out["notes"])
    bass = next(r for r in out["data"]["ranking"] if r["accession"] == "PSI-26")
    assert bass["nearest_test"]["fire_test"] is True


def test_relevance_ranks_the_requested_phase_first_and_tests_that_burned_nothing_last():
    custom = {"x_o2": 0.34, "pressure_kpa": 57}
    for scenario in [*api.SCENARIOS, custom]:
        for phase in api.TRANSFER:
            ranking = api.relevance(scenario, fuel_phase=phase)["data"]["ranking"]
            tiers = [(not r["fire_test"], not r["phase_match"]) for r in ranking]
            assert tiers == sorted(tiers), (scenario, phase)
            for tier in set(tiers):
                scores = [r["score"] for r, t in zip(ranking, tiers) if t == tier]
                assert scores == sorted(scores, reverse=True)
            assert {r["accession"] for r in ranking if not r["fire_test"]} == set(api.NOT_A_FIRE)

    cabin = api.relevance("iss-cabin", fuel_phase="solid")["data"]["ranking"]
    same_r = next(r for r in cabin if r["accession"] == "PSI-101")
    assert same_r["score"] == max(r["score"] for r in cabin)  # the score is unchanged, only the order
    assert [r["accession"] for r in cabin[:2]] == ["PSI-25", "PSI-26"]
    for scenario in ("moon-habitat", custom):
        top = api.relevance(scenario, fuel_phase="solid")["data"]["ranking"][0]
        assert top["phase_match"] and top["nearest_test"]["fuel_phase"] == "solid", scenario

    detection = api.relevance("iss-cabin", fuel_phase="solid", pillar="detection")
    assert detection["data"]["ranking"][0]["accession"] == "PSI-101"
    assert any(n.startswith("Not fire tests:") and "detection question" in n for n in detection["notes"])


def test_coverage_labels_smoke_only_tests():
    sea = api.coverage(fuel_phase="solid")["data"]["references"][0]
    assert sea["id"] == "earth-sea-level"
    assert sea["nearest_test"]["accession"] == "PSI-101" and sea["nearest_test"]["fire_test"] is False
    assert 0 < sea["n_not_fire_tests_in_cell"] < sea["n_tests_in_cell"]


def test_ambiguous_names_list_the_choices_and_cfi_is_told_apart_from_flex():
    with pytest.raises(KeyError, match="PSI-98 SAFFIRE-I, PSI-99 SAFFIRE-II, PSI-100 SAFFIRE-III"):
        api._accession("saffire")
    with pytest.raises(KeyError, match="CFI, PSI-39"):
        api._accession("FLEX-1246")
    cfi = api.get_investigation("CFI", sections=["findings"])["notes"]
    assert any(n.startswith("CFI (PSI-39, Cool Flames Investigation) is not FLEX (PSI-69)") for n in cfi)
    assert any("FLEX-1206 to FLEX-1431 are tests of CFI" in n for n in api.get_investigation("FLEX", ["findings"])["notes"])
    assert api.NAME_NOTES["PSI-39"] in api.filter_tests(accession="PSI-39", test_id="1246")["notes"]
    assert api.NAME_NOTES["PSI-39"] not in api.filter_tests(accession="PSI-69", limit=1)["notes"]
    timeseries = next(t for t in tools.TOOLS if t["name"] == "timeseries")["description"]
    assert "it is not FLEX, PSI-69" in timeseries and "FLEX is PSI-69" in tools.ACCESSION["description"]
