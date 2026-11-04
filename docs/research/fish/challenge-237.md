# Challenge 237: "Exocoetid flight is a multi-stroke task"

**Claim under review** (S30-organism.md, commit `59f421da`, branch `claude/s30-launch-budget-mass-k71prf`):

> "SO EXOCOETID FLIGHT IS A MULTI-STROKE TASK, not the single-impulse task S28 and S29 both modelled. The entire project framing -- one launch, one impulse -- does not describe how real fish gliders actually take off"

Recorded evidence level: **derived**. Value: n/a.

**Verdict: WEAKENED.** For adult exocoetids the claim holds, and the support is stronger than S30 realised. As a statement about "real fish gliders" in general, it overreaches. The one size class that resembles the project's 0.25–0.4 g design is juvenile flying fish of 1–5 cm. A search summary of a conference abstract reports that those fish leave the water in a ~0.05 s leap, not a surface taxi. S30 reached the universal claim by extrapolating downward with no small-fish source. It says so itself (§3.2: "I found no measurement of how the smallest exocoetids leave the water").

---

## 1. Arithmetic, redone independently

Every result in this section is **calculated by me**, not observed. I used ρ_air = 1.225 kg m⁻³ and CL_max = 1.07, the same values S30 assumes.

| Quantity | S30 value | My recomputation |
|---|---|---|
| Length of a 300 g *Cypselurus*, from L = 0.460·M^0.355 (Fish 1990 fit, project-transcribed) | 0.30 m | 0.300 m ✓ |
| V_to at WL 176 N m⁻²: √(2·WL/(ρ·CL)) | 16.4 m/s | 16.39 m/s ✓ |
| Fraction of the needed KE delivered at a 10 m/s exit: (10/16.39)² | 37 % | 37.2 % ✓ |
| Same fraction at a 3.9–5.2 m/s exit (Makiguchi et al. 2013; see §5) | not considered | **5.7–10.1 %** |

The arithmetic is correct. The second exit-speed source makes the adult case for multi-stroke *stronger*: if the fish leaves the water at 3.9–5.2 m/s, 90–94 % of the takeoff kinetic energy has to be added after exit.

## 2. Is a proxy standing in for the quantity that matters?

**Yes.** S30 uses **surface taxiing** as a proxy for **multi-stroke**.

- **The quantity that matters** for S28/S29 is how many propulsive strokes contribute to the kinetic energy the animal has at takeoff. "Single impulse" means one C-start-like stroke, as in S29's spring/LaMSA budget.
- **Taxiing is neither necessary nor sufficient** to settle that.
  - Saro-Cortes et al. 2022 (ICB 62:1202–1216) say the caudal fin propels the fish "directly into gliding flight or into the intermediate taxi stage". So not every adult takeoff includes a taxi.
  - Even a takeoff with no taxi is preceded by underwater acceleration to several m/s. My inference, not a measurement: that acceleration is burst swimming over many tailbeats, not one stroke. So a no-taxi launch would still be multi-stroke.
- **Effect on the adult case:** the proxy error does **not** hurt it. The right quantity, strokes per launch, gives the same answer as the proxy, by a wider margin.
- **Effect on the falsifier:** it does change S30's stated falsifier ("filmed … from a single submerged stroke … with no surface taxi"). Film showing no taxi would not, by itself, show a single stroke.

## 3. The hidden assumption, tested relaxed

**The hidden assumption:** what is true of adult (≥ tens of grams) exocoetids is also true at the masses the project actually models, 0.25–0.4 g. This is what carries the jump from "adult flying fish taxi" to "the entire project framing does not describe how real fish gliders take off".

**Relaxed test:** what do the smallest exocoetids do?

