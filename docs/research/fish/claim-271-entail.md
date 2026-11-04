# Claim 271: what it needs at the organ and behaviour scales

**Source claim (organism scale, evidence: derived):**
> THE CEILING HAS A CLEAN FORM: U_max = f·A_pp·sqrt(c6/C_D(Re)). Measured foil thrust scales with
> tail speed squared INDEPENDENT of forward speed while foil drag scales as U², so immersed area and
> mass DROP OUT. Only tail speed and lobe drag at Reynolds number matter.

**Adjacent scales:** organ (caudal fin and the axial muscle that drives it) and behaviour (free-swimming
kinematics: speed, tail-beat frequency and amplitude, distance per beat).

No experiment or simulation was run for this note. Every number below is either **measured** and
quoted from a source with its read-level, or **derived** by me with arithmetic. The text says which
in each case. Each claim is also labelled **retrieved** (I read it in this session) or **remembered**
(from prior knowledge, not checked). Nothing load-bearing is in the remembered category.

---

## 0. Where the claim comes from (retrieved, full-text)

The form of the claim matches Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.* 822:386–397,
"Scaling the propulsive performance of heaving and pitching foils". I read arXiv:1704.07478
(**full-text**, via pdftotext). Here is what the authors say:

- For a purely pitching rigid foil, eq. 2.7 gives `C_T = c6·St² + c7·St·A* − C_Dp`, with
  `St = 2fA/U∞`, where A is the *trailing-edge amplitude* (peak, not peak-to-peak), so `2A = A_pp`.
- The fitted values are `c6 = 2.55`, `c7 = 0` and `C_Dp = 0.08`. The authors add that "the values of
  the constants should not be taken to be universal".
- Dimensional thrust on the pitching foil was "independent of freestream velocity" for U∞ = 60 to
  120 mm/s. The heaving foil showed "only weakly" velocity-dependent thrust (§6, Fig. 8).
- Rig: teardrop foil with chord 80 mm, span 279 mm and AR 3.5. Chord Reynolds number was 4780 at
  60 mm/s. Pitch amplitude was θ0 = 3–15°. They **assumed** C_D was constant over their Re range.

**My inference (derived):** setting net C_T = 0 gives `St = sqrt(C_Dp/c6)`. Because `St = f·A_pp/U`,
this means `U = f·A_pp·sqrt(c6/C_Dp)`, which is claim 271's formula. With the authors' constants,
**St = 0.177 and U/(f·A_pp) = 5.65** (derived). The claim's `C_D(Re)` stands in for the authors'
constant C_Dp. That Re dependence is the claim's own extension. Floryan et al. did not measure it.

One consequence follows straight from the source. In the experiment, thrust and drag are measured on
**the same foil, with the same reference area (s·c)**. That is the only reason the area cancels. In a
fish, most of the drag is on the body and most of the thrust is on the fin. Constraint E5 below comes
from this.

---

## Constraints and checks

### E1. Behaviour: range of the Strouhal number (fA_pp/U)

**Requirement:** In steady free swimming, speed must be proportional to tail speed (U ∝ f·A_pp), and
the ratio St = f·A_pp/U = sqrt(C_D/c6) must sit in a fixed band that does not depend on body size.
**Bound:** St in [0.2, 0.4]. Through the claim (derived), this means C_D/c6 in [0.04, 0.16].

**Check: satisfied (literature).**
- Taylor, Nudds & Thomas 2003, *Nature* 425:707–711. Dolphins, sharks, bony fish, birds, bats and
  insects cruise at 0.2 < St < 0.4 (**search-summary**, retrieved). Their St is defined as fA/U with A
  the peak-to-peak amplitude (**remembered** for this paper; it is the convention Floryan's
  `2A` reproduces).
- Bainbridge 1958, *J. Exp. Biol.* 35:109–133. Dace, trout and goldfish up to 30 cm fit
  V = ¼·L(3f − 4). Tail-beat amplitude levels off at about L/5, so distance per beat follows
  amplitude (**search-summary** of the abstract, retrieved). The page range is disputed between
  sources: 109–133 (FishBase, Nature) and 129–153 (USGS).
- Gazzola, Argentina & Mahadevan 2014, *Nature Physics* 10:758–761. Over more than 1000 measurements
  (fish, amphibians, larvae, reptiles, mammals, birds), Re ~ Sw^α with α = 1 in turbulent flow and
  4/3 in laminar flow (**search-summary** of the APS DFD abstract, retrieved).
  **My inference (derived):** if C_D is constant, claim 271 gives U ∝ fA, so α = 1. If C_D ∝ Re^(−1/2)
  (Blasius), it gives U ∝ (fA)^(4/3)·(L/ν)^(1/3), so α = 4/3. Both of Gazzola's regimes therefore come
  out of the claim's C_D(Re). This is an agreement between two derivations. It is not a separate
  measurement.

