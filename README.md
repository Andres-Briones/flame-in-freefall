# Flame in Freefall

Data and analysis layer for the NASA Space Apps 2026 challenge "Flame in Freefall": the 24 microgravity combustion
investigations of NASA's Physical Sciences Informatics (PSI) repository, digested so a dashboard (and an AI
assistant inside it) can summarise, rank and interpret them for spacecraft and habitat fire safety.

## Project

- **Challenge**: [Flame in Freefall](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/),
  NASA Space Apps Challenge 2026.
- **Team**: [Zaba Zuput](https://www.spaceappschallenge.org/2026/find-a-team/zaba-zuput/).
- **The app**: Ignis, the team's dashboard and assistant built on this data:
  [sebascs04/flame-in-freefall](https://github.com/sebascs04/flame-in-freefall), live at
  <https://orbita-web-813905724775.us-central1.run.app>.
- **This repository**: the data, models and data server Ignis reads (its `/fuego` path).

## Start here

| You are | Read |
|---|---|
| building the dashboard | [docs/methods.md](docs/methods.md): what to load, the functions, the pitfalls |
| looking for what the data can answer | [docs/question-bank.md](docs/question-bank.md): 33 questions with the call and today's answer |
| interested in the science | [docs/digest/README.md](docs/digest/README.md), [docs/digest/synthesis.md](docs/digest/synthesis.md) |
| an AI agent, or pointing one at the data | `<demo server>/llms.txt` (guide), `/mcp`, `/api/tools`: see "For AI agents" in [demo/README.md](demo/README.md) |
| wanting to see it all on screen | [demo/README.md](demo/README.md): a static capability demo of the dashboard, built from `data/export/` |
| checking the data | [docs/tests-table.md](docs/tests-table.md) (per-test table, flags, corrections), [docs/formats.md](docs/formats.md) (raw files), [docs/models.md](docs/models.md) |
| reading these notes in a browser | `<demo server>/docs` (e.g. `/docs/methods`, `/docs/digest/PSI-25`, `/docs/corrections`): every page of `docs/` and the corrections file as HTML; the `url` of a function's sources points there (base: env `FIF_PUBLIC_URL`) |

## What is in it

- **Knowledge records** (`data/digest/`): one per investigation: question, physics with equations, method,
  findings with quoted sources, limitations, open questions, and where it ran (`location`: ISS rack or glovebox,
  Cygnus free flight, ground lab or computation, with a plain-language glossary of the facility names).
- **Publication reviews** (`data/publications/`): for each of the 352 papers listed in the PSI records, whether it
  could be read, what it adds, confirms or contradicts, with quotes (an AI reading of the papers). Served with
  `get_investigation`; papers that disagree with the PSI data are listed by `discrepancies()`.
- **Tables** (`data/processed/`): investigations, 2,177 test rows (2,059 single tests) on a common schema, the 39
  BASS-II spread rates by flow step (18 tests), the 637 hand-filled ACME test sheets (an AI reading of scans, not
  checked by a human), sensor time-series summaries, document text for search, and a column catalogue.
- **Methods** (`fif/api.py`): 11 functions that each return data, a chart suggestion, sources and caveats.
  Tool specs for an AI assistant are in `data/processed/tools.json`.
- **Static export** (`data/export/`): the same answers pre-computed as JSON, for a front end without a backend.
- **Errors in the original data**: where the raw sensor files contradict NASA's tables, the correction is recorded
  in `data/corrections/tests_patches.json` with its evidence and shown by `discrepancies()`. The original value is
  always kept. Where a published paper disagrees with PSI, `discrepancies()` shows it without changing the tables.

## Run

```
uv run python -m fif.api relevance '{"scenario": "moon-habitat", "fuel_phase": "solid"}'
uv run pytest -q
```

Raw NASA files (`data/raw/`, 7.5 GB, not in git) are needed only to rebuild the tables or to plot full sensor
traces. Fetch them with `scripts/fetch_psi.py` and `scripts/fetch_psi_files.py`; rebuild with
`uv run python -m fif.pipeline.<step>` in the order `build_files`, `build_investigations`, `build_tests`,
`build_test_sheets`, `build_evidence`, `build_timeseries`, `build_models`, `check_digest` (also checks
`data/publications/`), `render_digest`, `build_catalog`.

## Limits to keep in mind

- No PSI experiment was run in partial gravity, and no solid material was burned in an exploration atmosphere
  (30% O2 or more at reduced pressure). Statements about those cases are extrapolations and are labelled as such.
- The whole database was re-verified against the raw files on 2026-11-14 by independent passes; what they found
  wrong was corrected, and every correction of NASA's data is a visible patch or flag, never a silent edit.
- The three predictive models are small. Each headline score comes with the range it takes when the test days are
  resampled (for example AUC 0.89, range 0.51-0.94): show the range, not only the number.
- `test_id` is not unique in `tests` (12 rows share one); `source_file` + `source_row` is the row key.
- AI was used to read the documents and write the digest. Quotes from PSI files are machine-checked against the
  extracted text; quotes from external publications are not independently checked.

## License

Copyright (c) 2026 Andres Briones and the Órbita Chalaca team.

- Code (`fif/`, `demo/`, `scripts/`, `tests/`, `deploy/`, `run.sh`, the Docker and project files): MIT, see `LICENSE`.
- What we wrote that is not code (`docs/`, and in `data/` the processed tables, exports, digests, corrections,
  translations and publication reviews): Creative Commons Attribution 4.0 International, see `LICENSE-DATA`.
  Please credit "Flame in Freefall, Andres Briones and the Órbita Chalaca team" with a link to this repository.
- Not ours to license: the material of NASA's Physical Sciences Informatics (PSI) system that this repository
  quotes, transcribes (`data/transcriptions/`) or tabulates stays NASA's, under NASA's terms; quotes from
  published papers stay under their publishers' terms. We hold summaries, short quotes and links to them.
