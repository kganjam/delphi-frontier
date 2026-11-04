# Challenge 23: "The C_L,max ≤ 0.6 ceiling does NOT hold"

**Claim under attack:**

> "The CL_max <= 0.6 ceiling does NOT hold: it derives from a thick NACA 0012 proxy at Re ~2e4,
> where measured THIN wings at Re 7e2–1e4 give a steady CL_max of 0.9–1.15."
> Recorded evidence level: *literature*. Value: 1.07 CL_max. Source: the adversarial challenge to
> claim 5 (`challenge-5.md`, branch `origin/claude/zebrafish-glide-challenge-b7n5z9`), which agrees
> independently with `S2-low-reynolds-aero.md` (branch `origin/claude/s2-low-reynolds-aero-acdwr7`).

**Reviewer's status:** I ran no experiment and built no wing. Below, each number is labelled as
calculated by me, measured by others and relayed, or my own inference. Every source carries a
read-level.

**Verdict: weakened.** The direction is right. No steady C_L,max I found for thin insect-type wings
in this Re band is as low as 0.6. But the claim goes further than its evidence in three ways:

1. **The range is cherry-picked.** The 0.9–1.15 band takes the two best species. By the source's
   own account (relayed), those species exceed every other insect except the locust. It also
   counts a glide-observed C_L (0.93) as a C_L,max. Within the same Re band, the repository's own
   sources give **0.7–0.9** for other dragonfly species, and **≈ 0.8** for a thin aerofoil at
   Re 1e4.
2. **The Re span is overstated.** The 0.9–1.15 values come from Re 700–2,400. The only figure
   reached at Re 1e4 is ≈ 0.8, which falls outside the claimed band.
3. **"Does NOT hold" is stronger than relayed, unread data on a different structure can
   support.** The quantity that matters is the C_L,max of a fish-fin membrane in air. That value
   is `unknown`. What the evidence supports is that "≤ 0.6" is unsupported as a *probable*
   ceiling. It has not been shown false for a fin.

---

## 1. Arithmetic, redone independently (calculated)

The claim itself contains no arithmetic. Its consequence is that a higher C_L,max lowers the
required speed. I checked that from the parent inputs: m = 0.4 g, W = 3.924e-3 N, ρ = 1.2 kg/m³,
ν = 1.5e-5 m²/s, span 0.04 m, AR 5 (so S = 3.2 cm²), and Ucrit 0.548 m/s.
V = √(2W/(ρ S C_L)), and design Re = √(2W/(ρ C_L AR))/ν.

| C_L,max | V_stall (m/s) | × Ucrit | KE ratio | design Re (AR 5) |
|---|---|---|---|---|
| 0.6 | 5.84 | 10.65 | 113 | 3,113 |
| 0.7 | 5.40 | 9.86 | 97 | 2,882 |
| 0.8 | 5.05 | 9.22 | 85 | 2,696 |
| 0.9 | 4.77 | 8.70 | 76 | 2,542 |
| 1.07 | 4.37 | 7.98 | 64 | 2,331 |
| 1.15 | 4.22 | 7.69 | 59 | 2,248 |

This reproduces challenge-5's 4.37 m/s at C_L 1.07 (8.0×, 64×). It also confirms that the
corrected design Re (2.2e3–2.9e3) lies inside the 700–2,400 band of the dragonfly data, or just
above it. **The arithmetic is consistent. Even the most favourable value leaves a 7.7× speed gap,
so the parent verdict is unchanged.**

## 2. Proxy check: what stands in for the quantity that matters?

The quantity that matters is the steady C_L,max of a ray-supported teleost fin membrane, finite
and low-AR, in air at Re ≈ 2e3–3e3. The claim uses a different proxy: **isolated dragonfly and
damselfly wings**. These are stiff, corrugated, cuticular wings, measured on a balance in a wind
tunnel.

- *Better than the parent's proxy?* **Yes** (inference). It is the right Re, a thin sharp-edged
  section, and a finite wing. The NACA 0012 at Re 2e4 matches none of these. The claim's central
  move survives.
- *A good proxy for a fin?* **Not shown.** Corrugation is credited with raising lift at these Re:
  Kesel 2000, as relayed in a citing paper's summary, says corrugated profiles have "a much higher
  lift coefficient" than flat plates. A fin membrane between rays is compliant. It may camber, which
  would help, or flutter and lose shape in air, which would hurt. It also dries out. No measured
  polar of a fin membrane in air at any Re was found (search scope in §6). Transferring 1.07 to a
  fin is an **inference**, and the claim states it as a fact ("does NOT hold").
- *A second proxy hidden in the claim:* **C_L,max is not the glide operating C_L.** On thin
  plates at low Re, the steady C_L,max is reached at high incidence, where L/D is poor. That is
  textbook mechanism, remembered rather than retrieved, and I attach no number to it. The parent
  used 0.6 both as a *ceiling* and as a *design C_L*. Refuting the ceiling does not by itself
  justify flying at 1.07. The one operating-point datum in the band is the **0.93 recorded in free
  dragonfly glides**, and its source notes that it was not necessarily the maximum.

