"""`tests` table: one row per test, test day or planned condition set, unified from the
PSI "Experimental table" CSVs (one adapter per file), with three richer per-test sources
replacing or enriching their table (PSI-26 as-run matrix, PSI-39 data-summary spreadsheet,
PSI-107 master run log) and the corrections documented in the digest records
(data/digest/PSI-*.json). A corrected value keeps its source value in `extra`
(`<column>_original`) and every correction or doubt is listed in `flags`.
Column and flag reference: docs/tests-table.md.

Run: uv run python -m fif.pipeline.build_tests
"""
import json
import re
import warnings
from collections import Counter
from datetime import date, datetime, time, timedelta

import openpyxl
import pandas as pd
import xlrd

from fif import psi

ATM_KPA = 101.325
BAR_KPA = 100.0
MMHG_KPA = 101.325 / 760

COLUMNS = [
    "accession", "acronym", "test_id", "row_kind", "date",
    "fuel", "fuel_raw", "fuel_phase", "fuel_fraction", "config", "geometry",
    "x_o2_ambient", "x_o2_burner", "x_o2_min", "x_o2_max", "x_o2", "diluent", "pressure_kpa", "flow_cm_s", "gravity",
    "n_flames", "ignited", "burn_time_s", "extinction_mode", "outcome", "outcome_cause", "outcome_action",
    "outcome_setting", "outcome_quote",
    "t_ad_k", "peak_temp_c", "d0_mm", "ext_diameter_mm", "burn_rate_k_mm2_s", "n_reignitions", "cool_flame",
    "spread_rate_mm_s", "burn_length_cm", "flame_length_mm", "at_smoke_point", "smoke_point_reviewed", "measurement",
    "flags", "extra", "source_file", "source_row",
]
NUMERIC = [
    "fuel_fraction", "x_o2_ambient", "x_o2_burner", "x_o2_min", "x_o2_max", "x_o2", "pressure_kpa", "flow_cm_s",
    "n_flames", "burn_time_s", "t_ad_k", "peak_temp_c",
    "d0_mm", "ext_diameter_mm", "burn_rate_k_mm2_s", "n_reignitions", "spread_rate_mm_s", "burn_length_cm",
    "flame_length_mm",
]
BOOLEAN = ["ignited", "cool_flame", "at_smoke_point", "smoke_point_reviewed"]

FUELS = [
    (r"\bc2h4\b|ethylene", "ethylene"),
    (r"\bch4\b|methane", "methane"),
    (r"\bc3h8\b|propane", "propane"),
    (r"\bc4h10\b|butane", "butane"),
    (r"\bc2h6\b|\bethane\b", "ethane"),
    (r"\bc3h6\b|propylene", "propylene"),
    (r"\bh2\b|hydrogen", "hydrogen"),
    (r"methanol", "methanol"),
    (r"\bethanol", "ethanol"),
    (r"propanol", "propanol"),
    (r"glycerol", "glycerol"),
    (r"(?<!iso)(?<!iso-)\b(n-)?heptane", "n-heptane"),
    (r"iso-?octane", "isooctane"),
    (r"\b(n-)?octane\b", "n-octane"),
    (r"\b(n-)?decane\b", "n-decane"),
    (r"\bc12h26\b|(?<!iso-)(?<!iso)\b(n-)?dodecane", "n-dodecane"),
    (r"iso-?dodecane", "isododecane"),
    (r"pmma", "pmma"),
    (r"sibal", "sibal fabric"),
    (r"kapton", "kapton"),
    (r"teflon", "teflon"),
    (r"silicone", "silicone"),
    (r"lampwick", "lampwick"),
    (r"pyrell", "pyrell"),
    (r"nomex", "nomex"),
    (r"ultem", "ultem"),
    (r"par+af+in", "paraffin wax"),
    (r"japan wax", "japan wax"),
    (r"dibutyl phthalate", "dibutyl phthalate"),
    (r"farnesane", "farnesane"),
    (r"arizona road dust", "arizona road dust"),
]
LIQUIDS = {
    "methanol", "ethanol", "propanol", "glycerol", "n-heptane", "isooctane", "n-octane",
    "n-decane", "n-dodecane", "isododecane", "dibutyl phthalate", "farnesane",
}
EXTINCTION = {
    "se": "self_extinguished",
    "ft": "flow_terminated",
    "extinction": "extinction",
    "disruption": "disruption",
    "completion": "completion",
}
NUMBER = r"-?\d*\.?\d+(?:[eE]-?\d+)?"


def clean(value):
    return " ".join(str(value).split()) or None if value is not None else None


def num(text):
    """A plain or approximate ("~ 21.5") number, else None."""
    s = clean(text)
    m = re.fullmatch(rf"~?\s*({NUMBER})", s) if s else None
    return float(m.group(1)) if m else None


def qty(text, unit):
    """A number followed by `unit` ("20 cm/s"), else None."""
    s = clean(text)
    m = re.fullmatch(rf"~?\s*({NUMBER})\s*{re.escape(unit)}", s, re.I) if s else None
    return float(m.group(1)) if m else None


def fractions(text):
    """All standalone numbers in a list/range cell as fractions; percent values (>1) are divided by 100."""
    values = [float(v) for v in re.findall(r"(?<![\w.])(\d*\.?\d+)(?![\w.])", clean(text) or "")]
    return [v / 100 if v > 1 else v for v in values]


def percent(text):
    m = re.search(r"(\d*\.?\d+)\s*%", text or "")
    return float(m.group(1)) / 100 if m else None


def yyddd(text):
    """ACME YYDDD day code (optionally followed by a test letter/number) to an ISO date."""
    m = re.match(r"\s*(\d{2})(\d{3})(?!\d)", str(text or ""))
    if not m or not 1 <= int(m.group(2)) <= 366:
        return None
    d = date(2000 + int(m.group(1)), 1, 1) + timedelta(int(m.group(2)) - 1)
    return d.isoformat() if d.year == 2000 + int(m.group(1)) else None


def parse_date(text, *formats):
    for fmt in formats:
        try:
            d = datetime.strptime(clean(text) or "", fmt).date()
        except ValueError:
            continue
        return d.isoformat() if d <= date.today() else None
    return None


def fuel_name(text):
    s = (text or "").lower()
    hits = sorted((m.start(), name) for pattern, name in FUELS for m in [re.search(pattern, s)] if m)
    names = list(dict.fromkeys(name for _, name in hits))
    return "/".join(names) or None


def phase(fuel, default):
    return "liquid" if fuel and all(f in LIQUIDS for f in fuel.split("/")) else default


def o2_fields(values):
    if not values:
        return {}
    lo, hi = min(values), max(values)
    return {"x_o2_min": lo, "x_o2_max": hi, "x_o2": lo if lo == hi else None}


def diluent(parts):
    names = [name for name, share in parts if share]
    return names[0] if len(names) == 1 else "mix" if names else None


class Src:
    """Source row; reading a column with `take`/`num`/... marks it as captured, the rest goes to `extra`."""

    def __init__(self, cells):
        self.cells = cells
        self.used = set()

    def get(self, col):
        return clean(self.cells.get(col))

    def take(self, col):
        self.used.add(col)
        return self.get(col)

    def _parsed(self, col, value, scale=1.0):
        if value is None:
            return None
        if not (self.get(col) or "").startswith("~"):
            self.used.add(col)
        return value * scale

    def num(self, col, scale=1.0):
        return self._parsed(col, num(self.get(col)), scale)

    def qty(self, col, unit, scale=1.0):
        return self._parsed(col, qty(self.get(col), unit), scale)

    def o2(self, col, values=None):
        values = fractions(self.get(col)) if values is None else values
        if len(values) == 1 and not (self.get(col) or "").startswith("~"):
            self.used.add(col)
        return o2_fields(values)

    def yes_no(self, col):
        value = {"yes": True, "no": False}.get((self.get(col) or "").lower())
        return self._parsed(col, value) if value is not None else None

    def mode(self, col):
        value = EXTINCTION.get((self.get(col) or "").lower())
        if value:
            self.used.add(col)
        return value

    def extra(self):
        return {c: v for c, v in self.cells.items() if c not in self.used and clean(v)}


