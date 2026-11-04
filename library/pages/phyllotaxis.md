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
\theta_n = n\,\alpha,\qquad \alpha = \frac{2\pi}{\varphi^{2}} = 2\pi\left(1-\frac{1}{\varphi}\right) \approx 137.508^\circ,\qquad \varphi = \frac{1+\sqrt{5}}{2}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `theta_n` | 1 | rad | azimuthal position of the n-th organ (leaf, floret, scale, silique), counted in order of initiation |
| `n` | 1 | dimensionless | ordinal index of the organ in the initiation sequence |
| `phi` | 1 | dimensionless | golden ratio, (1 + sqrt 5)/2 = 1.6180340 |
| `alpha` | 1 | rad | divergence angle between successively initiated organs; equals the golden angle when alpha = 2*pi/phi^2 |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `golden_angle` | 137.508 deg | MATHEMATICAL constant, 360/phi^2 = 360*(1 - 1/phi) = 137.50776 deg (our arithmetic). It has no measurement interval. Its complement, 222.49 deg, describes the same spiral run in the other direction; which one a measurement reports depends on the chirality convention used. |
| `mean_divergence_angle_arabidopsis_col0` | 136 deg | OBSERVATION. Landrein et al. 2015, Table 1: mean angle 136 deg for Col-0 in BOTH growth regimes (short-then-long days, 704 angles from 29 sequences; long days only, 1193 angles from 34 sequences). The paper reports no SD or CI for this mean and does not say how it was computed (arithmetic vs circular mean, or how permuted pairs were treated), so no interval is given here -- `interval: null` means "not reported", not "zero". The same table gives means for other lines that are NOT a dispersion of this value and are listed separately below. |
| `mean_divergence_angle_arabidopsis_other_lines` | unknown deg | OBSERVATION, Landrein et al. 2015 Table 1 (via PMC4339594). Six genotype-by-condition means span 128 to 141 deg. These are different genotypes and day-length regimes, not an uncertainty band on one quantity; they are tabulated, not pooled. The 128 deg value (clasp-1, long days) coincides with the only Lucas sequences in the table (6 of 19 sequences); our inference is that the low mean reflects that branch switch, but the paper does not state the link in the portion read. |
| `permuted_organ_fraction_arabidopsis` | unknown fraction of organs | OBSERVATION, Landrein et al. 2015 Table 1. Non-canonical angles in the same table: Col-0 23% vs 5.7%, WS-4 60.5% vs 16%, clasp-1 14.8% vs 11.2% (short-then-long vs long days only). Landrein's own Col-0 counts disagree between Table 1 (704 angles, 29 sequences; 1193 angles long days), Fig. 2E (703 angles, 23 plants) and Fig. 5D (703 angles, 26 plants; 1190 angles, 34 plants). Preserved, not resolved. |
| `sunflower_parastichy_counts` | unknown count of parastichy numbers | OBSERVATION, Swinton, Ochu et al. 2016 Table 1 (photo-reviewed subset of data from 657 sunflowers). Our arithmetic: 565/768 = 0.736 strict Fibonacci; (565+25+41+1)/768 = 0.823 with Fibonacci-type structure; 136/768 = 0.177 non-Fibonacci. These are counts of visible spirals; the paper does not measure divergence angles (the words "divergence" and "angle" do not occur in it, per the fetch). Historical figures quoted by the same paper: Schoute 82% and Weisse 95% main-sequence Fibonacci. |

## Why it holds

