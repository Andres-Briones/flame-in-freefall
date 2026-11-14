# PSI-159: ACME CFI-G (Advanced Combustion via Microgravity Experiments / Cool Flames Investigation with Gases)

Ground-commanded tests on the ISS burned ethane, propane and butane on a pea-sized porous sphere, both normally (fuel out of the sphere into an oxygen/nitrogen atmosphere) and inside-out (an oxygen-rich stream of up to 85% O2 out of the sphere into a fuel-filled chamber), and found the first spherical 'cool flames' of gaseous fuel.

Investigators: Peter B. Sunderland (PI; University of Maryland, Department of Fire Protection Engineering); Richard L. Axelbaum (Co-I; Washington University in St. Louis); Forman A. Williams (Co-I; University of California, San Diego); Dennis P. Stocker (ACME Project Scientist; NASA Glenn Research Center)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS) |
| Facility | Combustion Integrated Rack (CIR), ACME chamber insert (constant-volume chamber, about 83 L free volume) |
| Dates | 2021-03-29 to 2021-10-18 |
| Fuels and samples | Ethane; Propane; n-Butane; Oxidiser |
| Varied | flame configuration: normal (fuel from burner into O2/N2 atmosphere; 179 tests) and inverse (O2/N2 from burner into fuel/N2 atmosphere; 154 tests)<br>fuel: ethane (94 tests), propane (99), n-butane (140)<br>ambient (chamber) O2 mole fraction, normal flames only: 0.18-0.40 (nominal fills of about 0.18, 0.21, 0.30 and 0.40; values drift down during a day) mole fraction<br>burner-stream O2 mole fraction, inverse flames only (NOT the ambient; the chamber held fuel + N2): 0.12-0.85 (79 of 154 inverse tests at 0.85) mole fraction<br>fuel mole fraction: normal: 0.018-1.0 in the burner stream; inverse: 0.056-0.43 in the chamber atmosphere mole fraction<br>chamber pressure: normal: 0.51-3.04 bar (50.7-304 kPa; nominal 7.35-44.1 psia); inverse table values 0.50-3.31 bar (49.5-331 kPa) kPa<br>burner mass flow of the limiting reactant (hydrocarbon in normal flames, O2 in inverse flames): normal: 0.1-3.2 mg/s hydrocarbon; inverse: 0.93-9.08 mg/s O2 mg/s<br>igniter energy (standard vs reduced, to try direct cool-flame ignition): preheat 2-3 V, ignition 2.5-4 V for 3-20 s V |
| Number of tests | 333 |
| Fire-safety pillars | fundamental, prevention, detection |

## Question

Cool diffusion flames, with peak temperatures of about 500-1000 K and governed by low-temperature (negative-temperature-coefficient) chemistry, were discovered in 2012 in ISS droplet experiments (FLEX, CFI). Droplets burn unsteadily and allow neither gaseous fuels, fuel dilution nor inverse flames. CFI-G set out to show, for the first time: steady cool diffusion flames on a spherical porous burner; cool flames of propane, n-butane and (as proposed) n-pentane over a wide range of stoichiometric mixture fraction $Z_{st}$, adiabatic flame temperature $T_{ad}$ and pressure; inverse cool flames; and cool flames that extinguish when the burner flow decreases and turn into hot flames when it increases. The data were meant to test and improve cool-flame kinetic mechanisms with CFD, and so to support more efficient engines. Because n-pentane's vapour pressure is too low for the CIR gas system, ethane replaced it.

## Summary

CFI-G, part of NASA's ACME project, burned spherical diffusion flames on a 6.35 mm porous burner in the ISS Combustion Integrated Rack from March to October 2021. It ran 333 tests on 23 days. In normal flames, nitrogen-diluted ethane, propane or n-butane flowed into atmospheres of 18-40% O2 at 0.5-3 atm. In inverse flames, an O2/N2 stream of 12-85% O2 flowed from the burner into a chamber filled with fuel and nitrogen; the chamber held no oxygen. Of 280 hot flames, 189 extinguished radiatively. Fifteen were followed, after about 1 s, by a quasi-steady cool diffusion flame, the first observed for gaseous fuels. These occurred only for 30% n-butane flowing at 0.75-1.5 mg/s into 39-40% O2 at 2 bar, with burner temperatures above 515 K. The hot flames were 2.6 times larger than the cool flames that followed. All normal flames in about 21% O2 self-extinguished within 20 s. Inverse flames from 85% O2 self-extinguished in 41 of 43 tests at 2-3 bar but in 0 of 14 at about 0.5 bar. These are burner flames, not material flammability limits.

## Physics

A diffusion flame sits where fuel and oxidiser meet in stoichiometric proportion. Around a porous sphere in microgravity, the flow is purely radial and weakens as $1/r^2$. A few burner diameters out, transport is by diffusion alone, so the flame is spherical and one-dimensional. On Earth, buoyancy breaks the symmetry. The investigators estimate a Richardson number of about 1300 in 1 g for this configuration. Reducing it well below 1 needs a gravity level about $10^{-4}$ g. The diffusion time $r^2/D$ at a 25 mm radius is about 30 s. Drop towers therefore cannot reach quasi-steady flames, still less observe their radiative extinction and any cool flame that follows. In a normal flame the fuel issues from the sphere and soot forms on the inside of the flame. In an inverse flame the oxidiser issues from the sphere, so the flame is inside out and soot forms on the outside. Microgravity flames grow slowly. They lose heat by radiation from soot and gas, and to the burner and its support tube. Many therefore extinguish radiatively after tens of seconds. Hydrocarbons such as n-butane have a negative-temperature-coefficient region in which low-temperature oxidation, producing formaldehyde, CO, H2O2 and H2O, can sustain a weak 'cool' flame at a few hundred kelvin above ambient. Such a flame can appear after the hot flame dies, provided the fuel stream and the burner surface are warm enough and the residence time is long. For fire safety, cool flames are a reminder that a mixture can keep reacting and can re-ignite after visible extinction.

