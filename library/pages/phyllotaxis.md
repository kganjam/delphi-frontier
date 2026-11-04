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
\alpha_t = \frac{2\pi}{t + \varphi^{-1}},\qquad \alpha_2 = \frac{2\pi}{\varphi^{2}} = 2\pi\left(1-\varphi^{-1}\right) \approx 137.5078^\circ,\qquad \varphi = \frac{1+\sqrt5}{2}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `alpha` | 1 | rad | limiting divergence angle between successively initiated organs on the branch labelled t |
| `t` | 1 | dimensionless | integer labelling the branch. The parastichy numbers run 1, t, t+1, 2t+1, ... t = 2 is the main Fibonacci branch (golden angle). t = 3 is the Lucas-type branch 1, 3, 4, 7, 11. t = 1 gives 222.49 deg, the complement of the golden angle, which is the same spiral read in the other direction |
| `phi` | 1 | dimensionless | golden ratio (1 + sqrt 5)/2 = 1.6180340 |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `golden_angle` | 137.508 deg — *derived* | EXACT and calculated, not measured: 360/phi^2 = 360*(1 - 1/phi) = 137.50776 deg (computed in this session). A mathematical constant has no measurement interval, so none is given. |
| `lucas_branch_angle` | 99.5016 deg — *derived* | Calculated from the equation with t = 3: 360/(3 + 1/phi) = 99.5016 deg. This is the angle a Lucas-type spiral (parastichy numbers 4, 7, 11, 18) converges to. A t = 4 branch gives 77.955 deg and a t = 5 branch gives 64.079 deg (also calculated). |
| `mean_divergence_angle_arabidopsis_col0` | 136 deg — *observed* | OBSERVED. Landrein et al. 2015, Table 1: Col-0 inflorescence, mean angle 136 deg in both growth regimes. Short-then-long days: 704 angles, 29 sequences. Long days only: 1193 angles, 34 sequences. interval is null because the table reports no SD or CI, NOT because the spread is zero. The paper does not say whether this is an arithmetic or a circular mean, or how permuted pairs were handled. The paper's own Col-0 counts also differ between sections: the Fig. 2 legend gives 703 angles and 23 plants, and the Fig. 5 legend gives 1190 angles and 34 plants. That discrepancy is preserved here, not resolved. The difference from the golden angle, 136 - 137.508 = -1.5 deg, is my arithmetic. Without a dispersion, I cannot say whether that difference is significant. |
| `mean_divergence_angle_arabidopsis_other_genotypes` | unknown deg — *observed* | OBSERVED, Landrein et al. 2015 Table 1. These are different genotypes and growth regimes, not a dispersion around one quantity, so they are tabulated rather than pooled. The range 128-141 deg is a span of genotype means. It is NOT an interval on the golden angle. |
| `permuted_organ_fraction_arabidopsis` | unknown fraction of organs — *observed* | OBSERVED, Landrein et al. 2015 Table 1. The same table gives the percentage of non-canonical angles: Col-0 23 / 5.7, WS-4 60.5 / 16, clasp-1 14.8 / 11.2 (short-then-long / long days only). Landrein et al. report that meristem size is positively correlated with the number of permutations. Refahi et al. 2016 describe permutations in "around half of the cases" in live-imaged meristems and "almost 30% of organs co-initiated". Those figures use a different denominator (cases and organs at the meristem, not organs along a mature stem), so they are not directly comparable with the Landrein percentages. They are kept side by side. |
| `sunflower_parastichy_counts` | unknown count of parastichy numbers — *observed* | OBSERVED, Swinton, Ochu et al. 2016 Table 1 (photo-reviewed subset, 657 sunflowers). The fractions are my arithmetic on the authors' counts: strict Fibonacci 565/768 = 0.736; Fibonacci-type structure 632/768 = 0.823; neither 136/768 = 0.177. The denominator is PARASTICHY NUMBERS, not flower heads. The paper counts spirals and does not measure divergence angles. For historical comparison it quotes Schoute at 82% and Weisse at 95% main-sequence Fibonacci, and the three figures are kept separate here. |
| `primordium_placement_resolution_arabidopsis` | 15 deg — *derived* | An ESTIMATE by Smith et al. 2006, not a measurement of angular noise: about 24 cells around the peripheral zone of the Arabidopsis apex limits placement precision to about 360/24 = 15 deg. It is a geometric resolution limit on individual organs, which is why the authors call for a robust patterning mechanism. |

