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
    _tool(api.filter_tests, "Rows of the per-test table (2,177 tests: fuel, O2, pressure, flow, outcomes). Use for any "
          "question about what was tested and what happened.", {
              **TEST_FILTERS, "columns": {"type": "array", "items": {"type": "string"}}, "limit": {"type": "integer"}}),
    _tool(api.compare, "Side-by-side comparison of investigations: question, fuels, tested ranges, sensors, key findings, limitations.", {
        "accessions": {"type": "array", "items": ACCESSION}, "findings": {"type": "integer"}}, ["accessions"]),
    _tool(api.coverage, "Count tests on a 2-D grid (default ambient O2 against pressure) and report which reference "
          "atmospheres (ISS cabin, Moon habitat, exploration, spacesuit) have no data. Use for gap questions.", {
              "x": {"type": "string"}, "y": {"type": "string"}, "x_step": {"type": "number"}, "y_step": {"type": "number"}, **TEST_FILTERS}),
    _tool(api.relevance, "Rank investigations by relevance to a fire-safety scenario and state how far the nearest real "
          "test is from it. Scenario names: " + ", ".join(api.SCENARIOS) + ".", {
              "scenario": {"type": ["string", "object"], "description": "scenario name, or {x_o2, pressure_kpa, flow_cm_s, gravity_g}"},
              "fuel_phase": {"type": "string", "enum": ["solid", "liquid", "gas"]}, "pillar": PILLAR, "top": {"type": "integer"}}),
    _tool(api.find_evidence, "Keyword search for passages: reviewed digest findings (with citation ids) and raw text of PSI "
          "documents (file and page). Keyword-based: use the documents' own terms and try synonyms.", {
              "query": {"type": "string"}, "accession": ACCESSION, "k": {"type": "integer"}, "raw": {"type": "boolean"}}, ["query"]),
    _tool(api.insights, "Cross-investigation synthesis entries with citations.", {
        "topic": {"type": "string", "enum": ["key_messages", "limits", "micro_vs_1g", "gaps", "lineage", "research_questions", "parameter_coverage"]},
        "accession": ACCESSION}),
    _tool(api.timeseries, "Sensor time series of one test (decimated) with summary features (burn duration, peak "
          "temperatures, chamber pressure). Available for PSI-10, PSI-23, PSI-39, PSI-159 and Saffire-I/III (PSI-98, "
          "PSI-100). Needs the raw files on disk.", {
              "test_id": {"type": "string"}, "channels": {"type": "array", "items": {"type": "string"}},
              "max_points": {"type": "integer"}, "test_point": {"type": "string"}, "accession": ACCESSION}, ["test_id"]),
    {**_tool(api.predict, "Small per-investigation statistical model. Without model_id: list models, their inputs, accuracy "
             "and valid domain. With model_id plus every input of that model as extra named arguments: prediction (none "
             "outside the fitted domain) and the nearest real tests.", {"model_id": {"type": "string"}}),
     "input_schema": {"type": "object", "properties": {"model_id": {"type": "string"}}, "required": [],
                      "additionalProperties": {"type": "number"}}},
    _tool(api.discrepancies, "Errors and doubts in the original PSI experiment tables: conflicts with the raw sensor data "
          "(table value, raw value, evidence, action taken), every value this dataset changed, flag meanings and counts, "
          "and statements resting on files PSI lists as removed. Use whenever the user asks about data quality or when "
          "showing a test whose row has flags.", {"accession": ACCESSION, "test_id": {"type": "string"}}),
]


def call(name, arguments):
    return api.FUNCTIONS[name](**arguments)
