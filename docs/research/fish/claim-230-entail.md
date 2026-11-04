# Claim 230: what it requires at the organ and behaviour scales, and what the literature says

**Source claim (230, organism scale, evidence: derived).**
> DECISIVE TEST: in-situ single-stroke spring-loading work of zebrafish fast myotomal muscle. A value at or above ~99 J/kg closes the energy term. Second: zebrafish C-start PIV efficiency.

This claim is S29's decisive-test statement (`docs/research/fish/S29-organism.md`, branch `claude/s29-launch-energy-2iuixr`, §6; read in full). Its threshold is
w ≥ 10.17 J/kg body ÷ (f 0.30 × η_s 0.93 × η_h 0.37) = **98.5 J/kg muscle** (recomputed here, *calculated*).

The claim therefore says: **a 0.4 g zebrafish launch at 4.37 m/s from a single latch-released stroke closes its energy budget if, and only if, one side of the axial muscle can put ≥ ~99 J/kg into a spring in one contraction, given an efficiency of 0.37 for converting that energy into body motion.** If that is true, conditions must hold at the organ scale (the muscle and its series elastic element) and at the behaviour scale (the escape/launch act). Those conditions are listed and checked below.

**Status of this document:** derived and literature-checked. **Nothing here is a new measurement.** All arithmetic comes from `python3 docs/research/fish/claim-230-entail_calc.py`. Every line of that script's output is *calculated*.

**Network scope.** Unreachable hosts in this session: escholarship.org, par.nsf.gov (DNS blocked). S29-D also lists iopscience, dspace.mit.edu, UBC library and silverchair as blocked. Europe PMC's REST API and pmc.ncbi.nlm.nih.gov were reachable.

---

## Summary

| # | Scale | Kind | Requirement | Status |
|---|---|---|---|---|
| C1 | organ | range | single-contraction energy stored in series spring, w ≥ 98.5 J/kg muscle | **unsatisfied**. No teleost measurement exists. The highest vertebrate value found is 81 J/kg (frog). |
| C2 | organ | range | isometric stress × usable fibre shortening ≥ ~104 kJ/m³, i.e. fibre strain ≥ 0.37 at full force (≥ 0.74 against a linear spring) at the measured adult teleost fast-fibre stress | **unsatisfied**. Adult zebrafish stress is unknown. The larval zebrafish stress (76 kPa, measured) would need strain ≥ 1.37, which is impossible. That measurement is at the wrong life stage, so this is not marked refuted. |
| C3 | organ | range | muscle mass loading the spring ≥ 0.30 of body mass (one side) | **unsatisfied**. No zebrafish measurement was found. The 0.60 total value is secondary only. |
| C4 | behaviour | range | KE_exit / E_stored ≥ 0.323 for a single latch-released stroke (equivalently η_h ≥ 0.37) | **unsatisfied**. No zebrafish value exists. The only *measured* spring-release analogue gives ≈ 0.10. |
| C5 | behaviour | timescale | a loading phase of ≥ 88 ms (≥ ~0.7 s at fish fast-start muscle power) must precede a ≤ 14 ms release | **unsatisfied**. No zebrafish locomotor behaviour with a held, pre-loaded axial posture was found. The only fish precedent is in feeding. |

**No constraint reached `unsatisfiable`.** The closest is C2. A *measured* larval zebrafish stress makes it physically impossible at the larval stage. The claim is about a 0.4 g adult, and adult zebrafish fast-muscle stress is `unknown`. I have not promoted C2 to unsatisfiable on a life-stage transfer. **If adult zebrafish fast-fibre stress turns out to be ≲ 105 kPa, C2 becomes unsatisfiable** for constant-force loading at strains ≤ 1. Against a linear spring the cutoff is ≲ 210 kPa. That would refute the claim from below.

---

## C1 — organ, range: single-stroke spring-loading work ≥ 98.5 J/kg muscle

**Requirement (generic).** The axial muscle must be able to store at least 98.5 J per kg of muscle in a series elastic element during one contraction. This is the claim's own threshold, restated at the organ scale. It is the organ-level quantity the claim names.

