"""Shared machinery: gait phase patterns, a quasi-static elastic voxel lattice,
and its analytic positive controls.

Scope: this is OUR reimplementation of the ACTUATION LAW used by the
delphi-frontier voxel-actuation artifact, in a form that can be posed as a
free-floating (no gravity, no floor) quasi-static elasticity problem. It is NOT
Voxelyze. Voxelyze is used unmodified, at its pin, for the dry-friction arms.

The actuation law reproduced here, read from the artifact's protocol.json:
    zero-stress voxel size   baseSize_i = s * (1 + alphaCTE * T_i)
    imposed temperature      T_i(t)     = A * sin(2*pi*f*t + phi_i)
phi_i per the named pattern, copied byte-for-byte in intent from
scripts/voxel_actuation/soft_actuation.cpp::phaseFor.
"""
import numpy as np

PI = np.pi

# ---------------------------------------------------------------- gaits ----
GAITS = ("uniform", "longitudinal", "lateral", "dorsoventral", "travelling", "checker")


def phase_for(pattern, x, y, z, nx, ny, nz):
    """Transcribed from soft_actuation.cpp::phaseFor at the pinned commit."""
    if pattern == "uniform":
        return 0.0
    if pattern == "longitudinal":
        return 0.0 if x < nx // 2 else PI
    if pattern == "lateral":
        return 0.0 if y < ny // 2 else PI
    if pattern == "dorsoventral":
        return 0.0 if z < nz // 2 else PI
    if pattern == "travelling":
        return 2.0 * PI * x / nx
    if pattern == "checker":
        return PI if (x + y + z) % 2 else 0.0
    raise ValueError(pattern)


def lattice_index(nx, ny, nz):
    """Voxel (x,y,z) integer coordinates in the driver's own loop order."""
    return np.array([(x, y, z) for x in range(nx) for y in range(ny) for z in range(nz)],
                    dtype=float)


def phase_vector(pattern, nx, ny, nz):
    idx = lattice_index(nx, ny, nz)
    return np.array([phase_for(pattern, int(x), int(y), int(z), nx, ny, nz)
                     for x, y, z in idx])


# ------------------------------------------------- reciprocity (exact) -----
def reciprocity(phi, tol=1e-12):
    """Is T_i(t) = A sin(wt + phi_i) a TIME-RECIPROCAL control sequence?

    T(t) = sin(wt) * u + cos(wt) * v,  u_i = cos(phi_i),  v_i = sin(phi_i).
    The control trajectory is a closed curve in R^N lying in span{u, v}. It is a
    degenerate curve -- a segment retraced forwards then backwards, i.e. time
    reciprocal -- exactly when rank([u; v]) <= 1. Otherwise it is a
    non-degenerate ellipse enclosing non-zero area and is non-reciprocal.

    This is a statement about the CONTROL. It transfers to the SHAPE only if the
    shape responds quasi-statically; see quasistatic_margin().
    """
    u, v = np.cos(phi), np.sin(phi)
    M = np.vstack([u, v])
    sv = np.linalg.svd(M, compute_uv=False)
    smax = sv[0] if sv[0] > 0 else 1.0
    rank = int(np.sum(sv > tol * max(1.0, smax) * len(phi)))
    # signed area of the ellipse the control traces, normalised by N:
    #   area = pi * |u x v| summed over the 2-planes = pi * sqrt(det(M M^T))
    G = M @ M.T
    det = G[0, 0] * G[1, 1] - G[0, 1] * G[1, 0]
    area = PI * np.sqrt(max(det, 0.0)) / len(phi)
    return {"rank": rank, "reciprocal": bool(rank <= 1),
            "enclosed_area_per_voxel": float(area),
            "singular_values": [float(s) for s in sv]}


