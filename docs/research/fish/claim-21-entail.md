# Claim 21: entailments at the organism and ecology scales

**Source claim (behaviour scale, evidence: derived).** "Adult *Danio* peak fast-start speed is 0.84 m/s (25.5 TL/s,
0.78–0.91 at ±1 s.e.m.), DERIVED from a measured maximum Reynolds number of 27,800 ± 2,140 for 33 mm adults at
1000 fps."

**Where it comes from.** `docs/research/fish/S21-behaviour.md` on branch
`origin/claude/zebrafish-fast-start-velocity-pxsv7e` (read-level: **full-text**, read this session).
- **Measured by Danos & Lauder 2012** (*J Exp Biol* 215:1854, doi 10.1242/jeb.068957): a mean maximum Re of
  27,800 ± 2,140 s.e.m. in 1 mPa·s water, n = 5 adults, TL 33.0 mm, 1000 fps. S21 read this at full text. I did not
  re-read it, so for me the read-level is **listing**, relayed via S21.
- **Calculated by S21:** U = Re·ν/L, with ν = 1.0×10⁻⁶ m²/s and L = 0.033 m.

**Subject of every number below.** The claim is about **adult zebrafish, *Danio rerio***. Every number I set against it
is labelled with its species and life stage. **No flying-fish (exocoetid) number is used anywhere in this note.**

**What is calculated.** Every number not quoted from a source is a calculation, from
`docs/research/fish/claim-21-entail_calc.py` (run with `python3 -I`). Nothing here is a new measurement.

## Verdict in one paragraph

None of the four requirements is `unsatisfiable`: no measured adult-zebrafish number contradicts any of them. None is
`satisfied` either, because none of the required quantities has been measured in **adult** zebrafish, as far as my
searches reached.

- **O1 (muscle power) and O2 (muscle twitch speed) look closest to being met, but only by proxy.** The only
  zebrafish muscle-mechanics measurement I found is from **5-day-old larvae** (Mead et al. 2020):
  - net work-loop power 134 ± 20 W/kg at 28 °C;
  - twitch full width at half-maximum 11 ± 1 ms.

  Both values are compatible with the requirements calculated from the claim. But a larval tail is not an adult
  myotome, so both stay `open`.
- **O3 (wake momentum) and E1 (wild-adult speed) are unsatisfied: nobody has looked.** I found no measurement of
  either quantity for zebrafish.
- **A disagreement inside the project, preserved.** The other adult measurement, Demesmay et al. 2025 (1.57 ± 0.27
  m/s, 240 fps), is ≈1.9× the claim. It does not refute the claim: it is the same species, but a different
  statistic, frame rate and arena (see §3). It does matter for O1: the power requirement at 1.57 m/s is about 3.5×
  higher.

## 1. Entailments

If adult zebrafish really reach a mean peak centre-of-mass speed of 0.78–0.91 m/s within one fast-start, then:

| # | Scale | Kind | Requirement (generic) | Bound (calculated) |
|---|---|---|---|---|
| O1 | organism | energetic | The axial fast muscle must deliver, over the time from movement onset to peak speed, at least the body's kinetic energy at the peak speed | mean muscle-mass-specific power ≥ 24–129 W/kg (KE-only floor; real requirement higher by 1/efficiency) |
| O2 | organism | timescale | Axial fast-muscle force must rise to its peak within stage 1 of the C-start, so that one muscle activation drives one bend | twitch time-to-peak ≤ ~13 ms (≤ 18 ms at +1 SD of stage-1 duration) |
| O3 | organism | conservation | Momentum must balance: the body and fins must shed into the wake an impulse at least equal to the body's momentum at the peak | impulse per kg body ≥ 0.78–0.91 N·s/kg (0.93–1.09 with added-mass coefficient 0.2) |
| E1 | ecology | range | The claim names the species, not a lab strain, so adults from wild populations must reach a peak fast-start speed of the same order at the same temperature | mean peak speed of wild-origin adults ∈ [0.42, 1.68] m/s (factor-2 band; the tolerance is my choice) |

**How the bounds were derived (calculation):**

