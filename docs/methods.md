# Data guide for the dashboard

Everything the dashboard needs is in this repo. Raw NASA files (`data/raw/`, 7.5 GB) are not needed at run time.

## What to load

| You want | Use | Size |
|---|---|---|
| A static front end, no backend | `data/export/*.json` (pre-computed) | 14 MB |
| A Python backend or an AI with tools | `fif.api` functions, specs in `data/processed/tools.json` | - |
| Your own queries | `data/processed/*.parquet` / `.csv`, columns in `data/processed/catalog.json` | 33 MB |
| Text for people | `docs/digest/` (one page per investigation, `synthesis.md`) | - |

`data/export/`:

| File | Content |
|---|---|
| `investigations.json` | 24 cards: accession, acronym, title, one-line description, pillars, fuel phases, counts, dataset `doi`, `doi_url`, `psi_url` |
| `records.json` | the 24 full knowledge records (question, physics with LaTeX equations, method, findings with quoted sources, limitations, open questions, dashboard hooks) |
| `tests.json` | the per-test table, 2,177 rows (dictionary: `docs/tests-table.md`) |
| `coverage.json` | test counts on the O2-pressure grid, for all fuels and per phase, with the reference atmospheres |
| `relevance.json` | scenario rankings for 5 scenarios x 3 fuel phases x 4 pillar choices, keyed `scenario|phase|pillar` |
| `models.json` | the 8 model cards: inputs, valid range, coefficients, cross-validated score, dropped candidates |
| `timeseries_features.json` | per-recording sensor summaries, 1,075 rows (burn duration, peak temperatures, pressure; droplet and flame diameters for 24 CFI tests) |
| `timeseries_examples.json` | decimated sensor traces for the two time-series questions in the question bank |
| `discrepancies.json` | errors and doubts in the PSI tables: 61 conflicts and notes with evidence (10 of the conflicts rest on a hand-filled test sheet only), every changed value, flag meanings |
| `test_sheets.json` | `{notes, rows}`: the 637 hand-filled ACME test sheets of PSI-10 and PSI-159, one row per page (`docs/formats.md`). An AI reading of scans, not checked by a human: show the note with any value |
| `questions.json` | the question bank: question, call, chart, answer |
| `synthesis.json` | key messages, limits, microgravity-vs-1-g comparisons, ranked gaps, lineage, research questions |

Rebuild after any table change: `uv run python -m fif.pipeline.build_catalog`.