# ------------------------------------------------------ elastic lattice ----
class VoxelLattice:
    """Free-floating quasi-static central-force spring lattice on a simple cubic
    grid: nearest-neighbour springs plus face-diagonal springs (the latter are
    what make the lattice shear-stable; a nearest-neighbour-only cubic lattice is
    a mechanism and has zero shear modulus).

    DECLARED DIFFERENCE FROM VOXELYZE. A central-force lattice obeys the Cauchy
    relations, so its Poisson ratio is fixed by the spring topology and cannot be
    set to the artifact's nu = 0.35 independently of E. The measured nu of this
    lattice is reported by calibrate(), not assumed. Voxelyze instead uses
    Euler-Bernoulli link elements with independent axial, bending and torsion
    terms. This lattice is used ONLY to produce a deformed SHAPE for the Stokes
    solve; no Voxelyze number is reproduced from it and none is claimed.
    """

    def __init__(self, nx, ny, nz, s=0.01, E=1e5, k2_ratio=0.5, cte=0.01):
        self.nx, self.ny, self.nz, self.s, self.cte = nx, ny, nz, s, cte
        self.idx = lattice_index(nx, ny, nz)
        self.X0 = self.idx * s
        self.N = len(self.idx)
        key = {tuple(int(q) for q in r): i for i, r in enumerate(self.idx)}
        bonds, kind = [], []
        offs1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        offs2 = [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]
        for r, i in key.items():
            for o, k in [(o, 1) for o in offs1] + [(o, 2) for o in offs2]:
                q = (r[0] + o[0], r[1] + o[1], r[2] + o[2])
                j = key.get(q)
                if j is not None:
                    bonds.append((i, j))
                    kind.append(k)
        self.bonds = np.array(bonds, dtype=int)
        self.kind = np.array(kind, dtype=int)
        # spring constants: k1 = E*s (the axial term Voxelyze uses, EA/L with
        # A=s^2, L=s), k2 scaled by k2_ratio. The resulting continuum E is
        # MEASURED by calibrate(), not assumed to equal E.
        self.k1 = E * s
        self.k2 = k2_ratio * E * s
        self.k = np.where(self.kind == 1, self.k1, self.k2)
        self.rest_mult = np.where(self.kind == 1, 1.0, np.sqrt(2.0))
        self.E_nominal = E

    def base_size(self, T):
        return self.s * (1.0 + self.cte * T)

    def rest_lengths(self, T):
        b = self.base_size(T)
        i, j = self.bonds[:, 0], self.bonds[:, 1]
        return 0.5 * (b[i] + b[j]) * self.rest_mult

    def energy_grad(self, X, L0):
        i, j = self.bonds[:, 0], self.bonds[:, 1]
        d = X[j] - X[i]
        L = np.linalg.norm(d, axis=1)
        L = np.maximum(L, 1e-15)
        dL = L - L0
        U = 0.5 * np.sum(self.k * dL ** 2)
        f = (self.k * dL / L)[:, None] * d           # force on i, -on j
        G = np.zeros_like(X)
        np.add.at(G, i, -f)
        np.add.at(G, j, f)
        return U, G

    def relax(self, T, X_init=None, tol=1e-12, maxit=4000):
        """Minimise elastic energy, free-floating. Gauge (translation+rotation)
        is left unfixed; the gradient has no component along the zero modes, and
        the caller removes rigid motion afterwards."""
        from scipy.optimize import minimize
        L0 = self.rest_lengths(np.asarray(T, float))
        X = (self.X0.copy() if X_init is None else X_init.copy()).ravel()

        def fun(v):
            U, G = self.energy_grad(v.reshape(-1, 3), L0)
            return U, G.ravel()

        res = minimize(fun, X, jac=True, method="L-BFGS-B",
                       options={"maxiter": maxit, "ftol": tol, "gtol": tol})
        return res.x.reshape(-1, 3), res


# --------------------------------------------- analytic positive controls --
def control_free_expansion(nx=5, ny=3, nz=3, s=0.01, E=1e5, cte=0.01, T=10.0):
    """P1-analogue. A free, unloaded block at uniform temperature T must take the
    rest length exactly: span = (n-1) * s * (1 + cte*T). Closed form, exact."""
    lat = VoxelLattice(nx, ny, nz, s=s, E=E, cte=cte)
    X, res = lat.relax(np.full(lat.N, T))
    span = X[:, 0].max() - X[:, 0].min()
    predicted = (nx - 1) * s * (1.0 + cte * T)
    return {"measured_span_m": float(span), "closed_form_m": float(predicted),
            "ratio": float(span / predicted), "converged": bool(res.success),
            "final_grad_inf": float(np.max(np.abs(res.jac)))}


