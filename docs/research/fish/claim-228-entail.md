# Claim 228: what it requires at `organ` and `behaviour`, checked

**Source claim (scale `organism`, evidence `derived`):**
> THE SHORTFALL IS ~1.86x (1.22-3.08), against >=10x for EVERY wing route. The launch-energy representation is an order of magnitude closer to feasible than the wing representation ever was.

**Where it comes from.** It is the headline of S29 (`docs/research/fish/S29-organism.md`, branch `origin/claude/s29-launch-energy-2iuixr`). The number is

shortfall = need / (f · w · r · η_h) = 10.17 / (0.30 · 53 · 0.93 · 0.37) = **1.86×**

where:
- f is the fraction of body mass that loads the spring (one side of the axial muscle, 0.30, assumed by S29);
- w is the energy one contraction stores per kg of muscle (frog 53 J/kg, range 32–81, Mendoza & Azizi 2021);
- r = 0.93 is the spring return;
- η_h = 0.37 is the hydromechanical efficiency (pike C-start).

The 1.22–3.08 range is **only** w varied over 32–81, with f and η_h held fixed. The claim is therefore true at the neighbouring scales only if f, w and η_h have the values it uses, and if the loading/release timing it assumes exists. The constraints below say exactly that.

**What this pass is.** One reader. Nothing is simulated. The bounds are **calculated by me** from S29's own formula, and are labelled so. Every literature value is someone else's measurement, and I give a read level for each. Most fetches were blocked by the session's network policy (`cse-lab.seas.harvard.edu` and `acnpsearch.tweb-dev.unibo.it` failed to resolve; earlier challenges 224 and 231 record `cob.silverchair.com`, `open.library.ubc.ca` and `discovery-pp.ucl.ac.uk` as blocked). Most of my reads are therefore **search-summary**.

**Prior challenges this builds on** (read level: full-text, from git):
- `challenge-224.md` (branch `claude/c-start-spring-energy-chv9eu`): η_h is a C-start proxy, and the stored energy is a lower bound.
- `challenge-231.md` (branch `claude/challenge-231-launch-barrier-lotnw9`): the wing and spring routes share S28's 4.37 m/s target, and loading by a single contraction is an unstated assumption.

I do not repeat those findings. I note where they bear on a constraint.

---

## C1 — organ, `range`: energy stored per kg of axial muscle in one loading contraction

**Requirement.** The muscle that loads the spring must store w ∈ **[32, 81] J/kg muscle** in one contraction for the stated 3.08–1.22× band. The 1.86× central figure needs **w ≈ 53 J/kg**. All of this is calculated from S29's formula: S(w = 32) = 3.08, S(53) = 1.86, S(81) = 1.22.

**Check.**
- **No teleost measurement found.** Searches (standard web, 4 queries) were on "fish fast muscle work per cycle", "single contraction J kg", "fast-start work loop" and "sculpin/carp fast muscle". None returned a measurement of energy stored into a series spring by fish axial muscle.
  - The values that do exist measure a **different quantity**: cyclic work-loop work. Short-horned sculpin fast fibres give **3.5 J/kg per cycle** at 25–30 W/kg peak power, 4–8 Hz (Johnston, Franklin & Johnson 1993, J. Exp. Biol. 185:251; search-summary). Fish fast myotomal muscle in a simulated fast-start gives **142.7 W/kg** (Wakeling & Johnston 1998, J. Exp. Biol. 201:1505; search-summary). Neither is spring-loading work. Comparing them would be a proxy error, so I do not.
  - S29 itself says this number is not in the literature it read for any teleost.
  - So this is **"nobody has looked"**, not "looked and found nothing".
