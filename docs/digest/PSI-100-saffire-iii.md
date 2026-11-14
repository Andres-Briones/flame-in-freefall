# PSI-100: SAFFIRE-III (Spacecraft Fire Experiment-III (Saffire-III))

A repeat of the first large spacecraft fire experiment, with the air blowing a little faster, to see how ventilation speed changes how fast a large sheet of fabric burns in an empty cargo spacecraft in orbit.

Investigators: David L. Urban (PI; NASA GRC); Gary A. Ruff (Saffire project; NASA GRC); Paul V. Ferkul, Sandra L. Olson, John Easton (NASA GRC science team); International Fire Safety in Space Topical Team (ESA-assembled), incl. James S. T'ien and Ya-Ting T. Liao (Case Western Reserve University), A. Carlos Fernandez-Pello, Jose L. Torero, Guillaume Legros, Christian Eigenbrod, Nickolay Smirnov, Osamu Fujita, Sebastien Rouvreau, Balazs Toth, Grunde Jomaas

## At a glance

| | |
|---|---|
| Platform | Orbital ATK Cygnus OA-7 Pressurized Cargo Module (uncrewed), operated in free flight after unberthing from the ISS |
| Facility | Saffire flow unit (flow duct plus avionics bay, about 53 x 90 x 133 cm) strapped in the Cygnus PCM |
| Dates | 2017-04-18 |
| Fuels and samples | SIBAL cotton-fibreglass fabric |
| Varied | flow direction relative to spread: opposed (S2, ignited at downstream edge, run first) and concurrent (S1, ignited at upstream edge)<br>forced flow speed (across the Saffire-I/III pair): 20 (Saffire-I) vs 25 (Saffire-III; planned 30) cm/s |
| Number of tests | 2 |
| Fire-safety pillars | fundamental, prevention, detection |

## Question

Saffire-III had the same objectives as Saffire-I: (1) determine how rapidly a large-scale fire grows in low gravity and whether it reaches a steady-state spread rate, and (2) investigate low-g flammability compared with NASA's normal-gravity screening test. Its particular role was to repeat the large-sample burn at a higher forced flow (planned 30 cm/s vs 20 cm/s), to show how the steady spread rate and flame size depend on ventilation speed. The motivation is the same: earlier microgravity tests used samples no larger than about 10 cm in small chambers, and terrestrial fire data carry large uncertainty for spacecraft fire-safety design.

## Summary

Saffire-III repeated Saffire-I in the uncrewed Cygnus OA-7 cargo module on 4 June 2017. A 40.6 cm x 94 cm sheet of SIBAL cotton-fibreglass fabric was burned in cabin air (21.2% O2 falling to 21.0%, near 1 atm) in a flow duct. The flow was planned at 30 cm/s but was about 25 cm/s. An opposed-flow burn was run first from the downstream edge and spread into the flow at 0.98 mm/s over about 10 cm in 60 s. The concurrent burn from the upstream edge then spread steadily at 2.3 mm/s over about 84 cm in about 300-320 s. Compared with Saffire-I at 20 cm/s (1.8 and 1.3 mm/s), the faster flow sped up concurrent spread in proportion to the flow and slowed opposed spread. Spread rates were below those of the small-duct BASS strips and the narrow Saffire-II strips. The fire again used about 0.2 percentage points of O2 and raised cabin pressure about 0.4 kPa. Fire growth depends on ventilation speed and on enclosure size, so small-sample tests do not set the hazard.

## Physics

The physics is that of Saffire-I (PSI-98): flame spread over a thin charring fabric in a purely forced flow, with no buoyancy. In concurrent flow, the flame and hot plume extend downstream and preheat the fuel. A faster forced flow brings more oxygen and stretches the flame and pyrolysis zone downstream, so concurrent spread speeds up roughly in proportion to the flow, while the steady state (fixed flame and pyrolysis length) is kept. In opposed flow, spread is driven by heat conducted forward from the flame's leading edge. Above a moderate flow speed, faster opposed flow shortens the gas residence time at the leading edge and cools it, so spread slows towards blow-off. BASS (PSI-26) found opposed spread over the same fabric peaks at 10-15 cm/s. Increasing the flow from 20 to 25 cm/s is therefore expected to make concurrent spread faster and opposed spread slower, widening the gap between them. Enclosure size also matters: in a small duct, hot-gas expansion accelerates the flow around the flame, which speeds concurrent spread.

