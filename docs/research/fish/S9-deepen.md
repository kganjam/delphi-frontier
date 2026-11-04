# S9-D: Deepening S9 (fin-ray bone and actinotrichia properties) by attacking its weakest input

Project: `zebrafish-flight` · Scale: tissue · Date: 2026-11-04
Parent: `docs/research/fish/S9-tissue.md` on branch `origin/claude/s9-fin-ray-materials-t0royp`
(not on `main`). Calculation script: `docs/research/fish/S9-deepen_calc.py`. Every number it prints is
a **calculation**, not an observation.

Read-level legend: full-text | abstract | listing | search-summary | could-not-access.

---

## 0. What S9 concluded

S9's prompt arrived with an empty "recorded answer" field. So I took the answer from S9's own
deliverable (`S9-tissue.md`, §4 and the swarm-result block). Its load-bearing conclusion was:

> "The key number for organ-scale work is the **proximal fin-ray modulus, 1.34 GPa (range
> 0.24–3.7 GPa, bluegill, search-summary)**."

S9 also read the zebrafish "effective modulus ~8 MPa" (its item Z2, a secondary citation) as an
artefact of using the I of the *whole fin plate including soft tissue*. On that reading, the MPa
figure was not comparable to a bone modulus (S9 §2d.3).

Every S9 read was search-summary. The network policy blocked the full-text hosts.

## 1. The input S9 is most sensitive to: the second moment of area I used to turn EI into E

**No fin-ray "Young's modulus" in S9 is measured directly.** The bluegill 1.34 GPa and the
zebrafish ~8 MPa are both computed as E = EI / I. EI is the measured flexural stiffness. I is a
cross-section that the authors **assumed**. So the conclusion depends on I, and I depends on which
cross-section model you assume.

There is one measured zebrafish datum, which I read at **full-text** this time: the in-vivo
whole-caudal-fin EI of **1.5×10⁻⁹ – 4×10⁻⁹ N·m²** (Puri et al. 2018, *J. Exp. Biol.*
221:jeb171777, PMC5868929). I recomputed the E it implies under each cross-section model, using
these inputs:

- 16–18 rays (Puri, full-text).
- Ray diameter 0.1–0.2 mm (Puri, full-text).
- Hemitrich wall thickness t = 15 µm. Source: §3.

Per-ray EI (calc) = 1.5e-9/18 … 4e-9/16 = **8.3×10⁻¹¹ – 2.5×10⁻¹⁰ N·m²**. This assumes the line
load is shared by all rays. Puri's interray-cut experiment supports that, because cutting changed
nothing (full-text).

