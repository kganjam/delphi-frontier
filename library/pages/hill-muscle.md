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
(F + a)(v + b) = (F_0 + a)\,b \quad\Longleftrightarrow\quad \frac{v}{v_{\max}} = \frac{1 - F/F_0}{1 + (F/F_0)/G}, \qquad G = \frac{a}{F_0} = \frac{b}{v_{\max}}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `F` | M*L/T^2 | N | force (afterload) borne during steady isotonic shortening |
| `v` | L/T | m/s | steady shortening velocity; usually reported normalised, in muscle or fibre lengths per second (L0/s) |
| `F0` | M*L/T^2 | N | the zero-velocity INTERCEPT of the hyperbola. In a fit constrained through measured isometric force it equals measured F0; in an unconstrained fit (e.g. Rome & Sosnicki 1990, who call it P0*) it is an extrapolated load that can exceed measured isometric force. Every curvature in `constants` says which one it is normalised to, or that this is unknown. |
| `a` | M*L/T^2 | N | Hill force constant; a FITTED parameter, not separately measured |
| `b` | L/T | m/s | Hill velocity constant; a FITTED parameter, b = a * v_max / F0 |
| `v_max` | L/T | m/s | zero-load velocity extrapolated from the fitted hyperbola; NOT the same quantity as slack-test V0 |
| `G` | 1 | dimensionless | curvature a/F0 = b/v_max; a SMALLER G means a MORE curved relation |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `curvature_G_general` | unknown (interval 0.066 to 0.49) dimensionless — *assembled-from-literature* | There is no single measured value of a/F0. The interval is MY assembly of the extreme MEANS in the sources I read (rat type 1 and 2A skinned fibres at 12 C, 0.066, Bottinelli et al. 1991; carp red muscle at 10 C, 0.49, Rome & Sosnicki 1990). It mixes species, fibre types, temperatures, preparations and normalisations, and is a span of means, not a confidence interval. Individual carp fast fibres span 0.18-0.53 per a search-result snippet whose source paper I did not identify or open, so that range is NOT entered as a constant. The value 0.25 that circulates in teaching material was not found in any source I read and is not entered. |
| `curvature_G_rat_type1_12C` | 0.066 (interval 0.059 to 0.073) dimensionless | MEASURED (fit to measured points). Bottinelli et al. 1991, 0.066 +/- 0.007 (spread type unlabelled). Normalisation of P0: unknown. |
| `curvature_G_rat_type2A_12C` | 0.066 (interval 0.042 to 0.09) dimensionless | Bottinelli et al. 1991, 0.066 +/- 0.024 (spread type unlabelled). |
| `curvature_G_rat_type2X_12C` | 0.132 (interval 0.124 to 0.14) dimensionless | Bottinelli et al. 1991, 0.132 +/- 0.008 (spread type unlabelled). |
| `curvature_G_rat_type2B_12C` | 0.113 (interval 0.1 to 0.126) dimensionless | Bottinelli et al. 1991, 0.113 +/- 0.013 (spread type unlabelled). Note the grouping: types 1 and 2A are the HIGH-curvature group, 2X and 2B the low-curvature group -- curvature does not track speed. |
| `v0_rat_type1_12C` | 0.639 (interval 0.601 to 0.677) L0/s | Bottinelli et al. 1991, 0.639 +/- 0.038 (S.E.M., labelled); observed range 0.35-0.95 L0/s. A slack-test V0, not a Hill v_max. |
| `v0_rat_type2B_12C` | 1.8 (interval 1.691 to 1.909) L0/s | Bottinelli et al. 1991, 1.800 +/- 0.109 (spread type unlabelled). Types 2A and 2X: 1.396 +/- 0.084 and 1.451 +/- 0.066. All type-2 fibres exceeded 0.91 L0/s; the whole population formed a continuum 0.35-2.84 L0/s. |
| `curvature_G_carp_red_10C` | 0.49 (interval 0.43 to 0.55) dimensionless | a/P0* (normalised to the EXTRAPOLATED intercept, not measured isometric force). Rome & Sosnicki 1990. |
| `curvature_G_carp_red_20C` | 0.29 (interval 0.23 to 0.35) dimensionless | a/P0*. Rome & Sosnicki 1990. G FELL (curvature rose) from 10 to 20 C in this preparation; see contested_by. |
| `extrapolated_intercept_carp_red` | unknown | P0* = 1.19 +/- 0.04 (10 C) and 1.51 +/- 0.20 (20 C), Rome & Sosnicki 1990 abstract. The abstract defines P0* as "the extrapolated load at zero velocity" and says the fit was "not constrained to pass through P0 = 1". It does NOT say outright that 1.19 and 1.51 are multiples of measured P0; MY INFERENCE, from the values exceeding 1 next to that sentence, is that they are. |
| `v_max_carp_red_10C` | 3.55 (interval 3.29 to 3.81) L0/s | Rome & Sosnicki 1990, 3.55 +/- 0.26. |
| `v_max_carp_red_20C` | 5.71 (interval 5.42 to 6) L0/s | Rome & Sosnicki 1990, 5.71 +/- 0.29. Same abstract: Q10 of v_max 1.63 +/- 0.07; Q10 of isometric tension 1.13 +/- 0.02; MEASURED maximal power 59.7 +/- 2.3 W/kg (10 C) and 94.3 +/- 3.2 W/kg (20 C), Q10 1.58. |
| `high_force_breakpoint_frog` | 0.784 (interval 0.78 to 0.788) F/F0 | MEASURED. Edman 1988 abstract: break at 78.4 +/- 0.4 % of P0 (n = 12), about 10.9 % of v_max; Rana temporaria single fibres, fused tetani at 1-3 C, sarcomere length 2.10 um. Interval is mean +/- 1 reported spread (my construction). Other preparations, AS REPORTED BY Alcazar et al. 2019 (primaries not read): about 0.80 F0 (Edman 1993, after dantrolene); 0.88 F0 at 7.3 % v_max in rat medial gastrocnemius in situ (Devrome & MacIntosh 2007); 0.90 F0 falling to 0.80 F0 after fatigue (Devrome & MacIntosh 2018). |
| `low_force_vmax_underestimate` | unknown (interval 0.06 to 0.07) fraction of v_max | Hill v_max UNDERESTIMATES the measured unloaded speed by about 6-7 % (Edman et al. 1976; Julian et al. 1986, both AS REPORTED BY Seow 2013; primaries not read). |
| `curvature_G_zebrafish` | unknown dimensionless | No Hill fit for Danio rerio muscle exists in the one source found. Mead et al. 2020 (5-day larval tails, n = 5, mean +/- SD) measured force at imposed shortening speeds up to 6.5 +/- 0.9 L/s and state they "were unable to fully characterize the shape of the force/velocity relationship"; they fitted no equation. Their v_max of about 45 L/s at 28 C is an ESTIMATE, made by assuming the peak work-loop shortening velocity (18.1 L/s) equals 0.4 v_max -- it is not measured. Scope of the negative: one web search (zebrafish muscle force-velocity curvature a/P0 Vmax larval fast fibres, Nov 2026) and one full-text read (first 100000 of 119992 characters) of Mead et al.; adult zebrafish fibres were not searched separately. Not filled from another teleost. |

