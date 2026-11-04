# Challenge 192: adversarial review of the S28 leap and flight ratios

**Claim under review (author: S28, `docs/research/fish/S28-organism.md`, commit e8ba4191, branch `claude/s28-organism-design-5z0vjz`):**
"A 3x leap would require a 2.39 m/s exit, 1.73x the measured maximum. Flight requires 4.37 m/s: 3.2x the speed and 10x the kinetic energy."
Recorded level: **derived**. Value: 3.2 (speed ratio).

**Status of this review:** every number in this file is **calculated** (closed form, or point-mass integration in
`docs/research/fish/challenge-192.py`). Nothing here is a measurement.

**Sources:**
- `S28-organism.md` and `S28_organism.py`: read-level **full-text**.
- Miln et al. 2021 (burst 0.45–1.38 m/s): **could-not-access**. I did not open it. I take 1.38 m/s as the author states it.
- Daane et al. 2021: not needed for this verdict.

## 1. Independent arithmetic

Inputs, as stated by the author: maximum burst 1.38 m/s (measured, swimming); V_to 4.37 m/s (derived by the project); g = 9.81 m s⁻².

| Quantity | My calculation | Author | Match |
|---|---|---|---|
| Vacuum range ∝ V², so 3× range needs V × √3 | 1.38 × 1.7321 = **2.390 m/s** | 2.39 | yes |
| Ratio to the maximum | √3 = **1.732** | 1.73 | yes |
| Flight speed ratio | 4.37 / 1.38 = **3.167** | 3.2 | yes (rounded) |
| Kinetic-energy ratio (per unit mass) | 3.167² = **10.03** | 10 | yes |
| V_to recomputed from m = 0.25 g, S = 192 mm², CL 1.07 | √(2·2.4525e-3 / (1.225·192e-6·1.07)) = **4.41 m/s** → ratio **3.20**, KE ratio **10.2** | 4.37 | 1 % apart, within the author's rounding of S |

The arithmetic holds.

## 2. Proxy check

- **Swimming burst speed stands in for water-exit speed.** The quantity that matters is exit speed, which nobody has measured. The author flags this proxy and states the direction: breaking the surface costs speed, so exit ≤ burst. *My inference:* that direction makes both ratios **lower bounds** on the deficit, so the proxy cannot rescue flight. One gap remains open. If 1.38 m/s is a *mean* burst speed and not a *peak*, the instantaneous peak could be higher. I could not check which it is (Miln 2021 not accessed): **unknown**.
- **"10× kinetic energy" is KE per unit mass at the moment of exit.** It leaves out the work of breaking the surface and the potential energy of climbing, so it understates the energy deficit. It cannot overstate it.

## 3. Hidden assumptions, tested relaxed

1. **The wing is ignored in the 3× leap figure.**
   - √3 scaling is wingless vacuum ballistics. S28 says "the wing contributes nothing towards it". That is not quite true at 2.39 m/s, where case-C lift at launch is (2.39/4.37)² ≈ 30 % of W.
   - I re-solved for the exit speed that gives 3 × the wild-type range (3 × 19.36 cm), with body drag, launch angle optimised, and CL chosen from 0 to 1.07 (calculated):

   | Configuration | Exit speed for 3× | Ratio to 1.38 |
   |---|---|---|
   | Wingless, body drag | **2.397 m/s** | 1.737 |
   | Case C, CD0 0.08 | **2.318 m/s** | 1.680 |
   | Case C, CD0 0.20 | 2.348 m/s | 1.701 |
   | Case B, CD0 0.12 | 2.346 m/s | 1.700 |
   | Case A, CD0 0.12 | 2.370 m/s | 1.718 |

   - The wing lowers the requirement by at most **3 %** (2.39 → 2.32 m/s; 1.73× → 1.68×). Body drag raises it by 0.3 %.
   - The claim's figures are right for a wingless fish and very slightly high for the winged design. This does not change any conclusion. The side remark that the wing contributes "nothing" should read "≤ 3 %".

2. **V_to = 4.37 m/s is the most generous geometry.** It uses case C (AR 5, S 192 mm², never measured) and the back-solved 0.25 g mass. Relaxing either *raises* the ratio (calculated):
   - Mass 0.40 g: V_to 5.58 m/s → **4.0×** speed, **16×** KE.
   - Case B area: 5.47 m/s → **4.0×**.
   - Case A area: 8.10 m/s → **5.9×**, **34×** KE.

   So "3.2×" is the **minimum** deficit under the author's own geometry range, not a central estimate. The author's §2.2 says that C is an upper bound, but the claim sentence on its own reads as a point value.

3. **CL_max = 1.07 in steady flow.**
   - Two effects could raise effective lift: ground effect over the water surface, and unsteady or high-angle lift at Re ≈ 600–1800.
   - Because V_to ∝ CL^-1/2, even a 50 % increase in effective CL (1.6, a figure I have not sourced) lowers V_to by only 18 %, to 3.57 m/s. That is still **2.6×** the measured maximum.
   - I did not search the literature for measured ground-effect CL in fish fins; the scope of the negative is **none searched**. This sensitivity bounds the effect without needing the number.

4. **Steady flight from a single exit.** Real flying fish taxi: the tail sculls while the body is airborne, and they accelerate past their exit speed. S28 covers that separately (132–199 Hz needed vs 52 Hz measured). That figure is not part of this claim and I did not re-derive it.

## 4. Evidence level

"Derived" is honest. The numbers come from one measured input (1.38 m/s burst) and one derived input (4.37 m/s). The phrase "reproduced here" means re-computed from stated inputs, not re-measured, and S28 labels it that way. The level carries no defect.

## 5. Counter-examples and regimes

- A regime the author underweights is ground-effect or unsteady lift near the surface (item 3). The bound above shows it cannot close a ≥ 2.6× gap.
- I cite no published zebrafish water-exit speed. I did not search for one. That search is item 2 on S28's own list.

## Verdict: SURVIVED

Every number reproduces independently. Each assumption I relaxed either leaves the ratios unchanged (≤ 3 % from wing lift on the 3× leap figure) or makes the deficit larger (mass, fin area, the exit-vs-burst penalty). The one inaccuracy I found is the side remark that the wing "contributes nothing" to a 3× leap. The true figure is ≤ 3 % (2.32 vs 2.39 m/s), well inside the claim's own rounding of the conclusion. Read 3.2× as a lower bound, not a point estimate.

```swarm-challenge
{"claim_id": 192, "outcome": "survived", "reason": "Independent recomputation gives 2.390 m/s (sqrt3 x 1.38), 1.732x, 3.17x speed and 10.0x KE; relaxing assumptions only raises the flight deficit (0.40 g -> 4.0x, case A -> 5.9x), and wing lift lowers the 3x-leap exit requirement by at most 3% (2.32-2.40 m/s calculated).",
  "corrected_value": null,
  "depends_on": ["Miln2021-burst 1.38 m/s (measured swimming burst, not exit speed; not accessed by me)", "V_to 4.37 m/s (project-derived; case C AR5 S=192 mm2, m=0.25 g, CL_max 1.07)", "point-mass trajectory model with body CD 0.3 and Oswald e 0.8 (S28 assumptions)", "g = 9.81 m/s2"]}
```
