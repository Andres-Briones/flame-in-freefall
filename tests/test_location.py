"""Where each investigation ran: `location` in the knowledge records, the platform_kind filters, the facility
glossary, the Saffire catalogue note in discrepancies, and the setting note of relevance."""
import json

import pytest

from fif import api, psi, tools
from fif.pipeline import check_digest as cd

pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "tests.parquet").exists(), reason="processed tables not built")

SAFFIRE = {"PSI-98", "PSI-99", "PSI-100"}
GROUND = {"PSI-60": "computation", "PSI-62": "computation", "PSI-115": "computation", "PSI-117": "computation",
          "PSI-142": "ground_lab"}
FIELDS = {"kind", "vehicle", "module", "facility", "crewed", "expedition", "uses_data_from", "also", "label", "source"}


def test_every_investigation_has_a_sourced_location():
    records = api.records()
    assert len(records) == 24
    for acc, rec in records.items():
        loc = rec["location"]
        assert set(loc) == FIELDS, acc
        assert loc["kind"] in api.PLATFORM_KINDS and set(loc["also"]) <= set(api.PLATFORM_KINDS), acc
        assert loc["label"] and loc["source"], acc
        assert set(loc["facility"]) <= set(api.facility_glossary()), acc
        assert set(loc["uses_data_from"]) <= set(records) - {acc}, acc
        expected = "cygnus_free_flight" if acc in SAFFIRE else GROUND.get(acc, "iss")
        assert loc["kind"] == expected, acc
        assert loc["crewed"] is {"iss": True, "cygnus_free_flight": False}.get(loc["kind"]), acc
        assert bool(loc["uses_data_from"]) == (acc in GROUND), acc


def test_drop_tower_precursors_are_recorded_but_no_test_row_is_one():
    also = {acc for acc, rec in api.records().items() if "drop_tower" in rec["location"]["also"]}
    assert also == {"PSI-10", "PSI-22", "PSI-23"}
    t = api.table("tests")
    assert set(t["platform_kind"]) == {"iss", "cygnus_free_flight"}
    kinds = {acc: rec["location"]["kind"] for acc, rec in api.records().items()}
    assert (t["platform_kind"] == t["accession"].map(kinds)).all()


def test_search_investigations_filters_by_platform_kind_and_cards_carry_location():
    cygnus = api.search_investigations(platform_kind="cygnus_free_flight")["data"]
    assert {c["accession"] for c in cygnus} == SAFFIRE
    assert all(c["location"]["vehicle"].startswith("Cygnus OA-") for c in cygnus)
    ground = api.search_investigations(platform_kind=["computation", "ground_lab"])["data"]
    assert {c["accession"] for c in ground} == set(GROUND)
    assert len(api.search_investigations(platform_kind="iss")["data"]) == 16
    assert api.search_investigations(platform_kind="drop_tower")["data"] == []
    with pytest.raises(ValueError):
        api.search_investigations(platform_kind="moon")


def test_filter_tests_by_platform_kind():
    out = api.filter_tests(platform_kind="cygnus_free_flight", row_kind=None, limit=10**4)["data"]
    t = api.table("tests")
    assert out["n_matching"] == int(t["accession"].isin(SAFFIRE).sum()) > 0
    assert {r["platform_kind"] for r in out["rows"]} == {"cygnus_free_flight"}
    iss = api.filter_tests(platform_kind="iss", row_kind=None)["data"]["n_matching"]
    assert iss + out["n_matching"] == len(t)


def test_get_investigation_explains_each_facility():
    loc = api.get_investigation("SAFFIRE-I")["data"]["location"]
    assert loc["kind"] == "cygnus_free_flight" and loc["vehicle"] == "Cygnus OA-6"
    assert set(loc["facility_notes"]) == {"Saffire enclosure", "Cygnus"}
    loc = api.get_investigation("CFI")["data"]["location"]
    assert set(loc["facility_notes"]) == {"CIR", "MDCA"} and all(loc["facility_notes"].values())
    assert "location" not in api.get_investigation("CFI", sections=["findings"])["data"]
    assert api.get_investigation("PSI-98")["data"]["identity"]["platform"].startswith("Orbital ATK Cygnus OA-6")


def test_saffire_flight_program_conflict_is_a_visible_note():
    for acc, pid in (("PSI-98", "D70"), ("PSI-100", "D71")):
        result = api.discrepancies(acc)
        notes = [r for r in result["data"]["raw_data_conflicts"] if r["column"] == "flight_program"]
        assert [n["id"] for n in notes] == [pid]
        assert notes[0]["table_value"] == "International Space Station (ISS)" and notes[0]["action"] == "note"
        assert "Cygnus" in notes[0]["evidence"]
        assert any("flight_program" in n for n in result["notes"])
    assert api.table("investigations").set_index("accession").loc["PSI-98", "flight_program"] == \
        "International Space Station (ISS)"
    assert not [r for r in api.discrepancies("PSI-99")["data"]["raw_data_conflicts"] if r["column"] == "flight_program"]


def test_relevance_says_where_the_closest_test_ran():
    out = api.relevance("moon-habitat", fuel_phase="solid")
    closest = out["data"]["closest_same_phase_test"]
    assert closest["setting"]["platform_kind"] == "cygnus_free_flight"
    assert out["data"]["gap"]["setting"] == closest["setting"]
    assert any(n.startswith("Setting of the closest solid-fuel test") and "cabin volume" in n for n in out["notes"])
    assert all("platform_kind" in r for r in out["data"]["ranking"])
    gas = api.relevance("mars-habitat", fuel_phase="gas")["data"]["closest_same_phase_test"]["setting"]
    assert gas["platform_kind"] == "iss" and "CIR" in gas["note"]


def test_tool_schemas_offer_platform_kind():
    specs = {t["name"]: t["input_schema"]["properties"] for t in tools.TOOLS}
    for name in ("search_investigations", "filter_tests", "coverage"):
        assert specs[name]["platform_kind"]["enum"] == list(api.PLATFORM_KINDS)
    json.dumps(tools.TOOLS)


def test_check_digest_rejects_bad_locations_and_record_quotes():
    record = {"location": {"kind": "moon", "also": ["drop_tower"], "facility": ["CIR", "Warp drive"],
                           "uses_data_from": ["PSI-0"], "source": []}}
    assert sorted(i["message"] for i in cd.location_issues(record, {"PSI-1"}, {"CIR": {}})) == [
        "'PSI-0' is not an investigation",
        "'Warp drive' has no entry in facilities.json",
        "location has no source",
        "unknown kind 'moon'; one of ['iss', 'cygnus_free_flight', 'drop_tower', 'ground_lab', 'computation']",
    ]

    class Raw(cd.Context):
        def raw_record(self, acc):
            return {"flightProgram": "Cygnus Spacecraft"}

    good = {"type": "psi_record", "field": "flightProgram", "quote": "Cygnus Spacecraft"}
    bad = {**good, "quote": "International Space Station"}
    assert not [i for i in cd.typed_source_issues("psi_record", "s", good, "PSI-99", Raw()) if i]
    assert [i["level"] for i in cd.typed_source_issues("psi_record", "s", bad, "PSI-99", Raw()) if i] == ["error"]
