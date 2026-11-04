# S32: Multi-stroke launch. Can an airborne-body taxi take the designed zebrafish from exit speed to glide speed?

**Status:** derived. These are equations of motion integrated on stated inputs, with literature read-levelled below. **Nothing in this document is a new measurement.**
Reproduce every number with `python3 docs/research/fish/S32_taxi.py` (RK4, about 6 s).

**Depends on:**
- S28 (`claude/s28-organism-design-5z0vjz`): the designed wing (case C: 192 mm², AR 5, CL_max 1.07), the 24 mm² frontal area, and the 1.38 m/s burst.
- S24 (`claude/s24-surface-taxiing-launch-tsepbn`): the 52 Hz maximum, the caudal fin length, and the guppy data.
- S29 (`claude/s29-launch-energy-2iuixr`): the body drag coefficient range in water.
- S30 (`claude/s30-launch-budget-mass-k71prf`): the reframing that real gliders launch over many strokes.
- The project's transcription of Fish 1990 Tables I–II (`connectors/fish_controls/fish1990.py` on `main`).

## 0. Short answer

**A multi-stroke launch does not reopen the flight question for this organism. It closes it for a different reason, and that reason is better founded than either earlier one.**

1. **Step 3 first: does thrust exceed drag at the exit speed?**
   - **At 1.38 m/s, yes.** Leaving the water drops body drag 816-fold, from 4.6 mN to 8 µN. The immersed lobe then makes 1.1–3.4 mN of thrust against 0.09–0.43 mN of total drag, in the generous and central cases. **Speed really does increase.** The first stroke adds about 0.26 m/s.
   - **At 0.45 m/s, the question is moot.** At that speed the wing carries 1 % of the weight. The immersed lobe would need a vertical lift coefficient of 1.3–10 to hold the body out of the water. The minimum speed at which the lobe can support the body (CL ≤ 1) is 0.51–1.39 m/s. The body falls back in, and the "taxi" becomes ordinary surface swimming.
2. **From 1.38 m/s the taxi accelerates and then stalls.**
   - It reaches an **equilibrium of 2.2–2.9 m/s, which is 50–65 % of the 4.41 m/s glide speed.** There the wing carries 25–43 % of the weight.
   - In the generous case it gets within 1 % of that speed after **about 30–38 strokes (0.6–0.7 s, about 1.5–2 m)**. It never reaches glide speed.
   - For a 0.40 g fish (V_to 5.58 m/s) the ceiling is the same, about 2.9 m/s, so the shortfall is larger.
3. **What sets the ceiling.** Measured flapping-foil thrust scales as (f·A)², set by tail speed and independent of forward speed U. The foil's own drag scales as C_D·U². Their ratio fixes a hard taxi ceiling:
   **U_max = f·A_pp·√(c₆/C_D(Re)).** Here c₆ = 2.55 and C_D = 0.08 are measured at Re 4,780–9,560 (Floryan et al. 2017). The immersed area cancels out of U_max. Mass barely matters.
4. **Why it works for a flying fish and not for a zebrafish.**
   - Both animals have the **same tail-speed-to-glide-speed ratio**, f·A_pp/V_to = 0.09–0.10.
   - What differs is **C_D at the lobe's Reynolds number**: about 0.06–0.08 at Re ~10⁴ for the zebrafish lobe, against about 0.010–0.011 at Re ~3×10⁵ for the exocoetid lobe.
   - That gives U_max/V_to = **0.58–0.68 for the zebrafish** and **1.3–1.5 for the exocoetid**.
   - Run with Re-independent C_D, the same equations say a flying fish **cannot** taxi from 10 m/s, because the ceiling is 7–9 m/s. Flying fish are reported to accelerate while taxiing (secondary source only), so that is evidence the Re dependence is real.
   - **The size argument returns, but as a Reynolds-number property of the taxi's propulsor, not as a single-impulse energy budget.**
