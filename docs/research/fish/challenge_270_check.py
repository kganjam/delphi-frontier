"""Challenge 270: independent re-derivation of the S32 low-exit support numbers, plus one relaxed assumption.
Inputs are S32's stated inputs (S32-organism.md section 2); the code is written fresh, not copied.
(1) Steady hydrofoil support only (S32's model): CL_z needed at 0.45 m/s and speed at which CL_z = 1.
(2) Relaxed: thrust vector may tilt nose-up by alpha (body pitched, tail down), so
    F_z = T sin(alpha) + q S CL_z,  horizontal: T cos(alpha) - D_ind(CL_z) - D_wing - D_body - F_sh >= 0.
"""
import math
rw, ra, g, sig = 1000.0, 1.225, 9.81, 0.072
c, h = 6e-3, 9e-3
S_lobe = 0.7 * c * h / 2                 # 18.9 mm^2
Sw, CLmax, Af = 192e-6, 1.07, 24e-6
k = 1 / (math.pi * 0.8 * 5)

def cdl(U, mode):
    if mode == "const": return 0.08
    Re = U * c / 1e-6
    if Re < 4780: return 0.08 * math.sqrt(4780 / Re)
    if Re > 9560: return 0.08 * math.sqrt(9560 / Re)
    return 0.08

cases = {  # name: m, phi, Cd_body(for G), cdmode, CD0, costh, dcos
 "generous": (0.25e-3, 1.0, 0.3, "scaled", 0.08, 0.0, 0.0),
 "central":  (0.25e-3, 0.5, 0.2, "scaled", 0.12, 0.5, 0.1),
 "stingy":   (0.40e-3, 0.25, 0.1, "const", 0.20, 1.0, 0.3),
}

def setup(m, phi, Cdb, mode, CD0, cth, dc):
    G = (Cdb * Af / (2 * S_lobe) + cdl(1.38, mode)) * 1.38**2
    Vto = math.sqrt(2 * m * g / (ra * Sw * CLmax))
    return dict(m=m, W=m*g, S=phi*S_lobe, d=phi*h/2, G=G, mode=mode, CD0=CD0,
                Fsv=2*sig*c*cth, Fsh=2*sig*c*dc, Vto=Vto)

def parts(U, p):
    qa, qw = 0.5*ra*U*U, 0.5*rw*U*U
    CL = min(CLmax, p["W"]/(qa*Sw)); Lw = qa*Sw*CL
    Dw = qa*Sw*(p["CD0"]+k*CL*CL); Db = qa*0.3*Af
    need = max(0, p["W"] + p["Fsv"] - Lw)
    T = 0.5*rw*p["S"]*(p["G"] - cdl(U, p["mode"])*U*U)
    AR = 2*p["d"]**2/p["S"]
    Dind = lambda CLz: qw*p["S"]*CLz**2/(math.pi*0.8*AR)
    return qw, need, T, Dw+Db+p["Fsh"], Dind

def cl_needed(U, p):
    qw, need, *_ = parts(U, p); return need/(qw*p["S"])

def bisect(f, lo, hi):
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if f(mid): hi = mid
        else: lo = mid
    return hi

def supported_tilt(U, p, CLzmax=1.0):
    """True if some (alpha, CL_z<=CLzmax) gives vertical balance with horizontal net >= 0."""
    qw, need, T, Dpar, Dind = parts(U, p)
    for i in range(0, 1001):
        CLz = CLzmax * i / 1000
        rem = need - qw*p["S"]*CLz
        if rem <= 0:
            if T - Dind(CLz) - Dpar >= 0: return True
            continue
        if rem > T: continue
        a = math.asin(rem / T)
        if T*math.cos(a) - Dind(CLz) - Dpar >= 0: return True
    return False

def min_tilt_angle(U, p):
    qw, need, T, Dpar, Dind = parts(U, p)
    best = None
    for i in range(0, 1001):
        CLz = i/1000; rem = need - qw*p["S"]*CLz
        if rem <= 0 or rem > T: continue
        a = math.asin(rem/T)
        if T*math.cos(a) - Dind(CLz) - Dpar >= 0:
            best = a if best is None else min(best, a)
    return best

for name, args in cases.items():
    p = setup(*args)
    qw, need, T, Dpar, Dind = parts(0.45, p)
    print(f"--- {name}: W={p['W']*1e3:.3f} mN, S_imm={p['S']*1e6:.2f} mm2, G={p['G']:.3f} m2/s2 "
          f"(fA={math.sqrt(p['G']/2.55):.3f} m/s), Vto={p['Vto']:.2f}")
    print(f"  at 0.45: q={qw:.1f} Pa, qS={qw*p['S']*1e3:.3f} mN, vertical need={need*1e3:.3f} mN, "
          f"T_lobe={T*1e3:.3f} mN, CLz needed (steady) = {cl_needed(0.45,p):.2f}")
    Umin = bisect(lambda U: cl_needed(U, p) <= 1.0, 0.05, 5.0)
    print(f"  min speed, steady CLz<=1: {Umin:.3f} m/s")
    print(f"  supported at 0.45 with thrust tilt + CLz<=1? {supported_tilt(0.45,p)}"
          + (f", min tilt {math.degrees(min_tilt_angle(0.45,p)):.1f} deg" if supported_tilt(0.45,p) else ""))
    print(f"  at 0.45, CLz=0 (pure tilt, vertical tail-stand): T/need = {T/need:.2f}")
    print(f"  supported at 0.45 with tilt and CLz<=0 (no hydrofoil lift)? {supported_tilt(0.45,p,CLzmax=0.0)}")

print("\n--- scan (support region is not monotonic in U, so scan rather than bisect) ---")
for name, args in cases.items():
    p = setup(*args)
    Us = [0.30 + 0.01*i for i in range(0, 171)]
    st = [u for u in Us if cl_needed(u, p) <= 1.0]
    tl = [u for u in Us if supported_tilt(u, p)]
    fmt = lambda L: f"{L[0]:.2f} m/s" if L else "none in 0.30-2.00 m/s"
    print(f"{name}: steady-only first supported U = {fmt(st)}; with tilt first supported U = {fmt(tl)}; "
          f"St=fA/U at 0.45 = {math.sqrt(p['G']/2.55)/0.45:.2f}")
