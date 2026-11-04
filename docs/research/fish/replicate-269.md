# Replication of claim 269: the zebrafish taxi stall speed

**Status:** independent re-derivation. **Everything below is calculated, not observed.** I numerically integrated an equation of motion on stated inputs. Nothing here is a measurement.

**Reproduce:** `python3 docs/research/fish/replicate_269_taxi.py` runs the full sweep. `python3 docs/research/fish/replicate_269_sens.py` runs the GENEROUS sensitivities and the CENTRAL case. Each takes a few seconds. I wrote both scripts from scratch. I did **not** read or run `S32_taxi.py`.

## 1. What I was asked and what I saw

The question, with the answer removed, was: *the taxi stalls at 2.19–2.88 m/s, 50–65 % of the 4.41 m/s glide speed, after ~30–38 strokes over 1.5–2 m.* The inputs live in `docs/research/fish/S32-organism.md`, on branch `claude/s32-multi-stroke-launch-qpq9g2`.

**Contamination disclosure. Read this before weighting my agreement.**
- I read S32 §1 (the equations of motion) and §2 (the input table) to get the inputs.
- §1 does not define the immersion depth *d*. To look for it, I grepped the doc for `depth|AR_eff|GENEROUS`. That grep showed me three lines of the original's results:
  - the definition of the GENEROUS case, with its force row at 1.38 m/s (T 3.43 mN, D_wing 0.04, D_ind 0.05, net +3.33 mN, CL_z 0.12);
  - a summary line containing "30–38 strokes (0.6–0.7 s, about 1.5–2 m)";
  - a line on the CL_z = 1 minimum speed.
- I then stopped reading.
- I picked *d* = φ·(lobe height 4.5 mm) **after** seeing that row. The 0.051 mN induced drag my model gives at 1.38 m/s matches it. So **the depth choice is not independent.** It only affects D_ind, which is small at φ = 1.
- I did not see the ceiling speeds before deriving them, except as the range given in the question itself.
- I read S32 §0 and §3 only **after** my numbers in §4 below were computed. I needed them to define CENTRAL and to compare.

**Limit of this replication.** I used the original's model form (§1) and its inputs (§2). What agrees below is the **arithmetic and integration**, not the physics. A shared modelling error would survive this check. See §6.

## 2. Inputs

Read-levels refer to my own access this session. Most inputs came from S32's input table. I did not re-open the primary papers, so each one is **listing** level for me, meaning I saw S32's statement of the value and not the source.

| Input | Value | Source | My read-level |
|---|---|---|---|
| Foil thrust law | C_T = 2.55 St² − 0.08, so T = ½ρ_w S (G − C_D U²) with G = 2.55 (f·A_pp)² | Floryan, Van Buren, Rowley & Smits 2017 (JFM; arXiv 1704.07478), as quoted in S32 §2 | listing (via S32); not re-read |
| Measured range of lobe C_D = 0.08 | Re 4,780–9,560 | same | listing (via S32) |
| C_D outside that range | "scaled": 0.08·(Re_edge/Re)^½. "const": 0.08 | S32 §2, ASSUMED there | listing |
| Burst speed (calibration) | 1.38 m/s | S28, via S32 | listing |
| Body frontal area | 24 mm² | S28, via S32 | listing |
| Body Cd in water (calibration) | 0.1–0.3 | S29, via S32 | listing |
| Caudal fin area / lower lobe | 37.8 / 18.9 mm²; height 9 mm, so lobe height 4.5 mm | S32, ASSUMED there | listing |
| Caudal chord | 6 mm | Wakamatsu 2019, via S24/S32 | listing |
| Tail-beat frequency (for counting strokes) | 52 Hz | Kyriakatos 2011, via S24/S32 | listing |
| Wing | S_w 192 mm², AR 5, CL_max 1.07, e 0.8, so k = 0.0796; CD0 0.08–0.20 | S28 case C, via S32 | listing |
| Mass | 0.25 g (also 0.40 g) | S32 | listing |
| Immersed fraction φ | 0.25 / 0.5 / 1.0 | S32, ASSUMED | listing |
| Immersion depth d | **φ × 4.5 mm** (my assumption; not stated in S32 §1–2; see the disclosure) | mine | — |
| AR_eff of the lobe | 2d²/S_imm (mirror image) | S32 §1 | listing |
| Surface tension | σ = 0.072 N/m; cosθ 0–1; Δcosθ 0–0.3 | physical constant; angles ASSUMED in S32 | listing |
| ρ_w, ρ_a, ν_w | 1000 kg/m³; 1000/816 = 1.225 kg/m³; 1.0×10⁻⁶ m²/s | standard values (S32 states the 816 ratio) | — |
| Body air drag | ½ρ_a·0.3·A_front·U² | S32 §1 | listing |

