# Design review (DRAFT) — genotype → fin growth → whole organism

**Status:** draft for root. **Not a biological feasibility assessment.**
**No probability of biological success appears anywhere in this document, and
none should be added.** There is no reference class from which to draw one and
no experiment behind it; "this is not established" is the honest form, and
"this is unlikely" is already more than the evidence supports.

**Method.** Primary sources fetched from Europe PMC *first*, then an adversarial
review grounded strictly in that text, then every specific claim checked back
against the sources. 13 of 13 fragments verified, 3 of 3 negative controls
absent, and the one direct quote context-read. Read levels are attached
throughout: an abstract is weaker evidence than a full text and is never written
up as though the paper had been read.

**What this reviews.** The chain the flying-fish mission implies:

```
(0) designed DNA sequence
 →  (1) transcription of the intended gene, in the intended cells, at the intended time
 →  (2) altered bioelectric state (Vmem / intracellular K+)
 →  (3) altered fin size or proportion
 →  (4) altered whole-organism capability (gliding)
```

## Verdict per interface

| Interface | Status | Where it breaks |
| --- | --- | --- |
| **(0) sequence design** | **UNSUPPORTED** | No supplied source addresses generative DNA models at all. The candidates were produced by a model that does not represent chromatin accessibility, and no accessibility predictor exists for zebrafish |
| **(0)→(1) sequence → transcription** | **UNSUPPORTED** | Every source drives expression from *validated* promoters — `hsp70`, `ubb`, `claudinb`, `-5.4k pax3a`. None establishes that a novel sequence transcribes in the intended cells; correct motifs can sit in closed chromatin and stay silent |
| **(1)→(2) transcription → bioelectric state** | **SUPPORTED** | In zebrafish embryonic pectoral fin buds, `Tg[hsp70:kcnk5b-GFP]` induction lowers intracellular K⁺ (KIRIN1/FLIM) and depolarises (DiSBAC2(3)) — PMC11018282. **But** that used a strong ubiquitous heat-shock promoter; it says nothing about whether a novel promoter reaches the needed expression threshold |
| **(2)→(3) bioelectric → fin size** | **SUPPORTED** | `kcnk5b` overexpression enlarges embryonic fin buds (PMC11018282); `kcnh2a` (*lof*), `kcnk5b` (*alf*) and `kcnj13` alleles elongate adult fins (PMC10137051; PMC8217709, abstract). **But** the viable overgrowth mutants are specific dominant/neomorphic alleles with particular spatiotemporal distributions |
| **(3)→(4) fin size → gliding** | **UNSUPPORTED — weakest link** | See below |

## The weakest link, stated precisely

The strongest source for (3)→(4) is Daane et al. 2021 (PMC9172250, **abstract
only**). Its own words, read in context:

> "interaction between these genetic loci in zebrafish closely phenocopies the
> observed **fin proportions** of flying fishes"

**Fin proportions.** Not gliding, not flight, not any organism-level capability.
The chain substitutes a morphological phenotype for a biomechanical one. Gliding
additionally requires musculature, skeletal reinforcement, control surfaces and
behavioural neural circuits, none of which a change in fin proportion supplies
and none of which the supplied sources address.

A long-finned zebrafish is a long-finned zebrafish.

**Falsifiable check:** startle-response assay near the water surface on
long-finned transgenics, measuring aerial distance and duration against
wild-type. A null result refutes the step as stated.

## Falsifiable checks for the other interfaces

| Interface | Check that would settle it |
| --- | --- |
| (0) design | ATAC-seq on cells carrying the designed sequence: is the region actually accessible *in vivo*? |
| (0)→(1) | Transgenic reporter under the designed sequence: does fluorescence appear in fin mesenchyme at the intended stage? |
| (1)→(2) | KIRIN1/FLIM on fin buds expressing a K⁺ channel from the *designed* promoter; compare the magnitude of K⁺ change to wild-type |
| (2)→(3) | Adult fin-to-body length ratio in those transgenics, with organismal viability recorded |

## Hypotheses that are uncertain and must not be stated as fact

1. A sequence generated without accessibility modelling will be accessible and
   transcribed *in vivo*.
2. A designed promoter will drive expression strongly enough to move ion
   homeostasis at all.
3. A change in fin proportion is sufficient for gliding capability.
4. Ectopic K⁺-channel expression from a novel promoter will not be lethal or
   pleiotropic in excitable tissue.

## Evidence that argues AGAINST the chain

Recorded because a proponent would be tempted to omit it.

- **Pleiotropy and viability.** K2P channels are expressed in neural tissue and
  regulate excitability; their mutation is linked to neuronal and cardiovascular
  disorders (PMC11269526, abstract). A promoter that is not tightly
  tissue-restricted is a viability risk, not merely an efficacy risk.
- **Perturbation can impair growth, not only increase it.** `kcnh2a lof/lof`
  **impairs** injury-induced proliferation and finfold regrowth (PMC12871474).
  The same channel family moves outcomes in both directions depending on context.
- **One channel is not enough.** The flying-fish-like proportion needed the
  *interaction* of `kcnh2a` with the amino-acid transporter `lat4a`
  (PMC9172250, abstract). A single-channel intervention is not the published
  result.
- **Context mismatches throughout.** The mechanistic K⁺ work is in **embryonic
  pectoral fin buds**; the dramatic phenotypes are **adult fins**; PMC12871474
  is **regeneration after injury**, not development. These are three different
  systems and the chain reads across all of them silently.

## What our own measurements do and do not add

From this harness's completed runs, reported with their limits:

- The 16 Evo 2 candidates are **indistinguishable from real zebrafish promoters**
  under the generating model's own likelihood (−1.2255 vs −1.2031) and under an
  independent motif scan (z = +0.69 vs +1.23, intervals overlapping).
- **Neither is evidence of function.** The likelihood test scores candidates with
  the model that produced them, so a high score is expected by construction. The
  motif scan is composition, not binding. Both sit within ~0.2 nats of the
  random floor.
- **Nothing has been transfected, expressed or assayed in any organism.** Every
  interface above from (0)→(1) onward is untested by us.

## How to read this document

The two SUPPORTED rows are supported **in zebrafish, in the specific system each
paper used, with validated promoters**. They are not support for the chain. A
chain is only as good as its weakest interface, two of the five are UNSUPPORTED,
and one of those is the step that would make the result interesting.

The model analysis behind this is a **lead**, not verified truth, and not a
review by a person. Its specifics were checked; its judgement was not.
