"""Challenge 267: independent recomputation of S25-D. All outputs are CALCULATED, not observed.
Inputs: k = 1.98 N/m, L = 40.3 mm (Alben et al. 2007); unsegmented proximal fraction 0.40
(Flammang et al. 2013 abstract: 'distal 60% of the fin ray is segmented').
"""
k, L, f = 1.98, 0.0403, 0.40
print("Uniform Euler-Bernoulli cantilever, EI = k a^3 / 3")
for name, a in [("L/2", L/2), ("2L/3", 2*L/3), ("L", L)]:
    ei = k*a**3/3
    print(f"  a={name:4s} EI={ei:.3e}  one-free(/12)={ei/12:.3e}  565e-6/EI={565e-6/ei:6.1f}  3.8e-6/EI={3.8e-6/ei:.2f}")

def compliance(a, EI1, EI2, f=f, L=L, n=200000):
    # deflection/force at load point a: integral_0^a (a-x)^2 / EI(x) dx
    dx = a/n; s = 0.0
    for i in range(n):
        x = (i+0.5)*dx
        s += (a-x)**2/(EI1 if x < f*L else EI2)*dx
    return s

print("\nStepped ray: proximal 40% EI1 = 565e-6, distal EI2 solved so k = 1.98 N/m")
for name, a in [("L/2", L/2), ("2L/3", 2*L/3), ("L", L)]:
    c1 = compliance(a, 565e-6, 1e300)          # proximal-only compliance
    rest = 1/k - c1
    c2unit = compliance(a, 1e300, 1.0)         # distal compliance per 1/EI2
    EI2 = c2unit/rest
    print(f"  a={name:4s} EI2={EI2:.3e}  proximal share of compliance={c1*k*100:.1f}%  check k={1/compliance(a,565e-6,EI2):.3f}")

print("\nSame test with EI1 = 3.8e-6 (if 3.8e-6 were the proximal value)")
for name, a in [("2L/3", 2*L/3)]:
    c1 = compliance(a, 3.8e-6, 1e300); rest = 1/k - c1
    print(f"  a={name} remaining compliance {'NEGATIVE: impossible' if rest<=0 else 'ok'}; EI2={compliance(a,1e300,1.0)/rest if rest>0 else float('nan'):.3e}")
