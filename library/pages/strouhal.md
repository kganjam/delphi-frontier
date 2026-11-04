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
| `St` | 1 | dimensionless | Strouhal number; ratio of the lateral (flapping) velocity scale to forward speed |
| `f` | 1/T | Hz | stroke (wingbeat or tail-beat) frequency |
| `A` | L | m | PEAK-TO-PEAK excursion of the trailing edge or wing/tail tip (see definition_note) |
| `U` | L/T | m/s | forward (cruising) speed |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `cruising_band` | 0.3 (interval 0.2 to 0.4) dimensionless | Observed range in which cruising animals cluster and in which propulsive efficiency of oscillating foils "usually peaks" (Taylor et al. 2003, Nature 425:707; abstract-level only -- the per-species values and the sample were NOT read). 0.3 is the band midpoint, written here as a convenience; it is not a reported mean. The interval is the reported band, not a confidence interval. |
| `odontocete_fraction_0.20_0.30` | 0.74 fraction of measured sequences | Rohr & Fish (2004): of 248 Strouhal numbers from six captive odontocete species, 74% fell in 0.20-0.30 versus 55% in the 0.25-0.35 range predicted for maximum efficiency; the authors place the odontocete range about 20% below the predicted optimum. Abstract/search-summary level; a later slide deck by the same authors reports 267 sequences, so the count is not settled here. |
| `larval_zebrafish_St` | 2.5 at Re = 60, falling to 0.72 at Re = 1400 (interval 0.72 to 2.5) dimensionless (peak-to-peak amplitude convention) | Measured (kinematics of 38 near-cyclic swimming events, Danio rerio 2-5 dpf), van Leeuwen, Voesenek & Mueller (2015). Quoted from the full text: "As Re increases (60 -> 1400), St (2.5 -> 0.72) decreases nonlinearly towards values of large swimmers (0.2-0.6)". Every value in this interval lies ABOVE the 0.2-0.4 band. |

## Why it holds

St is the ratio of the lateral speed of the propulsor (order f*A) to the forward speed U; equivalently it sets the angle of the propulsor's path through the fluid and the spacing of the vortices it sheds relative to their size. Why cruising animals sit at 0.2-0.4 is NOT settled, and three explanations are on record (see contested_by): (1) wake-instability tuning -- the band coincides with the frequency of maximal amplification of the reverse von Karman wake behind the animal (the framing associated with Triantafyllou and with Taylor et al. 2003); (2) propulsor drag -- with a drag-free foil efficiency rises monotonically and has no peak, so it is drag on the fin or wing that creates an efficiency peak, and thrust at that peak balances body drag to set cruising speed (Floryan et al. 2018, full text); (3) quasi-steady blade-element reasoning -- below St_lim = 1/(2*LDR) no thrust is possible, and efficiency peaks broadly near St = 0.5, so the observed band sits above the limit and slightly below the optimum (Usherwood 2025, full text; a model, not a measurement). The amplitude term is capped by morphology and by the need to avoid dynamic stall (Floryan et al. 2018), so f is the variable left to set St at a given speed.

## Where it holds

- **regime**: steady cruising (constant-speed, near-cyclic stroke) with lift-based or undulatory propulsion
- **reynolds min**: ~1e3 (lower edge of the 'Re = 10^3-10^5' range over which van Leeuwen et al. 2015 state adult fish and cetacean St is roughly constant at 0.2-0.4)
- **reynolds max**: ~1e5 per the same statement; behaviour above it was not checked in any source read here
- **taxa**: ['cetaceans (odontocetes)', 'sharks', 'bony fish', 'birds', 'bats', 'insects']
- **notes**: The taxon list is the one the Taylor et al. (2003) abstract names; the abstract says the flyers converge on the band "only when cruising". Which insects and how many species were sampled was not read (abstract-level only).


:::{danger} Where it breaks
(1) LOW REYNOLDS NUMBER -- DEMONSTRATED. Larval zebrafish (Danio rerio, 2-5 dpf) swimming at Re = 60-1400 cruise at St = 0.72-2.5, measured (van Leeuwen, Voesenek & Mueller 2015), i.e. 1.8x to 6x the top of the band; St falls toward the band only as Re rises. The authors attribute this to high, mainly viscous drag forcing a large f*A to make thrust. The failure boundary is therefore at roughly Re ~ 1e3: at Re = 1400 the measured St (0.72) is still outside the band. Exactly where below ~1e3-1e4 a given taxon re-enters the band was not measured in any source read here. For this project's subject (larval and juvenile zebrafish, small fins) this is the operative failure: do NOT check a small-fish or small-fin design against 0.2-0.4. (2) NON-CRUISING GAITS. The band is stated for cruising. Taylor et al. (abstract) say flyers converge on it "only when cruising". In hovering U -> 0 so St = f*A/U diverges -- my inference from the definition, not a measured value -- and the number stops being informative; slow, accelerating, turning or burst-and-coast swimming is likewise outside the claim. Fast-start / C-start escapes are not cyclic and St is undefined for them. (3) THE BAND DOES NOT LOCATE THE EFFICIENCY OPTIMUM. Odontocetes cluster at 0.20-0.30 (74% of sequences), about 20% below the 0.25-0.35 predicted optimum (Rohr & Fish 2004, abstract). Tytell et al., as reported by Dabiri (2019; Tytell not read directly), found similar St values can carry power coefficients differing by a factor of three, so St alone does not fix energetic efficiency once internal (muscle/body-stiffness) losses are included. And the location of the efficiency peak is drag- and Re-dependent (Floryan 2018) and lift-to-drag-dependent (Usherwood 2025, modelled). (4) CONVENTION ERRORS. A half-amplitude A substituted into f*A/U, or a peak-to-peak A into 2*f*A/U, shifts St by a factor of two (see definition_note); a reported out-of-band value should be checked for this before it is believed.
:::

