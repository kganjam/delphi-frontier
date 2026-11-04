---
title: Measured maximum lift coefficient of thin plates at Re 1e3-1e4
label: law-lift-coefficient-lowre
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-lift-coefficient-lowre
F_{L,\max} = \tfrac{1}{2}\,\rho\,U^{2}\,S\,C_{L,\max}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `F_Lmax` | M*L/T^2 | N | largest steady lift the wing can make at speed U, reached at the stall angle |
| `rho` | M/L^3 | kg/m^3 | fluid density |
| `U` | L/T | m/s | free-stream speed relative to the wing (translating, not revolving) |
| `S` | L^2 | m^2 | planform area of the wing (chord x span for a rectangle) |
| `C_Lmax` | 1 | dimensionless | maximum steady lift coefficient over angle of attack. It is a MEASURED property of one geometry at one Re and one kind of motion. |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `CLmax_thin_airfoil_Re1e4` | 0.8 dimensionless | MEASURED by Okamoto, Yasuda & Azuma (1996), but we hold it only SECONDHAND. Cheng & Sun (2016), read in full text, write "at Re = 10^4 the maximum lift coefficient of a thin airfoil is about 0.8", citing Okamoto et al. The word they use is "thin airfoil", not "flat plate". The 1996 abstract says the authors varied camber, thickness, leading-edge sharpness and roughness. Which of those sections the 0.8 belongs to is UNKNOWN to us, and so are its aspect ratio and its uncertainty. That is why the interval is `unknown`. We tried Europe PMC (it has the abstract only) and the journal site (sign-in wall). |
| `CLmax_Sympetrum_isolated_wing` | 1.07 dimensionless | MEASURED (Wakeling & Ellington 1997, abstract) on isolated real wings of the dragonfly Sympetrum sanguineum in steady air flow at Re 700-2400. These are corrugated insect wings, not plates. The band only partly overlaps this entry's, at its lower edge. The abstract gives no uncertainty. |
| `CLmax_Calopteryx_isolated_wing` | 1.15 dimensionless | MEASURED, same study, same conditions, on the damselfly Calopteryx splendens. We keep it separate from the 1.07. The two values are two species, not one estimate with an error bar, and we have not averaged them. |
| `CL_Sympetrum_free_glide_max` | 0.93 dimensionless | CALCULATED by Wakeling & Ellington (1997) from FILMED glide paths of free-flying S. sanguineum, using the stretches where acceleration could be treated as constant. It is the highest CL they recorded, not a CL_max. In the authors' words it "is not necessarily the maximum possible from the wings". |
| `revolving_over_translating_ratio` | 2 dimensionless | Kruyt et al. (2015), full text, MEASURED on a wing spinner with cambered (6%) carbon-fibre plates at Re 5000-25000. They write that the revolving-wing lift coefficient "is two times higher than found for with translating wings", citing Dickinson et al. 1999, Lentink & Dickinson 2009 and Okamoto & Azuma 2011. The "two" is their round figure. They give no interval, and the text does not give their own CL_max number, which appears only in a figure we could not read. |

## Why it holds

At Re 1e3-1e4 the boundary layer on a thin plate is laminar and cannot survive the suction peak at a sharp leading edge. Past a few degrees of incidence the flow separates at the leading edge. Lift then comes from a separated shear layer and leading-edge vortex, not from attached flow with leading-edge suction. CL_max is set by how long that separated region stays close to the surface before it is shed. On a translating wing it is shed, and CL saturates near 1 or below in the values quoted here. On a revolving or flapping wing, rotational (centripetal and Coriolis) accelerations keep the vortex attached. Lentink & Dickinson (2009) state this from force measurements and flow visualisation on a robotic fly wing. This is why the same plate at the same Re reaches a much higher CL when it revolves. The source attributions are the authors' own. The claim that the separation physics dominates and the section shape matters less is our inference from Kesel (2000), Usherwood & Ellington (2002a) and Sunada et al. (1997). Those sources do not agree on how much section shape matters; see contested_by.

## Where it holds

- **reynolds range**: 1e3 to 1e4, based on chord
- **motion**: steady translation (fixed wing in a wind or water tunnel, or a glide). NOT revolving, flapping or pitching.
- **geometry**: thin plates and thin sections (thickness a few percent of chord) with a sharp or thin leading edge. The 0.8 anchor's exact section is unknown.
- **aspect ratio**: not established. The anchor value's aspect ratio is unknown, and low-AR plates behave differently (see where_it_breaks).
- **taxa**: insect wings (dragonflies and damselflies); candidate small fish fins used as wings in air
- **notes**: No value here carries a published uncertainty. Treat every number as a magnitude, not a tolerance.


