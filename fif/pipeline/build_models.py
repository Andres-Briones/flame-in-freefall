"""Small, interpretable, cross-validated models of test outcomes, one investigation at a time
(never pooled: hardware, fuels and procedures differ between investigations).

Writes data/processed/models.json (one card per model, plus the dropped candidates),
data/processed/models/<id>.joblib (fitted on all training rows) and docs/models.md.

Run: uv run python -m fif.pipeline.build_models
"""
import json
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (balanced_accuracy_score, brier_score_loss, mean_absolute_error, r2_score,
                             roc_auc_score)
from sklearn.model_selection import GroupKFold, KFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text

from fif import models, psi

SEED = 0
N_FOLDS = 5
N_BOOT = 300
N_BOOT_CV = 200
DOCS = psi.ROOT / "docs" / "models.md"
N_CARBON = {"ethane": 2, "propane": 3, "butane": 4, "n-butane": 4}
ISO_FRACTION = {"[.60]/[.40] C12H26/iso-dodecane": 0.40, "[.75]/[.25] C12H26/iso-dodecane": 0.25, "C12H26": 0.0}


def feature(name, unit, expected, why, transform=None, allowed=None, untested=None):
    """`allowed`: the only values the input can take. `untested`: [lo, hi] ranges inside the training range that
    hold too few tests to predict in; `predict` treats them as outside the domain."""
    return {"name": name, "unit": unit, "transform": transform, "expected_sign": expected, "why": why,
            "allowed": allowed, "untested": untested}


# ---------------------------------------------------------------- data

def load_tests():
    return pd.read_parquet(psi.PROCESSED / "tests.parquet")


def extra_num(df, *keys):
    def get(raw):
        e = json.loads(raw) if isinstance(raw, str) else {}
        return next((e[k] for k in keys if k in e), None)
    return pd.to_numeric(df["extra"].map(get), errors="coerce")


def has_flag(df, code):
    return df["flags"].fillna("").str.split(";").map(lambda codes: code in codes)


def is_true(s):
    return s.astype("boolean").fillna(False).astype(bool)


def investigation(tests, accession):
    return tests[tests["accession"] == accession].copy()


class Rows:
    """Applies named exclusion steps to a frame and records how many rows each removed."""

    def __init__(self, df, start):
        self.df, self.steps = df, [{"step": start, "rows": len(df)}]

    def drop(self, mask, why):
        mask = mask.fillna(False).astype(bool)
        self.steps.append({"excluded": int(mask.sum()), "why": why})
        self.df = self.df[~mask]
        return self


def cfig(tests, config):
    df = investigation(tests, "PSI-159")
    df = df[df["config"] == config]
    df["fuel_flow_mg_s"] = extra_num(df, "mHC (mg/s)")
    df["o2_flow_mg_s"] = extra_num(df, "O2 flow rate (mg/s)")
    df["n_carbon"] = df["fuel"].map(N_CARBON)
    return df


def load_cfig_normal_self_extinction(tests):
    rows = Rows(cfig(tests, "normal"), "PSI-159 normal-flame tests")
    rows.drop(~is_true(rows.df["ignited"]), "no established hot flame (ignited False): there is nothing to extinguish "
              "(21106 F4 is kept: the table logs it as not ignited, the raw data show a 20 s flame, patch D03)")
    rows.drop(rows.df["extinction_mode"].isna(), "no recorded outcome")
    df = rows.df.assign(y=(rows.df["extinction_mode"] == "self_extinguished").astype(int))
    return df, rows.steps


def load_cfig_inverse_self_extinction(tests):
    rows = Rows(cfig(tests, "inverse"), "PSI-159 inverse-flame tests")
    rows.drop(has_flag(rows.df, "flash_only"), "flash_only: a ~1 s momentary flame is a failed ignition, "
              "not a radiative extinction of an established flame")
    rows.drop(~is_true(rows.df["ignited"]), "no hot ignition")
    rows.drop(rows.df["extinction_mode"].isna(), "no recorded outcome")
    df = rows.df.assign(y=(rows.df["extinction_mode"] == "self_extinguished").astype(int))
    return df, rows.steps


def load_cfig_normal_ignition(tests):
    rows = Rows(cfig(tests, "normal"), "PSI-159 normal-flame tests")
    rows.drop(rows.df["ignited"].isna(), "ignition outcome not recorded")
    rows.drop((rows.df["fuel_fraction"] <= 0) | (rows.df["fuel_flow_mg_s"] <= 0),
              "zero fuel fraction and zero fuel flow (21125 A4, H3): no fuel was supplied")
    df = rows.df.assign(y=rows.df["ignited"].astype(int))
    return df, rows.steps


def load_cfig_inverse_ignition(tests):
    rows = Rows(cfig(tests, "inverse"), "PSI-159 inverse-flame tests")
    rows.drop(has_flag(rows.df, "flash_only"), "flash_only: momentary flame, neither a clean ignition nor a failure")
    rows.drop(rows.df["ignited"].isna(), "ignition outcome not recorded")
    df = rows.df.assign(y=rows.df["ignited"].astype(int))
    return df, rows.steps


def flex(tests):
    df = investigation(tests, "PSI-69")
    df["x_co2"] = extra_num(df, "CO initial ambient composition; mole fraction")
    df["x_he"] = extra_num(df, "He initial ambient composition; mole fraction")
    df["is_heptane"] = (df["fuel"] == "n-heptane").astype(int)
    return df


def load_flex_burning_rate(tests):
    rows = Rows(flex(tests), "PSI-69 FLEX tests")
    rows.drop(rows.df["burn_rate_k_mm2_s"].isna(), "no burning-rate constant")
    rows.drop(rows.df[["d0_mm", "pressure_kpa"]].isna().any(axis=1),
              "no initial diameter or pressure (includes C11M201, pressure_zero_in_source)")
    rows.drop(has_flag(rows.df, "composition_sum"), "composition_sum: O2/N2/CO2/He fractions (features) sum to 0.98")
    rows.drop(has_flag(rows.df, "duplicate_id"), "duplicate_id: the two 193F001 rows disagree on d0, K and burn time")
    df = rows.df.assign(y=rows.df["burn_rate_k_mm2_s"])
    return df, rows.steps


def load_flex_methanol_extinction_diameter(tests):
    rows = Rows(flex(tests), "PSI-69 FLEX tests")
    rows.drop(rows.df["fuel"] != "methanol", "not methanol (heptane mixes radiative and diffusive branches)")
    rows.drop(rows.df["extinction_mode"] != "extinction", "test ended by disruption or completion, not extinction")
    rows.drop(has_flag(rows.df, "ext_zero") | has_flag(rows.df, "ext_gt_d0"),
              "ext_zero / ext_gt_d0: extinction diameter (the target) is a placeholder or impossible")
    rows.drop(rows.df[["ext_diameter_mm", "d0_mm", "pressure_kpa"]].isna().any(axis=1),
              "no extinction diameter, initial diameter or pressure")
    rows.drop(has_flag(rows.df, "composition_sum"), "composition_sum: ambient fractions (features) sum to 0.98")
    rows.drop(has_flag(rows.df, "duplicate_id"), "duplicate_id: the two 193F001 rows disagree")
    df = rows.df.assign(y=rows.df["ext_diameter_mm"])
    return df, rows.steps


def cfi(tests):
    df = investigation(tests, "PSI-39")
    df["x_he"] = extra_num(df, "Helium")
    df["iso_dodecane_fraction"] = df["fuel_raw"].map(ISO_FRACTION)
    return df


