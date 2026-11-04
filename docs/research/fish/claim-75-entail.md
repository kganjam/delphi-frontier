# Claim 75: what it requires at the organism and ecology scales

**Source claim (behaviour scale, evidence: measured):**
> S21-D VERDICT STRENGTHENS: directly measured adult zebrafish fast-start maxima span
> 0.45–1.38 m/s (Miln et al. 2021, n=50, 120 fps, full text, values digitised from Fig 1a),
> BRACKETING the Reynolds-derived 0.842 m/s. The fastest individual is still ~4.2x below the
> 5.84 m/s threshold.

**Adjacent scales checked:** organism, ecology.
**Date:** 2026-11-04.

## Context gaps, stated first

- **What the 5.84 m/s threshold is:** `unknown`. I searched this repository (`grep` for `5.84`,
  `0.842`, `S21`, `Miln`, `fast-start`, `zebrafish`, `Reynolds`) and found no record of
  claim 75, the S21-D verdict, or where the threshold comes from. The constraints below treat
  5.84 m/s only as a number that the claim says is not reached. I do not know what physical
  process it stands for.
- **Re-reading Miln et al. 2021 (read-level: full-text; I read it through an automated
  text extraction and did not view Fig 1).** *Social rank and not physiological capacity
  determines competitive success in zebrafish (Danio rerio).* R Soc Open Sci 8:210146,
  doi:10.1098/rsos.210146, PMC8025299. The extraction confirms these details:
  - n = 50 adult short-fin zebrafish of mixed sex.
  - Water temperature 23 ± 0.5 °C.
  - Escapes were triggered by a mechanical stimulus to the tail, in a 405 × 600 mm tank with
    30 mm of water.
  - Filmed with a GoPro Hero 6 at 120 frames s⁻¹. Each fish was filmed four times and its
    fastest response was used.
  - Speed is the "maximum speed calculated across two video frames", tracked at a point
    0.35 BL from the snout.
  - The text gives no fast-start speeds; the values are only in Fig 1.

  So I have **not** independently checked the 0.45–1.38 m/s digitisation. Two of these
  method details matter below: the 23 °C temperature and the two-frame (≈16.7 ms) speed
  window.

---

## Constraints

### C1 · organism · `timescale`: the speed window must be short compared with the escape it measures

**Requirement.** The claim calls the 120 fps values "maxima" and uses them to bracket 0.842 m/s.
That only works if the speed-averaging window is short compared with the propulsive phase
of the escape (stage 1 + stage 2). Otherwise the true peak is smoothed away.
- Bound: window / (stage 1 + stage 2 duration) ≤ 0.5. This 0.5 is my own choice of cutoff,
  not a value from the literature.
- Miln's window is 2 frames at 120 fps, which is about 16.7 ms.

**Check.**
- **Fish in general (review; read-level: search-summary).** Stage 1 lasts about 10–20 ms and
  stage 2 about 20–30 ms. Source: Domenici & Hale 2019, *Escape responses of fish: a review
  of the diversity in motor control, kinematics and behaviour*, J Exp Biol 222:jeb166009.
  - With these durations, my calculated ratio (derived, not observed) is 16.7/50 to 16.7/30,
    which is **0.33–0.56**. That straddles the 0.5 bound.
- **Larval zebrafish at 5 dpf (read-level: full-text, partial: first 100k characters).**
  Measured at 10,000 fps and 28 °C: C-bend 0–11 ms, counterbend 11–21 ms. Source: Ravel
  et al. 2025, iScience 28:112056, PMC11930232.
  - These are larvae, so they do not test the adult requirement.
- **Adult zebrafish (read-level: full-text minus tables).** Danos & Lauder 2012, J Exp Biol
  215:1854, doi:10.1242/jeb.068957.
  - Filmed adults (mean total length 33.0 ± 1.3 mm) at 1000 fps.
  - Reports a mean escape latency of 8.9 ms.
  - Puts stage 1 and stage 2 durations in Table 1. I could not read Table 1 through the
    publisher page.

**Status: `open`.** The adult zebrafish number exists in the literature but I could not read
it. This is "not accessed", not "nobody has looked".

