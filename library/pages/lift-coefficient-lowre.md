---
title: Measured maximum lift coefficient of thin plates at Re 1e3 to 1e4
label: law-lift-coefficient-lowre
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-lift-coefficient-lowre
C_{L,\max} = \frac{2\,L_{\max}}{\rho\,U^{2}\,S}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `CL_max` | 1 | dimensionless | maximum lift coefficient over angle of attack, for one wing, one motion and one Re |
| `L_max` | M*L/T^2 | N | largest lift measured over the angle-of-attack sweep |
| `rho` | M/L^3 | kg/m^3 | fluid density |
| `U` | L/T | m/s | free-stream speed (translating plate) or speed at a reference radius (revolving plate) -- the two are NOT interchangeable |
| `S` | L^2 | m^2 | planform area of the plate (chord x span) |
| `Re` | 1 | dimensionless | chord Reynolds number U*c/nu; see reynolds.yaml |
| `alpha` | 1 | rad | geometric angle of attack |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `CLmax_thin_airfoil_steady_Re1e4` | 0.8 dimensionless | MEASURED (wind tunnel), but read SECONDHAND. Cheng & Sun (2016, Sci. Rep., full text read via Europe PMC) write "at Re = 10^4 the maximum lift coefficient of a thin airfoil is about 0.8", citing Okamoto, Yasuda & Azuma (1996). We read only the Okamoto et al. abstract, which gives the Re range (10^3 to 10^4) and the parameters varied (camber, thickness, leading-edge sharpness, roughness) but no CLmax. So the plate geometry behind "about 0.8" (flat or cambered, aspect ratio, thickness) is UNKNOWN to us, and no interval is available. "About" is the citing authors' word. Tried for the primary figure: the JEB article page (paywalled, abstract only), Europe PMC (abstract only), Semantic Scholar API (blocked by this session's network policy). |
| `CLmax_model_fruitfly_wing_Re100` | 0.6 dimensionless | MEASURED, read SECONDHAND, and OUTSIDE this entry's Re range -- recorded only as the low-Re anchor for the trend. Cheng & Sun (2016) write "at Re = 100, the maximum lift coefficient of a model fruitfly wing is about 0.6", citing Vogel (1967, J. Exp. Biol. 46:431-443). We did not read Vogel (1967). |
| `CLmax_translating_flat_plate_Re2e4_5e4` | 1.19 dimensionless | MEASURED (water channel, translating flat plate, AR 6, chord 76 mm, thickness 8 mm so t/c about 0.105, Re 20,000-50,000), ABOVE this entry's Re range, and the plate is thicker than "thin". Su, Fan, Onoue, Vejdani & Breuer (arXiv 2302.09602v2, full text read) fit their measurements with CL(alpha) = -0.44 exp(-0.47 alpha) + 1.19 sin(1.74 alpha + 20 deg) (alpha in degrees, R^2 > 0.995) and state the maximum is reached "at approximately alpha = 40 deg". The 1.19 here is OUR evaluation of THEIR fitted curve at its peak (the exponential term is negligible there), not a number they state. They report the four Re gave closely similar curves; we did not extract a per-Re spread, hence no interval. They also state their maximum CL is "approximately 45%" smaller than the revolving-wing value of Dickinson et al. (1999). |
| `CLmax_revolving_flat_card_wing` | 1.44 dimensionless | MEASURED on a REVOLVING (propeller-like) flat card replica of a pigeon wing (Usherwood 2009, Exp. Fluids 46:991-1003; read via an automated summarising fetch of the PMC full text), versus 1.64 for the dried real wing. Revolving, not translating -- an attached leading-edge vortex is the reason the number is high. The Re of this test is DISPUTED between sources we read: see contested_by. Either way it lies above 1e4, so it marks what a different motion delivers, not a value inside this entry's domain. |
| `stall_angle_steady_flat_plate` | unknown deg | Not found for Re 1e3-1e4 in any source we could read. The only measured stall angle in hand is the approximately 40 deg of Su et al. at Re 2e4-5e4 (translating, AR 6), which is outside the domain. |

## Why it holds

