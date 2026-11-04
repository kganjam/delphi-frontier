# Claim 226 — entailments at organ and behaviour scale

**Source claim (organism scale, evidence: derived).**
> POWER PASSES: a 5–14 ms release needs 7400–18400 W/kg muscle — 1.3–3.2× beyond measured fish
> LaMSA (5795 W/kg, pipefish) but WITHIN measured insect LaMSA (36000–74000 W/kg, froghopper)

**Scope note.** This repository holds no record of which organism or movement claim 226 is
about, or of how its 7400–18400 W/kg was derived. I searched the working tree and both remote
branches (`claude/claim-226-entail-qpfmk7`, `work/frontier-foundation`) for "LaMSA", "pipefish",
"froghopper" and "W/kg" and found no matches. So every constraint below is written for "a fish
whose release lasts 5–14 ms and needs 7400–18400 W/kg of muscle". No check can be satisfied **for
that organism**. Where a fish precedent exists, I report it as a precedent and not as satisfaction.

## Before the constraints: the comparison values in the claim are not measurements

The claim calls both reference values "measured". Neither is a direct measurement.

- **Pipefish, 5795 W/kg.** Van Wassenbergh et al. 2008, *J R Soc Interface*, "Extremely fast prey
  capture in pipefish is powered by elastic recoil" (*Syngnathus leptorhynchus*). Read-level:
  full-text, through an automated fetch-and-summarise of PMC2607401, so the numbers here are as
  the summariser relayed them. According to the authors, 5795 W/kg is the peak *power
  requirement* from inverse-dynamic modelling of high-speed video, divided by epaxial plus
  hypaxial mass (32.2 + 16.5 mg). It splits into 2641 W/kg for head rotation and 3154 W/kg for
  body movement. It is a **derived** value. The authors compare it with 1121 W/kg, the peak
  vertebrate muscle power they cite (quail pectoralis in vitro, Askew & Marsh 2001), and say the
  requirement is "more than five times" that.
- **Froghopper, 36000–74000 W/kg.** Burrows 2003, *Nature* 424:509, doi:10.1038/424509a.
  Read-level: search-summary. Jump energies of 49 µJ (mean) and 100 µJ (best) come from
  kinematics. The power figure assumes the jump accelerates over 1 ms, and the result is divided
  by the trochanteral depressor mass (about 11% of body mass). This is also **derived**: it rests
  on an assumed acceleration time.

My inference, not in either paper: because the froghopper power assumes 1 ms, multiplying it by
1 ms gives energy per kg of muscle. That works out to **36–74 J/kg** for the froghopper. Claim 226
asks for 7400–18400 W/kg over 5–14 ms, which is about 1.4–5× longer, so its *energy* per kg of
muscle (constraint C2) is the froghopper's or higher, even though its *power* is lower. "Within
insect LaMSA" holds for power. It does not carry over to energy.

## Constraints

### C1 — organ — existence
**A power-amplifying element must exist in series with the muscle: an elastic store that the muscle
loads slowly, and a latch that holds the store and then releases it.**

Why the claim requires it: 7400–18400 W/kg is 6.6–16× the highest vertebrate muscle power the
pipefish authors cite (1121 W/kg, quail, in vitro). It is 50–440× the measured power of fish fast
myotomal muscle:
- about 42 W/kg, trout whole-muscle preparation (Johnsrude & Webb, *JEB* 119:71; search-summary);
- about 91 W/kg, dogfish white fibres (*JEB* 140:187; search-summary);
- about 143 W/kg, *Scorpaena notata* fast fibres at 20 °C (Wakeling & Johnston 1998, *JEB*
  201:1505; search-summary).

Direct muscle drive is therefore excluded. This is my inference, from measured muscle values and
the claim's derived requirement.

