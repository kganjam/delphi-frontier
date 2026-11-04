# Challenge 28 — adversarial review

**Claim under review (claim_id 28), verbatim:**

> "and2 is NOT supported as intrinsically disordered: FoldIndex +0.070 (positive) and a
> disordered-window fraction of 40.0% against a folded control at 38.4%. and1 IS (-0.056).
> 'No fold predicted' and 'disordered' are different claims"

Recorded evidence level: `derived`. Recorded value: 0.07 FoldIndex.
Recorded source: sequence analysis by the running agent, kcnk5b +0.166 as positive control.

**Verdict: REFUTED** — for the operative proposition only. Part of the author's analysis survives
and is credited explicitly in §7.

Everything below is **computed or predicted, not observed.** There is no experimental structural
measurement of And1 or And2 in either the author's evidence or mine (§6). The author's claim is a
prediction and my rebuttal is a prediction; the dispute is about which predictions can carry a
negative conclusion, not about measured structure.

---

## 1. Arithmetic, redone independently

I re-implemented FoldIndex from the published formula (Prilusky et al. 2005, *Bioinformatics*
21:3435), without reading the author's code or intermediate values:

```
FoldIndex = 2.785·⟨H⟩ − |⟨R⟩| − 1.151
  ⟨H⟩ = mean Kyte–Doolittle hydropathy, rescaled to [0,1] as (KD + 4.5)/9
  ⟨R⟩ = net charge per residue = (K + R − D − E)/N
```

Implementation committed alongside this file as `foldindex_recheck.py`.

The claim did not record which accessions it used. I resolved the genes against UniProt myself
(read-level: full record, UniProt REST):

| gene | accession | length | note |
|---|---|---|---|
| and1 | `E7F5V5` | 570 | Actinodin1 precursor, unreviewed; signal peptide 1–26 |
| and2 | `A9JRX1` | 508 | unreviewed; signal peptide 1–23 (identical-length duplicate entry `A0ACM8QEN9` also exists) |
| kcnk5b | `Q6PFU3` | 448 | unreviewed; 4 annotated helical TM segments (7–26, 116–137, 158–185, 229–250) |

**Result on the full UniProt precursors:**

| protein | ⟨H⟩ | ⟨R⟩ | FoldIndex (mine) | claim | match |
|---|---|---|---|---|---|
| and1 | 0.40187 | −0.02456 | **−0.0563** | −0.056 | ✅ |
| and2 | 0.44337 | −0.01378 | **+0.0700** | +0.070 | ✅ |
| kcnk5b | 0.48160 | +0.02455 | **+0.1657** | +0.166 | ✅ |

**All three FoldIndex values reproduce exactly.** The author's arithmetic is correct, and the
agreement also identifies the undocumented protocol: whole-sequence FoldIndex on the *full
precursors* of these three accessions. That is a real result and I credit it.

**The two window percentages do not reproduce.** My sliding-window implementation at the
conventional w=51 gives:

| protein | negative-window-centre fraction | residues covered by a negative window |
|---|---|---|
| and1 | 66.5% | 85.4% |
| and2 | **38.9%** | 58.7% |
| kcnk5b | **36.9%** | 60.7% |

The claim states 40.0% (and2) and 38.4% (control). I grid-searched 564 protocol variants —
window 10–150 residues, two counting conventions (negative window *centres* and residues
*covered* by a negative window), with and without the annotated signal peptide — and **0 of them
return 40.0% ± 0.06 for and2.** The figures land in the right neighbourhood but are not
regenerable from the stated accessions, and the identity of the "folded control at 38.4%" is not
recorded anywhere in the claim; I cannot confirm it was kcnk5b. Scope of this negative: my own
re-implementation only, w=10–150, two metrics, Kyte–Doolittle scale, ± signal peptide; I did not
query the original FoldIndex web server, which may window or pad differently.

## 2. A proxy is standing in for the quantity that matters — and here it degenerates to one variable