def load_cfi_reignition(tests):
    rows = Rows(cfi(tests), "PSI-39 CFI tests")
    rows.drop(rows.df["n_reignitions"].isna(), "not analysed in the data-summary spreadsheet (all farnesane, "
              "untested points)")
    rows.drop(rows.df["d0_mm"].isna(), "no initial diameter")
    rows.drop(has_flag(rows.df, "composition_sum"), "composition_sum: O2 + N2 = 0.97 (FLEX-1219 to 1222)")
    rows.drop(rows.df["pressure_kpa"] < 200, "below 2 atm: 0 re-ignitions in every analysed test (see the "
              "descriptive table); a logistic fit across that wall is pure separation")
    df = rows.df.assign(y=(rows.df["n_reignitions"] > 0).astype(int))
    return df, rows.steps


def load_spice_smoke_point_length(tests):
    df = investigation(tests, "PSI-107")
    df["nozzle_mm"] = df["geometry"].str.extract(r"([\d.]+)\s*mm", expand=False).astype(float)
    rows = Rows(df, "PSI-107 SPICE run-log rows")
    rows.drop(~is_true(rows.df["at_smoke_point"]), "not marked as at the smoke point")
    rows.drop(rows.df["flame_length_mm"].isna() | rows.df["flow_cm_s"].isna(), "no flame length or co-flow")
    for code in ("flow_below_sensor_range", "needs_review", "flow_missing_los"):
        rows.drop(has_flag(rows.df, code), f"{code}: co-flow (a feature) unreliable")
    df = rows.df.assign(y=rows.df["flame_length_mm"])
    return df, rows.steps


# ---------------------------------------------------------------- specs

RADIATIVE = r"\chi_r=\frac{\dot Q_{rad}}{\dot Q_{chem}}\sim\frac{\kappa_P\,\sigma T_f^{4}\,r_f^{3}}{\dot m_F\,\Delta h_c},\qquad r_f\propto\frac{\dot m}{4\pi\rho D\,\ln\!\left(1/(1-Z_{st})\right)}"

