---
title: Hagen-Poiseuille viscous dissipation and the r^-4 cost that Murray's law rests on
label: law-hagen-poiseuille
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-hagen-poiseuille
P_{\mathrm{diss}} = \Delta P \, Q = \frac{8 \mu L Q^2}{\pi r^4}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `P_diss` | M*L^2/T^3 | W | viscous power dissipated in one tube segment (pressure drop times volume flow) |
| `mu` | M/(L*T) | Pa*s | dynamic viscosity of a Newtonian fluid |
| `L` | L | m | segment length |
| `Q` | L^3/T | m^3/s | volume flow rate through the segment |
| `r` | L | m | lumen radius (inner wall, circular section) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `radius_exponent` | -4 — *derived* | EXACT under the assumptions (steady, fully developed, laminar, Newtonian, rigid circular tube, no slip); not fitted. At fixed flow, dissipation scales as r^-4: a 10 per cent narrower tube dissipates 1/0.9^4 = 1.52 times the power. This is the exponent from which Murray's cube is derived (see worked_examples), so every failure listed under where_it_breaks is also a failure of Murray's premise. |
| `geometric_coefficient` | 2.546 — *derived* | 8/pi, for a CIRCULAR section only. Other sections have other coefficients and the r^-4 form itself has to be restated in terms of a hydraulic radius; the value is not portable. |
| `sustained_turbulence_reynolds` | 2040 (interval 2030 to 2050) dimensionless (Re = U*D/nu with D the diameter) — *measured* | MEASURED critical point for SUSTAINED turbulence in pipe flow, Avila et al. 2011 (Science 333:192-196); the +/-10 interval is from a conference abstract by the same group, read only via a search summary, NOT from the paper's main text, which was not retrieved. Below it turbulent puffs are transient; above it they split faster than they decay. This is not the Reynolds number at which laminar flow MUST end -- disturbance-free laminar pipe flow is reported far above it (remembered, not retrieved; no value asserted here) -- it is the number above which laminar flow can no longer be RELIED on. |
| `conifer_tracheid_endwall_fraction` | 0.64 (interval 0.6 to 0.68) — *measured* | MEASURED, Pittermann et al. 2006 (Am J Bot 93:1265-1273): 64 +/- 4 per cent of tracheid hydraulic resistivity resides in the end-wall pitting, regardless of tracheid size or phylogenetic affinity, across four conifer families. Read via search-summary of the abstract only. The interval is +/- one reported spread, and whether that is an SD or SE was not confirmed. |
| `eudicot_vessel_endwall_fraction` | 0.56 (interval 0.54 to 0.58) — *measured* | MEASURED, attributed to Hacke et al. 2006 (Tree Physiol 26:689-701): 56 +/- 2 per cent of vessel resistance in end walls. CONFIRMED ONLY SECOND-HAND -- a search summary relayed the number from text attributing it to that paper; the paper's own abstract was not seen. Treat as provisional. |
| `laminar_entrance_length_coefficient` | 0.06 — *tabulated-remembered* | L_e / D ~ 0.06 * Re for laminar entry flow. The VALUE is a standard textbook coefficient and is REMEMBERED, not retrieved; no source or interval was retrieved for it, and textbooks give slightly different coefficients. Within L_e the profile is not parabolic and dissipation exceeds the Hagen-Poiseuille value. |

## Why it holds

Hagen-Poiseuille flow is the exact solution of the Navier-Stokes equations for steady, fully developed, laminar flow of a Newtonian fluid through a rigid circular tube with no slip at the wall. The velocity profile is a paraboloid, u(s) = (dP/(4*mu*L)) * (r^2 - s^2); integrating it over the section gives Q = pi * r^4 * dP / (8 * mu * L), and multiplying the pressure drop by the flow gives the dissipated power P_diss = 8*mu*L*Q^2/(pi*r^4). The r^4 is two powers of r from the area and two from the velocity, which itself scales as r^2 because the wall shear acts over a distance r. All of the dissipation happens in shear, and the shear is largest at the wall. Murray (1926) set this cost, falling as r^-4, against a volume-maintenance cost rising as r^2; the cube law is what that trade-off returns when -- and only when -- the dissipation term has exactly this form.

