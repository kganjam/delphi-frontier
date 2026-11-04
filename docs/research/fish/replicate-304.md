# Replication of claim 232 (S7-D-D girdle section): independent re-derivation

Date: 2026-11-04. Scripts, figures and raw outputs: `docs/research/fish/replicate-304/`.

**About the claim number.** The task asked me to replicate claim 232, the S7-D-D girdle section. It also told me to write this file as `replicate-304.md` and to tag the result with `claim_id 304`. I did both as instructed. The quantity replicated here is the S7-D-D girdle section modulus. If 304 is meant to be a different claim, this file is filed under the wrong ID.

## 0. Independence: I was partly exposed to earlier results

I must disclose this first, because it limits what my result is worth.

1. **What I saw before deriving anything.** To find the inputs, I ran `git show --stat` on the branch named in the task, `claude/s7-d-girdle-section-4o9w38`. That branch is **another agent's replication of claim 232**, not the original claim. Its commit message printed with the file list, and it says:
   - the earlier replicator's value, "narrowest cleithral-arm section Z_min ~1.05e-3 mm^3 (d_eq ~0.22 mm) at 24 mm SL";
   - the recorded value, "3.6-6.8e-3 mm^3".
2. **What else I read.** I then read the first 40 lines of that branch's `replicate-232.md`, looking for the problem statement. Those lines contain its headline: the cleithral arm above the fin base, bent about the AP axis, TL/SL = 1.23, and an isometric scaling table. As soon as I saw that, I stopped reading it, and I did not open its scripts.
3. **Where I took the problem statement from.** I read only S7 (`S7-organ.md`, branch `claude/s7-organ-pectoral-girdle-xlxpkt`) and S7-D (`S7-deepen.md`, branch `claude/deepen-s7-pectoral-girdle-b6j2hx`).
4. **When I opened the original claim.** I did not open S7-D-D (`S7-D-deepen.md`, branch `claude/deepen-s7-d-sensitive-input-tbjg48`) until my own numbers in §3 were fixed.

**What is independent.**
- The U3D decoder and the mesh slicer are my own code.
- The scale calibration is my own.
- The arithmetic is my own.

**What is not independent.**
- **The data.** I used the same Nguyen et al. 2022 mesh as both earlier agents. The DataSheet4 SHA-256 prefix is `ead58b4f8cf9cce9`, identical to the one S7-D-D quotes.
- **My choice of section.** I chose the dorsal cleithral limb, bent about the AP axis. That is the same choice as the earlier replicator's, and I already knew their number when I made it. My close agreement with that replicator (1.0 vs 1.05 × 10⁻³ mm³) is therefore **weak evidence**: the choice of section may have been anchored. My agreement with the original claim's own section definition (§4) was derived blind to the details of that section, though not to its headline range.

## 1. Result

**Calculated from a published µCT surface mesh. Not an observation.**

The section is the narrowest bending section of the zebrafish **cleithrum's dorsal limb**. It lies between the fin base and the region where the supracleithrum overlaps the cleithrum, and it is bent about the anteroposterior (AP) axis. At the specimen's own size (24 mm SL):

- **Section modulus:** **Z_min ≈ 1.0 × 10⁻³ mm³.** Left/right and the two unit calibrations together span 0.90–1.16 × 10⁻³. Adding a ±25% allowance for surface position widens this to about 0.7–1.45 × 10⁻³ mm³.
- **Solid-equivalent diameter:** **d_eq ≈ 0.22 mm** (range 0.19–0.245 mm).
- **Cross-sectional area at the minimum:** about 0.038–0.039 mm².

**The original claim's own section.** S7-D-D's definition is sagittal planes cut medial to the fin base through the ventral girdle. Applied to the exact mesh faces, it gives a minimum largest-section Z of **≈ 3.8 × 10⁻³ mm³**, and typical values of 1–2 × 10⁻² mm³ (§4). That falls inside the recorded 3.6–6.8 × 10⁻³ mm³.

## 2. Inputs, with source and read-level

