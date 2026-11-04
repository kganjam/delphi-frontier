# S40 (cell scale) — Membrane conductance needed to hold a ≥10 mV standing ΔVmem across zebrafish fin mesenchyme

Project: `zebrafish-flight`. Constraint: **C2 (quantitative)**.
Date of work: 2026-11-04. Status: **derived requirement; no fin-mesenchyme measurement found; surrogate mesenchymal measurements do not refute.**

Labels used throughout, in the sentence where each applies:
**[measured]** = a number the cited authors report observing; **[computed]** = arithmetic done here;
**[assumption]** = a value chosen here, not measured; **[inference]** = my reading, not the source's claim.

---

## 1. The question, restated precisely

Fin mesenchyme is a gap-junction-coupled cell population (zebrafish fin size depends on the connexin gene
*cx43*, the K⁺ leak channel *kcnk5b* and the voltage-gated K⁺ channel *kcnh2a*; sources in §2). For a
bioelectric pattern to carry positional information, a group of cells must sit at a membrane potential at least
**10 mV** away from its neighbours, and stay there.

The leak that erases such a difference is mainly **current through gap junctions** into neighbouring cells. The
thing that resists the leak is each cell's own **membrane conductance** (its ion channels), which pulls its Vmem
back toward its own reversal potential. The trade-off is set by the syncytial length constant

  λ = a · √(G_j / G_m)  (a = cell pitch, G_j = junctional conductance per neighbour pair, G_m = membrane conductance per cell).

A domain much narrower than λ is shorted out by its neighbours. A domain much wider than λ keeps its own Vmem.
So the question becomes: **what minimum specific membrane conductance g_m (S/cm²) keeps λ short enough that a
domain of width w, whose cells would rest ΔE mV from their neighbours if isolated, still shows ≥10 mV at its
centre?** And does any measured value of g_m, for fin mesenchyme or a comparable mesenchymal cell, fall in that range?

What makes it hard: **no input that matters has been measured in fin mesenchyme.** G_j is not, g_m is not, the
cell pitch is not, and the absolute Vmem difference is not (see §2). The requirement spans more than four orders
of magnitude across plausible inputs, so the answer depends on which corner of input space the real fin occupies.

---

## 2. What is measured

### 2a. Zebrafish fin: what exists and what does not

| Source | Read-level | What it reports | Relevance |
|---|---|---|---|
| Perathoner S, Daane JM, Henrion U, Seebohm G, Higdon CW, Johnson SL, Nüsslein-Volhard C, Harris MP. *Bioelectric signaling regulates size in zebrafish fins.* PLoS Genet 10:e1004080 (**2014**) | full-text (automated fetch read ~85% of the PMC page, PMC3894163) | **[measured]** *alf* (gain-of-function *kcnk5b*) channels in *Xenopus* oocytes show "an almost two-fold increase in K⁺ conductance" over wild type and shift oocyte Vm toward −90 to −100 mV. Currents were normalised to wild type, and the text gives **no absolute conductance**. **[measured]** In fish fins, the voltage dye DiSBAC₂(3) was used on juvenile caudal fins. Wild type shows hyperpolarisation in discrete regions, and *alf* shows depolarisation across the fin (p<0.001, N=21–23). Dye signal is **relative and not calibrated to mV**. | Shows that spatial Vmem differences exist in fins [author claim, dye-level]. Gives no conductance, no G_j and no mV value. |
| Daane JM et al. *Bioelectric-calcineurin signaling module regulates allometric growth and size of the zebrafish fin.* Sci Rep 8:10391 (**2018**) | search-summary (nature.com redirected to a login; bioRxiv 258442 returned HTTP 429) | Per a commentary: FK506 decreases conductance in cells *expressing* zebrafish Kcnk5b. The system is heterologous per the summary; I could not confirm which cells. | Not a fin-cell measurement, as far as I could verify. |
| Stewart S et al. *longfin* = cis over-expression of *kcnh2a* (bioRxiv 790329; PMC8217709 appeared in the same search but I did not confirm it is the published version) (**2019/2021**) | search-summary | Kcnh2a acts tissue-autonomously in the intra-ray mesenchymal lineage. Membrane-potential dynamics are **proposed** (a model, not measured). | Locates the relevant channels in mesenchyme. No conductance. |
| Hoptak-Solga AD et al. *cx43* (*sof*) alleles (**2008**, PMC2429987) | search-summary | **[measured]** Oocyte pairs: the weakest allele couples much more than the strong alleles. Dye coupling occurs for all alleles. **No in-fin electrical coupling measured.** | G_j in fin = **unknown**. |

