---
title: Phyllotaxis and the golden divergence angle: what is explained and what is not
label: law-phyllotaxis
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-phyllotaxis
\begin{aligned} &\theta_n = n\,\alpha,\qquad \alpha = \frac{2\pi}{\varphi^{2}} = 2\pi\left(1-\frac{1}{\varphi}\right) \approx 137.508^\circ,\qquad \varphi = \frac{1+\sqrt5}{2} \\ &\text{Vogel (1979) capitulum construction:}\quad r_n = c\,\sqrt{n},\qquad \theta_n = n\,\alpha \end{aligned}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `theta_n` | 1 | rad | azimuthal position of the n-th organ (leaf, floret, scale) counted in order of initiation |
| `n` | 1 | dimensionless | ordinal index of the organ in the initiation sequence |
| `phi` | 1 | dimensionless | golden ratio (1 + sqrt 5)/2 = 1.6180... |
| `alpha` | 1 | rad | divergence angle between successively initiated organs; the golden angle when alpha = 2*pi/phi^2 |
| `r_n` | L | m | radial distance of the n-th floret from the centre in Vogel's planar capitulum model |
| `c` | L | m | Vogel scale constant; each floret occupies area pi*c^2 in the model |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `golden_angle` | 137.508 deg | MATHEMATICAL constant, 360*(1 - 1/phi) = 137.50776 deg (our arithmetic). It has no measurement interval. The observed spread of divergence angles around it is NOT recorded here because no source read in this session gave a wild-type mean and standard deviation (see next entry). |
| `divergence_angle_arabidopsis_wt_spread` | unknown deg | unknown. Tried: Landrein et al. 2015 (PMC full text, summarising fetch) and Refahi et al. 2016 (eLife, first ~40% of the text). Neither yielded a wild-type mean +/- SD in the portions read; Refahi et al. state only that the angle is "mainly close to (~137 deg) with possible exceptions". Besnard et al. 2014 may contain it; only its abstract-level summary was seen. |
| `organ_permutation_fraction_arabidopsis_col0` | unknown (interval 0.021 to 0.14) fraction of organs | OBSERVATION, Landrein et al. 2015, Table 1 as quoted by a summarising fetch: Col-0 grown in long days only, 2.1% of organs permuted (1193 angles, 34 sequences); grown short then long days, 14% of siliques permuted (704 angles, 29 sequences), with 23% of angles non-canonical. The two numbers are different growth conditions, not an uncertainty; they are recorded side by side. The fetch also noted a mismatch in the paper between Table 1 (704 angles, 29 sequences) and Fig 2E (703 angles, 23 plants); not resolved here. |
| `sunflower_fibonacci_parastichy_fraction` | 0.736 (interval 0.736 to 0.823) fraction of parastichy numbers | OBSERVATION by Swinton, Ochu et al. 2016 (657 sunflowers; most reliable subset 768 parastichy numbers): 565 Fibonacci, a further 67 with predefined Fibonacci structure (25 double-Fibonacci, 41 Lucas, 1 F4), 136 non-Fibonacci (49 F-1, 17 F+1, 70 other). The fractions 565/768 = 0.736 and (565+67)/768 = 0.823 are OUR arithmetic on the authors' counts. Parastichy numbers are counts of spirals, not measured divergence angles. |
| `fibonacci_fraction_cross_species_survey` | more than 91% (over 96% counting double-Fibonacci) fraction of observations | Seen only as a search summary of the accepted manuscript of Turner et al. 2023, which reports it for about 12,000 observations from 650 angiosperm and gymnosperm species. The ORIGINAL survey this figure comes from was not identified or read (it is commonly attributed to R. V. Jean, but that attribution is NOT verified in this session). Treat as secondary. |

## Why it holds

