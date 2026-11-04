# S40-D-D — Deepening S40 (cell): attacking its most sensitive input

Parent: **S40 (cell)**, `docs/research/fish/S40-cell.md` on branch `claude/s40-cell-membrane-conductance-oar3jg`
(commit `f7cddad2`). Project `zebrafish-flight`, constraint **C2**. Date: 2026-11-04.
The script that reproduces every number in this file is `docs/research/fish/S40-D-sensitivity.py`.

Labels used, in the sentence where each applies: **[measured]** = reported as observed by the cited authors;
**[computed]** = arithmetic done here; **[assumption]** = a value chosen here; **[inference]** = my reading, not a
source's claim.

---

## 0. What S40 concluded

S40 derived the membrane conductance a fin-mesenchyme cell needs to hold a ≥10 mV standing Vmem difference against
gap-junction leak. It used a syncytial length-constant model, V_centre = ΔE·(1 − e^(−w/2λ)) with λ = a√(G_j/G_m).
Its headline: **C2 is not refuted from below.** The measured surrogate conductances (5–15 µS/cm² for Hosoi & Slayman
L cells; ~100–330 µS/cm² for Kohl & Gourdie cardiac fibroblasts) lie above the requirement, except in the worst corner
(ΔE 15 mV, w 50 µm, G_j 2 nS → 4.8×10⁻⁵ S/cm²). There the Hosoi value falls ~1 order below, which is short of the
2-order refutation rule. Its secondary inference was that **the binding variable is G_j**, the fin junctional
conductance.

I re-derived the slab solution, matching value and current at x = h. It is correct as written.

---

## 1. Which input is the answer most sensitive to? (recomputed, not asserted)

Throughout, the test is the conclusion's own decision rule: is the requirement ≥100× (2 orders) above the lowest
measured surrogate, 5 µS/cm²? At the worst corner the gap is **9.7×** **[computed]**. Each input was perturbed by a
factor of two **[computed]**:

| Input (worst corner base) | ×½ → g_m,req / gap to Hosoi-low | ×2 → g_m,req / gap to Hosoi-low | Elasticity of g_m,req | Flips "not refuted"? |
|---|---|---|---|---|
| **ΔE (15 mV)** | **∞: no g_m suffices, the requirement is undefined** | 6.6e-6 / 1.3× | **−3.6 at 15 mV, diverging as ΔE → 10 mV** | **Yes (halving it)** |
| w (50 µm) | 1.9e-4 / 39× | 1.2e-5 / 2.4× | −2 | No |
| cell pitch a (10 µm) | — | 1.9e-4 / 39× | +2 | No |
| G_j (2 nS) | 2.4e-5 / 4.8× | 9.7e-5 / 19× | +1 | No |
| A_cell (800 µm²) | 9.7e-5 / 19× | 2.4e-5 / 4.8× | −1 | No |
| surrogate g_m (5 µS/cm²) | gap 19× | gap 4.8× | — | No |

**[computed]** Only ΔE flips the conclusion on a factor-of-two error. In the central case (ΔE 30 → 15 mV, w 200 µm,
G_j 1 nS), halving ΔE raises the requirement 7.3× (2.1e-7 → 1.5e-6 S/cm²). That still sits below every surrogate, but
it is the largest single-input move there too (elasticity −2.5).

**[computed]** The decision is actually stranger than "sensitive". I solved for the ΔE at which the requirement
reaches 100× the lowest surrogate. The answer is **ΔE ≤ 10.3 mV** for the worst corner, and **ΔE ≤ 10.0 mV**
(indistinguishable from the threshold) for every other corner and for every surrogate. So within this model **the
g_m comparison almost never decides C2. The verdict is set by whether ΔE clears ~10.3 mV.** Above that, every
surrogate passes or misses by less than 2 orders. Below 10 mV, no conductance works. **[inference]** S40's secondary
claim that "the binding variable is G_j" therefore **falls**. G_j moves the requirement linearly. ΔE is the input
that switches the answer on or off.

---

## 2. How well is ΔE established?

**Evidence level: assumption.** In S40, ΔE ∈ {15, 30, 50} mV was chosen **[assumption]**. It was bounded above only
loosely, by "E_K (−90 to −100 mV in oocytes) minus a depolarised fibroblast Vm". Nothing in S40 measures ΔE.

