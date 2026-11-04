---
title: Strouhal number and the 0.2-0.4 cruising band of swimming and flying animals
label: law-strouhal
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-strouhal
\mathrm{St} = \frac{f A}{U}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `St` | 1 | dimensionless | Strouhal number; ratio of the lateral (or vertical) tail/wing-tip speed scale to forward speed |
| `f` | 1/T | Hz | tail-beat or wingbeat frequency |
| `A` | L | m | PEAK-TO-PEAK excursion of the tail tip or wake width (Eloy 2012 and van Leeuwen et al. 2015 state peak-to-peak; the Taylor et al. 2003 convention was not checked; some studies use semi-amplitude, which halves St) |
| `U` | L/T | m/s | mean forward (cruising) speed |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `cruising_band` | 0.3 (interval 0.2 to 0.4) dimensionless | The band claimed by Taylor, Nudds & Thomas 2003 (Nature 425:707): propulsive efficiency is high over a narrow range of St and usually peaks in 0.2 < St < 0.4, and dolphins, sharks, bony fish, birds, bats and insects cruise inside it. Read at search-summary level only; the number of species and the per-species values in that paper were NOT retrieved and are not stated here. The midpoint 0.3 is my placeholder for the value field, not a measured optimum. |
| `foil_optimum_band` | 0.3 (interval 0.25 to 0.35) dimensionless | Triantafyllou, Triantafyllou & Grosenbaugh 1993: the frequency of maximum spatial amplification of the reverse-Karman jet behind an oscillating foil, as a Strouhal number, falls in 0.25-0.35 (peak reported near 0.30 in secondary summaries). This is a STABILITY-ANALYSIS AND FOIL-EXPERIMENT result, not an animal measurement. Read at search-summary level. |
| `odontocete_observed` | unknown (interval 0.2 to 0.3) dimensionless | MEASURED, Rohr & Fish 2004 (J Exp Biol 207:1633): 248 St values from six captive odontocete species; 74 per cent fell in 0.20-0.30, against 55 per cent in the 0.25-0.35 band predicted for maximum efficiency. The authors place the cetacean optimum slightly LOWER than the foil prediction. The interval here is the band holding 74 per cent of their data, not a confidence interval. Read at search-summary level; the mean and the speed dependence were not retrieved. |
| `eloy_optimum_vs_lighthill` | unknown (interval 0.15 to 0.8) dimensionless | CALCULATED, not observed: Eloy 2012, from Lighthill elongated-body theory, predicts the optimal St rises with the Lighthill number Li (drag-to-available-thrust ratio) from 0.15 for the largest cetaceans to 0.8 for the smallest animals in his set, approximated by St_opt ~ 0.75 Li^(1/3). Eloy reports more than 85 per cent of his 53-species data inside his acceptable range (Froude efficiency within 0.1 of the optimum). So in this model the 0.2-0.4 band is the large-animal portion of a size-dependent curve, not a universal constant. |
| `eloy_table_outside_band` | 18 rows of 66 | MY COUNT, from the 66 kinematic rows (53 species) of Eloy 2012 tables 1-3 (arXiv 1102.0223v1, extracted with pdftotext): 18 of 66 rows have St outside 0.2-0.4, and ALL 18 are ABOVE 0.4 (none below 0.2; the lowest is 0.21, kawakawa tuna). The 18 are dominated by elongate or anguilliform bodies, amphibians and small fish: e.g. European eel 0.48 and 0.52, hagfish 0.56, axolotl 0.57, longnose gar 0.59, green frog tadpole 0.60, medicinal leech 0.63, West African lungfish 0.75 and 1.02, saltwater crocodile 0.78, bullfrog tadpole 0.79, fantail and eggfish goldfish (L about 5 cm, Re about 7e3) 0.47 and 0.54. This is a count over a literature compilation, not a sample of nature, and Eloy excluded larvae and snakes from it. |
| `larval_zebrafish_observed` | unknown (interval 0.72 to 2.5) dimensionless | MEASURED, van Leeuwen, Voesenek & Muller 2015 (J R Soc Interface 12:20150479), larval Danio rerio 2-5 dpf, peak-to-peak amplitude: as Re rises from about 60 to 1400, St falls nonlinearly from about 2.5 to 0.72. Even the fastest larvae are well above 0.4. |

## Why it holds

