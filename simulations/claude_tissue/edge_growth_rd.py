"""Sim D3: Turing pattern with growth only at one EDGE (apical/marginal growth), the contrast requested by the
gemini-4-argon review: teleost fin rays are reported to be added sequentially at margins, which uniform growth
(growing_rd_v2: synchronous frequency doubling) does not produce.
1-D Schnakenberg, same kinetics as Sims A/D; fixed grid spacing dx; the domain grows by appending cells at x = W
at speed v (width per time), new cells initialised at the homogeneous steady state; no-flux ends; IMEX
(explicit reaction, implicit banded diffusion).  W grows 12 -> 144 like growing_rd_v2.
Readouts: peak count vs width, jump sizes, and spacing of the final peaks vs lambda*.
SIMULATED; dimensionless; peaks -> rays is an assumption."""
import json, sys, time, pathlib, numpy as np
from scipy.linalg import solve_banded
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
from claude_tissue.growing_rd import count_peaks
import claude_tissue.rd_wavelength as rw

OUT = ROOT/"artifacts/simulations/claude-tissue-growing-rd"
A, B, GAM = 0.1, 0.9, 1.0
DX, W0, W_END, DT = 0.375, 12.0, 144.0, 0.02
DS = [15, 20, 30]
SPEEDS = [0.5, 0.1, 0.03]          # width per time; T_grow = 132/v = 264, 1320, 4400 (comparable to v2's 250/1000/4000)
SEEDS = [1, 2, 3, 4, 5]
RELAX = 200.0

def banded(n, coef):
    ab = np.zeros((3, n)); ab[0, 1:] = -coef; ab[2, :-1] = -coef; ab[1, :] = 1 + 2*coef; ab[1, 0] = ab[1, -1] = 1 + coef
    return ab

