# Challenge 271: the "clean form" of the airborne-taxi foil ceiling

**Claim under review** (S32-organism.md, on branch `claude/s32-multi-stroke-launch-qpq9g2`, read in full):

> THE CEILING HAS A CLEAN FORM: U_max = f·A_pp·√(c₆/C_D(Re)). Measured foil thrust scales with tail speed squared INDEPENDENT of forward speed while foil drag scales as U², so immersed area and mass DROP OUT. Only tail speed and lobe drag at Reynolds number matter.

Recorded evidence level: derived. **Verdict: WEAKENED.** The algebra is correct and the numbers reproduce. But the form holds only for the pure-pitching law. Its "C_D(Re)" is a regression intercept that depends on the type of motion, and nobody has measured it as a function of Re. The claim also drops the author's own κ, and the zebrafish kinematics lie outside the amplitude range Floryan measured. So "only tail speed and lobe drag at Re matter" is too strong. The S32 conclusion, that the taxi stalls below glide speed, is **not** overturned by any of this (§5).

## Sources and read levels

- Floryan, Van Buren, Rowley & Smits 2017, "Scaling the propulsive performance of heaving and pitching foils", arXiv 1704.07478v1: **full-text** (arXiv v1, downloaded and read this session; the published JFM version was not read).
- S32-organism.md: **full-text** (project document).
- No other literature was read. Every statement below about 3-D, free-surface or low-aspect-ratio effects is **my inference** and carries no number.

## 1. Independent arithmetic

My script is at `/tmp/claude-0/scripts/c271.py` (scratch, not committed). It uses S32's stated inputs: a 37.8 mm² fin, 6 mm chord, 52 Hz, a 1.38 m/s burst, 24 mm² frontal area, and body Cd 0.1–0.3.

- **Definitions checked against the full text.** Floryan defines St = 2fA/U∞, where A is the trailing-edge *amplitude* (h₀ or c·sinθ₀). So St = f·A_pp/U, and the claim's use of A_pp is correct.
- **The form follows.** Pitching gives C_T = c₆St² + c₇StA* − C_Dp, with c₆ = 2.55, c₇ = 0 and C_Dp = 0.08 (Floryan §5). Then F_x = ½ρsc[c₆(fA_pp)² − C_Dp U²], and F_x = 0 at U = fA_pp√(c₆/C_Dp). Span·chord multiplies both terms, so the foil's own area cancels. **Confirmed (derived).**
- **Calibration (calculated).** G = 0.273 / 0.394 / 0.515 m²/s² gives f·A_pp = 0.327 / 0.393 / 0.449 m/s, i.e. A_pp = 6.3 / 7.6 / 8.6 mm. This matches S32's 0.27–0.52 and 0.33–0.45.
- **Foil-only ceiling (calculated).**
  - C_D held at 0.08: U_max = 1.85 / 2.22 / 2.54 m/s.
  - S32's Re^−½ extrapolation: U_max = 1.94 / 2.48 / 2.96 m/s.
  - These bracket S32's integrated stall of 2.19–2.88 m/s, so the arithmetic is sound.

## 2. Proxy: "lobe drag at Reynolds number" is not what the formula contains

In the formula, C_D is **the intercept of a least-squares fit** of C_T against St², taken at one speed (60 mm/s). Floryan states: "We will assume that over our range of Reynolds numbers the drag coefficient C_D is constant." Two facts in the same paper show that the intercept is not a foil-drag property set by Re:

1. **The same foil at the same Re gives C_Dh = 0.15 in heave and C_Dp = 0.08 in pitch** (Floryan §4, §5; measured). The intercept changes by about 1.9× with the type of motion alone.
2. **No dependence on Re is measured.** Floryan's data hold C_D *constant* across 60–120 mm/s (Re 4,780–9,560). The "(Re)" in the claim, and the Re^−½ law S32 uses outside that span, are **assumed** (S32's own table says "ASSUMED extrapolation"). A laminar Re^−½ law would predict about a 29 % fall across Floryan's own 2× span. The paper reports the coefficients as "the same" there. That is **my inference** and weak evidence: they report no error bar on the intercept.

