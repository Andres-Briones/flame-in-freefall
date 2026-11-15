"""Render the knowledge records in data/digest to Markdown pages in docs/digest, plus an index.

Run: uv run python -m fif.pipeline.render_digest [PSI-26 ...]
"""
import json
import re
import sys

from fif import psi

OUT = psi.ROOT / "docs" / "digest"
QUOTE_CHARS = 300
FUEL_CHARS = 60


def present(value):
    return value not in (None, "", [], {})


def clean(text):
    return " ".join(str(text).split())


def truncate(text, limit):
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit)
    return text[:cut if cut > limit // 2 else limit].rstrip(" ,;:") + "…"


def italic(text):
    return "*" + truncate(text, QUOTE_CHARS).replace("*", r"\*") + "*"


def cell(text):
    return clean(text).replace("|", r"\|")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def page_name(record):
    acronym = (record.get("identity") or {}).get("acronym")
    return f"{record['accession']}-{slug(acronym)}.md" if acronym else f"{record['accession']}.md"


def source_line(src):
    kind = src.get("type")
    if kind == "psi_file":
        return f"`{src.get('file')}` ({src.get('locator')}): {italic(src.get('quote', ''))}"
    if kind == "psi_record":
        return f"PSI record field `{src.get('field')}`"
    if kind == "psi_table":
        return f"`{src.get('file')}`, sheet {src.get('sheet')}, row {src.get('row')}: {italic(src.get('value', ''))}"
    if kind == "table":
        return f"Table `{src.get('table')}`: {clean(src.get('note', ''))}"
    if kind == "external":
        quote = f": {italic(src['quote'])}" if src.get("quote") else ""
        removed = " (PSI lists this file as removed; it is still served)" if src.get("psi_status") == "removed" else ""
        return f"<{src.get('url')}>{removed}{quote}"
    if kind == "reference":
        return f"[Reference value `{src.get('id')}`](reference.md)"
    if kind == "background":
        return "Textbook background" + (f": {clean(src['note'])}" if src.get("note") else "")
    return clean(json.dumps(src))


def text_of(block):
    return clean(block["text"]) if isinstance(block, dict) and present(block.get("text")) else None


def short_fuel(name):
    head = re.split(r"\. | \(|:", clean(name), maxsplit=1)[0]
    return truncate(head, FUEL_CHARS)


def with_unit(item, key):
    value, unit = item.get(key), item.get("unit")
    return f"{clean(value)} {unit}" if present(unit) else clean(value)


def section(title, lines):
    lines = [l for l in lines if l is not None]
    return [f"## {title}", "", *lines, ""] if lines else []


def subsection(title, lines):
    lines = [l for l in lines if l is not None]
    return [f"### {title}", "", *lines, ""] if lines else []


def paragraph(text):
    return [text, ""] if text else []


def bullets(items):
    return [f"- {i}" for i in items if present(i)]


def glance(record):
    ident = record.get("identity") or {}
    dates = ident.get("dates") or {}
    tm = record.get("test_matrix") or {}
    fuels = [short_fuel(f["name"]) for f in (record.get("method") or {}).get("fuels_and_samples", []) if present(f.get("name"))]
    varied = [f"{cell(v['parameter'])}: {cell(with_unit(v, 'range'))}" if present(v.get("range")) else cell(v["parameter"])
              for v in tm.get("varied", []) if present(v.get("parameter"))]
    span = " to ".join(d for d in (dates.get("start"), dates.get("end")) if d)
    rows = [
        ("Setting", (record.get("location") or {}).get("label")),
        ("Module note", (record.get("location") or {}).get("module_note")),
        ("Platform", ident.get("platform")),
        ("Facility", ident.get("facility")),
        ("Dates", span),
        ("Fuels and samples", "; ".join(fuels)),
        ("Varied", "<br>".join(varied)),
        ("Number of tests", (tm.get("n_tests") or {}).get("value")),
        ("Fire-safety pillars", ", ".join((record.get("fire_safety") or {}).get("pillars") or [])),
    ]
    rows = [(k, v if k == "Varied" else cell(v)) for k, v in rows if present(v)]
    return section("At a glance", ["| | |", "|---|---|", *[f"| {k} | {v} |" for k, v in rows]])


def method(record):
    m = record.get("method") or {}
    fuels = []
    for f in m.get("fuels_and_samples", []):
        if present(f.get("name")):
            detail = ", ".join(clean(f[k]) for k in ("phase", "form") if present(f.get(k)))
            fuels.append(clean(f["name"]).rstrip(".") + (f" ({detail})" if detail else ""))
    lines = (subsection("Apparatus", paragraph(text_of(m.get("apparatus"))))
             + subsection("Fuels and samples", bullets(fuels))
             + subsection("Procedure", paragraph(text_of(m.get("procedure")))))
    return section("Method", lines)


def test_matrix(record):
    tm = record.get("test_matrix") or {}
    varied = [f"| {cell(v['parameter'])} | {cell(v.get('range') or '')} | {cell(v.get('unit') or '')} |"
              for v in tm.get("varied", []) if present(v.get("parameter"))]
    held = [f"{clean(h['parameter'])}: {clean(h.get('value') or 'not stated')}"
            for h in tm.get("held_constant", []) if present(h.get("parameter"))]
    n = (tm.get("n_tests") or {}).get("value")
    lines = []
    if varied:
        lines += ["Varied:", "", "| Parameter | Range | Unit |", "|---|---|---|", *varied, ""]
    if held:
        lines += ["Held constant:", "", *bullets(held), ""]
    if present(n):
        lines += [f"Number of tests: {clean(n)}", ""]
    return section("Test matrix", lines)


def measurements(record):
    rows = [f"| {cell(m['quantity'])} | {cell(m.get('instrument') or '')} | {'derived' if m.get('derived') else 'direct'} |"
            for m in record.get("measurements") or [] if present(m.get("quantity"))]
    return section("Measurements", ["| Quantity | Instrument | Direct or derived |", "|---|---|---|", *rows] if rows else [])


def findings(record):
    lines = []
    for i, f in enumerate(record.get("findings") or [], 1):
        if not present(f.get("claim")):
            continue
        tags = ", ".join(clean(f[k]) for k in ("kind", "confidence") if present(f.get(k)))
        lines.append(f"{i}. {clean(f['claim'])}" + (f" *({tags})*" if tags else ""))
        lines += [f"   - {source_line(s)}" for s in f.get("sources") or []]
    return section("Findings", lines)


def fire_safety(record):
    fs = record.get("fire_safety") or {}
    lines = (paragraph(text_of(fs.get("relevance")))
             + subsection("Habitat conditions", paragraph(text_of(fs.get("habitat_conditions"))))
             + subsection("Earth benefits", paragraph(text_of(fs.get("earth_benefits")))))
    return section("Fire-safety relevance", lines)


def human_size(gb):
    for unit, scale in (("GB", 1), ("MB", 1e3), ("kB", 1e6)):
        if gb * scale >= 1:
            return f"{gb * scale:.3g} {unit}"
    return f"{gb * 1e9:.0f} B"


def psi_data(record):
    d = record.get("psi_data") or {}
    rows = []
    for g in d.get("file_groups") or []:
        if not present(g.get("what")):
            continue
        size = human_size(g["size_gb"]) if isinstance(g.get("size_gb"), (int, float)) else ""
        usable = {True: "yes", False: "no"}.get(g.get("usable_now"), "")
        rows.append(f"| {cell(g.get('category') or '')} | {cell(g['what'])} | {cell(' '.join(g.get('formats') or []))} "
                    f"| {g.get('n_files') if g.get('n_files') is not None else ''} | {size} | {usable} |")
    lines = paragraph(clean(d["summary"]) if present(d.get("summary")) else None)
    if rows:
        lines += ["| Category | What | Formats | Files | Size | Usable now |", "|---|---|---|---|---|---|", *rows, ""]
    if present(d.get("tests_table_rows")):
        lines += [f"Rows in the unified `tests` table: {d['tests_table_rows']}", ""]
    return section("Data in PSI", lines)


def related(record, pages):
    items = []
    for r in record.get("related") or []:
        acc = r.get("accession")
        if not present(acc):
            continue
        name = f"[{acc}]({pages[acc]})" if acc in pages else acc
        items.append(f"{name}: {clean(r['relation'])}" if present(r.get("relation")) else name)
    return section("Related investigations", bullets(items))


def dashboard(record):
    items = []
    for h in record.get("dashboard_hooks") or []:
        if not present(h.get("view")):
            continue
        fields = ", ".join(f"`{f}`" for f in h.get("fields") or [])
        items.append(f"**{clean(h['view'])}**" + (f" ({fields})" if fields else "")
                     + (f": {clean(h['why'])}" if present(h.get("why")) else ""))
    return section("Dashboard ideas", bullets(items))


def equations(record):
    lines = []
    for eq in (record.get("physics") or {}).get("equations") or []:
        if not present(eq.get("latex")):
            continue
        lines += ["$$", eq["latex"].strip(), "$$", ""]
        if present(eq.get("meaning")):
            lines += [clean(eq["meaning"]), ""]
        lines += [source_line(s) for s in eq.get("sources") or []]
        lines.append("")
    return lines


def render(record, pages=None):
    pages = pages or {}
    ident = record.get("identity") or {}
    name = " ".join(x for x in (ident.get("acronym"), f"({ident['title']})" if ident.get("title") else None) if x)
    lines = [f"# {record['accession']}: {name}" if name else f"# {record['accession']}", ""]
    lines += paragraph(clean(record["one_line"]) if present(record.get("one_line")) else None)
    if ident.get("principal_investigators"):
        lines += paragraph("Investigators: " + "; ".join(clean(p) for p in ident["principal_investigators"]))
    lines += glance(record)
    lines += section("Question", paragraph(text_of(record.get("question"))))
    lines += section("Summary", paragraph(clean(record["summary"]) if present(record.get("summary")) else None))
    lines += section("Physics", paragraph(text_of(record.get("physics"))) + equations(record))
    lines += method(record)
    lines += test_matrix(record)
    lines += measurements(record)
    lines += findings(record)
    lines += fire_safety(record)
    lines += section("Limitations", bullets(text_of(l) for l in record.get("limitations") or []))
    lines += psi_data(record)
    lines += related(record, pages)
    lines += section("Open questions", bullets(clean(q) for q in record.get("open_questions") or [] if present(q)))
    lines += dashboard(record)
    lines += section("Gaps and data-quality notes", bullets(clean(g) for g in record.get("gaps") or [] if present(g)))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).rstrip() + "\n"


