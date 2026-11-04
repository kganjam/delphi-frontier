# Challenge 268: "THRUST PASSES" (S32, multi-stroke taxi)

**Outcome: WEAKENED.** The qualitative result survives: at the 1.38 m/s exit, net force on the airborne body is positive in S32's generous and central cases, so speed rises. Three of the claim's numbers do not survive:

1. The "816×, exactly the density ratio" drag cut does not match the pair it quotes. 4.6 mN → 8 µN is **544×**.
2. "Exactly the density ratio" only holds if the body drag coefficient is the same in air and water. The body's Reynolds number is about 15× lower in air.
3. "Thrust exceeds total drag 3–40×" is really **2.7–35×**. "Doubling in ~10 strokes" happens only in the generous case, and takes **13.6 strokes** there. The central case **never doubles**: it stalls at 2.19 m/s, below 2 × 1.38 = 2.76 m/s.

Everything below is **calculated**. I made no new observation. I reproduced every number with `docs/research/fish/challenge-268_check.py`, which runs against S32's own `S32_taxi.py`.

## The claim under review

> "THRUST PASSES: leaving the water cuts body drag by 816x -- exactly the water/air density ratio, 1000/1.225 -- from 4.6 mN to 8 uN, and burst-calibrated lobe thrust (1.1-3.4 mN) exceeds total drag 3-40x. Speed genuinely rises, doubling in ~10 strokes at 52 Hz"

The claim is recorded as *derived*, value 816-fold drag reduction. Source: `docs/research/fish/S32-organism.md` and `S32_taxi.py` on branch `claude/s32-multi-stroke-launch-qpq9g2`. I read both in full, and I ran the script.

## 1. Independent arithmetic

Inputs are the values S32 states: ρ_w 1000, ρ_a 1.225 kg/m³, frontal area 24 mm², U 1.38 m/s.

- ρ_w/ρ_a = **816.3**. The ratio itself is correct.
- Water drag at Cd 0.2: ½·1000·0.2·24×10⁻⁶·1.38² = **4.57 mN**. This matches S32.
- Air drag at the **same** Cd 0.2: **5.60 µN**. 4.57 mN / 5.60 µN = 816.
- S32's "8 µN" (8.40 µN) is computed at **Cd 0.3** (`S32_taxi.py` line 138: `D_air = 0.5 * RHO_A * 0.3 * ...`). Water uses Cd 0.2 (line 139 label). The quoted pair 4.57 mN → 8.40 µN is a **544×** cut, not 816×.
  - *My inference:* the 816 was taken from the density ratio, and the two drag figures were taken from mismatched Cd values. The sentence then joined the two as if they agreed. They do not.
- Thrust/drag at 1.38 m/s, from S32's own force printout (T is lobe thrust net of the lobe's profile drag; "total drag" is wing + lobe-induced + hysteresis + body):
  - GENEROUS: 3.428 / 0.097 mN = **35.3×**
  - CENTRAL: 1.143 / 0.431 mN = **2.7×**
  - So "3–40×" rounds the lower end up and the upper end up by about 14 %. A faithful statement is **2.7–35×**.
- Doubling (U reaching 2.76 m/s), from integrating S32's own equations with RK4 at 52 Hz:
  - GENEROUS: **13.6 strokes** (0.26 s).
  - CENTRAL: **never**, because U_eq = 2.19 m/s.
  - S32's own trajectory table also shows U = 2.64 m/s at stroke 10, which is not yet double. "Doubling in ~10 strokes" is the generous case, rounded down by about 35 %. It is presented next to a 3–40× range that includes a case which never doubles.

## 2. Proxy check

The claim uses the **body** drag collapse (816×) as the headline. The quantity that decides "thrust passes" is **net horizontal force = lobe thrust − total drag in the taxi configuration**. Once the body is out of the water, body drag is a minor term in that total: 8 µN of 97–431 µN, i.e. 2–9 %. The drag that matters is lobe induced drag (51–289 µN), wing drag (38–47 µN) and meniscus hysteresis (0–86 µN).

So the 816× figure is a vivid proxy that carries almost none of the result. That is not wrong, but it is the wrong number to headline. S32's own table gets this right (it lists the terms). The claim sentence does not.

## 3. Hidden assumptions, relaxed

**(a) Same body Cd in air and water.** This is what makes the cut "exactly the density ratio". At 1.38 m/s with L ≈ 30 mm:
- Body Re in water ≈ 41,400. In air ≈ 2,800 (ν_a/ν_w ≈ 14.8).
- If body drag is dominated by laminar skin friction (Cd ∝ Re^−½), the air Cd rises about 3.85×. The drag cut then becomes √(ρ_w μ_w / ρ_a μ_a) ≈ **212×**, not 816×. Body air drag becomes 11–32 µN for Cd_w 0.1–0.3.
- The 212× figure is my calculation under an assumed friction-dominated regime, not a measurement. The true ratio for a fish-shaped body plus pectoral wing at Re ~3×10³ is **unknown**. I did not search for it. A plausible bracket is ~200–816×, with S32's own mismatched pair (544×) inside it.
- **Effect on the verdict: small.** Rerunning S32's model with Cd_air 0.78 and 1.17 gives T/drag of 31× and 28× (generous) and 2.6× and 2.5× (central). U_eq moves by ≤0.05 m/s. The net force stays positive. **This assumption carries the headline number, not the pass/fail result.**

