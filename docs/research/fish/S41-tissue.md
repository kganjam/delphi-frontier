# S41 (tissue) — Decay length of the kcnh2a/kcnk5b potential gradient

Project: `zebrafish-flight`. Question C5. Scale: tissue.
Date of work: 2026-11-04.

---

## 1. The question, restated with the numbers that make it hard

The published bioelectric story of fin size says that potassium channels — `kcnk5b`
(gain-of-function in *another longfin*, `alf`) and `kcnh2a` (ectopically expressed in
*longfin*, `lof^t2`) — set appendage size by altering membrane potential in fin
mesenchyme. The flying-fish paper (Daane et al. 2021) carries that mechanism into
evolution: modulation of "bioelectric cues" as the lever on paired-fin proportion.

For a potential gradient to *pattern* a fin ray, its decay length ℓ must be
commensurate with the ray. Two failure modes bracket the claim:

- ℓ ≫ L: the gradient is flat across the structure. Every cell reads the same value.
  It patterns nothing; it can only switch a whole-organ state on or off.
- ℓ ≪ L: only the proximal-most cells sit on the gradient. It patterns the base and
  leaves the rest of the ray unaddressed.

The target range this project must span is **0.1 mm to 120 mm** of fin-ray length —
from a *Danio* larval fin-fold / short distal ray to a flying-fish pectoral ray in the
design target. That is a span of **1200×**. A single ℓ cannot be within a factor of 3
of both ends: a factor-3 window is only 9× wide. So the question is not "does it
work" but *where in that span, if anywhere, does it work*, and what would have to
change physically to move it.

Refutation thresholds set for this subproblem: ℓ < 0.03 mm or ℓ > 400 mm refutes the
patterning claim on spatial grounds.

An honesty point that must be stated before any number: **the question presupposes a
standing kcnh2a/kcnk5b-driven potential gradient along the fin axis. I could not find
a measurement of one, and the primary authors of both channel papers do not claim
one.** See §2.3. What follows substitutes the one tissue-level voltage decay length
that *has* been measured in zebrafish fin, and says plainly where that substitution
is and is not legitimate.

---

## 2. What is measured

### 2.1 The one measured decay length in zebrafish fin tissue

**Liu J, Nerli E, Duclut C, Vishen SA, Berbee N, Kaufmann S, Ponce C, Arrenberg BA,
Jülicher F, Mateus R. "Injury-induced electrochemical coupling triggers regenerative
cell proliferation." bioRxiv 2025.04.03.647033, posted 2025-04-08.**
Read-level: **full-text** (PDF retrieved and text-extracted in this session).

