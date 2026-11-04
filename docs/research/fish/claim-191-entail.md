# Claim 191: what must be true at the organ and behaviour scales

**Source claim (organism scale, evidence: derived):**
> At the measured maximum burst of 1.38 m/s the ballistic leap is 19.4 cm and the wing lengthens it by only +1.5 to +3.0% (3-6 mm); at 0.45 m/s the gain is ~0%

**Adjacent scales checked:** organ, behaviour.

## 0. What I could and could not pin down first

- **The species is not stated in the claim, and claim 191 is not recorded anywhere in this repository.** I searched the repo for the claim text, "191", "leap", "ballistic", "hatchet" and "pectoral". None of these turned up the claim or its parent analysis. So I do not know the taxon, body length, mass, fin area, or where the 1.38 m/s was measured (in water or in air).
- **The best-matching published system is the freshwater hatchetfishes (Gasteropelecidae).** This is my inference, not a stated fact. They are small fish that make ballistic aerial escapes with enlarged pectoral fins (Kapoor et al. 2026; Wiest 1995). Every check below that uses gasteropelecid data is **conditional on that taxon assumption**, and says so.
- **The 19.4 cm figure is exactly the drag-free range at a 45° launch, v²/g.** At 1.38 m/s, 1.38² / 9.81 = 0.1941 m. That is my calculation. So the claim's number implies a 45° launch, take-off and landing at the same height, and negligible drag.
- **Network limits on this session.** Wiley (`zslpublications.onlinelibrary.wiley.com`), ResearchGate, Semantic Scholar, the St Andrews repository and OUP full text could not be reached. Wiest (1995) is therefore known to me only at second hand. PubMed E-utilities and PMC were reachable.

## 1. Constraints (ENTAIL)

| # | Scale | Kind | Requirement (generic) | Bound |
|---|---|---|---|---|
| C1 | behaviour | range | The air-phase launch speed must equal the "maximum burst" speed. The range is v²/g only if the speed when the fish leaves the water is 1.38 m/s, with no gain or loss at water exit. | launch speed in [1.38, 1.38] m/s; with a ±5% tolerance, [1.31, 1.45] m/s |
| C2 | behaviour | range | The launch angle must be near 45°. Reaching ≥94% of v²/g needs sin 2θ ≥ 0.94. | θ in [35, 55]° |
| C3 | behaviour | timescale | The lifting surface must be deployed by water exit and held for the whole aerial phase. The aerial phase lasts 2v·sinθ/g = 0.199 s at 1.38 m/s and 0.065 s at 0.45 m/s (calculated). Deployment must be fast relative to that. | fin-spread onset ≤ 0 s relative to exit; held ≥ 0.2 s |
| C4 | organ | range | Effective wing loading (W/S)/C_L must make the lift-to-weight ratio large enough for +1.5–3% range at 1.38 m/s. That is about 13–27 Pa (derived, below). The same number must also give ~0% gain at 0.45 m/s. | (W/S)/C_L in [13, 27] Pa |
| C5 | organ | energetic | The propulsive muscle must supply ½v² = 0.95 J per kg of body mass in kinetic energy (calculated), within one fast-start, plus hydrodynamic losses. | ≥ 0.95 J/kg body (lower bound only) |

### Derivation of the C4 bound (calculated, not observed)

I used a point-mass model: no drag, a 45° launch, landing at launch height, and lift L = ½ρv²SC_L perpendicular to the velocity, with ρ_air = 1.2 kg/m³. I integrated it numerically (script kept in the session scratchpad, not committed).

| (W/S)/C_L (Pa) | gain at 1.38 m/s | gain at 0.45 m/s |
|---|---|---|
| 10 | +3.98% | +0.43% |
| 20 | +2.03% | +0.21% |
| 30 | +1.37% | +0.15% |
| 40 | +1.03% | +0.11% |

- **Range for the claimed gain:** +3.0% corresponds to about 13 Pa and +1.5% to about 27 Pa (interpolated).
- **The low-speed half of the claim is consistent:** lift-to-weight scales with v², and (0.45/1.38)² = 0.11. So "~0% at 0.45 m/s" follows automatically (≤0.3% in this model) once the high-speed gain is fixed.
- **Caveat:** the claim's own model is unknown to me. This is my model, and its bound can be no better than its assumptions.
- **What the bound means physically:** 27 Pa with C_L ≤ ~1 needs S/m ≥ g/27 ≈ 36 cm² of lifting area per gram of fish. That is a strong morphological requirement for a fish with a ~5 cm body.

