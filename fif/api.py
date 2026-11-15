"""Methods a dashboard (or its AI) calls to answer questions about the PSI combustion data.

Every function returns a JSON-serialisable dict:
    data     the answer (list of rows or a dict)
    chart    a suggested chart ({"type", "x", "y", ...}) or None
    sources  where the answer comes from (digest findings, PSI files, table rows)
    notes    caveats the reader must see next to the answer

Command line: uv run python -m fif.api <function> '<json kwargs>'
"""
import hashlib
import html
import json
import math
import re
import sys
from functools import lru_cache

import numpy as np
import pandas as pd

from fif import psi

REFERENCE_ATMOSPHERES = {
    "earth-sea-level": {"x_o2": 0.209, "pressure_kpa": 101.3, "label": "Earth sea level / ISS cabin"},
    "moon-habitat": {"x_o2": 0.30, "pressure_kpa": 70.3, "label": "Moon habitat (30% O2 or more, 10.2 psi or less)"},
    "exploration-8psi": {"x_o2": 0.34, "pressure_kpa": 56.5, "label": "Exploration atmosphere (34% O2, 8.2 psi)"},
    "spacesuit": {"x_o2": 1.0, "pressure_kpa": 29.6, "label": "Spacesuit (100% O2, 4.3 psi)"},
}
SCENARIOS = {
    "iss-cabin": {**REFERENCE_ATMOSPHERES["earth-sea-level"], "gravity_g": 0.0, "flow_cm_s": 10.0},
    "moon-habitat": {**REFERENCE_ATMOSPHERES["moon-habitat"], "gravity_g": 0.165},
    "mars-habitat": {**REFERENCE_ATMOSPHERES["exploration-8psi"], "gravity_g": 0.38},
    "pressurised-rover": {**REFERENCE_ATMOSPHERES["exploration-8psi"], "gravity_g": 0.165},
    "spacecraft-transit": {**REFERENCE_ATMOSPHERES["exploration-8psi"], "gravity_g": 0.0, "flow_cm_s": 10.0},
}
PILLARS = ("prevention", "detection", "suppression")

# One scale unit per dimension: a difference this large counts as "one step away" from a tested condition.
SCALES = {"x_o2": 0.03, "pressure_kpa": 15.0, "flow_cm_s": 10.0}
TEST_COLUMN = {"x_o2": "x_o2_ambient", "pressure_kpa": "pressure_kpa", "flow_cm_s": "flow_cm_s"}
COVERAGE_PARAMETER = {
    "oxygen fraction": "x_o2", "oxygen fraction (ambient)": "x_o2", "pressure": "pressure_kpa",
    "airflow speed": "flow_cm_s", "airflow speed (coflow)": "flow_cm_s", "airflow speed (relative)": "flow_cm_s",
}
# Flags that tell how to read a row; every other flag marks a correction or a doubt.
INFORMATIONAL_FLAGS = {"o2_is_burner_stream", "ramped", "smoke_point_bracket", "planned_not_flown", "flash_only",
                       "burner_over_limit"}
WEIGHTS = {"conditions": 0.40, "material": 0.25, "pillar": 0.20, "evidence": 0.15}
GRAVITY_WEIGHT = 0.10
UNKNOWN_STEPS = 2.0  # a condition nobody recorded counts as two steps away
HELD_TITLE_CHARS = 300  # a paper's title opens its first page (after a header such as "Title of Document:")
ENVELOPE_DISCOUNT = 0.8  # inside a stated range is weaker than on a tested point
# How far a result on one fuel phase carries to a hazard of another phase. A judgement, not a measurement:
# gas-burner and droplet flames share the gas-phase physics of a burning solid but not its pyrolysis.
TRANSFER = {
    "solid": {"solid": 1.0, "gas": 0.4, "liquid": 0.4, "aerosol": 0.3},
    "liquid": {"liquid": 1.0, "gas": 0.5, "solid": 0.4, "aerosol": 0.3},
    "gas": {"gas": 1.0, "liquid": 0.5, "solid": 0.4, "aerosol": 0.2},
}
# Run in ISS or Cygnus cabin air, with O2 or pressure not logged per test in the files read. Only missing
# dimensions are filled, with the nominal cabin atmosphere.
CABIN_AIR = {"PSI-47", "PSI-98", "PSI-99", "PSI-100", "PSI-101", "PSI-102", "PSI-106", "PSI-107"}
CABIN_RANGE = {"x_o2": (0.205, 0.215), "pressure_kpa": (98.0, 103.0)}
# Investigations whose test rows are not fires: nothing was ignited or meant to be. Their rows are typed like burns
# in `tests` (row_kind "test", no ignited/outcome value), so relevance labels them and never offers one as the
# closest test to a fire scenario. Sources: the PSI-101 and PSI-102 records ("heated to temperatures below the
# ignition point") and PSI-47 (aerosol sampling).
NOT_A_FIRE = {
    "PSI-101": "heated below ignition to make smoke; nothing burned",
    "PSI-102": "heated below ignition to make smoke; nothing burned",
    "PSI-47": "aerosol sampling; nothing burned",
}
# Test columns that say what a burn did, copied into relevance's test dicts when they have a value.
RESULT_COLUMNS = ("ignited", "outcome", "extinction_mode", "burn_time_s", "burn_length_cm", "spread_rate_mm_s")
PHASE_WITHOUT_TESTS = {"PSI-60": "gas", "PSI-62": "solid", "PSI-115": "aerosol", "PSI-117": "liquid", "PSI-142": "liquid"}
PLATFORM_KINDS = ("iss", "cygnus_free_flight", "drop_tower", "ground_lab", "computation")
# How far a result from each setting carries to a fire in a real cabin, for `relevance`. Only what the records and
# the facility glossary (data/digest/facilities.json) support.
SETTING_NOTES = {
    "CIR": "ISS rack test: burned in the sealed CIR combustion chamber (about 90 L) with an atmosphere set for the "
           "test, so O2, pressure and diluent were controlled and the flame was small; it does not show how a fire "
           "grows in an open cabin or what it does to the cabin air.",
    "MSG": "ISS glovebox test: a small sample or gas jet in a flow duct inside the sealed MSG work volume (about "
           "250 L), in cabin air or cabin air diluted with nitrogen; samples and flames are centimetre-sized, not "
           "cabin-scale.",
    "cygnus_free_flight": "Saffire: burned in a flow duct inside an uncrewed Cygnus cargo module in free flight, in "
                          "the module's cabin air; the three Saffire flights are the only burns in a real spacecraft "
                          "cabin volume, and Saffire-I and III (a 0.4 x 0.94 m fabric sheet) the only large ones.",
    "ground_lab": "Ground laboratory test in normal gravity, not a microgravity test.",
    "computation": "A computer model, not a test.",
}


def _clean(value):
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    return None if value is pd.NA or value is pd.NaT else value


def _rows(df):
    return _clean(df.astype(object).where(df.notna(), None).to_dict("records"))


def _result(data, chart=None, sources=(), notes=()):
    return {"data": _clean(data), "chart": chart, "sources": _clean(list(sources)), "notes": list(notes)}


@lru_cache(maxsize=None)
def table(name):
    return pd.read_parquet(psi.PROCESSED / f"{name}.parquet")


@lru_cache(maxsize=None)
def records():
    paths = sorted(psi.DIGEST.glob("PSI-*.json"), key=lambda p: psi.accession_number(p.stem))
    return {p.stem: json.loads(p.read_text()) for p in paths}


@lru_cache(maxsize=None)
def synthesis():
    return json.loads((psi.DIGEST / "synthesis.json").read_text())


QUOTES_ES = psi.ROOT / "data" / "translations" / "quotes_es.json"


@lru_cache(maxsize=None)
def _quotes_es():
    """Spanish machine translations of digest quotes, keyed by quote_key; empty when the file is absent or unreadable."""
    try:
        quotes = json.loads(QUOTES_ES.read_text())["quotes"]
        return {k: v["es"] for k, v in quotes.items() if isinstance(v, dict) and v.get("es")}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return {}


def quote_key(quote):
    return hashlib.sha1(quote.encode("utf-8")).hexdigest()[:16]


