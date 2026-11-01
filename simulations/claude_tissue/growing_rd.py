"""Sim D: Turing pattern on a laterally GROWING domain (fin width widens during development).
1-D Schnakenberg (same kinetics as Sim A) on x in [0, W(t)], W(t)=W0*exp(g t); no-flux ends.
Domain growth is uniform (IMEX, DCT-implicit Neumann diffusion) and isotropic along x with dilution term -g*c (conservative advection),
implemented on a fixed computational grid in the comoving coordinate.  Question: how does the
number of peaks ('rays') at final width depend on growth rate g and on a perturbation of the
diffusion ratio d, and is it history-dependent (insertion events vs. fixed wavelength)?
SIMULATED; dimensionless; the map from peaks to fin rays is a stated assumption only."""
import json, sys, time, pathlib, numpy as np
from scipy.fft import dct, idct
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
OUT = ROOT / "artifacts/simulations/claude-tissue-growing-rd"
A, B, GAM = 0.1, 0.9, 1.0
N, W0, W_END = 128, 12.0, 48.0
SEEDS = [1, 2, 3, 4, 5]
DS = [15, 20, 30]
TGROW = [0.0, 100.0, 300.0, 1000.0]    # time to grow W0 -> W_END (0 = static control at W_END)

def count_peaks(u):
    c = u - u.mean(); thr = 0.25*(u.max() - u.min())
    pk = [i for i in range(1, len(u)-1) if u[i] > u[i-1] and u[i] >= u[i+1] and (u[i]-u.mean()) > thr]
    return len(pk)

def run(d, T, seed, record=False):
    rng = np.random.default_rng(seed); u0 = A + B; v0 = B/u0**2
    x0 = np.linspace(0, 1, N); u = u0 + 0.01*rng.standard_normal(N); v = v0 + 0.01*rng.standard_normal(N)
    static = T == 0.0; dt = 0.02; lam = (np.pi*np.arange(N))**2   # Neumann cosine eigenvalues on comoving [0,1]
    tsim = 400.0 if static else T + 200.0   # +200 relaxation after growth stops
    g = 0.0 if static else np.log(W_END/W0)/T
    W = W_END if static else W0; hist = []
    nsteps = int(tsim/dt)
    for i in range(nsteps):
        t = i*dt
        if (not static) and t < T: W = W0*np.exp(g*t); gg = g
        else: gg = 0.0; W = W if static else W_END
        L2 = 1.0/W**2
        fu = GAM*(A - u + u*u*v); fv = GAM*(B - u*u*v)
        un = u + dt*(fu - gg*u); vn = v + dt*(fv - gg*v)       # explicit reaction + dilution
        u = idct(dct(un, norm="ortho")/(1 + dt*L2*lam), norm="ortho")  # implicit diffusion
        v = idct(dct(vn, norm="ortho")/(1 + dt*d*L2*lam), norm="ortho")
        if record and i % int(nsteps/120) == 0: hist.append((t, W, u.copy()))
    return u, hist

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True); rows = []; keep = {}
    for d in DS:
        for T in TGROW:
            for s in SEEDS:
                u, h = run(d, T, s, record=(s == SEEDS[0] and d == 20))
                rows.append(dict(d=d, T_grow=T, seed=s, n_peaks=count_peaks(u), amplitude=float(u.std())))
                if h: keep[T] = h
            print(d, T, [r["n_peaks"] for r in rows[-len(SEEDS):]], flush=True)
    (OUT/"sweep.json").write_text(json.dumps(dict(A=A, B=B, gamma=GAM, N=N, W0=W0, W_END=W_END, rows=rows), indent=1))
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    for d in DS:
        m = [np.mean([r["n_peaks"] for r in rows if r["d"] == d and r["T_grow"] == T]) for T in TGROW]
        sd = [np.std([r["n_peaks"] for r in rows if r["d"] == d and r["T_grow"] == T]) for T in TGROW]
        ax[0].errorbar(range(len(TGROW)), m, sd, marker="o", label=f"d={d}")
    ax[0].set_xticks(range(len(TGROW))); ax[0].set_xticklabels(["static" if T == 0 else f"T={T:g}" for T in TGROW])
    ax[0].set_ylabel("peaks at W=48 (5 seeds)"); ax[0].set_title("SIMULATED: peak number vs growth time"); ax[0].legend()
    for T, c in [(100.0, "tab:red"), (1000.0, "tab:blue")]:
        h = keep[T]; img = np.array([hh[2] for hh in h]); ax[1 if T == 100.0 else 2].imshow(img, aspect="auto", cmap="magma", origin="lower")
        ax[1 if T == 100.0 else 2].set_title(f"u(x,t), d=20, seed 1, T_grow={T:g} (comoving x)"); ax[1 if T == 100.0 else 2].set_xlabel("comoving position"); ax[1 if T == 100.0 else 2].set_ylabel("time ->")
    fig.tight_layout(); fig.savefig(OUT/"growing-rd.png", dpi=110)
    outs = [OUT/"sweep.json", OUT/"growing-rd.png"]
    write_receipt(OUT, "claude-tissue-growing-rd", "python3 simulations/claude_tissue/growing_rd.py", SEEDS, [], outs, t0,
                  extra=dict(parameters=dict(A=A, B=B, gamma=GAM, N=N, W0=W0, W_END=W_END, DS=DS, TGROW=TGROW)))
