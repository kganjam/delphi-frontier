# Claim 190: entailments at the organ and behaviour scales

**Source claim (organism scale, evidence: derived).** "Granting an unmeasured 1-BL span and AR-5 fin (S=192 mm2), the wing
produces 10% of body weight at launch and ~5% at the apex."

**Where it comes from.** `docs/research/fish/S28-organism.md` §3.2, on branch `origin/claude/s28-organism-design-5z0vjz`
(read-level: **full-text**). The organism is the Daane et al. 2021 `lat4a^nr21/+;kcnh2a^lof/+` zebrafish. The numbers rest
on these S28 inputs:

- m = 0.25 g (assumed, back-solved);
- CL_max = 1.07 (project-derived);
- exit speed = 1.38 m/s burst (cited as measured, unverified, see C4);
- launch angle 45°.

The claim states lift fraction = (V/V_to)². At launch that gives (1.38/4.37)² ≈ 0.10. At the apex only the horizontal
speed 1.38·cos 45° = 0.98 m/s remains, giving ≈ 0.05.

**Everything numeric in this note that is not quoted from a source is a calculation.** The script is
`docs/research/fish/claim-190-entail_calc.py` (`python3 -I`). Nothing here is a new measurement.

## Verdict in one paragraph

None of the five requirements is **satisfied** by a measured value. None is **unsatisfiable** either, because no measured
number for the *pectoral* fin or for a zebrafish *leap* contradicts one.

- **Fin-length bound (C1).** Its measured value exists (Daane 2021 Fig. 4B), but I could not read it. It stays `open`.
- **Fin area (C2), exit speed (C4) and in-air fin abduction (C5).** Nobody has measured them. This is "nobody has looked",
  not "looked and found nothing".
- **Fin stiffness (C3).** This is closest to failing. The nearest measured value is the in-vivo bending stiffness of the
  adult zebrafish *caudal* fin, 1.5×10⁻⁹–4×10⁻⁹ N m² (Puri et al. 2018). That is **7–18× below** the 2.7×10⁻⁸ N m² I derive
  for the pectoral fin to hold its shape under the claimed lift.
  - The measurement is for a different fin, in a wild-type fish, in water. So it is **not** a contradiction of the pectoral
    requirement, and I do not mark C3 unsatisfiable.
  - One pectoral-fin measurement in the same rig would convert C3 to satisfied or unsatisfiable.

## 1. Entailments

If the claim describes a real animal (and not only the granted geometry), the following must hold. Bounds are
calculated from S28's own inputs unless stated. The tolerance is ±1 percentage point on the "10 %".

| # | Scale | Kind | Requirement (generic) | Bound (calculated) |
|---|---|---|---|---|
| C1 | organ | spatial | Each pectoral fin must be long enough that the spread span is ≈ 1 SL (within ×1.2) | fin length / SL ∈ [0.36, 0.55] |
| C2 | organ | range | The combined lifting planform area must be large enough to give 9–11 % W at the launch speed | S ∈ [177, 216] mm² |
| C3 | organ | range | The fin must be stiff enough to stay near-planar under the claimed lift: tip deflection ≤ 10 % of fin length | whole-fin EI ≥ 2.7×10⁻⁸ N m² |
| C4 | behaviour | range | The fish must leave the water at the speed the 10 % is computed for | water-exit speed ∈ [1.32, 1.46] m/s |
| C5 | behaviour | timescale | A behaviour must exist that abducts the pectorals to a lifting posture. It must complete within ~10 % of the airtime (≤ 20 ms of a 199 ms flight) and hold the fins spread to at least the apex (~100 ms) | abduction time ≤ 20 ms; hold ≥ 100 ms |

How the bounds were derived (calculation):

- **C1.** b = 2ℓ + 4 mm body width, SL = 30 mm. b ∈ [31/1.2, 31×1.2] mm gives ℓ/SL ∈ [0.364, 0.553].
- **C2.** S = f·W / (½ρV²CL) at V = 1.38 m/s, for f = 0.09, 0.10, 0.11 → 177, 196, 216 mm².
  - At exactly 192 mm² the fraction is **9.8 %**, not 10.0 %. This is the 4.37 vs 4.41 m/s rounding already recorded in
    challenge-195. It is immaterial.
