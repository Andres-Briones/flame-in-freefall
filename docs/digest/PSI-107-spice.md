# PSI-107: SPICE (Smoke Point In Co-flow Experiment)

Astronauts on the Space Station burned tiny gas jets in a gentle, adjustable air stream and turned the fuel up until each flame just started to give off smoke, to learn how air flow and burner size control soot release when there is no gravity.

Investigators: David L. Urban (PI; NASA Glenn Research Center; succeeded the original PI, the late Gerard M. Faeth, University of Michigan, in 2006); Peter B. Sunderland (Co-I; University of Maryland); Zeng-Guang Yuan (Project Scientist; National Center for Space Exploration Research)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS) |
| Facility | Microgravity Science Glovebox (MSG) |
| Dates | 2009-02-14 to 2009-06-23 |
| Fuels and samples | ethylene; propane; propylene; 75% propylene / 25% nitrogen; 50% propylene / 50% nitrogen; methane |
| Varied | fuel: ethylene, propane, propylene, 75% and 50% propylene in N2, methane<br>burner (nozzle) inner diameter: 0.4064, 0.762, 1.6002 (nominal 0.41, 0.76, 1.6) mm<br>co-flow air velocity: 5.4-65 at smoke points; 0.66-85.3 in the run log (fan minimum gives about 0-10 depending on outlet-screen clogging) cm/s<br>fuel flow rate: 0-4.40 mg/s hydrocarbon (0-231 sccm actual fuel); smoke points at 0.39-3.89 mg/s mg/s<br>fuel jet exit velocity at smoke point: 11.2-763 cm/s |
| Number of tests | 526 logged flame conditions in the master sheet (the approach and final report call these '526 flames'); 469 rows in the PSI experimental table (the master minus the 57-row GMT 062 methane session); 108 + 155 = 263 'test points' per the 30-day report; '200 data points' per the 2011 crew training; 52 smoke points in the final-report table (55 in its closing remarks and 55 in the smoke-point review sheet). |
| Fire-safety pillars | fundamental, detection |

## Question

Laminar smoke points are a standard measure of how readily a fuel forms soot, and on Earth they are shaped by buoyancy. In a 1988 paper Glassman predicted that non-buoyant flames would not have smoke points at all, but aircraft and Space Shuttle tests (Laminar Soot Processes, LSP, in still air) found them. SPICE asked how smoke points of non-buoyant laminar jet diffusion flames depend on the surrounding air flow (co-flow velocity) and burner diameter, which together control the residence time of soot in the flame. Specific aims: (1) measure non-buoyant smoke points of several gaseous fuels; (2) find the effects of co-flow velocity and burner diameter on smoke points and luminous flame lengths; (3) rank the sooting propensity of the fuels; (4) test flame-shape and residence-time models against the data. The stated hypothesis (30-day report) was that smoke points would be observed in co-flowing flames and would depend on nozzle diameter and co-flow velocity.

## Summary

SPICE measured laminar smoke points, the largest flame that releases no soot, of round gas-jet diffusion flames burning in co-flowing air inside the Microgravity Science Glovebox on the ISS between February and June 2009. The crew set the air speed with a fan, ignited the flame on a 0.41, 0.76 or 1.6 mm burner and raised the fuel flow until soot escaped the tip; luminous lengths were measured from the downlinked video. About 526 flame conditions were logged and 52-55 smoke points found for ethylene, propane, propylene and 75%/50% propylene in nitrogen, at co-flow speeds of 5.4-65 cm/s. Methane flames reached the end of the duct without smoking. Smoke-point length grew with co-flow speed and with smaller burners, scaling as d^-0.91 u^0.41, and was roughly proportional to fuel mass flow over stoichiometric mixture fraction; a simple residence-time model did not collapse the data. Propane was unusually sooty in microgravity. For spacecraft fire safety the results show that ventilation speed and fuel-jet size, not only fuel type, decide whether a small non-buoyant flame emits smoke.

## Physics

A gas-jet diffusion flame burns where fuel from the nozzle meets air diffusing in. Soot forms on the fuel-rich side and is normally burnt out as it crosses the flame sheet near the tip. As the fuel flow (and flame length) is raised, the tip cools, largely by soot radiation, until soot oxidation stops and soot escapes: that luminous length is the laminar smoke point. Shorter smoke points mean sootier fuels. In 1 g, buoyancy accelerates the hot gas, so residence time grows only weakly with flow, and soot forms near the flame sheet and moves inward. Without buoyancy, the flow decelerates, residence times are long, and soot forms near the cool core and is carried straight toward the flame sheet. Radiative losses then dominate and the tip can extinguish, giving an 'open-tipped' flame that sheds soot in an annular shell. An imposed co-flow restores some control over residence time: faster air shortens the time soot spends in the formation region and may speed oxygen transport for soot burnout. A smaller nozzle raises the jet exit velocity at the same mass flow. Both are expected to push the smoke point to longer flames. Flame length itself depends mainly on fuel mass flow divided by the stoichiometric mixture fraction, not on nozzle size. Criteria proposed for the smoke point include a tip (soot) temperature of about 1300 K in 1 g and about 1000 K in microgravity, a radiative loss fraction of 0.2-0.4 (1 g) or 0.4-0.6 (0 g), or a luminous length about twice the stoichiometric length.

$$
\frac{L_f - L_o}{d} = \frac{C_f\,Re\,Sc}{16\,Z_{st}}
$$

Luminous length of a non-buoyant round laminar jet flame in co-flow (Spalding / Mahalingam et al. analysis as applied by Faeth and co-workers). L_f luminous flame length (mm), L_o virtual-origin correction (mm), d burner inner diameter (mm), C_f empirical coefficient (-), Re = \rho u d/\mu jet Reynolds number, Sc Schmidt number (evaluated for air at the mean of adiabatic and ambient temperature), Z_st stoichiometric mixture fraction. For still air the factor 1/16 becomes 3/32. Laminar, momentum-dominated jets; neglects radial velocity.

