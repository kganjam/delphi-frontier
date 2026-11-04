# Challenge 138 — adversarial review of S23-D-D

**Claim under review** (claim 138, from `harvest:deepen-s23-sensitive-input-hynbng`, recorded at
evidence level `derived`). In short: S23-D's sensitivity to `E0` came from a hidden assumption,
`a/L = 1`, buried in `f = 1`. In adult zebrafish, actinotrichia occupy only the distal ~200–300 µm
of each ray. That segment holds `φ = (a/L)^4 ≈ 1e-8 to 5e-8` of a uniform-load cantilever's tip
compliance. So even infinitely stiff actinotrichia cannot supply the required 39–981× reduction in
deflection. The conclusion flips only if `a/L > 0.99` or the taper exponent is `n > 3.99`. A
full-span fin-fold design would still be governed by `E0`. Verdict as recorded: *strengthens*.

**What I read.**
- The source file `docs/research/fish/S23-D-deepen.md` and its calculation script, at commit
  `fe5ffc30` on `origin/claude/deepen-s23-sensitive-input-hynbng`: `full-text`.
- S23-D (`docs/research/fish/S23-deepen.md` @ `efff2517`), §0–§3: `full-text`.
- I did **not** read S6 or S23 directly. I took the S6 requirement (tip deflection under self-weight)
  from how S23-D states it.

**Reproduction:** `python3 docs/research/fish/challenge-138-calc.py`. Every number in §1–§3 below
was **computed** by that script. None was observed.

---

## 1. Independent arithmetic (computed)

I recomputed every value from the stated inputs: `m` = 0.4 g, half the weight per fin,
`EI_req = (W/2)L²/(8·tol)`, and `EI_meas` from Puri 2018 as S23-D carries it.

| quantity | claim | my value |
|---|---|---|
| `S` lenient (2 cm, 50 %, 5e-9) | 39.2 | 39.24 |
| `S` central (4 cm, 10 %, 4e-9) | 981 | 981.0 |
| `φ`, a = 200 µm, L = 2 cm | 1e-8 | 1.00e-8 |
| `φ`, a = 300 µm, L = 2 cm | 5e-8 | 5.06e-8 |
| a/L needed to flip, uniform load | 0.9936 | 0.99357, i.e. a ≥ 19.87 mm |
| a/L needed to flip, tip point load | 0.991 | 0.99143 |
| taper exponent needed to flip, a = 300 µm | 3.994 | 3.9939 (3.9944 at 200 µm) |

I also checked the derivation of `φ = (a/L)^4`. By the unit-load method the tip deflection is
`∫ M(s)·s/EI ds` with `M = w s²/2`. Making `s < a` rigid removes `∫₀ᵃ s³ ds / ∫₀ᴸ s³ ds = (a/L)^4`
of it. The taper generalisation, `(a/L)^(4−n)` for `EI ∝ sⁿ`, is also correct.

**Every arithmetic value reproduces.**

## 2. Is a proxy standing in for the quantity that matters?

There are two candidates.

- **Caudal fin used for pectoral fin, and absolute `a` scaled onto an unrelated `L`.** The 200–300
  µm figure is for adult zebrafish *caudal* rays. S6 sizes a 2–4 cm design fin. The claim states the
  pectoral-fin value is `unknown`, and I found nothing either; I did not search for it. The question
  is whether the gap is large enough to matter. It is not. Actinotrichia would need to be 66–100×
  longer than measured just to reach the linear flip threshold. My elastica run in §3 shows a rigid
  3 mm segment, 10× the measured length, still changes nothing. The proxy is real, but it does not
  carry the result.
- **Linear small-deflection beam theory standing in for the real deflection.** S23, S23-D and the
  claim all use the linear `δ = wL⁴/(8EI)`. At the design points I checked, it predicts
  `δ/L = 19.6` (lenient) and `98` (central). Those values are physically impossible, because a tip
  cannot drop further than the span is long. So the linear model is the wrong quantity in this
  regime. §3 tests whether that matters.

