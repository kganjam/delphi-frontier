# Claim 271 — entailment to adjacent scales (organ, behaviour)

**Source claim (organism scale, evidence: derived).**
> THE CEILING HAS A CLEAN FORM: U_max = f·A_pp·sqrt(c6/C_D(Re)). Measured foil thrust scales with
> tail speed squared INDEPENDENT of forward speed while foil drag scales as U², so immersed area and
> mass DROP OUT. Only tail speed and lobe drag at Reynolds number matter.

No simulation was run for this note. Every number below is either quoted from a source (with its
read-level) or is a **calculation** of mine from quoted numbers, and the sentence says which.

## Where the formula comes from (read before the constraints)

The form matches the pitching-foil scaling of Floryan, Van Buren, Rowley & Smits 2017
(*J. Fluid Mech.* 822:386–397; arXiv:1704.07478) — **read-level: full-text** (arXiv PDF, text
extracted). Their equation 2.7, as written by the authors:

- `C_T = c6 St² + c7 St A* − C_Dp`, with `C_T = F_x / (½ ρ U² s c)` and `St = 2 f A / U`,
  where A is the trailing-edge (half) amplitude, so `2A = A_pp`.
- Fitted (authors' values, pitching, U = 60 mm/s, chord Re = 4780): **c6 = 2.55, c7 = 0,
  C_Dp = 0.08**. Heave fit: c1 = 3.52, c2 = 3.69, C_Dh = 0.15.
- Authors' words: "the dimensional thrust is independent of freestream velocity for pitching
  motions, and only weakly depends on freestream velocity for heaving motions", tested over
  **U = 60–120 mm/s** (a factor of 2). They also warn "The values of the constants should not be
  taken to be universal."

**My calculation (derived, not observed):** setting net C_T = 0 gives
`St* = sqrt(C_Dp/c6) = sqrt(0.08/2.55) = 0.177`, i.e. `U_max = 5.65 · f · A_pp`. For pure heave,
ignoring the c2 term, `sqrt(0.15/3.52) = 0.206`. These are the numbers I check below. Note that
balancing foil thrust against **foil** drag alone ignores body drag; since body drag is positive,
the expression is an upper bound, which is consistent with the claim calling it a ceiling (my
inference).

## Constraints and checks

### C1 — organ — `range`: propulsor thrust at fixed f·A_pp must not depend on U
*Requirement.* The caudal propulsor must be a device whose dimensional mean thrust, at fixed tail
frequency and amplitude, varies with forward speed by much less than the U² variation of drag
across the operating range (≈ 0.5·U_max to U_max). Bounded quantity: the thrust coefficient
normalised on tail speed, `C_T* = F_x/(½ρ f² A² s c)`, must be constant in U.

*Check.*
- **Satisfied for a rigid pitching foil (measured):** Floryan et al. 2017, full-text, fig. 8,
  U = 60–120 mm/s, Re ≈ 4.8×10³–9.6×10³. Heave: "only weakly" dependent (authors' words, no number
  given in text).
- **Disagreement preserved — theory says otherwise for an undulating body.** Lighthill
  elongated-body theory, as given in Imperial College lecture notes (ma.ic.ac.uk/~ajm8/BioFluids/
  lec1107.pdf; **read-level: search-summary**), gives mean thrust `¼ m(L) k² h0² (V² − U²)`, which
  depends on U and vanishes at U = V. This is a model prediction, not a measurement, so it cannot
  make C1 unsatisfiable; but it says the U-independence is a property of the pitching/added-mass
  regime, not of fish propulsion in general.
- **For a biological caudal fin:** I did not find a measurement of fin thrust at fixed f·A with U
  varied. Scope of search: web search on foil thrust vs forward speed (Anderson et al. 1998 — PDF
  host dspace.mit.edu not reachable from this session, so **could-not-access**), Floryan 2017,
  Saadat et al. 2017 (**search-summary**). This is "I did not find it in a narrow search", not
  "people looked and found nothing".

**Status: satisfied** for the rigid-foil analogue the claim actually cites; the transfer to a real,
flexible, heave+pitch fish tail is my inference and is untested here.

### C2 — behaviour — `range`: Strouhal number at or below U_max must be ≥ sqrt(C_D/c6)
*Requirement.* If U ≤ U_max = f·A_pp·sqrt(c6/C_D), then every observed steady swim must have
`St = f·A_pp/U ≥ sqrt(C_D/c6)`. With Floryan's pitching coefficients (derived): **St ≥ 0.177**.
No upper bound is entailed.

*Check.* Taylor, Nudds & Thomas 2003, *Nature* 425:707–711 (**read-level: abstract**, via search
summary): dolphins, sharks and bony fish cruise at **0.2 < St < 0.4**. All of that range lies above
0.177. Floryan 2017 (full-text, §6.1, adapting Rohr & Fish 2004) reports odontocetes raise speed by
raising fluke-beat frequency at constant amplitude, i.e. St roughly constant — the behaviour the
formula predicts.

Caveats: (i) the data are **cruise**, not maximal speeds, which is the regime the ceiling governs;
(ii) c6 and C_D come from a rigid foil at Re ≈ 5×10³ and the authors say they are not universal;
C_D(Re) at fish-tail Re (10⁴–10⁶) will differ, so 0.177 is a calculated, Re-specific bound.

**Status: satisfied** (literature, abstract-level) for cruising; the max-speed case is covered by C4.

### C3 — organ — `timescale`: muscle cycle must be fast enough, and must be the limit on f
*Requirement.* Since U_max ∝ f with no other organism variable, the ceiling at the organism scale
is set by the maximum tail-beat frequency. So a process must exist at the organ scale that caps f,
and the axial muscle's contraction + relaxation must fit in one half-beat: `t_twitch ≤ 1/(2 f)`.

*Check.* Wardle 1975, *Nature* 255:725 "Limit of fish swimming speed" (**read-level: abstract and
secondary sources; full text paywalled**): maximum tail-beat frequency is limited by the twitch
contraction time of the fast muscle; max observed speeds "fit the dimensions of the muscle twitch
time and stride length"; contraction time increases with fish length and decreases with
temperature. Prediction V = 0.7·L/(2t) (as quoted by a secondary source). Wardle & Videler 1980,
*Nature* 284:445 (**abstract via search-summary**) confirm max tail-beat frequency is predicted by
twitch time, and that skipjack tuna (L = 0.37–0.43 m) have twitch times like non-scombroid teleosts.

**Status: satisfied** (literature). Named mechanism: fast-muscle twitch kinetics capping f.

### C4 — behaviour — `spatial`: stride length must not exceed 5.65·A_pp
*Requirement.* Stride (distance per tail beat) = U/f. The ceiling requires
`U/f ≤ A_pp·sqrt(c6/C_D)`; with Floryan's pitching coefficients (derived) **stride ≤ 5.65 A_pp**.

*Check.*
- Ordinary teleosts: stride 0.6–0.8 L (Wardle 1975, via secondary source; consistent with
  Bainbridge 1958, *J. Exp. Biol.* 35, abstract: `V = ¼ L(3f − 4)`, which tends to **0.75 L per beat**
  at high f — that asymptote is my arithmetic on their formula). Stride typical range 0.5–1 L
  (Videler 1993, as cited by a sailfish paper; **search-summary**). An A/L of 0.20 was reported for
  coho salmon (**search-summary**; I could not confirm whether that is peak-to-peak). Taking
  A_pp = 0.2 L, the ceiling is 1.13 L per beat (calculated) — above 0.6–0.8 L. Satisfied.
- **Tension, not refutation — scombrids.** Wardle & Videler 1980 (abstract-level) say scombrids
  "move twice as far for each tail beat"; Stevens & Neil skipjack ≈ 10 m/s vs ≈ 8 m/s extrapolated
  (as relayed by search summary, **not read**). Twice 0.7 L ≈ 1.4 L per beat (my arithmetic). That
  exceeds 1.13 L **if** tuna A_pp = 0.2 L. It is within the ceiling if tuna A_pp ≥ 0.25 L (calculated:
  1.4/5.65), or if C_D at tuna Re (~10⁶) is lower than the 0.08 measured at Re 4780 — which is
  expected but not quantified here. I did not find a measured skipjack A_pp (searched: Wardle &
  Videler 1980, Videler & Wardle 1991 *Rev. Fish Biol. Fish.* 1:23–40 — both **could-not-access** in
  full; core.ac.uk was unreachable). So no measured number contradicts C4.

**Status: satisfied** for ordinary teleosts; the scombrid record is the sharpest available test and
is **unresolved** for lack of a measured A_pp and of C_D at that Re. If someone measures skipjack
A_pp < 0.25 L together with a lobe C_D ≥ 0.08, C4 becomes unsatisfiable and the claim is refuted
from below.

### C5 — organ — `energetic`: muscle power must cover the foil power at U_max
*Requirement.* The formula sets U_max by kinematics alone. That is only the ceiling if muscle power
is not limiting first: available muscle power at f_max must be ≥ the foil's hydrodynamic input
power at St*, `P = ½ρU³sc (c8 St² + c9 St² f*)` (Floryan eq. 2.7; c8 = 7.78, c9 = 4.89 for their
rigid foil) plus body drag power.

*Check.* Not done. I did not search for mass-specific red/white muscle power at maximal tail-beat
frequency, nor compute the required power for any species. The Wardle & Videler 1980 remark that
the scombrid style "requir[es] greater power" (abstract-level) shows power can matter, but that is
not a check.

**Status: open.**

## Summary

No constraint is unsatisfiable on measured numbers found here. C1–C4 are satisfied within the
scopes stated; C5 is unchecked. The claim's derivation rests on one rigid-foil dataset (Re ≈ 5×10³,
U varied ×2), and the formula's own c6 and C_D are explicitly non-universal per their authors. The
most promising falsifier is C4 for scombrids: a measured A_pp and lobe C_D at Re ~10⁶ would decide it.

