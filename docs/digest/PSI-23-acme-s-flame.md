# PSI-23: ACME s-Flame (Structure and Response of Spherical Diffusion Flames (Advanced Combustion via Microgravity Experiments))

On the space station, gas fuels (hydrogen, methane, ethylene, diluted with nitrogen or helium) were fed out of a small porous ball into still oxygen-containing gas to make nearly perfect spherical flames, to see how such flames grow, and how they go out when the fuel supply is too small or when the flame becomes so large that it loses too much heat by radiation.

Investigators: Chung K. (Ed) Law (PI; Princeton University); Stephen D. Tse (Co-I; Rutgers University); Kurt R. Sacksteder (Co-I named in the final report; NASA Glenn, moved to other work before flight operations); Dennis P. Stocker (ACME Project Scientist; NASA Glenn); Vladimir V. Gubernov (lead collaborator; P.N. Lebedev Physical Institute, Russian Academy of Sciences)

## At a glance

| | |
|---|---|
| Platform | International Space Station (ISS), Destiny module |
| Facility | Combustion Integrated Rack (CIR) |
| Dates | 2015-02-05 to 2019-11-24 |
| Fuels and samples | Ethylene diluted with nitrogen; Methane diluted with nitrogen; Hydrogen diluted with nitrogen; Hydrogen/methane blends diluted with nitrogen; Helium-diluted fuels premixed on the ground; Chamber atmospheres |
| Varied | fuel type and fuel-stream composition: C2H4 15-50%, CH4 15-45%, H2 15-70%, H2/CH4 blends (20/25, 30/15, 25/20 % with 55% diluent); balance N2 (round 1) or He (round 2) mole % in fuel stream<br>inert diluent (fuel stream and atmosphere): N2 (round 1, 9 test days) or He (round 2, 9 test days)<br>ambient oxygen: ~0.21 and ~0.30 (both diluents); 0.175 with He on 20190; O2 decreases during a day with vitiation mole fraction<br>fuel-mixture flow rate from the burner (constant, ramped up or ramped down): about 1 to 17.5 cc/s (as reported by the investigators)<br>ignition settings (igniter tip type, preheat/ignition power and duration, fuel-flow timing): loop tip (round 1 and first He day), coil tip thereafter; e.g. 2.25-4.49 V |
| Number of tests | 276 |
| Fire-safety pillars | fundamental, detection, prevention |

## Question

s-Flame asked whether detailed chemical-kinetic and transport models, validated mainly on homogeneous systems and premixed flames, also predict diffusion flames. The test case was the simplest diffusion flame there is: a steady, one-dimensional spherical flame around a porous sphere that discharges fuel into a quiescent oxidizer. Such a flame exists only without buoyancy. Three objectives were set. (A) Measure the transient structure (temperature, species) of spherical diffusion flames that start from a non-steady ignition, for H2/CH4/diluent (soot-free) and C2H4/diluent (sooty) mixtures at several flow rates. (B) Find the two quasi-steady extinction limits. The low system Damkohler number limit is convective/kinetic extinction (small flame, short residence time). The high Damkohler number limit is radiative extinction (large flame, large radiating volume). (C) Determine the existence, onset and nature of pulsating instabilities predicted for fuel/diluent mixtures above a critical Lewis number. A second line of work concerned soot onset versus residence time in initially non-steady sooty flames. Ground facilities (2.2 s and 5 s drop towers, parabolic aircraft) were too short or too noisy to observe radiative extinction, which simulations predicted needs more than 2.5 s and up to about 25 s.

## Summary

s-Flame burned gaseous fuels issuing from a 6.35 mm porous spherical burner into a quiescent oxygen atmosphere at about 1 atm inside the ISS Combustion Integrated Rack. The aim was to test detailed chemistry and transport models against a one-dimensional diffusion flame. In 18 test days (Sept. 2019 to July 2020), 276 flames were ignited: 145 with nitrogen dilution of fuel and atmosphere (about 21% or 30% O2) and 131 with helium dilution (about 21%, 30% and 17.5% O2). Fuels were ethylene, methane, hydrogen and hydrogen/methane blends at roughly 1-17.5 cc/s. Nitrogen-diluted ethylene and methane flames showed both extinction branches. Flows of 5-10 cc/s gave flames that grew until radiative loss extinguished them. Flows ramped down toward 1 cc/s gave kinetic extinction. Radiative extinction, never seen in drop towers, was common. No flame was inherently sooty. Helium made ignition much harder and moved the limits. Predicted pulsating instabilities were not clearly seen. For fire safety, the work shows that flame size and residence time set extinction in quiescent microgravity, and that dim hydrogen flames are hard to see.

## Physics

Fuel leaving a porous sphere at mass flow rate m moves radially outward, and its velocity falls as 1/r^2. A diffusion flame sits where fuel diffusing outward and oxygen diffusing inward meet in stoichiometric proportion. For a flame sheet the flame radius scales roughly linearly with m. Without buoyancy the problem is one-dimensional: convection, diffusion and net radiation all act along the radius. This removes the flow ambiguities of counterflow and jet flames. After ignition near the burner, the flame front moves outward toward its steady radius while fuel accumulates inside it. Simulations predicted tens of seconds of growth, which only orbit can provide. Extinction of a diffusion flame occurs through reactant leakage when the flame Damkohler number (diffusion time over chemical time) drops too low. That can happen in two ways. At small m the flame is small and residence time is short, giving kinetic (blow-out-like) extinction at low system Da. At large m the flame is large. Radiative loss, a volumetric process, then grows faster than heat release, cools the flame and causes radiative extinction at high system Da. The steady response is therefore a closed 'isola', not an S-curve. Gas-phase reabsorption of radiation (CO2, H2O) reduces net loss and enlarges the flame at extinction. Near either limit, theory predicts that flames with Lewis number Le > 1 can develop pulsating instabilities, which grow until extinction. Le is greater than 1 when the deficient reactant diffuses more slowly than heat. Helium instead of nitrogen as diluent raises thermal conductivity (about 6x) and flame temperature, and changes Le and the Zeldovich number. Visible or CH* luminosity is not a reliable measure of flame strength in these transient flames. CH* emission can fall while temperature rises, so extinction should be judged from temperature or radiometer data.

