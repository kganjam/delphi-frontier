"""Challenge 171: independent recomputation of S10-D-D. All outputs are CALCULATIONS."""
import math
g, rho, k = 9.81, 1.2, 1.2
m, R, M = 0.4e-3, 0.04, 1.5
W = m * g
Pi = k * math.sqrt(W**3 / (2 * rho * math.pi * R**2))
body = M * Pi / m
print(f"P_ind={Pi*1e3:.3f} mW  M*P_ind/m={body:.2f} W/kg body")
groups = {"abd_sup": 0.13, "abd_prof": 0.23, "add_sup": 0.15, "add_prof": 0.18}  # % body/fin, Mansuit&Herrel T1
four = sum(groups.values())
pairs = [(a, b, groups[a] + groups[b]) for i, a in enumerate(groups) for b in list(groups)[i+1:]]
print(f"four-group sum {four:.2f}%/fin")
for a, b, s in sorted(pairs, key=lambda t: -t[2]):
    tot = 2 * s
    ok = "consistent" if tot >= four - 1e-9 else "IMPOSSIBLE (< four-group sum)"
    print(f"  if 'two largest'={a}+{b}: girdle total {tot:.2f}%/fin -> f={2*tot/100:.4f} [{ok}]")
print(f"author upper bracket: four-group sum = half -> {2*four:.2f}%/fin; implied two-largest share "
      f"= {(0.23+0.18)/(2*four):.0%} (source says 50%)")
for f in (0.0138, 0.0164, 0.0276):
    reqs = [M_ * k * math.sqrt(W**3/(2*rho*math.pi*R_**2)) / (m*f) for R_, M_ in ((0.04,1.5),(0.04,2),(0.02,1.5),(0.02,2))]
    print(f"f={f}: req {[round(x) for x in reqs]} W/kg; shortfall vs 134.4 x{reqs[0]/134.4:.2f}..x{reqs[-1]/134.4:.2f}"
          f"; fwd-flight 0.5 generous x{reqs[0]*0.5/134.4:.2f}")
for pm in (0.15, 0.21):
    print(f"Pmech {pm}: x{body/pm:.0f}; if the unmeasured other half of girdle muscle doubled it: x{body/(2*pm):.0f}")
print(f"m flip factor: {(134.4/(M*Pi/(m*0.0138)))**2:.3f}")
