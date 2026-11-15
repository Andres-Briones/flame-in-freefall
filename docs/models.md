# Outcome models

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
- Coefficient intervals: cluster bootstrap by test date (300 resamples). Each refit is converted to per-unit
  coefficients with the scaler of its own resample; the per-SD interval is that same interval multiplied by the
  feature's SD over all training rows, so both columns and the verdict describe one interval. "Agrees" means the
  sign matches the physics expectation and the interval excludes 0.
- Prediction range (regressors): the 5th and 95th percentile of the grouped out-of-fold residuals, added to the
  prediction. 90% is its target. The coverage actually reached is measured by nested grouped cross-validation
  (the range of a held-out day is rebuilt from the other days only) and given on each card as counts; a share is
  called below or above 90% when its Wilson 95% interval excludes 0.90. A range is cut at 0 where the quantity
  cannot be negative, and the cuts are counted.
- Probabilities (classifiers): the Brier score on held-out days is given next to the AUC, with the Brier score of
  always giving the base rate for comparison. AUC ranks; Brier also penalises miscalibrated probabilities.
- Outcome-derived columns (burn time, burner temperature, extinction diameter for a mode, etc.) are never
  features. Rows flagged on a field the model uses are excluded and counted under *Training rows*.
- `predict` returns `prediction = None` outside the per-feature training range, and inside a range a card
  lists as untested (too few tests), unless the caller asks to extrapolate; it always returns the nearest real
  tests and refuses impossible inputs (mole fractions summing over 1, a fuel indicator other than 0 or 1). The per-feature range does not protect
  against untested *combinations*; check the nearest-test distances.


## Summary

| model | use | n | metric | grouped (mean ± SD) | 95% interval, days resampled (pooled) | ungrouped | baseline (grouped) | gradient boosting (grouped) |
|---|---|---|---|---|---|---|---|---|
| `cfig_normal_self_extinction` | predictive | 133 | roc_auc | 0.838 ± 0.0676 | 0.47 to 0.87 | 0.846 | 0.5 (single feature 0.599) | 0.82 |
| `cfig_inverse_self_extinction` | predictive | 131 | roc_auc | 0.831 ± 0.145 | 0.57 to 0.95 | 0.912 | 0.5 (single feature 0.56) | 0.701 |
| `cfig_normal_ignition` | descriptive | 177 | roc_auc | 0.614 ± 0.176 | 0.11 to 0.82 | 0.784 | 0.5 (single feature 0.474) | 0.726 |
| `cfig_inverse_ignition` | descriptive | 146 | roc_auc | 0.852 ± 0.145 | 0.36 to 0.88 | 0.828 | 0.5 (single feature 0.765) | 0.743 |
| `flex_burning_rate` | predictive | 251 | r2 | 0.686 ± 0.0934 | 0.63 to 0.8 | 0.766 | -0.212 (single feature -0.291) | 0.53 |
| `flex_methanol_extinction_diameter` | predictive | 100 | r2 | 0.697 ± 0.113 | 0.13 to 0.76 | 0.705 | -0.0179 (single feature 0.353) | 0.735 |
| `cfi_reignition` | descriptive | 62 | roc_auc | 0.51 ± 0.355 | 0.12 to 0.83 | 0.703 | 0.5 (single feature 0.294) | 0.392 |
| `spice_smoke_point_length` | descriptive | 23 | r2 | -45.2 ± 61.7 | -4.6 to 0.2 | -0.179 | -49.6 (single feature -77) | -169 |

## `cfig_normal_self_extinction` (PSI-159, classifier)

**Question.** Once a normal (fuel-from-burner) spherical gas flame is lit, does it go out on its own (radiative self-extinction) before the scripted flow cut-off?

**Target.** `self_extinguished`: 1 if extinction_mode == 'self_extinguished', 0 if 'flow_terminated' (flow cut by the script timeout or the burner temperature limit). n = 133 tests on 11 test days; 102 positive / 31 negative.

**Physics expectation.** These flames die by radiative loss, not by a residence-time (Damköhler) limit: the flame grows slowly in quiescent microgravity, radiates from soot and gas, and goes out when the radiative loss fraction drives T_f to about 1100-1200 K.

$$
\chi_r=\frac{\dot Q_{rad}}{\dot Q_{chem}}\sim\frac{\kappa_P\,\sigma T_f^{4}\,r_f^{3}}{\dot m_F\,\Delta h_c},\qquad r_f\propto\frac{\dot m}{4\pi\rho D\,\ln\!\left(1/(1-Z_{st})\right)}
$$

- `x_o2_ambient` (mole fraction; training range 0.18-0.4): expected **-**, more O2 raises T_f and heat release relative to radiation.
- `pressure_kpa` (kPa, log10; training range 50.7-304): expected **+**, soot and gas radiation grow with pressure.
- `fuel_flow_mg_s` (mg/s, log10; training range 0.125-3.21): expected **+**, flame radius grows with fuel flow, radiative loss ~ r_f^3 against heat release ~ mdot, so chi_r rises.
- `fuel_fraction` (mole fraction (burner stream); training range 0.031-1): expected **?**, dilution lowers T_ad (favours extinction) but also lowers soot (favours survival).
- `n_carbon` (C atoms (2 ethane, 3 propane, 4 n-butane); training range 2-4): expected **+**, larger alkanes soot more.

**Training rows.**

- PSI-159 normal-flame tests: 179
- excluded 46: no established hot flame (ignited False): there is nothing to extinguish (21106 F4 is kept: the table logs it as not ignited, the raw data show a 20 s flame, patch D03)
- training rows: 133

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | roc_auc grouped | brier grouped | balanced_accuracy grouped | roc_auc ungrouped | brier ungrouped | balanced_accuracy ungrouped |
|---|---|---|---|---|---|---|
| **logistic / linear (this model)** | 0.838 ± 0.0676 (pooled 0.808) | 0.136 ± 0.0279 (pooled 0.137) | 0.725 ± 0.0961 (pooled 0.709) | 0.846 ± 0.111 (pooled 0.85) | 0.124 ± 0.0358 (pooled 0.124) | 0.687 ± 0.0409 (pooled 0.69) |
| majority_class | 0.5 ± 0 (pooled 0.397) | 0.181 ± 0.0401 (pooled 0.181) | 0.5 ± 0 (pooled 0.5) | 0.5 ± 0 (pooled 0.481) | 0.179 ± 0.00829 (pooled 0.179) | 0.5 ± 0 (pooled 0.5) |
| single_best_feature_rule | 0.599 ± 0.104 (pooled 0.549) | 0.19 ± 0.0221 (pooled 0.19) | 0.55 ± 0.112 (pooled 0.494) | 0.603 ± 0.153 (pooled 0.578) | 0.18 ± 0.0413 (pooled 0.18) | 0.5 ± 0 (pooled 0.5) |
| decision_tree_depth3 | 0.739 ± 0.181 (pooled 0.719) | 0.144 ± 0.0769 (pooled 0.146) | 0.766 ± 0.16 (pooled 0.743) | 0.845 ± 0.0828 (pooled 0.844) | 0.12 ± 0.042 (pooled 0.12) | 0.728 ± 0.0901 (pooled 0.727) |
| gradient_boosting | 0.82 ± 0.104 (pooled 0.769) | 0.16 ± 0.0865 (pooled 0.164) | 0.718 ± 0.167 (pooled 0.689) | 0.892 ± 0.105 (pooled 0.885) | 0.106 ± 0.0464 (pooled 0.106) | 0.772 ± 0.116 (pooled 0.778) |