**Check.**
- **Teleost value: not found.** S29 (§6) and S29-D (§5) both report that no teleost value exists. My scope:
  - Europe PMC: `zebrafish muscle "work loop"` (16 hits). No spring-loading or series-elastic energy measurement among them.
  - Europe PMC: `(fish OR teleost) "fast muscle" isometric stress tetanic` (26 hits).
  - One web search on fish fast-muscle work per cycle.
  - **Classification: nobody has looked.** I found no study that loaded a teleost myotomal muscle against a compliant series element. This is *not* a case of people looking and finding a low value.
- **Best vertebrate measurement: below the threshold.** Mendoza & Azizi 2021, *J. Exp. Biol.* 224:jeb243180, doi:10.1242/jeb.243180. **Read level: full-text** (PMC10658917 HTML; results and discussion keyword-read).
  - Method: tetanic contractions with the muscle–tendon unit held at fixed length, so "any shortening of the muscle fascicles resulted in an equal stretch of the elastic elements". Work is the area under fascicle length against force.
  - Cuban tree frog plantaris "could store mass-specific energies averaging 53 J kg⁻¹ muscle mass (range: 32–81 J kg⁻¹ muscle mass)".
  - Cane toad 22 J/kg; bullfrog 37 J/kg.
  - The authors cite Olberding & Deban 2018 at "up to 73 J kg⁻¹" for the same species. That figure is **secondary**; I did not read the primary.
- **Gap to threshold** (*calculated*). The single highest measured individual value, 81 J/kg, is 0.82 of the threshold. The species mean, 53 J/kg, is 0.54 of it. The measurements come from a LaMSA-specialist frog, which the authors describe as tuned for energy storage.

**Disagreement with S29-D.** S29-D argues that the relevant chain efficiency for a spring release is ~0.10, not 0.323 (see C4). Under that value the threshold is not 98.5 but **339 J/kg muscle** (*calculated*), 4.2× the highest vertebrate value. That is a disagreement between two internal analyses. I report both and do not average them.

**Status: unsatisfied.** Teleost: nobody has looked. Vertebrates: every measured value is below the threshold.

## C2 — organ, range: stress × strain capacity of the fibres

**Requirement (generic).** Work done by a fibre in one contraction cannot exceed (stress) × (shortening strain) per unit volume. To store w = 98.5 J/kg at muscle density 1060 kg/m³ (*assumed*):
- at constant full isometric stress σ₀, σ₀ · ε ≥ 104 kJ/m³;
- against a linear series spring, force rises from 0 so work = ½ σ₀ ε, which doubles the requirement.

**The bounded quantity is fibre shortening strain at the available stress.**

**Check** (strains are *calculated* from measured stresses):

| Stress source | σ₀ | Read level | Strain needed (constant force / linear spring) |
|---|---|---|---|
| Sculpin *Myoxocephalus scorpius* fast myotomal fibres, 3 °C: "Maximum isometric tension was 281 kN m⁻²" (Altringham & Johnston 1988, *J. Comp. Physiol. B*, doi:10.1007/bf00582542) | 281 kPa | abstract | **0.37 / 0.74** |
| Larval zebrafish (5 dpf) whole tail: "maximal isometric stress (76 ± 3 mN/mm²)" (Mead et al. 2020, *Biophys. J.* 119:806, doi:10.1016/j.bpj.2020.06.036) | 76 kPa | abstract (full text returned a server error from Europe PMC) | **1.37 / 2.75** |
| Adult zebrafish fast fibres | `unknown` | — | — |

Notes on the table:
- Mead et al. normalise by whole-tail cross-section, which includes non-muscle tissue. The authors themselves call the stress "relatively low". It is therefore partly a geometric artefact and is not directly a fibre property. This caveat is mine, drawn from their abstract's framing.
- Search for an adult zebrafish value: Europe PMC `adult zebrafish skeletal muscle "specific force" OR "specific tension" OR "isometric stress"`. The top hits (Idoux et al. 2022 *J. Gen. Physiol.*, an excitation–contraction coupling study; Idoux et al. 2023 *PNAS*) report kinetics, not stress. I found no adult zebrafish fast-fibre stress.