**(b) Thrust of a surface-piercing lobe equals the 2-D submerged-foil law (κ = 1).** This one carries the pass/fail result.
- Searching on κ, net force at 1.38 m/s reaches zero at **κ = 0.62 in the central case** and **κ = 0.32 in the generous case**.
- The lobe chord is 6 mm. At 1.38 m/s, U/√(g·c) ≈ 5.7, a high-Froude, surface-piercing regime where ventilation and finite span can be expected to cut thrust. *That is my physical inference; I did not search the ventilation literature in this review, and I have no measured κ for any fish lobe.*
- S32 itself says κ is unknown and runs κ = 0.5 as a sensitivity case (§3.3). At κ = 0.5 the central case's step-3 pass becomes a **fail**.
- So "THRUST PASSES" is robust in the generous case, holding down to a 68 % thrust loss. In the central case it holds only for losses under about 38 %. The stingy case already fails at κ = 1. The claim names generous and central only, without this qualifier.

**(c) Burst calibration.** G assumes all burst thrust comes from the caudal fin and that dU/dt = 0 at the burst peak. S32 labels this generous, and I agree with that direction. I did not test it further.

## 4. Evidence level

"Derived" is the honest label for the drag ratio and the force balance. S32 states them as derived and does not present any of them as measured. **No defect there.**

The source tag "density ratio verified here" is literally true: 1000/1.225 = 816.3. But it is misleading as support for an 816× **drag** reduction. Verifying a ratio of two constants does not verify a drag ratio, which also depends on Cd(Re) in each medium. The drag figures the claim itself quotes give 544×.

## 5. Counter-examples and regimes

- Small-fish analogue: the guppy speeds up in air with tail beats continuing (Soares & Bierman 2013). Read-level: **via S24, full text per S24**; I did not read it myself. This agrees in sign with "speed rises". It does not test the magnitude.
- No published counter-example to "a partially immersed tail can accelerate an airborne fish body" was sought or found in this review. **Scope of negative search: none performed (no literature search; review restricted to S32's text, its script, and first-principles arithmetic).**

## Sources

| Source | Read-level |
|---|---|
| `S32-organism.md`, `S32_taxi.py` (branch `claude/s32-multi-stroke-launch-qpq9g2`) | full-text (both read; script executed) |
| Floryan et al. 2017 thrust law, as used inside S32 | could-not-access by me; used only as encoded in S32's script |
| Soares & Bierman 2013 (guppy) | could-not-access by me; as reported in S32 via S24 |
| Air/water viscosities (1.81×10⁻⁵, 1.0×10⁻³ Pa·s) | standard physical constants, not a citation |

## Corrected statement

> Leaving the water cuts body drag by an amount bounded by the density ratio (816× at equal Cd). With Re-dependent Cd it is plausibly ~200–800×. S32's own quoted pair, 4.6 mN → 8.4 µN, is 544×. Body drag is then 2–9 % of total taxi drag. Burst-calibrated lobe thrust (1.1–3.4 mN) exceeds total drag **2.7–35×** at the 1.38 m/s exit, *if the surface-piercing lobe keeps ≥62 % (central) or ≥32 % (generous) of 2-D foil thrust*. Speed rises in both cases. It doubles in **~14 strokes at 52 Hz in the generous case only**; the central case stalls at 2.19 m/s without doubling. (All calculated.)

```swarm-challenge
{"claim_id": 268, "outcome": "weakened", "reason": "Net force is positive at 1.38 m/s in S32's generous and central cases, but the quoted drag pair (4.57 mN at Cd 0.2 vs 8.40 uN at Cd 0.3) is 544x not 816x, equal-Cd ignores a ~15x Re drop in air, thrust/drag is 2.7-35x not 3-40x, doubling takes 13.6 strokes and only in the generous case (central never doubles), and the central-case pass fails if surface-piercing thrust falls below 62% of the 2-D foil law.", "corrected_value": "body drag cut 544x as quoted (816x only at equal Cd; ~212x if friction-dominated); thrust/total drag 2.7-35x; speed doubling 13.6 strokes (generous only)", "depends_on": ["S32_taxi.py force model and SCEN parameters (branch claude/s32-multi-stroke-launch-qpq9g2)", "S28 frontal area 24 mm2", "Miln2021 1.38 m/s burst via S28", "S29 body Cd 0.1-0.3", "Floryan2017 pitching-foil law c6 2.55, C_D 0.08 as encoded in S32", "Kyriakatos2011 52 Hz via S24", "assumed body length 30 mm and laminar-friction Cd scaling for the Re correction", "kappa (surface-piercing thrust factor) unmeasured"]}
```
