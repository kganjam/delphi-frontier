# Claim 270: what it entails at the organ and behaviour scales, and whether those requirements are met

**Source claim (organism scale, evidence: derived).** Taken from S32-organism.md §3.1 and its answer line, on branch `origin/claude/s32-multi-stroke-launch-qpq9g2`:

> "FROM THE LOW-END EXIT (0.45 m/s) it fails on WEIGHT SUPPORT, not thrust: the lobe would need CL 1.3-10 to hold the body clear of the water. Minimum supportable speed is 0.51-1.39 m/s"

**Context needed to read it.** The organism is S28's *designed* zebrafish: an extrapolated 192 mm², AR 5 pectoral "wing", 0.25–0.40 g. In S32's taxi model the body and wing are in air, and a fraction φ of an *assumed* 18.9 mm² lower caudal lobe stays in water. The vertical balance is

½ρ_w U² (φ·S_lobe) CL_z = W·[1 − (U/V_to)²] + 2σc·cosθ

The 0.45 m/s figure is the low end of the measured *swimming* burst range, 0.45–1.38 m/s (Miln et al. 2021, VIA S28). S28 states that this is "*swimming* burst, not water-exit speed".

**Prior work on this claim (read in full this session).** Two challenges have already been filed, `origin/claude/challenge-270-lobe-cl-nq8ftq` and `origin/claude/challenge-claim-270-akzls7`. Both reproduce the arithmetic and both return WEAKENED at the generous end. I reuse their numbers only where I recomputed them, and I mark those places.

**Read levels used below.**
- **full-text**: the whole document was read.
- **partial full-text**: a full-text page was read through a fetch tool, for the stated part only.
- **search-summary**: a search-engine summary only.
- **could-not-access**: the source was blocked or not reached.

Everything I label *calculated* comes from the one-line script in §4. **None of it is an observation.**

---

## 1. Entailments

If claim 270 is true, it requires the following at the adjacent scales. Constraints C1–C3 are at the **organ** scale (the caudal lobe and its surface). C4–C5 are at the **behaviour** scale (how the fish leaves the water and holds its attitude in air).

| # | Scale | Kind | Requirement, stated generically | Bound (calculated from S32's inputs) |
|---|---|---|---|---|
| C1 | organ | range | The immersed planform area of the propulsor lobe must be too small to carry the unsupported weight at 0.45 m/s with a vertical-force coefficient of 1 | S_imm < **24.0 mm²** (0.25 g, cosθ = 0). For full immersion this means a lower-lobe area < 24.0 mm², or a whole fin < ~48 mm² if the lobes are equal |
| C2 | organ | range | The lobe's attainable time-averaged vertical-force coefficient, referenced to forward speed, at chord Re ≈ 2.7×10³, must be below what support needs | CL_z,max < **1.27** for the claim to hold across its whole range. Only < 2.99 is needed for the central case and < 9.95 for the stingy case |
| C3 | organ | range | The propulsor surface must not be hydrophobic enough for the meniscus to *lift* the fish | cosθ > **−0.594**, i.e. water contact angle in air θ < **126°** (generous case). The central and stingy cases fail for any θ |
| C4 | behaviour | range | The animal must actually leave the water at about 0.45 m/s, roughly horizontally, with the body clear and the lobe immersed. Otherwise the claim describes a state that does not occur | water-exit speed distribution must include ~**0.45 m/s**, with a shallow exit angle |
| C5 | behaviour | range | While airborne the fish must not pitch nose-up far enough to redirect lobe thrust into support | pitch α < **6.3°** (generous, with CL_z = 1 lobe lift) or < **31.4°** (generous, no lobe lift). The central and stingy cases fail at any α, because the lobe force is 0.62× and 0.13× of the need |

**Notes on the bounds.**
- **C1.** The bound is (vertical need)/q. The need is 2.427 mN (generous, from W = 2.453 mN), and q = 101.25 Pa. Central gives 28.2 mm² and stingy (0.40 g) gives 47.0 mm².
- **C3.** The meniscus term 2σc = 0.864 mN. The generous case would close at CL_z = 1 only if 2σc·cosθ ≤ −0.513 mN.
- **C5.** The tilt numbers use S32's own lobe thrust at 0.45 m/s: 4.664 / 1.761 / 0.607 mN. I recomputed them. They match challenge nq8ftq (6.3°) and challenge akzls7 (~31°), which are the two variants of the same calculation.

## 2. Checks

### C1: lobe area < 24 mm² (organ, range) — **unsatisfied (nobody has reported the number; within my scope)**

