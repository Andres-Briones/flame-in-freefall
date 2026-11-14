"""Contact details in document text: a listed author's e-mail and phone stay, everything else leaves a marker."""
import pandas as pd
import pytest

from fif import psi
from fif.pipeline import redact as R
from fif.pipeline.build_evidence import extract

RECORDS = [
    {
        "contacts": [
            {"firstName": "Ada", "midInitials": "M", "lastName": "Flamel", "email": "ada.flamel@nasa.example"},
            {"firstName": "Chung", "lastName": "Law", "email": None},
        ]
    }
]
AUTHORS = R.authors_from(RECORDS)


def redact(text):
    return R.redact(text, AUTHORS)


def test_listed_author_email_and_phone_are_kept():
    text = "Contact: Ada Flamel, ada.flamel@nasa.example, 216-555-0101."
    assert redact(text) == text


def test_author_email_is_recognised_by_surname_or_by_initials_next_to_the_name():
    assert redact("a.flamel@univ.example") == "a.flamel@univ.example"
    assert redact("PI: Flamel, Ada M. PI Email: amf@univ.example") == "PI: Flamel, Ada M. PI Email: amf@univ.example"
    assert redact("PI Email: amf@univ.example") == f"PI Email: {R.EMAIL_GONE}"
    page = "PI: Flamel, Ada M. ... PI Email: amf@univ.example Phone: 314 555-0100"
    assert R.redact(page[-48:], AUTHORS, context=page) == page[-48:]


def test_other_people_lose_email_and_phone():
    text = "Sphere manufacturer: J. Smith, jsmith@vendor.example, tel (508) 555-0199, fax 508.555.0188"
    assert redact(text) == (
        f"Sphere manufacturer: J. Smith, {R.EMAIL_GONE}, tel {R.PHONE_GONE}, fax {R.PHONE_GONE}"
    )


def test_phone_formats():
    assert redact("Bo Smith (256)555-0142 and +1 256.555.0143") == f"Bo Smith {R.PHONE_GONE} and {R.PHONE_GONE}"
    assert redact("CHAIRMAN Wolf, S. 555-0100 X Flamel, A. 555-0101 X") == (
        f"CHAIRMAN Wolf, S. {R.PHONE_GONE} X Flamel, A. 555-0101 X"
    )
    assert redact("a range of 500-1500 C at 100-2000 kPa") == "a range of 500-1500 C at 100-2000 kPa"


def test_phone_far_from_any_author_is_removed():
    text = "Ada Flamel wrote this. " + "x" * 300 + " Help desk 301-555-0123"
    assert redact(text).endswith(f"Help desk {R.PHONE_GONE}")


def test_short_surname_matches_whole_words_only():
    assert redact("Prof. Law, 609-555-0144") == "Prof. Law, 609-555-0144"
    assert redact("lawful flaw, 609-555-0144") == f"lawful flaw, {R.PHONE_GONE}"


def test_numbers_that_are_not_phones_are_untouched():
    text = "ticks 200 400 600 800 1000 1200; part 123-456-78901; ratio 0.123.456.7890; Eq. (4.6)"
    assert redact(text) == text


def test_postal_addresses_are_removed():
    assert redact("NASA Glenn, 21000 Brookpark Road, Cleveland, Ohio 44135, USA") == (
        f"NASA Glenn, {R.ADDRESS_GONE}, USA"
    )
    assert redact("P.O. Box 123 Hampton, VA 23681-2199") == R.ADDRESS_GONE
    assert redact("a 250 GB Hard Drive and 2 Disk Drive bays") == "a 250 GB Hard Drive and 2 Disk Drive bays"


def test_task_book_address_fields_are_removed():
    text = (
        "Organization Name: Some University PI Address 1: Department of Fire PI Address 2: 12 Jolley Hall "
        "PI Web Page: City: St. Louis State: MO Zip Code: 63130 Congressional District: 1"
    )
    assert redact(text) == (
        f"Organization Name: Some University PI Address 1: Department of Fire PI Address 2: {R.ADDRESS_GONE} "
        f"PI Web Page: City: {R.ADDRESS_GONE} Congressional District: 1"
    )


def test_private_network_addresses_are_removed_but_section_numbers_are_not():
    assert redact("Type: ftp 192.168.1.2 then see 10.2.3.1 and 172.20.0.9") == (
        f"Type: ftp {R.IP_GONE} then see 10.2.3.1 and {R.IP_GONE}"
    )


def test_withheld_file_yields_no_text():
    (accession, file_name), = R.WITHHELD
    chunks, info = extract(
        {"accession": accession, "category": "Science Documents", "file_name": file_name, "extension": ".xlsx",
         "local_path": "does/not/matter.xlsx"}
    )
    assert chunks == [] and info["status"] == "withheld"


@pytest.fixture(scope="module")
def evidence():
    path = psi.PROCESSED / "evidence.parquet"
    if not path.exists():
        pytest.skip("evidence table not built")
    return pd.read_parquet(path)


def test_built_evidence_holds_no_unlisted_contact_details(evidence):
    authors = R.listed_authors()
    for _, page in evidence.groupby(["accession", "file_name", "locator"], sort=False)["text"]:
        context = " ".join(page)
        for text in page:
            assert R.redact(text, authors, context=context) == text
    assert not evidence[["accession", "file_name"]].apply(tuple, axis=1).isin(R.WITHHELD).any()


def test_phone_goes_to_the_nearest_person_not_to_an_author_listed_next_to_them():
    text = (
        "Dr. Ada Flamel, Cleveland; (216) 555-0101; ada.flamel@nasa.example "
        "Project Manager: Bo Smith, Cleveland; (216) 555-0102; bo.smith@nasa.example"
    )
    assert redact(text) == (
        "Dr. Ada Flamel, Cleveland; (216) 555-0101; ada.flamel@nasa.example "
        f"Project Manager: Bo Smith, Cleveland; {R.PHONE_GONE}; {R.EMAIL_GONE}"
    )
