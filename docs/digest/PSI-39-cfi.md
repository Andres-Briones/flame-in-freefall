# PSI-39: CFI (Cool Flames Investigation)

Fuel droplets about 4 mm across were burned in a sealed chamber on the ISS to study 'cool flames': invisible, low-temperature flames (roughly 700-900 K) that keep a droplet burning after its normal hot flame has gone out.

Investigators: Forman A. Williams (PI; University of California, San Diego); Frederick L. Dryer (Co-I; Princeton University); Tanvir I. Farouk (Co-I; University of South Carolina); Vedha Nayagam (Co-I; Case Western Reserve University); Daniel L. Dietrich (Project Scientist; NASA Glenn Research Center)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS) |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 2017-03-09 to 2017-09-15 |
| Fuels and samples | n-dodecane; n-dodecane/iso-dodecane blends, 75/25 and 60/40 by mass; Farnesane |
| Varied | fuel: n-dodecane; 75/25 and 60/40 (mass) n-dodecane/iso-dodecane; farnesane<br>ambient pressure: 0.5-5 atm (50.7-506.6 kPa): 0.5, 0.75, 1, 1.25, 2, 3, 5 atm. The experimental table alone covers 0.5-5 atm for the blends but only 1-2 atm for pure n-dodecane atm<br>ambient oxygen: 0.17 or 0.21 mole fraction<br>helium dilution (replacing nitrogen at 0.21 O2): 0, 0.29, 0.59 mole fraction<br>droplet support: free-floated or tethered on a 40 um SiC fibre<br>initial droplet diameter: about 3.8-6.4 (target about 4) mm |
| Number of tests | 227 |
| Fire-safety pillars | fundamental, prevention, detection |

## Question

FLEX and FLEX-2 had found, by accident, that large n-alkane droplets keep burning quasi-steadily after their hot flame is extinguished by radiation, supported by low-temperature ('cool flame') chemistry in the negative-temperature-coefficient (NTC) range. CFI set out to study this regime systematically. It asked how fuel structure (n-dodecane, branched iso-dodecane in blends, and the renewable fuel farnesane), ambient pressure (0.5-5 atm) and helium dilution change the hot-flame and cool-flame burning rates, flame sizes, radiant output and, above all, the droplet diameter at cool-flame extinction. That diameter gives a measure of low-temperature chemical time scales that can be used to test and improve kinetic mechanisms. A secondary aim was to understand soot behaviour during cool-flame burning.

## Summary

CFI burned about 4 mm droplets of n-dodecane, n-dodecane/iso-dodecane blends (75/25 and 60/40 by mass) and farnesane in the Multi-User Droplet Combustion Apparatus on the ISS in 2017, at 0.5-5 atm (51-507 kPa), 17-21% O2 and 0-59% helium. More than two hundred tests were run. Large droplets first burned with a hot flame that went out by radiative heat loss after about 10-14 s in air. A cool flame then kept the droplet burning quasi-steadily, close to the droplet, until it too extinguished at a finite diameter and left a cloud of condensed, partly oxidised vapour. For n-dodecane in air the cool-flame extinction diameter fell from about 1.7-1.9 mm at 0.5 atm to below 0.4 mm at 1.25 atm. Helium dilution increased it, to 2.1-2.6 mm with 59% helium at 1 atm. Iso-dodecane suppressed cool flames. At 2 atm and above, cool flames repeatedly re-ignited hot flames. For spacecraft fire safety, this means a fuel can keep reacting, and producing flammable vapour, after the visible flame has gone out.

## Physics

Alkane oxidation follows different chemical routes at different temperatures. Below about 900 K, chain branching runs through peroxy radicals (RO2, QOOH, O2QOOH) and ketohydroperoxides. As temperature rises through the NTC region the overall rate falls, because these intermediates dissociate back, before high-temperature branching takes over above about 1100-1200 K. A spherically symmetric droplet diffusion flame normally burns in the high-temperature branch, and its flame radius is many droplet diameters. A large droplet in microgravity has a large flame whose radiative loss scales with flame volume, while heat release scales only with droplet diameter, so it can extinguish radiatively. In FLEX and CFI the gas left near the droplet after this extinction is hot enough for low-temperature chemistry to ignite a 'cool' diffusion flame at roughly 700-900 K. This flame sits close to the droplet (flame standoff ratio about 3) and releases roughly half the heat. It burns quasi-steadily, following a d-squared law, until the residence time in the reaction zone, which shrinks with droplet size, falls below the chemical time at the lower turning point of the NTC branch, and the flame goes out. Pressure shortens chemical times, so it lowers the extinction diameter. Helium raises thermal diffusivity and heat loss, so it raises the extinction diameter. Branched isomers form fewer of the five- and six-membered ring transition states needed for low-temperature branching, so they weaken cool flames. On Earth, buoyant convection on mm-size droplets is far faster than diffusion, so neither the spherical symmetry nor the long residence times these flames need can be achieved. Drop towers are also too short to reach radiative extinction.

$$
D^2(t) = D_0^2 - k\,t
$$

Quasi-steady d-squared law. D is droplet diameter (mm), D_0 the initial diameter (mm), t time since ignition (s), k the burning-rate constant (mm^2/s). CFI fits k separately for the hot-flame stage (k_hot) and the cool-flame stage (k_cool), over roughly 0.1-0.9 of each stage. Valid for spherically symmetric, quasi-steady burning; it fails during ignition transients, re-ignition and on a disturbed fibre.

