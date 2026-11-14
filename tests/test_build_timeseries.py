import numpy as np
import pandas as pd
import pytest

from fif import psi
from fif.pipeline import build_timeseries as bt
from fif.pipeline.build_timeseries import (
    elapsed_s, features, flame_window, load_timeseries, parse_timeline, read_acme, type_b_c, type_k_c,
)

COLUMNS = ("Time,MFCA1StaticMixerFlow,MFCA2BypassFlow,MFCA3FuelFlow,IonCurrent,PTA1,PTA2,PTA3,EfieldVoltage,"
           "PMT1,PMT2,PMT3,TCA,TCB,TCC,TCD,TC200A,TC200B,TCBurner,Radiometer+60,Radiometer+60CJ,Radiometer+30,"
           "Radiometer+30CJ,RadiometerCenter,RadiometerCenterCJ,Radiometer-30,Radiometer-30CJ,Radiometer-60,"
           "Radiometer-60CJ,RadiometerOffset,RadiometerOffsetCJ,TCE,Ch20,Ch21,TCCJ,EfieldSetpointOut")
HEADER = ("2019-09-11 254 23:59:58:000 ,Experiment: 2,Test Point: 19254A1,MFCA1 Gas: 0,MFCA1 Full Scale: 20.000000,"
          "MFCA2 Gas: 0,MFCA2 Full Scale: 0.500000,MFCA3 Gas: 4,MFCA3 Full Scale: 0.500000,EField: 0,EFieldPol: 0,"
          "Igniter: 0,Burner: 3,Thermocouple: 2,Radiometer: 0,IPSU 1: 0,IPSU 2: 0,IPSU 3: 0,IPSU 4: 0,IPSU 5: 1,"
          "IPSU 6: 0,Fiber: 0,PMT 1 Gain: 5.000000,PMT 2 Gain: 3.000000,PMT 3 Gain: 4.000000")


def acme_row(clock, fuel_v=2.5, pta3_v=1.2, tc_burner_v=0.0, rad_center_v=1.36, tccj_v=0.874):
    values = dict.fromkeys(COLUMNS.split(",")[1:], 0.0)
    values.update({"MFCA3FuelFlow": fuel_v, "PTA3": pta3_v, "TCBurner": tc_burner_v,
                   "RadiometerCenter": rad_center_v, "TCCJ": tccj_v})
    return clock + "," + ",".join(str(v) for v in values.values())


@pytest.fixture
def acme_csv(tmp_path):
    rows = [acme_row("23:59:59:992"), acme_row("00:00:00:000", tc_burner_v=0.004096),
            acme_row("00:00:00:008")[:40] + "\x00" * 30, acme_row("00:00:00:016")]
    path = tmp_path / "PSI-23_Raw Data_19254A1_data.csv"
    path.write_text("\n".join([HEADER, COLUMNS, *rows]) + "\n", encoding="latin-1")
    return path


def test_thermocouple_conversions_match_nist_reference_points():
    assert type_k_c([4.096, 20.644, 41.276], [0, 0, 0]) == pytest.approx([100, 500, 1000], abs=0.1)
    assert type_k_c(0.0, 25.0) == pytest.approx(25.0, abs=0.1)
    assert type_b_c([4.834, 10.099], [0, 0]) == pytest.approx([1000, 1500], abs=0.1)
    assert np.isnan(type_k_c(-10.0, 25.0)) and np.isnan(type_b_c(0.1, 25.0))


def test_read_acme_converts_volts_and_drops_truncated_rows(acme_csv):
    header, df = read_acme(acme_csv)
    assert header["Test Point"] == "19254A1" and header["MFCA3 Full Scale"] == 0.5
    assert header["dropped_lines"] == 1
    assert df["time_s"].tolist() == pytest.approx([0, 0.008, 0.024])
    assert df["fuel_flow_slpm"].iloc[0] == pytest.approx(0.25)
    assert df["chamber_pressure_kpa"].iloc[0] == pytest.approx(0.7 * 14.5038 * 10 / 4 * 6.894757)
    assert df["cold_junction_temp_c"].iloc[0] == pytest.approx(23.12, abs=0.01)
    assert df["burner_temp_c"].iloc[1] == pytest.approx(122.4, abs=0.2)  # E(T) = 4.096 mV + E(23.1 °C)
    assert df["radiometer_center_w_cm2"].iloc[0] == pytest.approx(0.002894 * 1.36 - 0.003932)
    assert "rake_a_temp_c" not in df