## Why it holds

Hill (1938) fitted a rectangular hyperbola to the steady shortening speed of frog muscle at each afterload and identified the force constant a with the coefficient of the heat of shortening. That identification did not survive: the heat coefficient was later found to depend on load and speed (Hill 1964, AS REPORTED BY Seow 2013; I could not open Hill 1964 -- HTTP 403), and the equation was long treated as "purely empirical" (Abbott & Wilkie 1953, as quoted by Seow 2013). The cross-bridge reading (Huxley 1957, as summarised by Seow 2013; Huxley not read) is that a load lengthens the time each attached bridge spends bearing strain before it detaches, so fewer bridges cycle quickly; Seow argues the curvature therefore carries molecular information, and Bottinelli et al. 1991 found curvature grouped by myosin heavy-chain isoform. The hyperbola makes power F*v peak at an intermediate load: maximising f(1-f)/(1+f/G) gives f_opt = v_opt/v_max = sqrt(G^2+G) - G. That formula is DERIVED by me from the equation, not taken from a source; it gives about 0.3 for G near 0.25, consistent with Seow's statement that maximum power occurs at about 0.3 Fmax.

## Where it holds

- **regime**: steady-state isotonic (or isovelocity) SHORTENING under full, constant (tetanic) activation
- **force range**: about 0.05 to 0.8 F0 -- Seow 2013: velocities in this range are "remarkably close" to Hill predictions
- **taxa**: ['frog single fibres', 'rat skinned single fibres', 'teleost red myotomal muscle (carp)']
- **parameter scope**: a, b and v_max belong to ONE preparation at one temperature, sarcomere length and activation. They are refitted, never predicted. Edman 1988: lengthening sarcomeres from 1.85 to 2.60 um left v_max unchanged but steadily decreased curvature, so G is length-dependent as well.
- **notes**: Says nothing about isometric force versus length (the separate force-length relation) or about submaximal activation.

