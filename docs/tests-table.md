# `tests` table

`data/processed/tests.{parquet,csv}` has one row per test, per test day or per condition set across 19 PSI
combustion investigations (2,177 rows). It is built by `fif/pipeline/build_tests.py`
(`uv run python -m fif.pipeline.build_tests`).

Most rows come from the PSI "Experimental table" CSVs, with one adapter per file. Three richer sources replace
or enrich their table:

- **PSI-26 BASS**: the as-run test matrix (xlsx).
- **PSI-39 CFI**: the data-summary spreadsheet (xlsx).
- **PSI-107 SPICE**: the master run log (xls).

The build then applies the corrections documented in the digest records (`data/digest/PSI-*.json`, in their
`gaps`, `limitations`, `test_matrix`, `psi_data` and `findings` sections).

Rules:

- **No silent changes.** When a value is corrected, the source value stays in `extra` under
  `<column>_original` (or `<source column>_original` for a value that only lives in `extra`). The row also gets
  a code in `flags`.
- **Doubts are flagged even when no value changes.**
- Source cells that no column captures stay in `extra` verbatim. Approximate values (`~ 21.5`) are parsed but
  also stay in `extra`.

With pandas, read the flags column as `df["flags"]`. `df.flags` is a pandas attribute, not the column.

## Columns

Investigation numbers are PSI accession numbers (10 = PSI-10).

| column | meaning | unit | populated for |
|---|---|---|---|
| `accession` | PSI accession | - | all |
| `acronym` | investigation acronym (from `investigations.csv`) | - | all |
| `test_id` | test identifier from the source (test no., FLEX no., day code). When the source has none: `<accession>-r<source_row>` | - | all |
| `row_kind` | `test` (one test or burn), `test_day` (one row per day), `condition_set` (one test condition, possibly several runs), `planned` (pre-flight planning matrix, not flown) | - | all |
| `date` | test date (ISO). Null when the source date is missing, garbled or inconsistent | - | 10, 20, 21, 22, 23, 25, 26, 39, 47, 69, 106, 107, 159 |
| `fuel` | normalised fuel name(s), joined with `/`. For BASS / BASS-II rows whose label names only a shape it is inferred (`fuel_inferred`) | - | all except 8 unlabelled rows |
| `fuel_raw` | fuel or material text as in the source (or as corrected, see `fuel_raw_original`) | - | all |
| `fuel_phase` | `gas`, `liquid`, `solid` or `aerosol` | - | all |
| `fuel_fraction` | fuel mole fraction of the fuel stream. For inverse flames (PSI-10, PSI-159 `config = inverse`) it is the ambient (chamber) fuel fraction | mole fraction | 10, 20, 21, 22, 23, 106, 107, 159 |
| `config` | flame or sample configuration (normal / inverse, coflow, droplet, free / fiber-supported droplet, opposed / concurrent flow). For the 20 BASS-II slab tests (M series) it is `opposed flow`, from the summary report | - | 10, 21, 22, 25, 26, 39, 68, 69, 98, 99, 100, 107, 159 |
| `geometry` | burner, nozzle, sample or droplet size as text | as stated | 20, 25, 26, 68, 69, 98, 99, 100, 107 |
| `x_o2_ambient` | O2 mole fraction of the surrounding chamber or cabin atmosphere (single value). Null for inverse flames, whose ambient is fuel + N2 | mole fraction | 10, 20, 23, 25, 26, 39, 69, 98, 99, 159 |
| `x_o2_burner` | O2 mole fraction of a burner oxidiser stream (inverse flames) | mole fraction | 10, 159 |
| `x_o2_min`, `x_o2_max` | range of ambient O2 over the row (a day or condition set may list several values). Ambient only: null for inverse flames | mole fraction | 10, 20, 23, 25, 26, 39, 68, 69, 98, 99, 159 |
| `x_o2` | **deprecated, ambiguous; not in `data/export/tests.json`.** The single O2 value as first parsed: ambient for most rows but the burner stream for inverse flames. Kept for backward compatibility; use `x_o2_ambient` / `x_o2_burner` | mole fraction | 10, 20, 23, 25, 26, 39, 69, 98, 99, 159 |
| `diluent` | ambient inert: `n2`, `he`, `co2`, `mix`, or `n2 or he` | - | 20, 23, 39, 68, 69 |
| `pressure_kpa` | chamber or cabin pressure | kPa | 10, 26, 39, 69, 98, 100, 107, 159 |
| `flow_cm_s` | imposed air or oxidiser flow velocity (single value; null when the flow was ramped through several values) | cm/s | 25, 26, 98, 99, 100, 101, 102, 107 |
| `gravity` | always `micro` | - | all |
| `n_flames` | flames ignited on a test day | count | 20, 21, 22, 23 |
| `ignited` | hot ignition yes/no (null for CFI-G "flash"). For PSI-25 only `False`, on the one row (O12) whose air-display cell says "no ign"; for BASS and BASS-II use `outcome` | bool | 25, 159 |
| `burn_time_s` | burn time. For PSI-39 it is the hot-flame burn time. For PSI-25 (M series only) it is the summary report's burn time, given in minutes to 0.1 min | s | 25, 39, 69, 98, 99, 159 |
| `extinction_mode` | `self_extinguished`, `flow_terminated`, `extinction`, `disruption`, `completion` | - | 69, 159 |
| `outcome` | PSI-25 and PSI-26 only, whose tables have no outcome column: how the flame ended, read from the crew's own words. `no_ignition` (never lit, or not sustained once the igniter was withdrawn), `extinguished` (a sustained flame went out with fuel left), `burned_out` (burned until the fuel was gone). Null when the words do not say: 145 of the 250 runs. See "Outcomes read from notes" below | - | 25, 26 |
| `outcome_cause` | with `extinguished` only: `blowoff` (went out as flow was raised), `low_flow` (went out as flow was reduced or shut off), `nitrogen` (put out by the GN2 flow), `unspecified` | - | 25, 26 |
| `outcome_action` | with `extinguished` only: what was done to the flow when the flame went out. `flow_reduced` (the flow was turned down and the flame went out at a finite setting: a quenching limit), `flow_shut_off` (the crew stopped the fan or the air to end the run: not a limit), `flow_raised` (blowoff, every `blowoff` row), `nitrogen` (every `nitrogen` row), `none` (went out by itself at constant flow). Null when the words do not say (2 runs) | - | 25, 26 |
| `outcome_setting` | the setting at which the flame went out, when the source states it: `pot 0.31` (fan potentiometer), `fan 40` (fan display), `gn2 pot 6`. Text as logged, not a velocity: the fan calibration does not reach these settings and was not applied. `extra.outcome_setting_field` names the cell. 31 runs | as logged | 25, 26 |
| `outcome_quote` | the words the outcome was read from, verbatim; `extra.outcome_field` names the cell, `extra.outcome_doubt` gives a caveat where the reading is uncertain, `extra.outcome_cause_inferred` marks a cause that rests on the fan and air cells and not on the quoted words (3 runs) | - | 25, 26 |
| `t_ad_k` | computed adiabatic flame temperature | K | 10, 159 |
| `peak_temp_c` | peak burner temperature | °C | 159 |
| `d0_mm` | initial droplet diameter | mm | 39, 69 |
| `ext_diameter_mm` | droplet diameter at (hot / visible) flame extinction | mm | 39, 69 |
| `burn_rate_k_mm2_s` | burning-rate constant K (hot flame for PSI-39). PSI-69's "Burning rate; mm" column is K in mm²/s | mm²/s | 39, 69 |
| `n_reignitions` | hot-flame re-ignitions after radiative extinction | count | 39 |
| `cool_flame` | `True` when cool-flame data exist (k_cool, cool-flame extinction diameter or an extrapolated cool flame). Never `False`: missing cool-flame data do not show there was none | bool | 39 |
| `spread_rate_mm_s` | microgravity flame spread rate, one value for the whole test. Null for BASS-II: its rates belong to flow steps within a test and are in `extra.spread_steps` and the `spread_steps` table (see "BASS-II spread rates" below) | mm/s | 98, 99, 100 |
| `burn_length_cm` | microgravity burned length | cm | 98, 99, 100 |
| `flame_length_mm` | measured flame length: video length, or Nikon still flame height | mm | 107 |
| `at_smoke_point` | the log marks this flame as at its smoke point (`Smoke Height` / `SH ?` Y/N) | bool | 107 |
| `smoke_point_reviewed` | `True` when the row is one of the 55 smoke points of the science team's review (`SmokePointReview-0g-3.xlsx`), matched to this single log row (review values in extra, `review_*`). Never `False`: points between two log rows are flagged `smoke_point_bracket` instead | bool | 107 |
| `measurement` | `video` (downlink video measurement / timestamp) or `still` (Nikon still) | - | 107 |
| `flags` | semicolon-separated codes (below); null when none | - | 10, 23, 25, 26, 39, 69, 98, 99, 100, 102, 106, 107, 159 |
| `extra` | JSON object: uncaptured source cells, `<column>_original` values, notes and provenance | - | nearly all |
| `source_file` | file the row came from, relative to the repo | - | all |
| `source_row` | row number in that file: 1-based data row for CSVs, Excel row number for spreadsheets | - | all |

