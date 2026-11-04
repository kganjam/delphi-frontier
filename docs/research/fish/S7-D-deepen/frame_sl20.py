"""Put the 20 mm SL whole-body mesh into the same frame as the 24 mm one. CALCULATED.

Input : DataSheet3.PDF.1.u3d.pos.npz (vertices of the whole-body model in Nguyen et al. 2022 Suppl. Fig. 7)
Output: ds31_frame.npz with x = ventral-up (um), y as given (um), z = distance from snout (um).
Units : the file is in scan voxels; x10.5 um is the paper's stated scan resolution. Check: snout to
        caudal-fin base comes out at ~19.5 mm for a fish the paper labels 20 mm SL.
"""
import sys, numpy as np
P = np.load(sys.argv[1])["P"] * 10.5
Q = np.c_[12000 - P[:, 0], P[:, 1], 25062 - P[:, 2]]   # flip DV so ventral is high x; snout (z_max = 25062 um) -> 0
np.savez(sys.argv[2] if len(sys.argv) > 2 else "ds31_frame.npz", P=Q)
