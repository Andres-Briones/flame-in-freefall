# PSI-68: FLEX-2 (Flame Extinguishment Experiment - 2)

The follow-on to FLEX burned single drops and pairs of drops of practical-fuel ingredients and fuel mixtures (octanes, heptane, decane, alcohols) on the Space Station to give engine and fire modellers clean benchmark data, and showed that the 'cool flames' found in FLEX occur for many normal-alkane fuels.

Investigators: Forman A. Williams (University of California, San Diego) - Principal Investigator; Frederick L. Dryer (Princeton University) - Co-Investigator; Benjamin D. Shaw (University of California, Davis; affiliation blank in PSI) - Co-Investigator; Mun Y. Choi (University of Connecticut) - Co-Investigator; Vedha Nayagam (Case Western Reserve University) - Co-Investigator; C. Thomas Avedisian (Cornell University) - Co-Investigator; Daniel L. Dietrich (NASA Glenn Research Center) - Co-Investigator; Michael C. Hicks (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Setting | ISS · CIR · MDCA |
| Platform | International Space Station (ISS) |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 2016-08-12 to 2019-09-30 |
| Fuels and samples | iso-octane; n-octane; n-heptane; n-decane; ethanol; 1-propanol/glycerol 95/5 and 80/20; n-heptane/iso-octane 50/50; n-decane/1-hexanol 50/50 |
| Varied | fuel: 8 fuels/mixtures in PSI table (iso-octane, n-octane, n-heptane, n-decane, ethanol, propanol/glycerol 95/5 and 80/20, heptane/iso-octane 50/50)<br>ambient oxygen fraction: 0.17, 0.21, 0.25, 0.30 (record approach: 0.1-0.4) mole fraction<br>diluent: N2 or He (table); CO2 and Xe also used in published tests<br>ambient pressure: 50.7, 101.3, 152.0, 202.6, 304.0 kPa (0.5, 1.0, 1.5, 2.0, 3.0 atm) kPa<br>initial droplet diameter: 1.5-5 mm<br>imposed flow velocity (droplet translation): 0.1-5 cm/s<br>droplet spacing and size in binary linear arrays |
| Fire-safety pillars | fundamental, suppression, detection |

## Question

FLEX-2 set out to provide benchmark data on isolated and interacting droplet combustion for fuels and conditions closer to practical combustors than FLEX: bi-component and surrogate mixtures, a range of pure fuels, elevated pressure, sub-buoyant convective flow and droplet-droplet interaction. Itemised goals were the role of liquid-phase mixing in bi-component droplets, steady and unsteady phenomena in pure-fuel burning, flame extinction mechanisms and boundaries, soot formation and soot-shell dynamics, the influence of droplet interactions on flammability limits of arrays, and validation of numerical models whose chemistry, radiation and phase-coupling approximations had not been tested against benchmark data.

## Summary

FLEX-2 extended the ISS FLEX droplet-combustion experiments in the CIR Multi-User Droplet Combustion Apparatus from two pure fuels to transportation-fuel components and mixtures. The PSI table lists the planned conditions: eight fuels (iso-octane, n-octane, n-heptane, n-decane, ethanol, propanol/glycerol 95/5 and 80/20, heptane/iso-octane 50/50), droplets 1.5-5 mm, oxygen mole fractions 0.17-0.30 in nitrogen or helium, pressures 0.5-3 atm and imposed relative flow 0.1-5 cm/s, plus binary droplet arrays. Published results from the programme show three-stage burning of large n-alkane droplets: hot-flame radiative extinction, a quasi-steady cool-flame stage, then cool-flame extinction and vapour-cloud formation. A scaling based on a critical flame temperature correlates radiative extinction diameters across CO2, He and Xe dilution. At about 2 atm, decane/hexanol droplets switched from cool-flame burning back to a hot flame spontaneously. For fire safety this establishes that invisible cool-flame burning and re-ignition are general features of alkane fuels, not specific to heptane.

## Physics

As in FLEX, a quiescent microgravity droplet burns with a spherically symmetric diffusion flame whose squared diameter decreases nearly linearly in time, and the flame can extinguish diffusively (too little residence time when the droplet is small) or radiatively (too much radiant loss when the flame is large). FLEX-2 adds three ingredients. (1) Multicomponent liquids: in a mixture the more volatile component evaporates first from the surface, and slow liquid-phase diffusion relative to surface regression (large liquid Peclet number) traps the less volatile component, changing the burning rate, causing staged burning or micro-explosion (e.g. propanol/glycerol, where glycerol is nearly involatile). (2) Soot: sooting fuels form a soot shell between droplet and flame whose size and position depend on initial diameter, increasing radiative loss for large droplets. (3) Low-temperature chemistry: n-alkanes have a negative-temperature-coefficient (NTC) range in which a weak cool diffusion flame at roughly 700-800 K can sustain quasi-steady burning after hot-flame radiative extinction, in Linan's partial-burning regime where fuel and oxygen leak through the reaction zone. Pressure, diluent (He, CO2, Xe), droplet interaction and slow flow each shift the balance between these regimes. Sub-buoyant flows of 0.1-5 cm/s, imposed by translating a tethered droplet, are slower than any buoyant flow on Earth and probe the transition from spherical to convective burning.

$$
D^2(t) = D_0^2 - K t
$$

d-squared law: droplet diameter $D$ (mm) at time $t$ (s) from initial diameter $D_0$ (mm) with burning-rate constant $K$ (mm2/s). In FLEX-2 n-alkane tests it holds separately in the hot-flame stage and the cool-flame stage, each with its own $K$; e.g. an n-decane droplet (4.03 mm, air, 0.5 atm) had $K$ = 0.41 then 0.33 mm2/s. Not valid during ignition, at extinction, or when multicomponent effects make burning staged.

Textbook background: Godsave/Spalding d-squared law.
<https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *The burning rate constants K (=dD2/dt) corresponding to the ﬁrst and second stage combustion were found to be 0.41 and 0.33 mm2/s respectively.*

$$
\mathrm{Pe}_l = \frac{K}{D_l} \gg 1
$$

Liquid Peclet number for a multicomponent droplet: ratio of surface-regression rate to liquid species diffusion. $K$: burning-rate constant (m2/s); $D_l$: liquid-phase mass diffusivity (m2/s, typically ~1e-9). With $K$ ~ 1e-7 m2/s, $\mathrm{Pe}_l$ ~ 100, so in the absence of internal circulation (as in quiescent microgravity) the volatile component is depleted only in a thin surface layer, the involatile component accumulates there, and staged burning or disruption can follow. A FLEX-team paper used n-propanol/glycerol droplets burned in reduced gravity to estimate liquid species diffusivities (title only read).

Textbook background: Diffusion-limit model of multicomponent droplet vaporisation (Landis and Mills; Makino and Law).
PSI record field `objective`
<https://doi.org/10.1007/s12217-015-9455-8>: *Estimates of Liquid Species Diffusivities in N-Propanol/Glycerol Mixture Droplets Burning in Reduced Gravity*

$$
\frac{D_{ext}^{rad}}{D_0} = f\!\left(D_0,\; \text{ambient } c_p,\ \lambda,\ \kappa_P,\ x_{O_2}\right) \text{ from } T_f(D_f) = T_{crit},\ \dot Q_{rad} = \chi_r \dot Q_{chem}
$$

Structure of the FLEX-2 radiative-extinction scaling (Nayagam et al. 2018): extinction is assumed when flame temperature $T_f$ (K) falls to a critical value $T_{crit}$, with radiative loss $\dot Q_{rad}$ a fraction $\chi_r$ of heat release $\dot Q_{chem}$; because radiative loss grows with flame volume, the droplet diameter at radiative extinction $D_{ext}^{rad}$ (mm) is set by initial diameter $D_0$ and gas-mixture properties (heat capacity, conductivity, Planck-mean absorption coefficient $\kappa_P$, oxygen fraction). Only the functional form is given here; the paper's fitted expression was not available to us.

<https://doi.org/10.1016/j.combustflame.2018.04.023>: *a simple scaling analysis, based on the assumptions that radiative extinction occurs when the flame temperature drops to a critical value and that the radiative heat loss rate is a fraction of the heat-release rate at the flame*

$$
\frac{D_f}{D} \approx 3 \;(\text{cool flame, n-alkanes}) \quad\text{vs}\quad \frac{D_f}{D} = \frac{\ln(1+B)}{\ln(1+f\,Y_{O,\infty})} \;(\text{hot flame, quasi-steady})
$$

Flame standoff ratio: flame diameter $D_f$ over droplet diameter $D$. For the hot flame, classical quasi-steady theory with transfer number $B$, ambient oxygen mass fraction $Y_{O,\infty}$ and stoichiometric fuel-to-oxygen mass ratio $f$ (about 0.29 for alkanes) gives large values (about 34 for $B \approx 8$ in air) that n-alkane hot flames never reach (they stay in the transient zone). The hot-flame expression is our reconstruction of the textbook quasi-steady form, not taken from the FLEX-2 documents. For the cool flame, partial-burning theory with the NTC turnover temperature in place of the adiabatic flame temperature predicted 3.1, and a frame-averaged image of a cool flame around an n-decane droplet in 1 atm air gave 3.2.

Textbook background: Burke-Schumann quasi-steady droplet flame position.
<https://ntrs.nasa.gov/api/citations/20160000344/downloads/20160000344.pdf>: *Measured FSR 3.2, predicted 3.1!*
<https://ntrs.nasa.gov/api/citations/20160000344/downloads/20160000344.pdf>: *Hot flame FSR QS model predicts FSR orders of magnitude greater than experimental or numerical results*

## Method

### Apparatus

Same CIR chamber and MDCA insert as FLEX (opposed-needle deployment, retractable hot-wire igniters, backlit droplet camera, OH* UV camera, colour camera, radiometers), with an added second High Bit-Depth Multispectral (HiBMs) camera and crossed silicon-carbide fibre arrays to pin droplets at several positions for droplet-interaction tests. Droplets could be free or fibre-supported, and a fibre could be translated to impose a slow relative flow.

### Fuels and samples

- iso-octane (liquid, droplet 1.5-5 mm)
- n-octane (liquid, droplet 1.5-5 mm)
- n-heptane (liquid, droplet 1.5-5 mm)
- n-decane (liquid, droplet 1.5-5 mm, single and binary arrays)
- ethanol (liquid, droplet 1.5-5 mm)
- 1-propanol/glycerol 95/5 and 80/20 (liquid, bi-component droplet 1.5-5 mm)
- n-heptane/iso-octane 50/50 (liquid, bi-component droplet 1.5-5 mm)
- n-decane/1-hexanol 50/50 (by volume) (liquid, large bi-component droplet, free or fibre-supported (not in PSI table))

### Procedure

The chamber was filled to 0.5-3.0 atm with 0.1-0.4 O2 and a diluent balance and allowed to settle ~2 min. For tethered tests, a predetermined amount of fuel was dispensed onto the support fibre; after needle retraction a dwell of at least 10 s let deployment-induced liquid motion decay. The igniter was powered for 1-5 s and retracted; for convective tests the droplet translation started as the igniter retracted. The colour-camera video was downlinked in near real time to verify deployment, ignition and progress, and chamber pressure and temperature were recorded. Independently varied parameters: fuel type, ambient gas composition, pressure, initial diameter, translation velocity (and acceleration), and droplet spacing and size in a binary linear array.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel | 8 fuels/mixtures in PSI table (iso-octane, n-octane, n-heptane, n-decane, ethanol, propanol/glycerol 95/5 and 80/20, heptane/iso-octane 50/50) |  |
| ambient oxygen fraction | 0.17, 0.21, 0.25, 0.30 (record approach: 0.1-0.4) | mole fraction |
| diluent | N2 or He (table); CO2 and Xe also used in published tests |  |
| ambient pressure | 50.7, 101.3, 152.0, 202.6, 304.0 kPa (0.5, 1.0, 1.5, 2.0, 3.0 atm) | kPa |
| initial droplet diameter | 1.5-5 | mm |
| imposed flow velocity (droplet translation) | 0.1-5 | cm/s |
| droplet spacing and size in binary linear arrays |  |  |

Held constant:

- ambient temperature: 25 C
- gravity: ISS microgravity

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| droplet diameter history, burning-rate constants (hot- and cool-flame stages), extinction diameters | backlit HiBMs cameras | derived |
| radiant emission history (broadband 0.6-5.0 um and narrowband 5.0-7.0 um) | MDCA radiometers, 100 Hz | direct |
| flame diameter and flame standoff ratio; soot shell and soot volume fraction | OH* UV camera, colour camera, HiBMs | derived |

## Findings

1. Cool-flame (second-stage) burning after hot-flame radiative extinction occurs for several n-alkanes, not only heptane: n-heptane, n-octane and n-decane droplets in O2/N2/CO2 and O2/He/N2 at 0.5, 0.7 and 1 atm (14-25% O2) showed quasi-steady low-temperature burning, cool-flame extinction at a finite diameter and vapour-cloud formation, while smaller droplets burned to completion or disrupted. Cool-flame extinction diameters of the three alkanes followed a trend resembling their ignition delay times. *(result, high)*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *Large n-alkane droplets exhibited quasi-steady low-temperature burning and extinction following radiative extinction of the visible flame while smaller droplets burned to completion or disruptively extinguished.*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *Remarkably the “cool ﬂame” extinction diameters for all the three n-alkanes follow a trend reminiscent of the ignition delay times observed in previous studies.*
2. n-Decane at 0.5 atm in O2/N2: a 4.03 mm droplet in air burned with K = 0.41 mm2/s in the hot-flame stage (visible extinction at ~14.6 s) and 0.33 mm2/s in the cool-flame stage, whose end was marked by a drop in the narrowband radiometer signal; at 25% O2 a 3.79 mm droplet avoided radiative extinction and micro-exploded at 26 s (K = 0.52 mm2/s); at 17% and 14% O2 hot/cool K were 0.31/0.27 and 0.29/0.25 mm2/s with earlier extinctions. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *The burning rate constants for the ﬁrst and second stage combustion were 0.31 and 0.27 mm2/s, respectively.*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *In general it can be summarized based on the results presented in Fig. 1 that reducing the ambient oxygen concentration leads to earlier hot and cool ﬂame extinctions.*
3. Helium substitution for nitrogen at 21% O2 and 1 atm (n-octane): hot/cool-flame K rose from 0.48/0.38 mm2/s (no He, 3.6 mm) to 0.54/0.43 (15% He) and 0.63/0.53 mm2/s (50% He), with shorter burning in both stages; at 75% He the hot flame died within a fraction of a second and the cool flame also ended quickly, so quasi-steady burning was not achieved. A later FLEX-team analysis reports that helium drastically increases the cool-flame extinction diameter compared with N2, CO2 or Xe, while xenon gives longer burning and a smaller extinction diameter. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *The ﬁrst and second stage burning rates are now 0.54 and 0.43 mm2/s, respectively, which is slightly higher than R298 due to increased thermal conductivity of helium compared to nitrogen.*
   - <https://ntrs.nasa.gov/api/citations/20205008449>: *The results show that the cool-flame extinction diameter is drastically increased with helium dilution compared to N2, CO2 or Xe, and Xe dilution leads to longer burning with a smaller extinction diameter.*
4. Radiative extinction of large n-heptane, n-octane and n-decane droplets with CO2, He and Xe replacing nitrogen at moderately varied pressures is correlated by a simple scaling that assumes extinction at a critical flame temperature with radiative loss a fixed fraction of heat release; the extinction diameter depends on initial diameter and ambient-gas properties. *(result, medium)*
   - <https://doi.org/10.1016/j.combustflame.2018.04.023>: *It is shown that a simple scaling analysis, based on the assumptions that radiative extinction occurs when the flame temperature drops to a critical value and that the radiative heat loss rate is a fraction of the heat-release rate at the flame, is able to correlate the measured droplet diameter at…*
5. Pressure changes the cool-flame regime: 50/50 decane/hexanol droplets in air showed sustained cool-flame burning after radiative extinction at >= 0.10 MPa; at 0.20 MPa fibre-supported droplets burned with a cool flame and then the hot flame spontaneously re-ignited; at about 0.30 MPa the droplet burned to completion with a cool flame that appeared fundamentally different from the 1 atm cool flame. Hexanol enlarged the cool-flame extinction diameter relative to pure decane, suggesting it inhibits cool-flame burning. *(result, high)*
   - <https://doi.org/10.1080/00102202.2016.1225730>: *At 0.20 MPa large fiber-supported droplets radiatively extinguished then burned with a cool flame for a period of time before the hot flame spontaneously re-ignited.*
   - <https://doi.org/10.1080/00102202.2016.1225730>: *The droplet diameters at cool-flame extinction were larger for the decane/hexanol droplets than for pure decane droplets at atmospheric pressure, suggesting that hexanol inhibits the cool-flame burning.*
6. Initial-diameter effects for sooting n-alkanes (n-heptane, n-octane, n-decane) in 1 atm room-temperature air, combining ISS and drop-tower data over D0 = 0.5-5 mm: burning rate decreases monotonically with D0 as soot and radiative losses grow; for D0 > 3 mm a three-stage process appeared (early radiative extinction, continued evaporation, then a second abrupt limit attributed to cool-flame extinction), with oscillatory flame peel-away before final extinction. *(trend, high)*
   - <https://doi.org/10.2514/6.2014-1019>: *The results show that the burning rate monotonically decreases with increasing Do.*
   - <https://doi.org/10.2514/6.2014-1019>: *A three-staged burning process was found for Do > 3 mm suggesting several extinction modes.*
7. Cool flames were imaged directly for the first time by removing camera filters and dimming the backlight: around an n-decane droplet in 1 atm air the frame-averaged cool flame was broad, weak and closer to the droplet than a hot flame, with standoff ratio 3.2 against 3.1 predicted by partial-burning theory; the same theory predicts cool-flame K within about 20%. In binary n-decane droplet arrays at 17% O2 and 1 atm, droplets of a size that burned only with a hot flame when isolated showed cool-flame burning when paired. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20160000344/downloads/20160000344.pdf>: *Similar size droplets: Single droplets only hot flame – Binary droplets cool flame*
   - <https://ntrs.nasa.gov/api/citations/20160000344/downloads/20160000344.pdf>: *Predicts K within ± 20%*
   - <https://ntrs.nasa.gov/api/citations/20210022617/downloads/JASMAC-33%20FLEX%20w%20video.pdf>: *They are located closer to the droplet surface compared to the hot flames*
8. Simplified cool-flame chemistry (a 6-step reduced mechanism based on the San Diego mechanism with activation-energy asymptotics) gives reasonable agreement with ISS cool-flame extinction diameters for heptane and octane but over-predicts n-dodecane extinction diameters, and deteriorates with increasing pressure; widely used detailed mechanisms also fail to predict second-stage cool-flame extinction accurately. *(limit, medium)*
   - <https://ntrs.nasa.gov/api/citations/20210022617/downloads/JASMAC-33%20FLEX%20w%20video.pdf>: *Agreements for heptane and octane seem reasonable, but dodecane extinction diameters are over predicted appreciably.*
   - <https://doi.org/10.1016/j.combustflame.2019.10.036>: *indicates deterioration of the simplified chemistry with increasing pressure in predictions of droplet diameters at cool-flame extinction.*
9. Cool-flame extinction scaling: in O2/N2 atmospheres the cool-flame extinction diameter of n-heptane, n-octane and n-decane droplets varies with ambient oxygen molar concentration to the power -3/4. With CO2 or He replacing N2 and at 0.5-1 atm this no longer holds, but the residence time at extinction D_ce^2/K_c (with the measured cool-flame burning-rate constant) correlates with oxygen concentration at the predicted slope of -3/2. The exponent comes from an NTC-crossover argument: activation energies of about 120 kJ/mol (crossover) and 180 kJ/mol (ketohydroperoxide branching). *(trend, medium)*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *The cool flame extinction diameters vary as oxygen molar concentration to the power -3/4 for oxygen/nitrogen mixture.*
   - <https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf>: *Remarkably the data are reasonably well correlated, considering the number of variables involved in the experiments, and, within the appreciable scatter, the results are in agreement with the theoretical slope of -3/2.*
10. The FLEX-2 surrogate-fuel image set has 278 burns of 11 fuels: n-decane; decane/propylbenzene 25/75, 50/50 and 75/25; n-heptane; heptane/iso-octane 50/50; heptane/toluene 50/50; iso-octane; n-octane; propylbenzene; and toluene. 13 burns were tethered, 11 were fully hidden by soot, and droplets measured 1.17-3.81 mm. An automated circle-fitting algorithm (backlit 1024x1024 camera at 30 fps, field about 30 mm) measured 98% of free-droplet runs, with a precision of +/-0.2 pixel (about 6 um) when soot occlusion was limited, and gives a precision estimate for each diameter. Several of these fuels are not in the PSI experimental table. *(method, high)*
   - <https://www.osti.gov/servlets/purl/1998037>: *The FLEX-2 experiments on surrogate fuels comprised 278 individual experiments (Table 1) for 11 different fuel types.*
   - <https://www.osti.gov/servlets/purl/1998037>: *The actual diameter of the droplet varies from 1.17 mm to 3.81 mm.*
   - <https://www.osti.gov/servlets/purl/1998037>: *In cases of limited occlusion, a measurement precision of ±0.2 pixels for the FLEX-2 dataset was achieved.*
11. Large 50/50 decane/hexanol droplets: as pressure rose from 0.05 to 0.3 MPa, the visible and OH* luminosity of the hot flame fell steadily while its broadband radiance stayed nearly constant. The cool flame that followed hot-flame extinction radiated more at higher pressure, reaching almost half the hot-flame radiance at 0.3 MPa. This prompted the idea that a cool flame and a hot flame coexist around the droplet. A Burke-Schumann analysis finds such a dual-flame structure possible only over a narrow range of conditions. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20170000666/downloads/20170000666.pdf>: *It was also observed that the cool flames that formed immediately following hot-flame extinction had radiant outputs that increased with pressure, reaching almost one-half of the hot-flame radiance at 0.3MPa.*
   - <https://ntrs.nasa.gov/api/citations/20170000666/downloads/20170000666.pdf>: *A Burke-Schumann analysis of this dual-structure seems to indicate such flame structures are possible over a narrow range of initial conditions.*
12. The partial-burning model of cool-flame droplet combustion gives reasonable magnitudes for the measured cool-flame burning-rate constants but does not reproduce their apparent dependence on pressure or initial droplet diameter. The 0.30 MPa decane/hexanol cool flame also appears inconsistent with currently available cool-flame kinetics. *(limit, medium)*
   - <https://doi.org/10.2514/1.J054437>: *The simplified predictions are found to produce reasonable agreement with the experimentally measured values of burning-rate constants but not with their apparent dependencies on pressure or on the initial droplet diameter.*
   - <https://doi.org/10.1080/00102202.2016.1225730>: *This result does not appear to be consistent with expectations based on currently available cool-flame chemical kinetics and may suggest the need for a different chemical-kinetic mechanism.*

## Fire-safety relevance

FLEX-2 was framed mainly around fuel and engine science, but its results matter for spacecraft fire safety in two ways. First, it showed that invisible cool-flame burning after hot-flame extinction is a general feature of large n-alkane droplets (heptane, octane, decane, dodecane, alkane/alcohol mixtures) and that at elevated pressure a cool flame can spontaneously re-ignite into a hot flame, so 'flame out' seen on a camera is not proof that reaction has stopped and partially oxidised vapour may accumulate. Second, its diluent comparisons (N2, He, CO2, Xe) quantify how inert-gas properties shift radiative and cool-flame extinction. Transferability is limited: mm-size droplets of hydrocarbon fuels in quiescent or slowly moving gas, not solid materials or large fires.

### Habitat conditions

The planned envelope (O2 0.17-0.30 at 0.5-3.0 atm, i.e. 50.7-304 kPa) brackets the Earth sea-level reference (20.9% O2, 101.3 kPa) and includes 30% O2, the oxygen level of the Moon-habitat reference, but the listed pressures (0.5 and 1.0 atm) straddle rather than match its 70.3 kPa; which O2/pressure combinations were actually run is not in PSI. The 100% O2 spacesuit atmosphere (29.6 kPa) is outside the range. Most published FLEX-2 results are for air or diluted air at 0.5-3 atm.

### Earth benefits

Benchmark data for surrogate transportation fuels and for low-temperature (cool-flame) chemistry used in engine design, aimed at cleaner, more efficient combustors and validated jet-engine models.

## Limitations

- PSI contains no per-test data for FLEX-2, so no result can be checked or extended from PSI; the condition table repeats one envelope for all eight fuels and does not say which combinations were run.
- Fuels in the PSI table differ from those described in other sources (e.g. propylbenzene, toluene, heptane/hexadecane, decane/propylbenzene, heptane/toluene in the 2012 plan; decane/hexanol and dodecane in publications), and CO2/Xe diluents used in publications are absent from the table, so the table is not a complete description of the campaign.
- Single droplets and pairs of mm-size liquid fuel in near-quiescent gas; results do not transfer directly to solid-material fires, sprays or ventilated cabins. Cool flames were usually inferred from droplet regression and radiometers rather than imaged.

## Data in PSI

PSI holds only a 1 kB CSV with 8 rows, one per fuel, giving the planned envelope (diameter 1.5-5 mm, O2/N2 or O2/He, O2 0.17-0.30, pressure 0.5-3.0 atm, 25 C, flow 0.1-5 cm/s), identical for every fuel. There are no per-test results, no images, radiometer data or documents in PSI for this accession, although the record's totalFileSize (~1.22 TB) implies raw data exist. Nothing quantitative about outcomes can be computed from PSI; all results below come from publications listed in the record.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | condition-set table, 8 rows (one per fuel/mixture), 7 columns | .csv | 1 | 1 kB | yes |

Rows in the unified `tests` table: 8

## Related investigations

- [PSI-69](PSI-69-flex.md): precursor
- [PSI-39](PSI-39-cfi.md): follow-on
- [PSI-159](PSI-159-acme-cfi-g.md): follow-on
- [PSI-117](PSI-117.md): ground re-analysis
- [PSI-142](PSI-142.md): ground re-analysis

## Open questions

- Obtain the per-test FLEX-2 table (fuel, pressure, diluent, d0, hot- and cool-flame K, both extinction diameters, translation speed) to build cool-flame extinction maps comparable to the FLEX table.
- Compare multicomponent (propanol/glycerol, heptane/iso-octane) burning rates and disruption times with diffusion-limit models to extract liquid diffusivities.
- Quantify how droplet spacing in binary arrays shifts hot- and cool-flame extinction and flammability limits.
- Map conditions under which cool flames re-ignite into hot flames as a function of pressure, oxygen and fuel, as a fire-safety hazard boundary.

## Dashboard ideas

- **planned condition envelope** (`fuel`, `x_o2`, `pressure_kpa`, `d0_mm`, `flow_cm_s`, `diluent`): The only data PSI holds; shows coverage relative to habitat atmospheres.
- **two-stage burning explorer** (`fuel`, `x_o2`, `diluent`, `K_hot`, `K_cool`, `d_ext_hot`, `d_ext_cool`): Illustrates hot-flame radiative extinction followed by cool-flame burning; values from publications, not PSI.
- **diluent comparison** (`diluent`, `x_diluent`, `K_hot`, `K_cool`, `d_ext_cool`): Shows He vs N2 vs CO2 vs Xe effects on burning and extinction.

## Gaps and data-quality notes

- PSI holds only the 8-row condition table and no documents; results come from the PSI record text and external sources: NTRS 20120015928 (2012 FLEX/FLEX-2 overview), NTRS 20140006750 (2014 cool-flame extinction preprint), NTRS 20160000344 (2015 ASGSR slides), NTRS 20210022617 (2021 JASMAC slides), NTRS 20205008449 abstract, and abstracts via OpenAlex/Semantic Scholar of 10.1080/00102202.2016.1225730, 10.2514/6.2014-1019, 10.1016/j.combustflame.2018.04.023 and 10.1016/j.combustflame.2019.10.036.
- Attribution between FLEX and FLEX-2 is blurred in the literature: papers speak of 'FLEX experiments', the two PSI records share most publications, and test numbers (e.g. R298, R377, R694) are not labelled by investigation. Results assigned here to FLEX-2 are post-2011 tests with fuels or features (octane, decane, mixtures, arrays) outside the FLEX matrix; this is our inference.
- Dates: PSI gives 2016-08-12 to 2019-09-30, but the 2012 overview says FLEX-2 operations started in January 2012 (planned to July 2014); the PSI dates may be the grant period (NNX16AR09A). Record totalFileSize (~1.22 TB) does not match the single 1 kB file in PSI.
- Table oddities: header ' Ambient Temperature (C)' has a leading space and 'Ambient Gas Mixture ' a trailing space; O2 list '0.17; 0.21;0.25; 0.3' has inconsistent separators; pressure entries have a trailing space; the envelope is identical for all eight fuels; the table lists no CO2 or Xe diluent although publications report them; the record approach states O2 0.1-0.4 versus 0.17-0.30 in the table. Gas names here keep their digits (O2/N2), unlike the FLEX table.
- Not read: the Shaw and Vang (2015) propanol/glycerol diffusivity paper (10.1007/s12217-015-9455-8; Springer redirected to login, no abstract in OpenAlex/Semantic Scholar); 'Multistage oscillatory cool flame behavior ... elevated pressure' and several other record publications with no DOI; Elsevier full texts. No FLEX-2 per-test summary report (analogous to NASA/TP-2015-216046 for FLEX) was found on NTRS.
- Number of FLEX-2 tests is not stated in PSI; the 2012 plan targeted ~400 test points, and the 2014 preprint says over three hundred droplet tests were completed across the FLEX series to that date.
- Shaw's affiliation is blank in the PSI contacts; contact details were not copied.
- No text addressed to an AI or unrelated instructions was found in the PSI files.
- Publication review (Nov 2026; per-paper notes in data/publications/PSI-68.json): of 48 listed publications, 5 were read in full, 21 by abstract and 22 not at all (closed journals without an open copy or indexed abstract). About 19 are ground-based or modelling studies.
- Fuel list conflict: the PSI experimental table lists 8 fuels (iso-octane, n-octane, n-heptane, n-decane, ethanol, propanol/glycerol 95/5 and 80/20, heptane/iso-octane 50/50) and droplets of 1.5-5 mm. Rasul et al. 2022 (IEEE TPAMI; OSTI 1998037) report that the flown surrogate-fuel set had 278 burns of 11 fuels, including toluene, propylbenzene, decane/propylbenzene and heptane/toluene, which are absent from the table, and droplets of 1.17-3.81 mm. The table appears to be a planning envelope, not a test list. The 278 covers only the surrogate-fuel part of FLEX-2 (not the decane/hexanol, CO2/Xe or array tests), so n_tests stays null.
- Analysis of the 2014 preprint (NTRS 20140006750) gives the decane test R383 as 14% O2 and 96% N2, which sums to 110% (probably 86%).
