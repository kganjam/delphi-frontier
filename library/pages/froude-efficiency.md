---
title: Froude propulsive efficiency and the Froude number for a surface-piercing body
label: law-froude-efficiency
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-froude-efficiency
\eta_F = \frac{2U}{U + V_j} = \frac{2}{1 + V_j/U} \qquad \mathrm{Fr}_L = \frac{U}{\sqrt{g L_{wl}}}, \quad U_{hull} = \sqrt{\frac{g L_{wl}}{2\pi}} \;\Leftrightarrow\; \mathrm{Fr}_L = \frac{1}{\sqrt{2\pi}} \approx 0.40
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `eta_F` | 1 | dimensionless | useful propulsive power (thrust times speed) divided by the power added to the fluid |
| `U` | L/T | m/s | forward speed of the body |
| `V_j` | L/T | m/s | far-wake jet speed in the body frame; defined only if a steady jet exists |
| `Fr_L` | 1 | dimensionless | length Froude number: ratio of body speed to the speed of a gravity wave on the scale of the waterline length |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `L_wl` | L | m | waterline length of the surface-piercing body (not total length unless the whole body lies along the waterline) |
| `U_hull` | L/T | m/s | hull speed: the speed at which the bow-wave wavelength equals the waterline length |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `hull_speed_froude_number` | 0.399 | DERIVED, not measured. Deep-water gravity waves travel at c = sqrt(g*lambda/(2*pi)); setting the wavelength equal to the waterline length gives Fr_L = 1/sqrt(2*pi) = 0.399. No interval: it is a definition-dependent constant, not an estimate. Gough, Farina & Fish (2015) define hull speed the same way in words (the speed at which the wavelengths of the bow and hull waves equal the waterline length); I have not seen the formula they used. |
| `critical_froude_number_reported` | 0.45 (interval 0.4 to 0.5) | The interval is the SPREAD OF VALUES REPORTED BY DIFFERENT SOURCES, not an uncertainty. 0.45 is Blake & Chan (2007) for Synodontis nigriventris swimming at the surface (the abstract does not state which length it is based on); "approximately 0.5" is Blake (2009) in a review; 0.40 is the derived hull-speed value above. Kjendlie & Stallman (2008) measured adult human swimmers at maximal speed at Fr = 0.42 +/- 0.01 and children at 0.37 +/- 0.01. The sources do not agree on one number and this entry does not pick one. |
| `surface_drag_augmentation_fish` | 2 | Measured, one species. Blake & Chan (2007) report near-surface drag of S. nigriventris as "about double" the deeply submerged drag. No interval retrieved (abstract only). |
| `surface_drag_augmentation_technical_bodies` | 5 | Upper value, reported by Blake & Chan (2007) as "may be five times the deeply submerged values" for streamlined technical bodies of revolution. Secondary sources attribute the factor of five to Hertel (1966); Hertel was not retrieved, so that attribution is unverified here. |
| `wave_drag_vanishing_depth` | 3 body diameters below the surface | Blake & Chan (2007): the depth dependence of drag is similar for fish and technical bodies, "with augmentation vanishing at about 3 body diameters below the surface". No interval retrieved. |
| `pulsed_to_steady_efficiency_ratio_max` | 1.2 | Measured. Moslemi & Krueger (2010): the ratio of pulsed-jet propulsive efficiency to that of an equivalent steady jet reached 1.2 on a self-propelled vehicle at Re 1300-2700, for short pulses (small L/D) and high duty cycle. Interval not given in the abstract. |

## Why it holds

TWO RESULTS SHARE THE NAME FROUDE HERE, AND THEY ARE DIFFERENT QUANTITIES. (1) Froude propulsive efficiency comes from actuator-disc momentum theory. Thrust is the rate of momentum added to the fluid, mdot*(V_j - U). The kinetic energy left in the wake rises as (V_j - U)^2. Dividing useful power by total power gives eta_F = 2/(1 + V_j/U). Efficiency therefore favours accelerating a large mass of fluid by a small amount. The formula is exact WITHIN the theory; what is approximate is the theory (steady flow, a single uniform far-wake jet, no losses on the propulsor itself). (2) The length Froude number compares body speed with the speed of a gravity wave whose wavelength is the body's waterline length. A body piercing the surface makes a bow wave and a stern wave. Near Fr_L = 0.4, the bow wave's wavelength reaches the waterline length. The body then sits in the trough of its own wave and must climb its own bow wave to go faster, so wave drag rises steeply. This is a free-surface effect: it does not exist for a body deep enough that it makes no surface wave.

## Where it holds

- **efficiency**: steady or quasi-steady propulsion with an identifiable far-wake jet whose speed exceeds U
- **froude number**: a displacement body (weight supported by buoyancy) at or within about 3 body diameters of a free surface, in deep water
- **notes**: The hull-speed result assumes deep water. Blake (2009) reports a separate, shallow-water drag rise at Froude numbers of about 0.9. The abstract does not say which length that number is based on, so it must not be compared with Fr_L = 0.4 until the length is known.


