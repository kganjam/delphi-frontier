# Claim 192: what it requires at the organ and behaviour scales

**Source claim.** S28, `docs/research/fish/S28-organism.md`, branch `origin/claude/s28-organism-design-5z0vjz`.
Scale: organism. Evidence: derived.

> A 3x leap would require a 2.39 m/s exit, 1.73x the measured maximum. Flight requires 4.37 m/s: 3.2x the
> speed and 10x the kinetic energy.

**Subject of the claim.** Adult zebrafish, *Danio rerio*: the existing Daane et al. 2021 *lof/+ ; lat4a/+*
double heterozygote, which for leaping is a wild-type body.

**What the claim rests on:**
- **One measured input.** 1.38 m/s is called the "measured maximum" adult burst speed. S28 attributes it to
  Miln et al. 2021.
- **One project-derived input.** 4.37 m/s is the take-off speed for a 0.25 g fish with a 192 mm², AR-5
  pectoral surface at CL_max 1.07.
- **Vacuum ballistics.** Range is proportional to V², so 3× range needs √3 × V.

**Prior work.**
- Challenge 192 (`origin/claude/challenge-claim-192-7ss3xi`) re-derived the arithmetic and returned SURVIVED.
  I do not repeat that.
- An earlier entailment draft exists on `origin/claude/claim-192-entail-2ctr6q`. I read it, then fetched and
  read every source used below myself in this session. Where I quote a number, I read it myself; nothing is
  carried over unchecked.

**Labels used in every sentence that needs one:**
- **measured**: reported by the cited authors from experiments.
- **calculated**: arithmetic I did in this session. It is not an observation.
- **author's claim / my inference**: kept apart wherever both appear.

## Sources and read-levels

| Source | Animal | Used for | Read-level |
|---|---|---|---|
| Miln C, Ward AJW & Seebacher F 2021, *R Soc Open Sci* 8:210146, doi 10.1098/rsos.210146, PMC8025299 | adult *D. rerio* (short-fin, commercial) | method behind the 1.38 m/s value | **full-text** (Europe PMC XML, fetched this session). Figures and supplementary data were **not** read |
| Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, doi 10.1371/journal.pbio.3003484, PMC12604801 | adult *D. rerio*, 4–12 months, 2.6–3.6 cm BL | adult maximal escape speed | **full-text** (Europe PMC XML, fetched this session); quotes are verbatim |
| Wakeling JM & Johnston IA 1998, *J Exp Biol* 201:1505, doi 10.1242/jeb.201.10.1505 | six marine teleosts, **no *Danio*** | whether fast-starts are limited by muscle power | **abstract** |
| Bai R et al. 2026, *Behav Brain Res*, doi 10.1016/j.bbr.2026.116414 | adult *D. rerio* | terrestrial (out-of-water) jumping exists as a behaviour | **abstract** |
| "The Strategy of Predator Evasion in Response to a Visual Looming Stimulus in Zebrafish (*Danio rerio*)", *Integr Org Biol* 2020 (authors not recorded here), doi 10.1093/iob/obaa023, PMC7750966 | *D. rerio* | checked for a peak escape speed | **full-text**; gives only a "mean escape speed … v = 3.7 cm s⁻¹", which is not a peak value and is not used |
| Gibb AC et al. 2011, *J Exp Zool A* (zebrafish land jumps) | *D. rerio* | — | **search-summary** only; not used for any number |

---

## Behaviour scale

### B1 (range). The fastest measured adult zebrafish escape or burst must be about 1.38 m/s. **UNSATISFIABLE as stated**

**What the claim requires.**
- The ratios 3.2× and 10× are 4.37/1.38 and (4.37/1.38)² (calculated: 3.167 and 10.03).
- They hold only if 1.38 m/s really is the highest speed adult zebrafish reach in a maximal escape.
- Put as a bound: v_max ≤ 1.38 m/s.

**The animal on each side.**
- **The claim:** adult *Danio rerio*.
- **The contradicting measurement:** adult *Danio rerio* control fish, scn4aa⁺/⁺; scn4ab⁺/⁺ siblings "from the
  same laying", aged 4–12 months, body length 2.6–3.6 cm (Demesmay 2025, Methods).
- Both sides are the same species, life stage and behaviour (startle-evoked fast-start). **This is not a
  flying-fish number.**

**Measurement (Demesmay 2025, full-text, verbatim).**
- Speed: "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants) and latency
  to attain maximal speed (8 ± 4 ms for controls and 9 ± 3 ms for mutants)".
