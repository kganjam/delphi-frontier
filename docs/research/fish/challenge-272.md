# Challenge 272: "The size argument returns, correctly located"

**Claim under review** (from S32, on branch `claude/s32-multi-stroke-launch-qpq9g2`, file `docs/research/fish/S32-organism.md` §0.4 and §4):

> Zebrafish and exocoetids share f·A_pp/V_to at 0.09–0.10. They differ ONLY in lobe C_D at their Reynolds number: 0.06–0.08 at Re ~1e4 against ~0.01 at Re ~3e5, giving U_max/V_to of 0.58–0.68 versus 1.3–1.5. The barrier is a property of the TAXI, not of the single impulse S29 wrongly blamed.

Recorded evidence level: derived. Value: 0.63 U_max/V_to.

**Verdict: WEAKENED.** The arithmetic reproduces. The Reynolds-number mechanism, however, comes from one of several C_D(Re) extrapolations that are equally unanchored. Under one of the others the zebrafish taxi reaches glide speed. Under another the flying fish gets no Re advantage at all. The exocoetid cross-check that S32 cites cannot pick between the zebrafish branches, because it constrains C_D at Re ~3×10⁵, not at Re ~10⁴.

Everything below is **derived** (calculation) unless it is marked as read from a source. Nothing here is a measurement.

## Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| S32-organism.md and S32_taxi.py (branch above) | full-text | the claim, the model, and the inputs |
| Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478v1 | full-text (arXiv PDF, extracted with pdftotext this session; published JFM version not read) | foil geometry, how C_D was obtained, St range |
| Blasius laminar and Prandtl 1/7-power turbulent flat-plate friction (Cf = 1.328 Re^-½ and 0.074 Re^-⅕ per side) | textbook physical laws, not a source read this session | alternative C_D(Re) models |

## 1. Independent arithmetic

The foil-alone ceiling is U_max/V_to = (f·A_pp/V_to)·√(c₆/C_D), with c₆ = 2.55.
- √(2.55/0.08) = 5.646 and √(2.55/0.06) = 6.519. **Zebrafish: 0.095 × 5.646 = 0.536 up to 0.103 × 6.519 = 0.671.**
- √(2.55/0.011) = 15.23 and √(2.55/0.010) = 15.97. **Exocoetid: 0.087 × 15.23 = 1.325 up to 0.095 × 15.97 = 1.517.**
- S32's own §7 output gives the same pairs: 0.54, 0.58, 0.61 and 0.68 for the zebrafish; 1.31 and 1.52 for the exocoetid.
- The claim's lower bound of 0.58 drops the A_pp 8 mm case, which gives 0.54. The difference is minor.
- S32 §7 divides by V_to = 4.37 m/s, where every other section uses 4.41 m/s. This is a cosmetic inconsistency of about 1 %.

**The full model** (all drags included, `u_eq` re-run here) gives somewhat different numbers from the foil-alone ratio quoted in the claim:
- **Zebrafish:** 0.50 (central) to 0.65 (generous).
- **Exocoetid, scaled C_D:** 1.04–1.37. The 300 g fish with A_pp 2.6 cm reaches U_eq = 15.4 m/s against V_to = 16.4 m/s, so it fails to reach glide speed.
- **Exocoetid, A_pp 2.0 cm:** it fails even on the scaled branch (U_eq 11.1 m/s).

So the claimed 1.3–1.5 is foil-alone. Under the full equations the exocoetid margin is 1.04–1.37 and depends on the assumed A_pp.

## 2. The proxy: what "lobe C_D" actually is

