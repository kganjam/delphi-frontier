# S45-D — deepening S45 by attacking its weakest input

Project: `zebrafish-flight`. Date: 2026-11-04. Author: this agent.
Parent: `docs/research/fish/S45-organism.md` on branch `claude/zebrafish-flight-s45-organism-epe63k`
(commit `d188d0e1`), read at full text by me.
Reproduce every number here with `python3 -I docs/research/fish/S45_deepen_calc.py` (≈90 s).

**Headline: S45 STANDS.** Its deciding computation is most sensitive to one input it never sourced:
the **fraction f of the ray, measured from the base, that carries the stiff 565×10⁻⁶ N·m² rigidity**.
S45 used f = 0.40 with no citation. The Flammang et al. 2013 abstract, the same paper that supplies
the 565×10⁻⁶ N·m² value, states that "the distal 60% of the fin ray is segmented". That gives
**f = 0.40** for the unsegmented proximal part. So the value S45 assumed is now sourced, at
abstract level. The margin is narrow (§3.3), and the real exposure has moved to a question that is
not a number (§4.2).

---

## 1. What S45 concluded and what its conclusion rests on

S45 asked whether any high-scale claim in the project has an entailed low-scale requirement that a
published measurement already contradicts. It answered **no**. Its leading candidate was:

- **M3:** Flammang et al. 2013 give fin-ray EI = 565×10⁻⁶ N·m². The S6/S6-D passive-ray branch
  survives only on this value.
- **M1:** Alben, Madden & Lauder 2007 measure EI ≈ 10⁻⁶ to 10⁻⁵ N·m² on the same structure (bluegill
  pectoral ray).

Read as a single uniform EI, M3 is 56 to 565 times above M1. S45 killed the candidate with a
calculation: a **stepped** cantilever with M3 on a proximal fraction f and a free distal EI. At
f = 0.40, a distal EI of **2.44×10⁻⁶ N·m²** (inside M1) reproduces Alben's measured cantilever slope
of 1.98 N m⁻¹. S45 names that 2.44×10⁻⁶ N·m² as "the single number that decides it".

That number is an output, not an input. Its inputs are:

