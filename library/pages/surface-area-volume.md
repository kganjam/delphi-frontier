---
title: Surface-area-to-volume scaling and the diffusion limit on the size of an exchanging body
label: law-surface-area-volume
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-surface-area-volume
L_{\max} = \sqrt{\frac{G\, D\, C_s}{q}}, \qquad \frac{S}{V} \propto \frac{1}{L}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `L_max` | L | m | largest radius (sphere or cylinder) or half-thickness (slab) at which the centre still receives a non-zero concentration of the consumed substance |
| `G` | 1 | dimensionless | geometry factor: 6 for a sphere, 4 for an infinite cylinder, 2 for a slab supplied from both faces (L_max is then the half-thickness) |
| `D` | L^2/T | m^2/s | diffusion coefficient of the substance in the tissue or cytoplasm |
| `C_s` | N/L^3 | mol/m^3 | concentration just inside the surface. For a gas, D*C_s equals Krogh's permeation constant K times the surface partial pressure, so solubility is already inside K |
| `q` | N/(L^3*T) | mol/(m^3*s) | consumption rate per unit volume, assumed uniform and independent of concentration |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `geometry_factors` | 6 (sphere) | 4 (cylinder) | 2 (slab half-thickness) | EXACT under the assumptions, not fitted. They come from solving D * laplacian(C) = q with C = C_s at the surface and requiring C >= 0 at the centre. The sphere form, written with Krogh's constant, is the one Harvey (1928) used, citing Hill. The cylinder and slab factors are my own derivation from the same equation. I did not retrieve them from a source. |
| `isometric_exponent` | 0.6667 | Geometric. For shape held constant, S is proportional to V^(2/3), so S/V is proportional to V^(-1/3) and to 1/L. For a sphere, S/V = 3/r exactly. |
| `D_O2_water_25C` | 2e-09 (interval 1.8e-09 to 2.4e-09) m^2/s | REMEMBERED, not retrieved. NO SOURCE WAS RETRIEVED FOR THE INTERVAL. It is a guess at the spread over about 20-30 degrees C. In tissue and cytoplasm D is lower than in water. Krogh (1919) is the classical tissue source; I found only its metadata and could not read its values. Harvey (1928, full text) quotes Krogh's connective-tissue K as 1.15e-5 (cc O2 cm^-2 min^-1 per atm cm^-1). |
| `C_O2_airsat_water_20C` | 0.28 (interval 0.25 to 0.31) mol/m^3 | REMEMBERED (about 9 mg/L of fresh water at 20 degrees C). The interval is not sourced. Seawater holds about 20 per cent less, also remembered. This is the concentration in the external water. Using it for C_s assumes tissue solubility equals water solubility, which is an approximation. |
| `mammal_bmr_exponent` | 0.686 (interval 0.672 to 0.7) | MEASURED, White & Seymour 2005 (seen as a search summary): 0.686 +/- 0.014 for true BMR. White & Seymour 2003 (abstract): BMR is proportional to M^(2/3) across 619 species when body temperature, digestive state and phylogeny are accounted for. The 2/3 surface prediction and Kleiber's 3/4 are both still in use; see contested_by. |

## Why it holds

Exchange happens across a SURFACE, but demand comes from a VOLUME. If shape is held fixed, S/V falls as 1/L. A body that relies on diffusion through its outer surface therefore reaches a size at which supply across the surface can no longer match consumption inside it. For steady diffusion with uniform consumption q, the concentration at the centre of a sphere is C_s - q*r^2/(6D). Setting it to zero gives L_max. The same argument applies to heat: heat production scales with volume, heat loss with surface. This explains why small endotherms need high mass-specific metabolic rates and why the smallest endotherms are a few grams. That thermal consequence is remembered textbook reasoning. I did not compute it here.
The bound depends on the square root of D*C_s/q, so it is insensitive to errors. A factor-4 error in D moves L_max by a factor of 2.

## Where it holds

- **transport**: Diffusion alone. There is no internal convection (circulation, ventilation, cytoplasmic streaming) between the surface and the consuming tissue.
- **state**: Steady state. Consumption is uniform and independent of concentration (zero-order kinetics).
- **geometry**: The consuming material fills the body: a solid sphere, cylinder or slab.
- **scale**: From about 1 micrometre (single cells) to millimetres (diffusion-limited metazoans and embryos). Below about 1 micrometre, L_max is far larger than the body and the bound does not constrain anything.
- **notes**: The geometric statement S/V proportional to 1/L is exact for any fixed shape. Only the physiological consequence has a domain.

