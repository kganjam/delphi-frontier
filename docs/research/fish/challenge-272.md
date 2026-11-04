# Challenge 272: the S32 claim that a Reynolds-number size effect sets the taxi limit

**Claim under review (S32, commit `c1b761eb` on `origin/claude/s32-multi-stroke-launch-qpq9g2`, file `docs/research/fish/S32-organism.md`, §0 item 4 and §4):**
> "The size argument returns, correctly located. Zebrafish and exocoetids share f·A_pp/V_to at 0.09–0.10. They differ ONLY in lobe C_D at their Reynolds number: 0.06–0.08 at Re ~1e4 against ~0.01 at Re ~3e5. That gives U_max/V_to of 0.58–0.68 versus 1.3–1.5. The barrier is a property of the TAXI, not of the single impulse that S29 wrongly blamed."
> Recorded: evidence level *derived*, value 0.63 U_max/V_to.

**Verdict: WEAKENED.**
- The zebrafish half survives as a negative result, and it is more robust than S32 says.
- The exocoetid half, and with it the word "ONLY" and the causal attribution to C_D(Re), is not identified by the evidence.
- The 0.63 value is the midpoint of the *generous* calibration case only. Over the stated body-drag range, the zebrafish ceiling is 0.44–0.67 V_to.

Everything below is my own **calculation** on S32's stated inputs, using the scripts described. **None of it is an observation.** Literature read levels are given beside each source.

---

## 1. Arithmetic redone independently

**Zebrafish: a closed form that S32 does not state.**
- S32 calibrates G = (Cd_b·A_front/S_c + C_D)·U_b², where U_b is the burst speed. The foil-only ceiling is U_max = √(G/C_D).
- Substituting gives **U_max = U_b·√(1 + Cd_b·A_front/(S_c·C_D))**.
- **c₆ cancels.** The zebrafish ceiling therefore does not depend on Floryan's thrust coefficient or on f·A_pp at all. It is the measured burst speed multiplied by a ratio of body drag to fin parasitic drag. f·A_pp is a quantity back-computed from the calibration, and here it acts as a proxy (see §2).

My iterated values, with C_D scaled as Re^−½ outside the measured span, A_front 24 mm², S_c 37.8 mm², U_b 1.38 m/s and V_to 4.41 m/s:

| Cd_b (S29 range) | f·A_pp/V_to | U_max (m/s) | U_max/V_to |
|---|---|---|---|
| 0.1 | 0.074 | 1.94 | **0.44** |
| 0.2 | 0.089 | 2.48 | **0.56** |
| 0.3 | 0.102 | 2.96 | **0.67** |

- With C_D held constant at 0.08, Cd_b 0.3 gives 2.54 m/s, which is 0.58 V_to. This reproduces S32's 0.58–0.68 band.
- That band, and its midpoint 0.63, is the **Cd_b = 0.3 (GENEROUS) case only**. The claim presents it as the result.
- f·A_pp/V_to = 0.09–0.10 likewise holds only for Cd_b 0.2–0.3. At Cd_b 0.1 it is 0.074.
- **Direction:** every relaxation makes the zebrafish result *more* negative. The zebrafish half survives.

**Exocoetid:**
- I reproduce S32's §7 numbers: 191 g, A_pp 2.6 cm, 50 Hz gives f·A_pp/V_to 0.087 and U_max/V_to 1.31 with C_D iterated to 0.0112. For 300 g at 3.1 cm the figures are 0.095 and 1.52.
- The quantity that decides it is the lobe C_D at V_to. For a 191 g fish at A_pp 2.6 cm and 50 Hz, the taxi reaches V_to only if **C_D(Re ≈ 3.7×10⁵) ≤ c₆·(f·A_pp/V_to)² = 0.019**. The figure is 0.016 for a 300 g fish at 2.6 cm.
- That requirement is **≤ 20–24 % of the only measured value**, 0.08 (Floryan et al. 2017, Re 4,780–9,560).
- The script running S32's inputs reproduces their trajectory table: const C_D stalls at 7.0 m/s; scaled C_D reaches 15 m/s in 4.4 s.

**Arithmetic verdict:** no arithmetic error. The numbers are reproduced from S32's inputs.

## 2. Proxy check

