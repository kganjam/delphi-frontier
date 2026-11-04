# Challenge 232: adversarial review of S7-D-D ("girdle section derived from µCT geometry")

Date: 2026-11-04.

**Claim under review.** Source: `harvest:deepen-s7-d-sensitive-input-tbjg48`, which is the file `docs/research/fish/S7-D-deepen.md` on branch `claude/deepen-s7-d-sensitive-input-tbjg48`, commit `6cd6d61`. I read it in full.

The claim says the smallest girdle bending section crossed by sagittal planes medial to the fin base has Z ≈ 3.6–6.8×10⁻³ mm³ in the 24 mm SL fish and ≈5.4×10⁻³ mm³ in the 20 mm SL fish. That would be 2.1–3.9× the 1.73×10⁻³ mm³ required. The claim's verdict is *strengthens*.

**Outcome: WEAKENED.** The 24 mm number roughly survives. The 20 mm number does not: the component it measures is very probably not girdle. When the girdle band is tracked, the 20 mm fish's medial girdle section falls below the requirement.

**Status of my numbers.** Every number I produce below is a **calculation**. Some are computed on the published surface mesh, which is itself measured geometry. I made no observation of bone and no mechanical test. Bone identities are **my inference** from position and continuity. The mesh is not segmented by bone.

---

## 1. Arithmetic, redone independently

I recomputed everything from the stated inputs: m = 0.4 g, V = 3 m/s, n = 3, C_L = 0.78, AR = 9, half-width 2.5 mm, elliptic centroid 4/(3π)·s, σ_y = 62.6 MPa.

| Quantity | My value | Claim | Status |
|---|---|---|---|
| Root moment M | 1.0813×10⁻⁴ N·m | 1.08×10⁻⁴ | Reproduces |
| Required section modulus Z_req = M/σ_y | 1.727×10⁻³ mm³ | 1.73×10⁻³ | Reproduces |
| Ratios for Z = 3.56, 6.80 and 5.42×10⁻³ | 2.06×, 3.94×, 3.14× | 2.1–3.9×, 3.1× | Reproduces |
| Four radial rods, Z = 4πd³/32 | d = 0.10 mm: 0.227×; d = 0.15 mm: 0.767× | 0.23–0.77× | Reproduces |

**The arithmetic is correct.**

## 2. Reproduction of the measurement

**Data.**

- I downloaded the Europe PMC supplementary ZIP for PMC9204358 (88,394,848 bytes). **Read-level: full-text (data files).**
- The SHA-256 prefixes match the author's: DataSheet4 `ead58b4f8cf9cce9`, DataSheet3 `1617b074648c2127`.

**Decoding.** I ran the author's `extract.py` and `pos.py` unchanged. They gave the same vertex counts as the author: 574,708 and 249,338.

**Sweep.** I re-ran the section code in the 20 mm frame with a box of x 5.5–8.3 mm and z 3.2–6.2 mm. It reproduced their JSON:

| Plane | My Z | Their Z |
|---|---|---|
| y = 3400, ±30 µm | 5.4×10⁻³ mm³ | 5.42×10⁻³ mm³ |
| y = 2800, ±30 µm | 2.2×10⁻¹ mm³ | 2.17×10⁻¹ mm³ |

The decoder and the section routine are therefore not where the claim breaks.

## 3. The proxy: "largest component in the plane" stands in for "the girdle section"

The estimator that carries the claim is **min over planes of the largest single component in each plane**. That is only a girdle statistic if, in every plane, the largest component *is* the girdle. The author never tracked bone identity from plane to plane.

I listed every component per plane (`challenge-232/comp.py`) and plotted them (`challenge-232/fig_sl24_components.png` and `fig_sl20_components.png`).

### 3a. Midline error in the 20 mm fish

The author took the midline at y = 4000 µm. The trunk vertices (z 8–14 mm, i.e. ribs and vertebrae) give a mean y of 3838 and a median of 3724 (calculated).

So the 20 mm planes at y = 3400–3700 lie about **0.05–0.4 mm** from the midline, not the stated 0.3–0.6 mm.

### 3b. In the 20 mm fish, the minimum component is very likely a median element

The component that gives the claimed 5.42×10⁻³ mm³ (y = 3400) sits at x 6.34–6.82 mm and z 4.34–4.71 mm.

- **It is still present at y = 3700.** That plane is about 50 µm from the trunk midline. There the component is at x 6.41–6.92 mm, with Z = 8.9×10⁻³ mm³.
- **It sits at mid-depth.** In this frame larger x is more ventral. The ventral girdle at this z sits at x ≈ 7.0–7.6 mm: the ventral end of the cleithrum's DV limb is visible at x ≈ 7.2–7.45 mm in the author's own Fig. 3, at y = 3000.

