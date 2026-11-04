# Challenge 270: lobe CL needed from the 0.45 m/s exit

**Claim under review (S32-organism.md, not written by me):** "FROM THE LOW-END EXIT (0.45 m/s) it fails on WEIGHT SUPPORT, not thrust: the lobe would need CL 1.3-10 to hold the body clear of the water. Minimum supportable speed is 0.51-1.39 m/s." Recorded evidence level: derived. Value: CL 10 required.

**Verdict: WEAKENED.** The arithmetic is correct. The conclusion depends on one hidden assumption: the lobe's thrust stays horizontal, and only steady hydrofoil lift (CL_z ≤ 1, referenced to forward speed U) can hold the body up.
- If the body may pitch nose-up so the thrust vector tilts, the **generous** case is supported at 0.45 m/s. It needs a 6.3° tilt. In that case the lobe's thrust is 1.9× the weight.
- The **central** and **stingy** cases still fail. Their lobe force is too small even when pointed straight up.
- So the "1.3–10" figure and the 0.51 m/s lower bound are artefacts of the horizontal-thrust assumption at the generous end. The claim holds at the central and stingy ends.

Everything below is **calculated** with S32's own stated inputs. None of it is observed. Script: `docs/research/fish/challenge_270_check.py`. I wrote it fresh and did not copy S32_taxi.py.

## Sources and read levels