$$
Ri = \frac{g\,\Delta T\,L}{T\,u^2}
$$

Richardson number, the ratio of buoyancy to inertia. $g$ gravitational acceleration (m/s2); $\Delta T$ flame-to-ambient temperature difference (K); $T$ ambient temperature (K); $L$ characteristic length (m); $u$ characteristic velocity (m/s). With the investigators' values ($L$ = 50 mm, $u$ = 5 cm/s, $\Delta T$ = 2000 K, $T$ = 300 K), $Ri \approx 1300$ in 1 g. Spherical flames need $Ri \ll 1$, i.e. $g$ reduced by about four orders of magnitude. Order-of-magnitude estimate only.

`PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p5): *Taking as representative values L = 50 mm, u = 5 cm/s, ΔT = 2000 K, and T = 300 K, Ri = 1300 in normal gravity.*

$$
t_D \sim \frac{r^2}{D}
$$

Diffusion time to establish the flame at radius $r$ (m) with mass diffusivity $D$ (m2/s). For $r$ = 25 mm and $D$ = 20 mm2/s, $t_D \approx 30$ s. This is why about 30 s of quiet microgravity is needed and drop towers (2-5 s) are insufficient. Scaling estimate; the radial velocity decays as $1/r^2$, so diffusion dominates beyond a few burner radii.

`PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p5): *For r = 25 mm and D = 20 mm2/s, this diffusion time is 30 s.*

$$
r_{hf} = \frac{\dot m}{4\pi\rho D\,\ln\!\left(\frac{1}{1-Z_{st}}\right)}\ \text{(normal)},\qquad r_{hf} = \frac{\dot m}{4\pi\rho D\,\ln\!\left(\frac{1}{Z_{st}}\right)}\ \text{(inverse)}
$$

Quasi-steady hot-flame radius for a porous-sphere burner (Spalding droplet model applied to burner flames by Kim et al.). $\dot m$ total burner mass flow (kg/s); $\rho D$ density times mass diffusivity, taken constant (fitted as 0.0334 g/(m s) at 300 K); $Z_{st}$ stoichiometric mixture fraction. Assumes unit Lewis number, constant $\rho D$, uniform pressure, quasi-steady flow, and radiation absorbed into the choice of transport rate. The inverse form shows why the inverse-flame size scales with the oxidiser flow. Fitted against hot and cool flame radii with $R^2$ = 0.92.

<https://par.nsf.gov/servlets/purl/10426596>: *ρD was optimized to a value of 0.0334 g/m-s at 300 K.*
<https://par.nsf.gov/servlets/purl/10426596>: *The data has a coefficient of determination of R 2 = 0.92 with respect to the line shown with unity slope.*

$$
Z_s = 1-\exp\!\left(\frac{-\dot m}{4\pi r_s \rho D}\right),\qquad Z_{cf} = \frac{(T_{cf}-T_\infty)\,Z_s}{2T_{cf}-T_s-T_\infty},\qquad \frac{r_{hf}}{r_{cf}} = \frac{\ln(1-Z_{cf})}{\ln(1-Z_{st})}
$$

Partial-burning (cool-flame) model for a normal burner flame. $Z_s$ mixture fraction at the burner surface of radius $r_s$ (m); $Z_{cf}$ mixture fraction at the cool flame; $T_{cf}$ cool-flame peak temperature, $T_s$ burner surface temperature, $T_\infty$ ambient temperature (K). The cool flame sits where $dT/dZ$ changes sign, so both the burner and the ambient must be cooler than the cool flame. As $T_s \to T_{cf}$ the cool flame collapses onto the burner. For the ISS cool flames the model gives $Z_s$ = 0.75, $Z_{cf}$ = 0.53 and $T_{cf} \approx$ 869 K, with predicted $r_{hf}/r_{cf}$ = 3.2 against 2.6 measured.

<https://par.nsf.gov/servlets/purl/10426596>: *This relationship, along with its analog for in- verse flames, shows that for both flame types the burner surface and the ambient must be cooler than the cool flame.*
<https://par.nsf.gov/servlets/purl/10426596>: *The mean measured r hf / r cf is 2.6 and the mean predicted by Eq. (12) is 3.2.*

## Method

### Apparatus

Tests ran in the ACME chamber insert of the CIR, a windowed constant-volume chamber of about 83 L free volume. Burner flow raised the pressure and depleted the reactant during each day. The burner was a 6.35 mm sphere of sintered 316 stainless steel (10 micron media, about 41% porosity), sinter-bonded to a stainless supply tube. A fine type-K thermocouple was embedded up to about 1 mm into the sphere to measure burner temperature. Tests were terminated if the burner reached 723 K. Three crew-exchangeable mass flow controllers metered fuel, oxidiser and ISS nitrogen. Only one gas stream could be diluted with nitrogen on orbit at a time. CFI-G used a coiled Kanthal A-1 hot-wire igniter (0.32 mm wire) on a retracting arm. Cool flames were imaged by the intensified CFI camera, which had a formaldehyde (CH2O*) bandpass filter (390-490 nm) and ran at about 23 frames/s. Hot flames were also imaged by the ACME colour DataCam (12-bit, up to 30 fps, often about 1 fps with long exposures). The analog video was recorded on the ground. Other instruments: a CFI-G radiometer array with two fixed gains per sensor; a Schmidt-Boelter wide-angle radiometer at 154 mm radius (0.6-50 µm); three wide-angle PMTs (230-700 nm, 310 nm OH*, 430 nm CH*); thermocouple rakes; two thermocouples at 200 mm; and a chamber pressure transducer. On the far rake, thermocouple tips were at 45, 60, 100 and 100 mm from the burner centre. On the near rake they were at 13, 25, 50 and 100 mm. On each rake, the two innermost were type B (Pt/Rh) and the rest type K. The thin-filament pyrometry array had only 3 of its 5 SiC fibres (14 µm) left. Non-imaging data were logged at 125 Hz. The HiBMs camera with CIR backlight was rarely used: its IPSU failed on day 1 and was replaced on 18 May 2021.

