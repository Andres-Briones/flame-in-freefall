import json

import pandas as pd
import pytest

from fif.pipeline import build_tests as bt


def test_num_accepts_plain_and_approximate_numbers_only():
    assert bt.num("0.37") == 0.37
    assert bt.num("~ 21.5") == 21.5
    assert bt.num("RAMPED") is None
    assert bt.num("Insignificant") is None
    assert bt.num("") is None


def test_qty_requires_the_unit():
    assert bt.qty("20 cm/s", "cm/s") == 20.0
    assert bt.qty("145 s", "s") == 145.0
    assert bt.qty("1.25 atm ", "atm") == 1.25
    assert bt.qty("Insignificant", "s") is None


def test_pressure_conversions():
    assert bt.ATM_KPA == pytest.approx(101.325)
    assert 760 * bt.MMHG_KPA == pytest.approx(101.325)
    assert 3 * bt.BAR_KPA == 300


@pytest.mark.parametrize(
    "text, expected",
    [
        ("21; 26.5; 40", [0.21, 0.265, 0.40]),
        ("0.17; 0.21;0.25; 0.3", [0.17, 0.21, 0.25, 0.3]),
        ("21.5 - 21.7", [0.215, 0.217]),
        ("~30% and ~21% O2 with He", [0.30, 0.21]),
        ("~21% O2 with N2", [0.21]),
        ("30%-40%", [0.30, 0.40]),
    ],
)
def test_fractions_parses_o2_lists_and_ranges(text, expected):
    assert bt.fractions(text) == pytest.approx(expected)


def test_o2_fields_single_value_vs_range():
    assert bt.o2_fields([0.21]) == {"x_o2_min": 0.21, "x_o2_max": 0.21, "x_o2": 0.21}
    assert bt.o2_fields([0.21, 0.4, 0.265]) == {"x_o2_min": 0.21, "x_o2_max": 0.4, "x_o2": None}
    assert bt.o2_fields([]) == {}


def test_percent_reads_fuel_fraction():
    assert bt.percent("30% butane") == 0.3
    assert bt.percent("100%C2H4") == 1.0
    assert bt.percent("75 % Propylene") == 0.75
    assert bt.percent("Propylene") is None


@pytest.mark.parametrize(
    "code, iso",
    [("19115A1", "2019-04-25"), ("21196 A1", "2021-07-15"), ("17319", "2017-11-15"), ("20060", "2020-02-29"), ("21366", None), ("1206", None)],
)
def test_yyddd(code, iso):
    assert bt.yyddd(code) == iso


def test_parse_date_rejects_garbled_and_future_dates():
    assert bt.parse_date("2/19/2014", "%m/%d/%Y") == "2014-02-19"
    assert bt.parse_date("11/18/11", "%m/%d/%Y", "%m/%d/%y") == "2011-11-18"
    assert bt.parse_date("6/29/`12", "%m/%d/%Y") is None
    assert bt.parse_date("5/15/2103", "%m/%d/%Y") is None


@pytest.mark.parametrize(
    "raw, fuel",
    [
        ("100% C2H4", "ethylene"),
        ("C3H8", "propane"),
        ("Heptane (50%) IsoOctane (50%) (mixture)", "n-heptane/isooctane"),
        ("[.60]/[.40] C12H26/iso-dodecane", "n-dodecane/isododecane"),
        ("25% H2, 20% CH4, with He", "hydrogen/methane"),
        ("Cotton-Fiberglass (SIBAL)", "sibal fabric"),
        ("parrafin wax slab", "paraffin wax"),
        ("2 cm sphere", None),
    ],
)
def test_fuel_name(raw, fuel):
    assert bt.fuel_name(raw) == fuel


def test_every_table_has_exactly_one_adapter():
    paths = bt.table_paths()
    if not paths:
        pytest.skip("raw PSI files not downloaded")
    for path in paths:
        bt.adapter_for(path)


