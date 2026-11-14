# PSI-99: SAFFIRE-II (Spacecraft Fire Experiment-II)

Nine strip-shaped samples of spacecraft materials were set alight inside an empty cargo spacecraft in orbit to see whether they burn more or less readily than in NASA's standard ground flammability test; silicone and Nomex would not burn in weightlessness, while a cotton-fibreglass fabric and thick acrylic burned but with flames that stopped growing.

Investigators: David L. Urban (NASA Glenn Research Center) - Principal Investigator; Gary A. Ruff (NASA Glenn Research Center) - Investigator

## At a glance

| | |
|---|---|
| Platform | Orbital ATK Cygnus resupply vehicle (OA-5 mission), after unberthing from the ISS; uncrewed |
| Facility | Cygnus Pressurized Cargo Module |
| Dates | 2016-09-30 to 2017-04-01 |
| Fuels and samples | Silicone sheet, 0.27, 0.61 and 1.03 mm thick; SIBAL cotton-fibreglass fabric; Composite; PMMA slab, nominal 1 cm thick |
| Varied | material: silicone, SIBAL cotton-fibreglass fabric, PMMA-to-Nomex composite, thick PMMA (flat and grooved)<br>sample thickness: 0.27-1.03 mm (silicone); 0.37 mm (fabric); 0.85/0.37 mm (PMMA/Nomex); 10 mm (PMMA, grooved centre 4 mm) mm<br>spread direction relative to forced flow: concurrent (8 samples), opposed (sample 2-4 only)<br>forced air flow velocity: 20 (8 samples); 25 (sample 2-6) cm/s<br>igniter power and duration: 80 W for 9.2 s (2-1 to 2-7); 97 W for 30 s (2-8, 2-9) W, s |
| Number of tests | 9 |
| Fire-safety pillars | prevention, fundamental |

## Question

Saffire-II asked whether NASA's normal-gravity material screening test (NASA-STD-6001 Test 1, an upward-burning test on 5 cm x 30 cm strips in which a material fails if more than 15 cm burns) gives flammability limits that hold in long-duration microgravity with spacecraft-like ventilation. Its two stated objectives were to find how fast a large fire grows in low gravity and to compare low-g flammability limits with those from the 1-g screening test. The hypothesis is that fire behaviour differs enough between 1 g and low gravity that designing spacecraft fire safety from terrestrial tests and standards carries real but unquantified risk. That risk grows for exploration missions far from Earth, and microgravity data for designers are scarce. The approach was to burn materials whose 1-g limits lie near the cabin atmosphere (about 21% O2) in an expendable, uncrewed vehicle, so that whether a flame spreads or self-extinguishes is itself the result.

## Summary

Saffire-II burned nine 5 cm x 29 cm samples in a fan-driven flow duct aboard the uncrewed Cygnus OA-5 vehicle after it left the ISS in late 2016. Samples were sized and ignited like NASA-STD-6001 Test 1 (736 J over 9.2 s) so that microgravity flammability could be compared with this 1-g upward screening test. Air flowed at 20 cm/s (25 cm/s for one sample) with about 22.1% O2 near 100 kPa. None of four silicone sheets (0.27-1.03 mm) spread a flame, although the 0.27 mm sheet is fully consumed in 1-g tests and the 0.37 mm sheet burns downward in 1 g. Nomex HT90-40 did not ignite even after about two minutes of heating by a roughly 460 W PMMA pilot flame. Cotton-fibreglass fabric burned completely at a steady 2.1 mm/s (20 cm/s) and 2.6 mm/s (25 cm/s), instead of accelerating as in 1 g. Flames on 1 cm thick PMMA stayed anchored at a limiting size for 10-15 minutes. At these flows the 1-g test was conservative for these materials, and concurrent flames reached a bounded size.

## Physics

On Earth a flame climbing a vertical strip is driven by its own buoyant plume. The hot gas accelerates upward, thins the boundary layer and lengthens the flame, so the flame heats more fuel ahead of it and spread accelerates. In orbit there is no buoyancy. The only flow is the forced ventilation, here 20-25 cm/s, which is slower than typical buoyant velocities. In concurrent (flow-assisted) spread the flame then settles to a limiting length, set by the point where the net heat flux at the flame tip falls to zero. A thin fuel then spreads steadily. A thick fuel burns out more slowly than its pyrolysis zone extends, so the flame stays anchored near the upstream edge and its spread is controlled by burnout (regression). A slower flow also means a thicker boundary layer, lower convective heat flux to the solid and relatively larger radiative losses. Materials that only just burn in 1 g can therefore be extinguished. Silicone adds a complication: it produces silica powder that can deposit on fresh fuel as an insulating layer, and buoyant flow may sweep it away in 1 g but not in microgravity. Opposed-flow (downward) spread is governed by the heat conducted forward through the gas against the flow.