## 2. Checks

### C1: launch speed equals burst speed. **open** (with a flagged tension)

- **Small fish do reach this speed (measured):**
  - Guppies, *Poecilia reticulata*, standard length 1.85 ± 0.35 cm, reached a maximum velocity of 102.36 ± 33.75 cm/s in water and 123.57 ± 30.0 cm/s in air. One example jump reached 128 cm/s in water and 150 cm/s in air (Soares & Bierman 2013; read-level: full-text, via an automated page summary). The same paper's Discussion gives 100.16 ± 33.9 cm/s for water; the paper disagrees with itself on this point.
  - The same paper cites Shih & Techet (2010) for archer fish reaching "velocities of up to 1.4 m/sec" (read-level for Shih & Techet 2010: listing, cited second-hand).
- **Tension 1: in-air speed can exceed in-water speed.** In the guppy data, the in-air maximum exceeds the in-water maximum by about 21%. Those are the authors' numbers; the ratio is my calculation. If the claim's 1.38 m/s is an in-water burst, launch speed may not equal it, and the ballistic range could be larger (range ∝ v²). So equating burst speed with launch speed is an assumption that measured data in another species do not support.
- **Tension 2: hatchetfish jump much faster than 1.38 m/s in body-length terms.** Kapoor et al. (2026) report that *Gasteropelecus maculatus* and *Thoracocharax stellatus* "jumped at remarkable speeds (mean: 56 ± 14 BL/s)" (read-level: abstract). If the claim's organism were a gasteropelecid with body length ≥ 2.5 cm, the *mean* jump speed would be ≥ 1.4 m/s. That would make 1.38 m/s an implausible *maximum* (my inference).
- **Why this is not marked unsatisfiable:** I do not know the claim's species or body length, and the abstract does not give the body lengths used. No measured number directly contradicts 1.38 m/s for the claim's organism.
- **What would settle it:** the claim's taxon and body length, plus whether 1.38 m/s was measured in water or in air.

### C2: launch angle near 45°. **satisfied** (conditional on taxon; derived from reported values)

- **The behaviour exists:** Wiest (1995) describes two hatchetfish trajectory types. Vertical jumps reach about 1.5 body lengths high and 1 body length far. Horizontal jumps reach about 1 body length high and 4 body lengths far.
- **Read-level:** I have this only as Soares & Bierman's (2013) summary of Wiest (full-text of the citing paper; Wiest itself could-not-access). Wiest's abstract, at search-summary level, says the trajectories are "all consistent with projectile motion."
- **The angle (my inference):** for a ballistic arc, R/H = 4/tanθ. The horizontal jump type's R/H ≈ 4 gives θ ≈ 45°. The vertical type gives θ ≈ 80°. So the 45° launch the claim needs is within the repertoire of gasteropelecids, but it is one of two modes and not the only one.
- **Contrast:** in guppies the head-to-water "angle of attack" was 77.4 ± 24.91° (Soares & Bierman 2013). That is a body angle, not a trajectory angle, in a different family.

### C3: fin deployed by exit and held through the aerial phase. **satisfied** for deployment; hold duration **not verified**

- **Deployment before exit:** Wiest (1995) describes a stereotyped take-off of "a bilateral pectoral fin abduction and a C-start." The fins are moved forward, likely to open the fin surface fully, before downward motion begins (read-level: search-summary of the abstract; full text could-not-access).
- **Not checked:** I found no measurement of how long the fins stay spread during the ~0.2 s aerial phase. If they fold early, the realised gain would be below the claim's figure.

### C4: effective wing loading 13–27 Pa. **open**

- **Searched:**
  - PubMed: "hatchetfish Gasteropelecidae" (4 hits), "Gasteropelecus flight" (1 hit), "fish jumping out of water kinematics" (5 hits), "Park Choi 2010 aerodynamic flying fish" (1 hit).
  - Web: hatchetfish take-off and jump kinematics.
