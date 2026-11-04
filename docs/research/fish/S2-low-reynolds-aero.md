# S2: Low-Reynolds aerodynamics of a zebrafish-scale wing

**Question.** What is the best aerodynamic performance a zebrafish-scale wing can physically get,
and is the honest route gliding or flapping?

**Short answer.**

1. A 1–3 cm chord at 0.5–8 m/s in air gives **Re ≈ 170–16,000**. Most of the operating range is
   **Re 10³–10⁴** (computed, §1). That is insect territory, one to two decades below the flying
   fish, and conventional airfoil data does not apply there.
2. In that regime, sources I could reach agree that **thin, sharp-edged, slightly cambered plates do
   at least as well as profiled airfoils, and usually better**. Measured steady **CL_max values reported are about 0.8–1.07**, with
   **CD_min < 0.06** for insect-wing sections near Re 10⁴ (§2). A ray-supported fin membrane is
   geometrically that kind of section. **This is a real advantage**, not a handicap (§3).
3. **Steady L/D ceiling.** The best whole-wing values reported near this Re are **≈ 6–7 (locust,
   Jensen 1956)** and **≈ 5.8 (dragonfly forewing)**, both relayed second-hand. Measured whole
   flying fish reach **≈ 4.4–5.9**, not 5–10. For a fin wing with a fish body attached I estimate
   **L/D ≈ 3–5**. That is an estimate, not a measurement. **No glide of a fish-derived wing at
   this Re has ever been measured; the actual value is `unknown`** (§4).
4. **From a 0.5 m launch, L/D barely matters.** The equilibrium glide speed is 2.3–4.9 m/s
   (computed). Reaching it from rest takes 0.2–1.2 m of drop, so a 0.5 m launch is spent almost
   entirely on the transient. Starting at rest, the computed range is **1–4 body lengths**. With
   a 2 m/s horizontal launch it is **18–63 body lengths**, against **16 body lengths** for no wing
   at all. The ideal `h·L/D` figure of 25–75 body lengths applies only if the fish already arrives
   on the glide path at glide speed (§5).
5. **Flapping.** Revolving or flapping insect-like wings get **CL ≈ 1.75 at Re ≈ 8,000** from a
   stably attached leading-edge vortex (Usherwood & Ellington 2002, relayed). That is roughly
   1.6–2× the steady CL_max. The catch is that hovering insects run mean **lift/drag ≈ 1**: you
   buy force, not efficiency. Weight-supporting flapping for a 0.4 g fish needs about
   **19–52 Hz at 90–120° stroke amplitude** (computed). Larval zebrafish pectoral fins beat at
   **≈ 28–30 Hz in water** (relayed), but that is at small amplitude and without carrying body
   weight. **Whether an adult fin can be driven at that amplitude, frequency and power in air is
   an actuation question this aerodynamic analysis cannot answer: `unknown`** (§6).

**Verdict.** The *best physically available* aerodynamics is the flapping regime: CL ≈ 1.5–1.8
from a stable LEV on a revolving low-aspect-ratio plate, which a fin geometry suits well. The
*honest near-term path* is **gliding**, but gliding from 0.5 m buys tens of body lengths at best,
mostly from the launch speed rather than from the wing. If the goal is more than a short assisted
leap, the bottleneck is **not aerodynamics**. It is the S-problem that delivers ~20–50 Hz,
~100°-amplitude fin strokes with enough muscle power. That problem should be named and handed off,
not assumed solved.

---

## Provenance and read-level

**Network constraint, stated up front.** This session's network policy denied the publisher and
index hosts: `journals.biologists.com`, `cob.silverchair.com`, `ncbi.nlm.nih.gov`,
`europepmc.org`, `arxiv.org`, `doi.org`, `api.crossref.org`, `semanticscholar.org` and
`openalex.org`. Positive control: `pypi.org` returned 200 through the same proxy, so the probe was
working. The proxy log records `journals.biologists.com:443` refused with a 403 on CONNECT.
**No full text was read for this document.** Everything sourced came through a web-search tool
that returns a model-written summary of the pages it found. That is weaker than reading the
abstract myself. Read-levels used:

| Code | Meaning |
|---|---|
| **A** | Abstract-level content of the cited paper itself, as relayed by a search summary. I did not open the page. |
| **S** | Secondary: the number appears in a *citing* paper or a press/interview piece, relayed by a search summary. The primary was not read and the attribution may be wrong. |
| **M** | Remembered, not retrieved. Background mechanism only; it carries no numbers. |
| **C** | Computed by `S2_calcs.py` in this directory from stated assumptions. Not a measurement. |

Per CONTRIBUTING-VERIFICATION rule 9, I checked every number that *helps* the fish case for its
source. Several turned out to be relayed rather than read, and they are marked **S**.

---

## 1. Reynolds-number grid (C)

`Re = U·c/ν`, with ν = 1.5×10⁻⁵ m²/s.

| chord \ U | 0.5 m/s | 1 m/s | 2 m/s | 3 m/s | 5 m/s | 8 m/s |
|---|---|---|---|---|---|---|
| 5 mm | 167 | 333 | 667 | 1,000 | 1,667 | 2,667 |
| 10 mm | 333 | 667 | 1,333 | 2,000 | 3,333 | 5,333 |
| 15 mm | 500 | 1,000 | 2,000 | 3,000 | 5,000 | 8,000 |
| 20 mm | 667 | 1,333 | 2,667 | 4,000 | 6,667 | 10,667 |
| 30 mm | 1,000 | 2,000 | 4,000 | 6,000 | 10,000 | 16,000 |

The speeds a 0.4 g fish actually flies at follow from its wing loading (§5): 2–5 m/s gliding and
about 2–3 m/s mean wing speed in flapping. At a 15 mm chord that puts it at **Re ≈ 2,000–5,000**.
That matches the dragonfly glide range (Re 700–2,400, Wakeling & Ellington 1997, **S**) and the
hawkmoth hover case (Re ≈ 7,300–8,100, **S**). These are the correct reference animals, not
flying fish.

**About the flying-fish Re.** The task states Re ~10⁵–10⁶. I could not retrieve a Cypselurus fin
chord. If the chord were 3–8 cm (an assumption) at the ≈ 10 m/s approach speed relayed from
Davenport 1994 (**S**, via a Wikipedia summary), Re_chord would be 2×10⁴–5×10⁴ (C). The 10⁵–10⁶
figure is probably body-length-based. Either way flying fish sit **≥ 1 decade above** the zebrafish
wing, and the regime gap the task describes is real.

---

## 2. Measured performance at Re 10³–10⁴

