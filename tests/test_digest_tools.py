import json

import pytest

from fif import psi
from fif.pipeline import check_digest as cd
from fif.pipeline import render_digest as rd

TEMPLATE = {
    "_about": "ignored",
    "accession": "PSI-0",
    "identity": {"acronym": None, "dates": {"start": None, "end": None}},
    "one_line": "One sentence a non-specialist can read.",
    "question": {"text": "What the investigation set out to learn and why.", "sources": []},
    "findings": [{"claim": "One finding per item.", "kind": "result|limit|trend", "sources": []}],
    "gaps": ["What could not be found, and where we looked."],
}


def record(**overrides):
    r = {
        "accession": "PSI-1",
        "identity": {"acronym": "X", "dates": {"start": "2020-01-01", "end": None}},
        "one_line": "A flame burned in orbit.",
        "question": {"text": "Why?", "sources": [{"type": "background"}]},
        "findings": [{"claim": "It burned.", "kind": "result", "sources": [{"type": "background"}]}],
        "gaps": [],
    }
    r.update(overrides)
    return r


def messages(issues, level=None):
    return [f"{i['path']}: {i['message']}" for i in issues if level in (None, i["level"])]


@pytest.mark.parametrize(
    "quote, text",
    [
        ("burns  as well\nas", "it burns as well as before"),
        ("the “wake” flame", 'the "wake" flame'),
        ('the "wake" flame', "the “wake” flame"),
        ("0.15-0.21", "0.15 – 0.21".replace(" ", "")),
        ("NASA- STD-6001", "NASA- STD-6001"),
        ("ﬁre safety", "fire safety"),
    ],
)
def test_quote_matches_after_normalisation(quote, text):
    assert cd.quote_in(quote, [text])


def test_quote_does_not_ignore_real_differences():
    assert not cd.quote_in("burns better", ["burns as well"])
    assert not cd.quote_in("Burns", ["burns"])
    assert not cd.quote_in("", ["anything"])


def test_quote_may_span_consecutive_chunks():
    assert cd.quote_in("end of one. Start of two", ["text at the end of one.", "Start of two and more"])
    assert cd.quote_in("a hard-split word", ["a hard-sp", "lit word"])
    assert not cd.quote_in("end of one. Start of two", ["end of one.", "unrelated", "Start of two"])


def test_structure_accepts_a_complete_record():
    assert cd.structure_issues(record(), TEMPLATE) == []


def test_structure_reports_missing_and_unexpected_keys_at_any_depth():
    r = record(extra=1)
    del r["gaps"]
    del r["identity"]["dates"]["end"]
    r["findings"][0]["note"] = "x"
    assert sorted(messages(cd.structure_issues(r, TEMPLATE))) == [
        ": missing key 'gaps'",
        ": unexpected key 'extra'",
        "findings[0]: unexpected key 'note'",
        "identity.dates: missing key 'end'",
    ]


def test_structure_reports_wrong_container_types():
    r = record(question=None, findings={"claim": "x"})
    assert sorted(messages(cd.structure_issues(r, TEMPLATE))) == [
        "findings: expected a list, got dict",
        "question: expected an object, got NoneType",
    ]


def test_structure_flags_placeholders_and_enum_values():
    r = record(one_line=TEMPLATE["one_line"], gaps=[TEMPLATE["gaps"][0]])
    r["findings"][0]["kind"] = "guess"
    errors = messages(cd.structure_issues(r, TEMPLATE), "error")
    warnings = messages(cd.structure_issues(r, TEMPLATE), "warning")
    assert [e.split(":")[0] for e in errors] == ["gaps[0]", "one_line"]
    assert warnings == ["findings[0].kind: 'guess' is not one of ['result', 'limit', 'trend']"]


def test_structure_ignores_underscore_keys_and_short_example_values():
    template = {"_source_format": {}, "view": "extinction boundary map"}
    assert cd.structure_issues({"_about": "x", "view": "extinction boundary map"}, template) == []


def test_unsourced_claims_are_errors_and_other_text_warnings():
    r = record(physics={"text": "Buoyancy is absent.", "sources": []})
    r["findings"][0]["sources"] = []
    r["question"]["sources"] = []
    issues = cd.coverage_issues(r)
    assert sorted(messages(issues, "error")) == ["findings[0]: claim has no source", "question: claim has no source"]
    assert messages(issues, "warning") == ["physics: text has no source"]


