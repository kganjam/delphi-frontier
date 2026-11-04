# Challenge 209: does the 5.7x margin rest on where Alben 2007 measured 1.98 N/m?

**Claim under review (not written by me):**

> "OPEN DEPENDENCY: a challenge reports Alben 2007 places the 1.98 N/m stiffness at ~2/3 of ray length and in
> the BASE-CLAMPED state, not at the tip. The S26 scale correction and its 12x hemitrich-locking factor rest on
> that boundary condition, so the 5.7x margin needs rechecking."

Recorded evidence level: `unknown`. Source: challenge evidence, not yet verified.

**Verdict: WEAKENED.** The factual premise is mostly right, with one exception. The *mechanism* the claim gives
for why the margin needs rechecking is wrong. The 5.7x margin does not use the 1.98 N/m value or its load point
at all. The margin does need rechecking, but for a different reason: the boundary condition of the *baseline*
EI that the 12x multiplies. Prior work already did that recheck and got 1.6x to 2.8x. I reproduced it.

Every number below is tagged *measured* (by the cited authors), *calculated* (by me, `python3 -I`, inline
arithmetic shown) or *assumption*. I measured nothing.

## 1. Primary source, read by me

Alben, Madden & Lauder 2007, *J R Soc Interface* 4(13):243–256, doi:10.1098/rsif.2006.0181, PMC2359861.
**Read-level: full-text.** I got the publisher HTML on PMC with curl (HTTP 200, 213,488 bytes, sha256
`c930e59d…5e2f`), stripped the tags with `python3 -I` (70,550 characters) and searched it for keywords. The HTML
has no page numbers, so I cite by section and figure. Verbatim:

- Fig. 7a caption: "The ray is clamped horizontally at the base, and a vertical point force is applied at
  two-thirds of the distance from the ray base to the tip … In the latter case [both bases clamped], the
  force–displacement curve may be fit with a slope of 1.98 N m−1, about 12 times the value when one hemitrich
  is free." (measured)
- §5.2 text: "a probe pushes down on the fin ray at approximately two-thirds of the distance from the base to
  the tip, and the force on the probe is measured as a function of **tip deflection** of the ray."
- §5.2 text: clamped/free ratio "a factor of 4 (for G = 3) to 100 (for G > 10^5). In the experiment, the factor
  is 12, which occurs when G ≈ 100 in the model". The 4 to 100 range is the authors' model calculation. The 12
  is measured.
- §2: "Six fishes … maximum ray length = 40.3 ± 0.8 mm". The length of the ray tested in Fig. 7 is **not
  stated**. Fig. 7 says "as in figure 6a", and Fig. 6a shows ray 4. No n and no spread are given for the 12x.

**How the claim's premise checks out:**

- "~2/3 of ray length": **confirmed**. This applies to the *load point*.
- "BASE-CLAMPED state": **confirmed**. 1.98 N/m is the state with both hemitrich bases clamped.
- "not at the tip": **only half right.** The load is not at the tip. But §5.2 says the deflection is read *at
  the tip*. The caption says only "deflection of the ray". So 1.98 N/m is force at 2/3 L divided by either
  tip deflection or load-point deflection. The paper is ambiguous here, and the claim drops that ambiguity.

The premise is also **not new**. The S26-D document
(`origin/claude/deepen-s26-active-stiffening-48xj8q:docs/research/fish/S26-deepen.md`, read in full) already
states "load at 2/3 of ray length" and "both bases clamped". Its own back-calculation uses a = (2/3)L and the
clamped state. S26-organ.md M1 and its caveats say the same (read in full).

## 2. Independent arithmetic: what the 5.7x is made of

I recomputed the margin from S26-D's stated inputs (calculated):

- λ⁴ = (120 / 40.3)⁴ = 2.9777⁴ = **78.61**
- Passive EI at 120 mm = 3.8e-6 × 78.61 = **2.99e-4 N m²**
- Active factor needed = 6.3e-4 / 2.99e-4 = **2.109**
- Margin = 12 / 2.109 = **5.69 ≈ 5.7x**. This reproduces.

