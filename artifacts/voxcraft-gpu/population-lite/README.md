# Population, lite config: 3000 seeded random bodies x {actuated, passive, x-mirror, duplicate} = 12000 simulations
Config (disclosed, chosen for throughput after the E=1e6 population timed out): E=1e5 Pa, self-collision OFF, T=4 s, re-zero at 1 s,
DtFrac 0.9, gravity+floor, mu 1/0.8, contraction 10% peak @ 4 Hz. Bodies: `gen_sweep.py --lite`, seed 20261101, 6x6x5 box,
candidates c00000-c02999 (identical body files to the s1 generator).
| source | engine | bodies | wall |
|---|---|---|---|
| claude-voxgpu-unmod-l40s-lite1 (aijob-e00btpzyyxrgps71kz) | voxcraft-sim dd8668f UNMODIFIED, L40S | c0000-c0249 (1000) | 817 s + ~830 s per 500 |
| claude-voxgpu-fork-h100-lite2 (aijob-e00ex2xwetgsg9vfw1) | dd8668f + FORK-cdp-serial, H100 | c0000-c0999 (4000) | ~1390-1460 s per 1000 |
| claude-voxgpu-fork-h100-lite3 (aijob-e00ra5nbfzmtday6c8) | dd8668f + FORK-cdp-serial, H100 | c1000-c2999 (8000) | 1549 / 1623 s per 4000 |
Validation: the 1000 bodies run on both engines agree bitwise (0 disagreements), as do 3x33 lite endpoint bodies.
11000 of the 12000 simulations are fork output (labelled); all summary statistics are in population_summary.json
(`scripts/voxgpu/analyze_pop.py`). Invalid reports rejected: 0. Duplicates bitwise identical: 3000/3000.
Findings: 923/3000 (31%) passive controls move >= 10 um after the transient (max 16 mm); among the 2077 bodies whose passive
control holds, median |d| 1.48 mm (max 25.4 mm), x-mirror error median 7.9% of |d| (p90 30%, n=1327 with |d|>1 mm), 3.8% within 1%.
Throughput: unmodified/L40S ~0.6 bodies/s; fork/H100 0.68 bodies/s at 1000/batch and 2.6 bodies/s at 4000/batch.
Scope: generic soft-voxel ground-contact mechanics; not tissue, no fluid, not calibrated.