**What the numbers mean.**
- **At the adult teleost stress** (sculpin), the claim needs fast fibres to shorten by ≥ 37 % of their length at full force, or ≥ 74 % against a linear spring, in one contraction. That is my inference.
- **What is measured about fish fast-fibre strains:**
  - Optimal strain for maximum work per cycle in sculpin fast fibres is ±5 % (**search-summary only**; not verified at a higher read level).
  - Wakeling & Johnston 1999 (*J. Exp. Biol.* 202:675, abstract) and Wakeling et al. 2000 (*Am. J. Physiol.* 279:R657, abstract) measured white-muscle strain during carp fast-starts. Neither abstract gives the number: `unknown`.
  - van Leeuwen et al. 2026 (*J. Exp. Biol.*, doi:10.1242/jeb.251951, full-text keyword-searched) is a *model* of larval fibre strain, not a measurement. I did not extract a strain value from it.
- **No measured teleost fast-fibre strain anywhere near 0.37 was found.** No measured value contradicting it was found either: the carp numbers are behind abstracts.
- **At the larval zebrafish stress**, the needed strain exceeds 1. That is physically impossible: a fibre cannot shorten by more than its own length. This rests on a *measured* stress, but at 5 dpf, not the 0.4 g adult the claim concerns.

**Status: unsatisfied.** The adult value is unknown. The bound is strained at the best adult teleost stress, and impossible at the larval zebrafish stress. **Upgrade trigger:** a measured adult zebrafish σ₀ ≲ 105 kPa (or ≲ 210 kPa for linear-spring loading) makes C2 **unsatisfiable**.

## C3 — organ, range: fraction of body mass that loads the spring ≥ 0.30

**Requirement (generic).** The 98.5 J/kg threshold is computed with f = 0.30: one side of an axial musculature taken as 60 % of body mass. For the claim to hold at that threshold, one side of the axial muscle must be ≥ 0.30 of body mass and must all be recruitable into one spring.

Equivalently (*calculated*), at the measured frog values the muscle fraction needed is:
- **0.36** of body mass at w = 81 J/kg;
- **0.56** at w = 53 J/kg.

**Check.**
- Europe PMC: `zebrafish ("muscle mass" OR "myotomal muscle") ("percent of body mass" OR "proportion of body mass" OR "body mass fraction")`. 4 hits, none relevant.
- S29 sources its 60 % as a **secondary review figure, primary not read**.
- S29's 30 % for one side is S29's **assumption**.
- I found no dissection-based axial muscle mass fraction for adult zebrafish. **Nobody has looked, within this scope.**

**Status: unsatisfied.** No measurement was found. The value is assumed in the source claim.

## C4 — behaviour, range: energy-transfer efficiency of a single released stroke ≥ 0.323

**Requirement (generic).** The fraction of spring-stored energy that ends up as forward kinetic energy of the body (plus drag work during the stroke) must be ≥ 0.93 × 0.37 / 1.065 = **0.323** (S29-D §3b, *calculated*). Equivalently, η_h ≥ 0.37 for the behaviour as performed. The claim names this as its second test ("zebrafish C-start PIV efficiency").

**Check.**
- **Zebrafish value: not found.**
  - Liu et al. 2026, *Biomimetics* 11:156, PMC12938309. **full-text, keyword-searched.** Adult zebrafish C-turns: 3.60 cm, 0.74 g; high-speed video plus self-propelled *simulation*. My keyword search found no efficiency value.
  - Ravel et al. 2025, *iScience* 28:112056, PMC11930232. **full-text, keyword-searched.** Larval escape *simulation*. Reports mechanical power and cost of transport, and defines Froude efficiency in methods. My search found no C-start η_h number. S29-D reached the same result.
  - Scope: Europe PMC `zebrafish "C-start" OR "escape" particle image velocimetry adult` (189 hits; first 8 screened), plus S29-D's ~10 Europe PMC queries and 5 web searches.
  - No PIV-measured adult zebrafish C-start efficiency was found. **Nobody has looked, within this scope.**