:::{danger} Where it breaks
EFFICIENCY. (a) Pulsed jets beat the steady formula, and this is measured, not argued. Moslemi & Krueger (2010) measured pulsed-jet efficiency up to 1.2 times that of an equivalent steady jet. The authors attribute the gain to over-pressure at the nozzle exit while each vortex ring forms, a term that steady momentum theory leaves out. So the formula UNDERESTIMATES a pulsed propulsor; it is not an upper bound on it. (b) For an undulating body with no distinct jet, V_j is undefined. Tytell & Lauder (2004) measured the wake of steadily swimming eels and found it "lacks any significant downstream flow". The authors infer that thrust and drag are balanced along the body. There is no V_j to insert, so the formula cannot be evaluated, which is different from being inaccurate. (c) It prices thrust but does not supply it. eta_F tends to 1 as V_j tends to U, which is also where thrust tends to 0. A design can show eta_F = 0.95 and still be unable to move. (d) It leaves out profile and viscous losses on the propulsor, so it is one factor in a chain and not a whole-animal efficiency. Fish (1984) reports the muskrat's mechanical efficiency as 0.33 and its aerobic efficiency as 0.046. Those are different quantities and must not be compared with eta_F. HULL SPEED. (e) It is not a limit on any body that can generate dynamic lift, all of which have been observed to exceed it. Mallard ducklings burst at 1.73 m/s, which is 4 times predicted hull speed (Aigeldinger & Fish 1995). Common eiders moved 5.5 times hull speed when "steaming" and 6.8 times when paddle-assisted flying (Gough, Farina & Fish 2015). In both cases, the authors say the animals hydroplane or lift the body clear of the water. A planing body is outside the displacement assumption and Fr_L = 0.4 says nothing about it. (f) It does not apply to a submerged body. Wave-drag augmentation vanishes at about 3 body diameters depth (Blake & Chan 2007). S. nigriventris goes deep to exceed the surface-limited speed, which the authors observed. (g) Even for a displacement hull it is a steep drag rise, not a wall. Adult human swimmers reach Fr = 0.42 at maximal speed (Kjendlie & Stallman 2008). (h) The size of the drag rise depends on Reynolds number. Blake (2009) states that smaller, slower forms get relatively less drag augmentation. So the factor of 5 for technical bodies is the wrong number for a fish a few centimetres long; the right number at zebrafish scale is unknown (no measurement retrieved).
:::

## Worked examples

**generic steady propulsor, three jet-speed ratios**

```
V_j/U = 1.5 : eta_F = 2/(1 + 1.5) = 0.800   (excess jet speed 0.5 U)
V_j/U = 2.0 : eta_F = 2/(1 + 2.0) = 0.667   (excess 1.0 U: excess DOUBLED)
V_j/U = 3.0 : eta_F = 2/(1 + 3.0) = 0.500   (excess 2.0 U: excess QUADRUPLED)

```

- value: `0.667`

- Calculated. Doubling the excess jet speed (V_j - U) from 0.5U to 1.0U costs 13.3 efficiency points. Quadrupling it costs 30. An earlier version of this entry (commit aebc0736 on swarm-architecture) called the 30-point case a doubling. Challenge 46 flagged that error, and the arithmetic is redone here.

- evidence: **derived**

**Doryteuthis pealeii paralarvae (1.8 mm mantle length), Re 25-90**

```
measured eta_pd = 0.749 +/- 0.0883 (s.d.)   [Bartol et al. 2009, observation]
IF the steady formula held: V_j/U = 2/eta - 1 = 2/0.749 - 1 = 1.67  [my calculation]

```

- value: `0.749`

- The efficiency is an OBSERVATION (DPIV, deconvolved data). The slip ratio of 1.67 is MY CALCULATION. It inverts a formula that, per where_it_breaks (a), does not strictly hold for pulsed jets, so it is an equivalent steady slip, not a measured jet speed. The authors say the high efficiency "contradicts many studies that predict low propulsive efficiency at intermediate Re".

- evidence: **literature**

**Danio rerio at the surface, total length 0.04 m (project premise)**

```
L_wl taken = 0.04 m (assumption: whole body along the waterline)
U_hull = sqrt(9.81 * 0.04 / (2*pi)) = 0.250 m/s
Fr_L = 0.45 (Blake & Chan)  -> U = 0.45 * sqrt(9.81*0.04) = 0.282 m/s
launch speed 1.95 m/s (project figure, S24) -> Fr_L = 1.95/sqrt(9.81*0.04) = 3.11
                                             -> 1.95 / 0.250 = 7.8 times hull speed

```

- value: `0.25`

