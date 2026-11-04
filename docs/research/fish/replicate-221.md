# Replication 221: S7-D-D, "girdle bone probably not limiting" FALLS

Project: `zebrafish-flight`. Date: 2026-11-04. Script: `replicate-221/sec.py`.

## Disclosure before anything else

- I was told not to read the recorded result first. I mostly managed that, with one leak. Running `git show --stat` on `claude/s7-d-sensitive-input-n67r40` printed the commit message before I had derived anything. The message says: "solid-equivalent d 0.12-0.20 mm vs 0.26 mm required", that the section came from Ishizaka et al. 2024 Movie S4, and that S7-D's bone verdict "falls". So I knew the source paper and the rough answer in advance.
- To limit how much that leak could anchor me, I measured a **different** supplementary file from the same paper, **Movie S7**. Movie S7 shows real µCT slice images with the segmentation overlaid. Movie S4 is a rendered 3D isosurface. I also used a **different method**: true section moduli computed from the pixels of each slice, not silhouette widths. I did not open `S7-D-deepen.md` or `.py` until §5.
- **Independence caveat.** Both measurements come from the same paper and the same wild-type fish. Movie S7's legend says its outlines "were used to create Movies S4-S6". So my result is independent in method only, not in specimen.

## 1. The question

S7 (`S7-organ.md`, branch `claude/s7-organ-pectoral-girdle-xlxpkt`) concluded that girdle bone strength is "probably not limiting". It reached that by treating the receiving bone as a solid rod. It also left open whether the real element has the required solid-equivalent diameter. S7 named the flip condition itself: if the section is ≤ 0.15 mm, "the answer flips to 'no'".

The replication target is therefore this comparison: the measured solid-equivalent bending diameter of the wild-type proximal-radial row, against the diameter required at the design root moment.

## 2. Inputs

| Input | Value | Source | Read-level | Calculated, assumed or observed |
|---|---|---|---|---|
| Root moment per fin, worst case | 1.08×10⁻⁴ N·m. I re-checked it: 3·(3.92 mN/2)·18.4 mm = 1.083×10⁻⁴ | S7 §3c | full-text (repo document) | **Calculated** by S7. It rests on S7's own assumed brackets (V = 3 m/s, n = 3, C_L 0.78 at search-summary level, AR 9). |
| Other moments | 3.6×10⁻⁵ (V3,n1), 6.24×10⁻⁵ (V5,n3), 2.08×10⁻⁵ (V5,n1) N·m | S7 §3c | full-text (repo) | Calculated by S7 |
| Bone yield σ_y | 25–114 MPa | S7 A8 | full-text (repo) | **Assumed**: E × 0.5% strain. E comes from vertebral nanoindentation, read at search-summary level. |
| Bone yield, alternative | 62.6 MPa ("measured herring bone yield") | S7-D, as quoted in S7-D-D §0 | listing: seen only quoted, after my derivation | I did **not** verify it. I show it only for comparability. |
| Wild-type proximal-radial sections | Per-slice segmented yellow regions, wild-type panel | Ishizaka et al. 2024, *Sci. Rep.* 14:23602, doi:10.1038/s41598-024-74134-9, PMC11464670, **Supplementary Movie S7** (MOESM7), downloaded from the Europe PMC supplementaryFiles zip | full-text for the supplementary PDF legends (MOESM8). The movie itself was read frame by frame. | **My image measurement** from a published movie. These are not numbers the authors report. |
| Pixel scale | 150 µm scale bar = 152 px, so 0.987 µm/px (wild-type panel) | Same movie, measured by the script | as above | My image measurement |
| Number of proximal radials in wild type | 4 (pr1–pr4) | I count 4 grey rods in Movie S4, frame 1. The S7-D-D document says the paper states this, but I did not read that in the paper's text myself. | listing | Observation from an image |

**Authors' legend (MOESM8), as written:** "Movie S7. 2D movie showing the proximal radials and distal radials in wild-type … The 2D movie display the proximal radials (yellow) distal radials (magenta), and fin rays (cyan) … These outlines were used to create Movies S4-S6."

