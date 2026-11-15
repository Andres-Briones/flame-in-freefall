# PSI-98: SAFFIRE-I (Spacecraft Fire Safety Experiment-I (Saffire-I))

NASA lit a 94-cm-long sheet of cotton-fibreglass fabric inside an empty cargo spacecraft after it left the ISS, the first large fire deliberately set in orbit, to see whether a fire in microgravity keeps growing or settles to a steady size.

Investigators: David L. Urban (PI; NASA GRC); Gary A. Ruff (Saffire project; NASA GRC); Paul V. Ferkul, Sandra L. Olson, John Easton (NASA GRC science team); International Fire Safety in Space Topical Team (ESA-assembled), incl. James S. T'ien and Ya-Ting T. Liao (Case Western Reserve University), A. Carlos Fernandez-Pello, Jose L. Torero, Guillaume Legros, Christian Eigenbrod, Nickolay Smirnov, Osamu Fujita, Sebastien Rouvreau, Balazs Toth, Grunde Jomaas

## At a glance

| | |
|---|---|
| Platform | Orbital ATK Cygnus OA-6 Pressurized Cargo Module (uncrewed), operated in free flight after unberthing from the ISS |
| Facility | Saffire flow unit (flow duct plus avionics bay, about 53 x 90 x 133 cm) strapped in the Cygnus PCM |
| Dates | 2016-03-22 to 2016-06-19 |
| Fuels and samples | SIBAL cotton-fibreglass fabric |
| Varied | flow direction relative to spread: concurrent (S1, ignition at upstream edge) and opposed (S2, ignition at downstream edge, over the ~10 cm left after S1) |
| Number of tests | 2 |
| Fire-safety pillars | fundamental, prevention, detection |

## Question

Saffire-I asked two questions. (1) How rapidly does a large fire grow in low gravity, and does flame spread over a large, realistic piece of fabric reach a steady spread rate and a limiting flame size, or keep accelerating as upward fires do on Earth? (2) How do low-g flammability limits compare with NASA's normal-gravity material screening test (NASA-STD-6001 Test 1)? Saffire-I addressed the first; Saffire-II (PSI-99) addressed the second. The motivation is that all earlier microgravity flame-spread tests used samples no larger than about 10 cm in length and width, in small chambers, while a real spacecraft fire would be much larger. Designers have therefore relied on terrestrial fire data and standards, which carry large uncertainty for missions far from Earth. Full-scale fire tests had never been possible in a crewed vehicle; an expendable cargo vehicle after it leaves the ISS removes the risk to crew.

## Summary

Saffire-I burned a 40.6 cm x 94 cm sheet of SIBAL cotton-fibreglass fabric inside the uncrewed Cygnus OA-6 cargo module on 14 June 2016, after it left the ISS. This was about ten times larger in each dimension than any earlier microgravity flame-spread sample. Cabin air (about 21.7% O2, near 1 atm) was drawn through a flow duct at about 20 cm/s, and the sample was ignited at its upstream edge. The concurrent flame settled to a steady length of about 40 mm and spread steadily at 1.8 mm/s over about 84 cm for 420 s, releasing about 1.2 kW. On Earth, upward spread over this fabric accelerates. A contingency opposed-flow burn over the last ~10 cm spread at 1.3 mm/s; this fabric cannot burn downward in 1 g. Spread was slower than in the small BASS duct at half the flow, which the investigators attribute to duct size. The fire used about 0.2 percentage points of O2 and raised cabin pressure about 0.3 kPa. A steady flame size lets designers bound a fire's heat release.

## Physics

A flame spreading over a thin solid heats the fuel ahead of it until the fuel pyrolyses; the vapour mixes with oxygen and burns. On Earth, upward (concurrent) spread over a fabric is driven by a buoyant plume whose induced velocity grows with height, so the heated region, the flame and the spread rate all keep growing: upward fires accelerate. In orbit there is no buoyancy; the only flow is the imposed ventilation, here 20 cm/s, which is in the range of spacecraft cabin air circulation. In concurrent flow the flame and its hot plume extend downstream over unburnt fuel and preheat it, while the fuel behind the flame burns out. For a thin fuel, the burning (pyrolysis) zone has a length L_p set by how long the fuel takes to burn out, and the spread rate V_f is L_p divided by that burnout time. If the flame length is limited by the oxygen supply carried by a fixed forced flow, the flame, the pyrolysis zone and the spread rate can all reach steady values, so the fire stops growing. In opposed flow (the air moving against the spread, like downward burning on Earth), spread is governed by heat conducted forward from the flame's leading edge and is usually slower. A thin fabric that cannot spread downward on Earth because the strong buoyant flow blows it off can spread in a gentle forced opposed flow in microgravity. Two scale effects matter for comparisons with small experiments: a wider sample has less oxygen supply per unit width from the sides, and a small duct accelerates the flow around a flame because the hot gas expands, which increases spread rate.

$$
V_f = \frac{L_p}{t_b}
$$

