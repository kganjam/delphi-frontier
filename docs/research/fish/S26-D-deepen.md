# S26-D-D: Deepening S26-D by attacking its weakest input

**Status:** deepening pass on S26-D. I did calculation and literature work only. **I measured nothing.** Each
number is tagged *measured* (by the cited authors), *calculated* (by me, in
[`S26_DD_calc.py`](S26_DD_calc.py), run with `python3 -I`), *inferred* (my reading, not the authors' claim) or
*assumption*.

## 0. What I was handed and what I found upstream

The brief's "recorded answer" field arrived **empty**. I reconstructed the chain from sibling branches. I read
all four documents in full:

| Document | Branch | Claim |
|---|---|---|
| S26-D, `S26-deepen.md` + `S26_deepen_calc.py` | `origin/claude/deepen-s26-active-stiffening-48xj8q` (95578def) | S26's "no" **falls**. The 165x gap compares a ≤40 mm bluegill ray with a 120 mm per-ray requirement. Under isometric EI ∝ L^4 scaling (×78.6), the passive gap is ~2.1x, and the measured ~12x hemitrich-locking factor closes it with a ~5.7x margin. Conditional on isometry and on in-vivo clamping. |
| challenge-92 | `origin/claude/challenge-s26-active-stiffening-acr1ha` | **Weakened.** On the primary-derived one-free baseline (1.07e-6 N m^2), 7.5x is needed and the margin is 1.6x. "Isometry" is ray-only d ∝ L at fixed body mass. The yes needs diameter exponent b ≥ 0.89 on the primary path. |
| replicate-92 | `origin/claude/rederive-s26-deepen-7t7q55` | **Agrees** (2.1x needed, 5.7x margin). It fails only at EI_src ≈ 1e-6 with n ≤ 3.5. |
| S26 (organ) | not re-read here. Summarised by S26-D §0 | "No": 12x against a 165x gap. |

So the claim I am deepening is **S26-D's: "with size correction, a ~12x active locking factor carries the
per-ray load; the passive shortfall is only ~2x."**

## 1. The input the answer is most sensitive to, shown by recomputing

S26-D's conclusion is one inequality (*calculated* structure):

`margin = F_a × EI_src × (L_req / L_src)^n × (d_true/d_iso)^4 / EI_req ≥ 1`

The last factor is my addition. It is the ratio of the real diameter of a 120 mm ray to the diameter that
isometric scaling predicts. S26-D implicitly sets it to 1.

All rows are *calculated* (`S26_DD_calc.py` §1):

| Input changed by 2x | Relay path (S26-D, baseline margin 5.69) | Primary one-free path (challenge-92, baseline 1.60) |
|---|---|---|
| EI_req ×2 / ÷2 | 2.85 / 11.4 — pass both | **0.80 fail** / 3.20 |
| EI_src ×2 / ÷2 (same as size factor S ×2 / ÷2) | 11.4 / 2.85 — pass both | 3.20 / **0.80 fail** |
| F_a ×2 / ÷2 | 11.4 / 2.85 — pass both | 3.20 / **0.80 fail** |
| L_src ×2 / ÷2 | **0.36 fail** / 91 | **0.10 fail** / 25.6 |
| **Diameter of the 120 mm ray ×2 / ÷2** | 91 / **0.36 fail** | 25.6 / **0.10 fail** |

Reading this:

- On S26-D's own path, **no 2x error in EI_req, EI_src or F_a flips the conclusion.** The 5.7x margin absorbs
  each one. This is why a 2x test on those three inputs, which S26-D ran, could not find the weak point.
- **What flips it at 2x is the geometry of the size correction:** the real cross-section of a 120 mm ray (or,
  equivalently, the source length). It enters at the fourth power, so a 2x error becomes 16x.
- The tolerance is narrow. On the relay path, 12x stops closing the gap if the real 120 mm ray is thinner than
  isometry predicts by more than **35%** (break-even diameter ratio 0.647). On the primary path the limit is
  **11%** (ratio 0.889).
- In exponent form, EI ∝ L^n: break-even **n = 2.41** (relay) and **n = 3.57** (primary). Lowering n by 0.64
  halves the size factor.

**The single most sensitive input is the passive EI of a ray at the requirement's length (120 mm).** In
S26-D, it is set by the assumption that ray diameter scales in proportion to ray length (n = 4). Upstream it
was carried as "EI_passive". It is really a quantity nobody has measured, built from a 40 mm measurement plus
an extrapolation exponent.

## 2. How well is that input established?

**Evidence level: assumption, stacked on a cross-taxon proxy.**

- The **40 mm baseline** is measured, but for bluegill, and it is disputed. It might be the 3.8e-6 relay, the
  1.07e-6 one-free back-calculation, or Flammang 2013's 565e-6 abstract value. Challenge-92 and S26-D record
  that disagreement, and I keep it.
- The **exponent n = 4** is an assumption. No source upstream measured how fin-ray EI or diameter scales with
  ray length or body size. S26-D tags it as an assumption. Challenge-92 shows it is ray-only scaling at fixed
  body mass, not isometry of a fish.
- It has been **repeated until it reads as measured**. The headline "passive gap only ~2x" in S26-D and
  replicate-92 reads like a property of rays. It is a consequence of n = 4. Replicate-92's "agreement" shares
  this assumption, so it is not independent evidence on this point. Replicate-92 says so itself.

## 3. Going to improve it

### 3a. The real quantity: diameter / EI of an exocoetid pectoral ray (not found)

The real quantity is EI, or the cross-section, of a pectoral ray about 120 mm long in a fish of the size behind
EI_req.

**Negative search, with its scope:**

- WebSearch standard, "flying fish Exocoetidae pectoral fin ray diameter cross-section stiffness
  morphology". No source gives exocoetid ray diameter, cross-section or EI. It surfaced Fish 1990 (wing
  morphometrics: area, span, loading). Read-level **search-summary**. Ray dimensions are not reported in the
  summary.
