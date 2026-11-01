"""Independent linear calculation for the F003 alignment (does NOT import scopedesk.oracles.linear).
Closed-form Jacobians at the homogeneous steady state, Du = 1, gamma = 1, Neumann modes q_n = (n pi / L)^2.
Evidence kind: computed (linear algebra on declared equations). See PREREG.md."""
from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np
from scipy.linalg import expm


def steady(model, p):
    if model == "schnakenberg":
        a, b = float(F(p["a"])), float(F(p["b"]))
        return a + b, b / (a + b) ** 2
    A, B = float(F(p["A"])), float(F(p["B"]))
    return A, B / A


def jacobian(model, p):
    """Analytic Jacobian at the steady state (derived by hand, see docstring of PREREG)."""
    if model == "schnakenberg":
        a, b = float(F(p["a"])), float(F(p["b"]))
        s = a + b
        return np.array([[-1 + 2 * b / s, s * s], [-2 * b / s, -s * s]])
    A, B = float(F(p["A"])), float(F(p["B"]))
    return np.array([[B - 1, A * A], [-B, -A * A]])


def sigma(J, Dv, q):
    """max Re eigenvalue of J - q diag(1, Dv) for an array q, closed form."""
    tr = J[0, 0] + J[1, 1] - q * (1 + Dv)
    det = (J[0, 0] - q) * (J[1, 1] - Dv * q) - J[0, 1] * J[1, 0]
    disc = tr * tr / 4 - det
    return np.where(disc >= 0, tr / 2 + np.sqrt(np.abs(disc)), tr / 2)


def spectral_q(L, nmax):
    n = np.arange(1, nmax + 1)
    return n, (n * math.pi / L) ** 2


def fd_q(L, NB):
    """Discrete Neumann Laplacian eigenvalues of the cell-centred 3-point stencil (solver B), modes 1..NB-1."""
    n = np.arange(1, NB)
    h = L / NB
    return n, (2.0 / h * np.sin(n * math.pi / (2 * NB))) ** 2


def linear_summary(model, p, Dv, L, NA, NB):
    J = jacobian(model, p)
    Dv = float(F(Dv))
    n, q = spectral_q(L, NA - 1)
    s = sigma(J, Dv, q)
    # cross-check closed form vs numpy eigvals on every mode
    s_np = np.array([np.linalg.eigvals(J - qq * np.diag([1.0, Dv])).real.max() for qq in q])
    unstable = [int(k) for k in n[s > 0]]
    i = int(np.argmax(s))
    nb, qb = fd_q(L, NB)
    sb = sigma(J, Dv, qb)
    # continuum band check: is any q beyond the grid's last mode unstable? (should not happen)
    qhi = np.linspace(q[-1], q[-1] * 4 + 10, 2000)
    tail_unstable = bool((sigma(J, Dv, qhi) > 0).any())
    return {"wellmixed_stable": bool(np.trace(J) < 0 and np.linalg.det(J) > 0),
            "verdict": "applies" if unstable else "out_of_scope",
            "unstable_modes": unstable, "n_unstable": len(unstable),
            "fastest_mode": int(n[i]) if unstable else None, "sigma_fast": float(s[i]) if unstable else 0.0,
            "closed_form_vs_eigvals_maxabs": float(np.abs(s - s_np).max()),
            "unstable_modes_B": [int(k) for k in nb[sb > 0]],
            "fastest_mode_B": int(nb[int(np.argmax(sb))]) if (sb > 0).any() else None,
            "tail_unstable_beyond_grid": tail_unstable}


def l3_prediction(model, p, Dv, L, w0u, w0v, t):
    """Exact linear evolution of each DCT mode n>=1 from initial coefficients (w0u[n], w0v[n]) to time t.
    Returns |w_{n,u}(t)| for n = 0..N-1 (index 0 set to 0)."""
    J = jacobian(model, p)
    Dv = float(F(Dv))
    N = len(w0u)
    out = np.zeros(N)
    for k in range(1, N):
        q = (k * math.pi / L) ** 2
        w = expm((J - q * np.diag([1.0, Dv])) * t) @ np.array([w0u[k], w0v[k]])
        out[k] = abs(w[0])
    return out
