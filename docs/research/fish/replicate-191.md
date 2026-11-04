# Replication of claim 191 — wing gain on a ballistic leap

**Claim under test:** at the measured maximum burst of 1.38 m/s, the ballistic leap is 19.4 cm. The designed wing lengthens it by only +1.5 to +3.0 % (3–6 mm). At 0.45 m/s the gain is ~0 %.

**Result type:** every range number below is **calculated** (point-mass numerical integration). Nothing here was observed. No fish was flown and no fin was measured.

## 0. Process disclosure

- The task prompt was meant to hide the answer, but it did not: the claim text itself contains "19.4 cm" and "+1.5 to +3.0 % (3–6 mm)". I saw those figures before I started.
- `S28-organism.md` is not on this branch. I found it only on `origin/claude/s28-organism-design-5z0vjz` (`docs/research/fish/S28-organism.md`).
- **Before deriving,** I read only §1 (input table) and §2 (geometry) of that file. Those sections contain no leap-range results. I did not read §0 (short answer) or §3 until my simulations had finished.
- **After deriving,** I read §3.1–3.2 to compare. When I found a mismatch there, I ran one more targeted test (§4 below), and I say so where it appears.

## 1. Inputs

| Input | Value | Source | Read-level | Status |
|---|---|---|---|---|
| g | 9.81 m s⁻² | constant | — | constant |
| ρ_air | 1.225 kg m⁻³ | constant (ISA sea level) | — | constant |
| Burst speed U_b | 0.45–1.38 m/s | Miln et al. 2021, as cited in S28 §1 | **listing** (I saw only the S28 citation; I did not open the paper) | S28 labels it *measured*. It is a swimming burst, not a water-exit speed. I assume exit speed = burst speed, as S28 does, and that is generous |
| Body mass m | 0.25 g → W = 2.4525e-3 N | S28 §1 | full-text (S28) | S28 marks it *assumed, back-solved* |
| CL_max | 1.07 | S28 §1 | full-text (S28) | project-derived, not measured |
| Wing area S, aspect ratio AR | A: 57 mm², AR 16.9; B: 125 mm², AR 7.7; C: 192 mm², AR 5.0 | S28 §2.2 | full-text (S28) | all **assumed** bracketing cases. Fin area was never measured |
| Body drag | CD 0.3 on 24 mm² frontal area | S28 §3.2 | full-text, read **after** my first run | assumed. Used only in my second run, to match S28's assumptions |
| Wing drag | CD = CD0 + CL²/(π·0.8·AR), with CD0 swept from 0 to 0.20 | my choice (Oswald e = 0.8 matches S28) | — | assumed. Profile drag at Re ≈ 570 is not known for this fin. I tried a range instead of picking one value |

## 2. Arithmetic

**Ballistic range (vacuum, 45°):**
- R = V²/g = 1.38² / 9.81 = 1.9044 / 9.81 = **0.19413 m = 19.41 cm**
- At 0.45 m/s: 0.2025 / 9.81 = **2.064 cm**

**Lift fraction at launch, case C (my check):**
- q = ½ · 1.225 · 1.38² = 1.1664 Pa
- L = q · S · CL = 1.1664 · 192e-6 · 1.07 = 2.396e-4 N
- L/W = 2.396e-4 / 2.4525e-3 = **0.098**, so lift is about 10 % of weight

At the apex, speed falls to about 0.976 m/s, so L/W ≈ 0.049. On the descent, lift (which acts perpendicular to the path) partly points backward. That is why the gain is small.

**Integration model** (`leap.py`, `leap2.py`, kept in the session scratchpad and not committed):
- 2D point mass, explicit Euler, dt = 1e-5 s
- forces: lift perpendicular to velocity at fixed CL = 1.07; drag along −v
- landing interpolated at y = 0
- launch angle swept from 30° to 60° in 0.5° steps; maximum range reported

## 3. My results (calculated)

### Run 1 — no body drag; wild type (WT) = 19.414 cm

| Case | Wing CD | Range @1.38 | Gain |
|---|---|---|---|
| C | 0 (no wing drag) | 20.135 cm | **+3.71 %, +7.2 mm** |
| C | 0.091 (induced only) | 19.995 cm | +2.99 %, +5.8 mm |
| C | CD0 0.05–0.10 + induced | 19.92–19.85 cm | +2.6 to +2.2 %, +5.1 to +4.3 mm |
| B | CD0 0–0.10 + induced | 19.82–19.72 cm | +2.1 to +1.6 % |
| A | CD0 0–0.10 + induced | 19.61–19.57 cm | +1.0 to +0.8 % |