5. **How far short.** To reach glide speed, the airborne tail would need **1.38–1.77× the tail speed f·A_pp of the fish's best measured burst** (0.25 g), or **1.66–2.24×** (0.40 g). At the measured 52 Hz that means A_pp ≈ 12–19 mm (0.4–0.6 SL). At burst amplitude it means **72–117 Hz**.
   - This agrees independently with S24's 49–98 Hz, and it is now derived from a measured thrust law and not from a cruise Strouhal band.
   - If the shortfall were met, the taxi would close in only 3–14 strokes (0.05–0.26 s, 0.16–0.94 m). The barrier is the ceiling, not the run length.

---

## 1. Equations of motion for the taxi phase

**Configuration.** The body and the spread pectoral wing are in air. Only a fraction φ of the lower caudal lobe is in water, area S_imm = φ·S_lobe and depth d. The lobe oscillates at frequency f with peak-to-peak tip excursion A_pp. U is horizontal speed.

**Horizontal:**

  m dU/dt = T_lobe − D_wing − D_body,air − D_ind,lobe − F_σ,h

  T_lobe = ½ρ_w S_imm [ G − C_D(Re_c) U² ],  G = κ·c₆·(f A_pp)²

This is Floryan et al. 2017's pitching-foil law, C_T = c₆ St² − C_D with St = f A_pp/U, rewritten so that U appears only in the drag term. κ is a 3-D, free-surface and flexibility correction, with κ = 1 for the measured 2-D rigid foil.

**Vertical (the body must be held out of the water):**

  L_wing + F_z,lobe = W + F_σ,v

- **Wing.** L_wing = ½ρ_a S_w U² CL, with CL = min(CL_max, W/(½ρ_a S_w U²)). Wing drag is D_wing = ½ρ_a S_w U² (CD0 + k CL²), with k = 1/(π·0.8·5). This is S28's wing.
- **Lobe vertical force.** F_z,lobe = ½ρ_w U² S_imm CL_z, with the constraint **CL_z ≤ 1**. If the constraint fails, the body cannot be held airborne.
  - The lobe pays induced drag D_ind = ½ρ_w U² S_imm CL_z²/(π·0.8·AR_eff).
  - AR_eff = 2d²/S_imm, using the free-surface mirror image.
- **Surface tension.**
  - Meniscus pull-down: F_σ,v = 2σc·cosθ.
  - Contact-line hysteresis drag bound: F_σ,h = 2σc·Δcosθ.
- **Body in air.** D_body,air = ½ρ_a·0.3·A_front·U².

The script integrates dU/dt with fourth-order Runge–Kutta at dt = 20 µs. It stops when U reaches V_to, when CL_z exceeds 1, when |a| drops below 1 mg (equilibrium), or at t = 3–5 s.

**Not modelled.** Each of these makes the result worse for the taxi, or has unknown sign.
- Spray, ventilation and wave drag on the piercing lobe. Their effect is folded into κ < 1 as a sensitivity.
- Yaw recoil. In air the body has no water to react against the lobe's lateral force. This lowers the effective amplitude.
- The zebrafish lobe has no hypocercal cant, so vertical force on it competes with lateral thrust.
- Unsteady vertical dynamics. The support constraint is applied quasi-steadily.

## 2. The key quantities: measured or assumed

### Read levels
- **FULL**: full text read this session.
- **VIA Sxx**: inherited from a sibling document at its stated read level.
- **PROJECT-TRANSCRIBED**: transcribed from page images by earlier project work.
- **ABSTRACT**: the abstract only, via Europe PMC.
- **SEARCH-EXTRACT**: a search-engine summary only.
- **ASSUMED**: chosen by me, with sensitivity reported.