- **O1.** P ≥ ½U²/(f·t).
  - U = 0.778–0.907 m/s, from the claim.
  - t = 8–21 ms is the onset-to-peak time. It is bracketed from Demesmay et al. 2025 (adult zebrafish, author values):
    first movement to maximal head turn, 13 ± 5 ms; "latency to attain maximal speed", 8 ± 4 ms. The text I read does
    not make clear what reference point the 8 ms is measured from. So the bracket runs from 8 ms (if it is measured from
    response onset) to 13 + 8 = 21 ms (if it is measured from the maximal head turn).
  - f = 0.4–0.6 is the fast-muscle mass fraction. This is **assumed**; I found no zebrafish value (see O1 check).
  - The kinetic energy is 0.355 J/kg body at 0.84 m/s.
  - Added mass and wake energy are omitted, so the bound is a **floor**. At 50 % and 30 % conversion efficiency, the
    band becomes 48–257 and 80–429 W/kg.
- **O2.** Stage-1 duration of 13 ± 5 ms (Demesmay 2025). The C-bend is produced by one contralateral muscle
  activation, so muscle force must reach its peak inside that window. That last point is my inference from standard
  fast-start mechanics; the authors do not state it.
- **O3.** J/m = (1 + k)U. The added-mass coefficient k = 0.2 is an assumed illustrative value.
- **E1.** The band is 0.84/2 to 0.84×2.

**Considered and dropped.**
- **Viscosity–temperature.** If the fish were tested at 28 °C (ν ≈ 0.84×10⁻⁶ m²/s), would inverting Re with ν = 1.0×10⁻⁶
  give the wrong speed? It would not. Danos & Lauder state their Re is for "1 mPa s" water. Inverting with the same
  nominal viscosity returns their speed whatever the true temperature was. Temperature still matters for performance,
  but that is a behaviour-scale caveat (S21 §5), not an entailment at these scales.
- **Predators.** "Predators that elicit fast-starts must exist in the habitat" is **not** entailed. A reflex capability
  can exist without current selection for it. I record the predator inventory in §2 only as context.

## 2. Checks

### O1 — energetic: muscle power ≥ 24–129 W/kg (KE floor). **Status: open**

- **Nearest measurement, same species, wrong life stage.** Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM (2020),
  "Mechanical characteristics of ultrafast zebrafish larval swimming muscles", *Biophys J*, doi
  10.1016/j.bpj.2020.06.036, PMC7451861.
  - Read-level: **abstract** (Europe PMC REST), plus the full-text HTML via an automated summarizer for the temperature
    and how mass was estimated.
  - Author's claim: "myotomal muscles develop high net power (134 ± 20 W/kg at 80 Hz) in cyclical work loop
    experiments". The summarizer relayed 122.9 ± 11.1 W/kg at 100 Hz.
  - Conditions: 28 °C, **5-dpf larvae**, intact tail. Muscle mass was estimated from the cross-sectional area times
    myotome length times 1.06 g/cm³; the tissue was not weighed.
- **Comparison (my inference).**
  - 134 W/kg exceeds the KE-only floor across most of the bracket. The exception is the worst corner (129 W/kg,
    U = 0.91 m/s, t = 8 ms, f = 0.4), where the two are equal.
  - Once any realistic conversion efficiency is allowed, it no longer clears the upper end. At 50 % efficiency the
    requirement is 48–257 W/kg.
  - So a larval-grade muscle would satisfy the claim only if acceleration takes the slower half of the timing bracket
    or uses a large fast-muscle fraction.
- **Why this is `open`, not `satisfied`.**
  1. The measurement is larval, and adult axial muscle has not been measured in this way.
  2. Work-loop power at 80–100 Hz cyclic strain is not the single-shot power of a C-start.
  3. f is assumed.
- **Relayed context, not re-checked.** Challenge-132 cites a "461 W/kg traced ceiling" from the S21 lineage, which I
  have not read, and Wakeling & Johnston 1998 (~143 W/kg fast muscle at 20 °C, species not identified there). Neither is
  a zebrafish measurement that I can confirm, and I use neither as evidence.