| input | value S45 used | S45's source for it |
|---|---|---|
| k, cantilever slope | 1.98 N m⁻¹ | Alben 2007 Fig. 7a (full-text, read by S45's agent) |
| deflection convention for k | force vs **tip** deflection | Alben 2007 §5.2 wording (full-text, read by S45's agent) |
| L, ray length | 40.3 ± 0.8 mm | Alben 2007 §2 |
| load point | a = 2L/3 | Alben 2007 Fig. 7a caption |
| M3, proximal EI | 565×10⁻⁶ N·m² | Flammang 2013 abstract |
| M1 bracket edges | 1×10⁻⁶ and 1×10⁻⁵ N·m² | Alben 2007 §3.3 ("≈ 10⁻⁶–10⁻⁵") |
| **f, stiff proximal fraction** | **0.40 (also 0.50, 0.60 tabulated)** | **none given** |

## 2. Step 1: sensitivity, recomputed rather than asserted

All of §2 is **computation by me** (Euler–Bernoulli, two-section cantilever, trapezoidal
integration, 2×10⁵ nodes). None of it is an observation. Baseline reproduces S45: f = 0.40 gives
2.442×10⁻⁶ N·m², f = 0.50 gives 8.32×10⁻⁷ N·m², and f = 0.60 gives 1.13×10⁻⁷ N·m².

The decision variable is binary: is the reconciling distal EI inside M1's 10⁻⁶ to 10⁻⁵ N·m² bracket?

| perturbation at f = 0.40 | reconciling distal EI (N·m²) | ratio to baseline | inside M1? |
|---|---|---|---|
| baseline | 2.44×10⁻⁶ | 1.00 | yes |
| **M3 ×2** (1.13×10⁻³) | 2.40×10⁻⁶ | 0.98 | yes |
| **M3 ÷2** (2.83×10⁻⁴) | 2.54×10⁻⁶ | 1.04 | yes |
| M3 ÷10 (5.65×10⁻⁵) | 3.65×10⁻⁶ | 1.49 | yes |
| k ×2 (3.96 N m⁻¹) | 5.07×10⁻⁶ | 2.08 | yes |
| k ÷2 (0.99 N m⁻¹) | 1.20×10⁻⁶ | 0.49 | yes, barely |
| L ± 2% (the reported s.e.) | 2.30 to 2.60×10⁻⁶ | 0.94 to 1.06 | yes |
| **load-point instead of tip convention** | **8.37×10⁻⁷** | 0.34 | **no — flips** |

| f (proximal fraction at M3) | reconciling distal EI (N·m²) | inside M1? |
|---|---|---|
| 0.20 | 9.31×10⁻⁶ | yes |
| 0.30 | 5.19×10⁻⁶ | yes |
| **0.40** | **2.44×10⁻⁶** | **yes** |
| 0.45 | 1.51×10⁻⁶ | yes |
| 0.48 | 1.07×10⁻⁶ | yes |
| **0.50** | 8.32×10⁻⁷ | **no — flips** |
| **0.80 (f × 2)** | no solution: the step lies beyond the load point, so k ≈ 49.9 N m⁻¹ whatever the distal EI | **no — flips** |

Computed admissible window: **0.186 < f < 0.486**.

**Reading of the sensitivity (my inference from the computation above):**

- The candidate's apparent subject, M3, is **not** the sensitive input. Doubling or halving it
  moves the reconciling distal EI by 2–4%, because a 565×10⁻⁶ N·m² section is close to rigid
  compared with the distal section, whatever its exact value. S45's conclusion does not depend on
  M3 being right. It depends on where M3 applies.
- **f is the most sensitive input.** A factor-of-two change in f (0.40 → 0.80) flips the
  conclusion, and so does a factor of 1.25 (0.40 → 0.50). No other numeric input flips under a
  factor of two.
- The deflection convention also flips the conclusion, but it is a binary reading of a text, not a
  number. S45's agent read Alben §5.2 at full text and quoted "force … as a function of tip
  deflection", so I treat it as settled at full-text level. It is listed in `depends_on`.

## 3. Steps 2–3: how well f is established, and the improvement

### 3.1 Before this pass

f = 0.40 in S45 is an **assumption with no stated source**. S45 tabulated 0.40, 0.50 and 0.60
side by side and reported 0.40 as the decisive case without saying why 0.40 was the physical one.
Evidence level: assumption. I did not search the other ~860 project documents to see whether
another agent sourced it (scope of that negative: not searched).

### 3.2 The primary source

**Flammang BE, Alben S, Madden PGA, Lauder GV (2013). "Functional morphology of the fin rays of
teleost fishes." *J Morphol* 274(9):1044–1059. doi:10.1002/jmor.20161, PMID 23720195.**
Read-level: **abstract**. I retrieved the complete PubMed abstract myself via NCBI E-utilities
`efetch`, 2026-11-04. Quotations below are the authors' words:

- "Analysis of pectoral fin rays of bluegill sunfish showed that the more proximal portion of the
  fin ray is unsegmented while **the distal 60% of the fin ray is segmented**."
- "Under normal swimming conditions, curvatures did not exceed 0.029 mm⁻¹ in the proximal,
  unsegmented portion of the fin ray and 0.065 mm⁻¹ in the distal, segmented portion."
- "Flexural stiffness of the fin ray was **calculated** to be 565 × 10⁻⁶ Nm²."
- "Segmentation is a key design feature … and may serve as a means of making a flexible fin ray out
  of a rigid material (bone)."

Body text: **could-not-access**. What I tried:

| route | result |
|---|---|
| Wiley `onlinelibrary.wiley.com/doi/pdf/10.1002/jmor.20161` | HTTP 403 |
| Europe PMC REST | record found; `isOpenAccess: N`, `hasPDF: N`, no PMCID |
| PubMed → PMC elink | no PMC full text for this PMID; only citing articles are linked |
| Unpaywall, Semantic Scholar, OpenAlex APIs | proxy `403` on CONNECT |
| Lauder-lab PDF at `sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf` (found by web search) | host outside this session's network allowlist |
| Deep Blue (U. Michigan) record | proxy `403` |

A web-search summary (read-level: **search-summary**) says that the Harvard PDF's extracted text
"is garbled at this number". I give that no weight beyond noting that it exists.

### 3.3 The improved input

**f = 0.40, the unsegmented proximal fraction of the bluegill pectoral ray** (Flammang et al. 2013,
abstract). It is stated by the same authors, for the same species and fin, as M3 and as the Alben
2007 cantilever measurement (Alben is a co-author of both papers). It comes from their anatomical
analysis, so it is a **measured anatomical proportion**. The abstract does not give its n, spread
or ray length, so those are **unknown**.

Its fit to the computation is my inference, not the authors' claim. The segmentation boundary is a
physical place where rigidity can step, so it is the natural location for a stepped-EI model. The
authors' own curvature data point the same way: proximal curvature is at most 0.029 mm⁻¹ and distal
at most 0.065 mm⁻¹. That is consistent with a stiffer proximal section, though curvature also
depends on load, so it does not measure the EI ratio.

**Margin at the improved value (computation):** the reconciling distal EI is 2.44 times Alben's
lower bracket edge. f could grow by **+0.086, about 3.5 mm on a 40.3 mm ray**, before the
reconciliation fails. The abstract's "60%" carries no stated uncertainty. If it is rounded from
anywhere in 51–60% segmented (f = 0.40–0.49), the conclusion holds across that whole range except
its very top. That robustness is a computation on an unknown spread, not a measured robustness.

**What would settle f fully, and the cost:** micro-CT or cleared-and-stained imaging of n ≈ 10
adult bluegill pectoral rays, measuring the position of the first segment joint as a fraction of
ray length. Bluegill are commercially available and the method is routine, so the material and
scan-time cost is on the order of a few days of work. Alternatively, Flammang 2013's body text
probably reports it already (unknown, not read). Reading that text needs the Harvard host to be
allowed in this session's network settings, or an interlibrary copy.

## 4. Step 4: recompute and verdict

### 4.1 Recomputation

With f = 0.40 now sourced rather than assumed, the reconciling distal EI is **2.44×10⁻⁶ N·m²**
(computation), unchanged. It lies inside Alben's measured 10⁻⁶ to 10⁻⁵ N·m² bracket. So Alben 2007
still does **not** contradict Flammang 2013 when M3 is read as the EI of the unsegmented proximal
40%. S45's "no refutation found" **STANDS**.

It does not **strengthen**, because:

1. The number did not move. Only its provenance improved, from an assumption to an abstract-level
   anatomical proportion with unknown spread.
2. The margin is a factor of 2.44 against a bracket edge that is itself an order-of-magnitude
   statement. Alben's "≈ 10⁻⁶–10⁻⁵" is the product of E ≈ 10⁸–10⁹ N m⁻² and I ≈ 10⁻⁶ cm⁴, both
   given to one significant figure. A bracket that soft cannot exclude anything at a factor of 2.4
   in either direction. That cuts in favour of S45's non-exclusion, but it also means the
   reconciliation is not a positive demonstration.

### 4.2 Where the exposure went, which is not a number

Sourcing f exposed a different premise. The stepped reconciliation needs M3 to be the EI **of the
proximal unsegmented section**. The abstract's words are "flexural stiffness **of the fin ray**",
singular, with no section named. That wording reads at least as naturally as a single whole-ray
value. This is my reading of the authors' sentence; they do not say which they meant. On a
**whole-ray uniform** reading, my computation (§D of the script) gives a predicted cantilever slope
of **49.9 N m⁻¹ against the measured 1.98 N m⁻¹, 25.2 times too stiff**. That would contradict
Alben's measurement directly and turn S45 into a named refutation, as S45 §6.2 anticipated.

So the conclusion now rests less on any number than on **which structure the 565×10⁻⁶ N·m²
describes**, and on **how it was "calculated"**. The abstract does not let me decide either, and
the body text is could-not-access (§3.2). One more point is inference only: the abstract reports a
vortex-impact force of 67 ± 2.3 mN and curvatures. A value derived from those would be an
*in-vivo apparent* EI under dynamic load. That is a different kind of quantity from Alben's
quasi-static bending EI, so the two may not be commensurable at all. I could not check this.

### 4.3 What this pass does NOT establish

- It does not establish that M3 is a proximal-section value. It only establishes that **if** it is
  one, the section boundary the same authors report (f = 0.40) is inside the computed admissible
  window 0.186 < f < 0.486.
- It does not re-examine S45's other six candidates or its corpus scope (about 50 of 290+ claims
  unswept because the claim registry is blocked). Those parts of S45 are inherited unchanged and are
  listed in `depends_on`.
- The stepped model is Euler–Bernoulli with no shear coupling. Alben 2007 places the real ray in a
  shear-dominated regime (G ≈ 10²), so every EI in §2 is an *apparent* rigidity from a model the
  source says does not fully apply. As S45 argued, that makes it the right test of whether M1
  *excludes* M3, not a description of the ray.
- It does not touch any zebrafish feasibility conclusion. All values here are bluegill.

## 5. What would change the verdict

1. **Flammang 2013 body text** (needs `sites.harvard.edu` allowed, or a library copy). If 565×10⁻⁶
   N·m² is a whole-ray or distal value, S45 **falls**: Alben's measurement contradicts it by 25
   times. If it is the proximal unsegmented section, S45 strengthens. This is the decisive read.
2. **Measured segmentation fraction with spread.** If the true unsegmented fraction of Alben-sized
   rays exceeds 0.486, the reconciliation fails on geometry alone (computation, §2).
3. **A per-section bending test**: three-point bending of excised proximal and distal segments of a
   bluegill pectoral ray. That measures the step directly and replaces the whole stepped-model
   inference.

---

```swarm-result
{"subproblem": "S45-D", "evidence": "derived",
  "answer": "S45 stands: its deciding stepped-ray reconciliation is insensitive to the contested 565e-6 N m^2 value (x2 moves the result 2%) but flips if the stiff proximal fraction f exceeds 0.486; f was an unsourced assumption of 0.40 in S45 and is now sourced to Flammang et al. 2013's abstract ('the distal 60% of the fin ray is segmented', f = 0.40), keeping the reconciling distal EI at 2.44e-6 N m^2 inside Alben et al. 2007's measured 1e-6 to 1e-5 bracket, while the remaining exposure is whether the 565e-6 value describes the proximal section or the whole ray, which on a whole-ray reading would be 25x too stiff for Alben's measured slope and would make S45 a refutation.",
  "key_number": "f = 0.40 (unsegmented proximal fraction of bluegill pectoral ray, dimensionless; Flammang et al. 2013 abstract, spread unknown); computed admissible window 0.186 < f < 0.486",
  "verdict": "stands",
  "depends_on": [
    "S45 (docs/research/fish/S45-organism.md, branch claude/zebrafish-flight-s45-organism-epe63k, commit d188d0e1)",
    "S45 corpus scope: 237 of 290+ claims swept; claim registry frontier.morphoswarm.ai unswept",
    "S45 classifications of candidates 2-7 (S18, S14/S15, S15 lat4a, S13, S23, S9), inherited unexamined",
    "S6 / S6-D passive-ray feasibility branch resting on 565e-6 N m^2",
    "Flammang et al. 2013 J Morphol 274:1044, doi:10.1002/jmor.20161: distal 60% of bluegill pectoral ray segmented (f = 0.40), abstract read-level",
    "Flammang et al. 2013: fin-ray flexural stiffness 565e-6 N m^2, 'calculated', abstract read-level, section referent unknown",
    "Alben, Madden & Lauder 2007 J R Soc Interface 4:243, doi:10.1098/rsif.2006.0181: measured EI ~1e-6 to 1e-5 N m^2 (3-point bending), via S45 full-text read",
    "Alben et al. 2007 Fig 7a: cantilever slope 1.98 N/m, both hemitrich bases clamped, load at 2L/3, via S45 full-text read",
    "Alben et al. 2007 Sec 5.2: slope is force vs TIP deflection (load-point convention would flip the result), via S45 full-text read",
    "Alben et al. 2007 Sec 2: ray length L = 40.3 +/- 0.8 mm",
    "assumption: two-section Euler-Bernoulli cantilever, no shear coupling (source places ray at G ~ 1e2)",
    "assumption: Flammang's segmentation fraction applies to rays of Alben's 40.3 mm length",
    "computation: S45_deepen_calc.py (distal EI 2.44e-6 N m^2 at f = 0.40; whole-ray uniform 565e-6 predicts k = 49.9 N/m)"
  ]}
```
