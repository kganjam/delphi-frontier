# Challenge 110: adversarial review of S7-D-D (radial-row bending section)

Date: 2026-11-04.

**Claim under review.** S7-D-D, branch `claude/s7-d-sensitive-input-n67r40`, file `docs/research/fish/S7-D-deepen.md`. Its evidence level is recorded as *derived*.

**Scripts.**
- `challenge-110.py`: calculations only.
- `challenge-110-measure.py`: my own image measurement.

**Outcome: WEAKENED.**
- **The core number survived.** It is the locked-cantilever bending deficit of the proximal-radial row: a solid-equivalent d of 0.12–0.20 mm against 0.26 mm required, about 4× over yield at mid geometry. I re-derived it independently and re-measured it from the same source movie. It also survived every relaxation I tried.
- **Two downstream statements in the claim are not supported as stated.**
  - (a) "Bone survives … carry compression (≤23 MPa)" was checked against yield only. A slender plate in compression fails by buckling first. In the claim's own small-moment-arm regime, buckling is at or past critical for plausible bone moduli.
  - (b) The "~2–2.5× thicker plates" needed to lock the joint assumes fused radials still act as independent plates. My measurement shows the plates are not coplanar. If fusing makes them act as one section, the needed thickening is smaller.
- **The verdict word "falls" is broader than the evidence.** By the claim's own §4d, bone is still not limiting in the wild-type hinged load path. What falls is S7-D's bone conclusion **for the locked case**.

## 1. Arithmetic, redone independently

All values in this section are calculation (`challenge-110.py`).

**Root moment.**
- Inputs: W = 0.4 g · g; V = 3 m/s; n = 3; C_L = 0.78; AR = 9; body half-width 2.5 mm; elliptic loading. These are the claim's inherited inputs.
- Results: M = 1.081×10⁻⁴ N·m, wing area 9.32 cm² for both fins, span 9.2 cm.
- My note: the "design fish" has flying-fish-scale fins. This is inherited from S7 and not questioned here.

**Required section.** With σ_y = 62.6 MPa: Z_req = 1.727×10⁻³ mm³, d_req = 0.260 mm. This matches the claim.

**Section moduli,** Z = Σw·h²/6:

| Geometry | Z (mm³) | d_eq (mm) | Capacity / demand | Stress / yield |
|---|---|---|---|---|
| low (0.36, 0.055) | 1.82×10⁻⁴ | 0.123 | 0.105 | 9.5 |
| mid (0.40, 0.08) | 4.27×10⁻⁴ | 0.163 | 0.247 | 4.0 |
| high (0.44, 0.10) | 7.33×10⁻⁴ | 0.195 | 0.425 | 2.4 |

The claim's numbers (0.12/0.16/0.20 mm; "~4×", "2.4–9×") reproduce. **No arithmetic error was found.**

## 2. The image measurement, redone independently

**Source.** Ishizaka et al. 2024, *Sci. Rep.*, PMC11464670. Supplementary Movie S4 (`41598_2024_74134_MOESM4_ESM.mp4`), downloaded by me from the Europe PMC supplementaryFiles endpoint. Read-level: **full-text of the supplementary movie**, i.e. I viewed the file itself. I did not re-read the article text, and inherit the claim's reading of it.

Everything in this section is **my measurement from rendered images**, not a number the authors report.

- **Scale bar.** At 960-px width the 100 µm bar is about 62 px, so about 124 px at 1920 px. This confirms the claim's 0.806 µm/px.
- **Orientation check.** This was my main attempt to break the claim.
  - The worry: in the near-edge-on frames (24 fps, t ≈ 12–15 s) the red distal radials spread along the 0.93 mm long axis. That raised the possibility that the long axis is chordwise rather than proximodistal. If it were, Σw and length would be swapped.
  - The face-on frame (2 fps frame 22) settles it. Each grey proximal radial is a plate with a broad, fenestrated proximal end. It tapers to a rod-like shaft whose tip carries a red distal radial. The plates are staggered in length, so the tips lie on an oblique line.
  - **The claim's axis assignment is correct.**