def _with_quote_es(value):
    """A copy of `value` where every source dict with a `quote` that has a translation also carries `quote_es`."""
    if isinstance(value, list):
        return [_with_quote_es(v) for v in value]
    if not isinstance(value, dict):
        return value
    out = {k: _with_quote_es(v) for k, v in value.items()}
    es = _quotes_es().get(quote_key(value["quote"])) if isinstance(value.get("quote"), str) else None
    if es:
        out["quote_es"] = es
    return out


def _accession(acc):
    text = str(acc).strip()
    if text.upper().replace(" ", "") in records():
        return text.upper().replace(" ", "")
    if text.isdigit():
        return _accession(f"PSI-{text}")
    names = {a: (r["identity"]["acronym"] or "").lower() for a, r in records().items()}
    match = [a for a, n in names.items() if n == text.lower()] or [a for a, n in names.items() if text.lower() in n]
    if len(match) != 1:
        raise KeyError(f"unknown or ambiguous investigation {acc!r}; known: {', '.join(records())}")
    return match[0]


def _phases(acc):
    t = table("tests")
    phases = sorted(set(t.loc[t["accession"] == acc, "fuel_phase"].dropna()))
    return phases or [PHASE_WITHOUT_TESTS.get(acc, "gas")]


def _is_flight(rec):
    return rec["identity"].get("project_type") != "Ground Investigation"


def _finding_ref(acc, i):
    return f"[{acc} F{i}]"


def _card(acc):
    rec = records()[acc]
    t = table("tests")
    psi_row = table("investigations").set_index("accession").loc[acc]
    doi = psi_row["doi"] if isinstance(psi_row["doi"], str) and psi_row["doi"] else None
    return {
        "accession": acc, "acronym": rec["identity"]["acronym"], "title": rec["identity"]["title"],
        "one_line": rec["one_line"], "pillars": rec["fire_safety"]["pillars"], "fuel_phases": _phases(acc),
        "flight": _is_flight(rec), "n_test_rows": int((t["accession"] == acc).sum()),
        "n_findings": len(rec["findings"]), "page": _page_name(acc) and f"docs/digest/{_page_name(acc)}",
        "doi": doi, "doi_url": f"https://doi.org/{doi}" if doi else None, "psi_url": psi_row["source_url"],
        "location": rec["location"],
    }


@lru_cache(maxsize=None)
def facility_glossary():
    """Facility and vehicle name -> {note, sources, unsourced?} (data/digest/facilities.json)."""
    return json.loads((psi.DIGEST / "facilities.json").read_text())["facilities"]


def _facility_notes(location):
    names = [*location["facility"], *(["Cygnus"] if location["kind"] == "cygnus_free_flight" else [])]
    return {name: facility_glossary()[name]["note"] for name in names}


def _setting(acc):
    """Where the investigation ran and a one-line note on how far its result carries to a real cabin."""
    loc = records()[acc]["location"]
    key = loc["kind"] if loc["kind"] != "iss" else next((f for f in loc["facility"] if f in SETTING_NOTES), None)
    return {"platform_kind": loc["kind"], "label": loc["label"], "note": SETTING_NOTES.get(key)}


def _page_name(acc):
    digest = psi.ROOT / "docs" / "digest"
    pages = sorted(digest.glob(f"{acc}-*.md")) or sorted(digest.glob(f"{acc}.md"))  # no acronym: PSI-60.md
    return pages[0].name if pages else None


# --- text search --------------------------------------------------------------------------------------

def _digest_passages():
    out = []
    for acc, rec in records().items():
        out.append({"accession": acc, "kind": "summary", "ref": f"[{acc}]", "text": f"{rec['one_line']} {rec['summary']}"})
        for i, f in enumerate(rec["findings"], 1):
            out.append({"accession": acc, "kind": "finding", "ref": _finding_ref(acc, i), "text": f["claim"],
                        "confidence": f.get("confidence"), "sources": f.get("sources", [])})
        for i, lim in enumerate(rec["limitations"], 1):
            out.append({"accession": acc, "kind": "limitation", "ref": f"[{acc} L{i}]", "text": lim["text"]})
        for i, q in enumerate(rec["open_questions"], 1):
            out.append({"accession": acc, "kind": "open_question", "ref": f"[{acc} Q{i}]",
                        "text": q if isinstance(q, str) else q.get("text", "")})
    return out


@lru_cache(maxsize=None)
def _index(corpus):
    from sklearn.feature_extraction.text import TfidfVectorizer

    if corpus == "digest":
        passages = _digest_passages()
    else:
        ev = table("evidence")
        passages = ev[["accession", "file_name", "locator", "chunk", "text", "transcribed"]].to_dict("records")
    vec = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=1 if corpus == "digest" else 2, stop_words="english")
    return passages, vec, vec.fit_transform(p["text"] for p in passages)


def _search(corpus, query, accession, k):
    passages, vec, matrix = _index(corpus)
    scores = (matrix @ vec.transform([query]).T).toarray().ravel()
    order = [i for i in scores.argsort()[::-1] if scores[i] > 0 and (accession is None or passages[i]["accession"] == accession)]
    return [{**passages[i], "score": round(float(scores[i]), 3)} for i in order[:k]]


def find_evidence(query, accession=None, k=8, raw=True):
    """Passages that answer a free-text question: reviewed digest findings first, then raw document text."""
    acc = _accession(accession) if accession else None
    digest = _search("digest", query, acc, k)
    documents = _search("evidence", query, acc, k) if raw else []
    for d in documents:
        d["text"] = d["text"][:700]
    sources = [{"ref": d["ref"], "accession": d["accession"]} for d in digest]
    sources += [{"accession": d["accession"], "file": d["file_name"], "locator": d["locator"],
                 "transcribed": d["transcribed"]} for d in documents]
    notes = ["`digest` passages are reviewed claims with their own sources; `documents` are unreviewed extracts "
             "from PSI files and may contain extraction errors."]
    if any(d["transcribed"] for d in documents):
        notes.append(TRANSCRIBED_NOTE)
    return _result({"digest": _with_quote_es(digest), "documents": documents}, None, sources, notes)


TRANSCRIBED_NOTE = ("Documents with `transcribed: true` are an AI model's reading of a scanned page that has no text "
                    "layer, not the document's own text; numbers and names may be misread. Check them in the original file.")


def _page_order(locator, first):
    match = re.fullmatch(r"p(\d+)", locator)
    return (0, int(match.group(1))) if match else (1, first)


def document_text(accession, file, page=None):
    """Our extracted text of one PSI file, page by page, so a scanned PDF can be read and copied: without `page`, the
    pages (locators) that have text; with `page` (a number or a locator such as p3 or "sheet Results"), that page's
    passages in order."""
    try:
        acc = _accession(accession)
    except KeyError as e:
        raise ValueError(e.args[0]) from None
    files = table("evidence_files")
    status = files.loc[(files["accession"] == acc) & (files["file_name"] == file), "status"]
    if status.empty:
        raise ValueError(f"{file!r} is not a file of {acc}")
    ev = table("evidence")
    ev = ev[(ev["accession"] == acc) & (ev["file_name"] == file)]
    first = {loc: i for i, loc in reversed(list(enumerate(ev["locator"])))}
    pages = sorted(first, key=lambda loc: _page_order(loc, first[loc]))
    data = {"accession": acc, "file": file, "status": status.iloc[0], "pages": pages}
    notes = ["The text is an unreviewed extract from the PSI file and may contain extraction errors."]
    if page is None:
        data["transcribed_pages"] = sorted(set(ev.loc[ev["transcribed"], "locator"]), key=lambda loc: _page_order(loc, first[loc]))
        transcribed = bool(data["transcribed_pages"])
    else:
        locator = f"p{page}" if isinstance(page, int) or str(page).isdigit() else str(page)
        rows = ev[ev["locator"] == locator].sort_values("chunk")
        data["page"] = locator
        data["passages"] = [{"text": r.text, "locator": r.locator, "transcribed": bool(r.transcribed)} for r in rows.itertuples()]
        transcribed = any(p["transcribed"] for p in data["passages"])
    if not pages:
        notes.append(f"There is no text for this file (extraction status: {data['status']}).")
    if transcribed:
        notes.append(TRANSCRIBED_NOTE)
    sources = [{"accession": acc, "file": file, "locator": data.get("page"), "transcribed": transcribed}]
    return _result(data, None, sources, notes)


