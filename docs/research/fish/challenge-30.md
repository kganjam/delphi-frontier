# Challenge 30: "Tyrosine spatial clustering is significant in and2 but NOT in and1"

**Claim under review (the author's words):** "Tyrosine spatial clustering is significant in and2
(0.393 observed vs 0.211 shuffled, z=2.74, p=0.011) but NOT in and1 (p=0.064, where Tyr content
alone explains most of it); kcnk5b control p=0.72." Recorded evidence level: derived. Source: a
2000-shuffle test by the running agent.

**Verdict: WEAKENED.** I reproduced the and2 number. The "NOT in and1" half, and the explanation
given for it, do not hold up.

## Inputs

| Input | Source | Read-level |
|---|---|---|
| and1, Actinodin1 precursor, 570 aa, 47 Tyr | UniProt E7F5V5 SV=2, `rest.uniprot.org/uniprotkb/E7F5V5.fasta`, fetched 2026-11-04 | full-text (full sequence) |
| and2, Actinodin2 precursor, 508 aa, 29 Tyr | UniProt A0ACM8QEN9 SV=1, fetched 2026-11-04. I checked that A9JRX1 (used by S23) has the **identical** sequence. | full-text (full sequence) |
| kcnk5b, 448 aa, 12 Tyr | UniProt Q6PFU3 SV=1, fetched 2026-11-04. A0A8M1PBI1 gives the same Tyr spacing statistic. | full-text (full sequence) |
| The author's script or statistic definition | `git grep` across every `origin/*` branch (`*.md`, `*.py`) for `shuffl`, `tyr.*cluster`, `0.393`, `0.211`, `kcnk5b.*control`. No hits related to this claim. | could-not-access |

The claim does not define its statistic. I **reconstructed** it: **the fraction of
consecutive-Tyr gaps that are ≤ 4 residues**. For and2 this is 11/28 = 0.3929, which matches the
stated 0.393 exactly. The analytic null for a random sequence is about 1 − (1 − 29/508)^4 ≈ 0.21,
which matches the stated 0.211. This is my inference. The author may have used a different
statistic that happens to give the same values.

The script is at `docs/research/fish/challenge30_tyr.py`. All numbers below are **computed**
(simulation by permutation, 20 000 shuffles unless stated). None of them is observed.

## 1. Independent arithmetic

| Protein | Tyr / gaps | Gaps ≤ 4 | Observed | Null mean | z | p (one-sided) |
|---|---|---|---|---|---|---|
| and1 | 47 / 46 | 18 | 0.391 | 0.292 | 1.75 | 0.058 |
| and2 | 29 / 28 | 11 | 0.393 | 0.210 | 2.63 | 0.012 |
| kcnk5b | 12 / 11 | 1 | 0.091 | 0.102 | −0.12 | 0.71 |

With 2000 shuffles and 5 seeds, p ranged 0.0085–0.0145 (and2), 0.053–0.064 (and1) and
0.69–0.73 (kcnk5b). **The stated numbers reproduce within Monte-Carlo noise.** My z (2.63) is
slightly below the stated 2.74. This is consistent with seed or SD-estimator differences and
does not change anything.

## 2. Hidden assumptions, relaxed

**(a) The threshold t = 4 is unstated and changes the result.** All values below are computed.

| t (gap ≤ t) | and2 p | and1 p |
|---|---|---|
| 2 | 0.63 | 0.62 |
| 3 | 0.019 | 0.11 |
| **4** | **0.012** | **0.058** |
| 5 | 0.053 | 0.098 |
| 6 | 0.065 | 0.069 |

Only t = 3 and t = 4 give p < 0.05 for and2. A Bonferroni correction over these 5 thresholds
puts the best and2 p at about 0.06. A correction over 2 proteins at fixed t gives about 0.024. I
cannot tell whether t = 4 was chosen before the data were seen. Either way, the claim does not
disclose that this choice was made.

**(b) "NOT in and1" depends on how the statistic is defined.** If each run of consecutive Tyr
(YY, YYY) counts as one event, the result changes (computed): and1 p = 0.022, and2 p = 0.0055.
and1 has two such runs (Y168–Y169 and Y206–Y208); and2 has one (Y195–Y197). Under this equally
defensible statistic, **both** proteins are significant at 0.05.

**(c) Local-composition null (block shuffles).** Shuffling within windows of fixed size keeps
regional Tyr density (computed):

| Window | and2 p | and1 p |
|---|---|---|
| 100 aa | 0.011 | 0.14 |
| 50 aa | 0.035 | 0.16 |
| 20 aa | 0.032 | 0.17 |

and2 stays below 0.05, but its p value is not stable across window sizes.

**(d) Repeat motif.** Three of the 11 close pairs in and2 sit in the recurring `DPYC`
Cys-repeat context: `NPYLDPYCLY` (151–158) and `RYDPYCL` (351–354). A shuffle null treats every
residue as independent, so the clustering may be inherited from the repeat architecture rather
than placed independently. When I masked the Tyr in those two segments, and2 stayed
significant (computed: obs 0.348 vs null 0.177, p = 0.024). The and2 signal is therefore **not
solely** a repeat artefact. I did not run a profile/HMM repeat analysis, so degenerate repeats
I could not see may still contribute.

Excluding the signal peptide (residues 1–20) has no effect: and2 p = 0.014. Splitting the
sequence loses power: 1–300 p = 0.073, 301–508 p = 0.045.

## 3. Logical defects in the claim

1. **"Tyr content alone explains most of it" is incoherent for this test.** A full-sequence
   shuffle keeps Tyr content exactly, so the null already accounts for content. My inference:
   the author meant that and1's higher Tyr density (8.25 % vs 5.71 %) raises the null
   (0.292 vs 0.210). That is not the same as content "explaining" the observed value.
2. **A difference in significance is not a significant difference.** The observed statistic is
   essentially identical in the two proteins: 0.391 (and1) and 0.393 (and2). The excess over the
   null is +0.10 (and1) and +0.18 (and2), and and1's p of 0.058 sits on the boundary. Nothing
   here tests whether and1 and and2 differ. The data support "both show a modest excess of close
   Tyr spacing. It is nominally significant in and2 and borderline in and1."
3. **The kcnk5b control has almost no power.** It has 11 gaps, and its null distribution is so
   coarse that p = 1.00 at t ≤ 3. A p of 0.72 on this protein says little about the
   false-positive rate. A proper control would be a panel of Tyr-matched secreted or disordered
   proteins. I did not run one.

## 4. Proxy

The quantity that matters for the di-Tyr crosslinking hypothesis (S23 §3.3) is **3D proximity
of solvent-exposed Tyr within or between assembled fibrils**. This test measures a proxy:
**linear sequence spacing**. Close spacing in sequence is neither necessary nor sufficient for
di-Tyr formation, which is often inter-chain. No structural model or crosslink measurement
(for example di-Tyr fluorescence or MS) was run, so the right quantity is **unknown**.

## 5. Evidence level

"Derived" is honest: this is a computed permutation result, not an observation. One caveat: the
statistic and threshold are undocumented, so the recorded value of 0.011 cannot be reproduced
from the record alone. I could only match it by reverse-engineering.

## 6. Counter-examples and published work

I did not search the literature for published analyses of Tyr spacing in actinodins. Scope of
negative search: the repository's branches only (see Inputs). Whether such work exists is
**unknown**.

## Corrected statement (my wording)

Computed, not observed: under a full-sequence shuffle, the fraction of consecutive-Tyr gaps
≤ 4 aa is higher than expected in and2 (0.393 vs 0.210, p ≈ 0.012, 20 000 shuffles). The excess
is borderline in and1 (0.391 vs 0.292, p ≈ 0.058). Both p values depend on the threshold (and2
p ranges 0.012–0.63 for t = 2–6) and on how Tyr runs are counted (and1 p = 0.022 when runs are
collapsed). Neither is corrected for multiple comparisons. The and1/and2 contrast is not
supported, and the kcnk5b control has too few Tyr to calibrate the test.

```swarm-challenge
{"claim_id": 30, "outcome": "weakened", "reason": "The and2 p≈0.012 reproduces under the reconstructed statistic (fraction of Tyr–Tyr gaps ≤4 aa), but it is threshold-dependent (p 0.012–0.63 over t=2–6) and uncorrected, the 'NOT in and1' contrast flips to p=0.022 when Tyr runs are collapsed, 'content explains it' is incoherent for a composition-preserving shuffle, and the 12-Tyr kcnk5b control is underpowered.", "corrected_value": "and2 p≈0.012 (t≤4, full shuffle, 20000 perms; range 0.006–0.63 across thresholds/nulls); and1 p≈0.058 (range 0.022–0.21); difference between and1 and and2 not tested"}
```