## Where it holds

- **flow regime**: steady, fully developed, laminar
- **reynolds max**: 2040
- **fluid**: Newtonian, continuum (Knudsen number well below 0.01)
- **walls**: rigid, impermeable, no-slip, smooth
- **geometry**: circular section; segment long compared with the entrance length 0.06*Re*D
- **taxa**: ['mammalian small arteries and arterioles above the scale where blood stops behaving as a single-viscosity fluid (see the poiseuille entry for that boundary)', 'engineered microfluidic channels with liquids', 'plant xylem LUMENS, but not whole conduits (see where_it_breaks)']
- **notes**: The law is exact inside this domain. Outside it the law still returns a number, which is the hazard; the discriminators (Re, Womersley alpha, Kn, L/L_e, the end-wall fraction) have to be computed separately.

:::{danger} Where it breaks
It fails measurably above Re about 2040, where turbulence is sustained, and in plant xylem, where end-wall pits rather than the lumen carry 56-64 per cent of conduit resistance. Each failure below is a failure of an ASSUMPTION, and the useful question is what it does to the r^-4 exponent, because that exponent is what Murray's cube inherits. (1) TURBULENCE. Above Re about 2040 turbulence is sustained (Avila et al. 2011, measured), and in turbulent flow the dissipation stops scaling as Q^2 r^-4. My own derivation below (a calculation, not an observation) shows that with a constant Darcy friction factor it becomes Q^3 r^-5 and the Murray exponent becomes 7/3; with the Blasius smooth-pipe friction factor it becomes Q^(11/4) r^(-19/4) and the exponent 27/11 = 2.45. So a change of regime moves the optimal exponent by roughly 0.5-0.7, which the murray entry's worked example shows is measurable. (2) PULSATILE FLOW. When the Womersley number alpha = r*sqrt(omega*rho/mu) is well above 1 the profile is blunt rather than parabolic and wall shear is not the steady-flow value (Womersley 1955 is the standard source; listing only, not read). The poiseuille entry computes alpha about 19 for a human aorta from remembered inputs; the steady r^-4 term does not describe dissipation there. (3) ENTRANCE LENGTH. A parabolic profile needs about 0.06*Re*D of tube to develop (remembered coefficient). In a branching tree whose segments are only a few diameters long, much of each segment may be developing flow, where wall shear and dissipation EXCEED the Hagen-Poiseuille value; this is my inference from the coefficient and is quantified only in the worked example, not observed. (4) PLANT XYLEM, measured and large: the lumen is a Hagen-Poiseuille tube but the conduit is not. End-wall pitting carries 64 +/- 4 per cent of conifer tracheid resistance (Pittermann et al. 2006) and about 56 per cent of eudicot vessel resistance (attributed to Hacke et al. 2006, second-hand). My inference from those numbers: the lumen r^-4 term accounts for only roughly 36-44 per cent of the real resistance, so Hagen-Poiseuille OVER-predicts conduit conductivity by a factor of about 2.3-2.8, and an r^-4 optimum computed from lumen radius alone is optimising the minority of the cost. (5) RAREFIED GAS AND SLIP. No-slip fails when the Knudsen number Kn = lambda/D is no longer small. With a remembered mean free path for air near 68 nm, a tube of 0.2 micrometre diameter has Kn about 0.3 -- a derived figure, not a measurement of any organism -- which is the slip/transition regime, where flow per unit pressure exceeds Hagen-Poiseuille. Whether real insect tracheoles sit there was NOT checked: no diameter for them was retrieved. (6) BLOOD IN SMALL VESSELS. Apparent viscosity depends on diameter, so mu is not a constant and the effective radius exponent is not 4; the measured boundary and both directions of the error are recorded in the poiseuille entry and are not re-derived here. (7) GEOMETRY. A non-circular section changes 8/pi; a compliant or collapsible wall (veins, lymphatics) makes r a function of the pressure, so resistance stops being a fixed property of the tube.
:::

