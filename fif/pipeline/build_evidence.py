"""`evidence` table: text extracted from downloaded PSI documents, chunked per locator,
plus `evidence_files`: one row per processed file with its extraction status. A scanned PDF with no text layer
is read from its transcription in data/transcriptions/ when one exists; those chunks have `transcribed` = True.

Run: uv run python -m fif.pipeline.build_evidence
"""
import csv
import io
import logging
import warnings
import re
import zipfile
from concurrent.futures import ProcessPoolExecutor
from itertools import islice
from pathlib import Path

import pandas as pd

from fif import psi
from fif.pipeline.redact import WITHHELD, redact

CHUNK_CHARS = 1500
PREVIEW_ROWS = 5
MIN_PDF_CHARS_PER_PAGE = 50
TEXT_EXTENSIONS = {".pdf", ".pptx", ".docx", ".txt", ".xlsx", ".xls", ".csv", ".ppt", ".doc"}
RAW_DATA_EXTENSIONS = {".pdf", ".docx", ".txt"}
UNSUPPORTED = {".ppt", ".doc"}
ZIP_TEXT_MEMBERS = {".txt", ".csv", ".tsv", ".xml", ".json", ".md"}
TEST_REF = re.compile(r"(?<!\d)(\d{5}[A-Za-z]\d)(?!\d)")
EVIDENCE_COLUMNS = ["accession", "category", "file_name", "local_path", "locator", "chunk", "text", "test_ref", "transcribed"]
TRANSCRIPTIONS = psi.ROOT / "data" / "transcriptions"
PAGE_HEADING = re.compile(r"^## page (\d+)[ \t]*$", re.M)
BLANK_PAGE = "[blank page]"


def in_scope(category, extension):
    if category == "Raw Data":
        return extension in RAW_DATA_EXTENSIONS
    if extension == ".zip":
        return category == "metadata"
    return extension in TEXT_EXTENSIONS


def test_ref(file_name):
    m = TEST_REF.search(file_name)
    return m.group(1).upper() if m else None


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def _split_long(piece, size):
    sentences = re.split(r"(?<=[.!?;:])\s+", piece)
    out = []
    for s in sentences:
        while len(s) > size:
            cut = s.rfind(" ", 0, size)
            cut = cut if cut > size // 2 else size
            out.append(s[:cut].strip())
            s = s[cut:].strip()
        out.append(s)
    return out


def chunk_text(text, size=CHUNK_CHARS):
    pieces = []
    for para in re.split(r"\n\s*\n", text):
        para = normalize(para)
        if para:
            pieces.extend(_split_long(para, size) if len(para) > size else [para])
    chunks, current = [], ""
    for p in pieces:
        if current and len(current) + 1 + len(p) > size:
            chunks.append(current)
            current = p
        else:
            current = f"{current} {p}" if current else p
    if current:
        chunks.append(current)
    return [c for c in chunks if c]


def decode(data):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1")


FONT_SHIFT = 28


def _letters(text):
    return sum(c.islower() for c in text) / max(sum(not c.isspace() for c in text), 1)


def unshift(text):
    """Some PDFs embed a font whose character codes are 28 below ASCII, so the text layer reads `XLI JMREP`
    for `the final`. When shifting back turns a page with almost no lower-case letters into mostly lower-case
    text, the shifted reading is used. Blanks the extractor inserted itself are kept."""
    if len(text) < 40 or _letters(text) > 0.2:
        return text
    shifted = "".join(c if c.isspace() else chr(ord(c) + FONT_SHIFT) for c in text)
    return shifted if _letters(shifted) > 0.6 else text


def read_pdf(path):
    from pypdf import PdfReader

    reader = PdfReader(path)
    return [(f"p{i}", unshift(page.extract_text() or "")) for i, page in enumerate(reader.pages, 1)]


def read_transcription(accession, file_name):
    """Pages of an AI model's reading of a scanned PDF, as (locator, text) with the locators `read_pdf` gives."""
    path = TRANSCRIPTIONS / accession / f"{file_name}.md"
    if not path.exists():
        return []
    parts = PAGE_HEADING.split(path.read_text(encoding="utf-8"))
    return [(f"p{n}", "" if body.strip() == BLANK_PAGE else body) for n, body in zip(parts[1::2], parts[2::2])]


def _shape_text(shape):
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        return "\n".join(_shape_text(s) for s in shape.shapes)
    if getattr(shape, "has_table", False) and shape.has_table:
        return "\n".join(" | ".join(c.text for c in row.cells) for row in shape.table.rows)
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        return shape.text_frame.text
    return ""


def read_pptx(path):
    from pptx import Presentation

    out = []
    for i, slide in enumerate(Presentation(path).slides, 1):
        parts = [_shape_text(s) for s in slide.shapes]
        if slide.has_notes_slide:
            parts.append(slide.notes_slide.notes_text_frame.text)
        out.append((f"slide {i}", "\n\n".join(p for p in parts if p.strip())))
    return out


