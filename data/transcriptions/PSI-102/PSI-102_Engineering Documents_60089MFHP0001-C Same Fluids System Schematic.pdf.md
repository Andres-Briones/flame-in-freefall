<!-- visual transcription of a scanned PDF, read from page images by an AI model on 2026-11-14; not checked by a human -->
## page 1
Description: E-size fluids system schematic (sheet drawn rotated 90 degrees on the page) for the Smoke Aerosol Measurement Experiment (SAME). Shows the Fluids Control Unit (nitrogen supply from the MSG GN2 quick disconnect through filter, solenoid valve, relief valves and a 15 psig regulator to a nitrogen manifold; mass flow controller; vacuum manifold to the MSG vacuum QD), the aging chamber smoke piston (sample side / drive-vac side), the Dynamic Diagnostics Assembly (ISS and STS smoke detectors), the Dynamic Diluter (LFE, static mixer, VSO), Commercial Diagnostics Enclosures A and B (optics chamber and ion sensor each), the P-Trak enclosure and the Thermal Precipitator Module (TPM). Symbol legends along the bottom edge, general notes and balloon legend at right. Balloon tags combine a pressure letter and a gas letter (see balloon legend) with a number.

### Title block
- Title: SAME FLUIDS SYSTEM SCHEMATIC; next assembly: SMOKE AEROSOL MEASUREMENT EXPERIMENT 60089MFHP000
- Drawing number: 60089MFHP000, size E, rev C
- Organisation: National Aeronautics and Space Administration, John H. Glenn Research Center, Lewis Field, Cleveland, Ohio; ZIN Technologies
- Project lead, quality, safety, engineer, designer, reviewer: [name omitted], dated 7/21/05 to 7/26/05
- Contract number: NAS3-99154; delivery order: MRDOC-074; file location: M:\MRDOC\60089_074; CAD package: AutoCAD Mechanical 2004 DX
- Scale: none; official date 07/23/2005; sheet 1 of 6; bldg ZIN; area GRC; units: inch; discipline: mechanical; "AutoCad 2004"
- Tolerances: .X ±; .XX ±; .XXX ±; FRACTION ±; ANGULAR ± NA; BREAK EDGES NA (no values). Dimensioning and tolerancing per ASME Y14.5M-1994.
- "This drawing is under configuration control: do not revise without approved ECO". Approved: [name omitted], date 1/27/06

### Revisions
| CHG | ZONE | DESCRIPTION | APP/DATE |
|---|---|---|---|
| A | H7,8 E,D 5&6 B8 | REV. A INCORPORATED ECO No. SAME-ECO-077 | [name omitted] 11/23/05 |
| B | F8, D6, G1 | REV. B INCORPORATED ECO No. SAME-ECO-090 | [name omitted] 1/13/06 |
| C | B8 | REV. C INCORPORATED ECO No. SAME-ECO-095 | [name omitted] 1/27/06 |

### General notes
01 REFER TO CP SHEETS FOR COMPONENT INFORMATION
02 MAXIMUM DESIGN PRESSURE OF COMPONENTS UPSTREAM OF AND INCLUDING PRESSURE REGULATOR (PN06) IS 200 PSIA
03 MAXIMUM DESIGN PRESSURE OF COMPONENTS DIRECTLY CONNECTED TO THE DYNAMIC DIAGNOSTICS ASSEMBLY INCLUDING THE DYNAMIC DILUTER IS 15.7 PSIA
04 MAXIMUM DESIGN PRESSURE OF COMPONENTS DOWNSTREAM OF AND INCLUDING CHECK VALVES (VR09, VR20) IS 40 PSIA
05 ALL COMPONENTS NOT MENTIONED IN ABOVE NOTES HAVE A MAXIMUM DESIGN PRESSURE OF 29.7 PSIA
06 REFERENCES TO ASSEMBLY DRAWINGS ARE NOTED ON THE SCHEMATIC
07 ALL FLEXIBLE HARD LINES TO BE PROOF PRESSURE TESTED TO 2.0 X MDP. REFER TO SAME-TST-035.
08 FULL SYSTEM TO BE LEAK TESTED AT 1.0 X MDP OR 1.0 X HIGHEST OPERATING PRESSURE MINUMUM. REFER TO SAME-TST-036.
09 TUBING AND LINES ARE SHOWN ON COMPONENT ASSEMBLY DRAWINGS OR INTERFACE CONNECTION DRAWING

### Balloon legend
| PRESSURE | GAS |
|---|---|
| P - POSITIVE | N - NITROGEN |
| V - VACUUM | M - MSG ENVELOPE |
| B - BOTH (P OR V) | R - N AND/OR MSG ENV. |
| A - NEAR ATM | T - MSG ENV. AND/OR SMOKE |
| | U - ANY |

