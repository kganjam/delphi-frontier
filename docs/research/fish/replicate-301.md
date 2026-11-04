# Replication of claim 301 (S3-D): S3 launch-power shortfall under a fin-wing CL_max bracket

**Everything numeric in this file is calculated. None of it is an observation.** The only observed inputs are the measured values carried in from upstream documents, and their read-levels are listed below.

## What I read, and what I deliberately did not read

- The pointer was `harvest:s3-mass-power-budget-rcrklv`. Branch `claude/s3-mass-power-budget-rcrklv` adds three files: `S3_budget.py`, `S3-deepen.md` and `S3-deepen_calc.py`.
- **`S3-deepen.md` and `S3-deepen_calc.py` appear to be the claim's own working. I did not open them.** I saw only their file names in a `git diff --stat`.
- I read `S3_budget.py` in full. It is the upstream S3 input model, and the same file sits on `claude/s3-organism-mass-budget-000ync`.
- I grepped `S3-organism.md` (on `claude/s3-organism-mass-budget-000ync`) for its input table and its definition of the "most generous case".
  - That grep also showed the upstream S3 result at CL 1.07: 2.9× short, and 1.06× short at η_h = 1.
  - That is the *pre-deepen* baseline, not claim 301's value. I state it here so the reader knows I saw it.

## Model (re-derived; matches the structure of `S3_budget.py` §5)

Take-off speed with wing mass charged:

  V = √(2 M g / (ρ_air S CL)), with M = m_body + σ S

Launch power per kg of body, for constant acceleration from rest over a distance s:

  P_b = (V²/2) / t / η_h, with t = 2s/V, so **P_b = V³ / (4 s η_h)**

Launch power per kg of muscle:

  P_m = P_b · M / (f_m m_body)

**Scaling (algebra, not a fit).** M does not depend on CL, so P_m ∝ V³ ∝ CL^-1.5 exactly. The claim's exponent is correct.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| g, ρ_air | 9.81 m s⁻², 1.225 kg m⁻³ | standard constants | — |
| m_body | 0.40 g | project brief, via `S3_budget.py` | full-text (repo) |
| Wing area S (S10 planform) | 1070 mm² | S10, via `S3_budget.py` | full-text (repo) |
| Fin areal density σ (central) | (0.8×1050 + 0.2×1557) kg m⁻³ × 120 µm = 0.13817 kg m⁻² | Puri 2018 thickness; Robertson 2008 and Tont 1977 density proxies; 20 % ray fraction and 120 µm taper mean are ASSUMED. All via `S3_budget.py` / `S3-organism.md` | full-text (repo); primaries not read by me |
| Run-up distance s | 2 BL = 0.08 m (most generous of 0.5/1/2 BL) | S3 assumption | full-text (repo) |
| Muscle fraction f_m | 0.6 (most generous of 0.3/0.6) | S29, secondary figure | full-text (repo); primary not read |
| Hydromechanical efficiency η_h | 0.37 (pike, 0.34–0.39) | Frith & Blake, via S29 | abstract via S29 (per `S3-organism.md`); I did not read it |
| Muscle power | 142.7 W kg⁻¹ | Wakeling & Johnston 1998, *J Exp Biol* 201:1505 | abstract (per `S3-organism.md`); I did not read it |
| Burst speed | 1.38 m/s | Miln et al. 2021, via S28 | via S28; I did not read it |
| CL_max, project proxy | 1.07 | S2/S28, derived | full-text (repo) |
| CL_max, flying-fish bracket | 1.0–1.1 | **taken from the claim statement** | I did not verify this bracket. See "Independent check on the CL bracket" below |

**"Most generous case" definition.** `S3-organism.md` (§summary, line 33) defines it as: S10 wing, 2 BL, f_m 0.6, η_h 0.37.

- I adopt that definition, because it is the upstream one.
- **Inference:** the full grid in `S3_budget.py` also contains η_h = 1, and that cell is more generous still. I report it separately below.

## Arithmetic

M = 0.40 g + 0.13817 × 1070×10⁻⁶ kg = 0.40 + 0.14784 = **0.5478 g**

| CL | V (m/s) | P_b = V³/(4·0.08·0.37) (W kg⁻¹ body) | P_m = P_b × 0.5478/(0.6×0.40) (W kg⁻¹ muscle) | ÷ 142.7 |
|---|---|---|---|---|
| 1.00 | 2.8636 | 198.33 | 452.7 | **3.173** |
| 1.07 | 2.7684 | 179.19 | 409.0 | 2.866 |
| 1.10 | 2.7304 | 171.91 | 392.4 | **2.750** |

**Closure CL** (shortfall = 1): CL = 1.07 × 2.866^(2/3) = **2.159**. That is 1.96× the top of the 1.0–1.1 bracket.

**Factor-2 sensitivity at the CL 1.07 baseline (2.866×).**

| Change | Shortfall | Comment |
|---|---|---|
| CL ×2 (2.14) | 1.013 | reaches parity only approximately: still 1.3 % short |
| s ×2 | 1.433 | |
| 142.7 ×2 | 1.433 | |
| η_h ×2 (0.74) | 1.433 | |
| σ ÷2 | 1.995 | P_m ∝ M^2.5 / m_body |
| σ = 0 | 1.306 | |
| f_m → 1.0 | 1.720 | ×2 is not possible from 0.6 |