`PSI-107_Reports_SPICE_30-DayPostFlightReport.pdf` (p4): *( L f – Lo ) / d = Cf Re Sc / 16 Zst , (1) and ( L f – Lo ) / d = 3 Cf Re Sc / 32 Zst , (2) for coflowing and non-coflowing cases, respectively*

$$
L_f = C\,\frac{\dot m_f}{Z_{st}}
$$

With the virtual origin neglected and Sc and viscosity treated as constant, the expression above reduces to luminous length proportional to fuel mass flow rate \dot m_f (mg/s) over Z_st; C is a constant (mm s/mg). SPICE used this as the abscissa for correlating smoke-point lengths L_SP of all fuels with a through-origin linear fit; flames with low air-to-fuel velocity ratio (u_a/u_f < 0.08) lie above the line.

`PSI-107_Reports_SPICE_30-DayPostFlightReport.pdf` (p5): *Lf = C m˙ f / Zst , (3) where C is a constant and m˙ f is the fuel mass flow rate.*
`PSI-107_Reports_SPICE_FinalReport.pdf` (p22): *This choice of axes yields a reasonably good single correlation of the luminous lengths of all fuels.*

$$
Re = \frac{4\,\dot m}{\pi\,d\,\mu}
$$

Jet Reynolds number used in the SPICE tables: \dot m burner-gas mass flow rate (kg/s), d burner inner diameter (m), \mu burner-gas dynamic viscosity at 298 K and 101 kPa (Pa s). SPICE smoke-point flames had Re = 36-788, i.e. laminar jets.

`PSI-107_Reports_SPICE_FinalReport.pdf` (p6): *Re = jet Reynolds number, 4 m˙ / (π d µ)*
`PSI-107_Presentations_Laminar Smoke Points in Coflow Measured Aboard ISS.pdf` (p14): *Red < 788 → laminar jets*

$$
L_{SP} \propto d^{-0.91}\,u_a^{0.41}
$$

Empirical scaling of the microgravity smoke-point luminous length L_SP (mm) with burner diameter d (mm, 0.41-1.6) and co-flow air velocity u_a (cm/s, 5.4-65) reported in the SPICE final report. Fitted to the ISS data for ethylene, propane, propylene and propylene/N2; the AIAA presentation instead plots L_SP against TSI^{-1} d^{-0.8} u_a^{0.5} (y = 5.99x, R^2 = 0.93). Valid only within the tested range; it extrapolates to a weak diameter dependence at u_a = 0.

`PSI-107_Reports_SPICE_FinalReport.pdf` (p2): *The measured smoke point lengths were found to correlate with burner diameter to the –0.91 power times coflow velocity to the 0.41 power.*
`PSI-107_Presentations_Laminar Smoke Points in Coflow Measured Aboard ISS.pdf` (p22): *y = 5.99x R² = 0.93*

$$
Q_f = K\,Q_{N_2},\qquad K_{mix} = \Big(\sum_i x_i/K_i\Big)^{-1}
$$

Fuel-flow conversion. The mass flow controller reads in N2-equivalent sccm Q_{N2}; the actual fuel volume flow Q_f uses the gas factor K (N2 1.00, CH4 0.72, C2H4 0.60, 50% C3H6 0.582, 75% C3H6 0.481, C3H6 0.41, C3H8 0.36); x_i is the mole fraction of component i in a mixture. The 'Fuel Rate (sccm)' column of the PSI table equals the overlay fuel display times K.

`PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p37): *Converting to the actual flow of fuel requires correcting the measured flow by a factor of gas-specific constant K*
`PSI-107_Raw Data_Spice Flight Test Data II modified.xls`, sheet Reference, row Reference sheet rows 12-14: *K factor for a mixture is computed from Prof. Peter Sunderland's equation Kmixture = 1/sum(xi/Ki)*

$$
u_a = 0.9402\,A - 5.918
$$

Calibration used in the SPICE master spreadsheet to convert the AIR number on the video overlay (A, from the onboard hot-wire anemometer) to co-flow velocity u_a (cm/s) representative of the flow 13 mm downstream of the burner tip. Valid for A of roughly 10-77 (5-66 cm/s). A blank or zero A returns the intercept, -5.92 cm/s, which explains that value in the PSI table.

`PSI-107_Raw Data_Spice Flight Test Data II modified.xls`, sheet Reference, row Reference sheet rows 10-11: *Air to actual flow correlation ... slope 0.9402153845089276, intercept -5.918369593325366*
`PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p36): *Shown in Figure 3.4 is the correlation between this anemometer reading and another, measuring the air velocity at 13 mm above the tip of the burner tube and aligned with the centerlin*

## Method

### Apparatus

