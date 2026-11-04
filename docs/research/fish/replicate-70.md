# Replicate 70: and2 intrinsic-disorder call, re-derived independently

**Question (answer withheld from me):** "and2 disorder call is NOT supported either way".
The inputs were said to live in `challenge-28.md` on branch `claude/review-and2-disorder-claim-tq2sbd`.

**Note on what I saw.** To find the inputs I read the first 40 lines of that `challenge-28.md`, and I
stopped there. Those lines contain:

- claim 28 verbatim: and2 FoldIndex +0.070, 40.0% disordered windows against a folded control at 38.4%, and1 −0.056
- claim 28's recorded value (0.07 FoldIndex) and its positive control (kcnk5b +0.166)
- the challenger's verdict "REFUTED"
- the start of the challenger's method (the Prilusky formula, and1 = `E7F5V5`)

I did not read the challenger's numbers, code, or reasoning past line 40. Everything below is my
own derivation. Because I knew the target numbers before computing, the FoldIndex arithmetic
check is not blind. The two extra predictors in §3 were not in the part I read.

**Everything in this file is computed or predicted. None of it is observed.** I found no
experimental structural measurement of And1 or And2. The scope of that negative is limited: I
only checked whether UniProt and AlphaFold DB hold any experimental structure. I did not search
the literature for CD, NMR or SAXS data.

---

## 1. Inputs

| input | value | source | read-level |
|---|---|---|---|
| and2 sequence | UniProt `A9JRX1`, 508 aa (gene `and2`, zgc:175106). `A0ACM8QEN9` is byte-identical; both map to RefSeq NP_001104660.1 | UniProt REST FASTA | full-text (complete record) |
| and2 signal peptide | 1–23 (SignalP annotation in UniProt, so itself a prediction) | UniProt `ft_signal` | full-text |
| and1 sequence | UniProt `E7F5V5`, 570 aa, signal 1–26 | UniProt REST FASTA | full-text |
| kcnk5b control | UniProt `Q6PFU3`, 448 aa, no signal annotated | UniProt REST FASTA | full-text |
| FoldIndex formula | FI = 2.785·⟨H⟩ − \|⟨R⟩\| − 1.151; ⟨H⟩ = mean Kyte–Doolittle hydropathy rescaled as (KD+4.5)/9; ⟨R⟩ = (K+R−D−E)/N; window 51 | Prilusky et al. 2005, *Bioinformatics* 21:3435 | I used the formula as I recall it, and as it appears in challenge-28 lines 24–29. I did **not** re-open the paper, so read-level: could-not-access (paper not fetched) |
| AlphaFold DB global pLDDT and fractions | model v6 for each accession | `alphafold.ebi.ac.uk/api/prediction/<acc>` | full-text (API JSON) |
| AlphaFold per-residue pLDDT | — | `.pdb` and `confidence_v6.json` both returned **403 from the sandbox proxy** | could-not-access |
| metapredict | v3.1.01, `predict_disorder` default network, pip install | local run | n/a (my computation) |

Code: `replicate-70_foldindex.py` (FoldIndex for whole chains and 51-residue windows).

## 2. FoldIndex arithmetic (calculated)

| protein | chain | N | ⟨H⟩ | ⟨R⟩ | FI = 2.785·⟨H⟩ − \|⟨R⟩\| − 1.151 |
|---|---|---|---|---|---|
| and2 | full | 508 | 0.4434 | −0.0138 | 1.2349 − 0.0138 − 1.151 = **+0.0700** |
| and2 | mature (24–508) | 485 | 0.4319 | −0.0165 | **+0.0353** |
| and1 | full | 570 | 0.4019 | −0.0246 | 1.1193 − 0.0246 − 1.151 = **−0.0563** |
| and1 | mature (27–570) | 544 | 0.3884 | −0.0276 | **−0.0969** |
| kcnk5b | full | 448 | 0.4816 | +0.0246 | 1.3413 − 0.0246 − 1.151 = **+0.1657** |

51-residue windows for and2:

- **Per-window convention:** 178 of 458 windows are negative, which is 38.9%.
- **Per-residue convention:** each residue takes the score of its centred window, and the end
  residues take the nearest window. Under this convention 203 of 508 residues are negative, which
  is **40.0%**.
- **Where the negative residues are:** 40–110, scattered residues in 361–375, 383–421, and
  425–508. So the disorder is concentrated at the N-terminal and C-terminal ends.
- **Window range:** from −0.368 to +0.346.

kcnk5b under the per-window convention: 147 of 398 windows are negative, which is 36.9%. I did not
reproduce the claim's 38.4%. The gap is probably a windowing or end convention, and I did not
chase it.

