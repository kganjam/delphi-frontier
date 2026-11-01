"""Posters, videos and repo-format manifests for the three claude-eco models. Reads results.json / receipts written by the model
scripts; every number in a caption is read from those files, not typed. Single-threaded rendering (OMP_NUM_THREADS=1)."""
from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402
from engineering.ecology_sims.escape_ecology import series  # noqa: E402

FPS = 12
plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "figure.dpi": 100})
COL = {"ancestor (halfbeak-like)": "#7a8b99", "intermediate (flying-halfbeak p)": "#d08c2c", "target (Exocoetus-like)": "#1f6fb2"}
HYP_LABEL = {"vis": "H_vis (airborne distance breaks visual tracking)", "chase": "H_chase (only out-running the chase counts)", "both": "H_vis and H_chase"}
SIM = "SIMULATION, not an observation"


def writer():
    return FFMpegWriter(fps=FPS, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "23", "-threads", "1"])


def fish_topview(ax, z, P, x0=0.0, scale=1.0, color="#1f6fb2"):
    mo = C.morphology(z["p"], z["A"], z["M"], z["c"], P)
    SL = float(mo["SL"]) * scale; L = float(mo["L_fin"]) * scale; chord = L / z["A"]
    w = P["w_body_frac"] * SL
    t = np.linspace(0, 2 * np.pi, 80)
    ax.fill(x0 + SL / 2 * np.cos(t), w / 2 * np.sin(t), color=color, alpha=0.9, lw=0)
    root = x0 + 0.2 * SL
    for s in (1, -1):
        ax.fill([root - chord * 0.5, root + chord * 0.5, root - 0.15 * L, root - 0.25 * L - chord * 0.3],
                [s * w / 2, s * w / 2, s * (w / 2 + L), s * (w / 2 + L * 0.98)], color=color, alpha=0.55, lw=0)
    tail = x0 - SL / 2
    up, lo = 0.12 * SL * 2 * (1 - z["c"]), 0.12 * SL * 2 * z["c"]
    ax.fill([tail, tail - 0.18 * SL, tail - 0.05 * SL], [0, up, 0], color=color, alpha=0.7, lw=0)
    ax.fill([tail, tail - 0.18 * SL, tail - 0.05 * SL], [0, -lo, 0], color=color, alpha=0.7, lw=0)