- **C3.**
  - Load: the lift per fin at launch is 0.5 × 0.098 × 2.45 mN = 1.20×10⁻⁴ N. That is a wing loading of 1.25 Pa.
  - Model: a uniform-load cantilever of length 13.5 mm, with δ = FL³/(8EI). Requiring δ/L ≤ 0.1 gives
    EI ≥ FL²/0.8 = **2.73×10⁻⁸ N m²**.
  - The 10 % criterion is my choice. A 20 % criterion halves the bound.
- **C4.** V = √(f·W / (½ρ S CL)) at S = 192 mm² → 1.324, 1.396, 1.464 m/s.
- **C5.** Vacuum airtime at 45° is 2V sin 45°/g = 199 ms, and the apex comes at 99 ms. The 10 % lift is stated "at launch",
  so the fin must already be spread at or very near exit.

**Not written as a separate constraint, but also entailed (behaviour, range).** The "~5 % at the apex" needs a launch angle
θ ∈ [38°, 50°] (apex fraction 6 % … 4 %, from 0.098·cos²θ; calculated). I found no measured zebrafish leap angle. This is
`open`, and I did not search for it beyond the leap searches listed under C5.

**An organism-scale caveat, outside the adjacent scales.** The fractions scale as 1/m. Challenge-189 cites "adult zebrafish
rarely exceed 0.5 g" (read-level there: search-summary). At 0.40 g the launch fraction is **6.1 %**, and at 0.50 g it is
**4.9 %** (calculated). So the claim's "10 %" is a statement about a 0.25 g fish.

## 2. Checks

### C1 — spatial: pectoral length ≈ 0.45 SL per fin. **Status: open**

- **What exists.** Daane et al. 2021 (*Curr. Biol.* 31:5052, doi 10.1016/j.cub.2021.08.054, PMC9172250) measured pectoral
  fin length normalised to SL for wild type, *lof/+*, *nr21/+* and the double heterozygote (Fig. 4B).
  - Read-level: **full-text via an automated summarizer**, characters 0–149,104 in two passes. I did not view the figure
    image.
  - The text and legends carry **no numeric values**. The authors say only that the double het's "paired fins are
    overgrown". The bioRxiv preprint (10.1101/2021.03.05.434157, Fig. 8B) is the same: legend only, no values
    (read-level: full-text via summarizer, first 100 k of 187 k characters).
- **Why I could not get the value.**
  - The figure image hosts were unreachable: `ars.els-cdn.com` returned 403 through the proxy, and bioRxiv returned a stub.
  - Europe PMC says the article is "not open access" for supplementary files.
  - Data S1 (the workbook already parsed in `data/fish-controls/`) has no zebrafish fin sheet. Its sheets are listed in
    `data/fish-controls/sources.json`.
- **Context, not a check.** The band [0.36, 0.55] is a flying-fish band. The specimen measurements in
  `data/fish-controls/daane2021_s1a_observations.csv` (Daane Data S1A, **measured**) give pectoral/SL of:
  - 0.41–0.75 for *Exocoetus volitans*, 0.54–0.82 for *Hirundichthys*, 0.60–0.75 for *Cheilopogon*;
  - 0.18–0.39 for the two flying halfbeaks;
  - 0.07–0.18 for halfbeaks and needlefish.

  S28 itself labels 0.45 SL an **extrapolation**, not a reading of Fig. 4B.
- **Inference (mine).** The longfin-type alleles are described as roughly 1.5× fin *length* in one honors thesis for anal
  and caudal fins (pdxscholar, read-level: search-summary, not pectoral). That would put a zebrafish pectoral at 0.45 SL
  only if the wild-type pectoral were ≈ 0.3 SL. I have no measured wild-type zebrafish pectoral/SL either (one web search,
  below). Neither number is used as evidence.
- **Scope of the search.** The Daane full text and its preprint; Data S1; one web search for zebrafish pectoral length/SL
  in wild-type and longfin adults, which found no pectoral ratio.

### C2 — range: S ∈ [177, 216] mm². **Status: unsatisfied (nobody has measured it)**

- **Daane et al. measured length, not area.** I confirmed this against PMC9172250: no statement about fin area in the
  text, legends or back matter (summarizer, both passes). Challenge-195 reached the same result independently at
  full-text read-level.