| Input | Value | Source | Read-level |
|---|---|---|---|
| Surface mesh of a 24 mm SL zebrafish whole-body skeleton | U3D mesh "obj" in Supplementary DataSheet4.PDF, 3D annotation 1: 574,708 vertices, 1,153,000 faces | Nguyen, Lanni, Xu, Michaelson & McMenamin 2022, *Front. Physiol.* 13:875866, PMC9204358. Supplementary ZIP obtained via `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9204358/supplementaryFiles` (88.4 MB) | full-text (primary data file, decoded by me) |
| Identity of DataSheet4 as the 24 mm SL fish | Supplementary Figs 5–8 are captioned 12, 16, 20 and 24 mm SL. **My inference:** DataSheet1–4 map to Figs 5–8 in order. This is supported by DataSheet4's body length coming out at about 25 mm if 1 unit = 1 µm. | Paper XML | full-text (paper XML via Europe PMC `fullTextXML`) |
| Scan resolution | 10.5 µm | Nguyen 2022, Methods | full-text |
| Mesh units | Not stated in the file. Calibrated by me, see §3c: 0.956–1.000 µm per unit | My measurement on the mesh | calculated |
| Worst-case root moment per fin, M | 1.081 × 10⁻⁴ N·m | S7 §3c, restated in S7-D | full-text (S7 file). Its inputs are themselves assumed or search-summary; see S7. |
| Bone yield stress | 62.6 MPa (herring intermuscular bone, tensile) | Fiedler et al. 2019, as reported in S7-D §3b | S7-D's read of the paper is full-text. My own read is listing-level only: I did not re-read Fiedler. |
| MorphoSource raw scans (project 000415918) | — | www.morphosource.org | could-not-access: proxy CONNECT returned 403 |

## 3. Method and arithmetic

### 3a. Decoding the mesh (my own decoder)

1. **Extracting the streams.** I extracted the `/Subtype /U3D` streams with `pypdf` (`extract2.py`). Each PDF holds two streams: the whole body and the whole head.
2. **Block structure** (`blocks.py`, `hdr.py`).
   - A modifier chain "obj" holds a CLOD mesh declaration with mesh attributes = 1, which means normals are excluded.
   - It is followed by a single CLOD Base Mesh Continuation block, 0xFFFFFF3B.
   - That block contains 1,153,000 faces and 574,708 positions, with no normals, colours or texture coordinates.
   - There are no progressive-resolution blocks.
3. **Positions.** These are raw F32 triplets. They are written as byte symbols over a full-range arithmetic coder, so they read as plain little-endian floats.
4. **Faces** (`dec2.c`).
   - Each face starts with a shading ID coded in an *adaptive* context. Its position indices exceed the 0x3FFF static-context limit, so they are coded as U32 values made of four byte symbols.
   - I wrote a Witten–Neal–Cleary style decoder with a 16-bit low/high register. It reads bits LSB-first within each byte, assembles the code word MSB-first, and skips underflow bits. Byte symbols are bit-reversed.
   - It adds every decoded symbol to the adaptive histogram, *including the escape*.
   - The histogram is rescaled when its total exceeds 8191 by halving the non-escape symbol, rounding up; the escape frequency is not halved. I found this rule by search over 48 variants. Without rescaling, decoding desyncs at face 8,190.
5. **Validation (calculated).**
   - All 1,153,000 × 3 indices are below the position count.
   - Every one of the 1,729,500 edges is shared by exactly 2 faces, so the body mesh is a closed 2-manifold.
   - The decoder stops 9 bytes before the end of the block.
   - The head mesh decodes with zero out-of-range indices, and 99.9% of its edges are manifold.

### 3b. Locating the bone and choosing the section

- **Orientation**, from renders (`render.py`) and slices:
  - z runs anteroposterior: snout at z ≈ 0, caudal fin rays to z ≈ 30,956.
  - Low x is dorsal (neural side) and high x is ventral (ribs, anal and pelvic fins).
  - The midline is at y ≈ 2,900.
  - The pectoral fin is folded back along the flank; its base is near z ≈ 5,600–6,100 and x ≈ 5,900–6,300.