The intercept is small next to the instrument. At 60 mm/s, C_Dp = 0.08 corresponds to **3.2 mN**, and C_Dh to 6.0 mN (my calculation from ½ρU²sc). Floryan quotes the x-force resolution as 5 mN. Averaging over 20 cycles and at least 6 repeats reduces the noise on a mean, but the quantity the ceiling depends on as C_D^−½ is a fitted offset at about the level of the sensor's resolution.

**The right quantity** is the time-averaged streamwise force offset of the *actual* lobe, with its actual motion, shape (thin fin rays, not a 10 %-thick teardrop), aspect ratio and free surface. It is `unknown`: S32 found no measurement, and I searched for none beyond Floryan.

The ceiling is sensitive to it (calculated, with calibration redone at each C_D, body Cd 0.3):

| C_D | U_max |
|---|---|
| 0.15 | 2.08 m/s |
| 0.08 | 2.54 m/s |
| 0.04 | 3.31 m/s |
| 0.02 | 4.48 m/s |

At C_D 0.02 the ceiling would exceed V_to = 4.41 m/s.

## 3. The hidden assumptions, relaxed one at a time

**(a) U-independent thrust is a pure-pitching result, not a general foil law.**

- Floryan §6: dimensional thrust is independent of U "for pitching motions, and only weakly depends on freestream velocity for heaving motions". Fig. 8a, the velocity test, is pitching at **one amplitude, θ₀ = 7°**.
- The heave law is C_T = c₁St² + c₂St²f*U* − C_Dh, with c₁ 3.52, c₂ 3.69, C_Dh 0.15. Its second term gives dimensional thrust ∝ (fA_pp)²·fc/U, so **U does not drop out**. The ceiling then becomes the root of a cubic and depends on f and c separately, not on f·A_pp alone.
- Applying the heave law through the same calibration route (calculated): f·A_pp = 0.31–0.40 m/s, and the ceiling is **1.63–2.04 m/s** with C_D const, or **1.64–2.21 m/s** scaled. That is *lower* than the pitch form.
- A fish caudal lobe on the end of an undulating body combines heave and pitch. Floryan does not test combined motion; no combined-motion data were read.
- So the clean form describes one idealisation. It is not a measured property of fish tails.

**(b) The measured range of amplitudes is exceeded about 2–3×.**

- Floryan measured θ₀ = 3–15°, i.e. A* = A/c ≤ 0.26.
- S32's calibrated zebrafish lobe has A* = 0.52–0.72. As a rigid pitching foil that is θ₀ = **32–46°** (calculated).
- The St at the ceiling, 0.15–0.17, and f*, 0.10–0.16, are inside or at the edge of the measured span. Only the largest measured amplitude reaches f* ≈ 0.1.
- The St² law is derived "for small pitching motions" (Floryan §2.1–2.2). Its added-mass terms carry cosθ/sinθ factors that the small-angle scaling ignores.
- The law is therefore extrapolated in amplitude precisely where the ceiling is evaluated. The direction of the error is `unknown`.

**(c) κ is dropped.**

- S32's own equation is G = κ·c₆(fA_pp)². The ceiling is therefore U_max = fA_pp√(κc₆/C_D), not the claimed form.
- S32's sensitivity table reports κ = 0.5 lowering U_eq from 2.60 to 1.63 m/s.
- So "only tail speed and lobe drag matter" contradicts the author's own model. κ (3-D, ventilation, flexibility) is a third factor of the same rank.

**(d) "Immersed area drops out" is true only of the foil-only bound.**

- In the integrated equilibrium, wing drag, lobe induced drag and the meniscus terms do not scale with S_imm. S32's own sensitivity table gives **φ 0.25 → 2.46 m/s against φ 1.0 → 2.88 m/s**.
- More importantly, the tail speed in S32 is not measured. It is *inferred* by dividing body drag by an **assumed** 37.8 mm² fin area. That area re-enters through the calibration (calculated, body Cd 0.3, C_D const):

