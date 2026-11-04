# S42 (cell scale) — Is there a demonstrated route from membrane potential to fin-ray growth RATE?

Project: `zebrafish-flight`. Subproblem C4. Searches run 2026-11-04.

---

## 1. The question, restated precisely

The project's bioelectric chain, as cited elsewhere in this work, runs:

> K⁺ channel allele → change in membrane potential (V_mem) → change in osteoblast/mesenchymal
> behaviour → change in fin ray growth rate → change in final fin length.

Every citation the project currently carries attaches to the **two ends** of that chain: a channel
genotype (or a channel-blocking drug) at one end, and a **final, endpoint fin length** at the other.
C4 asks whether the **middle junction** — *V_mem change → ray growth rate change* — has ever been
measured as a junction, i.e. whether anyone has (a) imposed or recorded a membrane-potential change
and (b) measured a **rate** (length per unit time) of **bony fin-ray** elongation, with an effect
size.

The numbers that make this hard:

- **Rate vs. endpoint are not interchangeable here, and the field's own data proves it.** In the
  *longfin^t2* (`loft2`) mutant, overgrowth arises from a *longer* outgrowth period, not a faster
  one: "Wild-type and *loft2* fish had indistinguishable maximal growth rates reached between 3 and
  5 dpa" (Stewart et al. 2021, full-text partial). So a doubled final fin length in this mutant
  corresponds to a **~0 % change in peak growth rate**. Any design that assumes length ∝ rate is
  calibrated against the wrong variable.
- **The one readout that looks like a rate is a spatial proxy.** Fin-ray *segment length* (the
  distance between bone joints) is what the optogenetic experiments report. A segment-length change
  can be produced either by changing elongation rate at a fixed joint-laying clock, or by changing
  the clock at a fixed rate. Nothing read here separates those. *(This disambiguation is my
  inference, not a claim made by any author cited.)*
- **No author cited here reports a fin V_mem in millivolts.** Not one of the nine studies read gives
  a resting or manipulated membrane potential, in mV, for any cell in a zebrafish fin — larval,
  bud, or adult. The mV values that exist are from *Xenopus* oocytes expressing the fish channel
  (clamped at −80 mV; Daane et al. 2018) or from HEK293T cells (Yi et al. 2021). Two of the author
  groups say so explicitly, in their own words (see §2).

---

## 2. What is measured

Read-level key: `full-text (partial)` = fetched the open-access full text, which exceeded the
fetch window; approximately the first 100 000 characters were read and **figure source data /
supplementary tables were not read**. This matters: in several of these papers the authors state
that numeric effect sizes live only in the figures.

### 2a. Direct manipulation of membrane potential (not channel genotype)