### Fuels and samples

- Ethane (C2H6), from bottles of 100% C2H6 or 30% C2H6 / 70% N2, further diluted on orbit with ISS N2 as needed. Burner fuel in normal flames; mixed with N2 to fill the chamber (about 6-30% C2H6) for inverse flames. Substituted for the proposed n-pentane (gas, porous spherical burner (normal) or quiescent chamber fill (inverse))
- Propane (C3H8), from 100% C3H8 or 30% C3H8 / 70% N2 bottles. Normal-flame burner fuel; chamber fill of about 8-43% C3H8 in N2 for inverse flames. The fuel supply was two-phase for inverse propane flames (gas, porous spherical burner (normal) or chamber fill (inverse))
- n-Butane (n-C4H10), from 100%, 50% (in N2) or 30% (in N2) bottles. Normal-flame burner fuel; chamber fill of about 6-36% n-C4H10 in N2 for inverse flames. All observed cool flames used 30% n-butane / 70% N2 as burner fuel (gas, porous spherical burner (normal) or chamber fill (inverse))
- Oxidiser: O2/N2 bottles of 21, 30 and 40% O2 (balance N2) to fill the chamber for normal flames, which ACME capped at 40% O2. For inverse flames, an 85% O2 / 15% N2 bottle fed the burner. ISS nitrogen diluted it on orbit to give burner-stream O2 mole fractions of 0.12-0.85. In inverse tests the chamber held only fuel and nitrogen, so the 85% O2 never formed the ambient atmosphere (gas, chamber atmosphere (normal flames) or burner stream (inverse flames))

### Procedure

The crew configured the hardware: they swapped bottles and MFCs, exchanged igniter tips and changed thermocouple rakes. All tests were then run from the Glenn ISS Payload Operations Center using pre-programmed scripts and parameter files. No tests used manual control, apart from ending a test after extinction or on burner over-temperature. Round 1 (29 Mar - 23 Jun 2021, 10 days) used normal flames: the chamber was filled with an O2/N2 atmosphere of nominally 18%, 21% or 40% O2 at 0.5, 0.93, 1, 2 or 3 atm, and fuel flowed from the burner at 0.1-3.2 mg/s. Round 2 (15 Jul - 4 Oct 2021, 12 days) used inverse flames: the chamber was filled with fuel/N2 at 0.5-3 atm, and an O2/N2 mixture of 12-85% O2 flowed from the burner at about 0.9-9.1 mg/s O2. An added 13th round-2 day (18 Oct 2021) repeated the cool-flame normal-flame conditions of 23 Jun (30% n-butane into about 40% O2 at 2 atm) using the near thermocouple rake. In each test the scripted sequence recorded pre-ignition data and images, ignited the flame with the hot wire and retracted it, then held constant flow. The flow timeout was typically 90-360 s, and 66 s on many inverse tests. Post-flame data followed. The burner-flow conditions in a scripted run were constant; dilution, flow rate, O2 fraction and igniter energy were changed between tests. Some round-1 tests tried to ignite cool flames directly with low igniter power, using 2-2.9 V for 10-20 s instead of the standard 3 V preheat and 3.75-4 V ignition. A twin safety timer limited each day's total limiting-reactant flow to 999 s. About 12 tests were run per day. The chamber was not vented between tests, so O2 (or fuel) fell and pressure rose during the day. The investigators estimated chamber composition after each test from the flows, assuming complete or no combustion. Since the cool flames of 23 Jun were found only afterwards, in data review, flow was kept on after radiative extinction in later tests.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| flame configuration | normal (fuel from burner into O2/N2 atmosphere; 179 tests) and inverse (O2/N2 from burner into fuel/N2 atmosphere; 154 tests) |  |
| fuel | ethane (94 tests), propane (99), n-butane (140) |  |
| ambient (chamber) O2 mole fraction, normal flames only | 0.18-0.40 (nominal fills of about 0.18, 0.21, 0.30 and 0.40; values drift down during a day) | mole fraction |
| burner-stream O2 mole fraction, inverse flames only (NOT the ambient; the chamber held fuel + N2) | 0.12-0.85 (79 of 154 inverse tests at 0.85) | mole fraction |
| fuel mole fraction | normal: 0.018-1.0 in the burner stream; inverse: 0.056-0.43 in the chamber atmosphere | mole fraction |
| chamber pressure | normal: 0.51-3.04 bar (50.7-304 kPa; nominal 7.35-44.1 psia); inverse table values 0.50-3.31 bar (49.5-331 kPa) | kPa |
| burner mass flow of the limiting reactant (hydrocarbon in normal flames, O2 in inverse flames) | normal: 0.1-3.2 mg/s hydrocarbon; inverse: 0.93-9.08 mg/s O2 | mg/s |
| igniter energy (standard vs reduced, to try direct cool-flame ignition) | preheat 2-3 V, ignition 2.5-4 V for 3-20 s | V |

