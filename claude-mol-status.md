# claude-mol status
Updated: 2026-11-01 19:38 UTC / 11:38 PST
Branch: claude/mol-sims-20261101, last commit efb2e84a Two 40 ns ShhN replicas, and a log-reassembly defect  (pushed)

## Studio-scale contribution (gap report, 2026-11-01)
Manifests written to site/artifacts/simulations/, each naming one project_scale and what it does NOT establish:
- macromolecular (was 0): boltz2-shhN, boltz2-fgf10a-fgfr2b, openfold3-kcnk5b-dimer, boltz2-kcnj13, openmm-shhN-md, openmm-fgf10a-fgfr2b-md
- subcellular (was 1): sbml-hedgehog-pathway-perturbations, sbml-ra-fgf-bistable-switch
- cellular: bioelectric-kcnk5b-pump-leak

## Runs (local, exit 0)
s1 RA/FGF switch (Cyp26 arm invalid: no steady state); s2 + s2b Hedgehog (model fails Ptc/Sufu sign check);
s3 local sensitivity; s4 OpenFold2 confidence; s5 Kcnk5b/Kcnj13 pump-leak sweep; gemini-4-argon review HTTP 200.

## Nebius Scientific MCP
- msa_search_native x6 SUCCEEDED; template identity measured per chain (structures/msa_identity.json)
- boltz2: shhN (pLDDT 85), fgf_complex (0.77), fgfr2c negative control (0.84 - HIGHER, no specificity signal), kcnj13 (54% >=70 vs 18% recorded) - all SUCCEEDED
- openfold3: kcnk5b dimer SUCCEEDED (ipTM 0.48); kcnj13 tetramer SUCCEEDED but WORSE than monomer (pLDDT 46, ipTM 0.29)
- boltz2 kcnk5b_dimer FAILED (same-sequence MSA check) - receipt kept, retried on openfold3
- submit_openmm_workflow / alphafold3 / bioemu2 / stab_ddg: INVALID_REQUEST, upload-manifest format undocumented. BLOCKED.

## Nebius AI jobs (CLI-read)
- claude-mol-shhn-md-s1 aijob-e00jkrrepqcyqndjg3: COMPLETED, collected. 10 ns, 469 ns/day, all finite.
  RMSD plateau 4.19 A (drift -0.11 A/ns); CA RMSF vs start pLDDT Spearman -0.63 (p=2e-20).
- claude-mol-fgf-md-s1 aijob-e00kxeq47gf8bqrth1: COMPLETED, collected. 73% of 95 inter-chain contacts kept;
  RMSF vs pLDDT rho -0.10 (p=0.053) - the ShhN correlation did NOT reproduce on the complex.
- claude-mol-shhn-md-s2 aijob-e00fh453w6m5m3ds9t: COMPLETED, collected. rho -0.60 (reproduces); cross-replica RMSF rho 0.91;
  replicas disagree on drift (-0.11 vs +0.98 A/ns), so 10 ns is NOT converged.
- claude-mol-fgfnc-md-s1 aijob-e00nv1v66h5nrk4zpx: COMPLETED, collected. Non-cognate IIIc complex keeps 62% of its
  68 inter-chain contacts (cognate: 73% of 95) - the same range, so 10 ns interface persistence does NOT discriminate isoforms.
- claude-mol-shhn-md40-20261105 aijob-e00j94wgv579ddn7g9: FAILED at launch, and -20261106 aijob-e00kp81hkyhc9yb10p
  CANCELLED by me as doomed the same way: the Nebius CLI's repeated --args OVERRIDES instead of appending, so the
  "-c" was dropped and the container ran the script text as a filename. Relaunched through an injected runner:
- claude-mol-shhn-md40b-20261105 aijob-e00s0swv95fj2pfjwj: COMPLETED, collected (40 ns, 467 ns/day, rho -0.737)
- claude-mol-shhn-md40b-20261106 aijob-e00grxxts2zagf2hk5: COMPLETED, collected (40 ns, 467 ns/day, rho -0.633)
No jobs of mine are running. I cancelled only my own doomed job; no job I did not start was ever touched.
  Purpose: the 10 ns pair was NOT converged. Over 5 ns blocks both 10 ns replicas drift UP (+0.21, +0.32 A/ns),
  so the -0.11 A/ns last-2-ns figure in replica 1 was window noise, not a plateau. 40 ns x 2 tests whether the
  final block goes flat. Only 2 of my jobs run at once; no job I did not start has been touched.

