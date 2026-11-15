# PSI-10: ACME/Flame Design (Advanced Combustion via Microgravity Experiments / Flame Design (proposal title: Flame Design: A Novel Approach to Clean Efficient Diffusion Flames))

On the space station, small ball-shaped flames of ethylene gas were burned for minutes around a porous sphere, either as fuel blowing into oxygen-rich air or as oxygen blowing into a fuel atmosphere, to learn when such flames make soot and when they go out.

Investigators: Richard L. Axelbaum (PI; Washington University in St. Louis); Peter B. Sunderland (Co-I; University of Maryland); David L. Urban (Co-I; NASA Glenn Research Center); Sergey M. Frolov (Investigator / lead Russian collaborator; Semenov Institute of Chemical Physics, Russian Academy of Sciences); Dennis P. Stocker (Project Scientist; NASA Glenn Research Center)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS); precursor tests in the NASA Glenn 2.2 s and 5.2 s drop towers |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 1999-01-14 to 2025-04-30 |
| Fuels and samples | Ethylene; O2/N2; Propane |
| Varied | ambient O2 mole fraction (normal flames): 0.198-0.399 (nominal 21%, 30%, 40%); propane day 0.40 mole fraction<br>burner O2 mole fraction (inverse flames): 0.21-0.85 (52 of 109 numeric rows at 0.85) mole fraction<br>burner fuel mole fraction (normal flames, N2 diluent): 0.05-1.0 mole fraction<br>ambient C2H4 mole fraction (inverse flames): 0.080-0.658 mole fraction<br>total burner mass flow rate: normal 0.31-21.5; inverse 1.76-13.8 mg/s<br>chamber pressure: normal 0.93-1.31 atm (94-133 kPa); inverse 0.43-3.02 atm (43-306 kPa), in steps near 0.43-0.52, 1.0, 2.0 and 3.0 atm kPa<br>stoichiometric mixture fraction Z_st: 0.061-0.758 -<br>adiabatic flame temperature T_ad (computed): 1683-2974 K<br>flame configuration: normal (fuel into oxidizer), inverse (oxidizer into fuel) |
| Number of tests | 327 |
| Fire-safety pillars | fundamental, prevention |

## Question

Flame Design asked how the internal structure of a non-premixed (diffusion) flame, set by the stoichiometric mixture fraction Z_st, controls soot inception and extinction, separately from the direction of convection across the flame. Moving nitrogen from the oxidizer to the fuel stream raises Z_st at fixed adiabatic flame temperature, and in normal-gravity work this produced 'permanently blue' flames that never soot, with much higher extinction strain. Buoyancy and strain make those results ambiguous, and spherical flames on Earth are impossible, so the team used microgravity spherical flames, normal (fuel out of the burner) and inverse (oxygen out of the burner), to measure sooting limits, extinction limits (radiative and kinetic) and their temperatures as functions of flow rate, Z_st, dilution and pressure. It also asked whether truly steady spherical diffusion flames can exist despite radiative loss, and whether a 'pseudo-flammability limit' exists for non-premixed flames. The stated hypotheses were that soot needs a region of high enough local C/O ratio and temperature at low strain, that spherical flames extinguish when peak temperature falls below 1130 K, and that steady spherical flames are possible.

## Summary

ACME/Flame Design burned ethylene spherical diffusion flames on a 6.35 mm porous sphere in the Combustion Integrated Rack on the ISS. In 2019, fuel (pure or nitrogen-diluted) flowed into oxygen/nitrogen atmospheres of 21-40% O2 near 1 atm (normal flames). In 2021-22, oxygen/nitrogen with up to 85% O2 flowed into ethylene/nitrogen atmospheres at 0.43-3 atm (inverse flames); one day used propane. The tables list 327 tests. Flows were held constant while cameras, thin-filament pyrometry, thermocouples and photomultipliers tracked each flame. In the 2019 tests flames grew, cooled by gas radiation, oscillated and went out after 28-336 s. At 1 atm all ethylene flames extinguished near 1130 K, at a fuel flux through the flame of 0.2 g/m2/s (normal) or an oxygen flux of 0.68 g/m2/s (inverse). Small flames burned steadily for up to 870 s. Sustained soot appeared only at 40% O2 with concentrated fuel. For fire safety, quiescent microgravity flames persist far below the about 1500 K extinction temperature typical on Earth, although these gas-burner limits are not material flammability limits.

## Physics

