# PSI-102: SAME (Smoke and Aerosol Measurement Experiment (called Smoke Aerosol Measurement Experiment in the investigators' reports))

On the Space Station, small pieces of common spacecraft materials (Teflon, Kapton, silicone rubber, cotton lamp wick) were overheated without burning, and the size of the smoke particles was measured to find out what kind of smoke detector would reliably catch an early spacecraft fire.

Investigators: David L. Urban (PI; NASA Glenn Research Center); George W. Mulholland (Co-I; University of Maryland, formerly NIST); Thomas G. Cleary (Co-I; NIST); Jiann C. Yang (Co-I; NIST); Zeng-Guang Yuan (Co-I in the concept document; National Center for Space Exploration Research); Gary A. Ruff (Project Scientist in the concept document; NASA GRC); Claire Fortenberry (listed as Project Scientist in the PSI record; NASA GRC)

## At a glance

| | |
|---|---|
| Setting | ISS · MSG · SAME hardware |
| Platform | International Space Station (ISS), Expedition 15 (flight tests September to early October 2007) |
| Facility | Microgravity Science Glovebox (MSG) |
| Dates | 2001-03-02 to 2008-02-28 |
| Fuels and samples | Teflon; Kapton; Silicone rubber; Cellulose; Dibutyl phthalate |
| Varied | sample material: Teflon, Kapton, silicone rubber, cellulose lamp wick, dibutyl phthalate (reference) categorical<br>air flow velocity over the sample: 2-8 cm/s as flown (design range); the planning matrix in the PSI table lists 5 and 10 cm/s cm/s<br>aging (hold) time before measurement: 10-1800 s (summary results given for 0 and 720 s); planning matrix lists 1 and 20 min s<br>sample (pyrolysis) temperature, set as heater-wire resistance ratio Rt/R0: nominal Rt/R0 1.245 (lamp wick) to 1.440 (Teflon); flight values per run and conversion to degrees C not given dimensionless resistance ratio<br>planned sample weight-loss rate (planning matrix only): 1-2 mg/min |
| Number of tests | 47 |
| Fire-safety pillars | detection, fundamental |

## Question

Spacecraft smoke detectors (ionization on the Space Shuttle, near-infrared forward light scattering on the US ISS modules) were designed from 1-g data, and the two designs respond to non-overlapping particle sizes. Without buoyancy, smoke from an overheated material stays longer in the hot, vapour-rich zone near the source and takes longer to reach a detector, so particles might grow by nucleation, condensation and coagulation. The earlier Shuttle-glovebox Comparative Soot Diagnostics (CSD) experiment had found larger solid smoke particles in low gravity and a Shuttle detector that was blind to visible silicone-rubber and paper smoke, but could not size the liquid droplets. SAME set out to quantify the particle size distribution of smoke from overheated (not flaming) spacecraft materials in microgravity, including the effect of sample temperature, air flow and aging time, to compare it with 1 g, to test the hypothesis that liquid smokes form substantially larger droplets in microgravity, and to evaluate how the two existing US spacecraft detectors respond.

## Summary

SAME characterised pre-fire smoke in microgravity to guide spacecraft smoke-detector design. In the ISS Microgravity Science Glovebox during Expedition 15 (2007), wire-wrapped samples of Teflon, Kapton, silicone rubber, cellulose lamp wick and a reference liquid (dibutyl phthalate on a wick) were heated below ignition in a 2-8 cm/s air flow; the smoke was held in an aging chamber for 10-1800 s, then measured by three compact instruments giving the zeroth, first and third moments of the size distribution, from which a lognormal geometric mean diameter and spread were derived. Fresh smoke had geometric mean diameters of 80-189 nm and mass-mean diameters of 179-472 nm (geometric standard deviation 1.84-2.18); 720 s of aging, by coagulation, raised these to 155-352 nm and 267-606 nm. Silicone and lamp-wick smoke carried roughly half their mass above 1 um; Teflon and Kapton very little. At matched 8 cm/s flow, sizes matched 1-g tests. The Shuttle ionization detector responded to every test, the ISS light-scattering detector poorly to Teflon. The investigators concluded single-moment detectors are risky and recommended multi-moment or size-classifying detection.

## Physics

Smoke from a heated but unignited polymer is an aerosol of recondensed pyrolysis products: solid recondensed polymer (Teflon, Kapton) or liquid droplets (silicone rubber, paper/cellulose). Its size distribution is set near the source by homogeneous nucleation of supersaturated vapour, condensational growth and coagulation, and is then modified during transport by coagulation (number falls, mean size rises, mass is conserved) and by wall losses. On Earth the buoyant plume dilutes and carries away the vapour within a fraction of a second; in microgravity the only flow is the imposed or ventilation flow, so residence time at high concentration near the source and transit time to a detector both increase, which favours larger particles. Detectors respond to different moments of the distribution: an ionization chamber signal scales roughly with the first moment (total diameter per unit volume), a light-scattering detector with roughly the third moment (mass) for particles of about 0.2-2 um, so the same smoke can look strong to one and weak to the other. SAME exploited this by measuring three moments and assuming a lognormal distribution, which is fully defined by number concentration, geometric mean diameter and geometric standard deviation. The investigators' CFD model of the ISS Destiny lab showed that, without buoyancy, ventilation mixes smoke through the module instead of collecting it at a ceiling, so detection times are longer and depend on source location.

