---
title: Wing loading and its scaling with mass
label: law-wing-loading
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-wing-loading
\frac{W}{S} = \frac{mg}{S}, \qquad S \propto m^{2/3} \Rightarrow \frac{W}{S} \propto m^{1/3}, \qquad U \propto \left(\frac{W}{S}\right)^{1/2} \propto m^{1/6}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `W_S` | M/(L*T^2) | N/m^2 | wing loading -- weight carried per unit wing area |
| `m` | M | kg | body mass |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `S` | L^2 | m^2 | wing area |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `isometric_exponent` | 0.3333 | DERIVED: under isometry S is proportional to m^(2/3), so wing loading goes as m^(1/3). The null hypothesis, not a measurement. |
| `isometric_speed_exponent` | 0.1667 | DERIVED from lift = (1/2)*rho*U^2*S*C_L: at a fixed lift coefficient, U is proportional to the square root of wing loading, so U goes as m^(1/6) under isometry. This is the practical content -- a bird ten times heavier flies about 1.47 times faster at the same C_L. |
| `procellariiform_span_exponent` | 0.37 (interval 0.34 to 0.4) | Sato et al. 2009, 22 birds of 4 procellariiform species, major-axis fit. Isometry predicts 1/3, and the measured value differs significantly (P = 0.03). THIS IS THE ONLY CI-BEARING SET OF EXPONENTS RETRIEVED FOR THIS ENTRY. |
| `procellariiform_area_exponent` | 0.58 (interval 0.53 to 0.62) | Same study: wing area proportional to M^0.58 against an isometric 2/3 (P = 0.001). |
| `procellariiform_wing_loading_exponent` | 0.42 | DERIVED from the two above: wing loading goes as M^(1 - 0.58) = M^0.42, against an isometric 1/3. Large seabirds are more heavily wing-loaded than scaled-up small ones. The confidence intervals do NOT combine this way, so 0.42 is a point derivation and the paper does not state it. No interval is given here for that reason. |

## Why it holds

Wing loading is a definition, not a law: it is the weight a unit of wing area must carry, and it sets the speed needed to generate that lift at a given lift coefficient. What is law-like, and what is in question, is how it SCALES. Under geometric similarity area grows as the two-thirds power of mass, so wing loading rises as the one-third power and flight speed as the one-sixth. Everything interesting is a departure from that, and the departures are clade-specific.

## Where it holds

- **taxa**: within a clade of similar flight style; the retrieved exponents are procellariiform seabirds
- **notes**: The quantity itself is defined for any flier. Only the SCALING is restricted, and it is restricted narrowly.


:::{danger} Where it breaks
The scaling exponents differ by clade and by flight mode, and pooling across them is the standard error: hummingbirds, soarers, bats and insects do not lie on one line, and Greenewalt himself separated the groups. The practical consequence is that there is no such thing as "the" wing loading exponent for birds -- the only confidence-interval-bearing exponents retrieved here are for 22 individuals of four procellariiform species, and extending them to a 4 cm fish-sized glider is extrapolation across both clade and three orders of magnitude in mass. Wing loading exponents near 0.28-0.33 that circulate for birds, and Tennekes's Great Flight Diagram, are remembered and were not retrieved, so they are not used here. As a design check the quantity CAN be computed exactly for a specific design -- that part is arithmetic -- but the scaling relation cannot reject it; it can only say the design sits inside or outside the scatter of one measured clade, and the clade must be named.
:::

## Worked examples

**a ten-fold mass increase under isometry**

```
wing loading : 10^(1/3) = 2.15x
flight speed : 10^(1/6) = 1.47x   at the same lift coefficient

```

- value: `1.47`

- The isometric baseline a measured exponent is compared against.

- evidence: **derived**

**procellariiform seabirds, measured against isometry**

```
measured wing loading exponent 0.42 vs isometric 0.333
over a 10-fold mass range: 10^0.42 = 2.63x against 10^0.333 = 2.15x

```

- value: `0.42`

- A 22 per cent higher wing loading at ten times the mass than isometry predicts -- which is why the largest seabirds need wind to take off. Derived from two intervals whose CIs do not combine, so it carries no interval of its own.

- evidence: **derived**

:::{seealso} Contested
- Greenewalt 1962 and 1975, and Norberg & Rayner 1987 for bats, compiled the classic dimensional relations across birds, bats and insects. Their exponents were NOT retrieved in this compilation, so this entry cannot report what they disagree about -- only that a broader set of measurements exists and is not represented here.
:::

## Sources

| Citation | Read-level |
|---|---|
| Sato K et al. (2009) PLoS ONE 4:e5400, Scaling of soaring seabirds and implications for flight abilities of giant pterosaurs, doi 10.1371/journal.pone.0005400, PMC2670537 | `full-text` |
| Greenewalt CH (1962) Smithson Misc Coll 144(2), Dimensional relationships for flying animals, with special reference to hummingbirds (Smithsonian handle 10088/22978) | `metadata` |
| Greenewalt CH (1975) Trans Am Philos Soc 65(4), The flight of birds | `remembered` |
| Norberg UM, Rayner JMV (1987) Phil Trans R Soc B 316:335-427, doi 10.1098/rstb.1987.0030 | `metadata` |


---

*Generated from [`library/laws/wing-loading.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/wing-loading.yaml). Do not edit this page; edit the YAML.*