The SPICE module was the reworked Enclosed Laminar Flames (ELF) apparatus flown in the Shuttle middeck glovebox on STS-87 (1997). It was launched to ISS on ULF-2 in 2008 and run in the MSG at ISS cabin pressure (the MSG runs about 1.3 mbar below cabin). A DC fan drew glovebox air through a ceramic honeycomb and screen into a duct described as about 76 x 76 mm with rounded corners and about 170 mm long. The final report instead gives interior dimensions of 172 x 43 x 43 mm. Air and products left through a perforated copper plate and screen (soot trap) 120 mm downstream of the burner exit. For safety the fan always ran at a minimum of 5.5 V (overlay FAN number 55-139). An onboard TSI 8475 hot-wire anemometer (rated 5-254 cm/s, +/-3% of reading +/-1% of range) near the inlet gave the AIR overlay reading, calibrated on the ground against a probe 13 mm above the burner tip. Three burner tubes (0.41, 0.76 and 1.6 mm ID) were swapped by the crew. Fuel came from 150 ml bottles through a regulator and a 0-500 sccm (N2-equivalent) mass flow controller set by a potentiometer on the crew control box. A hot-wire (Kanthal) igniter and a retractable 105 mm ruler for length calibration could be swung to the nozzle. An Oriel thermopile radiometer (90 deg view) gave a qualitative radiation signal; it failed its accuracy verification because of EMI susceptibility. Imaging was a Nikon D100 12-bit still camera (3008 x 2000 pixels, 60 mm lens) through the top window and a Panasonic colour video camera viewing the front window via a 45 deg mirror. A titler stamped fuel flow, fan setting, air reading and radiometer gain on the video, logged at 4 Hz.

### Fuels and samples

- ethylene (C2H4), bottle fill 210 psia (gas, round laminar fuel jet from 0.41, 0.76 or 1.6 mm ID burner tube in co-flowing air)
- propane (C3H8), 110 psia (gas, round laminar fuel jet in co-flow)
- propylene (C3H6), 135 psia (gas, round laminar fuel jet in co-flow)
- 75% propylene / 25% nitrogen (mole basis), 180 psia (gas, round laminar fuel jet in co-flow)
- 50% propylene / 50% nitrogen (mole basis), 180 psia (gas, round laminar fuel jet in co-flow)
- methane (CH4), 210 psia (no smoke point reached) (gas, round laminar fuel jet in co-flow)

### Procedure

The safety package planned, per fuel, nine test points (two co-flow levels, 50% and 100% of maximum, times three burners, at 100% and 50% of the smoke-point fuel flow) plus about five repeats: 54 planned flames plus about 30 repeats. In practice the crew set the fan, ignited the flame with the hot wire, then adjusted fuel flow (and in later sessions swept the air speed) to bracket the smoke point. The crew used a cue card: look for the change from a distinct flame tip to dull red/orange breaking through it. Ground staff at the GRC TeleScience Center watched the real-time downlink at the same time. Flames were steady within about 5 s of any change. Typical burns lasted about 60 s, and after every two burns the MSG was flushed with cabin air for 3 minutes. For each condition the crew took a bracketed trio of Nikon stills, and a ruler reference image was taken for scale. Post-flight, smoke-point conditions were picked from the video. L_SP was measured on axis from the burner tip to the point of steepest grayscale change between yellow and black, which spans 2-5 mm. Flow rates were read from the overlay, and pixel-to-mm calibrations were made per day and per video source. Twelve sessions ran from 14 February (GMT 045) to 23 June 2009 (GMT 174). On 15 June (GMT 166) the crew vacuumed soot from the clogged outlet screen. A normal-gravity campaign with the prototype SPICE module and a 13.7 mm unconfined co-flow burner was run at the University of Maryland (Dotson thesis).

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel | ethylene, propane, propylene, 75% and 50% propylene in N2, methane |  |
| burner (nozzle) inner diameter | 0.4064, 0.762, 1.6002 (nominal 0.41, 0.76, 1.6) | mm |
| co-flow air velocity | 5.4-65 at smoke points; 0.66-85.3 in the run log (fan minimum gives about 0-10 depending on outlet-screen clogging) | cm/s |
| fuel flow rate | 0-4.40 mg/s hydrocarbon (0-231 sccm actual fuel); smoke points at 0.39-3.89 mg/s | mg/s |
| fuel jet exit velocity at smoke point | 11.2-763 | cm/s |

Held constant:

- ambient pressure: ISS cabin pressure, about 101 kPa (1 atm); MSG about 1.3 mbar (0.13 kPa) below cabin. Not logged per run in PSI.
- oxidizer: ISS cabin air in the MSG, O2 19-24% (assumed 21 +/- 1% in data reduction); refreshed every two burns
- gravity: ISS microgravity (MSG)
- flame regime: laminar, attached jet flames (all smoke-point flames attached, not lifted)

Number of tests: 526 logged flame conditions in the master sheet (the approach and final report call these '526 flames'); 469 rows in the PSI experimental table (the master minus the 57-row GMT 062 methane session); 108 + 155 = 263 'test points' per the 30-day report; '200 data points' per the 2011 crew training; 52 smoke points in the final-report table (55 in its closing remarks and 55 in the smoke-point review sheet).

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| smoke-point luminous flame length L_SP (burner tip to steepest yellow-to-black grayscale change on axis) | downlinked colour video frame grabs (DVD/DVCAM/PNG), pixel-to-mm calibration against in-duct ruler | derived |
| luminous flame length and width at non-smoke-point conditions | video and Nikon D100 stills (bracketed exposures) | derived |
| co-flow air velocity | onboard TSI 8475 hot-wire anemometer (overlay AIR reading), converted with a ground calibration | derived |
| fuel flow rate | MKS mass flow controller (N2-equivalent sccm, +/-1% FS), converted with gas K factors to sccm and mg/s | derived |
| flame radiation (qualitative) | Oriel 71768 thermopile radiometer with gain switch | direct |
| smoke onset (visual) | crew and ground observers on live video; tip dimming/reddening/rounding or sudden open tip | direct |
| duct velocity profiles without flame (pre-flight) | TSI 1261A boundary-layer hot-wire probe at 18 positions (13 and 56 mm stations) and 6 fan settings | direct |

## Findings