SPECS = [
    {
        "id": "cfig_normal_self_extinction",
        "accession": "PSI-159",
        "kind": "classifier",
        "question": "Once a normal (fuel-from-burner) spherical gas flame is lit, does it go out on its own "
                    "(radiative self-extinction) before the scripted flow cut-off?",
        "target": "self_extinguished",
        "target_definition": "1 if extinction_mode == 'self_extinguished', 0 if 'flow_terminated' (flow cut by the "
                             "script timeout or the burner temperature limit)",
        "load": load_cfig_normal_self_extinction,
        "features": [
            feature("x_o2_ambient", "mole fraction", "-", "more O2 raises T_f and heat release relative to radiation",
                    untested=[[0.25, 0.35]]),
            feature("pressure_kpa", "kPa", "+", "soot and gas radiation grow with pressure", "log10"),
            feature("fuel_flow_mg_s", "mg/s", "+", "flame radius grows with fuel flow, radiative loss ~ r_f^3 "
                    "against heat release ~ mdot, so chi_r rises", "log10"),
            feature("fuel_fraction", "mole fraction (burner stream)", "?", "dilution lowers T_ad (favours "
                    "extinction) but also lowers soot (favours survival)"),
            feature("n_carbon", "C atoms (2 ethane, 3 propane, 4 n-butane)", "+", "larger alkanes soot more",
                    allowed=[2, 3, 4]),
        ],
        "physics": "These flames die by radiative loss, not by a residence-time (Damköhler) limit: the flame grows "
                   "slowly in quiescent microgravity, radiates from soot and gas, and goes out when the radiative "
                   "loss fraction drives T_f to about 1100-1200 K.",
        "scaling": RADIATIVE,
        "describe_by": ("o2_band", lambda d: np.where(d["x_o2_ambient"] < 0.25, "about 0.21",
                                                      np.where(d["x_o2_ambient"] < 0.35, "about 0.33", "about 0.40"))),
        "interpretation": "Partly. Ambient O2 (-) and fuel flow (+, larger flame, more radiative loss) agree, with intervals "
                          "excluding 0; these two carry the model. Pressure and carbon number are indistinguishable from 0: "
                          "within these tests, radiative self-extinction does not measurably depend on pressure once O2 "
                          "and flow are fixed. The depth-3 tree and gradient boosting do no better on held-out days, so "
                          "the linear form leaves little on the table.",
        "caveats": [
            "'Flow-terminated' is not 'stable': flow was cut by scripted timeouts or burner over-temperature, so the "
            "target is 'self-extinguished before the cut-off', and the fractions depend on the chosen timeouts.",
            "At about 21% ambient O2 every lit flame self-extinguished (quasi-complete separation); the coefficients "
            "mainly describe the about 40% O2 tests. Only 3 tests sit at about 33% O2.",
            "Chamber composition drifts during a day (closed chamber); x_o2_ambient is the tabulated estimate, not a "
            "gas-chromatograph measurement. Mass flow controllers are poor below 10% of full scale.",
            "Burner temperature (which lengthens burns) is not a feature: it is an outcome of the burn.",
        ],
        "must_not": [
            "material flammability, cabin fires or condensed fuels",
            "other burners or flow timeouts (the target is tied to this hardware's cut-off times)",
            "O2 between 0.25 and 0.35 (3 tests) or any combination not near a listed nearest test",
        ],
    },
    {
        "id": "cfig_inverse_self_extinction",
        "accession": "PSI-159",
        "kind": "classifier",
        "question": "Once an inverse (oxidiser-from-burner, fuel ambient) flame is lit, does it self-extinguish "
                    "before the flow cut-off, and how strongly does chamber pressure matter?",
        "target": "self_extinguished",
        "target_definition": "1 if extinction_mode == 'self_extinguished', 0 if 'flow_terminated' (usually the 66 s "
                             "inverse timeout, sometimes the burner temperature limit)",
        "load": load_cfig_inverse_self_extinction,
        "features": [
            feature("pressure_kpa", "kPa (table values, ~9% above nominal fill)", "+",
                    "soot forms outside the inverse flame in the hot fuel-rich gas; radiation grows with pressure",
                    "log10"),
            feature("x_o2_burner", "mole fraction (burner stream)", "-", "more O2 in the burner stream raises T_ad"),
            feature("o2_flow_mg_s", "mg/s", "+", "O2 is the limiting reactant, so O2 flow sets the flame size and "
                    "hence radiative loss", "log10"),
            feature("n_carbon", "C atoms (2 ethane, 3 propane, 4 n-butane)", "+", "larger alkanes soot more",
                    allowed=[2, 3, 4]),
        ],
        "physics": "Same radiative-loss balance as normal flames, but the soot forms on the outside of the flame. "
                   "Raising pressure increases soot and radiating-gas density, so radiative extinction should "
                   "become more likely with pressure.",
        "scaling": RADIATIVE,
        "describe_by": ("pressure_level_kpa", lambda d: d["pressure_kpa"].round(-1).astype(int).astype(str)),
        "interpretation": "Pressure agrees strongly (+) and is the largest term (a pressure split alone gives a pooled "
                          "held-out AUC of 0.71 against 0.87 for the full model; gradient boosting does worse on held-out "
                          "days), matching 0/29 self-extinctions at 0.5-0.6 bar against 58/67 at 2.2-3.3 bar. Burner-stream O2 "
                          "has the opposite sign to the a-priori expectation (-): richer oxidiser streams "
                          "self-extinguished more often. This is a property of the test design, not a mechanism: the "
                          "O2 mass flow was held roughly fixed, so a richer burner stream means a smaller total burner "
                          "flow (correlation about -0.66 between burner O2 and the log of the estimated total flow). "
                          "The sign stays positive within each pressure level and with day fixed effects, and it "
                          "becomes indistinguishable from 0 once total flow is added, so the data cannot separate "
                          "burner O2 from total flow. O2 flow and carbon number are indistinguishable from 0.",
        "caveats": [
            "All inverse rows carry pressure_9pct_above_nominal: the table pressures are ~9% above the fill levels. "
            "Used as given: a uniform multiplicative offset only shifts the intercept of log10(pressure).",
            "Pressure and O2 flow are partly confounded with test day: pressure levels were run on separate days, so "
            "the grouped CV can only test pressure on held-out days with other pressures.",
            "79 of 154 inverse tests used 85% O2 in the burner stream; low burner-O2 cells are small.",
            "Ambient fuel fraction is left out: it was lowered as pressure was raised (r = -0.72 with pressure in "
            "the training rows), so the two cannot be separated and the fit would split the pressure effect "
            "between them.",
            "As for normal flames, 'flow_terminated' is a timeout outcome, not a stability limit.",
        ],
        "must_not": [
            "normal flames or real fires (an inverse flame has no fire-safety analogue in a cabin)",
            "pressures outside 0.5-3.3 bar or other burners",
        ],
    },
    {
        "id": "cfig_normal_ignition",
        "accession": "PSI-159",
        "kind": "classifier",
        "question": "Does a normal flame light (hot ignition) for a given chamber O2, pressure and fuel stream?",
        "target": "ignited",
        "target_definition": "1 if the table's 'Hot ignition' is yes, 0 if no",
        "load": load_cfig_normal_ignition,
        "descriptive": True,
        "features": [
            feature("x_o2_ambient", "mole fraction", "+", "faster chemistry and hotter flame (Damköhler number up)"),
            feature("pressure_kpa", "kPa", "+", "reaction rate ~ p^n with n ~ 2 for chain branching, so Da rises",
                    "log10"),
            feature("fuel_flow_mg_s", "mg/s", "+", "more fuel near the igniter", "log10"),
            feature("fuel_fraction", "mole fraction (burner stream)", "+", "heavily diluted fuel gives a cool, weak "
                    "mixture near the igniter", "log10"),
            feature("n_carbon", "C atoms", "?", "no clear expectation across C2-C4 alkanes", allowed=[2, 3, 4]),
        ],
        "physics": "Ignition succeeds when chemistry is fast compared with transport away from the igniter: a "
                   "Damköhler-number criterion. Dilution and low O2 lower the flame temperature and slow chemistry.",
        "scaling": r"\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}},\qquad \tau_{chem}^{-1}\propto p^{\,n-1}\exp\!\left(-\frac{E_a}{R T_f}\right)",
        "describe_by": ("fuel_fraction_band", lambda d: np.where(d["fuel_fraction"] < 0.05, "< 0.05", ">= 0.05")),
        "interpretation": "O2 agrees (+, interval excludes 0); pressure, flow and dilution agree in sign only. The robust "
                          "statement is the dilution table: 14/38 ignitions below 0.05 fuel fraction against 118/139 "
                          "above. The fit does not generalise to held-out days (grouped AUC near chance), because the "
                          "failures cluster on a few days with modified igniter settings.",
        "caveats": [
            "Igniter energy was deliberately lowered in some tests to try direct cool-flame ignition (final report); "
            "igniter settings are not in the table, so some failures are by design and look like condition effects.",
            "Mass flow controllers are poor below 10% of full scale, which is where most diluted, low-flow failures "
            "sit.",
            "Failures cluster by day: all 45 fall on 6 of 11 test days (12 Apr - 11 Jun 2021), 44 of them on 5, and the grouped CV "
            "(held-out days) is close to chance. Kept as a descriptive table, not a predictor.",
        ],
        "must_not": [
            "flammability limits of materials or of premixed gases",
            "igniters other than the ACME hot-wire igniter at standard settings",
        ],
    },
    {
        "id": "cfig_inverse_ignition",
        "accession": "PSI-159",
        "kind": "classifier",
        "question": "Does an inverse flame light, given the burner-stream O2 and chamber pressure?",
        "target": "ignited",
        "target_definition": "1 if 'Hot ignition' is yes, 0 if no ('flash' rows excluded)",
        "load": load_cfig_inverse_ignition,
        "descriptive": True,
        "features": [
            feature("x_o2_burner", "mole fraction (burner stream)", "+", "a richer oxidiser stream gives a hotter, "
                    "faster-reacting mixture at the igniter"),
            feature("pressure_kpa", "kPa (table values)", "+", "Da rises with pressure", "log10"),
        ],
        "physics": "As for normal flames, a Damköhler-number criterion; here the burner O2 fraction sets T_ad.",
        "scaling": r"\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}}",
        "describe_by": ("x_o2_burner_level", lambda d: d["x_o2_burner"].round(2).astype(str)),
        "interpretation": "Burner O2 agrees (+) on average, but the table shows the effect is not monotone: the failures "
                          "concentrate at 0.21 burner O2, while the few lower-O2 tests mostly lit.",
        "caveats": [
            "Only 15 non-ignitions, 10 of them at 0.21 burner O2; the fit is close to a lookup of that cell. Read the "
            "descriptive table first.",
            "Igniter settings varied and are not in the table.",
            "Not monotone in burner O2: 6 of 7 tests at 0.15-0.19 ignited while 10 of 26 at 0.21 failed, so a "
            "logistic curve in O2 misdescribes the low end. Kept as a descriptive table.",
        ],
        "must_not": ["normal flames", "any fire-safety ignition criterion"],
    },
    {
        "id": "flex_burning_rate",
        "accession": "PSI-69",
        "kind": "regressor",
        "question": "How fast does a free methanol or n-heptane droplet burn (d²-law constant K) in a given "
                    "atmosphere?",
        "target": "burn_rate_k_mm2_s",
        "target_definition": "average burning-rate constant K (mm²/s) of the d²-law d² = d0² - K t, as tabulated",
        "load": load_flex_burning_rate,
        "sum_at_most_one": ["x_o2_ambient", "x_co2", "x_he"],
        "features": [
            feature("is_heptane", "1 n-heptane, 0 methanol", "+", "heptane has the larger transfer number B",
                    allowed=[0, 1]),
            feature("x_o2_ambient", "mole fraction", "+", "B grows with ambient O2"),
            feature("x_co2", "mole fraction", "-", "CO2's heat capacity lowers T_f and B"),
            feature("x_he", "mole fraction", "+", "helium raises the gas conductivity lambda"),
            feature("pressure_kpa", "kPa", "?", "quasi-steady theory: K nearly independent of pressure", "log10"),
            feature("d0_mm", "mm", "-", "radiative loss grows with droplet and flame size; small methanol droplets "
                    "burn faster than predicted"),
        ],
        "physics": "Quasi-steady droplet burning gives the d²-law with K set by gas conductivity, liquid properties "
                   "and the Spalding transfer number B, which grows with ambient O2 and falls with diluent heat "
                   "capacity.",
        "scaling": r"d^2=d_0^2-Kt,\qquad K=\frac{8\lambda_g}{\rho_l c_{p,g}}\ln(1+B),\qquad B=\frac{Y_{O_2,\infty}\Delta h_c/\nu+c_p(T_\infty-T_s)}{h_{fg}}",
        "interpretation": "Yes, every term with an expectation agrees and its interval excludes 0: K rises with O2 and "
                          "helium (conductivity), falls with CO2 and with initial diameter (radiative loss), and is "
                          "slightly higher for heptane. Pressure has a small positive coefficient that is not "
                          "robust: it shrinks about fourfold when the tests that went out early are left out (see "
                          "Sensitivity), so K is best read as independent of pressure here, as quasi-steady theory "
                          "says. The linear model beats "
                          "gradient boosting on held-out days (R² 0.69 vs 0.53), so there is no evidence of missed "
                          "non-linearity.",
        "sensitivity": {
            "without": "the tests that went out early (D_ext/D0 > 0.9), where K is fitted over a short burn",
            "exclude": lambda d: (d["ext_diameter_mm"] / d["d0_mm"] > 0.9).fillna(False),
        },
        "caveats": [
            "The rows include tests that went out early (D_ext/D0 > 0.9). They are kept, because leaving them out "
            "would select on the outcome, but the pressure coefficient depends on them (see Sensitivity).",
            "K is one average per test; the tabulated value is not accompanied by the diameter history it came from.",
            "Needle conformal-coating contamination (2009-2011) is judged by the team to affect K minimally.",
            "Diluent fractions vary jointly (O2/N2/CO2/He sum to 1), so coefficients are partial effects at fixed "
            "remaining fractions; N2 is the implicit reference.",
        ],
        "must_not": [
            "other fuels, fibre-supported droplets or sprays",
            "predicting whether a droplet ignites (no failed-ignition rows exist)",
            "burn time (needs the extinction diameter, which this model does not predict)",
        ],
    },
    {
        "id": "flex_methanol_extinction_diameter",
        "accession": "PSI-69",
        "kind": "regressor",
        "question": "At what droplet diameter does a burning methanol droplet go out?",
        "target": "ext_diameter_mm",
        "target_definition": "visible-flame extinction diameter (mm), tests that ended in flame extinction",
        "load": load_flex_methanol_extinction_diameter,
        "sum_at_most_one": ["x_o2_ambient", "x_co2", "x_he"],
        "features": [
            feature("d0_mm", "mm", "+", "absorbed product water accumulates to ~30% of the droplet mass, so D_ext "
                    "grows roughly linearly with D0"),
            feature("x_o2_ambient", "mole fraction", "-", "diffusive (Damköhler) extinction diameter grows as O2 "
                    "falls"),
            feature("x_co2", "mole fraction", "?", "the team reports D_ext nearly independent of diluent type"),
            feature("x_he", "mole fraction", "?", "as for CO2"),
            feature("pressure_kpa", "kPa", "?", "no clear expectation over 0.7-3 atm", "log10"),
        ],
        "physics": "Methanol droplets in FLEX mostly went out diffusively: the flame's residence time shrinks with "
                   "the droplet until the Damköhler number falls below critical, and absorbed water (which "
                   "dilutes the fuel vapour) makes that happen at a larger diameter. Below about 14% O2, "
                   "radiative extinction takes over.",
        "scaling": r"\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}},\qquad \tau_{res}\sim\frac{d_f^{2}}{\alpha},\qquad \mathrm{Da}<\mathrm{Da}_{crit}\Rightarrow\text{extinction}",
        "interpretation": "Yes. D_ext grows with D0 (0.82 mm per mm, close to the linear water-absorption "
                          "scaling) and with lower O2. CO2 and helium both enlarge D_ext; that is consistent with the "
                          "Damköhler picture (CO2 lowers T_f and slows chemistry; helium's higher diffusivity shortens "
                          "the residence time d_f²/α), though the team describes D_ext as nearly independent of diluent. "
                          "Gradient boosting is only slightly better (R² 0.74 vs 0.70).",
        "caveats": [
            "Rows mix diffusive and (below ~14% O2) radiative extinctions; the table does not label which.",
            "Some extinction diameters were extrapolated when the droplet drifted out of view.",
            "Disrupted droplets (often from needle-coating contamination) are excluded, which selects cleaner tests.",
        ],
        "must_not": ["n-heptane or other fuels", "an oxygen index (LOI) estimate: no failed-ignition rows exist"],
    },
    {
        "id": "cfi_reignition",
        "accession": "PSI-39",
        "kind": "classifier",
        "question": "At 2-5 atm, does an n-dodecane (or n-/iso-dodecane blend) droplet re-ignite a hot flame "
                    "from its cool flame after the first radiative extinction?",
        "target": "reignited",
        "target_definition": "1 if n_reignitions > 0 (spreadsheet DATA sheet), else 0",
        "load": load_cfi_reignition,
        "sum_at_most_one": ["x_o2_ambient", "x_he"],
        "descriptive": True,
        "features": [
            feature("pressure_kpa", "kPa", "+", "low-temperature chemistry and heat release rise with pressure",
                    "log10"),
            feature("d0_mm", "mm", "+", "a larger droplet leaves more fuel and a longer cool-flame phase"),
            feature("iso_dodecane_fraction", "mole fraction of iso-dodecane in the fuel", "-",
                    "branched iso-dodecane suppresses low-temperature chemistry"),
            feature("x_he", "mole fraction", "?", "helium shortens hot flames but the team reports it helps the "
                    "heat-release/heat-loss balance in the NTC region"),
            feature("x_o2_ambient", "mole fraction", "+", "more O2, more vigorous cool-flame chemistry"),
        ],
        "physics": "After radiative extinction of the hot flame, n-alkane droplets keep burning as a cool flame "
                   "(low-temperature, NTC chemistry). At higher pressure the cool flame releases more heat and "
                   "accumulates reactive vapour, and can run away back into a hot flame.",
        "scaling": r"\mathrm{Da}_{cool}=\frac{\tau_{res}}{\tau_{LTC}},\qquad \tau_{res}\sim\frac{d_f^{2}}{\alpha},\qquad \tau_{LTC}^{-1}\ \text{rises with }p",
        "describe_rows": lambda tests: cfi_reignition_all_pressures(tests),
        "describe_by": ("pressure_level_kpa", lambda d: d["pressure_kpa"].round(0).astype(int).astype(str)),
        "interpretation": "Pressure agrees (+) and is the only effect: none of 86 analysed tests at or below 1.25 atm "
                          "re-ignited, against 36 of 62 at 2-5 atm. Within 2-5 atm nothing else is resolvable; d0 has the "
                          "opposite sign to expectation but its interval spans 0 widely.",
        "caveats": [
            "Below 2 atm no analysed test re-ignited (0/86): that wall is reported as a descriptive table, and the "
            "logistic model only covers 2-5 atm.",
            "The type-B thermocouple catalytic re-ignition seen in CFI-G (PSI-159) is a different hardware effect; "
            "CFI uses no such probe near the droplet.",
            "Farnesane tests are not analysed in the spreadsheet and are absent.",
            "Within 2-5 atm the logistic fit has no skill on held-out days (pressure levels were flown on separate "
            "days, and d0, blend and helium add nothing measurable), so only the pressure table is a result.",
        ],
        "must_not": ["pressures below 2 atm via this model (use the table)", "fuels other than n-dodecane blends"],
    },
    {
        "id": "spice_smoke_point_length",
        "accession": "PSI-107",
        "kind": "regressor",
        "descriptive": True,
        "target_transform": "log10",
        "question": "How long is a microgravity co-flow jet flame at its smoke point, for a given nozzle and "
                    "co-flow speed?",
        "target": "flame_length_mm",
        "target_definition": "luminous flame length (mm, video) of run-log rows marked as at the smoke point",
        "load": load_spice_smoke_point_length,
        "features": [
            feature("nozzle_mm", "mm", "-", "published fit L_SP ~ d^-0.91", "log10"),
            feature("flow_cm_s", "cm/s", "+", "published fit L_SP ~ u_a^0.41: co-flow shortens residence time",
                    "log10"),
        ],
        "physics": "A jet flame emits smoke when its tip is cooled (by soot radiation) below the temperature at "
                   "which soot oxidation stops; the luminous length at that point is the smoke point. Co-flow "
                   "shortens residence time, so more fuel (a longer flame) is needed before soot escapes.",
        "scaling": r"L_{SP}\propto d^{-0.91}\,u_a^{0.41}\quad\text{(SPICE final report, all fuels)},\qquad L_f=C\,\frac{\dot m_f}{Z_{st}}",
        "interpretation": "Only in sign. The fitted exponents (nozzle -0.04, co-flow +0.25, both intervals spanning 0) "
                          "are far from the published L_SP ~ d^-0.91 u_a^0.41, and no fit beats the mean on held-out "
                          "days. With fuels pooled and 23 rows, the fuel-specific smoke point dominates the scatter. The "
                          "run-log smoke-point rows do not reproduce the published correlation; the 55-point "
                          "smoke-point review sheet would be needed.",
        "caveats": [
            "Only 23 smoke-point rows with a length in the run log against 52-55 smoke points in the reports; the "
            "smoke-point review sheet could not be matched row by row.",
            "Fuels (ethylene, propane, 50/75/100% propylene) are pooled because 23 rows cannot support a fuel term; "
            "the smoke point is fuel-specific, so the scatter is large.",
            "Outlet-screen clogging changed the true co-flow for a given anemometer reading between days.",
        ],
        "must_not": ["any prediction: this is a descriptive fit", "1 g flames or unconfined burners"],
    },
]

