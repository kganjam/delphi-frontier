# Replication of claim 273: "the model validates against a real animal"

**What I was asked.** Re-derive, without seeing the answer, the number behind the S32 claim that its taxi model
validates against a real animal. Context file: `docs/research/fish/S32-organism.md` (branch `claude/s32-multi-stroke-launch-qpq9g2`).

**What I read before deriving.** S32 §1 (the equations of motion) and §2 (the input table) only. I did **not** read
S32 §0 (short answer), §3–§6, or `S32_taxi.py` before my numbers were fixed. §0 contains the result, so I stopped
before it. After my derivation was complete I read §0, §4 and §5 for the comparison below.

**Everything below is calculated, not observed.** These are equations of motion integrated on stated inputs. No number
here is a measurement of a flying fish.

---

## 1. The quantity

The question is the exocoetid run in S32 §4.2. Take the S32 taxi equations (§1) unchanged and apply them to a flying fish
leaving the water at 10 m/s. Does the speed rise to glide (take-off) speed V_to? How long does that take, and what ceiling
speed does it reach? The test is whether a model built for zebrafish reproduces what a flying fish actually does.

## 2. Inputs, sources and read-levels

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Pitching-foil thrust law | C_T = c₆ St² − C_D, c₆ = 2.55, C_D = 0.08. St = 2fA/U, where A is the half-amplitude, so St = f·A_pp/U. C_T is normalised by ½ρU²·s·c | Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478v1, §2.3 eq. 2.7 and §5 | **full-text** (arXiv v1, fetched this session) |
| Reynolds number of that law | The pitch data were taken "at a fixed velocity of 60 mm/s", c = 80 mm, so Re = 4,780. The tunnel ran 60–120 mm/s (Re up to 9,560), but §5 says pitch used 60 mm/s only | same | full-text |
| Pitching power law | C_P = c₈ St² + c₉ St² f\*, c₈ = 7.78, c₉ = 4.89 | same, §5 | full-text |
| Hypocaudal lobe area | 0.003·M^0.650 m² (Cypselurus, N = 90) | Fish 1990, *J. Zool.* 221:391, Table I, via `connectors/fish_controls/fish1990.py` on `main` | **listing**: a project transcription of page images. I could not reach the PDF myself |
| Wing loading | 285.015·M^0.400 N/m² (Cypselurus, N = 113) | Fish 1990 Table II, same transcription | listing |
| Wing aspect ratio (sensitivity only) | 12.717·M^0.163 | Fish 1990 Table III, same transcription | listing |
| Mass, kinematics | 0.191 kg, 0.25 m, 50 Hz, 15° deflection, 36 W for steady taxi at 10 m/s | Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560. **This is CFD, i.e. simulated** | **abstract** (bioRxiv API, fetched this session) |
| Exit speed 10 m/s, taxi to 15–20 m/s | as stated | S32 §2, "SEARCH-EXTRACT (via S30)". I did not find a primary observational source | **search-summary**, and second-hand |
| Lobe chord, A_pp | 2.5 cm. A_pp 2.0 / 2.6 / 3.1 cm (S32's assumed lobe length 4–6 cm × 2 sin 15°). I added 1.3 cm = 2·c·sin 15°, the pitch-about-leading-edge reading of "15° deflection" | **ASSUMED** (S32 assumes the same, apart from my 1.3 cm case) | — |
| Immersed fraction φ | 0.5, 1.0. Lobe depth d = φ × (S_lobe/c) | ASSUMED | — |
| Wing CD0, k | 0.08 / 0.20. k = 1/(π·0.8·5) as in S32, with a sensitivity case using Fish's AR | ASSUMED (S32 §2) | — |
| Body frontal area | 5.9 cm² (an ellipse 3 × 2.5 cm). Its term is about 1 % of drag | ASSUMED (mine) | — |
| C_D beyond the measured Re | "const": 0.08 at every Re. "scaled": 0.08·(Re_ref/Re)^½ for Re > Re_ref | ASSUMED extrapolation, as S32 §2 states | — |
| ρ_w, ρ_a, ν, σ, CL_max | 1025 or 1000, 1.225, 1.0e-6, 0.072, 1.07 | constants; CL_max from S28 | — |

## 3. Arithmetic

**Allometry, M = 0.191 kg.**
- S_lobe = 0.003 × 0.191^0.65 = 0.003 × 0.341 = **10.23 cm²**.
- WL = 285.0 × 0.191^0.4 = **147.0 N/m²**.
- V_to = √(2·147.0/(1.225·1.07)) = **14.98 m/s**.
- S_w = W/WL = 1.874/147.0 = 127 cm².

**M = 0.300 kg.** S_lobe = 13.72 cm², WL = 176.1 N/m², V_to = **16.39 m/s**.

**Closed-form foil ceiling.** Ignore every drag except the lobe's own. Thrust is ½ρS(c₆(fA_pp)² − C_D U²), so it is zero at
U_max = f·A_pp·√(c₆/C_D).
- **const** (C_D = 0.08), A_pp 2.6 cm: 1.30 × 5.65 = **7.3 m/s**. This is below the 10 m/s exit speed, so the fish decelerates.
- **scaled from Re 4,780.** C_D ∝ U^−½ makes C_D·U² = 0.08·√(4780ν/c)·U^1.5 = 0.0350·U^1.5.
  - A_pp 2.6 cm: G = 2.55·1.30² = 4.31, so U^1.5 = 123 and U_max ≈ **24.7 m/s**.
  - A_pp 2.0 cm: G = 2.55, U_max ≈ 17.6 m/s.
  - Wing, induced and body drag then pull these down, as in the table below.

**Support at the exit speed.** At 10 m/s the wing carries (10/14.98)² = 44.6 % of W. The lobe must supply 1.04 N on
½·1025·10²·5.1 cm² = 26.2 N, so **CL_z ≈ 0.04**. Support is trivial, and the induced drag is about 7 mN.

**Full model.** I integrated m dU/dt = T_lobe − D_wing − D_body − D_ind − F_σ,h with RK4 (dt = 0.1 ms) from 10 m/s
(`docs/research/fish/replicate_273_taxi.py`, my own code). The 1025 kg/m³, Re_ref 4,780 grid gives the following.
Time and distance are to V_to; "ceiling" is the highest U in [2, 40] m/s with net force ≥ 0.

| M | A_pp | φ | C_D | Ceiling (m/s) | Reaches V_to? | t, x |
|---|---|---|---|---|---|---|
| 0.191 | 3.1 cm | 0.5–1 | scaled | 20.2–27.3 | yes | 0.44–1.21 s, 5.6–15.4 m |
| 0.300 | 3.1 cm | 0.5–1 | scaled | 20.1–27.4 | yes | 0.70–2.07 s, 9.4–28.5 m |
| 0.191 | 2.6 cm | 0.5 | scaled | 15.7–19.1 | yes | 2.1–3.8 s, 27–51 m |
| 0.300 | 2.6 cm | 0.5 | scaled | 15.6–18.7 | **only at CD0 0.08** | 3.9 s / 54 m; with CD0 0.20 it stalls at 15.6 m/s, below 16.4 |
| both | 2.0 cm | 0.5–1 | scaled | 11.4–14.7 | **no** (just short) | — |
| both | 1.3 cm | 0.5–1 | scaled | 5.8–8.5 | no: decelerates | — |
| both | 2.0–3.1 cm | 0.5–1 | const | 4.9–8.6 | **no: decelerates in every case** | — |

**Threshold amplitudes, found by scan.**
- *scaled:* the ceiling reaches V_to when A_pp ≥ **2.1–2.8 cm**. It reaches 10 m/s when A_pp ≥ 1.5–1.8 cm.
- *const:* the ceiling reaches 10 m/s when A_pp ≥ 3.7–3.8 cm. It reaches V_to when A_pp ≥ **5.4–6.2 cm**.

**Variant using S32's stated conventions.** Here ρ_w = 1000 (from ρ_w/ρ_a = 816) and C_D is held at 0.08 up to Re 9,560.
I added this after my grid, for the comparison only.

| Case (M 0.191, φ 0.5, CD0 0.08) | Result |
|---|---|
| A_pp 2.6 cm, const | decelerates to **6.95 m/s** |
| A_pp 2.6 cm, scaled | reaches 15.0 m/s in **4.50 s / 60.5 m / 225 strokes** |
| A_pp 3.1 cm, scaled | reaches 15.0 m/s in **1.28 s / 16.3 m / 64 strokes** |

With CD0 0.20 the 2.6 cm scaled case stalls at 13.8 m/s and does not reach V_to.

**Power cross-check** (Floryan C_P, at 10 m/s, 50 Hz, A_pp 2.6 cm, φ 0.5, ρ 1000):
- St = 0.130, f\* = 0.125, so C_P = 0.0169 × (7.78 + 4.89 × 0.125) = 0.1418.
- P = 0.1418 × ½·1000·10³·5.12e-4 = **36.3 W**.

## 4. My value

**Result.** I ran the S32 equations on a Cypselurus-allometry flying fish of 191 g. They predict a taxi from 10 m/s to
V_to = 15.0 m/s **only if** two conditions hold:
- (a) foil drag falls with Reynolds number (the "scaled" extrapolation, about 26–50× beyond the measured Re);
- (b) the lobe's peak-to-peak tip excursion is A_pp ≳ 2.1–2.8 cm at 50 Hz.

**Time to V_to.** At A_pp 3.1 cm: **1.0–1.3 s, 13–16 m (50–64 strokes)** at φ 0.5. At A_pp 2.6 cm: 2.1–4.5 s.

**Constant-C_D branch.** It fails in every case I ran: the fish decelerates to **about 7–8.6 m/s** (range 4.9–8.6).
This is calculated. The spread comes from assumed inputs (A_pp, φ, CD0, Re_ref), and A_pp dominates.

**How strong is the "validation"? This is my inference, not S32's claim.** It is weaker than "validates against a real animal".
- The "real animal" side rests on a **search-summary** (10 → 15–20 m/s) that is second-hand.
- The other support is a **CFD abstract**, which is a simulation and not an observation.
- The decisive input, A_pp, is assumed. Agreement depends on it sharply: A_pp 2.0 cm fails and 2.6 cm passes.

**Unresolved disagreement between sources.**
- Deng's abstract says 50 Hz / 15° is the *steady state* at 10 m/s: thrust equals drag there (simulated). In this model,
  thrust equals drag at 10 m/s at 50 Hz only if A_pp ≈ 1.5–1.8 cm (scaled).
- At the A_pp values that make the taxi close (≥ 2.1 cm), the model's fish *accelerates* at 50 Hz, while Deng's CFD fish
  holds 10 m/s at 50 Hz.
- Deng's fish reaches 16.5 m/s only by raising power to 350 W, presumably through higher frequency or amplitude.
  The abstract does not say which, and I could not read the full text.
- So the 36 W power match and the force balance in the same abstract do not point at the same A_pp. The power match
  (36.3 W at 2.6 cm) holds. The force balance implies a smaller amplitude than the one the taxi needs. The two may differ
  because Deng's CFD body may sit partly in the water with more drag; that is unknown at abstract level.

## 5. Comparison with the recorded value (read only after §4 was fixed)

S32 §4.2 records the following.
- 2.6 cm const: −1.10 N at 10 m/s, decelerates to 7.0 m/s.
- 2.6 cm scaled: reaches 15.0 m/s in 4.4 s / 59 m / 221 strokes.
- 3.1 cm scaled: 1.3 s / 16 m / 64 strokes.
- The constant-C_D ceiling is 7–9 m/s, the 300 g scaled equilibrium is 15–20 m/s, and the power at 10 m/s is 36 W.

**My numbers compared with these:**
- My S32-convention variant gives 6.95 m/s, 4.50 s / 60.5 m / 225 strokes, and 1.28 s / 16.3 m / 64 strokes, which matches within about 2–3 %.
- My own grid (ρ 1025, Re_ref 4,780) gives 1.0–1.2 s for the 3.1 cm case and a const ceiling of 6.8–8.6 m/s.
- My power is 36.3 W against 36 W.

**AGREE** on the numbers and on the qualitative split (const C_D fails, scaled succeeds). Three caveats S32 does not state:
1. S32 attributes the Re span 4,780–9,560 to the pitching law. The full text says pitch was measured at 60 mm/s only
   (Re 4,780). This barely changes the result (≈ 1.0 vs 1.3 s).
2. The 2.6 cm scaled case is fragile. With CD0 0.20 it does not reach V_to at either mass (191 g stalls at 13.8 m/s
   under S32 conventions; 300 g stalls at 15.6 m/s on my grid). The pass is not robust across S32's own stated CD0 range.
3. S32's "escape" amplitude for constant C_D (A_pp ≥ 3.5 cm) is roughly the amplitude needed to *hold 10 m/s*
   (3.7–3.8 cm in my scan). *Reaching* V_to under constant C_D needs 5.4–6.2 cm.

Neither caveat changes the agreement on the recorded value. Both bear on how much "validates against a real animal" can carry:
in my reading it is a consistency check against a second-hand speed report and a CFD abstract, not a validation against observation.

**Negative-search scope.** I did not search for primary observational flying-fish taxi kinematics (tail amplitude, the
time course of speed). The 15–20 m/s figure stays at search-summary level. I could not read Fish 1990's PDF myself; it was
not attempted this session, and S32 reports it outside the allowed domains.

```swarm-replication
{"claim_id": 273, "my_value": "191 g exocoetid from 10 m/s: scaled-C_D reaches V_to 15.0 m/s in 1.0-1.3 s / 13-16 m at A_pp 3.1 cm (2.1-4.5 s at 2.6 cm; fails below A_pp ~2.1-2.8 cm); const-C_D decelerates to ~7-8.6 m/s; taxi power 36.3 W at 10 m/s (all calculated)", "agrees": true,
  "note": "Reproduced S32 sec 4.2 within ~3% (6.95 m/s; 4.50 s/60.5 m/225 strokes; 1.28 s/16.3 m/64 strokes; 36.3 W), but the 'validation' rests on an assumed A_pp, a second-hand speed report and a CFD abstract whose 10 m/s force balance implies a smaller amplitude than the taxi needs."}
```
