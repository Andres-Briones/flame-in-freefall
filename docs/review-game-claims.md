# Review of the claims made by the dashboard's games

Date: 2026-11-14

## What was reviewed

The teammates' dashboard app, repository `sebascs04/flame-in-freefall`, branch `origin/dev` at commit 34d41b3
(`web/src`). The review lists the factual and scientific claims the game-like parts make to a lay user (ship
simulator, relations-map mini-game, the mascot Sparky's lines, missions, quips, tours and their texts in
`web/src/i18n/en.json`) and checks each against this repository's data: the tests table, the evidence text, the
digest records and `data/digest/synthesis.json`. Three public NASA pages were used for claims that go beyond PSI.
Nothing in the app was changed.

## How to read the verdicts

- **SUPPORTED**: the source named in the evidence column says it.
- **SUPPORTED ONLY IN A NARROWER SCOPE**: true for the stated scope (fuel, shape, pressure, data set), not as
  written.
- **UNSUPPORTED / game choice**: no source we hold says it; a game rule or drawing presented as fact.
- **WRONG**: contradicted by the source named.
- **CITATION WRONG**: the statement may be fine, but the cited page or source does not say it.
- **NOT CHECKABLE**: cannot be checked with what we hold; the last section says what is needed.

Severity: high = a user would leave believing something false about fire safety; medium = misleading scope or
wrong citation; low = wording.

## Caveats

- The Saffire-V figures (rows 8 and 9) were read from a partial text extraction of the public paper ICES-2021-266
  (three of its pages failed to extract). A human should confirm Table 1 before the figures are used.
