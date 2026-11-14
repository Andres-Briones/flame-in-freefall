# PSI-101: SAME-R (Smoke Aerosol Measurement Experiment - Reflight (also called SAME-2 in the papers))

On the ISS, small pieces of five common spacecraft materials were overheated (without burning) to make smoke, and instruments measured how big the smoke particles were and whether the Shuttle and ISS smoke detectors would have noticed them.

Investigators: David L. Urban (PI; NASA GRC); Zeng-guang Yuan (Co-I; NASA GRC in the PSI record, National Center for Space Exploration Research in the final report); George W. Mulholland (Co-I; University of Maryland, formerly NIST); Thomas Cleary (Co-I; NIST); Jiann C. Yang (Co-I; NIST); Claire Fortenberry (Project Scientist in the PSI record; NASA GRC); Gary A. Ruff (Project Scientist in the SAME documents; NASA GRC); Marit E. Meyer (NASA GRC; lead author of the 2013 and 2018 papers)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS), Expedition 24 |
| Facility | Microgravity Science Glovebox (MSG) |
| Dates | 2010-07-01 to 2010-09-30 |
| Fuels and samples | Kapton; Teflon; Silicone rubber; Cotton lampwick; Pyrell |
| Varied | sample material: Kapton, Teflon, silicone rubber, cotton lampwick, Pyrell<br>air velocity past the sample during heating: 0, 1, 2, 8.0-8.1 (baseline 8.1); 11 zero-flow runs, 3 at 1 cm/s, 5 at 2 cm/s (plus 1 unlisted 2 cm/s Kapton run 112) cm/s<br>heating-wire resistance ratio Rt/R0 (sets sample temperature): 1.22-1.48 overall; material-specific (Pyrell 1.22-1.23, lampwick 1.245-1.28, silicone 1.304-1.36, Kapton 1.38-1.48, Teflon 1.445-1.452) dimensionless<br>derived sample (wire) temperature: Pyrell 225-245, lampwick 255-299, silicone 325-392, Kapton 417-583, Teflon 513-538 degC<br>smoke aging (net time from generation to measurement): about 21-62 s unaged; 218-1923 s aged; 720 s single-shot aging in 5 runs s<br>heating duration: 60 (one Kapton run 120) s |
| Number of tests | 67 |
| Fire-safety pillars | detection |

## Question

Spacecraft smoke detectors were designed from terrestrial smoke data, but smoke in orbit may differ. Without buoyancy, smoke stays longer near its source at high concentration, so pyrolysis droplets could grow larger by condensation and coagulation. Spacecraft materials also differ from standard test fuels. The SAME hypothesis was that microgravity liquid smoke would have substantially larger droplets, with fewer particles for the same mass, and that this could stop some detectors from alarming. SAME-R reflew the 2007 SAME experiment to (1) quantify the sizes smoke particles reach in low gravity and relate them to generation temperature, air flow and aging (transport) time; (2) obtain usable electron-microscope (TEM) samples, since all SAME-1 grids came back contaminated; (3) evaluate the existing Shuttle and ISS smoke detectors against these smokes; and (4) demonstrate a prototype two-moment smoke sensor (MPASS). The goal was a database for designing future spacecraft fire detectors and alarm set points.

## Summary

SAME-R, the 2010 reflight of the Smoke Aerosol Measurement Experiment, heated small cylindrical samples of Kapton, Teflon, silicone rubber, cotton lampwick and Pyrell foam below ignition in the ISS Microgravity Science Glovebox. Air flow past the sample was varied from 8.1 cm/s down to zero, sample temperature was set per material, and smoke was aged in a 6 L chamber for up to about 1900 s. Three instruments measured the zeroth, first and third moments of the particle size distribution; a two-angle prototype sensor, Shuttle (ionization) and ISS (light-scattering) detectors and electron-microscope grids recorded the same smoke. Unaged baseline smoke had geometric mean diameters of 0.05-0.18 um and diameters of average mass of 0.11-0.47 um; aging and low flow enlarged the particles, and zero flow gave much larger particles. Kapton and Teflon smoke was smallest and often fell below the ISS detector's alarm level, while silicone, lampwick and Pyrell saturated it. At 8.1 cm/s, flight sizes matched ground tests. The authors conclude that a single-moment detector cannot cover all smokes without nuisance alarms, and that multi-moment detection is promising.

## Physics

The target is the earliest stage of a spacecraft fire: an overheated material pyrolysing before it ignites, not flaming soot. Heated polymer releases vapour; as the vapour cools, it becomes supersaturated and nucleates particles, which grow by condensation within about a millisecond. Over much longer times (up to about $10^3$ s) particles collide by Brownian motion and coagulate. Liquid particles (lampwick, Kapton, silicone) merge into larger droplets; solid ones (Teflon, Pyrell) stick into fractal-like agglomerates. Coagulation preferentially removes the smallest, most mobile particles, so the count mean diameter grows faster than the diameter of average mass and the size distribution narrows towards a self-preserving geometric standard deviation of about 1.32. In 1 g, a hot plume rises and dilutes the smoke. In microgravity with no forced flow, transport is only by diffusion and thermal expansion (about 4 cm in 60 s), so the smoke stays concentrated, ages faster and forms larger particles. The experiment's 'moment method' measures moments $M_i=\int D^i f_N(D)\,dD$ of the number distribution: $M_0$ (number concentration, condensation particle counter), $M_1$ (roughly the ionization chamber signal) and $M_3$ (roughly the light-scattering mass signal for 0.2-2 um particles). Then $\bar D = M_1/M_0$ and $D_{avm} = (M_3/M_0)^{1/3}$ need no distribution assumption. For a lognormal distribution, $D_p = D_g \exp(p\ln^2\sigma_g)$ with $p=0.5$ and $1.5$ for these two diameters, so $D_g$ and $\sigma_g$ follow from their ratio. Detector physics matters: an ionization detector responds roughly to $M_1$ and favours numerous small particles, while a forward-scattering detector responds strongly to particles near or above its near-IR wavelength (about 1 um) and weakly to particles of about 0.1 um.

