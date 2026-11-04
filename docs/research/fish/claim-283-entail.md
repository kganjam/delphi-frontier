# Claim 283 — propagation to adjacent scales (tissue, organism)

**Source claim (organ scale, evidence: derived):** Required wing area at a 2 m/s launch with an
assumed CL 0.8 is ~20 cm², against a ~1.4 cm² whole-body dorsal silhouette: a ~14x shortfall,
falling to ~0.6x only if launch speed reaches 10 m/s.

**Date of check:** 2026-11-04. **Result in one line:** none of the four constraints is satisfied.
None is unsatisfiable. Two are open because the primary source that probably holds the deciding
number (Wiest 1995, full text) could not be reached from this session. One is unsatisfied
because the only available estimate is model-based and disagrees with the claim's implied mass.
One is unsatisfied because the required muscle power exceeds the measured values I found, but
the gap rests on an assumed duration and on muscle data from other species.

---

## 0. What the claim's numbers imply (derived, not observed)

The claim names no species, and nothing in this repository records its context (I searched the
repository for "283", "wing", "glid", "fish" and "dorsal silhouette"). **My inference, not the
claim's:** a ~1.4 cm² dorsal silhouette is consistent with a laterally compressed fish of
~3.5 cm, such as a freshwater hatchetfish (Gasteropelecidae, e.g. *Carnegiella strigata*,
max 3.5 cm SL per FishBase). That is the only family of small fish known for take-off from
water. Where I use hatchetfish literature below, the identification is my assumption.

Steady lift balance, L = ½ρv²S·CL = mg, with ρ = 1.2 kg m⁻³ and g = 9.81 m s⁻² (my calculation):

| quantity | value | how obtained |
|---|---|---|
| mass implied by 20 cm² at 2 m/s, CL 0.8 | **0.39 g** | calculated |
| area needed at 10 m/s | 0.80 cm² → 0.57x of 1.4 cm² | calculated (matches the claim's ~0.6x) |
| launch speed at which silhouette alone suffices (S ∝ v⁻²) | **7.6 m/s** | calculated |
| kinetic energy per kg body at 7.6 m/s | 28.6 J kg⁻¹ | calculated |

So the claim is internally consistent, provided the body mass is ~0.39 g. That mass is not
stated in the claim. It is implied by it.

---

## 1. Constraints (ENTAIL)

If claim 283 is true and meaningful, the following must hold.

**C1 — organism / range.** The realistic water-exit speed of the organism must lie below the
break-even speed of ~7.6 m/s (lo ~1, hi 7.6 m s⁻¹). Otherwise the "shortfall" does not
describe the animal. The 2 m/s launch in the claim is an assumption, and this is the
requirement that it be representative.

**C2 — organism / range.** Body mass must be close to the value the claim's area implies,
~0.39 g (taken as 0.3–0.5 g). If it is not, the "~20 cm²" figure is wrong. The required area
scales linearly with mass.

**C3 — organism / spatial.** The organism's total extended lifting planform (body plus spread
paired fins) must be well below the 20 cm² required at 2 m/s. That area is ~14x the silhouette,
roughly a 4.5 × 4.5 cm square on a ~3.5 cm fish. If the fins spread to supply it, there is no
shortfall.

**C4 — tissue / energetic.** For the escape branch of the claim (launch at ≥7.6–10 m/s), the
locomotor muscle must supply at least 28.6 J kg⁻¹ body within the launch run. This is a lower
bound with drag ignored. As power, the bound depends on run duration t. With an assumed muscle
fraction of 0.3–0.5 of body mass (calculated):

| assumed t | run length d = ½vt | W kg⁻¹ body | W kg⁻¹ muscle (f = 0.5 … 0.3) |
|---|---|---|---|
| 20 ms (single fast start) | 7.6 cm (~2 BL) | 1430 | 2860 … 4760 |
| 50 ms | 19 cm | 570 | 1140 … 1900 |
| 100 ms | 38 cm (~11 BL) | 290 | 570 … 950 |
| 200 ms | 76 cm (~22 BL) | 143 | 290 … 480 |

