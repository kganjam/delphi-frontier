---
title: Wolff's law of bone remodelling (bone adapts its mass and architecture to the loads it carries)
label: law-wolff
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-wolff
\frac{d\rho}{dt} = B\,S_{\mathrm{exc}}, \quad S_{\mathrm{exc}} = \begin{cases} S-(1+s)k & S>(1+s)k \\ 0 & (1-s)k \le S \le (1+s)k \\ S-(1-s)k & S<(1-s)k \end{cases}, \quad S = \frac{U}{\rho}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `drho_dt` | M/(L^3*T) | kg/(m^3*s) | rate of change of apparent bone density at a point |
| `B` | M*T/L^5 | kg*s/m^5 | remodelling rate coefficient; fitted, not measured (see constants) |
| `S_excess` | L^2/T^2 | J/kg | stimulus in excess of the lazy-zone bound; zero inside the lazy zone |
| `S` | L^2/T^2 | J/kg | mechanical stimulus: strain energy density per unit bone mass (U / rho) |
| `U` | M/(L*T^2) | J/m^3 | strain energy density from a finite-element or strain-gauge estimate |
| `rho` | M/L^3 | kg/m^3 | apparent density of the bone at that point |
| `k` | L^2/T^2 | J/kg | reference (homeostatic) stimulus; site-specific |
| `s` | 1 | dimensionless | half-width of the lazy zone as a fraction of k |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `reference_stimulus_k` | unknown J/kg | No universal value exists. In the Huiskes-type rule k is the "reference SED at the same location" (secondary-source description, search-summary): it is set from the intact, pre-intervention bone at that site. The model therefore fixes its reference to the state whose change it then predicts. A 2019 study in a different SED model (Sci Rep, doi 10.1038/s41598-019-51429-w, search-summary) used reference values of 0.002 to 0.014 J/g and found the converged mean density depends on that choice. That range belongs to that model and is NOT a measured constant of bone. |
| `lazy_zone_half_width_s` | unknown dimensionless | Searched for the value used by Huiskes et al. (1987) and Weinans et al. (1992); not found in any abstract or summary read in this session. The same 2019 study (search-summary) reports the equilibrium-zone width did not much change the converged mean density. Not invented here. |
| `rate_coefficient_B` | unknown kg*s/m^5 | Fitted per simulation. Not a measured property of bone; no value was found in this session. |
| `minimum_effective_strain_modelling_MESm` | 1000-1500 microstrain (Andrews review) vs about 800-1500 microstrain (Wikipedia 'Mechanostat') -- not reconciled dimensionless (strain) | ASSERTED, NOT MEASURED. This is Frost's mechanostat threshold (Frost 2003 update, not read). Both ranges reached us through secondary sources at search-summary level, and they disagree on the lower bound. Neither comes with a measurement interval, so `interval` is unknown. The threshold is a postulate of the hypothesis. We found no single experiment that measures it as a material constant (scope: the searches listed under sources only). |
| `minimum_effective_strain_remodelling_MESr` | unknown dimensionless (strain) | Frost's lower (disuse) threshold. Searched for a value; the summaries we read define MESr but give no number. Left as unknown rather than quoted from memory. |
| `peak_functional_strain_vertebrates` | -0.0025 (interval -0.0052 to -0.0017) dimensionless (principal compressive strain) | MEASURED (in vivo strain gauges), but relayed second-hand. A search summary attributes "-1700 to -5200 microstrain, averaging -2500" at cortical sites of various mammals and birds during strenuous activity to a later review whose identity we did not recover. The often-quoted 2000-3500 microstrain from Rubin & Lanyon (1984, J Theor Biol) could NOT be verified: the abstract summary we reached did not contain it. A UCL paper (search-summary) disputes that strain similarity explains the spread of safety factors across tetrapods. Recorded, not reconciled. |
| `daily_cycles_turkey_ulna` | 4 cycles/day: no net change; 36 cycles/day at 0.5 Hz: periosteal and endosteal formation cycles/day | MEASURED, Rubin & Lanyon (1984, JBJS 66A), abstract level. This is the functionally isolated turkey ulna, so the baseline it is compared with is DISUSE resorption, not normal use. The authors warn the result depends on the non-physiological load distribution they imposed. |
| `static_load_effect_turkey_ulna` | no measurable effect dimensionless | MEASURED, Lanyon & Rubin (1984, J Biomech 17), abstract/index level. Static load at strains in the normal functional range had no measurable effect on remodelling. A similar intermittent load (525 N as relayed) applied for 100 s/day was associated with a 24% increase in cross-sectional area, mostly new periosteal bone. |

