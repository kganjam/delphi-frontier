# Replicate 29: tandem repeats in and1, and2 and kcnk5b vs a shuffle null

**Question (answer withheld from me):** "No tandem repeats in any of the three proteins against a
null of 200 composition-preserving shuffles."
**Status:** independent re-derivation. **Every number below is computed or simulated**, not observed.
Nothing here is a wet-lab or database observation, apart from the sequences themselves.

## Bottom line

**My value:** the claim **does not survive** a local tandem-repeat test.

- **and1 (E7F5V5):** a short tandem repeat departs from the shuffle null. It has period 10 at
  residues ~172–191 (`LAPAPVKSPA|PAPAPVKAPA`, 8/10 identical) and contains a `PAPAPAP` run.
  Empirical p is 0.005–0.010 under BLOSUM62 scoring and 0.005 under identity scoring. 0.005 is the
  smallest p 200 shuffles can give, so this is the resolution floor. The signal holds across 4 seeds
  and 2 scoring schemes, and it survives a ×3 Bonferroni correction across the three proteins.
- **and2 (A0ACM8QEN9):** the result depends on the scoring scheme. With BLOSUM62, a period-39
  segment gives p = 0.01–0.02. With identity scoring, p = 0.15–0.41. I do not call this a repeat.
- **kcnk5b (Q6PFU3):** no tandem repeat with period ≥ 5 (p = 0.26–1.0). A gapped *internal*
  (non-adjacent) repeat gives p = 0.005 under BLOSUM62. My inference, which I did not test: this is
  the two-pore-domain duplication expected of a K2P channel. It is not a tandem array.

**Uncertainty:** empirical p-values from 200 shuffles have a floor of 1/201 ≈ 0.005, and they move by
about ±0.01 between seeds (see the seed table). Whether and1's two-copy, 10-residue repeat counts as
a "tandem repeat" depends on the definition. Tools such as TRF/XSTREAM-style detectors often
require ≥ 3 copies, and this repeat has about 2 copies plus a period-2 PA run. That is a definitional
caveat. It is not a statistical one.

## Inputs

| input | value | source | read-level |
|---|---|---|---|
| and1 sequence | E7F5V5_DANRE "Actinodin1 precursor", 570 aa, SV=2 | UniProt REST `rest.uniprot.org/uniprotkb/E7F5V5.fasta`, fetched 2026-11-04 | full-text |
| and2 sequence | A0ACM8QEN9_DANRE "Actinodin2 precursor", 508 aa, SV=1 | UniProt REST, same date | full-text |
| kcnk5b sequence | Q6PFU3_DANRE, 448 aa, SV=1 | UniProt REST, same date | full-text |
| repo copies | `results/fish-proteins/{A0ACM8QEN9,E7F5V5,Q6PFU3}.fasta` on `origin/swarm-architecture` | git | full-text; **byte-identical** to the UniProt fetch (checked with diff) |
| BLOSUM62 | standard NCBI matrix, embedded in the script | — | full-text |

I found the protein identities from the repo's FASTA file names and headers. I did not read any
results file before computing. I opened the recorded claim only in the comparison section below.

## Method (mine, designed before seeing theirs)

Script: `docs/research/fish/replicate-29_shuffle_null.py` (run with `python3 -I … <fasta dir>`, ~9 s).

1. **T_all / T_ge5 (tandem, ungapped):** for each period L (1..100, or 5..100), score the self-diagonal
   `B62[s[i], s[i+L]]` and take the best local segment *of length ≥ L*. That length rule makes the
   two copies abut or overlap, which is what makes the repeat tandem. The statistic is the maximum over L.
2. **G_ge5 (internal, gapped):** a Smith–Waterman self-alignment with BLOSUM62 and linear gap 8,
   restricted to cells with j − i ≥ 5.
3. **Null:** 200 uniform random permutations of each sequence, which preserve composition exactly.
   numpy `default_rng(29)`.
