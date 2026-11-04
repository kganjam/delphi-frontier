"""S9-D-D: does root (clamp) compliance explain Puri et al. 2018's rising 'effective modulus'?

EVERY OUTPUT OF THIS SCRIPT IS A CALCULATION, NOT AN OBSERVATION.

Inputs and read-levels
----------------------
E_APP  Puri et al. 2018, J. Exp. Biol. 221:jeb171777, Supplementary Fig. S5C (intact fins, 5 fish).
       Full-text supplement (PDF from the Europe PMC supplementaryFiles endpoint). The values below are
       MY READINGS OFF THE PLOT at 300 dpi, about +-0.1 mm in L and +-0.15 MPa in E. They are not
       tabulated values from the authors.
I_RAYS Puri et al. 2018 Fig. S5B (summed ray-only I versus effective beam length). Also read off the
       plot by me, about +-0.01e-15 m^4.
Model  Puri computed EI_app = (F/y) * L^3 / 3 (clamped-free cantilever, their Eqn 3), with L measured
       from the foam-pad fixation point p0 (their Fig. S4), and E_eff = EI_app / I_rays(L).
       If the root is not rigid, the measured compliance is
           y/F = L^3/(3 E I) + L^2/k_rot + 1/k_trans
       so  E_app(L) = E_inf / (1 + a/L + b/L^3),  a = 3 E I / k_rot,  b = 3 E I / k_trans.
       Simplification (mine): I is treated as constant within each fish's fit range. Puri's own
       I_rays varies only 0.45-0.50e-15 m^4 over L = 1-3 mm, so this is a <=10% effect proximally.
"""
from math import log

# (L mm, E_app MPa) read off Fig. S5C, ordered by L
E_APP = {
    "fish13": [(2.0, 6.45), (2.3, 5.72), (2.8, 7.22), (3.3, 9.70), (3.8, 10.35), (5.0, 8.00)],
    "fish12": [(1.3, 3.82), (1.7, 5.65), (2.3, 8.80), (3.0, 9.60), (3.5, 8.50), (5.0, 7.07)],
    "fish5":  [(1.4, 3.00), (2.1, 5.72), (2.8, 8.55), (3.6, 10.00), (4.4, 10.95), (5.4, 9.85)],
    "fish4":  [(2.1, 6.58), (2.8, 7.65), (3.4, 7.20), (4.1, 7.38), (4.4, 7.10), (4.5, 7.00)],
    "fish11": [(1.7, 1.88), (2.3, 3.07), (2.9, 4.05), (3.5, 4.85), (4.25, 4.70), (4.7, 4.55)],
}
# (L mm, I_rays 1e-15 m^4) read off Fig. S5B
I_RAYS = [(1.0, .488), (1.5, .500), (2.0, .500), (2.5, .490), (3.0, .450), (3.5, .405),
          (4.0, .372), (4.5, .353), (5.0, .337), (5.5, .310), (6.0, .297), (6.5, .284)]


def I_at(L):
    for (l0, i0), (l1, i1) in zip(I_RAYS, I_RAYS[1:]):
        if l0 <= L <= l1:
            return (i0 + (i1 - i0) * (L - l0) / (l1 - l0)) * 1e-15
    return (I_RAYS[0][1] if L < 1 else I_RAYS[-1][1]) * 1e-15


def fit(pts, use_a, use_b, use_c=0):
    """Grid search over a (mm), b (mm^3), c (mm^2) >= 0; E_inf by closed-form least squares.
    a/L  : rotational root spring.   b/L^3 : translational root spring.
    c/L^2: shear (Timoshenko / soft-core sandwich) deflection, y_s = F L / (kappa G A)."""
    best = None
    a_grid = [i * 0.02 for i in range(0, 401)] if use_a else [0.0]   # 0..8 mm  (8 = grid edge)
    b_grid = [i * 0.1 for i in range(0, 801)] if use_b else [0.0]    # 0..80 mm^3
    if use_c:
        a_grid, b_grid = [0.0], [0.0]
    c_grid = [i * 0.02 for i in range(0, 1001)] if use_c else [0.0]  # 0..20 mm^2
    for a in a_grid:
        for b in b_grid:
          for c in c_grid:
            g = [1 / (1 + a / L + b / L**3 + c / L**2) for L, _ in pts]
            Einf = sum(gi * y for gi, (_, y) in zip(g, pts)) / sum(gi * gi for gi in g)
            sse = sum((y - Einf * gi) ** 2 for gi, (_, y) in zip(g, pts))
            if best is None or sse < best[0]:
                best = (sse, a, b if not use_c else c, Einf)
    return best


def rising(pts):
    k = max(range(len(pts)), key=lambda i: pts[i][1])
    return pts[: k + 1]


print("=" * 100)
print("1. Sensitivity of EI_app to the clamp origin: EI_true/EI_app if the effective clamp lies")
print("   delta mm proximal of p0 (pure geometric offset, rigid otherwise)  [calc]")
for L in (1.3, 2.0, 3.0, 5.0):
    print(f"   L={L:3.1f} mm: " + "  ".join(f"d={d:.2f}->{((L + d) / L) ** 3:5.2f}x" for d in (0.25, 0.5, 1.0)))
for L in (1.3, 3.0, 5.0):
    print(f"   offset that doubles EI at L={L} mm: {L * (2 ** (1 / 3) - 1):.2f} mm")

