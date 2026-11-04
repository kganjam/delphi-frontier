---
title: The adder model of cell-size homeostasis
label: law-adder-cell-size
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-adder-cell-size
V_d = V_b + \Delta, \qquad \operatorname{cov}(\Delta, V_b) = 0
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `V_d` | L^3 | um^3 | cell volume at division |
| `V_b` | L^3 | um^3 | cell volume at birth |
| `Delta` | L^3 | um^3 | volume added between birth and division. The adder claim is that its distribution does not depend on V_b. For rod-shaped bacteria of near-constant width, length is used as the proxy for volume and Delta is reported in um of length. |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `slope_division_on_birth_adder` | 1 — *derived* | Follows from the equation with Delta independent of V_b: the regression slope of V_d on V_b is 1, and the slope of Delta on V_b is 0. The rival models give, for the same regression, 0 (sizer: divide at a fixed size) and 2 (timer: a fixed interval of exponential growth that on average doubles the cell). Those two numbers are derived here from the definitions; they are not measurements. |
| `perturbation_decay_per_generation` | 0.5 — *derived* | For symmetric division, V_b(n+1) = (V_b(n) + Delta)/2, so a deviation of birth size from its mean is multiplied by 1/2 each generation. Derived from the equation, not measured. Taheri-Araghi et al. 2015 report (summariser-relayed) that the autocorrelations of birth size, division size and generation time decay by a factor of 2 per generation in their data, which is the observed counterpart of this derived value. |
| `mother_daughter_generation_time_correlation` | -0.25 — *derived* | Taheri-Araghi et al. 2015 state that the adder PREDICTS a correlation of -1/4 between mother and daughter generation times and that their data confirm it (their Fig. S4). The -1/4 is the model prediction; the measured value is in a supplementary figure I did not read, so no measured number is asserted here. |
| `caulobacter_added_length_stalked` | 1.81 (interval 1.45 to 2.17) um | MEASURED, Campos et al. 2014, Caulobacter crescentus CB15N stalked progeny, n = 565: added length 1.81 +/- 0.36 um (mean +/- SD). The interval is +/- 1 SD of cell-to-cell spread, NOT a confidence interval on the mean. Kendall tau between added length and birth length = -0.001, the cleanest adder signature retrieved for this entry. Swarmer progeny: 2.06 +/- 0.35 um, n = 141. |
| `ecoli_added_length_LB` | 3.23 (interval 2.63 to 3.83) um | MEASURED, Campos et al. 2014, E. coli BW25113 in LB, n = 1305: 3.23 +/- 0.60 um (mean +/- SD; interval is +/- 1 SD). In M9 the same strain added 2.26 +/- 0.59 um (n = 1528) with Kendall tau 0.03 against birth length. Delta is therefore a property of the CONDITION, not of the species: the same strain adds about 43 per cent more length in rich medium (3.23/2.26 = 1.43, my arithmetic on their means). |
| `ecoli_added_vs_birth_correlation_witz` | -0.12 (interval -0.12 to -0.04) | MEASURED, Witz, van Nimwegen & Julou 2019, E. coli in M9 at 37 C: Pearson r between added length (birth to division) and birth length was -0.10 (glycerol, automated analysis), -0.07 (glycerol), -0.04 (glucose) and -0.12 (glucose + amino acids). The interval is the RANGE of those four condition values, not a confidence interval. The value field holds the largest-magnitude one. Small, consistently negative, i.e. slightly sizer-ward of a pure adder; the authors say added length weakly anti-correlates with birth length in fast growth. |
| `ecoli_slow_growth_delta_slope` | -0.31 | MEASURED, Si et al. 2019, E. coli NCM3722 at a doubling time of about 4 h (MOPS minus NH4Cl, 0.4% glucose, 5 mM arginine), in their own experiment and in their reanalysis of Wallden et al. 2016: slope of added size on birth size = -0.31. Adder = 0, sizer = -1. The deviation from adder is significant (p = 1.4e-6). Si et al. call it much closer to adder than sizer; Wallden et al. read the same condition as a departure from adder. No interval was found in the portion I read. |
| `msmegmatis_slope_glycerol` | 0.996 (interval 0.894 to 1.098) | MEASURED, Priestman et al. 2017, Mycobacterium smegmatis in HdB + glycerol, n = 544: slope 0.996 +/- 0.102, which the authors call consistent with an adder. The interval is +/- the reported error; whether that error is an SD, SE or CI was not stated in the text relayed to me. As relayed, this is the slope of division length on birth length (adder = 1). |
| `msmegmatis_slope_pyruvate` | 0.832 (interval 0.695 to 0.969) | MEASURED, Priestman et al. 2017, M. smegmatis on pyruvate, n = 367: slope 0.832 +/- 0.137, described by the authors as more sizer-like. Same caveat on the error type. On acetate the population slope was adder-consistent, but new-pole inheritors gave 0.682 +/- 0.187 (n = 186), which the authors call not consistent with an adder. |
| `pombe_slope_length` | 0.25 (interval 0.23 to 0.27) | MEASURED, Facchetti et al. 2019, Schizosaccharomyces pombe wild type (FC15), n = 256: slope of division length on birth length 0.25 +/- 0.02. Adder = 1, sizer = 0. The authors conclude the cell is a SIZER on SURFACE AREA, and that the non-zero slope in length arises because length is not the controlled variable. |
| `arabidopsis_meristem_slope` | 0.5 | MEASURED, Willis et al. 2016, Arabidopsis thaliana shoot apical meristem epidermis (central zone), 1013 complete cell cycles: slope of division volume on birth volume f of about 0.5 (their fit V_d = 0.5 V_b + mu_b(1.5 + noise)), with a strong NEGATIVE correlation between added volume and birth volume (P = 1e-64, pooled). Their words: plant stem cells do not add a fixed size between divisions. No interval on f was found in the portion I read. |
| `mammalian_slope_range` | unknown (interval 0.7 to 1.2) | MEASURED range, Cadart et al. 2018: slopes of volume at mitosis on volume at birth range from 0.7 to 1.2 across the cultured mammalian lines they analysed. The per-line values are in a figure table I did not read, so no single value is asserted. One line, Raji, was NOT adder: added volume correlated POSITIVELY with birth volume, with large dispersion. |

