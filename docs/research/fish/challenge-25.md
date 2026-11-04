# Challenge 25: "ESMFold2 is by far the best kcnk5b model"

**Claim under review (the author's, not mine):** "ESMFold2 is by far the best kcnk5b model: mean
pLDDT 83.6, pTM 0.607, 90.0% of residues above 70, 0.9% below 50, with both selectivity filters at
96.5 and 96.3." Recorded evidence level: *simulated*. Source: Nebius esmfold2 op-2112f97ee3d11f6e.

**Verdict: WEAKENED.** Every number reproduces. On the part of the protein that can be checked
against an experimental structure, ESMFold2 really is the best of the three models, and by a wide
margin. But the whole-chain figures (90.0% >70, 0.9% <50, mean 83.6) also count a C-terminal tail
that ESMFold2 builds as an extended chain with no tertiary contacts. That geometry does not match
the tail's 76 pLDDT. The AlphaFold DB model of the same UniProt entry also disagrees with it, and so
does the tail's sequence composition. The headline figures should be quoted for residues 1–260
only.

Everything below is either *calculated* (by me, from model files) or *predicted* (a model's own
confidence). The only *observed* data here are the two cryo-EM structures, and they are of the
mouse ortholog, not zebrafish kcnk5b. No fish measurement was made or used.

---

## Inputs and their provenance

| input | where | read-level | identity check |
|---|---|---|---|
| `kcnk5b_esmfold2.cif` | `origin/swarm-architecture:results/fish-proteins/structures/` | full-text (parsed) | sha256 `89dee0f7…46b0` matches `structure.sha256` in `kcnk5b-confidence.json`; git blob `132c661f6d66e7e110bf5a1c07cab116f5e6ad2d` |
| `kcnk5b-confidence.json` | same | full-text | `plddt_mean 0.83631`, `ptm 0.60675`, `runtime_id esmfold2`, seed 1, 1 sample |
| `kcnk5b_boltz2.cif` | same | full-text (parsed) | sha256 `cb2219df…0616` |
| `Q6PFU3.fasta` | `origin/swarm-architecture:results/fish-proteins/` | full-text | 448 aa. The sequences of both CIFs are identical to it (checked residue by residue) |
| RCSB 6WLV, 6WM0 (TASK-2, mouse `Kcnk5`, cryo-EM in nanodisc, pH 6.5 / 8.5; 6WLV 3.45 Å) | files.rcsb.org | full-text (mmCIF parsed) | 6WLV sha256 `f16b3d3b…6fec68`, 6WM0 `dad9722f…6d96d`. Must-fail control: `0000.cif` returned HTTP 404 |
| AlphaFold DB AF-Q6PFU3-F1 (v6, "AlphaFold Monomer v2.0 pipeline") | alphafold.ebi.ac.uk/api/prediction/Q6PFU3 | **listing** (summary JSON only) | The `.cif`, `.pdb`, `.bcif` and `confidence_v6.json` all returned HTTP 403, so **no per-residue AFDB values were read.** Must-fail control: a malformed ID returned HTTP 400 |

The source docs (`docs/research/fish/proteins-results.md`, `proteins-findings.md` on
`origin/swarm-architecture`) were read in full-text for the kcnk5b sections.

---

## 1. Arithmetic, redone independently

I parsed the `_atom_site` loop by its column header, took the CA B-factor of each residue as its
pLDDT, and checked the scale (range 47.22–98.53, so it is 0–100). The script is my own; I did not
use the author's `extract.py`.

| quantity | claimed | recomputed (ESMFold2) |
|---|---|---|
| residues | 448 | 448 |
| mean pLDDT | 83.6 | **83.63** (json: 83.631) |
| pTM | 0.607 | 0.6067 (json only; it cannot be recomputed from the CIF) |
| % >70 | 90.0 | **90.0** |
| % <50 | 0.9 | **0.9** (4 residues; minimum 47.22) |
| TIGYG 98–102 mean | 96.5 | **96.5** |
| TVGFG 203–207 mean | 96.3 | **96.3** |
| longest run >70 | 87 aa (157–243) | **87 aa (157–243)** |
| residues 1–250 / 261–448 | 89.2 / 76.4 | **89.2 / 76.4** |

The same script on the Boltz2 file reproduces the author's 62.0 / 38.8% / 33.0% / 80.2 / 82.6 /
1–250 = 77.5 / 261–448 = 41.4. **The arithmetic is correct and I found no transcription error.**

## 2. The proxy: pLDDT is self-confidence, not accuracy

"Best model" is being judged by each model's confidence in itself. pLDDT values from different
architectures are not calibrated against each other. The quantity that actually matters is
agreement with an experimental structure. For the transmembrane core there is a usable reference:
the cryo-EM structures of mouse TASK-2 (6WLV, 6WM0), which resolve residues 5–260. Over the aligned
core the zebrafish and mouse sequences are 64.5% identical (my global alignment).

I superposed the CA atoms of each model's residues 1–275 onto chain A of each structure. I used my
own fixed-alignment TM-score search (Kabsch superposition with fragment seeds, d0 from the
reference length). **This approximates TM-score; it is not TM-align.**

Controls for that routine, with answers known in advance:
- Positive: 6WLV:A against 6WM0:B, the same protein at two pH values, gave **TM 0.963**.
- Must-fail: ESMFold2 with its register shifted by 40 residues gave **0.19**.
- Must-fail: random coordinates gave **0.065**.

| (calculated) vs 6WLV:A / 6WM0:A | ESMFold2 | Boltz2 + PDB70 MSA |
|---|---|---|
| TM-score (approx.) | **0.892 / 0.912** | 0.642 / 0.645 |
| CA RMSD, all aligned, one superposition | **2.70 / 2.23 Å** | 14.30 / 14.06 Å |
| fraction of CA within 4 Å after TM superposition | **0.91 / 0.94** | 0.59 / 0.60 |
| selectivity-filter loops (96–104, 201–209), local CA RMSD | **0.38 / 0.42 Å** | 0.64 / 0.48 Å |
| mean deviation where the model's pLDDT >90 | **1.07 / 1.08 Å** | 13.1 / 13.1 Å |

**For the core, the claim survives this check, and survives it better than the author showed.**
ESMFold2's high core confidence is borne out against an experimental ortholog structure. Boltz2's is
not: its residues with pLDDT >90 sit about 13 Å from the reference, so part of its core is placed
wrongly while confident. The 96.5 / 96.3 filter confidences also hold up, at 0.4 Å local RMSD.
OpenFold2 was not compared because its CIF is not on the branch.

Caveats on this check (my inference, not tested):
- The reference is a mouse ortholog, not zebrafish kcnk5b.
- The models are monomers, while the channel is a dimer.
- 6WLV and 6WM0 (released 2020) may be in ESMFold2's training data, so agreement may partly be
  recall rather than prediction.

## 3. The hidden assumption: that pLDDT means the same thing along the whole chain

The whole-chain figures assume that ESMFold2's tail confidence is as meaningful as its core
confidence. **No experimental structure covers residues 261–448**, since the TASK-2 constructs stop
being resolved at 260. So the tail can only be tested for internal coherence and against other
predictors. It fails all three tests.

**(a) Geometry vs confidence (calculated, from the ESMFold2 CIF):**

| region | pLDDT | helix-like (CA i/i+3, i/i+4) | extended | long-range CA contacts per residue (<8 Å, \|i−j\|≥12) | Rg |
|---|---|---|---|---|---|
| 1–260 | 88.9 | 0.82 | 0.20 | 0.8 | 24.3 Å |
| 261–330 | 76.9 | 0.56 | 0.24 | 0.1 | 21.6 Å |
| **331–448** | **76.1** | **0.06** | **0.93** | **0.0** | **58.9 Å** |

Residues 331–448 are 118 residues built as an almost fully extended chain with zero tertiary
contacts, spanning a radius of gyration of 59 Å. That is what a predictor produces for a region it
cannot place. Yet ESMFold2 scores it 76.1 on average, with 82% of it (97 of 118 residues) above 70. A confident structure needs
something to be confident about. **The tail pLDDT is not coherent with the tail coordinates**, so
this runtime's pLDDT is not calibrated across this region. Note that pLDDT is a local measure, so
an unpacked chain can in principle score high locally. But a chain that is 93% extended and has no
contacts has no local structure to score either.

**(b) An independent predictor disagrees (AlphaFold DB, read at listing level):** the summary for
AF-Q6PFU3-F1 gives global mean pLDDT **69.5**, with **33.9% very low (<50)**, 6.0% low, 24.8%
confident and 35.3% very high. So AF2 run with a full MSA puts **33.9%** of residues below 50,
where ESMFold2 puts **0.9%**. I did not average these; they disagree. I could not see which
residues the AFDB very-low fraction covers, because the per-residue files were refused with 403.
33.9% of 448 is about 152 residues, which would fit inside the 188-residue tail, but **that
localization is my inference and is unverified.**

**(c) Sequence (calculated):** an Uversky charge–hydropathy FoldIndex, computed by me over residues
261–448, is **−0.129** (predicted unfolded). Over 1–260 it is +0.379. The tail is 36% K/R/D/E,
against 14% in the core. This is a sequence heuristic, not a measurement.

The author's own proteins documents argue that Boltz2's low tail confidence was an artefact of the
MSA running out, and that ESMFold2's 76.4 removes the evidence for disorder. I agree with the
first half. The second half does not follow: ESMFold2's 76.4 sits on contactless extended
coordinates, and AF2 with a full MSA disagrees. The tail is **unresolved, not shown ordered**. The
author did hedge this in prose ("76.4 is moderate … not a measurement"), but the headline numbers
still count those residues as confident.

**Relaxing the assumption:** restricted to the checkable core (1–260), ESMFold2 has mean pLDDT
**88.9** and 97.7% of residues >70, and it is still clearly the best model. The whole-chain
"90.0% >70 / 0.9% <50" should not be read as "kcnk5b is 90% confidently modelled".

## 4. Is the evidence level honest?

Mostly. "Simulated" is the closest of the repo's three columns (proved / simulated / observed) for
a model's own output, and the author's documents explicitly say pLDDT is not accuracy. There are
two defects:

1. **"By far the best"** is a ranking made on self-confidence, a predicted proxy. It is not
   accuracy. I have now partly confirmed the ranking with a calculation against an observed
   structure, but only for residues 5–260. As written, the claim presents a confidence ranking as
   a quality ranking.
2. **"recomputed here … and corroborated by confidence.json"** is the same number from the same
   run read twice: the json mean and the B-factor mean are one output. That is a consistency
   check, not corroboration. It is n = 1 seed and 1 sample.

## 5. Counter-examples the author missed

- **AlphaFold DB AF-Q6PFU3-F1** (listing): mean 69.5, 33.9% <50. It is a published model of the
  same sequence and was not in the comparison. "By far the best kcnk5b model" was judged only
  against two handicapped lanes: OpenFold2 with a dummy single-sequence MSA, and Boltz2 with a
  72-sequence PDB70 MSA that, by the author's own count, has depth 0 beyond residue 326. I did not
  compute AFDB's core accuracy, because its coordinates were refused, so I cannot say whether
  ESMFold2 also beats AF2 on the core.
- **TASK-2 cryo-EM 6WLV / 6WM0** were in the author's MSA hit list but were not used as an accuracy
  reference. Used as one, they *support* ESMFold2 on the core (section 2).

Negative-search scope: I looked for a kcnk5b ESMFold2 artefact on every remote branch of this repo
by filename (`esmfold`, `plddt`, `.cif`, `confidence.json`). Only `origin/swarm-architecture` holds
one. I did not search for literature on the disorder of the K2P C-terminus and cite none.

---

## Corrected statement

> On the transmembrane core (residues 1–260), the only region with an experimental reference,
> ESMFold2 is the best of the three models in this repo. It has mean pLDDT 88.9 (predicted). Its
> calculated approximate TM-score is 0.89 / 0.91 against cryo-EM TASK-2 6WLV / 6WM0, a mouse
> ortholog at 64.5% identity, versus 0.64 for Boltz2. Its selectivity filters reproduce the
> experimental geometry to 0.4 Å. The whole-chain figures (mean 83.6, 90.0% >70, 0.9% <50) are
> correctly computed but overstate confidence. They count residues 331–448, which ESMFold2 builds
> as a contactless extended chain at pLDDT ~76. The AlphaFold DB model of the same entry
> (AF-Q6PFU3-F1, summary only) puts 33.9% of residues below 50. The tail's structure is unknown.

```swarm-challenge
{"claim_id": 25, "outcome": "weakened", "reason": "All arithmetic reproduces and ESMFold2 is genuinely best on the cryo-EM-checkable core (approx. TM 0.89-0.91 vs 6WLV/6WM0, Boltz2 0.64), but the whole-chain 90.0%>70 / 0.9%<50 figures include residues 331-448 that ESMFold2 builds as a contactless extended chain at pLDDT ~76, contradicted by AlphaFold DB AF-Q6PFU3-F1 (33.9% <50) and a negative FoldIndex.", "corrected_value": "core residues 1-260: mean pLDDT 88.9 (predicted), approx. TM-score 0.89/0.91 vs 6WLV/6WM0 (calculated); whole-chain 90.0% >70 not supported for residues 331-448"}
```
