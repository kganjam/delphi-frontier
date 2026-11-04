# S6 (organ): can a lepidotrichial fin ray carry aerodynamic load?

Project: `zebrafish-flight`. Scale: organ. Status: **negative result (derived)**, with one named escape route.

Companion computation: [`S6_calc.py`](S6_calc.py). Every number in §3 comes from that script. Run `python3 docs/research/fish/S6_calc.py` to reproduce it.

---

## 1. The question, stated precisely

The fish is *Danio rerio*: 4 cm long, mass m = 0.4 g, so its weight is W = m·g = **3.92 × 10⁻³ N**. In a steady glide, lift has to equal W. That fixes the mean pressure on the lifting surfaces at p = W/S, where S is the total fin area. **This pressure does not depend on speed.** Speed only decides which lift coefficient C_L the wing must run at.

So the structural question is not tied to speed. It is this: is the fin's flexural rigidity per unit width, D_w (N·m), large enough that a fin of span L, cantilevered from the body and loaded by p, keeps its tip deflection within an aerodynamically usable fraction of L? The fin must also not flutter at the glide speed V = √(2W/(ρ S C_L)).

Three facts make this hard:

- In water a fin is loaded by a distributed pressure of order ½ρ_water·U² at U ≈ 0.1 m/s, which is about 5 Pa. Puri et al. tested it with forces of about 100 µN. A gliding wing small enough to fit a 4 cm fish carries **9–220 Pa** (computed, §3).
- A lepidotrichium is **bilaminar**: two hemirays separated by a soft core, and segmented along its length by joints. Its stiffness in whole-ray bending can therefore sit orders of magnitude below what its bone material would give in a solid section.
- Area and deflection pull in opposite directions. Small fins carry high pressure but have short lever arms. Large fins carry low pressure but deflect as L⁴. §3 shows that, at the measured stiffness, no fin size escapes this.

## 2. What is measured

