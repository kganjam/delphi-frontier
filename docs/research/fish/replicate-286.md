# Replicate 286 — independent check of the "unsatisfied existence constraint" (challenge 243)

**Date:** 2026-11-04. **Type of result:** a literature determination, not a calculation or simulation.
Every number below is an *observation reported by the cited authors*, unless it is labelled as my arithmetic.

## 0. Independence disclosure (read this first)

- The claim under challenge is **not on `main`**. I searched `main` / `work/frontier-foundation`
  (`git grep` for "existence constraint", "unsatisfied", "kcnk5b", "longfin", "bioelectric") and found
  only `findings/gemini-triage-267-problems.json` (`bioelectric-fin-size` entry) and
  `findings/README-no-gpu-problem.md`. Neither states the challenged constraint.
- **I did not open `docs/research/fish/challenge-243.md`.** But to locate it I ran `git show --stat` on
  branch `claude/challenge-243-bioelectric-claim-g6xwy2`, which printed the challenger's **commit
  message**. It names Le Bleu 2025 (PMC13078715), Cacna1g, and the conclusion "C3 is not 'unsatisfied'".
  So I am **not blind** to their headline answer or their key citation. I stopped there and did not read
  the file. A reader should discount my agreement on that account.
- To limit the anchoring, I read the primary paper in full text myself, checked its own numbers, and
  stated below exactly which parts of a "reader" constraint it does and does not satisfy.

**My reading of the question (my inference, because the claim text was not available to me):** the
framework asserts that, for "bioelectric" control of zebrafish fin size, there must *exist* a
voltage-sensitive reader (a transducer that turns fibroblast membrane voltage, Vm, into a growth-limiting
signal), and it says no such reader has been shown. I test whether a published reader satisfies that.

## 1. Result

**My value: the existence constraint is SATISFIED at the level of a named, genetically required,
voltage-gated candidate reader. It is NOT satisfied at the level of a demonstrated in-vivo link from
K⁺-channel-set Vm to that reader.**

- Satisfied: Cacna1g (Cav3.1, T-type), plus L/N-type Cav channels, in fin fibroblast-lineage blastema
  cells. Evidence: loss-of-function long fins, loss of in-vivo Ca²⁺ dynamics in the mutant, and
  Cav-dependent Ca²⁺ spikes when isolated fibroblasts are depolarised.
- Not satisfied (gaps reported by the authors or found by my search of the paper text):
  1. Vm was not measured in vivo in the paper. Depolarisation was imposed in vitro with 80 mM KCl.
  2. No double mutants or epistasis between `cacna1g` and `alf`/kcnk5b or `lof`/kcnh2a. The authors'
     K⁺→hyperpolarisation→less Cav→less calcineurin chain is offered as one of three alternatives
     ("could act upstream… Alternatively… Finally… feedback loop").
- **Uncertainty:** the categorical call depends on how strictly the framework defines "reader". Under a
  loose definition (a voltage-gated molecule whose loss phenocopies the K⁺ long-fin models), I am
  confident (high) that it is satisfied. Under a strict definition (shown to read the Vm set by the K⁺
  alleles, in vivo), it stays unsatisfied (also high confidence, based on the absences listed above).
  So "unsatisfied" with no qualifier is false under the loose definition. Under the strict one it is an
  overstatement, because it ignores a published candidate.

## 2. Inputs, sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| S1 | Le Bleu HK, Kioussi RG, Henner AL, Lewis VM, Stewart S, Stankunas K. *Voltage-gated calcium channels generate blastema Ca²⁺ fluxes restraining zebrafish fin regenerative outgrowth.* Development 152(23), 2025. doi:10.1242/dev.204739; PMID 41321290; PMC13078715 (NIHMS author manuscript); preprint bioRxiv 10.1101/2024.08.21.608903 | **full-text** (NCBI efetch, PMC author manuscript; supplementary figures **not** read) | All items in §3 |
| S2 | Jiang X, Zhao K, Sun Y, Song X, Yi C, Xiong T, et al. *The scale of zebrafish pectoral fin buds is determined by intercellular K⁺ levels and consequent Ca²⁺-mediated signaling via retinoic acid regulation of Rcan2 and Kcnk5b.* PLoS Biol 22(3): e3002565, 2024 | **abstract-plus** (first ~100k of ~210k characters, via a summarising fetch tool; not read line by line) | Kcnk5b overexpression *increases* depolarisation in embryonic fin buds (DiSBAC2(3) dye), through Na⁺ channels, IP3R and CaMKK, driving *shha* |
| S3 | Perathoner 2014; Daane 2018; Stewart 2021; Yi 2021; Kujawski 2014; Silic 2020 | **listing** only (as cited inside S1) | Background K⁺-channel and calcineurin long-fin models. I did not read them myself. |
| S4 | Repo `findings/gemini-triage-267-problems.json` (`bioelectric-fin-size`) | full-text (local) | Says in-vivo voltage maps are not in public data. Consistent with gap 1. |

Attempts that failed: the Europe PMC `fullTextXML` endpoint returned HTTP 500, pmc.ncbi.nlm.nih.gov
returned a reCAPTCHA page, and the bioRxiv full text returned HTTP 429. NCBI E-utilities `efetch db=pmc`
succeeded.