DROPPED = [
    {"id": "flex_extinction_mode", "accession": "PSI-69",
     "reason": "The end mode (extinction / disruption / completion) is confounded with needle-coating "
               "contamination, which the team blames for disruptions: 46 of 165 tests disrupted in 2009-2010 against "
               "15 of 109 in 2011. "
               "Radiative vs diffusive extinction is not labelled in the table; deriving it from D_ext/D0 would put "
               "the outcome into the label definition with an arbitrary threshold."},
    {"id": "flex_ignition", "accession": "PSI-69",
     "reason": "No failed-ignition rows: 'will it burn' (and an LOI) cannot be estimated."},
    {"id": "flex_heptane_extinction_diameter", "accession": "PSI-69",
     "reason": "Heptane extinctions mix an early radiative branch (D_ext/D0 > 0.9 in 24 of 56) and a diffusive "
               "branch, unlabelled; a single linear model across both is not physically meaningful."},
    {"id": "cfi_cool_flame_occurrence", "accession": "PSI-39",
     "reason": "cool_flame is True-or-null. Null rows are not negatives: among analysed tests with cool_flame null, "
               "comments describe cool-flame burning (FLEX-1214, 1216, 1229), droplets leaving the field of view, "
               "or no ignition (FLEX-1212)."},
    {"id": "cfi_hot_burning_rate", "accession": "PSI-39",
     "reason": "60 of 148 hot-flame K values come from flames that went out with D_ext/D0 > 0.95, where K is fitted "
               "over a tiny part of the burn (values down to 0.001 mm²/s). Filtering those out selects on the "
               "outcome; keeping them makes K mostly measurement noise."},
    {"id": "spice_at_smoke_point_classifier", "accession": "PSI-107",
     "reason": "Only 31 rows are marked True and 66 False (429 null). 'False' lumps flames below the smoke point "
               "with flames already past it, so the label is not monotone in flame length and a classifier on "
               "length, fuel, nozzle and flow has no physical threshold to learn; 21 of the 66 are Nikon still rows "
               "duplicating a video row."},
    {"id": "psi20_bre", "accession": "PSI-20",
     "reason": "18 test-day rows (several flames each) with no outcome column at all: nothing to "
               "model per test."},
]