## Why it holds

PHENOMENOLOGICAL, and this matters more than anything else in the entry. The adder states a statistical regularity: across a steadily growing population, the volume a cell adds between birth and division is independent of the volume it was born with. It does not by itself name a molecule. Written as a linear response, V_d = a V_b + b, the adder is a = 1 (sizer a = 0, timer a = 2), and for symmetric division it pulls a size deviation back by half each generation -- a weaker correction than a sizer, which removes it in one cycle, but enough to keep the size distribution bounded where a timer would let it random-walk.
Proposed molecular readings, each the AUTHORS' claim and not settled: (i) Amir 2014 -- a constant volume added per origin between successive replication INITIATIONS, from which the birth-to-division adder follows; (ii) Si et al. 2019 -- division triggers when a division protein (FtsZ is their candidate) reaches a threshold amount, with its synthesis balanced to volume growth, so a fixed amount accumulated equals a fixed volume added; (iii) Witz et al. 2019 -- two counters both reset at initiation, one timing the next initiation and one timing division, with the birth-to-division adder emerging from them; (iv) Micali et al. 2018 -- division waits for the slower of two concurrent processes. In mammalian cells Cadart et al. 2018 find the near-adder achieved by modulating BOTH cycle-phase duration and growth rate, which is a different route to the same statistic.

## Where it holds

