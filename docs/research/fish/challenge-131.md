# Challenge 131: adversarial review of claim [S2-D-D] (wing aspect ratio)

**Claim under review (another author's):** measured teleost pectoral planforms give a wing AR of 1.8-4.2
(labrids; AR_wing = 2 x L^2/A per fin = 1.82-4.16). With S2-D's Re-matched model that gives a
computed whole-animal L/D of 3.2-4.9, which puts S2's assumed AR 4 at the top of the measured
range. Flying fish reach AR 9.0-10.7. On a 3.2 cm fish, L/D saturates near 4.8 at any AR, so the
binding input is span per side relative to SL, not AR. e*AR = 1.3-2.9 at an assumed e = 0.7.
Recorded evidence level: *measured*. Source: `harvest:s2-d-sensitive-input-rasran`.

**Verdict: WEAKENED.** The arithmetic holds and the span-not-AR conclusion holds. The evidence
level is wrong, and the "measured range" that places AR 4 at its top does not match the
two sources I could reach.

## Sources and read-levels

| Source | Read-level | Used for |
| --- | --- | --- |
| The claim's S2-D model and the harvest note `s2-d-sensitive-input-rasran` | **could-not-access**. Not found on `origin/main`, `work/frontier-foundation` or this branch. GitHub code search in `kganjam/delphi-frontier` for `rasran`, `"S2-D"` and `labrid` returned 0 hits | none (model reconstructed below) |
| Fish FE (1990) J Zool 221:391-403, Table III, as transcribed in this repo (`origin/main:data/fish-controls/fish1990_tables.json`, read by an earlier worker from page images of the scanned PDF) | **full-text, second-hand.** I read the repo transcription, not the PDF | flying-fish pectoral AR |
| Wainwright, Bellwood & Westneat (2002) Env Biol Fish 65:47-62, doi:10.1023/A:1019671131001 | **search-summary.** The fishlab.ucdavis.edu and link.springer.com fetches failed (hosts not allowed in this session) | labrid pectoral AR range |
| Walker & Westneat (2002) J Exp Biol 205:177 | **could-not-access** (cob.silverchair.com not allowed) | none |

## 1. Independent arithmetic

- e*AR at e = 0.7: 0.7 x 1.82 = 1.27 and 0.7 x 4.16 = 2.91. **Reproduced.**
- The S2-D model itself was not available. I assumed a parabolic polar,
  (L/D)max = 0.5*sqrt(pi*e*AR/CD0), and solved it backwards from the claim's endpoints. That gives
  CD0 = 0.098 (AR 1.82, L/D 3.2) and 0.095 (AR 4.16, L/D 4.9). Both ends need almost the same
  CD0, about 0.096. So the claim's L/D range is consistent with a fixed whole-animal CD0 of
  about 0.096, referenced to wing area. *(This is my inference. The author did not state it.)*
- With that reconstructed polar (computed, not observed), AR 4 gives L/D = 4.79. That matches the
  claim's "about 4.8".
- **Span, not AR, binds.** At fixed span b, induced drag L^2/(q*pi*e*b^2) does not depend on area,
  so (L/D)max = 0.5*b*sqrt(pi*e/f), where f is the total parasite drag area. Raising AR at fixed
  span only shrinks area, so L/D levels off once body drag dominates f. This is standard
  lifting-line reasoning, and the claim's saturation statement is consistent with it. I could
  not reproduce the 4.8 saturation number itself, because it needs S2-D's body-drag term.
  **Structurally survived. Numerically unverified.**

## 2. Proxy check

- **Labrid fin AR is a stand-in for gliding-wing AR.** Labrid L^2/A is a fin-shape index for
  rowing and flapping propulsion (leading-edge length squared over fin area). It is not the
  aerodynamic span^2/S of two fins held out laterally across a body.
  - The quantity that matters is (2L + w_body)^2 / (2A + w_body*c_root).
  - Doubling L^2/A drops the body-width terms. That is acceptable only if body width is small
    next to 2L.
- **e = 0.7 lifting line is applied to AR below 3.** At e*AR of 1.3-2.9, lifting-line theory is
  outside its domain. Low-AR wings carry nonlinear, vortex-induced lift, and e is poorly defined
  at Re around 10^4.
  - The L/D numbers are therefore *computed under an assumption that is weakest exactly at the
    low end of the range* (the low-AR end).

## 3. The hidden assumption, relaxed: which AR convention and which dataset

The result depends on two things:
- that 1.82-4.16 is the whole measured labrid range;
- that it is per-fin L^2/A doubled.

**Wainwright et al. 2002** (search-summary) reports pectoral-fin AR of **1.12-4.48 across 143
labrid species**, with peaks near 2.0 and 3.0. This disagrees with the claim's range. I keep both
values and do not average them:

| Convention for the 1.12-4.48 | Whole-wing AR | Computed L/D (my reconstructed polar, CD0 ≈ 0.096, e = 0.7) | Where AR 4 sits |
| --- | --- | --- | --- |
| Already a whole-wing value | 1.12-4.48 | 2.5-5.1 | near the top, but not the top |
| Per-fin L^2/A, doubled as the claim does | 2.24-8.96 | 3.6-7.2 | mid-range |

I believe Wainwright 2002 defines AR as leading-edge length squared over the area of one fin.
That belief comes from my memory, not from reading the paper, so it is **unverified**.

Under either reading, "AR 4 at the top of the measured range" does not hold against the
143-species range. The claim's 1.82-4.16 may come from a smaller labrid subset (the source is
unknown; see read-levels). It should not be presented as *the* measured teleost range.