$$
Da_f \equiv \frac{\tau_{diff}}{\tau_{chem}} \sim \frac{d_f^2}{\alpha}\, \exp\!\left(-\frac{T_a}{T_f}\right)
$$

Flame Damkohler number of a spherical diffusion flame. d_f flame diameter (m); alpha thermal diffusivity (m^2/s); T_a activation temperature of the overall reaction (K); T_f flame temperature (K). tau_diff ~ d_f^2/alpha is the diffusion (residence) time, tau_chem ~ exp(T_a/T_f) the chemical time. Scaling only, from the s-Flame SRD (its Eqs. 1-2); valid for a quasi-steady flame sheet with one-step Arrhenius kinetics. The flame is extinguished when Da_f falls below a critical value Da_f,e.

`PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p10): *let us consider the Damkohler number in the flame region, Daf, which is the ratio of the characteristic diffusion time to the reaction time at the flame, τDiff/τChem.*
`PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p10): *where df is the flame diameter, Tf the flame temperature, Ta the activation temperature, and α the thermal diffusivity*

$$
d_f \sim \dot m, \qquad Da_f \sim \dot m^{2} \exp\!\left(-A\,\dot m^{2}\right)
$$

Dual (kinetic and radiative) extinction scaling with burner mass flow. mdot burner mass flow rate (kg/s); A a positive constant set by the radiative loss. Radiative loss from a shell of thickness delta at the flame scales with flame volume and lowers T_f. Expanding the exponential for small loss gives Da_f(mdot), which tends to 0 both as mdot -> 0 and as mdot -> infinity. A critical Da_f,e therefore gives two extinction flow rates: m_e,1 (purely kinetic extinction, low system Da) and m_e,2 (radiation-induced extinction, high system Da). Order-of-magnitude scaling from the SRD (its Eqs. 3-6), not a fitted correlation.

`PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p11): *This final expression, shown in Fig. 1.4 with Daf plotted versus m, clearly demonstrates the dual extinction nature of the problem.*
`PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p11): *The lower value corresponds to the m2 in the coefficient term of Eq. (6 ), and hence represents purely kinetic exti nction, in the absence of heat loss. The upper value corresponds to the m2 term in the exponent, and hence represents extinction being induced by radiative heat loss.*

$$
r_f = \frac{\dot m}{4\pi \rho D \,\ln\!\left(1 + \dfrac{Y_{O,\infty}}{\nu\, Y_{F,0}}\right)}
$$

Steady flame-sheet radius of a burner-generated spherical diffusion flame. r_f flame radius (m); mdot total mass flow of the fuel stream from the sphere (kg/s); rho D density times mass diffusivity, taken constant (kg m^-1 s^-1); Y_O,inf ambient oxygen mass fraction; Y_F,0 fuel mass fraction in the supply stream; nu stoichiometric oxygen-to-fuel mass ratio. Textbook Shvab-Zeldovich result for a steady, adiabatic flame sheet with unity Lewis number in an unbounded quiescent oxidizer, neglecting the burner's own surface. It shows why diluted fuels and higher O2 give smaller flames, and why the flame grows linearly with flow. The real flames approach it only slowly (tens of seconds) and radiation keeps them from reaching it at high flow.

Textbook background

$$
Le = \frac{\alpha}{D_i}, \qquad Ze = \frac{T_a\,(T_{ad} - T_\infty)}{T_{ad}^{2}}
$$

Lewis and Zeldovich numbers. alpha thermal diffusivity (m^2/s); D_i mass diffusivity of the deficient reactant (m^2/s); T_a activation temperature (K); T_ad adiabatic flame temperature (K); T_inf ambient temperature (K). Pulsating thermo-diffusive instability is expected for Le sufficiently above 1 and large Ze. Helium dilution raises the flame temperature (lower molar heat capacity than N2), which lowers Ze and is expected to suppress oscillations. CO2 (proposed for a third round) would lower T_ad and raise Ze. Textbook definitions.

Textbook background
`PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p28): *However, higher characteristic flame temperatures (given the lower molar heat capacity of monatomic He versus that of diatomic N2) correspond to lower Zeldovich numbers, which would suppress oscillations based on Sivashinsky’s criterion for premixed flames.*

$$
\dot q_{rad}''' = 4\,\sigma\, a_P \left(T^4 - T_\infty^4\right)
$$

Optically thin radiative heat loss per unit volume. sigma Stefan-Boltzmann constant (5.67e-8 W m^-2 K^-4); a_P Planck-mean absorption coefficient of the gas mixture (1/m), dominated by CO2 and H2O (and soot if present); T local gas temperature (K). This is the optically thin limit. The s-Flame SRD notes that wide-band Planck-mean coefficients over-predict loss compared with statistical narrow-band (SNB) mean coefficients in the optically thin case, and that SNB computations with gas-phase reabsorption better matched drop-tower flame trajectories. Integrated over the hot shell, it grows with flame volume, which is what drives radiative extinction of large flames.

Textbook background
`PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p16): *As expected, wide-band Planck mean absorption coefficients (T&H), based on Tien (1968) and Hubbard an d Tien (1978), over-pre dict radiative loss compared to the statistical narrow band (SNB) mean coefficients for the optically thin cases.*

## Method

### Apparatus

