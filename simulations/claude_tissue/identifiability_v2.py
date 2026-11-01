"""Sim C v2: identifiability of the Sim-B fin-growth model, corrected.
Review of v1 found (a) its rank-4 result was a time-step artifact: v1 integrated in time with fixed
dt, so changing body growth s changed the step count and broke the exact r/s symmetry at ~1e-3;
(b) its reduced fit sat on the lower bound of the gradient length l, so the reported SEs/bootstrap
were not valid intervals.  v2:
  * integrates dL/dSL = rho * F(L; p, l) in SL (exact reduction; t = (SL-SL0)/s only for time readouts)
  * computes the native 6-parameter Jacobian at two step sizes and uses a noise floor (max change
    between step sizes) as the rank threshold
  * profile likelihood in the reduced coordinates (log p, log l, log rho) on wide grids with the other
    two re-optimized; 95% interval from n*log(RSS/RSSmin) <= 3.84 (Gaussian iid residual assumption)
  * readout ladder: rank of the stacked Jacobian when (i) longitudinal L(t),SL(t), (ii) imaged gradient
    length, (iii) FRAP-type time-resolved gradient (sets D, k separately: needs the transient, so
    a quasi-steady model cannot use it: reported as structural, from the model equations), and
    (iv) calibrated absolute concentration + receptor dose-response (sets K) are added
  * sensitivity: same fit with initial fin length L0 free
Observed data: artifacts/observed-allometry/source-observations.csv, group 'flying fish' (49 rows).
SIMULATED model curves; the data constrain only what is reported here."""
import json, sys, time, pathlib, numpy as np
from scipy.optimize import least_squares
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
import claude_tissue.fin_growth as fg

OUT = ROOT / "artifacts/simulations/claude-tissue-identifiability"
NAMES = ["P", "D", "k", "K", "r", "s"]
SL0, L0_FIX, SL_END = fg.SL0, fg.L0, fg.SL_END
obs = fg.load_obs(); SLo = obs[:, 0]; yo = np.log10(obs[:, 1]); NOBS = len(yo)
DSL = 0.05

def F(L, p, l):
    x = np.linspace(0, L, 120); z = L/l
    lr = np.log(p) + np.logaddexp(x/l, -x/l) - z - np.log1p(-np.exp(-2*z) + 1e-300)
    m = np.exp(np.minimum(lr, 50)); return np.trapezoid(m/(1 + m), x)

def curve(p, l, rho, sl_grid, L0=L0_FIX):
    n = int(np.ceil((max(sl_grid.max(), SL_END) - SL0)/DSL)); S = SL0 + DSL*np.arange(n + 1)
    Ls = np.empty(n + 1); L = L0; Ls[0] = L
    for i in range(n):
        k1 = rho*F(L, p, l); k2 = rho*F(L + 0.5*DSL*k1, p, l); L += DSL*k2; Ls[i + 1] = L
    return np.interp(sl_grid, S, Ls)

def native_to_reduced(th):
    l = np.sqrt(th["D"]/th["k"]); return th["P"]*l/(th["D"]*th["K"]), l, th["r"]/th["s"]

def pred_native(lt, sl=SLo):
    th = dict(zip(NAMES, np.exp(lt))); return np.log10(np.maximum(curve(*native_to_reduced(th), sl), 1e-9))

def pred_red(q, sl=SLo, L0=L0_FIX):
    return np.log10(np.maximum(curve(*np.exp(q), sl, L0=L0), 1e-9))

LB, UB = np.array([-12.0, np.log(1e-4), -8.0]), np.array([25.0, np.log(50.0), 4.0])

def fit(y=yo, sl=SLo, x0s=None, fixed=None):
    """fixed: (index, value) of a reduced coord held fixed (profile)."""
    best = None
    x0s = x0s or [[np.log(400), np.log(0.05), np.log(2.5)], [np.log(5), np.log(1.0), np.log(0.5)],
                  [np.log(50), np.log(0.2), np.log(1.0)], [np.log(1e4), np.log(0.01), np.log(5.0)]]
    for x0 in x0s:
        x0 = np.clip(np.array(x0, float), LB + 1e-6, UB - 1e-6)
        if fixed is None:
            r = least_squares(lambda q: pred_red(q, sl) - y, x0, bounds=(LB, UB))
            q, cost = r.x, r.cost
        else:
            j, v = fixed; idx = [i for i in range(3) if i != j]
            def res(z):
                q = np.empty(3); q[j] = v; q[idx] = z; return pred_red(q, sl) - y
            r = least_squares(res, x0[idx], bounds=(LB[idx], UB[idx])); q = np.empty(3); q[j] = v; q[idx] = r.x; cost = r.cost
        if best is None or cost < best[1]: best = (q, cost)
    return best[0], 2*best[1]

