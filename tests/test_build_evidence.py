import pandas as pd
import pytest

from fif import psi
from fif.pipeline.build_evidence import chunk_text, extract, in_scope, test_ref as find_test_ref, unshift


def test_chunk_text_collapses_whitespace_and_drops_empty():
    assert chunk_text("  hello \t\n world  \n\n\n   \n\n") == ["hello world"]
    assert chunk_text("   \n\n  ") == []


def test_chunk_text_packs_paragraphs_up_to_size():
    paras = ["a" * 40, "b" * 40, "c" * 40]
    assert chunk_text("\n\n".join(paras), size=100) == [f"{paras[0]} {paras[1]}", paras[2]]


def test_chunk_text_splits_long_paragraph_on_sentences():
    text = " ".join(f"Sentence number {i} is here." for i in range(200))
    chunks = chunk_text(text, size=300)
    assert all(len(c) <= 300 for c in chunks)
    assert all(c.endswith(".") for c in chunks)
    assert " ".join(chunks) == text


def test_chunk_text_hard_splits_unbroken_text():
    chunks = chunk_text("x" * 3200, size=1500)
    assert [len(c) for c in chunks] == [1500, 1500, 200]


def test_test_ref():
    assert find_test_ref("PSI-10_Raw Data_as run19189A3.txt") == "19189A3"
    assert find_test_ref("PSI-159_Raw Data_21196M2_1_Comments.txt") == "21196M2"
    assert find_test_ref("PSI-10_Raw Data_21301 test sheets.pdf") is None


def test_in_scope():
    assert in_scope("Reports", ".pdf")
    assert in_scope("metadata", ".zip")
    assert not in_scope("Engineering Documents", ".zip")
    assert in_scope("Raw Data", ".txt")
    assert not in_scope("Raw Data", ".csv")
    assert not in_scope("Raw Data", ".xlsx")


def _first_downloaded_pdf():
    path = psi.PROCESSED / "files.csv"
    if not path.exists():
        return None
    files = pd.read_csv(path)
    pdfs = files[files["downloaded"] & (files["extension"] == ".pdf") & (files["category"] == "Reports")]
    for row in pdfs.to_dict("records"):
        if (psi.ROOT / row["local_path"]).exists():
            return row
    return None


def test_extract_real_pdf():
    row = _first_downloaded_pdf()
    if row is None:
        pytest.skip("no downloaded report PDF")
    chunks, info = extract(row)
    assert info["status"] == "ok"
    assert info["n_chars"] > 0
    assert chunks[0]["locator"].startswith("p")
    assert all(0 < len(c["text"]) <= 1500 for c in chunks)


def test_numeric_text_files_are_previewed_not_chunked(tmp_path):
    from fif.pipeline.build_evidence import read_txt

    data = tmp_path / "radiometer.txt"
    data.write_text("\n".join(f"{i * 0.01:.2f}\t{i * 1.5:.3f}" for i in range(5000)))
    notes = tmp_path / "comments.txt"
    notes.write_text("Flame ignited on the first attempt and burned blue for 40 s. " * 20)

    [(locator, text)] = read_txt(data)
    assert locator == "preview" and len(text) < 500
    [(locator, text)] = read_txt(notes)
    assert locator == "all" and "burned blue" in text


def test_delimited_tables_saved_as_txt_are_previewed(tmp_path):
    from fif.pipeline.build_evidence import read_txt

    table = tmp_path / "readings.txt"
    rows = ['"PIP TimeStamp","TIME(GMT)","IGNITER(N/A)","SAMPLE_00(VDC)"']
    rows += [f'"2017:068:19:03:{i % 60:02d}","19:03:{i % 60:02d}","OFF","{i * 0.001:.4f}"' for i in range(200)]
    table.write_text("\n".join(rows))

    [(locator, text)] = read_txt(table)
    assert locator == "preview" and "PIP TimeStamp" in text


def test_text_from_a_shifted_font_is_shifted_back():
    plain = "the FLEX-1 experiment has provided an abundance of data that is undergoing analysis."
    stored = "".join(c if c == " " else chr(ord(c) - 28) for c in plain)
    assert unshift(stored) == plain
    assert unshift(plain) == plain
    table = "T1 1200 K; P 101.3 KPA; O2 21.0 %; N2 79.0 %; RUN 12 OF 40; CH4 0.5 SLPM"
    assert unshift(table) == table
