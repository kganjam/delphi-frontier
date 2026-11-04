# S11-D — Deepening S11: what is the real bioelectric mechanism controlling fin size?

**Date:** 2026-11-04 · **Status:** desk research. No experiment was run. Every number below is
labelled **measured** (someone recorded it), **calculated** (I computed it) or **assumed**.

## 0. What answer is being deepened

The recorded S11 answer handed to me was **empty**. I also found no S11 file in this repository.
Scope of that search: `grep -ril` for `S11`, `fin size`, `kcnk5`, `bioelectric` over the whole
working tree except `.git`. The only relevant hit was the Gemini triage row `bioelectric-fin-size`
in `findings/gemini-triage-267-problems.json`. That row gives the verdict
`not-resolvable-with-public-data`, confidence 0.85. It is a model's assessment, not a mechanism.

So I deepen the answer the current literature gives. Its strongest published statement is
Le Bleu et al. 2025 (below): *"'bioelectricity' for fin size control reflects voltage-modulated
Ca²⁺ fluxes in fibroblast-lineage blastemal cells that decelerate outgrowth."* Spelled out as the
chain the field uses, it reads:

> **C (canonical):** gain-of-function K⁺ channels (Kcnk5b in *alf*; ectopic Kcnh2a in *lof*)
> **hyperpolarise** fin fibroblast-lineage cells → less voltage-gated Ca²⁺ entry (Cav, notably
> Cacna1g) → less calcineurin activity → the outgrowth brake engages later → longer fins.

Le Bleu et al. state the hyperpolarisation link in their Discussion:
*"Gain-of-function K⁺ channels producing long-finned phenotypes then could act upstream of
calcineurin by **hyperpolarizing fibroblasts (as indicated for the alf/Kcnk5b K⁺ channel;
Perathoner et al., 2014)**."* That sentence is the authors' claim. The rest of this document
tests the input it cites.

## 1. The input the answer is most sensitive to

**The input:** the sign and size of the membrane-potential change (ΔVm) that the long-fin K⁺
alleles cause in the cells that set fin size, *in vivo*. The baseline Vm of those cells is needed
alongside it.

**The sensitivity, recomputed.** Script: [`S11_deepen_sensitivity.py`](S11_deepen_sensitivity.py).
All output is **calculated**. Its parameters are **assumed** and swept, except the ×2 conductance
factor, which comes from Perathoner 2014. The model uses a parallel-conductance Vm and a generic
T-type-like steady-state Ca²⁺ window current (activation² × inactivation × driving force). These
are not measured Cacna1g parameters for fish.

| baseline K⁺ fraction (assumed) | Vm₀ (calc.) | gK × 2 → Vm (calc.) | Ca²⁺ drive change (calc.) | C predicts |
|---|---|---|---|---|
| 0.30 | −27.0 mV | −41.5 mV | **+865 %** | shorter fin (wrong sign) |
| 0.50 | −45.0 mV | −60.0 mV | −49.5 % | longer fin |
| 0.70 | −63.0 mV | −74.1 mV | −84.1 % | longer fin |
| 0.90 | −81.0 mV | −85.3 mV | −71.2 % | longer fin |

Flipping the sign of ΔVm, with the baseline Vm₀ held fixed (calculated):

| Vm₀ | ΔVm = −10 mV (oocyte direction) | ΔVm = +10 mV (in vivo dye direction) |
|---|---|---|
| −80 mV | Ca −95 % → longer fin ✔ | Ca +834 % → **no long fin** |
| −60 mV | Ca −75 % → longer fin ✔ | Ca +106 % → **no long fin** |
| −40 mV | Ca +53 % → **no long fin** | Ca −79 % → longer fin |

**What this shows (calculated):**

- A factor of two in the *magnitude* of the conductance change does not decide C.
- Two other inputs do: the **sign** of ΔVm, and **which side of the Ca²⁺ window peak the cell
  rests on**. Under the assumed parameters the peak sits at about −48 mV, and it moves from −38 to
  −58 mV across the sweep.
- Reversing the sign of ΔVm reverses C's prediction at every baseline tested.
- A factor of 0.3 → 0.5 in the baseline K⁺ fraction also reverses it.

The number that must be right, then, is a **sign**, together with a baseline voltage. Neither has
been measured in fin fibroblasts.

## 2. How well is that input established?