**Negative search, with its scope.** I found no patch-clamp, sharp-electrode or calibrated-dye measurement of
membrane conductance, input resistance, junctional conductance or absolute Vmem in zebrafish fin mesenchyme,
fin blastema, or zebrafish fibroblast lines (ZF4, PAC2). Scope: about 10 web searches (US web index) on 2026-11-04,
plus the full texts of Perathoner 2014 and the two mesenchymal sources below. PubMed was **unreachable** from this
session (DNS blocked by the network policy). Nature and bioRxiv full texts for Daane 2018 could not be accessed. Not
searched: Google Scholar, Web of Science, theses, or the Harris, Stankunas and Iovine lab supplements in full.
So **"unmeasured"** here means **"not found within this scope"**. It does not mean "known not to exist."

### 2b. Comparable mesenchymal / fibroblast cells (surrogates)

| Source | Read-level | Value **[measured unless stated]** | Converted to S/cm² |
|---|---|---|---|
| Hosoi S, Slayman CL. *Membrane voltage, resistance, and channel switching in isolated mouse fibroblasts (L cells).* J Physiol 367:267–290 (**1985**) | abstract | Slope conductivity **5–15 µS/cm²** at baseline, rising to 200–400 µS/cm² with ≥0.1 mM free Ca²⁺ in the pipette. Leak-corrected V₀ is −50 to −75 mV. Cells are 13–15 µm in diameter. Membrane resistance is "in the same range as the seal resistance" (seals were 10–50 GΩ). | **5×10⁻⁶ – 1.5×10⁻⁵** (as reported) |
| Kohl P, Gourdie RG. *Fibroblast–myocyte electrotonic coupling: does it occur in native cardiac tissue?* J Mol Cell Cardiol 70:37–46 (**2014**), a review | full-text (first ~60% of the page read) | Fibroblast membrane resistance **in situ 0.5–1 GΩ** (citing Kohl et al. 1994 and Kamkin et al. 2002). Isolated-cell capacitance is **6–10 pF** (citing Chilton 2005 and Dawson 2012). Isolated Vm is −10 to −20 mV. "As few as 10–30 connexin channels would provide sufficient coupling." | **[computed]** (1/0.5–1 GΩ) ÷ (6–10 pF ÷ 1 µF/cm²) = **1.0×10⁻⁴ – 3.3×10⁻⁴** |
| Kiseleva I et al. J Mol Cell Cardiol 30:1083–1093 (**1998**), rat atrial fibroblasts | listing (cited secondhand; values seen only via search-summary of Kamkin/Kiseleva/Isenberg) | Input resistance **~0.4–0.6 GΩ**. Vm −5 to −70 mV (another review cites −22 ± 1.9 mV). | No capacitance obtained, so **not converted** |
| Heubach JF et al. *Electrophysiological properties of human mesenchymal stem cells.* J Physiol 554:659–672 (**2004**) | full-text (~95% of the page read) | Cm **~54–55 pF** (up to 116 pF in a subgroup). Vm −35.2 ± 1.6 / −28.9 ± 2.1 mV. Outward current density 11–16 pA/pF at **+70 mV**. **No resting input resistance was reported** in the text I read. | **Not convertible to a resting g_m.** The +70 mV current is activated K⁺ current, not leak (see §5). |
| Rook MB et al. *Differences in gap junction channels between cardiac myocytes, fibroblasts, and heterologous pairs.* Am J Physiol 263:C959–977 (**1992**) | abstract (via catalogue records; PubMed blocked) | **Junctional coupling** in fibroblast pairs: pairs with G_j above **1–2 nS** showed no voltage gating, and pairs below 1 nS were also seen. Fibroblast single-channel conductance is ~21–22 pS. **Full G_j range not obtained.** | Used for G_j, not g_m |
| Sundelacruz S, Levin M, Kaplan DL. PLoS ONE 3:e3737 (**2008**), hMSC | search-summary | Differentiated hMSCs hyperpolarised by ~56 (osteo) and ~74 (adipo) mV relative to undifferentiated cells. The scale assumes 1% dye change = 1 mV, which is **an author calibration assumption, not a direct measurement**. | Bounds ΔE plausibility only |

