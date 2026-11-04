---
title: Murray's law for branching transport networks
label: law-murray
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-murray
r_0^3 = \sum_i r_i^3
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `r_parent` | L | m | radius of the parent vessel |
| `r_child` | L | m | radius of each daughter vessel |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `exponent_theory` | 3 — *derived* | EXACT under the assumptions, not fitted. Minimising viscous dissipation (falling as r^-4, from Poiseuille) against the metabolic cost of maintaining blood volume (rising as r^2) gives flow proportional to r^3; conservation of flow at the junction then gives the cube law. Because the exponent descends from the r^-4 in Poiseuille, it is tied to LAMINAR flow and does not survive a change of flow regime. A corollary worth checking separately: wall shear stress tau = 4*mu*Q/(pi*r^3) is then the same in every segment. |
| `coronary_pooled` | 2.39 (interval 2.24 to 2.54) | MEASURED. Taylor et al. 2024, a meta-analysis of 18 studies, 1070 trees, 372 humans and 112 animals; I-squared = 99 per cent, so the heterogeneity between studies is near-total and the narrow CI describes the pooled estimate, not the spread of real trees. This is a flow-diameter exponent. |
| `coronary_stem_crown` | 2.62 (interval 1.97 to 3.27) | MEASURED, Huo & Kassab 2012: 2.62 +/- 0.65 against their theoretical 2.33 for whole stem-crown trees. NOTE that 2.33 is a flow-diameter exponent for whole trees and NOT a radius exponent at a single bifurcation; the paper never writes 7/3, and the attribution in circulation is wrong. |
| `coronary_volume_diameter` | 2.98 (interval 2.96 to 3) | MEASURED, Huo & Kassab 2012. The VOLUME-diameter exponent sits at 3 while the FLOW-diameter exponent for the same vessels sits near 2.4-2.6, so which exponent is quoted matters as much as its value. |
| `epicardial_bifurcations` | 2.6 (interval 1.96 to 3.24) | MEASURED, Zamir 1999 as tabulated by Taylor et al. 2024: 2.60 +/- 0.64. |
| `aortic_arch` | 2 | MEASURED, Zamir et al. 1992: the aortic arch branches follow a square law rather than the classical cube law. Area-preserving. |
| `lymphatic_capillaries` | 1.45 | MEASURED, dermal lymphatic capillaries, Front Cardiovasc Med 2022 (abstract). Far below 3. |
| `insect_tracheae` | unknown | The claim that insect tracheae follow n = 2 because transport there is diffusive rather than convective is widely repeated and NO SOURCE FOR IT WAS FOUND. No value is asserted. |

## Why it holds

Minimisation of the total of (a) the power dissipated by Poiseuille flow, which falls as r^-4, and (b) the metabolic cost of maintaining blood volume, which rises as r^2. Setting the derivative of the sum to zero gives flow proportional to r^3, and conservation of flow at a junction then gives the cube law. The exponent is a consequence of the r^-4 in Poiseuille, so it is tied to LAMINAR flow and does not survive a change of flow regime.

## Where it holds

- **flow regime**: laminar
- **reynolds max**: 2000
- **taxa**: ['mammalian vasculature', 'plant xylem', 'insect tracheae']
- **notes**: Small vessels, where viscous dissipation dominates and flow is steady.

:::{danger} Where it breaks
This field is the reason Murray's law cannot be applied blindly, and the failures are measured rather than theoretical. In LARGE ARTERIES the exponent falls toward 2, and the premise fails directly: Murray's law requires constant wall shear stress, and infrarenal aortic mean wall shear stress instead runs from 8.8 Pa in mice to 0.5 Pa in humans -- a seventeen-fold range across species, so the quantity assumed invariant is not. Reneman & Hoeks describe the arterial tree as running possibly from 2 in larger arteries to about 3 in arterioles, so the exponent is a function of position within one organism rather than a constant of it. TURBULENT OR UNSTEADY FLOW: Taylor et al. 2024 report that when turbulence, unsteadiness and blood rheology are accounted for, an exponent between 2.0 and 3.0 is retrieved; the specific turbulent value of 7/3 often attributed to Uylings 1977 is remembered and unverified. CONDUITS THAT ALSO BEAR LOAD: angiosperm xylem conforms as long as the conduits do not additionally serve as supports (McCulloh et al. 2003), and the law is REJECTED for conifer wood where hydraulic function is coupled to mechanical support (McCulloh et al. 2004) -- the clearest statement in this library that a part serving two functions obeys neither single-function optimum. SCALE WITHIN ONE STRUCTURE: Lepidoptera wing veins above roughly 50 micrometres conform and smaller ones conform less well, across more than 1000 wings of 667 species. And lymphatic capillaries sit near 1.45. A design claiming to be Murray-optimal must therefore state WHICH exponent it uses, for which vessels, and why.
:::

