---
title: Strouhal number and the 0.2-0.4 cruising band of flapping and swimming animals
label: law-strouhal
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-strouhal
\mathrm{St} = \frac{f A}{U}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `St` | 1 | dimensionless | Strouhal number of the propulsor (wake width x frequency / speed) |
| `f` | 1/T | Hz | flapping, tail-beat or fluke-beat frequency |
| `A` | L | m | PEAK-TO-PEAK amplitude of the trailing edge (tail tip, fluke or wingtip), taken as a proxy for wake width |
| `U` | L/T | m/s | mean forward (cruising) speed |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `St_cruise_band_animals` | unknown (interval 0.2 to 0.4) dimensionless | The band Taylor, Nudds & Thomas (2003) report for cruising birds, bats, insects, fish and cetaceans. It is a band, not a point estimate, so no central value is given here; any midpoint would be ours, not theirs. Read only at search-summary level (paywalled). |
| `St_foil_optimum` | unknown (interval 0.25 to 0.35) dimensionless | Frequency of maximum wake amplification / peak efficiency for oscillating foils (Triantafyllou, Triantafyllou & Grosenbaugh 1993). This is a foil-experiment and stability-analysis result, not an animal observation. Read at search-summary level. |
| `St_odontocete_mode` | 0.25 (interval 0.2 to 0.3) dimensionless | Observation, Rohr & Fish (2004), 248 Strouhal numbers from six captive odontocete species. Per the abstract as summarised: 74% of values fell in 0.20-0.30 (the interval), and the densest 0.05 bin was 0.225-0.275 holding 44% of values. The value 0.25 is OUR arithmetic (the centre of that bin), not a number the authors report as a mean or median. |
| `St_birds_cruise_fitted` | 0.21 (direct fliers); 0.25 (intermittent fliers) dimensionless | Fitted values from Nudds, Taylor & Thomas (2004), 60 bird species. These are parameters of a fitted wingbeat-frequency model, not a direct per-species distribution. No interval was available at search-summary level; recorded as unknown. |
| `St_larval_zebrafish` | unknown (interval 0.72 to 2.5) dimensionless | Observation, van Leeuwen, Voesenek & Mueller (2015), larval Danio rerio over Re 60-1400; St falls from 2.5 at the lowest Re to 0.72 at the highest. Every measured value is ABOVE the 0.2-0.4 band. |
| `St_optimum_elongated_body_model` | unknown (interval 0.15 to 0.8) dimensionless | CALCULATED, not observed: Eloy (2012) uses Lighthill elongated-body theory and finds the optimal St rises from about 0.15 (largest cetaceans) to about 0.8 (smallest tadpoles). Eloy reports that kinematics of 53 species compiled from the literature lie near this predicted optimum. |

## Why it holds

St compares the width of the wake a flapping propulsor leaves (approximated by the peak-to-peak trailing-edge amplitude A) with the spacing between successive shed vortices (U/f). Triantafyllou et al. (1993) claim that the jet behind an oscillating foil is convectively unstable over a narrow frequency band, and that thrust and efficiency peak when the flapping frequency matches that band, which they place at St 0.25-0.35. Taylor et al. (2003) claim that because propulsive efficiency peaks in a narrow St range, natural selection should push cruising animals into roughly 0.2-0.4, and report that it has. The link from efficiency peak to selection is the authors' argument; the clustering of measured St is the observation. The two are separable and should not be cited as one finding.

## Where it holds

- **regime**: steady cruising (constant mean speed) with a flapping or undulating propulsor
- **reynolds min**: unknown
- **swimming number min**: 1.0e4
- **taxa**: ['cruising birds', 'bats', 'cruising fish', 'odontocete cetaceans', 'some cruising insects (thin data)']
- **notes**: The band is a high-Reynolds-number, cruise-only result. Gazzola, Argentina & Mahadevan (2014) report (search-summary level) that St is independent of Re only for swimming number Sw > 1e4, and depends weakly on Re (St ~ Re^-1/4) below it. Their Sw uses the HALF amplitude (Sw = omega*A*L/nu), so a threshold in Sw is not a threshold in Re and the two amplitude conventions differ by a factor of 2. We did not find a source giving a Reynolds-number lower bound in Re itself; recorded as unknown (scope: the web searches listed under sources, Nov 2026).


:::{danger} Where it breaks
(1) LOW REYNOLDS NUMBER -- demonstrated, not inferred. Larval zebrafish at Re 60-1400 swim at St 0.72-2.5 (van Leeuwen et al. 2015, observation); no measured value reaches the band. The authors attribute this to viscous forces and state that low propulsive efficiency is an unavoidable physical constraint for small undulatory swimmers. Gazzola et al. (2014) report the Re-dependence of St below Sw ~ 1e4. A design operating at Re ~ 1e3 (e.g. a centimetre-scale fin or wing at a few m/s) must NOT be checked against 0.2-0.4; the band would mark a sound low-Re design as wrong. (2) HOVERING AND SLOW FLIGHT -- St is undefined. As U -> 0 at finite f*A, St -> infinity, so hovering insects, hummingbirds and slow-flying animals fall outside the band by construction, not by inefficiency. The band applies only at cruise. (3) NON-STEADY LOCOMOTION -- fast starts, take-off, burst-and-coast, launching and acceleration are outside the cruise condition the band was measured in. Our inference: no St band should be applied to a launch or escape manoeuvre; we found no source reporting a band for these (scope: searches listed). (4) BODY-FORM DEPENDENCE -- the optimum is not one fixed band. Eloy (2012, calculated) predicts the optimum moving from ~0.15 for large cetaceans to ~0.8 for small tadpoles; odontocetes cluster about 20% below the foil-predicted optimum (Rohr & Fish 2004, observation). (5) AMPLITUDE CONVENTION -- the 0.2-0.4 band uses PEAK-TO-PEAK amplitude. Using half amplitude (as in the swimming number Sw) halves St and silently moves a design out of band. Check the convention of every source before comparing. (6) IN-BAND IS NOT SUFFICIENT. Our inference, not a cited result: St is one kinematic parameter; foil efficiency also depends on pitch amplitude and heave-pitch phase, so an in-band St does not certify an efficient propulsor. The band can reject a cruise design; it cannot approve one.
:::