Inputs that enter: 12 (the ratio), 3.8e-6 N m² (the Puri 2018 relay of Flammang 2013), 6.3e-4 N m² (S6-D), and
40.3 mm and 120 mm. **The value 1.98 N/m does not enter, and neither does its load point or deflection point.**

The 12x is a ratio of two stiffnesses taken at the same load and readout point on the same ray. For a uniform
Euler–Bernoulli cantilever, the point-convention factor (a³/3, or a²(3L − a)/6) cancels in such a ratio. So the
convention question cannot move the 12x. The 12x is *defined* by the clamped-vs-one-free comparison, so it
"resting on that boundary condition" is definitional, not a hidden dependency.

**So the claim's stated chain (load point and clamped state → scale correction and 12x → 5.7x) is broken at the
second link.** That is my inference from the arithmetic above.

## 3. The dependency that is real: the baseline's boundary condition

A 12x clamped/one-free ratio can only multiply a **one-base-free** (unlocked) baseline. 3.8e-6 N m² is a relay
whose base condition is `unknown`. Flammang 2013 full text is could-not-access, as reported upstream. The
location of 1.98 N/m *does* matter when Alben's own measurement is used to supply a self-consistent baseline. I
back-calculated it, assuming a uniform cantilever and L = 40.3 mm (*assumption*: the Fig. 7 ray's length is not
reported) (calculated):

| Reading of the 1.98 N/m | EI formula | EI clamped (N m²) | EI one-free = /12 | Locked EI at 120 mm (×78.61) | Margin vs 6.3e-4 |
|---|---|---|---|---|---|
| Deflection read at the 2/3 L load point (caption-neutral) | k·a³/3 | 1.28e-5 | 1.07e-6 | 1.01e-3 | **1.60x** |
| Deflection read at the tip, load at 2/3 L (§5.2 text) | k·a²(3L − a)/6 = k·28L³/162 | 2.24e-5 | 1.87e-6 | 1.76e-3 | **2.80x** |
| *Misreading:* load at the tip (what the claim warns against) | k·L³/3 | 4.32e-5 | 3.60e-6 | 3.40e-3 | 5.39x |
| S26-D as published (relay baseline × 12) | n/a | n/a | 3.8e-6 (taken as the unlocked value) | 3.59e-3 | **5.69x** |

Readings:

- Taking the relay as the unlocked baseline gives 12 × 3.8e-6 = 4.56e-5. That is **2.0x to 3.6x above Alben's own
  measured clamped state** (calculated). So 5.7x only holds if the relay ray is 2 to 3.6 times stiffer than
  Alben's unlocked ray.
- The point the claim cares about, the load point vs the tip, moves the Alben-consistent margin by a factor of
  only **1.75x** (1.60x vs 2.80x). The "load at the tip" misreading the claim warns against would *inflate* EI,
  not deflate it. Neither upstream document made that misreading. The adverse case is the load-point reading,
  1.6x, and it still passes at nominal EI_req.
- A coincidence worth flagging: the tip-load misreading gives 5.39x, close to the published 5.7x. **I found no
  sign that S26-D's 5.7x came from that misreading.** Its script inputs are the relay and λ⁴ (§2).
- Shorter tested ray: EI_back ∝ L³ and λ⁴ ∝ L⁻⁴, so the locked EI at 120 mm ∝ 1/L. Taking L = 40.3 mm (the
  group maximum) is the *conservative* choice for the margin (calculated).

This recheck is **not new**. challenge-92
(`origin/claude/challenge-s26-active-stiffening-acr1ha`, outcome "weakened", margin 5.7x → 1.6x) and replicate-96
(`origin/claude/hemitrich-locking-factor-dw1j0h`, margin 1.6x to 5.7x, baseline-consistent 1.6x to 2.8x)
already reached it. Both were read in full by me (grep of key lines plus the swarm blocks). My table reproduces
their 1.28e-5, 2.24e-5, 1.6x and 2.8x **independently** from the primary text and the formulas above.

## 4. Proxy, hidden assumption and regime checks

