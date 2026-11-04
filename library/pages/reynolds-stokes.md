---
title: The Stokes regime boundary, and what changes below Re ~1
label: law-reynolds-stokes
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-reynolds-stokes
F_D = 3\pi\mu U d = 6\pi\mu U a, \qquad C_D \equiv \frac{F_D}{\tfrac12\rho U^2 \tfrac{\pi}{4} d^2} = \frac{24}{\mathrm{Re}_d}\Big(1 + \tfrac{3}{16}\mathrm{Re}_d + \dots\Big), \qquad \mathrm{Re}_d = \frac{\rho U d}{\mu}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `F_D` | M*L/T^2 | N | steady drag on a rigid sphere translating at constant speed through quiescent fluid |
| `mu` | M/(L*T) | Pa*s | dynamic viscosity of a Newtonian fluid (a constant, not a shear-rate-dependent apparent viscosity) |
| `U` | L/T | m/s | speed of the sphere relative to the undisturbed far-field fluid |
| `d` | L | m | sphere DIAMETER; the radius form is 6*pi*mu*U*a with a = d/2 |
| `a` | L | m | sphere radius (used in the radius form and the unsteady worked example) |
| `rho` | M/L^3 | kg/m^3 | fluid density; absent from the Stokes law itself and enters only through Re and the inertial corrections |
| `Re_d` | 1 | dimensionless | Reynolds number on DIAMETER, rho*U*d/mu. Veysey & Goldenfeld use R = U*a/nu = Re_d/2 |
| `C_D` | 1 | dimensionless | drag coefficient normalised by 0.5*rho*U^2 times frontal area; Stokes gives 24/Re_d in this normalisation |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `stokes_prefactor` | 3*pi (diameter form) = 6*pi (radius form) | Derived, not measured: the exact solution of the Stokes (Re -> 0) equations with no-slip on a rigid sphere (Stokes 1851, not read; attribution as in Veysey & Goldenfeld 2007, read full text). |
| `C_D_stokes_coefficient` | 24 dimensionless (area normalisation, diameter Re) | CONVENTION TRAP. Veysey & Goldenfeld (2007, full text, their Eqn. 1 and the line defining C_D for the sphere) define R = u*a/nu and C_D = F/(rho*U^2*a^2), and write the Stokes result as C_D = 6*pi/R. Converting their convention to the area normalisation used here (our arithmetic) gives 24/Re_d = 12/R, NOT 6*pi/R. The two C_D values differ by a factor of pi/2 at the same force. A drag coefficient copied between sources without its normalisation is wrong by that factor. |
| `oseen_first_correction` | 3/16 per unit Re_d (= 3/8 per unit R) | Veysey & Goldenfeld (2007, full text, Eqn. 55) give the matched-asymptotics result C_D = (6*pi/R)[1 + (3/8)R + (9/40)R^2 log R + ...]. The 3/16 is our conversion with Re_d = 2R. They state that this "Oseen" term lies beyond the accuracy of Oseen's own analysis and is justified only by matched asymptotics (Proudman & Pearson 1957; Chester & Breach 1969), and that Illingworth's unpublished 1947 result also justifies it. That history is contested; see contested_by. |
| `schiller_naumann_correlation` | C_D = (24/Re_d)*(1 + 0.15*Re_d^0.687) | EMPIRICAL fit. The primary paper (Schiller & Naumann 1933) was not accessed. The form was seen at search-summary level only. A vendor manual (Rocky DEM, search-summary) states a maximum deviation of 5% from experiment, and OpenFOAM-style implementations switch it off above Re = 1000 (forum code, search-summary). The validity range at the LOW end is not verified: I found no source stating that it holds below Re_d ~0.2, so the values below 0.2 are extrapolations. Scope of that negative: two web searches, no handbook (Clift, Grace & Weber 1978) consulted. Uncertainty on 0.15 and 0.687: unknown. |
| `tolerance_boundary_Re_d` | Stokes drag within 1%: Re_d < 0.05 (Oseen) or < 0.02 (Schiller-Naumann). Within 5%: Re_d < 0.27 or < 0.20. Within 10%: Re_d < 0.53 or < 0.55 | CALCULATED in this entry by inverting the two corrections above, not observed. This is the number an engineer checks a design against. The two estimates are kept separate, not averaged. The Schiller-Naumann values below Re_d 0.2 are extrapolations (see above). |
| `stokes_underestimate_vs_Re_d` | Oseen / Schiller-Naumann: +1.9% / +3.1% at Re_d 0.1; +9.4% / +9.3% at 0.5; +18.8% / +15.0% at 1; +190% / +73% at 10; +1900% / +355% at 100 | CALCULATED here; each value is how much larger the corrected drag is than the Stokes drag. The two agree only near Re_d 0.5. Above Re_d 1 the Oseen term is outside its asymptotic validity, and the values at 10 and 100 show divergence, not a prediction. Use Schiller-Naumann there, or data. |
| `wall_ratio_for_2pct` | 100 container diameter / sphere diameter | Tritton, as quoted in Veysey & Goldenfeld (2007, full text, p. 18 of the arXiv version): "the container diameter must be more than one hundred times the sphere diameter for the error to be less than 2 percent". The same review relays Lindgren (1999): a ratio of 50 gives a 4% change in drag. I did not read Tritton or Lindgren. |
| `best_measurement_error` | 0.02 fraction of drag | Maxworthy's own estimate for his 1965 falling-sphere data (container over 700 sphere diameters), as reported by Veysey & Goldenfeld (full text). Maxworthy, as quoted there, also says the earlier data could not fix drag better than +/-20% once it is normalised by the Stokes drag. |

