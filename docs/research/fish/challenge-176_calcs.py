"""Challenge 176: independent recompute of S2-D whole-animal L/D. All outputs COMPUTED.
Inputs copied from the S2-D statement (assumed geometry, mass, body drag model), NOT its code path.
Run: python3 -I docs/research/fish/challenge-176_calcs.py
"""
import math
NU, RHO, G = 1.5e-5, 1.2, 9.81
M, S, C = 0.4e-3, 9e-4, 0.015          # ASSUMED (S2)
E = 0.7                                # ASSUMED (S2-D)
CL_CAP = 0.9                           # S2-D's own cap

def blasius2(re): return 2*1.328/math.sqrt(re)

def body_cda(v):  # same physical model as stated in S2-D (ellipsoid 32x7x4 mm, FF 1.5, 2 cm^2 median fins)
    a, b = 0.0035, 0.002
    per = math.pi*(3*(a+b)-math.sqrt((3*a+b)*(a+3*b)))
    cf = 1.328/math.sqrt(v*0.032/NU)
    return 1.5*cf*0.75*per*0.032 + blasius2(v*0.01/NU)*2e-4

def helmbold(ar):  # 3-D lift slope per rad, thin wing
    return 2*math.pi*ar/(2+math.sqrt(ar*ar+4))

def solve(ar, lam, k_mode, body=True):
    k = 1/(math.pi*E*ar) if k_mode == "suction" else 1/helmbold(ar)
    v = 3.0
    for _ in range(200):
        re = v*C/NU
        cd0 = lam*blasius2(re) + (body_cda(v)/S if body else 0)
        cl = min(math.sqrt(cd0/k), CL_CAP)
        vn = math.sqrt(2*M*G/(RHO*S*cl))
        if abs(vn-v) < 1e-10: break
        v = vn
    return cl/(cd0+k*cl*cl), cl, re, math.degrees(cl/helmbold(ar))

# hand check of Blasius anchors vs W&E 1997 range (natural pairing)
print("lambda at W&E ends: Re700 0.14 ->", round(0.14/blasius2(700),2), "; Re2400 0.07 ->", round(0.07/blasius2(2400),2))
print("| AR | lam | k model | whole L/D | wing-alone L/D | CL | Re | alpha_geo (deg, potential slope) |")
for ar in (1.5, 2, 3, 4, 6):
    for lam in (1.0, 1.4, 2.0):
        for km in ("suction", "no-suction"):
            w, cl, re, al = solve(ar, lam, km)
            wa = solve(ar, lam, km, body=False)[0]
            print(f"| {ar} | {lam} | {km} | {w:.2f} | {wa:.2f} | {cl:.2f} | {re:,.0f} | {al:.1f} |")
# control: reproduce S2-D AR4 lam1.4 suction ~4.8 (S2-D reports 4.79 uncapped, 4.80 capped)
assert abs(solve(4, 1.4, "suction")[0]-4.8) < 0.05
print("control passed: suction-model AR4 lam1.4 reproduces S2-D 4.8")
