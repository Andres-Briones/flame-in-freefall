# PSI-106: SLICE (Structure and Liftoff In Combustion Experiment)

Astronauts on the Space Station photographed small gas flames burning from a tube into a gentle stream of air, to see how flames lift off, hold on and make soot without gravity and to provide test cases for computer models of flames.

Investigators: Marshall B. Long (Yale University) - Principal Investigator; Mitchell D. Smooke (Yale University) - Co-Investigator; Fumiaki Takahashi (Case Western Reserve University) - Co-Investigator; Dennis P. Stocker (NASA Glenn Research Center) - Project Scientist (listed as Co-I in NASA papers)

## At a glance

| | |
|---|---|
| Setting | ISS · MSG |
| Module note | No SLICE flight document in hand names the ISS module (tests 9 Feb to 23 Mar 2012). The April 2010 SLICE/BASS design review planned to measure cabin pressure 'in the Columbus module'; the BASS-II summary report (2021) places the MSG in the Destiny Lab for the 2014-2016 BASS-II tests. |
| Platform | International Space Station (ISS), Microgravity Science Glovebox; tests 9 Feb to 23 Mar 2012 (module not stated by the sources in hand: see location.module_note) |
| Facility | Microgravity Science Glovebox (MSG) |
| Dates | 2012-02-09 to 2012-03-23 |
| Fuels and samples | methane; ethylene; ethane; propane |
| Varied | fuel and fuel dilution: CH4 mole fraction 0.4, 0.7, 1.0; C2H4 0.2, 1.0; C2H6 1.0 (balance N2) mole fraction in fuel stream<br>nozzle inner diameter: 0.41, 0.77, 1.59, 2.14, 3.23 mm<br>mean fuel jet velocity: up to 320 (published methane subsets 17-90) cm/s<br>air coflow velocity: about 15-70 cm/s |
| Number of tests | 12 |
| Fire-safety pillars | fundamental |

## Question

SLICE aimed to understand the structure and stability of laminar non-premixed (diffusion) flames without buoyancy. Specific aims were: what stabilises the flame base, particularly when it lifts off the nozzle; the lift-off velocity limits for different fuels and nozzle diameters; how nitrogen dilution of the fuel affects soot and stability; and how microgravity changes flame length and radiative loss compared with 1 g. It also aimed to provide a microgravity data set for validating numerical models of flame structure, soot and radiation. The hypothesis was that burner diameter, coflow velocity and fuel composition strongly influence flame structure and stability in microgravity, and that these flames differ fundamentally from 1-g flames. Before SLICE, no direct experiment-computation comparison existed for such microgravity flames. SLICE was also a precursor to refine the test matrix of ACME's CLD Flame experiment.

## Summary

SLICE ran laminar coflow jet diffusion flames in the ISS Microgravity Science Glovebox on 12 test days between 9 February and 23 March 2012. Fuel issued from interchangeable nozzles (0.41-3.23 mm inner diameter) into fan-driven air in a 76 mm square duct. Fuels were methane (100, 70 and 40% in N2), ethylene (100 and 20%) and ethane, at about 21% O2 and 100 kPa. The crew set fuel flow and coflow by hand. A colour DSLR recorded more than 4,000 images, used for flame shape, lift-off height, soot temperature (colour-ratio pyrometry), soot volume fraction and CH* chemiluminescence. A matching flight-hardware replica gave 1-g counterparts. For a 100% methane flame (3.23 mm nozzle, 46 cm/s fuel, 18 cm/s coflow), microgravity raised the peak soot volume fraction four- to eightfold and lowered the peak soot temperature by about 200 K. For nitrogen-diluted methane, flame length scaled with methane mass flow, and microgravity flames were on average 28% longer. The results benchmark combustion models; relevance to spacecraft fire safety is indirect (sooting and radiation of non-buoyant flames).

## Physics