**Not reported by the authors (per the supplementary PDF):** fish standard length and any element dimension.

## 3. Measurement method (image measurement, not observation)

1. I sampled Movie S7 at 2 frames per second from 4 to 17 s, giving 26 frames.
2. I masked the yellow (proximal-radial) pixels in the wild-type panel, applied a 1-pixel binary closing, and kept connected components of at least 150 px.
3. For each component I computed:
   - area A;
   - the principal second moments I_min and I_max from pixel moments (holes are excluded automatically, so the tubular radials count as hollow);
   - the extreme-fibre distance c along each principal direction, plus half a pixel;
   - Z = I/c;
   - the solid-rod-equivalent diameter d = (32Z/π)^(1/3).
4. Where several radials were cut in the same slice, I combined them as a **locked row that shares the moment**: d_row = (Σd³)^(1/3), since Z adds.

### Frames along the radial shafts (4–15 s, before the slices merge into the unsegmented scapulocoracoid)

| Frame | d per element, weak axis (µm) | d per element, strong axis (µm) | Row d, weak / strong (µm) |
|---|---|---|---|
| 011 | 82, 61 | 118, 103 | 92 / 140 |
| 012 | 80, 70 | 134, 82 | 95 / 144 |
| 015 | 95, 49 | 161, 58 | 99 / 163 |
| 017 | 94, 40 | 189, 63 | 96 / 191 |
| 020 | 68, 34, 34, 37 | 121, 93, 56, 95 | 76 / 153 |

Earlier frames (001–007) give elements of 10–60 µm (weak axis) and 30–100 µm (strong axis). Frames 022–026 reach 100–150 µm per element. At that level the slice is entering the scapulocoracoid junction, where the yellow regions enlarge and probably include oblique cuts, so I do not treat them as shaft sections.

**My value (image measurement plus calculation):**

- The solid-equivalent bending diameter of the wild-type proximal-radial row, treated as a locked cantilever, is **d ≈ 0.08–0.19 mm**. That is ≈ 0.08–0.10 mm about the weak principal axis and ≈ 0.14–0.19 mm about the strong axis.
- **Generous upper bound:** four radials each as large as the biggest shaft section seen, bent about the strongest axis, gives 4^(1/3) × 0.16 = **0.25 mm**. This is not physical, because the radials are not all that large in the slices.

**Uncertainties I cannot remove:**

- I do not know which principal axis corresponds to bending out of the fin plane. That is why I report both axes.
- The slice plane may be oblique to the radial long axis. Obliquity inflates area and Z, so the values lean high.
- Compression blur and the colour threshold make about ±1–2 px of boundary uncertainty. That is about ±5–10% on d for an 80 µm element.
- The size of the scanned fish is `unknown`.

## 4. Arithmetic (calculation)

Required diameter: d_req = (32M / (π σ_y))^(1/3). Capacity divided by demand: (d/d_req)³.

| M (N·m) | σ_y 25 MPa | σ_y 62.6 MPa | σ_y 114 MPa |
|---|---|---|---|
| 1.08×10⁻⁴ (worst case) | 0.353 mm | 0.260 mm | 0.213 mm |
| 3.6×10⁻⁵ (V3, n1) | 0.245 | — | 0.148 |
| 6.24×10⁻⁵ (V5, n3) | 0.294 | — | 0.177 |
| 2.08×10⁻⁵ (V5, n1) | 0.204 | — | 0.123 |

### Worst case: capacity divided by demand

| Measured d | 25 MPa | 62.6 MPa | 114 MPa |
|---|---|---|---|
| 0.08 mm (weak axis) | 0.01 | 0.03 | 0.05 |
| 0.10 mm | 0.02 | 0.06 | 0.10 |
| 0.16 mm (strong axis, typical) | 0.09 | 0.23 | 0.42 |
| 0.25 mm (unphysical upper bound) | 0.36 | 0.89 | 1.62 |