FoldIndex is algebraically the Uversky charge–hydropathy (C-H) boundary rearranged. It is a
**whole-protein** order/disorder classifier. Huang, Oldfield et al., "Improving protein
order-disorder classification using charge-hydropathy plots," *BMC Bioinformatics* 2014
(PMC4304195; read-level: **full text**, characters 0–100,000 of 121,798; note erratum PMC4520057
replaced a mis-printed Figure 1) benchmarks exactly this method and calls it "a straightforward,
simple, fast, yet effective whole protein disorder versus order predictor." Its reported
balanced two-state accuracies, on "109 disordered sequences" described as *fully* disordered
versus "563 fully structured protein sequences," are:

- **Kyte–Doolittle: 79%** ← the scale FoldIndex uses, and the scale behind the claim
- Guy: 84%
- IDP-Hydropathy: 90%

So the instrument the claim leans on misclassifies roughly one protein in five, and the better
scales were not used. A single protein sitting 0.07 from that boundary cannot carry a negative
conclusion at that error rate.

Worse, **the charge term is inert across all three proteins**, so the comparison is not really
charge-and-hydropathy at all. Decomposing the mature chains:

| protein | FCR (fraction charged, KRDE) | \|NCPR\| | charge term | hydropathy term | FoldIndex |
|---|---|---|---|---|---|
| and1 | 25.6% | 0.0276 | −0.0276 | −0.0694 | −0.0969 |
| and2 | 23.9% | 0.0165 | −0.0165 | +0.0517 | +0.0353 |
| kcnk5b | 23.4% | 0.0246 | −0.0246 | +0.1902 | +0.1657 |

All three carry ~a quarter charged residues, but their charges are near-balanced, so |⟨R⟩| ≈ 0.02
and the charge term contributes −0.017 to −0.028 — **essentially the same value for all three.**
Every bit of the discrimination among and1, and2 and kcnk5b comes from mean Kyte–Doolittle
hydropathy alone. The claim is therefore a mean-hydrophobicity ranking wearing a two-parameter
name, and mean hydropathy is exactly the quantity contaminated by the two confounds in §3 and §5.

The quantity that actually matters is **residue-level disorder propensity along a mosaic chain.**
Better instruments, and what I could and could not run: AlphaFold2 pLDDT (run, §5); IUPred2A and
metapredict (**not run** — `pip install metapredict` was attempted in this container and the
module was unavailable afterwards; no third predictor was obtained); experiment (none exists, §6).

## 3. The hidden assumption, relaxed

The result is carried by the assumption that **the C-H plot's whole-protein decision boundary,
calibrated on entirely-disordered versus entirely-structured proteins, transfers to a mosaic
secreted protein evaluated as its precursor.** Two relaxations:

**(a) Which chain?** And1 and And2 are secreted; the signal peptide is cleaved and absent from the
mature protein, so the mature chain is the biologically relevant species. Using UniProt's own
annotated cleavage sites:

| protein | precursor | mature | Δ |
|---|---|---|---|
| and1 | −0.0563 | −0.0969 | −0.0406 |
| and2 | **+0.0700** | **+0.0353** | −0.0348 |
| kcnk5b | +0.1657 | +0.1657 | 0 |

Removing a hydrophobic signal peptide that the mature protein does not contain **halves and2's
margin.** The sign does not flip, but the headline number +0.070 is inflated by ~2× relative to
the chain that exists in the extracellular matrix. (Adding His to the positive set, an alternative
convention, moves and2 by +0.006 — immaterial.)

**(b) How stable is the sign?** A 51-residue block bootstrap (4,000 resamples) over each chain:

| protein / chain | point | 95% interval | resamples called disordered |
|---|---|---|---|
| and1 precursor | −0.0563 | [−0.1928, +0.0264] | 91.8% |
| and1 mature | −0.0969 | [−0.2105, +0.0176] | 94.5% |
| and2 precursor | +0.0700 | [−0.0499, +0.1535] | 15.9% |
| and2 mature | +0.0353 | [−0.0520, +0.1515] | 16.4% |

**and2's interval spans zero on both chains.** This bootstrap measures compositional
heterogeneity within the protein — the right notion of uncertainty for a mosaic chain, where
"the" composition is not a single well-defined quantity — and it is *not* model error; the 21%
misclassification rate from §2 sits on top of it. A classification reported as "+0.070
(positive)" with no interval is a determinate verdict drawn from a quantity whose own interval
crosses the boundary.

## 4. Is the evidence level honest?