- Video: escape responses were recorded "at … 240 frames/s (escape response, 1 s long videos)".
- Stimulus: "Two similar objects (1 g) placed at approximately 30 cm above the water were simultaneously
  dropped". Tanks were 1.6 L with 3–4 fish each. Tracking was done in Fiji.

So the **mean** maximal speed of adult control zebrafish, 1.57 m/s, already exceeds the value the claim calls
the **maximum**. If the distribution is roughly normal (my assumption), a fish 1 SD above the mean reaches
1.84 m/s (calculated).

**Where the 1.38 m/s comes from, checked.**
- Miln et al. 2021 (full-text) describe their method:
  - escape responses "induced by a mechanical stimulus to the tail";
  - recorded in "a shallow tank (405 × 600 mm, 30 mm water depth)";
  - filmed "at 120 frames s⁻¹";
  - "four escape responses were analysed for each fish and the fastest speed was used".
- **The numbers 1.38 and 0.45 m/s do not appear anywhere in the article text.** The only speeds in the text are
  0.05 m s⁻¹ (the flume step) and 0.19 m s⁻¹ (the day-1 to day-7 gain in realized speed).
- The range S28 quotes must therefore come from Fig. 1a or the supplementary data. I read neither. **Its
  provenance is unverified by me**, though I have no reason to think it is wrong.

**The disagreement, kept as it is.** The two studies differ in method, and I do not average them:

| | Miln 2021 | Demesmay 2025 |
|---|---|---|
| Frame rate | 120 fps | 240 fps |
| Stimulus | tail touch | object dropped into the tank |
| Water depth / volume | 30 mm water depth | 1.6 L tanks |
| Maximum | fastest of 4 escapes per fish | n ≈ 20 per group |

- **My inference, a calculated plausibility argument and not a finding of either paper.** Demesmay report peak
  speed is reached 8 ± 4 ms after onset.
  - At 120 fps the frame interval is 8.3 ms, so a speed from two frames averages over most or all of the
    acceleration and would read low.
  - At 240 fps (4.2 ms) the peak rests on about two frames. Manual digitisation then risks reading high.
  - Both biases are plausible, and I cannot test either without per-frame data.
  - The direction of the first bias suggests the 1.38 m/s "maximum" is partly a sampling artefact.
- Demesmay's own distance figure is consistent with their peak. Their "3.8 ± 0.8 cm" covered in 40 ms is a
  mean of 0.95 m/s over the first 40 ms, including the C-bend (calculated). That is compatible with a peak
  near 1.6 m/s.

**Consequences (calculated) from the measured 1.57 m/s control mean.**
- Flight needs 4.37/1.57 = **2.78×** the speed and **7.7×** the kinetic energy, not 3.2× and 10×.
- The 1.73× figure for a 3× leap is √3. It is independent of the baseline and stands. The absolute 2.39 m/s
  does not: a 3× leap over a 1.57 m/s baseline needs **2.72 m/s**.

**Why the verdict is unsatisfiable:**
- The claim states a maximum of 1.38 m/s.
- A measured mean in the same species, life stage and behaviour exceeds it.
- So "3.2× the speed and 10× the kinetic energy … the measured maximum" is refuted from below as a numerical
  statement.

**What this does not refute.** It does not refute the qualitative conclusion that flight is out of reach. The
corrected deficit (2.8× speed, 7.7× KE) is still large; see B3.

### B2 (existence). A water-exit leap must exist in adult *Danio*, with its exit speed measured or bounded by burst speed. **UNSATISFIED: nobody appears to have measured it**

**What the claim requires.**
- The "3× leap" is a multiple of a wild-type *aerial* leap from water. S28 computes that leap as 19.4 cm from
  a 1.38 m/s exit.
- For that, adult zebrafish must perform water-exit leaps.
- Swimming burst speed must also be an upper bound on exit speed, which is S28's argument that crossing the
  surface costs momentum.

**What I found.**
- **Terrestrial jumping only.** Bai et al. 2026 (abstract) describe a "terrestrial jumping assay for adult
  zebrafish". In it, fish placed out of water perform "escape-like jumps".
  - That is take-off from a substrate, not exit from water. The abstract gives no speed or distance.
- **Water-exit jumping: none.**
  - **Search:** a WebSearch for "zebrafish adult jump out of water leap height water exit speed high-speed
    video".
  - **Result:** no zebrafish water-exit study. The hits were the terrestrial-jumping literature, a general
    water-exit scaling paper (H/L ~ Fr², with the authors noting exit velocity was not directly measured), and
    archer fish.
  - **Animals, kept apart:** the archer-fish exit speeds (about 2 m/s in a press summary, *Toxotes*) and the
    flying-fish 5 g take-off (*Exocoetidae*, APS DFD 2013 listing) are **not zebrafish**. I do not use them for
    any verdict.
