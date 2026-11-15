"""Check the publication reviews in data/publications against the PSI records' publication lists.

Each file is a list with one entry per publication of the record, in the record's order. Run on its own or as part
of check_digest: uv run python -m fif.pipeline.check_publications [PSI-26 ...]
"""
import json
import sys

from fif import api, psi

ENTRY_KEYS = {"title", "doi", "access", "read_url", "classification", "summary", "items", "notes"}
ITEM_KEYS = {"kind", "claim", "quote", "locator", "record_path"}
UNQUOTED_KINDS = {"out_of_scope", "unreadable"}


def issue(path, message):
    return {"level": "error", "path": path, "message": message}


def item_issues(item, path):
    if not isinstance(item, dict):
        return [issue(path, "item is not an object")]
    out = [issue(path, f"missing key '{k}'") for k in sorted(ITEM_KEYS - set(item))]
    out += [issue(path, f"unexpected key '{k}'") for k in sorted(set(item) - ITEM_KEYS)]
    if item.get("kind") not in api.PUBLICATION_KINDS:
        out.append(issue(path, f"kind {item.get('kind')!r} is not one of {list(api.PUBLICATION_KINDS)}"))
    elif item["kind"] not in UNQUOTED_KINDS:
        out += [issue(path, f"{item['kind']} item has no {k}") for k in ("quote", "locator")
                if not isinstance(item.get(k), str) or not item[k].strip()]
    return out


def entry_issues(entry, pub, path):
    if not isinstance(entry, dict):
        return [issue(path, "entry is not an object")]
    out = [issue(path, f"missing key '{k}'") for k in sorted(ENTRY_KEYS - set(entry))]
    out += [issue(path, f"unexpected key '{k}'") for k in sorted(set(entry) - ENTRY_KEYS)]
    if not api.same_publication(pub, entry):
        out.append(issue(path, f"is {entry.get('title')!r}, the record has {pub['title']!r} here"))
    elif entry.get("doi") and (entry["doi"] or "").lower() != (pub["doi"] or "").lower():
        out.append(issue(path, f"doi {entry['doi']!r} is not the record's {pub['doi']!r} (a DOI found elsewhere goes in notes)"))
    if entry.get("access") not in api.PUBLICATION_ACCESS:
        out.append(issue(path, f"access {entry.get('access')!r} is not one of {list(api.PUBLICATION_ACCESS)}"))
    classes = entry.get("classification")
    if not isinstance(classes, list) or not classes:
        out.append(issue(path, "classification is not a non-empty list"))
    else:
        out += [issue(path, f"classification {c!r} is not one of {list(api.PUBLICATION_KINDS)}")
                for c in classes if c not in api.PUBLICATION_KINDS]
    items = entry.get("items")
    if not isinstance(items, list):
        out.append(issue(path, "items is not a list"))
    else:
        for i, item in enumerate(items):
            out += item_issues(item, f"{path}.items[{i}]")
    return out


def check(acc, entries):
    """Issues of one investigation's review list against its record's publications."""
    pubs = api.get_investigation(acc, sections=["publications"])["data"]["publications"]
    if not isinstance(entries, list):
        return [issue("", "file is not a list")]
    out = []
    if len(entries) != len(pubs):
        out.append(issue("", f"{len(entries)} entries for {len(pubs)} publications in the record"))
    for i, (entry, pub) in enumerate(zip(entries, pubs)):
        out += entry_issues(entry, pub, f"[{i}]")
    return out


def main(argv):
    failed = False
    for acc in argv or list(api.records()):
        path = api.PUBLICATIONS / f"{acc}.json"
        try:
            issues = check(acc, json.loads(path.read_text()))
        except FileNotFoundError:
            issues = [issue("", f"no file {path.relative_to(psi.ROOT)}")]
        except json.JSONDecodeError as e:
            issues = [issue("", f"invalid JSON: {e}")]
        print(f"{acc} publications: {len(issues)} errors")
        for i in issues:
            print(f"  ERROR   {i['path'] or '<root>'}: {i['message']}")
        failed |= bool(issues)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
