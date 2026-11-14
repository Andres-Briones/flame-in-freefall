"""`timeseries_features` table: one row per raw per-test time-series file that joins to a `tests` row, with
summary features in engineering units:

- ACME 125 Hz `*_data.csv` (PSI-10, PSI-23, PSI-159). Raw volts are converted with ACME-DOC-010 Rev D,
  section 10 (PSI-23 Reference Data).
- CFI `<CIR>_Radiometer_Readings.txt` + `<CIR>_Chamber_Readings.txt` (PSI-39), joined on the CIR code.
- Saffire-I / III per-sample sensor workbooks (PSI-98, PSI-100), sheet `Calibrated Data` (slow to load: xlsx).

`load_timeseries(test_id)` returns one test's signals as a tidy DataFrame. See docs/formats.md.

Run: uv run python -m fif.pipeline.build_timeseries
"""
import io
import json
import re
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from fif import psi

ACME = ("PSI-10", "PSI-23", "PSI-159")
DATA_FILE = re.compile(r"_(\d{5}[A-Z]\d+)(_\d+)?_data\.csv$")
ROW_START = re.compile(r"\d{1,2}:\d{2}:\d{2}:\d{1,3},")
CFI = "PSI-39"
CFI_FILE = re.compile(r"_(F\d{3}[A-Z]\d{2})_Radiometer_Readings\.txt$")
CFI_SAMPLES_PER_ROW = 100
# The investigators' reduced per-test data of 24 CFI tests: small tab-separated tables, each on its own time axis.
CFI_REDUCED_FILE = re.compile(r"_FLEX-(\d{4})_DropletData\.txt$")
CFI_REDUCED_KINDS = ("DropletData", "ColorCamData", "CoolFlameData", "RadiometerData")
CFI_REDUCED_TIME = ("DropletTime_sec", "ColorCamTime_sec", "CoolFlameTime_s", "RadiometerTime_sec")
CFI_REDUCED_COLUMNS = {
    "DropletDiameter_mm": "droplet_diameter_mm", "ZeroedDropletXpos_mm": "droplet_x_mm",
    "ZeroedDropletYpos_mm": "droplet_y_mm", "ColorCamFlameDiameter_mm": "flame_diameter_mm",
    "ColorCamFlameStandoff": "flame_standoff", "CoolFlameDiameterFWHM_mm": "cool_flame_fwhm_mm",
    "CoolFlameDiameterP2P_mm": "cool_flame_p2p_mm", "TotalNarrowBandPower_W": "narrow_band_power_w",
}
# About -5.4e6 "W" in every file: not a power. Left out of the series and named in the notes.
CFI_REDUCED_DROPPED = ("TotalWideBandPower_W",)
CFI_REDUCED_SUFFIX = "-reduced"
CFI_SAMPLE_HZ = 100
SAFFIRE = ("PSI-98", "PSI-100")
SAFFIRE_FILE = re.compile(r"Sample (\d+) Sensor")
SAFFIRE_BASELINE_S = 50.0
SAFFIRE_COLUMNS = {
    "Elapsed Time (s)": "time_s", "Epoch Time": "epoch_ms", "CO2": "co2_pct", "O2": "o2_pct",
    "Anemometer 1": "anemometer_1_cm_s", "Anemometer 2": "anemometer_2_cm_s", "Ambient Pressure": "ambient_pressure_psia",
    **{f"Radiometer {k}": f"radiometer_{k}_mw_cm2" for k in range(1, 5)},
    "Humidity": "humidity_pct", "Test Section Inlet Temp": "inlet_temp_c",
    **{f"Plume Temp {k} (TC{k})": f"plume_temp_{k}_c" for k in range(1, 7)},
    **{f"Sample Temp {k} (TC{k + 6})": f"sample_temp_{k}_c" for k in range(1, 7)},
    "Igniter Current": "igniter_current_a", "Igniter Voltage": "igniter_voltage_v",
}
TEST_DAY_ACCESSIONS = {"PSI-23"}

SAMPLE_HZ_NOMINAL = 125
BASELINE_S = 2.0
FINAL_S = 1.0
SMOOTH_S = 0.2
FLAME_ON_FRACTION = 0.4
FLAME_LEVEL_QUANTILE = 0.9
# Igniter glow alone lasts up to ~2 s on the radiometers, so shorter on-times are not counted as a flame.
MIN_BURN_S = 2.0
# About 1% of each array's full-scale reading (standard array saturates near 0.0105 W/cm2,
# CFI-G low-gain channels near 4.8 V); far above baseline noise (~4e-7 W/cm2, ~3e-4 V).
FLAME_FLOOR = {"standard": 1e-4, "cfi-g": 0.05}

PSI_PER_V = 14.5038 * 10 / 4
KPA_PER_PSI = 6.894757

# ACME-DOC-010 Rev D 10.2.20-10.2.30: irradiance (W/cm2) = a * V + b
RADIOMETER_STD = {
    "Radiometer+60": ("radiometer_p60", 0.002622, -0.003370),
    "Radiometer+30": ("radiometer_p30", 0.001794, -0.002309),
    "RadiometerCenter": ("radiometer_center", 0.002894, -0.003932),
    "Radiometer-30": ("radiometer_m30", 0.002397, -0.003077),
    "Radiometer-60": ("radiometer_m60", 0.002591, -0.003300),
    "RadiometerOffset": ("radiometer_offset", 0.001798, -0.002307),
}
# The recorder saturates near 4.87 V, so each standard-array channel clips at its own irradiance: the highest
# value any file reaches (W/cm2). A peak within 1% of it is a lower bound, not a measurement.
RADIOMETER_CLIP = {"radiometer_p60": 0.00940, "radiometer_p30": 0.00644, "radiometer_center": 0.01012,
                   "radiometer_m30": 0.00859, "radiometer_m60": 0.00931, "radiometer_offset": 0.00646}
