# Result — full 6,789-variant Kir2.1 run

**Kind:** computational replication on public data. Not new channel biology.
**Preregistration:** [`PREREGISTRATION-full.md`](../../experiments/bioservices/kir21_esm2_assay_agreement/PREREGISTRATION-full.md),
frozen at commit `a940673` before the run.
**Verdict on H1: UNDETERMINED**, from the governing (position-clustered) interval.
The 256-variant verdict is retained as its own result, not replaced.

## Headline

| Predictor | ρ surface | ρ function | Δρ variant-level | Δρ clustered (391) | H1 |
| --- | --- | --- | --- | --- | --- |
| **ESM-2 650M** | **+0.353** [+0.331, +0.374] | **+0.388** [+0.367, +0.408] | **−0.035** [−0.062, **−0.009**] | **−0.035** [−0.090, **+0.018**] | **undetermined** |
| BLOSUM62 | +0.177 [+0.154, +0.199] | +0.101 [+0.077, +0.123] | +0.076 [+0.049, +0.104] | +0.076 [+0.040, +0.111] | **supported** |

n = 6,789 over 391 positions, none dropped. 10,000 resamples, seed 0.

## The preregistration earned its keep

**The variant-level interval excludes zero. The position-clustered interval does
not.** Reporting only the first would have announced H1 *falsified*. The
clustered interval is the one that respects variants at a position sharing a
residue, an environment and a single forward pass, and under the rule fixed in
the parent protocol — **where they disagree the wider governs** — the answer is
UNDETERMINED.

This exact scenario was written down in advance, before any number existed:

> *"the variant-level interval will tighten to a scale comparable with the
> external comparison's 0.030, and the position-clustered interval will not. If
> the clustered interval governs, the full run may well return UNDETERMINED
> again."*

**Three of the four tests say the difference is real, and all three assume
independence.** The paired permutation (p = 0.0103) and Williams (p = 0.0065)
both operate on variants, not positions, so they share the variant-level
interval's assumption. They are not independent corroboration of it. The one
procedure that drops that assumption is the one that returns undetermined.

## This pipeline reproduces ProteinGym's published numbers

| | surface | function | Δρ |
| --- | --- | --- | --- |
| ProteinGym v1.3 table (full datasets) | 0.352 | 0.382 | −0.030 |
| **This run (full matched set)** | **0.353** | **0.388** | **−0.035** |
| This run (256-variant subset) | 0.299 | 0.334 | −0.035 |

The 256 result noted that its correlations sat ~0.05 below ProteinGym's and
called that "a question to investigate, not a correction issued to ProteinGym."
**The question is now answered, and in ProteinGym's favour:** at full scale the
values land within **0.001 and 0.006** of the published figures. The gap was
small-sample, not a pipeline discrepancy.

These remain two observed comparisons on overlapping-but-not-identical data
computed with different code. Close agreement is evidence the implementations
agree; it is not a validation of either against a known truth.

## The baseline behaves differently from the model, and that is the finding

BLOSUM62 — biochemical similarity, no model, no position, no context — agrees
**better with surface expression** than with function, significantly so under
both intervals (Δρ = +0.076, clustered [+0.040, +0.111]).

ESM-2 does not show that preference. If anything it leans the other way.

So "which assay is easier to predict" is **not** a fixed property of the two
assays: a composition-only predictor and a sequence model disagree about its
direction. A reading that treats surface expression as simply the easier target
is not supported. ESM-2 also beats BLOSUM62 on both assays, decisively on
function (+0.388 vs +0.101).

## Sensitivity (preregistration §5)

**Measured versus predicted narrowing.** The √n rule was close for the
variant-level interval and badly pessimistic for the clustered one:

| Interval | subset half-width | full half-width | measured | predicted |
| --- | --- | --- | --- | --- |
| Variant-level | 0.1509 | 0.0269 | **5.62×** | 5.15× (√n) |
| Position-clustered | 0.1620 | 0.0543 | **2.99×** | 1.42× (√clusters) |

