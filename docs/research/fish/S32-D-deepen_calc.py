"""S32-D-D: deepen S32-D by attacking the most sensitive input of ITS conclusion.

Run:  python3 docs/research/fish/S32-D-deepen_calc.py      (under 10 s, no data files)

S32-D's conclusion is a THRESHOLD: the taxi reaches glide speed only if the calibration burst speed
U_b >= 1.94 m/s (GENEROUS) / 2.36 m/s (CENTRAL). This script asks which input moves that threshold
most, then recomputes it with literature drag coefficients in place of S32's assumed body Cd.

The force model is imported unchanged from S32-deepen_calc.py (itself S32_taxi.py with inputs made
parameters; that file reproduces S32's 2.88 / 2.19 m/s). Everything printed is CALCULATED.
"""
import contextlib
import importlib.util
import io
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("s32d", os.path.join(HERE, "S32-deepen_calc.py"))
d = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(d)  # runs S32-D's own printout silently; we only need its functions
BASE, CENTRAL, ratio = d.BASE, d.CENTRAL, d.ratio


def hr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


def ub_flip(s):
    """Calibration burst speed U_b at which U_eq = V_to (S32-D's threshold)."""
    lo, hi = 0.1, 20.0
    for _ in range(70):
        m = 0.5 * (lo + hi)
        lo, hi = (lo, m) if ratio(dict(s, UB=m))[0] >= 1.0 else (m, hi)
    return hi


hr("0. Reproduce S32 / S32-D (expect U_eq 2.88 / 2.19 m/s; threshold 1.94 / 2.36 m/s)")
for name, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    r, ue, V, _ = ratio(s)
    print(f"{name:8s} U_eq {ue:.2f} m/s  V_to {V:.2f}  ratio {r:.2f}  U_b threshold {ub_flip(s):.2f} m/s")

hr("1. Which input moves S32-D's U_b threshold most? (each input x0.5 and x2, others fixed)")
KEYS = ["Cdb", "A_FRONT", "S_CAUDAL", "CD_F", "C_FIN", "m", "SW", "CLMAX", "phi", "CD0"]
print("Threshold falls below 1.57 m/s (Demesmay 2025 control MEAN C-start peak) => conclusion flips at a mean input.")
for name, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    print(f"-- {name}  (base threshold {ub_flip(s):.2f} m/s)")
    for k in KEYS:
        out = []
        for f in (0.5, 2.0):
            v = s[k] * f
            if k == "phi":
                v = min(v, 1.0)
            out.append(ub_flip(dict(s, **{k: v})))
        flag = "  <-- x2 or x0.5 pushes threshold below 1.57" if min(out) < 1.57 else ""
        print(f"   {k:9s} x0.5 -> {out[0]:.2f}   x2 -> {out[1]:.2f}   (spread x{max(out)/min(out):.2f}){flag}")

hr("2. Wetted-to-frontal area ratio of the design body (CALCULATED from an assumed shape)")
L = 0.030                    # m, standard length (S32 implicit: fin height 9 mm = 0.3 SL)
A_front = BASE["A_FRONT"]    # m^2, S28
def spheroid_area(a, b):
    e = math.sqrt(1 - (b / a) ** 2)
    return 2 * math.pi * b * b * (1 + a / (b * e) * math.asin(e))
b_eq = math.sqrt(A_front / math.pi)
S_sph = spheroid_area(L / 2, b_eq)
# elliptic section, depth:width 2:1, same area: perimeter / circle perimeter (Ramanujan)
ar = 2.0
bb, aa = math.sqrt(A_front / (math.pi * ar)), math.sqrt(A_front * ar / math.pi)
h = ((aa - bb) / (aa + bb)) ** 2
P_ell = math.pi * (aa + bb) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))
corr = P_ell / (2 * math.pi * b_eq)
for lab, S in (("prolate spheroid, circular section", S_sph), ("same, 2:1 elliptic section", S_sph * corr)):
    print(f"{lab:38s} S_wet {S*1e6:6.0f} mm^2   S_wet/A_front {S/A_front:5.1f}")
RATIO_LO, RATIO_MID, RATIO_HI = 15.0, S_sph * corr / A_front, 20.0
print(f"Band carried forward: {RATIO_LO:.0f} / {RATIO_MID:.1f} / {RATIO_HI:.0f}")

Re_b = 1.38 * L / 1.0e-6
hr(f"3. Body Cd on FRONTAL area (S32's basis) from each source; Re at 1.38 m/s = {Re_b:,.0f}")
CANDS = [
    # label, wetted-area Cd (low, mid, high)
    ("Laminar flat plate 1.328/sqrt(Re) (theory, calc)", (1.328 / math.sqrt(Re_b),) * 3),
    ("Turbulent flat plate 0.074 Re^-0.2 (theory, calc)", (0.074 * Re_b ** -0.2,) * 3),
    ("Tandler 2019 bluegill coasting 0.0154 +/- 0.0070 SD, Re 41k (abstract)", (0.0084, 0.0154, 0.0224)),
    ("McHenry & Lauder 2005 adult zebrafish coasting C_inert ~0.024 (abstract)", (0.024,) * 3),
    ("  same, IF C_inert omits the 1/2 (basis unverified) -> conventional 0.048", (0.048,) * 3),
]
rows = []
for lab, (lo, mid, hi) in CANDS:
    cl, cm, ch = lo * RATIO_LO, mid * RATIO_MID, hi * RATIO_HI
    rows.append((lab, cl, cm, ch))
    print(f"{lab:76s} Cd_front {cl:.2f} / {cm:.2f} / {ch:.2f}")