CLIP_MARGIN = 0.99
# CFI-G dual-gain array: its characterisation report (CIR-RPT-4600) is not in PSI, so the channels stay in volts.
RADIOMETER_CFIG = {
    "Radiometer3+60LoGain": "radiometer3_p60_lo",
    "Radiometer3+60HiGain": "radiometer3_p60_hi",
    "Radiometer3+30LoGain": "radiometer3_p30_lo",
    "Radiometer3+30HiGain": "radiometer3_p30_hi",
    "Radiometer3-10LoGain": "radiometer3_m10_lo",
    "Radiometer3-10HiGain": "radiometer3_m10_hi",
}
FLAME_CHANNELS = {
    "standard": [f"{n}_w_cm2" for c, (n, _, _) in RADIOMETER_STD.items() if c != "RadiometerOffset"],
    "cfi-g": [f"{n}_v" for n in RADIOMETER_CFIG.values() if n.endswith("_lo")],
}
THERMOCOUPLES = {
    "TCBurner": ("burner_temp", "K"),
    "TC200A": ("ambient_200mm_a_temp", "K"),
    "TC200B": ("ambient_200mm_b_temp", "K"),
    "TCA": ("rake_a_temp", "K"),
    "TCB": ("rake_b_temp", "B"),
    "TCC": ("rake_c_temp", "B"),
    "TCD": ("rake_d_temp", "K"),
}
FLOWS = {
    "MFCA1StaticMixerFlow": ("oxidizer_flow", "MFCA1 Full Scale"),
    "MFCA2BypassFlow": ("inert_flow", "MFCA2 Full Scale"),
    "MFCA3FuelFlow": ("fuel_flow", "MFCA3 Full Scale"),
}
PMTS = {"PMT1": "pmt1_310nm", "PMT2": "pmt2_broadband_uv", "PMT3": "pmt3_430nm"}
PRESSURES = {"PTA1": "inner_coflow_pressure", "PTA2": "outer_coflow_pressure", "PTA3": "chamber_pressure"}

# ACME-DOC-010 Rev D Table 34 (codes above these ranges were used later and are not documented there).
OXIDIZER_GAS = {0: "O2/N2 21/79", 1: "O2/N2 30/70", 2: "O2/N2 40/60", 3: "O2/N2 85/15", 4: "O2/He 30/70"}
INERT_GAS = {0: "N2", 1: "He"}
FUEL_GAS = {
    0: "CH4", 1: "CH4/N2 30/70", 2: "CH4/N2 40/60", 3: "CH4/N2 45/55", 4: "C2H4", 5: "C2H4/N2 30/70",
    6: "C2H4/N2 50/50", 7: "H2", 8: "H2/CH4 44.4/55.6", 9: "H2/CH4 55.6/44.4", 10: "H2/CH4 66.7/33.3",
    11: "H2/CH4/He 20/25/55", 12: "H2/CH4/He 25/20/55", 13: "H2/CH4/He 30/15/55", 14: "H2/He 45/55",
    15: "CH4/He 45/55", 16: "C2H4/He 20/80", 17: "C2H4/He 25/75", 18: "C2H4/He 30/70",
}
RAKE = {0: "near", 1: "far", 2: "removed"}
SCRIPT_EVENTS = {"Ignition and retraction": "script_ignition_s", "Extinction detected": "script_extinction_detected_s",
                 "MFCs off": "script_mfcs_off_s"}

K_CJ = [-0.176004136860e-01, 0.389212049750e-01, 0.185587700320e-04, -0.994575928740e-07,
        0.318409457190e-09, -0.560728448890e-12, 0.560750590590e-15, -0.320207200030e-18,
        0.971511471520e-22, -0.121047212750e-25]
K_A = (0.118597600000e00, -0.118343200000e-03, 0.126968600000e03)
K_LOW = [0.0, 25.08355, 0.07860106, -0.2503131, 0.08315270, -0.01228034, 0.0009804036,
         -0.00004413030, 0.000001057734, -0.00000001052755]
K_HIGH = [-131.8058, 48.30222, -1.646031, 0.05464731, -0.0009650715, 0.000008802193, -0.00000003110810]
B_CJ = [0.0, -0.246508183460e-03, 0.590404211710e-05, -0.132579316360e-08, 0.156682919010e-11,
        -0.169445292400e-14, 0.629903470940e-18]
B_LOW = [98.423321, 699.71500, -847.65304, 1005.2644, -833.45952, 455.08542, -155.23037, 29.886750, -2.4742860]
B_HIGH = [213.15071, 285.10504, -52.742887, 9.9160804, -1.2965303, 0.11195870, -0.0060625199,
          0.00018661696, -0.0000024878585]


def _poly(coefs, x):
    return np.polynomial.polynomial.polyval(x, coefs)


def type_k_c(tc_mv, cj_c):
    """Type K temperature (°C) from thermocouple EMF (mV) and cold-junction temperature (°C).
    NaN outside 0-54.886 mV total EMF (the document's validity range)."""
    cj_c = np.asarray(cj_c, dtype=float)
    cj_mv = _poly(K_CJ, cj_c) + K_A[0] * np.exp(K_A[1] * (cj_c - K_A[2]) ** 2)
    mv = np.asarray(tc_mv, dtype=float) + cj_mv
    t = np.where(mv <= 20.644, _poly(K_LOW, mv), _poly(K_HIGH, mv))
    return np.where((mv >= 0) & (mv <= 54.886), t, np.nan)


