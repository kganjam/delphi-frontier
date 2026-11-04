import numpy as np
g=9.81; W=0.4e-3*g
def EIreq(L,tol): return (W/2)*L**2/(8*tol)
for nm,L,tol,EIc in (('central',0.04,0.10,4e-9),('lenient',0.02,0.50,5e-9)):
    S=EIreq(L,tol)/EIc
    for Et in (5,10):
        for C in (Et/0.35, round(Et/0.35)):
            print(nm, f"EIreq={EIreq(L,tol):.4g} S={S:.2f} C={C:.2f} margin=R*={S/C:.3f}")
# tip deflection coefficient: uniform vs elliptic load, same total, cantilever, uniform EI
n=4001; y=np.linspace(0,1,n)
def tipdefl(w):
    w=w/np.trapezoid(w,y)  # unit total load
    M=np.array([np.trapezoid(w[i:]*(y[i:]-y[i]),y[i:]) for i in range(n)])
    return np.trapezoid(M*(1-y),y)
u=tipdefl(np.ones(n)); e=tipdefl(np.sqrt(np.clip(1-y**2,0,None)))
print("uniform coeff",u,"(expect 1/8)", "elliptic coeff",e,"ratio",e/u)
print("lenient C=29 margin elliptic", 1.353*e/u, " C=28.57:", 39.24/28.571*e/u)
print("L flip at lenient C=29:", 0.02/np.sqrt(1.353))
print("labrid scale",(0.4/22.44)**(4/3))
