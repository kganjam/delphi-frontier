---
title: Cell size control -- sizer, timer and adder
label: law-cell-size-adder
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-cell-size-adder
\text{adder: } L_d = L_b + \Delta \ (\text{slope }1), \quad \text{sizer: } L_d = \text{const} \ (\text{slope }0), \quad \text{timer: } L_d = L_b e^{\lambda\tau} \ (\text{slope }2)
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `L_d` | L | um | length (or volume) at division |
| `L_b` | L | um | length at birth |
| `Delta_add` | L | um | the size ADDED during the cycle  under the adder model its distribution is independent of L_b |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `adder_slope` | 1 | The slope of division size against birth size that identifies an adder. Sizer gives 0  timer gives 2 at the mean. This is the discriminating measurement. |
| `caulobacter_correlation` | -0.001 | Campos et al. 2014, Caulobacter crescentus stalked cells, n = 565: no significant correlation between the added length and the birth length (Kendall tau = -0.001). The cleanest adder signature retrieved. |
| `ecoli_mother_daughter_correlation` | 0.55 | Amir 2014 predicts a mother-daughter size correlation of 0.5 under the incremental model, against a measured 0.55 for slow-growing E. coli. A prediction and its test, which is rarer in this library than it should be. |
| `pombe_slope` | 0.25 (interval 0.23 to 0.27) | Facchetti et al. 2019, fission yeast: division-length against birth-length slope 0.25 +/- 0.02. A pure sizer would give 0. Their analysis nonetheless supports pure SIZER control on SURFACE AREA -- the slope in length units is not the slope in the controlled variable. |

## Why it holds

Three rival control schemes, distinguished by what the cell holds constant. A sizer divides at a fixed size, a timer divides after a fixed interval, an adder adds a fixed increment regardless of birth size. They are told apart by the slope of division size against birth size, which is the measurement the whole field is organised around. Amir's version locates the increment more precisely -- a constant volume per origin between replication INITIATIONS, not from birth to division -- and Wallden et al. 2016 have replication initiate at a fixed volume per chromosome.

## Where it holds

- **growth**: steady-state, balanced growth
- **taxa**: rod-shaped bacteria at moderate to fast growth rates  budding yeast during the budded phase
- **notes**: Taheri-Araghi et al. 2015 established the adder across hundreds of thousands of E. coli and B. subtilis cells, and Soifer, Robert & Amir 2016 found budding yeast very well described by the incremental model when measured between budding events.


:::{danger} Where it breaks
THE ADDER SIGNATURE ALONE DOES NOT IDENTIFY THE MECHANISM, and this is stated by the people who measured it: Facchetti et al. 2019 show a sizer can in some circumstances REPRODUCE apparent adder behaviour, so a slope of 1 is consistent with more than one control scheme and the inference from slope to mechanism is invalid without further evidence. That alone demotes the measurement from proof to screen. The adder also fails in named conditions rather than vaguely: slow growth is the only known steady-state condition in which E. coli significantly deviates, and it deviates TOWARDS the sizer (Si et al. 2019), with the adder restored at a doubling time of about 4 h by repressing clpX and systematically broken by oscillating FtsZ. Fission yeast gives a slope of 0.25, not 1, and its control appears to act on surface area rather than length -- so the variable being held constant is not even the one being plotted. In budding yeast the behaviour differs between mother and daughter within one organism: size control contributes significantly to G1 variability in DAUGHTERS but not in mothers, with a CLN3-dependent step extending G1 in small daughters, which is sizer-like. A single slope for a population mixing the two is an average of two mechanisms.
:::

## Worked examples

**a symmetrically dividing adder cell born 30 per cent oversized**

```
at steady state the mean added size Delta equals the mean birth size L_bar
each cycle: L_b(n+1) = (L_b(n) + Delta)/2, so the DEVIATION HALVES every generation
excess: 30% -> 15% -> 7.5% -> 3.75% over three generations
a sizer removes the excess in ONE cycle (Fantes reports exactly this for S. pombe)
a timer never corrects it, and noise accumulates without bound

```

- value: `3.75`

- This is why the three models matter rather than being a taxonomy: they differ in how fast a population forgets a size perturbation, which is the engineering-relevant quantity. The adder is a geometric decay, the sizer a single-step reset, the timer a random walk.

- evidence: **derived**

:::{seealso} Contested
- Facchetti et al. 2019 against the adder consensus: a sizer on surface area can produce an apparent adder in length, so the signature is degenerate. This is the most important disagreement in the entry and is preserved rather than resolved.
- Amir 2014 and Wallden et al. 2016 locate the controlled increment at replication initiation rather than between birth and division. These are refinements of what the adder adds, not rivals to the adder.
:::

## Sources

| Citation | Read-level |
|---|---|
| Campos M et al. (2014) Cell 159:1433-1446, A constant size extension drives bacterial cell size homeostasis, doi 10.1016/j.cell.2014.11.022, PMC4258233 | `full-text` |
| Taheri-Araghi S et al. (2015) Curr Biol 25:385-391, Cell-size control and homeostasis in bacteria, doi 10.1016/j.cub.2014.12.009, PMC4323405 | `full-text` |
| Amir A (2014) Phys Rev Lett 112:208102, Cell size regulation in bacteria, doi 10.1103/PhysRevLett.112.208102 | `full-text-preprint` |
| Soifer I, Robert L, Amir A (2016) Curr Biol 26:356-361, doi 10.1016/j.cub.2015.11.067 | `abstract` |
| Wallden M et al. (2016) Cell 166:729-739, doi 10.1016/j.cell.2016.06.052 | `abstract` |
| Si F et al. (2019) Curr Biol 29:1760-1770.e7, Mechanistic origin of cell-size control and homeostasis in bacteria, doi 10.1016/j.cub.2019.04.062, PMC6548602 | `full-text` |
| Facchetti G, Knapp B, Chang F, Howard M (2019) Biophys J 117:1728-1738, Reassessment of the basis of cell size control based on analysis of cell-to-cell variability, doi 10.1016/j.bpj.2019.09.031, PMC6838950 | `full-text` |
| Fantes PA (1977) J Cell Sci 24:51-67, Control of cell size and cycle time in Schizosaccharomyces pombe, doi 10.1242/jcs.24.1.51 | `abstract` |
| Di Talia S et al. (2007) Nature 448:947-951, doi 10.1038/nature06072 | `abstract` |


---

*Generated from [`library/laws/cell-size-adder.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/cell-size-adder.yaml). Do not edit this page; edit the YAML.*
