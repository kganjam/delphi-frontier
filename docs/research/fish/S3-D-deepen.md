# S3-D-D: deepening S3-D by attacking its weakest input, the lift coefficient a launch can actually use

**Parent.** S3-D: `docs/research/fish/S3-deepen.md` and `S3-deepen_calc.py`, on branch
`claude/s3-mass-power-budget-rcrklv` (commit `1384d67f`). I read both in full this session. S3-D in
turn rests on S3: `S3-organism.md` and `S3_budget.py`, on branch
`claude/s3-organism-mass-budget-000ync` (commit `d0fd062f`). I read S3 §0–2 this session.

**The recorded answer was blank.** The task prompt quoted S3-D's recorded answer as empty, so I took
the answer from S3-D's own `swarm-result` block:
- **Verdict: STANDS.**
- Closure of the most generous launch case needs **CL_max ≥ 2.16**.
- The best fin-wing CL found is **1.0–1.1**.
- So the budget is about 2× short on lift.

**Status: derived.** This document recalculates the result with one input re-examined. **Nothing in
it is a measurement, by this project or by me.**
- Every computed number is printed by `python3 -I docs/research/fish/S3-D-deepen_calc.py`.
- That script re-implements S3's §3.5 launch model and asserts that it reproduces S3's
  409 W kg⁻¹ and 2,878 W kg⁻¹ and S3-D's 2.16.
- Each literature value carries its read-level in the sentence where it is used.

## 0. Result

**Verdict: STANDS. The margin narrows, and it now has a known edge.**

**1. The most sensitive input is still CL.** The specific weak point is S3-D's choice of *which*
CL to use.
- S3-D's conclusion is a margin: CL_needed / CL_best = 2.16 / 1.10 = **1.96**.
- Doubling CL_best takes the margin to **0.98**, so the verdict falls.
- Doubling any other input leaves the margin at 1.24 or above (computed, §1).
- So the conclusion stands or falls on whether any lift mechanism available to the fish gives
  about 2× the steady fin-wing value.

**2. How well is 1.0–1.1 established? Not well, and not as S3-D framed it.**
- **I read Park & Choi 2010 at full text this session** (first ~100k of 157k characters, through a
  summarising fetch tool). It contains **no numeric CL in its text**. The values exist only in
  Fig. 5, which is an image I could not read.
- That paper normalises CL by **A = A1 + A2 + A3**, where A1 is the pectoral fins, A2 the pelvic
  fins and A3 **the body** (verbatim, §2).
- S3 and S3-D applied that CL to **wing area only**. That undercounts the lift available to a design
  whose body also lifts.
- The number 1.0–1.1 is still only a search-engine quotation of a 2007 proceedings paper.
- "1.03" is a CFD result from a different paper (2019), not a measurement.

**3. Improving the input.** I bracketed three lift regimes S3-D left out:

| Regime | CL | Source | Read-level |
|---|---|---|---|
| (A) Steady, fin wing | 1.0–1.1 | Park & Choi | search-summary |
| (B) Steady leading-edge-vortex lift on revolving wings | 1.44–1.64 | Usherwood 2009 | search-summary |
| (C) Transient impulsive-start lift | +80 % for about 2 chords of travel | Dickinson & Götz 1993 | abstract |

Separately, I added the body as lifting area, as a scenario, because a measured zebrafish planform
area was not found.