Sources not reachable from this session: dspace.mit.edu (Anderson et al. 1998 PDF), core.ac.uk;
nature.com full texts are paywalled.

```swarm-entail
{"source_claim": 271, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The caudal propulsor's mean thrust at fixed tail frequency and peak-to-peak amplitude must be independent of forward speed over the operating range (tail-speed-normalised thrust coefficient constant in U).",
      "quantity": "variation of dimensional thrust with U at fixed f*A_pp, over U ratio tested", "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Rigid pitching foil: dimensional thrust independent of freestream velocity over U = 60-120 mm/s (heave: only weakly dependent). No equivalent measurement found for a biological caudal fin.",
      "satisfied_evidence": "measured",
      "note": "Floryan, Van Buren, Rowley & Smits 2017 JFM 822:386 (arXiv:1704.07478), full-text, fig. 8, Re 4780-9560. Disagreement: Lighthill elongated-body theory (Imperial lecture notes, search-summary) gives thrust proportional to (V^2-U^2), U-dependent; that is theory, not measurement. Fish-fin scope: narrow web search only; Anderson et al. 1998 could-not-access."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Observed steady swimming must have Strouhal number f*A_pp/U at or above sqrt(C_D/c6), since U cannot exceed the ceiling.",
      "quantity": "Strouhal number St = f*A_pp/U", "lo": 0.177, "hi": null, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Cruising fish, sharks and dolphins observed at 0.2 < St < 0.4, all above the derived bound 0.177; odontocetes raise f at constant amplitude (St roughly constant).",
      "satisfied_evidence": "literature",
      "note": "Bound 0.177 is calculated from Floryan 2017 pitching fit c6=2.55, C_Dp=0.08 at Re 4780 (non-universal per authors). Taylor, Nudds & Thomas 2003 Nature 425:707, abstract-level. Data are cruise, not maximal speed."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "A process must cap tail-beat frequency, and the propulsive muscle's contraction-relaxation must fit within one half tail-beat period.",
      "quantity": "twitch time relative to half-period 1/(2f)", "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Fast-muscle twitch contraction time limits maximum tail-beat frequency; max observed speeds fit twitch time and stride length; twitch time rises with length, falls with temperature.",
      "satisfied_evidence": "literature",
      "note": "Wardle 1975 Nature 255:725, abstract plus secondary sources (full text paywalled); Wardle & Videler 1980 Nature 284:445, abstract via search-summary."},
    {"target_scale": "behaviour", "kind": "spatial",
      "statement": "Distance travelled per tail beat must not exceed the peak-to-peak tail amplitude times sqrt(c6/C_D).",
      "quantity": "stride length U/f divided by A_pp", "lo": null, "hi": 5.65, "units": "dimensionless (stride / A_pp)",
      "status": "satisfied",
      "satisfied_by": "Ordinary teleost stride 0.6-0.8 L (Bainbridge asymptote 0.75 L) vs ceiling 1.13 L if A_pp = 0.2 L. Scombrid strides ~2x (about 1.4 L) are within the ceiling only if A_pp >= 0.25 L or lobe C_D at Re ~1e6 < 0.08; no measured skipjack A_pp found, so unresolved, not contradicted.",
      "satisfied_evidence": "literature",
      "note": "5.65 calculated from Floryan 2017 c6, C_Dp. Wardle 1975 (secondary), Bainbridge 1958 JEB 35 (abstract), Videler 1993 stride 0.5-1 L (search-summary), coho A/L 0.20 (search-summary, pp vs half unknown), Wardle & Videler 1980 'twice as far per tail beat' (abstract via search-summary). Videler & Wardle 1991 and core.ac.uk could-not-access. Scombrid case is the open falsification test."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Available muscle power at maximum tail-beat frequency must be at least the hydrodynamic input power of the propulsor at the ceiling Strouhal number plus body drag power, otherwise power, not kinematics, sets the ceiling.",
      "quantity": "muscle power available / hydrodynamic power required at U_max", "lo": 1, "hi": null, "units": "dimensionless ratio",
      "status": "open",
      "satisfied_by": "Not checked: no search for muscle power output at maximal tail-beat frequency and no required-power calculation was done.",
      "satisfied_evidence": "unknown",
      "note": "Power law to use: Floryan 2017 eq. 2.7, C_P = c8 St^2 + c9 St^2 f*, c8=7.78, c9=4.89 (rigid foil). Wardle & Videler 1980 note scombrid style requires greater power (abstract-level), which is not a check."}
  ]}
```