# ---------------------------------------------------------------------------------------------------- reachability
def render_reach(d, P):
    res = json.loads((d / "results.json").read_text())
    with open(d / "_keep.pkl", "rb") as fh:
        keep = pickle.load(fh)
    runs = res["runs"]
    get = lambda s, h: next(r for r in runs if r["setting"] == s and r["hypothesis"] == h)
    # poster: (a) W over p x c slice at ancestor A, M for H_both; (b) W along the Lande walk for three hypotheses; (c) maximin path dW
    fig, axs = plt.subplots(1, 3, figsize=(12.8, 4.6))
    g, a, t, r, W, path, traj, gradn, dist, s, Wl, rl = keep["both"]
    ia = [int(np.argmin(np.abs(g[k] - a[k]))) for k in ("p", "A", "M", "c")]
    sl = W[:, ia[1], ia[2], :]
    im = axs[0].pcolormesh(g["c"], g["p"], sl, shading="auto", cmap="viridis", vmin=0.3, vmax=1)
    fig.colorbar(im, ax=axs[0], label="W (escape per attack)")
    axs[0].plot(traj[:, 3], traj[:, 0], color="w", lw=2, label="Lande walk (H_vis+H_chase)")
    axs[0].plot(a["c"], a["p"], "o", color="#ff9f1c", ms=8, label="halfbeak-like ancestor")
    axs[0].plot(t["c"], t["p"], "*", color="#e63946", ms=13, label="Exocoetus-like target")
    axs[0].set(xlabel="hypocaudal share c", ylabel="pectoral length / SL  p", title=f"(a) W slice at ancestral A={a['A']:.1f}, M={a['M']*1000:.0f} g")
    axs[0].legend(fontsize=7, loc="lower right")
    for h, col in (("vis", "#2a9d8f"), ("chase", "#e76f51"), ("both", "#264653")):
        k = keep[h]; tr = k[6]
        Wt = []
        from scipy.interpolate import RegularGridInterpolator
        f = RegularGridInterpolator([k[0]["p"], np.log(k[0]["A"]), np.log(k[0]["M"]), k[0]["c"]], k[4], bounds_error=False, fill_value=None)
        Wt = f(tr)
        axs[1].plot(np.arange(len(Wt)), Wt, color=col, label=HYP_LABEL[h])
    axs[1].set(xlabel="generation (Lande walk, CV_A = 0.05)", ylabel="W along the walk", title="(b) selection-driven walk from the ancestor", xscale="symlog")
    axs[1].legend(fontsize=7)
    for h, col in (("vis", "#2a9d8f"), ("chase", "#e76f51"), ("both", "#264653")):
        k = keep[h]; Wg = k[4]; pth = k[5]
        dW = [Wg[pth[i + 1]] - Wg[pth[i]] for i in range(len(pth) - 1)]
        axs[2].plot(np.arange(1, len(dW) + 1), dW, ".-", color=col, ms=3, label=f"{h}: worst step {min(dW):.1e}")
    axs[2].axhline(0, color="k", lw=0.6)
    axs[2].set(xlabel="step on the best (maximin) single-trait path", ylabel="dW per step", title="(c) accessible path ancestor -> target", yscale="symlog")
    axs[2].set_yscale("symlog", linthresh=1e-5)
    axs[2].legend(fontsize=7)
    fig.suptitle(f"Reachability on a model escape-fitness landscape | {SIM} | does not show that the transition happened", fontsize=10)
    fig.tight_layout()
    fig.savefig(d / "poster.png", dpi=110); plt.close(fig)
    # video: the H_both Lande walk, phenotype + airborne path + W
    k = keep["both"]; tr = k[6]
    from scipy.interpolate import RegularGridInterpolator
    f = RegularGridInterpolator([k[0]["p"], np.log(k[0]["A"]), np.log(k[0]["M"]), k[0]["c"]], k[4], bounds_error=False, fill_value=None)
    Wt = f(tr)
    gens = np.unique(np.r_[0, np.geomspace(1, len(tr) - 1, 110).astype(int)])
    states = [{"p": tr[i, 0], "A": math.exp(tr[i, 1]), "M": math.exp(tr[i, 2]), "c": tr[i, 3]} for i in gens]
    ser = [series(z, P, stride=6) for z in states]
    st = series(t, P, stride=6)
    fig = plt.figure(figsize=(12.8, 7.2))
    gs = fig.add_gridspec(2, 3)
    ax1 = fig.add_subplot(gs[0, 0]); ax2 = fig.add_subplot(gs[0, 1:]); ax3 = fig.add_subplot(gs[1, :2]); ax4 = fig.add_subplot(gs[1, 2])
    w = writer()
    with w.saving(fig, str(d / "reachability.mp4"), dpi=100):
        for fi, (gi, z, s_) in enumerate(zip(gens, states, ser)):
            for ax in (ax1, ax2, ax3, ax4):
                ax.cla()
            fish_topview(ax1, z, P, color="#264653"); ax1.set_aspect("equal"); ax1.set_xlim(-0.14, 0.12); ax1.set_ylim(-0.16, 0.16); ax1.axis("off")
            ax1.set_title(f"generation {gi}\np={z['p']:.2f}  A={z['A']:.1f}  M={z['M']*1000:.0f} g  c={z['c']:.2f}", fontsize=9)
            ax2.plot(st["x"], st["h"], color="#e63946", lw=1, ls="--", label="Exocoetus-like target")
            ax2.plot(s_["x"], s_["h"], color="#264653", lw=2, label="current phenotype")
            ax2.set(xlim=(0, 45), ylim=(0, 3.5), xlabel="horizontal distance (m)", ylabel="height (m)", title=f"airborne path: {s_['d']:.1f} m in {s_['t_air']:.2f} s (project point-mass glide)")
            ax2.legend(fontsize=8, loc="upper right")
            ax3.plot(np.arange(len(Wt)), Wt, color="#bbb"); ax3.plot(np.arange(gi + 1), Wt[: gi + 1], color="#264653", lw=2)
            ax3.set(xscale="symlog", ylim=(0.3, 1.02), xlabel="generation", ylabel="W (escape per attack)", title="selection-driven walk, H_vis + H_chase, escape-only fitness (kappa_fin = 0)")
            ax4.plot(tr[:, 3], tr[:, 0], color="#bbb"); ax4.plot(tr[: gi + 1, 3], tr[: gi + 1, 0], color="#264653", lw=2)
            ax4.plot(t["c"], t["p"], "*", color="#e63946", ms=12); ax4.set(xlabel="c", ylabel="p", xlim=(0.45, 0.70), ylim=(0.1, 0.8), title="trait path (p, c)")
            fig.suptitle(f"{SIM}. A model of reachability is not evidence that it happened.", fontsize=10)
            fig.tight_layout()
            for _ in range(1 if fi < len(gens) - 1 else FPS * 2):
                w.grab_frame()
    plt.close(fig)
    return res


