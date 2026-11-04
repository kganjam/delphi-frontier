# Independent replication of claim 199 (S6 fin-ray load). Calculated, not observed.
import itertools
g = 9.81
m = 0.3648e-3            # kg, PLoS ONE 2011 table (adult males), search-summary read-level
W = m * g
EI_fin = (2e-9, 5e-9)    # N m^2, whole caudal fin, Puri et al. 2018 (JEB 221:jeb171777)
width  = (8e-3, 5e-3)    # m, fin width at those positions, same paper
e = (EI_fin[0]/width[0], EI_fin[1]/width[1])   # EI per unit width, N m
S = (0.5e-4, 1e-4, 2e-4) # m^2, total lifting area: ASSUMED bracket
L = (5e-3, 8e-3, 10e-3)  # m, cantilever span of fin: ASSUMED bracket
print(f"W = {W:.3e} N; EI per width = {e[0]:.2e} .. {e[1]:.2e} N m")
rows = []
for s, l, ee in itertools.product(S, L, e):
    p = W / s
    r = p * l**3 / (8 * ee)  # uniform-pressure cantilever strip: delta/L
    rows.append(r)
    print(f"S={s*1e4:.1f} cm2 p={p:5.1f} Pa L={l*1e3:4.1f} mm e={ee:.2e}  delta/L={r:7.2f}")
print("min", min(rows), "max", max(rows))
p, l = W/1e-4, 8e-3
print("central (S=1cm2,L=8mm, geometric-mean e):", p*l**3/(8*(e[0]*e[1])**0.5))
# Water comparison: dynamic pressure 0.5*rho*U^2
for U in (0.1, 0.2, 0.3):
    print(f"water q at U={U} m/s: {0.5*1000*U*U:.1f} Pa")