| Study | Year | Manipulation of potential | Readout | Numbers reported | Tissue | Read-level |
|---|---|---|---|---|---|---|
| Aramaki & Kondo, bioRxiv 10.1101/2024.03.27.587111 | v1 2024-03-27; page lists v2 posted 2026-08-24 | **Optogenetic**: ChR2D156C ("ChR2-XXL"), blue-light-gated cation channel, as `Tg(krt4:ChR2D156C)` (keratinocytes) and `Tg(5x osx:ChR2D156C)` (osteoblasts) | Fin length (FL/SL) and **fin-ray segment length** (V3 ray, unbranched proximal segments, normalised to WT = 100); regeneration time course in Fig. 4 | **No numeric effect sizes in the main text.** Group sizes n = 5–7 (Fig. 5, the optogenetic figure); Student's or Welch's *t*-test, P < 0.05. Regeneration: transgenics "matched controls until 8 dpa," rate "maintained until 16 dpa" while controls declined — **described qualitatively, no numeric rates** | Adult caudal fin, bony rays | full-text (partial) |
| Liu, Nerli, Duclut, Vishen, Berbee, Kaufmann, Ponce, Arrenberg, Jülicher, Mateus — *Sci Adv* 12(6):eaec0687, doi 10.1126/sciadv.aec0687 | 2026 | **Pharmacological depolarisation**: 135 mM KCl, 1 h or overnight; plus heat-shock VSP (*tpte*) overexpression; FK506 10 µM; Gap27 0.5 mM | **V_mem imaged directly** with Voltron2 + JF552; Ca²⁺ with GCaMP6f; EdU⁺ proliferation; finfold length at 3 dpa and 5 dpf | Depolarisation detectable **100 ms** post-injury; decay length **206 ± 48 µm (apical), 187 ± 24 µm (basal)**; Ca²⁺ front reaches **118.4 ± 14.3 µm**, D = 1677 ± 170 µm²/s. **KCl on uncut larvae → "10 % length increase"; VSP-OE → "similar 10 % finfold length increase."** Proliferation peaks 1–3 h and 7–9 h post-amputation. **No mV value for the depolarisation** (reported as −ΔF/F only) | **Larval caudal finfold — no bony rays** | full-text (partial) |
| Jiang, Zhao, Sun, Song, Yi, Xiong, … Antos — *PLoS Biol* 22(3):e3002565 | 2024 | **Pharmacological**: Na⁺-channel inhibitors vinpocetine 10 µM and dibucaine 40 µM, 4 h, which reduced baseline depolarisation and blocked the Kcnk5b-induced increase | **V_mem imaged** with DiSBAC₂(3) (photon counts per pixel, FLIM/TCSPC); fin **bud area** normalised to eye area at 48 hpf | Depolarisation lowest at 32 hpf, highest at 48–56 hpf; 6 points × 4 bud locations averaged; ≥15 embryos per repeat. **No mV values. No percentages or fold-changes for the growth effect in the text** (in S5 Data, not read) | **Embryonic pectoral fin bud — no rays** | full-text (partial) |
| Le Bleu, Kioussi, Henner, Lewis, Stewart, Stankunas — *Development* 152(23):dev204739 | 2025 | **80 mM KCl depolarisation of isolated 5 dpa fin cells** (*in vitro*), Ca²⁺ read with GCaMP6s; *in vivo* cilnidipine 5 µM, 4 h/day, 5–28 dpa | Ca²⁺ flux; fin length normalised to body length; outgrowth **rate as a derived curve** (Fig. 6B) | Cilnidipine overgrowth P = 0.0004 (n = 8 DMSO vs 7 drug); *cacna1g^b1477* P < 0.0001 at 46 dpa; rate curve n = 14/genotype. **"The maximum rate of outgrowth peaked at ~3–4 dpa for both" — no units, no numeric rate.** Group means not in text. V_mem **not** measured; the KCl step is *in vitro* and its resulting potential is not reported | Adult fin (rays) *in vivo*; dissociated cells for the KCl step | full-text (partial) |

### 2b. Channel genotype / channel drug → endpoint length or rate (the correlations C4 asks us to distinguish from)

