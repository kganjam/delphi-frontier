# F001 target specification v0: Fisher's fundamental theorem, partial-change form

Status: UNFROZEN DRAFT, single reader (claude-fseries agent, Claude). Not a proof. No Lean or other prover was run for this document. Lean work in this hackathon belongs to ff-xenomodel / claude-xenomodel. This spec is the input to that work and to an independent statement-fidelity review. It is not the output of either.

Record under target: `fisher-ftns`, `scopedesk/scorecard/records/fisher-ftns.json` at delphi-evolve `work/rethink-critic` (27ac6925), content sha256 `069a09125bf6923a630c23551826cfa9543e933ec547a24adb1fb2a5d7e3132a`. The record's math field reads `Δ_NS w̄ = V_A(w)/w̄ (discrete generations); dm̄/dt|_NS = V_A(m) for Malthusian fitness m`. The F004 review of this record is in `../F004.md`; its proposed corrections (C-F1 to C-F7 in `../F004/corrections-v1.json`) are taken into account here.

## 0. Sources this spec rests on, and how far

| Source | Read? | What is used |
|---|---|---|
| Fisher 1930, *Genetical Theory*, ch. II, pp. 30-35 (two independent archive.org scans of the 1930 Clarendon printing, receipts `fisher1930`, `fisher1930_dli` in `../F004/receipts/sources-v1.json`) | read (OCR; some displayed equations on pp. 34-35 are missing from one scan and present in the other) | average excess (p. 30), average effect (p. 31), genetic value X as a least-squares-type fit with Σ X(x−X)=0 (p. 32), W = Σ pqaα = Var(X) (p. 33), application to Malthusian m and the theorem statement (pp. 34-35), reproductive-value weighting and the exclusion of fluctuations (p. 35) |
| Frank 1998, *Foundations of Social Evolution*, ch. 2, pp. 16-23 (author-hosted PDF) | read | breeding value as best linear predictor on allele counts (eq. 2.5ff), Price form (2.6-2.8), partial change Δ_f w̄ = Cov(w,g)/w̄ = V_g/w̄ (2.10), Δ_f w̄ = Σ Δq_i g_i = n Σ Δr_j b_j |
| Frank 2012, J Evol Biol 25:1002 (author-hosted PDF) | read (section on partial change, eqs. 7-8) | Δ_s z = Cov(w,z)/w̄ as "partial change", attributed to Fisher 1930, Price 1972b, Ewens 1989, Frank & Slatkin 1992 |
| Ewens 1989, Theor Popul Biol 36:167 | abstract only (Europe PMC) | "correct as a mathematical statement, but of less biological value than was claimed" |
| Grafen 2021, Ecol Evol 11:735 (open access, PMC7820154) | read in part (grep of introduction) | consensus summary: the left side is a partial change, following Price 1972b |
| Price 1972, Ann Hum Genet 36:1 | **not read** (paywalled) | nothing used directly. Every "Price 1972" attribution here comes from Frank 1998/2012 |
| Frank & Slatkin 1992, TREE 7:92 | **not read** | nothing used directly |
| Edwards 1994, Biol Rev | **not read** | nothing used directly |

## 1. Population model (one generation, discrete)

- A finite, nonempty type set `ι` (genotypes, or individuals as types). Frequencies `q : ι → ℝ` with `q i ≥ 0` and `Σ q i = 1`.
- Fitness `w : ι → ℝ` with `w i ≥ 0` and `w̄ := Σ q i w i > 0`. Wrightian: the expected number of successful gametes or offspring per individual of type i over one generation, in absolute or relative units. The identity is homogeneous of degree 1 in w, so `Δ_NS w̄ / w̄ = V_A(w/w̄)`.
- Loci and alleles: a finite set `J` of allele labels, partitioned into loci. Gene counts `x : ι → J → ℕ` with `Σ_{j ∈ locus ℓ} x i j = n` (ploidy n, the same for every type; n = 1 haploid, n = 2 diploid). Only gene counts may be predictors. Constant ploidy is a v0 simplification: it excludes sex-linked loci and haplodiploidy. Neither the normal equations nor T1 need it (see §8 note). The predictor set must not contain w or any function of w that is not a function of the gene counts (see §6, guard G1).
- No assumptions about Hardy-Weinberg proportions, linkage equilibrium, mating system, dominance or epistasis. The regression handles all of these. They matter only for what *total* change does (§5).
- Fair transmission (Mendelian segregation, no meiotic drive, no mutation) is not needed for the partial-change identity as defined in §3. It is needed only to read §3's Δ_NS as "selection-caused change in allele frequency times average effect" (§3, remark R2).

