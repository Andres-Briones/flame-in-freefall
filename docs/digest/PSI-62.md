# PSI-62: (Concurrent Flame Spread Modeling using Flamelet Generated Manifolds in Microgravity with Comparison to BASS Experiments using Two-Color Tomography)

University at Buffalo researchers built and tested fast computer models of flames spreading over solid fuels in weightlessness, checking them against Space Station burning tests, as a step toward predicting which spacecraft materials can burn at which oxygen levels and air speeds.

Investigators: Paul E. DesJardin (University at Buffalo; PSI lists 'New York University, Buffalo') - Principal Investigator; David L. Urban (NASA Glenn Research Center) - Project Scientist

## At a glance

| | |
|---|---|
| Platform | Ground (numerical modelling and image analysis) using ISS BASS / BASS-II data |
| Dates | 2019-05-01 to 2021-04-30 |
| Fuels and samples | PMMA; wax |
| Varied | far-field oxygen level (2-D model vs BASS): range of BASS oxygen levels (values not available) mole fraction<br>flame strain (stretch) rate (flammability maps): low-strain radiative extinction to high-strain blowoff (values not available) 1/s<br>geometry: flat sheet, sphere, rod (PMMA), wax cylinder; planar and spherical 1-D models<br>benchmark: BASS-II PMMA rod flow speed and oxygen (experimental data used): 24 concurrent-flow rod tests; blowoff and quenching limits at several oxygen concentrations |
| Fire-safety pillars | prevention, fundamental |

## Question

Can a reduced-chemistry approach, the (unsteady, radiative) flamelet generated manifold, reproduce flame spread over solid fuels in microgravity with enough fidelity to predict flammability limits of spacecraft materials? Concurrent and opposed flame spread over solids is hard to model because heat transfer, mass transport and chemistry are tightly coupled near the solid-gas interface, and conventional hybrid turbulence/chemistry models are inconsistent and miss intermediate reaction pathways. The hypothesis was that the unsteady FGM approach, coupling near-wall thermal, mass transport and chemical processes with the far-field flow, could reproduce microgravity flame spread including the 'Goldilocks' flammability zone (burning only within an intermediate range of flow speed) reported by Olson and Ferkul for BASS-II PMMA rods. The long-term aim was a tool to predict flammability limits and to serve as a subgrid model in large-eddy simulations of spacecraft fires.

## Summary

This PSI-funded ground investigation (2019-2021) developed flamelet generated manifold (FGM) models for flames spreading over solid fuels in microgravity, using the ISS Burning and Suppression of Solids experiments (BASS and BASS-II) as benchmarks. An FGM tabulates detailed flame chemistry from simple one-dimensional flame solutions so that multidimensional simulations need only a few transported variables. The team built a two-dimensional flame-spread model with multi-step chemistry and fully coupled radiation, validated it against BASS data over a range of oxygen levels, and then built coupled radiative FGMs from one-dimensional flames with a quasi-coupled fuel surface boundary, which proved critical to capturing how mixture fraction varies along the fuel surface. The manifolds reproduced the chemical states in most of the flow but differed near the flame attachment point because of flame-wall interaction and flame curvature. An analytical thin-flame theory captured the low-strain radiative extinction branch of the U-shaped oxygen-versus-strain flammability map and agreed qualitatively with BASS-II PMMA rod data. The aim is to screen spacecraft materials' flammability limits numerically.

## Physics

When a solid burns, heat from the gas-phase flame pyrolyses the surface, and the fuel vapour feeds the flame; flame spread is the advance of this coupled process over unburnt material. In microgravity there is no buoyant flow, so the only flow is what ventilation imposes, often a few cm/s. The flammability of a solid then depends on oxygen and on the flow (expressed as a stretch or strain rate): at high flow the residence time is too short and the flame blows off (a Damkohler-number limit), while at very low flow the flame is weak, radiative losses from the flame and the hot surface dominate, and it quenches. Plotting minimum oxygen versus strain gives a U-shaped boundary whose minimum is the lowest oxygen at which the material can burn; in microgravity this minimum can lie below the 1 g value because buoyancy always imposes a relatively high strain on Earth. Flamelet models assume the local flame structure resembles a simple 1-D flame, so the chemistry can be pre-computed and tabulated against a few variables (mixture fraction, progress variable, and here enthalpy to represent radiative loss).

$$
Da = \frac{\tau_{flow}}{\tau_{chem}} \propto \frac{A\,\exp(-E_a/R T_f)}{a}, \qquad Da = Da_{crit} \text{ on the flammability boundary}
$$

