---
title: Elastic versus geometric similarity (McMahon) and buckling-limited scaling
label: law-elastic-similarity
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-elastic-similarity
S_b = \frac{l_{cr}}{l} = \frac{C_G}{l}\left(\frac{E}{\rho g}\right)^{1/3} d^{2/3}; \qquad S_b = \text{const} \Rightarrow l \propto d^{2/3},\; d \propto M^{3/8},\; l \propto M^{1/4}; \qquad d \propto l \Rightarrow S_b \propto l^{-1/3}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `S_b` | 1 | dimensionless | buckling margin -- the ratio of the Greenhill self-weight critical height to the actual height or length. Elastic similarity is the hypothesis that S_b is the same at every size.
 |
| `C_G` | 1 | dimensionless | Greenhill prefactor for a SOLID circular section clamped at the base and free at the top; 0.7883 |
| `E` | M/(L*T^2) | Pa | Young's modulus of the column material |
| `rho` | M/L^3 | kg/m^3 | density of the column material; in water replace with the EXCESS density (rho - rho_water), which is the change that makes the law near-vacuous for aquatic organisms
 |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `d` | L | m | diameter of the column (basal trunk diameter; bone midshaft diameter) |
| `l` | L | m | actual height of a stem or length of a segment |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `greenhill_eigenvalue` | 7.8373 — *derived* | CALCULATED in this session, not measured and not quoted, so it carries no interval. It is (3/2 * j)^2 where j = 1.866351 is the first positive zero of the Bessel function J_(-1/3); I found the zero by bisection on a 40-term power series (scipy was not installed), giving 7.83735. This agrees with the value already in the greenhill entry, which was computed independently. No source printing the number was read. |
| `C_G` | 0.7883 — *derived* | CALCULATED: (7.8373/16)^(1/3), using I/A = d^2/16 for a solid circle. A hollow section (bone, bamboo, a rachis) has a larger I/A at the same outer diameter and so a larger prefactor; do not carry 0.7883 across to one. |
| `exponent_l_vs_d_predicted` | 0.667 — *derived* | PREDICTIONS, derived not measured, for the exponent lambda in l ~ d^lambda: elastic similarity 2/3; geometric similarity 1; static-stress similarity 1/2. The corresponding mass exponents (from M ~ l*d^2) are elastic d ~ M^(3/8), l ~ M^(1/4); geometric both M^(1/3); static-stress d ~ M^(2/5), l ~ M^(1/5). These three model triplets are stated identically in Kokshenev & Christiansen 2009 (read full-text-preprint). |
| `exponent_l_vs_d_artiodactyl_families` | unknown | MEASURED, reported SECOND-HAND: 0.67 (Bovidae), 0.52 (Suidae), 0.83 (Cervidae), attributed to McMahon 1975 by arXiv physics/0303074 (read full-text-preprint); the original was not opened. No single value is asserted because the three families disagree with each other by more than the gap between the competing models. |
| `exponent_l_vs_C_all_mammals` | 0.8 (interval 0.78 to 0.82) | MEASURED (a re-analysis of measured bone dimensions), reported second-hand: slenderness exponent 0.80 +/- 0.02 for length against circumference, overall-bone average, from Kokshenev 2003's re-analysis of Christiansen 1999a's wide terrestrial-mammal sample, as stated in Kokshenev & Christiansen 2009 (read full-text-preprint). The interval is the stated +/- 0.02 and its statistical meaning (SE or SD) was not stated in the passage read. The authors' point, quoted in substance: it does not match ANY of McMahon's three predictions. |
| `exponent_l_vs_C_elephants_adult` | unknown | MEASURED, intraspecific, adults only, Kokshenev & Christiansen 2009 (read full-text-preprint): LS-average slenderness exponent 0.839 in Elephas maximus against 0.662 in Loxodonta africana, reported as significantly different (p < 0.05). The African value sits on the elastic prediction of 0.667; the authors read it as adaptation to axial compression by gravity, the Asian value as adaptation to muscular bending. No sample sizes are recorded here because the table holding them was not extracted. |
| `mammal_mass_exponents_shrew_to_elephant` | unknown | Alexander, Jayes, Maloiy & Wathuta 1979 are widely reported to find limb-bone length ~ M^0.35 and diameter ~ M^0.36 across mammals from shrew to elephant. I could NOT verify these numbers: the paper's abstract was not retrievable in this session (one index lists "no abstract available"), and the only place the figures surfaced was a search summary of a student flashcard site. They are used below ONLY in a clearly labelled illustrative calculation. The qualitative finding -- near-geometric similarity across orders -- is independently stated by both arXiv texts read in full. |
| `plant_buckling_margin` | 4 | MEASURED ratio H_crit/H of about 4 across 111 species (Niklas 1994), as carried in the greenhill entry at abstract level. I did not re-read that abstract in this session (searches did not return it); the Crossref record confirms the title, journal, volume and pages. No interval. |
| `mammal_bone_safety_factor` | 3 (interval 2 to 4) | MEASURED, Biewener 1989 (abstract as relayed by a search summary in this session): peak bone stress during strenuous activity is roughly independent of body size, at a safety factor of 2-4 against FRACTURE (not buckling). The 0.1-300 kg range often attached to this result comes from later Biewener writing, per the same search; it is not confirmed for the 1989 paper. |

