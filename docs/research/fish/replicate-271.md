# Replication 271: "The ceiling has a clean form"

This is an independent re-derivation of the S32 taxi-phase speed ceiling. S32 is the multi-stroke launch study of an airborne-body taxi for the designed zebrafish.

## What I read, and in what order (independence statement)

1. **S32-organism.md** is not on this branch. I found it on `origin/claude/s32-multi-stroke-launch-qpq9g2` and read only **§1 (equations of motion)** and **§2 (inputs table)**, lines 38–104. I deliberately skipped §0 "Short answer", §3–§5 and the answer block, because they carry the result.
   - §1–§2 contain no ceiling value or formula.
   - §1 does write the thrust in the form T = ½ρ_w S_imm [G − C_D U²]. Once the thrust is written that way, the clean form is one line of algebra. **So my derivation of the *form* is only weakly independent of S32.** The independent parts are:
     - checking the coefficients and the Strouhal definition against the primary paper;
     - the arithmetic;
     - the C_D(Re) sensitivity.
2. **Floryan, Van Buren, Rowley & Smits 2017**, arXiv:1704.07478v1. Read-level **full-text** (arXiv v1, 6-page PDF, downloaded and searched this session). I did not read the published JFM version (*could-not-access*; I did not try cambridge.org).
3. **Only after finishing the derivation** did I grep S32 for "ceiling"/"clean" and read the matching lines (§0 lines 23–34, the §4.1 table row at line 191, and the answer block at lines 269–271). I compare against those below.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Pitching-foil thrust law | C_T = c₆ St² + c₇ St A* − C_Dp. The fit gives **c₆ = 2.55, c₇ = 0, C_Dp = 0.08** | Floryan et al. 2017 §5, eq. 2.7 | full-text (arXiv v1) |
| Strouhal definition | St = 2fA/U∞, where A is the trailing-edge amplitude (c·sinθ₀, a half-amplitude). So **St = f·A_pp/U** with A_pp the peak-to-peak excursion. This confirms S32's usage | Floryan et al. 2017 §2 | full-text |
| Conditions of the fit | Pitch fit taken at 60 mm/s, Re = 4,780. Teardrop foil: c = 80 mm, AR 3.5, gaps < 5 mm, so effectively 2-D. The authors state that the coefficients are unchanged when the speed goes from 60 to 120 mm/s (Re ≈ 9,560 by my scaling), and that dimensional pitching thrust is independent of U∞ (their Fig. 8) | Floryan et al. 2017 §3, §5, §6 | full-text |
| Tail-speed scale G = κ c₆ (f A_pp)² | 0.27–0.52 m²/s². This is a calibration by the S32 author (burst-peak thrust = body drag), not a measurement | S32 §2 | listing of S32 (inputs table read in full; its upstream sources were not re-read by me) |
| Burst peak speed (calibration point) | 1.38 m/s | S32 §2, which cites S29/S24 | inherited, not re-read |
| Body Cd and frontal area | Cd 0.1–0.3 on 24 mm² (ASSUMED in S32) | S32 §2 | inherited |
| Caudal fin area | 37.8 mm² (ASSUMED in S32) | S32 §2 | inherited |
| Lobe chord | 6 mm | S32 §2, via Wakamatsu 2019 | inherited |
| Glide (take-off) speed V_to | 4.41 m/s at 0.25 g | S32 §2, via S28 (unmeasured wing) | inherited |
| κ (3-D, free-surface and flexibility correction) | 1, the 2-D rigid-foil value. ASSUMED | S32 §1 | inherited |
| ν (water) | 1.0×10⁻⁶ m²/s | physical constant, my value | — |

## Derivation (calculated, not observed)

The lobe's net horizontal force is

  T_lobe = ½ ρ_w S_imm U² C_T = ½ ρ_w S_imm U² [c₆ (f A_pp/U)² − C_D]
         = ½ ρ_w S_imm [c₆ (f A_pp)² − C_D U²]

The thrust term does not depend on U. The drag term grows as U². The lobe's own net force is zero at

  **U_max = f · A_pp · √(κ c₆ / C_D) = √(G / C_D)**

Equivalently, the ceiling sits at a fixed Strouhal number, **St* = √(C_D / c₆)**.

- **S_imm, ρ_w and body mass all cancel.** The immersed fraction φ and the fish's weight therefore do not move this ceiling.
- Every other term in S32's horizontal balance is a drag that only lowers the speed where net force is zero: wing drag, body air drag, lobe induced drag, and surface-tension drag. **U_max is therefore an upper bound** on the taxi equilibrium speed (my inference from the sign of the terms).

### Arithmetic

- √(c₆/C_D) = √(2.55/0.08) = √31.875 = **5.646**.
- St* = √(0.08/2.55) = **0.177**.