4. p = (1 + #{null ≥ obs}) / 201.
5. Sensitivity (`replicate-29_sensitivity.py`): seeds 1, 2 and 3, plus identity scoring (+1/−1, gap 2)
   with seeds 29 and 1.

## Arithmetic (seed 29, BLOSUM62)

| protein | stat | obs | null mean ± sd | null max | z = (obs−mean)/sd | p_emp |
|---|---|---|---|---|---|---|
| and2 | T_all | 43 (L=39) | 28.14 ± 5.48 | 53 | (43−28.14)/5.48 = 2.71 | 0.0199 |
| and2 | T_ge5 | 43 (L=39) | 26.82 ± 5.37 | 53 | 3.01 | 0.0100 |
| and2 | G_ge5 | 79 | 40.05 ± 5.35 | 59 | 7.28 | 0.0050 |
| and1 | T_all | 50 (L=10) | 30.45 ± 5.56 | 54 | 3.52 | 0.0100 |
| and1 | T_ge5 | 50 (L=10) | 29.45 ± 5.46 | 54 | 3.77 | 0.0100 |
| and1 | G_ge5 | 58 | 45.87 ± 6.07 | 63 | 2.00 | 0.0647 |
| kcnk5b | T_all | 35 (L=1, `KKK`/`EEE` runs) | 23.25 ± 4.78 | 42 | 2.46 | 0.0398 |
| kcnk5b | T_ge5 | 24 (L=7) | 22.43 ± 5.13 | 42 | 0.30 | 0.3433 |
| kcnk5b | G_ge5 | 63 | 33.23 ± 4.35 | 48 | 6.84 | 0.0050 |

p_emp = 0.0100 means that 1 of 200 shuffles reached the observed value: (1+1)/201. "null max ≥ obs"
with p = 0.01 is consistent with that. The p-value is the reported quantity. z assumes a normal
null, which the data do not guarantee. I give z for reference only.

Seed and scoring sensitivity (p_emp for T_all / T_ge5 / G_ge5):

| run | and2 | and1 | kcnk5b |
|---|---|---|---|
| B62 seed 1 | .025 / .020 / .005 | .005 / .005 / .050 | .030 / .264 / .005 |
| B62 seed 2 | .010 / .010 / .005 | .010 / .005 / .030 | .020 / .363 / .005 |
| B62 seed 3 | .020 / .015 / .005 | .005 / .005 / .055 | .015 / .398 / .005 |
| identity seed 29 | .388 / .204 / .174 | **.005 / .005 / .005** | .224 / 1.00 / .060 |
| identity seed 1 | .408 / .149 / .144 | **.005 / .005 / .005** | .269 / 1.00 / .110 |

Bonferroni for 3 proteins: α = 0.05/3 = 0.0167. and1 T_ge5 has p ≤ 0.01 in every run and passes.
and2 passes only under BLOSUM62. kcnk5b T_ge5 never passes.

## Comparison with the recorded value (read only after the above)

Recorded claim: `origin/swarm-architecture:docs/research/fish/proteins-disorder.md`, §3 (commit
699500a7). Read-level: full-text. **Author's claim:** "There are no detectable tandem repeats — in
any of the three". The test behind it was the maximum whole-sequence self-identity at offsets 1–80
against 200 shuffles. The recorded values were kcnk5b 0.110 (shuffled max 0.109), and1 0.116
(shuffled max 0.114) and and2 0.098 (shuffled max 0.111). All three were labelled "at/below the
null". The claim also says no 7-mer recurs 3 times.

I then implemented *their* statistic myself (`replicate-29_global_offset_identity.py`):

| protein | obs (mine) | obs (recorded) | my null max, 200 shuf (seed 29) | p, 200 shuf | p, 2000 shuf (seed 7) |
|---|---|---|---|---|---|
| kcnk5b | 0.1101 | 0.110 | 0.111 | 0.010 | **0.0020** |
| and1 | 0.1157 | 0.116 | 0.107 | 0.005 | **0.0020** |
| and2 | 0.0984 | 0.098 | 0.122 | 0.134 | 0.119 |

My observed values and Σf² (0.060 / 0.067 / 0.065) match the recorded ones exactly. My largest
7-mer count is 1 in every sequence, which agrees with "no 7-mer recurs 3 times".

**Where we disagree:**

- **My inference from their own table:** the recorded table puts the and1 observed value (0.116)
  *above* the maximum of all 200 shuffles (0.114). It also puts kcnk5b (0.110) above its maximum
  (0.109). That means p ≤ 1/201 for both, so the "at the null" verdict contradicts the numbers next
  to it. With 2,000 shuffles, both give p ≈ 0.002.
- **My local tandem test** also rejects the null for and1, and that result does not depend on the
  scoring scheme.

The claim is supported for and2. It is also supported for kcnk5b *if* "tandem" means adjacent
copies with period ≥ 5. Even then, the global offset-identity excess in kcnk5b is an internal-
similarity signal. I infer, without testing, that it reflects the two P-domains.

**Verdict: DISAGREE.** "No tandem repeats in any of the three" does not hold. and1 departs from a
composition-preserving shuffle null under both my local tandem statistic and the recorded global
statistic. The recorded table's own numbers already show this. The narrower statement "no periodic
multi-copy repeat array" is consistent with my results: there is no 7-mer recurrence, and and1's
repeat is about 2 copies.

**Scope of negative searches:** only these 3 UniProt entries. Periods 1–100. Ungapped tandem plus
gapped internal self-alignment with BLOSUM62 and identity scoring. I did not run TRF, XSTREAM,
RADAR, HHrepID or T-REKS, and I did not consider isoforms.

```swarm-replication
{"claim_id": 29, "my_value": "and1 (E7F5V5) tandem repeat vs 200 composition-preserving shuffles: empirical p = 0.005-0.01 (simulated; period-10, ~res 172-191); and2 p = 0.01-0.41 (scoring-dependent); kcnk5b period>=5 p = 0.26-1.0", "agrees": false,
  "note": "and1 departs from the shuffle null under my local tandem test and under the recorded global statistic, whose own table shows and1 0.116 and kcnk5b 0.110 above their 200-shuffle maxima (p<=0.005), so 'none in any of the three' does not hold."}
```