## Worked examples

**a symmetric bifurcation, 10 mm parent, under four exponents**

```
d_child = 10 * 2^(-1/n)
  n = 3    (theory)            : 2^-0.333 = 0.794 -> 7.94 mm
  n = 2.39 (coronary pooled)   : 2^-0.418 = 0.748 -> 7.48 mm
  n = 2    (aortic arch)       :                     7.07 mm  (area-preserving)
  n = 1.45 (lymphatic)         :                     6.19 mm
```

- value: `7.94`

- The exponents are DISTINGUISHABLE to within about 0.5 mm per branching at this scale, which is measurable. That is what makes this a real check rather than a slogan -- and also what makes quoting the wrong exponent a real error.

- evidence: **derived**

**human arterial tree**

- Exponent measured below 3 in the aorta and large arteries, consistent with the pulsatile-flow breakdown above rather than with a failure of the minimum-work argument itself. The argument is sound where its premises hold.

- evidence: **literature**

:::{seealso} Contested
- Generalisations (the Hess-Murray form r_p^n = sum(r_c^n) with n fitted) allow a non-cubic exponent for non-Poiseuille regimes. That is better read as a DIFFERENT LAW than as a correction to this one, because the cube exponent is derived and a fitted one is not.
- Hess's priority claim is remembered and its date is disputed between 1903 and 1914/1917 in secondary sources seen only as snippets, so no date is stated here.
- Leonardo's rule describes the MECHANICAL branches of a tree with an exponent near 2 while Murray's law describes the hydraulic conduits inside them with an exponent near 3. Two exponents coexist in one organism; see the leonardo entry.
:::

## Sources

| Citation | Read-level |
|---|---|
| Murray CD (1926) PNAS 12:207-214, The physiological principle of minimum work I: the vascular system and the cost of blood volume, doi 10.1073/pnas.12.3.207, PMC1084489 | `metadata` |
| Murray CD (1926) PNAS 12:299-304, ... II: oxygen exchange in capillaries, doi 10.1073/pnas.12.5.299 | `metadata` |
| Murray CD (1926) J Gen Physiol 9:835-841, ... applied to the angle of branching of arteries, doi 10.1085/jgp.9.6.835 | `metadata` |
| Taylor DJ et al. (2024) Am J Physiol Heart Circ Physiol 327:H182-H190, Systematic review and meta-analysis of Murray's law in the coronary arterial circulation, doi 10.1152/ajpheart.00142.2024, PMC11380967 | `full-text` |
| Huo Y, Kassab GS (2012) J R Soc Interface 9:190-200, Intraspecific scaling laws of vascular trees, doi 10.1098/rsif.2011.0270, PMC3223633 | `full-text` |
| Reneman RS, Hoeks AP (2008) Med Biol Eng Comput 46:499-507, doi 10.1007/s11517-008-0330-2, PMC2441533 | `full-text` |
| Schachat SR et al. (2021) BMC Biol, doi 10.1186/s12915-021-01130-0, PMC8444497 | `full-text` |
| Zamir M, Sinclair P, Wonnacott TH (1992) J Biomech 25:1303-1310, doi 10.1016/0021-9290(92)90285-9 | `abstract` |
| Kassab GS, Fung YC (1995) Ann Biomed Eng 23:13-20, doi 10.1007/BF02368296 | `abstract` |
| McCulloh KA, Sperry JS, Adler FR (2003) Nature 421:939-942, Water transport in plants obeys Murray's law, doi 10.1038/nature01444 | `abstract` |
| McCulloh KA, Sperry JS, Adler FR (2004) Funct Ecol 18:931-938, Murray's law and the hydraulic vs mechanical functioning of wood, doi 10.1111/j.0269-8463.2004.00913.x | `abstract` |
| Sherman TF (1981) J Gen Physiol 78:431-453, On connecting large vessels to small: the meaning of Murray's law, doi 10.1085/jgp.78.4.431, PMC2228620 | `abstract` |
| Talkington AM et al. (2022) Front Cardiovasc Med 9:840305, Dermal lymphatic capillaries do not obey Murray's law, doi 10.3389/fcvm.2022.840305 | `abstract` |
| Uylings HBM (1977) Bull Math Biol 39:509-520, Optimization of diameters and bifurcation angles in lung and vascular tree structures | `metadata` |


---

*Generated from [`library/laws/murray.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/murray.yaml). Do not edit this page; edit the YAML.*