Held constant:

- burner: 6.35 mm porous 316 stainless-steel sphere
- diluent: nitrogen (fuel, oxidiser and atmosphere)
- ambient temperature: about 298-300 K
- gravity: ISS microgravity; tests not run during thruster firings or dockings

Number of tests: 333

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| hot-ignition outcome (yes / no / momentary flash) | PMTs, video, investigator review | derived |
| extinction mode: self-extinguished (radiative extinction) vs flow-terminated (timeout or burner over-temperature) | PMT and radiometer traces | derived |
| hot-flame burn time | PMT-2 / radiometer | derived |
| peak burner surface temperature | embedded type-K thermocouple in porous sphere | direct |
| hot and cool flame radii | CFI intensified camera (CH2O* filter), ACME DataCam | derived |
| radiant heat flux vs time (used to detect cool flames after hot-flame radiative extinction) | thermopile radiometers (dual gain) | direct |
| gas temperature near the flame | type-B and type-K thermocouples on rakes (13-100 mm) and at 200 mm; SiC thin-filament pyrometry (occasional) | direct |
| OH*, CH* and broadband chemiluminescence | three PMTs | direct |
| burner flows (fuel, oxidiser, N2), chamber pressure | mass flow controllers, pressure transducers | direct |
| derived T_ad and Z_st per test | calculation by investigators | derived |

## Findings

1. Fifteen spherical cool diffusion flames of a gaseous fuel were observed, the first such observation. All followed radiative extinction of a hot flame, after a dark interval of 0.7-1.1 s. The cool flames of four tests in June 2021 (21174 C3, C4, C6, F1) were quasi-steady for about 14 s and disappeared when the fuel flow stopped; in one test the radiometer and burner temperature were steady enough to suggest the cool flame would have lasted indefinitely. The ten cool flames of tests 21291 A1 and C1 instead ended by re-igniting into hot flames. *(result, high)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p44): *Of those that extinguished radiatively, 15 subsequently reignited as cool diffusion flames.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p44): *For test points 21174C3, C4, C6, and F1, the cool flames lasted for approximately 14 s and disappeared as soon as the fuel flow stopped.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *A similar delay, 0.7 –1.1 s, occurred for all 15 cool flames.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *During the cool flame, the radiometer output and burner temperature were steady enough to suggest this flame would have lasted indefinitely with continued flow and an infinite domain.*
2. Cool flames formed in a narrow window only: normal (not inverse) flames, n-butane (not ethane or propane) at 30% in N2 in the burner stream, flowing at 0.75-1.5 mg/s into 0.385-0.399 ambient O2 at 2.03 bar (about 203 kPa). Burner temperature also had to be above 515 K. None were seen below about 0.4 O2, below 2 bar, or for any inverse flame, including those fed with 85% O2. *(limit, high)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p44): *These cool flames were observed only with the following conditions: a) concentrations of 30 vol% n- butane and 40 vol% O2, b) normal flames, c) a pressure of 2.03 bar, and d) mass flow rates between 0.75 – 1.5 mg/s.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p46): *21174C3 0.395 0.300 2.03 1.50 13.9 17.6 7.6 2.3*
   - <https://par.nsf.gov/servlets/purl/10426596>: *these cool flames were only observed for burner temperatures above 515 K*
   - <https://par.nsf.gov/servlets/purl/10426596>: *Cool flames were not observed for oxygen mole fractions below about 0.4, which is consistent with a limiting oxygen index for cool flames*
3. No inverse cool flames appeared in 154 inverse tests. The investigators attribute this mainly to short residence times. The paper also states that inverse flames had low burner temperatures (below 500 K), against more than 515 K needed in the normal cool-flame tests. The PSI inverse table disagrees: 44 of 151 inverse tests with a reading had a peak burner temperature above 500 K, up to about 925 K (21242 A1). Hypothesis 4 (inverse cool diffusion flames) was therefore not demonstrated. *(null_result, medium)*
   - <https://par.nsf.gov/servlets/purl/10426596>: *Cool flames were not observed for inverse burn- ing, primarily because of short residence times.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *The inverse flames also had low burner temperatures (below 500 K), but droplet cool diffusion flames are observed with surface temperatures near 400 K.*
   - Table `tests`: config = inverse; peak_temp_c + 273.15 > 500 K in 44 of 151 non-null readings (154 inverse tests); maximum 924.65 K at 21242 A1.
   - PSI record field `hypothesis`
4. Cool flames were smaller than the hot flames that preceded them. Measured hot-flame radii were 12.4-17.7 mm and cool-flame radii 5.1-7.6 mm, a mean ratio r_hf/r_cf of 2.6 against 3.2 predicted by the investigators' Spalding-type partial-burning model. Fitting the model to the radii gives a cool-flame mixture fraction of 0.53 (fuel-rich side of Z_st = 0.20), a burner-surface mixture fraction of 0.75 and an inferred cool-flame peak temperature of about 869 K. A SiC filament placed in one cool flame did not glow, so its peak temperature was below the 950 K detection limit of thin-filament pyrometry. *(result, high)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p23): *The hot flames that spawned the CDFs were 2.6 times as large.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p23): *They also indicate that the observed CDFs reside in rich regions near a mixture fraction of 0.53.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *The mean measured r hf / r cf is 2.6 and the mean predicted by Eq. (12) is 3.2.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *Finally, the mean T cf is found from Eq. (10) to be 869 K.*
   - <https://par.nsf.gov/servlets/purl/10426596>: *No glow was detected in the filament, indicating the peak temperature was below the TFP detection limit of 950 K*