# ---------------------------------------------------------------- estimators

def primary(kind):
    if kind == "classifier":
        return make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000))
    return make_pipeline(StandardScaler(), LinearRegression())


def comparisons(kind):
    if kind == "classifier":
        return {
            "majority_class": DummyClassifier(strategy="prior"),
            "single_best_feature_rule": DecisionTreeClassifier(max_depth=1, random_state=SEED),
            "decision_tree_depth3": DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=SEED),
            "gradient_boosting": GradientBoostingClassifier(max_depth=2, n_estimators=100, random_state=SEED),
        }
    return {
        "mean_predictor": DummyRegressor(strategy="mean"),
        "single_best_feature_rule": DecisionTreeRegressor(max_depth=1, random_state=SEED),
        "decision_tree_depth3": DecisionTreeRegressor(max_depth=3, min_samples_leaf=5, random_state=SEED),
        "gradient_boosting": GradientBoostingRegressor(max_depth=2, n_estimators=100, random_state=SEED),
    }


def splits(kind, X, y, groups):
    n_groups = len(set(groups))
    grouped = GroupKFold(n_splits=min(N_FOLDS, n_groups)).split(X, y, groups)
    plain = (StratifiedKFold if kind == "classifier" else KFold)(N_FOLDS, shuffle=True, random_state=SEED)
    return {"grouped_by_date": list(grouped), "ungrouped": list(plain.split(X, y))}


def fold_metrics(kind, y, pred):
    if kind == "classifier":
        auc = roc_auc_score(y, pred) if len(set(y)) == 2 else np.nan
        # a held-out day can hold a single class: AUC is then undefined and balanced accuracy degenerate
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            bacc = balanced_accuracy_score(y, pred >= 0.5)
        return {"roc_auc": auc, "brier": brier_score_loss(y, pred, labels=[0, 1]), "balanced_accuracy": bacc}
    return {"r2": r2_score(y, pred), "mae": mean_absolute_error(y, pred)}


def predict_any(est, X):
    return est.predict_proba(X)[:, 1] if hasattr(est, "predict_proba") else est.predict(X)


def cross_validate(est, kind, X, y, folds):
    oof = np.zeros(len(y))
    per_fold = []
    for train, test in folds:
        fitted = clone(est).fit(X[train], y[train])
        oof[test] = predict_any(fitted, X[test])
        per_fold.append(fold_metrics(kind, y[test], oof[test]))
    summary = {}
    for name in per_fold[0]:
        vals = np.array([f[name] for f in per_fold], dtype=float)
        ok = vals[~np.isnan(vals)]
        summary[name] = {"mean": ok.mean() if len(ok) else None, "sd": ok.std(ddof=1) if len(ok) > 1 else None,
                         "per_fold": [None if np.isnan(v) else v for v in vals], "pooled": None}
    for name, v in fold_metrics(kind, y, oof).items():
        summary[name]["pooled"] = v
    return summary, oof


def metric_interval(kind, X, y, groups):
    """Spread of the headline metric when the test days are resampled with replacement and the whole grouped
    cross-validation is rerun: 2.5th, 50th and 97.5th percentile of the pooled out-of-fold value."""
    metric = "roc_auc" if kind == "classifier" else "r2"
    rng = np.random.default_rng(SEED)
    labels = np.array(sorted(set(groups)))
    idx = {g: np.flatnonzero(groups == g) for g in labels}
    values = []
    while len(values) < N_BOOT_CV:
        rows = np.concatenate([idx[g] for g in rng.choice(labels, len(labels))])
        Xb, yb, gb = X[rows], y[rows], groups[rows]
        if kind == "classifier" and len(set(yb)) < 2:
            continue
        folds = GroupKFold(n_splits=min(N_FOLDS, len(set(gb)))).split(Xb, yb, gb)
        try:
            values.append(cross_validate(primary(kind), kind, Xb, yb, list(folds))[0][metric]["pooled"])
        except ValueError:  # a training fold with a single class
            continue
    lo, mid, hi = np.percentile(values, [2.5, 50, 97.5])
    return {"ci95": [lo, hi], "median": mid, "resamples": N_BOOT_CV}


