"""Contact details in document text: a listed author's e-mail and phone stay, the rest is replaced by a marker.

Listed author = a person in the contact block of any PSI record. Everything removed leaves a visible
`[... removed]` marker so a reader can see the text was changed.
"""
import re
import unicodedata
from functools import lru_cache

from fif import psi

# Holds an account/password row in its header; no text of this file is extracted.
WITHHELD = frozenset({("PSI-26", "PSI-26_Science Documents_Planned_Test Matrix.xlsx")})

EMAIL_GONE = "[e-mail removed]"
PHONE_GONE = "[phone removed]"
ADDRESS_GONE = "[address removed]"
IP_GONE = "[ip removed]"

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
# The last separator must be "-" or ".": runs of space-separated digits are axis ticks and table cells.
# A 7-digit number counts only right after a name's initial ("Wolf, S. 555-0100"); elsewhere it is a range.
PHONE = re.compile(
    r"(?<![\w.(])(?:\+?1[\s.-])?(?:\(\d{3}\)\s?|\d{3}[\s.-]{1,2})\d{3}[.-]\d{4}(?!\w)"
    r"|(?<=[A-Z]\.\s)\d{3}-\d{4}(?![\w-])"
)
# 10.x.x.x is left alone: it is indistinguishable from section numbers.
PRIVATE_IP = re.compile(r"(?<![\d.])(?:192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}(?![\d.])")
STREET = re.compile(
    r"\b\d{1,5} (?:[A-Z][\w.']*\s){1,4}(?<!Hard )(?<!Disk )"
    r"(?:Street|St\.|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Drive|Lane|Parkway|Pkwy\.?|Way|Circle|Court|Highway|Hwy\.?)"
    r"(?![a-z])"
)
PO_BOX = re.compile(r"\bP\.?\s?O\.? Box \d+", re.I)
CITY_STATE_ZIP = re.compile(
    r"\b[A-Z][a-z.]+(?: [A-Z][a-z]+)?, ?(?:[A-Z]{2}|[A-Z][a-z]+(?: [A-Z][a-z]+)?)\.? \d{5}(?:-\d{4})?\b"
    r"|\b[A-Z]{3,}, ?[A-Z]{2,} \d{5}(?:-\d{4})?\b"
)
# NASA Task Book contact block: labelled address fields.
LABELLED_ADDRESS = re.compile(
    r"(?<=PI Address \d: ).*?(?= PI Address \d:| PI Web Page:| City:)"
    r"|(?<=City: ).*? State: .*? Zip Code: [\d-]+"
)
GONE = re.compile(rf"{re.escape(EMAIL_GONE)}|{re.escape(PHONE_GONE)}")
MERGE = re.compile(rf"{re.escape(ADDRESS_GONE)}(?:[\s,]*{re.escape(ADDRESS_GONE)})+")

PHONE_OWNER_BEFORE = 200
PHONE_OWNER_AFTER = 60


def _fold(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()


def authors_from(records):
    """(e-mails, surnames, {initials: surname}) of everyone in the records' contact blocks."""
    emails, surnames, initials = set(), set(), {}
    for rec in records:
        for c in rec.get("contacts") or []:
            last = _fold(c.get("lastName") or "").strip()
            if not last:
                continue
            surnames.add(last)
            if c.get("email"):
                emails.add(c["email"].strip().lower())
            first, mid = _fold(c.get("firstName") or ""), _fold(c.get("midInitials") or "")
            if first:
                initials[first[0] + mid[:1] + last[0]] = last
    return frozenset(emails), frozenset(surnames), initials


@lru_cache(maxsize=1)
def listed_authors():
    return authors_from(psi.load_records())


def _has_surname(text, surname):
    return re.search(rf"(?<![a-z]){re.escape(surname)}(?![a-z])", text) is not None


def _is_author_email(address, folded_text, authors):
    emails, surnames, initials = authors
    address = address.lower()
    if address in emails:
        return True
    local = _fold(address.split("@")[0])
    if any(len(s) >= 4 and s in local for s in surnames):
        return True
    # rla@... next to "Axelbaum, Richard L."
    owner = initials.get(re.sub(r"[^a-z]", "", local))
    return owner is not None and _has_surname(folded_text, owner)


def redact(text, authors=None, context=None):
    """`context` is the page or sheet the text was cut from: an author named there owns their initials' e-mail."""
    authors = authors or listed_authors()
    folded = _fold(context or text)
    text = EMAIL.sub(lambda m: m.group() if _is_author_email(m.group(), folded, authors) else EMAIL_GONE, text)

    # A phone belongs to a listed author when it is the phone nearest to one of their e-mails, or when their
    # surname stands between the previous contact item and the phone. A name after the phone is the next person.
    phones = [m.span() for m in PHONE.finditer(text)]
    items = sorted(phones + [m.span() for m in EMAIL.finditer(text)] + [m.span() for m in GONE.finditer(text)])
    owned = set()
    for m in EMAIL.finditer(text):
        reach = [p for p in phones if m.start() - PHONE_OWNER_AFTER <= p[0] <= m.end() + PHONE_OWNER_BEFORE]
        if reach:
            owned.add(min(reach, key=lambda p: min(abs(p[0] - m.end()), abs(m.start() - p[1]))))

    def phone(m):
        span = m.span()
        if span in owned:
            return m.group()
        before = max([e for _, e in items if e <= span[0]] + [span[0] - PHONE_OWNER_BEFORE])
        near = _fold(text[before : span[0]])
        return m.group() if any(_has_surname(near, s) for s in authors[1]) else PHONE_GONE

    text = PHONE.sub(phone, text)
    text = PRIVATE_IP.sub(IP_GONE, text)
    # A labelled field without a number is a department name, not an address.
    text = LABELLED_ADDRESS.sub(lambda m: ADDRESS_GONE if re.search(r"\d", m.group()) else m.group(), text)
    for pattern in (STREET, PO_BOX, CITY_STATE_ZIP):
        text = pattern.sub(ADDRESS_GONE, text)
    return MERGE.sub(ADDRESS_GONE, text)
