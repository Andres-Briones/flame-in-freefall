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
| 13 | en:38-40 `home.nums[2]`; en:106 `scene.intro[2]`; en:487 | "2,177 fires NASA recorded in orbit"; "NASA lit 2,177 fires like me"; "real fires in the tables" | WRONG | 2,177 rows are 2,059 single tests, 100 day summaries, 10 condition sets and 8 planned. Of the 2,059, 116 are SAME smoke tests with no flame and 62 have `ignited = False`. The map's count note already says 2,059. | "2,059 single tests in orbit (flames, plus smoke and no-ignition tests)". |
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
