# Replication 29: "no tandem repeats in any of the three proteins" (200-shuffle null)

Independent re-derivation. First I identified the three proteins from commit messages and from the
input tables of replicates 14 and 15. I did **not** read any text about tandem repeats or shuffles
before I had my own numbers. After that I located the recorded claim in
`origin/claude/elastic-similarity-law-dqxwsj:docs/research/fish/proteins-disorder.md` §3 and
compared against it.

**Every number below is a calculation (a permutation test I ran on downloaded sequences), not an
experimental observation.**

## Inputs

| Input | Source | Read-level |
|---|---|---|
| kcnk5b, *Danio rerio*, 448 aa | UniProt Q6PFU3, `rest.uniprot.org/uniprotkb/Q6PFU3.fasta`, fetched 2026-11-04 | full-text (full sequence) |
| Actinodin1 (and1), 570 aa | UniProt E7F5V5 (SV=2), same route | full-text (full sequence) |
| Actinodin2 (and2), 508 aa | UniProt A0ACM8QEN9 (SV=1), same route. A9JRX1 (also GN=and2, 508 aa) was also fetched and is residue-for-residue identical (0 mismatches), so the choice between them does not matter | full-text (full sequence) |
| Which three proteins | Commit ba1dd261 message ("a K2P fold for kcnk5b, a real negative for the actinodins") and the input tables of `replicate-14.md` and `replicate-15.md` | listing (I read only the input rows) |
| BLOSUM62 | Biopython `substitution_matrices.load('BLOSUM62')` | full-text |

## Method (mine, chosen before seeing the recorded one)

A tandem repeat of period *p* means a stretch where residue *i* resembles residue *i+p* across at
least one full unit, i.e. two adjacent copies.

- **Statistic A (local, BLOSUM62).** For every period p = 1 … L/2, take the diagonal score
  d_i = BLOSUM62(s_i, s_{i+p}). Find the best-scoring contiguous segment of d whose length is at
  least p, using prefix sums: max_j [P_j − min_{i ≤ j−p} P_i]. The statistic is the maximum over
  all p.
- **Statistic B (exact).** The longest run of consecutive positions with s_i = s_{i+p}, maximised
  over p.