# ---------------------------------------------------------------------------------------------------- escape ecology
def render_escape(d, P):
    res = json.loads((d / "results.json").read_text())
    with open(d / "_series.pkl", "rb") as fh:
        ser = pickle.load(fh)
    fig, axs = plt.subplots(1, 3, figsize=(12.8, 4.6))
    U = np.array(res["escape_vs_U_burst"]["U_burst_m_s"])
    for k, col in COL.items():
        axs[0].plot(U, res["escape_vs_U_burst"]["curves"][f"{k}|both|t_burst=2.0"], color=col, lw=2, label=k)
        axs[0].plot(U, res["escape_vs_U_burst"]["curves"][f"{k}|chase|t_burst=2.0"], color=col, lw=1, ls="--")
    axs[0].axhline(P["e_swim"], color="k", lw=0.7, ls=":", label="stays in water (e_swim, assumed)")
    axs[0].axvspan(5.21, 20.46, color="#ccc", alpha=0.35, label="FishBase T. albacares burst rows")
    axs[0].set(xlabel="predator burst speed (m/s), burst 2 s", ylabel="escape probability per attack", title="(a) solid H_vis+H_chase, dashed H_chase only", ylim=(0, 1.02))
    axs[0].legend(fontsize=7, loc="lower left")
    sm = res["size_map"]
    gm = np.array(sm["gain"]["k=18.8|both"])
    im = axs[1].pcolormesh(np.array(sm["pred_SL_m"]) * 100, np.array(sm["prey_SL_m"]) * 100, gm, shading="auto", cmap="RdBu", vmin=-0.7, vmax=0.7)
    axs[1].contour(np.array(sm["pred_SL_m"]) * 100, np.array(sm["prey_SL_m"]) * 100, np.array(sm["gain"]["k=18.8|chase"]), levels=[0.05], colors="k", linewidths=1)
    fig.colorbar(im, ax=axs[1], label="escape gain over staying in the water")
    axs[1].set(xlabel="predator SL (cm); burst = 18.8 SL/s (FishBase row)", ylabel="prey SL (cm), Exocoetus-like shape", title="(b) where leaving the water pays\n(black: H_chase-only gain = 0.05)")
    am = res["aerial_map"]
    im = axs[2].pcolormesh(am["U_burst_m_s"], am["beta_air_per_s"], np.array(am["gain_both"]), shading="auto", cmap="RdBu", vmin=-0.7, vmax=0.7)
    axs[2].contour(am["U_burst_m_s"], am["beta_air_per_s"], np.array(am["gain_both"]), levels=[0], colors="k")
    fig.colorbar(im, ax=axs[2], label="gain (target phenotype)")
    axs[2].set(xlabel="predator burst speed (m/s)", ylabel="aerial predator hazard while airborne (1/s)", title="(c) underwater vs aerial predators\n(black: gain = 0)")
    fig.suptitle(f"Glide as predator escape | {SIM} | encounter and hazard rates are swept assumptions", fontsize=10)
    fig.tight_layout(); fig.savefig(d / "poster.png", dpi=110); plt.close(fig)
    # video: race of the three phenotypes vs a predator under the surface
    Ub, tb, Us = P["U_burst"], P["t_burst"], P["U_sus"]
    T = max(s["t"][-1] for s in ser.values()) + 0.6
    ts = np.arange(0, T, 1 / FPS / 0.5 * 0.5) if False else np.arange(0, T + 1e-9, 0.04)
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    w = writer()
    pred_x = lambda t: Ub * min(t, tb) + Us * max(0, t - tb)
    with w.saving(fig, str(d / "escape.mp4"), dpi=100):
        for ti, t in enumerate(ts):
            ax.cla()
            ax.axhspan(-1.2, 0, color="#cfe8f3"); ax.axhline(0, color="#4a90b8", lw=1)
            for (k, s), col in zip(ser.items(), COL.values()):
                on = s["t"] <= t
                ax.plot(s["x"][on], s["h"][on], color=col, lw=2)
                if t <= s["t"][-1]:
                    j = int(np.searchsorted(s["t"], t)); j = min(j, len(s["x"]) - 1)
                    ax.plot(s["x"][j], s["h"][j], "o", color=col, ms=8)
                else:
                    ax.plot(s["x"][-1], 0, "v", color=col, ms=8)
                res_k = res["phenotypes"][k]
                ax.text(0.01, 0.95 - 0.06 * list(ser).index(k), f"{k}: {res_k['airborne_distance_m']:.1f} m airborne in {res_k['airborne_time_s']:.2f} s; escape (H_vis+H_chase) {res_k['escape_both']:.2f}",
                        transform=ax.transAxes, color=col, fontsize=10)
            px = pred_x(t)
            ax.plot(px, -0.6, ">", color="#333", ms=16); ax.text(px, -1.0, f"predator {Ub if t < tb else Us:.2f} m/s", ha="center", fontsize=8)
            ax.set(xlim=(-2, 42), ylim=(-1.2, 3.6), xlabel="horizontal distance (m)", ylabel="height (m)",
                   title=f"t = {t:.2f} s | predator bursts {Ub} m/s for {tb} s then {Us} m/s (FishBase rows) | {SIM}")
            w.grab_frame()
        for _ in range(FPS * 2):
            w.grab_frame()
    plt.close(fig)
    return res


