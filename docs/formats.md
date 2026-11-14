# Raw data formats

These notes describe how to load each PSI raw or analysed file family that holds numeric data, so that
nobody has to guess the layout. Each family was decoded from several sample files. The notes give:

- the file-name pattern and file count;
- the join to `tests.test_id`, with the join rate checked in code;
- the layout: encoding, delimiter and header rows;
- each column with its meaning and unit;
- the sample rate and the sentinel (missing-value) markers;
- any oddities, plus a short loading snippet.

Conventions:

- **Counts** come from `data/processed/files.csv` and include downloaded files only. Images and videos are never
  downloaded.
- **Paths** are relative to the repository root. Raw files are in `data/raw/files/<accession>/<category>/` and are
  named `<accession>_<category>_<original name>`.
- **Unit sources** are marked in each table:
  - *header*: the unit is printed in the file.
  - *doc*: the unit comes from a named PSI document.
  - *inferred*: we worked the unit out ourselves.
  - *unknown*: we could not establish the unit.
- **Join** means the identifier taken from the file name is found in `tests.parquet` for the same accession.
  Spaces are removed before matching; the PSI-159 test ids contain spaces (`21196 A1`).
- **Untrusted data.** Treat everything under `data/raw/` as untrusted: parse it, never execute it. Some
  engineering documents contain phone numbers, postal addresses, credentials and network addresses. None are
  reproduced here. Published author contact — name, affiliation, role and institutional e-mail — is surfaced in the
  `author_contacts` column of `investigations`, taken only from the PSI record's structured contact block, never
  from document text (decision 009).

The per-test time series that join cleanly are summarised in `data/processed/timeseries_features`, built by
`fif/pipeline/build_timeseries.py` (last section). `load_timeseries(test_id)` in the same module returns any of
them as a tidy DataFrame in engineering units.

## Overview

| family | accession(s) | files | join to `tests` | in `timeseries_features` |
|---|---|---|---|---|
| ACME 125 Hz `<tp>_data.csv` | PSI-10, PSI-23, PSI-159 | 317 + 288 + 338 = 943 | 308/317, 288/288 (to test days), 328/338 | yes (924 rows) |
| ACME `mfcSetpoints.csv`, `as run`, `_TP`, `_Comments`, `.mdipsug`, GC `.asc`, logs, workbooks | PSI-10, PSI-23, PSI-159 | see below | 92–100% | `_TP` event times only |
| CFI `<CIR>_Radiometer_Readings.txt` + `_Chamber_Readings.txt` | PSI-39 | 123 + 123 | 123/123 via `extra.CIR` | yes (123 rows, no burn rule) |
| CFI reduced `FLEX-<id>_*.txt`, `.meta`, `.metadata`, settings | PSI-39 | 111 + 343 + … | 24/24 ids, 116/116 codes | yes for the four data files (24 rows, `test_point` `FLEX-<id>-reduced`); TestSheet, `.meta`, settings no |
| Saffire-I/III per-sample sensor workbooks | PSI-98, PSI-100 | 4 | 4/4 | yes (4 rows, no burn rule) |
| Saffire telemetry workbooks / CSVs | PSI-98, PSI-100 | 5 | mission-level, not per test | no |
| SAME-R housekeeping CSV / per-run workbooks | PSI-101 | 44 + 74 | 44/44 and 73/74 on the in-file `TestNumber` / run number, not 1:1 | no |
| SAME analysed workbooks | PSI-102 | 59 | 0 (`tests` holds only the 8 planned rows) | no |
| SPICE workbooks and text | PSI-107 | 35 | no time series (the run log is the source of `tests`) | no |
| DAFT particle-counter tracks | PSI-47 | 6 + 12 | 6/6 to D2 by date, not 1:1 | no |
| BASS, BASS-II, SLICE, FLEX, FLEX-2 | 26, 25, 106, 69, 68 | no numeric raw data | — | no |
| Ground studies | 115, 117, 142 (60, 62: metadata only) | 44 + 10 + 1 | no `tests` rows | no |

## ACME per-test data: `<tp>_data.csv` (PSI-10, PSI-23, PSI-159)

Advanced Combustion via Microgravity Experiments (ACME) in the Combustion Integrated Rack (CIR) records every
test point to one CSV of raw analogue-input voltages. The conversion to engineering units is given in
**ACME-DOC-010 Rev D, Software Interface Design Description, section 10** (`PSI-23_Reference Data_ACME-DOC-010_D.pdf`,
pages 126–143). Rev C extracts are in `PSI-23_Science Documents_ACME non-imaging data file description.pdf`.

**Files.** The name pattern is `<acc>_Raw Data_<tp>[_1]_data.csv`. The test point `<tp>` is `YYDDD` + letter + number
(e.g. `21228A1`): two-digit year, GMT day of year, then a point letter and number. A `_1` suffix marks a re-opened
test point: `19256B2_1`, `20176K1_1` and `21196M2_1`.

| accession | files | join key | joined | not joined |
|---|---|---|---|---|
| PSI-10 Flame Design | 317 | `tp` = `test_id` | 308 (the table id `22042M1` is corrected to `22024M1`, patch D01) | 19115C1, 19115D1, 19115H1, 19115P1, 19123H1, 19123L8, 19142B1, 19175B2, 19196N2 |
| PSI-23 s-Flame | 288 | `tp[:5]` = test day `test_id` | 288 (all 18 days) | — |
| PSI-159 CFI-G | 338 | `tp` (or `tp_1`) = `test_id` without spaces | 328 | 21106A1–A3, 21106G1–G5, 21106G8, 21242F1 |

The unjoined files are real test points. The experiment tables do not list them. The PSI-10 table has 19 tests
without a file (e.g. 19206A1, 19206G1–G9, 21301J1–J2). PSI-20, PSI-21 and PSI-22 (BRE, CLD Flame, E-FIELD)
have no downloaded raw data.

**Layout.**

- Encoding is ASCII (read as latin-1), comma-delimited, LF line endings.
- **Row 1** is a metadata header: `YYYY-MM-DD DDD hh:mm:ss:mmm ,Key: value,Key: value,...`. It holds the file-open
  time and the GMT day, then `Experiment`, `Test Point`, `MFCA1 Gas`, `MFCA1 Full Scale`, `MFCA2 Gas`,
  `MFCA2 Full Scale`, `MFCA3 Gas`, `MFCA3 Full Scale`, `EField`, `EFieldPol`, `Igniter`, `Burner`,
  `Thermocouple`, `Radiometer`, `IPSU 1`–`IPSU 6`, `Fiber`, and `PMT 1 Gain`–`PMT 3 Gain` (V).
- The codes are decoded in Rev D Table 34:
  - Experiment: 0 Flame Design, 2 s-Flame, 5 (undocumented, used by CFI-G and PSI-10 day 21301).
  - Thermocouple: rake position 0 near, 1 far, 2 removed.
  - Burner: 0–2 spherical, 3 coflow, 4–5 gas jet, 6–7 BRE.
  - MFCA3 Gas: 0–18 are documented. Codes 19–25 are not; joined to `tests.fuel` they are 19 and 22 propane,
    20, 23 and 24 butane, 21 and 25 ethane (inferred).
- **Row 2** is the column header. There are two variants: 467 files have the standard radiometer array and
  476 files have the CFI-G dual-gain array (all PSI-159 files and 138 PSI-10 files).
- **Rows 3+** hold the data: one row per sample.
- `Time` is `hh:mm:ss:mmm` (GMT clock, same clock as `_TP.txt`). The date is only in row 1, and the clock wraps at
  midnight (e.g. 21106G8).

**Sampling.** The nominal rate is 125 Hz (8 ms, Rev D §3.1.7.1). All 943 files have a median Δt of exactly
8.0 ms. Durations run from 8 s to 914 s (median 70 s). One file (19254L1) has a 23 s gap.

**Columns.** "V" is the raw DAQ voltage. The conversions follow Rev D §10.2. `build_timeseries.to_engineering`
implements them and produces the channel names shown.

| column | meaning | conversion → channel (unit) | source |
|---|---|---|---|
| `MFCA1StaticMixerFlow` | oxidiser MFC flow | V / 5 × `MFCA1 Full Scale` → `oxidizer_flow_slpm` (SLPM) | doc |
| `MFCA2BypassFlow` | inert (N2 bypass) MFC flow | V / 5 × `MFCA2 Full Scale` → `inert_flow_slpm` | doc |
| `MFCA3FuelFlow` | fuel MFC flow | V / 5 × `MFCA3 Full Scale` → `fuel_flow_slpm` | doc |
| `IonCurrent` | E-field ion current | 1000 V / 162 → `ion_current_ua` (µA) | doc |
| `PTA1`, `PTA2` | burner / coflow line pressure (Rev C and Rev D swap inner/outer) | (V − 0.5) × 14.5038 × 10 / 4 psia → `inner_coflow_pressure_kpa`, `outer_coflow_pressure_kpa` | doc |
| `PTA3` | chamber pressure | same as PTA1 → `chamber_pressure_kpa` (× 6.894757) | doc |
| `EfieldVoltage` | E-field supply monitor | V × 2486.1795 + 141.9733 (V); not exported | doc |
| `PMT1`, `PMT2`, `PMT3` | photomultipliers at 310 nm (OH\*), broadband UV and 430 nm (CH\*) | kept in V → `pmt1_310nm_v`, `pmt2_broadband_uv_v`, `pmt3_430nm_v`. Rev C: anode current µA = V. Rev D gives gain-specific irradiance polynomials for gains 2–8 V only; CFI-G ran at 8–10 V | doc |
| `TCA`, `TCD` | rake thermocouples A, D (type K) | thermocouple EMF; type K with cold-junction compensation → `rake_a_temp_c`, `rake_d_temp_c` | doc |
| `TCB`, `TCC` | rake thermocouples B, C (type B) | type B → `rake_b_temp_c`, `rake_c_temp_c`; NaN below about 250 °C (outside the polynomial range) | doc |
| `TC200A`, `TC200B` | type K at 200 mm from the axis (igniter / relay side) | → `ambient_200mm_a_temp_c`, `ambient_200mm_b_temp_c` | doc |
| `TCBurner` | type K on the burner (none on the coflow burner) | → `burner_temp_c` | doc |
| `Radiometer+60`, `+30`, `Center`, `-30`, `-60`, `Offset` | standard thermopile array | W/cm² = a·V + b with (a, b) = (0.002622, −0.003370), (0.001794, −0.002309), (0.002894, −0.003932), (0.002397, −0.003077), (0.002591, −0.003300), (0.001798, −0.002307) → `radiometer_p60_w_cm2` … `radiometer_offset_w_cm2` | doc (ACME-RPT-011 via Rev D) |
| `Radiometer…CJ` | radiometer cold-junction temperature (TI LM20) | °C = −1481.96 + √(2196200 + 257700 (1.8639 − V)); not exported | doc |
| `Radiometer3±NNLoGain` / `HiGain` (+60, +30, −10) | CFI-G dual-gain array (replaces the standard array) | **no conversion in PSI.** CIR-RPT-4600 is cited but not archived. Kept in V → `radiometer3_p60_lo_v` … `radiometer3_m10_hi_v` | header |
| `Ch13`–`Ch16`, `Ch20`, `Ch21`, `TCE` | unused or spare in non-BRE runs | — | doc |
| `TCCJ` | thermocouple cold junction (AD590) | °C = 338.98305 V − 273.15 → `cold_junction_temp_c` | doc |
| `EfieldSetpointOut` | E-field control voltage (9.99 when unused) | quadratic per polarity (Rev D §10.2.36); not exported | doc |

**Thermocouple conversion (Rev D §10.4–10.5).** The thermocouple EMF in mV is V × 1000. First convert the
cold-junction temperature (`TCCJ`) to mV with the NIST forward polynomial and add it to the EMF. Then apply
the NIST inverse polynomial: type K is valid for 0–54.886 mV, type B for 0.291–13.820 mV. The code was checked
against the NIST reference points E(100 °C) = 4.096 mV, E(500 °C) = 20.644 mV, E(1000 °C) = 41.276 mV (type K) and
E(1000 °C) = 4.834 mV (type B).

**Sentinels and oddities.**

- **PMT rail.** PMTs read about 4.4–4.58 V when they are unpowered (before ignition in most files) or saturated.
  Treat readings ≥ 4.4 V as off or saturated, not as signal.
- **Radiometer saturation.** The recorder clips near 4.87 V, so each standard-array channel has its own ceiling:
  +60 0.00940, +30 0.00644, Center 0.01012, −30 0.00859, −60 0.00931, Offset 0.00646 W/cm². Most flames reach it
  on the centre and ±30 channels (`radiometer_*_clipped` in `timeseries_features`); a clipped peak or burn mean
  is a lower bound. CFI-G
  high-gain channels saturate near 5.0–5.4 V; low-gain channels near 4.8 V.
- **Radiometer offsets.** CFI-G channels have negative offsets before ignition (about −0.03 V low gain, about
  −0.3 to −0.7 V high gain). Subtract the pre-ignition baseline.
- **Malformed rows.** 11 files contain truncated rows padded with NUL bytes: 21106F1, 21112C3, 21130N5, 21137A1,
  21137A7, 21216H1, 19254L1, 19352D5, 19352M1, 20006A5, 20170F2. Each has 1–3 such rows. Drop rows whose field
  count differs from the header.
- **Extra elapsed-time column.** `19256B1` has an extra unnamed second column holding elapsed seconds (`Time,,MFCA1…`).
- **Test-point suffix mismatches.** In 3 files the header `Test Point` carries a `_1` suffix while the file name
  does not.
- **Rake temperatures.** The rake thermocouples read cabin temperature when the rake is far from the flame. When
  the header has `Thermocouple: 2` (removed) they are not exported.
- **Header gas codes describe the bottle.** In PSI-23 the header `MFCA3 Gas` code is the nominal bottle, not the
  delivered mixture:
  - Days 20132, 20136 and 20142 all carry code 12 (H2/CH4/He 25/20/55), although the table lists three
    different mixtures.
  - Days 20006 and 20013 carry undiluted H2/CH4 codes (the table records an on-orbit 55% N2 dilution).

