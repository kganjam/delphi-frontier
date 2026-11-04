---
title: Measured maximum lift coefficient of thin plates at Re 1e3-1e4
label: law-lift-coefficient-lowre
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-lift-coefficient-lowre
L_{\max} = \tfrac{1}{2}\,\rho\,U^{2}\,S\,C_{L,\max}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `L_max` | M*L/T^2 | N | largest steady lift the wing can make at speed U |
| `rho` | M/L^3 | kg/m^3 | fluid density |
| `U` | L/T | m/s | steady free-stream (translational) speed |
| `S` | L^2 | m^2 | wing planform area |
| `C_Lmax` | 1 | dimensionless | maximum steady lift coefficient; measured, not derived |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `C_Lmax_cambered_plate_Re4e3` | 1.06 dimensionless | Best of the roughly fifteen sections Sunada et al. tested at Re = 4e3: a thin cambered plate with about 5% camber, reaching its maximum at alpha = 8 deg. The relaying summary also gives that section as 2.9% thick with maximum camber at 40% chord, so the "5% camber" label is not fully pinned down. No measurement uncertainty was retrieved, so the interval is `unknown`. Read level: search-summary. |
| `C_Lmax_flat_plate_Re4e3` | unknown (interval 0.42 to 0.53) dimensionless | Nobody reported this number as a number. The relaying source says the cambered plate's value is "higher by 100-150%" than the flat plate. My calculation 1.06/2.5 = 0.42 and 1.06/2.0 = 0.53 gives this interval, and it carries every weakness of that one relayed sentence. |
| `C_Lmax_dragonfly_isolated_wing_Re700_2400` | [1.07, 1.15] (interval 1.07 to 1.15) dimensionless | 1.07 is for Sympetrum sanguineum and 1.15 for Calopteryx splendens. The authors say these exceed the values of all other insects except the locust, so they are the TOP of the insect range, not typical. They are corrugated cuticular wings, not plates, and Re 700-2400 lies partly below the 1e3 floor of this entry. The interval is the spread between two species, not an error bar. Read level: search-summary. |
| `C_L_dragonfly_free_glide_observed` | 0.93 dimensionless | This is the highest CL recorded in free glides, which is an OPERATING lift coefficient. It is not a maximum, and the authors say it may not be the wing's true maximum. Do not use it as C_Lmax. Read level: search-summary. |
| `C_Lmax_post_stall_peak_flat_plate_Re2e4_5e4` | 1.19 dimensionless | OUTSIDE this entry's Re band. It is recorded here because it defines a failure mode (see where_it_breaks). Su et al. measured a rectangular plate (AR 6, chord 76 mm, thickness 8 mm, which my arithmetic puts at t/c = 10.5%, so not thin) at Re 2e4-5e4. They fitted CL(alpha) = -0.44 exp(-0.47 alpha) + 1.19 sin(1.74 alpha + 20 deg), and their text puts the lift peak "at approximately alpha = 40 deg". The maximum of that fit, 1.19 at alpha = 40.2 deg, is my calculation from their equation, not a number they state. Read level: full-text. |

## Why it holds

At Re 1e3-1e4 the boundary layer on a wing is laminar, and it separates at the leading edge at almost any useful incidence. Lift is then set less by attached-flow circulation than by the separated shear layer: how quickly it rolls up into a leading-edge vortex and whether it reattaches. Sunada et al. (1997, abstract as relayed) state that section characteristics at Re 4e3 "are strongly affected by leading edge vortices". This is why thin, sharp-edged, cambered plates do as well as or better than thick rounded sections here, and why the abstract reports that planform matters little at this Re. My inference: because the separated flow is fixed mainly by edge geometry and camber, C_Lmax depends weakly on Re inside the band and strongly on section shape. The measured values follow that pattern, but no source I read states it as a law.

## Where it holds

- **reynolds min**: 1.0e3
- **reynolds max**: 1.0e4
- **motion**: steady translation, fixed incidence, no rotation or flapping
- **geometry**: thin (t/c of a few percent), sharp leading edge; flat, cambered or corrugated, stated per value
- **taxa**: ['odonate wings (isolated)', 'model plates and sections']
- **notes**: Each constant applies to its own geometry. The band has no single C_Lmax: measured or relayed values run from about 0.4-0.5 (flat plate, inferred) through 1.06 (cambered plate) to 1.07-1.15 (the best dragonfly wings).


:::{danger} Where it breaks
Fails when carried across geometry or across wing motion at the same Re, because a steady C_Lmax for one section shape says nothing about another shape or about a revolving or flapping wing. (1) REVOLVING OR FLAPPING WINGS. A wing revolving like a propeller keeps a stable leading-edge vortex, and Usherwood & Ellington (2002b, abstract) report "high force coefficients" for revolving model and real wings across Re 1,100-26,000. The steady translational C_Lmax here therefore UNDER-states what a flapping or revolving wing achieves at the same Re. The reverse also fails: a revolving-wing coefficient must not be used as a gliding ceiling. I did not retrieve the revolving-wing numbers themselves (`unknown`), so the size of the gap is not stated here. (2) ACROSS GEOMETRY AT FIXED Re. At Re 4e3 a cambered plate beats a flat plate by a relayed 100-150%. A C_Lmax quoted without its section shape is not a constraint. Corrugated dragonfly sections (Kesel 2000, abstract: Re 7,880 and 10,000) reach "much higher lift values than flat plates"; no number was retrieved. (3) DEFINITION OF "MAXIMUM". On flat plates at Re 2e4-5e4 (just above this band), the measured lift peak sits near alpha = 40 deg in a post-stall, bluff-body regime (Su et al.), where L/D is poor. A C_Lmax taken from that peak is useless as a glide operating point. Whether a thin plate at Re 1e3-1e4 shows a separate low-incidence stall peak below the 40-deg one is `unknown` from what I read. The only incidence I have inside the band is alpha = 8 deg for Sunada's cambered plate. Always quote C_Lmax with the alpha at which it occurs. (4) THICK SECTIONS AND THE UPPER Re EDGE. Laitone (1997, search-summary) found thin and 5%-cambered plates "relatively insensitive" to Re and turbulence down to Re ~2e4. The NACA 0012 was "very seriously affected" below Re 5e4. A thick-aerofoil value from that regime is not a thin-plate value and must not be carried into this band, or the reverse. (5) COMPLIANT OR NON-INSECT MEMBRANES. Every in-band value comes from rigid model sections or stiff odonate wings. For a compliant membrane, such as a teleost fin in air, I found no measured polar. That search was not targeted (the scope is noted under worked_examples), so the absence is weak evidence. Transferring 1.07-1.15 to such a structure is an inference. (6) BELOW Re 1e3. Toward Re ~1e2 (Drosophila-scale), viscous effects grow. I did not retrieve values for that regime in this session, and the band must not be extrapolated downward.
:::