- **No published adult zebrafish pectoral area found, for any genotype.** Scope: one web search ("zebrafish pectoral fin
  area mm2 adult morphometrics", search-summary). It returned taxonomic tables for other species and one ZFIN record of
  embryonic (28–48 hpf) pectoral fin-bud geometry. No citation tracking was done.
- **What the absence means.** This is "nobody has looked" for this genotype. It is not a measured shortfall.
  - S28's own bracketing cases put the area anywhere from 57 mm² (length-only elongation) to 192 mm². Only the top case
    lies in the band.
  - Those cases are assumptions (S28 table §2.2). They are not evidence against C2.

### C3 — range: whole-fin EI ≥ 2.7×10⁻⁸ N m². **Status: unsatisfied. The nearest measured value points against it.**

- **Requirement (calculation).** EI ≥ 2.73×10⁻⁸ N m² for δ/L ≤ 0.1 under 1.20×10⁻⁴ N per fin, from §1.
- **The nearest measurement.** Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM. "In vivo quantification of mechanical
  properties of caudal fins in adult zebrafish." *J. Exp. Biol.* 221:jeb171777 (2018), doi 10.1242/jeb.171777,
  PMC5868929. Read-level: **full-text** (Europe PMC XML, searched by keyword; figures not viewed).
  - Author's claim: "We detected overall bending moments of 1.5×10⁻⁹–4×10⁻⁹ N m² along the proximal–distal axis".
  - Method: forces near 100 µN, deflections ≤ 2 mm, fin thickness falling from 200 to 40 µm.
  - Their cross-check from a bluegill-derived scaling gives "between 2×10⁻⁹ and 5×10⁻⁹ N m²".
- **Comparison (my inference).**
  - The measured caudal value is **7–18× below** the pectoral requirement.
  - Taken at face value, EI = 3×10⁻⁹ would give δ/L ≈ 0.9 under the claimed lift (calculated). In other words, the fin
    folds rather than lifting at CL 1.07, and the small-deflection model is no longer valid.
  - A further calculated point: the fin membrane's own weight in air, 0.54–1.08 Pa for 50–100 µm at 1100 kg m⁻³, is
    comparable to the 1.25 Pa lift loading. So the fin must carry its own weight about as much as it carries lift.
  - Equivalently, the aerodynamic loading at launch equals the dynamic pressure of water at only 0.05 m/s. That says
    nothing about the stiffness available. It only shows the loads are small in absolute terms.
- **Why this is not `unsatisfiable`.** The Puri number is for:
  1. the caudal fin, not the pectoral;
  2. wild type, not the *lof/+;nr21/+* double het, whose rays are elongated;
  3. a "lined force attack" from a pin. I did not establish whether that load spans the full fin width, so I cannot say
     whether it is a whole-fin or a part-fin EI.

  No pectoral-fin EI for zebrafish was found. So no measured value of the constrained quantity contradicts C3. The claim
  is under pressure from below, but it is not refuted.
- **A disagreement inside the project, preserved and not resolved.**
  - S28 §4 item 3 states the leap-load requirement as "about 0.1 × 6.3e-4 = **6.3e-5 N m²**". My cantilever requirement is
    **2.7×10⁻⁸ N m²**, about **2300× lower**.
  - S28 does not show its derivation. Its 6.3e-4 flight figure comes from elsewhere in the project, and I have not traced
    it.
  - On S28's number, every stiffness candidate (Puri 1.5–4×10⁻⁹; S25's 3.8×10⁻⁶ and 565×10⁻⁶, which are bluegill values)
    fails except 565×10⁻⁶. On mine, the bluegill values pass easily and only the zebrafish-measured value fails.
  - The two requirements cannot both be right. Which candidate EI counts as "sufficient" depends on which one is.
- **Scope of the search.**
  - One web search for zebrafish fin-ray bending stiffness. It found Puri 2018 and its poster; the poster host
    `ikarus.physik.uzh.ch` was unreachable.
  - Sibling reviews challenge-267 (bluegill ray EI, Alben 2007 and Flammang 2013) and challenge-175.
  - No pectoral-fin measurement in zebrafish was found. This is "nobody has looked" for the pectoral, and "looked and
    found 1.5–4×10⁻⁹" for the caudal.

### C4 — range: water-exit speed ∈ [1.32, 1.46] m/s. **Status: unsatisfied (exit speed never measured)**

- **No measured zebrafish water-exit speed found.**
  - Scope: two web searches (adult zebrafish leap kinematics; zebrafish water-exit speed with high-speed video), plus the
    sibling reviews challenge-183, -189 and -191.
  - The closest work is a SICB abstract (Hurbon & Gibb) on zebrafish jumping **on land**, read-level search-summary, with
    no speed figures.
- **The swimming-burst proxies disagree.** I keep them separate:

| Source | Speed (m/s) | Kind | Read-level (mine) |
|---|---|---|---|
| Miln et al. 2021 (S28's input) | 0.45–1.38 | cited as measured burst | **could-not-access**. Challenge-191's one search did not locate it, and I did not retry |
| Demesmay et al. 2025, *PLoS Biol.* 23:e3003484 | 1.57 ± 0.27 (SD), escape maximal speed | measured (author claim) | **listing**: relayed from challenge-183, which read it at full-text. I did not re-read it |
| Danos & Lauder 2012 | 0.84 | calculated from a reported Re | listing (relayed via challenge-183) |
| Challenge-189 | ≈ 0.64 U_max | derived from U_crit 56 cm/s (Plaut 2000) | listing (challenge-189 itself is search-summary) |

- **Inference (mine).** The band [1.32, 1.46] sits inside the spread of these burst proxies. So it is not contradicted.
  - But every one of them is a *submerged* speed.
  - Challenge-183 relays a guppy measurement (Soares & Bierman 2013: exit 1.02 m/s, airborne 1.24 m/s). I have not read
    it. If correct, it shows that exit speed and swimming speed are different quantities in a small poeciliid.
- **Conclusion.** Nobody has measured the quantity C4 bounds in this species.

### C5 — timescale: pectoral abduction ≤ 20 ms after exit, held ≥ 100 ms. **Status: unsatisfied (behaviour never observed)**

- **The behaviour.** No observation of adult zebrafish spreading their pectorals during an aerial leap was found. S28 says
  "Whether it does so has never been observed". Challenge-195 makes this the binary factor that makes area alone
  non-decisive.
  - Scope: two web searches on adult zebrafish leap/jump kinematics and pectoral fins (search-summary), described under C4.
  - A guppy study (PMC3629028, search-summary) reports pectoral use while backing up **before** a jump. It does not report
    in-air abduction.
- **The rate.**
  - No adult zebrafish pectoral fin-beat frequency or abduction duration was found. Scope: one web search. It returned the
    statement that adult zebrafish rely on body bending and use their fins for manoeuvring and stability (search-summary).
  - For **larvae**, Green et al. 2011 (*J. Exp. Biol.* 214:3111, read-level: search-summary) report about **28 Hz**. A
    half-cycle is then about 18 ms (calculated), which would just meet ≤ 20 ms.
  - **Inference only.** A 5-dpf larval fin is a different organ size and Reynolds regime from an adult, let alone an
    elongated *lof/+* fin, and fin-beat frequency normally falls with size. So the larval value is not evidence for the adult.
- **A lead I could not read.** Thorsen, Cassidy & Hale 2004 (*J. Exp. Biol.* 207:4175) on larval fin–axis coordination
  may say what the pectorals do during fast starts. The host `cob.silverchair.com` was unreachable, so its content is
  **unknown** to me. I make no claim about it.

## 3. What would move these statuses

1. **One in-vivo pectoral EI** in the Puri et al. rig, for wild-type and double-het fish (C3). This is the only check that
   could return `unsatisfiable` with a measured number, and it nearly does already by proxy.
2. **High-speed video of double-het leaps**, taken from above and from the side. It measures C4 (exit speed), C5 (whether
   and when the fins abduct) and the launch angle at once. This is the same recommendation as challenge-195.
3. **Planimetry of a spread fin** (C2), and a reading of Daane Fig. 4B (C1). Both are cheap. Neither can rescue the claim
   if (1) or (2) fails.

## Sources and read-levels

| Source | Read-level |
|---|---|
| S28-organism.md (`origin/claude/s28-organism-design-5z0vjz`) | full-text |
| Challenge-189, -191, -195, -183, -267, -38 (sibling branches) | full-text (repo files). Their own sources are relayed at **listing** level unless re-read here |
| Daane et al. 2021, PMC9172250 | full-text via summarizer (both passes); Fig. 4B image not viewed |
| Daane et al. preprint, bioRxiv 10.1101/2021.03.05.434157 | full-text via summarizer, first 100 k of 187 k characters |
| Daane Data S1A (`data/fish-controls/daane2021_s1a_observations.csv`, branch HEAD 7b5ba52) | full (repo data, measured) |
| Puri et al. 2018, PMC5868929 | full-text (XML keyword search; figures not viewed) |
| Green et al. 2011, *J. Exp. Biol.* 214:3111 | search-summary |
| Hurbon & Gibb SICB abstract; guppy jump PMC3629028 | search-summary |
| Thorsen et al. 2004; Puri poster (`ikarus.physik.uzh.ch`); Elsevier figure CDN | could-not-access |
| Miln et al. 2021 | could-not-access (not located) |

```swarm-entail
{"source_claim": 190, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Each pectoral fin must be long enough that the spread span is about one standard length (within a factor 1.2)",
      "quantity": "pectoral fin length / standard length (per fin)", "lo": 0.36, "hi": 0.55, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Measured value exists (Daane et al. 2021 Fig. 4B, preprint Fig. 8B) but is graphical only; image hosts unreachable, so the number was not read",
      "satisfied_evidence": "unknown",
      "note": "Daane et al. 2021 Curr Biol 31:5052 (PMC9172250, full-text via summarizer; no numeric pectoral/SL in text or legends). Bound calculated from b = 2l + 4 mm, SL 30 mm. For context, flying fish pectoral/SL 0.41-0.82 (Daane Data S1A, measured). S28 labels 0.45 SL an extrapolation."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The combined lifting planform area of the paired fins must be large enough to give 9-11% of body weight at the launch speed",
      "quantity": "pectoral planform area S (both fins)", "lo": 177, "hi": 216, "units": "mm2",
      "status": "unsatisfied",
      "satisfied_by": "No measurement: Daane et al. measured fin length only; no published adult zebrafish pectoral area found for any genotype",
      "satisfied_evidence": "unknown",
      "note": "Nobody has looked, not a measured shortfall. Scope: Daane 2021 full text (no area statement; matches challenge-195), one web search for zebrafish pectoral fin area (search-summary), no citation tracking. Bound calculated at V 1.38 m/s, CL 1.07, m 0.25 g; 192 mm2 gives 9.8%."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The fin must be stiff enough to stay near-planar (tip deflection <= 10% of length) under the claimed lift load",
      "quantity": "whole-fin flexural stiffness EI", "lo": 2.7e-8, "hi": null, "units": "N m2",
      "status": "unsatisfied",
      "satisfied_by": "No pectoral-fin EI measured in zebrafish. Nearest measurement: adult wild-type zebrafish CAUDAL fin in vivo EI 1.5e-9 to 4e-9 N m2, 7-18x below the requirement",
      "satisfied_evidence": "measured",
      "note": "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929 (full-text): 'overall bending moments of 1.5x10^-9-4x10^-9 N m2'. Not marked unsatisfiable because the value is for a different fin and genotype, and whether the load spans the full fin width was not established. Requirement calculated (cantilever, 1.2e-4 N per fin, L 13.5 mm). Disagrees ~2300x with S28's stated leap-load requirement of 6.3e-5 N m2 (derivation not shown); unresolved. Scope: one web search plus challenge-267/-175."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The fish must leave the water at the speed for which the launch lift fraction is computed",
      "quantity": "water-exit speed", "lo": 1.32, "hi": 1.46, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish water-exit speed has been measured; only submerged burst/escape speeds exist, and they disagree (0.64 derived, 0.84 Re-inverted, 0.45-1.38 Miln 2021 unverified, 1.57 +/- 0.27 SD Demesmay 2025)",
      "satisfied_evidence": "unknown",
      "note": "Nobody has measured exit speed in this species. Scope: two web searches on zebrafish leap/exit kinematics (search-summary; closest is a SICB abstract on jumping onto land, no speeds) plus challenges 183/189/191. Demesmay 2025 PLoS Biol relayed from challenge-183 (listing here). Bound calculated at S 192 mm2."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "A behaviour must exist that abducts the paired fins into a lifting posture within ~10% of the airtime after water exit and holds them spread at least to the apex",
      "quantity": "fin abduction time after exit (hold time >= 100 ms)", "lo": null, "hi": 0.020, "units": "s",
      "status": "unsatisfied",
      "satisfied_by": "In-air pectoral abduction during a leap has never been observed in zebrafish; no adult pectoral fin-beat or abduction duration found. Larval fin beat ~28 Hz (half-cycle ~18 ms) would meet the timing only by inference across life stages",
      "satisfied_evidence": "unknown",
      "note": "Nobody has looked. Scope: two web searches on adult zebrafish leap and pectoral kinematics, one on adult pectoral fin-beat frequency (search-summary). Green et al. 2011 J Exp Biol 214:3111 (search-summary) for larval 28 Hz. Thorsen et al. 2004 could-not-access. Airtime 199 ms at 1.38 m/s and 45 deg is calculated."}
  ]}
```
