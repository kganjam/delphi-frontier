---
title: Kleiber's law -- interspecific scaling of basal metabolic rate with body mass (exponent contested, 2/3 vs 3/4)
label: law-kleiber
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-kleiber
B = B_{\mathrm{ref}} \left(\frac{M}{M_{\mathrm{ref}}}\right)^{b}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `B` | M*L^2/T^3 | W | whole-organism basal (resting, post-absorptive, thermoneutral) metabolic rate |
| `B_ref` | M*L^2/T^3 | W | metabolic rate of a reference animal of mass M_ref on the fitted line (the normalisation constant) |
| `M` | M | kg | adult body mass |
| `M_ref` | M | kg | reference mass; 1 kg by convention, which makes B_ref the familiar W per kg^b coefficient |
| `b` | 1 | dimensionless | scaling exponent -- THE CONTESTED QUANTITY; 3/4 (Kleiber) or 2/3 (surface law / White & Seymour); see constants and contested_by |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `exponent_quarter_power_canonical` | 0.75 dimensionless | The value the law is named for. Per a secondary source (Smil essay, search-summary), Kleiber's 1932 fit was 0.74 and he later adopted 3/4 in The Fire of Life (1961). We did not read Kleiber 1932 or 1961 ourselves, so the rounding history is secondary-source only. 3/4 is a proposed exact value, not a measurement, so it has no measured interval. |
| `exponent_surface_law` | 0.6667 dimensionless | 2/3, the geometric-similarity (Rubner surface-law) value. Dodds, Rothman & Weitz (2001) treat it as the null hypothesis. A derived value, not a measurement; no interval. |
| `exponent_kleiber_1932_data_refit` | 0.737 dimensionless | OBSERVATION-BASED FIT, but White & Seymour's (2003) refit of Kleiber's 1932 compilation (13 data points, eight species; r^2 = 0.999), not a number we took from Kleiber himself. White & Seymour report 0.727 with the four ruminant points removed, and 0.667 (r^2 = 0.999) for the five points left after also removing the dog and human points. They report that none of 250,000 random 13-species mammal subsets reached r^2 > 0.999. No interval in the text we read. |
| `exponent_white_seymour_2003_uncorrected` | 0.69 dimensionless | Observation-based fit over 619 mammal species, five orders of magnitude in mass, r^2 = 0.94. The authors state that the 95% CI excludes BOTH 2/3 and 3/4, but the numeric CI is only in their Fig. 2a, which we did not extract. Recorded as unknown rather than read off a figure. |
| `exponent_white_seymour_2003_corrected` | 0.68 (interspecific; n = 469 species); 0.65 (interordinal; 15 orders) dimensionless | After a Q10 = 3 correction to 36.2 C and exclusion of artiodactyls, macropodids, lagomorphs and soricids. The authors report both values differ significantly from 3/4 and not from 2/3. The exclusions are the authors' choice, justified by them as removing groups whose fermentation or hyperactivity prevents a true basal measurement; quarter-power proponents (Savage et al. 2004) argue instead that the 2/3 result rests almost entirely on mammalian BMR. Numeric CIs not in the text read. |
| `exponent_metazoa_delong_2010` | 0.76; 0.79 dimensionless | DeLong et al. (2010), abstract level, two values reported for metazoans ("approximately Kleiber's law"). That the pair corresponds to inactive vs active metabolism is OUR inference from the parallel prokaryote pair in the same abstract, not confirmed from the full text. |
| `exponent_protists_delong_2010` | 1.0; 1.1 dimensionless | DeLong et al. (2010), abstract level. Near-linear -- outside Kleiber's law. |
| `exponent_prokaryotes_delong_2010` | 1.7; 2.0 dimensionless | DeLong et al. (2010), abstract level, inactive and active metabolism respectively. SUPERLINEAR. A third-party summary (arXiv 1612.04695) gives 1.72 and 1.96 and notes the prokaryote data span only about two orders of magnitude in mass, so the fit is sensitive to data inclusion. |
| `exponent_plants_saplings_enquist_reading` | 0.78 (interval 0.7 to 0.86) dimensionless | Enquist et al. (2007) refit of Reich et al.'s (2006) own data for saplings with above-ground biomass > 30 g: theta = 0.78 +/- 0.08, r^2 = 0.86. The interval is that +/- 0.08 taken literally; whether it is an SE or a 95% CI was not stated in the text we saw. Reich et al. read the same data as approximately isometric overall. Both readings are kept. |
| `B_ref_mammal_canonical` | 3.4 W | For M_ref = 1 kg and b = 3/4: the textbook form B ~ 70 kcal/day x M^(3/4) ~ 3.4 W x M^(3/4), M in kg. Source is Wikipedia (search-summary level); we could not tie the 70 kcal/day coefficient to a specific Kleiber paper. 70 kcal/day = 3.39 W is our unit conversion. White & Seymour (2003) report no normalisation constant in the text we read. Only valid paired with b = 3/4; a B_ref fitted with b = 2/3 is a different number and must not be mixed with this one. |

