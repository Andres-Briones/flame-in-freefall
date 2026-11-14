"""`test_sheets` table: one row per page of the ACME "Science Test Sheets" of PSI-10 (Flame Design) and PSI-159
(CFI-G), the hand-filled form the operations team completed for every test point, parsed from the AI
transcriptions of the scans in data/transcriptions/. Every value is an AI model's reading of handwriting, not
checked by a human: `*_written` columns keep the reading verbatim, the normalised columns next to them are empty
whenever the reading is not one clear option. Column reference: docs/formats.md.

Run: uv run python -m fif.pipeline.build_test_sheets
"""
import re
from datetime import date

import pandas as pd

from fif import psi
from fif.pipeline.build_evidence import PAGE_HEADING, TRANSCRIPTIONS
from fif.pipeline.build_tests import yyddd
from fif.pipeline.redact import redact

ACCESSIONS = ("PSI-10", "PSI-159")
SHEET_FILE = re.compile(r"_Raw Data_(\d{5}) tests? sheets\.pdf\.md$")
DATA_FILE = re.compile(r"_Raw Data_(\d{5}[A-Z]\d{1,2}(?:_\d)?)_data\.csv$")

SECTIONS = ("TEST CONDITIONS", "INSTRUMENTATION", "FLAME BEHAVIOR", "POST-TEST CONDITIONS", "GENERAL COMMENTS")
TITLE = re.compile(r"^ACME / (.+?) - Science Test Sheet", re.M)
FIELD = re.compile(r"^([^:]{1,60}?):(?:\s+(.*))?$")
MARKER = re.compile(r"\[(?:differs from as-run file:|no as-run file)[^\]]*\]")
BRACKETS = re.compile(r"\[[^\]]*\]")
NUMBER = re.compile(r"(?<![\w.])\d*\.?\d+(?![\w.]*\d)")
ID_TAIL = re.compile(r"([A-Z])\s?(\d{1,2})(?!\d)")
MONTHS = {m: i for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), start=1)}
OUT_OPTIONS = {"ext. detect": "ext_detect", "time out": "time_out", "temp. limit": "temp_limit"}
SOOT_LEVELS = ("none", "little", "lots")
# A test point the operators wrote under one id and the facility recorded under another.
RECORDED_AS = {
    ("PSI-159", "21196M3"): ("21196M2_1", "the sheet adds '(M2-1)' to the id: the run was recorded as 21196M2_1 "
                                          "(its data file starts at 22:06 GMT; the sheet says 22:05)"),
}

COLUMNS = [
    "accession", "file_name", "page", "form", "day",
    "test_id_written", "test_id", "test_id_basis", "test_id_note", "in_tests", "tests_test_id", "has_data_file",
    "date_written", "date_parsed", "date", "date_note", "gmt_written", "test_of_day_written", "flame_of_day_written",
    "test_type_written",
    "chamber_pressure_written", "chamber_pressure_psia", "fuel_flow_written", "fuel_flow_slpm",
    "o2_flow_written", "o2_flow_slpm", "n2_flow_written", "n2_flow_slpm",
    "ignited_written", "ignited", "flame_written", "flame", "flame_behavior_written",
    "soot_written", "soot_ignition_written", "soot_ignition", "soot_middle_written", "soot_middle",
    "soot_end_written", "soot_end", "out_written", "out",
    "chamber_pressure_post_written", "chamber_pressure_post_psia",
    "oxidizer_bottle_pressure_written", "oxidizer_bottle_pressure_psia",
    "flame_behavior_note", "comments", "n_uncertain", "n_illegible", "differs_from_asrun", "differs_text",
]


def label_key(label):
    """The printed label without the options or units a transcriber kept in it: 'Out (ext. detect / ...)' -> 'out'."""
    return re.split(r"\s*[(\[]", label, maxsplit=1)[0].strip().lower()


def main_part(value):
    """What is marked or written in the field itself: transcriber remarks in brackets and the `— note:` tail removed."""
    return " ".join(BRACKETS.sub(" ", (value or "").split("— note:")[0]).split())


def one_number(value):
    """The field's value when it holds exactly one number (a ramp '0.207 > 0.494' or an empty box gives None)."""
    found = NUMBER.findall(re.sub(r"(?<=\d),(?=\d{3})", "", main_part(value)))
    return float(found[0]) if len(found) == 1 else None