# ---------------------------------------------------------------------------------------------------- collective
def render_collective(d, P):
    res = json.loads((d / "results.json").read_text())
    with open(d / "_frames.pkl", "rb") as fh:
        fr = pickle.load(fh)
    fig, axs = plt.subplots(1, 2, figsize=(12.8, 4.8))
    Ns = sorted({int(k.split("|")[1]) for k in res["main"]})
    styles = {"glide_sync": ("#1f6fb2", "-", "glide + alarm cascade (synchronised emergence)"), "glide_indep": ("#2a9d8f", "--", "glide, each fish on its own detection"),
              "swim_sync": ("#e76f51", "-.", "swim + alarm cascade (control)"), "swim": ("#7a8b99", ":", "swim only (control)")}
    for cond, (col, ls, lab) in styles.items():
        pe = [res["main"][f"{cond}|{N}"]["P_capture_episode"] for N in Ns]; se = [res["main"][f"{cond}|{N}"]["se"] for N in Ns]
        pc = [res["main"][f"{cond}|{N}"]["per_capita"] for N in Ns]; pcs = [res["main"][f"{cond}|{N}"]["per_capita_se"] for N in Ns]
        axs[0].errorbar(Ns, pe, yerr=1.96 * np.array(se), color=col, ls=ls, marker="o", ms=4, label=lab, capsize=2)
        axs[1].errorbar(Ns, pc, yerr=1.96 * np.array(pcs), color=col, ls=ls, marker="o", ms=4, label=lab, capsize=2)
    axs[0].set(xscale="log", xlabel="school size N", ylabel="P(one capture per attack episode)", title="(a) does the attack succeed at all?", ylim=(0, 1.02))
    axs[1].set(xscale="log", yscale="log", xlabel="school size N", ylabel="per-capita capture probability per encounter", title="(b) per-capita risk (= P / N); 95% binomial bars")
    axs[0].legend(fontsize=7)
    fig.suptitle(f"Collective escape, population/behavioural layer | agent-based {SIM} | no rigid-body or hydrodynamic interaction", fontsize=10)
    fig.tight_layout(); fig.savefig(d / "poster.png", dpi=110); plt.close(fig)
    keys = ["glide_sync|32", "glide_indep|32", "swim_sync|32", "glide_sync|1"]
    titles = {"glide_sync|32": "N=32, glide + alarm cascade", "glide_indep|32": "N=32, glide, independent detection", "swim_sync|32": "N=32, swim + alarm (control)", "glide_sync|1": "solitary glider"}
    L = max(len(fr[k]["frames"]) for k in keys)
    fig, axs = plt.subplots(2, 2, figsize=(12.8, 7.2))
    w = writer()
    stride = 2
    with w.saving(fig, str(d / "collective.mp4"), dpi=100):
        for i in range(0, L, stride):
            for ax, k in zip(axs.ravel(), keys):
                ax.cla()
                F = fr[k]["frames"]; t, pos, status, ppos, pm, al = F[min(i, len(F) - 1)]
                cols = np.where(status == 2, "#e63946", np.where(status == 1, "#f4a261", "#1f6fb2"))
                ax.scatter(pos[:, 0], pos[:, 1], c=cols, s=14, edgecolors=np.where(al, "k", "none"), linewidths=0.6)
                ax.plot(ppos[0], ppos[1], marker=(3, 0, 0), color="#333", ms=12)
                ax.set(xlim=(-15, 45), ylim=(-20, 20), aspect="equal")
                ax.set_title(f"{titles[k]}  t={t:.2f} s" + ("  CAPTURE" if (status == 2).any() else ""), fontsize=9)
                ax.tick_params(labelsize=7)
            fig.suptitle(f"blue in water, orange airborne (ground track), red caught, black ring = alerted; triangle = predator | top view, metres | {SIM}", fontsize=9)
            fig.tight_layout()
            w.grab_frame()
        for _ in range(FPS * 2):
            w.grab_frame()
    plt.close(fig)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["reach", "escape", "collective"])
    a = ap.parse_args()
    P = dict(C.DEFAULT)
    d = C.OUT / {"reach": "eco-reachability", "escape": "eco-escape-ecology", "collective": "collective-school-escape"}[a.which]
    {"reach": render_reach, "escape": render_escape, "collective": render_collective}[a.which](d, P)
    print("rendered", d)


if __name__ == "__main__":
    main()
