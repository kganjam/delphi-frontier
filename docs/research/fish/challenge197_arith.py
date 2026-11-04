import math
# independent re-derivation from the STATED inputs only
g=9.81
m=0.4e-3
W=m*g
print("W (N) =", W)

rho=1.225; S=4e-4; CL=0.8
V=math.sqrt(2*W/(rho*S*CL))
print("V (m/s) =", V)
print("Re (c=0.01, nu=1.5e-5) =", V*0.01/1.5e-5)

b2=0.02
w=(W/2)/b2
print("UDL w (N/m) =", w)

# cantilever, UDL, tip deflection = w L^4 / (8 EI)
for frac in (0.10,0.20,0.40):
    d=frac*b2
    EI=w*b2**4/(8*d)
    print(f"delta={frac:.0%} semispan -> EI_req = {EI:.3e}")
    for EIm in (1.5e-9,2.75e-9,4.0e-9):
        print(f"    gap vs {EIm:.2e} = {EI/EIm:.0f}x")

# sanity: is whole-fin EI the right comparator for a WING SPAR?
# Puri EI is whole caudal fin (16-18 rays, 5-8mm wide plate).
# per-ray share:
for EIm in (1.5e-9,4.0e-9):
    print(f"whole-fin {EIm:.1e} / 17 rays = {EIm/17:.2e} per ray")

# required E given I of a 0.15 mm solid rod
for d in (1e-4,1.5e-4,2e-4):
    I=math.pi*d**4/64
    print(f"d={d*1e3:.2f}mm  I={I:.3e} m^4  E for EI=9.8e-7 (single rod) = {9.8e-7/I/1e9:.1f} GPa")
# and for a spar made of N such rods
for N in (17,34):
    I=N*math.pi*(1.5e-4)**4/64
    print(f"{N} rods d=0.15mm, I_sum={I:.3e}, E needed = {9.8e-7/I/1e9:.1f} GPa")
EI_req=9.81e-7
print("=== A. unit-consistent required EFFECTIVE modulus ===")
print("E_req = EI_req / I_eff, using Puri's MEASURED I_eff")
for I in (7e-16,5e-16,3e-16):
    print(f"  I_eff={I:.0e} -> E_req = {EI_req/I/1e9:.2f} GPa")

print("\n=== B. the measured (EI, I_eff) pair forces E_eff ===")
for EI in (1.5e-9,2.75e-9,4.0e-9):
    for I in (7e-16,3e-16):
        print(f"  EI={EI:.2e}, I={I:.0e} -> E_eff = {EI/I/1e6:.1f} MPa")

print("\n=== C. is the claim's 'baseline x 357' self-consistent? ===")
print("If ray material E were 0.3 GPa and I_eff=5e-16, implied EI would be:")
for E in (0.3e9,1.0e9):
    print(f"  E={E/1e9:.1f} GPa -> EI = {E*5e-16:.2e} N m^2 ; measured is 1.5-4e-9")
    print(f"     overshoot vs measured mid 2.75e-9 = {E*5e-16/2.75e-9:.0f}x")
print("-> baselines of 0.3-1 GPa are INCOMPATIBLE with the measured EI/I_eff pair.")
print("   Multiplying them by 357 double-counts the architectural loss.")

print("\n=== D. published teleost fin-ray EI vs requirement ===")
for v,lab in [(3.8e-6,'bluegill pectoral ray, Puri citing Flammang 2013'),
              (565e-6,'bluegill, Flammang 2013 abstract as summarised')]:
    print(f"  {lab}: EI={v:.2e} -> {v/EI_req:.1f}x the requirement 9.81e-7")