## Why it holds

The author's claim, Wolff (1892, as translated by Maquet & Furlong 1986; read at listing level only): bone architecture follows mathematical rules set by mechanical stress, with trabeculae lying along the principal stress trajectories. Wolff's version was a geometric claim about growth and form. A Springer chapter (search-summary) notes that the translators rendered "Transformation" as "remodelling", although Wolff was writing about growth and what is now called modelling. The modern MECHANISTIC reading is separate from Wolff's text and is a hypothesis. Osteocytes in the matrix sense dynamic strain or the fluid flow it drives, and they signal osteoblasts to form bone where the stimulus is above a set point and osteoclasts to remove it where the stimulus is below. The SED rule above encodes exactly that negative feedback, with a dead band (the lazy zone). What has actually been MEASURED is narrower than the mechanism. Bone mass in vivo rises under added DYNAMIC load: the turkey ulna, tennis players' playing arms and exercised adult zebrafish vertebrae. It falls under disuse, as in spaceflight. The feedback set point, the sensor cell, and the claim that architecture follows stress trajectories are ASSERTED or inferred, not measured.

## Where it holds

- **loading**: dynamic (cyclic) loading; static loading is outside it (see where_it_breaks)
- **tissue**: cellular (osteocytic) bone in mammals and birds; partial evidence in teleosts, including anosteocytic bone
- **taxa with in vivo evidence**: ['Meleagris gallopavo (turkey), functionally isolated ulna -- Lanyon & Rubin 1984; Rubin & Lanyon 1984', 'Homo sapiens, humerus of professional tennis players -- Jones et al. 1977; spine and hip in ISS crew -- Lang et al. 2004', 'Danio rerio, adult vertebrae under swim-tunnel exercise -- Suniaga et al. 2018', 'Oreochromis (tilapia), anosteocytic operculum under controlled loading -- Atkins et al. 2015 (search-summary)', 'Salmon vertebrae -- PMC3196754 (search-summary; authors not recovered)']
- **life stage**: strongest before sexual maturity (Pearson & Lieberman 2004, abstract level)
- **notes**: The law is reliable as a qualitative statement: under added dynamic load, bone mass at the loaded site rises, and under unloading it falls. The size of the response is specific to species, site and age. No source we read gives a transferable gain, threshold or time constant.