Damkohler number for the stagnation region of a burning solid: ratio of chemical reaction rate (pre-exponential A, activation energy E_a in J/mol, flame temperature T_f in K, gas constant R) to the stretch (strain) rate a (1/s). Olson and Ferkul showed the BASS-II PMMA rod flammability boundary corresponds to a critical Da; on the blowoff branch T_f is nearly constant so the limiting oxygen rises linearly with a, while on the quenching (low-a) branch radiative and conductive losses lower T_f and the exponential makes temperature critical.

<https://ntrs.nasa.gov/citations/20150008961>: *For the blowoff branch, the boundary exhibits a linear dependence on oxygen concentration and stretch rate, indicating that the temperature at blowoff must be fairly constant.*

$$
Z = \frac{s Y_F - Y_{O_2} + Y_{O_2,\infty}}{s Y_{F,s} + Y_{O_2,\infty}}
$$

Mixture fraction Z (0 in the far-field oxidiser, 1 in pure fuel vapour) for a one-step reaction with stoichiometric mass ratio s (kg O2 per kg fuel); Y_F, Y_O2 are local fuel and oxygen mass fractions, Y_O2,inf the far-field oxygen and Y_F,s the fuel mass fraction at a reference fuel surface. FGM tables are indexed by Z (plus progress variable and enthalpy); over a pyrolysing solid the surface value of Z varies along the surface, which is why the investigators' quasi-coupled fuel boundary in the 1-D flamelets was needed.

Textbook background: Standard Burke-Schumann-type mixture fraction definition.

## Method

### Apparatus

No hardware. Computational tools: (1) an existing fully coupled fluid-solid framework for charring and ablating materials, extended to a detailed 2-D flame-spread model with multi-step chemistry and fully coupled radiation heat transfer; (2) unsteady and coupled radiative flamelet generated manifolds (UFGM, CR-FGM) built from 1-D flame solutions with a quasi-coupled fuel boundary; (3) an analytical thin-flame theory with a solid-fuel heat and mass transfer model and a Damkohler-based reaction progress variable, compared with a 1-D detailed-chemistry, radiation-coupled numerical model in planar and spherical geometry. Image analysis: a two-colour pyrometry flamelet manifold (TCFM) diagnostic for DSLR images, with flame-hull reconstruction and 3-D ray tracing for radiative heat flux, intended for BASS/BASS-II imagery.

### Fuels and samples

- PMMA (polymethyl methacrylate) (solid, flat sheets, spheres and rods (BASS geometries); cylindrical rods in BASS-II)
- wax (solid, cylinders (BASS geometry))

### Procedure

Implement the unsteady FGM in the fluid-solid framework and test it on BASS geometries; validate the detailed 2-D model against BASS flame spread rates over a range of far-field oxygen levels; build CR-FGMs from 1-D flamelets and compare them a priori with the 2-D detailed solutions for intermediate species; derive analytical estimates of the low-strain radiative extinction bound and compare the resulting flammability maps qualitatively with the BASS-II PMMA rod extinction data compiled by Olson and Ferkul; post-process BASS and BASS-II DSLR imagery by two-colour tomography to compare flame geometry, temperature, soot volume fraction and spread rate with the models; and compare with a parallel NSF-funded normal-gravity flame-spread project.

## Test matrix

Varied:

| Parameter | Range | Unit |
|---|---|---|
| far-field oxygen level (2-D model vs BASS) | range of BASS oxygen levels (values not available) | mole fraction |
| flame strain (stretch) rate (flammability maps) | low-strain radiative extinction to high-strain blowoff (values not available) | 1/s |
| geometry | flat sheet, sphere, rod (PMMA), wax cylinder; planar and spherical 1-D models |  |
| benchmark: BASS-II PMMA rod flow speed and oxygen (experimental data used) | 24 concurrent-flow rod tests; blowoff and quenching limits at several oxygen concentrations |  |

Held constant:

- gravity in simulations: microgravity (no buoyancy); normal-gravity comparison via a parallel NSF project

## Measurements

| Quantity | Instrument | Direct or derived |
|---|---|---|
| flame spread rate (computed vs BASS measured) | 2-D detailed simulation; BASS video | derived |
| intermediate species fields: FGM vs detailed 2-D (a priori error) | simulation comparison | derived |
| flammability map (minimum oxygen vs strain rate) | analytical theory and 1-D numerical model | derived |
| soot temperature, soot volume fraction and flame-to-surface radiative heat flux from DSLR images | two-colour pyrometry flamelet manifold (TCFM) with 3-D ray tracing | derived |

## Findings