$$
U_m = U_f\,\frac{P}{P_0}\left[\frac{g^2 l_p^2}{U_f^4} + 1\right]^{1/4}
$$

Mixed-convection velocity used by Thomsen et al. to compare Saffire-II thick-PMMA concurrent spread with 1-g reduced-pressure tests. $U_m$ is the equivalent pure forced-flow velocity (m/s) that gives the same boundary-layer thickness; $U_f$ is the forced-flow velocity (m/s, 0.2 m/s in both the flight and ground tests); $P$ is ambient pressure and $P_0$ the reference sea-level pressure (kPa); $g$ is gravitational acceleration (m/s2); $l_p$ is the characteristic pyrolysis length (m, taken as half the sample length). For $g=0$ it reduces to $U_m = (P/P_0)U_f$. In 1 g, lowering $P$ lowers $U_m$ toward the microgravity value. The authors estimate about 20 kPa would be needed to mimic microgravity, where flame chemistry is no longer pressure-independent.

<https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *the following expression is obtained for the mixed flow velocity in terms of pressure, forced flow velocity component of the mixed flow, and gravity.*
<https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *This is important since it would be necessary to reduce the pressure to values of the order of 20 kPa to simulate microgravity conditions*

$$
V_f \approx l_h\,\frac{4\,[h\,(T_f - T_p)]^2}{\pi\,k_s\,\rho_s\,c_s\,(T_p - T_o)^2}
$$

Heat-transfer-limited concurrent flame spread rate over a thermally thick solid, as used by Thomsen et al. $V_f$ is the spread rate (m/s); $l_h$ is the heated length of solid downstream of the pyrolysis front (m); $h$ is the convective heat-transfer coefficient from flame to surface (W/m2 K), scaling as $U_m^{1/2}$ for a forced laminar boundary layer; $T_f$, $T_p$ and $T_o$ are the flame, pyrolysis and initial solid temperatures (K); $k_s$, $\rho_s$ and $c_s$ are the solid conductivity (W/m K), density (kg/m3) and specific heat (J/kg K). It assumes flame radiation to the surface roughly balances surface re-radiation and that gas-phase chemistry is fast. The authors note this breaks down at low velocity, low pressure or in microgravity, which is why the model somewhat under-predicts the Saffire-II rate.

<https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *From Eq. (2) it is seen that the flame spread rate is proportional to the heating length and the square of the convective heat transfer coefficient at the solid surface*
Textbook background: Thermally thick spread-rate formula (de Ris / Fernandez-Pello type).

$$
\dot{Q} \approx \rho_A\,W\,V_f\,\Delta H_c
$$

Order-of-magnitude heat release rate of a steadily spreading flame over a thin sheet. $\dot{Q}$ is flame power (W); $\rho_A$ is fuel areal density (kg/m2, 0.18 kg/m2 for the cotton-fibreglass SIBAL fabric, of which only the cotton burns); $W$ is sample width (m); $V_f$ is spread rate (m/s); $\Delta H_c$ is the effective heat of combustion of the burnable fraction (J/kg). It shows why the 5 cm wide Saffire-II fabric strip (reported 200 +/- 50 W) released far less power than the 40.6 cm wide Saffire-I sheet (1200 +/- 300 W) at similar spread rates. It applies only when the burning region has reached a steady length.

Textbook background: Steady-spread energy balance; the investigators' exact flame-power method is not documented in the sources reached.
<https://ntrs.nasa.gov/api/citations/20180005168/downloads/20180005168.pdf>: *Overall area density: 18 mg/cm2*

## Method

### Apparatus

The Saffire flight unit sat in the Cygnus Pressurized Cargo Module. It was a rectangular flow duct, about 460 mm x 510 mm in cross section. Fans at the top drew cabin air through it, and flow straighteners sat at the bottom. For Saffire-II the large single sample used in Saffire-I and -III was replaced by a card holding nine samples, each about 5 cm x 29 cm, mounted mid-duct so air passed on both faces. Each sample was ignited by a resistively heated hot wire (29-gauge Kanthal) at its leading edge. Instruments were two cameras (camera images were the primary diagnostic), thermocouples for flow, flame and plume temperature, radiometers, solid-state O2, CO2 and pressure sensors, and two anemometers. The PSI record says two radiometers; Thomsen et al. say four. Data were compressed and downlinked before the vehicle re-entered.

