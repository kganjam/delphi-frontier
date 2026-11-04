# Challenge 128: adversarial review of S23-D-D (the caudal→pectoral ratio `R`)

**Claim under review** (source `harvest:s23-sensitive-input-melodp`; document
`docs/research/fish/S23-D-deepen.md` and `S23-D-D-calc.py` on branch
`claude/s23-sensitive-input-melodp`, both read at `full-text` for this review):

> S23-D's weakest input is not E0 but EI_meas, a measurement of the zebrafish CAUDAL fin standing
> in for the PECTORAL glide wing via an undeclared ratio R that both ancestors silently set to 1.
> The computed flip threshold is R* = 1.35 at the lenient corner. Improving R to an upper bound
> R ≤ 1 (yellow perch: pectoral rays least stiff, caudal intermediate, abstract-level) leaves the
> parent's margins as lower bounds and the conclusion intact but numerically unimproved at 1.353.
> Verdict: stands. Recorded evidence: derived.

Date: 2026-11-04. Reproduction: `python3 docs/research/fish/challenge-128-calc.py`.
**Every number in this document is a computation, not an observation**, except where I name a
paper in the same sentence. I did not open the yellow perch, labrid or Puri papers myself. Where
I use them, I am relying on what the author reported about them, and I say so.

---

## 1. Independent arithmetic (computed)

I rebuilt it from the stated inputs: `m` = 0.4 g, `g` = 9.81, two wings, uniform-load cantilever,
`EI_req = (W/2)L²/(8·tol)`, `E0` = 0.35 GPa, `E_target` = 5 / 10 GPa.

| corner | `EI_req` (N·m²) | `S` | `C` exact | margin = `R*` (exact `C`) | `C` rounded | `R*` (rounded, as claimed) |
|---|---|---|---|---|---|---|
| central 4 cm, 10 %, 4×10⁻⁹ | 3.924×10⁻⁶ | 981.0 | 14.29 | 68.7 | 14 | 70.1 |
| central | | | 28.57 | 34.3 | 29 | 33.8 |
| lenient 2 cm, 50 %, 5×10⁻⁹ | 1.962×10⁻⁷ | 39.24 | 14.29 | 2.75 | 14 | 2.80 |
| lenient | | | 28.57 | **1.373** | 29 | **1.353** |

- All four claimed thresholds reproduce once `C` is rounded the way the author rounded it. The
  identity `R* = margin(R=1)` is correct, because `R` enters `S` as a single divisor.
- Rounding `C` = 28.57 up to 29 makes the headline 1.353 slightly *conservative* (exact: 1.373).
  Rounding `C` = 14.29 down to 14 makes the dry-collagen thresholds slightly *non-conservative*
  (2.80 vs 2.75, 70.1 vs 68.7). Both errors are about 2 % and no verdict changes. This is a
  cosmetic defect.
- Direction check: `R ≤ 1` means pectoral EI ≤ caudal EI. That raises `S = EI_req/(R·EI_caudal)`,
  so the parent margins really do become lower bounds. The logic is right.
- Line C check: `(0.4/22.44)^(4/3)` = 4.656×10⁻³, and the band 0.65–38.7 reproduces. That band
  pairs the lowest scaled pectoral value with the highest caudal value, and the reverse, which
  makes it as wide as possible, and the author presents it that way.

**I found no arithmetic error that changes the result.**

## 2. Is the "tighter than any other input" framing right? Partly false (computed)

The claim's "a 35 percent error kills the conclusion" is true, but it is not special to `R`.
The author's own §1.1 notes that every multiplicative input has the same elasticity. At the
lenient corner, an error of 1.353× in **any** of `m`, `tol`, `E0`, `E_target` or `EI_caudal` also
flips the conclusion. And `L` enters squared, so its tolerance is **tighter** than `R`'s:
`L* = 2 cm / √1.353 = 1.72 cm`, a 14 % change (computed). So the document body's sentence that
`R`'s 35 % tolerance is "tighter than any other input in the chain enjoys" is **false as
written**.

What survives is the author's real tie-break: `R` is the least *established* input. It is the
only one carried as a measurement that is not a measurement of the organ in question, while `L`
and `tol` are design choices that are declared soft. I accept that tie-break. The "weakest input"
label stands on provenance, not on numerical tightness.

## 3. Hidden assumption, relaxed: the shape of the load (computed)

The 1.353 margin also depends on the **uniform** spanwise lift load. The author declares this in
`depends_on`, but nowhere tests it. A glide wing near its best is closer to an elliptic load,
which puts the load centroid inboard (4L/3π ≈ 0.42 L against 0.50 L). I integrated tip deflection
numerically at equal total lift and uniform EI:

- uniform coefficient: 0.1250 (the textbook 1/8, a check on the integrator)
- elliptic coefficient: 0.0967, a ratio of **0.774**

So under elliptic loading `EI_req` falls by 23 % and the lenient-corner margin falls from
1.353 to **1.047** (1.063 with exact `C`) (computed). **It still holds**, but the surviving
tolerance on `R` drops from 35 % to about 5 %. Other relaxations push the other way. A gust or
manoeuvre load factor above 1 raises `EI_req`. Rays that taper distally lower EI outboard, which
raises the required root EI for a given tip deflection. I did not quantify either, so their net
effect is `unknown`.