Below Re of about 1e4 the boundary layer on a plate stays laminar and separates at, or very close to, a sharp leading edge, so the conventional attached-flow route to high lift (suction peak around a rounded nose, turbulent reattachment) is unavailable. Lift at moderate-to-high incidence comes instead from the pressure difference across a separated plate, with a leading-edge vortex that on a steadily TRANSLATING 2D plate grows and sheds, capping CLmax well below the values seen on revolving or flapping wings where the vortex stays attached. Sunada et al. (1997, abstract) state that at Re = 4e3 the characteristics "are strongly affected by leading edge vortices", and that the best sections are thinner than high-Re sections, sharp-nosed, and cambered about 5% at mid-chord. The link from that vortex picture to a specific CLmax number is OUR inference from the sources, not a derivation any of them gives.

## Where it holds

- **reynolds min**: 1000
- **reynolds max**: 10000
- **motion**: steady translation (wind tunnel or towing tank); NOT revolving, flapping or impulsively started
- **geometry**: thin plates, flat or lightly cambered, sharp leading edge, moderate-to-high aspect ratio
- **notes**: The CLmax figure in hand (about 0.8, secondhand) is attributed to Re 1e4; we have no numeric value at Re 1e3 to 5e3. The steady, translating, high-aspect-ratio case is the one the number is for; every other case is in where_it_breaks.


:::{danger} Where it breaks
(1) MOTION. A revolving or flapping plate at the SAME Re is not covered: revolving model wings from Re 1100 to 26000 produce "high force coefficients" from a stably attached leading-edge vortex (Usherwood & Ellington 2002b, abstract; we have no numeric value from that paper), a revolving flat card wing reached CLmax 1.44 (Usherwood 2009), and Su et al. report their translating-plate maximum is about 45% below a revolving-wing value. Using the steady figure for a flapping wing UNDERSTATES lift; using a revolving figure for a gliding plate OVERSTATES it. This is the error the Reynolds entry warns about: carrying a CL across motion classes at equal Re. (2) LOW ASPECT RATIO. For a rectangular flat plate of AR 1, Okamoto, Sasaki, Kamikubo & Fujii (2019) report a large CLmax from tip-vortex lift at Re 1e4 that DECREASES as Re falls, i.e. the vortex lift "disappears" at very low Re, with a smaller decline at other aspect ratios (search-summary level; no numbers in hand). So a low-AR value measured at 1e4 cannot be carried down to 1e3. (3) CAMBER AND CORRUGATION. Camber raises CLmax in this range (Sunada et al. 1997; Okamoto & Ebina 2016 report high CLmax for large-camber circular arcs even below Re 3e3, search-summary), and dragonfly sections "attain much higher lift values than flat plates" at Re 7880 and 10,000 (Kesel 2000, abstract), so a flat-plate value is a FLOOR for sections of that kind, not an estimate. (4) BELOW Re ~1e3 the trend continues downward (about 0.6 for a model fruit-fly wing at Re 100, Vogel 1967 via Cheng & Sun 2016), so the Re 1e4 figure is not a floor for the whole insect range. (5) THICKNESS AND NOSE. Thicker, round-nosed sections do worse here (Sunada et al. 1997, abstract), so conventional airfoil data must not be substituted. (6) UNSTEADY ONSET. Impulsively started plates show transient lift above the steady value before the vortex sheds; a test that does not wait for the steady state will report a CLmax above this law's.
:::

## Worked examples

**Danio rerio candidate wing in air (the reynolds.yaml case)**

```
U = 2 m/s, chord c = 0.01 m, span 0.02 m (S = 2e-4 m^2, an ASSUMED planform for illustration), rho_air = 1.2 kg/m^3 (standard sea-level value), CL_max = 0.8  ->  L_max = 0.5*1.2*2^2*2e-4*0.8 = 3.84e-4 N, the weight of about 39 mg.

```

- value: `0.000384`

- CALCULATED, not observed, and an OVERESTIMATE of what is supported. The 0.8 is a secondhand figure for Re 1e4; this wing sits at Re 1333 (reynolds.yaml), an order of magnitude lower, where we hold no measured steady CLmax. Of the Re-trend sources we have, Okamoto et al. (2019) show CLmax falling with Re for an AR 1 plate, while Fujita & Iima (arXiv 2503.12039, 2D simulation) report flat-wing lift histories similar at Re 1500 and 4000; the planform here has AR 2, between those. Treat 39 mg as an upper-side number for a steadily gliding flat plate, not a design value.

- evidence: **derived**

**model and real dragonfly wing sections (Aeshna cyanea), wind tunnel**

- At Re 7880 and 10,000 all sections had CD,min < 0.06 "closely resembling those of flat plates", while lift was "much higher than flat plates" (Kesel 2000, abstract). No CLmax number in hand.

- evidence: **literature**

