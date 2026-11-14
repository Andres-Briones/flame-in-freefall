"""Download PSI investigation files by category (default: everything but Raw Data, ~6 TB).

Usage: python3 scripts/fetch_psi_files.py [--raw-dir DIR] [--ext .csv .txt ...]
           [--acc PSI-26 ...] [--match SUBSTR] [category ...]
Resumable: files already present with the expected size are skipped.
"""
import argparse
import json
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--raw-dir", default="data/raw")
ap.add_argument("--ext", nargs="*", help="only these lowercase extensions")
ap.add_argument("--acc", nargs="*", help="only these accessions")
ap.add_argument("--workers", type=int, default=6)
ap.add_argument("--match", help="only file names containing this substring")
ap.add_argument("categories", nargs="*")
ARGS = ap.parse_args()
RAW = Path(ARGS.raw_dir)
CATEGORIES = set(ARGS.categories) or {
    "Experimental table", "metadata", "Representative Image(s)", "Science Documents",
    "Reports", "Presentations", "Engineering Documents", "Analyzed Data", "Reference Data",
}
BASE = "https://psi.nasa.gov/geode-py/ws/studies"


def manifest(record):
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
    return seen.values()


def download(job):
    acc, cat, name, dest = job
    url = f"{BASE}/{acc}/download?" + urllib.parse.urlencode(
        {"file": name}, quote_via=urllib.parse.quote
    )
    part = dest.with_name(dest.name + ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=300) as r, open(part, "wb") as out:
            while chunk := r.read(1 << 20):
                out.write(chunk)
        part.replace(dest)
        return True
    except Exception as e:
        part.unlink(missing_ok=True)
        print(f"FAIL {acc} {cat} {name}: {e}", flush=True)
        return False


def main():
    jobs = []
    skipped = 0
    for path in sorted((RAW / "investigations").glob("PSI-*.json")):
        rec = json.loads(path.read_text())
        acc = rec["accession"]
        if ARGS.acc and acc not in ARGS.acc:
            continue
        for f in manifest(rec):
            parts = (f.get("remote_path") or "").split("/")
            cat = parts[4] if len(parts) > 4 else "?"
            if cat not in CATEGORIES:
                continue
            if ARGS.ext and Path(f["file_name"]).suffix.lower() not in ARGS.ext:
                continue
            if ARGS.match and ARGS.match not in f["file_name"]:
                continue
            dest = RAW / "files" / acc / cat / f["file_name"]
            size = int(float(f.get("file_size") or 0))
            if dest.exists() and dest.stat().st_size == size:
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            jobs.append((acc, cat, f["file_name"], dest))
    print(f"{len(jobs)} to download, {skipped} already present", flush=True)
    with ThreadPoolExecutor(ARGS.workers) as pool:
        results = list(pool.map(download, jobs))
    print(f"done ok={sum(results)} skipped={skipped} failed={len(results) - sum(results)}", flush=True)


if __name__ == "__main__":
    main()
