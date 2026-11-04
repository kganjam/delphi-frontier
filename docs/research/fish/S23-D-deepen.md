# S23-D-D — Deepening S23-D by attacking *its* weakest input

Parent: `S23-D`, *"Deepen S23: attack its most sensitive input"*, recorded in
`docs/research/fish/S23-deepen.md` on branch `claude/deepen-s23-actinotrichia-bhvko5`
(read at `full-text` for this work, together with its calculator
`docs/research/fish/S23-deepen-calc.py`).
Grandparent: `S23` (protein), `docs/research/fish/S23-protein.md` on branch
`claude/s23-actinotrichia-stiffness-protein-wwp5m2` (read at `full-text`).

Date of work: 2026-11-04. Reproduction: `python3 docs/research/fish/S23-D-D-calc.py`.
**Every number in §1, §4 and §5 is computation, not observation.** Where a number is a
measurement I name the paper and the read-level in the same sentence.

---

## 0. The parent's conclusion, as the inequality it actually is

S23-D re-expressed S23 as a margin and declared it **STANDS**:

```
margin = S / C > 1
S = EI_req / EI_meas        EI_req = (W/2) L^2 / (8 * tol)     (uniform-load cantilever)
C = E_target / E0           (material ceiling, at f = 1)
```

Its recorded margins, which I reproduce exactly (§1 of the calculator):

| design corner | `S` | `C` | margin | parent's verdict |
|---|---|---|---|---|
| central: `L` = 4 cm, tol = 10 %, `EI_meas` = 4×10⁻⁹ | 981 | 29 | 33.8 | holds |
| central, dry-collagen target | 981 | 14 | 70.1 | holds |
| **lenient: `L` = 2 cm, tol = 50 %, `EI_meas` = 5×10⁻⁹** | **39.2** | **29** | **1.353** | holds, barely |
| lenient, dry-collagen target | 39.2 | 14 | 2.80 | holds |

The parent found its weakest input to be `E0` (the actinotrichial baseline modulus),
improved it from a generic-collagen AFM proxy to an elastoidin lower bound of ≥ 0.35 GPa,
and concluded that the surviving margin at the lenient corner is ~1.4×.

**That 1.353 is the whole story of this document.** A conclusion whose worst case is a
margin of 1.353 is not robust to anything. It can be destroyed by a 36 % error in any
single multiplicative input. So the question "which input is it most sensitive to" has a
sharper answer than the parent gave.

---

## 1. Which input is the answer most sensitive to? (computed)

### 1.1 The parent's own tie-break was spent, and it picked the wrong successor

The parent correctly observed that on a log scale every input has the same elasticity —
each enters `S/C` multiplicatively, so a factor-of-two error in any one moves the margin by
exactly 2× (`L` by 4×, entering squared). It therefore tie-broke on *which input is least
well established*, chose `E0`, and improved it.

After that improvement, `E0` is **no longer** the weakest input. The parent computed the
flip thresholds itself: `E0*` = 255 MPa at the lenient corner and 10 MPa at the central
case. Its improved bound (≥ 0.35 GPa) sits above both, and it has two independent reasons
for setting aside the MPa branch that used to straddle them. `E0` has headroom now.

So I re-ran the tie-break over what remains. The surviving inputs are:

| input | status in the parent | established? |
|---|---|---|
| `E0` ≥ 0.35 GPa | improved by S23-D | bounded above the flip threshold |
| `tol` = 5–50 % | acknowledged design assumption, range stated | soft but **declared** soft |
| `L` = 2–4 cm, `m` = 0.4 g | acknowledged design assumptions | soft but **declared** soft |
| `f` = 1 | set to the value most favourable to gain-of-function | conservative by construction |
| **`EI_meas` = 1.5–5×10⁻⁹ N·m²** | carried as **measured** (Puri 2018, `full-text`) | **measures the wrong organ** |