## Why it holds

A slender column carrying its own weight buckles when its height exceeds l_cr, set by bending stiffness E*I against weight per length rho*g*A (Greenhill 1881; the eigenvalue is a Bessel zero). For a solid circle l_cr goes as (E/(rho*g))^(1/3) * d^(2/3). Dividing by the actual length gives the buckling margin S_b. Two consequences follow by algebra alone and are the CONSTRAINING content: (i) under geometric scaling (d ~ l) S_b falls as l^(-1/3), so a scaled-up copy of any self-loaded column is relatively closer to buckling, whatever the material; (ii) holding S_b fixed requires d ~ l^(3/2), so mass ~ l*d^2 rises as l^4 rather than l^3. McMahon 1973 proposed that organisms do exactly (ii) -- "elastic similarity" -- and derived from it l ~ M^(1/4), d ~ M^(3/8), and a 3/4-power metabolic exponent. That last link is McMahon's argument and is not tested by this entry. The physics in (i) and (ii) is not in dispute; what is disputed is the biological premise that self-weight buckling (or the equivalent relative deflection) is the load an organism is designed against.

## Where it holds

- **load case**: self-weight loading of a slender, straight, prismatic, solid column, clamped at the base and free at the top
- **medium**: air; in water substitute the excess density, which usually removes the constraint
- **material**: isotropic and linearly elastic; E and rho constant along the column
- **taxa**: ['self-supporting stems and trees (the case the Greenhill bound was built for)', 'Bovidae limb bones and adult Loxodonta africana limb bones, where the measured exponent matches 2/3']
- **notes**: The S_b equation is exact only for the uniform column; taper and a crown change the prefactor, and the d^(2/3) dependence survives only while shape changes in proportion. The exponent 2/3 is a hypothesis about how organisms respond to the bound and holds only in the listed taxa.