$$
M_i = \int_0^\infty D^i f_N(D)\,dD, \quad i = 0, 1, 3
$$

Moments of the number size distribution $f_N(D)$ (particles per cm$^3$ per unit diameter). $M_0$ is the number concentration (cm$^{-3}$), measured by the condensation particle counter. $M_1$ is the 'diameter concentration' (um cm$^{-3}$), approximately what an ionization chamber responds to. $M_3$ is proportional to volume or mass concentration and approximately what a light-scattering photometer responds to for particles of about 0.2-2 um. Valid for any distribution shape.

`PSI-101_Reports_SAME-R_Final Report.pdf` (p74): *The moments of interest consist of the number concentration, M 0, the first moment M 1, and the volume or mass concentration moment, M 3 and are defined as*
`PSI-101_Reports_SAME-R_Final Report.pdf` (p74): *is approximately proportional to the ionization detector moment (signal).*

$$
\bar D = \frac{M_1}{M_0}, \qquad D_{avm} = \left(\frac{M_3}{M_0}\right)^{1/3}
$$

Count (arithmetic) mean diameter $\bar D$ ($D_{0.5}$) and diameter of average mass $D_{avm}$ ($D_{1.5}$), both in um, from the three measured moments. They need no assumption about the distribution shape and are the most robust SAME-R size statistics. $\bar D < D_{avm}$ for any polydisperse aerosol.

`PSI-101_Reports_SAME-R_Final Report.pdf` (p74): *These calculations do not depend on the assumption of log-normal behavior.*

$$
D_p = D_g \exp\left(p \ln^2 \sigma_g\right), \quad p = 0.5, 1.5 \;\Rightarrow\; \ln \sigma_g = \sqrt{\ln\left(D_{1.5}/D_{0.5}\right)}
$$

Hatch-Choate relation for a lognormal number distribution with geometric mean diameter $D_g$ (um) and geometric standard deviation $\sigma_g$ (dimensionless, > 1). $p = 0.5$ gives the count mean diameter and $p = 1.5$ the diameter of average mass. Inverting it gives $\sigma_g$ from the ratio of the two measured diameters and then $D_g$. Valid only if the smoke is close to lognormal: confirmed for Kapton and lampwick, not for silicone, and only approximate for aggregate smokes (Teflon, Pyrell).

Textbook background
<https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *For the lognormal distribution, one finds that the various diameter definitions given above are related to the geometric mean diameter, Dg, via the equation.*
<https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *where p is a parameter which refers to the specific mean diameter of interest, i.e. D0.5 for the count mean diameter, or D1.5 for the diameter of average mass.*

$$
M_{p,r}(D_l, D_u) = \tfrac{1}{2}\left[\operatorname{erf}(\eta_u) - \operatorname{erf}(\eta_l)\right], \quad \eta = \frac{\ln(D/d_g)}{\sqrt{2}\ln\sigma_g} - \frac{p\ln\sigma_g}{\sqrt{2}}
$$

Fraction of the total $p$-th moment of a lognormal distribution ($d_g$, $\sigma_g$) that an instrument sees if it detects only diameters between $D_l$ and $D_u$. Derived in the SAME-R final report to quantify signal lost to instrument size limits. Example: an SMPS limited to 1000 nm captures only about 40% of the volume ($p = 3$) distribution of high-temperature silicone smoke. Assumes a lognormal distribution.

`PSI-101_Reports_SAME-R_Final Report.pdf` (p30): *We can use eqs. (12) and (13) to find how much an instrument can see if its lower and upper detection limit are Dl and Du.*
`PSI-101_Reports_SAME-R_Final Report.pdf` (p29): *Thus, the total p moment of the lognormal distribution is*

$$
\frac{dN}{dt} = -\tfrac{1}{2} K N^2 \;\Rightarrow\; N(t) = \frac{N_0}{1 + \tfrac{1}{2} K N_0 t}
$$

Brownian coagulation of an aerosol with number concentration $N$ (cm$^{-3}$) and an effective coagulation coefficient $K$ (cm$^3$ s$^{-1}$, of order $10^{-9}$ for 0.1-1 um particles in air). Explains why concentrated smoke (a few $10^6$ cm$^{-3}$) aged in the 6 L chamber lost a factor of 1.7-2.7 in number over about 800 s while $D_{avm}$ grew. It also explains why concentrations below about $10^6$ cm$^{-3}$ (the drum tests, < $2\times10^4$ cm$^{-3}$) age negligibly. The monodisperse constant-K form is approximate for polydisperse smoke.

Textbook background
`PSI-101_Presentations_SAME-R_Particle Morphology and Size Results from the Smoke Aerosol Measurement Experiment-2.pptx` (slide 41): *For spacecraft materials, number counts decreased by a factor of 1.7 to 2.7 over 800 seconds.*
`PSI-101_Reports_SAME-R_Final Report.pdf` (p10): *which is below the rule-of-thumb threshold concentration of 106 particles/cm3.*

$$
\ell \sim \sqrt{\mathcal{D} t} \approx 4\,\text{cm (60 s)}, \quad \frac{C_{0\,flow}}{C_{8\,cm/s}} \sim \frac{V_{chamber}}{\ell^3} \approx \frac{6000}{64} \sim 50\text{-}100
$$