| Quantity | Value | Status |
|---|---|---|
| Thrust law for an oscillating foil | C_T = **2.55 St² − 0.08** (pitching). Heave: 3.52 St² + 3.69 St² f\*U\* − 0.15. Rigid teardrop foil, c 80 mm, AR 3.5, effectively 2-D. **Re 4,780–9,560**; the dimensional thrust and the coefficients are unchanged across this 2× range in velocity | **Measured.** Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.* (arXiv 1704.07478v1), **FULL** (arXiv v1; published version not read) |
| Max tail-beat frequency | **52 Hz**: an EMG maximum during escape, not shown to be sustainable | **Measured.** Kyriakatos 2011, VIA S24 (full text) |
| Thrust per stroke | Not measured anywhere for adult zebrafish (S24 §2.4). **Calibrated here:** at the peak of the measured 1.38 m/s burst dU/dt = 0, so whole-caudal-fin thrust = body water drag (Cd 0.1–0.3 on 24 mm², from S29). This gives **G = 0.27–0.52 m²/s²**, equivalent to f·A_pp = 0.33–0.45 m/s, i.e. A_pp = 6.3–8.6 mm at 52 Hz. It assigns *all* burst thrust to the tail, which is generous | **Derived** from measured burst + measured thrust law + assumed body Cd |
| Cross-check | A kinematic A_pp of 8 mm (0.2 L, a generic fish value at SEARCH-EXTRACT level) gives a predicted in-water burst maximum of **1.46 m/s**, against the measured 1.38 m/s | consistency, not validation |
| Caudal fin chord | 6 mm (fin length 5.6–6.5 mm) | **Measured.** Wakamatsu 2019, VIA S24 (full text) |
| Caudal fin height and area | Height 9 mm (0.3 SL); area 0.7·c·h = **37.8 mm²**; lower lobe 18.9 mm². No adult zebrafish fin area was found (searched; regeneration papers report normalised areas) | **ASSUMED** |
| Immersed fraction φ of the lower lobe | 0.25 / 0.5 / 1.0 | **ASSUMED.** Never measured for any fish |
| Lift the wing contributes | (U/V_to)² of W up to V_to = **4.41 m/s** (0.25 g) or **5.58 m/s** (0.40 g). S28 quoted 4.37 m/s; the script's 4.41 m/s is S28's own case-C value | derived (S28 wing, itself unmeasured: case C is an extrapolation) |
| Wing drag | CD0 0.08–0.20, k = 0.0796 | ASSUMED (S28) |
| Drag, water vs air, body | 4.57 mN in water (Cd 0.2) vs **8.4 µN** in air at 1.38 m/s; ρ_w/ρ_a = 816 | derived |
| Lobe C_D outside 4,780–9,560 | (a) held at 0.08 ("const"), or (b) scaled as Re^−½ outside the measured span ("scaled", laminar friction) | **ASSUMED extrapolation.** It matters little for the zebrafish (Re 2.7k–26k) and decisively for the exocoetid (Re 2.5–4×10⁵) |
| Lobe CL_z,max | 1.0 | ASSUMED |
| Surface tension | σ = 0.072 N/m. cosθ 0–1 and Δcosθ 0–0.3 are ASSUMED (the wettability of fin mucus was not read). Bound 2σc = 0.86 mN = **35 % of W** (0.25 g) | physical constant + assumed angles |
| Exocoetid hypocaudal lobe area | 0.003·M^0.650 m², which is 10.2 cm² at 191 g and 13.7 cm² at 300 g | **Measured allometry.** Fish 1990 Table I, PROJECT-TRANSCRIBED |
| Exocoetid wing loading | WL = 285.0·M^0.400, giving V_to 15.0 m/s (191 g) and 16.4 m/s (300 g) | Fish 1990 Table II, PROJECT-TRANSCRIBED; CL_max 1.07 assumed |
| Exocoetid taxi kinematics | 50 Hz; 15° deflection; 0.25 m, 0.191 kg; **36 W for steady taxi at 10 m/s**; 16.5 m/s at 350 W | **ABSTRACT** (Deng, Wang, Zhang & Mao 2019, bioRxiv 765560: CFD, *simulated*). Full text returned HTTP 429 or exceeded the size limit on six attempts |
| Exocoetid lobe length and A_pp | lobe 4–6 cm, giving A_pp = 2·l·sin15° = 2.0–3.1 cm; chord 2.5 cm | **ASSUMED** |
| Exocoetid exit and taxi speeds | ~10 m/s exit, 15–20 m/s after taxi | SEARCH-EXTRACT (via S30) |
| Guppy, small-fish analogue | 1.02 m/s in water → **1.24 m/s** in air, with tail beats continuing out of water | Soares & Bierman 2013, VIA S24 (full text) |