def flame_design_normal(r):
    tid, fuel_raw = r.take("Test"), r.take("Fuel")
    return {
        "test_id": tid, "row_kind": "test", "date": yyddd(tid), "_group": r.get("Day"),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": r.num("Xfuel"), "config": r.take("Flame Type").lower(),
        **r.o2("XO2 (init)"), "pressure_kpa": r.num("pinit (atm)", ATM_KPA), "t_ad_k": r.num("Tad (K)"),
    }


def flame_design_inverse(r):
    tid = r.take("Test")
    return {
        "test_id": tid, "row_kind": "test", "date": yyddd(tid), "_group": r.get("Day"),
        "fuel": "ethylene", "fuel_raw": "C2H4", "fuel_phase": "gas",
        "fuel_fraction": r.num("XC2H4 initial"), "config": r.take("Flame Type").lower(),
        **r.o2("XO2"), "pressure_kpa": r.num("pinit (atm)", ATM_KPA), "t_ad_k": r.num("Tad (K)"),
    }


def _cfig(r, o2_col, fuel_fraction_col, peak_col):
    tid, fuel_raw = r.take("Test"), r.take("Fuel")
    return {
        "test_id": tid, "row_kind": "test", "date": yyddd(tid), "_group": r.get("Day"),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": r.num(fuel_fraction_col), "config": r.take("Flame Type").lower(),
        **r.o2(o2_col), "pressure_kpa": r.num("approx p (bar)", BAR_KPA),
        "ignited": r.yes_no("Hot ignition"), "burn_time_s": r.num("burn time (sec)"),
        "extinction_mode": r.mode("Self-ext or flow term") or r.mode("Self -ext or flow term"),
        "t_ad_k": r.num("Tad (K)"), "peak_temp_c": r.num(peak_col),
    }


def cfig_normal(r):
    return _cfig(r, "XO2 before test", "Xf", "Peak burner T (C )")


def cfig_inverse(r):
    return _cfig(r, "XO2", "Xf before test", "Peak burner Temp (C)")


def bre(r):
    raw_o2 = r.get("Oxygen Conc (percent)")
    excel_percent = re.fullmatch(r"(\d+)00%", raw_o2 or "")
    o2 = [float(excel_percent.group(1)) / 100] if excel_percent else fractions(raw_o2)
    when = f"{r.take('Year')} {r.take('Month')[:3]} {r.take('Date')}"
    fuel_raw = r.take("Fuel Bottle")
    return {
        "row_kind": "test_day", "date": parse_date(when, "%Y %b %d"),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas", "fuel_fraction": percent(fuel_raw),
        "geometry": f"{r.take('Burner Size (mm)')} mm porous burner", **o2_fields(o2), "diluent": "n2",
        "n_flames": r.num("Flames Ignited"),
    }


def cld(r):
    day, fuel_raw = r.take("Test Day"), r.take("Fuel Bottle")
    conc = fractions(r.get("Fuel conc. Range"))
    return {
        "test_id": day, "row_kind": "test_day", "date": yyddd(day),
        "fuel": "methane" if re.search(r"\bCH\d", fuel_raw) else "ethylene", "fuel_raw": fuel_raw,
        "fuel_phase": "gas", "fuel_fraction": conc[0] if len(conc) == 1 and r.take("Fuel conc. Range") else None,
        "config": "coflow", "n_flames": r.num("Flames ignited"),
    }


def efield(r):
    day, fuel_raw = r.take("Test Day"), r.take("Fuel Bottle")
    for col in ("Year", "Month", "Date"):
        r.take(col)
    burner = re.search(r"with (.+)$", r.get("Test Type") or "")
    conc = fractions(r.get("Fuel Conc"))
    return {
        "test_id": day, "row_kind": "test_day", "date": yyddd(day),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": conc[0] if len(conc) == 1 and r.take("Fuel Conc") else None,
        "config": burner.group(1) if burner else None, "n_flames": r.num("Flames Ignited"),
    }


def s_flame(r):
    day, fuel_raw, atmosphere = r.take("Test Day*"), r.take("Fuel Bottle"), r.get("Atmosphere*")
    blended = re.search(r"with\s+(CH4|C2H4|H2)\b", fuel_raw)
    inert = re.search(r"\bwith (He|N\d)\b", atmosphere)
    for col in ("Year", "Month", "Date"):
        r.take(col)
    return {
        "test_id": day, "row_kind": "test_day", "date": yyddd(day),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": 1.0 if blended else sum(fractions(fuel_raw)),
        **r.o2("Atmosphere*"),
        "diluent": ("he" if inert.group(1) == "He" else "n2") if inert else None,
        "n_flames": r.num("Flames Ignited*"),
    }


def _checked_date(r, text, formats):
    """Explicit date, kept only when it agrees with the table's GMT day-of-year column."""
    iso = parse_date(text, *formats)
    gmt = num(r.get("GMT"))
    if iso and gmt is not None and date.fromisoformat(iso).timetuple().tm_yday != gmt:
        return None
    return iso


def bass2(r):
    material = r.take("Fuel Sample Material")
    iso = _checked_date(r, r.get("Date"), ["%m/%d/%Y"])
    if iso:
        r.take("Date")
        r.take("GMT")
    return {
        "test_id": r.take("Test #"), "row_kind": "test", "date": iso,
        "fuel": fuel_name(material), "fuel_raw": material, "fuel_phase": "solid", "geometry": material,
        **r.o2("Calibrated initial O2 % by vol", [v / 100 for v in [num(r.get("Calibrated initial O2 % by vol"))] if v]),
    }


def bass(r):
    material = r.take("Fuel Sample Material")
    if not r.get("Test #") and not r.get("As Run Test #"):
        return None
    iso = _checked_date(r, r.get("Date"), ["%m/%d/%Y"])
    if iso:
        r.take("Date")
        r.take("GMT")
    return {
        "test_id": r.take("Test #"), "row_kind": "test", "date": iso,
        "fuel": fuel_name(material), "fuel_raw": material, "fuel_phase": "solid", "geometry": material,
        "config": "opposed flow" if re.search(r"op+o?s+ed", material.lower()) else None,
    }


def cfi(r):
    fuel_raw, fiber = r.take("Fuel"), r.take("Fiber")
    fuel = fuel_name(fuel_raw)
    return {
        "test_id": r.take("Flex Number"), "row_kind": "test", "date": parse_date(r.take("Test Date"), "%d-%b-%y"),
        "fuel": fuel, "fuel_raw": fuel_raw, "fuel_phase": phase(fuel, "liquid"),
        "config": {"Yes": "fiber-supported droplet", "No": "free droplet"}.get(fiber, "droplet"),
        **r.o2("Oxygen"), "diluent": diluent([("n2", num(r.get("Nitrogen"))), ("he", num(r.get("Helium")))]),
        "pressure_kpa": r.qty("Pressure", "atm", ATM_KPA),
    }


def daft(r):
    day = re.fullmatch(r"GMT (\d+) \((\d{4})\)", r.get("Actual Day") or "")
    iso = (date(int(day.group(2)), 1, 1) + timedelta(int(day.group(1)) - 1)).isoformat() if day else None
    if iso:
        r.take("Actual Day")
    material = r.take("Sample Material")
    return {
        "test_id": r.take("Session Name"), "row_kind": "condition_set", "date": iso,
        "fuel": fuel_name(material), "fuel_raw": material, "fuel_phase": "aerosol",
    }


