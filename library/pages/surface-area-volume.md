---
title: The surface-area-to-volume constraint on passive exchange, and the size at which an unventilated body runs out of supply
label: law-surface-area-volume
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-surface-area-volume
\frac{A}{V} = \frac{\phi}{L} \;\Rightarrow\; q\,V \le j_{\max} A \iff L \le L_{\max} = \frac{\phi\, j_{\max}}{q}, \qquad r_{\max}^{\mathrm{diff}} = \sqrt{\frac{6\, D\, C_s}{q}}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `L_max` | L | m | largest characteristic length (radius, for a sphere with phi = 3) at which surface supply can still meet volume demand |
| `L` | L | m | characteristic length of the body; the same length phi is defined against |
| `phi` | 1 | dimensionless | shape factor A*L/V; exactly 3 for a sphere with L = radius, 6 for a cube with L = side, 2 for a long cylinder with L = radius (ends neglected) |
| `A` | L^2 | m^2 | area of the exchanging surface |
| `V` | L^3 | m^3 | volume of the consuming tissue |
| `j_max` | N/(L^2*T) | mol/(m^2*s) | maximum flux the surface can pass per unit area (for a membrane, permeability times the concentration difference across it) |
| `q` | N/(L^3*T) | mol/(m^3*s) | volume-specific consumption (or production) rate of the exchanged substance, assumed uniform and independent of concentration |
| `D` | L^2/T | m^2/s | diffusion coefficient of the substance in the tissue; D*C_s equals Krogh's diffusion constant K times the surface partial pressure |
| `C_s` | N/L^3 | mol/m^3 | concentration held at the body surface by the environment |
| `r_max` | L | m | internal-diffusion limit on sphere radius (the r_max^diff term in the latex) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `shape_factor_sphere` | 3 dimensionless | Geometry (A = 4 pi r^2 and V = 4/3 pi r^3), not a measurement. |
| `surface_area_exponent_geometric` | 0.6667 dimensionless | A proportional to V^(2/3) under geometric similarity. Okie (2013, abstract read) calls this the "zeroth-order geometric expectation" and states that organisms depart from it in both directions, "from exponents of less than two-thirds to superlinear scaling". It is a derived value; the measured exponents below are where it is tested. |
| `sphere_diffusion_coefficient_6` | 6 dimensionless | Sphere with zero-order uptake (Harvey 1928, full text read). Long cylinder 4; short cylinder ~5, which is the value Harvey actually used for his rod-shaped bacterium. |
| `krogh_K_connective_tissue` | 1.15e-05 cm^3 O2 / (cm * min * atm) | Krogh's (1919) diffusion constant for oxygen in connective tissue, AS QUOTED BY HARVEY (1928); we did not read Krogh 1919 (bibliographic record only). Harvey defines it as cc O2 diffusing per sq. cm per minute for a gradient of one atmosphere per cm. Harvey also quotes Krogh that diffusion through chitin is about 9 times slower. No interval in the text read. |
| `harvey_bacterial_O2_consumption` | 0.29 cm^3 O2 / (g * min) | OBSERVATION (Harvey 1928): 0.291 cc O2 per gram per minute for a luminous bacterium at ~21 C, assuming density 1. The underlying per-cell rate from his 1925 dimming experiments ranged 6.65 to 17.67 x 10^-15 mg O2 per bacterium per second over seven experiments at 18-23 C (mean 11.84 x 10^-15), which Harvey then says are 10 per cent too low. The 1928 respirometer and dimming methods agreed (6.95 vs 6.93 x 10^-6 cc O2 per cc of emulsion per second). We record the range as reported and do not convert it to an interval on 0.29 because the temperatures differ. |
| `harvey_bacterial_O2_flux_per_area` | 5.6 mg O2 / (m^2 * h) | Harvey reports "5.6 mg. O2 per sq. m. of bacterial surface" without a time base in the readable text (the table did not survive OCR). The PER-HOUR time base is OUR INFERENCE: 11.84e-15 mg/s x 3600 s = 4.26e-11 mg, which is his per-bacterium figure, and 4.26e-11 mg / 7.6 um^2 = 5.6 mg/m^2. |
| `O2_solubility_seawater_21C` | 0.0052 cm^3 O2 (NTP) / cm^3 seawater, air-equilibrated | Harvey (1928), citing Fox (1909); we did not read Fox. Harvey gives 0.0255 for pure O2 at 20 C. |
| `mammal_pulmonary_diffusing_capacity_exponent` | 0.99 dimensionless | OBSERVATION, Gehr et al. (1981, abstract read): morphometric DLO2 proportional to Mb^0.99 in African wild and domestic mammals 0.4-240 kg (21 individuals with paired VO2max), against VO2max proportional to Mb^0.79, so DLO2/VO2max ~ Mb^0.20. Confidence intervals are not in the abstract. A search-summary noted that a hosted PDF of the same paper describes 27 animals from 15 species; we could not open it (host outside the session's network allowlist) and so cannot reconcile the two counts. |
| `mammal_VO2max_exponent` | 0.79 dimensionless | Gehr et al. (1981, abstract read), same sample as above. |

## Why it holds

For a family of bodies of the same shape, area grows as L^2 and volume as L^3, so A/V = phi/L falls as 1/L. Any process whose demand is set by volume (respiration, heat production, waste production) and whose supply must cross a surface (gas, nutrient, heat loss) therefore has a size above which supply per unit volume falls below demand. With no internal convection the supply also has to diffuse inward, and diffusion time grows as L^2/D, so the internal limit r = sqrt(6 D C_s / q) is reached before the surface limit unless the surface itself is the main resistance. Every escape from the constraint works by breaking one of its two assumptions -- geometric similarity (flatten, elongate, fold, hollow, internalise surface) or diffusion-only transport (add convection) -- and these are the classes Okie (2013) models.

## Where it holds

- **transport**: diffusion only: no circulation, ventilation, cytoplasmic streaming or external stirring that is not captured in C_s
- **geometry**: geometrically similar bodies; phi must be computed for the actual shape, not assumed
- **kinetics**: consumption uniform through the volume and independent of concentration (zero-order) down to zero
- **boundary**: C_s is the concentration actually at the surface; an unstirred external boundary layer lowers it below bulk
- **taxa**: single cells, eggs and embryos before circulation, sponges and other thin organisms, cell aggregates and unperfused engineered tissue
- **notes**: The geometry (A/V = phi/L) holds universally. The exchange CONSTRAINT built on it holds only inside the box above, and the number it yields is no better than q and D, which are each uncertain by a factor that Harvey's own test (worked example 1) puts at about 4 for D in a bacterium.


:::{danger} Where it breaks
(1) WHEREVER THERE IS CONVECTION. Once a body has a circulation or ventilates an internal exchanger, its outer A/V no longer limits supply; the limit moves to the area of the internal exchanger and to the transport network feeding it. Mammals show this directly: Gehr et al. (1981) measured lung diffusing capacity scaling as Mb^0.99, not the Mb^0.67 that external geometry would give, i.e. large mammals build exchange surface roughly in proportion to mass. Applying the external A/V law to a vascularised animal gives a wrong answer by construction. (2) WHEREVER THE SHAPE IS NOT SIMILAR. Giant sulfur bacteria exceed any sphere-diffusion limit set on their outer radius: Thiomargarita namibiensis cells reach up to ~750 um across (Schulz et al. 1999; size from secondary sources), and Ca. Thiomargarita magnifica has an average cell length above 9000 um, which the authors state is "orders of magnitude over theoretical limits for bacterial cell size" (Volland et al. 2022, abstract). A secondary source reports the T. namibiensis cytoplasm as a 0.5-2 um shell around a vacuole that fills ~98% of the volume; if so, the diffusion length is the shell thickness, not the radius -- that is our inference from the secondary figure, not a measurement we read. Okie (2013) reports from compiled data that large eukaryotic phytoplankton reach near-linear (not 2/3) effective surface scaling by hollowness and internalised surfaces. (3) AT THE SCALE OF A BACTERIUM, THE TRANSPORT COEFFICIENT IS NOT THE TISSUE ONE. Harvey (1928) computed, with Krogh's connective-tissue D, that 0.0006 atm O2 should sustain a luminous bacterium, but observed dimming at ~0.0026 atm -- about 4 times higher. He concluded that the only unmeasured input, D, is too high for the cell, plausibly because of the envelope. That is a demonstrated failure of the law with borrowed coefficients at micrometre scale; the law is only as good as a measured q and D for the actual body. Harvey also flags that zero-order kinetics down to zero concentration is "questionable" for an object as small as a bacterium. (4) AS AN EXPLANATION OF WHOLE-ANIMAL SIZE LIMITS, IT IS CONTESTED rather than demonstrated -- see contested_by for insect gigantism and atmospheric oxygen. Heat exchange obeys the same geometry but is out of scope of this entry; we did not source it.
:::

## Worked examples

**luminous bacterium (Harvey 1928), rod 2.2 um x 1.1 um**

```
C_o = A r^2 / (5 D) = 0.29 * (5.5e-5 cm)^2 / (5 * 1.15e-5) = 1.53e-5 atm; / 0.0255 (O2 solubility in seawater) = 6.0e-4 atm
```

- value: `0.0006`

- Harvey's calculation, which we reproduced (1.526e-5 atm before the solubility step; the 6 D sphere form gives 1.27e-5). Harvey then compares it with his OBSERVED dimming threshold of ~0.0026 atm, about 4x higher, and infers a lower D in the bacterium. The calculation is literature; the comparison is between a calculated and an observed value, and the "envelope" explanation is Harvey's inference, not a measurement. Harvey's cell: area 7.6 um^2, volume 1.695 um^3, giving A/V = 4.5 per um (our arithmetic).

- evidence: **literature (calculation and observation), reproduced**

**an aerobic sphere respiring at Harvey's bacterial rate with connective-tissue diffusivity, surface held at air saturation**

```
r_max = sqrt(6 K P_s / A) = sqrt(6 * 1.15e-5 * 0.21 / 0.29) cm = 7.07e-3 cm
```

- value: `7.1e-05`

- CALCULATED, not observed: r_max ~ 71 um (value in metres). Uses K*P_s in place of D*C_s (the two are equal by definition of Krogh's constant), P_s = 0.21 atm assumes no external boundary layer, and q = Harvey's bacterial rate, which is high for most tissues -- r_max scales as q^-1/2, so a tissue respiring 100x slower would reach ~10x larger. If Harvey's inferred ~4x lower effective D applied, r_max would be ~35 um (also calculated). We did not find a sourced tissue q to substitute, so no tissue-specific number is given. The intended design use is a check on unperfused cell aggregates or constructs; we have not sourced an observed necrotic-core radius to test it against.

- evidence: **derived**

**African wild and domestic mammals, 0.4-240 kg**

- value: `DLO2 ~ Mb^0.99; VO2max ~ Mb^0.79`

- OBSERVATION (Gehr et al. 1981, abstract). The internal exchanger escapes the 2/3 geometry. The authors conclude that "large animals require a larger pulmonary diffusing capacity to transfer oxygen at the same rate from air to blood".

- evidence: **literature**

**Thiomargarita namibiensis; Ca. Thiomargarita magnifica**

- value range: `[750, 9000]`

- Micrometres; maximum cell diameter of T. namibiensis (secondary sources, ~750 um) and average cell length of T. magnifica (>9000 um, Volland et al. 2022 abstract). No direct comparison with the 71 um figure above is valid: we found no measured q for either organism, and T. namibiensis oxidises sulfide with nitrate stored at up to 800 mM in its vacuole (Schulz et al. 1999 abstract), so the O2-diffusion calculation does not describe its supply. Recorded as a shape-escape counterexample, not as a test of the number.

- evidence: **literature**

:::{seealso} Contested
- Insect gigantism and oxygen. Harrison, Kaiser & VandenBrooks (2010, abstract) argue that tracheal oxygen delivery plausibly sets the small size of insects and enabled Palaeozoic gigantism under hyperoxia, while stating that the fossil record makes it "impossible to definitively accept or reject the historical oxygen-size link". Clapham & Karr (2012, abstract), from >10,500 fossil wing lengths, report that maximum size tracked pO2 only until the end of the Jurassic and then decoupled from it, and argue that biotic interactions (birds, later bats) superseded oxygen as the main constraint. Not reconciled here.

- Whether the 2/3 surface geometry explains the scaling of metabolic rate (Rubner's surface law) is the 2/3-vs-3/4 dispute recorded in the Kleiber entry; this entry takes no side.

:::

## Sources

| Citation | Read-level |
|---|---|
| Harvey EN (1928) The oxygen consumption of luminous bacteria. J Gen Physiol 11(5):469-475. doi:10.1085/jgp.11.5.469 (PMC2141004) | `full-text` |
| Krogh A (1919) The rate of diffusion of gases through animal tissues, with some remarks on the coefficient of invasion. J Physiol 52(6):391-408. doi:10.1113/jphysiol.1919.sp001838 | `listing` |
| Okie JG (2013) General models for the spectra of surface area scaling strategies of cells and organisms: fractality, geometric dissimilitude, and internalization. Am Nat 181(3):421-439. doi:10.1086/669150 | `abstract` |
| Gehr P, Mwangi DK, Ammann A, Maloiy GM, Taylor CR, Weibel ER (1981) Design of the mammalian respiratory system. V. Scaling morphometric pulmonary diffusing capacity to body mass: wild and domestic mammals. Respir Physiol 44:61-86. doi:10.1016/0034-5687(81)90077-3 | `abstract` |
| Schulz HN, Brinkhoff T, Ferdelman TG, Marine MH, Teske A, Jorgensen BB (1999) Dense populations of a giant sulfur bacterium in Namibian shelf sediments. Science 284(5413):493-495. doi:10.1126/science.284.5413.493 | `abstract` |
| BioNumbers entry for Thiomargarita namibiensis cell size and vacuole fraction (bionumbers.hms.harvard.edu, id 102207) | `search-summary` |
| Volland JM et al. (2022) A centimeter-long bacterium with DNA contained in metabolically active, membrane-bound organelles. Science 376(6600):1453-1458. doi:10.1126/science.abb3634 | `abstract` |
| Harrison JF, Kaiser A, VandenBrooks JM (2010) Atmospheric oxygen level and the evolution of insect body size. Proc R Soc B 277:1937-1946. doi:10.1098/rspb.2010.0001 | `abstract` |
| Clapham ME, Karr JA (2012) Environmental and biotic controls on the evolutionary history of insect body size. PNAS 109:10927-10930. doi:10.1073/pnas.1204026109 | `abstract` |


---

*Generated from [`library/laws/surface-area-volume.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/surface-area-volume.yaml). Do not edit this page; edit the YAML.*