## Worked examples

**hypothetical robotic caudal fin (illustrative inputs, NOT measurements)**

```
f = 2 Hz, A = 0.05 m peak-to-peak, U = 0.4 m/s  ->  St = 2 * 0.05 / 0.4 = 0.25
```

- value: `0.25`

- Calculated from made-up inputs to show the check. Inside the band; per where_it_breaks (3) that shows the kinematics resemble cruising animals, not that the fin is efficient. Check the Re before using the band at all: with a 0.1 m body in water at 20 C, Re = U*L/nu = 0.4*0.1/1.004e-6 = 4.0e4 (calculated; nu from reynolds.yaml), inside the stated ~1e3-1e5 range.

- evidence: **derived**

**Danio rerio larvae, 2-5 dpf, cyclic swimming**

- value range: `[0.72, 2.5]`

- Measured, van Leeuwen et al. (2015): St = 2.5 at Re = 60 and 0.72 at Re = 1400 (peak-to-peak amplitude). Entirely above the band; the low-Re failure in where_it_breaks (1).

- evidence: **literature**

**odontocete cetaceans (six captive species)**

- value range: `[0.2, 0.3]`

- Rohr & Fish (2004): 74% of 248 measured St values fell in 0.20-0.30 (abstract-level). The value_range is the range holding that 74%, not the full spread, which was not read.

- evidence: **literature**

:::{seealso} Contested
- Floryan, Van Buren & Smits (2018): the St range for peak efficiency is 'largely determined by fluid drag on the fins and wings'; the optimal St decreases as Re increases until the drag constant becomes constant. They do NOT explicitly reject Taylor et al.; they explicitly reject the claim (attributed to Gazzola et al.) that thrust-drag balance alone yields a constant St, and call wake-resonance amplification possibly 'a signature of the efficient production of net thrust, but this is purely speculative'.
- Usherwood (2025): quasi-steady model puts the efficiency optimum near St = 0.5 (0.552 at LDR = 10) with a thrust limit St_lim = 1/(2*LDR); observed animals sit 'above the predicted limiting St, but rarely above those predicted to maximize mechanical efficiency', and the reverse von Karman wake is treated as 'an epiphenomenon or corollary'. This places the band BELOW the optimum, where Taylor et al. read it as AT the optimum. Model result, not measurement. The paper does not name Taylor et al. as wrong; the tension is my reading.
- Dabiri (2019, review): the match between kinematic St and the St of maximal wake-instability growth comes from a LINEAR stability analysis of a base flow that 'strictly speaking ... does not actually exist', so the correspondence 'may be a numerical coincidence'; he also asks 'whether the Strouhal number is indeed the appropriate organizing concept'.
- Rohr & Fish (2004): odontocetes mostly cruise at 0.20-0.30, below the 0.25-0.35 predicted efficiency optimum, and 'fluke kinematics are not determined by Strouhal number alone' (abstract paraphrase via search summary).
- Band width itself: van Leeuwen et al. (2015) give the large-swimmer range as 0.2-0.6 in their abstract and 0.2-0.4 in their discussion. Left unreconciled.
:::

## Sources

| Citation | Read-level |
|---|---|
| Taylor GK, Nudds RL, Thomas ALR (2003) Flying and swimming animals cruise at a Strouhal number tuned for high power efficiency. Nature 425:707-711. doi:10.1038/nature02000 | `abstract` |
| van Leeuwen JL, Voesenek CJ, Mueller UK (2015) How body torque and Strouhal number change with swimming speed and developmental stage in larval zebrafish. J R Soc Interface 12(110):20150479. PMID 26269230; PMC4614456 | `full-text` |
| Floryan D, Van Buren T, Smits AJ (2018) Efficient cruising for swimming and flying animals is dictated by fluid drag. PNAS 115(32):8116-8118. doi:10.1073/pnas.1805941115; PMC6094110 | `full-text` |
| Usherwood JR (2025) Limiting and optimal Strouhal numbers or tip speed ratios for cruising propulsion by fins, flukes, wings and propellers. J R Soc Interface 22(222):20240730. doi:10.1098/rsif.2024.0730; PMC11750378 | `full-text` |
| Rohr JJ, Fish FE (2004) Strouhal numbers and optimization of swimming by odontocete cetaceans. J Exp Biol 207(10):1633-1642. doi:10.1242/jeb.00948 | `search-summary` |
| Dabiri JO (2019) Landmarks and frontiers in biological fluid dynamics. arXiv:1904.13013v2 [physics.flu-dyn] | `full-text` |
| Gazzola M, Argentina M, Mahadevan L (2014) Scaling macroscopic aquatic locomotion. Nature Physics 10:758-761 | `listing` |


---

*Generated from [`library/laws/strouhal.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/strouhal.yaml). Do not edit this page; edit the YAML.*