| Cross-section model, D = 150 µm (calc) | I per ray (m⁴) | E implied by measured EI (calc) |
|---|---|---|
| Solid rod (≈ Puri's own Fig. S5B) | 2.5e-17 | **3.4 – 10 MPa** |
| Hemitrichs bonded, hollow tube, t = 15 µm | 1.5e-17 | 5.7 – 17 MPa |
| Hemitrichs uncoupled, semicircular crescents, t = 15 µm | 2.8e-18 | 30 – 89 MPa |
| Hemitrichs uncoupled, 60° half-angle crescents | 5.1e-19 | 164 – 493 MPa |
| Hemitrichs uncoupled, flat plates w = 150 µm, t = 15 µm | 8.4e-20 | **0.99 – 2.96 GPa** |
| (30° crescents; chord only 67 µm, so not directly comparable) | 5.4e-20 | 1.6 – 4.7 GPa |

**Sensitivity, recomputed rather than asserted (calc):**

- **Choice of model.** The same measured EI gives an E anywhere from **3.4 MPa to ~3–4.7 GPa**.
  That is a span of about **900×**. Only the uncoupled thin-plate model reproduces the 1.34 GPa
  bluegill proxy.
- **Hemitrich thickness t inside the uncoupled flat-plate model.** E ∝ t⁻³, so a factor-2 error in t
  is an **8×** error in E.
  - t = 7.5 µm → 7.9–23.7 GPa. This reaches the zebrafish vertebral nanoindentation ceiling of
    ~23–25 GPa.
  - t = 15 µm → 0.99–2.96 GPa.
  - t = 30 µm → 0.12–0.37 GPa.
  - The flat-plate model needs E above 25 GPa if t < **7.4 µm** (calc).
- **Ray diameter D.** In the flat-plate model E ∝ 1/D. Halving D (200 → 100 µm) only raises E by 2×.
  D is not the dominant input.
- **Forward check (calc).** Plug E = 1.34 GPa into the bonded-tube model with 17 rays. It predicts a
  whole-fin EI of 3.3×10⁻⁷ N·m², about **80–220× stiffer than Puri measured**. With the uncoupled
  flat-plate model it predicts 1.9×10⁻⁹ N·m², inside the measured 1.5–4×10⁻⁹ range.

So a factor-2 change in t would move S9's key number across the interval "tendon-like ~1 GPa"
→ "bone-tissue ~20 GPa". A factor-2 error in the model's I moves E by exactly 2×. The *model
choice* moves it by ~900×. **The single input is the I assigned to the ray.** Under the
physically supported model (§2), I is controlled by hemitrich wall thickness t.

## 2. How well is that input established?

**Bluegill 1.34 GPa (S9 L1).** Still search-summary only. The Lauder et al. 2011 abstract could not
be retrieved: Crossref returns no abstract and the publisher (IOP) was not tried, because S9 had
found it blocked. **How Lauder et al. estimated I is unknown.**

My inference, not the authors' claim: the 1.34 GPa figure **must rest on a hemitrich-only,
thin-wall I**. Puri cites a bluegill ray EI of 3.8×10⁻⁶ N·m² (citing Flammang et al. 2013; read
via Puri, full-text). Applied to a solid bluegill ray of D = 1–2 mm, that EI gives only
**4.8–77 MPa** (calc). A GPa figure is only reachable with a much smaller I.

**Zebrafish ~8 MPa (S9 Z2).** Now **full-text**, and S9's interpretation of it **falls**.

- Puri et al. computed two I's. Fig. S5A is a homogeneous whole-fin plate, 0.72→0.30×10⁻¹⁵ m⁴.
  Fig. S5B is **rays only**: "taking into account only the rays and their change in thickness
  along the length of the fin for every ray and adding up all these contributions", giving
  ~0.28–0.50×10⁻¹⁵ m⁴, read off the plot.
- The effective modulus in Fig. S5C uses the **ray-only** I. Read off the plot, it is
  **~1.9 to ~11 MPa** across 5 fish, peaking at 2.5–4.5 mm from the fixation.
- So the MPa figure is **not** a soft-tissue artefact, as S9 thought. It is the ray modulus under a
  solid-rod I.
- My solid-rod row above (3.4–10 MPa, calc) reproduces it independently. 17 rods × 2.5e-17 =
  4.2×10⁻¹⁶ m⁴, inside Puri's S5B range.

**Which I is physically right?**

- **Author claim** (Das, Hannard & Barthelat 2023, *Acta Biomater.*, PMID 37364788, **abstract**),
  for rainbow-trout rays tested at large deflection: the collagenous core "can be modeled with
  spring elements which are 3-4 orders of magnitude more compliant than the hemitrichs" and
  "provides negligible resistance to shearing from the initial position".
- **My inference:** for small deflections, the two hemitrichs bend nearly uncoupled. The
  "bonded tube" and "solid rod" I's (Puri's S5B, and S9's C2 table) therefore overstate I by
  ~170–300× and understate the bone modulus by the same factor. This is an inference across
  species (trout → zebrafish) and across loading regimes. It is not a zebrafish measurement.
- **Author claim** (Aiello et al. 2018, *J. Morphol.* 279:1031, **abstract**): in labrids, I "was
  always significantly correlated with fin ray flexural stiffness" and explained most of its
  variation, while E "was similar between species". This supports the view that geometry, not
  material, is the input that moves.

**Evidence level of the input as S9 used it:** a **proxy** (different species) for a **derived**
quantity (E = EI/I) whose I was **assumed and not reported** (Lauder 2011 method unseen). It was an
assumption that had been repeated until it read as measured. The "~1 GPa" in the 2024
*Interface Focus* paper (PMC11285607, full-text) is attributed there to Aiello et al. 2018 as a
"homogenized flexural modulus". The word "homogenized" confirms that this is a structural, not a
material, figure.

## 3. Improving it: a measured zebrafish hemitrich thickness

I looked for a direct measurement of zebrafish hemiray (hemitrich) wall thickness.

**Found (full-text, figure read).** The hox13 triple-mutant study, *PLoS Genet.* 2026, PMC12956070,
"Combined mutations of hoxa13a, hoxa13b, and hoxd13a lead to structural shifts in zebrafish soft
fin rays". Method and values:

- Micro-CT, hemiray cross-sections reconstructed at standard proximal–distal positions, n = 3
  fish per group.
- Fig. 7E plots wild-type "hemiray width (µm)". From the scale bar in Fig. 7B, this is the radial
  wall thickness of each crescent.
- I read the bar heights off the plot to ±~1 µm. These are **my readings, not tabulated values**:
  - ray A2: **~15 µm** (1000 µm), **~16 µm** (750 µm), **~16.5 µm** (500 µm)
  - ray A4: **~14 µm** (750 µm), **~15 µm** (500 µm)
  - ray A6: **~11.5 µm** (500 µm)
- Text, author claim: mutant hemirays are "between 2 and 2.5 times thicker compared to wildtype at
  every position analyzed".
- Fig. 7D traces show **crescent ("( )")** cross-sections, not flat plates. Taft 2011
  (*J. Morphol.*, abstract) also describes segmented hemitrichia as "crescent shape in cross
  section".

Caveats on this input:

- It is the **dorsal** fin, not the caudal. The fish were SL = 3.2 cm; Puri's caudal-fin fish were
  6–12 months old and their size is not stated.
- Positions run 500–1000 µm from the ray base, while Puri's bending positions are 1–6.5 mm.
- t is therefore **measured in zebrafish but in a different fin**. Its transfer to the caudal fin is
  an assumption.

**Not found (negative result, scope stated).**

- Searched for any zebrafish caudal-fin hemitrich wall thickness, crescent arc angle, or measured
  hemitrich-only I.
- Scope: Europe PMC queries on zebrafish + (hemiray | hemitrich | lepidotrichia) + (thickness |
  µm | micro-CT); "fin ray bone thickness regeneration"; hemitrich + (bending | stiffness).
  Roughly 60 titles screened. Full text grepped for 6 open-access papers: PMC5868929, PMC12956070,
  PMC5722281, PMC5171864, PMC11285607, PMC5454310.
- Result: no caudal-fin value.
- Not searched: Scopus, Web of Science, and paywalled journals (Lauder 2011 IOP; Alben 2007 not in
  Europe PMC full-text; Das 2023 Elsevier).

**Also noted.** Nguyen et al. 2017 (*J. R. Soc. Interface*, PMC5454310, full-text) give a
fin-ray bone modulus of "4–20 GPa". They cite **human/mammalian** bone papers for it (Reilly 1974;
Choi 1990; Rho 1998), checked in the reference list. That is a borrowed assumption, not a fish
measurement, so it is a further example of a repeated assumption.

**What measurement would settle the zebrafish fin-ray material E, and what it would cost.** My
estimates, not quoted prices:

1. **Micro-CT of the same caudal fins that are bending-tested.** Resolution ≤ 2 µm, because
   t ≈ 15 µm and E ∝ t⁻³ needs t to within ~5% for ~15% in E. This gives per-segment hemitrich I
   from the actual crescents. Cost: one benchtop µCT session, ~5–10 fins, roughly 1–2 instrument
   days. Core-facility rates are commonly in the low hundreds of USD per hour (unverified), so of
   order USD 2–5k.
2. **Nanoindentation of polished hemitrich cross-sections.** This gives material E directly, with
   no I, at ~10 µm length scale, wet. Cost: embedding plus 1–2 instrument days, of order
   USD 2–5k (estimate).
3. **The decisive check.** Combine (1) and (2) in a forward model: E_nano × I_µCT, uncoupled vs
   coupled, compared against Puri-type in-vivo EI on the same fish. The ratio separates material
   from joint and coupling compliance. The total is of order USD 10k and a few weeks, given an
   existing Puri-type rig.

## 4. Recompute S9's conclusion with the improved input

Improved input: measured WT hemiray t = **11–16.5 µm** (micro-CT, zebrafish dorsal fin), with the
uncoupled-hemitrich model (trout, abstract-level author claim) and the measured caudal-fin EI
(Puri, full-text).

Recomputed (calc), flat-plate bound, w = 150 µm:

- t = 16.5 µm → **0.74–2.2 GPa**
- t = 11 µm → **2.5–7.5 GPa**
- Envelope over D = 100–200 µm and t = 11–16.5 µm: **~0.6–11 GPa**

Treating hemitrichs as curved crescents raises I, so this flat-plate bound is the **highest** E an
uncoupled model allows. Semicircular crescents give ~30–90 MPa; 60° crescents give ~160–490 MPa.

What this means:

1. **S9's key number does not survive as an organ-scale input. It falls.**
   - With the measured zebrafish t, "fin-ray E" is anywhere from **~3 MPa** (Puri's ray-solid-rod
     definition, full-text: 1.9–11 MPa) to **~0.6–11 GPa** (uncoupled thin plates, calc). The
     answer depends on a coupling and crescent-shape assumption that no zebrafish measurement fixes.
   - 1.34 GPa is *consistent with* zebrafish only under the uncoupled flat-plate model. It is
     inconsistent by 80–220× under the bonded-tube model.
   - A bare E is not a usable organ-scale input. It has meaning only when paired with the I it was
     derived from.
2. **S9's reading of the ~8 MPa figure falls.** It is the rays' effective modulus with a solid-rod
   I (Puri Fig. S5B/C, full-text), not a whole-plate soft-tissue artefact.
3. **What replaces it.** Organ-scale work should carry the measured zebrafish flexural stiffness:
   **whole caudal fin EI = 1.5–4×10⁻⁹ N·m²** (Puri 2018, full-text), or **per ray ≈ 0.8–2.5×10⁻¹⁰
   N·m²** (calc, ÷16–18 rays). This sidesteps E entirely. Any design that *changes* ray dimensions
   still needs E and I separately. For that it must use E ∝ t⁻³ under the uncoupled model, with
   t = 11–16.5 µm as the measured (dorsal-fin) baseline.
4. **One inference worth flagging, not established.** Under the uncoupled flat-plate bound, the
   implied 0.6–11 GPa sits below zebrafish vertebral nanoindentation E (~23–25 GPa; search-summary
   only, S9 B3/B4). So either the joints add compliance, or the crescents are flatter than they
   look, or the foam-pad fixation in Puri's rig adds root compliance and lowers the apparent EI.
   That last is my hypothesis; Puri benchmarked steel and polyimide cantilevers but does not
   describe how they were clamped relative to the fish. None of these three is separated by any
   data I found.

**Unchanged from S9 (stands).**

- No measured fin-ray strength.
- No fin-ray density.
- No property of teleost actinotrichia.

This deepening did not search those again, so the S9 negative-search scope still applies to them.

## 5. Disagreements preserved

| Quantity | Value | Source | Read-level | Definition of I |
|---|---|---|---|---|
| Bluegill proximal ray E | 1.34 GPa (0.24–3.7) | Lauder et al. 2011 | search-summary | unknown |
| Labrid ray "homogenized flexural modulus" | "~1 GPa" | Aiello 2018, as cited by Interface Focus 2024 | full-text (citing paper); abstract (Aiello) | not stated in abstract |
| Zebrafish caudal ray effective E | ~1.9–11 MPa | Puri 2018 Fig. S5C | full-text (plot read) | rays as solid sections, summed |
| Zebrafish ray E, uncoupled thin plates | 0.6–11 GPa | this file | calculation | flat hemitrichs, t measured in dorsal fin |
| Fin-ray bone E used in a model | 4–20 GPa | Nguyen 2017 | full-text | n/a (borrowed from mammalian bone) |
| Zebrafish vertebral bone E | ~23–25 GPa | Fiedler 2018 and one other | search-summary | n/a (nanoindentation) |

These are not averaged. They differ by up to ~10⁴ because they are **different quantities**:
structural modulus under four different I definitions, versus material modulus.

## Sources

- Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). In vivo quantification of mechanical
  properties of caudal fins in adult zebrafish. *J. Exp. Biol.* 221:jeb171777. PMC5868929.
  **full-text, including supplementary Figs. S1–S6.**
