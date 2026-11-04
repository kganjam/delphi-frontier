import math
rho,g=1.2,9.81; m=0.4e-3; L=0.04; Iy=m*L*L/12
St,lt,at=1e-4,0.02,1.6
def f(V): return math.sqrt(0.5*rho*V*V*St*lt*at/Iy)/(2*math.pi)
print("Iy",Iy)
for V in (1,2,3): print("V",V,"f",round(f(V),3),"R@0.5",round(f(V)/0.5,2),"R@10",round(f(V)/10,3),"R@20",round(f(V)/20,3))
# trim speed of S18 reference wing 10 cm^2
for CL in (1.0,0.75,0.5):
    V=math.sqrt(2*m*g/(rho*1e-3*CL)); print("CL",CL,"Vtrim",round(V,2),"f",round(f(V),2),"R@10",round(f(V)/10,2))
# replicate-260 band
for fr in (3.1,5.0,7.2): print("rep260 f",fr,"R@10",round(fr/10,2),"R@20",round(fr/20,2))
# design-margin view: if loop must exceed mode by factor k (sensor >= k * f_mode)
for k in (3,5,10):
    print("k",k,"needed sensor Hz at 1.9:",round(1.91*k,1),"at 5:",5*k,"at 7.2:",round(7.2*k,1))