Common `extra` keys:

- `report_value`: what the report says, where it conflicts.
- `outcome_source`: the record finding behind a value.
- `report_source`, `spread_steps`, `report_width_cm`, `report_sides_burning`, `report_velocity_cm_s`,
  `spread_rate_note`: PSI-25 M series, from the summary report's Table 5.1 (see "BASS-II spread rates" below).
- `asrun_*`: PSI-26 as-run cells.
- `experimental_table_row`: PSI-39, the row in the old CSV.
- `verbatim_duplicate_dropped`: PSI-22.
- `review_*`: PSI-107 smoke-point review values (see PSI-107 below).
- `fuel_composition_on_orbit`: PSI-23.

## Flags

| code | meaning | rows |
|---|---|---|
| `o2_is_burner_stream` | inverse flame: the table's O2 is the burner stream (up to 0.85); stored in `x_o2_burner`, ambient O2 null | 274 (PSI-10 120, PSI-159 154) |
| `pressure_9pct_above_nominal` | CFI-G inverse table pressures are ~9% above the nominal 0.507-3.04 bar fill levels (kept as given). Not set on the six rows of day 21196 at 49.5 kPa, which are 2% below the 0.5 atm level | 148 (PSI-159) |
| `ramped` | a condition was ramped during the test, so no single value is given (PSI-10 RAMP/RAMPED cells; PSI-25 and PSI-26 air display lists several speeds) | 205 (PSI-10 69, PSI-25 79, PSI-26 57) |
| `burner_over_limit` | peak burner temperature above the stated 450 °C (723 K) termination limit | 30 (PSI-159) |
| `smoke_point_bracket` | PSI-107: a reviewed smoke point lies between this row and the neighbouring logged row of the same burn; `review_point` in extra names the point | 26 (PSI-107) |
| `placeholder_values` | propane day: nominal 0.40 O2, one initial pressure and repeated Zst/Tad for the whole day, no final values | 20 (PSI-10) |
| `needs_review` | value left null or doubtful: PSI-26 undiluted O2 reading right after a vitiated run with no value in the notes; PSI-107 air rate given although the AIR reading was lost (LOS) | 11 (PSI-26 4, PSI-107 7) |
| `flow_below_sensor_range` | air rate below the anemometer's 5 cm/s rated minimum (kept, unreliable) | 11 (PSI-107) |
| `composition_sum` | ambient mole fractions do not sum to 1 ± 0.01 | 10 (PSI-39 4, PSI-69 6) |
| `ext_gt_d0` | extinction diameter larger than initial diameter | 9 (PSI-39 8, PSI-69 1) |
| `ext_zero` | extinction diameter recorded as 0 | 8 (PSI-69) |
| `flash_only` | "flash" hot ignition: momentary flame of about 1 s | 8 (PSI-159) |
| `planned_not_flown` | row is the pre-flight planning matrix, not an as-flown test | 8 (PSI-102) |
| `unit_corrected` | thickness unit or decimal error fixed in `geometry` (original in `geometry_original`) | 7 (PSI-98 2, PSI-99 3, PSI-100 2) |
| `corrected_from_report` | value changed to the value in the reports or publications (original kept) | 6 (PSI-23 2, PSI-99 2, PSI-100 2) |
| `conflicts_with_report` | table disagrees with the reports; not changed (`report_value` in extra) | 7 (PSI-23 2, PSI-25 2, PSI-98 2, PSI-99 1) |
| `o2_final_artifact` | BASS-II "Calibrated final O2" is a spreadsheet artefact (sensor offset, or offset plus raw reading); removed from extra and kept as `..._original` | 5 (PSI-25) |
| `value_from_report` | value taken from a report, not from a PSI table: Saffire spread rate and burned length from a digest-record finding (`outcome_source` in extra); BASS-II M series `config`, `burn_time_s` and the spread rates in extra from the summary report's Table 5.1 (`report_source` in extra) | 24 (PSI-25 20, PSI-98 2, PSI-100 2) |
| `flow_missing_los` | air rate equals the conversion intercept (-5.918) because the AIR reading was lost; flow set to null | 3 (PSI-107) |
| `date_corrected` | date corrected (original in `date_original`) | 3 (PSI-25 2, PSI-39 1) |
| `o2_from_notes` | as-run O2 cell is the pre-dilution reading; the diluted value from the crew notes is used | 2 (PSI-26) |
| `duplicate_id` | the same test id appears on two rows of the investigation; `source_file` + `source_row` identify a row | 12 (PSI-26 8, PSI-69 2, PSI-101 2) |
| `fuel_inferred` | the sample label names only a shape (rod, film, sphere); `fuel` = pmma follows the investigators' documents (`fuel_source` in extra) | 85 (PSI-25 55, PSI-26 30) |
| `date_conflict` | the source date is unreadable or is not the day its GMT day-of-year column gives; `date` left null, source text in extra | 10 (PSI-25 1, PSI-26 9) |
| `autofill_artifact` | PSI-23: "N2" dragged down a spreadsheet column became "N3", "N4", ...; read as N2 | 7 (PSI-23) |
| `low_o2_in_source` | PSI-10: the table gives the text "LOW O2" instead of the burner O2, flows, Zst and Tad; left null | 2 (PSI-10) |
| `id_suspect` | test id looks mistyped | 1 (PSI-10) |
| `pressure_zero_in_source` | source gives 0 mmHg; pressure left null | 1 (PSI-69) |
| `label_fixed` | a label split across cells was repaired (original in extra) | 1 (PSI-106) |
| `corrected_from_raw` | value replaced by the raw sensor data (table value kept as `<column>_original`; patch ids in extra `discrepancies`) | 9 (PSI-10 3, PSI-23 1, PSI-39 2, PSI-159 3) |
| `filled_from_raw` | empty table cell filled from the raw sensor data | 5 (PSI-10 1, PSI-98 2, PSI-100 2) |
| `conflicts_with_raw` | raw data disagree with the table, or with the value this dataset gives; the value is kept (patch ids in extra `discrepancies`) | 28 (PSI-10 2, PSI-23 4, PSI-39 3, PSI-98 2, PSI-100 2, PSI-101 1, PSI-159 14) |
| `conflicts_with_test_sheet` | the operators' hand-filled test sheet contradicts the value or says the row was not what the table makes of it; the value is kept. The sheet is an AI reading of a scan, not checked by a human (patch ids in extra `discrepancies`) | 6 (PSI-10 1, PSI-159 5) |
| `conflicts_with_table` | PSI-39 only: the spreadsheet and the old experimental table disagree (old value as `experimental_table_<column>`) | 0 |

