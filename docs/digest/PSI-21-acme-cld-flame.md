# PSI-21: ACME CLD Flame (Advanced Combustion via Microgravity Experiments - Coflow Laminar Diffusion Flame)

Small methane and ethylene flames surrounded by a gentle co-flowing air stream were burned on the Space Station, from very diluted near-extinction flames to very sooty ones, to give computer models clean, buoyancy-free benchmark data; the sooty flames held several times more soot than on Earth and diluted flames survived at lower fuel concentrations.

Investigators: Marshall B. Long (Yale University) - Principal Investigator; Mitchell D. Smooke (Yale University) - Co-Investigator; Dennis P. Stocker (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS) |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 2006-10-01 to 2022-05-31 |
| Fuels and samples | methane; ethylene |
| Varied | fuel: methane (16 days, 157 flames), ethylene (16 days, 187 flames)<br>fuel mole fraction in N2 (commanded range per day): CH4 0.20-1.00; C2H4 0.10-1.00 (one 2021 day lists 0-0.30) mole (volume) fraction<br>fuel and coflow velocity (typically matched): not in PSI; MFC full scales imply a mean fuel-tube velocity upper bound of roughly 60-190 cm/s at standard conditions (derived, 2.1 mm tube) cm/s |
| Number of tests | 344 |
| Fire-safety pillars | fundamental |

## Question

Can detailed computational models with chemical-kinetic and soot sub-models predict laminar diffusion flames at the extremes of fuel dilution: heavily sooting pure-fuel flames and very dilute flames near extinction? Earlier work, including microgravity work, showed the models fall short there. Buoyancy complicates 1 g flames (it accelerates and narrows them, shortens residence time and causes flicker), so the ISS was used to obtain momentum-dominated, buoyancy-free coflow flames with long residence times as clean benchmark cases. Objective A: characterise weak coflow methane and ethylene flames versus velocity and dilution (flame shape, lift-off height, temperature, extinction limits). Objective B: characterise sooting tendency of long-residence-time flames versus velocity and dilution (shape, gas temperature in soot-free regions, soot luminosity, soot temperature, soot volume fraction). The stated hypothesis is to supply benchmark data to validate the investigators' computational models. Motivation is terrestrial combustion (efficiency, pollutants, design tools); NASA states the work does not serve space applications.

## Summary

CLD Flame produced benchmark data on laminar coflow diffusion flames, a fuel jet surrounded by co-flowing air, for testing chemical-kinetic and soot models at both extremes of fuel dilution. On the ISS, in the ACME insert of the Combustion Integrated Rack, a small coflow burner (about 2 mm fuel tube in a 25 mm air nozzle) burned nitrogen-diluted methane (20-100%) and ethylene (10-100%) in air on 32 test days from November 2017 to March 2021, igniting 344 flames. Cameras and pyrometry gave flame shape, lift-off height, CH* chemiluminescence, temperature, soot temperature and soot volume fraction. Preliminary results: sooty microgravity flames were taller and wider and held 5-8 times more soot than equivalent 1 g flames, and dilution limits of both fuels were extended, with lifted flames stable at lower fuel concentrations. Simulations of the ACME ethylene flames showed weaker gravity effects than in a larger burner, and highlighted errors in the predicted temperature field. For fire safety this is fundamental: microgravity flames can be sootier, more radiative and burn closer to dilution limits.

## Physics

In a coflow laminar diffusion flame, fuel (here methane or ethylene, often diluted with nitrogen) issues from a central tube into a surrounding stream of air; fuel and oxygen meet by diffusion and burn in a thin sheet roughly where they meet in stoichiometric proportion. On Earth the hot, light products are accelerated upward by buoyancy, which stretches and narrows the flame, pulls in air radially and shortens the time gas spends in the hot sooting region; the flame also flickers. In microgravity the flow is set only by the injection momentum, so flames are longer, wider and more diffuse, residence times are longer, and temperatures are lower. Longer residence time lets soot particles grow, so sooty flames carry several times more soot; more soot means more radiative loss, which cools the flame, which in turn changes soot chemistry - a strongly coupled problem that models struggle with. At the dilute extreme the flame is weak and lifts off the burner, stabilising where the local flow speed matches the propagation speed of its leading (triple-flame) edge; working with lifted flames removes heat loss to the burner rim from the problem. Without buoyancy-induced acceleration, dilute flames survive at lower fuel concentrations. Diluting the fuel with nitrogen lowers flame temperature and moves the stoichiometric surface, so dilution and velocity are the two knobs spanning weak to heavily sooting flames. Drop towers give only ~5 s, too short for soot to reach quasi-steady conditions, hence the need for ISS duration.

