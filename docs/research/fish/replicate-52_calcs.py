import math
def Cd(Re): return max(2*1.328*Re**-0.5, 0.072*Re**-0.2)
# check Eloy table rows (S/h2, Re -> Li)
for n,sh,Re,Li in [("rainbow trout 20.1cm",8.2,1.1e5,0.067),("rainbow trout j 5.5cm",8.8,1.6e4,0.184),("silverside",10.9,1.7e4,0.224),("goldfish common (Blake Cd)",4.7,2.1e4,0.093),("goldfish eggfish (Blake Cd)",10.6,7.1e3,0.538),("bullfrog tadpole",11.0,2.3e4,0.193)]:
    print("%-28s Li_eq16=%.3f table=%.3f  St_pow=%.3f"%(n,sh*Cd(Re),Li,0.75*(sh*Cd(Re))**(1/3)))
L=0.04; nu=1e-6; S=0.4*L*L
print()
for U in (0.548,0.84,1.95,5.84):
    Re=U*L/nu
    for hL in (0.15,0.20,0.25,0.30):
        sh=0.4/hL**2; Li=sh*Cd(Re); St=0.75*Li**(1/3)
        print("U=%.3f Re=%.2e Cd=%.5f h/L=%.2f S/h2=%5.2f Li=%.4f St=%.3f  f(A=0.2TL)=%.0f Hz"%(U,Re,Cd(Re),hL,sh,Li,St,St*U/(0.2*L)))
print()
for St in (0.2,0.25,0.3,0.48,0.54,0.56,0.59,0.79,1.02):
    print("St %.2f -> f at 1.95 m/s, A=8mm: %.0f Hz"%(St,St*1.95/0.008))