`EI_meas` is the one input that is carried as a measurement and is not one. Puri et al.
2018 measured the **caudal** fin of adult zebrafish. The conclusion is about a **pectoral**
fin, because the pectoral fin is the only candidate glide wing. Substituting one for the
other introduces a ratio

```
R = EI_pectoral / EI_caudal
```

which **neither S23 nor S23-D ever estimated**. Both implicitly set `R = 1`. S23 flagged the
junction in its §5 point 5 ("Uncalibrated junction") and then used the number anyway;
S23-D's sensitivity table perturbed `EI_meas` by factors of two but never asked which fin it
described. This is precisely the brief's third category: *an assumption that has been
repeated until it reads as measured*. The measurement is real; its application to the wing
is an assumption, and it is an assumption with a hidden free parameter set silently to 1.

### 1.2 The sensitivity, shown by recomputing

The conclusion flips when `margin < 1`, i.e.

```
R* = EI_req / (C * EI_caudal)
```

Computed (calculator §2):

| design corner | `C` | flip threshold `R*` |
|---|---|---|
| central (4 cm, 10 %, 4×10⁻⁹) | 14 | 70.1 |
| central | 29 | 33.8 |
| lenient (2 cm, 50 %, 5×10⁻⁹) | 14 | 2.80 |
| **lenient** | **29** | **1.35** |

**A 35 % error in `R` flips the parent's conclusion at its lenient corner.** Not a factor of
two — 1.35×. That is a far tighter tolerance than any other input in the chain enjoys, and it
sits on the one quantity nobody has looked at. `R` is the weakest input of S23-D.

A note on fairness to the parent: this is not a new weakness I introduced. It was always
there, inherited from S23, and it is *why* the parent's lenient-corner margin of 1.353 should
never have been reported as "holds, barely" without naming what it was resting on.

---

## 2. How well is `R` actually established? (honest read)

**Evidence level for `R` in the parent: `assumption, undeclared`.** This is a worse grade
than the one S23-D gave the input it chose to attack. `E0` was at least an explicit
`assumption via proxy` with a stated provenance. `R` has no provenance at all: it does not
appear as a symbol in either ancestor document, and its value of 1 is a consequence of
silently reusing a caudal number, not of a choice anyone defended.

What *is* established, stated precisely:

- **`EI_caudal` = 1.5–4×10⁻⁹ N·m² (abstract) and 2–5×10⁻⁹ N·m² (conclusions)** for the adult
  zebrafish caudal fin. Measured, in vivo. Puri et al. 2018, *J Exp Biol* 221:jeb171777,
  read-level `full-text` (as recorded by both ancestors; not re-read for this work). The
  internal spread of ~3× is the paper's own, and I keep both ranges rather than reconciling
  them.
- **`EI_pectoral` for zebrafish: `unknown`.** Scope of this negative: web index only, English,
  2026-11-04, extended mode, query `zebrafish pectoral fin flexural stiffness EI measurement
  bending rays`. The search returned the caudal-fin paper and pectoral-fin studies in other
  species; it returned no measurement of zebrafish pectoral-fin bending stiffness. I did not
  query PubMed, Web of Science or bioRxiv systematically, and I did not hand-search
  *J Exp Biol* or *J Morphol* tables of contents. A measurement the index ranks poorly would
  be missed.
- **Zebrafish pectoral ray count: 10–14**, with one source giving a wild-type mean of 10.8
  rays per pectoral fin (n = 6) and a developmental-anatomy source giving 11–13. Read-level
  `search-summary` (query `zebrafish pectoral fin ray number length morphometrics Danio rerio
  adult fin ray diameter`, 2026-11-04). **Zebrafish pectoral ray diameter: `unknown`** — the
  same search returned no ray diameter or ray length for the adult pectoral fin, and the
  summary itself said a micro-CT or Alizarin morphometry search would be needed.

So the quantity the conclusion is 35 %-sensitive to is the ratio of a measured number to an
unmeasured one.

---

## 3. Going and improving it

I could not find `R` measured for any species as a single reported ratio. I found three
independent lines that bear on it. **They disagree, and I am not averaging them.**

