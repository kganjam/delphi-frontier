---
title: Hill force-velocity relation for muscle, and its measured parameters
label: law-hill-muscle
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-hill-muscle
(F + a)(v + b) = (F_0 + a)\,b \quad\Longleftrightarrow\quad \frac{v}{v_{\max}} = \frac{1 - F/F_0}{1 + (F/F_0)/G},\; G = \frac{a}{F_0} = \frac{b}{v_{\max}}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `F` | M*L/T^2 | N | force (load) during steady isotonic shortening |
| `v` | L/T | m/s | steady shortening velocity (in practice reported in muscle or fibre lengths per second, L0/s) |
| `F0` | M*L/T^2 | N | maximum isometric force at the same length and activation |
| `a` | M*L/T^2 | N | Hill force constant; a FITTED parameter, not a measured quantity |
| `b` | L/T | m/s | Hill velocity constant; a FITTED parameter, b = a*v_max/F0 |
| `v_max` | L/T | m/s | unloaded shortening velocity extrapolated from the fitted hyperbola (not the same as slack-test V0) |
| `G` | 1 | dimensionless | curvature constant a/F0 = b/v_max; SMALLER G means a MORE curved relation |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `curvature_G_universal` | unknown (interval 0.066 to 0.49) dimensionless | There is no single measured value of a/F0. The interval is OUR assembly of the extreme means found in the sources read for this entry (rat type 1 and 2A skinned fibres at 12 C, 0.066, Bottinelli et al. 1991; carp red muscle at 10 C, 0.49, Rome & Sosnicki 1990). It mixes species, fibre types, temperatures and preparations, and is a span of reported means, not a confidence interval. A value of 0.25 is often quoted in teaching material; it was NOT found in any source read here, so it is not entered. Hill (1938) full text was not read. |
| `curvature_G_rat_type1_12C` | 0.066 (interval 0.059 to 0.073) dimensionless | Bottinelli et al. 1991; 0.066 +- 0.007 (SEM) |
| `curvature_G_rat_type2A_12C` | 0.066 (interval 0.042 to 0.09) dimensionless | Bottinelli et al. 1991; 0.066 +- 0.024 (SEM) |
| `curvature_G_rat_type2X_12C` | 0.132 (interval 0.124 to 0.14) dimensionless | Bottinelli et al. 1991; 0.132 +- 0.008 (SEM) |
| `curvature_G_rat_type2B_12C` | 0.113 (interval 0.1 to 0.126) dimensionless | Bottinelli et al. 1991; 0.113 +- 0.013 (SEM) |
| `v0_rat_type1_12C` | 0.639 (interval 0.601 to 0.677) L0/s | Bottinelli et al. 1991; 0.639 +- 0.038 (SEM); observed range 0.35-0.95 L0/s. Slack-test V0, not Hill v_max |
| `v0_rat_type2A_12C` | 1.396 (interval 1.312 to 1.48) L0/s | Bottinelli et al. 1991; 1.396 +- 0.084 (SEM) |
| `v0_rat_type2X_12C` | 1.451 (interval 1.385 to 1.517) L0/s | Bottinelli et al. 1991; 1.451 +- 0.066 (SEM) |
| `v0_rat_type2B_12C` | 1.8 (interval 1.691 to 1.909) L0/s | Bottinelli et al. 1991; 1.800 +- 0.109 (SEM). All type 2 fibres had V0 above 0.91 L0/s and fast-type ranges mostly overlapped |
| `curvature_G_carp_red_10C` | 0.49 (interval 0.43 to 0.55) dimensionless | 0.49 +- 0.06 (SEM) |
| `curvature_G_carp_red_20C` | 0.29 (interval 0.23 to 0.35) dimensionless | 0.29 +- 0.06 (SEM); curvature INCREASES (G falls) with temperature in this preparation |
| `v_max_carp_red_10C` | 3.55 (interval 3.29 to 3.81) L0/s | 3.55 +- 0.26 (SEM) |
| `v_max_carp_red_20C` | 5.71 (interval 5.42 to 6) L0/s | 5.71 +- 0.29 (SEM). Same abstract: Q10 of v_max 1.63 +- 0.07; Q10 of isometric tension 1.13 +- 0.02; maximal power 59.7 +- 2.3 W/kg (10 C) and 94.3 +- 3.2 W/kg (20 C), Q10 1.58. |
| `high_force_breakpoint_frog` | 0.784 (interval 0.78 to 0.788) F/F0 | Edman (1988), abstract: 78.4 +- 0.4 % of F0 (mean +- SEM, n = 12), corresponding to 10.9 +- 0.4 % of v_max, Rana temporaria anterior tibialis single fibres, 1-3 C, sarcomere length 2.10 um. The interval is mean +- 1 SEM (our construction from the reported SEM). Other preparations put the break higher: 0.88 F0 in rat medial gastrocnemius in situ (Devrome & MacIntosh 2007, as reported by Alcazar et al. 2019; primary not read) and 0.90 F0 falling to 0.80 F0 after fatigue (Devrome & MacIntosh 2018, as reported by Alcazar et al. 2019; primary not read). |
| `curvature_G_zebrafish` | unknown dimensionless | No force-velocity parameters (a/F0, v_max) for Danio rerio muscle were found. Scope of the negative: one web search ("fish muscle force-velocity Hill curvature Vmax temperature carp scup ... zebrafish muscle fibres Vmax a/P0", Nov 2026), which returned carp, icefish, cod and marlin work and no zebrafish data. No zebrafish-specific search beyond that one was run; not filled from memory or from another teleost. |

