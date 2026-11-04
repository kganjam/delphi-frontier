# Challenge 269: the S32 taxi-stall claim

**Claim under review** (from `docs/research/fish/S32-organism.md`, branch `claude/s32-multi-stroke-launch-qpq9g2`; not written by me):

> "THE TAXI STALLS at 2.19-2.88 m/s, 50-65% of the 4.41 m/s glide speed, after ~30-38 strokes over 1.5-2 m. It does not fail to accelerate; it accelerates to a ceiling below what is needed."
> Recorded evidence level: derived. Value: 2.5 m/s stall speed.

**Verdict: WEAKENED.** The main finding survives every test I ran: the modelled taxi tops out below glide speed. Three parts of the sentence do not hold as written:

1. The stroke and distance figures describe only one scenario, and they are partly set by a stopping rule in the code.
2. "Does not fail to accelerate" depends on an input the author does not flag as a proxy.
3. The 2.19–2.88 m/s range is narrower than the source's own sensitivity table.

Everything in this document is **calculated** (my own code integrating the source's stated equations) or **read**. Nothing here is a new observation or measurement.

Reproduce with:
- `python3 -I docs/research/fish/challenge-269-scripts/indep.py`
- `python3 -I docs/research/fish/challenge-269-scripts/heave.py`

## Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| S32-organism.md and S32_taxi.py (branch `claude/s32-multi-stroke-launch-qpq9g2`) | full-text | the claim, the equations and the inputs |
| Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478v1 | full-text (arXiv v1 PDF, extracted with pdftotext; the published JFM version was not read) | the thrust law and how it was fitted |
| Web search on adult zebrafish peak escape and sprint speeds (one standard query; results from PMC/bioRxiv/JEB listings) | search-summary | whether 1.38 m/s is a sustained speed or a transient peak |
| Miln 2021 (the source of the 1.38 m/s burst, via S28) | could-not-access (not attempted; inherited via S28) | — |

## 1. Independent arithmetic

I wrote a separate integrator from S32 §1 (`indep.py`). It uses semi-implicit Euler at dt = 10 µs, not the author's RK4, and does not import their code. It uses the inputs exactly as S32 §2 states them.

| Scenario | My result (calculated) | S32's stated result |
|---|---|---|
| GENEROUS | G = 0.515 m²/s². Stalls at **2.877 m/s = 65.2 % of V_to**. The \|a\| < 1 mg stop rule fires at 0.733 s = **38.1 strokes**, x = **1.95 m** | 2.88, 0.73 s, 38 strokes, 1.95 m |
| CENTRAL | G = 0.394. Stalls at **2.192 m/s = 49.6 %**. Stop rule at 1.423 s = **74.0 strokes**, x = **2.91 m** | 2.19, 1.42 s, 74 strokes, 2.91 m |
| STINGY | Support fails at exit | Support fails at exit |

Further checks:
- **V_to.** √(2·0.25e-3·9.81 / (1.225·192e-6·1.07)) = **4.415 m/s**. This matches the claim.
- **Closed-form ceiling.** f·A_pp·√(2.55/C_D) = 1.86–2.54 m/s at C_D 0.08, and 2.17–2.96 m/s at C_D 0.059 (the scaled C_D at Re ≈ 1.7×10⁴). This brackets the integrated values.
- **The arithmetic reproduces.** I found no calculation error.

**First defect: the stroke and distance figures.** I added a "within 1 % of final speed" test to my run. In GENEROUS, the speed reaches 99 % of 2.877 m/s at **0.398 s = 20.7 strokes, x = 0.99 m**, not at 30–38 strokes over 1.5–2 m.
- 38 strokes and 1.95 m come from the script's \|a\| < 1 mg stopping threshold. An asymptotic approach has no physical "stall moment".
- 30 strokes and 1.5 m is just a row of the trajectory table.
- In CENTRAL, the 99 % point is at **45.3 strokes and 1.70 m**. The stop rule fires at 74 strokes and 2.91 m.

So "after ~30–38 strokes over 1.5–2 m" applies only to GENEROUS, and is partly set by the stopping rule. The claim pairs it with the 2.19–2.88 range, whose lower end (CENTRAL) takes 45–74 strokes and 1.7–2.9 m. The source body (§0 item 2) does restrict the stroke count to "in the generous case". The extracted claim drops that restriction.

## 2. Proxy check

**The proxy:** whole-caudal-fin cyclic thrust, calibrated by setting thrust equal to body water drag at the **1.38 m/s burst peak** (dU/dt = 0).

**The quantity that matters:** the stroke-averaged, sustainable lobe thrust at 52 Hz over 20–74 strokes.

If 1.38 m/s is the peak of a transient escape, the calibration reads an instantaneous force balance as a cycle-mean force balance. Three things make that assumption risky:
- During escapes, much of the force comes from body bending and added mass.
- The author already flags that 52 Hz is "not shown to be sustainable".
- My search-summary found adult zebrafish flume figures of **U_crit ≈ 0.40–0.55 m/s, with U_max about 15 % above U_crit**. That is roughly 0.46–0.63 m/s. I could not retrieve an adult fast-start peak speed (search-summary only).

My inference, not the author's claim: within this model, the ceiling scales almost linearly with the calibration speed, U_eq ≈ 2.1 × U_b.

| Calibration speed U_b | U_eq (Cd_body 0.3 / 0.2), calculated | Result from a 1.38 m/s exit |
|---|---|---|
| 0.46 m/s | 0.50 / 0.50 | **support fails** |
| 0.55 m/s | 0.95 / 0.71 | **decelerates** |
| 0.63 m/s | 1.11 / 0.94 | **decelerates** |
| 0.80 m/s | 1.43 / 1.23 | ≈ holds / decelerates |
| 1.00 m/s | 1.87 / 1.57 | accelerates a little |
| 1.38 m/s (S32) | 2.88 / 2.41 | accelerates |
| 1.80 m/s | 4.04 | 92 % of V_to |
| 2.00 m/s | 4.60 | **reaches V_to** |

So "It does not fail to accelerate" is true only if the escape-peak calibration stands for sustained cyclic thrust. Calibrated to sustained-swimming U_max instead, the same equations predict that the taxi **decelerates**.

That alternative makes the main conclusion (no glide) stronger, but it contradicts the sub-claim. The two calibrations disagree, and I am reporting both rather than picking one: the right one depends on the unmeasured sustained aerial-tail thrust.

## 3. Hidden assumptions, relaxed one at a time (calculated, GENEROUS otherwise)

**Thrust law choice.** In Floryan 2017 (full-text), the pitching fit (c₆ = 2.55, C_D = 0.08) and the heave fit (c₁ = 3.52, c₂ = 3.69, C_D = 0.15) were both made **at one velocity, 60 mm/s**. Separately, the authors report that dimensional thrust in pitch is independent of velocity over 60–120 mm/s, and that coefficients at other velocities are "the same". S32's description of this is accurate.

A fish tail moves with combined heave and pitch, so I recalibrated with the heave law (`heave.py`, constant C_D):

| Law | U_eq at Cd_body 0.1 / 0.2 / 0.3 |
|---|---|
| Pitch (S32's choice) | 1.81 / 2.18 / 2.50 m/s |
| Heave | 1.61 / 1.83 / 2.02 m/s |

The pitching law S32 chose is the **more favourable** of the two for the taxi. Relaxing this assumption lowers the ceiling, so the main conclusion stands.

**Body Cd in the calibration.** A higher Cd means more thrust is needed to hold the burst, which means a higher ceiling. Results:

| Cd_body | U_eq |
|---|---|
| 0.30 | 2.88 m/s |
| 0.45 | 3.51 m/s |
| 0.60 | 4.09 m/s |
| **0.69** | **4.41 m/s = V_to** |
| 0.90 | 5.17 m/s |

The claim therefore breaks if a swimming zebrafish's effective frontal-area drag coefficient is at or above ~0.69, which is 2.3× the "generous" 0.3. Some literature reports that undulating swimmers have higher drag than rigid bodies, but I did not find or read a source giving a value for this fish. Whether 0.69 is plausible is **unknown**.

**C_D extrapolation exponent.** At lobe Re ≈ 1.7×10⁴, C_D comes out as:
- 0.080 (exponent 0)
- 0.071 (exponent 0.2)
- 0.060 (exponent 0.5)
- 0.045 (exponent 1.0, a deliberately extreme value)

The ceiling scales as C_D^−½. Even at 0.045, that is only (0.06/0.045)^½ ≈ 1.15× above S32's scaled branch, about 3.3 m/s and still below V_to. The zebrafish lobe is within about 2–3× of the measured Re, so this assumption matters little here, as S32 itself says.

**Range honesty.** S32 §3.3 lists one-factor values from the author's own model that fall below 2.19:
- body Cd 0.1 → 1.89 m/s
- κ 0.5 → 1.63 m/s
- A_pp 6 mm → 1.77 m/s

The quoted 2.19–2.88 is the spread between two hand-picked scenarios (CENTRAL and GENEROUS). It is not a bound on the model. A range that reflects the source's own sensitivities is about **1.6–2.9 m/s (37–65 % of V_to)**. Under the sustained-speed calibration in §2, it reaches below the 1.38 m/s exit speed.

## 4. Evidence level

"Derived" is honest. S32 labels every trajectory as an integration of equations on stated inputs, and calls none of them a measurement. The value of 2.5 m/s sits inside 2.19–2.88. It happens to equal S32's GENEROUS constant-C_D sensitivity value (2.50), but as a summary figure it is fine.

One caveat: "the taxi stalls" is a statement about a **model**. It should read "the modelled taxi stalls". No zebrafish, robotic lobe or physical model has been observed doing this. The source says so plainly; the extracted claim sentence does not.

## 5. Missed regimes and counter-examples

- **Flying fish.** S32 itself covers them. In its model they escape the ceiling only through Re-dependent C_D. That attribution rests on assumed exocoetid kinematics, as S32 notes.
- **Ground effect over the water surface.** The wing has a span of about 31 mm at a height of a few mm, so ground effect would cut its induced drag. But wing drag is only 0.04–0.07 mN in the force budget, and the ceiling is set by lobe thrust. My inference is that this is not a route around the ceiling.
- **Searches I did not run.** I did not search for surface-piercing flapping-foil thrust measurements at Re around 10⁴. S32 names that as the deciding experiment, and I did not test it.
- **Counter-example search.** One standard web query (adult zebrafish escape speed) did not turn up a counter-example to the ceiling. It did turn up the sustained-speed figures used in §2.

## 6. Summary

- **Survives:**
  - The arithmetic, reproduced independently.
  - The qualitative finding: a speed ceiling below V_to.
  - That finding's robustness to the thrust-law choice, the C_D extrapolation and the wing drag.
- **Weakened:**
  1. "30–38 strokes over 1.5–2 m" applies only to GENEROUS, and the upper figures come from the code's stopping rule. The 99 % point is 21 strokes and 1.0 m (GENEROUS), or 45 strokes and 1.7 m (CENTRAL).
  2. "It does not fail to accelerate" depends on treating the 1.38 m/s escape peak as sustainable cyclic thrust. Calibrated to sustained U_max, the same model decelerates.
  3. The 2.19–2.88 range understates the source's own sensitivity range of about 1.6–2.9 m/s.
- **What would refute the claim outright:**
  - Sustained cyclic thrust equivalent to a burst of ≥ 1.9–2.0 m/s, or
  - An effective body Cd_body ≥ 0.69 during the burst.

```swarm-challenge
{"claim_id": 269, "outcome": "weakened", "reason": "Arithmetic reproduces and the sub-glide ceiling is robust to thrust-law choice and C_D extrapolation, but the 30-38 strokes/1.5-2 m applies only to the GENEROUS case and is partly set by the 1 mg stopping rule (99% of final speed at 21 strokes/1.0 m), the quoted 2.19-2.88 m/s range is narrower than the source's own sensitivities (~1.6-2.9 m/s), and 'does not fail to accelerate' depends on treating a 1.38 m/s escape peak as sustained cyclic thrust, since calibrating to sustained-swim Umax makes the modelled taxi decelerate.",
  "corrected_value": "modelled ceiling ~1.6-2.9 m/s (37-65% of 4.41 m/s); 99% of ceiling after ~21-45 strokes, ~1.0-1.7 m; below the 1.38 m/s exit if thrust is calibrated to sustained U_max",
  "depends_on": ["S32-organism.md equations and inputs (branch claude/s32-multi-stroke-launch-qpq9g2)", "Floryan2017-foil-scaling (arXiv 1704.07478v1, full-text)", "Miln2021-burst 1.38 m/s via S28", "S28 wing case C (192 mm2, AR5, CLmax 1.07) for V_to 4.41 m/s", "S29 body Cd 0.1-0.3", "adult zebrafish Ucrit 0.40-0.55 m/s and Umax ~15% above Ucrit (search-summary only)", "Kyriakatos2011-52Hz via S24"]}
```
