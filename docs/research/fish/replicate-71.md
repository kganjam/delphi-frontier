# Replicate 71: and2 max self-identity against a composition-preserving shuffle null

**Claim under replication** (answer withheld from me): "and2 max self-identity 0.098 sits at ~89th
percentile of composition-preserving shuffles (p=0.106), not below null; and1/and2 carry a
conserved C-x(6,7)-C repea[t] …". The claim text I was given was cut off at "repea".

**My value (calculated, not observed):** and2 max self-identity = **0.0984** (44/447 identities at
offset k = 61). Against 10,000 whole-sequence shuffles it sits at the **88.8th percentile**,
empirical one-sided **p = 0.112 ± 0.003** (binomial SE). Across four smaller runs the p-value spans
**0.080–0.126**, so a 200-shuffle estimate carries roughly ±0.02 of Monte-Carlo noise. That puts
the value **not below the null and not significant**. In addition: and1 has 8 C-x(6,7)-C matches
and and2 has 10. No shuffle out of 5,000 reached either count (p < 2×10⁻⁴).

Everything here is **calculated** from public sequences. Nothing is a wet-lab observation.

## Procedure, and what I did and did not read first

1. To find the metric's definition, I read only §3 of the *original* claim
   (`docs/research/fish/proteins-disorder.md` on branch `swarm-architecture`). Read-level:
   full-text for that section. It defines the statistic as "maximum self-identity at any offset
   1–80, against 200 composition-preserving shuffles". That document names no accessions, and the
   sequences are not in the repo (searched with `git ls-tree` on that branch for
   and1/and2/actinodin/fasta).
2. I opened `challenge-29.md` on `claude/tandem-repeat-challenge-k6d4ao` and saw its first 12
   lines: the title, the quoted original claim, and the verdict word "REFUTED" with a statement
   that 0.098 reproduces. **I stopped reading there**, as instructed. I did not open its scripts.
   I read the rest only after my numbers below were final.
3. I fetched the sequences myself and wrote my own code. The scripts are in
   `replicate-71-scripts/`.

## Inputs

| input | value | source | read-level |
|---|---|---|---|
| and1 protein | E7F5V5 (SV=2), 570 aa, "Actinodin1 precursor", *Danio rerio* | rest.uniprot.org FASTA, fetched 2026-11-04 | full record (FASTA) |
| and2 protein | A0ACM8QEN9, 508 aa, "Actinodin2 precursor" | rest.uniprot.org FASTA, fetched 2026-11-04 | full record (FASTA) |
| and2 protein (alt.) | A9JRX1, 508 aa (zgc:175106) | rest.uniprot.org | full record. Checked: identical in sequence to A0ACM8QEN9 |
| metric definition | max over k = 1..80 of #{i : s[i] = s[i+k]} / (L−k); null = whole-sequence permutation | `proteins-disorder.md` §3, branch `swarm-architecture` | full-text (§3 only) |

The accessions came from a UniProt search for `gene_exact:and1` / `gene_exact:and2` with
`organism_id:7955`. The original author named no accession. That I am using the same sequences is
therefore an **inference**, supported by two facts: the lengths match, and my observed values
reproduce the author's table (and1 0.116, and2 0.098).

## Arithmetic

**Observed (and2, L = 508).** The best offset is k = 61. Identities: 44 of 508 − 61 = 447 pairs.
44 / 447 = **0.0984**.
Composition baseline Σf² = 0.0650.

**Null (and2), 10,000 permutations (numpy, seed 7).**

| quantity | value |
|---|---|
| mean of shuffled max | 0.0916 |
| SD | 0.0056 |
| 95th percentile | 0.1018 |
| fraction of shuffles < 0.0984 | **0.8878** |
| p = fraction ≥ 0.0984 | 1122 / 10,000 = **0.112** |
| SE of p | √(0.112 × 0.888 / 10,000) = 0.0032 |
| z | (0.0984 − 0.0916) / 0.0056 = **+1.2** |