- WebSearch standard, "Cypselurus flying fish pectoral fin rays bending stiffness specimen". No ray
  stiffness. The Park & Choi work used dried, mounted specimens. Read-level **search-summary**.
- WebSearch extended, "allometry fin ray lepidotrichia thickness diameter body size scaling flexural
  stiffness ontogeny". It found **no** study of how fin-ray diameter or EI scales with size in any teleost.
  Read-level **search-summary**.
- Europe PMC REST, query `("fin ray" OR "fin rays" OR lepidotrichia) AND ("flexural stiffness" OR "bending
  stiffness" OR "second moment of area") AND (allometr* OR "body size" OR "standard length" OR scaling)`.
  It returned **11 hits**, and I screened all 11 titles. Two were read in full text:
  - Stewart et al. 2020 PNAS, PMC6983361: second moment of area of hemitrichia in *Tiktaalik* and
    *Eusthenopteron*. These are fossils, n = 2 individuals per taxon, and the paper gives no extant-teleost
    exponent. Not usable.
  - Nguyen et al. 2017 *J R Soc Interface*, PMC5454310: curvature stiffening. No scaling data.
  - The other relevant hit is used in §3b.
- **Not searched:** Google Scholar, Web of Science, ZFIN, MorphoSource itself.
- **Could not access** (proxy 403 or DNS blocked in this session):
  - web.njit.edu (a Flammang 2013 full-text PDF. This would settle the 565e-6 vs 3.8e-6 disagreement.)
  - sites.harvard.edu
  - uchicago.cottagelabs.com (Aiello PhD thesis, reported to contain a chapter figure on body size vs flexural
    stiffness)
  - datadryad.org (Aiello 2017 data)
  - bamlab.princeton.edu (flying-fish paper)

  These hosts would have to be allowed in the session's network settings.

**Result: the exponent and the exocoetid ray diameter are `unknown`.** The negative applies only within the
scope above.

### 3b. What I could improve: an independent, measured anchor at a known ray length

**Aiello, Westneat, Hale et al. 2017**, *PNAS* 114:4459, "Mechanosensation is evolutionarily tuned to locomotor
mechanics", doi:10.1073/pnas.1616839114, PMC5410822. Read-level **full-text**: I fetched the PMC HTML with curl
and stripped the tags myself. The Europe PMC XML endpoint returned HTTP 500.

