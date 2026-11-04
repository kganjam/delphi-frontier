# Challenge 131: adversarial review of S2-D-D (fin-wing aspect ratio)

**Claim under review** (harvest `s2-d-sensitive-input-rasran`; source file
`docs/research/fish/S2-D-deepen.md` on branch `claude/s2-d-sensitive-input-rasran`, read in full):

> Measured teleost pectoral planforms give a wing aspect ratio of 1.8–4.2, so with S2-D's own
> Re-matched model the computed whole-animal L/D is 3.2–4.9, which places S2's assumed AR 4 at the top
> of the measured range. Flying-fish fins show AR 9–10.7 is anatomically possible, but on a 3.2 cm fish
> at flying-fish fin proportions the computed L/D saturates near 4.8 for any AR, so span per side
> relative to SL, not AR, is the binding input.
> Recorded evidence level: **measured**.

**Verdict: WEAKENED.** The arithmetic, the physics and the direction of the conclusion all
**survive**. The weakening is about how the evidence is labelled and how far the scope reaches,
not about the numbers:
- the headline output (L/D) is computed;
- the "measured" AR is a derived ×2 conversion of one labrid sample, which is skewed towards high AR;
- the claim generalises that sample to "teleost".

**Kinds of number.** I ran no experiment. Every number below is one of three kinds, and the sentence
says which:
- **computed** by my own script, `challenge-131_check.py` in this directory
  (`python3 -I docs/research/fish/challenge-131_check.py`);
- quoted from a source, with its read-level;
- my **inference**, labelled as such.

---

## 1. Independent arithmetic

I did not reuse the author's solver. The author solves a fixed point,
CL = min(√(CD0/k), cap), with a V-dependent CD0. My script instead does a brute-force minimisation
of total drag over airspeed: V is stepped from 0.5 m/s with CL ≤ cap enforced. The inputs are the
stated ones:
- ρ = 1.2, ν = 1.5×10⁻⁵, m = 0.4 g, S = 9 cm², e = 0.7;
- CD0_wing = λ·2.656/√Re_c with chord c = S/b;
- body: a 32×7×4 mm ellipsoid with form factor 1.5, plus 2 cm² of median fins;
- CL cap 0.9.

| AR_wing | author whole L/D, λ 1.4 | **mine** (computed), λ 1.4 | author, λ 2.0 | **mine**, λ 2.0 |
|---|---|---|---|---|
| 1.82 | 3.70 | **3.74** | 3.19 | **3.23** |
| 2.76 | 4.25 | 4.29 | 3.65 | 3.68 |
| 4.00 | 4.80 | 4.84 | 4.14 | 4.14 |
| 4.16 | 4.88 | **4.90** | 4.19 | 4.19 |
| 9.0 / 10.7 | 5.92 / 6.03 | 5.92 / 6.03 | 4.77 / 4.80 | 4.77 / 4.80 |

- The two solvers agree to within 0.04. A true drag minimum is slightly better than the fixed point,
  which is the expected direction.
- The "3.2–4.9" range reproduces. It spans λ 1.4–2.0 at e = 0.7.
- Other checks I recomputed (computed):
  - e·AR = 0.7 × 1.82 to 0.7 × 4.16 = **1.27–2.91** ✓;
  - span per fin at S = 9 cm², (b − 4 mm)/2/SL, = **0.57 / 0.87 / 1.34 / 1.47 SL** at AR
    1.82 / 4 / 9 / 10.7 ✓.
- Span-fixed sweep (0.70 SL per fin, λ 1.4, computed):

  | AR | 2 | 4 | 6 | 7 | 9 | 12 |
  |---|---|---|---|---|---|---|
  | L/D | 3.99 | 4.59 | **4.84** | **4.84** | 4.73 | 4.46 |

  The peak is **4.85 at AR ≈ 6.5**. "Saturates near 4.8" reproduces.
- One thing the headline drops (computed): the author's own two brackets, λ 1.4–2.0 and e 0.5–0.9,
  taken together give corners of **2.79** (AR 1.82, λ 2.0, e 0.5) and **5.46** (AR 4.16, λ 1.4,
  e 0.9).
  - The headline "3.2–4.9" applies the λ bracket but not the e bracket.
  - The body of the source text reports 3.2–5.5, which also omits the 2.8 corner.
  - This is a presentation gap, not an error. The claim's key line does state e = 0.7 as assumed.

## 2. Is the source data what the claim says? (re-read)

**Fulton, Wainwright, Hoey & Bellwood 2016**, *Ecol Evol* 7, PMC5214093
- Read-level: **full-text**. I fetched the Europe PMC XML myself: sha256 `45321787 4266ea9c…`,
  the same file the author used.
- Table 1 is confirmed verbatim:
  - minimum *Pseudocheilinus hexataenia* **0.91**;
  - maximum *Stethojulis bandanensis* **2.08**;
  - *Thalassoma* 1.81–1.97; *Halichoeres* 1.29–1.54.