A coflow jet diffusion flame burns at the interface between a central fuel jet and a surrounding air stream. Fuel and oxygen meet by diffusion, and the flame sits roughly where they are in stoichiometric proportion. On Earth the hot products are strongly buoyant. They accelerate (computed peak axial velocity about 200 cm/s in the 1-g SLICE methane case), which narrows the flame by drawing gas radially inward and shortens residence times. Without gravity, velocities stay near the inlet values (about 90 cm/s peak in the same case). The flame becomes longer and wider and more diffusion-controlled, and fuel spends longer in hot, fuel-rich regions. Soot therefore has more time to grow, and more soot means more radiative loss and a cooler flame. The flame base can be attached to the nozzle rim or, at higher jet or coflow speeds or with diluted fuel, lifted downstream. A lifted base is a partially premixed edge (triple) flame whose position is set by a balance between local flow speed and flame propagation speed. Too much flow blows the flame out. Lifted, non-sooting flames are especially good model test cases because heat loss to the burner is removed.

$$
L_f \propto \dot{m}_F
$$

Laminar jet diffusion flame length scaling (Roper). The luminous or stoichiometric flame length $L_f$ (m) is proportional to the fuel-stream mass flow rate $\dot{m}_F$ (kg/s) and independent of nozzle diameter and jet velocity at fixed flow rate. The full Roper form is $L_f \propto \dot{m}_F/(\rho D\,\ln(1+1/S))$, with $\rho D$ the density-diffusivity product (kg/m s) and $S$ the stoichiometric air-to-fuel-stream mass ratio. This mass-flow form approximates Roper's original, which uses volumetric flow and a molar stoichiometric ratio; the proportionality is the same. It applies to buoyant and non-buoyant laminar flames with modest coflow. The prefactor differs with gravity: SLICE microgravity flames were longer. In SLICE the measured log-log slope of modified flame length (lift-off height subtracted) against fuel-mixture mass flow rate was 1.07 in microgravity and 1.03 in 1 g.

Textbook background: Roper (1977) laminar jet flame length correlation.
<https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *In 1g, the average slopes of the computed and measured ˜Lf values with respect to ˙mFM on a log-log scale are 1.02 and 1.03; while in μg, the corresponding values are 1.12 and 1.07.*

$$
\frac{S_1}{S_2} = \frac{\int \eta_1(\lambda)\,\varepsilon(\lambda)\,I_b(\lambda,T)\,d\lambda}{\int \eta_2(\lambda)\,\varepsilon(\lambda)\,I_b(\lambda,T)\,d\lambda}
$$

Colour-ratio (two-colour) pyrometry used to get soot temperature from the DSLR images. $S_1$ and $S_2$ are signals in two colour channels (for example red and green); $\eta_i(\lambda)$ is the measured spectral response of each channel including the BG-7 filter; $\varepsilon(\lambda) \propto \lambda^{-\alpha}$ is the soot spectral emissivity (dispersion exponent $\alpha$; literature values run 0.5-2.2 and SLICE assumed $\alpha = 1.38$ for all flames); $I_b$ is Planck's blackbody intensity at wavelength $\lambda$ and temperature $T$ (K). The measured ratio is inverted for $T$ through a lookup table. Soot volume fraction then follows from the absolute intensity, calibrated against a flame-heated S-type thermocouple. Valid for optically thin soot after Abel inversion of the line-of-sight images.

Textbook background: Standard two-colour soot pyrometry relation; the SLICE paper's Eq. (1) is not quoted because it is garbled in the extracted text.
<https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *A color-ratio pyrometry approach based on a color DSLR camera, which was developed and discussed in [13, 14], was used in this study.*

## Method

### Apparatus

The hardware, shared with SPICE and later used for BASS, was based on the ELF experiment flown on STS-87. A DC fan at the upstream end drew cabin air through a ceramic honeycomb and wire mesh into a 76 mm x 76 mm (rounded-corner) square duct, 174 mm tall. Coflow speed was set by fan voltage and referenced by an omnidirectional hot-sphere anemometer. A central fuel tube took five threaded nozzles of 0.41, 0.77, 1.59, 2.14 and 3.23 mm inner diameter. A mass flow controller, manually adjustable over 0-500 sccm (N2-equivalent), metered the fuel. Instruments were a Nikon D300s DSLR with a 2 mm BG-7 filter, an analog colour video camera with fuel flow, fan setting, anemometer reading and timer overlaid, and a thermopile radiometer with manual gain. A replica (engineering/training unit) at Yale provided 1-g tests and hot-wire coflow profiles. The coflow near the nozzle was not perfectly symmetric.

