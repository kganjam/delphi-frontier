# Challenge 51: "LAWENTRY weis-fogh dispatched"

- **Claim under attack:** "LAWENTRY weis-fogh dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_016kCs8JW1Mm75rqfF8KL6wv`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict:** WEAKENED. The dispatch is real and delivered an entry, and the entry's arithmetic
  reproduces. But one load-bearing conclusion in that entry is contradicted by a published
  measurement the author did not find. That conclusion is the Re-bound and the "no gain should be
  assumed at Re ~1333" judgement.

## What the claim asserts, and what matters

Read literally, the claim records an operation: a Weis-Fogh law-library task was dispatched.
"Dispatched" is a **proxy**. What matters is whether the library now holds a correct, gated
Weis-Fogh entry that can safely be used to check a design. I tested both.

## 1. Was it dispatched, and did it deliver? (observed, from git)

- When I first looked (around 08:10 UTC), no branch, commit or file mentioning Weis-Fogh existed
  on any of 254 remote branches. A second `git fetch` showed `origin/claude/weis-fogh-law-entry-jc3w7t`.
  The work landed while this review was running.
- Commit `12d90144` ("Add Weis-Fogh clap-and-fling law entry, with the Re bounds where the lift gain
  fails", 2026-11-04 08:10:48 UTC) carries the trailer
  `Claude-Session: .../session_016kCs8JW1Mm75rqfF8KL6wv`, which matches the claim's source. It adds
  `library/laws/weis-fogh.yaml` (223 lines), `library/pages/weis-fogh.md` and one line in the index.
  This is observed: I read it from git.
- I ran the repository gate on an extracted copy of that commit:
  `check_laws.py --dir library/laws` gave **3 entries, 0 problems**, and `--selftest` passed, including
  its wrong-Reynolds negative control. This is observed, but the gate checks dimensions and fields
  only, not whether the content is right.
- `get_session` on the source session returned "not found", so I could not inspect the session itself.
  The commit trailer is the only link between the two.

**Scope of negative findings:**
- `git branch -r --contains 12d90144` lists only the feature branch.
- `library/laws/weis-fogh.yaml` is absent on `origin/main`.
- `gh api search/issues` with `is:pr head:claude/weis-fogh-law-entry-jc3w7t` returned 0.

So the entry is dispatched and delivered, but **not merged**, and I found no PR. The word "dispatched"
does not claim more than that.

## 2. Arithmetic, redone independently (calculated by me)

| Entry states | My result | Match |
|---|---|---|
| Γ = 0.69 × 100 rad/s × (0.01 m)² | 6.90×10⁻³ m²/s | yes |
| Kutta–Joukowski L′ = 1.2 × 2 × 6.9×10⁻³ | 0.01656 N/m (entry: 0.0166) | yes |
| Re of the project wing (reynolds.yaml): 2 × 0.01 / 1.5×10⁻⁵ | 1333 | yes |
| Dimensions: g(φ)·Ω·c² → L²/T, as Γ | yes | yes |

The 0.69 coefficient is Lighthill's. I could not access Lighthill (1973) (read-level:
could-not-access, not attempted beyond search). I neither confirm nor dispute it. The entry already
labels it as search-summary, CALCULATED, and inviscid.

## 3. Hidden assumption, relaxed: "the gain fades with Re, so expect little at Re ~1333"

The entry's `where_it_breaks` (1) is headed "ABOVE Re ~ 64 THE AUGMENTATION LARGELY DISAPPEARS --
calculated and measured". It sets `reynolds_max: 200`. In (7) it concludes, as **its own inference**,
that no clap-and-fling lift gain should be assumed for the Re ~1333 project wing, and that the
trend in (1) "suggests a small gain at most".

That inference extrapolates a low-Re trend, mostly from 2D CFD (Miller & Peskin 2005), across
roughly an order of magnitude in Re. There is a published measurement on the far side of Re 1333
that contradicts it:

- **Phan HV, Au TKL, Park HC (2016)**, "Clap-and-fling mechanism in a hovering insect-like two-winged
  flapping-wing micro air vehicle", *R Soc Open Sci* 3(12):160746, PMC5210694. Read-level: abstract
  quoted directly, plus the rest of the PMC full text through an automated summarising fetch (only the
  first 100k of 104k characters were processed). The values reported there are:
  - **Measured** (6-axis load cell, Re ≈ 15,000): mean vertical force 116.7 mN with clap-and-fling
    vs 100.4 mN without. That is **+16.2 %**, and I recomputed the ratio as 1.162.
  - **Calculated** (3D CFD, same Re): 120.4 vs 108.0 mN, or **+11.5 %** (I recomputed 1.115).
    Horizontal drag rose 18.4 % (CFD only). The CFD splits the gain 62.6 % fling and 37.4 % clap.
  - The effect became insignificant once the minimum wing separation exceeded 1.2 chords. This agrees
    in kind with the entry's geometry condition (3), but is expressed in chords, not degrees.