### Line A — a same-species, same-method ranking (the strongest line, and it has no number)

- **"Variation in flexural stiffness of the lepidotrichia within and among the soft fins of
  yellow perch under different preservation techniques," *Journal of Morphology*,
  doi:10.1002/jmor.20831.** Read-level: **`abstract`** / `search-summary`. Direct fetch of
  `onlinelibrary.wiley.com` returned **HTTP 403**, so the full text, the sample sizes, the
  fish body sizes and every numeric EI value are `could-not-access`. A search summary
  attributed the work to Taft, Taft, Henck and Mehner (2018); **I could not verify that
  author list against the full text and do not rely on it.**
  - **Authors' claim, as given in the abstract text returned:** three-point bending across the
    soft fins of *Perca flavescens* found that "the pelvic rays were significantly stiffer
    than the other fins and the pectoral fins the least stiff," with dorsal, anal and caudal
    rays similar to one another and intermediate between the paired fins. Rays on a fin's
    leading edge were stiffer than rays elsewhere in the same fin. Freezing had no significant
    effect; formalin reduced the stiffness of rays under 25 mm; the ranking held under every
    preservation method.
  - *My inference, not the authors' framing:* this is a direct, statistically tested,
    same-species, same-method comparison that places pectoral rays **below** caudal rays. It
    is evidence that **`R` < 1**. It gives no number, so it bounds `R` from above and no more.

### Line B — a review claim that puts `R` ≈ 1

- **Flammang et al. 2013, "Functional Morphology of the Fin Rays of Teleost Fishes,"
  *J Morphol*.** Read-level: **`search-summary`** only. Both mirrors I tried,
  `web.njit.edu` and `public.websites.umich.edu`, returned `ENOTFOUND` from this sandbox;
  they have to be allowed in the session's network settings before the paper can be read.
  - **Claim as relayed by the search summary:** fish fins that appear to play similar
    functional roles, "such as the pectoral and caudal fins of actinopterygian fishes," have
    fin rays with similar morphology and flexural stiffness.
  - This is a general statement about clades, not a same-species measurement, and the search
    summary itself noted that it "conflicts somewhat with the yellow perch result."
    **Disagreement preserved:** Line A says pectoral < caudal with statistics in one species;
    Line B says pectoral ≈ caudal as a generalisation across actinopterygians. I record both.

### Line C — the only line with numbers, and it is mine, and it is the weakest

There exists a measured pectoral-ray EI dataset, in a different family.

- **"The relationship between pectoral fin ray stiffness and swimming behavior in Labridae:
  insights into design, performance and ecology," *J Exp Biol* 221(1):jeb163360.**
  Read-level: **`full-text`** (journals.biologists.com page fetched 2026-11-04, first
  ~100 000 of 162 425 characters read; Table 1 and the final ~62 000 characters
  `could-not-access`). The author list was not in the portion I read, so I cite by title and
  identifier only and do **not** assert authors.
  - **Authors' measurements:** three-point bending, `EI = F d³ / (48 Y)`, support span 20 % of
    ray length, loading 0.1 mm s⁻¹, displacement held to 10 % of ray length. Pectoral fin ray
    flexural stiffness ranged **0.0001 to 1.5109 µN·m²** overall. Leading-edge rays:
    *Gomphosus varius* (flapping, n = 7, 7.8–39.8 g, mean 22.44 ± 13.19 g) proximal
    **0.8899 ± 0.4587** and middle **0.1588 ± 0.0613 µN·m²**; *Halichoeres bivittatus*
    (rowing, n = 8, 6.0–64.6 g, mean 22.03 ± 19.05 g) proximal **0.1671 ± 0.1496** and middle
    **0.0676 ± 0.0762 µN·m²**. Stiffness fell exponentially proximal→distal. The authors
    report EI as a single variable and state that `E` and `I` could not be separated reliably
    for this composite structure, so **no Young's modulus is reported.**
  - *My computation, not the authors':* scale these to a 0.4 g *Danio* under geometric
    similarity. With `EI = E·I`, `I ∝ d⁴`, `d ∝ L_body` and `L_body ∝ m^(1/3)`, and `E`
    size-invariant, `EI ∝ m^(4/3)`. The scale factor is `(0.4/22.44)^(4/3) = 4.656×10⁻³`.
    Self-consistency check on the isometry: a 56× mass ratio implies a 3.8× length ratio, so
    a ~15 cm wrasse maps onto a ~4 cm *Danio* — the assumption is at least not internally
    contradictory.