:::{danger} Where it breaks
(1) STATIC LOAD -- no response. Lanyon & Rubin (1984), abstract level: static load at normal functional strain had no measurable effect on remodelling of the isolated turkey ulna, while a similar intermittent load for 100 s/day added 24% cross-sectional area. Any formulation driven by strain or SED MAGNITUDE alone, including the SED rule in `equation` as written, predicts the same response for both and is therefore wrong here. The SED rule needs a load history averaged over cycles to avoid this. That diagnosis is our inference; it is not quoted from the paper. (2) TRABECULAR "TRAJECTORIES" -- Wolff's own mathematical claim. Cowin (1997, listing level) calls the comparison between stress trajectories in a homogeneous isotropic elastic body and trabecular architecture a "false premise". Secondary sources (search-summary) report non-orthogonal trabecular crossing near many joints, including the proximal femur. They also report that multiple-load analyses predict orientations that match the principal directions of NO single load case. So the exact orthogonal-trajectory form of the law fails, even where the qualitative mass response holds. (3) READING LOAD BACKWARDS FROM CROSS-SECTION -- the inference an engineer or palaeontologist most wants, and the one that is measured to fail. Lieberman, Polk & Demes (2004, abstract level), sheep tibia and metatarsal with rosette gauges: centroid-based section properties differ by up to 55% in magnitude from properties about the measured neutral axis. Cross-sectional properties "do not necessarily provide reliable data on the orientations of loads". Demes et al. (2001, macaque tibia, abstract level): the bending axis does not coincide with the section's maximum principal axis, so the geometry does not minimise strain or tissue. Demes et al. (1998, macaque ulna, abstract level): predominant bending is mediolateral, yet the ulna is not reinforced in that plane. (4) ADULTS -- reduced response. Pearson & Lieberman (2004, abstract level): cortical bone is primarily responsive to strain before sexual maturity, in both modelling and Haversian remodelling rates. The authors state Wolff's law "is not always true" and is several processes best treated separately. Do not apply a response gain measured in juveniles to adults. (5) LOW-STRAIN SKELETAL REGIONS -- bone persists where the stimulus is low. Hylander, Ravosa and colleagues (search-summary) report low strains in the primate cranial vault and upper face during feeding. They argue that bone mass there is set by growth, calcium metabolism or spatial packing rather than by chewing loads. Taken at face value, a homeostatic set-point model would resorb that bone. Contested (see contested_by). (6) THE SIMULATION ITSELF -- non-unique and discontinuous. Weinans, Huiskes & Grootenboer (1992, abstract level): the SED rule converges to a "discontinuous patchwork". It behaves as a nonlinear dynamical system that diverges relative to its objective, leading to "many possible solutions" that depend on the rule parameters, the load and the initial conditions. A density map from this rule is a SIMULATED result, not an observation, and its resemblance to a real femur is a visual comparison, not a validation. (7) TAXON -- the mechanism breaks before the phenomenon does. Most neoteleost fish have acellular (anosteocytic) bone. Atkins et al. (2015, search-summary) report that the tilapia operculum adapts to applied load with both resorption and deposition despite having no osteocytes, and propose osteoblasts as the sensor. Any design rule that relies on osteocyte density or osteocyte signalling therefore does not transfer to these fish. The adaptation itself does appear to transfer, on that one study. An Oxford review (search-summary; authors not recovered) argues that teleost osteocytes serve mineral homeostasis, not strain sensing. (8) EXTRAPOLATION IN TIME. Lang et al. (2004), abstract level, caution that their 4- to 6-month spaceflight loss rates should not be used to predict much longer missions. Linear projection of any measured rate beyond the measured duration is outside the evidence.
:::

## Worked examples

**Homo sapiens, professional tennis players (playing vs non-playing humerus)**

- value: `cortical thickness +34.9% (men), +28.4% (women), playing side vs control side`

- OBSERVATION (radiographs, Jones et al. 1977, as relayed at search-summary level). It is cross-sectional, so it cannot separate an adaptive response from a selection effect or a growth-period effect. Haapasalo et al. (1996, search-summary) report side-to-side differences of about 6.9% to 45.2%, larger in players who started young, which is consistent with breaking point (4).

- evidence: **literature**

**Homo sapiens, ISS crew (14 crewmembers, 4- to 6-month flights)**

```
6 months * 2.2 %/month = 13.2 % ; 6 months * 2.7 %/month = 16.2 % (linear, no compounding)
```

- value: `hip trabecular vBMD loss 2.2-2.7 %/month (measured); 6-month projection 13.2-16.2 % (calculated)`

- The monthly rates are MEASURED (QCT, Lang et al. 2004 abstract). Over the same flights, hip cortical vBMD fell 0.4-0.5 %/month and spine aBMD 0.9 %/month. The 6-month figure is our CALCULATION, a linear multiplication within the measured flight duration, not a reported value. A 2004 UCSF press summary gives hip cortical loss of 1.6-1.7 %/month, which disagrees with the paper's abstract (0.4-0.5 %/month). We use the abstract and record the discrepancy.