- **Muscle-driven values from other species:**
  - Pike 0.16–0.39 (Frith & Blake 1995) and carp 0.19–0.38 (Wakeling et al. 2000; **abstract**, read again here).
  - These are **model outputs** applied to measured kinematics, not measurements of energy flow (S29-D §2).
  - The best of them is ≈ 0.38–0.39. That would satisfy η_h ≥ 0.37, but only for a muscle-driven start.
- **The one measured spring-release value contradicts the requirement by analogy.**
  - Conte et al. 2010, *Bioinspir. Biomim.* 5:035004. **abstract only, via S29-D; not re-read here.**
  - Latch-released elastic fish robot: KE_final / E_stored "around 10%".
  - That is 0.10 against the required 0.323.
  - It is *measured*, but on an engineered body of unknown size whose material losses are lumped into the 10 %. It is not a zebrafish.
  - **I therefore do not mark C4 unsatisfiable.** A measured value from a different system is not a measured value of this constraint. S29-D's strongest reading, that the spring route fails by ~6×, rests on exactly this analogue.

**Status: unsatisfied.** Zebrafish: nobody has looked. The muscle-driven model values meet the bound. The only measured spring-release analogue misses it by 3.2×.

## C5 — behaviour, timescale: slow loading must precede fast release

**Requirement (generic).** A spring cannot store energy faster than the muscle delivers power. Loading 98.5 J/kg of muscle therefore takes at least t_load ≥ w / P_max (*calculated*):

| Muscle power used | t_load lower bound |
|---|---|
| vertebrate instantaneous maximum, 1,121 W/kg (Askew & Marsh 2001, **secondary** via S29) | **88 ms** |
| scorpionfish fast-start, 142.7 W/kg (Wakeling & Johnston 1998, abstract via S29) | **690 ms** |
| larval zebrafish work loop at 80 Hz, 134 ± 20 W/kg (Mead et al. 2020, abstract) | **735 ms** |

The release must be complete within 2.3–13.7 ms (S29 §2.2). So **t_load / t_release ≥ 6.4 at the most generous pairing, and up to ~320** (*calculated*).

At the behaviour scale, this requires an act in which the fish holds a loaded axial posture for ≥ ~0.1–0.7 s and then releases it. That is a deliberate, pre-loaded launch, not a reflex escape.

**Check.**
- **Fish precedent for slow loading: feeding only.** Pipefish epaxial EMG begins ">300 ms" before the strike (Van Wassenbergh et al. 2008, abstract via S29). That meets the timescale, but in a syngnathiform head-rotation feeding system.
- **Zebrafish locomotor precedent: none found.** I found no description of a zebrafish locomotor behaviour with a sustained, held axial pre-load before a fast start. The Liu et al. 2026 abstract mentions a "preparatory phase" in C-turns, but that is the bending stage of the turn itself, not a held loading phase, on my reading of the abstract and methods.
- **Scope:** Europe PMC adult zebrafish fast-start/C-start kinematics query (78 hits, top 6 screened). I did not systematically survey zebrafish escape-latency literature: my one targeted query did not return the intended paper. So **"no such behaviour" is partly a not-looked result**, not a looked-and-absent one.

**Status: unsatisfied.**

---

## What would change these statuses

| Measurement | Effect |
|---|---|
| Adult zebrafish fast-fibre isometric stress (single fibre or bundle, normalised to fibre cross-section) | Settles C2 and could make it **unsatisfiable**. This is cheap and is not the full in situ spring test. |
| Measured fast-fibre strain at near-plateau force in an adult cyprinid (sonomicrometry or fluoromicrometry) | Also settles C2 |
| The claim's own test: in situ single-stroke spring-loading work | Settles C1 |
| Dissected one-side axial muscle mass fraction | Settles C3 |
| PIV of an adult zebrafish C-start, or the S29-D bench test of a 30 mm latch-released elastic body | Settles C4 |

## Honesty ledger

