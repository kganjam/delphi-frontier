"""Poster from the returned raw fields only (state-based, nothing generated): per target, u(x) of target vs each method's selected candidate,
best-so-far score by evaluation, and the evaluated (d,L) points coloured by score. Failure and gate labels are printed as returned."""
import argparse, json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from engineering.rd_inverse import design as d


def render(out, png):
    out = Path(out)
    tr = json.loads((out / "traces.json").read_text())["traces"]; sel = json.loads((out / "selection.json").read_text())
    tj = json.loads((out / "targets.json").read_text())["targets"]; tf = np.load(out / "targets.npz")["fields"]; ef = np.load(out / "evaluated_fields.npz")
    n = len(tf); fig, ax = plt.subplots(3, n, figsize=(3.1 * n, 8.6), squeeze=False)
    col = {"baseline": "#1b7f79", "optimizer": "#b5541c"}
    for i in range(n):
        x = np.linspace(0, tj[i]["L_true"], tf.shape[-1], endpoint=False)
        ax[0, i].plot(x, tf[i, 0], "k", lw=2, label="target (synthetic)")
        for m in col:
            s = sel["selection"][m][i]
            if s.get("index") is not None:
                L = s["params_dL"][1]
                ax[0, i].plot(np.linspace(0, L, tf.shape[-1], endpoint=False), ef[f"{m}_{i}"][s["index"]][0], color=col[m], lw=1.2, label=f"{m} d={s['params_dL'][0]:.1f} L={L:.1f} rms={s['score']:.3g}")
        ax[0, i].set_title(f"{tj[i]['id']}  true d={tj[i]['d_true']:.1f} L={tj[i]['L_true']:.1f}", fontsize=8); ax[0, i].set_xlabel("x (model units)", fontsize=7); ax[0, i].legend(fontsize=5)
        for m in col:
            sc = [np.inf if t["score"] is None else t["score"] for t in tr[m][i]]
            ax[1, i].semilogy(np.minimum.accumulate(sc), color=col[m], label=m)
            P = np.array([t["params_dL"] for t in tr[m][i]]); c = np.array([t["score"] if t["score"] is not None else np.nan for t in tr[m][i]])
            ax[2, i].scatter(P[:, 0], P[:, 1], c=np.log10(np.maximum(c, 1e-12)), cmap="viridis", marker="o" if m == "baseline" else "^", s=18, vmin=-4, vmax=0)
        ax[1, i].axhline(d.GATE_B_RMS, color="gray", ls=":"); ax[1, i].set_xlabel("true evaluations (init counted)", fontsize=7); ax[1, i].set_ylabel("best RMS so far", fontsize=7)
        ax[2, i].plot(tj[i]["d_true"], tj[i]["L_true"], "r*", ms=12); ax[2, i].set_xlabel("d", fontsize=7); ax[2, i].set_ylabel("L", fontsize=7)
        ax[2, i].set_xlim(*d.D_RANGE); ax[2, i].set_ylim(*d.L_RANGE)
    fig.suptitle("Inverse Schnakenberg design: SIMULATED, synthetic targets, model units, n=6. Circles Sobol, triangles elite search, star = true parameters (never shown to either method). "
                 "Colour log10 RMS. Dotted: gate B 0.02. No biological claim.", fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(png, dpi=110); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("png"); a = ap.parse_args(); render(a.out, a.png)
