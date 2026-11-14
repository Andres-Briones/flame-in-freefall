# Flame in Freefall

Data and analysis layer for the NASA Space Apps 2026 challenge "Flame in Freefall": the 24 microgravity combustion
investigations of NASA's Physical Sciences Informatics (PSI) repository, digested so a dashboard (and an AI
assistant inside it) can summarise, rank and interpret them for spacecraft and habitat fire safety.

## Start here

| You are | Read |
|---|---|
| building the dashboard | [docs/methods.md](docs/methods.md): what to load, the functions, the pitfalls |
| looking for what the data can answer | [docs/question-bank.md](docs/question-bank.md): 33 questions with the call and today's answer |
| interested in the science | [docs/digest/README.md](docs/digest/README.md), [docs/digest/synthesis.md](docs/digest/synthesis.md) |
| an AI agent, or pointing one at the data | `<demo server>/llms.txt` (guide), `/mcp`, `/api/tools`: see "For AI agents" in [demo/README.md](demo/README.md) |
| wanting to see it all on screen | [demo/README.md](demo/README.md): a static capability demo of the dashboard, built from `data/export/` |
| checking the data | [docs/tests-table.md](docs/tests-table.md) (per-test table, flags, corrections), [docs/formats.md](docs/formats.md) (raw files), [docs/models.md](docs/models.md) |

## What is in it

- **Knowledge records** (`data/digest/`): one per investigation: question, physics with equations, method,
  findings with quoted sources, limitations, open questions.
- **Tables** (`data/processed/`): investigations, 2,177 test rows (2,059 single tests) on a common schema, the 39
  BASS-II spread rates by flow step (18 tests), the 637 hand-filled ACME test sheets (an AI reading of scans, not
  checked by a human), sensor time-series summaries, document text for search, and a column catalogue.
- **Methods** (`fif/api.py`): 11 functions that each return data, a chart suggestion, sources and caveats.
  Tool specs for an AI assistant are in `data/processed/tools.json`.
- **Static export** (`data/export/`): the same answers pre-computed as JSON, for a front end without a backend.
- **Errors in the original data**: where the raw sensor files contradict NASA's tables, the correction is recorded
  in `data/corrections/tests_patches.json` with its evidence and shown by `discrepancies()`. The original value is
  always kept.

## Run

```
uv run python -m fif.api relevance '{"scenario": "moon-habitat", "fuel_phase": "solid"}'
uv run pytest -q
```

Raw NASA files (`data/raw/`, 7.5 GB, not in git) are needed only to rebuild the tables or to plot full sensor
traces. Fetch them with `scripts/fetch_psi.py` and `scripts/fetch_psi_files.py`; rebuild with
`uv run python -m fif.pipeline.<step>` in the order `build_files`, `build_investigations`, `build_tests`,
`build_test_sheets`, `build_evidence`, `build_timeseries`, `build_models`, `check_digest`, `render_digest`,
`build_catalog`.

## Limits to keep in mind

- No PSI experiment was run in partial gravity, and no solid material was burned in an exploration atmosphere
  (30% O2 or more at reduced pressure). Statements about those cases are extrapolations and are labelled as such.
- The whole database was re-verified against the raw files on 2026-11-14 by independent passes; what they found
  wrong was corrected, and every correction of NASA's data is a visible patch or flag, never a silent edit.
- The four predictive models are small. Each headline score comes with the range it takes when the test days are
  resampled (for example AUC 0.84, range 0.47-0.87): show the range, not only the number.
- `test_id` is not unique in `tests` (12 rows share one); `source_file` + `source_row` is the row key.
- AI was used to read the documents and write the digest. Quotes from PSI files are machine-checked against the
  extracted text; quotes from external publications are not independently checked.
