# xenomorph pilots (not protocol seeds)

Run locally before the protocol was frozen, to choose the initial placement. Morpheus 2.3.9, generator
`engineering/xenomorph/cpm_model.py` at its pre-freeze state, same J/T as the frozen arms.

- `lowdensity-seed99-*`: random sequential addition in a ball of radius 38, gap >= 2 voxels (14% packing). Killed at
  4000 MCS (dah) / 4000 MCS (zero). dah: ~21 clusters that did not merge, rg_norm 0.872 -> 0.889 (no compaction).
  This stall is why the frozen protocol uses a dense suspension.
- `dense-seed98-*`: the frozen jittered-lattice placement, 3000 MCS each. dah compacted (8 aggregates at 500 MCS,
  one at 3000, rg_norm 0.752 -> 0.482, a perfect ball is 0.4806) and sorted (core-shell -0.07 -> +0.37). zero kept
  rg_norm nearly flat (0.752 -> 0.744, ratio 0.990) while jammed cells came to touch (largest cluster 0.46 at 500 MCS,
  0.95 at 3000): contact without cohesion. Only the 500 MCS zero point had been read when the zero gate was set on Rg.

`inputs.json` holds the TIFF hashes the metrics were computed from (the TIFFs themselves are not kept).