- **A derived ceiling from fish-measured inputs.** This is my calculation, not an observation.
  - Whatever the gearing, one contraction cannot do more work per kg than **σ_max · ε / ρ**. A lever or cam changes the force at the spring, not the stress × strain product in the fibre.
  - Inputs:
    - fish fast-muscle isometric stress σ = **136–151 kN m⁻²**: carp whole myotomal muscle, J. Exp. Biol. 182:191 table excerpt; author not confirmed; search-summary;
    - σ = **209 kN m⁻²**: carp skinned fast fibres at 23 °C, warm-acclimated; search-summary;
    - σ = **~220 kN m⁻²**: sculpin fast fibres (Johnston et al. 1993; search-summary);
    - ρ = 1060 kg m⁻³ (assumed);
    - in-vivo white-fibre strain from C2.
  - Result, with force held at isometric maximum throughout, an unreachable upper bound:

    | σ (kN m⁻²) | ε = 0.16 (carp C-start) | ε = 0.24 (carp S-start, anterior) |
    |---|---|---|
    | 136 | 20.5 J/kg | 30.8 J/kg |
    | 220 | 33.2 J/kg | 49.8 J/kg |

    For a linear spring loaded directly from slack (force rising from zero), each value is halved.
  - **Every cell lies below the 53 J/kg central value.** Only the top-right cell reaches the 32 J/kg lower end.
  - Fed back through S29's formula, the ceilings give shortfalls of **1.98× (49.8), 2.97× (33.2) and 4.81× (20.5)**. These are calculated.

**Status: `unsatisfied`.** No measured value meets the requirement, because nobody has measured it in a teleost. The derived ceiling puts the central 53 J/kg **above** what fish-measured stress × in-vivo-measured strain allows. That ceiling is not a measured *capacity*: the strains are what carp fibres were observed to do in fast-starts, not a measured maximum (see C2). So it is not `unsatisfiable`.

**What it does say (my inference).** On fish inputs, the **1.22× end of the range is out of reach**, and the central value is more likely ~2–5× than 1.86×. That is still well under 10×, so the "order of magnitude closer" half of the claim survives this check. The 1.86× point estimate does not survive it intact.

## C2 — organ, `range`: fibre strain the axial fast muscle must reach at near-maximal stress

**Requirement.** To store w = 53 J/kg at the best fish stress found (220 kN m⁻²), the mean fibre strain at isometric-level stress must be **ε ≥ 0.26**. This is calculated as w·ρ/σ. At 136 kN m⁻² it must be ε ≥ 0.41. For the 32 J/kg end it must be ε ≥ 0.15 (at 220) or ≥ 0.25 (at 136). With a linear spring loaded from slack, all of these double.

**Check.** Measured carp white-fibre strains (Spierts & van Leeuwen 1999, J. Exp. Biol. 202:393; search-summary; strains derived from measured fibre orientation plus kinematics, not sonomicrometry):

| Start | Anterior white | Posterior white | Red |
|---|---|---|---|
| C-start | ~16 % (another summary gives 14.7 % and ~16.5 %) | similar to anterior | ~27 % |
| S-start | 24 % (maximum) | 10 % | anterior 39 % |

Wakeling & Johnston 1999 (J. Exp. Biol. 202; search-summary) measured white strain by **sonomicrometry** in 70 carp fast-starts. Their values were not available to me (`unknown`). They report that strain varies less across the myotome than bending theory predicts.

**Status: `unsatisfied`.** Every measured white-fibre strain in carp fast-starts (0.10–0.24) is below the 0.26 that the central figure needs at the best fish stress. Only C-start and anterior S-start strains reach the 0.15 that the 3.08× end needs.

I do **not** mark this `unsatisfiable`. These are in-vivo strains during swimming, not a measured maximum of the fibre's working range. A fish whose muscle loads a tendon rather than bending the body could, in principle, shorten further. I searched for a measured maximal working strain or length–tension range of teleost fast fibres and found none: one query, scope as for C1. So whether fish fast fibres *can* reach 0.26 at near-isometric stress is **unknown**.