## 3. Hidden assumption: the top two species represent "thin wings"

The 0.9–1.15 range rests on Wakeling & Ellington 1997 (*J. Exp. Biol.* 200:543). My searches
returned, at search-summary level, a sentence relayed from that paper. It says the isolated-wing
values of **1.07 (*Sympetrum sanguineum*) and 1.15 (*Calopteryx splendens*) "are greater than those
recorded for all other insects except the locust."**

Relaxing the assumption that these two species are typical:

| Source | Re | Kind | C_L,max | Read-level |
|---|---|---|---|---|
| Wakeling & Ellington 1997, isolated wings | 700–2,400 | measured | 1.07 (*S. sanguineum*), 1.15 (*C. splendens*) | search-summary (this session: two independent search summaries; full text could-not-access) |
| Same paper, free glides | 700–2,400 | observed (operating C_L, not a max) | 0.93 | search-summary |
| `S2-low-reynolds-aero.md`, relaying the same paper | 700–2,400 | relayed | "other species ≈ 0.7–0.9" | that doc's level S; I could not confirm which species, `unknown` |
| *Sci. Rep.* 6:25706 (2016), relayed in S2 | 1e4 | relayed | "about 0.8" for a thin aerofoil | S, not re-read |
| "Other insects" (bumblebee, Dudley & Ellington 1990; *Drosophila*, Vogel 1967) | insect range | measured | **below Jensen's locust value** per a review relayed by search; the numbers themselves `unknown` (not retrieved) | search-summary |

I have kept these sources as they appear rather than averaging them. The honest band for steady
C_L,max of thin insect wings at Re 7e2–1e4 is **≈ 0.7–1.15**. The 1.07–1.15 values sit at its top,
and at Re ≈ 1e4 the single retrieved figure is ≈ 0.8. **Every value in that band is still above
0.6**, so the claim that the ceiling is too low survives the relaxation. The specific range
"0.9–1.15" and the headline value 1.07 do not.

## 4. Is the NACA 0012 attribution right?

Challenge-5 *inferred* that the parent's 0.455 → 0.59 pair comes from the NACA 0012. The claim
under attack drops the hedge and asserts "a thick NACA 0012 proxy". My search (search-summary of
Laitone 1997, *Exp. Fluids* 23:405; full text could-not-access, host not resolvable) retrieved:

- All the thin plates and the 5 % cambered plate were "relatively insensitive" to Re and
  turbulence. The NACA 0012 "was very seriously affected by either" below Re 5e4.
- At Re ≈ 20,700, very high turbulence cut the NACA 0012's L/D by 49 %, from 7.4 to 3.8.
- The 5 % cambered plate "had the highest lift coefficient at all angles of attack".
- The test articles were **rectangular finite wings**, not 2D sections.

Inference (mine): a +30 % turbulence-driven change in C_L,max fits the one turbulence-sensitive
section, so the attribution is **probable**. **It is not confirmed.** No retrieved text ties
0.455/0.59 to a named section. The claim should keep challenge-5's word "probably". A second point
works slightly against the claim: if the 0.59 belonged to a *plate* instead, the parent's
ceiling would have a better-matched basis than the claim allows. That is unlikely given the
insensitivity statement, but it is not ruled out.

## 5. Is the evidence level honest?

- "*literature*" is the right **category**: these are measurements by others, not derived numbers.
  But the read-level is **search-summary throughout**. Nobody in this chain, including this
  review, read Wakeling & Ellington or Laitone in full text. The record should say
  *literature (relayed, search-summary; primary not read)*.
- **Value 1.07** is a single species, the second-highest steady value in the insect literature
  per its own source. Recorded alone as *the* value, it overstates what is typical. The better
  record is the band 0.7–1.15, with 1.07–1.15 noted as the dragonfly upper end.
- **"Measured THIN wings ... 0.9"**: the 0.9 lower end is either the 0.93 glide observation,
  which is an operating C_L and not a C_L,max, or the top of S2's "0.7–0.9". Either way, a
  measured C_L,max of 0.9 as the band floor is not supported.
- **"does NOT hold"**: a categorical negative about a fin's C_L,max, built on relayed data from a
  different structure. The supported statement is narrower: *the ≤ 0.6 ceiling is not supported
  by the evidence offered for it and is contradicted by every relayed thin-insect-wing value in
  the band; the fin value is unknown.*

## 6. Counter-examples and missed regimes

- **Downward:** I found no published steady C_L,max ≤ 0.6 for a thin wing at Re 7e2–1e4. That
  search was limited to the five queries listed below. Values for bumblebee and *Drosophila* wings
  are reported as lower than the locust's, but I did not retrieve them, so I cannot say whether
  either falls near 0.6: `unknown`. That is the most likely place for a real counter-example, and
  it was not closed.
