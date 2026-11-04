"""challenge-138 independent check. Every number printed is COMPUTED, not observed."""
import math
import numpy as np
g, m = 9.81, 0.4e-3
W = m * g
def EIreq(L, tol): return (W / 2) * L**2 / (8 * tol)

print("1. Independent arithmetic")
for name, L, tol, EI in [("lenient", .02, .5, 5e-9), ("central", .04, .1, 4e-9)]:
    S = EIreq(L, tol) / EI
    need = 1 - 1 / S
    print(f" {name}: EIreq={EIreq(L,tol):.4g} S={S:.2f} need_phi={need:.5f} "
          f"a/L*={need**.25:.5f} a*={need**.25*L*1e3:.3f} mm  point-load a/L*={need**(1/3):.5f}")
    for a in (200e-6, 300e-6):
        q = (a / L) ** 4
        nstar = 4 - math.log(need) / math.log(a / L)
        # step taper: distal segment has baseline EI lower by R; rigidify it
        Rstar = (S - 1) * (1 - q) / q
        print(f"   a={a*1e6:.0f}um a/L={a/L:.4f} phi=(a/L)^4={q:.3e} n*={nstar:.4f} "
              f"step-taper R*={Rstar:.3e} -> tip-segment EI must be <= {EI/Rstar:.2e} N m^2")

d = 2e-6
I1 = math.pi * d**4 / 64
print(f"\n single 2-um fibre: I={I1:.3e} m^4; EI at E0=0.35 GPa = {0.35e9*I1:.2e}; at 10 MPa = {1e7*I1:.2e}")

print("\n2. Large-deflection (elastica) check, uniform gravity load, uniform EI")
def elastica(L, EI, wtot, rigid_tip=0.0, N=4000):
    """Gravity-loaded inextensible cantilever (elastica), shot from the free TIP on theta(L).
    theta' = -M/EI (0 in the rigid distal segment), M' = -w (L-s) cos(theta);
    tip: M(L) = 0; root: theta(0) = 0. Integrated root-ward (stable), bisection on theta(L)
    in (-pi/2, 0). Returns the root-to-tip vertical drop."""
    w = wtot / L
    ds = L / N
    def shoot(th_tip):
        th, M, y, s = th_tip, 0.0, 0.0, L
        for _ in range(N):  # midpoint (RK2), stepping from s = L down to 0
            k = 0.0 if s > L - rigid_tip else 1.0
            thm = th + 0.5 * ds * k * M / EI
            Mm = M + 0.5 * ds * w * (L - s) * math.cos(th)
            sm = s - 0.5 * ds
            km = 0.0 if sm > L - rigid_tip else 1.0
            y += ds * math.sin(thm)          # y(L) - y(s)
            th += ds * km * Mm / EI
            M += ds * w * (L - sm) * math.cos(thm)
            s -= ds
        return th, y                          # theta(0), y(L) - y(0)
    # theta(L) = -pi/2 + eps. Heavy loads put the physical root at eps << 1, so scan eps on a
    # log grid and take the first sign change of theta(0); then bisect in log(eps).
    f = lambda le: shoot(-math.pi / 2 + math.exp(le))[0]
    grid = np.linspace(math.log(1e-14), math.log(math.pi / 2), 300)
    vals = [f(g0) for g0 in grid]
    k0 = next(i for i in range(1, len(grid)) if vals[i - 1] < 0 <= vals[i])
    lo, hi = grid[k0 - 1], grid[k0]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    th0, y = shoot(-math.pi / 2 + math.exp(0.5 * (lo + hi)))
    return -y

# validation: small load must reproduce linear wL^4/(8EI)
dl = elastica(.02, 5e-9, 1e-6)
for a_ in (1.0, 8.0):
    dd = elastica(1.0, 1.0, a_)
    print(f" elastica at wL^3/EI={a_}: delta/L={dd:.4f} (linear {a_/8:.3f})")
print(f" validation small load: elastica {dl:.4e} m vs linear {1e-6*.02**3/(8*5e-9):.4e} m")
for name, L, tol, EI in [("lenient", .02, .5, 5e-9), ("central", .04, .1, 4e-9)]:
    wt = W / 2
    d0 = elastica(L, EI, wt)
    d3 = elastica(L, EI, wt, rigid_tip=300e-6)
    print(f" {name}: linear delta/L={wt*L**3/(8*EI)/L:.2f}; elastica delta/L={d0/L:.4f}; "
          f"rigid distal 300um delta/L={d3/L:.4f}; tolerance delta/L={tol}; "
          f"reduction={(d0-d3)*1e9:.2f} nm vs needed {(d0-tol*L)*1e3:.2f} mm")
    d30 = elastica(L, EI, wt, rigid_tip=3e-3)
    print(f"   rigid distal 3 mm (10x measured): delta/L={d30/L:.4f}")