- evidence: **derived**

**Meleagris gallopavo, functionally isolated ulna**

- value: `static load: no measurable effect; 100 s/day intermittent load: +24% cross-sectional area`

- OBSERVATION (Lanyon & Rubin 1984, abstract/index level). This is the cleanest demonstration of breaking point (1).

- evidence: **literature**

**Danio rerio, adult, 4 weeks forced swimming**

- value: `increased osteoblast number, vertebral bone volume, mineralisation and bone formation rate; mineral apposition rate not significantly different`

- OBSERVATION (Suniaga et al. 2018, search-summary of the paper and its ZFIN figure records). No effect sizes were extracted in this session, so none are given. Zebrafish bone is osteocytic (cellular); that is background knowledge, not taken from this source. So this case does not test breaking point (7).

- evidence: **literature**

**Homo sapiens, femur around a total-hip stem (finite-element model)**

- value: `predicted periprosthetic resorption increases with stem rigidity and depends on bonding`

- SIMULATED, not observed (Huiskes et al. 1987, abstract level). The model applies the SED rule in `equation` with k set from the intact femur. The output is a model prediction; whether it matched clinical radiographs was not checked in this session.

- evidence: **derived**

:::{seealso} Contested
- Bertram & Swartz (1991), 'The law of bone transformation: a case of crying Wolff?' -- a critique by title; its arguments were NOT read (bibliographic listing only) and are not summarised here.
- Cowin (1997): the trajectorial (Wolff's mathematical) form rests on a false premise. Ruff, Holt & Trinkaus (2006, AJPA 129:484-498; citation from memory, search did not reach it) are generally cited as defending bone functional adaptation for inferring behaviour from skeletons. Their arguments were not read.
- Lieberman, Polk & Demes (2004) and Demes et al. (2001): cross-sectional geometry does not reliably give loading direction. This stands against the routine palaeoanthropological use of section properties as a record of behaviour.
- Cranial bone: Hylander, Ravosa and colleagues hold that low-strain cranial bone is not maintained by feeding loads. Dechow, Wang & Peterson (2011; search-summary) report that functional forces appear important for maintaining bone mass across the craniofacial skeleton, including low-strain browridges. Their evidence is on material properties in dentate vs edentulous individuals, not on strain-driven remodelling directly. Not reconciled.
- Teleost sensor: Atkins et al. (2015) hold that anosteocytic bone adapts, with osteoblasts as the likely sensor. An Oxford review holds that teleost osteocytes serve mineral homeostasis rather than strain detection. Not reconciled.
- Strain similarity: Rubin & Lanyon (1984, J Theor Biol) propose that vertebrates hold peak functional strain similar across body size. A later UCL paper (search-summary) argues this does not explain the diversity of safety factors across taxa, ontogeny and function.
:::

## Sources

| Citation | Read-level |
|---|---|
| Wolff J (1892) Das Gesetz der Transformation der Knochen. Berlin: A. Hirschwald. English translation: Maquet P, Furlong R (1986) The Law of Bone Remodelling. Berlin: Springer. | `listing` |
| Lanyon LE, Rubin CT (1984) Static vs dynamic loads as an influence on bone remodelling. J Biomech 17(12):897-905 | `abstract` |
| Rubin CT, Lanyon LE (1984) Regulation of bone formation by applied dynamic loads. J Bone Joint Surg Am 66:397-402 | `abstract` |
| Rubin CT, Lanyon LE (1984) Dynamic strain similarity in vertebrates; an alternative to allometric limb bone scaling. J Theor Biol 107(2):321-327 | `search-summary` |
| Frost HM (2003) Bone's mechanostat: a 2003 update. Anat Rec A 275A:1081-1101 | `listing` |
| Andrews (Eur J Transl Myol / Basic Appl Myol, vol 26 issue 4) review relaying Frost's MESm; full author list and title not recovered | `search-summary` |
| Wikipedia, 'Mechanostat' (tertiary source; used only to show the disagreement on MESm) | `search-summary` |
| Huiskes R, Weinans H, Grootenboer HJ, Dalstra M, Fudala B, Slooff TJ (1987) Adaptive bone-remodeling theory applied to prosthetic-design analysis. J Biomech 20(11-12):1135-1150 | `abstract` |
| Weinans H, Huiskes R, Grootenboer HJ (1992) The behavior of adaptive bone-remodeling simulation models. J Biomech 25(12):1425-1441. doi:10.1016/0021-9290(92)90056-7 | `abstract` |
| Sci Rep 2019, doi:10.1038/s41598-019-51429-w (SED-model parameter sensitivity; authors and title not recovered) | `search-summary` |
| Cowin SC (1997) The false premise of Wolff's law. Forma 12:247-262 | `listing` |
| Bertram JEA, Swartz SM (1991) The 'law of bone transformation': a case of crying Wolff? Biol Rev 66(3):245-273 | `listing` |
| Ruff C, Holt B, Trinkaus E (2006) Who's afraid of the big bad Wolff?: 'Wolff's law' and bone functional adaptation. Am J Phys Anthropol 129:484-498 (citation details from memory; a search for it returned nothing relevant) | `could-not-access` |
| Pearson OM, Lieberman DE (2004) The aging of Wolff's 'law': ontogeny and responses to mechanical loading in cortical bone. Yearb Phys Anthropol 47:63-99. doi:10.1002/ajpa.20155 | `abstract` |
| Lieberman DE, Polk JD, Demes B (2004) Predicting long bone loading from cross-sectional geometry. Am J Phys Anthropol 123:156-171 | `abstract` |
| Demes B, et al. (2001) Patterns of strain in the macaque tibia during functional activity. Am J Phys Anthropol 116(4):257-265 | `abstract` |
| Demes B, et al. (1998) Patterns of strain in the macaque ulna during functional activity. Am J Phys Anthropol 106(1):87-100 | `abstract` |
| Jones HH, Priest JD, Hayes WC, Tichenor CC, Nagel DA (1977) Humeral hypertrophy in response to exercise. J Bone Joint Surg Am 59(2):204-208 | `search-summary` |
| Haapasalo H, et al. (1996) tennis-loaded humerus, side-to-side cortical differences (journal, volume and exact title not confirmed in this session) | `search-summary` |
| Lang T, LeBlanc A, Evans H, Lu Y, Genant H, Yu A (2004) Cortical and trabecular bone mineral loss from the spine and hip in long-duration spaceflight. J Bone Miner Res 19:1006-1012 | `abstract` |
| Suniaga S, Rolvien T, vom Scheidt A, Fiedler IAK, Bale HA, Huysseune A, Witten PE, Amling M, Busse B (2018) Increased mechanical loading through controlled swimming exercise induces bone formation and mineralization in adult zebrafish. Sci Rep 8:3646. doi:10.1038/s41598-018-21776-1 | `search-summary` |
| Atkins A, et al. (2015) The response of anosteocytic bone to controlled loading. J Exp Biol | `search-summary` |
| Dean MN, Shahar R (2012) The structure-mechanics relationship and the response to load of the acellular bone of neoteleost fish: a review. J Appl Ichthyol 28:320-329 | `listing` |
| Dechow PC, Wang Q, Peterson J (2011) craniofacial cortical bone properties in dentate vs edentulous individuals (journal and exact title not recovered; PMC3096942 as surfaced) | `search-summary` |
| Hylander, Ravosa and colleagues on low cranial strains during mastication (specific papers not recovered; position relayed by search summary) | `search-summary` |


---

*Generated from [`library/laws/wolff.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/wolff.yaml). Do not edit this page; edit the YAML.*
