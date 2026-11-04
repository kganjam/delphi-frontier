---
title: Strouhal number and the 0.2-0.4 cruising band
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
| `f` | 1/T | Hz | tail-beat or wing-beat frequency |
| `A` | L | m | PEAK-TO-PEAK excursion of the tail tip or wingtip, not the semi-amplitude |
| `U` | L/T | m/s | forward speed |
| `St` | 1 | dimensionless | ratio of propulsor tip speed to forward speed |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `cruising_band` | 0.3 (interval 0.2 to 0.4) | The band within which cruising swimming and flying animals are observed to fall (Taylor, Nudds & Thomas 2003). It is a RANGE OBSERVED TO CONTAIN animals, motivated by foil experiments -- not a fitted value with an error bar. The paper reports no confidence interval that could be cited, and the species count, the fraction of species inside the band, and the operational definition of "cruising" were not retrieved. The listed value 0.3 is the midpoint and is a label for the band, not a measurement. |
| `odontocete_band` | 0.25 (interval 0.2 to 0.3) | Rohr & Fish 2004, 248 Strouhal values from six odontocete species. 74 per cent of values fall in 0.20-0.30, against 55 per cent in the 0.25-0.35 foil band, and 44 per cent in 0.225-0.275. Cetaceans run about 20 per cent below the foil prediction, so for whales and dolphins this is a sharper check than 0.2-0.4. |
| `foil_optimum` | 0.3 (interval 0.25 to 0.35) | Triantafyllou, Triantafyllou & Gopalkrishnan 1991, from oscillating foils rather than animals: thrust comes from a reverse von Karman street whose preferred Strouhal number lies in this range, and optimal foil efficiency is achieved within it. Eloy 2012 reports this band was obtained by fitting Koochesfahani's experiments. |
| `bird_cruise` | 0.21 (interval 0.21 to 0.25) | Nudds, Taylor & Thomas 2004, 60 bird species. Birds converge on the LOWER end of 0.2-0.4; 0.21 for direct fliers and 0.25 for intermittent fliers. |

## Why it holds

For a heaving and pitching foil, thrust efficiency peaks where the shedding frequency matches the most unstable frequency of the reverse Karman wake, which concentrates shed vorticity into a jet rather than spreading it (Triantafyllou et al. 1991, 1993). Taylor et al. 2003 argue that natural selection tunes cruising animals into that efficient band, which is why animals in different media and across six orders of magnitude in size converge on it. The mechanism is NOT settled: Usherwood 2025 argues that observed Strouhal numbers for cruising animals are too low for optimal mechanical efficiency. The observed band is more robust than the explanation for it.

## Where it holds

- **motion**: cruising -- steady, sustained, forward locomotion
- **propulsor**: oscillating lift-based propulsor (tail, fluke, wing)
- **reynolds min**: 1.0e4
- **taxa**: ['cetaceans', 'sharks', 'bony fish', 'birds', 'bats', 'insects']
- **notes**: Taylor et al. state the convergence holds only when cruising. The band is a property of lift-based oscillatory propulsion, not of animals as such, which is why foils share it.


:::{danger} Where it breaks
Small, low-Reynolds and elongate swimmers sit ABOVE the band, and the optimum is not a universal constant: from Eloy 2012, goldfish 0.54 (Re 7.1e3), bullfrog tadpole 0.79, West African lungfish 1.02 (Re 7.0e3), hagfish 0.56, longnose gar 0.59, European eel 0.48-0.52. Eloy's model predicts the trend, with the optimum rising from 0.15 to 0.8 from the largest cetaceans to the smallest tadpoles. Cetaceans sit low, 0.20-0.30, about 20 per cent under the foil band, so applying 0.2-0.4 to a dolphin is a loose check where a sharper one exists. Non-cruising flight -- take-off, manoeuvring, acceleration -- is outside the band by the source's own statement. Hovering breaks it definitionally: as U goes to zero, St goes to infinity, and Strouhal number is the wrong descriptor there. Finally the CONVENTION is a trap: some authors write St = 2fA/U with A the semi-amplitude. The number is the same, but mixing the convention with the wrong definition of A is a factor-of-2 error, and a design check that does not state "A = peak-to-peak" has not been performed.
:::

## Worked examples

**Tursiops truncatus (bottlenose dolphin)**

