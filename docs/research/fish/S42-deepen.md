# S42-D — Deepening C4: is there a demonstrated Vm → fin-ray-growth-RATE route, with a measured effect size?

**Parent question (S42 / C4).** In zebrafish, is there any demonstrated route from a
**membrane-potential change** to a **change in fin ray growth rate**, with a **measured effect
size** — as opposed to a mere correlation between a channel *genotype* and a *final fin length*?

**Working answer being deepened.** No. The literature is dominated by genotype → final-length
correlations. The two things that look like exceptions each fall short of the full chain
(Vm-change → ray-growth-RATE, with effect size): the channel is manipulated but Vm itself is
never measured in fin cells; or Vm is perturbed but the readout is larval fin-fold *length*, not
adult ray *growth rate*. This note tests the single input that answer leans on hardest.

---

## 1. The input the answer is most sensitive to

The answer is a **negative** claim: "no study closes the loop." A negative of this shape is most
sensitive to the one study that comes *closest* to closing it, and within that study, to the one
number that makes "a membrane-potential change" sound like a large, established, causal driver.

That number is the **magnitude of the membrane-potential change attributed to the growth-driving
channel perturbation.** Across the whole corpus there is exactly **one** quoted value in
millivolts tied to a long-fin channel:

> *"the mutant channels lead to stronger hyperpolarization causing a shift in the membrane
> potential towards −90 to −100 mV"* — Perathoner et al. 2014, Fig. 5D text **[read-level:
> full-text]**.

Everything mechanistic rests on reading this as "the *alf*/kcnk5b gain-of-function hyperpolarizes
growth-relevant cells by ~30–40 mV (from a resting state toward −90/−100 mV)." If that Vm swing is
real and large, "a membrane-potential change drives growth" is on firm footing and the answer is
one small step from flipping to "partially yes." If the swing is actually single-digit mV in a
real fin cell, the mechanistic premise is a proxy that does not survive the trip from oocyte to
fin, and the answer hardens.

So the sensitivity test is: **does the −90/−100 mV figure hold for a fin cell, given the measured
driver (an "almost two-fold increase in K⁺ conductance", Perathoner Fig. 5B, full-text)?**

### Sensitivity shown by recomputing (not asserting)

The −90/−100 mV value is a **Xenopus oocyte** number. An oocyte is a near-pure K⁺ electrode: its
resting Vm already sits near E_K, so *any* increase in K⁺ permeability just pins it harder to
E_K ≈ −90/−100 mV. A real fin mesenchymal/epidermal cell has a finite Na⁺ (and leak) permeability,
so the same conductance change moves Vm far less. Goldman–Hodgkin–Katz, with K_i=140, K_o=4,
Na_i=12, Na_o=145 mM, RT/F ≈ 25.4 mV, scanning the baseline permeability ratio p_Na/p_K and
applying the **measured** driver (×1.5 to ×2 in p_K; ×4 shown as an upper bound):

```
p_Na/p_K   V0(mV)   ΔV @ ×1.5 pK   ΔV @ ×2 pK   ΔV @ ×4 pK
0.02       -76.5      -3.8           -6.0         -9.6
0.05       -64.1      -6.1           -9.8        -16.7
0.10       -51.6      -7.6          -12.5        -22.4
0.20       -37.1      -8.7          -14.5        -27.0
0.40       -21.5      -9.2          -15.6        -30.1
```
*(Calculated with GHK; this is a computation, not an observation.)*

A **2-fold** K⁺-conductance increase — the actual measured effect — hyperpolarizes a realistic
somatic cell by roughly **6 to 16 mV**, not 30–40 mV, and the final Vm lands near −70 to −65 mV,
nowhere near −90/−100 mV unless the cell was *already* an almost-pure K⁺ electrode like an oocyte.
Only an implausible ×4 change on an already-leaky cell reaches the high-20s mV. So the headline mV
figure is inflated by roughly 2–6× when transplanted from oocyte to fin — i.e. the input the
answer is most sensitive to **moves by well over the factor-of-two threshold** the moment it is
recomputed for the right cell.

---

## 2. How well is that input actually established?

**Poorly, and it is a proxy standing in for an unmeasured quantity.**

- **−90/−100 mV — proxy, not a fin measurement.** Measured in *Xenopus* oocytes by two-electrode
  voltage clamp (Perathoner 2014, full-text). It is the K⁺ reversal/working potential of an
  expression system, repeatedly cited as if it were the Vm of a fin cell. Read-level: full-text.