**Largely yes, and this is not where the claim fails.** `derived` is the correct level for a
FoldIndex computation, and the claim names FoldIndex explicitly rather than implying measurement.
Nothing is presented as an observation. The closing sentence — *"'No fold predicted' and
'disordered' are different claims"* — is correct and is the most valuable thing in the record.

Three record defects short of a level violation:

1. **Not reproducible as recorded.** No accession, isoform, chain (precursor vs mature), window
   size, or counting convention. I had to recover the accessions and reverse-engineer the chain
   from the fact that the values matched. A `derived` value should ship its inputs.
2. **An unidentified control.** "a folded control at 38.4%" names no protein. The separately
   recorded kcnk5b is described as a *positive control for FoldIndex sign*, which is not the same
   object as a window-fraction baseline, and my kcnk5b window fraction is 36.9%, not 38.4%.
3. **Precision overstated.** Three significant figures (40.0%, 38.4%, a 1.6 pp gap) from a
   classifier with 79% balanced accuracy and n=1 control. With one control protein there is no
   distribution, so a 1.6 pp difference cannot support or refute anything.

## 5. The counter-example is the author's own control

I looked for a regime where a positive whole-sequence FoldIndex coexists with a large intrinsically
disordered region. I did not have to leave the claim's own dataset.

**kcnk5b, the "folded control," is itself ~43% disordered by the claim's own metric.** Splitting it
at the end of the channel domains:

| segment | length | FoldIndex | ⟨H⟩ |
|---|---|---|---|
| TM / channel core, 1–255 | 255 | **+0.4054** | 0.560 |
| cytoplasmic C-tail, 256–448 | 193 | **−0.1614** | 0.378 |

AlphaFold DB agrees, and more strongly. Read-level: **full record** — AFDB v6 API summary plus the
per-residue `confidence_v6.json` for each accession (AlphaFold Monomer v2.0, model dated
2025-08-01). Using the standard pLDDT<50 ≈ disorder convention:

| protein | mean pLDDT | <50 | <70 | >90 | residues in ≥30-aa pLDDT<50 segments | longest such segment |
|---|---|---|---|---|---|---|
| and1 | 57.07 | 41.6% | 72.5% | 4.9% | 23.0% | 67 aa (473–539) |
| and2 | 55.90 | **45.9%** | 73.2% | **0.4%** | 8.9% | 45 aa (158–202) |
| kcnk5b | 69.50 | 33.9% | 40.0% | 35.0% | 26.8% | **120 aa (329–448)** |

So kcnk5b scores +0.166 overall while containing the **largest predicted IDR of the three
proteins** — a 120-residue cytoplasmic tail. This is a within-dataset demonstration that a
positive whole-sequence FoldIndex is compatible with a long IDR, which is precisely the inference
the claim forbids itself from making in one direction and then makes in the other.

It also explains the 40.0%-vs-38.4% near-tie mechanically: **the baseline is contaminated with a
real IDR.** A reference whose own disordered-window fraction is inflated by a 120-residue
disordered tail will sit next to almost any test protein, so that comparison has no discriminating
power by construction. The control is invalid twice over — its hydrophobicity is inflated by four
transmembrane helices (core ⟨H⟩ = 0.560) and its window fraction is inflated by its own IDR — and a
polytopic membrane channel is in any case the wrong reference class for a secreted ECM protein.

**And the orthogonal predictor reverses the claim's ordering on the statistic the claim itself
chose** (fraction of sequence predicted disordered): and2 45.9% > and1 41.6%. and2 also has
**0.4% of residues above pLDDT 90** — essentially no well-packed core anywhere in the protein —
against kcnk5b's 35.0%.

## 6. Disagreement I am preserving rather than averaging away

The two predictors do **not** agree on everything, and the honest statement is narrower than
"and2 is disordered":

- By **fraction** of very-low-confidence residues, and2 is *more* disordered than and1
  (45.9% vs 41.6%) — opposite to the claim.
- By **contiguous segment** structure, and1 looks *more* IDR-like than and2: 23.0% of and1's
  residues sit in ≥30-aa pLDDT<50 stretches across three segments (longest 67 aa), versus 8.9% of
  and2's in a single 45-aa segment. and2's low confidence is more diffuse.
- The FoldIndex *ordering* and1 < and2 is itself robust (§7).

