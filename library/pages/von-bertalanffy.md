---
title: Von Bertalanffy growth, and where it fails for indeterminate growers
label: law-von-bertalanffy
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-von-bertalanffy
\frac{dL}{dt} = K\,(L_\infty - L) \quad\Longrightarrow\quad L(t) = L_\infty\left(1 - e^{-K\,(t - t_0)}\right)
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `dL_dt` | L/T | m/s | rate of change of body length (in practice reported in cm/yr or mm/day) |
| `L` | L | m | body length at age t (standard, fork or total length; the convention must be stated per data set) |
| `L_inf` | L | m | asymptotic length: a FITTED parameter, the length at which the fitted curve predicts zero growth |
| `K` | 1/T | 1/s | Brody growth coefficient (in practice reported per year); sets how fast L approaches L_inf |
| `t` | T | s | age |
| `t_0` | T | s | hypothetical age at which the fitted curve gives zero length; usually negative and without biological meaning |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `anabolism_exponent` | 0.6667 (interval 0.14 to 0.94) dimensionless | 2/3 is the value ASSUMED in the classical derivation (anabolism scaling with an absorbing surface, i.e. mass^(2/3)), not a measured value; the length form above follows from it exactly. The interval is the range of best-fit exponents a in m' = p*m^a - q*m reported by Renner-Martin et al. (2018) for the 11 of their 60 data sets they considered free of fitting problems. Across all 60 the best fit ranged over the whole search range, 0 to 0.99, and 24 data sets had their optimum on the 0.99 boundary. These are fitted values (calculated from observed growth data), and the authors conclude the data do not support a universal exponent. |
| `anabolism_exponent_zebrafish` | 0.99 (interval 0.57 to 0.99) dimensionless | Renner-Martin et al. (2018), Table 3, two zebrafish data sets of 7 points each: Gomez-Requeni et al. (2010; male, time-weight) best fit a = 0.99 with non-refutation interval 0.66-0.99; Kaushik, Georga & Koumoundouros (2011; larvae, time-length, mass taken as length^3) best fit a = 0.99 with interval 0.57-0.99. The listed interval is the union of the two, which is our construction. Both optima sit on the upper boundary of the search range. 2/3 lies inside both non-refutation intervals, so these data do NOT refute the classical exponent; they fail to pin it down. |
| `L_inf_zebrafish` | unknown m | No published von Bertalanffy L_inf or K for Danio rerio was found. Scope of the negative: one web search ("zebrafish Danio rerio von Bertalanffy growth parameters L infinity K standard length", Nov 2026) and a fetch of the add-my-pet Danio rerio report, which failed because www.bio.vu.nl is outside this session's network allowlist. FishBase was not checked. Not filled from memory. |

## Why it holds

Von Bertalanffy (1938) wrote growth in mass as the difference of two processes, dm/dt = p*m^(2/3) - q*m: anabolism limited by an absorbing surface (scaling as mass^(2/3)) and catabolism proportional to mass (as summarised by secondary sources; the 1938 paper itself was not read). Under isometry (m ~ L^3) this becomes the linear equation dL/dt = K*(L_inf - L), whose solution is the exponential approach to an asymptote. Growth slows because the surface-limited intake falls behind mass-proportional maintenance. The asymptote is therefore a balance point of two assumed scalings, not a programmed size limit. Lester, Shuter & Abrams (2004) give a different reading (their claim, abstract level): the VB curve describes growth AFTER maturity, and its deceleration reflects energy diverted into reproduction, with VB parameters that are simple functions of age at maturity and reproductive investment. The two readings predict the same curve shape after maturity and differ on why it bends.

## Where it holds

- **taxa**: ['teleost fishes', 'elasmobranchs', 'other indeterminate growers fitted in fisheries practice (bivalves, crustaceans)']
- **life stage**: post-maturity somatic growth in length (Lester et al. 2004)
- **data requirement**: length-at-age spanning the bend toward the asymptote; the fit is an interpolation within the sampled ages
- **notes**: Valid as a descriptive fit to length-at-age of an iteroparous indeterminate grower after maturity, under roughly constant food and temperature, within the range of ages actually sampled. The parameters belong to a population under its rearing or environmental conditions, not to a species. Pauly (1980) used L_inf, K and mean temperature to predict natural mortality across 175 stocks of 84 species (title and abstract level; the regression coefficients were not verified in this session and are not reproduced here).


