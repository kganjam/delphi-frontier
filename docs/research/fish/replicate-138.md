# Replication of claim 138 (S23-D-D): distal-only actinotrichia and tip compliance

Date: 2026-11-04. Independent re-derivation. I derived the result before reading the claim file.
I read S23-D's inputs from `S23-protein.md` (branch `claude/s23-actinotrichia-stiffness-protein-wwp5m2`).
I did not open `S23-D-deepen.md` or `S23-D-deepen-calc.py` (branch `claude/deepen-s23-sensitive-input-hynbng`)
until the comparison step in §5.

Everything in §2–§4 is **computed**. None of it is an observation.

## 1. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Load model | cantilever with a uniformly distributed load, root clamped | S23 `S23-protein.md` §3.1 | full-text (repo file) |
| Semi-span `L` | 2 cm and 4 cm design cases | S23 §3.1 | full-text (repo file) |
| Required stiffening / deflection reduction `R` | 39–981× | taken from the question text. S23 §3.1 itself gives 245–2616× at the 10 % criterion. I did not trace the 39× lenient corner to its primary working. Both ranges are tested below. | listing (question text) / full-text (S23) |
| Measured fin `EI` profile | 1.5–4×10⁻⁹ N·m², non-monotonic along the proximal–distal axis | Puri et al. 2018 *J Exp Biol* 221:jeb171777, as quoted in S23 §2.4 | secondary (S23 cites it as full-text) |
| Adult actinotrichia distal extent `a` | 200–300 µm | Premise of the question. **I did not verify it.** One standard web search ("adult zebrafish fin actinotrichia located distal tip of lepidotrichia length µm") confirmed only the *location* ("bundles … at the distal end of each lepidotrichia", ZFIN ZDB-PUB-170802-15) and that König et al. 2017 and Nakagawa et al. 2021 quantify the length. It did not return a µm value. | search-summary |

Because `a` is unverified at my read-level, §3 treats it as a free variable and checks a 10× range around it.

## 2. Model

Tip deflection by the unit-load method, with `s` measured from the tip:

```
M(s) = q s^2 / 2        (bending moment from the uniform load)
m(s) = s                (moment from a unit tip load)
δ_tip = ∫_0^L M m / EI(s) ds = (q/2) ∫_0^L s^3 / EI(s) ds
```

The distal segment `0 ≤ s ≤ a` contributes this fraction of tip compliance:

```
φ = ∫_0^a s^3/EI ds  /  ∫_0^L s^3/EI ds
```

- Uniform `EI`: φ = (a/L)⁴. I checked this closed form against a midpoint-rule integral with N = 2×10⁵. The two agreed to all four printed digits.
- If the distal segment is made infinitely stiff, its contribution drops to zero. Deflection then falls by at most `1/(1−φ)`.
- The conclusion flips when `1/(1−φ) ≥ R`, which means `φ ≥ 1 − 1/R`.

## 3. Arithmetic (uniform EI)

| L | a | a/L | φ = (a/L)⁴ | max reduction 1/(1−φ) |
|---|---|---|---|---|
| 4 cm | 200 µm | 0.005 | 6.25×10⁻¹⁰ | 1 + 6.3×10⁻¹⁰ |
| 4 cm | 300 µm | 0.0075 | 3.16×10⁻⁹ | 1 + 3.2×10⁻⁹ |
| 2 cm | 200 µm | 0.010 | 1.00×10⁻⁸ | 1 + 1.0×10⁻⁸ |
| 2 cm | 300 µm | 0.015 | 5.06×10⁻⁸ | 1 + 5.1×10⁻⁸ |
| 5 mm (a real-fin-sized `L`, illustrative) | 300 µm | 0.06 | 1.30×10⁻⁵ | 1 + 1.3×10⁻⁵ |

Every case is below 10⁻⁷, and so is a 10× larger `a`: at L = 2 cm and a = 3 mm, φ = 5×10⁻⁴. Against any required `R ≥ 39`, the reduction is short by more than a factor of 38. This holds for any actinotrichial modulus, so it is independent of E0.

**Flip threshold on a/L.** `a/L ≥ (1 − 1/R)^{1/4}`:

| R | 39 | 245 | 981 | 2616 |
|---|---|---|---|---|
| a/L threshold | 0.99353 | 0.99898 | 0.99975 | 0.99990 |

So the conclusion flips only if a/L > 0.9935, which is the "a/L > 0.99" condition. At L = 2 cm that means a ≳ 19.87 mm.

