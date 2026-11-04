# Challenge 268: "THRUST PASSES" (S32, multi-stroke taxi launch)

**Claim under review (not written by me):**
"THRUST PASSES: leaving the water cuts body drag by 816x -- exactly the water/air density ratio, 1000/1.225 -- from 4.6 mN to 8 uN, and burst-calibrated lobe thrust (1.1-3.4 mN) exceeds total drag 3-40x. Speed genuinely rises, doubling in ~10 strokes at 52 Hz."
Recorded evidence level: derived. Recorded value: 816-fold drag reduction.

**Verdict: WEAKENED.** The qualitative result survives: in the model, thrust exceeds drag at exit speed and speed rises. But the headline number is internally inconsistent. The two endpoints the claim quotes are 544-fold apart, not 816-fold. And body drag is the wrong quantity to quote for "what leaving the water buys".

**Every number in this note is calculated, not observed.** It comes from my own arithmetic on the stated inputs, or from re-running the author's script. No measurement was made.

## Sources and read levels

| Source | Read level |
|---|---|
| `docs/research/fish/S32-organism.md` on branch `origin/claude/s32-multi-stroke-launch-qpq9g2` | full-text (§0–3 read in full, rest skimmed) |
| `docs/research/fish/S32_taxi.py` on the same branch | full-text of the relevant lines. I also re-ran it with `python3 -I` (exit 0) |
| Floryan et al. 2017 (thrust law), Kyriakatos 2011 (52 Hz), Soares & Bierman 2013 (guppy) | could-not-access this session. I did not open them, and I rely on S32's own read-level statements for them |

## 1. Independent arithmetic

Inputs: ρ_w = 1000, ρ_a = 1.225 kg/m³, U = 1.38 m/s, frontal area A = 24 mm².

- Density ratio: 1000/1.225 = **816.3**. Correct.
- Body drag in water at Cd 0.2: ½·1000·0.2·24e-6·1.38² = **4.57 mN**. Correct.
- Body drag in air at the **same** Cd 0.2: **5.6 µN**. Only this pairing gives the 816× ratio.
- The claim's "8 µN" is **8.40 µN**. The script computes it with **Cd 0.3** in air (`S32_taxi.py` line 138: `D_air = 0.5 * RHO_A * 0.3 * ...`).
- So the claim's own endpoints give 4.57 mN / 8.40 µN = **544×**, not 816×.
- **The sentence "816x … from 4.6 mN to 8 uN" is arithmetically self-contradictory.** It mixes Cd 0.2 in water with Cd 0.3 in air, and then reports the equal-Cd ratio. This is an inference from the script's line 138 and the doc's table row "4.57 mN in water (Cd 0.2) vs 8.4 µN in air … ρ_w/ρ_a = 816".

"Exactly the density ratio" holds only when Cd is the same in both media. Section 3 explains why it is not.

