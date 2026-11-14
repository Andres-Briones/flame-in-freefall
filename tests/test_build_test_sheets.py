import json

import pandas as pd
import pytest

from fif import api, psi
from fif.pipeline import build_test_sheets as ts
from fif.pipeline import build_tests as bt

# Three transcribers' spellings of the same form: units after the value, units in the label, bare 'Flame' labels.
INVERSE_UNITS_AFTER = """\
ACME / CFI-G (inverse flame) - Science Test Sheet
Test date: Oct 4, 2021
Local time: 2:00
GMT: 21 277 18:00
ACME test #: 21277A1
Test of day #: 1
Hot flame of day #: 1 sustained
Rack Officer (RO): [name omitted]
TEST CONDITIONS
Test type?: standard
Chamber pressure: 7.3 psia (CIR avg per FCU)
O2 flow rate: 0.295 slpm (N2 basis)
N2 flow rate: 0 slpm — note: no N2
INSTRUMENTATION
TFP?: no
FLAME BEHAVIOR
Flame (hot / cool / maybe cool): hot
Flame (hole/opening / partially detached): not marked
Flame (oscillating / unsteady / quasi-steady): quasi-steady
Out: temp. limit [underlined; "time out" ticked and struck through]
Ignited?: yes
Soot@ignition: lots — note: momentary
Soot@middle: none, little (both marked)
Soot@end: none
POST-TEST CONDITIONS
Chamber pressure: 7.4 psia (CIR avg per FCU)
Oxidizer bottle pressure: 1,230 psia
GENERAL COMMENTS
run w/o changes to parameters
* oxidizer flow dropped [?] during test [struck: illegible]
Form date: 22 Aug. 2021
"""
NORMAL_UNITS_IN_LABEL = """\
ACME / CFI-G (normal flame) - Science Test Sheet
Test date: May 5, 2021
GMT: 21 125 16:29
ACME test #: 21238N2 [differs from as-run file: 21328N2]
Flame of day #: no apparent ignition — note: "hot" written in left margin
TEST CONDITIONS
Chamber pressure (psia, CIR avg): 14.71
Fuel flow rate (slpm, N2 basis): 0.078 >
N2 flow rate (slpm): 0.207 > 0.494 > 0.207
FLAME BEHAVIOR — note: "n/a" written next to section title
Flame (hot / cool / maybe cool): not marked
Out (ext. detect / time out / temp. limit): not marked — note: "probably" written under time out
Ignited? (yes / no / yes, but ...*): no — note: no apparent ignition
Soot@ignition: not marked
Soot@middle: not marked
Soot@end: not marked
POST-TEST CONDITIONS
Chamber pressure (psia, CIR avg): 14.75
Oxidizer bottle pressure (psia): 360
GENERAL COMMENTS
Form date: 24 March 2021
"""
BARE_FLAME_LABELS = """\
ACME / Flame Design (inverse flame) - Science Test Sheet
Test date: 5/3/2019
ACME test #: [struck: illegible] N2
TEST CONDITIONS
Chamber pressure: psia
FLAME BEHAVIOR
Flame: hot, cool
Flame: partially detached
Flame: oscillating, unsteady
Out: ext. detect
Ignited?: [struck: yes] yes, but ...* Momentary <2s
Soot@end: little — note: residual
POST-TEST CONDITIONS
GENERAL COMMENTS
Form date: 19 Oct. 2021
"""
NORMAL_2019 = """\
ACME / Flame Design (normal flame) - Science Test Sheet
Test date: July 8, 2020
ACME test #: 19189H1
Flame of day #: 4
TEST CONDITIONS
Chamber pressure: ~18.5 psia — note: CIR avg
Fuel flow rate: 0.2 slpm (N2 basis)
N2 flow rate: 0.052 slpm
FLAME BEHAVIOR — note: flame out due to burner temp limit
Flame (asymmetric / hole/opening(s)): not marked
Flame (oscillating / unsteady / blew out): oscillating, blew out
Ignited?: yes
Soot: ignition only, lots
Soot@end: none
POST-TEST CONDITIONS
Oxygen conc.: 20.51 % (volume)
Oxidizer bottle pressure: 1446 psia
GENERAL COMMENTS
Form date: 6 Feb. 2019
"""


