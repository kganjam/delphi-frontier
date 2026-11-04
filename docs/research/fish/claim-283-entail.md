# Claim 283: what it requires at the tissue and organism scales, and whether the literature agrees

**Source claim (organ scale, evidence: derived).** At a 2 m/s launch with an assumed CL of 0.8, the wing area needed is about 20 cm². The whole-body dorsal silhouette is about 1.4 cm², so the shortfall is about 14x. It falls to about 0.6x only if launch speed reaches 10 m/s.

**Date:** 2026-11-04. **Adjacent scales checked:** tissue, organism.

## 0. What I had to reconstruct, and the caveats that follow

- The repository has no record of claim 283, no `docs/research/fish/` directory, and no file naming the organism. I searched the working tree and all branches for "283", "hatchet", "glid", "wing" and "silhouette".
- **Organism identity is my inference.** The numbers fit a small, laterally compressed freshwater hatchetfish (Gasteropelecidae, e.g. *Carnegiella*, about 3.5 cm SL). Nothing in the repo confirms this. If claim 283 is about another animal, sections C1 and C2 need re-checking. C3–C5 depend only on body size and mass, so they carry over to any fish of about 3.5 cm and 0.4–0.8 g.
- **The claim's implied body mass is my calculation, not something the claim states.** I used L = mg = ½ρv²SC_L with ρ_air = 1.2 kg m⁻³, v = 2 m/s, C_L = 0.8 and S = 20 cm². That gives **m ≈ 0.39 g**.
- With that mass and S = 1.4 cm², lift equals weight at **v ≈ 7.6 m/s** (calculated). At 10 m/s the ratio is 0.57, which matches the claim's "~0.6x". The claim is internally consistent.

## 1. Constraints (ENTAIL)

If claim 283 is true, these must hold at the neighbouring scales:

| # | Scale | Kind | Requirement (generic) | Bound |
|---|---|---|---|---|
| C1 | organism | range | Body mass must match the mass implied by the organ-scale arithmetic, within a factor of about 2. | 0.2–0.8 g |
| C2 | organism | range | Measured water-exit speeds must sit well below the speed at which the silhouette alone could carry the body's weight. Otherwise the "shortfall" describes conditions that never occur. | ≤ 7.6 m/s |
| C3 | organism | conservation | Aerial paths must follow vertical-momentum balance under gravity alone (ballistic). No sustained lift should be detectable. | — |
| C4 | tissue | timescale | Axial locomotor muscle must be too slow to reach the 7.6–10 m/s escape route. The minimum contraction (half-cycle) time must be longer than the ~1.2–1.6 ms that tail-beat propulsion would need. | half-cycle > 1.6 ms |
| C5 | tissue | energetic | Mass-specific muscle power must be too low to accelerate the body to ≥ 7.6 m/s within the few body lengths available before water exit. | available < ~2,000 W kg⁻¹ muscle |

C4 and C5 test the claim's own escape clause ("unless launch speed reaches 10 m/s"). If muscle could reach those speeds, the claim's practical conclusion (no gliding lift at real launch speeds) would fail even though its arithmetic is right.

## 2. Checks

### C1: organism body mass, range 0.2–0.8 g → **open** (two estimates disagree, no measurement found)

- **Searched for:** "Carnegiella strigata body mass grams standard length hatchetfish weight".
- **Found:** No measured body mass for any *Carnegiella*. This is a "nobody has reported it where I looked" negative, not a "people looked and found otherwise" negative. The scope is one web search plus FishBase.
- **Length:** FishBase and Wikipedia give max SL 3.5 cm for *C. strigata*; Seriously Fish gives 30–35 mm. *(read-level: search-summary)*
- **FishBase length–weight estimate:** Bayesian a = 0.01622, b = 3.13 for this species and its relatives. This is not a fit to the species itself. *(read-level: search-summary)*
  - **My calculation:** W = 0.01622 × 3.5^3.13 ≈ **0.82 g** at 3.5 cm. Because I treated SL as TL, this probably understates mass slightly.
- **Snappit:** lists 0.5–1 g. This is a popular encyclopedia, not a measurement. *(read-level: search-summary)*
- **The disagreement, kept as found:** both estimates are 1.3–2.6x the claim's implied 0.39 g.
  - **My calculation:** if mass is 0.8 g, the required area at 2 m/s is ~41 cm² (a ~29x shortfall), break-even speed rises to ~10.8 m/s, and at 10 m/s the ratio is ~1.17 rather than ~0.6.
  - **My inference:** the claim's direction (shortfall) gets stronger at the higher mass, but its quoted "~0.6x at 10 m/s" figure would be wrong.
  - It is not refuted, because neither value is a measurement.
