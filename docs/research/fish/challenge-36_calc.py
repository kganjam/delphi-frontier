# Challenge 36 calc. Every output is a CALCULATION. Floryan et al. 2017 heave thrust law applied to a zebrafish taxi lobe.
import math
rho=1000; g=9.81; W=0.4e-3*g; U=1.95; c=0.006; nu=1e-6
c1,c2=3.52,3.69   # Floryan et al. 2017 heave fit (AR 3.5 rigid foil, Re 4780)
def thrust(f,A,S,CD,c1=c1,c2=c2):
    St=f*A/U; fs=f*c/U; Us=1/math.sqrt(1+math.pi**2*St**2)
    return 0.5*rho*U**2*S*(c1*St**2+c2*St**2*fs*Us-CD), St
# independent check of claimed numbers
for St in (0.2,0.3): print("St %.1f A=8mm f=%.2f Hz"%(St,St*U/0.008))
Cf2=2*1.328/math.sqrt(U*c/nu); print("laminar 2-side Cf=%.4f"%Cf2)
def fneed(A,S,CD,LD,scale=1.0):
    Dair=W/LD
    for f10 in range(10,3000):
        f=f10/10
        T,St=thrust(f,A,S,CD,c1*scale,c2*scale)
        if T>=Dair: return f,St
    return None,None
print("A mm | S cm2/side | CD | L/D | c-scale -> f_needed Hz (St)")
for A in (0.006,0.008,0.010):
  for S in (0.15e-4,0.30e-4):
    for CD in (Cf2,0.15):
      for LD in (8,4):
        for sc in (1.0,0.5):
          f,St=fneed(A,S,CD,LD,sc)
          print("%2.0f | %.2f | %.3f | %d | %.1f -> %s"%(A*1e3,S*1e4,CD,LD,sc,"%.0f Hz (St %.2f)"%(f,St) if f else ">300"))