## 3. Hidden assumptions, relaxed (computed)

**(a) Large deflection.** I solved the inextensible elastica for a cantilever under a uniform
gravity load, using tip shooting with bisection. I validated the solver against the linear result
at small load, where it matches to 0.01 %. Then I made the distal segment rigid.

| case | elastica δ/L, as is | δ/L, distal 300 µm rigid | δ/L, distal 3 mm rigid | tolerance | reduction still needed |
|---|---|---|---|---|---|
| lenient | 0.951 | 0.951 | 0.951 | 0.50 | 9.0 mm |
| central | 0.979 | 0.979 | 0.979 | 0.10 | 35 mm |

The reduction from stiffening the distal segment is below 1 nm. This is a calculation, not an
observation.
- **Interpretation (my inference):** under this load the outboard part of the fin already hangs
  almost straight and nearly vertical. It carries almost no curvature, so stiffening it changes
  nothing.
- The real regime therefore **strengthens** the claim's main conclusion.

**(b) The "n > 3.99 flips it" escape is an artefact of linear theory.**
- **Geometric bound (my derivation):** the tip cannot sit more than `a` from the point at `s = L − a`.
  Making the distal segment rigid can therefore lower the tip drop by at most about `2a`. Its own
  load, moved outboard, can only add proximal moment.
- So stiffening the actinotrichial zone meets tolerance only if the proximal `(L − a)` region,
  which is bony ray, already drops less than `tol·L + 2a`. At the lenient corner that is
  10 mm + 0.6 mm.
- A taper of `n ≥ 3.99` therefore does not rescue actinotrichial gain-of-function. It describes a
  fin whose **bone** already nearly meets S6, which is a different conclusion.
- The claim lists the taper as a condition that flips its result. It is better read as a
  condition on the bone. This **refines** the claim and makes its main conclusion stronger, not
  weaker.

**(c) Step taper: the distal zone is much softer than the ray.** In the linear model, a distal
segment with baseline `EI` lower than the ray's by a factor `R` flips the lenient corner only if
`R ≥ 7.6e8` at a = 300 µm. That means the tip segment's `EI` would have to be at most 6.6e-18 N·m².
- For scale, I computed one 2 µm elastoidin fibre at `E0` = 0.35 GPa: 2.7e-16 N·m², 40× stiffer
  than that threshold.
- Tanimoto et al. 2026 (`full-text`, re-read by me for this challenge via Europe PMC XML, keyword
  extraction) report that the actinotrichia are "arranged parallel to the inner surface of the bone"
  at the bone tip. That puts them inside the hemiray, not on a bone-free flap.
- Any `R` that large would also make the result fail the large-deflection bound in (b). The claim
  survives this relaxation.

**(d) The fin-fold clause is mis-specified (my inference; the direction is conservative).** The
claim says a full-span fin-fold design "remains governed by S23-D's unmeasured E0".
- S23-D's margin is `S/C = EI_req·E0 / (EI_meas·E_target)`. With `f = 1`, `EI_meas = E0·I_eff`, so
  this simplifies to `EI_req / (E_target·I_eff)`.
- `E0` enters only through backing an effective section `I_eff` out of the **adult bony-ray**
  `EI_meas`.
- For a fin fold, the right baseline is the actinotrichial section of a fin fold, `I_fold`, or a
  measured fin-fold `EI`. I did not search for either, so both are `unknown` to me.
- Tanimoto et al. 2026 state that "in adults, fin rigidity is provided by fin bones" (`full-text`).
  That supports `I_fold < EI_meas/E0`. If it holds, the fin-fold margin is **larger** than S23-D's
  1.37, so the residual is not as close to the edge as the claim implies.
- The governing unknown for that variant is the actinotrichial geometry (fibre count, packing,
  layer separation, coupling) together with `E_target`. It is not `E0` alone.

## 4. Is the evidence level honest?

`derived` is correct. The source labels the length `a` as measured. It does not present `φ` or
the margins as observations.