:::{danger} Where it breaks
(1) REVOLVING OR FLAPPING WINGS. A translating CL_max does not transfer to a revolving or flapping wing at the same Re. Kruyt et al. (2015) measured revolving cambered plates at Re 5000-25000 and report a lift coefficient about two times that of translating wings. Usherwood & Ellington (2002b) report high coefficients on revolving mayfly-to-quail wings across Re 1100-26000. Usherwood (2009) measured a flat card revolving at Re 49,000-108,000 and found CL 1.44. That is above this entry's band, so we cite it only for direction. Using a fixed-wing CL_max for a flapping fin under-predicts its lift by roughly a factor of two. Using a revolving value for a glide over-predicts by the same factor. (2) BELOW Re ~1e3. Okamoto, Sasaki, Kamikubo & Fujii (2019) tested aspect-ratio-1 flat plates at Re 1e3-1e4 (read level: search-summary only). They report that the large CL_max at Re 1e4 fell as Re decreased, which they attribute to vortex lift disappearing. We do not have the magnitude of that fall. So the 0.8 at Re 1e4 is probably optimistic near Re 1e3 (our inference from their stated trend). At Re ~100, Cheng & Sun (2016) quote Vogel (1967) for a model fruit-fly wing CL_max of about 0.6. That is also secondhand. (3) LOW ASPECT RATIO (AR about 1 or less). Mizoguchi & Itoh (2013) report that tip vortices raise CL_max on rectangular wings with AR at or below 1.0 at Re of order 1e4 (read level: search-summary). Moscato & Romano (2024) measured an AR-1 flat plate at Re ~1e5 and report stall delayed to 20-25 degrees by tip vortices. A high-AR or 2-D value therefore under-predicts a stubby, fin-like plate. How much it under-predicts at Re 1e3-1e4 is unknown to us. (4) CAMBER AND CORRUGATION. Kesel (2000) measured at Re 7880 and 10000. Her wing profiles "attain much higher lift values than flat plates", but her abstract gives no number. Sunada et al. (1997) report that the best sections at Re 4000 are thin with about 5% camber near mid-chord. A flat-plate value is therefore a low estimate for a cambered or corrugated fin. The 0.8 itself may come from a cambered section, so it may not be a flat-plate value at all. (5) NOT COVERED: flexible or membrane fins, wet or partly submerged fins, gusty or turbulent free streams, and fast pitch-up manoeuvres. We found no data for these cases inside Re 1e3-1e4. Search scope: see search_scope only.
:::

## Worked examples

**Danio rerio candidate wing in air (hypothetical geometry)**

```
U = 2 m/s and chord c = 0.01 m, both taken from reynolds.yaml, so Re = 1333. ASSUMED: two fins, each 0.01 m chord x 0.02 m span, giving S = 4e-4 m^2 (illustrative, not a measured fin), and rho_air = 1.2 kg/m^3. F_Lmax = 0.5 * 1.2 * 2^2 * 4e-4 * C_Lmax = 9.6e-4 * C_Lmax N. C_Lmax = 0.8 gives 7.68e-4 N, which supports 78 mg. C_Lmax = 1.07 gives 1.03e-3 N (105 mg). C_Lmax = 1.15 gives 1.10e-3 N (113 mg).

```

- value range: `[0.000768, 0.0011]`

- CALCULATED, not observed. It shows how the answer depends on which "measured" value is used. The range of about 45% comes from geometry (a thin section vs real corrugated wings). It is not measurement noise. The 0.8 was measured at Re 1e4, roughly 7 times this Re, and by (2) above it is probably high here (our inference). For a fish whose mass needs a CL near or above 1 at this speed and area, the steady-glide case is NOT supported by any value in this entry.

- evidence: **derived**

**Sympetrum sanguineum (free glide)**

- value: `0.93`

- The highest glide CL that Wakeling & Ellington CALCULATED from filmed free glides. It is close to the isolated-wing tunnel value of 1.07, which suggests that gliding dragonflies operate near their steady CL_max. That reading is our inference; the authors say only that 0.93 is not necessarily the maximum.

- evidence: **literature**

:::{seealso} Contested
- SECTION SHAPE: Okamoto et al. (1996) and Sunada et al. (1997) report that camber, thickness and leading-edge sharpness change the low-Re characteristics, and Kesel (2000) reports that profiled sections give much more lift than flat plates. Usherwood & Ellington (2002a) report that on REVOLVING wings the force coefficients are 'remarkably unaffected by considerable variations in leading-edge detail, twist and camber'. The two sets of results come from different kinds of motion. We have not tested whether motion alone explains the difference, so we leave it open.
- Re DEPENDENCE: Okamoto et al. (2019), read as a search summary only, report that the AR-1 flat plate's CL_max falls as Re drops from 1e4 to 1e3. Lentink & Dickinson (2009), revolving fly wings, report that the LEV-stabilising mechanism does not depend on Re over 100 < Re < 14,000. Kruyt et al. (2015) report CL_max similar for all aspect ratios independent of Re over 5000-25000 (revolving). These disagree on whether Re matters in this band. They also differ in motion: translating in the first, revolving in the other two.
- ASPECT RATIO: search snippets that describe Okamoto & Azuma (2011) contradict each other. One says low-AR wings gave a large CL_max, another says CL_max drops significantly as AR falls. We could not access the paper, so the disagreement is recorded unresolved.
:::