def _kinds(platform_kind):
    kinds = [platform_kind] if isinstance(platform_kind, str) else list(platform_kind)
    unknown = sorted(set(kinds) - set(PLATFORM_KINDS))
    if unknown:
        raise ValueError(f"platform_kind must be among {list(PLATFORM_KINDS)}, not {unknown}")
    return kinds


def search_investigations(query=None, pillar=None, fuel_phase=None, flight=None, platform_kind=None, limit=24):
    """Investigation cards, filtered and (with a query) ranked by text match over their digest record.
    `platform_kind` (one kind or a list) keeps the investigations whose `location.kind` is one of them."""
    kinds = _kinds(platform_kind) if platform_kind else None
    cards = {acc: _card(acc) for acc in records()}
    if query:
        score = {}
        for hit in _search("digest", query, None, 200):
            score[hit["accession"]] = score.get(hit["accession"], 0) + hit["score"]
        cards = {a: {**c, "match": round(score[a], 3)} for a, c in cards.items() if a in score}
    out = [c for c in cards.values()
           if (pillar is None or pillar in c["pillars"])
           and (fuel_phase is None or fuel_phase in c["fuel_phases"])
           and (flight is None or c["flight"] == flight)
           and (kinds is None or c["location"]["kind"] in kinds)]
    out.sort(key=lambda c: (-c.get("match", 0), psi.accession_number(c["accession"])))
    return _result(out[:limit], None, [{"ref": f"[{c['accession']}]", "page": c["page"]} for c in out[:limit]])


