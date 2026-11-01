"""Sim C: parameter identifiability / sensitivity of the Sim-B fin-growth model against the
REAL observed flying-fish pectoral/SL measurements (49 rows, Daane 2021 Data S1A, repo copy).
 1. Jacobian (log-theta -> log10 L at observed SL) of the 6 native parameters: SVD, null space.
 2. Exact-reduction check: model with (p, l, rho=r/s) reproduces the 6-parameter model.
 3. Fit the reduced model; bootstrap (resample rows) for the identifiable combinations.
 4. Profile likelihood of each native parameter (others free) shows flat directions.
 5. Local elasticities of the Sim-A Turing wavelength to d, gamma, a, b; there is NO observed
    wavelength to constrain them (stated, not simulated away).
SIMULATED model + observed data; the data constrain only the combinations reported."""
import json, sys, time, pathlib, numpy as np
from scipy.optimize import least_squares
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
import claude_tissue.fin_growth as fg
from claude_tissue.rd_wavelength import linear_kmax
import claude_tissue.rd_wavelength as rw

OUT = ROOT / "artifacts/simulations/claude-tissue-identifiability"
NAMES = ["P", "D", "k", "K", "r", "s"]
obs = fg.load_obs(); SLo = obs[:, 0]; yo = np.log10(obs[:, 1])

def pred_native(logth, sl=SLo):
    th = dict(zip(NAMES, np.exp(logth)))
    return np.log10(np.maximum(fg.log_curve(th, sl), 1e-6))

def pred_reduced(lq, sl=SLo):
    p, l, rho = np.exp(lq); th = dict(P=p*l, D=l*l, k=1.0, K=1.0, r=rho, s=1.0)
    return np.log10(np.maximum(fg.log_curve(th, sl), 1e-6))

