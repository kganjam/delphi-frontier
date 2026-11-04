---
title: Turing reaction-diffusion instability
label: law-turing
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-turing
u_t = f(u,v) + D_u \nabla^2 u, \quad v_t = g(u,v) + D_v \nabla^2 v; \qquad k_c^2 = \frac{D_v f_u + D_u g_v}{2 D_u D_v}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `k_c` | 1/L | 1/m | critical wavenumber -- the first mode to go unstable; the pattern wavelength near onset is about 2*pi/k_c |
| `D_u` | L^2/T | m^2/s | diffusivity of the activator u |
| `D_v` | L^2/T | m^2/s | diffusivity of the inhibitor v |
| `f_u` | 1/T | 1/s | partial derivative of the u-kinetics with respect to u, at the homogeneous steady state |
| `g_v` | 1/T | 1/s | partial derivative of the v-kinetics with respect to v, at the steady state |
| `f_v` | 1/T | 1/s | cross term, entering conditions 2 and 4 |
| `g_u` | 1/T | 1/s | cross term, entering conditions 2 and 4 |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `condition_1` | unknown | f_u + g_v < 0. The steady state is stable WITHOUT diffusion. DERIVED here from the dispersion relation, not retrieved from Turing or Murray. |
| `condition_2` | unknown | f_u*g_v - f_v*g_u > 0. Same reason: the homogeneous state must be stable before diffusion destabilises it. |
| `condition_3` | unknown | D_v*f_u + D_u*g_v > 0. Together with condition 1 this forces f_u and g_v to have OPPOSITE SIGNS and D_v not equal to D_u -- the classical short-range activation, long-range inhibition. |
| `condition_4` | unknown | (D_v*f_u + D_u*g_v)^2 > 4*D_u*D_v*(f_u*g_v - f_v*g_u). The determinant must actually dip below zero for some wavenumber, not merely be able to. |
| `minimum_diffusivity_ratio_two_species` | 4.5 | For the worked example's kinetics, the inhibitor must diffuse at least 4.5 times faster than the activator. The ratio is NOT universal -- it depends on the Jacobian -- but a ratio substantially greater than 1 is forced for any two-species model, and that requirement is what Marcon et al. 2016 remove by adding a third, immobile species. |

## Why it holds

Perturb the homogeneous steady state by exp(lambda*t + i*k*x). The growth rate satisfies det(J - k^2*D) = D_u*D_v*k^4 - (D_v*f_u + D_u*g_v)*k^2 + det(J), and instability needs this to go negative for some k^2. Its minimum sits at the critical wavenumber above. The TRACE stays negative for all k, so instability can only ever come through the determinant -- which is why the four conditions take the form they do, and why diffusion, normally a stabilising process, can destabilise here: it acts on the two species at different rates and so can break the balance that made the uniform state stable.

## Where it holds

- **analysis**: LINEAR stability of a homogeneous steady state
- **species**: exactly two diffusible species, for the conditions as stated
- **output**: whether a given kinetic model is unstable, and the wavelength near onset, about 2*pi/k_c
- **notes**: This is a check on a MODEL, not on an organism. It takes a Jacobian and two diffusivities and returns a yes or no with a length scale, exactly and derivably. That is why it is constraining, and the restriction is what it is constraining ABOUT.


:::{danger} Where it breaks
LINEAR INSTABILITY IS NEITHER NECESSARY NOR SUFFICIENT FOR A PATTERN TO FORM. Subcritical patterns arise where the linear analysis says the state is stable, so a negative result does not exclude patterning and a positive one does not establish it -- this is the repository's own hard-learned rule, and it is the single most important line in the entry. The unequal-diffusivity requirement, the part of Turing's result everyone remembers, holds for TWO-SPECIES MODELS ONLY: Marcon et al. 2016 show that in the presence of cell-autonomous (immobile) factors, networks can pattern with equally diffusing signals and indeed for any combination of diffusion coefficients, and they add that realistic systems use mechanisms fundamentally different from short-range activation and long-range inhibition based on differential diffusivity. So the famous necessary condition is an artefact of the smallest case. Applied to real organisms the limitation is sharper still: of the best-supported biological Turing systems -- mouse digits, where Hox dose modulates the digit wavelength and a Bmp-Sox9-Wnt network drives specification; palatal rugae with FGF and Shh as an activator-inhibitor pair; and Pomanthus angelfish stripes, where Kondo & Asai conclude a reaction-diffusion wave is a VIABLE mechanism, their word -- NONE of the retrieved abstracts supplies the kinetic parameters needed to evaluate conditions 1 to 4 numerically. The check is exact and the inputs for real animals are missing.
:::

## Worked examples

**a two-species model system, not an organism**

```
take f_u = 1, f_v = -1, g_u = 2, g_v = -1.5, D_u = 1, D_v = d
trace J = -0.5 < 0 and det J = -1.5 + 2 = 0.5 > 0   -> stable without diffusion (conditions 1, 2)
condition 3: d - 1.5 > 0            -> d > 1.5
condition 4: (d - 1.5)^2 > 2d, i.e. d^2 - 5d + 2.25 > 0, roots 0.5 and 4.5  -> d > 4.5
at d = 4.5: k_c^2 = (4.5 - 1.5)/9 = 0.333, wavelength = 2*pi/sqrt(0.333) = 10.9 length units

```

- value: `4.5`

- Condition 4 is the binding one -- condition 3 alone would have allowed d > 1.5, a threefold underestimate of the required diffusivity ratio. A design or simulation checked against only the short-range-activation heuristic would pass at d = 2 and never pattern. Per Marcon et al., adding an immobile third species removes the requirement entirely.

- evidence: **derived**

:::{seealso} Contested
- Marcon et al. 2016: the differential-diffusivity requirement is a property of two-species models, not of Turing patterning, and realistic networks use fundamentally different mechanisms. This is a genuine restriction of the classical result rather than a refinement of it.
- Kondo & Asai 1995 describe reaction-diffusion as a VIABLE mechanism for angelfish stripes. The careful wording is preserved: demonstrating that a model can produce the observed pattern is not demonstrating that the organism uses it.
:::

## Sources

| Citation | Read-level |
|---|---|
| Turing AM (1952) Phil Trans R Soc B 237:37-72, The chemical basis of morphogenesis, doi 10.1098/rstb.1952.0012 | `metadata` |
| Gierer A, Meinhardt H (1972) Kybernetik 12:30-39, A theory of biological pattern formation, doi 10.1007/BF00289234 | `metadata` |
| Kondo S, Miura T (2010) Science 329:1616-1620, doi 10.1126/science.1179047 | `abstract` |
| Marcon L, Diego X, Sharpe J, Muller P (2016) eLife 5:e14022, doi 10.7554/eLife.14022, PMC4922859 | `full-text` |
| Sheth R et al. (2012) Science 338:1476-1480, doi 10.1126/science.1226804 | `abstract` |
| Raspopovic J et al. (2014) Science 345:566-570, doi 10.1126/science.1252960 | `abstract` |
| Kondo S, Asai R (1995) Nature 376:765-768, doi 10.1038/376765a0 | `abstract` |
| Economou AD et al. (2012) Nat Genet 44:348-351, doi 10.1038/ng.1090 | `abstract` |
| The four conditions and the critical wavenumber were DERIVED in the source catalogue from the dispersion relation, not read from Turing or Murray. | `remembered` |


---

*Generated from [`library/laws/turing.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/turing.yaml). Do not edit this page; edit the YAML.*
