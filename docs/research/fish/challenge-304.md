# Challenge 304: adversarial review of claim 232's replication (zebrafish cleithral section)

Date: 2026-11-04. Scripts and raw output: `docs/research/fish/challenge-304/`.

**Claim under review.** This is the harvester's summary of `replicate-232.md` on branch `claude/s7-d-girdle-section-4o9w38`:

- The narrowest girdle section is the vertical cleithral plate bending out of plane.
- Z_min = 1.05e-3 mm³ (1.0–1.2e-3 on the body mesh, 1.5–2.9e-3 on the head mesh); d_eq ≈ 0.22 mm; fish at 24 mm SL.
- That is 3.4–6.5× below the recorded 3.6–6.8e-3 mm³.
- It is below the 1.73e-3 mm³ requirement at the measured size.
- It passes only after isometric scaling to 40 mm, where it is 2.7–2.8× the requirement.
- The harvester did not re-run the mesh slicing.
- Recorded evidence level: *derived*.

**Verdict: WEAKENED.**

The arithmetic and the mesh slicing reproduce. But the section modulus the claim reports assumes the cleithrum is forced to bend about the anteroposterior (AP) axis. The actual cross-sections are oblique: their principal axes are rotated 30–65° from that axis. If the bone is free to bend obliquely (unsymmetric bending), the governing modulus is about 30–43% lower. With that correction, the "passes after scaling to 40 mm" conclusion holds only if 40 mm means standard length (SL) and no safety factor is applied, and even then by only 1.6–1.95×. If 40 mm means total length (TL), the section is at or below the requirement.

## 1. Re-running the slicing (the step the harvester did not re-run)

Everything in this section is calculation from primary data, not observation.

- **Data.** I downloaded Nguyen et al. 2022, *Front. Physiol.* 13:875866 (PMC9204358) supplementary files from the Europe PMC `supplementaryFiles` endpoint (read-level: primary data). From `DataSheet4.PDF` I extracted the U3D streams with pypdf: object 32 (body, 20,733,240 bytes) and object 33 (head, 9,000,732 bytes).
- **Decoder.** I recompiled the replicator's own decoder (`ac.c`, `base.py`, `runfaces.py`).
  - Body mesh: 1,153,000 faces; 0 bad indices; 110,688,593 of 110,688,664 bits used; all 1,729,500 edges shared by exactly two faces.
  - Head mesh: 500,000 faces.
  - This matches the replicator's validation exactly.
  - **Independence caveat:** this is the same decoder, not an independent one. The decode is self-validating (a fully 2-manifold mesh, and the bit budget consumed to within 71 bits), so I accept it.
- **Raw sections reproduce exactly**, with raw values recovered by dividing by k³ = 0.907. Left x = 4.2 gives 1.15e-3; left x = 4.4 gives 1.91e-3; right x = 4.4 gives 1.17e-3; right x = 4.0 gives 2.15e-3 mm³. These match `replicate-232.md` §3c.

### Independent arithmetic

| Quantity | My calculation | Claim |
|---|---|---|
| Requirement: 1.08e-4 N·m / 62.6e6 Pa | 1.725e-9 m³ = 1.725e-3 mm³ | 1.73e-3 ✔ |
| 3.6e-3 / 1.05e-3 and 6.8e-3 / 1.05e-3 | 3.43 and 6.48 | ✔ |
| d_eq = (32 Z/π)^(1/3) at Z = 1.05e-3 | 0.220 mm | 0.22 ✔ |
| Unit scale k³ at k = 0.968 | 0.907 | ✔ |
| Head mesh: d = 22–24 units × 11.3–12.9 µm, Z = π d³/32 | 0.249–0.310 mm; 1.52–2.92e-3 mm³ | ✔ |
| (40/24)³ | 4.630 | ✔ |
| Scaled Z at 1.0–1.05e-3 | 4.63–4.86e-3 mm³ → 2.68–2.82× | ✔ (but see below) |

**Minor inconsistency in the harvested sentence.** The text says "4.6–4.9e-3", but the claim's own body-mesh range of 1.0–1.2e-3 (1.01–1.17e-3 at full precision) scales to 4.7–5.4e-3 mm³. The harvester also:

- replaced the replicator's 40/24.25 with 40/24;
- dropped the replicator's 40 mm = TL reading (×2.41, giving 1.45×; 0.97× with safety factor 1.5).

So "2.7–2.8× at the top" covers only the most favourable reading of the 40 mm size. The replicator itself reported 1.45–2.7×, and that range should not have been narrowed away.