## Worked examples

**Odontocete cetaceans (six captive species) in steady swimming**

- value range: `[0.2, 0.3]`

- 74% of 248 measured values; densest bin 0.225-0.275 (Rohr & Fish 2004, abstract as summarised).

- evidence: **literature**

**Cruising birds (60 species)**

- value: `0.21 (direct fliers); 0.25 (intermittent fliers)`

- Fitted model parameters at the low end of 0.2-0.4 (Nudds et al. 2004).

- evidence: **literature**

**Larval Danio rerio, Re 60-1400**

- value range: `[0.72, 2.5]`

- Observed. Entirely above the cruising band -- the counterexample that sets the low-Re failure boundary, and the relevant one for any zebrafish-scale design in this project.

- evidence: **literature**

**Danio rerio candidate wing in air (same case as reynolds.yaml)**

```
U = 2 m/s, A = 0.01 m peak-to-peak (assumed), target St = 0.3  ->  f = St*U/A = 0.3*2/0.01 = 60 Hz
```

- value: `60`

- DERIVED, not observed; A is an assumed value, not a measurement. The point of the example is the warning: this case sits at Re ~ 1333 (reynolds.yaml), inside the regime where larval zebrafish are observed far above the band, so 60 Hz is the frequency the high-Re band would imply, not a frequency the band supports at this scale. Treat it as a descriptive comparison only.

- evidence: **derived**

:::{seealso} Contested
- Eloy (2012), calculated: the optimal St is not a universal band but rises with the Lighthill number from ~0.15 to ~0.8 across body forms. This is a model prediction; Eloy reports 53 species lie near it.
- Rohr & Fish (2004), observation: odontocetes cluster at 0.20-0.30, about 20% below the 0.25-0.35 foil optimum of Triantafyllou et al. (1993).
- van Leeuwen et al. (2015): the abstract gives large swimmers as 0.2-0.6, while the discussion of the same paper cites 0.2-0.4 for adult fish and cetaceans. The paper is internally inconsistent on the band; both figures are recorded, neither is preferred.
- Gazzola et al. (2014): St is Re-independent only above Sw ~ 1e4 and scales as Re^-1/4 below it, so the band is a high-Re asymptote rather than a property of flapping locomotion in general.
- arXiv:1904.13013 (Landmarks and Frontiers in Biological Fluid Dynamics; authors not recorded here): argues the kinematic St links linearly to vortex formation whereas appendage vortex formation is strongly nonlinear, and questions whether St is the right organising variable. Read at search-summary level only.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taylor GK, Nudds RL, Thomas ALR (2003) Flying and swimming animals cruise at a Strouhal number tuned for high power efficiency. Nature 425:707-711. doi:10.1038/nature02000 | `search-summary` |
| Triantafyllou GS, Triantafyllou MS, Grosenbaugh MA (1993) Optimal thrust development in oscillating foils with application to fish propulsion. J Fluids Struct 7(2):205-224. doi:10.1006/jfls.1993.1012 | `search-summary` |
| Triantafyllou MS, Triantafyllou GS, Gopalkrishnan R (1991) Wake mechanics for thrust generation in oscillating foils. Phys Fluids A (volume and pages not verified in this session) | `listing` |
| Rohr JJ, Fish FE (2004) Strouhal numbers and optimization of swimming by odontocete cetaceans. J Exp Biol 207:1633-1642. doi:10.1242/jeb.00948 | `search-summary` |
| Nudds RL, Taylor GK, Thomas ALR (2004) Tuning of Strouhal number for high propulsive efficiency accurately predicts how wingbeat frequency and stroke amplitude relate and scale with size and flight speed in birds. Proc R Soc B 271:2071-2076. doi:10.1098/rspb.2004.2838 | `search-summary` |
| Eloy C (2012) Optimal Strouhal number for swimming animals. J Fluids Struct 30:205-218. doi:10.1016/j.jfluidstructs.2012.02.008; arXiv:1102.0223 | `abstract` |
| van Leeuwen JL, Voesenek CJ, Mueller UK (2015) How body torque and Strouhal number change with swimming speed and developmental stage in larval zebrafish. J R Soc Interface 12:20150479. doi:10.1098/rsif.2015.0479 | `full-text` |
| Gazzola M, Argentina M, Mahadevan L (2014) Scaling macroscopic aquatic locomotion. Nature Physics 10:758-761 | `search-summary` |
| Borazjani I, Sotiropoulos F (2008) Numerical investigation of the hydrodynamics of carangiform swimming [title truncated in the listing seen]. J Exp Biol 211:1541 (end page not verified) | `search-summary` |
| Landmarks and Frontiers in Biological Fluid Dynamics, arXiv:1904.13013 | `search-summary` |


---

*Generated from [`library/laws/strouhal.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/strouhal.yaml). Do not edit this page; edit the YAML.*