- **Low-AR translating plates at Re 300–500** (Taira & Colonius 2009, *J. Fluid Mech.* 623:187):
  abstract-level only. The full text host (authors.library.caltech.edu) did not resolve. No C_L
  values were obtained.
- **Upward:** the flying-snake section, measured at C_L,max 1.1–1.9 at Re 3e3–1.5e4 (relayed via
  challenge-5), is a thick 2D section in water. It is not evidence for a finite membrane wing, so
  I do not use it.

**Negative-search scope.** Six web searches covered Wakeling & Ellington 1997, its species values,
Laitone 1997, Sunada et al. 1997, Kesel 2000 / Okamoto 1996, Taira & Colonius 2009, and insect
C_L,max comparisons. Four full-text fetches failed with DNS resolution errors: cob.silverchair.com,
springerlink.bibliotecabuap.elogim.com, acnpsearch.tweb-dev.unibo.it and
authors.library.caltech.edu. No Sunada, Kesel or Okamoto C_L,max number was retrieved. No fin-membrane
polar in air at any Re was found.

## 7. Corrected statement

> The parent's "C_L,max probably ≤ 0.6" is unsupported. It rests on one search-summary value,
> probably (not confirmed) from a NACA 0012 at Re ≈ 2e4. Relayed measurements on thin insect wings
> at Re 7e2–1e4 give a steady C_L,max of about **0.7–1.15**: 1.07–1.15 for the two best dragonfly
> species at Re 700–2,400, about 0.8 for a thin aerofoil at Re 1e4, and 0.93 observed in free
> glides. All are above 0.6. The C_L,max of a fin membrane in air is `unknown`. With any value in
> the band, the required glide speed is still 7.7–9.9× Ucrit (calculated), so the launch barrier
> stands.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| `challenge-5.md` (branch `origin/claude/zebrafish-glide-challenge-b7n5z9`) | full-text | the claim's origin and wording |
| `S2-low-reynolds-aero.md` (branch `origin/claude/s2-low-reynolds-aero-acdwr7`) | full-text (its sources are A/S) | "other species ≈ 0.7–0.9"; *Sci. Rep.* "≈ 0.8 at 1e4" |
| `zebrafish-glide-physics.md` (branch `origin/claude/zebrafish-glide-physics-j176og`) | full-text | parent basis for 0.6 (Laitone 0.455 → 0.59, section unidentified) |
| Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543 ([ResearchGate](https://www.researchgate.net/publication/13905162), [JEB](https://journals.biologists.com/jeb/article/200/3/543/20259/)) | search-summary; full text could-not-access | 1.07 / 1.15 isolated wings; "greater than all other insects except the locust"; 0.93 in glides |
| Laitone 1997, *Exp. Fluids* 23:405 ([typeset listing](https://typeset.io/papers/wind-tunnel-tests-of-wings-at-reynolds-numbers-below-70-000-4fxq9x7odp)) | search-summary; full text could-not-access | plate insensitivity; NACA 0012 L/D 7.4 → 3.8 at Re 20,700; rectangular finite wings |
| Kesel 2000, *J. Exp. Biol.* 203:3125 ([ResearchGate](https://www.researchgate.net/publication/12319395)) | search-summary (via a citing paper) | corrugation raises lift; no C_L,max number |
| Dudley & Ellington 1990; Vogel 1967; Jensen 1956 | search-summary (via a review) | other insects' steady C_L,max below the locust's; numbers `unknown` |
| Taira & Colonius 2009, *J. Fluid Mech.* 623:187 ([Caltech](https://resolver.caltech.edu/CaltechAUTHORS:20090629-092825317)) | abstract (search-summary); full text could-not-access | unretrieved lead; no numbers used |
| Sunada, Sakaguchi & Kawachi 1997, *J. Fluids Eng.* 119:129 | listing | no number retrieved |

```swarm-challenge
{"claim_id": 23, "outcome": "weakened", "reason": "Every relayed steady C_L,max for thin insect wings at Re 7e2–1e4 is above 0.6, so the ceiling is unsupported. But the claim's 0.9–1.15 band picks the two top species (which, per their own source, beat all insects except the locust) and counts a 0.93 glide-observed C_L as a maximum. The band's Re span stretches to 1e4, where the only value is ~0.8. The NACA 0012 attribution is an unconfirmed inference. 'Does NOT hold' asserts a fin-membrane result that remains unknown, on search-summary-level evidence.", "corrected_value": "steady C_L,max ≈ 0.7–1.15 for thin insect-type wings at Re 7e2–1e4 (measured by others, relayed at search-summary level; 1.07–1.15 are the upper dragonfly values at Re 700–2,400, ≈0.8 at Re 1e4); fin-membrane C_L,max in air unknown"}
```