@pytest.fixture(scope="module")
def table():
    if not bt.table_paths() or not (bt.psi.PROCESSED / "investigations.csv").exists():
        pytest.skip("raw PSI files or investigations table not available")
    return bt.build()


def row(df, acc, test_id=None, source_row=None):
    sel = df[df.accession == acc]
    sel = sel[sel.test_id == test_id] if test_id is not None else sel[sel.source_row == source_row]
    assert len(sel) == 1
    return sel.iloc[0]


def test_numeric_columns_are_floats(table):
    for col in bt.NUMERIC:
        assert table[col].dtype == "float64", col


def test_blank_and_note_rows_are_dropped(table):
    assert (table.accession == "PSI-142").sum() == 0
    assert (table.source_file.str.contains("CFI-G_Inverse")).sum() == 154
    assert (table.accession == "PSI-98").sum() == 2
    assert (table.accession == "PSI-99").sum() == 9
    assert (table.accession == "PSI-22").sum() == 20


def test_flame_design_normal_row(table):
    r = row(table, "PSI-10", "19115A1")
    assert r.date == "2019-04-25" and r.fuel == "ethylene" and r.config == "normal"
    assert r.x_o2 == pytest.approx(0.207128374)
    assert r.pressure_kpa == pytest.approx(1.01184402 * 101.325)
    assert r.t_ad_k == pytest.approx(2352.144414)
    assert json.loads(r.extra)["XO2 (final)"] == "0.206202891"


def test_ramped_values_stay_in_extra(table):
    r = row(table, "PSI-10", "19115D2")
    assert r.fuel_fraction != r.fuel_fraction and json.loads(r.extra)["Xfuel"] == "RAMPED"


def test_bre_test_day_with_o2_list(table):
    r = row(table, "PSI-20", source_row=1)
    assert r.row_kind == "test_day" and r.date == "2019-02-08" and r.n_flames == 10
    assert (r.x_o2_min, r.x_o2_max) == (0.21, 0.40) and r.x_o2 != r.x_o2
    assert json.loads(r.extra)["Oxygen Conc (percent)"] == "21; 26.5; 40"


def test_cld_fuel_typos_normalised(table):
    r = row(table, "PSI-21", "17324")
    assert r.fuel == "methane" and r.fuel_raw == "40% CH5" and r.date == "2017-11-20"


def test_s_flame_approximate_o2_and_typo_diluent(table):
    r = row(table, "PSI-23", "19256")
    assert r.x_o2 == 0.21 and r.diluent == "n2" and r.fuel_fraction == 0.5


def test_saffire2_units_and_unparseable_burn_time(table):
    r = row(table, "PSI-99", "2-1")
    assert r.flow_cm_s == 20 and r.x_o2 == pytest.approx(0.215)
    assert r.burn_time_s != r.burn_time_s and json.loads(r.extra)["Burn Time (s)"] == "Insignificant"
    r = row(table, "PSI-99", "2-8")
    assert r.x_o2 == pytest.approx(0.221) and r.burn_time_s == 600


def test_flex_mmhg_and_extinction(table):
    r = row(table, "PSI-69", "20CAL08")
    assert r.pressure_kpa == pytest.approx(757.7 * 101.325 / 760)
    assert r.extinction_mode == "disruption" and r.fuel == "methanol" and r.burn_time_s == 4.3


def test_cfig_inverse_row(table):
    r = row(table, "PSI-159", "21196 A2")
    assert r.config == "inverse" and r.fuel == "ethane" and r.ignited
    assert r.pressure_kpa == pytest.approx(110.0) and r.extinction_mode == "flow_terminated"
    assert r.burn_time_s == 35 and r.peak_temp_c == pytest.approx(162.9)


def test_mistyped_test_id_is_corrected_from_raw_files(table):
    r = row(table, "PSI-10", "22024M1")
    assert r.date == "2022-01-24" and extra(r)["test_id_original"] == "22042M1"
    assert {"corrected_from_raw", "filled_from_raw"} <= set(flags(r)) and extra(r)["discrepancies"] == ["D01", "D02"]


