# PSI-69: FLEX (Flame Extinguishment Experiment)

Single drops of methanol and heptane were burned floating freely on the Space Station in air thinned with nitrogen, carbon dioxide or helium, to find how little oxygen still lets a fuel burn in weightlessness and how well these gases put flames out; it also discovered that heptane drops keep burning with an invisible 'cool flame' after the visible flame dies.

Investigators: Forman A. Williams (University of California, San Diego) - Principal Investigator; Frederick L. Dryer (listed in PSI under University of South Carolina; Princeton University in the 2015 NASA report) - Co-Investigator; Benjamin D. Shaw (University of California, Davis) - Co-Investigator; Mun Y. Choi (listed in PSI under University of Missouri; University of Connecticut in the 2015 NASA report) - Co-Investigator; Vedha Nayagam (Case Western Reserve University / NASA GRC) - Co-Investigator; Michael C. Hicks (NASA Glenn Research Center) - Co-Investigator; Daniel L. Dietrich (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Setting | ISS · CIR (FCF) · MDCA |
| Platform | International Space Station (ISS), Destiny module |
| Facility | Combustion Integrated Rack (CIR) of the Fluids and Combustion Facility (FCF) |
| Dates | 2007-08-01 to 2016-07-31 |
| Fuels and samples | methanol; n-heptane |
| Varied | ambient oxygen fraction: 0.12-0.34 (0.12-0.21 at 1 atm in N2; 0.30 and 0.34 at 0.7 and 1 atm) mole fraction<br>carbon dioxide fraction (suppressant): 0.05-0.50 at 0.7-1 atm; 0.70 at 2-3 atm mole fraction<br>helium fraction (suppressant): 0.05-0.45 mole fraction<br>ambient pressure: 70-73 kPa (103 tests), 100-103 kPa (161 tests), 206-309 kPa (9 tests); original 526-2320 mmHg kPa<br>initial droplet diameter: 1.10-4.67 mm<br>fuel: methanol, n-heptane<br>support: free-floating or 80 um SiC fibre (some translated at low speed) |
| Number of tests | 274 |
| Fire-safety pillars | suppression, fundamental, prevention |

## Question

FLEX asked how much inert gas (carbon dioxide, helium, or extra nitrogen) is needed to stop a liquid fuel burning in microgravity, and how this depends on oxygen fraction and pressure, with the limiting oxygen index (LOI, the lowest ambient oxygen fraction supporting quasi-steady burning) as the headline quantity. The underlying hypothesis was that the absence of buoyant convection changes transport, radiative loss and chemistry so much that flammability limits and suppressant efficacy differ from those measured on Earth. The droplet was chosen because its spherical symmetry makes the problem one-dimensional, so measurements can test detailed chemical-kinetic and transport models that can then be used for spacecraft fire-suppression design. Pressures down to 0.5-0.7 atm were included because venting a cabin is itself a suppression strategy.

## Summary

FLEX burned isolated, mostly free-floating methanol and n-heptane droplets (initial diameter about 1.1-4.7 mm) in the ISS Combustion Integrated Rack between March 2009 and December 2011, in oxygen/nitrogen atmospheres diluted with carbon dioxide or helium at 0.7-3 atm. Cameras recorded droplet diameter and flame size, giving burning-rate constants (typically 0.4-0.6 mm2/s), extinction diameters and burn times for 274 tests. Small droplets extinguished diffusively, large ones radiatively, and the limiting oxygen index (LOI), where the two limits meet, was about 0.12 for methanol and 0.15 for heptane in nitrogen at 1 atm. Adding carbon dioxide to air raised the LOI to about 0.14 and 0.17; helium raised it to about 0.14 and 0.15. These limits are lower than in normal gravity, so terrestrial inert-gas suppressant standards carry less safety margin in orbit. Large heptane droplets kept burning after visible radiative extinction, supported by low-temperature cool-flame chemistry, which raises the possibility of an unseen fire re-igniting.

## Physics

A fuel droplet in still microgravity burns inside a spherical diffusion flame: fuel vapour diffuses outward, oxygen inward, and they meet at a flame several droplet diameters away. Heat conducted back from the flame evaporates the liquid, so the burning rate is set by gas-phase diffusion and the squared diameter falls linearly in time (the classical d-squared law). On Earth, buoyancy elongates the flame and blows fresh oxidizer in; without it the flame is larger, cooler, slower and long-lived, so two extinction mechanisms appear. Diffusive (kinetic) extinction happens late, when the shrinking droplet brings the flame so close that residence time is too short for chemistry (low Damkohler number). Radiative extinction happens early for large droplets, whose big flames lose a large share of their heat release to radiation from CO2, H2O and soot. Lowering oxygen makes diffusive extinction occur at larger diameters and radiative extinction at smaller ones; the oxygen fraction at which the two meet is the LOI, below which only transient burning after ignition is possible. Diluents act through heat capacity (CO2 lowers flame temperature and also radiates), conductivity and diffusivity (He raises burning rate and Lewis-number effects) and radiation. Methanol is special because it absorbs product water, which eventually dilutes the fuel and triggers extinction at a size that grows with initial diameter. Large n-alkane droplets showed a second, previously unknown regime: after radiative extinction of the hot flame, low-temperature (about 700 K) cool-flame chemistry in the negative-temperature-coefficient range sustains quasi-steady evaporation until a second, cool-flame extinction, after which unburned vapour forms a visible cloud.

$$
D^2(t) = D_0^2 - K\,t, \qquad K = -\frac{d(D^2)}{dt}
$$

The d-squared law: for quasi-steady, spherically symmetric burning the square of droplet diameter $D$ (mm) falls linearly with time $t$ (s) from its initial value $D_0$; the slope is the burning-rate constant $K$ (mm2/s). FLEX reports an average $K$ from a linear fit of $D^2(t)$ between about 0.1 and 0.9 of the burn time (from shortly after ignition to extinction). Valid after the ignition/heat-up transient and away from extinction, where the instantaneous slope decreases; methanol water absorption and large radiative losses cause departures.

Textbook background: Godsave/Spalding d-squared law.
<https://doi.org/10.1007/s12217-014-9372-2>: *The average burning rate constant (¯k) comes from a linear fit of the droplet-squared history between approximately t = 0.1τb and 0.9τb*
<https://ntrs.nasa.gov/api/citations/20150023456/downloads/20150023456.pdf>: *Burning rate—average burning rate constant from a linear fit of the droplet diameter squared versus time from shortly after ignition to extinction*

$$
K = \frac{8\lambda_g}{\rho_l c_{p,g}}\ln(1+B), \qquad B = \frac{q_f Y_{O,\infty} f + c_{p,g}(T_\infty - T_b)}{L}
$$

Classical quasi-steady burning-rate constant used by the FLEX team to compare with measured $K$. $\lambda_g$: gas thermal conductivity (W/(m K)); $c_{p,g}$: gas specific heat (J/(kg K)), both evaluated with the Law-Williams property rule; $\rho_l$: liquid density (kg/m3); $B$: Spalding transfer number (dimensionless); $q_f$: heat of combustion per unit fuel mass (J/kg); $Y_{O,\infty}$: ambient oxygen mass fraction; $f$: stoichiometric fuel-to-oxygen mass ratio, so $q_f Y_{O,\infty} f$ is the heat released per unit mass of ambient gas; $T_\infty$, $T_b$: ambient and fuel boiling temperatures (K); $L$: latent heat of vaporization (J/kg). It explains why helium (high $\lambda_g$) raises $K$ and why $K$ increases with oxygen. It neglects radiation, transient flame growth and water absorption; FLEX found small methanol droplets burned faster than this prediction.

Textbook background: Spalding B-number theory of droplet burning.
<https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *It is interesting to note that the smaller droplets have a higher burning-rate constant than the classical quasi-steady prediction.*

$$
t_b \approx \frac{D_0^2 - D_{ext}^2}{K}
$$

Burn time implied by the d-squared law: $t_b$ (s) is the time from ignition to visible flame extinction at droplet diameter $D_{ext}$ (mm), for initial diameter $D_0$ (mm) and average burning-rate constant $K$ (mm2/s). Applied to the 188 PSI table rows with all four quantities and a non-zero extinction diameter, the tabulated burn time is a median 1.05 times this estimate (interquartile range 1.03-1.09), the small excess being the ignition transient. This consistency is our check that the PSI column 'Burning rate; mm' is $K$ in mm2/s.

Textbook background: Direct integration of the d-squared law.
Table `tests`: Computed from PSI-69_Experimental table_FLEX.csv: ratio of 'Burn time; s' to (d0^2 - d_ext^2)/K for rows with d_ext > 0 and all values numeric (n = 188); median 1.053, IQR 1.03-1.09, median 1.05 for both fuels.

$$
\mathrm{Da} = \frac{t_{res}}{t_{chem}}, \quad t_{res} \sim \frac{D_f^2}{\alpha} \propto D^2; \qquad \mathrm{Da} \le \mathrm{Da}_c \Rightarrow \text{diffusive extinction}
$$

Damkohler-number criterion for diffusive (kinetic) extinction. $t_{res}$: residence time of reactants in the flame zone (s), scaling with flame diameter $D_f$ squared over thermal diffusivity $\alpha$ (m2/s); because $D_f/D$ is roughly constant during quasi-steady burning, $t_{res}$ shrinks with $D^2$. $t_{chem}$: chemical time (s), which grows steeply as flame temperature falls (lower O2). For CO2 dilution this simple picture does not hold: the precursor methanol work at fixed 21% O2 found that more CO2 slightly decreased the extinction diameter. Extinction occurs when Da drops to a critical value $\mathrm{Da}_c$, so lower oxygen gives larger diffusive extinction diameters. The FLEX team's earlier CO2 precursor work correlated methanol extinction diameters with a critical-Damkohler theory; activation-energy asymptotics with water absorption were later used.

Textbook background: Damkohler-number extinction theory of diffusion flames.
<https://ntrs.nasa.gov/api/citations/20110020695>: *These results are interpreted using a critical Damk hler number for extinction as predicted by an earlier theory*
<https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *An activation energy asymptotic theory accounting for time-dependent water dissolution or evaporation from the droplet is shown to predict the measured diffusive extinction conditions well.*

$$
\frac{\dot Q_{rad}}{\dot Q_{chem}} \sim \frac{\kappa_P\,\sigma T_f^4\,D_f^3}{q_f\,\rho_l K D} \propto D_f^2 \;\; (D_f \propto D)
$$

Order-of-magnitude reason why large droplets extinguish radiatively. Radiative loss from an optically thin flame scales with flame volume ($\propto D_f^3$), with Planck-mean absorption coefficient $\kappa_P$ (1/m), Stefan-Boltzmann constant $\sigma$ and flame temperature $T_f$ (K); chemical heat release scales with fuel mass burning rate, $\propto \rho_l K D$ ($q_f$ heat of combustion). The ratio therefore grows with flame (and droplet) size, so above some size the flame cools below its extinction temperature soon after ignition. CO2 dilution increases $\kappa_P$ and lowers $T_f$, moving radiative extinction to smaller droplets. A later FLEX-team scaling based on a critical flame temperature correlates measured radiative extinction diameters.

Textbook background: Optically thin radiative loss scaling for spherical diffusion flames.
<https://doi.org/10.1016/j.combustflame.2018.04.023>: *a simple scaling analysis, based on the assumptions that radiative extinction occurs when the flame temperature drops to a critical value and that the radiative heat loss rate is a fraction of the heat-release rate at the flame, is able to correlate the measured droplet diameter at extinction*
<https://doi.org/10.1007/s12217-014-9372-2>: *Carbon dioxide is also a radiatively participating gas*

$$
x_{O_2,LOI}: \; D_{ext}^{diff}(x_{O_2}) = D_{ext}^{rad}(x_{O_2})
$$

Operational definition of the limiting oxygen index used by FLEX. $x_{O_2}$: ambient oxygen mole fraction. As $x_{O_2}$ decreases, the diffusive extinction diameter $D_{ext}^{diff}$ (mm) increases and the radiative extinction diameter $D_{ext}^{rad}$ (mm) decreases; where they become equal no droplet size can burn quasi-steadily. Below it, ignition can still produce short transient burning sustained by igniter energy. Measured values (1 atm): methanol 0.12 and heptane 0.15 in O2/N2.

<https://doi.org/10.1007/s12217-014-9372-2>: *the limiting oxygen index (LOI), the oxygen concentration below which quasi-steady combustion cannot be supported. This is also the ambient oxygen mole fraction for which the radiative and diffusive extinction diameters become equal.*

## Method

### Apparatus

The CIR provides a ~90-95 L combustion chamber rated to about 9 atm (limited to about 3 atm for FLEX by safety analysis), a Fuel and Oxidizer Mixing Apparatus that fills the chamber from gas bottles and ISS nitrogen, and a vent to space. The MDCA insert dispenses fuel from syringe reservoirs (about 2.5 ml methanol and 1.25 ml heptane) through two opposed 250 um needles, stretches the liquid bridge, then retracts the needles to leave a nearly motionless free droplet; some tests used an 80 um SiC fibre that could also translate the droplet slowly. Two hot-wire igniters at 180 degrees ignite the droplet and retract. Diagnostics: backlit High Bit-Depth Multispectral camera (1024x1024, ~30 mm field, 30 fps; droplet size and soot), intensified Low Light Level UV camera with a 310 nm OH* filter (~50 mm field), and the MDCA colour camera (~93 mm field, downlinked live for operations). MDCA radiometers were not sensitive enough for quantitative data in 2009-2011. The rack sits on the Passive Rack Isolation System; measured g-levels were typically below 1e-5 g0.

### Fuels and samples

- methanol (CH3OH) (liquid, free-floating or SiC-fibre-tethered droplet, initial diameter 1.6-4.5 mm in PSI table)
- n-heptane (C7H16) (liquid, free-floating or SiC-fibre-tethered droplet, initial diameter 1.1-4.7 mm in PSI table)

### Procedure

Tests were run remotely from the Telescience Support Center at NASA Glenn, about 4-10 droplets per session; crew changed fuel reservoirs, gas bottles and fibres. For each test the chamber was filled (or an existing fill reused after ~1 min fan mixing), a droplet of chosen size was dispensed and stretched, the needles retracted, the igniters energised for a preset time and withdrawn, and cameras recorded for typically ~40 s. Because atmospheres were reused, the reported composition was computed from fill records and corrected for oxygen consumed and CO2, H2O and fuel vapour produced. The LOI search started at a high oxygen fraction (0.21 at 1 atm, or 0.25 with CO2 at 0.7 atm) and progressively added diluent (N2, then CO2 at constant pressure, then He) until quasi-steady burning was no longer observed, using droplets mostly of 3-4 mm and both free and tethered droplets; the original plan was to vary droplet size at each oxygen level until radiative extinction and then lower oxygen until no ignition. Early tests (Mar-Jul 2009) were in cabin air and in 0.21 O2/0.70 CO2/0.09 N2 at 2-3 atm; the high-pressure series was cut short because the fuel system responded poorly to pressure cycling.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| ambient oxygen fraction | 0.12-0.34 (0.12-0.21 at 1 atm in N2; 0.30 and 0.34 at 0.7 and 1 atm) | mole fraction |
| carbon dioxide fraction (suppressant) | 0.05-0.50 at 0.7-1 atm; 0.70 at 2-3 atm | mole fraction |
| helium fraction (suppressant) | 0.05-0.45 | mole fraction |
| ambient pressure | 70-73 kPa (103 tests), 100-103 kPa (161 tests), 206-309 kPa (9 tests); original 526-2320 mmHg | kPa |
| initial droplet diameter | 1.10-4.67 | mm |
| fuel | methanol, n-heptane |  |
| support | free-floating or 80 um SiC fibre (some translated at low speed) |  |

Held constant:

- ambient temperature: room temperature (~298 K)
- gravity: ISS microgravity, typically < 1e-5 g0
- imposed flow: none (quiescent) except brief fibre translation in some tethered tests; residual drift of order 1-2 mm/s

Number of tests: 274

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| droplet diameter history D(t), initial diameter D0 | backlit HiBMs camera, 30 fps, ~32.5 pixel/mm; uncertainty +/-50 um | direct |
| flame diameter (outer edge of OH* chemiluminescence) | LLUV intensified camera, 310 nm filter; uncertainty +/-200 um | direct |
| visible flame diameter, flame colour/soot, disruption, vapour cloud | MDCA colour camera; uncertainty +/-250 um | direct |
| average burning-rate constant K (mm2/s) | linear fit of D^2(t) | derived |
| visible-flame extinction diameter, burn time and test end mode (extinction / disruption / completion) | HiBMs and colour camera | derived |
| flame standoff ratio Df/D | LLUV flame diameter / HiBMs droplet diameter | derived |
| soot volume fraction (heptane) | HiBMs backlit extinction | derived |

## Findings

1. Limiting oxygen index in O2/N2: about 0.12 for methanol and 0.15 for n-heptane droplets. NASA describes the LOI found as significantly lower than in normal gravity and lower than predicted; the 2012 FLEX overview states microgravity flames burned at as much as 2-3 percent less oxygen (the source does not say whether relative or absolute). Consistent with this, the PSI table lists methanol tests that burned 5-11 s and extinguished at 0.12 O2 (8 tests) and heptane tests at 0.13 O2 that burned only 1.0-1.5 s with extinction diameter about equal to the initial diameter (transient burning below the LOI). *(limit, high)*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *For oxygen/nitrogen mixtures, the LOI is 0.12 and 0.15 for methanol and heptane, respectively.*
   - <https://www.nasa.gov/sites/default/files/atoms/files/np-2015-10-034-jsc_combustion_in_reduced_gravity-iss-mini-book-011116-508.pdf>: *identified an LOI that is both significantly lower than in normal gravity and lower than previously predicted and anticipated.*
   - <https://ntrs.nasa.gov/api/citations/20120015928/downloads/20120015928.pdf>: *They burn at lower oxygen levels, as much as 2-3 percent less oxygen, and are harder to detect, harder to extinguish, and are more persistent.*
   - Table `tests`: Methanol, N2 only, ~1 atm, O2 = 0.12: 8 rows, all 'Extinction', burn time 5.45-10.8 s. Heptane, N2, 1 atm, O2 = 0.13: 3 rows, burn time 1.0-1.5 s, d_ext/d0 = 0.98 where measured.
2. Carbon dioxide as suppressant: dispersing CO2 into 1 atm air raised the LOI to about 0.14 for methanol (0.14 O2/0.56 N2/0.30 CO2) and about 0.17 for heptane (0.17 O2/0.63 N2/0.20 CO2), i.e. roughly 30% and 20% CO2 by volume were needed to prevent quasi-steady burning of these fuels. The authors attribute the higher LOI to CO2's larger heat capacity (lower flame temperature) and its radiative participation. The PSI table shows methanol still burning 3.4-5.9 s at 0.14 O2 with 0.36 CO2, and heptane at 0.17 O2/0.20 CO2 extinguishing after 1.6-1.9 s with d_ext/d0 = 0.97. *(limit, high)*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *The LOI increases to approximately 0.14 (0.14 O2/0.56 N2/0.30 CO2) and 0.17 (0.17 O2/0.63 N2/0.20 CO2) for methanol and heptane, respectively, for ambient environments that simulated dispersing an inert-gas suppressant (carbon dioxide) into a nominally air (1.0 atm) ambient environment.*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *The higher LOI in the CO2-diluted tests results from increased specific heat of carbon dioxide*
   - Table `tests`: Methanol, CO2-diluted, ~1 atm, O2 0.14 / CO2 0.36: 2 rows, Extinction, burn time 3.4 and 5.9 s. Heptane, 1 atm, O2 0.17 / CO2 0.20: 2 rows, Extinction, burn 1.6 and 1.9 s, median d_ext/d0 0.97.
3. Helium as suppressant: dispersing helium into air at 1 atm gave an LOI of about 0.14 for methanol and 0.15 for heptane, i.e. helium was a weaker suppressant than CO2 for heptane and comparable for methanol. In the PSI table the lowest-oxygen helium test (methanol, 0.13 O2/0.40 He) burned only 0.3 s, extinguishing at 3.54 mm from 3.56 mm initial diameter. A related FLEX analysis comparing helium and xenon (same molar thermodynamics, different transport) concluded that transport properties of the ambient gas matter for LOI. *(limit, high)*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *The LOI is approximately 0.14 and 0.15 for methanol and heptane, respectively, when helium is dispersed into air at 1 atm.*
   - <https://doi.org/10.1080/00102202.2015.1072176>: *The results indicate that ambient gas transport properties play an important role in determining limiting oxygen indices as well as burning rates*
   - Table `tests`: Row H08M101 (PSI test 248): methanol, 763.5 mmHg, O2 0.13, He 0.40, d0 3.56 mm, d_ext 3.54 mm, burn time 0.3 s, Extinction.
4. Extinction regimes: as ambient oxygen was reduced, the diffusive-extinction droplet diameter increased and the radiative-extinction diameter decreased; quasi-steady burning existed only between the two. Radiative extinction was frequent for heptane and often preceded by flame oscillations at about 1 Hz; diffusive extinction of heptane was hard to observe because droplets disrupted first. Methanol seldom extinguished radiatively in the tested sizes but extinguished diffusively at large diameters because of absorbed water; below about 14% O2 radiative extinction took over. In the PSI table, 24 of 56 heptane extinctions with a measured extinction diameter had d_ext/d0 > 0.9 (extinction soon after ignition, radiative), against 14 of 103 for methanol. *(trend, high)*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *For both fuels, the flames exhibited pre-extinction flame oscillations during radiative extinction with a frequency of approximately 1 Hz.*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *Diffusive extinction was difficult to observe for heptane droplets.*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *In fact, we seldom observed radiative extinction for methanol*
   - <https://ntrs.nasa.gov/api/citations/20120015928/downloads/20120015928.pdf>: *For oxygen concentrations approximately below 14 percent, radiative extinction was found to occur rather than extinction caused by water absorption.*
   - Table `tests`: Rows with Test end = Extinction and d_ext > 0: heptane 56 (24 with d_ext/d0 > 0.9), methanol 103 (14 with d_ext/d0 > 0.9).
5. Discovery of droplet cool flames: for large n-heptane droplets, after the visible hot flame extinguished radiatively the droplet kept vaporising at a nearly linear D^2 rate for many seconds, then stopped abruptly at a finite diameter, coincident with a large vapour cloud. The team attributed this to quasi-steady, soot-free, low-temperature (~700 K in simulations) cool-flame chemistry that was invisible to the cameras. It was observed repeatably in air and in N2-, CO2- and He-diluted atmospheres, only after radiative hot-flame extinction, and was unexpected; NASA states it was thought impossible by many in the community. *(result, high)*
   - PSI record field `researchImpacts`
   - <https://doi.org/10.1007/s12217-014-9372-2>: *After the visible hot flame radiatively extinguished around a large heptane droplet, the droplet continued to burn with a cool flame. This phenomena was observed repeatably over a wide range of ambient conditions.*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *A defining feature is that it only occurs after radiative extinction of the hot flame.*
   - <https://www.nasa.gov/sites/default/files/atoms/files/np-2015-10-034-jsc_combustion_in_reduced_gravity-iss-mini-book-011116-508.pdf>: *This cool flame supported droplet combustion was not only unexpected, but also thought to be impossible by many in the peer community*
   - <https://ntrs.nasa.gov/api/citations/20120015928/downloads/20120015928.pdf>: *the science team has concluded that the event is a unique observation of second-stage vaporization sustained by a low-temperature, soot-free, chemical reaction*
6. Cool flames as a fire-safety hazard: the investigators warned that safety procedures based only on hot flames may be inadequate, because cool-flame burning persists invisibly after hot-flame extinction, produces partially oxidised fuel (a vapour cloud) and might re-ignite into a hot flame. Theory by the FLEX PI predicts a separate LOI for cool-flame-supported heptane combustion of order 0.10 O2 in O2/N2, below the hot-flame LOI. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20120015928/downloads/20120015928.pdf>: *Under certain conditions, it may be possible that a cool flame could reignite in the hot mode, essentially restarting the fire that the crew had thought to be extinguished.*
   - <https://ntrs.nasa.gov/api/citations/20210022617/downloads/JASMAC-33%20FLEX%20w%20video.pdf>: *These cool flames produce partially oxidized fuel and potentially re-ignite to hot flames posing fire safety concerns in spacecraft environments*
   - <https://doi.org/10.1080/13647830.2019.1588380>: *for heptane burning in oxygen-nitrogen mixtures at normal room temperature, a corresponding oxygen mole fraction on the order of 0.10 in the ambient atmosphere, below which cool-flame-supported combustion cannot occur.*
7. Burning-rate constants: across 258 tests K ranged 0.05-1.06 mm2/s (median 0.50). For methanol in O2/N2 at 1 atm the median K rose with oxygen from about 0.35 mm2/s at 0.12-0.14 O2 to 0.52 at 0.21 and 0.68 at 0.30. At 0.21 O2/0.49 N2 the remaining 0.30 as N2, CO2 or He gave methanol K of 0.52, 0.45 and 0.70 mm2/s respectively: helium's high conductivity raises K, CO2 lowers it. The classical quasi-steady B-number prediction correlated measured K reasonably well, with small methanol droplets burning faster than predicted. *(trend, high)*
   - Table `tests`: 'Burning rate; mm' (K, mm2/s): 258 numeric values, median 0.50. Methanol, N2 only, ~1 atm: median K 0.35 (O2 0.12, n=7), 0.36 (0.13), 0.345 (0.14), 0.39 (0.15), 0.425 (0.18), 0.515 (0.21, n=12), 0.68 (0.30, n=4).
   - <https://doi.org/10.1007/s12217-014-9372-2>: *The values of ¯k for the nitrogen, carbon dioxide and helium diluted tests was 0.52, 0.45 and 0.70 mm2/s, respectively.*
   - <https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *substituting carbon dioxide with helium leads to a higher burning rate due to the increased thermal conductivity of He compared to CO2*
8. Methanol diffusive extinction is set by water absorption: product water condenses into the droplet until about 30% of its mass is water, after which water evaporates outward and quenches the flame; hence the extinction diameter grows roughly linearly with initial diameter, nearly independent of diluent type. An a-priori activation-energy-asymptotics model reproduced the trend but under-predicted extinction diameters in air unless an effective (water-diluted) flame temperature near 1700 K was used. The CO2-dilution data also showed a quasi-steady flame standoff ratio of about 5 for methanol. *(result, high)*
   - <https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *At smaller droplet sizes, the data fall approximately along a straight line, irrespective of the diluent concentrations.*
   - <https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *the CP values were increased by 60% so that the adiabatic flame temperature was around 1700 K, and the resulting prediction of the AEA theory then lies much closer to the experimental data*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *This ratio is seen in Fig. 6 to be about 5 in all three atmospheres.*
9. Outcome statistics in the PSI table: of 274 tests, 186 ended in flame extinction at a finite droplet size, 61 in droplet disruption and 27 in burning to completion. In the oxygen-enriched N2 atmospheres at 0.7 atm (0.30 and 0.34 O2, 17 tests) no droplet extinguished: 15 disrupted and 2 burned to completion, which is why the team moved the matrix to lower oxygen. Burn times reached 39.2 s (methanol, 4.35 mm, 0.20 O2/0.05 CO2, 1 atm), far beyond drop-tower durations. *(result, high)*
   - Table `tests`: Counts of 'Test end'; subset O2 >= 0.30 with N2 diluent at 70-73 kPa; maximum 'Burn time; s' (row C01M301).
   - <https://ntrs.nasa.gov/api/citations/20150023456/downloads/20150023456.pdf>: *noticed a propensity for the droplets to burn disruptively and not exhibit flame extinction (at a finite-sized droplet diameter).*
10. Heptane is much more sensitive to dilution than methanol near the limit: at 0.7 atm with CO2, heptane burn time fell from about 10 s (0.24 O2/0.20 CO2) to 0.55-0.6 s (0.17 O2/0.45 CO2) with extinction at essentially the initial diameter, whereas methanol at 0.15 O2/0.50 CO2 still burned 1.3-3.4 s. Heptane extinction diameter ratios d_ext/d0 at 0.7 atm CO2 had medians above 0.96 at each O2 level <= 0.21 (one test at 0.18 O2 gave 0.954), i.e. early radiative extinction dominated across this range. *(trend, medium)*
   - Table `tests`: Heptane, CO2, 70-72 kPa: median burn time by O2 0.17/0.18/0.20/0.21/0.23/0.24 = 0.58/1.37/2.45/3.7/7.0/10.1 s; median d_ext/d0 0.998/0.965/0.974/0.965 at O2 0.17-0.21. Methanol, O2 0.15, CO2 0.50: burn time 1.3-3.4 s (4 rows).
11. Data quality: needle conformal coating contaminated the fuel in the 2009-2011 tests; the team judged burning rates, flame sizes and radiative extinction diameters minimally affected, but methanol disruptive extinction probably caused by the contaminant, and heptane disruption possibly. Droplets often drifted out of the 30 mm backlit field of view due to residual deployment velocity and g-jitter, truncating diameter histories; some extinction diameters were extrapolated. *(method, high)*
   - <https://ntrs.nasa.gov/api/citations/20150023456/downloads/20150023456.pdf>: *(4) Disruptive extinction of methanol is probably due to the presence of the contaminant.*
   - <https://ntrs.nasa.gov/api/citations/20150023456/downloads/20150023456.pdf>: *(7) Radiative extinction droplet diameters (larger diameters) were not influenced by the presence of the contaminant.*
   - <https://ntrs.nasa.gov/api/citations/20150023456/downloads/20150023456.pdf>: *we did estimate (extrapolate the burning history) to determine the extinction droplet diameter if there was sufficient burning history*
12. Numerical modelling of FLEX conditions (Farouk and Dryer) found distinct diffusive and radiative extinction regimes for methanol, with the transition strongly influenced by CO2 concentration, and helium dilution favouring diffusive extinction with higher burning rate; detailed-chemistry simulations including low-temperature chemistry reproduced the two-stage heptane burning. *(result, medium)*
   - <https://doi.org/10.2514/6.2012-1252>: *The transition from diffusive to radiative extinction is strongly influenced by ambient carbon dioxide concentration. Results for helium as the diluent show an increased burning rate and a dominance of extinction due to diffusive heat loss.*
   - <https://doi.org/10.1007/s12217-014-9372-2>: *The predictions from the model for the droplet history capture the two stage combustion behavior*
13. Methanol extinction mode versus oxygen at 1 atm (O2/N2/CO2, D0 about 2-4 mm): at 18% O2 or more every droplet extinguished diffusively, at 14% O2 or less every droplet extinguished radiatively, and at 15% and 16% O2 a critical initial diameter separated the two modes, larger droplets switching to radiative extinction (the switch happening at a larger D0 at 16% than at 15%). Tests with more CO2 lay closer to the radiative (no-burn) line, which the authors attribute to CO2's higher infrared emissivity; CO2 affected diffusive extinction about as N2 does. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf>: *In 18 % or more O2 all droplets exhibit diffusive extinction, and in 14 % or less O2 all exhibit radiative extinction, there being critical initial diameters separating the two limiting behaviors at the two intermediate O2 concentrations.*
   - <https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf>: *had more CO2 in the atmosphere, suggesting that this diluent promotes radiative extinction, as expected from its much greater infrared emissivity.*
14. Interpreting methanol extinction with the Zhang-Card-Williams water-absorption theory, diffusive extinction at 1 atm occurs when the infinite-rate (ideal) flame temperature falls to about 1800 K in 21% O2 (calculated lines for 1800 K and 1750 K bracket the data) and below 1650 K at 18% O2. Radiative extinctions occurred so close to the initial diameter that burning was transient and depended on ignition energy; the authors suggest such atmospheres are effectively outside the LOI and that water absorption can be neglected for them. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf>: *It may thus be concluded that diffusive extinction occurs when the infinite-rate ideal flame temperature decreases to a value not far from 1800 K in atmospheres having O2 contents of 21 %. That value decreases with dilution and is less than 1650 K at 18%.*
   - <https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf>: *In a sense, then, one might wish to consider these atmospheric conditions to lie outside the LOI.*
15. Methanol flame-standoff ratio (quasi-steady average of flame/droplet diameter) rises as ambient oxygen falls, at both 0.7 and 1 atm. A simplified quasi-steady model that includes water absorption predicts it reasonably, but measured ratios in O2/N2/He mixtures are consistently above the prediction while O2/N2/CO2 data agree better; the authors leave the cause open. *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20120016855/downloads/20120016855.pdf>: *As one would expect, df/d increases with decreasing ambient oxygen mole fraction since the flame needs to move father away to meet the stoichiometric requirement.*
   - <https://ntrs.nasa.gov/api/citations/20130014061/downloads/20130014061.pdf>: *The measured FSRs for O2 − N2 − He mixtures are consistently higher than the predicted values compared to the O2 − N2 − CO2 mixture data points.*
16. The first nine rows of the PSI table (identifiers 20CAL08 to 30CAL07, 5 March to 10 April 2009, 6 methanol and 3 heptane) are engineering tests in cabin air (0.21 O2/0.79 N2 at about 760 mmHg); the planned science matrix starts with row 10 on 22 May 2009. Analyses of suppressant effects should treat these rows as air baselines from the commissioning period. *(method, high)*
   - Table `tests`: PSI-69 rows 1-9: FLEX identifiers containing 'CAL', dates 2009-03-05 to 2009-04-10, O 0.21 / N 0.79, pressure 757.7-764.2 mmHg; row 10 (256F002) dated 2009-05-22.
   - <https://ntrs.nasa.gov/api/citations/20120015928/downloads/20120015928.pdf>: *The first nine “engineering” tests used cabin air rather than specified diluent gasses.*

## Fire-safety relevance

FLEX is the main ISS measurement of inert-gas suppression of liquid-fuel fires in quiescent microgravity. Its message is that weightless flames are weaker but more persistent: they survive at 2-3 points lower oxygen than on Earth, so suppressant concentrations derived from terrestrial standards give less margin in orbit, and CO2 needed roughly 30% (methanol) or 20% (heptane) dilution of 1 atm air to block quasi-steady burning, with helium less effective for heptane. Radiation, not convection, controls extinction of large quiescent flames. The cool-flame discovery adds a hazard: an alkane fire that appears extinguished can keep reacting invisibly, release partially oxidised vapour and possibly re-ignite. Transferability is limited: these are single, mm-size droplets of two pure fuels with a fixed, well-mixed diluent, not spreading fires on solids, sprays, or suppressant discharged into a ventilated cabin.

### Habitat conditions

Most tests were at 1 atm (100-103 kPa, the ISS/Earth sea-level reference) or about 0.7 atm (70-73 kPa). The 0.7 atm / 0.30 O2 condition was chosen by the team to represent the ISS EVA pre-breathe atmosphere and the maximum proposed exploration-vehicle oxygen; it essentially coincides with the reference Moon-habitat atmosphere (30% O2 at 70.3 kPa), and 0.34 O2 was also tested at 0.7 atm. Under these enriched conditions with nitrogen only, no droplet extinguished at a finite size (15 of 17 disrupted, 2 burned out), and CO2 dilution at 0.7 atm began from 0.25 O2. The 100% O2 spacesuit atmosphere (29.6 kPa) and pressures below 70 kPa were not tested in FLEX.

### Earth benefits

Benchmark data for chemical-kinetic and transport models of liquid fuels, especially low-temperature (cool-flame, negative-temperature-coefficient) chemistry relevant to engine knock, HCCI and efficient low-emission engines; suppression data relevant to confined spaces such as submarines and aircraft.

## Limitations

- Only two pure fuels (methanol, n-heptane) as isolated mm-size droplets in quiescent, well-mixed atmospheres; results are droplet flammability limits, not material flammability or flame-spread limits, and do not represent sprays, pools or solids.
- Atmospheres were reused between tests, so actual compositions include accumulated CO2, H2O and fuel vapour and were computed after the fact; the table gives 'initial' compositions, and suppressant concentration and oxygen vary together in the dilution series, so CO2/He effect and O2 effect are partly confounded.
- Fuel contamination from needle coating in all 2009-2011 tests; disruptive endings (61 tests) may be partly artefacts.
- LOIs were bracketed with few droplets per condition and limited fuel; methanol radiative extinction at higher O2 was deliberately not pursued because fuel volume scales with D0 cubed. The radiometers gave no quantitative data in 2009-2011 and the LLUV window was smudged, adding uncertainty to flame sizes.
- The PSI table has no rows for failed ignitions, so the LOI cannot be re-derived from PSI data alone, and it omits the fibre flag and notes that distinguish free from tethered droplets.

## Data in PSI

PSI holds a single experimental table (24.8 kB CSV, 274 rows, one per test) with test number, CIR identifier, date and GMT, fuel, pressure (mmHg), initial O2/N2/CO2/He mole fractions, initial droplet diameter, visible-flame extinction diameter, burning-rate constant, burn time and how the test ended. It reproduces Table IX of NASA/TP-2015-216046 (which also gives droplet and flame histories as plots), but drops the fibre/no-fibre flag and the per-test notes, and its own test numbers run 1-274 consecutively whereas the report numbers FLEX-001 to FLEX-280 with gaps. No images, droplet/flame time histories, radiometer data or documents are in PSI for this accession, although the record's totalFileSize (~924 GB) suggests the raw image data exist elsewhere. Outcome statistics, burning-rate constants and extinction diameters can be analysed now; flame sizes and LOI cannot be re-derived (no no-ignition tests are listed).

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | per-test summary table, 274 rows, 15 columns | .csv | 1 | 25 kB | yes |

Rows in the unified `tests` table: 274

## Related investigations

- [PSI-68](PSI-68-flex-2.md): follow-on
- [PSI-39](PSI-39-cfi.md): follow-on
- [PSI-159](PSI-159-acme-cfi-g.md): follow-on
- [PSI-117](PSI-117.md): ground re-analysis
- [PSI-142](PSI-142.md): ground re-analysis

## Open questions

- Fit diffusive and radiative extinction-diameter branches versus O2 for each fuel/diluent/pressure group in the PSI table and locate their crossing, to give an independent LOI estimate with uncertainty.
- Compare measured K in the table with the B-number prediction test by test, separating N2, CO2 and He groups, to quantify radiative and water-absorption departures.
- Re-express suppressant efficacy as oxygen partial pressure or adiabatic flame temperature at the limit, to compare CO2 and He on a heat-capacity basis.
- Identify which heptane tests with early radiative extinction show the long burn times or d_ext values implying cool-flame burning, using Appendix B histories of NASA/TP-2015-216046.
- Quantify the effect of 0.7 vs 1 atm on extinction at matched O2 and diluent fractions.

## Dashboard ideas

- **extinction boundary map** (`x_o2`, `diluent`, `x_diluent`, `d0_mm`, `d_ext_mm`, `extinction_mode`): Shows diffusive vs radiative branches and the LOI for methanol and heptane in N2, CO2 and He.
- **suppressant efficacy comparison** (`fuel`, `diluent`, `pressure_kpa`, `loi_x_o2`): Headline fire-safety numbers: LOI 0.12/0.15 in N2, 0.14/0.17 with CO2, 0.14/0.15 with He at 1 atm.
- **d-squared law explorer** (`d0_mm`, `K_mm2_s`, `burn_time_s`, `d_ext_mm`): Lets users check t_b = (d0^2 - d_ext^2)/K and see K rise with O2 and with helium.
- **outcome by atmosphere** (`x_o2`, `pressure_kpa`, `diluent`, `test_end`): Shows that enriched (0.30-0.34 O2, 0.7 atm) atmospheres never produced extinction.

## Gaps and data-quality notes

- PSI holds only the experimental table for PSI-69 (no documents, images or time histories); all interpretation comes from the PSI record text and external sources: NASA/TP-2015-216046 (NTRS 20150023456, source of the table), Dietrich et al. 2014 Microgravity Sci. Technol. (open access), Nayagam et al. 2013 US National Combustion Meeting paper (NTRS 20130014061), the 2012 FLEX overview (NTRS 20120015928), the MDCA-FLEX fact sheet (NTRS 20090014812), a 2021 JASMAC presentation (NTRS 20210022617), NTRS abstracts 20110020695 and 20120016855, and NASA's 2015 combustion researcher's guide.
- Column units verified: 'Burning rate; mm' is the burning-rate constant K in mm2/s (Table IX of the NASA report labels it 'Burning rate, mm2/s'; our d-squared consistency check gives burn time / ((d0^2-d_ext^2)/K) = 1.05 median). Subscripts were lost in the PSI headers: 'O', 'N', 'CO' mean O2, N2, CO2.
- Table oddities: test C11M201 (PSI row 114) has ambient pressure 0 mmHg (also 0 in the NASA report); its sibling tests were at ~535 mmHg and its GMT 19:14:22 equals that of heptane test C11H201 on the same date, so date/time/pressure look mis-entered. Identifier 193F001 appears twice (rows 70 and 73) with identical date and GMT but different d0 (4.67/4.64), K (0.41/0.56) and burn time, as in the report. Six rows (e.g. 193R002, 203F001) have compositions summing to 0.98. Eight rows give extinction diameter 0 (including one 'Completion'), one row (C13H102) has d_ext > d0, and 192F001 is 'Completion' with an extinction diameter of 1.56 mm. Burn times '~6' and '~9' are non-numeric. Row 24 (196F003) contains byte 0x96 (cp1252 en dash used as 'missing'), and the file is cp1252 encoded. Dates mix 2- and 4-digit years.
- PSI test numbers run 1-274 consecutively and do not match the report's FLEX-001 to FLEX-280 numbering after test ~155 (e.g. C03H401 is PSI 156 but FLEX-157); the report also lists 284 tests in its summary versus 274 rows.
- Report Table III lists tests 019-024 at 0.400 O2 / 0.600 N2 while Table IX (and PSI) give 0.34/0.66 for the same tests; unresolved.
- Dietrich et al. 2014 contain apparent typos: helium-diluted LOIs are given with 'N2/CO2' compositions (e.g. '0.14/0.56/0.35 O2/N2/CO2'). We report only the LOI values.
- PSI dates (2007-08-01 to 2016-07-31) look like grant dates; ISS testing in the table runs 2009-03-05 to 2011-12-08 and further FLEX tests with xenon were planned for late 2012. Record totalFileSize (~924 GB) does not match the single 25 kB file in PSI.
- Abstracts of the key Elsevier papers (Nayagam et al. 2012 'Can cool flames support quasi-steady alkane droplet burning?', Hicks et al. 2011 tethered methanol/CO2, Nayagam 2013 AEA, Farouk and Dryer cool-flame 2014) were not available via OpenAlex or Semantic Scholar; their content is cited only through the NASA summaries. Most other publication DOIs in the record are ground-based precursor or modelling studies and were not read in full.
- The xenon tests mentioned in NASA documents and Shaw and Vang (2015) are not in the PSI table (it ends Dec 2011); SF6 named in the PSI objective does not appear in any test.
- Investigator affiliations in PSI (Dryer at South Carolina, Choi at Missouri) differ from those in the 2015 NASA report (Princeton, Connecticut). One contact email in the PSI record has a malformed domain; contact details were not copied.
- No text addressed to an AI or unrelated instructions was found in the PSI files.
- Publication review (Nov 2026; per-paper notes in data/publications/PSI-69.json): of the 51 listed publications, 8 were read in full (NTRS preprints/reports, open-access journals), 18 by abstract only and 25 not at all (closed Elsevier/Springer/Taylor & Francis papers with no open copy or indexed abstract, including Nayagam et al. 2012 "Can cool flames support quasi-steady alkane droplet burning?" and Nayagam 2013 AEA). About 20 are ground-based or modelling studies outside the ISS data. The open-access Dietrich et al. 2014 PDF was blocked by a bot check this time; the record's earlier quotes from it were not re-verified.
- Run numbers in papers do not always equal PSI row numbers: Nayagam et al. 2013 (NTRS 20130014061) 'Run #204' (methanol, 2.75 mm, air, De 1.10 mm) is PSI row 203 (N01M201), and 'Run #263' (2.67 mm, 21% O2/30% He at 0.7 atm, De 1.42 mm) is PSI row 257 (H12M201); Run #110 equals PSI row 110. That paper also writes air as '20% O2 and 79% N2' where the table has 0.21/0.79.
- Hicks et al. 2012 ASGSR slides (NTRS 20130010979) give FLEX-145 as '20% O2 / 75% CO2 / 5% N2', D0 3.38 mm, Dext 1.66 mm, K 0.44 on one slide but 'O2 20% / N2 75% / CO2 5%', D0 3.3 mm on the next; PSI row 145 (C01M201) has 0.20 O2/0.75 N2/0.05 CO2, 3.33 mm, 1.61 mm, 0.45 mm2/s. The first slide appears to swap N2 and CO2.
- Nayagam et al. 2011 (NTRS 20120016855) describe a 1 atm methanol extinction test 'at 21% O2 had 70% CO2 and 9% N2' (Fig. 3, captioned 1 atm), but every 0.21/0.09/0.70 row in the PSI table (rows 10-18) is at 1546-2320 mmHg (2.0-3.05 atm); the only methanol one with an extinction diameter is row 16 (256F009, 2072 mmHg). The same paper counts 104 methanol tests by October 2011, against 142 methanol rows dated before then in the table (cut-off not stated).
- The conclusions of NASA/TP-2015-216046 give initial diameters 'between 2 and 5 mm' and atmospheres of O2 with N2, CO2 and mixtures, but its Table IX (the PSI table) has d0 down to 1.10 mm (26 tests below 2 mm) and 50 helium-diluted tests; its Appendix A says it covers March 2009 to December 2010 although the table runs to December 2011.
