# PSI-26: BASS (Burning and Suppression of Solids)

Astronauts burned small fabric strips, plastic spheres and slabs, and wax candles in a gentle, adjustable air stream on the ISS to see whether solids burn more readily without gravity than in the Earth-based test NASA uses to approve materials, and whether a puff of nitrogen puts the flames out.

Investigators: Paul V. Ferkul (PI; NASA GRC / National Center for Space Exploration Research); Sandra L. Olson (Project Scientist / Co-I; NASA GRC); Fumiaki Takahashi (Co-I; listed as Case Western Reserve University in the PSI record, NCSER in the presentations); James S. T'ien (Co-I; Case Western Reserve University)

## At a glance

| | |
|---|---|
| Setting | ISS · MSG |
| Platform | International Space Station (ISS) |
| Facility | Microgravity Science Glovebox (MSG) |
| Dates | 2009-10-01 to 2013-06-30 |
| Fuels and samples | SIBAL cotton-fibreglass fabric; Nomex fabrics; Ultem 1000 polyetherimide; PMMA; Thick flat samples; Candles within ceramic tubes |
| Varied | forced air flow speed (imposed by fan): <1 (fan pot near shut-off; below the 1 cm/s anemometer floor) to about 44; most runs 0-20 cm/s<br>flow direction relative to spread: concurrent, opposed (flat samples); forward-stagnation vs wake ignition (spheres, candles)<br>ambient oxygen (MSG volume): 0.209-0.227 in 2012 (ISS cabin air, not controlled); 0.159-0.212 in 2013 (MSG vitiated with N2 for most runs) mole fraction<br>fuel material and geometry: SIBAL fabric, Nomex (2 types), Ultem film, PMMA sphere/hemisphere, PMMA slab, wax slab, Japan-wax and paraffin candles<br>sample size: flat width 1 or 2 cm; sphere diameter 1 or 2 cm cm<br>nitrogen suppressant flow from upstream nozzle: 0 to about 500 (logged maximum 495) sccm (cc/min) |
| Number of tests | 121 |
| Fire-safety pillars | fundamental, prevention, suppression |

## Question

BASS tested the hypothesis that a solid with adequate ventilation burns as well as, or better than, the same material in normal gravity at the same pressure, O2 concentration and temperature. If true, NASA-STD-6001 Test 1 (an upward-burning 1-g test used to screen spacecraft materials) would offer less safety margin than assumed. Testing anything but the thinnest fuels needs minutes of microgravity, which drop towers and parabolic aircraft cannot give. The investigation had two objectives. (1) Begin to bridge the gap between the 1-g Test 1 method, ground-based microgravity tests and actual flammability in space, using practical, thicker fuels and wake flames (flames sheltered behind an object). (2) Assess how well an inert gaseous agent (nitrogen, similar to the ISS extinguisher agent) puts out flames over different materials, geometries, preheat states and flows. Behind the second objective is the worry that in microgravity the best place to aim a suppressant is unclear, and a jet might even feed the flame by entraining air.

## Summary

BASS (Burning and Suppression of Solids) burned 41 small solid samples in about 115 burns inside a 76 mm square flow duct in the ISS Microgravity Science Glovebox in 2012-2013, at about 1 atm and 16-23% O2. Fuels were a cotton-fibreglass (SIBAL) fabric, Nomex and Ultem sheets, PMMA spheres and slabs, and wax candles, in fan-driven air flows from below 1 to about 44 cm/s, with an upstream nitrogen jet of up to 500 cc/min. The fabric, which cannot burn downward in 1 g air, spread steadily in 9-10 cm/s opposed flow. Opposed spread peaked at 10-15 cm/s; concurrent spread rose linearly with flow (2.55 versus 1.21 mm/s opposed at about 10 cm/s), and concurrent flames quenched below 1 cm/s. PMMA and candle flames survived for minutes as dim blue flames near 1 cm/s. The nitrogen jet usually removed only the leading edge, and most flames went out only when the airflow stopped. Fire-retarded Nomex HT90-40 and Ultem did not burn at 21-22% O2. Normal-gravity screening therefore does not bound flammability in every configuration.

## Physics

A flame spreading over a solid heats the unburnt fuel ahead of it until the fuel pyrolyses. The vapour then mixes with oxygen and burns. On Earth, buoyancy drives an induced flow past the flame of order tens of cm/s (the BASS authors give about 20 cm/s at the flame zone for their fabric). In orbit, buoyancy is essentially absent, so the only flow is what the ventilation imposes, and that can be just a few cm/s. Two flow directions matter. In opposed flow the air moves against the direction of spread (downward burning on Earth), and spread is controlled by heat conducted forward from a small region at the flame's leading edge. In concurrent flow the air moves with the spread (upward burning on Earth), and the whole flame and hot plume preheat the fuel, so the flame can grow. A thin fuel's flammability boundary, plotted against flow speed, is U-shaped. At high flow, finite-rate chemistry fails and the flame blows off. At very low flow, the flame's heat release falls until radiative loss is a significant fraction of it, and the flame quenches. The low-flow quenching branch lies below the 1-g buoyant flow limit, so it can only be observed in microgravity. Between the branches there can be conditions, such as moderate opposed flows, where a material that self-extinguishes on Earth burns steadily in orbit. Inert-gas suppression works by diluting the oxygen and adding heat capacity at the flame. In microgravity, however, a jet also adds momentum and can entrain surrounding air, so where and how the agent is delivered matters.

$$
V_f = \frac{\pi}{4}\,\frac{\lambda_g\,(T_f - T_v)}{\rho_s\,c_s\,\tau\,(T_v - T_\infty)}
$$

Thermal-regime (de Ris) spread rate of an opposed-flow flame over a thermally thin solid. $V_f$ spread rate (m/s); $\lambda_g$ gas thermal conductivity (W/m K); $T_f$ flame temperature, $T_v$ fuel vaporisation (pyrolysis) temperature, $T_\infty$ ambient temperature (K); $\rho_s$ solid density (kg/m3); $c_s$ solid specific heat (J/kg K); $\tau$ fuel half-thickness (m). Valid when gas-phase chemistry is fast compared with the flow residence time (large Damkohler number) and radiative losses are negligible; $V_f$ is then independent of the opposed flow speed. BASS opposed spread over SIBAL fabric instead peaked at 10-15 cm/s and fell on either side, so the BASS flows lie partly outside this regime: kinetic effects at higher flows, radiative losses at low flows.

Textbook background
<https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *de Ris formula for the thin limit, Equation (2.9) modified with a factor of π/4, can be expressed as*
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Opposed-flow flame spread rate increases with flow to a maximum when the flow speed is around 10 to 15 cm/s and then decreases at higher speeds, in good agreement with previous research [Olson, 1991].*