Textbook background
`PSI-39_Science Documents_SRD_CFI.pdf` (p16): *The average burning rate constant (¯k) comes from a linear fit of the droplet-squared history between approximately t = 0.1τb and 0.9τb, where τb is the total burn time (igniter withdraw to extinction or burnout).*

$$
\tau_l = \frac{D_0^2}{k}
$$

Droplet lifetime (s) from the initial diameter D_0 (mm) and the average burning-rate constant k (mm^2/s). For D_0 = 3-6 mm and k = 0.5 mm^2/s this is 18-72 s, far longer than drop-tower times (up to about 5-10 s). That is why the ISS is needed.

`PSI-39_Science Documents_SRD_CFI.pdf` (p33): *Typically the droplet life-time (τl) can be estimated from the initial droplet size (D0) and the average burning rate constant (k) as τl = D2 0 k .*

$$
\frac{\tau_k}{\tau_b} = \frac{\sqrt{g D^3}}{\alpha_g}, \qquad \frac{\tau_m}{\tau_b} = \frac{\sqrt{g D^3}}{\mathcal{D}_g}
$$

Ratios of thermal (tau_k) and mass (tau_m) diffusion times to the buoyant residence time tau_b, for droplet diameter D (m), gravity g (m/s^2), gas thermal diffusivity alpha_g and mass diffusivity D_g (m^2/s). Both ratios must be much less than 1 for buoyancy to be negligible and the flame spherical. At 1 g and 1 atm this needs D much smaller than 1 mm, below cool-flame extinction diameters. Diffusivities scale as 1/p, so higher pressure makes buoyancy worse.

`PSI-39_Science Documents_SRD_CFI.pdf` (p33): *In order to justify neglecting buoyant effects the above ratios must be much lower than unity.*

$$
E_{t1} < E_b < E_{t2}
$$

Yang-Gray thermokinetic condition for an NTC region. In the scheme A -> X (initiation), X -> 2X (branching, activation energy E_b), X -> products (low-temperature termination E_t1, high-temperature termination E_t2), the overall rate falls with rising temperature over a range when this ordering holds. It is a conceptual model, not quantitative for real fuels.

`PSI-39_Science Documents_SRD_CFI.pdf` (p10): *They showed that for this scheme the NTC region is possible when the activation energies obey the following condition: Et1 <Eb <Et2.*

$$
\dot q_{rad} \propto r_f^3, \qquad \dot q_{chem} \propto D
$$

Scaling behind radiative extinction. Radiative loss from the flame grows with flame volume (r_f = flame radius), while heat release grows only linearly with droplet diameter D. Large droplets (and large flames in microgravity) therefore lose a growing fraction of their heat and extinguish radiatively. This sets up the cool-flame stage. Qualitative scaling for optically thin gas radiation.

Textbook background
`PSI-39_Science Documents_SRD_CFI.pdf` (p12): *the rate of radiant loss (proportional to the flame vol- ume) increases faster than the rate of heat release (proportional to the droplet diameter).*

## Method

### Apparatus

The CIR provides a 90 l combustion chamber (rated to about 9 atm; CFI went to 5 atm), gas mixing (FOMA), pressure and temperature sensors, and imaging. It is vibration-isolated by PaRIS (Passive Rack Isolation System), and g-levels were typically below 1e-5 g0. The MDCA deploys a droplet by dispensing fuel between two opposed 250 um outside-diameter needles, stretching it, then retracting the needles quickly. CFI used a thinner 40 um SiC tether fibre than FLEX's 80 um fibre, to keep droplets in view while disturbing them less near cool-flame extinction. Two hot-wire igniters (about 12-13 W, 1-11 s on-time) were positioned near the droplet and withdrawn once it ignited. Diagnostics: a backlit (red laser-diode) HiBMS camera at 30 frames/s for droplet diameter; an intensified camera with hot-flame and cool-flame modes for OH* and cool-flame imaging; a colour camera with live downlink; and a radiometer package with a wideband channel (0.6-10 um, mainly hot flame) and a narrowband channel (5.0-6.5 um water band, sensitive to the cool flame) sampled at 100 Hz. Chamber pressures and four temperatures were logged throughout. The CFI requirements asked for larger fields of view than FLEX (50 mm droplet view, 80 mm flame view) and auto-gain radiometers.

### Fuels and samples

- n-dodecane (C12H26), baseline fuel; derived cetane number 78 (liquid, free-floated or 40 um SiC fibre-supported droplet, initial diameter about 3.8-6.1 mm (mostly about 4-4.5 mm))
- n-dodecane/iso-dodecane blends, 75/25 and 60/40 by mass (liquid, free or fibre-supported droplet, D0 about 4.1-6.4 mm)
- Farnesane (2,6,10-trimethyldodecane), a renewable jet/diesel fuel component; derived cetane number 58 (liquid, droplet, about 4.6 mm (FLEX-1393))

### Procedure

