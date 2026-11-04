# Challenge 195: adversarial review of S28's "cheapest decisive measurement"

**Claim under review** (claim 195, source `S28-organism.md`, recorded evidence level **derived**, value n/a):

> CHEAPEST DECISIVE MEASUREMENT: pectoral fin AREA in the existing Daane double heterozygote. Daane et al.
> measured fin LENGTH only and never reported area, so the animal exists and the measurement does not. It
> decides whether even the small phenotype is detectable.

**What I read:**

- `docs/research/fish/S28-organism.md` at `origin/claude/s28-organism-design-5z0vjz` (the only branch in this
  repo carrying the file). Read-level: **full-text** for §3.5–§6; I read §4 item 1 and §5 line-by-line.
- Daane et al. 2021, "Modulation of bioelectric cues in the evolution of flying fishes", *Curr. Biol.*
  31:5052, doi 10.1016/j.cub.2021.08.054, via PMC9172250. Read-level: **full-text via an automated page
  summarizer, first ~100,000 of 149,104 characters** (the tail, which holds part of the back matter, was not
  read). I did **not** view the figure images themselves; I have only the legend and body text.
- Web search for a 2D flat-plate CL_max at Re 500–1000. Read-level: **search-summary**. Scope and result in §4.

I measured nothing. Every number below is **calculated** by me with `python3 -I` from the inputs stated in
S28, unless tagged otherwise.

## Verdict: WEAKENED

Two of the claim's three parts hold, and I confirmed the literature part against the paper's own text rather
than the author's note:

- **"measured fin LENGTH only and never reported area" — survives, now at full-text read-level.** Daane et al.
  state "we measured fin length as a function of body size (standard length)"; Fig. 4's legend says "Brackets
  indicate length of pectoral fin" and "In (B) and (C), length normalized by SL." The words *area*, *ImageJ*
  and *Fiji* do not appear in the ~100 k characters I read. S28's own table already flagged this honestly,
  including that it had not read Fig. 4B's numeric values.
- **Area is the single linear lever on lift — survives.** My arithmetic reproduces the author's exactly (§1).

What fails is the load-bearing word: **decisive**. It fails three ways, each independent of the others:

1. By the author's **own** decision rule, one of the three bracketing cases the author offers — the isometric
   case B, S = 125 mm² — falls in a band where the rule returns no verdict (§3).
2. The §3.6 phenotype the measurement is said to decide is a **product** in which S is one factor and an
   **unobserved behaviour** (does the fish abduct its pectorals during a leap?) is another. S28 states that
   behaviour "has never been observed". A zero in that factor makes any S undetectable (§2).
3. Photographic spread-fin area is a **proxy** for the quantity in the lift equation, and the gap between them
   is set by S25's own unresolved 149× stiffness dispute (§2).

"Cheapest" is also overstated, in one small way and one larger one (§5).

## 1. Independent arithmetic — reproduces, with one 1 % internal inconsistency

Inputs taken from S28: m = 0.25 g, ρ = 1.225 kg m⁻³, g = 9.81, CL_max = 1.07, span b = 2 × 13.5 + 4 = 31 mm,
burst 0.45–1.38 m/s. W = mg = **2.4525e-3 N**.

AR = 5 at b = 31 mm gives S = 961/5 = **192.2 mm²**, which is the author's case-C area.