| # | Quantity | Value | Species / organ | Source (year) | Read-level | Notes |
|---|---|---|---|---|---|---|
| M1 | Whole-fin bending stiffness EI, in vivo, anaesthetised | **1.5 × 10⁻⁹ to 4 × 10⁻⁹ N·m²**, non-monotonic along the proximo-distal axis, peak about 2–4 mm from the fixation point | *D. rerio*, adult caudal fin, AB strain, 6–12 months, 5 fins × 6 positions | Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter, *J. Exp. Biol.* 221:jeb171777 (2018), PMC5868929 | full-text (main text through PMC; supplementary Figs S1, S4 and S5 **could-not-access**) | Euler–Bernoulli fit to force–deflection curves at forces of about 100 µN, deflection ≤ 2 mm, stated accuracy ≥ 10 %. The authors report that cutting the interray tissue made no significant difference, and they conclude that **the rays set the stiffness**. |
| M2 | Fin width at the measurement positions | about 5–8 mm | same | Puri et al. 2018 | full-text | Measured with a digital calliper. |
| M3 | Fin thickness at the measurement positions | 200 µm proximally down to 40 µm distally | same | Puri et al. 2018 | full-text | The authors say this agrees with ray diameters seen in live images. |
| M4 | Ray diameter | 0.1–0.2 mm | *D. rerio* | Puri et al. 2018 | full-text | Given in the Conclusions without method detail, so treat it as an approximate figure. |
| M5 | Ray count | 16–18 caudal rays | *D. rerio* | Puri et al. 2018 | full-text | |
| M6 | Interray tissue tensional modulus | **≤ 4 ± 2 kPa** (the authors call it an upper bound) | *D. rerio* caudal | Puri et al. 2018 | full-text | Model-derived by the authors from k_intact = 0.4 ± 0.1 N/m and k_cut = 0.08 ± 0.04 N/m. |
| M7 | Effective second moment of area of the whole fin | 7 × 10⁻¹⁶ falling to 3 × 10⁻¹⁶ m⁴ | *D. rerio* caudal | Puri et al. 2018 | full-text | **Model-derived** by the authors (their Eqn 4), not measured directly. The ray-level effective modulus appears only in Fig. S5C, so its value is **unknown** here (could-not-access). |
| M8 | Reduced (indentation) modulus of fin-ray bone material | 4.57 ± 2.62 GPa (CTRL_REGEN, proximal) to 8.68 ± 8.74 GPa (ALN_REGEN, proximal). The proximal untreated-control (CTRL) Er is **not quoted numerically** in the text; it is shown only in a Fig. 5 box plot. | *D. rerio* caudal lepidotrichia, OCT-embedded 30 µm cryosections | Bohns, Shih, Chuang, Akhtar & Chen, *JBMR Plus* 5:e10435 (2020), PMC7872341 | full-text (through PMC; the PDF mirror on blob.core.windows.net was blocked by session network policy) | Berkovich tip, 100 nm depth. The paper does not state whether samples were hydrated. The SDs are as large as the means. Hardness is lower distally (CTRL 0.29 GPa proximal vs 0.06 GPa distal). These are **material** values, not whole-ray values. |
| M9 | Pectoral ray count | 10–14, not correlated with body size | *D. rerio* pectoral | *Zoological Letters* paper, doi 10.1186/s40851-019-0145-z (2019) | **search-summary** (link.springer.com blocked by network policy) | Pectoral fin length and ray length in mm: **unknown**. I searched for "adult zebrafish pectoral fin length mm ray number lepidotrichia segment length hemiray thickness µm" and found no numeric dimensions. |
| M10 | Whole-ray "composite" Young's modulus from three-point bending | **10⁸–10⁹ N·m⁻²** | *Lepomis macrochirus* (bluegill) pectoral rays, max ray length 40.3 ± 0.8 mm, 24 rays | Alben, Madden & Lauder, *J. R. Soc. Interface* 4:243–256 (2007; online 2006), PMC2359861 | full-text | Also reports I ≈ 10⁻⁶ cm⁴ and B = EI ≈ 10⁻⁶–10⁻⁵ N·m². Bony segments make up about 30 % of the ray thickness. |
| M11 | Ray stiffness with hemitrich bases clamped vs one base free | 1.98 N/m clamped, **about 12 ×** the free-base value | bluegill | Alben et al. 2007 | full-text | This shows the core-coupling effect directly. |
| M12 | Intraray connective tissue shear modulus | about 10³ Pa (authors' scaling **estimate**) | bluegill | Alben et al. 2007 | full-text | This is an estimate, not a measurement. |
| M13 | Single-ray flexural stiffness | 3.8 × 10⁻⁶ N·m² (as quoted by Puri et al.). A 565 × 10⁻⁶ N·m² figure also appears in a search snippet. | bluegill pectoral | Flammang et al., *J. Morphol.* (2013) | **search-summary / secondary citation** (sites.harvard.edu blocked by network policy) | **The two values disagree by about 150 ×. I cannot resolve which is correct, and I keep both.** Neither is used in any zebrafish computation below. |
| M14 | Homogenised flexural modulus of natural fin rays, "of order 1 GPa"; natural ray diameter "~100 µm" | — | salmonids (cited) | Das, Kunjam, Moling, Gao & Barthelat, *Interface Focus* 14:20230072 (2024), PMC11285607 | full-text | Both values are **cited** from earlier work (their ref. 27), not measured in this paper. |

**Where the sources disagree, and I have kept the disagreement.** The modulus of "fin ray" spans more than three orders of magnitude, depending on what is being measured:

- Bone material by nanoindentation (M8): about 5–9 GPa.
- Homogenised whole ray (M10, M14): 0.1–1 GPa, from bluegill and salmonids.
- Zebrafish whole ray in vivo: my inference in §3.2 places it far below the solid-section value.

These values are not in conflict: they measure different things. They should not be averaged. **For a load question, only the whole-organ value (M1) is relevant.** It is also the only zebrafish whole-structure measurement I found.

**Scope of negative searches.** Using web search plus PMC full text, I found no measured value for any of the following in *D. rerio*: pectoral fin span or chord; hemiray (hemitrich) wall thickness; joint stiffness between segments; torsional stiffness of any fin; fin-ray bone strength; any fin stiffness measured in air or under active (non-anaesthetised) muscle tone. Three hosts were unreachable from this session (sites.harvard.edu, link.springer.com, rcastoragev2.blob.core.windows.net). The JEB supplementary material on cob.silverchair.com was not attempted after those failures. All of these are reported as **unknown**.

## 3. What I computed (all of it is computation, not observation)

### 3.1 Flexural rigidity per unit width, from M1 and M2 (derived)

I bound D_w = EI / width from the measured extremes, without pairing them by position, because the per-position pairing is in the supplement I could not read:

- D_w,low = 1.5 × 10⁻⁹ / 8 × 10⁻³ = **1.9 × 10⁻⁷ N·m**
- D_w,high = 4 × 10⁻⁹ / 5 × 10⁻³ = **8.0 × 10⁻⁷ N·m**

### 3.2 Per-ray consistency check (derived; it explains the mechanism but is not used for the verdict)

Dividing M1 over 16–18 rays gives EI_ray ≈ 0.8–2.5 × 10⁻¹⁰ N·m² (computed).

- **Solid-section prediction.** A solid bone rod with d = 100–200 µm (M4) and E = 4.57–8.68 GPa (M8) would have EI = 2.2 × 10⁻⁸ to 6.8 × 10⁻⁷ N·m². That is **100–8000 × higher** than the per-ray value from the in-vivo measurement.
- **Decoupled-laminae prediction.** Treat the ray as two hemirays that bend independently, each a strip 150 µm wide and t thick (**t is assumed; it has not been measured, see §2**). This gives EI = 1.1–2.2 × 10⁻¹⁰ N·m² at t = 10 µm and 3.9–7.3 × 10⁻¹⁰ N·m² at t = 15 µm. **That matches the in-vivo value.**
- **Inference (mine, not the authors').** In the anaesthetised zebrafish, the measured fin stiffness is consistent with the hemirays acting as nearly uncoupled thin laminae. The bony material is stiff; the architecture is what makes the ray soft. This agrees in direction with the bluegill clamped-vs-free factor of 12 (M11). It is a consistency argument and does not establish the mechanism.

### 3.3 Static deflection of a fin used as a wing (derived)

**Assumptions:**
- (a) Two wings, each a square plate of span L equal to chord c, cantilevered at the body.
- (b) Uniform lift pressure p = W/(2Lc).
- (c) Linear Euler–Bernoulli bending along the span using D_w from §3.1, with the caudal-fin value applied to a pectoral wing (assumed transferable).
- (d) Tip deflection δ = p·L⁴/(8·D_w·L) = p·L³/(8·D_w).
- (e) **Aerodynamic tolerance δ/L ≤ 0.10.** For a uniform-load cantilever this means a tip slope of about 7.6°. This tolerance is my assumption; the project has not set one.
- (f) Glide speed at C_L = 1.0 (assumed) with ρ_air = 1.2 kg·m⁻³.
- (g) Areal fin density μ = 1100 kg·m⁻³ × 100 µm = 0.11 kg·m⁻² (assumed, from the M3 thickness range).

| L = c | Total S | p = W/S | V_glide (C_L = 1) | δ/L at measured D_w | D_w required for δ/L ≤ 0.1 | Shortfall (required/measured) | Self-weight sag δ/L, in air, no flow |
|---|---|---|---|---|---|---|---|
| 3 mm | 18 mm² | 218 Pa | 19.1 m/s | 0.92–3.9 | 7.4 × 10⁻⁶ N·m | **9–39 ×** | 0.00–0.02 |
| 5 mm | 50 mm² | 78.5 Pa | 11.4 m/s | 1.5–6.5 | 1.2 × 10⁻⁵ N·m | **15–65 ×** | 0.02–0.09 |
| 10 mm | 200 mm² | 19.6 Pa | 5.7 m/s | 3.1–13 | 2.5 × 10⁻⁵ N·m | **31–131 ×** | 0.17–0.72 |
| 15 mm | 450 mm² | 8.7 Pa | 3.8 m/s | 4.6–20 | 3.7 × 10⁻⁵ N·m | **46–196 ×** | 0.57–2.4 |

For a square wing, D_w,req = W·L/(16·tol). The requirement therefore **falls as the wing shrinks**, but only linearly in L. Meeting it at the measured D_w,high would take L ≈ 0.33 mm, which needs V ≈ 170 m/s (computed). There is no workable fin size. Every δ/L value above 1 is outside linear theory: what it means physically is that the fin folds or feathers rather than holding a lifting shape. The linear formula does not predict what it does after that point.

The self-weight column shows that a fin of 10 mm or more would also sag 17–72 % of its span **under its own weight in still air**, with no aerodynamic load at all (computed).

**Strength (rough, derived).** At L = c = 10 mm the root moment per wing is 9.8 × 10⁻⁶ N·m. Spread over 12 rays, with each hemiray carrying half (decoupled laminae, t = 15 µm, w = 150 µm), the bending stress is about 70 MPa. A fin-ray bone strength is **unknown** (none found), so I cannot say whether the ray would break. Stiffness fails long before this point anyway.

### 3.4 Flutter (a proxy only; a true flutter speed is unknown)

A classical bending–torsion flutter speed needs a torsional stiffness and the position of the elastic axis. No measurement of either exists for any zebrafish fin, so **the flutter speed is unknown**. As a proxy I computed the first cantilever bending frequency, f₁ = (1.875²/2π)·√(D_w/(μ·L⁴)), where μ is assumed (§3.3 g) and air added mass (about 9 % of μ) is neglected. I then found the airspeed at which the reduced frequency k = π·f₁·c/U falls to 0.1. That is a heuristic threshold below which the structure no longer responds quickly relative to the flow. It is not a flutter criterion.

| L = c | f₁ | U at k = 0.1 | V_glide |
|---|---|---|---|
| 3 mm | 81–168 Hz | 7.6–15.8 m/s | 19.1 m/s |
| 5 mm | 29–60 Hz | 4.6–9.5 m/s | 11.4 m/s |
| 10 mm | 7.3–15 Hz | 2.3–4.7 m/s | 5.7 m/s |

At every size, the glide speed is above the k = 0.1 speed. This points the same way as §3.3: the structure is aeroelastically soft at the speeds it would need to fly. It is **not** a computed flutter boundary.

### 3.5 Interray membrane (derived, secondary)

Assume ray spacing s = 0.4 mm and membrane thickness 40 µm (both assumed), with E ≤ 4 kPa (M6) and p = 20 Pa. A pretension-free membrane strip then bulges w/s ≈ (3ps/(64Eh))^(1/3) ≈ 0.13 between rays. Because 4 kPa is an upper bound, the true bulge is at least this. This is not the deciding failure, but the membrane would add uncontrolled camber.

## 4. The answer

**No. At the stiffness measured in zebrafish, a lepidotrichial fin cannot carry gliding lift for a 0.4 g zebrafish.**

Evidence level: **derived**. The verdict comes from a beam calculation built on one measured in-vivo whole-fin stiffness (Puri et al. 2018, caudal fin) and on stated assumptions. Two points about scope:

- Nothing here was simulated, and nothing was observed in air.
- The conclusion holds even though no flutter speed could be computed. It is set by **static** deflection under steady 1 g lift.

For any square fin-wing between 3 and 15 mm, the flexural rigidity needed to hold tip deflection to 10 % of span is **9 to 196 times** the rigidity derived from the measured value. The shortfall is smallest at the smallest wing, and there it requires a glide speed of about 19 m/s.

The per-ray check (§3.2) suggests why. The bone material (about 5–9 GPa) would be stiff enough in a solid section: the required per-ray EI at L = 10 mm is about 2 × 10⁻⁸ N·m², and a bonded solid ray of 100–200 µm would give 2 × 10⁻⁸ to 7 × 10⁻⁷ N·m². The ray appears soft because the hemirays bend as nearly decoupled laminae. That last statement is my inference, not a finding of any of the cited authors.

## 5. What this does NOT establish

1. **It is not a pectoral-fin measurement.** M1 is from the caudal fin. Using it for a pectoral "wing" is an assumption. Pectoral rays may differ in thickness, ray count (10–14 vs 16–18), and the coupling between hemirays. Pectoral span and chord in adult *D. rerio* are **unknown** here.
2. **It is not a measurement under active control.** Puri et al. measured anaesthetised fish (MS-222). In bluegill, fixing both hemitrich bases raises ray stiffness about 12 × compared with one free base (M11). Living fish may stiffen rays with muscle. An assumed 12 × gain would turn the 9–196 × shortfall into 0.8–16 × (computed from the table). That would still leave a gap at 5–15 mm (1.3–5.5 × at 5 mm). It **could** close it at 3 mm (0.8–3.3 ×), at a glide speed of about 19 m/s. I have not shown that zebrafish can produce such a gain. The comparison is in fact not like-for-like: Puri's fins had both bases attached, not one base free.
3. **It is not a large-deflection or nonlinear analysis.** Every δ/L above about 0.3 is outside the linear model. The real fin might reach some large-deflection equilibrium, such as feathering into a low-angle lifting shape, that a linear beam cannot represent. I have not shown that a deeply bent fin produces no useful lift. I have only shown that it cannot hold the shape a rigid-wing analysis assumes.
4. **It does not compute a flutter speed.** Torsional stiffness and the position of the elastic axis are unmeasured. The k = 0.1 figure in §3.4 is a heuristic, not a stability boundary.
5. **It does not test strength or fatigue.** Fin-ray bone strength is unknown. The 70 MPa estimate depends on an assumed hemiray thickness.
6. **It does not show that flexibility is necessarily fatal.** The 10 % tolerance is my assumption. Flexible insect and bat wings generate lift while deforming substantially. The real tolerance must come from the aerodynamics subproblem. If that tolerance turns out to be about 1–4 × span (meaning "the wing may fold"), the verdict changes, but only for a very unusual aerodynamic design.
7. **It does not cover other load paths.** I did not analyse bracing, chordwise tensioning, or a wing that is not cantilevered (for example, one supported along its leading edge by an enlarged, fused first ray). Nothing here rules out a leading-edge spar made of fused rays.
8. **The bone modulus is uncertain.** M8 values have SDs equal to their means, an unstated hydration state, and come from regenerating or drug-treated fins. The §3.2 mechanism inference depends on them and on an **assumed** hemiray thickness of 10–15 µm.
9. **It says nothing about flapping flight.** Inertial and dynamic loads in flapping would make the problem worse, not better, but I did not compute them.
10. **It does not use the Flammang 2013 bluegill value** (M13), because I could read neither the source nor its correct magnitude.

## 6. What would change the answer

- **A measured zebrafish (pectoral) fin rigidity D_w ≥ about 7 × 10⁻⁶ N·m**, roughly EI ≥ 2 × 10⁻⁸ N·m² per ray, would make a 3 mm square wing (19 m/s glide) structurally adequate at δ/L ≤ 0.1. This is the refutation criterion. It would have to be measured on the pectoral fin, ideally in a non-anaesthetised fish or with the hemiray bases clamped.
- **An aerodynamic tolerance looser than about δ/L ≈ 1** (from the aerodynamics subproblem), together with evidence that a passively folded fin still lifts, would weaken or overturn the result.
- **Design change: couple the hemirays.** If the soft intraray core were made stiff in shear (fused or mineralised, or the hemirays bonded), the §3.2 arithmetic says per-ray EI would rise toward the solid-section range of 2 × 10⁻⁸ to 7 × 10⁻⁷ N·m². That is enough for wings up to about 10 mm under the stated assumptions. This is the single most promising lever. It is a derived claim and has not been demonstrated. It hands a question to the tissue and gene scales: what controls the joint and core compliance between hemirays?
- **Design change: thicker hemirays.** Laminar stiffness grows as t³, so going from t ≈ 10–15 µm to about 40–60 µm (assumed baseline) would gain roughly 20–200 × without coupling. Whether lepidotrichia can be thickened that much is unknown.
- **Design change: a spar instead of a cantilevered fan**, such as a fused leading-edge ray, or a chordwise-braced wing. This would change the load path, and the analysis would need to be redone.
- **Getting the blocked sources** could narrow, but not reverse, the numbers: Puri 2018 Figs S1, S4 and S5 (ray-level effective modulus and I_eff), Flammang 2013 (bluegill ray EI, and settling the 3.8 × 10⁻⁶ vs 565 × 10⁻⁶ N·m² disagreement), and the Zoological Letters 2019 pectoral dimensions.

---

```swarm-result
{"subproblem": "S6", "evidence": "derived",
  "answer": "No: at the in-vivo measured zebrafish fin rigidity (EI 1.5-4e-9 N m^2 over 5-8 mm, i.e. 1.9-8.0e-7 N m per width) a cantilevered lepidotrichial fin-wing carrying 1 g gliding lift for a 0.4 g fish deflects 0.9-20 x its span, 9-196 x short of the rigidity needed for tip deflection <= 10% span at any wing size 3-15 mm; bone material is stiff enough, the decoupled bilaminar architecture is not (inference).",
  "key_number": "required/measured flexural rigidity >= 9x (D_w required >= 7.4e-6 N m vs measured-derived <= 8.0e-7 N m, 3 mm square wing)",
  "blocked_on": "pectoral-fin (not caudal) stiffness and dimensions in D. rerio; active-muscle stiffness; torsional stiffness for a true flutter speed; hemiray thickness; Puri 2018 supplement and Flammang 2013 full text (hosts blocked by session network policy)"}
```