- **Not checked:** the 1.4 cm² silhouette. I found no measured dorsal-projection area. The figure agrees with a ~3.5 cm × ~0.4 cm laterally compressed body, but that is a plausibility check, not a check.

### C2: water-exit speed ≤ 7.6 m/s → **satisfied** (derived from measured trajectories; one direct measurement in a related small fish)

- **Hatchetfish:**
  - Soares & Bierman (2013), citing Wiest (1995), say hatchetfish trajectories reach "up to ∼1.5 body lengths in height and ∼1 body length in distance" (vertical jumps) or "up to ∼1 body length in height and ∼4 body lengths in distance" (horizontal jumps). *(read-level: full-text of Soares & Bierman; Wiest itself: could-not-access, because the Wiley host is blocked from this session)*
  - **My calculation, for a 3.5 cm fish:** a 1.5 BL rise needs a vertical exit speed of at least √(2gh) ≈ 1.0 m/s. A 4 BL range needs at least √(gR) ≈ 1.2 m/s.
  - These are lower bounds on exit speed implied by the trajectories, not measured speeds. They sit ~6x below the 7.6 m/s break-even.
- **Guppy, directly measured** (Soares & Bierman 2013, PLoS ONE 8: e61617, Table 1; read-level: full-text):
  - SL 1.85 ± 0.35 cm.
  - Max velocity in air 123.57 ± 30.0 cm/s; max in water 102.36 ± 33.75 cm/s.
  - The Discussion gives 100.16 ± 33.9 cm/s for the water value, so the paper disagrees with itself; both values are recorded here.
  - The table prints body weight as "98±10" gm. That cannot be right for a 1.85 cm fish. My inference is that it means mg, so I do not use it.
