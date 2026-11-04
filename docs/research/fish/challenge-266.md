# Challenge 266: adversarial review of S26-D-D (the most sensitive input of S26-D)

**Claim under review** (written by someone else, harvested from `origin/claude/s26-d-sensitive-input-q4usu0`,
`docs/research/fish/S26-D-deepen.md` + `S26_DD_calc.py`, both read **full-text**):

> S26-D's conclusion stands as a conditional yes. Its most sensitive input is the passive EI of a 120 mm
> ray, which enters as diameter^4, so a 2x diameter error flips the result (relay margin 5.69 -> 0.36),
> while 2x errors in EI_req, EI_src or F_a do not. A measured wing-like labrid anchor (1.9-2.1e-7 N m^2 at
> ~18-20 mm), scaled the same way, reproduces a 1.4-2.7x passive shortfall that 12x clears. The yes still
> requires the real ray to be no more than ~35% thinner than isometry predicts (n >= 2.4 relay, >= 3.0
> labrid, >= 3.57 primary). Recorded evidence level: **measured**.

I measured nothing. Every number below is either *calculated* by me in
[`challenge_266_calc.py`](challenge_266_calc.py) (run with `python3 -I`) or *quoted* from a source, and each
one is labelled as such.

## 1. Arithmetic, redone independently

I wrote my own script from the stated inputs and did not reuse the author's code. All results are *calculated*.

| Quantity | Mine | Claim |
|---|---|---|
| EI_req, from 0.10 kg, 2 wings × 14 rays, uniform-load cantilever, δ/L = 0.10 | 6.31e-4 N m^2 | 6.3e-4 ✓ |
| Size factor (120/40.3)^4 | 78.6 | 78.6 ✓ |
| Relay path: need / margin | 2.11x / 5.69 | ✓ |
| Relay, diameter ÷2 (d^4) | 0.356 | 0.36 ✓ |
| Primary path: need / margin | 7.49x / 1.60 | ✓ |
| Break-even diameter ratio, relay / primary | 0.647 / 0.889 | ✓ |
| Break-even n, relay / primary | 2.41 / 3.57 | ✓ |
| Labrid high-AR break-even n (2.0e-7 N m^2, 19 mm) | 3.02 | ✓ |

**The core arithmetic reproduces.** I found no numerical error in the headline figures.

One sub-error, which runs in the conservative direction. The claim's ray length of "17.8–20.2 mm" mixes
phenotypes. I re-fetched Aiello et al. 2017 *PNAS* (PMC5410822; read-level **full-text**, fetched through a
summarising tool, with the threshold sentences returned verbatim). The high-AR pairs (1.05 mm / 5.91% and
1.5 mm / 8.20%) imply ray-3 lengths of **17.8–18.3 mm** (*calculated*). The 20.0–20.2 mm values come only
from the **low-AR** pairs. The author's script takes the min and max over all four pairs.

- With the high-AR fish's own lengths, the needed active factor is **1.44–1.79x** (*calculated*), not
  1.4–2.7x. The claim's upper bound is therefore pessimistic, and the conclusion is unaffected.
- With the low-AR fish's own lengths, it is **12.0–25x** (*calculated*). The 12x margin is ≤ 1.00 in every
  case, so the low-AR anchor fails outright rather than "mostly".

The quoted EI values (190 ± 30 to 210 ± 50, and 20 ± 10 to 40 ± 10, × 10^-9 N m^2) are confirmed verbatim.
The paper does not state absolute ray length. Deriving it from the paired thresholds is the author's inference,
and I agree that it is a reasonable one.

## 2. Proxy check

- **Diameter^4 as a proxy for the 120 mm ray's EI.** This assumes the cross-section is geometrically similar.
  A lepidotrich is a pair of hemicylindrical hemitrichs. If the bone wall thickness does not scale with outer
  diameter, then I ∝ d^3·t, not d^4. My inference is that this is plausible, and it is not measured.
  - Relaxed this way (*calculated*), a 2x diameter error costs 8x instead of 16x.
  - The relay margin becomes **0.71**, which still fails.
  - The break-even diameter ratio moves to 0.56 (relay) and 0.86 (primary).
  - The ranking "diameter is the most sensitive input" therefore survives this relaxation. The precise "35%
    thinner" tolerance does not: it depends on the section law, and is ~44% under d^3·t.
- **Mid-ray three-point bending as a proxy for the passive cantilever EI.** Aiello's test span is 20% of ray
  length, with deflection at 10% of span. The fetched text does not say how the ends or the hemitrichs were
  constrained. Treating it as the "passive / unlocked" state, comparable to Alben's one-free state, remains the
  author's **inference**, and the author labels it as one.
  - A short span with free ends also adds shear compliance. That pushes the measured EI down, which is
    conservative for the yes (my inference).
  - I could not show that the proxy is biased against the claim.

## 3. Hidden assumption, relaxed

**A. The "robust to 2x in EI_req, EI_src and F_a" statement is path-specific.**
- In the headline, "2x errors in EI_req, EI_src or F_a do not [flip the result]" is stated without
  qualification.
- It is true only on the relay path (margin 5.69).
- On the primary one-free path (margin 1.60), which the claim itself carries as a condition (n ≥ 3.57),
  **every one of those 2x errors flips the result, to margin 0.80** (*calculated*; the author's own §1 table
  shows the same).
- Likewise, "no more than ~35% thinner" is the relay tolerance. On the primary path the tolerance is
  **11%**. The body text states this, but the headline omits it.
