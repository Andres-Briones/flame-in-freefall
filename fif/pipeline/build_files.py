"""`files` table: every file listed in the 24 PSI records, downloaded or not.

Run: uv run python -m fif.pipeline.build_files
"""
import json
from pathlib import Path

import pandas as pd

from fif import psi

STATUS = psi.ROOT / "data" / "corrections" / "files_status.json"


def status(on_disk, same_size, dead):
    """on_disk: downloaded and the size PSI lists. size_differs: on disk, but PSI now lists another size (it
    regenerated the file). dead_link: PSI lists the file but its storage link fails. not_downloaded: the rest
    (images, video and raw archives that were never fetched, and files that could not be fetched)."""
    if dead:
        return "dead_link"
    if on_disk:
        return "on_disk" if same_size else "size_differs"
    return "not_downloaded"


def build():
    dead = {tuple(k) for k in json.loads(STATUS.read_text())["dead_link"]}
    rows = []
    for rec in psi.load_records():
        acc = rec["accession"]
        for f in psi.manifest(rec):
            path = psi.local_path(acc, f)
            size = int(float(f.get("file_size") or 0))
            rows.append(
                {
                    "accession": acc,
                    "category": psi.file_category(f),
                    "file_name": f["file_name"],
                    "extension": Path(f["file_name"]).suffix.lower(),
                    "size_bytes": size,
                    "downloaded": path.exists() and path.stat().st_size == size,
                    "status": status(path.exists(), path.exists() and path.stat().st_size == size,
                                     (acc, f["file_name"]) in dead),
                    "local_path": str(path.relative_to(psi.ROOT)),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build()
    psi.write_table(df, "files")
    summary = df.groupby("category").agg(
        files=("file_name", "size"), downloaded=("downloaded", "sum"), gb=("size_bytes", lambda s: round(s.sum() / 1e9, 2))
    )
    print(summary.to_string())