- **growth**: steady-state, balanced exponential growth in constant conditions
- **taxa**: ['Escherichia coli (multiple strains; MOPS and M9 media; doubling times about 17 to 89 min)', 'Bacillus subtilis (doubling times about 17 to 39 min)', 'Caulobacter crescentus (stalked and swarmer progeny)', 'Mycobacterium smegmatis on glycerol', 'Halobacterium salinarum (an archaeon)', 'budding yeast, when the increment is counted between budding events', 'most cultured mammalian lines, as a NEAR-adder']
- **notes**: Taheri-Araghi et al. 2015 established the adder across hundreds of thousands of E. coli and B. subtilis cells, and report that the Delta distributions of different conditions collapse onto one curve when rescaled by their mean, so a condition changes the statistics only through mean Delta. Eun et al. 2018 report an adder in H. salinarum with noisier growth and division than E. coli (abstract only). Soifer, Robert & Amir 2016 report budding yeast is well described by an increment added between successive buddings rather than from birth to division (abstract only). OUTSIDE steady state -- nutrient shifts, transients after a perturbation -- I retrieved no measurement either way, and the adder should not be assumed there.

:::{danger} Where it breaks
THE MEASURED FAILURE BOUNDARIES, each tied to a named condition and number.

(1) SLOW-GROWING E. COLI, doubling time about 4 h: the slope of added size on birth size is -0.31 against an adder value of 0, significant at p = 1.4e-6 (Si et al. 2019, own data and reanalysis of Wallden et al. 2016). It deviates TOWARD the sizer. Si et al. restore the adder by repressing clpX, and BREAK it deliberately by periodic under-expression of ftsZ, which makes division size oscillate while initiation size is unaffected. Si et al. state this is the only known steady-state condition in which E. coli significantly deviates; that is their scope statement, not a search of mine.

(2) MYCOBACTERIA ON POOR CARBON SOURCES: M. smegmatis is adder on glycerol (slope 0.996 +/- 0.102, n = 544) but sizer-ward on pyruvate (0.832 +/- 0.137, n = 367), and on acetate the new-pole daughters give 0.682 +/- 0.187 (n = 186) although the pooled population looks adder-like (Priestman et al. 2017). A pooled slope can therefore hide a sub-population that is not adder -- pole age, i.e. asymmetric inheritance, is the hidden variable.

(3) FISSION YEAST: slope 0.25 +/- 0.02 in length (n = 256), and the authors conclude the control is a sizer on surface area (Facchetti et al. 2019). Not an adder, and the variable controlled is not the one plotted.

(4) PLANT MERISTEM: Arabidopsis shoot apical meristem epidermal cells give a division-on-birth slope of about 0.5 over 1013 cycles, with added volume strongly anti-correlated with birth volume (Willis et al. 2016): intermediate between sizer and adder. Their reported ~75 per cent decay of a size fluctuation per generation matches what a slope of 0.5 implies (my derivation: deviation multiplied by f/2 = 0.25), against 50 per cent for an adder.

(5) MAMMALIAN CELLS: slopes 0.7 to 1.2 across cultured lines, so near-adder is a band, not a point; the Raji line is not adder at all, with added volume rising with birth volume (Cadart et al. 2018). Within the cycle the adder is not phase-by-phase: G1/S volume against birth volume gives slopes of 0.69 to 0.71 in HeLa and HT29 reporter lines, which the authors read as between adder and sizer.

(6) THE WRONG INTERVAL: in budding yeast the increment is reported to be added between budding events, not from birth to division (Soifer et al. 2016, abstract). Fitting a birth-to-division adder there measures the wrong interval.

(7) THE SIGNATURE DOES NOT IDENTIFY THE MECHANISM. Facchetti et al. 2019 state that pure sizer control can in some circumstances reproduce apparent adder behaviour in E. coli, through cell-radius variability combined with volume sizing; Witz et al. 2019 derive the birth-to-division adder as an emergent consequence of initiation-based counters. A slope of 1 is a SCREEN, not proof of an adder mechanism.

WHAT AN ENGINEER SHOULD TAKE FROM THIS: the adder is safe to use as a null model only for a symmetrically dividing microbe in steady, reasonably fast growth on a good carbon source. For slow growth, poor carbon sources, asymmetric division, fission yeast, plant meristems, or any population that pools mothers and daughters or old and new poles, measure the slope first; the measured values above run from 0.25 to 1.2.
:::

## Worked examples

