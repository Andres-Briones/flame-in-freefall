"""`catalog.json` (every table and column), `tools.json` (function-calling specs) and a static JSON export
for a front end without a Python backend.

Run: uv run python -m fif.pipeline.build_catalog
"""
import json
import re

import pandas as pd

from fif import api, psi, tools
from fif.questions import QUESTIONS

EXPORT = psi.ROOT / "data" / "export"
TABLES = {
    "investigations": "One row per PSI investigation, flattened from the PSI API record.",
    "tests": "One row per test, test day or condition set. Dictionary and caveats: docs/tests-table.md.",
    "discrepancies": "Curated conflicts between the PSI experiment tables and the raw sensor data, with the action taken. "
                     "Source: data/corrections/tests_patches.json. See docs/tests-table.md.",
    "spread_steps": "BASS-II (PSI-25) flame spread rates of the thick-PMMA slab tests, one row per test and flow step, "
                    "transcribed from the BASS-II Summary Report, Table 5.1 (data/corrections/tests_spread_bass2.json). "
                    "Steps of one test are not independent. See docs/tests-table.md.",
    "test_sheets": "ACME Science Test Sheets of PSI-10 and PSI-159, one row per page: the form the operators filled in "
                   "by hand for each test point (ignition, hot or cool flame, soot, how the flame ended, comments). "
                   "Every value is an AI model's reading of a hand-filled scan (data/transcriptions/), not checked by a "
                   "human; say so wherever a value is shown. See docs/formats.md.",
    "timeseries_features": "Summary features of each per-test sensor time series. See docs/formats.md.",
    "files": "Every file listed in the 24 PSI records, downloaded or not.",
    "evidence": "Text extracted from the downloaded documents, in chunks of about 1,500 characters.",
    "evidence_files": "Extraction status of each document (ok, transcribed, no_text for scans, unsupported, error, withheld).",
}
SHEET_FIELDS = {
    "test_id": "id box", "date": "test date", "gmt": "GMT day and time", "test_of_day": "'Test of day #'",
    "flame_of_day": "'Flame of day #' ('Hot flame of day #' on CFI-G inverse sheets); says 'no ignition' or 'abort' in words",
    "test_type": "'Test type?' (standard, ignition, no-flame, other)",
    "chamber_pressure": "chamber pressure before the test", "chamber_pressure_post": "chamber pressure after the test",
    "fuel_flow": "burner fuel flow (normal flames)", "o2_flow": "burner oxidizer flow (inverse flames)",
    "n2_flow": "burner nitrogen flow", "oxidizer_bottle_pressure": "oxidizer bottle pressure after the test",
    "ignited": "'Ignited?' (yes / no / yes, but ...)",
    "flame": "'hot / cool / maybe cool' row (inverse and CFI-G forms)",
    "flame_behavior": "the other 'Flame' rows (asymmetric, hole/opening, partially detached, oscillating, unsteady, "
                      "quasi-steady, blew out), '; '-separated",
    "soot": "single 'Soot' row of the 2019 normal-flame form", "soot_ignition": "'Soot@ignition'",
    "soot_middle": "'Soot@middle'", "soot_end": "'Soot@end'",
    "out": "'Out' row: how the flame ended (ext. detect / time out / temp. limit); not on the 2019 normal-flame form",
}
TEST_SHEETS = {
    **{f"{name}_written": f"{about}, as transcribed (with the transcriber's remarks in brackets and after '— note:')"
       for name, about in SHEET_FIELDS.items()},
    "accession": "PSI accession (PSI-10 or PSI-159)",
    "file_name": "scanned PDF the page is in (transcription: data/transcriptions/<accession>/<file_name>.md)",
    "page": "PDF page; one sheet per page", "form": "form title: investigation and flame type",
    "day": "ACME day code (YYDDD) in the file name",
    "test_id": "test point: the file's day code and the test letter and number written on the sheet",
    "test_id_basis": "as_written / day_from_file_name (the day digits on the sheet are wrong or unreadable) / "
                     "recorded_under_other_id",
    "test_id_note": "why test_id differs from test_id_written", "in_tests": "test_id is a row of `tests`",
    "tests_test_id": "that row's test_id as `tests` spells it (PSI-159 ids have a space)",
    "has_data_file": "PSI lists a sensor recording (<test_id>_data.csv) for the test point",
    "date_parsed": "date_written as an ISO date, when it is a full date", "date": "date of the day code",
    "date_note": "set when the date written on the sheet is not the day code's date",
    "chamber_pressure_psia": {"description": "chamber pressure before the test, when one number is written", "unit": "psia"},
    "chamber_pressure_post_psia": {"description": "chamber pressure after the test, when one number is written", "unit": "psia"},
    "oxidizer_bottle_pressure_psia": {"description": "oxidizer bottle pressure after the test, when one number is written", "unit": "psia"},
    **{f"{gas}_flow_slpm": {"description": f"{SHEET_FIELDS[f'{gas}_flow']}, when one number is written (empty for a ramp)",
                            "unit": "slpm, N2 basis"} for gas in ("fuel", "o2", "n2")},
    "ignited": "yes / yes_but (ticked 'yes, but ...': momentary or unsustained) / no / unclear; empty when not marked",
    "flame": "hot / cool / hot+cool / maybe_cool; empty when not marked",
    "soot_ignition": "none / little / lots when exactly one is marked", "soot_middle": "none / little / lots when exactly one is marked",
    "soot_end": "none / little / lots when exactly one is marked",
    "out": "ext_detect (extinction detected: the flame went out) / time_out (lasted the scripted time) / temp_limit "
           "(stopped by the burner temperature limit); empty when not exactly one is marked",
    "flame_behavior_note": "handwritten note next to the FLAME BEHAVIOR heading",
    "comments": "GENERAL COMMENTS lines, ' | '-separated",
    "n_uncertain": {"description": "[?] marks on the page: readings the transcriber was unsure of", "unit": "count"},
    "n_illegible": {"description": "places the transcriber marked illegible (struck or overwritten text included)", "unit": "count"},
    "differs_from_asrun": "the transcriber noted a difference from the as-run parameter file, or that none exists",
    "differs_text": "those notes",
}
DESCRIPTIONS = {
    "investigations": {
        "accession": "PSI accession", "acronym": "short name", "project_type": "Microgravity or Ground Investigation",
        "hardware": "hardware and facility names", "start_date": "MM-DD-YYYY, as in the PSI record; several are wrong (see digest)",
        "contacts": "investigator names from the PSI record contact block, '; '-separated",
        "author_contacts": "per-author name, affiliation, role and e-mail from the PSI record contact block",
        "objective": "objective text from the PSI record", "n_files": "files listed in the record",
        "total_gb": "size of all listed files", "publication_dois": "DOIs listed in the record, '; '-separated",
        "publications": "the record's publication list in its order: title, authors, doi (None when missing), status",
        "source_url": "PSI page of the investigation",
    },
    "files": {
        "category": "PSI file category (Raw Data, Science Documents, ...)", "downloaded": "present under data/raw/files/ with the size PSI lists",
        "status": "on_disk / size_differs (on disk, PSI now lists another size) / dead_link (listed by PSI, storage link fails; data/corrections/files_status.json) / not_downloaded",
        "local_path": "path relative to the repo",
    },
    "evidence": {
        "locator": "page (p3), slide, sheet, zip member or 'all'", "chunk": "chunk number within the locator",
        "text": "extracted text, whitespace-normalised; contact details of people who are not listed authors, postal "
        "addresses and private network addresses are replaced by [... removed] markers", "test_ref": "ACME test id found in the file name",
        "transcribed": "True when the text is an AI model's reading of a scanned page (no text layer), not the document's own text",
    },
    "discrepancies": {
        "id": "patch id (D01, ...), as listed in tests.extra `discrepancies`", "test_id": "test id as in the PSI table (null for a note on a whole investigation)",
        "test_id_now": "test id in `tests` after a test_id correction",
        "column": "`tests` column concerned, or a source column the table keeps only in `extra`",
        "table_value": "value in the PSI table", "evidence_value": "value the raw data give",
        "action": "replace / fill / flag / note",
        "flag": "flag put on the row; conflicts_with_test_sheet when the only evidence is a hand-filled test sheet "
                "(an AI reading of a scan, not checked by a human)",
        "evidence": "what the raw data or the test sheet show", "evidence_source": "file and channel the evidence comes from",
    },
    "test_sheets": TEST_SHEETS,
    "spread_steps": {
        "accession": "PSI accession (PSI-25)",
        "test_id": "test id of the `tests` row (M1 ... M20; M6 and M12 have no tracked rate and no row here)",
        "step": "position of the flow step in the report's list for the test (1 = first listed)",
        "n_steps": "steps with a spread rate in this test; the independent unit is the test, not the step",
        "flow_cm_s": "opposed-flow velocity of the step, as the report lists it (cm/s)",
        "spread_rate_mm_s": "flame spread rate tracked at that step (mm/s)",
        "thickness_mm": "PMMA slab thickness (mm)", "width_cm": "sample width as the report gives it (cm); the PSI table says 1 or 2 cm",
        "sides_burning": "1 = one side burning (other side on a metal substrate), 2 = both sides",
        "x_o2_initial": "O2 mole fraction at the start of the test (the `tests` row's x_o2_ambient)",
        "x_o2_final": "O2 mole fraction at the end of the test; O2 fell during the test and was not measured per step",
        "burn_time_s": "burn time of the whole test (s), from the report's minutes",
        "flags": "flags of the `tests` row", "source": "report, table and page the step was transcribed from",
        "source_file": "with source_row, the key of the `tests` row", "source_row": "with source_file, the key of the `tests` row",
    },
    "evidence_files": {"status": "ok / transcribed (scan read from data/transcriptions/ by an AI model) / no_text / unsupported / error / withheld (holds credentials, not extracted)", "n_chars": "extracted characters"},
}