$$
L_f \propto \frac{\dot{m}_F}{\rho D \,\ln\!\left(1 + 1/S\right)}
$$

Burke-Schumann/Roper scaling for the length of a laminar jet diffusion flame. $L_f$ flame length (m); $\dot{m}_F$ mass flow rate of the fuel mixture (kg/s); $\rho D$ density times diffusivity of the gas (kg m-1 s-1, roughly temperature-independent); $S$ moles of oxidiser stream needed per mole of fuel stream (dilution changes $S$). Length depends on fuel mass flow, not separately on velocity or burner diameter, to leading order in both buoyant and non-buoyant flames; buoyancy and coflow change the prefactor and the flame width. Consistent with the SLICE finding that luminous flame length is proportional to fuel mass flow in both 1 g and microgravity, with microgravity flames longer.

Textbook background: Roper (1977) laminar jet flame length correlations
<https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *Buoyant and nonbuoyant luminous flame lengths are proportional to the mass flow rate of the fuel mixture; computed and measured nonbuoyant flames are noticeably longer than their 1g counterparts*

$$
Z_{st} = \left[1 + \frac{s\,Y_{F,1}}{Y_{O_2,2}}\right]^{-1}
$$

Stoichiometric mixture fraction, locating the flame sheet in mixture-fraction space. $Y_{F,1}$ fuel mass fraction in the fuel stream (lowered by N2 dilution); $Y_{O_2,2}$ = 0.233, oxygen mass fraction in air; $s$ stoichiometric oxygen-to-fuel mass ratio (4.0 for CH4, 3.43 for C2H4). Dilution raises $Z_{st}$ and lowers flame temperature and soot formation, which is how the fuel concentrations in the experimental table span sooty to near-extinction flames. Valid for a one-step, equal-diffusivity picture.

Textbook background: standard mixture-fraction definition

$$
Fr = \frac{U^2}{g\,d}, \qquad t_{res} \sim \frac{L_f}{U}\ \ (0g)\quad \text{vs}\quad t_{res} \sim \sqrt{\frac{2 L_f}{g}}\ \ (1g,\ \text{buoyancy-dominated})
$$

Froude number comparing jet momentum to buoyancy for exit velocity $U$ (m/s), tube diameter $d$ (m) and gravity $g$ (9.81 m/s2 on Earth); residence time $t_{res}$ (s) of gas in a flame of length $L_f$ (m). For the ACME burner ($d \approx 2$ mm, $U$ of order 10-100 cm/s) $Fr$ in 1 g is of order 0.5-50, so small slow flames are buoyancy-affected on Earth; in orbit ($g \approx 10^{-6} g_0$) they are momentum-dominated and gas lingers longer, giving more time for soot growth. Order-of-magnitude only.

Textbook background: standard dimensional analysis; values are illustrative

$$
\frac{S_1}{S_2} = \eta_{12}\left(\frac{\lambda_2}{\lambda_1}\right)^{5+\alpha}\exp\!\left[\frac{C_2}{T_s}\left(\frac{1}{\lambda_2}-\frac{1}{\lambda_1}\right)\right], \qquad f_v = -\frac{\lambda\,\ln(1-\varepsilon_\lambda)}{K_e\,L}
$$

Two-colour (colour-ratio) soot pyrometry used with the calibrated colour camera, in the Wien approximation: $S_1/S_2$ signal ratio of two colour channels at effective wavelengths $\lambda_1,\lambda_2$ (m); $\eta_{12}$ instrument calibration factor; $\alpha$ soot dispersion exponent (emissivity $\propto \lambda^{-\alpha}$; 0.9-1.38 assumed for microgravity soot in the SLICE analysis); $C_2$ = 0.014388 m K; $T_s$ soot temperature (K). Soot volume fraction $f_v$ (dimensionless, ppm) then follows from the absolute emission (calibrated against a thermocouple) via spectral emissivity $\varepsilon_\lambda$ over path length $L$ (m) with dimensionless extinction coefficient $K_e$. Assumes optically thin, line-of-sight data after Abel inversion; self-absorption in sooty flames biases temperature (corrections up to 22-75 K).