| labrid leading-edge ray (measured) | scaled to 0.4 g (computed) |
|---|---|
| *G. varius* proximal, 8.899×10⁻⁷ N·m² | 4.144×10⁻⁹ N·m² |
| *G. varius* middle, 1.588×10⁻⁷ N·m² | 7.394×10⁻¹⁰ N·m² |
| *H. bivittatus* proximal, 1.671×10⁻⁷ N·m² | 7.975×10⁻¹⁰ N·m² |
| *H. bivittatus* middle, 6.76×10⁻⁸ N·m² | 3.226×10⁻¹⁰ N·m² |

Summing over a whole fin — `EI_whole = Σ EI_ray`, which is the right model by Puri et al.'s
own measured result that cutting interray tissue did not change fin stiffness, so the rays
dominate — with 10, 12 and 14 rays gives a scaled whole-pectoral band of
**3.23×10⁻⁹ to 5.8×10⁻⁸ N·m²**, hence

```
R  =  EI_pectoral(scaled)  /  EI_caudal(measured)   =   0.65  ..  38.7     (computed)
```

**This band straddles three of the four flip thresholds and is therefore almost
uninformative.** I report it because it is the only numeric line that exists, and I will not
quietly drop a line that fails to support the conclusion.

**Why I judge Line C's upper end not credible** (my inference, argued, not measured): the
high end requires a *Danio* pectoral fin — physically smaller than its own caudal fin, with
10–14 rays against the caudal fin's larger complement, and with ray diameters nobody has
measured — to be ten to forty times *stiffer in bending* than the caudal fin of the same
animal. Two things argue against it. First, labrid pectoral fins are specialised flapping
propulsors whose leading-edge rays are load-bearing spars; scaling a specialised spar across
families to an unspecialised fin biases the estimate high, and the paper's own leading-edge
vs non-leading-edge contrast shows the leading edge is the stiff extreme, not the average.
Second, the isometric exponent is applied across a 56× mass range and a family boundary, and
it assumes a size-invariant `E` that the labrid paper explicitly could not measure.

### The improved input

Weighing Line A (same species, same method, statistically tested, direction `R` < 1), Line B
(`R` ≈ 1 as a cross-clade generalisation), and Line C (numeric but cross-family and biased
high at its upper end), the defensible improvement is a **bound, not a number**:

```
R  =  EI_pectoral / EI_caudal   <=  1          (improved input; upper bound)
R  numeric value               =   unknown
```

It is better than the parent's hidden `R = 1` in three respects. It is *stated*, so it can be
refuted. It is supported by the only same-species, same-method comparison I could find. And
it is an upper bound in the direction that matters: it cannot hide a flip, whereas an
undeclared `R = 1` could.

It is worse than a measurement in every other respect, and I am not going to dress it up:
`R` is bounded, not known; the bound rests on an `abstract`-level read of a paper whose full
text returned 403 and whose author list I could not verify; it is a bound from a perch, not a
zebrafish; and it bounds a *ray-level* ranking which I am applying to a *whole-fin* ratio.

---

## 4. Recompute (computed)

With `R ≤ 1`, `S = EI_req / (R · EI_caudal)` is **at least** the parent's `S`, so every
parent margin becomes a **lower bound**:

| design corner | `C` | parent margin (`R` = 1) | margin with `R ≤ 1` | verdict |
|---|---|---|---|---|
| central (4 cm, 10 %, 4×10⁻⁹) | 14 | 70.1 | ≥ 70.1 | holds |
| central | 29 | 33.8 | ≥ 33.8 | holds |
| lenient (2 cm, 50 %, 5×10⁻⁹) | 14 | 2.80 | ≥ 2.80 | holds |
| **lenient** | **29** | **1.353** | **≥ 1.353** | **holds, by 35 %** |

For completeness, the margins at the endpoints of the Line C band I judged not credible
(calculator §5), reported so that a reader who weighs Line C differently can see what it
would do:

| design corner | `C` | `R` = 0.65 | `R` = 38.7 |
|---|---|---|---|
| central | 14 | 108.6 holds | 1.81 holds |
| central | 29 | 52.4 holds | **0.875 FLIPS** |
| lenient | 14 | 4.34 holds | **0.072 FLIPS** |
| lenient | 29 | 2.10 holds | **0.035 FLIPS** |

`f < 1` makes every margin larger; nothing here relies on `f`, which stays at the value most
favourable to gain-of-function.

---

## 5. Verdict

**STANDS.**

Recomputed with the improved input (`R` = `EI_pectoral`/`EI_caudal` ≤ 1, where both ancestors
had silently used `R` = 1), protein-level stiffening of actinotrichia still does not close the
S6 fin-stiffness gap, at `f` = 1 and at every design corner the ancestors state. The
parent's margins become lower bounds rather than point values.

I call it **stands** and not **strengthens**, deliberately. `R ≤ 1` admits `R` = 1 exactly, so
the worst-case margin is **numerically unchanged at 1.353**. Nothing got better; what changed
is that a hidden free parameter is now declared and bounded in the safe direction. Claiming a
strengthening would be claiming a number I do not have.

Three things this deepening establishes that the parent did not, and one it inherits:

1. **The weakest input of S23-D was not `E0`.** It was `EI_meas`, and specifically the
   undeclared caudal→pectoral ratio inside it. The flip threshold is `R*` = 1.35 at the
   lenient corner — a 35 % tolerance, tighter than any other input in the chain.
2. **The parent's lenient-corner margin of 1.353 was reported without naming what it rested
   on.** A margin that thin resting on an unexamined organ substitution should have been
   reported as indeterminate, not as "holds, barely".
3. **The only numeric line available (Line C) does not support the conclusion.** Scaling
   measured labrid pectoral-ray EI to a 0.4 g *Danio* gives `R` = 0.65–38.7, straddling three
   of four flip thresholds. I argue its upper end is not credible, but the argument is
   geometric and comparative, not measured, and a reader who weights Line C above Line A
   should read this verdict as *indeterminate* rather than *stands*.
4. **Inherited and still unrepaired:** S23's headline magnitude, "one to two orders of
   magnitude short", remains **unsupported** at the lenient corner, where the margin is 1.35×.
   S23-D found this and narrowed the claim; nothing here widens it back. The honest magnitude
   is still "short by ~1.4× to ~70×, depending on design assumptions S23 does not control."

---

## 6. What measurement would settle `R`, and what it would cost

1. **Read the yellow perch paper.** Cost: zero, once `onlinelibrary.wiley.com` is reachable or
   an institutional copy is available. doi:10.1002/jmor.20831 contains, by its own abstract, a
   same-species same-method pectoral-vs-caudal comparison. **If its tables give a numeric
   pectoral:caudal ratio, that single number converts this document's bound into a value.**
   This is the highest-value unread number in the chain, displacing Puri's Fig. S5 from the
   position S23 gave it.
2. **Read Flammang et al. 2013 and the labrid Table 1.** Also near-zero cost, once
   `web.njit.edu` or `public.websites.umich.edu` is allowed. Line B's "similar flexural
   stiffness" claim needs to be checked against whatever it cites, and the labrid Table 1
   holds the distal values and the non-leading-edge rays that would narrow Line C's band from
   the top — the end that does the damage.
