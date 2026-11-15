"""`investigations` table: one row per PSI accession, flattened from the API records.

Run: uv run python -m fif.pipeline.build_investigations
"""
from difflib import SequenceMatcher

import pandas as pd

from fif import psi


def _clean(text):
    return " ".join((text or "").split()) or None


def _people(rec):
    names = []
    for c in rec.get("contacts") or []:
        name = " ".join(x for x in (c.get("firstName"), c.get("lastName")) if x)
        if name:
            names.append(name)
    return "; ".join(names) or None


def _author_contacts(rec):
    """Author contact from the PSI record's structured contact block: name, affiliation, role, e-mail.

    An allowlist: the block's `address` is never emitted. Contact details found in document text are handled
    by `fif.pipeline.redact`.
    """
    out = []
    for c in rec.get("contacts") or []:
        name = " ".join(x for x in (c.get("firstName"), c.get("midInitials"), c.get("lastName")) if x)
        if not name:
            continue
        roles = [_clean(r.get("annotationValue")) for r in (c.get("roles") or [])]
        email = _clean(c.get("email"))
        out.append(
            {
                "name": name,
                "affiliation": _clean(c.get("affiliation")),
                "role": "; ".join(r for r in roles if r) or None,
                "email": email,
                "email_note": _email_doubt(email),
            }
        )
    return out or None


def _email_doubt(email):
    """The address is given as PSI prints it; a domain one or two letters away from nasa.gov is pointed out."""
    domain = (email or "").rpartition("@")[2].lower()
    if domain and not domain.endswith("nasa.gov") and SequenceMatcher(None, domain, "nasa.gov").ratio() >= 0.8:
        return "domain as printed in the PSI record; it looks like a misspelling of nasa.gov"
    return None


def _publications(pubs):
    """The record's publication list in its order, as printed (whitespace collapsed); a missing DOI stays None."""
    return [
        {
            "title": _clean(p.get("title")),
            "authors": _clean(p.get("authorList")),
            "doi": _clean(p.get("doi")),
            "status": _clean((p.get("status") or {}).get("annotationValue")),
        }
        for p in pubs
    ]


def build():
    rows = []
    for rec in psi.load_records():
        files = psi.manifest(rec)
        pubs = rec.get("publications") or []
        rows.append(
            {
                "accession": rec["accession"],
                "acronym": _clean(rec.get("investigationAcronym")),
                "title": _clean(rec.get("title")),
                "project_type": _clean(rec.get("projectType")),
                "sub_research_area": _clean(rec.get("subResearchArea")),
                "flight_program": _clean(rec.get("flightProgram")),
                "hardware": _clean(rec.get("experimentHardware")),
                "hardware_link": _clean(rec.get("experimentHardwareLink")),
                "start_date": _clean(rec.get("investigationStartDate")),
                "end_date": _clean(rec.get("investigationEndDate")),
                "managing_center": _clean(rec.get("managingNasaCenter")),
                "contacts": _people(rec),
                "author_contacts": _author_contacts(rec),
                "objective": _clean(rec.get("objective")),
                "approach": _clean(rec.get("approach")),
                "hypothesis": _clean(rec.get("hypothesis")),
                "research_impacts": _clean(rec.get("researchImpacts")),
                "description": _clean(rec.get("description")),
                "related_accessions": _clean(rec.get("related_glds")),
                "doi": _clean(rec.get("doi")),
                "license": _clean(rec.get("licenseIdentifier")),
                "n_publications": len(pubs),
                "publication_dois": "; ".join(p["doi"] for p in pubs if p.get("doi")) or None,
                "publications": _publications(pubs),
                "n_files": len(files),
                "total_gb": round(sum(float(f.get("file_size") or 0) for f in files) / 1e9, 3),
                "source_url": f"https://psi.nasa.gov/physci/repo/data/investigations/{rec['accession']}",
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build()
    psi.write_table(df, "investigations")
    print(df[["accession", "acronym", "sub_research_area", "hardware", "n_publications", "n_files", "total_gb"]].to_string())