In a diffusion flame, fuel and oxidizer meet by diffusion at a thin reaction zone near the stoichiometric surface, Z = Z_st. For ethylene in air Z_st is about 0.064. Diluting the fuel and enriching the oxidizer (for example 1 mol C2H4 with 11.28 mol N2 burning in pure O2) gives the same adiabatic temperature but Z_st near 0.78. The flame then sits on the fuel side of the mixing layer, where hot gas contains free oxygen and little fuel, so soot precursors cannot grow. On Earth, a burner flame is dominated by buoyancy: the Richardson number for these flames is about 1000. Making it much less than 1 needs gravity reduced by about four orders of magnitude, and the team's analysis required about 10 micro-g. In microgravity the porous-sphere flame is one-dimensional. The radial velocity falls as 1/r^2, so at a few burner radii transport is purely diffusive, the diffusion time r^2/D reaches tens of seconds, and the hot zone keeps growing. As it grows, CO2 and H2O accumulate and radiate. Radiative loss scales with flame surface area, while the reactant flux per unit flame area falls, so the peak temperature drops until the flame undergoes radiative extinction. This occurs at a much lower temperature (about 1100-1130 K) than the kinetic (strain or blow-off) extinction familiar on Earth (about 1500 K). Near that limit, low-temperature 'warm flame' chemistry involving HO2 appears. Normal and inverse flames reverse the direction of convection relative to the flame. Soot formed in a normal flame is carried toward the oxidizer and burned; in an inverse flame it is carried toward the fuel and can grow.

$$
Z_{st} = \left(1 + \frac{Y_{F,\infty} W_O \nu_O}{Y_{O,\infty} W_F \nu_F}\right)^{-1}
$$

Stoichiometric mixture fraction. Y_{F,inf}, Y_{O,inf}: fuel and oxygen mass fractions in the fuel and oxidizer supply streams (-); W_F, W_O: molecular weights (kg/kmol); nu_F, nu_O: stoichiometric coefficients. Z_st is the mixture fraction (0 = pure oxidizer stream, 1 = pure fuel stream) at which the flame sits. Low Z_st (~0.06 for C2H4/air) puts the flame on the oxidizer side and favours soot. High Z_st (~0.7-0.8, diluted fuel into O2) gives soot-free 'permanently blue' flames. In the experimental tables, Z_st ranges over 0.06-0.76.

`PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p8): *Zst = (1+YF,∞WOνO / YO,∞WFνF)-1*
Table `tests`: mean Zst column of both experimental tables: normal 0.061-0.715, inverse 0.095-0.758

$$
Ri = \frac{g\,\Delta T\,L}{T\,u^2}
$$

Richardson number (buoyancy vs inertia). g: gravitational acceleration (m/s^2); Delta T = T_ad - T_b: flame-to-burner temperature difference (K); T: temperature (K); L: length scale, properly the flame diameter (m); u: gas velocity at the flame (m/s). The investigators estimate Ri ~ 1000 for these spherical flames at 1 g. Spherical symmetry needs Ri << 1, which for general fuels requires g reduced by about 10^4, so about 10 micro-g (CIR environment).

`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p6): *Ri = g (ΔT L) / (T u2)*
`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p6): *we find that Ri is on the order of 1000 in normal gravity.*
`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p7): *As shown, the required g levels are on the order of 10 μg.*

$$
\tau_d \sim \frac{r^2}{D}
$$

Diffusion time scale of the spherical flame. r: radial distance from burner centre (m); D: gas diffusivity (m^2/s). Because the convective velocity decays as 1/r^2, transport beyond a few burner radii is diffusive. tau_d is tens of seconds at a few cm, and the investigators found the time for an unbounded spherical flame to reach steady state is of order 10^5 s. This is why drop towers (2-5 s) cannot reach quasi-steady conditions.

`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p6): *Since the characteristic diffusion time τd is given by r2/D, τd is on the order of tens of seconds a few centimeters from the burner.*
`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *In the spherical, infinite domain configuration, the characteristic time for the diffusion- controlled system to effectively reach steady-state is found to be on the order of 100,000 s.*

$$
T_{ad}\,[\mathrm{K}] = 1198\,Z_{st} + 1838
$$

Sooting-limit correlation (drop-tower spherical flames). Fitted line through the sooting-limit flames from 2.2 s drop-tower tests (ethylene, 1.5 mg/s fuel consumption, normal and inverse flames; Sunderland et al. 2004). Flames with T_ad below the line at a given Z_st were soot-free at the end of the drop ('permanently blue' regime). It is valid only for these transient 2 s flames; the longest-residence-time flames (>0.5 s) were excluded from the fit.

`PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p15): *Tad(K) = 1198 Zst + 1838*
`PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p16): *The sooting limits follow a linear relationship between adiabatic flame temperature and Zst, with Zst accounting for a variation of about 700 K in the sooting limit ad iabatic flame temperature.*

$$
r_{f,ext} = \sqrt{\frac{\dot m_R}{4\pi\,\dot m''_{crit}}},\quad \dot m''_{crit} \approx 0.2\ \mathrm{g\,m^{-2}\,s^{-1}}\ (\text{normal, fuel}),\ 0.68\ \mathrm{g\,m^{-2}\,s^{-1}}\ (\text{inverse, } O_2)
$$

Flame radius at radiative extinction from the critical mass flux. dot m_R: mass flow of the burner reactant (fuel for normal flames, O2 for inverse flames) (g/s); dot m''_crit: reactant mass flux through the flame sphere at extinction (g/m^2/s); r_f,ext: radius of peak temperature at extinction (m). This is a mass-conservation reconstruction (steady flux through a sphere) of the 'simple equation' the investigators say estimates extinction flame size from reactant flow rate alone. The published form was not available. Valid for 1 atm ethylene flames whose peak temperature reaches 1130 K. For example, 1 mg/s of fuel gives r_f,ext of about 2 cm.

`PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *Despite this broad range of conditions, all flames extinguish at a critical extinction temperature of 1130 K, and a fuel-based mass flux of 0.2 g/m2 - s for normal flames, and an oxygen- based mass flux of 0.68 g/m2-s for inverse flames.*
Textbook background

## Method

### Apparatus

Tests ran in the Combustion Integrated Rack on the ISS using the ACME chamber insert. The chamber is a constant-volume vessel with about 83-90 L of free volume, so pressure and composition drift during a test day (vitiation). The burner was a 6.35 mm (0.25 in) porous sphere of sintered stainless steel (10 micron pores), fed by a single supply tube. Burner serial 1002 was replaced by 1003 in June 2019 because flames were off-centre at high flows. Three mass-flow controllers metered fuel or oxidizer and ISS nitrogen, allowing on-orbit dilution. A retractable hot-wire igniter lit the flame. Diagnostics were: the ACME colour DataCam (12-bit, 1360x1024, up to 30 frame/s, with filters for colour, BG7 pyrometry, CH* at 430 nm and formaldehyde); an analog ops camera; the CIR HiBMs monochrome camera with backlight, for soot extinction; an intensified CFI camera, generally with a CH* filter; three PMTs (OH* at 310 nm, CH* at 430 nm, and broadband); a thermopile radiometer array; a crew-replaceable array of 14 micron SiC fibres spaced 5 mm apart for thin-filament pyrometry (TFP); a burner-surface thermocouple; far (45, 60, 100, 100 mm) or near (13, 25, 50, 100 mm) thermocouple rakes, plus two thermocouples at 200 mm; and chamber pressure transducers. Non-imaging data were logged at 125 Hz. The CIR gas chromatograph was used occasionally.

### Fuels and samples

- Ethylene (C2H4), pure or diluted with N2 (burner X_fuel 0.05-1) flowing into O2/N2 (gas, normal spherical diffusion flame on 6.35 mm porous sphere)
- O2/N2 (burner X_O2 0.21-0.85) flowing into ethylene/N2 atmosphere (X_C2H4 0.08-0.66) (gas, inverse spherical diffusion flame on 6.35 mm porous sphere)
- Propane (C3H8), pure or diluted with N2 (X_fuel 0.10-1) into 40% O2 (gas, normal spherical flame, one test day (21301) used for thermocouple/TFP calibration)

### Procedure

The ISS crew configured the hardware, swapping gas bottles, MFCs, igniter tips, burners, rakes and fibre arrays. Tests were then commanded from the Glenn ISS Payload Operations Center. Each test ran from uplinked script and parameter files in a nominally automated mode, without manual flow changes during a test except halting after extinction. A typical sequence was: pre-ignition data and images, igniter preheat, flow priming, ignition with automatic detection (usually by the OH* PMT) and igniter retraction, then a stabilisation period. The flow was then held constant, or in some tests ramped, for up to a few minutes, with test end on detected extinction or flow timeout. A burner-temperature limit (for example 500 C) protected the sphere. About 16 tests were run per test day, with a couple of failed or unsustained ignitions. The chamber was vented and refilled between days, and recirculated through a sorbent filter mid-day in normal-flame testing. Round 1 (Apr-Jul 2019, Increments 59/60) used normal flames in roughly 21%, 30% and 40% O2. Round 2 (Oct 2021-Feb 2022, Increment 66) began with one propane normal-flame day using the near thermocouple rake to calibrate TFP. It then ran inverse flames with 85% O2 bottle gas diluted on orbit into 8-65% C2H4 atmospheres. From January 2022, after the chamber limit was raised from 1.5 to 3 atm, these included tests at about 0.5, 2 and 3 atm. The same constant-flow flames give soot-inception limits (yellow luminosity disappearing as the flame cools) and radiative-extinction limits (flame growth until extinction). Extinction diameter and burn time come from the ops video and the PMTs.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| ambient O2 mole fraction (normal flames) | 0.198-0.399 (nominal 21%, 30%, 40%); propane day 0.40 | mole fraction |
| burner O2 mole fraction (inverse flames) | 0.21-0.85 (52 of 109 numeric rows at 0.85) | mole fraction |
| burner fuel mole fraction (normal flames, N2 diluent) | 0.05-1.0 | mole fraction |
| ambient C2H4 mole fraction (inverse flames) | 0.080-0.658 | mole fraction |
| total burner mass flow rate | normal 0.31-21.5; inverse 1.76-13.8 | mg/s |
| chamber pressure | normal 0.93-1.31 atm (94-133 kPa); inverse 0.43-3.02 atm (43-306 kPa), in steps near 0.43-0.52, 1.0, 2.0 and 3.0 atm | kPa |
| stoichiometric mixture fraction Z_st | 0.061-0.758 | - |
| adiabatic flame temperature T_ad (computed) | 1683-2974 | K |
| flame configuration | normal (fuel into oxidizer), inverse (oxidizer into fuel) |  |

Held constant:

- burner: 6.35 mm porous stainless-steel sphere (serial 1002 to June 2019, then 1003)
- inert diluent: nitrogen only (CO2 dilution not flown)
- gravity: ISS microgravity, CIR without active PaRIS isolation
- burner flow within a test: nominally constant (some tests ramped)

Number of tests: 327

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame diameter vs time and diameter at extinction | analog ops video (recorded on ground) and colour DataCam | derived |
| burn time / extinction time | PMTs (OH* 310 nm, CH* 430 nm, broadband) | derived |
| gas temperature profile (fibre temperature) | thin-filament pyrometry, 14 micron SiC fibres imaged by colour DataCam (two-colour ratio and intensity methods) | derived |
| soot temperature | two-colour ratio pyrometry from DataCam images | derived |
| soot volume fraction (attempted) | HiBMs camera with backlight (light extinction) and DataCam | derived |
| burner surface temperature and far-field gas temperature | type B/K thermocouples on rake, at 200 mm and on burner | direct |
| flame radiant emission | thermopile radiometers (standard array saturated in round 1; CFI-G dual-gain array in round 2) | direct |
| chemiluminescence images (CH*, OH*) | intensified CFI camera | direct |
| chamber pressure, MFC flows | pressure transducers, mass-flow controllers (125 Hz telemetry) | direct |

## Findings

1. At about 1 atm, every ethylene spherical flame that extinguished radiatively did so at a peak temperature of about 1130 K. The reactant mass flux through the flame sphere at extinction was about 0.2 g/m^2/s of fuel for normal flames and 0.68 g/m^2/s of oxygen for inverse flames. This held across normal flames with ambient X_O2 0.20-0.38, burner X_fuel 0.13-1, total flow 0.6-12.2 mg/s and T_ad 2000-2800 K, and inverse flames with ambient X_C2H4 0.08-0.12, burner X_O2 0.40-0.85, 2.3-11.3 mg/s and T_ad 2080-2590 K. *(limit, high)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *Despite this broad range of conditions, all flames extinguish at a critical extinction temperature of 1130 K, and a fuel-based mass flux of 0.2 g/m2 - s for normal flames, and an oxygen- based mass flux of 0.68 g/m2-s for inverse flames.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *For normal flames, the ambient oxygen mole fraction was varied from 0.2 to 0.38, burner supply fuel mole fraction from 0.13 to 1, total mass flow rate, mtotal , from 0.6 to 12.2 mg/s, and adiabatic flame temperature, Tad , from 2000 to 2800 K.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *For inverse flames, the ambient fuel mole fraction was varied from 0.08 to 0.12, burner supply oxygen mole fraction from 0.4 to 0.85, mtotal from 2.3 to 11.3 mg/s, and Tad from 2080 to 2590 K.*
2. At constant burner flow, the normal ethylene flames at 1 atm grew monotonically after ignition while their peak gas temperature generally fell. Burn times were 28-336 s. Radiative extinction occurred when the growing flame's radiative loss approached its chemical heat release. Just before total extinction, many flames entered an oscillatory mode, partially extinguishing and re-forming with growing amplitude. *(trend, high)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p26): *Burn times range from 28 –336 s. All flames grow monotonically after ignition. Peak gas temperature generally decreases with time.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p26): *Radiative extinction is observed when, at constant reactant flow rate, the flame expands until radiation heat loss approaches the chemical heat release.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p26): *Before a flame experiences complete extinction, it may enter an oscillatory mode in which part of the flame partially extinguishes and then reforms.*
3. Steady-state spherical diffusion flames can exist despite radiative loss. This requires the steady flame to be smaller than the radiative-extinction size, and the flame to develop fast enough that radiation does not first drive its temperature below 1130 K. Flames showing steady behaviour burned for up to 870 s on the ISS. In an unbounded domain, the diffusion-controlled approach to steady state takes of order 10^5 s. *(result, high)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *It is found that steady- state gaseous microgravity spherical diffusion flames can exist in the presence of radiation heat loss, provided that the steady-state flame size is less than the flame size for radiative extinction*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *Despite a narrow range of attainable conditions, flames that exhibit steady-state behavior are observed aboard the ISS for up to 870 s, even with the constraint of a finite boundary.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p25): *In the spherical, infinite domain configuration, the characteristic time for the diffusion- controlled system to effectively reach steady-state is found to be on the order of 100,000 s.*
4. Flame size increased with reactant flow rate and decreased with ambient O2. At a fixed ambient O2, larger (higher-flow) flames extinguished radiatively sooner than smaller ones, because of higher radiative loss and falling heat release. *(trend, high)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p39): *Flame size increases with reactant flow rate and decreases with ambient oxygen concentration.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p39): *For constant ambient oxygen concentration, larger flames (with higher fuel flow rates) radiatively extinguish faster than smaller flames (with lower flow rates) due to higher radiative losses and decreasing chemical heat release.*
5. For the smallest, near-steady flames, the porous burner acted as a heat sink. As it warmed, its cooling of the flame weakened and the measured fibre temperature rose with time. Test duration was then limited by the burner temperature limit (set at 500 C in the as-run files), so round-1 data could not prove that these flames were fully steady. *(limit, medium)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p26): *Sufficiently small flames with low radiation losses exhibit quasi-steady behavior, but burner heating is significant, and the experimental duration is dictated by the temperature limit of the porous sphere.*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p40): *The flames investigated appear to be asymptotically approaching a steady-state size and temperature, however, a decisive conclusion cannot be made because of burner heating.*
   - `PSI-10_Raw Data_21328D1.txt` (all): *burnerTemperatureLimitC:500, burnerTemperatureLimitDurationSecs:3*
6. Sustained soot was seen only in 40% O2 with high fuel concentrations. In 21% O2 no flame sooted steadily. Small flames lost too much heat to the burner, and large flames cooled radiatively below the sooting limit too quickly. *(result, medium)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p41): *Constantly sooting flames were only observed in 40% oxygen and high fuel concentrations. In 21% oxygen, small flames did not soot because of heat loss to the burner and large flames did not soot because high radiative losses caused the flame temperature to quickly drop below the sooting limit.*
7. In the precursor 2.2 s drop-tower tests (ethylene and propane, 0.98 bar), radiatively extinguishing spherical flames had peak temperatures at extinction onset of about 1100 K. That is far below the 1500 +/- 50 K usually quoted for hydrocarbon diffusion-flame extinction in normal gravity. Radiative loss was dominated by products outside the flame and scaled with flame surface area, not volume. *(result, high)*
   - `PSI-10_Reports_TaskbookRpts.pdf` (p34): *Peak temperatures at extinction onset were about 1100 K, which is significantly lower than for kinetic extinction.*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p21): *The present results indicate an extinction temperature of about 1100 K for the present flames. This is lower than past measurements of this property in normal-gravity flames (Quintiere 2006).*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p21): *For example, Williams (1981) indicates an extinction temperature of 1500 ± 50 K for hydrocarbon combustion in oxygen/nitrogen mixtures.*
   - `PSI-10_Reports_TaskbookRpts.pdf` (p34): *Radiative heat loss was dominated by the combustion products downstream of the flame and was found to scale with flame surface area, not volume.*
8. In the drop-tower precursor work (2.2 s, ethylene, 1.5 mg/s fuel consumption), the sooting limits of 17 normal and inverse spherical flames were measured. The four at the lowest Z_st (residence times above 0.5 s) were excluded from the fit; the others fell on a line T_ad = 1198 Z_st + 1838 K, so raising Z_st permits about 700 K higher T_ad before soot appears. Convection direction (fuel-to-oxidizer vs oxidizer-to-fuel) had no measurable effect on these sooting limits. *(result, high)*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p15): *Tad(K) = 1198 Zst + 1838*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p16): *The sooting limits follow a linear relationship between adiabatic flame temperature and Zst, with Zst accounting for a variation of about 700 K in the sooting limit ad iabatic flame temperature.*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p16): *Figure 1.7 shows that convection direction has no measurable effect on the sooting limits of these spherical flames.*
   - `PSI-10_Science Documents_SRD_ACMEFlameDesign.pdf` (p16): *Error bars are included for the four flames at the lowest Zst and these flames are excluded from the fit shown.*
9. Measured flame sizes agreed with transient numerical models only after the diffusivity was adjusted. On ISS, one-step-chemistry predictions matched flame size with adjusted diffusivity. In the earlier drop-tower comparison (2.2 s and 5.2 s facilities), close agreement needed thermal and mass diffusivities raised by 30% (or flow reduced by 25%). *(method, medium)*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p40): *Experimental measurements of flame size were in quantitative agreement with numerical results with one-step chemistry, provided the diffusivity was appropriately adjusted.*
   - `PSI-10_Reports_TaskbookRpts.pdf` (p34): *Close agreement could not be obtained without either increasing the model’s thermal and mass diffusion properties by 30% or reducing mass flowrate by 25%.*
   - `PSI-10_Reports_TaskbookRpts.pdf` (p34): *Experiments were performed in 2.2 s and 5.2 s microgravity facilities.*
10. Detailed-chemistry simulations of the ISS ethylene flames (UCSD mechanism, 57 species, 270 reactions) show that as peak temperature falls toward the ~1130 K extinction point, reactant leakage grows and HO2-driven 'warm flame' chemistry appears. This chemistry delays extinction but is not exothermic enough to prevent it. *(result, medium)*
   - <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/13647830.2024.2326830?fields=title,abstract>: *As the flame cools and the peak temperature approaches the critical extinction temperature, there is increased reactant leakage leading to higher O, OH, and HO2 concentrations on the fuel side.*
   - <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/13647830.2024.2326830?fields=title,abstract>: *The appearance of warm flame chemistry delays extinction but is not sufficiently exothermic to prevent it.*
11. One-dimensional transient modelling with a soot sub-model, by the Russian partner team, of the normal and inverse ISS flames (0.5-2 atm) puts soot formation where the local C/O atom ratio is 0.32-0.44 and the temperature exceeds 1300-1500 K. This is consistent with the project hypothesis that soot needs both a critical C/O ratio and a critical temperature. *(result, medium)*
   - <https://doi.org/10.3390/math11020261>: *The results indicate that soot formation in normal and inverse SDFs is concentrated in the region where the local C/O atomic ratio and local temperature satisfy the conditions 0.32 < C/O < 0.44 and T > 1300–1500 K.*
   - <https://doi.org/10.3390/math11020261>: *The objects of this study were “normal” and “inverse” SDFs of gaseous ethylene in an oxygen atmosphere with nitrogen addition at room temperature and pressures ranging from 0.5 to 2 atm.*
   - PSI record field `hypothesis`
12. Vitiation of the closed 83-90 L chamber appears to shorten flames. On day 19171 (40% O2, burner 1003), tests D1 to D5 burned for about 100 s (D1), about 60 s (D2-D4) and about 58 s (D5). The test notes say D5 was run like D1 apart from chamber vitiation; that accumulating combustion products caused the shortening is our inference. *(trend, low)*
   - `PSI-10_Raw Data_19171 flow traces etc.pdf` (p5): *run just like D1 neglecting chamber vitiation (although some inactive parameters differed), where D5 flame lasted for ~58 s, while D1 lasted ~100 s while D2-D4 lasted ~60 s*
   - `PSI-10_Reports_FinalRpt_ACMEFlameDesign.pdf` (p18): *The chamber’s free volume is approximately 83 liters depending on the installed hardware.*
13. Raising pressure lowers the extinction temperature. In round-2 ISS inverse flames with an 85% O2 burner stream (3.41 mg/s O2) into about 10% C2H4 in N2, thin-filament pyrometry gave similar extinction temperatures at 0.5 and 1 atm but about 50 K lower at 3 atm (the dissertation abstract says almost 60 K). At 3 bar the flame passed below the 1-atm critical 1130 K into the warm-flame regime. Simulations at 50 bar show warm-flame chemistry extending the burn by over 500 s, followed by a cool flame. *(trend, medium)*
   - <https://profiles.wustl.edu/en/publications/the-effects-of-elevated-pressure-on-the-kinetics-and-extinction-o/>: *Flame temperatures at extinction are shown to decrease with increasing pressure, and at a pressure of 3 bar the flame is shown to extend below the critical temperature of 1130 K and into the warm flame regime.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *Flame A and C extinguish at similar temperatures, but Flame B extinguishes roughly 50 K lower.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *Experimental results show that increasing the pressure from 1 atm to 3 atm decreased the ethylene extinction temperature by almost 60 K.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *At 50 atm the flame was able to extend its burn time by over 500 s due to the emergence of warm flame chemistry.*
   - Table `tests`: Inverse rows with burner X_O2 0.85 and ambient C2H4 about 0.10 exist at about 1 atm (22018 G1-G3), 3 atm (22027 B and D series) and 0.5 atm (22035 J1-J7). The dissertation (Table 4.1) does not name the test ids, so the match is by conditions only.
14. The transient detailed-chemistry model reproduces the ISS extinction state. For 17 radiatively extinguished normal ethylene flames at 1 atm (ambient X_O2 0.20-0.38, burner X_C2H4 0.13-1, 0.66-4.88 mg/s), measured extinction temperatures were 1130 +/- 23 K against 1126 +/- 6 K simulated, and simulated extinction radii matched measured ones with R^2 = 0.98. Thin-filament pyrometry temperatures carry an estimated +/- 100 K uncertainty. *(result, high)*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *The means are similar, at 1130 ± 23 K for the experiments and 1126 ± 6 K for the simulations*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *There is good agreement between the model and experiments, with an R2 value of 0.98.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *with an estimated uncertainty of ± 100 K*
15. The model matches measured porous-burner temperatures only if heat transfer from the sphere to the gas flowing through it is neglected at high flows, so the reactants appear to be heated elsewhere (supply tube or flame). Burner temperature matters mainly for small flames close to the burner: holding the burner at 298 K lowers the flame temperature at 30 s by 18 K for a 0.66 mg/s flame but by only 3 K for a 5.3 mg/s flame. *(method, medium)*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *The numerical model was shown to be able to predict experimentally measured burner temperature with the assumption that the heating of the fuel gas was ignored.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *At 30 s, the case with constant burner temperature is 18 K lower than the case with experimental burner temperature for Flame A.*
   - <https://api.drum.lib.umd.edu/server/api/core/bitstreams/5523b6f6-11fe-4493-9183-626127ec4e12/content>: *These results indicate that the temperature of the porous sphere has little effect on the overall flame properties, except in cases where the flame is small and close to the burner.*

## Fire-safety relevance

In quiescent microgravity, with no buoyant flow to strain or blow off a flame, gaseous diffusion flames survive until radiative loss cools them to about 1130 K. That is several hundred kelvin below normal-gravity extinction temperatures. Spherical ethylene flames burned for minutes (up to 870 s) at constant fuel supply. For spacecraft fire safety this means: (1) a small, slow fuel leak can sustain a weak, possibly dim flame much longer than ground experience suggests; (2) extinction criteria based on a ~1500 K limit temperature are non-conservative in microgravity; (3) larger flames self-extinguish sooner, by radiation, than smaller ones at the same atmosphere; and (4) the critical flux of about 0.2 g/m^2/s fuel (1 atm, ethylene) offers a simple test for whether a diffusion flame fed at a given rate can persist. The PI explicitly cited pressure-dependent extinction data as valuable for spacecraft fire safety. The ACME documents themselves state that ACME was not designed as a fire-safety project. These are gas-burner flames, not material flammability limits.

### Habitat conditions

Normal ethylene flames burned in ambient O2 of 0.20-0.40 at 0.99-1.31 atm (100-133 kPa), so O2 partial pressures were about 21-53 kPa. That brackets sea-level air (20.9% at 101.3 kPa) and exceeds the O2 partial pressure of the proposed Moon habitat (>=30% at <=70.3 kPa, about 21 kPa O2). No normal-flame (oxygen-atmosphere) test was run at reduced total pressure, so the habitat combination of enriched O2 at ~70 kPa was not reproduced. Reduced (0.43-0.52 atm, 43-53 kPa) and elevated (2-3 atm) pressures were used only for inverse flames, where the ambient is ethylene/N2 and O2 comes from the burner at up to 85%. That equals the highest O2 in PSI, also used in ACME CFI-G, but it does not represent a habitat atmosphere. The spacesuit condition (100% O2 at 29.6 kPa) was not approached.

### Earth benefits

The work is aimed at 'designed' non-premixed flames: shifting inert from oxidizer to fuel and enriching oxygen, to get robust, soot-free burners. It is cited as contributing to oxy-fuel combustion and to novel designs of future coal power plants with lower pollutant emissions.

## Limitations

- The sintered spherical burners did not give truly centred spherical flames, especially at high flow. More flow leaked through the sphere-tube joint, and heat loss to the support tube caused local quenching. The first burner (1002) was replaced mid-round 1 and some tests were repeated; burner 1003 was better but still imperfect. Operator notes record asymmetric flames and asymmetric extinction.
- By the PI's own account, gas-temperature and soot-volume-fraction diagnostics fell short. The round-1 radiometers saturated in nearly every test. The TFP fibre array was misaligned to the DataCam for four round-2 test days. HiBMs soot extinction is compromised by soot emission and asymmetric soot clouds, and the BG7 filter cut red too strongly for accurate pyrometry.
- Methane, CO2 dilution, coflow flames and 0.2 atm tests from the original objectives were not flown. Normal flames were capped at 40% O2 and inverse flames at 65% C2H4 for safety. Only ethylene (plus one propane day) and N2 were used.
- The chamber is closed, so each successive test on a day burned in a slightly vitiated, higher-pressure atmosphere (table conditions are approximate and ignore vitiation). Mass-flow controllers were not always steady or on set-point. The CIR vibration isolation (PaRIS) was not used, and g-jitter has not been correlated with the data.
- Published ISS results (critical extinction point, steady flames) are for about 1 atm. The PSI documents contain no analysis of the round-2 reduced- and elevated-pressure tests, and the pressure paper could not be retrieved. [Publications pass 2026-11-15: the pressure results were since found in the paper's abstract and the Waddell 2023 dissertation, see findings[12]; they cover three inverse flames only.]
- These are porous-sphere gas-burner flames with prescribed reactant supply. Their extinction and sooting limits are not flammability limits of solid or liquid spacecraft materials.

## Data in PSI

PSI holds 3,807 files (about 2.18 TB) for PSI-10. The two experimental tables (327 tests with conditions: mole fractions, mass flows, pressure, Z_st, T_ad) and the documents are small and immediately usable. They are the Final Report (2023, 92+ pages), the SRD (2010), the ACME ISRD and SORD, the Engineering Implementation report and 16 years of NASA Task Book reports. Per-test raw data are complete but heavy. Per test there are a 125 Hz data CSV (raw channel voltages for MFCs, pressure transducers, PMTs, thermocouples and radiometers, not engineering units), an MFC set-point CSV, the as-run parameter file, a test-point timeline (TP) with extinction-detection time, comments on missing images, and daily 'flow traces' PDFs with operator notes. Imagery is 1,183 zip archives (about 2.1 TB: DataCam raw and converted TIFFs, intensified and HiBMs images) and 317 ops-video .ts recordings (75 GB); none is downloaded here. Burn time, flame diameter and temperatures are not tabulated anywhere in PSI.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | Normal Flame (207 rows) and Inverse Flame (120 rows) test-condition tables | .csv | 2 | 40 kB | yes |
| Reports / Science / Engineering Documents | Final Report 2023, Task Book reports FY2004-FY2024, publication list, SRD 2010, ACME ISRD and SORD, ACME Engineering Implementation report | .pdf | 7 | 14.7 MB | yes |
| Raw Data | per-test 125 Hz sensor data in raw volts (_data.csv) and MFC set-points | .csv | 634 | 1.25 GB | yes |
| Raw Data | per-test notes: as-run parameter files, test-point timelines (_TP), image-downlink comments, camera configuration files | .txt | 993 | 1 MB | yes |
| Raw Data | daily test sheets, test-parameter notes, daily test-point logs (scanned, 51 without text layer) and 'flow traces etc' operator-note PDFs | .pdf | 69 | 110 MB | yes |
| Raw Data | intensified-camera frame index files, module/ACD logs, ACME logs, chamber-calculator workbooks | .mdipsug .asc .log .xlsx | 593 | 150 MB | yes |
| Raw Data | image archives: DataCam (_ACME, _ACME_Converted), intensified (_INTNS), HiBMs | .zip | 1183 | 2.1e+03 GB | no |
| Raw Data | ops (analog) camera video recorded on the ground | .ts | 317 | 75.1 GB | no |
| Representative Image(s) | flame and hardware photographs | .jpg .png | 5 | 900 kB | yes |

Rows in the unified `tests` table: 327

## Related investigations

- [PSI-23](PSI-23-acme-s-flame.md): shared hardware
- [PSI-159](PSI-159-acme-cfi-g.md): shared hardware
- [PSI-21](PSI-21-acme-cld-flame.md): shared hardware
- [PSI-20](PSI-20-acme-bre.md): shared hardware
- [PSI-22](PSI-22-acme-e-field-flames.md): shared hardware

## Open questions

- Convert the per-test 125 Hz _data.csv voltages to engineering units and tabulate burn time, extinction time and burner temperature for all 327 tests. PSI contains no outcome column.
- Map extinction (1130 K / critical-flux criterion) against chamber pressure using the round-2 inverse tests at 0.43-0.52, 1, 2 and 3 atm.
- Test whether the critical fuel and oxygen fluxes (0.2 and 0.68 g/m^2/s) hold for the propane day and for normal flames above 1.1 atm.
- Quantify how vitiation within a test day (successive tests in the closed chamber) shifts burn time, using repeated test points such as 19171D1-D5.
- Extract sooting-limit conditions (onset and disappearance of yellow luminosity) versus Z_st and T_ad from the DataCam images, and compare them with the drop-tower line T_ad = 1198 Z_st + 1838 K.

## Dashboard ideas

- **test-condition map** (`config`, `x_o2 (ambient for normal, burner for inverse)`, `fuel_fraction`, `pressure_kpa`, `mean Zst`, `t_ad_k`): Shows the 327 ISS test points in Z_st-T_ad space split by normal/inverse and pressure, with the drop-tower sooting-limit line overlaid.
- **extinction size predictor** (`mtot (mg/s)`, `mfuel or mO2 (mg/s)`, `config`): Applies r_ext = sqrt(m/(4*pi*m''_crit)) with 0.2 or 0.68 g/m^2/s to show expected flame radius at radiative extinction for any 1 atm test.
- **pressure ladder of inverse tests** (`test_id`, `pmean (atm)`, `XO2`, `XC2H4 initial`, `mtot (mg/s)`): Highlights the only PSI flames run at 43-53 kPa and at 2-3 atm, which have not yet been analysed in PSI documents.
- **test-day timeline** (`date`, `test_id`, `x_o2`, `pressure_kpa`, `burner serial`): Reveals vitiation and pressure drift within days and the burner swap (1002 to 1003) that affects data quality.

## Gaps and data-quality notes

- No per-test outcomes (ignited or not, burn time, extinction diameter or temperature, sooting yes/no) exist in the experimental tables or tests.csv. burn_time_s, extinction_mode and ignited are empty for all 327 rows. Outcomes would need the 125 Hz data CSVs (raw volts, no calibration in PSI) or the 2.1 TB of image zips and 75 GB of video, none of which were downloaded.
- Results for the round-2 reduced- and elevated-pressure inverse flames (0.43-3 atm) are not in any PSI document. The relevant paper (Waddell et al., Proc. Combust. Inst. 40 (2024) 105400, doi:10.1016/j.proci.2024.105400) was unreachable: no abstract on Crossref, Semantic Scholar or OpenAlex, and ScienceDirect blocked access. The Waddell 2023 dissertation (University of Maryland) was not located. [Publications pass 2026-11-15: the abstract of Waddell et al. 2024 is on the WUSTL research portal and the first author's 2023 UMD dissertation is open on DRUM (hdl.handle.net/1903/29996); the pressure results are now findings[12]. The paper's full text is still paywalled.]
- Full texts of Irace et al. 2021 (Combust. Flame 229, 111373) and the two 2023 Proc. Combust. Inst. papers were not retrieved. Their abstracts are reproduced in the Final Report, which was used instead. The 'simple equation' for extinction flame size is therefore reconstructed here from mass conservation, not quoted.
- Ambient (chamber) temperature is not given in the tables. The drop-tower SRD assumes 300 K burner temperature, but no ISS value was found.
- Final Report Table 1 counts 326 ignited flames (188 + 138). The tables have 327 rows (207 normal incl. 20 propane, 120 inverse), and some rows are ramped tests or possibly unsustained ignitions; the mapping is not stated.
- 51 scanned Raw Data PDFs (test sheets, test-parameter notes, daily test-point logs) have no text layer and were not read. None is a report.
- Several documents contain institutional contact details (emails, phone numbers, a manufacturer's sales contact in the ACME ISRD; PI phone/address in the Task Book reports, PSI-10_Reports_TaskbookRpts.pdf). These were not copied.
- No document contained text addressed to an AI or unrelated instructions.