| Source | Re | What was measured | Reported value | Read |
|---|---|---|---|---|
| Wakeling & Ellington 1997, *J Exp Biol* 200:543 (dragonfly wings, wind tunnel) | 700–2,400 | Steady CL_max of real wings | **0.93–1.07** (Sympetrum ≈ 1.05–1.07; other species ≈ 0.7–0.9). They also reported that the CL required for flight far exceeds these steady values. | S |
| Okamoto, Yasuda & Azuma 1996, *J Exp Biol* 199:281 (dragonfly wings and plates) | "10³–10⁴" in the abstract; citing papers disagree (700–2,400 vs 11,000–15,000) | Effects of camber, thickness, LE sharpness and roughness | Abstract scope only, **A**. Citing papers relay **CL_max ≈ 1.05** and say camber plus a sharper LE performed better, **S**. I could not retrieve the flat-plate L/D: `unknown`. | A / S |
| Kesel 2000, *J Exp Biol* 203:3125 (Aeshna forewing sections vs technical profiles) | 7,880 and 10,000 | Force balance | **CD_min < 0.06** for all sections, "closely resembling flat plates". Lift "comparable with technical profiles for low Re". Corrugation vortices change the effective profile (pressure data at Re 9,300). Per-profile CL_max and L/D: `unknown`. | A |
| Sunada, Yasuda, Yasuda & Kawachi 2002, *J Aircraft* 39:331 | 4,000 | 20 wing sections, AR 7.25 | Abstract scope only. A citing paper says the cambered wings had higher CD than the uncambered ones. Numbers: `unknown`. | A / S |
| Sunada, Sakaguchi & Kawachi 1997, *J Fluids Eng* 119:129 | 4,000 (per a 2026 citing paper) | Section optimum | A citing arXiv paper says the optimum is **~4% camber at α ≈ 6°**. The search summary *also* gave an abstract mentioning Re 1–200 simulations, which contradicts this. **Conflicting provenance; do not rely on it.** | S (conflicted) |
| Citation in *Sci Rep* 6:25706 (2016) | 10⁴ | Thin airfoil | "maximum lift coefficient of a thin airfoil is about **0.8**" | S |
| Laitone 1997, *Exp Fluids* 23:405 | ≥ 2×10⁴ (just above our range) | NACA 0012 vs flat and 5% cambered thin plates | A **5% circular-arc cambered plate gave the highest L/D and CL** at all turbulence levels. The plates were insensitive to Re and turbulence; **NACA 0012 was "very seriously affected" below Re 5×10⁴** (a citing review: −49% L/D). | A / S |

**Stall behaviour.** I could not retrieve primary text describing stall at Re 10³–10⁴, so the
stall characterisation is `unknown` at read-level A. The one retrieved qualitative signal is
Wakeling & Ellington's point that steady values fall short of what flight requires (S). Any
statement here about "soft, gradual stall of thin plates" would be **M**, so I have left it out as
a claim.

**Bottom line for §2.** At Re 10³–10⁴, steady **CL_max ≈ 0.8–1.1** and **CD_min ≈ 0.05–0.06**.
The peak section L/D was not retrieved for any plate.

---

## 3. Why thin plates win, and whether a fin is one

**Mechanism (M, textbook, consistent with the A-level Laitone and Mueller & DeLaurier 2003
abstracts).** Below Re ≈ 10⁵ the boundary layer stays laminar. On a thick, rounded-nose airfoil
it separates in the adverse pressure gradient aft of the suction peak. At higher Re the separated
shear layer transitions and reattaches as a *laminar separation bubble*. As Re falls, the bubble
lengthens and eventually fails to reattach, giving a large rise in pressure drag and hysteresis.
Thickness then costs drag and buys nothing. A thin plate with a sharp leading edge fixes
separation at the LE regardless of Re, so its behaviour depends little on Re. Laitone's abstract
(A) says exactly this: the plates were "fairly steady" with Re, NACA 0012 was not. Mueller &
DeLaurier (2003, *Annu Rev Fluid Mech* 35:89, **A**) identify boundary-layer behaviour and
laminar separation bubbles as the governing issue in this regime.

**Does a fin match the geometry that performs well?** Qualitatively, **yes**, and this is the
one genuine advantage worth stating:

| Good low-Re section property | Fin-on-rays | Status |
|---|---|---|
| Very thin (t/c of a few %) | Fin membrane is thin, rays are fine spars | Qualitative. Zebrafish fin thickness ratio: `unknown`. |
| Sharp leading edge | Leading ray, no rounded nose | Qualitative |
| Moderate camber, optimum ~4–6% (S, Sunada via citing paper; Laitone 5%) | Teleost rays can bend actively. Camber control via the paired hemitrich ray mechanism is **M** (I recall Alben, Madden & Lauder 2007 but did not retrieve it). | Plausible |
| Corrugation tolerated or helpful (Kesel, A) | Rays standing proud of the membrane form a shallow corrugation | Plausible |