def sheet(text, day="21277", accession="PSI-159"):
    return ts.sheet_row(accession, f"{accession}_Raw Data_{day} test sheets.pdf", day, 1, text)


def test_fields_are_read_whether_units_follow_the_value_or_sit_in_the_label():
    after, in_label = sheet(INVERSE_UNITS_AFTER), sheet(NORMAL_UNITS_IN_LABEL, day="21328", accession="PSI-10")
    assert (after["chamber_pressure_psia"], after["chamber_pressure_post_psia"]) == (7.3, 7.4)
    assert (in_label["chamber_pressure_psia"], in_label["chamber_pressure_post_psia"]) == (14.71, 14.75)
    assert (after["o2_flow_slpm"], after["n2_flow_slpm"], after["fuel_flow_written"]) == (0.295, 0.0, None)
    assert in_label["fuel_flow_slpm"] == 0.078 and in_label["o2_flow_written"] is None
    assert (after["oxidizer_bottle_pressure_psia"], in_label["oxidizer_bottle_pressure_psia"]) == (1230.0, 360.0)
    assert after["form"] == "CFI-G (inverse flame)" and after["flame_of_day_written"] == "1 sustained"


def test_the_reading_is_kept_verbatim_next_to_the_normalised_value():
    row = sheet(INVERSE_UNITS_AFTER)
    assert row["out"] == "temp_limit"
    assert row["out_written"] == 'temp. limit [underlined; "time out" ticked and struck through]'
    assert (row["soot_ignition"], row["soot_ignition_written"]) == ("lots", "lots — note: momentary")
    assert row["comments"] == ("run w/o changes to parameters | "
                               "* oxidizer flow dropped [?] during test [struck: illegible]")


def test_a_field_that_is_not_one_clear_option_stays_empty():
    both, unmarked = sheet(INVERSE_UNITS_AFTER), sheet(NORMAL_UNITS_IN_LABEL)
    assert both["soot_middle"] is None and both["soot_middle_written"] == "none, little (both marked)"
    assert unmarked["out"] is None and "probably" in unmarked["out_written"]  # a remark is not a tick
    assert unmarked["flame"] is None and unmarked["soot_end"] is None
    assert unmarked["n2_flow_slpm"] is None and unmarked["n2_flow_written"] == "0.207 > 0.494 > 0.207"  # a ramp
    assert sheet(BARE_FLAME_LABELS)["chamber_pressure_psia"] is None


def test_ignition_hot_or_cool_flame_and_ending_are_normalised():
    hot, none, bare, old = (sheet(t) for t in (INVERSE_UNITS_AFTER, NORMAL_UNITS_IN_LABEL, BARE_FLAME_LABELS, NORMAL_2019))
    assert [r["ignited"] for r in (hot, none, bare, old)] == ["yes", "no", "yes_but", "yes"]
    assert [r["flame"] for r in (hot, none, bare, old)] == ["hot", None, "hot+cool", None]
    assert [r["out"] for r in (hot, none, bare, old)] == ["temp_limit", None, "ext_detect", None]
    assert bare["flame_behavior_written"] == "partially detached; oscillating, unsteady"
    assert bare["soot_end"] == "little"


def test_the_2019_form_has_no_ending_box_and_keeps_its_handwritten_note():
    row = sheet(NORMAL_2019, day="19189", accession="PSI-10")
    assert row["out_written"] is None and row["flame_written"] is None
    assert row["flame_behavior_note"] == "flame out due to burner temp limit"
    assert row["flame_behavior_written"] == "not marked; oscillating, blew out"
    assert (row["soot_written"], row["soot_ignition_written"], row["soot_end"]) == ("ignition only, lots", None, "none")
    assert row["chamber_pressure_psia"] == 18.5


def test_wrong_day_digits_are_resolved_from_the_file_and_both_ids_kept():
    row = sheet(NORMAL_UNITS_IN_LABEL, day="21328", accession="PSI-10")
    assert (row["test_id_written"], row["test_id"]) == ("21238N2 [differs from as-run file: 21328N2]", "21328N2")
    assert row["test_id_basis"] == "day_from_file_name" and "21238" in row["test_id_note"]
    assert row["differs_from_asrun"] and row["differs_text"] == "[differs from as-run file: 21328N2]"
    struck = sheet(BARE_FLAME_LABELS, day="19182", accession="PSI-10")
    assert (struck["test_id"], struck["test_id_basis"]) == ("19182N2", "day_from_file_name")
    clean = sheet(INVERSE_UNITS_AFTER)
    assert (clean["test_id"], clean["test_id_basis"], clean["test_id_note"]) == ("21277A1", "as_written", None)
    assert not clean["differs_from_asrun"] and clean["differs_text"] is None