One table has no export and no function: `data/processed/spread_steps` (`fif.api.table("spread_steps")`), the 39
BASS-II spread rates by test and flow step. Read the independence caveat in `docs/tests-table.md` ("BASS-II spread
rates") before plotting it: the sample size is 18 tests, not 39 points.

## Functions (`fif/api.py`)

Each returns `{data, chart, sources, notes}`. `chart` is a suggestion, `sources` are citations to show, and
`notes` are caveats that must appear next to the answer. From a non-Python backend:
`uv run python -m fif.api relevance '{"scenario": "moon-habitat", "pillar": "detection"}'`.

| Function | Answers |
|---|---|
| `search_investigations(query, pillar, fuel_phase, flight)` | which investigations exist / match a topic |
| `get_investigation(accession, sections)` | everything about one investigation |
| `filter_tests(accession, fuel, fuel_phase, config, x_o2, pressure_kpa, flow_cm_s, extinction_mode, outcome, outcome_action, sheet_out, sheets, ...)` | what was tested and what happened; `sheets=True` attaches the operators' test sheet to PSI-10 and PSI-159 rows |
| `compare(accessions)` | side-by-side: question, fuels, ranges, sensors, findings |
| `coverage(x, y, **filters)` | where data exist and which atmospheres are empty; each reference gives its cell count in total and by fuel phase; its `nearest_test` lists in `not_measured` the columns placed from the investigation's narrow stated range, not measured for that test |
| `relevance(scenario, fuel_phase, pillar)` | which investigations matter for a scenario, and how far the data are from it |
| `find_evidence(query, accession)` | passages: reviewed findings and raw document text (keyword search) |
| `insights(topic, accession)` | cross-investigation conclusions, limits, gaps, research questions |
| `timeseries(test_id, channels, test_point, accession)` | sensor traces of one test; reads `data/raw/` (or `$FIF_RAW_ROOT`); `demo/server.py` fetches the missing files from PSI on demand (`docs/formats.md`) |
| `discrepancies(accession, test_id)` | errors and doubts in the original PSI tables: raw-data conflicts, changed values, flag meanings, removed files |
| `predict(model_id, **conditions)` | small per-investigation models (`docs/models.md`); no `model_id` lists them, `compact=True` for the short list |

For an AI assistant: pass `data/processed/tools.json` as the tool list and route calls through
`fif.tools.call(name, arguments)`. Tell the model to cite the `sources` and repeat the `notes`.

Citation ids: `[PSI-26 F3]` is finding 3 of the PSI-26 record (`L` = limitation, `Q` = open question). Each
finding carries its own sources: a PSI file with page and a verbatim quote, or an external URL/DOI.

## Scenario relevance score

`relevance()` ranks the investigations for a scenario (atmosphere, gravity, kind of fuel, fire-safety pillar).
It is a transparent heuristic, not a measurement: weights and scales are constants at the top of `fif/api.py`.

$$
S = 100 \, \frac{\sum_k w_k \, c_k}{\sum_k w_k}, \qquad c_k \in [0, 1]
$$

| Component | Weight | Definition |
|---|---|---|
| conditions | 0.40 | $c = e^{-d/2}$, with $d$ the distance from the scenario to the investigation's nearest test |
| material | 0.25 | fuel-phase transfer: same phase 1.0; gas or droplet flames for a solid hazard 0.4; an aerosol experiment 0.2-0.3 (the `TRANSFER` table in `fif/api.py`) |
| pillar | 0.20 | 1.0 if the requested pillar is the investigation's main applied pillar, 0.7 if secondary, 0.3 otherwise. With no pillar requested: 1.0 for any investigation with an applied pillar, 0.3 for the rest |
| evidence | 0.15 | $0.5\,f + 0.5\,\min(1, n_{high}/8)$, with $f$ = 1 for flight data, 0.5 for a ground investigation, and $n_{high}$ the number of high-confidence findings in the record |
| gravity | 0.10 | only for partial-gravity scenarios ($0 < g < 1$): $\min(1, n/3)$, with $n$ the microgravity-vs-1-g comparisons in the synthesis that cite the investigation |

$$
d = \sqrt{\left(\frac{\Delta x_{O_2}}{0.03}\right)^2 + \left(\frac{\Delta p}{15\ \text{kPa}}\right)^2 + \left(\frac{\Delta u}{10\ \text{cm/s}}\right)^2}
$$

- One step is 3 points of O2, 15 kPa or 10 cm/s. These are about the size of differences that change outcomes
  in the data (BASS-II oxygen limits differ by about 2 points between geometries).
- A condition nobody recorded counts as far away as the farthest investigation that did record it, and at
  least 2 steps: an unknown never ranks above a measured value. A condition known only as a wide range (no
  per-test value) uses the distance to that range and lowers the conditions score by 20%. A distance of 0 can
  therefore mean "the stated range contains the point" (BRE, FLEX-2), not "a test was run there".
- The weights are a judgement. Jittering them by 20% keeps FLEX first for a Moon habitat every time, but the
  set of the top five changes in about half the draws: read the ranking as tiers, not as an order.
- `fuel_phase` weights the ranking through the material component; it does not filter it. A droplet or gas-flame
  investigation run at the scenario's atmosphere can therefore rank above every solid-fuel one (FLEX for a Moon
  habitat). Each row says so: `phase_match` is false when the investigation has no fuel of that phase, and
  `nearest_test` is always a test of the requested phase, or null. For an investigation without such a test, the
  test its conditions score and distance come from is in `nearest_test_other_phase`. `closest_same_phase_test`
  gives the nearest test of the requested phase over all investigations, with its distance: use it, not the top
  row, to answer "what is the nearest real test for this material". A `Phase:` note is added when the top of
  the ranking has no test of the requested phase.
- `relevance` raises `ValueError` for an unknown `scenario`, `fuel_phase` (solid, liquid, gas) or `pillar`.
- Eight cabin-air experiments without logged O2 or pressure are placed at the nominal cabin atmosphere
  (20.5-21.5% O2, 98-103 kPa). Each result lists them in `conditions_assumed_cabin_air`.
