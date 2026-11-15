"""Check knowledge records in data/digest against the template, the evidence text and
the PSI records, and the publication reviews in data/publications (check_publications).

Run: uv run python -m fif.pipeline.check_digest [PSI-26 ...]
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from functools import cache

import pandas as pd

from fif import psi
from fif.pipeline import check_publications

TEMPLATE = psi.DIGEST / "_template.json"
REFERENCE_MD = psi.ROOT / "docs" / "digest" / "reference.md"
IGNORED_KEYS = {"_about", "_source_format"}
REQUIRED_FIELDS = {
    "psi_record": ["field"],
    "psi_file": ["file", "locator", "quote"],
    "psi_table": ["file", "sheet", "row", "value"],
    "table": ["table", "note"],
    "external": ["url"],
    "reference": ["id"],
    "background": [],
}
MUST_HAVE_SOURCES = re.compile(r"^(findings\[\d+\]|question|fire_safety\.relevance)$")
MAX_QUOTE_CHARS = 350
PUNCTUATION = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
    "―": "-", "−": "-", "­": None,
})


def normalize(text):
    text = unicodedata.normalize("NFKC", text or "").translate(PUNCTUATION)
    return re.sub(r"\s+", " ", text).strip()


def quote_in(quote, chunks):
    """True if the quote occurs in the chunks read as one text (chunks were split at spaces or mid-word)."""
    q = normalize(quote)
    parts = [normalize(c) for c in chunks]
    return bool(q) and any(q in sep.join(parts) for sep in (" ", ""))


def issue(level, path, message):
    return {"level": level, "path": path, "message": message}


def is_placeholder(text):
    return len(text) >= 25 and " " in text or any(c in text for c in "|…<") or text == "PSI-0"


def enum_options(text):
    return text.split("|") if "|" in text and not text.startswith("<") else None


def structure_issues(record, template, path=""):
    out = []
    if isinstance(template, dict):
        if not isinstance(record, dict):
            return [issue("error", path, f"expected an object, got {type(record).__name__}")]
        keys, expected = set(record) - IGNORED_KEYS, set(template) - IGNORED_KEYS
        for k in sorted(expected - keys):
            out.append(issue("error", path, f"missing key '{k}'"))
        for k in sorted(keys - expected):
            out.append(issue("error", path, f"unexpected key '{k}'"))
        for k in sorted(keys & expected):
            if k != "sources":
                out += structure_issues(record[k], template[k], f"{path}.{k}" if path else k)
    elif isinstance(template, list):
        if not isinstance(record, list):
            return [issue("error", path, f"expected a list, got {type(record).__name__}")]
        if template:
            for i, item in enumerate(record):
                out += structure_issues(item, template[0], f"{path}[{i}]")
    elif isinstance(template, str) and isinstance(record, str):
        options = enum_options(template)
        if record == template and is_placeholder(template):
            out.append(issue("error", path, f"template placeholder left in: {template[:60]!r}"))
        elif options and record not in options:
            out.append(issue("warning", path, f"{record!r} is not one of {options}"))
    return out


def walk_sources(o, path=""):
    """(path, source) for every item of a `sources` list and every other object with a `type`."""
    if isinstance(o, dict):
        if "type" in o:
            yield path, o
        for k, v in o.items():
            sub = f"{path}.{k}" if path else k
            if k == "sources" and isinstance(v, list):
                for i, s in enumerate(v):
                    if not isinstance(s, dict):
                        yield f"{sub}[{i}]", s
                    else:
                        yield from walk_sources(s, f"{sub}[{i}]")
            else:
                yield from walk_sources(v, sub)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_sources(v, f"{path}[{i}]")


def walk_sourced(o, path=""):
    """(path, object) for every object that carries a `sources` list."""
    if isinstance(o, dict):
        if "sources" in o:
            yield path, o
        for k, v in o.items():
            if k != "sources":
                yield from walk_sourced(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_sourced(v, f"{path}[{i}]")


def has_content(obj):
    return any(v not in (None, "", [], {}) for k, v in obj.items() if k != "sources")


def coverage_issues(record):
    out = []
    for path, obj in walk_sourced(record):
        if obj.get("sources") or not has_content(obj):
            continue
        if MUST_HAVE_SOURCES.match(path):
            out.append(issue("error", path, "claim has no source"))
        else:
            out.append(issue("warning", path, "text has no source"))
    for path in ("question", "fire_safety.relevance"):
        obj = record
        for k in path.split("."):
            obj = obj.get(k) if isinstance(obj, dict) else None
        if isinstance(obj, dict) and not has_content(obj):
            out.append(issue("warning", path, "empty"))
    habitat = (record.get("fire_safety") or {}).get("habitat_conditions")
    if isinstance(habitat, dict) and has_content(habitat) and not any(
            isinstance(s, dict) and s.get("type") == "reference" for s in habitat.get("sources") or []):
        out.append(issue("warning", "fire_safety.habitat_conditions", "no reference source (see docs/digest/reference.md)"))
    return out


class Context:
    """Lookups shared by all records; each loaded on first use."""

    @cache
    def evidence(self, acc):
        e = pd.read_parquet(psi.PROCESSED / "evidence.parquet", columns=["accession", "file_name", "locator", "chunk", "text"])
        e = e[e.accession == acc].sort_values(["file_name", "locator", "chunk"])
        out = {}
        for (f, loc), g in e.groupby(["file_name", "locator"], sort=False):
            out.setdefault(f, {})[loc] = g.text.fillna("").tolist()
        return out

    @cache
    def files(self, acc):
        f = pd.read_csv(psi.PROCESSED / "files.csv", usecols=["accession", "file_name"])
        return set(f.loc[f.accession == acc, "file_name"])

    @cache
    def raw_record(self, acc):
        path = psi.RAW / "investigations" / f"{acc}.json"
        return json.loads(path.read_text()) if path.exists() else None

    @cache
    def reference_ids(self):
        return set(re.findall(r"^\|\s*`([^`]+)`\s*\|", REFERENCE_MD.read_text(), re.M))

    @cache
    def processed_tables(self):
        return {p.stem for p in psi.PROCESSED.glob("*.parquet")}


def psi_file_issue(path, src, acc, ctx):
    texts = ctx.evidence(acc).get(src["file"])
    if texts is None:
        where = "has no extracted text" if src["file"] in ctx.files(acc) else "is not a file of this investigation"
        return issue("error", path, f"{src['file']} {where}")
    if quote_in(src["quote"], texts.get(src["locator"], [])):
        return None
    found = [loc for loc, chunks in texts.items() if quote_in(src["quote"], chunks)]
    if found:
        return issue("warning", path, f"quote is at locator {', '.join(found)}, not {src['locator']!r} in {src['file']}")
    return issue("error", path, f"quote not found in {src['file']}: {src['quote'][:80]!r}")


def source_issues(acc, record, ctx):
    out, counts = [], Counter()
    for path, src in walk_sources(record):
        if not isinstance(src, dict):
            out.append(issue("error", path, f"source is not an object: {src!r}"))
            continue
        kind = src.get("type")
        counts[kind] += 1
        if kind not in REQUIRED_FIELDS:
            out.append(issue("error", path, f"unknown source type {kind!r}"))
            continue
        missing = [f for f in REQUIRED_FIELDS[kind] if not src.get(f)]
        if missing:
            out.append(issue("error", path, f"{kind} source missing {', '.join(missing)}"))
            continue
        out += [i for i in typed_source_issues(kind, path, src, acc, ctx) if i]
    return out, counts


def typed_source_issues(kind, path, src, acc, ctx):
    if src.get("quote") and len(src["quote"]) > MAX_QUOTE_CHARS:
        yield issue("warning", path, f"quote is {len(src['quote'])} chars (keep under ~300)")
    if kind == "psi_file":
        yield psi_file_issue(path, src, acc, ctx)
    elif kind == "psi_record":
        raw = ctx.raw_record(acc)
        field = re.split(r"[.\[]", src["field"])[0]
        if raw is None:
            yield issue("error", path, f"no PSI record for {acc}")
        elif field not in raw:
            yield issue("error", path, f"PSI record has no field {src['field']!r}")
        elif raw[field] in (None, "", [], {}):
            yield issue("warning", path, f"PSI record field {src['field']!r} is empty")
    elif kind == "reference" and src["id"] not in ctx.reference_ids():
        yield issue("error", path, f"unknown reference id {src['id']!r}")
    elif kind == "psi_table" and src["file"] not in ctx.files(acc):
        yield issue("error", path, f"{src['file']} is not in files.csv for {acc}")
    elif kind == "table" and src["table"] not in ctx.processed_tables():
        yield issue("warning", path, f"table {src['table']!r} is not a processed table; spreadsheet rows should be psi_table")
    elif kind == "external" and not src.get("quote"):
        yield issue("warning", path, "external source has no quote")


def check_record(acc, record, template, ctx):
    issues = structure_issues(record, template)
    if record.get("accession") != acc:
        issues.append(issue("error", "accession", f"{record.get('accession')!r} does not match file name {acc}"))
    found, counts = source_issues(acc, record, ctx)
    issues += found + coverage_issues(record)
    findings = record.get("findings")
    return {
        "accession": acc,
        "issues": issues,
        "source_counts": counts,
        "n_findings": len(findings) if isinstance(findings, list) else 0,
    }


def record_paths(accessions):
    if accessions:
        return [psi.DIGEST / f"{a}.json" for a in accessions]
    paths = psi.DIGEST.glob("PSI-*.json")
    return sorted(paths, key=lambda p: psi.accession_number(p.stem))


def report(result):
    errors = [i for i in result["issues"] if i["level"] == "error"]
    warnings = [i for i in result["issues"] if i["level"] == "warning"]
    counts = ", ".join(f"{k}={v}" for k, v in sorted(result["source_counts"].items(), key=str))
    print(f"{result['accession']}: {len(errors)} errors, {len(warnings)} warnings, "
          f"{result['n_findings']} findings, sources: {counts or 'none'}")
    for i in errors + warnings:
        print(f"  {i['level'].upper():7} {i['path'] or '<root>'}: {i['message']}")


def main(argv):
    template = json.loads(TEMPLATE.read_text())
    ctx = Context()
    failed = False
    for path in record_paths(argv):
        if not path.exists():
            print(f"{path.stem}: no such record")
            failed = True
            continue
        try:
            record = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"{path.stem}: invalid JSON: {e}")
            failed = True
            continue
        result = check_record(path.stem, record, template, ctx)
        report(result)
        failed |= any(i["level"] == "error" for i in result["issues"])
    failed |= bool(check_publications.main([p.stem for p in record_paths(argv)]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
