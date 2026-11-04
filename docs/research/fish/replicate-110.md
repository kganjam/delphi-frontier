# Replicate 110: does the proximal-radial row have enough bending section? (S7-D-D)

**Status:** independent re-derivation of part of the claim. I measured the bending section of the wild-type
proximal-radial row myself. I could **not** derive the required section (0.26 mm), the ~4× overstress or the
"2–2.5× thicker" figure, because their inputs (fin root moment, bone yield stress, the 23 MPa compression) are in
`harvest:s7-d-sensitive-input-n67r40`, which is **not in this repository**. I searched every branch for
`harvest`, `n67r40`, `S7-D`, `Ishizaka` and `radial`, and the only hit was an unrelated zebrafish problem title in
`findings/gemini-triage-267-problems.json`. Nobody else's working for this claim appeared during the search, so
I read none of it.

## My value

All values below are **calculated from my own image measurement**. None of them is a direct observation of
strength.

- **Solid-equivalent bending section of the wild-type proximal-radial row, along the shaft region:
  0.09–0.21 mm**, expressed as the diameter of a solid round bar with the same section modulus.
  - The median is 0.13 mm (0.14 mm if I treat the radials as fused).
  - The section is smallest distally (~0.09–0.12 mm) and largest at mid/proximal levels (~0.17–0.21 mm).
  - It tapers to 0.04–0.06 mm at the articular ends.
- **Uncertainty:** about ±15% on the diameter, before the slice-orientation caveat below.
  - Segmentation-edge sensitivity (2 px erosion versus none) moves the diameter by up to −20% at the thin end.
  - The scale-bar read is ±1 px out of 153.
  - Slice obliquity is unknown and could bias the result in either direction.
- **Section geometry:** the radials are **hollow** in cross-section. They appear as rings or hollow triangles with
  walls roughly 15–40 µm thick, not solid plates.
  - The row's summed width at mid-levels is 0.44–0.47 mm.
  - The overall depth perpendicular to the row is 0.17–0.22 mm.
  - So "plates ≤55–100 µm thick" does not describe the section I see. Because the radials are hollow, the
    resulting section modulus nevertheless lands in a similar range.

## Sources and read-levels

| Input | Source | Read-level |
|---|---|---|
| Wild-type 3D segmentation of proximal (grey) and distal (red) radials, left pectoral fin | Ishizaka et al. 2024, *Sci Rep* 14:23602, doi:10.1038/s41598-024-74134-9, **Movie S4** (`MOESM4_ESM.mp4`, md5 120b6538…) | full-text (the movie file itself, from the Europe PMC supplementary zip) |
| Wild-type 2D CT slice series with proximal radials outlined yellow; per the legend, "these outlines were used to create Movies S4–S6" | same paper, **Movie S7** (`MOESM7_ESM.mp4`, md5 77fcd7cd…) | full-text (movie file) |
| Movie legends: S4 is wild-type, same individual as S1, Imaris 10 | same paper, MOESM8 supplementary PDF | full-text |
| Micro-CT ScanXmate-E090S105, isotropic voxel 3.1–3.4 µm; fish SL and age **not reported** | same paper, Methods (via PMC) | full-text (via a summarising fetch tool) |
| Scale: S4 has 100 µm = 123 px, constant across all 21 sampled frames; S7 wild-type panel has 150 µm = 153 px | my reading of the burned-in scale bars | measurement |
| Synovial-like cavities at the pectoral **ray–scapula** and **proximal–distal radial** joints; prg4b expressed in joint-lining cells | Askary et al. 2016, *eLife* 5:e16415 | search-summary (abstract and snippets only; I did not read the full text) |
| Fin root moment, bone yield strength, compressive stress (≤23 MPa), the "0.26 mm required" figure | `harvest:s7-d-sensitive-input-n67r40` | could-not-access (not in the repository) |

Note on Askary 2016, at search-summary level only:

- The summary I saw names the **proximal–distal radial** and **ray–scapula** joints.
- It does **not** name a proximal-radial–scapulocoracoid joint.
- The claim's step "radials articulate through synovial joints, so the root moment goes onto the muscle couple"
  needs the girdle-side joint of the proximal radials to be mobile.
- I have not confirmed from Askary that it is. This is my inference about a gap, not a statement of what the paper
  says.

## Method and arithmetic

1. **Getting the movies.** PMC served a proof-of-work page and Springer's static host returned 403, so I downloaded
   the supplementary zip from `ebi.ac.uk/europepmc/webservices/rest/PMC11464670/supplementaryFiles`.
2. **Using Movie S4.** S4 is a 3D surface render. Its "edge-on" views are oblique and show overlapping elements, so
   I could not measure the thickness of individual plates reliably from it. I used it to cross-check width only.
   - The anterior rod measures about 120 px × 0.813 µm/px ≈ 100 µm wide.
   - That matches the 96–124 µm component widths in S7.