:::{danger} Where it breaks
(1) HIGH FORCE, ABOVE ABOUT 0.78-0.90 F0 -- measured. Edman 1988 (abstract): frog fibres show a double-hyperbolic relation with a break at 78.4 +/- 0.4 % P0 and curvature "more pronounced in the high-force region". Seow 2013 places the failure at loads above about 80 % of isometric force. Breaks at 0.88 and 0.80-0.90 F0 in rat in situ are reported by Alcazar et al. 2019 (primaries not read). Consequence, as reported by Alcazar et al.: a hyperbola fitted to low and middle loads OVERESTIMATES measured isometric force -- by 17 % (Edman 1988a), 32 % with data truncated at 78 % P0 (Edman et al. 1976) and 13 % in a multi-joint task (Alcazar et al. 2018b). Rome & Sosnicki's unconstrained carp fit put the intercept at 1.19 and 1.51 (my reading: times measured P0). MY INFERENCE: an F0 taken from a Hill fit must never be used as a holding-force capacity, and a curvature reported as a/P0* must not be multiplied by a measured isometric stress. (2) VERY LOW FORCE, BELOW ABOUT 0.05 F0 -- measured: fibres shorten faster than the hyperbola, which underestimates unloaded speed by about 6-7 % (Edman et al. 1976; Julian et al. 1986, via Seow 2013). (3) LENGTHENING, F > F0 -- the hyperbola does not continue. Katz 1939 (via Alcazar et al. 2019) found lengthening speeds considerably smaller than Hill predicts. Edman 1988 traced the negative branch to 1.6-1.8 P0 and found it nearly flat between 0.90 and 1.20 P0. Human in vivo eccentric maxima are far lower and scattered (see contested_by). (4) NON-STEADY STATE AND HISTORY -- the law has no memory. Force enhancement after stretch and depression after shortening (Abbott & Aubert 1952, listing level only) cannot be produced by an instantaneous Hill force-velocity map. (5) CYCLIC CONTRACTION, WHICH IS HOW LOCOMOTOR MUSCLE WORKS -- measured. In work loops on mouse muscle, Askew & Marsh 1998 (search-summary level) found the power-optimal V/v_max varied almost fourfold, 0.075-0.30, generally BELOW the force-velocity prediction, but ABOVE it at high cycle frequency and brief shortening phases, owing to activation and deactivation kinetics; they conclude the force-velocity relation alone does not predict the optimum. MY INFERENCE: a swimming or flight power budget computed from Hill P_max is neither a safe upper bound nor an estimate unless the cycle is long and slow. (6) ULTRAFAST LARVAL FISH MUSCLE -- the relation is UNTESTED, not shown to fail. Mead et al. 2020 measured force only down to 0.74-0.86 of isometric and fitted nothing. MY CALCULATION (not an observation): taking their estimated v_max of 45 L/s, a Hill curve at any G from 0.066 to 0.49 predicts 0.27-0.66 F0 at 6.5 L/s, against the 0.86 they measured at 28 C. Either the estimated v_max is too low or the ramp force is not steady-state; the data cannot distinguish these, so this is a flag, not a refutation. (7) MULTI-JOINT HUMAN TASKS -- whole-limb force-velocity is often reported as linear (Bobbert 2012; Cuevas-Aburto et al. 2018, both via Alcazar et al. 2019); Alcazar et al. argue the apparent linearity reflects the narrow 40-90 % P0 range usually tested. Either way it is not the Hill relation of any one muscle. (8) PARAMETERS DO NOT TRANSFER across temperature, fibre type or species: G spans at least 0.066-0.49 in the sources read, its temperature direction disagrees between sources, and carp red-muscle v_max rose by a factor of 1.61 (5.71/3.55, my arithmetic) from 10 to 20 C.
:::