**How sure is the headline number?** Resampling the 11 test days and rerunning the grouped cross-validation 200 times puts the pooled roc_auc between 0.47 and 0.87 (95%, median 0.74). The single best feature alone reaches 0.6 (pooled 0.55). Brier score of the probabilities on held-out days (pooled, lower is better): 0.137, against 0.181 for always giving the training days' base rate.

Coefficients on the log-odds scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: 9.96.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `x_o2_ambient` | -1.97 | [-2.54, -1.29] | -24.5 | [-31.7, -16.1] | - | agrees |
| `log10(pressure_kpa)` | 0.0185 | [-0.683, 0.624] | 0.0848 | [-3.13, 2.86] | + | agrees in sign; CI includes 0 |
| `log10(fuel_flow_mg_s)` | 1.34 | [0.635, 2.57] | 5.54 | [2.62, 10.6] | + | agrees |
| `fuel_fraction` | -0.278 | [-1.38, 0.155] | -0.985 | [-4.87, 0.549] | ? | no prior expectation |
| `n_carbon` | 0.0289 | [-1.48, 0.64] | 0.0348 | [-1.78, 0.77] | + | agrees in sign; CI includes 0 |

**Does it match the physics?** Partly. Ambient O2 (-) and fuel flow (+, larger flame, more radiative loss) agree, with intervals excluding 0; these two carry the model. Pressure and carbon number are indistinguishable from 0: within these tests, radiative self-extinction does not measurably depend on pressure once O2 and flow are fixed. The depth-3 tree and gradient boosting do no better on held-out days, so the linear form leaves little on the table.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- x_o2_ambient <= 0.283
|   |--- class: 1
|--- x_o2_ambient >  0.283
|   |--- class: 1
```

Observed fractions with Wilson 95% intervals:

| o2_band | positives / n | fraction | Wilson 95% |
|---|---|---|---|
| about 0.21 | 41 / 41 | 1 | [0.91, 1] |
| about 0.33 | 1 / 3 | 0.33 | [0.061, 0.79] |
| about 0.40 | 60 / 89 | 0.67 | [0.57, 0.76] |

**Caveats.**

- 'Flow-terminated' is not 'stable': flow was cut by scripted timeouts or burner over-temperature, so the target is 'self-extinguished before the cut-off', and the fractions depend on the chosen timeouts.
- At about 21% ambient O2 every lit flame self-extinguished (quasi-complete separation); the coefficients mainly describe the about 40% O2 tests. Only 3 tests sit at about 33% O2.
- Chamber composition drifts during a day (closed chamber); x_o2_ambient is the tabulated estimate, not a gas-chromatograph measurement. Mass flow controllers are poor below 10% of full scale.
- Burner temperature (which lengthens burns) is not a feature: it is an outcome of the burn.

**Must not be used for.**

- material flammability, cabin fires or condensed fuels
- other burners or flow timeouts (the target is tied to this hardware's cut-off times)
- O2 between 0.25 and 0.35 (3 tests) or any combination not near a listed nearest test

## `cfig_inverse_self_extinction` (PSI-159, classifier)

**Question.** Once an inverse (oxidiser-from-burner, fuel ambient) flame is lit, does it self-extinguish before the flow cut-off, and how strongly does chamber pressure matter?

**Target.** `self_extinguished`: 1 if extinction_mode == 'self_extinguished', 0 if 'flow_terminated' (usually the 66 s inverse timeout, sometimes the burner temperature limit). n = 131 tests on 12 test days; 73 positive / 58 negative.

**Physics expectation.** Same radiative-loss balance as normal flames, but the soot forms on the outside of the flame. Raising pressure increases soot and radiating-gas density, so radiative extinction should become more likely with pressure.

$$
\chi_r=\frac{\dot Q_{rad}}{\dot Q_{chem}}\sim\frac{\kappa_P\,\sigma T_f^{4}\,r_f^{3}}{\dot m_F\,\Delta h_c},\qquad r_f\propto\frac{\dot m}{4\pi\rho D\,\ln\!\left(1/(1-Z_{st})\right)}
$$

- `pressure_kpa` (kPa (table values, ~9% above nominal fill), log10; training range 49.5-331): expected **+**, soot forms outside the inverse flame in the hot fuel-rich gas; radiation grows with pressure.
- `x_o2_burner` (mole fraction (burner stream); training range 0.15-0.85): expected **-**, more O2 in the burner stream raises T_ad.
- `o2_flow_mg_s` (mg/s, log10; training range 1.34-9.08): expected **+**, O2 is the limiting reactant, so O2 flow sets the flame size and hence radiative loss.
- `n_carbon` (C atoms (2 ethane, 3 propane, 4 n-butane); training range 2-4): expected **+**, larger alkanes soot more.

**Training rows.**

- PSI-159 inverse-flame tests: 154
- excluded 8: flash_only: a ~1 s momentary flame is a failed ignition, not a radiative extinction of an established flame
- excluded 15: no hot ignition
- training rows: 131

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | roc_auc grouped | brier grouped | balanced_accuracy grouped | roc_auc ungrouped | brier ungrouped | balanced_accuracy ungrouped |
|---|---|---|---|---|---|---|
| **logistic / linear (this model)** | 0.831 ± 0.145 (pooled 0.872) | 0.144 ± 0.0768 (pooled 0.141) | 0.753 ± 0.174 (pooled 0.794) | 0.912 ± 0.0643 (pooled 0.898) | 0.12 ± 0.0438 (pooled 0.12) | 0.798 ± 0.0735 (pooled 0.797) |
| majority_class | 0.5 ± 0 (pooled 0.167) | 0.303 ± 0.118 (pooled 0.308) | 0.4 ± 0.224 (pooled 0.368) | 0.5 ± 0 (pooled 0.481) | 0.247 ± 0.00219 (pooled 0.247) | 0.5 ± 0 (pooled 0.5) |
| single_best_feature_rule | 0.56 ± 0.051 (pooled 0.712) | 0.235 ± 0.0482 (pooled 0.233) | 0.648 ± 0.202 (pooled 0.72) | 0.787 ± 0.0715 (pooled 0.793) | 0.162 ± 0.0388 (pooled 0.161) | 0.787 ± 0.0715 (pooled 0.79) |
| decision_tree_depth3 | 0.652 ± 0.104 (pooled 0.635) | 0.297 ± 0.11 (pooled 0.302) | 0.586 ± 0.157 (pooled 0.58) | 0.868 ± 0.0559 (pooled 0.84) | 0.161 ± 0.0434 (pooled 0.161) | 0.709 ± 0.0736 (pooled 0.709) |
| gradient_boosting | 0.701 ± 0.194 (pooled 0.785) | 0.209 ± 0.0867 (pooled 0.205) | 0.677 ± 0.15 (pooled 0.715) | 0.902 ± 0.0553 (pooled 0.883) | 0.135 ± 0.0419 (pooled 0.134) | 0.787 ± 0.0692 (pooled 0.788) |

**How sure is the headline number?** Resampling the 12 test days and rerunning the grouped cross-validation 200 times puts the pooled roc_auc between 0.57 and 0.95 (95%, median 0.83). The single best feature alone reaches 0.56 (pooled 0.71). 1 of the 5 held-out folds contain a single outcome class, where roc_auc is undefined; the fold mean is over the remaining folds, so the pooled value is the safer number. Brier score of the probabilities on held-out days (pooled, lower is better): 0.141, against 0.308 for always giving the training days' base rate.

Coefficients on the log-odds scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: -14.3.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `log10(pressure_kpa)` | 1.95 | [1.1, 2.77] | 6.73 | [3.81, 9.58] | + | agrees |
| `x_o2_burner` | 0.875 | [0.494, 1.39] | 3.34 | [1.89, 5.3] | - | CONTRADICTS (CI excludes 0) |
| `log10(o2_flow_mg_s)` | -0.488 | [-1.34, 0.427] | -2.05 | [-5.62, 1.8] | + | opposite sign; CI includes 0 |
| `n_carbon` | -0.224 | [-0.788, 0.692] | -0.266 | [-0.936, 0.822] | + | opposite sign; CI includes 0 |

**Does it match the physics?** Pressure agrees strongly (+) and is the largest term (a pressure split alone gives a pooled held-out AUC of 0.71 against 0.87 for the full model; gradient boosting does worse on held-out days), matching 0/29 self-extinctions at 0.5-0.6 bar against 58/67 at 2.2-3.3 bar. Burner-stream O2 has the opposite sign to the a-priori expectation (-): richer oxidiser streams self-extinguished more often. This is a property of the test design, not a mechanism: the O2 mass flow was held roughly fixed, so a richer burner stream means a smaller total burner flow (correlation about -0.66 between burner O2 and the log of the estimated total flow). The sign stays positive within each pressure level and with day fixed effects, and it becomes indistinguishable from 0 once total flow is added, so the data cannot separate burner O2 from total flow. O2 flow and carbon number are indistinguishable from 0.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- log10(pressure_kpa) <= 2.193
|   |--- class: 0
|--- log10(pressure_kpa) >  2.193
|   |--- class: 1
```

