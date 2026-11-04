# Claim 269 — entailment to adjacent scales (organ, behaviour)

**Source claim (organism scale, evidence: derived):**
> THE TAXI STALLS at 2.19–2.88 m/s, 50–65% of the 4.41 m/s glide speed, after ~30–38 strokes over
> 1.5–2 m. It does not fail to accelerate; it accelerates to a ceiling below what is needed.

I read this as being about flying fish (Exocoetidae). The surface "taxi", where only the hypocaudal
(lower) tail lobe stays in the water, is the behaviour the literature means by that word. The repository
has no earlier fish documents (`docs/research/fish/` did not exist), so I don't know the body size,
species or model that produced the claim's numbers. That gap matters for constraint B1 below.

**Overall result:** One constraint is **unsatisfiable**. Reported field speeds for adult flying fish are
3–5× the claim's absolute numbers. That holds only if the claim is about adult field fish. Two constraints
are **satisfied**. Two are **unsatisfied**, and the available evidence leans against one of those two (the
energetic one), though not through a measured number.

---

## Sources and read-levels

| Source | What was used | Read-level |
|---|---|---|
| Deng J., Wang S., Zhang L., Mao X. (2019) *Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation.* bioRxiv 10.1101/765560 | CFD powers and speeds; its citations of Davenport, Hertel, Franzisket, Hubbs and Wardle | full-text (through an automated fetch-and-extract tool; numbers quoted from that extraction, not read line by line) |
| Davenport J. (1994) *How and why do flying fish fly?* Rev. Fish Biol. Fish. 4:184–214, doi:10.1007/BF00044128 | "tail beating in the water at up to 50 beats s⁻¹"; taxiing "to reach take-off speed" | search-summary (abstract snippet). link.springer.com is blocked from this session. Its other numbers are known only as cited by Deng et al. |
| Hertel H. (1966) | ~50 beats s⁻¹ in warm (~25 °C Caribbean) water | could-not-access; known only as cited by Deng et al. |
| Franzisket L. (1965) | 400 m in 30 s by repeated taxi + flight | could-not-access; known only as cited by Deng et al. |
| Makiguchi Y. et al. (2013) Aquat. Biol. 18:105–111 | stroke frequency 21.2 ± 4.6 Hz at take-off; take-off speeds 3.9–5.2 m/s estimated from acceleration loggers in a lab tank | search-summary (abstract snippet). int-res.com is blocked from this session. |
| APS March Meeting 2024, session S27.13, *Flying fish taxiing on the water's surface* | taxi tail-slap frequency 13.5 Hz; ~2 N minimum force for a 200 g fish | search-summary only. The host is blocked from this session. Authors unknown. Conference abstract. |
| Wardle C.S. (1975) Nature 255:725 *Limit of fish swimming speed* | stride frequency limited by muscle contraction time; minimum contraction time ≈ 0.025 s for L = 0.3 m at 20 °C | search-summary; the 0.025 s value comes from Deng et al.'s reading of Wardle's curve (secondary) |
| Bainbridge R. (1958) J. Exp. Biol. 35:109–133 | stride 0.6–0.8 body lengths per beat (dace, trout, goldfish) | search-summary, through a secondary citation in Wardle 1975 |
| Edgerton H.E. & Breder C.M. (1941) Zoologica 26:311–314 | photographs of the taxi phase, with taxi resumed and flight continued | search-summary |
| Park H. & Choi H. (2010) J. Exp. Biol. 213:3269–3279 | wind-tunnel lift-to-drag on stuffed specimens; the "70 km/h" glide speed appears only in press releases | search-summary |

Blocked hosts (they need allowing in the session network settings before the primary texts can be read):
int-res.com, link.springer.com, archive.org, researchgate.net, meetings-archive.aps.org. The nature.com
article page is paywalled.

---

## Quantities derived from the claim itself (calculated, not observed)

All of these are my arithmetic on the claim's own numbers:

- **Advance per stroke**: λ = distance / strokes = 1.5 m / 38 to 2 m / 30 = **0.039–0.067 m per stroke**.
- **Tail-beat frequency implied**: I assume speed rises monotonically and with a concave profile toward the
  ceiling, which is what "accelerates to a ceiling" describes. Under that assumption the mean speed is at
  least half the ceiling. That bounds mean speed to [1.10, 2.88] m/s, bout duration to [0.52, 1.83] s, and
  **f ∈ [16.4, 73] Hz**. If the profile is different (for example a late sprint), the lower bound moves.
- **Muscle contraction time implied**: T = 1/(2f), so **T ∈ [6.8, 30.5] ms**.
- **Stride ratio**: λ/L = 0.13–0.27 for L = 0.25–0.30 m. These lengths are the Deng et al. model fish and
  Davenport's fish. The claim's own body length is unknown.
- **Power ratio**: I scaled Deng et al.'s **simulated** 36 W at 10 m/s (steady taxi, 0.191 kg model fish)
  by U³. That gives about 0.38 W at 2.19 m/s, 0.86 W at 2.88 m/s and 3.1 W at 4.41 m/s. This extrapolates
  a simulation. It is not a measurement, and U³ scaling is a crude assumption at the free surface.

---

## Constraints

### B1 — behaviour · range — taxi terminal speed (absolute), [2.19, 2.88] m/s, below take-off speed
**Requirement:** For the claim to hold, the terminal speed of a surface taxi bout in the organism must
lie in [2.19, 2.88] m/s. The animal must also be unable to taxi up to the speed it needs to stay airborne.

**Status: unsatisfiable (conditional on the claim being about adult field flying fish).**

- *Measured value that contradicts it:* Franzisket (1965), as cited by Deng et al. (2019, full-text),
  reports a total flight of **400 m in 30 s through repeated taxiing and flight**. My arithmetic puts the
  mean speed over that whole sequence at **13.3 m/s**. That is 4.6× the claim's taxi ceiling and 3× its
  glide speed. Over a 30 s sequence with repeated taxi bouts, each later glide starts from the speed the
  taxi delivered. A mean of 13.3 m/s therefore can't be reached if each taxi stalls at ≤ 2.88 m/s. This
  is my inference from the reported number, not the author's claim.
- *Further reported values, all against the claim:*
  - Davenport (1994), as cited by Deng et al., reports a peak glide speed of about 15–20 m/s.
  - Davenport's abstract (search-summary) says the fish "accelerate to take-off speed by taxiing". That
    statement is qualitative but directly opposes "a ceiling below what is needed".
  - Edgerton & Breder (1941, search-summary) photographed taxi bouts that were followed by continued
    flight.
- *Disagreement I'm keeping, not averaging away:* Makiguchi et al. (2013, search-summary) estimated
  take-off speeds of **3.9–5.2 m/s** from accelerometer loggers in a lab tank. Those speeds bracket the
  claim's 4.41 m/s glide speed. The authors themselves say this is 39–52% of earlier film-measured maximum
  swimming speeds, and suggest the fish held back in the confined tank. Another source in the search
  results says the loggers may have changed the fish's locomotion. The claim's numbers may come from this
  lab regime or from a smaller animal.
- *Scope and weak points:* The contradicting record is a 1965 field observation. I couldn't access the
  primary paper, so its measurement method is unknown to me. If the claim's model fish is small, or
  parameterised to tank conditions, B1 drops to "open" for that regime. For adult open-ocean flying fish,
  the claim's absolute speeds are contradicted by reported field values.

### B2 — behaviour · timescale — taxi tail-beat frequency, [16.4, 73] Hz
**Requirement:** 30–38 strokes over 1.5–2 m at the claim's speeds require a tail-beat frequency of about
16–73 Hz (derived above).

**Status: satisfied, with a conflicting measurement kept below.**