- The unpushed commit 8eec74b (rework of the map mini-game's counting) was not reviewed. Rows it would change are
  marked.
- The assistant chat (`web/src/assistant`, `api/`) generates statements live and was not reviewed.
- es/de were spot-checked only: every number matches en (only "2177" formatting differs), and the 19 key claims
  read side by side say the same thing.

## Three things to know first

- **The simulator does not use our data server.** It runs on a bundled `web/src/data/psi.json` holding 5
  investigations (FLEX, BASS-II, Saffire-I/II, SAME) with no BASS and no pressure or flow for BASS-II. Several
  "NASA never tested this" and "NASA burned this" statements are artefacts of that file.
- **"NASA never burned a solid below about 90 kPa" is false outside PSI.** Saffire-V (2021) burned cotton and PMMA
  in orbit at 70.7-72.6 kPa and 25.4-26.2% O2 (ICES-2021-266, Table 1; see caveats). Saffire-VI was not checked.
- **es/de add or change no claims.**

Abbreviations: `S` = `web/src/views/Simulator.jsx`, `M` = `web/src/views/RelationsMap.jsx`,
`en` = `web/src/i18n/en.json` (all in the teammates' repo). KM = key message in `data/digest/synthesis.json`;
F = finding in `data/digest/PSI-n.json`; Guide =
`PSI-23_Presentations_ISS Researchers Guide - Combustion In Reduced Gravity.pdf`.

## High severity

| id | where | claim | verdict | evidence | suggested text |
|---|---|---|---|---|---|
| 1 | S:135; en:246-250 `sim.game.runaway` | O2 > 30% means "Fire out of control", spreads fast, water mist puts it out | UNSUPPORTED and CITATION WRONG (established) | The rule fires for every material and always on the Mars mission. Nearest data show the opposite of runaway: BRE burned steadily at 34% O2 / 56 kPa (KM12); 9 FLEX droplet tests above 30% O2 at 71-72 kPa ended 8 disruption, 1 completion. No solid burned in orbit above 22.7% O2 in PSI; Guide p26 is about the water-mist extinguisher; Apollo 1 (p34) carries no oxygen figure. | Remove. "Above 22.7% oxygen no solid was burned in orbit in NASA's PSI records, so I don't guess." |
| 2 | S:136; en:241-245 `sim.game.outFlow`; en:272 | Fans off and O2 < 26.5% means the flame goes out | UNSUPPORTED as universal (established); WRONG for droplets | 26.5% is the lowest enriched level ACME BRE tested (gas burner, flames burned steadily there). The rule also applies to methanol and heptane. FLEX has no imposed flow (PSI-69 digest: "none (quiescent)") and 250 tests below 26.5% O2 burned (184 extinction after seconds, 43 disruption, 23 completion). The Mir candle burned over 45 min (Guide p30). | Restrict to solids: "In air, small solid-fuel flames went out when the fan was stopped (BASS, Saffire). Flames on a gas burner kept burning in still air at 26.5% oxygen or more (ACME BRE)." |
| 3 | en:272 `sim.challenge.list[0].lesson` | "A flame needs oxygen and moving air, so it dies ... when the fans stop" | WRONG | Guide p30 (Mir candle, flame balls 40 min); PSI-20 F1 (minutes in still air); PSI-26 F10 and Guide p31 (a local jet sustains the flame with ambient flow off). | "Lower the oxygen below the limit NASA measured for acrylic rods and the flame goes out. Stopping the fans put out small flames in air, but not every flame." |
| 4 | en:77-79 `home.myths[1]` | "Cut the airflow and the fire goes out" shown as a myth | WRONG framing; body text SUPPORTED (Guide p31) | PSI-99 F9: "Turning off the flow put the thick-PMMA flames out quickly. This supports the ISS response of shutting down ventilation." Also PSI-98 F5, PSI-100 F6, PSI-26 F11, KM7. The app's own Experiments cards say the same. | Myth: "Less wind always means less fire." Orbit: "A gentle breeze of about 10 cm/s is where solids burn at the lowest oxygen and spread fastest. Stopping the air did put out small flames in normal air." (Guide p31; Saffire-II) |
| 5 | S:30-39, 106, 138; `web/src/lib/data.js`:37-38; en:251-255, 184, 155, 167 | PMMA at 21% O2 and 10 cm/s (the default cabin) gives "NASA never tested this"; "tested from 20 to 20 cm/s"; "42 tests" | WRONG | The flow envelope is one Saffire-II row. Tests table: 176 PMMA tests (BASS-II 96, BASS 78, Saffire-II 2), flow recorded on 39 rows from 0 to 20 cm/s, O2 13.6-22.6% (app shows 14.2-22.2). Eq. 6.1 data span under 1 to about 38 cm/s. "Burning" is reachable only at exactly 20 cm/s, and challenge 3 is won by the default state. | Take the envelope from the data server (`filter_tests`, `coverage`). "NASA burned acrylic at 13.6-22.6% oxygen and 0-20 cm/s; airflow was recorded for 39 of 176 tests." |
| 6 | S:105-106, 138-139; en:183, 233, 258 | "NASA burned this material in air like this" / "Close to what NASA tested" | WRONG | Unrecorded dimensions are ignored, so pressure is never checked for any solid (PMMA at 20 kPa, 21%, 20 cm/s gives "I'm burning... NASA burned this in air like this"). Kapton, lampwick and dibutyl phthalate have no recorded dimension, so they are always "inside"; Teflon is judged on flow only. | An unrecorded dimension must give "not recorded, cannot compare", never "inside". |
| 7 | en:126 tour; en:258; en:494 `map.lead`; en:523; M:10 | The materials list is "the ones NASA really burned in orbit"; "Each ball is something NASA set on fire in space" | WRONG for SAME and SAME-R materials | PSI-101 and PSI-102 overheated materials "without burning" (digest one-lines; the app's own `map.inv.PSI-101` says so). Affects the map balls Kapton 29, lampwick 20, Pyrell 20, Teflon 18, silicone 22 of 26, and the simulator's Teflon, Kapton, lampwick, dibutyl phthalate. | "...burned or overheated in orbit". Label these balls "heated to make smoke, not set on fire". |
| 8 | en:134, 195, 196, 282 (tour, `quip.pLow`, `quip.pSea`, challenge 3 lesson) | "NASA never burned a solid below about 90 kPa"; "Every solid ... between 12 and 24% oxygen and 90 to 110 kPa" | WRONG as a statement about NASA; SUPPORTED ONLY for PSI records, and only where pressure exists | Tests table: solid pressure is recorded on 125 of 379 rows (98.3-102.6 kPa), none for BASS-II, Saffire-II or SAME; O2 is 13.6-22.7%, not 12-24. Saffire-V burned solids at about 71-73 kPa (see caveats). | "In NASA's PSI records, every solid with a recorded pressure burned near 1 atm (98-103 kPa) at 13.6-22.7% oxygen. Saffire-V later burned cotton and acrylic at about 71 kPa and 26% oxygen (not in PSI)." |
| 9 | en:31-34, 220, 541-548, 563, 488; `web/src/components/Scoreboard.jsx`:42 | "0 solid materials NASA has burned in that air"; "Never tested by NASA"; "Nobody knows yet what happens" | SUPPORTED ONLY for PSI's 24 investigations | `coverage(fuel_phase="solid")` gives 0 in the moon-habitat cell and the nearest test BASS 2 at 22.7% / 100.8 kPa. Saffire-V at 26% / 71 kPa is closer but below 30%. "Nobody knows" ignores BRE emulation and droplets at 30-34% (KM12). | "In NASA's PSI records no solid was burned at 30% oxygen or more. The closest orbit test we know of is Saffire-V at about 26% and 71 kPa." |
| 10 | S:109-114, 137; en:186-188, 233, 238, 308-310 | PMMA goes out or burns by the "NASA limit" | SUPPORTED ONLY IN A NARROWER SCOPE (established) | BASS-II Summary Report p83 Eq. 6.1, correctly implemented: lit flames on rods, about 1 atm, O2 13.6-22.2%, flow under 1 to about 38 cm/s. The app's "PMMA" group is mostly films, and the "out" rule fires before the tested-range check, at any pressure. The margin is also shown as flame size. | "For an acrylic rod already burning at about 1 atm..."; show nothing for other shapes or pressures. |

## Medium severity

| id | where | claim | verdict | evidence | suggested text |
|---|---|---|---|---|---|
| 11 | en:277 challenge 2 lesson | "NASA measured the exact oxygen limit ... not a guess" | UNSUPPORTED (overclaim) | Eq. 6.1 is an empirical fit for one rod geometry (KM1: "mapped on one rod geometry and one fabric"). | "NASA fitted a limit curve to its acrylic-rod tests; inside those tests the answer rests on data." |
| 12 | S:139; en:256-259 `unknownNoRule` | NASA "published no rule" for non-PMMA materials | WRONG for droplets | PSI-69 F1: LOI 0.12 (methanol) and 0.15 (heptane) in O2/N2. `web/src/components/Scoreboard.jsx`:7-12 quotes that very limit. | "For methanol drops NASA found a limit near 12% oxygen, for heptane 15% (FLEX)." |
| 13 | en:38-40 `home.nums[2]`; en:106 `scene.intro[2]`; en:487 | "2,177 fires NASA recorded in orbit"; "NASA lit 2,177 fires like me"; "real fires in the tables" | WRONG | 2,177 rows are 2,059 single tests, 100 day summaries, 10 condition sets and 8 planned. Of the 2,059, 109 are SAME-R (PSI-101) smoke tests with no flame (corrected 2026-11-14: an earlier version of this review said "116 are SAME smoke tests", which was wrong; SAME, PSI-102, has 8 rows, all `planned`, outside the 2,059), so 1,950 are fire tests; 62 have `ignited = False`. The map's count note already says 2,059. | "2,059 single tests in orbit (flames, plus smoke and no-ignition tests)". |
| 14 | en:486, 403, 62 | "24 NASA fire experiments"; an investigation is "one NASA experiment in orbit" | WRONG for 5 of 24 | PSI-60, 62, 115, 117 and 142 are ground or modelling studies; 19 have test tables; DAFT, SAME and SAME-R burned nothing. | "24 NASA investigations: 19 flown in orbit, 5 ground or computer studies." |
| 15 | S:114; en:116, 193; `web/src/components/Sparky.jsx`:11-16 | "Raise the oxygen and watch me grow"; flame size is the oxygen margin; mood thresholds 15/24/32% | UNSUPPORTED game choice | For the spherical flame Sparky depicts, PSI-10 Final Report says "Flame size ... decreases with ambient oxygen concentration" (reviewer's inference that this applies to Sparky). | Drop the size cue or label it "drawing, not data". |
| 16 | S:152; en:286-288 challenge 4 | "Survive" Mars means igniting at 30% O2 or less | UNSUPPORTED | It rests on rule 1; once that rule is removed the challenge is always won. | Redesign: "Find what NASA has tested closest to the Mars-ship air." |
| 17 | S:17-21; en:225-226, 287-288 | "NASA recommends 34% oxygen at 56.5 kPa (8.2 psi) for exploration ships"; "to make spacewalks easier"; NTRS 20220005716 | NOT CHECKABLE | The NTRS record is a 2022 AsMA panel talk on exploration atmospheres and decompression; its metadata has no numbers and the PDF was not read. PSI-20 digest corroborates 34% / 8.2 psia as a "NASA-considered" atmosphere. "Trip to Mars" is unsourced. | "One atmosphere NASA considers for exploration vehicles is 34% oxygen at 56.5 kPa." |
| 18 | en:27-28, 220 | "30% oxygen planned"; "The plan here is 30% at 70.3 kPa" | SUPPORTED ONLY IN A NARROWER SCOPE | Challenge text as quoted in `docs/digest/reference.md`: "will likely be 30% or greater, with a corresponding pressure of 10.2 psi or less". | "likely 30% oxygen or more at 70.3 kPa or less". |
| 19 | en:199 `quip.flowBreeze`; en:713 | 10 cm/s is "exactly" where solids burn at the lowest oxygen | SUPPORTED ONLY IN A NARROWER SCOPE | Guide p31 says "on the order of 10 cm/s". BASS-II rods had the minimum at about 1.7-2.5 cm/s (PSI-25 F6), and the simulator's own Eq. 6.1 puts it at 2.2 cm/s. | "close to where" instead of "exactly where". |
| 20 | en:138, 243, 713 | Fans "are what bring fresh oxygen"; "nothing brings me fresh oxygen" | SUPPORTED ONLY IN A NARROWER SCOPE | Diffusion alone sustained the Mir candle and flame balls (Guide p30) and BRE flames (PSI-20 F1). | "Without fans oxygen only seeps in slowly, so many flames weaken or go out." |
| 21 | en:82-84 `home.myths[2]` | BASS: materials burn at lower oxygen in orbit than in NASA's ground test | SUPPORTED by Guide p31; NARROWER per digest | KM2: the comparisons are with downward 1-g burning, not Test 1 itself. KM3: Test 1 was conservative for Ultem, Nomex and silicone. | Say "some materials". |
| 22 | `web/src/components/Scoreboard.jsx`:7-12; en:489 | "12% lowest oxygen a flame survived" | SUPPORTED ONLY IN A NARROWER SCOPE | It is the methanol-droplet LOI in N2 at 1 atm; 8 tests at 0.12 burned 5-11 s then went out. A FLEX xenon test at 8% O2 is referenced in PSI-117 F8. | "12%: lowest oxygen where a methanol drop still burned (nitrogen-diluted air)". |
| 23 | S:348; `web/src/data/psi.json` PSI-69 row 114 | Methanol "tested from 0 to 309.3 kPa" | WRONG | The bundled row has raw pressure "0" mmHg; the tests table's FLEX minimum is 70.2 kPa. | Use the data server's values. |
| 24 | M:45-48; en:557, 567-568, 574 | "NASA's records: k of 10 went out" | SUPPORTED ONLY IN A NARROWER SCOPE (8eec74b changes the counting, not this) | The denominator is stated endings only: PMMA 73 of 176, SIBAL 5 of 45. BASS endings are our reading of crew notes, not a NASA column. Nomex: the question says "If NASA lit..." but 5 of 5 stated never ignited. | "In the tests with a known ending..."; require a larger stated share; skip never-lit materials. |
| 25 | M:24-28, 42-43 | Crew-driven extinctions counted as "went out"; comment "most flames go out on their own" | WRONG (established; fixed in unpushed 8eec74b) | PMMA 8 of 10; only 2 of 61 PMMA extinctions were unprovoked. | n/a |
| 26 | en:198 `quip.flow0` | Small flames go out in normal air; at 26.5% or more they burned for minutes | SUPPORTED ONLY IN A NARROWER SCOPE (established) | KM7, PSI-20 F2: a 25 mm gas burner; "not a material flammability limit". Fan-off extinction was observed for 24 small PMMA/wax runs at 17.1-22.4% O2, about 100 kPa. | Add "on a gas burner that imitates solids". |
| 27 | en:544, 547 | "Nobody knows yet what happens" | UNSUPPORTED | See row 9. | See row 9. |
| 28 | en:197 `quip.pHigh` | "More pressure means more oxygen molecules reaching me" | UNSUPPORTED | There is no solid flight data off 1 atm (gap 5 in the synthesis). | "NASA's PSI solid tests were all near 1 atm, so I can't say what pressure does." |
| 29 | en:134, 709 (cites the challenge text) | "lower pressure makes a ship lighter"; "thinner air saves weight" | NOT CHECKABLE | The challenge quote we hold gives no reason, and en:287 gives a different one (spacewalks). | Drop the reason or cite it. |
| 30 | en:28 | "so there everything burns more easily" (Moon air) | UNSUPPORTED for that atmosphere | It is untested for solids (KM12) and the same site says nobody knows. | "More oxygen generally makes materials easier to burn." |
| 31 | Experiments "What NASA found" cards (`web/src/data/summaries.json`) | PSI-25 F12 "showing it is an excellent fire barrier"; PSI-117 F8 "droplets can burn with only about 5% oxygen" | SUPPORTED ONLY IN A NARROWER SCOPE | F12 is 3 samples, the authors' words are "excellent result for ISS", and Nomex III is contradictory in KM3. F8 is a xenon simulation, not a test. | Add "in three tests" and "in computer models, with xenon". |

## Low severity

| id | where | claim | verdict | evidence |
|---|---|---|---|---|
| 32 | en:194 `quip.o2Max` | Apollo 1 "cabin ran on pure oxygen", cited "Apollo 1, NASA" | NOT CHECKABLE with holdings | Guide p34 names Apollo 1 without an oxygen figure. The quip fires at anything above 30%. |
| 33 | en:215 | The station is "where NASA lit most of its fires" | SUPPORTED ONLY IN A NARROWER SCOPE | By place: 2,046 of 2,059 tests. By air: only 492 of 1,143 tests with recorded O2 were at 20-22%. The cite ("solid tests") does not fit. |
| 34 | en:721 glossary droplet | "about 2 mm wide" | WRONG | FLEX `d0_mm`: median 3.0, range 1.1-4.67, n = 262. Use "about 3 mm". |
| 35 | en:717 glossary extinction | "goes out by itself" | SUPPORTED ONLY IN A NARROWER SCOPE | Many recorded endings were crew-driven (33 flow reduced, 24 shut off, 2 nitrogen). |
| 36 | en:22, 66, 105, 701 | "Fire is a sphere"; "a blue ball" | SUPPORTED ONLY IN A NARROWER SCOPE | True for still-air small flames. Saffire flames were yellow with a blue base (PSI-98 F5), and microgravity flames are sootier (KM10). |
| 37 | en:191, 202 `quip.o2Low` | Rods burned down to 13.5%, cited "BASS-II, key message 1" | SUPPORTED; CITATION not resolvable by a user | PSI-25 F6, Summary Report p83. "Key message 1" is our synthesis numbering; cite the report page. |
| 38 | en:72-74 `home.myths[0]` | Mir candle burned over 45 min at lower oxygen | SUPPORTED | Guide p30 ("in some tests"). |
| 39 | en:176 `sim.marginP` | The Eq. 6.1 description | SUPPORTED | Established; it states its own scope. |
| 40 | en:506, 546; S:19-21; en:684-693 | 2,059 count note; nearest Moon test (within PSI); 10.2 psi = 70.3 kPa and 8.2 psi = 56.5 kPa; map investigation names | SUPPORTED | `filter_tests` gives n_matching 2,059; coverage; digest one-lines for PSI-98, 99, 100, 101. |

Not in the table: the fuel and material descriptions (en:292-304, 585-680, for example Pyrell "used to pack items
for launch", farnesane "made from sugar") are general knowledge, NOT CHECKABLE with what we hold, and low risk.
"You now know more ... than most people on Earth" is fluff.

Background established before this review and used above: no per-test pressure exists for BASS-II or Saffire-II;
Saffire-I pressure is a pre-ignition sensor value with a second sensor about 2.5 kPa lower; the Moon-habitat
atmosphere (30% O2, 70.3 kPa) has no solid test, and the tests table's solids reach 22.7% O2 at most.

## Other views that state facts

- **Home:** the three numbers, three myths and lede (rows 4, 13, 18, 21, 30, 36, 38).
- **Experiments:** the Scoreboard (rows 9, 13, 14, 22); the "What NASA found" cards with their note "each number
  was checked against the record"; the chart reference lines "Moon base plan" at 30% and 70.3 kPa (row 18); the
  tour (row 14).
- **Glossary pop-ups** (`web/src/lib/glossary.js`): shown in all views (rows 19, 20, 29, 34, 35).
- **Assistant chat** (`web/src/assistant`, `api/`): generates statements live; not reviewed.

## Patterns

1. **PSI scope dropped.** "NASA never..." is written where only "in the 24 PSI investigations" is supported
   (rows 8, 9, 27).
2. **Missing data read as a fact.** Unrecorded pressure or flow becomes "inside" or "never tested"; a single row
   becomes a range; a raw "0" becomes a tested pressure (rows 5, 6, 23).
3. **One result stretched over all fuels.** The fan-off, runaway and PMMA-rod rules are applied to droplets, films
   and smoke-test materials (rows 1, 2, 10, 12).
4. **Rows counted as fires.** Day summaries, planned tests, smoke tests and model studies are all called fires or
   experiments in orbit (rows 7, 13, 14).
5. **Absolute wording.** "exactly", "exact limit", "needs moving air", "nobody knows", "everything"
   (rows 3, 11, 19, 27, 30).
6. **The app contradicts itself.** The Home myth disagrees with the Experiments cards and the simulator's fan-off
   rule; "never below 90 kPa" disagrees with "burned in air like this" at 20 kPa; "no rule" disagrees with the
   Scoreboard's LOI.
7. **Citations a user cannot follow or that do not carry the claim.** "key message 7", "coverage",
   "Apollo 1, NASA", the NTRS talk, and the challenge text cited for a reason it does not give.

The established errors recur elsewhere: the fan-off belief in challenge 1 and the tour; the "above 30% is danger"
threshold in challenge 4, Sparky's mood and the Apollo quip; the "no solid at this pressure" claim in four more
strings.

## Could not check, and what is needed

- **Row 17:** the PDF of NTRS 20220005716, or the Exploration Atmospheres Working Group report.
- **Row 9:** Saffire-VI test conditions (ICES-2024-365), to confirm no orbit solid test at 30% O2 or more.
- **Row 8:** the three pages of ICES-2021-266 that failed text extraction; a human read of Table 1 would confirm
  the figures.
- **Rows 29, 30:** the full challenge page.
- **Row 32:** a NASA Apollo 1 source.
- **Fuel descriptions:** vendor or NASA material sheets.
- **Row 31:** 7 of the 72 findings behind the cards were spot-checked against the digest; the "each number was
  checked" note is otherwise unverified.

## Count by verdict (40 rows)

| verdict | count | rows |
|---|---|---|
| WRONG | 11 | 3, 4, 5, 6, 7, 8, 12, 13, 14, 23, 34 |
| WRONG, already fixed in 8eec74b | 1 | 25 |
| UNSUPPORTED / game choice | 8 | 1 (also citation wrong), 2, 11, 15, 16, 27, 28, 30 |
| SUPPORTED ONLY IN A NARROWER SCOPE | 13 | 9, 10, 18, 19, 20, 21, 22, 24, 26, 31, 33, 35, 36 |
| NOT CHECKABLE | 3 | 17, 29, 32 |
| SUPPORTED | 4 | 37 (citation weak), 38, 39, 40 |

## External sources

- [Fire Safety Implications of Preliminary Results from Saffire IV and V (ICES-2021-266)](https://ntrs.nasa.gov/api/citations/20210011521/downloads/ICES%202021-266%200503-2021%20final.pdf)
- [NTRS 20220005716 record](https://ntrs.nasa.gov/api/citations/20220005716)
- [Preliminary Results from the Saffire VI Experiment](https://ntrs.nasa.gov/citations/20240002981) (search result
  only, not read)

## Re-check on dev 1cdb110 (2026-11-14)

The same app at `origin/dev` commit 1cdb110 (`web/src`), compared with 34d41b3 through
`git diff 34d41b3 1cdb110 -- web/src`. The teammates said rows 4, 7, 9, 13, 18, 21, 24, 30 and 36 were fixed on Home
and the map (c50ebf1), plus the Scoreboard, glossary, tour and two Dashboard findings (939d351) and Sparky's intro and
tour (1cdb110). Each row below was checked in the current text, in en, es and de. Every changed string was changed in
all three languages, and the numbers match (only the "2,059" / "2.059" formatting differs). Line numbers are `en` at
1cdb110. Nothing in the app was changed.

Numbers re-run on 2026-11-14 with `fif.api`, on the working tables and on the committed `tests.parquet`, which gave the
same results (other agents were rebuilding the data at the time, so the working copy differed from the commit in other
columns): 2,059 single tests (`filter_tests`, `n_matching`); 109 SAME-R smoke tests (PSI-101), so 1,950 fire tests;
62 with `ignited = False`, none of them SAME-R; solid pressure on 125 rows, 98.3-102.6 kPa; solid O2 13.6-22.7%; FLEX
`d0_mm` median 3.0 mm (n = 262); 24 investigations, 19 flown (`search_investigations`, `flight`); moon-habitat cell
0 solid tests, nearest BASS 2 SIBAL at 22.7% / 100.8 kPa (`coverage(fuel_phase="solid")`).

The simulator's rules (rows 1, 2, 3, 5, 6, 10, 16, and the sim strings of rows 8, 9, 26 and 32) are the subject of our
PR #3 (`sim-applicability`). It is still open, and GitHub reports it as conflicting with dev. It was written before
the lever bands, the console info texts and the smoke-only result, so it does not cover them.

### Status of the original rows

| row | status | current text at 1cdb110 (short quote) | what remains |
|---|---|---|---|
| 1 | still open | en:246-250 `sim.game.runaway` unchanged; S:145 `o2 > 30 ? 'runaway'` | Same rule and text. The new lever band repeats it ("fire out of control", S:188). PR #3 removes the rule, not the band. |
| 2 | still open | en:241-245 `sim.game.outFlow` unchanged; S:146 | The rule still applies to droplets. The new lever band "the flame goes out" (S:189) repeats it. PR #3. |
| 3 | still open | en:277 "A flame needs oxygen and moving air, so it dies ... when the fans stop." | Unchanged. PR #3 rewrites it. |
| 4 | fixed | en:77-79 "Less wind always means less fire" ... "Stopping the air did put out small flames in normal air." | Nothing. It now agrees with PSI-99 F9 and Guide p31. Low: de adds an absolute ("ist genau dort", "is exactly where"), see row 19. |
| 5 | still open | en:184 `say.outside`, en:155, en:167 unchanged; `web/src/data/psi.json` and `lib/data.js` unchanged | The PMMA flow range is still one Saffire-II row ("20 to 20 cm/s"). The new flow band shows it: green only at 20 cm/s. PR #3 changes the wording but leaves `psi.json` to the web team. |
| 6 | still open | S:111-114 envelope logic unchanged; en:183 "NASA burned this material in air like this" | An unrecorded dimension is still "inside". A new contradiction: for Kapton, Teflon, lampwick, silicone and dibutyl phthalate, Ignite now says "Only smoke ... overheated without burning", while Sparky's line (S:137, `say.inside`) and the panel ("Close to what NASA tested") still say NASA burned it in air like this. PR #3 (verdict `incomplete`). |
| 7 | partly fixed | en:126 tour "burned or overheated in orbit"; en:536 map "set on fire in space, or tried to"; the map drops SAME-R rows (M:49, M:224); the simulator gives SAME materials smoke only (S:144) | The new console text en:337 `sim.info.controls.body` repeats the old claim, in all three languages: "you only get the ones NASA really burned in orbit". Low: `map.svgLabel` (en:539) says "material NASA burned in space". |
| 8 | partly fixed | en:134 tour: "In NASA's PSI records every solid with a recorded pressure burned near 1 atm (98 to 103 kPa); Saffire-V later burned cotton and acrylic at about 71 kPa, outside PSI." | The tour is fixed (98.3-102.6 kPa re-verified; the Saffire-V caveat still applies). Still unchanged: en:195 `quip.pLow` "never burned a solid below about 90 kPa", en:196 `quip.pSea` "between 90 and 110 kPa", and en:287 challenge 3 "between 12 and 24 % oxygen and 90 to 110 kPa". PR #3 changes all three. |
| 9 | partly fixed | en:33 "0 solid materials burned at 30% oxygen or more, in NASA's public experiment archive"; en:522 Scoreboard "in NASA's PSI records"; en:585-589 map "Not in NASA's public records" | Home and Scoreboard are fixed. The map says "NASA's public records", which is wider than what we checked (PSI plus Saffire-V; Saffire-VI not read). Say "NASA's PSI records", as en:522 does. en:220 `mission.moon.say` "NASA never burned a solid in air like this" is unchanged (PR #3). The suggested "closest orbit test we know of is Saffire-V" was not added. |
| 10 | still open | en:186-188, 233, 238, 313-315 unchanged | No rod, 1 atm or lit-flame scope. The new en:341 `sim.info.burn.body` also leaves the scope out (see new claims). PR #3. |
| 11 | still open | en:282 "NASA measured the exact oxygen limit for acrylic rods, so in this air the result is not a guess." | Unchanged. PR #3 does not touch challenge 2. |
| 12 | still open | en:258 `unknownNoRule` "published no rule"; en:315 `simple.noRule` | Unchanged. The new en:341 adds "the only rule NASA published". The Scoreboard still quotes the FLEX LOI (PSI-69 F1), so the app still contradicts itself. PR #3 drops `simple.noRule` but keeps `unknownNoRule`. |
| 13 | fixed | en:38-39 "2,059 single tests in orbit ... flames, plus smoke and no-ignition tests"; en:106 Sparky "NASA ran 2,059 single tests in orbit"; en:521 Scoreboard; en:548 map "single fire tests (1,950)" | Nothing in the cited strings. 2,059, 109 smoke tests, 62 never lit and 1,950 fire tests are re-verified (the earlier 116 in row 13 was our error, corrected above). Low, not in the original row: the Dashboard tour (en:436, 438) still calls every bar entry "fires NASA lit", including PSI-101's smoke tests. |
| 14 | fixed | en:520 "NASA investigations: 19 flown in orbit, 5 ground or computer studies"; en:437 "one NASA study, most of them flown in orbit" | Nothing (19 of 24 have `flight = True`). Low: en:62 "The 24 NASA investigations with every test" (5 have no table). |
| 15 | still open | en:116 `poke` "Raise the oxygen and watch me grow"; en:193 "I'm getting bigger"; `Sparky.jsx`:11-16 unchanged | Unchanged. Not in PR #3. |
| 16 | still open | en:291-293 challenge 4 unchanged | It still rests on rule 1. PR #3 redesigns it. |
| 17 | still open (NOT CHECKABLE) | en:225 "NASA recommends 34 % oxygen at 56.5 kPa ... for exploration ships"; en:292 | Unchanged. The same values now also mark the Mars position on the levers. |
| 18 | partly fixed | en:28 "30% oxygen or more is likely for a Moon base, at lower pressure"; en:459-461 "Moon base, likely"; en:760 glossary "about 70 or less" | Unchanged: en:220 "The plan here is 30 % oxygen at 70.3 kPa" and en:193 "A Moon base would run at 30 % oxygen". |
| 19 | partly fixed | en:764 glossary "close to 10 cm/s"; en:78 myth "about 10 cm/s" | en:199 `quip.flowBreeze` still says "exactly where solids burn at the lowest oxygen". In de, `home.myths[1].p` adds "genau dort" ("exactly there"); en and es do not. |
| 20 | partly fixed | en:138 tour and en:764 glossary: "without fans oxygen only seeps in slowly, so many flames weaken or go out" | en:243 `outFlow` "nothing brings me fresh oxygen" is unchanged. The new en:337 `sim.info.controls.body` brings the claim back: fans are "the only thing that brings fresh air to a flame". |
| 21 | fixed | en:83 "some materials burn at lower oxygen in orbit than when the same samples burn downward on Earth" | Nothing (KM2). |
| 22 | fixed | en:523 "lowest oxygen where a methanol drop still burned (nitrogen-diluted air)" | Nothing (PSI-69 F1). |
| 23 | still open | `web/src/data/psi.json` unchanged | FLEX still "tested from 0" kPa. Our tests table minimum is 70.2 kPa. |
| 24 | fixed | en:604 "In the tests where NASA wrote down how {{name}} ended, how many of every 10 went out on their own?"; M:276-278 at least 30% stated and fewer than half never lit; en:625 caveat | Re-run: SIBAL (5 of 45 stated) and Nomex (never lit) no longer play; PMMA 2 of 72 stated went out unaided (0 of 10). Low: for BASS and BASS-II the endings are our reading of crew notes, yet the text says "NASA wrote down" and "NASA's records". |
| 25 | fixed | M:37, M:86-90; en:551-555 "Went out on its own" / "Put out on purpose" | 8eec74b is in dev. BASS/BASS-II extinctions count as unaided only with `outcome_action = none` (6 rows). |
| 26 | still open | en:198 `quip.flow0` unchanged | PR #3 rewrites it. |
| 27 | fixed | en:586, 589 "Nobody knows yet" removed; "That answer is still missing." | Nothing (scope: see row 9). |
| 28 | still open | en:197 `quip.pHigh` "More pressure means more oxygen molecules reaching me" | Unchanged. Not in PR #3. |
| 29 | text removed | en:134 and en:760 no longer give a reason for low pressure | Nothing. en:292 (challenge 4) still gives "to make spacewalks easier" (row 17). |
| 30 | fixed | en:28 "more oxygen generally makes materials easier to burn" | Nothing in en:28. en:193 `quip.o2High` still says "that makes everything easier to burn". |
| 31 | fixed | `summaries.json` PSI-25 F12 "In three tests ... which the authors called an excellent result for the ISS"; PSI-117 F8 "In computer models with xenon" | Nothing. es and de say the same. |
| 32 | still open (NOT CHECKABLE) | en:194 `quip.o2Max` and en:248-249 still cite "Apollo 1, NASA" | PR #3 replaces `o2Max` and removes `runaway`. |
| 33 | still open | en:215 "This is where NASA lit most of its fires", cite "NASA PSI solid tests (coverage)" | Unchanged. |
| 34 | fixed | en:772 "about 3 mm wide ... its flame forms a ball around it" | Nothing (median 3.0 mm, n = 262). |
| 35 | fixed | en:768 "either by itself ... or because the crew cut the air flow or added nitrogen" | Low: 7 BASS-II extinctions came from the crew raising the flow (`flow_raised`), which the text lists as "too much air" under "by itself". |
| 36 | partly fixed | en:66 lede "a small flame in still air ... a round, mostly blue ball"; en:752 glossary | Unchanged: en:22 `home.title1` "In orbit, fire is a sphere." and en:105 `scene.intro[1]` "I turn into a ball. A blue one." |
| 37 | still open | en:202 cite "BASS-II, key message 1" | Unchanged (low). |
| 38 | no fix needed | en:73 unchanged | SUPPORTED (Guide p30). |
| 39 | no fix needed | en:176 unchanged | SUPPORTED. |
| 40 | no fix needed | en:548 count note now "single fire tests in orbit ({{n}})", n = 1,950; en:588 nearest Moon test unchanged | SUPPORTED: 2,059 − 109 SAME-R = 1,950; coverage gives BASS 2 SIBAL. |

Count: fixed 12 (4, 13, 14, 21, 22, 24, 25, 27, 30, 31, 34, 35); text removed 1 (29); partly fixed 7 (7, 8, 9, 18,
19, 20, 36); still open 17 (1, 2, 3, 5, 6, 10, 11, 12, 15, 16, 17, 23, 26, 28, 32, 33, 37); no fix needed 3 (38, 39,
40); changed but now wrong in a new way 0. Rows 7 and 20 were fixed where the review pointed, but the same claim
came back in a new text (en:337). Of the 17 still open, PR #3 would close 1, 2, 3, 6, 10, 16, 26 and 32 and part of 5.
Rows 11, 12 (`unknownNoRule`), 15, 17, 23, 28, 33 and 37 are not in any change we know of.

Against the teammates' statement: rows 4, 13, 21, 24 and 30 are fixed as claimed. Rows 7, 9, 18 and 36 are fixed on
Home and the map but not in the simulator strings listed above. The Scoreboard, glossary, Dashboard tour and the two
findings (rows 14, 22, 31, 34, 35, 29) are fixed. The glossary fixed rows 19 and 20 only in the glossary. Sparky's
intro and tour are fixed (2,059, PSI scope for pressure, "burned or overheated", fans).

### New claims since 34d41b3

| id | where | claim | verdict | evidence | severity |
|---|---|---|---|---|---|
| N1 | en:337 `sim.info.controls.body` | "you only get the ones NASA really burned in orbit" | WRONG | Same as row 7: SAME overheated its materials "without burning" (PSI-102 digest one-line). The app's own tour (en:126) and smoke-only result (en:263) say so. | medium |
| N2 | en:337 `sim.info.controls.body` | Fan air "in space is the only thing that brings fresh air to a flame" | SUPPORTED ONLY IN A NARROWER SCOPE | Same as row 20: diffusion alone kept the Mir candle and flame balls burning (Guide p30), and BRE flames too (PSI-20 F1). The app's tour and glossary now say this correctly. | medium |
| N3 | en:341 `sim.info.burn.body` | "the only rule NASA published to know whether a flame stays alive ... For the others there is no published rule"; the rule "compares your oxygen with the minimum that flame needs at the wind you chose" | WRONG for droplets; the scope is missing (simulator rule text: PR #3 scope, but PR #3 predates this text) | Row 12 (PSI-69 F1: LOI 0.12 methanol, 0.15 heptane, quoted by the app's own Scoreboard); row 10 (Eq. 6.1: lit rods, about 1 atm). | medium |
| N4 | en:345 `sim.info.tested.body` | The panel shows "whether your air falls inside what NASA tested, looking at oxygen, pressure and wind one by one" | covered by PR #3 (rows 5, 6) | An unrecorded dimension is skipped, and "what NASA tested" is the 5 investigations in `psi.json`. | (PR #3) |
| N5 | S:179-202, en:348-352 `sim.zones` lever bands and legend | "fire out of control" above 30% O2; "the flame goes out" with fans off below 26.5% or under the PMMA limit; "NASA tested it" / "never tested" | covered by PR #3 (rows 1, 2, 5), but PR #3 predates the bands | The bands use the rules PR #3 removes. They are also drawn for smoke-only materials: Kapton above 30% shows "fire out of control" although its Ignite result is "Only smoke". "Never tested" means outside `psi.json`, not outside NASA's tests. | (PR #3); the bands need the same change when PR #3 is rebased |
| N6 | S:18-21, 205-213 mission marks on the levers | Moon at 30% / 70.3 kPa, Mars at 34% / 56.5 kPa | as rows 18 and 17 | The challenge text says "30% or greater" at "10.2 psi or less". The Mars figure is NOT CHECKABLE (row 17). | low |
| N7 | en:261-265 `sim.game.smokeOnly`; S:144; `PixelScene.jsx` `MATERIAL_SHAPE` | "In NASA's SAME experiment this material was overheated without burning, to measure its smoke and design better smoke detectors" (Teflon, Kapton, silicone, lampwick, dibutyl phthalate) | SUPPORTED; silicone narrower | PSI-102 digest: "Teflon, Kapton, silicone rubber, cellulose lamp wick and a reference liquid (dibutyl phthalate on a wick) were heated below ignition"; purpose: smoke detectors. 4 of the 5 bundled silicone rows are Saffire-II, which lit silicone sheets that did not spread a flame (PSI-99 one-line). Our tests table holds SAME's 8 rows as `planned`. | low |
| N8 | Sparky line S:137 with a SAME material | "NASA burned this material in air like this" | WRONG (row 6 logic, new contradiction) | It contradicts N7 on the same screen. PR #3's `incomplete` verdict would replace it. | medium (PR #3) |
| N9 | en:625 `map.game.caveat` | "NASA chose these tests close to the limit on purpose, so this is not the chance that the material goes out in a real spacecraft" | SUPPORTED | PSI-26 F5, F6: the crew stepped the flow down toward quenching; FLEX measured the LOI (PSI-69 F1), so its tests reached the limit. It narrows the claim instead of stretching it. | low |
| N10 | en:551-555, M:37 | "Went out on its own" / "Put out on purpose"; the game answers "k of every 10 went out on their own" | SUPPORTED | Re-run with the map's rules (SAME-R rows dropped, 1,950 rows): PMMA 0, propane 8, methanol 8, butane 6, ethane 6, heptane 5, Japan wax 0, paraffin 5 of 10. CFI-G `flow_terminated` (time-outs and burner temperature cut-offs, `docs/methods.md`) counts as stopped. Low: BASS endings are crew-note readings (row 24). | low |
| N11 | en:548 `map.countNote` | "Counts single fire tests in orbit (1,950)" | SUPPORTED | 2,059 − 109 SAME-R. All 2,059 have `gravity = micro`. | - |
| N12 | en:536 `map.lead` | "Each ball is something NASA set on fire in space, or tried to" | SUPPORTED | Nomex and Ultem never lit, and silicone did not spread (PSI-99), so "tried to" fits. | - |
| N13 | en:585-589, 613 | "Not in NASA's public records"; "NASA's public experiment archive has no solid material burned in the air planned for a Moon base" | SUPPORTED ONLY IN A NARROWER SCOPE | True for PSI (coverage: 0) and for Saffire-V (26% O2). "Public records" also covers Saffire-VI, which we have not read. | medium |
| N14 | en:66 lede | "NASA burned thousands of fires in orbit" | SUPPORTED ONLY IN A NARROWER SCOPE | 1,950 fire tests, 62 of them never lit. "Nearly two thousand" is accurate. The wording predates 34d41b3, but the sentence was rewritten. | low |
| N15 | en:525-531 `exp.err` stamps (Dashboard) | "NASA data errors ... fixed values keep the original next to them, doubts are left as NASA wrote them" | SUPPORTED | `discrepancies()`: `values_changed` carry `table_value` and `value_now`; doubts count `raw_data_conflicts` with action `flag` or `note`. The counts are live and will change as our patches change. | - |
| N16 | en:522 Scoreboard `moon` | "solids burned at Moon-base oxygen (30 % or more) in NASA's PSI records" | SUPPORTED | The value is the moon-habitat cell count (0). That cell is narrower than "30% or more", but no PSI solid exceeds 22.7%, so the 0 holds either way. | - |
| N17 | `PixelScene.jsx` `MATERIAL_SHAPE` (drawing) | PMMA is drawn as a rod | as row 10 | Most of the app's PMMA group are films. It is a drawing, not a claim in words. | low |

Not re-reviewed: the assistant chat; `PixelScene.jsx` code comments; `sim.ui` labels, `map.view` and `map.intro`
(UI words, no claims).