## Sources

| Citation | Read-level |
|---|---|
| Cheng X, Sun M (2016) Wing-kinematics measurement and aerodynamics in a small insect in hovering flight. Sci. Rep. 6:25706. doi:10.1038/srep25706 (PMC4863373) | `full-text` |
| Okamoto M, Yasuda K, Azuma A (1996) Aerodynamic characteristics of the wings and body of a dragonfly. J. Exp. Biol. 199(2):281-294. doi:10.1242/jeb.199.2.281 | `abstract` |
| Wakeling JM, Ellington CP (1997) Dragonfly flight. I. Gliding flight and steady-state aerodynamic forces. J. Exp. Biol. 200(3):543-556. doi:10.1242/jeb.200.3.543 | `abstract` |
| Kesel AB (2000) Aerodynamic characteristics of dragonfly wing sections compared with technical aerofoils. J. Exp. Biol. 203(20):3125-3135. doi:10.1242/jeb.203.20.3125 | `abstract` |
| Sunada S, Sakaguchi A, Kawachi K (1997) Airfoil section characteristics at a low Reynolds number. J. Fluids Eng. 119(1):129-135. doi:10.1115/1.2819098 | `search-summary` |
| Sunada, Yasuda, Yasuda, Kawachi (2002; initials not verified) Comparison of wing characteristics at an ultralow Reynolds number. J. Aircraft 39(2):331-338. doi:10.2514/2.2931 | `search-summary` |
| Okamoto, Sasaki, Kamikubo, Fujii (2019; initials not verified) Disappearance of vortex lift in low-aspect-ratio wings at very-low Reynolds numbers. Trans. JSASS 62(6):310-317 | `search-summary` |
| Mizoguchi, Itoh (2013; initials not verified) Effect of aspect ratio on aerodynamic characteristics at low Reynolds numbers. AIAA J. 51 (issue and pages not verified) | `search-summary` |
| Okamoto M, Azuma A (2011) Aerodynamic characteristics at low Reynolds number for wings of various planforms. AIAA J. 49 (issue and pages not verified) | `listing` |
| Usherwood JR, Ellington CP (2002a) The aerodynamics of revolving wings I. Model hawkmoth wings. J. Exp. Biol. 205(11):1547-1564. doi:10.1242/jeb.205.11.1547 | `abstract` |
| Usherwood JR, Ellington CP (2002b) The aerodynamics of revolving wings II. Propeller force coefficients from mayfly to quail. J. Exp. Biol. 205(11):1565-1576. doi:10.1242/jeb.205.11.1565 | `abstract` |
| Usherwood JR (2009) The aerodynamic forces and pressure distribution of a revolving pigeon wing. Exp. Fluids 46(5):991-1003. doi:10.1007/s00348-008-0596-z (PMC3380271) | `full-text` |
| Kruyt JW, van Heijst GF, Altshuler DL, Lentink D (2015) Power reduction and the radial limit of stall delay in revolving wings of different aspect ratio. J. R. Soc. Interface 12:20150051. doi:10.1098/rsif.2015.0051 (PMC4387534) | `full-text` |
| Lentink D, Dickinson MH (2009) Rotational accelerations stabilize leading edge vortices on revolving fly wings. J. Exp. Biol. 212:2705-2719. doi:10.1242/jeb.022269 | `abstract` |
| Nabawy MRA, Crowther WJ (2017) The role of the leading edge vortex in lift augmentation of steadily revolving wings: a change in perspective. J. R. Soc. Interface 14:20170159. doi:10.1098/rsif.2017.0159 (PMC5550969) | `full-text` |
| Moscato G, Romano GP (2024) Biomimetic wings for micro air vehicles. Biomimetics 9(9):553. doi:10.3390/biomimetics9090553 (PMC11430248) | `full-text` |
| Vogel S (1967) Flight in Drosophila. III. Aerodynamic characteristics of fly wings and wing models. J. Exp. Biol. 46:431-443 | `listing` |


---

*Generated from [`library/laws/lift-coefficient-lowre.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/lift-coefficient-lowre.yaml). Do not edit this page; edit the YAML.*
