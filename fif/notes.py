"""Our notes as public pages: which files are published, their address on the data server, their section anchors,
and the `url` and `label` every source of a `fif.api` result carries.

A page's key is its path under docs/ without `.md` (`methods`, `models`, `digest/synthesis`); a digest page of one
investigation is keyed by its accession (`digest/PSI-25` for docs/digest/PSI-25-bass-ii.md). The corrections file
is the page `corrections`. Links are absolute, on FIF_PUBLIC_URL (default: the live data server), because the team
app reaches this server on an internal address its users cannot open.
"""
import os
import re
from functools import lru_cache

from fif import psi

PUBLIC_URL = (os.environ.get("FIF_PUBLIC_URL") or "http://www.open-poker.ch:5187").rstrip("/")
DOCS = psi.ROOT / "docs"
CORRECTIONS = psi.ROOT / "data" / "corrections" / "tests_patches.json"
CORRECTIONS_KEY = "corrections"
# Working briefs, not notes: an agent prompt with local paths, and a review of the teammates' private repository.
NOT_PUBLISHED = frozenset({"digest/BRIEF", "review-game-claims"})
TITLES = {
    "methods": "how to use the data and functions",
    "formats": "sensor file formats",
    "models": "outcome models",
    "tests-table": "the tests table, its flags and corrections",
    "question-bank": "questions the data answer",
    "digest/README": "the investigation digest",
    "digest/synthesis": "what the 24 investigations say together",
    "digest/reference": "reference atmospheres and values",
    "digest/AUTHORING": "how the digest records are written",
    CORRECTIONS_KEY: "corrections to NASA's test tables",
}


@lru_cache(maxsize=None)
def pages():
    """Page key -> Markdown file, for every published note."""
    out = {}
    for path in sorted([*DOCS.glob("*.md"), *(DOCS / "digest").glob("*.md")]):
        key = path.relative_to(DOCS).with_suffix("").as_posix()
        match = re.match(r"digest/(PSI-\d+)(?:-|$)", key)
        key = f"digest/{match.group(1)}" if match else key
        if key not in NOT_PUBLISHED:
            out[key] = path
    return out


def page_key(path):
    """Key of a published note from a repository path such as docs/digest/PSI-25-bass-ii.md (None if unpublished)."""
    if str(path).replace("\\", "/").lstrip("./") == "data/corrections/tests_patches.json":
        return CORRECTIONS_KEY
    target = (psi.ROOT / path).resolve()
    return next((k for k, p in pages().items() if p.resolve() == target), None)


def slug(text):
    """GitHub-style anchor of a heading's text: lower case, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[^\w\- ]", "", text.replace("`", "").replace("*", "").strip().lower()).replace(" ", "-")


def plain(text):
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text).replace("`", "").replace("*", "").strip()


@lru_cache(maxsize=None)
def headings(key):
    """[(level, text, anchor)] of a page's headings outside code blocks, anchors made unique as GitHub does."""
    if key not in pages():
        return []
    out, seen, fence = [], {}, None
    for line in pages()[key].read_text().splitlines():
        marker = re.match(r"\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            fence = None if fence and marker.group(1).startswith(fence) else fence or marker.group(1)
            continue
        match = None if fence else re.match(r"\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if match:
            anchor = slug(match.group(2))
            n = seen.get(anchor, 0)
            seen[anchor] = n + 1
            out.append((len(match.group(1)), plain(match.group(2)), f"{anchor}-{n}" if n else anchor))
    return out


def section(key, pattern):
    """(text, anchor) of the first heading of a page that matches a regular expression, or None."""
    return next(((text, anchor) for _, text, anchor in headings(key) if re.search(pattern, text)), None)


def page_url(key, anchor=None):
    return f"{PUBLIC_URL}/docs/{key}" + (f"#{anchor}" if anchor else "")


def title(key):
    if key in TITLES:
        return TITLES[key]
    found = headings(key)
    return found[0][1] if found else key