$$
f_N(D)=\frac{N_t}{\sqrt{2\pi}\,D\ln\sigma_g}\exp\left[-\frac{(\ln D-\ln D_g)^2}{2\ln^2\sigma_g}\right],\qquad M_i=\int_0^\infty D^i f_N(D)\,dD
$$

Lognormal number distribution assumed by SAME. f_N(D) (cm^-4) is the number of particles per cm^3 per unit diameter; N_t = M_0 total number concentration (cm^-3); D_g geometric mean diameter (nm); sigma_g geometric standard deviation (dimensionless, >1). M_i is the i-th moment; SAME measured M_0 (P-Trak), M_1 (ionization chamber) and M_3 (DustTrak). Valid only if the smoke is unimodal and close to lognormal; a bimodal distribution cannot be recovered.

Textbook background: Standard lognormal aerosol distribution.
`PSI-102_Reports_SAME_Final Science Report.pdf` (p17): *Since a lognormal distribution function is uni quely defined by three parameters*

$$
D_p=D_g\exp\left(p\ln^2\sigma_g\right),\quad D_{0.5}=\frac{M_1}{M_0},\quad D_{1.5}=\left(\frac{M_3}{M_0}\right)^{1/3}
$$

Hatch-Choate relation for a lognormal distribution. D_0.5 is the count (arithmetic) mean diameter and D_1.5 the diameter of average mass (nm). The 2009 ICES paper (Appendix B, p37) instead prints D_1.5 = (3/(4 pi rho) M_3/M_0)^(1/3), with rho the particle density and M_3 a mass concentration. The factor 3/(4 pi rho) yields a radius, not a diameter; 6/(pi rho) is the factor that yields a diameter. This record uses the p17 definition above and the report's tabulated diameters, not the p37 factor. Exact for a lognormal distribution.

`PSI-102_Reports_SAME_Final Science Report.pdf` (p17): *There is a unique feature of the lognormal distribut ion, which is describe d by the Hatch-Choate conversion equations 17.*
`PSI-102_Reports_SAME_Final Science Report.pdf` (p37): *the diameter of average mass D 1.5 or md , which is equal to (3/(4πρ)M3/M0)1/3.*
Textbook background: Hatch-Choate conversion equations (Hinds, Aerosol Technology).

$$
\sigma_g=\exp\left[\left(\ln\frac{D_{1.5}}{D_{0.5}}\right)^{1/2}\right],\qquad D_g=\left(\frac{D_{0.5}^3}{D_{1.5}}\right)^{1/2}
$$

Inversion used to compute sigma_g and D_g from the two measured mean diameters. Check with the Kapton baseline: D_0.5 = 105 nm, D_1.5 = 179 nm gives sigma_g = 2.08 and D_g = 80 nm, as tabulated in the final report. Because D_1.5/D_0.5 enters through a square root of a logarithm, small errors in either moment produce large errors in sigma_g when the two diameters are close.

`PSI-102_Reports_SAME_Final Science Report.pdf` (p18): *Using equations (7) and (8), we can get the corresponding values for Dg and*
`PSI-102_Reports_SAME_Final Science Report.pdf` (p37): *Using equation (6), one can relate σ g to the ratio of D 1.5 and D0.5 via the equation:*

$$
\frac{dN}{dt}=-K_0N^2,\qquad N(t)=\frac{N_0}{1+N_0K_0t}
$$

Smoluchowski coagulation of a monodisperse aerosol, used to size the aging chamber. N number concentration (cm^-3), N_0 initial value, K_0 coagulation coefficient (cm^3/s; the EIRD uses 8.5e-7 mm^3/s for 0.1 um and 3.3e-7 mm^3/s for 1 um particles), t aging time (s). Since mass is conserved, the mean volume grows as 1/N. Valid for a quiescent, well-mixed volume when wall loss is small; the EIRD estimate for 0.1 um particles at 1e6 cm^-3 is N/N_0 = 0.66 after 600 s from coagulation versus 0.98 from wall diffusion.

`PSI-102_Engineering Documents_SAME_EIRD.pdf` (p32): *Considering Smoluchowski coagulation for a uniform particle distribution, (Hinds, 1999) the change in the number concentration can be expressed as:*
Textbook background: Smoluchowski coagulation (Hinds, Aerosol Technology).

## Method

### Apparatus