def extra(r):
    return json.loads(r.extra) if isinstance(r.extra, str) else {}


def flags(r):
    return set(r["flags"].split(";")) if isinstance(r["flags"], str) else set()


def test_droplet_checks_flag_composition_and_extinction_diameter():
    row = {"x_o2": 0.13, "extra": {"N": "0.85", "He": "0"}, "ext_diameter_mm": 3.34, "d0_mm": 3.33, "flags": []}
    bt.droplet_checks(row, ["N", "He"])
    assert row["flags"] == ["composition_sum", "ext_gt_d0"]
    row = {"x_o2": 0.2, "extra": {"N": "0.79", "He": "0"}, "ext_diameter_mm": 0.0, "d0_mm": 2.0, "flags": []}
    bt.droplet_checks(row, ["N", "He"])
    assert row["flags"] == ["ext_zero"]  # 0.99 is within 1 +/- 0.01


def test_note_o2_reads_the_diluted_value_from_as_run_notes():
    assert bt.note_o2("flow stop 14:44:30, final O2 is 17.3%. Had Chris anneal") == pytest.approx(0.173)
    assert bt.note_o2("vitiation to 17.3 % o2.  Lots of vapor jetting") == pytest.approx(0.173)
    assert bt.note_o2("increased flow to 20 cm/s, got a very sooty tail") is None


def test_correct_keeps_the_original_value_and_flags():
    row = {"flow_cm_s": 30.0, "extra": {}, "flags": []}
    bt.correct(row, "flow_cm_s", 25.0, "corrected_from_report")
    assert row == {"flow_cm_s": 25.0, "extra": {"flow_cm_s_original": 30.0}, "flags": ["corrected_from_report"]}


# 1. oxygen semantics
def test_inverse_flame_o2_is_the_burner_stream(table):
    r = row(table, "PSI-10", "21328A1")
    assert r.x_o2_burner == pytest.approx(0.37082819) and pd.isna(r.x_o2_ambient)
    assert pd.isna(r.x_o2_min) and r.x_o2 == pytest.approx(0.37082819)  # x_o2 kept for compatibility
    assert "o2_is_burner_stream" in flags(r)
    r = row(table, "PSI-159", "21242 A1")
    assert r.x_o2_burner == 0.85 and pd.isna(r.x_o2_ambient)
    r = row(table, "PSI-10", "19115A1")
    assert r.x_o2_ambient == pytest.approx(0.207128374) and pd.isna(r.x_o2_burner) and not flags(r)
    assert table[table.x_o2_ambient.notna()].x_o2_ambient.max() <= 0.41


# 2. SAME planning matrix
def test_same_rows_are_planned_not_flown(table):
    same = table[table.accession == "PSI-102"]
    assert len(same) == 8 and set(same.row_kind) == {"planned"}
    assert all("planned_not_flown" in flags(r) for _, r in same.iterrows())


# 3. s-Flame on-orbit dilution and 35 vs 45% H2
def test_s_flame_blend_days_diluted_on_orbit(table):
    r = row(table, "PSI-23", "20006")
    assert r.fuel_fraction == 0.45 and extra(r)["fuel_fraction_original"] == 1.0
    assert "corrected_from_report" in flags(r)
    r = row(table, "PSI-23", "20190")
    assert r.fuel_fraction == 0.45 and extra(r)["fuel_fraction_original"] == 0.35
    assert {"conflicts_with_report", "corrected_from_raw"} <= set(flags(r))


# 4. BASS-II final O2 artefacts and 2018 dates
def test_bass2_artefacts_blanked_and_dates_fixed(table):
    r = row(table, "PSI-25", "P22b")
    assert "Calibrated final O2 % by vol" not in extra(r)
    assert extra(r)["Calibrated final O2 % by vol_original"] == "39.1" and "o2_final_artifact" in flags(r)
    r = row(table, "PSI-25", "T9")
    assert r.date == "2014-06-24" and extra(r)["date_original"] == "2018-06-24" and "date_corrected" in flags(r)
    assert extra(row(table, "PSI-25", "B1"))["Calibrated final O2 % by vol"] == "22.2"


