# Claim 242: what it entails at the protein and tissue scales, and whether those requirements hold

**Source claim (242, `cell` scale, evidence: measured).** The GXL evidence API returned 0 supporting
passages out of 35 retrieved for *"a voltage-sensitive transducer reads membrane potential in zebrafish
fin mesenchyme to control ray growth"*. The same API returned 28 supports for the known-true
potassium-channel claim. Claim 242 reads this as the cross-scale constraint being "confirmed
unsatisfied".

**What this document does.** It assumes the underlying mechanism is true (a voltage-sensitive
transducer reads V_mem in fin mesenchyme and controls ray growth). It writes down what that would
require at the adjacent scales (protein, tissue) and checks each requirement against the primary
literature.

**Headline (stated before the detail).** The protein-scale existence requirement is **satisfied by
measured data in a paper that is in the literature**: Le Bleu et al. (bioRxiv 2024; *Development*
2025). Single-cell transcriptomics and RNAScope place voltage-gated Ca²⁺ channels (*cacna1c*,
*cacna1ba*, *cacna1g*) in fibroblast-lineage blastema mesenchyme. KCl depolarisation of those cells
triggers Ca²⁺ spikes that depend on these channels. *cacna1g* loss-of-function fish regenerate
abnormally long fins. **This contradicts claim 242's conclusion.** The GXL zero reflects what the
search covered, not what the field knows. The positive control (28 supports for the K⁺-channel
claim) tests whether the API can tell true K⁺-channel statements from false ones. It does not test
whether the API indexes the Ca²⁺-channel and voltage-transducer literature. *That last sentence is
my inference.* I did not query GXL and do not know what its corpus contains.

The range requirement (does the transducer's voltage window overlap the V_mem that fin mesenchyme
actually occupies?) is **open**. No calibrated millivolt measurement of adult fin-ray mesenchyme
V_mem was found. The papers that come closest say outright that it has not been done (quotes below).
This is "nobody has measured it", not "people measured and found a mismatch".

---

## Sources and read-levels

| # | Source | Read-level | Used for |
|---|---|---|---|
| S1 | Le Bleu HK, Kioussi RG, Henner AL, Lewis VM, Stewart S, Stankunas K. *Voltage-gated calcium channels generate blastema Ca²⁺ fluxes restraining zebrafish fin regenerative outgrowth.* bioRxiv 2024, doi:10.1101/2024.08.21.608903 (v1) | **full-text** (preprint PDF, text extracted; figures not inspected) | C1, C3, C4 |
| S1′ | Same title, *Development* 2025, doi:10.1242/dev.204739, PMC13078715 | **abstract** (full text not retrievable: Europe PMC returned HTTP 500; PMC served a CAPTCHA) | confirms S1 conclusions survived peer review |
| S2 | Stewart S, Le Bleu HK, Yette GA, Henner AL, Robbins AE, Braunstein JA, Stankunas K. *longfin causes cis-ectopic expression of the kcnh2a ether-a-go-go K⁺ channel to autonomously prolong fin outgrowth.* *Development* 2021, doi:10.1242/dev.199384, PMC8217709 | **full-text** (HTML text; figures not inspected) | C2 (negative scope), C3, C4 |
| S3 | Yi C et al. (Antos lab). *A calcineurin-mediated scaling mechanism that controls a K⁺-leak channel to regulate morphogen and growth factor transcription.* *eLife* 2021;10:e60691, PMC8110307 | **full-text** (XML, read by keyword search; not read end to end) | C2 (negative scope), disagreement D1 |
| S4 | Jiang et al. *The scale of zebrafish pectoral fin buds is determined by intercellular K⁺ levels and consequent Ca²⁺-mediated signaling via retinoic acid regulation of Rcan2 and Kcnk5b.* *PLoS Biol* 2024, doi:10.1371/journal.pbio.3002565, PMC11018282 | **full-text** (XML, read by keyword search) | C2 (negative scope), disagreement D1 |
| S5 | Liu J, Nerli E, Duclut C, Vishen AS, Berbee N, Kaufmann S, Ponce C, Arrenberg AB, Jülicher F, Mateus R. *Injury-induced electrochemical coupling triggers organ growth.* *Sci Adv* 2026;12(6), doi:10.1126/sciadv.aec0687, PMC12871474 | **full-text** (XML, read by keyword search) | C1 (alternative transducer, wrong tissue), C2, C4, disagreement D2 |

