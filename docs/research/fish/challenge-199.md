# Challenge 199 — zebrafish fin rigidity vs. a gliding fin-wing ([S6])

**Claim under review (the author's, not mine):** At the zebrafish fin rigidity measured in vivo
(EI 1.5–4e-9 N m² across a 5–8 mm width, so 1.9–8.0e-7 N m per unit width), a cantilevered
lepidotrichial fin-wing that carries 1 g of gliding lift for a 0.4 g fish deflects 0.9–20 × its span.
That is 9–196 × short of the rigidity needed to keep tip deflection ≤ 10 % of span, at any wing size
from 3 to 15 mm. KEY: required D_w ≥ 7.4e-6 N m against measured ≤ 8.0e-7 N m, a ratio of ≥ 9 × for a
3 mm square wing. The claim's evidence level is "derived".

**Verdict: WEAKENED.** The conclusion ("No") survives every relaxation I tried. Two parts of how it
is presented do not: the KEY margin ("≥ 9 ×") is not a lower bound, and "deflects 20 × its span" is
not something a beam can physically do.

## Sources and read-levels

- Puri S. et al. 2018, *J. Exp. Biol.* 221: jeb171777, "In vivo quantification of mechanical
  properties of caudal fins in adult zebrafish" (PMC5868929). **Read-level: search-summary.** I did not
  open the full text. The summary I saw gives these points:
  - bending stiffness of 1.5–4 × 10⁻⁹ N m² along the proximal–distal axis;
  - the stiffness varies non-monotonically along that axis;
  - cutting the inter-ray tissue did not significantly change overall bending stiffness.
- The claim cites only `harvest:s6-fin-ray-load-kqweu7`. I could not find that harvest anywhere in
  this repository (searched the whole working tree for "fin-ray" and "lepidotrich"; no hits).
  Read-level: **could-not-access**.

The EI input appears in Puri et al. 2018 at search-summary level. "In vivo" and "measured" fairly
describe that paper's number. Two points I could not check without the full text:
- whether the 1.5–4e-9 value is for the whole fin or for a strip of it;
- whether 5–8 mm is the right width to divide it by.

Both are `unknown` from what I read.

## 1. Arithmetic, redone independently

Inputs: fish mass 0.4 g, so W = 0.4e-3 × 9.81 = 3.92e-3 N. "1 g lift" is read as lift equal to
weight. The claimed numbers only come out if the lift is split over **two** wings, so F = 1.96e-3 N
per wing.

**Per-width rigidity:**
- 1.5e-9 / 8e-3 = 1.875e-7 N m
- 4e-9 / 5e-3 = 8.0e-7 N m

This matches the claim.

**Model:** a cantilever plate of span L and chord c under uniform pressure has tip deflection
δ = F L³ / (8 c D_w). For a square wing (c = L), δ/L = F L / (8 D_w). Requiring δ/L ≤ 0.1 gives
D_w ≥ F L / 0.8.

| L (mm) | D_w (N m) | δ/L, linear | D_w required (N m) | required/measured |
|---|---|---|---|---|
| 3  | 8.0e-7   | 0.92 | 7.36e-6 | 9.2 |
| 3  | 1.875e-7 | 3.92 | 7.36e-6 | 39 |
| 15 | 8.0e-7   | 4.6  | 3.68e-5 | 46 |
| 15 | 1.875e-7 | 19.6 | 3.68e-5 | 196 |

These are calculated values, not observations. All of the claim's numbers reproduce: 0.9–20 × span,
9–196 ×, and 7.4e-6 N m.

## 2. Proxy problems

- **"Deflects 20 × its span" is linear small-deflection output used far outside where it is valid.**
  A real cantilever cannot deflect its tip more than its own length. δ/L_linear ≈ 1–20 means "the
  wing folds up to near-vertical", not a literal displacement. The usable quantity is the rigidity
  ratio, which is linear in load and is the claim's own KEY. The deflection range should be reported
  as a linear-theory index, not as a physical deflection. (This is my inference.)
- **Caudal fin standing in for a pectoral fin-wing.** Puri et al. measured the **caudal** fin. A
  gliding fin-wing would be a pectoral (or pelvic) fin. I have no measured EI for zebrafish pectoral
  fins: `unknown` (I searched only the one query above). Pectoral rays are probably smaller and
  therefore more flexible, which would push the result further in the claim's direction, but that is
  my unverified inference.
- **The ≤ 10 % tip-deflection criterion is a stand-in for "aerodynamically functional".** Flexible
  wings (insects, bats) work with sizeable deflection. Even so, at δ/L_linear ≈ 0.9 the linear root
  slope is about 1.2 rad (~70°), which is not a usable lifting surface. A looser criterion of 30 %
  would cut every ratio by 3 ×, giving a floor of about 3 × at 3 mm. The verdict still holds.

## 3. Hidden assumptions, tested with each one relaxed

I computed load-shape coefficients numerically (δ = k F L³/EI):

| Load shape | k | Relative to uniform |
|---|---|---|
| uniform | 1/8 | 1.00 |
| elliptic span loading | 0.0967 | 0.77 |
| triangular, root-heavy | 1/15 | 0.53 |

| Relaxation | Factor | 3 mm, stiffest-measured ratio |
|---|---|---|
| none (claim) | — | 9.2 |
| elliptic lift distribution | × 0.77 | 7.1 |
| triangular, root-loaded | × 0.53 | 4.9 |
| four wings (pectoral + pelvic, as in four-winged flying fish) instead of two | × 0.5 | 4.6 |
| four wings + triangular load | × 0.27 | **2.5** |
| four wings + triangular load + 30 % deflection criterion | × 0.09 | **0.8** |

All ratios in this table are calculated. The **"≥ 9 ×" in the KEY is therefore not a floor.** It
depends on uniform loading and a two-wing load split, and neither is stated in the KEY. With
plausible favourable relaxations the margin shrinks to about 2.5 ×. It reaches parity only when the
deflection criterion is also loosened to 30 %.

An assumption that cuts the other way, which the author also did not use:

- **The small-wing end of the range is aerodynamically impossible.** Glide speed at C_L = 1 and
  ρ = 1.2 kg/m³:
  - two 3 mm square wings: v = √(2W / (ρ S C_L)) ≈ **19 m/s**;
  - two 15 mm square wings: ≈ 3.8 m/s.
- At a launch speed of 1–2 m/s (I assume this for a fish this size; I did not look up a measured
  zebrafish exit speed), each wing must be about **29–57 mm** square.
- Required rigidity scales with L for a square wing. At 29 mm the ratio rises to ≈ 89–380 ×
  (uniform load, two wings). That is about 24–100 × with every favourable relaxation above except
  the 30 % criterion.
- So the wings that could actually glide sit far outside the claimed 3–15 mm range, and they make
  the negative result **stronger**. The 3 mm best case flatters feasibility, and every other
  relaxation pushes the ratio up from there.

The "cantilevered" assumption also favours feasibility. Lepidotrichia articulate on radials at the
fin base rather than being rigidly clamped, so a real root adds compliance.

## 4. Evidence level

"Derived" is honest. The EI input is a measured value (Puri et al. 2018, search-summary read). The
deflections and ratios are calculations. One problem: the attribution clause — "bone material is
stiff enough, the decoupled bilaminar architecture is not" — is **not derived from any input in the
claim**. No bone modulus, ray cross-section or hemitrich coupling figure appears in the working. The
claim does flag it as "(inference)", which is correct. But an equally available explanation is
cross-section scale (I ∝ thickness³), and the numbers here cannot tell the two apart. The inter-ray
result in Puri et al. (cutting soft tissue between rays changes nothing) fits rays bending
independently of each other. That is a different thing from hemitrichia being decoupled *within* a
ray. I did not read anything that tests within-ray hemitrich coupling in zebrafish: `unknown`.

## 5. Counter-examples and regimes

Flying fishes (Exocoetidae) do glide on lepidotrichial pectoral fins. They are 10²–10³ × heavier,
with much thicker rays and larger fins. I did not search for measured exocoetid fin-ray EI, so I can
give no number. Their existence shows that the architecture is not incompatible with gliding at a
larger scale. It does not contradict the claim, which is about zebrafish-measured rigidity. Scope of
my negative search: one web query on zebrafish fin rigidity; nothing on exocoetid ray mechanics.

## Summary

- **What survives:** the zebrafish-measured fin rigidity cannot support a gliding fin-wing. This
  holds across every load model and wing count I tried, and becomes overwhelming once the wing is
  sized to glide at speeds a fish this size can plausibly reach.
- **What is weakened:**
  1. The KEY margin "≥ 9 ×" depends on unstated choices (uniform load, two wings). The defensible
     floor is about 2.5 × at the 3 mm, stiffest-measured, most-favourable corner. At realistic
     glide-capable sizes the ratio rises to tens to hundreds.
  2. "Deflects 0.9–20 × its span" is a linear-theory index, not a physical deflection.
  3. The material-versus-architecture attribution is not supported by the claim's inputs.

```swarm-challenge
{"claim_id": 199, "outcome": "weakened", "reason": "The 'No' survives every relaxation tried, but the KEY '>=9x' margin depends on unstated uniform-load and two-wing assumptions (four wings plus root-loaded lift gives ~2.5x at the 3 mm corner), the '0.9-20x span' deflections are linear-theory indices that no real beam can reach, and the bone-vs-architecture attribution has no supporting input.", "corrected_value": "required/measured flexural rigidity >= ~2.5x (3 mm square wing, 4 wings, triangular load, D_w 8.0e-7 N m); ~89-380x for glide-capable ~29 mm wings at 2 m/s (uniform load, 2 wings)", "depends_on": ["Puri et al. 2018 JEB jeb171777 caudal-fin EI 1.5-4e-9 N m^2 (search-summary read)", "width 5-8 mm used to convert EI to per-width rigidity (from claim, unverified)", "fish mass 0.4 g (from claim)", "linear Euler-Bernoulli cantilever plate model", "tip-deflection criterion 10% span (from claim)", "launch/glide speed 1-2 m/s (my assumption, not measured)"]}
```