Tests ran in the Combustion Integrated Rack on the ISS using the modular ACME chamber insert, a constant-volume chamber of about 83-90 L free volume. The burner was a 6.35 mm diameter porous sphere sintered from 316 stainless steel (10 micron media grade, about 41% porosity) on a supply tube. It carried a slightly embedded type-K surface thermocouple. The same unit (s/n 1003) served the earlier Flame Design and later CFI-G experiments. Three crew-exchangeable mass flow controllers metered fuel, oxidizer/inert and nitrogen. Their ranges were set on a nitrogen basis: 0.1, 0.5 and 1 slpm fuel MFCs were used on different days. A retracting resistive igniter, with a loop tip and later a thicker coil tip, lit the flame and was then withdrawn. Diagnostics, all synchronised by an automated script, were as follows. The ACME colour DataCam (1360x1024, 12-bit, fused-silica 'filter', often long exposures and bracketing, so frame rates near 1-10 fps) also served for thin-filament pyrometry (TFP). The CFI intensified camera (CH*, CH2O or clear filter, about 23 fps). The CIR LLL-UV intensified camera with a 310 nm OH* filter (512x512, 30 fps), used only by s-Flame among the ACME experiments. The CIR HiBMs camera with red backlight (15 fps), of little use for these soot-free flames. An analog ops camera recorded on the ground. A translatable array of 14 micron SiC fibres spaced 5 mm apart for TFP. Thermopile radiometers (0.2-11 micron) and three PMTs (OH* 310 nm, broadband, CH* 430 nm). Far-field thermocouples at 45-200 mm from the burner centre. Chamber pressure transducers. The CIR gas chromatograph sampled the chamber before and after tests. Non-imaging data were logged at 125 Hz. Accelerations were recorded by SAMS, although the rack isolation system was not used.

### Fuels and samples

- Ethylene diluted with nitrogen (bottle 50% C2H4/N2, diluted on orbit with ISS nitrogen to about 15-50% C2H4). Nominally the 'sooty' fuel (Le about 1) (gas, fuel stream from 6.35 mm porous spherical burner (normal flame))
- Methane diluted with nitrogen (bottle 45% CH4/N2; 15-45% CH4 tested) (gas, fuel stream from porous spherical burner)
- Hydrogen diluted with nitrogen (100% H2 bottle, diluted on orbit to 15-70% H2) (gas, fuel stream from porous spherical burner)
- Hydrogen/methane blends diluted with nitrogen (bottles 44.4% H2/55.6% CH4 and 66.7% H2/33.3% CH4; tested as 20% H2/25% CH4/55% N2 and 30% H2/15% CH4/55% N2). A third blend (25% H2/20% CH4) was lost when its bottle leaked (gas, fuel stream from porous spherical burner)
- Helium-diluted fuels premixed on the ground (round 2): 25% H2/20% CH4/He, 20% H2/25% CH4/He, 30% H2/15% CH4/He, 45% H2/He, 45% CH4/He, 20%, 25% and 30% C2H4/He (gas, fuel stream from porous spherical burner)
- Chamber atmospheres: O2/N2 (about 21% 'air' and 30% O2) in round 1; O2/He (30% O2/He bottles, diluted with 100% He to about 21%; also 17.5% O2/82.5% He on 20190) in round 2 (gas, quiescent oxidizer filling the ~83 L chamber at about 1 atm)

### Procedure

The crew only configured hardware: they swapped gas bottles, MFCs and igniter tips. Every test was commanded from the Glenn ISS Payload Operations Center and run automatically by a script with 68 parameters. The script steps were: open the image test point; position the TFP fibre array; preheat the igniter (e.g. 2 s at 3.5-4.49 V); start fuel flow; pulse the igniter (e.g. 0.5 s); retract it once OH* PMT ignition detection fired; then hold a constant flow or run one or more ramps and holds of fuel (and in round 1, on-orbit nitrogen dilution). Two protocols probed the two extinction branches. For radiative extinction, the flame was ignited at a given flow (often 3-17.5 cc/s), or established at about 3 cc/s and ramped up, and allowed to expand. For kinetic extinction, a near-steady flame was established at about 2-3 cc/s and then ramped down toward 1 cc/s. Extinction detection, a burner surface temperature limit of 250 C (held 3 s), or a flow timeout ended each test and stopped the gas. Typical flow times were up to about 45-120 s. An average of 15 flames were ignited per test day. The chamber was rarely vented between tests, so O2 fell and pressure rose slowly through a day ('vitiation'). Sometimes it was scrubbed through a molecular-sieve cartridge, or partly vented and refilled to change O2. The CIR gas chromatograph sampled the stirred chamber on most test days. Data were downlinked between test days so the next day's parameters could be adjusted. No testing took place during thruster firings or dockings.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel type and fuel-stream composition | C2H4 15-50%, CH4 15-45%, H2 15-70%, H2/CH4 blends (20/25, 30/15, 25/20 % with 55% diluent); balance N2 (round 1) or He (round 2) | mole % in fuel stream |
| inert diluent (fuel stream and atmosphere) | N2 (round 1, 9 test days) or He (round 2, 9 test days) |  |
| ambient oxygen | ~0.21 and ~0.30 (both diluents); 0.175 with He on 20190; O2 decreases during a day with vitiation | mole fraction |
| fuel-mixture flow rate from the burner (constant, ramped up or ramped down) | about 1 to 17.5 | cc/s (as reported by the investigators) |
| ignition settings (igniter tip type, preheat/ignition power and duration, fuel-flow timing) | loop tip (round 1 and first He day), coil tip thereafter; e.g. 2.25-4.49 V |  |

Held constant:

- burner: single 6.35 mm porous stainless-steel sphere (s/n 1003)
- chamber pressure: nominally ~1 atm (101 kPa) at fill, rising with vitiation. The uncalibrated ACME chamber transducer (PTA3) gives per-test medians of 1.03-1.09 atm (104.3-110.1 kPa) over 288 tests; the CIR chamber calculator file, which the project calls more reliable, is not in the downloaded set
- burner surface temperature limit (test abort): 250 C for 3 s
- gravity: ISS microgravity, rack isolation not used; SAMS acceleration data held at PIMS, not in PSI