The crew installed fuel syringes and gas bottles. Everything else was run from the Telescience Support Center at NASA GRC. For each test day the chamber was filled with the chosen O2/N2(/He) mixture and pressure and left about 2 minutes to settle. A set amount of fuel was then dispensed between the needles (or onto the fibre), stretched, and deployed. After a dwell of at least 10 s the igniters were powered for a preset time (1-5 s planned; later raised, e.g. to 8 s after a software change), then withdrawn. Cameras and radiometers recorded the hot-flame burn, its extinction, cool-flame burning, cool-flame extinction and vapour-cloud formation. A fan then mixed the chamber for about 15 s. Typically 5-10 droplets of different sizes were burned per atmosphere, about 8 per day, with later tests guided by earlier results. Data were downlinked and reduced to droplet diameter-squared histories (equivalent-area diameter of the backlit droplet), hot- and cool-flame diameters (FWHM and peak-to-peak of the cool-flame intensity profile), burning-rate constants from linear fits, extinction diameters and radiance traces.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel | n-dodecane; 75/25 and 60/40 (mass) n-dodecane/iso-dodecane; farnesane |  |
| ambient pressure | 0.5-5 atm (50.7-506.6 kPa): 0.5, 0.75, 1, 1.25, 2, 3, 5 atm. The experimental table alone covers 0.5-5 atm for the blends but only 1-2 atm for pure n-dodecane | atm |
| ambient oxygen | 0.17 or 0.21 | mole fraction |
| helium dilution (replacing nitrogen at 0.21 O2) | 0, 0.29, 0.59 | mole fraction |
| droplet support | free-floated or tethered on a 40 um SiC fibre |  |
| initial droplet diameter | about 3.8-6.4 (target about 4) | mm |

Held constant:

- ambient gas temperature: room temperature, about 299 K (FLEX-1206 test sheet: 299.19 K)
- gravity: ISS microgravity, typically below 1e-5 g0
- forced flow: none (quiescent chamber during the burn)

Number of tests: 227

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| droplet diameter vs time; initial diameter D0 | backlit HiBMS camera, 30 frames/s | direct |
| hot- and cool-flame burning-rate constants k_hot, k_cool (mm^2/s) | linear fits of droplet diameter-squared history | derived |
| droplet diameter at hot-flame and at cool-flame extinction | droplet history combined with narrowband radiometer inflection and vapour-cloud onset | derived |
| hot-flame diameter and flame standoff ratio | intensified UV (OH*) camera, colour camera | derived |
| cool-flame diameter (FWHM and peak-to-peak) and peak cool-flame grey level | intensified camera in cool-flame mode | derived |
| wideband and narrowband (water-vapour) flame radiance, W | radiometers, 100 Hz | derived |
| number of hot-flame re-ignitions, hot-flame burn time | video and radiometers | derived |
| chamber pressure and temperature | CIR FCU pressure transducers (psia) and thermocouples | direct |

## Findings