def test_elapsed_s_unwraps_midnight():
    clock = pd.Series(["23:59:59:990", "23:59:59:998", "00:00:00:006"])
    assert elapsed_s(clock) == pytest.approx([0, 0.008, 0.016])


def synthetic_burn(flame_s, hz=125.0, spike=True):
    """CFI-G-style low-gain radiometer: igniter glow, an ignition spike, then a weaker steady flame."""
    t = np.arange(0, 60, 1 / hz)
    v = np.full_like(t, -0.03)
    v[(t >= 20) & (t < 21)] += 0.2
    if flame_s:
        v[(t >= 22) & (t < 22 + flame_s)] += 0.8
        if spike:
            v[(t >= 22) & (t < 22.5)] += 4.0
    return pd.DataFrame({"time_s": t, "radiometer3_p30_lo_v": v, "radiometer3_m10_lo_v": v / 2,
                         "radiometer3_p60_lo_v": v / 3})


def test_flame_window_ignores_ignition_spike_and_floor():
    df = synthetic_burn(30)
    ign, out, threshold = flame_window(df["time_s"], df.drop(columns="time_s"), floor=0.05)
    assert ign == pytest.approx(22, abs=0.15) and out == pytest.approx(52, abs=0.15)
    assert 0.05 < threshold < 0.8
    flat = synthetic_burn(0)
    flat.iloc[:, 1:] = -0.03
    assert flame_window(flat["time_s"], flat.drop(columns="time_s"), floor=0.05) == (None, None, None)


def test_features_burn_duration_and_igniter_glow_is_not_a_flame():
    burn = features({}, synthetic_burn(30))
    assert burn["flame_detected"] and burn["burn_duration_s"] == pytest.approx(30, abs=0.3)
    assert burn["radiometer3_p30_lo_peak_v"] == pytest.approx(4.77, abs=0.01)
    glow = features({}, synthetic_burn(0))
    assert not glow["flame_detected"] and glow["burn_duration_s"] == 0
    assert 0 < glow["radiometer_on_s"] < 2


def test_parse_timeline():
    text = "\nTest Point: 21228A1\n\nScript start: 2021-08-16 17:29:23\nPreheat igniter: ***\n"
    events = parse_timeline(text)
    assert events["Script start"] == pd.Timestamp("2021-08-16 17:29:23")
    assert events["Preheat igniter"] is None


def test_load_timeseries_real_file():
    table = psi.PROCESSED / "timeseries_features.parquet"
    if not table.exists():
        pytest.skip("timeseries_features not built")
    feats = pd.read_parquet(table)
    row = feats[feats["test_point"] == "21228A1"]
    if row.empty or not (psi.ROOT / row["source_file"].iloc[0]).exists():
        pytest.skip("raw data absent")
    df = load_timeseries(row["test_id"].iloc[0])
    assert set(df["test_point"]) == {"21228A1"}
    assert len(df) == row["n_samples"].iloc[0]
    assert df["burner_temp_c"].max() == pytest.approx(row["burner_temp_max_c"].iloc[0])
    assert {"time_s", "chamber_pressure_kpa", "fuel_flow_slpm", "radiometer3_p30_lo_v"} <= set(df.columns)


@pytest.fixture(scope="module")
def built():
    path = psi.PROCESSED / "timeseries_features.parquet"
    if not path.exists():
        pytest.skip("timeseries features not built")
    return pd.read_parquet(path)