# 5. BASS as-run join
def test_bass_as_run_fills_o2_pressure_flow(table):
    r = row(table, "PSI-26", "7")  # as-run 4: O2 0.219, 0.97 atm, air 10
    assert r.x_o2_ambient == pytest.approx(0.219) and r.pressure_kpa == pytest.approx(0.97 * 101.325)
    assert r.flow_cm_s == 10 and extra(r)["asrun_sheet"] == "2012" and "Don" in extra(r)["asrun_notes"]
    r = row(table, "PSI-26", "100")  # as-run 86: cell 0.21111 is pre-dilution, note gives 17.3%
    assert r.x_o2_ambient == pytest.approx(0.173) and extra(r)["asrun_o2"] == "0.21111"
    assert "o2_from_notes" in flags(r)
    r = row(table, "PSI-26", "93")  # as-run 88, right after the 16.8% run, no value in notes
    assert pd.isna(r.x_o2_ambient) and "needs_review" in flags(r)


# 6. CFI data-summary spreadsheet
def test_cfi_rebuilt_from_data_summary(table):
    cfi = table[table.accession == "PSI-39"]
    assert len(cfi) == 227 and cfi.test_id.is_unique
    assert cfi.d0_mm.notna().sum() == 148 and cfi.ext_diameter_mm.notna().sum() == 144
    r = row(table, "PSI-39", "1206")
    assert (r.d0_mm, r.ext_diameter_mm, r.burn_rate_k_mm2_s, r.n_reignitions) == (4.039, 3.577, 0.379, 0)
    assert r.cool_flame and r.config == "free droplet" and extra(r)["experimental_table_row"] == 1
    assert row(table, "PSI-39", "1258").n_reignitions == 7
    r = row(table, "PSI-39", "1411")
    assert r.fuel == "farnesane" and r.date == "2017-09-06" and "date_corrected" in flags(r)
    assert extra(r)["date_original"] == "2011-09-06"
    assert "composition_sum" in flags(row(table, "PSI-39", "1219"))


# 7. FLEX outcomes and oddities
def test_flex_outcome_columns_and_flags(table):
    r = row(table, "PSI-69", "20CAL08")
    assert (r.d0_mm, r.ext_diameter_mm, r.burn_rate_k_mm2_s) == (1.69, 0.89, 0.52)
    assert "pressure_zero_in_source" in flags(row(table, "PSI-69", "C11M201"))
    assert "ext_gt_d0" in flags(row(table, "PSI-69", "C13H102"))
    assert "composition_sum" in flags(row(table, "PSI-69", "203F001"))
    dup = table[(table.accession == "PSI-69") & (table.test_id == "193F001")]
    assert len(dup) == 2 and all("duplicate_id" in flags(r) for _, r in dup.iterrows())
    assert extra(row(table, "PSI-69", source_row=24))["Droplet initial diameter; mm"] == "\u2013"  # cp1252 dash


# 8. SPICE master run log
def test_spice_rebuilt_from_master_log(table):
    spice = table[table.accession == "PSI-107"]
    assert len(spice) == 526 and spice.date.min() == "2009-02-14" and spice.date.max() == "2009-06-23"
    assert (spice.date == "2009-03-03").sum() == 57  # GMT 062 methane session, absent from the CSV
    r = row(table, "PSI-107", source_row=5)
    assert r.measurement == "video" and r.flame_length_mm == pytest.approx(46.1973) and r.at_smoke_point
    r = row(table, "PSI-107", source_row=6)
    assert r.measurement == "still" and r.flame_length_mm == pytest.approx(48.109, abs=1e-3)
    r = row(table, "PSI-107", source_row=397)
    assert pd.isna(r.flow_cm_s) and "flow_missing_los" in flags(r)
    r = row(table, "PSI-107", source_row=356)
    assert r.flow_cm_s == pytest.approx(-0.28, abs=0.01) and "flow_below_sensor_range" in flags(r)