- **Read.** Cardeira et al. 2016, *Sci. Rep.* 6:39191 (PMC5171864), **partial full-text**: characters 0–100,000 of 115,000 were read; the final ~15,000 were not.
  - It reports caudal fin areas **only as normalised ratios** (REG/STU, RMA/RAY, % of the 240 hpa mean).
  - It says pixel measurements were converted to mm², but it does not report the converted values.
  - Its fish were "50–200 mg (mean 100 mg) total weight, and measuring 15–24 mm (mean 19 mm) total length".
- **Not reached.** Chopra et al. 2023 (*iScience*) measured adult caudal fin areas in triplicate on 18 fish (**search-summary** of a ZFIN figure caption). Its values were not seen.
- **Search scope.** One web search ("adult zebrafish caudal fin area mm2 measured absolute"), plus the one paper read above. S32 independently reports the same gap: "No adult zebrafish fin area was found (searched; regeneration papers report normalised areas)".
- **Finding.** The quantity has been *measured* (Chopra 2023 measured it; Cardeira 2016 converted to mm² internally) but it has *not been reported* in anything I could read. This is "people measured it and the number did not reach me", not "nobody has looked". The constraint stays unsatisfied. Its satisfaction is one supplementary-table read away.
- **Scale tension (my inference).** Cardeira's cohort, 50–200 mg, is lighter than S32's 0.25–0.40 g. The weight and the fin area need to come from the same fish. Taking an area from a lighter cohort would bias C1 toward being satisfied.

### C2: CL_z,max < 1.27 at Re ~2.7×10³ (organ, range) — **open**

- **What I found** (all **search-summary**, no numbers seen):
  - Low-AR flat plates at Re ≈ 10⁴ reach a "large maximum lift coefficient" through tip-vortex lift, and CL_max *decreases* as Re falls toward and below ~3×10³. These are Okamoto et al. JJSASS 2017, a KAKEN project report, and a JAXA 2018 record.
  - The lobe's Re of ~2.7×10³ sits right at that transition, so the direction of the Re effect favours the claim. **The magnitude is unknown to me.**
- **Could not access:**
  - Torres & Mueller 2004 tables (typeset.io blocked);
  - jstage.jst.go.jp, kaken.nii.ac.jp and jaxa.repo.nii.ac.jp (outside the allowed network domains).
- **Pushing the other way:** challenge akzls7 cites delayed-stall flapping-foil CL ≈ 2 at Re 10²–10⁴ (search-summary there). I did not verify it.
- **Proxy problem.** Both challenges note that an *uncanted vertical* lobe makes little vertical force from forward flow at all. In that case the relevant number is below 1 and C2 is comfortably met. The flapping-driven force, however, is not captured by a U-referenced CL.
- **Finding.** No measured value meets or contradicts the bound. The sources disagree in direction (steady low-Re decline vs. unsteady augmentation), and I preserve that disagreement. **Open.**

### C3: fin surface water contact angle in air < 126° (organ, range) — **satisfied (literature; analogue tissue and taxa)**

- **Waghmare, Gunda & Mitra 2014**, *Sci. Rep.* (PMC4264028), **partial full-text** via fetch tool. *Measured* on tilapia (*Oreochromis niloticus*) scales, water in air: **34.1 ± 2.7° with mucus, 85.7 ± 4.7° without mucus.**
- **The same paper citing Bixler & Bhushan**, on trout (*Oncorhynchus mykiss*) scales: **< 10° with mucus, 58° without.** This is a citation; I did not read the original.
- **Liu et al. 2009**: described in the same paper as "complete wetting in air", with no number. The original was not read.
- **Conclusion.** Every measured value is < 90° (cosθ 0.07–0.98), far below the 126° that would rescue the generous case. The constraint is met.
- **Calculated consequence.** At the measured cosθ, the generous case needs CL_z **1.30–1.71**, not 1.27. S32's generous assumption cosθ = 0 is therefore *optimistic for support*, and this check **strengthens** the claim.
- **Scope caveat.** These are scale surfaces of tilapia and trout, not zebrafish fin-ray membrane. No zebrafish fin contact angle was searched for or found.

### C4: water exit at ~0.45 m/s, near-horizontal, body clear and lobe immersed (behaviour, range) — **unsatisfied (no zebrafish exit measurement found; within my scope)**

- **The 0.45 m/s value.** It is a swimming-burst speed (Miln et al. 2021, VIA S28, not re-read by me). S28 flags that it is "not water-exit speed".
- **Gibb, Ashley-Ross, Pace & Long 2011**, *J. Exp. Zool. A*, **search-summary**. They filmed zebrafish jumping *on a moist surface (land)*. No take-off speed was seen, and this is not water exit.
- **Soares & Bierman 2013**, *PLoS ONE* 8:e61617 (guppy, the nearest small-fish analogue), **partial full-text** via fetch tool:
  - *Measured* peak speed 102.36 ± 33.75 cm/s in water and 123.57 ± 30.0 cm/s in air. The paper also gives 100.16 ± 33.9 in its text, an internal inconsistency it does not resolve.
  - "Angle of attack of jump" **77.4° ± 24.91°**, defined as the angle between head and water surface.
  - Tail beats continue out of water. **No taxi with the tail immersed and the body held clear is described.**
  - The paper's Table 1 lists weight "98±10 g" for fish of SL 1.85 cm. That is presumably mg; I report it as printed.