### Fuels and samples

- Silicone sheet, 0.27, 0.61 and 1.03 mm thick (samples 2-1 to 2-3, concurrent/upward) and 0.37 mm (sample 2-4, opposed/downward) (solid, sheet, 5 cm x 29 cm)
- SIBAL cotton-fibreglass fabric (75% cotton, 25% fibreglass, 18 mg/cm2, 0.37 mm), samples 2-5 and 2-6, identical to the Saffire-I/III fabric (solid, thin fabric, 5 cm x 29 cm)
- Composite: thin PMMA sheet (0.8-0.85 mm, first 5 cm) leading into Nomex HT90-40 meta-aramid fabric (0.37 mm, remaining 24 cm), sample 2-7 (solid, sheet plus fabric, 5 cm wide)
- PMMA slab, nominal 1 cm thick: sample 2-8 'structured' with a grooved centre (middle 1.8 cm wide portion only 0.4 cm thick) and sample 2-9 flat (solid, thick slab, 5 cm x 29 cm)

### Procedure

Saffire-II was integrated into the OA-5 Cygnus on 12 May 2016, launched on an Antares from Wallops on 17 Oct 2016 and operated on 21 Nov 2016. It stayed dormant while Cygnus was docked; once the vehicle had unberthed it was run from the ground and the data downlinked before re-entry. Flow-visualisation runs were recorded before samples 2-1 and 2-2. The samples were burned one at a time in cabin air: about 22.1% O2 initially (an ISS reading), falling to 21.9% by the last PMMA test, near 100 kPa. Air speed was 20 cm/s for all samples except 2-6 (25 cm/s). Samples 2-1 to 2-7 were ignited at 80 W for 9.2 s (736 J), mimicking the NASA-STD-6001 Test 1 igniter. The thick PMMA samples 2-8 and 2-9 used 97 W for 30 s. All burns were concurrent (upward relative to the flow) except 2-4, which was ignited at the downstream end to spread against the flow. Burn length and spread rate were compared with 1-g tests on matching samples (upward, Test-1-like; downward for the 0.37 mm silicone).

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| material | silicone, SIBAL cotton-fibreglass fabric, PMMA-to-Nomex composite, thick PMMA (flat and grooved) |  |
| sample thickness | 0.27-1.03 mm (silicone); 0.37 mm (fabric); 0.85/0.37 mm (PMMA/Nomex); 10 mm (PMMA, grooved centre 4 mm) | mm |
| spread direction relative to forced flow | concurrent (8 samples), opposed (sample 2-4 only) |  |
| forced air flow velocity | 20 (8 samples); 25 (sample 2-6) | cm/s |
| igniter power and duration | 80 W for 9.2 s (2-1 to 2-7); 97 W for 30 s (2-8, 2-9) | W, s |

Held constant:

- atmosphere: Cygnus cabin air, O2 about 22.1% initially (derived from measured CO2 production referenced to the ISS O2 reading), drifting to 21.9% over the PMMA burns; about 100 kPa
- sample planform: 5 cm wide x 29 cm long (NASA-STD-6001 Test 1 geometry)
- gravity: microgravity in free-flying Cygnus

Number of tests: 9

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| whether the flame propagated or self-extinguished; burn length | two video cameras | derived |
| flame spread rate (flame-tip or flame-base position versus time) | video image processing | derived |
| O2 and CO2 mole fraction and pressure upstream of the samples (O2 during burns derived from CO2 production) | solid-state sensors | direct |
| flow, flame and plume temperatures | thermocouples | direct |
| flame radiation | radiometers (two per PSI record, four per Thomsen et al.) | direct |
| duct flow velocity | two anemometers | direct |
| average flame power | estimated from fuel consumption | derived |

## Findings