Steady concurrent spread over a thin fuel. $V_f$ spread rate of the pyrolysis front (mm/s); $L_p$ steady pyrolysis length, the burning zone between the burnout front and the pyrolysis front (mm); $t_b$ local burnout time of the fuel (s). A steady state needs $L_p$ to stop growing, which happens when the forced flow limits the flame length; in 1 g buoyant upward spread $L_p$ keeps growing and the flame accelerates. Li et al. use this definition of burnout time to compare the 5 cm and 41 cm Saffire samples.

Textbook background
<https://doi.org/10.1016/j.proci.2018.05.168>: *While steady state pyrolysis lengths were similar, the 5 cm wide sample had a slightly larger spread rate (by ∼13%) and a shorter burnout time (pyrolysis length over spread rate) compared to the 41 cm wide sample.*

$$
\dot Q \approx \eta\, m''_c\, W\, V_f\, \Delta h_c
$$

Heat release rate of a steadily spreading flame over a sheet. $\dot Q$ (W); $m''_c$ areal density of the combustible part (kg/m2; SIBAL: 0.75 x 18 mg/cm2 = 0.135 kg/m2); $W$ sample width (m); $V_f$ spread rate (m/s); $\Delta h_c$ heat of combustion (J/kg, about 16 MJ/kg for cellulose, textbook value); $\eta$ fraction of the cotton actually burned (combustion efficiency). For Saffire-I ($W$ = 0.406 m, $V_f$ = 1.8 mm/s) complete combustion gives about 1.6 kW, of the same order as the investigators' estimate of 1200 +/- 300 W; smoulder residue and incomplete burnout lower $\eta$. Valid only once the spread is steady.

Textbook background
<https://ntrs.nasa.gov/citations/20170008805>: *Average flame spread rate is 1.8 mm/s; estimated average flame power is 1200 +/- 300 W*

$$
\mathrm{C_6H_{10}O_5} + 6\,\mathrm{O_2} \rightarrow 6\,\mathrm{CO_2} + 5\,\mathrm{H_2O} \;\Rightarrow\; \Delta x_{O_2} \approx -\Delta x_{CO_2}
$$

Complete combustion of cellulose consumes one O2 molecule per CO2 produced, so the drop in cabin O2 mole fraction equals the rise in CO2 mole fraction ($x$, mole fraction or %). This is how the investigators derived the O2 decrement from the CO2 sensor (21.7 to 21.5%), and it matches the +0.21 percentage-point CO2 rise in the PSI sensor file. It neglects CO, soot and absorption by the vehicle's CO2 removal (if any) during the burn.

Textbook background
<https://ntrs.nasa.gov/citations/20170008805>: *i Derived from measured CO2 production and referenced to initial O2 concentration reported by ISS.*

$$
V_f = \frac{\pi}{4}\,\frac{\lambda_g\,(T_f - T_v)}{\rho_s\,c_s\,\tau\,(T_v - T_\infty)}
$$

Thermal-regime (de Ris) opposed-flow spread rate over a thermally thin solid. $\lambda_g$ gas conductivity (W/m K); $T_f$, $T_v$, $T_\infty$ flame, pyrolysis and ambient temperatures (K); $\rho_s c_s \tau$ solid heat capacity per unit area (J/m2 K), here with $\tau$ the half-thickness. Textbooks differ on this convention: de Ris's original form uses $\sqrt{2}$ with the half-thickness, and some texts pair $\pi/4$ with the full thickness, so the coefficient depends on that choice. It predicts a spread rate independent of the opposed flow when chemistry is fast and radiation negligible. It is the reference against which the Saffire-I opposed rate (1.3 mm/s at 20 cm/s) and the BASS opposed rates can be compared.

Textbook background

## Method

### Apparatus

The Saffire flight unit (about 53 x 90 x 133 cm) was a flow duct with an adjoining avionics bay, separated by a Lexan panel. It was strapped into the Cygnus Pressurized Cargo Module (PCM) and was open to the cabin air at both ends. Fans at the top (outlet) of the duct drew air through a flow straightener at the bottom; the duct cross-section was about 18 x 20 in (about 46 x 51 cm; a later paper gives a 25 cm duct height on each side of the sample and a 45 cm width). Two anemometers, one on each side of the sample, measured the air speed and fed the fan control loop. The single sample card sat in the middle of the duct. Hot-wire igniters were woven into the fabric along the upstream edge (main igniter) and the downstream edge (redundant igniter). Two cameras in the avionics bay viewed one face of the whole sample; a green LED was switched on 1 s in every 3 s to show the pyrolysis front. Four radiometers (two viewing the front and two the back, each pair upstream and downstream) measured broadband radiation. Six thermocouples were sewn into the fabric at the centreline, with beads at several heights above the surface, at two streamwise stations; six more measured plume temperature, and one the inlet temperature. Solid-state sensors measured O2 (at the avionics bay inlet), CO2, pressure and humidity. A smoke wire at the sample leading edge gave flow visualisation before and after the burns. Sensor data were logged at about 30 Hz (0.033 s steps) and cameras recorded at about 30 frames/s.