## 3. The evidence in S1 (author claims, quoted or closely paraphrased)

- **Alleles:** `cacna1g b1477` (6 bp 5′-UTR deletion plus 4 bp exon-3 deletion, frameshift, early stop) and
  `cacna1g b1478` (4 bp deletion plus 36 bp insertion at the exon-3 site, same early stop).
- **Phenotype:** homozygotes have "modestly overgrown" developmental fins. Regenerated caudal fins
  "exceeded their original length" by 24 dpa and were "nearly doubling in length by 46-50 dpa".
  Heterozygotes show only modest overgrowth.
- **In vivo Ca²⁺:** in wild type, *tph1b:GCaMP6s* fibroblast-lineage distal blastema cells show
  heterogeneous Ca²⁺ transients. In `cacna1g b1477/b1477`, "very few… cells showed Ca²⁺ transients". The
  discussion says the fluxes were "almost completely lost".
- **Depolarisation → Cav-dependent spikes (in vitro, primary fin cells, 80 mM KCl).** Fraction of cells
  responding, as reported:
  DMSO 39% (70/109); amlodipine (L) 12% (15/127); cilnidipine (L/N) 4% (4/103); PD17132 (N; the text spells it "PD17132" and "PD1732122", and I do not resolve which is right) 20% (29/147).
- **In vivo pharmacology:** daily 5 µM cilnidipine from 5 to 28 dpa caused significant overgrowth and
  fewer ray joints.
- **Authors' framing of the link to K⁺ channels:** a hypothesis with alternatives, not a demonstration
  (see gap 2).

## 4. Arithmetic (mine)

I recomputed the reported response fractions from the reported counts:

```
15/127 = 11.8 %  (reported 12 %)  ✓
 4/103 =  3.9 %  (reported  4 %)  ✓
29/147 = 19.7 %  (reported 20 %)  ✓
70/109 = 64.2 %  (reported 39 %)  ✗  — 39 % would need a denominator of ~179 (70/0.39 = 179.5)
```

**There is an internal inconsistency in S1's control group** (author manuscript text). Either the count or
the percentage is a typo. I cannot tell which without the figure or the supplement, which I did not read.
It does not change the qualitative call, because all three blockers are below the control under either
reading (39% or 64%). It does change any effect size someone might quote: for cilnidipine, 4/39 ≈ 10×
reduction vs 3.9/64.2 ≈ 16× reduction (my arithmetic).

## 5. Disagreement preserved

On the direction of Vm change caused by K⁺-channel gain of function, the sources disagree:
- Perathoner 2014, as cited in S1 (listing level): Kcnk5b/alf **hyperpolarises**. S1 builds its
  "restrict Cav" hypothesis on this.
- S2 (2024, embryonic pectoral bud, voltage dye): Kcnk5b **increases depolarisation**, through Na⁺ channels.

These come from different tissues and stages (adult regenerating fibroblasts vs a 48 hpf bud), and I do
not reconcile them. The disagreement matters for gap 2. If K⁺ GOF depolarises, then "K⁺ GOF → less Cav
activity" is not the obvious mechanism.

## 6. Scope of negative findings

- "Vm not measured in vivo" and "no epistasis with alf/lof" come from my keyword search of the S1 main
  text only ("voltage indicator", "ASAP", "double", "epista", "membrane potential", "in vivo"), plus my
  reading of its discussion. The supplement was not searched.
- I did no wider literature search for other candidate readers (for example, voltage-sensitive
  phosphatases or Vm-dependent K-Ras clustering in fin). There may be others. That does not affect the
  conclusion, because one satisfying candidate is enough for an existence constraint.

## 7. Comparison with the recorded value

I did not open the recorded working. Its commit message (seen before I knew it would reveal the answer,
see §0) says: "Le Bleu 2025… names a voltage-gated reader in fin fibroblasts (Cacna1g/Cav: LOF long fins,
Cav-dependent depolarisation-evoked Ca²⁺ spikes), so C3 is not 'unsatisfied'". It also says the K⁺
alleles' in-vivo Vm effect is unmeasured in fibroblasts.

**AGREE**, on both points: the reader exists as a candidate, and the in-vivo K⁺→Vm link is undemonstrated.
I add one thing the commit message does not mention: the 70/109 vs 39% inconsistency in S1. Because I
saw the challenger's conclusion first, this is weaker than a fully blind replication.

```swarm-replication
{"claim_id": 286, "my_value": "constraint satisfied at candidate level (Cacna1g/Cav: 2 LOF alleles, regenerates ~2x original length by 46-50 dpa; KCl-evoked spikes 39% [or 64.2% by counts 70/109] DMSO vs 4% cilnidipine); unsatisfied for in-vivo K+-Vm-to-reader link (no in-vivo Vm, no epistasis)", "agrees": true, "note": "Agrees that 'unsatisfied' is wrong for a candidate reader (Le Bleu 2025, full text), but I saw the challenger's commit message before deriving, so this is not fully blind; also found an internal 70/109 vs 39% inconsistency in the source."}
```