```python
from fif.pipeline.build_timeseries import read_acme, read_acme_raw
header, df = read_acme("data/raw/files/PSI-159/Raw Data/PSI-159_Raw Data_21228A1_data.csv")  # engineering units
header, raw = read_acme_raw(path)   # raw volts + time_s
# plain pandas: header dict from line 1, then
raw = pd.read_csv(path, skiprows=1, on_bad_lines="skip")  # 'Time' is hh:mm:ss:mmm
# 11 files end in a NUL-padded, truncated row that pandas keeps: drop rows whose Time does not parse (read_acme does)
```

## ACME sidecar files (PSI-10, PSI-23, PSI-159)
Scope: files in `data/raw/files/<acc>/Raw Data/` other than the per-test `*_data.csv`. Counts come from `files.csv` (downloaded == True). "Join" means the test point parsed from the file name, with spaces removed, is found in `tests.parquet`. For PSI-23 only the first 5 digits (the test day) are compared. Main reference: ACME-DOC-010 Rev D (Software Interface Design Description), §8.2–8.3 (p124) and Table 34 (p126–127).

**Join failures shared by most families:** in PSI-10 the test points 19115C1/D1/H1/P1, 19123H1/L8, 19142B1, 19175B2 and 19196N2 are not in `tests.parquet`. In PSI-159, test points 21106A1–A3, G1–G5, G8 and 21242F1 are missing (tests.parquet has other 21106 points). These files exist but `tests.parquet` has no row for them, so they are probably aborted or re-run points that the experiment tables leave out.

### 1. `<tp>_mfcSetpoints.csv`: MFC set-point log
| | PSI-10 | PSI-23 | PSI-159 |
|---|---|---|---|
| files | 317 | 288 (2 named `<tp>_1_…`) | 339 (incl. `<tp>_1_…`, `…mfcSetpoints1.csv`) |
| join | 307/317 | 288/288 (by day) | 329/339 |
| tests covered | 307/327 | 18/18 days | 327/333 |

- ASCII text, comma-delimited. Rows have no trailing comma. Row 1 is the metadata header, the same as in `_data.csv`: `YYYY-MM-DD DDD hh:mm:ss:mmm ,Experiment: n,Test Point: …,MFCA1 Gas: n,MFCA1 Full Scale: x,…,PMT 3 Gain: x`. The codes are decoded in Table 34. Row 2 is `Time,MFCA1Setpoint(V),MFCA2Setpoint(V),MFCA3Setpoint(V)`.
- Per DOC-010 §8.2, the software writes a row whenever any of the 3 MFCs changes set-point. Each row holds all three current values, so these are event rows, not a fixed sampling rate. Files have 24–2346 rows (median 36).

| column | meaning | unit (source) |
|---|---|---|
| Time | `hh:mm:ss:mmm` GMT. The date is only in the row-1 header | header / §8.2 |
| MFCA1Setpoint(V) | MFCA1, static-mixer/oxidizer MFC command | V, 0–5 (header; DOC-010 AO-0) |
| MFCA2Setpoint(V) | MFCA2, N2 bypass/inert MFC | V (AO-1) |
| MFCA3Setpoint(V) | MFCA3, fuel MFC | V (AO-2) |

- Conversion (DOC-010 AO-0..2): `SLPM = V * MFCA<n> Full Scale / 5`, with the full scale taken from row 1. Full scales seen are 0.1, 0.2, 0.5, 1, 2, 5 and 20 SLPM, and they change between tests. The maximum voltage seen is 5.0.
- Experiment code: PSI-10 has 0 (Flame Design) in 299 files and **5** in 18 files (all on day 21301). PSI-23 has 2 (s-Flame). PSI-159 has 5. Rev D Table 34 only defines codes 0–4, so code 5 (CFI-G?) is undocumented.
- MFCA3 gas codes 19–25 appear in PSI-10 and PSI-159, but Table 34 stops at 18. Those codes are unknown.
- Oddities:
  - The first 2 rows are usually identical, both at the time of "Script resumed #1".
  - 3 files are all zeros.
  - 1 file has non-monotonic Time.
  - The time can wrap at midnight, because the date is only in the header.
  - In 3 files the header Test Point carries a `_1` suffix that the file name lacks (19256B2, 20176K1, 21196M2). tests.parquet uses `21196M2_1`.
```python
hdr = open(p).readline()
fs = {k: float(v) for k, v in re.findall(r'(MFCA\d) Full Scale: ([\d.]+)', hdr)}
df = pd.read_csv(p, skiprows=1)
for i in (1, 2, 3): df[f'MFCA{i}_slpm'] = df[f'MFCA{i}Setpoint(V)'] * fs[f'MFCA{i}'] / 5
```

### 2. `as run<tp>.txt`: executed script parameters
- Counts: PSI-10 281 (join 277), PSI-23 280 (join 280; includes 1 `as run<tp>-created_from_log.txt`), PSI-159 338 (join 328; includes 1 `_1`).
- ASCII text with one `name:value,` per line. The last line has no trailing comma. There is no header, and booleans are written `true`/`false`. The values are the script inputs that were actually run. The same `param: "name":value` lines also appear in the ACME.log.
- The key set depends on the experiment script:
  - **Flame Design / CFI-G script.** Used by PSI-159 (80 keys) and about half of PSI-10. Keys: `dataCamera*ExposureUs`, `analogCameraShutter`, `intensifier*Gain`, the `autoGain*` group, the `bracketing*` group, `igniter*`, `pmt1-3Gain`, `fiber*`, and `{fuel|oxidizer|nitrogen}{Ignition|TestFlow1-3}Slpm`. The flow time keys are `constantFlowTime1-3Sec`, plus the `postExtinctionFlowChange*` group.
  - **s-Flame-style script.** Used by PSI-23 (68 keys) and about 143 PSI-10 files from 2019. Keys: `ipsu*ArchiveRate`, `analogCamera{PreIgnition,Ignition,Test,Extinction}Shutter`, `fuelBottle*FlowRateN2Slpm`, `nitrogen*FlowRateN2Slpm` and `constantFlowTimeSec`. PSI-23 also has the ramp keys `numberOfRampHolds`, `rampSize{Fuel,N2}Slpm`, `rampDurationSec` and `holdDurationSec`. PSI-10 also has the `constant/rampPostExtinction*` keys.
- Units come from the key-name suffixes: `Us` = µs, `Ms` = ms, `Sec` = s, `Slpm` = SLPM, `C` = °C, `dB`, `PowerV` = V. Two families of units are not documented: `*CountsPerSec`, `*Position` and fiber units are motor counts (inferred), and the `analogCameraShutter` / `intensifier*Gain` units are unknown. `*FlowRateN2Slpm` is presumably an N2-equivalent flow (inferred from the name).
- Oddity: about 37 PSI-23 files and a few PSI-10 files are truncated mid-list, so later keys are missing.
```python
kv = dict(l.rstrip(',\n').split(':', 1) for l in open(p, encoding='latin-1') if ':' in l)
s = pd.Series(kv); s = pd.to_numeric(s, errors='ignore')
```

### 3. `<tp>_TP.txt`: test-point event timeline
- Counts: PSI-10 314 (310 `<tp>_TP` + 4 `#JK#`/`#JP#`), join 300. PSI-23 266, join 266. PSI-159 305 (incl. 1 `_1`), join 296.
- PSI-10 names like `19189JK1_TP.txt` contain `Test Point: 19189K1` inside, so the name and the content disagree. Use the content.
- ASCII text with blank lines. It starts with `Test Point: <tp>`, followed by `Label: YYYY-MM-DD hh:mm:ss` lines (1 s resolution, GMT). `***` means the event was not reached or does not apply.
- Event labels, in file order:

  `Script start`, `Script paused #1`, `Script resumed #1`, `Pre-ignition data`, `Pre-ignition images`, `Preheat igniter`, `MFCs on for priming`, `Ignition and retraction`, `Flame stabilization #1`, `Dilution of fuel and inert`, `Flame stabilization #2`, `Ramp coflow to match test cond`, `Flame stabilization #3`, `Ramp to final velocity`, `Constant flow`, `MFCs off`, `Post-flame images`, `Post-flame data`, then `Script complete`. Aborted runs (317 of 885 files) instead have `Script complete after abort` plus `Reason: …`. The reasons seen are `EXTINCTION DETECTED` (258) and `Burner temperature limit exceeded for specified duration` (59). The list ends with `Extinction detected`, `Script paused #2` and `Script resumed #2`.
- After the events comes a fixed-width camera table with the columns `Camera | Archived | Start Image | End Image`. The rows are IPSU1, IPSU2, ACME and Intensified. Columns are separated by tabs and spaces, numbers can have thousands separators (`2,017`), and `***` means not used. The ACME and Intensified "Archived" counts match the row counts of the `.mdipsug` files (checked on 21088A1: 696 and 2017).
```python
ev = {k: (None if v.strip() == '***' else pd.Timestamp(v)) for k, v in
      re.findall(r'^([A-Z][^:\n]+): (\*\*\*|\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)$', txt, re.M)}
cams = re.findall(r'^(IPSU1|IPSU2|ACME|Intensified)\s+([\d,*]+)\s+([\d,*]+)\s+([\d,*]+)', txt, re.M)
```

### 4. `<tp>_Comments.txt`: image-downlink comments
- Counts: PSI-10 313 (join 303), PSI-23 276 (join 276), PSI-159 331 (join 322). The PSI-159 count includes 12 `_ImagesComments.txt`, 1 `_ImageComments.txt` and 1 `_1_`.
- Free-form ASCII notes written by ground operators. They contain dated entries (`M/D/YYYY …`) saying which image units (IPSU1 HiBMS, IPSU2 LLL-UV, IPSUG ACME, IPSUG INTNS) were downlinked or re-downlinked. Entries are separated by `****` lines. They may include missing-image lists in the form `Missing <unit>:` / `Test Point:` / `of N images files, there are k missing:` followed by onboard paths (`/sd1/sci/<tp>/…_00129.hobj`, `<tp>A_1.0008.fci`). Some files contain only `complete`. There is no fixed schema, so parse with regexes.
```python
txt = open(p, encoding='latin-1').read()
missing = re.findall(r'(\S+\.(?:hobj|fci|tiff))', txt)
```

### 5. `ACME_<tp>.mdipsug` / `INTNS_<tp>.mdipsug`: IPSU-G image metadata
- Counts: ACME files are PSI-10 250 (join 246), PSI-23 8 (join 8) and PSI-159 305 (join 297, incl. 1 `_1`). INTNS files are 240 (join 236), 8 (8) and 305 (297).
- **Text** CSV (ASCII, comma-delimited, `\n` line endings) with 1 header row and one row per archived image. The header is identical across all files of a type. Row counts: ACME 16–23098, INTNS 397–21051.
- Sampling: ACME frames are typically one per exposure (100 ms or 1 s). INTNS frames are ~43 ms apart (~23 fps).

| column | meaning / unit |
|---|---|
| Timestamp | `YYYYMMDD_hhmmss.mmm` image time (GMT, inferred) |
| Filename | onboard image path, `/sd0|sd1/sci/<tp>/<ts>_ACME_<tp>_NNNNN.hobj` (ACME) or `…_INTNS_<tp>_NNNNN.tiff` (INTNS). NNNNN is the frame index |
| DeltaMilliseconds | ms since the previous frame (inferred) |
| CalculatedRate | ≈1000/Delta, in Hz (inferred). 0 on the first row |
| BinningX, BinningY | binning. ACME: `1`; INTNS: `x1` |
| BlockId | camera frame counter |
| BufferIncomplete, BufferIncompleteTotal, BuffersNum | acquisition buffer diagnostics (unit unknown) |
| ExposureManual | ACME: exposure in µs (matches `dataCamera*ExposureUs` in as-run, inferred). INTNS: 32000, unit unknown |
| FrameRate | nominal camera frame rate setting (ACME 30.0003; INTNS 23) |
| GainManual | ACME: gain, probably dB (matches `dataCameraManualGain`, inferred). INTNS: 143, unknown |
| Height/Width (ACME), ImageHeight/ImageWidth, RegionHeight/RegionWidth (INTNS) | px. ACME 1024×1360; INTNS 1040×1392 |
| PixelFormat | ACME `BayerRG12` (raw colour); INTNS `Mono16` |
| RegionX, RegionY | ROI offset, px |
| TickTimestamp | camera clock ticks. ACME: ns (Δ≈1e9 per 1 s frame, inferred). INTNS: unit unknown (≈2.09e6 ticks/s) |
| INTNS only: BitShift, CameraSpeed, ExposureAuto, ExposureMode, GainAuto, GainMode | camera settings (`NoShift`, `Normal`, 43067, 0, 143, 0). Meaning unknown |
```python
df = pd.read_csv(p)
df['t'] = pd.to_datetime(df.Timestamp, format='%Y%m%d_%H%M%S.%f')
df['frame'] = df.Filename.str.extract(r'_(\d{5})\.(?:hobj|tiff)$')[0].astype(int)
```

### 6. `moduleDataACD_<NN>_<YYYYMMDD>_<HHMM>.asc`: GC chromatograms
- Counts: PSI-10 66 and PSI-23 170. Of the PSI-23 files, 89 are named `<tp>_moduleDataACD_…`, and the date in those names is ≥1 day after the test-point day, so the sample is acquired later. Joining on the name's date gives only 33/66 (PSI-10) and 29/170 (PSI-23). There is no reliable test join apart from the tp prefix.
- EZChrom/"EZIQ" ASCII export written by the ZIN GC_Converter (see the GC_Coverter logs). Line endings are CRLF. The 13 header lines are `Key:\tv1\tv2\tv3`: Version 3, Maxchannels 3, Sample ID, Data File, Method, User Name, Acquisition Date and Time, `Sample Rate: 100` (Hz), `Total Data Points` (25500 each = 255 s), `X Axis Title: Seconds`, `Y Axis Title: microvolts_(uV)`, `X Axis Multiplier: 0.01` and `Y Axis Multiplier` (1/10/100 per channel).
- The body is one integer per line. Channels A, C and D are **concatenated** in that order, using the per-channel counts in `Total Data Points`. Some channels have 25641–25658 points instead of 25500. Total rows equal the sum for all 236 files.
- Signal: y[µV] = int × Y multiplier. This is inferred: the converter log reports `Detector sensitivity = 100` alongside the Y multipliers. The species detected on channels A, C and D are not documented here.
```python
L = open(p, encoding='latin-1').read().splitlines()
h = {l.split(':')[0]: l.split('\t')[1:] for l in L[:13]}
n = list(map(int, h['Total Data Points'])); v = np.array(L[13:], float)
chans = dict(zip('ACD', np.split(v, np.cumsum(n)[:-1])))
```