## Worked examples

**Murray's cube derived from the r^-4 term (generic tube, no organism)**

```
Total cost of one segment = dissipation + volume maintenance
  W(r) = 8*mu*L*Q^2/(pi*r^4) + b*pi*r^2*L        (b = metabolic cost per unit volume per time)
dW/dr = -32*mu*L*Q^2/(pi*r^5) + 2*b*pi*r*L = 0
  -> Q^2 = b*pi^2*r^6/(16*mu)  ->  Q = (pi/4)*sqrt(b/mu)*r^3
Flow conservation at a junction then gives r_0^3 = sum(r_i^3).
Corollary: wall shear tau = 4*mu*Q/(pi*r^3) = sqrt(b*mu), the same in every segment.
```

- value: `3`

- A CALCULATION, not an observation. The general form is worth keeping: if dissipation scales as Q^k * r^-m and maintenance as r^2, then Q is proportional to r^((m+2)/k). Hagen-Poiseuille has k = 2 and m = 4, giving 3. The exponent is therefore set entirely by the two powers in the dissipation term, which is why this entry exists.

- evidence: **derived**

**the same optimisation outside the laminar regime (generic tube)**

```
Darcy-Weisbach: dP = f * (L/(2r)) * rho * V^2 / 2,  V = Q/(pi*r^2)
  constant f (fully rough):  dP ~ Q^2 r^-5  -> P_diss ~ Q^3 r^-5
      k = 3, m = 5  ->  exponent (5+2)/3 = 7/3 = 2.33
  Blasius smooth pipe, f ~ Re^(-1/4) ~ (Q/r)^(-1/4):
      dP ~ Q^(7/4) r^(-19/4)  -> P_diss ~ Q^(11/4) r^(-19/4)
      k = 11/4, m = 19/4  ->  exponent (27/4)/(11/4) = 27/11 = 2.45
  laminar Hagen-Poiseuille: k = 2, m = 4 -> 3
```

- value: `2.33`

- DERIVED by me, not observed. The 7/3 matches the turbulent value that the murray entry says is commonly attributed to Uylings 1977 and is unverified there; this derivation shows the value FOLLOWS from a constant friction factor, but it does NOT verify that Uylings derived it or derived it this way. The Blasius form assumes a smooth pipe and moderate Re (remembered validity, not retrieved). Measured coronary exponents near 2.4-2.6 (murray entry) lie between these calculated values and 3, which is consistent with mixed or unsteady flow but is not evidence for it.

- evidence: **derived**

**sensitivity to a radius measurement error (generic tube)**

```
fixed Q:  P_diss ratio = (r_true/r_measured)^4
  radius overestimated by 10%: (1/1.1)^4 = 0.683  -> dissipation under-predicted by 32%
  radius underestimated by 10%: (1/0.9)^4 = 1.524 -> dissipation over-predicted by 52%
```

- value: `1.524`

- A design check against this law is only as good as the radius measurement, and a 10 per cent radius error is a 30-50 per cent dissipation error. For vessels imaged near the resolution limit this, rather than the law, dominates the uncertainty. Calculation, not observation.

- evidence: **derived**

**entrance length versus segment length in a branching tree (illustrative inputs)**

```
L_e = 0.06 * Re * D
  Re = 500, D = 4 mm  ->  L_e = 0.06*500*4 mm = 120 mm
  Re = 1,   D = 50 um ->  L_e = 0.06*1*50 um  = 3 um
```

- value: `120`

- Inputs are ILLUSTRATIVE, not measured values for any named vessel, and the 0.06 coefficient is remembered. The point is the scaling: at Re of order 100s a tube needs tens of diameters to develop a parabolic profile, so a large-vessel tree with segments only a few diameters long is mostly entrance flow, while at Re of order 1 the entrance length is negligible and the law holds segment by segment. Units of value: mm.