:::{danger} Where it breaks
(1) MAMMALS IN GENERAL -- the taxon the hypothesis was most famously applied to. Kokshenev & Christiansen 2009 (full-text preprint) state flatly that the elastic and static-stress models "were found not to apply to terrestrial mammals as a group", citing Alexander et al. 1979, Biewener 1983, Economos 1983, Christiansen 1999 and others, and that limb bones are instead closer to isometry and become more robust with size in large mammals; the overall-mammal slenderness exponent of 0.80 +/- 0.02 matches none of 1, 2/3 or 1/2. Christiansen 1999 (abstract, relayed by a search summary) adds that NO single linear regression explains long-bone scaling across the size range, because small mammals approach geometric similarity much more closely than large ones -- so the failure is not just a wrong exponent but the wrong functional form. (2) THE EXPONENT IS NOT A PROPERTY OF A CLADE. Within Artiodactyla the families give 0.67, 0.52 and 0.83 (McMahon 1975, second-hand); within Elephantidae adult Asian elephants give 0.839 and adult African elephants 0.662. The two living elephant genera, the largest land mammals, fall either side of the gap, so a match in one lineage does not license the rule in its relatives. (3) THE MECHANISM IS WRONG FOR BONES even where the exponent matches. Selker & Carter 1989, as relayed by arXiv physics/0303074, report that long bones in living animals are very rarely fractured by axial load; curvature turns axial load into bending, and peak bone stresses come from muscle contraction rather than gravity. Biewener 1989 reports a size-independent fracture safety factor of 2-4, achieved (per the abstract as relayed) through posture and muscle mechanics rather than bone proportions. A matching exponent in bovids or African elephants therefore does not vindicate the buckling argument; my inference is that it is a coincidence of exponent, and Kokshenev & Christiansen offer a different (compressive stress) mechanism for the elephant case. (4) SPRAWLING TAXA. Romano & Rubidge 2019 (abstract, via search summary) report that elastic similarity does not appear to apply to captorhinid long bones, and that large captorhinids likely avoided peak-stress thresholds by moving more slowly, without repatterning bones or changing posture -- a third escape route, after posture and proportion, that the hypothesis does not contemplate. (5) PLANTS SWITCH REGIMES WITH SIZE. Niklas 1995 (Ann Bot 75:217; abstract via search summary), on 27 Robinia pseudoacacia trees, reports the height-diameter exponent above 1 in small young trees, falling to 2/3 and then 1/2 as trees grow: geometric, then elastic, then stress similarity within ONE species. Norberg 1988 is reported (search summary only) to place geometric similarity in mosses through small trees and elastic similarity only in large arborescent forms. And Niklas 1995 on herbaceous stems (Ann Bot 75:133; search summary) reports the buckling margin falling roughly as D^(-1/3) -- the margin is NOT held constant, which is the premise itself. (6) TALL TREES ARE NOT BUCKLING-LIMITED: Koch et al. 2004 (see the greenhill entry) place the height ceiling in water transport, so at the top end S_b is a number that is not the binding one. (7) WATER AND SMALL SCALE -- my calculation, not an observation: replacing rho by the excess density of near-neutrally buoyant tissue raises l_cr by a factor of about 2.8 (worked example), and for millimetre-scale rods in air l_cr already exceeds the structure by two orders of magnitude (greenhill entry), so in both regimes self-weight buckling never binds and flow, inertial or contact loads govern. The equation remains true there; it just stops being the constraint.
:::

## Worked examples

**idealised trunk scaled up tenfold GEOMETRICALLY, then tenfold ELASTICALLY**

```
assumed (not measured for any species): E = 10 GPa, rho = 600 kg/m^3, g = 9.81 m/s^2, solid section
start: d = 0.5 m, l = 15 m -> l_cr = 0.7883 * (1e10/(600*9.81))^(1/3) * 0.5^(2/3) = 59.3 m ; S_b = 3.95
geometric x10: d = 5 m, l = 150 m -> l_cr = 275 m ; S_b = 1.83      (= 3.95 * 10^(-1/3))
elastic   x10 in length: d must rise by 10^(3/2) = 31.6x to keep S_b = 3.95
mass ratio vs the start: geometric 10^3 = 1000x ; elastic 10 * 31.6^2 = 10000x

```

- value: `1.83`

- CALCULATED. The starting margin of about 4 was chosen to sit at the Niklas 1994 plant value; the tree is otherwise illustrative. The constraining content is the factor 10^(-1/3) = 0.464 and the tenfold mass penalty for holding the margin -- both follow from the equation alone and need no property values.

- evidence: **derived**

**a limb bone in an animal 1000x heavier -- elastic vs geometric vs a reported measurement**

