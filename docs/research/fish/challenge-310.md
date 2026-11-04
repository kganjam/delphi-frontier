# Challenge 310 — adversarial review of S43 (pectoral fin area, lat4a^nr21/+; kcnh2a^lof/+)

**Verdict: WEAKENED.** The sample-size arithmetic checks out *for the CV the author assumed*. The headline
rationale, that "measuring area rather than length cuts the required n about four-fold", does not hold
under the most ordinary model of fin-size variation. In that model area gives almost no power gain at all.

Source `harvest:zebrafish-fin-area-protocol-xy8ijv`: **could-not-access**. It is not in this repository.
I searched all `*.md` files for `lat4a`, `kcnh2a` and `fin area` and found no matches. I judged the claim
only on the text quoted in the challenge.

## 1. Independent arithmetic (calculated, not observed)

I used a two-sided two-sample t-test with the exact noncentral-t power and searched over n per group
(scipy, written for this review):

| Scenario (all calculated) | Standardised effect d | n per group for 90 % power, α = 0.05/3 |
|---|---|---|
| Author's case: area effect 10.25 %, CV_area = 0.10 | 1.025 | **28** |
| Length effect 5 %, CV_length = 0.10 | 0.50 | 110 |
| Area effect 10.25 %, CV_area = 0.20 (= 2 × CV_length) | 0.5125 | **105** |
| Area effect 10.25 %, CV_area = 0.15 | 0.683 | 60 |
| Area, CV_area = 0.10, tested as a 2×2 *interaction* contrast | 0.725 | 53 |
| Area, CV_area = 0.20, tested as an interaction contrast | 0.362 | 208 |

- 1.05² = 1.1025, so the 10.25 % figure is correct.
- α = 0.05/3 = 0.0167 is Bonferroni over 3 comparisons, which is consistent.
- n = 28 rounds up to the stated 30. **Under its own inputs the KEY number is right.**
- A cross between a double heterozygote and wild type gives four classes at 25 % each. From 200 genotyped
  fish the expected count is 50 per class. The binomial 1st percentile of Bin(200, 0.25) is about 35, so
  getting at least 30 fish per class is safe. (This is my inference. The claim does not name the cross design.)

## 2. Proxy and hidden assumption: CV_area = CV_length

The claimed four-fold saving is (10.25/5)² ≈ 4.2. That holds only if area and length have the **same
residual CV**. Area scales roughly as length², so to first order:
- CV_area ≈ 2·CV_length, and
- Var(log A) = 4·Var(log L).

The genotype effect on log area is also exactly 2× the effect on log length. The signal-to-noise ratio
therefore stays the same, and the power gain disappears. In the table, length at CV 0.10 needs 110 fish per
group, and area at CV 0.20 needs 105. That is about a 5 % saving, not a 4-fold one.

Area beats length by roughly 4× only when the residual is dominated by **measurement error that does not
double**: for example, segmentation noise in area that is smaller than 2 × the error of a length landmark.
Most fin-size variation is biological (between-fish size scatter that remains after SL adjustment), and
that component scales as length². This is my inference from the scaling identity, not a measured result.
The author does plan a pilot to estimate CV, which is the right defence. But the pilot is budgeted
to estimate CV_area. It cannot rescue the "four-fold" statement, which is a property of the variance
structure and not of the protocol.

**Relaxed:** if the pilot returns CV_area ≈ 0.15–0.20, the design needs 60–105 fish per class (240–420
measured, about 320–560 genotyped from several clutches). That is 2–3.5× the 120/200 budgeted. The
$12.2–18k cost and 32-week timeline were not re-derived. I had no access to the costing inputs, so
they are `unknown`.

## 3. Is the right contrast being powered?

The claim powers pairwise comparisons, Bonferroni ×3. If the scientific question is whether the two alleles
**interact** (whether the double heterozygote departs from additivity), the relevant test is the 2×2
interaction contrast. Its variance is 4σ²/n rather than 2σ²/n, which roughly doubles n: 53 at CV 0.10 and
208 at CV 0.20. This is my inference about intent. The quoted claim does not say which hypothesis it tests.

## 4. Allele biology (scope-limited)

From memory only (read-level: **could-not-access**, nothing fetched): the zebrafish *longfin* allele `lof`
has been reported to cause cis-ectopic expression of *kcnh2a*, which prolongs fin outgrowth. That makes it a
dominant gain-of-function-like allele, not a loss-of-function one. A reader could misread "kcnh2a^lof" as
loss-of-function. If heterozygous *lof* alone produces a large fin overgrowth, a 5 % length effect is an odd
target for any contrast involving the *lof* classes. I did **not** verify the effect size of *lof*/+ on the
pectoral fin. I also did not verify that `lat4a` or the `nr21` allele exist, so their status is `unknown`.
I treat none of this as a refutation.

## 5. Evidence level

The claim records evidence level "derived" and value "n/a". That is honest: n = 30 is a calculation from an
assumed CV = 0.10, and the claim says so. The one defect is the "four-fold" sentence. It is stated as a fact
about area versus length, but it depends on an unstated assumption that is probably false.

## Corrected statement

At CV_area = 0.10, n = 28 → 30 per class is a correct calculation. The "≈4× fewer fish than length" claim
should be withdrawn. If variation is size-driven (CV_area ≈ 2·CV_length), area and length need about the same
n: about 105 vs 110 per class for a 5 % length effect at CV_length = 0.10. Budget for up to about 105 per
class until the pilot measures CV_area directly.

```swarm-challenge
{"claim_id": 310, "outcome": "weakened", "reason": "n=30/genotype is arithmetically correct only at the assumed CV_area=0.10, but the claimed ~4-fold saving from measuring area instead of length assumes CV_area equals CV_length, whereas size-driven variation gives CV_area~2xCV_length and erases the gain (105 vs 110 fish/group, calculated).", "corrected_value": "28-30 fish/genotype if CV_area=0.10 (as claimed); ~105 fish/genotype if CV_area=0.20 (=2x CV_length 0.10); area-vs-length saving ~1.05x, not ~4x", "depends_on": ["two-sample t-test, two-sided, alpha=0.05/3, power=0.90", "area effect = 1.05^2-1 = 10.25%", "isometric scaling A proportional to L^2 so CV_area ~ 2*CV_length when residual is biological", "CV_length = 0.10 assumed for the length comparison", "pairwise rather than interaction contrast as the claim's test"]}
```