| Source | What was measured | System | Direction | Kind | Read-level |
|---|---|---|---|---|---|
| Perathoner et al. 2014, *PLoS Genet* 10:e1004080, PMC3894163 | Two-electrode voltage clamp; W169L and F241Y Kcnk5b give *"an almost two-fold increase in K⁺ conductance"* and shift oocyte Vm *"towards −90 to −100 mV"* | ***Xenopus* oocytes**, 4 ng cRNA, n = 5–26 | **hyperpolarising** | measured, heterologous | full-text (fetched via tool; first 100 k of 118 k chars) |
| same paper, Fig. S4 | DiSBAC2(3) fluorescence in juvenile fins (16–18 mm SL). Authors: WT shows *"hyperpolarization localized to discrete regions"*; *alf* shows *"high levels of depolarization across the fin with variable patterns in different tissues"*. p < 0.001, N = 21–23, 150 mM KCl positive control. DiSC3(5) was *"uninformative"* | **fish fin, in vivo**, whole fin, all tissues | **depolarising** | measured, relative fluorescence proxy, no mV | full-text (same) |
| Jiang et al. 2024, *PLoS Biol* 22:e3002565 | DiSBAC2(3) photon counts; *"overexpression of kcnk5b-mCherry significantly increased depolarization"*, dependent on Na⁺ channels (vinpocetine, dibucaine). The authors **propose, without measuring it**, that hyperpolarisation comes first and then activates Na⁺ channels | embryonic **pectoral fin bud**, heat-shock overexpression (not the *alf* allele), N ≥ 3 | **depolarising** | measured, relative proxy, no mV | full-text (first 100 k of 211 k chars) |
| Daane et al. 2018, *Sci Rep* 8:10391, PMC6039437 | FK506 lowers Kcnk5b conductance in oocytes; *kcnk5b*⁻/⁻ suppresses FK506 overgrowth (p = 0.0013). **No fin Vm measured** | oocytes, fish | — | measured (conductance only) | full-text |
| Yi et al. 2021, *eLife* 10:e60691 | HEK293T current density and KIRIN K⁺ FLIM. The S345 calcineurin site regulates conductance. **No Vm measured**, and no pore-dead control in the text I read | cell lines, fish | — | measured (current, [K⁺]ᵢ) | full-text (both halves, via tool) |
| Stewart et al. 2021, *Development* 148:dev199384, PMC8217709 | *lof* = cis-ectopic *kcnh2a* in fibroblasts. Astemizole 500 nM suppresses overgrowth. Longer growth period, same peak rate. **No Vm measured**: *"Key future steps include characterizing membrane potentials"* | fish fin regeneration | — | measured (phenotype) | full-text (first 100 k of 120 k chars) |
| Le Bleu et al. 2025, *Development*, doi:10.1242/dev.204739, PMC13078715 | GCaMP6s in fibroblast lineage. 80 mM KCl depolarisation of cultured fin fibroblasts triggers Ca²⁺ spikes (39 % excitable, 70/109; cilnidipine 4 %, 4/103). *cacna1g*⁻/⁻ gives long fins. **No Vm measured.** The hyperpolarisation link is attributed to Perathoner 2014 | fish, primary fibroblasts | (cites hyperpolarising) | measured (Ca²⁺); the Vm link is a citation | full-text (NCBI efetch XML, keyword-scanned, not read end to end) |
| Aramaki & Kondo, bioRxiv 10.1101/2024.03.27.587111 v2 (2026-08-24) | ChR2D156C (*"a blue-light-gated cation channel"*). In keratinocytes it *"selectively reduced fin size"*; in osteoblasts it shortened segments. n = 5–7. **No Vm measured**: *"not directly measured in adult fin tissues"*. The W169L direction is described as *"previously been proposed to hyperpolarize"* | fish, krt4 / osx promoters | perturbation, not measurement | measured (phenotype); preprint | full-text (v2 HTML, via tool) |

**Verdict on the input.** In vivo, in fin tissue, at the cell types that matter, the claim that
long-fin K⁺ alleles hyperpolarise cells is **an assumption that has been repeated until it reads as
measured**.

- The only direct measurement of hyperpolarisation is in *Xenopus* oocytes. An oocyte with a
  dominant overexpressed K⁺ leak conductance will sit near E_K almost by construction. This is my
  inference, not the authors' claim.
- **Both in vivo measurements in zebrafish fin tissue report depolarisation, not
  hyperpolarisation.** They are Perathoner 2014 Fig. S4 (*alf*, whole juvenile fin) and Jiang 2024
  (Kcnk5b overexpression, embryonic bud). Both groups explain this as a secondary effect
  (Perathoner: *"we cannot exclude that this, in turn, triggers a depolarization"*; Jiang: via Na⁺
  channels), and neither tested that explanation by measuring the primary step.