- **Search scope.**
  - Europe PMC: `(zebrafish OR "Danio rerio") AND ("work loop" OR "work-loop") AND adult`, 11 hits, none an adult
    zebrafish work loop.
  - Two web searches (zebrafish fast-muscle work-loop power; adult zebrafish muscle mass fraction). The second found
    microCT muscle-volume studies (García-Poyatos 2024; a 2025 bioRxiv microCT morphometry paper; Hasumura & Meguro
    2016), but no mass fraction in the snippets (read-level: search-summary).
  - The adult zebrafish fast-muscle fraction and adult work-loop power are both **unknown**. This is "nobody has looked",
    within this scope.

### O2 — timescale: twitch time-to-peak ≤ ~13 ms. **Status: open**

- **Requirement source.** Demesmay et al. 2025, *PLoS Biol* 23:e3003484, PMC12604801, **adult zebrafish** (4–12
  months, body length 2.6–3.6 cm), 240 fps (frames are 4.2 ms apart), reared at 28 °C. Read-level: **full-text**
  (Europe PMC XML, searched by keyword this session).
  - Quote: "Latency between first escape response movement and maximal head turn was also similar between the two groups
    (13 ± 5 for controls and 11 ± 5 ms for mutants)".
  - At 240 fps, the 13 ms is resolved only to about ±1 frame (my note).
- **Nearest measurement, same species, wrong life stage.** Mead et al. 2020 (above, abstract): larval myotomes "have
  rapid twitch kinetics (full width at half-maximal stress: 11 ± 1 ms)", at 28 °C.
  - Inference (mine): for a twitch with FWHM 11 ms, time-to-peak is at most about the FWHM, so it falls within ≤ 13 ms.
  - Larger fish usually have slower fast muscle, so the adult value could be longer. This is the general scaling
    expectation, not a zebrafish measurement.
- **Adult data found, but not comparable.** Search summaries describe a *J Gen Physiol* study of **skinned adult
  myofibrils at 10 °C**, with relaxation times of about 14 ms. Read-level: search-summary.
  - This is myofibrillar activation/relaxation kinetics, not an intact-muscle twitch.
  - It was measured 18 °C colder than husbandry temperature.
  - I do not use it as evidence.
- **Search scope.** One web search for adult zebrafish twitch time-to-peak and half-relaxation. It found no adult
  intact-muscle twitch. This is "nobody has looked", in this scope.

### O3 — conservation: wake impulse ≥ 0.78–0.91 N·s/kg. **Status: unsatisfied (nobody has looked)**

- **No wake measurement (PIV or similar) of an adult zebrafish fast-start was found.**
  - Scope: Europe PMC,
    `(zebrafish OR "Danio rerio") AND ("particle image velocimetry" OR PIV) AND ("C-start" OR "fast-start" OR "escape")`,
    87 hits. I scanned the top 10. They were carangid simulations, larval CFD (Ravel et al. 2025, 5-dpf, simulated), and
    unrelated work.
  - Larval CFD is a simulation of a different life stage, so it is not evidence here.
- Momentum balance itself is not in doubt. What is missing is a measured wake impulse that can be compared with the
  body momentum, which would test the claimed speed independently of tracking.
- Wake studies of fast-starts in other species (e.g. bluegill) exist in the literature, but I did not attempt to read
  them. A cross-species wake would not test this zebrafish claim anyway.

### E1 — range: wild-origin adult peak fast-start speed ∈ [0.42, 1.68] m/s. **Status: unsatisfied (nobody has looked)**

- **Nearest measurement: different life stage and different quantity.** Morgan R et al. 2022, "Reduced physiological
  plasticity in a fish adapted to stable temperatures", *PNAS* 119:e2201919119, PMC9295802. Read-level: **full-text**
  (Europe PMC XML, keyword search).
  - Fish: **juvenile** lab vs wild-caught F1 zebrafish, tested at 10–38 °C acclimation temperatures.
  - "Maximum swim speed" was a group swimming test in a stirred chamber. The final sustained speed was held for 30 s, so
    it is a prolonged-swimming quantity, not a fast-start peak.
  - Author's claim: "the thermal performance breadth of laboratory fish was within 1 °C of the wild fish, but the peak
    performance was lower".
  - The same paper filmed startles at 1000 fps, but it reports only the response **latency**, not speed.
  - I did not read figure values.
