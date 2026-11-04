---
title: D'Arcy Thompson's theory of transformations
label: law-darcy-thompson
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-darcy-thompson
(x, y) \longmapsto (x', y') \quad \text{by a smooth map; no further constraint is specified}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `x` | L | m | a coordinate on the Cartesian grid drawn over the first form |
| `x_prime` | L | m | the corresponding coordinate on the deformed grid over the second form |
| `J_map` | 1 | dimensionless | the local scale factor of the map -- which the theory does not specify, and that is the entire point |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `free_parameters` | unknown | There are no constants, because there is nothing fitted. The theory asserts that SOME smooth map exists between two related forms. It names no map, no family of maps, and no criterion for choosing one, so there is nothing to measure and nothing to put an interval on. |

## Why it holds

Draw a Cartesian grid over one organism's outline, deform the grid smoothly, and the outline of a related organism appears. Thompson's claim is that differences between related forms are often integrated transformations of the whole rather than independent changes to parts -- a real and influential biological insight about the UNIT of evolutionary change. The quantitative successor is landmark-based geometric morphometrics: Procrustes superimposition and thin-plate splines (Bookstein 1991), which do supply a well-defined map and a measure of its bending energy.

## Where it holds

- **scope**: pairs of related forms that can be put in landmark correspondence
- **notes**: The classic examples are Argyropelecus to Sternoptyx and Diodon to Orthagoriscus (Mola), both remembered rather than retrieved. Note the domain is a statement about when the PICTURE can be drawn, not about when a prediction holds, because there is no prediction.


:::{danger} Where it breaks
It does not break, and that is precisely the problem: a theory that cannot fail cannot inform a design. It shows that a smooth map EXISTS between two forms. It does not say why that map rather than another, it does not constrain which maps are possible or likely, and it makes no prediction that could turn out false -- for any two sufficiently similar outlines some smooth deformation can be drawn, so finding one is not evidence of anything. This entry is in the library as the clearest worked example of the descriptive class, and as a warning: the transformations are visually compelling in a way that reads as explanatory, which is exactly the property that makes them dangerous as a design input. The honest successor is geometric morphometrics, which replaces the existence claim with a specific map and a number; that number is a measure of SHAPE DIFFERENCE and still not a constraint a design can fail.
:::

## Worked examples

**what a check against this law would look like, and why there isn't one**

```
proposed design outline  -> landmark correspondence with a reference species
fit a thin-plate spline  -> some bending energy B results
test: is B too large?    -> NO THRESHOLD EXISTS. Any finite B is permitted by the theory.

```

- The procedure runs to completion and returns a number, which is what makes this trap easy to fall into. The step that is missing is the only one that would matter. Compare the golden angle, which supplies both an exact target AND a measured 18 per cent tolerance, and is therefore constraining.

- evidence: **derived**

:::{seealso} Contested
- Not contested -- there is no claim specific enough to contest. Geometric morphometrics supersedes it as a method without supplying the missing constraint.
:::

## Sources

| Citation | Read-level |
|---|---|
| Thompson DW (1917) On Growth and Form, Cambridge Univ Press, chapter 'On the theory of transformations' | `remembered` |
| Bookstein FL (1991) Morphometric Tools for Landmark Data | `remembered` |


---

*Generated from [`library/laws/darcy-thompson.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/darcy-thompson.yaml). Do not edit this page; edit the YAML.*
