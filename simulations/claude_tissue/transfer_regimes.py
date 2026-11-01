"""Transfer function between scales for the fin-growth model, conditioned on the observed allometry.
For gradient lengths l along a grid, re-fit (p, rho) to the 49 observed flying-fish rows, then
compute the organ-scale response (pectoral/SL at SL=24 cm) to a graded molecular perturbation of
morphogen production (P, i.e. p) and of gradient length (l).  Shows whether the data-compatible
regimes predict different dose-response slopes -> the experiment that discriminates them.
SIMULATED responses; observed data used only for the conditioning fit."""
import json, sys, time, pathlib, numpy as np
from scipy.optimize import least_squares
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
import claude_tissue.identifiability_v2 as iv

OUT = ROOT/"artifacts/simulations/claude-tissue-identifiability"
LS = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
DOSES = [0.25, 0.5, 1.0, 2.0, 4.0]
SL = np.array([24.0])

if __name__ == "__main__":
    t0 = time.time(); rows = []
    # initial fin length L0 (at SL0=1.5 cm) is FREE here: identifiability-v2 showed fixing it at 0.45 cm costs
    # 46 deviance units (observed fin/SL is already 0.54-0.76 at SL 1.7-3 cm)
    LO, HI = [iv.LB[0], iv.LB[2], np.log(0.05)], [iv.UB[0], iv.UB[2], np.log(2.0)]
    def fit_at(l):
        best = None
        for x0 in ([np.log(10.0), np.log(1.0), np.log(0.8)], [np.log(1e3), np.log(3.0), np.log(0.8)], [np.log(1.5), np.log(0.5), np.log(0.5)], [np.log(1e9), np.log(3.6), np.log(0.86)]):
            r = least_squares(lambda z: iv.pred_red(np.array([z[0], np.log(l), z[1]]), L0=np.exp(z[2])) - iv.yo, x0, bounds=(LO, HI))
            if best is None or r.cost < best.cost: best = r
        return best
    fits = {l: fit_at(l) for l in LS}
    rss_best = min(2*f.cost for f in fits.values())
    for l in LS:
        best = fits[l]
        p, rho, L0 = np.exp(best.x); rss = 2*best.cost
        base = iv.curve(p, l, rho, SL, L0=L0)[0]/24.0
        resp_p = [float(iv.curve(p*f, l, rho, SL, L0=L0)[0]/24.0/base) for f in DOSES]
        resp_l = [float(iv.curve(p, l*f, rho, SL, L0=L0)[0]/24.0/base) for f in DOSES]
        el_p = float(np.polyfit(np.log(DOSES), np.log(resp_p), 1)[0])
        rows.append(dict(l_cm=l, p=float(p), rho=float(rho), L0_cm=float(L0), rss=float(rss), delta_deviance=float(iv.NOBS*np.log(rss/rss_best)),
                         compatible_95=bool(iv.NOBS*np.log(rss/rss_best) <= 3.84), ratio_SL24=float(base),
                         response_to_production=dict(zip(map(str, DOSES), resp_p)), response_to_gradient_length=dict(zip(map(str, DOSES), resp_l)),
                         elasticity_ratio_wrt_production=el_p))
        print(rows[-1]["l_cm"], round(p, 3), round(rho, 3), round(rows[-1]["delta_deviance"], 2), round(el_p, 3), flush=True)
    out = dict(question="Given the observed allometry, how does fin/SL respond to graded morphogen production, and does the answer depend on the unidentified gradient length?",
               rss_best=float(rss_best), rss_best_note="minimum over the l grid with L0 free; grid-conditional", doses=DOSES, rows=rows,
               reading="Rows with compatible_95=true fit the 49 observations about equally; if their production elasticities differ, a dose series discriminates them where the allometry cannot.")
    p_json = OUT/"transfer-regimes.json"; p_json.write_text(json.dumps(out, indent=1))
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    cmap = plt.get_cmap("viridis")
    for i, r in enumerate(rows):
        ax[0].plot(DOSES, list(r["response_to_production"].values()), "o-", color=cmap(i/(len(rows)-1)),
                   ls="-" if r["compatible_95"] else ":", label=f"l={r['l_cm']:g} cm" + ("" if r["compatible_95"] else " (rejected)"))
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("morphogen production multiplier"); ax[0].set_ylabel("fin/SL at SL=24, relative")
    ax[0].set_title("SIMULATED dose-response, each regime re-fit to observed allometry"); ax[0].legend(fontsize=7)
    ax[1].semilogx([r["l_cm"] for r in rows], [r["elasticity_ratio_wrt_production"] for r in rows], "o-k", label="production elasticity")
    ax2 = ax[1].twinx(); ax2.semilogx([r["l_cm"] for r in rows], [r["delta_deviance"] for r in rows], "s--", color="tab:red"); ax2.axhline(3.84, color="tab:red", ls=":")
    ax2.set_ylabel("profile deviance vs best (red)", color="tab:red"); ax[1].set_xlabel("gradient length l (cm)"); ax[1].set_ylabel("d log(fin/SL) / d log(production)")
    ax[1].set_title("what the data allow vs what a dose series would show")
    fig.tight_layout(); p_png = OUT/"transfer-regimes.png"; fig.savefig(p_png, dpi=110)
    write_receipt(OUT, "claude-tissue-transfer-regimes", "python3 simulations/claude_tissue/transfer_regimes.py", "deterministic (no RNG)",
                  ["artifacts/observed-allometry/source-observations.csv"], [p_json, p_png], t0)