$$
\frac{V_{f,III}}{V_{f,I}} \approx \frac{U_{III}}{U_{I}} \quad\Leftrightarrow\quad V_f \propto U_\infty \;(\text{concurrent, thin fuel, forced flow})
$$

The investigators' scaling for concurrent spread in purely forced flow: spread rate $V_f$ (mm/s) proportional to the free-stream air speed $U_\infty$ (cm/s). Saffire-I: 1.8 mm/s at 20 cm/s; Saffire-III: 2.3 mm/s at 25 cm/s; ratios 1.28 and 1.25. The burn durations (400 s vs 320 s in the ASGSR slides) are in the inverse ratio. Supported by only two large-sample points at one O2 level and one duct size; BASS small-duct data instead fit a linear relation with an intercept.

<https://ntrs.nasa.gov/citations/20180005168>: *This is equal to the inverse ratio of the flame speed*
<https://ntrs.nasa.gov/citations/20180005168>: *3-1 182 W 8 s 300 s ~ 84 cm 2.3 mm/s Complete Acceleratory*

$$
V_f = \frac{L_p}{t_b}, \qquad \dot Q \approx \eta\, m''_c\, W\, V_f\, \Delta h_c
$$

Steady thin-fuel concurrent spread: $V_f$ spread rate (m/s), $L_p$ steady pyrolysis length (m), $t_b$ burnout time (s). Heat release rate $\dot Q$ (W) with $m''_c$ = 0.135 kg/m2 (cotton part of 18 mg/cm2 SIBAL), $W$ = 0.406 m, $\Delta h_c$ about 16 MJ/kg for cellulose (textbook), $\eta$ combustion fraction. For Saffire-III ($V_f$ = 2.3 mm/s) complete combustion gives about 2.0 kW; scaling the Saffire-I estimate (1200 +/- 300 W) by the spread-rate ratio gives about 1.5 kW. No published Saffire-III flame power was found.

Textbook background
<https://ntrs.nasa.gov/citations/20170008805>: *Average flame spread rate is 1.8 mm/s; estimated average flame power is 1200 +/- 300 W*

$$
\Delta x_{O_2} \approx -\Delta x_{CO_2} \quad (\mathrm{C_6H_{10}O_5} + 6\,\mathrm{O_2} \rightarrow 6\,\mathrm{CO_2} + 5\,\mathrm{H_2O})
$$

For complete combustion of cellulose, one O2 is consumed per CO2 formed, so the cabin O2 mole fraction drop equals the CO2 rise. The investigators derived the Saffire-III O2 decrement (21.2 to 21.0%) from CO2 this way; the PSI sensor file shows a +0.21 percentage-point CO2 rise over the concurrent burn. Neglects CO, soot and CO2 removal.

Textbook background
<https://ntrs.nasa.gov/citations/20180005168>: *III-1 Cotton-Fiberglass 40.6 cm 0.37 mm 94 cm 25 cm/s Concurrent 21.2 to 21.0*

## Method

### Apparatus

