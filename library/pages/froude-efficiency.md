---
title: Froude propulsive efficiency, and the Froude number of a surface-piercing body
label: law-froude-efficiency
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-froude-efficiency
\eta_F = \frac{2U}{U + V_j} = \frac{2}{1 + V_j/U}, \qquad \mathrm{Fr} = \frac{U}{\sqrt{g L_{wl}}}, \qquad U_{hull} = \sqrt{\frac{g L_{wl}}{2\pi}} \;\Leftrightarrow\; \mathrm{Fr} = \frac{1}{\sqrt{2\pi}} \approx 0.40
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `eta_F` | 1 | dimensionless | Froude (propulsive) efficiency -- useful thrust power T*U divided by the power imparted to the fluid |
| `U` | L/T | m/s | forward speed of the body relative to the undisturbed fluid |
| `V_j` | L/T | m/s | mean speed of the jet or wake far downstream, in the body frame (V_j > U for net thrust) |
| `Fr` | 1 | dimensionless | length Froude number U/sqrt(g*L_wl); ratio of inertial to gravitational (wave-making) effects at a free surface |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `L_wl` | L | m | waterline length of the surface-piercing body (NOT body length for a submerged swimmer, and NOT chest depth) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `froude_hull_speed` | 0.399 (interval 0.35 to 0.5) dimensionless — *derived* | The VALUE is DERIVED, not measured: deep-water gravity waves have wavelength 2*pi*U^2/g, and setting that equal to L_wl gives Fr = 1/sqrt(2*pi) = 0.3989. The INTERVAL IS NOT A CONFIDENCE INTERVAL. It is the band over which wave-making resistance of displacement hulls is described as rising steeply (from about 0.35, continuing to about 0.5), taken from a search-summary of the Wikipedia "Hull speed" article and naval-architecture forum posts -- no primary naval-architecture text was retrieved. Those same secondary sources say the 0.40 figure "varies with hull form". The imperial form 1.34*sqrt(LWL in ft) knots is the same number in different units (1.34 checked by me: sqrt(32.2/2pi)/1.688 = 1.34); sources quoting constants up to 1.51 are quoting a different, hull-form-dependent rule of thumb. |
| `eider_hull_speed` | 0.732 (interval 0.686 to 0.778) m/s — *literature* | Gough, Farina & Fish 2015, Somateria mollissima: 0.732 +/- 0.046 m/s (mean +/- s.d., interval here is +/- 1 s.d., NOT a CI). This is CALCULATED by the authors from waterline lengths of museum specimens, not observed as a speed limit. A 2015 SICB abstract by the same group gives 0.72 +/- 0.05; the journal figure is used. My back-calculation: 0.732 m/s at Fr = 0.399 implies L_wl = 0.343 m. |
| `eider_steaming_froude` | 2.17 dimensionless — *literature* | Gough et al. 2015: steaming eiders averaged 3.99 +/- 1.02 m/s (N = 38), 5.5 times the calculated hull speed, which the authors convert to Fr = 2.17. The SPEED is MEASURED (video); the Froude number is CALCULATED from it. Paddle-assisted flying reached 6.8 times hull speed. Back-calculation (mine): Fr = 2.17 at 3.99 m/s implies L_wl = 0.345 m, consistent with the 0.343 m implied by their hull speed, so the authors used the length Froude number defined above. The SICB abstract gives 5.9 times; the journal figure is used and the discrepancy is not reconciled. |
| `mallard_max_sustained` | 0.71 m/s — *literature* | Prange & Schmidt-Nielsen 1970: the maximum SUSTAINABLE swimming speed of mallards "coincided with" the hull speed of a displacement ship of the same waterline length, 0.33 m. The 0.71 m/s figure is the hull speed as CALCULATED in Aigeldinger & Fish 1995, relayed by search summary; my own recalculation from 0.33 m at Fr = 0.399 gives 0.718 m/s. Minimum cost of transport was at 0.50 m/s (5.77 kcal/kg/km), i.e. at Fr about 0.28 -- below hull speed. Read from abstracts only. |
| `duckling_burst_multiple` | 4 dimensionless — *literature* | Aigeldinger & Fish 1995 (abstract, via search summary): mallard ducklings, mean maximum burst speed 1.73 m/s, "four times greater than the predicted hull speed", achieved by hydroplaning. Gough et al. 2015 cite the SAME paper as 2.7 times. NOT RECONCILED -- see contested_by. My inference only: 4x implies a predicted hull speed of 0.43 m/s and L_wl about 0.12 m; 2.7x implies L_wl about 0.26 m, which is close to an adult mallard rather than a duckling, so the 4x reading is the more internally consistent one. That is arithmetic on a secondary relay, not a reading of the paper. |
| `squid_jet_propulsive_efficiency` | unknown (interval 0.7 to 0.93) dimensionless | NOT ASSERTED AS A SINGLE VALUE. A secondary review (relayed by search summary) attributes 70-93 per cent jet propulsive efficiency in squid to Anderson & Grosenbaugh 2005 and Bartol et al. 2008, 2009, and a whole-cycle value of 49 per cent to Anderson & Grosenbaugh 2005 "recalculated from Anderson & DeMont 2000". None of these tables was read. These are efficiencies computed from PIV wake measurements and models, not directly observed powers. |
| `wave_drag_depth_rule` | 3 (interval 2 to 3) body diameters — *literature* | Depth below which wave drag on a submerged swimmer becomes small: "about 2 to 3 body diameters" (Stokes et al. 2024 PNAS, abstract and press summaries), a theoretical prediction attributed to towing experiments by Hertel (1966), which was NOT retrieved. A figure of "surface drag about 5 times the drag at three body diameters" was seen only as a truncated fragment in a secondary paper and is NOT asserted. Stokes et al. report that non-foraging air-breathing animals from little penguins to pygmy blue whales travel at about this depth (observation, from tags, per the abstract). |
| `human_swimmer_streamline_depth` | unknown | Vennell, Pease & Wilson 2006 (abstract, via search summary), towed mannequin: wave drag below 5 per cent of total for tows deeper than 0.5 m at 1 m/s and 0.7 m at 2 m/s; total drag AT THE SURFACE up to 2.4 times fully-immersed drag; streamline deeper than 1.8 chest depths at Fr = 0.2 and 2.8 chest depths at Fr = 0.42. These are MEASURED on a mannequin, not a swimming human. Their Fr uses a 2.34 m toe-to-fingertip length (my check: 0.9 and 2.0 m/s give Fr = 0.19 and 0.42). |

