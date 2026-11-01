#!/usr/bin/env python3
"""F001 controls: witnesses that separate total fitness variance Var(w) from
additive genetic variance V_A(w), and check the partial-change identity
Delta_NS wbar = V_A(w)/wbar exactly (rational arithmetic, no floats).

Definitions (see target-spec-v0.md, sections 2-4):
  types i with frequencies q_i (sum 1), fitness w_i >= 0, wbar = sum q_i w_i > 0
  gene-count predictors x_ij (copies of allele j in type i)
  additive genetic value g_i = a + sum_j b_j x_ij, (a, b) the q-weighted least
    squares fit of w on x (intercept included)            -> V_A = Var_q(g)
  selected frequencies q*_i = q_i w_i / wbar
  partial change  Delta_NS wbar = sum_i (q*_i - q_i) g_i  (b held fixed)
  Price total-variance term (Price.lean fitness_selection) = Var_q(w)/wbar

Each witness prints these, plus (diploid one-locus cases) the TOTAL change in
mean fitness after random union of gametes, which is a different quantity.

Run: python3 -I variance_witness.py     (stdlib only; deterministic)
"""
from fractions import Fraction as F


def mean(q, x):
    return sum(qi * xi for qi, xi in zip(q, x))


def var(q, x):
    m = mean(q, x)
    return sum(qi * (xi - m) ** 2 for qi, xi in zip(q, x))


