# Candidate loci detected in GCA_018398805.1 (Hirundichthys speculiger)

Tool: miniprot 0.18-r281 · assembly FASTA sha256 `6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052`

**Scope.** Protein-to-genome alignment only. Not an annotation, not an ortholog assignment, not expression, not function. aa_identity = PAF column 10 (number of residue matches) / column 11 (alignment block length), both as miniprot reports them for the aligned block; it is not computed over the whole query. The number of ALTERNATIVE hits per query is not comparable to an unchunked run: -N5 and --outs=0.6 were applied per chunk, so secondary-hit counts can exceed 5 and are chunking artefacts. Best hits are unaffected because no scaffold was split.

| zebrafish query | UniProt | round | scaffold | interval | cov | aa id | AS | hits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cacna1g | A0AC58GY43 | round2 | JAGFBZ010002163.1 | 81287–379776 | 0.64 | 0.733 | 5064 | 7 |
| kcnh2b | A0AC58ISY3 | round3 | JAGFBZ010001591.1 | 1301510–1540581 | 1.0 | 0.762 | 3702 | 5 |
| kcnh2a | Q108P2 | round2 | JAGFBZ010001591.1 | 1301510–1579457 | 1.0 | 0.61 | 3088 | 7 |
| hhip | A1A5I0 | round2 | JAGFBZ010000865.1 | 2512–37451 | 1.0 | 0.768 | 2509 | 2 |
| slc43a2b_LAT4 | Q5PR35 | round2 | JAGFBZ010000485.1 | 561206–573455 | 1.0 | 0.786 | 2034 | 3 |
| tbx5a | Q9IAK8 | round1 | JAGFBZ010001382.1 | 1635753–1651051 | 1.0 | 0.782 | 1870 | 13 |
| actb1_POSITIVE_CONTROL | Q7ZVI7 | round1 | JAGFBZ010000555.1 | 105626–107418 | 1.0 | 0.989 | 1817 | 12 |
| tbx4 | F1R688 | round1 | JAGFBZ010001446.1 | 295196–317271 | 1.0 | 0.728 | 1814 | 8 |
| gja1_cx43_sof | O57474 | round2 | JAGFBZ010000226.1 | 84055–85219 | 1.0 | 0.892 | 1789 | 10 |
| kcnk5a | Q32PR9 | round3 | JAGFBZ010000776.1 | 49243–65363 | 1.0 | 0.691 | 1707 | 2 |
| shha | Q92008 | round1 | JAGFBZ010001012.1 | 2187728–2194143 | 1.0 | 0.743 | 1526 | 4 |
| and2 | A9JRX1 | round2 | JAGFBZ010000267.1 | 345469–347985 | 0.935 | 0.597 | 1499 | 3 |
| shhb_twhh | Q90419 | round2 | JAGFBZ010001012.1 | 2187764–2194128 | 0.964 | 0.728 | 1455 | 4 |
| and1 | E7F5V5 | round1 | JAGFBZ010000980.1 | 814249–819560 | 0.982 | 0.552 | 1448 | 2 |
| pitx1 | A9Y0D5 | round1 | JAGFBZ010001412.1 | 734755–740041 | 0.989 | 0.901 | 1294 | 2 |
| edar | A0A0R4IGE7 | round1 | JAGFBZ010000884.1 | 50977–73674 | 0.948 | 0.637 | 1268 | 1 |
| hoxa13a | Q6W990 | round1 | JAGFBZ010001649.1 | 576986–578444 | 1.0 | 0.723 | 1124 | 7 |
| kcnk5b | Q6PFU3 | round1 | JAGFBZ010001926.1 | 604214–606769 | 1.0 | 0.563 | 1086 | 8 |
| eda | B0YIF1 | round3 | JAGFBZ010002033.1 | 3037482–3047982 | 0.93 | 0.645 | 907 | 10 |
| tbx5b | E3W6T6 | round3 | JAGFBZ010000035.1 | 4085363–4093111 | 0.72 | 0.668 | 859 | 10 |
| fgf24 | Q0IIQ7 | round1 | JAGFBZ010002071.1 | 503196–516000 | 1.0 | 0.829 | 760 | 3 |
| fgf20a | Q38PL0 | round3 | JAGFBZ010000863.1 | 375649–377241 | 1.0 | 0.752 | 755 | 3 |
| msxb | Q03356 | round1 | JAGFBZ010000863.1 | 508027–509355 | 1.0 | 0.604 | 734 | 10 |
| msxb | Q03356 | round2 | JAGFBZ010000863.1 | 508027–509355 | 1.0 | 0.604 | 734 | 10 |
| rcan2 | E7F2L5 | round2 | JAGFBZ010000363.1 | 605297–649997 | 0.857 | 0.665 | 595 | 2 |
| fgf10a | Q8AY90 | round1 | JAGFBZ010000446.1 | 2711368–2727894 | 1.0 | 0.573 | 584 | 2 |
| fgf10b | Q1XG75 | round3 | JAGFBZ010002193.1 | 497969–503585 | 0.765 | 0.753 | 506 | 3 |
| slc43a2a_fragment | Q7ZUS0 | round2 | JAGFBZ010001224.1 | 1267873–1271840 | 0.908 | 0.748 | 474 | 3 |
| hoxd13a | Q90472 | round1 | JAGFBZ010000479.1 | 5214025–5216883 | 0.824 | 0.447 | 401 | 7 |

## Controls

- `actb1_POSITIVE_CONTROL` (round1): expectation coverage >= 0.95 and aa_identity >= 0.95 → **PASS**
- `fgf10a_SHUFFLED_NEGATIVE_CONTROL` (round1): expectation no hit → **PASS**
- `kcnh2a_SHUFFLED_NEGATIVE_CONTROL` (round2): expectation no hit → **PASS**
- `eda_SHUFFLED_NEGATIVE_CONTROL` (round3): expectation no hit → **PASS**

## Reproducibility across the two runs

- `msxb` mapped in round1, round2: same locus within 100 bp = **True** (JAGFBZ010000863.1 508027–509355 vs JAGFBZ010000863.1 508027–509355)

## Paralog ambiguity (a limit of the method, not a finding)

- `shha` and `shhb_twhh` best-hit the same region of JAGFBZ010001012.1 (overlap 6364 bp). These two query proteins cannot be assigned to distinct loci from best-hit protein-to-genome alignment alone.
- `kcnh2a` and `kcnh2b` best-hit the same region of JAGFBZ010001591.1 (overlap 239071 bp). These two query proteins cannot be assigned to distinct loci from best-hit protein-to-genome alignment alone.
