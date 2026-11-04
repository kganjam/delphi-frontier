# S7-D-D: Deepening S7-D. Measuring the girdle section it left unknown

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.

**Parent:** `docs/research/fish/S7-deepen.md`, branch `claude/deepen-s7-pectoral-girdle-b6j2hx`, commit `1155115`. That file in turn deepens `S7-organ.md` (branch `claude/s7-organ-pectoral-girdle-xlxpkt`, commit `a61c9688`).

**Code and outputs:** `docs/research/fish/S7-D-deepen/`.

**Status of the numbers.** Every number below that comes from that code is a **calculation**. Some calculations are made on geometry that was itself measured: a published µCT surface model. That makes them derived from a measurement. None of them is a new observation. I scanned nothing and tested nothing mechanically.

---

## 0. What S7-D left open

S7-D found that S7's conclusion ("girdle bone strength is probably not the binding constraint") is insensitive to every modelled input: a factor-of-two error in any of them moves the required section by ≤27%. It found one exception, the **actual bending section of the girdle that receives the fin's root moment**. That input was never measured. S7 had only guessed it ("a few tenths of a mm").

S7-D verified that the actual section was the most sensitive input, by recomputing:

- Stress in a section goes as 1/size³. A factor-of-two error in that guess changes bone stress by ×8.
- Halving a 0.4 mm guess flips the verdict.

S7-D then gave a threshold the measurement had to beat. With the worst-case root moment M = 1.08×10⁻⁴ N·m per fin (V = 3 m/s, n = 3, C_L = 0.78, AR = 9, m = 0.4 g) and the measured herring yield stress σ_y = 62.6 MPa, the requirement is a solid-equivalent section d ≈ 0.26 mm. That is a section modulus **Z_req = 1.73×10⁻³ mm³** (calculated, §3 below).

S7-D could not reach the data that would settle it, the MorphoSource µCT scans. It recorded the gap as unknown.

## 1. Most sensitive input, confirmed again by recomputing

I reran S7-D's sweep (`S7-deepen.py` from commit `1155115`, unchanged) before attacking that input. It reproduces S7-D's table: M changes by ×0.47–2.06 and the required d by ×0.78–1.27 (calculated). The required d varies only as M^(1/3) and σ_y^(−1/3) (calculated). The comparison, though, is **Z_actual / Z_req**:

- Z_actual goes as (linear size)³ of the bone.
- So a factor-of-two error in the girdle section is a factor-of-eight error in the margin.
- A factor-of-two error in any modelled input moves the margin by at most about ×2, through M. In S7-D's sweep, M changed by ×0.47–2.06 for V and exactly ×2 for n.

The girdle section is still the input to attack.

## 2. How well established was it? (before this work)

- **Evidence level: assumption.** S7 did not measure it and gave no proxy for it, only a guess. S7-D reclassified it honestly but could not improve it.
- **Read-level of the data S7-D pointed to:** MorphoSource project 000415918 was *could-not-access*. I checked again today: CONNECT refused with 403 by this session's network policy.

## 3. Improving it: the girdle section measured from published µCT geometry

### 3a. A route to the geometry that S7-D did not try

Nguyen et al. 2022 (*Front. Physiol.* 13:875866) published, alongside the MorphoSource scans, **interactive 3D PDFs of segmented skeletons**. These are Supplementary Figures 5–8: whole head and whole body for 12, 16, 20 and 24 mm SL fish.

- **Read-level: full text.** The paper's HTML was fetched and text-extracted. In the methods, the models were "generated in Amira 6.5 using the Segmentation Editor and Generate Surface module", then "simplified using MeshLab" and converted to U3D. The scan resolution was 10.5 µm.
- **Frontiers file host blocked.** The Frontiers file host (`public-pages-files-2025.frontiersin.org`) is refused by this session's network policy.
- **Europe PMC worked.** The same supplementary files were downloaded through Europe PMC's supplementary-files service for PMC9204358: one ZIP, 88 MB, containing DataSheet1–4.PDF. **Read-level: full-text (the data files themselves).**

**The surface models themselves.** I extracted the embedded U3D streams from the PDFs (`pypdf`). I then decoded them with a minimal decoder written for this task (`u3d.py`), following the ECMA-363 arithmetic-coded bitstream as I know it.

I could not reach the ECMA-363 specification PDF or the reference decoder source:

- ecma-international.org: 403 and DNS refusal.
- I did not use GitHub-hosted decoders, because repositories outside this session's scope are off-limits.

What the decoder can and cannot do:

- **Validated.**
  - Block names decode as readable strings (`model`, `obj`, `DefaultMaterial`).
  - Vertex clouds decode as an anatomically correct zebrafish skeleton (Fig. 1).
  - Snout to caudal-fin base comes out at ≈24.5 mm in the file labelled 24 mm SL. In the file labelled 20 mm SL it is ≈19.5 mm, once 10.5 µm per unit is applied.
- **Failed.** Face connectivity decodes correctly only for the first 8,190 faces, then desyncs. The desync occurs exactly where the adaptive histogram's total frequency reaches 0x1FFF. Six rescale and freeze variants did not fix it, and the cause is **unknown**.
- **Consequence.** All measurements below use **vertex positions only**. Positions are decoded before any adaptive context is used, so they are not affected by the desync.

| File (paper's label) | Vertices | Units (my calibration) | Median edge length |
|---|---|---|---|
| DataSheet4 annot 1: 24 mm SL whole body | 574,708 | µm. Snout to caudal-fin base ≈24.5 mm, total length ≈30.9 mm | 26 µm |
| DataSheet3 annot 1: 20 mm SL whole body | 249,338 | voxels × 10.5 µm. Snout to caudal-fin base ≈19.5 mm | 2.7 voxels ≈ 28 µm |

### 3b. Method (calculated)

**Locating the girdle.** In both fish, I located the pectoral fin base by inspecting slices (Figs. 1 and 4):

- In the 24 mm fish the fin is folded back along the flank.
- In the 20 mm fish it is abducted.

**Choice of cut.** For a fin spread laterally (span along y) with lift along the dorsoventral axis (x), the root moment is a vector along the anteroposterior axis (z). Every girdle section that the moment must cross medial to the articulation must then resist bending about z. So I cut **sagittal planes** (normal to y), from the fin base towards the midline, through a box enclosing the ventral girdle:

- 24 mm fish: x 4.5–6.9 mm, z 4.0–7.5 mm.
- 20 mm fish: the equivalent box.

**From cut to section modulus.** In each plane:

1. Take the surface vertices within a slab of ±15 µm or ±30 µm.
2. Rasterise at 10 µm.
3. Close by 30 µm, fill the enclosed interiors, and label the connected sections.
4. For each section, compute area, I about the centroidal z-axis, Z = I/c, and the maximum inscribed thickness (`section.py`, `sweep.py`).

**Validation on synthetic shapes** (calculated, `section.py` main):

| Shape | Error in Z |
|---|---|
| Solid rod, d = 260 µm | +14% |
| Plates 60–200 µm thick | +4% to +14% |

So the method reads slightly high on ideal shapes.

**Slab-width bracket.** The two slab widths bracket two opposite artefacts:

- **±15 µm under-samples the outline.** Gaps defeat the fill, and an unfilled outline counts only its rim, so Z reads *low*. This is clearly visible in the sparser 20 mm mesh (Fig. 3, top row).
- **±30 µm reads high.** It smears walls that are oblique to the cut plane.

Where both agree, the section is robust: for example the ventral girdle limb of the 24 mm fish at y = 1.8 mm (Fig. 2, middle column), a continuous bony band about 0.1–0.15 mm thick.

### 3c. Result (calculated from measured geometry)

Required section moduli (calculated, `recompute.py`, M = 1.081×10⁻⁴ N·m):

| Yield stress basis | SF 1.0 | SF 1.5 |
|---|---|---|
| S7 floor, 25 MPa (assumed construction) | 4.33×10⁻³ mm³ (d 0.353 mm) | 6.49×10⁻³ mm³ |
| S7-D, herring mean, 62.6 MPa | **1.73×10⁻³ mm³ (d 0.260 mm)** | 2.59×10⁻³ mm³ |
| S7-D, lower 1-SD, 43.4 MPa | 2.49×10⁻³ mm³ | 3.74×10⁻³ mm³ |

Measured girdle section moduli are below. The minimum is taken over every sagittal plane from the fin base to near the midline:

- **24 mm fish:** y = 1.3–2.5 mm, which is 1.7–0.5 mm from the midline.
- **20 mm fish:** y = 2.6–3.7 mm, which is 1.4–0.3 mm from the midline.

| Fish | Slab | Min plane-sum Z | Min largest-single-section Z | Median largest-section Z | Max inscribed thickness of the largest section |
|---|---|---|---|---|---|
| 24 mm SL | ±15 µm | 6.68×10⁻³ (y 1.3 mm) | 3.56×10⁻³ (y 1.3 mm) | 1.28×10⁻² | 0.13–0.23 mm |
| 24 mm SL | ±30 µm | 1.51×10⁻² | 6.80×10⁻³ | 2.19×10⁻² | 0.14–0.28 mm |
| 20 mm SL | ±15 µm | 2.78×10⁻³ ⚠ under-sampled (Fig. 3) | 1.29×10⁻³ ⚠ | 4.50×10⁻³ | not used |
| 20 mm SL | ±30 µm | 1.10×10⁻² | 5.42×10⁻³ | 2.00×10⁻² | 0.24–0.29 mm (y ≥ 3.4 mm) |

All Z values are in mm³.

**Ratio of measured to required Z** (calculated, unscaled: the measured fish are *smaller* than the 0.4 g design fish):

| Estimator | vs 62.6 MPa, SF 1 | vs 43.4 MPa, SF 1.5 | vs S7's 25 MPa, SF 1 |
|---|---|---|---|
| 24 mm, ±15 µm, plane sum | 3.9× | 1.8× | 1.5× |
| 24 mm, ±15 µm, largest single section (most conservative valid estimator) | **2.1×** | **0.95×** | 0.82× |
| 24 mm, ±30 µm, largest single section | 3.9× | 1.8× | 1.6× |
| 20 mm, ±30 µm, largest single section | 3.1× | 1.45× | 1.25× |
| 20 mm, ±30 µm, plane sum | 6.4× | 2.9× | 2.5× |

I excluded the 20 mm ±15 µm rows, which give 0.30–1.6×. Fig. 3 shows they are a sampling artefact: open outlines that were not filled. I did not treat them as a measurement.

**Size scaling (calculated, isometry assumed).** The design fish is "40 mm" in S7, which does not say whether that is SL or total length. Scaling Z ∝ L³ to 40 mm multiplies the measured Z by:

| Fish | If 40 mm is total length | If 40 mm is SL |
|---|---|---|
| 24 mm fish | ×2.2 | ×4.6 |
| 20 mm fish | ×4.9 | ×8.0 |

After the smallest of these scale-ups, the single worst row in the table becomes ≈2.1×: 24 mm fish, largest section, 43.4 MPa, SF 1.5.

**Secondary cut (horizontal planes).** I also cut horizontal planes (normal to x), bending about z with stress varying along y (`hsweep.py`). These gave largest-section Z = 7.5×10⁻³ to 2.9×10⁻² mm³ at x = 4.4–5.4 mm. That is also above the requirement. However, the largest sections there sit at y = 1.4–2.5 mm, and some of them are probably medial pharyngeal or branchial bones rather than girdle (*my inference*). I report them, but I do not rest the verdict on them.

### 3d. What the geometry could NOT resolve: the proximal radials

S7-D's anatomical point was that the moment first meets the four proximal radials and the scapula, and only then the cleithrum (Keer et al. 2019, full text, as cited in S7-D). This mesh did not let me isolate them:

- At the fin base, the scapulocoracoid, radials and fin-ray heads merge into one contour (Fig. 4). The likely causes are the Amira threshold, the 10.5 µm voxels and MeshLab simplification to about 26 µm edges.
- I found two separate rods about 0.10–0.15 mm in diameter running dorsoventrally near z ≈ 6.6 mm, y ≈ 1.3–1.45 mm in the 24 mm fish. From geometry alone I **cannot tell** whether they are proximal radials or the first pleural ribs, so I make no claim.

**Conditional calculation.** *If* the full root moment had to pass through four separate radial rods of 0.10–0.15 mm, each bending independently, their combined Z would be 4πd³/32 = 3.9×10⁻⁴ to 1.3×10⁻³ mm³. That is 0.23–0.77× the S7-D requirement (calculated): the bone would fail there.

Whether the radials are loaded that way is a question about the joint's load path. It is not answered here.

- **Radial cross-section: unknown.** I tried this mesh and one web search (scope below).
- **What would settle it:**
  - the raw MorphoSource volumes at 10.5 µm, not the decimated surface; or
  - a diceCT/µCT scan of a dissected adult fin base at ≤5 µm.
  With the volumes, segmenting the four radials is about one analyst-day in 3D Slicer (estimate). MorphoSource needs to be allowed in this session's network settings, and it may require a login.

## 4. Recomputation and verdict

S7's conclusion, as narrowed by S7-D, was: "girdle bone strength is probably not the binding constraint; the joint is". With a measured girdle section in place of S7's guess:

- **Measured margin for the girdle proper** (cleithrum and coracoid region, single largest section, unscaled):
  - **2.1–3.9×** against the S7-D requirement (62.6 MPa, SF 1), with both fish and both valid estimators agreeing.
  - **0.95–1.8×** in the most adverse combination (lower 1-SD yield and SF 1.5), before any size scaling.
  - About **2–17×** after isometric scaling to the 40 mm design body.
- **As a linear-size margin**, that is (Z ratio)^(1/3) ≈ 1.25–1.6× unscaled (calculated).
- **How this compares with S7's guess:** S7 had guessed "a few tenths of a mm". The measured inscribed wall thickness of the receiving girdle bone is 0.13–0.29 mm, but its *section modulus* is several times that of a 0.26 mm solid rod, because the plate is 0.5–1.3 mm deep in the bending direction.

**Verdict: STRENGTHENS**, for the girdle proper. The input that S7 assumed and S7-D could not reach is now derived from measured geometry in two individuals. It clears the requirement in every valid estimator once size is accounted for, and in all but one unscaled row.

The verdict does **not** extend to the proximal radials. Their section is still unknown, and the conditional calculation in §3d shows they would fail if they carried the moment in bending. That pushes the open question back to where S7 originally placed it, **the joint**: how the 9–55× body-weight root reaction is carried across the radial–scapula articulation (muscle, ligament or bony lock). S7's joint conclusion is unchanged; its inputs were not touched here.

**New most sensitive input.** Now that the girdle section is measured, the margin is most sensitive to:

1. whether the filled interiors are really mineralised bone (cartilage cores or marrow spaces would lower Z); and
2. the isosurface threshold. At ±1 voxel (10.5 µm) per side on a 0.13–0.15 mm wall, about ±15% thickness gives roughly ±30% in Z (calculated).

Neither moves the margin by 2× in the scaled case. The radial load path does.

## 5. What this does not establish

- **No observation was made.** All numbers are calculated on a published, simplified surface model. That model is an Amira isosurface at a threshold the paper does not state for meshes; the stated "20–120" range applies to density heatmaps.
- **Bone identities are my inference.** "Ventral girdle limb" and "cleithrum/coracoid region" come from position and continuity. The models are not segmented by bone.
- **Filled-section assumption.** I treated interiors as bone. Hollow, cartilaginous or marrow regions would reduce Z, so the reported Z values are upper bounds in that respect.
- **Two fish, one per size class.** Within-size variation is unknown.
- **Load direction.** I examined sagittal planes (fin abducted laterally, lift dorsoventral) and, secondarily, horizontal planes. Oblique fin postures and torsion were not examined. Neither were stress concentrations at articular facets, or buckling of the 0.1–0.15 mm walls.
- **Scaling.** The 24 and 20 mm SL fish are scaled to a 40 mm design body by isometry, which is an assumption. S7's "40 mm" is ambiguous between SL and total length, so both readings are given.
- **Decoder limits.** Face connectivity beyond 8,190 faces was not decoded, and the cause of the desync is unknown. Results do not depend on faces, only on vertex positions.
- **Material.** The material side still rests on herring intermuscular bone, tested in tension (S7-D §3b). It is not zebrafish girdle bone in bending.

## Negative searches (scope stated)

| Search | Scope | Result |
|---|---|---|
| Adult zebrafish proximal radial, scapula or coracoid dimensions | One extended web search ("zebrafish pectoral fin proximal radial length width µm adult measurement") | No numeric dimensions found. Waldmann et al. 2021 (bioRxiv 10.1101/2021.01.31.428959; Gdf5 and fin radials) was returned but could not be read (HTTP 429). Read-level: search-summary. |
| Open µCT dataset with the pectoral girdle on Figshare or Zenodo | One web search | None found; only amphibian datasets (University of Hamburg). |
| Numeric girdle measurements in Nguyen et al. 2022 text | Full HTML text, read through text extraction | None. The paper reports none for the cleithrum, scapula, coracoid or radials. |

## Sources

- **Nguyen S.V., Lanni D., Xu Y., Michaelson J.S., McMenamin S.K. (2022).** Dynamics of the zebrafish skeleton in three dimensions during juvenile and adult development. *Front. Physiol.* 13:875866. PMC9204358.
  - Article text: *full-text* (HTML fetched; methods quoted above).
  - Supplementary DataSheet1–4.PDF (3D models): *full-text (data files decoded)*, obtained through the Europe PMC supplementary-files service. SHA-256 prefixes: DataSheet4 `ead58b4f8cf9cce9`, DataSheet3 `1617b074648c2127`.
  - Frontiers file host: *could-not-access* (network policy).
  - MorphoSource project 000415918: *could-not-access* (network policy, 403).
- **ECMA-363, Universal 3D File Format, 4th ed. (2007).** *Could-not-access* (403 and DNS refusal). The decoder follows the bitstream algorithm as I know it and was validated only by the checks in §3a.
- **Keer S. et al. (2019).** *Anat. Rec.* PMC6800157. Carried over from S7-D: *full-text*, by that agent. Not re-read here.
- **Fiedler I.A.K. et al. (2019).** *J. Biomech.* 94:59–66. PMC6995032. Carried over from S7-D: *full-text*, by that agent. Not re-read here. Source of σ_y = 62.6 ± 13.2 and 66.8 ± 23.4 MPa.
- **S7 (`S7-organ.md`) and S7-D (`S7-deepen.md`).** Read in full from their branches. Source of the load model and requirements.

## Reproduce

1. Fetch `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9204358/supplementaryFiles` and unzip it into an empty directory.
2. Extract the 3D streams: `python3 -I S7-D-deepen/extract.py DataSheet*.PDF`, which writes `DataSheetN.PDF.K.u3d`.
3. Run:
   - `python3 -I S7-D-deepen/pos.py S7-D-deepen <u3d files>`
   - `frame_sl20.py`
   - `sweep.py`, with the boxes given in §3b, the y lists in the JSON files and the midlines 3000 / 4000 µm
   - `recompute.py`

```swarm-result
{"subproblem": "S7-D-D", "evidence": "derived", "answer": "The girdle section S7 guessed and S7-D could not reach is now derived from measured geometry: published µCT surface models of 24 and 20 mm SL zebrafish (Nguyen et al. 2022 Suppl. 3D PDFs, decoded here). The smallest girdle bending section crossed by sagittal planes medial to the fin base has Z ≈ 3.6–6.8×10⁻³ mm³ (24 mm) and ≈5.4×10⁻³ mm³ (20 mm), 2.1–3.9× the 1.73×10⁻³ mm³ needed for the worst-case 1.08×10⁻⁴ N·m root moment at 62.6 MPa, before any upward size scaling (×2.2–8 to a 40 mm fish). So 'girdle bone is not the limit' strengthens, but the proximal radials were not resolvable; if they carried the moment as four 0.10–0.15 mm rods they would fail (0.23–0.77×), which leaves the joint load path as the binding question.", "key_number": "girdle section modulus about the AP axis, min over planes medial to the pectoral fin base: 3.6e-3 to 6.8e-3 mm^3 (24 mm SL) and 5.4e-3 mm^3 (20 mm SL), wall thickness 0.13-0.29 mm (calculated from published µCT mesh vertices); proximal-radial section: unknown", "verdict": "strengthens", "depends_on": ["S7: worst-case root bending moment 1.08e-4 N·m per fin (V=3 m/s, n=3, C_L=0.78 Park & Choi 2010 search-summary, AR=9 search-summary, m=0.4 g project brief, half-width 2.5 mm assumed, elliptic lift centroid)", "S7-D: bone yield stress 62.6 MPa (lower 1-SD 43.4 MPa), Fiedler et al. 2019 herring intermuscular bone, tensile, transferred to zebrafish girdle bone in bending", "Nguyen et al. 2022 Suppl. Figs 7-8 surface models (Amira isosurface, MeshLab-simplified, 10.5 µm scans) as faithful bone geometry", "unit calibration: 24 mm file in µm and 20 mm file in 10.5 µm voxels, checked against labelled SL to ~2-3%", "my U3D decoder's vertex-position decoding (validated by block names, anatomy and SL; face decoding failed after 8190 faces)", "filled-section assumption: interiors of bone outlines are mineralised (no cartilage core or marrow)", "bone identification by position: ventral girdle limb / cleithrum-coracoid region (my inference; models not segmented by bone)", "load geometry: fin abducted laterally, lift dorsoventral, root moment about the anteroposterior axis carried by sagittal girdle sections", "isometric scaling Z ∝ L^3 from 20-24 mm SL to the 40 mm design body (SL vs TL ambiguous in S7)", "section method bias +4-14% on synthetic shapes; ±15 µm slab under-samples the 20 mm mesh (excluded)", "Keer et al. 2019: proximal radials articulate with scapula, so they lie in the load path before the cleithrum", "S7 joint conclusion: 9-55× body-weight reaction at the articulation (muscle moment arm 0.5-1 mm, 200 kPa muscle stress, both assumed), unchanged here"]}
```
