"""S32-D: deepen S32 (multi-stroke taxi launch) by attacking its most sensitive input.

Run:  python3 docs/research/fish/S32-deepen_calc.py      (about 10 s, no data files)

The force model is S32's, copied verbatim in physics from docs/research/fish/S32_taxi.py on branch
origin/claude/s32-multi-stroke-launch-qpq9g2 (commit c1b761eb). The only structural change: every input that
S32 hard-codes is now a parameter, so each can be multiplied by 0.5 and 2 and the conclusion recomputed.

Everything printed here is CALCULATED. Nothing is a measurement.
"""
import math

RHO_W, RHO_A, NU_W, G0, SIGMA = 1000.0, 1.225, 1.0e-6, 9.81, 0.072
RE_LO, RE_HI = 4780.0, 9560.0          # Floryan et al. 2017 measured Re span

# S32 base inputs (names as in S32_taxi.py)
BASE = dict(
    UB=1.38,          # m/s  calibration burst speed (Miln 2021 fastest single fish, 120 fps, digitised)
    Cdb=0.3,          # body drag coefficient in water, used ONLY in the thrust calibration (assumed, S29)
    A_FRONT=24e-6,    # m^2  frontal area (S28)
    S_CAUDAL=0.7 * 6e-3 * 9e-3,   # m^2 caudal fin area (ASSUMED: chord 6 mm x height 9 mm x 0.7)
    CD_F=0.08,        # Floryan residual drag coefficient C_D
    C_FIN=6e-3,       # m  lobe chord (sets Re and thus C_D scaling)
    m=0.25e-3,        # kg body mass
    SW=192e-6,        # m^2 wing area (S28 case C)
    CLMAX=1.07,       # wing CL_max (S28)
    phi=1.0,          # immersed fraction of lower lobe
    CD0=0.08, costh=0.0, dcos=0.0, cdmode="scaled", H_FIN=9e-3, Cd_air=0.3,
)
CENTRAL = dict(BASE, Cdb=0.2, phi=0.5, CD0=0.12, costh=0.5, dcos=0.1)


def cd_lobe(U, c, mode, cd0):
    if mode == "const":
        return cd0
    Re = max(U, 1e-6) * c / NU_W
    if Re < RE_LO:
        return cd0 * math.sqrt(RE_LO / Re)
    if Re > RE_HI:
        return cd0 * math.sqrt(RE_HI / Re)
    return cd0


def build(s):
    G = (s["Cdb"] * s["A_FRONT"] / s["S_CAUDAL"] + cd_lobe(s["UB"], s["C_FIN"], s["cdmode"], s["CD_F"])) * s["UB"] ** 2
    S_lobe = s["S_CAUDAL"] / 2
    Vto = math.sqrt(2 * s["m"] * G0 / (RHO_A * s["SW"] * s["CLMAX"]))
    return dict(s, G=G, S_imm=s["phi"] * S_lobe, d=s["phi"] * s["H_FIN"] / 2, k=1 / (math.pi * 0.8 * 5.0), Vto=Vto)


def forces(U, p):
    W = p["m"] * G0
    q_a, q_w = 0.5 * RHO_A * U * U, 0.5 * RHO_W * U * U
    CL = min(p["CLMAX"], W / (q_a * p["SW"])) if U > 0 else 0.0
    L_w = q_a * p["SW"] * CL
    D_w = q_a * p["SW"] * (p["CD0"] + p["k"] * CL * CL)
    D_b = q_a * p["Cd_air"] * p["A_FRONT"]
    Fsv = 2 * SIGMA * p["C_FIN"] * p["costh"]
    Fsh = 2 * SIGMA * p["C_FIN"] * p["dcos"]
    CLz = max(0.0, W + Fsv - L_w) / (q_w * p["S_imm"])
    AR = 2 * p["d"] ** 2 / p["S_imm"]
    D_i = q_w * p["S_imm"] * CLz * CLz / (math.pi * 0.8 * AR)
    T = 0.5 * RHO_W * p["S_imm"] * (p["G"] - cd_lobe(U, p["C_FIN"], p["cdmode"], p["CD_F"]) * U * U)
    return dict(T=T, net=T - D_w - D_b - D_i - Fsh, CLz=CLz)


def u_eq(p, lo=0.05, hi=60.0):
    if forces(hi, p)["net"] > 0:
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if forces(mid, p)["net"] > 0 else (lo, mid)
    return lo


def u_support(p):
    lo, hi = 0.01, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if forces(mid, p)["CLz"] > 1.0 else (lo, mid)
    return hi


def ratio(s):
    p = build(s)
    return u_eq(p) / p["Vto"], u_eq(p), p["Vto"], p


def hr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


hr("0. Reproduce S32 (must print 2.88 / 4.41 GENEROUS and 2.19 CENTRAL)")
for name, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    r, ue, V, p = ratio(s)
    print(f"{name:8s} U_eq {ue:.2f} m/s  V_to {V:.2f}  U_eq/V_to {r:.2f}  G {p['G']:.3f} m2/s2")