- **Proxy.** A point-load stiffness ratio at 2/3 L stands in for an EI multiplier under a distributed glide
  load on a 120 mm ray. In the authors' bilaminar model the clamped/free ratio depends on G (4 to 100) and on
  the tip condition (fused or free). It is not a fixed EI multiplier, and its value under a distributed load
  is `unknown` (not reported in the paper). This proxy problem is real. It is a *different* defect from the one
  the claim names, and S26-D already flags its version of it ("excised-ray clamping factor is achievable … in
  vivo").
- **Hidden assumption.** Isometric L⁴ scaling carries every margin in the table. Challenge-92 reports that
  whole-fish isometry (EI_req ~ L⁵) needs 6.3x to ~22x. I did not re-derive that, and it is outside this
  claim's scope.
- **Counter-example in the baseline.** Flammang 2013 (abstract, upstream read) gives 565e-6 N m². Under that
  baseline the passive ray already passes and the 12x is not needed. The 565e-6 vs 3.8e-6 disagreement stays
  unresolved, and I do not average it away.
- **n = 1.** No n and no spread are reported for the 12x (full-text). Halving it to 6x on the load-point path
  needs 7.5x, so it **fails** (calculated: 6.3e-4 / (1.07e-6 × 78.61) = 7.49).
- **Negative-search scope.** I searched only the Alben 2007 HTML, plus `git grep` over this repo's remote
  branches under `docs/research/fish` and `docs/dossier`. I did not search for other clamped/free hemitrich
  ratios.

## 5. Evidence-level audit

The claim's recorded level, `unknown`, is honest for an unverified relay. Its factual premise can now be
upgraded to **full-text-verified**, with the tip-deflection caveat. Its inference ("rest on that boundary
condition") is a **calculation-level** claim, and the arithmetic in §2 shows it is wrong as stated.

## 6. Bottom line

- **True:** Alben 2007 applies the load at about 2/3 L in the base-clamped state.
- **False:** the claim that the S26 scale correction and its 5.7x rest on that. 1.98 N/m does not enter the
  5.7x arithmetic, and the 12x ratio is invariant to the point convention.
- **Still true, for another reason:** the 5.7x does need rechecking, because of the *unknown base state of the
  3.8e-6 baseline*. With Alben's own unlocked state as the baseline, the margin is **1.6x to 2.8x
  (calculated)**. The spread is set by the load-point vs tip-deflection reading. It still passes at nominal
  EI_req, under isometric L⁴ scaling and in-vivo locking.

```swarm-challenge
{"claim_id": 209, "outcome": "weakened", "reason": "Alben 2007 full text confirms the 1.98 N/m is base-clamped with the load at ~2/3 L (but §5.2 says deflection was read at the tip), yet the 5.7x margin does not use 1.98 N/m or its load point and the 12x ratio is convention-invariant; the real recheck is the unknown base state of the 3.8e-6 baseline, which with Alben's own unlocked state gives a margin of 1.6x (load-point reading) to 2.8x (tip-deflection reading), calculated.", "corrected_value": "margin of 12x locking over required factor: 1.6x to 2.8x (calculated, Alben-consistent baseline, isometric L^4, L_src = 40.3 mm); 5.7x only if 3.8e-6 N m^2 is an unlocked-state EI", "depends_on": ["Alben, Madden & Lauder 2007 J R Soc Interface 4:243 (PMC2359861, full-text read by me): 1.98 N/m both-bases-clamped, ~12x vs one hemitrich free, point force at ~2/3 L, force vs tip deflection per §5.2", "Alben 2007: max pectoral ray length 40.3 +/- 0.8 mm; Fig. 7 ray length not stated", "assumption: tested ray length 40.3 mm for EI back-calculation", "assumption: uniform Euler-Bernoulli cantilever to convert 1.98 N/m to EI", "S26-D (S26-deepen.md on origin/claude/deepen-s26-active-stiffening-48xj8q): 5.7x = 12 / (6.3e-4 / (3.8e-6 x (120/40.3)^4))", "S6-D EI_req 6.3e-4 N m^2 per ray (assumption-driven, as relayed by S26-D)", "Puri 2018 relay of Flammang 2013: bluegill ray EI 3.8e-6 N m^2, base condition unknown", "assumption: isometric L^4 scaling from 40.3 mm to 120 mm", "assumption: the 12x ratio transfers unchanged to a scaled ray under distributed load", "Flammang 2013 abstract 565e-6 N m^2 (unresolved disagreement with the relay)"]}
```
