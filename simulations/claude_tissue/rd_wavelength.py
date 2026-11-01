"""Sim A: Schnakenberg Turing wavelength sweep over diffusion ratio d and rate scale gamma.
Question: how does the selected pattern wavelength (in units of domain width) respond to
the parameters that control it, and how many 'rays' (stripe/spot rows) would a fin of fixed
width carry?  Output is in dimensionless units; the map to ray spacing is a stated assumption.
IMEX pseudo-spectral, periodic domain, numpy only."""
import json, sys, time, pathlib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

OUT = ROOT / "artifacts/simulations/claude-tissue-rd-wavelength"
A, B = 0.1, 0.9          # standard Schnakenberg kinetics (Murray); declared, not fitted to fish
N, LX = 64, 32.0          # grid points, domain side (nondim); dx=0.5
SEEDS = [11, 22, 33]
DS = [10, 14, 20, 30, 45]
GAMMAS = [0.5, 1.0, 2.0]
T_END, DT = 150.0, 0.02

def linear_kmax(d, g):
    u0 = A + B; v0 = B / u0**2
    J = g * np.array([[-1 + 2*u0*v0, u0**2], [-2*u0*v0, -u0**2]])
    ks = np.linspace(0.01, 6, 3000); best = (-1, 0)
    for k in ks:
        M = J - k*k*np.diag([1.0, d]); lam = np.linalg.eigvals(M).real.max()
        if lam > best[0]: best = (lam, k)
    return best[1] if best[0] > 0 else None, best[0]

def run(d, g, seed):
    rng = np.random.default_rng(seed)
    u0 = A + B; v0 = B / u0**2
    u = u0 + 0.01*rng.standard_normal((N, N)); v = v0 + 0.01*rng.standard_normal((N, N))
    k1 = 2*np.pi*np.fft.fftfreq(N, d=LX/N); KX, KY = np.meshgrid(k1, k1); K2 = KX**2 + KY**2
    Lu = 1/(1 + DT*K2); Lv = 1/(1 + DT*d*K2)
    for _ in range(int(T_END/DT)):
        fu = g*(A - u + u*u*v); fv = g*(B - u*u*v)
        u = np.real(np.fft.ifft2(Lu*np.fft.fft2(u + DT*fu)))
        v = np.real(np.fft.ifft2(Lv*np.fft.fft2(v + DT*fv)))
    return u

def dominant_k(u):
    F = np.abs(np.fft.fft2(u - u.mean()))**2
    k1 = 2*np.pi*np.fft.fftfreq(N, d=LX/N); KX, KY = np.meshgrid(k1, k1); K = np.hypot(KX, KY)
    bins = np.linspace(0, 6, 61); idx = np.digitize(K.ravel(), bins)
    p = np.array([F.ravel()[idx == i].sum() for i in range(1, len(bins))])
    kc = 0.5*(bins[1:] + bins[:-1]); amp = float(u.std())
    return float((kc*p).sum()/p.sum()) if p.sum() > 0 else 0.0, amp, float(kc[p.argmax()])

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    rows = []; snaps = {}
    for g in GAMMAS:
        for d in DS:
            kth, lam = linear_kmax(d, g)
            for s in SEEDS:
                u = run(d, g, s); kmean, amp, kpk = dominant_k(u)
                rows.append(dict(d=d, gamma=g, seed=s, k_theory=kth, lambda_growth=lam, k_peak=kpk,
                                 k_centroid=kmean, amplitude=amp, patterned=bool(amp > 0.05)))
                if s == SEEDS[0]: snaps[(d, g)] = u
            print(f"gamma={g} d={d} k_th={kth} k_obs={[r['k_peak'] for r in rows[-3:]]}", flush=True)
    # wavelength in nondim length, and number of 'rays' across a fixed fin width W_FIN = LX
    for r in rows:
        r["wavelength_obs"] = 2*np.pi/r["k_peak"] if r["k_peak"] > 0 else None
        r["wavelength_theory"] = 2*np.pi/r["k_theory"] if r["k_theory"] else None
        r["rays_across_domain"] = LX/r["wavelength_obs"] if r["wavelength_obs"] else None
    (OUT/"sweep.json").write_text(json.dumps(dict(model="Schnakenberg", a=A, b=B, grid=N, domain=LX, t_end=T_END, dt=DT, rows=rows), indent=1))
    # figure: wavelength vs d per gamma, observed vs theory + pattern gallery
    fig = plt.figure(figsize=(13, 7))
    ax = fig.add_subplot(2, 1, 1)
    for g in GAMMAS:
        rs = [r for r in rows if r["gamma"] == g and r["patterned"]]
        if not rs: continue
        ds_ = sorted({r["d"] for r in rs})
        m = [np.mean([r["wavelength_obs"] for r in rs if r["d"] == x]) for x in ds_]
        sd = [np.std([r["wavelength_obs"] for r in rs if r["d"] == x]) for x in ds_]
        ax.errorbar(ds_, m, sd, marker="o", label=f"simulated gamma={g}")
        th = [2*np.pi/linear_kmax(x, g)[0] for x in ds_ if linear_kmax(x, g)[0]]
        ax.plot(ds_[:len(th)], th, "--", color="gray", lw=1)
    ax.set_xlabel("diffusion ratio d"); ax.set_ylabel("wavelength (nondim; dashed = linear theory)")
    ax.set_title("SIMULATED Schnakenberg wavelength sweep (not observed; dimensionless; 3 seeds)")
    ax.legend()
    pick = [(10, 1.0), (20, 1.0), (45, 1.0), (20, 0.5), (20, 2.0)]
    for i, key in enumerate(pick):
        a2 = fig.add_subplot(2, 5, 6+i); a2.imshow(snaps[key], cmap="magma"); a2.axis("off"); a2.set_title(f"d={key[0]} gamma={key[1]}", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT/"wavelength-sweep.png", dpi=110)
    outs = [OUT/"sweep.json", OUT/"wavelength-sweep.png"]
    write_receipt(OUT, "claude-tissue-rd-wavelength", "python3 simulations/claude_tissue/rd_wavelength.py", SEEDS, [], outs, t0,
                  extra=dict(parameters=dict(a=A, b=B, N=N, L=LX, ds=DS, gammas=GAMMAS, t_end=T_END, dt=DT)))