**Disagreement kept:** the foil constants predict St = 0.177 (derived). That falls **below** the
measured animal band of 0.2–0.4. The claim survives only if a whole fish's C_D, referenced to fin
area, is larger than a bare foil's C_Dp = 0.08 (see E2 and E5).

### E2. Behaviour: distance travelled per tail beat (spatial)

**Requirement:** stride length U/f = A_pp·sqrt(c6/C_D) must match the measured distance per tail beat
to within a factor of 2.
**Bound:** 0.6–0.8 body lengths per beat.

**Check: satisfied (measured), with a quantitative gap stated.**
- Svendsen et al. 2016, *Biology Open* 5:1415–1419 (PMC5087677; **full-text**, read through an
  automated page summary). Measured stride lengths: sailfish 0.76, barracuda 0.63, little tunny 0.65,
  dorado 0.65 L per beat. The authors say fish "rarely exceed about 1 body length per stride".
- The 0.6–0.8 L range that the paper attributes to Wardle 1975 (**search-summary**).

**My inference (derived):** with A_pp ≈ 0.2 L (Bainbridge), a stride of 0.6–0.8 L requires
sqrt(c6/C_D) = 3.0–4.0. With c6 = 2.55, that means **C_D,eff = 0.16–0.28**. The bare-foil
C_Dp = 0.08 would predict a stride of **1.13 L** (derived). That is 1.4–1.9× above the measured
strides and slightly above the "rarely > 1 L" ceiling. So the formula's shape fits the data, but the
foil-measured drag coefficient does not carry over to the fish. The fish must carry about 2–3.5× the
foil's drag, referenced to the same area. The claim's C_D(Re) has room for this, so this is not a
refutation. It does mean c6 and C_D cannot both be taken from the foil experiment.

### E3. Organ: muscle twitch versus tail-beat half-period (timescale)

**Requirement:** U_max depends on f, so something must cap f. The ceiling only exists if one
half-period of the tail beat cannot be shorter than the minimum contraction time t_c of the axial
muscle: f_max = 1/(2·t_c).
**Bound:** t_c in [0.047, 0.0685] s measured, giving f_max of 7.3–10.6 Hz (derived) for 1–3 m pelagic
predators.

**Check: satisfied (measured), with a disagreement in the literature.**
- Wardle 1975, *Nature* 255:725–727. Maximum observed speeds "fit the dimensions of the muscle
  twitch" via V = 0.7·L/(2t). Contraction time grows with fish length and shrinks as temperature rises
  (**search-summary**; full text not read).
- Svendsen et al. 2016 (**full-text** via summary). Minimum twitch times measured at 45% fork length:
  sailfish 68.5 ± 7.2 ms, barracuda 47.0 ± 10.8 ms, little tunny 48.3 ± 2.8 ms, dorado
  56.7 ± 10.3 ms. Their tail-beat limits are 7.4, 11.1, 10.4 and 9.1 Hz. The authors flag a key
  assumption: minimum contraction time does not depend on load.
- **Opposing evidence:** Wardle & Videler 1980 (*Nature* 284:445) reportedly note observed speeds
  above the predicted limit, for example skipjack tuna (**search-summary**, not read). Either the twitch
  limit is not the only cap on f, or the measured overshoots are wrong. I did not settle which.

**My inference:** size enters U_max through t_c(L), so "mass drops out" holds only at fixed tail
speed. Across sizes, the ceiling still depends on size through the muscle. The claim as worded
("only tail speed and lobe drag matter") is consistent with this, because tail speed carries the
size dependence. A reader should not take "mass drops out" to mean U_max is independent of size.

### E4. Organ: thrust independent of forward speed over the full range (range)

**Requirement:** the fin's mean thrust at fixed f and A_pp must not depend on U, from cruising speed up
to U_max, at the fin's real Reynolds number. If thrust falls off with U, the U_max formula
overestimates.
**Bound:** the propulsor chord Reynolds number must cover the operating range, at least
Re_c of about 5×10³ to 10⁶ (lower bound measured, upper bound **assumed** as an order of magnitude for
metre-scale fish at several m/s; I did not compute it from measured fin chords).

**Check: open. Partly measured at the low end only.**
- Floryan et al. 2017 (**full-text**): pitching thrust did not depend on U for U∞ = 60–120 mm/s,
  Re_c ≈ 4.8×10³ to 9.6×10³. Heaving thrust depended on U "only weakly".
- Van Buren, Floryan, Wei & Smits 2017/18, arXiv:1707.05608, "Flow speed has little impact on
  propulsive characteristics of oscillating foils" (**full-text**, sections read). Same rig and same
  60–120 mm/s range. "In pitching motions… the mean velocity has no measurable impact on the magnitude
  of the thrust. In heaving motions, there is little impact." Streamwise velocity oscillations of up to
  38% of the mean changed little.
