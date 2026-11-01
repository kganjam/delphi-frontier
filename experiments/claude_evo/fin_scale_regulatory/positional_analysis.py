"""Is the likelihood advantage earned across the window, or at one boundary?

The mean log-prob result (+0.1444 real vs own scramble) cannot distinguish two
very different situations:

  (a) real sequence is more predictable throughout the window, or
  (b) the advantage is concentrated at the start, where the model is still
      recovering from the prompt boundary, and the rest is flat.

(b) would mean the result is largely an artefact of where the annotation put the
window edge, which matters here because the two species' windows are anchored on
different features (TSS vs predicted start codon). This splits the window into
bins and reports the real-minus-shuffle advantage per bin, per species.

Usage: positional_analysis.py <positional_logprobs.json[.gz]> <out.json>
"""
from __future__ import annotations
import gzip, json, math, sys
import statistics as st
from scipy import stats

N_BINS = 10


def load(p):
    op = gzip.open if p.endswith(".gz") else open
    with op(p, "rt") as fh:
        return json.load(fh)


def ci(v):
    v = [float(x) for x in v]
    n = len(v)
    if n < 2:
        return {"n": n, "mean": round(st.mean(v), 4)}
    m, sd = st.mean(v), st.stdev(v)
    h = stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
    return {"n": n, "mean": round(m, 4), "lo": round(m - h, 4), "hi": round(m + h, 4)}


def main() -> int:
    curves = load(sys.argv[1])
    out_p = sys.argv[2]
    real = {c["target"]: c["logprobs"] for c in curves if c["kind"] == "real_held_out"}
    shuf = {c["target"]: c["logprobs"] for c in curves if c["kind"] == "dinucleotide_shuffle_of_real"}
    shared = sorted(set(real) & set(shuf))
    if not shared:
        sys.exit("no paired curves")
    L = min(min(len(real[t]) for t in shared), min(len(shuf[t]) for t in shared))
    edges = [round(i * L / N_BINS) for i in range(N_BINS + 1)]

    def binmeans(series):
        return [st.mean(series[edges[i]:edges[i + 1]]) for i in range(N_BINS)]

    rep = {"analysis": "positional log-prob advantage, real minus own dinucleotide shuffle",
           "question": "is the mean-level advantage earned across the window or "
                       "concentrated at the prompt boundary?",
           "n_windows": len(shared), "curve_length": L, "n_bins": N_BINS,
           "bin_edges_bp": edges}
    groups = {"all": shared,
              "zebrafish": [t for t in shared if t.startswith("dan:")],
              "flyingfish": [t for t in shared if t.startswith("hir:")]}
    for gname, ts in groups.items():
        if not ts:
            continue
        rb = {t: binmeans(real[t][:L]) for t in ts}
        sb = {t: binmeans(shuf[t][:L]) for t in ts}
        per_bin = []
        for i in range(N_BINS):
            d = [rb[t][i] - sb[t][i] for t in ts]
            row = ci(d)
            row["bin_bp"] = f"{edges[i]}-{edges[i + 1]}"
            row["excludes_zero"] = bool(row.get("lo") is not None and row["lo"] > 0)
            per_bin.append(row)
        rep[gname] = {"per_bin": per_bin,
                      "n_bins_excluding_zero": sum(1 for r in per_bin if r["excludes_zero"]),
                      "first_bin": per_bin[0], "last_bin": per_bin[-1]}
        # Is the advantage trending down across the window? Spearman on bin index.
        xs, ys = [], []
        for i, r in enumerate(per_bin):
            xs.append(i)
            ys.append(r["mean"])
        rho, p = stats.spearmanr(xs, ys)
        rep[gname]["trend_across_window"] = {
            "spearman_rho": round(float(rho), 4), "p": float(f"{p:.4g}"),
            "reading": "negative rho with small p would mean the advantage decays "
                       "across the window, i.e. boundary-driven"}
    json.dump(rep, open(out_p, "w"), indent=2)
    for g in ("all", "zebrafish", "flyingfish"):
        if g not in rep:
            continue
        print(f"\n{g}: bins excluding zero {rep[g]['n_bins_excluding_zero']}/{N_BINS}, "
              f"trend rho={rep[g]['trend_across_window']['spearman_rho']} "
              f"p={rep[g]['trend_across_window']['p']}")
        for r in rep[g]["per_bin"]:
            star = "*" if r["excludes_zero"] else " "
            print(f"  {r['bin_bp']:>10}  {r['mean']:+.4f}  [{r.get('lo')}, {r.get('hi')}] {star}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