def test_habitat_conditions_should_cite_a_reference_value():
    habitat = {"text": "Tested at 21% O2.", "sources": [{"type": "background"}]}
    r = record(fire_safety={"habitat_conditions": habitat})
    assert messages(cd.coverage_issues(r)) == [
        "fire_safety.habitat_conditions: no reference source (see docs/digest/reference.md)"]
    habitat["sources"].append({"type": "reference", "id": "moon-habitat"})
    assert cd.coverage_issues(r) == []


def test_sources_are_found_anywhere_and_type_fields_checked():
    r = record(extra={"deep": [{"sources": [{"type": "psi_file", "file": "f.pdf"}, {"type": "rumour"}, "text"]}]})
    issues, counts = cd.source_issues("PSI-1", r, cd.Context())
    assert counts == {"background": 2, "psi_file": 1, "rumour": 1}
    assert sorted(messages(issues)) == [
        "extra.deep[0].sources[0]: psi_file source missing locator, quote",
        "extra.deep[0].sources[1]: unknown source type 'rumour'",
        "extra.deep[0].sources[2]: source is not an object: 'text'",
    ]


class FakeContext(cd.Context):
    def evidence(self, acc):
        return {"doc.pdf": {"p1": ["Intro text."], "p2": ["The flame went", "out at 1 cm/s."]}}

    def files(self, acc):
        return {"doc.pdf", "drawing.pdf"}


@pytest.mark.parametrize(
    "locator, quote, expected",
    [
        ("p2", "went out at 1 cm/s", None),
        ("p1", "went out at 1 cm/s", ("warning", "quote is at locator p2, not 'p1' in doc.pdf")),
        ("p2", "went out at 2 cm/s", ("error", "quote not found in doc.pdf: 'went out at 2 cm/s'")),
    ],
)
def test_psi_file_quote_locations(locator, quote, expected):
    src = {"type": "psi_file", "file": "doc.pdf", "locator": locator, "quote": quote}
    found = cd.psi_file_issue("s", src, "PSI-1", FakeContext())
    assert (found and (found["level"], found["message"])) == expected


def test_psi_file_without_text_is_an_error():
    src = {"type": "psi_file", "file": "drawing.pdf", "locator": "p1", "quote": "x"}
    assert cd.psi_file_issue("s", src, "PSI-1", FakeContext())["message"] == "drawing.pdf has no extracted text"


def test_render_skips_empty_sections_and_truncates_quotes():
    r = record(physics={"text": None, "sources": []}, limitations=[{"text": None, "sources": []}])
    r["findings"][0]["sources"] = [{"type": "psi_file", "file": "doc.pdf", "locator": "p2", "quote": "word " * 100}]
    page = rd.render(r)
    assert "## Physics" not in page and "## Limitations" not in page
    assert "## Findings" in page and "*(result)*" in page
    quote_line = next(l for l in page.splitlines() if "doc.pdf" in l)
    assert len(quote_line) < 360 and quote_line.endswith("…*")
    assert "\n\n\n" not in page


PSI_26 = psi.DIGEST / "PSI-26.json"


@pytest.mark.skipif(not PSI_26.exists(), reason="PSI-26 record not present")
def test_render_psi_26_smoke():
    r = json.loads(PSI_26.read_text())
    page = rd.render(r, {"PSI-25": "PSI-25-bass-ii.md"})
    assert rd.page_name(r) == "PSI-26-bass.md"
    assert page.startswith("# PSI-26: BASS")
    for heading in ("At a glance", "Question", "Physics", "Method", "Test matrix", "Measurements",
                    "Findings", "Fire-safety relevance", "Limitations", "Data in PSI", "Related investigations",
                    "Open questions", "Dashboard ideas", "Gaps and data-quality notes"):
        assert f"\n## {heading}\n" in page
    assert f"\n{len(r['findings'])}. " in page
    assert "[PSI-25](PSI-25-bass-ii.md)" in page
    assert '"type"' not in page and "{'" not in page
