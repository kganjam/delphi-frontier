#!/usr/bin/env python3
"""Figures for the microcarrier runner (static PNG, light surface). Palette: dataviz reference
categorical order (blue, orange, aqua, yellow), validated in that skill; one y-axis per panel.
usage: mc_figures.py RUNDIR [RUNDIR...] --verdicts V.json --outdir DIR"""
import argparse, glob, json, math, os, re, collections
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
SURF, INK, INK2, GRID = "#fcfcfb", "#1f1f1e", "#5f5e58", "#e4e3dd"
L = 1e-3
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
FOOT = "Voxelyze @4287e365 · generic soft-voxel mechanics on a frictional floor · assumed materials · not tissue, not cilia, not a xenobot"

def load(dirs):
    R = {}
    for d in dirs:
        for rp in glob.glob(os.path.join(d, "*.receipt.json")):
            rec = json.load(open(rp)); o = rp.replace(".receipt.json", ".json")
            if rec["exit_code"] == 0 and os.path.exists(o):
                out = json.load(open(o))
                if not out["numerics"]["diverged"]: R[rec["run"]["id"]] = (rec, out)
    return R

def post(out):
    r = out["result"]; n = max(r["post_transient_cycles"], 1)
    return r["post_transient_dx_m"] / L / n, r["post_transient_dy_m"] / L / n   # body lengths per cycle

def fig_travelling(R, od):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for ax, d, ttl in zip(axes, ["bwd", "fwd"], ["wave travels toward -x", "wave travels toward +x"]):
        for i, f in enumerate([2.5, 5.0, 10.0, 20.0]):
            ks, ys = [], []
            for k in [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4]:
                e = R.get(f"S-trav-x-k{k}-{d}-f{f}")
                if e: ks.append(k); ys.append(post(e[1])[0])
            if ks: ax.plot(ks, ys, "-o", color=C[i], lw=2, ms=4, label=f"{f:g} Hz")
        ax.axhline(0, color=INK2, lw=0.8); ax.axvspan(2, 4.2, color="#efeee9", zorder=0)
        ax.text(3.1, ax.get_ylim()[1] if False else 0, "", fontsize=7)
        ax.set_title(ttl, fontsize=9, loc="left"); ax.set_xlabel("wavenumber k (wavelengths per body)")
    axes[0].set_ylabel("net x displacement per cycle (body lengths)")
    axes[1].legend(title="drive frequency", fontsize=8, title_fontsize=8, frameon=False)
    fig.suptitle("Travelling-wave actuation: displacement depends on wavelength and direction (equal L2 actuation)", fontsize=10, x=0.01, ha="left")
    fig.text(0.01, 0.005, FOOT + "\nshaded: k >= 2 has under 4 voxels per wavelength at mesh 1 (coarse). Mesh 2 at 10 Hz gives about half these magnitudes: not converged.", fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.06, 1, 0.95)); p = os.path.join(od, "pattern-vs-displacement.png"); fig.savefig(p, dpi=150); plt.close(fig); return p

def family(rid):
    for pre, name in [("S-trav-x", "travelling, x"), ("S-trav-k", "travelling, oblique"), ("S-stand", "standing"), ("S-seg", "segmented"),
                      ("S-half", "half-body"), ("S-helix", "helical"), ("S-dvtrav", "dorsoventral wave"), ("S-uniform", "uniform"),
                      ("S-rsmooth", "random smooth phase"), ("S-ramp", "random amplitude"), ("S-riid", "random per-voxel phase"), ("S-off", "passive")]:
        if rid.startswith(pre): return name
    return None

def fig_families(R, od):
    groups = collections.OrderedDict()
    for rid, (rec, out) in R.items():
        if rec["run"]["group"] != "sweep" or rec["run"]["mirror"] != "none": continue
        if rid.startswith("S-trav-x") and rec["run"]["freq"] != 10.0: continue
        fam = family(rid)
        if fam: groups.setdefault(fam, []).append(max(math.hypot(*post(out)), 1e-9))
    order = sorted(groups, key=lambda k: -np.median(groups[k]))
    fig, ax = plt.subplots(figsize=(9, 4.2))
    rng = np.random.default_rng(0)
    for i, k in enumerate(order):
        v = np.array(groups[k]); ax.scatter(v, i + rng.uniform(-0.18, 0.18, v.size), s=12, color=C[0], alpha=0.75, edgecolors=SURF, linewidths=0.5)
        ax.plot([np.median(v)] * 2, [i - 0.3, i + 0.3], color=INK, lw=2)
        ax.annotate(f"n={v.size}", (1.005, i), xycoords=("axes fraction", "data"), va="center", fontsize=7, color=INK2)
    NAMES = {"A": "wave k=1 bwd (A)", "B": "wave k=2 bwd (B)", "M": "oblique wave 30deg (M)", "C": "2-segment alternating (C)", "U": "uniform in-phase (U)",
             "T05b": "wave k=0.5 bwd", "T05f": "wave k=0.5 fwd", "S4b": "4-segment bwd", "St1": "standing wave k=1", "H1": "helical wave",
             "R1": "random smooth (seed)", "I1": "random per-voxel (seed)"}
    ax.set_yticks(range(len(order))); ax.set_yticklabels([NAMES.get(k, k) for k in order], fontsize=8); ax.invert_yaxis(); ax.set_xscale("log")
    ax.set_xlabel("|net displacement| per cycle, body lengths (log; passive floored at 1e-9)"); ax.grid(axis="y", visible=False)
    fig.suptitle("All sweep patterns at 10 Hz, mesh 1: displacement by family (dots = patterns, bar = median)", fontsize=10, x=0.01, ha="left")
    fig.text(0.01, 0.005, FOOT + "\nMagnitude includes the y component; at mesh 1 that contains a lateral solver-anisotropy artifact (see mirror results), so random families are likely inflated.", fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.06, 0.97, 0.95)); p = os.path.join(od, "sweep-families.png"); fig.savefig(p, dpi=150); plt.close(fig); return p

