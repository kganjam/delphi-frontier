# Replication of claim 232 (S7-D-D): the zebrafish pectoral girdle section, derived independently

Date: 2026-11-04. Scripts and figures: `docs/research/fish/replicate-232/`.

**Independence statement.** Before deriving anything, I read only the problem statements: S7 (`S7-organ.md`, branch `claude/s7-organ-pectoral-girdle-xlxpkt`) and S7-D (`S7-deepen.md`, branch `claude/deepen-s7-pectoral-girdle-b6j2hx`). I did not open the S7-D-D branch (`claude/deepen-s7-d-sensitive-input-tbjg48`) until §6, after my own numbers were fixed. Before that, the only thing I looked at on that branch was its list of file names.

S7-D did give me two things up front:

- the source it suggested: Nguyen et al. 2022 µCT, with the MorphoSource scans unreachable;
- its threshold table.

I used the same primary dataset the original agent probably used. "Independent" here means an independent decoder, an independent choice of section and independent arithmetic. It does not mean independent data.

## 1. Result (headline)

**Computed from published µCT surface meshes. Not a direct observation.** The narrowest bending section of the zebrafish **cleithral arm** above the pectoral-fin base has these values, at the measured 24 mm SL size:

- Section modulus about the anteroposterior (z) axis: **Z_min ≈ 1.0–1.2 × 10⁻³ mm³**.
- Solid-equivalent diameter d_eq = (32 Z/π)^(1/3): **≈ 0.22 mm**, range 0.22–0.23 mm.

The cleithral arm is the vertical cleithrum plate dorsal to the fin base. The load case is a root moment about the anteroposterior axis, which bends that plate out of its plane.

The left and right sides agree to within 2%.

An independent cross-check on the separate head mesh gives d_eq,min ≈ 0.25–0.31 mm. That figure carries a ±7% unit-scale uncertainty, explained in §3. The two meshes disagree by 15–35% in d_eq, and I report both.

Scaled isometrically (Z ∝ L³) to S7's 40 mm design fish:

| S7's "40 mm" read as | Scaling factor | Z | d_eq |
|---|---|---|---|
| SL | ×(40/24.25)³ = 4.49 | ≈ 4.7 × 10⁻³ mm³ | ≈ 0.36 mm |
| Total length (TL/SL = 1.23 in this mesh, so SL = 32.4 mm) | ×2.39 | ≈ 2.5 × 10⁻³ mm³ | ≈ 0.29 mm |

**Value: Z_min = 1.05 × 10⁻³ mm³ (range 1.0–1.2 × 10⁻³ body mesh; 1.5–2.9 × 10⁻³ head mesh) at 24 mm SL, i.e. d_eq ≈ 0.22 mm (0.22–0.31 mm across meshes).**

## 2. Inputs, with source and read-level

