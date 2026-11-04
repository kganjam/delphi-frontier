# Claim 270: entailments at the organ and behaviour scales, checked

**Source claim (organism scale, evidence: derived).** From S32-organism.md §0 and §3.1, branch `origin/claude/s32-multi-stroke-launch-qpq9g2`, read in full-text:

> "FROM THE LOW-END EXIT (0.45 m/s) it fails on WEIGHT SUPPORT, not thrust: the lobe would need CL 1.3-10 to hold the body clear of the water. Minimum supportable speed is 0.51-1.39 m/s"

**Subject of the claim.** The subject is S28's *designed* zebrafish, 0.25–0.40 g, with an extrapolated 192 mm² pectoral wing. In S32's taxi, the body and wing are in air. A fraction φ (0.25 / 0.5 / 1) of an **assumed** 18.9 mm² lower caudal lobe stays in water. The vertical balance is:

½ρ_w U² (φ·S_lobe) CL_z = W·[1 − (U/V_to)²] + 2σc·cosθ, with CL_z capped at 1 (assumed)

**What this document adds.** Prior work on this claim was read in full-text: challenges `challenge-claim-270-akzls7` (WEAKENED) and `replicate-fish-270-3e54dl` (AGREE, arithmetic only). A separate entail exists on `origin/claude/claim-270-entail-6zqt7s`; I read it to avoid duplicating searches. Three things here are new:

- a **measured absolute adult zebrafish caudal-fin area**, which that entail could not find;
- a low-AR lift curve read directly from a figure;
- a **timescale** constraint that S32's own numbers bear on.

**Calculations and read levels.** Every number labelled *calculated* comes from `docs/research/fish/claim-270-entail_calc.py`, which uses S32's §2 inputs. **None of the calculated numbers are observations.** Each source carries one of these read levels: full-text | partial full-text | abstract | listing | search-summary | could-not-access.

---

## 1. Entailments

| # | Scale | Kind | Requirement, stated generically | Bound (calculated from S32's inputs) |
|---|---|---|---|---|
| C1 | organ | range | The planform area of the immersed caudal propulsor must be too small to carry the body's unsupported weight at 0.45 m/s with a vertical-force coefficient of 1 | S_imm < **24.0 mm²** (generous: 0.25 g, cosθ 0). Central < 28.3 mm²; stingy < 47.1 mm² |
| C2 | organ | range | The time-averaged vertical-force coefficient that the immersed propulsor can attain, referenced to forward speed, must be below the coefficient support requires | CL_z,max < **1.27** for the claim to hold across its whole range (< 2.99 central, < 9.95 stingy) |
| C3 | behaviour | range | The animal must actually leave the water at speeds below the minimum supportable speed. If every exit is faster, the failure mode never arises | water-exit speeds must occur below **0.51 m/s** (generous) to **1.39 m/s** (stingy) |
| C4 | behaviour | timescale | Once the body is clear, the time to accelerate from exit speed to the minimum supportable speed must be *longer* than the time for the support deficit to bring the body back into contact with the water. Otherwise the shortfall is crossed, not fatal | t_acc / t_sink > **1** |

Two kinds are deliberately not used:
- **No `spatial` constraint.** The geometric question is how deep the lower lobe reaches below the belly, which bounds φ. That needs zebrafish body-depth and lobe-depth numbers I did not find, so I list it under "not done" (§4) rather than invent a bound.
- **No `energetic` or `conservation` constraint.** The claim is explicitly not about thrust or power ("not thrust"). Vertical momentum balance *is* the claim itself, so it adds no requirement at an adjacent scale.

---

## 2. Checks

### C1: immersed lobe area < 24 mm² (organ, range) — **satisfied (measured, zebrafish)**

**Source.** Azevedo et al. 2011 (full author list not verified this session), "The regenerative capacity of the zebrafish caudal fin is not affected by repeated amputations", *PLoS ONE* 6(7): e22820.

**Read level.**
- Text: **partial full-text** via a fetch tool (methods and results summary).
- Figure 2: **read directly from the figure image** (`journals.plos.org/plosone/article/figure/image?...g002`).

**The measurement.** Fig. 2B and 2C plot "Area of the fin (mm²)" for adult *Danio rerio* caudal fins, measured in ImageJ. The fish were 1 year old when the protocol started. Reading the bars by eye (a figure read-off, not tabulated values, so ±1 mm²):
- uncut fins at 0 cuts: **≈ 29.5 mm²**, with the SD bar reaching ≈ 33.5;
- uncut age-matched siblings: **≈ 33 mm²**, with the SD bar reaching ≈ 40.

The paper's text, as returned by the fetch tool, gives n = 24 for the uncut comparison. It reports **no body length or mass**.