1. No flame spread on silicone in microgravity. None of the four silicone sheets (0.27, 0.61 and 1.03 mm concurrent; 0.37 mm opposed; 20 cm/s air, about 22.1% O2; the PSI table lists sample 2-1 at about 21.5% while the published Table I (NTRS 20170008805) gives about 22.1%) propagated. After the 9.2 s, 80 W igniter switched off, a tiny gas-phase flame remained briefly, did not spread and went out. Burn time was 'insignificant' and microgravity burn length about 0 for all four. *(null_result, high)*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *Results were convincing although rather anticlimactic as none of the silicone samples burned.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *When the igniter was powered off, a tiny gas phase flame remained but did not spread and quickly extinguished.*
   - `PSI-99_Experimental table_SAFFIRE-2.csv` (all): *2-1 | Silicone | 0.27 mm | 29 cm | 5 cm | 20 cm/s | ~ 21.5 | 80 W | 9.2 s | Insignificant | Concurrent | ~ 0 | n/a | Complete | Acceleratory*
   - `PSI-99_Experimental table_SAFFIRE-2.csv` (all): *2-4 | Silicone | 037 mm | 29 cm | 5 cm | 20 cm/s | ~ 22.1 | 80 W | 9.2 s | Insignificant | Opposed | ~ 0 | n/a | Complete | 0.6 mm/s*
2. Silicone was less flammable in microgravity than in the 1-g test. In 1-g tests on matching samples, the 0.27 mm silicone burned completely with accelerating upward spread, the 0.61 mm burned on average 7.6 cm of 30 cm (1.2 mm/s) and the 1.03 mm did not burn. The 0.37 mm sheet burned completely downward at 0.6 mm/s. Published 1-g Test 1 minimum oxygen concentrations (MOC; the term used by the cited source) for silicone are 18% (0.25 mm), 20% (0.61 mm) and 22% (1.00 mm), so the roughly 22.1% O2 flight atmosphere was at or above the 1-g MOC for every thickness. The investigators conclude silicone flammability in microgravity is reduced compared with 1 g, at least at 20 cm/s. This was unexpected: cellulose and PMMA experience suggested that a material that burns upward in 1 g would also burn in microgravity at moderate flow. *(limit, high)*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *The 0.61-mm thickness burned on average 7.6 cm of the available 30 cm before extinguishing*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *In downward burning, normal gravity tests, this thickness was completely consumed.*
   - <https://ntrs.nasa.gov/api/citations/20150022421/downloads/20150022421.pdf>: *Thickness MOC ULOI 1.00 mm 22 23.4 0.61 mm 20 22.8 0.36 mm 19 21 0.25 mm 18 19.7*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *Flammability of silicone in microgravity appears to be reduced compared to normal gravity, at least for the flow speeds tested.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *Previous experience with cellulosic fuels (paper and fabric) and even PMMA suggested that if a flame could persist in upward 1-g tests then it would also burn in microgravity at a moderate flow speed which was less than that typical in buoyant flow.*
   - `PSI-99_Experimental table_SAFFIRE-2.csv` (all): *2-2 | Silicone | 0.61 mm | 29 cm | 5 cm | 20 cm/s | ~ 22.1 | 80 W | 9.2 s | Insignificant | Concurrent | ~ 0 | n/a | 7.6 cm | 1.2 mm/s*
3. Proposed mechanism for silicone (a hypothesis, not tested). Burning silicone makes fine silica that may deposit on fresh fuel and block pyrolysis. Buoyant flows of order 60-80 cm/s in 1 g may sweep the silica away and aid cracking and flaking that exposes fresh fuel. The 20 cm/s forced flow may not. Ground tests found an insulating silica layer (286 µm at the self-extinguishment point on a 0.36 mm sample) on upward-burning samples. The investigators call for microgravity repeats at 60-80 cm/s. *(trend, low)*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *Silicone produces fine silica powder as it burns, which could be deposited on the fuel and impede pyrolysis.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *It would be interesting to repeat these tests in microgravity but at a much higher flow speed of around 60 to 80 cm/s, which is more typical of the level in 1-g.*
   - <https://ntrs.nasa.gov/api/citations/20150022421/downloads/20150022421.pdf>: *It has been shown that this layer acts as a thermal barrier, which prohibits the fuel from reaching the pyrolysis temperature fast enough to sustain flame spread.*
   - <https://ntrs.nasa.gov/api/citations/20150022421/downloads/20150022421.pdf>: *Figure 12 shows a silica layer of 286 µm at the point of self-extinguishment on top of the originally 0.36-mm-*