## 2. Genetic projection (average effects, additive genetic value)

Fisher 1930 p. 32: the "expected value X" is built from increments per gene and fixed by the criterion that "in each such moiety the sum of the deviations, x − X, is zero", so that "the sum for the whole population of the product X(x − X) ... must be zero". This is the q-weighted least-squares projection of the trait on the span of {1, gene counts}. Frank 1998 p. 17 says the same thing ("the best linear fit").

Definition (projection). Coefficients `a : ℝ`, `b : J → ℝ` are *a least-squares fit of w on x under q* iff the residual `δ i := w i − g i`, with `g i := a + Σ_j b j · x i j`, satisfies the normal equations

- (N0) `Σ q i δ i = 0`
- (Nj) `Σ q i δ i x i j = 0` for every j ∈ J.

`g` is the **additive genetic value** (breeding value), the `b j` are **average effects**, and `V_A(w) := Var_q(g) = Σ q i (g i − ḡ)²`.

Facts the formal target must contain or rely on:
- Existence: the normal equations always have a solution (the Gram matrix is PSD). Uniqueness: b is not unique when the counts are collinear (they always are within a locus, since Σ x = n). The fitted values g are unique on the support of q. So V_A and Δ_NS (§3) are well defined. The Lean target can take "(a,b) satisfies N0, Nj" as a hypothesis. A separate existence lemma makes it non-vacuous.
- From (N0) and (Nj): `Cov_q(δ, g) = 0`, hence `Cov_q(w, g) = Var_q(g) = V_A`. This is Fisher's "variance of X is equal to the mean value of Xx" (p. 32).

## 3. Partial change ("due to natural selection")

Selected (parental-contribution) frequencies `q*_i := q i w i / w̄`.

Definition. `Δ_NS w̄ := Σ_i (q*_i − q i) · g i`, with **g and b held at their parental-generation values**.

Equivalently `Δ_NS w̄ = Σ_j b j · (E_{q*}[x_j] − E_q[x_j])`: average effects times the selection-caused change in mean gene count. Each mean count equals n times an allele frequency. This is Fisher's Σ α dp (p. 35, "an increase αdp in the average fitness ... where" α is the average effect) and Frank 1998's `Δ_f w̄ = Σ Δq_i g_i = n Σ Δr_j b_j`.

What is held fixed: the map from gene counts to g (the average effects). The "environment" in Fisher's sense (Frank 1998 p. 20: "every aspect of change in the genetic system, in interactions among individuals, and in the physical environment") is everything that changes the average effects or the fitness map between generations. Δ_NS deliberately excludes all of it.

Remarks.
- R1. Δ_NS is not the total change w̄' − w̄. W1 in §6 shows a case with Δ_NS = 1/28 and total change 13/392.
- R2. Under fair meiosis, the mean gene count among offspring equals E_{q*}[x_j]. Δ_NS is then "the change in mean breeding value from parents to offspring, evaluated with fixed average effects". Without fair meiosis or with mutation, §3's definition still holds as stated: it uses selected frequencies, not offspring frequencies. Then it is the selection component only. This is Frank 1998's reading ("partial changes caused by differential fitness"), not Fisher 1958's narrower reading. A reviewer must decide which reading the record means.

## 4. Target statements

T1 (discrete, Wrightian). Under §1-§3: `Δ_NS w̄ = V_A(w) / w̄`.

Proof route (for orientation, not a proof): `w̄ · Δ_NS w̄ = Cov_q(w, g)`. This is Price's selection term with z = zDesc = g. Then `Cov_q(w,g) = Var_q(g)` by §2.

T2 (continuous, Malthusian, one instant). Types i with Malthusian parameters `m i ∈ ℝ` (sign unrestricted), frequencies q as above, and selection-caused frequency rates `q̇ i := q i (m i − m̄)`. With g the least-squares projection of m on gene counts, `Σ_i q̇ i g i = V_A(m)`. This is Fisher's statement "rate of increase in fitness ... equal to its genetic variance in fitness" (p. 35) in his own fitness measure m (p. 34, "the special characteristic m which measures the relative rate of increase or decrease"). No division by mean fitness appears. T2 is the same finite algebra as T1 (replace q*−q by q̇ and drop the 1/w̄). T2 is a statement about an instant. It is not a statement about an ODE solution.