I re-read both length sources myself for this challenge. Read-level: `full-text`, Europe PMC XML,
keyword extraction.
- **Tanimoto et al. 2026**, *iScience*, PMC13573005. The text matches: "terminal ∼200 μm region of
  each fin bone".
- **Hanzelova et al. 2026**, *Development*, PMC13120675. The text matches: "200-300 μm at the tips
  of adult zebrafish caudal rays".
  - Hanzelova cite Nakagawa et al. 2022 for this figure. I did not read Nakagawa.
  - So the 300 µm end of the range is a secondary citation, as the claim says.
- **One nuance.** Tanimoto's ~200 µm is the extent of a *fluorescence signal* in wild-type fin-tip
  imaging. It is not a measured length of single fibres. The two sources measure slightly
  different things, and I keep both.

## 5. A regime, taxon or counter-example the author missed?

- **The `kcnk5b` gain-of-function long-fin mutant.** It enlarges actinotrichia (König 2018, as cited
  by the claim at `abstract`; I did not read it). It is the obvious route to a larger `a`.
  - The effect would have to reach `a/L > 0.99` in the linear model.
  - My elastica result says even that is not enough: stiffening material that already hangs
    straight does nothing.
- **Other taxa.** I did not search them. Larger teleosts or elasmobranchs, whose ceratotrichia are
  long, might have larger `a/L`. That would matter only for a fin built mainly from fibres, which is
  the fin-fold variant in §3(d), not the adult design.
- **Load case and metric.** The whole chain assumes S6's metric is root-to-tip deflection under
  self-weight. Suppose the real S6 requirement were *local* stiffness at the trailing edge, such as
  chordwise flexion of the fin margin during a flapping stroke. Then the distal zone would matter
  and the analysis would change. I did not read S6, so I can neither confirm nor rule this out.
  `depends_on` records it.

## Verdict

**SURVIVED.**
- All the arithmetic reproduces independently.
- The two key literature quotes check out at `full-text`.
- Each relaxation I tried leaves the adult conclusion standing or makes it stronger: large
  deflection, step taper, and a 10× longer actinotrichial zone.

Two of the claim's side clauses are overstated, both in the cautious direction:
1. The "n > 3.99" flip is an artefact of linear theory. It is a condition on the bone, not a route
   to an actinotrichial rescue.
2. The fin-fold variant depends on fin-fold actinotrichial geometry, not on `E0` alone, and its
   margin probably exceeds 1.37.

Neither weakens the headline.

```swarm-challenge
{"claim_id": 138, "outcome": "survived", "reason": "Arithmetic reproduces exactly (S=39.24/981, phi=1.0e-8 to 5.06e-8, flip a>=19.87 mm, n*=3.994), the 200-300 um sources check out at full-text, and relaxing to large-deflection elastica shows stiffening even a 3 mm distal segment changes tip drop by <1 nm, so the adult conclusion holds more strongly than claimed; only the n>3.99 escape (a linear-theory artefact) and the fin-fold 'governed by E0' clause are overstated, both conservatively.", "corrected_value": null,
  "depends_on": [
    "S23/S23-D: EI_req = (W/2) L^2 / (8 tol), m = 0.4 g, L = 2-4 cm, tol = 10-50% (S6 metric = root-to-tip deflection under self-weight; S6 not read by me)",
    "Puri et al. 2018 adult fin EI_meas = 4e-9 to 5e-9 N m^2 as carried by S23-D (not re-read by me)",
    "Tanimoto et al. 2026 (PMC13573005, full-text): adult actinotrichia restricted to terminal ~200 um of each fin bone, lying along inner bone surface",
    "Hanzelova et al. 2026 (PMC13120675, full-text) citing Nakagawa et al. 2022 (not read): adult caudal actinotrichia 200-300 um",
    "assumption: caudal-fin actinotrichial extent transfers to the pectoral design fin within ~10x",
    "challenge-138-calc.py elastica solution (computed): delta/L = 0.951 lenient, 0.979 central, unchanged by rigid distal 0.3 or 3 mm"
  ]}
```