$$
\mathrm{Da} = \frac{t_{res}}{t_{chem}} \approx \frac{\alpha_g / U_r^{2}}{\left[\rho_g\,Y_{O_2}\,A\,e^{-E/(R T_f)}\right]^{-1}}, \qquad U_r = U + V_f
$$

Damkohler number at the flame leading edge: gas residence time over chemical time. $\alpha_g$ gas thermal diffusivity (m2/s); $U_r$ flow speed relative to the flame (m/s), with $U$ the imposed opposed flow and $V_f$ the spread rate; $\rho_g$ gas density (kg/m3); $Y_{O_2}$ oxygen mass fraction; $A$ pre-exponential factor of a one-step overall reaction (units such that the bracket is a rate in 1/s); $E$ activation energy (J/mol); $R$ gas constant (8.314 J/mol K); $T_f$ flame temperature (K). High-flow branch of the flammability boundary: the flame blows off when Da falls below a critical value, i.e. when $U_r$ is too large or O2 too low. On Earth the buoyant flow at the flame (about 20 cm/s for SIBAL) sets $U_r$, and downward spread over SIBAL blows off; in BASS, 9-10 cm/s opposed flow kept Da above critical, and no blow-off was reached up to about 44 cm/s. Order-of-magnitude scaling, not a fitted relation.

Textbook background
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Normal gravity studies are limited to flow speeds above the minimum buoyant speed in the flame zone (20 cm/s for this system).*
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The explanation is that in normal gravity, the buoyant flow generated by the flame is too high for the flame to be supported and blowoff occurs.*

$$
\Phi_{rad} = \frac{\dot Q_{rad}}{\dot Q_{comb}} \approx \frac{\varepsilon\,\sigma\,(T_f^{4} - T_\infty^{4})\,A_f}{\dot m_f\,\Delta h_c}
$$

Radiative-loss fraction that controls the low-flow (quenching) branch. $\varepsilon$ effective emissivity of flame and hot surface; $\sigma$ Stefan-Boltzmann constant (5.67e-8 W/m2 K4); $A_f$ radiating area (m2); $\dot m_f$ fuel pyrolysis rate (kg/s); $\Delta h_c$ heat of combustion (J/kg); temperatures in K. As the forced flow falls towards zero in microgravity, oxygen supply and heat feedback weaken, the pyrolysis rate drops faster than the radiative loss, $\Phi_{rad}$ rises towards order one and the flame quenches. Buoyancy keeps $\Phi_{rad}$ small in 1 g, so this branch is observable only in microgravity. In BASS, concurrent SIBAL flames quenched below 1 cm/s, whereas PMMA and wax flames, fed by heat stored in the thick solid, stayed lit near 1 cm/s for minutes. Qualitative scaling, not fitted to BASS data.

Textbook background
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *This quenching extinction occurs when the flame power output decreases, and the radiative heat loss rate becomes a significant fraction of the total combustion heat release from the flame.*
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The observation of the quenching extinction branch is only possible at microgravity, since otherwise any buoyant flow generated would take the system out of the low-speed flow regime.*

$$
V_F = -0.20\,U_\infty + 0.56 \qquad V_F = -0.15\,U_\infty + 0.07
$$

Linear fits reported by the investigators to the steady base spread rate of concurrent-flow flames over SIBAL fabric (ISS cabin air, about 21-22% O2, about 1 atm), one fit per sample width (1 cm and 2 cm). $V_F$ flame-base spread rate (mm/s); $U_\infty$ imposed air speed (cm/s), plotted as negative for concurrent flow, so spread increases linearly with flow magnitude. At $U_\infty = -10$ cm/s the fits give 2.56 and 1.57 mm/s. The source does not label the fits by width; the first matches the 2.55 mm/s measured on a 2-cm sample at about 10 cm/s, and the second the 1.68 mm/s base speed of a 1-cm sample at 11 cm/s, so they are most likely the 2-cm and 1-cm fits respectively. Valid only within the flows tested; not near the quenching limit below about 1 cm/s.

`PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p25): *VF = - 0.20 U∞ + 0.56 VF = - 0.15 U∞ + 0.07*
`PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Concurrent-flow flame spread rate increases linearly with flow speed, and linear curve fits are shown. Spread rate is width-dependent for the two widths studied.*
`PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p24): *Concurrent and Opposed Spread at ~ 10 cm/s 2.55 mm/s versus 1.21 mm/s*

$$
x_{base} = 1.68\,t - 13.81, \qquad x_{tip} = 1.71\,t + 2.25, \qquad L_f = x_{tip} - x_{base} \approx 16\ \mathrm{mm}
$$

Investigators' linear fits to flame-base and flame-tip position for a 1-cm-wide SIBAL sample in 11 cm/s concurrent flow on ISS (air, about 1 atm), after the initial growth phase (about 20 s). $x$ position along the sample (mm); $t$ time (s); $L_f$ flame length (mm). Base and tip advance at nearly the same speed (about 1.7 mm/s), so the flame has reached a steady (limiting) length, as predicted for purely forced concurrent flow at low speed. Valid only for this run.

`PSI-26_Presentations_Flammability Aspects of Fabric_USNationalCombustion2013.pdf` (p23): *xbase = 1.68 t - 13.81 xtip = 1.71 t + 2.25*

$$
\dot r = \frac{\dot m}{\rho_s\,4\pi r^{2}}
$$

Mean surface regression rate of a burning sphere from its mass-loss rate. $\dot r$ regression rate (m/s); $\dot m$ mean burning rate (kg/s); $\rho_s$ solid density (PMMA 1190 kg/m3); $r$ sphere radius (m). For the BASS 1-cm PMMA sphere (617.5 mg, consumed over four burns totalling 325 s at various flows), a NASA analysis gives $\dot m \approx$ 1.9 mg/s and $\dot r \approx$ 0.005 mm/s (0.3 mm/min). This is a lumped average over changing flow and a shrinking, reshaped sphere, not a local or steady value.

Textbook background
<https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *The total burn time was 5 min and 25 s (325 s). The average burning rate was 617.5/325 = 1.9 mg/s.*
<https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *1.9 mg/s ÷ 1.19 mg/mm3 ÷ 314 mm2 = 0.005 mm/s × 60 s/min = 0.3 mm/min.*

## Method

### Apparatus

The tests used the SPICE flow duct (76 mm x 76 mm cross-section), installed in the MSG, which supplied power, imaging and containment. A variable-speed fan with a flow straightener drove air through the duct at nominally 0-40 cm/s (the highest reading logged was about 44 cm/s). A hot-wire anemometer measured air speed, with a minimum measurable speed of 1 cm/s. The BASS control box let the crew turn the fan fully off, both as a safety measure and as a way to extinguish flames. Nitrogen from the MSG gaseous-nitrogen supply passed through a mass-flow controller (0-500 sccm) to a 3.2 mm nozzle upstream of the sample. Samples mounted on magnets in a sample-frame insert. Flat samples had an integral 29-gauge Kanthal wire igniter (about 1 ohm, about 3.7 A, ignition within about 2 s). Spheres, slabs and candles used bendable igniter wires that the crew positioned within about 1 mm of the fuel. Imaging was a Nikon D300s digital still camera looking through the top window at about 1 frame/s, and a colour video camera giving an edge view through the front window at 30 frames/s. A text overlay showed fan setting, air speed, radiometer output, nitrogen flow and time. A wide-angle radiometer measured flame radiation. Overlay parameters were logged at 4 Hz. In 2013 the MSG volume was vitiated with nitrogen, and the crew measured O2 with a CSA-CP (Compound Specific Analyzer - Combustion Products).

### Fuels and samples

- SIBAL cotton-fibreglass fabric (75% cotton / 25% fibreglass by mass, 18.0 mg/cm2, 60 x 40 threads per inch). Made so that the fibreglass matrix stays in place after burnout and the sheet does not curl or crack. 11 samples flown in 2 cm and 1 cm widths, 8.5 cm exposed length (solid, thin flat sheet in a stainless-steel frame, 1 or 2 cm wide x 8.5 cm, burned on both faces)
- Nomex fabrics. The SRD lists Nomex III (blend) and WSTF Nomex natural HT90-40, a 12 mil (about 0.3 mm) fire-retarded aramid. Upward limiting oxygen index (ULOI) in 1 g: 22% O2 for Nomex III and 23.5% O2 for HT90-40 (solid, thin flat sheet, 2 cm wide)
- Ultem 1000 polyetherimide (PEI) film, 10 mil (about 0.25 mm), inherently flame-retarding and charring, ULOI 23.5% O2 (solid, thin flat film, 2 cm wide)
- PMMA (polymethyl methacrylate, acrylic) spheres, 1 and 2 cm diameter. Some had an inert forward hemisphere so that only a wake flame could form behind it. 12 sphere samples, each burned several times (solid, sphere / hemisphere on a support rod, forward or wake ignition)
- Thick flat samples: 1 cm wide x 2 mm thick one-sided PMMA slab, and a fibreglass fabric slab saturated with paraffin wax (2 PMMA + 2 wax samples flown) (solid, thick one-sided flat slab)
- Candles within ceramic tubes: Japan wax and paraffin wax-impregnated wicks (8 candle samples), forward (stagnation) or wake ignition (solid, candle / wax-impregnated wick inside a tube)

### Procedure

For each run the crew installed a sample, closed the duct and the MSG, and set the fan (and nitrogen flow, if used). They started video and still recording, then energised the igniter. For flat samples, flipping the holder 180 degrees put the igniter at the upstream end (opposed flow) or the downstream end (concurrent flow). After ignition the flame was left to burn, nominally for about 60 s in the original plan. For flat samples it usually burned until the fuel was consumed. Many runs changed the flow in steps during the burn. Opposed-flow flames re-reached steady spread within seconds, so one burn could give several flow conditions; concurrent flames respond too slowly for that. In suppression runs, nitrogen was raised in steps up to the maximum (about 495-500 cc/min). Flames that survived were put out by turning the air flow off. Afterwards the duct was cooled and vented: 2 min for thin samples and candles, 9 min for spheres and thick samples. The MSG was purged for 3 min after every 2 burns to dilute hydrogen fluoride (HF), a combustion by-product. Spheres, slabs and candles were re-ignited over several runs, so their shape changed from run to run. The 2012 runs were in ISS cabin air. Before many 2013 runs the MSG volume was diluted with nitrogen to about 16-18% O2, with O2 checked by CSA-CP. The ground team directed the runs in real time over audio and video links, and the crew's verbal observations were logged in the as-run test matrix.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| forced air flow speed (imposed by fan) | <1 (fan pot near shut-off; below the 1 cm/s anemometer floor) to about 44; most runs 0-20 | cm/s |
| flow direction relative to spread | concurrent, opposed (flat samples); forward-stagnation vs wake ignition (spheres, candles) |  |
| ambient oxygen (MSG volume) | 0.209-0.227 in 2012 (ISS cabin air, not controlled); 0.159-0.212 in 2013 (MSG vitiated with N2 for most runs) | mole fraction |
| fuel material and geometry | SIBAL fabric, Nomex (2 types), Ultem film, PMMA sphere/hemisphere, PMMA slab, wax slab, Japan-wax and paraffin candles |  |
| sample size | flat width 1 or 2 cm; sphere diameter 1 or 2 cm | cm |
| nitrogen suppressant flow from upstream nozzle | 0 to about 500 (logged maximum 495) | sccm (cc/min) |

Held constant:

- pressure (ISS cabin): 0.97-1.009 atm (98.3-102.2 kPa) over all logged runs
- flow duct: SPICE duct, 76 mm x 76 mm cross-section
- fabric sample length and areal density: 8.5 cm exposed length; 18.0 mg/cm2
- minimum O2 requirement (planned): SRD restricted testing to >= 21% O2; the 2013 vitiated runs departed from this

Number of tests: 121

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame base and tip position vs time, giving flame spread rate and flame length | digital still camera (top view, about 1 frame/s) and edge-view video (30 frames/s) | derived |
| flame shape, colour (blue vs sooty yellow), symmetry, smouldering, vapour jetting | still and video cameras; crew direct observation | direct |
| air flow speed in duct | hot-wire anemometer (overlay); fan setting / potentiometer for sub-1 cm/s flows | direct |
| flame radiation (visible to near-IR) | wide-angle radiometer in duct | direct |
| nitrogen suppressant flow rate | mass-flow controller display (overlay) | direct |
| flow condition at extinction (quenching, blow-off, N2 extinguishment, or burnout) | video/stills plus logged fan and GN2 settings | derived |
| PMMA sphere burning (regression) rate, flame standoff distance, flame growth rate | contrast-enhanced still images | derived |
| cabin / MSG O2 fraction, pressure, CO2 for each run | ISS environment readings and CSA-CP (logged in as-run matrix) | direct |

## Findings

1. In opposed flow in microgravity (2-cm-wide SIBAL cotton-fibreglass fabric, ISS air, about 21-22% O2, about 1 atm), the flame reached steady spread within seconds of each flow change. Spread rate rose with flow to a maximum at about 10-15 cm/s and fell at higher speeds. *(trend, high)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Opposed-flow flame spread rate increases with flow to a maximum when the flow speed is around 10 to 15 cm/s and then decreases at higher speeds, in good agreement with previous research [Olson, 1991].*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel rows 58-59 and 70-71, as-run 54, 55, 65, 66 (SIBAL), columns 'O2 % by volume' and 'pressure, atm': *O2 0.2272, 0.2267, 0.2152, 0.2158; pressure 0.995, 1.004, 0.991, 0.991 atm*
2. The same SIBAL fabric cannot sustain downward (opposed-flow) spread in 1 g air: it ignites, then extinguishes, because the buoyant flow exceeds the blow-off limit. In microgravity at about 9-10 cm/s opposed flow it burned steadily over the whole sample. For this fabric and geometry, it is more flammable in microgravity than in 1 g, which supports the BASS hypothesis. *(result, high)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The fuel used in this investigation cannot burn in the downward (opposed-flow) configuration in normal gravity.*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The explanation is that in normal gravity, the buoyant flow generated by the flame is too high for the flame to be supported and blowoff occurs.*
   - `PSI-26_Presentations_Flammability Aspects of Fabric_USNationalCombustion2013.pdf` (p26): *Note: Downward flame spread (opposed flow) in 1-g with this material is not possible in normal air.*
3. In concurrent flow, the base spread rate of SIBAL flames was constant within each run and increased linearly with flow speed, with different slopes for 1-cm and 2-cm widths. The plotted linear fits are V_F = -0.20 U + 0.56 and V_F = -0.15 U + 0.07 (V_F in mm/s, U in cm/s, concurrent flow plotted as negative U). The extracted text does not say which fit belongs to which width, but at 10-11 cm/s the first fit reproduces the 2.55 mm/s measured on a 2-cm sample and the second the 1.68 mm/s base speed of a 1-cm sample, so the steeper fit is most likely the 2-cm width. *(trend, medium)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Concurrent-flow flame spread rate increases linearly with flow speed, and linear curve fits are shown. Spread rate is width-dependent for the two widths studied.*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p25): *VF = - 0.20 U∞ + 0.56 VF = - 0.15 U∞ + 0.07*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p24): *Concurrent and Opposed Spread at ~ 10 cm/s 2.55 mm/s versus 1.21 mm/s*
   - `PSI-26_Presentations_Flammability Aspects of Fabric_USNationalCombustion2013.pdf` (p23): *xbase = 1.68 t - 13.81 xtip = 1.71 t + 2.25*
4. Concurrent-flow SIBAL flames reached a steady (limiting) length only below about 10 cm/s for the 2-cm-wide samples within the 8.5 cm sample length. At 10 cm/s and above, the flame tip was still accelerating. 1-cm-wide samples reached steady state, e.g. at 11 cm/s: after about 20 s, base and tip advanced in parallel at about 1.7 mm/s (fits x_base = 1.68 t - 13.81, x_tip = 1.71 t + 2.25, mm and s), with a flame length of about 16 mm. *(result, high)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *However, only air flows less than 10 cm/s yield steady flame lengths.*
   - `PSI-26_Presentations_Flammability Aspects of Fabric_USNationalCombustion2013.pdf` (p23): *xbase = 1.68 t - 13.81 xtip = 1.71 t + 2.25*
5. Quenching (low-flow) extinction of a concurrent-flow SIBAL flame was observed when the flow was reduced in steps from 5 to about 1 cm/s. Extinction occurred at a low but finite flow below 1 cm/s. The authors present this as direct confirmation of the low-flow branch of the U-shaped flammability boundary for a thin fuel. *(limit, high)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *For concurrent flow, extinction was observed at a low but finite flow speed of less than 1 cm/s (shown by the dashed vertical line).*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *5 | 2 | Concurrent | 5, 3, 1.5, 1 | Flow reduction; quenching extinction observed*
6. No opposed-flow quenching limit was reached: a 2-cm SIBAL flame stepped down from 10 to about 1 cm/s kept burning until the fuel ran out. The authors extrapolate an opposed-flow quenching limit below 1 cm/s, implying a narrow band of near-zero flow in which neither opposed nor concurrent spread is sustained. No blow-off limit was reached either: flames survived opposed and concurrent flows up to about 44 cm/s. *(limit, medium)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *Based on the trends however, it appears that an opposed-flow quenching extinction limit can be extrapolated to exist at an air flow speed of less than 1 cm/s.*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *3 | 2 | Opposed | 10, 20, 44 | Flow increase; blowoff extinction not attained*
7. At about 10 cm/s on 2-cm SIBAL, the concurrent-flow flame was longer than the opposed-flow flame and spread about twice as fast: 2.55 vs 1.21 mm/s. *(result, high)*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p24): *Concurrent and Opposed Spread at ~ 10 cm/s 2.55 mm/s versus 1.21 mm/s*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The concurrent-flow flame is longer and spreads twice as fast as the opposed-flow flame.*
8. Compared with a 1 g upward (concurrent) flame on the same fabric, the microgravity concurrent flame had a convex base and nearly reached a steady state. The 1 g flame was much longer and sootier, had a concave base, and was still accelerating at the end of the sample. *(result, high)*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The microgravity flame has a convex base and nearly reaches a steady-state condition.*
   - `PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx` (all): *The normal-gravity flame is much longer, sootier, has a concave base, and is still accelerating over the fuel length available.*
9. Ultem film and Nomex HT90-40 fabric did not burn in microgravity at 21-22% O2 and about 15 cm/s, similar to their 1 g behaviour. For these fire-retarded materials, microgravity was not more severe at those conditions (the ISS samples were narrower than 1 g test samples). A Nomex III sample did burn at 22% O2 and about 14-15 cm/s concurrent flow, which equals its 1 g ULOI. Its flame narrowed as it spread and went out within 1 cm of the sample end once its width fell below about 1 cm. *(result, medium)*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p30): *Results: Ultem and Nomex HT90-40 samples did not burn on ISS atmosphere 21% to 22% O2 Flow speeds around 15 cm/s Similar to 1-g (Note: samples narrower on ISS) Nomex-III sample did burn*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p31): *Flame was shrinking in width until it extinguished within 1 cm of the end of the sample, as its width became smaller than ~ 1 cm, which is on the scale of a fingering flamelet.*
10. Nitrogen from the upstream nozzle at up to about 500 cc/min generally failed to extinguish PMMA sphere flames in air or at 17% O2. It typically blew off the forward-stagnation region (leading edge), and the flame survived as a side- or wake-stabilised flame. The crew log attributes this to the jet entraining air into the flame zone. These flames went out only when the air flow was shut off. The as-run log records clear N2 blow-out only occasionally, e.g. a 2-cm sphere at 5 cm/s, and a weakened minimum flame at max N2 that eventually went out. In their 2013 summary the investigators attribute the failure to heat stored in the thick solid, which kept even small flames alive at the available N2 flow. *(result, medium)*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx` (sheet 2012): *N2 on at 1 minute. Blew off stagnation region but N2 did not extinguish wake, even with air flow off.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx` (sheet 2012): *Only extinguishes when all flow stops. N2 is entraining air to flame zone.*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p57): *PMMA sphere burning in wake configuration in air. Flow is from right to left Nitrogen flow of 500 cc/min weakens but does not extinguish the flame*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p56): *Near the end of the burn, a jet of nitrogen is imposed but it fails to extinguish the flame. Finally after a series of flow reductions, the flame goes out when the flow speed is zero.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 66, as-run 62 (2-cm PMMA sphere, fan 45, air 5 cm/s), column 'Test Observations and Anomalies': *flame did blow out with GN2 at about a pot 6.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 57, as-run 53 (2-cm PMMA sphere, wake ignition), column 'Test Observations and Anomalies' (excerpt): *GN2 on max did not blow it out right away, but did eventually extinguish it. LE blew off and ring flame stabilized for a number of s.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 64, as-run 60 (2-cm PMMA sphere), column 'Test Observations and Anomalies' (excerpt): *Did not blow out either at high flow or with GN2 although stagnation region blew out.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 65, as-run 61 (2-cm PMMA sphere), column 'Test Observations and Anomalies': *try blowing out the flame with GN2. blew out bottom half, but not top half. Could see where the leading edge gradually blew out with incre GN2*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 21, as-run 91 (2-cm PMMA sphere, O2 0.1753), column 'Test Observations and Anomalies': *Ign took 2 min, flame on top half. Used GN2 to try and blow out at low flow. No joy even at max GN2. Extinguished when flow off.*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *Thicker solids can store a great deal of heat even with only a small flame. One result is that extinction with the nitrogen jet was not possible for the given flow rate.*
11. Thick and low-oxygen fuels sustained small, dim, all-blue flames at very low flow for long periods. A 1-cm-wide PMMA slab in air at about 7-9 cm/s held a steady flame about 1 cm in size for minutes, spreading only about 1 cm, and went out only when the air was shut off. PMMA spheres and paraffin candles at about 17% O2 burned at flows below 1 cm/s and extinguished at a finite, very low flow or when the flow was stopped (a 2-cm sphere in 20.5% O2 behaved the same way). *(result, medium)*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p54): *The flame is about 1 cm in size and can persist for a very long time at this low air flow speed. The flame goes out only in the last two frames when the air flow is completely shut off.*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p59): *Image sequence of a burning paraffin wax candle within a ceramic tube at 17% oxygen and less than 1 cm/s flow.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 81, as-run 76 (PMMA slab, fan 67/60, air 9/7 cm/s, O2 0.219), column 'Test Observations and Anomalies' (excerpt): *Reached a steady size and spread downstream very slowly, all blue flame. Top stills look like about 1 cm long flame with curved base and slightly curved tail, mostly oval. All blue with intermittent yellow streaks. Very stable. Spread maybe 1 cm?*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 82, as-run 77 (PMMA slab, air 9 cm/s), column 'Test Observations and Anomalies' (excerpt): *Let it burn for 8 minutes, got 294 images all blue lopsided oval, longer than previous run. Spread maybe 1 cm*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 28, as-run 98 (2-cm PMMA sphere, O2 0.1734), column 'Test Observations and Anomalies' (excerpt): *2nd vitiation, got it ignited, burned just on forward stagnation region, minimal spread. Went out at finite flow.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 22, as-run 92 (2-cm PMMA sphere, O2 0.205), column 'Test Observations and Anomalies': *Ign in 1 min. Symmetric growth. Gets sooty, even when flow reduced to 41. Gets all blue at 18:38, out at 18:40 at finite extremely low flow.*
12. Ignition was markedly harder in vitiated air. In 2013 at about 17% O2, 2-cm PMMA spheres needed 1.5-4 min of igniter heating; a 2-cm sphere at 20.5% O2 ignited in about 1 min. A paraffin wax slab at 16.3% O2 held a blue flame wrapped around its leading edge without spreading, and went out on its own after 75 s. One-sided PMMA slabs in opposed flow (air, 9 and 15 cm/s) could not sustain a flame after the igniter was retracted. These are crew/PI log observations, not reduced measurements. *(null_result, low)*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx` (sheet TP without Data): *new sample. Blue flame wrapped around leading edge, didn't propagate at all. Went out on its own at a flow of 0.4 after 75 seconds*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 35, as-run 105 (2-cm PMMA sphere, O2 0.172), column 'Test Observations and Anomalies' (excerpt): *takes 4 min to ignite sphere at this O2.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 38, as-run 108 (2-cm PMMA sphere, O2 0.1717), column 'Test Observations and Anomalies' (excerpt): *new igniter, anneal it. 3 min to ignite,*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 39, as-run 109 (2-cm PMMA sphere, O2 0.1717), column 'Test Observations and Anomalies' (excerpt): *Ignition in 1.5 min.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 22, as-run 92 (2-cm PMMA sphere, O2 0.205), column 'Test Observations and Anomalies' (excerpt): *Ign in 1 min.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 26, as-run 96 (PMMA slab, opposed, air 9 cm/s, O2 0.21), column 'Test Observations and Anomalies' (excerpt): *Apparently not flammable in opposed flow for the same concurrent flow.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 27, as-run 97 (PMMA slab, opposed, air 15 cm/s, O2 0.21), column 'Test Observations and Anomalies' (excerpt): *Got a flame briefly, but did not sustain for any spread, shrank and winked out after maybe 15 s or so.*
13. The ISS imagery was used to test a comprehensive transient model of a burning PMMA sphere with solid-surface regression (CWRU; 2-cm acrylic sphere, 17% O2, 1 atm, 12 cm/s). The model captured the flame qualitatively. The authors note that adjusting the solid-phase kinetic parameters should improve the predicted flame standoff distance. Cost: 2.7 h of computing per simulated second on a 33,930-point mesh. *(method, medium)*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p51): *Adjusted solid phase chemical kinetic parameters will improve the prediction of the flame standoff distance. Fuel: Acrylic sphere; Atmosphere: 17% O2/N2; 1 atm; Flow speed: 12 cm/s (left to right)*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p37): *it takes 2.7 hours to compute one second in the computation*
14. Wax candles (wick in a ceramic tube) burned for long periods at near-zero flow and resisted the nitrogen jet. In ISS air (21.2% O2, about 0.97 atm), a Japan-wax candle ignited in the wake configuration burned for about 10 min as the fan was stepped down, held a steady flame at fan potentiometer setting 0.32 and went out each time at 0.31, a setting below the 1 cm/s anemometer floor. With nitrogen applied at each flow setting, another Japan-wax candle persisted for a long time as a dim all-blue flame and went out only when the fan was switched off. In the 2013 vitiated runs a Japan-wax candle burned for a long time at 1-2 cm/s in 15.9% O2, the lowest O2 logged in BASS, and a paraffin candle at about 16.8% O2 held a steady all-blue flame. A leftover BASS candle burned later in BASS-II ejected a wax droplet directly upstream, which the investigators cite as the droplet-ejection hazard of melting fuels. These are crew and PI log observations; no reduced candle data (flame size, burning rate, limiting flow speed) were found in PSI or externally. *(result, medium)*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 76, as-run 71 (Japan-wax candle, wake, O2 0.2124), column 'Test Observations and Anomalies': *P mode is auto-everything. Very long burn (~ 10 min), waited at every flow condition, steady radiometer at 0.32 pot ~ 2.2 (lowest for flame). Consistenly goes out at pot 0.31*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2012, row Excel row 79, as-run 74 (Japan-wax candle, wake, GN2 'multi'), column 'Test Observations and Anomalies': *Turned on N2 at each flow setting starting at 0.35, not at 0.31. At 0.31, flame persisted for a long time, went out when fan off (38). All blue and dim. 2 frames shy of 13 brackets/*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 19, as-run 89 (Japan-wax candle, O2 0.159), column 'Test Observations and Anomalies': *LONG candle burn at very low flow rates. Sooty at 2 cm/s and then at 1 cm/s. All blue at fan41. Candle out at flow change.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 14, as-run 87 (paraffin candle, wake), column 'Test Observations and Anomalies' (excerpt; the O2 column logs the pre-vitiation 0.21111): *new candle, started GN2 at 15:26 00 gmt 15:31:10 msg stopped gmt 17:20:20, O2 16.8%.*
   - `PSI-26_Science Documents_As Run_Test Matrix.xlsx`, sheet 2013, row Excel row 14, as-run 87, column 'Test Observations and Anomalies' (excerpt): *At 41 (pot 0.4), flame was steady all blue.*
   - `PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf` (p59): *Image sequence of a burning paraffin wax candle within a ceramic tube at 17% oxygen and less than 1 cm/s flow.*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *A secondary objective was to burn any unused Burning and Suppression Solids—I (BASS–I) samples, of which there was a single wax candle.*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *The ejected wax droplet shown in Figure 3.1(b) typifies the flame spread hazard associated with melting plastics in microgravity.*
15. The investigators' 2013 summary across all BASS sample types (17% to 21.5% O2, about 1 atm) is that flames were especially sensitive to air speed between 0 and 5 cm/s, and that the gas phase responded to flow changes almost without delay. Below 1 cm/s all flames became dim blue and very stable and, with little convective heat loss, could burn for a long time. Between about 1 and 5 cm/s the flame kept heating the solid, so fuel vaporisation rose and the flame grew stronger and more luminous with time. Only the smallest flames over acrylic slabs were visibly weakened by conductive loss to the solid, and even these burned for over 5 minutes before self-extinguishing. *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *Ambient oxygen atmospheres 17% to 21.5% (cabin air).*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *Microgravity flames were found to be especially sensitive to air flow speed in the range 0 to 5 cm/s.*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *At the lowest speeds examined (less than 1 cm/s) all the flames tended to become dim blue and very stable. However, heat loss at these very low convective rates is small so the flames can burn for a long time.*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *At moderate flow speeds (between about 1 and 5 cm/s) the flame continually heats the solid fuel resulting in an increasing fuel temperature, higher rate of fuel vaporization, and a stronger, more luminous flame as time progresses.*
   - <https://ntrs.nasa.gov/api/citations/20140011099/downloads/20140011099.pdf>: *Only the smallest flames burning acrylic slabs appeared to be adversely influenced by solid conductive heat loss, but even these burned for over 5 minutes before self-extinguishing.*
16. NASA's BASS-II summary report gives numbers for two BASS thick-fuel runs. A one-sided, 1-cm-wide PMMA slab burned at slow flow for 7.5 min in total: ignition took over 1 min, the flame reached a steady size after about 3 min, was only 15 mm long, and spread at 0.037 mm/s (2.2 mm/min). A 1-cm PMMA sphere (initial mass 617.5 mg) was fully consumed in four burns at various flow speeds totalling 325 s. That is an average burning rate of 1.9 mg/s, which the report converts to a mean regression rate of about 0.005 mm/s (0.3 mm/min), equivalent to a stretch rate of about 10 1/s. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *The 1-cm-wide sample took 7.5 min for the total test time, with the ignition taking over 1 min. Flame reached steady size in about 3 min and was only 15 mm long. The spread rate was 0.037 mm/s (0.0037 cm/s or 2.2 mm/min).*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *The BASS 1-cm sphere had an initial mass of 617.5 mg. Sample 19 (1-cm PMMA sphere) was completely consumed in four tests (various high- and low-flow speeds)*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *The total burn time was 5 min and 25 s (325 s). The average burning rate was 617.5/325 = 1.9 mg/s.*
   - <https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf>: *Note this is 0.0005 cm/s, which is equivalent to a stretch rate of 10*

## Fire-safety relevance

Prevention and material selection: BASS shows directly that a material which self-extinguishes in the 1 g downward configuration can burn steadily in microgravity at realistic cabin ventilation speeds (about 10 cm/s). Flames over thin and thick fuels can also persist for minutes at flows of 1 cm/s or less. Normal-gravity screening therefore does not bound flammability in all configurations. On the other hand, the fire-retarded Ultem and Nomex HT90-40 behaved as in 1 g at 21-22% O2, and Nomex III burned only near its 1 g limiting O2. So the 1 g upward test was not shown to be non-conservative for the fire-retarded materials actually tested. These are qualitative, few-sample results at about 1 atm, not material flammability limits. Suppression: a nitrogen jet of up to about 500 cc/min from a fixed upstream nozzle generally removed only the leading edge of PMMA flames. Wake- and side-stabilised flames survived, apparently helped by air entrained by the jet, while shutting off the ventilation reliably extinguished small flames. This supports stopping ventilation as an effective response to small flames, and suggests the agent must reach the whole flame zone, including wake regions, not only the leading edge. The nozzle geometry and flow are specific to this hardware, so the agent quantities do not transfer to ISS extinguishers.

### Habitat conditions

All runs were at ISS cabin pressure: 0.97-1.01 atm (98.3-102.2 kPa). In 2012, O2 was the uncontrolled cabin value, 20.9-22.7% by volume. In 2013 the MSG volume was diluted with nitrogen to 15.9-17.8% O2 for most runs; the rest were at about 20.5-21.2%. The logged O2 is sometimes the reading before vitiation, so a few 2013 runs logged near 21% actually burned at about 17%. BASS therefore covers normoxic and hypoxic (sub-21% O2) atmospheres at about the Earth sea-level reference (20.9% O2 at 101.3 kPa) only. It did not test the elevated-O2, reduced-pressure atmospheres of exploration: the shared reference for a Moon habitat is 30% O2 or more at 70.3 kPa (10.2 psi) or less, and a spacesuit is 100% O2 at 29.6 kPa (4.3 psi). Its highest O2 (22.7%) is below the Moon-habitat value, and its lowest pressure (98.3 kPa) is well above it. The SRD cites NASA CxP-70024 for such atmospheres but gives no values. BASS results cannot be applied to them without further tests or models. The flow range (below 1 to about 44 cm/s, mostly 0-20 cm/s) does span typical spacecraft ventilation speeds and the near-quiescent pockets behind equipment.

### Earth benefits

Microgravity's simple, buoyancy-free flow field gives clean validation data for detailed flame-spread and extinction models. Once validated, these models can be extended to buoyant flames and used in designing fire detection and suppression systems on Earth. The team also cites the goal of a new or improved Earth-based flammability test method.

## Limitations

- Very few samples per condition. There were 11 SIBAL samples (with flow stepped during burns), 1-2 samples each of Nomex, Ultem and the thick slabs, and spheres and candles re-ignited repeatedly, so the fuel shape and size changed between runs. Repeatability is largely unassessed.
- Short fabric samples (8.5 cm) were too short for concurrent flames at 10 cm/s and above to reach steady length, so limiting-length data exist only for low flows.
- Flow near extinction is poorly quantified. The anemometer floor is 1 cm/s, so the lowest flows are recorded only as fan display or potentiometer settings (e.g. 'pot 0.31'), and converting them needs the on-orbit fan calibrations. The fan also showed hysteresis.
- O2 was not a controlled variable. In 2012 it drifted with the cabin (20.9-22.7%). In 2013 it was set by bleeding N2 into the MSG volume and drifted during sessions (e.g. 17.07% to 17.3%), measured by a hand-held CSA-CP. The original requirement was O2 >= 21%. The O2 column is sometimes the reading taken before vitiation: as-run 86 and 87 log 21.1% while their notes give 17.3% and 16.8% after N2 dilution, so the logged O2 must be read together with the notes.
- Frequent hardware problems broke up many runs: igniter breakage (up to 4 igniters broken in one session), lens cap left on, a camera not triggered, loss of signal, and inconsistent camera settings. Several runs produced no usable still images.
- The suppression results are specific to one geometry: a 3.2 mm nozzle upstream of the sample, a maximum of about 500 sccm N2, and a small enclosed duct. Duct walls and the sample holder (e.g. the metal frame around the PMMA slab) add heat loss and flow effects not present in an open cabin.
- The microgravity vs 1 g Nomex/Ultem comparison used narrower samples on ISS than in 1 g testing, and the 1 g fabric comparisons are qualitative, image-based comparisons.

## Data in PSI

PSI-26 holds 212 files (163.6 GB). Almost all of it (195 files, 162.5 GB) is raw imagery that has not been downloaded: 22 zips of 2012 still images (85.1 GB), and for 2013, 114 crew/downlink MP4 videos (22.8 GB) plus 37 zips (55.6 GB) of original images, XMP sidecars and text files. Raw data are organised by date. The data layout document describes 21 image galleries for 2012, and 12 audio/video collections plus 15 image galleries for 2013. No reduced data (spread rates, extinction points, digitised positions) are in PSI. Quantitative results exist only as plots and captions in the presentations and the 2013 US National Combustion Meeting paper. The most useful structured source is the as-run test matrix (xlsx). For each run it logs date and time, sample, igniter, fan and air settings, radiometer, GN2 setting, camera settings, cabin O2, pressure and CO2, and free-text crew/PI observations (outcome, extinction mode, soot). It links each run to its date folder in the raw data. The PSI experimental table CSV is a 6-column extract of it. No raw-data date folder exists before 2012-05-02, so the first 8 as-run tests (2012-03-30 to 2012-04-09) appear to have no imagery in PSI. Both final reports (BASS and SPICE) are listed but were not downloaded.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | 2012 test-day still-image archives (orig zips), one per date folder | .zip | 22 | 85.1 GB | no |
| Raw Data | 2013 test-day video (crew and downlink MP4) | .mp4 | 114 | 22.8 GB | no |
| Raw Data | 2013 test-day image archives: 13 orig zips (55.6 GB), 14 XMP sidecar zips and 10 txt zips | .zip | 37 | 55.6 GB | no |
| Science Documents | Science Requirements Document (Feb 2010), PSI data layout document, planned and as-run test matrices (xlsx), 2013 US National Combustion Meeting paper (docx) | .pdf .xlsx .docx | 5 | 9.9 MB | yes |
| Presentations | ASGSR 2012 and USNCM 2013 fabric talks, ISS R&D 2013 overview of results, BASS overview, crew training 2010/2011 | .pdf .pptx | 6 | 15 MB | yes |
| Engineering Documents | BASS engineering requirements, SLICE/BASS system acceptance reviews (SAR-1, SAR-2), a SLICE design review, and 20 sample/hardware drawings with no text layer | .pdf .pptx | 24 | 13.8 MB | yes |
| Reports | BASS and SPICE final reports (not downloaded; identical byte size) | .pdf | 2 | 1.1 MB | no |
| Experimental table | 121-run list: date, GMT day, as-run no., test no., sample no., material | .csv | 1 | 4.7 kB | yes |
| metadata | ISA-Tab investigation metadata (zip file name says PSI-102, content is PSI-26) | .zip | 1 | 11.6 kB | yes |

Rows in the unified `tests` table: 121

## Related investigations

- [PSI-25](PSI-25-bass-ii.md): follow-on
- [PSI-107](PSI-107-spice.md): shared hardware
- [PSI-106](PSI-106-slice.md): shared hardware
- [PSI-62](PSI-62.md): ground re-analysis

## Open questions

- Digitise flame base/tip positions from the 2013 vitiated-O2 imagery (spheres, candles, slabs at 16-18% O2) to give spread and regression rates. Only captions and model comparisons for single cases are published in PSI.
- Convert the logged fan potentiometer settings at extinction into flow speeds using the on-orbit fan calibrations. This would give a quantitative low-flow quenching limit vs O2 for PMMA spheres, candles and fabric, i.e. an extinction boundary map.
- OCR the video overlay (fan, air speed, radiometer, GN2, time) from the 2013 MP4s to build per-run time series of flow, radiometer signal and N2 flow, synchronised with flame images.
- Tabulate nitrogen-suppression outcomes systematically (stagnation-region blow-off, wake survival, extinction) against air flow, N2 flow, sphere size and O2 from the as-run log and imagery.
- Compare the opposed- vs concurrent-flow SIBAL spread rates with thermal-regime and boundary-layer correlations (e.g. the Bhattacharjee papers listed in the record), and with the transient concurrent-flame growth model mentioned as under development.
- Quantify soot onset (blue to yellow transition) vs flow and O2 for PMMA spheres from the bracketed still images.

## Dashboard ideas

- **spread rate vs signed flow speed** (`flow_cm_s (negative = concurrent)`, `spread_rate_mm_s`, `sample_width_cm`, `direction`): Reproduces the key BASS plot: opposed peak at 10-15 cm/s, linear concurrent trend, concurrent quenching below 1 cm/s.
- **run timeline and outcome table** (`date`, `as_run_no`, `sample_no`, `material`, `x_o2`, `pressure_atm`, `outcome (spread / no ignition / quench / N2 extinguished / air-off)`): Lets a user filter the 121 logged runs by material, year and O2 and see which have raw imagery.
- **extinction boundary map** (`x_o2`, `flow_cm_s_at_extinction`, `fuel_geometry`, `extinction_mode`): Places BASS low-flow extinctions (air and about 17% O2) against the U-shaped flammability boundary sketched in the presentations.
- **suppression outcome matrix** (`fuel_geometry`, `ignition_side (forward/wake)`, `air_flow_cm_s`, `n2_sccm`, `result`): Shows at a glance that nozzle N2 rarely extinguished PMMA flames while shutting off flow did.

## Gaps and data-quality notes

- Final reports (PSI-26_Reports_BASS_FinalReport.pdf and PSI-26_Reports_SPICE_FinalReport.pdf) are listed in files.csv but not downloaded, and have no evidence chunks; the BASS final report is reported as unavailable from PSI (HTTP 404; not re-tested here). Both have the identical size of 553,693 bytes, so the 'BASS' report may be a duplicate of the SPICE report. To fill the gap, NTRS was searched: the ASGSR 2013 BASS talk (ntrs.nasa.gov 20140011099) and the BASS-II summary report NASA/TM-20210011385 (Appendix D gives BASS slab and sphere numbers; section 3.1 the leftover BASS candle) were used. The 9th USNCM 2015 fabric paper (ntrs.nasa.gov 20150008962) was read but reports mainly BASS-II runs, so it was not used for BASS findings.
- No reduced numerical data (spread-rate tables, extinction flow speeds, sphere regression rates) are in PSI. Quantitative findings are limited to the fabric paper and its plot labels, plus one slab spread rate and one lumped sphere burning rate from NASA/TM-20210011385. For candles, nitrogen suppression and the 2013 low-O2 runs there are only image captions and as-run log notes. Searches of NTRS, Crossref and the web found no published BASS sphere, candle or nitrogen-suppression results: Takahashi et al., 'Burning Characteristics of Paraffin and Japan Wax Candle Flames in a Low-Speed Oxidizing Stream in Microgravity' (ASGSR 2013), Endo et al. PMMA-sphere papers (ASGSR 2014, 2016) and M. Endo's 2016 CWRU dissertation are cited in the TM but no accessible copy was found. The DOIs in the PSI record are mostly BASS-II or ground opposed-flow papers and add nothing on these topics.
- The evidence parquet holds only the first rows of each As Run_Test Matrix.xlsx sheet. The full sheets were read directly from the xlsx, and facts from other rows are cited as psi_table sources with the Excel row number, as-run number and exact cell text (or an exact excerpt of it).
- The extracted text does not assign the two concurrent-flow linear fits (V_F = -0.20U + 0.56, -0.15U + 0.07) to the 1-cm and 2-cm widths. The assignment given (steeper fit = 2 cm) is inferred from single-run values and should be confirmed from the figure.
- Exploration-atmosphere values (O2 and pressure) are not given in any PSI-26 document; the SRD only cites NASA CxP-70024. The habitat comparison uses the shared values in docs/digest/reference.md.
- Data quality: the PSI-26_Science Documents_Planned_Test Matrix.xlsx header row contains what appear to be account names and passwords (not reproduced here). It should be flagged to the PSI curators.
- Data quality: the metadata zip is named 'PSI-26_metadata_PSI-102_BASS.zip', but PSI-102 is SAME (Smoke and Aerosol Measurement Experiment). Its content is the PSI-26 record.
- Data quality: the PSI record misspells Co-I Fumiaki Takahashi as 'Funiaki' and gives his affiliation as CWRU, while the presentations say NCSER. The 'approach' field is garbled ('measuring were used') and mentions 'cylinders', which appear in no other document (the candles-in-tubes are presumably meant).
- Data quality (experimental table CSV): date typos ('6/29/`12', '5/15/2103'); GMT day 113 given for 4/26/2013 (should be 116) and 137 for 6/1/2013 (should be 152; the as-run sheet's own 'GMT 150' for the following rows is also inconsistent with 6/1); as-run numbers 24, 85 and 89-91 reused for different runs; one non-test 'SOOT Cleaning' row; sample labels in 2013 ('PMMA 2 cm') omit 'sphere'.
- Data quality: Nomex naming is inconsistent. The SRD lists 'Nomex III (Blend)' and 'WSTF Nomex Natural (HT90-40)'. The as-run log uses 'Nomex blend 2 cm' and 'Nomex III Natural' / 'nomex natural III', and the 2013 overview says HT90-40 did not burn but Nomex III did. Which physical fabric burned (as-run 38, sample 29) is ambiguous.
- Data quality: the 2012 ASGSR talk captions the 1-cm concurrent case as 10 cm/s and the 2013 talk and paper as 11 cm/s, with identical fit equations.
- Raw-data coverage: no raw-data folder predates 2012-05-02, so imagery for as-run tests 1-8 (2012-03-30 to 2012-04-09) appears to be absent from PSI-26. The as-run 'Data without TP' sheet lists 2014 data folders (likely BASS-II, PSI-25) that are not among PSI-26 files. A 2013-07-09 raw folder falls after the last logged test (2013-06-01).
- The PSI-26 file set includes engineering documents for SLICE (PSI-106), e.g. PSI-26_Engineering Documents_SLICE_SysReqDesignReview.pdf, and SPICE drawings. These were not used except to confirm the shared hardware.
- Twenty engineering drawings have no text layer and were skipped, as instructed; none is a report.
- Data quality (external): NASA/TM-20210011385 Appendix D gives the BASS 1-cm sphere regression rate as 3.05 mm/min in section D.5 but derives 0.3 mm/min (0.005 mm/s) from the same data in section D.7; the arithmetic supports 0.3 mm/min, which is the value used here.
- Data quality (external): NASA/TM-20210011385 says BASS-II was the first ISS use of nitrogen dilution of the MSG volume, but the PSI-26 as-run log and the 2013 BASS talk show BASS runs vitiated to about 16-17% O2 in 2013. The 2013 vitiated runs are treated here as BASS, following PSI.
- Data quality: in the 2013 as-run sheet the 'O2 % by volume' column sometimes holds the reading before vitiation (as-run 86 and 87 log 0.21111, while their notes give 17.3% and 16.8%). Run-level O2 should be taken from the notes where they disagree.
- No text addressed to an AI or unrelated instructions were found. One editorial reviewer comment remains in the 2010 crew training deck ('Are CLD or ACME the approved names?').
- The as-run sheet's 'TP without Data' tab says 'NO DATA FOR ANY TESTPOINTS IN 2012'. This reads as 'no 2012 test points lack data', which conflicts with the missing March-April 2012 folders. The intent is unclear.