From the Floryan 2017 full text, read this session:
- The foil is a **rigid teardrop, chord 80 mm, maximum thickness 8 mm (10 %)**, pitched about its leading edge.
- **C_D = 0.08 is a least-squares regression intercept**, fitted to data "taken at a fixed velocity of 60 mm/s" (Re 4,780). The authors write: "We will **assume** that over our range of Reynolds numbers the drag coefficient C_D is constant."
- At 120 mm/s they state that the data follow the same coefficients, "although not shown here". S32's table describes C_D as "measured at Re 4,780–9,560". It was fitted at Re 4,780, and constancy up to 9,560 is asserted rather than shown.
- **The same foil at the same Re gives C_D = 0.15 in heave and 0.08 in pitch.** So this "C_D" depends on the motion. It is a fit parameter of the oscillating-foil model, not a section drag polar.
- St tested: 0.05–0.4. The St values S32 uses (zebrafish about 0.16 at 2.9 m/s; exocoetid about 0.09 at 15 m/s) fall **inside** that range. **I found no St-extrapolation fault.**

**My inference:** in S32, the quantity that matters is the cycle-averaged residual drag of a thin, flexible, low-aspect-ratio, surface-piercing fin lobe at Re 10⁴–3×10⁵. The proxy standing in for it is the intercept of a 10 %-thick rigid teardrop foil, fully submerged and effectively 2-D, fitted at one Re. Then:
- For the zebrafish, S32 uses the proxy value almost unchanged (0.06–0.08).
- For the exocoetid, S32 extrapolates the proxy 26–42× in Re with an assumed Re^-½ law applied to the **whole** coefficient. That treats all of it as laminar skin friction.

The value of 0.08 is about twice the laminar flat-plate friction at Re 4,780 (2 × 1.328/√4780 = 0.038). So under S32's own numbers, roughly half of C_D is not laminar friction.

## 3. The hidden assumption, relaxed

I re-ran S32's own equations and inputs with only `cd_lobe` replaced, using `challenge-272_probe.py`. The zebrafish G is recalibrated from the burst with the same C_D model each time, as S32 does.

| Lobe C_D(Re) model | ZF generous U_eq/V_to | ZF central | Exo 191 g, 2.6 cm | Exo 191 g, 3.1 cm | Exo 300 g, 3.1 cm |
|---|---|---|---|---|---|
| S32 const (0.08) | 0.57 | 0.46 | 0.46 | 0.56 | 0.51 |
| **S32 scaled** (all of C_D ∝ Re^-½) | **0.65** | 0.50 | 1.04 | 1.37 | 1.23 |
| fixed form part 0.042 + laminar friction | 0.63 | 0.50 | 0.60 | 0.72 | 0.66 |
| fixed form part 0.042 + turbulent friction above Re 1e5 | 0.63 | 0.50 | 0.56 | 0.68 | 0.62 |
| thin plate, laminar friction only | **1.10** | 0.75 | 1.73 | 2.15 | 1.96 |
| thin plate, turbulent above Re 1e5 | **1.10** | 0.75 | 1.10 | 1.39 | 1.25 |

How to read the table:
- **Form-plus-friction rows.** Split C_D into a fixed form part and a friction part. Then the exocoetid ratio (0.56–0.72) overlaps the zebrafish ratio (0.50–0.65), and **C_D no longer discriminates**. Within this model family, the flying fish's taxi would then have to rest on kinematics (larger f·A_pp than assumed), which is exactly the "one escape" S32 §4.2 itself names.
- **Thin-plate rows.** Treat the lobe as a thin plate, which is closer in shape to a fin membrane than a 10 % teardrop is. Then the **zebrafish generous case reaches 1.10 V_to**, and the "barrier" disappears in that case. The last row reproduces the exocoetid taxi as well as S32's scaled branch does (1.10–1.39). So S32's exocoetid consistency argument cannot exclude it.
- **Caveat on the thin-plate rows.** Friction alone ignores pressure and separation drag on an oscillating plate, so these rows are a lower bound on C_D and an upper bound on the ceiling. They are sensitivity cases, not my estimate. Zebrafish caudal-fin thickness-to-chord ratio and the oscillating-fin residual drag at Re 10⁴: **unknown**. I did not search for a measurement of either this session.

**Inference:** the claimed discriminator holds only when (a) the zebrafish lobe keeps the drag of a thick teardrop and (b) the exocoetid lobe's drag falls as if it were entirely laminar friction. No measurement in the chain supports either choice over the others.

## 4. Is the evidence level honest?