def tests_descriptions():
    out = {}
    for line in (psi.ROOT / "docs" / "tests-table.md").read_text().splitlines():
        m = re.match(r"\| (`[^|]+`) \| (.+?) \| (.+?) \| (.+?) \|$", line)
        if m:
            for name in re.findall(r"`(\w+)`", m.group(1)):
                out[name] = {"description": m.group(2).replace("**", ""), "unit": None if m.group(3) == "-" else m.group(3)}
    return out


FEATURE_RULES = [  # (pattern, description, unit); first match wins
    (r"^(accession|test_id)$", "key of the `tests` row the recording belongs to", None),
    (r"^test_point$", "code of the recording in the file name (21228A1, F068A03, S1); `FLEX-<id>-reduced` is the "
     "investigators' reduced data of a CFI test", None),
    (r"^source_file$", "raw file the features were computed from", None),
    (r"^n_samples$", "number of samples", "count"), (r"^duration_s$", "length of the recording", "s"),
    (r"^sample_hz$", "sampling rate", "Hz"), (r"^first_sample_utc$", "time of the first sample (GMT)", None),
    (r"^(experiment|burner)_code$", "code from the file header", None),
    (r"_gas$", "gas on this mass-flow controller, from the header gas code", None),
    (r"^thermocouple_rake$", "thermocouple rake fitted, from the header", None),
    (r"^pmt\d_gain_v$", "photomultiplier gain setting", "V"),
    (r"^radiometer_array$", "standard, cfi-g, cfi-droplet, cfi-droplet-reduced or saffire", None),
    (r"^reduced_files$", "which reduced files of the test could be read", None),
    (r"^droplet_diameter_(first|min)_mm$", "first and smallest tracked droplet diameter in the reduced data (zeros, which mark lost tracking, ignored)", "mm"),
    (r"^flame_diameter_max_mm$", "largest hot-flame diameter from the colour camera", "mm"),
    (r"^cool_flame_fwhm_max_mm$", "largest cool-flame diameter (FWHM)", "mm"),
    (r"^(hot|cool)_flame_last_s$", "last time the reduced data give a flame diameter above zero", "s"),
    (r"^narrow_band_power_max_w$", "maximum of the published narrow-band radiometer power", "W"),
    (r"^radiometer_on_s$", "time the flame signal stays above threshold, igniter glow included", "s"),
    (r"^flame_detected$", "radiometer_on_s of at least 2 s", None),
    (r"^ignition_time_s$", "first sample with the flame signal above threshold", "s"),
    (r"^flameout_time_s$", "last sample with the flame signal above threshold", "s"),
    (r"^burn_duration_s$", "flameout minus ignition; 0 when no flame is detected", "s"),
    (r"^flame_threshold$", "detection threshold used (W/cm2 standard array, V CFI-G)", None),
    (r"^script_", "event of the test script, relative to the first sample", "s"),
    (r"_clipped$", "peak within 1% of the channel's recorder ceiling: the peak and burn mean are lower bounds", None),
    (r"_flow_max_slpm$", "whole-file maximum of the flow reading; often a controller spike before ignition, not the test's flow", "slpm"),
    (r"_flow_max_burn_slpm$", "maximum flow during the detected burn", "slpm"),
    (r"_flow_mean_burn_slpm$", "mean flow during the detected burn", "slpm"),
    (r"^chamber_pressure_(start|end|max|mean_burn)_kpa$", "chamber pressure at the start, the end, its maximum, or its mean during the burn", "kPa"),
    (r"_time_of_(peak|max)_s$", "time of the channel's maximum", "s"),
    (r"_rise_peak_mw_cm2$", "peak radiometer signal above its pre-ignition baseline", "mW/cm2"),
    (r"_peak_w_cm2$", "peak irradiance (0.2 s smoothing)", "W/cm2"),
    (r"_mean_burn_w_cm2$", "mean irradiance during the detected burn", "W/cm2"),
    (r"_final_w_cm2$", "irradiance in the last second of the file", "W/cm2"),
    (r"_baseline_v$", "signal before ignition, uncalibrated", "V"),
    (r"_peak_v$", "peak signal, uncalibrated", "V"), (r"_final_v$", "signal in the last second, uncalibrated", "V"),
    (r"_(mean|max)_burn_v$", "mean or maximum signal during the detected burn, uncalibrated (PMT: 4.4 V or more is the rail)", "V"),
    (r"_temp_(start|final|max|mean)_c$|_temp_max_c$|^(plume|sample)_temp_max_c$", "temperature at the start, the end, its maximum or its mean", "C"),
    (r"^(o2|co2)_(start|min|max)_pct$", "Saffire cabin gas sensor reading at the start, or its extreme", "%"),
    (r"^anemometer_start_cm_s$", "Saffire flow speed at the start", "cm/s"),
    (r"^features_note$", "problems found while parsing, or why a feature is missing", None),
]