An MSG payload assembled by the crew from modular units (about 5 h of crew time) and then run largely from the GRC Telescience Center. Each sample was a roughly 3 mm diameter cylinder of material wrapped in a stainless-steel wire coil that both heated it and, through its resistance, measured and controlled its temperature (setpoints expressed as a resistance ratio Rt/R0: Kapton 1.380, lamp wick 1.245, silicone 1.327, Teflon 1.440). Six pre-weighed samples were mounted per carousel; five carousels were flown. A piston in a 5.65 L aging chamber drew air over the heated sample through the smoke generation tube (design range 2-8 cm/s; software maximum 9.8 cm/s), held the smoke for a set time with a mixing fan, then pushed it into a low-volume diagnostics duct. There the smoke was measured by: a TSI P-Trak condensation particle counter (isopropanol condensation, 20 nm to about 1 um, 0-1e5 cm^-3, after a software-controlled dynamic diluter; condenser grooved for microgravity), a First Alert residential ionization chamber (Am-241), two TSI DustTraks (90-degree red-laser scattering, 0.001-100 mg/m^3) with 1 um and 10 um inlet impactors, plus an ISS laser forward-scattering detector and a Space Shuttle ionization detector with inertial separator. Thermal precipitators sampled smoke onto TEM grids before and after aging. Signals were digitized at 1 Hz (8-bit).

### Fuels and samples

- Teflon (PTFE) (solid, approx. 3 mm diameter cylinder in heater-wire coil; produces solid recondensed-polymer particles)
- Kapton (polyimide) (solid, approx. 3 mm diameter cylinder in heater-wire coil; solid recondensed-polymer particles)
- Silicone rubber (solid, approx. 3 mm diameter cylinder in heater-wire coil; liquid-droplet smoke)
- Cellulose (cotton lamp wick) (solid, lamp-wick sample in heater-wire coil; liquid-droplet smoke)
- Dibutyl phthalate (DBP), reference smoke (liquid, liquid held in a cotton wick and vaporised by the heater coil; idealised liquid aerosol with known properties)

### Procedure

For each test point the ground team uplinked parameters (sample, heater setpoint, flow, aging time, diagnostics and dilution); the carousel rotated a new sample into the flow duct; the sample was heated for about 60 s (75 s in one run) below its ignition point while the retreating piston drew the smoke-laden air into the aging chamber. After the chosen aging time (10 s to 1800 s) the piston pushed the smoke through the diagnostics duct, where the moment instruments and the two spacecraft detectors sampled it; for aging runs the smoke was measured before and after aging. TEM grids were exposed in the thermal precipitators, and samples were weighed before launch and after return. DustTrak response was calibrated on the ground for each smoke source against a tapered element oscillating microbalance; P-Trak and ionization chamber were calibrated with monodisperse dioctyl phthalate (DOP) droplets against reference instruments. D_0.5 and D_1.5 were computed per run and converted to D_g and sigma_g assuming a lognormal distribution. Ground (1 g) comparison runs were made afterwards with the same type of hardware. Dibutyl phthalate samples were reheated repeatedly to obtain extra test points.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| sample material | Teflon, Kapton, silicone rubber, cellulose lamp wick, dibutyl phthalate (reference) | categorical |
| air flow velocity over the sample | 2-8 cm/s as flown (design range); the planning matrix in the PSI table lists 5 and 10 cm/s | cm/s |
| aging (hold) time before measurement | 10-1800 s (summary results given for 0 and 720 s); planning matrix lists 1 and 20 min | s |
| sample (pyrolysis) temperature, set as heater-wire resistance ratio Rt/R0 | nominal Rt/R0 1.245 (lamp wick) to 1.440 (Teflon); flight values per run and conversion to degrees C not given | dimensionless resistance ratio |
| planned sample weight-loss rate (planning matrix only) | 1-2 | mg/min |

Held constant:

- gravity: ISS microgravity (MSG work volume); 1 g ground comparison runs made separately
- heating duration: about 60 s (one DBP run 75 s)
- regime: non-flaming overheat below the ignition point

Number of tests: 47

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| particle number concentration (zeroth moment M0) | TSI P-Trak condensation particle counter with dynamic diluter | direct |
| first moment M1 (diameter concentration) | ionization chamber from a First Alert residential smoke detector | direct |
| mass concentration / third moment M3, below 1 um and below 10 um | two TSI DustTrak photometers with 1 um and 10 um impactors | direct |
| count mean diameter D0.5, diameter of average mass D1.5, geometric mean diameter Dg, geometric standard deviation sigma_g | moment method (lognormal assumption) from the three instruments | derived |
| response of spacecraft smoke detectors | ISS laser forward-scattering detector (scatter and obscuration channels) and Space Shuttle ionization detector in the diagnostics duct | direct |
| particle size and morphology | thermal precipitator onto TEM grids, post-flight transmission electron microscopy | derived |
| housekeeping: sample heater resistance, gas plume temperature, flow controller rates, pressures, valve states | DACU housekeeping telemetry at 1 Hz | direct |
| sample mass loss | pre-flight and post-flight weighing | derived |

## Findings