def flex2(r):
    fuel_raw = r.take("Sample (Fuel Type)")
    fuel = fuel_name(fuel_raw)
    gas = r.get("Ambient Gas Mixture") or ""
    return {
        "row_kind": "condition_set", "fuel": fuel, "fuel_raw": fuel_raw, "fuel_phase": phase(fuel, "liquid"),
        "config": "droplet", "geometry": f"droplet d0 {r.take('Initial Droplet Diameter (mm)')} mm",
        **r.o2("Oxygen Mole Fraction"),
        "diluent": " or ".join(d.lower() for d in re.findall(r"O2/(\w+)", gas)) or None,
        "pressure_kpa": r.num("Ambient Pressure (atm)", ATM_KPA), "flow_cm_s": r.num("Flow Velocity (cm/s)"),
    }


def flex(r):
    fuel_raw = r.take("Fuel")
    fuel = fuel_name(fuel_raw)
    pressure = num(r.get("Ambient pressure; mmHg"))
    d0 = num(r.get("Droplet initial diameter; mm"))
    shares = [(name, num(r.get(f"{col} initial ambient composition; mole fraction")))
              for name, col in (("n2", "N"), ("co2", "CO"), ("he", "He"))]
    return {
        "test_id": r.take("FLEX Identifier"), "row_kind": "test", "date": parse_date(r.take("Test Date"), "%m/%d/%Y", "%m/%d/%y"),
        "fuel": fuel, "fuel_raw": fuel_raw, "fuel_phase": phase(fuel, "liquid"),
        "config": "droplet", "geometry": f"droplet d0 {d0:g} mm" if d0 is not None else None,
        **r.o2("O initial ambient composition; mole fraction"), "diluent": diluent(shares),
        "pressure_kpa": r.num("Ambient pressure; mmHg", MMHG_KPA) if pressure else None,
        "burn_time_s": r.num("Burn time; s"), "extinction_mode": r.mode("Test end"),
        "d0_mm": r.num("Droplet initial diameter; mm"), "ext_diameter_mm": r.num("Visible flame extinction diameter; mm"),
        "burn_rate_k_mm2_s": r.num("Burning rate; mm"),
    }


def _with_unit(value, col):
    unit = re.search(r"\((\w+)\)$", col)
    return f"{value} {unit.group(1)}" if unit and num(value) is not None else value


def _saffire(r, thickness, length, width, flow, o2, burn, direction, burn_length=None, spread=None):
    material = r.take("Material")
    if not any(r.get(c) for c in (flow, o2, burn)):
        return None
    geometry = ", ".join(
        f"{k} {_with_unit(r.take(c), c)}" for k, c in (("thickness", thickness), ("length", length), ("width", width)) if r.get(c)
    )
    fuel = fuel_name(material)
    raw_o2 = r.get(o2) or ""
    o2_initial = re.split(r"\s+to\s+", raw_o2)[0]
    return {
        "test_id": r.take("Sample Number"), "row_kind": "test",
        "fuel": fuel, "fuel_raw": material, "fuel_phase": phase(fuel, "solid"), "geometry": geometry or None,
        "config": f"{r.take(direction).lower()} flow" if r.get(direction) else None,
        **o2_fields(fractions(o2_initial)),
        "flow_cm_s": r.num(flow) if num(r.get(flow)) is not None else r.qty(flow, "cm/s"),
        "burn_time_s": r.num(burn) if num(r.get(burn)) is not None else r.qty(burn, "s"),
        "burn_length_cm": (r.num(burn_length) if num(r.get(burn_length)) is not None else r.qty(burn_length, "cm"))
        if burn_length else None,
        "spread_rate_mm_s": r.qty(spread, "mm/s") if spread else None,
    }


def saffire1(r):
    return _saffire(r, "Sample Thickness (cm)", "Sample Length (cm)", "Sample Width (cm)", "Air Flow (cm/s)",
                    "Percent O2", "Burn Time (s)", "Flow Direction")


def saffire2(r):
    # '?-g' is 'µ-g' with the µ lost; the 'Spread Length' column holds spread rates in mm/s (PSI-99 record).
    return _saffire(r, "Samle Thickness", "Sample Length", "Sample Width (cm)", "Air Flow (cm/s)",
                    "Percent O2 (Note 1)", "Burn Time (s)", "Flow Direction", "?-g Burn Length", "?-g Spread Length")


def saffire3(r):
    return _saffire(r, "Sample Thickness", "Sample Length", "Sample Width", "Air Flow", None, None, "Direction")


def same_r(r):
    material = r.take("Sample Type")
    return {
        "test_id": r.take("SAME Test #"), "row_kind": "test",
        "fuel": fuel_name(material), "fuel_raw": material, "fuel_phase": "solid",
        "flow_cm_s": r.num("Inlet velocity (cm/s)"),
    }


def same(r):
    material = r.take("Sample Material")
    fuel = fuel_name(material)
    return {
        "test_id": r.take("Sample #"), "row_kind": "condition_set" if "same conditions" in material else "test",
        "fuel": fuel, "fuel_raw": material, "fuel_phase": phase(fuel, "solid"),
        "flow_cm_s": r.num("Air Flow (cm/s)"),
    }


def slice_(r):
    when, fuel_raw = r.get("Test Date"), r.take("Fuel Type")
    m = re.match(r"(\d{4}-[A-Z]{3}-\d{2})\s*(.*)$", when)
    if m and not m.group(2):
        r.take("Test Date")
    return {
        "row_kind": "test_day", "date": parse_date(m.group(1).title(), "%Y-%b-%d") if m else None,
        "fuel": fuel_name(f"{m.group(2) if m else ''} {fuel_raw}"), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": percent(fuel_raw),
    }


def spice(r):
    fuel_raw = r.take("Fuel")
    return {
        "row_kind": "test", "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas",
        "fuel_fraction": percent(fuel_raw), "geometry": f"nozzle {r.take('Nozzle (mm)')} mm",
        "flow_cm_s": r.num("Air Rate (cm/s)"),
    }


ADAPTERS = {
    "Flame Design_Normal Flame": flame_design_normal,
    "Flame Design_Inverse Flame": flame_design_inverse,
    "ACME BRE": bre,
    "CLD Flame": cld,
    "E-FIELD": efield,
    "s-Flame": s_flame,
    "BASS-II": bass2,
    "table_BASS.csv": bass,
    "table_CFI.csv": cfi,
    "DAFT": daft,
    "Flex2": flex2,
    "FLEX.csv": flex,
    "SAFFIRE-1": saffire1,
    "SAFFIRE-2": saffire2,
    "SAFFIRE-3": saffire3,
    "SAME-R": same_r,
    "SAME.csv": same,
    "Slice": slice_,
    "Spice": spice,
    "CFI-G_Normal": cfig_normal,
    "CFI-G_Inverse": cfig_inverse,
    "Data Summary Table": None,
}


def table_paths():
    return sorted((psi.RAW / "files").glob("PSI-*/Experimental table/*.csv"))


def adapter_for(path):
    keys = [k for k in ADAPTERS if k in path.name]
    if len(keys) != 1:
        raise KeyError(f"{path.name}: matches adapters {keys}")
    return ADAPTERS[keys[0]]


def read_rows(path):
    """(1-based row number, cells) for non-blank rows; a row with a blank first cell continues the previous one."""
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="cp1252")
    df.columns = [" ".join(c.split()) for c in df.columns]
    rows = []
    for i, cells in enumerate(df.to_dict("records"), start=1):
        cells = {c: clean(v) for c, v in cells.items()}
        if not any(cells.values()):
            continue
        if rows and not cells[df.columns[0]]:
            prev = rows[-1][1]
            for c, v in cells.items():
                if v:
                    prev[c] = f"{prev[c]}; {v}" if prev[c] else v
            continue
        rows.append((i, cells))
    return rows