## Blockers
Manifest-based MCP tools (OpenMM/AF3/BioEmu2/stab_ddg): schema not published; MD moved to raw H100 jobs instead.

## Round-2 review (gemini-4-argon) and what it changed
Prompt: experiments/mol_sims/conclusions_round2.json; reply: results/.../gemini_review_conclusions_round2_gemini-4-argon.json.
Four corrections made, all committed:
1. s5 Kcnk5b: the arms were compared at DIFFERENT times (10 min vs 1 h). Re-read at matched times and screened against
   Na_i 5-30 / K_i 100-150 mM, the recruitment arm is only physiological to x4 (+6.0 mV, not the -19 mV quoted at x8/1 h,
   where Na_i reaches ~90 mM). That figure is WITHDRAWN. Signs still differ inside the usable window.
2. Complex MD: pooling both chains was the wrong test. Split by chain, flexibility vs start-model pLDDT is strong in the
   LIGAND INTERFACE residues in BOTH complexes (rho -0.697 and -0.703, R2 ~0.49, surviving Bonferroni over 14 groups).
   The earlier "did not reproduce" null is WITHDRAWN.
3. Contact retention now reported as a COUNT (69.5 vs 42.4 pairs, 1.64x), not only a fraction that made them look alike.
4. A 5 ns-block slope is a weak convergence criterion (a drifting protein can pause); the frame-level test argon asked
   for needs trajectory frames, which the job log does not return. Recorded as not done, not claimed.
5. Template-free refold DONE: both complexes refolded with a single-sequence a3m. The IIIc > IIIb inversion SURVIVES
   (0.660 vs 0.614; gap narrows 0.077 -> 0.046), so template proximity does NOT explain it and the manifest line that
   named it as the cause is corrected. The Fgf10a ligand collapses without an alignment (-47.8 pLDDT) while the Fgfr2
   receptor stays above 80, which is itself learned structural memory, so the control cannot exclude memorisation.
6. Convergence DONE with 2 x 40 ns: both end on a near-flat final 5 ns block (+0.06, -0.11 A/ns) but block MEANS wander
   3.00 and 2.80 A with the slope changing sign 6 and 3 times. RMSD plateau is NOT a usable criterion here - argon's
   objection upheld. Across all four replicas: rho -0.60 to -0.74, pairwise RMSF rho 0.78-0.92. Ranking is the result.
Still outstanding: per-chain realignment of RMSF and a frame-level convergence test (pairwise RMSD / cluster overlap).
Both need trajectory frames, which the job log does not return. Recorded as not done, not claimed.

## Defect found in my own tooling (fixed, nothing committed was wrong)
collect_md.py reassembled out-of-order 16 KiB log chunks by accepting any ordering that PARSED as JSON. For arrays of
plain floats that is too weak: a wrong order spliced potential energies (~-9e5 kJ/mol) into the RMSD array, giving a
926209 A RMSD and a NEGATIVE radius of gyration on the first 40 ns collection. 10 ns runs make 2-3 chunks (wrong order
fails to parse); 40 ns makes 7 (it does not). The check now also validates array lengths, distance ranges and energy
signs. All six MD runs re-derived from their saved logs: 6/6 CONFIRMED (results/.../md_log_verification.json).

## Findings that limit what may be claimed
1. The non-cognate Fgfr2 IIIc control OUTSCORED the cognate IIIb complex (0.84 vs 0.77), and IIIc has the closer
   PDB70 template (81%/99% vs 78%/99%). The complex predictions carry no isoform-specificity signal.
2. ShhN's pLDDT 85 is largely template recall: closest MSA hit 95% identical over the full chain.
3. The RMSF-vs-confidence correlation is seed-robust on the ShhN monomer but absent on the complex (rho -0.10, p=0.053)
   and only weak in the IIIc control (rho -0.20); it is a monomer observation, not a general property.
4. MD does not rescue the failed specificity control: both complexes hold their interface over 10 ns. No FGF10-FGFR2b
   isoform-specificity claim is supported by any run here.

## Artifact export (lab account deleted tonight)
/data/artifacts/delphi-evolve-rethink/claude-mol-20261101/ = results/ + experiments/ + manifests/ (9) + README.md, 17 MB,
*.b64 inputs excluded. Status mirrored to /data/artifacts/delphi-evolve-rethink/claude-mol-status.md.

## Next
All planned runs are collected, verified and committed; 9 manifests validate and every declared source_files hash
matches on disk. Artifacts mirrored. Remaining blockers are external (undocumented upload manifest for
AlphaFold3/stab_ddg/BioEmu2) or need trajectory frames the job log will not return.
