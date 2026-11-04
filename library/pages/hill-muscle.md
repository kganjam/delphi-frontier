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
(F + a)(v + b) = (F_0 + a)\,b \quad\Longleftrightarrow\quad \frac{v}{v_{\max}} = \frac{1 - F/F_0}{1 + (F/F_0)/G},\qquad G = \frac{a}{F_0} = \frac{b}{v_{\max}}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `F` | M*L/T^2 | N | force (afterload) the muscle bears during steady isotonic shortening |
| `v` | L/T | m/s | steady shortening velocity; in practice reported normalised as muscle or fibre lengths per second (L0/s) |
| `F0` | M*L/T^2 | N | ZERO-VELOCITY INTERCEPT of the fitted hyperbola. It equals measured isometric force ONLY if the fit is constrained through it. In an unconstrained fit it is an extrapolated load (Rome & Sosnicki 1990 call it P0* and measure it at 1.19 and 1.51 times measured P0). Every curvature below says which normalisation it uses, or that this is unknown. |
| `a` | M*L/T^2 | N | Hill force constant; a FITTED parameter |
| `b` | L/T | m/s | Hill velocity constant; a FITTED parameter, equal to a * v_max / F0 |
| `v_max` | L/T | m/s | zero-load intercept of the fitted hyperbola. It is NOT the same quantity as a slack-test V0, and single-fibre work finds the hyperbola underestimates true unloaded speed (where_it_breaks). |
| `G` | 1 | dimensionless | curvature a/F0 = b/v_max. SMALLER G means a MORE curved relation and a LOWER peak power for the same F0 and v_max. |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `curvature_G_general` | unknown (interval 0.066 to 0.49) dimensionless — *assembled-from-literature* | NO SINGLE VALUE EXISTS and none is asserted. The interval is MY assembly of the extreme MEANS in the sources I read (rat type-1 and type-2A skinned fibres at 12 C, 0.066, Bottinelli et al. 1991; carp red muscle bundles at 10 C, 0.49 relative to the EXTRAPOLATED intercept, Rome & Sosnicki 1990). It mixes species, fibre types, temperatures, preparations and normalisations, so it is a span of means and NOT a confidence interval. The value 0.25 that circulates in teaching material was not found in any source I read (Seow 2013 full text; the abstracts listed below) and is not entered. |
| `curvature_G_frog_sartorius_Hill1938` | 0.203 dimensionless — *derived-from-published-fit* | DERIVED BY ME from Hill's own fitted constants (F + 14.35)(V + 1.03) = 87.6, as reproduced in Seow 2013 Fig. 2 (full text read). a/P0 = 14.35/70.70 = 0.203 and b/v_max = 1.03/5.075 = 0.203, as they must be. One fit to one preparation; no spread is available, so no interval is given. I did not read Hill 1938 itself and did not confirm the units of 14.35 and 1.03 (the ratio is unit-free). Frog sartorius at about 0 C per the standard account -- the temperature is REMEMBERED, not read. |
| `curvature_G_rat_type1_12C` | 0.066 (interval 0.059 to 0.073) dimensionless | MEASURED, Bottinelli et al. 1991 (abstract), single skinned fibres typed by myosin heavy chain, 12 C: 0.066 +/- 0.007. The abstract labels the spread as S.E.M. only for the type-1 V0 figure; for the curvatures the spread type is unlabelled in the text I read. Interval = mean +/- that spread. Whether a/P0 uses measured or extrapolated P0: unknown. |
| `curvature_G_rat_type2A_12C` | 0.066 (interval 0.042 to 0.09) dimensionless | MEASURED, Bottinelli et al. 1991: 0.066 +/- 0.024 (spread type unlabelled). |
| `curvature_G_rat_type2X_12C` | 0.132 (interval 0.124 to 0.14) dimensionless | MEASURED, Bottinelli et al. 1991: 0.132 +/- 0.008 (spread type unlabelled). |
| `curvature_G_rat_type2B_12C` | 0.113 (interval 0.1 to 0.126) dimensionless | MEASURED, Bottinelli et al. 1991: 0.113 +/- 0.013 (spread type unlabelled). The authors group types 1 and 2A as HIGH curvature and 2X and 2B as LOW curvature, so curvature does not simply track speed (2A and 2X have similar V0). |
| `v0_rat_fibres_12C` | unknown (interval 0.35 to 2.84) L0/s | MEASURED range across 74 fibres, Bottinelli et al. 1991. Means: type 1 0.639 +/- 0.038 (S.E.M., labelled), 2A 1.396 +/- 0.084, 2X 1.451 +/- 0.066, 2B 1.800 +/- 0.109. These are V0 values; the abstract does not say whether V0 was the hyperbola intercept or a slack-test value. |
| `curvature_G_carp_red_10C` | 0.49 (interval 0.43 to 0.55) dimensionless | MEASURED, Rome & Sosnicki 1990 (abstract): a/P0* = 0.49 +/- 0.06, n = 6, normalised to the EXTRAPOLATED intercept P0* = 1.19 +/- 0.04, from a hyperbola deliberately NOT constrained through measured P0. Spread type unlabelled in the abstract. |
| `curvature_G_carp_red_20C` | 0.29 (interval 0.23 to 0.35) dimensionless | MEASURED, Rome & Sosnicki 1990: a/P0* = 0.29 +/- 0.06, n = 6, with P0* = 1.51 +/- 0.20. Same normalisation caveat. The authors state the curve is MORE curved at 20 C than at 10 C. |
| `vmax_carp_red` | unknown (interval 3.55 to 5.71) L0/s | MEASURED, Rome & Sosnicki 1990: 3.55 +/- 0.26 ML/s at 10 C and 5.71 +/- 0.29 ML/s at 20 C (n = 6 each), Q10 1.63 +/- 0.07. Isometric-tension Q10 1.13 +/- 0.02. Peak power 59.7 +/- 2.3 W/kg at 10 C and 94.3 +/- 3.2 W/kg at 20 C, Q10 1.58. The two values are the two temperatures, not an interval of one quantity. |
| `vmax_zebra_finch_syrinx_30C` | 25 L0/s | MEASURED by the isovelocity technique, Gladman & Elemans 2024 (abstract). Entered to show that v_max is a property of a muscle and spans more than an order of magnitude between muscles; the authors' 37-42 L0/s at body temperature is a Q10 EXTRAPOLATION, not a measurement, and is not entered as a value. |
| `break_point_force_frog` | 0.784 (interval 0.78 to 0.788) F/P0 (measured) | MEASURED, Edman 1988 (abstract): the relation has TWO hyperbolic regions, 0-78 % and 78-100 % of measured P0, joined at 78.4 +/- 0.4 % P0 (mean +/- S.E., n = 12), corresponding to 10.9 +/- 0.4 % of Vmax. Single frog (Rana temporaria) fibres, 1-3 C, sarcomere length 2.10 um. The high-force region is MORE curved. |
| `lengthening_force_frog` | unknown (interval 1.6 to 1.8) F/P0 (measured) | MEASURED, Edman 1988: the negative (lengthening) branch was traced from P0 up to 1.6-1.8 P0 in five experiments; between 0.90 and 1.20 P0 the relation was nearly flat, speeds differing by 1.8 +/- 0.3 % of Vmax across that range. The 1.6-1.8 is the range of loads applied; the abstract I read does not state it is a measured plateau, so no ceiling value is asserted. |
| `valid_force_range` | unknown (interval 0.05 to 0.8) F/F0 | REVIEW STATEMENT, Seow 2013 (full text read): "velocity measurements within the force range of 0.05-0.8 Fmax are remarkably close to the values predicted by the Hill equation". Below about 0.05 measured speed exceeds the hyperbola (Hill underestimates Vmax by about 6-7 %, citing Edman et al. 1976 and Julian et al. 1986, which I did not read). Above about 0.8 the hyperbola fails (Edman 1988). |
| `vopt_cyclic_mouse_soleus` | unknown (interval 0.075 to 0.3) V/Vmax | MEASURED, Askew & Marsh 1998 (abstract), mouse soleus under sawtooth work loops: the V/Vmax giving maximum NET cyclic power ranged almost fourfold, 0.075-0.30, against an isotonic optimum of 0.22. Peak isotonic power 167 W/kg; maximum net cyclic power 94 W/kg. |
| `vratio_in_vivo_fish_red` | unknown (interval 0.17 to 0.37) V/Vmax | OBSERVED in swimming fish: carp red muscle used only over V/Vmax 0.18-0.36 at both 10 and 20 C (Rome & Sosnicki 1990); scup red muscle 0.17-0.37 (Rome, Sosnicki & Choi 1992). Interval is the union of the two. |