5. With a platinum-containing type-B thermocouple about 1 cm (13 mm radius) from the burner (18 Oct 2021 repeat day), each cool flame re-ignited into a hot flame within seconds. The thermocouple sat in the rich premixture left after hot-flame extinction and catalysed it once it reached 720-820 K. Test 21291C1 cycled through 6 hot and 5 cool flames, and 21291A1 also gave 5 cool flames, until the flow stopped at about 165 s. A catalytic surface near a flame-extinguished fuel/oxidiser mixture can thus repeatedly re-ignite a hot flame. *(result, high)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p15): *It appears that the closest thermocouple, approximately 1 cm from the burner surface, was a factor in the reignition.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p15): *The exposed type-B thermocouple includes platinum, a catalyst for the oxidation of hydrocarbons.*
   - Table `tests`: Row 21291 C1, Comments: '5 transitions from hot to cool, 6 hot and 5 cool flames'.
   - <https://par.nsf.gov/servlets/purl/10426596>: *These reignitions occurred for Tests F and G when the thermocouple reached 720 – 820 K*
6. Of 280 hot flames, 189 extinguished radiatively (self-extinguished) and the rest at flow termination. In the experimental tables, 183 of 272 tests with a recorded outcome self-extinguished: 102 of 133 normal (77%) and 81 of 139 inverse (58%). By fuel the fraction was similar: normal ethane 30/40, propane 34/40, n-butane 38/53; inverse ethane 27/49, propane 24/37, n-butane 30/53. Median hot-flame burn time was 29.5 s for self-extinguished normal flames and 8 s for self-extinguished inverse flames. For flow-terminated flames it was 61 s (normal) and 66 s (inverse, the usual flow timeout). The longest burns were 304 s (normal) and 152 s (inverse). *(result, high)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p44): *Among them, 189 flames experienced radiative extinction, and the rest were extinguished when their flow was terminated, either because the preset flow time was out or the burner overheated.*
   - Table `tests`: Crosstab of extinction_mode by config and fuel for rows with non-null extinction_mode (272); burn_time_s medians and maxima by config and extinction_mode. Flash rows count as self-extinguished with 1 s burn time.
7. Normal flames in nominally 21% O2 (x_o2 below 0.25, mostly 0.21-0.22 with a few at 0.18 and 0.23; any pressure 0.5-3 atm, any fuel) were weak. Only 41 of 64 tests ignited. All 41 with a recorded outcome self-extinguished, with a median burn time of 8 s and a maximum of 20 s. At about 40% O2, 88 of 112 tests ignited. Only 60 of 89 self-extinguished (67%), with a median burn time of 49 s; the others ran until flow timeout or burner over-temperature. Heavily diluted fuel streams (burner fuel mole fraction below 0.05) ignited in only 14 of 40 tests. Most of those 14 burned for about 1 s. *(trend, high)*
   - Table `tests`: config = normal; x_o2 < 0.25 vs > 0.35; counts of ignited and extinction_mode; burn_time_s median/max. Fuel-fraction split at fuel_fraction < 0.05.
8. Inverse flames fed with 85% O2 (burner stream; chamber of fuel + N2) showed a strong pressure effect. At 2.2-3.3 bar (221-331 kPa), 41 of 43 self-extinguished, with a median burn time of 11 s. At 0.55 bar (55 kPa), 0 of 14 self-extinguished: all ran to flow termination (median 66 s), several hitting the burner temperature limit. Across all inverse O2 levels, the self-extinguished fraction was 0/26 at 0.55 bar, 19/39 at 1.1 bar, 31/35 at 2.2 bar and 28/33 at 3.3 bar. Self-extinction (radiative extinction) of these inside-out flames is thus much more likely at elevated pressure, consistent with stronger radiative loss. This is an inference from outcome counts, not a measured radiation balance. *(trend, medium)*
   - Table `tests`: config = inverse; grouped by round(pressure_kpa) and x_o2 > 0.8; counts of extinction_mode and burn_time_s medians.
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p65): *These oscillations grew in strength until the flame self-extinguished.*
9. Raising the burner-stream O2 fraction made inverse flames easier to ignite. With 85% O2, 76 of 79 tests ignited (plus one momentary flash), and all 22 at 50% O2 ignited. With 21% O2, only 16 of 27 ignited. Below 20% O2 (0.12-0.19), 6 of 12 ignited, 5 more gave only a momentary flash, and the 0.12 O2 test did not ignite. *(trend, high)*
   - Table `tests`: config = inverse; crosstab of nominal x_o2 vs ignited (null = 'flash' in the 'Hot ignition' column).