def sensitivity(spec, df, X, y, groups):
    """The fit repeated without a doubtful subset of rows, to show which coefficients depend on it."""
    kind = spec["kind"]
    keep = ~np.asarray(spec["sensitivity"]["exclude"](df), dtype=bool)
    est = primary(kind).fit(X[keep], y[keep])
    metric = "roc_auc" if kind == "classifier" else "r2"
    folds = GroupKFold(n_splits=min(N_FOLDS, len(set(groups[keep])))).split(X[keep], y[keep], groups[keep])
    cv = cross_validate(est, kind, X[keep], y[keep], list(folds))[0][metric]
    return {"without": spec["sensitivity"]["without"], "excluded": int((~keep).sum()), "n": int(keep.sum()),
            "metric": metric, "grouped_mean": cv["mean"], "grouped_pooled": cv["pooled"],
            "per_unit": {label(f): c / s for f, c, s in zip(spec["features"], np.ravel(est[-1].coef_), est[0].scale_)}}


# ---------------------------------------------------------------- fitting and reporting

def coefficient_table(spec, est, X, y, groups):
    feats = spec["features"]
    scaler, lin = est[0], est[-1]
    coef = np.ravel(lin.coef_)
    boot = bootstrap_coefs(spec["kind"], X, y, groups)
    rows = []
    for j, f in enumerate(feats):
        lo, hi = np.percentile(boot[:, j], [2.5, 97.5])
        rows.append({
            "feature": label(f),
            "per_sd": coef[j],
            "per_unit": coef[j] / scaler.scale_[j],
            "per_sd_ci95_cluster_bootstrap": [lo, hi],
            "per_unit_ci95_cluster_bootstrap": [lo / scaler.scale_[j], hi / scaler.scale_[j]],
            "expected_sign": f["expected_sign"],
            "agreement": agreement(f["expected_sign"], coef[j], lo, hi),
        })
    intercept = float(np.ravel(lin.intercept_)[0]) - float(np.sum(coef * scaler.mean_ / scaler.scale_))
    scale = "log-odds" if spec["kind"] == "classifier" else label({"name": spec["target"],
                                                                   "transform": spec.get("target_transform")})
    return {"scale": scale, "intercept_per_unit": intercept, "terms": rows}


def bootstrap_coefs(kind, X, y, groups):
    rng = np.random.default_rng(SEED)
    labels = np.array(sorted(set(groups)))
    idx = {g: np.flatnonzero(groups == g) for g in labels}
    out = []
    while len(out) < N_BOOT:
        rows = np.concatenate([idx[g] for g in rng.choice(labels, len(labels))])
        if kind == "classifier" and len(set(y[rows])) < 2:
            continue
        out.append(np.ravel(primary(kind).fit(X[rows], y[rows])[-1].coef_))
    return np.array(out)


def agreement(expected, coef, lo, hi):
    if expected == "?":
        return "no prior expectation"
    sign_ok = (coef > 0) == (expected == "+")
    excludes_zero = lo > 0 or hi < 0
    if sign_ok:
        return "agrees" if excludes_zero else "agrees in sign; CI includes 0"
    return "CONTRADICTS (CI excludes 0)" if excludes_zero else "opposite sign; CI includes 0"


def label(f):
    return f"log10({f['name']})" if f["transform"] == "log10" else f["name"]


def level_key(level):
    try:
        return (0, float(level), "")
    except ValueError:
        return (1, 0.0, level)


def descriptive_table(spec, df):
    name, fn = spec["describe_by"]
    levels = pd.Series(fn(df), index=df.index)
    out = []
    for level in sorted(levels.unique(), key=level_key):
        part = df[levels == level]
        k, n = int(part["y"].sum()), len(part)
        lo, hi = models.wilson(k, n)
        out.append({name: level, "n": n, "positives": k, "fraction": k / n, "wilson95": [lo, hi]})
    return out


def groups_of(df):
    key = df[[f for f in ("fuel", "pressure_kpa", "config") if f in df]].astype(str).agg("|".join, axis=1)
    return df["date"].fillna(key).astype(str).to_numpy()


def target_summary(kind, y):
    if kind == "classifier":
        return {"class_counts": {"1": int(y.sum()), "0": int(len(y) - y.sum())}, "positive_fraction": y.mean()}
    return {"min": y.min(), "max": y.max(), "mean": y.mean(), "sd": y.std(ddof=1)}


def frame(spec, tests):
    df, steps = spec["load"](tests)
    names = [f["name"] for f in spec["features"]]
    before = len(df)
    df = df.dropna(subset=names + ["y"])
    if len(df) < before:
        steps.append({"excluded": before - len(df), "why": "missing a feature value"})
    logs = [f["name"] for f in spec["features"] if f["transform"] == "log10"]
    nonpositive = (df[logs] <= 0).any(axis=1)
    if nonpositive.any():
        steps.append({"excluded": int(nonpositive.sum()), "why": "non-positive value of a log-scaled feature"})
        df = df[~nonpositive]
    steps.append({"step": "training rows", "rows": len(df)})
    return df.sort_values("test_id", kind="stable").reset_index(drop=True), steps


def fit_model(spec, tests):
    df, steps = frame(spec, tests)
    feats = spec["features"]
    names = [f["name"] for f in feats]
    raw = df[names].to_numpy(dtype=float)
    X = models.transform(raw, feats)
    kind = spec["kind"]
    y_raw = df["y"].to_numpy(dtype=int if kind == "classifier" else float)
    y = np.log10(y_raw) if spec.get("target_transform") == "log10" else y_raw
    groups = groups_of(df)
    card = {k: spec[k] for k in ("id", "accession", "kind", "question", "target", "target_definition")}
    card["use"] = "descriptive" if spec.get("descriptive") else "predictive"
    card["target_transform"] = spec.get("target_transform")
    card["features"] = []
    for j, f in enumerate(feats):
        entry = {**{k: f[k] for k in ("name", "unit", "transform", "expected_sign", "why")},
                 "domain": [float(raw[:, j].min()), float(raw[:, j].max())]}
        if f.get("allowed"):
            entry["allowed"] = f["allowed"]
        if f.get("untested"):
            entry["untested"] = [{"range": [lo, hi], "n_tests": int(((raw[:, j] >= lo) & (raw[:, j] <= hi)).sum())}
                                 for lo, hi in f["untested"]]
        card["features"].append(entry)
    if spec.get("sum_at_most_one"):
        card["constraints"] = {"sum_at_most_one": spec["sum_at_most_one"]}
    card["training_filter"] = steps
    card["n"] = len(df)
    card["n_groups"] = len(set(groups))
    card["target_summary"] = target_summary(kind, y_raw)
    est = primary(kind).fit(X, y)
    card["estimator"] = describe_estimator(est)
    card["coefficients"] = coefficient_table(spec, est, X, y, groups)
    card["in_sample"] = fold_metrics(kind, y, predict_any(est, X))
    card.update(validation(kind, est, X, y, groups))
    if "sensitivity" in spec:
        card["sensitivity"] = sensitivity(spec, df, X, y, groups)
    card["tree_rules"] = {
        "single_best_feature_rule": tree_text(comparisons(kind)["single_best_feature_rule"], X, y, feats),
        "decision_tree_depth3": tree_text(comparisons(kind)["decision_tree_depth3"], X, y, feats),
    }
    if "describe_by" in spec:
        source = spec["describe_rows"](tests) if "describe_rows" in spec else df
        card["descriptive_table"] = descriptive_table(spec, source)
    card["interpretation"] = spec["interpretation"]
    card["caveats"] = spec["caveats"]
    card["must_not_be_used_for"] = spec["must_not"]
    bundle = {"estimator": est, "X": raw, "y": y_raw,
              "test_ids": df["test_id"].astype(str).tolist(), "features": names}
    return card, bundle