@pytest.mark.parametrize("written, expected", [
    ("21277H[overwritten: illegible] ← H1", "21277H1"),
    ("22024-C1", "22024C1"),
    ("21219/G1 [?] [differs from as-run file: 21291G1]", "21291G1"),
    ("22018J4 (written \"2208J4\" with a digit squeezed in [?])", "22018J4"),
    ("19123[struck: illegible] B1 — note: \"B1\" written above the box", "19123B1"),
])
def test_test_id_is_read_through_the_transcribers_remarks(written, expected):
    assert ts.resolve_id(written, expected[:5])[0] == expected


def test_a_date_that_is_not_the_day_codes_date_is_noted_not_corrected():
    row = sheet(NORMAL_2019, day="19189", accession="PSI-10")
    assert (row["date_written"], row["date_parsed"], row["date"]) == ("July 8, 2020", "2020-07-08", "2019-07-08")
    assert "2020-07-08" in row["date_note"]
    assert sheet(INVERSE_UNITS_AFTER)["date_note"] is None
    assert ts.parse_date("5/3/2019") == "2019-05-03" and ts.parse_date("27 Jan 2022") == "2022-01-27"
    assert ts.parse_date("Sept. 13 2021") == "2021-09-13" and ts.parse_date("April 22,") is None


def test_uncertain_and_illegible_marks_are_counted_per_page():
    row = sheet(INVERSE_UNITS_AFTER)
    assert (row["n_uncertain"], row["n_illegible"]) == (1, 1)
    assert (sheet(NORMAL_2019)["n_uncertain"], sheet(NORMAL_2019)["n_illegible"]) == (0, 0)


def test_no_personnel_field_reaches_the_table():
    row = sheet(INVERSE_UNITS_AFTER)
    assert not any("name omitted" in str(v) or "Rack Officer" in str(v) for v in row.values())


def test_sheets_are_linked_to_tests_rows_and_data_files(tmp_path, monkeypatch):
    folder = tmp_path / "PSI-159"
    folder.mkdir()
    pages = [INVERSE_UNITS_AFTER, INVERSE_UNITS_AFTER.replace("21277A1", "21277M3"), "[blank page]"]
    (folder / "PSI-159_Raw Data_21277 test sheets.pdf.md").write_text(
        "<!-- AI reading -->\n" + "".join(f"## page {i}\n{p}\n" for i, p in enumerate(pages, 1)), encoding="utf-8")
    (folder / "PSI-159_Raw Data_21277 daily test point log.pdf.md").write_text("## page 1\nnot a sheet\n")
    rows = ts.read_sheets(tmp_path)
    assert [(r["page"], r["test_id"]) for r in rows] == [(1, "21277A1"), (2, "21277M3")]  # a blank page is no sheet
    tests = pd.DataFrame({"accession": ["PSI-159"], "test_id": ["21277 A1"]})
    files = pd.DataFrame({"accession": ["PSI-159"] * 2, "file_name": ["PSI-159_Raw Data_21277A1_data.csv",
                                                                     "PSI-159_Raw Data_as run21277M3.txt"]})
    linked = ts.link(rows, tests, files)
    assert [(r["in_tests"], r["tests_test_id"], r["has_data_file"]) for r in linked[:2]] == [
        (True, "21277 A1", True), (False, None, False)]


# the built table and what the tests table says about the same tests
@pytest.fixture(scope="module")
def sheets():
    path = psi.PROCESSED / "test_sheets.parquet"
    if not path.exists():
        pytest.skip("test_sheets table not built")
    return pd.read_parquet(path)


def test_one_row_per_sheet_page_and_every_page_has_a_test_id(sheets):
    assert not sheets.duplicated(["accession", "file_name", "page"]).any()
    assert sheets["test_id"].notna().all() and not sheets.duplicated(["accession", "test_id"]).any()
    assert set(sheets["accession"]) == {"PSI-10", "PSI-159"}