4. Nomex did not ignite under a pilot flame. Nomex HT90-40 is a meta-aramid fabric common on the ISS and rated safe by Test 1; in 1 g it burns only at about 24-25% O2. In sample 2-7 it did not ignite in microgravity (20 cm/s, about 22.1% O2). This was despite about 2 minutes of heating by the plume of the leading 5 cm PMMA sheet, whose average flame power was about 460 +/- 50 W. The PMMA was fully consumed (140 s burn). The first 1 cm of Nomex was significantly damaged and the first 5 cm blackened, partly perhaps by soot. The 1-g comparison likewise gave about 0 Nomex burn length. *(null_result, high)*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *On Earth, it will only burn if the oxygen concentration is increased to around 24 to 25%.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *It took about two minutes for the PMMA to be consumed, all the while the flame plume was extending over and heating the base of the Nomex® fabric.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *Despite this significant heating load, the fabric was not ignited.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *The first 1-cm of the fabric was significantly damaged, the first 5-cm was completely blackened, and the remainder had a black streak down its center.*
   - `PSI-99_Experimental table_SAFFIRE-2.csv`, sheet PSI-99_Experimental table_SAFFIRE-2.csv, row Note 2: *Note 2 The PMMA portion was completely consumed but the Nomex was not ignited.*
5. Cotton-fibreglass fabric burned completely at a steady rate. The 5 cm wide SIBAL strips burned their full 29 cm in microgravity at steady concurrent spread rates of 2.1 mm/s (20 cm/s air, 145 s burn) and 2.6 mm/s (115 s). For the second strip (2-6) the published paper (NTRS 20170008805) gives 25 cm/s flow, but the PSI table lists 20 cm/s. In 1 g the same strips burned completely with accelerating spread. The 2.1 mm/s is marginally faster than the 1.8 mm/s of the 40.6 cm wide Saffire-I sheet at 20 cm/s. The investigators attribute this partly to the higher starting O2 (22.1% vs 21.7%) and possibly to side entrainment on the narrow strip. *(result, high)*
   - `PSI-99_Experimental table_SAFFIRE-2.csv` (all): *2-5 | Cotton-Fiberglass (SIBAL) | 037 mm | 29 cm | 5 cm | 20 cm/s | ~ 22.1 | 80 W | 9.2 s | 145 s | Concurrent | 29 cm | 2.1 mm/s | Complete | Acceleratory*
   - `PSI-99_Experimental table_SAFFIRE-2.csv`, sheet PSI-99_Experimental table_SAFFIRE-2.csv, row 2-6: *2-6,,037 mm,29 cm,5 cm,20 cm/s,~ 22.1,80 W,9.2 s,115 s,Concurrent,29 cm,2.6 mm/s,Complete,Acceleratory*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *The flame spread rate for the 5-cm-wide sample is marginally faster compared to the spread rate for the 40.6-cm-wide sample for the same flow speed of 20 cm/s (2.1 compared to 1.8 mm/s).*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *This is partly due to the slightly higher starting oxygen percentage (22.1% vs. 21.7%).*
6. Flame power scaled with sample width. The 5 cm wide Saffire-II fabric flame averaged about 200 +/- 50 W, against 1200 +/- 300 W for the 40.6 cm wide Saffire-I sheet. Igniter energy per unit width was higher on Saffire-II: 80 W for 9.2 s, 16 W/cm, versus 4.1 W/cm on Saffire-I. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20180005168/downloads/20180005168.pdf>: *Saffire 2: 200 +/- 50 W*
   - <https://ntrs.nasa.gov/api/citations/20180005168/downloads/20180005168.pdf>: *16 W/cm (per unit fuel width)*
7. Thick PMMA flames stayed anchored at a limiting size. On both 1 cm PMMA slabs (20 cm/s, about 22% O2) the flames stayed anchored at the upstream base and approached a steady, non-growing size with a limiting pyrolysis length. Burns lasted 600 s (2-8, grooved) and 900 s (2-9, flat). About 10 cm of each sample showed significant visible damage, and the base regressed very slowly (0.01-0.04 mm/s). In 1 g the same samples burned completely with accelerating spread. In microgravity, spread is therefore controlled by burnout (regression), not by flame growth. *(result, high)*
   - `PSI-99_Experimental table_SAFFIRE-2.csv`, sheet PSI-99_Experimental table_SAFFIRE-2.csv, row 2-9: *2-9,,1 cm,29 cm,5 cm,20 cm/s,22.0 to 21.9,97 W,30 s,900 s,Concurrent,~ 10 cm (note 4),Note 4,Complete,Acceleratory*
   - `PSI-99_Experimental table_SAFFIRE-2.csv`, sheet PSI-99_Experimental table_SAFFIRE-2.csv, row Note 4: *Note 4 The flames remain anchored at the base of the sample which has a very slow regression rate (0.01 to 0.04 mm/s)*
   - <https://doi.org/10.1016/j.combustflame.2018.10.012>: *The flame over the thick PMMA sample approaches a non-growing, steady state in the 15 min burning duration and has a limiting pyrolysis length.*
   - <https://www.research.ed.ac.uk/en/publications/ff08285f-8ff9-4f69-a81e-3bb66b589ad9>: *The limiting length implies that the spread rate of the flame will be controlled by the regression rate (burnout rate) of the material because the flames remains anchored to the upstream end of the fuel samples.*
