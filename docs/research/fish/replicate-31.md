# Replication 31: cysteine close pairs in kcnk5b, and1 and and2

**Claim under test (answer removed):** "Cysteine close pairs are ZERO in all three and significantly fewer than chance in and2 (z = ?), with no CxxC motifs." The test is a 2000-shuffle test. Its positive control is Lys clustering in kcnk5b at p = 0.005.

**What I did not read.** I did not read the earlier derivation. I searched the other branches by **file name only**. That search found `results/fish-proteins/{Q6PFU3,E7F5V5,A0ACM8QEN9}.fasta` on `origin/claude/elastic-similarity-law-dqxwsj`, and that is how I identified the "three" proteins. I opened only those FASTA files, and only to compare checksums with my own download. I read no markdown, JSON or code that might hold the earlier result. Every number below is **computed by me**: it is a calculation or a simulation, not an observation.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| kcnk5b protein | Q6PFU3, 448 aa, 9 Cys, 31 Lys | `rest.uniprot.org/uniprotkb/Q6PFU3.fasta` (fetched 2026-11-04) | full-text (raw sequence) |
| and1 protein | E7F5V5, 570 aa, 16 Cys, 26 Lys ("Actinodin1 precursor") | `rest.uniprot.org/uniprotkb/E7F5V5.fasta` | full-text |
| and2 protein | A0ACM8QEN9, 508 aa, 20 Cys, 28 Lys ("Actinodin2 precursor") | `rest.uniprot.org/uniprotkb/A0ACM8QEN9.fasta` | full-text |
| and2 alternative | A9JRX1 (and2, 508 aa, unreviewed) also exists | UniProt search `gene_exact:and2 AND organism_id:7955` | listing. Not tested. I assume it is the same sequence but did not check. |
| Repo FASTAs | md5 of the sequence matches my download for all three | `git show origin/claude/elastic-similarity-law-dqxwsj:results/fish-proteins/*.fasta` | full-text (sequence only) |

Which proteins "all three" means is **my inference** from those file names. I found no statement of it.

## Method (my own definition; the original definition is `unknown`)

- **Close pair:** two Cys (or two Lys) at positions i < j with j − i ≤ d. I count every such pair. I ran d = 1 to 5 because the original window is not stated.
- **Null:** shuffle the whole sequence uniformly, preserving composition, 2000 times (seed 1). z = (obs − mean)/SD, using the population SD. p is (1 + #null ≤ obs)/2001 for Cys depletion and (1 + #null ≥ obs)/2001 for Lys clustering.
- **Seed check:** 10 seeds × 2000 shuffles for the key cells.
- Scripts: `replicate-31-shuffle.py` and `replicate-31-seeds.py`, both in this directory.

## Results (simulated)

Cys positions (1-based): kcnk5b 51, 115, 121, 126, 162, 331, 359, 375, 403. The minimum gap is **5** (C121–C126). In and1 and and2 the Cys come in regular C-X6/7-C pairs, and the minimum gap is **7** in both. **CxxC count = 0 in all three** (a direct count, not a simulation).

Cys close pairs, observed / null mean ± SD / z / p(depletion):

| d | kcnk5b | and1 | and2 |
|---|---|---|---|
| ≤3 | 0 / 0.48±0.68 / −0.70 / 0.61 | 0 / 1.31±1.11 / −1.18 / 0.26 | 0 / 2.26±1.38 / **−1.63** / 0.084 |
| ≤4 | 0 / 0.63±0.78 / −0.80 / 0.52 | 0 / 1.74±1.28 / −1.36 / 0.16 | 0 / 2.99±1.60 / **−1.87** / 0.037 |
| ≤5 | **1** / 0.78±0.85 / +0.26 / 0.84 | 0 / 2.17±1.44 / −1.50 / 0.098 | 0 / 3.72±1.79 / **−2.08** / 0.014 |

Positive control, Lys close pairs in kcnk5b: d ≤ 3 gives obs 14 vs 6.31 ± 2.38, z = 3.23, **p = 0.005**. d ≤ 4 gives obs 20, z = 4.22, p = 0.001. d ≤ 5 gives z = 3.76, p = 0.002.

Spread across seeds (10 × 2000 shuffles): and2 Cys z is −1.53 to −1.63 at d ≤ 3, −1.76 to −1.87 at d ≤ 4, and −1.98 to −2.08 at d ≤ 5. The kcnk5b Lys p is 0.0030 to 0.0055 at d ≤ 3.

Arithmetic example (and2, d ≤ 4): z = (0 − 2.99)/1.60 = −1.87.

## My value

Under a window where the claim's first clause holds (zero Cys close pairs in all three, so d ≤ 4), and2 depletion is **z ≈ −1.8 ± 0.1 (d ≤ 4, p ≈ 0.04)** or **z ≈ −1.6 (d ≤ 3, p ≈ 0.09, not significant)**. A z near −2.0 appears only at d ≤ 5, and at d ≤ 5 kcnk5b has one Cys close pair (C121–C126), so "zero in all three" no longer holds. The window that reproduces the positive control (Lys p = 0.005) is d ≤ 3, and at d ≤ 3 and2 depletion is not significant at α = 0.05.

The original window might be defined differently: as a residue gap rather than a position difference, or as Cys-with-neighbour counts rather than pair counts. Under either, the claimed numbers might all hold together. I cannot rule that out, because the definition is `unknown` to me.

**Caveat (my inference):** the and2 "depletion" comes from its regular C-X7-C paired-cysteine architecture. That is a structured repeat, not a random arrangement, so a composition-preserving full shuffle is a weak null for it. The result says Cys are evenly spaced, not that close pairs are selected against.

## Comparison with the recorded value

The recorded values (from the task text) are and2 z = −2.02 and positive control p = 0.005, with zero Cys close pairs in all three.
- No CxxC motifs: **AGREE** (0 in each).
- Zero Cys close pairs in all three: **AGREE for d ≤ 4. DISAGREE for d ≥ 5** (kcnk5b C121–C126).
- and2 z = −2.02: reproduced only at d ≤ 5, where the "zero in all three" clause fails. At d ≤ 3, the window that reproduces p = 0.005, I get z ≈ −1.6 (not significant). No single window under my definition reproduces all three numbers together.
- Overall: **CANNOT TELL.** The individual numbers can each be reproduced, but not under one window, and the original window definition is unknown.

```swarm-replication
{"claim_id": 31, "my_value": "and2 Cys close-pair depletion z = -1.87 (d<=4, p~0.04; seed range -1.76..-1.87); z = -1.63 at d<=3; z = -2.08 only at d<=5 where kcnk5b has 1 pair (C121-C126); CxxC = 0 in all three", "agrees": null, "note": "Each recorded number (zero pairs, z=-2.02, Lys p=0.005) is reproducible under some window but no single position-difference window gives all three at once, and the original window definition is unknown."}
```