## Why it holds

WHAT IS EXPLAINED. Organs are initiated one at a time on the flank of the shoot apical meristem, and a new one forms only where it is far enough from the existing ones (a lateral-inhibition rule). Douady & Couder 1992 built a physical analogue: ferrofluid drops released periodically into a magnetic-field gradient, repelling one another as they drift outward. Their result, which I know only from the citation record and secondary accounts (the paper was not read; there is no abstract in Europe PMC), is that sequential, inhibition-limited placement self-organises into Fibonacci spirals with a divergence near the golden angle. On that account the golden angle is an attractor of the iteration, not a value encoded anywhere. Reinhardt et al. 2003 (experimental, abstract read) identify the molecular inhibitor as depletion of the hormone auxin. Existing primordia act as auxin sinks, and auxin accumulates only at certain minimal distances from them. Smith et al. 2006 built a computer SIMULATION of that transport model. They report that it reproduces the divergence angles measured in Arabidopsis seedlings "within the standard error", and that it also produces distichous, decussate and tricussate patterns. That is a simulated match to observations, not an observation. Besnard et al. 2014 (abstract read) add a second inhibitory field, made by the mobile cytokinin-signalling inhibitor AHP6 downstream of auxin. They report that this field contributes to robustness by imposing a temporal sequence on organ initiation.
WHAT IS NOT EXPLAINED, as far as the sources read here go. (a) WHY THE FIBONACCI BRANCH DOMINATES. The same dynamics admit the Lucas and n:(n+1) branches. No source read predicts their frequency: neither the 17.7% non-Fibonacci sunflower parastichy numbers (my arithmetic on Swinton et al.) nor the finding that every spiral in the Devonian lycopod Asteroxylon mackiei was n:(n+1) (Turner et al. 2023). Swinton et al. themselves say that some non-Fibonacci pairs would "pose a particularly severe challenge to models of the Douady and Couder type". (b) HOW THE PATTERN IS SUSTAINED. Smith et al. 2006 state that they "were not able to obtain sustained spiral phyllotactic patterns by using that mechanism alone", meaning the transport mechanism alone. Spirals appeared only after they added three hypothesised elements: zone-dependent auxin production, enhanced auxin production in primordia, and an auxin cap draining into vasculature. The published auxin account is therefore a sufficient model with extra assumptions, not a demonstration that auxin transport alone gives 137.5 deg. (c) THE SOURCE OF THE NOISE. Refahi et al. 2016 name "noise on inhibition perception as the most likely origin of disorders". That is a model inference, not a measurement of the noise source. (d) WHETHER THE ANGLE IS ADAPTIVE. This is contested; see contested_by.

## Where it holds

- **pattern class**: spiral (alternate, one organ per node) phyllotaxis at the shoot apex
- **regime**: steady initiation after the system has settled onto a branch; not during phyllotactic transitions
- **quantity**: a sequence or population mean of divergence angles between successively INITIATED organs. Not a per-organ value, and not necessarily the angle read off a mature stem after permutations or torsion
- **demonstrated in**: ['Arabidopsis thaliana inflorescence: observed mean 136 deg for Col-0 (Landrein et al. 2015)', 'Arabidopsis seedlings: simulated angles match observed ones within SE (Smith et al. 2006)', 'Helianthus annuus capitulum: parastichy counts only, no angles (Swinton et al. 2016)']
- **notes**: My inference from the sources, not a claim made in any of them: 137.5 deg is the expected divergence wherever organs are placed singly by a lateral-inhibition rule and the system has relaxed onto the t = 2 branch. When organs are initiated in pairs or whorls, or the system sits on another branch, the same mechanism gives a different angle, and 137.5 deg is the wrong prediction.