Investigators' estimate for zero flow in microgravity. Pyrolysis gases spread only by diffusion (effective diffusivity $\mathcal{D}$, cm$^2$/s) over a length $\ell$ in time $t$. In 60 s they fill about 64 cm$^3$ instead of being diluted into the 6000 cm$^3$ aging chamber, so the initial smoke concentration is of order 50 times higher (their figure), and coagulation is correspondingly faster. This is an order-of-magnitude scaling. The 2018 paper instead estimates the vapour concentration as about 8 times higher, from a thermal-expansion flow of 0.5-1.5 cm/s.

`PSI-101_Reports_SAME-R_Final Report.pdf` (p8): *If the same number of particles is generated as for the flow case, the initial concentration will be on the order of 50 times higher for the zero-flow case.*
<https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The vapor concentration is inversely proportional to the flow so the nominal vapor concentration for the zero-flow case is about eight times higher than for the standard 8.1 cm/s forced flow condition.*

## Method

### Apparatus

The SAME hardware was installed in the MSG. A sample carousel (six positions) indexed each sample into the smoke generation duct. A stainless-steel wire coiled around the sample both heated it and sensed its temperature through its resistance. A feedback loop held the wire at a set resistance ratio Rt/R0 for about 60 s. A rising piston in a 6 L (6000 cm3) aging chamber drew air past the sample, setting the duct velocity, and captured the smoke. Some smoke was pushed almost immediately into a low-volume diagnostics duct ('unaged'); the rest was held for a set time (secondary aging) and then measured. The diagnostics duct held: the ISS smoke detector (2-pass near-IR laser-diode forward scattering at 30 degrees, minimum reported sensitivity 0.3 um, planned alarm level 2 V); the Space Shuttle (STS) detector (dual-chamber ionization with a pump and inertial separator that rejects particles larger than 1-2 um); a modified TSI P-Trak condensation particle counter for $M_0$, fed through a dynamic nitrogen diluter; a First Alert residential ionization chamber (americium-241) calibrated for $M_1$; and a TSI DustTrak 90-degree photometer for $M_3$ (calibrated per material against a tapered-element oscillating microbalance). For SAME-R, one of the two DustTrak enclosures was replaced by the GRC-built MPASS, which detects scattered light at two angles to estimate the 2nd and 3rd moments. Thermal precipitators (a heated wire above a TEM grid, so particles deposit by thermophoresis) sampled smoke before and after aging for post-flight TEM. The six rebuilt precipitators held 12 grids each.

### Fuels and samples

- Kapton (polyimide) - wire-insulation material (solid, small cylindrical sample (about 0.5 cm diameter x 1.3 cm) wrapped with a heating wire)
- Teflon (PTFE) (solid, small wire-wrapped cylinder)
- Silicone rubber (solid, small wire-wrapped cylinder)
- Cotton lampwick (cellulose) (solid, small wire-wrapped cylinder)
- Pyrell (Foamex intumescent fire-retardant polyurethane foam; new in SAME-R, replacing dibutyl phthalate) (solid, small wire-wrapped cylinder)

### Procedure

Six carousels were preloaded (one Pyrell sample in carousel 5 was found unusable, probably shaken loose at launch). Thirty loose samples (6 Pyrell, 6 silicone, 9 Kapton, 5 lampwick, 4 Teflon) were later loaded into carousel 4 in groups, logged as carousels 7(4)-11(4). For each run, the operator set the wire resistance ratio Rt/R0 (material-specific: about 1.22-1.23 for Pyrell, 1.245-1.28 for lampwick, 1.30-1.36 for silicone, 1.38-1.48 for Kapton, 1.445-1.452 for Teflon). The sample was heated for 60 s (one Kapton run 120 s) while the piston drew air through the duct at 8.1 cm/s (baseline), 2 or 1 cm/s, or zero. Zero flow was not in the original design; it was obtained by changing the valve sequence. The baseline temperature was chosen to give 1-2 mg of mass loss in 60 s. Smoke was usually given 11 s of primary aging and 8 s of mixing, then half was measured unaged (net aging about 21-62 s). The rest was aged in the chamber and measured at about 218-1923 s ('a' runs in the table). Five 'aged STS det' runs held all the smoke for 720 s before measurement. The STS detector was used only in selected runs because its pump drew too much flow to allow aging. Flights ran from 16 July to 9 September 2010 in seven periods, with the science team at GRC's Telescience Center. Samples were weighed before and after flight for mass loss. Afterwards, three ground campaigns ran: (a) flow tests to correct the instruments' dilution ratios; (b) 1 g TEM tests under flight conditions; and (c) 'smoke-in-drums' tests in which smoke from the identical ground SAME unit was diluted into 55-gallon drums and measured with a TSI 3936 scanning mobility particle sizer (SMPS) to test the lognormal assumption. Actual wire (sample) temperatures were later derived from the logged resistances with a two-section wire heat-balance model.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| sample material | Kapton, Teflon, silicone rubber, cotton lampwick, Pyrell |  |
| air velocity past the sample during heating | 0, 1, 2, 8.0-8.1 (baseline 8.1); 11 zero-flow runs, 3 at 1 cm/s, 5 at 2 cm/s (plus 1 unlisted 2 cm/s Kapton run 112) | cm/s |
| heating-wire resistance ratio Rt/R0 (sets sample temperature) | 1.22-1.48 overall; material-specific (Pyrell 1.22-1.23, lampwick 1.245-1.28, silicone 1.304-1.36, Kapton 1.38-1.48, Teflon 1.445-1.452) | dimensionless |
| derived sample (wire) temperature | Pyrell 225-245, lampwick 255-299, silicone 325-392, Kapton 417-583, Teflon 513-538 | degC |
| smoke aging (net time from generation to measurement) | about 21-62 s unaged; 218-1923 s aged; 720 s single-shot aging in 5 runs | s |
| heating duration | 60 (one Kapton run 120) | s |