**Status: open** for the claim's organism, which is unidentified. Precedent in fish: in
Syngnathidae, the hyoid "locks" when fully elevated and blocks head rotation while the epaxial
muscles stretch their tendons. Van Wassenbergh et al. 2008 (full-text, machine-summarised) say
this, building on Muller 1987, and state that the trigger "remains unresolved". In seahorses,
sternohyoideus-tendon and urohyal tension hold the hyoid raised while energy is stored (Van
Wassenbergh et al. 2014, *PLoS One*, doi:10.1371/journal.pone.0109068; search-summary). A
snipefish slingshot was also reported (2018, phys.org; listing only). None of this shows that the
claim's organism has such a mechanism.

### C2 — organ — energetic
**The elastic store must take up, and in one release return, the work the release needs, per kg of
loading muscle.**

E = P × t_release. Over the claim's four corners this gives 37, 92, 104 and 258 J/kg (my
calculation). If shorter releases pair with higher power, the central estimate is 92–104 J/kg.
These values assume the stated W/kg is a mean over the release. If it is a peak and the pulse is
roughly triangular, E is about half, roughly 18–129 J/kg; I did not use that in the bounds.
Quantity: muscle-mass-specific elastic energy delivered per release, **lo 37, hi 258 J/kg**.

Comparison values:
- Cuban tree frog (*Osteopilus septentrionalis*) hindlimb muscle work in a jump is up to
  **60 J/kg**. Peplowski & Marsh 1997, *JEB* 200:2861, read search-summary, derive this from
  force plate and kinematics, so it is not a direct muscle measurement. Marsh 2022, *JEB*
  jeb244525 (PMC9659324), read search-summary, reports the same ceiling. Peplowski & Marsh judged
  60 J/kg to be within vertebrate muscle capacity. Marsh 2022 reports that average power rose with
  work only up to 36 J/kg.
- Fish fast muscle (sculpin) produced **3.5 J/kg** per cycle under optimal strain and stimulation,
  at swimming frequencies (*JEB* 1993; search-summary). That is cyclic work, not one maximal
  shortening, so it is not a ceiling.
- My own upper-bound estimate for one maximal shortening is about 62 J/kg: 220 kPa maximum
  tetanic stress for sculpin fast muscle (search-summary) × 0.3 strain ÷ 1060 kg/m³. Holding full
  stress through the whole shortening makes this an overestimate.
- A modelling paper, found as a search-summary only, argues that length–tension properties limit
  spring-actuated systems to at most one-third of the work the muscle could otherwise produce.
  That is a **simulated** result.
- Froghopper: 36–74 J/kg, derived above.

**Status: unsatisfied.** The lowest corner, 37 J/kg, falls under the frog's 60 J/kg. The central
estimate, 92–104 J/kg, and the upper corner, 258 J/kg, exceed every vertebrate or fish value I
found and the froghopper's derived 36–74 J/kg. Nothing I found in fish comes near it.

It is **not unsatisfiable**, for two reasons:
- (a) none of the comparison values is a measured *ceiling* on single-contraction work;
- (b) the loading muscle could be larger than the mass in the claim's denominator, which I could
  not inspect. A spring loaded by a large muscle mass, such as epaxials, and delivering to a small
  "muscle" mass would get around this.

Scope of the negative: web searches for fish fast-muscle work per contraction, maximum vertebrate
work per contraction, and frog and galago jump work. Full texts were not read except the pipefish
paper. I found no study measuring single-contraction work in fish that load a spring. That is
"I did not find it", not "people looked and found nothing".

**Upgrade path.** Recover how claim 226 computed 7400–18400 W/kg: which muscle mass, and whether
the power is mean or peak. If energy per kg of the *actual loading muscle* turns out ≥ 92 J/kg,
compare it with a measured maximum shortening work for that fish's muscle. A measured value below
it would make C2 unsatisfiable.

### C3 — behaviour — timescale
**A loading phase must come before the release, lasting at least E / P_load, where P_load is the
power the loading muscle can sustain.**