**Species on both sides.** Zebrafish and zebrafish. This is a same-species measurement.

**From whole fin to lower lobe (my inference, assuming the two lobes split the area equally).** The lower lobe is ≈ 14.8–16.5 mm², and ≤ 20 mm² even at the top of the larger SD bar. All of these values are below the 24.0 mm² bound, so the constraint is met.

**Calculated consequences.**
- With the measured area in place of S32's assumed 18.9 mm², the generous case needs **CL_z 1.46–1.63, not 1.27**.
- Its minimum supportable speed rises to **0.54–0.57 m/s**.
- At the top of the SD bar (20 mm² lobe) it needs 1.20, still above the cap of 1.
- So **the measurement strengthens the claim at its weakest (generous) end**. S32's assumed 37.8 mm² whole fin lies just at or above the upper SD bars, which makes it generous to the taxi.

**Caveats, stated rather than averaged away.**
1. **Mass mismatch, possibly.** The fish's mass is not reported. If they are lighter than 0.25 g, the area would be biased low relative to S32's fish. Supporting that possibility, Cardeira et al. 2016 (read via the prior entail, not by me) used 50–200 mg fish. A proportionally larger fin on a 0.25 g fish would raise the area as L², but would need a ~45 % larger lobe to break the bound.
2. **Equal-lobe split is assumed.**
3. **Immersed fraction.** If the *whole* fin were immersed (≈ 30–33 mm²), the bound would be exceeded. That configuration is not S32's, which immerses part of the lower lobe only, and it is not considered here.

### C2: attainable CL_z,max < 1.27 at chord Re ≈ 2.7×10³ (organ, range) — **open**

**What I read: Zhang & Taira 2020**, "Aerodynamic characterization of low-aspect-ratio swept wings at Re = 400", arXiv 2011.12336v1.
- Read level: **partial full-text**. The text was extracted from the PDF, and Fig. 3 was read from the rendered page.
- This is **simulated** (DNS), not measured. The object is a **wing with an airfoil section** (not a flat plate), at **Re = 400**, steady freestream, **not flapping**.
- Its midspan symmetry plane is a reasonable stand-in for the free-surface mirror in S32's AR_eff (my inference).
- For semi-aspect ratio 0.5–1, which brackets the lobe (span ≈ 3.2–4.5 mm on a 6 mm chord), Fig. 3a–b show **time-averaged CL ≤ ≈ 0.45 up to α = 30°**. For sAR 2 it is ≤ ≈ 0.6.
- The authors state that the lift coefficients "are significantly smaller than the inviscid limit for all three aspect ratios".

**Why this does not settle C2.**
- **The Reynolds number is ~7× below the lobe's.** Search-summary-level sources say low-AR plate CL_max *rises* with Re up to ~10⁴ through vortex lift: Okamoto et al. (JJSASS 2017), and a 2019 TJSASS paper on AR 1 plates at Re 10³–10⁴. I could not read either: jstage.jst.go.jp does not resolve in this session.
- **The flow is steady.** Challenge akzls7 cites delayed-stall flapping-foil CL ≈ 2 at Re 10²–10⁴ (search-summary there; not verified by me).
- **Taira & Colonius 2009** (*J. Fluid Mech.* 623:187), flat plates at Re 300/500: **could-not-access**, because authors.library.caltech.edu does not resolve in this session.

**Disagreement, preserved.**
- Steady low-Re simulations (simulated, Re 400) put CL far below the 1.27 bound.
- The unsteady flapping literature (search-summary, second-hand) puts it above.
- Neither is a measurement on a surface-piercing flapping fin at Re ~3×10³, and neither is about a zebrafish.

**Finding.** **Open.** No measured value meets the bound, and none contradicts it. Note also that C1's measured area moves this bound: with the measured lobe, the generous case needs CL_z,max < 1.46–1.63 for the claim to hold, which is easier to meet.

### C3: water exits occur below the minimum supportable speed (behaviour, range) — **unsatisfied (not looked for in zebrafish, as far as I can find)**

**Where 0.45 m/s comes from.** It is the low end of a measured *in-water swimming burst* range (Miln et al. 2021, via S28; I did not read it). S28 itself says it is "not water-exit speed".

**Searches, with scope.**
1. "zebrafish jump out of water leaping speed high-speed video".
2. "zebrafish jumping out of tank water surface jump behaviour measured height velocity".

Both returned search-summary results only. They found:
- Gibb, Ashley-Ross, Pace & Long 2011 (*J. Exp. Zool. A*, search-summary): zebrafish *terrestrial* jumps from a moist surface after stranding. **This is not water exit, and no speed was seen.** The same work notes that zebrafish do not leave the water in their natural habitat. That is the summary's wording, and I have not verified it in the original.
- A cross-taxon aquatic-jump scaling study (EPFL, search-summary). Zebrafish are not named in what I saw.