682 rows carry at least one flag.

**Row key.** `test_id` is not unique: 12 rows in PSI-26, PSI-69 and PSI-101 share an id with another row (flag
`duplicate_id`). `source_file` + `source_row` is unique and is the key of a row.

## Per investigation

**PSI-10 ACME Flame Design** (327 tests). The rows come from two tables:

- Normal flames: fuel flows into an O2/N2 atmosphere. `x_o2_ambient` is the chamber O2.
- Inverse flames: O2/N2 flows from the burner into C2H4/N2. `x_o2_burner` is the burner O2, `fuel_fraction`
  is the ambient C2H4, and the ambient has no O2.

Corrections and flags:

- Inverse rows are flagged `o2_is_burner_stream`.
- RAMP/RAMPED rows are flagged `ramped`.
- The 20 propane-day rows (21301*) are flagged `placeholder_values`.
- Propane fraction of day 21301 (patches D51 to D55, note D62). The A1 sheet says the fuel line still held 30%
  propane when the 100% bottle was connected. The recordings settle how far that reaches: per unit of
  fuel-controller flow, 21301A1 and A2 radiate 0.42 times as much as 21301A7 at the same setpoint and show a
  gas-line pressure drop 3.5 to 4 times larger, like the 30% propane day 21137 of PSI-159 and unlike its 100%
  propane day 21112 (same burner, 40% O2).

  | Rows | `fuel_fraction` | Flag | Why |
  |---|---|---|---|
  | 21301A1, A2 | 0.30 (table 1.0 in `fuel_fraction_original`) | `corrected_from_raw` | both sensors match the 30% day; 0.30 is the mixture the line held, not a measured composition |
  | 21301A3 | 1.0 kept | `conflicts_with_raw` | the fraction rose from about 0.3 towards 1.0 during the burn |
  | 21301A4 | 1.0 kept | `conflicts_with_raw` | 10 to 20% less radiation than pure propane: not decisive |
  | 21301A5 | 1.0 kept | `conflicts_with_test_sheet` | the sheet repeats the doubt; the recording is within 5% of pure propane |
  | 21301A6 to A9, H1 to H3 | 1.0 | none | indistinguishable from pure propane (about 5% spread); the diluted rows C, D, J3, J4 ran after A6 |

  `mfuel (mg/s)` and `mN2 (mg/s)` in extra are NASA's values for pure propane on all rows. The sheets of 21301H2 and
  H3 have their fuel flows swapped; the table, the as-run files and the recorded flows agree (0.082 and 0.092 slpm).
- Nine recorded Flame Design test points have no row (notes D27, D63): all are ignition attempts without a lasting
  flame (eight flashes or failed ignitions, one igniter burn-out). No rows were added.
- The tables have no column for how a flame ended. The test sheets say 17 flames were stopped by the burner
  temperature limit (note D59), and they are the only record of 21 attempts with no row and no data file (note
  D60). See "Test sheets" below.
- `22042M1` is flagged `id_suspect`: its day group is 22024. The raw files confirm the digit swap, so the row is now
  `22024M1`, dated 2022-01-24 (patches D01, D02; the table id is kept in extra as `test_id_original`).

**PSI-20 BRE, PSI-21 CLD Flame, PSI-22 E-FIELD, PSI-23 s-Flame** (test days).

- PSI-21: no change beyond the existing fuel-typo normalisation.
- PSI-22: the verbatim duplicate of day 18319 (and its continuation rows) was dropped, so the table has 20 days.
  The kept row lists the dropped source row in its extra.
- PSI-23: on days 20006 and 20013 the H2/CH4 bottles were diluted 55% with N2 on orbit
  (20/25/55 and 30/15/55% H2/CH4/N2). `fuel_fraction` changed from 1.0 to 0.45 (`corrected_from_report`).
  The raw data headers of these days name the undiluted bottle, as the table does, so the rows also carry
  `conflicts_with_raw` (patches D35, D36): the reports and the recordings disagree and both values are kept.
- PSI-23: cells reading "with N3", "with N4", ... are a spreadsheet autofill of "with N2" (`autofill_artifact`).
- PSI-23: day 20190 says "35% H2 with He" against 45% in the reports, and the 20132 test-type label is wrong
  (it was the first helium day). Both are flagged `conflicts_with_report` and not changed.

**PSI-25 BASS-II** (129 tests).