**Network limits this session:** cambridge.org (JFM published version), health-sciences.wcupa.edu (the Fish 1990 PDF), theses-dissertations.princeton.edu (flying-fish taxi robot thesis) and meetings-archive.aps.org (APS 2024 taxiing abstract) were outside the allowed domains. bioRxiv rate-limited.

## 3. Does it close for a zebrafish?

### 3.1 Step 3 first: net force at the exit speed

| Scenario | U0 | T_lobe | D_wing | D_ind,lobe | F_σ,h | **Net** | Wing lift | Lobe CL_z needed |
|---|---|---|---|---|---|---|---|---|
| GENEROUS (Cd_b 0.3, φ 1, C_D scaled, CD0 0.08, no surface tension, 0.25 g) | 1.38 | 3.43 mN | 0.04 | 0.05 | 0 | **+3.33 mN** | 9.8 % | 0.12 |
| | 0.45 | 4.66 | 0.00 | 0.57 | 0 | +4.09 | 1.0 % | **1.27 → support fails** |
| CENTRAL (0.2, 0.5, scaled, 0.12, cosθ 0.5, Δcos 0.1, 0.25 g) | 1.38 | 1.14 | 0.05 | 0.29 | 0.09 | **+0.71** | 9.8 % | 0.29 |
| | 0.45 | 1.76 | 0.01 | 3.17 | 0.09 | −1.50 | 1.0 % | **2.99 → fails** |
| STINGY (0.1, 0.25, const, 0.20, cosθ 1, Δcos 0.3, 0.40 g) | 1.38 | 0.29 | 0.07 | 3.42 | 0.26 | **−3.46** | 6.1 % | **1.01 → fails** |
| | 0.45 | 0.61 | 0.01 | 35.2 | 0.26 | −34.9 | 0.6 % | 9.95 → fails |

**Reading it:**
- At 1.38 m/s, in the generous and central cases, **thrust exceeds drag by 3–40×. The taxi is not killed at step 3.**
- At 0.45 m/s it is killed. The problem is not thrust but **weight support**: a 5–19 mm² lobe at a dynamic pressure of 100 Pa cannot carry 2.5–3.9 mN. This is a size effect. The weight-to-area ratio of a lobe grows as L, and the meniscus pull-down, which bounds at 22–35 % of W, grows as 1/L² relative to weight.
- The minimum speed for lobe support (CL_z = 1) is **0.51 / 0.77 / 1.39 m/s** (generous / central / stingy).

### 3.2 The integrated trajectory from 1.38 m/s (GENEROUS, 0.25 g, V_to 4.41 m/s)

| Stroke | t (ms) | x (cm) | U (m/s) | T (mN) | Net (mN) | Wing lift |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1.38 | 3.43 | +3.33 | 9.8 % W |
| 2 | 38 | 6.2 | 1.82 | 2.53 | +2.43 | 16.9 % |
| 4 | 77 | 13.8 | 2.14 | 1.89 | +1.76 | 23.4 % |
| 6 | 115 | 22.5 | 2.37 | 1.39 | +1.25 | 28.7 % |
| 10 | 192 | 41.9 | 2.64 | 0.78 | +0.60 | 35.7 % |
| 20 | 385 | 95.2 | 2.84 | 0.29 | +0.09 | 41.5 % |
| 30 | 577 | 150 | 2.87 | 0.22 | +0.01 | 42.4 % |
| → | 733 | 195 | **2.88 (equilibrium)** | — | 0 | 42.5 % |

