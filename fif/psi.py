"""Access to the downloaded PSI records and files."""
import json
import os
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RAW = Path(os.environ.get("FIF_RAW_ROOT") or ROOT / "data" / "raw")
PROCESSED = ROOT / "data" / "processed"
DIGEST = ROOT / "data" / "digest"


def accession_number(acc):
    return int(acc.split("-")[1])


def load_records():
    paths = sorted((RAW / "investigations").glob("PSI-*.json"), key=lambda p: accession_number(p.stem))
    return [json.loads(p.read_text()) for p in paths]


def file_category(entry):
    parts = (entry.get("remote_path") or "").split("/")
    return parts[4] if len(parts) > 4 else "?"


def manifest(record):
    """Current (not removed) files of an investigation record, one entry per file name."""
    seen = {}

    def walk(o, removed=False):
        if isinstance(o, dict):
            if "file_name" in o and not removed:
                seen.setdefault(o["file_name"], o)
            for k, v in o.items():
                walk(v, removed or k == "removed")
        elif isinstance(o, list):
            for v in o:
                walk(v, removed)

    walk(record)
    return list(seen.values())


def local_path(acc, entry):
    return RAW / "files" / acc / file_category(entry) / entry["file_name"]


def raw_file(source_file):
    """A `data/raw/...` path as stored in the tables, resolved under RAW (env FIF_RAW_ROOT moves it)."""
    rel = Path(source_file)
    return RAW / rel.relative_to("data/raw") if rel.parts[:2] == ("data", "raw") else ROOT / rel


def _json_cell(value):
    """Lists and dicts go into the CSV as JSON text (the parquet keeps them nested)."""
    if isinstance(value, np.ndarray):
        value = value.tolist()
    return json.dumps(value, ensure_ascii=False, default=str) if isinstance(value, (list, dict)) else value


def write_table(df, name):
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED / f"{name}.parquet", index=False)
    nested = [c for c in df.columns if df[c].map(lambda v: isinstance(v, (list, dict, np.ndarray))).any()]
    as_text = df.assign(**{c: df[c].map(_json_cell) for c in nested})
    as_text.to_csv(PROCESSED / f"{name}.csv", index=False)
    print(f"{name}: {len(df)} rows, {len(df.columns)} columns")
