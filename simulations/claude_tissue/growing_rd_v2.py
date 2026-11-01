"""Sim D v2: Turing pattern on a growing 1-D domain over a 12x width increase (v1 covered only 4x,
which holds ~4 peaks, too few to tell peak insertion from mode doubling).
Same Schnakenberg kinetics and comoving-grid scheme as v1 (exponential uniform growth with
dilution, Neumann ends, IMEX with DCT-implicit diffusion).  Readout: peak count n(t) versus
the static-wavelength expectation W(t)/lambda*, and the kind of transition events
(+1/+2 insertions vs near-doubling) along each trajectory.
Question for the transfer function: does ray/peak number track width (n ~ W/lambda*) or lag it
(history dependence), and how does that depend on growth rate relative to patterning rate?
SIMULATED; dimensionless; peaks -> fin rays is an assumption."""
import json, sys, time, pathlib, numpy as np
from scipy.fft import dct, idct
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
from claude_tissue.growing_rd import count_peaks
import claude_tissue.rd_wavelength as rw

OUT = ROOT / "artifacts/simulations/claude-tissue-growing-rd"
A, B, GAM = 0.1, 0.9, 1.0
N, W0, W_END = 384, 12.0, 144.0
SEEDS = [1, 2, 3, 4, 5]
DS = [15, 20, 30]
TGROW = [250.0, 1000.0, 4000.0]
DT = 0.02; RELAX = 200.0; NREC = 160

def run(d, T, seed):
    rng = np.random.default_rng(seed); u0 = A + B; v0 = B/u0**2
    u = u0 + 0.01*rng.standard_normal(N); v = v0 + 0.01*rng.standard_normal(N)
    lam = (np.pi*np.arange(N))**2; g = np.log(W_END/W0)/T
    nsteps = int((T + RELAX)/DT); every = max(1, nsteps//NREC); rec = []
    for i in range(nsteps):
        t = i*DT
        if t < T: W = W0*np.exp(g*t); gg = g
        else: W = W_END; gg = 0.0
        L2 = 1.0/W**2
        uuv = u*u*v
        un = u + DT*(GAM*(A - u + uuv) - gg*u); vn = v + DT*(GAM*(B - uuv) - gg*v)
        u = idct(dct(un, norm="ortho")/(1 + DT*L2*lam), norm="ortho")
        v = idct(dct(vn, norm="ortho")/(1 + DT*d*L2*lam), norm="ortho")
        if i % every == 0: rec.append((t, W, count_peaks(u), u[::3].copy()))
    if not np.isfinite(u).all(): raise RuntimeError("non-finite")
    return u, rec

def events(ns):
    ev = []
    for a, b in zip(ns[:-1], ns[1:]):
        if b != a: ev.append(int(b - a))
    return ev

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True); rows = []; keep = {}
    for d in DS:
        rw.A, rw.B = A, B; kst = rw.linear_kmax(d, GAM)[0]; lam_star = 2*np.pi/kst
        for T in TGROW:
            for s in SEEDS:
                u, rec = run(d, T, s)
                ts = np.array([r[0] for r in rec]); Ws = np.array([r[1] for r in rec]); ns = np.array([r[2] for r in rec])
                ev = events(ns)
                late = ts > 0.25*T     # ignore initial pattern formation
                rows.append(dict(d=d, T_grow=T, seed=s, growth_rate=float(np.log(W_END/W0)/T), lambda_star=lam_star,
                                 n_final=int(count_peaks(u)), n_expected_final=float(W_END/lam_star),
                                 wavelength_final=float(W_END/max(count_peaks(u), 1)),
                                 n_vs_W=[[float(w), int(n)] for w, n in zip(Ws[::4], ns[::4])],
                                 mean_abs_lag_peaks=float(np.mean(np.abs(ns[late] - Ws[late]/lam_star))),
                                 events=ev, n_events=len(ev), max_jump=int(max(ev)) if ev else 0,
                                 n_negative_events=int(sum(1 for e in ev if e < 0))))
                if s == SEEDS[0] and d == 20: keep[T] = rec
            sub = rows[-len(SEEDS):]
            print(d, T, "n_final", [r["n_final"] for r in sub], "expected", round(W_END/lam_star, 1),
                  "max_jump", [r["max_jump"] for r in sub], flush=True)
    (OUT/"sweep-v2.json").write_text(json.dumps(dict(version=2, A=A, B=B, gamma=GAM, N=N, W0=W0, W_END=W_END, dt=DT, relax=RELAX, rows=rows), indent=1))
    fig, ax = plt.subplots(1, 4, figsize=(20, 4.6))
    for T, c in zip(TGROW, ["tab:red", "tab:orange", "tab:blue"]):
        for d, mk in zip(DS, ["o", "s", "^"]):
            rs = [r for r in rows if r["d"] == d and r["T_grow"] == T]
            for r in rs[:1]:
                a = np.array(r["n_vs_W"]); ax[0].plot(a[:, 0], a[:, 1], color=c, alpha=0.8, lw=1, label=f"T={T:g}" if d == 20 else None)
    for d in DS:
        rw.A, rw.B = A, B; ls = 2*np.pi/rw.linear_kmax(d, GAM)[0]; w = np.linspace(W0, W_END, 50); ax[0].plot(w, w/ls, "k:", lw=0.8)
    ax[0].set_xlabel("domain width W"); ax[0].set_ylabel("peak count"); ax[0].set_title("SIMULATED peak count vs width (dotted: W/lambda*)"); ax[0].legend(fontsize=7)
    for j, d in enumerate(DS):
        m = [np.mean([r["n_final"] for r in rows if r["d"] == d and r["T_grow"] == T]) for T in TGROW]
        sd = [np.std([r["n_final"] for r in rows if r["d"] == d and r["T_grow"] == T]) for T in TGROW]
        ax[1].errorbar(np.arange(3) + 0.08*j, m, sd, marker="o", label=f"d={d} (W/lambda*={W_END/(2*np.pi/rw.linear_kmax(d, GAM)[0]):.1f})")
    ax[1].set_xticks(range(3)); ax[1].set_xticklabels([f"T={T:g}" for T in TGROW]); ax[1].set_ylabel("final peaks (5 seeds)"); ax[1].legend(fontsize=7)
    ax[1].set_title("final peak number vs growth time")
    for k, T in enumerate([TGROW[0], TGROW[-1]]):
        rec = keep[T]; img = np.array([r[3] for r in rec]); ax[2 + k].imshow(img, aspect="auto", cmap="magma", origin="lower")
        ax[2 + k].set_title(f"u(comoving x, t), d=20, seed 1, T_grow={T:g}"); ax[2 + k].set_xlabel("comoving position"); ax[2 + k].set_ylabel("record index (time)")
    fig.tight_layout(); fig.savefig(OUT/"growing-rd-v2.png", dpi=110)
    outs = [OUT/"sweep-v2.json", OUT/"growing-rd-v2.png"]
    write_receipt(OUT, "claude-tissue-growing-rd-v2", "python3 simulations/claude_tissue/growing_rd_v2.py", SEEDS, [], outs, t0,
                  extra=dict(parameters=dict(A=A, B=B, gamma=GAM, N=N, W0=W0, W_END=W_END, DS=DS, TGROW=TGROW, dt=DT, relax=RELAX)))