8. Geometry changed the thick-PMMA flame shape. On the grooved slab (2-8: 10 mm thick with a 4 mm thick, 1.8 cm wide centre section) the thin centre burned through. This formed a deep inverted-V notch, and the investigators argue it raised heat transfer to the solid through an effectively wider flame base. *(result, medium)*
   - <https://www.research.ed.ac.uk/en/publications/ff08285f-8ff9-4f69-a81e-3bb66b589ad9>: *the grooved sample developed a deep inverted-V shaped notch as the thin center section burned through.*
   - <https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf>: *The middle 1.8-cm-wide portion of Sample 2-8 is only 0.4 cm thick.*
9. Turning off the flow put the thick-PMMA flames out quickly. This supports the ISS response of shutting down ventilation on a fire alarm. *(result, medium)*
   - <https://www.research.ed.ac.uk/en/publications/ff08285f-8ff9-4f69-a81e-3bb66b589ad9>: *The rapid extinction of the flame when the flow was turned off also supports the existing fire mitigation strategy on the ISS to deactivate the ventilation system in the event of fire alarm.*
10. Flight versus ground PMMA spread. Concurrent spread over the 10 mm flat PMMA (2-9) in microgravity at 100 kPa and 20 cm/s was significantly slower than in 1 g at the same pressure and forced flow. In 1-g tests on 15 cm slabs at 100-40 kPa, lowering the pressure slowed spread toward the flight value. A mixed-convection correlation extrapolated to low pressure predicted the flight rate fairly well, slightly under-predicting it. Roughly 20 kPa would be needed in 1 g to match microgravity, a regime where pressure also alters flame chemistry. The pyrolysis front could not be tracked in the flight images, so the flight rate is from the flame tip. *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *It is seen that the microgravity flame spread rate is significantly lower than in normal gravity at the same ambient pressure, indicating that the buoyantly induced flow velocity plays an important role in normal gravity concurrent flame spread.*
   - <https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *The extrapolation of the correlation to low pressures predicts well the flame spread rate obtained in microgravity in the Saffire II experiments.*
   - <https://ntrs.nasa.gov/api/citations/20200000557/downloads/20200000557.pdf>: *It was not possible to track pyrolysis front from the Saffire II images because the flame covered the pyrolysis region and its luminosity prevented its visualization.*
11. Bounded flame size across materials. Across Saffire-I to -III, concurrent flames over thin fabric reached a steady spread rate and limiting length, and thick PMMA reached a limiting size. Upward spread at 1 g on the same samples accelerated ('Acceleratory' in the 1-g column for 2-1 (silicone), 2-5 and 2-6 (fabric) and 2-8 and 2-9 (PMMA); silicone 2-2 spread at 1.2 mm/s and 2-4 at 0.6 mm/s downward). The investigators note that a bounded flame size can be used to set the design heat-release rate in a vehicle. *(result, high)*
   - <https://doi.org/10.1016/j.combustflame.2018.10.012>: *The existence of a flame size limit has important considerations for spacecraft fire safety as it can be used to establish the heat release rate in the vehicle.*
   - Table `tests`: extra '1-g Spread Rate' = 'Acceleratory' for samples 2-1, 2-5, 2-6, 2-8, 2-9

## Fire-safety relevance

Saffire-II gave the first direct test, in long-duration microgravity, of whether the upward 1-g screening test (NASA-STD-6001 Test 1) is conservative. At about 22% O2 and 20-25 cm/s ventilation it was for every material flown. Silicone that burns completely in 1 g, and Nomex at the edge of its 1-g limit, would not sustain spread. Fabric and thick PMMA that burn in 1 g also burned in microgravity, but at steady or bounded size rather than accelerating. Bounded flames make flashover unlikely and let designers bound heat release. However, long-burning anchored flames can build up fuel vapour in a closed vehicle, and the investigators flag a possible backdraft hazard. Flames out quickly once flow stopped, supporting ventilation shutdown on alarm. Transferability limits: one sample per condition, only about 22% O2 at about 100 kPa, and only 20-25 cm/s flow. The silicone result may reverse at higher flows (60-80 cm/s was suggested). Opposed spread was tested on one sample only. Small (5 cm) strips do not represent large fires.