**Caveats against the advantage.** (i) Fins are tuned for water loads at about 800× the air
density. Whether the membrane holds camber without fluttering at 2–5 m/s in air is `unknown`.
(ii) A fin membrane out of water dries, and its stiffness after seconds of air exposure is
`unknown`. (iii) Planform: a pectoral-fin-derived wing is low aspect ratio (assumed per-wing
span/chord ≈ 2), which raises induced drag in steady glide. (iv) The fish body is a large
non-lifting drag source compared with an insect thorax.

---

## 4. L/D ceiling

| Flyer / model | Re | Max L/D | Read |
|---|---|---|---|
| Locust wing (Jensen 1956), as cited by Wang 2004 *J Exp Biol* | not retrieved | **≈ 6–7** (≈ 6.5 at small α) | S |
| Dragonfly forewing, from a review | ~10³–10⁴ | **5.8 at α = 5°** (the same review gives 17.9 for hindwings; I cannot confirm whose polars these are) | S (attribution uncertain) |
| Flying fish *Cypselurus hiraii*, stuffed, wind tunnel (Park & Choi, IUTAM 2007 proceedings) | "matches real conditions" | **≈ 4.4** (model 3) | S |
| Same group, as quoted by Choi in an interview, vs hawk ≈ 3.8, petrel ≈ 4.0, wood duck ≈ 3.8 | — | **5.9** ("measured (estimated)") | S |
| Flying fish CFD (*Bioinspir. Biomim.*, doi 10.1088/1748-3190/ab23e6) | — | 4.7 at α = 6°; CL_max 1.03 at 35°. **Computed, not measured.** | S |
| Park & Choi 2010, *J Exp Biol* 213:3269 | — | "Comparable to hawk, petrel, wood duck". Ground effect raises L/D. | A |
| Dragonfly-inspired glider, flight test | — | ≈ 6 | S |

**Verifying "flying fish L/D ≈ 5–10".** That claim is **not supported**. The measured wind-tunnel
values I could reach are ≈ 4.4 and ≈ 5.9, both on stuffed specimens, both relayed. Nothing
retrieved supports values near 10. Ground effect raises them by an amount I did not retrieve. The
14% drag reduction in one press report is **S**.

**Ceiling for a zebrafish-scale fin wing.**
- *Wing alone, steady:* **≈ 6–7 is the best measured value** I found for any wing in this Re
  band (locust and dragonfly, both S). I treat that as the ceiling. No claim is made above it.
- *Whole animal:* lower, because of the fish body's drag and the low aspect ratio. My estimate is
  **≈ 3–5**. That is an **engineering estimate, not a measurement or a computation from data**.
- *What a zebrafish-scale wing actually gets:* **`unknown`**. No such wing has been built or
  measured.

---

## 5. Consequence: glide from 0.5 m (C)

**Assumptions** (all stated in `S2_calcs.py`):
- Mass 0.4 g, inside the retrieved adult range of ≈ 0.25–0.55 g and 2.8–3.4 cm standard length
  (lab studies relayed by search, **S**).
- Body length 4 cm, per the task.
- Total wing area 4.5 / 9 / 18 cm². For example, 9 cm² is two fins each 3 cm × 1.5 cm.
- Fixed CL = 0.6, a value below the measured steady CL_max of ≈ 0.8–1.07.
- ρ = 1.2 kg/m³, quasi-steady, still air, no ground effect.

**Equilibrium glide speed** `V = √(2mg/ρSC_L)`:

| S (cm²) | CL | V_eq (m/s) | Re at 15 mm | drop to reach V_eq from rest, v²/2g (m) |
|---|---|---|---|---|
| 4.5 | 0.6 | 4.92 | 4,922 | 1.23 |
| 9.0 | 0.6 | 3.48 | 3,480 | 0.62 |
| 9.0 | 0.9 | 2.84 | 2,841 | 0.41 |
| 18.0 | 0.6 | 2.46 | 2,461 | 0.31 |