WHAT IS EXPLAINED. Organs are initiated one at a time at the flank of the shoot apical meristem, and a new primordium forms only where it is far enough from the existing ones -- a lateral-inhibition rule. Douady & Couder (1992) built a physical analogue: ferrofluid drops released periodically onto a dish, repelling one another and drifting outward in a magnetic-field gradient. Their claim, which we have seen only through secondary summaries, is that one parameter describing the timing of successive drops relative to their outward drift selects the pattern, and that sequential inhibition-limited placement self-organises into Fibonacci spirals with a divergence near the golden angle. On this account the golden angle is an attractor of the iteration, not a value encoded anywhere. The molecular candidate for the inhibitor is auxin depletion: existing primordia drain auxin through PIN1-mediated polar transport, so a new auxin maximum, and a new primordium, can form only away from them (Reinhardt et al. 2003, experimental). Smith et al. (2006) report that a computer SIMULATION of this transport model recreates the divergence angles measured in Arabidopsis seedlings "within the standard error", and also generates distichous, decussate and tricussate arrangements. Besnard et al. (2014) add a second inhibitory field, made by the mobile cytokinin-signalling inhibitor AHP6 downstream of auxin, which they report imposes a temporal order on initiation and so contributes to robustness.
WHAT IS NOT EXPLAINED, in the sources read. (a) Why living spiral systems sit on the Fibonacci branch so much more often than on the Lucas or n:(n+1) branches that the same dynamics admit. The self-organisation account makes the Fibonacci branch reachable; no source read predicts the measured 17.7% non-Fibonacci rate in sunflower heads (our arithmetic on Swinton et al. 2016), or why all spirals in Asteroxylon mackiei were n:(n+1) (Turner et al. 2023). (b) How the mechanism is sustained. Smith et al. (2006) state that with transport alone they "were not able to obtain sustained spiral phyllotactic patterns" and that primordium placement precision is about 15 deg, so they call for an additional robustness mechanism; the published auxin model therefore does not by itself produce a stable 137.5 deg spiral. (c) The source of organ-to-organ noise: Refahi et al. (2016) point to stochastic perception of the inhibitory fields as the "most likely origin" -- a model inference, not a measurement of the noise source. (d) The ADAPTIVE value, if any, of the golden angle. Contested; see contested_by.

## Where it holds

- **pattern class**: spiral (alternate, one organ per node) phyllotaxis at the shoot apex
- **regime**: steady initiation after the system has settled on the Fibonacci branch; not during transitions
- **quantity**: a sequence or population mean of divergence angles between successively INITIATED organs. Not a per-organ value, and not the angle read off a mature stem.

- **demonstrated in**: ['Arabidopsis thaliana inflorescence: measured mean 136 deg in Col-0, with permutations (Landrein et al. 2015)', 'Arabidopsis seedlings: simulated angles match measured ones within SE (Smith et al. 2006)', 'ferrofluid analogue (Douady & Couder 1992; secondary summaries only)']
- **notes**: Our inference from the sources: the golden angle is the expected divergence wherever organs are placed singly by a lateral-inhibition rule into the largest available gap, after the pattern has relaxed onto the main branch. Outside that construction -- organs initiated in pairs or whorls, or a different branch -- the same mechanism gives a different angle, and 137.5 deg is the wrong prediction.


:::{danger} Where it breaks
(1) NON-SPIRAL PHYLLOTAXIS. The law does not apply. Distichous arrangements diverge by 180 deg; decussate arrangements place opposite pairs rotated by 90 deg; whorls place several organs per node. Smith et al. (2006) report that one auxin-transport model generates distichous, decussate and tricussate patterns, so these are other outputs of the same mechanism rather than anomalies. A check that expects 137.5 deg from them is off by 42.5 deg (distichous) or 47.5 deg (decussate) (our arithmetic). We have not compiled which taxa are non-spiral from a source in this session.
(2) INDIVIDUAL ANGLES IN A SPIRAL SYSTEM. In Arabidopsis, the model spiral system, consecutive angles are frequently far from 137.5 deg. Landrein et al. (2015, observed, Table 1) report non-canonical angles in 5.7% to 60.5% of angles and permuted organs in 2.1% to 43.3% of organs, depending on genotype (Col-0, WS-4, clasp-1) and day length; they report that larger meristems correlate with more permutations. A two-organ permutation turns the ideal sequence alpha, alpha, alpha into 2*alpha, -alpha, 2*alpha, i.e. 275.0 deg then 222.5 deg then 275.0 deg (our CALCULATION, not a measured value). The golden angle survives only as a MEAN (136 deg in Col-0) over sequences that contain these events.
(3) NOT EVERY SPIRAL IS ON THE FIBONACCI BRANCH. Lucas sequences (ideal limit 360/(2 + phi) = 99.50 deg, our calculation) occurred in 6 of 19 clasp-1 long-day sequences, whose mean angle was 128 deg (Landrein et al. 2015). In sunflower heads, 136 of 768 parastichy numbers (17.7%) were non-Fibonacci and 41 were Lucas (Swinton et al. 2016, observed counts). In the Early Devonian lycophyte Asteroxylon mackiei, Turner et al. (2023) report leaves in whorls and in spirals, and that every spiral was of the non-Fibonacci n:(n+1) type; per press coverage (not the paper), of four reconstructed plants two were spiral and two whorled. So the Fibonacci/golden-angle association is not universal among living spiral systems and, per the authors' claim, not ancestral to leafy plants.
(4) THE MATURE STEM IS NOT THE APEX. Okabe (2015) states that the angle at the shoot tip is the golden angle while leaves on a developed stem sit at rational fractions such as 3/8 of a turn (135.0 deg) or 5/13 (138.5 deg), and that the fraction can vary along one plant. Comparing an angle measured on a grown stem with 137.5 deg conflates two different quantities.
(5) A FIBONACCI SPIRAL COUNT DOES NOT MEASURE ALPHA. Counting parastichies in a photograph identifies the branch, not the angle; the Swinton et al. data contain no angle measurements. A parastichy count is not a substitute for an angle measurement in a design check (our inference; we did not verify the standard theorem relating a visible parastichy pair to a band of angles against a primary source).
(6) TRANSITIONS. In the Douady-Couder account the golden angle is the limit of one regime; when the control parameter changes (for example at the vegetative-to-floral transition) the angle passes through other values. The law describes a settled meristem, not one in transition.
(7) OPTIMALITY CLAIMS. "137.5 deg maximises light capture" fails as a uniqueness claim: Strauss et al. (2020, SIMULATED) report that other angles generated by Fibonacci-like series found in nature are equally optimal for light capture. Do not derive a performance requirement from the golden angle.
:::