@pytest.mark.parametrize(
    "text, seconds",
    [("14:37:08", 52628), ("14.34.57", 52497), ("1744", 63840), ("1.4022453703703703", 34754), ("Ku LOS", None)],
)
def test_clock_reads_the_log_time_formats(text, seconds):
    assert bt.clock(text) == seconds


def review(r):
    return json.loads(r.extra) if isinstance(r.extra, str) else {}


def test_spice_smoke_point_review_unique_matches(table):
    spice = table[table.accession == "PSI-107"]
    assert spice.smoke_point_reviewed.sum() == 15 and not (spice.smoke_point_reviewed == False).any()  # noqa: E712
    assert table[table.accession != "PSI-107"].smoke_point_reviewed.isna().all()
    r = row(table, "PSI-107", source_row=331)  # same GMT data, fuel 49, air 20 and Rad 1.18
    assert r.smoke_point_reviewed and review(r)["review_tp"] == "75P16-7" and r.at_smoke_point
    assert review(r)["review_flame_length_mm_sheet2"].startswith("15.43")
    r = row(table, "PSI-107", source_row=427)  # air sweep at fixed fuel: only this row has air 51
    assert r.smoke_point_reviewed and review(r)["review_point"] == 16
    # P16-3 (GMT 058): the video row confirms Rad; the Nikon still of the same moment (r224) is not tagged
    assert row(table, "PSI-107", source_row=222).smoke_point_reviewed
    assert pd.isna(row(table, "PSI-107", source_row=224).smoke_point_reviewed)
    # 75P7-2: fuel and air agree with r365 but Rad (1.54 vs 2.13) does not, so it is a bracket, not a match
    assert pd.isna(row(table, "PSI-107", source_row=365).smoke_point_reviewed)


def test_spice_smoke_point_review_brackets(table):
    for source_row in (467, 468):  # P16-5: fuel 48 read between the logged 45 and 50
        r = row(table, "PSI-107", source_row=source_row)
        assert "smoke_point_bracket" in flags(r) and pd.isna(r.smoke_point_reviewed)
        assert review(r)["review_point"] == 38 and review(r)["review_fuel_display"] == "48"


def test_each_review_point_tags_one_row_or_a_bracket_pair(table):
    spice = table[table.accession == "PSI-107"]
    tagged = {}
    for _, r in spice.iterrows():
        if "review_point" in review(r):
            tagged.setdefault(review(r)["review_point"], []).append(r)
    assert len(tagged) == 28
    for point, rs in tagged.items():
        brackets = ["smoke_point_bracket" in flags(r) for r in rs]
        if len(rs) == 1:
            assert rs[0].smoke_point_reviewed is True and not brackets[0], point
        else:
            assert len(rs) == 2 and all(brackets) and not any(r.smoke_point_reviewed is True for r in rs), point


# 9. Saffire
def test_saffire_corrections_and_outcomes(table):
    r = row(table, "PSI-100", "S1")
    assert r.flow_cm_s == 25 and extra(r)["flow_cm_s_original"] == 30
    assert r.geometry.startswith("thickness 0.33 mm") and {"corrected_from_report", "unit_corrected"} <= flags(r)
    assert (r.spread_rate_mm_s, r.burn_length_cm) == (2.3, 84) and "PSI-100" in extra(r)["outcome_source"]
    r = row(table, "PSI-98", "S2")
    assert r.geometry.startswith("thickness 0.37 mm") and (r.spread_rate_mm_s, r.burn_length_cm) == (1.3, 10)
    r = row(table, "PSI-99", "2-6")
    assert r.flow_cm_s == 25 and r.fuel == "sibal fabric" and extra(r)["fuel_raw_original"] is None
    assert (r.spread_rate_mm_s, r.burn_length_cm) == (2.6, 29) and r.geometry.startswith("thickness 0.37 mm")
    assert row(table, "PSI-99", "2-9").fuel == "pmma"