What IS explained (a mechanism with physical and molecular support): organs are initiated one at a time at the periphery of the shoot apical meristem, and each new primordium appears in the largest gap left by its predecessors because existing primordia inhibit initiation nearby (Hofmeister's rule, as restated by the modelling literature). Douady & Couder (1992, 1996) reproduced this with a PHYSICAL experiment -- ferrofluid drops released periodically at the centre of a dish, mutually repelling and advected outward by a magnetic field gradient -- and showed in experiment and simulation that the pattern is set by one dimensionless parameter G (equivalent to Richards' plastochron ratio, the ratio of radial displacement per initiation period to meristem radius). In their account, as G decreases the parastichy numbers climb the Fibonacci sequence and the divergence angle tends to the golden angle (or its complement); at large G the system goes distichous (180 deg). That the golden angle is an ATTRACTOR of sequential, inhibition-limited placement under slowly decreasing G -- not a target encoded anywhere -- is the authors' claim, supported by their simulations. The molecular implementation proposed for the inhibitor is auxin depletion: existing primordia act as auxin sinks via PIN1-mediated polar transport, so auxin maxima (and new primordia) arise only at a minimum distance from them (Reinhardt et al. 2003, experimental). Smith et al. (2006) report a computer simulation of that transport model that reproduces, within standard error, divergence angles measured in Arabidopsis seedlings, and also distichous, decussate and tricussate patterns (a SIMULATED match to observed angles). Besnard et al. (2014) add a second, cytokinin-signalling inhibitory field (AHP6) that imposes a temporal order on initiation and, in their account, makes the angle sequence robust.
What is NOT explained, in the sources read: (a) why spiral systems sit on the Fibonacci branch so much more often than on the Lucas or other branches, which the same dynamics also admit -- the dynamical account makes the Fibonacci branch reachable from simple initial conditions, but the 17.7% non-Fibonacci sunflower parastichy numbers (our arithmetic on Swinton et al. 2016) are not predicted in frequency by any source read; (b) the ADAPTIVE value, if any, of the golden angle (contested; see contested_by); (c) the source of organ-to-organ noise -- Refahi et al. (2016) identify noise on the plastochron as a common feature and propose stochastic perception of inhibitory fields as its most likely origin (their model inference, other sources not ruled out by them); (d) why roughly half of the reconstructed early-Devonian Asteroxylon plants had whorls and the rest non-Fibonacci n:(n+1) spirals (Turner et al. 2023).

## Where it holds

- **pattern class**: spiral (alternate, one organ per node) phyllotaxis only
- **regime**: small expansion parameter G / plastochron ratio, after the system has relaxed onto the Fibonacci branch (Douady & Couder model claim)
- **quantity**: a population or sequence statistic of divergence angles at the apex; not a per-organ guarantee and not necessarily the angle seen on the mature stem
- **demonstrated in**: ['Arabidopsis thaliana inflorescence (with measured permutations)', 'Helianthus annuus capitulum (parastichy counts)', 'ferrofluid analogue (Douady & Couder 1992)']
- **notes**: Our inference from the sources: the golden angle is the expected divergence wherever organs are placed one at a time by a lateral-inhibition rule into a slowly shrinking relative gap. Outside that construction -- organs initiated in pairs or whorls, or with large G -- the rule gives a different angle (90, 180, 360/k deg) and the golden angle is not the right prediction.


