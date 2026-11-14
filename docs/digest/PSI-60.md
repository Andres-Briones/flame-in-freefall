# PSI-60: (Computational and Experimental Analysis of SPICE Data Sets)

Yale researchers re-analysed Space Station photographs of sooty ethylene flames and ran detailed computer models to find out why flames in weightlessness make so much more soot than on Earth, concluding that the models mainly get the flame temperature wrong.

Investigators: Mitchell D. Smooke (Yale University) - Principal Investigator; Marshall B. Long (Yale University) - Co-Investigator; Daniel L. Dietrich (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Platform | Ground (computational modelling and image re-analysis) using ISS coflow flame data |
| Dates | 2019-06-05 to 2022-08-29 |
| Fuels and samples | ethylene |
| Varied | gravity level (simulated and measured): 1 g, 0 g g<br>burner configuration: Yale burner, ACME burner (ACME flame smaller)<br>soot sub-model parameters, radiation and re-absorption treatment, scattering, burner boundary conditions: sensitivity perturbations (values not available) |
| Number of tests | over 1600 raw DSLR images analysed (number of distinct flames or simulation cases not reported) |
| Fire-safety pillars | fundamental, detection |

## Question

Why do laminar diffusion flames in microgravity form so much more soot than the same flames in 1 g, and why do detailed models fail to reproduce the difference? The study aimed to extract temperature and soot volume fraction fields from SPICE images in PSI, compare them with detailed soot simulations of normal- and microgravity flames, identify which processes (soot formation and oxidation, radiative re-absorption, aggregate growth) control the discrepancy and the approach to the smoke point, and assess sensitivity to model parameters. The hypothesis was that microgravity flames are longer, more diffuse, cooler and sootier, and that imposing measured temperature fields in the simulations would reduce the mismatch between measured and predicted soot.

## Summary

This PSI-funded ground investigation (2019-2022) combined re-analysis of microgravity flame images with detailed numerical modelling of sooting, laminar, ethylene-air coflow diffusion flames. Over 1600 raw camera images from the Smoke Point In Co-flow Experiment (SPICE) were decoded into colour channels and analysed by colour-ratio pyrometry to obtain soot temperature fields; the SPICE absolute light calibration then gave soot volume fractions. A coupled flow-species-soot model, extended with radiation re-absorption and sectional aggregate formation, simulated the Yale and ACME burner flames at 1 g and 0 g. Simulations reproduced the known trends: at 0 g the flame becomes longer, broader and more diffuse, cooler, with more soot and longer residence time, but these effects were much weaker for the smaller ACME flame. Perturbing soot sub-model parameters and radiation treatment did not remove the gap between model and measurement; the authors conclude the model mispredicts the temperature field, and that imposing measured temperatures and accounting for heat loss to the burner lip should improve soot predictions. For fire safety the work bears on soot, smoke and radiation modelling of microgravity fires.

## Physics

In a coflow diffusion flame, fuel issues from a central tube into a slower annular air stream and burns where the two meet. On Earth, buoyancy accelerates the hot gases, thinning the flame and shortening the time soot particles spend in the hot fuel-rich region. In microgravity there is no buoyant acceleration, so for the same fuel flow the flame is longer and wider, gas residence times are longer, and soot particles have more time to nucleate and grow; the larger soot load radiates more heat, lowering flame temperature, which in turn slows soot oxidation and can lead to smoke release at the flame tip (the smoke point). Soot temperature can be measured without probes by colour-ratio (two-colour) pyrometry: the ratio of soot emission in two camera colour channels depends on temperature through Planck's law and the soot emissivity's wavelength dependence; with absolute intensity calibration the emission intensity then gives soot volume fraction. Accurate soot prediction therefore depends strongly on the predicted temperature field, which in turn depends on radiation losses, re-absorption and heat transfer to the burner.

$$
\frac{I_{\lambda_1}}{I_{\lambda_2}} = \frac{\varepsilon_{\lambda_1}}{\varepsilon_{\lambda_2}}\left(\frac{\lambda_2}{\lambda_1}\right)^5 \exp\!\left[\frac{C_2}{T}\left(\frac{1}{\lambda_2}-\frac{1}{\lambda_1}\right)\right]
$$

Two-colour (colour-ratio) pyrometry in the Wien limit: ratio of spectral intensities I at wavelengths lambda_1, lambda_2 (m) emitted by soot at temperature T (K); epsilon is spectral emissivity (for soot roughly proportional to 1/lambda), C_2 = 1.4388e-2 m K is the second radiation constant. Measuring the ratio in two camera colour channels gives T independent of soot amount; valid for optically thin soot, so self-absorption in heavily sooting flames biases it. In practice the camera's spectral response is integrated over each colour filter rather than at single wavelengths.

Textbook background: Standard two-colour pyrometry relation (Planck/Wien law).

$$
f_v = \frac{\lambda\, \kappa_\lambda}{6\pi E(m)}
$$

Soot volume fraction f_v (dimensionless) from the spectral absorption coefficient kappa_lambda (1/m) at wavelength lambda (m) in the Rayleigh small-particle limit, with E(m) the soot refractive-index absorption function (about 0.3-0.4 in the visible). With T known from pyrometry and an absolute intensity calibration, the emitted intensity gives kappa_lambda and thus f_v (after tomographic inversion of line-of-sight images for an axisymmetric flame).

Textbook background: Rayleigh-limit soot absorption relation, textbook background.

## Method

### Apparatus

No new hardware. Experimental input: raw Nikon NEF (DSLR) images of SPICE coflow flames recorded on the ISS, decoded into three colour channels, plus the SPICE absolute light calibration; laboratory flames on the Yale coflow burner. Computational tool: a coupled flow-species-soot solver for axisymmetric laminar coflow flames (Yale group), modified to include radiation re-absorption and a discrete-sectional soot aggregate model, run for both the Yale and ACME burner geometries at 1 g and 0 g.

### Fuels and samples

- ethylene (in air) (gas, laminar coflow jet diffusion flame)

### Procedure

(1) Decode over 1600 raw DSLR images from SPICE into colour channels and apply colour-ratio pyrometry to obtain soot temperature fields; (2) use the SPICE absolute light calibration to convert emission to soot volume fraction; (3) simulate the Yale and ACME burner flames at 1 g and 0 g with the coupled flow-species-soot model; (4) compare computed and measured temperature and soot fields; (5) perturb soot evolution parameters and test the effects of radiation, re-absorption, scattering, boundary conditions and heat transfer to the burner, to identify the cause of the discrepancies.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| gravity level (simulated and measured) | 1 g, 0 g | g |
| burner configuration | Yale burner, ACME burner (ACME flame smaller) |  |
| soot sub-model parameters, radiation and re-absorption treatment, scattering, burner boundary conditions | sensitivity perturbations (values not available) |  |

Held constant:

- fuel/oxidiser: ethylene fuel, air coflow

Number of tests: over 1600 raw DSLR images analysed (number of distinct flames or simulation cases not reported)

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| soot temperature field | colour-ratio pyrometry of raw DSLR (NEF) images | derived |
| soot volume fraction field | DSLR emission with SPICE absolute light calibration | derived |
| computed temperature, species, soot volume fraction and aggregate fields at 1 g and 0 g | coupled flow-species-soot simulation with sectional aggregate model and radiation re-absorption | derived |

## Findings

1. Simulations of both burner configurations reproduce the established microgravity trends for sooting ethylene-air coflow flames: at 0 g the flame is longer, broader and more diffuse, temperatures are lower, and soot levels and gas residence times are higher than at 1 g. No numerical values were available in the sources read. *(trend, high)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *Computed simulations for both configurations under 1 g and 0 g conditions support previous experimental and modeling conclusions that at 0 g, the flame is lengthened, becomes broader and more diffuse, temperatures decrease and soot levels and gas residence times increase.*
2. For the smaller ACME burner flame, the gravity effects (lengthening, cooling, extra soot) were significantly diminished compared with the Yale burner flame, so flame size matters when transferring 1 g soot behaviour to microgravity. *(result, high)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *However, in the case of the smaller ACME flame, these effects are significantly diminished.*
3. Perturbing soot-evolution model parameters and the treatment of radiation and its re-absorption did not resolve the model-measurement discrepancy; the investigators conclude that the model most likely mispredicts the thermal field, and that imposing measured temperatures would give more accurate soot fields. *(result, medium)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *The results of the study indicate that it is likely that the model inadequately predicts the thermal field and the use of experimental temperatures imposed onto the solution would provide more accurate simulations of the soot field*
   - PSI record field `hypothesis`
4. Heat transfer from the flame to the burner lip was identified as a likely source of error: it can change the flame's boundary conditions and hence the computed solution, so burner thermal coupling should be included in models of these flames. *(method, medium)*
   - <https://doi.org/10.1080/00102202.2022.2041621>: *heat transfer to the burner lip could alter the boundary conditions of the flames and hence the subsequent solutions.*
5. Supporting 1 g evidence from the same group (Kempema, Dobbins, Long, Smooke 2021; not listed in the PSI record): imposing a measured 2-D temperature field on a 40% ethylene flame on the Yale burner moved the computed peak soot from the flame wings (surface-growth dominated) to the centreline (inception dominated), matching experimental soot distributions far better than the unconstrained solution. *(method, medium)*
   - <https://doi.org/10.1016/j.proci.2020.06.034>: *Similarly, the location of peak soot volume fraction migrates from along the flame wings in the unconstrained calculation, where soot surface growth processes dominate, to the centerline in the constrained case, where soot inception is the dominant condensed-phase formation mechanism.*
6. SPICE consumer-camera images can be turned into quantitative soot diagnostics: decoding the raw NEF files (rather than processed JPEGs) into three colour channels allowed colour-ratio pyrometry for soot temperature, and SPICE's absolute light calibration allowed soot volume fraction to be computed, over more than 1600 images. *(method, medium)*
   - PSI record field `approach`
   - PSI record field `objective`

## Fire-safety relevance

Soot governs flame radiation, smoke production and what smoke detectors see. This work shows that microgravity flames are sootier and cooler, and that current soot models fail mainly because they mispredict temperature, so predictions of radiant heat flux and smoke yield for spacecraft fires should be treated with caution until thermal fields are validated. The PSI record claims support for safer fire detection and suppression, but no detection- or suppression-specific result appears in the sources read. Transferability is limited: the flames are small laminar ethylene gas jets, not burning cabin materials, and the paper reports that a smaller flame (ACME) showed much weaker gravity effects, so size scaling matters.

### Habitat conditions

The flames burned ethylene in air; the ambient oxygen fraction and pressure of the ISS runs analysed are not stated in the sources read, so no comparison with exploration atmospheres (e.g. 30% or more O2 at 70.3 kPa or less for a Moon habitat) can be made. If the runs were in normal air near sea-level pressure, they correspond to the Earth sea-level reference rather than enriched-oxygen habitats.

### Earth benefits

Better soot and radiation models for laminar flames feed into predicting pollutant emissions and designing cleaner, more efficient combustion systems.

## Limitations

- Only the abstract of the single listed publication could be read; quantitative results (temperatures, soot volume fractions, flame lengths, size of model-experiment discrepancies) are not available here.
- The diagnosis (temperature field mispredicted) is a hypothesis supported by sensitivity runs, not demonstrated for the microgravity flames by a constrained-temperature 0 g simulation in the sources read.
- Colour-ratio pyrometry is line-of-sight and assumes optically thin soot; in heavily sooting microgravity flames self-absorption can bias temperature and soot volume fraction, which is why re-absorption was examined.

## Data in PSI

PSI holds only an ISA-Tab metadata zip (7.7 kB) that repeats the record text; its study file has a single placeholder row. No processed temperature or soot fields, simulation outputs or analysis code were deposited, so nothing in this record can be re-derived from PSI-60 itself. The source images are in the SPICE investigation (PSI-107).

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| metadata | ISA-Tab investigation and study files (i_Investigation.txt, s_PSI-60.txt with 'Do not use this' placeholder rows) | .zip .txt | 1 | 7.7 kB | yes |

## Related investigations

- [PSI-107](PSI-107-spice.md): ground re-analysis
- [PSI-21](PSI-21-acme-cld-flame.md): ground re-analysis

## Open questions

- Deposit the derived SPICE soot temperature and volume fraction fields in PSI so other modellers can use them.
- Run constrained-temperature (measured T imposed) simulations of the 0 g SPICE and ACME flames to test whether the 1 g improvement carries over.
- Relate the derived soot fields to the SPICE smoke-point measurements (PSI-107) to test smoke-point models for microgravity.

## Dashboard ideas

- **1 g vs 0 g flame comparison** (`burner`, `gravity`, `flame_length`, `peak_T_K`, `peak_fv`): Core result (longer, cooler, sootier at 0 g; smaller effect for ACME), but values must come from the paper, not PSI.
- **linked investigations** (`accession`, `relation`): Points users from this metadata-only record to the SPICE (PSI-107) image data it analysed.

## Gaps and data-quality notes

- PSI-60 holds only a metadata zip; no derived data, images or code. Findings rest on the PSI record text and one publication abstract (OpenAlex), plus a related Proc. Combust. Inst. 38 (2021) abstract (Semantic Scholar) by the same group that is not listed in the record.
- Data-source ambiguity: the record title and objective say SPICE (PSI-107) data, but the listed paper's abstract describes Yale and ACME burner configurations with ISS experiments, and NASA's ACME publication list (www1.grc.nasa.gov/wp-content/uploads/ACME-publications-20230830.pdf) files this paper under 'Coflow Laminar Diffusion Flame (CLD Flame) - Includes ISS results' (PSI-21). Which ISS data set(s) supplied the microgravity images in the paper could not be confirmed.
- Full text of 10.1080/00102202.2022.2041621 (Taylor & Francis) was not accessible; NTRS lists it only as an accepted manuscript with no download (NTRS 27530189361808). No Yale thesis by R. R. Dobbins was found.
- Ambient O2 fraction, pressure, fuel flow rates and coflow velocities of the analysed flames are not given in the record or the abstract.
- The record's statement that the hypothesis anticipated reduced discrepancy with imposed temperatures is consistent with the paper's conclusion but the paper (abstract) proposes it rather than demonstrating it for 0 g.