def type_b_c(tc_mv, cj_c):
    """Type B temperature (°C); NaN outside 0.291-13.820 mV total EMF (below about 250 °C)."""
    mv = np.asarray(tc_mv, dtype=float) + _poly(B_CJ, np.asarray(cj_c, dtype=float))
    t = np.where(mv <= 2.431, _poly(B_LOW, mv), _poly(B_HIGH, mv))
    return np.where((mv >= 0.291) & (mv <= 13.820), t, np.nan)


def parse_header(line):
    """First line of an ACME data file: `<date> <gmt day> <hh:mm:ss:ms> ,Key: value,...`."""
    fields = [f.strip() for f in line.strip().split(",") if f.strip()]
    head = {}
    stamp = fields[0].split()
    if len(stamp) == 3:
        head["start_date"], head["gmt_day"], head["start_time"] = stamp
    for f in fields[1:]:
        key, _, value = f.partition(":")
        value = value.strip()
        try:
            head[key.strip()] = float(value)
        except ValueError:
            head[key.strip()] = value
    return head


def clock_s(clock):
    parts = clock.str.split(":", expand=True).astype(float)
    return (parts[0] * 3600 + parts[1] * 60 + parts[2] + parts[3] / 1000).to_numpy()


def elapsed_s(clock):
    """`HH:MM:SS:mmm` strings to seconds since the first sample, unwrapping midnight."""
    s = clock_s(clock)
    s = s + 86400 * np.cumsum(np.r_[0, np.diff(s) < -43200])
    return s - s[0]


def read_acme_raw(path):
    """Header dict and raw-volt DataFrame (`time_s` first) of one ACME `_data.csv`.
    Truncated or NUL-padded rows are dropped and counted in `header["dropped_lines"]`."""
    lines = Path(path).read_text(encoding="latin-1").replace("\x00", "").splitlines()
    header = parse_header(lines[0])
    n_commas = lines[1].count(",")
    body = [ln for ln in lines[2:] if ln.strip()]
    good = [ln for ln in body if ln.count(",") == n_commas and ROW_START.match(ln)]
    header["dropped_lines"] = len(body) - len(good)
    raw = pd.read_csv(io.StringIO("\n".join(lines[1:2] + good)), dtype={"Time": str})
    raw = raw.loc[:, [c for c in raw.columns if not c.startswith("Unnamed")]]
    for c in raw.columns.drop("Time"):
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    header["first_clock"] = raw["Time"].iloc[0] if len(raw) else None
    raw.insert(0, "time_s", elapsed_s(raw.pop("Time")))
    return header, raw


def radiometer_array(df):
    if any(c in df for c in FLAME_CHANNELS["cfi-g"]):
        return "cfi-g"
    if any(c in df for c in FLAME_CHANNELS["standard"]):
        return "standard"
    return None


def to_engineering(header, raw):
    """Raw volts to named channels with units in the names (ACME-DOC-010 Rev D, section 10)."""
    out = {"time_s": raw["time_s"].to_numpy()}
    for col, (name, scale_key) in FLOWS.items():
        scale = header.get(scale_key)
        if col in raw and isinstance(scale, float):
            out[f"{name}_slpm"] = raw[col].to_numpy() / 5.0 * scale
    for col, name in PRESSURES.items():
        if col in raw:
            out[f"{name}_kpa"] = (raw[col].to_numpy() - 0.5) * PSI_PER_V * KPA_PER_PSI
    if "TCCJ" in raw:
        cj = 338.98305 * raw["TCCJ"].to_numpy() - 273.15
        out["cold_junction_temp_c"] = cj
        rake_installed = header.get("Thermocouple") in (0.0, 1.0)
        for col, (name, kind) in THERMOCOUPLES.items():
            if col not in raw or (name.startswith("rake") and not rake_installed):
                continue
            mv = raw[col].to_numpy() * 1000
            out[f"{name}_c"] = type_k_c(mv, cj) if kind == "K" else type_b_c(mv, cj)
    for col, name in PMTS.items():
        if col in raw:
            out[f"{name}_v"] = raw[col].to_numpy()
    for col, (name, a, b) in RADIOMETER_STD.items():
        if col in raw:
            out[f"{name}_w_cm2"] = a * raw[col].to_numpy() + b
    for col, name in RADIOMETER_CFIG.items():
        if col in raw:
            out[f"{name}_v"] = raw[col].to_numpy()
    if "IonCurrent" in raw:
        out["ion_current_ua"] = 1000 * raw["IonCurrent"].to_numpy() / 162
    return pd.DataFrame(out)


def read_acme(path):
    header, raw = read_acme_raw(path)
    return header, to_engineering(header, raw)


def smooth(series, hz):
    return series.rolling(max(1, round(SMOOTH_S * hz)), center=True, min_periods=1).median()


def flame_window(time_s, signals, floor):
    """Burn interval from radiometer signals (DataFrame, one column per channel).

    Rule: each channel is median-smoothed over 0.2 s and its pre-ignition baseline (median of the first 2 s) is
    subtracted; the flame signal is the maximum over channels. With `level` = the 90th percentile of the flame
    signal over the samples above `floor`, the flame is on where the signal exceeds
    max(floor, 0.4 * level). Ignition = first on-sample, flame-out = last on-sample.
    Returns (ignition_s, flameout_s, threshold) or (None, None, None) when nothing exceeds the floor."""
    t = np.asarray(time_s)
    hz = 1 / np.median(np.diff(t)) if len(t) > 1 else SAMPLE_HZ_NOMINAL
    sm = signals.apply(smooth, hz=hz)
    base = sm[t < BASELINE_S].median()
    sig = (sm - base).max(axis=1).to_numpy()
    above = sig[sig > floor]
    if not len(above):
        return None, None, None
    threshold = max(floor, FLAME_ON_FRACTION * np.quantile(above, FLAME_LEVEL_QUANTILE))
    on = np.flatnonzero(sig > threshold)
    return float(t[on[0]]), float(t[on[-1]]), float(threshold)


