---
title: Wolff's law, Frost's mechanostat and dynamic strain similarity
label: law-bone-strain
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-bone-strain
\varepsilon = \frac{\sigma}{E}; \qquad \varepsilon < 100\text{--}300\,\mu\varepsilon:\ \text{loss}; \quad \varepsilon > 1500\text{--}3000\,\mu\varepsilon:\ \text{gain}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `epsilon` | 1 | microstrain (1e-6) | peak working strain -- the quantity the thresholds are stated in |
| `sigma` | M/(L*T^2) | Pa | peak working stress in the element |
| `E` | M/(L*T^2) | Pa | Young's modulus of the bone |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `modelling_threshold_microstrain` | 2250 (interval 1500 to 3000) | Frost 1987 (Anat Rec), quoted: strains in or above the 1500-3000 microstrain range cause bone MODELLING to increase cortical bone mass. The listed 2250 is the band midpoint, a label rather than a measurement. |
| `disuse_threshold_microstrain` | 200 (interval 100 to 300) | Frost 1987, same sentence: strains below the 100-300 microstrain range release BMU-based remodelling, which then removes bone. Between the two bands is maintenance. |
| `peak_strain_across_species_microstrain` | 2500 (interval 2000 to 3000) | Peak strains of 2000-3000 microstrain for all animals, from a 2014 Life review read at full text as a SECONDARY source. This is the observed envelope, and note that it straddles Frost's modelling threshold -- normal locomotion sits at or just above the strain that adds bone. |
| `dynamic_strain_similarity_g` | 2.8 (interval 0.8 to 6.9) | Rubin & Lanyon 1984: axial force falls from 6.9 G in a 7 kg turkey to 2.8 G in a 130 kg horse to 0.8 G in a 2500 kg elephant, while peak STRESSES stayed remarkably similar across a 350-fold mass range. The interval here is the measured range of the G figures, not an uncertainty. |
| `loading_cycles_saturation` | 36 | Rubin & Lanyon, J Bone Joint Surg: 36 loading cycles per day at 0.5 Hz raised bone mineral content to 133 and 143 per cent, and MORE cycles, up to 1800, gave no further gain. The dose saturates almost immediately, which is the most design-relevant fact in the entry. The species (turkey ulna) is remembered; the retrieved abstract excerpt did not name it. |
| `microdamage_threshold_microstrain` | unknown | A ~3000 microstrain microdamage threshold is widely attributed to Frost. IT IS NOT IN THE RETRIEVED ABSTRACT and no value is asserted here. The values 50-200 also in circulation are likewise not in it. |

## Why it holds

Osteocytes sense strain and the fluid flow it drives through the lacuno-canalicular network, and the cell populations that add and remove bone respond to that signal, so the tissue converges on a strain set-point rather than on a shape. Frost's mechanostat is the thermostat analogy made quantitative: two thresholds with a maintenance band between them. The mechanistic detail below the cell level is outside this catalogue.

## Where it holds

- **quantity**: peak dynamic strain, not static strain and not stress
- **taxa**: vertebrate cortical bone; the strain-similarity measurements span 7 kg to 2500 kg
- **notes**: The equation given is the bridge a designer needs: it converts a predicted working stress into the strain the thresholds are stated in. The thresholds themselves are the law.


:::{danger} Where it breaks
Wolff's law as originally stated has NO equation at all -- it says bone adapts to load, which is not checkable, and Bertram & Swartz 1991 titled their critique "The 'law of bone transformation': a case of crying Wolff?". Only Frost's bands make anything testable, and those bands move with hormones, age and skeletal site, which is Frost's own point about nonmechanical agents; a single pair of thresholds is therefore a species- and state-averaged summary rather than a constant. The strain-similarity result is a summary across sites and species measured with gauges at ACCESSIBLE locations, so it is biased toward superficial cortical bone on limb elements. The dose-response saturating at 36 cycles means the law constrains strain MAGNITUDE and says almost nothing about duration or total load, so a design cannot trade one for the other. And the thresholds describe living, remodelling tissue: they are not failure criteria, so a structure at 3500 microstrain is outside the observed envelope but has not been shown to break -- confusing the adaptation threshold with a strength limit is the standard misuse.
:::

## Worked examples

**a structural element at two predicted working strains**

```
400 microstrain  : inside the 100-300 to 1500-3000 maintenance band -> living bone would
                   neither add nor remove mass
3500 microstrain : above the modelling threshold AND above the 2000-3000 observed peak
                   envelope -> outside the range any measured animal operates in

```

- value: `3500`

- The check is a band test, not a number test, and its output is "inside / adds / removes / outside the observed envelope" rather than a safety factor.

- evidence: **derived**

**converting a stress to a strain for the check**

```
sigma = 60 MPa, E = 20 GPa  ->  epsilon = 60e6/20e9 = 3.0e-3 = 3000 microstrain
```

- value: `3000`

- Both inputs are illustrative round numbers and are NOT measured values for any species; the arithmetic is shown so the conversion is reusable. At the top of both Frost's modelling band and the observed envelope.

- evidence: **derived**

:::{seealso} Contested
- Bertram & Swartz 1991 argue the law of bone transformation is not a predictive law. Only the title was retrieved; the content of the argument is relayed from memory and should be read before being leaned on.
- The ~3000 microstrain microdamage threshold and the 50-200 microstrain disuse figures are in circulation and are NOT in the retrieved Frost abstract. They are recorded here as unsupported rather than silently omitted.
:::

## Sources

| Citation | Read-level |
|---|---|
| Wolff J (1892) Das Gesetz der Transformation der Knochen, Hirschwald, Berlin | `metadata` |
| Frost HM (1987) Anat Rec 219:1-9, Bone mass and the mechanostat: a proposal, doi 10.1002/ar.1092190104 | `abstract` |
| Frost HM (1987) Bone Miner 2:73-85, The mechanostat: a proposed pathogenic mechanism of osteoporoses, PMID 3333019 | `metadata` |
| Rubin CT, Lanyon LE (1984) J Theor Biol 107:321-327, Dynamic strain similarity in vertebrates, doi 10.1016/S0022-5193(84)80031-4 | `abstract` |
| Rubin CT, Lanyon LE (1984) J Bone Joint Surg Am 66:397-402, doi 10.2106/00004623-198466030-00012 | `abstract` |
| Bertram JEA, Swartz SM (1991) Biol Rev 66:245-273, doi 10.1111/j.1469-185X.1991.tb01142.x | `metadata` |
| Life (2014) review, PMC4187165, for the 2000-3000 microstrain cross-species envelope | `full-text` |


---

*Generated from [`library/laws/bone-strain.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/bone-strain.yaml). Do not edit this page; edit the YAML.*