---

## 2. Checks

### C1 — exit speed below 7.6 m/s → **open**

- **Hatchetfish:** Wiest, F.C. (1995), *J. Zool.* 236: 571–592. Read-level: **search-summary**
  (abstract as paraphrased by search; Wiley page **could-not-access**: the host is outside this
  session's allowed network domains). The author used 200 fps video and reports a take-off made
  of pectoral abduction plus a C-start, with trajectories "consistent with projectile motion",
  and concludes that active flight is unlikely. No exit speed appeared in anything I could read.
  The paper has kinematics, so the number probably exists in the full text. This is
  "not read by me", **not** "looked for and found nothing".
- **Context, other taxon:** Makiguchi et al. (2013), *Aquatic Biology*. Read-level:
  **search-summary**. With accelerometer loggers on *Cypselurus heterurus doederleini*, a
  specialist flying fish many times larger, they estimated water-exit speeds of
  **3.9–5.2 m s⁻¹**, which is 38.7–51.5% of stroboscope-based maximum swimming speeds. Flight
  speeds of 10–20 m s⁻¹ come after taxiing, not at exit (secondary aerodynamics source,
  search-summary). **My inference:** if a specialist flier much larger than the claim's fish
  exits below 7.6 m/s, a ~3.5 cm fish probably does too. That is an inference across taxa and
  is not evidence that meets C1.
- **Small-fish burst speed:** searched for "maximum burst swimming speed small fish … 3 cm" and
  "zebrafish adult escape peak velocity". I found no sourced m/s value for a 2–4 cm fish. Relative
  burst speed falls with size and absolute speed rises (carp 1–9 cm, search-summary only).
- **Scope of the negative:** web search only, four queries. No full-text access to Wiest 1995,
  Domenici & Blake 1997 (*J. Exp. Biol.* 200: 1165–1178) or Davenport 1994 (*Rev. Fish Biol.
  Fish.* 4: 184–214).

### C2 — body mass ≈ 0.39 g → **unsatisfied**

- No measured mass for the organism was found. The organism itself is my inference.
- FishBase Bayesian length–weight relationship for *C. strigata*. Read-level:
  **search-summary**, with two mirrors that disagree. One gives a = 0.01950, b = 3.14; the other
  a = 0.01660, b = 3.13; both in cm total length. **These are model estimates (based on LWRs for
  the species and its subfamily–body shape), not measurements.** At 3.5 cm TL they give
  **0.84–1.0 g** and at 4 cm TL **1.5 g** (my arithmetic). Both mirrors give 2–4x the implied
  0.39 g. I keep the two mirrors separate rather than averaging them.
- Direction: a heavier fish raises the required area, so the claim's qualitative conclusion
  (a shortfall) gets **stronger**, but its stated "~20 cm²" and "~0.6x at 10 m/s" would be wrong.
  At ~1 g the area at 10 m/s would be ~2.0 cm² (calculated), i.e. still **short** of 1.4 cm².
  This is why C2 matters.
- Not unsatisfiable: no **measured** mass contradicts 0.39 g.
- Scope: one search on *Carnegiella strigata* length–weight. No museum or aquarium body-mass
  data were searched.

### C3 — extended planform ≪ 20 cm² → **open**

- I found no measured pectoral-fin area for any gasteropelecid. Wiest 1995 (search-summary)
  describes enlarged pectoral fins and hypertrophied abductor muscles but gives no area I could
  read. The figure that pectoral muscle is "up to one-quarter of body weight" (Wikipedia)
  traces to a pet-fish website, not to Wiest, so I do not cite it as a measurement.
- It is very plausible that fins on a 3.5 cm fish do not spread to 20 cm². Plausibility is not
  a check, so this stays open.
- Scope: one search. No morphometric databases or full texts were consulted.

### C4 — muscle energetics for the ≥7.6 m/s branch → **unsatisfied**

- **Measured fast-muscle power, other species:**
  - Wakeling & Johnston (1998), *J. Exp. Biol.* 201: 1505–1526. Read-level: **search-summary**.
    Work-loop mean of **142.7 W kg⁻¹** muscle in fast myotomal fibres of *Scorpaena notata* at
    20 °C. Power rose with temperature and with the travel rate of the body-curvature wave.
  - Sculpin fast-start study, *J. Exp. Biol.* 201: 913 (1998). Read-level: **search-summary**.
    Authors not confirmed by me. Mean maximum *instantaneous* power **307 W kg⁻¹** (C-bend) and
    222 W kg⁻¹ (contralateral), independent of body size.
  - Sculpin fibres, *J. Exp. Biol.* 185 (1992). Read-level: **search-summary**. Instantaneous
    power during shortening 175–265 W kg⁻¹, and 25–30 W kg⁻¹ averaged over swimming tail-beat
    cycles.
- **Comparison (my inference):** the requirement exceeds the highest measured value I found
  (307 W kg⁻¹) for every assumed run shorter than about 0.2 s. At 20 ms, a single fast start,
  it exceeds that value by 9–15x. Only a run of ≳0.2 s and ≳20 body lengths, with drag
  ignored, comes down to the measured range.
- **Why this is not `unsatisfiable`:** the required number depends on an **assumed** duration
  and muscle fraction, not a measured one. The measured powers are from scorpaeniform fishes,
  not from the claim's organism. Elastic energy storage or a multi-beat surface taxi (as
  described for exocoetids, ~50 beats s⁻¹, Davenport 1994, abstract-level via search) would
  spread the energy over a longer time. So no measured number contradicts C4. Nothing found
  meets it either.
