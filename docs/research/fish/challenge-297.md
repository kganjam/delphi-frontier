# Challenge 297: adversarial review of S3-D-D ("CL remains the only input whose factor-2 error flips S3-D")

**What I reviewed.** `docs/research/fish/S3-D-deepen.md` and `S3-D-deepen_calc.py` on branch
`claude/deepen-s3-sensitive-input-gqmmly` (commit `2bc2392d`). I read both in full. I did not re-read
S3 or S3-D. Where I use their inputs, I take them as S3-D-D states them.

**Status: derived.** Every number below is **calculated**. None of it is an observation. They come
from `python3 -I docs/research/fish/challenge-297_calc.py`, which I wrote from the model's formula
and not by copying the author's script:

P = V³·M / (4·s·η_h·f_m·m), with V = √(2Mg / (ρ·S_lift·CL)) and M = m + σ·S_wing.

I fetched no new literature, so no new source read-levels apply. The author's read-levels are
discussed in §4.

## Verdict: WEAKENED

**The headline verdict holds:** the budget does not close at the stated inputs. **Two parts of the
claim are wrong as stated:**
1. **"CL is the only input whose factor-2 error flips S3-D" survives by 1.0 %** in the author's own
   revised model. Four other inputs come within 1 % of flipping it too.
2. **The "~1 mm hop" is about 75× too large.** It rests on an excess lift that the parity condition
   rules out.

## 1. Independent arithmetic (calculated)

| Quantity | Author | Mine |
|---|---|---|
| Baseline shortfall, CL 1.07, no body | 2.87× | 2.866× |
| CL needed, no body | 2.16 | 2.159 |
| CL needed, 240 mm² body | 1.76 | 1.764 |
| Shortfall, CL 1.10 + 240 mm² body | 2.03× | 2.030× |
| Lift margin | 1.6× | 1.764 / 1.10 = 1.60× |
| Speed at transient parity | 1.84 m/s | 1.839 m/s |
| 2 chords of travel | 26.8 mm, 14.5 ms | 26.8 mm, 14.54 ms |
| Steady stay-up speed | 2.47 m/s | 2.468 m/s |
| Lift after the transient decays | 0.56 of weight | 1.10 / 1.98 = 0.556 |

**All of these reproduce.** I found no arithmetic error in the numbers the claim carries.

## 2. The hidden assumption: a sensitivity table run on the wrong model

**What the author did.** The sensitivity table (S3-D-D §1) perturbs every input on S3-D's
**baseline**, where the body does not lift. Under that baseline, a factor-2 error in η_h, f_m,
run-up or muscle power leaves the margin at 1.24.

**Why that is the wrong model to test.** The claim's own improvement is to count body lift, which
lowers CL needed to 1.76. Its "only input" statement should therefore be tested in that revised
model.

**What happens when I re-run it there** (240 mm² body, CL_best 1.10, calculated):

| Input with a ×2 error | Margin (CL_needed / 1.10) | Verdict |
|---|---|---|
| η_h 0.37 → 0.74 | **1.010** | stands, by 1 % |
| f_m 0.6 → 1.2 | **1.010** | stands, by 1 % |
| Run-up 2 BL → 4 BL | **1.010** | stands, by 1 % |
| Muscle power 142.7 → 285.4 W kg⁻¹ | **1.010** | stands, by 1 % |
| σ × 0.5 | 1.259 | stands |
| m_body × 2 | 2.518 | stands |
| CL_best × 2 | 0.802 | falls |

**Why these four tie.** The shortfall scales as 1/(η_h · f_m · s · P), and it is 2.03 at the stated
inputs. So the budget closes if any one of the following happens:
- one of those four inputs is about **2.03× higher** than stated;
- two of them are each about **1.43× higher**;
- the run-up is **4.06 body lengths (16.2 cm)** instead of 2.

