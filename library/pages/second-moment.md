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
| `k` | M/T^2 | N/m | tip bending stiffness of a cantilevered spar under a point load at the tip |
| `F` | M*L/T^2 | N | transverse force applied at the tip |
| `delta` | L | m | transverse tip deflection (small-deflection) |
| `E` | M/(L*T^2) | Pa | Young's modulus of the spar material along the span |
| `I` | L^4 | m^4 | second moment of area of the cross-section about the neutral axis, I = integral of y^2 over the section |
| `L` | L | m | span: free length from the clamped root to the loaded tip |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `tip_load_coefficient` | 3 | Exact, derived from Euler-Bernoulli theory for a uniform cantilever with a point load at the tip (delta = F L^3 / 3EI). Not measured, so no interval. A uniformly distributed load w per unit span gives delta = w L^4 / 8EI instead; using the wrong load case is a factor-of-2.7 error. |
| `section_forms` | solid circle I = pi r^4 / 4; thin-walled tube I = pi r^3 t (t << r); solid rectangle I = b h^3 / 12 (h in the bending direction) | Exact geometric results, not measured. The r^4 and h^3 dependence is the whole engineering content: doubling depth h multiplies I by 8, doubling width b only by 2, which is why spars are deep and why tubes beat rods for the same mass. |
| `zebrafish_caudal_fin_EI` | unknown (interval 1.5e-09 to 4e-09) N*m^2 | MEASURED (in vivo, anaesthetised adult Danio rerio, whole caudal fin, micro-Newton cantilever loading; Puri et al. 2018) as reported in a search summary I could not check against the full text: the range varies along the proximal-distal axis non-monotonically. No central value is given here because I did not read one. The search summary also states the authors computed EI from EI = F L^3 / (3 y) with an effective length -- i.e. THIS law, inverted. |
| `insect_spanwise_EI_exponent` | 3 | MEASURED interspecific scaling exponent of spanwise flexural stiffness against wing span, 16 insect species from six orders (Combes & Daniel 2003, from abstract-level summaries). The confidence interval is unknown: I could not reach the full text (two publisher/mirror hosts were outside this session's network allowlist), so only the rounded exponent is recorded. |

## Why it holds

Under pure bending a plane section stays plane and rotates, so axial strain grows linearly with distance y from the neutral axis, and (for a linear-elastic material) so does stress. The resisting moment is the integral of stress times lever arm, which puts y in twice: M = (E/R) * integral(y^2 dA) = E I / R. Material far from the neutral axis therefore counts with the square of its distance -- the reason I-beams, tubes and leading-edge vein complexes put material at the periphery. Integrating the curvature M/EI along a cantilever with a tip load gives delta = F L^3 / 3EI. The span enters as L^3 because the root moment grows as L and that curvature is then integrated twice over L. Scaling corollaries (DERIVED here, not observed): at fixed cross-section, k scales as L^-3, so doubling span cuts tip stiffness by 8x. Under geometric similarity (all lengths scale together) I scales as L^4 and k scales as E*L, so a larger isometric spar is stiffer in absolute terms; but its relative self-weight sag delta/L = rho g A L^3 / (8 E I) scales as L (Galileo's square-cube penalty), while relative deflection under an aerodynamic load at fixed dynamic pressure (load per span proportional to chord) is size-independent.

## Where it holds

- **theory**: Euler-Bernoulli (plane sections remain plane and normal to the neutral axis)
- **material**: linear-elastic, homogeneous along the span, same modulus in tension and compression
- **geometry**: slender (span-to-depth L/h well above 10 for an isotropic section -- see where_it_breaks for the derived boundary); prismatic, or I(x) integrated explicitly if tapered
- **deflection**: small: tip slope and delta/L small (under 1% error while delta/L < 0.1 for a tip load -- derived, see where_it_breaks)
- **loading**: static, quasi-static, or dynamic well below the first bending natural frequency
- **notes**: Valid for engineered spars (tubes, box beams, rods) and as a first approximation for single biological elements such as insect leading-edge veins or a single fin ray, provided the composite-section caveats in where_it_breaks are honoured.


:::{danger} Where it breaks
(1) SHORT, DEEP OR SHEAR-SOFT SPANS. Euler-Bernoulli ignores shear deformation. DERIVED here from Timoshenko beam theory for a tip-loaded rectangular cantilever (shear correction 5/6): shear adds a fraction 0.3 (E/G)(h/L)^2 to the bending deflection. For an isotropic material (nu = 0.3, E/G = 2.6) that is 0.8% at L/h = 10, 3.1% at L/h = 5 and 8.7% at L/h = 3. For anisotropic or shear-soft material the boundary moves out sharply: with an assumed E/G = 20 (illustrative of fibre composites and fibrous biological tissue, not a measured value for any organism) shear adds 6% even at L/h = 10 and 24% at L/h = 5. So the familiar "L/h > 10" rule is only safe for isotropic metals. (2) LARGE DEFLECTION. The linear formula assumes small slopes. COMPUTED here by shooting the inextensible elastica for a vertical tip load (scratch computation, not an observation): the linear formula over-predicts tip deflection by 1% at true delta/L = 0.10, 5% at delta/L = 0.21 and 10% at delta/L = 0.30 (load parameter F L^2/EI = 0.30, 0.68, 0.98). Beyond that the spar stiffens geometrically and k is no longer a constant. Flapping wings and fins routinely exceed delta/L = 0.2. (3) THIN-WALLED TUBES. Bending ovalises the section and progressively reduces I (Brazier 1927), giving a limit-point collapse; in practice local shell buckling usually precedes it. I = pi r^3 t overstates the stiffness of a thin tube near its collapse moment, and the law gives no collapse load at all. (4) COMPOSITE OR SLIDING SECTIONS -- the case that matters for fish. A ray-finned fin ray is two hemitrichs that can slide past each other (Alben, Madden & Lauder 2007). DERIVED here: two layers of thickness h bonded together give I = 8 b h^3/12; the same two layers free to slide give 2 b h^3/12 -- a factor of 4 from interlayer coupling alone, with real rays somewhere between, set by the connective tissue's shear stiffness, which this law does not contain. Distal fin rays are also segmented, so E is not uniform along the span. (5) SPAN SCALING IN ORGANISMS. The isometric prediction EI proportional to L^4 does NOT describe insect wings: measured spanwise EI scales approximately with span^3 (Combes & Daniel 2003). Using the isometric exponent to scale a biological spar up or down is therefore a demonstrated error, not a safe default.
:::

## Worked examples

**generic spar, fixed cross-section, span doubled**

```
k2/k1 = (L1/L2)^3 = (1/2)^3 = 0.125
```

- value: `0.125`

- Same tube, twice the span: one-eighth the tip stiffness. Derived from the law, not observed.

- evidence: **derived**

**generic spar, geometrically similar, all lengths doubled**

```
I2/I1 = 2^4 = 16;  k2/k1 = 16 / 2^3 = 2;  self-weight delta/L ratio = 2
```

- value: `2`

- Isometric scaling doubles tip stiffness yet also doubles relative sag under self-weight. Derived; and see where_it_breaks (5) -- insect wings do not scale isometrically.

- evidence: **derived**

**Danio rerio caudal fin, back-calculated tip stiffness**

```
k = 3 EI / L^3 with EI in [1.5e-9, 4.0e-9] N m^2 (measured, Puri et al. 2018, search-summary) and an ASSUMED effective length L = 5e-3 m  ->  k = 4.5e-9/1.25e-7 to 1.2e-8/1.25e-7 = 0.036 to 0.096 N/m
```

- value range: `[0.036, 0.096]`

- Calculated, not measured. EI is the authors' measurement; the 5 mm effective length is my assumption for illustration, not a value taken from the paper, and k scales as L^-3 so the result is only as good as that assumption. Note also that the whole-fin EI already lumps rays and interray tissue, so where_it_breaks (4) applies.

- evidence: **derived**

**insect wings, 16 species from six orders**

- Measured spanwise flexural stiffness scales with roughly the cube of wing span, and chordwise stiffness with the square of chord; wing size explains over 95% of the variance (Combes & Daniel 2003, per abstract-level summaries). MY INFERENCE, not the authors' claim: an exponent of 3 rather than the isometric 4 means larger insect wings are relatively more flexible than a geometrically scaled spar would be.

- evidence: **literature**

:::{seealso} Contested
- Exponent of EI against wing size in insects: Combes & Daniel (2003) report interspecific spanwise EI ~ span^3 and chordwise EI ~ chord^2. Ribak et al. (2025, iScience; summary-level read) state that WITHIN a beetle species chordwise stiffness grows with chord^4, attributing this to an earlier flower-chafer (Protaetia cuprea) study. Interspecific and intraspecific exponents disagree; this entry does not reconcile them, and isometry (EI ~ L^4) is a third, separate prediction.
:::

## Sources

| Citation | Read-level |
|---|---|
| Timoshenko SP, Gere JM, Mechanics of Materials (standard Euler-Bernoulli and Timoshenko beam results; cantilever tip-load formula) | `could-not-access` |
| Combes SA, Daniel TL (2003) Flexural stiffness in insect wings I. Scaling and the influence of wing venation. J Exp Biol 206(17):2979-2987 | `search-summary` |
| Puri S, Aegerter-Wilmsen T, Jazwinska A, Aegerter CM (2018) In vivo quantification of mechanical properties of caudal fins in adult zebrafish. J Exp Biol 221(4):jeb171777 | `search-summary` |
| Alben S, Madden PG, Lauder GV (2007) The mechanics of active fin-shape control in ray-finned fishes. J R Soc Interface 4(13):243-256 | `search-summary` |
| Brazier LG (1927) On the flexure of thin cylindrical shells and other thin sections. Proc R Soc Lond A 116:104-114 | `search-summary` |
| Ribak G et al. (2025) Insect wing flexibility improves the aerodynamic performance of small revolving wings. iScience (PMC11927721) | `search-summary` |
| This entry's own scratch computations: Timoshenko shear-to-bending ratio 0.3 (E/G)(h/L)^2 and elastica shooting solution for a tip-loaded cantilever (scipy solve_ivp + brentq) | `full-text` |


---

*Generated from [`library/laws/second-moment.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/second-moment.yaml). Do not edit this page; edit the YAML.*
