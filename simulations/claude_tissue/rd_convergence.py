"""Control for Sim A (raised by cross-review): is t=150 converged?  Re-run 3 cases to 4x longer (t=600)
and compare dominant k. Also a Neumann-boundary note: Sim A is periodic (declared limitation)."""
import json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import claude_tissue.rd_wavelength as rw
from claude_tissue.common import ROOT, write_receipt
OUT = ROOT / "artifacts/simulations/claude-tissue-rd-wavelength"
if __name__ == "__main__":
    t0 = time.time(); rows = []
    for d, g in [(20, 1.0), (45, 1.0), (20, 2.0)]:
        res = {}
        for T in (150.0, 600.0):
            rw.T_END = T; u = rw.run(d, g, 11); res[T] = rw.dominant_k(u)[2]
        rows.append(dict(d=d, gamma=g, seed=11, k_peak_t150=res[150.0], k_peak_t600=res[600.0], converged=res[150.0] == res[600.0]))
        print(rows[-1], flush=True)
    p = OUT/"convergence-control.json"; p.write_text(json.dumps(rows, indent=1))
    write_receipt(OUT, "claude-tissue-rd-convergence", "python3 simulations/claude_tissue/rd_convergence.py", [11], [], [p], t0)