- A fish caudal fin heaves and pitches at the same time. The heave part is the one with residual
  U-dependence.

**Scope of the negative:** I found measurements over one factor-of-2 velocity range at
Re_c ≤ 10⁴. I **did not search** for U-independence tests on oscillating foils at Re_c of 10⁵–10⁶ or
on live fish. This is "not looked", not "looked and found nothing". Burst speeds are 2× or more above
cruise, and their Re is 2–3 orders above the tested range, so the claim leans on an extrapolation that
nobody in my sources has tested.

### E5. Organ: thrust area and drag area must scale together (spatial)

**Requirement:** area drops out only if the drag in the formula uses the **same reference area** as
the thrust (fin area S_fin). In a fish, C_D,eff = C_D,body·(S_wet/S_fin). For U_max to be independent
of area across individuals or species, S_wet/S_fin must stay roughly constant (geometric similarity).
At the least it must not vary by more than a factor of about 4, which would move sqrt(C_D) by 2×.
**Bound:** variation in S_wet/S_fin across the size range within a factor of 4 (lo = 0.25, hi = 4,
relative to a reference fish). The bound is my choice, derived from the factor-of-2 tolerance in E2.

**Check: open.** I did not retrieve any measured scaling of caudal-fin area against wetted body area.
E2 suggests (derived) that whole-fish C_D,eff is about 2–3.5× the bare-foil value. That is what an
added body-drag term would do, but it tells us nothing about how the ratio changes with size. This
constraint is the one most directly tied to the claim's headline that "immersed area drops out". It has
not been checked.

### Not entered: energetic

Being kinematically possible does not make a speed reachable. Muscle power has to cover T·U at U_max,
and available power scales with muscle mass. That is the route by which mass could come back in. I
did not search for measured burst power of fish white muscle, so I am not stating it as a constraint
with numbers. It is the obvious next thing to check.

---

## Summary

| # | Scale | Kind | Status | Basis |
|---|---|---|---|---|
| E1 | behaviour | range | satisfied | St 0.2–0.4 (Taylor 2003); U ∝ fA (Bainbridge 1958); Gazzola 2014 regimes reproduced (derived) |
| E2 | behaviour | spatial | satisfied | strides 0.63–0.76 L measured (Svendsen 2016); bare-foil constants overpredict at 1.13 L (derived) |
| E3 | organ | timescale | satisfied | twitch 47–68.5 ms gives 7.4–11.1 Hz (Svendsen 2016); Wardle 1975; overshoots disputed (Wardle & Videler 1980) |
| E4 | organ | range | open | U-independence measured only for 60–120 mm/s, Re_c ≤ 10⁴; higher Re not searched |
| E5 | organ | spatial | open | S_wet/S_fin scaling not retrieved |

**Nothing came out unsatisfiable.** No measured number I found contradicts the claim. The closest is
the bare-foil prediction (St 0.177, stride 1.13 L). It conflicts with measured fish kinematics only
if one insists on C_D = C_Dp(foil), and the claim does not, since it writes C_D(Re). The real
weaknesses are E4 (extrapolation in Re) and E5 (the area cancellation for a body-plus-fin swimmer).
Both are untested, not refuted.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| Floryan, Van Buren, Rowley & Smits 2017, JFM 822:386 (arXiv:1704.07478) | full-text | origin of the formula; c6 = 2.55, C_Dp = 0.08; U-independence at 60–120 mm/s |
| Van Buren, Floryan, Wei & Smits, arXiv:1707.05608 | full-text (sections) | U-independence of pitch and heave thrust; same range |
| Taylor, Nudds & Thomas 2003, Nature 425:707 | search-summary | St 0.2–0.4 |
| Bainbridge 1958, J. Exp. Biol. 35 (pages disputed) | search-summary | V = ¼L(3f−4); amplitude about L/5 |
| Gazzola, Argentina & Mahadevan 2014, Nat. Phys. 10:758 | search-summary (APS abstract) | Re ~ Sw^(1 or 4/3) |
| Wardle 1975, Nature 255:725 | search-summary | twitch-time speed limit; V = 0.7L/2t |
| Wardle & Videler 1980, Nature 284:445 | search-summary | speeds above the twitch limit reported |
| Svendsen et al. 2016, Biol. Open 5:1415 (PMC5087677) | full-text (automated summary) | twitch times, tail-beat limits, stride lengths |
| Rohr & Fish 2004, J. Exp. Biol. 207:1633 | listing (cited in Floryan, not read) | not used directly |