The calibration of G can be checked independently: burst-peak thrust = body drag at U_b = 1.38 m/s (U_b² = 1.9044), so

  G = C_D U_b² + Cd_b (A_b/S_c) U_b², with A_b/S_c = 24/37.8 = 0.635

- Cd_b = 0.1: G = 0.152 + 0.121 = **0.273**, so f·A_pp = √(G/2.55) = 0.327 m/s.
- Cd_b = 0.3: G = 0.152 + 0.363 = **0.515**, so f·A_pp = 0.449 m/s.

This reproduces S32's 0.27–0.52. It also gives a second clean form:

  U_max = U_b · √(1 + Cd_b A_b / (C_D S_c))

With constant C_D = 0.08 (the Floryan value):

- Cd_b 0.1: U_max = √(0.273/0.08) = **1.85 m/s**, which is 0.42 V_to.
- Cd_b 0.3: U_max = √(0.515/0.08) = **2.54 m/s**, which is 0.58 V_to.

**Sensitivity: C_D(Re).** The lobe Re at ~2–3 m/s with c = 6 mm is 12k–18k, above Floryan's measured 4,780–9,560. As an assumed extrapolation, I scale C_D = 0.08·(9,560/Re)^½ for Re > 9,560 and solve self-consistently. Then U^{3/2} = (fA_pp)² (c₆/0.08) √(c/(ν·9,560)), which gives:

- Cd_b 0.1: **1.94 m/s** (0.44 V_to), with C_D = 0.073.
- Cd_b 0.3: **2.96 m/s** (0.67 V_to), with C_D = 0.059.

**Tail speed needed to reach V_to** (constant C_D): f·A_pp = 4.41/5.646 = **0.78 m/s**, i.e. A_pp ≈ 15 mm at 52 Hz. That is 1.7–2.4× the calibrated 0.33–0.45 m/s.

## My value

**Clean form: U_max = f·A_pp·√(κ c₆/C_D) ≈ 5.65·√κ·f·A_pp (with c₆ = 2.55 and C_D = 0.08), i.e. a zero-net-thrust Strouhal number St* = √(C_D/c₆) ≈ 0.18.**

- Numerically, for κ = 1: **1.85–2.54 m/s** with constant C_D, or **1.94–2.96 m/s** with Re^−½-scaled C_D. That is 0.42–0.67 of V_to = 4.41 m/s.
- All of these are **calculated**. None is observed.

Uncertainty and caveats:

- Floryan et al. give no confidence interval on c₆ or C_D in the text I read, so the coefficient's own uncertainty is *unknown*.
- The spread above comes from the assumed body Cd (×1.37 in U_max) and from the C_D extrapolation (up to ×1.17).
- κ is unmeasured, and U_max scales as √κ.
- **Caveat that I raise (my inference):** Floryan's Fig. 8 shows dimensional *net* pitching thrust independent of U∞ over 60–120 mm/s. Taken literally, that means the C_D·U² term was either small against the thrust term or not constant across that range. "C_D = 0.08 constant across 4,780–9,560" is therefore an interpretation of the paper, not a direct measurement at 9,560.

## Comparison with the recorded value (read only after the derivation above)

S32 records the ceiling as **U_max = f·A_pp·√(c₆/C_D(Re))**:

- line 269: "immersed area and mass drop out";
- key_number line 270: "ceiling U_max = f*A_pp*sqrt(2.55/C_D(Re)), lobe C_D ~0.06-0.08 at zebrafish Re ~1e4".

Its §4.1 table gives **U_max/V_to = 0.58–0.68**, and §0 quotes "about 2.9 m/s".

- **Form:** identical to mine, including the cancellation of S_imm and mass.
- **Numbers:** S32's 0.58–0.68 V_to (2.56–3.0 m/s) matches my generous end (Cd_b = 0.3): 0.58 V_to with constant C_D, 0.67 with Re-scaled C_D. My bracket extends lower (0.42–0.44 V_to) because I also evaluated the low-Cd_b calibration. S32 quotes its table row from the GENEROUS case, so this is a difference of scope, not a disagreement.
- S32's integrated taxi stall of 2.19–2.88 m/s sits below or at the ceiling. That is consistent with U_max being an upper bound.

**Verdict: AGREE** on the clean form and, for the generous calibration, on the value. Note the weak-independence caveat on the form above.

```swarm-replication
{"claim_id": 271, "my_value": "U_max = f*A_pp*sqrt(kappa*c6/C_D) ~= 5.65*f*A_pp (St* = 0.177); 1.85-2.54 m/s const C_D, 1.94-2.96 m/s Re-scaled C_D (0.42-0.67 V_to), calculated", "agrees": true, "note": "Same closed form with area and mass cancelling, and S32's 0.58-0.68 V_to matches my generous-calibration end; coefficients c6=2.55, C_D=0.08 and St=2fA/U confirmed in Floryan et al. 2017 arXiv v1 full text, but form independence is weak because S32's section 1 already writes thrust as G - C_D U^2."}
```