def _drop_odd_dates(rows):
    """Null a test-id date that disagrees with the rest of its table 'Day' group (a typo in the id)."""
    groups = {}
    for row in rows:
        if row.get("_group") and row["date"]:
            groups.setdefault(row["_group"], Counter())[row["date"]] += 1
    for row in rows:
        group = groups.get(row.pop("_group", None))
        if group and row["date"] != group.most_common(1)[0][0]:
            row["date"] = None


def rel(path):
    return str(path.relative_to(psi.ROOT))


def new_row(fields, extra, path, i):
    acc = path.relative_to(psi.RAW / "files").parts[0]
    row = dict.fromkeys(COLUMNS) | {"gravity": "micro"} | fields
    return row | {
        "accession": acc, "test_id": row["test_id"] or f"{acc}-r{i}",
        "flags": [], "extra": extra, "source_file": rel(path), "source_row": i,
    }


def table_rows(path, adapter=None):
    rows = []
    for i, cells in read_rows(path):
        src = Src(cells)
        fields = (adapter or adapter_for(path))(src)
        if fields is not None:
            rows.append(new_row(fields, src.extra(), path, i))
    _drop_odd_dates(rows)
    return rows


def flag(row, *codes):
    row["flags"] += [c for c in codes if c not in row["flags"]]


def correct(row, col, value, *codes):
    """Replace a value, keeping the source value in extra as `<col>_original`."""
    row["extra"].setdefault(f"{col}_original", row[col])
    row[col] = value
    flag(row, *codes)


def droplet_checks(row, gas_cols):
    """Flag droplet rows whose ambient mole fractions (x_o2 plus `gas_cols`, still in extra) do not sum to
    1 +/- 0.01, or whose extinction diameter is zero or larger than the initial diameter."""
    parts = [row["x_o2"]] + [num(row["extra"].get(c)) for c in gas_cols]
    if all(v is not None for v in parts) and abs(sum(parts) - 1) > 0.01 + 1e-9:
        flag(row, "composition_sum")
    ext, d0 = row["ext_diameter_mm"], row["d0_mm"]
    if ext is not None and d0 is not None and ext > d0:
        flag(row, "ext_gt_d0")
    if ext == 0:
        flag(row, "ext_zero")


# --- Spreadsheet sources that replace or enrich an experimental table ------------------------------

def cell_text(value):
    """A spreadsheet cell as the text a CSV export would hold."""
    if value is None or value != value:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return clean(str(value))


def read_sheet(path, sheet, header_row=1):
    """(Excel row number, {header: cell text}) for the non-blank rows below `header_row`."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # openpyxl drops embedded .wmf images with a warning
        ws = openpyxl.load_workbook(path, data_only=True, read_only=True)[sheet]
        values = list(ws.iter_rows(min_row=header_row, values_only=True))
    header = [" ".join(str(h).split()) if h is not None else None for h in values[0]]
    out = []
    for i, row in enumerate(values[1:], start=header_row + 1):
        cells = {h: cell_text(v) for h, v in zip(header, row) if h}
        if any(cells.values()):
            out.append((i, cells))
    return out


def science_doc(acc, name):
    return psi.RAW / "files" / acc / "Science Documents" / f"{acc}_Science Documents_{name}"


# PSI-26 BASS: the as-run matrix holds per-run cabin O2, pressure, fan/air and GN2 settings and crew notes
# that the 6-column experimental table drops. (Planned_Test Matrix.xlsx is deliberately not read: its
# header row holds account credentials, per the PSI-26 record.)
ASRUN_NOTES = "Test Observations and Anomalies (ignited, spread, extinguished, burn time, color, etc.)"
ASRUN_KEEP = {
    "Igniter": "asrun_igniter", "Flow restrictor": "asrun_flow_restrictor", "Sample distance": "asrun_sample_distance",
    "Fan display": "asrun_fan_display", "Air display": "asrun_air_display", "GN2 Pot": "asrun_gn2_pot",
    "GN2 display": "asrun_gn2_display", "O2 % by volume": "asrun_o2", "pressure, atm": "asrun_pressure_atm",
    "CO2, mm Hg": "asrun_co2_mmhg", ASRUN_NOTES: "asrun_notes",
}


def bass_asrun():
    path = science_doc("PSI-26", "As Run_Test Matrix.xlsx")
    runs = {}
    for sheet, header_row in (("2012", 3), ("2013", 2)):
        for i, cells in read_sheet(path, sheet, header_row):
            runs.setdefault((cells.get("As run test no."), cells.get("Test no.")), []).append((sheet, i, cells))
    return path, runs


def note_o2(notes):
    """Last O2 percentage quoted in an as-run note (e.g. 'final O2 is 17.3%'), as a fraction."""
    if not notes or not re.search(r"O2|vitiat", notes, re.I):
        return None
    values = [float(v) / 100 for v in re.findall(r"(\d{2}(?:\.\d+)?)\s*%", notes) if 14 <= float(v) <= 23]
    return values[-1] if values else None


def fix_bass(rows):
    path, runs = bass_asrun()
    previous = {}
    for row in rows:
        ex = row["extra"]
        date_conflict(row)
        infer_pmma(row, r"sphere", "PSI-26 record, samples: the spheres are PMMA (SRD p6, results overview p9)")
        matches = runs.get((ex.get("As Run Test #"), row["test_id"]), [])
        if len(matches) != 1:
            ex["asrun_match"] = f"{len(matches)} as-run rows for as-run/test no."
            flag(row, "needs_review")
            continue
        sheet, i, cells = matches[0]
        ex |= {"asrun_file": rel(path), "asrun_sheet": sheet, "asrun_row": i}
        ex |= {key: cells[col] for col, key in ASRUN_KEEP.items() if cells.get(col)}
        pressure, air = num(cells.get("pressure, atm")), cells.get("Air display")
        if pressure is not None:
            row["pressure_kpa"] = pressure * ATM_KPA
        if num(air) is not None:
            row["flow_cm_s"] = num(air)
        elif len(re.findall(r"\d*\.?\d+", air or "")) > 1:
            flag(row, "ramped")
        o2, notes, day = num(cells.get("O2 % by volume")), cells.get(ASRUN_NOTES), cells.get(next(iter(cells)))
        if sheet == "2013" and o2 is not None:
            # The 2013 'O2 % by volume' cell is sometimes the reading before GN2 vitiation (PSI-26 record).
            noted, before = note_o2(notes), previous.get(day)
            if noted is not None and abs(noted - o2) > 0.005:
                o2 = noted
                flag(row, "o2_from_notes")
            elif noted is None and o2 >= 0.20 and before is not None and before < 0.19 \
                    and not re.search(r"\bin air\b", notes or "", re.I):
                ex["asrun_o2_doubt"] = f"undiluted reading right after a run at {before:.3f} O2; notes give no value"
                o2 = None
                flag(row, "needs_review")
            if o2 is not None:
                previous[day] = o2
        if o2 is not None:
            row |= o2_fields([o2]) | {"x_o2_ambient": o2}
    return rows


def date_conflict(row):
    """The source has a date that could not be kept: unreadable, or not the day its GMT day-of-year column says."""
    if row["date"] is None and row["extra"].get("Date"):
        flag(row, "date_conflict")


def infer_pmma(row, pattern, source):
    """BASS / BASS-II sample labels that name only the shape; the investigators' documents give the material."""
    if row["fuel"] is None and re.search(pattern, row["fuel_raw"] or "", re.I):
        row["fuel"] = "pmma"
        row["extra"]["fuel_source"] = source
        flag(row, "fuel_inferred")


# PSI-39 CFI: the Jan 2021 data-summary spreadsheet (227 tests; D0, extinction diameters, k, re-ignitions,
# radiance, crew comments) supersedes the 87-row experimental table, which is a partial subset of it.
CFI_SUMMARY = "CFI_DataSummary_Spreadsheet_Jan2021.xlsx"
CFI_COMPARED = ["date", "fuel", "config", "x_o2", "diluent", "pressure_kpa"]