- `docs/research/fish/S32-organism.md`, branch `origin/claude/s32-multi-stroke-launch-qpq9g2`.
  - Read level: **full-text** for §1 (equations), §2 (input table), §3.1 (the claim's table) and the summary/answer lines.
- `docs/research/fish/S32_taxi.py`, same branch.
  - Read level: **full-text for lines 1–140**: the model, `forces()`, the parameter setup and `G_calibrated`.
  - Lines 141–289 (the printing and scenario driver) were not read. I took the scenario definitions from the §3.1 table header instead.
- No external literature was searched for this challenge. Any statement about other taxa below is my reasoning, not a citation.

## 1. Independent arithmetic

The inputs are as S32 states them:
- Lower lobe area 18.9 mm² (ASSUMED in S32), with φ = 1 / 0.5 / 0.25.
- Chord 6 mm, mass 0.25 / 0.25 / 0.40 g.
- Wing lift fraction (U/V_to)², with V_to = 4.41 / 4.41 / 5.58 m/s.
- Meniscus pull-down 2σc·cosθ, with cosθ = 0 / 0.5 / 1.
- ρ_w = 1000 kg/m³ and U = 0.45 m/s, so q = 101.25 Pa.

| Case | Vertical need (W − L_wing + F_σ,v) | q·S_imm | CL_z needed | U where CL_z = 1 |
|---|---|---|---|---|
| generous | 2.427 mN | 1.914 mN | **1.27** | **0.506 m/s** |
| central | 2.859 mN | 0.957 mN | **2.99** | **0.771 m/s** |
| stingy | 4.763 mN | 0.478 mN | **9.95** | **1.387 m/s** |

Hand check, generous case: 2.4525 mN × (1 − 0.0104) = 2.427 mN. Dividing by 1.914 mN gives 1.268.

For the CL_z = 1 speed, solve W + F_σ,v = U²(½ρ_w S_imm + W/V_to²). Generous: U² = 2.4525e-3 / (9.45e-3 + 1.26e-4), so U = 0.506 m/s.

These reproduce S32's 1.27 / 2.99 / 9.95 and 0.51 / 0.77 / 1.39 m/s exactly. **The arithmetic survives.**

## 2. Proxy

S32 frames the question as "can the lobe hold the body up?" It measures the answer with one proxy: the steady hydrofoil lift coefficient of the lobe, referenced to U. The quantity that actually matters is different. It is whether the lobe's **total hydrodynamic force vector** can be split between support and propulsion.

S32's own thrust law, T = ½ρ_w S_imm[G − C_D U²], is independent of U to first order. At 0.45 m/s, S32's table gives T_lobe = 4.66 / 1.76 / 0.61 mN, and I recompute 4.664 / 1.761 / 0.607 mN. So in the generous case the lobe produces **1.92× the vertical need**, and the model throws all of it away horizontally.

## 3. Hidden assumption, relaxed

**Assumption.** Thrust is horizontal.

**Relaxed assumption.** The body is in air and free to pitch. A nose-up, tail-down attitude of α tilts the thrust vector upward. So:
- Vertical: T sin α + q S CL_z (with CL_z ≤ 1) must cover the vertical need.
- Horizontal: T cos α − D_ind(CL_z) − D_wing − D_body,air − F_σ,h ≥ 0.

All other terms are S32's.

| Case | Supported at 0.45 m/s with tilt? | Minimum tilt | Lobe force ÷ need, fully vertical, no hydrofoil lift | First supported U, steady only → with tilt (scan 0.30–2.00 m/s) |
|---|---|---|---|---|
| generous | **yes** | **6.3°** | 1.92 | 0.51 → ≤ 0.30 (the bottom of the scan) |
| central | no | — | 0.62 | 0.78 → 0.51 |
| stingy | no | — | 0.13 | 1.39 → none up to 2.00 |

**Reading it (my inference):**
- At the generous end, the low exit does not fail on support. The failure in S32 follows from the horizontal-thrust assumption, not from the physics S32 otherwise uses.
- In the central and stingy cases the claim stands. Their failure is a shortage of total lobe force, which is a thrust-magnitude shortage as well. So "not thrust" is accurate only in the generous case, and that is precisely the case the relaxation rescues.
- The stated "minimum supportable speed 0.51–1.39 m/s" becomes ≤ 0.30–0.51 m/s for the two cases that can be supported at all. The stingy case cannot be supported below 2 m/s by either route. That is consistent with S32's own finding that stingy fails at 1.38 m/s too.

**Caveats on my relaxation.** These cut against my verdict, and I am stating them rather than averaging them away.
1. **The thrust law is extrapolated.**
   - At 0.45 m/s, St = f·A_pp/U = 1.00 / 0.87 / 0.73.
   - I did not read Floryan et al. 2017. Whether their measured Strouhal range reaches St ≈ 1 is **unknown** to me.
   - S32's own T_lobe at 0.45 m/s rests on the same extrapolation, so this does not separate my result from S32's. But it does mean neither result is anchored there.
2. **The generous case is itself generous.** S32 assigns all burst thrust to the caudal fin and immerses the whole lower lobe.
3. **Tilting the body tail-down would change immersion and ventilation.** S32 does not model this, and neither do I.
4. **S32's CL_z ≤ 1 may be optimistic in the opposite direction.** S32 itself notes that the zebrafish lobe has no hypocercal cant. An uncanted vertical lobe makes little vertical lift from forward flow.
   - If CL_z is forced to 0, steady-only support never closes at any speed.
   - With CL_z = 0, tilt alone still supports the generous case at 0.45 m/s (script line "CLz<=0 ... True").
   - So this caveat makes S32's minimum-speed proxy weaker, not stronger.

## 4. Evidence level

"Derived" is honest. S32 presents CL 1.3–10 as the output of a model, not as a measurement. The model's lobe area, immersed fraction and CL_z,max are all ASSUMED in S32's own table, and S32 flags them as assumed. No defect here.

## 5. Missed regime or counter-example

The missed regime is **thrust-vectored support**: a nose-up, tail-down body that holds itself up partly with tilted tail thrust. My only basis is the force budget above. I did **not** search the literature for documented tail-standing or tail-supported surface locomotion in small fish, so I cite no counter-example. The scope of that negative is: none searched.

## Inputs this verdict rests on

My verdict rests on S32's inputs, exactly as S32 states them:
- lower-lobe area 18.9 mm², φ, mass, the meniscus terms, V_to;
- the burst-calibrated G and S32's lobe thrust at 0.45 m/s;
- the extrapolation of the Floryan thrust law to St ≈ 0.7–1.0;
- CL_z,max = 1.

My added assumption is that the airborne body can pitch to tilt the thrust vector.

```swarm-challenge
{"claim_id": 270, "outcome": "weakened", "reason": "The CL 1.27/2.99/9.95 and 0.51/0.77/1.39 m/s figures recompute exactly, but they assume the lobe's thrust stays horizontal; in the generous case that thrust is 1.9x the vertical need, and a 6.3 deg nose-up tilt supports the body at 0.45 m/s, so failure at the low exit holds only for the central and stingy cases (lobe force 0.62x and 0.13x of need even pointed straight up).", "corrected_value": "CL_z needed 1.27-9.95 under horizontal thrust (calculated); with thrust tilt: generous supported at 0.45 m/s (6.3 deg), central and stingy still fail; minimum supportable speed <=0.30 / 0.51 / >2.0 m/s (generous/central/stingy, calculated)", "depends_on": ["S32 lower-lobe area 18.9 mm2 (assumed) and immersed fraction 1/0.5/0.25", "S32 masses 0.25/0.25/0.40 g and V_to 4.41/4.41/5.58 m/s", "S32 burst-calibrated G 0.27-0.52 m2/s2 and lobe thrust 4.66/1.76/0.61 mN at 0.45 m/s", "Floryan 2017 thrust law extrapolated to St 0.73-1.00 (Strouhal range not verified by me)", "S32 meniscus terms cos(theta) 0/0.5/1, sigma 0.072 N/m, chord 6 mm", "S32 CL_z,max = 1", "assumption (mine): airborne body can pitch nose-up to tilt lobe thrust"]}
```
