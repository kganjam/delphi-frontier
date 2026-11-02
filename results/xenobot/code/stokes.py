"""Stokes-regime (zero-Reynolds) bead-model swimmer.

Mobility: Rotne-Prager-Yamakawa for N equal spheres of radius a, including the
overlapping branch (needed here: neighbouring voxel centres are exactly 2a apart
at rest and come closer than 2a at peak contraction).

Swimmer solve. With the body shape x_i(t) prescribed in a body frame, the rigid
motion q = (V, Omega) is fixed by force-free and torque-free conditions:
    v_i = V + Omega x x_i + xdot_i,   F = R v,   R = M^-1
    B^T F = 0   (B maps q to rigid velocities; B^T is exactly sum F and sum x x F)
 => q = -(B^T R B)^-1 B^T R xdot

NOTE ON FREE DRAINING. If M were diagonal (no hydrodynamic interaction between
beads) this returns q = 0 identically for every gait: a free-draining body cannot
swim. Swimming at zero Reynolds number requires the hydrodynamic coupling that
the off-diagonal RPY blocks carry. That is physics, not an implementation detail,
and free_draining=True is retained as a must-fail arm.
"""
import numpy as np

MU_WATER_20C = 1.002e-3          # Pa s   (declared: assumed, see parameters list)


def rpy_mobility(X, a, mu, free_draining=False):
    N = len(X)
    M = np.zeros((3 * N, 3 * N))
    I3 = np.eye(3)
    self_m = 1.0 / (6 * np.pi * mu * a)
    for i in range(N):
        M[3 * i:3 * i + 3, 3 * i:3 * i + 3] = self_m * I3
    if free_draining:
        return M
    for i in range(N):
        for j in range(i + 1, N):
            d = X[j] - X[i]
            r = np.linalg.norm(d)
            if r < 1e-14:
                blk = self_m * I3
            else:
                rh = d / r
                rr = np.outer(rh, rh)
                if r >= 2 * a:
                    blk = (1.0 / (8 * np.pi * mu * r)) * (
                        (I3 + rr) + (2 * a * a / (3 * r * r)) * (I3 - 3 * rr))
                else:
                    blk = self_m * ((1 - 9 * r / (32 * a)) * I3 + (3 * r / (32 * a)) * rr)
            M[3 * i:3 * i + 3, 3 * j:3 * j + 3] = blk
            M[3 * j:3 * j + 3, 3 * i:3 * i + 3] = blk
    return M


def rigid_basis(X):
    """B: (3N, 6) mapping (V, Omega) to bead velocities V + Omega x x_i."""
    N = len(X)
    B = np.zeros((3 * N, 6))
    for i, x in enumerate(X):
        B[3 * i:3 * i + 3, 0:3] = np.eye(3)
        B[3 * i:3 * i + 3, 3:6] = np.array([[0, x[2], -x[1]],
                                            [-x[2], 0, x[0]],
                                            [x[1], -x[0], 0]])
    return B


def swim_step(X, Xdot, a, mu, free_draining=False):
    """Return (V, Omega) in the body frame for one instantaneous configuration."""
    M = rpy_mobility(X, a, mu, free_draining)
    R = np.linalg.inv(M)
    B = rigid_basis(X)
    A = B.T @ R @ B
    b = -(B.T @ R @ Xdot.ravel())
    # lstsq, not solve: a collinear bead set (the three-sphere control) has an
    # exact zero mode -- rotation about the common axis -- so B^T R B is rank 5.
    # The least-norm solution is the physically correct one: that rotation is
    # unresisted and unexcited. For a 3-D body the matrix is full rank and the
    # two agree to machine precision (asserted in the control suite).
    q, *_ = np.linalg.lstsq(A, b, rcond=1e-10)
    return q[0:3], q[3:6]


def kabsch(P, Q):
    """Rotation taking P onto Q (both already centroid-removed)."""
    H = P.T @ Q
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    return Vt.T @ D @ U.T


def integrate_cycle(shapes, dt, a, mu, free_draining=False):
    """shapes: (nt, N, 3) body-frame configurations sampled over one period,
    already centroid-removed and gauge-aligned. Returns the net lab-frame
    displacement of the body centroid over the sampled interval."""
    nt = len(shapes)
    Q = np.eye(3)
    pos = np.zeros(3)
    track = [pos.copy()]
    for t in range(nt):
        tp, tm = (t + 1) % nt, (t - 1) % nt
        Xdot = (shapes[tp] - shapes[tm]) / (2 * dt)
        V, Om = swim_step(shapes[t], Xdot, a, mu, free_draining)
        pos = pos + dt * (Q @ V)
        w = Q @ Om
        th = np.linalg.norm(w) * dt
        if th > 1e-15:
            k = w / np.linalg.norm(w)
            K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
            Q = (np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K) @ Q
        track.append(pos.copy())
    return pos, np.array(track)


def gauge_align(shapes):
    """Centroid-remove every frame and Kabsch-align each to its predecessor, so
    that xdot carries deformation only. This is a gauge choice; the net lab-frame
    displacement over a closed shape cycle does not depend on it."""
    out = []
    ref = None
    for X in shapes:
        Y = X - X.mean(axis=0)
        if ref is not None:
            Y = Y @ kabsch(Y, ref).T
        out.append(Y)
        ref = Y
    return np.array(out)


# -------------------------------------------------- analytic controls ------
def three_sphere(a, L, d1, d2, mu, nt=400):
    """Najafi-Golestanian three-sphere swimmer: three collinear beads, two arms
    opened and closed out of phase. Used as the solver's NON-ZERO positive
    control. We check the small-amplitude SCALING exponents, which are stated by
    the standard analysis (displacement per cycle proportional to a, to d1*d2 and
    to L^-2), rather than a remembered prefactor."""
    ts = np.arange(nt) / nt
    shapes = []
    for u in ts:
        s1 = L + d1 * np.sin(2 * np.pi * u)
        s2 = L + d2 * np.sin(2 * np.pi * u + np.pi / 2)
        x = np.array([[-s1, 0, 0], [0.0, 0, 0], [s2, 0, 0]])
        shapes.append(x - x.mean(axis=0))
    shapes = np.array(shapes)
    net, _ = integrate_cycle(shapes, 1.0 / nt, a, mu)
    return float(net[0])
