# Replication of claim 245: replication of the S7 pectoral-girdle result (claim 201)

## 0. Disclosure: this is not a blind re-derivation

The question I was given was the single word "Replication". The only pointer to its inputs was `replicate-201.md` on branch `claude/rederive-s7-pectoral-girdle-r2hm12`. That file **is** the recorded result for this claim, not only a list of inputs. To find out what was being claimed I had to read it, and I read it in full before computing anything. **So I saw the recorded value before I derived mine.** My agreement below is therefore weak evidence of independence. It is a third-party re-run of the arithmetic, not a blind derivation.

To limit further anchoring:

- I took the inputs from the original harvest file, `docs/research/fish/S7-organ.md` on branch `claude/s7-organ-pectoral-girdle-xlxpkt`. I read only its assumption table, §3a (A1–A10), not its computed sections §3b–§6.
- I wrote my own script, `replicate-245-calc.py`, from scratch.
- I added a third load model (uniform lift) and a C_L = 1.03 sensitivity case, neither of which appears in replicate-201's tables.

## 1. Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| A1 | Body mass, weight | 0.4 g; W = 3.923 mN (g = 9.80665 m s⁻²) | Project brief, via S7-organ.md A1 | listing |
| A2 | Lift coefficient | C_L = 0.78 | S7-organ.md A2, attributed to Park & Choi 2010, *J. Exp. Biol.*, doi:10.1242/jeb.046052 | abstract (Europe PMC REST, fetched 2026-11-04). **The abstract does not state 0.78**, so the value is unverified by me. |
| A2' | Alternative C_L | 1.03 | Bioinspir. Biomim. 2019, doi:10.1088/1748-3190/ab23e6, as reported in replicate-201 | **could-not-access by me.** I did not fetch it, so I am relying on replicate-201's abstract-level read. Run as a sensitivity case only. |
| A3 | Speed | V = 3, 5 m s⁻¹ | S7-organ.md A3 | listing. The author's own bracket, **not measured**. |
| A4 | Aspect ratio | 9 | S7-organ.md A4 | listing. The author's read-level was search-summary. |
| A5 | Body half-width | y₀ = 2.5 mm | S7-organ.md A5 | listing. Estimate. |
| A6 | Spanwise lift distribution | Elliptic over the fin; centroid at 4s/(3π) | S7-organ.md A6 | listing. An idealisation. |
| A7 | Load factor | n = 1, 3 | S7-organ.md A7 | listing. Bracket. |
| A8 | Bone yield stress | σ_y = 25–114 MPa | S7-organ.md A8 | listing. The yield strain (0.5%) is assumed. Teleost bone strength itself is **unknown**. |
| A9 | Muscle stress | 200 kPa | S7-organ.md A9 | listing. Assumed. |
| A10 | Adductor moment arm | r = 0.5–1.0 mm | S7-organ.md A10 | listing. Guess, not measured. |
| — | Air density | ρ = 1.204 kg m⁻³ (20 °C) | Standard atmosphere | n/a |

**Scope of negative searches.** I made one Europe PMC query, by DOI, for Park & Choi 2010. It returned the abstract, which contains no numeric C_L. I did not search for the zebrafish girdle cross-section, the adductor PCSA or teleost bone strength, so those remain **unknown**.

## 2. Arithmetic (all calculated; nothing here is observed)

The numerical integration uses the midpoint rule with N = 2×10⁵.

**Wing size.**

- S = 2W/(ρV²C_L)
- b = √(AR·S)
- fin length s = b/2 − y₀

**Moment models.**

