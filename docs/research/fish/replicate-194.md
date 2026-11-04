# Replicate 194: independent re-derivation of the S28 "deliverable phenotype" number

**Status:** calculation on stated inputs. **Nothing here is a measurement.** Script:
`docs/research/fish/replicate-194-scripts/r194.py`.

## What I was asked, and what I read before deriving

The question was given to me only as "THE DELIVERABLE", with `S28-organism.md` named as the place the
inputs live. That file exists only on branch `claude/s28-organism-design-5z0vjz`. To learn which
quantity claim 194 is, I read:

- S28 §1, the inputs table, in full.
- The first sentence of the "deliverable phenotype" paragraph.
- §3.6–§4 **with every digit masked** (`sed 's/[0-9]/#/g'`).
- The commit subject of `challenge-194-…`: "S28 ascent-deceleration claim weakened (lift ratio used as proxy)".
  I did **not** read that file.

From the masked text, claim 194 is this: *if the existing Daane double heterozygote spreads its
pectorals during a leap, the effective downward acceleration during the ascent is reduced by about
#–## % (lift ## % at exit, # % at apex).* I saw no S28 result digits until the comparison section
below. The commit subject did tell me a challenger had raised a proxy concern. My vertical-component
analysis below may have been primed by that, and I disclose it here.

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| ρ_air, g | 1.225 kg m⁻³, 9.81 m s⁻² | standard constants | — |
| Exit speed V₀ | 0.45 and 1.38 m/s | S28 §1 attributes these to "Miln et al. 2021, n = 50". **I could not locate that paper.** One standard web search for Miln 2021 zebrafish burst speed returned nothing matching. This is therefore a project input I have not verified. It is also *swimming burst*, not water-exit speed. | listing (project table); primary could-not-access |
| Body mass m | 0.25 g (also 0.40 g) | S28 marks it as assumed and back-solved. Singleman & Holtzman 2014 (*Zebrafish*, PMC4108942) gives the adult SL threshold (≥ 18 mm) but **no mass**. I found no length–mass regression in the searches I ran (one web search, one PMC fetch). | full-text (Singleman, no mass found); mass itself: assumed |
| CL | 1.07 (also 0.8) | project-derived CL_max, used unchanged. I did not re-derive it. | listing (project) |
| Total spread-fin area S | 40, 80, 196 mm² | **unknown from primary sources.** Daane et al. 2021 (*Curr Biol* 31:5052, PMC9172250) give pectoral length/SL only as plots (Fig. 4B), with no numbers in the text. Fin **area** was never measured. The ZFIN figure page returned 503, and a mirror was blocked by network policy. 40–80 mm² is **my own unsourced guess** for a 3 cm fish with elongated fins. 196 mm² is the area at which the project's V_to = 4.37 m/s is self-consistent (S28 §1 inputs table). | full-text (Daane text; figure values could-not-access) |
| Launch angle | 45° | assumption (range-optimal for a ballistic point mass) | — |
| Wing drag | CD0 0.08 + CL²/(π·0.8·AR), AR 5; body CD 0.3 on 24 mm² | generic choices, used only for the net-vertical check | assumption |

## Arithmetic

The lift-to-weight ratio is L/W = ½ ρ V² S CL / (m g).

At V₀ = 1.38 m/s: q = ½·1.225·1.38² = 1.1665 Pa, so q·CL = 1.248 Pa. W = 0.25e-3·9.81 = 2.4525e-3 N.

| S | L at exit | L/W at exit | L/W at apex of 45° leap (× cos²45 = 0.5) |
|---|---|---|---|
| 196 mm² | 2.446e-4 N | **10.0 %** | **5.0 %** |
| 80 mm² | 9.98e-5 N | 4.1 % | 2.0 % |
| 40 mm² | 4.99e-5 N | 2.0 % | 1.0 % |

With m = 0.40 g, every value is ×0.625 (so 196 mm² gives 6.2 % → 3.1 %). At V₀ = 0.45 m/s, every value is ×(0.45/1.38)² = 0.106 (so 196 mm² gives 1.1 %).

**L/W is not the reduction in downward acceleration.** Lift acts normal to the path. On a climbing path at
angle γ, its vertical part is L cos γ. Wing drag adds −D sin γ, which increases the downward deceleration
while climbing. For S = 196 mm², 0.25 g, 1.38 m/s at 45° (script output):

