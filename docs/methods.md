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
| `investigations.json` | 24 cards: accession, acronym, title, one-line description, pillars, fuel phases, counts, dataset `doi`, `doi_url`, `psi_url`, `location` (where it ran) |
| `records.json` | the 24 full knowledge records (question, physics with LaTeX equations, method, findings with quoted sources, limitations, open questions, dashboard hooks) |
| `tests.json` | the per-test table, 2,177 rows (dictionary: `docs/tests-table.md`) |
| `publications.json` | per accession: `publications` (the record's papers, each with its `review`) and `publication_review` (counts), as `get_investigation` returns them |
| `coverage.json` | test counts on the O2-pressure grid, for all fuels and per phase, with the reference atmospheres |
| `relevance.json` | scenario rankings for 5 scenarios x 3 fuel phases x 4 pillar choices, keyed `scenario|phase|pillar` |
| `models.json` | the 8 model cards: inputs, valid range, coefficients, cross-validated score, dropped candidates |
| `timeseries_features.json` | per-recording sensor summaries, 1,075 rows (burn duration, peak temperatures, pressure; droplet and flame diameters for 24 CFI tests) |
| `timeseries_examples.json` | decimated sensor traces for the two time-series questions in the question bank |
| `discrepancies.json` | errors and doubts in the PSI tables: 71 conflicts and notes with evidence (2 of the notes are about NASA's catalogue records) (6 of the conflicts rest on a hand-filled test sheet only), every changed value, flag meanings, and 11 published-paper disagreements (`source_disagreements`) |
| `test_sheets.json` | `{notes, rows}`: the 637 hand-filled ACME test sheets of PSI-10 and PSI-159, one row per page (`docs/formats.md`). An AI reading of scans, not checked by a human: show the note with any value |
| `questions.json` | the question bank: question, call, chart, answer |
| `synthesis.json` | key messages, limits, microgravity-vs-1-g comparisons, ranked gaps, lineage, research questions |

Rebuild after any table change: `uv run python -m fif.pipeline.build_catalog`.

One table has no export and no function: `data/processed/spread_steps` (`fif.api.table("spread_steps")`), the 39
BASS-II spread rates by test and flow step. Read the independence caveat in `docs/tests-table.md` ("BASS-II spread
rates") before plotting it: the sample size is 18 tests, not 39 points.

## Functions (`fif/api.py`)

Each returns `{data, chart, sources, notes}`. `chart` is a suggestion, `sources` are citations to show, and
`notes` are caveats that must appear next to the answer. Every source has a `url` anyone can open and a short
English `label` to show with it:

| Source | `url` | `label` |
|---|---|---|
| a PSI file (`accession`, `file`, maybe `locator`) | the investigation's NASA PSI page | `BASS-II (PSI-25): <file name>, p3` |
| a digest citation (`ref` such as `[PSI-25 F3]`) | our digest page of that investigation, at `#findings`, `#limitations` or `#open-questions` | `Our notes: BASS-II (PSI-25) digest, finding 3` |
| our notes (`page`, or `file` for the corrections) | the page on the data server, with the section anchor when known | `Our notes: sensor file formats, <section>` |
| the investigation itself, its dataset DOI | the NASA PSI page, `https://doi.org/<doi>` | `BASS-II (PSI-25): NASA PSI record` |

Our notes are served as HTML at `<server>/docs/<key>`: `methods`, `models`, `formats`, `tests-table`,
`question-bank`, `digest/synthesis`, `digest/<accession>` (e.g. `digest/PSI-25`), `corrections` (the patches of
`data/corrections/tests_patches.json`, anchored by accession and patch id; raw at `corrections.json`); `/docs` lists
them. Headings carry GitHub-style anchors. Links are absolute on `FIF_PUBLIC_URL` (default the live server
`http://www.open-poker.ch:5187`), because the team app reaches this server on an internal address; set it when
running a copy that should link to itself. The scheme is in `fif/notes.py`. From a non-Python backend:
`uv run python -m fif.api relevance '{"scenario": "moon-habitat", "pillar": "detection"}'`.

| Function | Answers |
|---|---|
| `search_investigations(query, pillar, fuel_phase, flight, platform_kind)` | which investigations exist / match a topic / ran in a given setting; each card has `location` |
| `get_investigation(accession, sections)` | everything about one investigation; `location` with `facility_notes` (see below); `publications` lists the record's papers in its order (`title`, `authors`, `doi`, `doi_url`, `status`, `held_file`, `review`), `publication_review` counts them, see below |
| `filter_tests(accession, fuel, fuel_phase, config, x_o2, pressure_kpa, flow_cm_s, extinction_mode, outcome, outcome_action, sheet_out, platform_kind, test_id, sort_by, sheets, ...)` | what was tested and what happened; `sheets=True` attaches the operators' test sheet to PSI-10 and PSI-159 rows; `test_id` (one id or a list, spaces and case ignored; with `accession`) picks single tests; `sort_by` (a column, `-` prefix for descending, rows without a value last) orders the rows before `limit`, for lowest / highest questions |
| `compare(accessions)` | side-by-side: question, fuels, ranges, sensors, findings |
| `coverage(x, y, **filters)` | where data exist and which atmospheres are empty; each reference gives its cell count in total and by fuel phase, and `n_not_fire_tests_in_cell` (SAME-R rows: heated, never burned); its `nearest_test` lists in `not_measured` the columns placed from the investigation's narrow stated range, not measured for that test, and has `fire_test` false when it is a smoke-only test |
| `relevance(scenario, fuel_phase, pillar)` | which investigations matter for a scenario, and how far the data are from it |
| `find_evidence(query, accession)` | passages: reviewed findings and raw document text (keyword search) |
| `insights(topic, accession)` | cross-investigation conclusions, limits, gaps, research questions |
| `timeseries(test_id, channels, test_point, accession)` | sensor traces of one test; reads `data/raw/` (or `$FIF_RAW_ROOT`); `demo/server.py` fetches the missing files from PSI on demand (`docs/formats.md`) |
| `document_text(accession, file, page)` | our extracted text of one PSI file: no `page` lists the pages that have text, a `page` (3, `p3`, `sheet Results`) gives its passages in order with `transcribed`; for reading scanned PDFs. Same redaction as `find_evidence`; `demo/server.py` returns no text for the files it does not show inline |
| `discrepancies(accession, test_id, compact)` | errors and doubts in the original PSI tables: raw-data conflicts, changed values, flag meanings, removed files, notes on NASA's catalogue records, and published papers that disagree with PSI (`source_disagreements`); `compact=True` lists every entry without evidence, quotes and claims |
| `predict(model_id, fuel, **conditions)` | small per-investigation models (`docs/models.md`); no `model_id` lists them, `compact=True` for the short list. `fuel` sets the input that encodes it (`is_heptane` from n-heptane / methanol, `n_carbon` from ethane / propane / n-butane, `iso_dodecane_fraction` 0 from n-dodecane), and `x_co2`, `x_he`, `iso_dodecane_fraction` not given are taken as 0; a note says each value so assumed. The tool description lists every model with its question and inputs (fitted range, unit), built from the cards |

Where each investigation ran: every knowledge record has a hand-checked `location` (in `data/digest/PSI-*.json`,
checked by `check_digest`), returned on each `search_investigations` card and by `get_investigation`:

| Field | Meaning |
|---|---|
| `kind` | `iss` (16), `cygnus_free_flight` (Saffire-I, II, III), `ground_lab` (PSI-142), `computation` (PSI-60, 62, 115, 117); `drop_tower` exists for completeness, no investigation is mainly a drop-tower one |
| `vehicle`, `module` | `ISS`, `Cygnus OA-6`; `Destiny`, `Columbus`, `Pressurized Cargo Module`. Null when no source says |
| `module_note` | when the module rests on a pre-flight document only, comes from another investigation's file, or the sources disagree: which document says what, for which dates (null otherwise). The glovebox (MSG) experiments disagree: SPICE's 2008 safety data package puts the MSG in Columbus for SPICE (2009); the 2010 BASS, BASS-II and SLICE requirements read cabin O2 or pressure "in the Columbus module"; the 2021 BASS-II report puts the MSG in Destiny (2014-2016). SLICE and BASS therefore have no module |
| `facility` | short names (`CIR`, `ACME`, `MDCA`, `FCF`, `MSG`, `SAME hardware`, `Saffire enclosure`, `P-Trak`, `DustTrak`, `Counterflow burner`) |
| `crewed` | true for the ISS (a crewed station; the source quotes crew work where the documents mention it), false for Saffire in Cygnus, null on the ground |
| `expedition` | ISS increments or expedition, as the documents state them, or null |
| `uses_data_from` | the flight investigations a ground or computation study reanalysed or took its conditions from |
| `also` | other settings of the investigation's own work: `drop_tower` for the precursor tests of PSI-10, 22 and 23, `computation` for PSI-142. 1-g comparison tests on the ground are not listed |
| `label` | a short label for a chip or a table cell (`ISS · Destiny · CIR · MDCA`) |
| `source` | where each fact comes from: `psi_record` (`field` of NASA's catalogue record and `quote`), `psi_file` (`file`, `locator`, `quote`, and `accession` when the file is filed under another investigation, e.g. a FLEX paper stored with PSI-23) or `external` (`url`, `quote`) |

When rows of the investigation's test table carry a correction or a doubt (a flag outside the informational ones),
`get_investigation` adds a note: how many of how many rows, the rows per flag code, and that
`discrepancies(accession=...)` lists them; the data are unchanged.

`get_investigation` adds `location.facility_notes`: one plain sentence per facility name (and `Cygnus` for
Saffire), from `data/digest/facilities.json`, whose entries carry their own quoted sources and, under `unsourced`,
what a note says that no quote supports. `identity.platform` stays as free text. `search_investigations` and
`filter_tests` take `platform_kind` (one kind or a list); test rows carry a `platform_kind` column, from their
investigation (no row in the PSI tables is a drop-tower or ground test). NASA's catalogue gives the ISS as the flight
program of Saffire-I and III, which burned in Cygnus: `discrepancies()` lists it (notes D70, D71).

Publications: `get_investigation(...)["data"]["publications"]` is the PSI record's publication list as printed
(whitespace collapsed; `doi` and `doi_url` are null when the record gives no DOI; `publication_dois` stays as before).
`held_file` names the PSI file of the same investigation that is that paper, or null: only when the normalised
title opens page 1 of a non-presentation PDF (first 300 characters) and no other listed publication is named on
that page, so publication lists and reports citing the papers never match. 3 of 352 publications match today.

Publication reviews: each publication carries `review` (`access`, `read_url`, `classification`, `summary`, `items`,
`notes`; format in `docs/formats.md`), or null when `data/publications/<accession>.json` has no entry naming it.
All 352 are reviewed today: 71 read in full, 158 from the abstract only, 123 not reachable. `publication_review`
gives `n_publications`, `n_reviewed` and counts `by_access` and `by_classification` (a paper can have several
classifications). The reviews are an AI model's reading of the papers and their quotes were not checked by script;
the result's `notes` say so. Show a review's `quote` with its `locator` and `read_url`.

Paper against PSI: `discrepancies()` returns `source_disagreements`, one per review item of kind
`contradicts_psi_data` (11 today): `accession`, `kind` (`published_paper_disagrees_with_psi`), `publication`,
`read_url`, `locator`, `quote`, `claim`, `record_path`. They are shown, never applied: the PSI tables keep their
values (decision 005). Label them as a published paper disagreeing with PSI, not as a correction. They concern a
whole investigation, so a call with `test_id` returns none.

For an AI assistant: pass `data/processed/tools.json` as the tool list and route calls through
`fif.tools.call(name, arguments)`. Tell the model to cite the `sources` and repeat the `notes`.

Citation ids: `[PSI-26 F3]` is finding 3 of the PSI-26 record (`L` = limitation, `Q` = open question). Each
finding carries its own sources: a PSI file with page and a verbatim quote, or an external URL/DOI.

Spanish for quotes: `data/translations/quotes_es.json` holds machine translations of digest quotes
(`{"note", "lang", "quotes": {key: {"en", "es"}}}`, key = first 16 hex digits of the SHA-1 of the quote's UTF-8
bytes, `fif.api.quote_key`). `get_investigation`, the `digest` part of `find_evidence` and `insights` add
`quote_es` next to every `quote` that has a translation. The translations are made by an AI model and not
reviewed: show `quote_es` labelled as a machine translation, with the English `quote` (the source) beside it.
The file is read once per process; a missing or unreadable file, or a quote without a key, means no `quote_es`.

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
- The weights are a judgement. Jittering them by 20% keeps FLEX the highest score for a Moon habitat every time,
  but the set of the five highest scores changes in about half the draws: read the scores as tiers, not as an order.
- The ranking is sorted in three tiers, by score within each: investigations with a fuel of the requested phase
  (`phase_match` true), then those on other phases, then the investigations where nothing burned (below). The
  score itself is unchanged, so a row lower in the list can have a higher score. `fuel_phase` enters the score
  through the material component and orders the list; it does not filter it. A droplet or gas-flame investigation
  run at the scenario's atmosphere (FLEX for a Moon habitat, the highest score there) is listed after every
  solid-fuel one, and an `Other phases:` note names the investigations of another phase whose tests are nearer to
  the scenario than any test of the requested phase. Each row says so: `phase_match` is false when the
  investigation has no fuel of that phase, and
  `nearest_test` is always a test of the requested phase, or null. For an investigation without such a test, the
  test its conditions score and distance come from is in `nearest_test_other_phase`. `closest_same_phase_test`
  gives the nearest test of the requested phase over all investigations, with its distance: use it, not the top
  row, to answer "what is the nearest real test for this material". A `Phase:` note is added when the top of
  the ranking has no test of the requested phase (a computation, such as PSI-62 for solids, can lead its tier).
- Not every test row is a fire. SAME and SAME-R (PSI-102, PSI-101) heated samples below their ignition point to
  make smoke, and DAFT (PSI-47) sampled aerosol; their rows are typed like burns in `tests` (`row_kind` test, no
  `ignited` or `outcome`). `NOT_A_FIRE` in `fif/api.py` lists them: their ranking rows and test dicts have
  `fire_test` false and test dicts a `test_kind`, a `Not fire tests:` note names them, and
  `closest_same_phase_test` and `gap` only consider tests where ignition was attempted. They rank below every
  investigation that burned something (SAME-R had the highest score for the ISS cabin, 96.4, from assumed cabin air
  and no fire), except for `pillar="detection"`, where they keep their place by score: smoke from overheated
  material is what they measured. A test dict has `result` when the table says what the burn did:
  the columns that say what the burn did (`ignited`, `outcome`, `extinction_mode`, `burn_time_s`,
  `burn_length_cm`, `spread_rate_mm_s`; only those with a value). When the closest test ignited but no flame spread
  (burn length 0, `no_ignition`), a `Result of the closest` note says so.
- `data.gap` holds the content of the `Gap:` note as fields (accession, acronym, test_id, fuel, fuel_phase,
  x_o2_ambient, pressure_kpa, distance_to_scenario, not_measured, result, condition_ranges), or null when the nearest
  same-phase test is within one scale step. Read it instead of parsing the note text.
- Each ranking row has `platform_kind`. `closest_same_phase_test` and `gap` carry `setting` (`platform_kind`,
  `label`, `note`), and a `Setting:` note repeats it: an ISS rack (CIR) test burned in a sealed chamber of about
  90 L with a controlled atmosphere; a glovebox (MSG) test burned a centimetre-sized sample in a 250 L work volume;
  Saffire burned in the cabin air of a Cygnus cargo module, the only burns in a real spacecraft cabin volume.
  Say how far the result carries with it.
- `relevance` raises `ValueError` for an unknown `scenario`, `fuel_phase` (solid, liquid, gas) or `pillar`. A
  custom scenario (or extra keyword conditions) may only set `x_o2`, `pressure_kpa`, `flow_cm_s`, `gravity_g`
  and `label`, needs at least one of the first three, and each value must be physically possible:
  `x_o2` a mole fraction from 0 to 1, pressure 0 to 10,000 kPa, flow and gravity 0 or more (`CONDITION_LIMITS` in
  `fif/api.py`). Anything else raises `ValueError` naming the accepted keys or the unit
  (`x_o2 is a mole fraction between 0 and 1: 0.34, not 34`), because a percent or a pascal value would otherwise
  rank every investigation hundreds of steps away without a warning. The server returns it as a 400 with that
  `detail`. `filter_tests` and `coverage` refuse an `x_o2` bound outside 0-1 the same way (a range in percent
  matched no row before, which read as "never tested"); pressure and flow bounds are not checked, because a value
  in the wrong unit there can still be a real one.
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
  3.2 steps away; the silicone was ignited but no flame spread (burn length about 0). For the ISS cabin it is
  Saffire-II sample 2-1 (silicone, 21.5% O2, 20 cm/s), 1.0 step away, also without spread; SAME-R Kapton run 51
  is nearer (0.19) but was heated, not burned. With a flow in the scenario (ISS cabin, spacecraft transit) no
  liquid or gas test qualifies: their flow (or O2) is unrecorded or known only as a wide range. A BASS-II PMMA test at 22.2% O2 follows, with a pressure (99 kPa) that is the middle of the
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
  its blends. 85 BASS and BASS-II rows are PMMA by inference from the documents (`fuel_inferred`). A name that
  matches no fuel at all is tried in `FUEL_ALIASES` (`fif/api.py`; cotton, candle, acrylic, polyimide, PTFE, ...,
  each backed by the rows' `fuel_raw` or the records' `fuels_and_samples`) and a note says how it was read; with no
  alias, a note lists the fuel names of the table. `filter_tests` and `coverage` share this.
- A range filter (`x_o2`, `pressure_kpa`, `flow_cm_s`) leaves out the rows with no value in that column: BASS-II,
  Saffire-II and SAME-R have no per-test pressure, so "solids at 95-105 kPa" misses 247 rows. A note counts them
  by investigation; `include_unrecorded=True` keeps them. A result with no row always carries a note saying
  which single filter, left out, would match rows.
- Flags come in two kinds: a correction or a doubt, and a remark on how to read the row (`o2_is_burner_stream`,
  `ramped`, `smoke_point_bracket`, `planned_not_flown`, `flash_only`, `burner_over_limit`). The `filter_tests`
  note counts them separately.
- `cool_flame` is `True` or empty, never `False`.
- Flagged test rows carry `flags` (corrections and doubts); original values are kept in `extra`. Show a badge on
  flagged rows and link it to `discrepancies(test_id=...)`, so users see where the PSI tables are wrong.
- CFI (PSI-39) is not FLEX (PSI-69): CFI's files number its tests FLEX-1206 to FLEX-1431 (it followed FLEX and
  FLEX-2 in the same MDCA apparatus), while FLEX's report numbers its own FLEX-001 to FLEX-280. The tests table
  keeps CFI's number without the prefix (FLEX-1246 is `test_id` 1246). `get_investigation`, `filter_tests` and
  `timeseries` add a note saying so (`NAME_NOTES` in `fif/api.py`), and an ambiguous or unknown name raises an
  error listing the accessions with their acronyms.
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
