"""Independent arithmetic for challenge 197 (claim S13). Inputs from Puri et al. 2018 as quoted in S13-protein.md."""
import math
g=9.81; m=0.4e-3; W=m*g
b2=0.02; w=(W/2)/b2
for frac in (0.10,0.20,0.30,0.50):
    d=frac*b2; EI=w*b2**4/(8*d)
    print(f"delta={frac:.0%}: EI_req={EI:.3e}  gap vs 4e-9={EI/4e-9:.0f}x  vs 1.5e-9={EI/1.5e-9:.0f}x")
EIreq=w*b2**4/(8*0.1*b2)
print("\nRequired effective modulus at Puri's measured I_eff (no outside baseline):")
for I in (7e-16,3e-16):
    print(f"  E_req = {EIreq:.3e}/{I:.0e} = {EIreq/I/1e9:.2f} GPa")
print("\nRay-only I check, 16-18 solid round rays, d = 0.10/0.15/0.20 mm:")
for d in (1e-4,1.5e-4,2e-4):
    for n in (16,18):
        I=n*math.pi*d**4/64
        print(f"  d={d*1e3:.2f} mm n={n}: I={I:.2e} m^4  E_eff(1.5e-9..4e-9)={1.5e-9/I/1e6:.1f}..{4e-9/I/1e6:.1f} MPa"
              f"  EI if E=1 GPa: {1e9*I:.2e} N m^2 ({EIreq/(1e9*I):.1f}x short of EI_req)")
print("\nAuthor's material route, required E = baseline x gap:")
for lab,E in (("distal ray min 0.11 GPa",0.11e9),("proximal ray min 0.24 GPa",0.24e9),("hydrated fibril 0.3 GPa",0.3e9),("proximal ray mean 1.34 GPa",1.34e9)):
    print(f"  {lab}: {E*245/1e9:.0f}-{E*654/1e9:.0f} GPa")
