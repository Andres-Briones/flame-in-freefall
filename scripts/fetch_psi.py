"""Download PSI combustion-science investigation records (metadata + file manifests).

Usage: python3 scripts/fetch_psi.py [out_dir]
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://psi.nasa.gov/geode-py/ws/repo"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    (OUT / "investigations").mkdir(parents=True, exist_ok=True)
    q = urllib.parse.urlencode(
        {"ffield": "Research Area", "fvalue": "combustion science", "size": 200}
    )
    search = get(f"{BASE}/search?{q}")
    (OUT / "search_combustion.json").write_text(json.dumps(search, indent=1))
    hits = search["hits"]["hits"]
    print(f"{len(hits)} investigations")
    for h in hits:
        acc = h["_source"]["Accession"]
        rec = get(f"{BASE}/investigations/{acc}")
        (OUT / "investigations" / f"{acc}.json").write_text(json.dumps(rec, indent=1))
        print(acc, "ok")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