1. Laminar smoke points exist for non-buoyant co-flowing jet flames, contrary to Glassman's 1988 prediction. On the ISS, 52 smoke points (final-report table: 6 ethylene, 6 propane, 20 propylene, 13 for 75% and 7 for 50% propylene; the same report's closing remarks say 55) were found at 0.41-1.6 mm burners and 5.4-65 cm/s co-flow. All smoke-point flames were attached, with Re 36-788. The archival paper (Dotson et al. 2011) reports 55: 6 ethylene, 6 propane, 22 propylene, 14 for 75% and 7 for 50% propylene. *(result, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p2): *Fifty)two smoke points were found for ethylene, propane, propylene, and propylene/nitrogen mixtures.*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p20): *# smoke points 6 6 20 13 7*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p20): *All smoke point flames were attached to the burner, i.e., not lifted.*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p24): *Smoke points of 55 microgravity gas-jet diffusion flames in coflowing air were measured in earth orbit.*
   - `PSI-107_Reports_SPICE_30-DayPostFlightReport.pdf` (p3): *Glassman predicted that smoke points would not occur in nonbuoyant gas- jet flames.*
   - <https://terpconnect.umd.edu/~pbs/2011%20Dotson%20et%20al.%20FSJ.pdf>: *A total of 55 smoke points were found for ethylene, propane, propylene, and propylene/nitrogen mixtures.*
2. For a given fuel and burner, raising the co-flow velocity lengthens the smoke point, even though at fixed fuel flow it shortens the luminous flame. Example (pure propylene, 1.6 mm burner, smoke-point review sheet): L_SP rose from about 14.0 mm at u_a = 9.1 cm/s to 25.7 mm at 51.4 cm/s. The investigators attribute this to decreased residence times and radiative losses as co-flow velocity increases. *(trend, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p21): *For a given choice of fuel and burner diameter, an increase in coflow velocity generally increases the smoke point length. This behavior is attributed to decreased residence times and radiative losses as coflow velocity increases*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p2): *Increasing co)flow velocity decreases luminous flame lengths, but moves smoke points to higher fuel flow rates and longer luminous flame lengths.*
   - `PSI-107_Raw Data_SmokePointReview-0g-3.xlsx`, sheet Smoke Point Datasheet, row rows 38 and 41 (P16-1, P16-4): *Propylene 1.6002 mm: uair 51.43 cm/s, smk pt 25.73 mm; uair 9.13 cm/s, smk pt 13.99 mm*
3. Smaller burners give longer smoke points in co-flow. Propylene smoke points at about 25-27 cm/s co-flow were about 16-18 mm (1.6 mm burner, 22-30 cm/s), 22-23 mm (0.76 mm) and 53 mm (0.41 mm). The step from 0.76 to 0.41 mm is much larger than from 1.6 to 0.76 mm. Extrapolated to zero co-flow the diameter dependence diminishes. The extrapolation matches the earlier still-air shuttle (LSP) smoke points for ethylene; for propane on the 0.76 mm burner it falls at the lower end of the LSP range. *(trend, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p21): *Figure 18 reveals that smoke points of nonbuoyant coflowing flames decrease with increasing burner diameter.*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p22): *When the present measurements are extrapolated to zero coflow velocity, the dependence on burner diameter diminishes.*
   - `PSI-107_Presentations_Laminar Smoke Points in Coflow Measured Aboard ISS.pdf` (p18): *Extrapolation to ua = 0 – Matches for C2H4. Matches for C2H4. – 0.76 mm C3H8 hits lower end of LSP range.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p54): *The difference in smoke point between 1.6 and 0.76 mm burners is not as strong as the difference between 0.76 and 0.41 mm.*
   - `PSI-107_Raw Data_SmokePointReview-0g-3.xlsx`, sheet Smoke Point Datasheet, row rows 40, 50, 56: *Propylene: 1.6002 mm, 22.29 cm/s, 15.79 mm; 0.762 mm, 26.99 cm/s, 21.67 mm; 0.4064 mm, 26.99 cm/s, 53.28 mm*
4. Across all fuels the smoke-point lengths fit L_SP proportional to d^-0.91 u_a^0.41 (d burner diameter, u_a co-flow velocity). *(result, medium)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p2): *The measured smoke point lengths were found to correlate with burner diameter to the –0.91 power times coflow velocity to the 0.41 power.*
5. Sooting-propensity ranking at fixed burner and co-flow (1.6 mm burner): propane < ethylene < 50% propylene < 75% propylene < propylene, the same order as in 1 g. With the 0.76 mm burner ethylene had the longer smoke point than propane. Example: ethylene reached L_SP of about 105 mm at 17.6 cm/s, a length propane reached only at 33.6 cm/s. The final report's closing remarks print the order with ethylene and propane swapped (see limitations). Across all three burners, the archival paper's fuel constants A_f of the d^-0.91 u^0.41 correlation (21.2 mm ethylene, 18.5 propane, 13.9 for 50% propylene, 7.65 for 75%, 6.05 propylene) rank ethylene < propane < 50% < 75% propylene < propylene: overall, propane soots more than ethylene in microgravity, the reverse of 1 g, which the authors attribute to propane's lower jet velocity (longer residence time) at equal flame length. The 1-g order holds only at the 1.6 mm burner. *(result, medium)*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p56): *The sooting propensity of the present fuels, identified from in the smoke point length for the 1.6 mm burner diameter and fixed coflow velocity, is generally propane < ethylene < 50% propylene < 75% propylene < propylene.*
   - `PSI-107_Presentations_Laminar Smoke Points in Coflow Measured Aboard ISS.pdf` (p23): *Propane < Ethylene < 50% Propylene < 75% Propylene < Propylene*
   - `PSI-107_Raw Data_SmokePointReview-0g-3.xlsx`, sheet Smoke Point Datasheet, row rows 10 and 14 (E7-1, P7-1): *Ethylene 0.762 mm: uair 17.59, smk pt 105.22 mm; Propane 0.762 mm: uair 33.57, smk pt 105.45 mm*
   - <https://terpconnect.umd.edu/~pbs/2011%20Dotson%20et%20al.%20FSJ.pdf>: *The only surprise of this ranking is that propane soots more than ethylene, which has not been observed in previous normal-gravity [7,30] or microgravity tests [21,24].*
   - <https://terpconnect.umd.edu/~pbs/2011%20Dotson%20et%20al.%20FSJ.pdf>: *The microgravity smoke points for propane are shorter than for ethylene for the 0.76 mm burner, leading to propane's lower value of Af. Note that this is not the case for the 1.6 mm burner.*
   - <https://terpconnect.umd.edu/~pbs/2011%20Dotson%20et%20al.%20FSJ.pdf>: *0.0637 2367 69.6–735 1.63–3.89 127–636 6 21.2 106 0.0603 2264 48.9–460 1.80–3.84 176–788 6 18.5 162*