**Cross-species numbers (informative, not a test).** These are about other animals:
- **Guppy** (*Poecilia reticulata*): 1.02 → 1.24 m/s in air, exit angle ≈ 77°. Soares & Bierman 2013, read by the prior entail and S24, not re-read by me.
- **Archerfish**: jumps up to 1.4 m/s (search-summary).

Both exit at or above the generous U_min and below the stingy one. They neither meet nor contradict a zebrafish requirement.

**Finding.** **Unsatisfied.** Within the scope above, nobody appears to have *measured* zebrafish water-exit speed. This is "not looked at", not "looked at and found absent". The claim's premise, a 0.45 m/s exit with the body clear, is therefore a hypothetical state, not an observed one.

### C4: time to accelerate through the deficit exceeds time to sink (behaviour, timescale) — **open, with an internal inconsistency at the generous end (calculated)**

**Calculated from S32's own §3.1 forces, not measured.**

| Case | Net horizontal force at 0.45 m/s (S32) | U_min | t_acc to U_min | Sink |
|---|---|---|---|---|
| Generous | +4.09 mN | 0.507 m/s | **3.5 ms** | The vertical deficit at CL_z = 1 is 0.52 mN, so the body sinks **≤ 12 µm** in that time (≤ 0.38 mm over one whole 52 Hz stroke) |
| Central | −1.50 mN | 0.772 m/s | never (decelerates) | sinks 1 mm in **16 ms** |
| Stingy | −34.9 mN | 1.388 m/s | never (decelerates) | sinks 1 mm in **14 ms** |

**Reading it (my inference).**
- In S32's own model, the generous corner **does not fail**. It is 6 % below U_min and has a large positive horizontal net, so it crosses the deficit in a fraction of one tail-beat, while the body drops by micrometres.
- The constraint is therefore violated by the claim's own inputs at the generous end. It is met at the central and stingy ends, where the net is negative and the body sinks within one stroke.
- This agrees in direction with challenge akzls7's WEAKENED verdict, by a different route.
- It is **not** a refutation. t_acc is shorter than a stroke period (19 ms), so S32's cycle-averaged thrust is not valid on that timescale. Thrust within a stroke is unknown.

**What would decide it.** Two measurements:
- the airborne clearance of the body at exit;
- in-stroke thrust or acceleration of a zebrafish with only the tail immersed.

I found neither. The only search scope that touches them is C3's two searches. This constraint is **open**, not satisfied: the calculation exposes the issue, and no measurement resolves it.

---

## 3. Summary

| # | Scale / kind | Status | Decided by | Species on each side |
|---|---|---|---|---|
| C1 lobe area < 24 mm² | organ / range | **satisfied** | Azevedo 2011 Fig. 2: whole fin ≈ 29.5–33 mm², so lobe ≈ 15–17 mm² (measured; lobe split assumed). This tightens the generous case to CL_z 1.46–1.63 and U_min 0.54–0.57 m/s | zebrafish / zebrafish |
| C2 CL_z,max < 1.27 | organ / range | open | Steady DNS at Re 400 gives CL ≤ 0.45 (simulated). Flapping CL ≈ 2 is second-hand. Measured Re ~10⁴ sources were not reachable | wing / none |
| C3 exits below U_min | behaviour / range | unsatisfied (not measured) | No zebrafish water-exit speed found in two searches | zebrafish claim; guppy and archerfish data only |
| C4 t_acc > t_sink | behaviour / timescale | open | Calculated: met for central and stingy; violated *in S32's own model* at the generous end (3.5 ms vs µm-scale sink) | model only |

**No constraint is unsatisfiable.** No measured number contradicts claim 270 from below.

**What the two decided constraints show.**
- The one same-species measurement found (C1) makes the claim **stronger**.
- The one timescale check (C4) shows that the *generous end* of "fails" is not a failure even on S32's own equations. That check is calculated, not measured.
- The robust content of the claim is therefore the central and stingy cases. There, support fails, the fish decelerates, and the body sinks within one stroke.

## 4. Not done, with scope

- **Spatial constraint: lobe depth below the belly vs immersion depth.** This was not attempted. No zebrafish body-depth or lobe-depth measurement was searched for.
- **Chopra et al. 2023** (*iScience*) absolute fin areas: not read. The ZFIN figure page returned HTTP 503.
- **Network blocks this session:** jstage.jst.go.jp and authors.library.caltech.edu do not resolve. They would need to be allowed in the session's network settings to read Okamoto 2017/2019 and Taira & Colonius 2009.

## Sources