Textbook background: standard two-colour pyrometry
<https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *While the true soot dispersion exponent remains unknown in microgravity, a range from 0.9 to 1.38 is estimated based on literature values*
<https://doi.org/10.1364/OL.43.001103>: *with the maximum correction quantified to be 22 K for a flame with a maximum optical depth of 0.31. This correction is as much as 42 and 75 K for simulated flames with the same optical properties, structure, and a factor of two and five increase in soot volume fraction, respectively.*

## Method

### Apparatus

ACME chamber insert in the CIR combustion chamber (nominally 100 L, ~83 L free volume; constant-volume tests lasting a few minutes). Small coflow burner: two concentric tubes of 2.1 mm (fuel) and 25 mm (air) inner diameter; a 2023 modelling paper gives 2.2 mm inner diameter with 0.1 mm wall. The same burner was later used by E-FIELD Flames. Gas delivery by crew-exchangeable mass flow controllers (fuel, nitrogen diluent, coflow); per test day the fuel MFC full scale was 0.1 or 0.2 slpm and the N2 MFC 0.02-0.2 slpm (nitrogen basis). Diagnostics: a pre-characterised high-definition colour camera (flame shape, lift-off, CH* concentration, flame and soot temperature by pyrometry, soot volume fraction), a gray-scale camera with an opposed collimated light source for soot by light extinction, intensified cameras for OH* and CH*, PMTs for CH*/OH* chemiluminescence, radiometers, and translating 14 micron SiC fibres for thin-filament pyrometry (TFP) of gas temperature. Tests configured by crew and commanded from NASA Glenn.

### Fuels and samples

- methane (CH4), from 40% and 100% bottles, diluted on orbit with N2 to 20-100% (gas, coflow burner jet flame in air coflow)
- ethylene (C2H4), from 100%, 50% and 30% bottles, diluted on orbit with N2 to 10-100% (gas, coflow burner jet flame in air coflow)

### Procedure

Each test day the crew set up the burner, fuel bottle and mass flow controllers, and tests were run from the ground. Flames were ignited in an air-filled chamber with an air coflow, fuel and air velocities typically matched; fuel concentration (N2 dilution) and velocity were varied between tests and sometimes during a test, stepping toward lower fuel concentration until extinction for the dilute-limit work. Three ISS rounds: methane, 14 days (2017-11-15 to 2018-02-22, 130 flames); ethylene, 14 days (2018-05-25 to 2018-09-14, 162 flames); 'improved coflow tests', 4 days (2021-02-10 to 2021-03-03; 2 ethylene, 2 methane; 52 flames). Total 32 test days, 344 flames. Normal-gravity comparison flames were burned at Yale, and the investigators' MC-Smooth vorticity-velocity code with sectional soot model was used to compute both. The precursor SLICE experiment (Microgravity Science Glovebox, January-March 2012) used a different burner (76 mm square duct, 5 interchangeable nozzles) to refine the test matrix; most published ISS results in the PSI publication list come from SLICE, not from these ACME test days.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel | methane (16 days, 157 flames), ethylene (16 days, 187 flames) |  |
| fuel mole fraction in N2 (commanded range per day) | CH4 0.20-1.00; C2H4 0.10-1.00 (one 2021 day lists 0-0.30) | mole (volume) fraction |
| fuel and coflow velocity (typically matched) | not in PSI; MFC full scales imply a mean fuel-tube velocity upper bound of roughly 60-190 cm/s at standard conditions (derived, 2.1 mm tube) | cm/s |

Held constant:

- oxidiser: air coflow and air-filled chamber; chamber pressure not stated in sources reached (constant-volume chamber)
- burner: ACME small coflow burner (2.1-2.2 mm fuel tube, 25 mm air nozzle)
- diluent: nitrogen (fuel side only)

Number of tests: 344

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame shape, flame length/radius and lift-off height | high-definition colour camera | derived |
| CH* (and OH*) chemiluminescence; absolute CH* concentration | colour camera blue channel with absolute light calibration; PMTs; intensified cameras | derived |
| gas temperature in soot-free regions | thin-filament pyrometry (SiC fibres) | derived |
| soot temperature and soot volume fraction | colour-ratio pyrometry with absolute calibration; laser/collimated-light extinction | derived |
| extinction limits (lowest fuel concentration sustaining a flame) | video during stepwise dilution | derived |

