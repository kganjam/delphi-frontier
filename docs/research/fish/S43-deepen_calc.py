"""S43-D recomputation. Every output of this script is CALCULATED, not observed.

Usage:  python3 -I S43-deepen_calc.py [path/to/NIHMS1735542-supplement-2.xlsx]

If the Daane et al. 2021 Data S1 workbook is given, sheet "A - fin measurement" is read and
the per-species residual SD of log(pectoral length) on log(SL) is recomputed from the authors'
per-specimen values. Without it, the values recorded in S43-deepen.md section 3.2 are used.
"""
import math
import statistics as st
import sys
from collections import defaultdict

from scipy import stats

ALPHA = 0.05 / 3  # Bonferroni over 3 contrasts vs wild-type siblings (parent S43)


def n_per_group(d, power, alpha=ALPHA):
    """Smallest n per group for a two-sided two-sample t-test (exact noncentral t)."""
    for n in range(2, 100000):
        df = 2 * n - 2
        tc = stats.t.ppf(1 - alpha / 2, df)
        ncp = d * math.sqrt(n / 2)
        if (1 - stats.nct.cdf(tc, df, ncp)) + stats.nct.cdf(-tc, df, ncp) >= power:
            return n
    return None


def d_from(effect_frac, sd_log):
    return math.log(1 + effect_frac) / sd_log


def beloniform_resid_sd(path):
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(wb["A - fin measurement"].iter_rows(values_only=True))[1:]
    g = defaultdict(list)
    for r in rows:
        if r[1] and isinstance(r[4], (int, float)) and isinstance(r[5], (int, float)) and r[5] > 0:
            g[r[1]].append((math.log(r[4]), math.log(r[5])))
    out = {}
    for sp, v in g.items():
        if len(v) < 4:
            continue
        x, y = zip(*v)
        mx, my = st.mean(x), st.mean(y)
        sxx = sum((a - mx) ** 2 for a in x)
        b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
        res = [c - my - b * (a - mx) for a, c in zip(x, y)]
        out[sp] = (len(v), math.sqrt(sum(e * e for e in res) / (len(v) - 2)))
    return out


RECORDED = {  # species: (n, residual SD of log pectoral length | log SL) -- see S43-deepen.md 3.2
    "Exocoetus volitans": (19, 0.0979),
    "Hirundichthys rondeleti": (18, 0.0998),
    "Strongylura marina": (15, 0.1017),
    "Cheilopogon furcatus": (12, 0.0721),
    "Hyporhamphus unifasciatus": (12, 0.0470),
    "Hemiramphus brasiliensis": (10, 0.0754),
    "Oxyporhamphus micropterus": (10, 0.0707),
    "Euleptorhamphus velox": (9, 0.1077),
    "Belone belone": (4, 0.0877),
}


def cost(n_per_genotype):
    """Parent S43 section 3.6 cost structure, scaled to the genotyped total. CALCULATED."""
    genotyped = math.ceil(n_per_genotype * 200 / 30)  # parent: 200 genotyped for n=30/class
    growout_tanks = math.ceil(genotyped / 10)  # parent: 10 fish per 3.5 L
    nursery_tanks = math.ceil(6 * genotyped / 200)
    parental = 6 * 220
    adult_td = parental + growout_tanks * 160
    nursery_td = nursery_tanks * 30
    wustl = adult_td * 0.24 + nursery_td * 0.48
    bu = (adult_td + nursery_td) * 1.48
    geno = genotyped * 2 * 3.00
    consum = 200 + 250
    # labour: parent 208 h at n=30; genotyping/imaging/tracing (148 h) scale with fish, rest fixed
    hours = 60 + 148 * genotyped / 200
    lab = hours * 45
    return dict(genotyped=genotyped, growout_tanks=growout_tanks,
                low=wustl + geno + consum + lab, high=bu + geno + consum + lab, hours=hours)