## Why it holds

Hill (1938) fitted a rectangular hyperbola to the steady shortening speed of frog sartorius at each afterload and originally identified the force constant a with the coefficient of the heat of shortening (title and listing level for the 1938 paper; its content as reported by Hill 1964 and secondary sources). Hill (1964) himself withdrew that identification: the heat coefficient depends on load (alpha/F0 = 0.16 + 0.18 F/F0 for frog sartorius at 0 C, as given in the abstract) and the 1938 agreement was probably a measurement error making alpha about 30 % too great. Since then the relation has been treated as an empirical description (Abbott & Wilkie 1953, as reported by Seow 2013). The cross-bridge reading (Huxley 1957, as summarised by Seow 2013; Huxley not read) is that speed falls with load because a load lengthens the time each attached bridge must bear strain before it detaches, so fewer bridges are cycling quickly; Seow (2013) shows that a two-state model gives the Hill form under three assumptions that are only approximately true, and argues the curvature carries molecular information. The hyperbola's shape makes power F*v peak at an intermediate load: maximising f(1-f)/(1+f/G) gives f_opt = v_opt/v_max = sqrt(G^2 + G) - G (derived here, not taken from a source), about 0.3 for G near 0.25, consistent with Seow's statement that maximum power occurs at about 0.3 F0.

## Where it holds

- **regime**: steady-state isotonic (or isovelocity) SHORTENING under full, constant activation
- **force range**: about 0.05 to 0.8 F0 (Seow 2013: velocities in this range 'remarkably close' to Hill predictions)
- **taxa**: ['frog', 'mammalian skeletal muscle (rat, cat, human)', 'teleost myotomal muscle (carp, icefish, cod, marlin)']
- **parameter scope**: a, b and v_max belong to one preparation at one temperature, length and activation; they are refitted, not predicted
- **notes**: Edman (1988) reports that changing sarcomere length from 1.85 to 2.60 um left v_max unchanged but progressively reduced curvature, so G is also length-dependent. The law says nothing about force at rest length versus other lengths (that is the separate force-length relation).