### 7. Daily logs: `*ACME.log`, `*IPSUG.log`, `GC_Coverter*.log`
- Counts: PSI-10 has 25 ACME + 10 GC_Coverter. PSI-23 has 36 ACME (incl. 7 `<date>_from_<date>_ACME.log` and 15 `<tp>_…`) + 32 IPSUG (15 `<tp>_…`). PSI-159 has 22 ACME. Names follow `YYYY-MM-DD_hh-mm[_]ACME.log`, where the date/time is when logging started (DOC-010 §8.3).
- ACME/IPSUG lines: `YYYY-MM-DD DDD hh:mm:ss:mmm~<category>~<message>`. Categories seen include `zt`, `zt.script`, `acme`, `acme.igniter`, `acme.diag`, `acmeflow…`, `ipsug`, `ipsug.Halcon`, `zt.fcf` and `zt.file…`. Lines before clock sync are stamped 2007-01-01 (ACME) or 2009-01-01 (IPSUG). The logs record script steps, `param:` dumps and the paths of the files written.
- GC_Coverter: a banner, then `[YYYY-Mon-DD_hh:mm:ss.fffff]   message` lines describing the .dat→.asc conversion. Each channel gets a line like `Channel C Using: Y_Axis_Scale_Factor = 1000000 Detector sensitivity = 100`.
```python
log = pd.read_csv(p, sep='~', header=None, names=['ts', 'cat', 'msg'], engine='python', on_bad_lines='skip', encoding='latin-1')
log['ts'] = pd.to_datetime(log.ts.str.replace(r' \d{3} ', ' ', regex=True), format='%Y-%m-%d %H:%M:%S:%f', errors='coerce')
```

### 8. Other per-test / camera `.txt`
- `<tp>.txt`: PSI-10 49 (join 42), PSI-23 114 (join 114), PSI-159 1 (join 1). Same `name:value,` format and keys as `as run<tp>.txt`. It is probably the planned (uploaded) script input, but this is not documented.
- `AcmeCameraConfigure_FusedSilica_<YYDDD>.txt`: PSI-10 9, PSI-23 17, PSI-159 23. Same `name:value,` format. Keys: `setCameraAttributes`, `frameRate`, `integrationTimeUs`, `gainDb`, `pixelFormat`, `binningX/Y`, `binningWidth/Height`, `roiXCoordinate`, `roiHCoordinate`, `roiHeight`, `roiWidth`, `whiteBalanceRed/BluePercent`, `setZoom`, `zoomPosition`, `setIris`, `irisPosition`, `setFocus`, `focusPosition`, `setFilter` and `filterNumber`. Positions are motor counts (inferred). Join on the day.
- `as runAcmeCameraConfigure_<YYYY-MM-DD>_<DDD>_<hh.mm.ss>.txt`: PSI-10 24, PSI-23 10, PSI-159 24. These are the executed versions of the files above.

### 9. Spreadsheets
- **`Final ACME Chamber Calculator - <from> to <to>.xlsx`**: PSI-10 has 2 (2019-04-09→2019-08-13 and 2021-10-28→2022-02-04). PSI-159 has 1 (2021-03-09→2021-10-21). It is a protected gas-inventory workbook with these sheets:
  - `Notes` and `Changelog`.
  - `EventData`, with 112 columns and a 3-row header. There is one row per chamber event: Cabin Air, Vent, O2/GN2/Diluent Fill, or a test point. The columns are:
    - OP, Ignite, TPID
    - FOMA bottle IDs for Diluent/Oxygen/Fuel/Adsorber
    - Tstart/Tend (GMT)
    - ACME MFC volumes Diluent/Oxygen/Nitrogen/Fuel (standard L at 0 °C and 760 Torr)
    - Pstart/Pend (psia)
    - Source-ID, Type, Fuel Type
    - Igniter Wattage, Igniter On Time (ms), Ign_1/Ign_2 Pos (counts)
    - TM1–4 start/end (°C)
    - Burn Fraction
    - species blocks (_O2, _He, _CO2, _N2, _H2O, _Ethylene, _Methane, _Propane, _Butane, _Ethane, _H2) for Start Mixture, Event Delta, Finish Mixture (std L), Finish Mixture (%), Recirculation Loop and Adsorber-cartridge vents.
  - Lookup sheets: `SourceTable` (bottle compositions and Hastings gas-correction factors), `Property Table`, `Stoich Table`, `Mass Fraction Table`, `Equations & Constants` (chamber volume 88 L), `Pick List` and `Hastings GCF`.
- **PSI-23 `ACME Daily Test Point Log 1.xlsx` / `… 2.xlsx`**: sheets `ACME` (12 columns, empty template) and `WITH IPSU2` (15–17 columns). Rows 1–3 are a header with "Downlink Data Limit (MB) = 127,000" and a running Total. Then there is one row per test point with these columns:
  - Test Point Name
  - Script Aborts Before IPSUs Open
  - Archived Images and D/L? (bool) for each of IPSU1/HiBMS, IPSU2/LLL-UV, ACME Camera and Intensified Camera
  - Downlink data in MB for IPSU1, IPSU2, ACME and Intens, plus a total.

  Test points start at 20164A1. Join by tp → day (first 5 digits).

## CFI (PSI-39) and ground studies (PSI-115, 117, 142, 60, 62)
All counts were checked by code against the local disk (`data/raw/files/...`) and `data/processed/files.csv`. Paths below are relative to the repo root.

### PSI-39 CFI: the join key

- **Key:** test-point code (CIR id) `F<ddd><L><nn>`, e.g. `F068A03`. `ddd` is the **GMT day of year 2017** (F068 = 9 Mar 2017), `L` is a block/series letter (A, B, D, E), and `nn` is the point number within that block. The `E` after the code in camera file names (`F068A03E`) is the camera stream suffix, **not** part of the key.
- **Mapping column:** `json.loads(tests.extra)["CIR"]` (lower case, e.g. `f068a03`, from the Jan 2021 data-summary xlsx). Upper-case it and join on the code in the file name.
- **Join rate (verified):** 227/227 PSI-39 test rows have a well-formed CIR. 123 distinct codes have Radiometer+Chamber files, the set is identical for both, all 123 match a tests row, and 123/227 tests rows have files (104 have none). There are no orphan files.
- **Not strictly 1:1:** CIR `F254B06` appears on two tests rows (test_id 1419 and 1420, both 2017-09-11, both with empty d0/burn). That code has no raw files, so the 123 joined codes are 1:1.
- **Date check:** the file `PIP TimeStamp` date differs from `tests.date` for 8 rows. 1231, 1232, 1233 (F095*) and 1278, 1279, 1280 (F160*) are GMT runs after midnight, so they are a local/GMT date difference. Two are real contradictions:
  - 1237 `F121A02`: the files and the code say 2017-05-01, tests says 05-02.
  - 1301 `F180D02`: the files and the code say 2017-06-29, tests says **07-29**, which looks like a month typo.
- **Pressure check:** median chamber PT16 × 6.894757 matches `pressure_kpa` within 5 kPa for all rows except 1336, 1337 and 1338 (`F200D03`–`D05`). For those, the chamber reads about 310 kPa and tests has 303.975, a nominal 3 atm. A 1–4 kPa positive offset is normal (for example, 104 vs 101.3 kPa).

### PSI-39 Raw Data `.txt`: inventory by suffix

files.csv lists 1,793 `.txt` files, of which 1,771 are on disk. Names are `PSI-39_Raw Data_<CODE><suffix>.txt`.

| suffix | n | content |
|---|---|---|
| `_Radiometer_Readings` | 123 | radiometer time series (below) |
| `_Chamber_Readings` | 123 | chamber P/T time series (below) |
| `_Filter_Positions` | 123 | 1 Hz log: AS phase text, igniter W/status, illumination, filter/CFI mode, camera exposure/gain |
| `_MDCA_CFI_Testpoint_Settings` | 123 | 1 data row: needle/igniter/dispenser profiles, positions, volumes |
| `_INTNS_`, `_HIBMS_`, `_HIBMS_CFI_`, `_Color_`, `_MDCA_Color_Camera_Settings` | 123 each (615) | 1 data row of camera config (frame rate, exposure, gain, ROI) |
| `` (bare `<CODE>.txt`) | 121 | test-point summary: igniter on-time/W, **event timestamps** (AS Started, Needles Retract, Burn to Completion/Igniter On, Igniter Off, AS Completed), per-camera image ranges, a per-second table |
| `A` / `C` / `D` | 115 / 79 / 114 | camera frame index (2 header lines, then fixed-width CSV: ImgNum, …, Mseconds, Delta [ms], Date, MTimeStamp, FileName; `D` adds WaveLength [nm]). About 30 fps |
| `_Comments` | 121 | free-text data-integrity log (not numeric) |
| `FLEX-<id>_{RadiometerData,DropletData,ColorCamData,CoolFlameData,TestSheet}` | 24, 24, 24, 17, 22 (111) | reduced per-test data keyed by **FLEX test_id directly** (24 ids, 24/24 in tests) |

Other PSI-39 files:
- **`.meta` (230):** per-image-sequence camera key:value config, first frame `_00000` and last frame `_99999`. Names are `<yyyymmdd>_<hhmmss.mmm>_INTNS_[F]<code>E_<frame>.meta`.
- **`.metadata` (113):** CSV frame log (Filename, BufferIncomplete, …, TickTimestamp, msecs, rate [fps ≈ 30]).
- Across both, 116 distinct codes match tests (116/116). 48 names **omit the leading `F`** (e.g. `INTNS_068A03E`), so prefix `F` before joining.
- **Analyzed `.pxp` (1 on disk, `FLEX-1206_SummaryGraph.pxp`, 77 kB):** Igor packed experiment, little-endian record headers (first record `Misc_Start`, MacRoman). From byte inspection only, it holds waves `Droplet_Data`, `DA_Do_sq`, `t_Do_sq`, `FlameDiameterF_mm`, `ColorCam_Data`, a fit `fit_DA_Do_sq` with `W_coef`/`W_sigma`, and graph macros. It is a d²-law fit plot for test 1206. The 28 Raw Data `.pxp` files are not downloaded. Not decoded.

### PSI-39 `<CODE>_Radiometer_Readings.txt`

Encoding is ASCII and the delimiter is `,`. There is 1 header row; `PIP TimeStamp` is quoted. All 123 files share one identical 208-column header and have 139–250 rows (median 173). No NaN values were found.

**Time base:** one row per second (every file has a median Δt of exactly 1.000 s). Each row packs **100 samples per band**, so the effective rate is **100 Hz** (the header says "100HZ").

| column(s) | meaning | unit (source) |
|---|---|---|
| `PIP TimeStamp` | row time, µs resolution | GMT (header) |
| `MAIN_COMPUTER_TIME(GMT)`, `MAIN_COMPUTER_MILLISECONDS(N/A)` | main-computer clock, s + ms (0–999) | GMT (header) |
| `AUTOMATED_SEQUENCE_IN_PROGRESS(N/A)` | Yes/No | — |
| `RADIOMETER_100HZ_FRAME_TIME(GMT)`, `RADIOMETER_100HZ_FRAME_MILLISECONDS(N/A)` | start time of the 100-sample frame; runs 1.2–1.8 s behind PIP time | GMT (header) |
| `IGNITER_POWER_STATUS(N/A)` | On/Off. **Ignition marker**: 3–15 "On" rows per file | — |
| `IGNITER_CURRENT_MONITOR(Adc)` | igniter current | A DC (header) |
| `NARROW_BAND_RADIOMETER_SAMPLE_00..99(VDC)` | narrow-band (water-vapour band per the spreadsheet "Peak Water Vapor Rad", inferred) radiometer, sample k at frame_time + k·10 ms (inferred) | V DC (header) |
| `WIDE_BAND_RADIOMETER_SAMPLE_00..99(VDC)` | wide-band radiometer | V DC (header) |

**Values and sentinels:**
- Raw voltages lie on a ±10 V rail. The baseline is about −9.7 V before ignition.
- The share of samples at the −9.99/−10.0 rail is 3.8e-5, and at ≥ 9.95 V it is 1.4e-6. Treat both as clipped.
- No V→W calibration is given in the file. The FLEX `RadiometerData` files are in W, but the conversion is unknown.

### PSI-39 `<CODE>_Chamber_Readings.txt`

Encoding is ASCII, the delimiter is `,`, and there is 1 header row. All files have 129 columns and 348–520 rows (median 442), with Δt = 1 s. The chamber log starts about 1 s before the radiometer log and covers a longer window.

| column(s) | meaning | unit (source) |
|---|---|---|
| `FCU TimeStamp` | row time | GMT (inferred, same clock as PIP) |
| `FCU_MP_PT16/17/28/29(PSIA)` | chamber pressure transducers, 1 Hz | psia (header) |
| `FCU_MP_TM1..TM4(Deg C)` | chamber temperatures, 1 Hz | °C (header) |
| `FCU_PT16_INDEX_0..29(PSIA)` (and the same for PT17, PT28, PT29) | 30 sub-samples per second, about 30 Hz (inferred) | psia (header) |

**Values and sentinels:**
- 51,850 rows have all 30 INDEX slots filled. In 2,569 rows only `INDEX_0` is filled, and the other slots hold about −0.04/−0.01/0.00. Treat values below 1 psia as missing.
- `INDEX_0` differs from `MP` by at most 0.11 psia.
- Observed ranges are pressure 7.0–74.4 psia (about 0.5–5 atm) and temperature 23–29 °C.

### Is it a clean per-test time series?