6. Pseudo threshold soot indices (TSI) from the microgravity data match 1 g values for ethylene (1.3 vs 1.3), propylene (4.51 vs 4.8) and the mixtures, but propane's 0 g TSI (1.39) is more than twice its 1 g value (0.6). The final report calls this an unusually high sooting propensity for propane in microgravity. *(result, medium)*
   - `PSI-107_Presentations_Laminar Smoke Points in Coflow Measured Aboard ISS.pdf` (p22): *C2H4 1.3 1.3 C3H8 1.39 0.6*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p2): *indicating an unusually high sooting propensity for propane in microgravity*
7. Smoke-point luminous lengths of all fuels collapse reasonably onto one through-origin line against fuel mass flow over stoichiometric mixture fraction (\dot m_f/Z_st). Flames with u_a/u_f < 0.08, the smallest-burner propylene, propane and ethylene cases, lie above it. The normal-gravity SPICE-module data fit Y = 1.7299x (R^2 = 0.9463). *(result, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p22): *This choice of axes yields a reasonably good single correlation of the luminous lengths of all fuels.*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p22): *This occurs in Fig. 19 for propylene, propane, and ethylene flames with the smallest burner, for which ua / u f < 0.08.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p61): *Y = 1.7299x R2 = 0.9463*
8. Residence time explains the trends qualitatively but does not correlate the smoke points. A simplified Schlichting-type centerline-velocity model gave no critical residence time or formation/oxidation time ratio; many points grouped near a ratio of 0.65 with wide scatter. COMSOL simulations showed the model fails for initial air-to-fuel velocity ratios above about 0.2-0.5. *(null_result, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p24): *6. Although residence time is helpful in understanding the present smoke points, it does not yield quantitative correlations of smoke points.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p1): *A simplified prediction of centerline jet velocity did not yield residence-time-based criticalities or data collapse.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p75): *COMSOL® simulations have shown that the simplified Schlichting-based analysis does not adequately predict the centerline velocity decay of air jets with initial air to fuel velocity ratios larger than around 0.2 – 0.5.*
9. Methane flames reached the copper exhaust plate (about 120 mm downstream) before any smoke point, at up to about 360 sccm on the 1.6 mm burner (GMT 062). Methane at 0.41-0.76 mm with higher co-flow blew off (GMT 168). *(limit, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p20): *Smoke points were attempted with methane, but could not be obtained before the flames impinged on the copper plate at the end of the duct.*
   - `PSI-107_Raw Data_Spice Flight Test Data II modified.xls`, sheet Data record of Video and Stills, row rows 281 and 409-411: *Methane 1.6002 mm, 357.12 sccm, flame length 104.5 mm (GMT 062); 'Blew Off' comments for methane 0.4064 and 0.762 mm (GMT 168)*
10. The two ways a flame can pass its smoke point were both seen. Propane and ethylene showed gradual tip dimming, reddening and rounding. The brighter propylene-based flames switched abruptly to an open tip, with soot leaving in an annular shell. Well past the smoke point, quenched soot was visible leaving the flame. *(result, high)*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p20): *Some smoke points (particularly for propane and ethylene) were identified by the onset of gradual dimming, reddening, and rounding of the luminous flame tip.*
   - `PSI-107_Reports_SPICE_FinalReport.pdf` (p20): *For these flames, smoke points were identified by the rapid transition to open-tipped flames.*
11. Soot from the flames progressively clogged the duct outlet screen. This changed the co-flow for a given anemometer reading, and the 0.41 mm propylene smoke points differed between days. Before the 15 June cleaning (GMT 058) they were 37.7-53.3 mm at 5.4-27 cm/s. After it (GMT 174) a smoke point of 59.2 mm was found at only 10.1 cm/s. In the run log the same minimum fan setting (FAN 55-56) read about 0 cm/s on GMT 136 but 11.9-16.6 cm/s on GMT 167. *(method, medium)*
   - `PSI-107_Reports_SPICE_30-DayPostFlightReport.pdf` (p2): *SPICE operated very successfully with the only significant anomaly being the accumulation of soot in the outlet screen which changed the flow behavior in the duct.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p51): *The lower smoke points were obtained with a relatively clogged exit, and the highest smoke point was found after the exit was vacuumed clean.*
   - `PSI-107_Raw Data_SmokePointReview-0g-3.xlsx`, sheet Smoke Point Datasheet, row rows 56-59 (P4-1..P4-4): *Propylene 0.4064 mm: GMT 058 26.99/14.77/5.36 cm/s -> 53.28/46.96/37.70 mm; GMT 174 10.07 cm/s -> 59.19 mm*
   - `PSI-107_Raw Data_Spice Flight Test Data II modified.xls`, sheet Data record of Video and Stills, row rows 356-361 and 389-396: *GMT 136, FAN 55-56, AIR 6-7 -> -0.28/0.66 cm/s; GMT 167, FAN 55-56, AIR 19-24 -> 11.9-16.6 cm/s*
