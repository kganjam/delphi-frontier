---
title: Second moment of area for a spar, and how bending stiffness scales with span
label: law-second-moment
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-second-moment
k = \frac{F}{\delta} = \frac{3 E I}{L^3}, \qquad I = \int_A y^2 \, dA
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `k` | M/T^2 | N/m | tip bending stiffness of a uniform cantilevered spar under a transverse point load at the tip |
| `F` | M*L/T^2 | N | transverse force applied at the tip |
| `delta` | L | m | transverse tip deflection (small-deflection theory) |
| `E` | M/(L*T^2) | Pa | Young's modulus of the spar material along the span |
| `I` | L^4 | m^4 | second moment of area of the cross-section about the neutral axis of bending |
| `L` | L | m | span: free length from the clamped root to the loaded tip |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `tip_load_coefficient` | 3 | Exact within Euler-Bernoulli theory for a prismatic cantilever with a tip point load (delta = F L^3 / 3EI). Derived, not measured, so no interval. A uniformly distributed load gives delta = w L^4 / 8EI instead; confusing the two load cases is a factor of 2.67 error (calculated: (1/3)/(1/8)). |
| `section_forms` | solid circle I = pi d^4 / 64; tube I = pi (D^4 - d_in^4) / 64; thin-walled tube I ~ pi r^3 t; rectangle I = b h^3 / 12 with h in the bending direction | Exact geometry, not measured. Depth enters as h^3 (or d^4), width only as b^1: doubling depth multiplies I by 8, doubling width by 2. |
| `span_exponent_fixed_section` | -3 | Derived: k is proportional to L^-3 at fixed E and I. Doubling span gives one-eighth the tip stiffness. |
| `span_exponent_isometric` | 1 | Derived: if every length scales together, I scales as L^4 and k as E*L^4/L^3 = E*L. Equivalently EI scales as L^4. This is the geometric-similarity null against which the measured exponents below are compared. |
| `insect_spanwise_EI_exponent_interspecific` | 2.97 dimensionless | MEASURED by Combes & Daniel 2003 on 16 insect species from six orders (static bending). Their abstract says only "scales strongly with the cube of wing span"; the figure 2.97 (and 2.08 for chordwise against chord) is as relayed by Ribak et al. 2025, which I read in full. I did not read the Combes & Daniel full text, so the confidence interval is unknown. |
| `beetle_EI_exponent_intraspecific` | 4.32 (interval 3.68 to 4.96) dimensionless | MEASURED by Ribak et al. 2025 on dry detached wings of the beetle Batocera rufomaculata, seven wings, static bending, EI against wing length; the authors give 4.32 +/- 0.64 as a 95% CI. The same wings after 24 h soaking gave 4.38 +/- 0.98, i.e. [3.40, 5.36], which the authors report as statistically indistinguishable from the dry value. Read in full text. |
| `zebrafish_caudal_fin_EI` | unknown (interval 1.5e-09 to 4e-09) N*m^2 | MEASURED in vivo on adult Danio rerio caudal fins with micro-Newton loads (Puri et al. 2018, abstract). The abstract gives only the range along the proximal-distal axis, which it reports as non-monotonic; no central value was available to me, so none is given. The abstract calls these "bending moments" but quotes N m^2, which are flexural-rigidity (EI) units; reading them as EI is my inference from the units. |
| `first_bending_mode_coefficient` | 1.8751 | Calculated here (bisection on cos(x)cosh(x) = -1): first root beta_1 L = 1.8751, so the first natural frequency of a uniform cantilever is f_1 = 0.5596 * sqrt(EI / (m' L^4)), with m' the mass per unit span. Used in where_it_breaks for the dynamic limit. Derived, not measured. |

## Why it holds

Under pure bending a plane section stays plane and rotates about the neutral axis, so axial strain, and for a linear-elastic material axial stress, grows linearly with distance y from that axis. The resisting moment is stress times lever arm integrated over the section, which puts y in twice: M = (E / rho_c) * integral(y^2 dA) = E I / rho_c, with rho_c the radius of curvature. Material far from the neutral axis therefore counts as the square of its distance, which is why tubes, box spars and I-sections, and leading-edge vein complexes in insect wings, carry material at the periphery. Calculated here: at equal cross-sectional area a tube with bore ratio K = d_in/D = 0.5 has 1.67x the I of a solid rod, 2.92x at K = 0.7 and 9.53x at K = 0.9. For a tip-loaded cantilever the bending moment grows linearly from tip to root, and integrating the curvature M/EI twice along the span gives delta = F L^3 / 3EI. That is where span gets its cube.
Span scaling, all DERIVED here from the equation and not observed. (a) Same section, longer span: k scales as L^-3. (b) Geometric similarity: k scales as L, so a larger isometric spar is stiffer in absolute terms, but relative deflection under its own weight, delta/L = w L^3 / 8EI with w proportional to A, scales as L (Galileo's square-cube penalty). (c) Geometric similarity under an aerodynamic load at fixed dynamic pressure (load per span proportional to chord, so to L): delta/L is size-independent. (d) Geometric similarity under a load that must support body weight (proportional to L^3, so load per span proportional to L^2): delta/L scales as L. (e) To hold self-weight delta/L constant in a solid section of the same material, depth must scale as L^1.5, the same exponent McMahon's elastic-similarity argument postulates, here reached from beam theory.

## Where it holds

- **theory**: Euler-Bernoulli: plane sections remain plane and normal to the neutral axis; shear deformation neglected
- **material**: linear-elastic, homogeneous along the span, same modulus in tension and compression, passive (no actuation)
- **geometry**: slender and prismatic; span-to-depth above about 10 for an isotropic section (see where_it_breaks for the shear-soft case); a tapered spar needs I(x) integrated explicitly and does not obey the 3EI/L^3 coefficient
- **deflection**: small: linear theory is within 1% of the elastica while true delta/L is below about 0.1 (calculated, see where_it_breaks)
- **loading**: static or quasi-static, at a forcing frequency well below the first bending mode
- **notes**: The formula is not in dispute inside these assumptions. In biology the uncertainty is in the inputs (E for hydrated anisotropic tissue, the real cross-section, whether layers are bonded) and in which exponent to use when scaling. Applies to engineered spars and, as a first approximation only, to single biological elements such as an insect leading-edge vein or a single fin ray.


:::{danger} Where it breaks
The equation mis-predicts tip stiffness in six regimes: it is too stiff for short or shear-soft spans and for thin-walled tubes, too compliant at large deflection, has no single EI to use for layered or actuated sections, does not apply near resonance, and measured span-scaling exponents in insect wings contradict the isometric EI ~ L^4 in both directions. Details follow. (1) SHORT OR SHEAR-SOFT SPANS. Euler-Bernoulli neglects shear. Calculated here from Timoshenko beam theory for a tip-loaded cantilever: shear adds delta_s/delta_b = 3EI/(kappa G A L^2). For a rectangle (kappa = 5/6) that is 0.300 (E/G)(h/L)^2; for a solid circle (kappa = 0.886, the Cowper form at Poisson ratio 0.3) it is 0.212 (E/G)(d/L)^2. Isotropic material (E/G = 2.6): rectangle 0.8% at L/h = 10, 3.1% at 5, 8.7% at 3; circle 0.6%, 2.2%, 6.1%. With E/G = 20 (an ASSUMED value, illustrative of fibre composites and fibrous tissue, not measured for any organism here) the rectangle error is 6% at L/h = 10, 24% at 5 and 67% at 3. The usual "L/h > 10" rule is therefore only safe for isotropic material; for a shear-soft spar the law over-predicts stiffness at spans that look slender. (2) LARGE DEFLECTION. Calculated here by shooting the inextensible elastica for a tip load that stays vertical (RK4 with bisection; a computation, not an observation): the linear formula over-predicts tip deflection by 1.0% at true delta/L = 0.099, 5.1% at 0.216, 10.1% at 0.297 and 35% at 0.494 (load parameter F L^2/EI = 0.3, 0.68, 0.98, 2.0). The solver reproduces the classical value delta/L = 0.3017 at F L^2/EI = 1. Here the real spar is STIFFER than the law says (error in the conservative direction for a stiffness check, unconservative for a deflection-clearance check). Past delta/L of about 0.2 k is no longer a constant, and flapping wings and swimming fins can reach that range. (3) THIN-WALLED TUBES. Brazier (1927, abstract) states that the linear St Venant solution implies the advantage of moving material away from the neutral axis "increases without limit" as the wall thins, and that this is not borne out in practice; the second-order effect is ovalisation of the section, which reduces I under load and gives a limit moment. Local shell buckling can come first. So the equal-mass gain above (9.5x at K = 0.9) is exactly the regime where the law over-promises, and the law itself gives no collapse load. I did not retrieve Brazier's closed-form limit moment and do not quote one. (4) LAYERED, SLIDING OR ACTUATED SECTIONS, which is the fish fin-ray case. A ray-finned fish fin ray is a pair of hemitrichs. Calculated here: two layers of thickness h fully bonded have I = 8 b h^3 / 12; the same two layers free to slide have 2 b h^3 / 12, a factor of 4 from interlayer coupling alone, with the real value set by connective-tissue shear stiffness, which the law does not contain. Alben, Madden & Lauder 2007 (abstract) report that fin-ray stiffness varies over more than an order of magnitude depending on actuation at the ray base, so a fin ray does not have a single EI and k = 3EI/L^3 with a fixed EI cannot describe it. Puri et al. 2018 (abstract) report that the whole-fin EI of the zebrafish caudal fin varies non-monotonically along the proximal-distal axis in a way they state is not due to fin geometry; my inference is that a geometric I calculation alone would not reproduce that profile. They also report that disrupting the interray tissue caused no significant change in overall bending stiffness, so for that fin the stiffness sits in the rays, not the webbing. (5) DYNAMIC LOADING. The static k applies only well below the first bending mode, f_1 = 0.5596 sqrt(EI/(m' L^4)) (calculated). Under geometric similarity f_1 scales as L^-1 (derived), so a scaled-up spar driven at the same frequency moves toward resonance, where effective stiffness and deflection are not given by this law at all. (6) USING ISOMETRY TO SCALE A BIOLOGICAL SPAR. The isometric prediction EI ~ L^4 is contradicted in both directions by measurement: insect wings across 16 species give spanwise EI ~ span^2.97 (Combes & Daniel 2003), below isometry, while beetle wings within one species give EI ~ length^4.32 with 95% CI [3.68, 4.96] (Ribak et al. 2025), at or above it. My inference, not either author's claim: interspecifically, k = 3EI/L^3 is roughly size-independent across insect wings (exponent about -0.03), whereas within Batocera rufomaculata k rises as about L^1.3. Scaling a biological spar by any single assumed exponent is an error of up to roughly L^1.3 in k; check the measured exponent for the lineage and the comparison (within versus between species) first.
:::

## Worked examples

**generic spar, fixed cross-section, span doubled**

```
k2/k1 = (L1/L2)^3 = (1/2)^3 = 0.125
```

- value: `0.125`

- Calculated from the law. Same section at twice the span has one-eighth the tip stiffness.

- evidence: **derived**

**generic spar, geometrically similar, every length doubled**

```
I2/I1 = 2^4 = 16;  k2/k1 = 16 / 2^3 = 2;  self-weight delta/L ratio = 2;  f_1 ratio = 1/2
```

- value: `2`

- Calculated. Isometric doubling doubles tip stiffness yet doubles relative sag under self-weight and halves the first bending frequency. See where_it_breaks (6): real wings do not scale this way.

- evidence: **derived**

**tube against solid rod of equal mass**

```
D = 1/sqrt(1 - K^2) for unit rod diameter;  I_tube/I_rod = D^4 (1 - K^4);  K = 0.5 -> 1.667, K = 0.7 -> 2.922, K = 0.9 -> 9.526
```

- value: `1.667`

- Calculated, exact for linear theory. The large gains at high K are the regime of where_it_breaks (3). Currey & Alexander 1985 (abstract) state that the mass-optimal K for a real bone depends on whether it is selected for yield or fatigue strength, ultimate strength, impact strength or stiffness, and on whether the cavity holds marrow or gas; I did not retrieve their numerical optima.

- evidence: **derived**

**Danio rerio caudal fin, back-calculated tip stiffness**

```
k = 3 EI / L^3 with EI in [1.5e-9, 4.0e-9] N m^2 (Puri et al. 2018, measured) and an ASSUMED effective length L = 5e-3 m -> k in [0.036, 0.096] N/m; L = 4e-3 m -> [0.070, 0.19]; L = 6e-3 m -> [0.021, 0.056]
```

- value range: `[0.036, 0.096]`

- Calculated, not measured. EI is the authors' measurement; the 4 to 6 mm effective lengths are my assumptions for illustration and are not taken from the paper (I did not find a fin length in the abstract). Because k goes as L^-3, the answer is only as good as that length. For a design that enlarges the fin ray to twice the span at the same tip stiffness, EI must rise eightfold (calculated); see where_it_breaks (4) for why a fixed EI is itself an approximation for a ray.

- evidence: **derived**

**insect wings, 16 species from six orders; Batocera rufomaculata wings, 7 wings**

```
interspecific EI ~ span^2.97 -> k ~ L^-0.03; intraspecific EI ~ L^4.32 [3.68, 4.96] -> k ~ L^1.32 [0.68, 1.96]; at 1.5x span k ratio 0.99 versus 1.71 [1.32, 2.21]
```

- The exponents are measurements (Combes & Daniel 2003; Ribak et al. 2025). The k exponents and ratios are my calculation from them via k = 3EI/L^3, assuming the measured EI is the uniform- cantilever EI, which neither wing is.

- evidence: **literature**

:::{seealso} Contested
- Scaling exponent of wing EI with size. Combes & Daniel 2003 (16 species, six orders, no beetles) report interspecific spanwise EI ~ span^3 (2.97 as relayed by Ribak et al.) and chordwise EI ~ chord^2 (2.08). Ribak et al. 2025 report intraspecific EI ~ length^4.32 +/- 0.64 in Batocera rufomaculata, significantly above both, and not significantly different from an intraspecific chordwise exponent of 4.0 they attribute to earlier work on Protaetia cuprea (Meresman & Ribak; not read here). Ribak et al. state it is not clear whether beetles differ from other insects or whether intraspecific and interspecific scaling differ. Not reconciled here.
- What the null exponent is. Ribak et al. 2025 call 3.0 'the theoretical 3.0 that is expected for a cantilever beam loaded at the tip'. Geometric similarity of the section gives EI ~ L^4 (derived in this entry). My inference is that 3.0 is the exponent at which tip stiffness F/delta is size-independent, not the isometric expectation; the two nulls are different and both are recorded rather than chosen between.
- Optimum wall thickness of tubular spars. Currey & Alexander 1985 (abstract) give different mass-optimal bore ratios for different design criteria; no single optimum follows from I alone.
:::

## Sources

| Citation | Read-level |
|---|---|
| Combes SA, Daniel TL (2003) Flexural stiffness in insect wings I. Scaling and the influence of wing venation. J Exp Biol 206(17):2979-2987, doi 10.1242/jeb.00523 | `abstract` |
| Ribak G, Stearns O, Sundararajan K, Dickerson-Evans D, Melamed D, Rabinovich M, Gurka R (2025) Insect wing flexibility improves the aerodynamic performance of small revolving wings. iScience, doi 10.1016/j.isci.2025.112035, PMC11927721 | `full-text` |
| Puri S, Aegerter-Wilmsen T, Jazwinska A, Aegerter CM (2018) In vivo quantification of mechanical properties of caudal fins in adult zebrafish. J Exp Biol 221(4):jeb171777, doi 10.1242/jeb.171777 | `abstract` |
| Alben S, Madden PGA, Lauder GV (2007) The mechanics of active fin-shape control in ray-finned fishes. J R Soc Interface 4(13):243-256, doi 10.1098/rsif.2006.0181 | `abstract` |
| Brazier LG (1927) On the flexure of thin cylindrical shells and other thin sections. Proc R Soc Lond A 116:104-114, doi 10.1098/rspa.1927.0125 | `abstract` |
| Currey JD, Alexander RMcN (1985) The thickness of the walls of tubular bones. J Zool 206:453-468, doi 10.1111/j.1469-7998.1985.tb03551.x | `abstract` |
| Cowper GR (1966) The shear coefficient in Timoshenko's beam theory. J Appl Mech 33:335-340, doi 10.1115/1.3625046 | `listing` |
| Euler-Bernoulli cantilever and Timoshenko shear results (standard textbook mechanics, e.g. Timoshenko & Gere, Mechanics of Materials) | `could-not-access` |
| This entry's own calculations: shear ratio, elastica shooting (pure-Python RK4 + bisection), equal-mass tube ratios, cantilever mode root, zebrafish k and exponent conversions | `full-text` |


---

*Generated from [`library/laws/second-moment.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/second-moment.yaml). Do not edit this page; edit the YAML.*