| Study | Year | Manipulation | Readout | Key numbers | V_mem measured in fin? | Read-level |
|---|---|---|---|---|---|---|
| Perathoner, Daane, Henrion, Seebohm, Higdon, Johnson, Harris — *PLoS Genet* 10:e1004080 | 2014 | *another longfin* (`alf`) = **gain-of-function `kcnk5b`**; mosaic transgenics | Final fin and barbel size; segment number | Increased K⁺ conductance shown by **electrophysiology in *Xenopus* oocytes**; channel acts in fin/barbel mesenchyme; `alf` shows **no increase in segment number** | **No** — oocytes only | search-summary (full text not opened) |
| Yi, Spitters, Al-Far, Wang, Xiong, Cai, Yan, Guan, Wagner, El-Armouche, Antos — *eLife* 10:e60691 | 2021 | `Tg[hsp70:kcnk5b-GFP]`, 10-min heat-shock pulses (single, or daily during regeneration) | Gene transcription; fin-to-body ratios; lengths | **No growth rate with units anywhere in the text read.** Patch clamp and KIRIN K⁺ FLIM were done in HEK293T cells. Replicates given as "three or more experiments," not per-animal n | **No** | full-text (partial) |
| Daane, Lanni, Rothenberg, Seebohm, Higdon, Johnson, Harris — *Sci Rep* 8:10391 | 2018 | FK506 100 nM (calcineurin inhibitor) in fish water, refreshed every 2 d; `kcnk5b^−/−`; `alf`; `sof` (*cx43*) | **"Fin growth rate was measured for individual fish as the slope of the linear growth regression line over time"** — the only clean rate metric found | F(2,23) = 27.89, P < 0.0001 (genotype × treatment); WT FK506 vs DMSO P = 0.0013; `sof` P < 0.0001; `kcnk5b^−/−` FK506 vs WT FK506 P = 0.0013. **No absolute rate values or units in the text** (figures not read). Oocyte clamp reference potential −80 mV | **No** — "The membrane potential was clamped at a reference potential of −80 mV" refers to *Xenopus* oocytes | full-text (partial) |
| Stewart, Le Bleu, Yette, Henner, Robbins, Braunstein, Stankunas — *Development* 148(11) | 2021 | `longfin^t2` cis-ectopic `kcnh2a`; **astemizole 500 nM**, 7–30 dpa, refreshed every 48 h | Growth fitted to a logistic curve; rate fitted to exponential decay after peak | Astemizole "fully suppressed excessive `loft2/+` fin outgrowth to wild-type levels," P < 0.0001; n ≥ 12 for the growth time course (not for the drug arm). **No numeric rate values in text.** Overgrowth attributed to **prolonged outgrowth period, not faster rate** | **No** — authors write: "Key future steps include characterizing membrane potentials and putative depolarizing signals" | full-text (partial) |
| Seaver, Li, Iovine — *Dev Biol* 528:57–65 | 2025 | `hsp70:Xl-kcna5-T2A-GFP`, systemic heat shock 37 °C × 1 h at 3 dpa | Regenerate length at 7 dpa; segment length (3rd dorsal ray, 1st→2nd joint); H3P⁺ mitoses; *evx1* rays | **Regenerate length unchanged: P > 0.99 (Fig. 2D), P = 0.96 (Fig. 5D). Mitoses unchanged at 4 and 7 dpa.** Segment length increased, P < 0.0001 (WT bg), P < 0.01 in `sof^b123`. *evx1*⁺ rays reduced P < 0.0001; *cx43* mRNA unchanged P = 0.26. **No µm/day, single timepoint only.** Means/SDs/n not in text | **No** — authors state that demonstrating ΔV_m as the signal is future work | full-text (partial) |
| Silic, Wu, Kim, Golling, Chen, Freitas, Chuby… — *Genetics* (2020), "Potassium channel-associated bioelectricity of the dermomyotome determines fin patterning in zebrafish" | 2020 | — | — | Not examined beyond the title/listing | unknown | listing |

### 2c. Disagreement to preserve, not average

1. **Sign of the potential change downstream of K⁺ gain-of-function.** Perathoner et al. 2014
   interpret `kcnk5b` gain-of-function as **hyperpolarising** (increased K⁺ conductance, oocyte
   electrophysiology). Jiang et al. 2024 report that *in vivo* in the pectoral bud, Kcnk5b
   "promotes **depolarization** via Na⁺ channels," and that this **depolarisation is required** for
   Kcnk5b-enhanced growth. These are opposite signs for the same gene product. I am not resolving
   them; both are the authors' own claims, in different tissues, with different methods.
2. **Sign of the growth effect of depolarisation.** Jiang et al. 2024 (bud) and Liu et al. 2026
   (larval finfold, +10 % with 135 mM KCl) have depolarisation **promoting** growth. Le Bleu et al.
   2025 have depolarisation-driven voltage-gated Ca²⁺ influx **restraining** adult regenerative
   outgrowth, such that blocking it with cilnidipine causes **overgrowth** (P = 0.0004).
   Developmental and regenerative contexts disagree in sign.
3. **Internal dose disagreement inside one paper.** Le Bleu et al. 2025: amlodipine is 500 nM in the
   Fig. 2 legend and 5 µM in Methods; PD17132 is 500 nM in the legend and 2 µM in Methods. The
   paper does not explain the discrepancy, and I did not resolve it.
4. **Title/version disagreement for the key preprint.** Europe PMC indexes
   doi 10.1101/2024.03.27.587111 as "Cell-type-dependent bioelectric regulation of fin size and
   fin-ray segment length in zebrafish" (2024, **no PMCID**); a search result rendered the indexed
   PDF title as "Independent size regulation of bones and appendages in zebrafish." I could not
   confirm a peer-reviewed version exists (see §5 for the search scope).

---

## 3. What I computed

**All of §3 is my arithmetic on other people's measured numbers. None of it is an observation.**

**(a) The field's mV figures are extracellular, and do not convert to a transmembrane potential.**
Liu et al. 2026 quote literature wound currents of **50–500 mV/mm** and measure an apical
depolarisation decay length of **206 ± 48 µm**. Treating the quoted field as uniform over one decay
length:

```
50 mV/mm × 0.206 mm =  10.3 mV
500 mV/mm × 0.206 mm = 103   mV
```

So the only mV-scale numbers in the whole literature read here bracket **~10–100 mV of
*extracellular potential drop* across one measured decay length** — a 10× range, and the wrong
quantity. Assumptions: uniform field, no geometry correction, and the cited field-strength range
taken as applicable to the zebrafish larval finfold (the paper quotes it as general wound-current
literature, not as its own measurement). **An extracellular field drop is not a cell's ΔV_mem**;
these two differ by the tissue's and membrane's impedance distribution, which no source read here
reports. This computation therefore sets an order of magnitude, and cannot substitute for the
missing measurement.

**(b) The one directly-potential-driven growth effect size, converted to a rate — and why that
fails.** Liu et al. 2026 report a **10 % finfold length increase** under 135 mM KCl and a similar
10 % under VSP overexpression, measured as an endpoint (3 dpa, or 5 dpf). If — and only if — the
increment accrued linearly over a treatment window of N days, the implied mean rate difference is
10 %/N per day: 10 %/day for N = 1, 5 %/day for N = 2, 3.3 %/day for N = 3. **The paper reports an
endpoint, not a growth curve, so N is not fixed by the data and the rate is not recoverable.** The
spread across plausible N is 3×. This is the arithmetic demonstration that an endpoint
measurement does not contain a rate.

**(c) Chain-completeness tabulation (a count, not a measurement).** Of the 9 studies read, scoring
each against the three requirements of C4:

| Requirement | Count satisfying | Which |
|---|---|---|
| V_mem imposed or recorded by a non-genotype method | 4 | Aramaki & Kondo (imposed, optogenetic); Liu 2026 (imposed + recorded); Jiang 2024 (imposed + recorded); Le Bleu 2025 (imposed, *in vitro* only) |
| V_mem reported in mV for any zebrafish fin cell | **0** | — |
| **Bony fin-ray** growth **rate** quantified with units and an effect size | **0** | — |
| All three, in one experiment | **0** | — |

The intersection of "potential manipulated directly" and "bony ray growth rate measured with an
effect size" is **empty** in everything I read.

---

## 4. The answer

**Evidence level: `literature`** (a negative finding established by literature search, not a
measurement or a simulation of mine).

**No.** As of this search, there is **no published, peer-reviewed experiment in zebrafish that
manipulates or measures a membrane-potential change and reports a resulting change in bony
fin-ray growth rate with a measured effect size.** The bioelectric chain the project relies on is
**inferential at exactly the junction C4 interrogates**, and must be labelled as such.

The three closest approaches, and precisely how each falls short:

1. **Aramaki & Kondo (bioRxiv, 2024/2026)** is the only study found that imposes a membrane-potential
   change *in the adult bony fin* by a method independent of channel genotype — optogenetically,
   with ChR2D156C in keratinocytes (`krt4`) and osteoblasts (`osx`) — and reads out fin size and
   **fin-ray segment length**. The authors' own claim is that "optogenetic manipulation demonstrated
   that membrane potential itself can regulate fin size" and segment length. It fails C4 on three
   counts: (i) **membrane potential was not measured** — the authors state that "membrane potential
   changes induced by the ion-channel manipulations were not directly measured in adult fin
   tissues," so the potential change remains inferred from ChR2's known conductance; (ii) the
   readouts are a **spatial endpoint** (segment length, FL/SL), with the regeneration time course in
   Fig. 4 described only qualitatively and **no numeric rate**; (iii) **no numeric effect size
   appears in the main text** (n = 5–7 for the optogenetic figure), and it is **a preprint with no
   PMCID** — I could not confirm peer review.
2. **Liu et al. (*Sci Adv*, 2026)** is the only study found that **both records membrane potential
   in fin tissue** (Voltron2) **and** imposes a depolarisation pharmacologically (135 mM KCl) with a
   **quantified growth effect (+10 % finfold length)**. It fails C4 because the tissue is the
   **larval caudal finfold, which has no bony rays**, the readout is an endpoint length plus EdU
   proliferation rather than a ray elongation rate, and the recorded depolarisation is reported as
   −ΔF/F with **no mV value**.