Stress check at d = 0.15 mm under the worst-case moment: σ = M/Z = 1.08×10⁻⁴ / (π·(0.15 mm)³/32) = **326 MPa**. That is 3–13 times the 25–114 MPa yield bracket.

**Result (calculated from my image measurement):**

- Across every plausible geometry, the measured wild-type radial row falls short of the S7 worst case by a factor of roughly **2.4–100 in Z**, or about 0.4–0.75 in d.
- It passes only in the unphysical upper-bound geometry combined with the top of the yield bracket.
- At steady glide (n = 1), the strong-axis value (0.14–0.19 mm) against d_req 0.148–0.245 mm is **marginal**.

So, under S7's own flip criterion ("≤ 0.15 mm … flips to 'no'"), "girdle bone probably not limiting" **does not stand** for the proximal-radial row as a locked cantilever.

**My inference, not a source's claim:** this verdict applies only to path 1 (a locked cantilever). If the fin–radial joint is a mobile hinge, which is S7's own "path 2", the radials carry compression and bearing rather than the full bending moment. Then the binding element is the joint and muscle, not bone stiffness. That does not rescue the claim as worded. It moves the problem to a part that has not been measured.

**Negative-search scope:**

- Europe PMC article metadata and supplementary zip for PMC11464670 only, plus one web search for "Ishizaka 2024 zebrafish pectoral fin proximal radials micro-CT supplementary movie".
- I did not try MorphoSource, other zebrafish µCT atlases, or the cleithrum and scapulocoracoid sections. The cleithrum was not measured.

## 5. Comparison with the recorded value (read only after §1–4)

The recorded result, from `S7-D-deepen.md` on `claude/s7-d-sensitive-input-n67r40`, read at full-text level:

- Measured from Movie S4 **silhouettes**: Σw 0.36–0.44 mm and h 55–100 µm, giving a solid-equivalent d of **0.12–0.20 mm (mid 0.163)**.
- d_req = **0.26 mm** at σ_y 62.6 MPa.
- Worst-case capacity divided by demand: **0.25 (0.11–0.42)**.
- Verdict: S7-D's "bone probably not limiting" **falls** for the radial row as a locked cantilever. The real load path is a synovial hinge (Askary et al. 2016).

**Agreement:**

- My d of 0.08–0.19 mm overlaps theirs (0.12–0.20 mm). Mine sits slightly lower at the weak-axis end.
- My worst-case ratio at 62.6 MPa is 0.03–0.23, against their 0.11–0.42.
- My d_req of 0.260 mm at 62.6 MPa matches theirs exactly. That is the same arithmetic, not an independent check of the yield value, which I did not verify.
- Both derivations conclude the claim falls on path 1, with the same caveat about the hinge.

**Disagreement preserved:**

- My sections suggest the row may be **weaker** than their silhouette estimate. That is plausible, because silhouettes ignore the hollow lumen, and the S7 slices show the radials as tubes.
- My strong-axis values (0.14–0.19 mm) sit close to their range.
- Neither of us knows the fish size or the true bending axis.

**AGREE.** The direction agrees, and the magnitude agrees within overlapping ranges. My central estimate is somewhat lower, which strengthens the "falls" verdict rather than weakening it. The independence is partial: same paper, same fish, different movie and different method, and I saw the recorded headline in a commit message before deriving mine.

```swarm-replication
{"claim_id": 221, "my_value": "proximal-radial row solid-equivalent d ≈ 0.08–0.19 mm (image-measured from Ishizaka 2024 Movie S7 CT slices) vs d_req 0.21–0.35 mm at M=1.08e-4 N·m; capacity/demand ≈ 0.01–0.42 (0.03–0.23 at 62.6 MPa)", "agrees": true,
  "note": "Independent section-modulus measurement from the CT-slice movie (not the S4 silhouettes) also puts the wild-type radial row below the S7 flip threshold, so 'girdle bone probably not limiting' falls for the locked-cantilever path; independence is partial (same paper/fish, and the recorded headline leaked via a commit message before derivation)."}
```