## Why it holds

TWO MECHANISMS, kept separate because they fail separately.
(1) FROUDE EFFICIENCY is actuator-disc momentum theory. Thrust is the rate of momentum added to the fluid, T = mdot*(V_j - U); the kinetic energy left in the wake is 0.5*mdot*(V_j - U)^2 per unit time in the fluid frame. Useful power T*U over useful-plus-wasted gives 2U/(U + V_j). For a FIXED thrust, efficiency therefore favours accelerating a large mass of fluid a little rather than a small mass a lot. The algebra is exact; the theory it sits in (steady, uniform, inviscid, a well-defined far wake) is the approximation.
(2) THE FROUDE NUMBER of a surface-piercing body measures how fast it moves relative to the waves it makes. A body at the surface generates a gravity-wave system whose wavelength grows as U^2. When that wavelength reaches the waterline length (Fr = 1/sqrt(2*pi), about 0.40) the bow wave and stern wave reinforce, the body sits in a trough of its own making, and wave-making resistance rises steeply. This is a power-cost barrier, not a speed ceiling: a body that can pay the power, or that generates enough dynamic lift to climb out of its own wave (planing), passes through it.
THE LINK between the two: a surface-limited animal that pushes harder near hull speed gains little speed, so it must raise V_j for little gain in U, and eta_F falls. The link is my inference from the two formulas, not a claim taken from any source read here.

## Where it holds

- **flow**: steady, quasi-one-dimensional momentum exchange with a well-defined far wake (for eta_F); a displacement-mode body piercing a free surface in deep water (for the hull-speed Froude number)
- **water depth**: deep relative to wavelength; in shallow water the wave speed is sqrt(g*h) and a different (depth) Froude number governs
- **notes**: eta_F applies to a continuously acting propulsor. Eloy 2012's more general definition, eta = D*U / (D*U + mean shed power), reduces to it in the steady case and is what is used for undulatory swimmers. The hull-speed Froude number applies only while the body is AT the surface: below about 2-3 body diameters it stops governing (see wave_drag_depth_rule).


