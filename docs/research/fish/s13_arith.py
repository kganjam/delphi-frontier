import math
g=9.81; rho_air=1.225; nu=1.5e-5
m=0.4e-3; W=m*g
print(f"W = {m:.1e} kg * {g} = {W:.3e} N  ({W*1e3:.2f} mN)")
S=4e-4; CL=0.8
V=math.sqrt(2*W/(rho_air*S*CL))
print(f"V = sqrt(2*{W:.3e}/({rho_air}*{S:.1e}*{CL})) = {V:.2f} m/s")
c=0.01; print(f"Re = {V:.2f}*{c}/{nu:.1e} = {V*c/nu:.0f}")
b2=0.02                      # semi-span 2 cm
w=(W/2)/b2                   # UDL per half wing
print(f"UDL w = (W/2)/b2 = {W/2:.3e}/{b2} = {w:.4f} N/m")
delta_allow=0.10*b2
EI_req = w*b2**4/(8*delta_allow)
print(f"EI_req = w*b2^4/(8*delta) = {w:.4f}*{b2**4:.3e}/(8*{delta_allow:.0e}) = {EI_req:.3e} N m^2")
for EI_meas,lab in [(1.5e-9,'low'),(2.75e-9,'mid'),(4.0e-9,'high')]:
    print(f"  ratio vs measured {lab} ({EI_meas:.2e}) = {EI_req/EI_meas:.0f}x")
# homogenised whole-fin modulus from Puri EI and Ieff
print()
for EI in (1.5e-9,4.0e-9):
    for I in (3e-16,7e-16):
        print(f"E_eff = {EI:.1e}/{I:.0e} = {EI/I/1e6:.1f} MPa")
# geometric equivalent
print()
for r in (245,356,653):
    print(f"  pure-I route: diameter x {r**0.25:.2f} for {r}x EI ; pure-E route: E x {r}")
# required E on measured tissue baselines
print()
for Ebase,lab in [(5e6,'homogenised fin plate 5 MPa'),(1.0e9,'teleost whole-ray 1.0 GPa (Flammang-type)'),(0.3e9,'hydrated collagen fibril 0.3 GPa')]:
    print(f"  from {lab}: required E = {Ebase*356/1e9:.1f} GPa (356x)")