```
Eloy 2012 table: L = 2.58 m, Re = 1.2e7, St = 0.26, U/V = 0.52
U  = Re*nu/L = 1.2e7 * 1.0e-6 / 2.58 = 4.65 m/s   (assumes Eloy used nu = 1e-6; not verified)
fA = St*U    = 0.26 * 4.65            = 1.21 m/s
A  = 0.20*L  = 0.52 m                 (Rohr & Fish mid-range A/L; their range is 0.15-0.25)
f  = 1.21/0.52                        = 2.3 Hz

```

- value: `0.26`

- A consistency reconstruction, not a measured kinematic record. It shows the check is closed -- given any three of f, A, U and St the fourth follows -- which is what makes St usable.

- evidence: **derived**

**odontocete envelope from Rohr & Fish normalised ranges**

```
St = (f*L/U) * (A/L)
mid-range: 1.5 * 0.20 = 0.30
extremes:  1.0 * 0.15 = 0.15   to   2.0 * 0.25 = 0.50

```

- The measured ranges of the two factors ALONE permit values outside the observed 0.2-0.3 cluster. The clustering is therefore a real constraint on the animals and not an artefact of the ranges, which is the control that makes the band worth checking against.

- evidence: **derived**

**pigeon-sized bird, from the Nudds et al. 2004 retrieved formula**

```
inputs: b = 0.65 m span, U = 10 m/s, St = 0.21 (direct flier)
theta/2 = 33.5 * b^-0.24 = 33.5 * 1.109 = 37.1 deg
A = b*sin(37.1) = 0.65 * 0.604 = 0.393 m
f = 0.21*10/0.393 = 5.3 Hz

```

- value: `5.3`

- Pigeon cruising wingbeat frequencies of roughly 5-7 Hz are remembered, not retrieved, so this is a plausibility check only.

- evidence: **derived**

**Pollachius virens (saithe) and Oncorhynchus mykiss (rainbow trout)**

- value range: `[0.23, 0.26]`

- Saithe St 0.23 at L 0.364 m; rainbow trout St 0.26 at L 0.201 m (Eloy table, from Videler & Hess 1984).

- evidence: **literature**

:::{seealso} Contested
- Usherwood 2025: observed Strouhal numbers for cruising animals appear TOO LOW for optimal mechanical efficiency, so the efficiency-tuning mechanism is under discussion even though the band itself is robust.
- Eloy 2012: the optimum is not a constant but scales as St ~ 0.75*Li^(1/3) with a Lighthill number Li = (S/h^2)*C_d/2, rising from 0.15 to 0.8 across animal size. More than 85 per cent of data points lie in his acceptable range. This is better read as a different, size-dependent law than as a correction to the band.
- The convention St = 2fA/U with A the semi-amplitude (Usherwood 2025) coexists in the literature with St = fA/U with A peak-to-peak. Both are in use and the entry preserves both rather than picking one.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taylor GK, Nudds RL, Thomas ALR (2003) Nature 425:707-711, Flying and swimming animals cruise at a Strouhal number tuned for high power efficiency, doi 10.1038/nature02000 | `abstract` |
| Triantafyllou MS, Triantafyllou GS, Gopalkrishnan R (1991) Phys Fluids A 3:2835-2837, doi 10.1063/1.858173 | `abstract` |
| Triantafyllou GS, Triantafyllou MS, Grosenbaugh MA (1993) J Fluids Struct 7:205-224, doi 10.1006/jfls.1993.1012 | `metadata` |
| Rohr JJ, Fish FE (2004) J Exp Biol 207:1633-1642, Strouhal numbers and optimization of swimming by odontocete cetaceans, doi 10.1242/jeb.00948 | `abstract` |
| Nudds RL, Taylor GK, Thomas ALR (2004) Proc R Soc B 271:2071-2076, doi 10.1098/rspb.2004.2838 | `abstract` |
| Eloy C (2012) J Fluids Struct 30:205-218, Optimal Strouhal number for swimming animals, doi 10.1016/j.jfluidstructs.2012.02.008 | `full-text-preprint` |
| Usherwood JR (2025) J R Soc Interface 22:20240730, doi 10.1098/rsif.2024.0730 | `abstract` |
| Saadat M et al. (2017) Phys Rev Fluids 2:083102, On the rules for aquatic locomotion, doi 10.1103/PhysRevFluids.2.083102 | `metadata` |


---

*Generated from [`library/laws/strouhal.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/strouhal.yaml). Do not edit this page; edit the YAML.*