Held constant:

- gravity level: ISS microgravity (ground units used for 1 g comparisons)
- gas environment: MSG work-volume air at ambient pressure; O2 and pressure not reported in the documents read
- aging chamber volume: 6 L
- combustion mode: pre-ignition pyrolysis (no flaming)

Number of tests: 67

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| particle number concentration (zeroth moment M0) | TSI P-Trak condensation particle counter, modified for microgravity, behind a dynamic N2 diluter; size-specific calibrations (100, 600, 1200 nm DOP) | direct |
| first moment M1 (diameter concentration) | First Alert residential ionization chamber, calibrated against a TSI Electrical Aerosol Detector | direct |
| mass concentration / third moment M3 | TSI DustTrak 90-degree photometer (1 um or 10 um impactor inlet), calibrated per material against a TEOM | direct |
| count mean diameter M1/M0, diameter of average mass (M3/M0)^1/3, geometric mean diameter and geometric standard deviation (lognormal assumption) | moment method computed from the three instruments | derived |
| two approximate moments (2nd and 3rd) from scattering at two angles | MPASS (Multi-Parameter Aerosol Scattering Sensor), GRC prototype | direct |
| ISS smoke detector scatter and obscuration voltages | ISS flight-design forward-scattering smoke detector | direct |
| Space Shuttle smoke detector voltage and offset | STS ionization smoke detector (selected runs) | direct |
| particle morphology and TEM size distributions | thermal precipitator onto TEM grids; Philips CM20 TEM at 200 kV; ImageJ analysis | derived |
| sample mass loss | pre- and post-flight weighing | direct |
| full particle size distribution (ground only) | TSI 3936 SMPS sampling diluted smoke from 55-gallon drums | direct |

## Findings

1. Unaged baseline smoke at 8 cm/s was sub-micrometre for every material. Kapton had geometric mean diameter Dg = 0.047 um, count mean 0.062 um and diameter of average mass 0.106 um. Teflon had Dg 0.093 um and D_avm 0.173 um, lampwick 0.103 and 0.271 um, silicone 0.152 and 0.468 um, and Pyrell 0.177 and 0.377 um. The geometric standard deviation was 2.03-2.38. Typical runs had a few million particles per cm3 and 2-15 mg/m3. (These are the final-report values; the appended 2012 paper gives slightly different numbers, e.g. Kapton Dg 0.042 um.) *(result, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p4): *Kapton Unaged 0.047 0.062 0.106 2.072 Aged 720 s 0.102 0.121 0.169 1.790*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p5): *Lampwick Unaged 0.103 0.142 0.271 2.232 Aged 720 s 0.269 0.308 0.401 1.673 Silicone Unaged 0.152 0.221 0.468 2.382 Aged 720 s 0.320 0.400 0.628 1.956 Teflon Unaged 0.093 0.111 0.173 2.081 Aged 720 s 0.080 0.115 0.237 2.342 Pyrell Unaged 0.177 0.227 0.377 2.032 Aged 720 s 0.348 0.400 0.529 1.697*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p4): *For typical runs, the partic le concentrations were a few million particles / cc and the mass concentrations were 2 to 15 mg/m 3 however there were runs with fewer particles.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p78): *Kapton Unaged 0.042 0.056 0.101 2.154 Aged 720 s 0.089 0.109 0.161 1.872*
2. Aging the smoke for 720 s in the chamber made the particles larger and the distribution narrower. D_avm rose from 0.106 to 0.169 um (Kapton), 0.271 to 0.401 um (lampwick), 0.468 to 0.628 um (silicone) and 0.377 to 0.529 um (Pyrell), and sigma_g fell to 1.67-1.96. Teflon was the exception: Dg did not grow (0.093 to 0.080 um) and sigma_g widened to 2.34. Number counts fell by a factor of 1.7-2.7 over about 800 s. This agreed with coagulation theory within about 20% for number and 4% for D_avm, but sigma_g fell more than twice as much as predicted. *(trend, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p4): *Kapton Unaged 0.047 0.062 0.106 2.072 Aged 720 s 0.102 0.121 0.169 1.790*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p5): *Lampwick Unaged 0.103 0.142 0.271 2.232 Aged 720 s 0.269 0.308 0.401 1.673 Silicone Unaged 0.152 0.221 0.468 2.382 Aged 720 s 0.320 0.400 0.628 1.956 Teflon Unaged 0.093 0.111 0.173 2.081 Aged 720 s 0.080 0.115 0.237 2.342 Pyrell Unaged 0.177 0.227 0.377 2.032 Aged 720 s 0.348 0.400 0.529 1.697*
   - `PSI-101_Presentations_SAME-R_Particle Morphology and Size Results from the Smoke Aerosol Measurement Experiment-2.pptx` (slide 41): *For spacecraft materials, number counts decreased by a factor of 1.7 to 2.7 over 800 seconds. The measured and predicted number decreases agree within about 20 %. The best agreement between experiment and prediction is Davm - agree within 4 %.*
   - `PSI-101_Presentations_SAME-R_Particle Morphology and Size Results from the Smoke Aerosol Measurement Experiment-2.pptx` (slide 41): *The decrease in the geometric standard deviation is typically more than a factor of two greater than the predicted change.*