**My inference**, kept separate from the source: a measured whole-cycle vertical-force gain of
~16 % at Re ~15,000 means the entry's (1) heading does not generalise to "measured above Re ~200".
The "small gain at most" extrapolation in (7) is not supported, and the evidence points the other
way at Re above the project wing's.

The entry's own negative is properly scoped ("We found no measured whole-cycle augmentation above
Re ~200 (scope: ...)"). So this is a **search gap, not a dishonesty**. But `reynolds_max: 200` and
the (7) judgement are what a downstream check would actually use.

Caveats on the counter-example, which keep it from being decisive:

- The Phan MAV has flexible membrane wings and a ~190° stroke amplitude. It is a robot, not an
  animal, and not the project's wing.
- I did not verify how the "without clap-and-fling" condition was produced. If it was produced by
  changing the kinematics (for example the stroke amplitude or wing spacing), the comparison is not
  perfectly controlled.
- So the right correction is "a gain of order 10–16 % has been measured and computed at
  Re ~1.5×10⁴ on a flexible-wing MAV; whether it applies to the project wing is unknown". It is not
  "assume +16 %".

Related, lower confidence (search-summary only, numbers not verified): DelFly II "clap-and-peel"
work (TU Delft, e.g. Perçin & Remes, AIAA J 2017) reports force and PIV evidence of clap-generated
thrust at Re of order 10⁴. One DelFly thesis summary reports that the clap itself attenuates lift
while the peel enhances it. These sources disagree with each other, and I record that without
reconciling it.

## 4. Evidence level

- The claim's own level is "unknown". For a dispatch event, the honest level is "observed" (a commit
  with a matching trailer). "unknown" understates rather than overclaims.
- Inside the entry, labelling is careful throughout. CALCULATED, MEASURED and DERIVED are
  distinguished. The Danio worked example is flagged DERIVED with an assumed Ω. The placeholder lower
  bounds (0.0, 1) are declared as the author's own. I found no derived number presented as measured.
- One minor point: Lehmann & Pick (2007) is labelled `read_level: full-text` although the entry's own
  note says only ~100k of ~180k characters were processed by a summarising fetch. "Partial full-text"
  would be more accurate. This is not load-bearing.

## 5. Regimes and counter-examples

- **Missed: Re ~10⁴ (flapping MAVs).** See §3. This is the substantive finding.
- **Preserved correctly:** the Lighthill vs Maxworthy mechanism dispute, the benefit vs inefficiency
  dispute at Re ~10, and the 1.4–70 % magnitude spread. All are recorded unreconciled, as they should be.
- I did not obtain Bennett (1977, J Exp Biol 69:261) or Cooter & Baker (1977, Nature 269:53, locust
  clap). The journal fetch for Bennett returned the wrong article (read-level: could-not-access).
  Both are older physical-model or animal studies at Re above 200 that the entry does not list.
  I make no claim about their numbers.

## Verdict

**WEAKENED.**

What holds:
- The literal claim is true. Session `016kCs8JW1Mm75rqfF8KL6wv` dispatched and delivered commit
  `12d90144`.
- The entry passes `check_laws.py`, and all its arithmetic reproduces.

What is weakened:
- The deliverable that "dispatched" stands in for has a defect. `reynolds_max: 200` and
  `where_it_breaks` (1)/(7) ("augmentation largely disappears above Re ~64", "small gain at most"
  for the Re ~1333 wing) are contradicted by Phan et al. (2016). They measured +16.2 % mean vertical
  force (CFD +11.5 %) from clap-and-fling at Re ≈ 15,000.

Suggested fix to the entry, not applied here:
- Add Phan 2016 to the sources and to `contested_by`.
- Raise the evidence span to Re ~1.5×10⁴, flagged as flexible-wing MAV.
- Rewrite (7) to say that the gain at Re ~1333 is unknown and bracketed by evidence on both sides,
  rather than "small at most".
- The entry is still unmerged and no PR was found.

```swarm-challenge
{"claim_id": 51, "outcome": "weakened", "reason": "The dispatch is real (commit 12d90144, matching session trailer, passes check_laws.py, arithmetic reproduces), but the delivered entry's reynolds_max 200 and its 'small gain at most at Re ~1333' inference are contradicted by Phan et al. 2016 (R Soc Open Sci 3:160746), who measured a +16.2% clap-and-fling vertical-force gain at Re ~15,000 (CFD +11.5%).", "corrected_value": null}
```