:::{danger} Where it breaks
(1) HIGH FORCE, ABOVE ABOUT 0.78-0.90 F0 -- measured. Edman (1988) found the frog-fibre relation is double-hyperbolic, with a break at 78.4 +- 0.4 % F0 (10.9 % v_max) and stronger curvature above it. The break is reported at 0.88 F0 in rat muscle in situ and 0.80-0.90 F0 depending on fatigue (Devrome & MacIntosh 2007, 2018, as reported by Alcazar et al. 2019). Consequence, as reported by Alcazar et al.: a hyperbola fitted to low and middle loads OVERESTIMATES measured isometric force, by 17 % (Edman 1988a), 32 % (Edman 1976, truncated fit) and 13 % (Alcazar 2018b). In carp red muscle the extrapolated zero-velocity load was 1.19 (10 C) and 1.51 (20 C) (Rome & Sosnicki 1990, abstract; our reading is that these are multiples of measured F0, which the abstract text seen did not state). Our inference: F0 taken from a Hill fit must not be used as a holding-force capacity. (2) VERY LOW FORCE, BELOW ABOUT 0.05 F0 -- measured. Single fibres shorten faster than the hyperbola predicts; the Hill v_max underestimates slack-test V0 by about 6-7 % (Edman et al. 1976; Julian et al. 1986, both as reported by Seow 2013). (3) LENGTHENING (F > F0) -- the hyperbola does not continue. Katz (1939) noted lengthening speeds smaller than the hyperbola predicts (as reported by Alcazar et al. 2019; Katz read at listing level only). The isolated-animal-muscle eccentric plateau is about 1.6-1.8 F0 (Edman 1988 delineated the negative branch to 1.6-1.8 F0; Alcazar et al. 2019 summary of animal work), whereas human in vivo eccentric values span 5 % BELOW to 80 % above isometric (Alcazar et al. 2019 compilation, see contested_by). Between 0.90 and 1.20 F0 frog-fibre speed changed by only 1.8 +- 0.3 % of v_max (Edman 1988). (4) NON-STEADY STATE AND HISTORY -- the law holds no memory. After active shortening, isometric force is depressed; after active stretch, it is enhanced (Abbott & Aubert 1952, as described in later reviews; primary read at listing level only). A muscle model that maps instantaneous velocity to force by the Hill relation alone cannot reproduce this. (5) CYCLIC CONTRACTION, WHICH IS HOW LOCOMOTOR MUSCLE ACTUALLY WORKS -- measured. In work-loop experiments (method: Josephson 1985), Askew & Marsh (1998, search-summary level) found the optimal V/v_max for power ranged about fourfold, 0.075 to 0.30, and lay BELOW the optimum predicted from the force-velocity curve, attributed to finite activation and deactivation kinetics and strain. Our inference: a swimming- or flight-power budget computed from Hill Pmax is an upper bound, not an estimate, and can overstate cyclic power at the cycle frequencies an animal uses. (6) MULTI-JOINT HUMAN TASKS -- the measured relation is often closer to LINEAR than hyperbolic (Alcazar et al. 2019 review; e.g. Cuevas-Aburto et al. 2018 bench press, linear vs hyperbolic R^2 0.997 vs 1.000 in one subject). Whole-limb force-velocity mixes several muscles, lever arms and activation limits; it is not the Hill relation of any one muscle. (7) PARAMETERS DO NOT TRANSFER ACROSS TEMPERATURE OR FIBRE TYPE. G spans at least 0.066 to 0.49 in the sources read, and the direction of its temperature dependence differs between sources (contested_by). v_max in carp red muscle rose 61 % from 10 C to 20 C (Rome & Sosnicki 1990). No zebrafish values were found (scope in constants.curvature_G_zebrafish).
:::

## Worked examples

**any muscle with a fitted curvature G (no taxon)**

```
maximise P/(F0*v_max) = f*(1-f)/(1+f/G)  ->  f_opt = sqrt(G^2+G) - G = v_opt/v_max;  G = 0.25 -> f_opt = 0.309, P_max = 0.0955*F0*v_max;  G = 0.066 -> 0.199, 0.0397;  G = 0.49 -> 0.364, 0.1328
```

- value: `0.309`

- value range: `[0.199, 0.364]`

- DERIVED from the equation, not observed. G = 0.25 is an illustrative value, not a measurement. Over the span of G found in the sources (0.066-0.49) the predicted peak-power load moves from 0.20 to 0.36 F0 and the dimensionless peak power changes 3.3-fold, so a power check is only as good as the measured G for the actual muscle and temperature. Note that f_opt equals v_opt/v_max for every G (a property of the hyperbola, derived here).

- evidence: **derived**

**Cyprinus carpio red myotomal muscle, 20 C**

```
G = 0.29, v_max = 5.71 L0/s  ->  f_opt = sqrt(0.29^2+0.29) - 0.29 = 0.322;  v_opt = 0.322*5.71 = 1.84 L0/s;  P_max = 0.1035*F0*v_max
```

- value: `1.84`

- DERIVED by us from the measured G and v_max of Rome & Sosnicki (1990, abstract). It is the shortening speed at which the steady-state Hill fit predicts peak power; it is not a measured optimum. The same paper reports a measured maximal power of 94.3 +- 3.2 W/kg at 20 C. We did not reconcile the two because absolute F0 for these bundles was not in the abstract text seen.

- evidence: **derived**

**mouse skeletal muscle in cyclic (work-loop) contraction (muscle identity as given by citing papers: soleus)**

- value range: `[0.075, 0.3]`

- OBSERVED optimal V/v_max for net power across the cycle conditions tested, maximum net power 94 W/kg (Askew & Marsh 1998, as summarised by search results; full text and abstract not read directly). The authors report it lies below the force-velocity prediction. Compare the derived 0.20-0.36 above.