print("S32 assumed Cd_front: 0.1 (STINGY) / 0.2 (CENTRAL) / 0.3 (GENEROUS)")

hr("4. Undulation multiplier on rigid/coasting drag: sources DISAGREE (search-summary level)")
MULTS = [("none (coasting/rigid)", 1.0), ("Ehrenstein & Eloy 2013 ~+20%", 1.2),
         ("Patankar group <= +60%", 1.6), ("Lighthill 1971 x3 (theory, unconfirmed)", 3.0),
         ("Lighthill 1971 x5 (theory, unconfirmed)", 5.0)]
for lab, k in MULTS:
    print(f"  {lab:42s} x{k:.1f}")

hr("5. Recompute: U_eq/V_to and S32-D's U_b threshold with each improved body Cd")
print("Others at GENEROUS (Cdb replaces 0.3) and CENTRAL (replaces 0.2). U_b = 1.38 (S32) and 1.57 (Demesmay mean).")
def line(lab, cdb):
    g138 = ratio(dict(BASE, Cdb=cdb, UB=1.38))[0]
    g157 = ratio(dict(BASE, Cdb=cdb, UB=1.57))[0]
    c138 = ratio(dict(CENTRAL, Cdb=cdb, UB=1.38))[0]
    c157 = ratio(dict(CENTRAL, Cdb=cdb, UB=1.57))[0]
    tg, tc = ub_flip(dict(BASE, Cdb=cdb)), ub_flip(dict(CENTRAL, Cdb=cdb))
    print(f"{lab:56s} Cdb {cdb:5.2f} | GEN {g138:4.2f} {g157:4.2f} thr {tg:4.2f} | CEN {c138:4.2f} {c157:4.2f} thr {tc:4.2f}")
print(f"{'':56s} {'':10s} | GEN Ub=1.38 1.57  thr | CEN Ub=1.38 1.57  thr")
for lab, cl, cm, ch in rows:
    line(lab[:50] + " mid", cm)
line("Tandler low (mean - 1 SD, ratio 15)", rows[2][1])
line("Tandler high (mean + 1 SD, ratio 20)", rows[2][3])
line("McHenry 0.024, ratio 15", rows[3][1])
line("McHenry 0.024, ratio 20", rows[3][3])
for lab, k in MULTS[1:]:
    line(f"McHenry mid x {k:.1f} ({lab.split(' ')[0]})", rows[3][2] * k)
    line(f"Tandler mid x {k:.1f} ({lab.split(' ')[0]})", rows[2][2] * k)

hr("6. Body Cd (frontal) at which S32-D's verdict flips")
for name, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    for ub in (1.38, 1.57, 1.84):
        lo, hi = 0.01, 20.0
        for _ in range(70):
            m = math.sqrt(lo * hi)
            lo, hi = (lo, m) if ratio(dict(s, Cdb=m, UB=ub))[0] >= 1.0 else (m, hi)
        print(f"{name:8s} U_b {ub:.2f} m/s: flips if Cd_front >= {hi:.2f}  "
              f"(= wetted Cd {hi/RATIO_MID:.4f} at ratio {RATIO_MID:.1f})")

hr("7. Analytic check: U_max/U_b = sqrt(1 + Cdb*A/(S_fin*C_D)), C_D const, air drag ignored")
for cdb in (0.1, 0.2, 0.3, 0.42, 0.66):
    k = math.sqrt(1 + cdb * BASE["A_FRONT"] / (BASE["S_CAUDAL"] * BASE["CD_F"]))
    print(f"Cdb {cdb:.2f}: U_max/U_b = {k:.2f}")

hr("8. Does the improved body Cd rescue the REPEATED-STROKE (flume U_max) branch? U_b = 0.39 / 0.54 m/s")
for lab, cdb in (("McHenry mid", rows[3][2]), ("McHenry mid x1.6", rows[3][2] * 1.6),
                 ("McHenry if no 1/2", rows[4][2]), ("McHenry mid x5 (Lighthill)", rows[3][2] * 5)):
    out = []
    for ub in (0.39, 0.54):
        r, ue, V, p = ratio(dict(BASE, Cdb=cdb, UB=ub))
        net = d.forces(1.38, p)["net"] * 1e3
        out.append(f"U_b {ub:.2f}: U_eq/V_to {r:4.2f}, net@1.38 {net:+5.2f} mN")
    print(f"GENEROUS {lab:28s} Cdb {cdb:4.2f} | " + " | ".join(out))

hr("9. Undulation multiplier on McHenry's coasting Cd needed to flip at the Demesmay mean (U_b 1.57)")
for name, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    lo, hi = 0.5, 10.0
    for _ in range(70):
        m = 0.5 * (lo + hi)
        lo, hi = (lo, m) if ratio(dict(s, Cdb=rows[3][2] * m, UB=1.57))[0] >= 1.0 else (m, hi)
    print(f"{name}: x{hi:.2f} on Cd_front {rows[3][2]:.2f}")
