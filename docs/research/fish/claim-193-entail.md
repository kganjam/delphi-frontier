# Claim 193: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived):** *A tail-driven skim at the measured 52 Hz
maximum reaches only 1.15–1.72 m/s, giving 7–16% of the lift needed.*

**Date of check:** 2026-11-04. **Adjacent scales:** organ, behaviour.

The claim's own derivation is not in this repository. I searched `docs/`, `findings/`, `ledger/`
and `frontier/` for "193", "skim", "52 Hz", "flying fish" and "Exocoet" and found nothing. So
the source of the 52 Hz figure, the stride model behind 1.15–1.72 m/s, and the lift model behind
7–16% are all **unknown** to me. Below, every number that comes from the claim is labelled
*claim-implied*. Every number I worked out is labelled *derived (mine)*.

## Network scope

Most primary hosts could not be reached from this session: researchgate.net, int-res.com,
semanticscholar.org, archive.org/biostor, par.nsf.gov, bamlab.princeton.edu and
meetings-archive.aps.org all failed DNS resolution. Only the bioRxiv HTML full text (Deng et al.
2019) was fetched. Everything else comes from web-search summaries of abstracts or of secondary
sources. This limits every negative result below: "not found" means *not found within web-search
summaries plus one bioRxiv full text*. It does **not** mean the literature has been read and
found empty.

## Numbers the claim implies (derived, mine)

- **Stride per tail beat:** 1.15/52 = 0.022 m and 1.72/52 = 0.033 m. For a 0.25 m fish that is
  0.09–0.13 body lengths (L) per beat.
- **Lift needed:** lift ∝ V², so the claim's two (speed, lift-fraction) pairs both imply a
  required speed of about 4.3 m/s (1.15/√0.07 = 4.35 and 1.72/√0.16 = 4.30).
- **Cross-check that disagrees with the claim:** I combined Deng et al.'s model inputs (m = 0.191 kg,
  pectoral area 0.024 m²) with Park & Choi's maximum C_L of 1.03 (as cited in search results) and
  ρ_air = 1.2 kg m⁻³.
  - The required speed comes out at about **11.2 m/s**.
  - At that requirement, 1.15–1.72 m/s gives **1.0–2.3%** of the needed lift, not 7–16%.
  - To need only 4.3 m/s, S·C_L would have to be about 0.17 m², roughly 7× those inputs.
  - So either the claim uses a different body or wing model, or its lift fraction is
    overstated. I cannot tell which without its derivation. Under either model the claim's
    *direction* (tail-only skim gives insufficient lift) still holds. **This is a calculation,
    not an observation.**

## Constraints and checks

### C1 — organ, range: taxi tail-beat frequency must have a ceiling near 52 Hz
For the claim's premise to hold, the caudal propulsor must not beat much faster than 52 Hz during
taxiing.

The sources disagree, and I leave the disagreement standing:

- **Davenport 1994**, *Rev. Fish Biol. Fish.* 4:184–214, doi:10.1007/BF00044128 (read-level:
  search-summary of the abstract). The tail beats "at up to 50 beats s⁻¹". This is consistent with a
  ceiling near 52 Hz.
- **Hertel 1966**, *Structure, form, movement*, as cited by Deng et al. 2019 (read-level:
  full-text of Deng; Hertel itself not accessed). "About 50 beats s⁻¹ … in warmer waters (~25 °C)".
  This is consistent.
- **Deng et al. 2019**, bioRxiv 765560 (read-level: full-text). Paraphrases Davenport as "50–70
  strokes s⁻¹". That conflicts with the Davenport abstract wording above.
- **Hubbs 1933**, as cited in a ScienceDirect topic overview (read-level: search-summary). "Tail
  beats reaching nearly 70/sec". Deng et al. also cite a Hubbs 1933 paper titled "Species and
  hybrids of *Mollienesia*", which does not obviously match a flying-fish claim. The attribution
  is doubtful.