## Worked examples

**any muscle with a fitted curvature G (no taxon)**

```
maximise P/(F0*v_max) = f*(1-f)/(1+f/G) -> f_opt = sqrt(G^2+G) - G = v_opt/v_max; G = 0.066 -> f_opt 0.199, P_max 0.0397*F0*v_max; G = 0.25 -> 0.309, 0.0955; G = 0.49 -> 0.364, 0.1328
```

- value: `0.309`

- value range: `[0.199, 0.364]`

- CALCULATED from the equation, not observed. G = 0.25 is illustrative, not a measurement. Over the span of G found (0.066-0.49) the peak-power load moves from 0.20 to 0.36 F0 and the dimensionless peak power changes 3.3-fold (0.1328/0.0397), so a power check is only as good as the measured G for the actual muscle at the actual temperature. f_opt equals v_opt/v_max for every G because the normalised hyperbola (f + G)(u + G) = G(1 + G) is symmetric in f and u.

- evidence: **derived**

**Cyprinus carpio red myotomal muscle, 20 C**

```
G = a/P0* = 0.29, v_max = 5.71 L0/s -> f_opt = sqrt(0.29^2 + 0.29) - 0.29 = 0.322 (of P0*); v_opt = 0.322 * 5.71 = 1.84 L0/s; P_max = 0.1035 * P0* * v_max = 0.156 * P0_measured * v_max if P0* = 1.51 P0_measured
```

- value: `1.84`

- CALCULATED by me from the measured G and v_max of Rome & Sosnicki 1990; it is the speed at which the steady-state fit predicts peak power, not a measured optimum. The power coefficient is 0.1035 relative to the EXTRAPOLATED intercept P0*, and about 1.5x larger (0.156) relative to measured isometric force -- the second figure rests on my inference that P0* is expressed in multiples of measured P0. Using measured isometric stress with 0.1035 would understate the fit's peak power by about a third. The paper's MEASURED maximal power is 94.3 +/- 3.2 W/kg; I did not compare because absolute stress for these bundles was not in the abstract text read.

- evidence: **derived**

**mouse skeletal muscle in cyclic (work-loop) contraction**

- value range: `[0.075, 0.3]`

- OBSERVED power-optimal V/v_max across the cycle conditions tested; peak net power 94 W/kg (Askew & Marsh 1998, at search-summary level -- abstract not opened). Citing papers identify the muscle as soleus; not verified. Compare the calculated 0.20-0.36 above.

- evidence: **literature**

**Danio rerio, 5-day larval tail, 28 C**

- value: `0.86`

- OBSERVED normalised force 0.86 +/- 0.02 (SD, n = 5) while shortening at 6.5 +/- 0.9 L/s; 0.74 +/- 0.1 at 4.3 +/- 0.3 L/s at 18 C (Mead et al. 2020, as relayed by a summarising fetch of the full text). No Hill fit exists for this muscle; see where_it_breaks (6) for the calculated mismatch with a Hill curve under their estimated v_max.

- evidence: **literature**