A paired girdle element does not sit at mid-depth on the body midline. **My inference:** this is a median pharyngeal or branchial element, for example a basibranchial or copula, not girdle. I cannot name the bone from the mesh.

### 3c. In the 24 mm fish, the same jump happens but does no harm

At y = 2400–2500 the "largest component" (Z ≈ 7.1–7.2×10⁻³ mm³) sits at x 4.6–5.2 mm. That is about 1 mm dorsal of the ventral bony band that runs continuously from the fin base at y 1300–2300, x 5.4–6.6 mm.

**The author's z ≥ 4.0 mm box truncates the girdle near the midline.** It clips that band where it turns anteriorly toward the midline. At y = 2500 the clipped band reads 3.4×10⁻⁴ mm³. Extending the box to z ≥ 3.0 mm restores it to 1.9×10⁻² (±15 µm) or 2.3×10⁻² (±30 µm) mm³.

### 3d. Re-estimate with the girdle tracked

The tracking estimator (`challenge-232/track.py`) uses the largest component whose centroid lies in the ventral band continuous with the fin-base girdle:

- 24 mm fish: x 5.5–6.7 mm
- 20 mm fish: x 7.0–8.3 mm

The z box is extended so the band is not clipped. All values are calculated, in mm³; ratios are to Z_req = 1.73×10⁻³.

| Fish | Slab | Min tracked-girdle Z (plane) | Ratio | Claim's value |
|---|---|---|---|---|
| 24 mm SL | ±15 µm | 3.1×10⁻³ (y 2400; ±30 gives 2.0×10⁻² in the same plane, so probably a fill gap) | 1.8× | 3.56×10⁻³, 2.1× |
| 24 mm SL | ±30 µm | 1.2×10⁻² (y 2100) | 7.0× | 6.80×10⁻³, 3.9× |
| 20 mm SL | ±15 µm | 3.8×10⁻⁴ (y 3400) | 0.22× | excluded as under-sampled |
| 20 mm SL | ±30 µm | **9.9×10⁻⁴ (y 3400)** | **0.57×** | 5.42×10⁻³, 3.1× |
| 20 mm SL | ±30 µm, sum of fragments | 1.5×10⁻³ to 2.25×10⁻³, depending on whether a far-anterior piece at z 3.0–3.4 mm is counted | 0.87–1.3× | none |

**24 mm fish: the claim survives.** Its girdle clears the requirement unscaled when tracked, by 1.8–7×.

**20 mm fish: the claim fails.** With the author's own preferred ±30 µm estimator, the tracked ventral girdle band is below the requirement unscaled: 0.57× for the single section and ≤1.3× summed. The claimed 3.1× comes from a component that is very probably not girdle.

**The two fish disagree.** I do not average them.

**Caveats on my own re-estimate:**

- The 20 mm mesh is sparse, which the author documented. Some of the low ±15 µm values are fill failures, and that could also affect my ±30 µm minimum.
- My band windows are positional choices. Bone identity is my inference.

So the honest statement is narrower than the claim. **The minimum medial girdle section in the 20 mm fish is unresolved.** On the available geometry it spans the requirement, about 0.2× to 1.3×. It is not ≈3.1×.

## 4. Hidden assumptions, tested relaxed

1. **The moment crosses the ventral midline through bone.** The sagittal sweep only matters if the root moment is carried medially through the ventral girdle to the symphysis.
   - **Relaxed, case one.** If the moment goes mainly dorsally to the skull (supracleithrum and posttemporal), the relevant sections are horizontal cuts of the cleithrum's dorsal limb. There the cleithrum is a thin plate bent about its weak axis. The author says their horizontal cuts are contaminated by pharyngeal bones and did not rest the verdict on them.
   - **Relaxed, case two.** If the moment is reacted by muscle and ligament before it reaches the midline, the near-midline minimum is irrelevant. That would *help* the claim.
   - **Load sharing: unknown.** Neither the claim nor this review measured how the load is shared between those paths.
2. **"Largest component = girdle."** Relaxed in §3. This is the assumption that breaks the 20 mm number.
3. **The fill fraction is mineralised bone.** The author flagged this already. Hollow or cartilaginous interiors would lower every value above, mine included.
4. **The size scale-up (×2.2–8).** The claim correctly keeps its headline unscaled.
   - Scaling would lift my 20 mm 0.57× to roughly 2.8–4.6×.
   - **The ×4.9–8 factor is not shown to be valid.** It assumes the 0.4 g design fish is a 40 mm fish and that bone section scales isometrically. I did not verify the mass–length relation. It is not an observation, and I did not search for it.