3. Lower air flow past the overheated sample produced larger particles for Kapton, Teflon and lampwick (runs from 8.1 down to 2 cm/s). The authors infer that smoke trapped in a poorly ventilated avionics enclosure will be substantially larger than smoke released into ventilated cabin air. The 2018 analysis puts the possible increase in D_avm at low flow at up to a factor of 2.5. *(trend, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p5): *These figures show a strong trend of increased particle size at low flow ra tes. This indicates that sm oke trapped in an avionics enclosure can be expected to be substantially larger than smoke released in ventilated areas.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The potential error of this analogy can be estimated using Figure 6 which suggests that lower flow rates could increase the diameter of average mass by as much as a factor of 2.5.*
4. In the 11 zero-flow runs (smoke moved only by diffusion and thermal expansion, at about 0.5-1.5 cm/s seen on video), D_avm was larger than at 8.1 cm/s. The sources quantify this differently: 30-40% larger for all materials (final report text); 2-3 times larger (conclusions of the appended 2012 paper); and on average a factor of 1.7, ranging from 1.3 for Teflon to 2.8 for Kapton (2018 journal paper). Example: silicone run 104 at 0 cm/s had D_avm 1.22 um vs 0.42-0.47 um in the 8.1 cm/s baseline runs. *(result, medium)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p9): *It is found for all of the materials the diameter of average mass is 30 % to 40 % larger for the zero-flow tests compared to the flow tests.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p84): *The zero flow conditions produced smoke particles that were 2 to 3 times larger than those produced at the nominal 8 cm/s flow rate.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The diameter of average mass is a factor of 1.7 larger for the zero-flow compared to the standard flow condition. This is an average for all the materials, which vary from as low as 1.3 for Teflon to 2.8 for Kapton.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The thermal expansion induced smoke-flow observed with a video camera ranged from 0.5 cm/s to 1.5 cm/s with the higher velocity corresponding to Kapton and Teflon with the highest pyrolysis temperatures.*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 104 (Flight=2): *No flow run w/ aging; Inlet Velocity 0; Diameter of Average mass 1.216880 micro-m*
5. Zero flow also changed particle morphology. Pyrell smoke changed from fractal-like clusters of up to 30 primary spheres at 8 cm/s to individual spherical particles at zero flow. Lampwick also formed large single spheres. The authors attribute this to higher gas temperatures when heat leaves the sample by conduction rather than convection. They stress that this concentrated, slow-mixing condition has no 1 g analogue, because buoyancy would widen the mixing zone. *(result, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p9): *change in the morphology of the Pyrell smoke from fractal-like clusters with up to 30 primary spheres for the case with a flow of 8 cm/s to spherical particles for the zero-flow condition*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p9): *It is important to recognize that this condition is unique to low-gravity scenarios.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *In zero-flow conditions,Pyrell and lamp wick particles coalesced into large individual spheres rather than forming agglomerates, as they did at higher air flows.*
6. Comparing the DustTraks with 10 um and 1 um impactor inlets showed that about 40% of the aerosol mass from lampwick and silicone had aerodynamic diameters above 1 um. For Teflon and Kapton the figure was about 20%, so their smoke was mostly below 1 um. *(result, high)*
   - `PSI-101_Presentations_SAME-2_Comparison of Flight and Ground Test Results.pptx` (slide 27): *For lampwick and silicone approximately 40% of the aerosol mass had aerodynamic diameters greater than 1 μm however Teflon and Kapton were mostly less than 1 μm*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *As shown in Figure 5, lamp wick and silicone exhibit larger portions of the particle distribution (~ 40% of the mass) larger than 1 μm compared to 20% of the mass for Teflon and Kapton.*
7. The ISS light-scattering detector missed small-particle smokes. The 2018 analysis states it would not have alarmed for over half of the Kapton tests and two-thirds of the Teflon tests. In the SAME-R rows of the results workbook, the raw ISS scatter voltage was below the 2 V planned alarm level in 21 of 30 Kapton entries and 12 of 17 Teflon entries (e.g. Teflon run 56: 0.18 V; Kapton run 61 at 417 C: 0.68 V). Silicone, lampwick and Pyrell gave 4.4-6.3 V, mostly at about 6.2-6.3 V, the ceiling of logged values (saturation). Kapton heated to 574 C (run 62) also reached 6.24 V. *(result, high)*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The ISS detector would not have alarmed for over half of the Kapton smoke tests, and 2/3 of the Teflon tests.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The ISS detector signal was frequently saturated mainly by the larger smoke materials Silicone, Pyrell and lamp wick.*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row all rows with Flight=2: *count of 'ISS Detector Scatter (volts)' < 2: Kapton 21/30, Teflon 12/17, lampwick/silicone/Pyrell 0*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 56 (Flight=2): *Teflon Baseline; ISS Detector Scatter 0.1842 V*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 61 (Flight=2): *Kapton Baseline Aging; ISS Detector Scatter 0.678 V; Sample Temperature 417.3 C*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 62 (Flight=2): *Kapton High Temp aging; ISS Detector Scatter 6.242 V; Sample Temperature 574.3 C*
   - `PSI-101_Engineering Documents_SAME EIRD Rev 2.00 02-25-05 HIgh Q.pdf` (p12): *The current planned alarm value is 2 volts which is calibrated to 1% obscuration per foot (visible light) for punk type smoke in a smoke box.*
