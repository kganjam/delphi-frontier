---
title: Huxley allometry y = a x^b -- what the exponent means and how it is estimated
label: law-allometry-huxley
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-allometry-huxley
y = a\,x^{b} \;\Longleftrightarrow\; \frac{y}{y_{\mathrm{ref}}} = \left(\frac{x}{x_{\mathrm{ref}}}\right)^{b}, \quad a \equiv y_{\mathrm{ref}}\,x_{\mathrm{ref}}^{-b}; \qquad \ln y = \ln a + b \ln x
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `y` | M | kg | the part: any positive measured trait (organ mass in Huxley's canonical case). The dimension is declared for the part-mass-vs-body-mass case; the normalised form balances for any dimensions of x and y |
| `y_ref` | M | kg | value of y at the reference size x_ref (same dimension as y) |
| `x` | M | kg | the whole: the size variable, usually body mass |
| `x_ref` | M | kg | an arbitrary reference size; choosing it near the centre of the data minimises the correlation between the estimates of a and b |
| `b` | 1 | dimensionless | allometric exponent: the slope on log-log axes, i.e. the ratio of relative growth rates d(ln y)/d(ln x) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `isometry_same_dimension` | 1 | DERIVED from geometric similarity, not measured. It applies when y and x have the same dimension, e.g. part mass vs body mass. b > 1 is positive allometry (the part becomes relatively larger with size) and b < 1 is negative allometry. |
| `isometry_area_vs_mass` | 0.6667 | DERIVED (an area scales as length^2 and mass as length^3 at constant density). Not measured. |
| `isometry_length_vs_mass` | 0.3333 | DERIVED (a length scales as mass^(1/3) at constant density and shape). Not measured. |
| `prefactor_a` | unknown | Not a constant of the law. Its dimension is [y]*[x]^-b, so its numerical value depends on the units chosen AND on b. My inference, not a quoted source: two values of a from fits with different b, or in different units, cannot be compared. Compare y at a stated reference size (y_ref at a common x_ref) instead. |
| `bmr_exponent_mammals_white_seymour_uncorrected` | 0.69 | MEASURED (fitted). White & Seymour 2003: least-squares regression of log BMR on log M across 619 species from 19 orders. The text says the 95% CI "does not include 3/4 or 2/3". The numerical CI bounds appear only in their figures, which I did not extract, so no interval is given. |
| `bmr_exponent_mammals_white_seymour_corrected` | 0.68 | MEASURED (fitted). The same paper corrects to a body temperature of 36.2 C and excludes artiodactyls, lagomorphs, soricids and macropods (469 species), which gives 0.68 interspecific and 0.65 interordinal. The authors report these values as significantly different from 3/4 and not significantly different from 2/3. CI bounds are not extracted (figures only). |

## Why it holds

Huxley's argument (as summarised in the secondary sources below; the 1932 book was not read) is that if a part and the whole each grow at a constant ratio of RELATIVE (specific) growth rates, (1/y)dy/dt = b (1/x)dx/dt, then integrating gives ln y = ln a + b ln x, i.e. y = a x^b. On this reading b is not a shape coefficient. It is the ratio of relative growth rates, and it is constant only while that ratio is constant. Everything below is that one condition failing. The power law is a straight line on log-log axes, which is why b is estimated by fitting a line to (ln x, ln y). The intercept is ln a and the slope is b. Doubling x multiplies y by 2^b (mathematical identity). Geometric similarity gives the isometric null values listed under constants. A departure from isometry is the usual scientific content of a fitted b. ESTIMATION -- three choices, each of which changes the number (the formulas are standard statistical identities, stated by me and not quoted from a source): (i) Line-fitting method on the log scale. The OLS slope is r * s_y/s_x. The standardised major-axis (SMA, also called RMA) slope is sign(r) * s_y/s_x. So b_SMA = b_OLS/|r|, and the two agree only when |r| = 1. Warton et al. 2006 (abstract) distinguish measurement error from "equation error" and say these "have quite different implications for choice of line-fitting method". They treat regression, MA and SMA as alternatives that are appropriate when there is no measurement error. When there is measurement error, it must be estimated and used to adjust the variance terms. (ii) The error model. Fitting on log axes assumes multiplicative (lognormal) error. Fitting y = a x^b by nonlinear regression on the original scale assumes additive error unless heteroscedasticity is modelled. This choice is CONTESTED (see contested_by). (iii) Back-transformation. With lognormal residuals of SD s (natural-log scale), exp(ln a + b ln x) estimates the MEDIAN of y. The mean is larger by the factor exp(s^2/2). This is a mathematical property of the lognormal distribution, not a measured result. Comparative data add a fourth problem. Species are not independent samples, because they share ancestry. Warton et al. 2006 review phylogenetic line-fitting, but I read only their abstract and have no numbers on how much it moves b.

## Where it holds

- **form**: Any pair of strictly positive quantities whose ratio of relative growth rates (ontogeny), or whose log-log relationship across individuals or species, is constant over the sampled range. The fit is valid only within the sampled range of x. That range should be reported next to every b.

- **levels**: Ontogenetic (one individual or cohort through growth), static (individuals of one stage), and evolutionary (across species) allometries are different relationships. A b estimated at one level is not an estimate of b at another. This is a standard distinction in the field; I did not verify it against a specific source in this entry.

- **taxa in entry**: ['mammals (basal metabolic rate; White & Seymour 2003 / Kolokotrones et al. 2010)', 'Onthophagus dung beetles (horns; Emlen & Nijhout 2000 summary)', "fiddler crab Uca pugnax (Huxley's historical case; no exponent value obtained)"]

:::{danger} Where it breaks
(1) CURVATURE: THE EXPONENT IS A PROPERTY OF THE MASS RANGE SAMPLED. Kolokotrones et al. 2010 (search summary of abstract only) report convex curvature in log BMR vs log M for mammals, persisting after accounting for body temperature. A quadratic fits better than a line, and the authors offer the curvature as an explanation of the variability among published exponents. If the log-log relation is curved, the local slope changes with mass, and a single b fitted to a sub-range does not extrapolate. My inference: this applies most strongly to extrapolation beyond the largest or smallest sampled animal. (2) THRESHOLD AND SIGMOID ALLOMETRIES ARE NOT POWER LAWS. In male Onthophagus taurus, males above a threshold body size develop long horns, while smaller males develop only rudimentary horns or none (Emlen & Nijhout 2000, search summary). A single log-log line fitted through such data gives a slope that describes neither morph. The authors frame scaling relationships as reaction norms whose slope AND shape evolve. The same source summary reports that diet shifts the horn-size relationship in O. acuminatus, so b is also environment-dependent, not only taxon-dependent. (3) NARROW SIZE RANGES MAKE b A PRODUCT OF THE METHOD, NOT OF THE DATA. Because b_SMA = b_OLS/|r| (identity), a low correlation -- typical when x spans less than about an order of magnitude, as in static allometry within one stage -- makes OLS and SMA disagree by a factor 1/|r|. Worked example 2 shows this method gap alone spanning the 2/3-vs-3/4 debate. The "order of magnitude" figure is my rule of thumb, not a sourced threshold. (4) ADDITIVE COMPONENTS AND ZERO-OFFSETS. The power law forces y -> 0 as x -> 0. A trait with a size-independent component (y = c + a x^b) plots as a curve on log-log axes, and a straight-line fit returns a biased b. This follows from the algebra, not from a measured case in this entry. (5) THE PREFACTOR IS NOT TRANSFERABLE. a has dimension [y][x]^-b, so it cannot be compared across fits with different b or different units. (6) THE ERROR MODEL CHANGES THE ANSWER. Log-scale and arithmetic-scale fits weight the largest animals differently and can return different b from the same data. Which one is correct is contested (contested_by). (7) SPECIES ARE NOT INDEPENDENT DATA. Cross-species b from an ordinary fit does not account for phylogeny. This entry has no number for the size of that effect (stated as a gap, not a finding).
:::

## Worked examples

**Mammalia, basal metabolic rate (literature values, then my arithmetic)**

```
Measured exponents from White & Seymour 2003: 0.69 (619 spp, uncorrected) and 0.68 / 0.65 (temperature-corrected with taxa excluded; interspecific / interordinal). The two contested theoretical values over three decades of mass: (10^3)^(3/4 - 2/3) = 10^(3*0.08333) = 10^0.25 = 1.778.

```

- value: `1.778`

- The 1.778 is CALCULATED, not observed. It means that a 2/3 law and a 3/4 law, anchored at the same small mammal, differ in predicted BMR by about 78% for a mammal 1000x heavier. That is the practical stake of the exponent dispute. The 0.69/0.68/0.65 values are fitted results reported by the authors.

- evidence: **literature**

**none (illustrative, hypothetical data summary)**

```
ASSUMED log-scale correlation r = 0.9 and OLS slope b_OLS = 0.675 (both invented for illustration, not measurements)  ->  b_SMA = b_OLS/|r| = 0.675/0.9 = 0.75.

```

- value: `0.75`

- Calculated, not observed. With a perfectly ordinary r = 0.9, the same data give about 2/3 by OLS and exactly 3/4 by SMA. The choice of line-fitting method alone can therefore move a slope across the most-cited exponent dispute in allometry. A b reported without its method and r cannot be checked.

- evidence: **derived**

**none (illustrative back-transformation)**

```
ASSUMED residual SD on the natural-log scale s = 0.3  ->  mean/median factor exp(s^2/2) = exp(0.045) = 1.046; a naive back-transformed prediction exp(ln a + b ln x) therefore sits 1 - 1/1.046 = 4.4% below the arithmetic mean of y at that x.

```

- value: `1.046`

- Calculated from the lognormal identity, not observed. The bias grows quickly with scatter: at s = 0.6 the factor is exp(0.18) = 1.197. Predicting a mean organ mass or metabolic rate for a design from a log-log fit without this factor underestimates it.

- evidence: **derived**

**Uca pugnax (male major chela vs body)**

- value: `unknown`

- This is Huxley's historical case (the 1924 "heterogonic" work, summarised in the 1932 book). I did not obtain his fitted exponent. One standard web search (2026-11-04) returned secondary histories without the number. I give no value rather than one from memory.

- evidence: **literature**

:::{seealso} Contested
- Kerkhoff & Enquist 2009 (J. Theor. Biol. 257:519-521) argue that log transformation is necessary because biological variation is multiplicative by nature, so multiplicative error is the better probability model.
- Packard 2009 (J. Theor. Biol. 257:515-518, same issue) argues that models should be fitted on the original scale of measurement and that multiplicative variation can be handled by modelling heteroscedasticity in nonlinear fits. Packard returned to the point in 2014 (not read; known only from a search summary). Not reconciled here.
- Mammalian BMR exponent: White & Seymour 2003 find no support for 3/4 and conclude BMR is proportional to M^(2/3). The 3/4 value is the prediction of the West-Brown-Enquist vascular-network model. Kolokotrones et al. 2010 (search summary) report that the WBE model fails their curvature test, and they suggest modifications. That makes the dispute partly about whether a single exponent exists at all. Not reconciled here.
- Huxley and Teissier fixed the notation jointly in 1936 (their form was written y = b x^a, with the letters swapped relative to modern usage). Gayon 2000 (search summary) records a tacit disagreement between them over what the coefficient means. I have not read either text, so the content of that disagreement is not stated here.
- Onthophagus horn scaling: Emlen & Nijhout 2000 treat it as a threshold (sigmoid) reaction norm. A 2006 study (authors not identified in my search; seen only as a search snippet) reports that horn measures that do not confound horn length with head size support positive allometry rather than threshold reprogramming. Not reconciled here.
:::

## Sources

| Citation | Read-level |
|---|---|
| Huxley JS (1932) Problems of Relative Growth. Methuen, London | `search-summary` |
| Huxley JS, Teissier G (1936) Terminology of relative growth. Nature 137:780-781 | `search-summary` |
| Gayon J (2000) History of the concept of allometry. American Zoologist 40(5), beginning p. 748 (end page not checked) | `search-summary` |
| Warton DI, Wright IJ, Falster DS, Westoby M (2006) Bivariate line-fitting methods for allometry. Biological Reviews 81(2):259-291 | `abstract` |
| White CR, Seymour RS (2003) Mammalian basal metabolic rate is proportional to body mass^2/3. PNAS 100(7):4046-4049, PMC153045 | `full-text` |
| Kolokotrones T, Savage V, Deeds EJ, Fontana W (2010) Curvature in metabolic scaling. Nature 464:753-756, doi 10.1038/nature08920 | `search-summary` |
| Kerkhoff AJ, Enquist BJ (2009) Multiplicative by nature: why logarithmic transformation is necessary in allometry. J. Theor. Biol. 257:519-521, doi 10.1016/j.jtbi.2008.12.026 | `search-summary` |
| Packard GC (2009) On the use of logarithmic transformations in allometric research. J. Theor. Biol. 257:515-518 | `search-summary` |
| Emlen DJ, Nijhout HF (2000) The development and evolution of exaggerated morphologies in insects. Annu. Rev. Entomol. 45:661-708 | `search-summary` |


---

*Generated from [`library/laws/allometry-huxley.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/allometry-huxley.yaml). Do not edit this page; edit the YAML.*