def jac(fun, x, h):
    cols = []
    for j in range(len(x)):
        e = np.zeros(len(x)); e[j] = h; cols.append((fun(x + e) - fun(x - e))/(2*h))
    return np.array(cols).T

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    base = dict(fg.BASE); tg = float(np.mean(obs[obs[:, 0] > 15, 1]/obs[obs[:, 0] > 15, 0])); base["r"] = fg.anchor_r(base, tg)
    lt0 = np.log([base[n] for n in NAMES])
    # 1. native Jacobian, two step sizes, noise floor
    J1 = jac(pred_native, lt0, 0.02); J2 = jac(pred_native, lt0, 0.01)
    S1 = np.linalg.svd(J1, compute_uv=False); S2 = np.linalg.svd(J2, compute_uv=False)
    noise = float(np.max(np.abs(J1 - J2))) * np.sqrt(J1.size)   # Frobenius-scale bound on FD error
    U, S, Vt = np.linalg.svd(J1, full_matrices=False)
    rank = int((S > max(noise, 1e-8*S[0])).sum())
    null = [dict(zip(NAMES, Vt[i].round(3).tolist())) for i in range(rank, 6)]
    print("native SV", S, "noise", noise, "rank", rank, flush=True)
    # 2. best fit, fixed L0
    qh, rss = fit(); sig = float(np.sqrt(rss/(NOBS - 3)))
    print("fit", np.exp(qh), rss, flush=True)
    # 3. profiles in reduced coords
    grids = [np.linspace(np.log(1.0), np.log(1e8), 16), np.linspace(np.log(2e-4), np.log(20.0), 16), np.linspace(np.log(0.05), np.log(30.0), 16)]
    names_r = ["p (tip m/K)", "l = sqrt(D/k) [cm]", "rho = r/s [1/cm]"]
    prof = {}
    for j in range(3):
        rs = []
        for v in grids[j]:
            x0s = [qh.copy(), [np.log(50), np.log(0.2), np.log(1.0)]]
            _, r_ = fit(fixed=(j, v), x0s=x0s); rs.append(r_)
        rs = np.array(rs); dev = NOBS*np.log(rs/rss); inside = np.exp(grids[j][dev <= 3.84])
        lo_open = bool(dev[0] <= 3.84); hi_open = bool(dev[-1] <= 3.84)
        prof[names_r[j]] = dict(grid=np.exp(grids[j]).tolist(), rss=rs.tolist(), deviance=dev.tolist(),
                                ci95=[float(inside.min()), float(inside.max())] if len(inside) else None,
                                ci_open_low=lo_open, ci_open_high=hi_open)
        print(names_r[j], prof[names_r[j]]["ci95"], lo_open, hi_open, flush=True)
    # 4. compound combination in the tip-localized limit: c = rho*l*ln(1+p) (dL/dSL when L >> l)
    pc, lc, rc = np.exp(qh); c_hat = float(rc*lc*np.log1p(pc))
    # 5. readout ladder (local, structural via exact model symmetries + numeric where the model allows)
    def time_readouts(lt):
        th = dict(zip(NAMES, np.exp(lt))); p, l, rho = native_to_reduced(th); tg_ = np.linspace(5, (SL_END - SL0)/th["s"]*0.95, 8)
        sl_t = SL0 + th["s"]*tg_; return np.concatenate([np.log10(curve(p, l, rho, sl_t)), np.log10(sl_t)])
    def ell_readout(lt):
        th = dict(zip(NAMES, np.exp(lt))); return np.array([0.5*np.log10(th["D"]/th["k"])])
    def frap_readout(lt):   # recovery time of a bleached gradient ~ 1/k, and D from spreading: separates D and k
        th = dict(zip(NAMES, np.exp(lt))); return np.log10(np.array([th["D"], th["k"]]))
    def amp_readout(lt):    # calibrated absolute tip concentration P*l/D (needs K-independent quantification) + dose-response K
        th = dict(zip(NAMES, np.exp(lt))); l_ = np.sqrt(th["D"]/th["k"]); return np.log10(np.array([th["P"]*l_/th["D"], th["K"]]))
    blocks = [("cross-sectional L(SL) [current data]", [J1]),
              ("+ longitudinal L(t), SL(t) (time-stamped individuals)", [J1, jac(time_readouts, lt0, 0.02)]),
              ("+ imaged gradient length l", [J1, jac(time_readouts, lt0, 0.02), jac(ell_readout, lt0, 0.02)]),
              ("+ FRAP / photoconversion kinetics (D, k)", [J1, jac(time_readouts, lt0, 0.02), jac(ell_readout, lt0, 0.02), jac(frap_readout, lt0, 0.02)]),
              ("+ calibrated concentration and receptor dose-response (P, K)", [J1, jac(time_readouts, lt0, 0.02), jac(ell_readout, lt0, 0.02), jac(frap_readout, lt0, 0.02), jac(amp_readout, lt0, 0.02)])]
    ladder = []
    for name, bl in blocks:
        M = np.vstack(bl); s_ = np.linalg.svd(M, compute_uv=False); rk = int((s_ > max(noise, 1e-8*s_[0])).sum())
        ladder.append(dict(readouts=name, rank_of_6=rk, smallest_retained_sv=float(s_[rk - 1])))
    print(ladder, flush=True)
    # 6. sensitivity: L0 free
    def res4(q4): return pred_red(q4[:3], L0=np.exp(q4[3])) - yo
    r4 = least_squares(res4, np.r_[qh, np.log(L0_FIX)], bounds=(np.r_[LB, np.log(0.05)], np.r_[UB, np.log(2.0)]))
    rss4 = 2*r4.cost
    out = dict(version=2, n_obs=NOBS, data="artifacts/observed-allometry/source-observations.csv (group 'flying fish')",
               v1_defects_fixed=["rank-4 was a dt artifact (time-domain integration broke exact r/s symmetry); v2 integrates in SL",
                                  "v1 reduced fit sat on the l lower bound (e^-4 cm), so v1 SE/bootstrap are not valid intervals; v2 uses wide bounds and profile likelihood"],
               native_jacobian=dict(singular_values_h002=S1.tolist(), singular_values_h001=S2.tolist(), fd_noise_floor=noise, rank=rank,
                                    null_directions_log_theta=null),
               exact_reduction="L(SL) depends on (P,D,k,K,r,s) only through p=P*l/(D*K), l=sqrt(D/k), rho=r/s (quasi-steady gradient; SL linear in t)",
               best_fit=dict(p=float(pc), l_cm=float(lc), rho_per_cm=float(rc), rss=float(rss), residual_sigma_log10=sig, L0_fixed_cm=L0_FIX),
               profiles=prof,
               tip_limit_combination=dict(c=c_hat, formula="dL/dSL -> rho*l*ln(1+p) when L >> l", meaning="if l is small, the data fix this one number; p and l trade off along it"),
               readout_ladder=ladder,
               L0_free_sensitivity=dict(p=float(np.exp(r4.x[0])), l_cm=float(np.exp(r4.x[1])), rho=float(np.exp(r4.x[2])), L0_cm=float(np.exp(r4.x[3])),
                                        rss=float(rss4), delta_deviance=float(NOBS*np.log(rss/rss4))),
               caveats=["Cross-sectional specimens of 3 flying-fish species pooled as one trajectory (strong assumption).",
                        "Gaussian iid log residuals assumed for the chi-square profile threshold; residual mixes species, measurement and model error.",
                        "FRAP and dose-response rungs are structural (from the model equations), not simulated experiments."])
    (OUT/"identifiability-v2.json").write_text(json.dumps(out, indent=1))
    # figure
    fig, ax = plt.subplots(1, 4, figsize=(19, 4.4))
    ax[0].semilogy(range(1, 7), S1/S1[0], "o-", label="h=0.02"); ax[0].semilogy(range(1, 7), S2/S2[0], "x--", label="h=0.01")
    ax[0].axhline(noise/S1[0], color="r", ls="--", label="FD noise floor"); ax[0].set_xlabel("singular value index"); ax[0].set_ylabel("sigma_i/sigma_1")
    ax[0].set_title(f"native Jacobian: rank {rank} of 6"); ax[0].legend(fontsize=7)
    for j, n in enumerate(names_r):
        ax[1].plot(np.array(prof[n]["grid"])/np.exp(qh[j]), prof[n]["deviance"], "o-", ms=3, label=n)
    ax[1].axhline(3.84, color="gray", ls=":"); ax[1].set_xscale("log"); ax[1].set_ylim(-0.5, 30); ax[1].set_xlabel("value / best fit")
    ax[1].set_ylabel("profile deviance n log(RSS/RSSmin)"); ax[1].set_title("profiles (below dotted = inside 95%)"); ax[1].legend(fontsize=7)
    ax[2].barh([d["readouts"].split("(")[0][:38] for d in ladder], [d["rank_of_6"] for d in ladder], color="tab:green")
    ax[2].set_xlim(0, 6.3); ax[2].set_xlabel("identifiable directions (of 6)"); ax[2].set_title("readout ladder (local rank)"); ax[2].tick_params(axis="y", labelsize=7)
    sg = np.linspace(SL0, SL_END, 80)
    ax[3].scatter(SLo, 10**yo, s=14, c="k", label="observed flying fish (49)")
    ax[3].plot(sg, curve(*np.exp(qh), sg), "r", label="best-fit model (simulated)")
    ax[3].set_xlabel("SL (cm)"); ax[3].set_ylabel("pectoral fin length (cm)"); ax[3].legend(fontsize=7); ax[3].set_title("observed vs fitted curve")
    fig.suptitle("SIMULATED model, OBSERVED allometry data: which parameters the data pin down", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT/"identifiability-v2.png", dpi=110)
    outs = [OUT/"identifiability-v2.json", OUT/"identifiability-v2.png"]
    write_receipt(OUT, "claude-tissue-identifiability-v2", "python3 simulations/claude_tissue/identifiability_v2.py", "deterministic (no RNG)",
                  ["artifacts/observed-allometry/source-observations.csv"], outs, t0, extra=dict(baseline=base))