Mostly yes. The 123 codes join 1:1 to tests rows via `extra.CIR` (except the duplicate F254B06, which has no files). Both files have one row per second with fixed headers. In every joined test, the radiometer window after ignition (88–169 s) is longer than `burn_time_s`. To build features you need:

1. **Key:** `CIR.upper()` → `F...` in the file name.
2. **Time:** parse `PIP TimeStamp` (GMT). Expand each radiometer row into 100 samples at 10 ms spacing from `RADIOMETER_100HZ_FRAME_TIME` + `_MILLISECONDS`.
3. **Ignition t0:** use `AS Burn to Completion/Igniter On` from the bare `<CODE>.txt` (ms precision), or the first `IGNITER_POWER_STATUS == "On"` row.
4. **Igniter-off marker:** `AS Igniter Off/Retract Start`. **End of burn:** t0 + `burn_time_s` (tests) or `AS Completed`.
5. **Channels:** narrow and wide band in V (subtract the pre-ignition baseline). Chamber PT16 (psia ×6.894757 → kPa) and TM1–4 (°C) give conditions and the pressure rise.
6. **Masks:** clip rail values. Chamber INDEX slots below 1 psia are missing.

```python
import pandas as pd, json
d = "data/raw/files/PSI-39/Raw Data/PSI-39_Raw Data_"
rad = pd.read_csv(d + "F068A03_Radiometer_Readings.txt", parse_dates=["PIP TimeStamp"])
nb = rad.filter(like="NARROW_BAND").to_numpy().ravel()   # 100 Hz, V
ch = pd.read_csv(d + "F068A03_Chamber_Readings.txt", parse_dates=["FCU TimeStamp"])
t0 = rad.loc[rad["IGNITER_POWER_STATUS(N/A)"] == "On", "PIP TimeStamp"].min()
```

### PSI-39 `FLEX-<id>_*.txt` (reduced data)

**Format:**
- Line endings are **CR only** (classic Mac), so `wc -l` reports 0. pandas handles this.
- The delimiter is a tab, with 1 header row (units are in the header names).
- TestSheet is free text (latin-1). It holds the date, GMT time, `CIR Test Number`, ambient P (atm) and mole fractions, D0, kavg, Dext and comments.

**Columns** (units from the header):

| file | columns |
|---|---|
| RadiometerData | `RadiometerTime_sec`, `TotalWideBandPower_W`, `TotalNarrowBandPower_W` (about 100 Hz, starts −52…−73 s, i.e. time relative to ignition, inferred) |
| DropletData | `DropletTime_sec`, `DropletDiameter_mm` (30 Hz) |
| ColorCamData | `ColorCamTime_sec`, `ColorCamFlameDiameter_mm`, `ColorCamFlameStandoff` (unit unknown) |
| CoolFlameData | `CoolFlameTime_s`, `CoolFlameDiameterFWHM_mm`, `CoolFlameDiameterP2P_mm` |

**In `timeseries`:** each of the 24 tests has a second recording, `test_point = "FLEX-<id>-reduced"` (the raw
radiometer recording `F…` stays the default for the test id). The four data files are stacked on their common time
axis as published, one row per file sample, so the other files' columns are empty in that row; nothing is
interpolated and zeros are kept. Channels: `droplet_diameter_mm` (plus `droplet_x_mm`, `droplet_y_mm` in two tests),
`flame_diameter_mm`, `flame_standoff`, `cool_flame_fwhm_mm`, `cool_flame_p2p_mm`, `narrow_band_power_w`.
`TotalWideBandPower_W` is left out. Time zero is ignition: the last time with a hot-flame diameter above zero equals
`tests.burn_time_s` within 0.13 s for the 23 tests that have both. Feature columns: `reduced_files`,
`droplet_diameter_first_mm`, `droplet_diameter_min_mm`, `flame_diameter_max_mm`, `hot_flame_last_s`,
`cool_flame_fwhm_max_mm`, `cool_flame_last_s`, `narrow_band_power_max_w`; unreadable files are named in
`features_note`. The burning-rate constant is not recomputed: the investigators' value is `tests.burn_rate_k_mm2_s`.

**Oddities:**
- The `ColorCamData` file of FLEX-1227 holds the cool-flame columns, not the colour-camera ones.
- `TotalWideBandPower_W` is about **−5.4e6** in all 21 readable files, which is not physical. Use the narrow band, or treat the wide band as uncalibrated.
- Zeros mark lost tracking at the end of a series.
- 5 files are not text:
  - FLEX-1227 and FLEX-1239 RadiometerData are actually **PDF**.
  - FLEX-1248 Droplet/Radiometer and FLEX-1249 TestSheet are unknown binary.
- The TestSheet CIR agrees with `extra.CIR` for all readable sheets (1249 is unreadable).

```python
f = pd.read_csv(d + "FLEX-1264_RadiometerData.txt", sep="\t")
```

### PSI-115 Analyzed Data `.dat` (44 files, ground simulation, no tests rows)

Names follow `<8|10>cm<Gravity|NoGravity>[NoTF_]<Quantity>.dat`, plus 2 `*_sGrid_grid3d.dat` grid files and `nodeDiameters.dat`. They are plain-text Fortran output, ASCII, with one value per line.

**Field files:**
- Header line `960 240 1 1` (ni, nj, nk, nvar), followed by 230,400 values in i-fastest order (verified).
- Units are inferred per the digest and range checks: U/V/uR/vR in units of U0, Temperature = T/T0 (1.00–1.58), SpeciesMF/VaporMF as mass fraction, Vort as unknown.
- NumDen/NucRate are log10 values (m⁻³ and m⁻³ s⁻¹, per the digest). **Sentinels:** `-20` (log of zero) and the literal `-Infinity`.

**Other files:**
- **Grid:** header `960 240 1`, followed by x, y, z blocks of 230,400 each. x runs 0–40 and y ±3.409, in units of L0 (4.4 mm per the digest). z is 0.
- **PSD files (about 44 lines):** `<bin> <value>` with bin edges in `nodeDiameters.dat` (m, inferred). The first bin can be about 5e20, which is the vapour node.
- **Snapshot time:** t = 7 s (digest).

```python
import numpy as np
v = np.loadtxt(p + "8cmGravityTemperature.dat", skiprows=1).reshape(240, 960)  # j, i
g = np.array(open(p + "8cm_sGrid_grid3d.dat").read().split()[3:], float).reshape(3, 240, 960)
```

### PSI-117 Analyzed Data `.csv` (9) + ReadMe xlsx (no tests rows)

These are figure data behind 5 papers. Encoding is UTF-8 **with BOM** (except `MST_2024_Kavg`), CRLF line endings, and `,` as the delimiter.

**Layout:**
- There is 1 header row.
- Several **side-by-side column blocks** are separated by empty columns, with an `EXP`/`Model` label in the first column. These are not tidy tables.
- Units are in the headers: t/time in s, d² in mm², dflame/Dext in mm, K in mm²/s, T in K, Q/Radiance in W, P in atm. `MST_2024_Dext` "Pressure" has no unit.

**ReadMe xlsx:** maps each file to fuel, do (mm), P (atm), XO2/XN2/XO3|XHe, DOI and figure number.

**Oddities:** the `PROCI_2019_*` time series start with t = 0 and 1e-10 rows (model initial condition).

```python
df = pd.read_csv(p + "PROCI_2019_Stable_Cool.csv", encoding="utf-8-sig")
blocks = [b.dropna(how="all") for b in np.split(df, np.where(df.columns.str.startswith("Unnamed"))[0], axis=1)]
```

### PSI-142 Analyzed Data xlsx (1 workbook, no tests rows)