## Why it holds

CONTESTED -- there is no agreed mechanism, and the two exponents come with rival ones. (1) Surface law, b = 2/3: under geometric similarity, area scales as M^(2/3), and heat loss (or any exchange across a surface) scales with area; Rubner's argument as recounted by White & Seymour (2003). (2) Network supply, b = 3/4: West, Brown & Enquist (1997) claim that a space-filling, fractal-like branching distribution network that minimises dissipation and has size-invariant terminal units (capillaries) forces whole-organism supply rate to scale as M^(3/4). (3) Neither: Glazier (2005) proposes a "metabolic-level boundaries hypothesis" in which b moves between 2/3 (surface-limited) and 1 (volume-limited) with activity level and lifestyle, so no single exponent is expected. Kolokotrones et al. (2010) report that the WBE model fails their curvature test. Which mechanism is right is not settled here; the entry records that the observation (a sublinear allometry in mammals) is much better established than any of the explanations.

## Where it holds

- **quantity**: basal (resting, post-absorptive, thermoneutral) metabolic rate, whole organism
- **comparison**: interspecific, across adult means of species -- not within a species or across ontogeny
- **taxa**: ['mammals (the original and best-sampled case)', 'metazoans broadly per DeLong et al. 2010 (b ~ 0.76-0.79)']
- **mass range mammals kg**: unknown
- **notes**: White & Seymour's mammal data span "five orders of magnitude" of body mass; we did not extract the endpoints, so the range is recorded as unknown rather than guessed. Even inside this domain the exponent depends on dataset composition and on temperature correction (0.65 to 0.74 across the analyses above), and the log-log relation is curved (Kolokotrones et al. 2010), so b is a local slope over whatever mass range was fitted, not a constant of nature.