I predicted ~1.42× for the clustered interval and it narrowed 2.99×. The √clusters
rule counts only added *clusters* and ignores that more variants per cluster also
sharpen the within-cluster estimate. **The prediction was right in direction and
wrong in magnitude, and the direction is what mattered** — the clustered interval
narrowed far less than the variant-level one and still spans zero.

**Cluster-count sensitivity, and the uncomfortable part.** Restricting to the same
193 positions the 256-variant subset covered, but using all 3,408 variants there:

| Set | clusters | n | Δρ clustered CI | half-width |
| --- | --- | --- | --- | --- |
| Restricted to the subset's 193 positions | 193 | 3,408 | **[−0.154, −0.001]** | 0.0763 |
| All positions | 391 | 6,789 | **[−0.090, +0.018]** | 0.0543 |

**These disagree about whether zero is excluded.** The restricted set excludes it,
barely; the full set does not. So the conclusion depends on *which* positions are
included and not only on how many. The 193 were chosen by hashing variant names,
with no reference to any measurement, so this is sampling variability rather than
selection — but it is reported because it bounds how firm "undetermined" is.

**Per-position balance.** 391 positions, 3 to 19 variants each, mean 17.36,
median 18, sd 2.43. Close to balanced, so cluster resampling is not dominated by a
few large clusters.

**Assay-to-assay ρ = +0.290** (0.270 on the subset). ESM-2 tracks each assay about
as closely as the two assays track each other.

## The reproduction control, and two mistakes in it

The control **passed**: 256 compared, 153 differ at the last bit, max relative
difference **5.9e-08** against a **4.76e-07** tolerance, **ranks identical**.

It failed twice first, and both failures were mine, not the model's:

1. It asserted **bit-for-bit** equality between two different arithmetic orders.
   The 256 run computed `float(lp[mut] − lp[wt])` — subtraction in float32, then
   widened. This run stores each log-probability as float64 and subtracts in
   float64. Same float32 inputs, different order, different last bits.
2. Replacing it, I tested ranks by asking whether **Spearman == 1.0** — the same
   exact-float comparison one level up. The correlation of two *identical*
   rankings came back as 0.9999999999999998. The check now compares rank vectors
   elementwise.

"My control failed" and "my control was mis-specified" look identical from
outside, and only one is a finding about the model. This was the second.

## Acceptance (self-assessed)

F1 all 391 positions scored · F2 reproduction control passed · F3 all eight
reference checks passed inside the run · F4 both intervals plus the four
sensitivity items · F5 **40.8 min** of scoring compute across 5 invocations,
inside the 60-minute bound.

**This is not independent review.** F1–F5 are this harness checking its own run
against criteria it fixed in advance. Under SPEC-005 the executor cannot certify
its own work, so this is a **proposed contribution carrying a self-assessment**,
not a Frontier-accepted result.

## Artifacts

| | |
| --- | --- |
| Analysis receipt | `kir21_full_analysis.json` (sha256 `d7eee7f5…94d6`) |
| Per-position log-probability vectors | `kir21_full_positions.json` — each with a sha256 of its masked input row |
| Derived scores + control | `kir21_full_positions_scores.json` |
| Predictions vs measurements | `kir21_full_predictions_vs_measurements.csv` (6,789 rows) |
| Figure | `kir21_full_predictions_vs_measurements.svg` |

Any future extension to variants at these 391 positions costs **no forward
passes** — the vectors are persisted, which the 256 run failed to do.

## Limitations

- One protein, two assays, one model, one checkpoint. Nothing generalises.
- Agreement is not mechanism, and neither assay is a claim about an organism.
- Function is measured downstream of surface expression, so these are not
  independent readouts; ρ = 0.290 is lower than that alone would imply.
- The two cluster sets disagree about whether zero is excluded (above).
- A difference in ρ can come from assay precision rather than from what the model
  represents.