1. A detailed 2-D flame-spread model with multi-step chemistry and fully coupled radiation, validated against NASA BASS data, predicts reasonable flame spread rates over a range of far-field oxygen levels (spread-rate values and error not available in the abstracts read). *(method, medium)*
   - <https://researchconnect.buffalo.edu/en/publications/radiative-flamelet-generated-manifolds-for-solid-fuel-flame-sprea/>: *The model is validated against measurements using the NASA BASS data and is shown to predict reasonable flame spread rates over a range of far-field oxygen levels.*
2. Building the flamelet manifolds from 1-D flames with a quasi-coupled fuel surface boundary (rather than a fixed fuel inlet) is critically important for capturing the spatial variation of mixture fraction along a pyrolysing fuel surface. *(method, high)*
   - <https://researchconnect.buffalo.edu/en/publications/radiative-flamelet-generated-manifolds-for-solid-fuel-flame-sprea/>: *coupled radiative flamelet generated manifolds (CR-FGM's) are created using a simplified one-dimensional (1D) descriptions that include a quasi-coupled, fuel boundary that is shown to be critically important for capturing the spatially dependent variation of mixture fraction on fuel surfaces.*
3. The coupled radiative FGMs reproduce the wide range of chemical states (intermediate species) of the detailed 2-D solution in most of the flow, but differ near the flame attachment (leading-edge) location, where flame-wall interaction before the fuel starts to burn and curved flame structure are not represented by 1-D flamelets. *(result, high)*
   - <https://researchconnect.buffalo.edu/en/publications/radiative-flamelet-generated-manifolds-for-solid-fuel-flame-sprea/>: *Differences between the 2D model data and the CR-FGM's are then identified to be from flame-wall interactions and curved flame structure effects.*
   - <https://researchconnect.buffalo.edu/en/publications/on-the-development-of-coupled-radiative-flamelet-generated-manifo/>: *Results show promising agreement for most of the flow regions except near the flame attachment location where some differences are observed due to flame wall interactions before the fuel starts to burn.*
4. An analytical thin-flame theory coupled to a solid-fuel heat and mass transfer model, with a Damkohler-based progress variable for incomplete combustion at high strain, captures the low-strain radiative extinction bound of the U-shaped flammability map as computed by a detailed 1-D model, and agrees qualitatively (similar trends) with Olson and Ferkul's BASS-II PMMA rod extinction data. *(result, medium)*
   - <https://researchconnect.buffalo.edu/en/publications/theoretical-estimates-of-flammability-bounds-for-thin-condensed-f/>: *The results show the newly developed analytics capture the radiative extinction bound compared to the numerical model and qualitatively agrees with microgravity data.*
5. Benchmark behaviour the models target (BASS-II, 24 concurrent-flow PMMA rod tests on the ISS): the flammability boundary is a critical Damkohler number; the blowoff branch is linear in oxygen and stretch rate (near-constant flame temperature), and near the quenching limit surface radiative loss exceeds conduction into the rod. *(limit, high)*
   - <https://ntrs.nasa.gov/citations/20150008961>: *A surface energy balance is presented that shows the surface radiative loss exceeds the conductive loss into the rod near the limit.*
   - <https://ntrs.nasa.gov/citations/20150008961>: *For the blowoff branch, the boundary exhibits a linear dependence on oxygen concentration and stretch rate, indicating that the temperature at blowoff must be fairly constant.*
6. A two-colour pyrometry flamelet manifold diagnostic was developed for DSLR images: the red/green intensity ratio indexes strained 1-D flames one-to-one, and accounting for soot self-absorption improves soot volume fraction estimates; flame-to-surface radiative heat flux from 3-D ray tracing agreed well with literature, with improvement near the flame base. It was demonstrated on upward (normal-gravity) flame spread, not on BASS imagery, in the source read. *(method, medium)*
   - <https://doi.org/10.1016/j.combustflame.2021.111395>: *Accounting for self-absorption effects provide improved soot volume fraction estimates. The radiative heat flux estimates are found to be in very good agreement with literature and improved results are obtained near the flame base.*
   - <https://doi.org/10.1016/j.combustflame.2021.111395>: *The developed diagnostic is used in upward flame spread experiments*

## Fire-safety relevance

Microgravity flammability tests of materials are scarce and expensive; validated models could screen new spacecraft materials for their minimum oxygen concentration and the flow range in which they burn, and flamelet tables could serve as subgrid models in large-eddy simulations of cabin fires for hazard assessment. The U-shaped map matters operationally: in microgravity, a material may keep burning at low ventilation speeds where buoyancy on Earth would have imposed a different strain, so 1 g tests can misjudge limits. Caveats: the agreement with BASS-II flammability data is qualitative only, the FGM approach has known errors at the flame leading edge, which controls spread and extinction, and the 'Goldilocks' zone reproduction stated as the goal is not reported in the sources read.