def cfi_summary(r):
    fuel_raw, fiber = r.take("Fuel"), r.take("Fiber")
    fuel = fuel_name(fuel_raw)
    k_cool, d_cool = num(r.get("kcool ( mm^2/s )")), num(r.get("Dext,cool ( mm )"))
    if num(r.get("Pressure (atm)")) == qty(r.get("Pressure"), "atm"):
        r.take("Pressure (atm)")
    return {
        "test_id": r.take("Flex Number"), "row_kind": "test", "date": parse_date(r.take("Test Date"), "%Y-%m-%d"),
        "fuel": fuel, "fuel_raw": fuel_raw, "fuel_phase": phase(fuel, "liquid"),
        "config": {"Yes": "fiber-supported droplet", "No": "free droplet"}.get(fiber, "droplet"),
        **r.o2("Oxygen"), "diluent": diluent([("n2", num(r.get("Nitrogen"))), ("he", num(r.get("Helium")))]),
        "pressure_kpa": r.qty("Pressure", "atm", ATM_KPA),
        "d0_mm": r.num("D0 ( mm )"), "ext_diameter_mm": r.num("Dext, hot ( mm )"),
        "burn_rate_k_mm2_s": r.num("khot ( mm^2/s )"), "n_reignitions": r.num("Reignitions"),
        "burn_time_s": r.num("HF Burn Time"),
        # Missing cool-flame data does not show there was no cool flame (comments often report one), so never False.
        "cool_flame": True if k_cool is not None or d_cool is not None or num(r.get("Extrap CF?")) == 1 else None,
    }


def cfi_rows():
    path = science_doc("PSI-39", CFI_SUMMARY)
    data = {c["Flex Number"]: c for _, c in read_sheet(path, "DATA")}
    comments = {c["Flex Number"]: c.get("Comments") for _, c in read_sheet(path, "Comments")}
    table_path = psi.RAW / "files" / "PSI-39" / "Experimental table" / "PSI-39_Experimental table_CFI.csv"
    table, seen = {}, set()
    for i, cells in read_rows(table_path):
        key = tuple(cells.items())
        if key in seen:  # FLEX-1285-1289 and 1295-1297 are listed twice, verbatim
            continue
        seen.add(key)
        table[cells["Flex Number"]] = (i, cfi(Src(cells)))
    rows = []
    for i, cells in read_sheet(path, "Master Sheet"):
        tid = cells["Flex Number"]
        merged = cells | {k: v for k, v in data.get(tid, {}).items() if k != "Flex Number"}
        if comments.get(tid):
            merged["Comments"] = comments[tid]
        src = Src(merged)
        row = new_row(cfi_summary(src), src.extra(), path, i)
        if tid in table:
            j, old = table.pop(tid)
            row["extra"]["experimental_table_row"] = j
            for col in CFI_COMPARED:
                if old.get(col) != row[col]:
                    row["extra"][f"experimental_table_{col}"] = old.get(col)
                    flag(row, "conflicts_with_table")
        rows.append(row)
    for tid, (j, old) in table.items():  # in the table only
        rows.append(new_row(old, {}, table_path, j))
    for row in rows:
        if row["test_id"] == "1411" and row["date"] == "2011-09-06":
            # CIR test point f249b10 is day 249 = 6 September; tests 1409 and 1410 ran on 2017-09-06
            row["extra"]["date_evidence"] = "CIR code f249b10 (day 249); FLEX-1409 and 1410 are dated 2017-09-06"
            correct(row, "date", "2017-09-06", "date_corrected")
        droplet_checks(row, ["Nitrogen", "Helium"])
    return rows


# PSI-107 SPICE: the master run log (526 rows) has the measured flame lengths, smoke flags and the GMT 062
# methane session that the 469-row experimental table drops.
SPICE_LOG = "PSI-107_Raw Data_Spice Flight Test Data II modified.xls"
SPICE_YEAR = 2009  # all twelve sessions, 14 Feb - 23 Jun 2009 (PSI-107 record)
AIR_INTERCEPT = -5.918  # the log converts u_a = 0.9402 * AIR - 5.918; a blank AIR cell leaves the intercept
ANEMOMETER_MIN_CM_S = 5.0
SPICE_TIMES = ("GMT ignition", "GMT Flame Off", "GMT data")


def day_time(value):
    """An Excel day fraction as hh:mm:ss; anything else as text."""
    if isinstance(value, float) and 0 <= value < 1:
        s = round(value * 86400)
        return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"
    return cell_text(value)


def spice_log(r, data_is_fraction):
    day = int(float(r.take("GMT date")))
    when = date(SPICE_YEAR, 1, 1) + timedelta(day - 1)
    if (r.get("Date") or "").upper() == f"{when:%b}-{when.day}".upper():
        r.take("Date")
    fuel_raw = r.take("Fuel")
    video, still = r.num("Length mm"), r.num("Flame Height Nikon (mm)")
    if video is not None or (still is None and data_is_fraction):
        measurement = "video"
    elif still is not None or re.fullmatch(r"\d{1,2}:\d{2}:\d{2}", r.get("GMT data") or ""):
        measurement = "still"
    else:
        measurement = None
    marks = {(r.get(c) or "").lower() for c in ("Smoke Height", "SH ?")}
    for c in ("Smoke Height", "SH ?"):
        if (r.get(c) or "").lower() in ("y", "n"):
            r.take(c)
    return {
        "row_kind": "test", "date": when.isoformat(),
        "fuel": fuel_name(fuel_raw), "fuel_raw": fuel_raw, "fuel_phase": "gas", "fuel_fraction": percent(fuel_raw),
        "config": "coflow", "geometry": f"nozzle {r.take('Nozzle (mm)')} mm",
        "pressure_kpa": r.num("Pressure (Pa)", 0.001),
        "flame_length_mm": video if video is not None else still, "measurement": measurement,
        "at_smoke_point": True if "y" in marks else False if "n" in marks else None,
    }


def spice_rows():
    path = psi.RAW / "files" / "PSI-107" / "Raw Data" / SPICE_LOG
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    header = [" ".join(f"{a} {b}".split()) or "Remark" for a, b in zip(sheet.row_values(2), sheet.row_values(3))]
    rows = []
    for k in range(4, sheet.nrows):
        values = dict(zip(header, sheet.row_values(k)))
        cells = {h: day_time(v) if h in SPICE_TIMES else cell_text(v) for h, v in values.items()}
        src = Src(cells)
        row = new_row(spice_log(src, isinstance(values["GMT data"], float)), None, path, k + 1)
        rate, air = num(cells.get("Air Rate (cm/s)")), num(cells.get("Air Display"))
        if rate is not None and air is None and abs(rate - AIR_INTERCEPT) < 0.01:
            flag(row, "flow_missing_los")  # downlink lost: the formula returned its intercept
        elif rate is not None:
            row["flow_cm_s"] = src.num("Air Rate (cm/s)")
            if rate < ANEMOMETER_MIN_CM_S:
                flag(row, "flow_below_sensor_range")
            if air is None:
                flag(row, "needs_review")  # air rate given although the AIR display reading was lost
        row["extra"] = src.extra()
        rows.append(row)
    tag_reviewed(rows, review_points())
    return rows