- The citation chain carries the sign forward without re-checking it:
  - Le Bleu 2025 cites Perathoner 2014 for *"hyperpolarizing fibroblasts"*.
  - Aramaki 2026 says *"proposed to hyperpolarize"*.
  - Perathoner's own in vivo data point the other way, and none of the three resolved fibroblasts.

  This is my inference from reading all three.

**Disagreement to preserve. Neither side is averaged away:**

1. **Sign.** Oocyte TEVC says hyperpolarising (measured, heterologous). Fin DiSBAC2(3) says
   depolarising (measured, proxy, in vivo). A proxy objection applies to the second: DiSBAC2(3) is
   a slow redistributive dye read as whole-fin mean intensity. Uptake differences between tissues
   could produce a genotype difference without any per-cell Vm difference. This is my inference.
   The authors used a KCl positive control but report no tissue-resolved quantification.
2. **Cell type.**
   - Stewart 2021 and Le Bleu 2025 place size control in the **fibroblast lineage**: ectopic
     Kcnh2a there is sufficient, and Cacna1g Ca²⁺ dynamics occur there.
   - Aramaki 2026 finds the **keratinocyte** compartment primarily sets fin size when it is
     manipulated with kcnk5bW169L or ChR2.

   These are not necessarily contradictory, since different alleles and stages were used, but no
   source reconciles them.
3. **Direction of depolarisation's effect.** Aramaki find that ChR2 depolarisation *shrinks* adult
   fins. Jiang find that depolarisation is *required* for Kcnk5b-enhanced embryonic bud growth.
   Aramaki's own caveat notes this opposite-sign result is stage- and tissue-dependent.

## 3. Improving the input

- **Primary source found and read.** The hyperpolarisation claim traces to Perathoner 2014 Fig. 5
  (oocytes). The same paper's Fig. S4 is the **only in vivo fin Vm measurement for a long-fin
  allele that I found, and it reports depolarisation.**
- **The real quantity is absolute resting Vm, and ΔVm, of fibroblast-lineage (and keratinocyte)
  blastema cells in *alf*/+, *lof*/+ and WT regenerating fins, during outgrowth (about 5–21 dpa).**
  Status: **unknown**.
  - Search scope: Europe PMC and web search, English. Query terms: kcnk5b, kcnh2a, longfin, fin
    regeneration, membrane potential, GEVI, voltage dye, patch clamp, 2014–2026.
  - Full-text scans: Stewart 2021, Le Bleu 2025, Aramaki 2026 v2, Yi 2021, Daane 2018.
  - None reports an mV value for fish fin cells. Two of those papers state outright that it is
    unmeasured.
  - Controls on the search: a positive control (the exact Le Bleu title in Europe PMC) returned
    the record. A must-fail nonsense query returned 0 hits.
