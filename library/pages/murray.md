---
title: Murray's law for branching transport networks
label: law-murray
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-murray
r_0^3 = \sum_i r_i^3
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `r_parent` | L | m | radius of the parent vessel |
| `r_child` | L | m | radius of each daughter vessel |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `exponent` | 3 (interval 2.7 to 3) | 3 is the value derived for laminar Poiseuille flow under a minimum-work argument. Measured exponents in real vasculature fall at or below it; the interval records the measured spread, not an uncertainty on the derivation. |

## Why it holds

Minimisation of the total of (a) the power dissipated by Poiseuille flow, which falls as r^-4, and (b) the metabolic cost of maintaining blood volume, which rises as r^2. Setting the derivative of the sum to zero gives flow proportional to r^3, and conservation of flow at a junction then gives the cube law. The exponent is a consequence of the r^-4 in Poiseuille, so it is tied to LAMINAR flow and does not survive a change of flow regime.

## Where it holds

- **flow regime**: laminar
- **reynolds max**: 2000
- **taxa**: ['mammalian vasculature', 'plant xylem', 'insect tracheae']
- **notes**: Small vessels, where viscous dissipation dominates and flow is steady.

:::{danger} Where it breaks
Fails in large arteries, where flow is pulsatile and inertial rather than viscous-dominated, and where measured exponents approach 2 rather than 3. Fails wherever Reynolds number exceeds roughly 2000 and the Poiseuille r^-4 dissipation term no longer describes the loss. It also assumes the only costs are dissipation and volume maintenance, so it does not describe networks under additional constraints such as mechanical support or thermal exchange.
:::

## Worked examples

**human arterial tree**

- Exponent measured below 3 in the aorta and large arteries, consistent with the pulsatile-flow breakdown above rather than with a failure of the minimum-work argument itself.

- evidence: **literature**

:::{seealso} Contested
- Generalisations (Hess-Murray) allow a non-cubic exponent for non-Poiseuille regimes, which is better read as a different law than as a correction to this one.
:::

## Sources

| Citation | Read-level |
|---|---|
| Murray CD (1926) PNAS 12(3):207-214, The physiological principle of minimum work | `search-summary` |


---

*Generated from [`library/laws/murray.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/murray.yaml). Do not edit this page; edit the YAML.*
