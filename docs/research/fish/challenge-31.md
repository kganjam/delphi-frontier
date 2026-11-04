# Challenge 31 — "Cysteine close pairs are zero … points the crosslink design inter-chain"

**Claim under review (author's words, commit `699500a7`, `docs/research/fish/proteins-disorder.md` §4
on branch `origin/swarm-architecture`):** "Cysteine close pairs are ZERO in all three and
significantly fewer than chance in and2 (z=−2.02), with no CxxC motifs: any disulfide architecture
would have to be long-range intra-chain or INTER-chain, which points the crosslink design inter-chain."
Recorded evidence level: *derived*. Source: 2,000-shuffle test; Lys clustering in kcnk5b (p=0.005)
as positive control.

**Verdict: WEAKENED.** The count reproduces exactly. The significance is right in direction but was
reported with the wrong-tail p-value and is not multiplicity-robust. The design inference does not
follow, because the proxy ("gap ≤ 4") hides the dominant feature of the actinodin cysteines: they
sit in a recurring **C-x6/7-C** spacing (gap 7–8) that is massively over-represented against the
same shuffle null. That is a *short-range intra-chain* pattern, which the claim says is excluded.

## Inputs (read-level)

- Sequences: `results/fish-proteins/{A0ACM8QEN9 (and2), E7F5V5 (and1), Q6PFU3 (kcnk5b)}.fasta` on
  `origin/swarm-architecture` — **full-text** (read directly). Full precursor sequences, signal
  peptides included (as in the original).
- Original scripts `disorder.py`, `disorder2.py`, `tyr_null.py` — **could-not-access**: not committed
  on any branch I checked (`git log --all`, `git grep` across all remote branches). So I could not
  diff methods; I re-implemented from the doc's stated definition: "fraction of consecutive
  same-residue gaps ≤ 4 residues", null = composition-preserving full-sequence shuffle.
- My scripts: `scripts/challenges/challenge31_cys_close.py`, `scripts/challenges/challenge31_cys_midrange.py`
  (20,000 shuffles each). Everything below is **calculated**, not observed.

## 1. Independent arithmetic

Cys positions → consecutive gaps (computed here):

| | length | nCys | consecutive Cys gaps | min gap | gaps ≤4 |
|---|---|---|---|---|---|
| kcnk5b | 448 | 9 | 64, 6, 5, 36, 169, 28, 16, 28 | 5 | 0 |
| and1 | 570 | 16 | 8, 23, 8, 68, 7, 26, 8, 19, 8, 17, 8, 85, 8, 44, 8 | 7 | 0 |
| and2 | 508 | 20 | 8, 26, 8, 61, 7, 26, 8, 19, 8, 23, 8, 31, 8, 36, 8, 19, 7, 28, 8 | 7 | 0 |

CC, CxC, CxxC counts: 0 in all three. **"Zero close pairs in all three" and "no CxxC" — confirmed.**
(Note "no CxxC" is not independent evidence: a CxxC is a gap of 3, already inside "gap ≤ 4".)

Shuffle test, my re-run (20,000 shuffles, seed-dependent at the second decimal):

| | null mean | z (mine) | z (author) | upper-tail p | **lower-tail p** | analytic P(no gap ≤4) |
|---|---|---|---|---|---|---|
| kcnk5b | 0.078 | −0.85 | −0.84 | 1.00 | 0.51 | 0.510 |
| and1 | 0.109 | −1.43 | −1.43 | 1.00 | 0.16 | 0.164 |
| and2 | 0.149 | −1.95 | −2.02 | 1.00 | **0.038** | **0.037** |

The analytic column is exact for random placement of m Cys on a line of N sites:
C(N−4(m−1), m)/C(N, m). It agrees with the shuffles. Positive control also reproduces: kcnk5b Lys
z=+3.12, p=0.0016 (author: +3.03, 0.005); Tyr and2 z=+2.67, p=0.010 (author +2.74, 0.011).

Defects in how the significance was reported:
- The table prints **p = 1.00** for and2 Cys beside the words "significantly fewer". That is the
  upper-tail p and tests the opposite hypothesis. The relevant one-sided lower-tail p is ≈0.037
  (calculated). The author's word "significantly" rests on |z| > 2 alone.
- The null is discrete (and2 observed = 0, the floor), so z from a mean/SD is a poor summary; the
  exact probability (0.037) is the honest number.
- Nine residue×protein tests were run in that table; 0.037 does not survive even a Bonferroni-3
  correction within the Cys row (0.11). "Significant" should be "nominally, uncorrected".

## 2. The proxy: "gap ≤ 4" stands in for "disulfide geometry"

The quantity that matters for the design inference is *which Cys–Cys sequence separations are
available for disulfides*, not whether any are within 4. Disulfide-bonded pairs with small loop
separations other than CxxC are common in small cysteine-rich domains; "gap ≤ 4 is zero" says only
that the tightest loops are absent. The right test is the full gap distribution against the same null.

Doing that (calculated, 20,000 shuffles):

