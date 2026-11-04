"""Challenge 110 (adversarial review of S7-D-D). All outputs are CALCULATIONS unless noted.
Inputs are the claim's stated inputs; E (bone Young's modulus) is MY ASSUMPTION, not sourced."""
import math
g, rho, m = 9.81, 1.2, 0.4e-3; W = m*g
def M_root(V, n, CL=0.78, AR=9, hw=2.5e-3):
    S = 2*W/(rho*V*V*CL); b = math.sqrt(AR*S); s = b/2 - hw
    return n*(W/2)*(4*s/(3*math.pi)), S, b
M, S, b = M_root(3, 3)
print(f"1. worst-case root moment {M:.3e} N m  (wing area both fins {S*1e4:.2f} cm^2, span {b*100:.1f} cm)")
sig = 62.6e6
Zreq = M/sig; dreq = (32*Zreq/math.pi)**(1/3)
print(f"   Z_req {Zreq*1e9:.3e} mm^3, solid-rod d_req {dreq*1e3:.3f} mm")
geo = {"low": (0.36e-3, 0.055e-3), "mid": (0.40e-3, 0.08e-3), "high": (0.44e-3, 0.10e-3)}
print("2. independent section moduli (Z = sum_w h^2/6) and ratios")
R = {}
for k, (sw, h) in geo.items():
    Z = sw*h*h/6; d = (32*Z/math.pi)**(1/3); R[k] = Z/Zreq
    print(f"   {k}: Z {Z*1e9:.3e} mm^3, d_eq {d*1e3:.3f} mm, capacity/demand {R[k]:.3f}, stress/yield {1/R[k]:.2f}")
print("3. relaxation: fully plastic rectangle (shape factor 1.5) instead of first yield")
for k in R: print(f"   {k}: {1.5*R[k]:.2f}")
print("   bone strength multiple needed to pass at worst case (elastic / plastic):",
      {k: (round(1/R[k], 2), round(1/(1.5*R[k]), 2)) for k in R})
print("4. thickening factor on h to reach ratio 1 / 1.5 (independent plates):",
      {k: (round(math.sqrt(1/R[k]), 2), round(math.sqrt(1.5/R[k]), 2)) for k in R})
print("5. isometric size loophole: scanned-fish length fraction of design fish at which ratio=1:",
      {k: round(R[k]**(1/3), 3) for k in R})
print("6. Euler buckling of the radials in the hinged (compression) load path, pinned-pinned,")
print("   4 independent plates, L = 0.95 mm (row length; upper bound on free length), E ASSUMED")
L = 0.95e-3
for E in (5e9, 10e9, 20e9):
    for k, (sw, h) in geo.items():
        w = sw/4; I = w*h**3/12; Pcr = 4*math.pi**2*E*I/L**2; A = sw*h
        line = []
        for r in (1.0e-3, 0.5e-3, 0.15e-3):
            F = M/r; line.append(f"r={r*1e3:.2f}mm F={F*1e3:.0f}mN sig={F/A/1e6:.1f}MPa Pcr/F={Pcr/F:.2f}")
        print(f"   E={E/1e9:.0f}GPa {k}: Pcr={Pcr*1e3:.0f} mN (sig_cr {Pcr/A/1e6:.0f} MPa) | " + " ; ".join(line))
print("7. composite (fused) section if the shafts are offset out of plane (my image measurement:")
print("   unoccluded distal stations, filled 51-83 um, envelope 139-176 um). 3 shafts w=0.10 mm, h=0.06 mm")
w, h = 0.10e-3, 0.06e-3
Zind = 3*w*h*h/6
for E_env in (0.130e-3, 0.160e-3):
    off = (E_env - h)/2
    I = 3*w*h**3/12 + w*h*2*off**2; Zc = I/(E_env/2)
    print(f"   envelope {E_env*1e6:.0f} um: Z_fused/Z_independent = {Zc/Zind:.2f}")