## Findings

1. Sooty attached ethylene coflow flames in microgravity were taller and wider and contained about 5 to 8 times more soot than equivalent 1 g flames (preliminary ACME results, soot volume fraction compared across C2H4 concentrations). *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *Sooty microgravity flames are taller & wider and contain 5x to 8x more soot than equivalent 1G flames.*
   - <https://ntrs.nasa.gov/api/citations/20210021781/downloads/JASMAC%20ACME%20paper%2020210921.pdf>: *For sooty attached flames, preliminary results have revealed that the soot volume fraction can be several times greater in microgravity flames than in comparison normal-gravity flames.*
2. Microgravity extended the fuel-dilution limits of both methane and ethylene coflow flames: near the limit microgravity flames were more stable, and lifted flames were sustained at lower fuel concentrations than in 1 g. The PSI table shows commanded concentrations down to 20-25% CH4 and 10-15% C2H4 (one improved-coflow test day, 21041, lists 0%-30% C2H4; the table does not explain the 0%, so it is not read as a dilution limit), but these are commanded lower bounds, not measured limits (flames sometimes went out before reaching them). *(limit, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *Microgravity increases the limits of fuel dilution. Near limits, microgravity flames are more stable, allowing for lifted flames at lower fuel concentrations.*
   - <https://ntrs.nasa.gov/api/citations/20210021781/downloads/JASMAC%20ACME%20paper%2020210921.pdf>: *Meanwhile, dilution limits for both methane and ethylene flames were extended in microgravity, where the microgravity flames are more stable, allowing for lifted flames at lower fuel concentrations.*
   - `PSI-21_Experimental table_CLD Flame.csv` (all): *Fuel conc. - (as diluted with nitrogen on a volume basis) was varied between tests and sometimes during tests where the listing here accounts for both. However, it does not account for extinction that sometimes occurred before the flame fully reached the lowest concentration.*
   - `PSI-21_Experimental table_CLD Flame.csv`, sheet PSI-21_Experimental table_CLD Flame.csv, row 18241: *10%-20%*
   - `PSI-21_Experimental table_CLD Flame.csv`, sheet PSI-21_Experimental table_CLD Flame.csv, row 18003: *25%-40%*
   - `PSI-21_Experimental table_CLD Flame.csv`, sheet PSI-21_Experimental table_CLD Flame.csv, row 21041: *0%-30%*
3. In simulations of sooting ethylene-air coflow flames at 1 g and 0 g for the larger Yale burner and the ACME burner, 0 g flames are longer, broader, more diffuse and cooler, with more soot and longer residence time; for the smaller ACME flame these gravity effects are significantly diminished. *(result, medium)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *In this paper, we consider a combined experimental and computational study of sooting, ethylene-air, laminar, coflow diffusion flames under normal and microgravity conditions.*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *Two different burner configurations (Yale and ACME) are studied. Microgravity experiments are performed aboard the International Space Station.*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *at 0 g, the flame is lengthened, becomes broader and more diffuse, temperatures decrease and soot levels and gas residence times increase. However, in the case of the smaller ACME flame, these effects are significantly diminished.*
4. Model-data disagreement for the ISS flames was traced mainly to the thermal field: the model likely mispredicts temperature (radiation and re-absorption were examined), imposing measured temperatures should improve soot predictions, and heat transfer to the burner lip may alter the boundary conditions. A ground companion study on the Yale burner (40% C2H4) found that imposing the measured 2-D temperature moved the predicted soot peak from the wings to the centreline, matching experiment. *(method, medium)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *it is likely that the model inadequately predicts the thermal field and the use of experimental temperatures imposed onto the solution would provide more accurate simulations of the soot field and heat transfer to the burner lip could alter the boundary conditions of the flames*
   - <https://doi.org/10.1016/j.proci.2020.06.034>: *Results are presented for a 40% ethylene-air flame on the Yale Coflow Burner.*
   - <https://doi.org/10.1016/j.proci.2020.06.034>: *The distribution of soot in the constrained solution is much more consistent with experimental observations, and this fact illustrates how the validation of a soot sub-model may be complicated by the necessity of modeling distributed heat losses in the flame.*
5. SLICE precursor (ISS Microgravity Science Glovebox, 2012; pure CH4 coflow jet flames, 1.59 and 3.23 mm nozzles): peak soot volume fraction was about 4-8 times higher in microgravity than in 1 g (range set by the uncertain soot dispersion exponent, 0.9-1.38), peak soot temperature ~200 K lower, and peak soot moved from the centreline at 1 g to the wings in microgravity; the model reproduced flame shape and soot migration but underestimated soot volume fraction, especially in microgravity. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *From the experiments, the microgravity flames were found to be sootier than normal gravity flames by a factor of approximately 4 to 8 in terms of the peak soot volume fraction (based on the uncertainty of the soot dispersion exponent and temperature measurements).*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *The peak soot temperature in μ g is shown to be ~ 200 K lower than its 1 g counterpart.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *The distribution of peak soot was also found to shift from the centerline of the flame at 1 g to the wings at μ g.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *However, the soot volume fraction is underestimated, especially in microgravity.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *The current study focuses on 100% CH4/air laminar diffusion jet flames using 1.59 mm and 3.23 mm fuel nozzles.*
6. SLICE precursor (N2-diluted CH4, mole fraction 0.4-1.0, mean inlet velocity 23-90 cm/s): luminous flame length is proportional to fuel-mixture mass flow in both 1 g and microgravity, microgravity flames are noticeably longer, dilution has negligible effect on shape once normalised by methane flow, and buoyancy narrows 1 g flames through radially inward convection near the flame front. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *with CH4 mole fraction ranging from 0.4 to 1.0 and average inlet velocity ranging from 23 to 90 cm/s*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *Buoyant and nonbuoyant luminous flame lengths are proportional to the mass flow rate of the fuel mixture; computed and measured nonbuoyant flames are noticeably longer than their 1g counterparts*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *Buoyancy-induced reduction of the flame radius through radially inward convection near the flame front is demonstrated.*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *Buoyant and nonbuoyant flame structure is mainly controlled by the fuel mass flow rate, and the effects from fuel dilution and inlet velocity are secondary.*
7. SLICE precursor (soot-free N2-diluted CH4 flames): in microgravity the peak CH* concentration rises with coflow velocity but depends only weakly on fuel velocity; the integrated CH* emission scales with total heat release rate, but the 2-D CH* distribution is not a good marker of local heat release. *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20160012298/downloads/20160012298.pdf>: *Results show that, in microgravity, the maximum flame CH\* concentration increases with the coflow velocity, but it is weakly dependent on the fuel velocity*
   - <https://ntrs.nasa.gov/api/citations/20160012298/downloads/20160012298.pdf>: *the integrated CH\* emission scales proportionally to the computed total heat release rate; the two-dimensional CH\* spatial distribution, however, does not appear to be a good marker for the local heat release rate.*
8. Diagnostic accuracy (ground study): soot self-absorption biases colour-ratio soot pyrometry by up to 22 K for an N2-diluted ethylene flame with peak optical depth 0.31, and by 42 and 75 K for two and five times more soot, which matters for sootier microgravity flames. *(method, medium)*
   - <https://doi.org/10.1364/OL.43.001103>: *with the maximum correction quantified to be 22 K for a flame with a maximum optical depth of 0.31. This correction is as much as 42 and 75 K for simulated flames with the same optical properties, structure, and a factor of two and five increase in soot volume fraction, respectively.*
9. Campaign scope from the PSI table: 344 flames on 32 test days across three ISS rounds (methane Nov 2017-Feb 2018, 130 flames; ethylene May-Sept 2018, 162 flames; 'improved coflow tests' Feb-Mar 2021, 52 flames), with 2 to 18 flames per day. *(method, high)*
   - Table `tests`: counts and sums of n_flames by Test Type; min 2, max 18 per day
   - `PSI-21_Experimental table_CLD Flame.csv` (all): *Flames ignited is the number ignited on that test day.*
   - <https://www1.grc.nasa.gov/wp-content/uploads/ACME-publications-20230830.pdf>: *ISS operations: Nov. 2017–Feb. 2018, May-Sept. 2018, Feb.-March 2021*
10. SLICE precursor computations (N2-diluted CH4 coflow flames, X_CH4 0.4-1.0, 23-90 cm/s): removing buoyancy lowers the peak centreline temperature by about 300 K and moves it downstream, more so for higher fuel concentration or inlet velocity, and raises the centreline residence time about 3.5-fold near the exit of the computational domain. This is the mechanism behind the cooler, sootier microgravity flames. *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *when buoyancy is eliminated, the peak temperature along the centerline drops by around 300 K and moves downstream, with larger changes occurring in flames with higher fuel concentration or higher inlet velocity*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *this difference will result in a 3.5-fold increase in residence time*

## Fire-safety relevance

CLD Flame is not a fire-safety experiment (NASA: no space application intended). Its relevance is fundamental: (1) in still or slow flows microgravity flames can carry several times more soot and lose more heat by radiation than the same flames on Earth, which affects smoke production (detection) and radiative heating of nearby surfaces; (2) dilute flames survived to lower fuel concentrations in microgravity, so dilution or inerting margins derived from 1 g flames may be non-conservative for gaseous fuel leaks in orbit; (3) validated soot/radiation models are a prerequisite for predictive spacecraft fire simulation. Transferability caveats: small laminar gas-jet flames in air with nitrogen-diluted fuel; no solid or liquid fuels, no oxygen enrichment or reduced pressure; extinction data are fuel-dilution limits of a burner flame, not material flammability limits.

### Habitat conditions

All tests used air (about 21% O2) as oxidiser; chamber pressure is not stated in sources reached and is presumably near the Earth sea-level reference (101.3 kPa), but this is not documented. No enriched-oxygen or reduced-pressure cases such as the lunar habitat concept (>=30% O2 at <=70.3 kPa) were run; a ground companion study (1.0-2.7 atm, 101-274 kPa) examined only elevated pressure. Gravity: ISS microgravity only; no partial-gravity data.

### Earth benefits

Better kinetic and soot models for diffusion flames, the flame type of most practical combustors, should improve efficiency and reduce pollutant and soot emissions, and shorten the design time and cost of furnaces and engines; understanding extinction also informs fire suppression.

## Limitations

- Most peer-reviewed results attached to this investigation in PSI use SLICE (2012, Microgravity Science Glovebox, different burner and duct) or ground data, not the 2017-2021 ACME test days in the PSI table; ACME-specific results are preliminary (slides, conference paper) plus one modelling paper.
- No quantitative ACME extinction limits, soot volume fractions or temperatures were found in sources reached; the 5-8x soot ratio and extended dilution limits are summary statements.
- Small laminar gas-jet flames in air with N2-diluted fuel only; results are not material flammability data and do not cover enriched or reduced-pressure atmospheres.
- Soot diagnostics depend on assumed soot optical properties (dispersion exponent) and self-absorption corrections; the SLICE analysis showed the soot volume fraction could be overestimated by nearly a factor of 2 from this uncertainty.
- Constant-volume chamber and few-minute tests: chamber atmosphere is slowly vitiated and pressure rises during a test day.

## Data in PSI

PSI holds only a one-page experimental table (32 test days: test type, test day code, fuel and N2 MFC full-scale ranges, fuel bottle, fuel concentration range, flames ignited) and an ISA-Tab metadata zip that repeats the record text. No images, video, pyrometry, chemiluminescence or soot data, and no documents, are in PSI, so none of the findings below can be re-derived from PSI data. The table supports only a campaign overview (fuels, dilution ranges, flames per day). The record's totalFileSize (2,005,536,295,241 bytes, ~2.0 TB) is inconsistent with the two ~18 kB files listed.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | summary of 32 ISS test days | .csv | 1 | 2.5 kB | yes |
| metadata | ISA-Tab i_Investigation.txt and s_PSI-21.txt ('Do not use this' placeholder rows); zip name refers to PSI-97 | .zip .txt | 1 | 15 kB | yes |

Rows in the unified `tests` table: 32

## Related investigations

- [PSI-106](PSI-106-slice.md): precursor
- [PSI-22](PSI-22-acme-e-field-flames.md): shared hardware
- [PSI-107](PSI-107-spice.md): same fuel
- [PSI-10](PSI-10-acme-flame-design.md): shared hardware
- [PSI-20](PSI-20-acme-bre.md): shared hardware
- [PSI-23](PSI-23-acme-s-flame.md): shared hardware
- [PSI-159](PSI-159-acme-cfi-g.md): shared hardware

## Open questions

- PSI holds no flame images or derived fields; with them one could tabulate lift-off height and extinction fuel fraction versus matched velocity for both fuels and compare with SLICE and 1 g limits.
- What changed in the 2021 'improved coflow tests' (hardware or flow conditions) is not documented in sources reached.
- Quantitative ACME soot volume fraction and temperature maps (behind the 5-8x statement) have not been seen in a peer-reviewed paper other than the Dobbins et al. 2022 modelling study.
- Whether the extended dilution limits imply measurably lower limiting fuel concentrations for leak or inerting scenarios has not been assessed.

## Dashboard ideas

- **ISS test-day timeline** (`date`, `test_type`, `fuel`, `fuel_conc_range`, `fuel_mfc_slpm`, `n2_mfc_slpm`, `n_flames`): Only data PSI holds; shows the three rounds and the dilution ranges explored.
- **dilution range by fuel** (`fuel`, `fuel_conc_min`, `fuel_conc_max`): Shows how far toward extinction each fuel was pushed (commanded, not measured limits).
- **1 g vs microgravity soot comparison** (`fuel`, `gravity`, `peak_soot_ppm`, `peak_soot_T_K`): Headline result (4-8x soot, ~200 K cooler) from SLICE and ACME summaries; values must come from external sources.

## Gaps and data-quality notes

- No Science Documents, Reports, Presentations, Analyzed or Raw Data in PSI: only the experimental table CSV and a metadata zip. All results come from the PSI record text and external sources.
- Per-test fuel and coflow velocities, lift-off heights, extinction concentrations, temperatures and soot data are not in PSI; chamber pressure is not stated anywhere reached.
- Full texts of the Elsevier papers (Giassi 2016, Cao 2015, Ma 2015, Kempema 2021) were not read from the publisher (ScienceDirect blocks automated access); NASA NTRS preprints of Ma 2015 (20140017780), Cao 2015 (20150002322) and a Giassi CH* abstract/poster (20160012298) were used instead, and Crossref/OpenAlex/Semantic Scholar abstracts for Dobbins 2022, Cao 2018, Kempema 2018 and 2021. Dobbins 2022 (Taylor & Francis) full text was not reachable.
- The ACME CLD Flame conference papers cited by NASA for ISS results (Tinajero, Giassi, Stocker & Long, 11th US National Combustion Meeting 2019; Tinajero & Long, 12th USNCM 2021) were not found online.
- Most publications listed in the PSI record are SLICE-precursor or ground studies; one DOI (10.1016/j.proci.2014.05.138) is listed twice. The PSI record does not list SLICE (PSI-106) as related.
- Table data issues: the 'Fuel Bottle' column is a spreadsheet auto-fill artefact after the first row of each block ('40% CH5' ... '40% CH14', '100% C2H5' ... '100% C2H11', '50% C2H5' ... '50% C2H9', '30% C2H5', '40% CH5'); the bottles are presumably 40% CH4, 100% CH4, 100%/50%/30% C2H4. data/processed/tests.csv carries these labels in fuel_raw and leaves fuel_fraction mostly empty. 2018-02-22 (18053) lists a 100% CH4 bottle diluted to 30-40% with only a 0.02 slpm N2 MFC, which implies very low fuel flows - possible but worth checking. 2021-02-10 (21041) lists '0%-30%'.
- Brief said 32 test days; confirmed (32 rows, 344 flames). The evidence.parquet chunk for the table previews only rows 1-5; other rows were read from the CSV.
- Metadata zip is named 'PSI-21_metadata_PSI-97_ACME CLD Flame.zip' (refers to PSI-97); files.csv marks it not downloaded although a 16,071-byte file (listed size 15,476) is on disk. Record totalFileSize (~2.0 TB) does not match the files listed.
- Investigation dates in PSI (2006-10-01 to 2022-05-31) span grant periods, not ISS operations (Nov 2017 to March 2021).
- Coflow burner fuel-tube inner diameter: 2.1 mm in the 2014 NASA paper, 2.2 mm in the 2023 E-FIELD modelling preprint.
- No text addressed to an AI or unrelated instructions was found in the PSI files.
- Publication review (data/publications/PSI-21.json): of the 18 listed publications (17 distinct), 3 were read in full via NTRS preprints (Cao 2015 counted twice, Ma 2015), 6 as abstracts, 9 not at all (Elsevier/Springer closed, no free abstract). Only Dobbins 2022 uses ACME CLD Flame ISS data; the rest are SLICE precursor or ground diagnostics and modelling work. No listed paper reports the CLD Flame dilution limits or lift-off heights; NASA cites the 2019 and 2021 US National Combustion Meeting papers (Tinajero et al.) for these, which remain unlocated.
