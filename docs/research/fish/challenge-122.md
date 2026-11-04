# Challenge 122: adversarial review of S27 ("EI alone is the wrong representation of a fin ray")

Claim under review: S27 (`docs/research/fish/S27-organ.md`, branch `claude/fin-ray-stiffness-screen-m78qcz`),
recorded at evidence level **measured**. Date: 2026-11-04.

**Verdict: WEAKENED.** The arithmetic holds, and so does the direction of the conclusion (no measured or derived
bluegill ray reaches the S6-D floor under absolute comparison). Four things are wrong with how the claim is stated:

1. The recorded evidence level, **measured**, is wrong. The headline number is a calculation, and S27's own
   swarm-result says "derived".
2. The 27.6× figure is one of two S6-D-D load-point models. The other gives 14.6×. S27 cites both values in
   different tables but plots only one.
3. The claim text states "27.6× below the line" without a condition. In fact the result holds only under S6-D's
   absolute (β = 0) size transfer, and it flips under isometric transfer. S27's §4 says so, but the claim text drops
   the condition.
4. The "84×" compounded multiplier is probably an *over*-estimate. That cuts in the claim's favour, so it does not
   weaken the verdict.

All numbers below are my own **calculations** from the stated inputs, not observations.

## Sources and read-levels

| Source | What I used | Read-level |
|---|---|---|
| S27-organ.md and S27_calc.py (branch `claude/fin-ray-stiffness-screen-m78qcz`) | the claim, inputs and working | full-text (repository) |
| S6-D-D v1, `S6-D-deepen.md` (branch `claude/deepen-s6-d-sensitive-input-t6ch0y`) | Alben k = 1.98 N/m clamped at 2/3 L, ~12× the one-base-free value; locked EI ≈ 2.2e-5 and passive ≈ 1.9e-6 N m² (its calculations) | full-text (repository); Alben 2007 itself is relayed, I did not read it |
| S6-D-D v2, `S6-D-deepen.md` (branch `claude/deepen-s6-d-sensitive-input-fc1hm8`) | the same k with a tip-load model, giving 4.3e-5 N m²; verdict "unresolved" under isometry | full-text (repository) |
| Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243 | k, L = 40.3 mm, 12× | **could-not-access** by me; values relayed through S6-D-D and S26 |
| Nguyen et al. 2017, arXiv:1608.05891 | R∞ = R0(1+γ), γ = Bt/Bn ~ W²/T² | relayed through S27 (full-text there); not re-read by me |
| Das, Hannard & Barthelat 2023 | role of the collagen core | relayed through S27 (abstract there); not re-read by me |
| Web search, "flying fish Exocoetidae pectoral fin ray flexural stiffness bending measurement" | counter-example search | search-summary |

## 1. Arithmetic, redone independently

I took every input from the claim or from the branch it cites, then recomputed.

| Quantity | My value | Claim | Status |
|---|---|---|---|
| M needed at EI_0 = 3.8e-6 (6.3e-4 / 3.8e-6) | 165.8 | 166 | ✓ |
| 1.9e-6 × 12 | 2.28e-5 | 2.3e-5 | ✓ |
| 6.3e-4 / 2.28e-5 | 27.6 | 27.6× | ✓ |
| Shortfall at M = 84, with EI_0 = 3.8e-6 / 1.9e-6 / 1.51e-6 | 1.97 / 3.95 / 4.97 | "2–5×" | ✓ |
| Shortfall at M = 700, same three EI_0 | 0.24 / 0.47 / 0.60 (clears) | 0.24–0.60 | ✓ |
| Fixed area A = WT, γ = (W/T)²: Bn ∝ A²/√γ, Bt ∝ A²√γ | derived from Bn = EWT³/12 | same | ✓ |
| Ceiling ∝ (1+γ)/√γ at γ = 10 / 100 | 3.48 / 10.1 | 3.5 / 10 | ✓ |

**No arithmetic error.** Two scoping points on the trade-off algebra (these are my inferences):

- **The ceiling is not monotonic.** (1+γ)/√γ has its minimum at γ = 1: it is 2.5 at γ = 0.25, 2.0 at γ = 1 and 2.12
  at γ = 2. For γ < 1, passive Bn and the engaged ceiling both fall as γ rises, so they **co-vary instead of
  trading off**. The anti-correlation holds only for γ > 1. That is the relevant regime for mackerel, since
  1+γ = 3–7 gives γ = 2–6. The claim states the trade-off without this bound.