## 5. Evidence level

"Derived" is honest. The author labels every number as calculated on published measured geometry, and states the decoder's limits.

**The defect is not the label. It is the scope.** "Smallest girdle bending section" is stated as if it were established, but the estimator does not identify the girdle.

## 6. Counter-examples, regimes, and negative-search scope

- **Counter-example: the claim's own second fish (20 mm), once the girdle is tracked (§3d).**
- **Negative-search scope.** I did not search the literature for zebrafish girdle cross-sections. I worked only with the Nguyen et al. 2022 supplementary meshes:
  - Nguyen S.V. et al. 2022, *Front. Physiol.* 13:875866, PMC9204358. Supplementary DataSheet3/4: **full-text (data files decoded)**. Article text: not re-read by me; I rely on the claim author's full-text read for the 10.5 µm voxel size.
- **No published value for the medial girdle section.** I found none. My search was limited to that one dataset.

## 7. What I did not break

- The arithmetic.
- The decoder's vertex output.
- The 24 mm fish's girdle clearance (1.8–7× when tracked).
- The conditional radial result (0.23–0.77×), which is plain arithmetic on assumed diameters.
- The author's own conclusion that the joint and radial load path is the open question.

**Reproduce.** Scripts are in `docs/research/fish/challenge-232/`. They need the author's `section.py` from commit `6cd6d61`.

```
python3 -I comp.py  <dir-with-section.py> DataSheet4.PDF.1.u3d.pos.npz 4500,6900,4000,7500 1300,...,2500 15
python3 -I track.py <dir> DataSheet4.PDF.1.u3d.pos.npz 4500,6900,3000,7500 1300,...,2800 5500,6700
python3 -I track.py <dir> ds31_frame.npz 5500,8600,3000,6200 2600,...,3800 7000,8300
```

`ds31_frame.npz` is produced by the author's `frame_sl20.py`.

```swarm-challenge
{"claim_id": 232, "outcome": "weakened", "reason": "Arithmetic and mesh decoding reproduce, but the 'min over planes of the largest component' estimator does not track bone identity: in the 20 mm fish the claimed 5.4e-3 mm^3 component sits at mid-depth and persists to within ~50 µm of the trunk-derived midline (very probably a median pharyngeal/branchial element, my inference), and the ventral band continuous with the girdle has a calculated minimum of 3.8e-4 to 9.9e-4 mm^3 (0.22-0.57x the requirement, <=1.3x summing fragments), while the 24 mm fish survives at 1.8-7x when tracked.", "corrected_value": "tracked medial girdle section modulus, calculated from published mesh vertices, unscaled: 24 mm SL 3.1e-3 to 1.2e-2 mm^3 (1.8-7x Z_req 1.73e-3); 20 mm SL 3.8e-4 to 9.9e-4 mm^3 single section (0.22-0.57x), 1.5e-3 to 2.25e-3 mm^3 summed fragments (0.87-1.3x); minimum girdle section across both fish therefore unresolved, spanning the requirement", "depends_on": ["S7: worst-case root moment 1.08e-4 N·m (V=3 m/s, n=3, C_L=0.78, AR=9, m=0.4 g, half-width 2.5 mm), recomputed here as 1.081e-4", "S7-D: yield stress 62.6 MPa (Fiedler et al. 2019 herring bone, tensile), giving Z_req 1.727e-3 mm^3", "Nguyen et al. 2022 Suppl. DataSheet3/4 surface meshes as faithful bone geometry (Europe PMC, SHA prefixes 1617b074648c2127 / ead58b4f8cf9cce9)", "author's U3D vertex decoding (pos.py, commit 6cd6d61), reproduced identical vertex counts", "author's section.py fill/closing method (+4-14% bias on synthetic shapes), used unchanged", "20 mm frame and 10.5 µm/voxel calibration from author's frame_sl20.py", "trunk-vertex midline estimate (z 8-14 mm): y~3720-3840 µm (20 mm), ~2870-2900 µm (24 mm)", "my inference of bone identity by position: ventral band x 5.5-6.7 mm (24 mm) and x 7.0-8.3 mm (20 mm) is the girdle; mid-depth component at x 6.3-6.9 mm near the 20 mm midline is not", "load-path assumption shared with the claim: root moment carried medially through ventral girdle sections in sagittal planes"]}
```