- **For the zebrafish,** "f·A_pp" is not an independent tail-speed measurement. It is inferred from the burst speed and an assumed Cd_b, so "sharing" f·A_pp/V_to with the exocoetid compares an inferred quantity with an assumed one.
- **The quantity that matters** for the zebrafish is the ratio of body drag to fin parasitic drag at burst (§1). For the exocoetid it is the C_D at V_to that the lobe can actually achieve.
- **For the exocoetid,** f = 50 Hz and the 15° deflection are Deng et al. 2019's CFD *minimum-power operating point*. That is a simulation result read at ABSTRACT level by S32, not a measured tail-beat frequency. A_pp = 2–3.1 cm is ASSUMED (S32's own ledger).
- The exocoetid side of "share f·A_pp/V_to at 0.09–0.10" is therefore **an input chosen by S32, not a finding**.

## 3. Hidden assumption carrying the result: the attribution is circular and under-identified

The exocoetid comparison has **two unknowns**:
- the lobe kinematics, f·A_pp;
- C_D at Re 2.5–4×10⁵, which is 26–42× beyond the measured span.

It has **one constraint**: flying fish are reported to taxi (secondary source).
- S32 fixes the kinematics by assumption, then selects the Re^−½ branch *because* it lets the flying fish taxi.
- It then cites the taxi as "evidence that the Re dependence is real". This is calibration presented as confirmation.
- S32's own §4.2 concedes the alternative: A_pp ≥ 3.5 cm with constant C_D is "the main open alternative".
- The claim as recorded drops that caveat and says "ONLY". **The word "ONLY" is not supported.**

**Relaxing the C_D extrapolation (my inference, from my calculation):**
- Floryan's C_D of 0.08 at Re ≈ 7,000 is about 2.5× the Blasius two-sided flat-plate friction at that Re (0.032, my calculation). So roughly 0.05 of it is form/pressure drag on a thick teardrop foil, which need not scale as Re^−½.
- At Re 3×10⁵, two-sided turbulent flat-plate friction alone is 0.012 (my calculation, 0.074·Re^−0.2 per side). That is already at the 0.011 that S32 extrapolates, with no form drag left over.
- If any form drag above about 0.007 survives, the exocoetid fails the 0.016–0.019 threshold under S32's own kinematics.
- Holding C_D at its value at the edge of the Senturk–Smits simulated range, Re 3.2×10⁴ (C_D ≈ 0.044), gives exocoetid U_max/V_to = 0.47–0.79 across A_pp 2.0–3.1 cm. That is the same "fails" regime as the zebrafish.
- **The Re branch is therefore fragile in exactly the direction that would erase the discriminator.**

**Partial support for S32 (preserved disagreement):**
- Senturk & Smits 2019, *AIAA J.* 57(7):2663–2669 (**search-summary**; the full text and the ege.edu.tr repository were not reachable) simulated pitching NACA foils at Re 500–32,000.
- They report that the empirical coefficients scale with Re^½, consistent with laminar flow. This supports S32's *form* of the scaling within that range.
- The same summary says thrust and power are "largely insensitive above Re ≈ 16,000", while efficiency keeps a Re dependence "driven by airfoil drag".
- That is consistent with drag continuing to fall, but it was established only up to 3.2×10⁴, about 10× short of the exocoetid lobe.

## 4. Evidence level

- "Derived" is honest for the arithmetic.
- **Defect:** the recorded value 0.63 is presented as *the* zebrafish ratio. It is the GENEROUS-case midpoint (Cd_b = 0.3), and the defensible derived range is **0.44–0.67**.
- The exocoetid ratio 1.3–1.5 is derived from an assumed frequency (a CFD output), an assumed amplitude and an extrapolated C_D. Calling it a comparison of the two animals overstates it. It is a comparison of the zebrafish with a parameterised model of an exocoetid tuned to taxi.

## 5. Counter-evidence S32 missed