Observed fractions with Wilson 95% intervals:

| pressure_level_kpa | positives / n | fraction | Wilson 95% |
|---|---|---|---|
| 50 | 0 / 3 | 0 | [0, 0.56] |
| 60 | 0 / 26 | 0 | [0, 0.13] |
| 110 | 15 / 35 | 0.43 | [0.28, 0.59] |
| 220 | 31 / 35 | 0.89 | [0.74, 0.95] |
| 330 | 27 / 32 | 0.84 | [0.68, 0.93] |

**Caveats.**

- All inverse rows carry pressure_9pct_above_nominal: the table pressures are ~9% above the fill levels. Used as given: a uniform multiplicative offset only shifts the intercept of log10(pressure).
- Pressure and O2 flow are partly confounded with test day: pressure levels were run on separate days, so the grouped CV can only test pressure on held-out days with other pressures.
- 79 of 154 inverse tests used 85% O2 in the burner stream; low burner-O2 cells are small.
- Ambient fuel fraction is left out: it was lowered as pressure was raised (r = -0.72 with pressure in the training rows), so the two cannot be separated and the fit would split the pressure effect between them.
- As for normal flames, 'flow_terminated' is a timeout outcome, not a stability limit.

**Must not be used for.**

- normal flames or real fires (an inverse flame has no fire-safety analogue in a cabin)
- pressures outside 0.5-3.3 bar or other burners

## `cfig_normal_ignition` (PSI-159, classifier)

**Question.** Does a normal flame light (hot ignition) for a given chamber O2, pressure and fuel stream?

**Target.** `ignited`: 1 if the table's 'Hot ignition' is yes, 0 if no. n = 177 tests on 11 test days; 133 positive / 44 negative.

**Physics expectation.** Ignition succeeds when chemistry is fast compared with transport away from the igniter: a Damköhler-number criterion. Dilution and low O2 lower the flame temperature and slow chemistry.

$$
\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}},\qquad \tau_{chem}^{-1}\propto p^{\,n-1}\exp\!\left(-\frac{E_a}{R T_f}\right)
$$

- `x_o2_ambient` (mole fraction; training range 0.18-0.4): expected **+**, faster chemistry and hotter flame (Damköhler number up).
- `pressure_kpa` (kPa, log10; training range 50.7-304): expected **+**, reaction rate ~ p^n with n ~ 2 for chain branching, so Da rises.
- `fuel_flow_mg_s` (mg/s, log10; training range 0.1-3.21): expected **+**, more fuel near the igniter.
- `fuel_fraction` (mole fraction (burner stream), log10; training range 0.0183-1): expected **+**, heavily diluted fuel gives a cool, weak mixture near the igniter.
- `n_carbon` (C atoms; training range 2-4): expected **?**, no clear expectation across C2-C4 alkanes.

**Training rows.**

- PSI-159 normal-flame tests: 179
- excluded 2: zero fuel fraction and zero fuel flow (21125 A4, H3): no fuel was supplied
- training rows: 177

**Use: descriptive only.** `predict` returns no prediction for this model, only the nearest real tests. The cross-validation below is shown to justify that choice.

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | roc_auc grouped | brier grouped | balanced_accuracy grouped | roc_auc ungrouped | brier ungrouped | balanced_accuracy ungrouped |
|---|---|---|---|---|---|---|
| **logistic / linear (this model)** | 0.614 ± 0.176 (pooled 0.565) | 0.214 ± 0.107 (pooled 0.207) | 0.604 ± 0.221 (pooled 0.519) | 0.784 ± 0.0685 (pooled 0.781) | 0.153 ± 0.00878 (pooled 0.153) | 0.627 ± 0.0626 (pooled 0.625) |
| majority_class | 0.5 ± 0 (pooled 0.248) | 0.21 ± 0.0883 (pooled 0.205) | 0.6 ± 0.224 (pooled 0.5) | 0.5 ± 0 (pooled 0.486) | 0.187 ± 0.00582 (pooled 0.187) | 0.5 ± 0 (pooled 0.5) |
| single_best_feature_rule | 0.474 ± 0.0515 (pooled 0.3) | 0.229 ± 0.133 (pooled 0.22) | 0.6 ± 0.224 (pooled 0.5) | 0.657 ± 0.05 (pooled 0.66) | 0.152 ± 0.0226 (pooled 0.152) | 0.657 ± 0.05 (pooled 0.655) |
| decision_tree_depth3 | 0.63 ± 0.139 (pooled 0.508) | 0.235 ± 0.154 (pooled 0.225) | 0.582 ± 0.126 (pooled 0.481) | 0.849 ± 0.0679 (pooled 0.843) | 0.123 ± 0.0191 (pooled 0.123) | 0.655 ± 0.053 (pooled 0.652) |
| gradient_boosting | 0.726 ± 0.057 (pooled 0.66) | 0.214 ± 0.151 (pooled 0.203) | 0.643 ± 0.223 (pooled 0.549) | 0.917 ± 0.0528 (pooled 0.917) | 0.101 ± 0.027 (pooled 0.101) | 0.745 ± 0.081 (pooled 0.747) |