1. Fresh (unaged) smoke from overheated spacecraft materials in microgravity was sub-micrometre in number terms. Final-report values (geometric mean / count mean / diameter of average mass, nm; sigma_g): Kapton 80/105/179, 2.08; lamp wick 186/227/341, 1.89; silicone rubber 189/257/472, 2.18; Teflon 170/205/297, 1.84. *(result, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p27): *Kapton 80 105 179 2.08 Kapton aged 155 186 267 1.82 Lamp wick 186 227 341 1.89 Lamp wick aged 258 308 438 1.81*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p27): *Silicone 189 257 472 2.18 Silicone aged 352 422 606 1.83 Teflon 170 205 297 1.84 Teflon aged 228 273 392 1.82*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p4): *The experimental results show that, for the materials tested, a su bstantial portion of the smoke particles are below 500 nm in diameter.*
2. Holding the smoke for 720 s raised all mean sizes and narrowed the distribution, consistent with coagulation. Geometric mean diameter rose to 155 nm (Kapton, x1.9), 258 nm (lamp wick, x1.4), 352 nm (silicone, x1.9) and 228 nm (Teflon, x1.3). Diameter of average mass rose by 28-49%, to 267-606 nm, and sigma_g fell to 1.81-1.83 for all four materials. During aging the P-Trak number count fell substantially while DustTrak mass stayed nearly constant, which indicates coagulation with little wall loss. *(trend, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p27): *Silicone 189 257 472 2.18 Silicone aged 352 422 606 1.83 Teflon 170 205 297 1.84 Teflon aged 228 273 392 1.82*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p25): *Results from the moment instruments for baseline runs (no aging) and 720 second aging runs are summarized in Table 1.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p25): *This behavior is consistent with particle coagulation with limited wall loss.*
3. A later analysis in the SAME-2 slides of the SAME aging runs found number concentrations of spacecraft-material smoke fell by a factor of 1.7-2.7 over 800 s. Measured and predicted (coagulation theory) number decreases agreed within about 20%, and diameters of average mass within 4%. The measured narrowing of sigma_g was typically more than twice the predicted change. *(result, medium)*
   - `PSI-102_Presentations_SAME-2_ParticleMorphology and Size Results.pptx` (slide 41): *For spacecraft materials, number counts decreased by a factor of 1.7 to 2.7 over 800 seconds. The measured and predicted number decreases agree within about 20 %. The best agreement between experiment and prediction is Davm - agree within 4 %.*
   - `PSI-102_Presentations_SAME-2_ParticleMorphology and Size Results.pptx` (slide 41): *The decrease in the geometric standard deviation is typically more than a factor of two greater than the predicted change.*
4. Silicone rubber and lamp wick (liquid-droplet smokes) carried a large share of their mass in particles larger than 1 um, even though their count mean diameters were around 200 nm. The ratio of the 10 um-impactor to the 1 um-impactor DustTrak readings averaged 1.92 for silicone and 1.79 for lamp wick, against 1.22 for Teflon and 1.26 for Kapton. The investigators read this as almost half of the silicone smoke mass lying above 1 um; the SAME-2 conclusions put it at about 40% for lamp wick and silicone. *(result, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p57): *Silicone Rubber 227 1.92 Teflon™ 158 1.22 Lamp wick 172 1.79 Kapton™ 128 1.26*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p28): *Consequently, although the CMD for silicone rubber is 189 nm, almost half the particle mass is larger than 1*
   - `PSI-102_Presentations_SAME2_FlightVSGroundTestResults.pptx` (slide 27): *For lampwick and silicone approximately 40% of the aerosol mass had aerodynamic diameters greater than 1 μm however Teflon and Kapton were mostly less than 1 μm*