Verbatim, *measured* by the authors:

- "The average flexural stiffness, or resistance to bending, at 50% fin ray length was between 190 ± 30 and
  210 ± 50 × 10^−9 N⋅m^2 (average ± SD) among the high AR species and between 20 ± 10 and 40 ± 10 × 10^−9
  N⋅m^2 among the low AR species."
- Method: three-point bending of **ray 3**, span = 20% of ray length, deflection ≤ 10% of span,
  EI′ = F·L^3/48Y. Tested within 4 h post mortem.
- Fish: eight labrid species, size-matched within pairs, standard length 7.3–13.2 cm.
- Response thresholds are given both as % ray length and in mm. For example, "5.91 ± 0.58 and 8.20 ± 3.03%
  fin ray length (1.05 ± 0.3 and 1.5 ± 0.42 mm)" for high-AR species.

**Ray length, *inferred* by me** (not stated as such by the authors): dividing each mm value by its paired
percentage gives **17.8–20.2 mm** for ray 3 (*calculated*). I am assuming the min/max pairing is the one the
sentence implies.

Why this matters:

- It is a **second lab, a second family and a second method** (three-point bending, not cantilever).
- It is reported **with n and SD**, at a known ray length and fish size.
- High-aspect-ratio "wing-like" labrid fins are the closest available mechanical analogue to a flying-fish
  pectoral wing. That is my inference.
- Three-point bending of a short excised span leaves the hemitrichs unclamped at the span ends. So I treat it
  as roughly the **passive** state. This is an inference, and the paper does not discuss hemitrich locking.
- It is measured at **50% length**. Stiffness falls exponentially along the ray, and a tip-loaded cantilever
  is governed by the base. So for the cantilever requirement, a mid-ray value is conservative (*inferred*).
  The companion abstract (Aiello et al. 2017 *J Exp Biol* jeb163360, read-level **abstract**, Europe PMC)
  reports proximal values up to 1.51 µN m^2 = 1.5e-6 N m^2.

**Recomputed with this anchor**, same n = 4 so that it is comparable (*calculated*, §2):

| Labrid phenotype | EI at ~18–20 mm (measured) | scaled passive EI at 120 mm | active factor needed | 12x margin |
|---|---|---|---|---|
| high-AR (wing-like) | 1.9–2.1e-7 N m^2 | **2.4e-4 to 4.4e-4 N m^2** | **1.4x–2.7x** | **4.5–8.3, pass** |
| low-AR (paddle) | 2–4e-8 N m^2 | 2.5e-5 to 8.3e-5 N m^2 | 7.6x–25x | 0.48–1.59, mostly **fail** |

- **High-AR anchor.** It independently reproduces S26-D's ~2.1x (3.0e-4 N m^2 scaled) from a different
  species, lab and method. It **does not support** challenge-92's 7.5x primary-path figure, but it does not
  refute it either. That disagreement is about which bluegill state the 12x multiplies. It is preserved, not
  resolved.
- **Low-AR anchor.** Here 12x mostly fails. So the answer depends on ray phenotype. A flying fish is assumed,
  not shown, to sit at the stiff end.

**The anchor does not fix the weakest input.** It needs a larger length extrapolation (×6.3 in length, against
×3.0 from bluegill), so it is *more* exposed to the exponent:

- break-even n = **3.02** for the high-AR anchor;
- break-even n = **4.05** for the low-AR anchor;
- at n = 3, the high-AR anchor needs 12.5x, so 12x just fails;
- at n = 3.5, it needs 5.0x.

**A two-point interspecific exponent check (*calculated*, §3; weak).** Bluegill at 40.3 mm against labrid at
19 mm gives:

- n = 3.9 (relay vs high-AR);
- a full range of n = 2.1 to 7.7 across the baseline choices.

This mixes species, methods and ray regions. **It does not constrain n**, and I do not use it as a
measurement. I report it only so that nobody reads it as support for n = 4.

### 3c. The measurement that would settle it, and its cost