* The only fin Vmem data are from Perathoner et al. 2014 (PLoS Genet 10:e1004080). They are DiSBAC₂(3) fluorescence,
  **uncalibrated, with no mV** (read-level: full-text, as read by the S40 agent. I did not re-read it in this session).
* The Silic & Zhang review (*Cells* 12:1148, 2023, PMC10137051, **full-text, first ~100k of 314k characters read**)
  states that "direct evidence of bioelectricity in zebrafish fin development is still lacking". Its tables of
  zebrafish GEVI use (ASAP1 etc.) contain **no fin entries**. Its only fibroblast Vm is a generic vertebrate
  −25 to −16 mV.
* Liu, Nerli et al. (Mateus lab), *Injury-induced electrochemical coupling triggers organ growth*, Science Advances
  2026 (bioRxiv 10.1101/2025.04.03.647033). **Read-level: search-summary.** Full text was **could-not-access**:
  bioRxiv returned HTTP 429, and PubMed and the author's site do not resolve from this session. The summary says
  imaging found a long-range depolarisation gradient across ~200 µm of larval fin within ~100 ms of injury. It is a
  transient, injury-evoked signal. I could not establish whether its amplitude was calibrated in mV. It does **not**
  give a standing ΔE.

**[inference]** In S40, ΔE reads like a parameter, but it is an assumption that has never been measured in fin. The
"50 mV generous upper bound" was an argument from the extreme reversal potentials, not from any channel-level data.

---

## 3. Improving it: from an assumed mV to a quantity tied to a measurement

A standing ΔE requires that the domain's own cells, if isolated, rest at a different Vm. In a two-conductance cell
(a K⁺ conductance g_K at E_K, and everything else lumped as g_L at E_L), V = (g_K·E_K + g_L·E_L)/(g_K + g_L).
Suppose the domain differs from the surround only by a factor f in g_K. Then **[computed]** the largest possible ΔE,
over every baseline ratio r = g_K/g_L, is reached at r = 1/√f:

  **ΔE_max = D · (√f − 1)/(√f + 1)**, where D = E_L − E_K.

Inverting gives the regional conductance contrast that each ΔE in S40's grid needs **[computed]**:

| ΔE needed | f_min (D = 90 mV) | f_min (D = 70 mV) |
|---|---|---|
| 10 mV (threshold) | 1.56 | 1.78 |
| 15 mV (S40 worst) | 1.96 | 2.39 |
| 30 mV (S40 central) | 4.0 | 6.25 |
| 50 mV (S40 best) | 12.3 | 36 |

Inputs for D:
* E_K ≈ −86 to −100 mV **[computed]**, from Nernst at 28 °C (RT/F = 25.9 mV) with [K⁺]ᵢ 140 mM and [K⁺]ₒ 3–5 mM.
  **Both concentrations are [assumption].** I found no fin-interstitial [K⁺] measurement. The S40 source gives
  −90 to −100 mV for *alf* oocytes **[measured, Xenopus oocyte, not fish]**.
* E_L ≈ 0 to −20 mV **[assumption]**, typical of non-selective cation and Cl⁻ leaks. So D ≈ 70–90 mV.

The only measured channel-level contrast available is in *alf* (*kcnk5b* gain-of-function). It shows "an almost
two-fold increase in K⁺ conductance" over wild type **[measured, Perathoner 2014, Xenopus oocytes; author's claim]**.
That is a mutant versus wild-type comparison in a heterologous cell. It is **not** a measured regional difference
inside a wild-type fin, which remains **unknown**. Scope of that negative: the searches in §5, plus S40's own scope.

**[computed]** With f = 2, ΔE_max = **15.4 mV (D = 90)** or **12.0 mV (D = 70)**. With f = 1.5, it is 9.1 / 7.1 mV,
which is below threshold. **[inference]** If regional channel contrast in fin is of the order of the one measured
fold-change, the realistic ΔE is **≈ 12–15 mV at best** (the optimum baseline). That is S40's worst corner, not its
central case. S40's central ΔE = 30 mV needs a 4–6-fold regional contrast in the dominant K⁺ conductance, and nothing
found supports that. One caveat **[computed]**: if two channels move in opposite directions (K⁺ up f, leak down f),
the effective ratio is f², and f = 2 then allows up to 30 mV (D = 90). Co-regulation of that kind is not evidenced
either.

