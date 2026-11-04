"""Challenge 184: independent recomputation of S10-D. All outputs are CALCULATIONS."""
import math
g, rho = 9.81, 1.2
def p_aero(m, R, k=1.2, M=1.5):
    W = m*g; A = math.pi*R**2
    return M*k*(W**1.5)/math.sqrt(2*rho*A)          # W, hover, Rankine-Froude x profile
m0 = 0.4e-3
f0 = 0.0013+0.0023+0.0015+0.0018                   # one fin, Mansuit&Herrel T1
print("one-fin sum", round(f0*100,2), "%  two fins", round(2*f0,4))
f = 2*f0
for R, M in ((0.04,1.5),(0.04,2.0),(0.02,1.5),(0.02,2.0)):
    P = p_aero(m0, R, M=M)
    req = P/(m0*f); fthr = P/m0/134.4
    # mass feedback: add muscle dm to body; solve f' s.t. P(m')/(m' f') = 134.4
    fp = fthr
    for _ in range(100):
        mp = m0*(1-f)/(1-fp)                        # non-muscle mass fixed
        fp = p_aero(mp, R, M=M)/mp/134.4
    mp = m0*(1-f)/(1-fp)
    print(f"R={R} M={M}: P={P*1e3:.2f} mW req={req:.0f} W/kg x{req/134.4:.1f}; "
          f"f_thr(no feedback)={fthr:.3f} (x{fthr/f:.1f}); with feedback f'={fp:.3f}, "
          f"m'={mp*1e3:.3f} g, muscle mass x{fp*mp/(f*m0):.1f}")
for L in (54,63,86): print("Marden f_min", L, round(g/L,3), "x", round(g/L/f,1))
# 'most sensitive' check: elasticities of req wrt inputs
print("elasticities: m +0.5, R -1, M +1, f -1 (analytic from formula)")
# what forward-flight reduction would close generous case with proxy f
print("reduction needed generous:", round(134.4/(p_aero(m0,0.04)/(m0*f)),3))