def test_attempts_without_table_row_stay_out_of_the_tests_table(sheets):
    only_record = sheets[~sheets["in_tests"] & ~sheets["has_data_file"]]
    assert {"19115M1", "19150G1", "21088M2", "22035D2"} <= set(only_record["test_id"])
    tests = api.table("tests")
    assert not tests["test_id"].str.replace(" ", "").isin(only_record["test_id"]).any()


def test_sheet_endings_never_contradict_the_cfig_extinction_mode(sheets):
    tests = api.table("tests")
    tests = tests[tests["accession"] == "PSI-159"].set_index("test_id")["extinction_mode"]
    linked = sheets[(sheets["accession"] == "PSI-159") & sheets["in_tests"] & sheets["out"].notna()]
    mode = linked["tests_test_id"].map(tests)
    assert (mode[linked["out"] == "ext_detect"].dropna() == "self_extinguished").all()
    assert (mode[linked["out"].isin(["time_out", "temp_limit"])] == "flow_terminated").all()
    assert (linked["out"] == "temp_limit").sum() >= 20


# patches that rest on the sheets (data/corrections/tests_patches.json)
def patch_row(**cells):
    return {"PSI-1": [{"test_id": "a", "source_row": 1, "flags": [], "extra": {"O2 flow (mg/s)": "8.9"}, **cells}]}


def test_a_sheet_based_patch_flags_with_its_own_flag_and_never_changes_the_value(monkeypatch):
    monkeypatch.setattr(bt, "read_transcription", lambda acc, name: [("p3", "GENERAL COMMENTS\nuncertain  C3H8 %")])
    patch = {"id": "X", "accession": "PSI-1", "test_id": "a", "column": "fuel_fraction", "table_value": 1.0,
             "evidence_value": None, "action": "flag", "basis": "test_sheet",
             "sheet": {"file_name": "s.pdf", "page": 3, "quote": "uncertain C3H8 %"}}
    groups = patch_row(fuel_fraction=1.0)
    bt.apply_patches(groups, [patch])
    row = groups["PSI-1"][0]
    assert row["fuel_fraction"] == 1.0 and row["flags"] == ["conflicts_with_test_sheet"]
    assert row["extra"]["discrepancies"] == ["X"] and "fuel_fraction_original" not in row["extra"]
    with pytest.raises(ValueError, match="can only be flagged"):
        bt.apply_patches(patch_row(fuel_fraction=1.0), [{**patch, "action": "replace", "evidence_value": 0.3}])


def test_a_sheet_based_patch_fails_once_its_quote_is_gone(monkeypatch):
    monkeypatch.setattr(bt, "read_transcription", lambda acc, name: [("p3", "re-read: certain C3H8 %")])
    patch = {"id": "X", "accession": "PSI-1", "test_id": "a", "column": "fuel_fraction", "table_value": 1.0,
             "evidence_value": None, "action": "flag", "basis": "test_sheet",
             "sheet": {"file_name": "s.pdf", "page": 3, "quote": "uncertain C3H8 %"}}
    with pytest.raises(ValueError, match="patch X: the quote"):
        bt.apply_patches(patch_row(fuel_fraction=1.0), [patch])


def test_a_source_column_kept_in_extra_can_be_flagged_but_not_replaced():
    patch = {"id": "X", "accession": "PSI-1", "test_id": "a", "column": "O2 flow (mg/s)", "table_value": "8.9",
             "evidence_value": 4.7, "action": "flag"}
    groups = patch_row()
    bt.apply_patches(groups, [patch])
    assert groups["PSI-1"][0]["flags"] == ["conflicts_with_raw"] and groups["PSI-1"][0]["extra"]["O2 flow (mg/s)"] == "8.9"
    with pytest.raises(ValueError, match="patch X"):
        bt.apply_patches(patch_row(), [{**patch, "table_value": "9.9"}])
    with pytest.raises(ValueError, match="can only be flagged"):
        bt.apply_patches(patch_row(), [{**patch, "action": "replace"}])