**Disagreement preserved.** The summaries give 14.7 %, ~16 % and ~16.5 % for white C-start strain, which I did not reconcile.

## C3 — organ, `range`: mass fraction of axial muscle available to load the spring

**Requirement.**
- **Central 1.86×:** one side of the axial muscle = **0.30 of body mass**, i.e. ~0.60 total (S29, assumed).
- **3.08× end at w = 53:** one-side fraction **≥ 0.18**, i.e. total axial muscle **≥ 0.36 of body mass** (calculated).

**Check.**
- **Zebrafish.** A zebrafish toxicology review states that skeletal muscle is **~60 % of adult body mass** (search-summary). It cites a primary source I did not check. This is the same SECONDARY figure S29 used.
- **No zebrafish dissection found** (2 queries).
- **Cyprinid proxy.** Common/mirror carp fillet yield is **42.9 ± 2.4 %** (Maas et al. 2020, Arch. Anim. Breed. 63:69; skin-on; search-summary) and **34–39 %** (Austrian farms, J. Appl. Ichthyol. 2009; skin status not stated; search-summary).
  - Fillet is not total axial muscle: it includes skin and omits some trimmed muscle. So the direction of its bias against "total axial muscle" is mixed and unknown.

**Status: `satisfied`, for the lower bound (≥ 0.36 total), with evidence `literature`.** The zebrafish 60 % figure meets it. The carp fillet proxy (0.34–0.43) straddles it. The **central** f = 0.30 rests only on the secondary 60 % figure.

**Disagreement preserved.** If total axial muscle is 0.34–0.43, the central shortfall becomes **2.6–3.3×** instead of 1.86× (calculated). That is still under 10×.

## C4 — behaviour, `range`: hydromechanical efficiency of an impulsive whole-body push-off against water

**Requirement.**
- **Stated 1.22–3.08× band:** η_h ∈ **[0.22, 0.56]** at w = 53 (calculated, 0.37 · 1.86 / S).
- **"Order of magnitude closer" (S < 10×):** η_h **> 0.069** (calculated).

**Check.** All values below are measured, from C-starts. They are the proxy that challenge 224 flagged: the claim needs spring-to-centre-of-mass efficiency for a straight push-off, which has not been measured.
- **Pike (*Esox lucius*) C-start:** **0.34–0.39**, S-start 0.27 (Frith 1990, UBC thesis; search-summary via challenge 224; S29 ABSTRACT).
- **Carp:** **0.19 → 0.38** across acute 10–20 °C (Wakeling, Cole, Kemp & Johnston 2000; search-summary via challenge 224). Efficiency did not change significantly with size from 7 mm larvae to 80 mm (Wakeling, Kemp & Johnston 1999; search-summary).
- **Larval zebrafish C-start:** described as energetically inefficient in simulation (Gazzola, van Rees & Koumoutsakos 2012, J. Fluid Mech. 698:5; search-summary of press coverage). This is a **simulated** result and no number was available: fetching the PDF failed, so the value is `unknown`.

**Status: `satisfied`.** Every measured fast-start value (0.19–0.39) clears the 0.069 needed for "order of magnitude closer". Pike and warm carp (0.34–0.39) lie inside the [0.22, 0.56] band.

**Disagreement preserved.**
- Carp at 10 °C (0.19) falls **below** the band and would give 3.6× (calculated).
- No value exists for a zebrafish at ~28 °C.
- Challenge 231 infers, without quantifying it, that a more heavily loaded 5 ms impulse would have lower efficiency than a C-start.
- So "satisfied" holds **only for the C-start proxy**. The actual launch-stroke efficiency has not been measured by anyone.

## C5 — behaviour, `timescale`: loading must be slow relative to release, with the load held between

**Requirement.**
- The spring's advantage depends on two things:
  - **slow loading**, which escapes the force–velocity penalty and is where the 3.7–9.4× gain over today's 8.6 J/kg comes from (S29 §5);
  - **fast release**, which S29 sets at 5–14 ms.
