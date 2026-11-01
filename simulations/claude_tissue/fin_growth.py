"""Sim B: morphogen-gradient -> pectoral-fin elongation, with perturbations.
1-D proximo-distal axis, morphogen source at the distal tip (flux P), diffusion D, first-order
decay k, no-flux at base.  Quasi-steady gradient on the growing domain:
    m(x)/K = p * cosh(x/l) / sinh(L/l),  l = sqrt(D/k),  p = P*l/(D*K)
Local growth rate (1/day) = r * h(m),  h = m/(K+m)  (saturating, declared form, no source).
dL/dt = r * integral_0^L h(m(x)) dx.  Body: SL(t) = SL0 + s*t (linear, declared).
Output: pectoral/SL ratio vs SL.  SIMULATED; parameters are anchored loosely to the descriptive
flying-fish allometry fit, which is anchoring, not validation (no calibration is registered)."""
import json, sys, time, csv, pathlib, subprocess, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

OUT = ROOT / "artifacts/simulations/claude-tissue-fin-growth"
DATA = pathlib.Path("artifacts/observed-allometry/source-observations.csv")
SL0, L0 = 1.5, 0.45          # cm at t=0 (declared; observed min flying-fish SL is 1.68)
BASE = dict(P=0.01, D=0.02, k=0.02, K=0.5, r=0.0, s=0.2)  # r set below by anchor; units: P~K*cm/day*..., D cm^2/day, k 1/day
SL_END = 24.0                # observed flying-fish SL max

def load_obs(group="flying fish"):
    rows = [r for r in csv.DictReader(open(ROOT/DATA)) if r["group"] == group]
    return np.array([[float(r["sl_cm"]), float(r["pectoral_cm"])] for r in rows])

def simulate(th, n_out=200, sl_end=SL_END):
    P, D, k, K, r, s = (th[x] for x in ("P", "D", "k", "K", "r", "s"))
    l = np.sqrt(D/k); p = P*l/(D*K)
    T = (sl_end - SL0)/s; dt = 0.2; L = L0; ts = [0.0]; Ls = [L]; xs = None
    nsteps = int(T/dt)
    def rate(L):
        x = np.linspace(0, L, 80); z = L/l
        # log-space cosh/sinh for stability
        lr = np.log(p) + np.logaddexp(x/l, -x/l) - z - np.log1p(-np.exp(-2*z))   # log[p cosh(x/l)/sinh(L/l)], overflow-safe
        m = np.exp(np.minimum(lr, 50)); h = m/(1 + m)
        return r*np.trapezoid(h, x)
    for i in range(nsteps):
        k1 = rate(L); k2 = rate(L + 0.5*dt*k1); L = L + dt*k2   # midpoint
        ts.append((i+1)*dt); Ls.append(L)
    ts = np.array(ts); Ls = np.array(Ls); SL = SL0 + s*ts
    return ts, SL, Ls

def log_curve(th, sl_grid):
    ts, SL, Ls = simulate(th)
    return np.interp(sl_grid, SL, Ls)

def anchor_r(th, target_ratio, sl=SL_END):
    """bisect r so that L/SL at sl_end equals target (anchoring only)."""
    lo, hi = 1e-4, 5.0
    for _ in range(40):
        mid = np.sqrt(lo*hi); t2 = dict(th, r=mid); _, SL, L = simulate(t2)
        if L[-1]/SL[-1] > target_ratio: hi = mid
        else: lo = mid
    return np.sqrt(lo*hi)

