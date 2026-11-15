"""Question bank: research questions the data answer today, each with the call that answers it.

`answer` is the answer as of the current tables; tests/test_questions.py runs every call.
Rendered to docs/question-bank.md by `uv run python -m fif.pipeline.build_catalog`.
"""

QUESTIONS = [
    # --- scenario and gaps ---
    {"theme": "Scenario and gaps", "question": "Which investigations matter most for a Moon habitat (30% O2, 70 kPa, 1/6 g)?",
     "function": "relevance", "arguments": {"scenario": "moon-habitat", "fuel_phase": "solid"},
     "chart": "stacked bar of score components per investigation",
     "answer": "FLEX leads: its droplet tests sit at that atmosphere (30% O2, 71 kPa). BRE and FLEX-2 also show a "
               "distance of 0, but only because their rows give O2 and pressure as ranges that contain the point. "
               "The solid-material experiments (BASS-II, Saffire-II, BASS) follow, all more than 3 steps away in O2 "
               "and pressure. No test was run at partial gravity."},
    {"theme": "Scenario and gaps", "question": "Has any solid material been burned in an exploration atmosphere?",
     "function": "coverage", "arguments": {"fuel_phase": "solid"},
     "chart": "heatmap of test counts, O2 against pressure, with reference atmospheres overlaid",
     "answer": "No. All solid-fuel tests were run at 13.6-22.7% O2 and about 1 atm. The Moon-habitat, exploration and "
               "spacesuit points fall on empty cells."},
    {"theme": "Scenario and gaps", "question": "What was tested at 30% O2 or more and 75 kPa or less?",
     "function": "filter_tests", "arguments": {"x_o2": [0.30, None], "pressure_kpa": [None, 75]},
     "chart": "scatter O2 against pressure, coloured by fuel",
     "answer": "37 tests: CFI-G gas flames (butane 14, ethane 6) and FLEX droplets (methanol 9, n-heptane 8). No solids."},
    {"theme": "Scenario and gaps", "question": "What are the biggest gaps in the PSI combustion data for exploration fire safety?",
     "function": "insights", "arguments": {"topic": "gaps"}, "chart": "ranked list",
     "answer": "13 ranked gaps. The top three: solid materials at elevated O2 and reduced pressure; partial gravity; "
               "imagery and raw signals that were never reduced to per-test outcomes."},
    {"theme": "Scenario and gaps", "question": "What does PSI say about partial gravity?",
     "function": "find_evidence", "arguments": {"query": "partial gravity lunar Martian electric field", "raw": False},
     "chart": None,
     "answer": "Nothing measured. E-FIELD Flames used an electric field as a stand-in for a body force; the link to "
               "partial gravity rests on a 2012 drop-tower precursor, not on the flight data in PSI."},
    {"theme": "Scenario and gaps", "question": "Which investigations address detection in an ISS-like cabin?",
     "function": "relevance", "arguments": {"scenario": "iss-cabin", "pillar": "detection"},
     "chart": "stacked bar of score components",
     "answer": "SAME-R and SAME (smoke particle size from overheated spacecraft materials), then SPICE (soot), "
               "BASS-II and BASS (small solid flames in cabin air, ranked on conditions rather than on detection) and "
               "the Saffire flights (a real fire seen by vehicle sensors)."},

    # --- prevention: materials ---
    {"theme": "Prevention", "question": "How low in oxygen did solid samples still burn in microgravity?",
     "function": "filter_tests", "arguments": {"fuel_phase": "solid", "x_o2": [None, 0.16]},
     "chart": "strip plot of O2 per fuel",
     "answer": "PMMA rods burned down to 14.2% O2 in the table (BASS-II test O5b); the attempt at 13.6% (O12) did "
               "not ignite at any flow. The BASS-II report puts the minimum of the fitted limit for rods at about 13.5%; "
               "its lowest final O2 reading with a flame, started higher, was 13.6%. The limit burning upward on "
               "Earth was 15.4%. Cotton-fibreglass fabric to 16.4%. "
               "The table has no ignition column for these rows: read the air-display and crew cells in extra."},
    {"theme": "Prevention", "question": "Is the normal-gravity flammability test conservative?",
     "function": "insights", "arguments": {"topic": "micro_vs_1g"},
     "chart": "paired dot plot, microgravity against 1 g per material",
     "answer": "Not always. 28 comparisons: PMMA rods and cotton-fibreglass fabric burn in orbit under conditions where "
               "they go out on Earth; silicone, Nomex and Ultem behaved as on Earth near 21-22% O2."},
    {"theme": "Prevention", "question": "How fast does a large fabric sheet burn compared with small samples?",
     "function": "filter_tests", "arguments": {"accession": ["PSI-98", "PSI-99", "PSI-100"]},
     "chart": "bar of spread rate per test, grouped by flow direction",
     "answer": "On the 94 cm Saffire sheet, concurrent spread was steady at 1.8 mm/s (20 cm/s flow) and 2.3 mm/s "
               "(25 cm/s); opposed spread 1.3 and 0.98 mm/s. Silicone samples did not spread."},
    {"theme": "Prevention", "question": "What happens to a small fire when the air stops moving?",
     "function": "find_evidence", "arguments": {"query": "flow turned off flame extinguished quench low flow", "accession": "PSI-26", "raw": False},
     "chart": None,
     "answer": "At 1 atm, in air and in some runs near 17% O2, small BASS flames went out when the air flow was "
               "shut off; concurrent fabric flames quenched below about 1 cm/s."},
    {"theme": "Prevention", "question": "What limits (minimum O2, quench flow, blow-off) have been measured?",
     "function": "insights", "arguments": {"topic": "limits"}, "chart": "table grouped by limit type",
     "answer": "35 limits with their conditions, from 1 cm/s radiative quench of thin PMMA to 44 cm/s without blow-off "
               "of fabric, and droplet limiting O2 of 12-17% by diluent."},
    {"theme": "Prevention", "question": "Do gas-burner flames survive at 21% O2 without flow, and at 40%?",
     "function": "filter_tests", "arguments": {"accession": "PSI-159", "config": "normal",
                                              "columns": ["fuel", "x_o2_ambient", "pressure_kpa", "extinction_mode", "burn_time_s"]},
     "chart": "stacked bar of extinction mode per O2 bin",
     "answer": "At 18-23% O2, 23 of 64 attempts did not ignite and all 41 flames that lit self-extinguished. At "
               "33-40% O2, 23 of 115 did not ignite, 61 of the 92 lit flames self-extinguished and 31 burned until the "
               "flow was stopped. Ethane, propane and butane on one spherical burner, 51-304 kPa."},
    {"theme": "Prevention", "question": "How do BASS and Saffire differ in what they can tell us?",
     "function": "compare", "arguments": {"accessions": ["PSI-26", "PSI-25", "PSI-98", "PSI-99", "PSI-100"]},
     "chart": "range bars per parameter",
     "answer": "BASS/BASS-II: many small samples, O2 13.6-22.7%, flow 0-55 cm/s, in a 7.6 cm duct. Saffire: few large "
               "samples (up to 94 cm) at 20-25 cm/s in cabin air, with vehicle-scale pressure and temperature response."},

    # --- suppression ---
    {"theme": "Suppression", "question": "Which diluent extinguishes droplet flames at the highest oxygen level?",
     "function": "insights", "arguments": {"topic": "limits", "accession": "PSI-69"},
     "chart": "bar of limiting O2 per fuel and diluent",
     "answer": "CO2: limiting O2 14% (methanol) and 17% (n-heptane), against 12% and 15% with N2. Helium: 14% and 15%."},
    {"theme": "Suppression", "question": "How do FLEX droplets stop burning?",
     "function": "filter_tests", "arguments": {"accession": "PSI-69", "columns": ["fuel", "x_o2_ambient", "pressure_kpa", "d0_mm", "extinction_mode", "ext_diameter_mm"]},
     "chart": "scatter d0 against O2, coloured by extinction mode",
     "answer": "Of 274 tests: 186 flame extinction with fuel left, 61 droplet disruption, 27 burned to completion. "
               "The table has no failed ignitions, so it cannot say when a droplet will not burn."},
    {"theme": "Suppression", "question": "Does a nitrogen jet put out a burning plastic sample?",
     "function": "find_evidence", "arguments": {"query": "nitrogen suppressant jet nozzle leading edge wake flame", "accession": "PSI-26", "raw": False},
     "chart": None,
     "answer": "Usually only the leading edge. Wake and side flames survived, helped by air the jet entrained."},
    {"theme": "Suppression", "question": "Can a flame survive as a cool flame after it seems to go out?",
     "function": "filter_tests", "arguments": {"accession": "PSI-39", "columns": ["fuel", "pressure_kpa", "d0_mm", "ext_diameter_mm", "n_reignitions", "cool_flame"]},
     "chart": "scatter pressure against extinction diameter, marker = cool flame",
     "answer": "Yes. 127 of 227 CFI droplet tests have cool-flame data after hot-flame radiative extinction, and at "
               "200 kPa and above some re-ignited as hot flames (up to 7 times)."},

    # --- detection ---
    {"theme": "Detection", "question": "Would the ISS smoke detector see smoke from overheated spacecraft materials?",
     "function": "find_evidence", "arguments": {"query": "ISS smoke detector alarm threshold Kapton Teflon light scattering", "accession": "PSI-101", "raw": False},
     "chart": None,
     "answer": "Often not: in SAME-R more than half the Kapton tests and two-thirds of the Teflon tests would not "
               "have reached the ISS light-scattering alarm level."},
    {"theme": "Detection", "question": "Which materials and flows were tested for smoke?",
     "function": "filter_tests", "arguments": {"accession": "PSI-101", "columns": ["fuel", "flow_cm_s", "date"]},
     "chart": "bar of test count per material",
     "answer": "109 SAME-R rows on Kapton, Teflon, silicone, lamp wick (cotton) and Pyrell foam at 0-8 cm/s. One row "
               "(Teflon 57) is a false copy of the lamp-wick run 57 and is flagged; run 112 (Kapton) is missing from the list."},
    {"theme": "Detection", "question": "Which flames are hard to see?",
     "function": "find_evidence", "arguments": {"query": "cool flame invisible dim hydrogen flame not visible camera", "raw": False},
     "chart": None,
     "answer": "Cool flames (FLEX, CFI, CFI-G) and hydrogen flames (SLICE, s-Flame) emit little or no visible light; "
               "cool flames were found from radiometer and droplet-size data, not from cameras."},
    {"theme": "Detection", "question": "When does a gas flame start to smoke?",
     "function": "filter_tests", "arguments": {"accession": "PSI-107", "columns": ["fuel", "geometry", "flow_cm_s", "flame_length_mm", "at_smoke_point"]},
     "chart": "scatter coflow speed against flame length, marker = at smoke point, facet by fuel",
     "answer": "The SPICE run log has 526 rows (video and still measurements of the same flames are separate rows). "
               "23 rows marked at the smoke point have a flame length: propylene 8.8-45.6 mm (17 rows), ethylene "
               "27-56 mm (3) and propane 60-92 mm (3), depending on nozzle and co-flow. No methane row is marked."},

    # --- physics and data ---
    {"theme": "Physics", "question": "How does pressure change droplet burning (CFI)?",
     "function": "filter_tests", "arguments": {"accession": "PSI-39", "columns": ["fuel", "pressure_kpa", "d0_mm", "burn_rate_k_mm2_s", "ext_diameter_mm"]},
     "chart": "box plot of K per pressure level",
     "answer": "The median burning-rate constant stays near 0.30-0.35 mm2/s from 50 to 300 kPa and roughly doubles "
               "(0.69) at 510 kPa; the extinction diameter stays near 4 mm."},
    {"theme": "Physics", "question": "What is the governing physics of an investigation?",
     "function": "get_investigation", "arguments": {"accession": "FLEX", "sections": ["physics", "question"]},
     "chart": None,
     "answer": "Each record has a plain-language physics section with LaTeX equations (for FLEX: the d-squared law, "
               "radiative and diffusive extinction)."},
    {"theme": "Physics", "question": "How do the investigations build on each other?",
     "function": "insights", "arguments": {"topic": "lineage"}, "chart": "network graph of investigations",
     "answer": "35 links: shared hardware (SPICE duct for SPICE, SLICE, BASS, BASS-II; MDCA for FLEX, FLEX-2, CFI; "
               "ACME for six gas-flame experiments), follow-ons and the ground studies that model flight data."},
    {"theme": "Physics", "question": "What new analyses could be launched from the data as they are?",
     "function": "insights", "arguments": {"topic": "research_questions"}, "chart": "cards",
     "answer": "20 research questions, each with the data it needs and the expected result."},
    {"theme": "Physics", "question": "Which investigations study soot?",
     "function": "search_investigations", "arguments": {"query": "soot formation smoke point sooting"},
     "chart": "cards", "answer": "SPICE, SLICE, Flame Design, CLD Flame and the coflow modelling study PSI-60 rank first."},

    # --- sensor traces and models ---
    {"theme": "Sensor traces", "question": "What does a flame that goes out on its own look like in the sensors?",
     "function": "timeseries", "arguments": {"test_id": "21088 M4", "max_points": 400},
     "chart": "line chart of radiometers and burner temperature against time, ignition and flame-out marked",
     "answer": "CFI-G test 21088 M4 (ethane, 21% O2, 1 atm): the radiometers show a flame from 23.4 s to 36.7 s, "
               "13.3 s in all, and the burner reaches 125 C. Radiometer volts have no archived calibration."},
    {"theme": "Sensor traces", "question": "What atmosphere did the Saffire-I fire actually burn in?",
     "function": "timeseries", "arguments": {"test_id": "S1", "accession": "PSI-98", "max_points": 400,
                                              "channels": ["o2_pct", "co2_pct", "anemometer_1_cm_s"]},
     "chart": "line chart of O2, CO2 and flow speed against time",
     "answer": "The raw sensors give 22.6% O2 falling to 22.2%, CO2 rising from 0.43% to 0.63%, 102.3 kPa and "
               "20 cm/s flow. The experiment table has 21.5-21.7% O2 and no pressure."},
    {"theme": "Models", "question": "Which outcomes can be predicted from test conditions, and how well?",
     "function": "predict", "arguments": {}, "chart": "table of models with sample size and cross-validated score",
     "answer": "Three models give a prediction, scored on whole held-out test days: self-extinction of inverse "
               "CFI-G gas flames (AUC 0.89) and FLEX droplet burning rate and methanol extinction diameter (R2 0.69 "
               "and 0.70). The numbers are soft: resampling the test days gives AUC 0.51-0.94, R2 0.63-0.80 and "
               "0.13-0.76. Five more models are descriptive only, among them self-extinction of normal CFI-G flames "
               "(AUC 0.69, range 0.36-0.80, not clearly better than chance)."},
    {"theme": "Models", "question": "How fast would a heptane droplet burn in a Moon-habitat atmosphere?",
     "function": "predict", "arguments": {"model_id": "flex_burning_rate", "is_heptane": 1, "x_o2_ambient": 0.30,
                                           "x_co2": 0, "x_he": 0, "pressure_kpa": 70.3, "d0_mm": 3.0},
     "chart": "predicted value against the nearest measured tests",
     "answer": "K about 0.69 mm2/s for a 3 mm droplet at 30% O2 and 70.3 kPa. FLEX measured 0.58 and 0.78 mm2/s "
               "in two tests at almost exactly these conditions (microgravity, not lunar gravity)."},
    {"theme": "Models", "question": "Would a small ethane gas flame in still cabin air go out on its own?",
     "function": "predict", "arguments": {"model_id": "cfig_normal_self_extinction", "x_o2_ambient": 0.21,
                                           "pressure_kpa": 101, "fuel_flow_mg_s": 1.0, "fuel_fraction": 1.0, "n_carbon": 2},
     "chart": "nearest measured tests, with the observed fractions by ambient O2",
     "answer": "In CFI-G it did: the five nearest tests all self-extinguished, as did all 41 lit flames at about "
               "21% O2. The model gives no probability, it is descriptive only (it did not hold up on held-out "
               "test days). Valid for the CFI-G spherical burner only."},
    # --- data quality ---
    {"theme": "Data quality", "question": "Where are the original PSI tables wrong or doubtful?",
     "function": "discrepancies", "arguments": {},
     "chart": "table grouped by investigation, with a badge for corrected / filled / flagged",
     "answer": "50 cells conflict with the raw data: 9 were corrected (a mistyped test id, an ignition logged "
               "as failed, two burn times, two dates, a fuel mixture, two propane fractions of a day that began with "
               "a diluted fuel line), 5 empty cells were filled (Saffire pressures, "
               "a date) and 36 are flagged with the value kept, among them a SAME-R row for a test that was never run "
               "and CFI-G runs listed as failed ignitions although nothing flowed. 6 more cells are flagged from the "
               "operators' hand-filled test sheets, which are an AI reading of scans that nobody checked. Thirteen notes "
               "cover whole investigations, such as recorded test points missing from the tables and flames stopped "
               "by the burner temperature limit."},
    {"theme": "Data quality", "question": "What is wrong with the CFI-G table?",
     "function": "discrepancies", "arguments": {"accession": "PSI-159"},
     "chart": "table of test, column, table value, raw value, action",
     "answer": "Test 21106 F4 is logged as not ignited but burned for 20 s; 21112 A6 is given 259 s of burning where "
               "the flame lasted 147 s; 21270 H3 carries the previous test's 43 s where the flame lasted 94 s. Six "
               "more burn times are 5-17 s short, ten recorded test points are not in the table (nine failed ignitions of day 21106 and one "
               "run aborted before gas flowed), and the pressures of "
               "normal flames are nominal fill levels about 3 kPa below the transducer reading. Six rows listed as not "
               "ignited were not ignition attempts (nothing flowed, or a no-flame test), two burner O2 values are "
               "contradicted by the flow controllers, and on day 21277 the oxidizer flow fell below its setpoint as "
               "the bottle emptied. On day 21106 five rows give 0.8 mg/s of fuel where the recorded flow is about "
               "0.5 or 0.65 mg/s (flagged, not changed). 24 flames logged as flow-terminated were stopped by the "
               "burner temperature limit "
               "(from the test sheets, an AI reading of scans that nobody checked)."},
]