- `fuel`: 55 rows are labelled only by shape ("1/4" clear rod", "100 micron film 2 cm wide"). The investigators'
  documents say the rods are cast PMMA (clear and black) and the films PMMA, so `fuel` = pmma with the flag
  `fuel_inferred`. The two "4 cm spherical section" rows stay without a fuel name.
- `flow_cm_s` is the air display when it holds one value (25 rows); when it lists several the row is flagged
  `ramped`. The display shows whole cm/s; the fan calibration was not applied.
- On runs that went out, `flow_cm_s` is not the flow at extinction: the cell that says "ext" or "blowoff" lists
  several values, so `flow_cm_s` is null on all 23. The setting at extinction, when stated, is `outcome_setting`.
- O10: the source date (7/22/2014) is not the day its GMT column gives, so `date` is null (`date_conflict`).

- The final-O2 artefacts for B2, P22a, P22b, T28a and T28b were removed from extra (kept as
  `Calibrated final O2 % by vol_original`) and flagged `o2_final_artifact`.
- F3, named in the record, has "none" in the CSV, so there was nothing to blank.
- T9 and T18 were dated 2018-06-24. They are GMT 175 of 2014, so the date is now 2014-06-24
  (`date_corrected`).
- The 20 thick-PMMA slab tests (M1 to M20) carry values from the BASS-II Summary Report (`value_from_report`):
  `config`, `burn_time_s` and, in extra, the spread rate at each flow step. See "BASS-II spread rates" below.

**PSI-26 BASS** (121 tests). Each experimental-table row was joined to the as-run matrix (sheets 2012 and 2013)
by (as-run no., test no.). All 121 rows matched exactly one as-run row. From the as-run row:

- `x_o2_ambient` and `x_o2*` are the cabin O2.
- `pressure_kpa` is the atm value × 101.325.
- `flow_cm_s` is the air display when it holds one value. When it lists several, the row is flagged `ramped`.
  It is the log's single "Air display" value, usually the flow at ignition, and not the flow at extinction: 13 of
  the 51 extinguished runs carry one (10 cm/s on runs 111 and 112, ended by shutting the air off; 5 cm/s on run
  103, which went out at pot 0.32). Use `outcome_action` and `outcome_setting` for how and where the flame went out.
- `fuel`: the 30 rows labelled only "sphere" are PMMA spheres according to the science requirements and the
  results overview (`fuel_inferred`). Candle and wax-slab rows stay without a fuel name.
- Nine rows have a source date that is unreadable or disagrees with the GMT day column; `date` is null and the
  row is flagged `date_conflict`.
- Four test numbers (114, 118, 75, 53) were used twice, in 2012 and 2013 (`duplicate_id`).
- Fan, air, GN2 (N2 dilution) settings, igniter and crew notes go to `asrun_*` keys in extra.

In 2013 the O2 cell sometimes holds the reading taken before GN2 vitiation:

- Where the notes give a different value, the note value is used (`o2_from_notes`): runs 86 (17.3%) and 87
  (16.8%).
- Some undiluted readings directly follow a vitiated run and have no note value (runs 88, 92, 96, 97). Their O2
  is left null and flagged `needs_review`.

`Planned_Test Matrix.xlsx` is never read; it contains credentials.

**PSI-39 CFI** (227 tests, previously 87). The rows are rebuilt from `CFI_DataSummary_Spreadsheet_Jan2021.xlsx`.
The conditions come from the Master Sheet. The DATA sheet supplies:

- `d0_mm`; `ext_diameter_mm` (hot flame); `burn_rate_k_mm2_s` (k_hot); `n_reignitions`;
  `burn_time_s` (hot-flame burn time); `cool_flame`.
- k_cool, the cool-flame extinction diameter and radiances, which go to extra.

Crew comments also go to extra.

The 79 unique tests of the old CSV all match the spreadsheet with no field differences. Their old row number is
in `experimental_table_row`. The CSV's 8 verbatim duplicate rows were dropped. Other flags:

- FLEX-1411 is dated 2011-09-06 in the spreadsheet. Its CIR test point code (f249b10, day 249) and its neighbours
  FLEX-1409 and 1410 (2017-09-06) give 2017-09-06, which is used (`date_corrected`, original in `date_original`).
- FLEX-1219 to 1222 are flagged `composition_sum` (O2 + N2 = 0.97).
- Eight tests are flagged `ext_gt_d0`, mostly blends where the extinction diameter is about the same as D0.

**PSI-47 DAFT, PSI-68 FLEX-2** (condition sets). Unchanged.

**PSI-69 FLEX** (274 tests).

- `d0_mm`, `ext_diameter_mm` and `burn_rate_k_mm2_s` are filled from the table.
- The file is read as cp1252, so the en dash used for "missing" is no longer a replacement character.
- Flags: C11M201 `pressure_zero_in_source`, both 193F001 rows `duplicate_id`, 6 rows `composition_sum`,
  C13H102 `ext_gt_d0` and 8 rows `ext_zero`.

**PSI-98 / 99 / 100 SAFFIRE-I / II / III** (2 / 9 / 2 burns). Changed values:

- Thickness errors fixed in `geometry` (`unit_corrected`): 0.37 "cm" becomes 0.37 mm, "037 mm" becomes 0.37 mm
  and ".33 cm" becomes 0.33 mm.
- Saffire-III flow changed from 30 to 25 cm/s.
- Saffire-II sample 2-6: flow changed from 20 to 25 cm/s, and the blank material filled as Cotton-Fiberglass
  (SIBAL).
- Saffire-II sample 2-9: the blank material filled as flat 1 cm PMMA.

These value changes are flagged `corrected_from_report`.

Spread rate and burned length:

- Saffire-II: from the table where the cell is numeric. "~ 0" is parsed as 0; note-only cells stay null.
- Saffire-I and Saffire-III: from the PSI-98 and PSI-100 record findings (`value_from_report`, cited in
  `outcome_source`).

Pressure of Saffire-I (patches D19, D20, D37, D38): the table has none. `pressure_kpa` is filled with the Saffire
ambient-pressure sensor before ignition (median of the first 50 s; the igniter comes on at 60 s): 102.3 and
102.6 kPa. The Cygnus cabin sensor reads 99.9 and 100.1 kPa over the same 50 s, about 2.5 kPa less. Neither
sensor's accuracy is documented, so the filled value is kept and the rows carry `conflicts_with_raw`.

Flagged `conflicts_with_report` without a change:

- Saffire-I: the table swaps the length and width.
- Saffire-II 2-1: the table gives O2 21.5% against the published 22.1%.

**PSI-101 SAME-R** (109 rows). The test list has run 57 twice, as Lampwick and as Teflon with identical cells.
The raw data hold only a lampwick run 57, so the Teflon row is not a test that was run: it is kept, flagged
`conflicts_with_raw` and `duplicate_id` (patch D30). Run 112 (Kapton, 2 cm/s) was flown but has no row (patch D29).
Exclude the false row with `exclude_flags=["conflicts_with_raw"]` when counting SAME-R tests.

**PSI-102 SAME** (8 rows). These rows are the pre-flight EIRD planning matrix (the flight ran 47 points at
2-8 cm/s). `row_kind` is `planned` (original in extra) and the rows are flagged `planned_not_flown`.

**PSI-106 SLICE** (12 test days). On the last day, the propane half of the fuel label was in the date cell.
`fuel_raw` is now "100% C3H8 and then 100% C2H4" (`label_fixed`). That day mixed SPICE and SLICE testing.

**PSI-107 SPICE** (526 rows, previously 469). The rows are rebuilt from the master run log
`Spice Flight Test Data II modified.xls`. It includes the GMT 062 methane session, which the CSV omits.

- Each row is one logged condition: usually a video row and a Nikon still row per condition, tagged in
  `measurement`.
- New columns: `flame_length_mm` (video length or Nikon height, in mm), `at_smoke_point` and
  `smoke_point_reviewed` (below).
- `pressure_kpa` is the logged nominal 101.325 kPa.
- Dates are GMT day-of-year in 2009.
- `test_id` is `PSI-107-r<Excel row>`, because the log's own "No." column is sparse and not unique (it is kept
  in extra).

Air rates:

- The three -5.918 values with a blank AIR cell have their flow set to null (`flow_missing_los`).
- Rates below 5 cm/s (-0.28, 0.66, 2.5-4.4) are kept and flagged `flow_below_sensor_range`.
- Seven LOS rows give an air rate of 15 cm/s although the AIR reading is missing. They are flagged
  `needs_review`.