10. The flames approached radiative extinction through growing oscillations and local quenching that opened holes in the flame shell. Soot clusters escaping the flame added to the heat loss. A hole lets fuel and oxidiser mix directly, which the investigators note enhances flammability. Inverse flame size was set by the O2 flow, the limiting reactant: larger O2 flow gave a larger flame, while extra N2 at fixed O2 flow did not change the size. *(result, medium)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p58): *The escaping soot clusters exacerbate the heat loss experienced by the flame and cause it to locally quench, creating a hole in the flame.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p58): *This hole allows for direct mixing of the fuel and oxygen, which are normally separated by the flame, thereby enhancing flammability.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p62): *The opening, which allows reactant mixing, often oscillates in size while growing until the flame fully extinguishes.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p60): *The flame size is dependent on the limiting reactant, which for inverse flames is the oxygen.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p61): *Flame size is determined by access to sufficient fuel to consume the oxygen, which was at the same flow rate in both cases.*
11. Normal flames, especially at elevated O2 and pressure, were bright and sooty at ignition. In microgravity the soot stayed in the flame longer and formed clusters, some escaping outward. The soot then faded as the flame cooled radiatively before extinction. Inverse flames formed their soot just outside the flame, in the hot fuel-rich chamber gas. Imaging at the end of each day showed no soot build-up on the chamber windows. *(result, medium)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p52): *Due to microgravity, the soot remains in the flame longer and forms clusters.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p61): *Therefore, in this test, the soot forms just outside the flame.*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p16): *However, the end-of-day imaging did not appear to change over time, suggesting that the soot was not an issue for the chamber windows.*
12. Burners and their supports heated strongly. Peak burner temperatures reached 532 °C (805 K) in normal flames (21088 F1, ethane, about 38% O2) and 651.5 °C (925 K) in inverse flames (21242 A1, 85% O2 into about 43% propane at 0.55 bar). 30 of 284 tests with a reading exceeded 450 °C (723 K), the stated termination limit. Longer hot-flame burns heated the burners further, hot burners enabled cool flames, while the cold support tube locally quenched flames. *(result, medium)*
   - Table `tests`: peak_temp_c maxima by config; count of rows with peak_temp_c > 450 (16 normal, 14 inverse) out of 133 + 151 non-null readings.
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p23): *The results identify the importance of burner temperature on the behavior of these CDFs.*
13. Lowering the igniter energy (for example 2-2.9 V for 10-20 s instead of the standard 3 V preheat and 3.75-4 V ignition) did not give confirmed direct ignition of cool flames. These attempts either failed to ignite or produced hot flames. All 15 confirmed cool flames followed hot-flame extinction. *(null_result, medium)*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p15): *Tests intended to directly ignite cool flames sometimes unintentionally resulted in hot flames.*
   - `PSI-159_Raw Data_21102 flow traces etc.pdf` (p22): *Test 21102C6 (test 8 of 16) – no apparent ignition*
   - `PSI-159_Reports_FinalRpt_ACME.CFI-G.pdf` (p34): *Based on the output from the photomultipliers, radiometers, and intensified camera images we do not believe any self-sustained cool flames were created.*

## Fire-safety relevance

CFI-G is a fundamental combustion study, not a materials or fire-response test, and its numbers are not flammability limits for spacecraft materials. Three results bear on fire safety. (1) Detection: after a hot gaseous flame extinguished radiatively, a nearly invisible cool flame could persist for as long as fuel kept flowing. It was detected only by an intensified formaldehyde-filtered camera and radiometers, and not by the operations video. The team did not notice the first cool flames until days later. Visible-light or flame-flicker detection would miss such a reacting zone. (2) Re-ignition: a hot platinum surface (a type-B thermocouple) in the rich mixture left after extinction repeatedly re-ignited the hot flame. Catalytic or hot surfaces near a leak that has 'gone out' can therefore restore a fire. A hot burner surface (above 515 K) was likewise needed to sustain the cool flame. (3) Prevention: oxygen enrichment strongly increased ignition success and burn duration. Normal flames in 21% O2 all self-extinguished within 20 s, while at 40% O2 a third of the flames survived until the flow was cut. Pressure had the opposite effect for inverse flames: oxygen-rich jets into fuel-laden gas self-extinguished at 2-3 atm but not at 0.5 atm. These trends concern small (mg/s) laminar gas flames on a 6 mm burner in a closed, quiescent 83 L chamber. They transfer qualitatively at most.

### Habitat conditions

Be precise about where the oxygen was. The 85% O2, the highest oxygen concentration in PSI, was only the oxidiser stream issuing from the burner in inverse-flame tests. During those tests the chamber atmosphere was fuel (about 6-43%) in nitrogen, with no oxygen. ACME limited the chamber atmosphere to 40% O2. In normal-flame tests the ambient was 18-40% O2 at 0.5-3 atm (about 51-304 kPa), with about 40% O2 tested at 0.5 atm (7.35 psia, about 51 kPa), 1 atm and 2 atm. That overlaps and exceeds the intermediate lunar-habitat atmosphere (30% O2 or more at 70.3 kPa or less). It brackets the Earth sea-level reference (20.9% O2, 101.3 kPa). The spacesuit condition (100% O2 at 29.6 kPa) was not tested: no ambient above 40% O2 and none below about 50 kPa. The inverse 85% O2 stream is better compared to an oxygen leak or jet into a fuel-rich region than to a cabin atmosphere. Cool flames were found only at about 39-40% O2 and 2 bar, a combination of oxygen fraction and total pressure higher than any planned habitat atmosphere. Flows were burner-driven only (no ventilation), with velocities of order cm/s at the flame.

### Earth benefits

Cool-flame (low-temperature) chemistry governs autoignition, knock, and octane and cetane behaviour in engines. Most engine design models neglect it. The steady, spherical, one-dimensional ISS cool flames give clean validation targets (flame radii, burner and ambient boundary conditions, durations) for cool-flame kinetic mechanisms. The investigators argue this could help engines move toward ultra-lean, low-temperature combustion, with efficiencies they put at up to 60% against 38% or less today. The soot observations in normal and inverse flames also bear on soot control in oxygen-enriched combustion.

## Limitations

