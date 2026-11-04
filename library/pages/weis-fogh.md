---
title: Weis-Fogh clap-and-fling and unsteady lift at low Reynolds number
label: law-weis-fogh
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-weis-fogh
\Gamma = \pm 0.69\, \Omega c^2
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `Gamma` | L^2/T | m^2/s | circulation generated around each wing during the fling |
| `Omega` | 1/T | rad/s | angular velocity of the fling |
| `c` | L | m | wing chord |
| `c_f` | 1 | dimensionless | the coefficient 0.69 from Lighthill's inviscid analysis |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `lighthill_circulation_coefficient` | 0.69 | Lighthill 1973: in the inviscid analysis the circulations around the two wings are -0.69*Omega*c^2 and +0.69*Omega*c^2. Equal and opposite, which is the whole trick -- see mechanism. |
| `encarsia_required_lift_coefficient` | 2.5 (interval 2 to 3) | Weis-Fogh 1973: at the Reynolds number of Encarsia formosa, 10-20, a lift coefficient of 2 or 3 "is not possible with steady-state aerodynamics". This is the DEFICIT the mechanism was proposed to explain, and it is the entry's load-bearing number. |
| `encarsia_reynolds` | 15 (interval 10 to 20) | Weis-Fogh 1973. |
| `wing_wing_lift_augmentation` | 0.17 | Lehmann, Sane & Dickinson 2005, robotic wings: wing-wing interaction augmented total lift by UP TO 17 per cent, and depended strongly on stroke kinematics. It requires an angular separation of no more than 10-12 degrees. The modest size of this number against the factor of 2-3 deficit is the reason this entry is classified descriptive. |
| `required_angular_separation_deg` | 11 (interval 10 to 12) | Lehmann et al. 2005. A real kinematic requirement, but measured on a robot rather than on an animal. |

## Why it holds

At the top of the stroke the wings clap together; they then fling apart by rotating about their trailing edges. Air rushes into the opening wedge and circulation of opposite sign builds around each wing IMMEDIATELY -- without waiting for the starting vortex that the Kutta condition requires in steady theory. Because the two circulations are equal and opposite, total vorticity is conserved and no starting vortex need be shed, so lift is available from the first instant of the stroke rather than after several chord lengths of travel. That is what makes it valuable at Reynolds numbers where a conventional aerofoil cannot build circulation fast enough.

## Where it holds

- **reynolds**: low, order 10-100, where steady aerofoil theory cannot supply the needed lift coefficient
- **taxa**: Weis-Fogh 1973 reports the fling in the normal flight of butterflies and possibly of Drosophila and other small insects, and as a useful mechanism in birds and bats during take-off. Ellington 1984 reports a near fling and partial fling for the ladybird. A 2025 robot modelled on Cynopterus brachyotis found an upstroke clap significantly increases lift at St 0.2-0.4.

- **notes**: Hover-flies and Odonata rely almost entirely on the flip rather than the fling, by the same source. Clapping during pigeon take-off and in thrips is remembered, not retrieved.


:::{danger} Where it breaks
It is not the general explanation of insect lift, and treating it as one is the error to avoid. Dickinson, Lehmann & Sane 1999 name three distinct yet interactive mechanisms -- delayed stall, rotational circulation and wake capture -- none of which is clap-and-fling, and Ellington concludes that most, if not all, hovering animals do not rely on quasi-steady aerodynamics at all. So the deficit this mechanism was invented to fill is real, but several things fill it. The measured benefit is also modest and fragile: at most 17 per cent augmentation, strongly dependent on stroke kinematics, and requiring the wings to approach within 10-12 degrees -- a tolerance a real or designed mechanism must actually hold. Repeated clapping costs wing wear, a cost that is remembered rather than measured here. The reason this entry is DESCRIPTIVE despite carrying numbers: it diagnoses why a quasi-steady calculation under-predicts lift, but it does not return a lift coefficient a design can be checked against, and the one number that is a design tolerance comes from a robot rather than from an animal.
:::

## Worked examples

**Encarsia formosa -- sizing the quasi-steady deficit**

```
required C_L (Weis-Fogh, retrieved)      : 2 to 3
steady C_L achievable at Re 10-20        : about 1   [REMEMBERED, not retrieved]
unexplained factor                        : at least 2

```

- value: `2.5`

- The factor of two is the gap any unsteady mechanism must close. Note the arithmetic rests on a remembered steady C_L of about 1; if that is wrong the factor moves with it. Weis-Fogh also reports specific powers of 1.3 and 4.7 W/N, but the abstract did not say which case each belongs to, so neither is attributed here.

- evidence: **derived**

:::{seealso} Contested
- Dickinson, Lehmann & Sane 1999: delayed stall, rotational circulation and wake capture are the mechanisms they identify, and clap-and-fling is not among the three. This is a competing account of the same deficit and is preserved rather than reconciled.
- Ellington 1984: most, if not all, hovering animals do not rely on quasi-steady aerodynamics -- a statement that the deficit is general rather than specific to the taxa where the fling was observed.
:::

## Sources

| Citation | Read-level |
|---|---|
| Weis-Fogh T (1973) J Exp Biol 59:169-230, Quick estimates of flight fitness in hovering animals, including novel mechanisms for lift production, doi 10.1242/jeb.59.1.169 | `abstract` |
| Lighthill MJ (1973) J Fluid Mech 60:1-17, On the Weis-Fogh mechanism of lift generation, doi 10.1017/S0022112073000017 | `abstract` |
| Ellington CP (1984) Phil Trans R Soc B 305:1-181, The aerodynamics of hovering insect flight I-VI; part VI is doi 10.1098/rstb.1984.0054 | `abstract` |
| Dickinson MH, Lehmann F-O, Sane SP (1999) Science 284:1954-1960, Wing rotation and the aerodynamic basis of insect flight, doi 10.1126/science.284.5422.1954 | `abstract` |
| Lehmann F-O, Sane SP, Dickinson MH (2005) J Exp Biol 208:3075-3092, The aerodynamic effects of wing-wing interaction in flapping insect wings, doi 10.1242/jeb.01744 | `abstract` |
| Fan et al. (2025) J R Soc Interface, doi 10.1098/rsif.2024.0590 | `abstract` |


---

*Generated from [`library/laws/weis-fogh.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/weis-fogh.yaml). Do not edit this page; edit the YAML.*