5. Microgravity versus normal gravity: the preliminary analysis (AIAA 2008), which used only the P-Trak and ionization-chamber signals, found that baseline count mean diameters in low gravity were larger than in comparable 1-g tests. Silicone rubber was 263 nm (+53%), lamp wick 248 nm (+65%) and Kapton 114 nm (+58%); Teflon was 223 nm, with no 1-g comparison given. The authors summarised this as typically 50% larger, with all sizes below 300 nm. *(result, medium)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p64): *Silicone Rubber 263 53 Teflon™ 223 Lamp wick 248 65 Kapton™ 114 58 Table 1: Count Mean Diameters for Baseline Runs with comparison to 1-g tests.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p66): *Smoke particulate produced in low-gravity was found to be typically 50% large in count mean diameter than similar conditions in normal gravity. The resultant sizes were all below 300 nm*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p64): *Values of D0.5 were calculated directly from the calibrated signals from the P-Trak and the Ion sensor*
6. The later flight-versus-ground comparison (SAME-2 presentation, 2013) reached a weaker conclusion than the 2008 analysis. At 8 cm/s, ground tests gave particle dimensions very close to the flight results, and particle size grew substantially as air flow was reduced. Imposed flow and residence time, rather than gravity as such, appear to control the size. The PSI documents do not reconcile the two statements, and the 2013 deck may include SAME-R flight data. The investigators' 2018 Fire Safety Journal paper, which covers both flights (2007 and 2010), settles it in favour of the weaker conclusion: low-gravity smoke was not significantly different from smoke made under equivalent 1-g conditions, and flight and ground diameters of average mass at matched flow, temperature and aging fall on a slope-1 line at 8.1 cm/s. Lower flow could raise the diameter of average mass by up to about a factor of 2. The preliminary 50% figure in findings[4] is therefore superseded. *(null_result, high)*
   - `PSI-102_Presentations_SAME2_FlightVSGroundTestResults.pptx` (slide 28): *Ground based testing at 8 cm/s showed particle dimensions very close to the flight results*
   - `PSI-102_Presentations_SAME2_FlightVSGroundTestResults.pptx` (slide 27): *Particle dimensions increase substantially as air flow was decreased*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/>: *Results from the ISS experiment show that smoke particles vary in morphology and average diameter, however, they are not significantly different from smoke particles generated in equivalent experiments performed in normal gravity.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/>: *The diameter of average mass from low-gravity is plotted versus the results from corresponding normal gravity tests under the same flow, temperature, and aging conditions and shown in Figure 8 . Overall the results correlate strongly with a slope of 1.*
   - <https://pmc.ncbi.nlm.nih.gov/articles/PMC7918997/>: *The potential error of this analogy can be estimated using Figure 6 which suggests that lower flow rates could increase the diameter of average mass by as much as a factor of 2.*
7. The Space Shuttle ionization detector, sensitive below about 1 um, gave strong signals in every SAME test, including the larger-particle lamp wick and silicone smokes. The ISS forward-scattering detector, sensitive above about 0.5 um, gave strong signals for silicone rubber but erratic or weak signals for Teflon (and Kapton) smoke, which is mostly below 1 um. The two US spacecraft detector designs therefore respond differently to realistic pre-fire smokes. *(result, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p28): *All of the tests conducted in this series of experiments show strong signals on the Space Shuttle detector (ionization) despite the larger particle size distributions seen for the lamp wick (cellulose) and silicone rubber.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p25): *In figure 12, the STS detector provided a strong signal, whereas the signal from the ISS detector was more erratic, because the Teflon smoke is comprised primarily of particles having diameters less than 1*
   - `PSI-102_Presentations_SAME2_FlightVSGroundTestResults.pptx` (slide 28): *ISS Detector showed reduced detection performance for Kapton and Teflon due to the small size STS Detector fared slightly better for Kapton and Teflon*
   - `PSI-102_Presentations_SAME2_FlightVSGroundTestResults.pptx` (slide 4): *ISS detector: sensitive > 0.5 micron*
8. The SAME results differ from the earlier CSD Shuttle experiment, in which the Shuttle detector was nearly blind to dense, visible smoke from overheated silicone rubber and paper. The investigators infer that some credible pre-fire conditions, not reproduced in SAME's controlled flow and heating, can push the size distribution beyond the SAME range. The SAME data therefore bound the problem but do not span it. *(limit, medium)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p28): *The reduced signal on the Space Shuttle detector for CSD suggests that under some reasonable pre-fire conditions the smoke size distribution can extend to diameters beyond those seen in the SAME experiment.*
   - `PSI-102_Engineering Documents_SAME_EIRD.pdf` (p19): *Despite producing dense smoke that was clearly visible, the STS detector showed virtually no signal while the ISS detector saturated.*
9. Implication for detector design: any detector that measures a single moment either needs a very large number concentration to alarm on small particles or alarms on very few large particles, such as dust. The investigators showed this with a hypothetical single-point alarm requirement of 2 mg/m^3 for a lognormal aerosol with GMD 500 nm and sigma_g 1.3. They recommended alarm requirements at several sizes across roughly 200-1200 nm and detectors that measure two or more moments or classify particles by size, which would also help reject false alarms. *(result, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p39): *These figures were developed assuming the alarm level was set at 2 mg/m 3 for a log-normal particle size distribution with a 500 nm geometric mean diameter (GMD) and a geometric standard deviation (GSD) of 1.3.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p40): *Consequently a specification for a single particle size (or no size specification) would be risky.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p40): *An alternative is to develop alarm requirements that include criteria at particle sizes spanning the expected range of fire particulate (e.g. 200 to 1200 nm).*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p29): *Two possible effective means of achieving this size discrimination are to employ a detector that measures more than one mo ment of the size distribution or to use a detector that can classify the particles into size ranges.*
10. Spacecraft background aerosol is sparse at small sizes: ISS US-lab counts measured by the precursor DAFT experiment were below 5 particles/cm^3, the instrument noise level. STS-32 impactors found about 40% of particles in each of the 2.5-10 um and >100 um ranges. This leaves a sub-micrometre detection window where pyrolysis smoke dominates. Because aging and slow mixing make smoke grow, the investigators cautioned against designing only for small particles. *(result, medium)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p14): *the particle count levels were at the noise level for the instrument (less than 5 particles/cm 3).*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p14): *The two impactors reported a bimodal particle size distribution with ~ 40% of the particles in each of the 2.5 μm to 10 μm and >100 μm ranges.*
   - `PSI-102_Presentations_SAME-2_ParticleMorphology and Size Results.pptx` (slide 30): *Given the effects of aging and the slow mixing seen in spacecraft, it is probably unwise to focus entirely on small particle sizes for fire detection*