:::{danger} Where it breaks
The geometry never fails. Every failure comes from an assumption that stops holding, and each one below is a documented way out.
(1) CONVECTION REMOVES THE SIZE LIMIT. Once a circulation, a ventilation system or cytoplasmic streaming carries the substance inward, the diffusion distance is the distance from the nearest capillary, tracheole or stream. It is no longer the body radius. L_max then limits the spacing of capillaries or tracheoles (Krogh's cylinder), not the size of the organism. The constraint moves to the area of the exchanger (gill, lung, tracheal system), and that area does not scale isometrically. Applying L_max to whole bodies of any animal with a circulation is the commonest misuse of this law. Insects are a partial exception: their tracheae are blind-ended and the last stretch is diffusive. Harrison et al. 2010 (abstract) list developmental and evolutionary evidence that oxygen limits insect size. They also state that the fossil record cannot settle the historical link. Clapham & Karr 2012 (abstract) find maximum insect size tracked oxygen only until the end of the Jurassic. After that it decoupled, which they attribute to birds. See contested_by.
(2) SHAPE IS NOT CONSTANT. The law assumes isometry. Flattening to a slab (G = 2), stretching into a filament (G = 4), or folding the surface fixes the thickness and lets length and area grow without bound. A flat body has no diffusion limit on its area. I have not retrieved any measured thickness limit for flatworms, so none is asserted here.
(3) THE VOLUME IS NOT ALL CONSUMING. The giant sulfur bacteria break the "solid body" assumption. Thiomargarita namibiensis cells are spherical, exceed the biovolume of the largest previously known prokaryotes by up to 100-fold, and store nitrate at up to 800 mM in a central vacuole (Schulz et al. 1999, abstract). The largest specimens reach about 750 micrometres (Volland et al. 2022, abstract). Ca. Thiomargarita magnifica averages more than 9000 micrometres in length. The authors say it grows "orders of magnitude over theoretical limits for bacterial cell size", with more than half a million genome copies and DNA held in membrane-bound organelles (Volland et al. 2022, abstract). My inference, not the authors' claim: a central inert vacuole turns a sphere into a thin shell, so the operative L is the shell thickness, not the cell radius. The internal store also feeds the shell from inside, which breaks the single-surface-source assumption. Distributing genome copies throughout the cell shortens an internal diffusion distance that this law does not model. A size limit computed from cell radius is therefore wrong for these cells by orders of magnitude.
(4) THE SUBSTANCE IS NOT THE LIMITING ONE. The bound applies to whatever is being consumed. Epulopiscium spp. reach up to 0.6 mm and are strict anaerobes (Angert 2021, abstract), so an oxygen L_max says nothing about them. Any check must name which substance it uses.
(5) TRANSPORT COEFFICIENTS BORROWED ACROSS MATERIALS. Harvey (1928, full text) applied Krogh's connective-tissue K to luminous bacteria. His own measured oxygen threshold was far above his calculated one. He concluded that oxygen enters the bacterium much more slowly than through gelatin or connective tissue (abstract). He also cautioned in a footnote that the equation may not apply to an object as small as a bacterium. See worked_examples for the size of the gap. A K or D taken from another tissue can be wrong by two orders of magnitude.
(6) NON-STEADY OR CONCENTRATION-DEPENDENT CONSUMPTION. Oxygen stores, anaerobic metabolism during bursts, and Michaelis-Menten uptake at low concentration each break the steady, zero-order assumption. The bound then sets a limit on sustained aerobic rate, not on survival.
(7) THERMAL SCALING IS DOMINATED BY INSULATION, NOT S/V. Scholander (1955) and Irving argued that the size differences within Bergmann clines are too small to conserve meaningful heat, and that cold adaptation depends mainly on insulation. This argument is reported in Kendeigh 1969 and in Hagen 2016 (both seen as search summaries). I could not read Scholander 1955. For heat, S/V is one term among several, and fur, feathers or blubber can swamp it.
:::

## Worked examples

**a sphere of tissue consuming oxygen at the whole-body average rate of a resting human, in air-saturated fresh water**

```
q = 250 mL O2/min (STP, remembered resting value) / 0.0224 m^3/mol / 0.07 m^3 / 60 s
  = 2.66e-3 mol m^-3 s^-1
D = 2.0e-9 m^2/s, C_s = 0.28 mol/m^3 (both remembered; water values used for tissue)
  sphere   G=6: L_max = sqrt(6*2e-9*0.28/2.66e-3) = 1.12 mm (radius)
  cylinder G=4: 0.92 mm (radius)
  slab     G=2: 0.65 mm (half-thickness)
```

- value: `0.00112`

- CALCULATED, not observed. A body at resting-human tissue metabolic rate can be about 2 mm across without internal transport. At 100 times that rate, L_max falls by a factor of 10 to about 0.11 mm (also calculated). The sphere-to-slab difference is under a factor of 2, so shape matters much less than metabolic rate. The water values for D and C_s overstate L_max in real tissue.

- evidence: **derived**

**luminous bacteria (Harvey 1928), the test of the law on a bacterium**

```
Harvey's inputs (full text): A = 0.29 cc O2 per g per min, r = 5.5e-5 cm,
  K = 1.15e-5 (Krogh, connective tissue).
A*r^2/(5K) = 1.53e-5 atm  (Harvey's figure; his short-cylinder form)
A*r^2/(6K) = 1.27e-5 atm  (sphere form; my arithmetic)
Observed onset of dimming: about 0.0026 atm (Harvey)
Ratio observed / calculated = 0.0026 / 1.53e-5 = 170
```

- value: `170`

- The inputs and the observed threshold are Harvey's. The ratio of 170 is MY CALCULATION. Harvey went on to divide 1.53e-5 by the solubility of O2 in seawater (0.0255) to get 0.0006 atm, which is only about 4 times below his observation. MY INFERENCE: that division is dimensionally inconsistent. K is defined per atmosphere of partial-pressure gradient, so A*r^2/K is already a partial pressure in atm, and dividing by a solubility leaves it in the wrong units. The adversarial review on branch lawentry-surface-area-volume-review-sjvpjr (challenge 57) reached the same conclusion independently. So the borrowed-coefficient failure is about 170-fold on this reading, not 4-fold. Harvey's qualitative conclusion (slower diffusion into the bacterium) is unaffected.

- evidence: **derived**

**Thiomargarita namibiensis, 750 micrometre cell treated (wrongly) as a solid sphere**

```
q_max = 6*D*C_s/r^2 = 6*2e-9*0.28/(375e-6)^2 = 2.4e-2 mol m^-3 s^-1
  = about 9 times the resting-human tissue rate in example 1
```

- value: `0.024`

- CALCULATED, and an illustration of break (3), not a prediction. The cell is mostly vacuole, and its main electron acceptor is stored nitrate rather than external oxygen (Schulz et al. 1999, abstract). This number therefore answers the wrong question. The correct check would use the thickness of the cytoplasmic shell, which I did not retrieve, so no shell value is given.

- evidence: **derived**

:::{seealso} Contested
- METABOLIC SCALING EXPONENT. Rubner's surface law predicts metabolic rate proportional to M^(2/3). Kleiber (1932) established 3/4, which "remains in widespread use" (White & Seymour 2003, abstract). White & Seymour 2003 find 2/3 for mammalian BMR across 619 species once temperature, digestive state and phylogeny are accounted for, and "no support" for 3/4. Their 2005 follow-up gives 0.686 +/- 0.014 (search summary). This entry does not reconcile them. See the kleiber entry if present.
- OXYGEN AND INSECT SIZE. Harrison et al. 2010 (abstract) argue that tracheal oxygen delivery plausibly sets the small size of insects and enabled Palaeozoic gigantism. They state the historical link cannot be definitively accepted or rejected. Clapham & Karr 2012 (abstract, more than 10,500 fossil wing lengths) find size tracked oxygen only until the end of the Jurassic. After that, biotic interactions "superseded oxygen as the most important constraint." Both positions are recorded here.
- BERGMANN'S RULE AS A SURFACE-TO-VOLUME CONSEQUENCE. Meiri & Dayan 2003 report that over 72 per cent of bird species and 65 per cent of mammal species conform, and call the rule a valid generalization. Those figures come from a catalogue snippet, not the paper. Scholander 1955 and Irving argued that the size differences are too small to matter thermally and that insulation dominates (secondary sources only). Conformity to the pattern and the S/V mechanism are separate questions. The first does not establish the second.
:::

## Sources

| Citation | Read-level |
|---|---|
| Harvey EN (1928) J Gen Physiol 11:469-475, The oxygen consumption of luminous bacteria, doi 10.1085/jgp.11.5.469, PMC2141004 | `full-text` |
| Krogh A (1919) J Physiol 52:391-408, The rate of diffusion of gases through animal tissues, doi 10.1113/jphysiol.1919.sp001838 | `listing` |
| Schulz HN et al. (1999) Science 284:493-495, Dense populations of a giant sulfur bacterium in Namibian shelf sediments, doi 10.1126/science.284.5413.493 | `abstract` |
| Volland JM et al. (2022) Science 376:1453-1458, A centimeter-long bacterium with DNA contained in metabolically active membrane-bound organelles, doi 10.1126/science.abb3634 | `abstract` |
| Angert ER (2021) Genome Biol Evol 13:evab037, Challenges faced by highly polyploid bacteria with limits on DNA inheritance, doi 10.1093/gbe/evab037, PMC8245194 | `abstract` |
| Harrison JF, Kaiser A, VandenBrooks JM (2010) Proc R Soc B 277:1937-1946, Atmospheric oxygen level and the evolution of insect body size, doi 10.1098/rspb.2010.0001, PMC2880098 | `abstract` |
| Clapham ME, Karr JA (2012) PNAS 109:10927-10930, Environmental and biotic controls on the evolutionary history of insect body size, doi 10.1073/pnas.1204026109, PMC3390886 | `abstract` |
| White CR, Seymour RS (2003) PNAS 100:4046-4049, Mammalian basal metabolic rate is proportional to body mass^(2/3), doi 10.1073/pnas.0436428100, PMC153045 | `abstract` |
| White CR, Seymour RS (2005) J Exp Biol, allometric scaling of mammalian metabolism (exact title and pages not retrieved) | `search-summary` |
| Meiri S, Dayan T (2003) J Biogeogr 30:331-351, On the validity of Bergmann's rule, doi 10.1046/j.1365-2699.2003.00837.x | `search-summary` |
| Scholander PF (1955) Evolution 9:15-26, Evolutionary climatic adaptation in homeotherms | `search-summary` |


---

*Generated from [`library/laws/surface-area-volume.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/surface-area-volume.yaml). Do not edit this page; edit the YAML.*