Number of tests: 276

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame radius vs time (position of peak CH* or OH* chemiluminescence along several radii) | CFI intensified camera (CH*), LLL-UV camera (OH*), DataCam | derived |
| gas temperature profile across the flame | thin-filament pyrometry on 14 micron SiC fibres imaged by the colour DataCam | derived |
| OH*, CH* and broadband chemiluminescence intensity vs time (ignition and extinction detection, oscillations) | three PMTs (310 nm, broadband, 430 nm) at 125 Hz | direct |
| flame radiant emission | thermopile radiometer array plus offset wide-view radiometer (0.2-11 micron) | direct |
| burner surface temperature and far-field gas temperatures | type-K burner thermocouple; type-B/K rake thermocouples at 45, 60, 100, 100 mm and two at 200 mm | direct |
| fuel, inert and oxidizer mass flow rates (set-point and measured), chamber pressure | Hastings MFCs (nitrogen-basis calibration) and pressure transducers, logged at 125 Hz | direct |
| chamber gas composition before/after tests | CIR Gas Chromatograph Instrumentation Package (raw .asc chromatograms, not yet reduced) | direct |
| flame appearance and colour (blue vs sooty ignition, symmetry, local extinction, 'flash' events) | DataCam colour imaging, analog ops camera video, HiBMs backlit images | direct |

## Findings

1. For nitrogen-diluted ethylene in air (20% C2H4/80% N2 fuel stream, ~21% O2, ~1 atm), a flow of 3 cc/s produced a quasi-steady spherical flame that lasted until the automated system stopped it at the 250 C burner limit. At 5-10 cc/s the same mixture's flames grew until radiative extinction. Mixtures of 25% and 30% C2H4 also showed radiative extinction at the higher flows. *(result, high)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p26): *For a case of fuel-mixture of 20% C2H4 / 80% N2 at a flow rate of 3 cc/s, a seemingly quasi-steady flame is attained for extended duration. For the same mixture, higher flow rates of 5-10 cc/s result in radiative extinctions, corresponding to high system Damköhler number.*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p8): *The flame was shut down by the automated system because the burner reached a cut-off temperature of 250°C.*
2. Both extinction branches were observed for the same nitrogen-diluted ethylene mixtures in air. With 20-30% C2H4, non-sooty spherical flames established at 3 cc/s extinguished kinetically during a ramp down before the flow reached 1 cc/s. They extinguished radiatively during a ramp up before reaching 8 cc/s. A 15% C2H4 mixture could not sustain a quasi-steady flame even at 3 cc/s. Flames at 13.5-15 cc/s were asymmetric and extinguished radiatively. This is the dual-extinction 'isola' behaviour predicted by theory, but the extinction flow rates are given only as brackets. *(limit, medium)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p26): *For mixtures with 20-30% C2H4 content, spherical non-sooty flames are established at 3 cc/s; and kinetic extinctions are observed during ramp down before reaching 1 cc/s. For the same mixtures, radiative extinctions are observed when the non-sooty flames are established at 3 cc/s and the flow rates…*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p9): *The 15% C2H4 mixtures were not strong enough to sustain a quasi-steady flame at 3 cc/s before ramp down.*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p9): *High flow rate cases (e.g., 13.5 cc/s, 15 cc/s) showed asymmetrical flames which radiatively extinguished.*
3. Nitrogen-diluted methane (45% CH4/55% N2) in air at ~21% O2 gave no quasi-steady flame within the 0.5 slpm fuel MFC range: all flows were in the kinetic-extinction regime. In 30% O2/70% N2, the same mixture burned for about 15 s at 2 cc/s and about 10 s at 3 cc/s. At 5 and 9.4 cc/s the flames expanded to large radii and extinguished radiatively. Reducing the flow from 2 to 1 cc/s produced extinction during the ramp, interpreted as kinetic. 30%, 25% and 20% CH4 behaved similarly, while 15% CH4 flames extinguished very quickly after ignition. *(limit, medium)*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p9): *The results indicated that the flow rates specified by the fuel MFC (0.5 slpm) were in the regime of kinetic extinction. Quasi-steady flames could not be established.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p26): *For 45% CH4 / 55% N2, relatively long duration flames of ~15 s and ~10 s are established at flow rates of 2 cc/s and 3 cc/s, respectively. At larger flow rates of 5 and 9.4 cc/s, the flames expand to large radii and then extinguish, demonstrating radiative extinction at high system Damköhler number.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p27): *For 15% CH4 / 85% N2, flames are ignited, but extinguish soon after.*
4. Radiative extinction of growing spherical diffusion flames, predicted computationally but never conclusively seen in 2.2 s or 5 s drop towers or on parabolic aircraft, turned out to be a common event on the ISS. Kinetic extinction could also be reached only because a near-steady flame could be established first and then ramped down. The investigators list it first among the flight's initial surprises and discoveries. *(result, high)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p29): *Surprisingly, radiative extinction has been found to be a common event in ISS testing, which was predicted computationally, but not observed previously for our flame conditions.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p29): *Initial surprises and discoveries include: (1) Nitrogen-diluted methane and ethylene flames in air seem to demonstrate kinetic extinction at low flow rates (low system Da) and radiative extinction at high flow rates (high system Da).*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p5): *Although experimental data of good quality were obtained on the transient response of spherical diffusion flames in the 2.2-s drop tower facility, the duration was insufficient to observe radiative extinction.*
5. No inherently sooty flame was produced. This held for ethylene (up to 40-50% C2H4 in N2 after ramping, and 20-30% C2H4 in He), with either diluent, and at ~21% or ~30% O2. Soot appeared only during forced hot-wire ignition and dissipated as the flame grew. The sooty-flame objective (soot onset vs residence time, soot effect on extinction) was therefore not met. The team proposes propane and CO2 dilution for any third round. *(null_result, high)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p30): *(2) Ethylene flames which tend to soot under normal gravity conditions did not soot under microgravity conditions. Sooting only occurred during forced ignition from the hotwire, but soon dissipated. Inherent sooting was also not found for enriched oxidizer conditions or for either of the inerts…*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p31): *None of the flames were inherently sooty, so the effect of soot on extinction could not be investigated.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p33): *experimentation with C3H8 is of utmost importance if we are to achieve our original objectives with respect to characteristically sooty flames*
6. Nitrogen-diluted hydrogen flames (15-45% H2 in N2, into air, 0.5 slpm fuel MFC) did not extinguish radiatively. At 10 cc/s they appeared quasi-steady until the flow timed out. The investigators conclude that such flames would have to grow much larger than the chamber and flow range allow before radiative loss could extinguish them. Hydrogen produces only H2O as a radiating product. Extinction during flow ramp-down was seen and may be kinetic, but this is unconfirmed. *(result, medium)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p27): *45%-15% H2/N2 balance mixtures are investigated, where flames at high flow rates, e.g., 10 cc/s, did not extinguish, appearing quasi- steady until time out. The hydrogen flames would likely need to reach a diameter much larger than that accommodated by the experiment to extinguish radiatively.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p25): *Additionally, pure H2 only produces H2O as its radiative product, thereby isolating its radiative properties.*
7. Nitrogen-diluted H2/CH4 blends in air behaved differently with composition. 20% H2/25% CH4/55% N2 flames extinguished radiatively during expansion even at flows as low as 2 cc/s. Some showed wavy oscillation and local extinction and re-ignition before final extinction. 30% H2/15% CH4/55% N2 flames at flows up to 15 cc/s persisted with patchy extinction areas until the flow timed out. Kinetic extinction was not identified for either blend. The authors suggest the kinetic extinction radius may lie within the burner radius (about 3.2 mm for the 6.35 mm spherical burner). *(result, medium)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p27): *However, it seems that even for very small flow rates, e.g., 2 cc/s, extinction is by the radiative mechanism during flame expansion.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p27): *Radiative extinction is difficult to identify conclusively because flames with larger flow rates, e.g. 15 cc/s, seem to last, although with patchy extinction areas, until time out.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p30): *The characteristic extinction radius may be within the burner radius, precluding experimental identification.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p10): *Ultimately, the spherical burners were limited to a single diameter of 6.35 mm*
8. Replacing nitrogen with helium (about 6 times higher thermal conductivity) made ignition much harder with the same hot-wire settings. On the first helium day (20132), 25% H2/20% CH4/He into 21% O2/He, igniter power was raised cautiously and the first ignition came on the ninth test: 7 flames from 15 tests. The team switched to a thicker coil igniter tip and moved part of the matrix to ~30% O2. Even so, 13 attempts with 20% C2H4/80% He in 21% O2/He failed to ignite, and 3 cc/s of 30% C2H4/He in 21% O2/He did not ignite. Methane without hydrogen needed even more ignition energy. *(limit, high)*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p5): *The power level was slowly increased from test to test until ignition was finally achieved on the ninth test, where only seven flames were ignited of the 15 tests conducted on May 11 (20132), the first day for flames in Increment 63.*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p12): *Although 13 tests were conducted with the 21% O2/He atmosphere, ignition was not achieved.*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p12): *Without H2 in the mixture, even larger energy and power were needed to ignite the mixtures.*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p13): *The 3 cc/s case did not ignite.*
9. Helium-diluted flames had extinction limits shifted relative to nitrogen-diluted ones, and kinetic extinction was hard to isolate. Many helium flames were stopped by the 250 C burner temperature limit before self-extinction: 45% H2/He at 10 and 14 cc/s (the top of that fuel MFC's range) in 30% O2/He; 5 cc/s of 20-30% C2H4/He in 30% O2/He. The authors attribute this to helium carrying heat to the burner. Ramp-down extinctions may thus reflect burner heat loss rather than chemistry. At higher flows (6-17.5 cc/s), helium-diluted CH4, C2H4 and H2/CH4 flames expanded to apparent radiative extinction. In 17.5% O2/82.5% He, 45% H2/He flames appeared to show both radiative and kinetic extinction. *(trend, medium)*
   - `PSI-23_Reports_s-Flame 30-day report Inc 63 20201216.pdf` (p12): *For the 30% O2/H2 atmosphere, the tests produced flames at 10 and 14 cc/s (MFC limit of 1 SLMP) that expanded after ignition, but were extinguished by the automated protocol because the burner reached the 250°C temperature limit before any self-extinction could occur.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p30): *(7) The highly thermal conductive nature of He seems to affect various processes, such as ignition and heat transfer to the burner (affecting isolation of kinetic extinction), despite higher characteristic flame temperatures.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p31): *Helium-diluted hydrogen displayed radiative extinction and showed kinetic extinction for oxygen-reduced environments. Helium-diluted ethylene and methane exhibited radiative extinction.*
