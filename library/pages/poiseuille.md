---
title: Hagen-Poiseuille flow in a tube
label: law-poiseuille
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-poiseuille
\Delta P = \frac{8 \mu L Q}{\pi r^4}, \qquad R_h = \frac{8 \mu L}{\pi r^4}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `dP` | M/(L*T^2) | Pa | pressure drop along the tube |
| `mu` | M/(L*T) | Pa*s | dynamic viscosity of the fluid |
| `L` | L | m | tube length |
| `Q` | L^3/T | m^3/s | volume flow rate |
| `r` | L | m | tube radius |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `radius_exponent` | 4 | Exact under the stated assumptions, not a fitted value. It is the load-bearing feature of the law: halving the radius raises resistance sixteenfold, which is why r is the variable every transport network is built around and why Murray's law has the exponent it has. |
| `laminar_reynolds_ceiling` | 2000 | The conventional transition Reynolds number for pipe flow. Above it the parabolic profile is not the solution. |
| `fahraeus_lindqvist_onset` | 0.0003 m | Blood's apparent viscosity becomes appreciably diameter-dependent below roughly 0.3 mm diameter (Farina et al. 2021, a secondary source read at abstract level). Pries et al. 1992 measured tubes from 3.3 to 1978 micrometres; Pries & Secomb 2005 report a distinctive minimum at 6-7 micrometres in glass tubes. |

## Why it holds

It is not a model but the exact solution of the Navier-Stokes equations for steady, fully developed, laminar flow of a Newtonian fluid in a rigid circular tube with a no-slip wall. The velocity profile is parabolic, and integrating it across the section gives the fourth power of the radius. Because it is exact rather than fitted, its failures are always failures of its ASSUMPTIONS, and each one can be named in advance -- which is unusual among the entries here.

## Where it holds

- **flow regime**: steady, fully developed, laminar
- **reynolds max**: 2000
- **fluid**: Newtonian
- **walls**: rigid, no-slip
- **geometry**: circular section, entrance length small compared with L

:::{danger} Where it breaks
Blood in small tubes is the first failure and it is quantitative, not marginal: apparent viscosity depends on diameter (the Fahraeus-Lindqvist effect), with a distinctive minimum at 6-7 micrometres in glass tubes, and resistance in vivo EXCEEDS the in vitro value because of an endothelial surface layer roughly 0.8-1 micrometre thick in 10-40 micrometre vessels. So the law fails in both directions depending on scale, and a design that assumes a single viscosity for a microvascular network is wrong twice over. The second failure is large arteries: flow there is pulsatile, and Reneman & Hoeks state directly that Poiseuille's law does not hold for the arterial system in vivo because of pulsatility. The Womersley number is the discriminator -- for a human aorta it is about 19, meaning the profile is blunt and inertia-dominated rather than parabolic. Compliant walls, bends and entrance regions each break it as well.
:::

## Worked examples

**human aorta -- the case where the law fails, shown by its own diagnostics**

```
inputs (remembered, not retrieved): r = 1.25 cm, rho = 1060 kg/m^3, mu = 3.5 mPa s, HR = 1.2 Hz
mean flow,  U = 0.2 m/s : Re = rho*U*2r/mu = 1060*0.2*0.025/0.0035 = 1514
peak systole, U = 1.0 m/s: Re = 7570                      -- above the laminar threshold
Womersley alpha = r*sqrt(omega*rho/mu), omega = 2*pi*1.2 = 7.54 1/s
  sqrt(7.54*1060/0.0035) = sqrt(2.28e6) = 1511 ; alpha = 0.0125*1511 = 18.9
alpha >> 1  ->  blunt, inertia-dominated profile. Poiseuille's assumptions fail here.

```

- value: `18.9`

- The worked example is deliberately a FAILURE case. Poiseuille gives a number for any tube you hand it, including this one; what tells you not to use it is a separate calculation. That is the general shape of the problem this library exists to address.

- evidence: **derived**

**a vessel of half the radius**

```
R_h ratio = (1/0.5)^4 = 16
```

- value: `16`

- Resistance rises sixteenfold. Exact within the domain.

- evidence: **derived**

:::{seealso} Contested
- Nothing contests the result within its assumptions; it is a derivation, not a regression. What is contested in the literature is how far into the microcirculation a corrected effective viscosity can carry it, rather than whether the uncorrected law applies there.
:::

## Sources

| Citation | Read-level |
|---|---|
| Pries AR, Neuhaus D, Gaehtgens P (1992) Am J Physiol 263:H1770-H1778, Blood viscosity in tube flow: dependence on diameter and hematocrit, doi 10.1152/ajpheart.1992.263.6.H1770 | `abstract` |
| Pries AR, Secomb TW (2005) Am J Physiol Heart Circ Physiol 289:H2657-H2664, doi 10.1152/ajpheart.00297.2005 | `abstract` |
| Reneman RS, Hoeks AP (2008) Med Biol Eng Comput 46:499-507, doi 10.1007/s11517-008-0330-2, PMC2441533 | `full-text` |
| Fahraeus R, Lindqvist T (1931) Am J Physiol 96:562-568 | `remembered` |
| The parabolic-profile derivation is standard textbook material and was not retrieved from a named source in this compilation. | `remembered` |


---

*Generated from [`library/laws/poiseuille.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/poiseuille.yaml). Do not edit this page; edit the YAML.*