- **Measured by others** (quoted, with read level):
  - Frog stored energy 53 (32–81) J/kg [full-text].
  - Sculpin fast-fibre σ₀ 281 kPa [abstract].
  - Larval zebrafish tail stress 76 kPa and work-loop power 134 W/kg [abstract].
  - Conte robot KE/E ≈ 0.10 [abstract, via S29-D].
  - Pipefish pre-strike EMG > 300 ms [abstract, via S29].
- **Model outputs by others (not measurements):** pike η_h 0.16–0.39 and carp η_h 0.19–0.38.
- **Calculated here:** the 98.5 and 339 J/kg thresholds, all strains, all muscle fractions, all t_load bounds and ratios.
- **Assumed:**
  - Muscle density 1060 kg/m³.
  - Work ≤ σ₀·ε per volume (constant force) or ½σ₀·ε (linear spring). These are physical bounds that ignore stretch-enhanced force; the sculpin abstract reports up to 1.4 P₀ transiently under stretch, which does not apply to a shortening contraction.
  - S29's need of 10.17 J/kg body, its f = 0.30, η_s = 0.93 and η_h = 0.37, taken as the claim defines them.
- **Not used:** a search-summary claim of "3.5 J/kg per cycle" for sculpin fast fibres. It is a cyclic work-loop figure at search-summary level, and is not comparable to single-stroke spring loading.