def test_every_sheet_based_patch_quotes_its_page_and_says_it_is_an_ai_reading():
    patches = [p for p in json.loads(bt.PATCHES.read_text()) if p.get("basis") == "test_sheet"]
    flags = [p for p in patches if p["action"] == "flag"]
    assert flags and {p["action"] for p in patches} == {"flag", "note"}
    for p in patches:
        assert "AI reading" in p["evidence"] and "not checked by a human" in p["evidence"], p["id"]
    for p in flags:
        assert not bt.sheet_quote_missing(p), p["id"]
    table = bt.discrepancies().set_index("id")
    assert set(table.loc[[p["id"] for p in flags], "flag"]) == {"conflicts_with_test_sheet"}
    assert table.loc[[p["id"] for p in patches if p["action"] == "note"], "flag"].isna().all()


def table_row(test_id, accession="PSI-159"):
    t = api.table("tests")
    sel = t[(t["accession"] == accession) & (t["test_id"] == test_id)]
    assert len(sel) == 1
    r = sel.iloc[0]
    return r, set(r["flags"].split(";")), json.loads(r["extra"])


def test_runs_where_nothing_flowed_are_flagged_and_still_listed_as_not_ignited():
    for test_id, flag in (("21196 A1", "conflicts_with_raw"), ("21130 A4", "conflicts_with_raw"),
                          ("21242 P2", "conflicts_with_raw"), ("21125 A4", "conflicts_with_test_sheet"),
                          ("21209 A2", "conflicts_with_test_sheet")):
        r, flags, extra = table_row(test_id)
        assert flag in flags and r["ignited"] == False and extra["discrepancies"], test_id  # noqa: E712


def test_burner_oxygen_the_flows_contradict_is_flagged_and_kept():
    for test_id, table_value in (("21256 C2", 0.5), ("21277 P1", 0.3)):
        r, flags, extra = table_row(test_id)
        assert r["x_o2_burner"] == pytest.approx(table_value) and "conflicts_with_raw" in flags
        assert "x_o2_burner_original" not in extra
    r, flags, extra = table_row("21277 F2")
    assert "conflicts_with_raw" in flags and extra["O2 flow rate (mg/s)"] == "8.946670681"


def test_uncertain_propane_fraction_is_flagged_from_the_sheet_and_kept():
    for n in range(1, 6):
        r, flags, extra = table_row(f"21301A{n}", "PSI-10")
        assert r["fuel_fraction"] == 1.0 and {"conflicts_with_test_sheet", "placeholder_values"} <= flags
    assert "conflicts_with_test_sheet" not in table_row("21301A6", "PSI-10")[1]


# the link from filter_tests
def test_filter_tests_attaches_the_sheet_with_the_ai_reading_note():
    result = api.filter_tests(accession="PSI-159", sheets=True, columns=["extinction_mode"], limit=1000)
    with_sheet = [r for r in result["data"]["rows"] if "test_sheet" in r]
    assert len(with_sheet) > 300
    ended = next(r for r in with_sheet if r["test_id"] == "21242 A1")
    assert ended["extinction_mode"] == "flow_terminated" and ended["test_sheet"]["out"] == "temp_limit"
    assert ended["test_sheet"]["file_name"].endswith("21242 test sheets.pdf") and ended["test_sheet"]["page"] >= 1
    assert any("AI model's reading" in n and "not checked by a human" in n for n in result["notes"])
    assert any(s.get("transcribed") and s["file"].endswith("sheets.pdf") for s in result["sources"])


def test_filter_tests_without_sheets_only_says_they_exist():
    result = api.filter_tests(accession="PSI-159", limit=5)
    assert not any("test_sheet" in r for r in result["data"]["rows"])
    assert any("sheets=true" in n and "not checked by a human" in n for n in result["notes"])
    assert not any("sheets=true" in n for n in api.filter_tests(accession="PSI-26", limit=5)["notes"])


def test_filter_tests_selects_flames_stopped_by_the_temperature_limit():
    result = api.filter_tests(accession="PSI-159", sheet_out="temp_limit", columns=["extinction_mode"])
    rows = result["data"]["rows"]
    assert len(rows) >= 20 and {r["extinction_mode"] for r in rows} == {"flow_terminated"}
    assert all(r["test_sheet"]["out"] == "temp_limit" for r in rows)
    assert any("not checked by a human" in n for n in result["notes"])