## 3. The arithmetic

**Thrust calibration.** At the burst peak (dU/dt = 0, whole fin in water), fin thrust equals body drag:

½ρ_w S_fin (G − 0.08 U²) = ½ρ_w Cd_b A U², so G = U²(0.08 + Cd_b·A/S_fin) = 1.9044 × (0.08 + Cd_b × 0.6349)

- Cd_b = 0.1 gives G = 0.273 m²/s².
- Cd_b = 0.2 gives G = 0.394 m²/s².
- Cd_b = 0.3 gives G = 0.515 m²/s².

These match S32's stated 0.27–0.52.

**Glide speed.** V_to = √(2mg/(ρ_a S_w CL_max)) = √(2 × 2.4525×10⁻³ / (1.225 × 192×10⁻⁶ × 1.07)) = √19.49 = **4.415 m/s** at 0.25 g. At 0.40 g it is 5.58 m/s.

**Horizontal equation.**

m dU/dt = ½ρ_w φS_lobe [G − C_D(Re)U²] − ½ρ_a S_w U²(CD0 + k CL²) − ½ρ_a 0.3 A U² − D_ind − 2σc Δcosθ

- Wing: CL = min(CL_max, W/(q_a S_w)).
- Lobe vertical force: F_z = W − L_wing + 2σc cosθ.
- Lobe lift coefficient: CL_z = F_z/(q_w S_imm). The fish fails if CL_z > 1.
- Lobe induced drag: D_ind = q_w S_imm CL_z²/(π·0.8·AR_eff).
- Reynolds number: Re = U·c/ν = 6000·U.

**Check at 1.38 m/s, GENEROUS** (Cd_b 0.3, φ 1, C_D scaled, CD0 0.08, no surface tension, 0.25 g):

| Term | Arithmetic | Value |
|---|---|---|
| Lobe thrust | 0.5 × 1000 × 18.9×10⁻⁶ × (0.515 − 0.08 × 1.9044) | 3.428 mN |
| Wing drag | | 0.038 mN |
| Body air drag | | 0.008 mN |
| Lobe induced drag | | 0.051 mN |
| **Net** | | **+3.331 mN** (CL_z = 0.123) |

**The ceiling.** I found the root of net force between 1.38 m/s and V_to by bisection. Separately, I integrated the trajectory from 1.38 m/s with RK4 at dt = 20 µs, stopping when |a| < 1 mg.

## 4. My result (computed before reading S32's results)

| Case | Ceiling U_eq | % of V_to | 99 % of U_eq reached at | Run stopped (\|a\| < 1 mg) at |
|---|---|---|---|---|
| GENEROUS | **2.878 m/s** | 65.2 % | 0.401 s, **20.8 strokes, 1.00 m** | 0.733 s, 38.1 strokes, 1.95 m |
| GENEROUS, C_D const | 2.495 | 56.5 % | 0.261 s, 13.6 strokes, 0.57 m | 0.498 s, 25.9 strokes, 1.16 m |
| GENEROUS, Δcosθ 0.3 + cosθ 1 | 2.773 | 62.8 % | 21.2 strokes | 38.6 strokes |
| GENEROUS, Cd_b 0.2 | 2.411 | 54.6 % | 21.7 strokes | 39.2 strokes |
| GENEROUS, Cd_b 0.1 | 1.887 | 42.7 % | 21.4 strokes | 39 strokes |
| GENEROUS, CD0 0.20 | 2.834 | 64.2 % | 20.3 strokes | 37.3 strokes |
| GENEROUS, κ 0.8 / 0.6 | 2.483 / 2.050 | 56.3 / 46.4 % | ~22 strokes | ~39 strokes |
| GENEROUS, 0.40 g | 2.872 | 51.4 % of 5.58 | 33.7 strokes | 57.6 strokes |
| φ = 0.25 (0.25 g, Cd_b 0.3) | 2.46 (scaled) | 55.7 % | ≈4 s: acceleration at 1.38 m/s is below 1 mg, so the run stalls at the start | — |
| φ = 0.25, Cd_b 0.1, or 0.40 g at φ ≤ 0.5 with Cd_b 0.1 | — | — | support fails (CL_z > 1) | — |