1. With pure n-dodecane in air (21% O2, balance N2), droplets of about 3.8-4.7 mm at 0.5-1.25 atm burned first with a hot flame. The flame went out by radiative extinction after about 10-14 s (up to 17 s), with the droplet at about 2.9-4.3 mm. Quasi-steady cool-flame burning usually followed, often ending with a large vapour cloud. Not every test shows this: FLEX-1207 to 1210 have no cool-flame extinction diameter, the FLEX-1207 comment notes no large vapour cloud, and the FLEX-1222 comment says the flame burned to completion. The cool-flame burning-rate constant (0.31-0.43 mm^2/s) was about the same as the hot-flame value (0.30-0.52 mm^2/s). *(result, high)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx` (sheet Comments): *Excellent deployment. Ignition just before igniters pull away. Droplet drifts W in color camera FOV but stays in FOV the entire time. Hot flame extinguishers without oscillations. Long cool flame burn with large vapor cloud.*
   - `PSI-39_Analyzed Data_FLEX-1223_Summary.pdf` (p1): *P = 946.618 mmHg YO2 = 0.210 YN2 = 0.790 YCO2 = 0.000 YHe = 0.000 Dodecane D0 = 4.040 mm Dext = 3.627 mm kavg = 0.388 mm2 /sec kavg, cool = 0.401 mm2 /sec Dext, cool = 0.392 mm*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1206-1253 (C12H26, 0.21 O2, 0 He, 0.5-1.25 atm): *HF Burn Time 9.75-16.92 s; Dext, hot 2.866-4.316 mm; khot 0.301-0.516 (rows with Dext, hot); kcool 0.310-0.429 mm^2/s*
2. For n-dodecane in air the cool-flame extinction diameter falls steeply with pressure. It was 1.73-1.92 mm at 0.5 atm (50.7 kPa; 5 tests), 0.68-1.14 mm at 0.75 atm (76 kPa; 5 tests), mostly 0.26-0.85 mm at 1 atm (101 kPa; one outlier of 2.97 mm in FLEX-1251), and 0-0.39 mm at 1.25 atm (127 kPa). At 2-5 atm most droplets left no measurable residual droplet (recorded as 0 mm). The investigators note that simplified chemistry predicts these diameters less well as pressure rises. *(trend, high)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p9): *Figure 4 shows the cool flame extinction diameter as function of ambient pressure for both free-floated and fiber-supported droplets for pure n-dodecane burning in air.*
   - `PSI-39_Analyzed Data_FLEX-1239_Summary.pdf` (p1): *P = 387.398 mmHg YO2 = 0.210 YN2 = 0.790 YCO2 = 0.000 YHe = 0.000 Dodecane D0 = 4.393 mm Dext = 3.923 mm kavg = 0.318 mm2 /sec kavg, cool = 0.310 mm2 /sec Dext, cool = 1.915 mm*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1236-1240: *Dext,cool ( mm ) = 1.787, 1.731, 1.780, 1.915, 1.903 at Pressure (atm) 0.5*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1242-1246: *Dext,cool ( mm ) = 0.681, 0.792, 1.139, 0.882, 0.978 at Pressure (atm) 0.75*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1223, 1225, 1226: *Dext,cool ( mm ) = 0.392, 0.000, 0.200 at Pressure (atm) 1.25*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1251: *Dext,cool ( mm ) = 2.972*
   - <https://doi.org/10.1016/j.combustflame.2019.10.036>: *indicates deterioration of the simplified chemistry with increasing pressure in predictions of droplet diameters at cool-flame extinction.*
3. The cool-flame burning-rate constant of n-dodecane in air increases with pressure: about 0.31-0.33 mm^2/s at 0.5 atm, 0.34-0.37 at 0.75 atm, about 0.36-0.42 at 1 atm, 0.41-0.54 at 3 atm and 0.50-0.56 mm^2/s at 5 atm. The hot-flame constant changed less up to 3 atm (mostly about 0.30-0.52 mm^2/s, with outliers of 0.626 in FLEX-1229 at 2 atm and 0.215 in FLEX-1258 at 3 atm) and reached 0.49-0.66 mm^2/s at 5 atm. *(trend, medium)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1236-1240: *kcool ( mm^2/s ) = 0.325, 0.324, 0.328, 0.310, 0.311*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1254-1258: *kcool ( mm^2/s ) = 0.506, 0.492, 0.491, 0.535, 0.413 at 3 atm*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1224, 1229, 1258: *khot ( mm^2/s ) = 0.516 (1.25 atm), 0.626 (2 atm), 0.215 (3 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1259-1262: *kcool ( mm^2/s ) = 0.501, 0.519, 0.564, 0.557; khot 0.588, 0.488, 0.618, 0.659 at 5 atm*
   - `PSI-39_Analyzed Data_FLEX-1261_Summary.pdf` (p1): *P = 3777.606 mmHg YO2 = 0.210 YN2 = 0.790 YCO2 = 0.000 YHe = 0.000 Dodecane D0 = 5.646 mm D0 = nan mm kavg = 0.618 mm2 /sec kavg, cool = 0.564 mm2 /sec*
4. Above about 2 atm the cool flame often re-ignited a hot flame, sometimes repeatedly. The sequence was hot flame, radiative extinction, cool flame, hot re-ignition, cool flame again, until the fuel was used up. No n-dodecane test at 0.5-1.25 atm re-ignited. In the spreadsheet, re-ignitions are logged for all 4 n-dodecane tests in air at 2 atm (FLEX-1227 twice, 1228-1230 once each) and for up to 7 cycles in one 3 atm test (FLEX-1258, D0 = 5.5 mm). The investigators had not expected this from FLEX. Under fire-safety applications, a CFI presentation notes that in space a persisting cool flame can generate combustible vapour that can re-ignite. *(result, high)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p6): *However, as the ambient pressure is increased above 2 atm, multiple reignition cycles were observed, where first the hot flame extinguishes due to radiative heat loss followed by cool flame, and then reignition to a hot-flame followed by a cool flame, with this cycle repeating several times until…*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p6): *This behavior is unexpected based on earlier observations from FLEX experiments.*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1258: *Reignitions = 7 (Pressure 3 atm, D0 5.493 mm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1227-1230: *Reignitions = 2, 1, 1, 1 (C12H26, 0.21 O2, 2 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Comments, row Flex Number 1227: *Hot flame oscillations then extinguishes after 12 sec. 7 sec ater entinction hot flame re-ignites followed by another re-ignition then cool flame burning.*
   - `PSI-39_Presentations_Cool Flames in Space, a Hot Prospect on Earth_CFI.pdf` (p22): *In space “cool flame” can persist after hot flame extinction and generate combustible vapor that can reignite (similar to smoldering combustion in solid fuels)*
5. Helium dilution at 21% O2 shortened the hot flame and enlarged the cool-flame extinction diameter. At 1 atm, n-dodecane extinction diameters were 0.90-0.97 mm with 29% helium (vs mostly 0.26-0.85 mm without) and 2.10-2.57 mm with 59% helium. Hot-flame burn time fell from about 10-12 s in air to about 7 s at 29% helium and 1.9-3 s at 59% helium. In FLEX-1281 (59% He, 1 atm) the hot flame existed only while the igniters were on. *(trend, high)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p9): *Increase helium dilution leads to earlier cool flame extinction giving a larger extinction diameter.*
   - `PSI-39_Analyzed Data_FLEX-1264_Summary.pdf` (p1): *P = 763.248 mmHg YO2 = 0.210 YN2 = 0.500 YCO2 = 0.000 YHe = 0.290 Dodecane D0 = 4.217 mm Dext = 3.906 mm kavg = 0.426 mm2 /sec kavg, cool = 0.464 mm2 /sec Dext, cool = 0.974 mm*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1263, 1264, 1266: *Dext,cool ( mm ) = 0.922, 0.974, 0.900; HF Burn Time 6.72, 7.18, 6.88 s (He 0.29, 1 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1281, 1282, 1284: *Dext,cool ( mm ) = 2.098, 2.536, 2.570; HF Burn Time 1.90, 3.03, 2.85 s (He 0.59, 1 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Comments, row Flex Number 1281: *Dim blue flame (no soot) appears 6 sec after igniters come on. Flame only exists while igniters are on.*
   - <https://ntrs.nasa.gov/citations/20205008449>: *The results show that the cool-flame extinction diameter is drastically increased with helium dilution compared to N2, CO2 or Xe, and Xe dilution leads to longer burning with a smaller extinction diameter.*
6. Adding iso-dodecane suppressed cool flames, most clearly in the 60/40 blend at low pressure. At 0.5-0.75 atm in air, 60/40 droplets had cool-flame burning-rate constants of only 0.10-0.23 mm^2/s, against 0.31-0.37 for pure n-dodecane, and cool-flame 'extinction' diameters of 3.8-5.6 mm, within about 0.1 mm of their hot-flame extinction diameters. In other words, the cool flame barely lasted. The 75/25 blend at 0.75 atm behaved more like pure n-dodecane (extinction diameters 0.48 and 0.90 mm). *(result, medium)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p7): *The addition of iso-dodecanol reduces the tendency to form cool flames in n-dodecanol.*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1355, 1356, 1358: *Dext, hot 5.295, 4.897, 5.670 mm; Dext,cool 5.281, 4.867, 5.628 mm; kcool 0.233, 0.116, 0.114 mm^2/s (60/40, 0.5 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1346-1348: *Dext,cool ( mm ) = 3.754, 5.189, 5.233; kcool 0.201, 0.097, 0.174 (60/40, 0.75 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1343, 1344: *Dext,cool ( mm ) = 0.482, 0.902 (75/25, 0.75 atm)*
7. At 17% O2 and 1 atm the hot flame was weak and short-lived: 4.7-7.2 s for n-dodecane and 3.3-4.7 s for the blends, with hot-flame burning-rate constants often below 0.1 mm^2/s for the blends. Pure n-dodecane still showed cool-flame burning, with larger extinction diameters (1.27-2.87 mm) than in air. Most blend tests at 17% O2 and 1 atm have no cool-flame burning rate in the spreadsheet; one 75/25 test extinguished at 4.35 mm. *(limit, medium)*
   - `PSI-39_Analyzed Data_FLEX-1215_Summary.pdf` (p1): *P = 773.386 mmHg YO2 = 0.169 YN2 = 0.830 YCO2 = 0.001 YHe = 0.000 Dodecane D0 = 4.289 mm Dext = 4.194 mm kavg = 0.163 mm2 /sec*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1213, 1215, 1217: *Dext,cool ( mm ) = 1.267, 1.861, 2.868; HF Burn Time 4.73, 5.22, 5.57 s (C12H26, 0.17 O2, 1 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1285-1294: *khot 0.001-0.156 mm^2/s, HF Burn Time 3.27-4.70 s; kcool only for 1285 (0.572), Dext,cool 4.348 mm (blends, 0.17 O2, 1 atm)*
8. The narrowband (water-band) radiometer signal rose with pressure for n-dodecane in air of similar size, while peak wideband hot-flame radiance stayed at about 20-27 W for 4-4.5 mm droplets at 0.5-5 atm (one higher value, 30.4 W, in FLEX-1237 at 0.5 atm). Peak narrowband radiance was about 6.9-7.7 W at 0.5 atm, about 8 W at 1 atm, about 10.3-10.5 W at 3 atm and about 12.9-13.3 W at 5 atm. 5.6 mm droplets at 5 atm reached 44-50 W wideband. *(trend, medium)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1237-1240: *Peak Water Vapor Rad 7.67, 7.50, 7.18, 6.88 W; Peak HF Rad 30.4, 24.7, 23.5, 22.5 W (0.5 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1254-1256: *Peak Water Vapor Rad 10.50, 10.25, 10.31 W (3 atm)*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet DATA, row Flex Number 1259-1262: *Peak Water Vapor Rad 13.28, 12.91, 21.46, 27.55 W; Peak HF Rad 24.9, 24.3, 44.0, 50.0 W (5 atm; 1261-1262 have D0 about 5.6 mm)*
   - `PSI-39_Science Documents_SRD_CFI.pdf` (p21): *The total flame radiance during the cool flame is more than an order of magnitude smaller than the flame radiance during the hot flame.*
9. Soot behaviour changed with pressure. At low pressure the hot flame formed a stable spherical soot shell, and none formed during the cool flame. As pressure rose the shell became diffuse and ill-defined, and residual soot stayed around the droplet after hot-flame extinction. The investigators state the mechanism is not understood. *(result, medium)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p10): *At low pressures a stable spherical soot-shell is formed. However, as the pressure increase the soot-shell becomes diffuse and undefined.*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p10): *But, when the pressure increases, residual soot is seen surrounding the droplet even after the hot flame extinction.*
   - `PSI-39_Analyzed Data_FLEX-1227_Summary.pdf` (p1): *Heavy soot near droplet*
10. At higher pressure (for example n-dodecane at 3 atm with 29% He, FLEX-1268), radiative extinction was followed by an intermediate 'warm flame', not visible on the colour camera. A hot flame then re-ignited and quickly went out to a cool flame. The investigators attribute warm flames to intermediate-temperature chemistry becoming active, and report that helium appears to help the heat-release/heat-loss balance in the NTC region. Sources conflict on the FLEX-1268 atmosphere: the Final Report's Figure 3 caption gives 12% O2/50% N2/29% He, while the data-summary spreadsheet (Master Sheet) gives O2 0.21, N2 0.50, He 0.29. The caption's 12% is probably a typo for 21%, since 12 + 50 + 29 = 91%. *(result, low)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p8): *Figure 3: FLEX-1268 – N-dodecane at 3 atm burning in 12%O2 – 50% N2 – 29% Helium. Reignition and warm flame formation are shown.*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Master Sheet, row Flex Number 1268: *Pressure 3 atm; Oxygen 0.21; Nitrogen 0.5; Helium 0.29; Fuel C12H26*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p7): *During warm flames the heat release rate dynamically balance the heat loss rate. Addition of helium seems to enhance this balance within the NTC region.*
11. The 40 um SiC support fibre had little effect on the n-dodecane cool-flame extinction diameter. For example, at 0.5 atm fibre-supported tests gave 1.73-1.79 mm and free droplets 1.90-1.92 mm. CFI used the 40 um fibre because FLEX's 80 um fibre had disturbed droplets near cool-flame extinction in almost all tests. *(method, medium)*
   - `PSI-39_Reports_CFI Science Final Report.pdf` (p9): *It is interesting to note that the 40 micron fiber shows relatively little effect on the extinction diameter.*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Master Sheet / DATA, row Flex Number 1236-1240: *Fiber Yes: Dext,cool 1.787, 1.731, 1.780; Fiber No: 1.915, 1.903 (0.5 atm)*
   - `PSI-39_Science Documents_CFI_SCR.pdf` (p7): *80 µm fiber in FLEX experiments created disturbances to droplet near cool flame extinction in almost all tests*
12. Farnesane (2,6,10-trimethyldodecane, cetane number 58) also supported cool flames in air at 1 atm. In FLEX-1393 (D0 = 4.61 mm) the hot flame extinguished at 4.33 mm, then a long cool flame (k_cool = 0.339 mm^2/s) extinguished at 1.27 mm with a large vapour cloud. In one 17% O2 test (FLEX-1426) the comment notes a very limited cool-flame burn. Farnesane tests are listed but not analysed in the data-summary spreadsheet. *(result, low)*
   - `PSI-39_Analyzed Data_FLEX-1393_Summary.pdf` (p1): *Farnesane D0 = 4.613 mm Dext = 4.330 mm kavg = 0.328 mm2 /sec kavg, cool = 0.339 mm2 /sec Dext, cool = 1.265 mm*
   - `PSI-39_Science Documents_SRD_CFI.pdf` (p31): *farnesane (2,6,10 trimethyldodecane), and 2,2,4,6,6 pentamethylheptane of carbon number similar to n-dodecane have derived cetane numbers of 58 and 15 in comparison to n-dodecane and its derived cetane number of 78*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Comments, row Flex Number 1393: *Perfect deployment. Very slow drift W after ignition. Near-perfect test. Stays in FOV the entire test. Long hot-flame burn w/ no oscillations at extinction. Long cool flame burn and large vapor cloud.*
   - `PSI-39_Science Documents_CFI_DataSummary_Spreadsheet_Jan2021.xlsx`, sheet Comments, row Flex Number 1426: *Good deployment on fiber. Good ignition. Very limited cool flame burn. Large residual droplet on fiber.*

## Fire-safety relevance

CFI is a fundamental combustion-chemistry experiment, not a material-flammability test, but it points to a spacecraft fire hazard. In microgravity, a burning liquid fuel (or, by analogy, a fuel-soaked object) whose visible flame has gone out can keep reacting through an invisible cool flame at about 700-900 K. That flame gasifies the fuel at nearly the hot-flame rate and leaves a cloud of fuel vapour and partly oxidised products. At 2 atm and above it repeatedly re-ignited hot flames, and a FLEX re-ignition burned brighter than the original flame, consistent with a premixed flame through the accumulated vapour. Detection and extinguishment criteria based only on visible flame or hot-flame radiation may therefore declare a fire out too early. The narrowband water-vapour radiometer did detect cool flames. Helium dilution and lower O2 shortened hot flames but increased the cool-flame extinction diameter, so inert agents change how much liquid is left unburned and vaporising.

### Habitat conditions

CFI used only 17% and 21% O2, with N2 or N2/He diluent, at 0.5-5 atm (50.7-506.6 kPa). The 21% O2, 1 atm tests match the Earth sea-level reference (20.9% O2 at 101.3 kPa). No test used the elevated-O2, reduced-pressure atmospheres planned for exploration: the Moon-habitat reference is 30% or more O2 at 70.3 kPa or less, and the spacesuit reference is 100% O2 at 29.6 kPa. The 0.5 and 0.75 atm air tests (O2 partial pressure about 10.7 and 16 kPa) are closest in total pressure to a habitat, but have much lower oxygen partial pressure. The low-pressure trend (larger cool-flame extinction diameter and slower cool-flame burning as pressure falls) suggests cool flames would be shorter-lived at habitat pressure, but the effect of 30% O2 was not measured. The SRD planned O2 up to 0.35-0.40 and xenon diluent, but these were not in the flown matrix. The predecessor FLEX tested a 30/70 O2/N2 pre-EVA atmosphere at 0.7 atm.

### Earth benefits

Data for validating low-temperature (NTC) chemical kinetic mechanisms for n-dodecane, a jet/diesel surrogate component, its branched isomer and the renewable fuel farnesane. These mechanisms underpin autoignition, knock, octane and cetane behaviour and the design of low-temperature engines (HCCI, RCCI). Other suggested applications are cool-flame fuel reforming (for example hydrogen for fuel cells) and new spray-burner concepts.

## Limitations

- By the final report (July 2020) the investigators had not fully analysed or modelled the CFI data. Findings are 'general observations' from preliminary analysis. The spreadsheet marks 81 of 227 test points as not analysed, including all 44 farnesane tests and all 75/25 blend tests with helium.
- The flown matrix was much narrower than the SRD plan. The SRD planned O2 of 0.10-0.40, xenon and CO2 diluents, surrogate blends (PRF, TRF, Jet-A surrogate), pentamethylheptane blends and a DTBP additive. CFI flew only 17-21% O2, N2/He, and three fuel types.
- The cool-flame extinction diameter is sometimes recorded as 0 mm (no residual droplet, e.g. burned to completion after re-ignitions), sometimes left blank, and is occasionally an outlier (2.97 mm in FLEX-1251 against about 0.3-0.5 mm for its neighbours). In the 60/40 blend at low pressure it is close to or slightly above the hot-flame extinction diameter. Per-test comments and plots must be checked before the column is used as a kinetic target.
- Several tests lost data: the intensified camera failed to switch to continuous mode in FLEX-1208 to 1210 (no hot- or cool-flame images), and droplets drifted out of the field of view or hit igniters (e.g. FLEX-1228, 1229). Many raw image streams have missing frames or irregular frame intervals, as logged in the Comments files.
- Droplet ignition used hot wires and a strong ignition stimulus. Cool flames in this configuration occur almost only after radiative extinction of a large (about 4 mm) droplet's hot flame, so the results describe large isolated droplets in a quiescent gas. They do not describe sprays, pools, wicks or ventilated cabins.

## Data in PSI

PSI-39 holds 2,832 files (about 719 GB), 2,125 of them downloaded locally. Nearly all the volume is Raw Data (2,791 files, 718.9 GB): 337 zip image archives (588.9 GB), one per camera stream per test point for 85 test points, with suffixes A, C, D, G and a few S/I; 120 .ts and 126 .mp4 downlink video recordings (109.8 and 18.9 GB); and 1,793 small text files. For each of about 123 CIR test points (CIR ids such as F068A03) there are: test-point settings (igniter power and on-time, needle and igniter positions, dispensed volume), camera settings, filter and CFI-mode logs, chamber readings (pressures in psia and temperatures in deg C, about 1 Hz), radiometer readings, image timing indexes, and a 'Comments' file. The Comments files are data-integrity logs (missing image files, bad frame intervals, re-downlinks), not science notes. For a subset of tests there are reduced text files (FLEX-xxxx_DropletData, RadiometerData, ColorCamData, CoolFlameData, TestSheet), 22 RTF test sheets and 28 Igor .pxp analysis files. The most usable products are the Jan 2021 data-summary spreadsheet, which gives 227 test conditions, and for 146 analysed tests D0, extinction diameters, k_hot, k_cool, re-ignition counts, burn time and peak radiances, with operator comments per test; and 30 Analyzed Data PDFs (FLEX-1206 to 1264 and 1393), each a one-page plot of droplet, flame and radiance histories. The 87-row experimental table is a partial subset of the spreadsheet's Master Sheet.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | per-test-point zipped image streams (backlit droplet, intensified, colour, IR/HiBMS-2) | .zip | 337 | 589 GB | no |
| Raw Data | downlinked colour-camera video recordings per test | .ts .mp4 | 246 | 129 GB | no |
| Raw Data | per-test-point text logs: testpoint settings, camera settings, filter/CFI-mode positions, chamber readings, radiometer readings, image timing indexes, data-integrity comments | .txt | 1793 | 180 MB | yes |
| Raw Data | reduced per-test data for a subset: Igor experiments, RTF test sheets, sample image PDFs, an image slide deck, image metadata | .pxp .rtf .pdf .pptx .meta .metadata | 415 | 1.04 GB | yes |
| Science Documents | SRD (Nov 2014), Science Concept Review (May 2014), data-summary spreadsheet (Jan 2021; sheets Master Sheet, DATA, Camera Settings, Igniter, Comments) | .pdf .xlsx | 3 | 20 MB | yes |
| Analyzed Data | one-page summary plots per test (droplet d^2, flame diameter, FSR, radiance, cool-flame diameter), FLEX-1206 to 1264 and 1393, plus one Igor file | .pdf .pxp | 32 | 10 MB | yes |
| Reports | CFI Science Final Report (Nayagam and Dietrich, 23 Jul 2020) | .pdf | 1 | 0 B | yes |
| Presentations | 2013 ISS R&D conference and 2015 ASGSR talks on FLEX cool flames (pre-CFI) | .pdf | 2 | 10 MB | yes |
| Experimental table | 87-row test list (FLEX number, date, CIR id, pressure, O2, N2, He, fibre, fuel) | .csv | 1 | 0 B | yes |

Rows in the unified `tests` table: 87

## Related investigations

- [PSI-69](PSI-69-flex.md): precursor
- [PSI-68](PSI-68-flex-2.md): precursor
- [PSI-159](PSI-159-acme-cfi-g.md): shared hardware
- [PSI-117](PSI-117.md): ground re-analysis
- [PSI-142](PSI-142.md): ground re-analysis

## Open questions

- Fit the n-dodecane cool-flame extinction diameter against pressure (0.5-5 atm), O2 (0.17, 0.21) and helium (0-0.59) from the DATA sheet, and compare with the Williams-Nayagam simplified chemistry and with detailed mechanisms to quantify the pressure deterioration they report.
- Analyse the 44 farnesane tests (FLEX-1388 to 1431), which have raw data but no reduced values in the spreadsheet, and compare cool-flame burning rates and extinction diameters with n-dodecane against cetane number (58 vs 78).
- Use the narrowband water-band radiometer records to build an objective cool-flame-presence and extinction detector, and test whether a fire sensor could flag invisible cool-flame burning after visible extinction.
- Quantify the re-ignition period and the number of cycles against pressure, droplet size and helium fraction (Reignitions column plus radiometer traces), and estimate the fuel vapour mass accumulated before each re-ignition.
- Measure soot-shell diameter and its loss of definition with pressure from the backlit images, to address the unexplained high-pressure soot behaviour.
- Separate fibre and free-droplet effects on k_cool and extinction diameter across all conditions using the Fiber column.

## Dashboard ideas

- **cool-flame extinction diameter vs pressure** (`pressure_kpa`, `fuel`, `x_he`, `fiber`, `D0_mm`, `Dext_cool_mm`): Reproduces the Final Report's Figure 4 and the helium effect (Figure 5) from the 227-row DATA sheet.
- **burning-rate constants by regime** (`pressure_kpa`, `fuel`, `x_o2`, `x_he`, `k_hot_mm2_s`, `k_cool_mm2_s`): Shows k_cool rising with pressure and iso-dodecane suppression at low pressure.
- **test timeline and outcome** (`flex_number`, `date`, `cir_id`, `fuel`, `pressure_atm`, `x_o2`, `x_he`, `fiber`, `reignitions`, `completed_analysis`, `comment`): Lets a user see which of the 227 tests were analysed, which re-ignited, and which have raw data.
- **droplet/flame/radiance history** (`t_over_D0sq`, `d_over_D0_sq`, `flame_diameter_mm`, `wideband_W`, `narrowband_W`): The FLEX-xxxx DropletData and RadiometerData text files allow re-plotting the summary graphs for the analysed tests.

## Gaps and data-quality notes

- Dates conflict. The PSI record gives investigationStartDate 10-01-2020 and investigationEndDate 10-20-2021. The experimental table and data-summary spreadsheet date the tests 9 Mar 2017 to 15 Sep 2017. The Final Report (dated 23 Jul 2020) says operations ran from January 2017 through September 2017. The record uses the dated test span (2017-03-09 to 2017-09-15). The 2020-2021 PSI dates may refer to a data-processing or archiving period; no document explains them.
- The spreadsheet Master Sheet dates FLEX-1411 (farnesane) to 2011-09-06, which is clearly a typing error for 2017 (neighbouring tests are August-September 2017). The tests table now corrects it to 2017-09-06 using its CIR code.
- The experimental table CSV (87 rows) lists FLEX-1285-1289 and 1295-1297 twice, so it has only 79 unique tests. It omits all farnesane tests and pure-dodecane tests at 0.5, 0.75, 3 and 5 atm and with helium. FLEX-1219 to 1222 list O2 0.21 + N2 0.76 (sum 0.97). Pressure strings carry trailing spaces. The full 227-row list is in the data-summary spreadsheet, which was read directly; facts from rows beyond its preview are cited as psi_table.
- The PSI record's approach says the chamber pressure ranged from 0.25 to 0.5 atm, and its objective and the Final Report mention 0.25 atm. No test below 0.5 atm appears in the table or spreadsheet, and the Operational Requirements give 0.5-5.0 atm. The approach also calls nitrogen 'atomic nitrogen' (it is N2).
- The Final Report text says 'n-dodecanol' and 'iso-dodecanol' in section 5.1, which are evidently typos for n-dodecane and iso-dodecane (its figure captions and all data use the alkanes). The PSI record hypothesis says 'faresane' for farnesane.
- The SRD says the initial chamber temperature will be 'around 250 C'. This is presumably a typo for about 25 C: the FLEX-1206 test sheet logs 299.19 K and the chamber readings about 24-27 C.
- The PSI record contact list gives D. Dietrich's email with a misspelled surname; contact emails were not copied into this record.
- The Final Report figures (cool-flame extinction diameter vs pressure; helium effect; backlit soot images) have no text layer for the plotted values, and the PDF pages could not be rendered here (no poppler). Values were taken from the data-summary spreadsheet instead. FLEX-1248_Summary.pdf failed text extraction (PdfStreamError).
- The main CFI results paper (Dietrich et al. 2024, Microgravity Sci. Technol., doi 10.1007/s12217-024-10115-x) is closed access, and its abstract is not available from Springer, Crossref or Semantic Scholar. Its results are not included. The 2020 ASGSR abstract on NTRS and the Williams and Nayagam 2020 Combustion and Flame abstract were reachable and are cited.
- Raw image zips, .ts and .mp4 videos (about 718 GB) were not inspected. The per-test 'Comments.txt' raw files sampled (e.g. F068A03, F160A03, F180D04) contain only image-integrity logs, not science observations. Science observations are in the spreadsheet Comments sheet.
- The two presentations (2013, 2015) predate CFI flight and describe FLEX cool-flame results and theory (partial-burning regime, flame standoff ratio about 3.1, extinction correlated with oxygen concentration to the -3/2 power). They give no CFI data.
- No 30-day operational accomplishments report exists (the Final Report appendix says 'Not available'). The Final Report gives the PSI data organisation as FLEX-1206 to 1284 (n-dodecane), 1285 to 1387 (blends) and 1388 to 1431 (farnesane).
- Publication review (Nov 2026; per-paper notes in data/publications/PSI-39.json): of the 7 listed publications, 1 was read in full (NTRS preprint of Nayagam et al. 2015), 3 by abstract and 3 not at all (Nayagam et al. 2012 Combustion and Flame, the 2024 CFI results paper, and the NASA blog post "Science in Short: Cool Flames", whose URL now redirects and whose archived copy refused automated access). The readable papers analyse FLEX/FLEX-2 n-heptane, n-octane and n-decane data from before CFI; none adds CFI-specific results to this record.