The same work appears as "Injury-induced electrochemical coupling triggers organ
growth", *Science Advances*, February 2026 (TU Dresden FIS record; PubMed 41637501).
Read-level for the **published** version: **search-summary** only — `pubmed.ncbi.nlm.nih.gov`
and `www.mpi-cbg.de` both failed DNS resolution from this session (outside the allowed
network domains), so I could not read the peer-reviewed version. Numbers below are from
the preprint. Title and framing changed between versions ("regenerative cell
proliferation" → "organ growth"), so treat the published numbers as unverified here.

Measured values, 2 days-post-fertilisation (dpf) *D. rerio* caudal fin, FRET voltage
reporter Voltron2, exponential fit to ΔF/F₀ versus distance from a local injury:

| Quantity | Value | Note |
|---|---|---|
| Characteristic length ℓ, apical epithelium | **186 ± 39 µm** | exponential fit, their Fig. 1J |
| Characteristic length ℓ, basal epithelium | **197 ± 22 µm** | exponential fit, their Fig. S4C-D |
| Spatial extent of depolarisation at 100 ms | ~200 µm from wound | reported as "~200µm" |
| Ca²⁺ activation extent at 100 ms | 20 µm from wound | contrast: Ca²⁺ is *not* the long-range signal |
| Ca²⁺ wavefront arrest distance | ~120 µm (apical 118.4 ± 14.3; basal 118.7 ± 8.5) | separate, slower, diffusive signal |
| Effective ion diffusivity in fin | apical 1677 ± 170 µm²/s; basal 1877 ± 179 µm²/s | "comparable ranges to ion diffusivity in aqueous medium" |
| Aqueous reference diffusivities they cite | Na⁺ 1334, K⁺ 1957, Cl⁻ 2032 µm²/s | their ref. 40 |
| Leakage parameter Λ | **0.05 s⁻¹** | *estimated by the authors* from ℓ and D, not measured |
| Implied epithelial resistance ×area | ~200 Ω·cm² | their inference; "well within the range of values reported for epithelial resistance" |
| Proliferation response zone, 1–3 hpa | ~100 µm from wound | the biology the gradient is claimed to drive |
| Voltage-sensing-phosphatase (VSP) activation threshold | ~40 mV | cited from their refs 59, 62, 63 |

Their own space-constant derivation, quoted:

> "the electric potential in the interstitial fluid relaxes to a quasi-steady state
> over 100 ms. After relaxation, it assumes an exponential profile that decays over a
> characteristic length 𝑙 = √(𝐷/𝛬), set by the diffusion constant of ions 𝐷, and the
> parameter 𝛬, describing leakage through the epithelium."

This is the only published, fitted voltage decay length in a zebrafish fin I located.
It is **measured** (the fit), on a **model-identified** parameter (Λ is back-solved
from ℓ, not independently measured — so the "derivation" runs ℓ → Λ, not Λ → ℓ; see
§3.1, this matters).

### 2.2 Direct link of that gradient to the channel genes in question

Also from Liu et al. 2025 (full-text): `lof^t2` homozygotes (the `kcnh2a` regulatory
allele) and FK506 were used as the two K⁺-efflux-enhancing perturbations. Measured
effects:

- Ca²⁺ flash amplitude increased in `lof^-/-` and under FK506.
- The Ca²⁺ activation wavefront was "mostly unaffected" in these conditions.
- The 1 hpa proliferation peak was impaired in `lof^-/-` and under FK506, with fin
  length defects following.
- High external KCl extended the Ca²⁺ wavefront "more than 300µm, 3-fold longer than
  wildtype".

Their stated working hypothesis, quoted: `lof^-/-` and FK506 "increase K⁺ leakage,
lowering the resting membrane potential of the tissue, hyperpolarizing V_mem", so that
the injury depolarisation no longer crosses the ~40 mV VSP threshold.

Note the **direction conflict the authors themselves flag**, quoted:

> "longfin^t2 mutations and FK506-treatments have been found to promote fin outgrowth
> in adult zebrafish and other fishes … This apparent discrepancy with our larval fin
> regeneration findings could be due to differences in the cell types that respond to
> injury: our larval system regenerates by essentially promoting epithelial
> proliferation through VSP activation, instead of a classic dedifferentiated,
> proliferative mesenchymal blastema structure."

So `kcnh2a` activity *shortens* larval fins in this assay and *lengthens* adult fins
in the fin-size literature. I preserve this disagreement; it is not reconciled.

They also state the adult case is unmeasured: "Deciphering the electrochemical
dynamics of V_mem and ion fluxes in the adult mesenchymal blastema … is an exciting
frontier to be [explored]".

### 2.3 What the channel papers actually measured — and did not

**Perathoner S, Daane JM, Henrion U, Seebohm G, Higdon CW, Johnson SL, Nüsslein-Volhard
C, Harris MP. "Bioelectric Signaling Regulates Size in Zebrafish Fins." *PLoS Genetics*
2014.** Read-level: **full-text** (first ~100k characters of PMC3894163; final ~18k not
read).

- Measured, in *Xenopus* oocytes, not fin: mutant Kcnk5b shifts membrane potential "towards
  −90 to −100 mV", with "an almost two-fold increase in K⁺ conductance". Holding −80 mV,
  pulses −100 to +60 mV.
- Measured allometric coefficients: wild type k = 1.29; `alf` heterozygotes "near 2".
- In fin tissue: juveniles (16–18 mm standard length) stained with the voltage dye
  DiSBAC₂(3) and confocal-imaged. **No calibrated mV values reported.** No fitted
  spatial profile. No decay length.
- The only gradient they invoke is embryonic, quoted: "a rostro-caudal and medio-lateral
  gradient of voltage within the developing embryo" — not a fin-axis gradient.
- Their positional-information language is explicitly a model, quoted: K⁺ channel
  modulation "shifts positional information, thereby setting a different register of
  size during development."
- Gap junctions: raised by analogy only. "Kcnk5b and Cx43 may act in parallel pathways
  to modulate final fin size", with no epistatic interaction found. "No length scale for
  voltage fields or coupling is discussed."
- **No absolute ray or fin lengths in mm.** Fin length is normalised to standard length.

**Stewart S, Le Bleu HK, Yette GA, Henner AL, Robbins AE, Braunstein JA, Stankunas K.
"longfin causes cis-ectopic expression of the kcnh2a ether-a-go-go K⁺ channel to
autonomously prolong fin outgrowth." *Development* 148(11), 2021** (PMC8217709;
bioRxiv 790329v3). Read-level: **full-text** (first ~100k characters of PMC8217709;
final ~20k not read). ZFIN record `ZDB-PUB-210602-7` returned HTTP 503; bioRxiv
`790329v3.full` returned HTTP 429.