- The text also says 2.08 is "the upper extreme … for this family".
- **Scope problem the author did not flag.** Per its caption, Table 1 lists only "the top three
  species per location" on *wave-swept reef crests*. The paper's thesis is that high-AR *Thalassoma*
  dominate those habitats. So this is a sample deliberately skewed towards high-AR species, not the
  labrid range, and still less a teleost range.
  - The family's true minimum is `unknown` from what I read. Fulton et al. 2005 and Wainwright et
    al. 2002 hold the full family data, and I did not reach either.
  - **My inference:** a less skewed sample would move the lower end down, not up. That moves AR 4
    further towards the top, so it reinforces the claim's "top of the range" point rather than
    breaking it.

**Walker, Alfaro, Noble & Fulton 2013**, *PLoS ONE* 8:e75422, PMC3799785
- Read-level: **full-text**. I fetched it myself: sha256 `83ab57b3…`.
- Verbatim: AR was "calculated from digitized images of amputated fins as 2\*length²/area for
  pectoral fins … where length … [was] the leading edge length of a single pectoral fin … (the
  pectoral fin AR is doubled to conform to the definition of AR for wings in the aerodynamics
  literature)".
- This confirms the ×2 relation for *Walker's* values.
- Whether Fulton 2016's Table 1 values are the undoubled form is still an **inference**:
  - Fulton 2016 says it used "the exact method of Fulton et al. (2005)", and I could not read the
    2005 methods;
  - "doubled to conform" implies the earlier convention was undoubled. That is suggestive, not proof.

**Park & Choi 2010**, *J Exp Biol* 213:3269 (flying-fish AR 9.0–10.7)
- Not re-read: **could-not-access** in this review. I made no attempt beyond relying on the author's
  quoted text.
- **My inference (dimensional sanity check, not a measurement):** on the per-fin convention, AR 9.5
  would mean a fin whose leading edge is about 9.5 mean chords long. That is much more slender than
  the broad flying-fish pectoral. The author's reading of it as a tip-to-tip wing AR is therefore the
  more plausible one, and its being unconfirmed is correctly flagged.

## 3. Proxy check

The quantity that matters is the zebrafish (or engineered-zebrafish) pectoral wing AR and span. The
claim uses two proxies:
- AR from labrids, which are high-AR, lift-based labriform swimmers;
- AR from exocoetids.

The author states that the zebrafish value is `unknown`, which is honest. The proxy is not hidden. It
is **mislabelled in the headline as "measured teleost"**:
- the claim's own flying-fish entry is also a measured teleost, at 9–10.7;
- so "measured teleost planforms give 1.8–4.2" is internally inconsistent. The defensible wording is
  "a high-AR-biased labrid sample gives 1.8–4.2".

## 4. Hidden assumptions, relaxed (computed)

The "span, not AR, binds" conclusion rests on the span-fixed sweep. I relaxed each input to it and
recorded the peak whole-animal L/D over AR 1.5–15, with span fixed:

| relaxation | peak L/D | at AR |
|---|---|---|
| baseline (0.70 SL per fin, cap 0.9, e 0.7, λ 1.4) | 4.85 | 6.5 |
| span 0.65 / 0.77 SL | 4.72 / 5.02 | 6.25 / 6.75 |
| CL cap 1.07 (W&E steady CLmax, no margin) | 5.03 | 7.75 |
| CL cap 1.5 | 5.36 | 11.25 |
| **no CL cap** | **5.72** | **14.75 (still rising)** |
| e 0.5 / 0.9 | 4.37 / 5.24 | 8.0 / 5.5 |
| λ 2.0 | 4.11 | 6.0 |
| **body drag ×0.5 / ×2** | **5.69 / 3.92** | 8.25 / 4.75 |
| mass 0.25 / 0.55 g | 4.47 / 5.12 | 6.0 / 6.75 |

**Finding (computed, with my inference on the mechanism).** At fixed span, induced drag does not
depend on S. The saturation therefore comes from two things together:
- the **CL cap**, which forces the flight speed above the optimum once S is small;
- **body parasite drag**, which grows with q.

With the cap removed, L/D keeps climbing with AR (5.72 at AR 14.75). So "for any AR" holds only
under the cap. Under any physically sane cap (0.9–1.07), the peak stays at 4.85–5.03, so the claim
holds where it is meant to.

**The claim is incomplete on one point.** Span is a binding input, but body-drag area moves the
saturated value about as much as the flying-fish span range does:
- body drag ×0.5 to ×2 gives 3.9 to 5.7;
- span 0.65–0.77 SL gives 4.7 to 5.0.

The claim's "span not AR" contrast is correct. Promoting span to *the* next most sensitive input,
which the source file does in its last section, is not established by the claim's own model. Body
drag area, also an assumption, is at least as sensitive. (This is a computed sensitivity, not a
claim that body drag is measured.)

**A regime the author mentioned but did not run (computed).** At the zebrafish-reachable span the
source itself infers, 0.36–0.43 SL per fin, the peak L/D over AR is:
- **3.3–4.0** (λ 2.0–1.4), at AR ≈ 4–5, S ≈ 1.7–2.2 cm² and V ≈ 5.7–6.5 m/s;
- 2.6–2.8 at the wild-type 0.21 SL.