# The science team's smoke-point review (the 55 published points, 6 + 6 + 23 + 13 + 7) reads each point from one
# video frame, picked on the flame tip's grayscale gradient, not from the log. A point is a log row only when the
# log recorded the same flame state; otherwise it lies between two logged rows of the same burn.
SPICE_REVIEW = "PSI-107_Raw Data_SmokePointReview-0g-3.xlsx"
REVIEW_SHEETS = ("Smoke Point Datasheet", "Smoke Point Datasheet (2)")  # (2): the x264 re-measurement
IGNITION_TOL_S = 3
DISPLAY_TOL = 1  # video and still rows logged at the same moment differ by at most 1 fuel or air display count
DATA_TOL_S = 15  # review and log clocks for one flame state differ by up to 11 s; logged rows are 10-40 s apart
RAD_TOL = 0.25  # radiometer readings of one flame state differ by up to 0.19
LENGTH_TOL_MM = 3.0  # the two review sheets' lengths for one frame differ by up to 1.3 mm
REVIEW_EXTRA = {
    "No.": "review_no", "GMT data": "review_gmt_data", "Fuel Display": "review_fuel_display",
    "Air Display": "review_air_display", "Rad": "review_rad", "smk pt mm": "review_flame_length_mm",
    "Total Fuel Rate sccm": "review_fuel_rate_sccm", "mdotburner (mg/s)": "review_fuel_mg_s",
    "uair (cm/s)": "review_air_velocity_cm_s", "ufuel (cm/s)": "review_fuel_velocity_cm_s",
}


def clock(text):
    """Seconds of day from hh:mm:ss, hh.mm.ss, hhmm (to the minute) or a filled-down Excel day fraction (n.fff)."""
    s = clean(text) or ""
    if m := re.fullmatch(r"(\d{1,2})[:.](\d{2})[:.](\d{2})", s):
        return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
    if m := re.fullmatch(r"(\d{2})(\d{2})", s):
        return int(m[1]) * 3600 + int(m[2]) * 60
    if re.fullmatch(r"\d+\.\d+", s):
        return round(float(s) % 1 * 86400)
    return None


def review_points():
    path = psi.RAW / "files" / "PSI-107" / "Raw Data" / SPICE_REVIEW
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        sheet, recheck = (list(wb[s].iter_rows(values_only=True)) for s in REVIEW_SHEETS)
    header = [" ".join(f"{a or ''} {b or ''}".split()) for a, b in zip(sheet[2], sheet[3])]
    points = []
    for i in range(4, 59):  # Excel rows 5-59; the KC-135 and shuttle reference values follow
        cells = dict(zip(header, sheet[i]))
        text = {h: cell_text(v) for h, v in cells.items()}
        points.append({
            "n": i - 3, "tp": text["TP #"], "source_row": i + 1, "day": int(cells["GMT date"]),
            "fuel": fuel_name(text["Fuel"]), "fuel_fraction": percent(text["Fuel"]),
            "nozzle": float(cells["Nozzle (mm)"]), "ignition": clock(text["GMT ignite"]),
            "flame_off": clock(text["GMT flame off"]), "data": clock(text["GMT data"]),
            "fuel_display": num(text["Fuel Display"]),
            "air_display": num(text["Air Display"]), "rad": num(text["Rad"]), "length": num(text["smk pt mm"]),
            "extra": {"review_point": i - 3, "review_tp": text["TP #"], "review_source_row": i + 1}
            | {key: text[col] for col, key in REVIEW_EXTRA.items() if text[col] is not None}
            | ({"review_flame_length_mm_sheet2": cell_text(recheck[i][15])}
               if abs(recheck[i][15] - cells["smk pt mm"]) > 1e-6 else {}),
        })
    return points


def log_state(row):
    ex = row["extra"]
    return {
        "row": row, "day": date.fromisoformat(row["date"]).timetuple().tm_yday,
        "nozzle": float(row["geometry"].split()[1]), "ignition": clock(ex.get("GMT ignition")),
        "ignition_tol": 60 if re.fullmatch(r"\d{4}", ex.get("GMT ignition") or "") else IGNITION_TOL_S,
        "flame_off": clock(ex.get("GMT Flame Off")), "data": clock(ex.get("GMT data")),
        "fuel_display": num(ex.get("Fuel Display")), "air_display": num(ex.get("Air Display")),
        "rad": num(ex.get("Rad")), "length": row["flame_length_mm"],
    }


def _close(a, b, tol):
    return a is None or b is None or abs(a - b) <= tol


def review_burn(point, states):
    """Log rows of the review point's burn: same day, fuel, nozzle and ignition (flame-off when ignition was lost)."""
    same = [s for s in states if s["day"] == point["day"] and s["row"]["fuel"] == point["fuel"]
            and s["row"]["fuel_fraction"] == point["fuel_fraction"] and abs(s["nozzle"] - point["nozzle"]) < 0.01]
    key = "ignition" if point["ignition"] is not None else "flame_off"
    return [s for s in same if s[key] is not None and point[key] is not None
            and abs(s[key] - point[key]) <= (s["ignition_tol"] if key == "ignition" else IGNITION_TOL_S)]


def review_match(point, states):
    """("unique", [row]), ("bracket", [before, after]), ("ambiguous", rows) or ("no_match", [])."""
    if point["data"] is None or point["fuel_display"] is None:
        return "no_match", []
    burn = sorted((s for s in review_burn(point, states)
                   if None not in (s["data"], s["fuel_display"], s["air_display"])), key=lambda s: s["data"])
    hits = [s for s in burn if abs(s["data"] - point["data"]) <= DATA_TOL_S
            and abs(s["fuel_display"] - point["fuel_display"]) <= DISPLAY_TOL
            and _close(s["air_display"], point["air_display"], DISPLAY_TOL)
            and _close(s["rad"], point["rad"], RAD_TOL) and _close(s["length"], point["length"], LENGTH_TOL_MM)]
    # a video row and the Nikon still of the same moment can both agree; the row that also confirms Rad wins
    confirmed = max((s["rad"] is not None for s in hits), default=False)
    hits = [s for s in hits if (s["rad"] is not None) == confirmed]
    if hits:
        return ("unique" if len(hits) == 1 else "ambiguous"), [s["row"] for s in hits]
    for a, b in zip(burn, burn[1:]):
        if a["data"] < point["data"] < b["data"] and all(
            point[k] is None or a[k] is None or b[k] is None
            or min(a[k], b[k]) - tol <= point[k] <= max(a[k], b[k]) + tol
            for k, tol in (("fuel_display", DISPLAY_TOL), ("air_display", DISPLAY_TOL), ("rad", RAD_TOL))
        ):
            return "bracket", [a["row"], b["row"]]
    return "no_match", []


def tag_reviewed(rows, points):
    states = [log_state(row) for row in rows]
    for point in points:
        kind, matched = review_match(point, states)
        for row in matched if kind in ("unique", "bracket") else []:
            if "review_point" in row["extra"]:
                raise ValueError(f"{row['test_id']}: review points {row['extra']['review_point']} and {point['n']}")
            row["extra"] |= point["extra"]
            if kind == "unique":
                row["smoke_point_reviewed"] = True
            else:
                flag(row, "smoke_point_bracket")


# --- Corrections documented in the digest records (data/digest/PSI-*.json) ------------------------

def fix_flame_design(rows):
    for row in rows:
        ex = row["extra"]
        if row["test_id"] == "22042M1":
            ex["test_id_note"] = "day code 22042 disagrees with its table Day group (22024); probably 22024M1"
            flag(row, "id_suspect")
        if row["fuel"] == "propane":  # nominal 0.40 O2, one pinit, no final values and repeated Zst/Tad for the day
            flag(row, "placeholder_values")
        if any(v in ("RAMP", "RAMPED") for v in ex.values()):
            flag(row, "ramped")
        if "LOW O2" in ex.values():
            flag(row, "low_o2_in_source")
    return rows


CFIG_FILL_ATM = (0.5, 1.0, 2.0, 3.0)


def fix_cfig(rows):
    for row in rows:
        if row["config"] == "inverse" and row["pressure_kpa"] is not None:
            # most table levels are ~9% above the 0.507-3.04 bar fill pressures; six rows at 49.5 kPa are not
            ratio = min((row["pressure_kpa"] / (n * ATM_KPA) for n in CFIG_FILL_ATM), key=lambda r: abs(r - 1.09))
            if 1.05 < ratio < 1.13:
                flag(row, "pressure_9pct_above_nominal")
        if (row["extra"].get("Hot ignition") or "").lower() == "flash":
            flag(row, "flash_only")
        if row["peak_temp_c"] is not None and row["peak_temp_c"] > 450:  # stated 723 K termination limit
            flag(row, "burner_over_limit")
    return rows