:::{seealso} Contested
- Re-dependence of flat-plate CLmax inside 1e3-1e4: Okamoto et al. (2019) report the maximum lift coefficient of an AR 1 flat plate DECREASES as Re falls below 1e4 (search-summary). Fujita & Iima (arXiv 2503.12039, simulation) report flat-wing CL histories similar at Re 1500 and 4000 and say this is consistent with experiments (Mueller 1999; Okamoto & Ebina 2016) in which flat-wing lift coefficient 'did not change when Re = O(10^3)'. The geometries differ (AR 1 three-dimensional plate vs 2D section), which may be the whole explanation; we have not tested that and do not reconcile it here.
- Steady vs revolving CLmax at similar Re: Cheng & Sun (2016) give about 0.8 for a steady thin airfoil at Re 1e4; revolving flat wings produce 'high force coefficients' over Re 1100-26000 (Usherwood & Ellington 2002b) and 1.44 for a flat card wing (Usherwood 2009). These are different motions, not conflicting measurements of one quantity -- recorded so the two are never averaged.
- Reynolds number of the Usherwood (2009) flat-card test: Su et al. (arXiv 2302.09602) describe that study as 'at Reynolds number up to 10,800'; our automated read of the Usherwood (2009) PMC full text reported the card wing tested at Re about 54,000 and 108,000. We have not resolved which is correct; the value is therefore not placed inside this entry's domain.
:::

## Sources

| Citation | Read-level |
|---|---|
| Cheng X, Sun M (2016) Wing-kinematics measurement and aerodynamics in a small insect in hovering flight. Sci. Rep. 6:25706. doi:10.1038/srep25706 (PMC4863373) | `full-text` |
| Okamoto M, Yasuda K, Azuma A (1996) Aerodynamic characteristics of the wings and body of a dragonfly. J. Exp. Biol. 199(2):281-294. doi:10.1242/jeb.199.2.281 | `abstract` |
| Sunada S, Sakaguchi A, Kawachi K (1997) Airfoil section characteristics at a low Reynolds number. J. Fluids Eng. 119(1):129-135. doi:10.1115/1.2819098 | `abstract` |
| Kesel AB (2000) Aerodynamic characteristics of dragonfly wing sections compared with technical aerofoils. J. Exp. Biol. 203(20):3125-3135. doi:10.1242/jeb.203.20.3125 | `abstract` |
| Usherwood JR, Ellington CP (2002a) The aerodynamics of revolving wings I. Model hawkmoth wings. J. Exp. Biol. 205(11):1547-1564. doi:10.1242/jeb.205.11.1547 | `abstract` |
| Usherwood JR, Ellington CP (2002b) The aerodynamics of revolving wings II. Propeller force coefficients from mayfly to quail. J. Exp. Biol. 205(11):1565 (end page not verified). doi:10.1242/jeb.205.11.1565 | `abstract` |
| Usherwood JR (2009) The aerodynamic forces and pressure distribution of a revolving pigeon wing. Exp. Fluids 46(5):991-1003. doi:10.1007/s00348-008-0596-z | `full-text` |
| Su Y, Fan X, Onoue K, Vejdani H, Breuer KS. An improved aerodynamic model for quasi-steady simulations of animal flight at moderate Reynolds numbers. arXiv:2302.09602v2 (2025) | `full-text` |
| Fujita Y, Iima M. Reynolds-number regimes of corrugation-induced lift enhancement in two-dimensional dragonfly-like wings. arXiv:2503.12039v2 | `full-text` |
| Okamoto M, Ebina K (2016) Effectiveness of large-camber circular arc airfoil at very low Reynolds numbers. Trans. JSASS 59(5):295-304. doi:10.2322/tjsass.59.295 | `search-summary` |
| Okamoto M, Sasaki D, Kamikubo T, Fujii S (2019) Disappearance of vortex lift in low-aspect-ratio wings at very-low Reynolds numbers. Trans. JSASS 62:310-317. doi:10.2322/tjsass.62.310 | `search-summary` |
| Vogel S (1967) Flight in Drosophila. III. Aerodynamic characteristics of fly wings and wing models. J. Exp. Biol. 46:431-443 | `listing` |
| Mueller TJ (1999) Aerodynamic measurements at low Reynolds numbers for fixed wing micro-air vehicles. RTO AVT/VKI Special Course | `listing` |


---

*Generated from [`library/laws/lift-coefficient-lowre.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/lift-coefficient-lowre.yaml). Do not edit this page; edit the YAML.*
