"""S26-D-D: attack the weakest input of S26-D. Every output is CALCULATED; nothing here is measured by me.
Run: python3 -I docs/research/fish/S26_DD_calc.py
Inputs and their sources are listed in docs/research/fish/S26-D-deepen.md section 5."""
from math import log

EI_REQ  = 6.3e-4    # N m^2 per ray, S6-D calculated (m=0.10 kg, N=14, L=0.12 m, dL<=0.10)
EI_RELAY= 3.8e-6    # N m^2, bluegill, Puri 2018 relaying Flammang 2013
EI_1F   = 1.07e-6   # N m^2, bluegill one-hemitrich-free, back-calculated by S26-D from Alben 2007 1.98 N/m
F_A     = 12.0      # Alben 2007 clamped / one-free, effectively n=1
L_REQ   = 0.120     # m
L_BG    = 0.0403    # m, Alben 2007 bluegill max pectoral ray length (measured)

def margin(ei_src, L_src, n=4.0, f=F_A, ei_req=EI_REQ, d_ratio=1.0):
    """>1: actively stiffened scaled ray meets requirement. d_ratio multiplies the diameter that
    EI ~ L^n scaling would predict at L_REQ (EI ~ d^4 at fixed modulus and section shape)."""
    S = (L_REQ / L_src) ** n * d_ratio ** 4
    return ei_src * S * f / ei_req

print("== 1. factor-of-two sensitivity of S26-D's conclusion ==")
for lab, src in (("relay path (S26-D)", EI_RELAY), ("primary one-free path (challenge-92)", EI_1F)):
    b = margin(src, L_BG)
    print(f"-- {lab}: baseline margin {b:.2f}")
    S = (L_REQ / L_BG) ** 4
    cases = [("EI_req x2", dict(ei_req=2*EI_REQ)), ("EI_req /2", dict(ei_req=EI_REQ/2)),
             ("EI_src x2", dict(ei_src=2*src)), ("EI_src /2", dict(ei_src=src/2)),
             ("F_a x2", dict(f=2*F_A)), ("F_a /2", dict(f=F_A/2)),
             ("L_src x2 (80.6 mm)", dict(L_src=2*L_BG)), ("L_src /2 (20.2 mm)", dict(L_src=L_BG/2)),
             ("diameter at 120 mm x2", dict(d_ratio=2.0)), ("diameter at 120 mm /2", dict(d_ratio=0.5))]
    for name, kw in cases:
        kw = {"ei_src": src, "L_src": L_BG, **kw}
        m = margin(**kw)
        print(f"   {name:24s} margin {m:8.3f}  {'pass' if m >= 1 else 'FAIL'}  (x{m/b:.4g} vs baseline)")
    # size factor S x2 / /2 is identical to EI_src x2 / /2; exponent shift that halves S:
    print(f"   exponent change that halves S: dn = {log(2)/log(L_REQ/L_BG):.2f} (n 4 -> {4-log(2)/log(L_REQ/L_BG):.2f})")
    nbe = log(EI_REQ / (src * F_A)) / log(L_REQ / L_BG)
    print(f"   break-even exponent n (12x exactly closes): {nbe:.2f}; break-even diameter ratio: {(1/b)**0.25:.3f}")

print("\n== 2. independent anchor: Aiello et al. 2017 PNAS, labrid ray 3, three-point bending at 50% length ==")
# measured (authors): high-AR species 190+-30 .. 210+-50 e-9 N m^2 ; low-AR 20+-10 .. 40+-10 e-9 N m^2
# ray length: inferred by me from the paper's paired thresholds (% ray length, mm); pairing is my assumption
pairs = {"high-AR min": (1.05, 5.91), "high-AR max": (1.50, 8.20), "low-AR min": (3.6, 17.84), "low-AR max": (6.12, 30.67)}
Ls = {}
for k, (mm, pct) in pairs.items():
    Ls[k] = mm / (pct / 100)
    print(f"   implied ray length from {k}: {mm} mm / {pct}% = {Ls[k]:.1f} mm")
L_LAB_LO, L_LAB_HI = min(Ls.values()) / 1e3, max(Ls.values()) / 1e3
for lab, eis in (("high-AR (wing-like)", (1.9e-7, 2.1e-7)), ("low-AR (paddle)", (2e-8, 4e-8))):
    for ei in eis:
        for L in (L_LAB_LO, L_LAB_HI):
            S = (L_REQ / L) ** 4
            need = EI_REQ / (ei * S)
            print(f"   {lab:20s} EI {ei:.1e} at L {L*1e3:4.1f} mm: S x{S:6.0f}; scaled passive {ei*S:.2e}; need {need:6.2f}x; 12x margin {F_A/need:5.2f} {'pass' if F_A>=need else 'FAIL'}")
print("   break-even exponent n, labrid high-AR (EI 2.0e-7, L 19 mm):",
      f"{log(EI_REQ/(2.0e-7*F_A))/log(L_REQ/0.019):.2f}")
print("   break-even exponent n, labrid low-AR (EI 3.0e-8, L 19 mm):",
      f"{log(EI_REQ/(3.0e-8*F_A))/log(L_REQ/0.019):.2f}")
print("   labrid high-AR, n=3:", f"need {EI_REQ/(2.0e-7*(L_REQ/0.019)**3):.1f}x;", "n=3.5:", f"need {EI_REQ/(2.0e-7*(L_REQ/0.019)**3.5):.1f}x")

print("\n== 3. two-point interspecific exponent, bluegill (40.3 mm) vs labrid (19 mm) ==")
for bl_lab, bl in (("bluegill relay 3.8e-6", 3.8e-6), ("bluegill Alben low 1e-6", 1e-6), ("bluegill Alben high 1e-5", 1e-5)):
    for lb_lab, lb in (("labrid high-AR 2.0e-7", 2.0e-7), ("labrid low-AR 3.0e-8", 3.0e-8)):
        n = log(bl / lb) / log(0.0403 / 0.019)
        print(f"   {bl_lab:26s} vs {lb_lab:22s}: n = {n:5.2f}")
