---
title: Von Bertalanffy growth
label: law-von-bertalanffy
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-von-bertalanffy
\frac{dL}{dt} = K(L_\infty - L) \Rightarrow L(t) = L_\infty\left(1 - e^{-K(t - t_0)}\right), \qquad \frac{dm}{dt} = \eta m^{2/3} - \kappa m
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `L_t` | L | m | length at time t |
| `L_inf` | L | m | asymptotic length |
| `K` | 1/T | 1/yr | growth coefficient -- the rate at which the gap to L_inf closes |
| `t` | T | yr | age |
| `t_0` | T | yr | nominal age at zero length; a fitting offset, not a biological event |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `half_asymptote_time` | unknown | DERIVED, exact: half of L_inf is reached at t = ln(2)/K, independent of L_inf. A useful invariant, and the only thing in the entry that is not fitted. |
| `anabolism_exponent` | 0.6667 | In the mass form dm/dt = eta*m^(2/3) - kappa*m, anabolism is ASSUMED to scale with surface (m^(2/3)) and catabolism with mass. These exponents are assumptions, and they are exactly the 2/3 versus 3/4 question of the kleiber entry -- so the model's foundation is contested upstream of any fit to data. |
| `fitted_parameters` | unknown | NO ORGANISM'S FITTED K OR L_inf WAS RETRIEVED in this compilation, so the worked example uses illustrative values and demonstrates the arithmetic only. |

## Why it holds

A balance of anabolism against catabolism: build-up assumed proportional to a surface, breakdown proportional to mass. Their difference falls to zero at a finite size, which produces the asymptote. In the length form this reduces to the statement that the growth RATE is proportional to the remaining gap, dL/dt = K*(L_inf - L), which is why the solution is a saturating exponential. The mechanism is therefore an assumption about two exponents rather than a derived result, and the model's success is evidence that growth saturates, not that it saturates for this reason.

## Where it holds

- **growth type**: indeterminate growers, mainly fish
- **life stage**: AFTER maturity
- **notes**: The post-maturity restriction is not a caveat added later; it is where the measured fit holds and where it does not.


:::{danger} Where it breaks
It fails before maturity, which is half the life history and the half a growth model is usually wanted for. Lester, Shuter & Abrams 2004 state that the equation provides a good description of somatic growth AFTER maturity but not before, and attribute the departure to the cost of reproduction -- so the failure has a known cause rather than being unexplained scatter. Day & Taylor 1997 go further in their title alone: von Bertalanffy's growth equation SHOULD NOT BE USED to model age and size at maturity, which is a direct prohibition on one of its common uses (the content of that paper was not retrieved, only the title). Determinate growers -- birds and mammals -- are outside it entirely. And as a class it is a curve family with free parameters: it fits growth after the growth has happened, so agreement with data is weak evidence for the mechanism, and the real question is only ever whether it fits better than the logistic or Gompertz alternatives. No retrieved source tests that comparison here.
:::

## Worked examples

**illustrative parameters -- no fitted values for any species were retrieved**

```
L_inf = 100 cm, K = 0.2 /yr, t_0 = 0
L(5)  = 100*(1 - e^-1) = 63.2 cm
L(10) = 100*(1 - e^-2) = 86.5 cm
half of L_inf at t = ln(2)/0.2 = 3.47 yr

```

- value: `3.47`

- The half-time is independent of L_inf, so it is the parameter-light way to compare two growth curves. Everything else here is illustration.

- evidence: **derived**

:::{seealso} Contested
- West, Brown & Enquist 2001 base ontogenetic growth on allocation of metabolic energy between maintenance of existing tissue and production of new biomass, giving what they call a single parameterless universal curve. Their equation dm/dt = a*m^(3/4)*[1 - (m/M)^(1/4)] is remembered, not retrieved. It rests on the 3/4 exponent, so it inherits the kleiber dispute.
- Lester, Shuter & Abrams 2004 and Day & Taylor 1997 both restrict its legitimate use rather than replacing it.
:::

## Sources

| Citation | Read-level |
|---|---|
| von Bertalanffy L (1938) Hum Biol 10:181 | `remembered` |
| von Bertalanffy L (1957) Q Rev Biol 32:217-231, Quantitative laws in metabolism and growth, doi 10.1086/401873 | `metadata` |
| Lester NP, Shuter BJ, Abrams PA (2004) Proc R Soc B 271:1625-1631, Interpreting the von Bertalanffy model of somatic growth in fishes: the cost of reproduction, doi 10.1098/rspb.2004.2778 | `abstract` |
| Day T, Taylor PD (1997) Am Nat 149:381-393, Von Bertalanffy's growth equation should not be used to model age and size at maturity, doi 10.1086/285995 | `metadata` |
| West GB, Brown JH, Enquist BJ (2001) Nature 413:628-631, A general model for ontogenetic growth, doi 10.1038/35098076 | `abstract` |


---

*Generated from [`library/laws/von-bertalanffy.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/von-bertalanffy.yaml). Do not edit this page; edit the YAML.*