```
diameter: geometric 1000^0.333 = 10.0x ; elastic 1000^0.375 = 13.3x ; reported 1000^0.36 = 12.0x
length  : geometric 1000^0.333 = 10.0x ; elastic 1000^0.25  =  5.6x ; reported 1000^0.35 = 11.2x

```

- value: `11.2`

- CALCULATED from exponents. The model rows are derived; the "reported" row uses the Alexander et al. 1979 exponents that I could NOT verify (see constants), so this row is illustrative only. The structural point holds regardless of those exact figures: the diameter row cannot discriminate the models (any value between 10 and 13.3 fits a story) while the length row separates them by a factor of two, so a check on diameters alone is not a test of the hypothesis.

- evidence: **derived**

**adult Elephas maximus vs adult Loxodonta africana, bone length change for a doubling of circumference**

```
2^0.839 = 1.79x (Asian) ; 2^0.662 = 1.58x (African) ; 2^(2/3) = 1.59x (elastic prediction) ; 2^1 = 2x (geometric)

```

- value: `1.58`

- Exponents MEASURED (Kokshenev & Christiansen 2009, full-text preprint); the multipliers are my CALCULATION from them. The African elephant matches elastic similarity to two decimal places and the Asian elephant does not; the authors attribute the African pattern to gravity-driven axial compression, not to Greenhill self-weight buckling.

- evidence: **derived**

**near-neutrally buoyant skeletal column in water (e.g. a fish fin ray)**

```
assumed: rho_tissue = 1050 kg/m^3, rho_water = 1000 kg/m^3 (illustrative, not measured for any fin ray)
l_cr(water)/l_cr(air) = (rho / (rho - rho_water))^(1/3) = (1050/50)^(1/3) = 2.76

```

- value: `2.76`

- CALCULATED. The excess density, not the tissue density, carries the weight in water, so the margin rises by about 2.8x on top of the already-vacuous small-scale margin in air. Measured densities for zebrafish fin rays are unknown; not searched in this task.

- evidence: **derived**

**Bovidae limb bones**

- value: `0.67`

- Length-versus-diameter exponent attributed to McMahon 1975 by arXiv physics/0303074. The family on which the hypothesis was built, and still the cleanest match.

- evidence: **literature**