def index(records, pages):
    rows = []
    for r in records:
        ident = r.get("identity") or {}
        n = len([f for f in r.get("findings") or [] if present(f.get("claim"))])
        pillars = ", ".join((r.get("fire_safety") or {}).get("pillars") or [])
        rows.append(f"| {r['accession']} | {cell(ident.get('acronym') or '')} | {cell(r.get('one_line') or '')} "
                    f"| {cell(pillars)} | {n} | [page]({pages[r['accession']]}) |")
    return "\n".join([
        "# Investigation digest",
        "",
        "One page per PSI investigation, rendered from `data/digest/PSI-<n>.json` by "
        "`uv run python -m fif.pipeline.render_digest`. Do not edit the pages by hand.",
        "See [AUTHORING.md](AUTHORING.md) for how the records are written and [reference.md](reference.md) "
        "for the shared reference values.",
        "",
        "| Accession | Acronym | In one line | Fire-safety pillars | Findings | Page |",
        "|---|---|---|---|---|---|",
        *rows,
    ]) + "\n"


def load_records():
    paths = sorted(psi.DIGEST.glob("PSI-*.json"), key=lambda p: psi.accession_number(p.stem))
    return [json.loads(p.read_text()) for p in paths]


def main(argv):
    records = load_records()
    targets = [r for r in records if not argv or r["accession"] in argv]
    rendered = [r for r in records if r in targets or (OUT / page_name(r)).exists()]
    pages = {r["accession"]: page_name(r) for r in rendered}
    OUT.mkdir(parents=True, exist_ok=True)
    for r in targets:
        (OUT / pages[r["accession"]]).write_text(render(r, pages))
        print(f"{r['accession']}: docs/digest/{pages[r['accession']]}")
    (OUT / "README.md").write_text(index(rendered, pages))
    print(f"index: docs/digest/README.md ({len(rendered)} investigations)")


if __name__ == "__main__":
    main(sys.argv[1:])