- "Derived" is the right label for the 0.63 ratio, and S32 says plainly that it is not a measurement. **No mislabelling of the ratio.**
- **Defect (wording).** The claim states the inputs "~0.01 at Re ~3×10⁵" and "0.06–0.08 at Re ~10⁴" as though they were lobe properties. The first is an **assumed extrapolation** (S32's own table says "ASSUMED extrapolation"). The second is a proxy borrowed from a different body. The claim sentence drops both labels.
- **Defect (wording).** "Share f·A_pp/V_to at 0.09–0.10" pairs a derived zebrafish value (burst-calibrated, with assumed body Cd) with an **assumed** exocoetid A_pp (lobe 4–6 cm × sin 15°). The match is between an inference and an assumption, not an observed shared ratio. "ONLY" therefore overstates what was shown.
- **Defect (in S32's support).** The evidence that the Re dependence is real (flying fish accelerate while taxiing) is read at **search-summary** level. It discriminates only against the const branch, and only at the assumed A_pp. It is silent on the zebrafish's C_D.

## 5. Counter-examples and regimes

- **Regime the author missed:** the thin-plate (fin-like) section at the zebrafish's own Re. See §3.
- **Published taxon counter-example** (a small fish that taxis to glide speed), or measured surface-piercing fin thrust at Re ~10⁴: none found. Search scope: none run this session beyond the Floryan full text. This is **not** a negative result about the literature.
- S32 §4.2 says the escape needs A_pp ≥ 3.5 cm with C_D constant. That threshold looks inconsistent with S32's own numbers: const C_D at 3.1 cm gives U_eq 8.4 m/s, and the foil-alone formula needs f·A_pp ≥ 15/5.646 = 2.66 m/s, i.e. A_pp ≥ 5.3 cm at 50 Hz, to reach 15 m/s. My inference is that the escape would need a larger amplitude than S32 states. This does not change the verdict.

## 6. What survives

- The **ceiling structure** U_max = f·A_pp·√(c₆/C_D) follows correctly from Floryan's pitching law, in which thrust is independent of U. It is a real, useful result.
- The direction "lower C_D at higher Re raises the ceiling" is physically sound.
- The specific attribution of the zebrafish/exocoetid difference **only** to C_D(Re) is not established. With the honest C_D uncertainty, the zebrafish ceiling spans 0.46–1.10 V_to in the full model (0.50–0.65 under S32's own branches). Settling it needs the measurement S32 already names first: thrust and residual drag of an oscillating, partially immersed fin lobe at Re 10⁴–3×10⁴.

Reproduce: `git show origin/claude/s32-multi-stroke-launch-qpq9g2:docs/research/fish/S32_taxi.py > S32_taxi.py && python3 -I docs/research/fish/challenge-272_probe.py S32_taxi.py`

```swarm-challenge
{"claim_id": 272, "outcome": "weakened", "reason": "The 0.58-0.68 vs 1.3-1.5 arithmetic reproduces, but the Re discriminator rests on an assumed Re^-1/2 extrapolation of a single-Re fitted intercept for a 10%-thick rigid teardrop foil; equally unanchored form+friction or thin-plate C_D models either remove the exocoetid advantage (0.56-0.72 V_to) or let the generous zebrafish taxi reach 1.10 V_to, and the exocoetid cross-check cannot distinguish these at zebrafish Re.", "corrected_value": "zebrafish taxi ceiling 0.46-1.10 U_eq/V_to depending on unmeasured lobe C_D(Re) model (0.50-0.65 under S32's own C_D branches; foil-alone 0.54-0.67)", "depends_on": ["S32_taxi.py equations and inputs (branch claude/s32-multi-stroke-launch-qpq9g2)", "Floryan2017-foil-scaling (arXiv 1704.07478v1 full text: c6 2.55, C_D 0.08 fitted at 60 mm/s, teardrop t/c 0.10, St 0.05-0.4)", "Blasius laminar and Prandtl turbulent flat-plate friction laws", "S28 wing and V_to", "Fish1990-tables (exocoetid lobe area, wing loading)", "S32 assumed exocoetid A_pp 2.0-3.1 cm"]}
```
