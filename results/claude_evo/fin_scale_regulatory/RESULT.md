# Evo 2 on fin/ray/scale regulatory windows: zebrafish and the one flying fish assembly

**claude-evo harness, 2026-11-01.** Two completed 1× H100 jobs. Every number
below comes from a job that reached a terminal state with exit code 0; receipts,
hashes and controls are in `MANIFEST.md`.

**What this is:** sequence likelihoods under one genomic language model, and
sequence that model generated. **What it is not:** an observation, a functional
enhancer, a validated design, or any claim about a live fish.

## 1. The result that survives scrutiny

Real regulatory windows beat **their own** dinucleotide-preserving scrambles.
Paired by window, so composition, GC and gene identity are held fixed:

| | n | mean log-prob/base | 95% CI |
| --- | --- | --- | --- |
| real held-out window | 19 | −1.2058 | [−1.2570, −1.1547] |
| dinucleotide shuffle of that window | 19 | −1.3502 | [−1.3654, −1.3351] |
| GC-matched random of that window | 19 | −1.3698 | [−1.3849, −1.3547] |
| uniform random (self-check) | — | −1.3997 | required near −ln 4 = −1.3863 |
| **paired real − own shuffle** | **19** | **+0.1444** | **[0.0980, 0.1908]**, t=6.53, p=3.9×10⁻⁶ |

This is the only comparison here that is neither circular nor cross-species.
It holds in **flying fish alone** (+0.0993, CI [0.0453, 0.1533], n=9), and that
is the part worth attention: `GCA_018398805.1` is almost certainly **not** in
Evo 2's training corpus, so that figure cannot be verbatim recall. Zebrafish is
+0.1850 (CI [0.1124, 0.2577], n=10) and carries less weight, being in-corpus.

**What it means:** Evo 2 assigns above-composition likelihood to these windows,
including in a species it has almost certainly never seen.
**What it does not mean:** it does **not** show the model read *cis*-regulatory
syntax. Beating a dinucleotide shuffle demonstrates structure above k = 2 —
higher-order Markov statistics, repeat structure, codon-like periodicity — and
nothing more specific.

## 2. The finding that tracks training-corpus membership — **WEAKENED by §7, read both**

> **Correction, added after the conditional-scoring job
> (`aijob-e00bvd85xvypgq1j6a`).** The significance reported in this section is
> partly an artefact of scoring unconditionally. Under the fair comparison —
> real continuation vs generated continuation given the **same** prompt, which
> is the quantity generation actually optimised — the overall real-vs-generated
> difference is **+0.0577, CI [−0.0169, +0.1324], p=0.122: not significant**,
> and the zebrafish gap falls to p=0.088. The *direction* and the species
> *ordering* below survive; the claim of a statistically reliable gap does not.
> §7 has the detail. I am leaving this section standing rather than rewriting
> it, so the correction is visible instead of silent.

Generated candidates were compared with the real windows, paired by window,
**scored unconditionally**:

| species | corpus status | real − candidate (paired) | p |
| --- | --- | --- | --- |
| zebrafish | GRCz11 **in** OpenGenome2 | **+0.1374** CI [0.0521, 0.2226] | 0.0054 |
| flying fish | `GCA_018398805.1` almost certainly **out** | **+0.0107** CI [−0.0727, +0.0940] | 0.78 |

The gap between real and generated sequence appears **only** where the model has
likely seen the real sequence. This is a *within-species* paired comparison, so
unlike the cross-species contrast in §4 it is **not** subject to the leakage,
window-definition or GC confounds — they cancel. **But see the correction above:
under conditional scoring neither species reaches significance.**

Two readings, and the honest position is that this single observation does not
separate them:
1. On novel sequence the model generates windows indistinguishable from real
   ones under its own likelihood.
2. The zebrafish gap is memorisation inflating the *real* row, rather than the
   candidates being worse.

They are not mutually exclusive and both predict exactly this pattern.
**Power caveat:** "indistinguishable" at n = 9 with a CI half-width of ±0.083 is
*absence of a detectable difference*, **not** demonstrated equivalence.

Candidates also beat their own scrambles (+0.0783, CI [0.0429, 0.1137], n=38,
t=4.48, p=6.8×10⁻⁵), in both species.

## 3. The candidates are not degenerate — and my own screen was wrong first

Argon's main worry was repetition collapse: a temperature-1.0 sample can
degrade into a repeat scoring near zero log-prob and beat real sequence as a
pure artefact. Run 1 produced exactly such a sequence. It did not happen here.

38/38 candidates sit inside or above the real-window complexity band:
gzip ratio 0.309–0.372 (real: 0.326–0.370), 6-mer fraction 0.695–0.886 (real:
0.673–0.846). If anything candidates are *slightly more* random-like than real
sequence, which is the opposite of collapse.

