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
| `discrepancies.json` | errors and doubts in the PSI tables: 36 raw-data conflicts and notes with evidence, every changed value, flag meanings |
| `questions.json` | the question bank: question, call, chart, answer |
| `synthesis.json` | key messages, limits, microgravity-vs-1-g comparisons, ranked gaps, lineage, research questions |

Rebuild after any table change: `uv run python -m fif.pipeline.build_catalog`.

## Functions (`fif/api.py`)

Each returns `{data, chart, sources, notes}`. `chart` is a suggestion, `sources` are citations to show, and
`notes` are caveats that must appear next to the answer. From a non-Python backend:
`uv run python -m fif.api relevance '{"scenario": "moon-habitat", "pillar": "detection"}'`.

| Function | Answers |
|---|---|
| `search_investigations(query, pillar, fuel_phase, flight)` | which investigations exist / match a topic |
| `get_investigation(accession, sections)` | everything about one investigation |
| `filter_tests(accession, fuel, fuel_phase, config, x_o2, pressure_kpa, flow_cm_s, extinction_mode, outcome, outcome_action, ...)` | what was tested and what happened |
| `compare(accessions)` | side-by-side: question, fuels, ranges, sensors, findings |
| `coverage(x, y, **filters)` | where data exist and which atmospheres are empty; each reference gives its cell count in total and by fuel phase |
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
- The output always states the gap: the nearest test of the requested fuel phase and its distance. For a Moon
  habitat and solid fuels that is Saffire-II sample 2-2 (silicone, 22.1% O2, cabin pressure assumed 100 kPa),
  3.2 steps away; the nearest test with both values measured is a BASS-II PMMA test at 22.2% O2 and 99 kPa.
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
- Scanned PDFs have no text layer (`evidence_files.status = no_text`). Where an AI model has transcribed the page
  images (`data/transcriptions/<accession>/<file_name>.md`, one `## page N` section per PDF page), the evidence
  builder reads that file instead: the status is `transcribed`, locators are the PDF pages (`p3`), and every chunk
  has `evidence.transcribed = True`. The same redaction applies. This text is a machine reading, not the
  document's own: `find_evidence` returns `transcribed` on each document passage and its source, adds a note when
  any are present, and the search view shows an "AI reading of a scan" chip. Check numbers and names in the scan.
- `timeseries_features` (1,075 recordings, PSI-10, 23, 39, 159, 98, 100; 24 of the PSI-39 ones are the
  investigators' reduced droplet data, `test_point` `FLEX-<id>-reduced`) needs no raw files. Its `test_id` is
  the `tests` id (`21088 M4`); `test_point` is the recording's name without the space (`21088M4`).
  `timeseries()` accepts both.
- `*_flow_max_slpm` is the whole-file maximum and is often a controller spike before ignition, above the
  controller's range; use `*_flow_max_burn_slpm` or `*_flow_mean_burn_slpm`. Standard-array radiometer peaks
  with `*_clipped = True` hit the recorder's ceiling and are lower bounds.
- Radiometer and PMT channels in volts have no archived calibration. Compare shapes, not magnitudes.
- `predict` returns no value outside the fitted range or inside a range a card lists as untested (normal CFI-G
  flames at 25-35% O2), only the nearest measured tests; it raises on impossible inputs. Four of the eight
  models are descriptive only (`use` field). Each headline score comes with a range from resampling the test
  days (`cv_metric.grouped_pooled_ci95_days_resampled`); the ranges are wide, show them.
- Solid-fuel tests cover 13.6-22.7% O2 at about 1 atm only (the lowest that burned is 14.2%). Anything about solids in exploration atmospheres
  is an extrapolation from gas-burner and droplet experiments.