**This is the key result.** The drop needed just to *reach* glide speed is comparable to, or
larger than, the 0.5 m launch height. A 0.5 m glide is therefore a transient, not a steady glide,
and `range = h·L/D` overstates it badly.

**Range** (integrated trajectory, CL = 0.6). Body lengths use 4 cm.

| S (cm²) | L/D | from rest | 2 m/s horizontal launch | already on glide path at V_eq (ideal h·L/D) |
|---|---|---|---|---|
| 4.5 | 2 | 0.03 m (1 BL) | 0.73 m (18 BL) | 1.0 m (25 BL) |
| 4.5 | 6 | 0.03 m (1 BL) | 0.76 m (19 BL) | 3.0 m (75 BL) |
| 9.0 | 4 | 0.07 m (2 BL) | 0.91 m (23 BL) | 2.0 m (50 BL) |
| 9.0 | 6 | 0.07 m (2 BL) | 0.94 m (23 BL) | 3.0 m (75 BL) |
| 18.0 | 4 | 0.14 m (4 BL) | 1.47 m (37 BL) | 2.0 m (50 BL) |
| 18.0 | 6 | 0.14 m (4 BL) | 2.52 m (63 BL) | 3.0 m (75 BL) |

**Wingless ballistic reference**, 2 m/s horizontal from 0.5 m: **0.64 m (16 BL)**.

**Reading the table.** With the small wings (4.5–9 cm²), the wing adds only 2–7 body lengths over
a plain jump, and L/D hardly matters. Only a large wing (18 cm², about 2× the fish's lateral
profile; an assumption) together with a fast launch approaches the ideal. The full table, with
all rows, is printed by the script.

**Controls, both directions (rule 8):**
- With aerodynamic forces set to ~0, the integrator returns the analytic ballistic range
  `v₀√(2h/g)` = 0.6386 m.
- Started on the equilibrium glide path, it returns exactly `h·L/D` = 1.000 / 2.000 / 3.000 m for
  L/D 2 / 4 / 6.
- Must-fail check: the wing must *extend* range beyond ballistic; an error in the lift sign would
  fail this.

All three are asserted in the script and pass.

---

## 6. Does flapping change the regime?

**Measured unsteady force coefficients:**

| Source | Re | Result | Read |
|---|---|---|---|
| Usherwood & Ellington 2002, *J Exp Biol* 205:1547 (revolving model hawkmoth wings) | ≈ 8,000–8,100 | High force coefficients from an attached LEV, "remarkably unaffected" by LE detail, twist and camber (A). **CL ≈ 1.75** (S, via a citing paper). | A / S |
| Ellington et al. 1996, *Nature* 384:626 (hawkmoth and flapper) | hawkmoth hover ≈ 7,300 (S) | An intense LEV on the downstroke, "sufficient to explain the high-lift forces" | A |
| Lentink & Dickinson 2009, *J Exp Biol* 212:2705 | 110 and 1,400 quoted | LEV stabilised by centripetal and Coriolis accelerations at **Rossby number ~O(1)**, i.e. a propeller-like sweep | A |
| Dickinson, Lehmann & Sane 1999, *Science* 284:1954 | Drosophila scale | Three mechanisms: delayed stall, rotational circulation, wake capture. **CL values: not retrieved, `unknown`.** | A |
| Sane & Dickinson 2001, *J Exp Biol* 204:2607 | Drosophila scale | Lift maximised by brief flips just before stroke reversal; quasi-steady models underestimate drag. **CL_max: not retrieved.** | A |
| Lehmann, Sane & Dickinson 2005, *J Exp Biol* 208:3075 (clap-and-fling) | **100–200** | Up to **+17% lift**, strongly kinematics-dependent, needs ≤ 10–12° wing separation. Effect at Re 10³–10⁴: `unknown`. | A |
| *Sci Rep* 6:25706 (2016) | ≥ 100 | Hovering mean **lift/drag ≈ 1–1.2** for larger insects | S |