```swarm-entail
{"source_claim": 230, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The axial muscle must be able to store at least ~98.5 J per kg of muscle in a series elastic element during a single contraction.",
      "quantity": "single-contraction spring-loading work density w", "lo": 98.5, "hi": null, "units": "J/kg muscle",
      "status": "unsatisfied",
      "satisfied_by": "No teleost measurement exists (nobody has looked: no study loading teleost myotomal muscle against a compliant series element found). Best vertebrate measurement is below the bound: Cuban tree frog plantaris mean 53, range 32-81 J/kg muscle; cane toad 22, bullfrog 37.",
      "satisfied_evidence": "measured",
      "note": "Mendoza & Azizi 2021 J Exp Biol 224:jeb243180 (full-text, PMC10658917). Olberding & Deban 2018 up to 73 J/kg (secondary via Mendoza & Azizi). Scope of teleost negative: Europe PMC 'zebrafish muscle work loop' (16 hits) and 'fish/teleost fast muscle isometric stress tetanic' (26 hits), one web search, plus S29 and S29-D searches. If S29-D's measured spring-release chain efficiency 0.10 applies, the threshold rises to 339 J/kg (calculated); this disagreement with S29 is preserved, not averaged."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The fast fibres must combine isometric stress and single-contraction shortening strain such that stress x strain >= ~104 kJ/m3 (constant force) or ~209 kJ/m3 (loading a linear spring); at the measured adult teleost fast-fibre stress of 281 kPa this means fibre shortening strain at near-plateau force of at least 0.37 (0.74 against a linear spring).",
      "quantity": "fast-fibre shortening strain at full force in one contraction", "lo": 0.37, "hi": 1.0, "units": "fraction of fibre length",
      "status": "unsatisfied",
      "satisfied_by": "No measured teleost fast-fibre strain near 0.37 found; carp fast-start white-muscle strains measured (Wakeling & Johnston 1999; Wakeling et al. 2000) but values not in abstracts (unknown). Adult zebrafish fast-fibre stress unknown. Larval (5 dpf) zebrafish tail stress 76 kPa (measured) would require strain 1.37 (constant force), which is physically impossible, but that is the wrong life stage, so not marked unsatisfiable.",
      "satisfied_evidence": "derived",
      "note": "Altringham & Johnston 1988 J Comp Physiol B doi:10.1007/bf00582542 sculpin fast fibres P0 281 kN/m2 (abstract). Mead et al. 2020 Biophys J doi:10.1016/j.bpj.2020.06.036 larval tail 76+/-3 mN/mm2 (abstract; whole-tail normalisation includes non-muscle tissue). Sculpin optimal strain +/-5% is search-summary only. Strains calculated with assumed muscle density 1060 kg/m3. Search for adult zebrafish stress: Europe PMC 'adult zebrafish skeletal muscle specific force/specific tension/isometric stress', top hits are E-C coupling studies with no stress value. Upgrade trigger: adult zebrafish fast-fibre stress <= ~105 kPa (constant force) or <= ~210 kPa (linear spring) makes this unsatisfiable."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The muscle recruitable into loading one spring in one contraction must be at least ~0.30 of body mass (one side of the axial musculature); 0.36 at w=81 J/kg and 0.56 at w=53 J/kg.",
      "quantity": "mass fraction of body that is spring-loading muscle", "lo": 0.30, "hi": null, "units": "fraction of body mass",
      "status": "unsatisfied",
      "satisfied_by": "No dissection-based axial muscle mass fraction for adult zebrafish found. The 0.60 total skeletal muscle value used by S29 is a secondary review figure; the 0.30 one-side value is S29's assumption.",
      "satisfied_evidence": "assumed",
      "note": "Scope: Europe PMC 'zebrafish (muscle mass OR myotomal muscle) (percent/proportion of body mass OR body mass fraction)', 4 hits, none relevant. Nobody has looked, within this scope. Fractions 0.36/0.56 are calculated from 10.17 J/kg body need / (w x 0.93 x 0.37)."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "In a single latch-released stroke, the fraction of stored elastic energy converted to forward body kinetic energy plus in-stroke drag work must be at least ~0.323 (equivalently hydromechanical efficiency >= 0.37 with 0.93 spring return).",
      "quantity": "KE_exit / E_stored for a single released stroke", "lo": 0.323, "hi": 1.0, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish C-start efficiency measurement (PIV or otherwise) found. Muscle-driven efficiencies in pike 0.16-0.39 and carp 0.19-0.38 are model outputs, not measurements. The only measured latch-released elastic fish body (robot) gives ~0.10, 3.2x below the bound, but it is a different system of unknown size with lumped material loss, so it does not make this unsatisfiable.",
      "satisfied_evidence": "literature",
      "note": "Conte et al. 2010 Bioinspir Biomim 5:035004 (abstract, via S29-D). Frith & Blake 1995 J Exp Biol 198:1863 (abstract, via S29-D). Wakeling et al. 2000 Am J Physiol 279:R657 (abstract). Liu et al. 2026 Biomimetics 11:156 PMC12938309 adult zebrafish C-turn video+simulation, no efficiency found (full-text keyword search). Ravel et al. 2025 iScience 28:112056 larval CFD, no C-start eta_h found (full-text keyword search). Scope: Europe PMC 'zebrafish C-start/escape PIV adult' (189 hits, first 8 screened) plus S29-D's ~10 queries and 5 web searches. Zebrafish: nobody has looked, within scope."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Spring loading must take much longer than release: a held, pre-loaded axial phase of at least ~88 ms (absolute vertebrate power ceiling) and ~0.7 s at measured fish fast-muscle power must precede a release of <= ~14 ms, so the launch must be a deliberate pre-loaded act, not a reflex escape.",
      "quantity": "loading duration before release", "lo": 0.088, "hi": null, "units": "s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish locomotor behaviour with a sustained held axial pre-load before a fast start found. The only fish precedent meeting the timescale is pipefish feeding (epaxial EMG >300 ms before strike), a syngnathiform head-rotation system, not axial locomotion.",
      "satisfied_evidence": "literature",
      "note": "t_load bounds calculated as 98.5 J/kg / power: 1121 W/kg vertebrate instantaneous max (Askew & Marsh 2001, secondary via S29) -> 88 ms; 142.7 W/kg scorpionfish fast-start (Wakeling & Johnston 1998, abstract via S29) -> 690 ms; 134 W/kg larval zebrafish work loop (Mead et al. 2020, abstract) -> 735 ms. Release window 2.3-13.7 ms from S29 sec 2.2. Van Wassenbergh et al. 2008 J R Soc Interface 5:285 (abstract via S29). Scope: Europe PMC adult zebrafish fast-start/C-start kinematics (78 hits, top 6 screened); escape-latency literature not systematically surveyed, so the negative is partly not-looked."}
  ]}
```