- The sensitivity *ranking* (diameter > the rest) holds on both paths. The *robustness* claim does not.
- The relay value (3.8e-6, relaying Flammang 2013) versus the primary back-calculation (1.07e-6) is an
  unresolved source disagreement (D1). Which path is right is `unknown`, so the headline should not read as
  though the relay path were settled.

**B. F_a treated as size-invariant and multiplicative.**
- The 12x locking factor comes from one 40 mm bluegill ray, excised (Alben 2007, as quoted upstream; I did not
  re-read it).
- In an interconnected two-layer beam, the free-versus-clamped ratio depends on ray length relative to the
  shear-coupling length. So 12x need not transfer to 120 mm. This is my inference, from general composite-beam
  mechanics.
- What the requirement needs is the product F_a·EI_passive, which is the clamped (composite) EI, at 120 mm.
  Whether that product scales as L^4 is the same unmeasured exponent question.
- I therefore count this as part of the identified weak input, not as a new independent fault. I cannot
  quantify it: `unknown`.

## 4. Evidence level

**Defect.**
- The record lists the evidence level as **measured**.
- The claim's key number is a **calculation**: a measured labrid EI scaled by an *assumed* exponent n = 4 to
  an unmeasured 120 mm ray.
- The author's own swarm-result labels it "derived: calculation". The key_number string says "calculated".
- The only measured element is the source anchor (1.9–2.1e-7 N m^2 at roughly 18 mm, measured by Aiello et
  al.).
- The correct level is **calculated, resting on an assumption** (n = 4, or d ∝ L). Recording it as measured
  violates the rule even though the number is arithmetically right. The mislabel looks like a harvest/record
  error rather than the author's wording; that is my inference.

## 5. Missed regime, taxon or counter-example

I searched once (WebSearch, standard): "fin ray flexural stiffness scales with body size allometry
lepidotrichia ontogeny". Read-level **search-summary**. It found:

- a shortnose-gar SICB abstract, CT plus three-point bending, reporting that cross-sectional *shape* as well as
  size sets stiffness;
- a coho-salmon SICB abstract, reporting that some rays are "stiffer than their size alone would predict";
- a bluegill ontogeny abstract, on whole-body viscoelasticity, which is not about fin rays.

None of these gives a fin-ray EI–size exponent or any exocoetid ray dimension. Shape mattering independently
of size supports §2: the d^4 law is itself an assumption. These abstracts give no direction or magnitude, so
**they are not counter-examples**.

- **Scope of this negative:** one standard web query, plus the re-fetch of PMC5410822.
- **Not searched:** Google Scholar, Web of Science, MorphoSource, Dryad.

I also found no published flying-fish ray stiffness or diameter that contradicts n ≈ 4.

## 6. Verdict: WEAKENED

- **What survived:**
  - All headline arithmetic.
  - The identification of the 120 mm ray's cross-section, or equivalently the exponent n, as the most
    sensitive input. This holds on both paths and under a d^3·t section law.
  - The conditional, not-yet-shown character of the yes.
- **What did not survive:**
  1. The recorded evidence level "measured". It is calculated, on an assumed exponent.
  2. The unqualified statement that 2x errors in EI_req, EI_src or F_a do not flip the result. On the primary
     path, which the claim itself carries, each one flips it (margin 0.80).
  3. The single "~35% thinner" tolerance. It is relay-only; the primary path allows 11%. It is also tied to a
     d^4 section law and becomes ~44% (relay) / ~14% (primary) under d^3·t.
- **Minor correction, which helps the claim:** the high-AR labrid anchor needs 1.44–1.79x, not 1.4–2.7x.

This is a weakening of the claim's statement and labelling, not a refutation of its conclusion. The yes stays
conditional on an unmeasured exponent, exactly as the author says in the body text.

```swarm-challenge
{"claim_id": 266, "outcome": "weakened", "reason": "Arithmetic and the diameter-is-most-sensitive ranking reproduce, but the result is a calculation on an assumed n=4 recorded as 'measured', and the headline's robustness to 2x errors in EI_req/EI_src/F_a and its ~35% thinness tolerance hold only on the relay path (primary path: each 2x error gives margin 0.80, tolerance 11%).", "corrected_value": "evidence level: calculated (assumption n=4); primary-path margin under 2x EI_req/EI_src/F_a error 0.80 (fail); diameter tolerance 35% relay / 11% primary (d^4), ~44% / ~14% (d^3 t); labrid high-AR need 1.44-1.79x (ray 3 = 17.8-18.3 mm)", "depends_on": ["S26-D-D: docs/research/fish/S26-D-deepen.md and S26_DD_calc.py on origin/claude/s26-d-sensitive-input-q4usu0", "S6-D EI_req 6.3e-4 N m^2 per ray (m=0.10 kg, 2 wings x 14 rays, L=0.12 m, uniform load, delta/L<=0.10)", "Puri et al. 2018 relay bluegill EI 3.8e-6 N m^2 (citing Flammang 2013), as quoted upstream", "S26-D back-calculated bluegill one-free EI 1.07e-6 N m^2, as quoted upstream", "Alben et al. 2007: 12x locking factor and 40.3 mm ray length, as quoted upstream (not re-read)", "Aiello et al. 2017 PNAS PMC5410822: EI at 50% length 190-210e-9 (high-AR), 20-40e-9 (low-AR) N m^2 and paired %/mm thresholds (full-text via fetch)", "inference: ray-3 length from paired thresholds, high-AR 17.8-18.3 mm", "assumption: EI ~ d^4 (geometric section similarity); relaxed alternative EI ~ d^3 t", "negative search: one standard WebSearch on fin-ray stiffness allometry, no exponent or exocoetid ray data found"]}
```