def parse_timeline(text):
    """`_TP.txt` test-point timeline: {event label: datetime or None for `***`}."""
    events = {}
    for line in text.splitlines():
        m = re.match(r"\s*([A-Za-z][^:]*?):\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\*\*\*)\s*$", line)
        if m:
            value = m.group(2)
            events[m.group(1)] = None if value == "***" else datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return events


def first_sample_time(header):
    date, clock = header.get("start_date"), header.get("first_clock")
    if not date or not clock:
        return None
    h, m, s, ms = (int(x) for x in clock.split(":"))
    start = datetime.strptime(date, "%Y-%m-%d") + timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)
    head_h = int(header.get("start_time", "0").split(":")[0])
    return start + timedelta(days=1) if h < head_h - 12 else start


def _window(df, t0, t1):
    return df[(df["time_s"] >= t0) & (df["time_s"] <= t1)]


def _num(x):
    return float(x) if x is not None and np.isfinite(x) else np.nan


def channel_features(df, col, prefix, unit, burn, hz):
    s = df[col]
    if s.notna().sum() == 0:
        return {}
    sm = smooth(s, hz)
    t = df["time_s"]
    i = sm.idxmax()
    out = {
        f"{prefix}_peak_{unit}": _num(sm[i]),
        f"{prefix}_time_of_peak_s": _num(t[i]),
        f"{prefix}_final_{unit}": _num(s[t >= t.iloc[-1] - FINAL_S].median()),
    }
    out[f"{prefix}_mean_burn_{unit}"] = _num(_window(df, *burn)[col].mean()) if burn else np.nan
    return out


def features(header, df, timeline=None):
    """Summary features of one converted data file (see docs/formats.md for the column list)."""
    t = df["time_s"]
    hz = 1 / np.median(np.diff(t)) if len(t) > 1 else np.nan
    start = df[t < BASELINE_S]
    end = df[t >= t.iloc[-1] - FINAL_S]
    array = radiometer_array(df)
    f = {
        "n_samples": len(df),
        "duration_s": _num(t.iloc[-1]),
        "sample_hz": _num(hz),
        "first_sample_utc": first_sample_time(header),
        "experiment_code": header.get("Experiment"),
        "burner_code": header.get("Burner"),
        "oxidizer_gas": OXIDIZER_GAS.get(header.get("MFCA1 Gas"), _code(header.get("MFCA1 Gas"))),
        "inert_gas": INERT_GAS.get(header.get("MFCA2 Gas"), _code(header.get("MFCA2 Gas"))),
        "fuel_gas": FUEL_GAS.get(header.get("MFCA3 Gas"), _code(header.get("MFCA3 Gas"))),
        "thermocouple_rake": RAKE.get(header.get("Thermocouple")),
        "pmt1_gain_v": header.get("PMT 1 Gain"),
        "pmt2_gain_v": header.get("PMT 2 Gain"),
        "pmt3_gain_v": header.get("PMT 3 Gain"),
        "radiometer_array": array,
    }
    ign = out = thr = None
    if array:
        cols = [c for c in FLAME_CHANNELS[array] if c in df]
        ign, out, thr = flame_window(t, df[cols], FLAME_FLOOR[array])
    f["radiometer_on_s"] = _num(out - ign) if ign is not None else (0.0 if array else np.nan)
    f["flame_detected"] = bool(f["radiometer_on_s"] >= MIN_BURN_S) if array else None
    burn = (ign, out) if f["flame_detected"] else None
    f["ignition_time_s"] = _num(ign) if burn else np.nan
    f["flameout_time_s"] = _num(out) if burn else np.nan
    f["burn_duration_s"] = _num(out - ign) if burn else (0.0 if array else np.nan)
    f["flame_threshold"] = _num(thr)

    if timeline is not None and f["first_sample_utc"] is not None:
        for label, name in SCRIPT_EVENTS.items():
            when = timeline.get(label)
            f[name] = (when - f["first_sample_utc"]).total_seconds() if when else np.nan

    if "chamber_pressure_kpa" in df:
        p = df["chamber_pressure_kpa"]
        f["chamber_pressure_start_kpa"] = _num(start["chamber_pressure_kpa"].median())
        f["chamber_pressure_end_kpa"] = _num(end["chamber_pressure_kpa"].median())
        f["chamber_pressure_max_kpa"] = _num(smooth(p, hz).max())
        f["chamber_pressure_mean_burn_kpa"] = _num(_window(df, *burn)["chamber_pressure_kpa"].mean()) if burn else np.nan
    if "cold_junction_temp_c" in df:
        f["cold_junction_temp_mean_c"] = _num(df["cold_junction_temp_c"].mean())
    if "burner_temp_c" in df:
        b = df["burner_temp_c"]
        f["burner_temp_start_c"] = _num(start["burner_temp_c"].median())
        f["burner_temp_max_c"] = _num(b.max())
        f["burner_temp_time_of_max_s"] = _num(t[b.idxmax()]) if b.notna().any() else np.nan
        f["burner_temp_final_c"] = _num(end["burner_temp_c"].median())
    for name in ("ambient_200mm_a_temp", "ambient_200mm_b_temp"):
        if f"{name}_c" in df:
            f[f"{name}_max_c"] = _num(df[f"{name}_c"].max())
            f[f"{name}_final_c"] = _num(end[f"{name}_c"].median())
    for name in ("rake_a_temp", "rake_b_temp", "rake_c_temp", "rake_d_temp"):
        if f"{name}_c" in df:
            f[f"{name}_max_c"] = _num(df[f"{name}_c"].max())
    for name, _ in FLOWS.values():
        col = f"{name}_slpm"
        if col in df:
            # whole-file maximum: often a 9.99 V controller spike before ignition, above the controller's range
            f[f"{name}_max_slpm"] = _num(smooth(df[col], hz).max())
            f[f"{name}_max_burn_slpm"] = _num(smooth(df[col], hz)[(t >= burn[0]) & (t <= burn[1])].max()) if burn else np.nan
            f[f"{name}_mean_burn_slpm"] = _num(_window(df, *burn)[col].mean()) if burn else np.nan
    for name in PMTS.values():
        col = f"{name}_v"
        if col in df:
            w = _window(df, *burn)[col] if burn else pd.Series(dtype=float)
            f[f"{name}_mean_burn_v"] = _num(w.mean()) if len(w) else np.nan
            f[f"{name}_max_burn_v"] = _num(w.max()) if len(w) else np.nan
    for _, (name, _, _) in RADIOMETER_STD.items():
        if f"{name}_w_cm2" in df:
            f.update(channel_features(df, f"{name}_w_cm2", name, "w_cm2", burn, hz))
            peak = f.get(f"{name}_peak_w_cm2")
            if peak is not None and np.isfinite(peak):
                f[f"{name}_clipped"] = bool(peak >= CLIP_MARGIN * RADIOMETER_CLIP[name])
    for name in RADIOMETER_CFIG.values():
        if f"{name}_v" in df:
            f.update(channel_features(df, f"{name}_v", name, "v", burn, hz))
    return f