def main():
    print("== Positive controls (must reproduce known values)")
    print("parent S43 cell CV=0.10, area effect 10.25%, power 0.90 -> 28 expected:",
          n_per_group(d_from(0.1025, 0.10), 0.90))
    print("challenge-310 cell CV_area=0.20, 10.25%, power 0.90 -> 105 expected:",
          n_per_group(d_from(0.1025, 0.20), 0.90))
    print("  (log-scale d = ln(1.1025)/SD gives 30 and 115; the parent and challenge-310 used the")
    print("   linear d = 0.1025/CV, which must give exactly 28 and 105:",
          n_per_group(0.1025 / 0.10, 0.90), n_per_group(0.1025 / 0.20, 0.90), ")")
    print("must-fail control: d=0 must not reach power 0.90 below n=100000 ->",
          n_per_group(1e-9, 0.90))

    print("\n== Step 1: sensitivity of the key number to residual CV (area effect 10.25%)")
    for sd in (0.05, 0.10, 0.20):
        n = n_per_group(d_from(0.1025, sd), 0.90)
        print(f"  SD(log area)={sd:.2f}  n/genotype={n:4d}  genotyped={math.ceil(n*200/30)}")

    print("\n== Step 1b: sensitivity to the effect size (SD(log area)=0.10)")
    for eff in (0.05, 0.1025, 0.21):
        print(f"  area effect={eff:.4f}  n/genotype={n_per_group(d_from(eff, 0.10), 0.90)}")

    data = RECORDED
    if len(sys.argv) > 1:
        data = beloniform_resid_sd(sys.argv[1])
        print("\n(read from workbook)")
    sds = sorted(v[1] for v in data.values())
    print("\n== Step 3: measured proxy, residual SD(log pectoral LENGTH | log SL), 9 beloniforms")
    for sp, (n, s) in sorted(data.items(), key=lambda kv: kv[1][1]):
        print(f"  {sp:28s} n={n:2d}  {s:.3f}")
    med = st.median(sds)
    print(f"  min={sds[0]:.3f} median={med:.3f} max={sds[-1]:.3f}")
    print(f"  species at or below the parent's implied 0.05: {sum(s <= 0.05 for s in sds)}/9")

    print("\n== Step 4: recompute. Isotropic size scatter => SD(log area) = 2 * SD(log length)")
    print("   and a 5% length effect => 10.25% area effect, so d is identical for length and area.")
    for label, sl in (("min", sds[0]), ("median", med), ("max", sds[-1]),
                      ("zebrafish wt regenerate, eye-read", 0.08)):
        sa = 2 * sl
        n = n_per_group(d_from(0.1025, sa), 0.90)
        n_len = n_per_group(d_from(0.05, sl), 0.90)
        c = cost(n)
        print(f"  {label:34s} SD(logL)={sl:.3f} SD(logA)={sa:.3f}  n_area={n:4d} n_length={n_len:4d}"
              f"  genotyped={c['genotyped']:5d} grow-out tanks={c['growout_tanks']:4d}"
              f"  cost ${c['low']:,.0f}-${c['high']:,.0f}  labour {c['hours']:.0f} h")

    print("\n== Interaction (non-additivity) contrast, variance 4 sigma^2/n: d halves")
    for label, sl in (("median", med),):
        print(f"  {label}: n/genotype={n_per_group(d_from(0.1025, 2*sl)/math.sqrt(2), 0.90)}")

    print("\n== What effect does n=30 detect at the median proxy? (power 0.90)")
    sa = 2 * med
    for eff in [x / 100 for x in range(5, 61)]:
        if n_per_group(d_from(eff, sa), 0.90) <= 30:
            print(f"  smallest area effect with n<=30: {eff:.0%} "
                  f"(= {math.sqrt(1+eff)-1:.1%} in length, isotropic)")
            break

    print("\n== Parent n=30 reproduced:", cost(30))


if __name__ == "__main__":
    main()
