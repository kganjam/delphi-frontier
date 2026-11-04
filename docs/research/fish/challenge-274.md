# Challenge 274: S32 reopening condition ("1.4–2.2× its best measured burst tail speed")

**Claim under review (S32-organism.md, recorded evidence level: derived, value 2.2× burst tail speed):**
> REOPENING CONDITION, falsifiable: an airborne zebrafish lobe beating at 1.4–2.2× its best measured
> burst tail speed (A_pp 12–19 mm at 52 Hz, or 72–117 Hz at burst amplitude), or surface-piercing lobe
> thrust at Re 1e4 measuring well above the 2-D foil law.

**Verdict: WEAKENED.** The arithmetic holds for the one calibration the author used. But the claim
calls the denominator "measured" when it is a derived quantity. The 1.4–2.2× band also covers only
the most generous end of S32's own stated body-drag range. Across the full stated range, the
multiplier is **1.4–3.2×** (72–164 Hz at burst amplitude). The absolute amplitude form (A_pp 12–19 mm
at 52 Hz) survives.

**Sources and read levels:**
- S32-organism.md and S32_taxi.py on `origin/claude/s32-multi-stroke-launch-qpq9g2`: **full-text**.
- The commit `09c06c98` (docs/FINDINGS.md) that carries the same sentence: **full-text**.
- Floryan et al. 2017, Kyriakatos 2011 and Miln 2021 were **not** read by me. I use the values exactly
  as S32 states them, so they are inherited inputs and not checked here.

All numbers below are **calculated** by me, from S32's stated inputs. None of them is an observation.

---

## 1. Independent arithmetic

I wrote my own calculation (`indep.py`, scratch, not committed). It uses only these stated inputs:
- c₆ = 2.55 and C_D = 0.08 over Re 4,780–9,560;
- C_D scaled as Re^−½ outside that span, or held constant;
- chord 6 mm, caudal fin area 0.7·6·9 = 37.8 mm², frontal area 24 mm²;
- burst speed U_b = 1.38 m/s;
- V_to = 4.41 m/s (0.25 g) or 5.58 m/s (0.40 g).

**Burst tail speed.** "Thrust = body drag at the burst peak" gives G = (Cd_b·A/S_c + C_D)·U_b², and
then f·A_pp = √(G/c₆):

| Cd_b | f·A_pp at burst | A_pp at 52 Hz |
|---|---|---|
| 0.1 | 0.327 m/s | 6.3 mm |
| 0.2 | 0.393 m/s | 7.6 mm |
| 0.3 | 0.449 m/s | 8.6 mm |

These match S32's 0.33–0.45 m/s.

**Required tail speed.** This is a pure-foil lower bound, with wing, induced and hysteresis drag
ignored: f·A_pp ≥ V_to·√(C_D(Re at V_to)/c₆).

| Mass | C_D scaled | C_D constant |
|---|---|---|
| 0.25 g | 0.606 m/s | 0.781 m/s |
| 0.40 g | 0.722 m/s | 0.988 m/s |

So **A_pp at 52 Hz = 11.6–19.0 mm**. This matches the claim's 12–19 mm. It **does not depend on the
burst calibration**, because the ceiling U_max = f·A_pp·√(c₆/C_D) involves neither G nor the fin area.

**The ratio does depend on the calibration.** My pure-foil ratio is 1.35–2.20× at Cd_b 0.3, which
reproduces the author's 1.38–2.24× (the author's figure includes the extra drag terms). It rises to
1.85–3.02× at Cd_b 0.1.

**Full-model rerun.** I reran S32's own `u_eq` and `zf_params` with the multiplier bisection extended
to all three Cd_b values. The original script calls `G_calibrated(0.3, …)` only.

| Scenario | Cd_b | f·A_pp multiplier (0.25–0.40 g, scaled–const C_D) | Frequency at burst amplitude |
|---|---|---|---|
| GENEROUS | 0.3 | 1.38–2.24 (reproduces the claim) | 72–116 Hz |
| GENEROUS | 0.2 | 1.58–2.56 | 82–133 Hz |
| GENEROUS | 0.1 | 1.90–3.07 | 99–160 Hz |
| CENTRAL | 0.2 | 1.65–2.62 | 86–136 Hz |
| CENTRAL | 0.1 | 1.98–3.15 | 103–164 Hz |

**Finding (my inference from the rerun):** "1.4–2.2×" and "72–117 Hz" hold only at Cd_b = 0.3. S32
lists 0.3 as the *generous* end of an assumed 0.1–0.3 range. Over the range the document itself
states, the band is **1.4–3.2×** and **72–164 Hz**. The source text does not say that the band is
conditional on Cd_b = 0.3.

## 2. Proxy

**What the claim uses:** "best measured burst tail speed."
- No tail speed was measured. S32's own table labels this quantity **Derived**.
- It is calibrated from three inputs:
  - a measured *swimming* speed (1.38 m/s);
  - an **assumed** body Cd (0.1–0.3);
  - an **assumed** caudal fin area (37.8 mm²; S32 reports that no adult zebrafish measurement was
    found).