- **Identification** (my inference from shape and continuity; the mesh is not segmented by bone).
  - The **cleithrum** is the large curved plate behind the opercle (`render_dorsal_girdle_right.png`).
  - Its dorsal process tapers to a tip at x ≈ 3,450.
  - A separate oblique band, running from the posttemporal region down to the cleithrum, is the **supracleithrum**.
  - On the right side it overlaps the cleithrum at about x ≈ 3,800–4,200. On the left side the overlap is at x ≈ 3,800–3,900, where the two sections merge in `xslices_left.png`.
- **Load case.** This is S7's, taken as given:
  - the fin is spread laterally, so its span runs along y, and lift acts dorsoventrally, along x;
  - the root moment is therefore a vector along z.
  - The dorsal cleithral limb runs roughly along x, so it carries this moment as out-of-plane bending.
  - The section is the plane normal to x, and I is taken about the centroidal axis parallel to z, so the bending depth lies along y.
- **Which section is "the minimum".** It is the narrowest section between the fin base and the supracleithral overlap.
  - Above the overlap, the tapering dorsal tip (Z falls to 3.5 × 10⁴ u³ at x = 3,500) is excluded. There the load has already passed to the supracleithrum.
  - This exclusion is **my modelling choice**.

### 3c. Section properties (`slice.py`, `secprops.py`, `cleith_fine.py`)

**Method.**
1. Intersect the exact triangles with the plane x = c.
2. Fill the outlines by even–odd scanline at a 1-unit grid.
3. Label the connected regions and track the cleithrum region from slice to slice.
4. Compute A, the centroid, I_z = Σ(y − ȳ)² dA, c = max |y − ȳ|, and Z = I_z/c.

The fill uses closed contours from real faces. No slab or morphological closing is needed.

**Finest sampling, 25-unit steps** (calculated, in mesh units):

| Side | x at minimum | A (u²) | y-depth × z-width (u) | I_z/c = Z_min (u³) |
|---|---|---|---|---|
| Right | 4,425 | 39,100 | 268 × 325 | 1.161 × 10⁶ |
| Left | 4,125 | 38,162 | 273 × 283 | 1.027 × 10⁶ |

**Checks.**
- Grid size 2 u versus 1 u changes Z by less than 0.3% (right side at x = 4,400: 1.164 vs 1.163 × 10⁶).
- The limb axis is tilted from x by 5.9° (right) and 12.2° (left), judged from the centroid track. An x-normal cut therefore overstates the perpendicular section slightly, by ≤ 5% in Z (my estimate). I did not apply this as a correction; it is included in the uncertainty.

**Unit calibration.**
- The paper labels this fish 24 mm SL.
- On the mesh, I measured snout tip (z_min = −19) to the posterior margin of the hypural plates at z ≈ 25,100 ± 200 (`render.py` tail view). That gives SL_mesh ≈ 25,100 u.
- Total length is z_max − z_min = 30,956 u, so TL/SL = 1.233.
- **Two readings of the scale:**
  - (a) units are µm (s = 1.000 µm/u), which implies SL = 25.1 mm;
  - (b) the labelled SL is exact (s = 24/25,100 = 0.956 µm/u).
- The paper sampled a size about every 0.5 mm, so the labelled SL is nominal. I keep both readings as the scale bracket.

**Arithmetic.** Z_mm³ = Z_u × s³ × 10⁻⁹ mm³/µm³.

| Side | s = 1.000 | s = 0.956 (s³ = 0.874) |
|---|---|---|
| Right | 1.161 × 10⁻³ mm³ | 1.015 × 10⁻³ mm³ |
| Left | 1.027 × 10⁻³ mm³ | 0.898 × 10⁻³ mm³ |