## Why it holds

Re_d compares inertial with viscous stress. As Re -> 0 the inertial term of Navier-Stokes drops out. The remaining Stokes equations are LINEAR in velocity and have NO time derivative, and every qualitative change below Re ~1 follows from those two facts. (a) Drag is linear in speed and in LENGTH, F = 3*pi*mu*U*d, not area times U^2. Halving speed halves drag, power goes as U^2, and fluid density drops out. (b) No inertial coasting: a body stops in a distance set by its own (and its added) inertia, which is sub-angstrom for a micron body (worked example, calculated). (c) Kinematic reversibility: the sequence of shapes, not the rate, sets the displacement. Lauga (2011, full text) states the scallop theorem and quotes Purcell (1977): "Fast, or slow, it exactly retraces its trajectory, and it's back where it started". A reciprocal stroke gives no net motion in a Newtonian fluid with no inertia. My inference from (a) to (c), not a cited claim: gliding, flap-and-coast and circulation-based lift have no physical basis in this regime. The regime is a limit, not a sharp threshold, and it cannot be uniform. Veysey & Goldenfeld (2007, full text) show that the inertial-to-viscous ratio grows with distance from the body as O(R*r/a). For any nonzero R, inertia therefore dominates far enough away. The Stokes solution is right near the body and wrong far from it, which is why the perturbation series is singular.

## Where it holds

- **flow regime**: steady creeping flow, Re_d << 1
- **reynolds max**: Re_d about 0.02-0.05 for 1% drag error, 0.2-0.27 for 5%, and about 0.55 for 10% (CALCULATED, see constants.tolerance_boundary_Re_d). 'Re ~1' is a tolerance choice of roughly 15-19%, not a transition
- **geometry**: rigid sphere; other compact 3D bodies need a shape factor that is NOT recorded here; unbounded fluid with container more than 100 sphere diameters for under 2% wall error
- **fluid**: Newtonian, incompressible, continuum (body much larger than the gas mean free path), no slip
- **motion**: steady, or slow enough that the body's relaxation time far exceeds the viscous diffusion time a^2/nu (see break 7)
- **taxa**: ['bacteria and protists (body scale)', 'cilia and flagella (appendage scale; slender, so break 2 applies)', 'sperm', 'settling cells, eggs, marine snow and particles']
- **notes**: No swimming stage of zebrafish is in this regime. van Leeuwen et al. (2015; abstract read) report Re 60 to 1400 for cyclic swimming of larvae aged 2 to 5 dpf, defined on body length and centre-of-mass speed. My inference: in this project the Stokes law applies to cilia, sperm, particles and flow inside small structures, never to the fish's own locomotion. The lowest observed larval Re is still about two orders of magnitude above the 10% boundary.