Smoke-point review. `SmokePointReview-0g-3.xlsx` lists the 55 smoke points of the published set (AIAA 2010
presentation "Laminar Smoke Points in Coflow Measured Aboard ISS": 6 ethylene, 6 propane, 23 propylene, 13 75 %
and 7 50 % propylene; the sheet itself has 22 propylene and 14 75 % propylene points). The team read each point
from one video frame, at the flame tip's maximum grayscale gradient: its own GMT data time, fuel and air display,
radiometer (Rad) and x264 pixel length. Most of these frames are not log rows. Matching (`review_match`):

1. Burn: same GMT day, fuel and fuel fraction, nozzle, and ignition time within 3 s (60 s when the log gives the
   ignition as hhmm only; the flame-off time when the review's ignition was lost to Ku LOS). All points but E16-1
   find their burn. Where the review gives a test number (`No.`), it agrees with the burn's log No. (up to an
   a/b suffix).
2. Unique: one row of the burn agrees on fuel and air display within 1 count (the most that a video row and a
   Nikon still row logged in the same second differ), GMT data within 15 s, Rad within 0.25 and flame length
   within 3 mm where both rows have them. When the video row and the still of the same moment both agree, the
   video row wins because only it carries Rad (P16-3 and P4-2: stills r224 and r256 are not tagged).
3. Bracket: otherwise, the review time lies strictly between two consecutive logged rows of the burn, and its fuel
   display, air display and Rad lie within their range (plus the tolerances above).
4. Otherwise no match. No point is ambiguous: no point had two rows pass step 2 after the Rad tie-break.

