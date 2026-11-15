import copy

import pytest

from fif import api, psi
from fif.pipeline import check_publications as cp

pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "tests.parquet").exists(), reason="processed tables not built")


def reviews(acc):
    return copy.deepcopy(api.publication_reviews(acc))


def messages(issues):
    return [f"{i['path']}: {i['message']}" for i in issues]


def test_every_publication_file_passes_the_check():
    assert cp.main([]) == 0


def test_check_reports_a_missing_entry_and_a_misplaced_one():
    entries = reviews("PSI-25")
    entries[0], entries[1] = entries[1], entries[0]
    out = messages(cp.check("PSI-25", entries[:-1]))
    assert out[0] == ": 16 entries for 17 publications in the record"
    assert any(m.startswith("[0]: is ") for m in out) and any(m.startswith("[1]: is ") for m in out)


def test_check_reports_bad_enums_and_unquoted_items():
    entries = reviews("PSI-107")
    entry = entries[8]
    entry["access"] = "paywalled"
    entry["classification"].append("interesting")
    entry["items"][0]["quote"] = " "
    entry["items"].append({"kind": "out_of_scope", "claim": "Not about fire.", "quote": None, "locator": None,
                           "record_path": None})
    out = messages(cp.check("PSI-107", entries))
    assert "[8]: access 'paywalled' is not one of ['full_text', 'abstract', 'none']" in out
    assert any(m.startswith("[8]: classification 'interesting'") for m in out)
    assert f"[8].items[0]: {entry['items'][0]['kind']} item has no quote" in out
    assert not any(m.startswith(f"[8].items[{len(entry['items']) - 1}]") for m in out)


def test_check_rejects_a_doi_the_record_does_not_give():
    entries = reviews("PSI-68")
    assert api.get_investigation("PSI-68")["data"]["publications"][1]["doi"] is None
    entries[1]["doi"] = "10.1016/j.proci.2014.06.043"
    assert any(m.startswith("[1]: doi ") for m in messages(cp.check("PSI-68", entries)))


def test_a_publication_carries_its_review_and_the_investigation_the_counts():
    data = api.get_investigation("PSI-107")["data"]
    pub = data["publications"][8]
    assert pub["title"] == "Laminar smoke points of coflowing flames in microgravity"
    review = pub["review"]
    assert set(review) == {"access", "read_url", "classification", "summary", "items", "notes"}
    assert review["access"] == "full_text" and "contradicts_psi_data" in review["classification"]
    assert all(i["quote"] and i["locator"] for i in review["items"] if i["kind"] not in ("out_of_scope", "unreadable"))
    counts = data["publication_review"]
    assert counts["n_publications"] == counts["n_reviewed"] == len(data["publications"]) == 9
    assert sum(counts["by_access"].values()) == 9
    assert counts["by_classification"]["contradicts_psi_data"] == sum(
        "contradicts_psi_data" in p["review"]["classification"] for p in data["publications"])
    assert any("AI model's reading" in n for n in api.get_investigation("PSI-107")["notes"])


def test_a_review_that_does_not_name_the_publication_is_not_attached(monkeypatch):
    entries = reviews("PSI-25")
    entries[0]["title"], entries[0]["doi"] = "Some other paper on flames", None
    monkeypatch.setattr(api, "publication_reviews", lambda acc: entries if acc == "PSI-25" else [])
    pubs = api.get_investigation("PSI-25")["data"]["publications"]
    assert pubs[0]["review"] is None and pubs[1]["review"] is not None


def test_same_publication_tolerates_entities_and_trailing_text():
    assert api.same_publication({"title": "A Researcher&#x27;s Guide to the ISS", "doi": None},
                                {"title": "A Researcher's Guide to the ISS", "doi": None})
    assert api.same_publication({"title": "Soot Formation in Normal and Microgravity Conditions (2022)", "doi": None},
                                {"title": "Soot Formation in Normal and Microgravity Conditions", "doi": None})
    assert not api.same_publication({"title": "Soot Formation in Normal Gravity", "doi": None},
                                    {"title": "Soot", "doi": None})


def test_discrepancies_lists_a_paper_disagreeing_with_psi():
    result = api.discrepancies("PSI-69")
    found = result["data"]["source_disagreements"]
    assert found and all(d["kind"] == "published_paper_disagrees_with_psi" and d["accession"] == "PSI-69" for d in found)
    first = found[0]
    assert first["quote"] and first["locator"] and first["claim"] and first["read_url"].startswith("https://")
    assert any("not applied" in n for n in result["notes"])
    assert not api.discrepancies("PSI-25")["data"]["source_disagreements"]
    every = api.discrepancies()["data"]["source_disagreements"]
    n_items = sum(i["kind"] == "contradicts_psi_data" for acc in api.records()
                  for e in api.publication_reviews(acc) for i in e["items"])
    assert len(every) == n_items
    assert api.discrepancies(test_id="22024M1")["data"]["source_disagreements"] == []
