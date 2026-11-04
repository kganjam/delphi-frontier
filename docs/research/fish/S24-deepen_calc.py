"""S24-D: sensitivity of the S24 taxi-frequency verdict, and recomputation with an improved St input.
Every output is a CALCULATION. Inputs: M = measured (literature), A = assumption. See S24-deepen.md.
Run: python3 S24-deepen_calc.py
"""
U = 1.95          # m/s, 3-BL glide target (inherited, calc in zebrafish-glide-physics.md)
L = 0.040         # m, project premise TL
A = 0.008         # m, peak-to-peak tail amplitude 0.20 TL (A, S24)
FMAX = 52.0       # Hz, adult zebrafish escape EMG maximum (M, Kyriakatos 2011)
NU = 1e-6

def f_req(St, U=U, A=A):
    return St * U / A

print("1. Sensitivity of the recorded answer (St 0.54-0.816, A 8 mm, U 1.95, fmax 52)")
for St in (0.54, 0.816):
    base = f_req(St) / FMAX
    print(f"  St {St}: f_req {f_req(St):.0f} Hz, ratio {base:.2f}")
    for name, r in (("St/2", f_req(St / 2) / FMAX), ("A*2", f_req(St, A=2 * A) / FMAX),
                    ("U/2", f_req(St, U=U / 2) / FMAX), ("fmax*2", f_req(St) / (2 * FMAX))):
        print(f"     {name:7s} -> ratio {r:.2f}")
print("  Break-even values (ratio = 1), all else at recorded values:")
print(f"    St* = {FMAX * A / U:.3f}  (recorded 0.54 must fall {0.54 / (FMAX * A / U):.2f}x; 0.816 {0.816 / (FMAX * A / U):.2f}x)")
for St in (0.54, 0.816):
    print(f"    at St {St}: A* = {St * U / FMAX * 1e3:.1f} mm ({St * U / FMAX / L:.2f} TL), "
          f"fmax* = {f_req(St):.0f} Hz, U* = {FMAX * A / St:.2f} m/s")
print("  Source spread of each input (max/min):")
print(f"    St (peak-to-peak) 0.20 band edge .. 1.03 Mwaffo burst: {1.03 / 0.20:.1f}x")
print(f"    A 0.15..0.25 TL: {0.25 / 0.15:.2f}x")

print("\n2. Operating-point Reynolds number")
for Lx in (0.040, 0.033):
    print(f"  L {Lx*1e3:.0f} mm: Re = {U * Lx / NU:.2e}")

print("\n3. Improved input: measured stride length U/(fL) at Re 2e4-1e6 (Bainbridge 1958; Wardle 1975)")
print("   f_req = U/(lambda*L) -- needs no assumed A or St")
for Lx in (0.040, 0.033):
    for lam in (0.6, 0.7, 0.75, 0.8, 1.0):
        f = U / (lam * Lx)
        print(f"  L {Lx*1e3:.0f} mm, lambda {lam:.2f} L/beat: f_req {f:5.1f} Hz, ratio to 52 Hz {f / FMAX:.2f}")
    fb = 4.0 / 3.0 * (U / Lx + 1.0)   # Bainbridge V = L(3f-4)/4, V in cm/s, L in cm, f in Hz
    print(f"  L {Lx*1e3:.0f} mm, Bainbridge formula f = (4/3)(U/L + 1 Hz): {fb:.1f} Hz, ratio {fb / FMAX:.2f}")
# Equivalent St (Seo et al. 2025 reduction): St_A = (4/3)(A_F/L)(1 + f0 L/U), A_F/L = 0.18 peak-to-peak
for AFL in (0.18, 0.20):
    St = 4.0 / 3.0 * AFL * (1 + 1.0 * L / U)
    print(f"  Bainbridge-equivalent St (A_F/L {AFL}) at 1.95 m/s, L 40 mm: {St:.3f}")
print(f"  Seo 2025 simulated St_A 0.28 at Re 3.6e4 with S24 A=8 mm: f_req {f_req(0.28):.0f} Hz, ratio {f_req(0.28)/FMAX:.2f}")
print(f"  Seo 2025 St_min 0.23: f_req {f_req(0.23):.0f} Hz, ratio {f_req(0.23)/FMAX:.2f}")

print("\n4. Cross-check: laminar St ~ Re^-1/4 (Gazzola 2014/2015 scaling) from Mwaffo 2017 zebrafish")
Re_target = U * L / NU
for St0, lab in ((0.73, "cruise"), (1.03, "burst")):
    for Re0 in (900, 3400):
        for Ret in (1e4, 3e4, Re_target):
            St = St0 * (Re0 / min(Ret, Re_target)) ** 0.25
            print(f"  {lab} St {St0} at Re {Re0}, laminar law to Re_t {Ret:.0e} then flat: St {St:.2f} -> f {f_req(St):.0f} Hz ({f_req(St)/FMAX:.2f}x)")

print("\n5. Context: Videler 1993 Vmax = 0.4 + 7.4 L (search-summary) at L 0.04: %.2f m/s" % (0.4 + 7.4 * 0.04))
