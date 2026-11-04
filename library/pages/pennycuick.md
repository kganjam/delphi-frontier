---
title: Pennycuick power curve for flapping flight
label: law-pennycuick
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-pennycuick
P(U) = \underbrace{\frac{k(mg)^2}{2\rho S_d U}}_{\text{induced}} + \underbrace{\tfrac{1}{2}\rho S_b C_{Db} U^3}_{\text{parasite}} + \underbrace{P_{pro}}_{\text{profile}}, \qquad S_d = \frac{\pi b^2}{4}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `P` | M*L^2/T^3 | W | total mechanical power required for steady level flight |
| `k_i` | 1 | dimensionless | induced-power factor, about 1.1-1.2 |
| `m` | M | kg | body mass |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `rho` | M/L^3 | kg/m^3 | air density |
| `S_d` | L^2 | m^2 | disc area swept by the wings, pi*b^2/4 for span b |
| `U` | L/T | m/s | airspeed |
| `S_b` | L^2 | m^2 | body frontal area |
| `C_Db` | 1 | dimensionless | body drag coefficient |
| `P_pro` | M*L^2/T^3 | W | profile power -- the drag of the wings themselves, often treated as roughly constant across cruise speeds |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `induced_power_factor` | 1.15 (interval 1.1 to 1.2) | REMEMBERED, not retrieved. The usual allowance for non-ideal induced flow. Flagged because it multiplies the dominant term at low speed. |
| `minimum_power_speed_exponent` | 0.1667 | REMEMBERED: under geometric similarity the minimum-power speed V_mp scales as m^(1/6). Not retrieved from Pennycuick, and no measured V_mp values were available to test it. |
| `added_load_speed_exponent` | 0.5 | RETRIEVED from Pennycuick 1969: adding weight increases both minimum-power speed and maximum-range speed in proportion to the SQUARE ROOT of the weight, and the corresponding powers in proportion to the three-halves power. This is the one quantitative scaling in the entry that comes from the source rather than from memory. |
| `fat_load_ceiling_g` | 750 | Pennycuick 1969: birds up to about 750 g fat-free can double their fat-free mass and still have sufficient power to fly at the maximum-range speed. A usable number for a migration energy budget. |

## Why it holds

Actuator-disc theory borrowed from aircraft. Induced power -- the cost of accelerating air downwards to make lift -- falls as 1/U, because at higher speed more air is handled per second so less downwash is needed. Parasite power, the drag of the body, rises as U^3. Their sum is therefore U-shaped, and two speeds fall out of it: V_mp where P is least, and V_mr where P/U is least, found as the tangent from the origin. The shape is the content; the two speeds are what a flight plan is built on.

## Where it holds

- **motion**: steady, level, flapping flight
- **taxa**: birds and bats
- **notes**: The theory is aerodynamic rather than biological, so it computes a number for any set of inputs. Its validity question is whether the inputs -- k, S_b, C_Db and the profile power -- are known for the animal, and usually they are not.


:::{danger} Where it breaks
The decisive measurement is Tobalske et al. 2003, and it breaks the curve's USE rather than its algebra: measured power curves range from acutely concave in cockatiels, through intermediate in doves, to RELATIVELY FLAT over intermediate velocities in the magpie. Where the curve is flat its minimum is not localised, so V_mp is a poor predictor of the speed a bird actually chooses, and a design optimised to a computed V_mp is optimising a quantity the animal does not appear to track. The same study found that wingbeat frequency and mechanical power output do not necessarily share minima, so neither can stand in for the other. Beyond that, intermittent flight -- bounding and flap-gliding -- hovering, and very small fliers where unsteady mechanisms dominate are all outside it. The honest classification is therefore descriptive: the curve is a MODEL THAT COMPUTES a number once you supply k, S_b, C_Db and the profile power, and that can be a legitimate design calculation, but it is not a biological check, because the measured curves are too varied for agreement with it to confirm anything. Use it to compute, not to validate.
:::

## Worked examples

**a 10 kg swan against a 0.4 kg pigeon**

```
V_mp ratio = (10/0.4)^(1/6) = 25^0.1667 = 1.71
```

- value: `1.71`

- The swan's minimum-power speed should be about 1.7 times the pigeon's. NO RETRIEVED V_mp VALUES WERE AVAILABLE TO CHECK THIS, and the m^(1/6) exponent it rests on is itself remembered, so the example demonstrates the calculation and confirms nothing.

- evidence: **derived**

**a migrating bird taking on fat, from Pennycuick's retrieved scaling**

```
doubling mass: speeds rise by 2^(1/2) = 1.41x, powers by 2^(3/2) = 2.83x

```

- value: `2.83`

- Power required grows twice as fast as speed, which is why the 750 g ceiling exists at all. Both exponents are retrieved from the 1969 abstract.

- evidence: **derived**

:::{seealso} Contested
- Tobalske et al. 2003 do not contest the theory; they measure that its central qualitative prediction -- a well-defined U-shaped minimum -- varies from sharp to nearly absent across species. That is a limit on inference from the curve rather than a rival model.
:::

## Sources

| Citation | Read-level |
|---|---|
| Pennycuick CJ (1968) J Exp Biol 49:527-555, Power requirements for horizontal flight in the pigeon Columba livia, doi 10.1242/jeb.49.3.527 | `metadata` |
| Pennycuick CJ (1969) Ibis 111:525-556, The mechanics of bird migration, doi 10.1111/j.1474-919x.1969.tb02566.x | `abstract` |
| Pennycuick CJ (1975) Mechanics of flight, in Avian Biology vol 5 | `remembered` |
| Pennycuick CJ (2008) Modelling the Flying Bird | `remembered` |
| Tobalske BW, Hedrick TL, Dial KP, Biewener AA (2003) Nature 421:363-366, Comparative power curves in bird flight, doi 10.1038/nature01284 | `abstract` |
| The three-term power decomposition is a standard form and was not retrieved verbatim from any of the above. | `remembered` |


---

*Generated from [`library/laws/pennycuick.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/pennycuick.yaml). Do not edit this page; edit the YAML.*