1. **Existing CT data, cheapest.** An oVert micro-CT record exists for *Exocoetus volitans*, UF Fish 231939,
   on MorphoSource as record 000S13364 (read-level **search-summary**, from a Sketchfab listing. I did not
   open MorphoSource).
   - Whether the pectoral fin is inside the scanned volume is `unknown`. The listing says "skull and partial
     skeleton".
   - If it is, measure the hemitrich cross-section and I at 10–90% span of the leading pectoral rays. Combined
     with an assumed bone modulus, this gives the real d at the right length and replaces n.
   - Cost (my estimate, not sourced): free data, about 1–2 analyst-days.
2. **Direct test.** Three-point bending (Aiello protocol) plus cantilever tests with bases free, one free and
   both clamped, on 3–5 excised exocoetid pectoral rays (fishery by-product), with micro-CT. This measures
   passive EI at 120 mm and a second, replicated locking factor.
   - Cost (my estimate): a few person-weeks with a micro-mechanical tester.
3. **An ontogenetic exponent from existing data.** Aiello 2017 tested *H. bivittatus* over standard length
   5.3–16.2 cm. The stiffness-vs-size relation is not reported in the main text; its Table S7 relates threshold
   to stiffness and size. The Dryad archive doi:10.5061/dryad.0463n may allow EI vs ray length to be fitted
   within one species.
   - Cost: zero, once datadryad.org is reachable.

## 4. Recompute and verdict: STANDS

All figures *calculated*:

- **S26-D's central number survives an independent primary cross-check.** A measured, replicated (with SD)
  wing-like labrid ray, scaled the same way, needs 1.4–2.7x active stiffening. S26-D's bluegill-relay route
  needs 2.1x. The 12x locking factor clears both, with a 4.5–8.3x margin.
- **It does not strengthen**, because the input the conclusion is most sensitive to was not improved by any
  measurement. That input is the cross-section (EI) of a real 120 mm ray, equivalently the exponent n.
  - It is still an assumption (n = 4).
  - The yes holds only if the real ray is no more than 35% thinner than isometry predicts on the relay path,
    11% on challenge-92's primary path, or n ≥ 3.0 on the labrid anchor.
  - No exocoetid ray dimension was found within the scope of §3a.
- **It does not fall.** No source found contradicts n ≈ 4. The paddle-fin (low-AR) anchor fails, which shows
  the answer is phenotype-conditional. It is not evidence about flying fish.

**The conclusion, with its conditions stated:** S26-D's "falls" for S26's "no" stands, as a **conditional
yes**. Active hemitrich locking (~12x, n = 1, excised) can carry the per-ray load if a 120 mm flying-fish
pectoral ray is built like a scaled-up wing-type ray, with diameter ∝ length within ~35%. That condition is
unmeasured. The cheapest test is one existing CT scan.

Also unaddressed, carried forward:

- in-vivo achievability of 12x (S26-D, *unmeasured*);
- whole-fish isometry raising EI_req (challenge-92 §3a);
- the Flammang 565e-6 vs 3.8e-6 disagreement (D1, unresolved; full text blocked);
- the fact that EI_req is for a 100 g fish, not a zebrafish.

## 5. Sources and read-levels

- S26-deepen.md and S26_deepen_calc.py, challenge-92.md, replicate-92.md: **full-text** (repo branches named
  in §0).
- Aiello et al. 2017 *PNAS* 114:4459, PMC5410822: **full-text** (PMC HTML via curl, tags stripped by me).
- Aiello et al. 2017 *J Exp Biol* 221 jeb163360: **abstract** (Europe PMC REST).
- Aiello et al. 2018 *J Morphol* 279:1031, doi:10.1002/jmor.20830: **abstract** (Europe PMC REST). It reports
  that I explains most of the variation in EI. It gives no size-scaling numbers in the abstract.
- Stewart et al. 2020 *PNAS*, PMC6983361: **full-text** (Europe PMC XML). Not usable (fossil taxa).
- Nguyen et al. 2017 *J R Soc Interface*, PMC5454310: **full-text** (Europe PMC XML). No scaling data.
- Flammang et al. 2013 *J Morphol* 274:1044: **could-not-access** (web.njit.edu DNS-blocked; sites.harvard.edu
  blocked). A search snippet mentioned a basal-unsegmented EI value, but the units were garbled in the snippet,
  so it is **not used**.