11. A companion FDS (Fire Dynamics Simulator) model of smoke transport in the ISS Destiny lab, with g = 0 and propane sources giving 1.46-8.47 mg/s of particulate, found that ventilation mixes smoke fairly uniformly through the module. Detection times by the two area detectors (alarm about 0.5 mg/m^3) were long and depended strongly on source location and on obstructions. Some low-soot-yield cases never alarmed. *(result, medium)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p65): *The alarm point for the ISS detector is on the order of 0.5 mg/m 3.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p66): *Numerical modeling of smoke transport in the US Lab Module of the ISS predicted that actual detection times can be quite long and strongly dependent on lo cation and the presence of obstructions.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p66): *Note that a DNA (did not alarm) condition occurred for LA1 for the 0.05 soot yield on the N1 wall for LAS5RR and for LA3 0.05 soot yield on the S3 wall for LAP1RR.*
12. Method: the moment method (three compact instruments plus a lognormal assumption) worked inside the MSG volume and produced on-orbit size statistics without sample return. Uncertainty propagation shows the first-moment (ionization chamber) error dominates the uncertainty in D_g and sigma_g, while the third-moment error matters least. An early Mie-scattering inversion of the DustTrak signal failed to converge for some runs (all silicone baseline runs in the 2009 AIAA paper), possibly because of bimodal distributions. The final values instead used per-material DustTrak calibration against a microbalance. *(method, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p19): *both equations (12) and (13) show the uncertainty of M3 contributes the least to the combined uncertainties of Dg and*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p48): *This non-convergence is currently under investigation but may be due to the presence of a bimodal particle size distribution.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p48): *The Silicone results did not converge for these conditions*
13. The TEM grids from the thermal precipitators were contaminated by extraneous particles, believed to come from the precipitator assembly. Only the lamp wick and Teflon grids showed distinct smoke particles consistent with ground experience, so SAME produced no independent microscopy check of the moment-method sizes for Kapton or silicone. *(limit, high)*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p28): *The TEM grids recovered from the thermal precipi tators were unfortunately contaminated with extraneous particles whose origin was believed to be somewhere in the assembly of the thermal precipitators.*
   - `PSI-102_Reports_SAME_Final Science Report.pdf` (p28): *Despite the contamination, the lamp wick and Teflon samples pr oduced distinct particles consistent with ground based experience.*

## Fire-safety relevance

SAME is the main microgravity data set behind requirements for next-generation spacecraft smoke detectors. Its central message is that early (pre-flaming) smoke from common spacecraft materials spans roughly 100 nm to beyond 1 um and shifts with material, flow and aging. Teflon and Kapton smoke stays mostly below 300 nm and is hard for light-scattering detectors such as the ISS unit to see. Silicone and cellulose smoke puts much of its mass above 1 um, where ionization detectors with particle separators, such as the Shuttle unit, may lose it (as in CSD). Smoke trapped in enclosures or carried slowly by cabin ventilation coarsens by coagulation. Background dust is mostly large, so a detector that measures two moments, or classifies by size, can both catch small-particle smoke and reject dust. Transferability: these are small, controlled, non-flaming overheat events of four materials at 2-8 cm/s and up to 30 min aging. They are not flaming fires (soot), not full-scale cabin fires, and the gravity effect itself is uncertain because ground tests at matched flow gave similar sizes.

### Habitat conditions

No PSI document states the oxygen fraction or pressure of the air drawn over the samples. The smoke was generated in air inside the MSG on ISS, nominally cabin air, but this is not documented. Against the common references: Earth sea level is 20.9% O2 at 101.3 kPa; a Moon habitat would likely have 30% O2 or more at 70.3 kPa or less; a spacesuit has 100% O2 at 29.6 kPa. SAME gives no data on how oxygen enrichment or reduced pressure would change pyrolysis rate, nucleation or particle size, or on how lower pressure (longer mean free path, faster coagulation and diffusion) would affect detector response. Its results apply to near-sea-level air only by assumption. There is also no partial-gravity smoke data.

### Earth benefits

The investigators expect the smoke-detector technology to be useful in other confined, extreme environments on Earth, such as submarines and underwater laboratories. The multi-moment detection concept also addresses the familiar trade-off between ionization and photoelectric residential detectors.

## Limitations