- **Exit (γ = 45°).** Vertical lift is 10.0 % × 0.707 = 7.1 % W. Wing drag: CD_w = 0.08 + 1.07²/(π·0.8·5) = 0.171, so D_w/W = 10.0 % × 0.171/1.07 = 1.6 %. Its vertical part is −1.6 % × 0.707 = −1.1 %. The fin-attributable net reduction is **≈ 5.9 % W**. Including body drag, which wild-type fish also have, it is 5.7 %.
- **Apex (γ = 0, V = 0.976 m/s).** The net reduction is **5.0 % W**, all of it lift.
- **Vertical leap.** Lift has no vertical component, so the reduction is ≈ 0. For comparison, the time-mean of L/W over a vertical deceleration is (L/W)_exit/3 = 3.3 %, and its vertical part is still 0.

## My value

**Fin-attributable reduction in effective downward acceleration during the ascent of a 45° leap:**

- **≈ 5–6 % of g**, but only if S ≈ 196 mm², m = 0.25 g and V₀ = 1.38 m/s (top of the unverified burst range).
- About 1–3 % for the 40–80 mm² areas I consider more plausible for the Daane fish (unsourced guess).
- About 0.1–0.6 % at V₀ = 0.45 m/s.

The raw lift ratios are **10 % W at exit and 5 % W at apex** for the 196 mm² case.

The uncertainty is dominated by S, which is unknown and scales the result linearly, then by V₀ (squared, and unverified as an exit speed), then by m. A 1.6× range in m gives a 1.6× range in the result.

## Comparison with the recorded value (read only after the derivation above)

Recorded (S28 line 133): "reduced by about **5–10 %** (lift 10 % at exit, 5 % at apex)".

- **The lift ratios: AGREE.** S28 gets 10 % and 5 % from (1.38/4.37)² and (0.98/4.37)². That is the same algebra as mine at S ≈ 192–196 mm², 0.25 g, CL 1.07.
- **The claimed reduction in downward acceleration: DISAGREE on the upper end.**
  - The 10 % figure is the full lift at exit. At exit, lift points 45° off vertical, and wing drag works against the climb. The vertical net is ≈ 6 %, not 10 %, so the defensible range is ≈ 5–6 %.
  - S28's own §3.2 integration says the apex is "unchanged or lower" with the wing. That is consistent with drag eating the small lift, and not consistent with a 10 % reduction.
- **Attribution: DISAGREE.** The sentence applies the number to the *existing* Daane double het. 196 mm² is the project's designed AR-5 wing (case C), not a measured Daane fin. S28 itself says ≤ 3 % W at exit for S ≤ 60 mm². That is my inference from S28 §4, which I read after deriving.

Verdict: **DISAGREE**. The lift arithmetic replicates. The stated "5–10 %" reduction does not: the upper bound
is a lift-to-weight proxy rather than a vertical net force, and it is conditional on an unmeasured fin area.

Sources: [Daane et al. 2021, PMC9172250](https://pmc.ncbi.nlm.nih.gov/articles/PMC9172250/) (full-text; figure
values not available as text); [ZFIN fig. ZDB-FIG-221222-35](https://zfin.org/ZDB-FIG-221222-35) (could-not-access, HTTP 503);
[Singleman & Holtzman 2014, PMC4108942](https://pmc.ncbi.nlm.nih.gov/articles/PMC4108942) (full-text, no mass data);
Miln et al. 2021 (could-not-access; not found in one web search).

```swarm-replication
{"claim_id": 194, "my_value": "~5-6 % of g net vertical reduction during ascent of a 45-degree leap (lift/W 10 % at exit, 5 % at apex) only for S~196 mm2, 0.25 g, 1.38 m/s; ~1-3 % for 40-80 mm2 fins; ~0 for a vertical leap", "agrees": false,
  "note": "Lift ratios 10 %/5 % replicate exactly, but the 10 % upper end of '5-10 % reduction' treats full lift at a 45-degree climb as vertical and ignores wing drag (net ~6 %), and it is conditional on the designed 196 mm2 wing rather than any measured Daane fin."}
```