3. **Measure the zebrafish pectoral fin directly.** Puri et al.'s in-vivo bending apparatus
   already resolves ~10⁻⁹ N·m² in a live adult zebrafish caudal fin; applying the same rig to
   the pectoral fin of the same animals is a protocol transfer, not a new method. Paired
   measurements on the same fish give `R` directly and remove the cross-species step
   entirely. **Decision rule, computed above:** `R` > 1.35 kills the lenient corner at the
   silk-like target, `R` > 2.80 kills it at the dry-collagen target, and `R` > 33.8 would be
   needed to kill the central case. My estimate of cost, not sourced: weeks of work for a
   group that already owns the rig; the apparatus is the expensive part and it exists.
4. **Measure adult zebrafish pectoral ray diameter and count by micro-CT.** `unknown` at
   present (§2). With diameters, `R` can be *predicted* from `I ∝ d⁴` and ray count rather
   than measured, as an independent check on (3).
5. **Still outstanding from S23-D:** read Rajaram, Sanjeevi & Ramanathan 1981, *J. Biosci.*
   3(3):303–309 for a wet elastoidin modulus. I retried `www.ias.ac.in` for this work and it
   again returned `ENOTFOUND`; it has to be allowed in the session's network settings. `E0`
   remains a conditional bound, not a read number.

---

## Sources

- Parent: `docs/research/fish/S23-deepen.md` and `S23-deepen-calc.py` @
  `claude/deepen-s23-actinotrichia-bhvko5`. Read-level: `full-text`.
- Grandparent: `docs/research/fish/S23-protein.md` @
  `claude/s23-actinotrichia-stiffness-protein-wwp5m2`. Read-level: `full-text`.
- [Puri et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/)
  — caudal-fin `EI`, ray dominance. Read-level: `full-text` **as recorded by the ancestors**;
  not re-read for this work. Supplementary Fig. S5 remains `could-not-access`.