I computed CENTRAL only after reading S32 §3 for its definition: Cd_b 0.2, φ 0.5, scaled, CD0 0.12, cosθ 0.5, Δcosθ 0.1, 0.25 g. Result: **U_eq = 2.194 m/s (49.7 %)**. 99 % is reached at 46.5 strokes and 1.75 m; the 1 mg stop comes at 74.0 strokes and 2.91 m.

**My value:** the taxi stalls at **2.19–2.88 m/s (50–65 % of V_to = 4.41 m/s)** across CENTRAL to GENEROUS. This is computed.

**Uncertainty.** Within the stated input ranges, the ceiling spans about 1.9–2.9 m/s:
- Cd_b, which sets the thrust calibration, dominates.
- C_D extrapolation (scaled vs const) moves it by 0.4 m/s.
- κ < 1 lowers it further.

Integration error is negligible: bisection and RK4 agree to 1 mm/s. No input in range lifts the ceiling to V_to. Reaching V_to needs a larger thrust term G, not a different mass or wing.

## 5. Comparison with the recorded value

I read S32 §0, §3.1–3.3 after computing the above.

| Quantity | S32 (recorded) | Mine | Verdict |
|---|---|---|---|
| GENEROUS ceiling | 2.88 m/s, 65 % | 2.878 m/s, 65.2 % | **AGREE** |
| CENTRAL ceiling | 2.19 m/s | 2.194 m/s, 49.7 % | **AGREE** |
| GENEROUS sensitivities | Cd_b 1.89 / 2.41 / 2.88; const 2.50; CD0 0.20: 2.83; Δcos 0.3: 2.78; φ 0.25: 2.46; 0.40 g: 2.87 | 1.887 / 2.411 / 2.878; 2.495; 2.834; 2.776; 2.459; 2.872 | **AGREE** |
| Strokes / distance to the stall, GENEROUS | "within 1 % of that speed after about 30–38 strokes (0.6–0.7 s, about 1.5–2 m)" | within 1 % after **20.8 strokes, 0.40 s, 1.00 m**. The 38 strokes, 0.73 s, 1.95 m figure is my \|a\| < 1 mg stopping time | **DISAGREE on wording** |

**On the stroke count.** S32's own trajectory table (§3.2) gives 2.84 m/s at stroke 20, which is 98.6 % of 2.88, and 2.87 m/s at stroke 30 (99.7 %). S32's 38 strokes, 733 ms and 195 cm are the equilibrium stop, which matches my 1 mg stop exactly.

*My inference, not the author's claim:* "within 1 % after 30–38 strokes, 1.5–2 m" mixes 99.7 % (stroke 30) with the solver's stop criterion (stroke 38). A strict 1 % criterion is met at about 21 strokes and about 1.0 m. This does not change the ceiling, the conclusion, or the "accelerates then stalls" description.

## 6. What this replication does not test

- **The model form.** I took S32 §1's equations as given. The quasi-steady pitching-foil law applied to a surface-piercing, partly immersed caudal lobe in air-supported taxi has not been validated for any fish. Here the model is assumed, not tested. The ceiling formula U_max ≈ f·A_pp·√(c₆/C_D) follows from that law. If the law is wrong for a ventilating lobe, both derivations fail together.
- **The primary sources.** I did not re-open Floryan et al. 2017, Kyriakatos 2011, Wakamatsu 2019, S24, S28 or S29. Each value is at listing level, via S32.
- **The depth d.** It is my assumption, and it was chosen after seeing one of the original's force rows (see §1).

## 7. Verdict

**AGREE** on the stall ceiling of 2.19–2.88 m/s, 50–65 % of V_to. **Minor DISAGREE** on the "within 1 % after ~30–38 strokes, 1.5–2 m" phrasing: by a strict 1 % criterion it is about 21 strokes and 1.0 m in GENEROUS, and about 47 strokes and 1.75 m in CENTRAL.

```swarm-replication
{"claim_id": 269, "my_value": "2.19-2.88 m/s ceiling (CENTRAL 2.194, GENEROUS 2.878 m/s; 49.7-65.2% of V_to 4.415 m/s), computed not observed", "agrees": true, "note": "Ceilings reproduce to 0.01 m/s with an independently written RK4 integrator on S32's model and inputs, but the 1%-of-ceiling point is ~21 strokes / 1.0 m in GENEROUS (not 30-38 strokes / 1.5-2 m, which is the |a|<1 mg solver stop), and the shared model form plus a depth assumption chosen after seeing one original force row limit the independence."}
```