12. In 1 g, the prototype SPICE module (0.41-1.6 mm burners, confined co-flow) showed the same trends: longer smoke points with more co-flow and smaller burners. But flames lifted more easily and smoked at longer lengths. A 13.7 mm unconfined co-flow burner gave the opposite trend for ethylene and propylene (shorter smoke points with more co-flow) while propane still lengthened. The co-flow effect is therefore configuration-dependent. *(result, high)*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p1): *For burner diameters of 0.41, 0.76, and 1.6 mm, smoke points increased with increases of coflow velocity. For an unconfined coflow burner with a burner diameter of 13.7 mm smoke point length decreased with increasing coflow velocity for ethylene and propylene, while increasing for propane flames.*
   - `PSI-107_Reports_SMOKE POINTS OF MICROGRAVITY AND  NORMAL GRAVITY COFLOW DIFFUSION  FLAMES_DotsonThesis.pdf` (p59): *An additional difficulty encountered while searching for smoke points was that the flames tended to lift at lower fuel and/or coflow velocities*

## Fire-safety relevance

SPICE is fundamental soot science, not a material flammability test. Its main fire-safety value: in microgravity, whether a small flame releases smoke depends strongly on the local ventilation speed and on the size of the fuel source, not just on the fuel. Faster co-flow (5-65 cm/s, spanning typical cabin ventilation) and smaller fuel jets let flames grow longer before smoking. Non-buoyant flames well past their smoke point open at the tip and shed quenched soot, which is also the main carrier of CO and the signal smoke detectors respond to. Propane was relatively sootier in microgravity than its 1 g ranking suggests, so 1 g sooting indices may not transfer directly. The data and correlations (L_SP vs \dot m_f/Z_st, d^-0.91 u^0.41) are benchmarks for soot models used to predict radiation and smoke yield of spacecraft fires. The SPICE duct itself became the platform for BASS solid-fuel flammability and suppression tests and SLICE lifted-flame tests. These are gas-jet results at about 1 atm and 21% O2; they do not give material ignition or spread limits.

### Habitat conditions

All SPICE flames burned in ISS cabin air: O2 19-24% (assumed 21 +/- 1%), about 101 kPa, which is close to the Earth sea-level reference (20.9% O2, 101.3 kPa). Neither O2 nor pressure was varied. The proposed lunar habitat atmosphere (30% O2 or more at 70.3 kPa or less) and suits (100% O2 at 29.6 kPa) are outside the tested range. Higher O2 raises flame temperature and soot formation and lower pressure reduces soot, so SPICE smoke points cannot be applied to those atmospheres without new tests. The co-flow range (5-65 cm/s) does cover realistic ventilation speeds. There is no partial-gravity SPICE data.

### Earth benefits

Smoke points are a classical metric for fuel sooting propensity used in fire modelling and in correlating soot and radiation of turbulent flames (e.g. gas-turbine soot emissions correlate with TSI). Many practical flames are effectively non-buoyant, so SPICE's co-flow data help predict heat release and soot emission in combustors such as jet engines and furnaces. Soot is also a pollutant linked to premature deaths and climate warming.

## Limitations

- No velocity measurement with a flame present. Co-flow is a far-field value from an anemometer upstream of the nozzle, calibrated on the ground. The duct profile is non-uniform: there is a centerline velocity deficit from the nozzle boundary layer at 13 mm downstream, and periodic flame motion attributed to non-uniform co-flow was seen in long, high-co-flow flames.
- Co-flow at the fan minimum is poorly defined. The fan never stops (minimum 5.5 V), the anemometer is rated only from 5 cm/s, and soot clogging of the outlet screen changed the flow for a given reading until the screen was vacuumed on 15 June 2009. Air-rate values below about 5 cm/s, including the -0.28 and 0.66 cm/s entries, are not reliable velocities.
- Smoke points were judged visually from analog video and were not always clearly exceeded. For ethylene and the 1.6 mm propane flames the true smoke point might be slightly higher. Flame tips span 2-5 mm from yellow to black. Fuel ran out before some planned conditions, notably for ethylene.
- Only one O2 level (cabin air, not logged per run) and one pressure were tested. Smoke points depend on both, so the results do not cover enriched or reduced-pressure exploration atmospheres.
- The documents disagree on several basics. Duct size: 76 x 76 x 170 mm vs 172 x 43 x 43 mm. Fuel bottles: 150 cc vs 75 cc. Mass flow controller: MKS vs Sierra. Number of smoke points: 52 vs 55, with 20 vs 23 for propylene. Number of tests: 526 / 263 / 200. The fuel ranking in the final report's conclusion 4 (ethylene < propane) contradicts its own discussion and the other papers (propane < ethylene). The final report is an unpolished draft whose appendices B-F are empty. [Correction, Publications pass 2026-11-15: the ranking ethylene < propane is not an error. It is the conclusion of the peer-reviewed paper (Dotson et al., Fire Saf. J. 46 (2011) 550-555), derived from the fuel constants fitted over all burners; propane < ethylene holds only at the 1.6 mm burner and is the 1-g order (see findings[4]). The paper also gives a third smoke-point split: 55 in all, 22 propylene and 14 for 75% propylene.]
- The radiometer gives only a qualitative signal and failed its accuracy verification (EMI). No quantitative radiative-loss fractions, soot volume fractions or temperatures were measured in flight. Those would need the raw NEF images (as attempted in the PSI-60 re-analysis).

## Data in PSI