8. The Space Shuttle ionization detector, run only in selected tests because its pump drew about 3 L/min, was somewhat less sensitive overall than the ISS detector. It did better than the ISS detector for Teflon smoke. Some Kapton, Teflon and lampwick points fell below its alarm boundary. Its signal drop (offset minus signal) was smallest for Kapton and Teflon baseline runs (0.20 V, run 92; 0.24 V, run 89). It was larger for silicone (0.79-1.00 V, runs 72 and 91) and Pyrell (0.81 V, run 87). In SAME-1 raw traces, Teflon gave a weak ISS signal but a strong STS signal. *(result, medium)*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *For the Space Shuttle detector, the materials in this category are Kapton, Teflon, and lamp wick, whereas the ISS detector had difficulties detecting Kapton and Teflon smoke.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The Shuttle was somewhat less sensitive than the ISS detector but, for the conditions tested, performed better for Teflon smoke than the ISS detector.*
   - `PSI-101_Presentations_SAME-2_Comparison of Flight and Ground Test Results.pptx` (slide 28): *ISS Detector showed reduced detection performance for Kapton and Teflon due to the small size STS Detector fared slightly better for Kapton and Teflon*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 92 (Flight=2): *Kapton Baseline STS det; STS detector delta 0.2027 V*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 89 (Flight=2): *Teflon Baseline STS det; STS detector delta 0.2405 V*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 72 (Flight=2): *Silicone Baseline STS det; STS detector delta 0.7909 V*
   - `PSI-101_Analyzed Data_SAME, SAME-R_Results.xlsx`, sheet Reduced Data with STS Det, row SAME # 87 (Flight=2): *Pyrell Baseline STS det; STS detector delta 0.8118 V*
   - `PSI-101_Presentations_SAME-R_Particle Morphology and Size Results from the Smoke Aerosol Measurement Experiment-2.pptx` (slide 50): *Teflon: Note weak scattering (ISS) detector signal but ionization (STS) is still strong*
9. The prototype two-moment sensor MPASS was tested with a single least-squares third-order correlation fitted to all test points with signal-to-noise > 2, regardless of material, heating rate or aging. The correlation cut the relative variance of the size-normalised response by at least a factor of 2 compared with a single-output sensor. Mass-concentration prediction was better than number prediction, consistent with MPASS having been optimised for mass. The authors conclude that a two-moment sensor can tell a high smoke concentration from a lower concentration of large dust particles. *(result, medium)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p6): *A least-squares, third-order, correlation was computed on all test points with a signal to noise ratio greater than 2 independent of all other parameters (e.g. material, heating rate, and aging time).*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *Both figures show that the correlation decreases the relative variance by roughly a factor of at least 2 relative to that provided by a conventional single-output sensor.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *The resulting variance for the mass response is substantially lower than for the number concentration.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *The MPASS therefore has the ability to discern the difference between a strong signal from a high smoke concentration and a strong signal from a lower concentration of very large dust particles, a feature which can minimize false smoke detector alarms.*
10. Clean TEM grids were recovered this time (70-72 grid samples, compared with all SAME-1 grids being contaminated). They show distinct morphologies by material. Kapton and lampwick formed spherical droplets; Kapton particles were small and rarely agglomerated, and lampwick particles were 200-1400 nm. Teflon formed agglomerates of uniform primaries under about 200 nm, while Pyrell formed agglomerates of primaries widely spread in size. Silicone left no TEM-visible particles, presumably because liquid droplets evaporated in the vacuum. The visible effect of aging was the disappearance of the smallest particles, not a growth of the large ones. *(result, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p3): *In the SAMER flight tests, 70 TEM samples were collected totally.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *Overall, 72 particle samples were taken on Transmission Electron Microscope (TEM) grids using the thermal precipitator.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p16): *Kapton particles are smaller but rarely agglomerated.*
   - `PSI-101_Presentations_SAME-R_Particle Morphology and Size Results from the Smoke Aerosol Measurement Experiment-2.pptx` (slide 23): *Teflon aggregates: numerous primaries of same dimension Pyrell Aggregates: primaries widely distributed in size*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *Overall, silicone rubber presented no particles that were visible via TEM, presumably because the particles were condensed liquid that evaporated before they coul d be imaged in the TEM.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p7): *instead the mo st visible change is the disappearance of the smallest particles.*
11. The ground SMPS drum tests checked the lognormal assumption behind the moment method. Kapton and lampwick smoke were well described by lognormal distributions. Silicone was not: it had a shoulder at small sizes and a steeper large-size tail, and the SMPS (up to 1000 nm) captured only about 40% of its volume distribution. Teflon and Pyrell aggregates are non-spherical and were excluded. In flight, TEM and moment-method diameters agreed well for Kapton, the best-suited smoke. For lampwick, Kapton and Pyrell, the moment method gave a reasonable D_avm. *(method, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p22): *Overall, the qualitative comparison of these diameters strongly suggests that the smoke particle size distributions for Kapton® and lamp wick can be considered lognormal and silicone should not.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p20): *the black bar representing a 1000 nm upper size limit is only at 40%, indicating that 60% of the distribution is missed by the instrument*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p11): *Pyrell® and Teflon® are not spherical aerosols and thus are not relevant to the moment method approach.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p24): *Thus, it can be concluded that Kapton smoke at these temperatures is very well suited to measurement by the moment method.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p25): *For the three materials in this graph, the moment method provides a reasonably good measurement for the diameter of average mass.*
12. Ground tests with identical SAME hardware at 8.1 cm/s, matching temperature and aging (218-1923 s), gave diameters of average mass that fell on a slope-1 line against the flight values. At ventilation speeds of at least 8.1 cm/s, pre-ignition pyrolysis smoke is therefore about the same size in low gravity as in 1 g. The hypothesised large microgravity droplets appeared only at low or zero flow and with long aging. *(null_result, high)*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *The diameter of average mass from low-gravity is plotted versus the results from corresponding normal gravity tests under the same flow, temperature, and aging conditions and shown in Figure 8. Overall the results correlate strongly with a slope of 1.*
   - `PSI-101_Presentations_SAME-2_Comparison of Flight and Ground Test Results.pptx` (slide 28): *Ground based testing at 8 cm/s showed particle dimensions very close to the flight results*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/ (doi:10.1016/j.firesaf.2018.04.004)>: *Results from the ISS experiment show that smoke particles vary in morphology and average diameter, however, they are not significantly different from smoke particles generated in equivalent experiments performed in normal gravity.*