**The speed increases, and that is not trivial.** Two observations support it:
- It agrees in sign with the guppy, which gains 22 % in air while still beating its tail.
- It doubles the speed in about 10 strokes.

**But the speed asymptotes.** Thrust falls as U² while the drag it must overcome stays roughly constant, because the support drag falls as the wing unloads. Net force approaches zero at **2.88 m/s = 65 % of V_to**.

| Scenario | Outcome from 1.38 m/s | U_end | Time | Distance | Strokes | Wing lift at end |
|---|---|---|---|---|---|---|
| GENEROUS 0.25 g | stalls | 2.88 | 0.73 s | 1.95 m | 38 | 42.5 % |
| CENTRAL 0.25 g | stalls | 2.19 | 1.42 s | 2.91 m | 74 | 24.6 % |
| STINGY 0.40 g | support fails at exit | — | — | — | 0 | 6.1 % |
| any, from 0.45 m/s | support fails at exit | — | — | — | 0 | ≤ 1 % |

Strokes are counted at 52 Hz. Whether 52 Hz can be held for 38–74 strokes is unknown (S24).

### 3.3 Sensitivity of the ceiling (one factor at a time, from GENEROUS)

| Factor | Values → U_eq (m/s) |
|---|---|
| Body Cd used in thrust calibration | 0.1 → 1.89; 0.2 → 2.41; 0.3 → 2.88 |
| Immersed fraction φ | 0.25 → 2.46; 0.5 → 2.79; 1.0 → 2.88 |
| Lobe C_D extrapolation | const → 2.50; scaled → 2.88 |
| Wing CD0 | 0.08 → 2.88; 0.20 → 2.83 |
| Meniscus cosθ | 0–1 → 2.88 (support is cheap at 2–3 m/s) |
| Hysteresis Δcosθ | 0 → 2.88; 0.3 → 2.78 |
| Body mass | 0.25 g → 2.88; 0.40 g → 2.87 (but V_to rises to 5.58) |
| κ (3-D / ventilation) with kinematic A_pp 8 mm | κ 1 → 2.60; κ 0.5 → 1.63 |
| Kinematic A_pp at 52 Hz, κ 1 | 6 mm → 1.77; 8 → 2.60; **12 → 4.43**; 15 → 6.01 |

**Thrust multiplier needed on the burst-calibrated G for U_eq = V_to:**

| Mass | C_D scaled | C_D const |
|---|---|---|
| 0.25 g | ×1.92 (f·A_pp ×1.38) | ×3.13 (×1.77) |
| 0.40 g | ×2.74 (×1.66) | ×5.00 (×2.24) |

**No assumed parameter within its stated range lifts the ceiling to V_to.** Only one thing does: an airborne tail moving its lobe **1.4–2.2× faster laterally than the fish's tail moves in its best measured all-out burst**. That is 12–19 mm peak-to-peak at 52 Hz, or 72–117 Hz at burst amplitude.

The kinematic row at 12 mm and κ = 1 reaches 4.43 m/s. That needs both of these together:
- an amplitude 1.4× the calibrated one;
- a lobe with no 3-D or ventilation loss.

**If the multiplier were available** (×2–×4), the taxi would reach glide speed in **14 / 6 / 4 / 3 strokes** (0.26 / 0.12 / 0.09 / 0.05 s; 0.94 / 0.39 / 0.27 / 0.16 m). Strokes and distance are not the limit. **The ceiling is.**

## 4. Why it works for a 300 g exocoetid and may not for a 0.4 g zebrafish