**How sure is the headline number?** Resampling the 11 test days and rerunning the grouped cross-validation 200 times puts the pooled roc_auc between 0.11 and 0.82 (95%, median 0.46). The single best feature alone reaches 0.47 (pooled 0.3). 1 of the 5 held-out folds contain a single outcome class, where roc_auc is undefined; the fold mean is over the remaining folds, so the pooled value is the safer number. Brier score of the probabilities on held-out days (pooled, lower is better): 0.207, against 0.205 for always giving the training days' base rate.

Coefficients on the log-odds scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: 0.662.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `x_o2_ambient` | 0.587 | [0.16, 1.36] | 7.1 | [1.94, 16.5] | + | agrees |
| `log10(pressure_kpa)` | 0.223 | [-0.37, 0.783] | 1.05 | [-1.74, 3.7] | + | agrees in sign; CI includes 0 |
| `log10(fuel_flow_mg_s)` | 0.369 | [-0.398, 1.57] | 1.38 | [-1.49, 5.88] | + | agrees in sign; CI includes 0 |
| `log10(fuel_fraction)` | 0.593 | [-2.31, 1.46] | 1.24 | [-4.83, 3.06] | + | agrees in sign; CI includes 0 |
| `n_carbon` | -0.71 | [-1.95, 0.0528] | -0.891 | [-2.45, 0.0663] | ? | no prior expectation |

**Does it match the physics?** O2 agrees (+, interval excludes 0); pressure, flow and dilution agree in sign only. The robust statement is the dilution table: 14/38 ignitions below 0.05 fuel fraction against 118/139 above. The fit does not generalise to held-out days (grouped AUC near chance), because the failures cluster on a few days with modified igniter settings.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- log10(fuel_fraction) <= -1.537
|   |--- class: 0
|--- log10(fuel_fraction) >  -1.537
|   |--- class: 1
```

Observed fractions with Wilson 95% intervals:

| fuel_fraction_band | positives / n | fraction | Wilson 95% |
|---|---|---|---|
| < 0.05 | 14 / 38 | 0.37 | [0.23, 0.53] |
| >= 0.05 | 119 / 139 | 0.86 | [0.79, 0.9] |

**Caveats.**

- Igniter energy was deliberately lowered in some tests to try direct cool-flame ignition (final report); igniter settings are not in the table, so some failures are by design and look like condition effects.
- Mass flow controllers are poor below 10% of full scale, which is where most diluted, low-flow failures sit.
- Failures cluster by day: all 45 fall on 6 of 11 test days (12 Apr - 11 Jun 2021), 44 of them on 5, and the grouped CV (held-out days) is close to chance. Kept as a descriptive table, not a predictor.

**Must not be used for.**

- flammability limits of materials or of premixed gases
- igniters other than the ACME hot-wire igniter at standard settings

## `cfig_inverse_ignition` (PSI-159, classifier)

**Question.** Does an inverse flame light, given the burner-stream O2 and chamber pressure?

**Target.** `ignited`: 1 if 'Hot ignition' is yes, 0 if no ('flash' rows excluded). n = 146 tests on 12 test days; 131 positive / 15 negative.

**Physics expectation.** As for normal flames, a Damköhler-number criterion; here the burner O2 fraction sets T_ad.

$$
\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}}
$$

- `x_o2_burner` (mole fraction (burner stream); training range 0.12-0.85): expected **+**, a richer oxidiser stream gives a hotter, faster-reacting mixture at the igniter.
- `pressure_kpa` (kPa (table values), log10; training range 49.5-331): expected **+**, Da rises with pressure.

**Training rows.**

- PSI-159 inverse-flame tests: 154
- excluded 8: flash_only: momentary flame, neither a clean ignition nor a failure
- training rows: 146

**Use: descriptive only.** `predict` returns no prediction for this model, only the nearest real tests. The cross-validation below is shown to justify that choice.

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | roc_auc grouped | brier grouped | balanced_accuracy grouped | roc_auc ungrouped | brier ungrouped | balanced_accuracy ungrouped |
|---|---|---|---|---|---|---|
| **logistic / linear (this model)** | 0.852 ± 0.145 (pooled 0.761) | 0.0946 ± 0.0737 (pooled 0.1) | 0.517 ± 0.0373 (pooled 0.514) | 0.828 ± 0.074 (pooled 0.808) | 0.0768 ± 0.0061 (pooled 0.0768) | 0.5 ± 0 (pooled 0.5) |
| majority_class | 0.5 ± 0 (pooled 0.283) | 0.092 ± 0.0754 (pooled 0.0961) | 0.5 ± 0 (pooled 0.5) | 0.5 ± 0 (pooled 0.497) | 0.0922 ± 0.00122 (pooled 0.0922) | 0.5 ± 0 (pooled 0.5) |
| single_best_feature_rule | 0.765 ± 0.2 (pooled 0.722) | 0.0964 ± 0.0825 (pooled 0.102) | 0.5 ± 0 (pooled 0.5) | 0.793 ± 0.14 (pooled 0.735) | 0.0795 ± 0.0175 (pooled 0.0794) | 0.5 ± 0 (pooled 0.5) |
| decision_tree_depth3 | 0.716 ± 0.269 (pooled 0.517) | 0.125 ± 0.113 (pooled 0.134) | 0.483 ± 0.0373 (pooled 0.481) | 0.815 ± 0.0959 (pooled 0.798) | 0.0854 ± 0.0244 (pooled 0.0853) | 0.57 ± 0.135 (pooled 0.57) |
| gradient_boosting | 0.743 ± 0.254 (pooled 0.606) | 0.119 ± 0.113 (pooled 0.129) | 0.483 ± 0.0373 (pooled 0.481) | 0.777 ± 0.149 (pooled 0.745) | 0.09 ± 0.0362 (pooled 0.0898) | 0.632 ± 0.13 (pooled 0.632) |

**How sure is the headline number?** Resampling the 12 test days and rerunning the grouped cross-validation 200 times puts the pooled roc_auc between 0.36 and 0.88 (95%, median 0.75). The single best feature alone reaches 0.77 (pooled 0.72). Brier score of the probabilities on held-out days (pooled, lower is better): 0.1, against 0.0961 for always giving the training days' base rate.

Coefficients on the log-odds scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: -2.33.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `x_o2_burner` | 1.19 | [0.565, 2.22] | 4.3 | [2.04, 7.98] | + | agrees |
| `log10(pressure_kpa)` | 0.353 | [-0.314, 1.06] | 1.19 | [-1.06, 3.58] | + | agrees in sign; CI includes 0 |

**Does it match the physics?** Burner O2 agrees (+) on average, but the table shows the effect is not monotone: the failures concentrate at 0.21 burner O2, while the few lower-O2 tests mostly lit.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- x_o2_burner <= 0.350
|   |--- class: 1
|--- x_o2_burner >  0.350
|   |--- class: 1
```

Observed fractions with Wilson 95% intervals:

| x_o2_burner_level | positives / n | fraction | Wilson 95% |
|---|---|---|---|
| 0.12 | 0 / 1 | 0 | [0, 0.79] |
| 0.15 | 3 / 3 | 1 | [0.44, 1] |
| 0.18 | 2 / 2 | 1 | [0.34, 1] |
| 0.19 | 1 / 1 | 1 | [0.21, 1] |
| 0.21 | 16 / 26 | 0.62 | [0.43, 0.78] |
| 0.3 | 6 / 8 | 0.75 | [0.41, 0.93] |
| 0.4 | 3 / 3 | 1 | [0.44, 1] |
| 0.45 | 1 / 1 | 1 | [0.21, 1] |
| 0.5 | 22 / 22 | 1 | [0.85, 1] |
| 0.7 | 1 / 1 | 1 | [0.21, 1] |
| 0.85 | 76 / 78 | 0.97 | [0.91, 0.99] |

**Caveats.**

- Only 15 non-ignitions, 10 of them at 0.21 burner O2; the fit is close to a lookup of that cell. Read the descriptive table first.
- Igniter settings varied and are not in the table.
- Not monotone in burner O2: 6 of 7 tests at 0.15-0.19 ignited while 10 of 26 at 0.21 failed, so a logistic curve in O2 misdescribes the low end. Kept as a descriptive table.

**Must not be used for.**

- normal flames
- any fire-safety ignition criterion

## `flex_burning_rate` (PSI-69, regressor)

**Question.** How fast does a free methanol or n-heptane droplet burn (d²-law constant K) in a given atmosphere?

**Target.** `burn_rate_k_mm2_s`: average burning-rate constant K (mm²/s) of the d²-law d² = d0² - K t, as tabulated. n = 251 tests on 79 test days; range 0.05-1.06, mean 0.503.

**Physics expectation.** Quasi-steady droplet burning gives the d²-law with K set by gas conductivity, liquid properties and the Spalding transfer number B, which grows with ambient O2 and falls with diluent heat capacity.

$$
d^2=d_0^2-Kt,\qquad K=\frac{8\lambda_g}{\rho_l c_{p,g}}\ln(1+B),\qquad B=\frac{Y_{O_2,\infty}\Delta h_c/\nu+c_p(T_\infty-T_s)}{h_{fg}}
$$

- `is_heptane` (1 n-heptane, 0 methanol; training range 0-1): expected **+**, heptane has the larger transfer number B.
- `x_o2_ambient` (mole fraction; training range 0.12-0.34): expected **+**, B grows with ambient O2.
- `x_co2` (mole fraction; training range 0-0.7): expected **-**, CO2's heat capacity lowers T_f and B.
- `x_he` (mole fraction; training range 0-0.45): expected **+**, helium raises the gas conductivity lambda.
- `pressure_kpa` (kPa, log10; training range 70.2-309): expected **?**, quasi-steady theory: K nearly independent of pressure.
- `d0_mm` (mm; training range 1.13-4.53): expected **-**, radiative loss grows with droplet and flame size; small methanol droplets burn faster than predicted.

**Training rows.**

- PSI-69 FLEX tests: 274
- excluded 16: no burning-rate constant
- excluded 1: no initial diameter or pressure (includes C11M201, pressure_zero_in_source)
- excluded 4: composition_sum: O2/N2/CO2/He fractions (features) sum to 0.98
- excluded 2: duplicate_id: the two 193F001 rows disagree on d0, K and burn time
- training rows: 251

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | r2 grouped | mae grouped | r2 ungrouped | mae ungrouped |
|---|---|---|---|---|
| **logistic / linear (this model)** | 0.686 ± 0.0934 (pooled 0.741) | 0.0453 ± 0.00228 (pooled 0.0453) | 0.766 ± 0.122 (pooled 0.759) | 0.043 ± 0.0126 (pooled 0.0431) |
| mean_predictor | -0.212 ± 0.234 (pooled -0.061) | 0.108 ± 0.0191 (pooled 0.108) | -0.0439 ± 0.0405 (pooled -0.0149) | 0.106 ± 0.014 (pooled 0.106) |
| single_best_feature_rule | -0.291 ± 0.37 (pooled -0.0752) | 0.11 ± 0.0146 (pooled 0.11) | 0.109 ± 0.0879 (pooled 0.134) | 0.0961 ± 0.0124 (pooled 0.0961) |
| decision_tree_depth3 | 0.227 ± 0.324 (pooled 0.386) | 0.0817 ± 0.00681 (pooled 0.0816) | 0.419 ± 0.216 (pooled 0.45) | 0.0688 ± 0.0112 (pooled 0.0689) |
| gradient_boosting | 0.53 ± 0.115 (pooled 0.61) | 0.0589 ± 0.00811 (pooled 0.0589) | 0.7 ± 0.122 (pooled 0.706) | 0.0489 ± 0.0119 (pooled 0.049) |

**How sure is the headline number?** Resampling the 79 test days and rerunning the grouped cross-validation 200 times puts the pooled r2 between 0.63 and 0.8 (95%, median 0.73). The single best feature alone reaches -0.29 (pooled -0.075).

**Prediction range.** `predict` adds the 5th and 95th percentile of the grouped out-of-fold residuals (-0.0892 and +0.09, target units) to the prediction. 90% is the target, not a measured coverage. Measured on held-out test days, with each day's range rebuilt from the other days only, the range held 225 of 251 tests (90%; 13 below it, 13 above): methanol 144 of 148 (97%), n-heptane 81 of 103 (79%). It is wider than needed for methanol (share above 90%). That is clearly below 90% for n-heptane (Wilson 95% interval of the share 0.7-0.85, tests counted as independent): the range is too narrow for n-heptane, and about 2 in 10 such tests fall outside it. The target cannot be below 0, so `predict` cuts the range there and says so (`interval_clipped`): 0 of the 251 held-out ranges were cut. When even the upper end is below 0, `predict` returns no range (`interval` null, `interval_clipped` false, the reason in `interval_unavailable`).

Coefficients on the burn_rate_k_mm2_s scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: 0.0842.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `is_heptane` | 0.0122 | [0.00205, 0.0243] | 0.0249 | [0.00417, 0.0495] | + | agrees |
| `x_o2_ambient` | 0.0962 | [0.0858, 0.108] | 2.04 | [1.82, 2.29] | + | agrees |
| `x_co2` | -0.0204 | [-0.0329, -0.00837] | -0.125 | [-0.202, -0.0514] | - | agrees |
| `x_he` | 0.0619 | [0.0512, 0.0748] | 0.538 | [0.446, 0.651] | + | agrees |
| `log10(pressure_kpa)` | 0.00927 | [0.000602, 0.0227] | 0.0906 | [0.00588, 0.222] | ? | no prior expectation |
| `d0_mm` | -0.0436 | [-0.0533, -0.0336] | -0.0646 | [-0.0791, -0.0499] | - | agrees |

**Sensitivity.** Refitted without the tests that went out early (D_ext/D0 > 0.9), where K is fitted over a short burn (35 rows left out, n = 216; grouped r2 0.736, pooled 0.758). Coefficients per unit:

| feature | all rows | without them |
|---|---|---|
| `is_heptane` | 0.0249 | 0.057 |
| `x_o2_ambient` | 2.04 | 1.78 |
| `x_co2` | -0.125 | -0.0594 |
| `x_he` | 0.538 | 0.525 |
| `log10(pressure_kpa)` | 0.0906 | 0.0217 |
| `d0_mm` | -0.0646 | -0.0523 |

