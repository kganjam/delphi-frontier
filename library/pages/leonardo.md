---
title: Leonardo's rule for branch diameters, and fractal dimension
label: law-leonardo
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-leonardo
d^{\Delta} = \sum_i d_i^{\Delta} \Longleftrightarrow \sum_i \left(\frac{d_i}{d}\right)^{\Delta} = 1
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `d_parent` | L | m | parent branch diameter |
| `d_child` | L | m | each daughter branch diameter |
| `Delta` | 1 | dimensionless | the Leonardo exponent, fitted rather than derived |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `leonardo_exponent` | 2 (interval 1.8 to 2.3) | Eloy 2011: the available data indicate the Leonardo exponent lies in 1.8 < Delta < 2.3 for a large number of species. Delta = 2 means cross-sectional AREA is preserved at a branching. Compare Murray's Delta = 3, which is derived rather than fitted and describes the hydraulic conduits INSIDE the same tree. |
| `eloy_model_range` | 2.07 (interval 1.93 to 2.21) | Eloy's wind-stress model gives 1.93 < Delta < 2.21 when the fractal dimension D lies in 2 < D < 3. The model range sits inside the measured range, which is the agreement the paper claims. |
| `fractal_dimension_measured_on_trees` | unknown | Eloy notes that the fractal dimension D HAS NEVER BEEN MEASURED DIRECTLY ON REAL TREES. The model's input is therefore unmeasured, so its agreement with the Delta data is weaker evidence than it looks. |
| `coral_fractal_dimension` | unknown | Values of 1.1-1.5 for coral outlines are widely quoted from Martin-Garin et al. 2007. The paper was blocked and the numbers are REMEMBERED; no coral D is asserted here as retrieved. |

## Why it holds

Two accounts, and they predict nearly the same exponent for different reasons. Eloy 2011 derives the rule from mechanics: a self-similar tree designed so that every branch has the same probability of breaking in WIND satisfies Leonardo's rule. Earlier accounts appeal to area-preservation for sap transport, which gives Delta = 2 directly but conflicts with the Murray exponent measured for the conduits themselves. The entry is written in the normalised form -- the sum of child-to-parent diameter ratios raised to Delta equals one -- because with a FITTED exponent the raw form d^Delta has a dimension that changes with Delta, and only the normalised form is dimensionally clean for every value. The same device is used in the Huxley allometry entry, and for the same reason.

## Where it holds

- **system**: woody tree branching -- the structural branches, not the vascular conduits
- **notes**: TWO EXPONENTS COEXIST IN ONE ORGANISM, one mechanical and one hydraulic, and they are different laws rather than competing estimates of one number. Leonardo's Delta near 2 describes the branches; Murray's exponent near 3 describes the xylem inside them, where it is not also bearing load.


:::{danger} Where it breaks
Delta varies with species and with the branching geometry itself: Minamino & Tateno 2014 found biomechanical models deviating from da Vinci's rule as the weights and branching angles of lateral daughter branches increased, though the deviation was small for branching patterns found in nature. Fagus crenata fitted a uniform-stress model best while Abies homolepis often agreed with da Vinci's rule, and neither paper reports a Delta, so the fitted range above rests on Eloy alone. The fractal half of the entry breaks harder and is the reason this law is only LOOSELY constraining. Self-similarity holds over a finite scale range: Nelson, West & Goldberger state that the finite nature of the lung ultimately limits the range over which self-similarity applies, and the general claim that natural fractals span only one to two decades (Avnir et al. 1998) is at metadata level here. A box-counting dimension measured over one decade cannot exclude a design, it describes texture, and for the one group this project might care about -- corals -- no value was retrievable at all. Treat Delta in 1.8-2.3 as a usable loose check on MECHANICAL branching, and treat fractal dimension as descriptive.
:::

## Worked examples

**a 10 cm branch splitting into two equal daughters**

```
d_child = 10 * 2^(-1/Delta)
  Delta = 1.8          : 6.80 cm
  Delta = 2.0          : 7.07 cm   (area-preserving)
  Delta = 2.3          : 7.40 cm
  Delta = 3 (Murray)   : 7.94 cm

```

- value: `7.07`

- The 0.6 cm gap between Delta = 2.3 and Murray's value is measurable with a tape, which is exactly what makes Leonardo's rule and Murray's law DISTINGUISHABLE in data rather than two names for one observation. A design claiming either must say which and why.

- evidence: **derived**

:::{seealso} Contested
- Eloy 2011 (wind-induced stress) against the older sap-transport area-preservation argument. Both predict Delta near 2, so the exponent does not discriminate between them; Eloy's model additionally predicts the dependence on fractal dimension, which has never been measured on real trees.
- Minamino & Tateno 2014 find uniform-stress models fitting better than da Vinci's rule in Fagus crenata, with the reverse in Abies homolepis. Recorded rather than reconciled.
:::

## Sources

| Citation | Read-level |
|---|---|
| Eloy C (2011) Phys Rev Lett 107:258101, Leonardo's rule, self-similarity, and wind-induced stresses in trees, doi 10.1103/PhysRevLett.107.258101 | `full-text-preprint` |
| Minamino R, Tateno M (2014) PLoS ONE 9:e93535, Tree branching: Leonardo da Vinci's rule versus biomechanical models, doi 10.1371/journal.pone.0093535, PMC3979699 | `full-text` |
| Nelson TR, West BJ, Goldberger AL (1990) Experientia 46:251-254, The fractal lung, doi 10.1007/BF01951755 | `abstract` |
| Avnir D, Biham O, Lidar D, Malcai O (1998) Science 279:39-40, Is the geometry of nature fractal?, doi 10.1126/science.279.5347.39 | `metadata` |
| Martin-Garin B et al. (2007) Coral Reefs 26:541-550, Use of fractal dimensions to quantify coral shape, doi 10.1007/s00338-007-0256-4 | `metadata` |
| West GB, Brown JH, Enquist BJ (1999) Science 284:1677-1679, The fourth dimension of life, doi 10.1126/science.284.5420.1677 | `metadata` |


---

*Generated from [`library/laws/leonardo.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/leonardo.yaml). Do not edit this page; edit the YAML.*