def render_video(path, cases, sl_grid_n=60):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.5)); frames = []
    sims = {n: simulate(th) for n, th in cases.items()}
    nf = 90; cols = {"baseline": "k", "morphogen x2": "tab:red", "morphogen x0.4": "tab:blue"}
    import tempfile, os
    d = tempfile.mkdtemp(dir="/tmp/ct")
    for f in range(nf):
        for a in axs: a.clear()
        for j, (n, (ts, SL, Ls)) in enumerate(sims.items()):
            i = int(f/(nf-1)*(len(ts)-1)); th = cases[n]; l = np.sqrt(th["D"]/th["k"]); p = th["P"]*l/(th["D"]*th["K"])
            L = Ls[i]; x = np.linspace(0, L, 100); m = p*np.cosh(x/l)/np.sinh(L/l)
            y0 = 2-j; axs[0].fill_between(x/SL[i], y0-0.35*np.ones_like(x)*0, y0+0.0, alpha=0)
            axs[0].plot([0, 1], [y0, y0], color="gray", lw=6, solid_capstyle="round", alpha=0.35)  # body = 1 SL
            axs[0].plot([0, L/SL[i]], [y0+0.15, y0+0.15], color=cols[n], lw=5)
            axs[0].text(1.03, y0, f"{n}\nL/SL={L/SL[i]:.2f}", fontsize=8, va="center")
            axs[1].plot(SL[:i+1], Ls[:i+1]/SL[:i+1], color=cols[n], label=n)
        axs[0].set_xlim(-0.05, 1.55); axs[0].set_ylim(-0.6, 2.7); axs[0].axis("off")
        axs[0].set_title(f"SIMULATED fin vs body (SL=1), SL={SL[i]:.1f} cm", fontsize=9)
        axs[1].set_xlim(SL0, SL_END); axs[1].set_ylim(0, 1.2); axs[1].set_xlabel("SL (cm)"); axs[1].set_ylabel("pectoral/SL")
        axs[1].set_title("simulated, not observed", fontsize=9)
        if f == 0: axs[1].legend(fontsize=7)
        fig.tight_layout(); fig.savefig(f"{d}/f{f:03d}.png", dpi=80)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "1", "-framerate", "15", "-i", f"{d}/f%03d.png",
                    "-pix_fmt", "yuv420p", "-c:v", "libx264", str(path)], check=True)
    plt.close(fig)

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    obs = load_obs(); target = float(np.mean(obs[obs[:, 0] > 15, 1]/obs[obs[:, 0] > 15, 0]))   # ratio of observed flying fish SL>15 cm
    base = dict(BASE); base["r"] = anchor_r(base, target)
    print("anchor r =", base["r"], "target ratio", target, flush=True)
    # one-at-a-time perturbations (x0.5, x2 on each parameter), plus duration (SL_END) variation
    res = []; ts, SL, Ls = simulate(base); b_ratio = Ls[-1]/SL[-1]
    sl_grid = np.linspace(2, SL_END, 40); slope = lambda th: np.polyfit(np.log10(sl_grid), np.log10(log_curve(th, sl_grid)), 1)[0]
    b_slope = slope(base)
    for name in ("P", "D", "k", "K", "r", "s"):
        for f in (0.5, 2.0):
            th = dict(base); th[name] *= f; _, S, L = simulate(th)
            res.append(dict(param=name, factor=f, ratio_at_SL24=float(L[-1]/S[-1]), pectoral_cm_at_SL24=float(L[-1]), loglog_slope=float(slope(th)),
                            pct_change_ratio=float(100*(L[-1]/S[-1]/b_ratio - 1))))
    # joint P x ell sweep: map of final ratio
    Pg = base["P"]*np.array([0.25, 0.5, 1, 2, 4]); lg = np.sqrt(base["D"]/base["k"])*np.array([0.5, 0.75, 1, 1.5, 2])
    grid = np.zeros((len(Pg), len(lg)))
    for i, P in enumerate(Pg):
        for j, l in enumerate(lg):
            th = dict(base, P=P, D=base["D"]*(l/lg[2])**2); _, S, L = simulate(th); grid[i, j] = L[-1]/S[-1]
    # observed band: flying-fish ratio at SL>15
    r_obs = obs[obs[:, 0] > 15, 1]/obs[obs[:, 0] > 15, 0]
    summ = dict(baseline=base, baseline_ratio_SL24=float(b_ratio), baseline_slope=float(b_slope), anchor_target_ratio=target, anchor_n=int(len(r_obs)),
                observed_ratio_SL_gt15=dict(min=float(r_obs.min()), max=float(r_obs.max()), mean=float(r_obs.mean()), n=int(len(r_obs))),
                observed_flying_fish_loglog_slope=float(np.polyfit(np.log10(obs[:, 0]), np.log10(obs[:, 1]), 1)[0]),
                oat=res, joint_P_by_l=dict(P=list(Pg), ell=list(lg), ratio=grid.tolist()),
                note="Anchoring: r was bisected so baseline ratio at SL=24 equals the observed flying-fish mean at SL>15 cm. That makes the baseline an anchor, not a validation; perturbation deltas are the result.")
    (OUT/"summary.json").write_text(json.dumps(summ, indent=1))
    # figure
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    for n, f, c in [("baseline", 1, "k"), ("P x2", 2, "tab:red"), ("P x0.5", 0.5, "tab:blue")]:
        th = dict(base); th["P"] *= f; _, S, L = simulate(th); ax[0].plot(S, L/S, color=c, label=n)
    ax[0].axhspan(r_obs.min(), r_obs.max(), color="orange", alpha=0.25, label="observed flying-fish SL>15 cm range")
    ax[0].set_xlabel("SL (cm)"); ax[0].set_ylabel("pectoral/SL"); ax[0].legend(fontsize=7); ax[0].set_title("SIMULATED trajectories vs observed ratio band")
    lab = [f"{r['param']}x{r['factor']:g}" for r in res]; v = [r["pct_change_ratio"] for r in res]
    o = np.argsort(np.abs(v)); ax[1].barh(np.array(lab)[o], np.array(v)[o], color=["tab:red" if x > 0 else "tab:blue" for x in np.array(v)[o]])
    ax[1].set_xlabel("% change in fin/SL at SL=24 cm"); ax[1].set_title("one-at-a-time perturbations (simulated)")
    im = ax[2].imshow(grid, origin="lower", aspect="auto", cmap="viridis"); ax[2].set_xticks(range(5)); ax[2].set_xticklabels([f"{x:.1f}" for x in lg]); ax[2].set_yticks(range(5)); ax[2].set_yticklabels([f"{x:.2g}" for x in Pg])
    ax[2].set_xlabel("gradient length l (cm)"); ax[2].set_ylabel("production P"); ax[2].set_title("fin/SL at SL=24 cm"); fig.colorbar(im, ax=ax[2])
    fig.tight_layout(); fig.savefig(OUT/"fin-growth.png", dpi=110); plt.close(fig)
    cases = {"baseline": base, "morphogen x2": dict(base, P=base["P"]*2), "morphogen x0.4": dict(base, P=base["P"]*0.4)}
    render_video(OUT/"fin-growth.mp4", cases)
    outs = [OUT/"summary.json", OUT/"fin-growth.png", OUT/"fin-growth.mp4"]
    write_receipt(OUT, "claude-tissue-fin-growth", "python3 simulations/claude_tissue/fin_growth.py", "deterministic (ODE; no RNG)", [str(DATA)], outs, t0,
                  extra=dict(parameters=base, SL0=SL0, L0=L0, SL_END=SL_END))