**What flapping buys.** CL rises from the steady ≈ 0.8–1.07 to about **1.75 at the right Re**.
That is a real gain of about 1.6–2×, and it is available at *exactly* this Re. Usherwood &
Ellington's finding that the result is insensitive to LE detail, twist and camber (A) favours a
fin-derived wing: it does not need a precise profile. What flapping does not buy is efficiency.
Mean lift/drag in hovering is ≈ 1, against 4–7 in a steady glide.

**Could a fin-derived wing access it?** Aerodynamically, plausibly. A low-aspect-ratio plate
sweeping about its root is the LEV-stable configuration (Lentink & Dickinson, A). The fin
**must sweep with large amplitude about its base like a propeller**; a heave or undulation stroke
will not do. A clap-and-fling contribution should not be counted, because it is measured only at
Re 100–200.

**The separate constraint: actuation.** Hover frequency needed (C, `W = ½ρU²SC_L`,
`U = 2Φ f r₂`, `r₂ = 0.55R`; the 0.55 is **M**, typical of insect wings):

| R (one wing) | S (both) | Φ | CL | f needed |
|---|---|---|---|---|
| 3 cm | 9 cm² | 90° | 1.0 | 52 Hz |
| 3 cm | 9 cm² | 120° | 1.75 | 29 Hz |
| 4 cm | 12 cm² | 90° | 1.75 | 26 Hz |
| 4 cm | 12 cm² | 120° | 1.75 | 19 Hz |

**Comparisons:**
- Hawkmoth: ≈ 1.5 g at ≈ 28 Hz (S).
- Larval zebrafish pectoral fins: ≈ 28–30 Hz, or 18–28 Hz in slow swimming (S, larvae in water,
  small amplitude, no weight support).
- Adult zebrafish rely on body bending for propulsion and use their fins for manoeuvring (S).
- Larval *axial* muscle peaks in power at 100 Hz work loops (Mead et al., S). That is axial
  muscle, not fin muscle.

So **frequency alone is not disqualifying**. The unknowns are stroke **amplitude** (~90–120° of
fin sweep, against the small fin excursions seen in swimming), **power** (adult pectoral fin
muscle mass and mass-specific power output: `unknown`), and the **stroke-reversal control** that
the Dickinson-group results show matters. I did not quantify power because the inputs (profile
drag coefficient of a flapping fin, muscle mass) are not retrieved. A power number here would be
invented.

---

## 7. Answer

**Best available, physically.**
- Steady: CL_max ≈ 0.8–1.1, CD_min ≈ 0.05–0.06, and a wing-alone L/D ceiling of ≈ 6–7.
- Unsteady (revolving, LEV): CL ≈ 1.75 at lift/drag ≈ 1.

Thin, sharp-edged, slightly cambered, ray-stiffened membranes are the *right* geometry for this
Re, so a fin is not handicapped by its section.

**Honest path.**
- **Gliding is achievable**, and from 0.5 m it is worth **~20–60 body lengths with a 2 m/s
  launch**, of which ~16 come from the launch itself.
- The constraint is **launch speed and height, not L/D**: at 0.5 m the fish never reaches
  equilibrium glide.
- **Sustained flight requires flapping.** It is aerodynamically available at this Re, but it moves
  the problem to an **actuation spec of ~20–50 Hz at ~90–120° fin sweep** with unmeasured power.
  That is a different subproblem, and this one should not claim it is solvable.

**What would change this verdict.** (a) A measured polar of an actual teleost fin, or a
fin-like ray-membrane, in air at Re 2,000–5,000. This is the first experiment and it is cheap.
(b) Adult zebrafish pectoral-fin maximum amplitude, frequency and muscle mass.

---

## Sources (all reached only through search summaries; see read-level table)