- *Satisfied by:*
  - Hertel (1966), as cited by Deng et al.: about **50 beats s⁻¹** at ~25 °C.
  - Davenport (1994): "**up to 50 beats s⁻¹**" in the abstract (search-summary); Deng et al. cite it as
    50–70 strokes s⁻¹.
  - Makiguchi et al. (2013): 21.2 ± 4.6 Hz. This was measured at take-off, not during a taxi.
- *Conflicting:* The APS 2024 abstract (search-summary only, conference abstract, authors unknown)
  reports **13.5 Hz** for taxi tail-slapping. That is below the derived floor of 16.4 Hz. I don't treat
  it as making B2 unsatisfiable, for two reasons. The floor depends on my assumption about the speed
  profile. And I couldn't read the abstract's species, size or temperature. If 13.5 Hz turns out to be
  the general taxi rate, the claim's stroke count and distance can't both hold together with its speeds.
- *Inference:* The claim is internally consistent with a ~50 Hz taxi, since 50 Hz × 0.039–0.067 m gives
  2.0–3.4 m/s. Field fish beating at ~50 Hz while reaching ≥ 10 m/s, however, implies an advance of
  ≥ 0.2 m per beat. The claim's short stride is what produces its low ceiling. See O1.

### O1 — organ · spatial — advance per hypocaudal-lobe stroke, [0.039, 0.067] m (λ/L ≈ 0.13–0.27)
**Requirement:** The caudal propulsor working in surface-piercing mode must advance the body only
0.039–0.067 m per beat. For a 0.25–0.30 m fish that is 0.13–0.27 body lengths per beat.

**Status: unsatisfied. Nobody I could find has measured it, which is different from people looking and
finding nothing.**

- I searched for paired measurements of taxi speed and tail-beat frequency in the same bout, which is
  what you need to get stride length. I searched under "taxiing tail beat frequency speed", "taxiing
  duration distance video kinematics", Makiguchi 2013, Edgerton & Breder 1941 and the APS 2024 abstract.
  None of them gave a paired value.
- The nearest data come from a different mode. Fully submerged steady swimming in dace, trout and
  goldfish gives 0.6–0.8 L per beat (Bainbridge 1958, via Wardle 1975, search-summary). Deng et al. use
  Y = 0.8 for flying fish. The claim's 0.13–0.27 L is 2–6× shorter. That is physically plausible for a
  lobe that is only partly submerged, but nothing measured confirms it.
- If you combine Hertel's ~50 Hz with Davenport's 10–20 m/s, you get ~0.2–0.4 m per beat. That figure
  comes from two separate reports, not from one bout, so I don't use it as a measured contradiction.

### O2 — organ · energetic — power from the axial or caudal musculature, ~0.4–3.1 W ceiling for a 0.19 kg fish
**Requirement:** For the taxi to plateau at 2.19–2.88 m/s and stay below 4.41 m/s, the sustained power
the caudal musculature can deliver in taxi mode must lie between the power needed at the ceiling and the
power needed at 4.41 m/s. Using Deng et al.'s simulation scaled by U³ (derived), that window is about
0.38–3.1 W, or 2–16 W/kg body mass.

**Status: unsatisfied. The evidence leans against it, but only through a simulation, so I haven't marked
it unsatisfiable.**

- I found no measured mechanical power output for flying fish muscle. I searched the sources above;
  Deng et al. cite only Gao & Techet (2011) for a required density of ~2300 W/kg, which is a required
  value, not a measured one.
- Against the claim: Makiguchi et al. (2013) derived underwater exit speeds of 3.9–5.2 m/s, and Davenport
  (1994, via Deng) reports underwater speeds up to 10 m/s. In Deng et al.'s **simulation**, swimming
  submerged needs about 10× more power than taxiing at the same speed (350 W versus 36 W at 10 m/s). If
  that ratio holds, a fish that can swim submerged at ≥ 3.9 m/s has more than enough power to taxi at
  4.41 m/s. This is my inference. It joins a value derived from measurements to a simulated ratio, so it
  doesn't reach the measured-contradiction standard for unsatisfiable. A measured taxi power, or measured
  exocoetid muscle power, would settle it.

