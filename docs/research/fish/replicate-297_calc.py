#!/usr/bin/env python3
"""Replicate-297: independent re-derivation of the CL needed to close S3's most generous launch
when Park & Choi 2010's reference area (pectoral + pelvic + BODY planform) is applied consistently.
All outputs are CALCULATIONS. Run: python3 -I docs/research/fish/replicate-297_calc.py"""
from math import sqrt, pi

g, rho = 9.81, 1.225
m_b = 0.40e-3                 # kg, S3 brief
sigma = 1150 * 120e-6         # kg/m2, S3 central fin tissue (0.138)
S_w = 1070e-6                 # m2, S10 wing (S3 most generous planform)
s = 2 * 0.04                  # m, 2 BL run-up
eta, fm, P_av = 0.37, 0.6, 142.7
M = m_b + sigma * S_w

def P_req(CL, S_lift):
    V = sqrt(2 * M * g / (rho * S_lift * CL))
    return V**3 / (4 * s) / eta * M / (fm * m_b), V

# control: S3's 409 W/kg at CL 1.07, wing only
P0, V0 = P_req(1.07, S_w)
print(f"control: CL1.07 wing-only P={P0:.1f} W/kg  V={V0:.3f} m/s  shortfall {P0/P_av:.3f}x")

# closure: P_req = P_av  ->  V_c^3 = 4 s eta fm m_b P_av / M
Vc = (4 * s * eta * fm * m_b * P_av / M) ** (1/3)
CLS = 2 * M * g / (rho * Vc**2)          # CL * S_lift needed (m2)
print(f"closure V = {Vc:.4f} m/s ; CL*S needed = {CLS*1e6:.1f} mm2")
print(f"CL needed, wing only (S3-D framing): {CLS/S_w:.3f}")

# body planform from McHenry & Lauder 2005 wetted area (adult L 35.4 mm, m 485 mg, S_wet 777 mm2;
# 660 mm2 used in their Fig 8). Elliptical cross-section (their assumption); width/depth ratio ASSUMED.
def ellipse_perim(a, b):
    return pi * (3*(a+b) - sqrt((3*a+b)*(a+3*b)))
for Swet_label, Swet in [("660 (M&L Fig8)", 660), ("777 (M&L Tab1 mean)", 777),
                         ("683 (777 scaled to 0.40 g, m^2/3)", 777*(0.400/0.485)**(2/3))]:
    for wh in (0.4, 0.5, 0.7, 1.0):
        frac = wh / ellipse_perim(1.0, wh/1.0) * 2 / 2  # width w=2b over perimeter with a=1 (h=2), b=wh
        frac = (2*wh) / ellipse_perim(1.0, wh)
        Sb = frac * Swet
        CLn = CLS / (S_w + Sb*1e-6)
        Pb, _ = P_req(1.10, S_w + Sb*1e-6)
        print(f"S_wet {Swet_label:32s} w/h {wh:.1f}: planform/wetted {frac:.3f} S_body {Sb:6.1f} mm2 "
              f"-> CL needed {CLn:.3f}; at CL 1.10 shortfall {Pb/P_av:.3f}x, lift margin {CLn/1.10:.3f}")

# what S_body would give 1.76?
for target in (1.76,):
    print(f"S_body implied by CL_needed={target}: {(CLS/target - S_w)*1e6:.0f} mm2")
# wing-only shortfall at CL 1.10
Pw, _ = P_req(1.10, S_w)
print(f"wing only, CL 1.10: shortfall {Pw/P_av:.3f}x, lift margin {CLS/S_w/1.10:.3f}")