- Scope: two searches. No data on gasteropelecid muscle power, or on power amplification in
  fish water-exit, were found or searched for beyond these.

---

## 3. What would settle it

1. Wiest 1995 full text: exit speed (C1) and pectoral fin area (C3). This one paper likely
   decides two constraints. It needs `onlinelibrary.wiley.com` (or a ResearchGate copy)
   allowed in the session's network settings.
2. Any measured wet mass for a hatchetfish of known length (C2).
3. Fast-start launch duration from water-exit kinematics in a small fish, which turns the C4
   table into a single measured comparison.

## Sources

- Wiest 1995 abstract page (could-not-access; seen through search summary): https://zslpublications.onlinelibrary.wiley.com/doi/abs/10.1111/j.1469-7998.1995.tb02733.x
- Seriously Fish, *Carnegiella* pages (listing): https://www.seriouslyfish.com/species/carnegiella-strigata
- Wikipedia, Gasteropelecidae (listing): https://en.wikipedia.org/wiki/Gasteropelecidae
- Makiguchi et al. 2013 (search-summary): https://doaj.org/article/493bffccbbca47fa8f3f04753091f546
- Davenport 1994 abstract (search-summary): https://data.zhenzhi.com/details/1/1008777797
- Wakeling & Johnston 1998 (search-summary): https://www.sciencegate.app/document/10.1242/jeb.201.10.1505
- Sculpin fast-start PDF, JEB 201:913 (search-summary): https://cob.silverchair.com/jeb/article-pdf/201/7/913/3399524/jexbio_201_7_913.pdf
- JEB 185:251 sculpin fibres (search-summary): https://next.sciencegate.app/document/10.1242/jeb.185.1.251
- Domenici & Blake 1997 (listing only): https://tethys.pnnl.gov/publications/kinematics-performance-fish-fast-start-swimming
- FishBase *C. strigata* (search-summary; two mirrors disagree): https://fishbase.se/summary/10736 , https://nrm-fishbaselinux01.nrm.se/summary/Carnegiella-strigata