### 4.1 Term by term

The same equations and the same measured foil law are used throughout. Exocoetid geometry comes from Fish 1990, with assumed kinematics.

| Term | Zebrafish 0.25–0.40 g | Exocoetid 191–300 g | Scaling and consequence |
|---|---|---|---|
| Tail speed / glide speed, f·A_pp/V_to | 0.095–0.103 | 0.087–0.095 (assumed A_pp) | **≈ size-independent.** Not the discriminator |
| Lobe Re | 8×10³ at exit; 2.6×10⁴ at V_to | 2.5–4×10⁵ | ∝ L·U. Zebrafish within 3× of the measured span; exocoetid 26–42× outside it |
| Lobe C_D | 0.06–0.08 | 0.010–0.011 (scaled); 0.08 if held const | **The discriminator.** U_max ∝ C_D^−½ |
| Foil ceiling U_max/V_to | **0.58–0.68** | **1.31–1.52** (scaled); 0.49–0.53 (const) | — |
| Meniscus 2σc / W | 22–35 % | 0.19 % | ∝ L⁻² |
| Weight / (lobe area · ½ρU_exit²) | needs CL_z 0.12–1.0 at 1.38 m/s; 1.3–10 at 0.45 m/s | CL_z ≈ 0.04 at 10 m/s | ∝ L/U². High exit speed makes support trivial |
| Body drag collapse on exit | ×816 | ×816 | size-independent; helps both equally |
| Exit-speed lift fraction | 1–10 % | 44 % (10/15)², 37 % (10/16.4)² | the flying fish starts with the wing far more loaded |

### 4.2 The flying fish run with the same equations

M = 191 g with φ = 0.5:

| A_pp | C_D | Net at 10 m/s | Outcome | Time / distance / strokes |
|---|---|---|---|---|
| 2.6 cm | const | **−1.10 N** | decelerates to 7.0 m/s | — |
| 2.6 cm | scaled | +0.55 N | reaches 15.0 m/s | 4.4 s / 59 m / 221 |
| 3.1 cm | scaled | +1.01 N | reaches 15.0 m/s | 1.3 s / 16 m / 64 |

The 300 g fish behaves the same way (U_eq 15–20 m/s scaled, 7–8 m/s const).

**Power cross-check against Deng 2019.** Floryan's pitching power law (c₈ 7.78, c₉ 4.89) at 10 m/s, 50 Hz, A_pp 2.6 cm and φ 0.5 gives **36 W**. That matches Deng's abstract CFD value of 36 W for steady taxi at 10 m/s. φ and A_pp are assumed, so this is a consistency check, not a calibration.

**What this shows.** With the Reynolds-number dependence of foil drag removed, the model predicts that a flying fish cannot taxi. Flying fish are reported to taxi from about 10 m/s to 15–20 m/s (secondary source) and are simulated to do so (Deng, abstract). The constant-C_D branch is therefore contradicted for large fish. The scaled branch:
- reproduces a 15–20 m/s ceiling for exocoetids;
- leaves the zebrafish at 0.58–0.68 V_to.

So the Reynolds-number effect the brief anticipated is the actual mechanism. **The size argument legitimately returns, as a property of the taxi.**

**The one escape** from this reading would be that flying fish tail amplitudes are much larger than assumed (A_pp ≥ 3.5 cm at 50 Hz with C_D constant). That would put the discriminator back on kinematics, not Re. Measured exocoetid taxi kinematics were not readable this session, which leaves this the main open alternative.

## 5. Verdict

**The multi-stroke launch closes the question. It does not reopen it.**

**Why this closure is better founded than S28 or S29:**
- S28 (wing) and S29 (single-impulse energy) both modelled a mode that real gliders do not use (S30).
- S32 models the mode they do use. It uses a thrust law measured at the zebrafish lobe's own Reynolds number. Its thrust is calibrated to the zebrafish's own measured burst, not to an invented coefficient.
- Applied unchanged, the same model reproduces the exocoetid taxi: both its 15–20 m/s ceiling and Deng's 36 W.

