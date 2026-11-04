# Claim 234 — entailment to organ and behaviour scales

**Source claim (organism scale, evidence: derived).** S29's "property of size" conclusion is wrong
in sign. Required specific energy scales as m^β (β = 1/3 geometric, 0.36–0.53 measured in
exocoetids, Fish 1990 Tables I–III), while single-stroke LaMSA supply per kg is size-independent
(Sutton 2019, α = 0). Since β > α the budget closes as mass *decreases*, so the crossover is an
*upper* bound.

**Context gap.** S29 is not in this repository (searched the repo for `S29`, `LaMSA`, `Sutton
2019`, `flying fish`, `Exocoet`: no hits outside this file). I checked claim 234 as written and did
not check S29's original wording.

**What I ran.** No experiment and no simulation. Every number below is one of three kinds, and each
sentence says which: **measured** (an observation reported in a source), **derived** (my own
arithmetic on measured or model numbers, done in a Python one-liner), or **model parameter** (an
input to someone else's model).

## Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| Fish, F. E. (1990) Wing design and scaling of flying fish with regard to flight performance. *J. Zool., Lond.* 221: 391–403. PDF from health-sciences.wcupa.edu, sha256 `1efed334…21f8ea` | **full-text** (pdftotext of the PDF; Tables I–III and the Discussion read) | β; mass range; take-off speeds; taxi length (relayed) |
| Sutton, G. P. et al. (2019) Why do large animals never actuate their jumps with latch-mediated springs? Because they can jump higher without them. *Integr. Comp. Biol.* 59(6): 1609–1618, PMC6907395 | **abstract + targeted excerpts** (a WebFetch summary answering specific questions; I did not read the whole paper) | α = 0; model energy densities; 2.5 g crossover |
| Bullimore, S. R. & Burn, J. F. (2005) Scaling of elastic energy storage in mammalian limb tendons: do small mammals really lose out? *Biol. Lett.* 1: 57–59, PMC1629047 | **targeted excerpts** (WebFetch) | the measured-anatomy counter-case to α = 0 |
| Pollock & Shadwick (1994a), via Bullimore & Burn | **could-not-access** (seen only as cited by Bullimore & Burn) | exponent 1.28 |
| Hubbs (1933), Edgerton & Breder (1941), Shoulejkin (1929) and others, via Fish 1990 | **could-not-access** (seen only as cited by Fish 1990) | taxi 9 m; take-off 10 → 16–20 m/s; fish under 0.05 m do not fly |
| Davenport, J. (1994) How and why do flying fish fly? *Rev. Fish Biol. Fish.* | **search-summary** | tail beats "up to 50 per second" while taxiing |
| Deng et al., bioRxiv 10.1101/765560 | **search-summary** (full-text fetch returned HTTP 429) | tail beats 50–70 per s; glide 15–20 m/s |
| APS March Meeting 2024 abstract, s27/13 | **search-summary** | tail-slap frequency 13.5 Hz (disagrees with the above; see C4) |
| Burrows, M. (2003) Froghopper insects leap to new heights. *Nature* 424: 509 | **search-summary** (consistent across several snippets; full text not read) | best-in-class LaMSA specific energy |

---

## C1 — organ / range — the wing-loading mass exponent must exceed the supply exponent

**Requirement.** The claim's sign rests on β > α. The required specific energy is ½v², and the
minimum glide speed v ∝ √(W/S). So β is the mass exponent of wing loading (W/S), an organ-scale
(fin) property. β must be strictly greater than α = 0, and must be measured, not assumed.

**Check: satisfied (measured).** Fish 1990, Table II (full-text) gives the r.m.a. exponent of wing
loading on body mass:

| Genus | N | b | 95% CI | vs 0.33 |
|---|---|---|---|---|
| *Cypselurus* | 113 | 0.400 | 0.372–0.430 | P = 0.002 |
| *Danichthyes* | 11 | 0.533 | 0.464–0.614 | P = 0.001 |
| *Exocoetus* | 26 | 0.360 | 0.262–0.495 | ns |
| *Fodiator* | 9 | 0.434 | 0.284–0.663 | ns |
| *Hirundichthyes* | 21 | 0.526 | 0.502–0.551 | P = 0.001 |
| *Parexocoetus* | 19 | 0.408 | 0.257–0.649 | ns |

Fish states that "the exponents are all significantly different from zero (P < 0.001)". The
claim's range "0.36–0.53" matches Fish's own summary ("ranging from 0.36 to 0.53"). The smallest
lower CI bound is 0.257 (*Parexocoetus*). Fish links speed to wing loading in the Discussion: "the
horizontal and vertical speeds are directly proportional to the square root of the wing loading
(Pennycuick, 1972)". So β = b(W/S) is the author's own link and not my inference.

Two corrections to the claim's wording:

- **Tables I and III do not carry β.** Table I has length, span and area exponents, and Table III
  has aspect ratio. Only Table II gives the wing-loading exponent.
- **"β = 1/3 geometric" is the isometric prediction.** Three of the six genera do not differ from
  it.

**Disagreement on α that has to be kept, not averaged away.** α = 0 is a *model result* in Sutton
2019 ("jump height in spring-actuated systems is independent of size"), built from model
parameters (muscle 15.0 J/kg, of which the spring "can maximally store only 28%", giving 4.2 J/kg).
It is not a measurement. The only measured-anatomy exponent I found points the other way:

- Bullimore & Burn (2005) relay Pollock & Shadwick (1994a): limb-tendon storage *capacity* scales
  as M^1.28 in mammals. That is ∝ M^0.28 per kg (derived).
- Bullimore & Burn also say the capacity is "likely to be utilized only rarely".
- This is cyclic, mammalian and tendon-based, and is not LaMSA in fish.

If α ≈ 0.28 rather than 0, the sign β > α still holds for *Cypselurus*, *Danichthyes* and
*Hirundichthyes*, whose lower CI bounds are 0.37–0.50. It is **undetermined** for *Exocoetus*
(0.262) and *Parexocoetus* (0.257), and marginal for *Fodiator* (0.284). This inference is mine.

## C2 — organ / energetic — a single-stroke spring must deliver the take-off specific energy

**Requirement.** For the budget to "close" at any mass, some single-release elastic element must
supply, per kg of body, at least the specific kinetic energy at take-off.

**Required specific energy.**

- *Derived from measured speeds:* take-off speeds of "10 to 16–20 m/s" (Fish 1990, relaying
  Shoulejkin 1929, Edgerton & Breder 1941 and others) give ½v² = **50–200 J/kg**.
- *Derived from measured wing loadings, with an assumed lift coefficient:* minimum glide speed
  v = √(2(W/S)/(ρC_L)), with ρ = 1.2 kg/m³ and assumed C_L = 1.0–1.5.
  - At 11.7 N/m² (0.001 kg *Hirundichthyes*): 3.6–4.4 m/s, so **6.5–9.8 J/kg**.
  - At 208.9 N/m² (0.53 kg *Danichthyes*): 15–19 m/s, so 116–174 J/kg. This agrees with the
    measured 16–20 m/s.

**Supply.**

- *Model parameter:* Sutton's 4.2 J/kg of muscle × 10–20% muscle fraction gives **0.42–0.84 J/kg
  of body** (derived).
- *Measured:* the best froghopper jumps, at 4 m/s on 12.3 mg (Burrows 2003, search-summary), give
  ½v² = **8.1 J/kg**. The mean jump at 2.8 m/s gives 3.9 J/kg.

**Check: unsatisfied.** No single-stroke biological spring I found reaches the 50 J/kg that the
lowest measured take-off speed needs. The best I read (8.1 J/kg) is about 6× short. Sutton's model
supply is 60–480× short.

- **Why this is not `unsatisfiable`:** no measurement shows that 8.1 J/kg is a *ceiling*. It is the
  best case I read.
- **Search scope:** Sutton 2019, Burrows 2003, a web search for tendon and resilin energy density,
  and a search for Ilton et al. 2018 (*Science* 360: eaao1082). The Ilton energy-density table was
  **not accessed**: the full text was not retrieved, and par.nsf.gov is blocked from this session.
- **Not checked:** measured specific energies of other LaMSA systems (fleas, click beetles, springtails).

The derived glide-minimum figure (6.5–9.8 J/kg at 1 g) is within reach of the froghopper number,
so the verdict depends on whether take-off needs the glide minimum or the measured 10+ m/s. See C5.

## C3 — organ / existence — a latch and a spring must exist in the exocoetid launch apparatus

**Requirement.** The claim's supply term is *single-stroke LaMSA*. For the claim to describe
exocoetids rather than a hypothetical launcher, there has to be an elastic store loaded slowly and
released by a latch, in the caudal or axial propulsor.

**Check: unsatisfied — I found nothing, and the search was narrow.**

- **What I searched:**
  - the Fish 1990 full text, which describes thrust from the hypocaudal lobe during the taxi and no
    latch;
  - the search summaries for Davenport 1994 and Deng et al.;
  - a web search for `flying fish Exocoetidae elastic energy storage latch take-off spring tendon
    caudal`.
- **What came back:** active tail-beat propulsion only, with no latch, catch or tendon store
  reported.
- **What I did not search:** primary anatomical or functional-morphology literature on exocoetid
  axial tendons, and Breder 1930. The finding is therefore "not found in a shallow search", not
  "people looked and found nothing".

## C4 — behaviour / timescale — take-off energy must be delivered in one release

**Requirement.** Single-stroke supply means that the kinetic energy at take-off is delivered within
one release, on the millisecond scale of LaMSA. Burrows 2003 (search-summary) estimates about 1 ms
for the froghopper. That has to be fast compared with the take-off behaviour, and the take-off must
not be a train of strokes.

**Check: unsatisfiable for taxiing exocoetids (measured values contradict it).**

- **Taxi length:** "The average taxi is 9 m (Hubbs, 1933)". During the taxi "the elongated
  hypocaudal lobe of the caudal fin continues to remain in the water and generate thrust increasing
  speed for take-off from 10 to 16–20 m/s" (Fish 1990, full-text, relaying Hubbs and others).
- **Tail-beat rate:** Davenport reports tail beats "up to 50 per second" while taxiing
  (search-summary). Deng et al. report 50–70 strokes per second (search-summary).
- **Implied duration (derived):** 9 m at 10–20 m/s takes 0.45–0.9 s, which is about 22–45 beats at
  50 Hz. That is two to three orders of magnitude longer than a single release.
- **Disagreement on beat rate, kept:** an APS 2024 abstract reports a 13.5 Hz tail-slap frequency
  (search-summary). That may be a different quantity. At 13.5 Hz the taxi is still about 6–12 strokes
  (derived), so it is multi-stroke whichever rate is right.

**Scope.**

- The contradiction holds for *Cypselurus*-type taxiing genera.
- For *Exocoetus*-type launches, Fish describes "emergence from the water at an angle up to 45°"
  with a short taxi. I found no stroke count for those, so their status is **open**.

**Consequence (my inference).**

- What this refutes is applying a *single-stroke* supply term to the animals whose β is used. It
  does not refute the inequality β > α itself.
- Real exocoetids supply take-off energy cyclically, with muscle and many strokes. Their per-kg
  supply exponent is then set by the work per stroke × the number of strokes, and the number of
  strokes is free to grow with taxi length.
- So α = 0 is not established for the organism the claim is about.

## C5 — behaviour / range — the closure mass must fall inside the mass window where gliding happens

**Requirement.** If the crossover is an upper bound, there has to be a mass range in which the budget
closes *and* the animal glides. That means the closure mass must lie at or above the smallest
gliding exocoetid.

**The lower edge of gliding.** Fish 1990 (full-text, relaying Hubbs 1933): "Young *Cypselurus* less
than 0.05 m long do not fly". Converting with Fish's *Cypselurus* length regression
(L = 0.460 M^0.355) gives about **1.9 g** (derived; the units are assumed to be m and kg). Fish's
specimens span "0.003 to 0.53 kg" in the Results text, but the same page quotes a wing loading for
"a 0.001 kg *Hirundichthyes*". That is an internal inconsistency in the source, and I keep both
figures.

**Closure mass (derived).** Supply is the 8.1 J/kg froghopper figure. Requirement is the glide
minimum at 1 g (C2), scaled as m^β with β = 0.33–0.53.

- C_L = 1.0: closure ≈ 0.57–0.71 g, below the 1.9 g flight threshold.
- C_L = 1.5: closure ≈ 1.5–1.9 g, at the threshold.
- Using the measured ≥10 m/s take-off instead: closure falls much lower, but I cannot place it,
  because the take-off speeds are not mass-resolved in what I read.

**Check: open.** The answer turns on an assumed C_L and on take-off speed in the smallest fliers,
which I found no measurement of. On either assumption the window is at best marginal.

**Prior art bearing on the claim's novelty.** Sutton 2019 itself concludes that "animals smaller
than this point can jump higher with a spring-actuated mechanism", with a simulated crossover of
about 2.5 g. So the result that "the crossover is an upper bound on mass" is already Sutton's
conclusion for jumping. Claim 234 adds only the gliding-requirement exponent β.

---

## Net result

| # | Scale | Kind | Status |
|---|---|---|---|
| C1 | organ | range | **satisfied** (measured, Fish 1990 Table II), but α is contested (0 from a model vs ≈0.28 from mammal tendons) |
| C2 | organ | energetic | **unsatisfied** (the best single-stroke spring I read is about 6× short of 50 J/kg) |
| C3 | organ | existence | **unsatisfied**, narrow search (no latch or spring reported in exocoetids) |
| C4 | behaviour | timescale | **unsatisfiable** for taxiing genera (measured 9 m multi-beat taxi) |
| C5 | behaviour | range | **open** (depends on an assumed C_L) |

**Sign.** The *sign* argument (β > α ⇒ upper bound) survives at the organ scale, provided α = 0.

**Supply side.** The supply side is refuted from below as a description of exocoetid behaviour:
taxiing flying fish are not single-stroke launchers (C4). C2 and C5 show that even a hypothetical
single-stroke glider would sit at or below the smallest size at which exocoetids fly at all.

**Scope of the claim.** Claim 234 should be rescoped to a *hypothetical single-stroke launcher that
uses exocoetid wing-loading scaling*. It should not be read as a statement about flying fish.

```swarm-entail
{"source_claim": 234, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The mass exponent of the lifting surface's loading (which sets required specific energy via v^2 proportional to W/S) must exceed the mass exponent of per-kg energy supply (alpha = 0 in the claim).",
      "quantity": "r.m.a. exponent b of wing loading on body mass", "lo": 0.0, "hi": null, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Fish 1990 Table II: b = 0.360-0.533 across six exocoetid genera, all P<0.001 vs 0; lowest 95% CI bound 0.257 (Parexocoetus)",
      "satisfied_evidence": "measured",
      "note": "Fish 1990 J Zool 221:391-403 (full-text). beta is in Table II only, not Tables I/III as the claim says. alpha=0 is a model result (Sutton 2019 ICB 59:1609, excerpts); measured mammal tendon storage capacity scales M^1.28, i.e. M^0.28 per kg (Pollock & Shadwick 1994 via Bullimore & Burn 2005 Biol Lett 1:57, excerpts; P&S not accessed). If alpha=0.28, sign holds for Cypselurus, Danichthyes, Hirundichthyes; undetermined for Exocoetus and Parexocoetus; marginal for Fodiator."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "A single-release elastic element must supply, per kg body mass, at least the specific kinetic energy at take-off.",
      "quantity": "specific kinetic energy at take-off, 0.5 v^2", "lo": 50, "hi": 200, "units": "J/kg",
      "status": "unsatisfied",
      "satisfied_by": "None found. Best single-stroke LaMSA specific energy read: froghopper 8.1 J/kg (4 m/s, 12.3 mg; Burrows 2003). Sutton 2019 model supply is 0.42-0.84 J/kg body (derived from model parameters 4.2 J/kg muscle x 10-20% muscle).",
      "satisfied_evidence": "derived",
      "note": "lo/hi derived from measured take-off speeds 10-20 m/s (Fish 1990 relaying Shoulejkin 1929, Edgerton & Breder 1941). Glide-minimum alternative (assumed C_L 1.0-1.5): 6.5-9.8 J/kg at 1 g. Not unsatisfiable: 8.1 J/kg is not a measured ceiling. Searched: Sutton 2019, Burrows 2003 (search-summary), tendon/resilin energy-density web search; Ilton 2018 Science table not accessed; fleas, click beetles and springtails not checked."},
    {"target_scale": "organ", "kind": "existence",
      "statement": "An elastic energy store that is loaded slowly and released by a latch must exist in the exocoetid launch propulsor.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Not found. The sources read describe active, muscle-driven hypocaudal-lobe thrust during the taxi, with no latch or spring.",
      "satisfied_evidence": "unknown",
      "note": "Scope: Fish 1990 full-text; Davenport 1994 and Deng et al. bioRxiv 765560 at search-summary level; one web search for elastic storage, latch, spring, tendon in flying fish. Primary exocoetid axial or tendon anatomy literature and Breder 1930 not searched, so this is not-found-in-shallow-search, not looked-and-absent."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Take-off energy must be delivered within a single release (ms scale), fast relative to the take-off behaviour, not by a train of strokes.",
      "quantity": "number of propulsive strokes in take-off", "lo": 1, "hi": 1, "units": "strokes",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by measurement: average taxi 9 m with the hypocaudal lobe generating thrust from 10 to 16-20 m/s (Hubbs 1933 via Fish 1990); tail beats up to 50/s (Davenport) or 50-70/s (Deng et al.). Derived: 0.45-0.9 s, about 22-45 strokes.",
      "satisfied_evidence": "measured",
      "note": "Fish 1990 full-text, relaying Hubbs 1933 (not accessed); Davenport and Deng at search-summary level. Disagreement kept: APS 2024 abstract gives a 13.5 Hz tail-slap rate (still about 6-12 strokes, derived). Scope: holds for Cypselurus-type taxiing genera; for Exocoetus-type 45-degree emergence no stroke count was found (open). Refutes applying single-stroke supply to exocoetids, not the inequality beta > alpha itself."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The mass at which the energy budget closes (an upper bound) must lie at or above the smallest mass at which gliding behaviour occurs.",
      "quantity": "closure body mass relative to minimum gliding mass", "lo": 1.9, "hi": null, "units": "g",
      "status": "open",
      "satisfied_by": "Derived closure is 0.57-0.71 g (C_L=1.0) or 1.5-1.9 g (C_L=1.5) using 8.1 J/kg supply and the glide-minimum requirement; the flight threshold is about 1.9 g (Cypselurus under 0.05 m do not fly, Hubbs 1933 via Fish 1990, converted with Fish's length regression).",
      "satisfied_evidence": "derived",
      "note": "Turns on an assumed C_L and on take-off speed in the smallest fliers, which was not found mass-resolved. Fish 1990 is internally inconsistent on minimum specimen mass (0.003 kg in Results vs a 0.001 kg Hirundichthyes wing loading). Prior art: Sutton 2019 already concludes the LaMSA advantage holds below a crossover (simulated about 2.5 g)."}
  ]}
```