- **APS March Meeting 2024 abstract, "Flying fish taxiing on the water's surface"** (meetings-archive.aps.org/mar/2024/s27/13). **Read level: search-summary only.** The host is outside this session's allowed network domains, so the abstract itself was not read.
- **What the summary says:** taxiing flying fish "slap their tails on the water" at **≈13.5 Hz**, and about 2 N of tail-beat force is predicted to keep a 200 g fish above the surface.
- **My inference, if that frequency applies:** S32's f = 50 Hz is about 3.7× too high. f·A_pp/V_to becomes 0.016–0.028 at A_pp 2–3.1 cm. Under S32's own equations, U_max/V_to is then 0.22–0.37 *even with* the Re^−½ C_D.
- Reaching V_to would then need A_pp ≈ 7.9–8.4 cm (my calculation at C_D(Re_Vto)). That is a kinematic discriminator, not a Reynolds-number one.
- The "slapping" description also suggests a propulsor regime (surface slapping or water-walking) that S32's submerged pitching-foil law may not describe at all.
- **This is a search summary, and the conditions are unknown** (fish size, lab or field, steady or accelerating taxi). It **weakens** the claim and does not refute it.

**Negative search, scope stated:**
- Measured exocoetid taxi tail-beat *amplitude*: two web searches this session (Senturk–Smits Re scaling; flying-fish taxi tail-beat frequency/amplitude, Edgerton/Breder). **No amplitude value was found.** `unknown`.
- The Edgerton & Breder high-speed film work was not located.

## 6. What survives and what does not

- **Survives:** the zebrafish taxi ceiling is below glide speed for every Cd_b, C_D branch and φ in S32's ranges (0.44–0.67 V_to, foil-only). Because c₆ cancels, it is insensitive to the thrust-law coefficient.
- **Does not survive as stated:**
  - "differ ONLY in lobe C_D";
  - "share f·A_pp/V_to at 0.09–0.10" as an empirical fact;
  - "the barrier is a property of the taxi's Reynolds number" as an identified cause.
  - The zebrafish/exocoetid contrast could equally be kinematic (amplitude) or a change of propulsion mechanism (slapping), and one secondary source points that way.
- **What would decide it:** measured exocoetid taxi f and A_pp, and/or measured oscillating-foil C_D at Re 10⁵–4×10⁵.

## Sources and read levels
- S32-organism.md and S32_taxi.py, commit `c1b761eb`: **full-text** (script re-run; §6–7 output reproduced).
- Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478: **via S32** (S32 states FULL; not re-read here).
- Senturk & Smits 2019, *AIAA J.* 57(7): **search-summary** (repository host not reachable).
- APS March Meeting 2024, s27/13, flying-fish taxiing: **search-summary** (host not reachable).
- Deng et al. 2019, bioRxiv 765560: **search-summary** this session (36 W, 15°, 50 Hz as a CFD minimum-power point; 15–20 m/s peak).
- Blasius and turbulent flat-plate friction: textbook formulas, my calculation.

```swarm-challenge
{"claim_id": 272, "outcome": "weakened", "reason": "The arithmetic reproduces, and the zebrafish ceiling stays below glide speed (0.44-0.67 V_to over Cd_body 0.1-0.3, with c6 cancelling), but the exocoetid side rests on an assumed 50 Hz (a CFD output), an assumed amplitude and a Re^-1/2 C_D extrapolation 26-42x beyond the data, which was selected because it lets flying fish taxi; the attribution 'ONLY C_D(Re)' is therefore unidentified, and a search-summary-level 2024 APS report of ~13.5 Hz taxi tail slapping would put the discriminator on kinematics instead.", "corrected_value": "zebrafish U_max/V_to 0.44-0.67 (derived, foil-only; 0.63 is the Cd_body=0.3 generous midpoint); exocoetid ratio unidentified, >1 only if lobe C_D at Re ~3.7e5 is <=0.016-0.019", "depends_on": ["S32-organism.md and S32_taxi.py (commit c1b761eb) inputs", "Floryan2017-foil-scaling (c6 2.55, C_D 0.08, Re 4780-9560)", "Miln2021-burst 1.38 m/s via S28", "S29 body Cd 0.1-0.3", "S28 wing V_to 4.41 m/s", "Fish1990-tables (exocoetid V_to)", "Deng2019-taxi-CFD 50 Hz/15 deg (search-summary)", "Senturk-Smits2019 Re^1/2 scaling Re 500-32000 (search-summary)", "APS2024-flying-fish-taxiing 13.5 Hz (search-summary)", "Blasius and turbulent flat-plate friction formulas"]}
```