**What the closure says:**
- A zebrafish-sized taxi **does accelerate**, doubling speed in about 10 strokes. It **stalls at 2.2–2.9 m/s, 50–65 % of glide speed**.
- The stall is set by U_max = f·A_pp·√(c₆/C_D(Re)), whose C_D at Re ~10⁴ is 5–7× a flying fish's.
- From the low-end exit speed (0.45 m/s) the body cannot be held out of the water at all.

**What would reopen it.** The barrier is narrow but real: **1.4–2.2× more lobe tail-speed in air than the animal produces in its best burst.** This is a kinematic-physiology quantity, not a wing quantity. It is the same quantity S24 identified (49–98 Hz needed), now with a physical drag model behind it. Two measurements would decide it:
1. **Thrust of a partially immersed, oscillating caudal lobe at Re 10⁴–3×10⁴** (a zebrafish-scale robotic or excised lobe in a flume at 1–4 m/s, φ 0.25–1). This tests c₆, C_D and κ in the surface-piercing case. **It is the term the result hangs on.**
2. **Tail-beat frequency × amplitude achievable with the body out of the water.** Filming the guppy-like aerial tail beats of adult zebrafish would do it. **The result reopens only if f·A_pp ≥ 0.62–1.0 m/s**, against 0.33–0.45 m/s implied by the burst.

## 6. Honesty ledger

- **Measured, by others:**
  - Floryan 2017 thrust and power coefficients and C_D (FULL, arXiv v1).
  - 52 Hz; caudal fin length 5.6–6.5 mm; 1.38 m/s burst; guppy in-air acceleration (all VIA S24/S28).
  - Exocoetid hypocaudal area and wing loading allometries (PROJECT-TRANSCRIBED).
  - Deng 2019 CFD outputs (ABSTRACT, simulated, not observed).
  - Exocoetid taxi 10 → 15–20 m/s (SEARCH-EXTRACT).
- **Derived here:**
  - The equations of motion and every trajectory.
  - The burst-calibrated thrust parameter G.
  - The support-failure speeds, the ceiling formula, the multipliers, the power cross-check.
- **Assumed:**
  - Caudal fin height and area.
  - Immersed fraction φ.
  - Lobe CL_z,max = 1 and Oswald factor 0.8.
  - κ.
  - The C_D extrapolation outside Re 4,780–9,560.
  - Contact angles.
  - Wing CD0.
  - Body Cd in the calibration.
  - Exocoetid lobe length, chord and A_pp.
  - That airborne tail kinematics equal burst kinematics; the multiplier table states what is needed if they do not.
- **Not invented:** no thrust coefficient, immersed area or efficiency is fitted to make anything pass. The thrust law is Floryan's as printed. Every free parameter is swept and reported in §3.3.
- **Weakest links:**
  1. The rigid 2-D foil is used for a flexible, surface-piercing, low-AR lobe. κ is unknown: flexibility may raise it, ventilation and finite span lower it.
  2. The exocoetid kinematics are assumed, so the Re-versus-amplitude attribution in §4.2 is inferred, not measured.
  3. Whether 52 Hz can be sustained at all is open.