**a symmetrically dividing cell born at twice the mean birth size, under the three models**

```
at steady state mean Delta = mean V_b; call that unit 1, so this cell has V_b = 2
  adder (a = 1): V_d = 2 + 1        = 3   -> daughters born at 1.5  (excess 1.0 -> 0.5)
  sizer (a = 0): V_d = mean V_d     = 2   -> daughters born at 1.0  (excess removed in one cycle)
  timer (a = 2): V_d = 2 * 2        = 4   -> daughters born at 2.0  (excess never removed)
```

- value: `3`

- DERIVED from the definitions, not observed. The three predictions for division size are 2, 3 and 4 units for the same oversized cell, separated by a full mean birth volume each, so a single experiment that over-sizes cells at birth discriminates the models far more sharply than the population slope does.

- evidence: **derived**

**Arabidopsis shoot apical meristem (consistency check of a published number)**

```
linear response V_d = f * V_b + c, symmetric division: V_b(n+1) = (f * V_b(n) + c)/2
  deviation multiplier per generation = f/2
  adder   f = 1.0 -> 0.50 retained -> 50% decay
  Willis f = 0.5 -> 0.25 retained -> 75% decay
  sizer   f = 0.0 -> 0.00 retained -> 100% decay
```

- value: `0.75`

- DERIVED by me from Willis et al.'s measured slope; Willis et al. separately report a ~75 per cent decay per generation, and the two agree. The derivation assumes symmetric division, which the meristem does not strictly obey (Willis et al. report asymmetric divisions with the smaller daughter growing faster), so the agreement is a consistency check, not a test.

- evidence: **derived**

**Caulobacter crescentus stalked cell, hypothetical birth length**

```
L_d = L_b + Delta_L, Delta_L = 1.81 +/- 0.36 um (Campos et al. 2014, mean +/- SD)
  for an assumed L_b = 2.00 um: L_d = 3.81 um, 1-SD band 3.45 to 4.17 um
```

- value: `3.81`

- The birth length of 2.00 um is an ASSUMED input chosen for illustration, not a measured Caulobacter value; the added length and its spread are measured. The point is that the adder turns one measured number into a prediction for any birth size -- and that the prediction band (+/- 0.36 um) is set by the spread of Delta, which Taheri-Araghi et al. report is the most variable quantity in the cycle.

- evidence: **derived**