- **Makiguchi et al. 2013**, *Aquatic Biology* 18:105–111, doi:10.3354/ab00494 (read-level:
  search-summary of the abstract). The authors measured, with accelerometer loggers, a stroke-cycle
  frequency of 21.2 ± 4.6 Hz at take-off in 9 fish of 30.8 ± 3.1 cm. They say this is lower than
  in field studies. These fish were in a controlled enclosure, and this is not a taxi-phase maximum.
- **APS March Meeting 2024 abstract, session S27.13** (read-level: search-summary only;
  could-not-access the abstract itself). A search summary reports "a measured frequency of 13.5 Hz".
  The species and context are unknown.

**Status: open.** No primary source I could read gives a measured taxi maximum, and the values
cited for one range from about 50 to about 70 Hz.
- If about 70 Hz is a real measurement, then 52 Hz is not the maximum, and the claim's speed
  understates by about 35%. Using the claim's own linear-in-f model, that gives about 1.55–2.3 m/s
  and about 13–29% lift (derived, mine).
- Even then, the claim's conclusion (insufficient lift) survives. This is not a refutation.

### C2 — organ, timescale: one muscle-activation cycle must fit inside 9.6 ms
At 52 Hz a full tail cycle lasts 19.2 ms. Each side's axial muscle must therefore activate and
relax within about 9.6 ms at about 25 °C. If it cannot, 52 Hz cannot be the operating frequency.

- **Wardle 1975**, *Nature* 255:725 (read-level: search-summary). Argues that maximum tail-beat
  frequency is limited by muscle contraction time. That time lengthens with body length and
  shortens with temperature.
- No twitch time or contraction-time measurement for exocoetid axial muscle was found.

**Status: unsatisfied.** Search scope: web searches for Wardle's contraction-time framework and for
flying-fish muscle kinetics. I found no study that measured exocoetid muscle twitch times. This
reads as "nobody has looked, as far as I can see". It is not "looked and found too slow".
Deng et al. (full-text) work out a need for "83.3 contractions s⁻¹" at 41.7 Hz. That is a model
statement, not a measurement.

### C3 — organ, spatial: stride per tail beat during the skim must be no more than about 0.033 m
For 52 Hz to give at most 1.72 m/s, the in-water propulsor (the hypocaudal lobe) must advance the
fish at most about 0.033 m per beat. That is about 0.13 L for L = 0.25 m (claim-implied).

- **Wardle 1975** (search-summary): submerged swimming strides are 0.6–0.8 L per beat. That applies
  to a whole submerged body, not to a lobe-only skim, so it neither meets nor contradicts C3.
- **Deng et al. 2019** (full-text): their CFD reaches 10 m/s at 50 Hz, about 0.2 m or 0.8 L per
  beat. This **simulated** value is about 6× the claim-implied ceiling. It conflicts with the claim,
  but being a simulation it cannot refute the claim from below.
- **Edgerton & Breder 1941** (read-level: search-summary of a plate caption). High-speed
  photographs show a zigzag taxi track that "gives some idea of the value of each tail thrust in
  terms of the fish's length". I could not access the numbers.

**Status: open.** No measured taxi stride length was obtained. Edgerton & Breder 1941 is the
obvious place to measure one.

### C4 — behaviour, range/conservation: the speed carried out of the water must cover the deficit
If the tail can only skim at 1.15–1.72 m/s, then airborne glides require the fish to leave the water
already at or above the take-off speed, carrying momentum from underwater swimming. The bound is
v_emergence ≥ about 4.3 m/s (claim-implied required speed).

- **Makiguchi et al. 2013** (search-summary of the abstract). The fish "were estimated to leap from
  the water surface at speeds of 3.9 to 5.2 m s⁻¹". This is an author estimate from accelerometer
  data, not a direct velocity measurement.
  - The upper part of that range meets 4.3 m/s. The lower end does not.
  - The authors put these at 38.7–51.5% of earlier stroboscopically filmed maximum swim speeds,
    which works out to about 10.1 m/s (derived, mine, from their percentages).