```swarm-result
subproblem: S32
evidence: derived (equations of motion for the airborne-body/immersed-lobe taxi integrated by RK4, script docs/research/fish/S32_taxi.py) on - FULL: Floryan, Van Buren, Rowley & Smits 2017 JFM (arXiv 1704.07478v1) measured oscillating-foil law C_T = 2.55 St^2 - 0.08 (pitch), 3.52 St^2 + 3.69 St^2 f*U* - 0.15 (heave), Re 4780-9560, coefficients unchanged over 2x velocity; VIA S24 (full text): Kyriakatos 2011 52 Hz escape max, Wakamatsu 2019 caudal fin length 5.6-6.5 mm, Soares & Bierman 2013 guppy 1.02 -> 1.24 m/s with aerial tail beats; VIA S28: 1.38 m/s burst, designed wing 192 mm2 AR5 CLmax 1.07, 24 mm2 frontal area; PROJECT-TRANSCRIBED: Fish 1990 Table I hypocaudal area 0.003 M^0.650 m2, Table II WL 285 M^0.400; ABSTRACT: Deng et al. 2019 bioRxiv 765560 CFD taxi 36 W at 10 m/s, 50 Hz, 15 deg (simulated); SEARCH-EXTRACT: exocoetid exit ~10 m/s, taxi to 15-20 m/s; ASSUMED (swept): caudal fin height/area, immersed fraction, lobe CLz_max, kappa, C_D extrapolation outside measured Re, contact angles, exocoetid lobe kinematics
answer: Step 3 (thrust > drag at exit) PASSES at the 1.38 m/s exit: leaving water cuts body drag 816x (4.6 mN -> 8 uN) and the burst-calibrated lobe thrust (1.1-3.4 mN) exceeds total drag 3-40x, so speed genuinely rises (doubling in ~10 strokes at 52 Hz). It FAILS at 0.45 m/s, on weight support not thrust: the lobe would need CL 1.3-10 to hold the body out of the water (minimum supportable speed 0.51-1.39 m/s). From 1.38 m/s the integrated taxi stalls at 2.19-2.88 m/s = 50-65% of the 4.41 m/s glide speed (wing carrying 25-43% W), within 1% of equilibrium after ~30-38 strokes (~0.6-0.7 s, ~1.5-2 m) in the generous case; the 0.40 g fish (V_to 5.58) stalls at the same speed. The ceiling is U_max = f*A_pp*sqrt(c6/C_D(Re)): measured foil thrust scales with tail speed squared, independent of U, while foil drag scales as U^2; immersed area and mass drop out. Zebrafish and exocoetids share f*A_pp/V_to ~0.09-0.10; they differ in lobe C_D at Re ~1e4 (0.06-0.08) vs ~3e5 (~0.01), giving U_max/V_to 0.58-0.68 vs 1.3-1.5. The same equations reproduce the exocoetid taxi (reaches 15 m/s; Deng's 36 W) only with Re-dependent C_D; with constant C_D a flying fish could not taxi at all, so the Re effect is the operative size argument, now a property of the taxi. Closure would need 1.38-2.24x the tail speed of the best measured burst (A_pp 12-19 mm at 52 Hz, or 72-117 Hz at burst amplitude), consistent with S24's 49-98 Hz; given that, the run is short (3-14 strokes, 0.16-0.94 m).
key_number: taxi stalls at 2.2-2.9 m/s = 50-65% of glide speed (4.41 m/s) from a 1.38 m/s exit; closure needs 1.4-2.2x the lobe tail-speed f*A_pp of the best measured burst; ceiling U_max = f*A_pp*sqrt(2.55/C_D(Re)), lobe C_D ~0.06-0.08 at zebrafish Re ~1e4 vs ~0.01 at exocoetid Re ~3e5
verdict: NEGATIVE, better founded - multi-stroke launch closes rather than reopens the question: the taxi accelerates but has a Reynolds-number-set speed ceiling well below glide speed, and from the low-end exit the body cannot even be supported; reopens only if an airborne zebrafish lobe can be shown to beat at >=1.4-2.2x its burst tail speed, or if surface-piercing lobe thrust at Re 1e4 measures well above the 2-D foil law
depends_on: [S28, S24, S29, S30, Floryan2017-foil-scaling, Kyriakatos2011-52Hz, Wakamatsu2019-fin-length, Miln2021-burst, Soares-Bierman2013-guppy, Fish1990-tables, Deng2019-taxi-CFD]
```