Out of scope for v0: age structure. Fisher p. 35 requires the ratio p:q to be counted over "all individuals having reproductive value, weighted according to the reproductive value of each". The v0 target has no age classes. Stating T2 for an age-structured population requires reproductive-value weights and is a separate target. Also out of scope: stochastic fluctuation (Fisher p. 35: "the theorem is exact only for idealized populations, in which fortuitous fluctuations in genetic composition have been excluded").

Open fidelity question F-Q1 (factor of 2 for diploids). Fisher 1930 writes the per-factor contribution as `pqaα` (p. 32-33: "the contribution of that factor to the genetic variance is represented by the expression pqaα"), the dynamics as `dp = pqa dt`, and the selection increment as `αdp = pqaα dt` (p. 35). Both 1930 scans read it this way. Under random mating a = α, so that gives `pqα²`. The regression definition in §2 gives `V_A = 2pqα²` for a diploid locus in Hardy-Weinberg proportions (W1 below: α = b = 1/4, p = 1/2, V_A = 1/32 = 2pqα²). The selection-caused change in mean breeding value is `2α dp`, since a diploid carries two copies. So Fisher's 1930 expressions and the regression convention differ by a factor of 2 for diploids, unless Fisher's p, dp or α are scaled per gene in a way I have not identified. A Gemini critique asserted that Fisher writes `2pqaα`. That is contradicted by both 1930 scans. The 1958 second edition, which may differ, was not read. The target as written uses the regression convention (Frank 1998 eq. 2.10). A reviewer must settle this (record correction C-F7).

## 5. Assumptions, all explicit

| # | Assumption | Needed for | Source locator |
|---|---|---|---|
| A1 | finite types, q ≥ 0, Σq = 1 | all | modelling choice |
| A2 | w ≥ 0 and w̄ > 0 (T1 only); w ≥ 0 only to give a population interpretation, since the algebra needs only w̄ ≠ 0 | T1 | Price.lean `Population` |
| A3 | predictors are gene counts with fixed ploidy n | definition of V_A as *genetic* | Fisher p. 30-32; Frank 1998 p. 17 |
| A4 | (a,b) satisfy the q-weighted normal equations | Cov(w,g) = Var(g) | Fisher p. 32; Frank 1998 p. 17 |
| A5 | average effects held fixed (definition of Δ_NS) | the "partial" in partial change | Fisher p. 35 (αdp); Frank 1998 p. 20-21 citing Price 1972b and Ewens 1989 (not read) |
| A6 | one generation (T1) or one instant (T2) | no dynamics claimed | — |
| A7 | no reproductive-value weighting, no age structure | v0 scope | Fisher p. 35 requires it in general |
| A8 | deterministic (no drift) | v0 scope | Fisher p. 35 |

Not assumed, and the target must not assume them: Hardy-Weinberg, linkage equilibrium, no dominance, no epistasis, constant fitnesses, weak selection.

## 6. Controls that separate total from additive variance (computed)

Script: `variance_witness.py` (stdlib, exact rationals, run as `python3 -I variance_witness.py` with Python 3.13.12). Full output: `variance_witness.out.txt`. Script sha256 `d76099f8ba06616a851b0acdc5d21936b255232bb44a4345e4eb3bcd067f5c9c`, output sha256 `e104629bdbf8c138be1a326740979e8fd40852871406d972398df46e4aa62abf`. For every case the script asserts the normal equations and asserts `Δ_NS w̄ = Σ_j b_j ΔE[x_j] = V_A/w̄` exactly.

| Case | Model | w̄ | Var(w) | V_A(w) | Δ_NS w̄ = V_A/w̄ | Var(w)/w̄ (Price `fitness_selection`) | total Δw̄ after random union |
|---|---|---|---|---|---|---|---|
| W1 | diploid, 1 locus, complete dominance (1, 1, 1/2), p = 1/2, HW | 7/8 | 3/64 | 1/32 | 1/28 | 3/56 | 13/392 |
| W2 | diploid, overdominance (4/5, 1, 3/5) at equilibrium p* = 2/3 | 13/15 | 4/225 | 0 | 0 | 4/195 | 0 |
| W3 | haploid, 2 loci, AB = 2, others 1, linkage equilibrium, all freq 1/4 | 5/4 | 3/16 | 1/8 | 1/10 | 3/20 | (not computed) |
| C1 | diploid, no dominance (3/2, 5/4, 1), p = 1/3, HW | 7/6 | 1/36 | 1/36 | 1/42 | 1/42 | 1/42 |
| C2 | haploid, 1 locus, 2 alleles, fitness (3/2, 1), freq (1/3, 2/3) (saturated regression) | 7/6 | 1/18 | 1/18 | 1/21 | 1/21 | (not computed) |