| Fin area | U_max |
|---|---|
| ×0.5 | 3.31 m/s |
| ×1 | 2.54 m/s |
| ×2 | 2.04 m/s |

- Area cancels from the formula only once f·A_pp is known independently. For the zebrafish it is not.
- **Mass** does drop out of U_max: it appears in neither term. That part of the claim survives. It still enters U_max/V_to through V_to.

## 4. Evidence level

- "derived" is honest for the formula.
- Calling the law "measured" is honest for c₆ = 2.55 and C_Dp = 0.08 at Re 4,780–9,560, A* ≤ 0.26, pure pitch, on a 2-D rigid teardrop.
- Calling it "measured" is **not** honest for:
  - "C_D(Re)", which is assumed;
  - U-independence as a property of fish lobes, which is measured for pitch only, at one amplitude, over 2× in U.

The claim sentence blurs this line. S32's body table keeps it clean.

## 5. Regimes, counter-examples, and what does *not* change

- **Not covered by the measurement, and not quantified:** surface-piercing operation (free-surface waves, spray, ventilation); a very low effective aspect ratio for a few-mm immersed lobe; fin flexibility. These are **my inferences** and come with no number.
  - Spray and wave drag do not scale with S_imm and depend on Froude number. If present, they break both the area cancellation and the pure C_D U² drag form.
  - No published measurement of surface-piercing oscillating-foil thrust was read (none was searched beyond Floryan this session).
- **No published counter-example** to the stall conclusion was found. The search was limited to Floryan full text plus S32's own source list.
- **What survives:**
  - Within the pure-pitch idealisation, the ceiling is the stated closed form.
  - Every relaxation I tested lowers the zebrafish ceiling, except the two assumed inputs whose values are unknown: a lower C_D (§2) and a smaller fin area (§3d). Heave law: 1.6–2.2 m/s. κ < 1: lower.
  - So the S32 conclusion (stall below V_to) is not refuted here. What is refuted is the claim that the ceiling is *cleanly* fixed by tail speed and Re-set drag alone.

## Corrected statement

For a rigid foil in **pure pitch**, within Floryan's measured span (A* ≤ 0.26, St 0.05–0.4, Re 4.8–9.6×10³), the foil-only ceiling is U_max = f·A_pp·√(κ·c₆/C_Dp). Here C_Dp is a motion-dependent fit intercept (0.08 in pitch, 0.15 in heave for the same foil), and its Re dependence is unmeasured. For S32's zebrafish inputs this gives **1.85–2.96 m/s** (calculated, κ = 1). The heave law has no clean form and gives **1.6–2.2 m/s** (calculated). Immersed fraction cancels from the bound but not from the integrated stall. Fin area re-enters through the tail-speed calibration.

```swarm-challenge
{"claim_id": 271, "outcome": "weakened", "reason": "The closed form is algebraically right and reproduces (foil-only U_max 1.85-2.96 m/s) but holds only for Floryan's pure-pitch law at A*<=0.26; it omits the author's own kappa, its C_D is a motion-dependent fit intercept (0.08 pitch vs 0.15 heave, same foil and Re) whose Re-dependence is assumed, heave thrust is not U-independent, and fin area re-enters via the tail-speed calibration, so 'only tail speed and Re-set lobe drag matter' overstates it.", "corrected_value": "U_max = f*A_pp*sqrt(kappa*c6/C_Dp), pure pitch only: 1.85-2.96 m/s for S32 zebrafish inputs (calculated, kappa=1); heave law (no clean form) 1.6-2.2 m/s", "depends_on": ["Floryan2017-foil-scaling (arXiv 1704.07478v1, full text: St=2fA/U, c6=2.55, C_Dp=0.08, C_Dh=0.15, c1=3.52, c2=3.69, theta0 3-15 deg, 60-120 mm/s, 5 mN resolution)", "S32 calibration inputs: fin area 37.8 mm2 (assumed), chord 6 mm, 52 Hz, 1.38 m/s burst, body Cd 0.1-0.3 on 24 mm2", "S32 sensitivity table (phi and kappa rows)", "S32 Re^-1/2 C_D extrapolation (assumed)"]}
```