### Fuels and samples

- SIBAL cotton-fibreglass fabric (75% cotton / 25% fibreglass by mass, 18 mg/cm2 areal density, 60 x 40 threads per inch, about 0.37 mm thick). Developed for the SIBAL (Solid Inflammability Boundary at Low-Speeds) flight experiment; it burns like cotton but the glass matrix keeps the sheet intact after the cotton is consumed. Same fabric as BASS (PSI-26) and Saffire-II samples 5 and 6 (solid, single thin flat sheet, 40.6 cm wide x 94 cm long, burned on both faces, flow parallel to the 94 cm length)

### Procedure

Saffire-I launched in the Cygnus OA-6 PCM on 22 March 2016 and stayed unpowered while the vehicle was berthed to the ISS. Before unberthing, the crew checked that the duct inlet and outlet were not blocked by stowed trash. After Cygnus left the ISS and moved to a separate orbit, the ground (Orbital ATK and NASA flight operations teams) powered the unit, ran a built-in test, recorded pre-test smoke-wire flow visualisation (F1), and sent the RUN command. On 14 June 2016 the fan set the flow to about 20 cm/s and, about 60 s into the recording, the upstream igniter was powered for 8 s (about 182 W measured; the 2017 slides give 165 W, 4.1 W/cm of width). The flame then spread downstream (concurrent flow) until the 420 s allotted burn time ended and the fan was switched off, which extinguished the flame at once. About 90% of the fabric had burned, so the contingency opposed-flow test was run: about 11 minutes later the downstream igniter was powered for 8 s and the flame spread upstream into the flow over the remaining ~10 cm, for about 70 s. Post-test flow visualisation (F2) followed. Images were compressed on board and downlinked over the following days, limited to 20 Gbit in total; selected raw (uncompressed) frames were then requested. The relays were opened on 19 June 2016 and Cygnus re-entered on 21 June.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| flow direction relative to spread | concurrent (S1, ignition at upstream edge) and opposed (S2, ignition at downstream edge, over the ~10 cm left after S1) |  |

Held constant:

- forced air flow speed: 20 cm/s nominal; anemometers read 20.5 and 19.4 cm/s before S1 ignition and 21.2 and 18.8 cm/s before S2
- oxygen (Cygnus cabin air, not controlled): 21.7% falling to 21.5% during S1; ~21.5% for S2 (ISS reading at hatch closure, decrement derived from CO2 production)
- pressure (Cygnus cabin): about 14.49 psi (99.9 kPa) on the Cygnus PCM sensor; 14.84 psia (102.3 kPa) on the Saffire ambient-pressure sensor
- sample: one SIBAL sheet, 40.6 cm x 94 cm, 0.37 mm, 18 mg/cm2
- ignition: hot wire across the sample width, 8 s at about 182 W (165 W in the 2017 slides)

Number of tests: 2

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame base and pyrolysis-front position vs time, giving spread rate, flame length and pyrolysis length | 2 colour cameras (~30 frames/s, compressed jpeg plus selected raw frames), green LED illumination 1 s in 3, distortion-corrected ('mapped') with pre-flight checkerboard grids | derived |
| flame radiation (broadband), upstream and downstream, front and back faces | 4 radiometers, mW/cm2 | direct |
| flame temperature near the sample surface at two streamwise stations (beads at several heights) and plume temperature | 6 sample thermocouples (TC7-TC12) and 6 plume thermocouples (TC1-TC6) | direct |
| air speed in the duct and fan speed | 2 anemometers (cm/s), fan tachometer (RPM) | direct |
| vehicle O2 and CO2 mole fraction, pressure, relative humidity, inlet temperature | solid-state sensors in or at the inlet of the avionics bay | direct |
| Cygnus PCM air temperature and pressure, smoke detector obscuration and scatter, cabin fan pressure rise, vehicle body rates and accelerations | Cygnus vehicle telemetry (about 1 sample per 10 s for pressure/temperature) | direct |
| average flame power (heat release rate) | estimated from spread rate and fuel loading | derived |
| flow uniformity before and after the burns | smoke wire at the sample leading edge, imaged by both cameras (F1, F2 image sets) | direct |

## Findings

1. In concurrent flow at about 20 cm/s and 21.7% O2 (falling to 21.5%) near 1 atm, the flame over the 40.6 cm x 94 cm SIBAL sheet reached a steady state: it spread at a constant average 1.8 mm/s, and the flame length reached a plateau of about 40 mm. It burned about 84 cm of the 94 cm sheet during the 420 s allotted. On Earth the same configuration (upward burning) consumes the whole sample with an accelerating flame. This answers the main Saffire question: a large concurrent fire in microgravity, under forced ventilation, need not keep growing. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *For the concurrent flame, the length reaches a plateau value of around 40 mm, while the opposed-flow flame is a bit shorter at 24 mm.*
   - <https://ntrs.nasa.gov/citations/20170008805>: *1-1 182 W 8 s 420 s ~ 84 cm 1.8 mm/s Complete Acceleratory*
   - <https://doi.org/10.1016/j.combustflame.2018.10.012>: *The downloaded test data show that a concurrent (downstream) spreading flame over thin fabrics in microgravity reaches a steady spread rate and a limiting length.*