## Why it holds

EMPIRICAL IN ORIGIN, with a later mechanistic reading. Hill (1938) fitted a rectangular hyperbola to the speed at which frog muscle shortened against a range of loads, and tied the constant a to the extra heat liberated by shortening. That energetic identity did not hold: as reported by Seow 2013, the heat coefficient was later found to depend on load and speed (Hill 1964), and Abbott & Wilkie (1953) regarded the equation as purely empirical. The cross-bridge reading (A.F. Huxley 1957; worked through by Seow 2013): myosin heads attach at a speed-independent rate and detach at a rate that rises with filament sliding speed, so faster sliding leaves fewer heads attached and each bears less force. Seow shows that a two-state model reduces EXACTLY to Hill's hyperbola under three stated assumptions -- detachment rate linear in velocity, attachment rate independent of velocity, and force per bridge falling linearly with velocity. MY INFERENCE: the hyperbola therefore holds where those assumptions hold and fails where they do not, which is consistent with the measured failures at very low speed (near the isometric end, where Edman reports a different curvature) and in lengthening, where heads are pulled off rather than released by ATP-driven cycling.

## Where it holds

- **regime**: steady-state, isotonic or isovelocity SHORTENING of fully and constantly activated muscle
- **force range**: about 0.05-0.8 F0 (Seow 2013)
- **preparation**: single fibres or fibre-type-homogeneous bundles; mixed whole muscles are better described by a sum of hyperbolas (Claflin & Faulkner 1989, as reported by Seow 2013)
- **temperature**: only the temperature at which G and v_max were measured; neither transfers
- **taxa**: ['frog (Rana)', 'rat and mouse limb muscle', 'carp and scup red muscle', 'zebra finch syringeal muscle (v_max only)']
- **notes**: Parameters are properties of ONE muscle (fibre type, temperature, sarcomere length). Edman 1988 reports that raising sarcomere length from 1.85 to 2.60 um left Vmax unchanged but steadily reduced curvature, so G also depends on operating length. For Danio rerio no measured G or v_max was found: Europe PMC query (zebrafish OR "Danio rerio") AND ("force-velocity" OR "Hill equation" OR "maximum shortening velocity") AND muscle returned 234 hits, of which I read the top 5 by relevance, none a zebrafish skeletal-muscle force-velocity fit. That is a narrow search, and the negative is scoped to it.