def fix_same(rows):
    for row in rows:  # the EIRD planning matrix; the flight ran 47 points at 2-8 cm/s
        correct(row, "row_kind", "planned", "planned_not_flown")
    return rows


S_FLAME_BLENDS = {"20006": "20% H2 / 25% CH4 / 55% N2", "20013": "30% H2 / 15% CH4 / 55% N2"}


def fix_s_flame(rows):
    for row in rows:
        ex = row["extra"]
        if row["test_id"] in S_FLAME_BLENDS:
            correct(row, "fuel_fraction", 0.45, "corrected_from_report")
            ex["fuel_composition_on_orbit"] = S_FLAME_BLENDS[row["test_id"]]
        if row["test_id"] == "20190":
            ex["report_value"] = "reports give 45% H2 with He"
            flag(row, "conflicts_with_report")
        if re.search(r"with N[3-9]", f"{row['fuel_raw']} {ex.get('Atmosphere*')}"):
            flag(row, "autofill_artifact")  # "N2" dragged down a spreadsheet column became N3, N4, ...; read as N2
        if row["test_id"] == "20132":
            ex["report_value"] = "first day of the helium (second) round, not nitrogen-diluted"
            flag(row, "conflicts_with_report")
    return rows


BASS2_FINAL_O2 = "Calibrated final O2 % by vol"
BASS2_O2_ARTEFACTS = {"B2", "F3", "P22a", "T28a", "P22b", "T28b"}  # sensor offset, or offset plus raw reading


def fix_bass2(rows):
    for row in rows:
        ex = row["extra"]
        if row["test_id"] in BASS2_O2_ARTEFACTS and num(ex.get(BASS2_FINAL_O2)) is not None:
            ex[f"{BASS2_FINAL_O2}_original"] = ex.pop(BASS2_FINAL_O2)
            flag(row, "o2_final_artifact")
        if row["test_id"] in ("T9", "T18") and row["date"] == "2018-06-24":  # GMT 175 of 2014
            correct(row, "date", "2014-06-24", "date_corrected")
        date_conflict(row)
        infer_pmma(row, r"\brod\b|film|micron", "PSI-25 record, samples: cast PMMA rods (clear and black) and PMMA films")
        air = ex.get("Air display")
        if num(air) is not None:  # one steady reading of the duct anemometer, whole cm/s (as for PSI-26)
            row["flow_cm_s"] = num(air)
        elif len(re.findall(r"\d*\.?\d+", air or "")) > 1:
            flag(row, "ramped")
        if re.search(r"\bno ign", air or "", re.I):
            row["ignited"] = 0.0
    return rows


def fix_flex(rows):
    for row in rows:
        if row["test_id"] == "C11M201":
            flag(row, "pressure_zero_in_source")
        droplet_checks(row, [f"{g} initial ambient composition; mole fraction" for g in ("N", "CO", "He")])
    return rows


SAFFIRE_OUTCOMES = {  # (spread rate mm/s, burn length cm, source) for the two large-sheet missions
    ("PSI-98", "S1"): (1.8, 84, "PSI-98 record finding 1 (NTRS 20170008805 results table, test 1-1: ~84 cm, 1.8 mm/s)"),
    ("PSI-98", "S2"): (1.3, 10, "PSI-98 record finding 2 (NTRS 20170008805 results table, test 1-2: ~10 cm, 1.3 mm/s)"),
    ("PSI-100", "S1"): (2.3, 84, "PSI-100 record finding 1 (NTRS 20180005168 results table, test 3-1: ~84 cm, 2.3 mm/s)"),
    ("PSI-100", "S2"): (0.98, 10, "PSI-100 record finding 2 (NTRS 20180005168 results table, test 3-2: ~10 cm, 0.98 mm/s)"),
}
SAFFIRE_THICKNESS = {"thickness 0.37 cm": "thickness 0.37 mm", "thickness 037 mm": "thickness 0.37 mm",
                     "thickness .33 cm": "thickness 0.33 mm"}


def fix_saffire(rows):
    for row in rows:
        acc, tid, ex = row["accession"], row["test_id"], row["extra"]
        for wrong, right in SAFFIRE_THICKNESS.items():
            if (row["geometry"] or "").startswith(wrong):
                correct(row, "geometry", right + row["geometry"][len(wrong):], "unit_corrected")
        if (acc, tid) in SAFFIRE_OUTCOMES:
            row["spread_rate_mm_s"], row["burn_length_cm"], ex["outcome_source"] = SAFFIRE_OUTCOMES[(acc, tid)]
            flag(row, "value_from_report")
        if acc == "PSI-98":
            ex["report_value"] = "documents give 40.6 cm wide x 94 cm long (table swaps length and width)"
            flag(row, "conflicts_with_report")
        if acc == "PSI-100" or (acc, tid) == ("PSI-99", "2-6"):  # anemometers / published Table I: ~25 cm/s
            correct(row, "flow_cm_s", 25.0, "corrected_from_report")
        if (acc, tid) == ("PSI-99", "2-6"):
            correct(row, "fuel_raw", "Cotton-Fiberglass (SIBAL)", "corrected_from_report")
            correct(row, "fuel", "sibal fabric")
        if (acc, tid) == ("PSI-99", "2-9"):
            correct(row, "fuel_raw", "PMMA (flat, 1 cm)", "corrected_from_report")
            correct(row, "fuel", "pmma")
        if (acc, tid) == ("PSI-99", "2-1"):
            ex["report_value"] = "published Table I gives ~ 22.1 % O2"
            flag(row, "conflicts_with_report")
    return rows


def fix_efield(rows):
    kept, seen = [], {}
    for row in rows:
        key = json.dumps({k: v for k, v in row.items() if k != "source_row"}, sort_keys=True, default=str)
        if key in seen:  # day 18319 and its continuation rows are listed twice, verbatim
            seen[key]["extra"].setdefault("verbatim_duplicate_dropped", []).append(row["source_row"])
            continue
        seen[key] = row
        kept.append(row)
    return kept


def fix_slice(rows):
    for row in rows:
        if "C3H8" in (row["extra"].get("Test Date") or ""):  # the propane half of the label sits in the date cell
            correct(row, "fuel_raw", "100% C3H8 and then 100% C2H4", "label_fixed")
            row["extra"]["day_note"] = "last day mixed SPICE (propane) and SLICE (ethylene) testing"
    return rows


FIXES = {
    "PSI-10": fix_flame_design, "PSI-159": fix_cfig, "PSI-102": fix_same, "PSI-23": fix_s_flame,
    "PSI-25": fix_bass2, "PSI-26": fix_bass, "PSI-69": fix_flex, "PSI-98": fix_saffire, "PSI-99": fix_saffire,
    "PSI-100": fix_saffire, "PSI-22": fix_efield, "PSI-106": fix_slice,
}
REBUILT = {"PSI-39": cfi_rows, "PSI-107": spice_rows}
INVERSE_FLAMES = {"PSI-10", "PSI-159"}  # inverse rows: XO2 is the burner stream; the ambient is fuel + N2


PATCHES = psi.ROOT / "data" / "corrections" / "tests_patches.json"
PATCH_FLAGS = {"replace": "corrected_from_raw", "fill": "filled_from_raw", "flag": "conflicts_with_raw"}


def _same(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) < 1e-6
    return str(a) == str(b)