| Input | Value | Source | Read-level |
|---|---|---|---|
| µCT surface models of a 24 mm SL zebrafish (whole body and whole head) | U3D meshes embedded in Supplementary Data Sheet 4 (3D PDF), objects 32 (body: 574,708 vertices, 1,153,000 faces) and 33 (head: 250,002 vertices, 500,000 faces) | Nguyen, Lanni, Xu, Michaelson & McMenamin 2022, *Front. Physiol.* 13:875866, PMC9204358, supplementary files via Europe PMC `supplementaryFiles` endpoint | full-text (paper XML) + primary data (meshes decoded by me) |
| Scan resolution 10.5 µm; SkyScan 1275; surfaces made in Amira 6.5 (Segmentation Editor, Generate Surface) | — | same paper, Methods | full-text |
| Which data sheet is which size | Supplementary Figs S5–S8 = 12, 16, 20, 24 mm SL. I take DataSheet4 = 24 mm; the body mesh is the longest fish, consistent with that. | same paper | full-text + my inference |
| Unit scale of the body mesh | No unit metadata in the PDF or U3D model nodes (identity transforms). I measured SL in the mesh as 25.06 k units: snout tip at z = −19, posterior hypural margin at z ≈ 25,040 (`b_hyp.png`). Against the nominal 24 mm category (24.0–24.5 mm fixed SL), k = 0.958–0.978 µm/unit. I use **0.968**; k = 1.0 (plain µm) is the upper bracket. | calculation | — |
| Unit scale of the head mesh | Unknown. A width-profile fit gave ≈12.8 body units per head unit. Scaled ICP onto the body mesh converged at 11.3–12.9 depending on the start, so the fit is not unique. Head and body may be different individuals, or differ in jaw pose. I bracket it at **11.3–12.9 µm/unit**. | calculation | — |
| Bending load case | Fin abducted laterally, lift dorsoventral, so the root moment is about the anteroposterior (z) axis. This is S7's load case. | S7-organ.md §1, §3 | full-text (repo) |
| Requirement to compare against (not my derivation) | Z_req = 1.73 × 10⁻³ mm³ (M = 1.08 × 10⁻⁴ N·m, σ_y = 62.6 MPa, no SF). With SF 1.5: 2.59 × 10⁻³ mm³. | S7 §3c; S7-D §3b (Fiedler et al. 2019 herring bone) | full-text (repo); I did not re-check Fiedler |