| S (mm²) | V_to = √(2W/ρSCL) | lift at 1.38 m/s | lift at 0.45 m/s |
|---|---|---|---|
| 57 (case A) | 8.103 m/s | **2.90 % W** | 0.31 % |
| 60 (rule's lower threshold) | 7.897 | 3.05 % | 0.33 % |
| 125 (case B) | 5.471 | **6.36 % W** | 0.68 % |
| 190 (rule's upper threshold) | 4.438 | 9.67 % | 1.03 % |
| 192.2 (case C) | **4.412** | **9.78 % W** | 1.04 % |

Case A's 8.10 m/s and case B's 5.47 m/s match S28 to three figures. The rule's "≤ 3 % W" and "10 % W" anchors
are internally consistent with its ~60 and ~190 mm² thresholds. **There is no arithmetic fault in the claim.**

One inconsistency, immaterial to the verdict but worth recording because other S28 numbers are divided by it:
S28's headline case-C V_to is **4.37 m/s**, but 192.2 mm² gives **4.412 m/s**. 4.37 corresponds to
S = 196.0 mm², i.e. AR = 4.90, not 5.00. Carrying my value through S28's own scaling, the area needed to fly
at 1.38 m/s is 192.2 × (4.412/1.38)² = **1963 mm²**, and from first principles 2W/(ρ·1.38²·CL) =
**1965 mm²**, against S28's 1925 mm². Both are ~19–20 cm², so the "10× the fish's own lateral area" conclusion
is untouched.

## 2. The proxy, and the factor that is not S

**The quantity in the lift equation is not anatomical area.** It is the time-averaged area projected normal to
the flow during the ascent, multiplied by the CL actually achieved in that posture. S28's recommended protocol
— anaesthetise, **spread** the fin, one calibrated photograph — returns the maximum anatomical planform area
of a manually flattened fin. That is an **upper bound** on the quantity that matters, and the size of the gap
is unknown for two reasons S28 itself documents elsewhere:

- **Abduction is unobserved.** §3.6 conditions the whole phenotype on "**if** the fish spreads its pectorals
  during the leap. Whether it does so has never been observed." Lift scales as (projected area), so a fish
  that keeps its pectorals adducted through the ascent yields a detectable phenotype at **no** value of S in
  the bracket. This is the author's own caveat; my inference is the consequence for the word *decisive* — a
  measurement of one factor in a product cannot decide the product when a second factor is an unobserved
  binary. The claim as recorded drops that condition, which §3.6 states.
- **Planarity under load is disputed.** S28 §4 item 3 puts the required EI at leap loads at ~6.3e-5 N m² and
  reports S25 as unresolved between 3.8e-6 and 565e-6 N m² — a **149×** spread straddling the requirement. On
  the low branch the fin deflects in a leap, so flattened-photograph area overestimates the in-flight
  projected area by an unquantified factor; on the high branch it holds. S28 says as much ("This changes
  whether case C's lift is actually realised") while still ranking stiffness third.

**Right quantity, and how to get it:** the projected pectoral planform area and incidence during an actual
ascent, i.e. a dorsal/lateral high-speed video of a leap. That is the author's candidate 2, which also returns
exit speed and, by fitting ascent deceleration, **the §3.6 phenotype itself** rather than an input to it. S28
concedes the structure of this objection in its own candidate 2 — "Combine it with (1) in the same session" —
without drawing the conclusion that this makes (1) non-decisive on its own.

## 3. The decision rule is undefined over the most plausible outcome

S28's rule, verbatim:

- S ≤ ~60 mm² (AR ≥ 15): "Declare the aerodynamic phenotype undetectable and close the line."
- S ≥ ~190 mm²: "Proceed to film leaps."

The author's own three bracketing cases are A = 57, B = 125, C = 192 mm². So case A closes the line, case C
proceeds, and **case B returns nothing** — and case B is the isometric case, the one that follows if the
elongated fin keeps wild-type shape. By my arithmetic case B gives **6.36 % W** at the measured burst maximum,
which is neither the rule's ≤ 3 % "undetectable" nor its 10 % "proceed".

Taking the author's own bracketing at face value, the proposed measurement is decisive in at most **2 of 3**
enumerated outcomes, over a band 60–190 mm² that is 3.2× wide in area. A measurement that returns "no verdict"
across the middle third of its own prior is a **screening** measurement, not a decisive one. This is the
cleanest break I found, because it needs no input the author did not supply.

## 4. Hidden assumption: CL_max = 1.07 at Re of a few hundred, and the thresholds move with it

Both rule thresholds are **linear in CL**, which is assumed, never measured, and sits at a Reynolds number
where I could not verify it.

Re = Vc/ν with ν_air = 1.5e-5 m² s⁻¹: case A's 3 mm chord at 1.38 m/s gives **Re ≈ 276**; case C's mean chord
192.2/31 = 6.2 mm gives **Re ≈ 570** (**1824** at the 4.41 m/s take-off speed). These are my calculations.

Relaxing CL, holding V = 1.38 m/s, the area needed for the rule's 10 % W "proceed" threshold:

| CL_max | S for 10 % W |
|---|---|
| 1.07 (S28) | **196 mm²** |
| 0.80 | **263 mm²** |
| 0.67 | **314 mm²** |

**Scope of my search, stated beside the finding:** I searched for a 2D flat-plate CL_max at Re 500–1000 and
**found nothing below Re ≈ 10⁴** — so I cannot assert that 1.07 is wrong, and I will not invent a correction
factor. Two things the search did return, which **disagree with each other** on how much this matters, and
which I therefore keep separate rather than averaging:

- Flat plates are reported as relatively **insensitive** to Re within tested ranges, with peak lift
  "virtually unchanged" where NACA 0012 and Clark-Y peak lift more than doubles. This **supports** S28's use
  of a single CL across regimes.
- A CFD study reports a finite flat-plate **wing** CL,max of about **0.67** at Re = 3×10⁵ — a 3D value, three
  orders of magnitude above S28's regime, and **37 % below** S28's 1.07. A zebrafish pectoral at AR 5 is a
  finite wing, not a 2D section.

If the 3D figure is the better analogue, the "proceed" threshold moves to ~314 mm², i.e. **above every one of
the author's three bracketing cases** — in which case the area measurement cannot return "proceed" at all, and
the rule collapses to a single outcome. That possibility is unresolved, and it is unresolved on an input the
claim does not list.

## 5. Is it the cheapest?

- **A cheaper partial route exists.** Daane et al. Fig. 4 shows pectoral fins with length brackets in images
  normalised to SL. Planimetry of the **published figure** costs minutes, needs no animal, and would bracket
  area for free. I did **not** view the figure images, so I cannot say whether their resolution, orientation
  or fin posture supports it — this is a lead, not a result. It is weaker than S28's protocol for exactly the
  §2 reason (figure fish are not deliberately spread), but it is strictly cheaper than handling a fish.
- **"The animal exists" understates the cost, modestly.** The *genotype* has been made and both parent lines
  exist, which is the author's point and is fair. But a double heterozygote is produced by a **cross**: a lab
  that does not already hold both lines needs a line request, a cross, and rearing to adult before the
  "hours of work" photograph. S28's "hours" scopes the photography step only. This does not change the
  ranking against candidates 2–4, which need the same animals.

## 6. Searches that came back negative, with their scope

- **Numeric Fig. 4B pectoral length/SL values for the double het:** not found in the ~100 k characters of
  PMC9172250 I read. The automated reader reports they are presented graphically only. Scope: body text and
  figure legends of that one article; I did not open the supplementary data files or the bioRxiv preprint
  (biorxiv.org/content/10.1101/2021.03.05.434157v1), either of which may carry them. So the claim's own
  "length only, area never" stands, and the underlying length value remains **unknown** to me as a number.
- **Any published zebrafish pectoral fin *area* for *longfin* or *lat4a* genotypes:** not searched
  systematically. I checked only the Daane 2021 paper itself. The regeneration literature routinely measures
  caudal fin area, so a published pectoral area for *lof/+* alone cannot be ruled out from what I did; it
  would not rescue the double het, which is the genotype at issue.
- **2D flat-plate CL_max at Re 500–1000:** searched, nothing found below Re ≈ 10⁴ (§4).

## 7. Evidence level

Recorded as **derived**. That is **honest**, and better than the alternatives: the claim's content is a
recommendation resting on a calculated lift relation and on a documented absence in the literature, and S28
labels the absence as "literature, length only" and its own fin areas as "never measured" / "extrapolated"
throughout. S28's honesty ledger explicitly lists CL and the case-B/C areas as assumed. I found no instance of
a calculation presented as an observation in the material under review. The one defect of this kind is in my
§1 note — S28's 4.37 m/s is quoted as if it followed from AR = 5, and it follows from AR = 4.90 — which is a
rounding slip, not a mislabelled evidence level.

## 8. What I could not break

- The arithmetic. Every reproducible number matched.
- The literature absence, which I verified at full-text read-level rather than trusting the note.
- The ranking against candidates 3 and 4. Stiffness (3) is an input to the same product and no cheaper;
  muscle mass (4) is irrelevant once launch fails.
- The "it cannot flip the flight verdict" sub-claim: ~1965 mm² (my value) on a 3 cm fish is out of reach, and
  my recomputation moved it the wrong way for the claim's opponent.

**Net:** the measurement is still the right **first** thing to do and the claim's facts are sound. It is a
cheap **screening** measurement that returns no verdict over the middle third of its own prior and that
decides one factor of a product whose other factors are an unobserved behaviour and a 149×-disputed stiffness.
On the §3.6 phenotype as stated, the decisive measurement is the high-speed leap video — the author's
candidate 2, which S28 already proposes running in the same session.

```swarm-challenge
{"claim_id": 195, "outcome": "weakened", "reason": "The arithmetic and the literature absence both hold at full-text read-level, but 'decisive' does not: the author's own rule returns no verdict over 60-190 mm2, which contains the isometric case S=125 mm2 (6.36% W by my calculation), and area is one factor of a product whose other factors are an abduction behaviour S28 says has never been observed and a 149x-disputed ray stiffness.", "corrected_value": "decision rule undefined over 60-190 mm2; case B S=125 mm2 gives 9.78%-scaled lift of 6.36% W at 1.38 m/s; case-C V_to is 4.412 m/s at AR=5 (S=192.2 mm2), not 4.37 m/s", "depends_on": ["S28-organism.md section 3.6 (phenotype conditional on unobserved pectoral abduction)", "S28-organism.md section 4 item 1 (decision rule thresholds 60 and 190 mm2)", "S28-organism.md cases A/B/C fin areas 57/125/192 mm2", "S28-organism.md span b = 2x13.5 mm + 4 mm = 31 mm", "CL_max = 1.07 (assumed, unverified at Re 276-570)", "m = 0.25 g, SL = 3.0 cm (assumed)", "Miln2021-burst (0.45-1.38 m/s)", "Daane2021-genetics (Curr. Biol. 31:5052, PMC9172250, length-only measurement)", "structure/S25 (ray EI 3.8e-6 vs 565e-6 N m2, unresolved)"]}
```