### Fuels and samples

- methane (CH4): 100%, 70% and 40% in N2 (gas, round coflow jet, nozzles 0.41-3.23 mm ID)
- ethylene (C2H4): 20% in N2, and 100% (gas, round coflow jet)
- ethane (C2H6), 100% (gas, round coflow jet)
- propane (C3H8), 100% - run on the last day as SPICE testing, not SLICE (gas, round coflow jet)

### Procedure

The crew installed a nozzle, ignited the flame manually, and set fuel flow (mass flow controller) and coflow (fan voltage) by hand. They then took still images in bracketed exposures so that at least one was unsaturated. The flow conditions for each still were recovered by matching the image EXIF time to the video, whose data overlay was read automatically by optical character recognition. Calibration runs included coflow/fan calibrations and pyrometry calibrations; an S-type thermocouple heated in the flame served as an absolute light source for soot volume fraction. Testing ran on 12 days from 9 Feb to 23 Mar 2012, one fuel bottle per day; on most days the bottle was emptied. Over the campaign more than 4,000 high-resolution images were taken. The same conditions were repeated in 1 g at Yale on the replica hardware, and flames were simulated with a vorticity-velocity (MC-Smooth) code with sectional soot model.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| fuel and fuel dilution | CH4 mole fraction 0.4, 0.7, 1.0; C2H4 0.2, 1.0; C2H6 1.0 (balance N2) | mole fraction in fuel stream |
| nozzle inner diameter | 0.41, 0.77, 1.59, 2.14, 3.23 | mm |
| mean fuel jet velocity | up to 320 (published methane subsets 17-90) | cm/s |
| air coflow velocity | about 15-70 | cm/s |

Held constant:

- oxidiser / ambient: ISS cabin air drawn through the duct, about 21% O2 (balance N2), about 100 kPa
- duct geometry: 76 mm square, 174 mm tall

Number of tests: 12

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame shape and size (luminous length, radius) and lift-off height | Nikon D300s DSLR images | derived |
| soot temperature | colour-ratio pyrometry on DSLR images (BG-7 filter), Abel-inverted | derived |
| soot volume fraction | absolute light calibration with a flame-heated S-type thermocouple | derived |
| CH* chemiluminescence concentration (blue channel near 431 nm) | spectrally characterised DSLR, Abel deconvolution, absolute calibration | derived |
| fuel flow, coflow fan voltage, coflow reference velocity, time | mass flow controller, hot-sphere anemometer, video overlay | direct |
| flame radiation | thermopile radiometer (manual gain) | direct |

## Findings