- Size statistics rest on a lognormal assumption from three moments. Bimodal distributions (suspected for silicone) cannot be represented, and the third-moment instrument depends strongly on particle size and refractive index. The final DustTrak calibration assumed each smoke's size distribution matched its ground calibration aerosol.
- Published values changed between analyses. Teflon baseline GMD was 159 nm (AIAA 2009) and 170 nm (final report), and its diameter of average mass 219 and 297 nm. Lamp wick diameter of average mass was 420 and 341 nm. Silicone count mean diameter was 263, 227 and 257 nm in the three papers. The 2012 SAME-1&2 table gives much smaller unaged values, for example Kapton GMD 47 nm. Absolute sizes therefore carry a calibration uncertainty of tens of percent.
- The final report's text says the aged silicone diameter of average mass rose to over 1 um. Its own table (606 nm) and the 2009 ICES paper ('over 500 nm') contradict this, so the 1 um statement looks like an error.
- The final report gives no results for the dibutyl phthalate reference smoke (22 of 47 test points), even though the 1-g versus microgravity comparison of a liquid aerosol was objective 2. The hypothesis that liquid smokes form much larger droplets in microgravity was therefore not directly tested in the reported results.
- Sample temperatures were controlled as heater-wire resistance ratios, but no degrees-C values, measured mass-loss rates or per-run flow and aging settings are tabulated in the reports. Run-by-run conditions must be reconstructed from the command logs and housekeeping files.
- Only non-flaming overheat of small samples was studied, with no soot-producing flaming fires, and only four real materials (Pyrell foam was added in the reflight). The smoke is drawn into a closed chamber, so the near-source residence time is set by the hardware rather than by a free microgravity plume.

## Data in PSI

PSI holds the documents needed to understand SAME: a 68-page final science report (2010) that appends the four SAE/AIAA papers of 2008-2009 and the flight test log, the requirements document (EIRD) with the CSD background and design calculations, a concept description, operations manual, software and crew-interface documents, and two readable 2012-2013 presentations that actually belong to the SAME reflight era (SAME-2). The 59 readable analyzed-data spreadsheets are per-run 1 Hz housekeeping and diagnostic time series (P-Trak, two DustTraks, two ionization channels, ISS and STS detector voltages, heater resistance, flows) for most of the 47 test points, some with averaging windows marked, plus command logs. They contain no computed particle diameters and no calibration curves, so re-deriving the size table requires the ground calibrations, which are not in PSI. The 8-row experimental table reproduces the pre-flight planning matrix, not the as-flown conditions. Three legacy .ppt files and one .doc are unreadable, and 18 engineering drawings have no text layer.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Reports | SAME Final Science Report (March 2010) with flight test log and four conference papers appended | .pdf | 1 | 3.7 MB | yes |
| Analyzed Data | per-run housekeeping/diagnostic time series (.xls/.xlsx, 1 Hz), averaging sheets and test command logs, named by GMT day, material and run number; 4 zero-byte .xml placeholders | .xls .xlsx .xml | 63 | 228 MB | yes |
| Presentations | two readable SAME-2 decks (particle morphology and size, 2012; flight versus ground, 2013); three unreadable legacy .ppt (early results; 2008 size measurement; 2005 detection of smoke) and one .doc (2005 paper) | .pptx .ppt .doc | 6 | 61.5 MB | no |
| Engineering Documents | EIRD requirements document, verification plan, ignitor-wire characterization report and data, 18 drawings without text, heater-coil videos and an operations image archive | .pdf .xls .mp4 .zip | 28 | 362 MB | yes |
| Science Documents | Baseline Concept Description Document and Operations Manual | .pdf | 2 | 900 kB | yes |
| Reference Data | crew interface, software description and software requirements documents | .pdf | 3 | 1.4 MB | yes |
| Experimental table | 8-row planning test matrix (material, flow, weight-loss rate, aging time) | .csv | 1 | 330 B | yes |
| metadata | ISA-Tab metadata zip (file name refers to PSI-170) | .zip | 1 | 13 kB | yes |

Rows in the unified `tests` table: 8

## Related investigations

- [PSI-101](PSI-101-same-r.md): follow-on
- [PSI-47](PSI-47-daft-daft-2.md): precursor
- [PSI-115](PSI-115.md): ground re-analysis

## Open questions

- Re-derive per-run M0, M1 and M3 averages from the 59 housekeeping spreadsheets (averaging windows are already marked in the 'for average' sheets). Tabulate size statistics for every test point, including the DBP reheats and the intermediate aging times between 10 and 1800 s that the reports do not show.
- Correlate the ISS-detector scatter voltage and the STS-detector voltage with the measured moments run by run, to build empirical detector response curves (signal per unit M1 and M3) for microgravity smoke.
- Use the DBP runs, whose vapour properties are well known, to test the nucleation/condensation model in the EIRD appendix and to settle whether liquid droplets grow larger in microgravity than at matched 1-g flow.
- Reconcile the 2008 '50% larger than 1 g' result with the 2013 'ground at 8 cm/s very close to flight' result by separating the effects of flow velocity and gravity.
- Fit coagulation kernels to the aging runs (number decay versus time) to extrapolate size growth to cabin transport times of tens of minutes.
- Check whether the heater resistance and gas-plume temperature records give a usable surface-temperature history per sample, which would link pyrolysis rate to particle size.