Two distinct arguments are made for why animals cruise near St 0.2-0.4, and they should not be merged. (a) WAKE STABILITY (Triantafyllou et al. 1993): an oscillating foil produces thrust through a jet-like mean wake that forms a reverse Karman street; linear stability analysis of that jet gives maximum spatial amplification at St 0.25-0.35, and foil experiments show peak efficiency in about the same range. Taylor et al. 2003 argue selection for efficiency should therefore tune cruise kinematics into that band. (b) ELONGATED-BODY OPTIMISATION (Eloy 2012): maximising Froude efficiency under the constraint thrust = drag gives an optimal St that depends on a single number, the Lighthill number Li (body drag over available reactive thrust); for large, streamlined, low-drag animals this optimum lands near 0.15-0.3. Under (b) the band is a CONSEQUENCE of low relative drag, which is why it shifts upward for draggy, elongate or small bodies. Physically St is the ratio of the lateral tail-tip speed scale (f*A) to forward speed U, so it also sets the angle of attack of the propulsor.

## Where it holds

- **regime**: inertial, Reynolds number roughly 1e4 and above
- **gait**: steady cruising (not accelerating, not hovering, not fast-start)
- **taxa**: ['cetaceans', 'sharks', 'scombrids and most carangiform/thunniform fish', 'birds, bats and insects in forward cruising flight (Taylor et al. 2003, search-summary only)']
- **amplitude convention**: peak-to-peak
- **notes**: Lowest Re in Eloy 2012 tables is 7.0e3 to 7.7e3 (two goldfish varieties and one lungfish row), and those rows are OUTSIDE the band; I found no compilation that tests the band with adult animals below that. The roughly-1e4 boundary is my inference from where Eloy's data and the larval data diverge, not a threshold any source states.

:::{danger} Where it breaks
MEASURED FAILURE 1 -- LOW REYNOLDS NUMBER. Larval zebrafish (van Leeuwen et al. 2015) cruise at St 2.5 at Re about 60, falling only to 0.72 at Re about 1400: a factor of 2 to 6 above the band, peak-to-peak convention, measured. Voesenek et al. 2018 define the intermediate regime as 1 <~ Re <~ 2000 and state that animals there operate at higher St than the inertial optimum. The authors attribute this to relatively high, mainly viscous drag, which demands a high f*A product. Consistent with this, Gazzola et al. 2014 find swimming speed scales as Re ~ Sw^(4/3) in the laminar regime but Re ~ Sw in the turbulent regime, where Sw = omega*A*L/nu; since St is proportional to Sw/Re, St is approximately constant only in the turbulent branch (this St corollary is MY derivation from their stated scaling; I read the paper only at search-summary level and did not confirm they state it). MEASURED FAILURE 2 -- ELONGATE, ANGUILLIFORM AND HIGH-DRAG BODIES at moderate Re. In Eloy 2012's compilation (my count, see constants) 18 of 66 rows lie above 0.4 and none below 0.2: eels 0.48-0.52, hagfish 0.56, gar 0.59, lungfish 0.75 and 1.02, crocodile 0.78, tadpoles 0.60 and 0.79, leech 0.63. Eloy's model predicts this upward shift (optimum up to 0.8 at high Lighthill number), so these are failures of the 0.2-0.4 band, not necessarily of efficiency tuning. FAILURE 3 -- NON-CRUISING GAITS. St is undefined in hovering (U -> 0 sends St to infinity), and Taylor et al. 2003 restrict the flying-animal claim to cruising; fast-starts, accelerations and slow flight are outside the claim. FAILURE 4 -- CONVENTION. A semi-amplitude St is half the peak-to-peak one, so 0.3 peak-to-peak reads 0.15 and appears to fall out of the band; any comparison across sources must first fix the convention. FAILURE 5 -- ST IS NOT SUFFICIENT EVEN IN-BAND. Saadat et al. 2017 argue (search-summary level) that St alone does not secure optimal swimming and that a separate condition on amplitude-to-length ratio A/L is also needed; Rohr & Fish 2004 likewise conclude fluke kinematics depend on more than St. For an engineer: the band is a check on a LARGE, STREAMLINED cruiser only; for anything centimetre-scale or smaller in water, or elongate, expect required St above 0.4 and do not size a propulsor to St 0.3.
:::

## Worked examples

**Tursiops truncatus (bottlenose dolphin)**

- value: `0.26`

- Eloy 2012 table 1, compiled from the literature (L 258 cm, Re 1.2e7, Li 0.063). Inside the band; the canonical case.

- evidence: **literature**

**larval Danio rerio, 4-5 dpf, consistency check on reported values**

```
U = f * A / St, using the reported maxima f = 95 Hz, A = 2.4 mm (peak-to-peak), St = 0.72
  U = 95 * 0.0024 / 0.72 = 0.317 m/s
```

- value: `0.317`

- CALCULATED by me from three values in the van Leeuwen et al. 2015 abstract; it agrees with the paper's stated top speed of nearly 0.30 m/s, so the reported numbers are mutually consistent. Caveat: the maximum f and maximum A need not come from the same bout. Had a designer assumed St = 0.3 at the same f and A, the predicted speed would be 0.76 m/s -- a 2.4-fold overestimate, which is the size of the error the band introduces at Re ~ 1e3.