**Inference:** CL is the only single input whose factor-2 change brings the shortfall to about 1. "Reaches parity" is accurate only to about 1 %.

**More generous cell, η_h = 1** (the rest is the same): 1.017–1.174×, and 1.061× at CL 1.07.

- At η_h = 1, CL 1.1 leaves a 1.7 % shortfall, and closure needs CL ≥ 1.113.
- **So the "power verdict stands" depends on η_h = 0.37.** That is also how upstream S3 framed it ("not robust to η_h").

**Self-carry sub-claim at 1.38 m/s.**

- Lift per area = ½ρV²CL/g = 0.11891·CL kg m⁻².
- Central σ = 0.13817 kg m⁻².

| CL | lift/area (kg m⁻²) | σ / lift (margin by which the tissue fails) | V_self / 1.38 |
|---|---|---|---|
| 1.00 | 0.1189 | 1.162 | 1.078 |
| 1.07 | 0.1272 | 1.086 | 1.042 |
| 1.10 | 0.1308 | 1.056 | 1.028 |

At the low σ bracket (40 µm, soft density), the tissue carries itself at every CL (σ/lift 0.32–0.35). At the high bracket it fails by 2.4–2.6×.

## My value

**Launch-power shortfall: 2.75–3.17× (calculated)** in the upstream-defined most generous case (S10, 2 BL, f_m 0.6, η_h 0.37), over CL_max 1.0–1.1.

- Closure needs CL_max ≥ 2.16 (calculated).
- Uncertainty is dominated by inputs other than CL, none of which is measured for zebrafish:
  - η_h: at 1.0 the range is 1.02–1.17×.
  - f_m: at 0.3 the shortfall doubles.
  - The 142.7 W kg⁻¹ comparator is *Scorpaena* at 20 °C.

**Self-carry margin: 1.06–1.16 (σ/lift), or 1.03–1.08 in speed terms (calculated)**, at central σ over CL 1.0–1.1.

## Independent check on the CL bracket (could not complete)

- One standard web search for a measured flying-fish CL_max returned a **search-summary** attributing about **0.78 at 30–35°** (physical wind tunnel, *Cypselurus hiraii*) to Park & Choi 2010, *J Exp Biol* 213:3269.
  - The attribution came via a 2023 paper's summary.
  - That same summary gave a **numerical** value of **1.03** at 35°.
- I could not open either full text: typeset.io and imkhanhnguyen.github.io do not resolve from this session.
  - Read-level for both: **search-summary**.
  - **I treat 0.78 as unverified. It may be wrong.**
- **If** the physical value were 0.78, the most generous shortfall would be 2.866 × (1.07/0.78)^1.5 = **4.61×** (calculated), and the self-carry margin would be 1.49.
  - That makes the power verdict stronger, not weaker.
  - But it would put the low end of the "1.0–1.1 fin-wing bracket" in question.
- The original 2010 PDF needs checking before anyone relies on the bracket.
- I did not search for the dragonfly 1.07 provenance.
- Search scope: two standard web searches and two failed fetches.

## Comparison with the recorded value

I compared only after finishing the derivation. The source is the claim text itself; I still have not opened `S3-deepen.md`.

- **Shortfall 2.75–3.17× and closure CL ≥ 2.16: AGREE.** I reproduce them to 3 significant figures. The definition of "most generous" (η_h 0.37) is upstream's own; the η_h = 1 cell would give 1.02–1.17×.
- **CL^-1.5 scaling: AGREE** (exact algebra).
- **"CL is the only input whose factor-2 error reaches parity": AGREE**, with the caveat that it reaches 1.013, not 1.000.
- **Self-carry margin 1.01–1.25: CANNOT TELL.**
  - My central-σ margin is 1.06–1.16 (σ/lift) or 1.03–1.08 (speed). Both ranges sit inside 1.01–1.25 but are narrower.
  - The recorded range presumably also brackets σ (for example, ray fraction or density) in a way I cannot reconstruct without reading their working.
  - **Inference:** the qualitative reading, "near break-even", agrees. "Weakens" is mild: at the 1.07 baseline the margin was already 1.086.
- **The flying-fish bracket 1.0–1.1 itself: CANNOT TELL.** One search-summary points to a lower measured value (about 0.78), and I could not verify it.

```swarm-replication
{"claim_id": 301, "my_value": "2.75-3.17x launch-power shortfall (calculated; S10, 2 BL, f_m 0.6, eta_h 0.37, CL 1.1-1.0), closure CL >= 2.16; self-carry sigma/lift 1.06-1.16 at central sigma", "agrees": true,
  "note": "Shortfall, closure CL and CL^-1.5 scaling reproduce to 3 s.f., but the verdict depends on eta_h=0.37 (eta_h=1 gives 1.02-1.17x), the 1.01-1.25 self-carry range could not be reconstructed, and an unverified search-summary suggests measured flying-fish CL_max may be ~0.78 rather than 1.0-1.1."}
```
