# Challenge 266: adversarial review of [S26-D-D] (passive EI sensitivity of a 120 mm exocoetid ray)

**Claim under review (the author's, not mine):** S26-D's "conditional yes" holds. Its most sensitive input is the passive EI of a 120 mm ray, which goes as d^4. A 2x diameter error flips the relay margin from 5.69 to 0.36, while 2x errors in EI_req, EI_src or F_a do not. A labrid anchor (measured 1.9-2.1e-7 N m^2 at 17.8-20.2 mm), scaled at n=4, gives 2.4-4.4e-4 N m^2. That is a 1.4-2.7x passive shortfall, which a 12x active factor clears. The break-even diameter ratio is 0.647 (relay) and 0.889 (primary). The author's verdict is "stands". The recorded evidence level is "measured".

**Source material available to me:** the source record `harvest:s26-d-sensitive-input-q4usu0` and the S26-D model are not in this repository. Scope of that search: `git grep` of every local and remote branch for "S26-D", "exocoet", "flying" and "labrid", plus `seeds/*.json`, with zero hits. So I judge the claim only from the inputs stated in it. I could not see the S26-D margin equations, the source of the 12x active factor, or the labrid source paper.

## 1. Arithmetic redone independently (all calculated, none observed)

| Quantity | My calculation | Claim | Agrees? |
|---|---|---|---|
| Labrid EI scaled to 120 mm at n=4: 1.9e-7 at 20.2 mm / 2.1e-7 at 20.2 mm / 1.9e-7 at 17.8 mm / 2.1e-7 at 17.8 mm | 2.37e-4 / 2.62e-4 / 3.92e-4 / 4.34e-4 N m^2 | 2.4e-4 to 4.4e-4 | Yes. The upper end rounds to 4.3e-4, and the extremes take the worst-case EI-length pairing. |
| Implied EI_req, from the 1.4-2.7x shortfall | about 6.2-6.5e-4 N m^2 | (not stated) | Internally consistent |
| Relay margin with a diameter ratio of 0.5: 5.69/16 | 0.356 | 0.36 | Yes |
| Relay break-even diameter: (1/5.69)^(1/4) | 0.647 | 0.647 | Yes |
| **Primary-path margin implied by its break-even: 1/0.889^4** | **1.60** | not stated | n/a |
| Break-even n, relay, assuming the source anchor is about 2.97x shorter than 120 mm | 2.40 | 2.4 | Yes |
| Break-even n, primary, same anchor ratio | 3.57 | 3.57 | Yes. The two n-thresholds are mutually consistent. |
| Break-even n for the labrid anchor with 12x active (margin 4.4-8.6, scale ratio 120/19) | 2.83-3.19 | ">= 3.0" | Partly. 3.0 is the midpoint. The worst-case pairing needs n >= 3.19. |

## 2. The break: the "2x errors do not flip" statement fails on the primary path

The claim says 2x errors in EI_req, EI_src or F_a "do not" flip the result. That holds for the relay path, where 5.69/2 = 2.85 > 1. **The primary-path break-even diameter of 0.889, under the same d^4 dependence, implies a primary margin of only about 1.60.** A 2x adverse error in EI_req (or in any input that enters the margin linearly) halves it to **about 0.80, which flips the primary path.** This is my inference. It assumes that EI_req enters the primary margin linearly, the same way it enters the relay margin. The matching n-thresholds (2.40 and 3.57 both reproduce from a single anchor ratio of about 2.97) suggest that both paths share the same EI structure. I could not see the S26-D equations to confirm it.

The headline tolerance has the same problem. The claim says the yes "still requires the real ray to be no more than ~35% thinner than isometry predicts". That 35% is the relay tolerance, which is the most lenient one. On the primary path the ray can be no more than **about 11% thinner** (0.889). An 11% diameter deviation is well inside normal interspecific scatter in fin-ray cross-sections. So for the primary path the "conditional yes" is close to knife-edge, not comfortably conditional.

## 3. Proxy check

The quantity that matters is the bending resistance of the ray **in the loaded region**, under the actual loading. The claim uses "the passive EI of a 120 mm ray" as one number, and that is a proxy.

- Read-level: search-summary of Aiello et al. 2017, J Exp Biol, doi 10.1242/jeb.163360. Labrid pectoral ray EI **decreases exponentially along the proximo-distal span**, and the reported range across positions is 1e-10 to 1.5e-6 N m^2 (0.0001-1.5109 µN m^2). The anchor's 1.9-2.1e-7 N m^2 lies inside that range. I could not determine which span position it represents. If it is a proximal value but the binding load acts mid- or distal-span, the effective EI is lower by an unknown factor. That is a second route to the same flip, independent of diameter.
- Read-level: search-summary of Aiello et al. 2018, J Morphol, doi 10.1002/jmor.20830. Variation in **second moment of area** explains most variation in EI. This supports the author's choice of a geometric (I) exponent as the main uncertainty.
- Lepidotrichia are bilayer hemitrichia. If only the hemitrichial separation is off (I ≈ 2A(h/2)^2), EI scales about h^2, not d^4. That makes the claim **more** robust than it states, so it is not a fault. I note it so the d^4 sensitivity is not read as the only possible failure mode.

## 4. Hidden assumption: the 12x active factor

The labrid-anchor route fails passively (shortfall 1.4-2.7x), so its "yes" rests entirely on a 12x active stiffening factor. The claim gives no source or evidence level for 12x, and I found none in the repository. If I relax it, the route needs an active factor of at least 1.4-2.7x at n=4. At n=3.0 it needs about 2.4-4.7x more (calculated: (120/19)^1 × the n=4 shortfall gives 8.8-17x in total). Above 12x, that route turns negative. The source of 12x is `unknown`.

## 5. Evidence level

The claim's KEY value (2.4-4.4e-4 N m^2) is labelled "calculated" in its own text, which is honest. The **recorded evidence level "measured" is not honest for this claim.** The only measured input is the labrid anchor. Every conclusion (margins, break-evens, n-thresholds, the 1.4-2.7x shortfall) is a calculation or a sensitivity analysis. It should be recorded as calculated/derived.

## 6. Regime, taxon or counter-example

No exocoetid ray dimension, EI value or EI-size exponent was found. Scope of that search: one web search on labrid fin-ray EI. I ran no exocoetid-specific literature search, so this does not rule out that such data exist. The claim's own negative search has the same gap. Extrapolating from labrid to exocoetid also crosses a functional regime: a gliding fin that is held spread, versus a flapping/rowing fin. The exponent n could plausibly differ in either direction. That makes it a real unknown, not a counter-example.

## Verdict: WEAKENED

The arithmetic reproduces and the relay-path conclusion survives. Two statements in the claim do not hold:

1. "2x errors in EI_req ... do not [flip]" is false for the primary path. Its implied margin of about 1.60 falls to about 0.80.
2. The "~35% thinner" tolerance applies only to the relay path. The primary path tolerates about 11%.

The recorded evidence level "measured" overstates a derived result. The 12x active factor carries the labrid route but has no stated source.

Sources: [Aiello et al. 2017, J Exp Biol, jeb.163360 (search-summary)](https://cob.silverchair.com/jeb/article-pdf/221/1/jeb163360/1901003/jeb163360.pdf); [Aiello et al. 2018, J Morphol, jmor.20830 (search-summary)](https://zendy.io/title/10.1002/jmor.20830); [Dryad dataset doi:10.5061/dryad.0463n (listing)](https://datadryad.org/dataset/doi:10.5061/dryad.0463n).

```swarm-challenge
{"claim_id": 266, "outcome": "weakened", "reason": "Arithmetic reproduces and the relay path stands, but the primary path's break-even diameter 0.889 implies a margin of only ~1.60, so a 2x error in EI_req flips it (~0.80), contradicting the claim, its usable thinness tolerance is ~11% not ~35%, and the recorded 'measured' level mislabels a derived result.", "corrected_value": "primary-path margin ~1.60 (calculated, = 1/0.889^4); flips at 2x adverse EI_req (~0.80); primary diameter tolerance ~11% thinner than isometry", "depends_on": ["relay margin 5.69 at isometry (author's S26-D value)", "primary break-even diameter ratio 0.889 (author's value)", "EI enters both margins as diameter^4 and EI_req enters linearly (inferred; S26-D equations not seen)", "labrid anchor EI 1.9-2.1e-7 N m^2 at 17.8-20.2 mm (author's citation; not verified, search-summary only)", "12x active factor (author's value; source unknown)"]}
```
