# Claim 235: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived):** m\* = 39 mg (8.5–173 mg) for the
latch-mediated spring actuation (LaMSA) route. A 0.4 g zebrafish is ~10× (2.3–47×) *too large* for
single-impulse launch, not too small. The muscle-only route has no realisable crossover at all.

**Date:** 2026-11-04.

**Provenance caveat:** This repository does not contain the derivation of claim 235. I searched the
working tree and all 30 commits on both branches for `LaMSA`, `39 mg`, `zebrafish` and `latch`, and
none of them is the source. So I do not know its inputs (the spring and latch parameters, or the
displacement length). The constraints below come from the claim's statement plus the general LaMSA
framework of Ilton et al. 2018 (*Science* 360:eaao1082; read-level: **abstract**). In that framework,
muscle beats a spring-and-latch below a crossover mass, and muscle is adequate above it. I have not
re-derived the 39 mg.

**Network scope:** I could not open the full texts on `journals.biologists.com` /
`cob.silverchair.com`, `par.nsf.gov`, `discovery-pp.ucl.ac.uk` or `sciencegate.app`, because those
hosts are not on this session's network allowlist. Every *J. Exp. Biol.* source is therefore read at
search-summary or abstract level. PMC pages could be fetched.

---

## What the claim entails

If a 0.4 g zebrafish sits above m\*, the LaMSA framework says its escape should be explainable by
**direct muscle drive, with no amplification**. That sets four requirements one scale down or across:

| # | Target scale | Kind | Requirement (generic) | Status |
|---|---|---|---|---|
| C1 | organ | timescale | The propulsive stroke lasts at least as long as the fast axial muscle takes to contract (ratio ≥ 1), so the muscle is not limited by how fast it can contract | **open** for 0.4 g. Satisfied by measurement in 5–7 dpf larvae |
| C2 | organ | energetic | The escape's peak mass-specific mechanical power is no more than what fast axial muscle can deliver by work loop, with no amplifier needed | **open** for zebrafish. Supported in other teleosts (authors' claim) |
| C3 | organ | existence | A latched elastic mechanism must be buildable from fish tissue, or "the LaMSA route" has no physical meaning for fish | **satisfied** (measured, other species) |
| C4 | behaviour | conservation | For the single-impulse comparison to describe the behaviour, most of the escape's linear momentum must come from one propulsive stroke | **open**: measured data exist but their reading depends on interpretation |

There is no `range` or `spatial` constraint. The claim supports one only through m\*'s unknown
inputs (spring stroke, displacement length), and without the derivation I would have had to invent
the bounds.

---

## C1 — timescale (organ): stroke duration vs muscle contraction time

*Requirement:* t_stroke / t_contraction ≥ 1 (dimensionless; lo = 1, hi = none). Above the crossover,
a muscle-driven body does not reach the end of its stroke before the muscle can finish contracting.

*Measured values found (larvae only):*
- Contraction half-time of single twitches in 5–7 dpf zebrafish larval muscle is **3.2 ± 0.2 ms**,
  and relaxation half-time is 4.7 ± 0.2 ms, at 22 °C (Dou, Andersson-Lendahl & Arner 2008, *J Gen
  Physiol* 131:445; PMC2346565; read-level: **full-text**, read through a fetch summariser).
- C-bend lasts **0–11 ms**, counterbend 11–21 ms, and fast swimming 21–54 ms, in 5 dpf larvae
  (total length 4.08 mm) (Ravel et al. 2025, *iScience* 28:112056; PMC11930232; read-level:
  **full-text**, first 100k of 153k characters).
- A search summary of another source gives intact larval tail fast muscle a twitch full-width at
  half-max stress of 11.5 ± 1 ms (par.nsf.gov/servlets/purl/10377057; read-level:
  **search-summary**, not opened). This is a different measure from the 3.2 ms half-time, and I
  have not reconciled the two.

*My calculation, not an observation:* 11 ms ÷ 3.2 ms ≈ 3.4. Against the 11.5 ms full-width figure
the ratio is ≈ 1.0. Both numbers come from different labs and conditions. In larvae the constraint is
**met, though marginally on the second figure**.

*For the 0.4 g adult the claim is about:* **unknown**. I ran two web searches (one standard, one
extended) for adult zebrafish stage-1 duration in ms and found no value. The only adult study
surfaced (doi:10.1242/jeb.068957, a water-viscosity study; read-level: **search-summary**) reports
trends but gave no numbers in the summary. Nobody's adult measurement has been read here, so this is
"not found within scope", not "looked for and absent".

*Inference (mine):* 5 dpf larvae lie far below m\*, though I could not find their body mass. Even
there the bend is not clearly faster than the muscle can contract. That is mild tension with the
idea that sub-m\* bodies are contraction-limited. But a fish in water is not a projectile with a
fixed take-off stroke, so this does not test the claim directly. **Status: open.**