- ["The relationship between pectoral fin ray stiffness and swimming behavior in Labridae", *J Exp Biol* 221(1):jeb163360](https://journals.biologists.com/jeb/article/221/1/jeb163360/19550/The-relationship-between-pectoral-fin-ray)
  — measured labrid pectoral-ray `EI`. Read-level: `full-text` (first ~100 k of 162 425
  characters; Table 1 `could-not-access`). Author list not in the portion read.
- ["Variation in flexural stiffness of the lepidotrichia within and among the soft fins of yellow perch…", *J Morphol*, doi:10.1002/jmor.20831](https://onlinelibrary.wiley.com/doi/10.1002/jmor.20831)
  — the pectoral-least-stiff / caudal-intermediate ranking. Read-level: `abstract` /
  `search-summary`. Direct fetch: **HTTP 403**, `could-not-access`. Author list unverified.
- Flammang et al. 2013, "Functional Morphology of the Fin Rays of Teleost Fishes", *J Morphol*
  — the "pectoral and caudal … similar flexural stiffness" claim. Read-level:
  `search-summary`. Both mirrors (`web.njit.edu`, `public.websites.umich.edu`) returned
  `ENOTFOUND`; they need to be allowed in the session's network settings.
- Zebrafish pectoral ray counts (10–14; mean 10.8, n = 6; 11–13) — Read-level:
  `search-summary` across the [2019 fin-ray/distal-radial paper](https://link.springer.com/article/10.1186/s40851-019-0145-z),
  [PMC6751676](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6751676/), and the
  [2024 HoxA/HoxD pectoral-fin paper](https://www.nature.com/articles/s41598-024-74134-9).
  I cannot say which source supplied which count in the summary.
- Rajaram, Sanjeevi & Ramanathan 1981, *J. Biosci.* 3(3):303–309 — retried for this work.
  `www.ias.ac.in`: `ENOTFOUND`, `could-not-access`. Carried forward from S23-D at
  `search-summary`.

```swarm-result
{"subproblem": "S23-D-D", "evidence": "derived",
  "answer": "S23-D's weakest input is not E0 but EI_meas, which is a measurement of the zebrafish CAUDAL fin standing in for the PECTORAL glide wing via an undeclared ratio R that both ancestors silently set to 1; the computed flip threshold is R*=1.35 at the lenient design corner, so a 35 percent error kills the conclusion, and improving R to a stated upper bound of <=1 (from the only same-species same-method comparison found, yellow perch pectoral rays least stiff and caudal intermediate, read at abstract level) leaves the parent's margins as lower bounds and the conclusion intact but numerically unimproved at 1.353.",
  "key_number": "R = EI_pectoral/EI_caudal <= 1 (upper bound, numeric value unknown); flip threshold R* = 1.35 (lenient, C=29), 2.80 (lenient, C=14), 33.8 (central, C=29), 70.1 (central, C=14)",
  "verdict": "stands",
  "depends_on": [
    "S23-D conclusion that margin = S/C > 1 at every stated design corner (docs/research/fish/S23-deepen.md, verdict stands)",
    "S23 conclusion that actinotrichial gain-of-function cannot close the S6 fin flexural-stiffness gap (docs/research/fish/S23-protein.md)",
    "S6 premise that a 4 cm 0.4 g Danio rerio paired fin must act as a load-bearing glide aerofoil",
    "E0 >= 0.35 GPa, wet elastoidin axial modulus, conditional lower bound inherited from S23-D (search-summary; Rajaram et al. 1981 could-not-access)",
    "E_target = 5 GPa (dry-collagen-like) and 10 GPa (silk-like) best-case redesign modulus, inherited from S23",
    "C = E_target/E0 = 14 to 29, material ceiling at f = 1 (computed)",
    "f = 1, the actinotrichial share of fin EI, unknown and set to the value most favourable to gain-of-function",
    "EI_caudal = 1.5e-9 to 4e-9 N*m^2 (abstract) and 2e-9 to 5e-9 N*m^2 (conclusions), measured in vivo, adult zebrafish caudal fin, Puri et al. 2018 J Exp Biol 221:jeb171777, full-text",
    "Puri et al. 2018 measured result that cutting interray tissue does not change fin bending stiffness, i.e. rays dominate fin EI (used to justify EI_whole = sum of EI_ray)",
    "R = EI_pectoral/EI_caudal <= 1, this document's improved input, an upper bound and not a measured value",
    "Yellow perch Perca flavescens three-point-bending ranking: pectoral rays least stiff, caudal intermediate, statistically significant, J Morphol doi:10.1002/jmor.20831, read at abstract level, full text HTTP 403, author list unverified",
    "Flammang et al. 2013 J Morphol review claim that pectoral and caudal fin rays of actinopterygians have similar flexural stiffness (search-summary, R approx 1, conflicts with the yellow perch ranking)",
    "Labrid pectoral fin ray EI measured by three-point bending, 0.0001 to 1.5109 uN*m^2 overall, leading-edge proximal 0.8899 +/- 0.4587 uN*m^2 (G. varius) and 0.1671 +/- 0.1496 uN*m^2 (H. bivittatus), J Exp Biol 221(1):jeb163360, full-text (Table 1 could-not-access)",
    "Labrid body masses: G. varius mean 22.44 g (n=7), H. bivittatus mean 22.03 g (n=8), from the same paper",
    "Isometric scaling assumption EI proportional to m^(4/3), from EI = E*I, I proportional to d^4, d proportional to body length, body length proportional to m^(1/3), with E size-invariant",
    "Zebrafish adult pectoral fin ray count 10 to 14 (search-summary); zebrafish pectoral ray diameter unknown",
    "Design assumptions inherited from S23: body mass 0.4 g, semi-span L = 2 to 4 cm, tip-deflection tolerance tol = 5 to 50 percent (borrowed from aeroelastic practice, not derived)",
    "Mechanics model: steady glide with lift = weight and no gust factor, two wings sharing the load, uniform-load cantilever beam with uniform EI, EI_req = (W/2)L^2/(8*tol)",
    "Euler-Bernoulli beam theory and I proportional to d^4 for a rod"
  ]}
```