- **Null.** 200 uniform permutations of each sequence. This keeps the composition exactly.
  Seed 20261104. Empirical p = (1 + #{null ≥ obs}) / 201. With 200 shuffles the smallest
  achievable p is 0.005.
- **Robustness.** Five more seeds (0–4) at 200 shuffles each, plus one run of 2,000 shuffles.
- **Scripts.** `replicate-29/tr.py`, `replicate-29/rob.py` and `replicate-29/glob.py`. Run them
  from a directory that contains `seq/<ACC>.fa`.

## Results (calculated)

### Statistic A: local BLOSUM62 tandem score

| protein | obs score | best period | segment (1-based) | null mean ± sd | null max | p (200, seed 20261104) | p across seeds 0–4 | p (2,000) |
|---|---|---|---|---|---|---|---|---|
| kcnk5b | 35 | 1 | 313–324 `DEKRRKKKQEEE` | 23.4 ± 4.6 | 44 | 0.035 | 0.010–0.030 | 0.027 |
| and1 | 50 | 10 | 170–197 (`PYLAPAPVK` / `PAPAPAPVK`, 11/18 identical) | 30.8 ± 5.3 | 47 | 0.005 | 0.005–0.015 | 0.005 |
| and2 | 43 | 39 | 276–355 (41-aa unit vs next, 11/41 identical, Cys/`CN`/`DP` positions conserved) | 28.0 ± 4.9 | 45 | 0.010 | 0.005–0.025 | 0.008 |

Bonferroni correction for 3 proteins, using the 2,000-shuffle p: kcnk5b 0.08, and1 0.015,
and2 0.024.

### Statistic B: exact identity runs

| protein | longest run (period) | null mean | null max | p (200) |
|---|---|---|---|---|
| kcnk5b | 5 (78) | 3.6 | 6 | 0.055 |
| and1 | 6 (10) | 4.0 | 6 | 0.010 |
| and2 | 5 (199) | 3.9 | 7 | 0.12 |

### My value

Under a local tandem-repeat test with a 200-shuffle composition-preserving null, the result is
**not** "none in any of the three":

- **and1** carries a short Pro/Ala-rich period-10 tandem repeat at residues 170–197. It exceeds the
  null (p ≈ 0.005, at the resolution floor of the test) and survives correction.
- **and2** carries a weak, imperfect ~39–41-residue duplication at 276–355. The identity is only
  27%, but the cysteine framework is conserved. p ≈ 0.008–0.025 depending on seed.
- **kcnk5b** carries a period-1 charged low-complexity stretch (`DEKRRKKKQEEE`). It is nominally
  significant (p ≈ 0.03) but not after correction.

**Interpretation (my inference):** none of these is a long, regular repeat array of the kind seen
in collagen or silk. All are short or highly degenerate. The shuffle null is also known to be
anti-conservative for low-complexity, compositionally biased segments, because a global shuffle
destroys local composition bias. So "no extensive tandem-repeat architecture" is defensible. "No
detectable tandem repeats in any of the three, at the null" is not, for and1 or for the local test.

**Uncertainty.** The p-values carry Monte-Carlo noise of roughly ±0.01 at 200 shuffles (see the
seed spread). The conclusion depends on the detector: statistic B finds nothing for and2 (p = 0.12).

**Scope of the negative searches.** Three UniProt entries only (the and2 duplicate is identical). No
other isoforms or Ensembl translations. Ungapped detectors only, so gapped or indel-containing
repeats would be missed. No external tools (T-REKS, XSTREAM, HHrepID, RADAR) were run.

## Comparison with the recorded value (read only after the above)

The recorded claim is in `proteins-disorder.md` §3 on `origin/claude/elastic-similarity-law-dqxwsj`
(read-level: full-text of §3 and §5). It uses a **different statistic**: the maximum
*whole-sequence* fractional identity at offsets 1–80, compared against 200 shuffles. The author
reports:

| | max obs | Σf² | shuffled mean-max | shuffled max | author's verdict |
|---|---|---|---|---|---|
| kcnk5b | 0.110 | 0.060 | 0.088 | 0.109 | at the null |
| and1 | 0.116 | 0.067 | 0.093 | 0.114 | at the null |
| and2 | 0.098 | 0.065 | 0.091 | 0.111 | below the null |

I re-implemented that statistic (`replicate-29/glob.py`, a calculation) and reproduced the observed
values and Σf² exactly (0.110/0.060, 0.116/0.067, 0.098/0.065). My null means also match: 0.088,
0.092–0.093 and 0.092. The inputs and arithmetic therefore agree.

**The verdict does not follow from the author's own table.** For kcnk5b (0.110 > 0.109) and and1
(0.116 > 0.114), the observed value is **above every one of the 200 shuffles**, which gives
p = 1/201 ≈ 0.005. With my seeds 1–3 I get kcnk5b p = 0.005, 0.010, 0.015 and and1 p = 0.005 in all
three runs. That is the upper tail, not "at the null". For and2, "below the null" is also a
misstatement: 0.098 is above the null mean of 0.091, with p ≈ 0.10–0.14, which is not significant
but is not below it. The peak offsets are p = 3 for kcnk5b, p = 8 for and1 and p = 61 for and2.

This is my inference, not the author's claim: a global offset-identity score dilutes short local
repeats, so it is the less sensitive test. Even so, it flags kcnk5b and and1. The author's separate
statement that no 7-mer recurs 3 times was not checked here.

**Verdict: DISAGREE.** The numbers reproduce. The "no tandem repeats in any of the three / at the
null" reading does not, either under the author's statistic (kcnk5b and and1 beat all 200
shuffles) or under my local test (and1 and and2 significant after correction). What is supported
is the weaker claim "no extensive or regular tandem-repeat architecture".

```swarm-replication
{"claim_id": 29, "my_value": "Not null for all three: local BLOSUM62 tandem test vs 200 composition-preserving shuffles gives and1 p≈0.005 (period-10 PAPAPAPVK repeat, res 170-197), and2 p≈0.008-0.025 (degenerate ~40-aa duplication, res 276-355), kcnk5b p≈0.03 (period-1 charged stretch, n.s. after Bonferroni); the recorded global statistic reproduces exactly but kcnk5b (0.110) and and1 (0.116) exceed all 200 shuffles (p≈0.005)", "agrees": false, "note": "Inputs and numbers reproduce, but the recorded table itself puts kcnk5b and and1 above the shuffled maximum, so 'at the null' is wrong; only 'no extensive repeat architecture' is supported (calculation, not observation)."}
```
