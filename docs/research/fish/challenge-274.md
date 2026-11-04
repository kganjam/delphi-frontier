# Challenge 274: the zebrafish lobe reopening condition

**Claim under review (the author's words, from S32-organism.md):**
"REOPENING CONDITION, falsifiable: an airborne zebrafish lobe beating at 1.4-2.2x its best measured
burst tail speed (A_pp 12-19 mm at 52 Hz, or 72-117 Hz at burst amplitude), or surface-piercing lobe
thrust at Re 1e4 measuring well above the 2-D foil law."
Recorded evidence level: derived. Recorded value: 2.2 times burst tail speed.

**Source access.** `S32-organism.md` is **could-not-access**. I searched every file and all 30 commits on
every branch of this repository (`grep -ri` for "S32", "zebrafish", "tail speed", "lobe") and found
nothing. So I cannot check how the author derived the 1.4-2.2x band from a force balance. Everything
below is either worked from the numbers inside the claim itself or comes from the sources I cite.

## 1. Independent arithmetic (calculated, not observed)

- The amplitude arm gives a burst A_pp of 12/1.4 = 8.57 mm and 19/2.2 = 8.64 mm. That points to a
  burst baseline of about **8.6 mm A_pp at 52 Hz**. It holds together.
- The frequency arm gives 72/52 = **1.385x** and 117/52 = **2.25x**. Read the other way, it implies a
  burst frequency of 51.4-53.2 Hz, not exactly 52 Hz. So the two arms do not describe the same band:
  2.2x at 52 Hz is 114 Hz, not 117 Hz. The error is small (about 2%) but real. My inference is that the
  bounds were rounded on their own and not computed from one baseline.
- Taking tail speed as about 2·A_pp·f, the baseline is 2 × 8.6 mm × 52 Hz ≈ **0.89 m/s** mean tip speed.
  Taking it as π·A_pp·f, the peak is ≈ **1.40 m/s**. The claim does not say which "tail speed" it means.

## 2. Proxy problem: the claim uses tail speed where force is what matters

The claim treats amplitude × frequency (tip speed) as the quantity that matters. But the reopening
question turns on force, and the two routes to the same tip speed produce different force:

- The quasi-steady (circulatory) force goes as (A·f)², which is the same on both routes.
- The added-mass, or acceleration-reaction, force goes as A·f². For the same tip-speed multiple r,
  raising frequency multiplies this term by r² (1.96x-4.84x), but raising amplitude multiplies it by
  only r (1.4x-2.2x). This scaling is calculated, not measured.

So "A_pp 12-19 mm at 52 Hz" and "72-117 Hz at burst amplitude" are offered as equal triggers, but they
are not equal in force. If the band came from a force requirement, at most one of the two arms can be
right. The proxy should be the force or impulse per beat at the stated Re, not tail speed.

In air, dynamic pressure at 1.4-2.2x tip speed is (1.2/998)·r² ≈ **0.0024-0.0058** of the water-burst
value. This is calculated from ρ_air = 1.2 and ρ_water = 998 kg/m³. My inference: no airborne beat at
2.2x could make useful aerodynamic force, so the airborne arm can only make sense as a kinematic
capability test (can the lobe reach that speed without water loading?). The claim does not say that
this is what the arm tests.

## 3. Hidden assumption carrying the result

The claim assumes **A_pp and f are independent and linearly tradeable**. In fish, amplitude normally
plateaus or falls as frequency rises, and frequency is capped by muscle contraction speed. If I relax
that assumption, the upper bound of 117 Hz is not just a "lobe beating faster". It asks the muscle to
contract about 2.25x faster than its best measured burst. Whether zebrafish muscle can do that at
adult body size is **unknown**: I found no adult maximum-frequency value (see §5).

Also unclear: is the 8.6 mm / 52 Hz baseline from one animal and one stage? An A_pp of 8.6 mm is
bigger than a whole larval zebrafish (roughly 4 mm long), so it has to be adult kinematics. My inference
is that this makes 52 Hz a high adult burst frequency. Neither number could be traced: the source is
could-not-access, and my search for adult escape kinematics (below) turned up only larval values.

## 4. Is the evidence level honest?

The label "derived" is honest for the 1.4-2.2x multiplier. But the claim's own word "**measured**"
("best measured burst tail speed") rests on a baseline I could not trace to any observation. The
second arm, "**well above** the 2-D foil law", gives no threshold. A condition with no number cannot be
falsified, so the label "falsifiable" does not hold for that arm. It needs a stated ratio and
uncertainty, for example a force coefficient above the 2-D prediction by more than k·σ.

## 5. Regimes and taxa the author may have missed

- **Flying fish (Exocoetidae) taxiing** is a natural case of surface-piercing caudal-lobe thrust, and
  it is the exact regime of the second arm. The sources disagree, and I keep the disagreement:
  - Deng et al. (bioRxiv preprint 10.1101/765560) cites field tail-beat rates of about **50 beats/s** and
    models a minimum-power optimum near **50 Hz** for a 0.25 m fish at 10 m/s. Read-level: search-summary.
  - An APS March Meeting 2024 abstract (s27/13) reports **13.5 Hz** tail slapping, measured, with about
    2 N of force for a 200 g fish. Read-level: search-summary.
  - The claim does not mention this taxon (my inference from its wording alone; S32 itself is
    could-not-access). It is a direct, testable comparison for "surface-piercing lobe thrust vs 2-D
    foil law" in a fish that actually does this.
- Low-aspect-ratio and surface-piercing foils can depart from 2-D foil theory in either direction:
  down through ventilation and wave drag, up through leading-edge-vortex lift. "Well above 2-D" is not
  the only way the condition could break. I have not quantified this; it is stated as an inference.

**Negative search scope:** two web searches on 2026-11-04 (standard mode):
1. "adult zebrafish escape response tail beat frequency Hz amplitude". This returned only larval
   values: about 37-40 Hz fast-swim and escape tail-beat frequency (ZFIN figure pages, read-level:
   search-summary). I found **no adult maximum-frequency or A_pp value**, so the 52 Hz / 8.6 mm baseline
   is **unknown** (not verified, not refuted).
2. "flying fish taxiing tail beat frequency caudal lower lobe surface". Results above. This search did
   not reach any lower-lobe-specific data.

## Verdict: WEAKENED

The number is not refuted. 2.2x is internally consistent with the amplitude arm. But:
(a) the frequency arm actually spans 1.385-2.25x, not 1.4-2.2x;
(b) the two arms are equal in tip speed but not in force, so tip speed stands in for force;
(c) the burst baseline it calls "measured" could not be traced, and the only zebrafish values I found
are larval, at about 37-40 Hz;
(d) the second arm has no threshold, so it cannot be falsified as written;
(e) flying-fish taxiing is a regime that applies directly and is not addressed in the claim.

```swarm-challenge
{"claim_id": 274, "outcome": "weakened", "reason": "The 2.2x band is internally consistent only on the amplitude arm (the frequency arm spans 1.385-2.25x), it uses tail speed as a stand-in for force even though the amplitude and frequency routes differ in added-mass force by up to 2.2x, its 'measured' 8.6 mm/52 Hz baseline is untraceable, and the 'well above 2-D foil law' arm has no threshold and so cannot be falsified.",
  "corrected_value": "1.385-2.25x burst tip speed on the frequency arm (1.40-2.21x on the amplitude arm); the force-equivalent band is unknown",
  "depends_on": ["burst baseline A_pp ~8.6 mm at 52 Hz implied by the claim's own numbers (unverified; S32-organism.md could-not-access)", "tail speed ~ A_pp*f; added-mass force ~ A*f^2 scaling (standard oscillating-foil theory, calculated)", "rho_air 1.2 and rho_water 998 kg/m3", "Deng et al. bioRxiv 10.1101/765560 (search-summary): ~50 Hz flying-fish taxiing", "APS March Meeting 2024 s27/13 abstract (search-summary): 13.5 Hz flying-fish tail slapping", "negative search: no adult zebrafish maximum tail-beat frequency found in one standard web search"]}
```

Sources:
- [Deng et al., bioRxiv 765560](https://www.biorxiv.org/content/10.1101/765560.full.pdf)
- [APS MAR 2024 s27/13](https://meetings-archive.aps.org/mar/2024/s27/13)
- [ZFIN ZDB-FIG-201003-5](https://www.zfin.org/ZDB-FIG-201003-5)