**Smaller runs (Python `random`, seeds 1–4)** show the Monte-Carlo spread:

| run | n | p = frac ≥ obs | percentile | mean | max |
|---|---|---|---|---|---|
| seed 1 | 200 | 0.100 | 90.0 | 0.0914 | 0.1104 |
| seed 2 | 200 | 0.080 | 92.0 | 0.0910 | 0.1076 |
| seed 3 | 200 | 0.115 | 88.5 | 0.0915 | 0.1130 |
| seed 4 | 2,000 | 0.126 | 87.5 | 0.0917 | 0.1258 |

The observed value lies below the *maximum* of every run. That is why a "shuffled max" column
can make it look "below the null". It lies **above the mean** in every run, at about the
88th–92nd percentile.

**C-x(6,7)-C counts.** Overlapping starts were counted with the regex `(?=C.{6,7}C)`. The null
was 5,000 whole-sequence shuffles (seed 71).

| | Cys count | observed | shuffle mean | shuffle max | n ≥ obs | p |
|---|---|---|---|---|---|---|
| and1 | 16 | 8 | 0.83 | 5 | 0 | < 2×10⁻⁴ |
| and2 | 20 | 10 | 1.45 | 6 | 0 | < 2×10⁻⁴ |

Match start positions:
- and1: 121, 152, 228, 261, 288, 313, 406, 458.
- and2: 114, 148, 217, 250, 277, 308, 347, 391, 418, 453.

Several hits share the core C-[DN]-P-x-x-D-P-x-C (e.g. `CDPYRDPYC`, `CDPRYDPYC`).

The claim also asserts that the motif is "conserved". I did **not** independently test whether the
motif is conserved across the paralogs or in its flanks. Conservation therefore remains
**unverified by me**. The visible correspondence of the hit lists (8 vs 10, similar order and
spacing) is my inference only.

**Side finding, outside the claim.** and1's maximum self-identity is 0.1157, at offset k = 8
(65/562). Against 10,000 shuffles, p = 0.0009 ± 0.0003 (z ≈ +4.4). So and1 is *above* chance under
this metric, not "at the null". I did not test kcnk5b.

## Comparison with the recorded value (read after the derivation)

`challenge-29.md` records: and2 0.098 at k = 61, null mean 0.0915, SD 0.0055, p = 0.106 from
2,000 shuffles, "~89th percentile". It also records C-x(6,7)-C counts of 8 (and1) and 10 (and2),
with shuffle means 0.82 and 1.45, maxima 5 and 6, and p < 0.0002.

Where the numbers line up:

- **and2 self-identity.** My p = 0.112 ± 0.003 (10,000 shuffles) is within about 2 SE of their
  0.106 (2,000 shuffles, SE ≈ 0.007). My percentile of 88.8 matches "~89th".
- **Same offset and mean.** The offset (61) and the null mean match.
- **Motif counts.** These match exactly. My shuffle means and maxima are 0.83/5 and 1.45/6
  against their 0.82/5 and 1.45/6.
- **and1 side finding.** It agrees in direction with their p = 0.0015. My 10,000-shuffle estimate
  is smaller, 0.0009.

**Verdict: AGREE** on the numeric parts. One caveat: I did not test their flank-conservation claim,
so "conserved" is not independently replicated here.

```swarm-replication
{"claim_id": 71, "my_value": "and2 max self-identity 0.0984 (44/447 at k=61) = 88.8th percentile of 10,000 composition-preserving shuffles, p=0.112±0.003 (dimensionless fraction); C-x(6,7)-C counts 8 (and1) / 10 (and2), 0/5000 shuffles reach either", "agrees": true, "note": "Independent recomputation from UniProt E7F5V5/A0ACM8QEN9 reproduces 0.098, the ~89th percentile (p within 2 SE of 0.106) and the 8/10 motif counts; motif conservation across flanks was not independently tested."}
```