## Worked examples

**any spiral system (pure arithmetic)**

```
alpha = 360/phi^2 = 360*(1 - 1/1.6180340) = 137.508 deg; complement 360 - 137.508 = 222.492 deg
```

- value: `137.508`

- CALCULATED. A mathematical limit, not a measurement.

- evidence: **derived**

**Lucas-branch spiral (pure arithmetic)**

```
alpha_Lucas = 360/(2 + phi) = 360/3.6180340 = 99.502 deg
```

- value: `99.502`

- CALCULATED limit angle of the Lucas branch. Swinton et al. counted Lucas parastichy numbers; they did not measure this angle.

- evidence: **derived**

**two-organ permutation signature (pure arithmetic)**

```
organs at 0, a, 2a, 3a initiated in order 0, 2a, a, 3a -> successive angles 2a = 275.02, -a mod 360 = 222.49, 2a = 275.02 deg
```

- value range: `[222.49, 275.02]`

- CALCULATED. This is the pattern an analysis should look for in a measured Arabidopsis angle sequence, instead of flagging these angles as measurement error.

- evidence: **derived**

**rational stem fractions vs the golden angle (pure arithmetic)**

```
3/8*360 = 135.000; 5/13*360 = 138.462; 8/21*360 = 137.143; 13/34*360 = 137.647 deg; golden 137.508
```

- value range: `[135.0, 138.462]`

- CALCULATED. Successive Fibonacci fractions bracket the golden angle and approach it, so a stem fraction of 3/8 is 2.5 deg below and 5/13 is 1.0 deg above. A stem reading within about 2.5 deg of 137.5 does not distinguish "golden angle at the apex" from "rational fraction on the stem".

- evidence: **derived**

**Arabidopsis thaliana Col-0 inflorescence**

- value: `136`

- OBSERVED mean angle, Landrein et al. 2015 Table 1, in both day-length regimes; no dispersion reported. The difference from the golden angle is 1.5 deg (our arithmetic). Because the paper reports no SD, we cannot say whether 1.5 deg is distinguishable from zero.

- evidence: **literature**

**Helianthus annuus capitulum (citizen-science sample)**

```
565/768 = 0.736 Fibonacci; (565 + 67)/768 = 0.823 Fibonacci-structured; 136/768 = 0.177 non-Fibonacci
```

- value range: `[0.736, 0.823]`

- OBSERVED counts (Swinton et al. 2016); the fractions are our arithmetic on them. Two definitions of "Fibonacci", not an uncertainty band.

- evidence: **literature**

