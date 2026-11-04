# Replication 30: Tyrosine spatial clustering in zebrafish actinodins (and1, and2)

**Claim, with its numbers removed from my brief:** Tyr spatial clustering is significant in and2
(observed 0.393 vs shuffled 0.211, z = 2.74, p = 0.011) and not in and1 (p = 0.064, where Tyr content
alone explains it). Source: a 2000-shuffle test run by another agent. I did not see their working.

**What kind of result this is:** every number below is a **calculation or simulation** I ran on public
protein sequences. None of it is a laboratory observation.

## My value

Metric: the fraction of consecutive Tyr–Tyr gaps that are **≤ 4 residues** (the Tyr positions are i, j and the gap is j − i).
Null: the full sequence shuffled with its composition kept (`random.shuffle`). One-sided p = (#null ≥ obs + 1)/(N + 1).

| protein | Tyr / length | observed | shuffled mean (sd) | z | p (2000 shuffles, 20 seeds) | p (100,000 shuffles) |
|---|---|---|---|---|---|---|
| and2 (A0ACM8QEN9) | 29 / 508 | 11/28 = **0.3929** | 0.210 (0.069) | **2.54–2.75** | 0.0075–0.0145, median **0.0110** | **0.0107** |
| and1 (E7F5V5) | 47 / 570 | 18/46 = **0.3913** | 0.292 (0.057) | 1.68–1.83 | 0.048–0.076, median **0.060** | **0.0598** |

Uncertainty: the binomial SE of the Monte Carlo p is about ±0.0023 for and2 and ±0.0053 for and1 at N = 2000.
This matches the spread across seeds. At N = 100k it falls to about ±0.0003 and ±0.0008.
The z-score ranges from 2.54 to 2.75 across seeds because the sd of the null shifts slightly from run to run.

Read on its own terms: and2 has the same observed fraction as and1 (0.393 vs 0.391).
The two differ only in their null. and1 has more Tyr (8.2% vs 5.7%), so a shuffled and1 is expected to reach 0.29 by chance anyway.
That supports the claim's wording that "Tyr content alone explains" the and1 value. This is my inference from the table.

## Inputs

| input | source | read-level |
|---|---|---|
| and1 protein, Danio rerio, 570 aa, "Actinodin1 precursor", unreviewed | UniProtKB **E7F5V5** (SV=2), `rest.uniprot.org/uniprotkb/E7F5V5.fasta` | full-text (sequence record) |
| and2 protein, Danio rerio, 508 aa, "Actinodin2 precursor", unreviewed | UniProtKB **A0ACM8QEN9** (SV=1) | full-text (sequence record) |
| and2 alternate entry, 508 aa | UniProtKB **A9JRX1** (zgc:175106). Its sequence is byte-identical to A0ACM8QEN9, so the result is the same | full-text (sequence record) |
| gene lookup | UniProt search `gene_exact:and1/and2 AND organism_id:7955`, which returned only the three entries above | listing |

I used full-length precursors. The and2 signal-peptide region (residues 1–23) contains no Tyr. I did not test a version with the signal peptide removed for and1.

## Arithmetic

Tyr gap lists, taken directly from the sequences:

- and2, 28 gaps: 10, 19, 3, 16, 8, 40, **4, 3**, 37, **1, 1**, 30, 6, **2**, 10, 12, 14, **3**, 60, 17, **3**, 35, **3, 3**, 64, 31, 12, **4**.
  There are 11 gaps of ≤ 4, and 11/28 = 0.392857.
- and1, 46 gaps: 18 of them are ≤ 4, and 18/46 = 0.391304.
- Rough check on the and2 null: with Tyr frequency f = 29/508 = 0.0571, the chance that a geometric gap is ≤ 4 is 1 − (1 − f)^4 = 1 − 0.9429^4 = 0.2096. The simulated mean is 0.210.
- For and1: f = 0.0825, and 1 − 0.9175^4 = 0.291, against a simulated 0.292.
- and2 z = (0.3929 − 0.2099)/0.0694 = 2.64. and1 z = (0.3913 − 0.2918)/0.0570 = 1.75.

## Important caveat: how the metric was chosen

The brief gave no definition of "spatial clustering". I picked a metric **post hoc**, by scanning candidates to see which reproduced the brief's and2 numbers:

- 0.211 ≈ 1 − (1 − f)^4 for and2's Tyr frequency.
- 0.393 = 11/28, and and2 has 29 Tyr, so 28 gaps.

I scanned these candidates (2000 shuffles each):

- Per-Tyr "has a neighbour within ±w" for w = 1, 2, 3. For and2 this gave obs 0.103, 0.172 and 0.552, none of which match.
- Consecutive gaps ≤ d for d = 1…8. Only **d = 4** gives 0.393 vs about 0.21.

So the **and2 match follows from how I chose the metric and is not independent evidence**. Only these are genuine checks:

1. the and2 z and p, given the metric;
2. **all** of the and1 numbers, which I did not fit to.

Both reproduce. The sensitivity scan also shows the and2 result **depends on the threshold**:

| d | and2 p |
|---|---|
| 3 | 0.023 |
| 4 | 0.0065 (seed 7) |
| 5 | 0.044 |
| 6 | 0.060 |
| 7 | 0.155 |

With the threshold left free, a correction over the eight thresholds would weaken the and2 result.
That correction is my inference. I did not compute a corrected p.

## Comparison with the recorded value (done only after the derivation above)

The recorded numbers are 0.393 observed vs 0.211 shuffled, z = 2.74, p = 0.011 for and2, and p = 0.064 for and1. My numbers are:

| quantity | recorded | mine | match? |
|---|---|---|---|
| and2 observed | 0.393 | 0.3929 | exact (but used to choose the metric) |
| and2 shuffled mean | 0.211 | 0.208–0.213 across seeds | within Monte Carlo spread |
| and2 z | 2.74 | 2.54–2.75 across seeds | inside my seed range |
| and2 p | 0.011 | median 0.0110; 0.0107 at 100k | yes |
| and1 p | 0.064 | 0.048–0.076 across seeds; 0.0598 at 100k | yes, within Monte Carlo noise |

After my derivation was finished, I found a different branch, `claude/tyrosine-clustering-replication-tx87zl`, with its own replicate-30.md.
I read **only its final verdict block**. It reports the same metric, also reverse-engineered, and the same conclusion.
Because both of us inferred the metric from the same and2 numbers, the two derivations are not fully independent of each other.

**Verdict: AGREE.** All the stated numbers reproduce from UniProt E7F5V5 and A0ACM8QEN9, using a metric I inferred.
The claim's own framing ("significant in and2") should state that the result holds for d = 3–5 and does not survive at d ≥ 6.

Script: `docs/research/fish/replicate-30-tyr.py`.

```swarm-replication
{"claim_id": 30, "my_value": "and2: 0.393 observed vs 0.210 shuffled (z 2.64, range 2.54-2.75; p 0.011 +/- 0.002); and1: 0.391 vs 0.292 (z 1.75; p 0.060 +/- 0.005)", "agrees": true,
  "note": "Reproduced from UniProt E7F5V5/A0ACM8QEN9 as the fraction of consecutive Tyr gaps <=4 aa vs composition-preserving shuffles; the metric was inferred post hoc from the and2 numbers, so only and2 z/p and all and1 numbers are independent checks, and and2 significance is threshold-sensitive (p>0.05 for d>=6)."}
```