PSI-107 holds 188 files (6.95 GB); 59 are downloaded locally. Text-bearing documents are readable: the 2011 final report (a draft with editing notes, appendices B-F empty), the 30-day post-flight report with the 2009 Eastern States paper, the 2009 Dotson M.S. thesis, the 2010 AIAA presentation, two crew-training decks, the safety data package, the science verification report, a duct-velocity memo and an image organization guide. The SRD (.doc) and two .ppt decks could not be extracted. The most valuable structured file is 'Spice Flight Test Data II modified.xls' (526 rows, 43 columns). For every logged condition it gives GMT times, test number, fuel, nozzle, overlay fuel/air/fan/radiometer readings, converted fuel and air rates, video and Nikon flame lengths and widths, a smoke Y/N flag, and Nikon file IDs. 'SmokePointReview-0g-3.xlsx' lists the 55 microgravity smoke points with derived u_a, u_f, Re, \dot m_f/Z_st and residence-time estimates, plus normal-gravity and shuttle comparison points. The PSI experimental table is a 9-column extract of the master sheet. It drops the measurement columns (flame length, Nikon dimensions, smoke flag, data timestamp) and the GMT 062 methane session, so it holds flow settings only. Raw imagery (NEF zips, jpeg/contact-sheet zips, 83 downlink frame-grab zips, picture-book .ppt, 20 videos; about 6.9 GB) is not downloaded. 22 duct-calibration and 8 fuel-flow-calibration files are present (one of each not downloaded).

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | Master run log 'Spice Flight Test Data II modified.xls' (526 condition rows plus reference/calibration sheet) and SmokePointReview-0g-3.xlsx (55 microgravity smoke points with derived quantities) | .xls .xlsx | 2 | 1 MB | yes |
| Raw Data | Other analysis spreadsheets and notes: flame-length calibration, Nikon colour-saturation sheets for GMT 052/055/058, DSC-to-ISS image number lists, image organization guide | .xls .txt .docx .pptx | 8 | 23 MB | yes |
| Raw Data | Pre-flight duct velocity calibration (18 probe positions x 6 fan settings) and airflow comparison sheets | .xls .xlsx .ppt | 22 | 3 MB | yes |
| Raw Data | Fuel mass-flow controller calibration and settings | .xls .xlsx .pdf .pptx | 8 | 3 MB | yes |
| Raw Data | Downlink video frame grabs per test point (TP 13-104) | .zip | 83 | 573 MB | no |
| Raw Data | Nikon D100 raw images (NEF) for GMT 045/048/052/055/062 plus a focus-check frame | .zip .nef | 6 | 2.06 GB | no |
| Raw Data | Nikon jpeg and contact-sheet zips; contact-sheet PDFs for GMT 119/136/166/167/173/174 (text only: file IDs, exposure, time) | .zip .pdf | 17 | 861 MB | no |
| Raw Data | Nikon picture books per session | .ppt | 6 | 913 MB | no |
| Raw Data | Downlink and crew video (GMT 062, 119, 136 ignitions) | .mp4 .avi .zip | 20 | 2.47 GB | no |
| Reports | Final report (2011 draft), 30-day post-flight report with 2009 ESSCI paper, Dotson M.S. thesis (2009) | .pdf | 3 | 3 MB | yes |
| Presentations | AIAA 2010 talk, 2010/2011 crew training (SPICE/SLICE/BASS); SPICE Overview and Ops/cue-card .ppt (not extractable) | .pdf .ppt | 5 | 37 MB | yes |
| Engineering Documents | Phase III flight safety data package, science verification report, duct velocity memo (SPICE-MEM-010), assembly drawing (no text) | .pdf | 4 | 5 MB | yes |
| Science Documents | SPICE Science Requirements Document 2007 (legacy .doc, not extracted) | .doc | 1 | 1 MB | no |
| Experimental table | PSI experimental table: 469 rows x 9 columns (GMT date, ignition/flame-off times, fuel, nozzle, fuel rate sccm and mg/s, HC fuel rate, air rate) | .csv | 1 | 0 B | yes |

Rows in the unified `tests` table: 469

## Related investigations

- [PSI-26](PSI-26-bass.md): shared hardware
- [PSI-25](PSI-25-bass-ii.md): shared hardware
- [PSI-106](PSI-106-slice.md): shared hardware
- [PSI-60](PSI-60.md): ground re-analysis

## Open questions

- Rebuild a clean smoke-point and flame-length table from the master sheet: restore the measurement columns the PSI CSV drops (video and Nikon flame length, width, smoke Y/N, data timestamp) and the GMT 062 methane session. Then fit L_f vs \dot m_f/Z_st for all 526 conditions, not only smoke points.
- Use the Nikon NEF stills (bracketed exposures, about 2 GB) for colour-ratio pyrometry of soot temperature at and beyond the smoke point. This would test the ~1000 K tip-temperature criterion for microgravity smoke points. PSI-60 attempted this; its results should be compared with SPICE.
- Quantify the effect of outlet-screen clogging: compare air readings vs fan setting before and after the GMT 166 cleaning to build a day-specific co-flow correction, and re-evaluate the 0.41 mm propylene smoke points.
- Combine SPICE smoke points with SLICE (PSI-106) lifted-flame data from the same duct to map the attached, smoking and lifted regimes in (u_a, u_f, d) space.
- Test a residence-time model that includes thermal expansion and the burner wake (the thesis notes its Schlichting model fails for u_a/u_f > 0.2-0.5) against the 55 smoke points.

## Dashboard ideas