The workbook is `PSI data summary Princeton with links.xlsx`. It has a `data summary` sheet (Data ID, publication, figure #, description) and sheets `data ID 1`–`8`.

**Layout:**
- Each sheet has a 2–3-row title.
- Each sheet has side-by-side blocks with header labels plus units:
  - Yf with `aCFE`/`aHFE (1/s)`
  - `a`, `ϕ_HFE`, `ϕ_CFE`
  - `distance [cm]` with `PLIF signal [a.u.]` or `chemi. signal [counts]`
  - `location [cm]` with `temperature [K]`
  - `Xf` with `T_max [K]`

**Oddities:**
- In `data ID 6`, the nC10 and nC7 blocks have their distance and signal columns visibly swapped or shifted relative to nC12.
- The summary sheet and the workbook disagree on which of IDs 1 and 2 has ozone (per the digest).

```python
x = pd.read_excel(p + "PSI data summary Princeton with links.xlsx", sheet_name="data ID 1", header=3).dropna(axis=1, how="all")
```

### PSI-60 / PSI-62

files.csv has **one file each**: an ISA-Tab metadata zip of 7.7 kB / 9.7 kB. The study sheets hold only placeholder rows. There are no numeric data and no tests rows, so there is nothing to decode.

## Saffire-I/II/III, BASS/BASS-II, SLICE, FLEX/FLEX-2
Scope: numeric files only (no imagery). Paths are relative to `data/raw/files/<acc>/<category>/`, and every file is prefixed `<acc>_<category>_`. Workbooks were opened with openpyxl `read_only=True`, and only the first 50 rows of each sheet were read. "dims" is openpyxl's `max_row x max_column`. It counts formatted blank rows, so it overstates the real row count (see the Saffire-III note). Join rates were checked with code against `data/processed/tests.parquet` on the key `(accession, test_id)`.

### Saffire-I (PSI-98) and Saffire-III (PSI-100): per-sample sensor workbooks

| file | acc | sheets (dims) | first timestamp (UTC, from epoch) | -> test_id |
|---|---|---|---|---|
| `Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx` (25 MB) | PSI-98 | `Calibrated Data` (20002x73), `Camera Data` (18126x9) | 2016-06-14 20:44:03 | S1 |
| `Saffire-I Sample 2 Sensor Data Complete TM graphs.xlsx` (25 MB) | PSI-98 | `Calibrated Data` (32601x73), `Camera Data` (18152x9) | 2016-06-14 20:55:38 | S2 |
| `Saffire III Sample 1 Sensors.xlsx` (22.5 MB) | PSI-100 | `Calibrated Data` (32601x65) | 2017-06-04 21:13:31 | S1 |
| `Saffire III Sample 2 Sensors.xlsx` (5.4 MB) | PSI-100 | `Calibrated Data` (32601x65) | 2017-06-04 21:10:16 | S2 |

**Join:** `test_id = "S" + re.search(r"Sample (\d+) Sens", file_name)`, key `(accession, test_id)`. Result: 4/4 files join and 4/4 Saffire-I/III tests rows are covered (1:1). Saffire-II (PSI-99, `2-1`..`2-9`) has **no** sensor files, so its join rate is 0/9.

**Layout:** row 1 holds channel names and row 2 holds units (blank for time and index columns and for flags). Data start at row 3, so use `header=0, skiprows=[1]`.

**Time base:** `Elapsed Time (s)` starts at 0 and steps by 0.032–0.033 s, so **about 30 Hz** (from the time column). `Epoch Time` is Unix ms in UTC. `Timestamp (ms)` is a text local time (US Eastern, UTC-4) in the form `M-D-YYYY h:mm:ss.fff PM`. `Index` is the sample counter.

The digest gives about 660 s per run for Saffire-I, 690 s (20,909 rows) for Saffire-III S1 and 160 s (4,848 rows) for S2. I did not re-verify these durations because I read only 50 rows.

**Channels (`Calibrated Data`).** Units come from the header in row 2. Sensor locations come from the evidence text "Saffire-I, II, and III Diagnostics" table in `SAFFIRE Objectives…pdf`, p3.

| column(s) | meaning | unit |
|---|---|---|
| Average Fan Speed | test-section fan | RPM |
| CO2 | CO2 mole fraction, solid-state sensor in avionics bay | % |
| O2 | O2 mole fraction, sensor at avionics-bay inlet | % |
| Anemometer 1, 2 | flow velocity, one on each side of sample | cm/sec |
| Ambient Pressure | avionics-bay pressure | PSIA |
| Radiometer 1–4 | flame radiative flux (2 viewing front, 2 viewing back of sample) | mW/cm2 (S-I S1); "mw/cm^2" elsewhere |
| *Saffire-I only:* `R1..R4 Avg 0-50 s` + `Downstream Front`, `Upstream Front`, `Upstream Back`, `Downstream Back` | Avg = a single value in row 3 (pre-burn baseline, 0–50 s); the named columns = Radiometer n minus baseline. The mapping is R1=Downstream Front, R2=Upstream Front, R3=Upstream Back, R4=Downstream Back. In S2 the six columns have no header name or unit, but their positions are identical. | mW/cm2 (S1 header); S2 unit inferred |
| Humidity | relative humidity | % |
| Test Section Inlet Temp | flow inlet | Degrees C |
| Plume Temp 1–6 (TC1–TC6) | plume thermocouples | Degrees C |
| Sample Temp 1–6 (TC7–TC12) | thermocouples embedded in the sample | Degrees C |
| Radiometer Temp 1–4 | radiometer body temperature | Degrees C |
| Igniter Current / Igniter Voltage | igniter drive | Amps / Volts |
| Avionics H&S Temp 1–3; Avionics 24V; PC104 5V, -12V, +12V | housekeeping | Degrees C / Volts |
| Igniter Voltage Set Point, Fan Speed Control | commands | unknown (values about 0 and 3.7–4.3) |
| Igniter Power Enable, Igniter Select 1–9, Smoke Wire Select, LED Power 1, Camera 1/2 Trigger, GSE DIO0/1, Camera 1/2 Power Control, Anemometer Power Control 1&2, O2 & CO2 Power Control, Test Section Fan Power Control | discrete flags | 0/1 |
| Fan Tach /100 | equals Average Fan Speed / 100 | RPM/100 (inferred) |

**Missing channels:** there is no CO channel, no flow-meter channel beyond the two anemometers, and no gas-temperature channel at the outlet.

**`Camera Data` (Saffire-I only):** row 1 holds the group labels `Camera 1` and `Camera 2`, and row 2 holds the headers `Time (s), Epoch Time (ms), Exposure, Gain` (a blank column separates the two cameras). The time is on the same `Elapsed Time` base and starts at **about 55.0 s** at about 30 fps, which marks the start of sample imaging.

**Burn window:** there is no explicit marker. To find it, use the rising `Igniter Current` / `Igniter Power Enable` (ignition), the start of `Camera Data` (about 55 s, Saffire-I), and the `Downstream/Upstream` radiometer rise. tests.parquet `burn_time_s` gives 420 s for PSI-98 S1 and 70 s for S2, and NaN for Saffire-III.

**Verdict:** these are clean per-sample-burn time series at about 30 Hz, and they join 1:1 to tests rows for PSI-98 and PSI-100 (4 tests). They are usable for per-test features once the radiometer offsets are handled.

**Oddities and sentinels:**
- Raw radiometers have a negative offset (about -12 to -18 mW/cm2) before ignition. Use the baseline-subtracted columns (Saffire-I) or subtract the 0–50 s mean yourself (Saffire-III).
- Sample thermocouples TC7–TC12 are noisy, jumping by ±1–3 °C between samples.
- In Saffire-III, S2 was recorded before S1 (S2 started 3 min 15 s earlier). The MergeResult frame times agree: S2 at 21:11:11 UTC, S1 at 21:14:26 UTC.
- The sensor O2 reads **22.6 % (PSI-98 S1)** and **22.3 % (S2)**, while tests.parquet `x_o2_min/max` gives 0.215–0.217 and 0.215. For Saffire-III the sensor reads **19.76–19.81 %**, and tests `x_o2_ambient` is NaN for both rows.
- Anemometer readings agree with tests `flow_cm_s`: about 19–21 cm/s for PSI-98 (20) and about 24.4–25.5 cm/s for PSI-100 (25, already corrected from 30).
- Ambient pressure is 14.84 PSIA (about 102.3 kPa) for Saffire-I and 14.42 PSIA (about 99.4 kPa) for Saffire-III, while tests `pressure_kpa` is NaN for all 4 rows.

```python
import pandas as pd
p = "data/raw/files/PSI-98/Raw Data/PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx"
df = pd.read_excel(p, sheet_name="Calibrated Data", header=0, skiprows=[1], engine="openpyxl")
df["t_utc"] = pd.to_datetime(df["Epoch Time"], unit="ms", utc=True)
df["test_id"] = "S1"; df["accession"] = "PSI-98"
```

### Saffire-I/III telemetry (PSI-98, PSI-100): low-rate, whole-mission, not per test

| file | sheets (dims) |
|---|---|
| PSI-98 `Saffire-I Telemetry Data Good Process Version.xlsx` (2.8 MB) | `RawData` 9750x48, `CygnusData` 8073x23, `CygnusSmokeDetectorData` 291x9, `CygnusPressureData` 333x10, `CygnusTemperatureData` 323x4, `SaffireData` 6084x33 |
| PSI-100 `Saffire-III Telemetry Data.xlsx` (8.7 MB) and `Saffire-III 1 Hz Telemetry Data.xlsx` (21 MB) | the same six sheets: `RawData` 73463x50, `CygnusData` 69870x25, `CygnusSmokeDetectorData` 58307x9, `CygnusPressureData` 58306x10, `CygnusTemperatureData` 58306x4, `SaffireData` (48x33 in the first file, 11450x33 in the 1 Hz file) |
| PSI-100 `Saffire_Data_Table2017.161.00.42.03-EU.csv` (11,450 rows x 47) | the only `Saffire_Data_Table*.csv` that exists |
| PSI-100 `Raw telemetry file.csv` (3,972 rows x 47) | |

**Header row:** row 1 is the header in all sheets, except `CygnusSmokeDetectorData`, where row 1 holds group labels and row 2 holds the headers.

**`RawData` columns:**
- `RelativeSeconds` is in ms despite its name (inferred: it steps by about 1000).
- `CygnusTimestamp` and `SaffireTimestamp` are epoch ms.
- `Cyg-Saf TS (ms)` is their difference.
- `Radiometer1..4Value`, `Anemometer1/2`, `FanTachometer`, `SmokeWireV/I` and `Sample1..9IgniterV/I` have no units in the header. I infer they match the sensor workbook (mW/cm2, cm/s, RPM, V/A).
- The Cygnus vehicle channels have units in their headers: `PCM Air Temp (degC)`, `PCM Press (psi)` (Saffire-I) or `PCM Press EPS1/2/3 (psi)` (Saffire-III), `PCM Press/Temp (psi/K)`, `FIZ 1/2 Smoke Detector Obscuration/Scatterometer (V)`, `FIZ 1/2 Cabin Fan delta P (Pa)`, `body rate x/y/z (rad/s)` and `acceleration x/y/z (m/s^2)`.
- The last two columns are `Saffire Repeat?` (bool) and `Row to Row Delta T (ms)`.
- `SaffireData` adds `delta timestamp (ms)`, `Relative Time (ms)/(s)`, `Rel-to-Cygnus Time (s)` and `Tach/100`.

The CSVs carry the same 47 channels under flight mnemonics. For example, `P@sfsHk.Radiometer1value` is Radiometer 1, `P@PCM_ETS_TEMP_SIG` is the PCM air temperature, `P@F1PCM_AIR_PRES_EPS1_SIG_POS` is PCM pressure EPS1, `P@GNCAttitudeNavigatorShared.omegaEst_bdy.elements[0..2]` are the body rates and `P@GNCImuSensor.imu[0].currentMeas_Bdy.acc.elements[0..2]` are the accelerations.

**Sampling (from the time columns):**
- Cygnus rows arrive about every 1.0–1.25 s, and every 0.5 s in the EU csv (median dt 498 ms).
- New Saffire values arrive every **30 s** in `SaffireData` (Saffire-I and the Saffire-III Telemetry file) and every **1 s** in the EU csv and the 1 Hz file.
- Between updates, values repeat (`Saffire Repeat?`).

**Sentinels:** these are constants written before a channel has its first update.
- Radiometers: about -4077/-4061/-3867/-3954 (Saffire-I) and -4002.47/-4001.98/-3844.32/-3969.93 (Saffire-III).
- Anemometers: about -72/-66 and -76.19/-75.49.
- FanTachometer: -69894 and 77938.3.
- Igniter V/I: -80.84/-12.59 and -7.378/-3.052.
- Cygnus channels: 0 means no update.
- Timestamps of about -6.2e13 ms (year 0) and `SaffireTimestamp = 0` are null.
- Saffire-I `RawData` row 2 contains `#REF!`.

**Oddities:**
- `Raw telemetry file.csv` stores `CygnusTimestamp`/`SaffireTimestamp` rounded to `1.4966E+12` (only 3–4 distinct values), so it has no usable time.
- In the 1 Hz file and the EU csv, the Cygnus time is 2017-06-05 while the `SaffireTimestamp` maximum is 2017-06-04 21:30 UTC. This is likely a next-day downlink of on-board data (inferred).
- The `MergeResult-raw` "Date / GMT" column shows 2017-06-03, one day earlier than its own epoch column (2017-06-04).
- There is no O2, CO2 or thermocouple data at all in the telemetry.

**Join:** there is no per-test key. To slice by test, use `SaffireTimestamp` within the sensor-workbook epoch window (or the `SampleNIgniterI` rise). Telemetry join rate as files: 0 (they are mission-level).

```python
tm = pd.read_excel(p_tm, sheet_name="SaffireData", engine="openpyxl")
tm = tm[tm["SaffireTimestamp"] > 1e12]
tm["t_utc"] = pd.to_datetime(tm["SaffireTimestamp"], unit="ms", utc=True)
eu = pd.read_csv(p_eu); eu = eu[eu["SaffireTimestamp"] > 1e12]
```

### Saffire Science Documents xlsx (PSI-98: 1 file, PSI-100: 2 files): image inventories, not sensor data

**Files and sheets:**
- `SAFFIRE-1_MergeResult-jpeg_Update_Final_v2.xlsx` has the sheets `PreFlowVis/PostFlowVis/Sample1/Sample2 - jpeg [TimeSort]`, `BIT - jpeg` and `Received - jpeg [Corrupted|Zips]`.
- `SAFFIRE-III_MergeResult-jpeg_Final.xlsx` and `…-raw_Final.xlsx` have the sheets `Requested/Received - RAW|jpeg`, `BIT`, `PreFlowVis`, `PostFlowVis` and `Sample1/Sample2 - raw|jpeg`.

**Columns:** `Timestamp`/`EpochTime` (Unix ms, stored as a string in the raw workbook), `Time delta` (a datetime offset from 1970, an Excel artefact), file IDs in hex and decimal, file name `S<n>C<cam>-<epoch>.jpeg|raw`, received/corrupt flags, file sizes in bytes, and (raw only) `Exposure` and `Gain`.

**Rates:** frames arrive about every 33 ms (30 fps). Saffire-I has about 36.5k rows per sample. Saffire-III has 38,051 rows for S1 and about 30k rows for S2 (the digest says 6,276 S2 frames were received).

**Join:** the sheet name `Sample<n>` maps to `S<n>`, which joins 4/4. These files are useful only for frame timing.

### Saffire-II (PSI-99)

Only `SAFFIRE-2.csv` (the experimental table, which is the tests source) and a metadata zip exist. There are **no sensor or telemetry files**.

### BASS (PSI-26) and BASS-II (PSI-25)

**Raw data:**
- PSI-26 has 59 zips (images; the `*_txt.zip` files probably hold text logs) and 114 mp4. None are downloaded, so nothing was decoded.
- PSI-25 has 125 downloaded PDFs (`GMT2014_<doy>_BASS_S<sample>_TPB<n>_ProofSheet.pdf`, image proof sheets), 264 zips and 296 mp4 (not downloaded). It has **no numeric raw data**.

**Numeric xlsx that exist (Science and Reference documents, one row per test):**

| file | sheets | header | key -> join |
|---|---|---|---|
| PSI-25 `BASS-II_Test.Matrices.xlsx` | one sheet per PI group (6 sheets, max 30 rows each) | row 1 | `Test no.` (B1.., F1.., M1.., O1.., P1.., T1..) = test_id: **129/129** rows and **129/129** tests |
| PSI-26 `As Run_Test Matrix.xlsx` | `as run matrix` (main), `2012`, `2013`, `Data without TP`, `TP without Data` | title in row 1, group labels in row 2, headers in **row 3** (in sheet `2013`, headers are in row 2) | `Test no.` (column D) = test_id: 121 rows, **117/117** unique tests (the 121 tests rows include 4 duplicated ids) |
| PSI-25 `Fan calibration data.xlsx` | `Fan Calibration data` (35x109) | free-form blocks | none (calibration, per date) |

**BASS-II matrix columns:**
- Date, GMT day-of-year, Test no., Sample no., Material, Flow restrictor (count), Fan display, Air display (display units), Radiometer gain (1000/250/50/10) and total frames shot.
- Initial and final O2 (% by vol), CO2 (% by vol) and CO (ppm). Units come from the header.
- Some cells hold lists such as `'89,62,50,41'`, and sample numbers can be strings such as `'185M'`.
- Initial O2 vs tests `x_o2_ambient`: 129/129 agree.

**BASS As Run columns:**
- Date, approximate start time (GMT), as-run number, Test no., Sample no., material, igniter, flow restrictor and sample distance.
- Fan display and Air display, written as ramps such as `66 > 52`.
- Radiometer gain and display, GN2 pot and display, and camera settings.
- `O2 % by volume` (a fraction despite the name, e.g. 0.221), `pressure, atm`, `CO2, mm Hg`, and observations (free text).
- Compared with tests: pressure agrees 117/117. O2 agrees except for **tests 85 and 100**: the matrix gives 0.211, while tests gives 0.168 and 0.173 (flagged `o2_from_notes`/`ramped`, so not an error).

**Fan calibration:**
- The sheet contains blocks per date and per number of restrictors (none, 1 or 2). Each block has the columns `Pot`, `Fan Display`, `Air Display`, `Fan V` and `U cm/s*`.
- The footnote gives `U = 1.0066*(AIR)` cm/s, based on SPICE calibration 56 mm downstream.
- The fan turns off below about 3.8 V.

**Not read:** `Planned_Test Matrix.xlsx` (PSI-26) was deliberately not opened.

```python
m = pd.concat(pd.read_excel(p25, sheet_name=None, header=0).values(), ignore_index=True).rename(columns={"Test no.": "test_id"})
a = pd.read_excel(p26, sheet_name="as run matrix", header=2).rename(columns={"Test no.": "test_id"})
a["test_id"] = a["test_id"].astype(str).str.strip()
```

### SLICE (PSI-106)

Only `Slice.csv` (the experimental table, the tests source: 12 `test_day` rows `PSI-106-r1..`) and a metadata zip exist. There is **no raw or analysed numeric data**.

### FLEX (PSI-69) and FLEX-2 (PSI-68)

files.csv lists **exactly one file each**: `FLEX.csv` (274 tests rows) and `Flex2.csv` (8 `condition_set` rows), both experimental tables and the source of the tests rows. There is no raw or analysed numeric data (no droplet-diameter or radiometer time series) and no metadata zip.

## SAME-R (PSI-101), SAME (PSI-102), SPICE (PSI-107), DAFT (PSI-47)
Scope: numeric files in the Raw Data and Analyzed Data categories that are downloaded locally (`data/processed/files.csv`, `downloaded=True`).
I checked every join rate below with code against `data/processed/tests.parquet`. Unit sources: **hdr** = column header,
**doc** = a document or note sheet in PSI, **inf** = inferred from the values, **unknown** = could not be determined.
Paths are relative to `data/raw/files/<acc>/<category>/`.

---

### PSI-101 SAME-R: housekeeping CSVs `HKPData_gmt<ddd>_<n>.csv`

| Item | Value |
|---|---|
| Files | 44, Raw Data (`HKPData_gmt211_2.csv` … `HKPData_gmt252_6.csv`; one is named `gmt242_6_run89.csv`). `<ddd>` = GMT day of 2010, `<n>` = download index for that day, **not** the run number |
| Format | ASCII, comma-separated, 1 header row, 98 columns, no index |
| Rows | 558–3 824 per file (68 698 in total) |
| Time | `TimeString` `YYYY/DDD/hh:mm:ss` (GMT), `Time` = Unix epoch s. Median Δt = 1 s, so **1 Hz**. There are repeated seconds (Δt=0; 0–70 per file) and occasional 2 s gaps |
| Run key | The run number is **in the data**: `TestNumber` (0 outside a test) |
| Join | key = `str(TestNumber)` for rows with TestNumber>0, matched to `tests.test_id`. **44 of 44 files join**, covering 45 distinct runs (63–108). `gmt252_5` holds 2 runs (103, 105). 21 base runs have no CSV: 48–57, 71, 72, 74, 83, 88, 104, 109, 110, 111, 113, 114 |
| Sentinels | `PTrakMeasurement = -999` (1 974 rows, instrument not ready). `-1.#IND` (C runtime NaN) in `GasPlumeTemperature` (pandas reads it as NaN by default). Power-up rows (`RunMode` 0/1, 236 rows) carry rail values: −10 V on the analogue channels, −400 on LFE, −500/−50 on the pressures |
| Oddities | `gmt251_4.csv` repeats the header line at line 6, so read with `dtype=str` and drop rows where `TimeString=='TimeString'`. Files start before the test and end after it (TestRunning=1 for 63 398 / 68 698 rows) |

Columns (98). Units come from the header suffix unless stated otherwise.

| Group | Columns | Meaning / unit |
|---|---|---|
| Clock/state | `TimeString`, `Time`, `RunMode` (0–4), `TestNumber`, `ElapsedTestTime(Secs)` [s, hdr], `SampleNumber`, `CarouselNumber`, `DriveKBRemaining` [kB, hdr], `CycleCounter`, `WatchdogReset`, `EnetSelect`, `EnetOverride`, `OKStatus`, `EventSet`, `EventCode`, `TestRunning`, `12VDCHeaterEnable`, `HeatingInProgress`, `SampleHeaterOverride` | flags and counters; meaning of the RunMode codes is unknown |
| Smoke generation | `GasPlumeTemperature(DegC)` [°C]; `SampleResistance(Ohms)` [Ω] (heating wire, giving Rt/R0 → sample temperature, doc: digest) | |
| Detectors | `ISSDetectorObscurationMeasurement(Volts)`, `ISSDetectorScatterMeasurement(Volts)`, `STSDetectorMeasurement(Volts)`, `IonDetectorAMeasurement(Volts)`, `IonDetectorBMeasurement(Volts)` [V] | ISS light-scattering detector, Shuttle ionisation detector, First Alert ionisation chambers (M1) (doc: digest) |
| Particle instruments | `PTrakMeasurement(PtPerCC)` [particles/cm³] (M0, behind a diluter, so not ambient); `DustTrakAMeasurement(MgPerM3)`; `DustTrakBMeasurement(MgPerM3)` [mg/m³]; `DustTrakA/BAnalogMeasurement(Volts)` [V] | **DustTrakA holds integer codes 10009–22997, not mg/m³.** The digest says DustTrak A was replaced by the MPASS prototype in SAME-R, so this channel is probably MPASS output (inf; encoding unknown) |
| Flow/pressure | `LFEFlowRate[AT08](SCCM)`, `VSOSetpoint[PN23](Volts)`, `ZeroLFE`, `MFCSetpoint(LPM)`, `MFCMassFlowRate(LPM)`, `MFCTemperature(DegC)`, `MFCPressure(PSIA)`, `MFCAnalogSetpoint[BN19](LPM)`, `MFCAnalogFlowRate(LPM)`, `GN2MainPressure[PN02](PSIA)`, `GN2RegulatedPressure[PN12](PSIG)`, `VacuumPressure[VR04](PSIA)`, `DriveSidePressure[BN02](PSIA)`, `SampleSidePressure[AT20](PSIA)` | units from hdr; the bracketed tags are hardware IDs |
| Instrument/hardware state | `ThermalPrecipitatorPre/PostAgeChannel`, `PTrakState`, `PTrakKeySelect`, `PTrakPowerMeasurement(Volts)`, `DustTrakA/BState`, `DustTrakA/BKeySelect`, `ProximitySensor1/2/4(Volts)`, `CarouselProximitySensor(Volts)` | codes; meaning unknown |
| Discrete on/off (0/1) | `MixingFanPower` … `IlluminationLEDPower` (39 columns: power switches, 15 solenoids, thermal-precipitator heaters/valves/cable sense, STS/ISS self-test/alarm, video/camera) | boolean (inf) |

```python
import pandas as pd
df = pd.read_csv(path, dtype=str)                      # all-str because of the repeated header
df = df[df.TimeString != "TimeString"].apply(pd.to_numeric, errors="ignore")
df["t"] = pd.to_datetime(df.Time.astype(float), unit="s")
df = df.replace({"PTrakMeasurement(PtPerCC)": {-999: pd.NA}})
run = df[df.TestNumber > 0]                             # test_id = str(TestNumber); 'a' rows = aged part of same run
```

**Usable for features?** Yes, as a clean 1 Hz series per run, after filtering on `TestNumber`. It is **not** a strict 1:1 join. Each run N covers two tests rows, `N` (unaged) and `Na` (aged measurement later in the same file). The file does not mark the boundary between the two; it has to be cut from the timeline (the averaging windows are only in the analysed xls). Coverage is 45 of 66 base runs.

---

### PSI-101 SAME-R: per-run analysed workbooks `<yyyy>_<ddd>_<hh>_<material>_run<NN>.xls`

| Item | Value |
|---|---|
| Files | 72 `.xls` in Analyzed Data: **70 run workbooks**, plus `Copy of 2010_235_10_silicone_run66 test.xls` (same layout) and `TEMflowvsnoflow.xls` (a 17-row reduced table). 3 more in Raw Data (`run55 wrong`, `lampwick run 55 corrected`, `2010_211_13_silcon_run60`), plus `2010_210_10_lampwick_run57_a.xlsx` |
| Name parsing | regex `_([a-z]+)[_ ]run ?(\d+)` gives material and run. `<hh>` = GMT hour. Variants with an `a` suffix (`run63a`, `run65a`, `run60 a`, `run57_a`) are re-cuts for the aged part, not different runs. Typos: `2342` (=242), `silcon`/`silcone` |
| Join | key = run number from the name as str, matched to `test_id`. **73 of 74 workbooks join** (all except `run112`; run 112 is not in tests.parquet, see the contradictions below). They cover 66 distinct runs; only test 51 has no workbook. Material in the name agrees with `tests.fuel` for all joined files |
| Sheets | always 2: `Sheet used to Graph` and `Original (cut and paste)` |
| `Original (cut and paste)` | header row 0. It is the **same 98-column HKP layout** as the CSVs above (the downlinked HKP pasted in). `TestNumber` in it equals the run in the name for all files. Ten workbooks also contain neighbouring runs: run52 and run53 (both 52+53), run88 (86, 88, 89), run103 and run105 (103+105), run104 (103+104), run106 (105–107), run110 (110+111), run113 (113+114) |
| `Sheet used to Graph` | header row 0. Usually 10 columns: `Time`, ISS obscuration/scatter, STS, Ion A/B [V], `PTrakMeasurement(PtPerCC)/1000 (Right Axis)` [10³ /cm³, hdr], `DustTrakAAnalogMeasurement(Volts)`, `DustTrakBMeasurement(MgPerM3) (Right Axis)`, `DustTrakAMeasurement(MgPerM3)`, `GasPlumeTemperature(DegC)`. Some files add HKP columns (run54, run57: full set; run60, run57_a: `TimeString`, `TestNumber`, raw PTrak, pressures, `GN2MainPressure/10`) |
| Time | `Time` in the graph sheet is the **row index in s from the start of the pasted file** (0,1,2,…; not test time and not epoch). It skips seconds where HKP skips them, so it is effectively 1 Hz |
| Sentinels | The graph sheet is a formula block pre-sized to about 3 615 rows. Rows after the data are **all-zero padding** (e.g. run58: 1 705 data rows, then 1 909 zero rows). Drop trailing rows where `Time==0`. PTrak `-999` shows up as ±0.999 in the /1000 column |
| Oddities | The sign of ISS scatter is flipped relative to HKP in some sheets. `run55` exists in 3 versions (analysed, `wrong`, `corrected`); `run60` in 3. `run65`/`run65a` etc. duplicate the same Original data |

```python
x = pd.ExcelFile(path)                                   # xlrd for .xls
o = pd.read_excel(x, "Original (cut and paste)")         # = HKP CSV schema
g = pd.read_excel(x, "Sheet used to Graph")
g = g.loc[: g.iloc[:, 0].ne(0).cumsum().idxmax()]        # cut zero padding
run = int(re.search(r"run ?(\d+)", path).group(1))
```

**Usable for features?** Use the `Original` sheet, which duplicates the CSV schema and extends coverage to runs 48–57, 71, 72, 74, 83, 88, 104, 109–114. Same caveat as the CSVs: N and Na share one timeline, and some workbooks contain more than one run, so filter on `TestNumber`. Choose one workbook per run, because of the duplicates and the "wrong/corrected" pairs. The graph sheet is a derived subset and adds nothing.

### PSI-101 SAME-R: analysed `.xlsx` (13 in Analyzed Data, 1 in Raw Data)

| File(s) | Content | Join |
|---|---|---|
| `SAME, SAME-R_Results.xlsx` (43 sheets) | Run-level reduced results. Key sheet `Reduced Data with STS Det`: header on **row 1** (row 0 = "Smoke Generation"). Columns: `Flight 1=same 2=sameR, g=ground`, `Sample Type`, `SAME #`, `Description`, `Inlet Velocity (cm/sec)`, `Rt/R0`, `Net Aging Duration` [s, inf], ISS/STS detector [V], `M0 best`, `M1 (mm/cm^3)`, MPASS 3rd/2nd, DustTrak A/B calibrated [mg/m³], `M1/M0 (micro-m)--AMD`, `Diameter of Average mass (micro-m)`, `Hatch Choate Sigma g`, `Hatch Choate Dg`, `Sample Temperature C`, `Mass Loss mg`, … (units in hdr) | key `SAME #` (int→str, keeps `a`) where Flight==2. **108 of 109 rows join**; the unjoined row is run `112`. Flight==1 rows (45) are SAME-1 runs 5–47 plus `a` variants (PSI-102) |
| `54 lampwick binneddatacorr from GWM`, `55 Lampwick`, `60 silicone`, `62 Kapton aged issue with bins`, `62 Kapton unaged`, `63/64 Pyrell aged/unaged`, `94 Kapton aged- results` | TEM particle sizing. `Results*` sheets = one row per particle from image analysis (`Area`, `Diameter`, `Volume`, `LN(D)`, `Perim.`, `Circ.`, `AR`, `Round`, `Solidity`; 94 has `XM`, `YM`, `BX`, `BY`, `Width`, `Height`). Diameters in µm (doc: "Minimum particle size 0.010 um", sheet `Comments on binned data`); area µm² (inf). `all data*` = totals/moments; `Binned data*` = 0.132 ln-width bins with dN/dlnD and dV/dlnD; `SizeDist` = fitted Dgn/σg | run number = leading integer of the name (54, 55, 60, 62, 63, 64, 94, all present as tests). Aged/unaged maps to `Na`/`N` (inf). **The `Results 64-pre-*` sheets are byte-identical in 6 workbooks (54, 55, 62×2, 63 aged, 64×2): they are template leftovers from run 64, not data for that run** |
| `thermal precipitator map updated.xlsx` | TEM grid map, 28×12 | none |
| Raw `SPV of 54-7L_21 all quarters (3).xlsx` | TEM grid quarter statistics for run 54 | run 54 |

**Not time series.** These are per-run or per-particle tables. Results.xlsx is the best source for run-level targets.

---

### PSI-102 SAME (SAME-1, 2007): analysed `.xls`/`.xlsx`

| Item | Value |
|---|---|
| Files | 53 `.xls` + 6 `.xlsx` (59). 4 `.xml` are not downloaded (zero-byte per digest) |
| Name patterns | very irregular: `GMT<ddd> Run <n> DBP.xls`, `GMT<ddd><material><n>[hkp].xls`, `GMT<ddd>dbp<n>hkp peak 1/2.xls`, `Run <n> GMT<ddd> testlog.xls[x]`, `GMT<ddd>hkp.xls`/`GMT<ddd>LOG.xlsx` (whole day), `<material>GMT257hkp[ zgy average].xls` (no run number). `<ddd>` = GMT day of 2007. "zgy average" = copy with an added averaging sheet |
| Sheet kinds | (a) **full HKP**: 98–99 columns, same schema as PSI-101 (99 = an extra blank 2nd column in `Housekeeping` sheets); sheet names vary (`Housekeeping`, `Copy of GMT255hkp`, `GMT264HKP`, `2007_277_17.eng`, …). (b) **graph subsets** (14–27 columns): `TimeString`, `Time`, ISS obsc/scatter, STS, Ion A/B, PTrak, DustTrak A/B, sometimes `Ion A delta`, plus a duplicated block with `PTrakMeasurement(PtPerCC/1000)` or `/100` and the ISS scatter sign flipped (sheets `Sheet1`, `for graphing`, `Graph Data`, `ALLGMT256`, `209D8A~1.HKP.eng`). (c) **averaging windows** (`for average`, `for aged average`, `for average_2ndAging`; 10–17 columns): a slice of (b) with `Time` restarting at the window start. (d) **command logs** (`*LOG*`, `testlog`; 7–8 columns, **no header**): GMT string, event text (e.g. `Command Received`), command, argument, two numeric codes (unknown) |
| Header row | row 0 in (a)–(c); none in (d) |
| Time | 1 Hz (median Δt = 1 s in every time sheet). `Time` is epoch s in HKP sheets, but relative s in some graph/average sheets (starts at 0) |
| Run key | Name number (47 of 59 files have one) and HKP `TestNumber`. **They differ for early runs**: `DBP run 4 GMT255` has TestNumber 2; `Silicone … run 5s` has TestNumber 2, 3. From run 17 onwards TestNumber = run number. `TestNumber=998` appears in 12 files (non-science / maintenance test, inf) |
| Oddities | `kaptonGMT257*.xls` contain **GMT 254** data (TimeString 2007/254). `GMT264 Run 22 DBP.xls` and `Run 21` are the same data. Several files span two GMT days. The digest notes the same file is often saved 2–3 times |
| Join | `tests.parquet` PSI-102 has only test_ids `1`..`8`, flagged `planned_not_flown` (pre-flight EIRD matrix). A naive name-run→test_id join "matches" 10 files (runs 1, 2, 4, 5), but **0 joins are valid**: flown runs 1–47 have no tests rows |

```python
o = pd.read_excel(path, sheet_name=None)                 # pick the sheet with 'TestNumber' in its columns
hkp = next(d for d in o.values() if "TestNumber" in d.columns)
hkp = hkp.loc[:, ~hkp.columns.str.startswith("Unnamed")]
hkp["t"] = pd.to_datetime(hkp.TimeString, format="%Y/%j/%H:%M:%S")
log = pd.read_excel(log_path, header=None, names=["gmt","event","cmd","arg","code1","code2","x7"][:ncols])
```

**Usable for features?** The 1 Hz HKP is clean once extracted, but there is **no join target**: tests.parquet holds the planning matrix, not the 47 flown points. The as-flown conditions are in the final report's flight test log and in `SAME, SAME-R_Results.xlsx` (Flight==1, `SAME #` 5–47). The run identity has to be taken from TestNumber + GMT, not from file names.

---

### PSI-107 SPICE: Raw Data spreadsheets and text

There is no time series in this family. The files are a run log, image-analysis sheets and calibrations. All downloaded: 27 xls, 6 xlsx, 2 txt.

| File(s) | Layout | Columns / units | Join to tests |
|---|---|---|---|
| `Spice Flight Test Data II modified.xls`, sheet `Data record of Video and Stills` (530×43) | title row 0, **two header rows 2–3** (name + unit), data from Excel row 5 | GMT date (day number as text `045`), Date, GMT ignition/flame off/data, `No.`, Fuel, Nozzle (mm), Pressure (Pa), Fuel/Air Display (raw overlay counts), Fan, Rad, Gain, Length mm, Fuel Rate sccm, Fuel Rate (mg/s), HC Fuel Rate (mg/s), Air Rate (cm/s), Max Flame Width (pixels/mm), Flame Height Nikon (pixels/mm), Smoke Height (Y/N), comment, `# in filename`, NIKON DIMS file no., D100 file no., exposure comp., bracket EV, Nikon GMT/offset (Hr/Min/Sec), NEF saturated R/G/B, Nikon Sat (all units from the 2-row hdr). Sheet `Reference`: nozzle notes, K factors | **This is the source of tests.** `test_id = PSI-107-r<Excel row>`, i.e. `df.iloc[row-1]` with `header=None`. Check: `Fuel Display` matches in **516 of 526**; the other 10 are `Ku LOS` (9 rows, matching after whitespace normalisation) and 1 empty |
| `GMT052nikon_propy.xls`, `GMT055nikon.xls`, `GMT058nikon.xls` | sheets `overview` + one per nozzle (`1.6`/`0.8`/`0.4` or `Propy 1.6`…). Rows 0–2 are title/header, data from row 3 | `number` = NEF/DIMS image number (ISS018E0#####), `time` (GMT hh:mm:ss), `f#`, `exp (s)`, `1/exp`, colour flags, `fuel`/`air` display, `Saturation` Red/Green/Blue (fraction, inf), `Blue Max` (counts, inf), `Optimum …` | key = image number matched to the IDs parsed from extra `NIKON DIMS Exchange File No.` (regex `ISS018E0*(\d+)`). Overview sheets: **156/162, 115/119, 128/137 image rows join**, mapping to 52, 39, 43 tests rows. Many images map to one row, so this is not 1:1 |
| `Spice_Flight_Flamelength.xls` | `Calib` (ruler pixels vs mm), `FlameLength` (header row 2: `TP`, `AdobePS ruler`, `Spice ruler` mm) | TP 1–11, flame length mm (hdr) | TP numbers do not match the `review_tp` labels in extra (`P16-3`, `75P16-5`…): **no key** |
| 18 `SPICE Flow Duct Cal - <13/56> mm Station x <19/36/57> mm Height, <CENTER/INSIDE/OUTSIDE>.xls` | one sheet `Data`, 51×19. Metadata block rows 2–23 (date 2008-06-17, probe/bridge model, R0, T_op, cal-curve coefficients a–d). Table header rows 25–26, data rows 27–32 (fan settings 0–10) and row 35 (zero flow) | Fan setting, FAN/AIR reading (display counts), T (°F), probe V min/max/avg/std (V), corrected V, U (cm/s), fluctuations (cm/s), all hdr | ground calibration: maps the fan/AIR display to duct velocity; **no test join** |
| `SPICE_Airflow_Test_*.xls[x]` (3), `SPICE Flow settings_w chart.xls`, `MASS_FLOW_CALIBRATION.xls`, `SPICE_FuelFlow_411259meter.xls`, `_EngineeringUnitControl.xlsx`, `_MFC_settings.xlsx`, `__Voltage.xlsx` | small calibration tables with free-text headers | flow (sccm) vs output (V); pot setting vs pin voltage vs fuel display; velocity profiles (cm/s) | none (calibration) |
| `SmokePointReview-0g-3.xlsx` | `Smoke Point Datasheet` (header rows 2–3, 61 cols), `Reference` | reviewed smoke points: GMT, No., TP, fuel, nozzle, MWmix, Xf, displays, smoke-point length (px, mm), HC density g/m³, Tad K, viscosity … | already merged into tests as `review_*` extra (26 rows flagged `smoke_point_bracket`) |
| `045_SPICE_DSC_num.txt`, `048_SPICE_num.txt` | ASCII, 4–6 free-text header lines (path, shot/downlink day, crew), then tab-separated `ISS018E0xxxxx<TAB>DSC_nnnn` | image-number cross reference | indirect, through the DIMS number |

```python
log = pd.read_excel(p, "Data record of Video and Stills", header=None)
hdr = (log.iloc[2].fillna("").astype(str) + " " + log.iloc[3].fillna("").astype(str)).str.strip()
data = log.iloc[4:].set_axis(hdr, axis=1)
data["test_id"] = [f"PSI-107-r{i+1}" for i in data.index]   # Excel row = iloc + 1
```

**Usable for features?** There is no per-test time series in PSI-107 (the video/NEF imagery is not downloaded). The run log *is* tests.parquet. The Nikon sheets add per-image exposure and saturation, joinable many-to-one.

---

### PSI-47 DAFT: Raw Data `PTrk<n>.txt`, `DTrk<n>.txt`

| Item | Value |
|---|---|
| Files | 6: `PTrk0002-0004.txt` (TSI P-Trak), `DTrk0002-0004.txt` (TSI DustTrak). `<n>` = instrument TestID |
| Encoding | ASCII. Line ending is **`\r\r\n`**, so naive readers see blank lines |
| Header | 8 `Key: value` lines: `Instrument`, `SerialNumber`, `TestID`, `GMT` (download time, `04Mar05 hh:mm:ss`), `StartDate` (`MM/DD/YY`), `StartTime` (local instrument clock), `Units`, `Number of points` |
| Data | one value per line, no time column. P-Trak: particles/cm³; DustTrak: mg/m³ (hdr `Units`) |
| Sampling | 1 s. The workbook `Retrieved Data Summary.xls` sheet `Raw PTrak Data` has per-sample clock times 1 s apart, and `flight data 063.xls` adds `Time (sec)` 1..N. The `Headers` sheet says "Log Interval 00:01:00", read as mm:ss:hundredths? (unclear); time constant 10 s (DustTrak), 0 (P-Trak) |
| Sentinels / oddities | `DTrk0002`: 779 values vs 778 declared; the trailing extra token `2` has no line terminator (drop it). `PTrk0003`: last line `1\r\0\0`, a NUL-padded truncation (708 tokens, 707 declared). `PTrk0002` max 45 400 /cm³ against typical values below 100 (spike; kept). The HEPA zero periods are in the series (see `TIMING`) |
| Join | All 6 have `StartDate 03/04/05` = `tests.date` 2005-03-04 of **D2** (key: parsed StartDate == tests.date): **6 of 6 join to D2**, 0 to D1. Test ID 1 (D1, 22 Feb 2005) has no txt; it is only in `DAFT Flight Data GMT053.xls` |

```python
import re
raw = open(p, "rb").read().decode("ascii", "ignore").replace("\x00", "")
lines = [l.strip() for l in re.split(r"\r+\n|\r", raw) if l.strip()]
meta = dict(l.split(":", 1) for l in lines if ":" in l)
v = pd.to_numeric(pd.Series([l for l in lines if ":" not in l]), errors="coerce").iloc[: int(meta["Number of points"])]
s = pd.Series(v.values, index=pd.to_timedelta(range(len(v)), unit="s"), name=meta["Instrument"])
```

### PSI-47 DAFT: Analyzed Data `.xls` (12)

| File(s) | Sheets / layout | Notes |
|---|---|---|
| `flight data 063.xls` + 7 copies `flight data 063_{DTrk0002..4,PTrk0002..4,TIMING}.xls` | `TIMING` (event table: per test, P-Trak and DustTrak "Seconds into the video" and "seconds after log" for Log on, HEPA on/off, hose on/off, velcro start/stop, Log off), and `DTrk000n`/`PTrk000n`: column A = raw txt lines pasted in, then `Time (sec)` 1..N and value (`mg/m^3` / `pt/cc`) | identical content in all 8 workbooks (sheet names and shapes match) |
| `DAFT Flight Data GMT053.xls` | `PTrk0001`: P-Trak and DustTrak test 1 (22 Feb 2005), header block in rows 0–7, `Time (sec)` | the only copy of TestID 1, so D1 |
| `DAFT Retrieved Data Summary.xls` | `Headers` (instrument metadata for TestIDs 1–7), `Raw PTrak Data` / `Raw DustTrak Data` (header row 0: `Date<k>`, `Time<k>`, `Data<k>` for k=1..7, 1 s), `Logged Data Summary` (bag averages, mass per particle, D µm), `Voice Down Data Summary`, `P-Trak vs. DustTrak Data` | TestIDs 5–7 = 2006-08-17/21 sessions (cabin air + ARD bags), which have **no tests rows** |
| `ISS_Daft_Aug21_06 urban.xls`, `…0611zgy time hist.xls` | `Data`: voiced-down readings every 30 s per bag (`time`/GMT, `P-Trak n/cm3`, `DustTrak mg/m3`) | 2006 ARD bags 1–3; digest notes a garbled GMT and a one-row bag-3 offset between the two files |

**Usable for features?** The 1 Hz series are clean, but the join is **not 1:1**. tests has 2 `condition_set` rows that describe hardware (D1 = P-Trak, D2 = DustTrak), not runs. D2 maps to 3 TestIDs × 2 instruments. TestIDs 5–7 (2006, the only ARD runs) have no row.

---

### SAME / SPICE / DAFT: contradictions with tests.parquet or digest

- **PSI-101 run 112** has an analysed workbook (`2010_253_14_kapton_run112.xls`) and a Results.xlsx row ("low flow run w STS"), but no tests row. The digest mentions it as an "unlisted 2 cm/s Kapton run".
- **PSI-101 test_id `57` is duplicated** in tests (one row `lampwick`, one `teflon`). The workbook `2010_210_10_lampwick_run57.xls` (TestNumber 57) is lampwick, so the teflon row is not a test that was run. Both points are recorded as patches D29 and D30 (`discrepancies()`); the teflon row is kept and flagged `conflicts_with_raw`.
- **PSI-101 test `51`** (Kapton) has no workbook or HKP file, while every other base run 48–114 has one.
- **PSI-102**: tests has 8 *planned* rows; the data hold flown runs 1–47 (Results.xlsx Flight==1 lists `SAME #` 5–47 and 16 `a` variants). Early file-name run numbers ≠ onboard `TestNumber` (run 4 → TN 2, run 5 → TN 2/3). `kaptonGMT257*.xls` contains GMT 254 data.
- **PSI-47**: D1 date 2005-02-23 vs instrument/workbook date 22 Feb 2005 (GMT 053). Both rows say Arizona road dust, but the logged 2005 runs sampled cabin air and Velcro (digest agrees). The ARD runs (2006, TestIDs 5–7) are absent from tests.
- **PSI-107**: `Spice_Flight_Flamelength.xls` TP numbering (1–11) cannot be matched to `review_tp` labels.

### SAME / SPICE / DAFT: not decoded

- `RunMode`, `EventCode`, `*State`/`*KeySelect` code meanings (HKP).
- The `DustTrakAMeasurement` integer encoding in SAME-R (probably MPASS).
- The two numeric code columns in the PSI-102 command logs.
- The "Log Interval 00:01:00" notation in the DAFT `Headers` sheet; 1 s is confirmed from the time columns instead.
- The not-downloaded zips, videos and `.xml` placeholders.

## `timeseries_features` table

`data/processed/timeseries_features.{parquet,csv}` has one row per raw per-test time-series file that joins to a
`tests` row, plus one row per CFI test with reduced data (1,075 rows, 147 columns). It is built by `fif/pipeline/build_timeseries.py`
(`uv run python -m fif.pipeline.build_timeseries`, about 45 s).

| accession | rows | tests covered | source |
|---|---|---|---|
| PSI-10 | 308 | 308 | ACME `_data.csv` |
| PSI-23 | 288 | 18 test days (several files per day) | ACME `_data.csv` |
| PSI-159 | 328 | 328 | ACME `_data.csv` |
| PSI-39 | 123 | 123 | CFI `_Radiometer_Readings.txt` + `_Chamber_Readings.txt` |
| PSI-98, PSI-100 | 2 + 2 | 4 | Saffire `Sample <n> Sensor*.xlsx`, sheet `Calibrated Data` |

**Families not added, and why.**

- SAME-R (PSI-101) housekeeping does join on the in-file `TestNumber`, but it is not 1:1: aged and unaged runs
  share one timeline with no boundary, and several workbooks hold neighbouring runs.
- SAME (PSI-102) data cover flown runs 1–47, but `tests` holds only the 8 planned rows.
- SPICE (PSI-107) and DAFT (PSI-47) have no per-test time series.
- Saffire-II (PSI-99) has no sensor files.

**`load_timeseries(test_id, test_point=None, accession=None)`** returns a tidy DataFrame with these columns:

- `test_point`;
- `time_s`, in seconds from the first sample;
- one column per channel, with its unit in the name (`burner_temp_c`, `chamber_pressure_kpa`,
  `radiometer_center_w_cm2`, `narrow_band_radiometer_v`, `o2_pct`, …).

It accepts a `tests.test_id` (with or without spaces) or a test-point or CIR code. PSI-23 test days and
re-opened points return all their files stacked; pass `test_point` to pick one. It was checked for all 776
`test_id`s in the table, and its row counts equal `n_samples`. Saffire workbooks take about 10–30 s each to
load.

ACME files are 125 Hz. CFI radiometers are 100 Hz, with the 1 Hz chamber readings attached to each sample (the
latest earlier reading). Saffire is about 30 Hz.

### Columns

Times are in seconds from the file's first sample. "Burn" is the window [`ignition_time_s`, `flameout_time_s`].
"Final" is the median of the last 1 s. "Start" is the median of the first 2 s, or the first 50 s for Saffire.
"Peak" is taken after a 0.2 s running median. Temperature maxima are the raw maxima.

| column(s) | meaning | families |
|---|---|---|
| `accession`, `test_id`, `test_point`, `source_file` | keys. `test_point` is the code in the file name (`21228A1`, `21196M2_1`, `F068A03`, `S1`) | all |
| `n_samples`, `duration_s`, `sample_hz`, `first_sample_utc` | size and time base. `first_sample_utc` combines the header date with the first row's clock (GMT) | all |
| `experiment_code`, `burner_code`, `oxidizer_gas`, `inert_gas`, `fuel_gas`, `thermocouple_rake`, `pmt1_gain_v`…`pmt3_gain_v` | header metadata. Gas names come from Rev D Table 34; undocumented codes are written `code N` | ACME |
| `radiometer_array` | `standard`, `cfi-g`, `cfi-droplet` or `saffire` | all |
| `radiometer_on_s` | time the flame signal stays above threshold (rule below), including igniter glow | ACME |
| `flame_detected` | `radiometer_on_s ≥ 2 s` | ACME |
| `ignition_time_s`, `flameout_time_s`, `burn_duration_s` | first and last on-sample of the flame signal, and their difference. `burn_duration_s` is 0 and the times are NaN when no flame is detected | ACME |
| `flame_threshold` | threshold used, in W/cm² (standard array) or V (CFI-G low gain) | ACME |
| `script_ignition_s`, `script_extinction_detected_s`, `script_mfcs_off_s` | events from `<tp>_TP.txt` (1 s resolution), relative to the first sample. For CFI and Saffire, `script_ignition_s` is the first igniter-on sample (CFI `IGNITER_POWER_STATUS`; Saffire igniter current > 50% of its maximum) | ACME, CFI, Saffire |
| `chamber_pressure_start_kpa`, `_end_kpa`, `_max_kpa`, `_mean_burn_kpa` | chamber pressure: ACME `PTA3`, CFI `FCU_MP_PT16` (the transducer that matches `tests.pressure_kpa`; which one it is was inferred), Saffire `Ambient Pressure` (Cygnus cabin) | all |
| `cold_junction_temp_mean_c` | thermocouple cold junction | ACME |
| `burner_temp_start_c`, `_max_c`, `_time_of_max_s`, `_final_c` | burner thermocouple | ACME |
| `ambient_200mm_{a,b}_temp_max_c`, `_final_c`; `rake_{a,b,c,d}_temp_max_c` | thermocouples 200 mm off-axis and on the rake (rake columns are NaN when the rake was removed; B and C are NaN below about 250 °C) | ACME |
| `{oxidizer,inert,fuel}_flow_max_slpm`, `_max_burn_slpm`, `_mean_burn_slpm` | MFC readings. `_max_slpm` is the whole-file maximum: in about a quarter of the files it is a 9.99 V controller spike of under 0.5 s before ignition, above the controller's full scale, so it is not the test's flow. `_max_burn_slpm` and `_mean_burn_slpm` cover the detected burn only | ACME |
| `pmt{1,2,3}_…_mean_burn_v`, `_max_burn_v` | PMT voltage during the burn (≥ 4.4 V = rail or saturation) | ACME |
| `radiometer_{p60,p30,center,m30,m60,offset}_{peak,final,mean_burn}_w_cm2`, `_time_of_peak_s`, `_clipped` | standard array (and the offset radiometer on CFI-G runs), W/cm². `_clipped` is true when the peak is within 1% of the channel's ceiling (see Radiometer saturation) | ACME |
| `radiometer3_{p60,p30,m10}_{lo,hi}_{peak,final,mean_burn}_v`, `_time_of_peak_s` | CFI-G array, uncalibrated V (not baseline-subtracted) | ACME |
| `narrow_band_radiometer_{peak,final,baseline}_v`, `wide_band_…`, `_time_of_peak_s` | CFI radiometers, raw V (baseline about −9.7 V, rail ±10 V → NaN) | CFI |
| `chamber_gas_temp_start_c`, `chamber_gas_temp_max_c` | mean / max of the chamber `TM1`–`TM4` | CFI |
| `o2_start_pct`, `o2_min_pct`, `co2_start_pct`, `co2_max_pct`, `anemometer_start_cm_s`, `plume_temp_max_c`, `sample_temp_max_c`, `radiometer_{1..4}_rise_peak_mw_cm2`, `radiometer_{1..4}_time_of_peak_s` | Saffire sensors. Radiometer rise = signal − median of the first 50 s | Saffire |
| `features_note` | problems found while parsing (dropped rows, missing `_TP.txt` (looked up by file name, then by the test point written inside the timeline files), time gap, re-opened point, id alias, timeline not overlapping), or why a feature is not derived | all |

### Burn-detection rule (ACME)

1. **Channels.** The standard array uses its five on-axis radiometers in W/cm². The CFI-G array uses its three
   low-gain channels in V. High-gain channels saturate, and the offset radiometer sees the whole chamber, so
   neither is used.
2. **Flame signal.** Smooth each channel with a 0.2 s running median and subtract its pre-ignition baseline (the
   median of the first 2 s). The flame signal is the maximum over the channels at each instant.
3. **Floor.** The floor is 1×10⁻⁴ W/cm² for the standard array and 0.05 V for CFI-G. This is about 1% of full
   scale and about 200× the baseline noise.
4. **Threshold.** Take the 90th percentile of the flame signal over the samples above the floor, and multiply
   it by 0.4. The threshold is that value or the floor, whichever is larger. Using the 90th percentile rather
   than the peak keeps a short ignition spike from hiding a weaker steady flame.
5. **Burn window.** Ignition is the first sample above the threshold and flame-out is the last.
6. **Flame or not.** `flame_detected` requires at least 2 s on. Igniter glow alone gives 0.5–2 s.

The fraction (0.4), the percentile and the floor were **chosen by comparison with PSI-159 `burn_time_s`**. The
PSI-159 agreement below is therefore in-sample. The agreement with the `_TP.txt` script events (all three
accessions) and the temperature and pressure checks are independent.

For CFI (PSI-39) a similar rule gave on-times uncorrelated with the hot-flame `burn_time_s` (r ≈ 0). The
water-band radiometer keeps seeing the hot product cloud for tens of seconds. No burn duration is derived for
CFI or Saffire; the `features_note` says so.

### Agreement with the `tests` table

| comparison | n | median diff | median \|diff\| | p95 \|diff\| | within tol | r |
|---|---|---|---|---|---|---|
| PSI-159 `burner_temp_max_c` − `peak_temp_c` (°C) | 282 | −0.02 | 0.04 | 1.31 | 85% (±0.5) | 1.0000 |
| PSI-159 `burn_duration_s` − `burn_time_s`, ignited and detected (s) | 241 | +0.25 | 0.55 | 1.88 | 95% (±2) | 0.989 |
| … self-extinguished | 153 | +0.06 | 0.43 | 1.37 | 98% (±2) | 0.986 |
| … flow-terminated | 88 | +0.61 | 0.69 | 6.52 | 91% (±2) | 0.993 |
| PSI-10 `chamber_pressure_start_kpa` − `pressure_kpa` (kPa) | 308 | +2.70 | 2.70 | 3.56 | 100% (±5) | 1.0000 |
| PSI-10 `chamber_pressure_end_kpa` − `pfinal (atm)` × 101.325 | 290 | +2.84 | 2.84 | 4.33 | 99% (±5) | 1.0000 |
| PSI-10 `chamber_pressure_mean_burn_kpa` − `pmean (atm)` × 101.325 | 290 | +3.32 | 3.32 | 4.91 | 96% (±5) | 0.9999 |
| PSI-159 `chamber_pressure_start_kpa` − `pressure_kpa` (kPa) | 328 | +2.42 | 3.32 | 23.11 | 64% (±5) | 0.997 |
| … normal flames, ratio − 1 | 175 | +2.9% | 2.9% | 6.4% | 56% (±3%) | |
| … inverse flames, ratio − 1 | 153 | −5.7% | 5.8% | 7.3% | 13% (±3%) | |
| PSI-39 `chamber_pressure_start_kpa` − `pressure_kpa` (kPa) | 123 | +2.44 | 2.50 | 3.63 | 98% (±5) | 0.9999 |

PSI-159 ignition outcome against `flame_detected`:

| `ignited` | flame not detected | flame detected |
|---|---|---|
| False | 57 | 1 (21106 F4) |
| True | 21 | 241 |

All 21 ignited tests with no detected flame have `burn_time_s` ≤ 5 s; 13 of them are 1 s. Of the 8 `flash_only`
tests (`ignited` null), 7 are not detected.

Against the `_TP.txt` script events (independent of the tuning):

- **Ignition.** The radiometer ignition comes 1.1–2.5 s (median) after the script's "Ignition and retraction"
  stamp: PSI-23 +1.14 s (86% within ±2 s), PSI-10 +1.91 s, PSI-159 +2.50 s.
- **Flame-out.** For PSI-10 and PSI-23, flame-out falls 0.4–0.9 s before the script's "Extinction detected"
  (65% / 84% within ±2 s).
- **CFI-G exception.** For PSI-159 the script flags extinction a median 11 s after the radiometers drop. Its
  averaged extinction detector evidently lags the hot-flame radiation (or follows the cool flame).

**Reading the pressure offsets.**

- The ACME transducer conversion in Rev D reads 2–3 kPa above the tabulated pressures in every accession:
  PSI-10, PSI-39 and PSI-159 normal flames. The tables probably carry a calibrated or zero-corrected value.
  Treat the raw conversion as having an offset of about +2.7 kPa.
- The PSI-159 **inverse-flame** table pressures are 5.7% *above* the measured chamber pressure, while the
  measurement sits 1–2% above the nominal 2 and 3 atm fills. This confirms the
  `pressure_9pct_above_nominal` flag: the table values are wrong and the raw data are not.

### Raw data that contradict the `tests` table or digest records

- **PSI-10 22042M1** (flagged `id_suspect`). The raw files are named `22024M1`, and the header says `Test Point:
  22024M1`, dated 2022-01-25. The table id is a digit swap; `tests` now uses `22024M1` (patch D01 in `data/corrections/tests_patches.json`).
- **PSI-159 21106 F4.** `ignited` is False, but the radiometers show a 20.4 s flame. `burn_time_s` is 22 and the
  comment says "hot flame". `ignited` should be True.
- **PSI-159 21112 A6.** `burn_time_s` is 259 s, but the radiometer flame lasts 147 s and the script's "MFCs off"
  is at 180 s after the first sample. 259 s is not possible within the recording.
- **PSI-159 21270 H3.** `burn_time_s` is 43 s (the same as H2), but the flame lasts 94 s, ending when the MFCs
  are turned off. 21270 H2 measures 57 s. Other flow-terminated 21270 and 21277 tests run 6–17 s longer than the
  table (21270 A1/A2/A4, 21277 M1).
- **PSI-159 inverse flames.** The table pressure is about 7% too high (see above; already flagged).
- **PSI-23 20190.** The table says "35% H2 with He". The raw header fuel code is 14 = H2/He 45/55, which supports
  the reports' 45% (the row is flagged `conflicts_with_report`).
- **PSI-23 20132 / 20136 / 20142.** All three days carry the same bottle code 12 (H2/CH4/He 25/20/55), while the
  table lists 25/20, 20/25 and 30/15. Either the code was not updated or the table is wrong; unresolved.
- **PSI-39 1336–1338 (F200D03–D05).** The chamber reads about 309.5 kPa against the table's 303.975 (3 atm
  nominal). That is 5.5 kPa, beyond the usual +2.4 kPa offset.
- **PSI-39 1301 (F180D02)** is dated 2017-07-29 in the table, but the code and files say 2017-06-29 (GMT day 180).
  **1237 (F121A02)** is dated 05-02, but the files say 05-01.
- **Saffire-I (PSI-98).** The O2 sensor reads 22.6% (S1) and 22.3% (S2), against 0.215–0.217 in the table.
  Saffire-III reads 19.8% O2, while the table has none. Cabin pressure (102.3 and 99.4 kPa) is missing from the
  table. The anemometers agree with `flow_cm_s` (20.0 and 25.0 cm/s).

### Not decoded

- **CFI-G radiometers.** The dual-gain array has no V→W/cm² calibration in PSI (CIR-RPT-4600 is cited but not
  archived), so it stays in V.
- **PMT irradiance.** Rev D gives polynomials only for gains 2–8 V. PMT columns stay in V.
- **Undocumented codes.** Experiment code 5 is not in Rev D. Fuel codes 19–25 are mapped to a base fuel only by
  joining to `tests.fuel`; their compositions are unknown.
- **CFI calibrations.** The CFI radiometers have no V→W calibration. The reduced `FLEX-<id>_RadiometerData`
  wide-band power reads about −5.4×10⁶ W, which is not physical.