def run(d, v, seed):
    rng = np.random.default_rng(seed); u0 = A + B; v0 = B/u0**2
    n = int(round(W0/DX)); u = u0 + 0.01*rng.standard_normal(n); w = v0 + 0.01*rng.standard_normal(n)
    cu, cw = DT/DX**2, d*DT/DX**2; acc = 0.0; T = (W_END - W0)/v; nsteps = int((T + RELAX)/DT)
    rec = []; every = max(1, nsteps//160); abu = banded(n, cu); abw = banded(n, cw)
    for i in range(nsteps):
        uuw = u*u*w
        u = solve_banded((1, 1), abu, u + DT*GAM*(A - u + uuw)); w = solve_banded((1, 1), abw, w + DT*GAM*(B - uuw))
        if i*DT < T:
            acc += v*DT
            while acc >= DX:
                acc -= DX; u = np.append(u, u0); w = np.append(w, v0); n += 1
                abu = banded(n, cu); abw = banded(n, cw)
        if i % every == 0: rec.append((i*DT, n*DX, count_peaks(u), np.interp(np.linspace(0, 1, 128), np.linspace(0, 1, n), u)))
    if not np.isfinite(u).all(): raise RuntimeError("non-finite")
    return u, rec

def spacing(u):
    c = u.mean(); thr = 0.25*(u.max() - u.min())
    pk = [i for i in range(1, len(u)-1) if u[i] > u[i-1] and u[i] >= u[i+1] and (u[i]-c) > thr]
    return (np.diff(pk)*DX).tolist()

def merge_parts():
    rows = []; keep = {}
    for d in DS:
        part = json.loads((OUT/f"edge-growth-part-d{d}.json").read_text()); rows += part["rows"]
        if d == 20: keep = {float(k): v for k, v in part["kymo"].items()}
    return rows, keep

if __name__ == "__main__":
    # usage: edge_growth_rd.py <d>   (one diffusion ratio per capped process)   |   edge_growth_rd.py merge
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] != "merge":
        d = int(sys.argv[1]); rows = []; keep = {}
        rw.A, rw.B = A, B; lam = 2*np.pi/rw.linear_kmax(d, GAM)[0]
        for v in SPEEDS:
            for s in SEEDS:
                u, rec = run(d, v, s); ns = np.array([r[2] for r in rec]); ev = [int(b - a) for a, b in zip(ns[:-1], ns[1:]) if b != a]
                sp = spacing(u)
                rows.append(dict(d=d, speed=v, T_grow=(W_END - W0)/v, seed=s, lambda_star=lam, n_final=int(count_peaks(u)),
                                 n_expected_final=float(W_END/lam), mean_spacing=float(np.mean(sp)) if sp else None,
                                 spacing_cv=float(np.std(sp)/np.mean(sp)) if len(sp) > 1 else None,
                                 events=ev, max_jump=int(max(ev)) if ev else 0, n_plus1=int(sum(e == 1 for e in ev)),
                                 n_vs_W=[[float(r[1]), int(r[2])] for r in rec[::4]]))
                if s == 1: keep[v] = [r[3].tolist() for r in rec]
            sub = rows[-len(SEEDS):]
            print(d, v, "n_final", [r["n_final"] for r in sub], "expected", round(W_END/lam, 1), "max_jump", [r["max_jump"] for r in sub],
                  "spacing", [round(r["mean_spacing"] or 0, 1) for r in sub], "lambda*", round(lam, 1), flush=True)
        part = OUT/f"edge-growth-part-d{d}.json"; part.write_text(json.dumps(dict(d=d, rows=rows, kymo={str(k): v for k, v in keep.items()})))
        write_receipt(OUT, f"claude-tissue-edge-growth-rd-d{d}", f"python3 simulations/claude_tissue/edge_growth_rd.py {d}", SEEDS, [], [part], t0)
        sys.exit(0)
    rows, keep = merge_parts()
    (OUT/"edge-growth.json").write_text(json.dumps(dict(model="Schnakenberg, apical (edge) growth", A=A, B=B, gamma=GAM, dx=DX, W0=W0, W_END=W_END, dt=DT,
                                                       relax=RELAX, speeds=SPEEDS, rows=rows), indent=1))
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.6))
    for v, c in zip(SPEEDS, ["tab:red", "tab:orange", "tab:blue"]):
        for d, ls in zip(DS, ["-", "--", ":"]):
            r = [x for x in rows if x["d"] == d and x["speed"] == v][0]; a = np.array(r["n_vs_W"])
            ax[0].plot(a[:, 0], a[:, 1], color=c, ls=ls, lw=1, label=f"v={v}, d={d}" if d == 20 or v == SPEEDS[0] else None)
    for d in DS:
        lam = [x for x in rows if x["d"] == d][0]["lambda_star"]; ww = np.linspace(W0, W_END, 50); ax[0].plot(ww, ww/lam, "k", lw=0.5, alpha=0.6)
    ax[0].set_xlabel("domain width W"); ax[0].set_ylabel("peak count"); ax[0].set_title("SIMULATED edge growth: peaks vs width (thin black: W/lambda*)"); ax[0].legend(fontsize=6)
    for k, v in enumerate([SPEEDS[0], SPEEDS[-1]]):
        img = np.array(keep[v]); ax[1 + k].imshow(img, aspect="auto", cmap="magma", origin="lower")
        ax[1 + k].set_title(f"u(x/W, t), d=20, seed 1, edge speed {v}"); ax[1 + k].set_xlabel("relative position (growing edge at right)"); ax[1 + k].set_ylabel("record index (time)")
    fig.tight_layout(); fig.savefig(OUT/"edge-growth.png", dpi=110)
    write_receipt(OUT, "claude-tissue-edge-growth-rd", "python3 simulations/claude_tissue/edge_growth_rd.py merge", SEEDS,
                  [f"artifacts/simulations/claude-tissue-growing-rd/edge-growth-part-d{d}.json" for d in DS], [OUT/"edge-growth.json", OUT/"edge-growth.png"], t0, extra=dict(parameters=dict(DS=DS, SPEEDS=SPEEDS, DX=DX, W0=W0, W_END=W_END)))