At 0.45 m/s, every case gains between +0.08 and +0.38 % (≤ 0.08 mm).

### Run 2 — S28's body drag added; WT = 19.362 cm (S28 reports 19.36 cm)

| Case, wing CD0 | My gain @1.38 | S28 §3.2 gain | Match? |
|---|---|---|---|
| C, CD0 0.08 | +2.36 % (19.819 cm) | +2.4 % (19.82 cm) | yes |
| C, CD0 0.20 | +1.45 % (19.643 cm) | +1.5 % (19.64 cm) | yes |
| B, CD0 0.12 | +1.49 % (19.650 cm) | +1.5 % (19.65 cm) | yes |
| A, CD0 0.12 | +0.74 % (19.506 cm) | +0.7 % (19.50 cm) | yes |
| C, "zero wing drag" upper bound | **+3.69 % (20.077 cm, +7.2 mm)** | **+3.0 % (19.94 cm)** | **no** |

At 0.45 m/s, my gains are +0.06 to +0.38 %. S28 reports ~0 to +0.2 %. These agree.

## 4. The one disagreement (diagnosed after reading S28)

I tested case C with CD0 = 0 but induced drag kept (CD = 0.0911). That gives **19.939 cm, +2.98 %**, which matches S28's "19.94 cm, +3.0 %" exactly.

*My inference:* S28's "upper bound: case C with zero wing drag" row actually sets **zero profile drag** and keeps induced drag. With truly zero wing drag, the bound is **+3.7 % (≈ 7 mm)**. A lifting wing cannot avoid induced drag, so S28's +3.0 % is the more physical ceiling. But the row's label is wrong, and calling it "zero wing drag" understates the true no-drag bound by 0.7 percentage points.

## 5. My value

Gain at 1.38 m/s for the headline case C (AR 5, 192 mm²), with physically plausible wing drag (CD0 0.05–0.20 plus induced drag):
- **+1.5 to +3.0 %, i.e. +2.8 to +5.8 mm**, on a WT leap of 19.4 cm
- uncertainty driven by CD0
- the same band holds whether or not body drag is included

Wider bounds:
- **Across area cases A–C:** +0.6 to +3.0 %
- **Absolute ceiling** (no wing drag at all, a non-physical case): +3.7 % (7.2 mm)
- **At 0.45 m/s:** +0.1 to +0.4 %, i.e. < 0.1 mm, effectively 0

Caveats:
- All of these inherit S28's **assumed** mass, area and CL_max.
- They also inherit the generous assumption that exit speed equals swimming burst speed.
- At a heavier 0.40 g (S28 also calls this typical), L/W falls by 0.25/0.40, and the gain shrinks roughly in proportion.

## 6. Comparison and verdict

**AGREE**, with one caveat:
- The 19.4 cm range reproduces.
- The +1.5 to +3.0 % (3–6 mm) band at 1.38 m/s reproduces for S28's case B/C rows to within ±0.05 percentage points.
- The ~0 % gain at 0.45 m/s reproduces.

The caveat:
- The claim's band leaves out case A (+0.7 %), which S28 itself calls the closest to what the *longfin* allele does.
- S28's "zero wing drag" upper bound is mislabelled: it keeps induced drag. True zero drag gives +3.7 %.
- Neither point changes the conclusion that the wing adds only millimetres.

This is one independent re-run of the same physics on the same assumed inputs. It checks the arithmetic and the model, not the inputs. The inputs (mass, fin area, CL_max, exit speed) are still assumed or unverified.

```swarm-replication
{"claim_id": 191, "my_value": "19.41 cm WT range; wing gain at 1.38 m/s +1.5 to +3.0 % (+2.8 to +5.8 mm) for case C with CD0 0.05-0.20 + induced drag (+3.7 %/7.2 mm if wing drag is zero; +0.7 % for case A); +0.1 to +0.4 % at 0.45 m/s", "agrees": true, "note": "All S28 §3.2 rows reproduce to within 0.05 pp, except the 'zero wing drag' upper bound (+3.0 %), which actually keeps induced drag; true zero drag gives +3.7 %."}
```