def _norm(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


@lru_cache(maxsize=None)
def _first_pages(acc):
    """Normalised text of page 1 of each PDF we hold for the investigation. Slides of a talk are not the paper."""
    ev = table("evidence")
    ev = ev[(ev.accession == acc) & (ev.locator == "p1") & (ev.category != "Presentations")]
    return {f: _norm(" ".join(g.sort_values("chunk")["text"])) for f, g in ev.groupby("file_name")}


def _held_file(acc, pub, pubs):
    """The PSI file that is this publication: its title opens page 1 and no other listed publication is named there.

    A publication list or a report that cites the papers names several of them on page 1, so it never matches.
    """
    title = _norm(pub["title"])
    if len(title.split()) < 4:
        return None
    others = [k for p in pubs if _norm(p["title"]) != title
              for k in (_norm(p["title"]), _norm(p["doi"])) if k and len(k.split()) >= 2]
    for name, page in sorted(_first_pages(acc).items()):
        if title in page[:HELD_TITLE_CHARS] and not any(k in page for k in others):
            return name
    return None


PUBLICATIONS = psi.ROOT / "data" / "publications"
PUBLICATION_ACCESS = ("full_text", "abstract", "none")
PUBLICATION_KINDS = ("new_finding", "confirms", "contradicts_psi_data", "contradicts_record", "out_of_scope", "unreadable")
REVIEW_FIELDS = ("access", "read_url", "classification", "summary", "items", "notes")
REVIEW_NOTE = ("Each publication's `review` is an AI model's reading of the paper (full text, abstract or nothing "
               "reachable, see `access`); its quotes were not checked against the papers by script.")
PAPER_DISAGREEMENT_NOTE = (
    "`source_disagreements` are places where a published paper by the investigators disagrees with the PSI data or "
    "documents (a paper quote against PSI). They are shown, not applied: the PSI tables stay as they are. Read by an "
    "AI model from the paper; open `read_url` and check the quote before relying on one.")


def same_publication(pub, entry):
    """True if a review entry names this publication of the record: same DOI, or the same title (the record's may
    carry trailing text such as a year or an affiliation)."""
    if pub.get("doi") and entry.get("doi") and pub["doi"].lower() == entry["doi"].lower():
        return True
    record, review = (_norm(html.unescape(p.get("title") or "")) for p in (pub, entry))
    return bool(review) and (record == review or len(review.split()) >= 4 and record.startswith(review + " "))


@lru_cache(maxsize=None)
def publication_reviews(acc):
    """The reviewed publication list of an investigation (data/publications/<acc>.json), or [] when there is none."""
    path = PUBLICATIONS / f"{acc}.json"
    return json.loads(path.read_text()) if path.exists() else []


def _review(acc, i, pub):
    reviews = publication_reviews(acc)
    if i >= len(reviews) or not same_publication(pub, reviews[i]):
        return None
    return {k: reviews[i][k] for k in REVIEW_FIELDS}


def _publications(acc, pubs):
    pubs = [dict(p) for p in pubs]
    return [{**p, "doi_url": f"https://doi.org/{p['doi']}" if p["doi"] else None, "held_file": _held_file(acc, p, pubs),
             "review": _review(acc, i, p)} for i, p in enumerate(pubs)]


def _publication_review(pubs):
    reviews = [p["review"] for p in pubs if p["review"]]
    return {"n_publications": len(pubs), "n_reviewed": len(reviews),
            "by_access": {a: sum(r["access"] == a for r in reviews) for a in PUBLICATION_ACCESS},
            "by_classification": {k: sum(k in r["classification"] for r in reviews) for k in PUBLICATION_KINDS}}


def get_investigation(accession, sections=None):
    """The full knowledge record of one investigation (or only the named sections)."""
    acc = _accession(accession)
    rec = records()[acc]
    data = _with_quote_es({k: v for k, v in rec.items() if sections is None or k in sections or k == "accession"})
    data["card"] = _card(acc)
    if "location" in data:
        data["location"] = {**data["location"], "facility_notes": _facility_notes(data["location"])}
    api = table("investigations").set_index("accession").loc[acc]
    if sections is None or "publication_dois" in sections:
        dois = api["publication_dois"]
        data["publication_dois"] = [d.strip() for d in dois.split(";") if d.strip()] if isinstance(dois, str) else []
    notes = []
    if sections is None or "publications" in sections:
        data["publications"] = _publications(acc, api["publications"])
        data["publication_review"] = _publication_review(data["publications"])
        if data["publication_review"]["n_reviewed"]:
            notes.append(REVIEW_NOTE)
    return _result(data, None, [{"ref": f"[{acc}]", "page": data["card"]["page"], "url": api["source_url"], "doi": api["doi"]}],
                   notes)


# --- tests table --------------------------------------------------------------------------------------

def _between(series, bounds):
    lo, hi = bounds if isinstance(bounds, (list, tuple)) else (bounds, bounds)
    mask = series.notna()
    if lo is not None:
        mask &= series >= lo
    if hi is not None:
        mask &= series <= hi
    return mask


SHEET_NOTE = ("`test_sheet` values are an AI model's reading of a hand-filled scanned form (the ACME Science Test "
              "Sheets of PSI-10 and PSI-159), not checked by a human: ids, numbers and ticks may be misread. Check "
              "them in the scan (file and page are given) before relying on one.")
SHEET_FIELDS = ["file_name", "page", "ignited", "flame", "out", "flame_behavior_written", "flame_behavior_note", "comments"]


@lru_cache(maxsize=None)
def _sheets():
    """The test-sheet page of each `tests` row that has one, keyed by (accession, test id as in `tests`)."""
    s = table("test_sheets")
    s = s[s["in_tests"]]
    return {(row["accession"], row["tests_test_id"]): row for row in _rows(s)}


def _sheet_keys(df):
    return pd.Series([key in _sheets() for key in zip(df["accession"], df["test_id"])], index=df.index, dtype=bool)


def _select_tests(accession=None, fuel=None, fuel_phase=None, config=None, x_o2=None, pressure_kpa=None,
                  flow_cm_s=None, extinction_mode=None, outcome=None, outcome_action=None, sheet_out=None,
                  platform_kind=None, row_kind="test", exclude_flags=None):
    t = table("tests")
    mask = pd.Series(True, index=t.index)
    if sheet_out:
        wanted = [sheet_out] if isinstance(sheet_out, str) else sheet_out
        mask &= pd.Series([_sheets().get(key, {}).get("out") in wanted for key in zip(t["accession"], t["test_id"])],
                          index=t.index)
    if accession:
        accs = [accession] if isinstance(accession, str) else accession
        mask &= t["accession"].isin([_accession(a) for a in accs])
    if platform_kind:
        mask &= t["platform_kind"].isin(_kinds(platform_kind))
    for column, value in (("fuel_phase", fuel_phase), ("extinction_mode", extinction_mode), ("outcome", outcome),
                          ("outcome_action", outcome_action), ("row_kind", row_kind)):
        if value:
            mask &= t[column].isin([value] if isinstance(value, str) else value)
    if fuel:
        # "ethane" must not match "methane"; "heptane" matches "n-heptane" and the blend "n-heptane/isooctane".
        mask &= t["fuel"].fillna("").str.contains(rf"(?<![a-z]){re.escape(fuel.strip())}(?![a-z])", case=False, regex=True)
    if config:
        mask &= t["config"].fillna("").str.contains(config, case=False, regex=False)
    for key, bounds in (("x_o2", x_o2), ("pressure_kpa", pressure_kpa), ("flow_cm_s", flow_cm_s)):
        if bounds is not None:
            mask &= _between(t[TEST_COLUMN[key]], bounds)
    if exclude_flags:
        codes = t["flags"].fillna("").str.split(";")
        mask &= ~codes.apply(lambda c: bool(set(c) & set(exclude_flags)))
    return t[mask]


def _test_sources(df):
    return [{"accession": a, "file": f, "rows": int(n)} for (a, f), n in df.groupby(["accession", "source_file"]).size().items()]


def filter_tests(columns=None, limit=500, sheets=False, **filters):
    """Rows of the per-test table. Ranges are [min, max] with None for open ends; `fuel` matches a whole fuel name
    (ethane does not return methane; heptane returns n-heptane and its blends), `config` is a substring match; row_kind defaults to "test" (pass None for all kinds).
    `sheets=True` attaches to each PSI-10 / PSI-159 row its hand-filled test sheet as `test_sheet` (ignited, hot or
    cool flame, how the flame ended, operator comments); `sheet_out` keeps the rows whose sheet ticks that ending."""
    df = _select_tests(**filters)
    notes = []
    if len(df) > limit:
        notes.append(f"{len(df)} rows match; the first {limit} are returned.")
    codes = df["flags"].dropna().str.split(";").apply(set)
    if len(codes):
        n_info = int(codes.apply(lambda c: c <= INFORMATIONAL_FLAGS).sum())
        notes.append(f"{len(codes)} of {len(df)} rows carry a flag: {len(codes) - n_info} a correction or a doubt, "
                     f"{n_info} only a remark on how to read the row; see docs/tests-table.md.")
    keys = df[["accession", "test_id"]].apply(tuple, axis=1)
    if keys.duplicated().any():
        notes.append(f"{int(keys.duplicated(keep=False).sum())} rows share a test id with another row of the same "
                     "investigation (flag duplicate_id); a row is identified by source_file and source_row.")
    shown = df.head(limit)
    if columns:
        shown = shown[[c for c in dict.fromkeys(["accession", "test_id", *columns]) if c in shown.columns]]
    else:
        shown = shown.dropna(axis=1, how="all").drop(columns=["x_o2"], errors="ignore")
    numeric = [c for c in ("x_o2_ambient", "pressure_kpa", "flow_cm_s") if c in shown.columns and shown[c].notna().any()]
    chart = {"type": "scatter", "x": numeric[0], "y": numeric[1], "color": "fuel"} if len(numeric) > 1 else None
    rows, sources = _rows(shown), _test_sources(df)
    n_sheets = int(_sheet_keys(df).sum())
    if n_sheets and (sheets or filters.get("sheet_out")):
        pages = {}
        for row in rows:
            sheet = _sheets().get((row["accession"], row["test_id"]))
            if sheet:
                row["test_sheet"] = {k: sheet[k] for k in SHEET_FIELDS if sheet[k] is not None}
                pages.setdefault((sheet["accession"], sheet["file_name"]), []).append(f"p{sheet['page']}")
        sources += [{"accession": a, "file": f, "locator": ", ".join(p), "transcribed": True} for (a, f), p in pages.items()]
        notes.append(SHEET_NOTE)
    elif n_sheets:
        notes.append(f"{n_sheets} of {len(df)} rows have a hand-filled test sheet (ignition, how the flame ended, operator "
                     "comments; an AI reading of a scan, not checked by a human): pass sheets=true to attach it.")
    return _result({"n_matching": len(df), "rows": rows}, chart, sources, notes)


@lru_cache(maxsize=None)
def _envelopes():
    """Per investigation and dimension: (min, max, origin) of the ambient conditions it covered."""
    env = {acc: {} for acc in records()}
    for p in synthesis()["parameter_coverage"]:
        key = COVERAGE_PARAMETER.get(p["parameter"])
        if key and p["min"] is not None and p["max"] is not None:
            env[p["accession"]][key] = (float(p["min"]), float(p["max"]), "digest")
    t = table("tests")
    t = t[t["row_kind"] != "planned"]
    for acc, group in t.groupby("accession"):
        for key, column in TEST_COLUMN.items():
            lo = group[column].min() if key != "x_o2" else pd.concat([group[column], group["x_o2_min"]]).min()
            hi = group[column].max() if key != "x_o2" else pd.concat([group[column], group["x_o2_max"]]).max()
            if pd.notna(lo):
                # single-value rows miss the ramped tests, so a wider range stated in the documents is kept
                dlo, dhi, _ = env[acc].get(key, (lo, hi, None))
                wider = dlo < lo - 1e-9 or dhi > hi + 1e-9
                env[acc][key] = (float(min(lo, dlo)), float(max(hi, dhi)), "tests table and digest" if wider else "tests table")
    for acc in CABIN_AIR:
        for key, (lo, hi) in CABIN_RANGE.items():
            env[acc].setdefault(key, (lo, hi, "assumed cabin air"))
    return env


def compare(accessions, findings=3):
    """Side-by-side summary of several investigations: question, fuels, tested ranges, sensors, key findings."""
    out, sources = [], []
    t = table("tests")
    for acc in map(_accession, accessions):
        rec, env = records()[acc], _envelopes()[acc]
        rows = t[(t["accession"] == acc) & (t["row_kind"] != "planned")]
        ranked = sorted(enumerate(rec["findings"], 1), key=lambda f: f[1].get("confidence") != "high")[:findings]
        out.append({
            **_card(acc), "question": rec["question"]["text"],
            "fuels": sorted(rows["fuel"].dropna().unique())[:12],
            "ranges": {k: {"min": v[0], "max": v[1], "from": v[2]} for k, v in env.items()},
            "measurements": [m["quantity"] for m in rec["measurements"]],
            "key_findings": [{"ref": _finding_ref(acc, i), "claim": f["claim"], "confidence": f.get("confidence")} for i, f in ranked],
            "limitations": [lim["text"] for lim in rec["limitations"][:3]],
        })
        sources.append({"ref": f"[{acc}]", "page": out[-1]["page"]})
    chart = {"type": "range-bars", "x": "ranges.x_o2", "y": "acronym", "facet": ["x_o2", "pressure_kpa", "flow_cm_s"]}
    notes = ["Ranges are envelopes: an investigation did not test every combination inside them. Oxygen is the "
             "ambient atmosphere; burner-stream oxygen of inverse flames is excluded."]
    return _result(out, chart, sources, notes)


def _filled(df, acc_env):
    """Tests with missing O2 / pressure filled from the investigation's envelope when that envelope is narrow."""
    df = df.copy()
    df["filled"] = ""
    for key, column in (("x_o2", "x_o2_ambient"), ("pressure_kpa", "pressure_kpa")):
        for acc, idx in df[df[column].isna()].groupby("accession").groups.items():
            lo, hi, _ = acc_env.get(acc, {}).get(key, (None, None, None))
            if lo is not None and hi - lo <= 0.1 * hi:
                df.loc[idx, column] = (lo + hi) / 2
                df.loc[idx, "filled"] += column + ";"
    return df


def _bin(values, step):
    """Index of the bin [i*step, (i+1)*step) a value falls in; 0.30 // 0.02 is 14 in floating point, not 15."""
    return np.floor(np.asarray(values, dtype=float) / step + 1e-9).astype(int)


def coverage(x="x_o2_ambient", y="pressure_kpa", x_step=0.02, y_step=10.0, **filters):
    """Where PSI has tests in a 2-D parameter plane, and which reference atmospheres fall on empty ground."""
    df = _filled(_select_tests(**filters), _envelopes())
    have = df.dropna(subset=[x, y])
    grid = have.assign(ix=_bin(have[x], x_step), iy=_bin(have[y], y_step))
    cells = []
    for (ix, iy), g in grid.groupby(["ix", "iy"]):
        cells.append({
            "x_min": round(ix * x_step, 6), "x_max": round((ix + 1) * x_step, 6),
            "y_min": round(iy * y_step, 6), "y_max": round((iy + 1) * y_step, 6), "n": len(g),
            "by_phase": g["fuel_phase"].value_counts().to_dict(), "accessions": sorted(g["accession"].unique()),
            "n_from_stated_range": int((g["filled"] != "").sum()),
        })
    references = []
    if (x, y) == ("x_o2_ambient", "pressure_kpa"):
        for rid, ref in REFERENCE_ATMOSPHERES.items():
            d = ((have[x] - ref["x_o2"]) / SCALES["x_o2"]) ** 2 + ((have[y] - ref["pressure_kpa"]) / SCALES["pressure_kpa"]) ** 2
            near = have.loc[d.idxmin()] if len(d) else None
            in_cell = grid[(grid["ix"] == _bin(ref["x_o2"], x_step)) & (grid["iy"] == _bin(ref["pressure_kpa"], y_step))]
            references.append({
                "id": rid, **ref, "n_tests_in_cell": len(in_cell),
                "n_tests_in_cell_by_phase": {p: int((in_cell["fuel_phase"] == p).sum()) for p in ("solid", "liquid", "gas")},
                "n_from_stated_range": int((in_cell["filled"] != "").sum()),
                "n_not_fire_tests_in_cell": int(in_cell["accession"].isin(NOT_A_FIRE).sum()),
                "nearest_test": None if near is None else {
                    "accession": near["accession"], "test_id": near["test_id"], "fuel": near["fuel"],
                    "fuel_phase": near["fuel_phase"], x: near[x], y: near[y],
                    "not_measured": [c for c in near["filled"].split(";") if c],
                    "fire_test": near["accession"] not in NOT_A_FIRE,
                    **({"test_kind": NOT_A_FIRE[near["accession"]]} if near["accession"] in NOT_A_FIRE else {})},
            })
    notes = [f"{len(have)} of {len(df)} selected rows have both {x} and {y}; the rest are not on the map."]
    if "row_kind" not in filters:
        notes.append("Only rows of kind `test` are selected (one row per test); test-day summaries, condition sets "
                     "and planned tests are left out. Pass row_kind to change that.")
    n_filled = int((have["filled"] != "").sum())
    if n_filled:
        notes.append(f"{n_filled} rows had no per-test value and use their investigation's (narrow) stated range, "
                     "e.g. cabin pressure about 1 atm; `n_from_stated_range` counts them in each cell and `not_measured` "
                     "names the columns of a reference's `nearest_test` filled that way (the value is the middle of "
                     "the range, not a reading of that test). filter_tests returns these cells empty, as in the source.")
    if any(r["n_not_fire_tests_in_cell"] or (r["nearest_test"] and not r["nearest_test"]["fire_test"])
           for r in references):
        notes.append(f"Not every test is a fire: {', '.join(sorted(NOT_A_FIRE))} heated samples to make smoke or "
                     "sampled aerosol, and nothing burned. `n_not_fire_tests_in_cell` counts their rows in a "
                     "reference's cell, and a reference's `nearest_test` has `fire_test` false when it is one.")
    if references and not (filters.get("fuel_phase") or filters.get("fuel")):
        notes.append("`n_tests_in_cell` counts every fuel (gas flames, droplets, solids). Before saying a material was "
                     "tested at a reference atmosphere, read `n_tests_in_cell_by_phase` or filter by fuel_phase or fuel.")
    chart = {"type": "heatmap", "x": x, "y": y, "value": "n", "facet": "by_phase", "overlay": "references"}
    return _result({"cells": cells, "references": references, "n_on_map": len(have)}, chart, _test_sources(have), notes)


# --- scenario relevance ---------------------------------------------------------------------------------

def _narrow(lo, hi):
    return hi - lo <= 0.1 * hi


def _distance(row, env, scenario, unknown_steps):
    """Scaled distance from a test (or an envelope where the test has no value) to the scenario."""
    parts, unknown, ranged = {}, [], []
    for key, scale in SCALES.items():
        target = scenario.get(key)
        if target is None:
            continue
        value = row.get(TEST_COLUMN[key]) if row is not None else None
        if value is not None and not pd.isna(value):
            parts[key] = abs(value - target) / scale
        elif key in env:
            lo, hi, _ = env[key]
            parts[key] = max(lo - target, target - hi, 0) / scale
            ranged.append(key)
        else:
            parts[key] = unknown_steps.get(key, UNKNOWN_STEPS)
            unknown.append(key)
    return math.sqrt(sum(v * v for v in parts.values())), parts, unknown, ranged


def _conditions(acc, scenario, fuel_phase, unknown_steps=None):
    env = _envelopes()[acc]
    t = table("tests")
    rows = t[(t["accession"] == acc) & (t["row_kind"] != "planned")]
    if fuel_phase and (rows["fuel_phase"] == fuel_phase).any():
        rows = rows[rows["fuel_phase"] == fuel_phase]
    candidates = rows.to_dict("records") or [None]
    d, parts, unknown, ranged, row = min((_distance(r, env, scenario, unknown_steps or {}) + (r,) for r in candidates), key=lambda c: c[0])
    nearest = None
    if row is not None:
        nearest = {k: row[k] for k in ("test_id", "fuel", "fuel_phase", "x_o2_ambient", "pressure_kpa", "flow_cm_s")}
        nearest["not_measured"] = [c for c in TEST_COLUMN.values() if pd.isna(nearest[c])]
        nearest["fire_test"] = acc not in NOT_A_FIRE
        if acc in NOT_A_FIRE:
            nearest["test_kind"] = NOT_A_FIRE[acc]
        result = {c: _clean(row[c]) for c in RESULT_COLUMNS if not pd.isna(row[c])}
        if result:
            nearest["result"] = result
        for key in ("x_o2", "pressure_kpa"):
            if pd.isna(nearest[TEST_COLUMN[key]]) and key in env and _narrow(*env[key][:2]):
                nearest[TEST_COLUMN[key]] = round((env[key][0] + env[key][1]) / 2, 3)
    ranges = {k: {"min": round(env[k][0], 4), "max": round(env[k][1], 4), "from": env[k][2], "wide": not _narrow(*env[k][:2])} for k in ranged}
    for p in synthesis()["parameter_coverage"]:
        key = COVERAGE_PARAMETER.get(p["parameter"])
        if p["accession"] == acc and key in ranges and "digest" in ranges[key]["from"] and p.get("note"):
            ranges[key]["note"] = p["note"]
    assumed = [k for k in ranged if env[k][2] == "assumed cabin air"]
    wide = any(r["wide"] for r in ranges.values())
    return {"score": math.exp(-d / 2) * (ENVELOPE_DISCOUNT if wide else 1.0), "distance": round(d, 2), "assumed": assumed,
            "per_dimension": {k: round(v, 4) for k, v in parts.items()}, "unknown": unknown,
            "from_range": [k for k in ranged if k not in assumed], "ranges": ranges, "nearest_test": nearest}


def _pillar_score(rec, pillar):
    applied = [p for p in rec["fire_safety"]["pillars"] if p in PILLARS]
    if pillar is None:
        return 1.0 if applied else 0.3
    if pillar not in applied:
        return 0.3
    return 1.0 if applied[0] == pillar else 0.7


def _evidence_score(rec):
    high = sum(f.get("confidence") == "high" for f in rec["findings"])
    return 0.5 * (1.0 if _is_flight(rec) else 0.5) + 0.5 * min(1.0, high / 8)


@lru_cache(maxsize=None)
def _gravity_comparisons():
    """Number of microgravity-vs-1-g comparisons each investigation contributes (the only handle on partial gravity)."""
    counts = {}
    for entry in synthesis()["micro_vs_1g"]:
        for acc in {c["accession"] for c in entry["citations"]}:
            counts[acc] = counts.get(acc, 0) + 1
    return counts


def relevance(scenario="moon-habitat", fuel_phase="solid", pillar=None, top=24, **overrides):
    """Rank the investigations by how much they tell us about a fire-safety scenario.

    scenario: a name in SCENARIOS or a dict with x_o2, pressure_kpa and optionally flow_cm_s, gravity_g.
    fuel_phase: phase of the hazard ("solid" for cables, fabrics and plastics; "liquid"; "gas"). It weights the
        ranking (the material component) and does not filter it: `phase_match` marks the investigations that tested
        that phase, and `nearest_test` is always a test of that phase or None.
    pillar: "prevention", "detection" or "suppression" (None = any).
    """
    if fuel_phase not in TRANSFER:
        raise ValueError(f"fuel_phase must be one of {sorted(TRANSFER)}, not {fuel_phase!r}")
    if pillar is not None and pillar not in PILLARS:
        raise ValueError(f"pillar must be one of {list(PILLARS)} or None, not {pillar!r}")
    if isinstance(scenario, str) and scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {sorted(SCENARIOS)} or a dict of conditions, not {scenario!r}")
    name = scenario if isinstance(scenario, str) else "custom"
    sc = {**(SCENARIOS[scenario] if isinstance(scenario, str) else scenario), **overrides}
    partial_g = 0 < (sc.get("gravity_g") or 0) < 1
    weights = {**WEIGHTS, **({"gravity": GRAVITY_WEIGHT} if partial_g else {})}
    total = sum(weights.values())
    ranked = []
    conditions = {acc: _conditions(acc, sc, fuel_phase) for acc in records()}
    # A condition nobody recorded must not rank above one that was measured far away: it counts as far as the
    # farthest measured investigation on that dimension (and at least UNKNOWN_STEPS).
    farthest = {}
    for cond in conditions.values():
        for key, steps in cond["per_dimension"].items():
            if key not in cond["unknown"]:
                farthest[key] = max(farthest.get(key, UNKNOWN_STEPS), steps)
    for acc, rec in records().items():
        cond = conditions[acc]
        if cond["unknown"]:
            cond = _conditions(acc, sc, fuel_phase, farthest)
        comp = {
            "conditions": cond["score"],
            "material": max(TRANSFER[fuel_phase].get(p, 0.2) for p in _phases(acc)),
            "pillar": _pillar_score(rec, pillar),
            "evidence": _evidence_score(rec),
        }
        if partial_g:
            comp["gravity"] = min(1.0, _gravity_comparisons().get(acc, 0) / 3)
        score = 100 * sum(weights[k] * comp[k] for k in weights) / total
        findings = [(i, f) for i, f in enumerate(rec["findings"], 1) if f.get("confidence") == "high"][:2]
        nearest = cond["nearest_test"]
        same = nearest is not None and nearest["fuel_phase"] == fuel_phase
        ranked.append({
            "accession": acc, "acronym": rec["identity"]["acronym"], "score": round(score, 1),
            "components": {k: round(v, 2) for k, v in comp.items()},
            "distance_to_scenario": cond["distance"], "distance_per_dimension": {k: round(v, 2) for k, v in cond["per_dimension"].items()},
            "platform_kind": rec["location"]["kind"],
            "phase_match": fuel_phase in _phases(acc), "nearest_test": nearest if same else None,
            "nearest_test_other_phase": None if same else nearest, "conditions_unknown": cond["unknown"],
            "conditions_from_range": cond["from_range"], "conditions_assumed_cabin_air": cond["assumed"],
            "condition_ranges": cond["ranges"],
            "pillars": rec["fire_safety"]["pillars"], "fuel_phases": _phases(acc), "one_line": rec["one_line"],
            "key_findings": [{"ref": _finding_ref(acc, i), "claim": f["claim"]} for i, f in findings],
        })
    ranked.sort(key=lambda r: -r["score"])
    same_phase = [r for r in ranked if fuel_phase in r["fuel_phases"] and r["nearest_test"]
                  and r["nearest_test"]["fire_test"] and not r["conditions_unknown"]
                  and not any(c["wide"] for c in r["condition_ranges"].values())]
    closest = min(same_phase, key=lambda r: r["distance_to_scenario"], default=None)
    notes = [
        "Score = weighted mean of four components in [0, 1]: conditions (closeness of the nearest test to the "
        "scenario's O2, pressure and flow), material (fuel-phase transfer), pillar and evidence strength. "
        "Weights and scales are in fif/api.py and docs/methods.md; they are a judgement, shown so it can be argued with.",
        "A distance of 1 means one scale step away: 3 points of O2, 15 kPa or 10 cm/s. A condition that was not "
        "recorded counts as far away as the farthest investigation that did record it (at least 2 steps); "
        "cabin-air experiments without logged O2 or pressure are placed at the nominal cabin atmosphere "
        "(listed in conditions_assumed_cabin_air).",
        "A condition with no per-test value is read from the investigation's range (conditions_from_range or "
        "conditions_assumed_cabin_air; range and origin in condition_ranges); a wide range lowers the conditions "
        "score by 20%. A value shown for a column in a test's `not_measured` is the middle of a narrow range, not a "
        "reading of that test.",
    ]
    if partial_g:
        notes.append(f"No PSI combustion test was run at partial gravity ({sc['gravity_g']} g). The gravity component "
                     "only rewards investigations that compare microgravity with 1 g, which brackets partial gravity.")
    notes.append(f"fuel_phase weights the ranking, it does not filter it: an investigation on another fuel phase keeps "
                 f"its place with a lower material component and `phase_match` false. `nearest_test` is always a "
                 f"{fuel_phase}-fuel test (null when the investigation ran none); the test of another phase that its "
                 f"conditions score and distance come from is in `nearest_test_other_phase`.")
    not_fire = [f"{r['accession']} ({r['nearest_test']['test_kind']})" for r in ranked
                if r["nearest_test"] and not r["nearest_test"]["fire_test"]]
    if not_fire:
        notes.append(f"Not fire tests: {'; '.join(not_fire)} (`fire_test` false). They keep their rank, but "
                     f"`closest_same_phase_test` and `gap` only use tests where ignition was attempted.")
    first = next((i for i, r in enumerate(ranked) if r["nearest_test"]), None)
    if first:
        r = ranked[first]
        notes.append(f"Phase: the top {first} of this ranking ({', '.join(x['accession'] for x in ranked[:first])}) "
                     f"ran no {fuel_phase}-fuel test; they rank on conditions tested with another fuel phase. The "
                     f"best-ranked investigation with a {fuel_phase}-fuel test is {r['accession']}, rank {first + 1}, "
                     f"{r['distance_to_scenario']} scale steps from the scenario.")
    elif first is None:
        notes.append(f"Phase: no investigation has a {fuel_phase}-fuel test in the table.")
    gap = None
    if closest and closest["distance_to_scenario"] > 1:
        n = closest["nearest_test"]
        # The same statement as the "Gap:" note below, as fields, so a client does not have to parse the sentence.
        gap = {"accession": closest["accession"], "acronym": closest["acronym"], "test_id": n["test_id"],
               "fuel": n["fuel"], "fuel_phase": fuel_phase, "x_o2_ambient": n["x_o2_ambient"],
               "pressure_kpa": n["pressure_kpa"], "distance_to_scenario": closest["distance_to_scenario"],
               "not_measured": n["not_measured"], "result": n.get("result", {}),
               "condition_ranges": closest["condition_ranges"], "setting": _setting(closest["accession"])}

        def origin(key):
            c = closest["condition_ranges"].get(key)
            if not c:
                return ""
            return " assumed cabin air" if c["from"] == "assumed cabin air" else f" not measured, middle of the range {c['min']:g}-{c['max']:g}"
        notes.append(f"Gap: the closest {fuel_phase}-fuel test to this scenario is {closest['accession']} {n['test_id']} "
                     f"({n['fuel']}, O2 {n['x_o2_ambient']:.3f}{origin('x_o2')}, {n['pressure_kpa']:.0f} kPa{origin('pressure_kpa')}), "
                     f"{closest['distance_to_scenario']} scale steps away. Conclusions for this scenario are extrapolations.")
    if closest:
        n, res = closest["nearest_test"], closest["nearest_test"].get("result", {})
        if res.get("burn_length_cm") == 0 or res.get("outcome") == "no_ignition" or res.get("ignited") is False:
            notes.append(f"Result of the closest {fuel_phase}-fuel test ({closest['accession']} {n['test_id']}, "
                         f"{n['fuel']}): ignited, but no flame spread. The material resisted fire there; it does not "
                         f"show how a fire grows.")
        setting = _setting(closest["accession"])
        if setting["note"]:
            notes.append(f"Setting of the closest {fuel_phase}-fuel test ({closest['accession']}, {setting['label']}): "
                         f"{setting['note']}")
    data = {"scenario": {"name": name, **sc, "fuel_phase": fuel_phase, "pillar": pillar}, "weights": weights,
            "ranking": ranked[:top], "gap": gap, "closest_same_phase": closest and closest["accession"],
            "closest_same_phase_test": closest and {"accession": closest["accession"], **closest["nearest_test"],
                                                    "condition_ranges": closest["condition_ranges"],
                                                    "distance_to_scenario": closest["distance_to_scenario"],
                                                    "setting": _setting(closest["accession"])}}
    chart = {"type": "stacked-bar", "x": "components", "y": "acronym", "sort": "score"}
    sources = [{"ref": f"[{r['accession']}]"} for r in ranked[:top]]
    return _result(data, chart, sources, notes)


# --- synthesis, time series, models ---------------------------------------------------------------------

def insights(topic="key_messages", accession=None):
    """Cross-investigation synthesis: key_messages, limits, micro_vs_1g, gaps, lineage, research_questions,
    parameter_coverage. Optionally only entries that cite one investigation."""
    syn = synthesis()
    if topic not in syn or topic.startswith("_"):
        raise KeyError(f"unknown topic {topic!r}; known: {', '.join(k for k in syn if not k.startswith('_'))}")
    entries = syn[topic]
    if accession:
        acc = _accession(accession)
        entries = [e for e in entries if re.search(rf"{acc}(?!\d)", json.dumps(e))]
    return _result(_with_quote_es(entries), None, [{"ref": r} for r in _citation_refs(entries)], ["Full text with citations: docs/digest/synthesis.md"])


SECTION_LETTER = {"findings": "F", "limitations": "L", "open_questions": "Q"}


def _citation_refs(entries):
    refs = set()
    for e in entries:
        for c in [*e.get("citations", []), *([e["citation"]] if e.get("citation") else [])]:
            letter = SECTION_LETTER.get(c.get("section"))
            refs.add(f"[{c['accession']} {letter}{c['index']}]" if letter and c.get("index") else f"[{c['accession']}]")
        refs.update(f"[{e[k]}]" for k in ("from", "to") if str(e.get(k, "")).startswith("PSI-"))
    return sorted(refs)


def timeseries(test_id, channels=None, max_points=2000, test_point=None, accession=None):
    """Sensor time series of one test (decimated), with its summary features. Reads the raw files in data/raw."""
    from fif.pipeline import build_timeseries

    features = table("timeseries_features")
    key = str(test_id).replace(" ", "")
    features = features[(features["test_id"].str.replace(" ", "") == key) | (features["test_point"] == key)]
    if test_point is not None:
        features = features[features["test_point"] == test_point]
    if accession is not None:
        features = features[features["accession"] == _accession(accession)]
    if features.empty:
        raise KeyError(f"no time series for test {test_id!r}; tests with one are listed in timeseries_features")
    notes = []
    if features["accession"].nunique() > 1:
        raise KeyError(f"test id {test_id!r} exists in {sorted(features['accession'].unique())}; pass accession")
    if len(features) > 1 and test_point is None:
        notes.append(f"{len(features)} recordings share this test id ({', '.join(features['test_point'])}); "
                     "showing the first. Pass test_point to pick another"
                     + (" (`-reduced` is the investigators' droplet and flame diameters)."
                        if features["test_point"].str.endswith(build_timeseries.CFI_REDUCED_SUFFIX).any() else "."))
        features = features.iloc[:1]
    row = features.iloc[0]
    df = build_timeseries.load_timeseries(row["test_point"], test_point=row["test_point"], accession=row["accession"])
    df = df.drop(columns="test_point")
    if channels:
        df = df[["time_s", *[c for c in channels if c in df.columns]]]
    reduced = row["test_point"].endswith(build_timeseries.CFI_REDUCED_SUFFIX)
    if reduced:
        # each row comes from one of the reduced files: keep the rows that carry a requested channel
        df = df.dropna(how="all", subset=[c for c in df.columns if c != "time_s"])
        notes += ["Reduced data as published by the investigators (droplet and flame diameters from image analysis, "
                  "radiometer power), not raw sensor output. Each quantity has its own sampling, so a row holds one "
                  "file's values and the others are empty.",
                  "Time is as published; zero appears to be ignition (inferred, not stated in the files).",
                  "Zeros are in the source: they mark lost tracking or no flame, not a zero diameter.",
                  *str(row.get("features_note") or "").split("; ")[1:]]
    step = max(1, math.ceil(len(df) / max_points))
    shown = df.iloc[::step]
    if reduced and step > 1:
        # thin each file's rows on their own, or the 100 Hz radiometer would crowd out the 7 s flame-diameter curve
        origin = df.drop(columns="time_s").notna().idxmax(axis=1)
        budget = max(1, max_points // origin.nunique())
        shown = pd.concat(g.iloc[::max(1, math.ceil(len(g) / budget))] for _, g in df.groupby(origin, sort=False)).sort_index()
        notes.append(f"Decimated: {len(shown)} of {len(df)} samples, each quantity thinned separately to about {budget} points.")
    elif step > 1:
        notes.append(f"Decimated: every {step}th sample of {len(df)}.")
    if row["accession"] in ("PSI-10", "PSI-23", "PSI-159", "PSI-39") and not reduced:
        notes.append("Radiometer and PMT channels in volts have no archived calibration: compare shapes, not magnitudes.")
    chart = {"type": "line", "x": "time_s", "y": [c for c in df.columns if c != "time_s"]}
    data = {"test_id": row["test_id"], "test_point": row["test_point"], "accession": row["accession"],
            "features": _rows(features.dropna(axis=1, how="all")), "series": _rows(shown)}
    files = [row["source_file"]]
    if reduced:
        used = str(row.get("reduced_files") or "").split(";")
        files = [f for kind, f in build_timeseries.cfi_reduced_siblings(row["source_file"]).items() if kind in used]
    return _result(data, chart, [*({"accession": row["accession"], "file": f} for f in files),
                                 {"page": "docs/formats.md"}], notes)


def _compact_model(card):
    metric = card.get("cv_metric") or {}
    return {
        "id": card["id"], "accession": card["accession"], "kind": card["kind"], "use": card["use"],
        "question": card["question"], "target": card["target"], "n": card["n"],
        "inputs": [{"name": f["name"], "unit": f.get("unit"), "domain": f.get("domain"),
                    "untested": [gap["range"] for gap in f.get("untested") or []]} for f in card["features"]],
        "accuracy": {"metric": metric.get("name"), "held_out": metric.get("grouped_pooled"),
                     "ci95_days_resampled": metric.get("grouped_pooled_ci95_days_resampled")},
        "must_not_be_used_for": card.get("must_not_be_used_for") or [],
    }


def predict(model_id=None, compact=False, **conditions):
    """Prediction from one of the small per-investigation models (no model_id: list the models; `compact` keeps
    only what is needed to choose a model and call it)."""
    from fif import models

    if model_id is None:
        cards = json.loads((psi.PROCESSED / "models.json").read_text())
        if not compact:
            return _result(cards, None, [{"page": "docs/models.md"}])
        return _result({"models": [_compact_model(c) for c in cards["models"]],
                        "dropped": [{"id": d["id"], "accession": d["accession"]} for d in cards["dropped"]]},
                       None, [{"page": "docs/models.md"}],
                       ["Compact list. `use` says whether a model is predictive or descriptive only; `domain` is the "
                        "fitted range of each input and `untested` the gaps inside it, where predict returns no value. "
                        "Call predict without `compact` for coefficients, cross-validation detail and caveats."])
    out = models.predict(model_id, **conditions)
    notes = ["Each model is fitted on one investigation's hardware and fuels; it is not a general flammability model."]
    if out.get("in_domain") is False:
        notes.append("The conditions are outside the range the model was fitted on (or inside a range it lists as "
                     "untested), so no value is returned; `nearest_tests` are the closest measured tests.")
    m = out.get("cv_metric") or {}
    if out.get("prediction") is not None and m.get("grouped_pooled_ci95_days_resampled"):
        lo, hi = m["grouped_pooled_ci95_days_resampled"]
        notes.append(f"Held-out skill ({m['name']}) is {m['grouped_pooled']:.2f}, but between {lo:.2f} and {hi:.2f} "
                     "when the test days are resampled: treat the value as indicative.")
    if out.get("prediction") is not None and m.get("brier_grouped_pooled") is not None:
        notes.append(f"Brier score of the probability on held-out days is {m['brier_grouped_pooled']:.3f} (lower is "
                     f"better; always giving the base rate scores {m['brier_baseline_grouped_pooled']:.3f}).")
    cov = out.get("interval_coverage")
    if cov and out.get("prediction") is not None:
        levels = (cov.get("by") or {}).get("levels") or {}
        counts = "".join(f"; {k} {c['n_inside']} of {c['n']}" for k, c in levels.items())
        low = [k for k, c in levels.items() if c["verdict"] == "below nominal"]
        if cov["verdict"] == "below nominal":
            low.insert(0, "these tests")
        notes.append(f"`interval` targets {cov['nominal']:.0%} coverage. Measured on held-out test days it held "
                     f"{cov['n_inside']} of {cov['n']} tests{counts}."
                     + (f" It is too narrow for {' and '.join(low)}." if low else ""))
    if out.get("interval_clipped"):
        notes.append("The lower end of `interval` was cut at 0: the quantity cannot be negative.")
    if out.get("prediction_unavailable"):
        notes.append("No estimate is given (`prediction` and `interval` are null): it came out below 0, which is "
                     "impossible for this quantity. Each input is inside its fitted range but the combination was not "
                     "tested; see `nearest_tests` for the closest measured tests.")
    elif out.get("interval_unavailable"):
        notes.append("No range is available (`interval` is null): the whole range came out below 0 "
                     "(`interval_unclipped`), which is impossible for this quantity.")
    if out.get("use") != "predictive":
        notes.append("This model is descriptive only: it summarises the tests and did not hold up in cross-validation.")
    return _result(out, None, [{"page": "docs/models.md", "model": model_id}], notes)


ACTIONS = {
    "replace": "table value replaced by the raw-data value; the table value is kept in extra as `<column>_original`",
    "fill": "table cell was empty; filled from the raw data",
    "flag": "raw data disagree with the table; the table value is kept and the row is flagged. With the flag "
            "conflicts_with_test_sheet the evidence is a hand-filled test sheet, not sensor data",
    "note": "applies to the whole investigation, not to one cell",
}


# Rows whose table value was replaced or blanked while the original stayed under its source column name.
ORIGINAL_KEPT_AS = {
    "o2_from_notes": ("x_o2_ambient", "asrun_o2"),
    "needs_review": ("x_o2_ambient", "asrun_o2"),
    "flow_missing_los": ("flow_cm_s", "Air Rate (cm/s)"),
}


@lru_cache(maxsize=None)
def flag_meanings():
    """Flag code -> meaning, read from the flags table in docs/tests-table.md."""
    out = {}
    for line in (psi.ROOT / "docs" / "tests-table.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"`[a-z0-9_]+`", cells[0]):
            out[cells[0].strip("`")] = cells[1]
    return out


def _removed_sources(accession=None):
    found = []

    def walk(node, acc, where):
        if isinstance(node, dict):
            if node.get("psi_status") == "removed":
                found.append({"accession": acc, "where": where, "url": node.get("url")})
            for key, value in node.items():
                walk(value, acc, where if key == "sources" else f"{where}.{key}" if where else key)
        elif isinstance(node, list):
            for i, value in enumerate(node, 1):
                walk(value, acc, f"{where}[{i}]")

    for acc, record in records().items():
        if accession in (None, acc):
            walk(record, acc, "")
    return found


def _paper_disagreements(accession=None):
    """`contradicts_psi_data` items of the publication reviews: a published paper that disagrees with PSI."""
    out = []
    for acc in records():
        if accession not in (None, acc):
            continue
        for entry in publication_reviews(acc):
            for item in entry["items"]:
                if item["kind"] == "contradicts_psi_data":
                    out.append({"accession": acc, "kind": "published_paper_disagrees_with_psi",
                                "publication": entry["title"], "read_url": entry["read_url"],
                                "locator": item["locator"], "quote": item["quote"], "claim": item["claim"],
                                "record_path": item["record_path"]})
    return out


def discrepancies(accession=None, test_id=None):
    """Where the PSI experiment tables are wrong or doubtful: disagreements with the raw sensor data (each with
    the table value, the raw value, the evidence and what was done), every value this dataset changed, the meaning
    and count of each flag, digest statements that rest on files PSI lists as removed, and places where a published
    paper by the investigators disagrees with the PSI data (shown, never applied to the tables)."""
    acc = _accession(accession) if accession else None
    raw = table("discrepancies")
    tests = table("tests")
    if acc:
        raw, tests = raw[raw["accession"] == acc], tests[tests["accession"] == acc]
    if test_id:
        key = str(test_id).replace(" ", "")
        raw = raw[raw["test_id"].fillna("").str.replace(" ", "").eq(key) | raw["test_id_now"].fillna("").str.replace(" ", "").eq(key)]
        tests = tests[tests["test_id"].str.replace(" ", "") == key]
    changed = []
    for row in tests[tests["extra"].notna()].itertuples():
        extra = json.loads(row.extra)
        originals = {name[:-9]: v for name, v in extra.items() if name.endswith("_original") and name[:-9] in tests.columns}
        for flag, (column, key) in ORIGINAL_KEPT_AS.items():
            if flag in str(row.flags).split(";") and key in extra and column not in originals:
                originals[column] = extra[key]
        for column, original in originals.items():
            changed.append({"accession": row.accession, "test_id": row.test_id, "column": column,
                            "table_value": original, "value_now": getattr(row, column), "flags": row.flags,
                            "patch_ids": extra.get("discrepancies")})
    counts = tests["flags"].dropna().str.split(";").explode().value_counts()
    meanings = flag_meanings()
    flags = [{"flag": code, "rows": int(n), "meaning": meanings.get(code)} for code, n in counts.items()]
    data = {
        "raw_data_conflicts": _rows(raw),
        "actions": ACTIONS,
        "values_changed": changed,
        "flags": flags,
        "rows_flagged": int(tests["flags"].notna().sum()),
        "rows_total": len(tests),
        "removed_sources": _removed_sources(acc),
        "source_disagreements": [] if test_id else _paper_disagreements(acc),
    }
    notes = ["`replace` and `fill` entries changed the table; the PSI value is always kept next to the new one.",
             "Raw-data conflicts were found only where raw sensor files exist (PSI-10, 23, 39, 159, 98, 100, 101); "
             "the other tables were checked against the reports only."]
    if raw["column"].eq("flight_program").any():
        notes.append("Entries whose `column` is flight_program (a field of the investigations table) are errors in "
                     "NASA's catalogue record of the investigation, not in a test table; the record's `location` "
                     "gives where the tests really ran.")
    if data["removed_sources"]:
        notes.append("Some statements rest on files that PSI lists as removed but still serves; they are marked.")
    if data["source_disagreements"]:
        notes.append(PAPER_DISAGREEMENT_NOTE)
    if raw["evidence_source"].str.contains("test sheet").any():
        notes.append("Entries that cite a test sheet rest, in part or (flag conflicts_with_test_sheet) entirely, on an AI "
                     "model's reading of a hand-filled scanned form, not checked by a human; they never change a value.")
    sources = [{"file": "data/corrections/tests_patches.json"}, {"page": "docs/tests-table.md"}, {"page": "docs/formats.md"}]
    return _result(data, {"type": "table", "group_by": "accession", "badge": "action"}, sources, notes)


FUNCTIONS = {f.__name__: f for f in (
    search_investigations, get_investigation, filter_tests, compare, coverage, relevance, find_evidence,
    insights, timeseries, predict, discrepancies, document_text,
)}

if __name__ == "__main__":
    kwargs = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    json.dump(FUNCTIONS[sys.argv[1]](**kwargs), sys.stdout, indent=1, ensure_ascii=False, default=str)
