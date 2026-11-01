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

## 2. The finding that tracks training-corpus membership

Generated candidates were compared with the real windows, paired by window:

| species | corpus status | real − candidate (paired) | p |
| --- | --- | --- | --- |
| zebrafish | GRCz11 **in** OpenGenome2 | **+0.1374** CI [0.0521, 0.2226] | 0.0054 |
| flying fish | `GCA_018398805.1` almost certainly **out** | **+0.0107** CI [−0.0727, +0.0940] | 0.78 |

The gap between real and generated sequence appears **only** where the model has
likely seen the real sequence. This is a *within-species* paired comparison, so
unlike the cross-species contrast in §4 it is **not** subject to the leakage,
window-definition or GC confounds — they cancel.

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