- **Edge-on thickness.**
  - Method: I used full-rate frames near the minimum whole-assembly projected extent, which is a stable 272–283 µm over many consecutive 1/24 s frames. At 10% stations along the long axis I measured both the envelope extent and the filled grey thickness.
  - **Occlusion.** At several stations red distal radials sit in front of the grey and depress the filled count. The claim did not mention this. Examples: frames whose stations read 12–39 µm filled carry 135–600 red px.
  - At **unoccluded** distal-half stations, filled thickness is **51–83 µm** and envelope **139–176 µm**. This matches the claim's 55–100 µm. The claim's 55 µm low end is not purely an occlusion artefact, because unoccluded stations reach 51 µm.
  - Interpretation, my inference: filled is well below envelope at the same station, so the shafts are **not coplanar**. They sit at different depths across a 140–175 µm envelope (the row is arched or staggered). Some of this could be residual tilt, which I could not fully exclude.
- **Width.** Face-on, the distal shafts measure about 80–115 µm each (by eye on frame 22). That is consistent with Σw ≈ 0.3–0.45 mm across 3–4 elements.
- **Consequence for the claim's model.**
  - The claim's h is a union-projected thickness through several non-coplanar shafts. Each shaft's own h is therefore ≤ that value.
  - For independent plates this makes capacity **lower**, not higher. **The locked-cantilever deficit is, if anything, understated.**

## 3. Hidden assumptions, relaxed

All results here are calculation.

| Relaxation | Mid ratio | High ratio | Verdict on core number |
|---|---|---|---|
| Fully plastic section (shape factor 1.5) instead of first yield | 0.37 | 0.64 | still fails |
| Bone strength needed to pass (elastic / plastic) | 4.0× / 2.7× of 62.6 MPa | 2.4× / 1.6× | needs 100–250 MPa |
| Isometric size: scanned fish would need to be ≤ this fraction of design-fish length | 0.63 | 0.75 | same loophole the claim stated |
| Bending direction swapped (in-plane) | — | — | see below |

**Bending direction.** The claim says swapping in-plane would raise capacity about 5× (Σw/h). For separate side-by-side plates bending in-plane, Z = Σ h·w_i²/6 = h·Σw²/(6n). That is a gain of Σw/(n·h) ≈ 1.25 at mid geometry, not 5. The claim's own escape hatch is smaller than it says, which strengthens the core claim.

**Proxies.**
- Rendered-isosurface silhouette standing in for a true cross-section. The claim disclosed this.
- Herring intermuscular-bone tensile yield standing in for zebrafish radial strength. The claim disclosed this too.
- Relaxing the strength proxy by up to 2.4× (high) or 4× (mid) is needed to rescue the claim. I have **no sourced zebrafish radial strength**. I did not search for one this session, so this stays `unknown`.

## 4. Where the claim is weakened

### 4a. Compression rescue omits buckling

The claim says bone survives because the radials "carry compression (≤23 MPa)", and compares that only with yield. I ran an Euler check, pinned-pinned because both ends are synovial per the claim's own Askary 2016 reading. Setup:
- Four independent plates.
- Free length 0.95 mm. This is an upper bound; lateral soft-tissue support would raise P_cr.
- E is **my assumption**, bracketed 5/10/20 GPa. It is not sourced.

P_cr / F at the worst case (`challenge-110.py` §6):

| r | low geometry, E 5 / 10 / 20 GPa | mid geometry, E 5 / 10 / 20 GPa |
|---|---|---|
| 1.0 mm | 2.5 / 5.1 / 10 | 8.6 / 17 / 35 |
| 0.5 mm | 1.3 / 2.5 / 5.1 | 4.3 / 8.6 / 17 |
| 0.15 mm | **0.38 / 0.76** / 1.5 | 1.3 / 2.6 / 5.2 |

**Reading the table:**
- At S7's assumed moment arm r = 0.5–1 mm, the compression rescue holds.
- At r = 0.15 mm, buckling is the governing mode. Low geometry buckles at E ≤ 10 GPa, and mid geometry has only 1.3× margin at 5 GPa. The claim itself raised r = 0.15 mm as an "untested lead".
- So "≤23 MPa, therefore fine" is **not established** across the claim's own stated range. This is calculation on an assumed E.

### 4b. "~2–2.5× thicker plates" depends on the plates staying independent

The 2.0× (no safety factor) and 2.46× (SF 1.5) figures reproduce for independent plates. Fusing or locking the radials is exactly the design option in question.

If fused shafts act as one section across the measured 130–160 µm envelope, Z rises by about **1.7–2.5×**. This is calculation from my rough image-measured offsets (3 shafts, w 0.10 mm, h 0.06 mm). On that assumption, fusion alone closes much of the mid-geometry 4× deficit, and the plate-thickening needed is smaller than 2×.