:::{seealso} Contested
- Adaptive value of the golden angle. Okabe (2015, theoretical model) proposes that 137.5 deg minimises the energy cost of the transition between stem phyllotaxis fractions (stem twisting) and states the model also accounts for the "high precision" of the angle. Strauss et al. (2020, simulation) report that other Fibonacci-like angles found in nature are equally optimal for light capture, so light capture does not single out 137.5 deg. The Douady-Couder account needs no selection at all: the angle is an attractor of the initiation dynamics. These positions are recorded without reconciliation.
- Precision of the angle in real plants. A search summary attributes to Okabe (2015, Acta Soc Bot Pol 84:79-85) a claim that sunflower floret divergence stays within about 0.001 deg of 137.508 deg; we could not read that paper (host outside this session's network allowlist) and do NOT know whether the figure is measured or inferred. Against it, Landrein et al. (2015, observed) report Arabidopsis genotype-by-condition mean angles from 128 to 141 deg and permuted organs in up to 43.3% of organs, and Smith et al. (2006) state primordium placement precision is about 15 deg. Different organs and taxa (sunflower florets vs Arabidopsis siliques); disagreement preserved.
- Mechanism of the inhibitory field. Reinhardt et al. (2003) and Smith et al. (2006) present auxin depletion by PIN1 transport as the inhibitor. Besnard et al. (2014) add an AHP6 cytokinin-signalling field for robustness, and Smith et al. themselves report transport alone did not sustain spirals in their simulations. A separate line of theory attributes the pattern to mechanical buckling of the meristem surface; a 2008 J Theor Biol paper ("Phyllotaxis: cooperation and competition between mechanical and biochemical processes", 251:421-439) compares and couples the auxin and buckling models, and Lee & Levitov (1998) present a mechanical (deformable-lattice) theory. We read only titles and abstracts of the mechanical work. Unresolved.
:::

## Sources

| Citation | Read-level |
|---|---|
| Landrein B, Refahi Y, Besnard F, Hervieux N, Mirabet V, Boudaoud A, Vernoux T, Hamant O (2015) Meristem size contributes to the robustness of phyllotaxis in Arabidopsis. J Exp Bot 66(5):1317-1324. doi:10.1093/jxb/eru482 | `full-text` |
| Swinton J, Ochu E, MSI Turing's Sunflower Consortium (2016) Novel Fibonacci and non-Fibonacci structure in the sunflower: results of a citizen science experiment. R Soc Open Sci 3(5):160091. doi:10.1098/rsos.160091 | `full-text` |
| Smith RS, Guyomarc'h S, Mandel T, Reinhardt D, Kuhlemeier C, Prusinkiewicz P (2006) A plausible model of phyllotaxis. PNAS 103(5):1301-1306. doi:10.1073/pnas.0510457103 | `full-text` |
| Refahi Y, Brunoud G, Farcot E, Jean-Marie A, Pulkkinen M, Vernoux T, Godin C (2016) A stochastic multicellular model identifies biological watermarks from disorders in self-organized patterns of phyllotaxis. eLife 5:e14093. doi:10.7554/eLife.14093 | `full-text` |
| Okabe T (2015) Biophysical optimality of the golden angle in phyllotaxis. Sci Rep 5:15358. doi:10.1038/srep15358 | `full-text` |
| Okabe T (2015) Extraordinary accuracy in floret position of Helianthus annuus. Acta Soc Bot Pol 84:79-85 | `search-summary` |
| Turner HA, Humpage M, Kerp H, Hetherington AJ (2023) Leaves and sporangia developed in rare non-Fibonacci spirals in early leafy plants. Science 380:1188-1192. doi:10.1126/science.adg4014 | `search-summary` |
| Douady S, Couder Y (1992) Phyllotaxis as a physical self-organized growth process. Phys Rev Lett 68(13):2098-2101 | `search-summary` |
| Reinhardt D, Pesce ER, Stieger P, Mandel T, Baltensperger K, Bennett M, Traas J, Friml J, Kuhlemeier C (2003) Regulation of phyllotaxis by polar auxin transport. Nature 426:255-260. doi:10.1038/nature02081 | `could-not-access` |
| Besnard F, Farcot E, Refahi Y, ... Vernoux T (2014) Cytokinin signalling inhibitory fields provide robustness to phyllotaxis. Nature 505(7483):417-421. doi:10.1038/nature12791 | `abstract` |
| Strauss S, Lempe J, Prusinkiewicz P, Tsiantis M, Smith RS (2020) Phyllotaxis: is the golden angle optimal for light capture? New Phytol 225(1):499-510 | `abstract` |
| Phyllotaxis: cooperation and competition between mechanical and biochemical processes. J Theor Biol 251(3):421-439 (2008). doi:10.1016/j.jtbi.2007.11.036 | `abstract` |
| Lee H-W, Levitov L (1998) Universality in phyllotaxis: a mechanical theory. In Jean RV, Barabe D (eds) Symmetry in Plants, World Scientific. arXiv:2101.02652 | `abstract` |


---

*Generated from [`library/laws/phyllotaxis.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/phyllotaxis.yaml). Do not edit this page; edit the YAML.*