:::{danger} Where it breaks
FROUDE EFFICIENCY. (a) PULSED JETS: Anderson & DeMont 2000 derived squid-specific jet and whole-cycle efficiency equations and report (abstract) that the Froude equation UNDERESTIMATES jet-period efficiency and OVERESTIMATES whole-cycle efficiency in Loligo pealei -- it is wrong in BOTH directions for the same animal, depending on whether the refill phase is counted, and the refill phase is where most of the loss sits. So for a jetting design, quoting eta_F without stating which period it covers is meaningless. (b) VORTEX-RING FORMATION: Krueger & Gharib 2003 measured (piston-cylinder, force balance) that a starting jet with vortex-ring formation carries more impulse than the jet velocity alone predicts, attributed to nozzle over-pressure; the steady formula therefore misprices pulsed propulsion. Their result is a gain RELATIVE TO A STEADY JET of matched parameters; I have NOT found that it beats the momentum-theory bound itself, and the earlier version of this entry, which said it did, had no source for that and is withdrawn. (c) eta_F prices thrust but does not supply it: eta_F -> 1 as V_j -> U, where thrust -> 0, so a high eta_F is not a sign of a working propulsor. (d) It is blind to viscous and profile losses on the propulsor and to the body's drag, so it is an UPPER BOUND on one term of the budget, never a system or metabolic efficiency.
HULL-SPEED FROUDE NUMBER. (e) IT IS NOT A SPEED LIMIT FOR ANIMALS THAT CAN PLANE. Measured: mallard ducklings burst to about four times predicted hull speed by hydroplaning (Aigeldinger & Fish 1995); common eiders steam at 5.5 times hull speed, Fr = 2.17, and paddle-assisted flying reaches 6.8 times (Gough et al. 2015). The 0.40 barrier holds for SUSTAINED DISPLACEMENT swimming (adult mallards, Prange & Schmidt-Nielsen 1970) and fails for burst planing. (f) IT STOPS APPLYING UNDERWATER: below roughly 2-3 body diameters wave drag becomes small (Stokes et al. 2024; Vennell et al. 2006 measured under 5 per cent of total drag below 0.5-0.7 m on a mannequin), so a fully submerged swimmer is not hull-speed limited at all -- the length that matters for wave drag then becomes DEPTH relative to body thickness, not waterline length. (g) THE 0.40 IS A HUMP, NOT A WALL: secondary naval-architecture sources put the steep rise from about Fr 0.35 to 0.5 and say it varies with hull form; long, slender hulls are routinely driven beyond it with enough power. A design check of "U < 0.40 sqrt(g L)" is therefore a check on POWER COST, and a hard speed claim made from it is an error. (h) SHALLOW WATER changes the governing wave speed to sqrt(g*h) and the length Froude number above is then the wrong group.
:::

## Worked examples

**generic propulsor, three jet-speed ratios**

```
V_j = 1.5*U : eta_F = 2/(1 + 1.5) = 0.800
V_j = 2.0*U : eta_F = 2/(1 + 2.0) = 0.667
V_j = 3.0*U : eta_F = 2/(1 + 3.0) = 0.500
```

- value: `0.8`

- CORRECTED from the previous version of this entry, after challenge 46. The excess jet speed is V_j - U. Going from 1.5U to 3.0U QUADRUPLES the excess (0.5U to 2.0U) and costs 30 points; DOUBLING the excess (0.5U to 1.0U) costs 13.3 points. All three numbers are calculated from the formula, not measured.

- evidence: **derived**

**Anas platyrhynchos, adult, waterline length 0.33 m**

```
U_hull = sqrt(9.81 * 0.33 / (2*pi)) = 0.718 m/s  (Fr = 0.399)
minimum cost of transport at 0.50 m/s  ->  Fr = 0.50 / sqrt(9.81*0.33) = 0.28
```

- value: `0.718`

- Calculated by me from the published waterline length. Prange & Schmidt-Nielsen OBSERVED that the maximum sustainable speed coincided with this limit (abstract). The check passes for sustained displacement swimming.

- evidence: **derived**

**Somateria mollissima (common eider), steaming**

```
L_wl implied by published hull speed: 2*pi*0.732^2/9.81 = 0.343 m
Fr at measured steaming speed: 3.99 / sqrt(9.81 * 0.345) = 2.17  (published value)
```

- value: `2.17`

- The published Fr is reproduced from the published speed, so the definition used here matches the authors'. This is the counterexample to treating 0.40 as a ceiling: the measured speed is 5.5 times the calculated hull speed.

- evidence: **literature**

**Danio rerio-scale surface-piercing body, waterline length 0.03 m (hypothetical design)**

```
U_hull = sqrt(9.81 * 0.03 / (2*pi)) = 0.216 m/s  (about 7 body lengths per second)
```

- value: `0.216`

- Calculated, not observed. A 3 cm body swimming AT the surface and asked to sustain more than about 0.2 m/s in displacement mode is paying the wave-drag hump; the same body two to three body depths down is not. This is the number a design can be checked against, and the where_it_breaks section says when the check stops applying. Zebrafish are not surface swimmers; the scale is chosen only to put the library's recurring design case on this law.

- evidence: **derived**

**Homo sapiens, towed mannequin, 2.34 m toe-to-fingertip length**

```
U_hull = sqrt(9.81 * 2.34 / (2*pi)) = 1.91 m/s
Vennell et al. speeds 0.9 and 2.0 m/s  ->  Fr = 0.19 and 0.42
```

- value: `1.91`