```swarm-entail
{"source_claim": 271, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "In steady free swimming, speed must be proportional to tail speed (f*A_pp) with a size-independent Strouhal number St = f*A_pp/U = sqrt(C_D/c6)",
      "quantity": "Strouhal number f*A_pp/U", "lo": 0.2, "hi": 0.4, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Cruising fish, cetaceans, birds, bats and insects at 0.2<St<0.4; Bainbridge's U = 1/4 L(3f-4) with amplitude about L/5; Gazzola's Re~Sw (turbulent) and Re~Sw^(4/3) (laminar) both follow from the claim with C_D constant or C_D ~ Re^-1/2 (derived)",
      "satisfied_evidence": "literature",
      "note": "Taylor, Nudds & Thomas 2003 Nature 425:707 (search-summary); Bainbridge 1958 J Exp Biol 35 (search-summary, page range disputed 109-133 vs 129-153); Gazzola et al. 2014 Nat Phys 10:758 (search-summary of APS abstract). Disagreement: bare-foil constants of Floryan 2017 (c6=2.55, C_Dp=0.08) give St=0.177 (derived), below the animal band."},
    {"target_scale": "behaviour", "kind": "spatial",
      "statement": "Distance travelled per tail beat, U/f = A_pp*sqrt(c6/C_D), must match measured stride length within a factor of 2",
      "quantity": "stride length per tail beat", "lo": 0.6, "hi": 0.8, "units": "body lengths per beat",
      "status": "satisfied",
      "satisfied_by": "Measured strides 0.76 (sailfish), 0.63 (barracuda), 0.65 (little tunny), 0.65 (dorado) L/beat; with A_pp about 0.2 L these require sqrt(c6/C_D)=3-4, i.e. C_D,eff=0.16-0.28 for c6=2.55 (derived). Bare-foil C_Dp=0.08 would predict 1.13 L/beat (derived), 1.4-1.9x too long",
      "satisfied_evidence": "measured",
      "note": "Svendsen et al. 2016 Biol Open 5:1415, PMC5087677 (full-text via automated summary); 0.6-0.8 L range attributed to Wardle 1975 (search-summary). The formula fits only if whole-fish drag referenced to fin area exceeds the bare-foil value by about 2-3.5x."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The tail-beat half-period must be bounded below by the minimum contraction time of the axial propulsive muscle, so that f (and hence U_max) has a ceiling: f_max = 1/(2 t_c)",
      "quantity": "minimum muscle twitch contraction time t_c", "lo": 0.047, "hi": 0.0685, "units": "s",
      "status": "satisfied",
      "satisfied_by": "Measured minimum twitch times 47.0-68.5 ms at 45% fork length in barracuda, little tunny, dorado and sailfish give tail-beat limits of 7.4-11.1 Hz; Wardle's twitch-limited speed law V = 0.7 L/(2t)",
      "satisfied_evidence": "measured",
      "note": "Svendsen et al. 2016 Biol Open 5:1415 (full-text via summary; assumes t_c is independent of load); Wardle 1975 Nature 255:725 (search-summary). Disagreement kept: Wardle & Videler 1980 Nature 284:445 report observed speeds above the predicted limit, e.g. skipjack (search-summary). t_c rises with body length, so size re-enters U_max through f_max."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Mean propulsor thrust at fixed f and A_pp must be independent of forward speed across the operating range up to U_max, at the propulsor's actual chord Reynolds number",
      "quantity": "propulsor chord Reynolds number over which thrust is U-independent", "lo": 5000, "hi": 1000000, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Measured U-independence of pitching-foil thrust (and weak dependence for heave) only for U = 60-120 mm/s, Re_c about 4.8e3-9.6e3; no test found at Re_c of 1e5-1e6 or on live fish",
      "satisfied_evidence": "measured",
      "note": "Floryan et al. 2017 JFM 822:386, arXiv:1704.07478 (full-text); Van Buren et al. arXiv:1707.05608 (full-text sections). Upper bound 1e6 is an assumed order of magnitude, not computed. Negative scope: I did not search for high-Re or in-vivo tests. This is 'not looked', not 'looked and found nothing'."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "For immersed area to drop out, drag must be referenced to the same area as thrust: the ratio of drag-bearing (wetted body) area to thrust-producing (caudal fin) area must stay roughly constant across sizes",
      "quantity": "S_wet/S_fin relative to a reference fish", "lo": 0.25, "hi": 4, "units": "dimensionless ratio",
      "status": "open",
      "satisfied_by": "not searched; no measured scaling of caudal-fin area against wetted area retrieved",
      "satisfied_evidence": "unknown",
      "note": "In Floryan 2017, thrust and drag act on the same foil with the same reference area (s*c), which is why area cancels there (full-text). The factor-4 bound is my choice, derived from E2's factor-2 tolerance on stride. Not checked."}
  ]}
```