This does not break the claim, because `R ≤ 1` still keeps every margin ≥ its `R = 1` value. It
does mean that "the conclusion intact … at 1.353" rests on the load-model choice nearly as much
as on `R`.

## 4. Proxy check: is `R` the right ratio?

*My inference, not the author's.* `R` is defined between the **existing** pectoral and caudal
fins. The design corners, though, have a 2–4 cm semi-span. The author's own §2 records zebrafish
pectoral ray length as `unknown`, so it is not shown that the existing pectoral fin is anywhere
near that span. The quantity the conclusion actually needs is the root-section EI of whatever
structure would *be* a 2–4 cm wing before protein-level stiffening. An existing-fin ratio, even a
measured one, is still a proxy for that. This defect comes from S23 and S6 (fixed geometry
together with a design span). S23-D-D did not introduce it, so I do not count it against this
claim. It does mean `R ≤ 1`, even if confirmed, would not close the proxy chain.

There is also a ray-level to whole-fin step. The perch ranking compares individual rays (author's
report of the abstract). Whole-fin EI is the sum over rays, by Puri et al. 2018 as relayed by the
author. So `R_whole ≤ 1` also needs the zebrafish pectoral ray count to be ≤ the caudal count.
The author asserts that the caudal fin has the "larger complement" but gives no caudal count. I
did not verify a zebrafish caudal principal-ray count in this review, so that leg is `unverified`.
If it holds, it pushes `R` further below 1, in the safe direction.

## 5. Counter-examples and other regimes

- *Taxon:* the author's own Line C (Labridae, read at `full-text` by the author) shows pectoral
  rays can be stiff spars in species that use the pectoral fin for propulsion. The perch ranking
  (`abstract`, full text HTTP 403) therefore may not hold across ecologies. Zebrafish (a
  cypriniform that swims with its body and caudal fin) is closer to the perch case than to the
  labrid case. That is an inference, and I did not test it against a measurement.
- *Disagreement preserved:* Flammang et al. 2013 (`search-summary` via the author) says pectoral
  ≈ caudal stiffness. That would put `R` ≈ 1, which is still ≤ 1.35 at the lenient corner, so even
  that line does not flip the conclusion. The conclusion flips only if `R` > 1.35, and the only
  evidence for that is the upper end of Line C, which the author argues against without a
  measurement.
- *Negative search scope:* I ran no new literature search for this review. I relied on the
  author's recorded sources and read-levels. I found no published zebrafish pectoral-fin EI, and
  that statement covers only my reading of the author's search record, not a fresh search.

## 6. Evidence level

`derived` is honest. The document marks `R ≤ 1` as a bound, not a value. It says the bound rests
on an `abstract`-level read with an unverified author list. It reports the one numeric line (Line
C) that cuts against it, and it labels its computations as computations. I found no derived
number presented as measured.

## 7. Verdict: SURVIVED

I could not break the central claim:

- The arithmetic reproduces (within the ~2 % rounding of `C`).
- The direction of `R ≤ 1` is correct.
- The conclusion holds at every stated corner for every `R ≤ 1.35`. That includes Line B's `R ≈ 1`,
  and it also holds when I relax the load to elliptic (margin 1.047).

These defects remain, and none of them changes the verdict:

- The "tighter than any other input" sentence is false, because `L` has a 14 % tolerance.
- Under elliptic loading the lenient-corner tolerance on `R` shrinks to about 5 %.
- The ray-to-whole-fin step depends on a caudal ray count that is not given.
- `R` itself is a proxy for an undefined design-span root EI, a problem inherited from S23 and S6.

```swarm-challenge
{"claim_id": 128, "outcome": "survived", "reason": "Independent recomputation reproduces R* = 1.35/2.80/33.8/70.1 (with C rounded to 29/14; exact C gives 1.373/2.75/34.3/68.7) and R <= 1 correctly turns every margin into a lower bound, so the stands verdict holds, though the body's claim that R's 35% tolerance is tighter than any other input is false (L tolerates only 14%) and an elliptic rather than uniform load cuts the lenient margin to 1.047 (computed).",
  "corrected_value": null,
  "depends_on": ["EI_req = (W/2)L^2/(8*tol) uniform-load cantilever, m = 0.4 g, two wings (S23 design assumptions)",
                 "Lenient corner L = 2 cm, tol = 50 %, EI_caudal = 5e-9 N*m^2; central L = 4 cm, tol = 10 %, EI_caudal = 4e-9 N*m^2",
                 "EI_caudal measured in vivo, Puri et al. 2018 J Exp Biol 221:jeb171777, as relayed by the author (not re-read here)",
                 "E0 >= 0.35 GPa and E_target = 5 / 10 GPa, giving C = 14.29 / 28.57 (rounded 14 / 29), inherited from S23-D",
                 "R = EI_pectoral/EI_caudal <= 1, from the yellow perch ray ranking, J Morphol doi:10.1002/jmor.20831, abstract-level via the author, full text could-not-access",
                 "Zebrafish pectoral ray count <= caudal principal ray count (needed for ray-level to whole-fin transfer; unverified here)",
                 "Elliptic-load relaxation: tip-deflection coefficient 0.0967 vs 0.125 (computed here, uniform EI)"]}
```