- Cool flames were obtained under one narrow condition set only (30% n-butane, about 40% O2, 2 bar, 0.75-1.5 mg/s): 15 flames in 7 tests on 2 days. The first five were cut short because they were not detected in real time, and the later ones were disturbed by catalytic reignition on the type-B thermocouple. So no cool-flame extinction limit (in flow, O2 or pressure) was mapped.
- The burner was not spherically symmetric: more flow leaked through the sintered joint at the supply tube, and the tube itself was a heat sink. At high flows the flames became offset, ellipsoidal or parabolic and quenched locally near the tube. One-dimensional models therefore only approximate these flames.
- Mass flow controllers performed poorly below about 10% of full scale, so low-flow set points may differ from actual flows. The chamber was a closed volume, so O2 or fuel fraction fell and pressure rose through each day. Tabulated chamber compositions are estimates from flow balances, not gas-chromatograph measurements.
- 'Flow-terminated' does not mean the flame was stable. Flow was cut by scripted timeouts (often 66 s in inverse tests) or when the burner reached its temperature limit. Self-extinction fractions therefore depend on the chosen timeouts and are not burning-limit statistics.
- Data losses: an IPSU-G hard-drive failure and igniter failure on 30 Aug 2021 lost nearly all imagery of that propane inverse day, which could not be repeated. The HiBMs camera was unavailable for most of round 1. Some image data were deliberately deleted on orbit to meet daily downlink limits. Acceleration effects were not evaluated with SAMS data.
- Results are for small laminar gas flames (a 6.35 mm burner, mg/s flows) in a quiescent nitrogen-diluted chamber. They are not material flammability data and cannot be applied directly to cabin fires, ventilated spaces or condensed fuels.

## Data in PSI

PSI-159 holds 3,756 files, about 2.09 TB. Nearly all of the volume is raw imagery that has not been downloaded here: 986 zip archives (about 2.0 TB) of intensified-camera TIFFs, DataCam HOBJ images, converted images and HiBMs images, plus 336 ground-recorded analog video files (.ts, 81.7 GB). The most usable data are already local: 338 per-test 125 Hz CSV files (1.46 GB) of raw channel voltages, with matching mfcSetpoints CSVs. Channels include MFC flows, PMTs, thermocouples (rakes, 200 mm, burner), dual-gain radiometers and pressure transducers. Calibrations are given in the ACME Software Interface Design Document, which is not in PSI. Also local are about 1,000 small text files per test: as-run script parameters, timestamped test-point timelines, image-downlink comments and camera configurations. There are 22 daily operation logs, 24 'flow traces' PDFs with per-test narrative and parameters, and the two experimental-table CSVs, which give one row per test with conditions and outcomes. The CSVs feed tests.csv. Daily 'test sheets', 'test parameter notes' and 'daily test point log' PDFs are scans with no text. The final report (2022) and the ACME Engineering Implementation report are the only analysis documents. Acceleration (SAMS) data are not archived in PSI.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | per-test non-imaging data at 125 Hz (data.csv) and MFC set-point logs | .csv | 678 | 1.47 GB | yes |
| Raw Data | image archives: CFI intensified camera (TIFF), ACME DataCam (HOBJ), converted images, HiBMs | .zip | 986 | 2e+03 GB | no |
| Raw Data | ground-recorded analog (ops) video per test | .ts .mp4 | 337 | 81.7 GB | no |
| Raw Data | per-test text notes: as-run script parameters, test-point timelines (_TP), image-downlink comments, camera configuration; IPSU image metadata (.mdipsug); daily ACME logs | .txt .mdipsug .log | 1654 | 155 MB | yes |
| Raw Data | daily PDFs: flow-trace narratives (text, 24 files) and scanned test sheets, test parameter notes and daily test-point logs (no text layer); chamber-calculator workbook | .pdf .xlsx | 92 | 137 MB | yes |
| Experimental table | Normal Flames (179 tests) and Inverse Flames (154 tests) summary tables | .csv | 2 | 100 kB | yes |
| Reports | ACME/CFI-G Final Report (21 Nov 2022), including 30-day reports, timeline, cool-flame table | .pdf | 1 | 3.9 MB | yes |
| Engineering Documents | ACME Engineering Implementation report (19 May 2022) | .pdf | 1 | 7.5 MB | yes |

Rows in the unified `tests` table: 333

## Related investigations

- [PSI-10](PSI-10-acme-flame-design.md): shared hardware
- [PSI-23](PSI-23-acme-s-flame.md): shared hardware
- [PSI-20](PSI-20-acme-bre.md): shared hardware
- [PSI-21](PSI-21-acme-cld-flame.md): shared hardware
- [PSI-22](PSI-22-acme-e-field-flames.md): shared hardware
- [PSI-39](PSI-39-cfi.md): precursor
- [PSI-69](PSI-69-flex.md): precursor
- [PSI-68](PSI-68-flex-2.md): precursor

## Open questions

- Use the 338 local 125 Hz data files (radiometer, PMT, burner and rake thermocouples) to systematically screen all 189 radiatively extinguished flames for a non-zero radiometer plateau after extinction. That would test whether further, unreported cool flames occurred, for example in other butane tests at 2 atm.
- Build a hot-flame radiative-extinction map: burn time and self-extinction versus Z_st, T_ad, pressure and limiting-reactant flow for normal and inverse flames. The experimental-table CSVs already give Z_st, T_ad and outcomes per test.
- Quantify the inverse-flame pressure effect (0/26 self-extinguished at 0.55 bar versus 59/68 at 2.2-3.3 bar) using radiometer heat flux and burner temperature histories, separating radiative from conductive (burner) losses.
- Extract hot-flame radius versus time from the intensified-camera and DataCam archives (about 2 TB, not downloaded) for comparison with the Spalding-type model of Kim et al. across all fuels and both configurations.
- Compare CFI-G inverse ethane flames with the inverse ethylene flames of ACME Flame Design (PSI-10), which used the same burner and 85% O2 oxidiser, for soot-formation boundaries.
- Convert raw channel voltages to engineering units. That needs the ACME Software Interface Design Document (ACME-DOC-010), which is not in PSI.