13. The commanded heater set point is not a reliable proxy for sample temperature. Runs with the same Rt/R0 differed by up to 30 C in actual heating temperature, because the length of wire not in contact with the sample varies. The team therefore re-characterised each test by a derived wire temperature, using a two-section convective heat-balance model of the heater. *(method, high)*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p26): *it is surprising that for the same R t/R0, the actual heating temperature di fference can be as large as 30 degrees Celsius.*
   - `PSI-101_Reports_SAME-R_Final Report.pdf` (p27): *It was identified that each sample has a significant length of leading section of the resistive wire.*

## Fire-safety relevance

SAME-R is the main PSI dataset on what early (pre-flaming) spacecraft smoke looks like to a detector. Overheated Kapton and Teflon, the insulation materials most likely to overheat first in electrical faults, give very small particles (D_avm about 0.1-0.2 um unaged). The ISS forward-scattering detector would often not alarm on these. Silicone, cellulose and Pyrell give large particles that saturate it. The older Shuttle ionization design handles small particles better but rejects particles above 1-2 um, and long aging or stagnant (avionics-box) conditions push smoke towards those sizes. The authors conclude that a single-moment detector cannot be sensitive across this size range and also reject large background dust. They recommend size-selective detection, either by classifying particles or by measuring two or more moments, as the MPASS demonstrated, possibly with gas-species sensing. Because 1 g and microgravity smoke matched at 8.1 cm/s, ground tests with controlled aging can screen detectors for ventilated conditions. Low-flow and stagnant microgravity cases still need special attention, because they produce larger, differently shaped particles.

### Habitat conditions

All smoke was generated in MSG air, and the documents do not report oxygen fraction or pressure (presumably ISS cabin air near sea-level conditions: about 20.9% O2 at 101.3 kPa). No tests were made in the enriched-oxygen, reduced-pressure atmospheres planned for exploration (e.g. 30% or more O2 at 70.3 kPa or less for a lunar habitat). Pyrolysis rates and particle formation could differ there, and the lower gas density changes diffusion and coagulation rates. The results also cover only 0-8.1 cm/s local flow and pre-ignition heating, not flaming soot.

### Earth benefits

The investigators note that smoke detectors developed from SAME results could serve other confined, hard-to-evacuate environments such as submarines and underwater laboratories. The moment-method and two-moment sensing approach also bears on reducing nuisance alarms in terrestrial detectors.

## Limitations

- The geometric mean diameter and sigma_g depend on a lognormal assumption that held for Kapton and lampwick but not for silicone. Teflon and Pyrell aggregates are non-spherical, so their moment-method diameters are equivalent-sphere approximations.
- Instrument uncertainties are large: about +/-30% for the zeroth moment, +/-12% for the first and +/-25% for the third. Diameter repeatability is about +/-15%. Many smokes exceeded the calibration range of the ionization (first-moment) chamber, which most affects Dg and sigma_g.
- The DustTrak dilution orifices did not run at critical flow, because the N2 regulator was undersized and the orifices were never calibrated. Dilution ratios had to be reconstructed after flight from a generic orifice curve and logged pressures.
- In the zero-flow runs, roughly half (final report) or two-thirds (2018 paper) of the smoke escaped through the duct inlet into the MSG. Particle counts were therefore low, TEM grids sparse, and zero-flow concentrations are not comparable with flow runs.
- The Shuttle detector was used in only a few runs and never with chamber aging. The ISS detector saturated for the large-particle smokes. Detector conclusions therefore rest on a small set of points, and the documents read give no detector response times.
- Only five materials were tested, at small scale, under pre-ignition heating, in cabin-like air. Real spacecraft fires involve more materials, flaming soot, larger volumes and background dust, which the authors note can be large.
- Sample temperature was never measured directly. It was inferred from heater-wire resistance with a simplified heat-balance model, and the same set point could differ by up to 30 C.

## Data in PSI