### Habitat conditions

The BASS/BASS-II benchmark tests varied oxygen by nitrogen vitiation of the glovebox (lowering it below air, at near-cabin pressure); the specific oxygen fractions and pressures modelled are not given in the sources read. No modelling at enriched-oxygen, reduced-pressure exploration atmospheres (e.g. 30% or more O2 at 70.3 kPa or less) is reported, although the model framework could in principle be run there.

### Earth benefits

Improved coupled thermal-chemical-flow models of solid-fuel flame spread and new camera-based radiative heat flux diagnostics can inform terrestrial fire safety standards and fire modelling.

## Limitations

- Validation against BASS is described only qualitatively ('reasonable' spread rates, 'similar trends'); no quantitative errors are available in the sources read.
- Flamelet manifolds are least accurate at the flame attachment point, the region that governs flame spread and blowoff, so manifold-based predictions of limits need further correction there.
- The planned two-colour tomographic reconstructions of BASS/BASS-II soot and temperature fields, the sphere, rod and wax-cylinder simulations, and the 'Goldilocks'-zone comparison are described in the PSI record but no published results for them were found.

## Data in PSI

PSI holds only an ISA-Tab metadata zip (9.7 kB) repeating the record text; its study file has a single placeholder row. No model code, flamelet tables, simulation output or reconstructed BASS soot/temperature fields were deposited. The experimental benchmarks are in BASS (PSI-26) and BASS-II (PSI-25).

| Category | What | Formats | Files | Size | Usable now |
|---|---|---|---|---|---|
| metadata | ISA-Tab investigation and study files (i_Investigation.txt, s_PSI-62.txt with 'Do not use this' placeholder rows) | .zip .txt | 1 | 9.7 kB | yes |

## Related investigations

- [PSI-26](PSI-26-bass.md): ground re-analysis
- [PSI-25](PSI-25-bass-ii.md): ground re-analysis

## Open questions

- Quantitatively overlay the model's U-shaped flammability boundary on the BASS-II PMMA rod blowoff and quenching points (oxygen vs stretch rate) from PSI-25.
- Apply the two-colour flamelet diagnostic to BASS/BASS-II DSLR imagery in PSI to obtain soot temperature, soot volume fraction and surface radiative heat flux for microgravity flames.
- Run the validated model at exploration-habitat atmospheres (elevated O2 at reduced pressure) to predict how the minimum-oxygen point moves.

## Dashboard ideas

- **flammability map (U-curve)** (`x_o2`, `strain_rate_1_s`, `limit_type (blowoff/quench)`, `source (model/BASS-II)`): Central concept linking this model study to BASS-II measured limits; experimental points must come from PSI-25.
- **linked investigations** (`accession`, `relation`): Points users from this metadata-only record to the BASS and BASS-II data it benchmarks against.

## Gaps and data-quality notes

- PSI-62 holds only a metadata zip; no model code, manifolds or outputs. Findings rest on the PSI record and abstracts from the University at Buffalo research portal (researchconnect.buffalo.edu) for the two 2023 Combustion and Flame papers and the AIAA SciTech 2024 paper (not listed in PSI), Semantic Scholar for 10.1016/j.combustflame.2021.111395, and NTRS 20150008961 (Olson et al., BASS-II PMMA rods, 2015 conference paper) in place of the Olson and Ferkul 2017 journal paper.
- Abstracts for 10.1016/j.combustflame.2017.03.001, 10.1016/j.combustflame.2023.112939 and 112910 are absent from OpenAlex, Crossref and Semantic Scholar; ScienceDirect returned HTTP 403. The 2023 abstracts were taken from the UB portal pages whose titles match; the portal page for 112939 was matched by title only.
- No thesis by K. Budzinski or S. Aphale was located; no spread-rate numbers, oxygen levels or error metrics were available.
- PI affiliation in PSI is 'New York University, Buffalo'; the publications are from the University at Buffalo (SUNY).
- The PSI record lists Olson and Ferkul (2017) as a publication, but it is a NASA BASS-II paper used as a benchmark, not a product of this grant. The Aphale and DesJardin (2021) diagnostic paper applies to upward (1 g) flame spread.
- Grant period ended 2021-04-30 while the main modelling papers appeared in 2023-2024; whether the 2023 papers were funded by this grant is assumed from their listing in the record.
- The 'Goldilocks' flammability zone is attributed to Olson and Ferkul in the record; the term was not found in the abstracts read.