**My pre-registered flag rule fired three times and the rule was wrong, not the
candidates.** All three flags were `max_homopolymer >= 12`. Calibrating against
the real windows afterwards: they run to a **30 bp** homopolymer with a median
of 9, and **13 of 38** real windows exceed 12. A cutoff that flags sequence for
being *less* repetitive than the real thing measures nothing. Both counts are
reported in `armA/screen.json` — pre-registered 3, calibrated 0 — so the
goalposts are visibly not moved. The statistics that actually detect collapse
(gzip, 6-mer) flagged nothing under either rule, and the calibrated rule still
catches a planted `AT`×500 control.

**No evidence of verbatim retrieval.** Best 60 bp local identity of any
candidate against the held-out window it was never shown: max **0.283**, median
0.167. Zebrafish identity (0.150–0.217) is **not** higher than flying fish
(0.150–0.283). So whatever leakage does to likelihood, it does not operate by
reciting these windows.

## 4. The cross-species comparison, reported and void for biology

Zebrafish real windows score higher than flying fish, paired on the 9 shared
genes: **+0.1156, CI [0.0122, 0.2190]**.

**This number carries no evolutionary or regulatory information.** Three
confounds each independently predict the same sign before any biology enters:

1. **Training-corpus membership.** GRCz11 is in OpenGenome2; the flying fish
   assembly almost certainly is not. In-distribution versus out-of-distribution.
2. **Window definition.** Zebrafish windows are TSS-anchored and include UTR;
   flying fish windows sit upstream of a *predicted start codon* from a CDS-only
   GeneWise model with no TSS/UTR annotation. Fish 5′ UTRs often carry large
   introns, so those windows may be UTR intron or intergenic sequence rather
   than core promoter.
3. **Composition.** Flying fish GC runs systematically higher (0.349–0.577 vs
   0.256–0.408).

It is reported for completeness and must not be cited as a finding about flying
fish biology.

## 5. Claims explicitly refused

- **Not** that Evo 2 learned fin, ray or scale regulatory *grammar*. Every gene
  here (`shha`, `tbx5a`, `runx2b`, `lef1`, …) is a pleiotropic developmental
  regulator, not a fin- or scale-exclusive one. Nothing in this design could
  isolate a fin-specific signal.
- **Not** that flying fish regulatory regions are less conserved, more complex
  or harder to predict.
- **Not** that any candidate is an enhancer, is optimised, or would do anything
  in a cell.
- **Not** that beating a dinucleotide shuffle shows *cis*-regulatory syntax.
- **Not** that `top_k = 4` constrained base choice. Evo 2's tokenizer is
  byte-level, so it suppresses non-ACGT bytes and nothing more.
- **Not** that the candidate likelihoods are the quantity generation optimised:
  candidates were sampled as P(x | 1 kb prompt) but scored as unconditional
  P(x), the same treatment every group received.

## 6. Where this differs from the earlier bioservices run

Run 1 and its scoring job reported candidates "indistinguishable from real
promoters" (−1.2255 vs −1.2031, zebrafish only, unpaired groups). My paired,
two-species test finds real **ahead** of candidates overall (+0.0773, CI
[0.0153, 0.1393], p=0.017) — and §2 shows that overall gap is carried entirely
by zebrafish. The two results are consistent once pairing and corpus membership
are accounted for; the earlier framing simply could not see the split, having
only in-corpus windows and no composition-matched baseline for the real row.


## 7. Conditional scoring — the fair real-vs-generated test, and a correction

`aijob-e00bvd85xvypgq1j6a`, `EVOCD_RC=0`, 1× H100 80GB, 29.8 s, 76 rows. Arm A
sampled candidates as P(x | 1 kb prompt) but scored everything as unconditional
P(x). That is internally consistent, so arm A's group comparison stands — but it
is not the quantity generation optimised, and argon was right that it matters.
This job feeds prompt+continuation as one sequence and averages over the
continuation positions only, so every arm shares an identical conditioning
prefix. Gate specific to this job: conditioning on a real upstream prompt must
not flatter a random continuation — `cond_iid_given_real_prompt` = **−1.4059**,
below the −1.30 bar. Passed.

### The headline result gets *stronger*

| | paired mean | 95% CI | p |
| --- | --- | --- | --- |
| real − own dinucleotide shuffle, **unconditional** | +0.1444 | [0.0980, 0.1908] | 3.9×10⁻⁶ |
| real − own dinucleotide shuffle, **conditional** | **+0.1685** | **[0.1164, 0.2206]** | 2.3×10⁻⁶ |

§1 does not depend on the scoring convention.

### The real-vs-generated gap does *not* survive

| comparison (paired, same prompt) | mean | 95% CI | p |
| --- | --- | --- | --- |
| real − generated, all windows | +0.0577 | [−0.0169, +0.1324] | **0.122** |
| real − generated, zebrafish (in corpus) | +0.1061 | [−0.0192, +0.2314] | 0.088 |
| real − generated, flying fish (out of corpus) | +0.0039 | [−0.0845, +0.0924] | 0.921 |

Against the unconditional values (+0.0773 p=0.017; zebrafish +0.1374 p=0.005),
every one of these is weaker. **The mechanism is visible and not mysterious:**
conditioning helps the generated sequences (+0.0391, CI [0.0078, 0.0704]) about
twice as much as it helps the real ones (+0.0195, CI [0.0111, 0.0278]) — exactly
as expected, since the candidates were *sampled* under that prompt. Scoring
unconditionally therefore penalised the candidates relative to their own
objective, and part of the §2 significance came from that penalty rather than
from the sequences.

