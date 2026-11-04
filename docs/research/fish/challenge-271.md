# Challenge 271: the foil-ceiling formula U_max = f·A_pp·√(c₆/C_D(Re))

**Claim under review** (author: S32-organism.md, on branch `claude/s32-multi-stroke-launch-qpq9g2`; not written by me):
> "THE CEILING HAS A CLEAN FORM: U_max = f·A_pp·√(c₆/C_D(Re)). Measured foil thrust scales with tail speed squared INDEPENDENT of forward speed while foil drag scales as U², so immersed area and mass DROP OUT. Only tail speed and lobe drag at Reynolds number matter."
> Recorded evidence level: derived.

**Verdict: WEAKENED.** The algebra is correct and the source is quoted correctly. But the formula is a bound on the foil alone, and the claim presents it as the taxi ceiling. The words "immersed area and mass drop out" and "only tail speed and lobe drag at Re matter" do not survive. The author's own sensitivity table contradicts them. The primary source restricts the regime where the law applies, and the claim needs it outside that regime.

## Sources and read-levels

| Source | Read-level | Use |
|---|---|---|
| Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.* 822:386–397, arXiv 1704.07478v1 | **full-text** (arXiv v1 PDF, downloaded and read this session; I did not read the published JFM version) | Thrust law, coefficients, tested ranges |
| S32-organism.md (the author's document) | **full-text** | The claim, the author's inputs, the author's sensitivity table §3.3 |
| Ehrenstein & Eloy 2013, *J. Fluid Mech.* (skin friction on a laterally moving wall, "Bone–Lighthill" boundary-layer thinning) | **could-not-access**. I did not fetch it this session; it is cited from prior knowledge and its details are unverified | Raised only as a lead. **No part of the verdict rests on it** |

## 1. Independent arithmetic

I started from Floryan's definitions (§2, arXiv v1): St = 2fA/U∞ where A is the trailing-edge *half*-amplitude, so 2A = A_pp. C_T = F_x/(½ρU∞²sc). For pitching, eq. 2.7 gives C_T = c₆St² + c₇St·A* − C_Dp, with **c₆ = 2.55, c₇ = 0, C_Dp = 0.08** (§5). These match the author's inputs.

The net streamwise force on the foil alone is
F_x = ½ρ·s·c·[c₆(f·A_pp)² − C_D·U²].
It is zero at **U₀ = f·A_pp·√(c₆/C_D)**. The area s·c is a common factor and cancels from U₀. This **matches the author's formula.**

Numbers, computed by me (calculated, not observed):
- √(2.55/0.08) = **5.646**, so U₀ = 5.65·f·A_pp when C_D is held constant.
- Zebrafish, f·A_pp = 0.33–0.45 m/s (the author's burst calibration): U₀ = **1.86–2.54 m/s**. Dividing by V_to = 4.41 m/s gives 0.42–0.58. The author's 0.58–0.68 uses the Re-scaled C_D, which is consistent.
- Exocoetid, 50 Hz × 2.6 cm = 1.3 m/s: U₀ = **7.34 m/s** with constant C_D. With C_D = 0.0105 (scaled) it is 20.3 m/s, or 1.35·V_to at 15 m/s. Both match the author's "7–9 m/s" and "1.31–1.52".
- St at the ceiling = √(C_D/c₆) = **0.177** (constant C_D) and **0.064** (C_D = 0.0105). Both lie inside Floryan's tested St range of 0.05–0.40.
- I checked the author's thrust calibration. G = C_D·U² + D_body/(½ρS_fin) at U = 1.38 m/s, with Cd_body 0.1–0.3 on 24 mm² and S_fin = 37.8 mm². That gives 0.152 + (0.121–0.363) = **0.27–0.52 m²/s²**, which matches.

**No arithmetic error found.**

## 2. Proxy check

U₀ is where the *foil's own* net force is zero. That is a proxy. The quantity that matters is **U_eq**, the speed at which the *whole animal's* horizontal forces balance. That balance includes wing drag, body air drag, the lobe's induced drag from carrying weight, and contact-line drag. These are the author's own equations in §1. U₀ is therefore an **upper bound** on U_eq, not the ceiling itself.

Mass and immersed area enter U_eq. Lobe induced drag goes as W²/(ρU²·S_imm·AR_eff), and the meniscus terms go as σc against W. The author's own one-at-a-time sweep (§3.3) shows this:
- φ = 0.25 → U_eq 2.46 m/s, and φ = 1.0 → 2.88 m/s. That is a **15 % effect of immersed area**.
- Δcosθ 0 → 0.3 lowers U_eq from 2.88 to 2.78 m/s.

So "immersed area and mass DROP OUT" is true of U₀ and **false of the ceiling the animal experiences**. The author's own simulation is the evidence. (This is my inference from the author's table; I did not rerun the author's script.)

## 3. Hidden assumptions, relaxed

**(a) κ is missing from the "clean form".** The author's own equation of motion uses G = κ·c₆·(f·A_pp)². The ceiling is therefore U₀ = f·A_pp·√(κc₆/C_D). The author lists κ (3-D, free-surface, flexibility and ventilation effects) as unknown and as a weakest link. At κ = 0.5, U₀ falls by a factor of √0.5 = 0.71. The author's table shows 2.60 → 1.63 m/s at κ 1 → 0.5. A form that drops κ is clean only because it leaves out an unknown of first-order size.

Caveat in the author's favour, which is my inference: for the zebrafish, G is calibrated in water from the burst. So c₆ and the in-water κ are absorbed into G, and U₀ = √(G/C_D). What is still unknown is how κ changes between full immersion and a surface-piercing lobe in air.

**(b) Pitch law versus heave law.** U-independent thrust holds for **pitching only**. Floryan state this outright: "for pitching motions the dimensional thrust should be independent of the freestream velocity", and the heaving thrust "only weakly depends on freestream velocity" (§6, Fig. 8). The heave law is C_T = St²(c₁ + c₂f*U*) − C_Dh, with c₁ 3.52, c₂ 3.69, C_Dh 0.15. Its thrust depends on U through f* = fc/U.

A caudal lobe moves by both heave and pitch. I solved the heave-law ceiling by fixed-point iteration (calculated):

| Case | f·A_pp (m/s) | Pitch law U₀ | Heave law U₀ | Heave/f·A_pp |
|---|---|---|---|---|
| Zebrafish, 52 Hz, c 6 mm | 0.45 | 2.54 | **2.31** | 5.13 |
| Zebrafish | 0.33 | 1.86 | **1.72** | 5.22 |
| Exocoetid, 50 Hz, c 2.5 cm, C_D const | 1.30 | 7.34 | **6.80** | 5.23 |

Under the heave law, U₀ is about 8–9 % lower, and it depends weakly on chord and U through f*. That is a moderate change, not a reversal. It does show that "independent of forward speed" belongs to one idealised motion, not to fish lobes in general.

Floryan also warn: "The values of the constants should not be taken to be universal; they are simply the values that work best for our data" (§4, and repeated in §5). The coefficient ratio is c/C_D = 31.9 for pitch and 23.5 for heave. That difference shows how much the ratio depends on the foil and the motion.

**(c) Amplitude is outside the tested range. This is the largest extrapolation, and the claim does not mention it.** Floryan tested pitch θ₀ = 3–15°, so A* = A/c = **0.052–0.26**. The author's inputs give:
- zebrafish: A_pp 6.3–8.6 mm on a 6 mm chord → A* = **0.53–0.72** (θ₀-equivalent 32–46°);
- exocoetid: A_pp 2.0–3.1 cm on a 2.5 cm chord → A* = **0.40–0.62**.

That is 1.5–2.8× beyond the largest amplitude measured. The St² law (c₇ = 0, with thrust coming only from added mass) is shown only for small pitching motions, and §2 of the paper says "small pitching motions". Large-amplitude separation could change both c₆ and the drag offset. I have no measurement of their direction or size, so the effect is **unknown**.

**(d) U-independence of thrust is measured only over a 2× range.** Floryan's check is U∞ = 60–120 mm/s, shown in Fig. 8a at θ₀ = 7° only. The claim applies it from 1.38 to about 3 m/s (zebrafish) and from 10 to 20 m/s (exocoetid).

**(e) C_D(Re) is assumed, not measured, and the primary source points the other way inside its own range.** Floryan *assume* C_D "constant, independent of the amplitude or frequency" over their Re range. They report that data at 60–120 mm/s (Re 4,780–9,560) follow the laws "with the same values for the coefficients", but this is "not shown here". If the drag offset scaled as Re^−½, as in the author's "scaled" branch, it would fall by **29 %** across that 2× span. The paper reports no such change.

This is weak counter-evidence, since the data are not shown and the force-sensor resolution limits what could be seen. Even so, it is the only Re-varying data in the source. The C_D(Re) dependence, which the claim names as the discriminating variable, is therefore an **assumption**. Inside the measured span the source reports it as flat.

**(f) Other drag terms on a surface-piercing lobe.** A piercing lobe has wave, spray and ventilation drag, which depend on Froude number and ventilation, not only on Re. The author lists these as "not modelled" and folds them into κ. So "only tail speed and lobe drag at Re matter" is contradicted by the author's own §1 list of omissions.

## 4. Evidence level

"Derived" is the honest label for the formula. It follows algebraically from a measured fit.

The claim sentence still mixes in two things that are not measured:
- "Measured foil thrust ... INDEPENDENT of forward speed": the measurement covers a rigid 2-D teardrop foil in pure pitch, at θ₀ = 7°, over U 60–120 mm/s.
- "lobe drag at Reynolds number": the Re dependence is an **assumed** extrapolation. The author labels it so in S32 §2, but the claim sentence does not carry that label.

This is a scope defect, not a mislabelled number.

## 5. Regimes and counter-examples the author missed

- The **same paper's heave law**: thrust depends weakly on U, C_D 0.15, ceiling about 8–9 % lower (see 3b).
- **Amplitude** beyond the tested A* in both taxa (see 3c). It is not raised in the claim.
- **Drag on an oscillating surface that depends on amplitude.** Literature on Bone–Lighthill boundary-layer thinning (Ehrenstein & Eloy 2013; **could-not-access**, unverified) suggests that friction drag on a laterally moving surface rises with lateral speed. If so, C_D would depend on St and not only on Re. This is a **lead only**, and the verdict does not depend on it.
- **Negative search scope.** I did not search for combined heave–pitch scaling laws, or for surface-piercing foil thrust data, this session. Measured exocoetid lobe kinematics were also not found, as in S32.

## 6. What survives

- U₀ = f·A_pp·√(c₆/C_D) is a correct, derived **upper bound** on the taxi speed set by the foil alone, under Floryan's small-amplitude pitching law.
- For the zebrafish its value is 1.86–2.54 m/s with constant C_D (calculated).
- The broader S32 conclusion depends on a different question: whether the true U_eq stays below V_to. Every relaxation above lowers U₀ or leaves its sign unknown: κ < 1, the heave law, and the extra drag terms. So the zebrafish "stall short of glide speed" conclusion is not weakened by this review.
- What is weakened is the claimed **mechanism**: "only tail speed and C_D(Re)", with C_D(Re) as the exocoetid discriminator. It relies on an assumed Re^−½ drag offset applied 26–42× outside the measured Re span, and on amplitudes 1.5–2.8× outside the tested range.

**Corrected statement:** U_eq ≤ U₀ = f·A_pp·√(κ·c₆/C_D). This is derived from a pitching law measured at A* ≤ 0.26 and Re 4,780–9,560. Immersed area and mass cancel from U₀ only, not from U_eq (about 15 % effect of φ in the author's own sweep). κ, the motion type (heave gives about 8–9 % lower U₀) and the Re dependence of C_D are unmeasured for a fish lobe.

```swarm-challenge
{"claim_id": 271, "outcome": "weakened", "reason": "The algebra is correct, but U_max is only the foil-alone zero-thrust bound: it omits the unknown κ, immersed area and mass re-enter the true equilibrium (about 15% per the author's own φ sweep), U-independent thrust is measured only for small-amplitude pitch (A* ≤ 0.26 against 0.40–0.72 used), and C_D(Re) is an assumed extrapolation that the source reports flat across its own 2× Re range.", "corrected_value": "U_eq ≤ f·A_pp·√(κ·c6/C_D); = 5.65·f·A_pp for pitch with κ=1 and C_D=0.08 (1.86–2.54 m/s zebrafish), ≈5.1–5.2·f·A_pp under the same paper's heave law", "depends_on": ["Floryan et al. 2017 arXiv 1704.07478v1 pitch law c6=2.55, c7=0, C_Dp=0.08 and tested ranges θ0 3–15°, St 0.05–0.4, U 60–120 mm/s (full-text)", "Floryan et al. 2017 heave law c1=3.52, c2=3.69, C_Dh=0.15 (full-text)", "S32 author inputs: f·A_pp 0.33–0.45 m/s, chord 6 mm, A_pp 6.3–8.6 mm, exocoetid A_pp 2.0–3.1 cm and chord 2.5 cm", "S32 §3.3 sensitivity table (φ 0.25→2.46, 1.0→2.88 m/s; κ 0.5→1.63 m/s), not rerun by me"]}
```