- Fish 1990 (flying-fish wing design), Park & Choi (gliding *Cypselurus*): **search-summary**. No ray
  dimensions surfaced.
- oVert *Exocoetus volitans* UF 231939, MorphoSource 000S13364: **listing** (via search-summary of a Sketchfab
  page). Not opened.
- Alben et al. 2007 (12x, 40.3 mm, B ≈ 1e-6 to 1e-5), Puri et al. 2018 (3.8e-6 relay), S6-D (EI_req): **not
  re-read by me**. I used them as quoted upstream, at the read-levels recorded there.

```swarm-result
{"subproblem": "S26-D-D", "evidence": "derived: calculation; size-corrected baseline cross-checked against an independent measured anchor (Aiello et al. 2017 PNAS labrid ray-3 three-point bending, full-text); the decisive scaling exponent / 120 mm ray cross-section remains an unmeasured assumption", "answer": "S26-D's conclusion stands as a conditional yes: its most sensitive input is the passive EI (cross-section) of a 120 mm ray, which enters as diameter^4 so a 2x diameter error flips the result (relay margin 5.69 -> 0.36) while 2x errors in EI_req, EI_src or F_a do not; an independent measured wing-like labrid anchor (1.9-2.1e-7 N m^2 at ~18-20 mm) scaled the same way reproduces a 1.4-2.7x passive shortfall that 12x clears, but no exocoetid ray dimension or EI-size exponent was found, so the yes still requires the real ray to be no more than ~35% thinner than isometry predicts (n >= 2.4 relay, >= 3.0 labrid anchor, >= 3.57 primary path).", "key_number": "passive EI of a 120 mm ray from the labrid high-AR anchor scaled at n=4: 2.4e-4 to 4.4e-4 N m^2 (calculated; source measured 1.9-2.1e-7 N m^2 at 17.8-20.2 mm), i.e. 1.4-2.7x active factor needed; break-even diameter ratio 0.647 (relay) / 0.889 (primary)", "verdict": "stands", "depends_on": ["S26-D claim: docs/research/fish/S26-deepen.md on origin/claude/deepen-s26-active-stiffening-48xj8q (2.1x needed, 5.7x margin, falls)", "challenge-92: primary one-free baseline 1.07e-6 N m^2 gives 7.5x needed, margin 1.6x; whole-fish isometry objection", "replicate-92: agreement sharing EI_req, relay and n=4", "S6-D EI_req 6.3e-4 N m^2 per ray (m=0.10 kg, N=14, L=0.12 m, delta/L<=0.10)", "Puri et al. 2018 relay: bluegill ray EI 3.8e-6 N m^2 citing Flammang 2013", "Flammang et al. 2013 abstract 565e-6 N m^2 (disagreement D1 unresolved)", "Alben et al. 2007: ~12x clamped vs one-hemitrich-free, effectively n=1", "Alben et al. 2007: bluegill max pectoral ray length 40.3 +/- 0.8 mm", "S26-D back-calculation: bluegill one-free EI 1.07e-6 N m^2 (uniform cantilever, load at 2/3 L, L=40.3 mm)", "Aiello et al. 2017 PNAS (PMC5410822): labrid ray-3 EI at 50% length 190-210e-9 N m^2 high-AR, 20-40e-9 N m^2 low-AR, three-point bending, SL 7.3-13.2 cm", "inference: labrid ray-3 length 17.8-20.2 mm from paired %-length and mm thresholds in Aiello 2017", "inference: three-point bending of excised span approximates the passive (unlocked) state", "inference: mid-ray EI is conservative for a base-dominated cantilever", "assumption: EI ~ L^4 (diameter proportional to ray length, constant modulus and section shape) from source ray to 120 mm ray", "assumption: flying-fish pectoral rays resemble high-AR wing-like rays rather than low-AR paddle rays", "assumption: excised-ray 12x locking factor is achievable in vivo", "negative search: no exocoetid ray diameter/EI and no fin-ray EI-size exponent found (scope: 3 WebSearch queries, 1 Europe PMC query with 11 hits; Scholar/WoS/ZFIN/MorphoSource not searched; njit/harvard/dryad/uchicago/princeton hosts blocked)"]}
```