Using E from C2 (37–258 J/kg) and measured fish fast-muscle power (42–143 W/kg), the minimum
preload duration is **lo 0.26 s, hi 6.1 s** (my calculation). The central E of 92–104 J/kg gives
0.64–2.5 s. These are lower bounds: elastic and latch losses lengthen the load time. If the loading
muscle produced quail-class 1121 W/kg instead, the minimum would drop to about 0.03–0.23 s.
Measured pre-activation in fish runs far below that.

Precedent (measured): pipefish epaxial EMG starts at least 105 ms before head rotation. Mean
onsets were −209 ± 74 ms and −258 ± 112 ms in two individuals, with a range of 104–586 ms across
the Discussion (Van Wassenbergh et al. 2008, full-text, machine-summarised). Seahorses show the
same pre-activation pattern (Van Wassenbergh et al. 2014, search-summary; no duration in what I
read).

The pipefish maximum, 586 ms, sits below the 0.64 s that the claim's central energy needs at the
best fish muscle power. My inference: pipefish need much less energy per kg, because their 5795
W/kg is a peak about 1.5 ms after onset within a 5 ms rotation.

**Status: open.** The organism is unknown and I have no measurement of its preparatory phase.
Prediction to test: high-speed video with EMG of the loading muscle should show activity starting
≥ 0.26 s before release, and more likely around 0.6–2.5 s, if claim 226 is right. Measured onsets
consistently under 0.26 s, with the loading muscle no larger than the claim's denominator, would
make this unsatisfiable.

### C4 — behaviour — existence
**A trigger action separate from the loading contraction must exist: a small movement or muscle
event that opens the latch and starts the 5–14 ms release.**

**Status: open.** For the claim's organism there is no data. Precedent:
- Seahorses: neurocranial rotation never came before hyoid rotation, which the cited kinematic
  study reads as hyoid rotation triggering the strike (search-summary; this is the authors'
  interpretation).
- Pipefish: the authors call the trigger unresolved, possibly protractor hyoidei or relaxation of
  m. adductor arcus palatini (full-text, machine-summarised).
- Snipefish: a small hyoid movement releases the latch (phys.org 2018; listing only).

## Summary

| # | scale | kind | status |
|---|---|---|---|
| C1 | organ | existence (spring + latch) | open (precedent in Syngnathidae) |
| C2 | organ | energetic, 37–258 J/kg per release | **unsatisfied**: central 92–104 J/kg exceeds every value found (frog 60, froghopper 36–74, derived) |
| C3 | behaviour | timescale, preload ≥ 0.26–6.1 s | open (pipefish precedent 0.10–0.59 s measured) |
| C4 | behaviour | existence (trigger) | open |

The finding that matters most is C2. The claim compares *power* with the froghopper, but at 5–14
ms its *energy* per kg of muscle is the froghopper's or more, and above the frog's 60 J/kg. That
tension sits one level below the claim, and resolving it needs the denominator the claim used.

## Sources

Read-levels are given in the text beside each use. "Full-text (machine-summarised)" means fetched
through a tool that summarises the page. I did not read the PDF myself.

- Van Wassenbergh S. et al. 2008 *J R Soc Interface* — https://pmc.ncbi.nlm.nih.gov/articles/PMC2607401
- Burrows M. 2003 *Nature* 424:509 — https://doi.org/10.1038/424509a
- Van Wassenbergh S., Dries B., Herrel A. 2014 *PLoS One* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4185880/
- Peplowski M.M., Marsh R.L. 1997 *JEB* 200:2861 — https://scilit.com/publications/184a0782ed446e68a2ab636929060773
- Marsh R.L. 2022 *JEB* — https://pmc.ncbi.nlm.nih.gov/articles/PMC9659324
- Johnsrude & Webb, *JEB* 119:71 — https://cob.silverchair.com/jeb/article/119/1/71/5099/Mechanical-properties-of-the-myotomal-musculo
- Wakeling & Johnston 1998 *JEB* 201:1505 — https://www.sciencegate.app/document/10.1242/jeb.201.10.1505
- Fish fast-muscle work and stress (sculpin, cod) — https://cob.silverchair.com/jeb/article/185/1/251/6749/RECRUITMENT-PATTERNS-AND-CONTRACTILE-PROPERTIES-OF ; https://cob.silverchair.com/jeb/article-pdf/170/1/143/2467023/jexbio_170_1_143.pdf
- Snipefish slingshot (listing) — https://phys.org/news/2018-07-elastic-slingshot-powers-snipefish.pdf