:::{danger} Where it breaks
(1) NON-SPIRAL PHYLLOTAXIS: the law does not apply at all. Distichous arrangements diverge by 180 deg and decussate ones by 90 deg between opposite pairs. Whorls place several organs at each node. Smith et al. 2006 report that their auxin model also produces distichous, decussate and tricussate patterns, so these are regimes of the same mechanism, not anomalies. A checker expecting 137.5 deg would be wrong by 42.5 deg on a distichous plant and by 47.5 deg on a decussate one (my arithmetic). I give no taxon list here, because which families are distichous or decussate was not verified against a source in this session. (2) OTHER SPIRAL BRANCHES. A Lucas-type spiral converges to 99.50 deg, not 137.5 deg (calculated). Swinton et al. 2016 observed Lucas parastichy numbers in 41 of 768 counts in sunflower. Turner et al. 2023 report that every spiral in Asteroxylon mackiei, an Early Devonian lycopod, was n:(n+1) non-Fibonacci, alongside whorls. So the golden angle fails across a whole fossil taxon at the base of the leafy lycophyte lineage, as well as within a living species. (3) INDIVIDUAL ORGANS, EVEN IN A GOOD SPIRAL. In Arabidopsis Col-0, 2.1% to 14% of organs are permuted depending on growth regime. In WS-4 under short-then-long days the figure is 43.3%, with 60.5% of angles non-canonical (observed, Landrein et al. 2015). When two successive organs swap order, a perfect 137.5 deg spiral reads as successive angles of 275.0, 222.5 and 275.0 deg (my calculation). The individual angle is therefore NOT a valid check, even where the underlying spiral is golden. Smith et al. 2006 estimate a geometric resolution of only about 15 deg per organ at the Arabidopsis apex. (4) GENOTYPE AND ENVIRONMENT MOVE THE MEAN. Within one species the observed genotype means run from 128 deg (clasp-1, long days) to 141 deg (WS-4, long days) (Landrein et al. 2015). That is -9.5 to +3.5 deg from the golden angle (my arithmetic), and no dispersion is reported for any of them. (5) THE LAW SAYS NOTHING ABOUT FUNCTION. In SIMULATIONS (not observations) by Strauss et al. 2020, other angles from Fibonacci-like series were "equally optimal for light capture". Matching 137.5 deg therefore does not certify a light-capture, packing or vascular benefit. Negative-search scope: I found no source giving a measured wild-type mean together with an SD or CI for divergence angle. I checked Landrein et al. 2015 Table 1 (full text, PMC), Refahi et al. 2016 (first ~100,000 of ~237,000 characters of the eLife page), and the Smith et al. 2006 text (PMC; the values are in Fig. 5, which was not visible). Besnard et al. 2014 was seen only as an abstract.
:::

## Worked examples

**branch angles from the equation**

```
phi = 1.6180340
  t = 1 : 360/(1 + 0.618034) = 222.492 deg  (complement of the golden angle; same spiral, other direction)
  t = 2 : 360/(2 + 0.618034) = 137.508 deg  (Fibonacci branch, golden angle)
  t = 3 : 360/(3 + 0.618034) =  99.502 deg  (Lucas-type branch, 4:7:11)
  t = 4 : 360/(4 + 0.618034) =  77.955 deg
```

- value: `137.50776405`

- CALCULATED in this session. Adjacent branches are 38 to 85 deg apart, so the branch is identifiable from a mean angle even at the roughly 15 deg per-organ resolution Smith et al. estimate. That is the one use of this law I would treat as a check, and it is a classification, not a tolerance.

- evidence: **derived**

**Arabidopsis thaliana Col-0 inflorescence**

```
observed mean 136 deg - derived 137.508 deg = -1.5 deg
```

- value: `136`

- The 136 deg is OBSERVED (Landrein et al. 2015). The -1.5 deg is my arithmetic. Because the source reports no SD, this is not a test of the law. It shows only that the observed mean sits on the t = 2 branch and not on t = 3 (99.5 deg).

- evidence: **literature**

**a perfect golden spiral with organs 1 and 2 permuted**

```
initiation positions 0, a, 2a, 3a with a = 137.508 deg; read along the stem as 0, 2a, a, 3a
  successive differences: 2a = 275.0 deg, -a mod 360 = 222.5 deg, 2a = 275.0 deg
```

- value: `275.0`

- CALCULATED. This is the signature of a permutation in a measured sequence. A pipeline that scores individual angles against 137.5 deg would count the three angles as three failures when there is one order swap.

- evidence: **derived**

**Helianthus annuus (sunflower) capitula**

```
565 / 768 = 0.736 strict Fibonacci; 632 / 768 = 0.823 Fibonacci-type; 136 / 768 = 0.177 neither
```

- value: `0.823`

- Counts OBSERVED by Swinton et al. 2016. Fractions calculated here. These are parastichy counts, not angles. They support the branch-dominance pattern without measuring the angle.

- evidence: **literature**