:::{danger} Where it breaks
(1) NON-SPIRAL PHYLLOTAXIS -- the law simply does not apply. Distichous arrangements have a 180 deg divergence; decussate (opposite pairs at 90 deg) and whorled/tricussate arrangements place several organs per node. Smith et al. (2006) state their auxin model reproduces distichous, decussate and tricussate patterns, confirming these are real regimes of the SAME mechanism, not exceptions to be explained away. Taxon examples (our general botanical knowledge, NOT verified against a source in this session): distichous leaves in grasses (Poaceae), decussate leaves in the mint family (Lamiaceae). A checker that expects 137.5 deg from these would be wrong by 40-50 deg or more. (2) INDIVIDUAL ORGANS, EVEN IN SPIRAL SYSTEMS. In Arabidopsis, a model spiral system, successive divergence angles of ~274 deg and ~220 deg (signature of two organs initiated in swapped order) are common (Besnard et al. 2014, search-summary); Landrein et al. (2015, observed) report permuted organs at 2.1% (long days) to 14% (short then long days) of the sequence in Col-0, and that larger meristems correlate with more permutations. The ahp6 cytokinin-signalling mutant amplifies permutations (Besnard et al. 2014). So the golden angle holds for the spatial positions of initiation sites (Refahi et al. 2016 call these "highly robust"), but the angle between consecutive organs on the stem is noisy, and the noise depends on genotype, day length and meristem size. (3) THE ANGLE ON THE MATURE STEM IS NOT THE APICAL ANGLE. Okabe (2015) argues the divergence measured on developed stems differs from that at the shoot tip because of stem twisting (author's model claim, read at search-summary level). Measuring a mature plant and comparing it to 137.5 deg conflates the two. (4) NON-FIBONACCI SPIRALS ARE MEASURABLY COMMON IN SOME SYSTEMS. Swinton et al. (2016, observed, 768 parastichy numbers from photo-reviewed sunflowers): 136 non-Fibonacci (17.7%, our arithmetic), with F-1 counts (49) significantly more frequent than F+1 (17), plus 41 Lucas numbers and "quasi-regular" heads with no definite parastichy number. Lucas parastichies correspond in the standard theory to a divergence near 99.5 deg (360/(3 + 1/phi) = 99.50 deg, our CALCULATION; Swinton et al. measured counts, not angles). In early lycophytes (Asteroxylon mackiei, Rhynie chert, Early Devonian) Turner et al. (2023) report whorls and spirals, with ALL spirals of non-Fibonacci n:(n+1) type -- on a sample reported in press coverage as four reconstructed plants. The golden-angle/Fibonacci association is therefore not ancestral to all leafy plants, per the authors' claim. (5) LARGE G / TRANSITIONS. In the Douady-Couder dynamics the golden angle is the small-G limit; at large G the pattern converges to distichy, and during changes of G (e.g. vegetative-to-floral transition, where G is reported to decrease) the angle passes through other values. The law is a limit, not a constant, and does not describe a meristem in transition. (6) FIBONACCI PARASTICHIES DO NOT CERTIFY A GOLDEN ANGLE. Our inference (standard phyllotaxis geometry, not checked against a primary source in this session): a given visible parastichy pair is consistent with a band of divergence angles around 137.5 deg, so a spiral count from a photograph cannot be used as a measurement of alpha to better than that band. (7) FUNCTIONAL-OPTIMALITY CLAIMS BREAK. The statement "plants use 137.5 deg because it maximises light capture" is not supported as a uniqueness claim: Strauss et al. (2020, simulated) report other Fibonacci-like-series angles found in nature are equally optimal for light capture, and Valladares & Brites (2004, as summarised by a search) report indistinguishable light-interception efficiencies across divergence angles. Do not derive a performance requirement from the golden angle.
:::

## Worked examples

**any spiral system (pure arithmetic)**

```
alpha = 360 deg / phi^2 = 360 * (1 - 1/1.6180340) = 137.508 deg; Lucas-branch angle 360/(3 + 1/phi) = 99.502 deg
```

- value: `137.508`

- CALCULATED. The two angles are the limits of the main (Fibonacci) and Lucas branches; neither is a measurement.

- evidence: **derived**

**Vogel capitulum (hypothetical sizing, NOT a measured sunflower)**

```
c = 1 mm, N = 1000 florets -> outer radius r_N = c*sqrt(N) = 1 mm * 31.6 = 31.6 mm; each floret area pi*c^2 = 3.14 mm^2
```

- value: `31.6`

- CALCULATED from Vogel's model with an arbitrary c chosen by us. Shows the only constraining use of the law: as a geometric construction for packing N equal-area points in a disc. It is a design rule for engineered layouts, not a prediction about any plant.

- evidence: **derived**

**Helianthus annuus (citizen-science sample, UK and elsewhere)**

```
565 / 768 = 0.736 Fibonacci; (565 + 67) / 768 = 0.823 Fibonacci-structured; 136 / 768 = 0.177 non-Fibonacci
```

- value range: `[0.736, 0.823]`

- OBSERVED counts (Swinton et al. 2016); the fractions are our arithmetic on them.

- evidence: **literature**

**Arabidopsis thaliana Col-0 inflorescence**

- value range: `[0.021, 0.14]`

- OBSERVED (Landrein et al. 2015): long days only vs short-then-long days. A divergence-angle sequence from a real Arabidopsis stem should be expected to contain ~274/220 deg pairs at this rate; a design or analysis that treats every consecutive angle as 137.5 deg is wrong at this rate.

- evidence: **literature**

:::{seealso} Contested
- Adaptive value of the golden angle. King, Beck & Lüttge (2004, as summarised by later papers and a blog; original not read) propose it was selected for minimal self-shading / optimal light capture. Strauss et al. (2020, simulation) report other naturally occurring Fibonacci-like angles are equally optimal for light capture; Valladares & Brites (2004, search-summary) report indistinguishable light-interception efficiencies across angles. Okabe (2015) proposes instead that the golden angle minimises the energy cost of the transition from apical to stem arrangement (stem twisting). Three incompatible adaptive accounts and a no-selection-needed dynamical account (Douady & Couder) are recorded; this entry does not reconcile them.
- Identity and sufficiency of the inhibitory field. Reinhardt et al. (2003) and Smith et al. (2006) present auxin depletion by PIN1-mediated transport as the inhibitor and report the simulation reproduces measured Arabidopsis angles. Besnard et al. (2014) argue auxin-depletion zones alone are not sufficient for the observed robustness and add an AHP6/cytokinin field. Refahi et al. (2016) attribute residual disorder to plastochron noise from stochastic field perception (model inference). Recorded as unresolved.
- Universality of Fibonacci phyllotaxis. A cross-species survey (>91% Fibonacci across ~650 species, seen only as quoted by Turner et al. 2023) versus Turner et al.'s report that all spirals in Asteroxylon mackiei were non-Fibonacci, and Swinton et al.'s 17.7% non-Fibonacci sunflower parastichy numbers. Earlier sunflower counts quoted by Swinton et al.: Schoute 82% and Weisse 95% main-sequence Fibonacci, neither reporting non-Fibonacci structure. The disagreement in rates is preserved, not averaged.
:::

## Sources

| Citation | Read-level |
|---|---|
| Vogel H (1979) A better way to construct the sunflower head. Mathematical Biosciences 44(3-4):179-189. doi:10.1016/0025-5564(79)90080-4 | `search-summary` |
| Douady S, Couder Y (1992) Phyllotaxis as a physical self-organized growth process. Phys Rev Lett 68:2098-2101 | `search-summary` |
| Douady S, Couder Y (1996) Phyllotaxis as a dynamical self organizing process, Parts I-III. J Theor Biol 178 (pages not verified in this session) | `could-not-access` |
| Reinhardt D, Pesce ER, Stieger P, Mandel T, Baltensperger K, Bennett M, Traas J, Friml J, Kuhlemeier C (2003) Regulation of phyllotaxis by polar auxin transport. Nature 426:255-260. doi:10.1038/nature02081 | `search-summary` |
| Smith RS, Guyomarc'h S, Mandel T, Reinhardt D, Kuhlemeier C, Prusinkiewicz P (2006) A plausible model of phyllotaxis. PNAS 103(5):1301-1306. doi:10.1073/pnas.0510457103 | `search-summary` |
| Besnard F et al. (2014) Cytokinin signalling inhibitory fields provide robustness to phyllotaxis. Nature 505(7483):417-421. doi:10.1038/nature12791 | `search-summary` |
| Landrein B, Refahi Y, Besnard F, Hervieux N, Mirabet V, Boudaoud A, Vernoux T, Hamant O (2015) Meristem size contributes to the robustness of phyllotaxis in Arabidopsis. J Exp Bot 66(5):1317-1324. doi:10.1093/jxb/eru482 | `full-text` |
| Refahi Y, Brunoud G, Farcot E, Jean-Marie A, Pulkkinen M, Vernoux T, Godin C (2016) A stochastic multicellular model identifies biological watermarks from disorders in self-organized patterns of phyllotaxis. eLife 5:e14093. doi:10.7554/eLife.14093 | `full-text` |
| Swinton J, Ochu E, MSI Turing's Sunflower Consortium (2016) Novel Fibonacci and non-Fibonacci structure in the sunflower: results of a citizen science experiment. R Soc Open Sci 3(5):160091. doi:10.1098/rsos.160091 | `full-text` |
| Turner HA, Humpage M, Kerp H, Hetherington AJ (2023) Leaves and sporangia developed in rare non-Fibonacci spirals in early leafy plants. Science 380:1188-1192 | `search-summary` |
| Strauss S, Lempe J, Prusinkiewicz P, Tsiantis M, Smith RS (2020) Phyllotaxis: is the golden angle optimal for light capture? New Phytologist 225(1):499-510. doi:10.1111/nph.16040 | `search-summary` |
| Okabe T (2015) Biophysical optimality of the golden angle in phyllotaxis. Sci Rep 5:15358. doi:10.1038/srep15358 | `search-summary` |
| King S, Beck F, Lüttge U (2004) On the mystery of the golden angle in phyllotaxis. Plant Cell Environ (volume and pages NOT verified in this session) | `search-summary` |
| Valladares F, Brites D (2004) Plant Ecology (title, volume and pages unknown -- not retrieved) | `search-summary` |


---

*Generated from [`library/laws/phyllotaxis.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/phyllotaxis.yaml). Do not edit this page; edit the YAML.*