**Disagreement preserved.** The two convertible g_m estimates differ by **~1–2 orders of magnitude**: 5–15 µS/cm²
(Hosoi & Slayman, isolated cultured mouse L cells, direct specific conductivity) against 100–330 µS/cm²
(Kohl & Gourdie, *in situ* cardiac fibroblast resistance divided by *isolated*-cell capacitance). I do not average
them. **[inference]** Several things could explain the gap. Seal leak inflates conductance in whole-cell recordings
of high-resistance cells (Hosoi & Slayman's own point; also a 2017 J Physiol synovial-fibroblast modelling figure,
PMC5285716, search-summary). The two cells are different types. The Kohl figure mixes an in-situ resistance
(which coupling to neighbours lowers) with an isolated-cell area. Kohl & Gourdie themselves say isolated cells show
resistance roughly an order of magnitude **higher** than in situ, which pushes toward Hosoi's value. Both are
carried forward as the low and high ends.

---

## 3. What I computed (computation, not observation)

### Model **[assumption]**
* Mesenchyme is treated as a cubic lattice of identical cells, pitch **a = 10 µm**. This is a placeholder: fin
  mesenchymal cell pitch is not measured here.
* Extracellular space is isopotential (r_e ≪ r_i). This is the standard syncytium simplification. It ignores the
  epidermal and transepithelial path.
* Each cell has membrane conductance G_m = g_m·A_cell. **A_cell = 8×10⁻⁶ cm²** (800 µm²), taken from the 6–10 pF
  fibroblast capacitance at the textbook 1 µF/cm². hMSCs (~55 pF) would be ~7× larger, which lowers the required
  g_m by ~7× for the same G_m.
* Junctional conductance per neighbour pair: **G_j ∈ {0.2, 1, 2} nS**. 0.2 nS ≈ Kohl's "10–30 channels" × ~21 pS
  [computed]. 1–2 nS is the voltage-gating threshold seen in Rook 1992 pairs. **Higher values certainly occur in
  other tissues. The fin value is unknown.**
* A slab domain of width **w ∈ {50, 200, 1000} µm** is embedded in tissue. If isolated, its cells would rest **ΔE**
  away from the surround, with **ΔE ∈ {15, 30, 50} mV**. This is bounded above by roughly E_K − (depolarised
  fibroblast Vm). The −90 to −100 mV oocyte E_K and the −10 to −50 mV fibroblast Vm in §2 make 50 mV generous.
  The real ΔE is **unknown**.

### Derivation **[computed]**
In steady state, along the slab normal: a² (G_j/G_m) V'' = V − V_∞, so λ = a√(G_j/G_m). The solution for a slab of
half-width h·λ, matching value and current at its edges, gives

  V_centre − V_far = ΔE · (1 − e^(−w/2λ)).

Requiring ≥10 mV gives w/2λ ≥ −ln(1 − 10/ΔE), so:

| ΔE | required w/2λ | λ_max |
|---|---|---|
| 15 mV | 1.099 | 0.455 w |
| 30 mV | 0.405 | 1.233 w |
| 50 mV | 0.223 | 2.241 w |

Then **G_m ≥ G_j·(a/λ_max)²** and **g_m,req = G_m / A_cell**.

### Required specific membrane conductance g_m,req (S/cm²) **[computed]**

| ΔE \ w | G_j | 50 µm | 200 µm | 1000 µm |
|---|---|---|---|---|
| 15 mV | 0.2 nS | 4.8e-6 | 3.0e-7 | 1.2e-8 |
| 15 mV | 1 nS | 2.4e-5 | 1.5e-6 | 6.0e-8 |
| 15 mV | 2 nS | **4.8e-5** | 3.0e-6 | 1.2e-7 |
| 30 mV | 0.2 nS | 6.6e-7 | 4.1e-8 | 1.6e-9 |
| 30 mV | 1 nS | 3.3e-6 | **2.1e-7** | 8.2e-9 |
| 30 mV | 2 nS | 6.6e-6 | 4.1e-7 | 1.6e-8 |
| 50 mV | 0.2 nS | 2.0e-7 | 1.2e-8 | 5.0e-10 |
| 50 mV | 1 nS | 1.0e-6 | 6.2e-8 | 2.5e-9 |
| 50 mV | 2 nS | 2.0e-6 | 1.2e-7 | 5.0e-9 |

The worst case in the grid is **4.8×10⁻⁵ S/cm²**. A central case (ΔE 30 mV, w 200 µm, G_j 1 nS) needs
**2.1×10⁻⁷ S/cm²**.

### Inverse: the junctional conductance that would break the requirement **[computed]**
G_j,max = G_m·(λ_max/a)², using measured surrogate g_m and A_cell = 8×10⁻⁶ cm²:

| surrogate g_m | G_m | ΔE15 / w50 | ΔE30 / w200 | ΔE50 / w1000 |
|---|---|---|---|---|
| 5 µS/cm² (Hosoi low) | 40 pS | **0.21 nS** | 24 nS | 2.0 µS |
| 15 µS/cm² (Hosoi high) | 120 pS | 0.62 nS | 73 nS | 6.0 µS |
| 100 µS/cm² (Kohl low) | 0.8 nS | 4.1 nS | 0.49 µS | 40 µS |
| 330 µS/cm² (Kohl high) | 2.7 nS | 14 nS | 1.6 µS | 134 µS |

Length constants implied by the surrogates **[computed]**: λ ≈ 3–70 µm (that is, 0.3–7 cell pitches) for
g_m 5–330 µS/cm² and G_j 0.2–2 nS.

Time to reach steady state **[computed]**: τ_m = C_m/g_m ≈ 1 µF/cm² ÷ (5–330 µS/cm²) ≈ **3 ms – 0.2 s**. Any pattern
lasting hours is effectively steady-state, so the steady-state model is the relevant one.

---

## 4. The answer

**Evidence level: derived** (requirement derived from a model; compared against *surrogate* measurements; the
fin-mesenchyme conductance itself is **unknown**).

* **[computed]** Holding ≥10 mV across a mesenchymal domain requires a specific membrane conductance between
  ~10⁻⁹ and **~5×10⁻⁵ S/cm²** over the input grid. It is ~2×10⁻⁷ S/cm² in a central case, and 4.8×10⁻⁵ S/cm² in
  the worst case (ΔE = 15 mV, w = 50 µm, G_j = 2 nS).
* **[measured, surrogate]** Two measured mesenchymal/fibroblast conductances: **5–15 µS/cm²** (mouse L-cell
  fibroblasts, Hosoi & Slayman 1985, abstract) and **~100–330 µS/cm²** (cardiac fibroblasts in situ, Kohl & Gourdie
  2014, a value I computed from their reported resistance and capacitance).