def read_docx(path):
    import docx

    doc = docx.Document(path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        parts.extend(" | ".join(c.text for c in row.cells) for row in table.rows)
    return [("all", "\n\n".join(parts))]


MAX_NOTE_CHARS = 200_000


def is_data_dump(text):
    """True for instrument output saved as .txt: mostly numbers, or a delimited table."""
    sample = text[:20000]
    if not sample:
        return False
    if len(text) > MAX_NOTE_CHARS:
        return True
    if sum(c.isdigit() or c in ".,-+eE \t\n\r" for c in sample) / len(sample) > 0.8:
        return True
    lines = [line for line in sample.splitlines()[:-1] if line.strip()]
    if len(lines) < 30:
        return False
    counts = [max(line.count(","), line.count("\t")) for line in lines]
    typical = max(set(counts), key=counts.count)
    return typical >= 3 and counts.count(typical) / len(counts) > 0.8


def read_txt(path):
    text = decode(Path(path).read_bytes())
    if is_data_dump(text):
        lines = text.splitlines()
        return [("preview", f"data file, {len(lines)} lines; first lines:\n" + "\n".join(line[:400] for line in lines[:6]))]
    return [("all", text)]


def _cells(row):
    return " | ".join("" if v is None else str(v).strip() for v in row)


def sheet_preview(name, rows):
    rows = (r for r in rows if any(v not in (None, "") for v in r))
    head = list(islice(rows, PREVIEW_ROWS + 1))
    n_rows = len(head) + sum(1 for _ in rows)
    lines = [f"sheet {name}: {n_rows} non-empty rows"]
    if head:
        lines.append("header: " + _cells(head[0]))
        lines.extend(f"row {i}: {_cells(r)}" for i, r in enumerate(head[1:], 1))
    return "\n".join(lines)


def read_xlsx(path):
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        return [(f"sheet {ws.title}", sheet_preview(ws.title, ws.iter_rows(values_only=True))) for ws in wb.worksheets]
    finally:
        wb.close()


def read_xls(path):
    import xlrd

    wb = xlrd.open_workbook(path, on_demand=True)
    out = []
    for name in wb.sheet_names():
        sh = wb.sheet_by_name(name)
        out.append((f"sheet {name}", sheet_preview(name, (sh.row_values(i) for i in range(sh.nrows)))))
    return out


def read_csv(path):
    text = decode(Path(path).read_bytes())
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    return [("all", sheet_preview(Path(path).name, csv.reader(io.StringIO(text), dialect)))]


def read_zip(path):
    out = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if not info.is_dir() and Path(info.filename).suffix.lower() in ZIP_TEXT_MEMBERS:
                out.append((f"member {info.filename}", decode(zf.read(info))))
    return out


READERS = {
    ".pdf": read_pdf,
    ".pptx": read_pptx,
    ".docx": read_docx,
    ".txt": read_txt,
    ".xlsx": read_xlsx,
    ".xls": read_xls,
    ".csv": read_csv,
    ".zip": read_zip,
}


def file_status(extension, locators, n_chars):
    if n_chars == 0:
        return "no_text"
    if extension == ".pdf" and n_chars / max(len(locators), 1) < MIN_PDF_CHARS_PER_PAGE:
        return "no_text"
    return "ok"


def extract(row):
    meta = {k: row[k] for k in ("accession", "category", "file_name", "extension")}
    if row["extension"] in UNSUPPORTED:
        return [], {**meta, "status": "unsupported", "n_locators": 0, "n_chars": 0, "error": None}
    if (row["accession"], row["file_name"]) in WITHHELD:
        return [], {**meta, "status": "withheld", "n_locators": 0, "n_chars": 0, "error": None}
    try:
        locators = READERS[row["extension"]](psi.ROOT / row["local_path"])
    except Exception as e:
        return [], {**meta, "status": "error", "n_locators": 0, "n_chars": 0, "error": f"{type(e).__name__}: {e}"[:200]}
    chunks = to_chunks(row, locators, transcribed=False)
    n_chars = sum(len(c["text"]) for c in chunks)
    status = file_status(row["extension"], locators, n_chars)
    if status == "no_text" and row["extension"] == ".pdf":
        pages = read_transcription(row["accession"], row["file_name"])
        transcribed = to_chunks(row, pages, transcribed=True)
        if transcribed:
            locators, chunks, status = pages, transcribed, "transcribed"
            n_chars = sum(len(c["text"]) for c in chunks)
    return chunks, {**meta, "status": status, "n_locators": len(locators), "n_chars": n_chars, "error": None}


def to_chunks(row, locators, transcribed):
    ref = test_ref(row["file_name"]) if row["category"] == "Raw Data" else None
    keys = ("accession", "category", "file_name", "local_path")
    return [
        {**{k: row[k] for k in keys}, "locator": loc, "chunk": i, "text": redact(text, context=raw), "test_ref": ref,
         "transcribed": transcribed}
        for loc, raw in locators
        for i, text in enumerate(chunk_text(raw))
    ]


def selected_files():
    files = pd.read_csv(psi.PROCESSED / "files.csv")
    scoped = [in_scope(c, e) for c, e in zip(files["category"], files["extension"])]
    mask = files["downloaded"] & pd.Series(scoped, index=files.index)
    return files[mask].to_dict("records")


def quiet_parsers():
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def build(workers=None):
    rows = selected_files()
    with ProcessPoolExecutor(workers, initializer=quiet_parsers) as pool:
        results = list(pool.map(extract, rows, chunksize=8))
    evidence = pd.DataFrame([c for chunks, _ in results for c in chunks], columns=EVIDENCE_COLUMNS)
    files = pd.DataFrame([f for _, f in results])
    return evidence, files


if __name__ == "__main__":
    evidence, files = build()
    psi.write_table(evidence, "evidence")
    psi.write_table(files, "evidence_files")
    print(pd.crosstab(files["extension"], files["status"], margins=True).to_string())
    per_acc = evidence.assign(n_chars=evidence["text"].str.len()).groupby("accession").agg(
        chunks=("text", "size"), chars=("n_chars", "sum")
    )
    print(per_acc.to_string())