**Thrust / total drag at 1.38 m/s.** I recomputed the ratios from the script's printed force terms (T_lobe ÷ [D_wing + D_ind,lobe + F_σ,h + D_body,air]):
- GENEROUS: 3.428 / 0.0974 = **35×**
- CENTRAL: 1.143 / 0.430 = **2.7×**
- So "3–40×" is really **2.7–35×**. That is minor rounding on both ends, and the direction is right.
- **STINGY** (S32's own third case): thrust 0.29 mN against 3.73 mN of drag. Net is **−3.46 mN** and lobe support fails at exit.
- The claim as recorded drops the source's qualifier "in the generous and central cases". As recorded, it is unconditional, and the source's own lower bound contradicts it.

**Doubling in ~10 strokes.** Script output, GENEROUS case:
- Stroke 10: U = 2.639 m/s, which is **1.91×**.
- Doubling (2.76 m/s) falls between stroke 10 and stroke 20 (2.844 m/s).
- In **CENTRAL** the speed **never doubles**: equilibrium is 2.19 m/s, which is 1.59× the exit speed.
- So "doubling in ~10 strokes" is a GENEROUS-only, slightly optimistic statement. "Speed genuinely rises" holds for both GENEROUS and CENTRAL, and fails for STINGY.

## 2. Proxy check

**Proxy used:** body drag (water → air).

**Quantity that matters:** the total resistance the immersed lobe must beat. That is wing drag, plus induced drag of the lobe carrying weight, plus contact-line drag, plus body air drag. It should be compared with the water drag the same thrust balanced at the burst peak.

- After exit, body air drag is **< 10 %** of total resistance in both passing cases (8.4 µN of 97 µN and of 430 µN).
- The real resistance drop is:
  - GENEROUS: 6.86 mN (Cd 0.3, the Cd used to calibrate G in that case) → 0.097 mN = **~70×**
  - CENTRAL: 4.57 mN (Cd 0.2) → 0.43 mN = **~11×**
- The 816× figure overstates the relief by 1–2 orders of magnitude. The new drag source is weight support by the lobe, and the claim's framing hides it.
- The author's conclusion depends on this ~11–70× figure, not on 816×. That is my inference from the force table.

## 3. Hidden assumptions, relaxed

**a) Cd unchanged across media (needed for "exactly the density ratio").**
- Body Reynolds number at 1.38 m/s, taking SL ≈ 31 mm (inferred from S32's "12–19 mm = 0.4–0.6 SL"):
  - water ≈ 4.3×10⁴ (ν = 1.0e-6 m²/s)
  - air ≈ 2.9×10³ (ν ≈ 1.5e-5 m²/s, a standard property value)
- That is a 15× fall in Re. At these Re a streamlined body's Cd rises as Re falls; laminar friction scales as Re^−½, which gives ~3.9× for a 15× fall.
- So the true drag-cut factor is **below 816×**, plausibly a few hundred. I have no measured air Cd for a zebrafish body; it is `unknown`.
- The author partly allowed for this by using Cd 0.3 in air, but then quoted the equal-Cd ratio anyway.
- **This does not change the conclusion.** Body air drag is negligible at any plausible Cd. Even Cd ≈ 1 gives ~28 µN, still < 3 % of GENEROUS thrust.

**b) Density values.** 1000/1.225 is the 4 °C water / ISA sea-level air convention. At 28 °C, a typical zebrafish husbandry temperature, ρ_w ≈ 996 and ρ_a ≈ 1.17 kg/m³ (ideal gas, 1 atm), so the ratio is ≈ **850**. "Exactly" is a convention, not a physical constant. This is immaterial.

**c) Burst-calibrated thrust carries over to a surface-piercing lobe on an airborne body.**
This assumption carries the result. G is set so that whole-fin thrust equals body water drag at the burst peak. That gives 1.1–3.4 mN, and the claim attributes it to the lobe in air. Three things can break the carry-over:
- **(i) The thrust law is for a fully submerged rigid 2-D foil.** The lobe pierces the free surface. Its Froude number is U/√(g·d) ≈ 1.38/√(9.81·~0.005) ≈ 6, using a depth of a few mm (my estimate). That is a regime where surface-piercing foils are prone to ventilation. S32 folds this into κ < 1 but does not quantify it. The magnitude is `unknown`; I found no measured ventilation-loss figure for a fish-scale lobe in this session (I did not run a literature search).
- **(ii) Yaw recoil.** An airborne body has no water to push against for lateral reaction. S32 lists this as not modelled and of adverse sign.
- **(iii) Calibration attributes all burst thrust to the tail.** S32 itself calls this generous.

How far can the thrust fall before the claim fails? Holding drag terms fixed (a crude test; drag also changes with U and support):
- GENEROUS still passes at 1.38 m/s until thrust falls ~35×.
- CENTRAL fails if thrust falls **~2.7×**, i.e. at κ ≈ 0.37.