- So the loading phase must be **≥ ~10× the release duration**, roughly ≥ 50–140 ms. This order of magnitude is my judgement and is not derived; the measured case below exceeds it by a wide margin.
- The load must be held by a latch or a locked posture during that phase.

**Check.**
- **Bay pipefish (*Syngnathus leptorhynchus*).** Epaxial EMG starts **more than 300 ms** before the strike. The head then rotates by more than 20° in **under 5 ms**. The hyoid is held locked during the preparatory phase (Van Wassenbergh et al. 2008, J. R. Soc. Interface 5:285; abstract fragment, search-summary). A later summary gives "at least 200 ms" before head rotation (search-summary), which is consistent with it, not contradictory.
  - Ratio: loading ≥ 300 ms / release < 5 ms gives **> 60×**, calculated from the reported numbers.
- **Seahorses** show the same epaxial pre-activation (2014 study; search-summary).
- **Scope.** This is satisfied **in teleosts, in feeding, in Syngnathiformes only**. I did not search for a preparatory loading phase in zebrafish or cyprinid escape or leaping behaviour. Zebrafish fast-starts are described as reflexive. Larvae reach the C-shape in 5–6 ms (SICB abstract; search-summary), and adult C-escapes last ~50 ms (a modelling study, age unconfirmed; search-summary). Neither shows a held pre-load.
  - So the existence of slow-load and fast-release *timing* in a teleost is shown, but in a **locomotor** context it is **not searched**.

**Status: `satisfied`, with evidence `literature`.** The requirement is generic: teleost muscle–tendon can load slowly and release fast with a hold in between. The named mechanism is the syngnathiform epaxial-tendon / hyoid-lock system, which is measured. That it is a feeding system in the head, not the axis, is S29's "latch is an invention" point, and it remains true.

---

## Summary

| # | Scale | Kind | Required | Status | What decides it |
|---|---|---|---|---|---|
| C1 | organ | range | w 32–81 J/kg muscle per contraction (53 central) | **unsatisfied**: never measured in a teleost; derived ceiling on fish inputs 20–50 J/kg | single-contraction spring-loading work of zebrafish myotomal muscle |
| C2 | organ | range | fibre strain ≥ 0.26 at near-isometric stress (central) | **unsatisfied**: measured in-vivo 0.10–0.24 | maximal working strain of teleost fast fibres (not found) |
| C3 | organ | range | total axial muscle ≥ 0.36 of body mass (0.60 central) | **satisfied** (lower bound; secondary 60 %); carp fillet proxy 0.34–0.43 disagrees on the central value | zebrafish dissection |
| C4 | behaviour | range | η_h 0.22–0.56 (band); > 0.069 (order of magnitude) | **satisfied**, C-start proxy only (0.19–0.39 measured) | PIV on a zebrafish push-off |
| C5 | behaviour | timescale | loading ≥ ~10× release, load held | **satisfied** in syngnathiform feeding (> 300 ms vs < 5 ms); locomotor case not searched | — |

**Nothing is `unsatisfiable`.** No measured number contradicts a requirement. The closest is C2: every measured strain is below the requirement, but those strains are in-vivo observations, not a measured ceiling.

**What the propagation shows (my inference, from calculated bounds on measured inputs).**
- The claim splits into two parts.
- **"An order of magnitude closer than the wing route" survives every check at both neighbouring scales.** All the fish-input variants I computed give 1.98–4.81× (C1), 2.6–3.3× (C3) and up to 3.6× (C4 at 10 °C). Each is under 10×.
- **"~1.86× (1.22–3.08)" does not survive cleanly.**
  - Its central value needs a fibre-work density (53 J/kg) and a fibre strain (≥ 0.26) above anything measured for teleost fast muscle.
  - Its lower end (1.22×) needs 81 J/kg, i.e. ε ≥ 0.39 at the best fish stress.
  - On fish inputs, the honest band is closer to **~2–5×**.