Hosts that could not be reached from this session: pubmed.ncbi.nlm.nih.gov, mpi-cbg.de,
scholarsbank.uoregon.edu, charlieduclut.github.io. bioRxiv HTML was rate-limited (HTTP 429), but
the S1 PDF downloaded. None of these failures removed a source I needed. S1′ is the only source read
at abstract level only.

---

## Constraints and checks

### C1: protein · existence: SATISFIED (measured)

**Requirement.** Fin-ray mesenchyme must express a protein with a voltage-sensing element whose
output changes when V_mem changes, and loss of that protein must change ray outgrowth.

**Check.** S1 (full-text) meets every part of this:
- **Expression in the right cells.** In re-analysed 7-dpa scRNA-seq, together with RNAScope on 7-dpa
  sections, "*cacna1ba* exclusively was expressed in *dachc* coexpressing distal blastema" and
  "*cacna1c* and *cacna1g* transcripts were enriched in all fibroblast-lineage cells and adjacent
  blastema-lining osteoblasts". The authors conclude these channels "likely contribute to the
  observed cytosolic Ca²⁺ dynamics within intra-ray fibroblast-lineage cells".
- **Voltage → output.** Primary *tph1b:GCaMP6s* fibroblast-lineage cells were depolarised with KCl
  (80 mM final, starting from 5 mM in Tyrode's). "56% of tph1b:GCaMP6s-responsive cells spiked
  GCaMP6s fluorescence upon membrane depolarization". VGCC blockers lowered the fraction of
  excitable cells from 39% (70/109, DMSO) to 12% (amlodipine, 15/127), 4% (cilnidipine, 4/103) and
  20% (PD17132, 29/147). (Two different percentages appear in the preprint, 56% and 39%. They seem to
  come from different denominators or filters, and I have not reconciled them.)
- **Output → ray growth.** "Daily 5 µM cilnidipine from 5-28 dpa caused significant fin overgrowth".
  The *cacna1g^b1477^* and *cacna1g^b1478^* homozygotes "regenerated exceptionally long caudal fins
  that greatly exceeded their developed length by 24 dpa".

**Limits, in the authors' own data.** The depolarisation was 80 mM KCl applied to dissociated cells
*in vitro*, which is not a physiological stimulus. No millivolt value was recorded. The in vivo link
rests on the mutant and the pharmacology, not on a voltage measurement in vivo. A Ca²⁺ channel
matches "voltage-sensitive transducer" as the claim states it generically. Whether the in vivo
trigger is V_mem as opposed to some other gate on these channels is not shown directly (see C2).

**Alternative transducer, ruled out for this tissue.** S5 identifies voltage-sensing phosphatase
(*tpte*) as the transducer that is "necessary and sufficient" for injury-induced proliferation. That
work is in **2-dpf larval fin-fold epithelium**, and the authors say their larval system regrows "by
essentially promoting epithelial proliferation … instead of a classic dedifferentiated, proliferative
mesenchymal blastema". So S5 does not meet C1 for adult fin-ray mesenchyme, and I do not count it.

**Bearing on claim 242.** Claim 242's "confirmed unsatisfied" is contradicted by S1/S1′. S1′ is a
peer-reviewed 2025 paper whose abstract is close to a restatement of the queried proposition: it
concludes that "'bioelectricity' for fin size control reflects voltage-modulated Ca²⁺ fluxes in
fibroblast-lineage blastemal cells". It is my inference that the GXL result is a corpus-coverage
miss. I did not inspect the GXL index.

### C2: protein · range: OPEN (searched; the required measurement does not exist)

**Requirement.** The transducer's voltage operating window must overlap the in vivo V_mem range of
fin-ray mesenchyme, *including* the V_mem shift produced by the known long-fin K⁺-channel alleles
(*kcnh2a* in *longfin^t2^*, *kcnk5b* in *another longfin*). Quantity: in vivo resting V_mem and its
excursions in fin-ray mesenchyme. Bounds: **unknown**.

**What I searched.** Calibrated, millivolt-scale V_mem in adult fin-ray mesenchyme or blastema,
using web search ("resting membrane potential mV fin regenerate blastema … patch clamp"; "zebrafish
fin membrane potential measured mesenchyme kcnk5b DiBAC voltage dye") and full-text keyword searches
for `mV`, `membrane potential` and `resting` in S1–S5.

**What I found.**
- S2 (2021): "Key future steps include characterizing membrane potentials and putative depolarizing
  signals … of intra-ray mesenchymal cells during fin outgrowth." The authors flag this as not done.
- S1: every `mV` hit is absent. The only voltage manipulation is the 80 mM KCl step. The authors
  speculate about "heterogeneous cell states with differential resting membrane potential", which
  is a hypothesis, not a measurement.
- S3: the only `mV` values are patch-clamp command potentials in HEK cells (held at −80 mV, stepped
  from −100 to +70 mV). There is no fin V_mem.
- S4: membrane potential is reported only as DiSBAC2(3) photon counts, without calibration, in
  **embryonic pectoral fin buds** (32–56 hpf), not adult rays.
- S5: Voltron2 is reported only as −ΔF/F, in **larval epithelium**. The ~+40 mV figure in S5 is
  the activation threshold of VSP, which the authors cite from earlier literature. It is not a fin
  measurement. The authors themselves suggest *longfin^t2^* tissue has a "hyperpolarized V_mem
  baseline" so that injury "may not be sufficient to trigger VSP activation". That is their
  inference, not a measured value.

**Status reasoning.** No measured fin-mesenchyme V_mem exists in what I read, so I cannot test
whether the window overlaps. This is **not** `unsatisfiable`, because no measured number contradicts
the requirement. It is also **not** `unsatisfied` in the sense of "people looked and found nothing
that fits". The literature says the measurement has not been made. The scope of this negative: five
full-text papers plus two web searches. I did not run a systematic database search (PubMed was
unreachable). The negative therefore does not exclude a V_mem recording published somewhere I did
not look.

**Note for anyone who picks this up.** T-type channels such as *cacna1g* are generally described
as activating near rest. S1 calls Cacna1g potentially responsive to "small membrane potential
changes", but I found no zebrafish-fin V½ for any of the three channels. I did not import mammalian
V½ values, because that would be a guess about this tissue rather than a measurement of it.

### C3: tissue · timescale: SATISFIED (measured)

**Requirement.** The process that reads voltage and controls growth must act during the
outgrowth-deceleration phase of regeneration, which lasts days. It cannot act only during blastema
establishment. It must therefore integrate over a period much longer than individual V_mem or Ca²⁺
events. Quantity: the window (dpa) over which perturbing K⁺-channel, VGCC or calcineurin activity
changes final ray length. Bounds: about 5 to about 21 dpa.

**Check (all measured, from full text).**
- S2: wild-type and *longfin^t2^* have "indistinguishable maximal growth rates reached between 3 and 5
  dpa". The overgrowth comes from "an extended outgrowth period beginning around 6 dpa". "Wild-type
  fins largely ceased regenerative outgrowth by 21 dpa, whereas lof t2 fins continued to extend
  through the 30 dpa" endpoint. Kcnh2a inhibition with astemizole (500 nM) from 7 to 30 dpa
  suppressed the overgrowth. FK506 "from 1-5 dpa had no effect on fin outgrowth", whereas "FK506
  treatment from 6-21 or 1-21 dpa caused the same extent of pronounced fin overgrowth".
- S1: cilnidipine from 5 to 28 dpa caused overgrowth. The authors place VGCC action "after 5 dpa and
  onwards to slow and eventually terminate outgrowth".
- S1: in vivo Ca²⁺ events in distal blastema cells are "spikes of variable duration and oscillatory
  pattern" at 3 dpa. I did not find their durations given in the text. They are individual events
  set against a control window measured in days, so the requirement for integration follows.
  *That conclusion is my inference.* S2 and S1 propose calcineurin as the integrating node. That is
  the authors' hypothesis, not a demonstrated integrator.

**A contrast, not a contradiction.** S5 (larval epithelium) measures V_mem depolarisation at 100 ms
and VSP-dependent proliferation within 1 h of injury. This is a different tissue at a different
stage, working on a different timescale. S5 itself notes that the adult blastema process takes about
2 weeks and is "an exciting frontier to be explored".

### C4: tissue · spatial: SATISFIED (measured, qualitative bound only)

**Requirement.** The voltage signal must be read where the growth decision is made: within the
intra-ray fibroblast-lineage mesenchyme, at cell-autonomous scale. Any coordinating field must not
need to extend beyond that compartment. Quantity: the spatial range over which the voltage-dependent
signal is coordinated. A numeric bound is **unknown**. The bound I can support is qualitative:
cell-autonomous.

**Check.**
- S2 (full-text; transplantation measurement): "*longfin^t2^*-ectopic *kcnh2a* acts tissue
  autonomously within the fin intra-ray mesenchymal lineage."
- S1 (full-text): in vivo Ca²⁺ fluxes were "qualitatively heterogeneous and not overtly coordinated,
  arguing against the transmission of bioelectric signals across a blastema field". That is the
  authors' interpretation of their imaging.
- S3 (full-text): Kcnk5b-induced *shh*/*lef1* activation is cell-autonomous in mosaic larvae (the
  cells include mesenchyme surrounding the otic vesicle and fin-fold epithelium; not adult rays).

**Disagreement kept.** S5 measures a tissue-scale depolarisation gradient spanning about 200 µm
within 100 ms in larval epithelium, and a Ca²⁺ wavefront extending to about 120 µm. This is a
coordinated field. It is in a different tissue (larval epithelium versus adult intra-ray mesenchyme)
and serves a different function (injury sensing versus growth cessation). I have not averaged the
two pictures. They describe different systems, and nothing I read tests either one in the other's
tissue.

---

## Disagreements between sources (not resolved)

- **D1. Direction of V_mem change from Kcnk5b, and whether V_mem or [K⁺]ᵢ is the signal.**
  S3: "opening of Kcnk5b causes a flow of K⁺ out of the cell, which hyperpolarizes the membrane
  potential". This is stated from channel biophysics, not measured in fin. The mechanism S3 proposes
  is lowered cytoplasmic K⁺ (measured by FRET-FLIM). S3 identifies no voltage-sensitive protein:
  "It will be important to find out how this electrophysiological signal coordinates the activity
  of these developmental signals". S4 *measured* the opposite direction in fin buds:
  "overexpression of *kcnk5b*-mCherry significantly increased depolarization". S4 explains this with
  Na⁺ channels, inferred from pharmacology only (vinpocetine, dibucaine) with no *scn* gene named.
  If the operative variable is [K⁺]ᵢ rather than V_mem, the claim's wording ("reads membrane
  potential") would be the wrong description of the mechanism even though a K⁺-dependent growth
  control exists. No source I read settles this for adult ray mesenchyme.
- **D2. Sign of the growth response to depolarisation.** In adult regenerating fins (S1), voltage-gated
  Ca²⁺ entry *restrains* outgrowth: blocking it or losing *cacna1g* gives longer fins. In larval fins
  (S5), depolarisation with KCl or VSP over-expression *promotes* growth (about 10% longer fin folds),
  and the hyperpolarising *longfin^t2^* allele *impairs* larval regrowth at 3 dpa. That is the
  opposite of its adult phenotype. S5 flags the discrepancy itself and attributes it to differences
  in cell type.

---

## What this does and does not establish

- No experiment or simulation was run for this document. Every status above rests on published
  measurements, quoted with their source. Where I drew an inference I have said so in the same
  sentence.
- The one finding that changes the record: **claim 242's "confirmed unsatisfied" does not survive a
  literature check.** The existence constraint is met by S1/S1′. This does not mean the full
  proposition ("reads membrane potential … to control ray growth") is proven. C2 is open, and D1
  leaves open whether V_mem or [K⁺]ᵢ is the variable being read.
- No constraint reached `unsatisfiable`. No measured number contradicts any of them.

```swarm-entail
{"source_claim": 242, "source_scale": "cell",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "A protein with a voltage-sensing element must be expressed in fin-ray mesenchyme, change its output with membrane potential, and alter ray outgrowth when lost",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Voltage-gated Ca2+ channels cacna1c (L), cacna1ba (N), cacna1g (T) expressed in fibroblast-lineage blastema (scRNA-seq + RNAScope, 7 dpa); KCl depolarisation triggers VGCC-dependent Ca2+ spikes in primary fin fibroblasts (excitable fraction 39% DMSO vs 4-20% with blockers); cilnidipine 5-28 dpa and cacna1g b1477/b1478 homozygotes give regenerative fin overgrowth",
      "satisfied_evidence": "measured",
      "note": "Le Bleu et al. bioRxiv 2024 doi:10.1101/2024.08.21.608903 (full-text); Development 2025 doi:10.1242/dev.204739 (abstract). Depolarisation was 80 mM KCl in vitro, no mV recorded. Contradicts claim 242's 'confirmed unsatisfied': the GXL zero is inferred (not verified) to be a corpus-coverage miss. VSP/tpte (Liu et al. Sci Adv 2026, full-text) is a voltage transducer but in larval epithelium, not mesenchyme, so not counted."},
    {"target_scale": "protein", "kind": "range",
      "statement": "The transducer's voltage operating window must overlap the in vivo membrane-potential range of fin-ray mesenchyme, including the shift caused by long-fin K+-channel alleles",
      "quantity": "in vivo resting membrane potential and excursions of adult fin-ray mesenchyme", "lo": null, "hi": null, "units": "mV",
      "status": "open",
      "satisfied_by": "Searched for calibrated mV measurements of fin-ray mesenchyme/blastema V_mem: none found. Stewart 2021 lists characterising mesenchymal membrane potentials as future work; Le Bleu 2024 reports no mV; Yi 2021 mV values are HEK command potentials only; Jiang 2024 uncalibrated DiSBAC2(3) photon counts in embryonic fin buds; Liu 2026 Voltron2 dF/F in larval epithelium. No zebrafish-fin V1/2 found for cacna1c/cacna1ba/cacna1g.",
      "satisfied_evidence": "unknown",
      "note": "This is 'nobody has measured it', not 'measured and mismatched'. Scope: 5 full-text papers (Le Bleu 2024 bioRxiv; Stewart 2021 Development PMC8217709; Yi 2021 eLife PMC8110307; Jiang 2024 PLoS Biol PMC11018282; Liu 2026 Sci Adv PMC12871474) plus two web searches; PubMed unreachable, no systematic database search. The VSP threshold ~+40 mV in Liu 2026 is literature-cited, not a fin measurement, and does not contradict the constraint."},
    {"target_scale": "tissue", "kind": "timescale",
      "statement": "The voltage-read growth control must act during the multi-day outgrowth-deceleration phase, not only at blastema establishment, and so must integrate over much longer than individual voltage/Ca2+ events",
      "quantity": "regeneration window (days post-amputation) in which K+-channel, VGCC or calcineurin perturbation changes final ray length", "lo": 5, "hi": 21, "units": "dpa",
      "status": "satisfied",
      "satisfied_by": "Peak growth rate equal in WT and longfin t2 at 3-5 dpa; overgrowth from extended outgrowth beginning ~6 dpa; WT outgrowth largely ceases by 21 dpa; astemizole 7-30 dpa suppresses longfin overgrowth; FK506 1-5 dpa has no effect on outgrowth while 6-21 dpa causes full overgrowth; cilnidipine 5-28 dpa causes overgrowth",
      "satisfied_evidence": "measured",
      "note": "Stewart et al. Development 2021 doi:10.1242/dev.199384 (full-text); Le Bleu et al. bioRxiv 2024 (full-text). Ca2+ spike durations not found in text. Calcineurin as integrator is the authors' hypothesis. Liu 2026 (larval epithelium) operates on ms-to-1 h timescales, which is a different system, not a contradiction."},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "The voltage signal must be read where the growth decision is made (within intra-ray fibroblast-lineage mesenchyme, at cell-autonomous scale), without requiring a field coordinated beyond that compartment",
      "quantity": "spatial range of coordination of the voltage-dependent growth signal", "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Blastula transplantation: longfin t2 ectopic kcnh2a acts tissue-autonomously in intra-ray mesenchymal lineage; in vivo blastema Ca2+ fluxes heterogeneous and not overtly coordinated",
      "satisfied_evidence": "measured",
      "note": "Stewart 2021 (full-text); Le Bleu 2024 (full-text; 'arguing against transmission of bioelectric signals across a blastema field' is the authors' interpretation). Bound is qualitative only; no numeric length scale found for the adult blastema. Disagreement kept: Liu 2026 measures a ~200 um depolarisation gradient in 100 ms in larval epithelium (different tissue and function)."}
  ]}
```