- evidence: **derived**

**conifer tracheid, lumen-only prediction against measured total resistance**

```
lumen fraction of resistance = 1 - endwall fraction
  conifer tracheid: 1 - 0.64 = 0.36  (range 0.32-0.40)
  eudicot vessel:   1 - 0.56 = 0.44  (range 0.42-0.46)
Hagen-Poiseuille lumen conductivity / true conductivity = 1/lumen fraction
  conifer: 1/0.36 = 2.8  (2.5-3.1)
  eudicot: 1/0.44 = 2.3  (2.2-2.4)
```

- value: `2.8`

- The end-wall fractions are MEASURED (sources above, read at search-summary level only); the over-prediction factors are MY ARITHMETIC on them, assuming the remaining resistance is lumen resistance well described by Hagen-Poiseuille, which the sources were not seen to state.

- evidence: **derived**

:::{seealso} Contested
- Priority. The law carries two names because Hagen (1839) and Poiseuille (1840-1841) obtained it independently; how the credit and the dates should be divided is treated in Sutera & Skalak 1993, which was seen only as a listing. No priority judgement is made here.
- Whether the r^-4 law holds for blood in the microcirculation is contested in BOTH directions: in vitro tube measurements show apparent viscosity falling with diameter, which lowers resistance, while in vivo resistance is reported higher than in vitro, attributed to an endothelial surface layer. Both are relayed from the poiseuille entry, whose sources were not re-read for this entry; the disagreement is recorded, not reconciled.
- Whether minimising Hagen-Poiseuille dissipation plus volume is the RIGHT objective for a biological network is disputed in the murray entry (generalised exponents, load-bearing conduits). That dispute is about Murray's objective function, not about this law; it is listed here so a reader does not take the exactness of the r^-4 as evidence for the optimality argument built on it.
:::

## Sources

| Citation | Read-level |
|---|---|
| Hagen GHL (1839) Ueber die Bewegung des Wassers in engen cylindrischen Roehren, Ann Phys Chem 46:423-442 | `could-not-access` |
| Poiseuille JLM (1840-1841) Recherches experimentales sur le mouvement des liquides dans les tubes de tres-petits diametres, Comptes Rendus Acad Sci 11 and 12 | `could-not-access` |
| Sutera SP, Skalak R (1993) The history of Poiseuille's law, Annu Rev Fluid Mech 25:1-20, doi 10.1146/annurev.fl.25.010193.000245 | `listing` |
| Avila K, Moxey D, de Lozar A, Avila M, Barkley D, Hof B (2011) The onset of turbulence in pipe flow, Science 333:192-196, doi 10.1126/science.1203223 | `search-summary` |
| Womersley JR (1955) Method for the calculation of velocity, rate of flow and viscous drag in arteries when the pressure gradient is known, J Physiol 127:553-563, doi 10.1113/jphysiol.1955.sp005276, PMC1365740 | `listing` |
| Pittermann J, Sperry JS, Hacke UG, Wheeler JK, Sikkema EH (2006) Inter-tracheid pitting and the hydraulic efficiency of conifer wood: the role of tracheid allometry and cavitation protection, Am J Bot 93:1265-1273, doi 10.3732/ajb.93.9.1265 | `search-summary` |
| Hacke UG, Sperry JS, Wheeler JK, Castro L (2006) Scaling of angiosperm xylem structure with safety and efficiency, Tree Physiol 26:689-701, doi 10.1093/treephys/26.6.689 | `listing` |
| Sperry JS, Hacke UG, Pittermann J (2006) Size and function in conifer tracheids and angiosperm vessels, Am J Bot 93:1490-1500 | `search-summary` |
| Murray CD (1926) PNAS 12:207-214, doi 10.1073/pnas.12.3.207 | `could-not-access` |
| library/laws/poiseuille.yaml and library/laws/murray.yaml (this library) | `full-text` |


---

*Generated from [`library/laws/hagen-poiseuille.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/hagen-poiseuille.yaml). Do not edit this page; edit the YAML.*
