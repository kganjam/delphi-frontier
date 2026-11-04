# Challenge 20 — ProteinMPNN recovery on Boltz-2 vs OpenFold2 kcnk5b backbones

**Claim under review (author's words):** "ProteinMPNN sequence recovery is 0.292–0.324 on the Boltz2
core backbone (pLDDT 77.5) against 0.127–0.152 on the poor OpenFold2 backbone, so the
near-poly-leucine output was a backbone artifact and not a property of kcnk5b."
Recorded evidence level: `simulated`. Recorded value: 0.32 sequence recovery.
Source: Nebius `infer_proteinmpnn_native`, second run as its own control.

**Verdict: WEAKENED.** The direction is probably right, but the low arm of the contrast is arithmetically
uninformative, the high arm is not in the healthy range, the comparison has no control whose answer was
known in advance, and the one such control is cheap and available. Details below. Nothing here shows the
near-poly-leucine output *is* a property of kcnk5b; I am saying the stated evidence does not decide it.

## 0. What I could and could not read

- **Could not access:** no run artifact for this claim exists in this repository. `grep -ril` for
  `proteinmpnn`, `kcnk5b`, `boltz`, `openfold`, `nebius` over the whole working tree (all files, excluding
  `.git/`) returns only `findings/proteingym-spearman-dms-level.csv`,
  `findings/gemini-triage-267-problems.json`, `findings/README-no-gpu-problem.md`,
  `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` and
  `preregistrations/2026-10-31-kcne1-binding-ddg.md` — none of which contains a ProteinMPNN run, a
  designed sequence, a per-residue recovery table, or a backbone file. **Scope of that negative search:**
  one `git`-tracked working tree at commit `3272d3e`, all file types, no other branches searched beyond
  the two that exist (`claude/proteinmpnn-kcnk5b-challenge-t43pzj`, `work/frontier-foundation`).
  So every check below is against the *stated numbers*, not against the run.
- **Full record, read directly:** UniProt `Q6PFU3` (`Q6PFU3_DANRE`, `kcnk5b`, *Danio rerio*, 448 aa,
  **unreviewed/TrEMBL**) and its FASTA, fetched from `rest.uniprot.org`. A second unreviewed entry,
  `A0A8M1PBI1`, is also 448 aa. Composition numbers below are **computed by me** from `Q6PFU3`.
- **Search-summary:** Dauparas et al., *Science* 378(6615):49–56 (2022) — native-backbone sequence
  recovery **52.4%** for ProteinMPNN vs **32.9%** for Rosetta on 402 monomer backbones; a 690-monomer
  evaluation gives median ~52%. I did not open the full text; read-level is search-summary.
- **Search-summary:** PDB **6WLV** (3.45 Å) and **6WM0** (3.52 Å), *Mus musculus* TASK-2 / Kcnk5 in
  MSP1D1 lipid nanodisc, pH 6.5 and 8.5; Li, Rietmeijer & Brohawn, *Nature* 586:457–462 (2020),
  PMID 32999458. Read from PDBj/RCSB summary pages via search, not from the coordinate files.
- **Search-summary:** Perathoner et al., *PLoS Genetics* (2014), `alf` = gain-of-function point mutations
  in `kcnk5b`, increased K⁺ conductance, hyperpolarisation, acts locally in fin mesenchyme.
- **Unknown:** ProteinMPNN sampling temperature, model weights (full-PDB vs `--use_soluble_model`),
  residue range scored, chain count, random seed, and the reference sequence used as "native" — for
  *both* runs. These are the variables the whole claim turns on (§3).

## 1. Arithmetic, redone from the stated inputs only

| quantity | my value |
|---|---|
| high arm midpoint | (0.292 + 0.324)/2 = **0.308**, width 0.032 |
| low arm midpoint | (0.127 + 0.152)/2 = **0.1395**, width 0.025 |
| ratio of midpoints | 0.308 / 0.1395 = **2.21×** |
| ratio of minima / of maxima | 0.292/0.127 = 2.30× ; 0.324/0.152 = 2.13× |
| high arm as fraction of published native-backbone 0.524 | **0.588** (absolute shortfall 0.216) |

The ~2.2× gap is real as stated. Two arithmetic defects:

**(a) The recorded value 0.32 is the top of the range, not its centre.** The midpoint is 0.308. Reporting
0.32 for a 0.292–0.324 interval reports the best sample as the result. One significant figure hides this;
the ledger should carry `0.308 (0.292–0.324)`.

**(b) n = 1 per arm.** The stated ±ranges are spreads over ProteinMPNN sampling (seeds/temperature) on a
*single* backbone each. They are not a between-backbone variance estimate, so they cannot support an
inference whose unit of analysis is the backbone. Two points, one per arm, with the within-arm spread
substituted for the between-arm error model.

## 2. The proxy — and it is load-bearing, on both ends

**At the output end.** Sequence recovery stands in for "the design is not degenerate". The quantity that
matters is stated in the claim itself: *near-poly-leucine*. The direct measurements are per-position
composition entropy, the single-most-frequent-residue fraction, and (for design quality proper) self-
consistency — refold the designed sequence and report TM-score/RMSD to the input backbone plus the
refold's own pLDDT. None of those is reported. Recovery is the weakest available read on degeneracy,
because of §2.1.

**2.1 The low arm is almost exactly the all-leucine baseline, so it measures composition, not backbone
quality.** Computed by me from `Q6PFU3`:

| window | leucine fraction |
|---|---|
| 1–448 (full length) | 0.0960 |
| 1–200 | 0.1250 |
| **1–250 (TM/pore core)** | **0.1280** |
| 1–280 | 0.1214 |
| 20–250 / 30–260 | 0.1299 |
| 40–290 | 0.1195 |

A sequence that is **all leucine** scores 0.113–0.130 recovery against any plausible core window of
kcnk5b, with no information content whatsoever. The reported low arm is 0.127–0.152: its midpoint
0.1395 sits **1.2 percentage points — about 3 residues in 250 — above** the all-leucine baseline for
1–250, and its top (0.152) about 2.4 points (~6 residues) above it. *My inference:* the low arm is
reproduced by "the output was near-poly-leucine" alone, with the backbone never entering the
calculation. It therefore cannot be evidence about the backbone. The author's own description of the
output already predicts that number.

Note the direction of the composition effect: kcnk5b's core is **12.8% leucine** and 48% LVIFAMW, well
above a typical PDB average, so a degenerate hydrophobic output is *flattered* on this target rather
than penalised. The low arm is even less informative than it looks.

**At the backbone end.** pLDDT 77.5 is Boltz-2's own confidence, not backbone accuracy, and ProteinMPNN
reads only N/CA/C/O geometry plus a virtual CB — so the relevant quantity is *local backbone geometry
accuracy*, for which a global confidence score is a second-order proxy. The right measurement exists
here and was not taken: superpose the Boltz-2 core on the experimental K2P coordinates (**6WLV**/**6WM0**,
mouse TASK-2 = Kcnk5, same gene family as the target) and report TM-score/GDT. "pLDDT 77.5" vs "poor"
is a confidence label against an adjective; TM-score against 6WLV is a number against a crystal.

## 3. The hidden assumption, relaxed

**Assumption:** between the two runs, the only thing that differed was backbone quality.

The claim's own wording undermines this: the good arm is on the **"Boltz2 *core* backbone"**. "Core"
means a truncated region. kcnk5b is 448 aa with a long C-terminal tail past the pore domain
(~residue 250–280 onward), which no structure predictor models meaningfully. If the OpenFold2 run scored
**full-length** and the Boltz-2 run scored **core only**, the entire 2.2× contrast is a denominator
choice: recovery over a folded TM core vs recovery over core-plus-disordered-tail, where the tail
contributes near-baseline hits. Relaxing the assumption this one way reproduces the result with backbone
quality held constant. Nothing in the record excludes it, because the residue ranges are unknown (§0).

Three further uncontrolled variables, any one of which produces low-complexity hydrophobic output on its
own:

1. **Sampling temperature.** Low temperature plus an under-packed backbone is the standard route to
   low-complexity output. Unknown for both runs.
2. **Model weights.** ProteinMPNN ships a full-PDB model and a soluble-only model. Which was used is
   unknown; for a membrane protein the choice changes the hydrophobic/polar prior directly.
3. **Oligomeric state.** K2P channels are obligate **dimers** with a domain-swapped, two-pore-per-subunit
   architecture; the conduction pathway is built from both subunits. Designing a single chain in isolation
   presents the entire inter-subunit interface to ProteinMPNN as solvent, which systematically
   mis-assigns exactly the residues the native keeps hydrophobic. Whether either run included the second
   chain is unknown, and 6WLV/6WM0 are the deposited dimers that make the correct run possible.

## 4. Is the evidence level honest?

`simulated` is defensible for the recovery numbers themselves — they are neural-network inference output,
not observation — and the repository's own column discipline (`CONTRIBUTING-VERIFICATION.md` §6) is
satisfied on that narrow point. Two defects remain:

- **The conclusion is an inference carrying the measurement's level.** "0.292–0.324 vs 0.127–0.152" is
  simulated. "*Therefore* the near-poly-leucine output was a backbone artifact and not a property of
  kcnk5b" is an inference from two uncontrolled runs, and the claim ships both at one level in one
  sentence. Under §2.1 the premise does not reach the conclusion at all.
- **"Second run as its own control" is not a control.** It is a self-comparison between two runs that
  differ in unknown ways. The repository's rule 8 is explicit: *"beside every search, scan or query, run
  one case whose answer you already know, in both directions."* Here that control exists and is cheap:
  **run `infer_proteinmpnn_native` on 6WLV (or 6WM0) chain A+B with the deposited mouse TASK-2 sequence
  as native.** Expected ~0.45–0.52 if the pipeline is healthy, per the 52.4% native-backbone figure. A
  must-fail direction is equally available: score the same designed sequence against a shuffled native,
  which must collapse to ~0.05–0.10.

## 5. Regime and counter-example the author missed

**Regime: membrane proteins.** ProteinMPNN is trained on PDB structures with no lipid environment and no
membrane term. Its recovery on transmembrane proteins is not the 52.4% headline, and a hydrophobic-shifted,
lower-entropy output in the TM span is the expected failure mode of the method on this class of target —
i.e. *partly a property of the target class*, which is the possibility the claim rules out. I did not find
a published TM-specific recovery figure for ProteinMPNN in one English-language web search (two queries,
search-summary depth, no full texts opened): **absence of evidence at that depth, not evidence of
absence.** This is exactly what the 6WLV control decides, and it is why the control matters more than
another sampling run: if ProteinMPNN reaches ~0.50 on an experimental K2P dimer, then 0.308 on Boltz-2 is
backbone-limited and the claim's direction is vindicated with the right number attached; if it reaches
only ~0.30, then 0.308 is the method's ceiling on this fold and "backbone artifact" is wrong.

**The high arm is not in the healthy range.** 0.308 is 0.588 of the published native-backbone 52.4%, and
is below the 32.9% that *Rosetta* fixed-backbone design reached on native monomers. *My inference:* the
Boltz-2 core backbone at pLDDT 77.5 is still a degraded-backbone regime, not a recovered one. The honest
reading of the pair is "both backbones are poor, one much less so" — not "the artifact was removed".

**Counter-example to the framing, not the number.** `kcnk5b` reaches this project through Perathoner et al.
(2014): `alf` is a **gain-of-function point mutant** with increased K⁺ conductance and hyperpolarisation.
Neither sequence recovery nor foldability is the quantity that bears on that phenotype. Whatever this run
settles, it is three proxies away (recovery → degeneracy → design quality → mutational effect on
conductance) from the question kcnk5b was selected for. That is a scoping observation about the claim's
usefulness, not a refutation of its arithmetic.

## 6. What would make the claim stand

1. Publish both runs' residue ranges, chain sets, temperature, seed, model weights and native reference
   accession. If the ranges differ, the contrast is withdrawn, not corrected.
2. Report the single-most-frequent-residue fraction and per-position entropy for both outputs. That
   measures the near-poly-leucine phenomenon directly instead of through recovery.
3. Run the 6WLV/6WM0 positive control and the shuffled-native must-fail control.
4. Report TM-score of the Boltz-2 core against 6WLV, replacing "pLDDT 77.5 vs poor".
5. Report self-consistency (refold the design, TM-score + pLDDT vs input) for the Boltz-2 designs.

Steps 1–2 cost nothing and are re-reads of artifacts that should already exist.

## Sources

- [UniProt Q6PFU3 (kcnk5b, D. rerio)](https://rest.uniprot.org/uniprotkb/Q6PFU3.fasta) — full record, composition computed here
- [Dauparas et al., ProteinMPNN (Science 2022 / bioRxiv)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9997061/) — search-summary
- [PDB 6WLV, mouse TASK-2 in nanodisc](https://pdbj.org/mine/summary/6WLV) — search-summary
- [PDB 6WM0, mouse TASK-2 pH 8.5](https://rcsb.org/structure/6WM0) — search-summary
- [Perathoner et al. 2014, kcnk5b / alf (ZFIN record)](https://www.zfin.org/ZDB-PUB-140321-22) — search-summary

```swarm-challenge
{"claim_id": 20, "outcome": "weakened", "reason": "The 2.2x ratio is arithmetically correct but the low arm (0.127-0.152) is reproduced by the all-leucine baseline against kcnk5b's own core composition (0.128, computed from UniProt Q6PFU3) and so carries no information about the backbone, while the high arm (midpoint 0.308, not the recorded 0.32) is only 0.588 of ProteinMPNN's published 0.524 native-backbone recovery and below Rosetta's 0.329 - consistent with 'both backbones poor' rather than 'artifact removed' - with no positive control on the available experimental K2P backbone 6WLV and with residue range, temperature, model weights and chain count unknown for both runs.", "corrected_value": "0.308 mean sequence recovery (0.292-0.324) on the Boltz-2 core backbone, against an all-leucine baseline of 0.128 on kcnk5b residues 1-250 and a published native-backbone reference of 0.524; the 0.127-0.152 arm is uninformative, not a backbone measurement"}
```
