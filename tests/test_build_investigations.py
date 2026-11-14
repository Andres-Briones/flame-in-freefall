"""Author-contact policy (decision 009): the record's structured contact block
may surface name, affiliation, role and institutional e-mail — and nothing else.
"""
from fif.pipeline.build_investigations import _author_contacts


def test_surfaces_professional_fields():
    rec = {
        "contacts": [
            {
                "firstName": "David",
                "midInitials": "L.",
                "lastName": "Urban",
                "affiliation": "NASA GRC",
                "email": "david.l.urban@nasa.gov",
                "roles": [{"annotationValue": "Principal Investigator (PI)"}],
            }
        ]
    }
    assert _author_contacts(rec) == [
        {
            "name": "David L. Urban",
            "affiliation": "NASA GRC",
            "role": "Principal Investigator (PI)",
            "email": "david.l.urban@nasa.gov",
            "email_note": None,
        }
    ]


def test_drops_phone_fax_and_address_even_if_present():
    # The allowlist must hold if PSI ever populates these in the record.
    rec = {
        "contacts": [
            {
                "firstName": "A",
                "lastName": "Author",
                "email": "a@example.gov",
                "phone": "+1-216-555-0100",
                "fax": "+1-216-555-0199",
                "address": "21000 Brookpark Rd, Cleveland OH",
            }
        ]
    }
    (entry,) = _author_contacts(rec)
    assert set(entry) == {"name", "affiliation", "role", "email", "email_note"}
    assert "+1-216-555-0100" not in str(entry)
    assert "Brookpark" not in str(entry)


def test_contact_without_a_name_is_skipped():
    assert _author_contacts({"contacts": [{"email": "orphan@example.gov"}]}) is None
    assert _author_contacts({}) is None


def test_a_misspelt_nasa_domain_is_pointed_out_not_changed():
    rec = {"contacts": [{"firstName": "A", "lastName": "Author", "email": "a.author@nasa.gv"}]}
    (entry,) = _author_contacts(rec)
    assert entry["email"] == "a.author@nasa.gv" and "misspelling of nasa.gov" in entry["email_note"]
    rec = {"contacts": [{"firstName": "A", "lastName": "Author", "email": "a.author@case.edu"}]}
    assert _author_contacts(rec)[0]["email_note"] is None
