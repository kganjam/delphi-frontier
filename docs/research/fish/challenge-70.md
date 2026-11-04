# Challenge 70 — adversarial review

**Claim under review (claim_id 70), verbatim:**

> "and2 disorder call is NOT supported either way: FoldIndex +0.035 on mature chain, 95% bootstrap
> CI [-0.052,+0.152] spans the boundary (challenger-reported, unverified)."

Recorded evidence level: `derived`. Recorded value: 0.035 FoldIndex.
Source: `challenge-28.md` on branch `claude/review-and2-disorder-claim-tq2sbd`.

**Verdict: SURVIVED.** I tried to break the number, the interval and the "either way" conclusion,
and could not. Two caveats on how the interval is reported are in §3; they change no conclusion.

Everything below is **computed or predicted, not observed.** No experimental structural data on
And2 was found by me or by the source (scope in §5).

---

## 1. Arithmetic, redone independently

I re-downloaded the sequences myself and wrote my own FoldIndex
(`FI = 2.785·⟨H⟩ − |⟨R⟩| − 1.151`, Kyte–Doolittle rescaled as (KD+4.5)/9, ⟨R⟩ = (K+R−D−E)/N).
I did not run or read the source's `foldindex_recheck.py`. My script is
`challenge-70_foldindex.py`, committed beside this file.

Inputs (UniProt REST, read-level: **full record**):

- `A9JRX1`, gene `and2`, 508 aa, unreviewed (TrEMBL). The signal peptide 1–23 carries evidence
  code ECO:0000256 (SAM/SignalP), meaning it is an **automatic prediction, not an experimentally
  determined cleavage site**.
- `A0ACM8QEN9`: its sequence is byte-identical to A9JRX1, so the choice between the two entries
  makes no difference.

| chain | N | ⟨H⟩ | ⟨R⟩ | FoldIndex (mine) |
|---|---|---|---|---|
| and2 precursor | 508 | 0.4434 | −0.0138 | +0.0700 |
| **and2 mature (24–508)** | 485 | 0.4319 | −0.0165 | **+0.0353** |
| and1 precursor (`E7F5V5`) | 570 | 0.4019 | −0.0246 | −0.0563 |
| kcnk5b (`Q6PFU3`) | 448 | 0.4816 | +0.0246 | +0.1657 |

**The point value +0.035 reproduces exactly.**

**Interval.** I wrote my own block bootstrap: 4,000 resamples, concatenating random blocks up to
the length of the chain. With 51-residue blocks, non-circular, seed 99, I get **[−0.053, +0.152]**,
which matches the claimed [−0.052, +0.152] to within resampling noise. **The interval
reproduces.**

## 2. Is a proxy standing in for the quantity that matters?

Yes, and there are two proxies:

1. **Whole-chain FoldIndex stands in for residue-level disorder.** The source already establishes
   this (Huang, Oldfield et al. 2014 report 79% balanced accuracy for Kyte–Doolittle C-H
   classification). I did not re-read that paper (read-level for me: **could-not-access, not
   attempted**; I rely on the source's full-text reading). This proxy problem **helps** the claim:
   the claim is a statement of *indeterminacy*, and adding classifier error on top of a score that
   sits 0.035 from the boundary only makes it more indeterminate.
2. **A residue-resampling interval stands in for classification uncertainty.** A fixed sequence
   has no sampling error. The bootstrap measures how heterogeneous the composition is along the
   chain, not the probability that And2 is disordered. The quantity that actually matters,
   P(disordered | FI = +0.035), would need the class-conditional score distributions from a
   benchmark, which I do not have, so it is `unknown`. This is a defect in what the interval
   *means*. It does not threaten the conclusion: under either reading, +0.035 lies inside the
   ambiguous zone.

## 3. Hidden assumptions, relaxed

| assumption | relaxation | FoldIndex | 95% CI | share of resamples < 0 |
|---|---|---|---|---|
| 51-aa blocks, non-circular (as claimed) | — | +0.035 | [−0.053, +0.152] | 17% |
| block length | 1 (iid residues) | +0.035 | [−0.055, +0.115] | 25% |
| block length | 100, non-circular | +0.035 | [−0.034, +0.178] | 8% |
| block length | 100, circular | +0.035 | [−0.095, +0.157] | 30% |
| circular vs not | 51, circular | +0.035 | [−0.069, +0.135] | 27% |
| **mature chain = SignalP cut** | additional cleavage at the RKRR motif (residues 47–50, a furin-like R-X-[KR]-R site I found by scanning the sequence) → chain 51–508 | **+0.050** | [−0.042, +0.163] (51, non-circ.) | 12–18% |

Findings:

- **"Spans the boundary" is robust.** Every variant I tried contains zero (block length 1–100,
  circular and non-circular, two candidate mature chains). This is the part of the claim that
  carries its conclusion, and it holds.
- **Caveat A, reporting precision.** The endpoints depend on protocol: the upper bound ranges from
  +0.115 to +0.178, and the share of resamples called disordered ranges from 8% to 30%. The
  interval should be reported together with its protocol (51-aa blocks, non-circular, 4,000
  resamples), not as a property of the protein.
- **Caveat B, which chain is "mature".** The 1–23 cut is a SignalP prediction. The RKRR propeptide
  scenario is **my inference from the sequence motif only**. I found no evidence that And2 is
  processed there, and I am not claiming that it is. Even if it were, the score would move to
  +0.050, which is still inside the indeterminate zone.

## 4. Is the evidence level honest?

**Yes.** `derived` is correct, and the claim labels itself "challenger-reported, unverified",
which was accurate when it was recorded. After this review, the number and the interval are
**independently reproduced**, though still derived and not measured. Nothing in the claim is
presented as an observation.

## 5. Missed regime or counter-evidence?

I looked for evidence that would settle the question "either way". If such evidence existed, the
claim would be wrong.

- **AlphaFold2.** I fetched the AFDB v6 API summary myself (read-level: **full record** for the
  summary fields; I did not fetch the per-residue file). For A9JRX1: mean pLDDT 55.91, fraction
  very low (<50) **0.459**, fraction very high (>90) **0.004**. For E7F5V5: 57.06, 0.416, 0.053.
  The and2 values match the source. For and1, the source gives 4.9% very-high and AFDB's summary
  gives 5.3%. That is a small disagreement, which I am preserving and not resolving, and it does not
  affect this claim.
  - Does this settle the question in favour of disorder? **My inference: no.** Low pLDDT is
    expected both for genuine disorder and for proteins with shallow multiple sequence alignments.
    The source reports actinodins as teleost- and elephant-shark-specific, and that lineage
    restriction plausibly means few homologs. I did not measure MSA depth (`unknown`), so AF2
    cannot separate "disordered" from "unmodellable" here. AF2 does show that **no folded core is
    predicted**. As the source itself says, "no fold predicted" is not "disordered".
- **Experimental data.** I did not run a new literature search. I rely on the source's negative
  search (no PDB entry, no CD/NMR/SAXS located; scope: one web search plus the actinodin
  literature). **The scope of that negative is the source's, not mine.**

So no predictor in hand, and no experiment, resolves And2's disorder status. That is exactly what
the claim says.

## 6. Why SURVIVED

- The point value (+0.0353) and the interval ([−0.053, +0.152]) reproduce from independently
  retrieved sequences and independent code.
- The proposition that carries the conclusion, that the interval spans zero, survives every
  relaxation I tried.
- The orthogonal predictor (AF2) does not break the "either way" symmetry, because low pLDDT
  cannot tell disorder apart from a shallow alignment for a lineage-restricted protein.
- The faults I found are reporting caveats (protocol-dependent endpoints; a SignalP-predicted
  rather than measured cleavage site). Neither moves the score out of the ambiguous zone.

Suggested wording for the record (optional; the substance is unchanged):

> and2 disorder status is unresolved by prediction. Whole-chain FoldIndex is +0.035 on the
> SignalP-predicted mature chain (24–508); the 95% block bootstrap (51-aa non-circular blocks,
> 4,000 resamples) is [−0.052, +0.152], and its endpoints are protocol-dependent, but every
> variant tested spans 0. AF2 predicts no folded core (0.4% pLDDT>90) but cannot tell disorder
> apart from a shallow alignment. Derived; independently reproduced; no experimental data.

### Read-levels

| source | read-level |
|---|---|
| UniProt `A9JRX1`, `A0ACM8QEN9`, `E7F5V5`, `Q6PFU3` (sequence, signal-peptide evidence code) | full record |
| AFDB v6 prediction API, `A9JRX1`, `E7F5V5` | full record (summary fields only) |
| `challenge-28.md` (source) | full text |
| Huang, Oldfield et al. 2014; Prilusky et al. 2005 | not read by me; cited via the source |

```swarm-challenge
{"claim_id": 70, "outcome": "survived", "reason": "Independent re-implementation reproduces FoldIndex +0.0353 on A9JRX1 24-508 and a 51-aa block-bootstrap CI of [-0.053,+0.152]; the interval spans zero under every relaxation tried (block length 1-100, circular/non-circular, an alternative RKRR-processed chain at +0.050), and AF2 low pLDDT cannot break the either-way symmetry, so the indeterminate verdict stands, with the caveat that the CI endpoints are protocol-dependent and the mature chain is SignalP-predicted.", "corrected_value": null, "depends_on": ["UniProt A9JRX1 sequence (508 aa)", "UniProt A9JRX1 signal peptide 1-23 (SignalP, ECO:0000256)", "FoldIndex formula 2.785<H>-|<R>|-1.151 with Kyte-Doolittle scale (Prilusky 2005, via challenge-28)", "block bootstrap protocol: 51-aa non-circular blocks, 4000 resamples", "AFDB v6 A9JRX1 summary: fractionPlddtVeryLow 0.459, VeryHigh 0.004", "challenge-28 negative literature search for experimental And2 structure data"]}
```