def parse_page(text):
    """{'form', 'fields': {section: [(label key, raw label, value)]}, 'comments', 'section_notes'} of one sheet."""
    page = {"form": None, "fields": {s: [] for s in ("HEADER", *SECTIONS)}, "comments": [], "section_notes": {}}
    section = "HEADER"
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if title := TITLE.match(line):
            page["form"] = title.group(1)
            continue
        header = next((s for s in SECTIONS if line == s or re.match(rf"{re.escape(s)}\s*(:|—|\[)", line)), None)
        if header:
            section = header
            if line != header:
                page["section_notes"][header] = line[len(header):].lstrip(" :—").removeprefix("note:").strip()
            continue
        if line.startswith("Form date:"):
            section = "FOOTER"
        elif section == "GENERAL COMMENTS":
            page["comments"].append(line)
        elif section != "FOOTER" and (m := FIELD.match(line)):
            page["fields"][section].append((label_key(m.group(1)), m.group(1), (m.group(2) or "").strip() or None))
    return page


def first(page, section, *keys):
    return next((value for key, _, value in page["fields"][section] if key in keys), None)


def resolve_id(written, day):
    """(test id, basis, note). The day code comes from the file name whenever the digits written on the sheet are
    not that day: the sheets of one PDF are one test day, and the operators' slips are all in the digits."""
    text = re.sub(r"\(.*?\)", " ", main_part(MARKER.sub(" ", written or "")))
    tails = ID_TAIL.findall(text)
    if not tails:
        return None, None, "no test letter and number readable in the id box"
    letter, number = tails[-1]
    digits = re.sub(r"\D", "", text[:text.rfind(letter)])
    test_id = f"{day}{letter}{number}"
    if digits == day:
        return test_id, "as_written", None
    seen = f"day digits written as {digits!r}" if digits else "day digits struck or illegible"
    return test_id, "day_from_file_name", f"{seen}; the sheet is in the {day} file"


def parse_date(written):
    """ISO date from 'April 25, 2019', 'Sept. 13 2021', '27 Jan 2022' or '5/3/2019'; None without a full date."""
    text = main_part(re.sub(r"\(.*?\)", " ", written or ""))
    if m := re.search(r"(?<!\d)(\d{1,2})/(\d{1,2})/(\d{4})(?!\d)", text):
        month, day, year = map(int, m.groups())
    else:
        m = re.search(r"([A-Za-z]{3})[a-z]*\.?\s*(\d{1,2})(?!\d),?\s*(\d{4})(?!\d)", text) \
            or re.search(r"(?<!\d)(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?,?\s*(\d{4})(?!\d)", text)
        if not m:
            return None
        a, b, year = m.groups()
        name, day = (a, b) if a[0].isalpha() else (b, a)
        month, day, year = MONTHS.get(name.lower()), int(day), int(year)
    try:
        return date(year, month, day).isoformat() if month else None
    except ValueError:
        return None


def ignited(value):
    text = main_part(value).lower()
    if not text or text.startswith("not marked"):
        return None
    if re.search(r"yes,? but", text):
        return "yes_but"
    if re.match(r"(yes|no)\b", text):
        return text.split()[0].strip(",;")
    return "unclear"


def flame_kind(flame_lines):
    """hot / cool / hot+cool / maybe_cool from the hot-or-cool row of the inverse and CFI-G forms. Some
    transcriptions drop the options from the label: the row is then the first of the form's three 'Flame' rows."""
    labelled = [(raw, value) for key, raw, value in flame_lines if "hot" in raw.lower()]
    if not labelled and len(flame_lines) == 3 and all(raw.strip().lower() == "flame" for _, raw, _ in flame_lines):
        labelled = [(flame_lines[0][1], flame_lines[0][2])]
    if not labelled:
        return None, None
    raw, value = labelled[0]
    text = main_part(value).lower()
    if raw.strip().lower() == "flame hot":
        return value, "hot" if text.startswith("marked") else None
    marks = [m for m in re.split(r"\s*[,;/]\s*", text) if m]
    if not marks or any(m not in ("hot", "cool", "maybe cool") for m in marks):
        return value, None
    return value, "+".join(dict.fromkeys(marks)).replace(" ", "_")


def one_option(value, options):
    """The single option a field shows; None when none or several are marked."""
    text = main_part(value).lower()
    hits = [name for name in options if re.search(rf"(?<![a-z]){re.escape(name)}(?![a-z])", text)]
    return hits[0] if len(hits) == 1 else None