3. **Daane et al. (*Sci Rep*, 2018)** is the only study found that measures fin growth as a genuine
   **rate** — "the slope of the linear growth regression line over time." It fails C4 because the
   perturbations are a **calcineurin inhibitor (FK506, 100 nM)** and **channel genotypes**, not a
   potential manipulation; no potential was measured in fin; and the text reports only F- and
   P-values, with no absolute rate in any unit.

Two of the author groups concerned state the gap in their own words: Stewart et al. 2021 — "Key
future steps include characterizing membrane potentials and putative depolarizing signals";
Seaver et al. 2025 — demonstrating ΔV_m as the signal is future work.

---

## 5. What this does NOT establish

Read this as carefully as §4.

- **It does not establish that bioelectric control of ray growth is false.** It establishes that
  the specific junction is unmeasured. Converging genetic evidence across at least five independent
  loci (`kcnk5b`, `kcnh2a`, `kcna5`, `cx43`, `cacna1g`) and two independent pharmacologies
  (astemizole, cilnidipine) is substantial support for *some* ion-flux control of fin size. It is
  not a measurement of potential-to-rate coupling.
- **It does not establish that the Aramaki & Kondo optogenetic result is wrong.** It establishes
  that I could not verify a peer-reviewed version, could not extract numeric effect sizes from the
  text, and that the authors themselves did not measure the potential their tool imposes. If that
  preprint is published with a voltage measurement and a numeric growth-rate time course, **C4
  flips to `measured`** and this document is superseded.
- **It does not establish that a ray growth rate has never been measured.** Rates clearly exist in
  the field — Daane et al. fit growth-rate regressions; Stewart et al. fit logistic growth with
  exponential rate decay; Le Bleu et al. plot a derived outgrowth-rate curve (n = 14/genotype).
  What is absent is a rate measured **against a potential manipulation**. Furthermore, the numeric
  values of those rates almost certainly exist in figure panels and source-data files I did **not**
  read; my read level is `full-text (partial)` throughout, truncated at ~100 000 characters with
  figures and supplementary data unread. **A reader with figure-level access may well be able to
  extract µm/day values from Daane Fig. 1–2, Stewart Fig. 3, and Le Bleu Fig. 6B.** That would not
  by itself satisfy C4, because the manipulations in those figures are not potential manipulations.
- **It does not establish that segment length is uninformative about rate.** It establishes that no
  source read here separates a rate change from a joint-timing change. The claim that segment length
  conflates the two is **my inference** (§1), not an authors' claim.
- **It does not resolve the sign disagreement** (§2c). Depolarisation promotes growth in the
  embryonic bud (Jiang 2024) and larval finfold (Liu 2026), and restrains it during adult
  regeneration (Le Bleu 2025). For a flight-design chain that needs *more* ray growth, this
  unresolved sign is a first-order problem: the same manipulation may act in opposite directions in
  developing and regenerating adult fin, and nothing read here tells us which regime governs normal
  adult ray elongation.
- **It does not establish that the larval finfold result transfers to rays.** The larval finfold is
  an unossified fold; adult rays are segmented dermal bone with osteoblasts, joints, and
  intra-ray mesenchyme. The +10 % finfold number is a measurement in the wrong tissue for this
  project, and I have made no attempt to scale it.
- **Negative-search scope, stated explicitly.** The negative finding covers: Europe PMC REST
  searches on 2026-11-04 for `"fin ray" AND "growth rate" AND "membrane potential"` (9 hits, all
  examined by title; the 5 relevant ones are in §2),
  `zebrafish AND fin AND (channelrhodopsin OR "ChR2") AND (size OR growth)` (130 hits, first 8 by
  relevance examined), `zebrafish AND fin AND "resting membrane potential"` (96 hits, first 8
  examined), `zebrafish AND "fin regeneration" AND "voltage-sensitive dye"` (3 hits, all examined),
  `"fin-ray segment length"` (11 hits, all examined by title), `AUTH:"Aramaki" AND fin AND
  bioelectric` (1 hit), `optogenetic AND zebrafish AND fin AND "membrane potential"` (60 hits,
  first 8 examined); plus four web searches on the same terms. **The scope therefore does not
  include**: hits ranked below ~8th in the three large queries; any non-English literature; any
  work indexed only outside Europe PMC and the web index used; figure source data and supplements
  for every paper listed; and the full text of Perathoner et al. 2014 and Silic et al. 2020, which
  I have at `search-summary` and `listing` level only. `pubmed.ncbi.nlm.nih.gov` and
  `charlieduclut.github.io` did not resolve from this session and would need to be allowed in the
  session's network settings; I substituted the Europe PMC REST API and PMC, which served the same
  records.