- **Other jumpers** (the same paper's review; read-level: full-text, secondary): archer fish jumps up to 1.4 m/s; Alaskan salmon take-offs ~0.5 m/s.
- **Not found:** a directly measured hatchetfish exit velocity.
  - Wiest filmed at 200 fps. A *C. strigata* study at 1000 fps was mentioned in search results, but I could not identify or retrieve it.
  - **Scope:** three web searches and one full-text paper.
- **Consequence for the claim:** at a realistic ~1–1.2 m/s, the shortfall is ~37–57x, not 14x (my calculation, at m = 0.39 g). The claim's chosen 2 m/s is generous to gliding.

### C3: ballistic aerial phase (momentum balance under gravity alone) → **satisfied** (literature)

- Wiest (1995), *J. Zool.* 236: 571–592, as quoted in search snippets: "a wide range of trajectories, all consistent with projectile motion, can be elicited." The take-off is a bilateral pectoral-fin abduction combined with a C-start. *(read-level: search-summary; the full text and abstract page could not be accessed)*
- Soares & Bierman (2013) say *C. strigata* jumpers "leave the water, moving along a ballistic aerial path, in response to startle stimuli." *(read-level: full-text)*
- Seriously Fish, citing Wiest, says the pectoral fins work during water exit but not in the air. *(read-level: search-summary; hobby source)*
- **Caveat:** "consistent with projectile motion" at 200 fps and ~1 m/s would not detect a small lift fraction. This finding agrees with the claim; it does not measure lift = 0.

### C4: axial muscle half-cycle time > 1.6 ms → **satisfied** (derived from measured contraction times)

- **What's required (my calculation):**
  - Wardle (1975) gives a stride of ~0.6–0.8 L per tail beat, read via a secondary source. Using 0.7 L and L = 3.5 cm, 7.6 m/s needs ~310 Hz tail beat, or a 1.6 ms half-cycle.
  - 10 m/s needs ~410 Hz, or 1.2 ms.
- **Measured** (all read-level: search-summary; primary papers not opened):
  - Wardle 1975 (*Nature* 255: 725–727): tail-beat frequency is limited by the twitch time of the swimming muscle, and twitch time is shorter in smaller, warmer fish.
  - Whiting, minimum twitch time: 45.8 ms at 7 °C and 33.9 ms at 12 °C.
  - Haddock: 38.8 ms and 27.6 ms at the same temperatures.
  - Fish larvae (the closest size class): C-start muscle contraction 17–21 ms at 15 °C; post-escape tail-beat 18–35 Hz.
- **Result:** the shortest locomotor contraction I found, ~17 ms, is about 10x longer than the 1.6 ms needed. The constraint is met by a wide margin.
- **Limits of this check:**
  - No measurement in a hatchetfish, and none above 20 °C. Hatchetfish live at ~24–28 °C.
  - **My calculation:** a Q10 of 2–3 from 15 to 27 °C would shorten 17 ms to ~4–7 ms, still more than twice 1.6 ms.
  - Hatchetfish exit uses the pectoral stroke as well as axial muscle, so a stride argument does not cover the pectoral contribution. C5 does.

### C5: muscle power < ~2,000 W kg⁻¹ (no route to ≥ 7.6 m/s) → **satisfied** (derived from measured muscle power)

- **What's required (my calculation):**
  - Kinetic energy at 7.6 m/s for 0.39 g is ≈ 11 mJ.
  - Constant acceleration over 1 BL (3.5 cm) takes 9.3 ms. Over 3 BL it takes 28 ms.
  - Mean power is then ~3,100 or ~1,000 W kg⁻¹ of body mass.
  - Per kg of muscle that is ~2,000–6,200 W kg⁻¹ if half the body is muscle, or ~4,100–12,300 W kg⁻¹ if only the pectoral muscle (≤ ~25% of body mass) does the work.
  - Water drag is ignored, so these are lower bounds.
- **Measured:**
  - Wakeling & Johnston (1998), *J. Exp. Biol.* 201: 1505–1526: fast myotomal fibres of "*Sc. notata*" (abbreviated in the snippet; I could not expand it, so I give no full binomial) produced a mean muscle-mass-specific power of **142.7 W kg⁻¹ at 20 °C** in work loops at in-vivo-like strains. *(read-level: search-summary of the abstract)*
  - The same snippet says power *declined* at cycle frequencies simulating a C-start (15 Hz). If anything, fast-start power is below the peak.
  - Other teleost fast-fibre work-loop values found: ~20–35 W kg⁻¹ at 4 °C; 27.5 W kg⁻¹ in a 10 cm cod; ~80 W kg⁻¹ quoted as a typical teleost maximum. *(read-level: search-summary)*
  - Muscle mass fraction: "up to a quarter of body weight" for the pectoral musculature. *(read-level: search-summary, Wikipedia mirror)*
- **Result:** the highest fish muscle power I found (142.7 W kg⁻¹) is roughly 14–90x short of the requirement. The claim's escape clause cannot be reached with muscle power alone.
- **Not checked:** an elastic power-amplification (catapult) mechanism in hatchetfish take-off. I did not search for one. A catapult would loosen C5 but not C4's tail-beat route. **C5 is satisfied on the assumption that there is no such store.**

## 3. Verdict

- **No constraint is unsatisfiable.** No measured number contradicts claim 283 from below.
- **C2–C5 are satisfied, mostly by calculation from measured inputs.** The organism and tissue scales back the claim's direction (silhouette lift is far too small at real launch speeds).
  - Real launch speeds (~1–1.2 m/s from hatchetfish trajectories and ~1.0–1.2 m/s measured in guppy) mean the claim's 2 m/s case understates the shortfall.
  - The 10 m/s escape clause is closed at the tissue scale by both muscle timing and muscle power.
- **C1 is open, with disagreement:** the mass the claim implies (0.39 g) is 1.3–2.6x below the available estimates (0.5–1 g; ~0.82 g from FishBase L–W).
  - If the estimates are right, the "~0.6x at 10 m/s" figure should be ~1.2x and the 2 m/s shortfall ~29x.
  - The qualitative claim survives; the quoted numbers would need revising.
- **Biggest gaps:**
  - The organism identity is inferred.
  - Wiest 1995 was not readable here (Wiley host blocked; sciencegate.app also blocked).
  - No direct hatchetfish exit velocity or body mass was found.

## Sources

| Source | Used for | Read-level |
|---|---|---|
| Soares D, Bierman HS (2013) Aerial jumping in the Trinidadian guppy (*Poecilia reticulata*). PLoS ONE 8(4): e61617. doi:10.1371/journal.pone.0061617 | C2, C3 | full-text |
| Wiest FC (1995) The specialized locomotory apparatus of the freshwater hatchetfish family Gasteropelecidae. J. Zool. 236: 571–592 | C2, C3 | search-summary (could-not-access full text) |
| Wardle CS (1975) Limit of fish swimming speed. Nature 255: 725–727 | C4 | search-summary (paywalled) |
| Lateral-muscle twitch-time studies of whiting, haddock and fish larvae (as returned by search; primary papers not opened) | C4 | search-summary |
| Wakeling JM, Johnston IA (1998) Muscle power output limits fast-start performance in fish. J. Exp. Biol. 201: 1505–1526 | C5 | search-summary |
| FishBase species summary, *Carnegiella strigata* | C1 | search-summary |
| Snappit, *Carnegiella strigata* | C1 | search-summary |
| Wikipedia mirror, Gasteropelecidae (pectoral muscle fraction) | C5 | search-summary |

```swarm-entail
{"source_claim": 283, "source_scale": "organ",
  "constraints": [
    {"target_scale": "organism", "kind": "range",
      "statement": "Organism body mass must match, within ~2x, the mass implied by the organ-scale lift arithmetic (L = 0.5*rho*v^2*S*CL at 2 m/s, CL 0.8, 20 cm2)",
      "quantity": "body mass", "lo": 0.2, "hi": 0.8, "units": "g",
      "status": "open",
      "satisfied_by": "No measured mass found. Estimates disagree with the implied 0.39 g: FishBase Bayesian length-weight (a=0.01622, b=3.13) gives ~0.82 g at 3.5 cm (my calculation); Snappit lists 0.5-1 g.",
      "satisfied_evidence": "unknown",
      "note": "Organism identity (Gasteropelecidae, Carnegiella, ~3.5 cm SL) is inferred; the repo does not name it. Searched: one web search on Carnegiella strigata mass plus FishBase (search-summary). At 0.8 g the 2 m/s shortfall becomes ~29x and the 10 m/s ratio ~1.2x, not ~0.6x (calculated). The 1.4 cm2 silhouette was not checked against a measurement."},
    {"target_scale": "organism", "kind": "range",
      "statement": "Measured water-exit speeds must lie well below the speed at which the dorsal silhouette alone could support body weight",
      "quantity": "water-exit (launch) speed", "lo": null, "hi": 7.6, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Hatchetfish trajectories (<=1.5 BL height, <=4 BL range; Wiest 1995 via Soares & Bierman 2013) imply exit speeds of ~1.0-1.2 m/s (calculated lower bounds). Guppy measured max 1.24 m/s in air, 1.02 m/s in water.",
      "satisfied_evidence": "derived",
      "note": "Soares & Bierman 2013 PLoS ONE 8:e61617 (full-text); Wiest 1995 J Zool 236:571-592 (could-not-access, cited secondarily). The paper's water speed differs between Table 1 (102.36) and Discussion (100.16 cm/s). No direct hatchetfish exit velocity found; scope: three web searches and one full-text paper."},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "The aerial phase must obey vertical momentum balance under gravity alone (ballistic), with no detectable sustained aerodynamic lift",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Wiest 1995: trajectories 'all consistent with projectile motion'; Soares & Bierman 2013: Carnegiella strigata 'moving along a ballistic aerial path'",
      "satisfied_evidence": "literature",
      "note": "Wiest 1995 (search-summary; full text inaccessible because the Wiley host is blocked); Soares & Bierman 2013 (full-text). 'Consistent with projectile motion' at 200 fps does not exclude a small lift fraction."},
    {"target_scale": "tissue", "kind": "timescale",
      "statement": "Axial locomotor muscle minimum contraction (half-cycle) time must exceed the time needed to drive tail-beat propulsion to the silhouette break-even speed, so the 7.6-10 m/s escape route is closed",
      "quantity": "locomotor muscle half-cycle / twitch time", "lo": 1.6, "hi": null, "units": "ms",
      "status": "satisfied",
      "satisfied_by": "Shortest locomotor contraction found: fish larvae C-start 17-21 ms at 15 C (tail beat 18-35 Hz); whiting 33.9 ms and haddock 27.6 ms at 12 C. Required: ~1.6 ms (7.6 m/s) to 1.2 ms (10 m/s), calculated with a stride of 0.7 L and L = 3.5 cm.",
      "satisfied_evidence": "derived",
      "note": "Wardle 1975 Nature 255:725-727 and twitch-time studies, all read at search-summary level. No hatchetfish or >20 C measurement; a Q10 of 2-3 to 27 C still gives ~4-7 ms (calculated). Does not cover pectoral-stroke propulsion (see energetic constraint)."},
    {"target_scale": "tissue", "kind": "energetic",
      "statement": "Mass-specific muscle power must be insufficient to accelerate the body to the silhouette break-even speed within the 1-3 body lengths available before water exit",
      "quantity": "muscle-mass-specific power available", "lo": null, "hi": 2000, "units": "W/kg muscle",
      "status": "satisfied",
      "satisfied_by": "Highest fish fast-muscle power found: 142.7 W/kg at 20 C (work loops). Requirement ~2,000-12,300 W/kg muscle (calculated, drag ignored, 0.39 g, 7.6 m/s, 25-50% muscle fraction).",
      "satisfied_evidence": "derived",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505-1526 (search-summary of abstract); other teleost values 20-80 W/kg (search-summary). Did not search for an elastic power-amplification (catapult) mechanism in hatchetfish take-off; this result assumes there is none."}
  ]}
```