hr("1. Factor-of-two sensitivity: every input x0.5 and x2, U_eq/V_to (>= 1.00 means the conclusion FALLS)")
KEYS = ["UB", "Cdb", "A_FRONT", "S_CAUDAL", "CD_F", "C_FIN", "m", "SW", "CLMAX", "phi", "CD0"]
print(f"{'input':9s} | {'GENEROUS x0.5':>13s} {'x1':>6s} {'x2':>6s} | {'CENTRAL x0.5':>12s} {'x1':>6s} {'x2':>6s}")
for k in KEYS:
    row = []
    for s in (BASE, CENTRAL):
        for f in (0.5, 1.0, 2.0):
            v = s[k] * f
            if k == "phi":
                v = min(v, 1.0)
            row.append(ratio(dict(s, **{k: v}))[0])
    flag = "  <-- FLIPS" if max(row) >= 1.0 else ""
    print(f"{k:9s} | {row[0]:13.2f} {row[1]:6.2f} {row[2]:6.2f} | {row[3]:12.2f} {row[4]:6.2f} {row[5]:6.2f}{flag}")
print("(CLMAX x2 = 2.14 is outside any measured fish-fin/wing value; listed for completeness. phi capped at 1.)")

hr("2. Flip factor: multiplier on ONE input (others at GENEROUS / CENTRAL) needed to make U_eq = V_to")
def flip(s, k, up=True):
    lo, hi = 1.0, 64.0
    if not up:
        lo, hi = 1 / 64.0, 1.0
    f_ok = (lambda f: ratio(dict(s, **{k: s[k] * f}))[0] >= 1.0)
    if not f_ok(hi if up else lo):
        return None
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if up:
            lo, hi = (lo, mid) if f_ok(mid) else (mid, hi)
        else:
            lo, hi = (mid, hi) if f_ok(mid) else (lo, mid)
    return hi if up else lo
for k, up in (("UB", True), ("Cdb", True), ("A_FRONT", True), ("S_CAUDAL", False), ("CD_F", False),
              ("SW", True), ("CLMAX", True), ("m", False)):
    out = []
    for s in (BASE, CENTRAL):
        f = flip(s, k, up)
        out.append("never (within 64x)" if f is None else f"x{f:.2f} -> {s[k]*f:.4g}")
    print(f"{k:9s} {'raise' if up else 'lower'}:  GENEROUS {out[0]:28s} CENTRAL {out[1]}")

hr("3. The calibration speed U_b, recomputed with every measured candidate (others GENEROUS / CENTRAL)")
CANDS = [
    ("Widrick 2018 Tbl 2 flume U_max, low  (13.0 SL/s x 30 mm)", 13.0 * 0.030),
    ("Widrick 2018 Tbl 2 flume U_max, high (17.9 SL/s x 30 mm)", 17.9 * 0.030),
    ("Miln 2021 fast-start, visual centre (my read of Fig 1a)", 0.80),
    ("Demesmay 2025 mean speed over first 40 ms (3.8 cm/40 ms)", 0.95),
    ("Miln 2021 fastest single fish (S32's input)", 1.38),
    ("Demesmay 2025 control mean max speed", 1.57),
    ("Demesmay 2025 control mean + 1 SD", 1.57 + 0.27),
    ("Demesmay 2025 control mean + 2 SD", 1.57 + 2 * 0.27),
]
print("U_eq printed as 'none' when net force is negative at every speed above 0.05 m/s (support drag wins).")
print("net@1.38 = net horizontal force at S32's 1.38 m/s exit speed, mN (negative = decelerates from the first stroke)")
def fmt(u):
    return " none" if u <= 0.0501 else f"{u:5.2f}"
for lab, ub in CANDS:
    rg, ug, Vg, pg = ratio(dict(BASE, UB=ub))
    rc, uc, Vc, pc = ratio(dict(CENTRAL, UB=ub))
    print(f"{lab:60s} U_b {ub:4.2f} | GEN U_eq {fmt(ug)} ({rg*100:3.0f}% V_to) net@1.38 {forces(1.38, pg)['net']*1e3:+6.2f}"
          f" | CEN U_eq {fmt(uc)} ({rc*100:3.0f}%) net@1.38 {forces(1.38, pc)['net']*1e3:+6.2f}")
for lab, s in (("GENEROUS", BASE), ("CENTRAL", CENTRAL)):
    f = flip(s, "UB", True)
    print(f"U_b needed for U_eq = V_to, {lab}: {s['UB']*f:.2f} m/s ({s['UB']*f/0.030:.0f} SL/s at 30 mm SL)")
# 0.40 g body too
for lab, s in (("GENEROUS 0.40 g", dict(BASE, m=0.40e-3)), ("CENTRAL 0.40 g", dict(CENTRAL, m=0.40e-3))):
    f = flip(s, "UB", True)
    print(f"U_b needed for U_eq = V_to, {lab}: {s['UB']*f:.2f} m/s")

hr("4. Analytic check: foil-only ceiling U_max = U_b * sqrt(1 + Cdb*A/(S*C_D)) (C_D const, air drag ignored)")
for s, lab in ((BASE, "GENEROUS"), (CENTRAL, "CENTRAL")):
    k = math.sqrt(1 + s["Cdb"] * s["A_FRONT"] / (s["S_CAUDAL"] * s["CD_F"]))
    print(f"{lab}: U_max/U_b = {k:.2f}; so U_b enters LINEARLY, Cdb, A_FRONT, 1/S_CAUDAL, 1/CD_F under a square root")