def feature_descriptions(columns):
    out = {}
    for name in columns:
        for pattern, description, unit in FEATURE_RULES:
            if re.search(pattern, name):
                out[name] = {"description": description, "unit": unit}
                break
    return out


def column_entry(series, described):
    entry = {"dtype": str(series.dtype), "non_null": int(series.notna().sum())}
    entry.update(described if isinstance(described, dict) else {"description": described})
    values = series.dropna()
    if pd.api.types.is_bool_dtype(values) or values.empty:
        return entry
    if pd.api.types.is_numeric_dtype(values):
        entry["min"], entry["max"] = float(values.min()), float(values.max())
    elif values.map(lambda v: isinstance(v, str)).all() and values.nunique() <= 40:
        entry["values"] = values.value_counts().to_dict()
    return entry


def catalog():
    described = {**DESCRIPTIONS, "tests": tests_descriptions()}
    out = {}
    for name, about in TABLES.items():
        path = psi.PROCESSED / f"{name}.parquet"
        if not path.exists():
            continue
        df = pd.read_parquet(path)
        if name == "timeseries_features":
            described[name] = feature_descriptions(df.columns)
        columns = {c: column_entry(df[c], described.get(name, {}).get(c)) for c in df.columns}
        out[name] = {"description": about, "rows": len(df), "files": [f"data/processed/{name}.parquet", f"data/processed/{name}.csv"],
                     "columns": columns}
    return out


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1, allow_nan=False, default=str))
    print(f"{path.relative_to(psi.ROOT)}: {path.stat().st_size / 1024:.0f} kB")