- **Reading it (my inference).** The one measured small-fish analogue exits at about 1 m/s and steeply (~77°), not at 0.45 m/s near-horizontally. It does not contradict C4, because a different species and a different behaviour cannot contradict a zebrafish requirement. But it also does not supply the configuration the claim presupposes.
- **Search scope.**
  - One search for zebrafish water-exit and jump take-off speed.
  - One search for small-fish tail skittering. That found only needlefish and halfbeaks, at ~10 m/s and at encyclopedia or popular-press level.
  - One search for hatchetfish taxiing. Wiest 1995, via a seriouslyfish summary: the pectorals drive the exit, and no speeds are given.
- **Finding.** As far as this scope reaches, **nobody has measured zebrafish water-exit speed or exit angle.** This is "not looked", not "looked and found nothing".

### C5: airborne pitch below 6.3° (generous) (behaviour, range) — **open**

- **No measurement found.** I found no measured airborne body pitch for zebrafish. Soares & Bierman (above) plot body angle over time in Fig. 1C but give no aerial-phase values. I did not search further.
- **Geometric inference (assumed dimensions, no measurement).**
  - The generous case sets φ = 1 (whole lower lobe immersed) and horizontal thrust.
  - With S32's assumed fin height of 9 mm, the lower lobe reaches only ~4.5 mm below the peduncle midline.
  - Full immersion with the belly clear therefore probably requires *some* nose-up tilt.
  - If so, the generous case's two assumptions pull against each other, and the tilt they force would itself supply support.
  - This point rests on body and fin dimensions that are assumed, not measured. **I do not count it as a check.**
- **Finding.** **Open.** This is the constraint most likely to break the generous end of the claim, and it is the cheapest to test: one high-speed side view of a zebrafish tail-beating with its body in air.

## 3. Summary

| # | Status | What decided it |
|---|---|---|
| C1 lobe area < 24 mm² | unsatisfied | Measured by others, but not reported in anything I could read |
| C2 CL_z,max < 1.27 | open | Numeric sources were blocked; the literature disagrees in direction |
| C3 contact angle < 126° | **satisfied** | Measured 34–86° (tilapia) and < 10–58° (trout, cited). This tightens the generous need to CL 1.30–1.71 |
| C4 exit at 0.45 m/s, horizontal | unsatisfied | No zebrafish exit measurement exists in my scope. The guppy analogue exits at ~1 m/s and ~77° |
| C5 pitch < 6.3° | open | Not measured |

**No constraint is unsatisfiable.** No measured number contradicts claim 270 from below.

**The robust part of the claim.** The central and stingy cases fail for any contact angle and any pitch, and for CL_z,max up to 2.99 and 9.95 respectively. This conclusion is calculated.

**The fragile part.** The generous end hangs on C2 and C5, which are both open. It also hangs on C4, the presupposition that a 0.45 m/s near-horizontal exit happens at all, and that is unsatisfied.

**Not entailed, noted in passing (calculated, assumed body depth 3–6 mm).**
- The support deficit would sink the body by one body depth in **24–76 ms**, which is **1.2–4 strokes** at the measured 52 Hz (Kyriakatos 2011, VIA S24).
- So S32's quasi-steady treatment of support is marginal at this speed, and unsteady lobe forces (C2) cannot be dismissed on timescale grounds.

## 4. Reproduction

```
python3 -c "q=0.5*1000*0.45**2; s2=2*0.072*0.006; W=0.25e-3*9.81; need=W*(1-(0.45/4.41)**2); print(need/q*1e6, (q*18.9e-6-need)/s2)"
# -> 23.97 mm^2 (C1 bound), -0.594 (C3 cos(theta) bound)
```