What both predictors agree on, and what defeats the claim: **neither And1 nor And2 has a
predicted folded core** (and1 4.9%, and2 0.4% of residues >pLDDT 90, against 35.0% for a real
channel), so there is no basis for placing and2 on the "folded" side of a binary with and1.
Which of the two is "more disordered" depends on which statistic you pick — which is itself a
reason not to publish a binary IS/IS-NOT split between them.

**No experimental data exists on either protein**, and both sides of this dispute are predictions:

- No PDB entry for `E7F5V5` or `A9JRX1` (read-level: full UniProt cross-reference record).
- No CD, NMR or SAXS characterisation of And1/And2 found. Scope: one English-language web search
  for biophysical characterisation, plus a targeted search of the actinodin literature; returned
  Zhang et al. 2010 *Nature* 466 (nature09137, read-level: **abstract / search-summary**), two
  University of Ottawa theses and a ZFIN record (read-level: **listing**). Hits for "AND-1" in the
  PDB are human WD-repeat/HMG-box protein 1 — a name collision, not this protein.
- Zhang et al. describe And1/And2 as structural components of actinotrichial elastoidin alongside
  collagen, present in teleosts and elephant shark and absent in tetrapods. **I found no
  published statement that actinodins are intrinsically disordered** (scope as above) — so the
  claim is not contradicting a published characterisation, and a reader should not infer from this
  review that one exists.

**An attack line I tested and discarded.** I expected actinodins to be glycine-rich collagen-like
sequences, which would make them a classic FoldIndex false-positive regime (poly-glycine scores
+0.118 by this formula). It is not so: G+P is 17.2% (and1) and 16.3% (and2), and the dominant
residues are P 11.8%, A 9.8–10.6%, with Y/L/D/E/S following. Neither protein is glycine-rich.
Recording this because it would have been a plausible-sounding manufactured fault.

I also could not confirm the numeric FCR boundaries of the Das & Pappu 2013 *PNAS* diagram of
states (read-level: **search-summary**, boundaries not found), so I have **not** used that
framework to classify and2, and the FCR figures in §2 stand only as composition arithmetic.

## 7. What survives

Stated plainly, because a review that credits nothing is not a review:

- **The three FoldIndex values are arithmetically correct** (verified independently, exact match).
- **The and1-versus-and2 ordering is robust.** Paired block bootstrap of the difference
  (precursors): point −0.1264, 95% interval [−0.2835, +0.0194], and 96.0% of resamples preserve
  the claimed sign. and1 genuinely scores more FoldIndex-negative than and2, and that is not
  noise. The error is in converting a robust *ranking* into a binary *classification* across a
  boundary that neither protein is far from.
- **The epistemic caveat is correct and worth keeping:** "no fold predicted" and "disordered" are
  indeed different claims. The claim then commits the mirror-image error — treating "a fold is not
  excluded" as "disorder is not supported" — using a method whose published scope is whole-protein
  classification of fully-disordered versus fully-structured sequences.

## 8. Why REFUTED rather than weakened

Both supporting prongs fail and the conclusion is contradicted:

1. The window comparison (40.0% vs 38.4%) is **not reproducible** under 564 protocol variants, its
   control is **unidentified**, and the kcnk5b candidate baseline is **invalid** — ~43% of it is
   disordered by the claim's own metric and it contains the largest predicted IDR in the set.
2. The FoldIndex sign rests on **+0.070 falling to +0.035 on the mature secreted chain**, with a
   bootstrap interval spanning zero, from a classifier with **79% balanced accuracy** on the
   Kyte–Doolittle scale, applied **outside its calibration domain** (mosaic rather than fully
   disordered/fully structured), and in which the charge term is **inert**, leaving a bare
   mean-hydropathy comparison against a 4-TM membrane protein.
3. An orthogonal predictor **supports** and2 lacking folded structure (45.9% of residues pLDDT<50;
   0.4% above 90), so the assertion that and2 "is NOT supported as intrinsically disordered" is
   false as a statement about the evidence base — support exists; the chosen method cannot see it.

This refutes the claim's negative conclusion. It does **not** establish that And2 is intrinsically
disordered: that would require experiment, and none exists (§6). The correct record is *unresolved
by prediction, with no folded core predicted for either protein*, not a binary split between them.