- A condition with no per-test value is never shown as measured. `conditions_from_range` lists every condition
  read from the investigation's range (stated in the documents or spanned by its other tests), wide or narrow;
  `condition_ranges` gives the range of each, its origin (`from`: digest, tests table, assumed cabin air), for a digest range the `note` saying what it was
  reported for, and
  `wide`. Only a wide range (over 10% of its upper end) takes the 20% discount; a narrow one scores like a
  measured value. Each test dict (`nearest_test`, `nearest_test_other_phase`, `closest_same_phase_test`) lists
  in `not_measured` the columns the tests table has no value for: an O2 or pressure shown for one of them is
  the middle of a narrow range. BASS-II has no per-test pressure at all: its 99.35 kPa is the middle of the
  99.2-99.5 kPa the summary report states for the thin-film tests.
- The output always states the gap: the nearest test of the requested fuel phase and its distance. For a Moon
  habitat and solid fuels that is Saffire-II sample 2-2 (silicone, 22.1% O2, cabin pressure assumed 100 kPa),
  3.2 steps away. A BASS-II PMMA test at 22.2% O2 follows, with a pressure (99 kPa) that is the middle of the
  campaign range, not a reading of that test. The nearest solid-fuel tests with both values in the tests table
  are from BASS: test 2 (SIBAL fabric, 22.7% O2, 100.8 kPa, airflow ramped during the test) at 3.17 steps and
  PMMA tests at 22.4% O2 and 100.1 kPa at 3.22. `closest_same_phase_test` does not return them, because the BASS
  row nearest to the scenario has no O2 value and is placed from the investigation's wide O2 range.
- No PSI test was run at partial gravity. The gravity component does not pretend otherwise; it rewards
  investigations that bracket partial gravity with microgravity and 1-g results.

## Things that will bite

- `x_o2_ambient` is the atmosphere. `x_o2_burner` (up to 0.85) is an oxidiser stream in inverse flames, not an
  atmosphere. Do not plot them on one axis.
- `row_kind`: only `test` rows are single tests. `filter_tests` returns those by default.
- `test_id` is not unique (12 rows share an id, flag `duplicate_id`). The key of a `tests` row is
  `source_file` + `source_row`.
- The `fuel` filter matches a whole fuel name: `ethane` does not return methane, `heptane` returns n-heptane and
  its blends. 85 BASS and BASS-II rows are PMMA by inference from the documents (`fuel_inferred`).
- Flags come in two kinds: a correction or a doubt, and a remark on how to read the row (`o2_is_burner_stream`,
  `ramped`, `smoke_point_bracket`, `planned_not_flown`, `flash_only`, `burner_over_limit`). The `filter_tests`
  note counts them separately.
- `cool_flame` is `True` or empty, never `False`.
- Flagged test rows carry `flags` (corrections and doubts); original values are kept in `extra`. Show a badge on
  flagged rows and link it to `discrepancies(test_id=...)`, so users see where the PSI tables are wrong.
- `find_evidence` is keyword search (TF-IDF), not semantic search. Raw document passages are unreviewed.
- Document text in `evidence` keeps the e-mail and phone of listed authors (people in a PSI record's contact
  block). Postal addresses, other people's e-mails and phones, and private network addresses are replaced by
  `[address removed]`, `[e-mail removed]`, `[phone removed]`, `[ip removed]` (`fif/pipeline/redact.py`). One file
  that holds credentials is not extracted (`evidence_files.status = withheld`).
- Scanned PDFs have no text layer. All 185 of them (1,168 pages) were transcribed by an AI model on 2026-11-14,
  so no file has `evidence_files.status = no_text` today; a scan added later gets it until it is transcribed.
  The evidence builder reads the transcription
  (`data/transcriptions/<accession>/<file_name>.md`, one `## page N` section per PDF page) in place of the PDF:
  the status is `transcribed`, locators are the PDF pages (`p3`), and every chunk
  has `evidence.transcribed = True`. The same redaction applies. This text is a machine reading, not the
  document's own: `find_evidence` returns `transcribed` on each document passage and its source, adds a note when
  any are present, and the search view shows an "AI reading of a scan" chip. Check numbers and names in the scan.