def solve(A, y):
    """Exact Gaussian elimination; returns one solution (free vars = 0)."""
    n = len(A)
    M = [row[:] + [yi] for row, yi in zip(A, y)]
    piv_cols, r = [], 0
    for c in range(n):
        p = next((k for k in range(r, n) if M[k][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for k in range(n):
            if k != r and M[k][c] != 0:
                f = M[k][c]
                M[k] = [vk - f * vr for vk, vr in zip(M[k], M[r])]
        piv_cols.append(c)
        r += 1
    sol = [F(0)] * n
    for i, c in enumerate(piv_cols):
        sol[c] = M[i][n]
    return sol


def additive_values(q, w, X):
    """q-weighted least squares of w on [1, X]; returns fitted g_i."""
    D = [[F(1)] + list(row) for row in X]
    k = len(D[0])
    A = [[sum(q[i] * D[i][r] * D[i][c] for i in range(len(q))) for c in range(k)]
         for r in range(k)]
    y = [sum(q[i] * D[i][r] * w[i] for i in range(len(q))) for r in range(k)]
    beta = solve(A, y)
    g = [sum(bc * dc for bc, dc in zip(beta, row)) for row in D]
    return beta, g


def report(name, q, w, X, total=None):
    assert sum(q) == 1 and all(v >= 0 for v in q) and all(v >= 0 for v in w)
    wbar = mean(q, w)
    beta, g = additive_values(q, w, X)
    resid = [wi - gi for wi, gi in zip(w, g)]
    # least-squares normal equations: residual orthogonal to 1 and to each x_j
    assert mean(q, resid) == 0
    for j in range(len(X[0])):
        assert mean(q, [r * row[j] for r, row in zip(resid, X)]) == 0
    VA, Vw = var(q, g), var(q, w)
    qs = [qi * wi / wbar for qi, wi in zip(q, w)]
    dNS = sum((a - b) * gi for a, b, gi in zip(qs, q, g))
    # same partial change via gene counts: sum_j b_j * Delta E[x_j]
    dNS2 = sum(beta[1 + j] * (mean(qs, [r[j] for r in X]) - mean(q, [r[j] for r in X]))
               for j in range(len(X[0])))
    assert dNS == dNS2 == VA / wbar
    print(f"== {name}")
    print(f"   wbar = {wbar}  ({float(wbar):.6f})")
    print(f"   Var(w) total = {Vw}  ({float(Vw):.6f})")
    print(f"   V_A(w)       = {VA}  ({float(VA):.6f})")
    print(f"   Var(w) - V_A = {Vw - VA}  ({float(Vw - VA):.6f})  [non-additive part]")
    print(f"   average effects b = {[str(b) for b in beta[1:]]}")
    print(f"   partial change Delta_NS wbar = {dNS}  ({float(dNS):.6f})  == V_A/wbar: {dNS == VA / wbar}")
    print(f"   Price total-variance term Var(w)/wbar = {Vw / wbar}  ({float(Vw / wbar):.6f})")
    if total is not None:
        print(f"   total change in wbar after one generation = {total}  ({float(total):.6f})")
    return dict(wbar=wbar, Vw=Vw, VA=VA, dNS=dNS, total=total)


def diploid_one_locus(p, w11, w12, w22):
    q = [p * p, 2 * p * (1 - p), (1 - p) ** 2]          # HW genotype frequencies
    w = [w11, w12, w22]
    X = [[F(2)], [F(1)], [F(0)]]                         # copies of allele A1
    wbar = mean(q, w)
    p_next = (p * p * w11 + p * (1 - p) * w12) / wbar    # fair meiosis, random union
    wbar_next = mean([p_next ** 2, 2 * p_next * (1 - p_next), (1 - p_next) ** 2], w)
    return q, w, X, wbar_next - wbar


if __name__ == "__main__":
    out = {}
    # W1: one-locus diploid, complete dominance of A1 (fitness 1,1,1/2), p=1/2.
    q, w, X, tot = diploid_one_locus(F(1, 2), F(1), F(1), F(1, 2))
    out["W1"] = report("W1 diploid 1 locus, complete dominance, p=1/2", q, w, X, tot)
    # W2: overdominance at the internal equilibrium: V_A = 0 but Var(w) > 0.
    # w11=1-s, w12=1, w22=1-t, equilibrium p* = t/(s+t); s=1/5, t=2/5 -> p*=2/3.
    q, w, X, tot = diploid_one_locus(F(2, 3), F(4, 5), F(1), F(3, 5))
    out["W2"] = report("W2 diploid 1 locus, overdominance at equilibrium p*=2/3", q, w, X, tot)
    # W3: two-locus haploid, pure (multiplicative-free) epistasis, no LD:
    # fitness 1 + e*[AB] with e = 1, equal allele frequencies 1/2.
    q = [F(1, 4)] * 4                                     # AB, Ab, aB, ab
    X = [[F(1), F(1)], [F(1), F(0)], [F(0), F(1)], [F(0), F(0)]]
    w = [F(2), F(1), F(1), F(1)]
    out["W3"] = report("W3 haploid 2 loci, AxB epistasis, linkage equilibrium", q, w, X)
    # C1 (control, agreement expected): diploid 1 locus, no dominance.
    q, w, X, tot = diploid_one_locus(F(1, 3), F(3, 2), F(5, 4), F(1))
    out["C1"] = report("C1 diploid 1 locus, additive (no dominance), p=1/3", q, w, X, tot)
    # C2 (control): haploid 1 locus, two alleles: regression is saturated, V_A = Var(w).
    q = [F(1, 3), F(2, 3)]
    out["C2"] = report("C2 haploid 1 locus (saturated regression)", q, [F(3, 2), F(1)], [[F(1)], [F(0)]])

    print("\nSummary checks:")
    print("  W1 Var(w) != V_A:", out["W1"]["Vw"] != out["W1"]["VA"],
          "; total change != V_A/wbar:", out["W1"]["total"] != out["W1"]["dNS"])
    print("  W2 V_A == 0 and Var(w) > 0:", out["W2"]["VA"] == 0 and out["W2"]["Vw"] > 0)
    print("  W3 Var(w) != V_A:", out["W3"]["Vw"] != out["W3"]["VA"])
    print("  C1 Var(w) == V_A and total == partial:", out["C1"]["Vw"] == out["C1"]["VA"],
          out["C1"]["total"] == out["C1"]["dNS"])
    print("  C2 Var(w) == V_A:", out["C2"]["Vw"] == out["C2"]["VA"])