- **Found:** no measured pectoral fin area, body mass, wing loading or lift coefficient for any gasteropelecid.
- **Closest data, different family:** Park & Choi (2010) measured lift on flying fish models (*Cypselurus hiraii*, Exocoetidae). Lift coefficient was largest at attack angles around 30–35° (read-level: abstract). I did not get the numerical C_L, so I cannot use it to bound C4.
- **Scope of the negative:** this is "nobody I could reach has reported the number," not "people measured it and it fails."
- **What would settle it:** fin area and body mass of the claim's organism. A rough plausibility concern stands (my inference): ≥36 cm²/g of lifting area is a lot for a small fish. If the measured wing loading came out far above 27 Pa, the +1.5–3% figure would be too high, and the claim would be refuted from below.
- **Disagreement on the fin's role, preserved:**
  - Brousseau (1976; read-level: abstract) describes *Gasteropelecus sternicla* pectoral anatomy as "specialized for self-propelled, aerial flight," with "massive ventral flight muscles."
  - Wiest (1995; read-level: search-summary) concludes that "active flight in the gasteropelecids is unlikely."
  - The claim's small, passive-lift gain is closer to Wiest's reading. If Brousseau's powered-flapping reading were right, the fins would do work in the air, and a passive lift model like the claim's (or mine) would be the wrong model.

### C5: ≥ 0.95 J/kg of kinetic energy from one fast-start. **satisfied** (measured existence; the energy figure is calculated)

