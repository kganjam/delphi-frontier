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
    vc = json.loads((out / "validation_controls.json").read_text()); gA = json.loads((out / "targets.json").read_text())["gate_A_met"]
    allu = [tf[:, 0]] + [ef[f"{m}_{i}"][sel["selection"][m][i]["index"]][0] for m in ("baseline", "optimizer") for i in range(len(tf)) if sel["selection"][m][i].get("index") is not None]
    ylo, yhi = min(float(np.min(a)) for a in allu) - 0.05, max(float(np.max(a)) for a in allu) + 0.05
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
        ax[0, i].set_ylim(ylo, yhi)  # one explicit concentration scale for every target (all selected fields included); raw values unchanged
        tag = "" if gA[i] else "\nUNPATTERNED: amplitude gate failed;\ndesign success undefined"
        ax[0, i].set_title(f"{tj[i]['id']}  true d={tj[i]['d_true']:.1f} L={tj[i]['L_true']:.1f}{tag}", fontsize=8, color="k" if gA[i] else "#a00000")
        wi = vc["wrong_ic_scores"][i]; fails = wi is None or wi <= 1e-6
        ax[0, i].text(0.02, 0.97, f"controls (RMS vs target)\noracle {vc['positive_oracle_scores'][i]:.1e}\nwrong d {vc['negative_wrong_d_scores'][i]:.2g}  wrong L {vc['negative_wrong_L_scores'][i]:.2g}\nwrong IC {wi:.2g}" + ("  <1e-6: control FAILED" if fails else ""),
                      transform=ax[0, i].transAxes, fontsize=5.5, va="top", color="#a00000" if fails else "k", bbox=dict(fc="w", ec="none", alpha=.8))
        if not gA[i]:
            ins = ax[0, i].inset_axes([0.42, 0.40, 0.55, 0.22]); ins.plot(x, tf[i, 0] - tf[i, 0].mean(), "k", lw=1)
            for m in col:
                s_ = sel["selection"][m][i]
                if s_.get("index") is not None:
                    ins.plot(np.linspace(0, s_["params_dL"][1], tf.shape[-1], endpoint=False), ef[f"{m}_{i}"][s_["index"]][0] - tf[i, 0].mean(), color=col[m], lw=.8)
            ins.set_title("MAGNIFIED inset, own scale (~1e-6)", fontsize=5); ins.tick_params(labelsize=4); ax[0, i].set_xlabel("x (model units)", fontsize=7); ax[0, i].legend(fontsize=5, loc="lower left")
        for m in col:
            sc = [np.inf if t["score"] is None else t["score"] for t in tr[m][i]]
            ax[1, i].semilogy(np.minimum.accumulate(sc), color=col[m], label=m)
            P = np.array([t["params_dL"] for t in tr[m][i]]); c = np.array([t["score"] if t["score"] is not None else np.nan for t in tr[m][i]])
            ax[2, i].scatter(P[:, 0], P[:, 1], c=np.log10(np.maximum(c, 1e-12)), cmap="viridis", marker="o" if m == "baseline" else "^", s=18, vmin=-4, vmax=0)
        if gA[i]:
            ax[1, i].axhline(d.GATE_B_RMS, color="gray", ls=":")
        else:
            ax[1, i].text(0.5, 0.5, "Gate B undefined / not evaluable\n(gate A failed); no threshold drawn", transform=ax[1, i].transAxes, ha="center", fontsize=6, color="#a00000")
        ax[1, i].set_xlabel("true evaluations (init counted)", fontsize=7); ax[1, i].set_ylabel("best RMS so far", fontsize=7)
        ax[2, i].plot(tj[i]["d_true"], tj[i]["L_true"], "r*", ms=12); ax[2, i].set_xlabel("d", fontsize=7); ax[2, i].set_ylabel("L", fontsize=7)
        ax[2, i].set_xlim(*d.D_RANGE); ax[2, i].set_ylim(*d.L_RANGE)
    import textwrap
    fig.suptitle(textwrap.fill("Inverse Schnakenberg design: SIMULATED, synthetic targets, model units, n=6. Circles Sobol, triangles elite search, star = true parameters (never shown to either method). "
                 "Colour log10 RMS. Dotted: gate B 0.02 (drawn only where gate A is met; T5 is unpatterned, success undefined). All u(x) panels share one scale. "
                 "Wrong-IC control failed on T5 only (red). No biological claim.", 190), fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(png, dpi=110); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("png"); a = ap.parse_args(); render(a.out, a.png)