- **Source:** Yang, Phonekeo, Xu, Chang & Hu, APS DFD 2013, abstract "Flying fish accelerate at 5 G to leap from the water surface". **Read level: search-summary.** Fetching archive.aps.org failed because the host is outside this session's allowed network domains.
- **As summarised:** juvenile flying fish **1–5 cm** long were filmed at high speed. Leaving the water "lasts 0.05 seconds, with body accelerations of 5 times earth's gravity and gliding speeds of 1.3 m/s". The fish described "leap", not "taxi".
- **My consistency check (calculated):** 5 g × 0.05 s = 2.45 m/s of velocity change. That is the right order to produce a 1.3 m/s glide after drag and gravity losses, so the summary is internally plausible.
- **What it implies (my inference, not the authors' claim):**
  - **Duration:** the event is far shorter than an adult taxi (S30 cites 15–20 m/s reached by taxiing; Davenport 1994 gives up to 50 tailbeats s⁻¹ during taxi). A 0.05 s event is at most a few tailbeats. Whether it is literally one stroke is **unknown**: I could not read the abstract's full text or see the video.
  - **Wing loading:** a 1.3 m/s glide implies WL ≈ ½·ρ·CL·V² ≈ **1.1 N m⁻²** (calculated, with the same CL_max = 1.07 assumed). That is about 11× below the S28 design's 12.5 N m⁻². The specific energy needed is 0.85 J/kg, against 9.55 J/kg for the design.
  - **Consequence:** small exocoetids are not doing the S28/S29 task with a different launch mechanism. They are doing a much *easier* task, with low wing loading and a slow glide, using what looks like a brief leap.
- **Relation to S30's own scaling:** this fits S30's scaling direction ("smaller is easier"). It contradicts S30's universal claim that real gliders use multi-stroke launch "at every size" (§5 of S30).
- **Relation to S30's stated falsifier:** S30's falsifier needs a ≥1 g fish reaching ≥4 m/s. The juvenile record does not meet it (1.3 m/s, and mass unknown at the low end of 1–5 cm). **So S30's scaling survives. Its generalisation to "real fish gliders" does not.**

## 4. Is the evidence level honest?

**Partly.**

- **The adult part is mislabelled as derived.** Adults launching with a surface taxi is an **observation by others**: Edgerton & Breder 1941 high-speed photography, and Davenport 1994's abstract ("taxiing with the lateral fins expanded and the tail beating in the water at up to 50 beats s⁻¹"). Both are at search-summary level here. S30 cites only a SEARCH-EXTRACT of bioRxiv 765560 for it, and calls that "the weakest link". It is actually the best-attested part of the claim. Labelling it "derived" undersells it.
- **The small-fish part is mislabelled as derived.** "Multi-stroke at every size" is an **extrapolation with no source** (S30 §3.2 admits this). Calling it "derived" oversells it. It should read **"inferred, unsupported below adult size; contradicted at search-summary level by juvenile leap data"**.
- **What the label gets right:** S30 itself does not present a derived number as measured. Its honesty ledger is careful. The defect is that one headline sentence fuses an observation with an extrapolation under a single "derived" label.

## 5. Regimes, taxa and counter-examples the author missed

All sources below were read at search-summary level only. Direct fetches of par.nsf.gov, bamlab.princeton.edu, archive.aps.org, doaj.org and int-res.com all failed because those hosts are outside this session's allowed network domains.

1. **Juvenile exocoetids, 1–5 cm (Yang et al., APS DFD 2013).** Launch is a 0.05 s leap at 5 g, followed by a 1.3 m/s glide (§3). **This is the main counter-example, and it is in the size class closest to the project.**
2. **Makiguchi et al. 2013, *Aquat. Biol.* 18:105–111, doi 10.3354/ab00494.** Accelerometer loggers on *Cypselurus heterurus doederleini* give a leap speed of 3.9–5.2 m/s, which the authors put at 38.7–51.5 % of previously reported maximum swimming speeds.
   - **This disagrees with S30's ~10 m/s exit speed.** I keep both rather than average them.
   - A later review (Wikipedia, "Aerial locomotion in marine animals", search-summary) notes that the loggers may have changed the fish's locomotion.
   - Either value supports multi-stroke launch in adults.
3. **Saro-Cortes et al. 2022, ICB 62:1202.** Adult takeoff may go "directly into gliding flight" with no taxi stage. That breaks "taxi" as the defining feature of exocoetid launch, but not "multi-stroke" (§2).
4. **Freshwater hatchetfish (Gasteropelecidae).** Wiest 1995 (J. Zool. 236:571–592) is NOT READ; only secondary aquarium and ADW summaries were found. They report pectoral beating during water exit, followed by skimming or short ballistic leaps rather than true gliding. These are not established gliders, so they are neither support nor counter-example. They are noted only because they are another small (~1 g order) fish that leaves the water.
5. **Halfbeaks (Hemiramphidae) and *Pantodon*.** No source was searched in this session, so no claim is made either way.

**Scope of negative searches:**
- I ran four web searches, on Exocoetus/two-winged takeoff without taxi, hatchetfish exit, juvenile exocoetid takeoff, and Makiguchi 2013 details.
- I found **no source stating that two-winged *Exocoetus* launches without taxiing**. That was a counter-example I expected and could not confirm.
- I found no frame-by-frame stroke count for the juvenile leap.

## 6. What the claim should say

> In adult exocoetids (tens to hundreds of grams), takeoff is a multi-stroke task. Underwater burst swimming brings the fish to an exit speed of ~4–10 m/s (sources disagree), and most often a caudal-fin surface taxi follows, taking it to 15–20 m/s. That is not the single-impulse task S28/S29 modelled. In juvenile exocoetids of 1–5 cm, launch is reported (search-summary level) as a ~0.05 s, 5 g leap into a ~1.3 m/s glide. The stroke count there is unknown, but it is much closer to the single-impulse framing. It runs at a wing loading (~1 N m⁻², calculated) an order of magnitude below the S28 design's. So the single-impulse framing is wrong for adult flying fish. It is untested, not wrong, at the project's size.

## 7. What would settle it

1. Frame-by-frame tailbeat count during the juvenile leap (Yang et al. 2013 full data or video). If it is one stroke, the project framing describes real small gliders.
2. Juvenile exocoetid mass and wing area at 1–5 cm, to place them on the S30 m* curve.
3. A full-text read of Davenport 1994 on two-winged versus four-winged taxi frequency.

```swarm-challenge
{"claim_id": 237, "outcome": "weakened", "reason": "Multi-stroke launch is well attested for adult exocoetids (stronger than S30 knew: an observation, not a derivation, and Makiguchi 2013's 3.9-5.2 m/s exit means 90-94% of KE must come after exit), but the universal 'real fish gliders' / 'every size' extension has no small-fish source and is contradicted at search-summary level by juvenile (1-5 cm) flying fish that launch in a ~0.05 s, 5 g leap into a 1.3 m/s glide, and S30 uses surface taxi as a proxy for multi-stroke even though no-taxi launches occur.", "corrected_value": null, "depends_on": ["Yang-Phonekeo-Xu-Chang-Hu-APS-DFD-2013-juvenile-leap (search-summary)", "Makiguchi-2013-AquatBiol-18-105 (search-summary)", "Saro-Cortes-2022-ICB-62-1202 (search-summary)", "Davenport-1994-RevFishBiolFish-4-184 abstract (search-summary)", "Edgerton-Breder-1941 (search-summary)", "Fish1990-tables (project-transcribed, via S30)", "S30 V_to arithmetic (rho 1.225, CL_max 1.07 assumed)"]}
```