**Flip threshold on taper.** I model `EI(s) ∝ s^n`, with stiffness tending to zero at the tip. Then φ = (a/L)^{4−n} for n < 4, and the flip needs `4 − n ≤ ln(1−1/R) / ln(a/L)`:

| R | a/L = 0.005 | 0.0075 | 0.015 | 0.06 |
|---|---|---|---|---|
| 39 | n ≥ 3.9951 | 3.9947 | 3.9938 | 3.9908 |
| 981 | n ≥ 3.99981 | 3.99979 | 3.99976 | 3.99964 |

So the flip needs n > 3.99 for every adult case, and n > 3.9938 for the a/L values in the claim.

## 4. Caveats I add (my inference, not the claim author's)

1. **n = 4 is not exotic.** It is what a solid circular ray gives if its radius tapers linearly to a point (`I ∝ r⁴`). At n = 4 the compliance integral diverges logarithmically. So the "n > 3.99" escape sits right next to a simple geometric idealisation. The physical reason it does not apply is that real rays do not taper to zero radius at the tip. Puri 2018 reports a measured `EI` that varies only ~2.7× (1.5–4×10⁻⁹) along the fin, which is nothing like a power law going to zero.
2. **Using Puri's profile bounds φ but loosens the 10⁻⁷ figure.** If `EI` varies by a factor of at most 4/1.5 along the span, then φ ≤ 2.67 × (a/L)⁴. At L = 2 cm and a = 300 µm that gives ≤ 1.35×10⁻⁷. That is slightly above the claim's "<10⁻⁷" but still negligible by 7 orders of magnitude, so the conclusion does not change. Strictly, "<10⁻⁷" holds for uniform `EI`, and the bound is ~1.4×10⁻⁷ under the measured stiffness variation.
3. **`a` is unverified by me** (search-summary only; see §1). The conclusion survives any `a` up to 99 % of `L`, so this does not matter for the verdict.
4. **Full-span larval fin fold.** If a/L = 1, then φ = 1 and the bound disappears. The outcome is then set by the material modulus, as S23-D's f = 1 case was. I agree with the claim's last clause on structural grounds. I did not re-derive the E0 dependence.

**My value.** Uniform-load cantilever (my calculation): the distal 200–300 µm carries φ = 6×10⁻¹⁰ to 5×10⁻⁸ of tip compliance (≤1.4×10⁻⁷ allowing Puri's ~2.7× stiffness variation). The flip requires a/L ≥ 0.9935 (R = 39) to 0.99975 (R = 981), or a taper exponent n ≥ 3.991–3.9998.

## 5. Comparison with the recorded value (read after §1–§4 were done)

I then grepped `S23-D-deepen.md` on `claude/deepen-s23-sensitive-input-hynbng`. Its recorded figures are:
- φ = (a/L)⁴ = 1.0×10⁻⁸ to 5.1×10⁻⁸ at L = 2 cm, and 3.2×10⁻⁹ at L = 4 cm
- flip at a/L ≥ 0.9936
- taper flip at n ≥ 3.994 (a = 300 µm)
- R = 39.2 (lenient) to 981 (central)

These match my numbers to the stated precision. The file sources `a` from Tanimoto et al. 2026 (PMC13573005), which gives about 200 µm, and from Hanzelova et al. 2026 (PMC13120675), which gives 200–300 µm citing Nakagawa et al. 2022. I did not read those sources myself.

**Verdict: AGREE.** One refinement: "<10⁻⁷" is exact only for uniform `EI`. With the measured non-uniform profile the bound is ~1.4×10⁻⁷, and the conclusion is unchanged.

Sources used in this replication:
- [ZFIN ZDB-PUB-170802-15](https://zfin.org/ZDB-PUB-170802-15) — search-summary
- [ZFIN ZDB-PUB-210922-3 figures](https://zfin.org/action/publication/ZDB-PUB-210922-3/all-figures) — search-summary
- `S23-protein.md` (repo) — full-text

```swarm-replication
{"claim_id": 138, "my_value": "distal 200-300 um carries phi=(a/L)^4 = 6e-10 to 5.1e-8 of tip compliance (<=1.4e-7 with Puri's 2.7x EI variation); flip needs a/L>=0.9935 (R=39) or taper n>=3.991", "agrees": true,
  "note": "Unit-load integral reproduces phi=(a/L)^4, a/L flip 0.9935 and n flip ~3.994; the <1e-7 bound holds for uniform EI but loosens to ~1.4e-7 under measured EI variation, with no change to the conclusion."}
```