2. The opposed-flow flame (spreading into the 20 cm/s flow, ~21.5% O2) burned the remaining ~10 cm of fabric in about 70 s at an average 1.3 mm/s, with a flame length of about 24 mm. In 1 g this fabric does not spread downward (burn length ~0). So for this material, opposed-flow spread is possible in microgravity at a cabin-like ventilation speed but not on Earth. The concurrent flame spread about 1.4 times faster than the opposed flame. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *1-2 182 W 8 s 70 s ~ 10 cm 1.3 mm/s ~ 0 n/a*
   - <https://ntrs.nasa.gov/citations/20170008805>: *The average concurrent-flow flame spread rate is 1.8 mm/s. The opposed-flow flame average spread rate 1.3 mm/s.*
3. The average flame power of the concurrent fire was estimated at 1200 +/- 300 W. This is a 40.6-cm-wide flame front; the 5-cm-wide SIBAL samples of Saffire-II gave about 200 W. *(result, medium)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *Average flame spread rate is 1.8 mm/s; estimated average flame power is 1200 +/- 300 W*
   - <https://ntrs.nasa.gov/citations/20180005168>: *Saffire 1: 1200 +/- 300 W Saffire 2: 200 +/- 50 W*
4. The concurrent flame was unsteady at first: flame length and brightness oscillated at about 1.4 Hz until about 90 s into the test, then settled, with small fluctuations at about 0.75 Hz persisting for the whole burn. The cause is unknown; the investigators suggest a flow oscillation present even in cold flow, or flame interaction with the flow in the duct entrance. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *Initially the flame length fluctuated at about 1.4 Hz before finally becoming more stable at about 90 s*
   - <https://ntrs.nasa.gov/citations/20170008805>: *However, subtle fluctuations in flame length and brightness persisted for the duration of the test albeit at a slightly slower frequency of around 0.75 Hz.*
5. Flame appearance: at ignition the flame was bright yellow and vigorous; it soon developed a blue base with orange radiation from incandescent soot. Behind the flame, exothermic smoulder spots kept burning leftover fuel. When the air flow was switched off at the end of the allotted time, the flame went out immediately. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *At ignition, the flame was mostly bright yellow and relatively vigorous but it soon developed a blue base and a pattern of orange radiation coming from incandescent soot*
   - <https://ntrs.nasa.gov/citations/20170008805>: *The flame burned the entire allotted test time of about 7 min. at which point the air flow was shut off and the flame immediately extinguished*
6. Scale and duct size matter. The Saffire-I concurrent flame (1.8 mm/s at 20 cm/s in a ~46 x 51 cm duct) spread more slowly than BASS flames over the same fabric in the 7.6 cm SPICE duct, even though the Saffire sample was much wider and the flow was twice as fast. BASS 2-cm strips spread at 2.55 mm/s at about 10 cm/s, and BASS's linear concurrent fits (printed as V_F = -0.20 U + 0.56 and -0.15 U + 0.07 mm/s on an axis where concurrent flow is negative; written with U as the concurrent speed in cm/s, V_F = 0.20U + 0.56 or 0.15U + 0.07) extrapolate to about 3.1-4.6 mm/s at 20 cm/s (our extrapolation). The investigators attribute this to flow acceleration from hot-gas expansion in the smaller tunnels, and conclude that concurrent spread is more sensitive to duct dimensions than anticipated. Small-duct microgravity data can therefore overestimate concurrent spread in an open cabin. *(trend, medium)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *Compared to previous microgravity work in smaller tunnels, the flame in the larger tunnel spread more slowly, even for a wider sample. This is attributed to the effect of flow acceleration in the smaller tunnels as a result of hot gas expansion.*
   - <https://ntrs.nasa.gov/citations/20180005168>: *Concurrent flame spread (with the wind) was shown to be more sensitive to the flow duct dimension than previously anticipated.*
   - <https://doi.org/10.60555/58h4-dy80 (PSI-26 BASS, file PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf p24)>: *Concurrent and Opposed Spread at ~ 10 cm/s 2.55 mm/s versus 1.21 mm/s*
   - <https://doi.org/10.60555/58h4-dy80 (PSI-26 BASS, file PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf p25)>: *VF = - 0.20 U∞ + 0.56 VF = - 0.15 U∞ + 0.07*