## Dashboard ideas

- **outcome map by configuration** (`config`, `x_o2 (ambient for normal, burner stream for inverse)`, `pressure_kpa`, `fuel`, `ignited`, `extinction_mode`, `burn_time_s`): Shows self-extinguished vs flow-terminated fractions by O2 and pressure. The x_o2 axis must be labelled differently for normal and inverse flames so that 85% is not read as an ambient atmosphere.
- **cool-flame window** (`fuel`, `fuel_fraction`, `x_o2`, `pressure_kpa`, `mHC_mg_s`, `peak_temp_c`, `cool_flame`): Places the 15 cool flames (30% n-butane, about 0.39 O2, 2 bar, 0.75-1.5 mg/s, burner above 515 K) among all 333 tests.
- **burn time vs adiabatic flame temperature** (`t_ad_k`, `Zst`, `burn_time_s`, `extinction_mode`, `config`): Relates radiative extinction to flame strength and stoichiometry using columns already in tests.csv.
- **habitat comparison strip** (`x_o2`, `pressure_kpa`, `config`): Shows the ambient O2-pressure points of normal flames against Earth, lunar-habitat and spacesuit references. Inverse 85% O2 tests are flagged as burner-stream O2 with an oxygen-free chamber.

## Gaps and data-quality notes

- The PSI record has no start or end dates. Test dates (29 Mar - 18 Oct 2021) come from the final report and the tables.
- The PSI record's hypothesis and objective still list n-pentane. Ethane replaced it because of n-pentane's low vapour pressure (final report p6, p17).
- Only two publications are listed in the PSI record. The second (Waddell et al., Combust. Flame 254 (2023) 112852) is a normal-gravity n-heptane pool / stagnation-flow study with no ISS data. The ISS results are in Kim et al., Proc. Combust. Inst. 39 (2023) 1647-1656 (doi 10.1016/j.proci.2022.07.015). Its accepted manuscript at par.nsf.gov was used for quotes. Other works found: M. Kim, MS thesis, U. Maryland 2022 (doi 10.13016/n8ln-uehb), and NASA NTRS 20210022542 (Stocker, JASMAC-33 ACME overview, which reports 'Observed the first spherical, quasi-steady, burner-supported cool flames!'). The report also lists conference papers (Eastern States 2022, Central States 2022) that were not retrieved. No NTRS record specific to CFI-G was found. No later journal paper on the CFI-G inverse flames or their soot was found. The ScienceDirect and ADS abstract pages were not fetched (ADS returned HTTP 405).
- Kim et al. cite a version of their cool-flame model for inverse flames in their ref. [32]. It was not retrieved.
- Raw-data PDFs 'test sheets', 'test parameter notes' and 'daily test point log' (21 of each, plus misspelled variants) have no text layer and were not read, as instructed.
- Data check: the two flow-trace PDFs for 21222 ('flow traces etc.pdf' and 'flow traces etc-1.pdf') appear to be duplicates.
- Data check: in tests.csv, x_o2 and fuel_fraction mean different things by config. For normal flames they are the ambient O2 and the burner fuel mole fraction; for inverse flames, the burner-stream O2 and the ambient fuel mole fraction. Any cross-config plot must keep these apart.
- Data check: inverse-table pressures are 0.495, 0.552, 1.10-1.103, 2.207 and 3.310 bar. Fill pressures were nominally 7.35/14.7/29.4/44.1 psia (0.507-3.04 bar), and Kim et al. give 0.46-3.04 bar. The table values are about 9% higher at each level, and tests.csv inherits them (pressure_kpa up to 331).
- Data check: tests.csv 'ignited' is null for 8 inverse rows whose 'Hot ignition' is 'flash' (momentary flame, about 1 s, marked SE). The Inverse Flames CSV has 861 empty trailing rows. Its 'Color' column holds 'limit' in 29 rows, apparently flagging the burner temperature limit rather than flame colour. 'Peak burner temp (K)' contains '#VALUE!' and 'Tad'/'Zst' contain '#DIV/0!' in some rows.
- Data check: counts differ between sources. The report has 280 hot flames, 189 radiatively extinguished; the tables have 263 ignited plus 8 flashes, 183 SE and 89 FT. The difference is presumably reignitions within one test (for example 21291A1 and C1, each with several hot flames, recorded as one FT row).
- Data check: report Table 3 lists '21174D13' while the CSV has '21174 D1'. Report Appendix D says the 18 Oct 2021 (GMT 291) tests used 30% C3H8, but Table 2, the 21291 flow-trace notes and the experimental table all say 30% n-butane.
- Data check: 30 tests show peak burner temperatures above 450 °C (723 K), the stated termination limit (max 651.5 °C in 21242 A1). This is presumably overshoot after flow cut-off or lag, but it is not explained in the documents.
- The Engineering Implementation report (dated 19 May 2022) still states inverse-flame tests 'have yet to be conducted'. This is stale text carried over from an earlier version.
- Raw 125 Hz data files are in instrument voltages. The calibration document (ACME-DOC-010 Rev. D) is not in PSI. SAMS acceleration data are not archived with the experiment.
- The final report and engineering report contain a NASA staff phone number and e-mail; these were not copied. No credentials and no text addressed to an AI were found in the sampled raw notes (as-run parameter files, TP timelines, image comments, flow-trace PDFs).
