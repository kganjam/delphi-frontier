# Challenge 180: adversarial review of S7-D (pectoral girdle, bone yield)

Claim under review (by another author; source `harvest:deepen-s7-pectoral-girdle-b6j2hx`, file `docs/research/fish/S7-deepen.md` on branch `claude/deepen-s7-pectoral-girdle-b6j2hx`):

> The conclusion is insensitive (≤27%) to factor-2 errors in every modelled input, but it flips with a factor-2 error in the unmeasured actual girdle section. Replacing the assumed 25–114 MPa yield with measured herring yield (62.6–66.8 MPa) narrows the worst-case required solid-equivalent section to about 0.26 mm. "Bone probably not limiting" stands, but stays open. Recorded evidence level: derived.

My script is `docs/research/fish/challenge-180.py`. **Every number from it is a calculation, not an observation.**

**Outcome: WEAKENED.** The headline survives: bone is probably not the limit, and the question is still open. The arithmetic is right. Two parts of the supporting statement fail:

- the "≤27% for every modelled input" bound;
- the "narrows to ~0.26 mm" figure.

## 1. Independent arithmetic

I wrote my own code from the stated inputs: m = 0.4 g, V = 3 m/s, n = 3, C_L = 0.78, AR = 9, body half-width 2.5 mm, elliptic lift centroid at 4s/3π, and a solid circular section with d = (32M/πσ)^⅓.

| Quantity | Claim | My recomputation (calculated) |
|---|---|---|
| Root moment per fin, worst case | 1.1×10⁻⁴ N·m | 1.081×10⁻⁴ N·m |
| d at σ = 62.6 MPa | 0.26 mm | 0.260 mm |
| d at σ = 66.8 MPa | 0.255 mm | 0.255 mm |
| d at σ = 25 MPa (S7 worst) | 0.353 mm | 0.353 mm |
| Halving a linear section dimension | stress ×8 | ×8 (Z ∝ size³) |

**The arithmetic reproduces.** No fault was found here.

## 2. Faults found

### 2a. "≤27% for every modelled input" is false: body mass was never swept

The author's sweep function `run()` takes the mass `m` as an argument. But the sweep dictionary leaves `m` out; it varies only V, C_L, AR, n, σ, r, muscle stress and half-width.

Mass enters the moment roughly as W^1.5, because a heavier fish needs a larger fin and so a longer moment arm. My calculated results:

- **m ×2:** M ×2.88, so d ×1.42 (+42%).
- **m ×0.5:** d ×0.70.

So one modelled input moves the required section by 42%, not by 27% or less.

This does not flip the conclusion on its own. Two caveats apply, both my inference:

1. Mass is a design choice. It is not a measured quantity.
2. If the fish is simply scaled up, the girdle grows with it. Under isometry the bone stress rises only ×1.42 (calculated: M ×2.85, Z ×2).

But the stated bound, as written, is wrong.

### 2b. "Narrows to ~0.26 mm" depends on using the *mean* yield stress with no safety factor

The 0.26 mm figure uses the **mean** measured yield. A section sized to the mean strength yields in roughly half of specimens. The author's own threshold table (§3a of S7-D) applies a safety factor of 1.5, while §4 and the headline do not. The two sections are inconsistent with each other.

Required d at the worst case (calculated). The design yield values are derived from Fiedler 2019's means ± SD:

| Yield basis | σ (MPa) | d, no safety factor | d, safety factor 1.5 |
|---|---|---|---|
| Mean, large fish | 62.6 | 0.260 mm | 0.298 mm |
| Mean, small fish | 66.8 | 0.255 mm | 0.291 mm |
| Mean − 1 SD, small fish | 43.4 | 0.294 mm | 0.336 mm |
| Mean − 2 SD, large fish | 36.2 | 0.312 mm | 0.357 mm |
| Mean − 2 SD, small fish | 20.0 | 0.380 mm | 0.436 mm |
| S7 original worst | 25 | 0.353 mm | 0.404 mm |

Small fish have SD 23.4 MPa on a mean of 66.8, a coefficient of variation of 35%. On a lower-tail design basis, the required section is **0.29–0.38 mm**. That is the same band as S7's original 0.21–0.35 mm, and it can sit above it.

The measured data **anchor** the strength value. They do not **narrow** the requirement. The "26% smaller in the worst case" improvement is an artefact of comparing a mean against S7's lower bound.

### 2c. Proxy check: right quantity, wrong tissue (the author already says so)

Yield stress is the right quantity for this check. The proxy problem is in the tissue: herring intermuscular bone is tensile tendon ossification, whereas the girdle is dermal and endochondral bone loaded in bending. The author states this caveat (§3b, §5), so it is not a hidden defect.

I re-read Fiedler 2019 (read-level: full-text, through a summarising fetch). Three further points:

- **Yield is not defined.** The paper gives no yield criterion. It does not mention a 0.2% offset; it says only that the bones show "a distinct yield point". Its Table 1 is internally odd:
  - E × yield strain gives 94–105 MPa (calculated: 3.5 GPa × 0.030; 2.6 GPa × 0.036).
  - The reported yield stress is 62.6–66.8 MPa.
  - A separate "transition strain" of about 0.015 is listed, twice, with slightly different values.

  So the author's inference that fish bone yields at "~3%, not 0.5%" rests on an undefined yield criterion. Using the transition strain instead, about 1.5% is still above 0.5%. The qualitative point survives, but the exact figure does not.
- **Loading rate.** The test speed was 10 mm/s over a 3 mm gauge length, a strain rate of about 3 s⁻¹. The paper calls this "quasi-static" (calculated rate; the label is the authors'). Bone yield stress generally rises with strain rate. For a sustained gliding load, these values may therefore be slightly high. I did not quantify this.
- **Specimen size.** The specimens are 0.04–0.09 mm² in area, about 0.23–0.34 mm across (calculated from the area). That matches the required section's scale, so a size-effect objection does not apply.

### 2d. The hidden assumption that carries the result: the share of the root moment the receiving element carries

The whole "bone OK vs not" comparison assumes one solid section carries the full root moment. The author already flags that the moment path runs through four proximal radials and the scapula, and that the moment share was not computed. I could not improve on this. Relaxing the assumption cuts both ways:

- Four radials sharing the load would lower the stress in each one.
- A stress concentration at the articular facets would raise it.

This is still the dominant open input, as the claim says.

## 3. Evidence level

"Derived" is honest. The claim labels 62.6–66.8 MPa as measured (it is, in herring) and the 0.26 mm as calculated. It also gives the actual section as `unknown`. No calculated value is presented as an observation.

## 4. Counter-examples and regimes

This is my inference, from general knowledge; I ran no literature search for this section, so its scope is nil.

- **Freshwater hatchetfishes** (Gasteropelecidae) are small teleosts known for aerial pectoral-fin locomotion, and they have a greatly enlarged pectoral girdle. That enlargement is usually tied to muscle attachment, not bone strength. So it points at the joint and muscle constraint S7 already named binding. It is not evidence that the bone is limiting. I did not retrieve a measurement.
- **Repeated or gust loading** is a regime the yield-only check does not cover. Fatigue strength under repeated loading is below monotonic yield. I could not retrieve fish-bone fatigue data and did not search for it.

## 5. Verdict

**WEAKENED.**

- "Bone probably not limiting, still open until the radial/scapula section is measured" **stands**.
- "≤27% for every modelled input" is **false**: mass ×2 gives +42% (calculated).
- "Narrows to ~0.26 mm" is **not robust**. It holds only at mean yield with no safety factor. On the author's own safety factor of 1.5, or a lower-tail yield, the requirement is 0.29–0.38 mm, about the same as S7's original band. The measured yield anchors the strength value but does not narrow the requirement.

## Sources

- Fiedler I.A.K. et al. (2019). *J. Biomech.* 94:59–66. [PMC6995032](https://pmc.ncbi.nlm.nih.gov/articles/PMC6995032/). Read-level: full-text, through a summarising fetch. Read for Table 1, method, yield definition and specimen area.
- S7-D, `docs/research/fish/S7-deepen.md` and `.py` (branch `claude/deepen-s7-pectoral-girdle-b6j2hx`). Read-level: full-text.
- MorphoSource 000415918: not attempted; the claim's author reports could-not-access.

```swarm-challenge
{"claim_id": 180, "outcome": "weakened", "reason": "Arithmetic reproduces and 'bone probably not limiting, still open' stands, but the '≤27% for every input' bound omits body mass (×2 mass → +42% in required section, calculated) and the 'narrows to 0.26 mm' figure holds only at mean yield with no safety factor—on the author's own SF 1.5 or a mean−1/2 SD yield the requirement is 0.29–0.38 mm, i.e. not narrowed relative to S7's 0.21–0.35 mm.", "corrected_value": "required solid-equivalent section 0.29–0.38 mm worst case (0.30 mm at mean 62.6 MPa with SF 1.5; 0.38 mm at mean−2SD 20 MPa, no SF); mass ×2 sensitivity +42%", "depends_on": ["root moment 1.08e-4 N·m per fin from S7 worst-case inputs (m=0.4 g, V=3 m/s, n=3, C_L=0.78, AR=9)", "Fiedler 2019 herring IB yield stress 62.6±13.2 / 66.8±23.4 MPa (tensile, yield criterion undefined)", "solid circular section model d=(32M/πσ)^(1/3)", "safety factor 1.5 as used in S7-D §3a", "actual girdle section: unknown"]}
```