3. **Using Movie S7.** S7 shows transverse CT slices through the fin base, stepping from the rays to the
   scapulocoracoid, in three panels: wild-type, hoxaa⁻/⁻, and hoxda⁻/⁻. I sampled it at 2 fps (51 frames).
   - From the wild-type panel I took the yellow (proximal-radial) pixels with an RGB threshold and a 1-px opening.
   - The script is `replicate-110-section.py` and the per-frame output is `replicate-110-table.txt`.
4. **Section properties, per frame.**
   - The row direction **r** is the major principal axis of all yellow pixels. The bending normal **n** is
     perpendicular to it.
   - Hydrodynamic load normal to the fin plane bends the row about **r**.
   - For each radial *i*, I computed its area, Iᵢ = Σ tⱼ² · (px area) with tⱼ the distance along **n** from that
     radial's centroid, and cᵢ = max|t| + ½ px.
   - Treating the radials as separate members: Z_sep = Σ Iᵢ/cᵢ.
   - Treating them as fused: Z_fused uses the row's common centroid.
   - Equivalent solid round diameter: d_eq = (32 Z / π)^(1/3).
5. **Worked example, frame 032 (mid-row, largest section):**
   - Two components: 13,948 µm² (136 µm wide) and 31,303 µm² (332 µm wide). Total A = 0.0453 mm².
   - Z_sep = 9.38×10⁻⁴ mm³.
   - d_eq = (32 × 9.38×10⁻⁴ / π)^(1/3) = (9.55×10⁻³)^(1/3) = **0.212 mm**.
6. **Worked example, frame 014 (distal shaft):**
   - Z_sep = 1.14×10⁻⁴ mm³.
   - d_eq = (32 × 1.14×10⁻⁴ / π)^(1/3) = (1.16×10⁻³)^(1/3) = **0.105 mm**.
7. **Range over the shaft frames 014–036 (22 frames):**
   - d_eq_sep runs 0.105–0.212 mm, median 0.132 mm.
   - After a 2-px erosion it runs 0.090–0.205 mm.
8. **What would be required.** Z_req = M/σ_y. With M and σ_y unavailable, the required diameter is **unknown**.
   - For comparison only: *if* d_req = 0.26 mm, then Z_req = π · 0.26³ / 32 = 1.73×10⁻³ mm³.
   - The ratio Z_req/Z_measured would then be 1.73e-3 / 9.4e-4 = 1.8× at the strongest level.
   - The same ratio would be 1.73e-3 / 1.14e-4 = 15× at frame 014, or 1.73e-3 / 7.7e-5 ≈ 22× with erosion.
   - These ratios assume the 0.26 mm I could not verify, and they assume the distal shaft actually carries the full
     root moment, which it may not, because the moment falls off away from the root.

## Caveats, stated as limits on the result

- **Slice orientation is unknown.** S7 gives no slice spacing or plane normal. If the plane is oblique to the
  radial axes by θ, the cross-section dimensions are inflated by about 1/cos θ along one direction.
- **Unknown fish size.** Ishizaka report no standard length or age for the CT specimens, so I cannot scale the
  result to other fish.
- **Single individual.** S4 and S7 show one wild-type left fin. Ishizaka scanned n = 3, but only one is in the
  movies.
- **Where the moment peaks.** The maximum root moment is at the girdle end. At the most proximal frames (037–041)
  only one radial remains in the slice, with d_eq 0.11–0.17 mm. The others have presumably already ended at their
  articulations; that is my inference from the slices.

## Comparison with the recorded value

I looked at the recorded value only after finishing everything above.

The recorded claim gives a measured solid-equivalent section of ~0.12–0.20 mm. My independent value is
0.09–0.21 mm, median 0.13 mm.

- **Measured section:** I **agree** on the magnitude. I **disagree** on the geometry. I see hollow tubular radials
  with 170–220 µm overall depth, not plates ≤55–100 µm thick. The two descriptions happen to give a similar section
  modulus.
- **"0.26 mm required", "~4× yield", "2–2.5× thicker plates":** I **cannot tell**. The load and strength inputs are
  not accessible to me, and my Askary read is too shallow to confirm that the girdle-side joint is synovial.
- **Overall: CANNOT TELL.** Only the measurement half of the claim is replicated. The load-side conclusion, that a
  locked joint would yield ~4×, is not.

```swarm-replication
{"claim_id": 110, "my_value": "0.09–0.21 mm solid-equivalent (round-bar) bending section of WT proximal-radial row, median 0.13 mm (calculated from Ishizaka 2024 Movie S7 slices; required section unknown)", "agrees": null,
  "note": "Measured section matches the recorded 0.12–0.20 mm, but radials are hollow tubes not ≤100 µm plates, and the 0.26 mm requirement/4× overstress could not be re-derived because the S7-D load inputs are not in the repo."}
```