print("=" * 100)
print("2. Can a rotational root spring alone explain the rise?  Max possible E_app ratio between two")
print("   spans under a pure hinge is L2/L1 (limit a -> inf).  Observed ratio vs that ceiling  [calc]")
for f, pts in E_APP.items():
    r = rising(pts)
    (L1, E1), (L2, E2) = r[0], r[-1]
    print(f"   {f}: E {E1:.2f}->{E2:.2f} MPa over L {L1}->{L2} mm: observed x{E2 / E1:.2f}, "
          f"hinge ceiling x{L2 / L1:.2f}  -> {'EXCEEDS' if E2 / E1 > L2 / L1 else 'within'}")

print("=" * 100)
print("3. Fits on the rising limb (points up to each fish's maximum)  [calc]")
print("   (for model 'shear' the b column holds c in mm^2; a = 8.00 means the fit ran into the grid edge,")
print("    i.e. the parameter is unconstrained, not estimated)")
print(f"   {'fish':7s} {'model':6s} {'n':>2s} {'a mm':>6s} {'b mm3':>6s} {'E_inf MPa':>9s} {'rmse':>6s}"
      f" {'E_inf/E_peak':>12s} {'E_inf/E_first':>13s}")
summary = {}
for f, pts in E_APP.items():
    r = rising(pts)
    Epk = r[-1][1]
    for name, ua, ub, uc in (("const", 0, 0, 0), ("rot", 1, 0, 0), ("trans", 0, 1, 0),
                             ("both", 1, 1, 0), ("shear", 0, 0, 1)):
        sse, a, b, Einf = fit(r, ua, ub, uc)
        rmse = (sse / len(r)) ** 0.5
        print(f"   {f:7s} {name:6s} {len(r):2d} {a:6.2f} {b:6.1f} {Einf:9.2f} {rmse:6.2f}"
              f" {Einf / Epk:12.2f} {Einf / r[0][1]:13.2f}")
        summary[(f, name)] = (a, b, Einf, rmse)

print("=" * 100)
print("4. What whole-fin EI does each reading imply?  [calc]")
print("   Puri's reported EI_app range (abstract): 1.5e-9 .. 4e-9 N m^2 (full-text).")
rows = []
shear_rows = []
for f, pts in E_APP.items():
    a, b, Einf, _ = summary[(f, "trans")]
    a2, b2, Einf2, _ = summary[(f, "both")]
    # corrected EI at the proximal-most measured span, and the max over measured spans
    EIc = [Einf * 1e6 * I_at(L) for L, _ in pts]
    EIc2 = [Einf2 * 1e6 * I_at(L) for L, _ in pts]
    _, _, c3, Einf3 = summary[(f, "shear")][0], 0, 0, summary[(f, "shear")][2]
    EIc3 = [Einf3 * 1e6 * I_at(L) for L, _ in pts]
    shear_rows.append((min(EIc3), max(EIc3)))
    EIapp = [E * 1e6 * I_at(L) for L, E in pts]
    rows.append((f, min(EIapp), max(EIapp), min(EIc), max(EIc), max(EIc2)))
    print(f"   {f:7s} EI_app {min(EIapp):.2e}..{max(EIapp):.2e}   corrected(trans) "
          f"{min(EIc):.2e}..{max(EIc):.2e}   max corrected(both) {max(EIc2):.2e} N m^2")
lo_app = min(r[1] for r in rows); hi_app = max(r[2] for r in rows)
lo_c = min(r[3] for r in rows); hi_c = max(r[4] for r in rows); hi_c2 = max(r[5] for r in rows)
print(f"   ALL: EI_app {lo_app:.2e}..{hi_app:.2e};  corrected(trans) {lo_c:.2e}..{hi_c:.2e};"
      f"  corrected(both) max {hi_c2:.2e}")
hi_s = max(r[1] for r in shear_rows); lo_s = min(r[0] for r in shear_rows)
print(f"   corrected(shear) {lo_s:.2e}..{hi_s:.2e}")
print(f"   Upper-end shift, corrected(shear)/reported-4e-9: x{hi_s / 4e-9:.2f}")
print(f"   Upper-end shift, corrected/reported-4e-9: trans x{hi_c / 4e-9:.2f}, both x{hi_c2 / 4e-9:.2f}")

print("=" * 100)
print("5. Implied root stiffness (trans model), k_trans = 3 E_inf I / b  [calc]")
for f in E_APP:
    a, b, Einf, _ = summary[(f, "trans")]
    I = I_at(1.5)
    if b > 0:
        k = 3 * Einf * 1e6 * I / (b * 1e-9)
        print(f"   {f}: b={b:.1f} mm^3 -> k_trans ~ {k:.2f} N/m  (cf. measured F/y at L~1.3-1.7 mm: ~0.6-2.5 N/m)")

print("=" * 100)
print("6. Propagate into S9-D's derived ray modulus (uncoupled flat-plate bound, EI_fin / 16 rays, w=150 um)")
EI_bone_ceiling = 25e9
for t in (11e-6, 15e-6, 16.5e-6):
    I_fp = 2 * 150e-6 * t**3 / 12
    for lab, EIfin in (("reported max 4e-9", 4e-9), ("corrected max", hi_c), ("corrected max (shear)", hi_s),
                       ("corrected max (both)", hi_c2)):
        E = EIfin / 16 / I_fp
        print(f"   t={t * 1e6:4.1f} um  {lab:22s} EI_fin={EIfin:.2e} -> per-ray E <= {E / 1e9:5.2f} GPa"
              f"{'  (> 25 GPa bone ceiling)' if E > EI_bone_ceiling else ''}")