10. Some helium-diluted H2/CH4 flames showed an unexplained 'flash'. With 25% H2/20% CH4/He into 21% O2/He at 5-10 cc/s, and 20% H2/25% CH4/He at 17.5 cc/s, the flame seemed to disappear and then re-ignite with a flash, or to waver, before final extinction. With 20% H2/25% CH4/He at 5 and 7 cc/s, the mixture ignited but extinguished at once with almost no flame-front expansion. *(result, low)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p28): *For 5-10 cc/s, the flames seemed to disappear and 're- ignite' with a "flash" before final extinction. We are currently investigating the flash phenomenon.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p28): *For 5 cc/s and 7 cc/s, the mixture ignites but immediately extinguishes, with almost no observable flame-front expansion.*
11. The pulsating (Le > 1) instabilities that theory and simulation predict near both extinction limits were not conclusively observed, at least in the video. Wavy or oscillatory flame behaviour before extinction was common. The investigators attribute much of it to the region near the burner support tube, where fuel is lacking and heat is lost, rather than to intrinsic pulsation. PMT and radiometer records still have to be analysed for oscillations. *(null_result, medium)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p30): *However, such instabilities were not conclusively observed in the ISS tests, at least from the video images. Radiometer and PMT data will need to be examined in detail.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p31): *Many flames presented unstable behavior near the burner tube prior to extinction, likely because of lack of fuel mixture and heat loss in that region, rather than inherent pulsating instability.*
12. Flame luminosity was not a reliable indicator of flame strength. Before flight, simulations showed CH* emission from expanding flames decaying while peak temperature rose, so extinction should be judged from temperature or radiometer data rather than visible light. The flight confirmed this as a finding. Diluted hydrogen flames were barely or not at all visible to the DataCam and ops camera, and were tracked mainly by OH* (310 nm) imaging and PMTs. *(method, medium)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p30): *(8) Flame luminosity does not necessarily correspond with flame strength (or combustion intensity).*
   - `PSI-23_Science Documents_s-Flame_SRD_20100125.pdf` (p17): *In particular, Fig. 1.13 shows that the peak visible emission from CH\* decreases rapidly despit e an ever increasing flame temperature.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p18): *A critical challenge for s-Flame was in imaging the pure hydrogen and diluted hydrogen flames, which were not apparent or hardly visible to the DataCam and analog operations camera.*