:::{danger} Where it breaks
(1) BEFORE MATURITY -- claimed in the source. Lester, Shuter & Abrams (2004) state that the VB equation describes somatic growth after maturity "but not before". Our inference: any design or model that needs juvenile or larval size from a VB curve fitted to adults is extrapolating outside the claimed domain. (2) LARVAE AND EARLY JUVENILES -- VB has no inflection point. The curve is concave from t_0 onward, so it cannot represent an initial accelerating (exponential or sigmoid) phase. Zweifel & Lasker (1976) argued Gompertz or logistic forms are more appropriate for early fish growth and fitted two-phase Gompertz curves to larval data (search-summary level). Urban (2002) reports that special VB and Richards curves cannot reproduce the exponential growth of the first two developmental stages of bivalves (search-summary level; bivalves, not fish). (3) THE ASYMPTOTE IS A FIT ARTIFACT, NOT A SIZE LIMIT. L_inf is the length at which the fitted curve stops, and it moves with the curve family and with which ages were sampled. Pardo, Cooper & Dulvy (2013) report that fixing the third parameter (L0) at observed size-at-birth in elasmobranchs biases the growth estimate, and recommend the three-parameter form. Our inference: an indeterminate grower sampled only while still growing gives an L_inf that is an extrapolation beyond every observation, and should not be used as a maximum body size in a design check. (4) THE EXPONENT IS NOT UNIVERSAL. The mass^(2/3) anabolism term is an assumption. Renner-Martin et al. (2018) fitted the general exponent to 60 data sets (37 fish, 23 non-fish) and found best-fit values from 0 to 0.99, and conclude no universal exponent is supported. For both zebrafish data sets the optimum was on the 0.99 boundary, with 2/3 still inside the non-refutation interval: 7-point zebrafish growth series do not identify the exponent at all. (5) MATURITY CANNOT BE OPTIMISED INSIDE A FIXED VB CURVE. Day & Taylor (1997) argue, by their title, that VB should not be used to model age and size at maturity (title and listing only; argument not read). Lester et al. (2004) make the consistent claim that the VB parameters themselves depend on age at maturity and reproductive effort, so holding L_inf and K fixed while varying maturation is self-contradictory. Our inference from both: VB cannot be used to predict how an engineered change in maturation timing changes adult size. (6) ZEBRAFISH: AGE IS A POOR PREDICTOR OF SIZE. Singleman & Holtzman (2014) state that growth rate varies with temperature, density, water quality, genetics and food, and that defining stages by age is problematic; they stage by standard length instead. Our inference: a K fitted in one facility is not a zebrafish constant and must not be carried to another rearing regime. (7) DETERMINATE GROWERS ARE OUTSIDE THE LAW. Secondary sources report that von Bertalanffy himself used an exponent of 1 (exponential growth stopped by metamorphosis) for insects rather than the 2/3 form.
:::

## Worked examples

**any population with a fitted K (no taxon)**

```
L/L_inf = 1 - exp(-K*(t - t_0)) = 0.95  ->  t - t_0 = ln(20)/K = 3.0/K;  with an ASSUMED K = 0.5 /yr, t - t_0 = 6.0 yr
```

- value: `6.0`

- DERIVED, not observed; K = 0.5 /yr is an assumed illustrative value, not a measurement for any species. The point is the shape of the law: a fixed fraction of L_inf is reached at a time that scales as 1/K, and the curve never reaches L_inf, so "time to adult size" depends entirely on the arbitrary fraction chosen.

- evidence: **derived**

**Danio rerio, two published growth series (male time-weight; larval time-length)**

- value: `0.99`

- value range: `[0.57, 0.99]`

- Fitted by Renner-Martin et al. (2018) from observed data: best-fit anabolism exponent at the upper boundary for both series, 2/3 not refuted. A calculated result from observations, not a direct observation. It shows that the available zebrafish series cannot discriminate VB from near-exponential growth.

- evidence: **literature**

**Elasmobranchs (published length-at-age compilations)**

- Pardo et al. (2013) report that the two-parameter VB with L0 fixed at birth size often mismatched the data and that small errors in the fixed L0 biased the growth coefficient considerably (as summarised by search results; abstract not read directly).