def _code(value):
    return f"code {int(value)}" if isinstance(value, float) else None


def data_files():
    """ACME `_data.csv` files with their test point and the `tests` row they join to (None if none)."""
    files = pd.read_csv(psi.PROCESSED / "files.csv")
    files = files[files["accession"].isin(ACME) & files["downloaded"].astype(bool)]
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet")
    tests = tests[tests["accession"].isin(ACME)]
    lookup = {(a, tid.replace(" ", "")): tid for a, tid in zip(tests["accession"], tests["test_id"])}
    rows = []
    for acc, name, path in zip(files["accession"], files["file_name"], files["local_path"]):
        m = DATA_FILE.search(name)
        if not m:
            continue
        base, point = m.group(1), m.group(1) + (m.group(2) or "")
        key = base[:5] if acc in TEST_DAY_ACCESSIONS else base
        test_id = lookup.get((acc, point)) or lookup.get((acc, key))
        rows.append({"accession": acc, "test_id": test_id, "test_point": point,
                     "reopened": bool(m.group(2)), "source_file": path})
    return pd.DataFrame(rows)


@lru_cache(maxsize=None)
def _timelines_by_test_point(folder):
    """Test point named inside each `_TP.txt` of a folder -> file. A few timelines are filed under another name
    (19189K1 is in `...19189JK1_TP.txt`)."""
    found = {}
    for path in sorted(Path(folder).glob("*_TP.txt")):
        m = re.search(r"Test Point:\s*(\S+)", path.read_text(encoding="latin-1")[:400])
        if m:
            found.setdefault(m.group(1), path)
    return found


def timeline_path(source_file, test_point=None):
    p = psi.ROOT / source_file
    by_name = p.with_name(p.name[: -len("_data.csv")] + "_TP.txt")
    if by_name.exists() or test_point is None:
        return by_name
    return _timelines_by_test_point(str(p.parent)).get(test_point, by_name)


def file_features(row):
    path = psi.ROOT / row["source_file"]
    notes = []
    try:
        header, df = read_acme(path)
    except Exception as e:
        return {**row, "features_note": f"parse failed: {type(e).__name__}: {e}"}
    tp = timeline_path(row["source_file"], row["test_point"])
    timeline = parse_timeline(tp.read_text(encoding="latin-1")) if tp.exists() else None
    if timeline is None:
        notes.append("no _TP.txt timeline")
    if header.get("dropped_lines"):
        notes.append(f"{header['dropped_lines']} malformed rows dropped (truncated/NUL-padded)")
    if row["reopened"]:
        notes.append("re-opened test point (file name suffix _1); the test point also has a file without the suffix")
    if header.get("Test Point") and str(header["Test Point"]) != row["test_point"]:
        notes.append(f"header test point {header['Test Point']} differs from file name")
    f = features(header, df, timeline)
    script = [f.get(k) for k in SCRIPT_EVENTS.values()]
    if any(x is not None and np.isfinite(x) and not -60 <= x <= f["duration_s"] + 60 for x in script):
        notes.append("_TP.txt timeline does not overlap the data (script times dropped)")
        f.update({k: np.nan for k in SCRIPT_EVENTS.values()})
    if f["sample_hz"] and abs(f["sample_hz"] - SAMPLE_HZ_NOMINAL) > 1:
        notes.append(f"sample rate {f['sample_hz']:.1f} Hz")
    gaps = np.diff(df["time_s"].to_numpy())
    if len(gaps) and gaps.max() > 1:
        notes.append(f"time gap of {gaps.max():.1f} s")
    return {**row, **f, "features_note": "; ".join(notes) or None}