13. A fuel-bottle safety error was found during the mission. The first H2/CH4 blend bottle leaked on installation (July 2019). The review showed that the H2/CH4 bottles had been over-filled: a leak into the open CIR rack volume could reach flammable or explosive limits. The safe fill pressure had been set by considering the two fuels separately rather than combining them with Le Chatelier's mixing rule. The final report states the plan to vent each H2/CH4 bottle to a safe pressure before its use. *(method, high)*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p40): *During the review of the leaked fuel bottle, it was determined that the bottles with the hydrogen/methane blends (H2/CH4) were over-filled in that the flammable and explosive limits could be reached if the fuel were to leak into the open volume of the CIR rack.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p40): *The two fuels were considered individually instead of collectively using Le Chatelier's mixing rule.*
   - `PSI-23_Reports_s_Flame_final_report_20210729.pdf` (p40): *Therefore, before their use, the plan is to vent each H2/CH4 bottle to a pressure that will be safe if a bottle leaks into the CIR free volume.*

## Fire-safety relevance

s-Flame is fundamental combustion research, not a materials or suppression test, so its fire-safety value is indirect. (1) In quiescent microgravity, a fed diffusion flame need not reach a steady state. If its fuel supply is large it keeps growing until radiative loss kills it. If the supply is small it dies from too short a residence time. This flow-controlled 'isola' is the gas-phase analogue of the low-flow and radiative quenching limits relevant to a leak or a pyrolysing material in a still cabin. Validated chemistry, transport and radiation models from these data would improve predictions of fire size and extinction in spacecraft. The gas-burner results are not material flammability limits. (2) Detection: diluted hydrogen flames were nearly invisible to colour cameras, and the investigators stress that luminosity does not track flame strength. Visual or visible-band detection of hydrogen or lean flames in a cabin could therefore miss a burning flame, whereas OH* (310 nm) UV sensing worked. (3) Prevention: the leaked and over-filled H2/CH4 bottles show that flammability of fuel mixtures leaking into an enclosed rack must be assessed with mixing rules (Le Chatelier), not per component. (4) Helium-diluted atmospheres made ignition much harder and moved extinction limits, a reminder that the inert gas is not a passive participant.

### Habitat conditions

All tests were near 1 atm. The chamber was filled to about 1 atm (101 kPa) and rose slightly with vitiation; the uncalibrated ACME transducer reads 104-110 kPa. That is close to Earth sea level (20.9% O2 at 101.3 kPa). Round 1 used ~21% and ~30% O2 in N2; round 2 used ~21%, ~30% and 17.5% O2 in He. The ~30% O2 cases match the oxygen fraction expected for Moon habitats (30% or more), but at about 1.4 times the habitat pressure (70.3 kPa or less). So the oxygen partial pressure (about 30 kPa) was higher than in such a habitat (about 21 kPa or more), and the nitrogen dilution was greater than in a reduced-pressure cabin. Reduced-pressure, elevated-O2 atmospheres such as the 100% O2 / 29.6 kPa spacesuit were not tested. Helium atmospheres are not cabin-relevant: they were chosen to change transport and Lewis number. Results transfer to exploration atmospheres only through the models they are meant to validate.

### Earth benefits

Better-validated kinetic, transport and radiation models for diffusion flames, the basis of most engines and burners. The investigators cite lean-burn engine development for higher efficiency and lower emissions, plus improved understanding of extinction, ignition in non-premixed flames and the role of diluents.

## Limitations

- Results are preliminary and largely qualitative. The final report (2021) gives extinction behaviour as flow brackets and descriptive observations. No reduced flame-radius histories, temperature profiles, extinction flow rates or model comparisons are in PSI, and no peer-reviewed paper with ISS results is listed (only conference talks and posters). Several extinction-mode attributions are explicitly 'presumed' or 'seems'.
- The porous sphere did not produce spherically symmetric flames at high flow. More gas escaped through the sintered joint to the supply tube, so flames shifted toward the tube and became ellipsoidal or even parabolic, with local quenching near the tube. Heat loss to the support tube adds further asymmetry. This limited the flows usable for radiative extinction.
- Flow-control limits. MFC ranges were often too small (e.g. a 0.1 slpm fuel MFC on 19352) or used at small fractions of full scale, where the delivered flow differed from the set point. Overshoot, undershoot and small flow perturbations showed up in the PMT signals. MFCs are calibrated for nitrogen, and the chamber-calculator estimates of chamber composition ignore gas conversion factors (about 0.6 for ethylene).
- Uncontrolled atmosphere drift. The chamber was rarely vented between tests, so O2 decreased and pressure and combustion products increased over each test day. GC samples exist, but species concentrations have not been reduced because the analysis software runs only on retired Windows versions. The ACME pressure transducer had not been calibrated in years.
- The test matrix was inconsistent. Ignition problems in round 2 forced part of the helium matrix from the planned ~21% O2 to ~30% O2, which limits planned test-to-test comparisons. The planned 25% H2/20% CH4/N2 blend was lost to a leaking bottle. The burner temperature limit (250 C) cut off many low-flow helium flames before self-extinction, confounding kinetic extinction with burner heat loss.
- Imaging losses and limits. Much of the image data on 19256 was lost (IPSU-G failure, later replaced). DataCam files were mis-formatted on 19352; both days were repeated. Hydrogen flames were invisible to the colour cameras. The two intensified cameras faced each other, so 3-D symmetry of dim flames cannot be assessed. The TFP fibre arms partly block the intensified cameras' fields of view. Radiation damage causes growing numbers of hot pixels. The DataCam's long exposures cut frame rates to about 1 fps in some tests.
- The finite chamber (about 83 L, constant volume) limits the largest flames and, through oxygen depletion, the useful test time. The SRD set a 25 s bound for a 20 cm penetration depth. Because radiative reabsorption enlarges flames at extinction, the investigators note that chamber size becomes a parameter. The acceleration environment has not been checked against SAMS data.