```swarm-entail
{"source_claim": 283, "source_scale": "organ",
  "constraints": [
    {"target_scale": "organism", "kind": "range",
      "statement": "The organism's realistic water-exit (launch) speed must lie below the break-even speed at which its dorsal silhouette alone would support its weight at CL 0.8; otherwise the stated shortfall does not describe the animal.",
      "quantity": "water-exit speed", "lo": 1, "hi": 7.6, "units": "m/s",
      "status": "open",
      "satisfied_by": "No exit speed found for the (inferred) taxon. Wiest 1995 has 200 fps take-off kinematics but the full text could not be accessed. Only comparator: specialist flying fish Cypselurus heterurus doederleini exit at 3.9-5.2 m/s (Makiguchi et al. 2013), a different and much larger taxon.",
      "satisfied_evidence": "unknown",
      "note": "Wiest FC 1995 J Zool 236:571-592 (search-summary; Wiley could-not-access); Makiguchi et al. 2013 Aquatic Biology (search-summary). 7.6 m/s is calculated (S proportional to v^-2). Scope: 4 web searches; not read by me, which is different from looked for and absent."},
    {"target_scale": "organism", "kind": "range",
      "statement": "Body mass must be close to the value implied by the claim's own area figure (20 cm2 at 2 m/s, CL 0.8, rho 1.2 implies 0.39 g).",
      "quantity": "body mass", "lo": 0.3, "hi": 0.5, "units": "g",
      "status": "unsatisfied",
      "satisfied_by": "No measured mass found. FishBase Bayesian length-weight models for Carnegiella strigata (organism identity is an inference) give 0.84-1.0 g at 3.5 cm TL and 1.5 g at 4 cm TL. These are model estimates, not measurements; the two mirrors give different a (0.0195 vs 0.0166).",
      "satisfied_evidence": "literature",
      "note": "FishBase summary 10736 (search-summary). A heavier mass strengthens the qualitative shortfall but invalidates the stated 20 cm2 and the 0.6x at 10 m/s. Not unsatisfiable: no measured mass contradicts it. Scope: 1 search; no museum or aquarium mass data."},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "Total extended lifting planform (body plus spread paired fins) must be well below the ~20 cm2 required at 2 m/s, i.e. well below ~14x the dorsal silhouette.",
      "quantity": "extended planform area", "lo": null, "hi": 20, "units": "cm2",
      "status": "open",
      "satisfied_by": "No measured pectoral-fin area for any gasteropelecid found. Wiest 1995 describes enlarged pectoral fins without an area I could read.",
      "satisfied_evidence": "unknown",
      "note": "Wiest 1995 (search-summary). Plausible but unchecked, so left open. Scope: 1 web search; no morphometric databases."},
    {"target_scale": "tissue", "kind": "energetic",
      "statement": "For the escape branch (launch at >=7.6 m/s), locomotor muscle must deliver at least 28.6 J per kg body within the launch run, drag ignored; as power this is 143-1430 W/kg body for assumed runs of 0.2-0.02 s, i.e. ~290-4800 W/kg muscle at muscle fraction 0.3-0.5.",
      "quantity": "muscle mass-specific power during launch", "lo": 290, "hi": null, "units": "W/kg muscle",
      "status": "unsatisfied",
      "satisfied_by": "Highest measured fish fast-muscle values found: 142.7 W/kg work-loop mean (Scorpaena notata, 20 C) and 307 W/kg peak instantaneous (sculpin C-bend). Both are below the requirement for any assumed run under ~0.2 s. Requirement depends on an assumed duration and muscle fraction; the data come from other taxa; elastic storage or multi-beat taxiing could bypass it. Not unsatisfiable.",
      "satisfied_evidence": "literature",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505-1526 (search-summary); J Exp Biol 201:913 (1998), authors unconfirmed (search-summary); J Exp Biol 185 (1992) (search-summary). Requirement is calculated. Scope: 2 searches; no gasteropelecid muscle data searched beyond these."}
  ]}
```
