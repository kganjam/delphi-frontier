"""S14-D-D: discriminability computed from Jiang et al. 2024 author-deposited data.

These are the authors' own per-individual numbers (PLoS Biol 10.1371/journal.pbio.3002565,
S1-S7 Data). Nothing here is digitized and nothing here is my observation: the inputs are
the authors' measurements, the Cohen's d values are my calculation on them.

Fetch the two inputs:
  curl -sSL "https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3002565.s002&type=supplementary" -o s002.xlsx
  curl -sSL "https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3002565.s005&type=supplementary" -o s005.xlsx
Run:
  python3 -I docs/research/fish/S14-D-D-authordata.py s002.xlsx s005.xlsx
Requires openpyxl.

PARSING HAZARD, recorded because it bit me first time round: sheet 'Fig. 2C' stacks the
ratio block (rows 4-25) on top of per-genotype RAW AREA blocks (rows 29+) in the same
columns. Reading a column to its end silently concatenates fin-bud/eye ratios (~0.2) with
raw pixel areas (~10^5) and returns a CV of 558%. The row bounds below are explicit for
that reason. Control: every mean printed for Fig 2C must lie in 0.1-0.5, and every CV
under 30%; if not, the block bounds have drifted.
"""
import sys, math, statistics as st
import openpyxl

s002, s005 = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("s002.xlsx", "s005.xlsx")

def desc(name, v):
    m, s = st.mean(v), st.stdev(v)
    print(f"  {name:28s} n={len(v):3d} mean={m:9.4f} SD={s:8.4f} CV={100*s/m:5.1f}%")
    return (m, s, len(v))

def cohen(a, b, label):
    sp = math.sqrt(((a[2]-1)*a[1]**2 + (b[2]-1)*b[1]**2)/(a[2]+b[2]-2))
    d = abs(b[0]-a[0])/sp
    print(f"  >> {label:42s} fold={b[0]/a[0]:5.2f}x  d={d:5.2f}  "
          f"setpoints: 1-SD {d:4.2f} | 2-SD {d/2:4.2f}")
    return d

print("Jiang et al. 2024, Fig 2C -- pectoral fin bud-to-eye AREA ratio (the output variable)")
ws = openpyxl.load_workbook(s002, data_only=True)["Fig. 2C"]
rows = [list(r) for r in ws.iter_rows(values_only=True)]
m = {}
for j, hdr in enumerate(rows[2]):
    if not isinstance(hdr, str):
        continue
    v = [rows[i][j] for i in range(3, 25)                      # ratio block ONLY
         if j < len(rows[i]) and isinstance(rows[i][j], (int, float))]
    if v:
        k = hdr.replace("\n", " ")
        m[k] = desc(k, v)
        assert 0.1 < m[k][0] < 0.5 and 100*m[k][1]/m[k][0] < 30, f"block bounds drifted on {k}"
print()
for t in ("32 hpf", "48 hpf", "56 hpf"):
    cohen(m[f"AB {t}"],  m[f"GFP {t}"],    f"AB vs GFP  NULL CONTROL @{t}")
    cohen(m[f"GFP {t}"], m[f"kcnk5b {t}"], f"GFP -> kcnk5b @{t}")
    cohen(m[f"GFP {t}"], m[f"kcnk10 {t}"], f"GFP -> kcnk10 @{t}")
    print()

wb = openpyxl.load_workbook(s005, data_only=True)
def sheet(name, marker, maxcol=8):
    ws = wb[name]; rows = [list(r) for r in ws.iter_rows(values_only=True)]
    hi = next(i for i, r in enumerate(rows)
              if any(isinstance(c, str) and marker in c for c in r))
    out = {}
    for j, hdr in enumerate(rows[hi][:maxcol]):
        if not isinstance(hdr, str):
            continue
        v = [r[j] for r in rows[hi+1:] if j < len(r) and isinstance(r[j], (int, float))]
        if v:
            out[hdr.replace("\n", " ").strip()] = v
    return out

print("Jiang et al. 2024, Fig 5K -- DiSBAC2(3) photon count/pixel per fin bud (Vm proxy)")
k = {n: desc(n, v) for n, v in sheet("Fig. 5K", "mCherry").items()}
ks = list(k); cohen(k[ks[0]], k[ks[1]], "mCherry -> kcnk5b-Tg")

print("\nJiang et al. 2024, Fig 5L -- same readout, separate experiment, +/- channel blockers")
l = {n: desc(n, v) for n, v in sheet("Fig. 5L", "mCherry").items()}
ls = list(l)
cohen(l[ls[0]], l[ls[2]], "mCherry -> kcnk5b (Et+DMSO)")
cohen(l[ls[2]], l[ls[3]], "kcnk5b: Et+DMSO -> Vin+Dib")

print("\nJiang et al. 2024, Fig 5Q -- fin-to-eye ratio, kcnk5b +/- channel blockers")
q = {n: desc(n, v) for n, v in sheet("Fig. 5Q", "Et+DMSO", 6).items()}
qs = list(q)
cohen(q[qs[0]], q[qs[1]], "AB: Et+DMSO -> Vin+Dib  DRUG-ONLY CONTROL")
cohen(q[qs[0]], q[qs[2]], "AB -> kcnk5b")
cohen(q[qs[2]], q[qs[3]], "kcnk5b: Et+DMSO -> Vin+Dib")