def fig_refinement(R, V, od):
    e2 = V.get("E2", {})
    if "d_A_L" not in e2: return None
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.4), sharex="col")
    dts = ["0.5", "0.25", "0.125", "0.0625"]; ms = ["1", "2", "3"]; n = 5
    for i, (t, name) in enumerate([("A", "A: k=1 wave"), ("B", "B: k=2 wave")]):
        d = e2[f"d_{t}_L"]
        for row, comp in ((0, 0), (1, 1)):
            axes[row, 0].plot([float(x) for x in dts], [d[f"m1-dt{x}"][comp] / n for x in dts], "-o", color=C[i], lw=2, ms=5, label=name)
            axes[row, 1].plot([int(m) for m in ms], [d[f"m{m}-dt0.5"][comp] / n for m in ms], "-o", color=C[i], lw=2, ms=5, label=name)
            axes[row, 1].plot([2], [d["m2-dt0.25"][comp] / n], "s", color=C[i], ms=6, mfc=SURF, mew=1.5)
    axes[1, 0].set_xscale("log", base=2); axes[1, 0].invert_xaxis(); axes[1, 0].set_xlabel("dt / recommended dt (mesh 1)")
    axes[1, 1].set_xticks([1, 2, 3]); axes[1, 1].set_xticklabels(["8x4x4", "16x8x8", "24x12x12"]); axes[1, 1].set_xlabel("mesh (dt 0.5; open square: mesh 2 at dt 0.25)")
    axes[0, 0].set_ylabel("x per cycle (body lengths)"); axes[1, 0].set_ylabel("y (lateral) per cycle (body lengths)")
    for ax in axes.flat: ax.axhline(0, color=INK2, lw=0.8)
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[1, 1].annotate("B's lateral drift at mesh 1 vanishes\nwith refinement: a solver artifact", xy=(1, e2["d_B_L"]["m1-dt0.5"][1] / n), xytext=(1.6, 0.0045), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    fig.suptitle(f"Endpoint 2 refinement series: D at mesh 3 = {e2['D_L_by_level']['m3-dt0.5']:.2g} L vs envelope R = {e2['R_envelope_L']:.2g} L -> {e2['verdict']}\n"
                 "In x, the k=1 and k=2 waves converge to nearly the same speed; the mesh-1 difference was lateral artifact.", fontsize=9.5, x=0.01, ha="left")
    fig.text(0.01, 0.005, FOOT + "\nmesh-consistent damping · E1 FAILED at mesh 3 (diagnosed numerical, <= 7.3e-6 L)", fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.05, 1, 0.92)); p = os.path.join(od, "refinement.png"); fig.savefig(p, dpi=150); plt.close(fig); return p

def fig_robust(R, od):
    pats = collections.OrderedDict()
    for rid, (rec, out) in R.items():
        m = re.match(r"X-(\w+)-mu([\d.]+)-amp([\d.]+)-E(\d+)", rid)
        if m: pats.setdefault(m.group(1), []).append((float(m.group(2)), float(m.group(3)), int(m.group(4)), math.hypot(*post(out))))
    if not pats: return None
    order = sorted(pats, key=lambda k: -np.median([x[3] for x in pats[k]]))
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for i, k in enumerate(order):
        v = np.array([max(x[3], 1e-9) for x in pats[k]])
        ax.scatter(v, np.full(v.size, i) + np.linspace(-0.2, 0.2, v.size), s=10, color=C[2], alpha=0.8, edgecolors=SURF, linewidths=0.4)
        ax.plot([np.median(v)] * 2, [i - 0.3, i + 0.3], color=INK, lw=2)
    NAMES = {"A": "wave k=1 bwd (A)", "B": "wave k=2 bwd (B)", "M": "oblique wave 30deg (M)", "C": "2-segment alternating (C)", "U": "uniform in-phase (U)",
             "T05b": "wave k=0.5 bwd", "T05f": "wave k=0.5 fwd", "S4b": "4-segment bwd", "St1": "standing wave k=1", "H1": "helical wave",
             "R1": "random smooth (seed)", "I1": "random per-voxel (seed)"}
    ax.set_yticks(range(len(order))); ax.set_yticklabels([NAMES.get(k, k) for k in order], fontsize=8); ax.invert_yaxis(); ax.set_xscale("log"); ax.grid(axis="y", visible=False)
    ax.set_xlabel("|net displacement| per cycle, body lengths (27 combinations of friction x amplitude x modulus per pattern)")
    fig.suptitle("Exploratory robustness grid: does the ranking survive the three assumed parameters?", fontsize=10, x=0.01, ha="left")
    fig.text(0.01, 0.005, FOOT + " · not preregistered", fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 0.95)); p = os.path.join(od, "robustness.png"); fig.savefig(p, dpi=150); plt.close(fig); return p

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+"); ap.add_argument("--verdicts"); ap.add_argument("--outdir", required=True)
    a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True); R = load(a.dirs)
    V = json.load(open(a.verdicts)) if a.verdicts and os.path.exists(a.verdicts) else {}
    for f in (fig_travelling(R, a.outdir), fig_families(R, a.outdir), fig_refinement(R, V, a.outdir), fig_robust(R, a.outdir)): print(f)