**Does it match the physics?** Yes, every term with an expectation agrees and its interval excludes 0: K rises with O2 and helium (conductivity), falls with CO2 and with initial diameter (radiative loss), and is slightly higher for heptane. Pressure has a small positive coefficient that is not robust: it shrinks about fourfold when the tests that went out early are left out (see Sensitivity), so K is best read as independent of pressure here, as quasi-steady theory says. The linear model beats gradient boosting on held-out days (R² 0.69 vs 0.53), so there is no evidence of missed non-linearity.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- x_o2_ambient <= 0.235
|   |--- value: [0.474]
|--- x_o2_ambient >  0.235
|   |--- value: [0.630]
```

**Caveats.**

- The rows include tests that went out early (D_ext/D0 > 0.9). They are kept, because leaving them out would select on the outcome, but the pressure coefficient depends on them (see Sensitivity).
- K is one average per test; the tabulated value is not accompanied by the diameter history it came from.
- Needle conformal-coating contamination (2009-2011) is judged by the team to affect K minimally.
- Diluent fractions vary jointly (O2/N2/CO2/He sum to 1), so coefficients are partial effects at fixed remaining fractions; N2 is the implicit reference.

**Must not be used for.**

- other fuels, fibre-supported droplets or sprays
- predicting whether a droplet ignites (no failed-ignition rows exist)
- burn time (needs the extinction diameter, which this model does not predict)

## `flex_methanol_extinction_diameter` (PSI-69, regressor)

**Question.** At what droplet diameter does a burning methanol droplet go out?

**Target.** `ext_diameter_mm`: visible-flame extinction diameter (mm), tests that ended in flame extinction. n = 100 tests on 37 test days; range 0.81-3.96, mean 1.88.

**Physics expectation.** Methanol droplets in FLEX mostly went out diffusively: the flame's residence time shrinks with the droplet until the Damköhler number falls below critical, and absorbed water (which dilutes the fuel vapour) makes that happen at a larger diameter. Below about 14% O2, radiative extinction takes over.

$$
\mathrm{Da}=\frac{\tau_{res}}{\tau_{chem}},\qquad \tau_{res}\sim\frac{d_f^{2}}{\alpha},\qquad \mathrm{Da}<\mathrm{Da}_{crit}\Rightarrow\text{extinction}
$$

- `d0_mm` (mm; training range 1.61-4.35): expected **+**, absorbed product water accumulates to ~30% of the droplet mass, so D_ext grows roughly linearly with D0.
- `x_o2_ambient` (mole fraction; training range 0.12-0.3): expected **-**, diffusive (Damköhler) extinction diameter grows as O2 falls.
- `x_co2` (mole fraction; training range 0-0.7): expected **?**, the team reports D_ext nearly independent of diluent type.
- `x_he` (mole fraction; training range 0-0.45): expected **?**, as for CO2.
- `pressure_kpa` (kPa, log10; training range 70.2-276): expected **?**, no clear expectation over 0.7-3 atm.

**Training rows.**

- PSI-69 FLEX tests: 274
- excluded 117: not methanol (heptane mixes radiative and diffusive branches)
- excluded 31: test ended by disruption or completion, not extinction
- excluded 24: no extinction diameter, initial diameter or pressure
- excluded 2: composition_sum: ambient fractions (features) sum to 0.98
- training rows: 100

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | r2 grouped | mae grouped | r2 ungrouped | mae ungrouped |
|---|---|---|---|---|
| **logistic / linear (this model)** | 0.697 ± 0.113 (pooled 0.707) | 0.349 ± 0.0574 (pooled 0.349) | 0.705 ± 0.102 (pooled 0.716) | 0.333 ± 0.0485 (pooled 0.333) |
| mean_predictor | -0.0179 ± 0.0254 (pooled -0.0057) | 0.65 ± 0.038 (pooled 0.65) | -0.0407 ± 0.0422 (pooled -0.0135) | 0.65 ± 0.0491 (pooled 0.65) |
| single_best_feature_rule | 0.353 ± 0.181 (pooled 0.358) | 0.523 ± 0.0946 (pooled 0.523) | 0.191 ± 0.268 (pooled 0.212) | 0.562 ± 0.103 (pooled 0.562) |
| decision_tree_depth3 | 0.526 ± 0.263 (pooled 0.529) | 0.41 ± 0.0949 (pooled 0.41) | 0.48 ± 0.221 (pooled 0.508) | 0.428 ± 0.0743 (pooled 0.428) |
| gradient_boosting | 0.735 ± 0.145 (pooled 0.737) | 0.307 ± 0.088 (pooled 0.307) | 0.805 ± 0.0607 (pooled 0.813) | 0.273 ± 0.0589 (pooled 0.273) |

**How sure is the headline number?** Resampling the 37 test days and rerunning the grouped cross-validation 200 times puts the pooled r2 between 0.13 and 0.76 (95%, median 0.63). The single best feature alone reaches 0.35 (pooled 0.36).

**Prediction range.** `predict` adds the 5th and 95th percentile of the grouped out-of-fold residuals (-0.644 and +0.731, target units) to the prediction. 90% is the target, not a measured coverage. Measured on held-out test days, with each day's range rebuilt from the other days only, the range held 87 of 100 tests (87%; 6 below it, 7 above). The target cannot be below 0, so `predict` cuts the range there and says so (`interval_clipped`): 5 of the 100 held-out ranges were cut. When even the upper end is below 0, `predict` returns no range (`interval` null, `interval_clipped` false, the reason in `interval_unavailable`).

Coefficients on the ext_diameter_mm scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: 1.68.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `d0_mm` | 0.532 | [0.418, 0.658] | 0.824 | [0.648, 1.02] | + | agrees |
| `x_o2_ambient` | -0.361 | [-0.49, -0.224] | -9.99 | [-13.6, -6.19] | - | agrees |
| `x_co2` | 0.245 | [0.0961, 0.347] | 1.41 | [0.552, 1.99] | ? | no prior expectation |
| `x_he` | 0.193 | [0.0897, 0.318] | 1.47 | [0.679, 2.41] | ? | no prior expectation |
| `log10(pressure_kpa)` | -0.0338 | [-0.178, 0.113] | -0.382 | [-2.01, 1.27] | ? | no prior expectation |

**Does it match the physics?** Yes. D_ext grows with D0 (0.82 mm per mm, close to the linear water-absorption scaling) and with lower O2. CO2 and helium both enlarge D_ext; that is consistent with the Damköhler picture (CO2 lowers T_f and slows chemistry; helium's higher diffusivity shortens the residence time d_f²/α), though the team describes D_ext as nearly independent of diluent. Gradient boosting is only slightly better (R² 0.74 vs 0.70).

Single-best-feature rule (depth-1 tree on all rows):

```
|--- d0_mm <= 3.390
|   |--- value: [1.575]
|--- d0_mm >  3.390
|   |--- value: [2.709]
```

**Caveats.**

- Rows mix diffusive and (below ~14% O2) radiative extinctions; the table does not label which.
- Some extinction diameters were extrapolated when the droplet drifted out of view.
- Disrupted droplets (often from needle-coating contamination) are excluded, which selects cleaner tests.

**Must not be used for.**

- n-heptane or other fuels
- an oxygen index (LOI) estimate: no failed-ignition rows exist

## `cfi_reignition` (PSI-39, classifier)

**Question.** At 2-5 atm, does an n-dodecane (or n-/iso-dodecane blend) droplet re-ignite a hot flame from its cool flame after the first radiative extinction?

**Target.** `reignited`: 1 if n_reignitions > 0 (spreadsheet DATA sheet), else 0. n = 62 tests on 18 test days; 36 positive / 26 negative.

**Physics expectation.** After radiative extinction of the hot flame, n-alkane droplets keep burning as a cool flame (low-temperature, NTC chemistry). At higher pressure the cool flame releases more heat and accumulates reactive vapour, and can run away back into a hot flame.

$$
\mathrm{Da}_{cool}=\frac{\tau_{res}}{\tau_{LTC}},\qquad \tau_{res}\sim\frac{d_f^{2}}{\alpha},\qquad \tau_{LTC}^{-1}\ \text{rises with }p
$$

- `pressure_kpa` (kPa, log10; training range 203-507): expected **+**, low-temperature chemistry and heat release rise with pressure.
- `d0_mm` (mm; training range 3.87-6.43): expected **+**, a larger droplet leaves more fuel and a longer cool-flame phase.
- `iso_dodecane_fraction` (mole fraction of iso-dodecane in the fuel; training range 0-0.4): expected **-**, branched iso-dodecane suppresses low-temperature chemistry.
- `x_he` (mole fraction; training range 0-0.59): expected **?**, helium shortens hot flames but the team reports it helps the heat-release/heat-loss balance in the NTC region.
- `x_o2_ambient` (mole fraction; training range 0.17-0.21): expected **+**, more O2, more vigorous cool-flame chemistry.

**Training rows.**

- PSI-39 CFI tests: 227
- excluded 76: not analysed in the data-summary spreadsheet (all farnesane, untested points)
- excluded 3: no initial diameter
- excluded 3: composition_sum: O2 + N2 = 0.97 (FLEX-1219 to 1222)
- excluded 83: below 2 atm: 0 re-ignitions in every analysed test (see the descriptive table); a logistic fit across that wall is pure separation
- training rows: 62

**Use: descriptive only.** `predict` returns no prediction for this model, only the nearest real tests. The cross-validation below is shown to justify that choice.

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | roc_auc grouped | brier grouped | balanced_accuracy grouped | roc_auc ungrouped | brier ungrouped | balanced_accuracy ungrouped |
|---|---|---|---|---|---|---|
| **logistic / linear (this model)** | 0.51 ± 0.355 (pooled 0.5) | 0.305 ± 0.12 (pooled 0.302) | 0.505 ± 0.258 (pooled 0.526) | 0.703 ± 0.177 (pooled 0.643) | 0.233 ± 0.0645 (pooled 0.232) | 0.641 ± 0.101 (pooled 0.639) |
| majority_class | 0.5 ± 0 (pooled 0.347) | 0.254 ± 0.0193 (pooled 0.254) | 0.5 ± 0 (pooled 0.5) | 0.5 ± 0 (pooled 0.474) | 0.244 ± 0.00463 (pooled 0.244) | 0.5 ± 0 (pooled 0.5) |
| single_best_feature_rule | 0.294 ± 0.167 (pooled 0.289) | 0.38 ± 0.0857 (pooled 0.381) | 0.294 ± 0.167 (pooled 0.28) | 0.543 ± 0.135 (pooled 0.498) | 0.269 ± 0.0699 (pooled 0.27) | 0.543 ± 0.135 (pooled 0.541) |
| decision_tree_depth3 | 0.285 ± 0.297 (pooled 0.402) | 0.38 ± 0.18 (pooled 0.376) | 0.409 ± 0.143 (pooled 0.433) | 0.462 ± 0.151 (pooled 0.486) | 0.318 ± 0.0844 (pooled 0.318) | 0.456 ± 0.139 (pooled 0.449) |
| gradient_boosting | 0.392 ± 0.303 (pooled 0.409) | 0.414 ± 0.145 (pooled 0.411) | 0.388 ± 0.178 (pooled 0.388) | 0.552 ± 0.118 (pooled 0.578) | 0.298 ± 0.062 (pooled 0.297) | 0.6 ± 0.101 (pooled 0.597) |

**How sure is the headline number?** Resampling the 18 test days and rerunning the grouped cross-validation 200 times puts the pooled roc_auc between 0.12 and 0.83 (95%, median 0.46). The single best feature alone reaches 0.29 (pooled 0.29). Brier score of the probabilities on held-out days (pooled, lower is better): 0.302, against 0.254 for always giving the training days' base rate.

Coefficients on the log-odds scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: -12.2.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `log10(pressure_kpa)` | 0.845 | [0.142, 2.32] | 6.27 | [1.06, 17.2] | + | agrees |
| `d0_mm` | -0.323 | [-1.25, 0.523] | -0.575 | [-2.22, 0.931] | + | opposite sign; CI includes 0 |
| `iso_dodecane_fraction` | -0.311 | [-1.29, 0.762] | -1.75 | [-7.26, 4.29] | - | agrees in sign; CI includes 0 |
| `x_he` | -0.441 | [-1.6, 1.04] | -2.04 | [-7.44, 4.85] | ? | no prior expectation |
| `x_o2_ambient` | 0.00893 | [-0.977, 0.561] | 0.565 | [-61.8, 35.5] | + | agrees in sign; CI includes 0 |

**Does it match the physics?** Pressure agrees (+) and is the only effect: none of 86 analysed tests at or below 1.25 atm re-ignited, against 36 of 62 at 2-5 atm. Within 2-5 atm nothing else is resolvable; d0 has the opposite sign to expectation but its interval spans 0 widely.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- log10(pressure_kpa) <= 2.594
|   |--- class: 0
|--- log10(pressure_kpa) >  2.594
|   |--- class: 1
```

