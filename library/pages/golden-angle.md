---
title: Phyllotaxis and the golden angle
label: law-golden-angle
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-golden-angle
\psi = 360^\circ\left(1 - \frac{1}{\varphi}\right) = \frac{360^\circ}{\varphi^2} = 180^\circ(3 - \sqrt{5}) = 137.5077640500^\circ
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `psi` | 1 | degrees | divergence angle between successive organs; angles are dimensionless, so the unit is a scale |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `golden_angle_deg` | 137.508 | EXACT, derived: 360*(1 - 1/phi) = 360/phi^2 = 180*(3 - sqrt(5)), with phi = (1 + sqrt(5))/2. Organs placed at this angle form parastichy spirals whose counts are consecutive Fibonacci numbers. This is a mathematical fact, not a measurement, which is why it carries no interval. |
| `sunflower_fibonacci_fraction` | 0.82 | Swinton, Ochu et al. 2016, a citizen-science study of 657 sunflower heads. Of 768 parastichy numbers evaluated, 565 were Fibonacci and a further 67 had a predefined Fibonacci-type structure: 632/768 = 82 per cent with Fibonacci structure. THE DENOMINATOR IS PARASTICHY NUMBERS, NOT FLOWER HEADS -- a confusion that is in circulation. |
| `sunflower_non_fibonacci_fraction` | 0.18 | 136/768 = 18 per cent did NOT have Fibonacci structure, splitting into Fibonacci minus one (49), Fibonacci plus one (17) and other (70). This is the tolerance of the check: nearly one in five counts is allowed off-sequence before a result is unlike real sunflowers. |
| `historical_fibonacci_fractions` | 0.82 (interval 0.82 to 0.95) | For comparison, Schoute reported 82 per cent and Weisse 95 per cent. Jean's often-quoted ~92 per cent of spiral species is remembered, not retrieved. |
| `arabidopsis_permutation_rate` | 0.5 | Refahi et al. 2016: organs are sometimes co-initiated in the meristem, leading randomly to post-meristematic organ-order permutations in AROUND HALF of the cases, measured against a perfect 137.5 degree spiral as reference. |

## Why it holds

Douady & Couder reproduce Fibonacci spirals as a self-organised growth process rather than a genetic instruction: each new primordium forms where the inhibitory fields of the existing ones are weakest, and the golden angle is the fixed point that packing dynamic converges on. The molecular implementation is auxin transport -- Reinhardt et al. 2003 show auxin accumulation occurs only at certain minimal distances from existing primordia, defining the position of future primordia. So the angle is an emergent consequence of local inhibition plus growth, which is why the same number appears in systems with no common ancestry.

## Where it holds

- **system**: spiral phyllotaxis in the shoot apical meristem
- **notes**: The angle is exact; what is empirical is how closely real organ series follow it and how often the parastichy counts come out Fibonacci.


:::{danger} Where it breaks
Nearly one sunflower parastichy count in five is NOT Fibonacci -- 136 of 768, split into Fibonacci minus one, Fibonacci plus one, and other -- so a design or simulation reproducing perfect Fibonacci counts every time is not matching sunflowers but exceeding them. In Arabidopsis the departure is mechanistic rather than statistical: organs are sometimes co-initiated, which randomly permutes post-meristematic organ order in about half of cases, so the observed ANGLE SEQUENCE can depart from 137.5 degrees even where the underlying spiral is perfect. Distichous (180 degree) and whorled phyllotaxis do not use the golden angle at all, so the law does not apply to a large fraction of plants rather than applying to them badly. And the number says nothing about what matters functionally -- light interception, packing density, vascular connection -- so matching it is necessary for a spiral array to look right and sufficient for nothing.
:::

## Worked examples

**the check a design or simulation can actually be held to**

```
successive organ angles modulo 360 should cluster at 137.5077640500 degrees
parastichy pairs should read (8,13), (13,21), (21,34), (34,55), ...
allow about 18 per cent of counts off-sequence before the result is unlike sunflowers

```

- value: `137.50776405`

- This is a rare case of a pattern law with both an exact target AND a measured tolerance, which is what makes it constraining. The tolerance is the valuable half: a simulation with 0 per cent non-Fibonacci counts fails the comparison just as a simulation with 50 per cent does.

- evidence: **derived**

:::{seealso} Contested
- Nothing contests the angle, which is a theorem. What varies between studies is the Fibonacci fraction: Schoute 82 per cent, Weisse 95 per cent, Swinton et al. 82 per cent on the largest and most recent sample. These are preserved side by side.
:::

## Sources

| Citation | Read-level |
|---|---|
| Douady S, Couder Y (1992) Phys Rev Lett 68:2098-2101, Phyllotaxis as a physical self-organized growth process, doi 10.1103/PhysRevLett.68.2098 | `metadata` |
| Douady S, Couder Y (1996) J Theor Biol 178:255-273, doi 10.1006/jtbi.1996.0024 | `metadata` |
| Reinhardt D et al. (2003) Nature 426:255-260, Regulation of phyllotaxis by polar auxin transport, doi 10.1038/nature02081 | `abstract` |
| Swinton J, Ochu E, MSI Turing's Sunflower Consortium (2016) R Soc Open Sci 3:160091, Novel Fibonacci and non-Fibonacci structure in the sunflower, doi 10.1098/rsos.160091, PMC4892450 | `full-text` |
| Refahi Y et al. (2016) eLife 5:e14093, doi 10.7554/eLife.14093, PMC4947393 | `full-text` |


---

*Generated from [`library/laws/golden-angle.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/golden-angle.yaml). Do not edit this page; edit the YAML.*