| Source | Read level |
|---|---|
| S32-organism.md (`origin/claude/s32-multi-stroke-launch-qpq9g2`) | full-text |
| Challenge 270 (akzls7), replication 270 (3e54dl), prior entail (6zqt7s) | full-text |
| [Azevedo et al. 2011 PLoS ONE 6:e22820](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0022820) | partial full-text; Fig. 2 image read directly |
| [Zhang & Taira 2020, arXiv 2011.12336](https://arxiv.org/abs/2011.12336) | partial full-text (simulated) |
| Gibb et al. 2011 J. Exp. Zool. A | search-summary |
| Okamoto et al. JJSASS 2017; TJSASS 2019 AR-1 plate | search-summary; could-not-access |
| Taira & Colonius 2009 J. Fluid Mech. 623 | could-not-access |
| Chopra et al. 2023 iScience | search-summary (figure caption only) |
| Soares & Bierman 2013 PLoS ONE (guppy) | not re-read; via S24 and prior entail |
| Archerfish jump speed | search-summary |

```swarm-entail
{"source_claim": 270, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The planform area of the immersed caudal propulsor must be too small to carry the unsupported body weight at 0.45 m/s with a vertical-force coefficient of 1",
      "quantity": "immersed lower caudal lobe planform area (0.25 g fish, cos theta 0)", "lo": null, "hi": 24.0, "units": "mm^2",
      "status": "satisfied",
      "satisfied_by": "Measured adult zebrafish whole caudal fin area ~29.5-33 mm^2 (SD bar tops ~33.5-40), giving a lower lobe of ~15-17 mm^2 (<=20 mm^2) under an assumed equal-lobe split",
      "satisfied_evidence": "measured",
      "note": "Azevedo et al. 2011 PLoS ONE 6:e22820, Fig 2B/C read by eye from the figure image (+-1 mm^2); text partial full-text; 1-year-old zebrafish, n=24 uncut, mass not reported. Same species on both sides. Calculated consequence: generous case needs CL_z 1.46-1.63 and U_min 0.54-0.57 m/s, strengthening the claim. Bound 28.3 (central), 47.1 (stingy) mm^2."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The attainable time-averaged vertical-force coefficient of the immersed propulsor, referenced to forward speed at chord Re ~2.7e3, must lie below what support requires",
      "quantity": "CL_z,max of the immersed lobe", "lo": null, "hi": 1.27, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Steady DNS of low-AR wings (sAR 0.5-2) at Re 400 gives time-averaged CL <= ~0.45-0.6 up to 30 deg (simulated, wrong Re, not flapping, not a fin); flapping delayed-stall CL ~2 cited second-hand against",
      "satisfied_evidence": "simulated",
      "note": "Zhang & Taira 2020 arXiv 2011.12336 partial full-text, Fig 3. Okamoto et al. JJSASS 2017 and an unnamed-author TJSASS 2019 paper on AR-1 plates at Re 1e3-1e4: search-summary, jstage could-not-access (DNS fail). Taira & Colonius 2009: could-not-access. Disagreement preserved. With C1's measured lobe area the bound relaxes to 1.46-1.63."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The animal must actually leave the water at speeds below the minimum supportable speed, or the failure mode never arises",
      "quantity": "zebrafish water-exit speed", "lo": null, "hi": 0.51, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish water-exit speed found; 0.45 m/s is an in-water burst speed (Miln 2021 via S28). Gibb et al. 2011 measured terrestrial (stranding) jumps, not water exit. Cross-species only: guppy 1.02->1.24 m/s, archerfish up to 1.4 m/s",
      "satisfied_evidence": "unknown",
      "note": "Scope: two web searches (zebrafish leaping speed; zebrafish jumping out of tank), search-summary level. Not looked for in zebrafish rather than looked for and absent. hi is the generous U_min; stingy U_min is 1.39 m/s. Guppy (Soares & Bierman 2013) and archerfish are different species and are not a test."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Once the body is clear, the time to accelerate from exit speed to the minimum supportable speed must exceed the time for the support deficit to return the body to the water",
      "quantity": "t_acc / t_sink", "lo": 1, "hi": null, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Calculated from S32's own forces: central and stingy decelerate (net -1.50, -34.9 mN) and sink 1 mm in 14-16 ms (met); generous reaches U_min 0.507 m/s in 3.5 ms while sinking <=12 um (violated in-model). No measurement of exit clearance or in-stroke thrust with only the tail immersed",
      "satisfied_evidence": "derived",
      "note": "docs/research/fish/claim-270-entail_calc.py. Not a refutation: t_acc < one 52 Hz stroke (19 ms), where S32's cycle-averaged thrust is not valid. Agrees in direction with challenge akzls7 (WEAKENED at generous end). Searched only within C3's scope."}
  ]}
```
