# Claim 242: what has to hold at the protein and tissue scales

**Source claim (cell scale, evidence: measured):** *"a voltage-sensitive transducer reads membrane
potential in zebrafish fin mesenchyme to control ray growth."* The source record says the GXL evidence
API returned 0 supporting passages out of 35 retrieved for this sentence. The same API returned 28
supports for the known-true potassium-channel claim.

**Result in one line.** The literature check **contradicts the GXL zero on existence**. A
voltage-gated Ca²⁺ channel gene, *cacna1g* (T-type, Cav3.1), is expressed in fin fibroblast-lineage
blastema cells. Its loss-of-function mutants grow abnormally long regenerated fins (Le Bleu et al.
2025). So the protein-scale existence requirement is **satisfied**. The range requirement is
**unsatisfied**: no paper reports an absolute membrane potential for fin mesenchyme, so nobody has
shown that mesenchymal Vmem sits inside the transducer's operating window. **No constraint is
unsatisfiable.** No measured number contradicts the claim.

The GXL zero and this finding disagree, and I am not averaging them. My guess at why they differ is an
**inference that I have not tested**. Le Bleu et al. never write "voltage-sensitive transducer" or
"membrane potential … read". They describe "voltage-gated calcium channels" that "generate blastema
Ca²⁺ fluxes". A passage retriever matching the claim's wording could plausibly miss it. The paper is
also recent: bioRxiv 2024, *Development* 2025. If the GXL corpus predates it, that would also explain
the zero. I do not know the GXL corpus date (`unknown`).

---

## Sources and read-levels

All of these were read through an automated page fetch that returned a model-written summary of the
full text, with verbatim quotes on request. I did not read the PDFs line by line. The read-level is
**full-text (machine-summarised)** unless a source says otherwise.

| # | Source | Read-level |
|---|---|---|
| S1 | Le Bleu HK, Kioussi RG, Henner AL, Lewis VM, Stewart S, Stankunas K. *Voltage-gated calcium channels generate blastema Ca²⁺ fluxes restraining zebrafish fin regenerative outgrowth.* Development 2025;152(23):dev204739. doi:10.1242/dev.204739. PMC13078715 | full-text (machine-summarised; first 100k of 106k characters) |
| S2 | Stewart S, Le Bleu HK, Yette GA, Henner AL, Robbins AE, Braunstein JA, Stankunas K. *longfin causes cis-ectopic expression of the kcnh2a ether-a-go-go K⁺ channel to autonomously prolong fin outgrowth.* Development 2021;148(11):dev199384. doi:10.1242/dev.199384. PMC8217709 | full-text (machine-summarised; first 100k of 120k characters) |
| S3 | Perathoner S, Daane JM, Henrion U, Seebohm G, Higdon CW, Johnson SL, et al. *Bioelectric signaling regulates size in zebrafish fins.* PLoS Genet 2014;10(1):e1004080. doi:10.1371/journal.pgen.1004080 | full-text (machine-summarised) |
| S4 | Jiang X, Zhao K, Sun Y, Song X, Yi C, Xiong T, et al. *The scale of zebrafish pectoral fin buds is determined by intercellular K⁺ levels and consequent Ca²⁺-mediated signaling via retinoic acid regulation of Rcan2 and Kcnk5b.* PLoS Biol 2024;22(3):e3002565. doi:10.1371/journal.pbio.3002565 | full-text (machine-summarised; first 100k of 211k characters) |
| S5 | Yi C, Spitters TW, Al-Far EAA, et al. *A calcineurin-mediated scaling mechanism that controls a K⁺-leak channel to regulate morphogen and growth factor transcription.* eLife 2021;10:e60691 | search-summary (abstract-level content and peer-review remarks from a search tool; not opened) |
| S6 | Baumgart JP, Vitko I, Bidaud I, Kondratskyi A, Lory P, Perez-Reyes E. *I–II loop structural determinants in the gating and surface expression of low voltage-activated calcium channels.* PLoS One 2008;3(8):e2976. PMC2495038 | full-text (machine-summarised; Table 1 values quoted) |
| S7 | Lory P, Nicole S, Monteil A. *Neuronal Cav3 channelopathies: recent progress and perspectives.* Pflügers Arch 2020;472(7):831–844. PMC7351805 | full-text (machine-summarised; first 100k of 184k characters). Used only for the qualitative statement that the Cav3 window current lies near the resting potential |

---

## C1 — protein · existence — **satisfied**

**Requirement (generic).** At least one protein must exist that (a) changes activity with membrane
voltage, (b) is expressed in fin intra-ray mesenchyme or its blastema derivatives, and (c) changes
ray outgrowth when it is lost.