- Wakeling & Ellington 1997, *J Exp Biol* 200:543–556. https://www.researchgate.net/publication/13905162
- Okamoto, Yasuda & Azuma 1996, *J Exp Biol* 199:281–294. https://journals.biologists.com/jeb/article/199/2/281/7462/
- Kesel 2000, *J Exp Biol* 203:3125–3135. https://www.researchgate.net/publication/12319395
- Sunada, Yasuda, Yasuda & Kawachi 2002, *J Aircraft* 39:331–338, doi 10.2514/2.2931. https://www.researchgate.net/publication/245429992
- Sunada, Sakaguchi & Kawachi 1997, *J Fluids Eng* 119:129–135 (relayed via https://arxiv.org/html/2605.19468v3; conflicted)
- Laitone 1997, *Exp Fluids* 23:405–409, doi 10.1007/s003480050128. https://www.osti.gov/etdeweb/biblio/559531
- Mueller & DeLaurier 2003, *Annu Rev Fluid Mech* 35:89–111. https://www.annualreviews.org/content/journals/10.1146/annurev.fluid.35.101101.161102
- Usherwood & Ellington 2002, *J Exp Biol* 205:1547–1564. https://pubmed.ncbi.nlm.nih.gov/12000800 ; CL 1.75 relayed via https://www.biorxiv.org/content/10.1101/099713v1.full ; Re ≈ 8,100 via https://files.core.ac.uk/download/pdf/81845397.pdf
- Ellington, van den Berg, Willmott & Thomas 1996, *Nature* 384:626–630. https://www.doi.org/10.1038/384626A0
- Lentink & Dickinson 2009, *J Exp Biol* 212:2705–2719. https://research.wur.nl/en/publications/rotational-accelerations-stabilize-leading-edge-vortices-on-revol/
- Dickinson, Lehmann & Sane 1999, *Science* 284:1954–1960. https://www.science.org/doi/abs/10.1126/science.284.5422.1954
- Sane & Dickinson 2001, *J Exp Biol* 204:2607–2626. http://repository.ias.ac.in/114131/
- Lehmann, Sane & Dickinson 2005, *J Exp Biol* 208:3075–3092. https://resolver.caltech.edu/CaltechAUTHORS:20110609-133142140
- Wang 2004, *J Exp Biol* (Jensen 1956 locust L/D relayed). https://dragonfly.tam.cornell.edu/publications/2004_JEB_Wang.pdf
- *Sci Rep* 6:25706 (2016), small-insect hovering. https://www.nature.com/articles/srep25706
- Park & Choi 2010, *J Exp Biol* 213:3269–3279, doi 10.1242/jeb.046052. Park & Choi IUTAM 2007: https://flair.monash.edu/intranet/proceedings/iutam2007/pages/pdf/S1_Park.pdf ; interview: http://blogs.britannica.com/2010/10/science-up-front-haecheon-choi-on-the-aerial-design-and-dynamics-of-the-flying-fish
- Flying-fish CFD, *Bioinspir. Biomim.* doi 10.1088/1748-3190/ab23e6. https://iopscience.iop.org/article/10.1088/1748-3190/ab23e6
- Davenport 1994, *Rev Fish Biol Fish* 4:184–214. https://link.springer.com/article/10.1007/BF00044128
- Fish 1990, *J Zool* 221:391–403. https://zslpublications.onlinelibrary.wiley.com/doi/10.1111/j.1469-7998.1990.tb04009.x
- Larval zebrafish fin and tail beat frequency. https://cob.silverchair.com/jeb/article/207/24/4175/2675/ and https://www.zfin.org/ZDB-PUB-110901-13
- Hawkmoth ≈ 28 Hz, ≈ 1.5 g. https://engineering.purdue.edu/~xdeng/BB09.pdf and https://pmc.ncbi.nlm.nih.gov/articles/PMC1693252
- Adult zebrafish mass and length. https://pmc.ncbi.nlm.nih.gov/articles/PMC1890438/table/tbl1 , https://pmc.ncbi.nlm.nih.gov/articles/PMC5764186/table/T2