:::{danger} Where it breaks
Measured failure boundaries, in the order a designer will hit them. (1) HIGH FORCE, above about 0.78 F0. Edman 1988 measured in single frog fibres that the relation is TWO hyperbolas joined at 78.4 +/- 0.4 % of measured P0 (10.9 % Vmax), the high-force one more curved; Seow 2013 adds reports of outright reversal of curvature there (Wang et al. 1994; Devrome & MacIntosh 2007 -- not read by me). Consequence: a hyperbola fitted at low and middle loads and extrapolated to zero speed OVERSHOOTS measured isometric force. Rome & Sosnicki 1990 measured that overshoot directly in carp red muscle: the unconstrained fit's intercept P0* was 1.19 x measured P0 at 10 C and 1.51 x at 20 C. A fitted F0 must never be used as a holding force, and a G quoted relative to P0* is not interchangeable with one quoted relative to measured P0 (see worked example 2 -- the choice moves a predicted power ratio by about 25 %). (2) VERY LOW FORCE, below about 0.05 F0. Measured speed exceeds the hyperbola; the fitted v_max underestimates true unloaded speed by about 6-7 % in single fibres, and by much more in mixed whole muscle, where fast fibres outrun slow ones (Seow 2013, reporting Edman et al. 1976, Julian et al. 1986, Claflin & Faulkner 1989). (3) LENGTHENING (eccentric) contraction. The Hill equation has no lengthening branch that matches data. Continued past F0 it gives F = (F0*b - a*v)/(v + b), which diverges as v approaches -b: the equation predicts UNBOUNDED force at a finite stretch speed b (this is my algebra, not a reported result). Edman 1988 measured lengthening loads only up to 1.6-1.8 P0, with the relation nearly flat between 0.90 and 1.20 P0 -- a smooth continuation of the HIGH-force hyperbola, not of the Hill hyperbola fitted below 0.78 P0. (4) HISTORY. The relation is a steady-state, history-free mapping. Force after active stretch is enhanced: de Campos et al. 2022 (meta-analysis, 45 studies) find residual torque enhancement in human adductor pollicis, ankle dorsiflexors and plantar flexors and knee extensors, but NOT in elbow or knee flexors -- so even the history correction does not transfer between muscles. (5) CYCLIC CONTRACTION, which is what locomotor muscle does. Askew & Marsh 1998 measured in mouse soleus that the V/Vmax giving maximum net work-loop power ranged 0.075-0.30 against an isotonic optimum of 0.22, and peak net cyclic power (94 W/kg) was 56 % of peak isotonic power (167 W/kg) (ratio mine). Length-force effects pull the optimum down at large strain; velocity-dependent activation and deactivation push it up at high cycle frequency. Their conclusion, verbatim in substance: the force-velocity relationship alone does not accurately predict the optimal V/Vmax in muscles operating over a wide range of conditions, explicitly naming fish red muscle. FOR AN UNDULATING OR FLAPPING ANIMAL, THE HILL CURVE GIVES AN UPPER BOUND ON POWER, NOT AN ESTIMATE. (6) WHOLE MULTI-JOINT HUMAN TASKS. Jaric 2015 reviews evidence that force-velocity data from maximal multi-joint movements are approximately LINEAR, not hyperbolic. A Hill G cannot be read off, or applied to, such data. (7) NON-TRANSFER OF PARAMETERS. G spans at least 0.066-0.49 across the sources read here; v_max spans 0.35 L0/s (slow rat fibre, 12 C) to 25 L0/s (zebra finch syrinx, 30 C). Carp v_max rose 1.6-fold over 10 C and its G fell from 0.49 to 0.29. Using another species's, fibre type's or temperature's parameters is the commonest misuse, and the curve itself gives no warning when it is done. (8) PARTIAL ACTIVATION is outside every source here: all fits are at maximal activation, and recruitment in a swimming fish is partial and changes with speed (Rome et al. 1992). Behaviour of G under submaximal activation: unknown to me; not searched.
:::