- **Model A (S7's A6).** M = (nW/2)·4s/(3π)
- **Model B.** Lift is elliptic over the whole span, l(y) = (4W/πb)√(1−(2y/b)²). M = n∫_{y₀}^{b/2} l(y)(y−y₀)dy.
- **Model C (mine; an upper bound on the centroid).** Lift is uniform over the fin. M = (nW/2)(s/2).

**Bone section and muscle force.**

- Bone: d = (32M/(πσ_y))^(1/3)
- Muscle: F = M/r, and PCSA = F/200 kPa

Worked example, V = 3, n = 1, C_L = 0.78:

- S = 2(3.923×10⁻³)/(1.204·9·0.78) = 9.282×10⁻⁴ m²
- b = √(9·9.282×10⁻⁴) = 91.40 mm
- s = 45.70 − 2.5 = 43.20 mm
- M_A = 1.9615×10⁻³ × 0.4244 × 0.04320 = 3.596×10⁻⁵ N·m
- At r = 1 mm: F = 36.0 mN = 9.2 W

| C_L | V | n | s (mm) | M_A (N·m) | M_B | M_C | F/W at r = 0.5 mm (A / B / C) | F/W at r = 1.0 mm (A / B / C) |
|---|---|---|---|---|---|---|---|---|
| 0.78 | 3 | 1 | 43.20 | 3.60e-5 | 3.33e-5 | 4.24e-5 | 18.3 / 17.0 / 21.6 | 9.2 / 8.5 / 10.8 |
| 0.78 | 3 | 3 | 43.20 | 1.08e-4 | 9.99e-5 | 1.27e-4 | 55.0 / 50.9 / 64.8 | 27.5 / 25.5 / 32.4 |
| 0.78 | 5 | 1 | 24.92 | 2.07e-5 | 1.82e-5 | 2.44e-5 | 10.6 / 9.3 / 12.5 | **5.3** / 4.6 / 6.2 |
| 0.78 | 5 | 3 | 24.92 | 6.22e-5 | 5.46e-5 | 7.33e-5 | 31.7 / 27.8 / 37.4 | 15.9 / 13.9 / 18.7 |
| 1.03 | 3 | 3 | 37.27 | 9.31e-5 | 8.52e-5 | 1.10e-4 | 47.5 / 43.4 / 55.9 | 23.7 / 21.7 / 28.0 |
| 1.03 | 5 | 1 | 21.36 | 1.78e-5 | 1.53e-5 | 2.10e-5 | 9.1 / 7.8 / 10.7 | 4.5 / 3.9 / 5.3 |

**Bone diameter (Model A, C_L = 0.78).**

- Smallest: M = 2.074×10⁻⁵ with σ_y = 114 MPa gives **d = 0.123 mm**.
- Largest: M = 1.079×10⁻⁴ with σ_y = 25 MPa gives **d = 0.353 mm**.

**PCSA (Model A).** 0.10–1.08 mm².

## 3. My value (calculated, conditional on the assumed inputs A2–A10)

- **Root moment per fin:** 2.07×10⁻⁵ to 1.08×10⁻⁴ N·m. This is on the original idealisation, Model A, at C_L = 0.78.
- **Solid-equivalent bone diameter:** 0.12–0.35 mm.
- **Adductor muscle force:** 5.3–55 × body weight over the full V × n × r grid.
  - The ≈9× figure is only the lowest case at V = 3 m s⁻¹.
  - Including the load-model and C_L uncertainty, the force spans about 3.9–65 × W.
  - My inference, following replicate-201: the articular reaction differs from the muscle force by at most the fin lift, nW/2 ≤ 1.5 W.
- **Uncertainty.** The load model contributes about ±15%, and C_L contributes about −14%. The guessed r (force ∝ 1/r) and the chosen V bracket dominate both. Bone strength and r are **unknown**, not measured.

## 4. Comparison with the recorded value (replicate-201, read before deriving; see §0)

The recorded replication claims four things:

1. The moment and bone-section values reproduce claim 201's numbers.
2. The lower bound of the joint reaction should be about 5× W, not 9× W, because the V = 5, n = 1, r = 1 mm case gives 5.3× W.
3. Model B is 7–12% lower than Model A.
4. The qualitative conclusion stands.

**AGREE on all four.** I reproduce every number in replicate-201's Model A and Model B tables to the stated precision:

- moments 2.07×10⁻⁵ to 1.079×10⁻⁴ N·m
- d = 0.123–0.353 mm
- 5.3–55.0 W (Model A)
- 4.6–50.9 W (Model B)

The added Model C and the C_L = 1.03 case do not overturn the ≈5× lower-bound correction. They widen the band to 3.9–65× W. My inference is that "≈4–6× W" is a fairer lower bound than 9×.

**Caveat on evidential weight.** My inputs come from the same harvest table, which is the same assumptions. I also saw the result first. This check shows the arithmetic is reproducible. It does not independently validate the inputs: C_L = 0.78 is still unconfirmed in the abstract, and V, r and σ_y are still assumed.

```swarm-replication
{"claim_id": 245, "my_value": "M = 2.07e-5 to 1.08e-4 N·m per fin; d = 0.12-0.35 mm; adductor force 5.3-55 x W (Model A; 3.9-65 x W across load models and C_L 0.78/1.03) -- calculated", "agrees": true,
  "note": "Own script reproduces replicate-201's numbers, including the 5.3x (not 9x) lower bound, but I read the recorded result before deriving and used the same assumed inputs, so this confirms arithmetic only."}
```