1. Microgravity made a sooting methane flame larger, sootier and cooler. For a 100% CH4 flame on the 3.23 mm nozzle (mean fuel velocity 46 cm/s, nominal coflow 18 cm/s), the microgravity flame was taller and wider than its 1-g counterpart. Its peak soot volume fraction was about 4 to 8 times higher (about 8 at nominal values), and its peak soot temperature about 200 K lower because of the larger radiative loss. *(result, high)*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *In μ g, a taller and wider flame was produced and the peak soot volume fraction increased by a factor of ~ 8.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *The peak soot temperature in μ g is shown to be ~ 200 K lower than its 1 g counterpart.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *A 100% CH 4 flame using 3.23 mm ID nozzle with average fuel velocity of 46 cm/s and nominal air coflow of 18 cm/s was measured at 1 g and μ g.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *the microgravity flames were found to be sootier than normal gravity flames by a factor of approximately 4 to 8 in terms of the peak soot volume fraction*
2. Soot moved from the centreline in 1 g to the flame wings in microgravity, which the investigators interpret as a change from inception-dominated to surface-growth-dominated soot formation. Computed peak axial velocity fell from about 200 cm/s (1 g, far downstream) to about 90 cm/s (microgravity, near the nozzle), giving longer residence times. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *From 1 g to μ g, the peak of soot volume fraction was also redistributed from the flame centerline to the wings.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *The soot growth mode is believed to change from an inception-dominated mode to a surface-growth-dominated mode [28].*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *Due to the buoyancy effect, the hot flow under 1 g is accelerated and the maximum velocity is up to ~ 200 cm/s at the far downstream location, while the μ g maximum velocity is only ~ 90 cm/s at the upstream location around the tip of the burner given the parabolic fuel velocity profile.*
3. The model predicted flame shape and soot location but not the microgravity soot increase. The sectional soot model reproduced the 1-g to microgravity change in flame shape and the shift of soot to the wings. It gave the right order of magnitude for 1-g soot but did not capture the eightfold rise in microgravity. The investigators suspect the optically thin radiation assumption (no reabsorption). *(result, high)*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *However, the computation does not capture the dramatic increase in soot volume fraction from 1 g to μ g.*
   - <https://ntrs.nasa.gov/api/citations/20140017780/downloads/20140017780.pdf>: *It should be noted that the current computational model uses an optically thin radiation assumption that does not account for radiation reabsorption.*
4. Flame length scaled with fuel flow and was longer in microgravity. For N2-diluted methane flames (CH4 fraction 0.4-1.0, mean fuel velocity 23-90 cm/s), the modified flame length (luminous length minus lift-off height) was proportional to fuel-mixture mass flow. Measured log-log slopes were 1.07 in microgravity and 1.03 in 1 g. Microgravity flames were on average 28% longer (22% computed), and the gap widened with flow rate. Computed and measured lengths agreed within 15%. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *In 1g, the average slopes of the computed and measured ˜Lf values with respect to ˙mFM on a log-log scale are 1.02 and 1.03; while in μg, the corresponding values are 1.12 and 1.07.*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *with computed and measured nonbuoyant ﬂames 22% and 28% longer, on average, and the diﬀerence in ˜Lf increases as ˙mFM increases.*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *where the diﬀerence between computed and mea- sured ˜Lf is always less than 15%.*
5. Methane flow controlled flame shape; dilution and velocity mattered less. Flame shape (length and radius) was set mainly by the methane mass flow rate. With shape normalised by methane flow, the effect of N2 dilution was negligible and fuel-velocity effects were secondary. Buoyancy narrows the 1-g flame by drawing gas radially inward near the flame front. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20150002322>: *the effect of fuel dilution on flame shape (i.e., flame length and flame radius) is negligible when the flame shape is normalized by the methane flow rate.*
   - <https://ntrs.nasa.gov/api/citations/20150002322>: *(2) Buoyancy-induced reduction of the flame radius through radially inward convection near the flame front is demonstrated.*
   - <https://ntrs.nasa.gov/api/citations/20150002322>: *(3) Buoyant and nonbuoyant flame structure is mainly controlled by the fuel mass flow rate, and the effects from fuel dilution and inlet velocity are secondary.*
6. Lift-off depended on gravity and dilution. At the low coflow of the published methane subset, only the 40% CH4 flame in 1 g was lifted; the corresponding microgravity flames and all other flames stayed attached. The full data set spans lifted, non-sooting flames to attached, heavily sooting flames, from weak near-extinction flames to strong ones. It supports study of lift-off and blowout, but quantitative lift-off velocity limits were not found in the sources reached. *(result, medium)*
   - <https://ntrs.nasa.gov/api/citations/20150002322/downloads/20150002322.pdf>: *Since the coﬂow velocity is relatively small in this study, only the 40% CH4 ﬂame in 1g is lifted and all other ﬂames are attached.*
   - <https://ntrs.nasa.gov/api/citations/20140017780>: *This data covers a range of conditions from weak flames near extinction to strong, highly sooting flames, and enabled the study of gravitational effects on phenomena such as liftoff, blowout and soot formation.*