Same flight design as Saffire-I; the three Saffire units differed only in the sample card. The flow unit (about 53 x 90 x 133 cm) had a flow duct (about 18 x 20 in; 25 cm height on each side of the sample and 45 cm width according to a later paper) and an adjoining avionics bay behind a Lexan window, strapped into the Cygnus PCM and open to the cabin. Fans at the outlet drew air through a flow straightener. Two anemometers, one on each side of the sample, controlled the fan. Igniters were woven into the upstream and downstream edges of the single 40.6 x 94 cm sample. Diagnostics: two cameras (one face), four radiometers (two front, two back), six sample thermocouples sewn into the fabric at two stations with beads at several heights, six plume thermocouples, inlet temperature, O2, CO2, pressure and humidity sensors in the avionics bay, and a smoke wire for flow visualisation. Calibrated sensor data are at 0.033 s intervals; the PSI workbooks label the radiometers only as 1-4 (Saffire-I's workbook names their positions).

### Fuels and samples

- SIBAL cotton-fibreglass fabric (75% cotton / 25% fibreglass by mass, 18 mg/cm2, 0.37 mm in the investigators' table; 0.33 mm in the 2016 status paper), same material as Saffire-I and BASS (solid, single thin flat sheet, 40.6 cm wide x 94 cm long, flow along the 94 cm length, burned on both faces)

### Procedure

Saffire-III launched in the Cygnus OA-7 PCM (PSI start date 18 April 2017) and stayed unpowered while berthed. After unberthing, the Cygnus team moved the vehicle to a separate orbit, powered the experiment, ran a check, put the vehicle in free drift and started the run. This took about half a day from undocking. The burns took place on 4 June 2017 (sensor timestamps, UTC). Pre-test smoke-wire flow visualisation (F1) started at 21:09. The sensor files show that the opposed-flow sample (S2) was run first: the downstream igniter was powered at about 21:11:16 UTC and the fan was switched off about 60-70 s later. The concurrent sample (S1) followed: igniter on at about 21:14:31 UTC, and the flame spread upstream-to-downstream over about 84 cm. Post-test flow visualisation (F2) began at 21:26. Both burns used the same ~25 cm/s flow; the planned 30 cm/s was not reached. Only a subset of the data was downlinked (20 Gbit limit); about 3,400 raw frames were requested for S1 and S2.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| flow direction relative to spread | opposed (S2, ignited at downstream edge, run first) and concurrent (S1, ignited at upstream edge) |  |
| forced flow speed (across the Saffire-I/III pair) | 20 (Saffire-I) vs 25 (Saffire-III; planned 30) | cm/s |

Held constant:

- forced air flow speed: about 25 cm/s (anemometers 24.5 and 25.4-25.5 cm/s before each ignition); the PSI record and table say 30 cm/s
- oxygen (Cygnus cabin air, not controlled): 21.2% falling to 21.0% over the two burns (decrement derived from CO2)
- pressure (Cygnus cabin): about 13.97-13.99 psi (96.3-96.5 kPa) on the Cygnus PCM sensors; 14.42 psia (99.4 kPa) on the Saffire sensor
- sample and ignition: one SIBAL sheet 40.6 x 94 cm; igniters 182 W for 8 s (investigators' table)

Number of tests: 2

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame base and pyrolysis-front position vs time, spread rate, flame shape (concurrent vs opposed) | 2 cameras (~30 frames/s jpeg; selected raw frames), distortion-corrected image sets | derived |
| flame radiation | 4 radiometers (mW/cm2), positions not labelled in the Saffire-III workbooks | direct |
| sample-surface (flame) and plume temperatures | 6 sample thermocouples (TC7-TC12), 6 plume thermocouples (TC1-TC6) | direct |
| air speed, fan speed | 2 anemometers, fan tachometer | direct |
| vehicle CO2, O2, pressure, relative humidity, inlet temperature | solid-state sensors in the avionics bay | direct |
| Cygnus PCM air temperature, three cabin pressure sensors, smoke detectors, cabin fan pressure rise, body rates and accelerations | Cygnus vehicle telemetry | direct |

## Findings

1. Concurrent burn (S1) at about 25 cm/s and 21.2-21.0% O2, near 1 atm: the flame spread over about 84 cm of the 40.6-cm-wide sheet at an average 2.3 mm/s, burning for about 300 s (investigators' table; 320 s in the ASGSR slides). In 1 g the same configuration burns completely with an accelerating flame. Together with Saffire-I, the investigators conclude that concurrent spread over this thin fabric in microgravity reaches a steady rate and a limiting flame length. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20180005168>: *3-1 182 W 8 s 300 s ~ 84 cm 2.3 mm/s Complete Acceleratory*
   - <https://ntrs.nasa.gov/citations/20180005168>: *Saffire-III burned for 320 sec.*
   - <https://doi.org/10.1016/j.combustflame.2018.10.012>: *The downloaded test data show that a concurrent (downstream) spreading flame over thin fabrics in microgravity reaches a steady spread rate and a limiting length.*
2. Opposed burn (S2) at about 25 cm/s: the flame spread into the flow at 0.98 mm/s over about 10 cm in 60 s. This fabric does not spread downward in 1 g (burn length ~0). At 25 cm/s the concurrent flame spread 2.3 times faster than the opposed flame, against 1.4 times at 20 cm/s in Saffire-I. *(result, high)*
   - <https://ntrs.nasa.gov/citations/20180005168>: *3-2 182 W 8 s 60 s ~ 10 cm 0.98 mm/s ~ 0 n/a*
   - <https://ntrs.nasa.gov/citations/20170008805>: *1-2 182 W 8 s 70 s ~ 10 cm 1.3 mm/s ~ 0 n/a*
3. Raising the flow from 20 cm/s (Saffire-I) to 25 cm/s (Saffire-III) increased the concurrent spread rate from 1.8 to 2.3 mm/s, a ratio of 1.28 against a flow ratio of 1.25. The burn durations (400 vs 320 s in the ASGSR slides) are in the inverse ratio. The investigators state that the concurrent flame speed is proportional to the air flow velocity. By the same scaling, the Saffire-III fire's heat release would be about 1.5 kW (our estimate; no published value). *(trend, medium)*
   - <https://ntrs.nasa.gov/citations/20180005168>: *Saffire-I burned for 400 sec*
   - <https://ntrs.nasa.gov/citations/20180005168>: *This is equal to the inverse ratio of the flame speed*
   - <https://ntrs.nasa.gov/citations/20180005168>: *The flame speed is proportional to the air flow velocity*
4. Opposed spread was slower at 25 cm/s (0.98 mm/s) than at 20 cm/s (1.3 mm/s, Saffire-I). This is consistent with the BASS finding that opposed spread over this fabric peaks at 10-15 cm/s and falls at higher flows. The comparison mixes two flights with slightly different O2 (21.2-21.0% vs ~21.5%) and only ~10 cm of burning each, so it is indicative only. *(trend, low)*
   - <https://ntrs.nasa.gov/citations/20180005168>: *3-2 182 W 8 s 60 s ~ 10 cm 0.98 mm/s ~ 0 n/a*
   - <https://doi.org/10.60555/58h4-dy80 (PSI-26 BASS, file PSI-26_Science Documents_FlammabilityAspectsofFabric_USNationalCombustion.2013.docx)>: *Opposed-flow flame spread rate increases with flow to a maximum when the flow speed is around 10 to 15 cm/s and then decreases at higher speeds, in good agreement with previous research [Olson, 1991].*
5. The actual flow was about 25 cm/s, not the 30 cm/s in the PSI record, readme and experimental table. Before each ignition the anemometers read 24.5 and 25.4 cm/s, and the investigators report 25 cm/s. The 30 cm/s value was the plan ('close to 30 cm/sec'). *(method, high)*
   - `PSI-100_Raw Data_Saffire III Sample 1 Sensors.xlsx`, sheet Calibrated Data, row row 912 (t = 30.0 s): *Anemometer 1 24.5180 cm/sec, Anemometer 2 25.4160 cm/sec*
   - `PSI-100_Experimental table_SAFFIRE-3.csv` (all): *S1 | SIBAL Fabric | .33 cm | 94 cm | 40.6 cm | 30 cm/s | Concurrent | S1C1 | S1C2*
   - <https://ntrs.nasa.gov/citations/20170002628>: *Flow will be close to 30 cm/sec as opposed to 20 cm/sec for Saffire-I*
   - <https://ntrs.nasa.gov/citations/20180005168>: *Saffire-III (25 cm/s)Saffire-I (20 cm/s)*
6. Run order and termination (our reading of the sensor files). Unlike Saffire-I, the opposed burn came first. S2 recording started at 21:10:16 UTC on 4 June 2017, with ignition at t = 60 s. Its two responding radiometers rose by at most 12-14 mW/cm2 (a small flame) and dropped back at t = 131 s, the same time the fan was switched off (anemometers ~0.15 cm/s by t = 145 s). The opposed flame was therefore ended by stopping the flow, not by running out of fuel. The concurrent burn followed at 21:13:31 UTC (ignition at t = 60 s) with the fan running throughout. *(method, medium)*
   - `PSI-100_Raw Data_Saffire III Sample 2 Sensors.xlsx`, sheet Calibrated Data, row row 3921 (t = 129.3 s) and row 4397 (t = 145.0 s): *t = 129.3 s: Radiometer 2 -5.18 (baseline -17.9), Anemometer 1 24.44; t = 145.0 s: Radiometer 2 -17.82, Anemometer 1 0.150 cm/sec*
   - `PSI-100_Raw Data_Saffire III Sample 1 Sensors.xlsx`, sheet Calibrated Data, row row 3 (Elapsed Time 0): *6-4-2017 5:13:31.148 PM*
   - `PSI-100_Science Documents_SAFFIRE-III_MergeResult-raw_Final.xlsx` (sheet Sample2 - raw): *sheet Sample2 - raw: 6276 non-empty rows*
7. Concurrent-burn radiation (our analysis): baseline-subtracted radiometer peaks were 166-168 mW/cm2 for one pair (t = 196-198 s, 136 s after ignition) and 175-187 mW/cm2 for the other pair (t = 293 s). This is about 20% above Saffire-I's 139-149 mW/cm2, and the flame reached each pair about 20% sooner, consistent with the faster spread. Signals above 5 mW/cm2 lasted from t = 64 s to t = 333 s and t = 421 s. The fan stayed on until about t = 650 s, so the concurrent flame ended by reaching the end of the fuel (the region already burned by the opposed test), not by flow shut-off. Radiometer view factors are not documented, so these are relative signals. *(result, medium)*
   - `PSI-100_Raw Data_Saffire III Sample 1 Sensors.xlsx`, sheet Calibrated Data, row row 5994 (t = 197.70 s) and row 8897 (t = 293.50 s): *t = 197.7 s: Radiometer 1 148.93 mw/cm^2 (baseline -17.5); t = 293.5 s: Radiometer 2 156.62 mw/cm^2 (baseline -17.9)*
   - <https://doi.org/10.60555/0t15-1z43 (PSI-98 Saffire-I, file PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx, sheet Calibrated Data, column maxima of baseline-subtracted radiometer columns)>: *Upstream Front 138.9, Upstream Back 139.4, Downstream Front 144.7, Downstream Back 149.1 mW/cm2*
8. Vehicle response (our analysis of PSI sensor files). Over the concurrent burn, CO2 at the Saffire sensor rose from 0.395% to 0.606% (+0.21 percentage points), consistent with the investigators' O2 drop of 21.2% to 21.0%. The opposed burn added only +0.01 points. The Saffire ambient pressure rose from 14.424 to about 14.48 psia (+0.056 psi, +0.39 kPa), peaking near t = 440 s, and the Cygnus PCM pressure sensors rose by about 0.065 psi (+0.45 kPa, from ~13.99 to 14.056 psi). The PCM air temperature rose from 20.19 to 20.70 C. This is a slightly larger response than in Saffire-I (+0.31-0.34 kPa, +0.2 C). *(result, medium)*
   - `PSI-100_Raw Data_Saffire III Sample 1 Sensors.xlsx`, sheet Calibrated Data, row row 912 (t = 30.0 s), row 13336 (t = 440.0 s), row 16685 (t = 550.5 s): *CO2 0.39427 -> 0.60552 %; Ambient Pressure 14.43054 -> 14.49000 PSIA (t = 440 s) -> 14.47141 PSIA (t = 550.5 s)*
   - `PSI-100_Raw Data_Saffire-III Telemetry Data.xlsx`, sheet CygnusData, row non-zero entries 30 min before vs during 21:11-21:25 UTC, 4 June 2017: *PCM Press EPS 1 (psi) 13.992 -> max 14.056; PCM Press EPS 3 (psi) 13.994 -> max 14.059; PCM Air Temp (degC) 20.186 -> max 20.704*
   - <https://ntrs.nasa.gov/citations/20180005168>: *III-1 Cotton-Fiberglass 40.6 cm 0.37 mm 94 cm 25 cm/s Concurrent 21.2 to 21.0*
9. Scale and duct comparisons at about 25 cm/s. The 40.6-cm sheet (2.3 mm/s) spread about 12% slower than the 5-cm Saffire-II strip burned at 25 cm/s in the same duct (2.6 mm/s), similar to the ~14% width effect at 20 cm/s (1.8 vs 2.1 mm/s). Both are far below the BASS 2-cm strips in the 7.6 cm duct: BASS spread at 2.55 mm/s at only ~10 cm/s, and its linear concurrent fits extrapolate to about 3.8-5.6 mm/s at 25 cm/s (our extrapolation beyond the BASS fit). The investigators attribute the small-duct excess to flow acceleration by hot-gas expansion. *(trend, medium)*
   - <https://ntrs.nasa.gov/citations/20180005168>: *2-6 80 W 9.2 s 115 s 29 cm 2.6 mm/s Complete Acceleratory*
   - <https://ntrs.nasa.gov/citations/20170008805>: *Compared to previous microgravity work in smaller tunnels, the flame in the larger tunnel spread more slowly, even for a wider sample. This is attributed to the effect of flow acceleration in the smaller tunnels as a result of hot gas expansion.*
   - <https://doi.org/10.60555/58h4-dy80 (PSI-26 BASS, file PSI-26_Presentations_BASS_Overview of Recent ISS Results.pdf p24-p25)>: *Concurrent and Opposed Spread at ~ 10 cm/s 2.55 mm/s versus 1.21 mm/s*
10. Sample thermocouples (our analysis) peaked at 710, 858 and 1060 C at the first station (t = 177-186 s) and 706, 1088 and 329 C at the second (t = 291-307 s). These are bead readings at several heights, uncorrected for radiation; the peak values match Saffire-I within ~3%. The flame took about 120 s between stations, against 150-165 s in Saffire-I. The ratio (~1.27) matches the spread-rate ratio 2.3/1.8, and implies the same ~28 cm station spacing in both flights. Positions are not in PSI, so this is a consistency check only. *(method, low)*
   - `PSI-100_Raw Data_Saffire III Sample 1 Sensors.xlsx`, sheet Calibrated Data, row column maxima of Sample Temp 1-6 (TC7-TC12): *TC7 710.1 C @176.9 s; TC8 857.8 @183.8; TC9 1060.0 @185.7; TC10 706.4 @307.2; TC11 1088.2 @307.2; TC12 329.5 @290.9*
   - <https://doi.org/10.60555/0t15-1z43 (PSI-98 Saffire-I, file PSI-98_Raw Data_Saffire-I Sample 1 Sensor Data Complete TM graphs.xlsx, sheet Calibrated Data, column maxima of Sample Temp 1-6 (TC7-TC12))>: *TC7 698.3 C @193.8 s; TC8 886.0 @206.7; TC9 1078.1 @204.4; TC10 688.1 @359.5; TC11 1091.8 @369.0; TC12 332.6 @344.7*

## Fire-safety relevance

Saffire-III shows how ventilation speed sets the growth of a large fabric fire in a spacecraft. A 25% increase in forced flow (20 to 25 cm/s) gave about 28% faster concurrent spread, and so roughly proportionally faster fuel consumption and heat release, while the flame still reached a steady state. Higher cabin flow therefore worsens a downstream-spreading fire. Upstream (opposed) spread slowed at the higher flow, and the gap between the two modes widened from 1.4x to 2.3x. As in Saffire-I, a fabric that will not burn downward on Earth spread against the flow in orbit, so the 1-g downward test is not conservative for opposed spread. The opposed flame went out when the fan was stopped, which supports ventilation shut-down as a first response. The relation 'flame speed proportional to air speed' and the flame-size limit let designers bound a fabric fire's heat release for a given ventilation speed. The duct-size and width effects mean that small-sample glovebox tests overestimate concurrent spread for this fabric, and that quantitative fire models must include the enclosure. The O2 use (~0.2 percentage points) and pressure rise (~0.4 kPa) give an anchor for habitability models. Results are for one thin cotton fabric at ~21% O2 and ~1 atm, not a flammability limit.

### Habitat conditions

Saffire-III burned in Cygnus cabin air at 21.2% O2 falling to 21.0%. The pressure was about 13.97-13.99 psi (96.3-96.5 kPa) on the Cygnus sensors, or 14.42 psia (99.4 kPa) on the Saffire sensor. This is close to the Earth sea-level reference (20.9% O2, 101.3 kPa) and far from exploration atmospheres such as a Moon habitat at 30% O2 or more at 70.3 kPa or less, or a spacesuit at 100% O2 at 29.6 kPa. In those atmospheres higher O2 would be expected to raise spread rates, so these results do not bound fire growth there. Elevated-O2, reduced-pressure tests were planned for the follow-on Saffire flights. The 25 cm/s flow is within the range of cabin ventilation speeds.

### Earth benefits

Fire behaviour in small, sealed volumes such as mines, aircraft and submarines; and two-flow-speed validation data for forced-flow flame-spread models.

## Limitations

- Two burns on one sample at one flow speed. The opposed burn covered only ~10 cm in 60 s and was ended by switching off the fan, so it may not have reached a steady state. The flow-speed trend rests on comparing two separate flights (Saffire-I and III) with slightly different O2 and pressure.
- The intended 30 cm/s was not achieved (about 25 cm/s), so the planned flow-speed contrast with Saffire-I was smaller than designed.
- The burn duration is reported inconsistently: 300 s in the results table and 320 s in the slide text. The radiometers show signal for about 270-360 s after ignition. The burn length (~84 cm) and spread rate cannot be cross-checked from PSI files alone.
- O2 and pressure readings disagree between instruments: the Saffire O2 sensor read ~19.8% against the 21.2% ISS-referenced value, and the Saffire and Cygnus pressure sensors differ by ~0.43 psi (3 kPa). Absolute O2 and pressure are therefore uncertain at the percent level, although the changes during the burns are consistent.
- The flame was confined in a duct whose size affects concurrent spread, so the spread rates are specific to the Saffire duct. Only a subset of the imagery was downlinked as raw frames.

## Data in PSI

PSI-100 holds 87 files (35.2 GB). Imagery dominates: 67 zips (35.1 GB, not downloaded) for the BIT, F1/F2 flow-visualisation and S1/S2 runs per camera, as jpeg, mapped jpeg, Raw2TIFF (demosaiced raw frames), mapped and exposure/gain-annotated sets. Raw-frame sets are much larger than for Saffire-I (up to 2.7 GB per zip). Downloaded and usable: 'Saffire III Sample 1 Sensors.xlsx' (690 s, 20,909 rows at 0.033 s) and 'Sample 2 Sensors.xlsx' (160 s, 4,848 rows). Their 'Calibrated Data' sheet has the same columns as Saffire-I without the radiometer position labels: fan speed, CO2, O2, anemometers, ambient pressure, 4 radiometers, humidity, inlet, plume and sample temperatures, igniter current/voltage and housekeeping. 'Saffire-III Telemetry Data.xlsx' has real-time Saffire and Cygnus telemetry (three PCM pressure sensors, air temperature, smoke detectors, cabin fans, attitude rates, accelerations) for 4 June 2017. The '1 Hz Telemetry Data.xlsx' and the EU csv (day 161) cover 5 June 2017, the day after the burns. 'Raw telemetry file.csv' gives the same channels under the flight mnemonics (P@sfsHk...). Two docx files hold sensor plots. Two MergeResult workbooks list each jpeg/raw frame with time, exposure, gain and received status (38,052 S1 and 6,276 S2 frames). There are no reduced flame data; spread rates come from NASA NTRS presentations. The three ICES presentations listed under Presentations were not downloadable from PSI, but matching versions were found on NTRS.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | image archives (BIT, F1, F2, S1, S2 x 2 cameras): jpeg, JPEG_Mapped, RAW2TIFF, Raw2TIFF_Mapped, Map_icmad, jpeg2png, distortion grids | .zip | 67 | 35.1 GB | no |
| Raw Data | calibrated sensor workbooks for Sample 1 and Sample 2, real-time telemetry plus Cygnus data, 1 Hz telemetry (5 June) | .xlsx | 4 | 57.9 MB | yes |
| Raw Data | raw telemetry with flight mnemonics, and an engineering-unit data table for day 161 (5 June 2017) | .csv | 2 | 6.9 MB | yes |
| Raw Data | sensor plots for samples 1 and 2 | .docx | 2 | 2.4 MB | yes |
| Presentations | 45th, 46th and 47th ICES Saffire presentations (not downloadable from PSI; equivalent versions on NTRS 20150022123, 20170002628, 20170008805) | .pdf | 3 | 10.2 MB | no |
| Science Documents | Saffire objectives/development/status paper, Saffire-I/III readme, image directory nomenclature v3.0, raw and jpeg frame merge logs | .pdf .docx .xlsx | 5 | 16.1 MB | yes |
| Engineering Documents | Saffire-III operations summary (downloaded); offgassing testing strategy (not downloaded) | .pdf | 2 | 1.7 MB | yes |
| Experimental table | 2 burns (S1 concurrent, S2 opposed) | .csv | 1 | 200 B | yes |
| metadata | ISA-Tab metadata zip (file name says PSI-168) | .zip | 1 | 8 kB | no |

Rows in the unified `tests` table: 2

## Related investigations

- [PSI-98](PSI-98-saffire-i.md): precursor
- [PSI-99](PSI-99-saffire-ii.md): shared hardware
- [PSI-26](PSI-26-bass.md): same fuel

## Open questions

- Measure the Saffire-III flame length, pyrolysis length and spread rate vs time from the mapped image sets. No Saffire-III flame-length value was found in the sources, so whether the 40 mm plateau of Saffire-I grows with flow is open.
- Test the 'spread proportional to flow' scaling against a model (e.g. the CWRU 3-D transient model used for Saffire-I) at 20 and 25 cm/s, including duct confinement.
- Compute the heat release rate of the Saffire-III fire from CO2 production and from spread rate x fuel loading, and compare with the 1200 W Saffire-I estimate.
- Use the three Cygnus pressure sensors and the PCM temperature to estimate the free volume and the heat lost to the structure during and after each fire.
- Check whether the Cygnus smoke detectors (FIZ obscuration/scatter) responded to the Saffire-III fire, and with what delay.

## Dashboard ideas

- **spread rate vs flow speed, large vs small samples** (`flow_cm_s`, `direction`, `spread_rate_mm_s`, `sample_width_cm`, `duct`, `investigation`): Saffire-I (20 cm/s) and III (25 cm/s) concurrent and opposed points next to Saffire-II 5-cm and BASS 1-2-cm points show the flow, width and duct effects.
- **sensor time series (S1, S2)** (`elapsed_s`, `radiometers`, `anemometers`, `fan_rpm`, `co2_pct`, `pressure_kpa`, `sample_tc_C`): Shows ignition, flame passage, opposed-burn termination at fan shut-off and the vehicle response.
- **Saffire-I vs III vehicle impact** (`flow_cm_s`, `burn_time_s`, `delta_co2_pct`, `delta_p_kPa`, `delta_T_C`): Compares cabin response of two similar fires at two flow speeds.

## Gaps and data-quality notes

- The three PSI-100 presentations (45th, 46th and 47th ICES) were not downloadable from PSI. Equivalent versions were found on NASA NTRS: 20150022123 (2015, silicone buoyancy study, not used here), 20170002628 (2016 status, pre-Saffire-III) and 20170008805 (2017 results; its results table covers Saffire-I and II only). Saffire-III numbers come from the ASGSR 2017 presentation (NTRS 20180005168). File sizes differ slightly from the PSI listings, so the NTRS versions may not be byte-identical.
- No Saffire-III flame length, pyrolysis length, flame power or flame-position plot data were found in text form. The Combustion and Flame (2019) paper covering Saffire-III is paywalled; only its abstract was read.
- The PSI record gives no end date; relay opening and Cygnus OA-7 re-entry dates were not found. The ASGSR slide lists the launch as 'Mar 27, 2017' while the PSI start date is 18 April 2017; the identity uses the PSI date.
- Data quality: the PSI record approach, the readme and the experimental table give 30 cm/s, but the anemometers and the investigators' results give ~25 cm/s. The table thickness '.33 cm' should be about 0.33-0.37 mm. The PSI 'researchImpacts' field text names Saffire-I rather than Saffire-III.
- Data quality: the 'Date / GMT' column in the MergeResult-raw workbook gives 2017-06-03, but the epoch times (e.g. 1496610866187) correspond to 2017-06-04 21:14 UTC, which agrees with the sensor workbooks ('6-4-2017 5:13 PM', EDT).
- Data quality: in the Saffire-III sensor workbooks the igniter current and voltage peak at only ~0.94 A and ~4.4 V (about 4 W), against 182 W in the investigators' table; the igniter channels appear to use a different calibration from Saffire-I's (4.1 A, 45.8 V). The radiometer columns lack the upstream/downstream labels given for Saffire-I.
- The '1 Hz Telemetry Data.xlsx' and 'Saffire_Data_Table2017.161...-EU.csv' cover 5 June 2017 (19:35-21:30 UTC), the day after the burns, so they do not contain the fires.
- Sensor-derived values in findings (pressure, CO2, radiometer and thermocouple peaks, run order) are our computations from the PSI workbooks, not published numbers.
- No text addressed to an AI or unrelated instructions were found in the PSI-100 documents.
