# PSI-20: ACME BRE (Advanced Combustion via Microgravity Experiments - Burning Rate Emulator)

A flat gas burner on the Space Station imitated small burning patches of plastics and liquids in still air, showing that such flames can burn steadily for minutes without any air flow when oxygen is raised to about 26.5% or more, but go out within tens of seconds at 21%.

Investigators: James G. Quintiere (University of Maryland) - Principal Investigator; Peter B. Sunderland (University of Maryland) - listed in PSI as Project Scientist; described as Co-Investigator by UMD; John L. de Ris - Co-Investigator; Dennis P. Stocker (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Setting | ISS · CIR · ACME |
| Platform | International Space Station (ISS) |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 2010-01-01 to 2025-02-08 |
| Fuels and samples | ethylene; ethylene diluted with nitrogen; methane; emulated materials |
| Varied | ambient oxygen fraction (O2 diluted with N2): 0.21-0.40 (table lists approximate values 21, 25, 26.5, 34, 40%) mole (volume) fraction<br>ambient pressure: 56-100 kPa (0.56-1 bar; Wright gives 0.57-1 bar) kPa<br>burner diameter: 25, 50 mm<br>fuel type: ethylene, methane<br>fuel mole fraction in fuel/N2 mixture (sets heat of combustion and smoke point): 0.15-1 (round 1 design); bottles of 100% and 50% C2H4 mole fraction<br>fuel mixture mass flux through burner: 1-12 (round 1 design) g/(m2 s) |
| Number of tests | 194 |
| Fire-safety pillars | prevention, fundamental |

## Question

Can a small condensed-fuel (solid or liquid) fire burn steadily in quiescent microgravity, where there is no buoyant or forced flow to bring oxygen in, and if so for which combinations of material properties and cabin atmospheres? Testing dozens of real materials in orbit is too expensive, so BRE emulates them: a porous gas burner fed with ethylene or methane (optionally diluted with nitrogen) is set to match a material's heat of combustion, heat of gasification, surface re-radiation and smoke point. The hypothesis is that a quasi-steady burning regime exists as a function of these properties, and that if so the ground-based cone calorimeter test (NASA-STD-6001 Test 2), which measures such properties, could be used to build microgravity flammability maps for real materials. Objectives also named three NASA-considered cabin atmospheres (21% O2 at 14.7 psia, 26.5% at 10.2 psia, 34% at 8.2 psia), O2/CO2 ambients (desired) and extinction limits.

## Summary

ACME BRE (Burning Rate Emulator) used flat porous gas burners, 25 and 50 mm across, in the Combustion Integrated Rack on the International Space Station to imitate small burning patches of solids and liquids in still air. Ethylene, nitrogen-diluted ethylene or methane was fed at a fixed mass flux (about 1-12 g/(m2 s)) into nitrogen-oxygen atmospheres of 21-40% O2 at 56-100 kPa; embedded heat-flux gauges, radiometers and cameras gave the effective heat of gasification of each flame, its radiative loss and its size. Over 18 test days in 2019-2021, 194 flames were ignited. All 25 mm flames at 21% O2 self-extinguished within 40 s, whereas at 26.5, 34 and 40% O2 many burned steadily for 2-5 minutes until shut down. Larger, higher-flow and methane flames extinguished sooner; radiative heat loss drove the oscillation and extinction. Models built on these data suggest common plastics could burn steadily at about 1-3 g/(m2 s) in microgravity, and that low-pressure, oxygen-enriched cabin atmospheres widen the burning range. Stopping ventilation may therefore not quickly put out a small fire at elevated oxygen.

## Physics

On Earth a burning surface is fed by a buoyant plume that brings in fresh air and carries away hot products. In quiescent microgravity there is no buoyancy, so oxygen reaches the flame only by diffusion; the flame becomes a slowly growing, nominally hemispherical blue diffusion flame over the surface. For a steadily burning condensed fuel the mass burning rate equals the net heat flux to the surface divided by the heat of gasification L (energy needed to turn unit mass of solid or liquid into vapour), so L = q''_net / m''. BRE inverts this: the fuel mass flux m'' is imposed through the porous burner, the heat flux to the surface is measured, and the 'effective' L of the emulated material is derived. Stagnant-layer (Spalding B-number) theory gives a purely diffusive burning rate proportional to ln(1+B). Because microgravity flames are large, slow and long-lived, radiative loss from soot and from CO2/H2O becomes a large fraction of the heat release; as the flame grows the flame temperature drops until it oscillates and undergoes radiative extinction. Higher oxygen raises flame temperature; dilution with nitrogen lowers heat of combustion and makes flames smaller and less radiative. A drop-tower test (5 s) is too short for these flames to reach steady state, hence the need for ISS-duration tests.

$$
L = \frac{\dot q''_{net}}{\dot m''}, \qquad \dot q''_{net} = \dot q''_{f,c} + \dot q''_{f,r} - \dot q''_{s,r} + \dot q''_{e,r}
$$

Steady energy balance at a burning surface, used by BRE to define the emulated material. $L$: heat of gasification (kJ/g), energy to turn unit mass of condensed fuel into vapour at the surface; $\dot q''_{net}$: net heat flux into the surface (kW/m2), measured by the burner's heat-flux gauges and slug calorimeter; $\dot m''$: fuel mass flux (g/(m2 s)), imposed through the porous burner. Components: flame convective flux $\dot q''_{f,c}$, flame radiative flux $\dot q''_{f,r}$, surface re-radiation $\dot q''_{s,r}$ and external radiation $\dot q''_{e,r}$ (zero in the ISS tests). Exact for a simply vaporising fuel at steady state; only approximate for real pyrolysis (charring, in-depth heating).

<https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *burning of a condensed fuel, the heat of gasification L is given by the ratio of the net heat flux and the burning rate.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *the heat of gasification, L, (a material property) is found by Eq. (4.8)*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The external radiative heat flux is not present in the experiments but could be included in the theory to follow.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *This is exact for vaporizing solids and approximant under real pyrolysis conditions.*

$$
B = \frac{Y_{O_2,\infty}(1 - X_r)\,\Delta h_c / S - c_p (T_s - T_\infty)}{L_e}, \qquad L_e = L - \frac{\dot q''_{f,r} + \dot q''_{e,r} - \dot q''_{s,r}}{\dot m''}
$$

Spalding B number (mass transfer number): ratio of the energy the flame can deliver per unit mass of fuel to the energy needed to gasify it. $Y_{O_2,\infty}$: ambient O2 mass fraction; $\Delta h_c$: heat of combustion of the fuel/diluent stream (kJ/g; 15-47.2 kJ/g in BRE); $S$: mass of O2 consumed per unit mass of fuel stream; $\Delta h_c/S$ is the heat released per unit mass of O2 (taken as 13.76 kJ/g for ethylene); $c_p$: gas specific heat (kJ/(g K), consistent with $L$ and $\Delta h_c/S$); $T_s$, $T_\infty$: surface and ambient temperatures (K); $L$: heat of gasification (kJ/g); $L_e$: effective heat of gasification (kJ/g), $L$ less the net radiative fluxes per unit mass flux (dissertation Eq. 4.6 and 4.7), so that $\dot m'' L_e$ is the convective flux alone. The Dehghani analysis uses this effective B, in which the heat of combustion is reduced by the flame radiative loss fraction $X_r$ (transparent-flame assumption) and the denominator is $L_e$; $X_r$ and $L_e$ belong together. With $X_r = 0$ and no radiative fluxes this is the classical textbook B number. Higher O2 raises B and so the burning rate.

Textbook background
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *is the effective B number*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *the formulas will be used throughout the paper as modified to include the heat of combustion reduced by a flame radiation loss fraction, Xr, the ratio of radiant energy lost by the flame to its combustion energy.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *taken in this analysis for the experimental fuel, ethylene as 13.76 kJ/g*

$$
\dot m'' = \frac{8k}{\pi c_p D}\,\ln(1 + B) \quad\Longleftrightarrow\quad \lambda \equiv \frac{\pi c_p R\,\dot m''}{4k} = \ln(1 + B)
$$

Steady, purely diffusive burning rate of a flat circular fuel surface in quiescent surroundings (stagnant-layer and oblate-ellipsoid models give the same form); the relation BRE is built on. $\dot m''$: fuel mass flux (kg/(m2 s)); $k$: gas thermal conductivity (W/(m K)); $c_p$: gas specific heat (J/(kg K)); $D = 2R$: burner diameter (m); $\lambda$: dimensionless mass flux (burning eigenvalue); $B$: Spalding B number. Unity Lewis number ($\rho\mathcal{D} = k/c_p$), constant properties, laminar, no buoyancy. Note the rate scales as $1/D$, so small surfaces burn faster per unit area. In BRE $\dot m''$ is prescribed, so the relation is inverted to find the $B$ (and hence $L$) a flame emulates. Neglecting radiation, it over-predicted the measured drop-tower burning rates, and the 25 and 50 mm data followed two distinct curves.

<https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *According to both models, the burning rate of the fuel is identically expressed as:*
<https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *The steady state theory assumes negligible radiation which might be the reason for over-prediction.*
<https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *The dimensionless burning rate in Figure 4 follows two distinct curves corresponding to the two burner diameters.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *the corresponding burning eigenvalue is equivalently found in terms of the solid fuel properties and B number as given by Eq. (4.5)*
Textbook background

$$
\frac{x_f}{R} = \tan\!\left[\frac{\pi}{2}\left(1 + \frac{\ln\!\left(\frac{\alpha}{\alpha+1}\right)}{\lambda}\right)\right], \qquad \alpha = \frac{S}{Y_{O_2,\infty}}
$$

Steady flame height on the burner axis from the oblate-ellipsoid diffusion solution (Markan et al., used by Dehghani). $x_f$: flame stand-off height on axis (m); $R$: burner radius (m); $\lambda$: dimensionless mass flux defined above; $\alpha$: stoichiometric O2-to-fuel-stream mass ratio divided by ambient O2 mass fraction. Height depends only on diffusion and stoichiometry, not radiation; it grows with fuel flux and as O2 falls. Properties taken for nitrogen at 1400 K; the investigators found good agreement with measured steady heights for 0.265-0.40 O2 mole fraction and heats of combustion of 23.6 and 47.2 kJ/g. Reconstructed from a garbled PDF text layer (Eq. 4.18) and checked for consistency with the mixture-fraction solution.

<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The flame height along the axis normal to the burner at r = 0 is given by Eq. (4.18)*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The flame position has no dependence on flame radiation because it is governed solely by diffusive effects.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The properties were evaluated at 1400 K for nitrogen based on optimizing the results.*

$$
c_p (T_f - T_\infty) = \frac{c_p (T_s - T_\infty) + Y_{F,s}(1 - X_r)\,\Delta h_c}{\alpha Y_{F,s} + 1}, \quad Y_{F,s} = 1 - \frac{1+\alpha}{\alpha} e^{-\lambda}, \quad \text{steady burning if } T_f \gtrsim 1100\ \mathrm{K}
$$

Flame temperature of the steady flame with radiative loss, and the extinction criterion the investigators used. $T_f$: flame temperature (K); $Y_{F,s}$: fuel mass fraction at the surface; $X_r$: flame radiative loss fraction; other symbols as above. A flame is predicted to burn steadily only if $T_f$ exceeds a critical value of about 1100 K, the value commonly used for low-strain (about 1 s$^{-1}$) microgravity flames, versus about 1600 K for buoyant 1-g flames (strain about 10 s$^{-1}$). All steady ISS data computed above 1100 K; a 1100-1200 K band separated steady from self-extinguished flames. The criterion is a surrogate for a Damkohler-number limit.

<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The theoretical flame temperature can be calculated by Eq. (4.15)*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *Steady burning is theoretically decided by ensuring the flame temperature is above a critical value of 1100 K.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *where 1600 K corresponds to about a strain rate of 10 s-1, and 1100 K to a strain rate of 1 s-1.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The flame temperature becomes a surrogate for the Damkohler number*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *it is clear from Figure 4.7 that all the steady results theoretically correspond to flame temperatures above 1100 K.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *A critical flame temperature range of 1100 K to 1200 K was found to distinguish*

$$
X_r = 0.0633\,\ln\Omega + 0.452
$$

Empirical best fit of the measured flame radiative loss fraction $X_r$ (from radiometers) for the steady 25 mm ethylene flames on ISS. $\Omega$ is a dimensionless group from a dimensional analysis based on gas-radiation theory, built from the CO2 and H2O partial pressures for complete combustion (through an emissivity computed with the RADCAL narrow-band model), the normalised flame height squared $(x_f/R)^2$ and a flame-to-ambient temperature ratio; its full expression (dissertation Eq. 4.33) is garbled in the PDF text layer and is not reproduced here. Valid only for the sootless (blue) BRE ethylene flames analysed; predicted $X_r$ within 10% of measurement. A later chapter of the same dissertation reports an alternative power-law fit $X_r = 0.49\,\Omega^{n}$ with exponent $n = 0.12$ ($R^2 = 0.87$, dissertation Fig. 5.1).

<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *A best-fit equation for the steady data is given as*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *0.0633ln(Ω)+0.452*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *the dimensionless parameter depends on the partial pressures of CO2 and H2O for complete combustion, flame size, and oxygen.*
<https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The prediction is within 10 % of the experiment.*

$$
t_{osc},\ t_{ext} \;\propto\; X_{O_2}^{3}\,\mathrm{Re}^{-1/2}, \qquad \mathrm{Re} = \frac{\rho u D}{\mu}
$$

Correlation reported by Wright (2021) for the ISS flames that oscillated and self-extinguished: the times correlate with $X_{O_2}^3\mathrm{Re}^{-1/2}$. The proportional form is our reading of the abstract, not an established law. $t_{osc}$, $t_{ext}$: time from ignition to oscillation onset and to extinction (s); $X_{O_2}$: ambient O2 mole fraction (0.21-0.40); Re: jet Reynolds number of the fuel stream leaving the burner, with $\rho$, $u$, $\mu$ the fuel-stream density, mean velocity and viscosity and $D$ the burner diameter (25 or 50 mm). Times were independent of pressure over 0.57-1 bar. The abstract gives only the scaling group, not the prefactor or scatter; the Re definition is the standard one.

<https://drum.lib.umd.edu/handle/1903/27484>: *The measurements are reasonably well correlated by scaling the oscillation onset and extinction times with XO23 Re–0.5, where Re is the jet Reynolds number.*
<https://drum.lib.umd.edu/handle/1903/27484>: *These times decrease with increasing burner diameter but are independent of pressure.*
Textbook background

## Method

### Apparatus

Flat, round, porous gas burners of 25 mm and 50 mm diameter with a copper top plate, embedded heat-flux gauges (two on the 25 mm burner: centre and offset at 9.5 mm radius), a copper slug calorimeter and surface thermocouples, mounted in the ACME chamber insert inside the CIR combustion chamber (nominally ~100 L, about 15 L occupied by hardware). The insert provides a hot-wire igniter, mass flow controllers for fuel delivery, a radiometer array, photomultiplier tubes (one with an OH* filter) and cameras; tests are configured by ISS crew and commanded remotely from NASA Glenn.

### Fuels and samples

- ethylene (C2H4), undiluted (gas, flat porous burner, 25 and 50 mm)
- ethylene diluted with nitrogen (50% C2H4 bottle; flow-controlled fuel mole fraction 0.15-1, heats of combustion 15-47.2 kJ/g) (gas, flat porous burner, 25 mm)
- methane (CH4), undiluted bottle (objective names CH4/N2 mixtures) (gas, flat porous burner, 25 mm)
- emulated materials (not burned on ISS): e.g. PMMA, nylon, POM, polyethylene, polypropylene (solid, represented by burner settings matched to material properties)

### Procedure

For each test the crew/ground set the chamber atmosphere (diluent, O2 concentration, pressure), started fuel flow at a fixed rate and ignited it with the hot-wire igniter. The flame was observed at constant flow while burner surface temperature and heat flux evolved; a test ended either at self-extinction or, for flames that appeared steady, by commanded fuel shutdown (in practice after about 2-5 min, partly to conserve fuel and keep the atmosphere roughly constant). The planned extinction-limit procedure was to reduce flow stepwise after the burner reached steady temperature. Ignition limits were deliberately not studied in orbit. Several ignitions were made per test day: 194 flames over 18 test days, 2019-02-08 to 2021-01-28 (a 2019 round and a 2020-21 round after a one-year hiatus). Normal-gravity lab tests with gas, liquid and solid fuels, 5.18 s drop-tower tests at NASA Glenn and CFD modelling supported the flight work.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| ambient oxygen fraction (O2 diluted with N2) | 0.21-0.40 (table lists approximate values 21, 25, 26.5, 34, 40%) | mole (volume) fraction |
| ambient pressure | 56-100 kPa (0.56-1 bar; Wright gives 0.57-1 bar) | kPa |
| burner diameter | 25, 50 | mm |
| fuel type | ethylene, methane |  |
| fuel mole fraction in fuel/N2 mixture (sets heat of combustion and smoke point) | 0.15-1 (round 1 design); bottles of 100% and 50% C2H4 | mole fraction |
| fuel mixture mass flux through burner | 1-12 (round 1 design) | g/(m2 s) |

Held constant:

- ambient flow: quiescent (no forced or buoyant flow)
- ambient diluent: nitrogen in all tests documented (O2/CO2 ambients were a 'desired' objective; no evidence found that they were run)
- fuel flow during a test: constant (set per test)

Number of tests: 194

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| net heat flux to burner surface (centre and offset points) | embedded heat-flux gauges | direct |
| area-averaged heat flux | copper slug calorimeter (operation compromised; theoretically corrected) | derived |
| burner surface (copper) temperature | two surface thermocouples | direct |
| effective heat of gasification L | heat flux / imposed fuel mass flux | derived |
| flame radiative loss fraction | radiometers | derived |
| flame height, base radius, oscillation onset and extinction time | four video cameras (image analysis) | derived |
| OH* chemiluminescence | photomultiplier tube with OH* filter | direct |
| fuel mass flow rate | mass flow controllers | direct |

## Findings

1. Small (25 mm) emulated condensed-fuel flames burned quasi-steadily for minutes in quiescent microgravity, with no air flow and no flame spread; more than half of round-1 tests (59 analysed ignitions) burned at least 2 and up to 5 minutes, and ~29 flames reached an apparently steady state for 120 s or more before shutdown. *(result, high)*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *Hazard! Low-momentum microgravity flames can burn for minutes in the absence of an air flow or flame spread.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *More than half of the tests resulted in long burns of at least 2 and as long as 5 minutes.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *Twenty-nine of the flames lasted*
   - PSI record field `researchImpacts`
2. Oxygen threshold for the 25 mm ethylene/N2 flames tested: all flames in 21% O2 (by volume) self-extinguished within 40 s, whereas steady flames were observed at nominal 26.5%, 34% and 40% O2. NASA's summary places the self-extinction boundary at roughly 25% O2. This is a threshold for these burner conditions (flow rates, sizes), not a material flammability limit. *(limit, high)*
   - <https://drum.lib.umd.edu/handle/1903/29303>: *All flames burning in 21% by volume oxygen self-extinguished within 40 s. However, steady flames were observed at 26.5, 34, and 40% oxygen.*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *they were found to self-extinguish in concentrations below ~25% (by volume).*
   - PSI record field `researchImpacts`
3. Flames that were shut down rather than self-extinguishing were close to steady: by theoretical analysis all such end points were above 94% of steady-state heat flux (and the steadiest above 94% of steady height), supporting use of their end-point heat flux to derive an effective heat of gasification. *(method, medium)*
   - <https://drum.lib.umd.edu/handle/1903/29303>: *The steadiest flames reached more than 94% of their steady-state heat fluxes and heights.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *all of the test endpoints were more than 94 % of steady state in flame heat flux*
4. At fixed atmosphere (34% O2, 0.56 bar = 56 kPa, undiluted C2H4, 25 mm), raising the fuel mass flux made flames larger and eventually unstable: 1.78 and 2.55 g/(m2 s) flames grew to steady state and were shut down at ~3 min, while a 6.95 g/(m2 s) flame oscillated (partial extinction from 20 s) and fully extinguished at 34 s; self-extinguished flames in this set occurred above ~3 g/(m2 s) and all showed periodic growth and decay first. *(trend, medium)*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *As the mass flux is increased: 1.78, 2.55 and 6.95 g/m2s, the flame grows taller and finally extinguishes at the highest flow rate.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The self-extinguished flames occurred above 3 g/m2s and they all showed periodic growth and decay before final flame cessation.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *It periodically moves from full to partial in existence until complete elimination at 34 s.*
5. Larger burner flames were less persistent: at elevated O2 larger flames (including those on the 50 mm burner) generally self-extinguished within 1.5 minutes, whereas 25 mm flames could burn for minutes. Oscillation-onset and extinction times decreased with burner diameter, were independent of pressure (0.57-1 bar), and correlated with X_O2^3 Re^-0.5 (Re = jet Reynolds number). *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *larger flames were generally seen to self-extinguish within 1.5 minutes.*
   - <https://drum.lib.umd.edu/handle/1903/27484>: *These times decrease with increasing burner diameter but are independent of pressure.*
   - <https://drum.lib.umd.edu/handle/1903/27484>: *The measurements are reasonably well correlated by scaling the oscillation onset and extinction times with XO23 Re–0.5, where Re is the jet Reynolds number.*
6. Methane flames at elevated oxygen self-extinguished within a minute, whereas ethylene flames under similar conditions could burn for minutes. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210022542/downloads/ACME%20JASMAC-33%2020211007.pdf>: *While ethylene flames at elevated oxygen concentrations can burn for minutes, methane flames were seen to self-extinguish within a minute.*
7. Qualitatively, higher oxygen, lower pressure and lower heat of combustion (more N2 dilution) gave more stable flames; at 1 bar some shut-down flames showed sustained periodic extinction for ~1 minute, while the same conditions at 0.56 bar showed no periodic behaviour. *(trend, low)*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *All these image sequences suggest that higher oxygen, lower pressure, and lower heats of combustion tend to generate more stable flames that could reach steady state or last longer.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *except with an atmospheric pressure of 0.56 bar there was no periodic behavior observed.*
8. Radiation dominates the loss budget: radiative loss fraction stayed below 0.6 for steady flames and correlated with flame height; in simulations of these burner flames the radiative fraction was an order of magnitude higher than for 1-g flames from the same burner, and radiative loss caused the extinction and instability. *(result, medium)*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *radiation fractions remained below 0.6 for the steady flames and correlate with the flame height.*
   - <https://doi.org/10.1134/S0010508220040036>: *The radiative fraction in the microgravity flames is found to be by an order of magnitude higher than that in the normal gravity flames produced by the same burner.*
9. Mapping derived heats of gasification onto real materials suggests that, at 25 mm scale, polyethylene and polypropylene could burn steadily in microgravity at about 3 g/(m2 s), nylon and PMMA at about 2.5 g/(m2 s), and a phenolic-glass composite at about 1 g/(m2 s) - much lower rates than in 1 g (PMMA ~19 g/(m2 s) at 25 mm), implying materials may burn more easily but more slowly in microgravity. On the resulting flammability map an emulated PMMA flame falls in the flammable zone at X_O2 0.40 and 0.34 but in the extinction zone at 0.265. These are model-based inferences from emulator data, not tests of the materials. *(result, low)*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *Nylon and PMMA would burn at about 2.5 g/m2s, and the phenolic glass fiber composite would burn at about 1 g/m2s.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The implication is that materials can burn more easily in microgravity than in normal gravity but with much lower burning rates.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *it suggests that PMMA burns steadily at XO2 of 0.4, and 0.34. But, for the last case, XO2 of 0.265, since the PMMA point falls in the extinction zone*
   - PSI record field `researchImpacts`
10. The theoretical model (flame extinction criterion 1100 K) predicts that lowering cabin pressure widens the range of steady burning toward higher burning rates, so the low-pressure, higher-O2 atmospheres NASA is considering would widen the burning range (worse for fire safety). *(trend, low)*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *The effect of dropping the atmospheric pressure tends to expand the range of burning to higher burning rates.*
   - <https://drum.lib.umd.edu/bitstream/1903/29303/2/Dehghani_umd_0117E_22750.pdf>: *As NASA seeks to provide habitable atmospheres of lower pressure and higher oxygen levels. Such a move will exacerbate the burning conditions.*
11. Ground precursor: in 5 s drop-tower tests (25 and 50 mm burners, CH4 and C2H4, 0.5-1 atm, 21-30% O2) the heat flux became quasi-steady but flame height reached only ~37% of its steady value in a typical 25 mm test, so ISS-duration tests were required; the burner could emulate heats of gasification of about 0.4-4 kJ/g. *(method, high)*
   - <https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *For the particular case shown in Figure 2a, the flame height reaches only about 37% of steady state after 5 seconds.*
   - <https://ntrs.nasa.gov/api/citations/20170009141/downloads/20170009141.pdf>: *the BRE burner could emulate fuels with heat of gasification in the range of 0.4 – 4 kJ/g*
12. Simulations of the ISS test conditions in normal air (3-D, transient) reproduce the observed time to extinction; extinction happens when the instantaneous radiative fraction rises to 60-70% of the current heat release rate, a level reached because the low-momentum microgravity flame has a long residence time. After local extinction the flame edge takes a hook-like (bibrachial) form, and on re-ignition a triple flame runs along the stoichiometric surface. *(result, medium)*
   - <https://doi.org/10.1016/j.proci.2020.06.110>: *Time to flame extinction predicted in this work agrees with the experimental observations. Extinction occurs due to the excessive radiative losses when the instantaneous radiative fraction grows up to 60–70% of the current heat release rate.*
   - <https://doi.org/10.1016/j.proci.2020.06.110>: *The excessively high level of the radiative losses is facilitated by the long residence time in the low-momentum microgravity flame.*

## Fire-safety relevance

Spacecraft fire response relies partly on stopping ventilation to starve a fire. BRE indicates that a small burning surface can keep burning for minutes in still air in microgravity, particularly in oxygen-enriched atmospheres, so turning off flow may not extinguish a fire quickly at elevated O2. The investigators suggest NASA make more use of the cone-calorimeter-based flammability Test 2, whose measured properties (heat of combustion, heat of gasification) map onto BRE's flammability maps, alongside the upward-flame-spread Test 1. Transferability caveats: BRE is a gas burner with imposed fuel flow; it does not pyrolyse, melt, drip, char or spread, and L is derived as heat flux / mass flux, which is exact only for simply vaporising fuels. Emulation was validated for several materials in 1 g, but its accuracy for real materials in microgravity was not directly verified with real samples on ISS. Sizes were 25 and 50 mm only. The O2 thresholds therefore describe burner flames at the tested flow rates, not material flammability limits.

### Habitat conditions

The test atmospheres bracket the NASA-considered cabin atmospheres named in the objective: 21% O2 at 14.7 psia (101.4 kPa), 26.5% at 10.2 psia (70.3 kPa) and 34% at 8.2 psia (56.5 kPa, the exploration atmosphere). The dissertation describes these nominal pairs as 21% at 1 bar, 26.5% at 0.7 bar and 34% at 0.565 bar. Steady burning was seen at 26.5% and 34% (and at 40%, above any proposed habitat level), while 21% flames self-extinguished; i.e. the exploration atmosphere (34% O2, 56.5 kPa) falls on the side where these small flames persist. Pressures per test are not in PSI. Against the shared reference atmospheres: the 21% O2 / ~100 kPa tests correspond to Earth sea level (20.9% O2 at 101.3 kPa), where these flames self-extinguished. The 34% O2 / 56.5 kPa case lies inside the Moon-habitat envelope (30% O2 or more at 70.3 kPa or less), and the 40% tests exceed it in O2; the 26.5% / 70.3 kPa case is at the envelope's pressure but below its O2. Steady burning was observed in all three of these enriched conditions. Spacesuit conditions (100% O2 at 29.6 kPa) were far outside the tested range (at most 40% O2, at least ~56 kPa).

### Earth benefits

The emulation approach and its 1-g validation (wick and gas-burner tests on ignition and extinction of small fires) are aimed at fire science generally; NASA states the results could improve fire safety on Earth, but no specific Earth application is documented in the sources reached.

## Limitations

- Emulation, not real materials: a gas burner with prescribed fuel flow cannot reproduce pyrolysis chemistry, charring, melting, bubbling, dripping, in-depth heating or flame spread; real-material burning in microgravity was not tested.
- Only 25 and 50 mm burners; results are size-dependent (larger flames radiated more and extinguished sooner), so extrapolation to larger fires is uncertain.
- Quiescent ambient only; no ventilation-flow cases, so results apply to post-ventilation-shutdown conditions, not to normal cabin airflow.
- Only ethylene and methane (with N2) were used; heat of combustion range 15-47.2 kJ/g; smoke point is set by these fuels. Methane flames behaved differently (short-lived).
- Measurement issues: the slug calorimeter's operation was compromised and needed a theoretical correction; heat-flux gauges showed early water-condensation artefacts.
- Steadiness is inferred from theory (flames were shut down at ~2-5 min to conserve fuel and keep the atmosphere constant), and the slowly varying chamber atmosphere during a day's tests is not documented in PSI.

## Data in PSI

PSI holds only a one-page summary table (18 test days: date, burner size, fuel bottle, approximate O2 values, number of flames ignited) and an ISA-Tab metadata zip that repeats the record text. No per-test conditions (pressure, flow rate, outcome, duration), no sensor data, no video and no documents are in PSI, so none of the findings below can be re-derived from PSI data. The record's totalFileSize field (2,035,568,427,496 bytes, ~2 TB) is inconsistent with the two ~16 kB files actually listed.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | summary of ISS test days (18 rows) | .csv | 1 | 1.1 kB | yes |
| metadata | ISA-Tab investigation/study files (i_Investigation.txt, s_PSI-20.txt with placeholder rows); zip name refers to PSI-96 | .zip .txt | 1 | 15 kB | yes |

Rows in the unified `tests` table: 18

## Related investigations

- [PSI-10](PSI-10-acme-flame-design.md): shared hardware
- [PSI-21](PSI-21-acme-cld-flame.md): shared hardware
- [PSI-22](PSI-22-acme-e-field-flames.md): shared hardware
- [PSI-23](PSI-23-acme-s-flame.md): shared hardware
- [PSI-159](PSI-159-acme-cfi-g.md): shared hardware

## Open questions

- PSI lacks per-test conditions; with the investigators' Table 3.1 (O2, fuel fraction, pressure, mass flux, heat fluxes, flame size, burn time, end point) one could build an O2-pressure-mass-flux map of steady vs self-extinguished outcomes.
- Reconcile the 194 flames in the PSI table with the 149 successful ignitions reported in the dissertation (possibly different subsets, e.g. methane or 50 mm tests).
- Analysis of the methane and 50 mm tests is only summarised in slides; quantitative extinction-time results for them were not found beyond the Wright thesis abstract.
- Whether the O2/CO2 ambients (objective 2) and stepwise flow-reduction extinction tests (objective 3) were actually run is not documented in the sources reached.
- Direct comparison of BRE-predicted flammability with cone-calorimeter (Test 2) data for specific spacecraft materials has not been seen.

## Dashboard ideas

- **ISS test-day timeline** (`date`, `burner_mm`, `fuel_bottle`, `o2_values_pct`, `flames_ignited`): Only data PSI holds; shows campaign structure (2019 round, 2020-21 round), fuel and size coverage.
- **oxygen vs outcome summary** (`x_o2`, `pressure_kPa`, `outcome (steady/self-extinguished)`, `burn_time_s`): Core fire-safety message (21% extinguishes, >=26.5% steady); requires per-test data not in PSI.
- **habitat atmosphere overlay** (`x_o2`, `pressure_kPa`): Places the three NASA cabin atmospheres (101.4/70.3/56.5 kPa) on the tested range.
- **flammability map** (`heat_of_combustion_kJ_g`, `heat_of_gasification_kJ_g`, `x_o2`): How BRE links to cone-calorimeter material properties (e.g. PMMA, nylon).

## Gaps and data-quality notes

- No Science Documents, Reports, Presentations, Analyzed/Raw Data in PSI: only the experimental table CSV and a metadata zip. All results come from the PSI record text and external sources.
- Per-test pressure, flow rate, fuel mole fraction, burn duration and outcome are not in PSI (table notes say pressures are not identified). Pressure ranges are from the dissertation and Wright thesis.
- Abstracts of the 11 Elsevier papers in the record (Combustion and Flame, Proc. Combust. Inst., Fire Safety Journal) were not reachable: Crossref has no abstracts, Semantic Scholar elides them, ScienceDirect returned HTTP 403. Only the abstracts of 10.1002/fam.2896 and 10.1177/0734904113495650 (Crossref) and 10.1134/S0010508220040036 (reconstructed from OpenAlex's word index) were read. 10.3850/978-981-07-5936-0_03-01 was not tried.
- Update (publication review, data/publications/PSI-20.json): the statement above is partly outdated. A Semantic Scholar batch query returned abstracts for 10.1016/j.combustflame.2021.01.035, 10.1016/j.proci.2020.06.110, 10.1016/j.combustflame.2019.09.030, 10.1016/j.proci.2018.05.006 and 10.1016/j.combustflame.2018.01.044, and the Lund University portal gave the abstract of 10.1016/j.firesaf.2019.02.003. The Dehghani 2021 abstract confirms the dissertation-based findings (59 tests, 21-40% O2, 0.56-1 bar, steady flames at nominal 26% O2 and above, end points above 94% of steady heat flux) and adds that the analysed mixtures had heats of combustion of 23.6 and 47.2 kJ/g. Still unread: 10.1016/j.combustflame.2023.112809, 10.1016/j.proci.2022.08.107, 10.1016/j.combustflame.2021.111572, 10.1016/j.firesaf.2016.11.003, 10.1016/j.combustflame.2015.05.005 and 10.3850/978-981-07-5936-0_03-01 (no abstract anywhere; ScienceDirect accepted manuscripts refuse automated access).
- NASA Glenn ACME page in the record (www1.grc.nasa.gov/.../acme/) now redirects to a generic NASA combustion-science page with no BRE content. Used instead: science.nasa.gov ACME and BRE pages, a 2021 NASA JASMAC-33 presentation (NTRS 20210022542), the 2015 Researcher's Guide to Combustion Science (pre-flight description only), NTRS 20160010073/20170009141 (drop-tower precursor), and UMD theses (Dehghani 2022, Wright 2021) not listed in the PSI record.
- Dissertation quotes come from the PDF's text layer, in which equations and symbols are garbled. The physics.equations taken from it (heat-of-gasification balance, effective B number, flame height, flame temperature, X_r fit) were reconstructed from that garbled text and checked for internal consistency; the full definition of the group Omega (Eq. 4.33) and the exponent of the later power-law X_r fit could not be read.
- Count mismatch: PSI table sums to 194 flames ignited; dissertation reports 149 successful ignitions (round 1 analysis used 59). Not resolved.
- Oxygen threshold wording differs: researchImpacts says 21% flames self-extinguished; JASMAC slides say below ~25%; table lists both 25% and 26.5% as nominal levels in different rounds.
- Table data issues: '3400%' (2019 Mar 7) and '2100%' (2019 Apr 1) are spreadsheet percent-format artefacts, read as 34 and 21; 2020 Dec 4 row is listed after Dec 5; 2019 Apr 1 had 0 flames ignited (reason not given).
- The evidence.parquet text chunk for the table is truncated after row 5 although it reports 19 non-empty rows; table statistics here were computed from the CSV.
- Metadata zip is named 'PSI-20_metadata_PSI-96_ACME BRE.zip' (refers to PSI-96); its contents are PSI-20. Record field totalFileSize (~2.04 TB) does not match the two files (~16 kB) listed.
- Investigator roles differ: PSI lists Sunderland as Project Scientist; UMD and NASA describe him as Co-Investigator.
- PSI record says 16 publications; 15 have DOIs; the Bustamante MS thesis has a DRUM link only in the metadata zip. ACME project count differs between sources (five vs six experiments).
- No text addressed to an AI or unrelated instructions was found in the PSI files.
- Source quality: several key results (O2 threshold, burn durations, material mapping, extinction-time scaling) rest on a PhD dissertation (Dehghani 2022), a master's thesis (Wright 2021) and a conference slide deck (JASMAC-33, 2021) rather than on the peer-reviewed papers, whose abstracts could not be read (see above).