- **Older lead.** Robison & Rowland 2005 report a "reduced startle response" in domesticated vs wild-derived zebra
  danio. Read-level: **search-summary**. The quantity measured is not clear from the summary.
- **Inference (mine).** Both leads point the same way: wild-origin fish perform at least as well as lab fish. So if
  anything, the claim's lab-derived value would be a lower bound for wild adults. That direction cannot push E1 below
  0.42 m/s, but nothing measures E1 itself.
- **Danos & Lauder strain.** The strain used by Danos & Lauder 2012 is **unknown** to me (not in S21's notes).
- **Search scope.**
  - One web search on wild vs domesticated zebrafish escape speed.
  - Europe PMC: `(zebrafish OR "Danio rerio") AND (wild OR "wild-caught" OR "wild-type strain") AND ("thermal
    performance" OR "maximum swim speed" OR "sprint")`, 182 hits, top 10 scanned. This found Morgan 2022 and Miller,
    Dugand & McGuigan 2025 (*Curr Zool*, PMC12011485). The latter covers lab strains AB/WIK/Tu and prolonged swimming
    speed only; read-level full-text, keyword search.
  - Unreachable: ecoevorxiv.org and par.nsf.gov, which host possibly relevant preprints. Both are outside this session's
    network policy.
- **Context only, not a check.** The predator inventory for wild zebrafish lists snakeheads, freshwater garfish,
  catfish, spiny eels, kingfishers, pond herons and dragonfly larvae (Animal Diversity Web and the eLife
  natural-history feature, read-level: search-summary). The Spence et al. 2008 review was not read. No measured strike
  kinematics against adult zebrafish were found.

## 3. The disagreement this note does not resolve

There are two adult zebrafish speed sources, and they disagree by ≈1.9×:

| Source | Subject | Value | Statistic | Instrument | Read-level (mine) |
|---|---|---|---|---|---|
| Danos & Lauder 2012, inverted by S21 (the claim) | adult *D. rerio*, TL 33 mm, n = 5 | 0.84 m/s (calculated) | mean of per-sequence peaks | 1000 fps, 12 cm dish | listing (via S21 full-text) |
| Demesmay et al. 2025, controls | adult *D. rerio*, 2.6–3.6 cm | 1.57 ± 0.27 m/s (author value, "calculated maximal speed") | per-response maximum | 240 fps, 1.6 L tank, 3–4 fish per tank | full-text |

- **This is not a refutation of claim 21.** The species is the same. But the two sources differ in:
  - the statistic;
  - frame rate and tracking point (Demesmay tracked manually in Fiji);
  - the arena;
  - possibly the length basis.
- **What it does to O1.** It makes O1 harder. At 1.57 m/s the KE-only floor is 98–385 W/kg (calculated), which is
  above the larval 134 W/kg over most of the bracket.
- **What would settle it.** If Danos & Lauder Table 1 (direct COM velocity) were read, it would settle which statistic
  the 0.84 m/s represents.

## 4. What would move these statuses

1. **Adult work-loop and twitch measurements at 28 °C** (O1, O2). Use the Mead et al. intact-preparation protocol on
   adult myotome strips, and report the fast-muscle mass fraction from dissection or microCT. This is the only route by
   which O1 could become `unsatisfiable`. That would happen if adult power were measured well below the floor, which at
   present it is not.
2. **PIV of adult zebrafish C-starts** (O3). This gives the wake impulse, and with it a tracking-independent speed.
3. **Wild-caught F1 adults filmed at ≥ 1000 fps** with the Danos & Lauder stimulus (E1).

```swarm-entail
{"source_claim": 21, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "energetic",
      "statement": "Axial fast muscle must deliver, over the onset-to-peak interval of the fast-start, at least the body's kinetic energy at peak speed",
      "quantity": "mean muscle-mass-specific power during acceleration (kinetic-energy-only floor)", "lo": 24, "hi": 129, "units": "W/kg muscle",
      "status": "open",
      "satisfied_by": "Nearest value is LARVAL zebrafish (5 dpf) net work-loop power 134 +/- 20 W/kg at 80 Hz, 28 C (Mead et al. 2020), which meets the KE-only floor across the bracket but not the upper end once any conversion efficiency <1 is allowed; no adult zebrafish muscle power or fast-muscle mass fraction found",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated (claim-21-entail_calc.py) from U 0.78-0.91 m/s, onset-to-peak 8-21 ms bracketed from Demesmay et al. 2025 PLoS Biol 23:e3003484 (adult D. rerio, full-text), muscle fraction 0.4-0.6 ASSUMED. Mead AF et al. 2020 Biophys J doi 10.1016/j.bpj.2020.06.036 PMC7451861 (abstract + summarizer full-text). Negative scope: Europe PMC adult zebrafish work-loop query (11 hits, none adult) + 2 web searches; adult value is 'nobody has looked' in this scope. At Demesmay's 1.57 m/s the floor is 98-385 W/kg."},
    {"target_scale": "organism", "kind": "timescale",
      "statement": "Axial fast-muscle force must rise to peak within stage 1 of the C-start (one activation drives one bend)",
      "quantity": "intact fast-muscle twitch time-to-peak at test temperature", "lo": null, "hi": 18, "units": "ms",
      "status": "open",
      "satisfied_by": "Nearest value is LARVAL zebrafish (5 dpf) twitch FWHM 11 +/- 1 ms at 28 C (Mead et al. 2020); adult intact-muscle twitch kinetics not found (only skinned adult myofibril kinetics at 10 C, search-summary, not comparable)",
      "satisfied_evidence": "unknown",
      "note": "Stage-1 duration 13 +/- 5 ms from Demesmay et al. 2025 (adult D. rerio, 240 fps, full-text); hi = mean + 1 SD. Mead 2020 read at abstract level. Negative scope: one web search for adult zebrafish twitch time-to-peak; 'nobody has looked' in this scope. Adult muscle may be slower than larval (general scaling expectation, not a zebrafish measurement)."},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "Momentum must balance: body and fins must shed into the wake an impulse at least equal to body momentum at peak speed",
      "quantity": "wake impulse per unit body mass", "lo": 0.78, "hi": null, "units": "N s/kg",
      "status": "unsatisfied",
      "satisfied_by": "No wake (PIV) measurement of an adult zebrafish fast-start found; only larval CFD (Ravel et al. 2025, simulated, 5 dpf), which is neither adult nor measured",
      "satisfied_evidence": "unknown",
      "note": "lo = (1+k)U with k = 0 at U_lo; 0.93-1.09 N s/kg with assumed added-mass coefficient 0.2 (calculated). Negative scope: Europe PMC zebrafish AND PIV AND (C-start OR fast-start OR escape), 87 hits, top 10 scanned. Nobody has looked (in this scope); not a measured shortfall. Cross-species wakes (e.g. bluegill) not read and would not test this claim."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Because the claim names the species, adults from wild populations must reach a peak fast-start speed of the same order at the same temperature",
      "quantity": "mean peak fast-start COM speed of wild-origin adult D. rerio", "lo": 0.42, "hi": 1.68, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No fast-start peak speed for wild-origin adult zebrafish found. Nearest: Morgan et al. 2022 PNAS (JUVENILE wild F1 vs lab; prolonged group 'maximum swim speed', lab peak lower; startle latency only), and Robison & Rowland 2005 (domesticated 'reduced startle', search-summary) - both suggest wild fish are not slower, neither measures the bounded quantity",
      "satisfied_evidence": "unknown",
      "note": "Factor-2 tolerance band is the author's choice (calculated). Morgan R et al. 2022 PNAS 119:e2201919119 PMC9295802 (full-text, keyword search). Miller, Dugand & McGuigan 2025 Curr Zool PMC12011485 (lab strains, Ucrit only). Negative scope: 1 web search + Europe PMC wild/sprint query (182 hits, top 10); ecoevorxiv.org and par.nsf.gov unreachable. Nobody has looked, in this scope. Danos & Lauder 2012 strain unknown."}
  ]}
```