- The 52 Hz is an EMG maximum, not a filmed tail-beat frequency (S32 §2).

**What matters physically:** the absolute airborne lobe tail speed. The criterion should be
**f·A_pp ≥ ~0.61–0.99 m/s**, as S32 §5 itself states (0.62–1.0 m/s). Equivalently, **A_pp ≥ 12–19 mm
at 52 Hz**.
- A high-speed film of an airborne zebrafish measures exactly this quantity.
- It needs no calibration chain.
- The ratio form divides that measurement by a model output. So the ratio form is only as good as the
  assumed Cd_b and fin area, and it is the weaker way to state the test.

## 3. The hidden assumption, relaxed

**What carries the band:** body Cd_b = 0.3 in the thrust calibration. Relaxing it to the stated range
widens the upper end by about 40% (section 1).

**Fin area acts in the same direction.**
- In the calibration, G ∝ Cd_b·A/S_c + C_D.
- A larger true fin area gives a lower inferred burst tail speed, and so a *higher* required
  multiplier.
- The fin area is unmeasured, so the multiplier is further unbounded on that side.
- The absolute A_pp criterion is unaffected.

**Two things are unchanged by these relaxations:**
- the A_pp 12–19 mm figure;
- S32's qualitative conclusion that the taxi stalls below V_to.

## 4. Evidence level

The recorded level, "derived", is honest for the number 2.2. The claim's *wording*, "its best measured
burst tail speed", presents a derived quantity as measured. That is a labelling defect in the sentence
even though the ledger entry is correct.

## 5. Second clause, and counter-examples

**"Surface-piercing lobe thrust … well above the 2-D foil law" is not quantified, so as written it is
not falsifiable.**
- I calculated the threshold from S32's own model: a thrust multiplier κ ≥ 1.9–5.0 at Cd_b 0.3, and up
  to about 9.9 over the stated Cd_b range.
- That threshold refers to the burst-calibrated tail speed, so it inherits the same calibration
  dependence as the ratio in section 1.
- A direct lobe-thrust measurement would also need the airborne f·A_pp to be specified.

**Counter-example search.** I ran one web search: "adult zebrafish C-start tail tip velocity amplitude
kinematics high-speed video" (standard mode).
- It returned **no** reported adult zebrafish tail-tip velocity or amplitude values.
- I found only larval 3-D C-start kinematics and an adult killifish fast-start study. I read search
  listings only (read-level: **listing**).
- So I can neither confirm nor refute whether transient C-start tail speeds already reach
  0.6–1 m/s. That is **unknown**, and it is the most direct possible counter-example.
- This negative result covers that one query only.

Sources (listing only):
- [JEB fast-start directional control](https://cob.silverchair.com/jeb/article/218/24/3996/14311/The-kinematics-of-directional-control-in-the-fast)
- [Least killifish 3-D fast-start data (Dryad)](https://datadryad.org/dataset/doi:10.5061/dryad.qb5j6)
- [APS 2019 zebrafish startle kinematics](https://meetings-archive.aps.org/mar/2019/l70/353)
- [AIP Advances 2024 zebrafish C-maneuver](https://doaj.org/article/8290cb0c076649519ce434c8410f1cc0)

## Recommended restatement

> Reopens if an airborne zebrafish lobe reaches **f·A_pp ≥ 0.61–0.99 m/s** (A_pp ≥ 12–19 mm at the
> 52 Hz EMG maximum). That is **1.4–3.2×** the *derived* burst tail speed over body Cd 0.1–0.3, or
> 72–164 Hz at the derived burst amplitude. Or it reopens if surface-piercing lobe thrust at Re ~1e4
> exceeds the 2-D law by κ ≳ 2–5 at matched kinematics.

```swarm-challenge
{"claim_id": 274, "outcome": "weakened", "reason": "The 1.4-2.2x band reproduces only at the generous body Cd 0.3 calibration and its denominator is a derived (not measured) burst tail speed; over S32's own stated Cd 0.1-0.3 range the multiplier is 1.4-3.2x (72-164 Hz), while the absolute A_pp 12-19 mm at 52 Hz criterion survives.", "corrected_value": "1.4-3.2x derived burst tail speed (72-164 Hz at burst amplitude); calibration-free form f*A_pp >= 0.61-0.99 m/s, A_pp 12-19 mm at 52 Hz", "depends_on": ["S32_taxi.py equations and G_calibrated (Cd_body 0.1-0.3)", "Floryan2017-foil-scaling c6=2.55, C_D=0.08 at Re 4780-9560 (as stated by S32, not read by me)", "C_D Re^-1/2 extrapolation (S32 assumed)", "Miln2021-burst 1.38 m/s (via S28)", "Kyriakatos2011-52Hz", "S28 V_to 4.41/5.58 m/s", "assumed caudal fin area 37.8 mm2", "Wakamatsu2019 chord 6 mm"]}
```