def apply_patches(groups, patches):
    """Apply the curated raw-data discrepancies (data/corrections/tests_patches.json). `replace` and `fill` change
    the value and keep the table's in extra; `flag` keeps the table value. Every patched row lists the patch ids
    in extra["discrepancies"]. A patch whose `table_value` no longer matches the table fails loudly."""
    index = {}
    for acc, rows in groups.items():
        for row in rows:
            index.setdefault((acc, row["test_id"]), []).append(row)
    for patch in patches:
        if patch["test_id"] is None:
            continue
        found = [r for r in index[(patch["accession"], patch["test_id"])]
                 if patch.get("source_row") in (None, r.get("source_row"))]
        if len(found) != 1:
            raise ValueError(f"patch {patch['id']}: {len(found)} rows match; give source_row")
        row = found[0]
        col = patch["column"]
        current = row["extra"].get(f"{col}_original", row[col])
        if not _same(current, patch["table_value"]):
            raise ValueError(f"patch {patch['id']}: table has {current!r}, patch expects {patch['table_value']!r}")
        if patch["action"] == "flag":
            flag(row, PATCH_FLAGS["flag"])
        else:
            value = patch["evidence_value"]
            if col in BOOLEAN and row[col] is not None:
                row["extra"].setdefault(f"{col}_original", bool(row[col]))
            correct(row, col, float(value) if isinstance(value, bool) else value, PATCH_FLAGS[patch["action"]])
        row["extra"].setdefault("discrepancies", []).append(patch["id"])


OUTCOMES = psi.ROOT / "data" / "corrections" / "tests_outcomes.json"
OUTCOME_VALUES = ("no_ignition", "extinguished", "burned_out")
OUTCOME_CAUSES = ("blowoff", "low_flow", "nitrogen", "unspecified")
# What was done to the flow when the flame went out. Two causes name it themselves; the other two need a reading of
# the words, given per run as `action` (null when the words do not say).
CAUSE_ACTION = {"blowoff": "flow_raised", "nitrogen": "nitrogen"}
READ_ACTIONS = {"low_flow": ("flow_shut_off", "flow_reduced", None), "unspecified": ("none", None)}
OUTCOME_ACTIONS = ("flow_shut_off", "flow_reduced", "flow_raised", "nitrogen", "none")


def _squash(text):
    return " ".join(str(text).split())


def apply_outcomes(groups, outcomes):
    """Fill `outcome` for solid-fuel runs whose tables have no outcome column, from a reading of the crew's own words
    (data/corrections/tests_outcomes.json). Each entry names the `extra` field it was read from and quotes it; an
    entry whose quote is no longer in that field fails loudly, so a reading can never outlive its source.
    `outcome_action` follows from the cause where the cause names it and is read per run otherwise; `outcome_setting`
    is the fan, pot or GN2 setting at which the flame went out, kept only while its number is in the source cell."""
    index = {}
    for acc, rows in groups.items():
        for row in rows:
            index[(acc, row["test_id"], row.get("source_row"))] = row
    for item in outcomes:
        key = (item["accession"], item["test_id"], item["source_row"])
        row = index.get(key)
        if row is None:
            raise ValueError(f"outcome {key}: no such row")
        if item["outcome"] not in OUTCOME_VALUES:
            raise ValueError(f"outcome {key}: unknown outcome {item['outcome']!r}")
        if (item["outcome"] == "extinguished") != (item.get("cause") in OUTCOME_CAUSES) or \
                (item["outcome"] != "extinguished" and item.get("cause") is not None):
            raise ValueError(f"outcome {key}: a cause goes with extinguished, and only with it")
        if _squash(item["quote"]) not in _squash(row["extra"].get(item["field"], "")):
            raise ValueError(f"outcome {key}: the quote is not in {item['field']!r}")
        cause = item.get("cause")
        if cause in READ_ACTIONS:
            if "action" not in item or item["action"] not in READ_ACTIONS[cause]:
                raise ValueError(f"outcome {key}: {cause} needs an action among {READ_ACTIONS[cause]}")
        elif "action" in item:
            raise ValueError(f"outcome {key}: an action is read only for {tuple(READ_ACTIONS)}")
        row["outcome"], row["outcome_cause"], row["outcome_quote"] = item["outcome"], cause, item["quote"]
        row["outcome_action"] = CAUSE_ACTION.get(cause, item.get("action"))
        row["extra"]["outcome_field"] = item["field"]
        if item.get("setting"):
            field = item.get("setting_field", item["field"])
            number = item["setting"].split()[-1]
            if item["outcome"] != "extinguished" or not {number, number.lstrip("0")} & set(
                    re.findall(r"\d*\.?\d+", str(row["extra"].get(field, "")))):
                raise ValueError(f"outcome {key}: the setting {item['setting']!r} is not in {field!r}")
            row["outcome_setting"], row["extra"]["outcome_setting_field"] = item["setting"], field
        if item.get("cause_inferred"):
            row["extra"]["outcome_cause_inferred"] = True
        if item.get("doubt"):
            row["extra"]["outcome_doubt"] = item["doubt"]


def oxygen_semantics(row):
    if row["accession"] in INVERSE_FLAMES and row["config"] == "inverse":
        row["x_o2_burner"], row["x_o2_min"], row["x_o2_max"] = row["x_o2"], None, None
        flag(row, "o2_is_burner_stream")
    elif row["x_o2_ambient"] is None:
        row["x_o2_ambient"] = row["x_o2"]


def build():
    acronyms = pd.read_csv(psi.PROCESSED / "investigations.csv").set_index("accession")["acronym"].to_dict()
    groups = {}
    for path in table_paths():
        adapter, acc = adapter_for(path), path.parts[-3]
        if adapter is None or acc in groups and acc in REBUILT:
            continue
        groups.setdefault(acc, []).extend(REBUILT[acc]() if acc in REBUILT else table_rows(path, adapter))
    out = []
    groups = {acc: list(FIXES.get(acc, list)(rows)) for acc, rows in groups.items()}
    for rows in groups.values():
        ids = Counter(row["test_id"] for row in rows)
        for row in rows:
            oxygen_semantics(row)
            if ids[row["test_id"]] > 1:
                flag(row, "duplicate_id")
    apply_patches(groups, json.loads(PATCHES.read_text()))
    apply_outcomes(groups, json.loads(OUTCOMES.read_text()))
    for acc, rows in groups.items():
        for row in rows:
            row["acronym"] = acronyms.get(acc)
            row["flags"] = ";".join(row["flags"]) or None
            row["extra"] = json.dumps(row["extra"], ensure_ascii=False) if row["extra"] else None
            out.append(row)
    df = pd.DataFrame(out, columns=COLUMNS)
    df[NUMERIC] = df[NUMERIC].astype(float)
    df[BOOLEAN] = df[BOOLEAN].astype("boolean")
    return df


def discrepancies():
    """The curated patches as a table: what the PSI table says, what the raw data say, and what was done."""
    df = pd.DataFrame(json.loads(PATCHES.read_text())).drop(columns="source_row", errors="ignore")
    df["flag"] = df["action"].map(PATCH_FLAGS)
    replaced = df[df["column"] == "test_id"].set_index(["accession", "test_id"])["evidence_value"].to_dict()
    df["test_id_now"] = [replaced.get((a, t), t) for a, t in zip(df["accession"], df["test_id"])]
    for col in ("table_value", "evidence_value"):
        df[col] = [None if v is None or v != v else str(v) for v in df[col]]
    return df[["id", "accession", "test_id", "test_id_now", "column", "table_value", "evidence_value", "action", "flag",
               "evidence", "evidence_source"]]


def flag_counts(df):
    return df["flags"].dropna().str.split(";").explode().value_counts()


if __name__ == "__main__":
    df = build()
    psi.write_table(df, "tests")
    psi.write_table(discrepancies(), "discrepancies")
    print(df.groupby(["accession", "acronym", "row_kind"]).size().to_string())
    print(df.notna().sum().to_string())
    print(flag_counts(df).to_string())