**Implication (my inference, not the authors').** If the window is not short enough, the
bias runs one way: the 120 fps values *understate* true peaks. That would push the measured
range up, towards the threshold, not away from it. So the "~4.2x below" margin is a lower
bound on how far below the threshold the fish are, only if the 120 fps values are unbiased;
any bias makes the true margin smaller. Even a 2x underestimate would leave the fastest fish
at about 2.8 m/s, which is still below 5.84 m/s (simple arithmetic, not a measurement).

### C2 · organism · `range`: burst speed must be at least the sustained-swimming ceiling

**Requirement.** A fast-start peak is a burst. It must be at least the speed the same kind of
fish can hold in a prolonged swim test (Ucrit).
- Bound: fast-start maximum ≥ about 0.55 m/s, i.e. lo = 0.55 m/s.

**Check (measured; read-level: search-summary).** Both values below come from Palstra et al.
2010 (PLoS ONE); I read only the search summary.
- Palstra et al.: Ucrit = 0.549 ± 0.007 m/s (18.0 SL s⁻¹), n = 10 individual zebrafish.
- Plaut, as cited by Palstra: Ucrit = 0.560 ± 0.048 m/s (15.5 SL s⁻¹).
- A protocol source (bio-protocol e3712; search-summary) notes that absolute adult zebrafish
  Ucrit varies between swim-tunnel setups.

**Status: `satisfied` for what the claim relies on (the 0.842 m/s Reynolds value and the
1.38 m/s maximum, both above ~0.55 m/s). There is a disagreement I am not averaging away:**
- Miln's reported *lower* end, 0.45 m/s, is *below* the Ucrit that other labs measured.
- I see three possible causes. I have not tested which is right:
  1. Population or temperature differences: Miln measured at 23 °C, and the Ucrit studies'
     temperatures were not checked.
  2. The 120 fps under-sampling described in C1.
  3. Weak responders in a 30 mm-deep tank.
- Miln also measured a flume sprint speed (U10), but the text gives no values for it, so I
  cannot compare it within the same fish.

### C3 · organism · `energetic`: the muscle must deliver enough power

**Requirement.** Fast-twitch muscle must deliver enough power to bring the body plus its
added mass to the measured peak speed within the propulsive phase.

**My calculation (derived, not measured; every input is an assumption or a value from
another source):**
- Assumed inputs:
  - added-mass factor 1.2;
  - propulsive duration 30–50 ms (the general-fish range from C1);
  - fast muscle 50% of body mass (assumed: I did not find an adult zebrafish value);
  - no wake losses, which makes this a lower bound.
- To reach 1.38 m/s: kinetic energy ≈ 1.14 J per kg of body, so required power ≈ 23–38 W
  per kg of body, or **≈ 46–76 W per kg of muscle**.
- To reach the 5.84 m/s threshold with the same assumptions: ≈ 820–1360 W per kg of muscle.

**Available power (measured in vitro, other species; read-level: search-summary).**
- Wakeling & Johnston 1998, *Muscle power output limits fast-start performance in fish*,
  J Exp Biol 201:1505.
- Reports a mean muscle-mass-specific power of 142.7 W kg⁻¹ at 20 °C from fast myotomal
  fibres, measured by work loop under in-vivo-like strain.
- The species is abbreviated "Sc. notata" in the summary; I did not verify the full name.
- I could not open the full text: the publisher URL returned a different article, and
  st-andrews.ac.uk and sciencegate.app are blocked by the session's network policy.
- No zebrafish adult fast-muscle power value was found. I ran one targeted search on
  adult *Danio* escape, muscle and acclimation; it was not exhaustive.

**Status: `open`.** The derived requirement for 1.38 m/s (≥ 46 W/kg muscle, a lower bound)
is below the one measured value I found (142.7 W/kg), but that value is from another species.
I am not calling it satisfied on cross-species plausibility.

**A second, derived observation (not a measurement).** The threshold would need roughly
6–10x the one muscle power value I found. That is consistent with the claim that the
threshold is not reached. It is an argument about energy, not a check of the claim.

### C4 · ecology · `range`: the measurement temperature must lie inside the wild temperature range

**Requirement.** The 23 °C measurement must lie inside the temperatures wild zebrafish
actually experience. Otherwise the speed range does not describe the animal in its habitat.

**Check.**
- Engeszer et al. 2007, *Zebrafish in the wild*, Zebrafish 4:21. Abstract read
  (read-level: abstract): wild zebrafish are abundant in silt-bottomed, vegetated pools and
  rice paddies beside slow-moving streams.
- A secondary source attributes to Engeszer et al. a temperature range from about 18 °C
  (cold, fast rivers) to 36 °C (warm, stagnant paddy pools). I read only a search summary of
  that secondary source and not the original table (read-level: search-summary).

**Status: `satisfied`, on a secondary source.** 23 °C lies inside roughly 18–36 °C.

### C5 · ecology · `range`: speed must not rise too steeply with temperature

**Requirement.** The claim says even the fastest fish stays below the threshold. For that to
hold across the habitat, and not just at 23 °C, fast-start peak speed must not rise too
steeply between 23 °C and the top of the habitat range (~36 °C).
- My calculation (derived, not measured): to go from 1.38 to 5.84 m/s over 13 °C needs
  Q10 ≈ 4.23^(10/13) ≈ **3.0**.
- So the constraint is: Q10 of fast-start peak velocity over 23–36 °C must be < 3.0.

**Check.**
- I searched for a measured Q10 or thermal-acclimation curve of *adult* zebrafish fast-start
  speed, in two web searches covering adult *Danio rerio* escape speed with temperature and
  acclimation. Found:
  - one larval muscle-mechanics preprint (bioRxiv 2026, larvae only);
  - an adult study of Ucrit and cost of transport at 24 and 30 °C (J Exp Biol 229:jeb252605),
    which does not measure escape speed;
  - a sculpin burst-speed acclimation study.
- None gives an adult zebrafish fast-start Q10. Danos & Lauder 2012 cite a 23% change for a
  10 °C shift, but I could not tell what quantity that refers to, so I do not use it.

**Status: `unsatisfied`, with a narrow scope:** two web searches, not a database review.
This is the most directly falsifying open measurement. An adult escape-speed series at
28–36 °C would settle it.

### C6 · ecology · `existence`: predators that trigger fast starts must exist in the wild habitat

**Requirement.** Fast-start maxima are only ecologically meaningful if predators that elicit
fast starts exist in the natural habitat.

**Check (read-level: search-summary).**
- An antipredator review of zebrafish (YouScribe listing, title *Antipredatory behavior of
  zebrafish: adaptive function and a tool for…*) states that predatory fish such as *Channa*
  (snakeheads) share zebrafish waters. It also says few studies have examined zebrafish
  natural ecology.
- A general species page lists *Channa striata*, *Fowlea piscator*, *Alcedo atthis* and
  *Egretta garzetta*. That page is low reliability.

**Status: `satisfied`, weakly.** Predators are named, but only through secondary or
summary sources.

**Not checked: predator strike speeds.** Whether the 0.45–1.38 m/s escape speeds are matched
to predator approach speeds is a separate ecology `range` constraint. I found no strike-speed
data for zebrafish predators in one search, so I have not listed it as a scored constraint.

---

## Summary

| # | Scale | Kind | Status |
|---|---|---|---|
| C1 | organism | timescale | open (adult stage durations exist but could not be accessed) |
| C2 | organism | range | satisfied for the claim's headline numbers; Miln's low end (0.45 m/s) sits below Ucrit measured elsewhere (unresolved) |
| C3 | organism | energetic | open (only cross-species muscle power found) |
| C4 | ecology | range | satisfied (via a secondary source) |
| C5 | ecology | range | unsatisfied (no adult zebrafish fast-start Q10 found, in a narrow search) |
| C6 | ecology | existence | satisfied (weak sources) |

**No constraint is `unsatisfiable`.** No measured number I found contradicts claim 75.
The strongest caveat is C1: the 120 fps / two-frame method can only *understate* peaks, which
narrows the true margin below the threshold rather than widening it. Even a 2x
underestimate keeps the fastest fish below 5.84 m/s.

## Sources and read-levels

- Miln C, Ward AJW, Seebacher F (2021). R Soc Open Sci 8:210146. Read through automated
  text extraction; Fig 1 not viewed. **full-text**
- Danos N, Lauder GV (2012). J Exp Biol 215:1854. Text read; tables not accessible.
  **full-text (tables could-not-access)**
- Ravel G et al. (2025). iScience 28:112056 (larvae). **full-text (partial)**
- Domenici P, Hale ME (2019). J Exp Biol 222:jeb166009. **search-summary**
- Palstra AP et al. (2010) PLoS ONE, with the Plaut Ucrit value cited inside it.
  **search-summary**
- Wakeling JM, Johnston IA (1998). J Exp Biol 201:1505. **search-summary** (full text
  could-not-access: the network policy blocks st-andrews.ac.uk and sciencegate.app)
- Engeszer RE et al. (2007). Zebrafish 4:21. **abstract**; the temperature range comes from
  a secondary source, read at **search-summary**
- Zebrafish antipredator review (YouScribe listing). **listing**

```swarm-entail
{"source_claim": 75, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "timescale",
      "statement": "The velocity-sampling window used to report fast-start maxima must be short relative to the propulsive phase (stage 1 + stage 2) of the adult escape, or reported maxima underestimate true peaks",
      "quantity": "ratio of speed-averaging window (2 frames at 120 fps = 16.7 ms) to stage 1+2 duration", "lo": null, "hi": 0.5, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "General-fish stage 1 ~10-20 ms and stage 2 ~20-30 ms (Domenici & Hale 2019) give a derived ratio 0.33-0.56, straddling the bound; adult zebrafish stage durations are in Danos & Lauder 2012 Table 1, which could not be accessed",
      "satisfied_evidence": "unknown",
      "note": "Domenici & Hale 2019 JEB 222:jeb166009 (search-summary); Danos & Lauder 2012 JEB 215:1854 (full text, tables not accessible; 1000 fps, TL 33.0 mm, latency 8.9 ms); larval 5 dpf durations 0-11 / 11-21 ms at 10,000 fps (Ravel et al. 2025 iScience, full-text partial), larvae only. Any bias makes 120 fps values UNDERSTATE peaks."},
    {"target_scale": "organism", "kind": "range",
      "statement": "Fast-start maximum speed must be at or above the population's sustained-swimming ceiling (Ucrit)",
      "quantity": "fast-start maximum speed", "lo": 0.55, "hi": null, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Measured adult zebrafish Ucrit 0.549 +/- 0.007 m/s (Palstra et al. 2010) and 0.560 +/- 0.048 m/s (Plaut, cited by Palstra) are below the claim's 0.842 m/s and 1.38 m/s",
      "satisfied_evidence": "measured",
      "note": "Palstra et al. 2010 PLoS ONE (search-summary). DISAGREEMENT preserved: Miln's lower end 0.45 m/s is below Ucrit measured in other labs; possible causes (temperature 23 C, 120 fps under-sampling, weak responders in 30 mm water) not tested. Miln's own flume U10 has no values in the text."},
    {"target_scale": "organism", "kind": "energetic",
      "statement": "Fast-twitch myotomal muscle must deliver enough mass-specific power to bring body plus added mass to the peak speed within the propulsive phase",
      "quantity": "required fast-muscle mass-specific power to reach 1.38 m/s (derived lower bound: added mass 1.2, 30-50 ms, muscle 50% of body mass assumed, no wake losses)", "lo": 46, "hi": null, "units": "W/kg muscle",
      "status": "open",
      "satisfied_by": "Only cross-species value found: 142.7 W/kg fast myotomal muscle at 20 C, work loop (Wakeling & Johnston 1998, 'Sc. notata'). No adult zebrafish fast-muscle power found.",
      "satisfied_evidence": "derived",
      "note": "Wakeling & Johnston 1998 JEB 201:1505 (search-summary; full text could-not-access, network policy). Derived (not measured): the 5.84 m/s threshold would need ~820-1360 W/kg muscle under the same assumptions. Scope of the negative: one targeted web search for adult Danio escape/muscle/acclimation."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "The temperature at which the fast-start maxima were measured must lie within the thermal range wild zebrafish occupy",
      "quantity": "measurement temperature (Miln 2021: 23 C) vs field temperature range", "lo": 18, "hi": 36, "units": "degC",
      "status": "satisfied",
      "satisfied_by": "23 C lies within the ~18-36 C field range attributed to Engeszer et al. 2007",
      "satisfied_evidence": "literature",
      "note": "Engeszer et al. 2007 Zebrafish 4:21 (abstract read: slow streams, pools, rice paddies); the 18-36 C range is from a secondary chapter citing Engeszer (search-summary), not checked against the original."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Thermal sensitivity of adult fast-start peak speed between 23 C and the top of the field range (~36 C) must be low enough that the peak stays below the threshold across the habitat",
      "quantity": "Q10 of adult fast-start peak velocity over 23-36 C (derived bound: (5.84/1.38)^(10/13))", "lo": null, "hi": 3.0, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No measured adult zebrafish fast-start Q10 or thermal acclimation curve found",
      "satisfied_evidence": "unknown",
      "note": "Scope of the negative: two web searches (adult Danio rerio escape speed x temperature/acclimation). Found only a larval muscle-mechanics preprint (bioRxiv 2026), an adult Ucrit/COT study at 24/30 C (JEB 229:jeb252605) with no escape speed, and a sculpin acclimation study. This is 'not found in a narrow search', not 'shown absent'."},
    {"target_scale": "ecology", "kind": "existence",
      "statement": "Predators that elicit fast-start escapes must exist in the natural habitat",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Piscivorous snakeheads (Channa spp.) reported to share zebrafish waters; general sources also list kingfisher, egret and keelback snake",
      "satisfied_evidence": "literature",
      "note": "Zebrafish antipredator review (listing / search-summary); species page (low reliability). Predator strike speeds, needed to test whether escape speeds are matched to predators, were not found in one search and are not scored here."}
  ]}
```