### O3 — organ · timescale — fast-muscle contraction time, T ∈ [6.8, 30.5] ms
**Requirement:** For the tail-beat frequencies in B2 to be reachable, the axial fast muscle must complete
contraction cycles in 6.8–30.5 ms (T = 1/2f).

**Status: satisfied, with an extrapolation from other species flagged.**

- Wardle (1975) relates the maximum stride frequency to muscle contraction time. Deng et al. read his
  curve as giving a minimum contraction time of **≈ 0.025 s for L = 0.3 m at 20 °C** (search-summary of
  Wardle; value via Deng, secondary). 25 ms ≤ 30.5 ms, so the claim's lowest required frequency (about
  16.4 Hz; ≤ 20 Hz at 25 ms) is kinetically reachable. Contraction time shortens at higher temperature.
- *Scope:* Wardle's relation comes from other teleosts, not exocoetids. I found no direct measurement
  of flying fish muscle contraction kinetics.
- *Disagreement kept:* By the same relation, Hertel's ~50 Hz would need T ≈ 10 ms. Deng et al. compute
  T = 0.012 s to reach 10 m/s and note that this is about half of Wardle's 20 °C value. So the field
  frequencies themselves are under strain from Wardle's relation. The claim's lower-frequency regime is
  not.

---

## Summary

| ID | Scale | Kind | Status |
|---|---|---|---|
| B1 | behaviour | range | **unsatisfiable**: field record of 400 m in 30 s, mean 13.3 m/s (Franzisket 1965, as cited by Deng et al.); conditional on adult field fish |
| B2 | behaviour | timescale | satisfied: ~50 Hz (Hertel 1966; Davenport 1994); conflicts with 13.5 Hz (APS 2024) |
| O1 | organ | spatial | unsatisfied: no paired taxi speed and frequency measurement found |
| O2 | organ | energetic | unsatisfied: no measured muscle power; simulated evidence leans against |
| O3 | organ | timescale | satisfied: Wardle 1975 contraction-time relation (other species) |

**What would change this:**
- Reading Franzisket 1965 and Hertel 1966 in the original, to confirm the method behind the record.
- Stating the body length and conditions behind claim 269. If it models a tank-confined or small fish,
  B1 becomes open.
- Any taxi bout filmed with both speed and tail-beat frequency, which would close O1 and test B1 and B2
  directly.