**What stands and what falls.** Zebrafish still shows the larger gap and flying
fish essentially none, so the species *ordering* in §2 is unchanged. The claim
that there is a statistically reliable real-vs-generated gap **falls**. The
honest summary is: under the fair test, Evo 2's own samples are not reliably
distinguishable from real held-out sequence by its own likelihood, in either
species, at n=10 and n=9.

## 8. Motif level: the result survives, and is strongest out of corpus

879 JASPAR2024 CORE vertebrate motifs, both strands, per-motif thresholds at
FPR 1×10⁻⁴, 5 dinucleotide-preserving shuffles per sequence. Pre-registered
primary endpoint: total hits, real vs own mean shuffle, paired. Run locally —
Nebius non-GPU vCPU quota was saturated tenant-wide (see `MANIFEST.md`).

| group | real hits | own-shuffle mean | **excess** | 95% CI | p |
| --- | --- | --- | --- | --- | --- |
| real held-out (n=19) | 391.9 | 266.6 | **+125.3** | [61.0, 189.7] | **0.00069** |
| ↳ flying fish (n=9) | — | — | **+181.4** | [75.2, 287.7] | 0.0043 |
| ↳ zebrafish (n=10) | — | — | +74.8 | [−5.8, 155.4] | 0.065 |
| generated (n=38) | 304.9 | 265.4 | +39.5 | [14.1, 64.9] | 0.0033 |

17 of 19 real windows carry more motif hits than their own scrambles, and
**9 of 9** flying fish windows do.

This is the motif-level version of §1 and it agrees with it. It also lands
hardest where memorisation cannot explain it: the out-of-corpus species shows
the larger and the more consistent excess, while zebrafish alone does not reach
significance. Generated sequence carries a real but much smaller excess (+39.5
against +125.3), which is the cleanest separation between real and generated
sequence anywhere in this work — notably clearer than the likelihood test in §7.

**Limits.** A single pooled background was used (per-sequence backgrounds cost
~3.8 h against ~6 min), so each window against its own shuffles is
composition-controlled and valid, but comparing *excess magnitudes between
species* is not confound-free — flying fish GC runs higher and absolute hit rates
scale with composition. Treat flying-fish-vs-zebrafish excess as descriptive.
Per-motif results are secondary and Holm-corrected in `motif/motif_hits.json`;
no individual motif claim is made here. And a PWM hit is a sequence match, **not
binding** — nothing here shows a transcription factor occupies these sites.

## 9. Where in each window the structure sits (tiling perturbation)

`aijob-e00ep572741570h1f8`, `EVOTL_RC=0`, 1× H100, 54.3 s. Each 1 kb held-out
window split into 20 tiles of 50 bp; one tile at a time replaced by a
dinucleotide-preserving shuffle **of that tile**, everything else byte-identical,
rescored conditioned on the window's own prompt. `delta = baseline − perturbed`,
so positive means the intact tile's **order** carried likelihood.

Gate: a sequence rebuilt through the same splice expression with the tile left
unmodified must score identically. `identity_delta` = **0.0** exactly. All 380
perturbations verified for identical length, identical base composition and
byte-identity outside the tile.

| | value |
| --- | --- |
| tiles scored / skipped | 380 / 0 |
| mean tile delta | **+0.01063**, CI [+0.00903, +0.01224] |
| positive tiles | **345/380 (91%)**, one-sample t=13.02, p=2.8×10⁻³² |
| range | +0.0964 (runx2b zebrafish, 50–100 bp) to −0.0037 |
| zebrafish / flying fish mean | +0.01359 / +0.00735 |

**The decomposition adds up, which is the real check here.** Summing a window's
20 tile deltas and comparing with that window's whole-window real-vs-shuffle
effect from §7 gives a ratio of **1.21 (median 1.23, sd 0.36)**. So the localised
measurements account for the aggregate effect to within about 20%, mildly
superadditively — expected, because scrambling one tile also degrades the context
available for predicting its neighbours, so each delta carries a little of its
neighbours' cost and summing double-counts it. A localisation that summed to a
small fraction of the aggregate, or to several times it, would have meant the
tiling was measuring something else.

**Structure is distributed, not a hotspot.** Per-window maximum deltas run 3–9×
that window's mean, so there is real localisation, but no window has a single
tile carrying its signal. Anyone hoping for one crisp 50 bp element per gene
will not find it here.

**Limits.** Each v1 tile delta rests on a **single** scramble, so it is a
one-sample estimate and the per-tile ranking is noisy; the replicate job
(`aijob-e00vjsseen85f1j3ac`, 5 shuffles per tile) exists to fix exactly that and
its SDs should be read before trusting any individual tile. Several top tiles sit
at window edges (0–50, 950–1000), which may be boundary effects rather than
biology. And a tile Evo 2 relies on is **not** a binding site, **not** an
enhancer, and **not** an edit worth making in a fish.