## Data in PSI

PSI-23 has 4,165 files (782 GB). Almost all of it is raw imagery that is not downloaded: 1,974 per-test zips (770.6 GB) and 287 MP4 ops-camera videos (9.3 GB). The zips hold DataCam HOBJ images (568 zips, 253 GB), CFI intensified TIFFs (550, 329 GB), HiBMs (283, 130 GB), LLL-UV OH* TIFFs (286, 35 GB) and ground-recorded ops video (285, 24 GB). The downloaded raw data (1,795 files, 0.88 GB) are fully usable. They comprise a 125 Hz non-imaging data CSV for 288 test points (raw voltages: MFC flows, chamber pressure, PMTs, thermocouples, radiometers; conversions in ACME-DOC-010 Rev D) and an MFC set-point CSV for each. There are also as-run script parameter files (290) and test-timing files (266), image-completeness comments (276), daily ACME and IPSU-G logs, camera metadata, and 170 raw GC chromatograms (.asc, not reduced). Reference Data holds 48 zips of TFP fibre images (one or two per test day, ten for 20142) and 4 video files, plus the interface document (twice). Documents are rich: SRD (2010), Science Concept Review, ISRD, SORD, a 30-day operations report, a 113-page final report (2021), a data-interpretation guide and the experimental procedure with script. No reduced data (flame radius vs time, extinction flow rates, temperatures) and no ISS-results journal paper are in PSI. The experimental table is an 18-row per-test-day summary (date, atmosphere, fuel bottle, flames ignited).

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Raw Data | per-test image zips: DataCam HOBJ, CFI intensified, HiBMs, LLL-UV OH*, ops-camera recordings | .zip | 1974 | 771 GB | no |
| Raw Data | ops-camera video recorded on the ground (VLC captures), one per test | .mp4 | 287 | 9.32 GB | no |
| Raw Data | 125 Hz non-imaging data and MFC set-point files per test point (288 each) | .csv | 576 | 773 MB | yes |
| Raw Data | as-run script parameter files, test-timing (_TP) files, image-completeness comments, test-point parameter text files | .txt | 946 | 1.1 MB | yes |
| Raw Data | daily ACME/IPSU-G logs, camera metadata (.mdipsug), GC chromatograms (.asc), daily test-point log spreadsheets | .log .mdipsug .asc .xlsx | 273 | 100 MB | yes |
| Reference Data | thin-filament-pyrometry fibre image zips per test day, 4 reference videos, ACME-DOC-010 Rev D software interface description (two identical copies) | .zip .mp4 .pdf | 50 | 1.12 GB | yes |
| Science Documents | SRD (2010), Science Concept Review (2008), RDR-era ISRD presentation, ISRD Rev B, SORD Rev A, non-imaging data file description, DoD sheet | .pdf | 7 | 9.8 MB | yes |
| Reports | 30-day operations report for Increment 63 and the s-Flame final report (2021) with all 30-day reports appended | .pdf | 2 | 3.5 MB | yes |
| Engineering Documents | ACME engineering implementation, ERD Rev K, CDR package, s-Flame RDR, data interpretation guide, experimental procedure, drawing zips (some PDFs have no text layer) | .pdf .zip | 29 | 190 MB | yes |
| Presentations | ACME overview talks (ASGSR 2012/2013, CSSCI 2014, AIAA 2012, IAC 2008), fact/info sheets, ISS researcher's guide, FLEX paper; general to ACME, no s-Flame ISS results | .pdf | 17 | 51 MB | yes |
| Experimental table | 18 test-day rows: test day, date, atmosphere, fuel bottle, flames ignited | .csv | 1 | 2.5 kB | yes |
| metadata | ISA-Tab metadata zip (named PSI-99 but containing the PSI-23 record) | .zip | 1 | 20 kB | yes |

Rows in the unified `tests` table: 18

## Related investigations

- [PSI-10](PSI-10-acme-flame-design.md): shared hardware
- [PSI-159](PSI-159-acme-cfi-g.md): shared hardware
- [PSI-20](PSI-20-acme-bre.md): shared hardware
- [PSI-21](PSI-21-acme-cld-flame.md): shared hardware
- [PSI-22](PSI-22-acme-e-field-flames.md): shared hardware

## Open questions

