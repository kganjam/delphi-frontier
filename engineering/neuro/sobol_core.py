"""Shared Saltelli/Sobol routines (moved unchanged from sobol_m1.py so jobs can ship them without the M1 model)."""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import qmc


def indices(fA, fB, fAB, rng, nboot=300):
    N, d = fAB.shape
    def est(idx):
        a, b, ab = fA[idx], fB[idx], fAB[idx]
        V = np.var(np.r_[a, b])
        S1 = np.mean(b[:, None] * (ab - a[:, None]), axis=0) / V
        ST = 0.5 * np.mean((a[:, None] - ab) ** 2, axis=0) / V
        return S1, ST, V
    S1, ST, V = est(np.arange(N))
    bs = [est(rng.integers(0, N, N)) for _ in range(nboot)]
    S1b = np.array([b[0] for b in bs]); STb = np.array([b[1] for b in bs])
    return {"S1": S1, "ST": ST, "S1_ci95": np.percentile(S1b, [2.5, 97.5], axis=0).T, "ST_ci95": np.percentile(STb, [2.5, 97.5], axis=0).T, "var": V}


def saltelli(N, d, seed):
    X = qmc.Sobol(d=2 * d, scramble=True, seed=seed).random(N)
    A, B = X[:, :d], X[:, d:]
    AB = np.repeat(A[None], d, axis=0)
    for j in range(d):
        AB[j, :, j] = B[:, j]
    return A, B, AB


def ishigami_control(seed):
    a, b = 7.0, 0.1
    f = lambda X: np.sin(X[:, 0]) + a * np.sin(X[:, 1]) ** 2 + b * X[:, 2] ** 4 * np.sin(X[:, 0])
    A, B, AB = saltelli(8192, 3, seed); sc = lambda Z: -math.pi + 2 * math.pi * Z
    fA, fB = f(sc(A)), f(sc(B)); fAB = np.stack([f(sc(AB[j])) for j in range(3)], 1)
    r = indices(fA, fB, fAB, np.random.default_rng(seed), nboot=50)
    V = a * a / 8 + b * math.pi ** 4 / 5 + b * b * math.pi ** 8 / 18 + 0.5
    V1 = 0.5 * (1 + b * math.pi ** 4 / 5) ** 2; V2 = a * a / 8; V13 = b * b * math.pi ** 8 * (1 / 18 - 1 / 50)
    exact_S1 = [V1 / V, V2 / V, 0.0]; exact_ST = [(V1 + V13) / V, V2 / V, V13 / V]
    ok = bool(np.all(np.abs(r["S1"] - exact_S1) < 0.03) and np.all(np.abs(r["ST"] - exact_ST) < 0.03))
    return {"name": "control: Ishigami S1/ST within 0.03 of analytic (N 8192)", "pass": ok, "detail": {"S1": r["S1"].tolist(), "exact_S1": exact_S1, "ST": r["ST"].tolist(), "exact_ST": exact_ST}}
