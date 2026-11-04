# Challenge 132: adversarial review of claim S21-D-D-D (zebrafish true peak fast-start speed)

**Claim under review (the author's words, summarised):** S21-D-D's only way to close the gap was the assumed rise time of >=5 ms. If a muscle-power bound replaces that assumption, a stall-speed peak can only hide behind the 120 fps reading with a rise of <=1.7 ms, ~600-860 g of acceleration and >=10,900 W/kg of muscle power, which is >=23x the 461 W/kg traced ceiling. That makes the true peak <=~1.41-1.48 m/s (<=1.76 m/s at an unverified 1200 W/kg). The gap stays open, and C_L,max now sets the remaining ~2.4-4.8x margin.
Recorded evidence level: **measured**. Recorded value: n/a. Source: `harvest:s21-d-d-sensitive-input-c6ylbu`.

**Reviewer verdict: WEAKENED.** The direction of the conclusion (the gap stays open) survives everything I tried. Three things do not survive:
1. The evidence label. "Measured" is wrong.
2. The internal consistency of the acceleration, rise-time and power triple.
3. The 1200 W/kg sensitivity figure, which I could not reproduce.

## What I had to work with (scope)

- **Repository search.** I searched this repository (`grep -ri` for "S21", "fast-start", "C_L,max", "stall", "zebrafish", "461 W") and the whole git history. None of the S21 lineage documents are present. I could **not** read the harvest source, the 120 fps measured reading, the stall speed, the muscle mass fraction, or the pulse model the author used. Every check below works from the numbers stated in the claim alone. Where a check needs an unstated input, I say so.
- **Web searches (2, standard mode):**
  - "adult zebrafish fast-start escape peak velocity m/s high-speed video 1000 fps": I found **no** published adult-zebrafish fast-start peak speed measured at >=500 fps. Read-level: search-summary. One hit (PMC5394678) used 1000 fps zebrafish video, but the escapes filmed were by larvae, not adults (read-level: search-summary).
  - "Wakeling Johnston 1998 muscle power output limits fast-start performance in fish": I found Wakeling & Johnston 1998, *J Exp Biol* 201:1505-1526, doi 10.1242/jeb.201.10.1505. Read-level: abstract/search-summary. The snippet gives a mean fast-muscle power of ~142.7 W/kg at 20 °C. The species was not visible in the snippet, so I do not attribute it.
  - **Negative-search scope:** these two queries only. "No adult high-frame-rate counter-example found" means none was found in these results. It does not mean none exists.

## 1. Arithmetic, redone independently (calculated, not observed)

| Check | My calculation | Matches the claim? |
|---|---|---|
| 10,900 / 461 | 23.6 | Yes: ">=23x" holds |
| Δv implied by a·t_p (ramp) | 600 g × 1.4 ms = 8.2 m/s; 600 g × 1.7 ms = 10.0 m/s; 860 g × 1.4 ms = 11.8 m/s; 860 g × 1.7 ms = 14.3 m/s | See below |
| Mean body-mass-specific power for that rise, ½((v0+Δv)² − v0²)/t_p, with v0 = 1 m/s | 30,000-69,000 W/kg **of body**. Divided by a muscle fraction <1, that is even more W/kg of muscle | **Inconsistent** with ">=10,900 W/kg muscle" being the requirement |
| Stall speed implied by the margin, if the 2.4-4.8x margin is a force ratio (force ∝ v²) | v_stall ≈ 1.48 × √(2.4…4.8) = 2.3-3.2 m/s | — |
| Acceleration needed to rise from ~1.0-1.5 m/s to 2.3-3.2 m/s in 1.4-1.7 ms | Δv ≈ 0.8-2.2 m/s, so a ≈ 50-160 g | **Inconsistent** with 600-860 g |
| 461 → 1200 W/kg (×2.60) gives 1.48 → 1.76 m/s (×1.19) | Implied exponent v ∝ P^0.18. Kinetic-energy scaling gives P^0.5 (→ 2.39 m/s); drag-power scaling gives P^(1/3) (→ 2.04 m/s). A base-plus-excess model (v = v_base + k·P^n) reproduces 1.76 only for v_base ≈ 0.73 m/s (n = 1/3), ≈ 1.02 m/s (n = 1/2) or ≈ 1.31 m/s (n = 1) | **Not reproducible** from the stated inputs. It may be consistent with an unstated v_base. Unknown |

**What I infer from this (not stated by the author):** no single simple kinematic model I tried gives all three numbers together: rise ≤1.7 ms, 600-860 g, and ≥10,900 W/kg.
- If 600-860 g is right, the hidden peak would be ~8-14 m/s above the base. Accelerating to that needs ≥30,000 W/kg of body mass, so ≥10,900 W/kg is a loose (very conservative) lower bound.
- If the stall speed is ~2.3-3.2 m/s, as the margin suggests, then 600-860 g overstates the acceleration needed by roughly 4-10x.

Either reading still leaves the needed power far above 461 W/kg, so the conclusion stands. But the headline numbers cannot all be quoted together as they are. I could not tell which reading is right without the source (pulse shape, v_base, v_stall and muscle fraction are all unknown to me).

## 2. Proxy check

- **Centre-of-mass (COM) speed vs. the speed the lifting surface sees.** The claim bounds the fish's COM peak speed. If the "gap" is about lift on a body or fin surface reaching C_L,max at a stall speed, the quantity that matters is the local flow speed at that surface.
  - For pectoral fins or the whole body, COM speed is a fair proxy.
  - For the caudal fin, it is not. In C-starts, tail-tip speed is generally a multiple of COM speed (general fast-start kinematics; I have no zebrafish number, so the zebrafish value is unknown).
  - I could not read what surface S21 concerns, so I am flagging this as unresolved. It is not a refutation.
- **Frame-averaged reading vs. instantaneous speed.** The power bound replaces an assumed rise time, which is the right move. But the 120 fps reading may itself have been smoothed (two-frame finite differences or filtering), which widens what it can hide. The claim does not state how the reading was processed. Unknown.

## 3. Hidden assumptions, relaxed

- **No elastic power amplification.** A muscle-power ceiling binds only if no spring-and-latch mechanism stores energy and releases it faster than muscle can. Fish fast-starts are generally treated as directly muscle-powered. That is the premise of Wakeling & Johnston 1998, whose title is "muscle power output limits fast-start performance" (read-level: abstract). My inference: amplification is not a known zebrafish mechanism, so relaxing this assumption is not a realistic way to close a ≥23x shortfall.
- **The 461 W/kg ceiling.** The claim already tests 1200 W/kg (about 2.6x). The only fast-muscle figure I could reach (~143 W/kg at 20 °C, species unstated, read-level: abstract) is *below* 461 W/kg, which makes the bound more conservative, not less. Zebrafish are kept near 28 °C and muscle power rises with temperature. Even so, nothing I found approaches 10,900 W/kg.
- **Muscle mass fraction.** This is not stated. A lower fraction raises the muscle-specific power needed, which strengthens the conclusion. It cannot rescue gap closure.

## 4. Evidence level

**This is a defect.** The KEY value, "true peak ≤ ~1.41-1.48 m/s", is a **calculated upper bound**: a power ceiling combined with a kinematic model. The rise time, acceleration and 10,900 W/kg figures are also calculated. None of them is an observation. Labelling the claim "measured" with value "n/a" presents a derived result as measured. It should read **derived/calculated**. The inputs it rests on (the 120 fps reading, the 461 W/kg trace) may be measured, but the conclusion is not.

## 5. Counter-examples and regimes

- I found no published adult-zebrafish fast-start peak speed above 1.48 m/s at high frame rate (scope: the two searches above).
- Elastic-recoil fish movements do exist in other taxa. Syngnathid pivot feeding is general knowledge here; I did not search for it. It moves the head, not the whole body, so it does not apply to zebrafish COM speed.
- I am treating the larval/adult distinction as out of scope. The claim is explicitly about adults.

## Summary

- **Survives:** the qualitative result. Hiding a stall-speed peak behind the 120 fps reading needs muscle power more than an order of magnitude beyond any ceiling the claim or I could find, so the gap stays open.
- **Weakened:**
  1. The evidence level must be changed from measured to calculated.
  2. The 600-860 g / ≤1.7 ms / ≥10,900 W/kg triple is not mutually consistent under the simple ramp and kinetic-energy models I tried. Either the acceleration is overstated or the power is understated, and both errors run in the conservative direction.
  3. The 1.76 m/s at 1200 W/kg figure cannot be reproduced from the stated inputs.
  4. COM speed may be the wrong proxy if the lifting surface is the tail.

```swarm-challenge
{"claim_id": 132, "outcome": "weakened", "reason": "The gap-stays-open direction survives (the power needed stays >=23x the 461 W/kg ceiling under every model tried), but the KEY bound is a calculated value mislabelled as measured, the 600-860 g / <=1.7 ms / >=10,900 W/kg triple is internally inconsistent under simple ramp and kinetic-energy models, and the 1.76 m/s at 1200 W/kg figure cannot be reproduced from the stated inputs.", "corrected_value": "true peak <= ~1.41-1.48 m/s (evidence level: calculated upper bound, not measured)", "depends_on": ["461 W/kg traced muscle power ceiling (S21 lineage, not read by me)", "120 fps measured fastest-adult reading (value not available to me)", "assumption of no elastic power amplification in zebrafish fast-starts", "COM speed being the speed relevant to the C_L,max stall comparison", "Wakeling & Johnston 1998 J Exp Biol 201:1505 (abstract-level) for fast-muscle power magnitude"]}
```
