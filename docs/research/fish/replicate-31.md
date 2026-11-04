# Replicate 31: cysteine close pairs in and1 / and2 / kcnk5b (independent re-derivation)

**Claim under test (answer withheld from me):** "Cysteine close pairs are ZERO in all three and
significantly fewer than chance in and2 (z=-2.02), with no CxxC motifs." Context: a 2000-shuffle
test, with Lys clustering in kcnk5b at p=0.005 as the positive control.

**What I did not read.** I did not open any prior working for this claim. I listed file *names* on
remote branches to find where the fish work lives. I deliberately did **not** open
`challenge-14.md`, `replicate-14.md`, `challenge-18.md` or any other doc that mentions `and2`. I
grepped `S13-protein.md` only for accession/gene-symbol tokens. That turned up the token `and1` and
the accession E7F5V5, and nothing about cysteines. Every number below is my own **calculation**
(simulation or exact combinatorics) on primary sequences. None of them is an observation.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| "All three" proteins | and1, and2, kcnk5b (zebrafish, *Danio rerio*, taxon 7955) | **My inference.** The claim names and2 and kcnk5b. I assumed and1 is the third because it is the actinodin paralog. If the original used a different third protein (e.g. kcnh2a), my and1 row does not apply. | n/a (inference) |
| and1 sequence | E7F5V5, 570 aa, 16 Cys, 26 Lys | UniProt REST `rest.uniprot.org/uniprotkb/E7F5V5.fasta` | full-text (sequence record) |
| and2 sequence | A9JRX1, 508 aa, 20 Cys, 28 Lys. A0ACM8QEN9 is byte-identical (checked with `cmp`). | UniProt REST | full-text |
| kcnk5b sequence | Q6PFU3, 448 aa, 9 Cys, 31 Lys. A0A8M1PBI1 is byte-identical. | UniProt REST | full-text |
| Shuffles | 2000 per test, full-sequence permutation (composition preserved), seed 1. Plus 10 extra seeds for and2. | from the claim's context | n/a |

Cys positions (0-based):
- and1: 120, 128, 151, 159, 227, 234, 260, 268, 287, 295, 312, 320, 405, 413, 457, 465
- and2: 113, 121, 147, 155, 216, 223, 249, 257, 276, 284, 307, 315, 346, 354, 390, 398, 417, 424, 452, 460
- kcnk5b: 50, 114, 120, 125, 161, 330, 358, 374, 402

In both actinodins the Cys come in pairs spaced 7–8 apart (a C-x6/7-C pattern). The closest Cys pair
in either actinodin is 7 residues apart. In kcnk5b the closest pair is 120/125, 5 apart.

## Definition

A "close pair" is a pair of Cys at positions i<j with j−i ≤ d. The claim's "CxxC" points to
d = 3, which counts CC, CxC and CxxC. I report d = 2…6 because the original's d is unknown.

I calibrated d with the positive control, using the same definition for Lys in kcnk5b. Observed
Lys pairs at d ≤ 3 = 14, against a null mean of 6.31 (sd 2.38). That gives z = +3.23 and a one-sided
p_high of (1+9)/2001 = **0.0050**, which exactly matches the stated positive control. At d ≤ 4 the
result is p = 0.0010 (z = +4.22), which does not match. **Inference:** the original most likely used
d ≤ 3.

## Results (simulated, 2000 shuffles, seed 1)

The z-score is z = (obs − mean_null)/sd_null. The one-sided p is p_low = (1 + #{null ≤ obs})/(N+1).

| Protein | d | obs Cys pairs | null mean | null sd | z | p_low |
|---|---|---|---|---|---|---|
| and1 | ≤3 | 0 | 1.306 | 1.110 | −1.18 | 0.256 |
| and2 | ≤3 | 0 | 2.260 | 1.383 | **−1.63** | **0.084** |
| kcnk5b | ≤3 | 0 | 0.475 | 0.683 | −0.70 | 0.613 |
| and1 | ≤4 | 0 | 1.740 | 1.284 | −1.36 | 0.158 |
| and2 | ≤4 | 0 | 2.991 | 1.597 | −1.87 | 0.037 |
| kcnk5b | ≤4 | 0 | 0.627 | 0.782 | −0.80 | 0.516 |
| and1 | ≤5 | 0 | 2.17 | — | −1.50 | 0.098 |
| and2 | ≤5 | 0 | 3.72 | — | −2.08 | 0.0135 |
| kcnk5b | ≤5 | **1** (C120–C125) | 0.78 | — | +0.26 | 0.840 |

- A regex search for `C..C` (overlapping) finds **0 CxxC motifs** in all three proteins. There are
  also 0 CC dipeptides.
- **Exact null mean, as an arithmetic check (calculated).** For a uniform permutation,
  E = Σ_{δ=1..d}(L−δ) · k(k−1)/(L(L−1)). For and2 (L = 508, k = 20), d = 3:
  (507 + 506 + 505) · 380 / (508 · 507) = 1518 · 380 / 257556 = **2.240**. This agrees with the
  simulated mean of 2.260.
- **Seed sensitivity for and2 z (10 seeds × 2000 shuffles):**
  - d ≤ 3: mean −1.575 (range −1.634 to −1.535)
  - d ≤ 4: mean −1.807 (−1.873 to −1.757)
  - d ≤ 5: mean −2.034 (−2.078 to −1.981)
  - d ≤ 6: mean −2.231 (−2.285 to −2.160)

## My value

At d ≤ 3, the window that reproduces the positive control:
- Cys close pairs are **0 / 0 / 0** in and1 / and2 / kcnk5b.
- There are **0 CxxC** motifs in any of them.
- For and2, **z = −1.6 ± 0.05** (seed spread), one-sided **p ≈ 0.08**. This is *not* significant at
  α = 0.05.

Because the observed count is 0, a Poisson approximation also bounds the result. The best possible
one-sided p is roughly e^(−2.24) ≈ 0.11 (calculated). So with this composition a z-score cannot turn
a zero count into strong evidence of depletion.

## Comparison with the recorded value

The only recorded value I compared against is the claim text quoted in the task. I did not look up
the original working.

- **"Zero in all three": AGREE**, at d ≤ 3 and d ≤ 4 (with and1 assumed as the third protein).
- **"No CxxC motifs": AGREE.**
- **"Significantly fewer than chance in and2 (z = −2.02)": DISAGREE.**
  - At the window that reproduces the Lys positive control (d ≤ 3), I get z ≈ −1.6, p ≈ 0.08.
  - z ≈ −2.0 reproduces only at d ≤ 5 (z = −2.03 averaged over seeds).
  - At d ≤ 5, kcnk5b has one close pair (C120–C125), so the claim's own "zero in all three" would
    then be false.
  - So no single window I tested gives both "zero in all three" and z ≈ −2.02 for and2. I cannot
    rule out that the original used a different and2 sequence or a different shuffle scheme (e.g.
    windowed or dipeptide-preserving). I did not test either.

```swarm-replication
{"claim_id": 31, "my_value": "Cys close pairs (|i-j|<=3) = 0/0/0 in and1/and2/kcnk5b, 0 CxxC; and2 z = -1.6 +/- 0.05 (p_one-sided ~0.08, 2000 shuffles), not significant", "agrees": false,
  "note": "Zero counts and absent CxxC reproduce, but the window that reproduces the kcnk5b Lys p=0.005 control (<=3) gives and2 z~-1.6, and z~-2.02 only appears at <=5, where kcnk5b has a C120-C125 pair, so the significance claim does not hold together."}
```