- Calculated by me. Vennell et al.'s upper test speed, 2.0 m/s, sits at Fr = 0.42 -- at the hump -- which is consistent with their measured surface drag of up to 2.4 times submerged drag. That consistency is my inference; the paper (abstract only) does not frame it as hull speed. Whether elite surface swimmers are hull-speed limited was NOT searched and is not claimed.

- evidence: **derived**

:::{seealso} Contested
- DUCKLING BURST MULTIPLE: Aigeldinger & Fish 1995 (abstract) give four times predicted hull speed; Gough, Farina & Fish 2015 cite the same paper as 2.7 times. Both relayed by search summary; neither full text was read. Not reconciled.
- EIDER MULTIPLE: Gough et al. 2015 (journal) give 5.5 times hull speed for steaming; the same group's 2015 SICB abstract gives 5.9 times and a hull speed of 0.72 +/- 0.05 m/s. Not reconciled; the journal figures are used in constants.
- PULSED-JET THRUST AUGMENTATION: Krueger & Gharib report large impulse gains from vortex-ring formation (later fully-pulsed-jet work: up to 90 per cent augmentation as duty cycle approaches 1, per search summary). A 2021 arXiv paper states its findings contradict Krueger & Gharib 2003 and reports lower augmentation; another critic attributes the gap partly to a Reynolds number an order of magnitude higher. Seen only as search summaries; the arXiv paper's authors were not retrieved, so it is not listed as a source. Not reconciled.
- SHARE OF WAVE DRAG IN HUMAN SWIMMING near 2 m/s: about 5 per cent (Vorontsov & Rumyantsev 2000), 21 per cent (Toussaint et al. 2002), up to 60 per cent (Vennell et al. 2006), as tabulated in a Southampton thesis seen by search summary. The definitions differ (active versus passive, depth) and are not reconciled.
- Not contested as mathematics. What is contested in biology is whether a given wake is steady enough for eta_F to apply; see the lighthill entry for the undulatory case, where shed power is computed rather than assumed.
:::

## Sources

| Citation | Read-level |
|---|---|
| Rankine WJM and Froude RE, actuator-disc momentum theory -- standard derivation (dates and venues not retrieved) | `remembered` |
| Eloy C (2012) J Fluids Struct 30:205-218, Optimal Strouhal number for swimming animals, doi 10.1016/j.jfluidstructs.2012.02.008 | `full-text-preprint` |
| Gough W, Farina SC, Fish FE (2015) J Exp Biol 218:1632-1638, Aquatic burst locomotion by hydroplaning and paddling in common eiders (Somateria mollissima), doi 10.1242/jeb.114140 | `search-summary` |
| Aigeldinger TL, Fish FE (1995) J Exp Biol 198:1567-1574, Hydroplaning by ducklings -- overcoming limitations to swimming at the water surface, doi 10.1242/jeb.198.7.1567 | `search-summary` |
| Prange HD, Schmidt-Nielsen K (1970) J Exp Biol 53:763-777, The metabolic cost of swimming in ducks, doi 10.1242/jeb.53.3.763 | `search-summary` |
| Vennell R, Pease D, Wilson B (2006) J Biomech 39:664-671, Wave drag on human swimmers, doi 10.1016/j.jbiomech.2005.01.023, PMID 16439236 | `search-summary` |
| Stokes KL et al. (2024) PNAS, Optimization of swim depth across diverse taxa during horizontal travel, doi 10.1073/pnas.2413768121 | `search-summary` |
| Hertel H (1966) Structure, Form, Movement. Reinhold, New York | `remembered` |
| Anderson EJ, DeMont ME (2000) J Exp Biol 203:2851-2863, The mechanics of locomotion in the squid Loligo pealei -- locomotory function and unsteady hydrodynamics of the jet and intramantle pressure, doi 10.1242/jeb.203.18.2851 | `abstract` |
| Anderson EJ, Grosenbaugh MA (2005) J Exp Biol 208:1125-1146, Jet flow in steadily swimming adult squid, doi 10.1242/jeb.01507 | `search-summary` |
| Bartol IK, Krueger PS, Stewart WJ, Thompson JT (2009) J Exp Biol 212:1889-1903, Hydrodynamics of pulsed jetting in juvenile and adult brief squid Lolliguncula brevis -- evidence of multiple jet modes and their implications for propulsive efficiency, doi 10.1242/jeb.027771 | `search-summary` |
| Krueger PS, Gharib M (2003) Phys Fluids 15:1271-1281, The significance of vortex ring formation to the impulse and thrust of a starting jet, doi 10.1063/1.1564600 | `search-summary` |
| Wikipedia, Hull speed (accessed via search summary 2026-11-04) | `search-summary` |


---

*Generated from [`library/laws/froude-efficiency.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/froude-efficiency.yaml). Do not edit this page; edit the YAML.*