- **Europe PMC search:** `(zebrafish OR "Danio rerio") AND (TITLE_ABS:jump OR jumping OR leap OR leaping) AND
  adult`. 58 hits; I inspected the top 15. The only relevant hit was Bai 2026 (terrestrial).

**Scope of the negative.**
- Covered: one WebSearch and one Europe PMC query, top-ranked hits only. Not searched: Google Scholar, Web of
  Science, Gibb 2011 in full.
- I found no study that *looked* for zebrafish water-exit leaps and reported their absence or failure.
- **This is "nobody appears to have measured it", not "people looked and found nothing".**

**Consequence.**
- The claim's 3× leap figure is a multiple of a leap that is computed, not observed.
- The burst-to-exit proxy cannot be checked.

### B3 (range). No adult zebrafish may reach the take-off speed in any measured locomotion: attainable speed < 4.37 m/s. **SATISFIED**

**What the claim requires.**
- "Flight requires 4.37 m/s" is offered as out of reach.
- For that, measured adult *Danio* speeds must lie well below 4.37 m/s.

**The animal on each side.** Adult *D. rerio* for the claim, and adult *D. rerio* in both measurements.

**Measured.**
- Demesmay 2025: control mean 1.57 ± 0.27 m/s; scn4a double-null mean 1.61 ± 0.33 m/s.
- Miln 2021: maxima as S28 relays them. As noted in B1, I could not locate the values in the text.

**Calculated.**
- 4.37 m/s lies (4.37 − 1.57)/0.27 = **10.4 SD** above the control mean.
- Even the control mean + 3 SD (2.38 m/s) is 54 % of 4.37.

**Scope.** Two studies. Demesmay's per-fish values (supplementary data) were not read, so an individual outlier
is unreported, not excluded. No conceivable outlier within the reported spread approaches 4.37 m/s.

---

## Organ scale

### O1 (energetic). The axial fast muscle must already be near its power limit in a maximal escape, with no reserve of about 3× for a 3× leap or about 10× for flight. **OPEN: supported in other teleosts, untested in *Danio***

**What the claim requires.**
- The claim treats the measured burst as a ceiling. That is physical only if the propulsive organ is
  power-limited, rather than limited by motivation, stimulus or tank geometry.
  - Miln 2021 used 30 mm water depth. Demesmay 2025 dropped a 1 g object.
- Kinetic energy per unit body mass (calculated):
  - 0.95 J kg⁻¹ at 1.38 m/s;
  - 2.86 J kg⁻¹ at 2.39 m/s;
  - 9.55 J kg⁻¹ at 4.37 m/s.
- At fixed fast-start duration and efficiency, mean muscle power must therefore rise about 3.0× for the 3× leap
  and about 10× for flight (calculated, v² scaling).

**The animal on each side.**
- **The claim:** *Danio rerio*.
- **The evidence (Wakeling & Johnston 1998, abstract):** *Notothenia coriiceps*, *N. rossii*, *Myoxocephalus
  scorpius*, *Scorpaena notata*, *Serranus cabrilla* and *Paracirrhites forsteri*. **No cyprinid. No *Danio*.**