- **It does not establish anything about mammals, *Xenopus*, or axolotl**, where the comparable
  measurement may exist. I did not search outside zebrafish.

---

## 6. What would change the answer

In descending order of decisiveness:

1. **The decisive experiment.** In an adult zebrafish caudal fin, impose a graded depolarisation on
   a known cell type — optogenetically (ChR2 variant) or pharmacologically — while (a) **recording
   V_mem in that cell type in millivolts**, with a calibrated genetically encoded voltage indicator
   or patch clamp on isolated fin cells, and (b) measuring **ray length at ≥4 timepoints** to
   extract **µm/day**, reporting a dose–response of rate on ΔV_mem with means, SDs and n. A single
   such experiment converts C4 from `literature`/inferential to `measured` and gives the project its
   first real transfer coefficient (µm·day⁻¹·mV⁻¹) instead of an inferred link.
2. **Peer-reviewed publication of Aramaki & Kondo with a voltage measurement and a numeric rate.**
   This is the cheapest path and may already be in progress; the optogenetic manipulation and the
   adult bony-ray readout are both already in hand. Adding a V_mem measurement in the targeted
   keratinocytes and osteoblasts, plus a ray-elongation time course with numbers, would close the
   junction.
3. **Reading the figure source data** of Daane et al. 2018, Stewart et al. 2021 and Le Bleu et al.
   2025 to recover absolute growth rates in µm/day. This would **not** satisfy C4 — the
   manipulations there are not potential manipulations — but it would supply the denominator the
   project needs to express any future ΔV_mem effect as a fractional rate change, and would convert
   several `no numeric effect size` entries in §2 to numbers.
4. **Any measurement that separates rate from duration under a potential manipulation.** Given that
   `loft2` overgrowth is a duration effect at **unchanged peak rate** (Stewart et al. 2021), a
   depolarisation experiment that reports only final length is uninterpretable for this project.
   Reporting the logistic fit's rate parameter *and* its duration parameter separately would settle
   which of the two bioelectric signalling controls — and the project's fin-area target depends on
   which.
5. **A resolution of the sign disagreement** by applying the same potential manipulation, with the
   same voltage readout, to embryonic bud, larval finfold, and adult regenerating ray in one study.
   Until then the project must carry both signs.

---

```swarm-result
{"subproblem": "S42", "evidence": "literature",
  "answer": "No peer-reviewed zebrafish experiment manipulates or measures a membrane-potential change and reports a resulting change in bony fin-ray growth rate with an effect size; the closest are an unrefereed optogenetic preprint that changed adult fin-ray segment length without measuring membrane potential or any rate (Aramaki & Kondo, bioRxiv 10.1101/2024.03.27.587111), a Sci Adv 2026 study that imaged depolarisation and measured a +10% larval finfold length increase in a tissue with no bony rays (Liu et al.), and a Sci Rep 2018 study that measured fin growth rate but perturbed calcineurin and channel genotype rather than potential (Daane et al.), so the project's bioelectric chain must be labelled inferential at the potential-to-rate junction.",
  "key_number": "0 peer-reviewed experiments pairing a membrane-potential manipulation or measurement with a bony fin-ray growth rate in um/day (searched 2026-11-04); the nearest quantified potential-driven growth effect is +10% larval finfold length under 135 mM KCl, wrong tissue",
  "blocked_on": "Figure source data and supplementary files for Daane 2018, Stewart 2021, Le Bleu 2025, Jiang 2024 and Aramaki & Kondo (read-level full-text partial, ~first 100k characters, figures unread), so no absolute growth rate in um/day could be extracted; full text of Perathoner 2014 (search-summary only) and Silic 2020 (listing only); confirmation of whether Aramaki & Kondo has a peer-reviewed version; pubmed.ncbi.nlm.nih.gov and charlieduclut.github.io did not resolve from this session and need allowing in the session network settings"}
```