## C2 — energetic (organ): required power ≤ available muscle power

*Requirement:* the peak mass-specific power of a 0.4 g zebrafish escape, normalised to muscle mass,
must not exceed the power of fast teleost myotomal muscle.

*Available-power side (measured):*
- Fast myotomal fibres of *S. notata* produce **142.7 W kg⁻¹ muscle** (mean) by work loop at 20 °C.
  The paper's title states the authors' conclusion: "Muscle power output limits fast-start
  performance in fish" (Wakeling & Johnston 1998, *J Exp Biol* 201:1505; read-level:
  **search-summary/abstract**).
- Sculpin: the required power for the contralateral contraction was **20 and 58 W kg⁻¹**, against
  work-loop values of **33 and 66 W kg⁻¹**, at 5 and 15 °C (St Andrews thesis,
  hdl:10023/14938; read-level: **search-summary**).
- Carp ontogeny: muscle power output explains most of the size-related gain in fast-start
  performance (Wakeling, Kemp & Johnston 1999, *J Exp Biol* 202:3057; read-level:
  **search-summary**; the full text could not be reached).
- For scale, the maximum in-vitro vertebrate muscle power is **1121 W kg⁻¹** and largemouth bass
  epaxial muscle is about **216 W kg⁻¹**, both as cited by Longo et al. 2018 (read-level:
  **full-text**, via fetch).

*Required-power side for zebrafish:* **unknown**. Ravel et al. 2025 give larval power only in
absolute units (×10⁻⁵ W) with no mass normalisation. The authors claim larvae "maximize
neuromuscular power output", which is consistent with being muscle-limited but gives no ratio. I
found no adult zebrafish power estimate in the searches above.

*Inference (mine):* in three other teleosts, required power is at or below available muscle power,
which is what the claim predicts above m\*. Zebrafish was not one of the species, so I am not
counting this as satisfaction. **Status: open.**

## C3 — existence (organ): a latched elastic actuator can be built from fish tissue

*Requirement:* for "the LaMSA route" to be a real alternative whose crossover can be computed, a
fish musculoskeletal system must be able to load a spring against a latch and release it.

*Satisfied by:* the snipefish *Macroramphosus scolopax*. Its feeding strikes last **2.0–7.5 ms** and
need a mean peak power of **~2800 ± 560 W kg⁻¹ muscle**, with a range of 1090–5500. That is above
the 1121 W kg⁻¹ vertebrate maximum, so muscle alone cannot supply it, and the authors attribute the
excess to elastic recoil with a hyoid latch (Longo, Goodearly & Wainwright 2018, *Proc R Soc B*
285:20181078; PMC6053929; read-level: **full-text**, via fetch). Seahorses show a comparable
tendon-and-latch system in a preprint, which is not peer reviewed (bioRxiv
10.1101/2020.08.13.249466; read-level: **search-summary**).

*Caveat, which matters for interpreting m\* (my inference):* in these fish the mass that gets
launched is the **head**, rotated about the neck, not the whole body. Their body masses were not
reported on the page I read. So these systems do not contradict a whole-body m\* of 39 mg. They do
mean m\* has to be read as the mass of the *projectile*, not the organism. A 0.4 g fish could still
fall below m\* for a head-sized projectile. **Status: satisfied (measured).**

*Negative, scoped:* one standard web search for latch or elastic-storage mechanisms in fish
**fast-start escape** (whole-body axial) found none. The search was limited to that and to the
syngnathiform feeding literature it returned. It is not an exhaustive review.

## C4 — conservation (behaviour): momentum delivered in one stroke

*Requirement:* the "single-impulse launch" picture needs the escape's linear momentum to come mainly
from one propulsive stroke.

*Measured, but the reading is ambiguous:*
- In 5 dpf zebrafish larvae, stage 1 produces mostly torque and reorientation with limited
  propulsion. The propulsive force peaks in stage 2, and final speed depends mostly on start
  duration (Voesenek, Muijres & van Leeuwen 2019, *J Exp Biol* 222:jeb203091, Dryad
  doi:10.5061/dryad.gv43sm2; read-level: **abstract/search-summary**).
- In adult least killifish (*Heterandria formosa*), the centre of mass barely accelerates in stage 1
  in many cases (Dryad doi:10.5061/dryad.qb5j6; read-level: **search-summary**).

*Inference (mine):* if stage 2 is the single impulse, the measurements meet C4. If the escape counts
as a two-stroke bend-and-unbend, they break the premise, and the single-impulse m\* then describes a
behaviour fish do not perform. Neither reading contradicts "too large"; the question is whether the
comparison applies at all. Stage 1 also looks structurally like a loading phase, which is
interesting in LaMSA terms, but nothing I read shows elastic storage in it. **Status: open.**

---

## Disagreement kept, not averaged