- **"3.5×" is measured against the γ = 1 passive Bn, not the γ = 1 ceiling.** The γ = 1 ceiling is itself 2 in
  those units. Measured ceiling against ceiling, flattening from γ = 1 to 10 gains 1.74×, and from 1 to 100 gains
  5.05×. The trade-off is real but about half as steep as "3.5×" suggests. This sits in S27 §3, not in the claim
  text, so I note it without counting it against the claim.

## 2. Proxy check

**The proxy:** "best *measured* point, EI_0·M = 2.3e-5 N m²".

**What it actually is:** S6-D-D v1 calculated EI_0 = 1.9e-6 as (locked EI) / 12. The locked EI came from one
measured point-load stiffness, through an assumed cantilever model with the load at 2/3 L and deflection read at the
tip. Multiplying by M = 12 therefore just undoes that division. EI_0·M is **the back-calculated locked EI of a
single bluegill ray** (2.24e-5 N m² by my calculation). It is not an independent pairing of two measured axes. For
this point the two-axis map adds no information beyond one derived number.

**The quantity that matters:** the locked, in-vivo ray EI at flying-fish ray length. None has been measured (§5).

**The model dependence the claim omits.** The same k = 1.98 N m⁻¹ gives two values, depending on the load-point
model:

| Model | Locked EI (calculated) | Shortfall against 6.3e-4 |
|---|---|---|
| Load at 2/3 L, tip deflection (S6-D-D v1) | 2.24e-5 N m² | 28.1× (27.6× with S27's rounding) |
| Tip load (S6-D-D v2) | 4.32e-5 N m² | 14.6× |

S27 itself cites 4.3e-5 in its C1 table, then plots only the 1.9e-6 × 12 point. The two S6-D-D versions disagree.
I preserve that disagreement instead of averaging it: the shortfall is **14.6–28.1×**, not 27.6×. Both values are
still below the line.

## 3. Hidden assumptions, tested by relaxing them

**(a) Size transfer, β = 0. This assumption carries the result.**

The requirement of 6.3e-4 N m² is for a 120 mm ray. The bluegill ray is 40.3 mm, so λ = 2.98 and λ⁴ = 78.6. Under
isometric transfer (EI ∝ L⁴), the locked bluegill value becomes:

| Starting value | Transferred EI (calculated) | Against 6.3e-4 |
|---|---|---|
| 2.24e-5 × 78.6 | 1.76e-3 N m² | **clears**, at 0.36 of the requirement |
| 4.3e-5 × 78.6 | 3.4e-3 N m² | clears |
| passive 1.9e-6 × 78.6 | 1.49e-4 N m² | about 4.2× short; measured locking (12×) closes it |

So **relaxing β = 0 flips the claim's headline.** S27 §4 concedes this ("as long as the comparison is absolute")
and says the dispute belongs to S6-D-D, not to the second axis. The claim text, however, states "27.6× below the
line" and "only the modelled near-fused ceiling (700×) clears it" **without that condition**. As recorded, the
claim overstates its own robustness. Note also that "only the multiplier axis M can flip it" is true only of
*second axes*. A change in the size-transfer assumption on the x-axis flips it too.

**(b) Locking and curvature compound multiplicatively (12 × 7 = 84). This is probably an overestimate,** which works
in the claim's favour.

S27 flags this as unverified but does not model it. Here is a first-order model (my inference, not a source
claim). Nguyen's engaged ceiling is R∞ ∝ Bn(1+γ) = Bn + Bt. Base locking raises Bn through bilaminar shear coupling,
and the hemitrich offset lies along the *normal* direction. If locking leaves the in-plane Bt roughly unchanged, the
locked, curved stiffness is about 12·Bn + Bt = (12 + γ)·Bn. For γ = 2–6 that gives **M ≈ 14–18, not 36–84**.

Shortfalls at M ≈ 14–18, with EI_0 = 3.8e-6 / 1.9e-6 / 1.51e-6, are 9–12× / 18–24× / 23–30×. So "2–5× short" is the
*most generous* case, and the negative verdict gets firmer, not weaker. This rests on my assumption that locking
does not raise Bt, which nobody has measured. Separately, using the low end of the curvature range (12 × 3 = 36)
already gives 4.6–11.6×. "2–5×" uses only the 7× end.

**(c) n = 1.** M = 12 is one ray from one fish. No variance exists, so the y-coordinate carries no error bar. S27
discloses this.

## 4. Evidence level

The level is recorded as **measured**, but the claim is **derived**. Each element of the claim is one of: a model
(Nguyen's γ algebra), a calculation on a single relayed measurement (EI_0, EI_0·M), or a scenario requirement that
rests entirely on assumptions (6.3e-4, from m = 0.10 kg, N = 14, L = 0.12 m and δ/L ≤ 0.10). S27's own swarm-result
block says "derived". The phrase "best measured point" in the claim should read "best calculated point (from one
measured stiffness)". **This is a labelling defect, independent of whether the numbers are right.**

## 5. Counter-examples and missed regimes

- **Flying-fish rays.** My search (one web search, query in the source table) found **no measured flexural
  stiffness, locking ratio or cross-section for any exocoetid fin ray**. Scope: that one query only, at
  search-summary level. The hits were labrid three-point bending (Aiello 2018), the bluegill 565e-6 value
  (Flammang 2013) and a robotic flying-fish model. So no taxon contradicts the claim, because the target taxon is
  unmeasured.
- **Flammang 2013, 5.65e-4 N m².** Taken at face value, this sits at 1.1× the floor before any multiplier, which
  would make it a counter-example. S27 handles it fairly: it lists the value as "cannot place", and S6-D-D v2 argues
  it cannot be an excised passive value. I did not read Flammang's methods (could-not-access), so it remains an
  unresolved source disagreement, not a refutation.
- **The fused-ray regime.** Many acanthomorphs have unsegmented, fused spines. That is the G → ∞ case where S27's
  700× ceiling applies. So "near-fused" is not physically exotic. But no spine EI at 120 mm was found within my
  search, and spines are not wing rays. I raise this as an open regime, not a counter-example.

## 6. What survives

- The arithmetic.
- The structural point that a feasibility floor can be flipped only by an axis that multiplies EI, not by
  competing-property trade-offs.
- The negative verdict under S6-D's absolute comparison, at a corrected shortfall of 14.6–28× rather than 27.6×.

What fails is the evidence label, the single-model point estimate, and the unconditional wording of a result that
depends on β = 0.

```swarm-challenge
{"claim_id": 122, "outcome": "weakened", "reason": "Arithmetic and the absolute-comparison verdict hold, but the claim is derived not measured (EI_0*M is a back-calculated locked EI from one k=1.98 N/m), the 27.6x shortfall is one of two S6-D-D load-point models (14.6-28.1x), and the headline is stated unconditionally although isometric size transfer makes the locked bluegill ray clear the floor (1.76e-3 vs 6.3e-4 N m^2).",
  "corrected_value": "best calculated (not measured) EI_0*M = 2.2e-5 to 4.3e-5 N m^2, 14.6-28.1x below 6.3e-4 N m^2 under absolute (beta=0) transfer only; ~0.36x of requirement (clears) under isometric transfer",
  "depends_on": ["S27-organ.md and S27_calc.py, branch claude/fin-ray-stiffness-screen-m78qcz (full-text)", "S6-D-D v1 branch claude/deepen-s6-d-sensitive-input-t6ch0y: locked EI 2.2e-5 / passive 1.9e-6 N m^2 from Alben k=1.98 N/m at 2/3 L (calculated there)", "S6-D-D v2 branch claude/deepen-s6-d-sensitive-input-fc1hm8: tip-load bound 4.3e-5 N m^2; unresolved under isometry", "Alben, Madden & Lauder 2007: k=1.98 N/m clamped, ~12x one-base-free, L=40.3 mm, n=1 (relayed; could-not-access by me)", "S6-D: EI_req = 6.3e-4 N m^2 from assumed m=0.10 kg, N=14, L=0.12 m, delta/L<=0.10", "Nguyen et al. 2017: R_inf = R0(1+gamma), gamma=Bt/Bn, mackerel 1+gamma = 3-7 (relayed via S27)", "my assumption: base locking raises Bn but not Bt, giving combined M ~ 12+gamma = 14-18 (unmeasured)", "my assumption: isometric transfer EI ~ L^4 as the relaxed alternative to beta=0", "web search (one query, search-summary): no measured Exocoetidae fin-ray EI found"]}
```