**Check.** S1 meets all three parts with measured data:
- **(b) Expression, measured (RNAscope plus single-cell data).** *cacna1g* (T-type) and *cacna1c*
  (L-type) are enriched across fibroblast-lineage blastema cells and blastema-lining osteoblasts.
  *cacna1ba* (N-type) is localised to the distalmost blastema cells.
- **(c) Loss-of-function phenotype, measured.** *cacna1g* loss-of-function alleles (`b1477`, `b1478`)
  reduced in vivo Ca²⁺ fluxes. Homozygous mutants "regenerated extraordinarily long fins due to
  prolonged outgrowth" (P<0.0001). Daily 5 µM cilnidipine (an L/N-type blocker) from 5 to 28 dpa
  "caused significant fin overgrowth" (P=0.0004).
- **(a) Voltage sensitivity.** These are voltage-gated channels by molecular class. In S1, the
  80 mM KCl depolarisation in isolated cells produced Ca²⁺ responses, and Cav blockers reduced the
  number of excitable cells. That is measured in vitro.

**What this does not establish (author claim vs. my inference).** S1 did not measure membrane
potential in any form. S1 also did not image Ca²⁺ or Vmem in *alf* (*kcnk5b*) or *longfin*
(*kcnh2a*) fish. The authors **propose** that K⁺ channels act upstream by limiting Ca²⁺ influx. That
is their model, not their result. It is my **inference** that Cav3.1 is *the* transducer reading the
Vmem set by Kcnk5b or Kcnh2a. That inference is not tested anywhere I found. The existence constraint
is satisfied. The claim's full causal chain, from K⁺ channel to Vmem to Cav to growth, is not.

**Disagreement to preserve.** S4 (pectoral fin **buds**, embryonic, not adult rays) proposes the
opposite kind of mechanism. In S4, intracellular **K⁺ concentration**, not voltage, is the signal.
Ca²⁺ comes from **IP3R-mediated ER release**, and "plasma-membrane Ca²⁺ channel inhibition had no
significant effect on SHH transcription". S5 likewise attributes the Kcnk5b → *shh*/*lef1* effect to
reduced cytoplasmic K⁺. An S5 reviewer questioned whether the transcriptional response reflects the
electrophysiological change. These sources concern a different stage and a different readout
(*shha* transcription, not ray length), so they do not refute C1. They do show that a non-voltage
transducer has published support in the same organ.

## C2 — protein · range — **unsatisfied** (people looked; nobody made an absolute measurement)

**Requirement (generic).** The resting Vmem of fin mesenchyme, and the shifts produced by the growth
mutants, must fall inside the voltage window where the transducer's activity changes. Otherwise the
transducer cannot "read" the potential.

**Bound used.** For the one transducer named in C1, the window comes from **measured** values in a
heterologous system. Human Cav3.1 in HEK-293 cells (S6, Table 1):
- activation: V½ = −44.6 ± 0.7 mV, k = 5.8 mV (n=19)
- inactivation: V½ = −77.7 ± 0.7 mV, k = −5.0 mV (n=15)

**Derived, not observed.** I multiplied the two Boltzmann curves with those parameters. The
steady-state window peaks at **−69 mV** and is above half its maximum between **−82 and −50 mV**.
That interval is the lo/hi below. It is a calculation from S6's fitted parameters. It is not a
measurement of a window current, and it is for the **human** channel. The gating parameters of
zebrafish Cacna1g are `unknown`; I found no paper reporting them. S7 states qualitatively that the
Cav3 window current lies near the resting membrane potential.

**Check — what exists for the fin side of the comparison:**
- **S3.** Absolute values come only from **Xenopus oocytes**. There, mutant Kcnk5b shifts Vmem
  "towards −90 to −100 mV". In juvenile fins, a DiSBAC₂(3) dye gave only a **relative** readout:
  "alf fins … show high levels of depolarization across the fin". The **direction is opposite** to
  the oocyte result, and the authors acknowledge this.
- **S4.** DiSBAC₂(3) in pectoral fin buds gave photon counts only, with no mV values. Kcnk5b
  overexpression *depolarised*, and the authors caveat possible differences in dye penetration.
- **S1, S2.** No Vmem measurement at all. S2 lists "characterizing membrane potentials" as future
  work.

**Scope of the negative.** One extended web search (zebrafish fin, membrane potential, voltage
imaging, mesenchyme, *kcnk5b*, longfin), plus full reading of S1–S4 for any mV value in fin tissue.
I did not search patch-clamp or sharp-electrode literature on fin fibroblasts specifically, and I did
not check GEVI transgenic-line papers beyond what the search returned. The one ASAP1 line it surfaced
was used in early embryos, not fins. The finding is: **people looked at fin Vmem, and they used only
relative dyes.** It is not "nobody looked". Because no absolute fin value exists, nothing contradicts
the window either. That is why C2 is not unsatisfiable.

