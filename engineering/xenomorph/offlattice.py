"""Off-lattice cell-mechanics aggregation engine (PyTorch, batched on one GPU).

Second, independent engine for the same question as the Cellular Potts arms: does a dissociated
two-type population compact, and does unequal adhesion sort it into core and shell?

Mechanics follow the standard PhysiCell 1.x potential form (Ghaffarizadeh et al. 2018, PLoS Comput Biol
14:e1005991, read at abstract/methods-summary level here; no code from PhysiCell is used):
  repulsion  F_r = c_r (1 - d/R)^2            for d < R   = 2 r
  adhesion   F_a = -c_ij (1 - d/R_A)^2        for d < R_A = 1.25 * 2 r
  overdamped:  dx = sum F dt + sqrt(2 D dt) xi
All quantities dimensionless: r = 1 length unit, mobility 1. No organism parameter is used.
Not PhysiCell itself: PhysiCell 1.14.2 is not installed on this host.

Usage: python -m engineering.xenomorph.offlattice --sweep sweep.json --out DIR [--device cuda]
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

R_CELL = 1.0
R_REP = 2.0 * R_CELL
R_ADH = 1.25 * R_REP


def place(n: int, gap: float, ball: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    dmin = R_ADH + gap  # dissociated: no pair inside adhesion range at t=0
    pts = []
    tries = 0
    while len(pts) < n:
        tries += 1
        if tries > 5_000_000:
            raise RuntimeError("placement failed")
        p = rng.uniform(-ball, ball, 3)
        if np.linalg.norm(p) > ball:
            continue
        if pts and np.min(np.linalg.norm(np.asarray(pts) - p, axis=1)) < dmin:
            continue
        pts.append(p)
    types = np.array([0] * (n // 2) + [1] * (n - n // 2))
    rng.shuffle(types)
    return np.asarray(pts), types


def components(adj: torch.Tensor) -> torch.Tensor:
    """Connected-component labels per system by min-label propagation. adj: (B,N,N) bool."""
    B, N, _ = adj.shape
    lab = torch.arange(N, device=adj.device).expand(B, N).clone()
    big = torch.full_like(lab, N)
    for _ in range(N):
        nb = torch.where(adj, lab[:, None, :], big[:, None, :]).min(dim=2).values
        new = torch.minimum(lab, nb)
        if torch.equal(new, lab):
            break
        lab = new
    return lab


@torch.no_grad()
def metrics(x: torch.Tensor, ty: torch.Tensor) -> dict:
    B, N, _ = x.shape
    d = torch.cdist(x, x)
    eye = torch.eye(N, dtype=torch.bool, device=x.device)[None]
    contact = (d < R_REP * 1.05) & ~eye
    lab = components(contact)
    counts = torch.zeros(B, N, device=x.device).scatter_add_(1, lab, torch.ones_like(lab, dtype=torch.float))
    n_agg = (counts > 0).sum(1)
    lcf = counts.max(1).values / N
    # overlap-weighted contact "area" proxy: sum over contacting pairs of (R_REP*1.05 - d)
    w = torch.where(contact, (R_REP * 1.05 - d), torch.zeros_like(d))
    same = ty[:, :, None] == ty[:, None, :]
    tot = w.sum((1, 2))
    homo = torch.where(same, w, torch.zeros_like(w)).sum((1, 2)) / tot.clamp_min(1e-12)
    c0 = x.mean(1, keepdim=True)
    r = (x - c0).norm(dim=2)
    rg = (r ** 2).mean(1).sqrt()
    rg_norm = rg / (N ** (1 / 3) * R_CELL)
    a = ty == 0
    ra = (r * a).sum(1) / a.sum(1).clamp_min(1)
    rb = (r * ~a).sum(1) / (~a).sum(1).clamp_min(1)
    core_shell = (rb - ra) / rg
    # shape: gyration-tensor asphericity of the whole population (0 = sphere)
    xc = x - c0
    G = torch.einsum("bni,bnj->bij", xc, xc) / N
    ev = torch.linalg.eigvalsh(G)
    asph = ((ev[:, 2] - ev[:, 0]) ** 2 + (ev[:, 2] - ev[:, 1]) ** 2 + (ev[:, 1] - ev[:, 0]) ** 2) / (2 * ev.sum(1) ** 2)
    return {"n_aggregates": n_agg, "largest_cluster_fraction": lcf, "contact_proxy": tot / 2,
            "sorting_index_homotypic": homo, "rg_norm": rg_norm, "core_shell_index": core_shell,
            "asphericity": asph}


def run(cfg: dict, out: Path, device: str) -> dict:
    systems = cfg["systems"]
    N = cfg["n_cells"]
    dev = torch.device(device)
    X, T, C, D, DT, STEPS = [], [], [], [], [], []
    for s in systems:
        p, t = place(N, cfg["gap"], cfg["ball"], s["seed"])
        X.append(p)
        T.append(t)
        C.append([[s["c_AA"], s["c_AB"]], [s["c_AB"], s["c_BB"]]])
        D.append(s["D"])
        DT.append(s["dt"])
    x = torch.tensor(np.stack(X), dtype=torch.float32, device=dev)
    ty = torch.tensor(np.stack(T), dtype=torch.long, device=dev)
    Cm = torch.tensor(C, dtype=torch.float32, device=dev)  # (B,2,2)
    Dv = torch.tensor(D, dtype=torch.float32, device=dev)[:, None, None]
    dtv = torch.tensor(DT, dtype=torch.float32, device=dev)[:, None, None]
    B = x.shape[0]
    cij = Cm[torch.arange(B, device=dev)[:, None, None], ty[:, :, None], ty[:, None, :]]  # (B,N,N)
    c_r = cfg["c_rep"]
    t_end = cfg["t_end"]
    snaps = cfg["snapshot_times"]
    g = torch.Generator(device=dev).manual_seed(cfg["noise_seed"])
    # each system integrates to t_end with its own dt: run the max step count, freeze finished systems
    nsteps = (t_end / dtv.flatten()).round().long()
    max_steps = int(nsteps.max())
    snap_steps = {k: (torch.tensor(snaps, device=dev)[:, None] / dtv.flatten()[None]).round().long() for k in [0]}[0]
    hist = {k: [] for k in ["n_aggregates", "largest_cluster_fraction", "contact_proxy", "sorting_index_homotypic",
                            "rg_norm", "core_shell_index", "asphericity"]}
    rec = torch.zeros(len(snaps), B, len(hist), device=dev)
    pos_rec = torch.zeros(len(snaps), B, N, 3, device=dev)
    eye = torch.eye(N, device=dev, dtype=torch.bool)[None]
    t0 = time.time()
    for step in range(max_steps + 1):
        hit = snap_steps == step  # (S,B)
        if hit.any():
            m = metrics(x, ty)
            vals = torch.stack([m[k].float() for k in hist], 1)  # (B,K)
            for si in torch.nonzero(hit.any(1)).flatten().tolist():
                sel = hit[si]
                rec[si, sel] = vals[sel]
                pos_rec[si, sel] = x[sel]
        if step == max_steps:
            break
        active = (step < nsteps).float()[:, None, None]
        diff = x[:, :, None, :] - x[:, None, :, :]
        d = diff.norm(dim=3).clamp_min(1e-6)
        u = diff / d[..., None]
        rep = torch.where(d < R_REP, c_r * (1 - d / R_REP) ** 2, torch.zeros_like(d))
        adh = torch.where(d < R_ADH, cij * (1 - d / R_ADH) ** 2, torch.zeros_like(d))
        f = ((rep - adh).masked_fill(eye, 0.0))[..., None] * u
        F = f.sum(2)
        noise = torch.randn(x.shape, generator=g, device=dev) * torch.sqrt(2 * Dv * dtv)
        x = x + active * (F * dtv + noise)
        if not torch.isfinite(x).all():
            raise FloatingPointError(f"non-finite positions at step {step}")
    wall = time.time() - t0
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "trajectory.npz", metrics=rec.cpu().numpy(), metric_names=np.array(list(hist)),
                        positions=pos_rec.cpu().numpy().astype(np.float16), types=ty.cpu().numpy().astype(np.int8),
                        snapshot_times=np.array(snaps))
    summ = {"schema": "frontier.xenomorph.offlattice/1", "device": str(dev),
            "gpu": torch.cuda.get_device_name(0) if dev.type == "cuda" else None,
            "torch": torch.__version__, "wall_s": round(wall, 2), "n_systems": B, "n_cells": N,
            "max_steps": max_steps, "config_sha256": hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest(),
            "engine_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "trajectory_sha256": hashlib.sha256((out / "trajectory.npz").read_bytes()).hexdigest()}
    (out / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    return summ


def default_sweep() -> dict:
    systems = []
    for c_AA, ratio, D, dt, seed in itertools.product([0.0, 0.5, 1.0, 2.0, 4.0], [1.0, 0.5, 0.25],
                                                      [0.005, 0.02], [0.02, 0.01], [1, 2, 3, 4]):
        if c_AA == 0.0 and ratio != 1.0:
            continue
        c_BB = c_AA * ratio
        systems.append({"c_AA": c_AA, "c_BB": c_BB, "c_AB": math.sqrt(c_AA * c_BB) if ratio != 1.0 else c_AA,
                        "ratio": ratio, "D": D, "dt": dt, "seed": seed})
    return {"n_cells": 256, "gap": 0.3, "ball": 13.0, "c_rep": 10.0, "t_end": 2000.0,
            "snapshot_times": [0, 25, 50, 100, 200, 400, 700, 1000, 1500, 2000], "noise_seed": 20261101,
            "systems": systems,
            "scope": "dimensionless off-lattice DAH-type adhesion sweep; zero-adhesion (c=0), equal-adhesion (ratio 1) and dt-refinement (0.02 vs 0.01) arms included; not an organism"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep")
    ap.add_argument("--write-default")
    ap.add_argument("--out")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    a = ap.parse_args()
    if a.write_default:
        Path(a.write_default).write_text(json.dumps(default_sweep(), indent=1) + "\n")
    else:
        cfg = json.loads(Path(a.sweep).read_text())
        print(json.dumps(run(cfg, Path(a.out), a.device)))