```swarm-entail
{"source_claim": 269, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The terminal speed of a surface taxi bout must lie in the claim's ceiling band and stay below the speed needed to remain airborne; the animal must be unable to taxi up to flight speed.",
      "quantity": "taxi terminal speed (absolute)", "lo": 2.19, "hi": 2.88, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by a field record: 400 m in 30 s by repeated taxi+flight (Franzisket 1965, as cited in Deng et al. 2019), mean 13.3 m/s by my arithmetic, 4.6x the claimed ceiling; also reported glide peak 15-20 m/s and taxiing 'to reach take-off speed' (Davenport 1994).",
      "satisfied_evidence": "measured",
      "note": "Franzisket 1965: could-not-access (cited in Deng et al. 2019 bioRxiv 10.1101/765560, full-text via automated extraction). Davenport 1994 Rev Fish Biol Fish 4:184-214: search-summary. Disagreement kept: Makiguchi et al. 2013 Aquat Biol 18:105-111 (search-summary) estimated lab-tank take-off speeds of 3.9-5.2 m/s, which bracket the claim's 4.41 m/s; the authors attribute the low values to tank confinement. Conditional: if claim 269 models a small or tank-confined fish, this becomes open. The method behind the 1965 record is unknown to me."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Taxi tail-beat frequency must be high enough to fit 30-38 strokes into a 1.5-2 m bout at the claimed speeds.",
      "quantity": "taxi tail-beat frequency (derived from claim, assuming monotone concave speed rise)", "lo": 16.4, "hi": 73, "units": "Hz",
      "status": "satisfied",
      "satisfied_by": "~50 beats/s in ~25 C water (Hertel 1966, as cited in Deng et al. 2019); 'up to 50 beats/s' (Davenport 1994 abstract); 21.2 +/- 4.6 Hz at take-off (Makiguchi et al. 2013).",
      "satisfied_evidence": "literature",
      "note": "Hertel 1966: could-not-access (via Deng et al. full-text). Davenport 1994 and Makiguchi 2013: search-summary. Conflict kept: APS March Meeting 2024 S27.13 abstract (search-summary only; authors, species and temperature unknown) reports 13.5 Hz taxi tail-slapping, below the derived 16.4 Hz floor. The floor depends on my speed-profile assumption."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The surface-piercing caudal propulsor must advance the body only a short distance per beat, a small fraction of body length.",
      "quantity": "advance per stroke (0.13-0.27 body lengths for L = 0.25-0.30 m)", "lo": 0.039, "hi": 0.067, "units": "m",
      "status": "unsatisfied",
      "satisfied_by": "Not found. Searched for paired taxi speed + tail-beat frequency in the same bout (taxiing kinematics/video searches, Makiguchi 2013, Edgerton & Breder 1941, APS 2024, Deng et al. 2019). Nobody found has measured it; this is absence of measurement, not a negative finding.",
      "satisfied_evidence": "unknown",
      "note": "Nearest data are a different mode: submerged steady swimming gives 0.6-0.8 L per beat (Bainbridge 1958 J Exp Biol 35:109-133, via Wardle 1975; search-summary), 2-6x longer than the claim requires. Combining Hertel's 50 Hz with Davenport's 10-20 m/s gives 0.2-0.4 m per beat, but from separate reports, so it is not used as a contradiction."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The sustained power the caudal musculature can deliver in taxi mode must cover the power needed at the ceiling but fall short of the power needed at the 4.41 m/s glide speed.",
      "quantity": "available taxi power for a ~0.19 kg fish (derived by U^3 scaling of a simulated 36 W at 10 m/s)", "lo": 0.38, "hi": 3.1, "units": "W",
      "status": "unsatisfied",
      "satisfied_by": "No measured mechanical power output for exocoetid muscle found. Leans against the claim: underwater speeds of 3.9-5.2 m/s (Makiguchi 2013) to 10 m/s (Davenport 1994) combined with a simulated ~10x higher power for submerged swimming than for taxiing (Deng et al. 2019 CFD: 350 W vs 36 W at 10 m/s) would imply more power than the window allows. This is my inference through a simulation, so it is not unsatisfiable.",
      "satisfied_evidence": "simulated",
      "note": "Deng et al. 2019 bioRxiv 10.1101/765560 (full-text via automated extraction); the power window is my U^3 extrapolation of their CFD, not a measurement. The only muscle-power density in that paper (Gao & Techet 2011, ~2300 W/kg) is a requirement, not a measured capacity."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The axial fast muscle must complete contraction cycles fast enough to sustain the required tail-beat frequency.",
      "quantity": "muscle contraction time T = 1/(2f)", "lo": 6.8, "hi": 30.5, "units": "ms",
      "status": "satisfied",
      "satisfied_by": "Wardle 1975 stride-frequency/contraction-time relation: minimum contraction time ~25 ms for L = 0.3 m at 20 C (as read by Deng et al. 2019), which is within the 30.5 ms bound for the claim's lowest required frequency.",
      "satisfied_evidence": "literature",
      "note": "Wardle 1975 Nature 255:725: search-summary; the 25 ms value is secondary, via Deng et al. The relation comes from other teleosts; no exocoetid muscle kinetics found. Disagreement kept: by the same relation the field ~50 Hz needs T ~ 10-12 ms, about half of Wardle's 20 C value (Deng et al.), so the field frequencies are under strain from it but the claim's lower-frequency regime is not."}
  ]}
```