**Derived observation worth testing, not observed.** A window-current transducer responds
non-monotonically. With S6's parameters, both a hyperpolarisation to −90 mV (product ≈ 3.7×10⁻⁴) and
a depolarisation to −30 mV (≈ 6.7×10⁻⁵) *reduce* steady-state open probability relative to the
−69 mV peak (≈ 2.2×10⁻³). If that held in vivo, both the oocyte-direction (hyperpolarising) and the
dye-direction (depolarising) reading of *alf* would predict less Cav3 Ca²⁺ entry. That would match
the *cacna1g* loss-of-function overgrowth. This is a calculation on human-channel parameters with no
fin data behind it. It could make the S3 sign disagreement irrelevant to C1. It does not resolve that
disagreement.

## C3 — tissue · timescale — **satisfied** (with a stated gap)

**Requirement (generic).** The transducer must be active during the same developmental window in
which the Vmem-setting channel controls growth. That window is the late outgrowth phase, lasting
days to weeks. Individual Ca²⁺ events last seconds to minutes, so growth control must integrate
events across that window rather than respond to any single one.

**Check (measured).**
- **S2.** Astemizole at 500 nM from 7 to 30 dpa "fully suppressed excessive *loft2/+* fin outgrowth".
  Starting at 6 dpa worked as well as treatment throughout regeneration. Early-only treatment could
  not be tested because of astemizole's half-life, so the channel requirement is shown for the late
  window.
- **S1.** Cav block from 5 to 28 dpa (cilnidipine) caused overgrowth, so Cav activity restrains
  growth during the same late window. In vivo Ca²⁺ events had "variable duration and oscillatory
  pattern" across 5–10 min movies, so a single event lasts minutes or less while growth spans weeks.

**Gap (scope).** S1 could image Ca²⁺ only up to about 5 dpa because *tph1b:GCaMP6s* expression was
lost after that. Ca²⁺ fluxes have therefore not been **observed** during the 7–30 dpa window where
Kcnh2a acts. The late-window Cav requirement rests on cilnidipine, an L/N-type blocker, not on the
T-type *cacna1g* mutant. The overlap is satisfied by pharmacology, not by direct observation.

## C4 — tissue · spatial — **satisfied** (at compartment resolution, not single-cell)

**Requirement (generic).** The Vmem-setting channel and the transducer must act in the same cells,
or within electrically coupled range of each other: the intra-ray fibroblast-lineage mesenchyme or
blastema. The growth effect must be local to the rays carrying the perturbation, not systemic.

**Check (measured).**
- **S2.** In transplantation chimeras, "All overgrown chimeric rays contained EGFP+ intra-ray
  mesenchymal cells". Chimeras with epidermis only were normal. Mosaic CRISPR fins showed
  regionalised overgrowth.
- **S3.** *kcnk5b* overexpression in mesenchymal fibroblasts was sufficient for outgrowth.
  DsRed-positive mesenchyme correlated with overgrowth in 89.2% of cases (N=37). Chimeras gave local
  overgrowth only, in 29 of 120 fish, never global.
- **S1.** *cacna1g* and *cacna1c* are expressed in fibroblast-lineage blastema cells, and *cacna1ba*
  in the distal blastema.