## Worked examples

**Rana (frog sartorius), Hill's own 1938 fit**

```
(F + 14.35)(V + 1.03) = 87.6
  P0    = 87.6/1.03 - 14.35 = 70.70
  v_max = 87.6/14.35 - 1.03 = 5.075
  G     = 14.35/70.70 = 1.03/5.075 = 0.203
  peak power where F/F0 = v/v_max = sqrt(G^2 + G) - G = 0.291
  P_max = 0.291^2 * F0 * v_max = 0.0848 * F0 * v_max
```

- value: `0.0848`

- CALCULATED by me from the published fit constants (via Seow 2013); not an observation. Peak power sits at 29 % of F0 and 29 % of v_max -- the two fractions are equal for every G because the normalised hyperbola (f + G)(u + G) = G(1 + G) is symmetric in f and u. This agrees with Seow's statement that maximum power occurs at about 0.3 F0.

- evidence: **derived**

**Cyprinus carpio red muscle -- Hill optimum against in vivo use, and a consistency check**

```
f_opt = u_opt = sqrt(G^2 + G) - G
  10 C: G = 0.49 -> 0.3645;  V_opt = 0.3645 * 3.55 = 1.29 L0/s
  20 C: G = 0.29 -> 0.3216;  V_opt = 0.3216 * 5.71 = 1.84 L0/s
  in vivo V/Vmax 0.18-0.36 (observed): Hill power there, as a fraction of Hill peak
    G = 0.29: 0.88 at 0.18, 0.99 at 0.36
    G = 0.49: 0.81 at 0.18, 1.00 at 0.36
  predicted peak-power ratio 20 C / 10 C = (f20^2 * 5.71 * F0_20) / (f10^2 * 3.55 * F0_10)
    with F0 = P0*  (1.51 vs 1.19 x measured P0, P0 Q10 1.13): 1.80
    with F0 = measured P0 (P0 Q10 1.13):                     1.42
    measured power Q10:                                       1.58
```