Other constants used: tilt bounds asin((need − q·S)/T) and asin(need/T), with T = 4.664 mN, and CL at the measured cosθ = (W' + s2·cosθ)/(q·S). All inputs are S32's, as stated in its §2.

## Sources
- S32-organism.md, `origin/claude/s32-multi-stroke-launch-qpq9g2`: full-text.
- S28-organism.md lines matching 0.45, `origin/claude/s28-organism-design-5z0vjz`: grep-level (partial).
- Challenges 270 (nq8ftq, akzls7): full-text.
- [Cardeira et al. 2016, Sci. Rep.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5171864/): partial full-text.
- [Waghmare et al. 2014, Sci. Rep.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4264028): partial full-text.
- [Soares & Bierman 2013, PLoS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629028): partial full-text.
- Gibb et al. 2011 *J. Exp. Zool. A*: search-summary.
- Chopra et al. 2023 *iScience*: search-summary.
- Okamoto et al. 2017 JJSASS, KAKEN 16K06894, JAXA 2018: search-summary.
- Torres & Mueller 2004: could-not-access.
- Wiest 1995: search-summary (via seriouslyfish.com).

```swarm-entail
{"source_claim": 270, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The immersed planform area of the caudal propulsor lobe must be too small to carry the unsupported weight at 0.45 m/s with a vertical-force coefficient of 1",
      "quantity": "immersed lower-lobe planform area (0.25 g fish, cos theta = 0)", "lo": null, "hi": 24.0, "units": "mm^2",
      "status": "unsatisfied",
      "satisfied_by": "No absolute adult zebrafish caudal-fin area found in readable sources; Cardeira 2016 reports only normalised areas; Chopra 2023 measured areas but values not seen",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated from S32 inputs (need 2.427 mN / q 101.25 Pa; central 28.2, stingy 47.0 mm^2). Cardeira et al. 2016 Sci Rep 6:39191 partial full-text (fish 50-200 mg, lighter than S32's 0.25 g); Chopra et al. 2023 iScience search-summary. Scope: one web search plus one paper; S32 reports the same gap. Measured-but-unreported, not unlooked-for."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The lobe's attainable time-averaged vertical-force coefficient referenced to forward speed, at chord Re ~2.7e3, must lie below what support requires",
      "quantity": "CL_z,max of lobe", "lo": null, "hi": 1.27, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not determined: low-AR flat-plate CLmax reportedly declines below Re ~3e3 (no numbers seen), while flapping delayed-stall CL ~2 is cited against",
      "satisfied_evidence": "unknown",
      "note": "Okamoto et al. 2017 JJSASS, KAKEN 16K06894, JAXA 2018: search-summary only. Torres & Mueller 2004, jstage, kaken, jaxa repo: could-not-access (network). Flapping CL ~2 from challenge akzls7, unverified. Bound is 2.99 (central) and 9.95 (stingy) if only those cases are claimed."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The propulsor surface must not be hydrophobic enough for the meniscus to lift the body",
      "quantity": "water contact angle in air on fin/skin surface", "lo": null, "hi": 126, "units": "deg",
      "status": "satisfied",
      "satisfied_by": "Measured fish-scale water contact angles in air 34.1+-2.7 deg (mucus) and 85.7+-4.7 deg (no mucus), tilapia; <10 and 58 deg, trout (cited)",
      "satisfied_evidence": "literature",
      "note": "Waghmare, Gunda & Mitra 2014 Sci Rep (PMC4264028) partial full-text, measured tilapia; Bixler & Bhushan trout values cited therein, original not read. Analogue tissue (scales) and taxa, not zebrafish fin membrane. Calculated consequence: generous case then needs CL_z 1.30-1.71, strengthening the claim. Central and stingy fail for any theta."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The animal must actually leave the water at about the low-end speed, near-horizontally, with body clear and lobe immersed",
      "quantity": "zebrafish water-exit speed", "lo": 0.45, "hi": 0.51, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish water-exit speed or angle found; 0.45 m/s is a swimming-burst speed (Miln 2021 via S28); guppy analogue exits at ~1.0 m/s and 77.4+-24.9 deg, no tail-immersed taxi described",
      "satisfied_evidence": "unknown",
      "note": "Soares & Bierman 2013 PLoS ONE partial full-text; Gibb et al. 2011 JEZ-A search-summary (jumps on land, not water exit). Scope: one search each for zebrafish exit/jump speed, small-fish skittering (only needlefish/halfbeak ~10 m/s, popular sources), hatchetfish taxi (Wiest 1995 via summary). Not looked for in zebrafish, rather than looked-for and absent."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "While airborne and tail-beating, the body must not pitch nose-up enough to redirect lobe thrust into weight support",
      "quantity": "airborne body pitch angle (generous case, with CL_z=1 lobe lift; 31.4 deg if no lobe lift)", "lo": null, "hi": 6.3, "units": "deg",
      "status": "open",
      "satisfied_by": "No measured airborne pitch for zebrafish; guppy paper plots body angle (Fig 1C) but gives no aerial values",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated from S32 lobe thrust 4.664 mN at 0.45 m/s; agrees with challenges nq8ftq (6.3 deg) and akzls7 (~31 deg). Central/stingy fail at any pitch (lobe force 0.62x, 0.13x of need). Soares & Bierman 2013 partial full-text. Geometric inference that full lobe immersion forces some tilt rests on assumed dimensions and is not counted as a check. Scope: no dedicated search."}
  ]}
```