:::{seealso} Contested
- WHAT IS ADDED, AND FROM WHEN. Amir 2014 and Witz et al. 2019 place the controlled increment at replication INITIATION (per-origin volume between initiations; or two counters reset at initiation), making the birth-to-division adder emergent. Si et al. 2019 report that perturbing ftsZ breaks the division adder while leaving the initiation adder intact, and attribute division to threshold accumulation of a division protein. My inference, not either group's statement: if division timing were set from initiation as Witz et al. propose, a perturbation that leaves initiation unchanged would not be expected to break the division adder, so the two accounts are in tension. Not reconciled here.
- CONCURRENT PROCESSES. Micali et al. 2018 argue that division is set by the slower of two concurrent processes, one setting initiation and one setting inter-division time, and that this reproduces the adder. Witz et al. 2019 judge that model potentially consistent but only with precise parameter tuning across conditions. Recorded from Witz et al.'s text and a search summary of Micali et al.; I did not read Micali et al. itself.
- IS THE ADDER REAL OR AN ARTEFACT OF THE VARIABLE? Facchetti et al. 2019 argue a volume sizer plus radius variability can produce an apparent length adder in E. coli and say a sizer explanation for E. coli cannot be fully ruled out. Taheri-Araghi et al. 2015 reject both sizer and timer on the correlation data. Preserved as a live disagreement.
- IS SLOW-GROWTH E. COLI AN ADDER? Wallden et al. 2016 read it as a departure from adder; Si et al. 2019, reanalysing the same data, call slope -0.31 much closer to adder than sizer while agreeing the deviation is significant. Same number, two readings. I have Wallden et al.'s position only as relayed by Si et al.
- See also the library entry cell-size-adder, which treats sizer, timer and adder together. This entry overlaps it deliberately and was written independently; where the two disagree on a number, check the sources rather than either entry.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taheri-Araghi S, Bradde S, Sauls JT, Hill NS, Levin PA, Paulsson J, Vergassola M, Jun S (2015) Curr Biol 25:385-391, Cell-size control and homeostasis in bacteria, doi 10.1016/j.cub.2014.12.009, PMC4323405 | `full-text` |
| Campos M, Surovtsev IV, Kato S, Paintdakhi A, Beltran B, Ebmeier SE, Jacobs-Wagner C (2014) Cell 159:1433-1446, A constant size extension drives bacterial cell size homeostasis, doi 10.1016/j.cell.2014.11.022, PMC4258233 | `full-text` |
| Amir A (2014) Phys Rev Lett 112:208102, Cell size regulation in bacteria, doi 10.1103/PhysRevLett.112.208102 | `abstract` |
| Si F, Le Treut G, Sauls JT, Vadia S, Levin PA, Jun S (2019) Curr Biol 29:1760-1770.e7, Mechanistic origin of cell-size control and homeostasis in bacteria, doi 10.1016/j.cub.2019.04.062, PMC6548602 | `full-text` |
| Witz G, van Nimwegen E, Julou T (2019) eLife 8:e48063, Initiation of chromosome replication controls both division and replication cycles in E. coli through a double-adder mechanism, doi 10.7554/eLife.48063, PMC6890467 | `full-text` |
| Wallden M, Fange D, Lundius EG, Baltekin O, Elf J (2016) Cell 166:729-739, The synchronization of replication and division cycles in individual E. coli cells, doi 10.1016/j.cell.2016.06.052 | `listing` |
| Micali G, Grilli J, Osella M, Cosentino Lagomarsino M (2018) Sci Adv 4:eaau3324, Concurrent processes set E. coli cell division, doi 10.1126/sciadv.aau3324 | `search-summary` |
| Priestman M, Thomas P, Robertson BD, Shahrezaei V (2017) Front Cell Dev Biol 5:64, Mycobacteria modify their cell size control under sub-optimal carbon sources, doi 10.3389/fcell.2017.00064, PMC5506092 | `full-text` |
| Facchetti G, Knapp B, Chang F, Howard M (2019) Biophys J 117:1728-1738, Reassessment of the basis of cell size control based on analysis of cell-to-cell variability, doi 10.1016/j.bpj.2019.09.031, PMC6838950 | `full-text` |
| Willis L, Refahi Y, Wightman R, Landrein B, Teles J, Huang KC, Meyerowitz EM, Jonsson H (2016) PNAS 113:E8238-E8246, Cell size and growth regulation in the Arabidopsis thaliana apical stem cell niche, doi 10.1073/pnas.1616768113, PMC5187701 | `full-text` |
| Cadart C, Monnier S, Grilli J, Saez PJ, Srivastava N, Attia R, Terriac E, Baum B, Cosentino-Lagomarsino M, Piel M (2018) Nat Commun 9:3275, Size control in mammalian cells involves modulation of both growth rate and cell cycle duration, doi 10.1038/s41467-018-05393-0, PMC6095894 | `full-text` |
| Eun YJ, Ho PY, Kim M, LaRussa S, Robert L, Renner LD, Schmid A, Garner E, Amir A (2018) Nat Microbiol 3:148-154, Archaeal cells share common size control with bacteria despite noisier growth and division, doi 10.1038/s41564-017-0082-6 | `abstract` |
| Soifer I, Robert L, Amir A (2016) Curr Biol 26:356-361, Single-cell analysis of growth in budding yeast and bacteria reveals a common size regulation strategy, doi 10.1016/j.cub.2015.11.067 | `abstract` |
| Logsdon MM et al. (2017), a parallel-adder model for Mycobacterium smegmatis and BCG | `search-summary` |


---

*Generated from [`library/laws/adder-cell-size.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/adder-cell-size.yaml). Do not edit this page; edit the YAML.*