**Gap (scope).** No source shows *kcnh2a*/*kcnk5b* and *cacna1g* co-expressed in the **same cell**.
The match is at the level of the intra-ray mesenchyme/blastema compartment. I set no numeric
length-scale bound because no source gives a coupling length or a co-localisation distance (`unknown`).

## Constraints not written

I did not write `energetic` or `conservation` constraints. I found no measured ionic flux,
pump-capacity or ATP number for fin mesenchyme that would make one checkable. Writing one would have
produced a constraint I could only mark `open` with no prospect of a measured check from the sources
in hand.

---

```swarm-entail
{"source_claim": 242, "source_scale": "cell",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "A protein whose activity depends on membrane voltage must be expressed in fin intra-ray mesenchyme or its blastema derivatives, and its loss must alter ray outgrowth",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Voltage-gated Ca2+ channels: cacna1g (T-type) and cacna1c (L-type) in fibroblast-lineage blastema cells, cacna1ba (N-type) in distal blastema (RNAscope). cacna1g loss-of-function alleles b1477/b1478 reduce in vivo Ca2+ fluxes and give 'extraordinarily long' regenerated fins (P<0.0001); 5 uM cilnidipine 5-28 dpa causes overgrowth (P=0.0004)",
      "satisfied_evidence": "measured",
      "note": "Le Bleu et al. 2025 Development 152(23):dev204739, PMC13078715 (full-text, machine-summarised). Contradicts the GXL 0/35 result. Not shown: that this channel reads the Vmem set by kcnk5b/kcnh2a; S1 measured no Vmem and did not image alf/longfin fish. Competing non-voltage model (intracellular K+ -> IP3R ER Ca2+ release; plasma-membrane Ca2+ channel block had no effect on shha) in pectoral fin buds: Jiang et al. 2024 PLoS Biol 22(3):e3002565 (full-text, machine-summarised); Yi et al. 2021 eLife 10:e60691 (search-summary)"},
    {"target_scale": "protein", "kind": "range",
      "statement": "Resting membrane potential of fin mesenchyme, and the shifts produced by growth-altering K+-channel mutants, must lie inside the voltage window where the transducer's steady-state activity changes",
      "quantity": "absolute in vivo Vmem of fin intra-ray mesenchyme vs. transducer window (human Cav3.1 window derived from measured Boltzmann parameters)",
      "lo": -82, "hi": -50, "units": "mV",
      "status": "unsatisfied",
      "satisfied_by": "No absolute fin Vmem found. Window bounds are DERIVED by me (half-max of activation x inactivation product, peak -69 mV) from MEASURED human Cav3.1 in HEK-293: act V1/2 -44.6 mV k 5.8, inact V1/2 -77.7 mV k -5.0. Zebrafish Cacna1g gating: unknown. Fin-side data are relative only: DiSBAC2(3) in juvenile fins shows alf depolarised, opposite to the oocyte hyperpolarisation toward -90 to -100 mV (Perathoner 2014); DiSBAC2(3) photon counts in fin buds (Jiang 2024); no Vmem in Le Bleu 2025 or Stewart 2021",
      "satisfied_evidence": "unknown",
      "note": "Baumgart et al. 2008 PLoS One 3(8):e2976 Table 1 (full-text, machine-summarised); Perathoner et al. 2014 PLoS Genet 10(1):e1004080 (full-text, machine-summarised). Negative scope: one extended web search (zebrafish fin membrane potential / voltage imaging / mesenchyme / kcnk5b / longfin) plus reading S1-S4 for any mV value in fin tissue; fin-fibroblast patch-clamp literature and GEVI fin lines not searched beyond that. Finding is 'looked, only relative dyes used', not 'nobody looked'. Not unsatisfiable: no absolute measured value contradicts the window. Sign disagreement between oocyte and in-fin dye data preserved"},
    {"target_scale": "tissue", "kind": "timescale",
      "statement": "The transducer must be active during the same late outgrowth window (days to weeks) in which the Vmem-setting channel controls growth; growth control must integrate seconds-to-minutes Ca2+ events over that window",
      "quantity": "overlap of channel-requirement window and transducer-requirement window",
      "lo": 7, "hi": 28, "units": "days post-amputation",
      "status": "satisfied",
      "satisfied_by": "Kcnh2a requirement: astemizole 500 nM 7-30 dpa fully suppresses loft2/+ overgrowth (start at 6 dpa as effective as throughout). Cav requirement: cilnidipine 5-28 dpa causes overgrowth. Individual Ca2+ events oscillatory/variable within 5-10 min movies",
      "satisfied_evidence": "measured",
      "note": "Stewart et al. 2021 Development 148(11):dev199384 PMC8217709; Le Bleu et al. 2025 (both full-text, machine-summarised). lo/hi is the intersection of the two treatment windows. Gap: Ca2+ fluxes were imaged only up to about 5 dpa (tph1b:GCaMP6s lost after), so not observed in the overlap window; late Cav requirement rests on an L/N-type blocker, not the T-type cacna1g mutant"},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "The Vmem-setting channel and the voltage transducer must act in the same cell compartment (intra-ray fibroblast-lineage mesenchyme/blastema) or within electrically coupled range, and the growth effect must be local to perturbed rays",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "kcnh2a acts autonomously in intra-ray mesenchyme lineage (all overgrown chimeric rays contained EGFP+ intra-ray mesenchyme; epidermis-only chimeras normal); kcnk5b overexpression in mesenchymal fibroblasts sufficient (89.2%, N=37), local not global overgrowth (29/120 chimeras); cacna1g/cacna1c in fibroblast-lineage blastema cells",
      "satisfied_evidence": "measured",
      "note": "Stewart et al. 2021; Perathoner et al. 2014; Le Bleu et al. 2025 (all full-text, machine-summarised). Satisfied at compartment resolution only: same-cell co-expression of K+ channel and Cav not shown in any source read; coupling length scale unknown, so no numeric bound given"}
  ]}
```