def control_cantilever(n=10, s=0.01, E=1e5, k2_ratio=0.5, F=1e-4):
    """P2-analogue. End-loaded cantilever against delta = F L^3 / (3 E I).

    This control does double duty: it both TESTS the lattice's bending response
    and CALIBRATES it, because the effective continuum E of a spring lattice is a
    property of the spring constants and not an input. We therefore report the
    EFFECTIVE E back-solved from the closed form, and the ratio to the nominal E.
    A ratio far from 1 is a real, reported property of this lattice, not a
    failure to be tuned away: the Stokes study uses the lattice only for SHAPE.
    """
    lat = VoxelLattice(n, 3, 3, s=s, E=E, k2_ratio=k2_ratio)
    L0 = lat.rest_lengths(np.zeros(lat.N))
    X = lat.X0.copy()
    clamp = np.where(lat.idx[:, 0] <= 1)[0]          # two end planes clamped
    tip = np.where(lat.idx[:, 0] == n - 1)[0]
    from scipy.optimize import minimize
    free = np.setdiff1d(np.arange(lat.N), clamp)
    Fvec = np.zeros_like(X)
    Fvec[tip, 2] = -F / len(tip)

    def fun(v):
        Y = X.copy()
        Y[free] = v.reshape(-1, 3)
        U, G = lat.energy_grad(Y, L0)
        U -= np.sum(Fvec * Y)
        G -= Fvec
        return U, G[free].ravel()

    res = minimize(fun, X[free].ravel(), jac=True, method="L-BFGS-B",
                   options={"maxiter": 20000, "ftol": 1e-16, "gtol": 1e-14})
    Y = X.copy()
    Y[free] = res.x.reshape(-1, 3)
    delta = float(np.mean(X[tip, 2] - Y[tip, 2]))
    Lb = (n - 1 - 1) * s                              # free length from clamp
    I = (3 * s) ** 4 / 12.0
    E_eff = F * Lb ** 3 / (3.0 * I * delta) if delta > 0 else float("nan")
    return {"n": n, "tip_deflection_m": delta, "free_length_m": Lb,
            "second_moment_m4": I, "E_effective_Pa": float(E_eff),
            "E_nominal_Pa": E, "E_eff_over_E_nominal": float(E_eff / E),
            "converged": bool(res.success)}


def calibrate_uniaxial(n=8, s=0.01, E=1e5, k2_ratio=0.5, strain=1e-3):
    """Measure the lattice's effective Young's modulus and Poisson ratio by a
    numerical uniaxial tension test. Reported, not assumed."""
    lat = VoxelLattice(n, n, n, s=s, E=E, k2_ratio=k2_ratio)
    L0 = lat.rest_lengths(np.zeros(lat.N))
    X = lat.X0.copy()
    xmax = (n - 1) * s
    lo = np.where(lat.idx[:, 0] == 0)[0]
    hi = np.where(lat.idx[:, 0] == n - 1)[0]
    held = np.concatenate([lo, hi])
    free = np.setdiff1d(np.arange(lat.N), held)
    Y0 = X.copy()
    Y0[hi, 0] += strain * xmax
    from scipy.optimize import minimize

    def fun(v):
        Y = Y0.copy()
        Y[free] = v.reshape(-1, 3)
        U, G = lat.energy_grad(Y, L0)
        return U, G[free].ravel()

    res = minimize(fun, Y0[free].ravel(), jac=True, method="L-BFGS-B",
                   options={"maxiter": 20000, "ftol": 1e-18, "gtol": 1e-16})
    Y = Y0.copy()
    Y[free] = res.x.reshape(-1, 3)
    _, G = lat.energy_grad(Y, L0)
    Fx = float(np.sum(G[hi, 0]))                      # reaction at the held face
    area = ((n - 1) * s) ** 2
    E_eff = abs(Fx) / area / strain
    mid = np.where(np.abs(lat.idx[:, 0] - (n - 1) / 2) < 0.51)[0]
    wy0 = Y0[mid, 1].max() - Y0[mid, 1].min()
    wy = Y[mid, 1].max() - Y[mid, 1].min()
    nu_eff = -((wy - wy0) / wy0) / strain
    return {"E_effective_Pa": float(E_eff), "E_nominal_Pa": E,
            "E_eff_over_E_nominal": float(E_eff / E), "nu_effective": float(nu_eff),
            "applied_strain": strain, "converged": bool(res.success)}