## 4. Is the evidence level honest?

**No.**
- The headline outputs are a **computed** L/D and a **computed** e*AR (from an assumed e).
- AR_wing = 2 x L^2/A is a **derived** conversion of a measured quantity.
- The flying-fish value is flagged by the author's own text as "convention unconfirmed".

Recording the claim as *measured* presents a derived and simulated result as an observation.
That is a defect even where the numbers are right. The correct level is "derived from measured
fin planforms, plus a computed L/D under an assumed e and an assumed polar".

## 5. Counter-examples the author missed

- **Flying fish: the range is wider than stated.** Fish 1990 Table III (repo transcription) gives
  individual pectoral-fin AR ranges by genus:

  | Genus | Pectoral-fin AR range |
  | --- | --- |
  | Cypselurus | 3.0-12.2 |
  | Danichthys | 4.6-11.7 |
  | Exocoetus | 8.9-19.9 |
  | Fodiator | 6.1-8.9 |
  | Hirundichthys | 5.1-10.7 |
  | Parexocoetus | 7.1-12.9 |

  - The paper's text says 3.0-16.9.
  - The claim's 9.0-10.7 lies inside these ranges and coincides with the Exocoetus minimum (8.9)
    and the Hirundichthys maximum (10.7). I cannot tell whether the author's source is a
    different paper. I record this as a disagreement, not as an error.
  - "Anatomically possible" is understated: per-fin AR up to 16.9-19.9 is reported.
- **Small fish have lower AR.** Fish 1990 fits AR = a*M^b with b of +0.14 to +0.20 in the genera
  where the fit is significant, so AR rises with body mass. I extrapolated the Table I length
  fits and the Table III AR fits to a 3.2 cm SL fish (about 0.26-0.55 g). That is **below the
  0.003 kg specimen floor, so it is an extrapolation and a computation, not an observation**:

  | Genus | Predicted pectoral AR at 3.2 cm SL |
  | --- | --- |
  | Cypselurus | 3.7 |
  | Hirundichthys | 4.1 |
  | Exocoetus | 5.2 |

  - These values support the author's point that a 3.2 cm fish should not be modelled at AR 9-10.
  - They also suggest that AR around 4 (per-fin convention) is typical, not extreme, for small
    flying fish.
  - This undercuts "top of the range" from a second direction.

## What survives

- The e*AR arithmetic.
- The internal consistency of the L/D endpoints (a single CD0 of about 0.096 reproduces both).
- The physical argument that span per side, not AR, is the binding input at fixed span.

## What fails

- The *measured* evidence label.
- "AR 4 at the top of the measured range". The 143-species labrid range (1.12-4.48, a
  search-summary read) and the factor-of-2 convention ambiguity both move AR 4 toward
  mid-range.

```swarm-challenge
{"claim_id": 131, "outcome": "weakened", "reason": "The arithmetic and the span-not-AR argument reproduce, but the headline L/D and e*AR are computed (not measured), and the 143-species labrid range of 1.12-4.48 (Wainwright 2002, search-summary), together with an unresolved factor-of-2 per-fin/whole-wing convention, moves S2's AR 4 from the top of the range to near-top or mid-range.", "corrected_value": "labrid pectoral AR 1.12-4.48 (search-summary; convention unverified), or whole-wing AR 2.24-8.96 if per-fin and doubled; computed L/D 2.5-5.1 or 3.6-7.2 respectively (reconstructed polar, CD0 ~0.096, e=0.7 assumed); evidence level: derived+computed, not measured", "depends_on": ["Wainwright, Bellwood & Westneat 2002 Env Biol Fish 65:47-62 labrid AR range 1.12-4.48 (search-summary read)", "Wainwright 2002 AR definition = per-fin leading-edge L^2/A (unverified recollection)", "Fish 1990 J Zool 221:391-403 Table III pectoral AR ranges and allometric fits, as transcribed in data/fish-controls/fish1990_tables.json", "Fish 1990 Table I length-mass fits (for 3.2 cm SL mass extrapolation)", "reconstructed parabolic polar with CD0 ~0.096 back-solved from the claim's own L/D endpoints", "assumed span efficiency e = 0.7 (the claim's)"]}
```