**4. Recomputed (calculated, not observed):**
- **Steady fin CL with the body counted** (the consistent use of Park & Choi's normalisation): CL
  needed falls to **1.76**, and the generous case is **2.03–2.75× short**. **Stands.**
- **Revolving-wing LEV values:** **1.12–1.84× short**. **Stands.** These values also need
  rotation, which a translating run-up does not supply.
- **Transient lift plus body lift:** this stack **does reach parity** (0.84–0.97×). It lasts about
  2 chords of travel, which is **14.5 ms** and buys a calculated **≈1 mm hop**. When it decays, lift
  falls to **0.56 of weight**. Staying up needs 2.47 m/s against the 1.84 m/s reached. A sustained
  launch is still **2.03× short**.
- **So the budget does not close for a launch into flight. It closes only for a hop of about a
  millimetre.**

**5. What changed from S3-D:**
- S3-D said closure needs "about 2× every steady value found", and that power fails by
  2.75–3.17×.
- That margin was overstated in one direction and understated in another:
  - **Overstated:** body lift and the reference-area convention lower the requirement to 1.76.
  - **Understated by nothing so far:** no lift mechanism found sustains CL ≥ 1.76 on a
    translating wing.
- The honest margin on sustained launch is **1.6× in lift (1.76 vs 1.10) and 2.0× in power**. It is
  not S3-D's 1.96× and 2.75×. The verdict is the same.

---

## 1. Which input S3-D's conclusion is most sensitive to (recomputed)

S3-D's conclusion is the inequality CL_needed > CL_best. Both sides were perturbed separately. Each
non-CL input moves CL_needed, and CL_best moves directly (script §1):

| Input (value) | ×2 → margin | ×0.5 → margin | Verdict at ×2 error |
|---|---|---|---|
| **CL_best (1.10)** | **0.98** | 3.93 | **FALLS** |
| η_h (0.37) | 1.24 | 3.12 | stands |
| f_m (0.6) | 1.24 | 3.12 | stands |
| run-up (2 BL) | 1.24 | 3.12 | stands |
| muscle power (142.7 W kg⁻¹) | 1.24 | 3.12 | stands |
| σ (0.138 kg m⁻²) | 2.92 | 1.54 | stands |
| m_body (0.40 g) | 3.08 | 1.46 | stands |

The power-side inputs enter CL_needed as factor^(−2/3), because the shortfall ∝ CL^−1.5. So a ×2
error on any one of them moves CL_needed only by 1.59×. CL_best enters linearly, so it is the only
input whose factor-2 error flips the verdict. This confirms S3-D's choice of input. **It does not
confirm S3-D's value.**

## 2. How well is CL_best = 1.0–1.1 established?

**Park & Choi 2010**, *J. Exp. Biol.* 213:3269, doi:10.1242/jeb.046052.
- **Read-level: full-text, partial.** I read characters 0–100,000 and 100,000–157,328 of the
  journals.biologists.com HTML through a summarising fetch tool that quotes sentences. **Fig. 5 and
  Tables 1–2 are images and were not read.**
- Verbatim quotes:
  - "the reference area as the sum of the planform areas of the pectoral (A1) and pelvic (A2) fins and body (A3)."
  - "The measurements were performed at the free-stream velocity (u∞) of 12 m s–1"
  - Re = 1.9–2.2 × 10⁴ "based on the average pectoral-fin chord" (the fetch tool's paraphrase, not a verbatim quote)
  - "the lift coefficients for models L1–L3 and M are largest at α=30–35 deg."
  - "The maximum lift coefficient of flying fish is measured at α=30–35 deg"
  - Without pelvic fins, "the lift coefficient is smaller than those with pectoral and pelvic fins (models L1–L3) by more than 20%"
- **Negative, with its scope:** in both passes, the fetch tool found **no numeric CL value** in the
  text. Scope: the HTML text only, not the figure images.
- The A1/A2/A3 areas are in Table 1, an image, so they are `unknown`. My attempts to get the PDF
  failed: curl got Cloudflare "Just a moment...", Playwright got the same, and cob.silverchair.com
  got proxy 403 and then did not resolve.

**The 1.0–1.1 itself.**
- It comes from a search engine's quotation of Park & Choi's IUTAM 2007 proceedings,
  "the maximum lift coefficients are about 1.0 ~ 1.1". **Read-level: search-summary** (S3-D's
  retrieval, not repeated here).
- The PDF host flair.monash.edu returned proxy 403 this session.

**The 1.03.**
- A search summary this session attributed it to the 2019 *Bioinspir. Biomim.* CFD study
  (doi:10.1088/1748-3190/ab23e6, PubMed 31117061). That study "follow[s] a previous wind tunnel
  experiment (Park and Choi 2010)" (**search-summary**).
- So it is a **simulation**, as S3-D already said. It is not a second measurement.

**Assessment:**
- **Measured?** Yes, the value is a wind-tunnel measurement, but on whole dried flying-fish models
  at Re ≈ 2 × 10⁴. That is 8× the designed wing's Re of 2,468 (computed, script §5).
- **What the number is.** It is a **whole-animal coefficient normalised by total planform**,
  including the body. S3 and S3-D applied it to wing area alone.
- **My inference on the direction.** For a design whose body also lifts, this convention makes S3-D
  *pessimistic*: it ignores lift the denominator was built to include. For the wing alone, the
  wing-only CL is `unknown` from what I read. The author's claim covers only the whole model.
- **Repeated until it reads as measured?** Partly. "1.0–1.1, measured" has travelled from S3-D into
  descendants. Its only textual basis is a search-engine snippet. The primary paper states the angle
  of maximum lift, but not its value, in any text I could read.

## 3. Improving it: what CL can a launching fish actually use?

The real quantity is not the "steady CL_max of a fin". It is **the lift per unit of lifting
planform that the animal can hold for long enough to leave the water and stay up**. Three regimes
bear on it.

| # | Regime | Value | Re | Source | Read-level |
|---|---|---|---|---|---|
| A | Steady, translating, whole flying fish | ~1.0–1.1, normalised by fins + body | 1.9–2.2 × 10⁴ | Park & Choi 2007 / 2010 | search-summary (value); full-text partial (normalisation, Re) |
| B1 | Steady LEV on a **revolving** flat-card replica of a pigeon wing | **1.44** | up to 1.08 × 10⁵ (one secondary source says 10,800: **disagreement preserved**) | Usherwood 2009, *Exp. Fluids* 46:991, doi:10.1007/s00348-008-0596-z | search-summary |
| B2 | same, **real dried pigeon wing** | **1.64**, at ~43° | same | same | search-summary |
| C | **Transient** after an impulsive start (translating) | "an 80% increase in lift compared to the performance measured 5 chord lengths later"; the LEV "stayed attached to the wing for the first 2 chord lengths of travel" | 10 < Re < 1000 | Dickinson & Götz 1993, *J. Exp. Biol.* 174:45 | abstract (journals.biologists.com, this session). **No absolute CL in the abstract** |

**Usherwood & Ellington 2002 (I and II)**, *J. Exp. Biol.* 205:1547 and 205:1565.
- **Read-level: abstract** (Europe PMC, this session).
- The abstracts state "high" force coefficients at Re 1,100–26,000 but give no value.
- The full text was paywalled ("You do not currently have access").
- So no number is taken from them.

**Dickinson, Lehmann & Sane 1999**, *Science* 284:1954.
- **Read-level: abstract.** It gives no number, so none is used.

**Limits, kept visible:**
- **B needs revolution.** The sustained LEV in B is held by spanwise flow on a rotating wing. A fish
  with wings spread during a straight run-up is a *translating* wing, so B applies to a flapping
  design (S10) and not to S3's run-up model. **I include B as an upper bound only. Using it there is
  my scenario, not the source's claim.**
- **C is relative, not absolute.** The "+80 %" is relative to the same wing 5 chords later, not to
  a steady CL_max. Applying ×1.8 to 1.07–1.10 is **my scenario**. It is generous, because the
  5-chord value at α > 13.5° may itself sit on the post-stall plateau.
- **C's Re is ~2.5× below the designed wing.**

**Body as lifting area (scenario).**
- A measured dorsal planform area for a 0.4 g zebrafish is `unknown`. Scope of that negative: I
  searched only S3 §0–2's inputs. No primary search was run on it.
- I bracket 0 / 120 / 240 mm². The 240 mm² case is my assumption of about 40 mm × 6 mm. It is
  generous.

**What would settle it, and what it would cost:**
1. **Digitise Park & Choi 2010 Fig. 5 and Table 1** (A1, A2, A3). That gives the measured CL and the
   wing fraction of area. Cost: one PDF. The only blocker is network policy: journals.biologists.com
   is behind a Cloudflare challenge, and cob.silverchair.com and flair.monash.edu are outside this
   session's allowed hosts. This is the cheapest improvement left.
2. **The S3-D micro-balance tunnel test, extended.** Run an excised long-fin zebrafish pectoral fin,
   or a membrane replica, at 2–6 m/s. Record (i) the steady polar and (ii) the **impulsive-start
   lift history over the first 5 chords**. Item (ii) measures regime C at the right Re and material.
   Expected forces are ~0.5 mN (S3-D's computation). Cost (my estimate, not a quote): days on an
   existing insect-flight rig.

## 4. Recompute S3-D with the improved input

All rows are the most generous case: the S10 wing, 2 BL run-up, η_h 0.37, f_m 0.6. Calculated by
script §2–4.

| CL regime | CL | Body lift (scenario) | Shortfall | Closes? |
|---|---|---|---|---|
| S3-D baseline | 1.07 | none | 2.87× | no |
| A, steady fin | 1.00–1.10 | none | 2.75–3.17× | no |
| A, steady fin, normalisation-consistent | 1.10 | 120 / 240 mm² | 2.34× / **2.03×** | no |
| B, revolving LEV (upper bound only) | 1.44–1.64 | none | 1.51–1.84× | no |
| B2 + body | 1.64 | 240 mm² | 1.12× | no |
| C, transient | 1.93–1.98 | none | 1.14–1.19× | no |
| **C + body** | 1.98 | 120 / 240 mm² | **0.97× / 0.84×** | **for ~15 ms only** |

**The transient case, followed through** (script §4, calculated):
- The S10 mean chord is 13.4 mm, so 2 chords is 26.8 mm of travel.
- At the 1.84 m/s where transient plus body lift equals weight, that is **14.5 ms**.
- A generous bound, taking 1 g of excess lift for the whole window, gives 143 mm s⁻¹ of vertical
  speed and an **apex of 1.04 mm**.
- Once the LEV sheds, lift is **0.56 of weight**. Staying airborne on steady CL needs 2.47 m/s, not
  1.84 m/s.
- The fish is out of the water by then and cannot accelerate further. That is my inference: S3's
  model has no aerial thrust.
- **A sustained launch is still 2.03× short on power.**

**Conclusion (my inference from the computation):**
- **S3-D STANDS.** No regime found sustains a translating-wing CL near the 1.76 that closure needs,
  even with the body lifting.
- **What changed is the size and shape of the margin:**
  - It narrows from S3-D's "2.16 vs 1.1, ≈ 2×" to **1.76 vs 1.10, 1.6×**, once Park & Choi's
    normalisation is applied consistently.
  - It now has a defined edge. **Transient leading-edge-vortex lift stacked on body lift reaches
    parity, but only for about 15 ms**, which is a hop and not a launch.
- **That edge is the next weakest point.** If a fin could hold a near-transient CL (~1.8) for
  ~10 chords instead of 2, for example through membrane camber, the conclusion would need
  re-examining.
- **I did not find a measurement of how long the LEV persists on a translating membrane at
  Re ~2.5 × 10³.** Scope of that negative: Dickinson & Götz 1993 abstract only, plus 4 web searches
  (listed in §5).

## 5. Search scope and access log

**Europe PMC REST**, 5 DOI queries:
- Park & Choi 2010;
- Usherwood & Ellington 2002 I and II;
- Dickinson & Götz 1993 (0 hits);
- Dickinson et al. 1999.

All returned hits gave abstracts only. None is in PMC.

**journals.biologists.com via WebFetch:**
- Park & Choi 2010: full text, 2 passes.
- Usherwood & Ellington I and II: paywalled.
- Dickinson & Götz 1993: abstract.
- Two initial fetches went to wrong article IDs and returned unrelated papers. Those were discarded.

**Web searches (5):**
- 1 extended, for the Park & Choi CL value and reference area;
- 4 standard: Usherwood revolving-wing values; revolving-wing CL_max at Re 10³–10⁴;
  Li & Dong / Usherwood "1.64" "1.44"; the Dickinson 1999 translational CL.

**Hosts that failed:**
- cob.silverchair.com: proxy 403, then did not resolve.
- flair.monash.edu: proxy 403.
- rvc-repository.worktribe.com: did not resolve.
- journals.biologists.com raw HTML: Cloudflare challenge to both curl and headless Chromium.

**To raise A and B from search-summary to full text, these hosts must be allowed in the session's
network settings.**

## 6. What this does NOT establish

- **It measures nothing.** Each CL here is a literature value at search-summary or abstract level,
  or a scenario multiplier.
- **It does not test flapping launch**, which S10's planform implies and where regime B would be
  legitimate.
- **It inherits every other S3 input unchanged:**
  - η_h from pike;
  - f_m, which was assumed;
  - muscle power from *Scorpaena* (abstract);
  - σ from caudal-fin thickness with proxy densities;
  - the constant-acceleration run-up;
  - the 40 mm body length.
- **The body-lift bracket is an assumption,** not a measured zebrafish planform.

```swarm-result
{"subproblem": "S3-D-D", "evidence": "derived (recalculation of S3/S3-D's launch model; Park & Choi 2010 raised from abstract to partial full-text for normalisation and Re but its CL values sit in an unread figure; revolving-wing LEV CL at search-summary; impulsive-start enhancement at abstract; body lift area is an assumption; no new measurement)", "answer": "CL remains the only input whose factor-2 error flips S3-D; applying Park & Choi's whole-planform normalisation consistently lowers the CL needed for the most generous launch from 2.16 to 1.76 against a best steady fin-wing value of 1.10 (calculated 2.03x power shortfall), and only transient impulsive-start lift stacked on body lift reaches parity, for ~14.5 ms and a ~1 mm hop, so S3-D's 'power budget does not close' stands with its margin narrowed from ~2x to ~1.6x in lift.", "key_number": "CL usable for a sustained launch = 1.0-1.1 (whole-planform normalised, fins + body; Park & Choi, value search-summary) vs 1.76 needed when the body lifts (calculated); transient ceiling ~1.98 for ~2 chords = 14.5 ms", "verdict": "stands", "depends_on": ["S3-D conclusion: docs/research/fish/S3-deepen.md @ 1384d67f (CL_needed 2.16, CL_best 1.0-1.1, verdict stands)", "S3 launch model: docs/research/fish/S3-organism.md and S3_budget.py @ d0fd062f, P = (V^2/2)/t/eta_h * M/(f_m m_body), constant-acceleration run-up", "law: quasi-steady lift L = 0.5 rho V^2 S CL; take-off at stall speed", "Park & Choi 2010 J Exp Biol 213:3269 full-text (partial): CL normalised by A1+A2+A3 incl. body; u 12 m/s; Re 1.9-2.2e4; CL max at alpha 30-35 deg; no numeric CL in text", "Park & Choi IUTAM 2007: max CL about 1.0-1.1 (search-summary)", "2019 Bioinspir Biomim doi:10.1088/1748-3190/ab23e6: CL 1.03 is CFD, not measurement (search-summary/abstract)", "Usherwood 2009 Exp Fluids 46:991: revolving pigeon wing CL 1.64, card replica 1.44, ~43 deg (search-summary; Re 1.08e5 vs 10,800 disagreement)", "Dickinson & Goetz 1993 J Exp Biol 174:45 abstract: +80% lift vs 5 chords later, LEV attached for first 2 chords, 10<Re<1000", "assumption: x1.8 transient multiplier applies to steady CL_max 1.07-1.10 at Re ~2.5e3", "assumption: revolving-wing LEV CL is an upper bound only, not available to a translating run-up", "assumption: zebrafish body dorsal planform 0-240 mm^2 lifts at the same CL and adds no wing mass (unmeasured)", "assumption: no aerial thrust after water exit", "S10 planform 1070 mm2, span 80 mm (mean chord 13.4 mm)", "S3 input: eta_h 0.37 (pike, via S29, abstract)", "S3 input: fast-muscle power 142.7 W/kg (Wakeling & Johnston 1998, abstract)", "S3 input: muscle fraction f_m 0.6 (assumption / secondary review via S29)", "S3 input: run-up 2 body lengths of 4 cm (assumption)", "S3 input: central fin areal density 0.138 kg/m^2 (Puri 2018 caudal thickness, proxy densities)", "S3 input: body mass 0.40 g (project brief)", "air density 1.225 kg/m3, kinematic viscosity 1.5e-5 m2/s, g 9.81"]}
```
