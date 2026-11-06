---
title: Second moment of area, beam stiffness and span
label: law-second-moment
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-second-moment
I_\mathrm{solid} = \frac{\pi r^4}{4}, \quad I_\mathrm{tube} = \frac{\pi (R^4 - r_\mathrm{in}^4)}{4}, \quad \delta = \frac{F L^3}{3 E I}, \quad \delta_\mathrm{self} = \frac{q L^4}{8 E I}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `delta` | L | m | tip deflection of an end-loaded cantilever |
| `F` | M*L/T^2 | N | transverse tip load |
| `L_span` | L | m | span of the cantilever |
| `E` | M/(L*T^2) | Pa | Young's modulus of the beam material |
| `I` | L^4 | m^4 | second moment of area of the cross-section about the neutral axis |
| `r` | L | m | radius of a solid circular section |
| `R` | L | m | outer radius of a tubular section |
| `r_in` | L | m | inner radius of a tubular section |
| `q` | M/T^2 | N/m | self-weight per unit length, rho*g*A, for the self-loaded case |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `span_thickness_exponent` | 1.5 | Derived, exact. Hold relative sag delta/L fixed in the same material under self-weight: delta/L is proportional to rho*g*L^3/(E*d^2), so d^2 scales as L^3 and d scales as L^1.5. This is the SAME relation McMahon calls elastic similarity, reached from beam theory rather than from a similarity postulate -- which is why the mechanics entry is constraining and the similarity entry is not. |
| `mammal_optimum_r_over_t` | 2 (interval 2 to 4) | Taylor & Dirks 2012 (secondary, full text): the optimum outer-radius-to-wall-thickness ratio for mammals is 2 on a strength criterion or 4 on a stiffness criterion, and the most common value for land mammals is 2. Birds range 2-8. If r is the OUTER radius, r/t = 2 corresponds to a bore ratio K = 0.5 -- that convention for r was NOT confirmed in the source, so the conversion is provisional. |
| `bird_r_over_t` | 5 (interval 2 to 8) | Birds, from the same secondary source. The wide range is the measurement, not an uncertainty. |

## Why it holds

Bending strain grows linearly with distance from the neutral axis, so a fibre's contribution to resisting the moment grows as distance SQUARED, and the integral of that over the section is I. Material near the axis is nearly idle, which is why a hollow tube gives the most bending stiffness per unit mass and why so many load-bearing biological structures -- long bones, feather rachises, grass culms, insect legs -- are tubes. The fourth-power dependence on radius is the same algebra that gives Poiseuille its r^4, from a different integral over the same section.

## Where it holds

- **geometry**: slender beams, span much greater than depth
- **material**: linear elastic, isotropic, small deflections
- **notes**: The formulae are exact within those assumptions and are not in dispute. What is uncertain in biology is the INPUTS -- E for a hydrated anisotropic tissue, and the real cross-section.


:::{danger} Where it breaks
Thin walls buckle locally before they yield: Brazier ovalisation flattens the section of a bent tube, which collapses I itself, so the stiffness the formula promises disappears at exactly the wall thickness that the mass-optimum argument pushes you towards. The optimisation and the failure mode therefore pull in opposite directions, and a design that takes the hollowness argument to its conclusion without a buckling check is wrong. Bone is anisotropic and its cross-section is not circular, so a single E and a textbook I are both approximations. Beam theory itself needs span much greater than depth and fails for short, stubby elements. And for small animals the governing criterion may not be strength at all: Biewener 1990 notes that at smaller sizes skeletal STIFFNESS may be more critical than strength, so the quantity to hold constant changes with scale, and Currey & Alexander 1985 show the optimum wall ratio itself depends on whether the structure is designed for yield, ultimate strength, impact or stiffness, and on whether the cavity holds marrow or gas -- four different optima from one geometry.
:::

## Worked examples

**a tube against a solid rod of EQUAL MASS**

```
solid rod radius 1. Tube with bore ratio K = 0.5 and the same cross-sectional area:
  R^2*(1 - 0.25) = 1  ->  R = 1.155
tube:  I = pi*(R^4 - (0.5R)^4)/4 = (pi/4) * 1.778 * 0.9375 = (pi/4) * 1.667
solid: I = (pi/4) * 1
ratio = 1.667

```

- value: `1.667`

- At equal mass the tube is 1.67x stiffer in bending. This is the single most reusable number in the entry and it is exact.

- evidence: **derived**

**scaling a wing spar or fin ray up in span**

```
geometric scaling, d proportional to L : relative sag delta/L grows proportionally to L
constant relative sag             : d must grow as L^1.5

```

- Scaling a beam up geometrically makes it relatively floppier, which is why long spans in organisms -- wing spars, necks, tree branches -- are disproportionately thick or hollow. This is the check that bites on an enlarged fin ray.

- evidence: **derived**

:::{seealso} Contested
- Nothing contests the mechanics. Currey & Alexander 1985 and Taylor & Dirks 2012 differ on what the optimum wall ratio IS, because they optimise different criteria; both are recorded rather than reconciled.
:::

## Sources

| Citation | Read-level |
|---|---|
| Currey JD, Alexander RMcN (1985) J Zool 206:453-468, The thickness of the walls of tubular bones, doi 10.1111/j.1469-7998.1985.tb03551.x | `abstract` |
| Taylor D, Dirks J-H (2012) J R Soc Interface 9:3480, doi 10.1098/rsif.2012.0567 | `full-text` |
| Biewener AA (1990) Science 250:1097-1103, Biomechanics of mammalian terrestrial locomotion, doi 10.1126/science.2251499 | `abstract` |
| Euler-Bernoulli beam formulae are standard textbook results and were not retrieved from a named source here. | `remembered` |


---

*Generated from [`library/laws/second-moment.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/second-moment.yaml). Do not edit this page; edit the YAML.*