This is an estimate on uncertain offsets, possibly inflated by residual tilt. It is not a measured composite section. The direction of the effect is robust; its size is not.

### 4c. Scope of "falls"

S7 already placed the binding constraint at the mobile joint and its muscle couple (S7-D lines 14 and 137). S7-D's "bone probably not limiting" was a bending check that it itself called "genuinely open" for radial-sized rods.

The claim's own §4d finds bone not limiting in the wild-type (hinged) path. **My inference:** the accurate statement is "falls for the locked-joint case; survives, for a different reason, in the hinged case, pending the buckling check in 4a". "Falls as stated" in the headline overstates what was refuted.

## 5. Evidence level

*derived* is honest:
- The claim labels §3b as its own image measurement and §4 as calculation.
- It calls h an "upper-bound silhouette".
- The opening "Measured from published wild-type µCT" is qualified in the same sentence ("my image measurement").

Two small honesty gaps:
- Red-occlusion of grey pixels was not disclosed as a bias.
- The ≈5× in-plane figure in §6 is wrong (≈1.25×).

Neither changes the core number.

## 6. Counter-examples and regimes not covered

**Parallel load path.** Askary 2016 (as quoted by the claim) describes a joint "between the marginal ray and scapula". If the leading marginal ray articulates directly with the scapula, part of the root moment bypasses the radial row in a locked design. This is a parallel path the claim omits.
- Its section is `unknown`: I did not measure the marginal ray.
- The scan is a dissected fin, so the scapula is not in Movie S4.
- This could only reduce the radial row's share of the moment.

**Taxa.** I ran no literature search for flying-fish or hatchetfish radial sections this session. The claim reported its own Europe PMC searches (17 hits, no numbers) and I did not repeat them. Scope of my negative: none run.

## Sources

| Source | What I used | Read-level |
|---|---|---|
| Ishizaka et al. 2024, *Sci. Rep.*, doi:10.1038/s41598-024-74134-9, PMC11464670 | Supplementary Movie S4, downloaded and measured by me | full-text for the movie file; article text not re-read by me |
| Askary et al. 2016, *eLife* 5:e16415 | Quoted via the claim | listing for me (not re-read) |
| S7-D (`claude/deepen-s7-pectoral-girdle-b6j2hx:docs/research/fish/S7-deepen.md`) | Verdict and the stated binding constraint | full-text |
| S7-D-D (`claude/s7-d-sensitive-input-n67r40`) | Document and script | full-text |

```swarm-challenge
{"claim_id": 110, "outcome": "weakened", "reason": "The locked-cantilever deficit (solid-equivalent d 0.12–0.20 mm vs 0.26 mm, ~4× over yield) reproduces arithmetically and on my independent re-measurement of Movie S4 and survives plastic-section and size relaxations, but the claim's compression rescue ignores Euler buckling (P_cr/F 0.38–1.3 at r = 0.15 mm, E 5–10 GPa assumed), its 2–2.5× plate-thickening figure assumes fused radials act as independent plates although they are non-coplanar (fused Z ~1.7–2.5× higher, estimate), and 'falls' overstates a refutation that applies only to the locked-joint case.", "corrected_value": "locked-row capacity/demand 0.11/0.25/0.43 (first yield) and 0.16/0.37/0.64 (fully plastic) at 1.08e-4 N·m — unchanged; thickening needed if fused ≈1.3–1.6× (estimate) rather than 2–2.5×", "depends_on": ["S7 root moment 1.08e-4 N·m (V 3 m/s, n 3, C_L 0.78, AR 9, m 0.4 g; inherited, recomputed)", "bone yield 62.6 MPa (Fiedler 2019 herring IB, inherited proxy)", "Ishizaka 2024 Movie S4 scale bar 100 µm = 124 px (my check)", "my image measurement: unoccluded distal filled thickness 51–83 µm, envelope 139–176 µm, shaft width ~80–115 µm", "assumption: bone E 5–20 GPa (not sourced) for buckling", "assumption: pinned-pinned free length 0.95 mm, no lateral support", "claim's muscle moment arm range r 0.15–1 mm", "assumption: fused shafts act as one section with offsets from the measured envelope", "Askary 2016 synovial radial joints and marginal-ray–scapula joint (as quoted by the claim)"]}
```