- hox13 triple-mutant paper (2026). Combined mutations of hoxa13a, hoxa13b, and hoxd13a lead to
  structural shifts in zebrafish soft fin rays… *PLoS Genet.* doi 10.1371/journal.pgen.1012055,
  PMC12956070. **full-text** (text and Fig. 7). Author list not transcribed here.
- Das S, Hannard F, Barthelat F (2023). Mechanics and properties of fish fin rays in nonlinear
  regimes of large deformations. *Acta Biomater.* PMID 37364788. **abstract.**
- Aiello BR, Hardy AR, Cherian C, Olsen AM, Orsbon CP, Hale ME, Westneat MW (2018). *J. Morphol.*
  279:1031–1044. PMID 29693259. **abstract.**
- Taft NK (2011). Functional implications of variation in pectoral fin ray morphology… *J. Morphol.*
  PMID 21626534. **abstract.**
- Stiff morphing composite beams inspired from fish fins (2024). *Interface Focus*. PMC11285607.
  **full-text** (grepped for moduli; read in part).
- Nguyen K, Yu N, Bandi MM, Venkadesan M, Mandre S (2017). Curvature-induced stiffening of a fish
  fin. *J. R. Soc. Interface*. PMC5454310. **full-text** (grepped; modulus sentence and reference
  list read).
