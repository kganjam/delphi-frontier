# Challenge 269: does the taxi really stall at 2.19–2.88 m/s?

**Claim under review (S32, `docs/research/fish/S32-organism.md` on branch `claude/s32-multi-stroke-launch-qpq9g2`, read in full):**
"THE TAXI STALLS at 2.19-2.88 m/s, 50-65% of the 4.41 m/s glide speed, after ~30-38 strokes over 1.5-2 m. It does not fail to accelerate; it accelerates to a ceiling below what is needed." Recorded evidence level: derived. Recorded value: 2.5 m/s stall speed.

**Verdict: WEAKENED.** The qualitative claim survives: in this model the taxi accelerates and then levels off below glide speed. The numbers do not:
- The quoted band is narrower than the model's own uncertainty, because one unmeasured input, caudal fin area, was never swept.
- The stroke count and distance apply to only one of the two scenarios that the band covers.

Everything below is **calculated**. Nothing in it is an observation. Reproduce it with `python3 docs/research/fish/challenge-269.py`. That script was written independently and does not import `S32_taxi.py`.

## 1. Independent arithmetic

I rebuilt the force balance from S32's stated inputs: the Floryan 2017 law C_T = 2.55 St² − 0.08; the burst calibration G = (Cd_b·A/S_c + C_D)·U_b²; U_b = 1.38 m/s; A = 24 mm²; S_c = 37.8 mm²; S28's wing, 192 mm², CL_max 1.07.

- **Glide speed.** V_to = √(2·0.25e-3·9.81 / (1.225·192e-6·1.07)) = **4.41 m/s**. ✔
- **Foil-only ceiling, closed form.** U_max = √(G/C_D(U_max)). With Cd_b 0.3: G = (0.3·24/37.8 + 0.08)·1.38² = 0.515 m²/s².
  - With C_D held constant: U_max = **2.54 m/s**.
  - With Re-scaled C_D: U_max = **2.96 m/s**.
  - The full model, which adds wing drag and lobe induced drag, gives a slightly lower value. This is consistent with S32.
- **Full-model equilibrium, my code:**
  - GENEROUS: **2.88** m/s
  - GENEROUS with constant C_D: **2.50** m/s
  - CENTRAL: **2.19** m/s

  All three match S32 to 0.01 m/s. 2.19/4.41 = 49.7 % and 2.88/4.41 = 65.3 %. ✔
