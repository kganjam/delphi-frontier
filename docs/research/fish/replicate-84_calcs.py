import math
def Cd(Re): return max(2*1.328*Re**-0.5, 0.072*Re**-0.2)
# check against Eloy Table 2 rows (Li = S/h^2 * Cd)
for name,Sh2,Re,Li in [("Rainbow trout 20.1",8.2,1.1e5,0.067),("Saithe",7.0,3.9e5,0.038),("Atl silverside",10.9,1.7e4,0.224),("Bullfrog tadpole",11.0,2.3e4,0.193),("Rainbow trout j",8.8,1.6e4,0.184)]:
    print(f"check {name}: Cd={Cd(Re):.5f} Li_calc={Sh2*Cd(Re):.4f} table={Li}  fit St={0.75*Li**(1/3):.3f}")
L=0.04; U=1.95; A=0.008
for T,nu in [("20C",1.004e-6),("28C",0.836e-6)]:
    Re=L*U/nu; c=Cd(Re)
    print(f"\n{T}: Re={Re:.3g} Cd={c:.5f} (lam {2*1.328*Re**-0.5:.5f}, turb {0.072*Re**-0.2:.5f})")
    for hL in [0.15,0.20,0.25,0.30]:
        Sh2=0.4/hL**2
        for k in [1,2]:
            Li=Sh2*c*k; St=0.75*Li**(1/3); f=St*U/A
            print(f"  h/L={hL:.2f} S/h2={Sh2:5.2f} Cdx{k} Li={Li:.4f} St={St:.3f} f={f:5.1f} Hz  f/52={f/52:.2f}")
print("\nfit at goldfish eggfish Li .538:",0.75*.538**(1/3))
