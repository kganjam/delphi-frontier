---
title: Reynolds number and flow-regime boundaries
label: law-reynolds
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-reynolds
\mathrm{Re} = \frac{\rho U L}{\mu} = \frac{U L}{\nu}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `rho` | M/L^3 | kg/m^3 | fluid density |
| `U` | L/T | m/s | characteristic velocity |
| `L` | L | m | characteristic length (chord, for a wing) |
| `mu` | M/(L*T) | Pa*s | dynamic viscosity |
| `nu` | L^2/T | m^2/s | kinematic viscosity |
| `Re` | 1 | dimensionless | ratio of inertial to viscous forces |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `nu_air_15C` | 1.5e-05 (interval 1.42e-05 to 1.57e-05) m^2/s | varies with temperature |
| `nu_water_20C` | 1.004e-06 (interval 8e-07 to 1.3e-06) m^2/s | varies with temperature |

## Why it holds

The ratio of inertial to viscous forces in the Navier-Stokes equations. It is the similarity parameter for incompressible flow: two geometrically similar flows at equal Re are dynamically similar, which is what licenses reasoning from one scale to another at all.

## Where it holds

- **notes**: Universally defined for incompressible flow. The CONSEQUENCES attached to a given Re -- the attainable lift coefficient, the stall behaviour -- are geometry-specific and must not be carried across geometries.


:::{danger} Where it breaks
Re itself does not break; the inferences people hang on it do. The common error is transferring a lift coefficient measured on one body at a given Re to a different body at the same Re. Re also ceases to be the sole similarity parameter once compressibility (Mach), free-surface effects (Froude), or unsteadiness (Strouhal) matter -- and for a flapping or launching animal, at least two of those apply simultaneously.
:::

## Worked examples

**Danio rerio candidate wing in air**

```
U = 2 m/s, L = 0.01 m, nu = 1.5e-5 m^2/s  ->  Re = 2*0.01/1.5e-5 = 1333
```

- value: `1333`

- Low-Reynolds regime, two orders of magnitude below exocoetid gliding flight. Conventional airfoil performance does not apply and thin cambered plates outperform thick sections here.

- evidence: **derived**

**Exocoetidae in gliding flight**

- value range: `['1.0e5', '1.0e6']`

- evidence: **literature**

## Sources

| Citation | Read-level |
|---|---|
| Reynolds O (1883) Phil. Trans. R. Soc. 174:935-982 | `search-summary` |
| Vogel S, Life in Moving Fluids, 2nd ed. | `search-summary` |


---

*Generated from [`library/laws/reynolds.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/reynolds.yaml). Do not edit this page; edit the YAML.*