7. CH* rose with coflow in microgravity and tracked total heat release. In soot-free, N2-diluted methane flames in microgravity, peak CH* concentration rose with coflow velocity but depended only weakly on fuel velocity; attached 1-g flames followed the same trend at different peak values. Integrated CH* emission scaled with the computed total heat release rate, but the 2-D CH* distribution was not a good marker of local heat release. *(trend, high)*
   - <https://ntrs.nasa.gov/api/citations/20160012298>: *Results show that, in microgravity, the maximum flame CH\* concentration increases with the coflow velocity, but it is weakly dependent on the fuel velocity; normal gravity flames, if not lifted, tend to follow the same trend, albeit with different peak concentrations.*
   - <https://ntrs.nasa.gov/api/citations/20160012298>: *it is shown that the integrated CH\* emission scales proportionally to the computed total heat release rate; the two-dimensional CH\* spatial distribution, however, does not appear to be a good marker for the local heat release rate.*
8. The camera-based diagnostics worked with minimal instrumentation. With only a consumer DSLR, soot temperature and volume fraction were obtained in orbit by colour-ratio pyrometry with a flame-heated thermocouple calibration. Test conditions were recovered automatically from the video overlay by optical character recognition. This approach fed into the design of the ACME CLD Flame experiment. *(method, high)*
   - <https://ntrs.nasa.gov/api/citations/20140009169/downloads/20140009169.pdf>: *Despite the limited instrumentation, py rometric measurements were made in 2012 of the soot temperature and volume fraction using the innovative techniques discussed in [23-24].*
   - <https://ntrs.nasa.gov/api/citations/20140009169/downloads/20140009169.pdf>: *The SLICE experiment was conducted as a precursor to ACME’s CLD Flame experiment, in order to maximize its science, e.g., through refinement of the test matrix.*

## Fire-safety relevance

SLICE is a fundamental combustion experiment with a fixed gas-jet burner, not a material flammability test, so it gives no material limits or spread rates. Its fire-safety value is indirect. It shows that, at the same fuel supply, non-buoyant flames are larger, longer-lived in residence time, much sootier (about 8x) and cooler than in 1 g. This bears on how much radiation and smoke a spacecraft fire may produce, and on detector design (larger soot loads and particles). It also gives validated test cases for the soot and radiation models used to predict microgravity fire behaviour. The record's research impacts mention fire safety only in general terms.

### Habitat conditions

Flames burned in cabin air at about 21% O2 and about 100 kPa, essentially the Earth sea-level atmosphere (20.9% O2, 101.3 kPa). No oxygen-enriched or reduced-pressure atmosphere was used, so the results do not cover the proposed Moon-habitat atmosphere (30% O2 or more at 70.3 kPa or less). The successor ACME experiments in the Combustion Integrated Rack can vary these conditions; for example CFI-G used up to 85% O2. Coflow speeds of about 15-70 cm/s bracket typical cabin ventilation speeds.

### Earth benefits

The record expects improved numerical models of flame behaviour and soot formation to help design cleaner, more efficient engines and industrial burners with lower soot emissions. The SLICE data serve as a microgravity test case for model development.

## Limitations

- Gas-jet burner flames with prescribed fuel flow; they do not represent pyrolysing solids, flame spread or material flammability limits.
- Manually operated, exploratory hardware with limited instrumentation (one still camera, video, one radiometer). Flow conditions were set by hand and recovered after the fact from video overlay.
- Coflow near the nozzle was not perfectly symmetric, and flight and replica hardware may differ in velocity-profile details. This adds uncertainty to the 1-g versus microgravity and the experiment versus model comparisons.
- Only one atmosphere (cabin air at about 100 kPa) was tested.
- PSI holds no images or per-flame conditions, so none of the results can be checked or extended from PSI. Published analyses cover mainly methane subsets; results for ethylene and ethane flames and the lift-off and blowout limits were not found.

## Data in PSI