def test_clipped_flag_marks_peaks_at_the_recorder_ceiling(built):
    for name, ceiling in bt.RADIOMETER_CLIP.items():
        peak, clipped = built[f"{name}_peak_w_cm2"], built[f"{name}_clipped"]
        assert peak.max() <= ceiling * 1.005
        assert (clipped[peak.notna()].astype(bool) == (peak[peak.notna()] >= bt.CLIP_MARGIN * ceiling)).all()
    assert built["radiometer_center_clipped"].sum() > 300


def test_burn_window_flow_maximum_excludes_pre_ignition_spikes(built):
    both = built.dropna(subset=["fuel_flow_max_burn_slpm"])
    assert (both["fuel_flow_max_burn_slpm"] <= both["fuel_flow_max_slpm"] + 1e-9).all()
    assert (both["fuel_flow_max_burn_slpm"] < 0.7 * both["fuel_flow_max_slpm"]).sum() > 50


def test_timeline_is_found_by_the_test_point_written_inside_it(built):
    note = built.loc[built["test_point"] == "19189K1", "features_note"].iloc[0]
    assert "no _TP.txt" not in str(note)
    assert built.loc[built["test_point"] == "19189K1", "script_ignition_s"].notna().all()
    assert not built.isna().all().any()


def test_reduced_cfi_files_are_read_as_published_and_problems_are_named(tmp_path):
    base = tmp_path / "PSI-39_Raw Data_FLEX-9999_DropletData.txt"
    base.write_text("DropletTime_sec\tDropletDiameter_mm\r-1.0\t4.0\r0.0\t3.9\r1.0\t0\r")  # CR line ends, as in PSI
    base.with_name(base.name.replace("Droplet", "ColorCam")).write_text(
        "CoolFlameTime_s\tCoolFlameDiameterFWHM_mm\tCoolFlameDiameterP2P_mm\n0.5\t11.0\t0.2\n")  # misnamed file
    base.with_name(base.name.replace("Droplet", "Radiometer")).write_bytes(b"%PDF-1.3 not a table")
    parts, problems = bt.read_cfi_reduced_parts(base)
    assert set(parts) == {"DropletData", "ColorCamData"}
    assert any("PDF" in p for p in problems) and any("ColorCamData file holds other columns" in p for p in problems)
    df = bt.read_cfi_reduced(base)[1]
    assert list(df["time_s"]) == [-1.0, 0.0, 0.5, 1.0]
    assert list(df["droplet_diameter_mm"].dropna()) == [4.0, 3.9, 0.0]  # the zero stays: it is in the source
    assert df["cool_flame_fwhm_mm"].notna().sum() == 1

    base.with_name(base.name.replace("Droplet", "Radiometer")).write_text(
        "RadiometerTime_sec\tTotalWideBandPower_W\tTotalNarrowBandPower_W\n0.0\t-5.4e6\t0.1\n0.01\t-5.4e6\t8.0\n")
    row = {"accession": "PSI-39", "test_id": "9999", "test_point": "FLEX-9999-reduced", "source_file": str(base)}
    f = bt.cfi_reduced_features(row)
    assert f["droplet_diameter_first_mm"] == 4.0 and f["droplet_diameter_min_mm"] == 3.9
    assert f["narrow_band_power_max_w"] == 8.0 and "not physical" in f["features_note"]
    assert "narrow_band_power_w" in bt.read_cfi_reduced(base)[1] and "TotalWideBandPower_W" not in bt.read_cfi_reduced(base)[1]


def test_reduced_recordings_join_the_24_cfi_tests(built):
    reduced = built[built["test_point"].str.endswith(bt.CFI_REDUCED_SUFFIX)]
    assert len(reduced) == 24 and set(reduced["accession"]) == {"PSI-39"} and reduced["test_id"].is_unique
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet")
    tests = tests[tests["accession"] == "PSI-39"].set_index("test_id")
    both = reduced.set_index("test_id").join(tests[["burn_time_s", "d0_mm"]]).dropna(subset=["hot_flame_last_s", "burn_time_s"])
    # the published curves agree with the investigators' own summary table: time zero is ignition
    assert len(both) >= 20 and ((both["hot_flame_last_s"] - both["burn_time_s"]).abs() < 0.5).mean() > 0.9