So "thrust passes" is robust only in the GENEROUS case. In CENTRAL it rests on κ staying above ~0.4, which no measurement in S32 supports or refutes.

**d) 52 Hz held for ≥10 strokes.** 52 Hz is an EMG escape maximum. S32 states it was not shown to be sustainable. "Doubling in ~10 strokes at 52 Hz" assumes 10+ consecutive maximal beats, about 0.2 s. If the tail beats slower, doubling takes longer in wall-clock time. The per-stroke picture is roughly unchanged only if amplitude scales so that f·A holds, and it may not.

## 4. Evidence level

- "derived" is the honest label. S32 says so and nothing is presented as measured. **Pass.**
- One defect: the source line says "density ratio verified here". The density ratio was verified. The **drag reduction** it is offered for was not, and on the claim's own numbers it is 544×.
- The recorded value ("816 fold drag reduction") is therefore a derived number that does not follow from its own inputs.

## 5. Regimes and counter-examples

- **Same source, own counter-case.** S32's STINGY case: thrust fails and support fails at exit. The claim's unconditional "thrust passes" is contradicted within S32.
- **Same source, low exit speed.** From 0.45 m/s, every case fails on weight support (S32 §3.1). "Leaving the water" helps only if exit speed is already high.
- **Supporting, not counter.** The guppy gains 1.02 → 1.24 m/s in air while beating its tail (Soares & Bierman 2013, via S24, which S32 quotes). Flying fish accelerate during taxiing (secondary only, per S32). Both agree in sign with "speed rises". I did not read either primary source here.
- **Negative search scope.** I searched for no published counter-example outside the repository. My review covered only S32's text, its script, and first-principles checks. A literature counter-example is therefore not excluded. It is `unknown`.

## Corrected statement

On S32's own derived model, leaving the water at 1.38 m/s:
- Body drag falls from 4.57 mN (Cd 0.2, water) to 8.4 µN (Cd 0.3, air). That is **544×**, not 816×; 816× holds only at equal Cd, and a 15× drop in Re argues against equal Cd.
- Total resistance falls only **~11–70×**, because supporting the weight on the lobe adds induced drag.
- Burst-calibrated thrust (1.1–3.4 mN) exceeds the total by **2.7–35×** in the GENEROUS and CENTRAL cases. It **fails** in STINGY.
- Speed rises in GENEROUS and CENTRAL. It reaches **1.9× by stroke 10** in GENEROUS only, and never doubles in CENTRAL.
- All of this assumes submerged-foil thrust carries over to a surface-piercing lobe on an airborne body. That assumption is untested and decisive for CENTRAL.

```swarm-challenge
{"claim_id": 268, "outcome": "weakened", "reason": "The claim's own endpoints (4.57 mN at Cd 0.2 in water, 8.40 uN at Cd 0.3 in air) give 544x not 816x, body drag is a proxy for a total-resistance drop of only ~11-70x, and 'thrust passes / doubles in ~10 strokes' holds only in the GENEROUS case (CENTRAL 2.7x margin and never doubles, STINGY fails).", "corrected_value": "544-fold body-drag reduction (4.57 mN -> 8.40 uN); ~11-70-fold total-resistance reduction; thrust/total drag 2.7-35x (GENEROUS/CENTRAL only)", "depends_on": ["S32_taxi.py line 138 air-drag Cd 0.3 and printed force terms (branch claude/s32-multi-stroke-launch-qpq9g2)", "S32 frontal area 24 mm^2 (from S28)", "S32 body water Cd 0.1-0.3 (from S29, assumed)", "S32 burst speed 1.38 m/s (from S28)", "S32 burst-calibrated G (derived; assumes all burst thrust from tail)", "Floryan et al. 2017 pitching-foil thrust law as read by S32 (not read by me)", "rho_w 1000 and rho_a 1.225 kg/m^3; nu_air ~1.5e-5 m^2/s", "SL ~31 mm inferred from S32's 12-19 mm = 0.4-0.6 SL"]}
```