7. Sample width effect: a 5-cm-wide SIBAL strip burned on Saffire-II at the same 20 cm/s spread at 2.1 mm/s versus 1.8 mm/s for the 40.6-cm sheet (the model paper says about 13% faster; 2.1/1.8 is 17%), with a similar steady pyrolysis length and shorter burnout time. Part of the difference is the higher starting O2 (22.1% vs 21.7%). A 3-D transient model attributes the narrow sample's shorter burnout time to more effective oxygen transport across its width; neither source splits the spread-rate difference between this and the O2 difference. The large sample also showed an initial overshoot of pyrolysis length before reaching steady state, which the model explains by flow reduction in the growing boundary layer. *(trend, medium)*
   - <https://ntrs.nasa.gov/citations/20170008805>: *The flame spread rate for the 5-cm-wide sample is marginally faster compared to the spread rate for the 40.6-cm-wide sample for the same flow speed of 20 cm/s (2.1 compared to 1.8 mm/s).*
   - <https://doi.org/10.1016/j.proci.2018.05.168>: *While steady state pyrolysis lengths were similar, the 5 cm wide sample had a slightly larger spread rate (by ∼13%) and a shorter burnout time (pyrolysis length over spread rate) compared to the 41 cm wide sample.*
   - <https://doi.org/10.1016/j.proci.2018.05.168>: *Compared to a wide sample, a narrow sample has more effective oxygen transport across the width of the sample.*
   - <https://doi.org/10.1016/j.proci.2018.05.168>: *However, the pyrolysis length exhibited an initial overshoot before reaching steady state for the large sample.*
   - <https://doi.org/10.1016/j.proci.2018.05.168>: *The modeling results reveal that flow reduction in a growing boundary layer along the sample surface accounts for the overshoot of the flame length observed for the large sample.*
8. Effect on the vehicle (our analysis of the PSI sensor files). During the concurrent burn, CO2 at the Saffire sensor rose from 0.426% to 0.632% (+0.21 percentage points), consistent with the investigators' O2 drop of 21.7% to 21.5% derived from CO2. The Saffire ambient pressure rose from 14.843 to about 14.888 psia (+0.045 psi, +0.31 kPa, +0.3%), peaking near the end of the burn and decaying after the fan stopped. The Cygnus PCM pressure rose from 14.488 to 14.537 psi (+0.34 kPa) and the PCM air temperature from 19.98 to 20.18 C. The opposed burn added only +0.02 percentage points CO2. The investigators describe the oxygen use as '1.5 of the available oxygen' (unit missing in the source). *(result, medium)*
   - `PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row row 912 (t = 30.0 s, before ignition) and row 18055 (t = 595.7 s, after the burn): *CO2 0.42648 % -> 0.63240 %; Ambient Pressure 14.83757 PSIA -> 14.85616 PSIA (20-s means peak at 14.888 PSIA near t = 460 s)*
   - `PSI-98_Raw Data_Saffire-I Telemetry Data Good Process Version.xlsx`, sheet CygnusData, row non-zero entries 30 min before vs during 20:45-21:06 UTC 14 June 2016: *PCM Press (psi) 14.488 -> max 14.537; PCM Air Temp (degC) 19.978 -> max 20.183*
   - `PSI-98_Raw Data_Saffire-I Sample 2 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row pre-ignition mean (t < 55 s) vs max: *CO2 0.6286 % -> 0.6458 %*
   - <https://ntrs.nasa.gov/citations/20170008805>: *The sample was an order of magnitude larger than anything studied to date in microgravity and was of sufficient scale that it consumed 1.5 of the available oxygen.*
9. Radiometer records (our analysis) bracket the concurrent burn. Baseline-subtracted radiation at the upstream pair rose from ignition (t = 60 s) to 139 mW/cm2 at t = 225 s. The downstream pair peaked at 145-149 mW/cm2 at t = 343 s as the flame passed them. Signal above 5 mW/cm2 lasted from t = 65 s to t = 485 s, i.e. about 420 s, matching the reported burn time and ending when the fan stopped (anemometers fall to ~0.1 cm/s by t = 500 s). For the opposed burn, only the downstream radiometers responded (peak 18-21 mW/cm2 at t = 105 s). The signal fell to baseline by t = 138 s, about 75 s after ignition, while the fan was still running, consistent with burnout of the remaining fuel. The radiometers' view geometry is not documented in PSI, so these are relative signals, not flame emissive power. *(result, medium)*
   - `PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row row 6851 (t = 225.98 s) and row 10409 (t = 343.40 s): *Radiometer 2 123.17 (Upstream Front); Radiometer 1 132.17 (Downstream Front) mW/cm2 raw; baseline-subtracted maxima: Upstream Front 138.9, Upstream Back 139.4, Downstream Front 144.7, Downstream Back 149.1*
   - `PSI-98_Raw Data_Saffire-I Sample 2 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row row 3170 (t = 104.51 s): *Radiometer 1 6.756 mw/cm^2 raw (baseline -12.52); Downstream Front max 20.64, Downstream Back max 17.67 mw/cm^2*