**Evidence (author's claim, abstract).**
- "At all temperatures, the predicted mean muscle-mass-specific power outputs, as calculated from swimming
  sequences, were similar to the muscle power outputs measured from work-loop experiments".
- *Sc. notata* fast fibres gave "142.7 W kg⁻¹ at 20 degrees C".
- The title states the conclusion: "Muscle power output limits fast-start performance in fish".

**Why it stays open.**
- Extending this to zebrafish is **my inference**, not a measurement.
- **Searches for a *Danio* measurement:**
  - Europe PMC `(zebrafish OR "Danio rerio") AND adult AND ("work loop" OR "work-loop") AND muscle` gave 11
    hits. None is an adult zebrafish fast-muscle work loop; the closest is a larval axial-strain paper, JEB
    2026.
  - A WebSearch for "adult zebrafish fast muscle work loop power output W/kg" returned only larval values. One
    larval work-loop study is reported as about 134 W kg⁻¹ at 80 Hz (search-summary only).
- The adult *Danio* white-muscle mass fraction is **unknown**; I did not find it.
- This is a cross-species prior, so the status is `open`, not `satisfied`.

### O2 (spatial). A paired lifting surface of at least about 192 mm² (span about 1 SL, AR about 5) must exist on a 0.25 g fish for take-off speed to be as low as 4.37 m/s. **UNSATISFIED: never measured, nothing found**

**What the claim requires.**
- 4.37 m/s is not a property of a wild-type fish. It needs S ≈ 192 mm², i.e. a wing loading of 12.5 N m⁻²
  (S28's figure).
- A smaller area raises V_to. S28's own cases give 5.47 m/s at 125 mm² and 8.10 m/s at 57 mm²; I did not
  re-derive these.

**Search.**
- A WebSearch for "adult zebrafish pectoral fin surface area mm2 measured" turned up imaging and developmental
  papers (Paulissen 2022, Dokmegang 2021, Thorsen & Hale 2005, van Eeden 1996). As summarised, none gives an
  adult pectoral fin area. I did not open them in full.
- Daane et al. 2021 Fig. 4B, which reports length/SL rather than area, was not read.

**Scope.** One WebSearch, summaries only. I found no measured area, wild-type or mutant. This is "not measured as
far as I found". Nothing measured contradicts 192 mm², so it is not unsatisfiable.

**Direction of the effect.** If the true area is smaller, the claim's 4.37 m/s is too low and the flight deficit
is larger. A violation here falsifies the exact number while strengthening the conclusion.

---

## Summary

| # | Scale | Kind | Status | One line |
|---|---|---|---|---|
| B1 | behaviour | range | **unsatisfiable** | The measured adult zebrafish control mean of 1.57 ± 0.27 m/s (Demesmay 2025) exceeds the claimed 1.38 m/s maximum. Same species, so a true contradiction. Corrected deficit (calculated): 2.78× speed, 7.7× KE; the 3× leap needs 2.72 m/s |
| B2 | behaviour | existence | unsatisfied | No zebrafish water-exit leap or exit speed is measured. Only terrestrial jumping is documented. Nobody appears to have looked |
| B3 | behaviour | range | satisfied | All measured adult zebrafish speeds are ≤ about 1.6 m/s mean; 4.37 m/s is 10 SD above |
| O1 | organ | energetic | open | Fast-starts are power-limited in six marine teleosts; not tested in *Danio* |
| O2 | organ | spatial | unsatisfied | A 192 mm² pectoral surface has never been measured; a smaller one worsens the deficit |

**Net effect on claim 192.**
- **Refuted from below:** the figures "3.2× the speed and 10× the kinetic energy" and "2.39 m/s". The baseline
  "measured maximum" of 1.38 m/s is below a measured *mean* for the same animal.
- **Standing:** √3 = 1.73× and the qualitative conclusion. Flight remains about 2.8× out of reach in speed.
- **Weakest support:** B2. The behaviour the 3× leap is a multiple of has not been observed in this species.

```swarm-entail
{"source_claim": 192, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The fastest measured adult escape/burst speed of the claimed animal must be about the stated maximum, so that the flight ratios v_to/v_max = 3.2x and (v_to/v_max)^2 = 10x hold",
      "quantity": "maximum measured adult Danio rerio fast-start (escape) speed", "lo": null, "hi": 1.38, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by a same-species measurement: Demesmay et al. 2025 report adult Danio rerio control (scn4aa+/+;scn4ab+/+ sibling) maximal escape speed 157 +/- 27 cm/s (mean +/- SD, 4-12 month adults, BL 2.6-3.6 cm). A population MEAN above the claimed MAXIMUM. Recomputed (calculated): flight needs 2.78x speed and 7.7x KE; the 3x leap ratio sqrt(3)=1.73x stands but its absolute speed becomes 2.72 m/s",
      "satisfied_evidence": "measured",
      "note": "Demesmay L et al. 2025 PLoS Biol 23(11):e3003484, PMC12604801, full-text (240 fps phone camera, dropped 1 g object, 1.6 L tanks, Fiji tracking). Disagrees with Miln, Ward & Seebacher 2021 R Soc Open Sci 8:210146, PMC8025299, full-text read: method is fastest of 4 tail-touch escapes at 120 fps in 30 mm water depth, but the values 0.45/1.38 m/s do not appear in the article text (figures and supplementary not read), so their provenance is unverified by me. My inference, not either paper's: peak speed is reached in 8 +/- 4 ms, so 120 fps (8.3 ms frames) would under-read the peak, while ~2-frame peaks at 240 fps risk over-reading. Both animals are adult D. rerio, so this is not a cross-species comparison. The qualitative flight deficit is not refuted."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "An aquatic water-exit leap must exist in adult Danio with a measured exit speed (defining the 1x leap baseline and validating swimming burst speed as an upper bound on exit speed)",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Not found. Only terrestrial (out-of-water, substrate) jumping is documented for adult D. rerio (Bai et al. 2026 Behav Brain Res, doi 10.1016/j.bbr.2026.116414, abstract; no speeds given). No measured water-exit speed or aerial leap height located for Danio",
      "satisfied_evidence": "unknown",
      "note": "Searches: WebSearch 'zebrafish adult jump out of water leap height water exit speed high-speed video' (hits were terrestrial-jump work, a general H/L~Fr^2 water-exit paper, archer fish Toxotes, flying fish Exocoetidae -- none zebrafish, none used); Europe PMC '(zebrafish OR \"Danio rerio\") AND (TITLE_ABS:jump OR jumping OR leap OR leaping) AND adult' 58 hits, top 15 inspected. Shallow scope (no Google Scholar / Web of Science; Gibb et al. 2011 seen only as search summary). No study found that looked and failed: 'nobody appears to have measured it', not 'looked and found nothing'."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Measured attainable speed of the adult animal must lie below the take-off speed, so that flight is out of reach",
      "quantity": "attainable adult Danio rerio locomotor speed", "lo": null, "hi": 4.37, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Demesmay 2025 adult control maximal escape speed 1.57 +/- 0.27 m/s (mean +/- SD; mutants 1.61 +/- 0.33), same species; 4.37 m/s is 10.4 SD above the control mean and mean+3SD = 2.38 m/s (calculated, normality assumed)",
      "satisfied_evidence": "measured",
      "note": "Demesmay L et al. 2025 PLoS Biol, PMC12604801, full-text; Miln et al. 2021 PMC8025299 full-text (method only, values not located in text). Scope: two studies; Demesmay per-fish supplementary values not read, so an outlier is unreported rather than excluded."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The propulsive axial musculature must already operate near its maximal mass-specific power during the maximal escape, with no ~3x reserve (3x leap) or ~10x reserve (flight) at fixed fast-start duration",
      "quantity": "ratio of available to used muscle-mass-specific power in a maximal fast-start", "lo": null, "hi": 3.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Supported only in other species: Wakeling & Johnston 1998 report in-vivo fast-start muscle power similar to work-loop maxima (Scorpaena notata fast fibres 142.7 W/kg, 20 C) in six marine teleosts (Notothenia coriiceps, N. rossii, Myoxocephalus scorpius, Scorpaena notata, Serranus cabrilla, Paracirrhites forsteri) -- no cyprinid, no Danio. No adult Danio fast-muscle power measurement found; Danio white-muscle mass fraction unknown",
      "satisfied_evidence": "literature",
      "note": "Wakeling JM & Johnston IA 1998 J Exp Biol 201:1505, doi 10.1242/jeb.201.10.1505, abstract. Required power ratios calculated from KE per mass (0.95, 2.86, 9.55 J/kg at 1.38, 2.39, 4.37 m/s). Extending to Danio is my inference. Search scope: Europe PMC '(zebrafish OR \"Danio rerio\") AND adult AND (\"work loop\" OR \"work-loop\") AND muscle' (11 hits, none adult fast-muscle); one WebSearch (larval values only, search-summary)."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "A paired lifting surface of at least ~192 mm2 (span ~1 SL, AR ~5) must exist on a ~0.25 g fish for take-off speed to be as low as 4.37 m/s",
      "quantity": "total pectoral planform area", "lo": 192, "hi": null, "units": "mm^2",
      "status": "unsatisfied",
      "satisfied_by": "No measured adult Danio pectoral fin area found (wild type or Daane 2021 double heterozygote). Nothing measured contradicts 192 mm2, so not unsatisfiable. A smaller true area raises V_to (S28 cases 5.47 m/s at 125 mm2, 8.10 m/s at 57 mm2) and worsens the deficit",
      "satisfied_evidence": "unknown",
      "note": "Search: WebSearch 'adult zebrafish pectoral fin surface area mm2 measured' (Paulissen 2022, Dokmegang 2021, Thorsen & Hale 2005, van Eeden 1996 surfaced; per summaries none report adult area; not opened in full). Daane et al. 2021 Curr Biol 31:5052 Fig. 4B (length/SL) not read. Shallow scope: 'not measured as far as found'."}
  ]}
```