def sheet_row(accession, file_name, day, page_no, text):
    page = parse_page(text)
    f = page["fields"]
    written_id = first(page, "HEADER", "acme test #") or ""
    test_id, basis, note = resolve_id(written_id, day)
    if (accession, test_id) in RECORDED_AS:
        (test_id, note), basis = RECORDED_AS[(accession, test_id)], "recorded_under_other_id"
    date_written = first(page, "HEADER", "test date")
    parsed, day_date = parse_date(date_written), yyddd(day)
    flames = [x for x in f["FLAME BEHAVIOR"] if x[0].startswith("flame")]
    flame_written, flame = flame_kind(flames)
    out_written = first(page, "FLAME BEHAVIOR", "out")
    markers = MARKER.findall(text)
    pressure = first(page, "TEST CONDITIONS", "chamber pressure")
    pressure_post = first(page, "POST-TEST CONDITIONS", "chamber pressure")
    bottle = first(page, "POST-TEST CONDITIONS", "oxidizer bottle pressure")
    flows = {gas: first(page, "TEST CONDITIONS", f"{gas} flow rate") for gas in ("fuel", "o2", "n2")}
    soot = {when: first(page, "FLAME BEHAVIOR", f"soot@{when}") for when in ("ignition", "middle", "end")}
    return {
        "accession": accession, "file_name": file_name, "page": page_no, "form": page["form"], "day": day,
        "test_id_written": written_id or None, "test_id": test_id, "test_id_basis": basis, "test_id_note": note,
        "date_written": date_written, "date_parsed": parsed, "date": day_date,
        "date_note": f"sheet says {parsed}; day code {day} is {day_date}" if parsed and parsed != day_date else None,
        "gmt_written": first(page, "HEADER", "gmt"), "test_of_day_written": first(page, "HEADER", "test of day #"),
        "flame_of_day_written": first(page, "HEADER", "flame of day #", "hot flame of day #"),
        "test_type_written": first(page, "TEST CONDITIONS", "test type?"),
        "chamber_pressure_written": pressure, "chamber_pressure_psia": one_number(pressure),
        **{f"{gas}_flow_written": value for gas, value in flows.items()},
        **{f"{gas}_flow_slpm": one_number(value) for gas, value in flows.items()},
        "ignited_written": first(page, "FLAME BEHAVIOR", "ignited?"),
        "ignited": ignited(first(page, "FLAME BEHAVIOR", "ignited?")),
        "flame_written": flame_written, "flame": flame,
        "flame_behavior_written": "; ".join(v for _, _, v in flames if v != flame_written and v) or None,
        "soot_written": first(page, "FLAME BEHAVIOR", "soot"),
        **{f"soot_{when}_written": value for when, value in soot.items()},
        **{f"soot_{when}": one_option(value, SOOT_LEVELS) for when, value in soot.items()},
        "out_written": out_written, "out": OUT_OPTIONS.get(one_option(out_written, OUT_OPTIONS)),
        "chamber_pressure_post_written": pressure_post, "chamber_pressure_post_psia": one_number(pressure_post),
        "oxidizer_bottle_pressure_written": bottle, "oxidizer_bottle_pressure_psia": one_number(bottle),
        "flame_behavior_note": page["section_notes"].get("FLAME BEHAVIOR"),
        "comments": " | ".join(page["comments"]) or None,
        "n_uncertain": text.count("[?]"), "n_illegible": text.count("illegible"),
        "differs_from_asrun": bool(markers), "differs_text": " ".join(markers) or None,
    }


def read_sheets(root=None):
    rows = []
    for accession in ACCESSIONS:
        for path in sorted(((root or TRANSCRIPTIONS) / accession).glob("*.md")):
            m = SHEET_FILE.search(path.name)
            if not m:
                continue
            parts = PAGE_HEADING.split(path.read_text(encoding="utf-8"))
            for number, body in zip(parts[1::2], parts[2::2]):
                if not TITLE.search(body):
                    continue
                rows.append(sheet_row(accession, path.name.removesuffix(".md"), m.group(1), int(number), redact(body)))
    return rows


def link(rows, tests, files):
    """Mark the sheets whose resolved id is a row of `tests` (ids compared without spaces) and those whose test
    point has a sensor recording (`<id>_data.csv`) among the files PSI lists."""
    in_tests = {(a, t.replace(" ", "")): t for a, t in zip(tests["accession"], tests["test_id"].astype(str))}
    recorded = {(a, m.group(1)) for a, name in zip(files["accession"], files["file_name"].astype(str))
                if (m := DATA_FILE.search(name))}
    for row in rows:
        key = (row["accession"], row["test_id"])
        row["tests_test_id"] = in_tests.get(key)
        row["in_tests"], row["has_data_file"] = key in in_tests, key in recorded
    return rows


def build(root=None):
    tests = pd.read_parquet(psi.PROCESSED / "tests.parquet", columns=["accession", "test_id"])
    files = pd.read_parquet(psi.PROCESSED / "files.parquet", columns=["accession", "file_name"])
    df = pd.DataFrame(link(read_sheets(root), tests, files), columns=COLUMNS)
    return df.astype({c: "string" for c in df.columns if df[c].dtype == object})


if __name__ == "__main__":
    df = build()
    psi.write_table(df, "test_sheets")
    print(df.notna().sum().to_string())  # the parse coverage quoted in docs/formats.md
    print(df.groupby(["accession", "in_tests", "has_data_file"]).size().to_string())