| | Cys gaps of 7–8 (obs) | null mean ± SD | z | p_hi | Cys gaps 5–10 (obs) | null | p_hi |
|---|---|---|---|---|---|---|---|
| kcnk5b | 0 | 0.28 ± 0.52 | −0.5 | 1.0 | 2 | 0.86 | 0.20 |
| and1 | **8 of 15** | 0.71 ± 0.81 | **+9.0** | <5e-5 (0/20,000) | 8 | 2.12 | 0.00015 |
| and2 | **10 of 19** | 1.16 ± 1.02 | **+8.6** | <5e-5 (0/20,000) | 10 | 3.50 | 0.00025 |

The 7–8 window was chosen **after** seeing the gaps, so its p-value is inflated by selection; the
5–10 window is a generic "short loop" window and still gives p ≈ 2×10⁻⁴. The motifs themselves
(and2, positions 0-based): `CANSDDPDC`, `CNPYLDPYC`, `CNPSDTEC`, `CDPTKDPYC`, `CNPATDPLC`,
`CNPLFDEGC`, `CDPRYDPYC`, `CYMFYDKDC`, `CHPFDPNC`, `CDPEIDYNC` — the same "C…DP…C" elements the
author's own §3 noted as motif matches, but did not connect to §4. Every one of and2's 20 Cys
(and 16 of and1's 16) sits in such a pair: the cysteines are **paired at fixed short spacing**, not
"dispersed". The zero at gap ≤ 4 is a by-product of that fixed spacing (the minimum gap is 7).

## 3. Hidden assumption that carries the result

Assumption: "if no Cys are within 4, intra-chain disulfides must be long-range." Relaxing the
cutoff from 4 to 10 reverses the picture: in both actinodins the short-range (i, i+7/8) Cys pair
is the single most over-represented feature in the whole Cys/Tyr/Lys panel (z ≈ +9 vs the strongest
reported signal, Lys kcnk5b z ≈ +3). The conclusion is entirely a function of the arbitrary cutoff.

What my result does **not** show (inference, separated): sequence spacing does not establish that
these pairs are bonded, nor bonded to each other rather than to another chain. A C-x6/7-C element
is *compatible* with a short intra-chain loop and also with inter-chain bonding. So the correct
statement is that the data **do not discriminate** intra- vs inter-chain — not that they point
inter-chain. If anything, a strongly conserved fixed spacing is the signature one would expect of
a local structural unit, which tilts (weakly, by inference only) the other way.

## 4. Evidence level

"derived" is honest for the count and the z. But the sentence "any disulfide architecture would have
to be long-range … or inter-chain" is presented as a consequence of the derivation; it is an
**inference** that the derivation does not support. The p=1.00 printed beside "significantly fewer"
is a reporting defect.

## 5. Regimes / counter-examples missed

- The author's own data (§3 C…DP…C motifs, 4 in and1, 6 in and2 by their count; 8 and 10 C-x6–9-C
  by mine with a looser pattern) is the counter-example.
- kcnk5b as Cys control is weak for this question: it has only 9 Cys, and K2P channels are known
  to form an inter-subunit disulfide via a cap-domain Cys (general knowledge, **not** re-sourced
  here — read-level: none; I did not verify which kcnk5b Cys). So the control doesn't calibrate
  intra- vs inter-chain either.
- Literature on actinodin disulfide connectivity: **unknown** — I did not search; no experimental
  connectivity data were found in the repository (scope: all remote branches, `git grep` for
  cysteine/CxxC/disulfide terms).
- Precursor vs mature chain: the signal peptides contain no Cys, so trimming them changes N slightly
  and does not change any conclusion (not separately re-run; inference from the sequences).

## Corrected statement

"Cys pairs at separation ≤ 4: 0 in all three (calculated); for and2 this is nominally fewer than
composition predicts (exact lower-tail p ≈ 0.037, uncorrected; reported p=1.00 was the wrong tail).
But the actinodin Cys are not dispersed: 8/15 (and1) and 10/19 (and2) consecutive Cys gaps are 7–8
residues, ≈9 SD above the shuffle null (calculated; window chosen post hoc; generic 5–10 window
p ≈ 2×10⁻⁴). Sequence spacing alone does not decide intra- vs inter-chain disulfides, so it does
not point the crosslink design inter-chain."

```swarm-challenge
{"claim_id": 31, "outcome": "weakened", "reason": "The zero-close-pair count reproduces (and2 lower-tail p≈0.037, not the reported p=1.00), but the gap≤4 proxy hides that actinodin cysteines are paired at a fixed i,i+7/8 spacing far above chance (z≈+9), a short-range intra-chain-compatible pattern, so the inference that disulfides must be long-range or inter-chain does not follow.", "corrected_value": "0 Cys pairs at gap ≤4 residues in all three (and2 lower-tail p≈0.037); Cys pairs at gap 7–8 residues: and1 8/15, and2 10/19 (null ≈0.7 and ≈1.2)"}
```