PSI-101 holds 343 files (about 6.3 GB). The most useful file is the analysed workbook 'SAME, SAME-R_Results.xlsx' (about 45 sheets). It holds per-run reduced data for SAME-1, SAME-R and ground tests: test conditions, ISS and STS detector voltages, P-Trak, DustTrak and MPASS outputs, moment diameters, Hatch-Choate sigma_g and D_g, sample temperature and mass loss. It also has sheets for detector-alarm analysis, flight vs ground and SMPS drum comparisons. Another 70 or so per-run .xls files hold the reduced time series for runs 48-114, and per-run TEM size-analysis workbooks cover runs 54, 55, 60, 62, 63, 64 and 94. The 89-page final report (2014) includes the test matrix (Appendix A), mass loss (Appendix C), the TEM grid map (Appendix D/E) and the 2012 ICES paper (Appendix F). Raw data (223 files, 5.7 GB) are mostly not downloaded: 78 zips (1.7 GB), 8 MP4 downlink videos (3.7 GB), 44 housekeeping CSVs and 74 TEM image decks (pptx). The engineering documents are SAME-era (EIRD, verification plan, wire tests). The two legacy .ppt presentations could not be read. The experimental table CSV is a 10-column extract of Appendix A.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Analyzed Data | combined results workbook, per-run reduced .xls files, per-run TEM size-analysis workbooks, sample-description tables (docx) | .xlsx .xls .docx | 86 | 495 MB | yes |
| Raw Data | housekeeping CSVs, video downlinks, TEM image decks and zips, a few raw .xls and PDF image sheets | .zip .mp4 .csv .pptx .pdf .tif .xls .xlsx .doc | 223 | 5.72 GB | no |
| Reports | SAME-R final report (2014) with appendices and the 2012 ICES paper | .pdf | 1 | 5 MB | yes |
| Presentations | 2012 and 2013 ICES talks (.pptx readable); two legacy SAME talks (.ppt, unreadable) | .pptx .ppt | 4 | 33 MB | yes |
| Engineering Documents | SAME EIRD (science requirements and detector background), VPRED, wire tests, thermal precipitator usage, drawings (no text) | .pdf .xls .xlsx .zip | 24 | 55 MB | yes |
| Science Documents | SAME baseline concept description and operations manual | .pdf | 2 | 1 MB | yes |
| Reference Data | SAME software description and requirements documents | .pdf | 2 | 1 MB | yes |
| Experimental table | SAME-R test matrix extract (109 rows) | .csv | 1 | 0 B | yes |

Rows in the unified `tests` table: 109

## Related investigations

- [PSI-102](PSI-102-same.md): precursor
- [PSI-102](PSI-102-same.md): shared hardware
- [PSI-115](PSI-115.md): ground re-analysis
- [PSI-47](PSI-47-daft-daft-2.md): precursor

## Open questions

- Re-derive detector alarm/no-alarm outcomes for every SAME-R run with consistent offsets (ISS scatter baseline, STS offset) and plot them against M0, M1/M0 and D_avm, as a quantitative detector-design map.
- Fit coagulation (aging) kinetics run by run from the paired unaged/aged rows (number decay and D_avm growth vs net aging time), and compare with the self-preserving sigma_g of 1.32.
- Use the per-run housekeeping CSVs and reduced .xls time series to compare time-to-alarm for the ISS and STS detectors, not only peak signals.
- Reconcile the three different zero-flow size-increase figures (30-40%, 2-3x, 1.7x average) from the per-run workbook.
- Combine the ImageJ TEM particle lists (runs 54, 55, 60, 62, 63, 64, 94) into full size distributions and fractal parameters for the Teflon and Pyrell aggregates.

## Dashboard ideas

- **smoke size by material, aging and flow** (`material`, `flow_cm_s`, `net_aging_s`, `sample_temp_c`, `count_mean_diam_um`, `d_avm_um`, `sigma_g`): Shows the central SAME-R result: Kapton/Teflon smallest, silicone/lampwick/Pyrell largest, and growth with aging and low flow.
- **detector response map** (`material`, `M0_per_cm3`, `d_avm_um`, `iss_scatter_v`, `sts_delta_v`, `alarm_threshold`): Lets users see which smokes each spacecraft detector would or would not alarm on, and the ISS detector saturation.
- **flight vs ground scatter** (`material`, `d_avm_flight_um`, `d_avm_ground_um`, `aging_s`): Reproduces the slope-1 result that 1 g tests predict microgravity smoke at 8.1 cm/s.
- **TEM morphology gallery** (`run`, `material`, `aged`, `flow_cm_s`, `morphology_note`, `image_file`): Pairs morphology (droplets vs agglomerates, zero-flow spheres) with the moment data for each run.

## Gaps and data-quality notes

- The two legacy .ppt presentations ('Measurement of Smoke Particle Size under Low-Gravity Conditions', 'Detection of Smoke from Microgravity Fires') have no extracted text and were not read.
- The detector-performance figures (alarm boundaries in Fig. 9 of the 2018 paper; slides 23-26 of the 2013 talk) are images only. Alarm counts were taken from the 2018 paper text and recomputed from raw ISS volts against the 2 V planned alarm level, without offset correction. The STS alarm threshold voltage was not found in the documents read.
- Oxygen fraction, pressure and humidity in the MSG during tests are not stated in the documents read (final report, presentations, EIRD excerpts, BCDD).
- Table 1 (baseline diameters) appears with two different value sets in the same final report (pp. 4-5 vs Appendix F p. 78, e.g. Kapton unaged Dg 0.047 vs 0.042 um). This record quotes the main-text set.
- The size increase at zero flow is reported inconsistently: 30-40% (final report text), 2-3x (appended 2012 paper conclusions), factor 1.7 average (2018 paper). Smoke lost at zero flow is 'about half' vs 'about 2/3'.
- TEM sample count is 70 (final report, flight operation section) vs 72 (results section and 2018 paper).
- Run counts differ: the PSI record says 66 test points, the final report 67 runs (109 entries including secondary aging). The experimental-table CSV has 109 rows, but one is a mislabelled duplicate ('Teflon, 57', Rt/R0 1.253, which Appendix A lists as lampwick reburn run 57), and Kapton run 112 (2 cm/s, STS) is missing.
- The PSI record's experimentHardware field says 'Comparitive Soot Diagnostic Hardware' with a 1996 NTRS link. That describes the earlier CSD experiment, not the SAME hardware actually used.
- The SAME Operations Manual contains laptop FTP instructions with an internal IP address and anonymous login. They were not copied; no real credentials were seen.
- Sample dimensions (about 0.5 cm x 1.3 cm) come only from the 2018 journal paper; the PSI documents read do not state them.
- Most raw data (zips, MP4 downlink video, housekeeping CSVs) are not downloaded and were not inspected.