- Central value: **Z_min ≈ 1.0 × 10⁻³ mm³**, spread 0.90–1.16 × 10⁻³.
- **Surface allowance.** The isosurface threshold is unstated. I allow ±1 voxel (10.5 µm) per face on a 270 µm depth, plus MeshLab simplification to about 26 µm edges. That is roughly ±8% in depth and ±6% in width, so about ±25% in Z (my estimate, not measured). The range widens to about **0.7–1.45 × 10⁻³ mm³**.
- d_eq = (32 Z/π)^(1/3):
  - Z = 1.0 × 10⁻³ gives 0.217 mm;
  - Z = 0.7 × 10⁻³ gives 0.192 mm;
  - Z = 1.45 × 10⁻³ gives 0.245 mm.

**Compared with S7-D's requirement** (calculated, using S7/S7-D inputs as given). Z_req = M/σ_y = 1.081 × 10⁻⁴ N·m / 62.6 × 10⁶ Pa = 1.727 × 10⁻¹² m³ = **1.73 × 10⁻³ mm³**.

| Case | Z | Ratio to Z_req |
|---|---|---|
| Unscaled, at 24 mm SL | 1.0 × 10⁻³ mm³ (range 0.7–1.45) | **0.58** (0.41–0.84): the dorsal limb alone would yield |
| Scaled to 40 mm, read as SL: ×(40/24)³ = 4.63 | ≈ 4.6 × 10⁻³ mm³ | ≈ 2.7 |
| Scaled to 40 mm, read as TL: SL = 40/1.233 = 32.4 mm, ×(32.4/24)³ = 2.47 | ≈ 2.5 × 10⁻³ mm³ | ≈ 1.4 |

The scaled rows assume isometry, which is an assumption.

## 4. Comparison with the recorded value (made after §3 was fixed)

**The claim.** S7-D-D (`S7-D-deepen.md`, branch `claude/deepen-s7-d-sensitive-input-tbjg48`) records:

> "girdle section modulus about the AP axis, min over planes medial to the pectoral fin base: 3.6e-3 to 6.8e-3 mm^3 (24 mm SL)"