## Worked examples

**Danio rerio-sized glider in air (hypothetical design check)**

```
Inputs are taken from this repository's challenge-23 record: m = 0.4 g, W = 3.924e-3 N, rho = 1.2 kg/m^3, S = 3.2e-4 m^2 (span 0.04 m, AR 5, mean chord 8 mm), nu = 1.5e-5 m^2/s. Steady stall speed V = sqrt(2 W / (rho S C_Lmax)). Results: C_Lmax 0.47 -> 6.59 m/s (Re 3,517); 0.8 -> 5.05 m/s (Re 2,696); 1.06 -> 4.39 m/s (Re 2,342); 1.15 -> 4.22 m/s (Re 2,248).

```

- value: `[4.22, 6.59]`

- All four design points land inside the band, so the band is the right one to consult. The choice of section moves the stall speed by a factor of about 1.56, which is my calculation, ratio 6.59/4.22. That spread comes from geometry, not from Re. These are calculated stall speeds, not observations of any animal. Search scope behind the "no fin-membrane polar" statement: this session's web searches targeted plates, aerofoils and odonate wings only; challenge-23 (same repository) reports a separate, also negative, search. Neither was a systematic search for membrane data.

- evidence: **derived**

**Sympetrum sanguineum and Calopteryx splendens (isolated wings)**

- value range: `[1.07, 1.15]`

- Measured steady C_Lmax at Re 700-2400; see constants. The glide-observed 0.93 is an operating value.

- evidence: **literature**

:::{seealso} Contested
- The size of the band itself. A claim recorded elsewhere in this repository puts the steady C_Lmax of thin wings at Re 7e2-1e4 at "0.9-1.15". Challenge-23 in the same repository argues that this takes the two best species, counts the 0.93 glide value as a maximum, and ignores relayed values of "about 0.7-0.9" for other dragonfly species and "about 0.8" for a thin aerofoil at Re 1e4. I have not re-read the sources for the 0.7-0.9 or 0.8 values (they are cited there as Wakeling & Ellington 1997 and Sci. Rep. 6:25706, 2016), so both readings are kept unreconciled.

- The Re of Usherwood (2009, Exp. Fluids 46:991-1003; revolving pigeon wing and flat-plate replica). Su et al. state that it was measured "at Reynolds number up to 10,800", which would put it inside this band. A review commit in this repository (challenge 65) states the range resolves to 49k-108k, which would put it outside. I could not access Usherwood 2009 to settle this, and its numbers are not used in this entry.

:::

## Sources

| Citation | Read-level |
|---|---|
| Sunada S, Sakaguchi A, Kawachi K (1997) Airfoil section characteristics at a low Reynolds number. J. Fluids Eng. 119(1):129-135 | `search-summary` |
| Srinath DN, Mittal S (2010) Optimal aerodynamic design of airfoils in unsteady viscous flows. Comput. Methods Appl. Mech. Eng. 199:1976-1991 | `search-summary` |
| Wakeling JM, Ellington CP (1997) Dragonfly flight I. Gliding flight and steady-state aerodynamic forces. J. Exp. Biol. 200:543-556 | `search-summary` |
| Okamoto M, Yasuda K, Azuma A (1996) Aerodynamic characteristics of the wings and body of a dragonfly. J. Exp. Biol. 199:281-294 | `abstract` |
| Kesel AB (2000) Aerodynamic characteristics of dragonfly wing sections compared with technical aerofoils. J. Exp. Biol. 203:3125-3135 | `abstract` |
| Usherwood JR, Ellington CP (2002b) The aerodynamics of revolving wings II. Propeller force coefficients from mayfly to quail. J. Exp. Biol. 205:1565-1576 | `abstract` |
| Laitone EV (1997) Wind tunnel tests of wings at Reynolds numbers below 70 000. Exp. Fluids 23:405-409 | `search-summary` |
| Su Y, Fan X, Onoue K, Vejdani H, Breuer KS (2025) An improved aerodynamic model for quasi-steady simulations of animal flight at moderate Reynolds numbers. arXiv:2302.09602v2 | `full-text` |
| Usherwood JR (2009) The aerodynamic forces and pressure distribution of a revolving pigeon wing. Exp. Fluids 46:991-1003 | `could-not-access` |


---

*Generated from [`library/laws/lift-coefficient-lowre.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/lift-coefficient-lowre.yaml). Do not edit this page; edit the YAML.*