- **Trajectory (S32's own script, rerun).**
  - GENEROUS reaches the |a| < 1 mg stop at 38.1 strokes, 0.733 s, 1.95 m.
  - **CENTRAL takes 74.0 strokes, 1.42 s, 2.91 m.**

**Defect 1 (scope).** The claim attaches "~30–38 strokes over 1.5–2 m" to the whole 2.19–2.88 band. Those figures hold only for the GENEROUS end. The CENTRAL end, at 2.19 m/s, takes about twice as many strokes and 2.9 m. The "38 strokes" also depends on an arbitrary stopping rule (|a| < 1 mg) applied to an asymptotic approach. The S32 body text describes it correctly as "within 1 %" in the generous case. The claim sentence drops that qualifier.

## 2. Proxy check

The quantity that matters is the cycle-averaged thrust per unit immersed area that an airborne tail can produce. S32 stands in for it with the **instantaneous force balance at the peak of the 1.38 m/s burst**, spread over an **assumed** fin area. The burst is reported as an escape maximum (VIA S24/S28; I did not read the primary source).

- **The fin-area proxy.** The ceiling depends on the assumed fin area, even though S_imm cancels. G is thrust per unit area inferred by dividing body drag by S_c, so U_max = U_b·√(1 + Cd_b·A/(S_c·C_D)).
  - A **smaller** assumed fin gives a **higher** ceiling.
  - This runs opposite to the intuition behind S32's "generous" labels.
- **The transient proxy.** dU/dt = 0 at a fast-start peak does not establish a steady, cycle-averaged thrust. The direction of this bias is **unknown**. I did not test it, because the burst time series was not available to me.

## 3. Hidden assumption, relaxed

**Caudal fin area S_c = 37.8 mm²** is labelled ASSUMED in S32: height 9 mm, taper 0.7, and "no adult zebrafish fin area was found". It does not appear in S32's sensitivity table (§3.3), even though §3.3 states that "no assumed parameter within its stated range lifts the ceiling to V_to".

My sweep, all calculated, GENEROUS otherwise, 0.25 g, V_to 4.41 m/s:

| S_c (mm²) | Cd_b 0.2, constant C_D | Cd_b 0.2, scaled C_D | Cd_b 0.3, constant C_D | Cd_b 0.3, scaled C_D |
|---|---|---|---|---|
| 45 | 2.08 | 2.26 | 2.36 | 2.67 |
| 37.8 (S32) | 2.18 | 2.41 | 2.50 | 2.88 |
| 24.8 (taper 0.46, forked fin) | 2.49 | 2.86 | 2.90 | **3.48** |
| 18 | 2.77 | 3.28 | 3.27 | 4.05 |
| 15 | 2.95 | 3.56 | 3.51 | **4.42 (closes)** |

What it takes to close, i.e. U_eq ≥ V_to:
- **Fin area.** Even the most favourable branch needs S_c ≤ 15.0 mm², 0.40× S32's value. Other branches need S_c ≤ 5–9 mm².
- **Body drag.** At S32's area, body Cd_b must be ≥ 0.69 (scaled C_D) or ≥ 1.21 (constant C_D). S32's stated range was 0.1–0.3.

My inference: a 15 mm² caudal fin on a fish with a 6 mm fin length implies a fin height of about 3.6 mm at 0.7 taper. I judge that implausibly small, but I have **no measurement**, so this judgement is not evidence.

A forked-fin taper of about 0.46 is equally unmeasured. With it the ceiling rises to **3.48 m/s, 79 % of V_to**. That is outside the claimed 50–65 % band, but still below V_to.

**Body drag during burst.** Body drag during undulatory swimming may exceed rigid-body drag. The size of that enhancement is debated in the literature, but I read no source this session and quote no factor. An enhancement of about 2.3× over Cd 0.3 would close the scaled branch. This is the most credible route to breaking the qualitative claim, and it is **untested**.

**Defect 2 (band too narrow).** Counting only calibrated-thrust cases and S32's own Cd_b range, and adding the fin-area range above, the equilibrium spans **about 1.8–3.5 m/s (41–79 % of V_to)**, not 2.19–2.88.
- Low end: Cd_b 0.1 gives 1.81–1.89 m/s. This is in S32's own §3.3 but left out of the claim.
- High end: S_c about 25 mm², Cd_b 0.3, scaled C_D gives 3.48 m/s.

The recorded point value of 2.5 m/s is the GENEROUS case with constant C_D. It is not a central estimate.

## 4. Evidence level

"Derived" is **honest**. S32 states at the top that nothing is a measurement, and the stall speed comes from integrating ODEs on partly assumed inputs. No defect here.

## 5. Counter-examples searched

- **Hatchetfishes (Gasteropelecidae), small freshwater fish said to skim the surface.**
  - Search (standard web) found Wiest 1995, *J. Zool.* 236:571–592, at **listing** level only.
  - A hobbyist page says Wiest's high-speed video disproved propelled flight (**search-summary**).
  - Britannica describes gliding/hydroplaning "short distances" (**search-summary**).
  - **No speeds were found.** This is not a usable counter-example.
- **Juvenile flying fish.**
  - A secondary report of Davenport 1994 says juveniles begin "flying" at about 5 cm (**search-summary**; original not read).
  - An APS DFD 2013 abstract, "Flying fish accelerate at 5 G to leap from the water surface", describes 1–5 cm juveniles **leaping** (**listing**; abstract text not read).
  - My inference: this suggests small exocoetids may use a single-impulse leap rather than a taxi. That bears on S29's single-impulse mode, not on this taxi ceiling, so it does not refute the claim. It is a regime the claim's framing does not cover. Juvenile taxi speeds: **unknown**.

Scope of the negative search: two standard web searches. No primary full text was read for either taxon.

## 6. Summary

- **Holds:**
  - The arithmetic replicates exactly.
  - Within the model, the acceleration-then-ceiling behaviour is robust.
  - Closure needs either a fin of 15 mm² or less, or a body Cd of 0.69 or more, both well outside the stated inputs.
- **Does not hold as stated:**
  - The 2.19–2.88 m/s (50–65 %) band omits S32's own Cd_b 0.1 cases and an unswept fin-area assumption that moves the ceiling to about 3.5 m/s (79 %).
  - "30–38 strokes, 1.5–2 m" belongs to the generous case only. CENTRAL is 74 strokes, 2.9 m.

```swarm-challenge
{"claim_id": 269, "outcome": "weakened", "reason": "Arithmetic replicates and the sub-V_to ceiling survives, but the unswept assumed caudal fin area (37.8 mm2) and S32's own Cd_b=0.1 cases widen the derived stall band to ~1.8-3.5 m/s (41-79% of V_to), and the 30-38 strokes / 1.5-2 m figure applies only to the generous case (central: 74 strokes, 2.9 m).", "corrected_value": "~1.8-3.5 m/s derived taxi ceiling (41-79% of 4.41 m/s); 38-74 strokes, 1.95-2.91 m to the |a|<1 mg stop", "depends_on": ["S32 taxi model and S32_taxi.py (claude/s32-multi-stroke-launch-qpq9g2)", "Floryan2017-foil-scaling (c6 2.55, C_D 0.08, Re 4780-9560) as transcribed by S32", "S28 wing (192 mm2, CL_max 1.07) and 24 mm2 frontal area", "Miln2021-burst 1.38 m/s via S28", "S29 body Cd range 0.1-0.3", "assumed caudal fin area 15-45 mm2 (unmeasured)", "Wakamatsu2019 caudal fin length 6 mm via S24"]}
```