- **Measurements that would settle it.** The cost and time figures are my estimates, not sourced.
  1. **Cheapest, weeks.** Perforated-patch or sharp-electrode resting Vm of primary regenerating-fin
     fibroblasts from *alf*/+, *lof*/+, *cacna1g*⁻/⁻ and WT siblings. The culture method already
     exists (Le Bleu 2025 Methods: L-15 + 10 % FBS, 30 °C, Tyrode's). One electrophysiologist,
     about 1–2 months, under about US$10 k in consumables. Limitation: culture can reset Vm, so this
     settles the sign in vitro only.
  2. **Decisive, months.** A ratiometric or lifetime-calibrated GEVI under the fibroblast driver
     Le Bleu used (`tph1b`), plus a `krt4` keratinocyte version, crossed into *alf*/+ and *lof*/+.
     Image 5–21 dpa blastemas, with KCl and valinomycin calibration to convert to mV. This means
     building a transgenic line and imaging it: about 9–15 months for one postdoc, roughly
     US$100–200 k fully loaded.
  3. **Causal test.** Clamp Vm independently of the channel genotype. For example, express a
     **pore-dead** Kcnk5b W169L (no conductance) and check that the overgrowth disappears. Then
     add a light-gated K⁺ channel in `tph1b` cells to hyperpolarise WT fibroblasts and test whether
     that alone causes overgrowth. Le Bleu's model predicts it should, and Aramaki's ChR2 data
     predict it might in keratinocytes.

## 4. Recomputing the conclusion with the improved input

Improved input: **ΔVm in vivo is not measured in fin fibroblasts. The only in vivo fin-tissue
readouts (two studies, one dye) show depolarisation in relative units.**

I fed that sign into the sensitivity model (calculated). C predicts long fins only if the
resting fibroblast Vm lies *above* the Ca²⁺ window peak, on the depolarised flank. The fibroblasts'
own excitability data cannot place that baseline either way. KCl depolarisation triggers spikes in
39 % of cultured cells, which suggests a negative resting Vm, but that is my inference and not a
measurement.

What survives, and what does not:

- **Stands** (measured, independent of the sign question): the Ca²⁺ → calcineurin brake.
  - *cacna1g* loss of function gives long fins.
  - FK506 gives long fins, and that requires *kcnk5b*.
  - L/N-type blockers cause overgrowth.
  - Ectopic Kcnh2a acts during outgrowth only.
- **Supported, at perturbation level, cell type disputed:** membrane voltage, or at least cation
  influx, can change adult fin size (Aramaki ChR2 in keratinocytes; preprint). ChR2 is a cation
  channel, so this does not isolate voltage from ion flux. That is my inference from the authors'
  own description.
- **Falls as an established premise:** *"the long-fin K⁺ alleles act by hyperpolarising
  fibroblasts."* It rests on an oocyte measurement. The two in vivo measurements contradict it. It
  survives in the literature by citation, not by measurement.

**Verdict: FALLS.** The canonical mechanism "K⁺ gain-of-function hyperpolarises fibroblasts,
which lowers Cav Ca²⁺ and calcineurin" is not established. Its load-bearing input (the in vivo
sign of ΔVm) is unmeasured in the relevant cells, and the only in vivo readouts point the other
way. The downstream Ca²⁺/calcineurin brake stands on its own evidence. How the K⁺ channels couple
to it remains unresolved. This is a negative result: it does not show the hyperpolarisation model
is wrong. It shows the model has not been tested where it would need to be.

```swarm-result
{"subproblem": "S11-D", "evidence": "measured-heterologous + measured-proxy-in-vivo (conflicting); in-vivo fibroblast Vm unmeasured", "answer": "The Ca2+/calcineurin brake on fin outgrowth stands (cacna1g LOF, FK506, Cav blockers), but its claimed coupling to long-fin K+ channels via fibroblast hyperpolarisation falls as an established premise: hyperpolarisation was measured only in Xenopus oocytes, the only in vivo fin readouts (DiSBAC2(3), Perathoner 2014; Jiang 2024) show depolarisation, and fibroblast resting Vm has never been measured.", "key_number": "in vivo fin-cell dVm for alf/lof: unknown in mV; sign by DiSBAC2(3) in whole fin = depolarising (relative fluorescence, p<0.001, N=21-23); oocyte dVm = toward -90 to -100 mV with ~2x gK", "verdict": "falls", "depends_on": ["Perathoner2014-PMC3894163-Fig5: alf Kcnk5b W169L/F241Y ~2x K+ conductance, oocyte Vm toward -90 to -100 mV (measured, heterologous)", "Perathoner2014-PMC3894163-FigS4: alf fins depolarised by DiSBAC2(3), N=21-23 (measured, proxy)", "Jiang2024-PLoSBiol-e3002565: Kcnk5b overexpression depolarises fin bud cells via Na+ channels (measured, proxy, embryonic)", "Daane2018-PMC6039437: FK506 lowers Kcnk5b conductance; kcnk5b-/- suppresses FK506 overgrowth", "Yi2021-eLife-60691: calcineurin regulates Kcnk5b via S345; no Vm measured", "Stewart2021-PMC8217709: lof = cis-ectopic kcnh2a in fibroblasts, prolongs outgrowth period; no Vm measured", "LeBleu2025-PMC13078715: cacna1g-/- long fins; KCl-evoked Cav-dependent Ca2+ spikes in fin fibroblasts (39% 70/109); hyperpolarisation link is a citation to Perathoner2014", "Aramaki-Kondo-bioRxiv-2024.03.27.587111v2: ChR2D156C depolarisation in keratinocytes reduces fin size, n=5-7, preprint; no Vm measured", "assumption: DiSBAC2(3) whole-fin intensity reflects per-cell Vm", "assumption: Ca2+ window-current non-monotonicity (generic T-type Boltzmann parameters, not measured for zebrafish Cacna1g)", "unknown: resting Vm of fin fibroblast-lineage blastema cells", "repo: findings/gemini-triage-267-problems.json#bioelectric-fin-size (verdict not-resolvable-with-public-data)", "S11 recorded answer (empty as delivered)"]}
```