**Access notes.** These hosts were unreachable from this session: MorphoSource (raw volumes), zenodo, figshare, ecma-international.org (the U3D spec) and archive.org. I could not clone the open-source U3D library from GitHub (outside this session's scope). The commercial Aspose.3D library failed to load the U3D streams. So I wrote the decoder myself (§3).

## 3. Method and arithmetic

### 3a. Decoding the meshes (my own decoder: `u3dwalk.py`, `base.py`, `ac.c`, `runfaces.py`)

- In seven of the eight streams, the whole mesh is a single U3D **CLOD base mesh** block (min resolution = max resolution). Normals are excluded (attribute 1), and there are no colours or texture coordinates.
- The base-mesh vertex positions are raw float32 values, and I read them directly.
- The faces are arithmetic-coded: an adaptive context for the shading ID, and 32-bit indices passed through the coder. I reimplemented the ECMA-363 bitstream decoder from memory, since the spec was unreachable: the 16-bit range coder with underflow, static and dynamic contexts, and the escape and halving rules.
- **Validation**, for all 7 base meshes:
  - every index is in range;
  - the decoder consumes the block to within 57–72 bits of padding (for example, 48,000,310 of 48,000,376 bits);
  - every vertex is used;
  - 99.9–100% of edges are shared by exactly two faces. The 24 mm body mesh is fully 2-manifold: 1,729,500 edges, all shared by two faces.

  A wrong decoder would desynchronise within a few faces. The streams in DataSheet1 (12 mm) use progressive-mesh blocks, which I did not decode; they are not needed here.

### 3b. Choosing the section

I located the bones on rendered views (`b_latL.png`, `b_ventL.png`, `render.py`). Axes: z is anteroposterior, x is dorsoventral (ventral is +), y is lateral.

The cleithrum is a curved plate whose broad face points laterally:

- a dorsal spine at z ≈ 5.8–6.0 mm;
- a posterior lamina at z ≈ 6.0–6.25 mm;
- a ventral limb at x ≈ 5.5–6.3 mm.

The postcleithrum is a separate slender rod. The fin-ray heads articulate at z ≈ 6.0–6.5 mm, y ≈ 0.9–1.25 mm.

Parasagittal planes (normal y) cut the cleithrum **lengthwise**, which is not a beam section. Here is my inference, which is a modelling choice and not an observation. A root moment about the z axis bends the vertical cleithral plate out of its own plane. Its governing section is therefore a **horizontal cut (normal x)**, with the bending stress varying along y:

- I_z = ∫(y − ȳ)² dA
- c = max |y − ȳ|
- Z = I_z / c

I sliced the closed surface exactly (triangle–plane intersection), chained the segments into closed loops and filled them by even–odd nesting. I computed area and second moments with the polygon (Green's theorem) formulas (`slicer.py`, `secs.py`). Loops cut by the crop box were dropped, not truncated.

### 3c. Sections: body mesh, 24 mm SL, raw mesh units (k = 1)

Crop for the first block: z 5.5–6.23 mm. Left side y 0–2.0 mm; right side y 3.93–5.93 mm.

| x (mm below dorsal reference) | Left A (mm²) | Left Z (mm³) | Left d_eq (mm) | Right A | Right Z | Right d_eq |
|---|---|---|---|---|---|---|
| 4.0 | 0.0496 | 1.58e-3 | 0.252 | 0.0540 | 2.15e-3 | 0.280 |
| 4.2 | 0.0403 | **1.15e-3** | **0.227** | 0.0528 | 1.81e-3 | 0.264 |
| 4.4 | 0.0526 | 1.91e-3 | 0.269 | 0.0398 | **1.17e-3** | **0.228** |
| 4.6 | 0.0660 | 2.58e-3 | 0.297 | 0.0435 | 1.43e-3 | 0.244 |
| 4.8 | 0.0857 | 3.76e-3 | 0.337 | 0.0526 | 1.86e-3 | 0.267 |
| 5.0 | 0.111 † | 7.06e-3 † | 0.416 † | 0.0664 | 2.66e-3 | 0.300 |
| 5.2 | 0.138 † | 9.49e-3 † | 0.459 † | 0.0962 | 5.06e-3 | 0.372 |

† These sections include the postcleithrum loop, so they overstate the cleithrum alone. They are not used for the minimum.

Rows x = 4.8–5.2 come from a wider crop: z 5.15–6.8 mm, left y 0–2.3 mm, right y 3.63–5.93 mm. At x ≥ 5.4 mm the cleithrum runs out of every crop I tried and merges into the ventral girdle, so I report no value there.

**Unit conversion.** Z scales as k³ and d as k. At k = 0.968, Z = 0.907 × table value:

- left: 1.15e-3 → **1.04e-3 mm³**, d_eq 0.220 mm;
- right: 1.17e-3 → **1.06e-3 mm³**, d_eq 0.221 mm.

Across the full bracket k = 0.958–1.0: **Z_min = 1.01–1.17 × 10⁻³ mm³**, d_eq = 0.218–0.228 mm.

### 3d. Cross-check: head mesh (DataSheet4 object 33), horizontal sections x = 360–480 head units

Narrowest d_eq: left 24 units at x = 390, right 22 units at x = 390 (`h_B_L.png`). Section shapes match the body mesh: an L/hook-shaped plate about 50 × 12 units.

- At 11.3–12.9 µm/unit: d_eq,min = **0.25–0.31 mm**.
- Z = π d³/32 = **1.5–2.9 × 10⁻³ mm³**.

This is 15–35% higher in d_eq than the body mesh. Two explanations are possible, and I cannot tell which applies:

- the head-mesh scale is uncertain (at the 10.5 µm voxel size it would give 0.23–0.25 mm, close to the body mesh);
- the head mesh may be a different individual.

### 3e. Comparison with the requirement

All of this is calculation:

| Case | Z | Ratio to Z_req = 1.73e-3 | Ratio to Z_req with SF 1.5 = 2.59e-3 |
|---|---|---|---|
| Measured size (24 mm SL), body mesh | 1.05e-3 | 0.61× | 0.41× |
| Scaled to 40 mm (40 = SL) | 4.7e-3 | 2.7× | 1.8× |
| Scaled to 40 mm (40 = TL) | 2.5e-3 | 1.45× | 0.97× |

The 24 mm fish is not the 0.4 g design fish. So only the scaled rows answer S7's question, and they rest on isometric scaling, which is an assumption.

## 4. Uncertainty and what this does NOT establish

- **Section choice dominates.** The answer depends on which element and plane carry the moment.
  - Parasagittal cuts through the ventral girdle (my exploratory run, `a.json`, not adopted) gave Z of order 10⁻² to 10⁻¹ mm³. Those cuts slice the cleithrum lengthwise and mix several bones.
  - The narrow cleithral arm is the weakest beam-like section I found on the dorsal load path.
  - The ventral path (girdle floor → symphysis) was not resolved into a clean section.
  - The proximal radials and scapula were **not resolved**. Section: **unknown**.
- **The mesh is a decimated isosurface**, with edges of about 26 µm, made with an unknown threshold. Wall thicknesses of about 100–150 µm span only 4–6 edges. The threshold could bias Z by tens of percent in either direction; I did not quantify this.
- **The section is assumed fully mineralised**, with no cartilage core.
- **Units are inferred from anatomy**, not metadata: ±2% for the body mesh, ±7% for the head mesh.
- **I identified the bones by position and shape**, not from a segmentation.
- **Only one fish per mesh**, so there is no individual variation.

## 5. Final value (stated before comparison)

**Z_min (cleithral arm, bending about the AP axis) = 1.05 × 10⁻³ mm³.**

- Range: 1.0–1.2 × 10⁻³ mm³ on the body mesh, and 1.5–2.9 × 10⁻³ mm³ on the head mesh.
- d_eq ≈ 0.22 mm (0.22–0.31 mm).
- This is at 24 mm SL, calculated from published µCT surface meshes.

## 6. Comparison with the recorded value (read only after §1–5)

The recorded S7-D-D result (`S7-D-deepen.md`, branch `claude/deepen-s7-d-sensitive-input-tbjg48`) states:

- the smallest girdle section in **sagittal planes medial to the fin base** has Z ≈ **3.6–6.8 × 10⁻³ mm³ at 24 mm SL** (and ≈5.4 × 10⁻³ at 20 mm SL), giving 2.1–3.9× the requirement before scaling;
- its secondary horizontal cuts gave 7.5 × 10⁻³ to 2.9 × 10⁻² mm³ at x = 4.4–5.4 mm. Its author flagged those as possibly including pharyngeal or branchial bones.

That agent also reports that its U3D face decoding failed after 8,190 faces, so it worked from vertex slabs. My decoder recovered all faces, so my sections are exact mesh slices.

**Verdict: DISAGREE on the number.** My governing section is 3.4–6.5× smaller than the recorded minimum. At the measured size it falls *below* the requirement (0.61×), where the recorded value is above it (2.1–3.9×).

My inference about the cause: the difference comes mainly from **which section is taken to govern**. The recorded value comes from sagittal cuts through the girdle base. Mine is the out-of-plane bending of the thin vertical cleithral plate, which the recorded horizontal sweep appears to have merged with neighbouring bones.

The two derivations **agree qualitatively**: after isometric scaling to a 40 mm fish, the bone section meets the requirement (mine by 1.45–2.7×, or 0.97–1.8× with SF 1.5). But in my derivation the margin is thin, and it depends on reading S7's 40 mm as SL rather than TL. It is not the comfortable 2–8× the recorded claim implies.

```swarm-replication
{"claim_id": 232, "my_value": "Z_min = 1.05e-3 mm^3 (range 1.0-1.2e-3 body mesh, 1.5-2.9e-3 head mesh), d_eq ≈ 0.22 mm (0.22-0.31), cleithral arm, bending about the AP axis, 24 mm SL; ≈2.5-4.7e-3 mm^3 scaled to 40 mm", "agrees": false,
  "note": "From the same Nguyen et al. 2022 3D-PDF meshes, fully decoded and sliced exactly, the narrowest girdle section (the vertical cleithral plate bending out of plane) is 3.4-6.5x smaller than the recorded 3.6-6.8e-3 mm^3 and below the 1.73e-3 mm^3 requirement at measured size; it passes only after isometric scaling to 40 mm (1.45-2.7x), so the recorded number disagrees while the qualitative conclusion survives with a much thinner margin."}
```