**What that means for the claim** (my inference, not the author's claim):
- "CL is the *only* input whose factor-2 error flips S3-D" is true by a 1.0 % margin, not by a
  comfortable one.
- In practice, all four power-side inputs share the deciding role with CL.
- These are inputs the author lists as weak (S3-D-D §6): η_h is taken from pike at abstract level,
  f_m is assumed, the 2 BL run-up is assumed, and muscle power is from *Scorpaena* at abstract level.
- A compound error of 1.43× in two of them is an easier route to closure than doubling CL, and
  nothing in the document rules it out.

**f_m = 1.2 is unphysical.** A muscle fraction cannot exceed 1, so that row is not a real route.
The other three rows are not bounded in the same way.

**A regime the author did not test** (my inference, not searched this session). Flying fishes
(Exocoetidae) do not launch from a 2 BL burst. They taxi: the body is already in the air while the
caudal fin keeps thrusting in the water. That stretches the thrust phase.
- The S3 model has neither a taxi phase nor any thrust after water exit, and the author states that
  as an assumption.
- A zebrafish-derived design does not have a flying fish's hypocaudal lobe. So I do not claim taxiing
  is available to it.
- The point is narrower: the "≥ 4 BL run-up" route to closure exists in the model and was not
  examined.
- Scope of this negative: I ran no literature search. I give no taxi distances or durations, because
  I did not retrieve any.

## 3. The hop is overstated by about 75× (calculated)

**The author's bound.** The author bounds the hop by assuming **1 g of excess lift** for the whole
transient window, which gives an apex of 1.04 mm (I reproduce 1.038 mm).

**Why that bound cannot hold.** The window is evaluated at the speed where transient plus body lift
**equals** weight. At that speed the excess lift is zero by definition.

**What the available power actually allows.** The shortfall at CL 1.98 with body lift is 0.841. The
fish can therefore reach V = 1.839 × (1/0.841)^(1/3) = **1.949 m/s**. At that speed:
- the excess lift is **0.123 of weight**;
- the window is 13.7 ms;
- the vertical speed gained is 16.5 mm s⁻¹;
- the **apex is about 0.014 mm**.

**What this changes.** It makes the author's conclusion ("a hop, not a launch") stronger. But the
specific figure in the claim, "~1 mm hop", is not the calculated value. It is a loose upper bound,
and the claim text presents it without saying so.

## 4. Proxy and evidence-level checks

**Proxy.**
- "Best steady CL = 1.0–1.1" is a whole flying-fish model in a wind tunnel at Re 1.9–2.2 × 10⁴. The
  design wing's Re is 2,473 (I calculate the same as the author).
- The author already flags the 8× Re gap and the normalisation issue.
- Applying a whole-planform CL to wing + body area is consistent only if the design's body:wing area
  ratio is close to the flying fish's. Park & Choi's A1/A2/A3 areas are `unknown` (Table 1, an image
  that was not read), so that ratio cannot be checked.
- The 240 mm² body area is the generous end of an **assumed** bracket. At 120 mm², CL needed is
  **1.94** (calculated), and the lift margin is 1.76×, not 1.6×.
- So the claim's "~1.6× in lift" belongs to the most generous assumption. That is defensible for a
  "does not close" verdict, but it depends on an area that has not been measured.

**Evidence level.** The claim records "derived", and that is honest.
- The document labels the 1.0–1.1 as **search-summary**.
- It labels the transient multiplier as **abstract** and as a scenario.
- It labels the body area as an assumption.
- I found no calculated value presented as observed.

**The "key number" text is the one weak spot.** It says "CL usable for a sustained launch = 1.0–1.1
(Park & Choi)". The tag "value search-summary" sits beside it. A reader of the key number alone could
take it as a measured value for this design. It is a search-engine quotation, from a different
animal, at a different Re.

## 5. What I could not break

- The arithmetic.
- The direction of the verdict at the stated inputs (2.03× power shortfall).
- The finding that transient lift lasts only ~2 chords (~14.5 ms) and cannot sustain flight in this
  model.

```swarm-challenge
{"claim_id": 297, "outcome": "weakened", "reason": "Arithmetic reproduces and the budget still fails at stated inputs (2.03x), but in the author's own body-lift model a factor-2 error in any of eta_h, muscle power or run-up leaves a margin of only 1.010 (so CL is not meaningfully the only deciding input), and the '~1 mm hop' assumes 1 g excess lift where parity allows only 0.12 g, giving ~0.014 mm (calculated).", "corrected_value": "margin 1.01 (not >=1.24) under x2 error in eta_h, f_m, run-up or muscle power once 240 mm^2 body lift is counted; closure at run-up 4.06 BL (16.2 cm); transient hop apex ~0.014 mm (calculated), not ~1 mm", "depends_on": ["S3-D-D model and inputs as stated in docs/research/fish/S3-D-deepen.md @ 2bc2392d", "S3 launch model P = V^3 M/(4 s eta_h f_m m), constant-acceleration run-up from rest, take-off at V = sqrt(2Mg/(rho S CL))", "assumption (author's): body planform 240 mm^2 lifts at same CL, no added mass", "S3 input: eta_h 0.37 (pike, abstract)", "S3 input: fast-muscle power 142.7 W/kg (Wakeling & Johnston 1998, abstract)", "S3 input: f_m 0.6 (assumption)", "S3 input: run-up 2 BL of 4 cm (assumption)", "S3 input: sigma 0.138 kg/m^2; m_body 0.40 g; S10 wing 1070 mm^2, span 80 mm", "Park & Choi 2007 CL 1.0-1.1 (search-summary, via author)", "assumption (author's): transient CL 1.98 = 1.8 x 1.10 for 2 chords (Dickinson & Goetz 1993, abstract)", "rho 1.225 kg/m^3, g 9.81 m/s^2"]}
```