- **Davenport 1994** (search-summary): fish "approach the surface at high speed (about 10 m/s in
  large fish; 20–30 L/s)".

**Status: satisfied, conditionally.** It is met if the required speed is about 4.3 m/s, as the
claim implies. Under my cross-check (about 11.2 m/s), the logger estimates of 3.9–5.2 m/s fall short.
The roughly 10 m/s approach speeds would only just reach it, which would again leave a deficit
that something has to supply during the taxi.

### C5 — behaviour, range: speed must not rise during a tail-only taxi
If a tail-driven skim tops out at 1.72 m/s, a fish whose body is airborne with only the tail in the
water cannot gain speed while taxiing above that ceiling. Speed during the taxi must stay flat or
fall. Any measured *rise* in speed above about 1.72 m/s during a tail-only taxi would refute the
claim from below.

Against this:
- Davenport 1994 (search-summary of the abstract) states that fish "accelerate to take-off speed by
  taxiing with the lateral fins expanded and the tail beating in the water". This is the author's
  claim, and in the text I retrieved it is qualitative.
- Deng et al. 2019 (full-text) say taxiing "can probably accelerate the flying fish to a speed up to
  15–20 m s⁻¹", citing Davenport. The wording is hedged. Their 10–25 m/s taxi speeds are
  **simulated**.
- Franzisket 1965 (cited by Deng) reports 400 m in 30 s through repeated taxiing. That is a mean
  speed of about 13 m/s (derived, mine). It is not a taxi-phase speed time series, and the speed
  could come from repeated re-entries rather than tail thrust.

**Status: open.** This is the constraint most likely to be **unsatisfiable**. It would take a
*measured* taxi-phase speed above 1.72 m/s, or a measured speed rise, with only the tail in the
water. I found qualitative author statements and simulations, but no measured velocity time series
within the scope above. So I do not mark it unsatisfiable. Franzisket 1965, Edgerton & Breder 1941
and Hertel 1966 should be read in full before this is closed either way.

## Summary

| # | Scale | Kind | Status |
|---|---|---|---|
| C1 | organ | range | open (sources conflict: 50 vs about 70 Hz) |
| C2 | organ | timescale | unsatisfied (no exocoetid muscle kinetics found) |
| C3 | organ | spatial | open (only a simulated stride, about 6× the ceiling) |
| C4 | behaviour | range/conservation | satisfied, conditionally on the required speed |
| C5 | behaviour | range | open (qualitative "accelerates while taxiing", no measurement) |

No constraint was found unsatisfiable. The sharpest risk to the claim is C5: the literature
consensus *says* taxiing accelerates fish to 15–20 m/s, but I could not locate the measurement
behind that statement. Separately, the claim's 7–16% lift fraction is about 3–7× higher than my
cross-check (1.0–2.3%). That needs the claim's derivation to resolve. It weakens nothing in the
claim's conclusion.