Observed fractions with Wilson 95% intervals:

| pressure_level_kpa | positives / n | fraction | Wilson 95% |
|---|---|---|---|
| 51 | 0 / 10 | 0 | [0, 0.28] |
| 76 | 0 / 12 | 0 | [0, 0.24] |
| 101 | 0 / 52 | 0 | [0, 0.069] |
| 127 | 0 / 12 | 0 | [0, 0.24] |
| 203 | 5 / 12 | 0.42 | [0.19, 0.68] |
| 304 | 17 / 34 | 0.5 | [0.34, 0.66] |
| 507 | 14 / 16 | 0.88 | [0.64, 0.96] |

**Caveats.**

- Below 2 atm no analysed test re-ignited (0/86): that wall is reported as a descriptive table, and the logistic model only covers 2-5 atm.
- The type-B thermocouple catalytic re-ignition seen in CFI-G (PSI-159) is a different hardware effect; CFI uses no such probe near the droplet.
- Farnesane tests are not analysed in the spreadsheet and are absent.
- Within 2-5 atm the logistic fit has no skill on held-out days (pressure levels were flown on separate days, and d0, blend and helium add nothing measurable), so only the pressure table is a result.

**Must not be used for.**

- pressures below 2 atm via this model (use the table)
- fuels other than n-dodecane blends

## `spice_smoke_point_length` (PSI-107, regressor)

**Question.** How long is a microgravity co-flow jet flame at its smoke point, for a given nozzle and co-flow speed?