```swarm-entail
{"source_claim": 226, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "existence",
      "statement": "An elastic energy store loaded slowly by muscle, plus a latch that holds it and then releases it, must exist in series with the driving muscle, because direct muscle drive cannot supply 7400-18400 W/kg",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Not checked for claim 226's organism (unidentified in repo). Fish precedent: syngnathid hyoid lock with epaxial tendon storage (pipefish, seahorse); trigger unresolved in pipefish",
      "satisfied_evidence": "literature",
      "note": "Van Wassenbergh et al. 2008 J R Soc Interface (full-text, machine-summarised); Van Wassenbergh et al. 2014 PLoS One (search-summary). Fish fast muscle measured at 42-143 W/kg (Johnsrude & Webb; Wakeling & Johnston 1998; search-summary). Precedent only, not satisfaction for the claim's organism."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The elastic store must take up and return in one release the work E = P x t_release per kg of loading muscle",
      "quantity": "muscle-mass-specific elastic energy delivered per release", "lo": 37, "hi": 258, "units": "J/kg",
      "status": "unsatisfied",
      "satisfied_by": "Searched fish fast-muscle work per contraction, maximum vertebrate work per contraction, frog and galago jump work. Highest found: Cuban tree frog 60 J/kg (derived from kinematics); froghopper 36-74 J/kg (derived from Burrows 2003 with 1 ms assumption); fish fast muscle 3.5 J/kg per cycle (cyclic, not maximal). Only the 37 J/kg corner is met; the central 92-104 J/kg and the 258 J/kg corner are met by nothing found",
      "satisfied_evidence": "derived",
      "note": "Peplowski & Marsh 1997 JEB 200:2861 and Marsh 2022 JEB (search-summary); Burrows 2003 Nature 424:509 (search-summary). Bounds are my calculation from the claim's numbers. Not unsatisfiable: no measured ceiling on single-contraction work was found, and the claim's muscle-mass denominator is unknown. Scope: web search, full texts not read except pipefish. Not found, which is not the same as looked for and absent."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "A loading or preparatory phase lasting at least E / P_load must precede the release",
      "quantity": "minimum preload duration before release", "lo": 0.26, "hi": 6.1, "units": "s",
      "status": "open",
      "satisfied_by": "No measurement for claim 226's organism. Precedent: pipefish epaxial EMG onset 104-586 ms before head rotation (measured), which overlaps only the low end; the central estimate of 0.64-2.5 s exceeds the pipefish maximum",
      "satisfied_evidence": "unknown",
      "note": "Van Wassenbergh et al. 2008 (full-text, machine-summarised): onset means -209 +/- 74 and -258 +/- 112 ms. Bounds are my calculation using E from C2 and fish muscle power 42-143 W/kg. With quail-class 1121 W/kg the minimum falls to about 0.03-0.23 s."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "A trigger action separate from the loading contraction must exist that opens the latch and starts the 5-14 ms release",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "No data for claim 226's organism. Precedent: seahorse hyoid rotation always precedes neurocranial rotation (authors read it as the trigger); pipefish trigger unresolved; snipefish hyoid release (listing)",
      "satisfied_evidence": "literature",
      "note": "Van Wassenbergh et al. 2008 (full-text, machine-summarised); seahorse kinematics (search-summary); phys.org 2018 snipefish (listing)."}
  ]}
```
