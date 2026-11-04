"""S26-D: sensitivity and recomputation. Every output here is CALCULATED, nothing is measured.
Run: python3 -I S26_deepen_calc.py"""
EI_REQ = 6.3e-4      # N m^2, per ray, S6-D calculated (m=0.10 kg, N=14, L=0.12 m, n=1, dL<=0.10)
EI_P   = 3.8e-6      # N m^2, Puri 2018 relaying Flammang 2013 (bluegill)
F_A    = 12.0        # Alben 2007 clamped / one-base-free stiffness ratio
F_CEIL = 100.0       # Alben 2007 model asymptote, G > 1e5
L_REQ  = 0.12        # m, ray length behind EI_REQ (S6-D assumption)
L_BG   = 0.0403      # m, bluegill max pectoral ray length, Alben 2007 (6 fish)

def margin(ei_req=EI_REQ, ei_p=EI_P, f=F_A):
    """>1 means active ray meets requirement."""
    return ei_p * f / ei_req

print("== 1. factor-of-two sensitivity, original (size-uncorrected) framing ==")
rows = [("baseline", {}),
        ("EI_req x2", dict(ei_req=2*EI_REQ)), ("EI_req /2", dict(ei_req=EI_REQ/2)),
        ("EI_p x2", dict(ei_p=2*EI_P)), ("EI_p /2", dict(ei_p=EI_P/2)),
        ("F_a x2", dict(f=2*F_A)), ("F_a /2", dict(f=F_A/2))]
for name, kw in rows:
    m = margin(**kw); mc = margin(**{**kw, "f": F_CEIL * (kw.get("f", F_A)/F_A)})
    print(f"{name:10s} measured-path margin {m:6.3f} ({'pass' if m>=1 else 'fail'})   ceiling-path margin {mc:5.2f} ({'pass' if mc>=1 else 'fail'})")
print("EI_p needed for 12x to close:", f"{EI_REQ/F_A:.2e}", "= x", f"{EI_REQ/F_A/EI_P:.1f} of 3.8e-6")
print("candidate EI_p values: Alben B 1e-6..1e-5; Flammang abstract 5.65e-4")
for ei in (1e-6, 1e-5, 5.65e-4):
    print(f"  EI_p={ei:.2e}: gap {EI_REQ/ei:8.1f}x, with 12x margin {margin(ei_p=ei):7.3f}")

print("\n== 2. EI of the bluegill ray implied by Alben's measured 1.98 N/m ==")
k = 1.98; a = (2/3)*L_BG          # assumption: tested ray length = group max ray length
EI_cl = k*a**3/3                  # uniform cantilever, point load at a: k = 3EI/a^3
print(f"a = {a*1e3:.1f} mm; EI_clamped = {EI_cl:.2e}; EI_one-free = {EI_cl/F_A:.2e} N m^2")
for L in (0.020, 0.030, 0.0403):
    aa = (2/3)*L; e = k*aa**3/3
    print(f"  if tested ray L={L*1e3:.0f} mm: EI_clamped={e:.2e}, one-free={e/F_A:.2e}")
print(f"locked bluegill ray vs requirement, no size correction: {EI_REQ/EI_cl:.0f}x short")

print("\n== 3. size correction (isometric EI ~ L^4) from a bluegill-sized ray to the 12 cm ray ==")
for L_src in (0.020, 0.030, L_BG):
    s4 = (L_REQ/L_src)**4
    need = EI_REQ/(EI_P*s4)
    print(f"source ray {L_src*1e3:4.1f} mm: scale x{s4:7.1f}; passive scaled EI {EI_P*s4:.2e}; active factor needed {need:6.2f}x; 12x margin {F_A/need:6.2f}")
print("source ray length at which 12x exactly closes:", f"{L_REQ/(EI_REQ/(EI_P*F_A))**0.25*1e3:.1f} mm")

print("\n== 4. size-corrected (L_src = 40.3 mm) robustness grid ==")
s4 = (L_REQ/L_BG)**4
for lab, er in (("EI_req 6.3e-4", EI_REQ), ("x1.47 tip-heavy load", EI_REQ*1.47), ("replicate upper corner 3.1e-3", 3.1e-3), ("replicate lower corner 1.1e-4", 1.1e-4)):
    for f in (F_A, F_A/2):
        need = er/(EI_P*s4)
        print(f"  {lab:30s} F_a={f:4.1f}: need {need:5.2f}x -> {'pass' if f>=need else 'fail'}")
print("  with EI_p = 1e-6 (Alben low end):", f"need {EI_REQ/(1e-6*s4):.1f}x")
