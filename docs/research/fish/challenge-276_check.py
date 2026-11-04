"""Challenge 276: independent recomputation for the S5-D claim.
Run: python3 -I docs/research/fish/challenge-276_check.py
Every output is CALCULATED. Only p0, f, and the AR thresholds are inputs carried over from the claim.
"""
import math

# 1. Span, per fin, in SL (inputs as stated in the claim's source note)
f = 1.74
for p0 in (0.173, 0.208, 0.260):
    print(f"span p0={p0:.3f}: {p0*f:.3f} SL")

# 2. Dilation invariance of per-fin AR: a = L^2/S, L->fL, S->f^2 S
L, S = 0.208, 0.0216
for k in (1.0, 1.74, 2.05):
    print(f"per-fin AR at f={k}: {(k*L)**2/(k*k*S):.4f}")

# 3. Equal-ray sector: AR = R^2/(theta R^2/2) = 2/theta
for target in (3.0, 9.0):
    print(f"sector theta for AR={target}: {math.degrees(2/target):.1f} deg")

# 4. Convention map. Per-fin a = L^2/S.
#    doubled per-fin (Walker 2013 convention): 2a
#    tip-to-tip wing, body width b, body strip area Sb in the denominator:
#       AR_w = (2L+b)^2/(2S+Sb) = 2a(1+beta)^2/(1+gamma), beta=b/(2L), gamma=Sb/(2S)
#    Required per-fin a for a given threshold T:
for T in (3.0, 9.0, 10.7, 16.9):
    print(f"T={T}: per-fin a>= {T:.2f}; doubled-conv a>= {T/2:.2f}; "
          f"tip-to-tip beta=0.1,gamma=0 a>= {T/(2*1.1**2):.2f}")

# 5. Under the tip-to-tip convention, dilation does NOT leave AR exactly unchanged,
#    because body width b and body strip area do not scale with f (assumption).
#    AR_w(f) = 2a(1+beta/f)^2/(1+gamma/f^2). Illustrative beta, gamma (ASSUMED, not measured).
a = 2.0
for beta, gamma in ((0.1, 0.05), (0.24, 0.12)):
    r1 = 2*a*(1+beta)**2/(1+gamma)
    r2 = 2*a*(1+beta/f)**2/(1+gamma/f**2)
    print(f"beta={beta}, gamma={gamma}: AR_w f=1 {r1:.2f} -> f=1.74 {r2:.2f} (ratio {r2/r1:.3f})")