:::{seealso} Contested
- McMahon 1973/1975 (elastic similarity fits ungulates and trees) against Alexander et al. 1979, Biewener 1983/1989, Economos 1983 and Christiansen 1999 (mammals as a group do not fit; near-isometry; postural compensation). Recorded as a disagreement; the physics of the bound is not what is contested, the biological premise is.
- arXiv physics/0303074 (author names not printed in the extracted text) argues that Biewener 1983, Bertram & Biewener 1992 and Christiansen 1999a exponents are close to MODIFIED elastic-force criteria built on muscle forces rather than self-weight, while conceding Christiansen's most accurate data conflict with the modified buckling scenario. That is the letter's proposal, not an established correction, and it disagrees with Christiansen's own conclusion that the data 'support neither geometric nor elastic similarity'.
- Kokshenev et al. 2003, as summarised by Kokshenev & Christiansen 2009, hold that the failure of McMahon's power laws reflects his simplifying assumptions (gravity dominant, muscles ignored) rather than a failure of elastic-force constraints as such. Economos 1983, as cited in both arXiv texts, doubts that any single power law can explain mammalian allometry. These two positions are incompatible and are left unreconciled.
- Plants: Norberg 1988 (geometric in small growth forms, elastic only in large trees) and Niklas 1995 (geometric to elastic to stress similarity through ontogeny in one tree species) broadly agree with each other that the regime changes with size; Niklas's herbaceous-stem result that the buckling margin falls with size contradicts the constant-margin premise in both. Niklas 1993, cited for 'neither model' in an earlier draft of this entry, could not be located in this session and is not relied on.
- Romano & Rubidge 2019: in sprawling captorhinids the compensation was neither proportion nor posture but reduced speed (authors' inference from morphometrics), adding a third mechanism the mammalian literature does not need.
:::

## Sources

| Citation | Read-level |
|---|---|
| McMahon T (1973) Science 179:1201-1204, Size and shape in biology, doi 10.1126/science.179.4079.1201 | `metadata` |
| McMahon TA (1975) Am Nat 109:547-563, Allometry and biomechanics: limb bones in adult ungulates, doi 10.1086/283026 | `metadata` |
| McMahon TA, Kronauer RE (1976) J Theor Biol 59:443-466, Tree structures: deducing the principle of mechanical design, doi 10.1016/0022-5193(76)90182-X | `metadata` |
| Alexander RMcN, Jayes AS, Maloiy GMO, Wathuta EM (1979) J Zool 189:305-314, Allometry of the limb bones of mammals from shrews (Sorex) to elephant (Loxodonta), doi 10.1111/j.1469-7998.1979.tb03964.x | `metadata` |
| Biewener AA (1983) J Exp Biol 105:147-171, Allometry of quadrupedal locomotion: the scaling of duty factor, bone curvature and limb orientation to body size, doi 10.1242/jeb.105.1.147 | `metadata` |
| Biewener AA (1989) Science 245:45-48, Scaling body support in mammals: limb posture and muscle mechanics, doi 10.1126/science.2740914 | `search-summary` |
| Biewener AA (1990) Science 250:1097-1103, Biomechanics of mammalian terrestrial locomotion, doi 10.1126/science.2251499 | `metadata` |
| Economos AC (1983) J Theor Biol 103:167-172, Elastic and/or geometric similarity in mammalian design?, doi 10.1016/0022-5193(83)90206-0 | `metadata` |
| Christiansen P (1999) J Zool 247:333-348, Scaling of mammalian long bones: small and large mammals compared, doi 10.1111/j.1469-7998.1999.tb00996.x | `search-summary` |
| Christiansen P (1999) J Morphol 239:167-190, Scaling of the limb long bones to body mass in terrestrial mammals | `listing` |
| Selker F, Carter DR (1989) J Biomech 22:1175-1183, Scaling of long bone fracture strength with animal mass | `listing` |
| Long-bone allometry of terrestrial mammals and the geometric-shape and elastic-force constraints of bone evolution, arXiv:physics/0303074v1 (2003), letter to J Theor Biol; author names not printed in the extracted text | `full-text-preprint` |
| Kokshenev VB, Christiansen P (2009) Salient features in locomotor evolutionary adaptations of proboscideans revealed via the differential scaling of limb long bones, arXiv:0909.1516v1 (submitted to J R Soc Interface) | `full-text-preprint` |
| Romano M, Rubidge B (2019) Lethaia 52:389-402, Long bone scaling in Captorhinidae: do limb bones scale according to elastic similarity in sprawling basal amniotes?, doi 10.1111/let.12319 | `search-summary` |
| Norberg RA (1988) Am Nat 131:220-256, Theory of growth geometry of plants and self-thinning of plant populations: geometric similarity, elastic similarity, and different growth modes of plant parts, doi 10.1086/284787 | `search-summary` |
| Niklas KJ (1994) Am J Bot 81:1275-1279, Interspecific allometries of critical buckling height and actual plant height, doi 10.1002/j.1537-2197.1994.tb11449.x | `metadata` |
| Niklas KJ (1995) Ann Bot 75:217-227, Size-dependent allometry of tree height, diameter and trunk-taper, doi 10.1006/anbo.1995.1015 | `search-summary` |
| Niklas KJ (1995) Ann Bot 75:133-142, Plant height and the properties of some herbaceous stems, doi 10.1006/anbo.1995.1004 | `search-summary` |
| Koch GW, Sillett SC, Jennings GM, Davis SD (2004) Nature 428:851-854, The limits to tree height, doi 10.1038/nature02417 | `listing` |
| Greenhill AG (1881) Proc Camb Philos Soc 4:65-73, Determination of the greatest height consistent with stability that a vertical pole or mast can be made | `could-not-access` |


---

*Generated from [`library/laws/elastic-similarity.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/elastic-similarity.yaml). Do not edit this page; edit the YAML.*