**Target.** `flame_length_mm`: luminous flame length (mm, video) of run-log rows marked as at the smoke point. n = 23 tests on 6 test days; range 8.79-91.7, mean 29.6.

**Physics expectation.** A jet flame emits smoke when its tip is cooled (by soot radiation) below the temperature at which soot oxidation stops; the luminous length at that point is the smoke point. Co-flow shortens residence time, so more fuel (a longer flame) is needed before soot escapes.

$$
L_{SP}\propto d^{-0.91}\,u_a^{0.41}\quad\text{(SPICE final report, all fuels)},\qquad L_f=C\,\frac{\dot m_f}{Z_{st}}
$$

- `nozzle_mm` (mm, log10; training range 0.406-1.6): expected **-**, published fit L_SP ~ d^-0.91.
- `flow_cm_s` (cm/s, log10; training range 9.12-57.1): expected **+**, published fit L_SP ~ u_a^0.41: co-flow shortens residence time.

**Training rows.**

- PSI-107 SPICE run-log rows: 526
- excluded 495: not marked as at the smoke point
- excluded 8: no flame length or co-flow
- training rows: 23

**Use: descriptive only.** `predict` returns no prediction for this model, only the nearest real tests. The cross-validation below is shown to justify that choice.

**Result.** Cross-validated metrics, mean ± SD across folds (pooled out-of-fold value in brackets). *Grouped* holds out whole test days; *ungrouped* shuffles tests, so the gap between the two is the optimism from same-day tests sharing conditions.

| model | r2 grouped | mae grouped | r2 ungrouped | mae ungrouped |
|---|---|---|---|---|
| **logistic / linear (this model)** | -45.2 ± 61.7 (pooled -1.79) | 0.369 ± 0.173 (pooled 0.407) | -0.179 ± 0.154 (pooled -0.0575) | 0.251 ± 0.103 (pooled 0.246) |
| mean_predictor | -49.6 ± 77.2 (pooled -0.515) | 0.316 ± 0.153 (pooled 0.306) | -0.105 ± 0.111 (pooled -0.0244) | 0.257 ± 0.0939 (pooled 0.253) |
| single_best_feature_rule | -77 ± 132 (pooled -1.55) | 0.348 ± 0.186 (pooled 0.379) | -0.282 ± 0.754 (pooled -0.0862) | 0.257 ± 0.112 (pooled 0.258) |
| decision_tree_depth3 | -134 ± 246 (pooled -1.11) | 0.391 ± 0.203 (pooled 0.359) | -0.383 ± 0.977 (pooled -0.183) | 0.264 ± 0.123 (pooled 0.263) |
| gradient_boosting | -169 ± 310 (pooled -2.04) | 0.462 ± 0.197 (pooled 0.451) | -1.6 ± 1.1 (pooled -1.31) | 0.399 ± 0.15 (pooled 0.401) |

**How sure is the headline number?** Resampling the 6 test days and rerunning the grouped cross-validation 200 times puts the pooled r2 between -4.6 and 0.2 (95%, median -1.7). The single best feature alone reaches -77 (pooled -1.6).

**Prediction range.** `predict` adds the 5th and 95th percentile of the grouped out-of-fold residuals (-0.925 and +0.617, log10 of the target) to the prediction. 90% is the target, not a measured coverage. Measured on held-out test days, with each day's range rebuilt from the other days only, the range held 15 of 23 tests (65%; 5 below it, 3 above). That is clearly below 90% (Wilson 95% interval of the share 0.45-0.81, tests counted as independent): the range is too narrow, and about 3 in 10 such tests fall outside it.

Errors (MAE, residuals) of this model are in log10 of the target: an MAE of 0.37 is a factor of 2.3.

Coefficients on the log10(flame_length_mm) scale (per SD of the feature, and per unit of the feature as transformed). Intercept per unit: 1.03.

| feature | per SD | 95% CI (cluster bootstrap by date) | per unit | 95% CI per unit | expected | verdict |
|---|---|---|---|---|---|---|
| `log10(nozzle_mm)` | -0.00934 | [-0.328, 0.155] | -0.0431 | [-1.51, 0.716] | - | agrees in sign; CI includes 0 |
| `log10(flow_cm_s)` | 0.0668 | [-0.0208, 0.236] | 0.25 | [-0.0781, 0.886] | + | agrees in sign; CI includes 0 |

**Does it match the physics?** Only in sign. The fitted exponents (nozzle -0.04, co-flow +0.25, both intervals spanning 0) are far from the published L_SP ~ d^-0.91 u_a^0.41, and no fit beats the mean on held-out days. With fuels pooled and 23 rows, the fuel-specific smoke point dominates the scatter. The run-log smoke-point rows do not reproduce the published correlation; the 55-point smoke-point review sheet would be needed.

Single-best-feature rule (depth-1 tree on all rows):

```
|--- log10(flow_cm_s) <= 1.140
|   |--- value: [1.158]
|--- log10(flow_cm_s) >  1.140
|   |--- value: [1.441]
```

**Caveats.**

- Only 23 smoke-point rows with a length in the run log against 52-55 smoke points in the reports; the smoke-point review sheet could not be matched row by row.
- Fuels (ethylene, propane, 50/75/100% propylene) are pooled because 23 rows cannot support a fuel term; the smoke point is fuel-specific, so the scatter is large.
- Outlet-screen clogging changed the true co-flow for a given anemometer reading between days.

**Must not be used for.**

- any prediction: this is a descriptive fit
- 1 g flames or unconfined burners

## Candidates dropped

- `flex_extinction_mode` (PSI-69): The end mode (extinction / disruption / completion) is confounded with needle-coating contamination, which the team blames for disruptions: 46 of 165 tests disrupted in 2009-2010 against 15 of 109 in 2011. Radiative vs diffusive extinction is not labelled in the table; deriving it from D_ext/D0 would put the outcome into the label definition with an arbitrary threshold.
- `flex_ignition` (PSI-69): No failed-ignition rows: 'will it burn' (and an LOI) cannot be estimated.
- `flex_heptane_extinction_diameter` (PSI-69): Heptane extinctions mix an early radiative branch (D_ext/D0 > 0.9 in 24 of 56) and a diffusive branch, unlabelled; a single linear model across both is not physically meaningful.
- `cfi_cool_flame_occurrence` (PSI-39): cool_flame is True-or-null. Null rows are not negatives: among analysed tests with cool_flame null, comments describe cool-flame burning (FLEX-1214, 1216, 1229), droplets leaving the field of view, or no ignition (FLEX-1212).
- `cfi_hot_burning_rate` (PSI-39): 60 of 148 hot-flame K values come from flames that went out with D_ext/D0 > 0.95, where K is fitted over a tiny part of the burn (values down to 0.001 mm²/s). Filtering those out selects on the outcome; keeping them makes K mostly measurement noise.
- `spice_at_smoke_point_classifier` (PSI-107): Only 31 rows are marked True and 66 False (429 null). 'False' lumps flames below the smoke point with flames already past it, so the label is not monotone in flame length and a classifier on length, fuel, nozzle and flow has no physical threshold to learn; 21 of the 66 are Nikon still rows duplicating a video row.
- `psi20_bre` (PSI-20): 18 test-day rows (several flames each) with no outcome column at all: nothing to model per test.