# 10. E-FIELD duplicate, SLICE last day
def test_efield_duplicate_dropped_and_slice_label_fixed(table):
    r = row(table, "PSI-22", "18319")
    assert r.fuel_fraction != r.fuel_fraction and extra(r)["verbatim_duplicate_dropped"] == [29]
    r = row(table, "PSI-106", source_row=12)
    assert r.fuel_raw == "100% C3H8 and then 100% C2H4" and extra(r)["fuel_raw_original"] == "100% C2H4"
    assert "label_fixed" in flags(r)


# 11. CFI-G flags
def test_cfig_flags(table):
    r = row(table, "PSI-159", "21196 J1")
    assert {"flash_only", "pressure_9pct_above_nominal", "o2_is_burner_stream"} <= flags(r)
    assert "burner_over_limit" in flags(row(table, "PSI-159", "21242 A1"))
    assert "pressure_9pct_above_nominal" not in flags(row(table, "PSI-159", "21088A1"))
    low = row(table, "PSI-159", "21196 K1")  # 49.5 kPa is below the 0.5 atm fill level, not 9% above it
    assert low.pressure_kpa < 50 and "pressure_9pct_above_nominal" not in flags(low)


# 12. Flame Design flags
def test_flame_design_flags(table):
    assert "id_suspect" in flags(row(table, "PSI-10", "22024M1"))
    assert "placeholder_values" in flags(row(table, "PSI-10", "21301A1"))
    assert "ramped" in flags(row(table, "PSI-10", "19115D2"))
    assert "ramped" not in flags(row(table, "PSI-10", "19115A1"))


# raw-data patches (data/corrections/tests_patches.json)
def test_patch_replaces_value_and_keeps_the_table_value(table):
    r = row(table, "PSI-159", "21112 A6")
    assert r.burn_time_s == 147 and extra(r)["burn_time_s_original"] == 259 and "corrected_from_raw" in flags(r)
    r = row(table, "PSI-159", "21106 F4")
    assert r.ignited and extra(r)["ignited_original"] == 0


def test_patch_flag_keeps_the_table_value(table):
    r = row(table, "PSI-39", "1336")
    assert r.pressure_kpa == pytest.approx(303.975) and "conflicts_with_raw" in flags(r)
    assert "pressure_kpa_original" not in extra(r)


def test_patch_fills_empty_cell(table):
    r = row(table, "PSI-98", "S1")
    assert r.pressure_kpa == pytest.approx(102.3) and "filled_from_raw" in flags(r)


def test_stale_patch_fails():
    from fif.pipeline import build_tests

    groups = {"PSI-1": [{"test_id": "a", "burn_time_s": 5.0, "flags": [], "extra": {}}]}
    patch = {"id": "X", "accession": "PSI-1", "test_id": "a", "column": "burn_time_s", "table_value": 9.0,
             "evidence_value": 7.0, "action": "replace"}
    with pytest.raises(ValueError, match="patch X"):
        build_tests.apply_patches(groups, [patch])
    build_tests.apply_patches(groups, [{**patch, "table_value": 5.0}])
    assert groups["PSI-1"][0]["burn_time_s"] == 7.0 and groups["PSI-1"][0]["extra"]["burn_time_s_original"] == 5.0



# 13. Rows the verification found wrong or ambiguous
def test_every_repeated_test_id_is_flagged_and_rows_have_a_unique_key(table):
    repeated = table.duplicated(["accession", "test_id"], keep=False)
    assert repeated.sum() == 12
    assert all(("duplicate_id" in flags(r)) == rep for (_, r), rep in zip(table.iterrows(), repeated))
    assert not table.duplicated(["source_file", "source_row"]).any()


def test_false_same_r_row_is_kept_and_flagged(table):
    r = row(table, "PSI-101", source_row=74)
    assert (r.test_id, r.fuel) == ("57", "teflon") and "conflicts_with_raw" in flags(r)
    assert extra(r)["discrepancies"] == ["D30"]
    assert "conflicts_with_raw" not in flags(row(table, "PSI-101", source_row=56))


