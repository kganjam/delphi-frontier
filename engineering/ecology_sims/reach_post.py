"""Post-analysis of the saved default reachability landscape (landscape_default.npz): is mass the only trait that forces a dip?

  (a) maximin single-trait path to the target cell (as in reachability.py, recomputed as a check)
  (b) same, but the goal is ANY mass at the target's (p, A, c)  -- mass left free
  (c) same, with mass frozen at the ancestor's value (3-D walk over p, A, c) to (p, A, c)_target
  (d) the H_chase plateau: size of the flat region (cells with W == e_swim to 1e-12) connected to the ancestor
Reads only the saved landscape; no new flight integration. SIMULATION-derived; not evidence that any lineage took a path.
"""
from __future__ import annotations

import heapq
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402

TR = ["p", "A", "M", "c"]


def widest(W, start, goals, axes=(0, 1, 2, 3), tol=1e-9):
    best = np.full(W.shape, -np.inf); best[start] = np.inf; prev = {}
    h = [(-np.inf, start)]; goals = set(goals); hit = None
    while h:
        nb, u = heapq.heappop(h); b = -nb
        if b < best[u]:
            continue
        if u in goals:
            hit = u; break
        for ax in axes:
            for s in (-1, 1):
                v = list(u); v[ax] += s; v = tuple(v)
                if not 0 <= v[ax] < W.shape[ax]:
                    continue
                g = W[v] - W[u]; g = 0.0 if abs(g) <= tol else g
                nv = min(b, g)
                if nv > best[v]:
                    best[v] = nv; prev[v] = u; heapq.heappush(h, (-nv, v))
    path = [hit]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path = path[::-1]
    gains = [W[path[i + 1]] - W[path[i]] for i in range(len(path) - 1)]
    k = int(np.argmin(gains))
    ax = [i for i in range(4) if path[k][i] != path[k + 1][i]][0]
    return {"worst_step_dW": float(best[hit]), "goal_cell": list(map(int, hit)), "path_len": len(path) - 1, "n_downhill": int(sum(g < -tol for g in gains)),
            "n_neutral": int(sum(abs(g) <= tol for g in gains)), "bottleneck_trait": TR[ax], "bottleneck_index_from_to": [int(path[k][ax]), int(path[k + 1][ax])]}


def main():
    started = C.utcnow(); inputs = C.input_hashes(__file__)
    d = C.OUT / "eco-reachability"; npz = d / "landscape_default.npz"
    inputs["site/artifacts/simulations/eco-reachability/landscape_default.npz"] = C.sha256_file(npz)
    z = np.load(npz); g = {k: z[k] for k in TR}
    P = dict(C.DEFAULT); a, t = C.ancestor_phenotype(P), C.target_phenotype(P)
    ia = tuple(int(np.argmin(np.abs(g[k] - a[k]))) for k in TR); it = tuple(int(np.argmin(np.abs(g[k] - t[k]))) for k in TR)
    out = {"schema": "frontier.eco.reach-post/1", "ancestor_cell": list(ia), "target_cell": list(it), "grids": {k: g[k].tolist() for k in TR}, "by_hypothesis": {}}
    for h in ("vis", "chase", "both"):
        W = z[f"W_{h}"]
        r = {"a_target_cell": widest(W, ia, [it]),
             "b_any_mass": widest(W, ia, [(it[0], it[1], m, it[3]) for m in range(W.shape[2])]),
             "c_mass_frozen_at_ancestor": widest(W, ia, [(it[0], it[1], ia[2], it[3])], axes=(0, 1, 3))}
        flat = np.abs(W - P["e_swim"]) <= 1e-12
        if flat[ia]:
            seen = {ia}; q = deque([ia])
            while q:
                u = q.popleft()
                for ax in range(4):
                    for s in (-1, 1):
                        v = list(u); v[ax] += s; v = tuple(v)
                        if 0 <= v[ax] < W.shape[ax] and v not in seen and flat[v]:
                            seen.add(v); q.append(v)
            pmax = max(g["p"][u[0]] for u in seen); cmax = max(g["c"][u[3]] for u in seen)
            r["d_plateau"] = {"cells_connected_to_ancestor_with_W_equal_e_swim": len(seen), "max_p_on_plateau": float(pmax), "max_c_on_plateau": float(cmax)}
        else:
            r["d_plateau"] = None
        out["by_hypothesis"][h] = r
        print(h, {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk in ("worst_step_dW", "bottleneck_trait", "n_downhill", "cells_connected_to_ancestor_with_W_equal_e_swim", "max_p_on_plateau")}) for k, v in r.items()}, flush=True)
    C.dump(d / "reach_post.json", out)
    C.dump(d / "receipt_post.json", C.receipt(__file__, 0, started, {"note": "deterministic; reads landscape_default.npz only"}, outputs=[d / "reach_post.json"], inputs=inputs))


if __name__ == "__main__":
    main()