Uses in the formal target:
- G1 (anti-substitution guard). A statement that is also true with V_A replaced by Var(w) is not the Fisher target. W1, W2 and W3 each make `Δ_NS w̄ = Var(w)/w̄` false. At least one of them should be compiled as a witness theorem in the same compilation unit. W2 is the sharpest: V_A = 0 while Var(w) > 0.
- G2 (anti-total guard). A statement whose left side is total change is false for W1 (13/392 ≠ 1/28). It should appear as a negative witness.
- G3 (non-vacuity). C1 and C2 show that the hypotheses are satisfiable and that the partial and total forms agree where the literature says they should (additive diploid, haploid single locus).

## 7. Reuse of the existing Price identity: type and assumption check

I read two Price files. The probe version is the one to reuse.

- delphi-evolve `b4e60db9:experiments/price_probe/Price.lean` (sha256 `a5d38f13...fd0a`), namespace `DelphiPrice`: `mean p x := Σ p i * x i`, `cov p x y := mean p (x*y) − mean p x * mean p y`, `descendantMean p w zDesc := mean p (w*zDesc) / mean p w`. `price` and `selection_only` require only `mean p w ≠ 0`. `cov_add`, `cov_scale`, and `cov_const` (the last needs `Σ p = 1`) are exactly the lemmas needed to turn (N0, Nj) into `cov p δ g = 0`. Fit: frequency-weighted, real-valued, finite `ι`. This matches §1. Δ_NS in §3 equals `descendantMean p w g − mean p g` by unfolding definitions (`Σ q*_i g_i − Σ q_i g_i`). So T1 is `selection_only p w g` plus `cov p w g = cov p g g`. Gap: `fitness_selection` (z = w) gives `cov p w w = Var(w)`. Its own docstring says it is NOT the additive FTNS, and W1-W3 show it is a different statement.
- delphi-evolve `work/rethink-critic:lean_price/Price.lean` (sha256 `c429c8f4...258a`), namespace `PriceProbe`: unweighted `E f := (Σ f i)/card ι` over individuals, `w` any real with `Σ w ≠ 0`. Usable only if types are individuals of equal weight. It is not directly a frequency model. Using it would need a weighted-mean bridge. Recommendation: reuse the `DelphiPrice` version.

Neither file defines gene counts, projections, or a partial-change operator. Those are the new content of this target.

## 8. Lean signature sketch

```lean
-- UNFROZEN DRAFT — not compiled. Not run through any prover. Names, universes and
-- Mathlib API are guesses; owner of Lean work: ff-xenomodel / claude-xenomodel.
import DelphiPrice  -- experiments/price_probe/Price.lean @ b4e60db9
namespace FisherTarget
open DelphiPrice
variable {ι J : Type*} [Fintype ι] [Fintype J]

/-- additive genetic value from intercept a and average effects b on gene counts x -/
def addVal (x : ι → J → ℕ) (a : ℝ) (b : J → ℝ) : ι → ℝ :=
  fun i => a + ∑ j, b j * (x i j : ℝ)

/-- (a,b) is a q-weighted least-squares fit of w on gene counts x (normal equations) -/
structure IsLSFit (q w : ι → ℝ) (x : ι → J → ℕ) (a : ℝ) (b : J → ℝ) : Prop where
  n0 : mean q (fun i => w i - addVal x a b i) = 0
  nj : ∀ j, mean q (fun i => (w i - addVal x a b i) * (x i j : ℝ)) = 0

/-- ploidy constraint: each locus carries exactly n gene copies in every type -/
def Ploidy (locus : J → L) (n : ℕ) (x : ι → J → ℕ) : Prop :=
  ∀ i ℓ, (∑ j in Finset.univ.filter (fun j => locus j = ℓ), x i j) = n

def VA (q : ι → ℝ) (g : ι → ℝ) : ℝ := cov q g g

/-- partial change: selected-frequency change weighted by FIXED additive values -/
def partialChange (q w g : ι → ℝ) : ℝ := descendantMean q w g - mean q g

theorem ftns_discrete (q w : ι → ℝ) (x : ι → J → ℕ) (a : ℝ) (b : J → ℝ)
    (hq0 : ∀ i, 0 ≤ q i) (hq1 : ∑ i, q i = 1) (hw0 : ∀ i, 0 ≤ w i)
    (hwbar : 0 < mean q w) (hfit : IsLSFit q w x a b) :
    partialChange q w (addVal x a b) = VA q (addVal x a b) / mean q w := by
  sorry

-- Malthusian, one instant: rates qdot i = q i * (m i - mean q m)
theorem ftns_malthusian_instant (q m : ι → ℝ) (x : ι → J → ℕ) (a : ℝ) (b : J → ℝ)
    (hq1 : ∑ i, q i = 1) (hfit : IsLSFit q m x a b) :
    ∑ i, (q i * (m i - mean q m)) * addVal x a b i = VA q (addVal x a b) := by
  sorry

-- required companions: existence of an LS fit; witness theorems W1 (or W2) showing
-- partialChange ≠ cov q w w / mean q w, and W1 showing total change ≠ partialChange.
end FisherTarget
```