def cfi_files():
    """PSI-39 radiometer files with their CIR code and the `tests` row they join to (via `extra.CIR`)."""
    files = pd.read_csv(psi.PROCESSED / "files.csv")
    files = files[(files["accession"] == CFI) & files["downloaded"].astype(bool)]
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet")
    tests = tests[tests["accession"] == CFI]
    cir = tests["extra"].map(lambda x: str(json.loads(x).get("CIR", "")).upper() if isinstance(x, str) else "")
    by_cir = tests.assign(cir=cir).groupby("cir")["test_id"].agg(list)
    rows = []
    for name, path in zip(files["file_name"], files["local_path"]):
        m = CFI_FILE.search(name)
        if m:
            ids = by_cir.get(m.group(1), [])
            rows.append({"accession": CFI, "test_id": ids[0] if len(ids) == 1 else None, "test_point": m.group(1),
                         "reopened": False, "source_file": path})
    return pd.DataFrame(rows)


def read_cfi(path):
    """CFI radiometer file (100 samples per 1 s row) expanded to 100 Hz, with the chamber file's 1 Hz readings
    attached by time (nearest earlier row). Returns (first sample datetime, DataFrame)."""
    path = Path(path)
    rad = pd.read_csv(path)
    frame = (pd.to_datetime(rad["RADIOMETER_100HZ_FRAME_TIME(GMT)"])
             + pd.to_timedelta(rad["RADIOMETER_100HZ_FRAME_MILLISECONDS(N/A)"], unit="ms"))
    n = CFI_SAMPLES_PER_ROW
    when = frame.to_numpy()[:, None] + (np.arange(n) * 1000 // CFI_SAMPLE_HZ).astype("timedelta64[ms]")[None, :]
    out = pd.DataFrame({"when": when.ravel()})
    for band in ("NARROW", "WIDE"):
        v = rad.filter(like=f"{band}_BAND_RADIOMETER_SAMPLE").to_numpy(dtype=float).ravel()
        out[f"{band.lower()}_band_radiometer_v"] = np.where((v <= -9.99) | (v >= 9.95), np.nan, v)
    out["igniter_on"] = np.repeat((rad["IGNITER_POWER_STATUS(N/A)"] == "On").to_numpy(), n)
    out["igniter_current_a"] = np.repeat(rad["IGNITER_CURRENT_MONITOR(Adc)"].to_numpy(dtype=float), n)
    chamber_path = path.with_name(path.name.replace("_Radiometer_Readings", "_Chamber_Readings"))
    if chamber_path.exists():
        ch = pd.read_csv(chamber_path)
        cols = {"FCU TimeStamp": "when"}
        cols.update({f"FCU_MP_PT{k}(PSIA)": f"pt{k}_pressure_kpa" for k in (16, 17, 28, 29)})
        cols.update({f"FCU_MP_TM{k}(Deg C)": f"chamber_tm{k}_temp_c" for k in (1, 2, 3, 4)})
        ch = ch[list(cols)].rename(columns=cols)
        ch["when"] = pd.to_datetime(ch["when"])
        for c in ch.columns[1:5]:
            ch[c] = ch[c].where(ch[c] >= 1) * KPA_PER_PSI
        out = pd.merge_asof(out.sort_values("when"), ch.sort_values("when"), on="when")
    t0 = out["when"].iloc[0]
    out.insert(0, "time_s", (out.pop("when") - t0).dt.total_seconds())
    return t0.to_pydatetime(), out


def cfi_features(row):
    try:
        t0, df = read_cfi(psi.ROOT / row["source_file"])
    except Exception as e:
        return {**row, "features_note": f"parse failed: {type(e).__name__}: {e}"}
    t = df["time_s"]
    hz = 1 / np.median(np.diff(t))
    ign = t[df["igniter_on"]]
    f = {"n_samples": len(df), "duration_s": _num(t.iloc[-1]), "sample_hz": _num(hz), "first_sample_utc": t0,
         "radiometer_array": "cfi-droplet", "script_ignition_s": _num(ign.iloc[0]) if len(ign) else np.nan}
    notes = ["burn duration not derived (radiometer on-time does not track tests.burn_time_s)"]
    if "pt16_pressure_kpa" in df:
        p = df["pt16_pressure_kpa"]
        f["chamber_pressure_start_kpa"] = _num(p[t < BASELINE_S + 1].median())
        f["chamber_pressure_end_kpa"] = _num(p[t >= t.iloc[-1] - FINAL_S - 1].median())
        f["chamber_pressure_max_kpa"] = _num(p.max())
        temps = df.filter(like="chamber_tm")
        f["chamber_gas_temp_start_c"] = _num(temps[t < BASELINE_S + 1].median().mean())
        f["chamber_gas_temp_max_c"] = _num(temps.max().max())
    else:
        notes.append("no _Chamber_Readings file")
    for band in ("narrow", "wide"):
        col = f"{band}_band_radiometer_v"
        f.update(channel_features(df, col, f"{band}_band_radiometer", "v", None, hz))
        f[f"{band}_band_radiometer_baseline_v"] = _num(df.loc[t < BASELINE_S, col].median())
    return {**row, **f, "features_note": "; ".join(notes)}


def saffire_files():
    files = pd.read_csv(psi.PROCESSED / "files.csv")
    files = files[files["accession"].isin(SAFFIRE) & files["downloaded"].astype(bool) & (files["category"] == "Raw Data")]
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet")
    known = set(zip(tests["accession"], tests["test_id"]))
    rows = []
    for acc, name, path in zip(files["accession"], files["file_name"], files["local_path"]):
        m = SAFFIRE_FILE.search(name)
        if m and name.endswith(".xlsx"):
            tid = f"S{m.group(1)}"
            rows.append({"accession": acc, "test_id": tid if (acc, tid) in known else None, "test_point": tid,
                         "reopened": False, "source_file": path})
    return pd.DataFrame(rows)


def read_saffire(path):
    """Saffire `Calibrated Data` sheet: row 1 names, row 2 units, data from row 3 (about 30 Hz).
    Returns (first sample datetime, DataFrame with `time_s` and the channels in SAFFIRE_COLUMNS)."""
    raw = pd.read_excel(path, sheet_name="Calibrated Data", header=0, skiprows=[1], engine="openpyxl",
                        usecols=lambda c: c in SAFFIRE_COLUMNS)
    df = raw.rename(columns=SAFFIRE_COLUMNS).apply(pd.to_numeric, errors="coerce").dropna(subset=["time_s"])
    df["ambient_pressure_kpa"] = df.pop("ambient_pressure_psia") * KPA_PER_PSI
    t0 = pd.to_datetime(df.pop("epoch_ms").iloc[0], unit="ms").to_pydatetime()
    return t0, df.reset_index(drop=True)


def saffire_features(row):
    try:
        t0, df = read_saffire(psi.ROOT / row["source_file"])
    except Exception as e:
        return {**row, "features_note": f"parse failed: {type(e).__name__}: {e}"}
    t = df["time_s"]
    hz = 1 / np.median(np.diff(t))
    base = df[t < SAFFIRE_BASELINE_S]
    igniter = df["igniter_current_a"]
    on = t[igniter > 0.5 * igniter.max()] if igniter.max() > 0 else t[:0]
    f = {"n_samples": len(df), "duration_s": _num(t.iloc[-1]), "sample_hz": _num(hz), "first_sample_utc": t0,
         "radiometer_array": "saffire", "script_ignition_s": _num(on.iloc[0]) if len(on) else np.nan,
         "chamber_pressure_start_kpa": _num(base["ambient_pressure_kpa"].median()),
         "chamber_pressure_end_kpa": _num(df.loc[t >= t.iloc[-1] - FINAL_S, "ambient_pressure_kpa"].median()),
         "chamber_pressure_max_kpa": _num(smooth(df["ambient_pressure_kpa"], hz).max()),
         "o2_start_pct": _num(base["o2_pct"].median()), "o2_min_pct": _num(smooth(df["o2_pct"], hz).min()),
         "co2_start_pct": _num(base["co2_pct"].median()), "co2_max_pct": _num(smooth(df["co2_pct"], hz).max()),
         "anemometer_start_cm_s": _num(base[["anemometer_1_cm_s", "anemometer_2_cm_s"]].median().mean()),
         "plume_temp_max_c": _num(smooth(df.filter(like="plume_temp"), hz).max().max()),
         "sample_temp_max_c": _num(smooth(df.filter(like="sample_temp"), hz).max().max())}
    for k in range(1, 5):
        col = f"radiometer_{k}_mw_cm2"
        rise = smooth(df[col], hz) - base[col].median()
        f[f"radiometer_{k}_rise_peak_mw_cm2"] = _num(rise.max())
        f[f"radiometer_{k}_time_of_peak_s"] = _num(t[rise.idxmax()])
    note = "burn duration not derived (no burn marker; radiometer baseline = median of first 50 s)"
    return {**row, **f, "features_note": note}


def cfi_reduced_files():
    """One row per CFI test with reduced data, keyed by its DropletData file (every such test has one)."""
    files = pd.read_csv(psi.PROCESSED / "files.csv")
    files = files[(files["accession"] == CFI) & files["downloaded"].astype(bool)]
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet")
    known = set(tests.loc[tests["accession"] == CFI, "test_id"])
    rows = []
    for name, path in zip(files["file_name"], files["local_path"]):
        m = CFI_REDUCED_FILE.search(name)
        if m:
            rows.append({"accession": CFI, "test_id": m.group(1) if m.group(1) in known else None,
                         "test_point": f"FLEX-{m.group(1)}{CFI_REDUCED_SUFFIX}", "reopened": False, "source_file": path})
    return pd.DataFrame(rows)


def cfi_reduced_siblings(source_file):
    """The four reduced files of a test, named from its DropletData file (same folder, kind swapped)."""
    return {kind: str(source_file).replace("_DropletData.txt", f"_{kind}.txt") for kind in CFI_REDUCED_KINDS}


def read_cfi_reduced_parts(path):
    """Each reduced file of a test as published: ({kind: DataFrame with time_s first}, [problems]). Columns are
    taken from the file's own header, because one ColorCamData file holds cool-flame columns."""
    parts, problems = {}, []
    for kind, sibling in cfi_reduced_siblings(path).items():
        sibling = Path(sibling)
        if not sibling.exists():
            if kind != "CoolFlameData":  # only tests with a cool flame have that file
                problems.append(f"{kind} file absent")
            continue
        head = sibling.open("rb").read(8)
        if head.startswith(b"%PDF"):
            problems.append(f"{kind} file is a PDF, not a table")
            continue
        try:
            df = pd.read_csv(sibling, sep="\t")
        except (UnicodeDecodeError, pd.errors.ParserError):
            problems.append(f"{kind} file is not readable text")
            continue
        time = [c for c in df.columns if c in CFI_REDUCED_TIME]
        keep = [c for c in df.columns if c in CFI_REDUCED_COLUMNS]
        if len(time) != 1 or not keep:
            problems.append(f"{kind} file has unexpected columns ({', '.join(map(str, df.columns))})")
            continue
        if not any(c.startswith(kind.removesuffix("Data")) for c in keep) and kind != "RadiometerData":
            problems.append(f"{kind} file holds other columns ({', '.join(keep)})")
        if any(c in df.columns for c in CFI_REDUCED_DROPPED):
            problems.append("TotalWideBandPower_W is not physical (about -5e6 W) and is left out")
        parts[kind] = df[[*time, *keep]].rename(columns={time[0]: "time_s", **CFI_REDUCED_COLUMNS})
    return parts, problems


def read_cfi_reduced(path):
    """The reduced files of one test stacked on their shared time axis (seconds as published; zero appears to be
    ignition). Each row comes from one file, so the other files' columns are empty in it; values are unchanged."""
    parts, _ = read_cfi_reduced_parts(path)
    if not parts:
        return None, pd.DataFrame({"time_s": []})
    out = pd.concat(parts.values(), ignore_index=True).sort_values("time_s", kind="stable").reset_index(drop=True)
    return None, out


def cfi_reduced_features(row):
    parts, problems = read_cfi_reduced_parts(psi.ROOT / row["source_file"])
    f = {"radiometer_array": "cfi-droplet-reduced", "reduced_files": ";".join(parts)}
    if parts:
        times = pd.concat([p["time_s"] for p in parts.values()])
        f["n_samples"], f["duration_s"] = int(len(times)), _num(times.max() - times.min())

    def column(name):
        found = [p[name] for p in parts.values() if name in p]
        return pd.concat(found) if found else None

    def last_time(name):
        found = [p.loc[p[name] > 0, "time_s"] for p in parts.values() if name in p]
        found = pd.concat(found) if found else pd.Series(dtype=float)
        return _num(found.max()) if len(found) else np.nan

    droplet = parts.get("DropletData")
    if droplet is not None:
        f["sample_hz"] = _num(1 / np.median(np.diff(droplet["time_s"])))
        tracked = droplet.loc[droplet["droplet_diameter_mm"] > 0, "droplet_diameter_mm"]
        if len(tracked):
            f["droplet_diameter_first_mm"], f["droplet_diameter_min_mm"] = _num(tracked.iloc[0]), _num(tracked.min())
    for name, feature in (("flame_diameter_mm", "flame_diameter_max_mm"), ("cool_flame_fwhm_mm", "cool_flame_fwhm_max_mm"),
                          ("narrow_band_power_w", "narrow_band_power_max_w")):
        values = column(name)
        if values is not None:
            f[feature] = _num(values.max())
    f["hot_flame_last_s"], f["cool_flame_last_s"] = last_time("flame_diameter_mm"), last_time("cool_flame_fwhm_mm")
    notes = ["reduced data as published by the investigators, time zero as in the files (ignition, inferred)", *problems]
    return {**row, **f, "features_note": "; ".join(notes)}


def build(workers=None):
    files = pd.concat([data_files(), cfi_files(), cfi_reduced_files(), saffire_files()], ignore_index=True)
    joined = files[files["test_id"].notna()]
    with ProcessPoolExecutor(workers) as ex:
        acme = joined[joined["accession"].isin(ACME)].to_dict("records")
        recs = list(ex.map(file_features, acme, chunksize=4))
        cfi = joined[joined["accession"] == CFI]
        reduced = cfi["test_point"].str.endswith(CFI_REDUCED_SUFFIX)
        recs += list(ex.map(cfi_features, cfi[~reduced].to_dict("records")))
        recs += list(ex.map(cfi_reduced_features, cfi[reduced].to_dict("records")))
        recs += list(ex.map(saffire_features, joined[joined["accession"].isin(SAFFIRE)].to_dict("records")))
    out = pd.DataFrame(recs).drop(columns=["reopened"])
    out = out.dropna(axis=1, how="all")  # channels no file carries
    out = out.sort_values(["accession", "test_point", "source_file"]).reset_index(drop=True)
    psi.write_table(out, "timeseries_features")
    unjoined = files[files["test_id"].isna()]
    print(f"{len(joined)} of {len(files)} data files join to tests; not joined:",
          ", ".join(f"{a} {p}" for a, p in zip(unjoined["accession"], unjoined["test_point"])))
    return out


def load_timeseries(test_id, test_point=None, accession=None):
    """Signals of one test in engineering units: `test_point`, `time_s`, then one column per channel with the
    unit in its name. `test_id` is a `tests.test_id` (a test-point or CIR code like "21228A1" also works).
    Tests with several files (PSI-23 test days, re-opened test points, the 24 CFI tests that also have reduced
    data as `FLEX-<id>-reduced`) return all of them stacked; pass
    `test_point` to pick one, and `accession` if a test id could be ambiguous."""
    feats = pd.read_parquet(psi.PROCESSED / "timeseries_features.parquet",
                            columns=["accession", "test_id", "test_point", "source_file"])
    key = str(test_id).replace(" ", "")
    sel = feats[(feats["test_id"].str.replace(" ", "") == key) | (feats["test_point"] == key)]
    if test_point is not None:
        sel = sel[sel["test_point"] == test_point]
    if accession is not None:
        sel = sel[sel["accession"] == accession]
    if sel.empty:
        raise KeyError(f"no time series for test {test_id!r}")
    frames = []
    for acc, point, source in zip(sel["accession"], sel["test_point"], sel["source_file"]):
        reader = (read_cfi_reduced if point.endswith(CFI_REDUCED_SUFFIX) else read_cfi if acc == CFI
                  else read_saffire if acc in SAFFIRE else read_acme)
        df = reader(psi.raw_file(source))[1]
        df.insert(0, "test_point", point)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    build()