This paper is the strongest evidence *against* the premise of the question:

- Quoted: `lof^t2` "does not seem to change positional information established at the
  outset of fin regeneration."
- Quoted: ion signaling alters organ size "rather than establishing growth-defining
  positional information", by changing growth *periods*.
- Quoted: Kcnh2a and calcineurin inhibition disrupt growth deceleration "tuned to
  interpret, rather than set, positional information."
- Mechanism of extra length: prolonged outgrowth *duration*, not increased maximal
  growth rate. "Wild-type fins largely ceased regenerative outgrowth by 21 dpa" while
  "`lof^t2` fins continued to extend through the 30 dpa period."
- Expression is broad along the axis, not a sharp proximal source: "kcnh2a was
  expressed in Msx+ or tph1b:mCherry+ cells in proximal regenerating tissue", also
  "at lower levels in growth-promoting distal blastema cells", and "highest near the
  amputation site but still detectable in medial and distal blastema."
- **No membrane potential measured.** Their own stated next step: "characterizing
  membrane potentials and putative depolarizing signals".
- **No absolute ray lengths in mm**; ray 3 is reported as "normalized length".
- No discussion of electrical coupling or a length scale.

**Daane JM et al. "Modulation of bioelectric cues in the evolution of flying fishes."
*Current Biology* 31(22):5052–5061, 2021.** Read-level: **search-summary** (X-MOL and
AMiner abstract mirrors, ZFIN figure records; `www.x-mol.com`/full text not read). Genes
implicated: `lat4a` and `kcnh2a`. No gradient measurement is claimed in the abstract.

**Hoptak-Solga AD et al., FEBS Lett. 2007 and Dev. Biol. 2008 (Cx43 / *short fin*).**
Read-level: **search-summary**. Dye coupling and ionic coupling differ by allele;
`sof^b123` fins are "half the length of wild-type"; cx43 knockdown reduces proliferation
and segment length. No decay length; no voltage profile.

### 2.4 Fin-ray lengths to compare against

