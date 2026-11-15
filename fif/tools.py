"""Tool definitions (JSON Schema, the shape LLM function-calling APIs expect) for the functions in fif.api."""
from fif import api

RANGE = {"type": "array", "items": {"type": ["number", "null"]}, "minItems": 2, "maxItems": 2,
         "description": "[min, max]; null leaves that end open"}
ACCESSION = {"type": "string", "description": "PSI accession (PSI-26) or acronym (BASS)"}
PHASE = {"type": "string", "enum": ["solid", "liquid", "gas", "aerosol"]}
PILLAR = {"type": "string", "enum": list(api.PILLARS)}
TEST_FILTERS = {
    "accession": {"type": ["string", "array"], "items": {"type": "string"}, "description": "one or several investigations"},
    "fuel": {"type": "string", "description": "a normalised fuel name, matched as a whole word: pmma, heptane (also n-heptane blends); ethane does not return methane"},
    "fuel_phase": PHASE,
    "config": {"type": "string", "description": "substring: normal, inverse, coflow, droplet, opposed flow, concurrent flow"},
    "x_o2": {**RANGE, "description": "ambient O2 mole fraction [min, max]"},
    "pressure_kpa": RANGE,
    "flow_cm_s": RANGE,
    "extinction_mode": {"type": "string", "enum": ["self_extinguished", "flow_terminated", "extinction", "disruption", "completion"]},
    "outcome": {"type": "string", "enum": ["no_ignition", "extinguished", "burned_out"],
                "description": "solid-fuel runs of BASS (PSI-26) and BASS-II (PSI-25) only: how the flame ended, read from "
                               "the crew's notes; each row quotes its source in outcome_quote and gives outcome_cause "
                               "(blowoff, low_flow, nitrogen, unspecified) when extinguished. Null on most rows: not stated"},
    "outcome_action": {"type": "string", "enum": ["flow_shut_off", "flow_reduced", "flow_raised", "nitrogen", "none"],
                       "description": "extinguished runs of BASS and BASS-II: what was done to the flow when the flame went "
                                      "out. flow_reduced = it went out at a finite low setting (a quenching limit, the "
                                      "setting in outcome_setting when stated); flow_shut_off = the crew stopped the flow to "
                                      "end the run (not a limit); flow_raised = blowoff; none = it went out by itself at "
                                      "constant flow. Null when the words do not say. flow_cm_s on these rows is the log's "
                                      "single air-display value, not the flow at extinction"},
    "sheet_out": {"type": "string", "enum": ["ext_detect", "time_out", "temp_limit"],
                  "description": "ACME gas flames (PSI-10 inverse flames of 2021-22, PSI-159) only: the ending ticked on the "
                                 "test's hand-filled sheet. ext_detect = the flame went out by itself; time_out = it lasted "
                                 "the scripted time; temp_limit = it was cut off because the burner got too hot (neither "
                                 "an extinction nor a full-length flame). An AI reading of a scan, not checked by a human"},
    "row_kind": {"type": ["string", "null"], "enum": ["test", "test_day", "condition_set", "planned", None]},
    "exclude_flags": {"type": "array", "items": {"type": "string"}, "description": "drop rows carrying any of these flag codes"},
}


def _tool(function, description, properties, required=()):
    return {"name": function.__name__, "description": description,
            "input_schema": {"type": "object", "properties": properties, "required": list(required)}}