The 3.3–4.0 still sits inside S2-D's 3–5 band, so "strengthens" survives. It sits in the lower half,
and at those speeds the chord Re is above the Wakeling & Ellington 0.7–2.4×10³ calibration range of
λ. That regime is an extrapolation.

## 5. Evidence level

- The recorded level "**measured**" overstates the claim:
  - (a) the deliverable quantity, whole-animal L/D 3.2–4.9 and saturation ≈ 4.8, is **computed**;
  - (b) AR_wing 1.82–4.16 is a **derived** number. It is 2 × measured per-fin L²/A, and that the
    ×2 applies to Fulton 2016's values is an inference;
  - (c) it is a **proxy** from another family, sampled with a skew towards high AR.
- The source document itself correctly says "measured proxy". The harvested record drops "proxy" and
  calls the derived ×2 value "measured, full-text".
- Under the honesty floor, a derived number presented as measured is a defect even when the number is
  right. The honest label is: **computed from a measured proxy** (labrid per-fin AR, full-text),
  converted by an inferred ×2.

## 6. Counter-examples and taxa missed

- **Gasteropelecidae (freshwater hatchetfishes)** are otophysans, much closer relatives of *Danio*
  than labrids or exocoetids are. They have enlarged pectoral fins and a reputation for brief aerial
  excursions. They are the obvious nearer proxy and are not considered.
  - I found no AR or span number for them. I ran no search in this review, so their value is
    `unknown`.
  - This is a gap, not a refutation.
- **Pantodon** (freshwater butterflyfish) is a similar case: `unknown`, not searched.
- I found no published counter-example that breaks the 1.8–4.2 labrid range or the saturation
  result. The scope of this check is only the two papers re-read above. I ran no new literature
  search.

## 7. Bottom line

- **Survives:**
  - every number the claim states (independently recomputed, within ≤0.04);
  - the Table 1 values (re-read in full text, same hash);
  - the ×2 convention for Walker 2013;
  - AR 4 sitting at the top of the sample;
  - the span-limited saturation near 4.8–5.0 under a CL cap of 0.9–1.07.
- **Weakened:**
  - the evidence label: computed and derived values are recorded as "measured";
  - the scope: a top-3-abundance, wave-crest labrid sample is called the "teleost" range;
  - the completeness: body drag area is as sensitive as span in the saturated regime, and saturation
    depends on the CL cap.

## Sources

| source | read-level |
|---|---|
| S2-D-deepen.md and S2-D-deepen_calc.py, branch `claude/s2-d-sensitive-input-rasran` | full-text |
| Fulton, Wainwright, Hoey & Bellwood 2016, Ecol Evol, doi 10.1002/ece3.2624, PMC5214093 (sha256 `453217874266ea9c…`) | full-text |
| Walker, Alfaro, Noble & Fulton 2013, PLoS ONE 8:e75422, PMC3799785 (sha256 `83ab57b356b431f7…`) | full-text |
| Park & Choi 2010, J Exp Biol 213:3269 | could-not-access in this review (relayed from the author's partial full-text) |
| Fulton, Bellwood & Wainwright 2005; Wainwright, Bellwood & Westneat 2002 | could-not-access (not attempted) |

```swarm-challenge
{"claim_id": 131, "outcome": "weakened", "reason": "All numbers reproduce independently (L/D 3.74-4.90 vs 3.70-4.88; saturation peak 4.85 at AR 6.5), but the record labels as 'measured' a computed L/D and a derived 2x AR taken from a top-3-abundance, high-AR-biased labrid sample called 'teleost', and the span-limited saturation depends on the CL cap with body drag area at least as sensitive as span.", "corrected_value": "AR_wing 1.82-4.16 = derived (2 x measured per-fin L^2/A, convention inferred) from a high-AR-biased labrid sample, not a teleost range; whole-animal L/D 3.2-4.9 computed (2.8-5.5 across the claim's own lambda 1.4-2.0 and e 0.5-0.9 brackets); evidence level should be 'computed from measured proxy'", "depends_on": ["Fulton et al. 2016 Ecol Evol Table 1 labrid pectoral AR 0.91-2.08, top-3 species per wave-swept crest (full-text, re-read, sha256 45321787...)", "Walker et al. 2013 PLoS ONE pectoral AR = 2*L^2/A doubled convention (full-text, re-read)", "inference: Fulton 2016 values are the undoubled per-fin L^2/A", "S2-D model inputs as stated: rho 1.2, nu 1.5e-5, m 0.4 g, S 9 cm^2, e 0.7, CD0 = lambda x Blasius with lambda 1.4-2.0, CL cap 0.9, body 32x7x4 mm ellipsoid form factor 1.5 + 2 cm^2 median fins (all assumed)", "flying-fish pectoral 0.65-0.77 SL (search-summary, relayed via S22-D)", "zebrafish reachable span 0.36-0.43 SL (inference, relayed from S22-D-D)", "Park & Choi 2010 flying-fish AR 9.0-10.7 (could-not-access here; relayed)", "independent brute-force drag-minimisation script challenge-131_check.py (computed)"]}
```
