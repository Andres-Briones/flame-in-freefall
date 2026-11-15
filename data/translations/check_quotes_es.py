"""Check data/translations/quotes_es.json against the digest.

Run from the repo root: python3 -I data/translations/check_quotes_es.py
Exit 1 if any check fails. Finding quotes must be fully covered; the other
categories are reported, and anything they do contain is checked the same way.
"""
import collections
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIGEST = os.path.join(ROOT, "data", "digest")
PATH = os.path.join(ROOT, "data", "translations", "quotes_es.json")

NUMBER = re.compile(r"\d+(?:\.\d+)?")
WORD = re.compile(r"[A-Za-zÀ-ÿ]+")
# Names and symbols of 4+ letters that are not English words, so a quote made
# only of these, numbers and units may be identical in both languages.
NOT_WORDS = {
    "Saffire", "Tmax", "xbase", "xtip",
    "burnerTemperatureLimitC", "burnerTemperatureLimitDurationSecs",
}


def key(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def quotes_in(node):
    if isinstance(node, dict):
        for name, value in node.items():
            if name == "quote" and isinstance(value, str):
                yield value
            else:
                yield from quotes_in(value)
    elif isinstance(node, list):
        for value in node:
            yield from quotes_in(value)


def has_translatable_words(text):
    return any(
        len(w) >= 4 and not w.isupper() and w not in NOT_WORDS
        for w in WORD.findall(text)
    )


def load_digest():
    records = {}
    for path in sorted(glob.glob(os.path.join(DIGEST, "PSI-*.json"))):
        with open(path, encoding="utf-8") as fh:
            record = json.load(fh)
        records[record["accession"]] = record
    cats = collections.OrderedDict()
    cats["findings"] = set()
    cats["synthesis key messages (cited sections)"] = set()
    cats["limitations"] = set()
    cats["open_questions"] = set()
    cats["equations"] = set()
    everything = set()
    for record in records.values():
        cats["findings"].update(quotes_in(record.get("findings")))
        cats["limitations"].update(quotes_in(record.get("limitations")))
        cats["open_questions"].update(quotes_in(record.get("open_questions")))
        cats["equations"].update(quotes_in((record.get("physics") or {}).get("equations")))
        everything.update(quotes_in(record))
    with open(os.path.join(DIGEST, "synthesis.json"), encoding="utf-8") as fh:
        synthesis = json.load(fh)
    everything.update(quotes_in(synthesis))
    for message in synthesis.get("key_messages", []):
        cats["synthesis key messages (cited sections)"].update(quotes_in(message))
        for cite in message.get("citations", []):
            section = records.get(cite.get("accession"), {}).get(cite.get("section"))
            index = cite.get("index")
            if index is not None and isinstance(section, list) and 0 < index <= len(section):
                section = section[index - 1]
            cats["synthesis key messages (cited sections)"].update(quotes_in(section))
    cats["other record sections"] = everything - set().union(*cats.values())
    return cats, everything


def main():
    errors = []
    with open(PATH, encoding="utf-8") as fh:
        raw = fh.read()
    data = json.loads(raw)
    quotes = data.get("quotes", {})
    if data.get("lang") != "es" or not data.get("note"):
        errors.append("header: 'lang' must be 'es' and 'note' must be present")
    if raw != json.dumps(data, ensure_ascii=False, indent=1) + "\n":
        errors.append("file is not in canonical form (indent 1, UTF-8, trailing newline)")
    if list(quotes) != sorted(quotes):
        errors.append("keys are not sorted")

    cats, everything = load_digest()
    identical = 0
    for k, entry in quotes.items():
        en, es = entry.get("en"), entry.get("es")
        if not isinstance(en, str) or not isinstance(es, str) or set(entry) != {"en", "es"}:
            errors.append(f"{k}: entry must be exactly {{'en': str, 'es': str}}")
            continue
        if key(en) != k:
            errors.append(f"{k}: key is not the sha1 prefix of 'en' ({key(en)})")
        if en not in everything:
            errors.append(f"{k}: orphan, 'en' is not a quote in the digest")
        if not es.strip():
            errors.append(f"{k}: empty translation")
        if collections.Counter(NUMBER.findall(en)) != collections.Counter(NUMBER.findall(es)):
            errors.append(f"{k}: number tokens differ\n    en: {en}\n    es: {es}")
        if es == en:
            identical += 1
            if has_translatable_words(en):
                errors.append(f"{k}: translation identical to the English: {en}")

    print(f"{len(quotes)} entries, {identical} identical to the English (numbers, symbols and names only)")
    for name, wanted in cats.items():
        have = sum(1 for q in wanted if key(q) in quotes)
        print(f"  {name}: {have}/{len(wanted)} distinct quotes translated")
    missing = [q for q in cats["findings"] if key(q) not in quotes]
    for q in sorted(missing)[:20]:
        errors.append(f"finding quote without translation ({key(q)}): {q[:100]}")
    if len(missing) > 20:
        errors.append(f"... and {len(missing) - 20} more finding quotes without translation")

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(" -", e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