The claim says "the muscle-only route has no realisable crossover at all". A search summary of
jumping-scaling work in the Ilton/Patek line says LaMSA can store only ~30% of the work muscle could
do, and that muscle-actuated jumpers of all sizes can exceed spring-actuated jump heights by about 3×
(source in the search results: escholarship qt2n60g31p / *J Exp Biol* 223:jeb208678; read-level:
**search-summary**; the full text could not be reached). That model compares jump *height*, not
power or take-off time, so it may not conflict with claim 235. Still, the two framings differ on
whether muscle has a crossover at all, and this note does not settle it.

## Outcome

No measured number contradicts claim 235 at the organ or behaviour scale. **Nothing is
unsatisfiable.** One constraint is satisfied by measurement (C3). Three are open: the adult
zebrafish values needed for C1 and C2 were not found within the stated search scope, and C4 depends
on interpretation. The best next step is to get adult zebrafish stage-1 durations and
muscle-normalised fast-start power. Most likely sources: doi:10.1242/jeb.068957, and full texts on
journals.biologists.com once that host is allowed.

```swarm-entail
{"source_claim": 235, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The propulsive stroke of the escape must last at least as long as the fast axial muscle's contraction time, so the muscle is not limited by contraction rate above m*",
      "quantity": "t_stroke / t_contraction", "lo": 1, "hi": null, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Larvae only: C-bend 0-11 ms (Ravel et al. 2025) vs twitch contraction half-time 3.2 ms at 22 C (Dou et al. 2008), ratio ~3.4 (calculated); ~1.0 against an 11.5 ms twitch FWHM (search-summary). No adult (0.4 g) stage-1 duration found.",
      "satisfied_evidence": "measured",
      "note": "Dou, Andersson-Lendahl & Arner 2008 J Gen Physiol 131:445, PMC2346565 (full-text); Ravel et al. 2025 iScience 28:112056, PMC11930232 (full-text, partial); par.nsf.gov 10377057 (search-summary). Negative scope: 2 web searches for adult zebrafish stage-1 ms; adult viscosity study doi:10.1242/jeb.068957 surfaced but unread (host blocked). Not found within scope, not confirmed absent. Ratio is my calculation."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Peak mass-specific mechanical power required by the escape must not exceed the power available from fast axial muscle, so that no amplifier is needed",
      "quantity": "required power / available muscle power", "lo": null, "hi": 1, "units": "dimensionless (each in W per kg muscle)",
      "status": "open",
      "satisfied_by": "Available side measured in other teleosts: 142.7 W/kg muscle, S. notata fast fibres, 20 C (Wakeling & Johnston 1998); sculpin required 20/58 vs work-loop 33/66 W/kg. Zebrafish required power not found: Ravel 2025 reports only absolute power (x1e-5 W), larvae.",
      "satisfied_evidence": "literature",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505 (search-summary/abstract), authors' claim that muscle power limits fast-start; St Andrews hdl:10023/14938 (search-summary); Wakeling, Kemp & Johnston 1999 J Exp Biol 202:3057 (search-summary). Zebrafish not among species studied; not counted as satisfied."},
    {"target_scale": "organ", "kind": "existence",
      "statement": "A latched elastic actuator (spring loaded by muscle against a latch, then released) must be constructible from fish musculoskeletal tissue for the LaMSA route to be physically meaningful",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Snipefish (Macroramphosus scolopax) feeding strike: 2.0-7.5 ms, ~2800 +/- 560 W/kg muscle, above the 1121 W/kg vertebrate muscle maximum; attributed to hyoid-latched elastic recoil. The projectile is the head, not the whole body.",
      "satisfied_evidence": "measured",
      "note": "Longo, Goodearly & Wainwright 2018 Proc R Soc B 285:20181078, PMC6053929 (full-text). Seahorse preprint bioRxiv 10.1101/2020.08.13.249466 (search-summary, not peer reviewed). Implies m* must be read as projectile mass, not organism mass (my inference). Negative scope: one web search found no latch mechanism in whole-body fast-start escape."},
    {"target_scale": "behaviour", "kind": "conservation",
      "statement": "For a single-impulse launch model to describe the escape, most of the body's linear momentum must come from one propulsive stroke",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Measured but ambiguous: zebrafish larvae produce little propulsion in stage 1, with the propulsive peak in stage 2 (Voesenek et al. 2019); adult killifish centre of mass barely accelerates in stage 1. Whether stage 2 counts as the single impulse decides the outcome.",
      "satisfied_evidence": "measured",
      "note": "Voesenek, Muijres & van Leeuwen 2019 J Exp Biol 222:jeb203091, Dryad doi:10.5061/dryad.gv43sm2 (abstract/search-summary); Heterandria formosa Dryad doi:10.5061/dryad.qb5j6 (search-summary). No adult zebrafish impulse partition found."}
  ]}
```