- All numbers here are calculated. None is an observation of zebrafish. The design check is this: a surface-taxiing zebrafish at 1.95 m/s would be at 7.8 times hull speed. That is above the largest exceedance observed in the sources retrieved here (eiders, 6.8 times, with the body held out of the water). So no displacement-mode surface swimming can reach launch speed. The speed must come from planing, from propulsion with the body mostly clear of the water, or from a submerged run (deeper than about 3 body diameters) that ends in a breach. The 0.04 m length and the 1.95 m/s are project inputs (docs/research/fish/S24_calcs.py on branch claude/s24-surface-taxiing-launch-tsepbn), not checked by me. Taking L_wl equal to total length is my assumption. A fish partly clear of the water has a shorter waterline and a LOWER hull speed, so the 7.8 is if anything an underestimate.

- evidence: **derived**

**Somateria mollissima (common eider)**

- value: `0.732`

- Hull speed 0.732 +/- 0.046 m/s, which the authors calculated from waterline lengths of museum specimens. Observed speeds were 5.5 times and 6.8 times this. My inference, not the authors' statement: if they used U_hull = sqrt(g*L/(2*pi)), the implied waterline length is 0.343 m.

- evidence: **literature**

:::{seealso} Contested
- Whether hull speed constrains animals at all. Blake (2009) argues that hydrodynamic limits at the critical Froude number 'do not necessarily set biological limitations as most behaviours occur well below the hull speed'. Aigeldinger & Fish (1995) and Gough, Farina & Fish (2015) instead treat hull speed as a real limit that ducks must actively overcome by hydroplaning. These are not reconciled here. Both can be true at once: the limit can be real for burst escape and irrelevant for routine swimming.
- The numerical value of the critical Froude number: 0.40 (derived from wavelength = waterline length), 0.45 (Blake & Chan 2007, catfish), about 0.5 (Blake 2009). Recorded as a spread, not averaged.
- Whether low-Re jetting is inefficient. Moslemi & Krueger (2011) measured average propulsive efficiency falling by 26% as Re fell from 2000 to 50. Bartol et al. (2009) measured squid paralarvae at Re 25-90 with efficiency 74.9%, which they say contradicts predictions of low efficiency at intermediate Re. The two disagree on the absolute level; both report pulsing gaining relative to steady at low Re.
- Froude efficiency and the gait Froude number (froude-gait entry, U^2/(gL)) share a name only. Note also that the gait entry squares the speed and this entry does not: Fr_gait = Fr_L^2 for the same length.
:::

## Sources

| Citation | Read-level |
|---|---|
| Aigeldinger T, Fish FE (1995) J Exp Biol 198(7):1567-1574, Hydroplaning by ducklings: overcoming limitations to swimming at the water surface, doi 10.1242/jeb.198.7.1567 | `abstract` |
| Gough WT, Farina SC, Fish FE (2015) J Exp Biol 218(11):1632 (end page not retrieved), Aquatic burst locomotion by hydroplaning and paddling in common eiders (Somateria mollissima), doi 10.1242/jeb.114140 | `abstract` |
| Blake RW, Chan KH (2007) J Exp Biol 210:2979-2989, Swimming in the upside down catfish Synodontis nigriventris: it matters which way is up, doi 10.1242/jeb.006437 | `abstract` |
| Blake RW (2009) Bioinspir Biomim 4:015004, Biological implications of the hydrodynamics of swimming at or near the surface and in shallow water, doi 10.1088/1748-3182/4/1/015004 | `abstract` |
| Kjendlie PL, Stallman RK (2008) J Appl Biomech 24:35-42, Drag characteristics of competitive swimming children and adults, doi 10.1123/jab.24.1.35 | `abstract` |
| Moslemi AA, Krueger PS (2010) Bioinspir Biomim 5:036003, Propulsive efficiency of a biomorphic pulsed-jet underwater vehicle, doi 10.1088/1748-3182/5/3/036003 | `abstract` |
| Moslemi AA, Krueger PS (2011) Bioinspir Biomim 6:026001, The effect of Reynolds number on the propulsive efficiency of a biomorphic pulsed-jet underwater vehicle, doi 10.1088/1748-3182/6/2/026001 | `abstract` |
| Bartol IK, Krueger PS, Stewart WJ, Thompson JT (2009) J Exp Biol 212:1506-1518, Pulsed jet dynamics of squid hatchlings at intermediate Reynolds numbers, doi 10.1242/jeb.026948 | `abstract` |
| Tytell ED, Lauder GV (2004) J Exp Biol 207:1825-1841, The hydrodynamics of eel swimming: I. Wake structure, doi 10.1242/jeb.00968 | `abstract` |
| Fish FE (1984) J Exp Biol 110:183-201, Mechanics, power output and efficiency of the swimming muskrat (Ondatra zibethicus), doi 10.1242/jeb.110.1.183 | `abstract` |
| Hertel H (1966) -- the factor-of-five surface drag figure as attributed to it by secondary sources; the original was not retrieved | `search-summary` |
| Actuator-disc momentum theory and the deep-water dispersion relation behind hull speed: standard results, written from memory. No primary source (Rankine, W. or R.E. Froude) was retrieved or attempted. | `could-not-access` |


---

*Generated from [`library/laws/froude-efficiency.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/froude-efficiency.yaml). Do not edit this page; edit the YAML.*