### Habitat conditions

All burns were in Cygnus cabin air at about 22.1-21.9% O2 and about 100 kPa. That is essentially the Earth sea-level / ISS atmosphere (20.9% O2 at 101.3 kPa), slightly O2-enriched. Nothing was tested at the proposed Moon-habitat atmosphere (30% O2 or more at 70.3 kPa or less) or at spacesuit conditions (100% O2 at 29.6 kPa). The material limits seen here (silicone and Nomex non-flammable, fabric and PMMA flammable) therefore cannot be carried over to enriched exploration atmospheres. For example, the 1-g Nomex threshold of about 24-25% O2 would be exceeded there. The follow-on Saffire-IV to -VI were defined to characterise fire growth in high-O2, low-pressure atmospheres. Ventilation speeds of 20-25 cm/s are typical of spacecraft air circulation.

### Earth benefits

The PSI record says that studying fire in small, sealed volumes benefits fire safety and prevention in mines, aircraft and submarines. The thick-PMMA flight data also validated a reduced-pressure ground method for approximating weak-buoyancy burning. No specific terrestrial application is documented.

## Limitations

- One sample per material and thickness, and one flow speed for most materials (20 cm/s; 25 cm/s for one fabric strip). Flammability limits are bracketed by pass or fail at a single condition, not mapped.
- Oxygen was not controlled. It was the cabin value (about 22.1%, inferred during burns from CO2 production) at about 100 kPa. No enriched or reduced-pressure atmospheres were tested.
- The silicone non-result may depend on flow speed: 20 cm/s is below typical 1-g buoyant velocities. The mechanism (silica deposition, flaking) is a hypothesis, not a measurement.
- Samples were 5 cm wide strips, and the duct is much larger than the samples. Earlier Saffire results showed concurrent spread is sensitive to duct size, so rates may not transfer to other enclosures or to larger fuel areas.
- For thick PMMA the pyrolysis front was hidden by the flame, so microgravity spread rates come from flame-tip tracking and are approximate.
- Some Nomex discolouration may be soot deposited from the PMMA pilot flame rather than pyrolysis, so the degree of Nomex damage is uncertain.
- PSI contains only the summary table, so none of the time-resolved data (video, temperatures, radiometers, O2/CO2) can be analysed from PSI. The 1-g comparison values are averages from ground tests whose replicate counts are not given in the table.

## Data in PSI

PSI holds only a one-page summary table and an ISA-Tab metadata zip. The table lists the nine samples with material, thickness, size, flow, O2, igniter settings, burn time, flow direction, microgravity burn length and spread rate, 1-g burn length and spread rate, and camera file IDs. The metadata zip repeats the record text. The table reproduces Table I of the investigators' papers, with transcription errors (see gaps). Flight video, sensor time series and the 'Experimental Details' file named in the approach text are not in PSI. The record's totalFileSize (16.9 GB) suggests those data exist on the server but were not part of what was downloaded or listed. The findings can be checked against the table but not re-derived.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | summary of the nine Saffire-II samples, conditions and burn outcomes (with 1-g comparison) plus notes | .csv | 1 | 2 kB | yes |
| metadata | ISA-Tab investigation/study files (zip named after PSI-167) | .zip .txt | 1 | 11 kB | yes |

Rows in the unified `tests` table: 9

## Related investigations

- [PSI-98](PSI-98-saffire-i.md): precursor
- [PSI-100](PSI-100-saffire-iii.md): follow-on
- [PSI-26](PSI-26-bass.md): same fuel
- [PSI-25](PSI-25-bass-ii.md): same fuel

## Open questions

- Repeat the silicone and Nomex tests at higher forced flow (60-80 cm/s) and at enriched O2 / reduced pressure to locate the actual microgravity limits, rather than single pass/fail points.
- If the flight video and sensor data behind the 16.9 GB file size can be obtained, extract flame length versus time for the SIBAL and PMMA samples to quantify limiting length and heat release, and compare with the Saffire-I/III wide-sample data.
- Quantify how close each flight sample was to its 1-g MOC (Test 1 MOC is known for silicone; obtain it for SIBAL, Nomex HT90-40 and PMMA) to build a 1-g versus microgravity flammability comparison chart.
- Use the downward 0.37 mm silicone (complete in 1 g, no spread in microgravity) to test opposed-flow spread models that include silica deposition.
- Compare the thin-fabric 2.1/2.6 mm/s rates with BASS (PSI-26) narrow-duct SIBAL data to separate flow-speed, width and duct-size effects.