:::{danger} Where it breaks
Fails outright in prokaryotes (superlinear exponent) and protists (isometric), fails in small plants, fails within a species across growth, and even inside mammals the exponent is unsettled between 2/3 and 3/4 and the log-log line is curved. Details: (1) PROKARYOTES: the exponent is superlinear, b ~ 1.7 (inactive) to 2.0 (active) (DeLong et al. 2010, abstract) -- mass-specific metabolic rate RISES with size, the opposite of Kleiber's law. (2) PROTISTS: b ~ 1.0-1.1, effectively isometric (same source). (3) SMALL PLANTS: whole-plant respiration scales approximately isometrically with mass across ~500 plants of 43 species (Reich et al. 2006, abstract); Enquist et al. (2007) read the same data as shifting from ~1 in seedlings to 0.78 +/- 0.08 above 30 g above-ground biomass -- so for plants the law fails at least below ~30 g, and the two groups disagree on whether it holds above. (4) WITHIN AND ACROSS ONTOGENY OF A SPECIES: Glazier (2005) reports that the 3/4 law "is not universal, either within or among animal species" and catalogues intraspecific patterns including isometric (b = 1) scaling and ontogenetic shifts in b; Kleiber's law is an interspecific statement and must not be used to scale one animal through growth. (5) ACROSS LARGE MASS SPANS IN MAMMALS: the log-log relation is convex, not straight (Kolokotrones et al. 2010, 637 species), and Dodds et al. (2001) report a systematic rise in the fitted exponent at larger masses -- so a single-exponent extrapolation is biased at both ends of the range, and in which direction depends on where it was fitted. (6) ANY ONE SPECIES: residuals are large; White & Seymour report humans at 180-200% of the predicted value. The law predicts a clade's trend, not an individual species' BMR. (7) THE EXPONENT ITSELF: across a mouse-to-elephant span, 2/3 and 3/4 predictions differ by a factor of ~2.8 (calculated, see worked_examples), and the literature does not agree which is right; any design number that depends on that factor is not constrained by this law. (8) ECTOTHERMS, including fish: basal rate depends strongly on body temperature, and the mammalian B_ref does not transfer; we found no fish-specific normalisation in the searches listed under sources (scope: six web searches, Nov 2026, none targeted at fish).
:::

## Worked examples

**Homo sapiens, 70 kg adult, canonical form**

```
B = 3.39 W x 70^0.75 = 3.39 x 24.2 = 82 W (= 1694 kcal/day)
```

- value: `82`

- CALCULATED from the textbook coefficient, not a measurement. White & Seymour (2003) report measured human BMR at 180-200% of the value predicted by THEIR 2/3 fit -- a different line, so their percentage cannot be applied to this 82 W figure. The example shows the arithmetic, not accuracy.

- evidence: **derived**

**mouse (0.02 kg) to elephant (4000 kg) extrapolation, 3/4 vs 2/3**

```
Mass ratio 4000/0.02 = 2.0e5. Predicted BMR ratio: (2.0e5)^(3/4) = 9457 vs (2.0e5)^(2/3) = 3420. Divergence = (2.0e5)^(1/12) = 2.77.

```

- value: `2.77`

- CALCULATED, not observed. Anchored at the mouse, the two contested exponents predict elephant BMRs differing by a factor of ~2.8. Over a 1e3 mass span the factor is 1.78; over 1e6 it is 3.16. This is the size of the disagreement an engineer inherits if they extrapolate with this law. The 0.02 kg and 4000 kg masses are round illustrative values, not data from any cited study.

- evidence: **derived**

**Danio rerio (adult zebrafish)**

- value: `unknown`

- Not computed. Zebrafish are ectotherms outside the mammalian domain where B_ref = 3.4 W was fitted, and no fish normalisation constant or fish exponent was found in the searches listed under sources (none of which targeted fish). Applying the mammal line here would be manufacturing a number.

- evidence: **none**

