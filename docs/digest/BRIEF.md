# Brief for record writers

Work in /workspace/flame-in-freefall. Run Python with `uv run python` (ignore
the VIRTUAL_ENV warning). Do NOT git commit. Create or edit only the
`data/digest/PSI-<n>.json` file(s) you were assigned; put any scratch files in
the scratchpad directory, not in the repo.

1. Read `docs/digest/AUTHORING.md` (rules), `data/digest/_template.json`
   (schema) and `docs/digest/reference.md` (shared atmosphere values).
2. Look at `data/digest/PSI-26.json` (document-rich example) or
   `data/digest/PSI-20.json` (thin example, external sources) for the expected
   depth: detailed method, 5-13 specific findings with numbers, honest
   limitations and gaps.
3. Write the record(s). Sources of facts, in order: the PSI record JSON,
   `data/processed/evidence.parquet` (filter by accession),
   `data/processed/tests.csv` (filter by accession) and the raw experimental
   table, `data/processed/files.csv`, then external sources.
4. Run `uv run python -m fif.pipeline.check_digest PSI-<n>` and fix every
   error and warning it reports for your record(s).

Final message: per record, a short report: number of findings, sections left
null and why, most useful sources, external sources that were unreachable,
and anything in the data that looked wrong. Nothing else.