Notes on the sketch. `hq0`, `hw0` and the strict `hwbar` are interpretive. The algebra needs only `mean q w ≠ 0` (as in `selection_only`) and `Σ q = 1` (for `cov_const`). A reviewer should decide whether the frozen statement carries the interpretive hypotheses, as `DelphiPrice.Population` does, and apply the same choice to both theorems. `Ploidy` needs `[DecidableEq L]` and a binder for `L`. `Ploidy` is not used by `ftns_discrete`: the identity holds for any real predictors. That is a fidelity point in its own right. The algebra does not need genetics. Genetics enters only through what x is allowed to be (guard G1) and through how Δ_NS is read (R2). A reviewer should decide whether to keep x : ℕ-valued gene counts with `Ploidy` as a hypothesis for interpretive fidelity even though the proof ignores it. `L` in `Ploidy` is an unbound locus type in this draft.

## 9. What the acceptance criterion still requires (not done here)

1. Independent statement-fidelity review of §2-§4 against Fisher 1930 ch. II and against Price 1972b and Ewens 1989. A different reader is needed, and so is access to the two papers I did not read. Open item F-Q1 (the factor of n) and remark R2 (which reading of "due to selection") must be settled.
2. Exact target freeze: a hash of the frozen statement file, after review.
3. Compile, by the Lean owner: T1, and T2 if kept, plus existence of the LS fit and the witnesses W1/W2 (negative: ≠ Var(w)/w̄; negative: ≠ total change) and C1 (non-vacuity).
4. Standard axiom audit (`#print axioms` showing only propext, Classical.choice, Quot.sound) and no `sorry`.
5. A projection/covariance correspondence proof that `cov q w g = cov q g g` follows from IsLSFit. This is the step that separates the target from `fitness_selection`.

None of 1-5 is done. This document does not answer F001's question. It proposes a candidate answer for review.

## 10. External critique log

One critique pass, model `gemini-4-argon` (Google Generative Language API, `generateContent`), 2026-11-01 08:58 PST. Input: this spec and `../F004/corrections-v1.json`, both as drafted at that time. The prompt asked for concrete errors only. The critique is not a review of record and not an independent human review.

| Critique point | Response |
|---|---|
| Fisher 1930 writes 2pqaα, not pqaα, so F-Q1 is an OCR artifact | **Rejected after checking.** A second, independent 1930 scan (`fisher1930_dli`) also reads `pqaα`, `dp = pqa dt` and `αdp = pqaα dt`. F-Q1 stays open and now states the evidence. Added record correction C-F7. |
| `Δ_NS w̄/w̄ = V_A(w/w̄)` is wrong | Rejected. V_A(w/w̄) = V_A(w)/w̄², and Δ_NS w̄/w̄ = V_A(w)/w̄². The critique's own derivation ends at the same identity. |
| Constant ploidy excludes sex linkage and haplodiploidy | Accepted. Recorded as a v0 scope limitation in §1. |
| C1/C2 rows lack HW and parameters | Accepted. Added. |
| Lean sketch: unused positivity hypotheses, asymmetric between theorems; `Ploidy` needs `DecidableEq L` | Accepted as notes in §8. Not resolved: this is for the reviewer or freezer. |
| F004 C-F5 example "no dominance" is not a case "with dominance" | Accepted. C-F5 now cites W2 (overdominance at equilibrium, both changes 0) and treats the additive case separately. |
| F004 C-F6 misattributes the transmission term to Robertson | Accepted. Locator reworded. |
| F004 C-H2 should say joint least squares with intercept (residual orthogonal to g) | Accepted. |
| F004 C-H5 rescaling needs a positive constant; polygenic g is not a single-gene frequency | Accepted. |
| F004 C-H1 attribution wording | Accepted in part. The rationale now states what Frank 1998 credits to Hamilton 1970 and to Queller 1992. |
| Date and timezone of the corrections file are wrong | Rejected. The session date is 2026-11-01. Seattle is on PST after 02:00 that day. |