- evidence: **literature**

:::{seealso} Contested
- Meaning of the constant a: Hill (1938) identified a with the heat-of-shortening coefficient; Hill (1964) reported the two are different quantities and attributed the 1938 agreement to a measurement error of about 30 %. Abbott & Wilkie (1953, via Seow 2013) treat the equation as purely empirical; Seow (2013) argues it encodes cross-bridge kinetics. Not reconciled here.
- Shape: single hyperbola (Hill 1938) vs double hyperbola with a high-force break (Edman 1988; Devrome & MacIntosh 2007, 2018) vs near-linear relations in multi-joint human tasks and in older single-joint data above about 0.4 F0 (Ralston et al. 1949; Abbott & Wilkie 1953 reanalysed; Alcazar et al. 2019). Recorded as a live disagreement about which form to fit.
- Temperature and curvature: in carp red muscle G FELL from 0.49 to 0.29 between 10 and 20 C (Rome & Sosnicki 1990), and in icefish, cod and marlin fast fibres curvature increased with temperature (Johnston & Altringham 1985), yet marlin G was identical at 15 and 25 C (same source, as summarised). Ranatunga (1984, as reported by Seow 2013) found a/F0 INCREASES with temperature in rat EDL and soleus over 10-35 C, the opposite direction. Seow (2013) also states that in some cold-water fish a/F0 is temperature-insensitive. These are different taxa and preparations; the disagreement is preserved, not averaged.
- Eccentric force: isolated animal muscle reaches about 1.6-1.8 F0, while human in vivo studies compiled by Alcazar et al. (2019) range from 5 % below isometric (Webber & Kriellaars 1997) to 80 % above (Cook & McDonagh 1995, 27.6 C). Whether the human deficit is neural inhibition or measurement protocol is not settled in the sources read.
:::

## Sources

| Citation | Read-level |
|---|---|
| Hill AV (1938) The heat of shortening and the dynamic constants of muscle. Proc R Soc B 126:136-195 | `listing` |
| Hill AV (1964) The effect of load on the heat of shortening of muscle. Proc R Soc B 159:297-318. doi:10.1098/rspb.1964.0004 | `search-summary` |
| Edman KA (1988) Double-hyperbolic force-velocity relation in frog muscle fibres. J Physiol 404:301-321. doi:10.1113/jphysiol.1988.sp017291 | `abstract` |
| Bottinelli R, Schiaffino S, Reggiani C (1991) Force-velocity relations and myosin heavy chain isoform compositions of skinned fibres from rat skeletal muscle. J Physiol 437:655-672. doi:10.1113/jphysiol.1991.sp018617 | `abstract` |
| Rome LC, Sosnicki AA (1990) The influence of temperature on mechanics of red muscle in carp. J Physiol 427:151-169. doi:10.1113/jphysiol.1990.sp018165 | `abstract` |
| Seow CY (2013) Hill's equation of muscle performance and its hidden insight on molecular mechanisms. J Gen Physiol 142(6):561-573. doi:10.1085/jgp.201311107 | `full-text` |
| Alcazar J, Csapo R, Ara I, Alegre LM (2019) On the shape of the force-velocity relationship in skeletal muscles: the linear, the hyperbolic, and the double-hyperbolic. Front Physiol 10:769. doi:10.3389/fphys.2019.00769 | `full-text` |
| Johnston IA, Altringham JD (1985) Evolutionary adaptation of muscle power output to environmental temperature [title as given by search results; any subtitle not verified]. Pflugers Arch. doi:10.1007/BF00584534 | `search-summary` |
| Katz B (1939) The relation between force and speed in muscular contraction. J Physiol 96(1):45-64. doi:10.1113/jphysiol.1939.sp003756 | `listing` |
| Abbott BC, Aubert XM (1952) The force exerted by active striated muscle during and after change of length. J Physiol 117(1):77-86 | `listing` |
| Josephson RK (1985) Mechanical power output from striated muscle during cyclic contraction. J Exp Biol 114:493-512 | `search-summary` |
| Askew GN, Marsh RL (1998) Optimal shortening velocity (V/Vmax) of skeletal muscle during cyclical contractions [title as given by search results; any subtitle not verified]. J Exp Biol 201:1527-1540 | `search-summary` |


---

*Generated from [`library/laws/hill-muscle.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/hill-muscle.yaml). Do not edit this page; edit the YAML.*