:::{seealso} Contested
- White & Seymour (2003): 619 mammal species; after temperature correction and exclusion of fermenting/hyperactive groups, b = 0.68 (n = 469), not different from 2/3 and different from 3/4. They argue Kleiber's 3/4 'seems to stem from an exceedingly fortuitous selection of data' (13 points, ~20% artiodactyls).
- Dodds, Rothman & Weitz (2001): treat 2/3 as the null; reanalysis of Heusner, Bennett & Harvey, Bartels, Hemmingsen, Brody and Kleiber data finds little evidence for rejecting 2/3 in favour of 3/4, and judges theories for 3/4 too assumption-dependent to reject the null. They explicitly do not propose replacing the 3/4 law with a 2/3 law.
- Savage et al. (2004): argue the opposite -- quarter-power scaling is pervasive across basal, field and maximal metabolic rates and many other biological rates and times, and that recent claims for 2/3 rest almost entirely on mammalian BMR.
- West, Brown & Enquist (1997): derive 3/4 from space-filling fractal supply networks. Kolokotrones et al. (2010) report the model fails their curvature test; Price, Enquist & Savage (2007) concede it cannot fully explain the range of observed exponents.
- Kolokotrones et al. (2010): the mammalian relation is convex on log-log axes and therefore not a pure power law at all, so the 2/3-vs-3/4 question has no single answer. A further position, not a reconciliation of the first two.
- Glazier (2005): no universal exponent within or among animal species; b varies between ~2/3 and 1 with activity level, lifestyle and temperature regulation (metabolic-level boundaries hypothesis).
- White, Blackburn & Seymour (2009, Evolution), per a search summary only: no single value of b adequately characterises the mammalian mass-BMR relation under phylogenetically informed methods.
- This entry does NOT reconcile these positions. The 0.65-0.74 spread within mammals is a disagreement about data selection, temperature correction and curvature, not measurement noise to be averaged.
:::

## Sources

| Citation | Read-level |
|---|---|
| Kleiber M (1932) Body size and metabolism. Hilgardia 6(11):315-353 | `could-not-access` |
| Kleiber M (1947) Body size and metabolic rate. Physiol Rev 27(4):511-541 | `listing` |
| Smil V, essay on Kleiber's law (Bennington College document, https://bennington.edu/doc/21846) | `search-summary` |
| Kleiber's law, Wikipedia (https://en.wikipedia.org/wiki/Kleiber%27s_law) | `search-summary` |
| White CR, Seymour RS (2003) Mammalian basal metabolic rate is proportional to body mass^2/3. PNAS 100(7):4046-4049. doi:10.1073/pnas.0436428100 | `full-text` |
| Dodds PS, Rothman DH, Weitz JS (2001) Re-examination of the '3/4-law' of metabolism. J Theor Biol 209:9-27. doi:10.1006/jtbi.2000.2238 (preprint arXiv:physics/0007096) | `abstract` |
| West GB, Brown JH, Enquist BJ (1997) A general model for the origin of allometric scaling laws in biology. Science 276:122-126 | `search-summary` |
| Savage VM, Gillooly JF, Woodruff WH, West GB, Allen AP, Enquist BJ, Brown JH (2004) The predominance of quarter-power scaling in biology. Funct Ecol 18(2):257-282. doi:10.1111/j.0269-8463.2004.00856.x | `abstract` |
| DeLong JP, Okie JG, Moses ME, Sibly RM, Brown JH (2010) Shifts in metabolic scaling, production, and efficiency across major evolutionary transitions of life. PNAS 107(29):12941-12945. doi:10.1073/pnas.1007783107 | `abstract` |
| Kolokotrones T, Savage V, Deeds EJ, Fontana W (2010) Curvature in metabolic scaling. Nature 464:753-756 | `search-summary` |
| Glazier DS (2005) Beyond the '3/4-power law': variation in the intra- and interspecific scaling of metabolic rate in animals. Biol Rev 80:611-662. doi:10.1017/S1464793105006834 | `abstract` |
| Reich PB, Tjoelker MG, Machado J-L, Oleksyn J (2006) Universal scaling of respiratory metabolism, size and nitrogen in plants. Nature 439:457-461 | `abstract` |
| Enquist BJ et al. (2007) Does the exception prove the rule? Nature 445 (doi:10.1038/nature05548; comment on Reich et al. 2006; page numbers not verified) | `search-summary` |
| Price CA, Enquist BJ, Savage VM (2007) PNAS, PMC1941814 (title and pages not verified) | `search-summary` |
| White CR, Blackburn TM, Seymour RS (2009) Evolution (mammalian BMR scaling, phylogenetically informed) | `search-summary` |


---

*Generated from [`library/laws/kleiber.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/kleiber.yaml). Do not edit this page; edit the YAML.*