## Dashboard ideas

- **1-g versus microgravity outcome matrix** (`sample`, `material`, `thickness_mm`, `flow_direction`, `ug_burn_length`, `ug_spread_rate_mm_s`, `1g_burn_length`, `1g_spread_rate`): The core Saffire-II result: which materials burn in each environment, directly from the PSI table.
- **silicone thickness versus burn length** (`thickness_mm`, `1g_burn_length_cm`, `ug_burn_length_cm`, `1g_MOC_pct`, `x_o2`): Shows the reversal: 1-g burn length falls with thickness while the microgravity burn length is zero at all thicknesses despite O2 at or above the 1-g MOC.
- **habitat atmosphere overlay** (`x_o2`, `pressure_kPa`): Places the single Saffire-II atmosphere (about 22% O2, about 100 kPa) against Moon-habitat and spacesuit atmospheres to show the untested region.

## Gaps and data-quality notes

- PSI has no Science Documents, Reports, Presentations or data for PSI-99: only the experimental table CSV and a metadata zip. The 'Experimental Details file in the Science document folder' named in the approach is not present. Results come from the table, the record text and external sources.
- Table header defects: the '?-g' columns are 'µ-g' with the µ lost. The '?-g Spread Length' column holds spread rates in mm/s ('µ-g Spread Rate' in the published Table I). The header 'Samle Thickness' is misspelt and 'Sample Length' has no unit.
- Table value errors against the published Table I (NTRS 20170008805, 20180005168): thickness '037 mm' for 2-4, 2-5 and 2-6 is 0.37 mm. Material is blank for 2-6 (Cotton-Fiberglass/SIBAL) and 2-9 (flat PMMA). Air flow for 2-6 is listed as 20 cm/s but published as 25 cm/s. O2 for 2-1 is '~ 21.5' but published as '~ 22.1'. Camera IDs 'S56C2' (2-6) and Camera 2 = 'S4C1' (2-4) look like typos. Sample 2-8 thickness 'See Fig. 5' refers to a figure not in PSI (grooved 10 mm slab with 4 mm, 1.8 cm wide centre).
- tests.csv inherits these errors: fuel blank for 2-6 and 2-9, flow_cm_s = 20 for 2-6, x_o2 = 0.215 for 2-1, and the '?-g' column names. The evidence.parquet chunk for the CSV stops after row 5, so rows 6-9 and the notes are cited as psi_table from the CSV.
- PSI approach text says flow was 20 or 30 cm/s; all publications give 20 or 25 cm/s. It says two radiometers; Thomsen et al. say four. The 30 cm/s value was planned for Saffire-III in 2016 papers.
- PSI dates (2016-09-30 to 2017-04-01) are not the flight dates. Per NASA slides, launch was 17 Oct 2016 and operations 21 Nov 2016.
- Record totalFileSize (16,931,016,137 bytes, about 16.9 GB) does not match the two files listed (about 12.5 kB). The metadata zip is named 'PSI-99_metadata_PSI-167_SAFFIRE-II.zip'. Study design descriptors include 'SHS', 'Smoldering' and 'Smoke Distribution', which do not apply to Saffire-II.
- Two of the seven record publications are not Saffire-II results: Li et al. 2019 (Saffire-I fabric modelling) and Wang et al. 2020 (ground sensor evaluation for Saffire). The record lists 7 publications and the metadata says 7, but only 5 have DOIs.
- Full texts of Urban et al. 2019 (Combust. Flame 199) and Olson et al. 2019 (Fire Technol.) were not reachable. The Elsevier abstract was read via the Semantic Scholar API, and the Olson abstract from the University of Edinburgh repository page; the accepted-manuscript PDF there returned HTTP 403 / Cloudflare challenge. Quantitative flame lengths and thick-PMMA spread rates in those papers were therefore not extracted. The ICES 2015 silicone paper (Niehaus et al.) was read via NTRS 20150022421.
- The 'average flame power' figures (200 +/- 50 W fabric; 460 W PMMA) are from conference slides. Their derivation is not documented, and the PMMA value is printed as '460 + 50 W', probably '+/-'.
- No personal data copied. The metadata contains investigator e-mail addresses, which were not reproduced. No text addressed to an AI was found.