### Fluids Control Unit (see 60089MFHA220 for detail)
Nitrogen supply path (heavy line, 1/8" OD SS):
- MSG GN2 QD -> PN08 / PN01 quick disconnect (PN10, PN09 quick disconnect with shut-off and cap outside the unit) -> PN05 filter (F) -> PN04 relief valve "RELIEF VALVE 1, 220 PSIG WITH MANUAL OVERRIDE" -> PN02 PT (pressure transducer) -> PN03 solenoid valve -> PN06 pressure regulator, 15 PSIG
- Downstream of PN06: 1/8" ID TYGON nitrogen manifold with PN12 PT; PN13, PN14, PN16 relief valves each 20 PSIG; solenoid valves PN07, PN24 (-> orifice PN25), PN15, PN27 (-> orifice PN28)
- PN07 feeds 3-way/4-way solenoid valves BN08 and BN09
- Mass flow controller BN19, between 3-way solenoid valves BN18 and BN17; BN20 solenoid valve to VENT; BN02 PT; BN16 solenoid valve
- Lines leave the unit through quick disconnects to BN03 VACUUM/GN2 QD1 and BN23 VACUUM/GN2 QD2
Vacuum path:
- VM06 solenoid valve -> VM05 orifice -> VM07 orifice -> AT16 filter (F) -> quick disconnect
- VR12, VR11, VR06 solenoid valves on vacuum branches to quick disconnects; VR04 PT on the vacuum header
- VM09 solenoid valve -> VM10 orifice -> AT20 PT -> AT11 filter (F)
- VR03 solenoid valve; VR02 relief valve "RELIEF VALVE 2, 20 PSIG WITH MANUAL OVERRIDE"
- Check valves VR09 and VR20 in series, 1/8" ID TYGON, -> VR01 quick disconnect -> VR19 MSG VACUUM QD; VR14, VR13 quick disconnect with shut-off and cap
- VR10 VACUUM QD

### Aging chamber (see 60089MFHA150 for detail)
- SMOKE PISTON block: SAMPLE SIDE above the piston, DRIVE/VAC SIDE below
- Sample side ports with valves operated by actuators BN21 and BN22
- Drive/vac side port BN25 to VACUUM/GN2 QD1; VACUUM/GN2 QD2 (BN23)
- Line "FROM MSG WORK VOLUME" to the sample side

### Dynamic Diagnostics Assembly (see 60089MDBA165 for detail)
- AT05 check/inlet "FROM MSG WORK VOLUME" -> ISS SMOKE DETECTOR -> STS SMOKE DETECTOR -> AT06 filter (F) -> TO MSG RECIRCULATION FANS
- AT13 SAMPLE OULET QD (as written) between the two detectors

### Dynamic Diluter (see 60089MFHA180 for detail)
- AT03 inlet (SAMPLE QD2) -> AT07 -> LFE (laminar flow element) with AT08 PT across it -> AU01 STATIC MIXER -> AU02 SAMPLE QD1 outlet
- PN20 GN2 QD -> PN23 VSO (voltage sensitive orifice) feeding dilution gas into the stream

### P-Trak enclosure (see 60089MFHA500 for detail)
- AU03 inlet (SAMPLE QD) -> OPTICS CHAMBER -> AU05 filter -> VR07 orifice -> VR05 VACUUM QD
- Bypass: AU06 filter -> VR08 orifice

### Commercial Diagnostics Enclosure (A) (see 60089MFHA600 for detail)
- SAMPLE INLET 1 (AU07) -> AU08 filter -> OPTICS CHAMBER -> AU09 filter -> VR15 orifice -> VR16 VACUUM QD
- SAMPLE INLET 2 (AT04) -> AT09 ION -> AT10 filter -> VM04 orifice -> vacuum

### Commercial Diagnostics Enclosure (B) (see 60089MFHA600 for detail)
- SAMPLE INLET 1 (AU10) -> AU11 filter -> OPTICS CHAMBER -> AU12 filter -> VR17 orifice -> VR18 VACUUM QD
- SAMPLE INLET 2 (AT17) -> AT18 ION -> AT19 filter -> VM13 orifice -> vacuum

### Thermal Precipitator Module (TPM) (see 60089MFHA300 for detail)
- SAMPLE INLET 1 (AT14) and SAMPLE INLET 2 (AT15) each to a manifold of 6 solenoid-valved sample lines (12 total) -> common outlet -> VM08 VACUUM QD

### Symbol legends
Piping component symbols: butterfly valve; check valve; gate valve; relief valve; ball valve; voltage sensitive orifice; directional valves 2-way, 3-way, 4-way; pressure regulator; loader; cylinder regulator; turb flowmeter; orifice; venturi; rupture disk; quick disconnect; press gauge; filter; strainer; heat exch; pump; motor; quick disconnect with shut-off.
Actuator symbols: cylinder; hand; pneu control; rotary motor; solenoid.
Primary control element symbols: EP elec-pneu xdcr; EH elec-hydr xdcr; LLS liq level switch; LLT liq level xdcr; LS limit switch; PDS press diff switch; PDT press diff xdcr; PS pressure switch; PT pressure xdcr; TC thermocouple; TS temp switch.
Item designations: locally mounted; control room mounted; altn control room mounted; ref drawing.
Instrument letter designations: first letter B burner, E emergency, F flow, H hand, L level, P pressure, S speed, T temperature, Z position, J power, U surge; succeeding letter A alarm, C control, D differential, H high, I indicate, L low, P permissive, R record, S shutdown, Y datalog.
Instrument symbols: general; prgm logic controller; data collector facility; prgm process controller; fluids system labels.