- Lauder GV et al. (2011). *Smart Mater. Struct.* 20:094014. **search-summary** (via S9). Crossref:
  no abstract. Full text: could-not-access.
- Flammang BE et al. (2013). *J. Morphol.* 274:1044. Bluegill ray EI 3.8×10⁻⁶ N·m², **as cited by
  Puri (full-text)**. Primary: not accessed.
- Alben S, Madden PG, Lauder GV (2007). *J. R. Soc. Interface* 4:243. Europe PMC full-text:
  could-not-access (empty response).
- Petersen JC, Ramsay JB (2020). Walking on chains… *J. Exp. Biol.* PMID 32709626. **abstract** (no
  modulus in the abstract).

```swarm-result
{"subproblem": "S9-D", "evidence": "literature (Puri 2018 and hox13 2026 at full-text; trout coupling claim at abstract; bluegill 1.34 GPa still search-summary)",
  "answer": "S9's key number (bluegill fin-ray E = 1.34 GPa) is an E = EI/I figure whose I is assumed; recomputing from the full-text zebrafish in-vivo fin EI with micro-CT-measured hemitrich wall thickness (11-16.5 um, dorsal fin) shows the implied 'fin-ray modulus' spans ~3 MPa (solid-rod I, Puri's own definition) to ~0.6-11 GPa (uncoupled thin hemitrichs, calculated), with E scaling as t^-3, so a bare E is not a usable organ-scale input and the measured EI should be carried instead.",
  "key_number": "zebrafish caudal fin EI = 1.5-4e-9 N m^2 (in vivo, measured; ~0.8-2.5e-10 N m^2 per ray, calculated), with hemitrich wall thickness t = 11-16.5 um (micro-CT, dorsal fin) controlling any derived E as t^-3",
  "verdict": "falls"}
```