## 2. The proxy: AP-axis I/c on oblique sections

The claim, and the replicator's code (`secs.py`), compute Z = I_zz / c_y. This is the second moment of area about the AP axis through the centroid, divided by the extreme lateral fibre distance. That equals the governing modulus only if:

- the section is symmetric about that axis (product of inertia I_yz = 0), or
- the bone is restrained so that it can only bend in the y direction.

**Neither condition holds** on the measured sections. I re-sliced at 0.1 mm steps (`challenge-304/mine.py`) and computed three versions of Z:

- **Z_naive:** the claim's definition.
- **Z_unsym:** a moment about z applied to an unrestrained section. The stress field σ = a·y + b·z is solved so that ∫σ y dA = M and ∫σ z dA = 0.
- **Z_min,anydir:** the weakest moment direction.

All values are at k = 0.968, in mm³ × 10⁻³, using the replicator's crop. "pr" is the principal-axis angle from y, in degrees.

| x (mm) | L Z_naive | L Z_unsym | L Z_min,any | L pr | R Z_naive | R Z_unsym | R Z_min,any | R pr |
|---|---|---|---|---|---|---|---|---|
| 4.0 | 1.43 | 1.23 | 0.94 | 36 | 1.95 | 1.51 | 1.15 | 34 |
| 4.1 | **0.97** | 0.76 | 0.63 | 49 | 1.94 | 1.92 | 1.24 | 3 |
| 4.2 | 1.04 | 0.77 | 0.63 | 55 | 1.64 | 1.41 | 1.09 | −31 |
| 4.3 | 1.39 | 0.76 | 0.64 | 58 | 1.31 | 0.96 | 0.80 | −48 |
| 4.4 | 1.73 | **0.73** | 0.67 | 62 | **1.06** | 0.72 | 0.65 | −52 |
| 4.5 | 2.01 | 0.82 | 0.76 | 64 | 1.12 | 0.65 | 0.59 | −55 |
| 4.6 | 2.34 | 0.99 | 0.93 | 65 | 1.30 | **0.60** | 0.55 | −58 |
| 4.7 | (lost to crop) | | | | 1.42 | 0.60 | 0.56 | −63 |
| 4.8 | (lost to crop) | | | | 1.69 | 0.74 | 0.70 | −65 |

What the table shows:

1. **The claim's own definition holds to within ~8%.** Finer sampling moves the left minimum from x = 4.2 to x = 4.1 (0.97e-3 versus 1.04e-3).
2. **Unrestrained bending gives a much smaller modulus.** Z_unsym,min = **0.60e-3 (right) to 0.73e-3 (left) mm³**, 30–43% below the claimed 1.05e-3. That corresponds to d_eq = 0.18–0.20 mm. The left and right minima also fall at different heights from the claim's.
3. **Which is right?** The truth lies between Z_unsym (a free plate) and Z_naive (fully restrained). The cleithrum is joined dorsally to the supracleithrum and ventrally to the girdle floor, so it is partly restrained. Inference, not measurement: I cannot quantify that restraint from the mesh.
4. **What this means for the claim.** It reports the upper bound of this bracket as "the" Z_min and gives no range for it.

## 3. The hidden assumption that carries "passes after scaling"

The pass/fail result depends on three choices stacked together:

1. the definition of Z (§2);
2. whether S7's 40 mm is SL or TL;
3. whether a safety factor is applied.

Ratios to the requirement, using Z_req = 1.725e-3 mm³ and 2.59e-3 mm³ with SF 1.5. All are calculated.

| Z at 24 mm (mm³) | 40 = SL, ×4.63 | 40 = SL, SF 1.5 | 40 = TL, ×2.41 | 40 = TL, SF 1.5 |
|---|---|---|---|---|
| 1.06e-3 (Z_naive, top) | 2.84× | 1.89× | 1.48× | 0.99× |
| 0.97e-3 (Z_naive, finer sampling) | 2.60× | 1.73× | 1.35× | 0.90× |
| 0.73e-3 (Z_unsym, left) | 1.95× | 1.30× | 1.02× | 0.68× |
| 0.60e-3 (Z_unsym, right) | 1.61× | 1.08× | **0.84×** | **0.56×** |

The claim's qualitative conclusion is "survives with a much thinner margin". That holds for the SL reading. Under the TL reading with unrestrained bending, the bone section **does not meet** the requirement even with no safety factor (0.84–1.02×).

Two further assumptions carry the result and I did not test them:

- **Isometric scaling (Z ∝ L³) from 24 to 40 mm.** I did not search for zebrafish girdle allometry. The meshes for other sizes in the same paper (DataSheets 1–3: 12, 16 and 20 mm) could test it. I did not slice them.
- **Size mismatch.** The claim's "below the requirement at measured size" compares a 24 mm fish's section with a moment derived for the 40 mm, 0.4 g design fish. This is my inference: that comparison is not meaningful in either direction and should not be read as a failure. The replicator says the same in its §3e. The harvested sentence drops that caveat.

## 4. The neighbouring-bone issue (not resolved)

I listed every closed loop in the lateral band with no AP crop (`challenge-304/loops.py`). At x = 3.8–4.2 mm a second loop of 0.024–0.043 mm² lies just anterior to the cleithral loop. On the left at x = 4.2 it sits at z ≈ 5.0–5.2 mm (scaled), outside the replicator's crop. On the right at x = 3.8–3.9 it is cut by the crop boundary.

On the right, the cleithral loop alone at x = 3.8–3.9 has Z_naive ≈ 0.85e-3 mm³, lower than anything in the claim. At x = 4.0 the area jumps from 0.031 to 0.051 mm², which looks like a merger with that neighbouring loop.

My inference, unverified: this is the cleithrum–supracleithrum overlap. Two consequences follow:

- the "narrowest section" near x ≈ 4.0–4.2 sits at a joint where load is shared;
- a single-bone section there is not the right model.

This cuts both ways (shared load would raise the effective capacity), so I do not use it in the verdict. I identified bones by position only, as the replicator did.

## 5. Evidence level

"Derived" is honest. The value is calculated from published µCT surface meshes, and both the replicator and the harvested claim label it as a calculation. I found no presentation of the number as measured.

The harvester's note "mesh slicing not re-run" is accurate for the harvester. I have now re-run it, and the claim's numbers reproduce under its own definition.

## 6. Scope of negative searches and what I did not do

- I did not read S7 / S7-D (the source of M = 1.08e-4 N·m, σ_y = 62.6 MPa and the 40 mm design fish). I did not re-check Fiedler et al. 2019. Read-level for those inputs: could-not-access (not attempted). My ratios inherit them unchanged.
- I did not search the literature for zebrafish pectoral girdle allometry or girdle load sharing. Scope: none.
- I did not slice the 12, 16 or 20 mm meshes.
- I did not quantify the effect of the isosurface threshold, as the replicator also did not.

## 7. Summary

- **What reproduces:** the claim's arithmetic and its exact mesh sections, under its own definition (Z_naive about the AP axis ≈ 0.97–1.06e-3 mm³ at 24 mm SL).
- **What is wrong:** the definition is a proxy. It ignores the 30–65° obliquity of the cleithral sections. The unrestrained-bending modulus is 0.60–0.73e-3 mm³ (d_eq 0.18–0.20 mm).
- **Consequence:** the scaled pass margin falls to 1.6–1.95× (SL reading), and the section fails under the TL reading.
- **Harvester's summary:** it also narrowed the replicator's 1.45–2.7× scaled range to 2.7–2.8×, dropping the TL reading.

```swarm-challenge
{"claim_id": 304, "outcome": "weakened", "reason": "The mesh sections and arithmetic reproduce under the claim's AP-axis I/c definition, but the cleithral sections are oblique (principal axes 30-65 deg off), so unrestrained-bending Z is 30-43% lower; the scaled-to-40 mm pass is then 1.6-1.95x (SL reading) and fails at 0.84-1.02x if 40 mm is TL, a reading the harvested summary dropped.", "corrected_value": "Z_min = 0.60-1.06e-3 mm^3 at 24 mm SL (0.60-0.73e-3 unrestrained unsymmetric bending; 0.97-1.06e-3 AP-axis restrained), d_eq 0.18-0.22 mm", "depends_on": ["Nguyen et al. 2022 Front Physiol 13:875866 DataSheet4 U3D meshes (objects 32/33)", "replicator's U3D face decoder ac.c (self-validated: 2-manifold, bit budget)", "unit scale k = 0.968 um/unit from mesh SL vs 24 mm category (replicate-232 §2)", "cleithral arm horizontal section crop z 5.5-6.23 mm raw as the governing section (replicate-232 §3b)", "load case: root moment about AP axis (S7-organ.md, not re-read)", "requirement M = 1.08e-4 N m and sigma_y = 62.6 MPa (S7 §3c / S7-D §3b, Fiedler 2019; not re-checked)", "isometric scaling Z ~ L^3 from 24 to 40 mm", "TL/SL = 1.23 from the body mesh (replicate-232 §1)"]}
```
