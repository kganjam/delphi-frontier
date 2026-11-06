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
| `nu_air_15C` | 1.5e-05 (interval 1.42e-05 to 1.57e-05) m^2/s — *tabulated-remembered* | The VALUE is a standard tabulated property of air and is REMEMBERED, not retrieved. NO SOURCE WAS RETRIEVED FOR THE INTERVAL, which represents variation with temperature over roughly 10-25 degrees C; it is recorded so the uncertainty is visible, and it should be replaced with a tabulated range from a named source before anything rests on its width. |
| `nu_water_20C` | 1.004e-06 (interval 8e-07 to 1.3e-06) m^2/s — *tabulated-remembered* | Same status as the air value: the magnitude is standard and remembered, the interval has no retrieved source and spans roughly 10-30 degrees C. Eloy 2012's organism Reynolds numbers below appear to assume 1.0e-6 for water, which was not confirmed in the paper. |
| `measured_organism_reynolds` | unknown | Measured values spanning fourteen orders of magnitude, to place a design: Encarsia formosa (wasp) 10-20 [Weis-Fogh 1973]; Drosophila wing 100-200 [Lehmann et al. 2005]; goldfish 7.1e3, bottlenose dolphin 1.2e7, killer whale 2.6e7 [Eloy 2012, table]. For comparison, derived from remembered inputs: E. coli 6e-5, human sperm 2.5e-3, pigeon wing 6.7e4, blue whale 1.25e8. No single value is asserted, because Re is a property of a flow and not of an animal. |

## Why it holds

The ratio of inertial to viscous forces in the Navier-Stokes equations. It is the similarity parameter for incompressible flow: two geometrically similar flows at equal Re are dynamically similar, which is what licenses reasoning from one scale to another at all.

## Where it holds

- **notes**: Universally defined for incompressible flow. The CONSEQUENCES attached to a given Re -- the attainable lift coefficient, the stall behaviour -- are geometry-specific and must not be carried across geometries.


:::{danger} Where it breaks
Re itself does not break -- it is a definition, and the inferences people hang on it are what fail. THE COMMONEST ERROR is transferring a lift coefficient measured on one body at a given Re to a different body at the same Re: equal Re gives dynamic similarity only between GEOMETRICALLY SIMILAR flows, and that condition is usually the one quietly dropped. THE SECOND is that the number is not well defined until the characteristic length and velocity are stated: choosing chord against body length, or wing speed against body speed, moves Re by orders of magnitude for the same animal, so a design document that reports a Reynolds number without naming both L and U has reported nothing. Re also ceases to be the SOLE similarity parameter once compressibility (Mach), free-surface effects (Froude) or unsteadiness (Strouhal) matter, and for a flapping or launching animal at least two of those apply at once -- so matching Re alone does not make a model dynamically similar to the thing modelled. Finally the regime boundaries themselves are soft: below about Re 1 flow is reversible and coasting is impossible (Purcell's scallop theorem), above about 1e3 inertia dominates, and the ground between is a transition rather than a line.
:::

## Worked examples

**Danio rerio candidate wing in air**

```
U = 2 m/s, L = 0.01 m, nu = 1.5e-5 m^2/s  ->  Re = 2*0.01/1.5e-5 = 1333
```

- value: `1333`

- Low-Reynolds regime, two orders of magnitude below exocoetid gliding flight. Conventional airfoil performance does not apply and thin cambered plates outperform thick sections here. Note that L is the CHORD; using body length instead would give about 5300 for the same animal.

- evidence: **derived**

**Exocoetidae in gliding flight**

- value range: `[100000.0, 1000000.0]`

- evidence: **literature**

**Encarsia formosa (wasp)**

- value range: `[10, 20]`

- Weis-Fogh 1973. At this Re a steady aerofoil cannot supply the lift coefficient the animal needs, which is the opening for the unsteady mechanisms in the weis-fogh entry.

- evidence: **literature**

**Tursiops truncatus (bottlenose dolphin)**

- value: `12000000.0`

- Eloy 2012 table. Fully inertial.

- evidence: **literature**

## Sources

| Citation | Read-level |
|---|---|
| Reynolds O (1883) Phil Trans R Soc 174:935-982 | `search-summary` |
| Vogel S, Life in Moving Fluids, 2nd ed. | `search-summary` |
| Purcell EM (1977) Am J Phys 45:3-11, Life at low Reynolds number, doi 10.1119/1.10903 | `metadata` |
| Eloy C (2012) J Fluids Struct 30:205-218, Optimal Strouhal number for swimming animals, doi 10.1016/j.jfluidstructs.2012.02.008 | `full-text-preprint` |
| Weis-Fogh T (1973) J Exp Biol 59:169-230, doi 10.1242/jeb.59.1.169 | `abstract` |
| Lehmann F-O, Sane SP, Dickinson MH (2005) J Exp Biol 208:3075-3092, doi 10.1242/jeb.01744 | `abstract` |


---

*Generated from [`library/laws/reynolds.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/reynolds.yaml). Do not edit this page; edit the YAML.*
