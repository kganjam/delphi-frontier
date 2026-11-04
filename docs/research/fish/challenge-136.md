# Challenge 136: adversarial review of claim [S6-D-D], the passive-ray verdict with a size transfer

Date: 2026-11-04. Reviewer: an independent pass that did not write the claim.
**No experiment was run and nothing was measured here.** Every number below is tagged:
*quoted* (from a source, with its read-level), *calculated* (by this reviewer, independently, see §1),
or *inference* (this reviewer's reasoning, not any author's claim).

Claim under review: branch `claude/deepen-s6-d-sensitive-input-t6ch0y`, file `docs/research/fish/S6-D-deepen.md`
plus `s6_d_deepen_calc.py`. Read-level: full-text (repository). Recorded evidence level: **measured**.

**Outcome: WEAKENED.** The physics and the arithmetic survive. The direction ("a passive, bluegill-proportioned
ray falls short, by a few-fold, not 166×") survives every relaxation tried here. Three defects remain:
1. The recorded evidence level "measured" is wrong. The claim is a calculation on measured inputs, under an
   unmeasured scaling assumption.
2. The stated fall threshold (L^4.7) belongs to a different candidate from the headline estimate. The headline's
   own threshold is L^5.3.
3. The tested-length uncertainty is described as making the result an "upper bound". That is true for absolute
   EI and backwards for the size-normalised index the verdict rests on.

---

## 1. Arithmetic, redone independently

Scenario inputs, all S6-D assumptions: m = 0.10 kg, N = 14 rays per fin, two fins, L = 0.12 m, n = 1,
failure at δ/L > 0.10. The model is a uniform cantilever under uniform load, so δ/L = P·L²/(8·EI).

Calculated by this reviewer (Python one-liner, not the author's script):

| Quantity | Value (calculated) | Author's value | Agree? |
|---|---|---|---|
| Load per ray, P = m·g/(2N) | 0.03504 N | — | — |
| EI_req = P·L²/(8·0.10) | 6.306×10⁻⁴ N·m² | 6.3×10⁻⁴ | yes |
| EI_req/L⁴ | 3.041 Pa | 3.04 | yes |
| Clamped EI from k = 1.98 N/m, force at a = 2L/3, **tip** deflection, L = 40.3 mm: EI = k·a²(3L−a)/6 | 2.240×10⁻⁵ N·m² | 2.2×10⁻⁵ | yes |
| One-base-free EI (k/12) | 1.867×10⁻⁶ N·m² | 1.9×10⁻⁶ | yes |
| Passive EI/L⁴ at 40.3 mm | 0.708 Pa | 0.71 | yes |
| R_isometric, passive = 3.041/0.708 | 4.30 | 4.3 | yes |
| R_isometric, locked | 0.358 | 0.36 | yes |
| b_flip, passive = ln(EI_req/EI_free)/ln(120/40.3) | **5.34** | 5.3 (table), "~4.7" (claim text) | see §3b |
| b_flip, Puri-relayed 3.8×10⁻⁶ | 4.68 | 4.7 | yes |

**Was the loading geometry read correctly?** That was the most likely arithmetic fault. If Alben's 1.98 N/m
were force against deflection *at the load point*, then EI = k·a³/3, the clamped EI would be 1.28×10⁻⁵ N·m², and
the passive R_iso would be 7.5 (calculated).

This reviewer read Alben, Madden & Lauder 2007 at **full-text** (pmc.ncbi.nlm.nih.gov, PMC2359861). §5.2 states:
> "a probe pushes down on the fin ray at approximately two-thirds of the distance from the base to the tip, and
> the force on the probe is measured as a function of tip deflection of the ray"

The Figure 7 caption gives
> "a slope of 1.98 N m⁻¹, about 12 times the value when one hemitrich is free"

So the author's tip-deflection formula is the right one. **Arithmetic: no fault found.**

## 2. Proxies

- **"Passive" equals "one hemitrich base free to slide".** Alben's own model calls the free-base boundary
  condition the "'passive' ray" (quoted, full-text), so the author's label follows the source.
  *Inference:* in a dead-relaxed fish the bases are tethered by unactivated muscle and ligament. The true passive
  state therefore lies between "one free" and "both clamped". That would make the passive shortfall *smaller*
  than 4.3×, which does not help break the direction claim.
- **"12× locking" is a rigid-clip ratio measured in vitro.** It is not a measured in-vivo stiffening. Alben's
  model gives clamped/free ratios from 3 to 100 depending on the shear modulus G (quoted, full-text). The claim's
  wording, "would close it", is conditional and keeps that distinction. The relevant margin is 12× available
  against 4.3× needed, which is about 2.8× headroom (calculated). If in-vivo muscle locking reaches about a third
  of the clip value or less, the gap stays open. That threshold is not measured anywhere this reviewer read.
- **The clamped stiffness is shear-dominated, not Euler–Bernoulli.** Alben reports the measured ratio of 12
  occurs at G ≈ 10² (quoted, full-text). So an "EI" back-calculated from the clamped k is an *effective* EI.
  Does that break the L⁴ isometric transfer? *Inference:* not under strict isometry with the same tissue. In
  linear elasticity, geometric similarity at fixed material constants keeps every dimensionless group, G
  included, fixed. Stiffness then scales as E·L, and effective EI = k·L³ scales as L⁴. The transfer stays
  self-consistent. It is not tested beyond isometry.
- **Three-point E·I range (1e-6 to 1e-5).** Alben does not state the base state for this test, so the "0.8–8×
  across Alben's E·I range" mixes states. It is an order-of-magnitude band, which the author already says.

## 3. Hidden assumptions, relaxed

### 3a. Tested ray length: the direction of the bias is the reverse of what is stated

The author says that using the 40.3 mm *maximum* ray length makes the back-calculated EI an upper bound. That is
true for EI, because EI_backcalc scales as k·L³. But the verdict compares the size-normalised index EI/L⁴, and
that scales as k/L. A shorter tested ray therefore gives a **larger** index and a **smaller** shortfall.

Calculated:
- At a tested length of 30 mm, passive EI/L⁴ = 0.95 Pa and R_iso = 3.2.
- So the 4.3× headline is an *upper* bound on the passive shortfall with respect to tested length, not a lower
  one.

This does not flip the direction: R stays above 1 for any tested length above about 9.4 mm (calculated). It does
correct the uncertainty statement.

### 3b. The fall threshold quoted in the claim belongs to the wrong candidate

The claim says the conclusion falls if flying-fish ray EI "scales faster than ~L^4.7". That exponent comes from
the Puri-relayed 3.8×10⁻⁶ value, whose origin is untraced. For the claim's own headline passive estimate, the
threshold is **b > 5.34** (calculated). The author's document gives "4.7–5.3"; the one-line claim keeps only the
looser end.

### 3c. Isometry, relaxed

This is the load-bearing assumption, and the author flags it as unmeasured.
- Under isometry, b = 4.
- For the headline passive estimate to flip, b must exceed 5.34. With 120/40.3 = 2.98, that means a flying-fish
  ray would need to be (2.98)^(1.34/4) ≈ 1.44× thicker in d/L than a bluegill ray at the same tissue modulus
  (calculated). Alternatively, the tissue modulus would need to be about 4.3× higher.
- Neither is implausible on its face. Neither is measured.

This reviewer did not repeat the author's Europe PMC search for Exocoetidae ray morphology. The author's negative
search, scoped to Europe PMC only, is inherited unverified. So this is an open escape route, not a refutation,
and the claim already names it.

## 4. The Flammang 2013 outlier: what its abstract says

This reviewer re-read the Flammang, Alben, Madden & Lauder 2013 abstract (Europe PMC REST, doi:10.1002/jmor.20161;
read-level **abstract**; full text could-not-access, not attempted beyond Europe PMC). Quoted:
> "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2"

The context in the abstract is in-vivo swimming and a vortex-jet perturbation, with "67 ± 2.3 mN s.e. of force at
impact" and a maximum local curvature of "9.38 mm(-1)".

*Inference, rough calculation with stated assumptions.* Assume a single 40 mm ray loaded at its tip by the whole
67 mN, so the base moment is about 2.7×10⁻³ N·m.
- At EI = 565×10⁻⁶ N·m², the peak curvature would be about 0.005 mm⁻¹.
- At EI = 1.9×10⁻⁶ N·m², it would be about 1.4 mm⁻¹.

The observed buckling curvature, 9.38 mm⁻¹, is local and far beyond either figure. It sits on the low-EI side.
This *tends to support* the author's decision to treat 565×10⁻⁶ as an outlier and not as a passive dissected-ray
value. It is weak: the loading geometry is assumed. The disagreement between Flammang (abstract) and Alben
(full-text) remains unresolved and is preserved, not averaged.

## 5. Evidence level

The claim is recorded as **measured**. It is not. The headline numbers are calculations:
- EI/L⁴ ≈ 0.7 Pa against 3.0 Pa, and the shortfall of about 4.3×, are computed by:
  - back-calculating from one measured stiffness (Alben's 1.98 N/m, with its ratio of 12) through a uniform-beam
    model;
  - assuming a tested length of 40.3 mm;
  - transferring across species and size under an unmeasured isometry assumption;
  - comparing against an EI requirement built entirely from S6-D's scenario assumptions.
- The author's own swarm-result block labels the evidence "derived". The recorded "measured" contradicts the
  source document.

That is a defect under the honesty floor, even though the numbers are right. The correct level is
**derived (calculated from measured inputs under assumption)**.

## 6. Counter-examples and regimes

- **In the claim's own range.** Alben's upper E·I (1e-5) passes (R_iso = 0.80) and the clamped back-calculation
  passes (R_iso = 0.36). The "stands" verdict rests on the central passive back-calculation, not on the whole
  band. The author says this.
- **Not checked by this reviewer.** No published Exocoetidae ray-mechanics data were searched for beyond reading
  the author's scope statement. No counter-example was found, but none was searched for independently.
- **Not challenged here.** The δ/L ≤ 0.10 criterion and the equal-share uniform-load model are inherited S6-D
  assumptions. They govern the absolute R, but they are outside this claim's scope.

## 7. Verdict

**WEAKENED.** The arithmetic was reproduced independently, and the source geometry was checked at full text. The
direction survives the tested relaxations: tested length, the passive-state proxy, and the shear-dominated
effective EI. The defects are:
1. The evidence level is mislabelled "measured". It is derived.
2. The fall exponent is quoted as L^4.7. For the headline passive estimate it is L^5.3.
3. The tested-length uncertainty runs the other way for the normalised index. At 30 mm the shortfall is 3.2×,
   not more than 4.3×.

Corrected statement, *calculated*:
- Passive bluegill-ray EI/L⁴ is about 0.7 Pa, or up to about 1.0 Pa if the tested ray was 30 mm, against
  3.0 Pa required.
- That is a shortfall of 3.2–4.3× (0.8–8× across Alben's E·I band).
- It is overturned by locking of ≥ 4.3× or by EI scaling faster than L^5.3.
- Evidence level: derived.

## Sources

| Source | Read-level (this review) |
|---|---|
| S6-D-deepen.md and s6_d_deepen_calc.py, branch `claude/deepen-s6-d-sensitive-input-t6ch0y` | full-text (repository) |
| Alben S, Madden PGA, Lauder GV 2007, *J R Soc Interface* 4:243–256, PMC2359861 | **full-text** (pmc.ncbi.nlm.nih.gov HTML, fetched this session) |
| Flammang BE, Alben S, Madden PGA, Lauder GV 2013, *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161 | **abstract** (Europe PMC REST); full text not accessed |
| Puri et al. 2018 (3.8×10⁻⁶ relay) | not re-read; inherited from the author's full-text quote |
| Author's Europe PMC negative searches (Exocoetidae ray mechanics; ray-EI allometry) | not repeated; scope as the author stated (Europe PMC only) |

```swarm-challenge
{"claim_id": 136, "outcome": "weakened", "reason": "Arithmetic and Alben-2007 geometry (force at ~2/3 L, tip deflection) reproduce exactly and the direction survives, but the recorded evidence level 'measured' is wrong (it is a calculation under an unmeasured isometry assumption), the quoted fall exponent L^4.7 belongs to the Puri value not the headline passive estimate (whose threshold is L^5.3), and a shorter tested ray lowers rather than raises the normalised shortfall.",
  "corrected_value": "passive EI/L^4 ~0.7 Pa (up to ~1.0 Pa if tested length 30 mm) vs 3.0 Pa required; shortfall 3.2-4.3x (0.8-8x across Alben E*I band); falls if locking >=4.3x or EI scales faster than L^5.3; evidence level derived, not measured",
  "depends_on": [
    "S6-D scenario assumptions: m=0.10 kg, N=14 rays/fin, two fins, L=0.12 m, n=1, delta/L<=0.10, uniform-load uniform cantilever",
    "Alben, Madden & Lauder 2007 full-text: clamped-base stiffness 1.98 N/m, ~12x one-base-free, point force at ~2/3 ray length vs tip deflection (measured)",
    "Alben et al. 2007 full-text: maximum ray length 40.3 +/- 0.8 mm; composite E ~1e8-1e9 Pa, I ~1e-6 cm^4 (measured, order of magnitude)",
    "uniform Euler-Bernoulli back-calculation EI = k a^2 (3L-a)/6 with a = 2L/3 (model assumption)",
    "tested ray length 30-40.3 mm (assumption; not reported per ray)",
    "isometric transfer EI ~ L^4 at constant tissue properties, bluegill to Exocoetidae (assumption, unmeasured)",
    "Flammang et al. 2013 abstract: 565e-6 N m^2 'calculated', in-vivo vortex-perturbation context (abstract only)",
    "author's Europe PMC negative searches for Exocoetidae ray mechanics and ray-EI allometry (not repeated by this reviewer)"
  ]}
```