def fit_reduced(y, sl, x0):
    f = lambda q: pred_reduced(q, sl) - y
    r = least_squares(f, x0, bounds=([-6, -4, -6], [6, 4, 3]), x_scale=1.0)
    return r

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    base = dict(fg.BASE); tg = float(np.mean(obs[obs[:, 0] > 15, 1]/obs[obs[:, 0] > 15, 0])); base["r"] = fg.anchor_r(base, tg)
    lt0 = np.log([base[n] for n in NAMES])
    # 2. exact reduction check
    l = np.sqrt(base["D"]/base["k"]); pcomp = base["P"]*l/(base["D"]*base["K"]); rho = base["r"]/base["s"]
    red_err = float(np.max(np.abs(pred_native(lt0) - pred_reduced(np.log([pcomp, l, rho])))))
    # 1. Jacobian at baseline (central differences in log theta)
    h = 0.02; J = np.zeros((len(SLo), 6))
    for j in range(6):
        e = np.zeros(6); e[j] = h; J[:, j] = (pred_native(lt0 + e) - pred_native(lt0 - e))/(2*h)
    U, S, Vt = np.linalg.svd(J, full_matrices=False)
    sv = S.tolist(); rank = int((S > 1e-6*S[0]).sum())
    null_vecs = [dict(zip(NAMES, Vt[i].round(3).tolist())) for i in range(rank, 6)]
    # 3. fit reduced (multi-start), residual sigma
    best = None
    for x0 in ([np.log(pcomp), np.log(l), np.log(rho)], [0.0, 0.0, -1.5], [np.log(3), np.log(2), -2.0], [-1.0, np.log(0.5), -1.0]):
        r = fit_reduced(yo, SLo, np.array(x0, float))
        if best is None or r.cost < best.cost: best = r
    rss = 2*best.cost; sigma = float(np.sqrt(rss/(len(yo)-3)))
    q_hat = best.x; Jr = best.jac; cov = np.linalg.pinv(Jr.T@Jr)*sigma**2
    se = np.sqrt(np.diag(cov))
    # bootstrap rows
    rng = np.random.default_rng(2026); boots = []
    for b in range(30):
        ix = rng.integers(0, len(yo), len(yo)); r = fit_reduced(yo[ix], SLo[ix], q_hat); boots.append(r.x)
    boots = np.array(boots)
    # 4. profile likelihood of native parameters, others free via reduced reparam: since only (p,l,rho) matter, the
    # profile of a native parameter v over a grid = min over (p,l,rho) subject to v-compatible native completion; any grid
    # value of P,D,K,k,s,r is attainable for the other natives -> profile is flat by construction. Verify numerically:
    prof = {}
    for j, n in enumerate(NAMES):
        vals = []
        for f in (0.25, 0.5, 1, 2, 4):
            th = np.array(lt0); th[j] += np.log(f)
            # re-optimize the 5 other natives starting at th
            idx = [i for i in range(6) if i != j]
            def res(z):
                t = th.copy(); t[idx] = z; return pred_native(t) - yo
            rr = least_squares(res, th[idx], max_nfev=25, x_scale=1.0)
            vals.append(float(2*rr.cost))
        prof[n] = dict(factors=[0.25, 0.5, 1, 2, 4], rss=vals)
        print(n, [round(v, 4) for v in vals], flush=True)
    # 5. wavelength elasticities (Sim A theory)
    def kth(d, g, a, b):
        rw.A, rw.B = a, b; return linear_kmax(d, g)[0]
    el = {}; p0 = dict(d=20.0, g=1.0, a=0.1, b=0.9); k0 = kth(**p0)
    for n in p0:
        q1 = dict(p0); q1[n] *= 1.05; q2 = dict(p0); q2[n] /= 1.05
        el[n] = float(-(np.log(kth(**q1)) - np.log(kth(**q2)))/(np.log(1.05)*2))   # d log lambda / d log param
    rw.A, rw.B = 0.1, 0.9
    # 6. design question: which ADDED readouts raise the Jacobian rank?  (rank counts at 1e-6 relative cutoff; local, at baseline)
    def Jrank(fun, n_out):
        Jx = np.zeros((n_out, 6))
        for j in range(6):
            e = np.zeros(6); e[j] = h; Jx[:, j] = (fun(lt0 + e) - fun(lt0 - e))/(2*h)
        return Jx
    def time_readouts(lt):
        th = dict(zip(NAMES, np.exp(lt))); ts, SL, Ls = fg.simulate(th); idx = np.linspace(0, len(ts)-1, 8).astype(int)
        return np.concatenate([np.log10(Ls[idx]), np.log10(SL[idx])])         # longitudinal (t known): L(t), SL(t)
    def ell_readout(lt):
        th = dict(zip(NAMES, np.exp(lt))); return np.array([0.5*np.log10(th["D"]/th["k"])])    # imaged gradient length l
    def amp_readout(lt):
        th = dict(zip(NAMES, np.exp(lt))); l_ = np.sqrt(th["D"]/th["k"]); return np.array([np.log10(th["P"]*l_/(th["D"]*th["K"]))])  # tip m/K in units of K (needs calibrated reporter)
    blocks = {"cross-sectional L(SL) only": J, "+ longitudinal L(t),SL(t)": np.vstack([J, Jrank(time_readouts, 16)]),
              "+ longitudinal + gradient length": np.vstack([J, Jrank(time_readouts, 16), Jrank(ell_readout, 1)]),
              "+ longitudinal + gradient length + calibrated amplitude": np.vstack([J, Jrank(time_readouts, 16), Jrank(ell_readout, 1), Jrank(amp_readout, 1)])}
    design_rank = {k: int((np.linalg.svd(v, compute_uv=False) > 1e-6*np.linalg.svd(v, compute_uv=False)[0]).sum()) for k, v in blocks.items()}
    print(design_rank, flush=True)
    out = dict(n_obs=int(len(yo)), data="artifacts/observed-allometry/source-observations.csv, group=flying fish",
               jacobian_singular_values=sv, rank_6_native=rank, null_space_directions_in_log_theta=null_vecs,
               reduction_max_abs_log10_error=red_err,
               reduced_fit=dict(names=["p=P*l/(D*K)", "l=sqrt(D/k) cm", "rho=r/s"], estimate=np.exp(q_hat).tolist(), se_log=se.tolist(),
                                bootstrap_log_sd=boots.std(0).tolist(), bootstrap_n=30, bootstrap_q05=np.exp(np.percentile(boots, 5, 0)).tolist(),
                                bootstrap_q95=np.exp(np.percentile(boots, 95, 0)).tolist(), residual_sigma_log10=sigma, rss=float(rss)),
               profile_rss=prof, rank_by_added_readout=design_rank, wavelength_elasticity_dlogLambda_dlogParam=el,
               wavelength_note="No observed Turing wavelength or ray spacing is in the repo; these parameters have zero data constraint.",
               caveat="Cross-sectional pooled specimens of 3 species are treated as one growth trajectory (strong assumption); residual sigma mixes measurement error, species differences and model misspecification.")
    (OUT/"identifiability.json").write_text(json.dumps(out, indent=1))
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    ax[0].semilogy(range(1, 7), S/S[0], "o-"); ax[0].axhline(1e-6, color="r", ls="--"); ax[0].set_xlabel("singular value index"); ax[0].set_ylabel("sigma_i/sigma_1")
    ax[0].set_title(f"Jacobian spectrum, 6 native params, rank={rank} (simulated model, observed SL)")
    for n in NAMES: ax[1].plot(prof[n]["factors"], np.array(prof[n]["rss"])/prof["P"]["rss"][2], "o-", label=n)
    ax[1].set_xscale("log"); ax[1].set_xlabel("fixed parameter factor"); ax[1].set_ylabel("profile RSS / best"); ax[1].legend(fontsize=7); ax[1].set_title("profile RSS (flat = not pinned)")
    ax[2].scatter(SLo, 10**yo, s=14, c="k", label="observed flying fish (49)"); sg = np.linspace(2, 24, 50)
    ax[2].plot(sg, 10**pred_reduced(q_hat, sg), "r", label="reduced-model fit (simulated curve)"); ax[2].set_xlabel("SL (cm)"); ax[2].set_ylabel("pectoral (cm)"); ax[2].legend(fontsize=7); ax[2].set_title("observed points vs fitted model curve")
    fig.tight_layout(); fig.savefig(OUT/"identifiability.png", dpi=110)
    outs = [OUT/"identifiability.json", OUT/"identifiability.png"]
    write_receipt(OUT, "claude-tissue-identifiability", "python3 simulations/claude_tissue/identifiability.py", "bootstrap rng seed 2026",
                  ["artifacts/observed-allometry/source-observations.csv"], outs, t0, extra=dict(baseline=base))