10. Sample thermocouples (our analysis) peaked at 698, 886 and 1078 C at the first station (t = 194-207 s) and 688, 1092 and 333 C at the second (t = 345-369 s). These are bead temperatures at different heights above the surface, uncorrected for radiation. The flame arrival times differ by about 150-165 s between stations; at 1.8 mm/s this implies a station spacing of about 27-30 cm. The thermocouple positions are not given in PSI, so this is only a consistency check. *(method, low)*
   - `PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row column maxima of Sample Temp 1-6 (TC7-TC12): *TC7 698.3 C @193.8 s; TC8 886.0 @206.7; TC9 1078.1 @204.4; TC10 688.1 @359.5; TC11 1091.8 @369.0; TC12 332.6 @344.7*
   - <https://ntrs.nasa.gov/citations/20170008805>: *Plots of igniter current and thermocouple temperatures. X-distance along the sample for each thermocouple is shown on the diagram.*
11. The fan control loop held the measured air speed near 20 cm/s by cutting fan speed from about 6340 to about 5100 RPM as the flame grew (t = 60-200 s), then raising it again. During the burn the two anemometers diverged (one rising to ~21.6 cm/s, the other falling to ~18.4 cm/s), so the fire itself perturbed the duct flow. The free-stream velocity over the flame is therefore known only to about +/-1-2 cm/s. *(method, medium)*
   - `PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx`, sheet Calibrated Data, row 20-s means, t = 0-40 s vs t = 160-200 s; row 6851 (t = 225.98 s): *Average Fan Speed ~6340 -> ~5100 RPM; Anemometer 1 21.6077, Anemometer 2 18.3924 cm/sec at t = 225.98 s*
   - <https://ntrs.nasa.gov/citations/20170000230>: *Two flow anemometers, one on each side of the sample will quantify the flow velocity in the duct and serve as input to the fan flow control algorithm.*
12. Plan versus flight. The pre-flight paper held in PSI (written by 30 April 2016) planned Saffire-I as a burn of a SIBAL sheet about 0.94 m long and 0.4 m wide at 20 cm/s (Saffire-III at 30 cm/s), in hardware identical across the three units, a few hours after Cygnus unberthed on 2 June 2016. The flight followed the plan in sample and flow (94 x 40.6 cm, about 20 cm/s) but burned on 14 June 2016. The same paper warned that only two large samples and nine small ones would be burned, too few for a thorough evaluation, and that the results would likely raise new questions. *(method, high)*
   - `PSI-98_Science Documents_SAFFIRE Objectives, Development and Status.pdf` (p2): *Saffire-I will be conducted at an air flow velocity of 20 cm/s while Saffire-III will be run at a flow velocity of 30 cm/s*
   - `PSI-98_Science Documents_SAFFIRE Objectives, Development and Status.pdf` (p2): *This sample material is approximately 0.94 meters long and 0.4 meters wide.*
   - `PSI-98_Science Documents_SAFFIRE Objectives, Development and Status.pdf` (p4): *As of the writing of this paper, the un- berthing of the Cygnus is scheduled for June 2, 2016 and Saffire-I is scheduled to operate a few hours afterwards.*
   - `PSI-98_Science Documents_SAFFIRE Objectives, Development and Status.pdf` (p5): *A thorough evaluation of these phenomena would require many more samples and range of materials. Also, if they are typical of most low-g combustion experiments, the findings will raise additional significant questions for material flammability in spacecraft.*

## Fire-safety relevance

Saffire-I is the first measurement of how a realistically large fabric fire behaves in a spacecraft. Its key result is that, with forced ventilation of about 20 cm/s and no buoyancy, a concurrent flame over a thin charring fabric does not keep growing as it would on Earth. It reaches a steady spread rate (1.8 mm/s) and a limiting size (flame length ~40 mm, about 1.2 kW for a 40 cm front). The investigators note that a bounded flame size lets designers set the heat release rate a fire can impose on the vehicle. The opposed-flow burn confirms that a fabric which cannot burn downward in 1 g can burn against a cabin-like flow in orbit, so the 1-g downward configuration is not conservative. The duct-size effect means small-chamber microgravity flammability data (BASS, glovebox tests) are not directly transferable to an open cabin: here the larger enclosure gave slower spread. Vehicle impact was small: about 0.2 percentage points of O2 consumed and a 0.3 kPa pressure rise in the Cygnus PCM. This bounds the effect of one ~1 kW, 7-minute fire in a cargo-module-sized volume, not a worst case. The vehicle telemetry (smoke detectors, pressure, temperature) gives a first data set for detection and habitability modelling. The result applies to one thin cellulosic fabric at about 21% O2 and 1 atm; it is not a flammability limit and does not cover thick fuels or exploration atmospheres.

### Habitat conditions

Saffire-I burned in Cygnus cabin air: 21.7% O2 at the start (ISS reading at hatch closure), falling to 21.5%, at about 14.5-14.8 psi (99.9-102.3 kPa depending on the sensor). This is essentially the Earth sea-level reference (20.9% O2 at 101.3 kPa), and slightly O2-enriched. It is far from the exploration atmospheres in the shared reference: a Moon habitat at 30% O2 or more at 70.3 kPa or less, and spacesuits at 100% O2 at 29.6 kPa. Higher O2 mole fraction generally raises spread rates and flame temperatures, so these results do not bound fire growth in such atmospheres. The Saffire team listed elevated-O2, reduced-pressure flame behaviour as a follow-on objective, to be compared with Saffire-I to III. The 20 cm/s flow is representative of cabin ventilation.

### Earth benefits

Studying fire in a small, sealed vehicle is relevant to fire safety in other confined spaces such as mines, aircraft and submarines. The purely forced-flow data also give clean validation cases for flame-spread models (e.g. the CWRU 3-D transient model) used for both space and terrestrial fire scenarios.

## Limitations

- Only one large sample. There was a single concurrent burn and a contingency opposed burn over only ~10 cm of leftover fabric, at a single flow speed and O2 level, so there is no repeatability and the opposed result rests on about 70 s of burning.
- The flame was in a duct (~46 x 51 cm), not open cabin air; the investigators found spread to be sensitive to duct size, and the fan control loop and the flame interacted (fan speed changed by ~20% during the burn). Results are specific to this duct geometry.
- Oxygen was not controlled or measured independently. The reported 21.7-21.5% comes from the ISS reading at hatch closure plus CO2 production. The Saffire O2 sensor read about 22.6%, so it has an offset of roughly 1 percentage point, and the two pressure sensors (Saffire and Cygnus) disagree by about 0.35 psi (2.4 kPa).
- Image data are limited by the 20 Gbit downlink: most frames exist only as on-board compressed jpegs, a subset as raw frames, and some frames were lost or corrupted (gaps visible in the LED timing).
- One thin, charring, cellulosic fabric was tested. Thick fuels, melting or dripping materials, and complex geometries (gaps, corners, cluttered stowage) were not tested, and the sample was flat and centred in a uniform flow.

## Data in PSI

PSI-98 holds 76 files (12.25 GB). Almost all of it (61 zips, 12.18 GB, not downloaded) is imagery: for each run (S1, S2, F1, F2) and camera (C1, C2) there are on-board jpegs, distortion-corrected ('Mapped') jpegs, raw camera frames (DistroMaster, with the 8-byte offset fixed), demosaiced TIFFs, and PNGs annotated with exposure and gain, plus checkerboard distortion grids. The S1 sets are split into parts and are the largest (the annotated PNG sets alone are 1.0-1.5 GB per part). What is usable now are the downloaded sensor workbooks. 'Sample 1/2 Sensor Data Complete TM graphs.xlsx' (25 MB each) hold a 'Calibrated Data' sheet at about 30 Hz for 660 s per run: fan speed, CO2, O2, two anemometers, ambient pressure, four radiometers (raw and baseline-subtracted, labelled upstream/downstream, front/back), humidity, inlet temperature, six plume and six sample thermocouples, radiometer temperatures, igniter current and voltage, avionics housekeeping and control flags; plus a 'Camera Data' sheet of per-frame exposure and gain. 'Telemetry Data Good Process Version.xlsx' holds the low-rate real-time telemetry (radiometers, anemometers, fan tachometer, igniters for all 9 Saffire-II-style channels) and Cygnus vehicle data (PCM air temperature and pressure, smoke detectors, cabin fan pressure rise, body rates, accelerations). Two docx files hold the sensor plots. The MergeResult xlsx lists every image file by timestamp, whether it was received or corrupted, and its zip (about 36,000 images each for S1 and S2). No reduced data (flame position vs time, spread rates) are in PSI; the published results come from NASA technical reports and journal papers.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | image archives per run and camera (S1C1, S1C2, S2C1, S2C2, F1, F2): jpeg, mapped jpeg, raw DistroMaster, Raw2TIFF, icmad-annotated PNG/TIFF, distortion grids | .zip | 61 | 12.2 GB | no |
| Raw Data | sensor workbooks: Sample 1 and Sample 2 calibrated 30 Hz data (660 s each) and the real-time telemetry plus Cygnus vehicle data | .xlsx | 3 | 52.7 MB | yes |
| Raw Data | sensor time-history plots for samples 1 and 2 (figures with captions only) | .docx | 2 | 2.4 MB | yes |
| Raw Data | thermocouple placement verification sheet (scanned, no positions given) and image frame-size / ROI offset grid document (not downloaded) | .pdf | 2 | 1.9 MB | no |
| Science Documents | Saffire objectives/development/status paper (IAASS 2016), Saffire-I/III readme, image directory nomenclature, image merge/received log (xlsx) | .pdf .docx .xlsx | 4 | 12.8 MB | yes |
| Engineering Documents | Saffire-I operations summary (downloaded); offgassing testing strategy (not downloaded) | .pdf | 2 | 1.7 MB | yes |
| Experimental table | 2 burns (S1 concurrent, S2 opposed) plus F1/F2 flow-visualisation rows | .csv | 1 | 500 B | yes |
| metadata | ISA-Tab metadata zip (file name says PSI-166) | .zip | 1 | 10 kB | no |

Rows in the unified `tests` table: 2

## Related investigations

- [PSI-99](PSI-99-saffire-ii.md): shared hardware
- [PSI-100](PSI-100-saffire-iii.md): follow-on
- [PSI-26](PSI-26-bass.md): same fuel

## Open questions

- Digitise flame base, flame tip and pyrolysis front vs time from the mapped jpeg/raw image sets (S1C1, S1C2, S2C1) to reproduce the 1.8 and 1.3 mm/s spread rates, the ~40 mm plateau and the pyrolysis-length overshoot directly from PSI data.
- Combine CO2 rise, Cygnus pressure/temperature rise and spread rate to estimate the PCM free volume and an independent heat-release rate (the investigators listed both as planned analyses).
- Analyse the Cygnus smoke detector (FIZ obscuration/scatter) records around the burn for detection time and signal level; the raw telemetry shows scatter spikes before as well as during the burn, so a careful baseline is needed.
- Spectral (FFT) analysis of radiometer and plume-thermocouple signals to confirm the 1.4 Hz and 0.75 Hz flame oscillations and test whether they appear in the pre-test cold-flow smoke-wire images.
- Recover the sample thermocouple x-positions and heights (drawing 120102MFA310, not in PSI) to turn the TC records into flame stand-off and spread-rate data for model validation.

## Dashboard ideas

- **spread rate vs signed flow speed (all SIBAL data)** (`flow_cm_s (negative = concurrent)`, `spread_rate_mm_s`, `sample_width_cm`, `duct_size_cm`, `investigation`): Places Saffire-I/III (40.6 cm, large duct) beside Saffire-II 5 cm strips and BASS 1-2 cm strips (7.6 cm duct) to show the scale/duct effect.
- **sensor time series for each burn** (`elapsed_s`, `radiometers_mW_cm2`, `anemometers_cm_s`, `fan_rpm`, `co2_pct`, `pressure_kpa`, `sample_tc_C`): The calibrated 30 Hz workbooks are directly plottable and show ignition, flame passage, fan shut-off and vehicle response.
- **vehicle impact panel** (`delta_o2_pct`, `delta_co2_pct`, `delta_p_kPa`, `delta_T_C`, `flame_power_W`, `burn_time_s`): Compares the cabin response of Saffire-I and III fires for habitability and detection discussions.

## Gaps and data-quality notes

- No reduced results (flame position vs time, spread rates, flame lengths) are in PSI-98; all quantitative flame results come from external NASA NTRS presentations (ICES 2016 and 2017, ASGSR 2017) and journal abstracts (Combustion and Flame 2019; Proc. Combust. Inst. 2019). The full journal papers are paywalled and only their abstracts were read.
- Thermocouple x-positions and bead heights are not in PSI. The thermocouple placement PDF is a scanned verification sheet that refers to drawing 120102MFA310 and an internal eRoom link but gives no coordinates.
- The flame stand-off, pyrolysis-length time series and the Saffire-I flame-position plots exist only as figures in the external slides (no text layer for the data).
- Not downloaded: the 61 image zips (12.2 GB), the ImageFrameSizes/ROI offsets PDF, the offgassing strategy PDF and the metadata zip.
- Data quality: the PSI record dates (start 2001-03-02, end 2008-02-28) do not match the experiment (launch 22 March 2016, burn 14 June 2016, relays opened 19 June 2016); the identity dates here use the external sources. The PSI 'proposalTitle' ('Characterization of Smoke from Microgravity Fires for Improved Spacecraft Fire Detection') belongs to a smoke investigation, not Saffire.
- Data quality: the experimental table gives thickness '0.37' in a cm column, but the published value is 0.37 mm; it also swaps length and width (length 40.6, width 94) relative to all documents (40.6 cm wide x 94 cm long). The table's ignition power (182 W) matches the raw igniter data, while the 2017 slides say 165 W.
- Data quality: the Saffire O2 sensor reads ~22.6% before ignition, against the 21.7% ISS reading used by the investigators. Pressure differs between the Saffire sensor (14.84 psia) and the Cygnus PCM sensor (14.49 psi).
- Data quality: the ICES 2016 slide (NTRS 20170002628) says OA-6 unberthed on 'June 22', which conflicts with the 14 June operations date in the same slide and the sensor timestamps.
- The external ICES 2017 abstract says the fire 'consumed 1.5 of the available oxygen' with no unit; the table in the same deck gives 21.7 to 21.5% O2. The exact meaning is unclear.
- Saffire-I sensor-derived values in findings (pressure, CO2, radiometer and thermocouple peaks, fan speed) are our computations from the PSI workbooks, not published numbers.
- No text addressed to an AI or unrelated instructions were found in the PSI-98 documents.