- 0.1 mm and 120 mm endpoints: **taken as given by the project framing** (this
  subproblem's statement). I did not independently source either endpoint in this
  session and do not assert them as measured here.
- Adult *D. rerio* caudal fin ray length in mm: **unknown**. What I tried: targeted
  searches for absolute mm ray lengths in Stewart 2021, Perathoner 2014, Iovine &
  Johnson 2000, Géraudie 1995; all three channel/length papers report **normalised**
  lengths or length-vs-standard-length regressions, not absolute per-ray mm. A search
  surfaced a Lanni et al. 2019 wild-type fit "caudal fin length = 0.9209 × STL −
  0.2495, R² = 0.97" (read-level: **search-summary**), but the search result itself
  states the units are not given in the caption, and a slope of 0.92 implies a caudal
  fin nearly as long as the body, which does not match *D. rerio*. I therefore
  **reject that fit as unusable here** rather than convert it.
- Larval 2 dpf fin, where ℓ was measured: Liu et al. report fin lengths only in plots
  (their Fig. 3B, 2–5 dpf), with "zero, notochord tip" as the origin; their scale bars
  are 50–200 µm and the depolarisation spans ~200 µm of it. Read-level: full-text, but
  **the absolute 2 dpf fin length in µm is not in the text I extracted** — I infer only
  that it is of the same order as ℓ, which is also the authors' own point ("The similar
  tissue length scales between proliferation and graded depolarization").

For the arithmetic below I therefore use the project-given endpoints 0.1 mm and 120 mm,
and a **clearly-labelled placeholder of 5 mm** for an adult *Danio* caudal ray. The
5 mm figure is **my order-of-magnitude placeholder, not a measurement** — a ~40 mm fish
with a caudal fin of a few mm. Every conclusion below that depends on it is marked, and
none of the refutation-threshold conclusions do.

---

## 3. What I computed

**All of §3 is computation, not observation.**

### 3.1 Checking the authors' space constant is self-consistent

Their relation: ℓ = √(D/Λ). Taking D = 1700 µm²/s (midpoint of their measured 1677 and
1877 µm²/s) and their Λ = 0.05 s⁻¹:

    ℓ = √(1700 / 0.05) = √34,000 = 184 µm

This reproduces their fitted 186–197 µm, as it must — **Λ was back-solved from ℓ**, so
this is a consistency check of my reading, not an independent derivation of ℓ. The
*independent* content is that the implied epithelial resistance, ~200 Ω·cm², lands in
the range reported for real epithelia; that is the authors' claim, and I did not verify
an epithelial-resistance range from source in this session.

The physically important form of the relation, for scaling:

    ℓ = √(D/Λ)  and  Λ ∝ 1/(R_epithelium)   ⟹   ℓ ∝ √(D · R)

So **ℓ scales as the square root of the product of ion diffusivity and transepithelial
resistance.** To extend ℓ by a factor *n*, D·R must rise by *n²*.

### 3.2 Is ℓ within a factor of 3 of the claimed range?

Take ℓ = 0.19 mm (mean of 186 and 197 µm). A factor-3 window is 0.064 mm to 0.57 mm.

| Target ray length L | L/ℓ | Within factor 3? |
|---|---|---|
| 0.1 mm (low end of project range) | 0.53 (i.e. ℓ/L = 1.9) | **Yes** |
| 0.57 mm | 3.0 | borderline — the upper edge |
| ~5 mm (my placeholder adult *Danio* ray) | **26×** | No — off by ~9× |
| 120 mm (project design target) | **632×** | No — off by ~210× |

At L = 120 mm, ℓ/L = 0.0016: the gradient covers 0.16% of the ray. The remaining 99.8%
of the ray sits at a uniform, essentially zero, deviation. That is the "patterns only
the base" failure mode, in its extreme form.

### 3.3 What D·R would have to be

Using ℓ ∝ √(D·R), with the measured baseline D = 1700 µm²/s, Λ = 0.05 s⁻¹:

Required Λ = D/ℓ²:

| Target ℓ | Required Λ (s⁻¹), D held at 1700 µm²/s | Fold reduction in leakage vs. 0.05 s⁻¹ | Required R if all of it comes from R (Ω·cm²) |
|---|---|---|---|
| 0.19 mm (measured) | 0.05 | 1 | ~200 |
| 1 mm | 1.7 × 10⁻³ | 29 | ~5.8 × 10³ |
| 5 mm | 6.8 × 10⁻⁵ | 735 | ~1.5 × 10⁵ |
| 120 mm | 1.2 × 10⁻⁷ | 4.2 × 10⁵ | ~8.4 × 10⁷ |

Arithmetic shown for the 5 mm row: Λ = 1700 µm²/s ÷ (5000 µm)² = 1700 / 2.5×10⁷ =
6.8×10⁻⁵ s⁻¹; 0.05 / 6.8×10⁻⁵ = 735; 200 Ω·cm² × 735 = 1.47×10⁵ Ω·cm².
And for 120 mm: Λ = 1700 / (1.2×10⁵)² = 1700 / 1.44×10¹⁰ = 1.18×10⁻⁷ s⁻¹;
0.05 / 1.18×10⁻⁷ = 4.2×10⁵; 200 × 4.2×10⁵ = 8.4×10⁷ Ω·cm².

**Assumptions, stated:** (i) the cable form ℓ = √(D/Λ) still holds at these scales,
which assumes the same two-compartment, leaky-epithelium geometry — false for an adult
ray with a vascularised, mesenchyme-filled lumen; (ii) D cannot be raised much, because
the measured value already sits at free-aqueous ion diffusivity (1677–1877 µm²/s versus
Na⁺ 1334, K⁺ 1957, Cl⁻ 2032 µm²/s), so there is **less than ~1.2× of headroom in D** and
essentially the entire required *n²* must come from R; (iii) ~200 Ω·cm² is the correct
baseline, which is itself the authors' model inference.

Point (ii) is the load-bearing one: **D is pinned at the physical ceiling of aqueous ion
diffusion.** The decay length of an electrodiffusive tissue gradient cannot be bought
with faster ions. It can only be bought with a tighter epithelium, and quadratically
expensively.

### 3.4 A timescale cross-check (independent of ray length)

1/Λ is the leak-equilibration time of the interstitial potential. This is **my
inference**, not the authors' statement; they report a measured relaxation to
quasi-steady state at 100 ms, which is a faster, membrane-capacitive relaxation and a
different quantity.

- At the measured Λ = 0.05 s⁻¹: 1/Λ = 20 s.
- At the Λ required for ℓ = 5 mm: 1/Λ = 1.5 × 10⁴ s ≈ 4.1 hours.
- At the Λ required for ℓ = 120 mm: 1/Λ = 8.5 × 10⁶ s ≈ **98 days**.

A gradient that takes ~3 months to establish cannot pattern an appendage that
regenerates in weeks. Marked as **derived**, and it depends on assumption (i) above,
which is the weakest link.

### 3.5 Is the measured gradient even the right *kind* of object?

Computation is not needed for this, but it governs how much the above is worth. The
Liu et al. gradient is:

- **injury-triggered**, not developmental: it exists because amputation short-circuits
  the transepithelial potential;
- **transient on the relevant scale**: established in 100 ms, voltage maintained over
  ~3 s;
- **epithelial**, in a 2 dpf fin consisting of two adjacent epithelial layers;

whereas the thing it is being asked to pattern is a ray length set over **weeks** of
adult outgrowth in **intra-ray mesenchyme** (the tissue Stewart et al. identified by
blastula transplantation as the autonomous site of `kcnh2a` action). These are different
tissues, different timescales, and different triggers. Using 0.19 mm as "the decay
length of the kcnh2a-driven gradient" is a substitution across all three axes.

---

## 4. The answer

**Evidence level: derived.** (The 0.19 mm number itself is **measured**; identifying it
as "the kcnh2a/kcnk5b-driven gradient's decay length" is my inference, because no such
gradient has been measured.)

The only fitted voltage decay length in zebrafish fin tissue is **ℓ ≈ 0.19 mm**
(apical 186 ± 39 µm, basal 197 ± 22 µm; Liu et al. 2025 preprint, full-text), with the
space constant ℓ = √(D/Λ) from cable theory, D ≈ 1700 µm²/s measured and Λ = 0.05 s⁻¹
back-solved.

Against the refutation thresholds set for this subproblem: 0.19 mm is **neither below
0.03 mm nor above 400 mm**, so the patterning claim is **not refuted on spatial grounds
at the low end of the range.** At L ≈ 0.1 mm the gradient and the structure are
commensurate (ℓ/L = 1.9, within a factor of 3) — and that is exactly the regime the
measurement was made in, where the authors note "similar tissue length scales between
proliferation and graded depolarization."

But the claim fails the factor-of-3 test across most of the range it is asked to cover:
**26× off** for an adult *Danio* caudal ray (placeholder 5 mm, not measured) and
**632× off** for the 120 mm flying-fish-scale ray the project targets, where the
gradient spans 0.16% of the structure. Extending ℓ to 120 mm requires D·R to rise
**4.2 × 10⁵-fold**, and because the measured ion diffusivity already sits at the
free-aqueous ceiling, nearly all of that must come from transepithelial resistance —
an implied ~8 × 10⁷ Ω·cm².

The sharper finding, and the honest one: **the premise is largely not the published
claim.** Stewart et al. 2021 state in full text that `lof^t2` "does not seem to change
positional information", that Kcnh2a is "tuned to interpret, rather than set, positional
information", and that the extra length comes from a prolonged outgrowth *period*, not a
spatial gradient. Perathoner et al. 2014 present "shifts positional information" as a
model, measure voltage only in *Xenopus* oocytes, image fin tissue with an uncalibrated
voltage dye, and report no spatial profile and no length scale. So for a duration-tuning
mechanism, a short ℓ is not a defect: a 0.19 mm gradient is adequate to switch a
whole-ray timer on or off, and never needed to span the ray. The spatial-patterning
version of the story — the one this question tests — appears to be a secondary framing
rather than the primary authors' claim, and on the numbers above it does not survive
beyond ~0.5 mm.

Direction of effect is also unresolved in the literature and I do not average it:
`kcnh2a` activity (`lof^-/-`, FK506) **impairs** larval fin regeneration and shortens
fins in Liu et al., and **promotes** outgrowth in adult zebrafish in Perathoner 2014 /
Stewart 2021. The authors of the former flag this discrepancy themselves and attribute
it to epithelial-vs-mesenchymal responder cell types.

---

## 5. What this does NOT establish

Read this as carefully as §4.

1. **It does not establish that a kcnh2a- or kcnk5b-driven potential gradient exists at
   all.** No paper I read reports one. The 0.19 mm figure is from a wound-induced
   transepithelial short-circuit in wild-type larvae. `kcnh2a` (`lof^t2`) enters that
   work only as a perturbation of the same ion-flux system, not as the generator of a
   measured gradient.
2. **It does not transfer tissue.** ℓ was fitted in a two-layer epithelial larval fin
   fold. `kcnh2a` acts autonomously in adult intra-ray **mesenchyme** (Stewart et al.,
   blastula transplantation). An adult ray has bone, vasculature and a mesenchymal
   lumen; the leaky-tight-junction, two-compartment geometry that produces
   ℓ = √(D/Λ) does not describe it. The cable form may not hold, and the scaling table
   in §3.3 inherits that failure.
3. **It does not transfer timescale.** 100 ms to 3 s of injury depolarisation versus
   weeks of adult ray outgrowth. A standing developmental gradient, if one exists, could
   have an entirely different ℓ set by entirely different parameters (gap-junctional
   coupling rather than paracellular leak, for instance).
4. **It does not test the gap-junction route.** If the relevant coupling in adult
   mesenchyme is Cx43 gap-junctional rather than interstitial-fluid electrodiffusive,
   the space constant is set by junctional versus membrane resistance and is not the
   √(D/Λ) of §3.1 at all. Perathoner et al. explicitly place Cx43 in a *parallel*
   pathway with no epistasis, and discuss no length scale. I did no computation for this
   route and it is not refuted by anything here.
5. **The adult ray comparison rests on a placeholder.** The 5 mm figure and the 26×
   mismatch are my order-of-magnitude stand-in. Absolute adult *Danio* ray lengths in mm
   are `unknown` to this analysis (§2.4). None of the §4 refutation-threshold
   conclusions depend on it; the 26× row does.
6. **The 0.1 mm and 120 mm endpoints are inherited, not verified here.** I took them
   from the project framing.
7. **Λ is not independently measured.** It is back-solved from ℓ by the authors. The
   ~200 Ω·cm² epithelial resistance is therefore also an inference, and I did not verify
   a sourced range for real epithelial resistances in this session, so the claim "~200
   Ω·cm² is normal, 10⁵ Ω·cm² is not" is **not established here** — I show only the
   fold-change required, which is the part that does not depend on knowing the range.
8. **It does not refute bioelectric control of fin size.** It constrains one specific
   mechanism — a spatial potential gradient read as positional information along a ray.
   Duration-tuning, threshold switching, proliferation-rate control and calcineurin
   coupling are all untouched by this result, and the duration-tuning version is what
   the primary sources actually argue.
9. **It does not read the peer-reviewed version** of the only paper carrying the key
   number. The *Science Advances* 2026 version is search-summary only; PubMed and
   MPI-CBG hosts failed DNS resolution from this session and would need to be allowed in
   the session's network settings. The title changed between preprint and publication,
   so numbers may have changed too.
10. **Parts of two full texts were unread**: the final ~18k characters of PMC3894163 and
    ~20k of PMC8217709, plus all figure-panel data in all papers. A fitted spatial
    profile could in principle sit in a figure I could not read; I found none in text.

---

## 6. What would change the answer

**The decisive measurement.** A calibrated voltage profile along the proximodistal axis
of an **adult** zebrafish fin ray during outgrowth, in intra-ray mesenchyme, in wild
type versus `lof^t2` and `alf` — with an exponential fit and a reported ℓ. Stewart et al.
name this as their own next step ("characterizing membrane potentials and putative
depolarizing signals"). Genetically-encoded voltage reporters (Voltron2, as Liu et al.
used; or ASAP/Archon) driven in the `tph1b`+ / Msx+ intra-ray mesenchymal lineage would
do it. If that ℓ comes back at a few mm, the spatial-patterning claim is live for
*Danio*; if it comes back at ~0.2 mm, §4 stands and the mechanism is a timer, not a map.

**The parameter that moves ℓ.** From ℓ ∝ √(D·R): only transepithelial/junctional
resistance. D is already at the aqueous ceiling. An independent measurement of adult
intra-ray transepithelial resistance would convert the §3.3 table from fold-changes into
a decisive feasibility test — if adult ray R is, say, 100× larger than the larval
~200 Ω·cm², ℓ rises only 10× to ~2 mm, still ~60× short of 120 mm.

**What would refute §4 outright.** A fitted adult-ray ℓ below 0.03 mm or above 400 mm,
per this subproblem's thresholds. Also: any demonstration that the relevant coupling is
gap-junctional, which would retire the √(D/Λ) scaling and require the whole calculation
to be redone with junctional resistance, where the length scale is set by
√(R_membrane/R_junctional) × cell length and can be far longer than the electrodiffusive
one.

**The design implication, if §4 holds.** For `zebrafish-flight`, a bioelectric lever on
paired-fin size should be specified as a **duration/threshold** control — set how long
outgrowth runs — not as a gradient that maps position along a ray. Those are different
engineering targets: the first needs a switch and a clock, the second needs a 1200×
increase in a length scale that is quadratically expensive in a parameter that is
already near its physical ceiling. The second is, on these numbers, not available.

---

```swarm-result
{"subproblem": "S41", "evidence": "derived",
  "answer": "The only fitted voltage decay length in zebrafish fin tissue is ~0.19 mm (apical 186+/-39 um, basal 197+/-22 um; injury-induced transepithelial gradient in 2 dpf larval fin, Liu et al. 2025 preprint, cable theory l=sqrt(D/Lambda)); it is within a factor of 3 of only the 0.1 mm end of the claimed 0.1-120 mm ray range, is ~26x short of an adult Danio ray and ~632x short of the 120 mm design target, and no kcnh2a/kcnk5b-driven standing gradient has ever been measured - the primary authors claim outgrowth-duration tuning and explicitly deny changing positional information.",
  "key_number": "0.19 mm (190 um) decay length; 632x short of the 120 mm target, requiring a 4.2e5-fold rise in D*R that diffusivity cannot supply",
  "blocked_on": "No calibrated voltage profile along an adult fin ray in intra-ray mesenchyme exists; absolute adult Danio ray lengths in mm unavailable (all three channel papers report normalized lengths); peer-reviewed Science Advances 2026 version of the key paper unreadable (pubmed.ncbi.nlm.nih.gov and www.mpi-cbg.de failed DNS resolution from this session)"}
```
