"""Pack Morpheus TIFF snapshots of one run into a compact npz (uint8 cell index + per-cell type).

Usage: python -m engineering.xenomorph.pack_fields RUN_DIR [--every K] [--keep MCS,MCS,...]
Writes RUN_DIR/fields.npz with arrays ids_<mcs> (uint8, 0 = medium, 1..n = cell) and types_<mcs>
(uint8 per cell index, 1 = A, 2 = B; index 0 unused). Snapshot selection: every K-th plus the --keep list
plus first and last.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np

from engineering.xenomorph.analyze import load_snapshot


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--keep", default="")
    a = ap.parse_args(argv)
    run = Path(a.run)
    tiffs = sorted(run.glob("cell.id_cell.type_*.tif"), key=lambda p: int(re.findall(r"(\d+)\.tif$", p.name)[0]))
    keep = {int(k) for k in a.keep.split(",") if k}
    arrays = {}
    for i, t in enumerate(tiffs):
        mcs = int(re.findall(r"(\d+)\.tif$", t.name)[0])
        if not (i % a.every == 0 or mcs in keep or i == len(tiffs) - 1):
            continue
        ids, types = load_snapshot(t)
        labels = np.unique(ids[ids > 0])
        if len(labels) > 255:
            raise ValueError("more than 255 cells")
        remap = np.zeros(int(ids.max()) + 1, dtype=np.uint8)
        remap[labels] = np.arange(1, len(labels) + 1, dtype=np.uint8)
        dense = remap[ids]
        ct = np.zeros(len(labels) + 1, dtype=np.uint8)
        np.maximum.at(ct, dense[ids > 0].astype(np.int64), types[ids > 0].astype(np.uint8))
        arrays[f"ids_{mcs}"] = dense
        arrays[f"types_{mcs}"] = ct
        arrays[f"labels_{mcs}"] = labels.astype(np.int32)
    np.savez_compressed(run / "fields.npz", **arrays)
    print(run / "fields.npz", len(arrays) // 3, "snapshots", (run / "fields.npz").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