- The decisive measurement is the one S29 already named: **single-contraction spring-loading work of zebrafish fast myotomal muscle**. This propagation adds a cheaper first test: **the maximal working strain of zebrafish fast fibres at ≥ 0.9 P0**, because C1's ceiling is σ × ε.

## Sources and read levels

| Source | Used for | Read level |
|---|---|---|
| S29-organism.md (`origin/claude/s29-launch-energy-2iuixr`) | claim, formula, inputs | full-text |
| challenge-224.md, challenge-231.md | prior challenges; Frith 1990, Wakeling 1999/2000 values | full-text |
| Johnston, Franklin & Johnson 1993, J. Exp. Biol. 185:251 (sculpin fast fibres, ~220 kN m⁻², 3.5 J/kg/cycle) | C1 | search-summary |
| Carp myotomal P0 136–151 kN m⁻², J. Exp. Biol. 182:191 (author not confirmed) | C1 | search-summary |
| Carp skinned fast fibres 209 kN m⁻² at 23 °C (source paper not identified) | C1 | search-summary |
| Wakeling & Johnston 1998, J. Exp. Biol. 201:1505 (142.7 W/kg) | C1 (not comparable) | search-summary |
| Spierts & van Leeuwen 1999, J. Exp. Biol. 202:393 (carp fibre strains) | C2 | search-summary |
| Wakeling & Johnston 1999, J. Exp. Biol. 202 (sonomicrometry, white strain) | C2 (values unknown) | search-summary |
| Zebrafish toxicology review, "~60 % of adult body mass" (PMC; primary not checked) | C3 | search-summary |
| Maas et al. 2020, Arch. Anim. Breed. 63:69 (fillet 42.9 %) | C3 | search-summary |
| Austrian carp fillet yield 34–39 %, J. Appl. Ichthyol. 2009 | C3 | search-summary |
| Frith 1990 UBC thesis (pike η 0.34–0.39) | C4 | search-summary (via 224) |
| Wakeling, Cole, Kemp & Johnston 2000 (carp η 0.19–0.38) | C4 | search-summary (via 224) |
| Gazzola, van Rees & Koumoutsakos 2012, J. Fluid Mech. 698:5 | C4 (no number) | search-summary; PDF could-not-access |
| Van Wassenbergh et al. 2008, J. R. Soc. Interface 5:285 (pipefish) | C5 | search-summary (abstract fragment) |

Searches: 12 standard web searches. Fetch attempts: 2, both refused by the network policy.