def cfi_reignition_all_pressures(tests):
    """All analysed CFI rows, before the 2 atm cut of the logistic fit."""
    df = cfi(tests)
    df = df[df["n_reignitions"].notna() & df["d0_mm"].notna()]
    return df.assign(y=(df["n_reignitions"] > 0).astype(int))


def validation(kind, est, X, y, groups):
    folds = splits(kind, X, y, groups)
    out = {"cv_scheme": {"grouped_by_date": f"GroupKFold({len(folds['grouped_by_date'])}) by test date",
                         "ungrouped": f"{'Stratified' if kind == 'classifier' else ''}KFold({N_FOLDS}, shuffle, "
                                      f"random_state={SEED})"}}
    cv, comp = {}, {}
    oof_grouped = None
    for scheme, fs in folds.items():
        cv[scheme], oof = cross_validate(est, kind, X, y, fs)
        if scheme == "grouped_by_date":
            oof_grouped = oof
        comp[scheme] = {name: cross_validate(c, kind, X, y, fs)[0] for name, c in comparisons(kind).items()}
    out["cv"] = cv
    out["comparison_cv"] = comp
    metric = "roc_auc" if kind == "classifier" else "r2"
    g = cv["grouped_by_date"][metric]
    interval = metric_interval(kind, X, y, groups)
    out["cv_metric"] = {"name": metric, "grouped_mean": g["mean"], "grouped_sd": g["sd"], "grouped_pooled": g["pooled"],
                        "ungrouped_mean": cv["ungrouped"][metric]["mean"],
                        "folds_without_metric": sum(v is None for v in g["per_fold"]),
                        "grouped_pooled_ci95_days_resampled": interval["ci95"],
                        "grouped_pooled_median_days_resampled": interval["median"],
                        "single_feature_grouped_mean": comp["grouped_by_date"]["single_best_feature_rule"][metric]["mean"],
                        "single_feature_grouped_pooled": comp["grouped_by_date"]["single_best_feature_rule"][metric]["pooled"]}
    if kind == "regressor":
        resid = y - oof_grouped
        out["prediction_interval"] = {
            "residual_quantiles": [float(np.percentile(resid, 5)), float(np.percentile(resid, 95))],
            "method": "5th-95th percentile of grouped out-of-fold residuals, added to the prediction",
        }
    return out


def describe_estimator(est):
    steps = [type(s).__name__ for s in est]
    params = {k: v for k, v in est[-1].get_params().items() if k in ("C", "penalty", "max_iter", "fit_intercept")}
    return {"pipeline": steps, "params": params}


def tree_text(tree, X, y, feats):
    return export_text(clone(tree).fit(X, y), feature_names=[label(f) for f in feats], decimals=3)


# ---------------------------------------------------------------- output