**Improved input: ΔE ≈ 12–15.4 mV (upper bound, computed from a measured ~2-fold K⁺ conductance contrast and assumed
reversal potentials). It replaces S40's assumed 15–50 mV.**

---

## 4. Recompute the conclusion with the improved input [computed]

g_m,req (S/cm²) at a = 10 µm and A_cell = 800 µm² (S40's placeholders, unchanged):

| ΔE | w 50 µm, G_j 0.2 nS | 50, 1 nS | 50, 2 nS | 200, 1 nS | 200, 2 nS | 1000, 2 nS |
|---|---|---|---|---|---|---|
| 15.4 mV | 4.4e-6 | 2.2e-5 | 4.4e-5 | 1.4e-6 | 2.7e-6 | 1.1e-7 |
| 12.0 mV | 1.3e-5 | 6.4e-5 | **1.3e-4** | 4.0e-6 | 8.0e-6 | 3.2e-7 |
| 10.5 mV | 3.7e-5 | 1.9e-4 | 3.7e-4 | 1.2e-5 | 2.3e-5 | 9.3e-7 |

Against the measured surrogates (5–15 µS/cm² Hosoi; 100–330 µS/cm² Kohl, the latter computed in S40):
* **50 µm domains**: Hosoi-low falls 1–26× below the requirement for ΔE 12–15.4 mV, and 7–74× below at 10.5 mV.
  The Kohl values satisfy the requirement or roughly tie with it. **No case reaches the 100× refutation rule.**
* **200 µm domains**: Hosoi passes or misses by ≤ 1.6× (ΔE 12). Kohl passes by 12–80×.
* **1000 µm domains**: everything passes.

**Verdict: STANDS (the headline), on a thinner margin. S40's secondary inference FALLS.**
* "C2 is not refuted from below by any data found" still holds **[computed comparison against surrogate
  measurements]**.
* S40's statement that the surrogates lie "above the requirement over almost the whole grid, typically by 1–5
  orders" does not survive. With the improved ΔE, the realistic cases are the narrow-margin ones.
* The claim that G_j is the binding variable falls. C2 now rests on **whether a wild-type fin domain has ≳1.6–2.4-fold
  more (or less) of its dominant K⁺ conductance than its neighbours.** That is a threshold question, and it has not
  been measured.

---

## 5. What measurement would settle it, and what it would cost

1. **Cheapest proxy, likely already in public data:** the regional ratio of *kcnk5b* (and *kcnh2a*) transcript levels
   across fin mesenchyme domains (proximal/distal, intra-ray/joint), from existing fin-regeneration scRNA-seq or
   HCR/RNAscope images. This bounds f. The settling test is whether any wild-type domain contrast is ≥ 2-fold. It is
   only a proxy, because transcript ≠ conductance and Kcnk5b activity is post-translationally regulated by
   calcineurin (Yi et al. eLife 2021, 60691, listing only). Cost: analysis time on public data, with no wet lab.
   I did not locate a dataset reporting *kcnk5b* by region. Scope: two web searches. One returned a 3/7 dpa
   fibroblast scRNA-seq preprint (bioRxiv 2022.10.09.511495, search-summary) whose snippets do not mention *kcnk5b*.
2. **Decisive:** calibrated Vmem imaging in adult fin using the existing Tg(ubi:ASAP1) line (Silic & Zhang 2023, a
   line that exists but has not been used in fins). A perforated-patch recording in the same explant would give the
   mV calibration. Its outcome is ΔE directly. If the domain contrast is ≥ 10.3 mV, C2 passes against the Hosoi
   surrogate in every case. If it is < 10 mV everywhere, C2 fails regardless of conductance. Monetary cost:
   **unknown**. I have no sourced figure, so none is given. In resources, it needs a fish facility, a confocal or
   light-sheet microscope, and a patch rig.

---

## 6. What this does NOT establish

* It does not measure ΔE. 12–15.4 mV is a **computed upper bound**, and it rests on a mutant-versus-wild-type
  oocyte fold-change used as a stand-in for wild-type regional contrast.
* The two-conductance cell is a simplification **[assumption]**. Voltage-gated Kcnh2a makes g_K depend on V, and
  more channel classes could widen or narrow ΔE_max.
* The isopotential-extracellular assumption is carried over from S40 unchanged. Liu et al. 2026
  (search-summary) model fin interstitial ionic fluxes and potential as **coupled** ("electrodiffusive"), which
  suggests r_e may not be negligible in fin. That would lengthen the effective λ and raise g_m,req. This is
  **untested here**.
* All of S40's other caveats (surrogate cell types, G_j unmeasured, placeholder a and A_cell, steady-state only)
  still apply.

### Sources (read-level)
* Parent S40-cell.md, branch `claude/s40-cell-membrane-conductance-oar3jg` — **full-text** (the repository file).
* Perathoner et al. 2014, PLoS Genet 10:e1004080, PMC3894163 — values taken via S40 (full-text there). Not
  re-read in this session.
* Silic MR, Zhang G. *Cells* 12(8):1148 (2023), PMC10137051 — **full-text** (first ~32% of the page).
* Liu, Nerli et al., Science Advances 2026; bioRxiv 10.1101/2025.04.03.647033 — **search-summary**. Full text
  **could-not-access** (HTTP 429; pubmed.ncbi.nlm.nih.gov, charlieduclut.github.io and mpi-cbg.de do not resolve
  under this session's network policy).
* Hosoi & Slayman 1985; Kohl & Gourdie 2014; Rook et al. 1992 — values reused from S40 at S40's read-levels
  (abstract / full-text / abstract).
* Yi et al., eLife 2021;10:e60691 — **listing**.
* fibroblast scRNA-seq preprint, bioRxiv 2022.10.09.511495 — **search-summary**.

Negative-search scope for this deepening: 5 web searches (US index) on 2026-11-04, covering calibrated fin Vmem,
fin-fibroblast patch clamp, GEVIs in fin, and the regional *kcnk5b* expression gradient. None found a calibrated mV,
a standing regional Vmem, or a regional K⁺-conductance ratio in zebrafish fin. Not searched: Google Scholar,
PubMed (unreachable), Web of Science, or supplementary tables.

```swarm-result
{"subproblem": "S40-D-D", "evidence": "derived",
  "answer": "The S40 verdict is decided almost entirely by the isolated-domain Vmem offset dE (any dE below ~10.3 mV makes C2 fail regardless of conductance, while above it no surrogate misses by 2 orders); bounding dE from the only measured channel contrast (~2-fold K+ conductance, kcnk5b alf in oocytes) gives dE <= 12-15.4 mV, which puts the fin in S40's worst corner, so 'C2 not refuted from below' stands on a thin margin, while S40's claim that G_j is the binding variable falls.",
  "key_number": "dE_max = 12.0-15.4 mV (computed upper bound for a 2-fold regional K+ conductance contrast, D = E_L - E_K = 70-90 mV); refutation threshold dE <= 10.3 mV",
  "verdict": "stands",
  "depends_on": ["S40 (cell) slab length-constant model V_centre = dE(1-exp(-w/2lambda)), lambda = a*sqrt(Gj/Gm)", "assumption: isopotential extracellular space (r_e << r_i), possibly challenged by Liu et al. 2026 electrodiffusive coupling", "measured: alf kcnk5b ~2-fold K+ conductance increase vs WT in Xenopus oocytes (Perathoner 2014), used as proxy for WT regional contrast f", "assumption: WT regional K+ conductance contrast f ~ 2 (unmeasured)", "computed: E_K -86 to -100 mV from assumed [K+]i 140 mM, [K+]o 3-5 mM at 28 C", "assumption: lumped leak reversal E_L 0 to -20 mV", "assumption: two-conductance cell model, dE_max = D(sqrt f - 1)/(sqrt f + 1)", "measured surrogate: Hosoi & Slayman 1985 L-cell g_m 5-15 uS/cm2", "computed surrogate: Kohl & Gourdie 2014 cardiac fibroblast g_m 100-330 uS/cm2", "assumption: Gj 0.2-2 nS per pair (Rook 1992 pairs; Kohl channel-count estimate)", "assumption: cell pitch a = 10 um", "assumption: A_cell = 800 um2 from 6-10 pF at 1 uF/cm2", "assumption: domain width w 50-1000 um", "S40 refutation rule: >=2 orders below requirement refutes", "negative search: no calibrated fin Vmem or regional fin K+ conductance found (scope: 5 web searches + S40 scope; PubMed unreachable)"]}
```