:::{danger} Where it breaks
(1) FINITE Re: the main failure, and a quantitative one. Inertia adds drag to the Stokes value. To keep the drag error under 5% you need Re_d < ~0.2-0.27, and under 1% you need Re_d < ~0.02-0.05 (both CALCULATED from the Oseen term and the Schiller-Naumann fit, kept separate). At Re_d = 1 Stokes underestimates drag by 15-19% (calculated). Veysey & Goldenfeld (full text) report "large deviations between theory and experiment for R ~ 0.5" (Re_d ~ 1) even for the best matched-asymptotic expansion. They quote Proudman that the numerical "convergence" is "particularly disappointing", and Van Dyke that the higher-order terms barely extend the range. At Re_d = 100 (the lower end of larval-fish Re), Schiller-Naumann puts sphere drag at 4.5x the Stokes value (calculated); there the law is wrong by a factor, not by a percentage. (2) TWO-DIMENSIONAL BODIES: the Stokes equations have no solution for flow past an infinite cylinder (Stokes's paradox). Veysey & Goldenfeld (full text) report that the paradox holds for any unbounded 2D flow (Krakowski & Charnes 1953). They show by dimensional analysis that the R -> 0 force per unit length would be independent of the cylinder radius, which is absurd. A fin ray, filament or flagellum modelled as a long cylinder cannot use the sphere law; its drag depends on log(Re) or log(aspect ratio). The correct slender-body coefficients were NOT verified in this session and are not given. (3) FAR FIELD: inertia dominates beyond r ~ a/R (Veysey & Goldenfeld). My inference: a superposed Stokes interaction between bodies many radii apart is not trustworthy, even when each body's own Re is tiny. (4) WALLS AND CONFINEMENT: the law assumes unbounded fluid. Tritton (as quoted) needs a container diameter over 100x the sphere diameter for under 2% error, and Lindgren (as relayed) gives 4% at 50x. Maxworthy (as quoted) attributes the +/-20% scatter of pre-1965 data mainly to uncorrected wall effects. A cell in a capillary, a cilium beside an epithelium or a particle in a microchannel violates this assumption, and the error grows with confinement. (5) RAREFIED GAS: when the particle approaches the gas mean free path (about 0.066-0.07 um in air), the no-slip continuum assumption fails, and Stokes OVER-predicts drag by the Cunningham factor Cc. From the Davies constants (Cc = 1 + Kn*(1.257 + 0.400*exp(-1.10/Kn)), Kn = 2*lambda/d; search-summary, also written with 0.55*d/lambda in the exponent, which is the same thing) I CALCULATE Cc = 1.17 at d = 1 um and 2.9 at 0.1 um. A Clarkson course table (search-summary) gives 1.17 and 3.01 with lambda = 0.07 um. The break does not apply in water at these sizes. (6) NON-NEWTONIAN FLUIDS (mucus, biofilm matrix, most biological gels): a constant mu does not describe them, so the drag law fails. The kinematic consequence also fails. Lauga (2011, full text) gives three ways a reciprocal stroke can produce net motion in complex fluids: rate-dependent (shear-thinning) viscosity, normal-stress differences and stress relaxation. Each is cited there to theoretical work (with flapping-force experiments for normal stresses). (7) UNSTEADY MOTION: the steady law omits added mass and the Basset-Boussinesq history force. The full linear equation (Maxey & Riley 1983 with later corrections, as stated in Farazmand & Haller 2015, full text) contains both. Farazmand & Haller report that the history term was routinely neglected until experiments and simulations showed it matters quantitatively and qualitatively. Criterion (my inference from the time scales): the quasi-steady law is self-consistent only if the body's relaxation time m/(6*pi*mu*a) far exceeds the vorticity diffusion time a^2/nu. That ratio is (2/9)(rho_p/rho_f), so for any body near neutral buoyancy, which covers every cell and larva, the unsteady forces are leading order whenever the body accelerates. The coasting example below shows the size of the effect.
:::

## Worked examples

**rigid 1 um-radius sphere in water, near neutral buoyancy, impulsively given 30 um/s and then free (a bacterium-scale coasting test)**

```
Quasi-steady (WRONG model here): tau = 2*rho_p*a^2/(9*mu) = 2.22e-7 s, so x = U*tau = 6.7e-12 m. Unsteady linear (BBO) model, quiescent fluid, solved in Laplace space: V(p) = J/((m_p+m_a)p + 6*pi*mu*a + 6*pi*a^2*sqrt(rho_f*mu*p)), with impulse J = (m_p+m_a)U and added mass m_a = rho_f*V_sphere/2. Final-value theorem: X = V(p->0) = J/(6*pi*mu*a) = U*(m_p+m_a)/(6*pi*mu*a) = 1.0e-11 m. Numerical inverse Laplace (mpmath Talbot) gives x(t) = 5.2e-12 m at 1 us, 8.2e-12 m at 10 us and 9.94e-12 m at 10 ms, which converges to the closed form.

```

- value: `1e-11`

- CALCULATED (an analytical result cross-checked by numerical inversion), not observed. The inputs are assumed round numbers (rho_p = rho_f = 1000 kg/m^3, mu = 1e-3 Pa*s, U = 30 um/s), not measurements of any species. Three results: (i) the total distance is 1.5x the quasi-steady value. The added mass sets the change; the history force does NOT change the total, because its Laplace term vanishes as p -> 0. (ii) The history force changes the SHAPE of the motion. Velocity decays algebraically (about t^-3/2, measured from the inversion: v/U = 2.8e-3 at 10 us against 3e-20 for the exponential), so about 18% of the distance is still to go after 10 us. (iii) Either way the distance is sub-angstrom, so "no coasting" stands. CAVEAT: the result holds for an impulsively started sphere in fluid at rest. A self-propelled swimmer that stops is force-free and leaves a different flow behind it, so it is a different initial condition, which I did not solve. A dimensional estimate in this project's challenge-53 review (U*a^2/nu = 3e-11 m) differs from this closed form by 3x; both are recorded and not reconciled.

- evidence: **derived**

**10 um particle settling in water, density excess 50 kg/m^3 (assumed)**

```
v = drho*g*d^2/(18*mu) = 50*9.81*(1e-5)^2/(18*1e-3) = 2.7e-6 m/s; check Re_d = v*d/nu = 2.7e-6*1e-5/1e-6 = 2.7e-5
```

- value: `2.7e-06`

- CALCULATED. Re_d is three orders below the 1% boundary, so the answer is self-consistent to within the assumed inputs. The pattern is the point: compute Re_d FROM the Stokes answer, then check it against the tolerance boundary before you trust the answer.

- evidence: **derived**

**cilium-scale appendage (length 10 um, tip speed 1 mm/s, assumed) in water**

```
Re = U*L/nu = 1e-3*1e-5/1e-6 = 0.01
```

- value: `0.01`

- CALCULATED from assumed kinematics, not measured ones. This is inside the Stokes regime, but a cilium is slender, so break (2) applies and the sphere law is the wrong model even here.

- evidence: **derived**

**larval Danio rerio, equivalent-sphere comparison at Re_d = 100**

```
Schiller-Naumann factor 1 + 0.15*100^0.687 = 4.55
```

- value: `4.55`

- CALCULATED. This is a sphere drag ratio, not a fish drag, and a body-length Re is not a sphere- diameter Re. It shows only that the linear Stokes law, applied near the low end of observed larval Re (60-1400; van Leeuwen et al. 2015, abstract), would underpredict drag several-fold.

- evidence: **derived**

:::{seealso} Contested
- Faxen (1923), as reported in Veysey & Goldenfeld (2007, full text): when Oseen's equation is properly solved it gives the Stokes drag with NO 3R/8 term; Bohlin (1960) and Haberman & Saure (1958, spelled so in the review) are reported to concur. Against this, the same review says Faxen actually solved a BOUNDED-flow problem, and that matched asymptotics (Proudman & Pearson 1957) and Illingworth's unpublished 1947 work justify the 3/8 term. Recorded as reported, not reconciled.
- Pruppacher's sphere-drag data (Eqn. 27 of the review) disagree with every other experimental and numerical result for R < 1 but agree for R > ~20; Veysey & Goldenfeld disregard them at low R. Pruppacher and Steinberger (1968), as quoted there, in turn criticised Maxworthy's setup. That is the review's judgement against Pruppacher's, not re-examined here.
- The first inertial correction near Re_d 0.1-1 differs between the Oseen asymptotic term and the Schiller-Naumann fit: 1.6x larger in SN at Re_d 0.1 and 0.8x at Re_d 1 (calculated). Neither is preferred: the asymptotic term is exact only as Re -> 0, and the fit is unverified below Re_d ~0.2.
- Coasting distance of a micron sphere: 1.0e-11 m (closed-form unsteady Stokes, impulsive start, this entry) against an order-of-magnitude estimate of 3e-11 m (challenge-53 review, dimensional reasoning) against 6.7e-12 m (quasi-steady, earlier unmerged entry 44fa61f7). All three are calculated; none is observed.
:::

## Sources

| Citation | Read-level |
|---|---|
| Veysey J II, Goldenfeld N (2007) Simple viscous flows: from boundary layers to the renormalization group. Rev Mod Phys 79:883-927. arXiv:physics/0609138v2 | `full-text` |
| Lauga E (2011) Life around the scallop theorem. Soft Matter 7:3060-3065. arXiv:1011.3051 | `full-text` |
| Purcell EM (1977) Life at low Reynolds number. Am J Phys 45:3-11 | `could-not-access` |
| Farazmand M, Haller G (2015) The Maxey-Riley equation: existence, uniqueness and regularity of solutions. Nonlinear Anal Real World Appl. arXiv:1310.2450 | `full-text` |
| Maxey MR, Riley JJ (1983) Equation of motion for a small rigid sphere in a nonuniform flow. Phys Fluids 26:883-889. doi:10.1063/1.864230 | `search-summary` |
| Proudman I, Pearson JRA (1957) Expansions at small Reynolds numbers for the flow past a sphere and a circular cylinder. J Fluid Mech 2:237-262 | `listing` |
| Stokes GG (1851) On the effect of the internal friction of fluids on the motion of pendulums. Trans Camb Phil Soc 9 (part II) | `listing` |
| Schiller L, Naumann A (1933) Z. Ver. Dtsch. Ing. 77 (pages not verified) | `could-not-access` |
| Davies CN (1945) Definitive equations for the fluid resistance of spheres. Proc Phys Soc 57 (pages not verified); Cunningham correction tables, Clarkson University ME437 aerosol notes | `search-summary` |
| van Leeuwen JL, Voesenek CJ, Mueller UK (2015) How body torque and Strouhal number change with swimming speed and developmental stage in larval zebrafish. J R Soc Interface 12:20150479. doi:10.1098/rsif.2015.0479 | `abstract` |
| docs/research/fish/challenge-53.md (this repository, branch claude/challenge-53-reynolds-stokes-upfryp) and library/laws/reynolds-stokes.yaml at commit 44fa61f7 (branch claude/reynolds-stokes-law-ar3x7v, unmerged) | `full-text` |


---

*Generated from [`library/laws/reynolds-stokes.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/reynolds-stokes.yaml). Do not edit this page; edit the YAML.*