- value: `0.3216`

- All numbers in the computation are CALCULATED by me from the measured parameters of Rome & Sosnicki 1990, except the 0.18-0.36 in vivo range and the 1.58 power Q10, which are their OBSERVATIONS. Finding 1 (calculated): the band the fish actually uses sits at or below the Hill optimum and costs at most about 20 % of Hill peak power, consistent with the authors' claim that V/Vmax is a design constraint -- but note Askew & Marsh's cyclic optimum can lie well below the isotonic one, so this agreement is not a test of the Hill curve. Finding 2 (calculated): neither normalisation reproduces the measured 1.58; the choice of F0 moves the prediction by about 25 %. I assumed P0* is expressed in multiples of measured P0, which the abstract implies (fits "not constrained to pass through P0 = 1") but does not state outright. The same 25 % ambiguity was first raised by an earlier adversarial review of a previous draft of this entry (docs/research/fish/challenge-59.md on branch claude/challenge-59-lawentry-hill-muscle-559i0r); I recomputed it independently.

- evidence: **derived**

**any muscle, lengthening -- the hyperbola continued past F0**

```
F = (F0*b - a*v)/(v + b);  as v -> -b from above, F -> +infinity
  with G = 0.203 (frog, Hill 1938): stretch at 0.203 v_max predicts infinite force
```

- CALCULATED (algebra on the equation), compared with Edman 1988's OBSERVATION that loads of 1.6-1.8 P0 were applied and the fibre lengthened at modest speeds. The equation must not be used on the lengthening side at all.

- evidence: **derived**

:::{seealso} Contested
- SHAPE AT HIGH FORCE: one hyperbola (Hill 1938) versus two hyperbolas with a break near 0.78 P0 (Edman 1988, measured) versus reversal of curvature (Wang et al. 1994; Devrome & MacIntosh 2007, as reported by Seow 2013, not read). Recorded, not reconciled.
- SHAPE IN WHOLE-BODY TASKS: hyperbolic for isolated muscle versus approximately linear for maximal multi-joint human movements (Jaric 2015). These may be different objects rather than a disagreement, but both are called "the force-velocity relationship" in the literature.
- TEMPERATURE AND CURVATURE: Rome & Sosnicki 1990 measure carp red-muscle curvature INCREASING from 10 to 20 C (a/P0* 0.49 to 0.29). Edman's 1988 Adv Exp Med Biol abstract states that changing temperature within 1-11 C does NOT affect the shape of either portion of the frog relation. Different species, ranges and normalisations; left as two measurements that disagree on whether curvature is temperature sensitive.
- MEANING OF THE EQUATION: purely empirical (Abbott & Wilkie 1953, as reported by Seow 2013, not read) versus carrying cross-bridge kinetic content (Seow 2013, who derives it from a two-state model under three assumptions).
:::