**Corrected value:** and2 FoldIndex **+0.035** (dimensionless; mature chain, `A9JRX1` signal
peptide 1–23 removed), 95% block-bootstrap interval **[−0.052, +0.152]** — spans the decision
boundary. Orthogonal: AlphaFold2 pLDDT<50 = **45.9%** of residues (and1 41.6%), pLDDT>90 =
**0.4%**.

### Recommended replacement for the claim record

> and2 whole-chain FoldIndex is +0.035 for the mature secreted chain (+0.070 for the precursor),
> 95% block-bootstrap interval [−0.052, +0.152], i.e. not resolved against the decision boundary.
> FoldIndex is the Uversky charge–hydropathy boundary, a whole-protein classifier with 79% balanced
> accuracy on the Kyte–Doolittle scale, calibrated on fully disordered vs fully structured proteins;
> here its charge term is inert (|NCPR| ≈ 0.017) so it reduces to mean hydropathy. It cannot
> support a negative disorder call for a mosaic protein. AlphaFold2 predicts no folded core for
> either actinodin (pLDDT>90: and1 4.9%, and2 0.4%; vs 35.0% for kcnk5b) with and2 having the
> larger very-low-confidence fraction (45.9% vs 41.6%) but shorter contiguous low-confidence
> stretches. kcnk5b is not a usable folded control: its C-terminal tail scores −0.161 and is a
> 120-residue predicted IDR. All values derived; no experimental structural data exists for And1 or
> And2 (no PDB entry; no CD/NMR/SAXS located).

---

### Methods and read-levels

| Source | Read-level |
|---|---|
| UniProt REST records `E7F5V5`, `A9JRX1`, `Q6PFU3`, `A0ACM8QEN9` (sequence, signal peptide, TM, PDB xrefs) | full record |
| AlphaFold DB v6 API summaries + per-residue `confidence_v6.json`, all three accessions | full record |
| Huang, Oldfield et al., *BMC Bioinformatics* 2014, PMC4304195 | full text (chars 0–100,000 of 121,798) |
| Erratum PMC4520057 (mis-printed Figure 1) | listing |
| Prilusky et al. 2005, *Bioinformatics* 21:3435 (FoldIndex) | search-summary — formula confirmed; a reported ±0.005 "ambiguous" band around the boundary is **unverified**, and if real it concerns numerical ties, not the 21% model error rate |
| Zhang et al. 2010, *Nature* 466, nature09137 (actinodin discovery) | abstract / search-summary |
| U. Ottawa and1/and2 mutant theses; ZFIN ZDB-PUB-100625-29 | listing |
| Das & Pappu 2013, *PNAS* diagram-of-states FCR boundaries | search-summary — **could not confirm; not used** |
| metapredict / IUPred2A second-opinion predictor | **could-not-access** — `pip install metapredict` attempted in-container, module unavailable afterwards |

FoldIndex re-implementation, window grid search, charge decomposition and block bootstraps were
written for this review from the published formula; `foldindex_recheck.py` is committed beside this
file. Bootstrap seeds 7/11/23; a 2,000-resample run of and2-mature at a different seed gave
+0.0353, [−0.0517, +0.1558], 17.0% below zero, consistent with the 4,000-resample figures reported.

```swarm-challenge
{"claim_id": 28, "outcome": "refuted", "reason": "The FoldIndex values reproduce exactly and the and1<and2 ordering is robust, but the negative call for and2 collapses: its margin falls to +0.035 on the mature secreted chain with a bootstrap interval spanning zero, the charge term is inert so the test reduces to mean hydropathy against a 4-TM membrane protein whose own C-terminal tail scores -0.161 and is the largest predicted IDR in the set, the 40.0%/38.4% window figures are unreproducible under 564 protocol variants against an unidentified control, and AlphaFold2 puts and2's pLDDT<50 fraction above and1's (45.9% vs 41.6%) with only 0.4% of residues above pLDDT 90.", "corrected_value": "and2 FoldIndex +0.035 (dimensionless, mature chain A9JRX1 after removing signal peptide 1-23), 95% block-bootstrap CI [-0.052, +0.152], spanning the decision boundary; orthogonal AlphaFold2 pLDDT<50 = 45.9% of residues vs and1 41.6%, pLDDT>90 = 0.4%"}
```