- evidence: **literature**

:::{seealso} Contested
- Mechanism of the bend: von Bertalanffy (1938, via secondary sources) attributes deceleration to surface-limited anabolism (exponent 2/3); Lester, Shuter & Abrams (2004) attribute post-maturity deceleration to reproductive investment. Not reconciled here.
- Exponent: West, Brown & Enquist (2001) derive an ontogenetic growth model with exponent 3/4 in place of 2/3; Banavar, Damuth, Maritan & Rinaldo (2002, Nature comment) argue the data do not distinguish 3/4 from 2/3; Renner-Martin et al. (2018) find no universal exponent at all across 60 data sets.
- Gill-oxygen limitation: Pauly & Cheung (2017, 2018) defend gill surface area limitation as the cause of asymptotic growth in water-breathers; Lefevre, McKenzie & Nilsson (2017, 2018) argue the gill-area scaling assumption is invalid because gills are folded surfaces whose area can scale linearly with body mass. Recorded as a live dispute.
- Early growth: Zweifel & Lasker (1976) favour Gompertz-type curves for larval fish; Urban (2002) finds a generalized VB with an extra shape parameter fits bivalve early stages best. Which replacement is better is unresolved and taxon-dependent.
:::

## Sources

| Citation | Read-level |
|---|---|
| von Bertalanffy L (1938) A quantitative theory of organic growth (Inquiries on growth laws. II). Human Biology 10:181-213 | `search-summary` |
| Lester NP, Shuter BJ, Abrams PA (2004) Interpreting the von Bertalanffy model of somatic growth in fishes: the cost of reproduction. Proc R Soc B 271:1625-1631. doi:10.1098/rspb.2004.2778 | `abstract` |
| Day T, Taylor PD (1997) Von Bertalanffy's growth equation should not be used to model age and size at maturity. American Naturalist 149(2):381-393. doi:10.1086/285995 | `listing` |
| Renner-Martin K, Brunner N, Kuehleitner M, Nowak WG, Scheicher K (2018) On the exponent in the Von Bertalanffy growth model. PeerJ 6:e4205. doi:10.7717/peerj.4205 | `full-text` |
| Pardo SA, Cooper AB, Dulvy NK (2013) Avoiding fishy growth curves. Methods in Ecology and Evolution 4:353-360 | `search-summary` |
| Zweifel JR, Lasker R (1976) Fishery Bulletin 74(3) (volume and issue inferred from the NOAA archive URL path; title and pages not verified in this session) | `search-summary` |
| Urban HJ (2002) Modeling growth of different developmental stages in bivalves. Marine Ecology Progress Series 238:109-114 | `search-summary` |
| Singleman C, Holtzman NG (2014) Growth and maturation in the zebrafish, Danio rerio: a staging tool for teaching and research. Zebrafish 11(4):396-406. doi:10.1089/zeb.2014.0976 | `full-text` |
| Pauly D (1980) On the interrelationships between natural mortality, growth parameters, and mean environmental temperature in 175 fish stocks. J Cons Int Explor Mer 39(2):175-192 | `search-summary` |
| West GB, Brown JH, Enquist BJ (2001) A general model for ontogenetic growth. Nature 413:628-631 | `search-summary` |
| Banavar JR, Damuth J, Maritan A, Rinaldo A (2002) Nature comment on West et al. 2001; title not verified in this session. arXiv:cond-mat/0301217 | `search-summary` |
| Lefevre S, McKenzie DJ, Nilsson GE (2017) Models projecting the fate of fish populations under climate change need to be based on valid physiological mechanisms. Global Change Biology 23:3449-3459 | `search-summary` |
| Pauly D, Cheung WWL (2017) Sound physiological knowledge and principles in modeling shrinking of fishes under climate change. Global Change Biology 24(1) | `search-summary` |
| Lefevre S, McKenzie DJ, Nilsson GE (2018) In modelling effects of global warming, invalid assumptions lead to unrealistic projections. Global Change Biology 24(2):553-556 | `search-summary` |
| Pauly D, Cheung WWL (2018) On confusing cause and effect in the oxygen limitation of fish. Global Change Biology | `search-summary` |


---

*Generated from [`library/laws/von-bertalanffy.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/von-bertalanffy.yaml). Do not edit this page; edit the YAML.*