- **smoke point length vs co-flow velocity** (`fuel`, `nozzle_mm`, `u_a_cm_s`, `L_sp_mm`): Reproduces the core SPICE plot: one line per fuel/burner pair, rising with co-flow, highest for the 0.41 mm burner.
- **flame length collapse** (`mdot_f_mg_s`, `Z_st`, `L_sp_mm`, `u_a_over_u_f`): Shows all fuels on one L_SP vs \dot m_f/Z_st line and flags the low u_a/u_f outliers.
- **run log timeline** (`gmt_date`, `gmt_ignition`, `fuel`, `nozzle_mm`, `fuel_rate_mg_s`, `air_rate_cm_s`, `row_kind (video/Nikon)`): Lets a user see the 11 sessions in the PSI table, which rows are video/still duplicates, and the LOS/negative air-rate rows.
- **fuel sooting ranking** (`fuel`, `TSI_0g`, `TSI_1g`): Compares microgravity and 1 g sooting indices; highlights propane's anomaly.

## Gaps and data-quality notes

- DATA ODDITY - 34 duplicate rows in the PSI experimental table: they are not repeated tests. The table is a 9-column extract of 'Spice Flight Test Data II modified.xls'. In that sheet each condition usually has a video-measurement row and a Nikon still-image row with identical flow settings, differing only in columns the CSV drops (GMT data timestamp, video vs Nikon flame length, smoke flag, ISS image IDs). Matching the CSV row-for-row to the master (minus GMT 062): the 34 extra rows fall in 31 identical-row groups. 27 groups have distinct data timestamps; the other 4 share a timestamp and pair a video length with a Nikon image record. Two are 'Ku LOS' rows with no data. De-duplicating the CSV would therefore delete real measurement records; they should be tagged video/still instead.
- DATA ODDITY - air rate -5.92 cm/s (3 rows, GMT 167, 50% propylene, 0.41 mm burner, ignition time 'LOS'): an artefact, not a reverse flow. The master sheet converts the overlay AIR reading with u_a = 0.9402*AIR - 5.918 (Reference sheet). For these three rows the AIR and FAN cells are blank because the downlink was lost (LOS), so the formula returned its intercept. Treat them as missing. Likewise -0.28 and 0.66 cm/s (6 rows, GMT 136) correspond to AIR readings of 6-7 at the minimum fan setting with a soot-clogged outlet screen, below the anemometer's 5 cm/s rated minimum. They mean 'near-zero, unreliable', not negative flow.
- DATA ODDITY - the PSI experimental table omits the whole GMT 062 session (3 March 2009; 57 methane rows in the master sheet: 0.41/0.76/1.6 mm, up to 357 sccm, flames to 110 mm). That is why it has 469 rows against the master's 526 ('526 flames' in the PSI approach is the master row count, not 526 separate ignitions). The table also lacks every measured quantity (flame length, smoke flag) and has no smoke-point column, so it cannot be used alone to reproduce SPICE results.
- Other table issues: 25 rows have blank air rate ('Ku LOS', 'no data', or Nikon rows where the formula was not filled); 10 rows have zero hydrocarbon fuel rate (LOS rows and a 'ran out of fuel' row); the 75% propylene label is spelled two ways ('75 % Propylene' 119 rows, '75% Propylene' 16); GMT ignition times use mixed formats (14:37:08, 14.43.58, 1744, 'no ku', 'Ku LOS'); in tests.csv the date column is empty because GMT day-of-year was not converted (all 2009); and fuel_fraction is null for pure fuels and methane.
- Max air rate in the table (85.28 cm/s, GMT 052) is above the 65 cm/s maximum at smoke points and the 5-50 cm/s design requirement; it is a single reading during a fan sweep and was not checked further.
- Not readable: SPICE SRD (.doc), 'SPICE Overview.ppt', 'SPICE-1 Ops Overview and Smoke Point Cue Card.ppt' (legacy formats, unsupported by the extractor); the assembly drawing PDF has no text layer. The 2011 crew training gives the cue-card text, so the ops procedure is covered. Imagery, picture books and videos (about 6.9 GB) were not downloaded.
- The final report's Appendices B-F (the 2009 ESSCI, 2010 AIAA, 33rd Symposium, Leeds and Fire Safety Journal papers) are empty placeholders in PSI. The Fire Safety Journal paper (doi 10.1016/j.firesaf.2011.08.002, listed in the metadata) was not fetched because sections 1-4 already covered the results. The figures (L_SP vs u_a, L_SP vs \dot m_f/Z_st, TSI plot) are images, so per-point values were taken from SmokePointReview-0g-3.xlsx and cited as psi_table. [Publications pass 2026-11-15: the paper was read from the author copy at terpconnect.umd.edu/~pbs; it changed findings[0], findings[4] and limitations[4].]
- Personal contact details (emails, phone numbers) appear in the PSI record contacts and the crew-training decks; they were not copied.
- Metadata oddities: the ISA metadata zip is named 'PSI-176_SPICE', and its study design descriptors include 'butane-lighter flame', which does not match SPICE. The PSI record has no start/end dates; dates here come from the final report (12 sessions, 14 Feb - 23 Jun 2009).
- Per-run O2, pressure and temperature were not logged in PSI for SPICE; only the 19-24% O2 cabin range is stated.
- Publications pass 2026-11-15: the archival paper (Dotson et al. 2011, sec. 3) gives cabin O2 as an estimated 20-23% (PSI final report: 19-24%) and says the glovebox was flushed with cabin air after each burn (PSI documents: after every two burns). Not reconciled.
- Publications pass 2026-11-15: a later UMD MS thesis (DeBold 2012, hdl.handle.net/1903/13569, not listed in the PSI record) reports a 2012 SPICE extension aboard the ISS with 57 more smoke points (methane, ethane, ethylene, propane; burners 0.76-3.2 mm; coflow 3.0-47 cm/s), including the first methane smoke point at atmospheric pressure. Those tests are not in the PSI tables; it was not used for findings.