:::{seealso} Contested
- USABILITY, within this library. golden-angle.yaml classifies the golden angle as CONSTRAINING. It treats the exact angle plus the roughly 18% non-Fibonacci sunflower fraction as a target with a measured tolerance. This entry classifies it as DESCRIPTIVE. The sunflower fraction is a tolerance on parastichy COUNTS, not on angles, and no measured dispersion of divergence ANGLE was found. Both readings are recorded and neither entry has been edited to agree with the other.
- PERMUTATION RATE: two sources, two denominators. Refahi et al. 2016 describe permutations in "around half of the cases" and almost 30% of organs co-initiated (live imaging at the meristem). Landrein et al. 2015 report 2.1% to 43.3% permuted organs depending on genotype and regime (mature inflorescence). golden-angle.yaml quotes the Refahi figure. Not reconciled.
- ADAPTIVE VALUE. Okabe 2015 proposes an adaptive explanation: the golden angle minimises the energy cost of phyllotaxis transitions (a theoretical model). Strauss et al. 2020 find in simulation that other Fibonacci-like angles are equally good for light capture. They argue that the iterative positioning mechanism, not a specific angle, is the more likely target of selection. Both are model results, and neither is a measurement of fitness.
- PRECISION. Strauss et al. 2020 write that plants control the divergence angle "sometimes to within a fraction of a degree", and that sentence cites no measurement in the abstract read. Smith et al. 2006 estimate a resolution of about 15 deg per primordium at the Arabidopsis apex. My inference: these may refer to a sequence mean and to an individual organ respectively, but neither source says so. Not reconciled.
- FIBONACCI FREQUENCY. Schoute 82%, Weisse 95% (both as quoted by Swinton et al. 2016), and Swinton et al.'s own 73.6% strict or 82.3% Fibonacci-type. These have different denominators and different strictness and are kept separate. A widely repeated figure of over 90% across about 650 species was seen only as a search snippet attributed to the Turner et al. 2023 accepted manuscript. Its host could not be reached, so it is NOT used.
:::

## Sources

| Citation | Read-level |
|---|---|
| Douady S, Couder Y (1992) Phys Rev Lett 68:2098-2101, Phyllotaxis as a physical self-organized growth process, doi 10.1103/PhysRevLett.68.2098 | `listing` |
| Reinhardt D et al. (2003) Nature 426:255-260, Regulation of phyllotaxis by polar auxin transport, doi 10.1038/nature02081 | `abstract` |
| Smith RS, Guyomarc'h S, Mandel T, Reinhardt D, Kuhlemeier C, Prusinkiewicz P (2006) PNAS 103:1301-1306, A plausible model of phyllotaxis, doi 10.1073/pnas.0510457103, PMC1345713 | `full-text` |
| Besnard F et al. (2014) Nature 505:417-421, Cytokinin signalling inhibitory fields provide robustness to phyllotaxis, doi 10.1038/nature12791 | `abstract` |
| Landrein B, Refahi Y, Besnard F et al. (2015) J Exp Bot 66:1317-1324, Meristem size contributes to the robustness of phyllotaxis in Arabidopsis, doi 10.1093/jxb/eru482, PMC4339594 | `full-text` |
| Refahi Y et al. (2016) eLife 5:e14093, A stochastic multicellular model identifies biological watermarks from disorders in self-organized patterns of phyllotaxis, doi 10.7554/eLife.14093 | `full-text` |
| Swinton J, Ochu E, MSI Turing's Sunflower Consortium (2016) R Soc Open Sci 3:160091, Novel Fibonacci and non-Fibonacci structure in the sunflower, doi 10.1098/rsos.160091, PMC4892450 | `full-text` |
| Turner HA, Humpage M, Kerp H, Hetherington AJ (2023) Science 380:1188-1192, Leaves and sporangia developed in rare non-Fibonacci spirals in early leafy plants, doi 10.1126/science.adg4014 | `abstract` |
| Strauss S, Lempe J, Prusinkiewicz P, Tsiantis M, Smith RS (2020) New Phytol 225:499-510, Phyllotaxis -- is the golden angle optimal for light capture?, doi 10.1111/nph.16040 | `abstract` |
| Okabe T (2015) Sci Rep 5:15358, Biophysical optimality of the golden angle in phyllotaxis, doi 10.1038/srep15358, PMC4607949 | `abstract` |


---

*Generated from [`library/laws/phyllotaxis.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/phyllotaxis.yaml). Do not edit this page; edit the YAML.*