def test_unusable_source_dates_are_flagged(table):
    for acc, tid in (("PSI-26", "35"), ("PSI-26", "53a"), ("PSI-25", "O10")):
        r = row(table, acc, tid)
        assert pd.isna(r.date) and "date_conflict" in flags(r) and extra(r)["Date"]


def test_bass_shapes_get_their_material_from_the_documents(table):
    r = row(table, "PSI-25", source_row=int(table[(table.accession == "PSI-25")
                                                   & (table.fuel_raw == '1/4" clear rod')].source_row.iloc[0]))
    assert r.fuel == "pmma" and "fuel_inferred" in flags(r) and "PSI-25 record" in extra(r)["fuel_source"]
    assert table[(table.accession == "PSI-25") & (table.fuel_raw == "4 cm spherical section")].fuel.isna().all()
    assert (table[(table.accession == "PSI-26") & table.fuel_raw.str.contains("sphere")].fuel == "pmma").all()
    assert table[(table.accession == "PSI-25")].flow_cm_s.notna().sum() == 25


def test_low_o2_text_and_autofill_cells_are_flagged(table):
    assert "low_o2_in_source" in flags(row(table, "PSI-10", "22024K2"))
    assert "autofill_artifact" in flags(row(table, "PSI-23", "19256"))
    assert "autofill_artifact" not in flags(row(table, "PSI-23", "19254"))


def test_report_and_recording_disagree_on_s_flame_dilution(table):
    r = row(table, "PSI-23", "20006")
    assert r.fuel_fraction == 0.45 and extra(r)["fuel_fraction_original"] == 1.0
    assert {"corrected_from_report", "conflicts_with_raw"} <= flags(r)


def test_replaced_boolean_keeps_a_boolean_original(table):
    assert extra(row(table, "PSI-159", "21106 F4"))["ignited_original"] is False


def test_bass_outcomes_are_read_from_the_crews_words_and_quote_them(table):
    solid = table[table["accession"].isin(["PSI-25", "PSI-26"])]
    assert table.loc[~table.index.isin(solid.index), "outcome"].isna().all()
    assert solid.groupby("accession")["outcome"].count().to_dict() == {"PSI-25": 25, "PSI-26": 80}
    for r in solid[solid["outcome"].notna()].itertuples():
        assert " ".join(r.outcome_quote.split()) in " ".join(extra(r)[extra(r)["outcome_field"]].split())
        assert (r.outcome == "extinguished") == (r.outcome_cause in bt.OUTCOME_CAUSES)
    r = row(table, "PSI-25", "B18")
    assert (r.outcome, r.outcome_cause, r.outcome_quote) == ("extinguished", "blowoff", "10 blowoff")
    r = row(table, "PSI-26", "1")
    assert r.outcome == "burned_out" and pd.isna(r.outcome_cause) and "burnout" in r.outcome_quote
    assert row(table, "PSI-26", "95").outcome == "no_ignition"
    assert pd.isna(row(table, "PSI-26", "42").outcome)  # "2 minute burn": a duration, not an ending


def test_an_outcome_whose_quote_left_the_source_is_refused():
    rows = {"PSI-26": [{"test_id": "1", "source_row": 2, "extra": {"asrun_notes": "Burned to completion."}}]}
    item = {"accession": "PSI-26", "test_id": "1", "source_row": 2, "outcome": "burned_out", "cause": None,
            "field": "asrun_notes", "quote": "Burned to  completion."}
    bt.apply_outcomes(rows, [item])
    assert rows["PSI-26"][0]["outcome"] == "burned_out"
    with pytest.raises(ValueError, match="quote"):
        bt.apply_outcomes(rows, [{**item, "quote": "went out"}])
    with pytest.raises(ValueError, match="cause"):
        bt.apply_outcomes(rows, [{**item, "cause": "blowoff"}])