**Their method** (the author's description):
- sagittal planes, normal to y, at y = 1.3–2.5 mm;
- a box of x 4.5–6.9 mm and z 4.0–7.5 mm around the ventral girdle;
- **vertex positions only**, because their decoder desynced at face 8,190;
- slabs of ±15 or ±30 µm, rasterised at 10 µm, closed by 30 µm and filled;
- the "largest single section" in each plane, then the minimum over planes.

**Reproducing their definition with exact faces** (`sag.py`, calculated). Using the same box and bending axis (depth along x), I cut planes every 100 µm on both sides:
- Left side, y = 1,300–2,500: minimum largest-section Z = **3.81 × 10⁶ u³** at y = 2,400, and 5.78 × 10⁶ at y = 1,800. Typical values are 1–2 × 10⁷ u³.
- Right side, y = 3,500–4,700 (mirror of the left): minimum 1.34 × 10⁷ u³.
- At s = 0.956–1.000 the left minimum is **3.3–3.8 × 10⁻³ mm³**. That is consistent with the recorded 3.6–6.8 × 10⁻³ mm³.

Two caveats from my own figure (`sagittal_left.png`):
- At y = 2.1 and 2.4 mm, the "largest section" is a blob at x ≈ 4.75–4.95 mm, away from the ventral girdle band at x ≈ 5.5–6.3 mm. It is probably a pharyngeal or branchial element, not girdle (my inference).
- So the estimator can pick non-girdle bone. S7-D-D itself flags this possibility for its horizontal cuts.

**Where the two derivations differ, and why.**
- **The number, as defined.** Under the recorded definition I reproduce it (≈ 3.8 × 10⁻³ vs 3.6–6.8 × 10⁻³). The vertex-only method did not distort the number badly.
- **The governing section.** The recorded definition only examines the ventral, medial load path. The dorsal cleithral limb also carries the fin's AP-axis moment, towards the supracleithrum and skull, and it is **3.5–7× weaker**: 1.0 × 10⁻³ against 3.6–6.8 × 10⁻³.
- **What each author claims, and what I infer.**
  - S7-D-D's verdict is that the girdle clears the requirement "in all but one unscaled row".
  - My inference: at the measured 24 mm size, the dorsal limb by itself does **not** clear it (ratio 0.58).
  - After isometric scaling to 40 mm it does (1.4–2.7×).
  - The ventral and dorsal paths act in parallel. How the moment divides between them was not computed, by either author or by me.
  - S7-D-D's qualitative conclusion therefore survives *if* the ventral loop carries most of the moment, or once the fish is scaled up. Its statement that the *minimum* girdle section is 3.6–6.8 × 10⁻³ mm³ does not hold for the girdle as a whole.
- **The earlier replication.** Its headline (Z_min ≈ 1.05 × 10⁻³ mm³, cleithral arm) agrees with mine, but see §0: I knew it in advance.

**Verdict: DISAGREE** on the value of the minimum girdle bending section (1.0 × 10⁻³ vs 3.6–6.8 × 10⁻³ mm³). **AGREE** with the recorded number as the minimum over *its own stated planes* (ventral sagittal cuts).

## 5. What this does not establish

- **No observation was made.** Everything here is calculated on a decimated isosurface whose threshold is unstated.
- **Hollowness.** Interiors were taken as solid bone. Cartilage or marrow would lower every Z.
- **Bone identities** (cleithrum, supracleithrum, opercle) are my inference from shape. The model is not segmented.
- **Sample size.** This is one fish (n = 1). I did not use the separate head mesh (DataSheet4, annotation 2) as a cross-check: it decodes, but it uses a different, uncalibrated unit, and I ran out of scope.
- **Excluded regions.** The proximal radials and scapulocoracoid were not isolated. At the fin base they merge in the mesh (x ≳ 5,600), as S7-D-D also reported.
- **Load sharing.** Torsion in the ventral arm and the division of moment between the dorsal and ventral paths were not computed.
- **Scaling** to the 40 mm design fish assumes isometry, and "40 mm" in S7 is ambiguous between SL and TL.

## 6. Negative or failed access (scope stated)

- **MorphoSource:** one curl request to the home page, refused with proxy CONNECT 403.
- **ECMA-363 specification:** not fetched. The decoder was written from my own knowledge and validated only by the topology checks in §3a.

## Reproduce

1. Fetch the Europe PMC `supplementaryFiles` ZIP for PMC9204358 into an empty directory and unzip it.
2. Extract the streams: `python3 -I extract2.py DataSheet4.PDF ds4`.
3. Find the face offset: `python3 -I hdr.py ds4_1.u3d`. The face offset is the block start + 33 + 12·P.
4. Build and run the face decoder: `gcc -O2 dec2.c -o dec2 && ./dec2 ds4_1.u3d 6897157 1153000 574708 0 ds4_1.F.bin 8191`.
5. Save `ds4_1.V.npy` and `ds4_1.F.npy` (see `load.py`).
6. Compute the cleithrum sections:
   - `python3 -I cleith_fine.py ds4_1 R out 25 1 4700 4200 4400,5750`
   - `python3 -I cleith_fine.py ds4_1 L out 25 1 4400 3950 1250,5800`
7. Compute the sagittal check: `python3 -I sag.py ds4_1 1300,...,2500 sagL`.

```swarm-replication
{"claim_id": 304, "my_value": "1.0e-3 mm^3 (range 0.7-1.45e-3; d_eq 0.22 mm) narrowest dorsal-cleithral-limb section modulus about the AP axis at 24 mm SL", "agrees": false,
  "note": "Independent face-exact decode of the same Nguyen 2022 mesh reproduces the recorded 3.6-6.8e-3 mm^3 only on its own ventral sagittal planes (I get ~3.3-3.8e-3), but the dorsal cleithral limb carrying the same AP-axis moment is 3.5-7x weaker (~1.0e-3 mm^3, 0.58x Z_req unscaled); I was exposed to a prior replication's 1.05e-3 headline before deriving, so agreement with it is weak evidence."}
```