- Extract flame radius vs time (peak CH*/OH*) from the LLL-UV and CFI intensified image zips for the nitrogen-diluted ethylene and methane tests. Compare the trajectories with transient detailed-chemistry simulations with and without radiation reabsorption, which the reports say are underway.
- Use the 125 Hz MFC, PMT and burner-thermocouple traces to pin down the actual flow rate and burner temperature at each detected extinction. Classify each extinction as kinetic, radiative or burner-heat-loss, giving a quantitative extinction map (flow vs fuel fraction vs O2 vs diluent).
- Look for pulsating instability in the PMT (OH*, CH*) and radiometer time series near extinction (frequency, amplitude, growth rate), comparing N2- vs He-diluted flames as Objective C intended.
- Reduce the thin-filament pyrometry images (Reference Data fibre zips and DataCam HOBJ) to radial temperature profiles, especially for the hydrogen flames where the fibres glowed.
- Reduce the 170 GC chromatograms to chamber O2/CO2/fuel concentrations, so that test-by-test ambient O2 (vitiation) is known rather than nominal.
- Investigate the 'flash' re-ignition events seen in helium-diluted H2/CH4 flames, using synchronized PMT and intensified-camera data.
- Check the acceleration environment for each test from PIMS/SAMS archives (not in PSI) for g-jitter effects on flame symmetry.

## Dashboard ideas

- **test-day timeline** (`test_day`, `date`, `round (N2/He)`, `x_o2_nominal`, `fuel_bottle`, `flames_ignited`): The 18-row table shows how the matrix moved from N2 to He and from 21% to 30% O2, and the 276 flames per day.
- **extinction mode map** (`fuel`, `fuel_fraction`, `diluent`, `x_o2`, `flow_cc_s`, `outcome (quasi-steady / radiative ext. / kinetic ext. / burner-limit stop / no ignition)`): Places the reported flow brackets (e.g. kinetic below 1-3 cc/s, radiative at 5-10 cc/s for N2-diluted C2H4) on a dual-extinction (isola) diagram.
- **per-test time series** (`time_s`, `fuel_flow_slpm`, `PMT_OH`, `PMT_CH`, `radiometer`, `T_burner`, `pressure`): The downloaded 125 Hz _data.csv files let a user see ignition, flame growth, ramps and extinction for any of 288 test points without the image archive.
- **data availability matrix** (`test_point`, `has_data_csv`, `camera_zips (DataCam/CFI/LLL-UV/HiBMs)`, `video`, `image_completeness_comment`): Shows which tests have which imagery (and the lost 19256 / mis-formatted 19352 data) before anyone downloads 780 GB.

## Gaps and data-quality notes

- No reduced quantitative results (flame radius histories, extinction flow rates, temperatures) and no ISS-results journal paper exist in PSI; the final report lists only conference presentations with ISS results (ASGSR 2019 and 2020, Russian conferences 2019/2021, USNCM 2021 poster). A web search (NASA s-Flame page, general search) found no later peer-reviewed s-Flame ISS paper; the NASA investigation page has no results.
- Flow rates are reported only in 'cc/s' without stating whether they are standard or actual volumetric rates or whether they refer to the total fuel-mixture stream; the parameter files give slpm on a nitrogen basis. Values are kept as reported.
- Chamber pressure: the CIR chamber calculator workbook named in the data-interpretation guide (the reliable pressure/composition record) was not found among the downloaded files. The 1.03-1.09 atm range was computed from the uncalibrated ACME PTA3 channel of the 288 _data.csv files using the ACME-DOC-010 conversion and should be treated as approximate.
- Actual ambient O2 per test is unknown: only nominal ~21%/~30%/17.5% values are given; GC data are unreduced and the chamber calculator is not available.
- Data quality (experimental table CSV): the Atmosphere column reads '~21% O2 with N3/N4/N5/N6' and one fuel cell '50% C2H4 with N3' (spreadsheet auto-increment of 'N2'); row 20132 is labelled 'First round of tests with nitrogen-diluted fuel' although it was the first helium (second-round) day; row 20190 lists '35% H2 with He' while the reports say 45% H2 with He; tests.csv parses the H2/CH4 bottles 20006 and 20013 as fuel fraction 1.0 although they were diluted 55% with N2 on orbit. The 30-day report's Table 1 also mislabels the helium round as 'First round of tests, with helium-diluted fuel and oxygen'.
- Data quality: the metadata zip is named 'PSI-23_metadata_PSI-99_ACME s-Flame.zip', but PSI-99 is SAFFIRE-II; its content is the PSI-23 record. The two Reference Data PDFs 'ACME-DOC-010_D.pdf' and 'ACME-DOC-010_D Software Interface Design Description.pdf' are identical (same size and text). The 2012 FLEX paper (PSI-23_Presentations_20120015928.pdf) was previously filed under Raw Data.
- The PSI record lists only Law (PI), Tse (Co-I) and Stocker (PS); the final report also names Kurt Sacksteder as Co-I and Vladimir Gubernov as lead collaborator. The PSI record end date (2019-11-24) precedes the last test day (2020-07-08).
- Objective statements in the 30-day reports are mislabelled (objective C printed as 'A' or 'B'); content is otherwise identical to the SRD.
- Documents contain staff work contact details (e-mail, phone) and the GC raw files contain an instrument user-name header field; these were not copied. The ACME-DOC-010 interface document defines FTP login parameter fields (no actual credentials seen). No text addressed to an AI was found.
- Raw-data notes were sampled, not read in full: the _Comments.txt files record only image-download completeness (e.g. missing frames on 19256), the as-run/test-point .txt files are script parameter lists, and the daily test-point log spreadsheets hold only image counts for 20164; none contains science observations.
- Three drawing/poster PDFs (s1101mfa0100_C, s1101mfa1800_B, PS-01374 ACME poster, PS-03403 ACME on the ISS) have no text layer and were not read; none is a report.
- Most ACME presentations in PSI-23 (ASGSR 2012/2013, CSSCI 2014, AIAA 2012, IAC 2008, researcher's guide) predate the s-Flame flight and describe ACME generally; they were used only for hardware context.
- Publications pass 2026-11-15: all 44 publications listed in the PSI record were checked (35 by abstract, 2 by full text, 7 not reachable; details in data/publications/PSI-23.json). All date from 1994-2019, before the 2019-2020 flight, and none reports s-Flame ISS results. Six confirm background already in the record (2.2 s too short for steady flames; oscillation before radiative extinction in theory and low-pressure tests; luminosity not tracking flame strength; the porous-sphere configuration).
