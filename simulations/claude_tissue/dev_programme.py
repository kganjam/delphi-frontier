"""Developmental-programme model linking ADULT fin proportions to a growth programme (studio developmental scale).

Model (derived from the fin-growth gradient model, Sim B):
  dL/dSL = (r/s) * integral_0^L h(m(x)) dx,   m(x) = quasi-steady distal-source gradient, h = m/(K+m)
In the tip-saturated limit that the observed flying-fish allometry favours (identifiability-v2: l -> 0.009 cm,
p -> large), the integral tends to l*ln(1+p), so the programme becomes two-phase:
  phase 1 (before the observed size range, unobserved); a is the EXTRAPOLATED intercept of phase 2, not a measured
  early fin length (a < 0 for flying fish means the linear phase cannot extend below the observed range)
  phase 2 (observed range): constant growth-zone output  dL/dSL = c,  c = (r/s) * sqrt(D/k) * ln(1+p)
  =>  L(SL) = a + c*SL,     adult ratio  R(SL) = L/SL = c + a/SL  ->  c  as SL -> infinity
This script fits (a, c) per group to OBSERVED specimens (artifacts/observed-allometry/source-observations.csv:
flying fish, flying halfbeak, halfbeak, needlefish), compares with a power law L = b*SL^alpha (AIC),
bootstraps CIs, and decomposes the flying-fish vs halfbeak difference in fin/SL at a reference size into an
early-phase (a) part and a growth-zone (c) part.  Fitted model curves are computed; specimens are observed.
It does NOT identify a morphogen, a gradient, r, s, D, k, P or K separately (only the composite c), and
cross-sectional pooled-species data are not growth trajectories."""
import json, sys, time, csv, pathlib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

OUT = ROOT/"artifacts/simulations/claude-tissue-dev-programme"
DATA = "artifacts/observed-allometry/source-observations.csv"
GROUPS = ["flying fish", "flying halfbeak", "halfbeak", "needlefish"]
NBOOT = 2000; SEED = 20261101; SL_REF = 20.0

def load():
    rows = list(csv.DictReader(open(ROOT/DATA)))
    return {g: np.array([[float(r["sl_cm"]), float(r["pectoral_cm"])] for r in rows if r["group"] == g and r["pectoral_cm"]]) for g in GROUPS}

def fit_lin(x, y):     # L = a + c SL, least squares in log space would bias a; use ordinary LS on L with log-residual check
    A = np.c_[np.ones_like(x), x]; coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A@coef
    return coef, res

def fit_pow(x, y):
    """L = b*SL^alpha fitted by nonlinear least squares on the SAME raw-length scale as the linear model
    (argon review: a log-space fit makes the AIC comparison invalid); log-space fit used only as a start."""
    from scipy.optimize import least_squares
    A = np.c_[np.ones_like(x), np.log(x)]; coef, *_ = np.linalg.lstsq(A, np.log(y), rcond=None)
    r = least_squares(lambda q: q[0]*x**q[1] - y, [np.exp(coef[0]), coef[1]])
    return r.x, y - r.x[0]*x**r.x[1]

def aic(res, k):
    n = len(res); return float(n*np.log((res**2).sum()/n) + 2*k)