* **No measured membrane conductance for zebrafish fin mesenchyme was found** (scope in §2a).
* **[inference]** Comparing the two: the surrogate conductances lie **above** the requirement over almost the whole
  grid, typically by 1–5 orders of magnitude. The one exception is the narrow/weak-drive/strong-coupling corner
  (ΔE 15 mV, w 50 µm, G_j ≥ 1 nS), where the Hosoi value falls about **one order below** the requirement. Per the
  refutation rule stated for S40 (two or more orders *below* refutes), **C2 is not refuted from below by any data
  found.** It is also **not settled as satisfied**, because the settling measurement (fin mesenchyme itself) does
  not exist in the searched literature.
* **[inference]** The binding variable is not membrane conductance. It is **gap-junctional coupling G_j in fin
  mesenchyme**, which is unmeasured. With surrogate g_m, the gradient fails only if fin G_j exceeds roughly
  0.2–14 nS per pair (for 50 µm domains) or 24 nS – 1.6 µS (for 200 µm domains). Strong Cx43 coupling of that size
  is not excluded by anything found.

---

## 5. What this does NOT establish

1. **It does not establish that fin mesenchyme has the surrogate conductance.** Mouse L cells (cultured, 1985) and
   rat cardiac fibroblasts are not zebrafish fin intra-ray fibroblasts or blastema cells. Teleost cells at ~28 °C, in
   teleost ionic conditions, with *kcnk5b*/*kcnh2a* expression, could differ by orders of magnitude. The two
   surrogates already disagree with each other by 1–2 orders.
2. **It does not establish that a ≥10 mV difference exists in fins.** The only fin Vmem evidence (Perathoner 2014,
   DiSBAC₂(3)) is a relative, uncalibrated fluorescence difference between genotypes and regions. It contains no mV.
3. **It does not establish ΔE.** Achieving ΔE ≥ 15 mV requires differential channel expression (for example,
   regional *kcnk5b* or *kcnh2a* levels). Whether fins express channels differentially enough is a separate
   question that is not answered here. If ΔE < 10 mV, no g_m suffices, because the requirement is undefined.
4. **G_j is assumed, not measured.** The 0.2–2 nS range comes from cultured cardiac-fibroblast pairs and a
   channel-count estimate. Cx43-rich tissues can couple far more strongly. *sof* data (oocyte pairs) show fin Cx43
   alleles differ in coupling, but give no in-fin G_j. If fin G_j is ≥10–100 nS, the narrow-domain cases fail even
   with the higher surrogate g_m.
5. **The model omits**: anisotropic coupling (along versus across rays), the epidermis and its transepithelial
   potential, extracellular resistance (which lengthens the effective λ when r_e is not negligible), gating of G_j by
   transjunctional voltage (Rook 1992: gating appears only below ~1–2 nS, so at ΔE ≥ 15 mV gating could *reduce*
   G_j and help), voltage dependence of g_m (Kcnh2a is voltage-gated, so g_m at the resting Vm can differ from any
   single slope value), and cell-to-cell heterogeneity.
6. **The Heubach hMSC current density (11–16 pA/pF at +70 mV) is not a resting conductance.** I deliberately did not
   convert it. Doing so would overstate resting g_m.
7. **The A_cell = 800 µm² and a = 10 µm values are placeholders.** g_m,req scales as a²/A_cell. A 7× larger cell
   (hMSC-sized) lowers g_m,req by ~7×, and a 2× larger pitch raises it 4×.
8. **This is a static (steady-state) persistence argument only.** It does not address the energetic cost of
   maintaining the boundary current, whether downstream readers (calcineurin, according to Daane 2018 and Stewart
   et al.) can decode a 10 mV difference, or whether such a gradient could be re-patterned to serve a gliding
   fin rather than merely a longer one.
9. **Nothing here is an observation of zebrafish fins.** Every fin-specific number in §3 is a computation or an
   assumption.

---

## 6. What would change the answer

* **Decisive measurement:** whole-cell (perforated-patch, to avoid seal-leak bias) input resistance and capacitance
  of acutely dissociated or in-explant zebrafish fin intra-ray mesenchyme, at resting Vm. Ideally it would be done
  in wild type, *alf* (*kcnk5b* gain-of-function) and *lof* (*kcnh2a* cis over-expression).
  - If **g_m ≥ ~5×10⁻⁵ S/cm²**, C2 is satisfied for every case in the grid, given G_j ≤ 2 nS.
  - If **g_m ≤ ~5×10⁻⁷ S/cm²** (two orders below the worst-case requirement), the mechanism is refuted from below
    for 50 µm domains with weak drive. Refuting it for mm-scale domains would need g_m ≤ ~10⁻¹⁰–10⁻⁹ S/cm².
* **Second decisive measurement:** dual-patch or calibrated dye-transfer G_j between neighbouring fin mesenchymal
  cells. A value above the "G_j,max" column in §3 for the relevant domain width breaks C2 regardless of g_m.
* **Calibrated Vmem imaging** (a ratiometric GEVI, or a dye calibrated by a patch electrode in the same tissue) to
  give ΔE and w directly. This replaces two of my four assumed inputs.
* **Design levers, if C2 fails**: raise g_m regionally (over-express a leak K⁺ channel such as *kcnk5b*; each
  doubling of g_m shortens λ by √2), lower G_j regionally (reduced *cx43* coupling, as in *sof* alleles, at a
  known fin-length cost), or widen the patterned domain (w enters λ_max linearly, so g_m,req ∝ 1/w²).

---

### Sources (with read-level)
* Perathoner et al. 2014, PLoS Genet 10:e1004080, PMC3894163. **Full-text** (partial automated read).
* Kohl & Gourdie 2014, J Mol Cell Cardiol 70:37–46, PMC4001130. **Full-text** (partial automated read).
* Heubach et al. 2004, J Physiol 554:659–672, PMC1664789. **Full-text** (partial automated read).
* Hosoi & Slayman 1985, J Physiol 367:267–290, PMC1193063. **Abstract**.
* Rook et al. 1992, Am J Physiol 263:C959–977. **Abstract** (via catalogue records; PubMed blocked).
* Kiseleva et al. 1998, J Mol Cell Cardiol 30:1083–1093. **Listing** (values seen secondhand).
* Daane et al. 2018, Sci Rep 8:10391. **Search-summary**; full text **could-not-access**.
* Stewart et al. (*longfin*/*kcnh2a*), bioRxiv 790329 (PMC8217709 unconfirmed as its published version). **Search-summary**.
* Hoptak-Solga et al. 2008, PMC2429987. **Search-summary**.
* Sundelacruz, Levin & Kaplan 2008, PLoS ONE 3:e3737. **Search-summary**.
* Synovial fibroblast seal-leak figure, J Physiol 2017, PMC5285716. **Search-summary**.

```swarm-result
{"subproblem": "S40", "evidence": "derived",
  "answer": "A syncytial length-constant model requires fin-mesenchyme membrane conductance of roughly 1e-9 to 4.8e-5 S/cm2 (central case ~2e-7) to hold >=10 mV; the two measured mesenchymal surrogates (5-15 uS/cm2 mouse L-cell fibroblasts; ~1-3.3e-4 S/cm2 cardiac fibroblasts in situ) lie above this except in the narrow-domain/strong-coupling corner where one sits ~1 order below, so C2 is not refuted from below, but no fin-mesenchyme conductance or gap-junction conductance has been found, so C2 is not settled.",
  "key_number": "4.8e-5 S/cm2 (worst-case required g_m, computed: dE=15 mV, w=50 um, Gj=2 nS, a=10 um, A=800 um2)",
  "blocked_on": "No measured membrane conductance, junctional conductance, or calibrated Vmem for zebrafish fin mesenchyme found (PubMed unreachable from session; Daane 2018 full text inaccessible)"}
```