TOOLS = [
    _tool(api.search_investigations, "List the 24 PSI combustion investigations as cards; filter by fire-safety pillar, "
          "fuel phase or flight/ground, and rank by a keyword query.", {
              "query": {"type": "string"}, "pillar": {"type": "string", "enum": [*api.PILLARS, "fundamental"]},
              "fuel_phase": PHASE, "flight": {"type": "boolean"}, "limit": {"type": "integer"}}),
    _tool(api.get_investigation, "Full knowledge record of one investigation: question, physics (with equations), method, "
          "test matrix, measurements, PSI data, findings with quoted sources, fire-safety relevance, limitations, open questions.", {
              "accession": ACCESSION,
              "sections": {"type": "array", "items": {"type": "string"}, "description": "only these sections, e.g. [\"findings\", \"limitations\"]"}},
          ["accession"]),
    _tool(api.filter_tests, "Rows of the per-test table (2,177 rows, of which 2,059 are single tests: fuel, O2, "
          "pressure, flow, outcomes). Use for any question about what was tested and what happened.", {
              **TEST_FILTERS, "columns": {"type": "array", "items": {"type": "string"}}, "limit": {"type": "integer"},
              "sheets": {"type": "boolean", "description": "attach to each PSI-10 / PSI-159 row its hand-filled ACME test "
                         "sheet as `test_sheet`: ignited, hot or cool flame, how the flame ended (`out`), operator "
                         "comments, file and page. An AI reading of a scan, not checked by a human: repeat that note"}}),
    _tool(api.compare, "Side-by-side comparison of investigations: question, fuels, tested ranges, sensors, key findings, limitations.", {
        "accessions": {"type": "array", "items": ACCESSION}, "findings": {"type": "integer"}}, ["accessions"]),
    _tool(api.coverage, "Count tests on a 2-D grid (default ambient O2 against pressure) and report which reference "
          "atmospheres (ISS cabin, Moon habitat, exploration, spacesuit) have no data. Use for gap questions. "
          "A reference's `nearest_test` lists in `not_measured` the columns filled from the investigation's stated "
          "range, not measured for that test.", {
              "x": {"type": "string"}, "y": {"type": "string"}, "x_step": {"type": "number"}, "y_step": {"type": "number"}, **TEST_FILTERS}),
    _tool(api.relevance, "Rank investigations by relevance to a fire-safety scenario and state how far the nearest real "
          "test is from it. fuel_phase weights the ranking and does not filter it: check `phase_match` on each row; "
          "`nearest_test` is always a test of that phase (null if none), and `closest_same_phase_test` is the nearest "
          "one overall. Never present `nearest_test_other_phase` as a test of the requested material. A condition a "
          "test dict lists in `not_measured` was not recorded for that test: a value shown for it is the middle of the "
          "investigation's range in `condition_ranges` (stated range or assumed cabin air), so say so when quoting it. "
          "Scenario names: " + ", ".join(api.SCENARIOS) + ".", {
              "scenario": {"type": ["string", "object"], "description": "scenario name, or {x_o2, pressure_kpa, flow_cm_s, gravity_g}"},
              "fuel_phase": {"type": "string", "enum": ["solid", "liquid", "gas"]}, "pillar": PILLAR, "top": {"type": "integer"}}),
    _tool(api.find_evidence, "Keyword search for passages: reviewed digest findings (with citation ids) and raw text of PSI "
          "documents (file and page; `transcribed` marks an AI model's reading of a scanned page). Keyword-based: use the "
          "documents' own terms and try synonyms.", {
              "query": {"type": "string"}, "accession": ACCESSION, "k": {"type": "integer"}, "raw": {"type": "boolean"}}, ["query"]),
    _tool(api.insights, "Cross-investigation synthesis entries with citations.", {
        "topic": {"type": "string", "enum": ["key_messages", "limits", "micro_vs_1g", "gaps", "lineage", "research_questions", "parameter_coverage"]},
        "accession": ACCESSION}),
    _tool(api.timeseries, "Sensor time series of one test (decimated) with summary features (burn duration, peak "
          "temperatures, chamber pressure). Available for PSI-10, PSI-23, PSI-39, PSI-159 and Saffire-I/III (PSI-98, "
          "PSI-100). For 24 PSI-39 droplet tests the investigators' reduced data (droplet diameter, hot- and "
          "cool-flame diameter, radiometer power against time) are a second recording: test_point "
          "\"FLEX-<test id>-reduced\". Reads the raw NASA files: from disk in a local copy; the demo server fetches each from NASA PSI on first use and caches it, so a recording nobody opened before fails with 502 while PSI is down.", {
              "test_id": {"type": "string"}, "channels": {"type": "array", "items": {"type": "string"}},
              "max_points": {"type": "integer"}, "test_point": {"type": "string"}, "accession": ACCESSION}, ["test_id"]),
    {**_tool(api.predict, "Small per-investigation statistical model. Without model_id: list models, their inputs, accuracy "
             "and valid domain. With model_id plus every input of that model as extra named arguments: prediction (none "
             "outside the fitted domain) and the nearest real tests. For a quantity: prediction and interval [low, high] in "
             "`unit`, interval_nominal (0.9, the target), interval_coverage (n_inside of n on held-out test days, "
             "per fuel under by.levels), interval_clipped and interval_low_unclipped (lower end cut at 0), interval_unclipped, "
             "interval_unavailable (why interval is null: the whole range is below 0), prediction_below_floor (the estimate "
             "itself is impossible), "
             "interval_method, accession (source). The full list is about 75 kB: pass compact=true "
             "to get only id, inputs with their valid domain, accuracy and what each model must not be used for.",
             {"model_id": {"type": "string"}}),
     "input_schema": {"type": "object", "properties": {
         "model_id": {"type": "string"},
         "compact": {"type": "boolean", "description": "with no model_id: the short list (about 5 kB)"}}, "required": [],
                      "additionalProperties": {"type": "number"}}},
    _tool(api.discrepancies, "Errors and doubts in the original PSI experiment tables: conflicts with the raw sensor data "
          "(table value, raw value, evidence, action taken), every value this dataset changed, flag meanings and counts, "
          "and statements resting on files PSI lists as removed. Use whenever the user asks about data quality or when "
          "showing a test whose row has flags.", {"accession": ACCESSION, "test_id": {"type": "string"}}),
]


def call(name, arguments):
    return api.FUNCTIONS[name](**arguments)
