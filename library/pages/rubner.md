---
title: Rubner's surface law
label: law-rubner
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-rubner
B = c_h S, \qquad S \propto M^{2/3} \Rightarrow B \propto M^{2/3}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `B` | M*L^2/T^3 | W | resting metabolic rate |
| `S` | L^2 | m^2 | body surface area |
| `c_h` | M/T^3 | W/m^2 | heat flux per unit area |
| `M` | M | kg | body mass, entering through S proportional to M^(2/3) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `surface_exponent` | 0.6667 | DERIVED from geometry, not measured: for geometrically similar bodies at constant density, area scales as length squared and mass as length cubed, so S is proportional to M^(2/3). Everything in this law rests on that one step, which is why it fails exactly where geometric similarity or the heat-balance premise fails. |

## Why it holds

A homeotherm at rest in steady state must replace the heat it loses, and heat loss scales with surface area. Combined with geometric similarity this gives the two-thirds exponent. It is a genuine mechanism rather than a fit, and it is the oldest answer to the metabolic scaling question -- priority is usually given to Sarrus & Rameaux 1839 rather than to Rubner.

## Where it holds

- **taxa**: resting homeotherms
- **level**: Rubner's own data were dogs of different sizes, i.e. WITHIN one species
- **notes**: The intraspecific origin matters: the law was established on one species and is routinely applied across species, which is the level-pooling error Huxley allometry warns about.


:::{danger} Where it breaks
Ectotherms, plants and unicells do not thermoregulate metabolically, so the mechanism simply does not apply to them, and their measured exponents are not 2/3 -- unicells are super-linear at roughly 1 to 2. Bodies are also not geometrically similar: insulation, posture, appendages and shape all change with size, so the S proportional to M^(2/3) step is an idealisation rather than a measurement. Interspecifically the whole question is contested, and the dispute is not settled in Rubner's favour: Kleiber's re-analysis displaced 2/3 for decades, White & Seymour later argued for it again, and the best-sampled modern fit lands at 0.69 with a confidence interval excluding both 2/3 and 3/4. As a design check it returns no tolerance at all -- it gives an exponent and no scatter band -- so there is nothing a design can be said to pass or fail.
:::

## Worked examples

**a tenfold mass range**

```
surface rises by 10^(2/3) = 4.64x
mass-specific heat loss falls to 4.64/10 = 0.46x

```

- value: `0.46`

- The whole content of the law in one line: a larger homeotherm loses less heat per unit mass, so it needs less metabolism per unit mass. That direction is not in dispute; the exponent is.

- evidence: **derived**

:::{seealso} Contested
- Kleiber's law and the whole 2/3 versus 3/4 literature. See the kleiber entry, which holds the dispute; this entry holds the mechanism that motivates 2/3.
:::

## Sources

| Citation | Read-level |
|---|---|
| Rubner M (1883) Z Biol 19:535 | `remembered` |
| Sarrus and Rameaux (1839) Bull Acad R Med 3:1094 | `remembered` |


---

*Generated from [`library/laws/rubner.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/rubner.yaml). Do not edit this page; edit the YAML.*