- **In-fin Vm — semiquantitative dye, and it disagrees in sign.** The only *in vivo* fin Vm readout
  in the same paper is DiSBAC2(3) staining, "pixel intensity, N = 21–23, p < 0.001" (Fig. S4), with
  the authors conceding the result only *"suggest[s] that this might indeed be the case."*
  Critically, the dye reports *alf* fins as **depolarized** across the fin — the **opposite sign**
  to the oocyte hyperpolarization. This disagreement is preserved, not averaged: the channel biology
  predicts hyperpolarization; the in vivo dye reports depolarization. No calibrated mV value exists
  for either state. Read-level: full-text.
- **Downstream channel papers never measure Vm at all.** Yi/Antos 2021 (eLife 60691, full-text):
  HEK293T patch clamp measures **current/conductance**, held at −80 mV; a KIRIN FLIM sensor reports
  intracellular **K⁺**, not voltage; no fin-cell Vm. Stewart 2021 (Development, PMC8217709,
  full-text) explicitly lists Vm as *future* work: *"Key future steps include characterizing
  membrane potentials and putative depolarizing signals."* Daane 2018 (Sci Rep, PMC6039437,
  full-text): defines V_mem but reports **no** in vivo mV.
- **Newest direct-Vm work uses uncalibrated reporters.** Liu/Nerli et al. (bioRxiv 2025
  647033 preprint, full-text; publ. Sci Adv 2026): a Voltron2 voltage reporter read as **−ΔF/F0**,
  not calibrated to mV. The only mV figure in it (~40 mV VSP activation threshold) is cited from
  prior literature, not measured.

So "a membrane-potential change of ~30–40 mV drives fin growth" is an **assumption repeated until
it reads as measured**: an oocyte reversal potential, imported into a cell type whose real Vm has
never been recorded in calibrated millivolts.

---

## 3. Going to improve it — the real quantity, and what would settle it

**The real quantity** is the *in-fin-ray-cell membrane potential and its change* (in mV) under a
growth-driving perturbation. I searched for it directly.

- **Primary sources read (full-text):** Perathoner 2014 (PMC3894163); Daane 2018 (PMC6039437);
  Yi/Antos 2021 eLife 60691 (PMC8110307); Stewart 2021 Development (PMC8217709); Liu/Nerli 2025
  bioRxiv 647033.
- **Read at abstract/search-summary only:** Silic 2020 *Genetics* (kcnj13 dermomyotome —
  patterning, not ray growth rate); Le Bleu/Stankunas 2025 *Development* (cacna1g; bioRxiv 608903
  full-text was rate-limited/unreachable — HTTP 429 and `could-not-access`).
- **Hosts that could not be resolved in this session (need network allow-listing):**
  `pubmed.ncbi.nlm.nih.gov`, `charlieduclut.github.io`. Stated as a scope limit, not worked around.

**Result of the search: a calibrated in-fin-cell Vm number does not exist in the accessible
literature.** The closest primary values are: an oocyte reversal potential (−90/−100 mV, wrong cell
type), a sign-conflicting DiSBAC dye (uncalibrated), and a Voltron2 ΔF/F0 (uncalibrated). I did not
find — and therefore do not invent — any mV value recorded in a fin ray blastema or lepidotrichial
cell. Where the number is unavailable it is written here as what it is: **unknown**.

**What would settle it.** Calibrated in vivo voltage imaging (ratiometric Voltron / Archon with a
mV calibration curve, or a blastema patch recording) of the fin-ray blastema and intra-ray
mesenchyme, in wild-type vs a long-fin channel genotype (*alf*/kcnk5b, loft2/kcnh2a, or
hsp70:kcnk5b induced), **paired in the same animals with longitudinal ray growth-rate measurement
(µm/day) by repeated imaging.** That single experiment produces the missing edge: ΔVm (mV) on one
axis, Δ(ray growth rate) (µm/day) on the other, with an effect size. **Cost:** modest — existing
transgenic voltage-reporter lines and existing long-fin mutants; roughly one graduate-student-year;
no new reagent class required. The binding difficulty is calibration of the reporter to absolute
mV in vivo, not feasibility.

---

## 4. Recompute the conclusion with the improved input

Replacing the inflated proxy (−90/−100 mV, oocyte) with the honest improved input (**in-fin-ray-cell
ΔVm = unknown in calibrated mV; the measured channel driver is a ~2-fold K⁺-conductance change,
which GHK puts at ~6–16 mV in a realistic cell, and the only in vivo dye reports the opposite
sign**), the original answer:

**STANDS — and sharpens into a cleaner negative.**

- The study with a genuine *growth-RATE* effect size (Yi/Antos: hsp70:kcnk5b^S345E highest vs
  hsp70:kcnk5b^S345A lowest *allometric regenerative growth rates*, adult fin, Student's t-test,
  "three or more experiments", full-text) **measures no Vm** — the membrane-potential leg of the
  chain is absent.
- The study with a genuine direct *Vm perturbation* and a measured size effect (Liu/Nerli: 1 h KCl
  depolarization → *"fin overgrowth (10% length increase) by amplifying fin-wide proliferation"*,
  p ≤ 0.001; VSP/*tpte* loss blocks regeneration, VSP overexpression → longer fins, full-text)
  works on the **larval fin fold — which has no rays** — and reports endpoint **length/proliferation,
  not a ray growth rate**, with Vm as an uncalibrated ΔF/F0.
- The canonical long-fin channel papers (Perathoner, Daane, Stewart, Silic) deliver exactly what
  C4 warned against: channel **genotype** correlated with **final length** or allometric exponent
  (e.g. *alf* k ≈ 2 vs wild-type k = 1.29, full-text), with Vm either unmeasured or a
  sign-conflicting semiquantitative dye. Stewart is explicit that longfin overgrowth comes from a
  **prolonged outgrowth period**, with *"indistinguishable maximal growth rates"* between loft2 and
  wild type — so even the rate/duration decomposition cuts against a Vm→rate story.

No single study supplies all four of {membrane-potential change, measured in fin-ray cells, →
change in ray growth rate, with an effect size}. The deepening did not find the missing edge; it
showed that the one number making the edge look present is an oocyte artifact that GHK does not let
you carry into the fin. A precise negative, and the experiment that would convert it, are the
deliverable.

---

```swarm-result
{"subproblem": "S42-D", "evidence": "full-text",
  "answer": "No zebrafish study closes the loop from a measured in-fin-cell membrane-potential change to a change in fin-ray growth rate with an effect size; the lone mV figure (-90/-100 mV) is a Xenopus-oocyte reversal potential that GHK shows cannot be a ~2-fold-conductance-driven fin-cell Vm swing, so the negative answer stands and sharpens.",
  "key_number": "in-fin-ray-cell delta-Vm = unknown (calibrated mV); measured driver is ~2x K+ conductance => ~6-16 mV by GHK, vs the quoted -90/-100 mV oocyte proxy",
  "verdict": "stands",
  "depends_on": [
    "Perathoner2014: alf/kcnk5b oocyte ~2-fold K+ conductance increase (PMC3894163, full-text, Fig 5B)",
    "Perathoner2014: oocyte Vm shift to -90/-100 mV (PMC3894163, full-text, Fig 5D)",
    "Perathoner2014: DiSBAC2(3) dye shows alf fins DEPOLARIZED in vivo, semiquantitative, opposite sign (PMC3894163, full-text, Fig S4)",
    "Perathoner2014: alf allometric coefficient k~2 vs wild-type k=1.29, final length not rate (PMC3894163, full-text, Fig 1D)",
    "YiAntos2021: hsp70:kcnk5b S345E vs S345A change allometric regenerative growth RATES, no fin-cell Vm measured (eLife 60691, PMC8110307, full-text, Fig 6)",
    "Stewart2021: longfin overgrowth is prolonged outgrowth with indistinguishable maximal growth rates; Vm listed as future work (Development, PMC8217709, full-text, Fig 3)",
    "Daane2018: FK506/kcnk5b growth as slope of length/SL, no in vivo mV (Sci Rep, PMC6039437, full-text)",
    "LiuNerli2025: 1h KCl depolarization -> 10% larval fin-fold length increase via proliferation; VSP/tpte loss blocks regeneration; Voltron2 reporter uncalibrated to mV; larval fold has no rays (bioRxiv 647033, full-text)",
    "GHK recompute: 2x p_K on a realistic cell (p_Na/p_K 0.05-0.2) yields ~6-16 mV hyperpolarization, not 30-40 mV (calculation, this note, section 1)",
    "Silic2020: kcnj13 dermomyotome affects fin patterning not ray growth rate (Genetics, search-summary)",
    "LeBleu2025: cacna1g long-fin via prolonged outgrowth, Ca2+ not Vm, full text could-not-access HTTP429 (Development/bioRxiv 608903, search-summary)"
  ]}
```
