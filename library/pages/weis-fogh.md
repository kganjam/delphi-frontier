---
title: Weis-Fogh clap and fling, and the measured lift augmentation at low Reynolds number
label: law-weis-fogh
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-weis-fogh
\Gamma = g(\phi)\,\Omega\,c^{2}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `Gamma` | L^2/T | m^2/s | bound circulation on EACH wing as the fling opens; equal and opposite on the two wings |
| `g_phi` | 1 | dimensionless | Lighthill's inviscid shape factor, a function of the opening angle phi between the wings; 0.69 at phi = 2*pi/3 (120 degrees) |
| `Omega` | 1/T | rad/s | angular velocity at which the wings rotate apart about their trailing edges |
| `c` | L | m | wing chord |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `g_lighthill_120deg` | 0.69 dimensionless — *calculated* | CALCULATED, not measured. Lighthill (1973) inviscid potential-flow analysis of two plates opening at constant Omega: circulations of -0.69*Omega*c^2 and +0.69*Omega*c^2 on the two wings, at an opening angle of 120 degrees (the angle is taken from Crowdy 2009 as relayed by a search summary). No interval exists because it is a theoretical coefficient. Maxworthy (1979) reports measured fling circulation "substantially larger" than the inviscid value; no numeric ratio was found (scope: one web search, Nov 2026; the Cambridge pages were not opened). So 0.69 is neither a bound nor a prediction of real circulation. |
| `encarsia_required_CL` | unknown (interval 2 to 3) dimensionless — *estimated* | Weis-Fogh (1973, summary): for Encarsia formosa at Re 10-20 "the high lift coefficient of 2 or 3 is not possible with steady-state aerodynamics". This is the author's quick ESTIMATE from filmed kinematics, not a force measurement. It is the deficit the mechanism was proposed to fill. |
| `encarsia_reynolds` | unknown (interval 10 to 20) dimensionless — *estimated* | Weis-Fogh 1973, summary. |
| `max_angular_separation_for_benefit_robot` | unknown (interval 10 to 12) degrees — *measured-physical-model* | MEASURED on a dynamically scaled robotic Drosophila wing pair, Re 100-200 (Lehmann, Sane & Dickinson 2005, abstract): lift enhancement "requires an angular separation between the two wings of no more than 10-12 degrees". A robot, not a flying animal. |
| `max_wing_gap_for_benefit_MAV` | 1.2 chords (minimum wing-to-wing distance) — *measured-physical-model* | Phan, Au & Park (2016), flexible-wing two-winged MAV at Re ~15,000: the clap-and-fling effect was insignificant once the minimum distance between the wings exceeded 1.2 chords (paraphrase of the paper, read through an automated summarising fetch). Whether this came from the load-cell measurement, the CFD, or both was not established in this reading. Expressed in chords, not in degrees, so it is not directly comparable with the 10-12 degree robot figure. |
| `lift_augmentation_robot_Re100_200` | unknown (interval 0 to 0.17) fraction of total lift — *measured-physical-model* | MEASURED, Lehmann et al. 2005 (abstract): clap-and-fling "augmented total lift production by up to 17%" and the effect "depended strongly on stroke kinematics". The lower bound 0.0 is MY placeholder for "kinematics-dependent"; the abstract gives no minimum. |
| `vertical_force_augmentation_robot_Re134` | unknown (interval 0.014 to 0.174) fraction of vertical force — *measured-physical-model* | MEASURED, Lehmann & Pick (2007, abstract; Re ~134 from the methods): minimum 1.4 per cent and maximum 17.4 per cent across figure-eight stroke patterns, and augmentation "significantly decreased with increasing vertical force production" -- the stroke that already lifts most gains least. |
| `vertical_force_augmentation_MAV_Re15000_measured` | 0.162 fraction of mean vertical force — *measured-physical-model* | MEASURED with a 6-axis load cell, mean of more than 10 tests, flexible-wing MAV at Re ~15,000 (Phan, Au & Park 2016): 116.7 mN with clap-and-fling against 100.4 mN without; 116.7/100.4 = 1.162 (ratio recomputed by me). The "without" condition was produced by widening the spacing of the two flapping axes from 16 mm to 40 mm (1.6 c), so only the wing-wing distance was changed. No interval is stated because none was found in the reading; it is unknown. |
| `vertical_force_augmentation_MAV_Re15000_CFD` | 0.115 fraction of mean vertical force — *calculated* | CALCULATED (3D CFD), same MAV and Re: 120.4 mN against 108.0 mN; 120.4/108.0 = 1.115 (ratio recomputed by me). The same CFD gives an 18.4 per cent rise in horizontal drag over the cycle. The measured (16.2) and computed (11.5) figures disagree by about 5 percentage points; both are kept. |
| `full_clapfling_lift_gain_CFD_Re20` | 0.28 fraction of mean lift coefficient — *calculated* | CALCULATED, 3D Navier-Stokes at Re 20 (Cheng & Sun 2017, as read through an automated summarising fetch of the PMC text): full clap-fling raised mean CL about 28 per cent while mean CD roughly doubled. Partial clap-fling raised mean CL about 12 per cent; the drag wording for the partial case was garbled in the extracted text and is not used. |
| `full_clapfling_lift_gain_CFD_range` | unknown (interval 0.2 to 0.7) fraction of mean lift coefficient — *calculated* | CALCULATED. Range attributed by the introduction of Cheng & Sun (2017) to Miller & Peskin (2005) and Sun & Yu (2006), "depending on the wing kinematic model". I did not read Sun & Yu (2006). |
| `fling_drag_ratio_rigid_Re10` | unknown (interval 1 to 10) ratio to drag without wing-wing interaction — *calculated* | CALCULATED, 2D immersed-boundary simulation at Re 10 (Miller & Peskin 2009, abstract and introduction): fling drag with rigid wings "can be up to 10 times larger" than without wing-wing interaction; flexibility cut the maximum fling drag by about 50 per cent. The lower bound 1 (no penalty) is mine, not the paper's. |