- evidence: **derived**

**hypothetical 3 cm fish-scale swimmer at 2 body lengths per second (design check)**

```
L = 0.03 m, U = 0.06 m/s, A = 0.2 L = 0.006 m (ASSUMED, peak-to-peak)
  Re = U*L/nu = 0.06*0.03/1.0e-6 = 1800
  f required at St 0.3 = 0.3*0.06/0.006 = 3.0 Hz
  f required at St 0.72 = 0.72*0.06/0.006 = 7.2 Hz
```

- value: `3.0`

- CALCULATED, all inputs assumed. Re 1800 is below every row in Eloy's compilation and inside the larval zebrafish range, so the 0.2-0.4 band is NOT validated here; borrowing the larval St at similar Re (0.72) more than doubles the required frequency. Neither number is a measurement of any animal. Which St applies at this Re for an adult-shaped body is unknown.

- evidence: **derived**

**amplitude-convention trap**

```
St_peak_to_peak = 0.30  ->  St_semi_amplitude = 0.30 / 2 = 0.15
```

- value: `0.15`

- Same animal, same motion. A source quoting 0.15 may be inside the band; check the convention before calling it an outlier.

- evidence: **derived**

:::{seealso} Contested
- WHY THE BAND EXISTS IS CONTESTED. Taylor et al. 2003 and Triantafyllou et al. 1993 attribute it to wake-instability tuning for efficiency. Eloy 2012 argues the optimum is not a constant but a function of the Lighthill number (0.15 to 0.8), so the band is the large-animal end of a size/drag-dependent curve. Dabiri 2019 (search-summary level) notes the band coincides with maximal growth of linear perturbations of a jet and suggests the correspondence may be a numerical coincidence. These are not reconciled here.
- WHERE CETACEANS SIT. Rohr & Fish 2004 find 74 per cent of odontocete values in 0.20-0.30 and place the optimum slightly below the foil prediction of 0.25-0.35; Eloy 2012's model places the large-cetacean optimum lower still (about 0.15) while listing measured cetacean values of 0.24-0.35 in his own table.
- WHETHER ST IS THE RIGHT CONTROL VARIABLE. Saadat et al. 2017 (search-summary level) argue St alone is insufficient and an amplitude condition on A/L is also needed, and that a minimal-power cruising St is predetermined by body shape and drag. The A/L range they give differs between sources seen: 0.1-0.3 in the published abstract and synopsis vs 0.15-0.25 in a 2017 APS conference abstract. Both are recorded; the full text was not read.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taylor GK, Nudds RL, Thomas ALR (2003) Nature 425:707-711, Flying and swimming animals cruise at a Strouhal number tuned for high power efficiency, doi 10.1038/nature02000 | `search-summary` |
| Triantafyllou GS, Triantafyllou MS, Grosenbaugh MA (1993) J Fluids Struct 7:205-224, Optimal thrust development in oscillating foils with application to fish propulsion | `search-summary` |
| Rohr JJ, Fish FE (2004) J Exp Biol 207:1633-1642, Strouhal numbers and optimization of swimming by odontocete cetaceans, doi 10.1242/jeb.00948 | `search-summary` |
| Eloy C (2012) J Fluids Struct 30:205-218, Optimal Strouhal number for swimming animals, doi 10.1016/j.jfluidstructs.2012.02.008 | `full-text-preprint` |
| van Leeuwen JL, Voesenek CJ, Muller UK (2015) J R Soc Interface 12:20150479, How body torque and Strouhal number change with swimming speed and developmental stage in larval zebrafish, doi 10.1098/rsif.2015.0479, PMC4614456 | `full-text` |
| Voesenek CJ, Muijres FT, van Leeuwen JL (2018) J Exp Biol 221:jeb149583, Biomechanics of swimming in developing larval fish, doi 10.1242/jeb.149583 | `full-text` |
| Gazzola M, Argentina M, Mahadevan L (2014) Nature Phys 10:758-761, Scaling macroscopic aquatic locomotion, doi 10.1038/nphys3078 | `search-summary` |
| Saadat M, Fish FE, Domel AG, Di Santo V, Lauder GV, Haj-Hariri H (2017) Phys Rev Fluids 2:083102, On the rules for aquatic locomotion, doi 10.1103/PhysRevFluids.2.083102 | `search-summary` |
| Dabiri JO (2019) Phys Rev Fluids 4:110501, Landmarks and frontiers in biological fluid dynamics, doi 10.1103/PhysRevFluids.4.110501 | `search-summary` |


---

*Generated from [`library/laws/strouhal.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/strouhal.yaml). Do not edit this page; edit the YAML.*