- **Muscle power (measured):** Wakeling & Johnston (1998) measured fast myotomal fibres of *Scorpaena notata* producing "a mean muscle-mass-specific power of 142.7 W kg⁻¹ at 20 °C." Power output predicted from swimming sequences matched the work-loop measurements (read-level: abstract).
- **Time needed (my inference):** at that power, 0.95 J/kg is delivered in about 7 ms per kg of muscle. Even at a muscle mass fraction well below 1 (not known for the claim's organism) and with losses, this fits within a fast-start of a few tens of ms. The guppy fast-start bend lasted 7.8 ± 0.5 ms (Soares & Bierman 2013), on the same timescale.
- **Direct evidence that the energy is available:** small fish reach ≥1.38 m/s in jumps (C1 data), and hatchetfish reach 56 ± 14 BL/s (Kapoor et al. 2026). Those speeds would be impossible if the energy were not available.
- **Limits of the check:** this satisfies only the lower bound. It says nothing about the claim's specific species.

## 3. Summary

- **No constraint is unsatisfiable on the evidence I could reach.** No measured value directly contradicts any requirement for the claim's organism, mainly because that organism is not identified.
- **Two things put the claim at risk:**
  1. **C1:** the claim equates burst speed with launch speed. Guppy data (air > water by ~21%) and hatchetfish speed data (56 ± 14 BL/s) both sit uneasily with a 1.38 m/s "maximum" defining the leap.
  2. **C4:** the claimed +1.5–3% gain needs an effective wing loading of about 13–27 Pa (my model). No gasteropelecid fin area or mass was found to test it.
- **Next step:** identify the claim's taxon, body length and fin area. C1 and C4 can then be decided with no simulation.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| Soares D, Bierman HS (2013) Aerial jumping in the Trinidadian guppy (*Poecilia reticulata*). PLoS ONE 8:e61617. PMC3629028 | full-text (automated page summary) | C1, C2, C5; second-hand Wiest 1995 and Shih & Techet 2010 |
| Wiest FC (1995) The specialized locomotory apparatus of the freshwater hatchetfish family Gasteropelecidae. J Zool 236:571–592 | search-summary (full text could-not-access: Wiley/ResearchGate/Semantic Scholar blocked) | C2, C3, C4 disagreement |
| Kapoor H et al. (2026) Mechanosensory stimuli, rather than ambient light, shapes freshwater hatchetfish aerial escapes. Integr Comp Biol 66:icag131. PMID 42496600 | abstract | C1 tension, C5 |
| Brousseau RA (1976) The pectoral anatomy of selected Ostariophysi. I. The Characiniformes. J Morphol 148:89–135. PMID 1246081 | abstract | C4 disagreement |
| Wakeling JM, Johnston IA (1998) Muscle power output limits fast-start performance in fish. J Exp Biol 201:1505–1526. PMID 9556535 | abstract | C5 |
| Park H, Choi H (2010) Aerodynamic characteristics of flying fish in gliding flight. J Exp Biol 213:3269–3279. PMID 20833919 | abstract | C4 (closest-family context only) |
| Shih AM, Mendelson L, Techet AH (2017) Archer fish jumping prey capture: kinematics and hydrodynamics. J Exp Biol 220:1411–1422. PMID 28424312 | abstract | C1 context (ballistic aerial phase; energy balance) |
| Shih & Techet (2010), archer fish up to 1.4 m/s | listing (cited inside Soares & Bierman 2013; not read) | C1 |

```swarm-entail
{"source_claim": 191, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The speed at water exit (initial air-phase speed) must equal the stated maximum burst speed, since the 19.4 cm range is exactly v^2/g; no speed gain or loss at the water surface",
      "quantity": "air-phase launch speed", "lo": 1.31, "hi": 1.45, "units": "m/s",
      "status": "open",
      "satisfied_by": "Speed is attainable by small fish (guppy in-air max 123.57 +/- 30.0 cm/s; archer fish up to 1.4 m/s), but guppy in-air max exceeds in-water max by ~21%, and hatchetfish jump at 56 +/- 14 BL/s, which for any BL >= 2.5 cm puts the mean above 1.38 m/s. Claim taxon and body length unknown, so not decidable.",
      "satisfied_evidence": "measured",
      "note": "Soares & Bierman 2013 PLoS ONE (full-text); Kapoor et al. 2026 Integr Comp Biol PMID 42496600 (abstract; body lengths not given); Shih & Techet 2010 (listing, second-hand). Tension, not contradiction: claim's species not identified anywhere in repo."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The launch trajectory angle must lie near 45 degrees for the ballistic range to reach >=94% of v^2/g",
      "quantity": "launch angle", "lo": 35, "hi": 55, "units": "deg",
      "status": "satisfied",
      "satisfied_by": "Hatchetfish 'horizontal' jumps reach ~1 BL high and ~4 BL far, which for a ballistic arc (R/H = 4/tan theta) implies theta ~45 deg (my derivation); a second 'vertical' mode (~80 deg) also exists. Conditional on the organism being a gasteropelecid.",
      "satisfied_evidence": "derived",
      "note": "Wiest 1995 J Zool 236:571-592 as summarised in Soares & Bierman 2013 (full-text of citing paper; Wiest itself search-summary only)."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "The lifting surface must be deployed no later than water exit and held spread for the whole aerial phase (~0.2 s at 1.38 m/s, calculated)",
      "quantity": "fin-spread onset relative to exit; hold duration", "lo": 0.2, "hi": null, "units": "s (hold duration)",
      "status": "satisfied",
      "satisfied_by": "Bilateral pectoral fin abduction is a stereotyped component of hatchetfish take-off, occurring before the downward C-start motion. Hold duration through the aerial phase was NOT verified.",
      "satisfied_evidence": "literature",
      "note": "Wiest 1995 (search-summary of abstract; full text could-not-access). Satisfied for deployment only; hold duration open."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Effective wing loading (weight per lifting area, divided by lift coefficient) must be low enough that air-phase lift gives +1.5 to +3% range at 1.38 m/s and ~0% at 0.45 m/s",
      "quantity": "(W/S)/C_L", "lo": 13, "hi": 27, "units": "Pa",
      "status": "open",
      "satisfied_by": "No measured pectoral fin area, body mass, wing loading or lift coefficient found for any gasteropelecid. Bound itself is from my point-mass simulation, not the claim's model.",
      "satisfied_evidence": "unknown",
      "note": "Searched PubMed ('hatchetfish Gasteropelecidae', 'Gasteropelecus flight', 'fish jumping out of water kinematics', 'Park Choi 2010 aerodynamic flying fish') and web (hatchetfish take-off kinematics). Not-reported, not measured-and-failed. Park & Choi 2010 (Exocoetidae, abstract) gives max C_L at 30-35 deg attack but no number read. Disagreement preserved: Brousseau 1976 (abstract) calls the fins specialised for self-propelled flight; Wiest 1995 says active flight unlikely."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The propulsive musculature must deliver at least the launch kinetic energy, 0.5 v^2 = 0.95 J per kg body mass, within a single fast-start, plus hydrodynamic losses",
      "quantity": "specific launch kinetic energy", "lo": 0.95, "hi": null, "units": "J/kg body",
      "status": "satisfied",
      "satisfied_by": "Fast myotomal fibres deliver 142.7 W/kg muscle (Scorpaena notata, 20 C, work-loop). That is ~7 ms per kg of muscle for 0.95 J (my calculation). Small fish are measured jumping at >=1.38 m/s, which is direct evidence the energy is available.",
      "satisfied_evidence": "measured",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505 PMID 9556535 (abstract); Soares & Bierman 2013 (full-text); Kapoor et al. 2026 (abstract). Lower bound only; species-specific muscle fraction unknown."}
  ]}
```