## Why it holds

Weis-Fogh (1973) filmed the chalcid wasp Encarsia formosa bringing its wings together at the top of the stroke (the clap) and then opening them about their trailing edges like a book (the fling), and claimed the fling as "a hitherto undescribed mechanism for creating lift". Lighthill (1973) supplied the inviscid argument: Kelvin's theorem forbids a net circulation around a body set moving from rest, but once the closed pair splits into two bodies, each can carry an equal and opposite circulation, so bound circulation -- and therefore lift once the wings translate (Kutta-Joukowski, rho*U*Gamma per unit span) -- exists from the start of the stroke without the Wagner delay of a single wing shedding its starting vortex. Air drawn into the opening gap sets Gamma = g(phi)*Omega*c^2 on each wing. Maxworthy (1979, search-summary) reports that in experiments a leading-edge separation vortex carries virtually all of the fling circulation and that it is substantially larger than the inviscid figure, so the carrier of the circulation in real flows is viscous separation, not Lighthill's potential flow. The equation is therefore a scaling statement -- circulation grows as Omega*c^2 -- with an inviscid coefficient attached, not a calibrated predictor.

## Where it holds

- **regime**: hovering or slow flight with a dorsal stroke reversal at which the two wings meet or nearly meet
- **reynolds min**: 4
- **reynolds max**: 15000
- **geometric condition**: wings within 10-12 degrees at reversal (robot, Re 100-200) or within 1.2 chords (MAV, Re ~15,000)
- **taxa**: ['Encarsia formosa (Weis-Fogh 1973)', 'thrips (Re 4.9-35 from measured wings, Santhanakrishnan et al. 2014)', 'flapping micro air vehicles (Phan et al. 2016) -- an engineered device, not a taxon']
- **notes**: The Re bounds are the SPAN OF THE EVIDENCE I FOUND, not a validity limit any author states: Re 4-10 (Santhanakrishnan et al. 2014, 2D porous-wing simulation), 8-128 (Miller & Peskin 2005, 2D simulation, range as recorded in the earlier repository entry; the abstract I read names Re 32 and 64 as the break points), 20 (Cheng & Sun 2017, 3D simulation), 10-20 (Weis-Fogh's estimate), ~134 and 100-200 (robots, Lehmann & Pick 2007; Lehmann et al. 2005), and ~15,000 (flexible-wing MAV, measured and CFD, Phan et al. 2016). The span between Re ~200 and ~15,000 is EMPTY of evidence in what I read (scope stated under where_it_breaks). An earlier version of this entry set reynolds_max 200; that bound was contradicted by Phan et al. 2016 (repository challenge 51) and is replaced here.


:::{danger} Where it breaks
(1) THE Re TREND IS CONTESTED, AND THE MIDDLE IS EMPTY. In 2D simulation, Miller & Peskin (2005, abstract) find that for Re >= 64 lift is enhanced only during the initial rotation, that for Re <= 32 it is enhanced per wing during rotation as well, and that "lift enhancement increases as Reynolds number decreases". Robots at Re ~134 and 100-200 measured 1.4-17.4 per cent. But a flexible-wing MAV at Re ~15,000 MEASURED +16.2 per cent mean vertical force (CFD +11.5 per cent) (Phan et al. 2016) -- no smaller than the robot figures two orders of magnitude lower in Re. So "the gain fades with Re" is true inside the 2D rigid-plate simulations and is NOT supported as a general rule. My inference: the difference may lie in flexibility, 3D flow or stroke amplitude rather than in Re, but no source I read isolates which, so the trend is recorded as contested, not resolved. Between Re ~200 and ~15,000 I found NO measured or computed whole-cycle augmentation (scope: the journal pages and PMC text listed under sources plus one web search, 4 Nov 2026; DelFly "clap-and-peel" work at Re ~1e4 is reported by the repository's challenge 51 at search-summary level only and is not used here). (2) THE GEOMETRY CONDITION IS HARD. Benefit requires the wings to come within 10-12 degrees (robot) or within 1.2 chords (MAV); beyond that the measured effect vanishes. A wing pair that does not nearly meet at reversal gets nothing from this entry, whatever its Re. This is the one part a design can be checked against, and the two thresholds are in different units from different devices. (3) BELOW Re ~10 LIFT IS BOUGHT WITH DRAG -- calculated, not observed. Rigid-wing fling drag reaches up to 10x the no-interaction value at Re 10 (Miller & Peskin 2009) and "an order of magnitude larger" than a single wing (Santhanakrishnan et al. 2014); Cheng & Sun (2017) compute mean CD roughly doubling for a +28 per cent lift gain at Re 20. A lift-only check would approve a motion its own modellers call inefficient. Porous (bristled) and flexible wings reduce the drag in those same simulations, so a solid-plate model misrepresents the animals that actually use the mechanism at this scale. (4) THE INVISCID COEFFICIENT IS NOT THE REAL CIRCULATION. Measured fling circulation exceeds 0.69*Omega*c^2 and is carried by a leading-edge vortex (Maxworthy 1979, search-summary). The equation gives an order of magnitude, never a value to hold a design to. (5) NO AUGMENTATION FIGURE TRANSFERS. Reported gains run from 1.4 to ~70 per cent across robots, 2D and 3D CFD, full and partial claps, rigid, porous and flexible wings, and Re 4 to 15,000. Lehmann & Pick (2007) show the gain FALLS as the stroke's own lift rises. Any single percentage is a property of that study's kinematics, not of the mechanism. (6) SIDE EFFECTS. Lehmann & Pick (2007) measured mean pitching moments reinforced by ~21 per cent, nose-down in most patterns; Phan et al. (2016, CFD) compute an 18.4 per cent rise in horizontal drag. Adopting the clap for lift buys a trim change and a drag cost. (7) NOT THE GENERAL EXPLANATION OF INSECT LIFT. Delayed stall, rotational circulation and wake capture (Dickinson, Lehmann & Sane 1999, as recorded in the earlier repository entry; not re-read here) fill the same quasi-steady deficit without a clap. Large insects mostly do not clap in free flight (Cheng & Sun 2017, introduction, as read by summarising fetch). (8) THIS PROJECT'S WING, Re ~1333 (reynolds.yaml, derived), lies INSIDE THE EMPTY BAND of (1). The gain there is UNKNOWN: bracketed below by 2D simulations predicting little whole-cycle gain above Re 64 and above by a measured +16 per cent at Re ~15,000 on a different, flexible device. Neither "no gain" nor "16 per cent" may be assumed.
:::

## Worked examples

**Encarsia formosa hovering**

- value range: `[2, 3]`

- Required mean lift coefficient ESTIMATED by Weis-Fogh (1973) at Re 10-20, beyond steady-state aerodynamics. A calculation from filmed kinematics, not a force measurement.

- evidence: **literature**

**Flexible-wing two-winged MAV, Re ~15,000 (Phan et al. 2016)**

```
measured: 116.7 mN / 100.4 mN = 1.162  -> +16.2 %   (load cell, >10 tests)
CFD:      120.4 mN / 108.0 mN = 1.115  -> +11.5 %
chord implied by "40 mm = 1.6 c": c = 40/1.6 = 25 mm   [DERIVED by me]
gap threshold 1.2 c = 1.2 * 25 = 30 mm                 [DERIVED by me]

```

- value: `0.162`

- The ratios are my recomputation of the paper's forces. The chord and the 30 mm figure are DERIVED from the paper's own spacing statement, not reported by it. A robot, not an animal.

- evidence: **literature**

**Robotic Drosophila-scale wing pairs, Re ~134 and 100-200**

- value range: `[0.014, 0.174]`

- MEASURED vertical-force / lift augmentation (Lehmann & Pick 2007; Lehmann et al. 2005). Generic stroke kinematics, not those of a flying animal.

- evidence: **literature**

**Danio rerio candidate wing in air (same case as reynolds.yaml)**

```
c = 0.01 m, Omega = 100 rad/s (ASSUMED, no measurement), g = 0.69
Gamma = 0.69 * 100 * 0.01^2 = 6.9e-3 m^2/s
Kutta-Joukowski, rho_air = 1.2 kg/m^3, U = 2 m/s: L' = 1.2 * 2 * 6.9e-3 = 0.0166 N/m
geometric check, IF the MAV threshold transferred: gap <= 1.2 * 10 mm = 12 mm

```

- value: `0.0069`

- DERIVED, not observed. Omega is assumed, the coefficient is inviscid (where_it_breaks 4), and the 12 mm gap transfers a threshold from a 25 mm-chord flexible MAV at Re ~15,000 to a 10 mm wing at Re ~1333 -- an assumption, not a result. The only defensible use is the order of magnitude and the warning in where_it_breaks (8) that the augmentation at this Re is unknown.

- evidence: **derived**

:::{seealso} Contested
- Re trend: Miller & Peskin (2005, 2D simulation) report that lift enhancement increases as Re decreases, with only transient enhancement at Re >= 64; Phan et al. (2016) measured +16.2 per cent (CFD +11.5 per cent) at Re ~15,000 on flexible wings. Recorded, not reconciled.
- Mechanism: Lighthill (1973) derives the fling circulation from inviscid potential flow; Maxworthy (1979) reports that a leading-edge separation vortex carries virtually all of it and that it is substantially larger than the inviscid value.
- Benefit at the smallest scale: Miller & Peskin (2005) read the rising enhancement at low Re as favouring tiny insects; Miller & Peskin (2009) and Santhanakrishnan et al. (2014) find the rigid-wing fling drag up to 10x or an order of magnitude larger at Re ~10; Cheng & Sun (2017) call partial clap-fling 'a more practical choice'. All are simulations.
- Magnitude: measured on robots 1.4-17.4 per cent (Re ~134) and up to 17 per cent (Re 100-200); measured on a MAV 16.2 per cent (Re ~15,000); calculated 11.5 per cent (MAV CFD), 28 per cent (3D CFD, Re 20) and 20-70 per cent (2D/3D CFD as cited by Cheng & Sun 2017). The spread is preserved, not averaged.
- Measurement vs computation on the same MAV: 16.2 per cent measured against 11.5 per cent CFD (Phan et al. 2016).
:::

## Sources

| Citation | Read-level |
|---|---|
| Weis-Fogh T (1973) Quick estimates of flight fitness in hovering animals, including novel mechanisms for lift production. J Exp Biol 59(1):169-230. doi 10.1242/jeb.59.1.169 | `abstract` |
| Lighthill MJ (1973) On the Weis-Fogh mechanism of lift generation. J Fluid Mech 60:1-17. doi 10.1017/S0022112073000017 | `search-summary` |
| Maxworthy T (1979) Experiments on the Weis-Fogh mechanism of lift generation by insects in hovering flight. Part 1. Dynamics of the 'fling'. J Fluid Mech 93:47-63 | `search-summary` |
| Crowdy DG (2009) The spreading phase in Lighthill's model of the Weis-Fogh lift mechanism. J Fluid Mech (volume and pages not verified) | `search-summary` |
| Lehmann F-O, Sane SP, Dickinson MH (2005) The aerodynamic effects of wing-wing interaction in flapping insect wings. J Exp Biol 208:3075-3092. doi 10.1242/jeb.01744 | `abstract` |
| Lehmann F-O, Pick S (2007) The aerodynamic benefit of wing-wing interaction depends on stroke trajectory in flapping insect wings. J Exp Biol 210(8):1362-1377. doi 10.1242/jeb.02746 | `abstract` |
| Miller LA, Peskin CS (2005) A computational fluid dynamics of 'clap and fling' in the smallest insects. J Exp Biol 208(2):195-. doi 10.1242/jeb.01376 | `abstract` |
| Miller LA, Peskin CS (2009) Flexible clap and fling in tiny insect flight. J Exp Biol 212(19):3076-. doi 10.1242/jeb.028662 | `abstract` |
| Santhanakrishnan A, Robinson AK, Jones S, Low AA, Gadi S, Hedrick TL, Miller LA (2014) Clap and fling mechanism with interacting porous wings in tiny insect flight. J Exp Biol 217(21):3898-3909. doi 10.1242/jeb.084897 | `abstract` |
| Cheng X, Sun M (2017) Aerodynamic forces and flows of the full and partial clap-fling motions in insects. PeerJ 5:e3002. PMC5346288 | `full-text` |
| Phan HV, Au TKL, Park HC (2016) Clap-and-fling mechanism in a hovering insect-like two-winged flapping-wing micro air vehicle. R Soc Open Sci 3(12):160746. PMC5210694 | `full-text` |
| Sun M, Yu X (2006) -- cited by Cheng & Sun 2017 for part of the 20-70 per cent range; title and journal not verified | `listing` |
| Dickinson MH, Lehmann F-O, Sane SP (1999) Wing rotation and the aerodynamic basis of insect flight. Science 284:1954-1960. doi 10.1126/science.284.5422.1954 | `listing` |


---

*Generated from [`library/laws/weis-fogh.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/weis-fogh.yaml). Do not edit this page; edit the YAML.*