def tidy(o, digits=4):
    if isinstance(o, dict):
        return {str(k): tidy(v, digits) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [tidy(v, digits) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        o = float(o)
        return None if np.isnan(o) else float(f"{o:.{digits}g}")
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def build(tests=None, specs=None):
    tests = load_tests() if tests is None else tests
    cards, bundles = [], {}
    for spec in SPECS if specs is None else specs:
        card, bundle = fit_model(spec, tests)
        cards.append(tidy(card))
        bundles[card["id"]] = bundle
    return {"models": cards, "dropped": DROPPED}, bundles


def write(doc, bundles, out_dir=None, docs_path=None):
    out_dir = psi.PROCESSED if out_dir is None else out_dir
    (out_dir / "models").mkdir(parents=True, exist_ok=True)
    (out_dir / "models.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    for model_id, bundle in bundles.items():
        joblib.dump(bundle, out_dir / "models" / f"{model_id}.joblib")
    (DOCS if docs_path is None else docs_path).write_text(render_markdown(doc))


# ---------------------------------------------------------------- docs/models.md

def fmt(v, digits=3):
    if v is None:
        return "–"
    if isinstance(v, float):
        return f"{v:.{digits}g}"
    return str(v)


def metric_cell(m):
    return f"{fmt(m['mean'])} ± {fmt(m['sd'])} (pooled {fmt(m['pooled'])})"


def results_table(card):
    metrics = list(card["cv"]["grouped_by_date"])
    head = "| model | " + " | ".join(f"{m} grouped" for m in metrics) + " | " + \
           " | ".join(f"{m} ungrouped" for m in metrics) + " |"
    lines = [head, "|" + "---|" * (1 + 2 * len(metrics))]
    rows = [("**logistic / linear (this model)**", card["cv"])]
    rows += [(name, {s: card["comparison_cv"][s][name] for s in card["comparison_cv"]})
             for name in card["comparison_cv"]["grouped_by_date"]]
    for name, cv in rows:
        cells = [metric_cell(cv["grouped_by_date"][m]) for m in metrics] + \
                [metric_cell(cv["ungrouped"][m]) for m in metrics]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def coef_table(card):
    c = card["coefficients"]
    lines = [f"Coefficients on the {c['scale']} scale (per SD of the feature, and per unit of the feature as "
             f"transformed). Intercept per unit: {fmt(c['intercept_per_unit'])}.", "",
             "| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |",
             "|---|---|---|---|---|---|---|"]
    for t in c["terms"]:
        lo, hi = t["per_sd_ci95_cluster_bootstrap"]
        ulo, uhi = t["per_unit_ci95_cluster_bootstrap"]
        lines.append(f"| `{t['feature']}` | {fmt(t['per_sd'])} | [{fmt(lo)}, {fmt(hi)}] | {fmt(t['per_unit'])} | "
                     f"[{fmt(ulo)}, {fmt(uhi)}] | {t['expected_sign']} | {t['agreement']} |")
    return "\n".join(lines)


def describe_table(card):
    rows = card["descriptive_table"]
    key = next(k for k in rows[0] if k not in ("n", "positives", "fraction", "wilson95"))
    lines = [f"| {key} | positives / n | fraction | Wilson 95% |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[key]} | {r['positives']} / {r['n']} | {fmt(r['fraction'], 2)} | "
                     f"[{fmt(r['wilson95'][0], 2)}, {fmt(r['wilson95'][1], 2)}] |")
    return "\n".join(lines)


def filter_lines(card):
    out = []
    for s in card["training_filter"]:
        if "step" in s:
            out.append(f"- {s['step']}: {s['rows']}")
        elif s["excluded"]:
            out.append(f"- excluded {s['excluded']}: {s['why']}")
    return "\n".join(out)


def section(card, spec):
    ts = card["target_summary"]
    balance = (f"{ts['class_counts']['1']} positive / {ts['class_counts']['0']} negative"
               if "class_counts" in ts else f"range {fmt(ts['min'])}-{fmt(ts['max'])}, mean {fmt(ts['mean'])}")
    feats = "\n".join(f"- `{f['name']}` ({f['unit']}{', log10' if f['transform'] else ''}; training range "
                      f"{fmt(f['domain'][0])}-{fmt(f['domain'][1])}): expected **{f['expected_sign']}**, {f['why']}."
                      for f in card["features"])
    parts = [
        f"## `{card['id']}` ({card['accession']}, {card['kind']})",
        f"**Question.** {card['question']}",
        f"**Target.** `{card['target']}`: {card['target_definition']}. n = {card['n']} tests on "
        f"{card['n_groups']} test days; {balance}.",
        f"**Physics expectation.** {spec['physics']}",
        f"$$\n{spec['scaling']}\n$$",
        feats,
        "**Training rows.**\n\n" + filter_lines(card),
    ]
    if card["use"] == "descriptive":
        parts.append("**Use: descriptive only.** `predict` returns no prediction for this model, only the nearest "
                     "real tests. The cross-validation below is shown to justify that choice.")
    parts.append("**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in "
                 "brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap "
                 "between the two is the optimism from same-day tests sharing conditions.\n\n"
                 + results_table(card))
    m = card["cv_metric"]
    lo, hi = m["grouped_pooled_ci95_days_resampled"]
    spread = (f"**How sure is the headline number?** Resampling the {card['n_groups']} test days and rerunning the "
              f"grouped cross-validation {N_BOOT_CV} times puts the pooled {m['name']} between {fmt(lo, 2)} and "
              f"{fmt(hi, 2)} (95%, median {fmt(m['grouped_pooled_median_days_resampled'], 2)}). The single best "
              f"feature alone reaches {fmt(m['single_feature_grouped_mean'], 2)} (pooled "
              f"{fmt(m['single_feature_grouped_pooled'], 2)}).")
    if m["folds_without_metric"]:
        spread += (f" {m['folds_without_metric']} of the {len(card['cv']['grouped_by_date'][m['name']]['per_fold'])} "
                   f"held-out folds contain a single outcome class, where {m['name']} is undefined; the fold mean is "
                   "over the remaining folds, so the pooled value is the safer number.")
    parts.append(spread)
    if card.get("target_transform") == "log10":
        parts.append(f"Errors (MAE, residuals) of this model are in log10 of the target: an MAE of "
                     f"{fmt(card['cv']['grouped_by_date']['mae']['mean'], 2)} is a factor of "
                     f"{fmt(10 ** card['cv']['grouped_by_date']['mae']['mean'], 2)}.")
    parts.append(coef_table(card))
    if "sensitivity" in card:
        s = card["sensitivity"]
        terms = {t["feature"]: t["per_unit"] for t in card["coefficients"]["terms"]}
        rows = "\n".join(f"| `{k}` | {fmt(terms[k])} | {fmt(v)} |" for k, v in s["per_unit"].items())
        parts.append(f"**Sensitivity.** Refitted without {s['without']} ({s['excluded']} rows left out, n = {s['n']}; "
                     f"grouped {s['metric']} {fmt(s['grouped_mean'])}, pooled {fmt(s['grouped_pooled'])}). "
                     "Coefficients per unit:\n\n| feature | all rows | without them |\n|---|---|---|\n" + rows)
    parts.append(f"**Does it match the physics?** {card['interpretation']}")
    parts.append("Single-best-feature rule (depth-1 tree on all rows):\n\n```\n"
                 + card["tree_rules"]["single_best_feature_rule"] + "```")
    if "descriptive_table" in card:
        parts.append("Observed fractions with Wilson 95% intervals:\n\n" + describe_table(card))
    parts.append("**Caveats.**\n\n" + "\n".join(f"- {c}" for c in card["caveats"]))
    parts.append("**Must not be used for.**\n\n" + "\n".join(f"- {c}" for c in card["must_not_be_used_for"]))
    return "\n\n".join(parts)


HEADER = """# Outcome models

Small, interpretable models of test outcomes, one investigation at a time. They are never pooled
across investigations: hardware, fuels and procedures differ. Built by `fif/pipeline/build_models.py`
(`uv run python -m fif.pipeline.build_models`) from `data/processed/tests.parquet`; cards in
`data/processed/models.json`, fitted estimators in `data/processed/models/<id>.joblib`, and
`fif.models.predict(model_id, **conditions)` for the dashboard. This page is generated: edit the specs in
the build script, not this file.

Method, common to all models:

- Estimator: standardised features into logistic regression (C = 1, L2) or ordinary least squares.
  Features are physically motivated and log-transformed where the physics is multiplicative (pressure,
  flows). Comparison lines: majority class or mean predictor, the single best feature (a depth-1 tree),
  a depth-3 tree, and gradient boosting (to show what the simple model leaves on the table).
- Validation: `GroupKFold` grouped by test date, because tests run on the same day share fills, hardware
  state and conditions; plain (stratified) shuffled K-fold is shown alongside so the optimism is visible.
  All random states are fixed (0).
- Uncertainty of the headline metric: the test days are resampled with replacement and the grouped
  cross-validation rerun (200 times); the 95% range of the pooled out-of-fold metric is quoted next to every
  headline number. With 11-12 test days the ranges of the CFI-G classifiers are wide: quote them, not the
  point value. A held-out fold with a single outcome class has no AUC and is left out of the fold mean (counted
  on each card).
- Coefficient intervals: cluster bootstrap by test date (300 resamples). "Agrees" means the sign matches
  the physics expectation and the interval excludes 0.
- Outcome-derived columns (burn time, burner temperature, extinction diameter for a mode, etc.) are never
  features. Rows flagged on a field the model uses are excluded and counted under *Training rows*.
- `predict` returns `prediction = None` outside the per-feature training range, and inside a range a card
  lists as untested (too few tests), unless the caller asks to extrapolate; it always returns the nearest real
  tests and refuses impossible inputs (mole fractions summing over 1, a fuel indicator other than 0 or 1). The per-feature range does not protect
  against untested *combinations*; check the nearest-test distances.
"""


def render_markdown(doc):
    specs = {s["id"]: s for s in SPECS}
    body = [HEADER, "## Summary", summary_table(doc)]
    body += [section(card, specs[card["id"]]) for card in doc["models"]]
    body.append("## Candidates dropped\n\n" + "\n".join(
        f"- `{d['id']}` ({d['accession']}): {d['reason']}" for d in doc["dropped"]))
    return "\n\n".join(body) + "\n"


def summary_table(doc):
    lines = ["| model | use | n | metric | grouped (mean ± SD) | 95% interval, days resampled (pooled) | ungrouped | baseline (grouped) | gradient boosting (grouped) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for c in doc["models"]:
        m = c["cv_metric"]["name"]
        comp = c["comparison_cv"]["grouped_by_date"]
        base = comp.get("majority_class", comp.get("mean_predictor"))[m]
        rule = comp["single_best_feature_rule"][m]
        lines.append(f"| `{c['id']}` | {c['use']} | {c['n']} | {m} | {fmt(c['cv_metric']['grouped_mean'])} ± "
                     f"{fmt(c['cv_metric']['grouped_sd'])} | {fmt(c['cv_metric']['grouped_pooled_ci95_days_resampled'][0], 2)}"
                     f" to {fmt(c['cv_metric']['grouped_pooled_ci95_days_resampled'][1], 2)} | "
                     f"{fmt(c['cv_metric']['ungrouped_mean'])} | "
                     f"{fmt(base['mean'])} (single feature {fmt(rule['mean'])}) | "
                     f"{fmt(comp['gradient_boosting'][m]['mean'])} |")
    return "\n".join(lines)


if __name__ == "__main__":
    doc, bundles = build()
    write(doc, bundles)
    for c in doc["models"]:
        print(c["id"], c["use"], c["n"], c["cv_metric"])