- Test sheets (PSI-10, PSI-159): the form the operators filled in by hand for each test point is in the table
  `test_sheets` (637 pages, 596 of them a `tests` row) and reaches the API through `filter_tests`: `sheets=True`
  adds `test_sheet` to each row that has one (ignited, hot or cool flame, `out`, comments, file and page) and
  `sheet_out="temp_limit"` selects by the ending ticked. It is an AI reading of a scan that nobody checked: the
  result says so in `notes`; repeat it. `out` = `temp_limit` means the flame was cut off because the burner got too
  hot: not an extinction, and not a flame that lasted the scripted time. In the CFI-G table these 24 tests are
  `flow_terminated` together with the 54 time-outs; the Flame Design table has no ending column at all.
- `timeseries_features` (1,075 recordings, PSI-10, 23, 39, 159, 98, 100; 24 of the PSI-39 ones are the
  investigators' reduced droplet data, `test_point` `FLEX-<id>-reduced`) needs no raw files. Its `test_id` is
  the `tests` id (`21088 M4`); `test_point` is the recording's name without the space (`21088M4`).
  `timeseries()` accepts both.
- `*_flow_max_slpm` is the whole-file maximum and is often a controller spike before ignition, above the
  controller's range; use `*_flow_max_burn_slpm` or `*_flow_mean_burn_slpm`. Standard-array radiometer peaks
  with `*_clipped = True` hit the recorder's ceiling and are lower bounds.
- Radiometer and PMT channels in volts have no archived calibration. Compare shapes, not magnitudes.
- `predict` returns no value outside the fitted range or inside a range a card lists as untested, only the
  nearest measured tests; it raises on impossible inputs. Five of the eight models are descriptive only (`use`
  field): for them `predict` never returns a value, only the nearest tests and the observed table. Each headline score comes with a range from resampling the test
  days (`cv_metric.grouped_pooled_ci95_days_resampled`); the ranges are wide, show them.
- The CFI-G models leave out rows whose outcome is not what the target means; each card lists them in
  `training_filter`. The ignition models drop the six rows that were not ignition attempts (patches D45 to D50).
  The self-extinction models drop the 24 flames stopped by the burner temperature limit (12 normal, 12 inverse;
  note D58): they were cut off early, so whether they would have gone out is not known. That set comes from the
  test sheets, an AI reading of scans that nobody checked. Without them the normal-flame model has no established
  held-out skill (AUC 0.69, range 0.36-0.80), so it is descriptive only: show its observed table and nearest tests.
- A `predict` value for a quantity (the two FLEX models) comes with named fields: `prediction` and `interval`
  `[low, high]` in `unit`; `interval_nominal` (0.9, the target the range is built for); `interval_coverage`, the
  share actually reached on held-out test days as counts (`n_inside`, `n`, and the same per fuel under
  `by.levels`, each with a `verdict`); `interval_clipped` (true when the lower end was cut at 0 because the
  quantity cannot be negative) with `interval_low_unclipped` (the value before the cut) and `interval_unclipped`
  (the whole range before it). When even the upper end is below 0, `interval` is null, `interval_clipped` is
  false (nothing was cut: there is no range) and `interval_unavailable` says why (null otherwise). When the
  estimate itself is negative (an untested combination of inputs) it is withheld: `prediction` and `interval` are
  null, `prediction_below_floor` is true, `prediction_unavailable` says why (null otherwise) and `prediction_raw`
  keeps the number as computed, a diagnostic only, never to be shown as a result. A non-null `prediction` is
  never below 0 and lies inside any non-null `interval`. `interval_method` (one line) and `accession` (the
  source). The burning-rate range held 81 of 103 n-heptane tests, clearly under 90%:
  say so when showing a heptane range. For the probability models `cv_metric` carries `brier_grouped_pooled`
  and `brier_baseline_grouped_pooled` next to the AUC.
- Solid-fuel tests cover 13.6-22.7% O2 at about 1 atm only (the lowest that burned is 14.2%). Anything about solids in exploration atmospheres
  is an extrapolation from gas-burner and droplet experiments.