```swarm-entail
{"source_claim": 193, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The caudal propulsor's maximum tail-beat frequency during surface taxiing must not substantially exceed the 52 Hz value the claim takes as the ceiling",
      "quantity": "maximum taxi tail-beat frequency", "lo": null, "hi": 52, "units": "Hz",
      "status": "open",
      "satisfied_by": "Davenport 1994 abstract: 'up to 50 beats s-1'; Hertel 1966 (via Deng 2019): ~50 beats s-1 at ~25 C. Conflicting: Hubbs 1933 (via ScienceDirect overview) 'nearly 70/sec'; Deng 2019 paraphrases Davenport as 50-70 strokes s-1. Lab logger data (Makiguchi 2013) 21.2 +/- 4.6 Hz at take-off, not a taxi maximum.",
      "satisfied_evidence": "literature",
      "note": "Davenport 1994 Rev Fish Biol Fish 4:184-214 doi:10.1007/BF00044128 (search-summary); Deng et al. 2019 bioRxiv 765560 (full-text); Hubbs 1933 via secondary (search-summary; Deng's Hubbs reference title looks mismatched); Makiguchi et al. 2013 Aquat Biol 18:105-111 doi:10.3354/ab00494 (search-summary); APS 2024 S27.13 '13.5 Hz' (search-summary, could-not-access). Disagreement kept unresolved. If 70 Hz is real, claim-model speeds become ~1.55-2.3 m/s, lift ~13-29% (derived): the conclusion still holds."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The axial muscle driving the tail must complete activation and relaxation within one half tail-beat cycle at the operating frequency and sea temperature",
      "quantity": "half-cycle muscle activation-relaxation time", "lo": null, "hi": 9.6, "units": "ms",
      "status": "unsatisfied",
      "satisfied_by": "Searched for exocoetid axial muscle twitch or contraction-time measurements and for Wardle-type contraction-time limits applied to flying fish; none found. Deng 2019's '83.3 contractions s-1' is a model requirement, not a measurement.",
      "satisfied_evidence": "unknown",
      "note": "Wardle 1975 Nature 255:725 framework (search-summary). Negative scope: web search summaries only; reads as 'nobody has looked', not 'looked and found too slow'."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The distance advanced per tail beat by the in-water propulsor during a tail-only skim must be at most the claim-implied stride",
      "quantity": "stride length per tail beat during taxi", "lo": null, "hi": 0.033, "units": "m",
      "status": "open",
      "satisfied_by": "No measured taxi stride found. Deng 2019 CFD gives ~0.2 m/beat (10 m/s at 50 Hz): simulated, ~6x the ceiling, so it conflicts but cannot refute. Wardle 1975 submerged-swimming stride 0.6-0.8 L applies to a different gait.",
      "satisfied_evidence": "unknown",
      "note": "Claim-implied ceiling 1.72/52 = 0.033 m (~0.13 L at L = 0.25 m), derived. Edgerton & Breder 1941 high-speed photographs show a zigzag taxi track per tail thrust (search-summary of plate caption; numbers not accessed): the best source to close this."},
    {"target_scale": "behaviour", "kind": "conservation",
      "statement": "Because the tail cannot supply take-off speed, the fish must carry at least take-off speed out of the water as momentum from underwater swimming",
      "quantity": "speed at water-surface emergence", "lo": 4.3, "hi": null, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Makiguchi et al. 2013: leap speeds estimated at 3.9-5.2 m/s from accelerometer loggers (upper part meets 4.3 m/s); Davenport 1994: surface approach ~10 m/s in large fish.",
      "satisfied_evidence": "measured",
      "note": "Makiguchi 2013 values are author estimates from acceleration data (search-summary of abstract); Davenport 1994 (search-summary). Conditional: lo = 4.3 m/s is claim-implied. My cross-check (m 0.191 kg, S 0.024 m2 from Deng 2019; CL 1.03 from Park & Choi 2010 as cited) gives ~11.2 m/s required, which the 3.9-5.2 m/s estimates do not meet and ~10 m/s approaches only marginally meet."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "During a taxi with only the tail in the water, the fish's speed must not rise above the tail-only skim ceiling; observed taxi-phase speed must be flat or falling",
      "quantity": "speed gain during tail-only taxi phase", "lo": null, "hi": 1.72, "units": "m/s",
      "status": "open",
      "satisfied_by": "Against: Davenport 1994 says fish 'accelerate to take-off speed by taxiing' (qualitative author claim); Deng 2019 'can probably accelerate... up to 15-20 m/s' (hedged, citing Davenport) and simulated 10-25 m/s; Franzisket 1965 400 m in 30 s over repeated taxis (~13 m/s mean, derived; not a taxi-phase time series). No measured taxi velocity time series found.",
      "satisfied_evidence": "literature",
      "note": "This is the constraint most likely to become unsatisfiable: a measured taxi-phase speed rise above 1.72 m/s with only the tail immersed would refute claim 193 from below. Not marked so because no measurement was located. Scope: web search summaries plus Deng 2019 full text; Franzisket 1965, Edgerton & Breder 1941 and Hertel 1966 not read (hosts unreachable or not online)."}
  ]}
```