:::{seealso} Contested
- Meaning of the constant a: Hill 1938 identified it with the heat-of-shortening coefficient; the heat coefficient was later shown to vary with load and speed (Hill 1964, via Seow 2013). Abbott & Wilkie 1953 (via Seow) treat the equation as purely empirical; Seow 2013 argues it encodes cross-bridge kinetics. Not reconciled here.
- Shape: single hyperbola (Hill 1938) vs double hyperbola with a high-force break (Edman 1988; Devrome & MacIntosh 2007, 2018 via Alcazar et al. 2019) vs linear in multi-joint human tasks (Bobbert 2012 via Alcazar) -- with Hahn et al. 2014 and Alcazar et al. 2018b (both via Alcazar 2019) arguing the linearity is an artefact of the tested range. A live disagreement about which form to fit.
- Direction of the temperature effect on curvature: in carp red muscle G FELL from 0.49 to 0.29 between 10 and 20 C (Rome & Sosnicki 1990), and Katz 1939 (via Alcazar et al. 2019) found higher temperature decreased a/P0; but Ranatunga 1984 (via Seow 2013) found a/F0 INCREASES with temperature over 10-35 C in rat fast and slow muscle, and Seow reports a/F0 temperature-INSENSITIVE in some cold-water fish (Johnston & Salamonski 1984; Johnston & Sidell 1984, via Seow). Different taxa and preparations; the three directions are preserved, not averaged.
- Eccentric force: isolated animal muscle reaches about 1.6-1.8 P0 (Edman 1988; Alcazar et al. 2019 summary), while human in vivo maxima compiled by Alcazar et al. 2019 run from 5 % BELOW isometric (Webber & Kriellaars 1997) to 80 % above (Cook & McDonagh 1995, 27.6 C), with most 4-30 % above. Whether the human deficit is neural or methodological is not settled in the sources read.
:::

## Sources

| Citation | Read-level |
|---|---|
| Hill AV (1938) The heat of shortening and the dynamic constants of muscle. Proc R Soc B 126:136-195 | `listing` |
| Hill AV (1964) The effect of load on the heat of shortening of muscle. Proc R Soc B 159:297-318, doi 10.1098/rspb.1964.0004 | `could-not-access` |
| Edman KAP (1988) Double-hyperbolic force-velocity relation in frog muscle fibres. J Physiol 404:301-321, PMC1190827 | `abstract` |
| Bottinelli R, Schiaffino S, Reggiani C (1991) Force-velocity relations and myosin heavy chain isoform compositions of skinned fibres from rat skeletal muscle. J Physiol 437:655-672, PMC1180069 | `abstract` |
| Rome LC, Sosnicki AA (1990) The influence of temperature on mechanics of red muscle in carp. J Physiol 427:151-169, PMC1189924 | `abstract` |
| Seow CY (2013) Hill's equation of muscle performance and its hidden insight on molecular mechanisms. J Gen Physiol 142:561-573, doi 10.1085/jgp.201311107, PMC3840917 | `full-text` |
| Alcazar J, Csapo R, Ara I, Alegre LM (2019) On the shape of the force-velocity relationship in skeletal muscles: the linear, the hyperbolic, and the double-hyperbolic. Front Physiol 10:769, doi 10.3389/fphys.2019.00769 | `full-text` |
| Askew GN, Marsh RL (1998) Optimal shortening velocity (V/Vmax) of skeletal muscle during cyclical contractions: length-force effects and velocity-dependent activation and deactivation. J Exp Biol 201:1527-1540, doi 10.1242/jeb.201.10.1527 | `search-summary` |
| Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM (2020) Mechanical characteristics of ultrafast zebrafish larval swimming muscles. Biophys J 119:806-820, doi 10.1016/j.bpj.2020.06.036, PMC7451861 | `full-text` |
| Katz B (1939) The relation between force and speed in muscular contraction. J Physiol 96:45-64 | `listing` |
| Abbott BC, Aubert XM (1952) The force exerted by active striated muscle during and after change of length. J Physiol 117:77-86 | `listing` |


---

*Generated from [`library/laws/hill-muscle.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/hill-muscle.yaml). Do not edit this page; edit the YAML.*