## Dashboard ideas

- **size statistics by material, fresh versus aged** (`material`, `aging_s`, `Dg_nm`, `D0.5_nm`, `D1.5_nm`, `sigma_g`): Shows the main SAME result: Kapton and Teflon small, silicone and lamp wick larger, all coarsening with 720 s aging (final report Table 1).
- **lognormal distribution explorer** (`Dg_nm`, `sigma_g`, `N_t`): Plot number and mass distributions from the tabulated parameters, overlaid with the ionization (<1 um) and scattering (>0.3-1 um) detector sensitivity bands.
- **mass fraction above 1 um** (`material`, `dusttrak_10um_over_1um_ratio`, `CMD_nm`): Contrasts count-based size with mass-based size and explains why one detector sees smoke the other misses.
- **run time series** (`time_s`, `ptrak_cm3`, `dusttrakA_mg_m3`, `dusttrakB_mg_m3`, `ion_V`, `iss_scatter_V`, `sts_V`): The housekeeping spreadsheets support replaying any of the 47 test points, including before/after-aging comparisons.
- **detector alarm-requirement simulator** (`Dg_nm`, `sigma_g`, `alarm_mg_m3`, `detector_moment`): Reproduces the investigators' argument that single-moment alarm thresholds are too sensitive at one end of the size range and blind at the other.

## Gaps and data-quality notes

- The experimental table (and tests.csv, 8 rows) reproduces the pre-flight EIRD planning matrix (5 and 10 cm/s, 1-2 mg/min, 1 and 20 min aging) with rows 5-8 reading 'same conditions as 1-4'. It is not the as-flown test list: the flight used 2-8 cm/s, aging of 10-1800 s and 47 test points (final report Appendix A).
- Sample O2 fraction and pressure are not stated anywhere in the PSI documents examined (final report, EIRD, concept description, operations manual).
- Sample temperatures in degrees C, measured mass-loss rates, per-run flow velocities and aging times are not tabulated. Only the heater Rt/R0 setpoints and a few log comments (2 cm/s, 30 min aging, 75 s heating) were found.
- Unreadable files: PSI-102_Presentations_SAME_EarlyResults.ppt, ..._MeasurementofSmokeParticleSizeUnderLowGravityConditions.ppt, ..._Detection of Smoke from Microgravity Fires.2005.ppt and ..._Detection of Smoke from Microgravity Fires_paper.2005.doc. The 2008 SAE paper of the same title as the second is appended to the final report (Appendix D). The 2005 ICES paper (SAE 2005-01-2930) was not found on NTRS by title search. NTRS 20070031686 (2007 ISDC talk, pre-flight) was read but added nothing beyond the final report.
- 18 engineering drawings (sample assemblies, aging chamber, fluids schematics) have no text layer and were not read. Heater-coil videos (TN001/TN002 .mp4 and .zip) and the 'SAME OPS images' zip were not examined.
- The two readable presentations are SAME-2 (reflight, PSI-101) material dated 2012-2013 and mix SAME and SAME-R data (e.g. run numbers 54-84, Pyrell samples, 'SAME-1&2 Results'). Findings drawn from them are flagged as such.
- No DBP particle-size results and no 1-g DBP comparison are reported in the final report, although DBP accounts for 22 of the 47 test points.
- The PSI record field experimentHardware ('Comparitive Soot Diagnostic Hardware') and its NTRS link (19960008413, 'Smoke detection in low-G fires') describe the earlier CSD experiment, not SAME hardware. The metadata zip is named PSI-102_metadata_PSI-170_SAME.zip.
- Final report text says aged silicone diameter of average mass exceeded 1 um, contradicting its own table (606 nm). Count mean diameters for the same materials differ between the 2008 ICES, 2008 AIAA, 2009 AIAA and final-report tables.
- Four Analyzed Data .xml files (16904, 16912, 16937, 16942) are listed in files.csv with zero size and were not downloaded. The PSI record lists 52 removed files (legacy duplicates of the analyzed data).
- Investigator affiliations: the PSI record lists Mulholland at University of Maryland and Claire Fortenberry as Project Scientist; the 2005 concept document lists Mulholland at NIST and Gary Ruff as Project Scientist (the role at the time of flight). Contact e-mail addresses in the record were not copied.
- Changed in the publication review (2026-11-15): findings[5] used to end 'The two statements are not reconciled in the PSI documents, and the 2013 deck may include SAME-R flight data.' with confidence medium. Meyer et al., Fire Safety Journal 98 (2018), which covers both SAME flights (NIST author manuscript PMC7918997), reconciles them: no significant gravity effect at matched conditions of at least 8.1 cm/s. findings[4] (the preliminary 2008 claim of about 50% larger low-g count mean diameters) is kept as the historical result but is superseded. The summary sentence 'An early analysis put low-gravity count mean diameters about 50% above 1-g values.' was replaced accordingly. Per-paper review: data/publications/PSI-102.json.