PSI holds only a 12-row table of test dates and fuel bottles, with notes on calibration runs, plus an ISA-Tab metadata zip that repeats the record text. Images, video, radiometer data and per-flame conditions are not in PSI: no nozzle, fuel velocity, coflow, lift-off height or outcome is listed. The record's totalFileSize (72.9 GB) suggests the image set exists on the PSI server but was not listed for download. The table can only give the campaign timeline and fuel coverage.

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| Experimental table | test dates and fuel bottle per day, with calibration notes (12 rows) | .csv | 1 | 730 B | yes |
| metadata | ISA-Tab investigation/study files (zip named after PSI-174) | .zip .txt | 1 | 8.7 kB | yes |

Rows in the unified `tests` table: 12

## Related investigations

- [PSI-107](PSI-107-spice.md): shared hardware
- [PSI-26](PSI-26-bass.md): shared hardware
- [PSI-21](PSI-21-acme-cld-flame.md): follow-on

## Open questions

- If the 72.9 GB image set can be obtained, extract lift-off height versus jet and coflow velocity for each fuel and nozzle to build the lift-off and blowout maps that were objective 2 but are not published in the sources reached.
- Compare the 20% and 100% ethylene and the 100% ethane flames with the methane results (soot, length, radiation); only methane analyses were found.
- Use the radiometer record (in the video overlay) to quantify radiative loss fraction versus soot loading in 1 g and microgravity (objective 4).
- Reconcile '13 testing experiments' (record) with the 12 test days in the table.

## Dashboard ideas

- **campaign timeline** (`date`, `fuel`, `fuel_fraction`, `notes`): The only data PSI holds: 12 test days showing fuel coverage and calibration runs.
- **1-g versus microgravity flame comparison** (`fuel`, `nozzle_mm`, `fuel_velocity_cm_s`, `coflow_cm_s`, `flame_length_cm`, `peak_soot_fv`, `peak_soot_T_K`): Headline results (8x soot, 200 K cooler, 28% longer); values come from publications, not PSI.

## Gaps and data-quality notes

- PSI has only the experimental table (date and fuel) and a metadata zip; no documents, images or per-flame data. All results come from the record text and external NASA NTRS papers and presentations.
- PSI record has no investigationStartDate/EndDate, experimentHardware or funding fields. Dates were taken from the table (first and last test day).
- The record says '13 testing experiments'; the table has 12 test days. The last row is labelled 'SPICE testing with 100% C3H8 and then 100% C2H4', so that day mixes SPICE and SLICE. tests.csv labels it fuel 'propane/ethylene' with fuel_raw only '100% C2H4' because the propane text sits in the Test Date cell. Several Test Date cells carry trailing text ('SLICE testing with') that belongs to the Fuel column.
- Ethane (100% C2H6, 2012-03-09) is in the table but not in any publication's fuel list.
- Objective 2 (lift-off velocity limits) and objective 4 (radiative heat loss) have no quantitative results in the sources reached.
- Full texts of the Elsevier papers (Proc. Combust. Inst. 35, Combust. Flame 2016) were not read. NTRS preprints/abstracts were used instead (20140017780, 20150002322, 20150011070, 20160012298/20160010264, 20140009169). Semantic Scholar has no abstracts for three of the DOIs. The Dobbins et al. 2022 abstract covers ethylene flames on 'Yale and ACME' burners; it is unclear whether its microgravity data are from SLICE, so it was not used.
- Record totalFileSize (72,914,598,688 bytes, about 72.9 GB) does not match the two files listed (about 9.5 kB). The metadata zip is named after PSI-174.
- Metadata contains investigator e-mail addresses; not copied. No text addressed to an AI was found.
- Correction (Publications pass 2026-11-15): findings[0] previously read "Its peak soot volume fraction was about 8 times higher" and the summary "about eightfold". The same paper's conclusions bound the increase at about 4 to 8 times, allowing for uncertainty in the soot dispersion exponent and temperature (NTRS 20140017780, Conclusions); 8 is the upper value.