```swarm-entail
{"source_claim": 228, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The muscle that loads the launch spring must store, in a single contraction, an energy density within the band that produces the stated shortfall range (53 J/kg for the 1.86x central value).",
      "quantity": "single-contraction spring-loading work per kg of axial muscle", "lo": 32, "hi": 81, "units": "J/kg muscle",
      "status": "unsatisfied",
      "satisfied_by": "No teleost measurement exists in search scope (nobody has looked, not looked-and-absent). Only cyclic work-loop values found (sculpin 3.5 J/kg/cycle), which measure a different quantity. Derived ceiling sigma*eps/rho from fish-measured stress (136-220 kN/m2) and carp in-vivo white strain (0.16-0.24) is 20.5-49.8 J/kg (calculated), all below the 53 central value.",
      "satisfied_evidence": "derived",
      "note": "Johnston, Franklin & Johnson 1993 JEB 185:251 (search-summary); carp P0 JEB 182:191 (search-summary); Spierts & van Leeuwen 1999 JEB 202:393 (search-summary). Scope: 4 standard web searches on fish fast-muscle work per contraction / work loops; S29 also reports none. Ceiling is not a measured capacity, so not unsatisfiable. Feeding the ceilings back gives shortfall 1.98-4.81x (calculated)."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Axial fast fibres must shorten far enough at near-isometric stress to deliver the required work density (strain >= w*rho/sigma).",
      "quantity": "mean fibre strain at near-maximal stress for w=53 J/kg at sigma=220 kN/m2", "lo": 0.26, "hi": null, "units": "dimensionless (fraction of resting length)",
      "status": "unsatisfied",
      "satisfied_by": "Measured carp white-fibre strains in fast-starts are 0.10-0.24 (C-start ~0.16; S-start anterior 0.24, posterior 0.10), all below 0.26. No measured maximal working strain of teleost fast fibres found, so no measured ceiling contradicts the requirement.",
      "satisfied_evidence": "literature",
      "note": "Spierts & van Leeuwen 1999 JEB 202:393 (search-summary; strain from fibre orientation + kinematics); Wakeling & Johnston 1999 JEB 202 sonomicrometry values unknown (could-not-access). Summaries disagree on C-start white strain (14.7%, ~16%, ~16.5%). Scope: 2 searches; maximal teleost fast-fibre working-strain range not searched beyond one query, found none."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Enough axial muscle must exist to load the spring: total axial muscle mass fraction >= 0.36 for the 3.08x end at w=53; ~0.60 for the 1.86x central value.",
      "quantity": "total axial (skeletal) muscle mass / body mass", "lo": 0.36, "hi": 1.0, "units": "fraction of body mass",
      "status": "satisfied",
      "satisfied_by": "Zebrafish skeletal muscle ~60% of adult body mass (secondary review; primary not checked). Disagreeing cyprinid proxy: carp fillet yield 0.34-0.43, which would make the central shortfall 2.6-3.3x (calculated).",
      "satisfied_evidence": "literature",
      "note": "Zebrafish review via PMC (search-summary); Maas et al. 2020 Arch Anim Breed 63:69 (search-summary); J Appl Ichthyol 2009 Austrian carp 34-39% (search-summary). No zebrafish dissection found in 2 searches. Lower bound satisfied; central 0.60 rests only on the secondary figure."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "An impulsive whole-body push-off against water must convert stored energy to body kinetic energy with an efficiency inside the band producing the stated range; >0.069 keeps the shortfall under 10x.",
      "quantity": "hydromechanical efficiency of the launch stroke", "lo": 0.22, "hi": 0.56, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Measured fast-start efficiencies (C-start proxy): pike 0.34-0.39; carp 0.19-0.38 across 10-20 C, size-invariant 7-80 mm. All exceed 0.069; pike and warm carp lie inside [0.22,0.56]; carp at 10 C (0.19) falls below. No measurement of the actual straight launch-stroke efficiency exists.",
      "satisfied_evidence": "literature",
      "note": "Frith 1990 UBC thesis (search-summary via challenge 224); Wakeling, Cole, Kemp & Johnston 2000 and Wakeling, Kemp & Johnston 1999 (search-summary via 224). Gazzola et al. 2012 JFM 698:5 says larval C-start is inefficient (simulated; number unknown, PDF could-not-access). Satisfied for the C-start proxy only; zebrafish at ~28 C unmeasured."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Spring loading must be slow relative to release (order >=10x the 5-14 ms release), with the load held by a lock between loading and release.",
      "quantity": "loading duration / release duration", "lo": 10, "hi": null, "units": "ratio",
      "status": "satisfied",
      "satisfied_by": "Bay pipefish feeding strike: epaxial EMG onset >300 ms before strike, head rotation >20 deg in <5 ms, hyoid locked during preparation (ratio >60x, calculated from reported values); same pre-activation in seahorses.",
      "satisfied_evidence": "literature",
      "note": "Van Wassenbergh et al. 2008 J R Soc Interface 5:285 (search-summary of abstract). Satisfied only in syngnathiform feeding, in the head; a preparatory loading phase in zebrafish/cyprinid locomotion was not searched (not looked, not absent). The >=10x threshold is my judgement, not derived."}
  ]}
```