Result: 15 unique (`smoke_point_reviewed` = True), 13 brackets (26 rows flagged `smoke_point_bracket`, never
`smoke_point_reviewed`), 27 no match, 0 ambiguous. Tagged rows get the review's values in extra:
`review_point` (1-55, sheet order and the No. of sheet (2)), `review_tp` (the TP # label, not unique: P16-1..3
and P7-1..3 are used for both propane and propylene), `review_source_row`, `review_no`, `review_gmt_data`,
`review_fuel_display`, `review_air_display`, `review_rad`, `review_flame_length_mm`, `review_fuel_rate_sccm`,
`review_fuel_mg_s`, `review_air_velocity_cm_s`, `review_fuel_velocity_cm_s`, and
`review_flame_length_mm_sheet2` where sheet (2)'s re-measurement differs (75P16-7, 75P16-8). The review has no
quality or remark column (sheet (2)'s `SP?` column is empty).

- Brackets are not interpolations. The review's fuel display differs from the time-interpolated log value by up
  to 22 counts (50P16-2: 156 against 134). It is a separate reading of a frame between two logged rows. Only two
  brackets run from an unmarked row to a Y row (E16-4, 50P16-5), and one starts at an N row (50P16-2).
- Log Y marks: 8 of the 15 unique rows are Y, 7 are unmarked, none is N. Of the log's 31 Y rows, 10 are tagged
  (8 unique, 2 in brackets). 13 are in a reviewed burn where the review chose another frame: earlier in 9 of 13,
  at a higher fuel display in 12 of 13, and with a longer flame in all 13, by 0.8-27 mm (P7-1: 105.5 mm at fuel
  350 against the Y row's 91.7 mm at 314). 8 are in burns the review leaves out; 6 of these are 50 % propylene
  on the 0.76 and 0.41 mm nozzles, in burns the log comments as lifted (the presentation keeps attached flames
  only).
- Where a tagged row has a log length, it agrees with the review's within 2.1 mm (r331, r222, r254).
- Review-sheet oddities: E16-3 gives Rad 100 and fan 48; E16-4's Rad is typed as a time (4:10); P16-7 and P7-5
  have flame-off before ignition (as in the log); sheet (2) gives 09:40:59 for 50P16-5 (09:41:01 in sheet 1).

Unique matches (Δt = log minus review):

| # | TP | GMT day | review data | fuel / air | Rad | length mm | log row (measurement, mark) | Δt | log fuel / air | log Rad |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | P16-3 | 048 | 17:45:17 | 164 / 30 | 1 | 45.5 | r59 (still, -) | -2 s | 164 / 30 | - |
| 16 | 75P16-4 | 173 | 11:09:27 | 105 / 51 | 2.29 | 26.7 | r427 (video, -) | -2 s | 104 / 51 | 2.16 |
| 17 | 75P16-5 | 052 | 16:23:20 | 79 / 37 | 1.66 | 21.1 | r103 (still, -) | -11 s | 79 / 37 | - |
| 19 | 75P16-7 | 119 | 10:29:30 | 49 / 20 | 1.18 | 14.2 | r331 (video, Y) | +0 s | 49 / 20 | 1.18 |
| 26 | 75P7-4 | 173 | 12:40:44 | 156 / 47 | 3.72 | 44.0 | r461 (video, Y) | -5 s | 156 / 47 | 3.8 |
| 29 | 50P16-3 | 167 | 09:23:36 | 115 / 20 | 2.16 | 26.5 | r368 (video, Y) | +2 s | 115 / 20 | 2.14 |
| 30 | 50P16-4 | 167 | 09:32:48 | 155 / 34 | 2.69 | 33.4 | r371 (video, Y) | -1 s | 155 / 34 | 2.69 |
| 32 | 50P16-6 | 167 | 09:45:36 | 234 / 58 | 3.77 | 49.5 | r375 (video, Y) | +0 s | 234 / 58 | 3.77 |
| 35 | P16-2 | 058 | 09:47:29 | 61 / 42 | 1.3 | 19.6 | r229 (still, -) | -2 s | 61 / 42 | - |
| 36 | P16-3 | 058 | 09:44:41 | 46 / 30 | 1.24 | 15.8 | r222 (video, -) | +4 s | 46 / 29 | 1.25 |
| 39 | P16-6 | 174 | 10:49:00 | 33 / 17 | 1.16 | 13.4 | r470 (video, -) | +10 s | 34 / 17 | 0.97 |
| 40 | P16-7 | 174 | 11:05:39 | 60 / 38 | 1.5 | 17.6 | r473 (video, Y) | -3 s | 60 / 38 | 1.5 |
| 47 | P7-4 | 174 | 12:34:40 | 62 / 32 | 1.64 | 21.9 | r517 (video, -) | -7 s | 61 / 32 | 1.56 |
| 50 | P7-7 | 174 | 12:47:37 | 80 / 40 | 2.23 | 26.3 | r529 (video, Y) | +10 s | 80 / 40 | 2.25 |
| 53 | P4-2 | 058 | 11:26:27 | 113 / 22 | 3.56 | 47.0 | r254 (video, Y) | +4 s | 113 / 22 | 3.64 |

Brackets (row before, row after):

| # | TP | GMT day | review data | fuel / air | Rad | length mm | before | after |
|---|---|---|---|---|---|---|---|---|
| 4 | E16-4 | 168 | 09:50:28 | 209 / 45 | - | 57.5 | r405 (-) 09:50:18 181/45, Rad 4.1 | r406 (Y) 09:50:35 211/44, Rad 4.1 |
| 14 | 75P16-2 | 173 | 10:38:23 | 147 / 69 | 3.24 | 35.8 | r413 (-) 10:38:03 134/72, Rad 2.45 | r414 (-) 10:38:25 149/69, Rad 3.24 |
| 20 | 75P16-8 | 119 | 10:38:53 | 72 / 35 | 1.4 | 20.4 | r334 (-) 10:38:41 59/35, Rad 1.07 | r335 (-) 10:39:07 79/35, Rad 2.08 |
| 22 | 75P16-10 | 136 | 15:53:36 | 61 / 31 | 1.5 | 17.9 | r339 (-) 15:53:26 49/31, Rad 1.05 | r340 (-) 15:54:02 63/31, Rad 1.77 |
| 24 | 75P7-2 | 136 | 17:23:30 | 70 / 22 | 1.54 | 22.0 | r364 (-) 17:23:15 55/21, Rad 1.37 | r365 (-) 17:23:43 69/21, Rad 2.13 |
| 28 | 50P16-2 | 055 | 09:37:29 | 156 / 34 | 2.78 | 32.5 | r160 (N) 09:37:11 70/34, Rad 0.76 | r164 (-) 09:37:36 159/33, Rad - |
| 31 | 50P16-5 | 167 | 09:41:01 | 207 / 49 | 3.57 | 42.4 | r373 (-) 09:40:55 194/49, Rad 3.14 | r374 (Y) 09:41:38 209/49, Rad 3.51 |
| 38 | P16-5 | 174 | 10:46:19 | 48 / 28 | 1.44 | 15.5 | r467 (-) 10:46:14 45/28, Rad 1.13 | r468 (-) 10:46:25 50/28, Rad 1.55 |
| 42 | P16-9 | 174 | 11:22:35 | 81 / 56 | 2.02 | 23.1 | r481 (-) 11:22:23 75/56, Rad 1.65 | r482 (-) 11:22:44 91/56, Rad 2.54 |
| 43 | P16-10 | 174 | 11:25:31 | 64 / 49 | 1.66 | 19.4 | r485 (-) 11:25:18 65/55, Rad 1.41 | r486 (-) 11:25:40 65/43, Rad 1.85 |
| 48 | P7-5 | 174 | 12:36:49 | 44 / 20 | 1.29 | 15.9 | r520 (-) 12:36:42 40/20, Rad 1.08 | r521 (-) 12:37:05 48/20, Rad 1.56 |
| 49 | P7-6 | 174 | 12:44:11 | 111 / 60 | 2.9 | 31.8 | r523 (-) 12:43:58 115/61, Rad 3.37 | r524 (-) 12:44:23 85/60, Rad 1.85 |
| 54 | P4-3 | 174 | 11:48:02 | 145 / 17 | 4.1 | 59.2 | r501 (-) 11:47:46 130/17, Rad 4.1 | r502 (-) 11:48:09 150/17, Rad 4.1 |

No match (most review frames fall before the first logged row of their burn, at a different fuel display):

| # | TP | GMT day | review data | fuel / air | Rad | length mm | why |
|---|---|---|---|---|---|---|---|
| 1 | E16-1 | 045 | 15:03:15 | 285 / 68 | 4.1 | 75.4 | no burn with this ignition time in the log. Its No. 3 points at log TP 3 (r9-r11: air 67, fan 139 as here) but that burn ignited at 15:35:44 at fuel 229-230 |
| 2 | E16-2 | 045 | 14:37:56 | 207 / 42 | 0.28 | 54.0 | burn r5-r6; 528 s before the first logged row (r5: 173/45); log Y on r5 |
| 3 | E16-3 | 045 | 14:50:32 | 211 / 48 | 100 | 55.8 | burn r7-r8; 65 s before the first logged row (r7: 85/49) |
| 5 | E16-5 | 045 | 15:48:47 | 140 / 26 | 4.1 | 37.0 | burn r14-r15; 13 s before the first logged row (r15: 106/25); log Y on r14 |
| 6 | E7-1 | 045 | 17:28:29 | 335 / 25 | 4.1 | 105.2 | burn r26-r27; after the last logged row. Displays equal r26 (335/25, length 102.5 mm) but the review time is 22 s later and 8 s after the logged flame-off |
| 7 | P16-1 | 048 | 16:54:27 | 276 / 54 | 1.73 | 71.4 | burn r47-r48; 22 s before the first logged row (r48: 257/53) |
| 8 | P16-2 | 048 | 17:12:08 | 230 / 45 | 1.43 | 61.1 | burn r53-r56; 14 s before the first logged row (r55: 218/45) |
| 10 | P7-1 | 052 | 11:39:28 | 350 / 42 | 4.1 | 105.5 | burn r61-r64; 24 s before the first logged row (r63: 315/41); log Y on r61 |
| 11 | P7-2 | 052 | 11:43:05 | 240 / 29 | 4.1 | 75.6 | burn r65-r68; 21 s before the first logged row (r67: 232/28); log Y on r65 |
| 12 | P7-3 | 052 | 11:49:43 | 206 / 24 | 4.1 | 64.3 | burn r69-r72; 16 s before the first logged row (r71: 193/23); log Y on r69 |
| 13 | 75P16-1 | 052 | 16:14:10 | 149 / 75 | 3.05 | 37.7 | burn r100-r101; 9 s before the first logged row (r100: 121/75) |
| 15 | 75P16-3 | 052 | 16:26:48 | 117 / 61 | 2.9 | 31.7 | burn r105-r107; 8 s before the first logged row (r107: 131/60) |
| 18 | 75P16-6 | 052 | 16:09:59 | 50 / 20 | 1.12 | 14.5 | burn r98-r99; fuel display outside the neighbouring logged rows |
| 21 | 75P16-9 | 136 | 15:57:52 | 52 / 24 | 1.27 | 15.6 | burn r341-r345; fuel display outside the neighbouring logged rows; log Y on r344 |
| 23 | 75P7-1 | 052 | 17:30:19 | 149 / 46 | 3.4 | 39.5 | burn r118-r123; 15 s before the first logged row (r121: 94/47) |
| 25 | 75P7-3 | 136 | 17:21:52 | 68 / 22 | 1.54 | 20.2 | burn r362-r365; 33 s before the first logged row (r362: 25/22). Repeats 75P7-2's ignition, flame-off and Rad |
| 27 | 50P16-1 | 055 | 09:40:13 | 205 / 49 | 3.78 | 41.7 | burn r165-r171; fuel display outside the neighbouring logged rows; log Y on r165, r166 |
| 33 | 50P16-7 | 055 | 08:56:28 | 103 / 18 | 0.49 | 22.1 | burn r145-r151; 9 s before the first logged row (r148: 82/17); log Y on r145 |
| 34 | P16-1 | 058 | 09:55:32 | 84 / 61 | 2.08 | 25.7 | burn r232-r236; 6 s before the first logged row (r232: 81/60); log Y on r232 |
| 37 | P16-4 | 058 | 09:38:07 | 37 / 16 | 1 | 14.0 | burn r218-r221; 7 s before the first logged row (r218: 35/16); log Y on r218 |
| 41 | P16-8 | 174 | 11:14:07 | 98 / 67 | 2.4 | 26.5 | burn r474-r476; fuel display outside the neighbouring logged rows |
| 44 | P7-1 | 058 | 10:41:26 | 84 / 50 | 2.13 | 26.6 | burn r249-r251; 4 s before the first logged row (r249: 81/50) |
| 45 | P7-2 | 058 | 10:36:31 | 69 / 37 | 1.79 | 22.8 | burn r246-r248; 7 s before the first logged row (r246: 63/36) |
| 46 | P7-3 | 058 | 12:45:55 | 64 / 35 | 1.66 | 21.7 | burn r272-r272; 11 s before the first logged row (r272: 30/35) |
| 51 | P7-8 | 058 | 10:13:37 | 41 / 14 | 1.08 | 14.2 | burn r240-r242; 8 s before the first logged row (r240: 32/14) |
| 52 | P4-1 | 058 | 11:32:14 | 136 / 35 | 4.1 | 53.3 | burn r258-r259; 12 s before the first logged row (r258: 121/35) |
| 55 | P4-4 | 058 | 11:23:35 | 92 / 12 | 3.5 | 37.7 | burn r252-r253; 6 s before the first logged row (r252: 85/11) |

**PSI-159 ACME CFI-G** (333 tests).

- Inverse rows: `o2_is_burner_stream` and (except six rows at 49.5 kPa) `pressure_9pct_above_nominal`.
- Normal rows give the nominal fill pressure; the transducer reads about 3 kPa more (patch D32).
- "flash" ignitions: `flash_only`.
- Peak burner temperature above 450 °C: `burner_over_limit` (30 rows).
- `extinction_mode` = `flow_terminated` covers two endings that the test sheets tell apart: 54 time-outs and 24
  stops by the burner temperature limit (note D58, `filter_tests(sheet_out="temp_limit")`). A temperature-limit
  stop is neither a self-extinction nor a flame that lasted the scripted time. No sheet contradicts the column.
  The two self-extinction models leave the 24 out (`docs/models.md`).
- Six rows listed as not ignited were not ignition attempts: nothing flowed, or it was a no-flame test of the
  igniter (21196 A1, 21130 A4, 21242 P2: `conflicts_with_raw`, patches D45 to D47; 21125 A4, 21125 H3, 21209 A2,
  which have no data file: `conflicts_with_test_sheet`, D48 to D50). `ignited` stays false; leave these rows out
  of ignition statistics with `exclude_flags`, which also drops the other rows carrying those flags. The two
  ignition models leave out exactly these six, by patch id.
- Burner O2 the flow controllers contradict (`conflicts_with_raw` on `x_o2_burner`): 21256 C2 (no nitrogen
  flowed: 85%, not 50%; D39) and 21277 P1 (oxidizer and nitrogen flows swapped: about 55%, not 30%; D40).
- Day 21277, oxidizer bottle nearly empty: the measured oxidizer flow of C2, F2, M1 and N1 is 41 to 90% of the
  table's `O2 flow rate (mg/s)` (in extra), which is the setpoint (`conflicts_with_raw`, D41 to D44).
- 21291 A1 and C1: `burn_time_s` spans six hot flames with cool flames between, not one flame
  (`conflicts_with_test_sheet`, D56, D57).
- For inverse rows `fuel_fraction` is the ambient fuel fraction.
- Ten recorded test points have no row (notes D28, D64). Nine are failed ignitions of day 21106 that the table
  leaves out (21106A1 to A3 at about 39% O2; G1 to G5 and G8 at about 21% O2): the recordings show fuel flowing for
  13 to 15 s with no flame, at most flashes around the igniter. 21242F1 was aborted before any gas flowed. No rows
  were added, so the table's count of failed ignitions, and the ignition models trained on it, miss these nine.

## Conflicts with the raw sensor data

`data/corrections/tests_patches.json` lists every place where the raw sensor files contradict an experiment
table: the table value, the raw value, the evidence and the action. `build_tests.py` applies it and fails if a
patch no longer matches the table. The same list is the `discrepancies` table and `fif.api.discrepancies()`.

| Action | Effect on `tests` | Flag |
|---|---|---|
| `replace` | the raw value replaces the table value; the table value is kept in extra as `<column>_original` | `corrected_from_raw` |
| `fill` | an empty cell is filled from the raw data | `filled_from_raw` |
| `flag` | the value is kept, because the raw evidence is not decisive (sensor accuracy unknown, a difference a few seconds wide) or because two sources disagree and neither can be ruled out; also marks a row that was not a test (PSI-101 Teflon 57) | `conflicts_with_raw` |
| `note` | nothing; the entry concerns a whole investigation (for example recorded test points missing from the table) | - |

A patched row lists its patch ids in extra `discrepancies`. Raw files exist only for PSI-10, 23, 39, 159, 98, 100
and 101, so the other tables could be checked against the reports only.

`column` is a `tests` column, or a source column the table keeps only in `extra` (`O2 flow rate (mg/s)`); a value
in extra can be flagged but not changed.

### Test sheets

For PSI-10 and PSI-159 the operators filled in a paper sheet per test point. The scans were read by an AI model
(`data/transcriptions/`, table `test_sheets`, `docs/formats.md`) and nobody has checked the readings. A patch
whose only evidence is a sheet therefore:

- carries `"basis": "test_sheet"` and the flag `conflicts_with_test_sheet`, not `conflicts_with_raw`;
- can only be a `flag` or a `note`: a sheet never changes a value;
- names the page and quotes it (`sheet`: file, page, quote). `build_tests.py` fails if the quote is no longer on
  that page of the transcription, so a patch cannot outlive a corrected reading.

Where the sensor data confirm what a sheet says, the patch is an ordinary `conflicts_with_raw` one and cites the
sheet as a second source. What the sheets were checked for and did not show: pressures agree with the tables to
within the known offsets (notes D26, D32); `Ignited?` never contradicts `ignited` (56 no, 252 yes on the PSI-159
rows that have both); the ending ticked never contradicts `extinction_mode`. Differences between a sheet and the
as-run parameter file that leave the table untouched (21301H2 and H3 fuel flows swapped on the sheets, 19123L1
fuel flow, 21106D1 post-test pressure) are in `test_sheets.differs_text` and the written fields, not patches.

## Outcomes read from notes (PSI-25, PSI-26)

The BASS and BASS-II tables say what was burned and at which settings, not how the burn ended. The ending is in
free text: for BASS (PSI-26) the crew notes of the as-run matrix (`extra.asrun_notes`), for BASS-II (PSI-25) the
shorthand in the flow cells (`Air display`, `Fan display`: "5 down to ext", "10 blowoff", "no ign at any flow").
`data/corrections/tests_outcomes.json` holds one reading per run that states its ending: the outcome, the cause, the
cell and the quoted words. `build_tests` refuses an entry whose quote is no longer in that cell.

| | no_ignition | extinguished: low_flow | blowoff | nitrogen | unspecified | burned_out | not stated |
|---|---|---|---|---|---|---|---|
| PSI-26 BASS (121) | 17 | 42 | 0 | 2 | 7 | 12 | 41 |
| PSI-25 BASS-II (129) | 2 | 16 | 7 | 0 | 0 | 0 | 104 |

How to read it:

- It is a reading of prose, done once by a language model and checked by hand, not a NASA column. Show the quote
  with the outcome.
- One outcome per run: the final end of the flame. A partial blow-off that left a wake flame is not an extinction.
- `low_flow` covers two different events, told apart by `outcome_action`: `flow_shut_off`, the crew stopped the
  flow to end the run (in microgravity the flame goes out without it; not a limit), and `flow_reduced`, the flow
  was turned down until the flame went out at a finite setting (a quenching limit).
- Runs where the notes say the flame survived maximum flow or nitrogen but not how it ended are null, as are two
  runs whose igniter broke.
- BASS-II has no notes column, so only the 25 runs whose flow cell carries a word are filled.

What was done to the flow on the 74 extinguished runs (`outcome_action`), and how many state the setting
(`outcome_setting`):

| | flow_reduced | flow_shut_off | flow_raised | nitrogen | none | not stated | with a setting |
|---|---|---|---|---|---|---|---|
| PSI-26 BASS (51) | 19 | 22 | 0 | 2 | 6 | 2 | 18 |
| PSI-25 BASS-II (23) | 14 | 2 | 7 | 0 | 0 | 0 | 13 |

- `flow_raised` and `nitrogen` follow from the cause. For `low_flow` and `unspecified` the action is read per
  run and stored as `action` in `tests_outcomes.json`; `build_tests` refuses a `low_flow` or `unspecified` entry
  without one. Runs 87 ("Candle out at flow change", direction not given) and 32 are null.
- `flow_reduced` means the words or the settings cell put the extinction at a finite setting, in one step or
  many. Runs 31, 54, 82, 82a and 100 went out at fan 39 to 40, one or two counts above the stopped fan (38): a
  limit only within the resolution of the fan. On runs 99, 105 and 118 the notes say "very low" or "finite" flow
  without a setting.
- `none` is a flame that went out with no flow change tied to it ("extinguished all by itself"). These six keep
  the cause `unspecified`; run 78 names its setting (pot 0.4).
- `outcome_setting` is the knob and the number as logged; `build_tests` refuses a setting whose number is not in
  the named cell. In BASS-II the knob is the fan pot where the cell says "pot" or lists decimals below 1 in the
  same series as cells that do. 25 of the 33 `flow_reduced` runs state it, 4 `flow_raised` runs (the pot or fan
  value at blowoff), run 64 (GN2 pot) and run 78. It is not converted to cm/s: the fan calibration does not
  reach these settings.
- `flow_cm_s` on these rows is the log's single "Air display" value and is not the flow at extinction.
- Readings where two cells disagree, each with the reason in `extra.outcome_doubt`: M17 (air display "0ext",
  fan pot "0.3ext": read as a quench at pot 0.3), BASS 86a (notes "stepped to 0 flow", fan cell "0.31 (out)":
  read as a quench at pot 0.31), P5 and P13a (air display "5 down to ext", fan pot "... 0 ext": shut off; the
  quote is now the fan cell), 31 (notes "pot ~ 39", a fan-display value).
- Three `low_flow` causes rest on the fan and air cells, not on the quoted words, and carry
  `extra.outcome_cause_inferred`: 87, 118 (2013) and 89. The cause was left as it was.

## BASS-II spread rates (PSI-25, M series)

The PSI table has no spread rate for BASS-II. The BASS-II Summary Report (NASA/TM-20210011385), Table 5.1 (PDF
page 65, printed page 57) lists, for the 20 thick-PMMA slab tests in opposed flow (M1 to M20): thickness, width,
one or two sides burning, the flow velocities at which a spread rate was tracked, the spread rate at each, burn
time, and initial and final O2. The table is transcribed in `data/corrections/tests_spread_bass2.json`, from the
rendered page with every cell checked against the extracted text; the two agree on every cell, and a test checks
the file against the extracted text. `build_tests` fails if an entry does not match exactly one row or has a
different number of velocities and rates.

What the M rows get:

- `extra.spread_steps`: the steps in the report's order, `[{"flow_cm_s": 10, "spread_rate_mm_s": 0.106}, ...]`.
  18 tests, 39 steps (5 tests with one step, 6 with two, 6 with three, 1 with four), 0.012 to 0.144 mm/s.
  M6 and M12 are "Not tracked" (`extra.spread_rate_note`); their listed velocities are in
  `extra.report_velocity_cm_s`.
- `spread_rate_mm_s` stays null on all 20, also on the five one-step tests. A rate here is the rate at one flow
  step, and the row has no flow for it (`flow_cm_s` is null, the run log shows the flow was changed in those five
  tests too). Filling the column for five tests would offer a subset as if it were the set, and no average is taken.
- `config` = `opposed flow` ("The airflow was always opposed") and `burn_time_s` (report minutes x 60).
- `extra.report_width_cm` (2.2 or 1.2) and `extra.report_sides_burning` (1 or 2). The PSI sample label says 2 or
  1 cm wide on all 20 rows; the report's own text uses both pairs of numbers, so this is read as nominal against
  actual width and is not flagged. The label states the sides on 6 rows; they agree.
- `extra.report_source` (report, table, page) and the flag `value_from_report`.

Compared with the PSI row at build time, a difference being flagged `conflicts_with_report` and never written
over: thickness (20 of 20 agree), sides (6 of 6), initial O2 (20 of 20) and final O2 (20 of 20).

Velocities. The report's velocities are not the run log's: in 10 of the 20 tests at least one is not among the
whole-cm/s values of the `Air display` cell (9 against "10 8" for M1, 21 against "10 20 15 12" for M11); the
report does not say how they were obtained. Two tests are flagged `conflicts_with_report`, with the words in
`extra.report_value`:

- M12: the table lists 12 and 10 cm/s (spread not tracked). The Air display says "<1", and the report's own
  Figure 5.4(c) caption gives <1 cm/s for that sample.
- M14: rates are given at 15, 14 and 10 cm/s; the Air display says "10 ~8". The rates are kept as reported.

`data/processed/spread_steps.{parquet,csv}` (`api.table("spread_steps")`) is the same data with one row per test
and step (39 rows): `test_id`, `step`, `n_steps`, `flow_cm_s`, `spread_rate_mm_s`, `thickness_mm`, `width_cm`,
`sides_burning`, `x_o2_initial`, `x_o2_final`, `burn_time_s`, `flags`, `source`, and `source_file` + `source_row`,
the key of the `tests` row. It is not in `data/export/`.

**The steps of a test are not independent points.** They are successive flow settings on one sample that is
already burning and preheated, in the order listed, while the O2 falls (by 0.3 to 3.2 vol% over a test). O2 was
measured only at the start and the end of a test, not per step: `x_o2_initial` and `x_o2_final` repeat on every
step of a test, and the report itself assumes a linear decay between them. The honest sample size is the number
of tests, 18 (5 one-sided, 13 two-sided), not 39. A fit of spread rate against flow across all 39 rows treats
within-test trends as independent evidence and mixes thickness, width, sides and O2; group by `test_id` or use a
per-test effect.
