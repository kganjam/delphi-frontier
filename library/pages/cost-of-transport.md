---
title: Cost of transport against body mass
label: law-cost-of-transport
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-cost-of-transport
\frac{E_\mathrm{metab}}{M_b} = 10.7\, M_b^{-0.316} v_g + 6.03\, M_b^{-0.303}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `P_spec` | L^2/T^3 | W/kg | mass-specific metabolic power |
| `M_b` | M | kg | body mass |
| `v_g` | L/T | m/s | ground speed |
| `c_1` | M^0.316*L/T^2 | J kg^-1 m^-1 kg^0.316 | the slope coefficient, 10.7; this IS the incremental cost of transport once multiplied by M_b^-0.316 |
| `c_2` | M^0.303*L^2/T^3 | W kg^-1 kg^0.303 | the postural or zero-speed intercept coefficient, 6.03 |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `slope_coefficient` | 10.7 J kg^-1 m^-1 (at M_b = 1 kg) | Taylor, Heglund & Maloiy 1982, from 62 avian and mammalian species, with 1 ml O2 = 20.1 J. The coefficient is in J per kg per metre and NOT in ml O2 per kg per km, a unit confusion that is in circulation. In oxygen units the equation reads 0.533*M^-0.316*v_g + 0.300*M^-0.303 ml O2 per s per kg. |
| `slope_exponent` | -0.316 | Alexander 2005 independently summarises running cost of transport as proportional to M^-0.32, which is consistent. No confidence interval was retrieved for either. |
| `intercept_coefficient` | 6.03 W kg^-1 (at M_b = 1 kg) |  |
| `scatter_band` | 0.25 (interval 0.75 to 1.25) | Ninety per cent of the data lie within 25 per cent of the line. This is the stated tolerance of the check and it is wide: any single animal may legitimately sit a quarter off. |

## Why it holds

There is no agreed mechanism, and the entry is honest about that: the relation is an empirical regression. Proposals include the cost of generating muscle force scaling with stride frequency, and the different mechanics of small animals. The tell is in the units: the coefficient c_1 must carry a FRACTIONAL MASS DIMENSION, M^0.316, for the equation to balance at all. A physical law does not need a coefficient with a fractional dimension; a fit across a mass range does. That is the cheapest available diagnostic for distinguishing the two, and it is why this entry sits on the boundary between the constraining and descriptive classes.

## Where it holds

- **motion**: steady level running
- **taxa**: birds and mammals, 62 species
- **mass range kg**: about 0.01 to 250 (the range is remembered, not retrieved)
- **speed**: the range over which metabolic power is linear in speed

:::{danger} Where it breaks
Outside the linear power-against-speed range the two-term form is simply the wrong shape, and the fit carries no warning when you leave it. Hopping kangaroos are the standard counterexample: their cost is roughly constant with speed, so a slope coefficient describes them not at all. Inclines and carried loads are outside the dataset. Humans lie above the line. And the plus-or-minus 25 per cent band holding only 90 per cent of 62 species means one animal in ten is outside even that, so the relation cannot reject a design: it can only say the design is unlike the measured sample. The claim it supports is "this is within the observed scatter of running birds and mammals", which is a weaker statement than it looks.
:::

## Worked examples

**incremental cost of transport across three masses, 10.7*M^-0.316 J kg^-1 m^-1**

```
mouse  0.03 kg : 0.03^-0.316 = 3.03  -> 32.4 J kg^-1 m^-1
70 kg mammal   : 70^-0.316   = 0.261 ->  2.79 J kg^-1 m^-1
horse  500 kg  : 500^-0.316  = 0.140 ->  1.50 J kg^-1 m^-1
ratio mouse:horse = 32.4/1.50 = 21.6

```

- value: `21.6`

- The mouse pays 21.6 times more per kilogram per metre than the horse. The 25 per cent band means any single animal could legitimately lie 0.75 to 1.25 times off the line, so a two-fold discrepancy is informative and a 20 per cent one is not.

- evidence: **derived**

:::{seealso} Contested
- Alexander 2005 gives separate scalings for other modes: flight mechanical power at maximum-range speed scales as M^1.02 against metabolic power M^0.83; fish modelled as submarines give power proportional to M^0.5*U^2.5 (laminar) or M^0.6*U^2.8 (turbulent). These are different laws for different media, not corrections to this one.
- Schmidt-Nielsen 1972's three-line picture -- swimming cheaper than flying cheaper than running at a given mass -- is widely cited, but the paper was reached only at metadata level here and its exponents were not retrieved, so it is recorded as unverified.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taylor CR, Heglund NC, Maloiy GMO (1982) J Exp Biol 97:1-21, Energetics and mechanics of terrestrial locomotion I, doi 10.1242/jeb.97.1.1 | `abstract` |
| Alexander RMcN (2005) J Exp Biol 208:1645-1652, Models and the scaling of energy costs for locomotion, doi 10.1242/jeb.01484 | `abstract` |
| Schmidt-Nielsen K (1972) Science 177:222-228, doi 10.1126/science.177.4045.222 | `metadata` |
| Tucker VA (1970) Comp Biochem Physiol 34:841-846, doi 10.1016/0010-406X(70)91006-6 | `metadata` |


---

*Generated from [`library/laws/cost-of-transport.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/cost-of-transport.yaml). Do not edit this page; edit the YAML.*