## Sources

| Citation | Read-level |
|---|---|
| Hill AV (1938) Proc R Soc Lond B 126:136-195, The heat of shortening and the dynamic constants of muscle, doi 10.1098/rspb.1938.0050 | `listing` |
| Seow CY (2013) J Gen Physiol 142:561-573, Hill's equation of muscle performance and its hidden insight on molecular mechanisms, doi 10.1085/jgp.201311107, PMC3840917 | `full-text` |
| Edman KAP (1988) J Physiol 404:301-321, Double-hyperbolic force-velocity relation in frog muscle fibres, doi 10.1113/jphysiol.1988.sp017291 | `abstract` |
| Edman KAP (1988) Adv Exp Med Biol 226:643-652, Double-hyperbolic nature of the force-velocity relation in frog skeletal muscle, PMID 3261494 | `abstract` |
| Edman KAP (1993) Adv Exp Med Biol 332:667-676, Mechanism underlying double-hyperbolic force-velocity relation in vertebrate skeletal muscle, doi 10.1007/978-1-4615-2872-2_59 | `abstract` |
| Rome LC, Sosnicki AA (1990) J Physiol 427:151-169, The influence of temperature on mechanics of red muscle in carp, doi 10.1113/jphysiol.1990.sp018165 | `abstract` |
| Rome LC, Sosnicki A, Choi IH (1992) J Exp Biol 163:281-295, The influence of temperature on muscle function in the fast swimming scup. II. The mechanics of red muscle, doi 10.1242/jeb.163.1.281 | `abstract` |
| Rome LC, Choi IH, Lutz G, Sosnicki A (1992) J Exp Biol 163:259-279, ... scup. I. Shortening velocity and muscle recruitment during swimming, doi 10.1242/jeb.163.1.259 | `abstract` |
| Rome LC et al. (1988) Nature 335:824-827, Why animals have different muscle fibre types, doi 10.1038/335824a0 | `abstract` |
| Bottinelli R, Schiaffino S, Reggiani C (1991) J Physiol 437:655-672, Force-velocity relations and myosin heavy chain isoform compositions of skinned fibres from rat skeletal muscle, doi 10.1113/jphysiol.1991.sp018617 | `abstract` |
| Askew GN, Marsh RL (1998) J Exp Biol 201:1527-1540, Optimal shortening velocity (V/Vmax) of skeletal muscle during cyclical contractions, doi 10.1242/jeb.201.10.1527 | `abstract` |
| Jaric S (2015) Int J Sports Med 36:699-704, Force-velocity relationship of muscles performing multi-joint maximum performance tasks, doi 10.1055/s-0035-1547283 | `abstract` |
| de Campos D, Orssatto LBR, Trajano GS, Herzog W, Fontana HB (2022) J Sport Health Sci 11:94-103, Residual force enhancement in human skeletal muscles -- a systematic review and meta-analysis, doi 10.1016/j.jshs.2021.05.006, PMC8847921 | `abstract` |
| Gladman NW, Elemans CPH (2024) J Exp Biol 227:jeb246330, Male and female syringeal muscles exhibit superfast shortening velocities in zebra finches, doi 10.1242/jeb.246330 | `abstract` |
| Medler S (2002) Am J Physiol Regul Integr Comp Physiol 283:R368-R378, Comparative trends in shortening velocity and force production in skeletal muscles, doi 10.1152/ajpregu.00689.2001 | `abstract` |
| Huxley AF (1957) Prog Biophys Biophys Chem 7:255-318, Muscle structure and theories of contraction | `listing` |


---

*Generated from [`library/laws/hill-muscle.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/hill-muscle.yaml). Do not edit this page; edit the YAML.*
