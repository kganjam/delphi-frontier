---
title: Gompertz growth
label: law-gompertz
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-gompertz
\frac{dN}{dt} = a N e^{-bt} \Rightarrow N(t) = N_0 \exp\left[\frac{a}{b}\left(1 - e^{-bt}\right)\right]
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `N_t` | 1 | dimensionless | size or cell number at time t; dimensionless because the curve is used for counts and for normalised sizes alike |
| `N_0` | 1 | dimensionless | initial size or number |
| `a_g` | 1/T | 1/d | initial specific growth rate |
| `b_g` | 1/T | 1/d | rate at which that specific growth rate decays |
| `t` | T | d | time |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `asymptote` | unknown | DERIVED, exact: the curve approaches N_0*exp(a/b). The ratio a/b is dimensionless, which is why it can sit inside an exponential at all. |
| `half_log_asymptote_time` | unknown | DERIVED: half of the log-asymptote is reached at t = ln(2)/b, independent of a and N_0 -- the same parameter-light invariant that von Bertalanffy has. |

## Why it holds

NONE IS GIVEN, and that is the honest statement. It is an empirical curve whose specific growth rate decays exponentially in time: dN/dt = a*N*exp(-b*t). Gompertz's own use in 1825 was human mortality, not growth at all; Winsor 1932 applied the curve to growth. A function that was invented for one phenomenon and transplanted to another, with no derivation in either, is a fitting family and should be labelled as one.

## Where it holds

- **use**: tumour growth (Laird 1964) and many organism growth curves
- **notes**: It is applied wherever a sigmoid on a log scale is wanted. The domain is therefore a statement about convention rather than about biology. That its tumour fits are Gompertzian is remembered.


:::{danger} Where it breaks
There is no regime where it is derived to hold, so there is no regime where it can be said to break -- which sounds like strength and is the opposite. A curve family with two free parameters plus an initial value will fit most monotone saturating data, so a good fit is close to uninformative: the only meaningful question is whether it fits BETTER than the logistic or von Bertalanffy alternatives on the same data, and no retrieved source tests that here. Because it is not derived, its parameters a and b do not correspond to measurable biological rates, so they cannot be predicted from physiology, compared across studies with different sampling, or used to constrain a design. Fitting it and reporting a and b is a description of the data, and extrapolating it beyond the sampled interval has no justification at all.
:::

## Worked examples

**illustrative parameters -- no fitted values for any system were retrieved**

```
a = 1, b = 0.2
asymptote = N_0 * e^(a/b) = N_0 * e^5 = 148 * N_0
half of the log-asymptote when 1 - e^(-0.2 t) = 0.5, i.e. t = ln(2)/0.2 = 3.47 time units

```

- value: `3.47`

- Note that a 5-fold change in the dimensionless ratio a/b produces a 148-fold change in the asymptote. The curve's output is exponentially sensitive to a ratio of two fitted rates, which is a further reason not to extrapolate it.

- evidence: **derived**

:::{seealso} Contested
- Logistic and von Bertalanffy growth are the standard alternatives. Which fits best is a per-dataset empirical question and no retrieved source settles it; the three are preserved as a choice the analyst must make and justify, not as a ranking.
:::

## Sources

| Citation | Read-level |
|---|---|
| Gompertz B (1825) Phil Trans R Soc Lond 115:513-583, On the nature of the function expressive of the law of human mortality, doi 10.1098/rstl.1825.0026 | `metadata` |
| Winsor CP (1932) PNAS 18:1-8, The Gompertz curve as a growth curve, doi 10.1073/pnas.18.1.1 | `metadata` |
| Laird AK (1964) Br J Cancer 18:490-502, Dynamics of tumour growth, doi 10.1038/bjc.1964.55 | `metadata` |


---

*Generated from [`library/laws/gompertz.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/gompertz.yaml). Do not edit this page; edit the YAML.*