**Arithmetic result:** my numbers match claim 28 for and2 FI (+0.070), and1 FI (−0.056), kcnk5b FI
(+0.166) and the and2 window fraction (40.0%). This is a check of the calculation only. It is not
independent support for any biological conclusion.

## 3. Independent predictors (predicted, not observed)

| protein | AF pLDDT mean (whole chain) | frac pLDDT < 50 | frac pLDDT < 70 | metapredict mean | metapredict frac ≥ 0.5 |
|---|---|---|---|---|---|
| and2 | 55.91 | 0.459 | 0.733 | 0.632 | **0.772** |
| and1 | 57.06 | 0.416 | 0.725 | 0.657 | 0.663 |
| kcnk5b | 69.50 | 0.339 | 0.399 | 0.373 | 0.346 |

- The AlphaFold fractions are whole-chain values taken from the API, signal peptide included,
  because I could not get per-residue data (403).
- frac < 70 is the sum of the API's `fractionPlddtVeryLow` and `fractionPlddtLow` fields.
- metapredict was run on the full chain.
- Low pLDDT means "low confidence". It suggests disorder but does not establish it.

## 4. Interpretation (my inference, separated from the author's claim)

- **Author's claim (claim 28):** and2 is NOT intrinsically disordered, while and1 IS.
- **My inference:** that asymmetry rests entirely on the sign of a whole-chain FoldIndex that sits
  within ±0.07 of zero. The sign also depends on the chain: removing the signal peptide halves
  and2's value to +0.035.
  - kcnk5b is a membrane channel with hydrophobic transmembrane segments, so it is a poor
    "folded" calibrator for a secreted protein.
  - Even taking it at face value, its window fraction (36.9–38.4%) is about the same as and2's
    (~39–40%). The comparison therefore shows that FoldIndex cannot separate the two. It does not
    show that and2 is ordered.
- **The other two predictors disagree with the negative call:**
  - metapredict predicts **77%** of and2 residues as disordered, more than and1's 66%. The
    control is 35%.
  - AlphaFold DB gives and2 essentially the same low-confidence profile as and1: mean 55.9 vs
    57.1, and 73% vs 73% of residues below 70. The control's mean is 69.5.
  - Neither predictor reproduces "and1 disordered, and2 not".
- **Sources disagree, and I keep the disagreement visible:**
  - FoldIndex on the whole chain: and2 is weakly folded (+0.070).
  - FoldIndex per-residue: about 40% of and2 is disordered, at the ends.
  - metapredict: about 77% of and2 is disordered.
  - AlphaFold: about 73% of and2 has low or very low confidence.
- **Mature-chain composition (calculated):** P 12.4%, A 10.3%, 20 Cys, P+G+S 22.5%.
  - The high Pro content fits disorder.
  - 20 cysteines could form disulfides in an extracellular protein. A sequence predictor cannot
    weigh that.

**My value:** and2 whole-chain FoldIndex = **+0.070**. The uncertainty is about ±0.035 from the
choice of chain alone (mature chain gives +0.035), and any value this close to 0 is inside the
method's ambiguous zone. Per-residue, about 40% of and2 is FoldIndex-disordered (38.9–40.0%
depending on windowing).

**Conclusion:** predictions alone cannot support a call that and2 is *not* disordered. The other
two predictors lean towards substantial disorder, but no measurement exists to settle it, so I
make no positive call either. Status: not supported either way, with the predictions tilting
towards partial or extensive disorder.

## 5. Comparison with the recorded value

- **Arithmetic (claim 28):** recorded and2 FoldIndex 0.07. Mine is +0.0700. **AGREE.**
- **Proposition (claim 70):** "and2 disorder call is NOT supported either way". The negative call
  ("and2 NOT disordered") is not supported, and no positive call is supported by measurement.
  **AGREE**, with one caveat: two independent predictors (metapredict, AlphaFold pLDDT) lean
  towards disorder rather than sitting neutral.
- **Not compared:** I did not read the challenger's numbers beyond line 40 of challenge-28.md, so
  I cannot compare them with mine figure by figure.

```swarm-replication
{"claim_id": 70, "my_value": "and2 FoldIndex +0.070 (full chain; +0.035 mature; ~40% of residues in negative 51-aa windows); metapredict 77% disordered; AF pLDDT mean 55.9", "agrees": true,
  "note": "FoldIndex arithmetic reproduces exactly but sits near zero and cannot separate and2 from the control, while metapredict and AlphaFold pLDDT (both predictions, no measurement) treat and1 and and2 alike and lean towards disorder, so the negative call is unsupported and no positive call is measured."}
```
