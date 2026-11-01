# claude-mol status
Updated: 2026-11-01 17:14 UTC / 09:14 PST
Branch: claude/mol-sims-20261101, last commit 0f6ea3ea Collect the non-cognate Fgfr2 IIIc control MD: the sp (pushed)

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
- claude-mol-shhn-md40-20261105 aijob-e00j94wgv579ddn7g9: RUNNING (ShhN apo 40 ns, convergence replica A)
- claude-mol-shhn-md40-20261106 aijob-e00kp81hkyhc9yb10p: RUNNING (ShhN apo 40 ns, convergence replica B)
  Purpose: the 10 ns pair was NOT converged. Over 5 ns blocks both 10 ns replicas drift UP (+0.21, +0.32 A/ns),
  so the -0.11 A/ns last-2-ns figure in replica 1 was window noise, not a plateau. 40 ns x 2 tests whether the
  final block goes flat. Only 2 of my jobs run at once; no job I did not start has been touched.

## Blockers
Manifest-based MCP tools (OpenMM/AF3/BioEmu2/stab_ddg): schema not published; MD moved to raw H100 jobs instead.

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
Collect the two 40 ns replicas (~2.2 h each), run experiments/mol_sims/md_convergence.py over all four ShhN
replicas, and correct the openmm-shhN-md manifest + README if the longer runs change the drift statement.