def export():
    """Pre-computed answers, so a static front end needs no Python."""
    write(EXPORT / "investigations.json", api.search_investigations()["data"])
    write(EXPORT / "records.json", api.records())
    write(EXPORT / "publications.json", {
        acc: {k: v for k, v in api.get_investigation(acc, sections=["publications"])["data"].items()
              if k in ("publications", "publication_review")} for acc in api.records()})
    write(EXPORT / "synthesis.json", api.synthesis())
    write(EXPORT / "tests.json", api.filter_tests(row_kind=None, limit=10**6)["data"]["rows"])
    write(EXPORT / "coverage.json", {phase or "all": api.coverage(fuel_phase=phase) for phase in (None, "solid", "liquid", "gas")})
    ranked = {
        f"{scenario}|{phase}|{pillar or 'any'}": api.relevance(scenario, fuel_phase=phase, pillar=pillar)
        for scenario in api.SCENARIOS for phase in ("solid", "liquid", "gas") for pillar in (None, *api.PILLARS)
    }
    write(EXPORT / "relevance.json", ranked)
    write(EXPORT / "models.json", api.predict()["data"])
    write(EXPORT / "discrepancies.json", api.discrepancies()["data"])
    write(EXPORT / "test_sheets.json", {"notes": [api.SHEET_NOTE], "rows": api._rows(api.table("test_sheets"))})
    if (psi.PROCESSED / "timeseries_features.parquet").exists():
        write(EXPORT / "timeseries_features.json", api._rows(api.table("timeseries_features")))
        traces = {f"{q['arguments'].get('accession', '')}|{q['arguments']['test_id']}".lstrip("|"):
                  api.timeseries(**q["arguments"]) for q in QUESTIONS if q["function"] == "timeseries"}
        write(EXPORT / "timeseries_examples.json", traces)


def question_bank():
    lines = ["# Question bank", "",
             "Questions the data answer today. Each has the `fif.api` call that answers it, a chart suggestion and the",
             "answer as of the current tables. `tests/test_questions.py` runs every call. Source: `fif/questions.py`.", ""]
    theme = None
    for n, q in enumerate(QUESTIONS, 1):
        if q["theme"] != theme:
            theme = q["theme"]
            lines += [f"## {theme}", ""]
        call = f"{q['function']}({', '.join(f'{k}={json.dumps(v)}' for k, v in q['arguments'].items())})"
        lines += [f"**{n}. {q['question']}**", "", f"- Call: `{call}`", f"- Chart: {q['chart'] or 'none (text with citations)'}",
                  f"- Answer today: {q['answer']}", ""]
    path = psi.ROOT / "docs" / "question-bank.md"
    path.write_text("\n".join(lines))
    write(EXPORT / "questions.json", QUESTIONS)


if __name__ == "__main__":
    question_bank()
    write(psi.PROCESSED / "catalog.json", catalog())
    write(psi.PROCESSED / "tools.json", tools.TOOLS)
    export()