if __name__ == "__main__":
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True); D = load(); rng = np.random.default_rng(SEED); out = {}
    boots = {}
    for g in GROUPS:
        x, y = D[g][:, 0], D[g][:, 1]
        (a, c), rl = fit_lin(x, y); (b, al), rp = fit_pow(x, y)
        bs = []
        for _ in range(NBOOT):
            i = rng.integers(0, len(x), len(x))
            if len(np.unique(x[i])) < 3: continue
            bs.append(fit_lin(x[i], y[i])[0])
        bs = np.array(bs); boots[g] = bs
        q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        out[g] = dict(n=int(len(x)), sl_range_cm=[float(x.min()), float(x.max())],
                      programme_fit=dict(a_cm=float(a), c=float(c), a_ci95=q(bs[:, 0]), c_ci95=q(bs[:, 1]),
                                         ratio_at_SLref=float(c + a/SL_REF), ratio_at_SLref_ci95=q(bs[:, 1] + bs[:, 0]/SL_REF),
                                         rmse_cm=float(np.sqrt((rl**2).mean())), aic=aic(rl, 2)),
                      power_law_fit=dict(b=float(b), alpha=float(al), rmse_cm=float(np.sqrt((rp**2).mean())), aic=aic(rp, 2)),
                      observed_mean_ratio=float(np.mean(y/x)))
        print(g, out[g]["programme_fit"], "alpha", round(al, 3), flush=True)
    # decomposition: flying fish vs each relative at SL_REF;  dR = dc + da/SL_REF
    dec = {}
    for other in GROUPS[1:]:
        ff, ot = out["flying fish"]["programme_fit"], out[other]["programme_fit"]
        dR = ff["ratio_at_SLref"] - ot["ratio_at_SLref"]; dc = ff["c"] - ot["c"]; da = (ff["a_cm"] - ot["a_cm"])/SL_REF
        n = min(len(boots["flying fish"]), len(boots[other]))
        bdc = boots["flying fish"][:n, 1] - boots[other][:n, 1]; bda = (boots["flying fish"][:n, 0] - boots[other][:n, 0])/SL_REF
        dec[f"flying fish - {other}"] = dict(delta_ratio_at_SLref=float(dR), from_growth_zone_c=float(dc), from_early_offset_a=float(da),
                                             c_share=float(dc/dR) if dR else None,
                                             delta_c_ci95=[float(np.percentile(bdc, 2.5)), float(np.percentile(bdc, 97.5))],
                                             delta_a_term_ci95=[float(np.percentile(bda, 2.5)), float(np.percentile(bda, 97.5))])
        print(other, dec[f"flying fish - {other}"], flush=True)
    summ = dict(model="two-phase distal growth-zone programme (tip-saturated limit of the fin-growth gradient model)",
                equations={"growth law": "dL/dSL = (r/s) * int_0^L m/(K+m) dx", "tip-saturated limit": "dL/dSL -> c = (r/s) sqrt(D/k) ln(1+p)",
                           "observed-phase solution": "L = a + c SL", "adult proportion": "L/SL = c + a/SL -> c"},
                data=DATA, sl_ref_cm=SL_REF, bootstrap=dict(n=NBOOT, seed=SEED, resample="specimens within group"),
                groups=out, decomposition=dec,
                does_not_establish=["which molecule (if any) forms the gradient; the model's morphogen is hypothetical",
                                    "r, s, D, k, P or K individually; only the composite c and the offset a are fitted",
                                    "growth trajectories: specimens are cross-sectional and species are pooled within groups",
                                    "anything about the early (phase-1) outgrowth: the smallest specimen is 1.68 cm SL, where flying-fish fin/SL is already about 0.54, so an early larval head start is neither shown nor excluded",
                                    "independent replication: species are pooled within groups without phylogenetic correction, so bootstrap CIs are anticonservative",
                                    "that flying-fish fins are an evolutionary consequence of a change in c or a",
                                    "aerodynamic or behavioural consequences of the proportions"])
    (OUT/"programme.json").write_text(json.dumps(summ, indent=1))
    # figure
    cols = {"flying fish": "tab:blue", "flying halfbeak": "tab:purple", "halfbeak": "tab:orange", "needlefish": "tab:gray"}
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
    for g in GROUPS:
        x, y = D[g][:, 0], D[g][:, 1]; p = out[g]["programme_fit"]; sg = np.linspace(max(1.0, x.min()*0.8), x.max()*1.05, 80)
        ax[0].scatter(x, y, s=12, color=cols[g], label=f"{g} (observed, n={len(x)})"); ax[0].plot(sg, p["a_cm"] + p["c"]*sg, color=cols[g], lw=1.2)
        ax[1].scatter(x, y/x, s=12, color=cols[g]); ax[1].plot(sg, p["c"] + p["a_cm"]/sg, color=cols[g], lw=1.2); ax[1].axhline(p["c"], color=cols[g], ls=":", lw=0.8)
    ax[0].set_xlabel("standard length SL (cm)"); ax[0].set_ylabel("pectoral fin length L (cm)"); ax[0].legend(fontsize=7); ax[0].set_title("observed specimens; lines = fitted L = a + c*SL")
    ax[1].set_xlabel("SL (cm)"); ax[1].set_ylabel("fin / SL"); ax[1].set_xscale("log"); ax[1].set_title("adult proportion R = c + a/SL (dotted: c)")
    names = list(GROUPS); cs = [out[g]["programme_fit"]["c"] for g in names]; ce = np.array([out[g]["programme_fit"]["c_ci95"] for g in names])
    as_ = [out[g]["programme_fit"]["a_cm"] for g in names]; ae = np.array([out[g]["programme_fit"]["a_ci95"] for g in names])
    xx = np.arange(len(names))
    ax[2].errorbar(xx - 0.1, cs, [np.array(cs) - ce[:, 0], ce[:, 1] - np.array(cs)], fmt="o", label="c (growth-zone output, dL/dSL)")
    ax2 = ax[2].twinx(); ax2.errorbar(xx + 0.1, as_, [np.array(as_) - ae[:, 0], ae[:, 1] - np.array(as_)], fmt="s", color="tab:red", label="a (early offset, cm)")
    ax[2].set_xticks(xx); ax[2].set_xticklabels(names, rotation=15, fontsize=8); ax[2].set_ylabel("c"); ax2.set_ylabel("a (cm)", color="tab:red")
    ax[2].set_title("programme parameters, bootstrap 95% CI"); ax[2].legend(loc="upper right", fontsize=7); ax2.legend(loc="center right", fontsize=7)
    fig.suptitle("Developmental programme fitted to OBSERVED allometry (model curves computed; not a growth trajectory)", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT/"programme.png", dpi=110); plt.close(fig)
    write_receipt(OUT, "claude-tissue-dev-programme", "python3 simulations/claude_tissue/dev_programme.py", SEED, [DATA],
                  [OUT/"programme.json", OUT/"programme.png"], t0)
