#!/usr/bin/env python3
"""Actuation-pattern generator for the tissue-microcarrier runner.

Patterns are functions of PHYSICAL position (normalised by body length L), so the same
pattern is defined at every mesh level; that is what makes mesh refinement meaningful.
Exception: family 'riid' (independent random phase per voxel) is lattice-defined and is
flagged mesh_defined=false; it is a control, not a refinable pattern.

Equal total actuation: every active pattern is scaled so that the volume-mean of a_i^2
is 1 (equal L2 actuation budget; voxels have equal volume at a given mesh level). The
volume-mean of |a_i| (L1) is reported too. Phase-only patterns (uniform amplitude) are
equal under both norms.

Coordinates: u in (-1/2, 1/2) along x (body axis), v, w along y, z, all in body lengths.
"""
import argparse, hashlib, json, math, sys
import numpy as np

MESH = {1: (8, 4, 4), 2: (16, 8, 8), 3: (24, 12, 12)}
BODY_LEN_M = 1.0e-3


def mesh_coords(level):
    nx, ny, nz = MESH[level]
    ix, iy, iz = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    u = (ix + 0.5) / nx - 0.5
    v = ((iy + 0.5) / ny - 0.5) * ny / nx
    w = ((iz + 0.5) / nz - 0.5) * nz / nx
    return (nx, ny, nz), ix.ravel(), iy.ravel(), iz.ravel(), u.ravel(), v.ravel(), w.ravel()


def parse(spec):
    fam, _, rest = spec.partition(":")
    kv = {}
    for tok in filter(None, rest.split(",")):
        k, _, val = tok.partition("=")
        kv[k] = val
    return fam, kv


def seed_of(spec):
    return int(hashlib.sha256(spec.encode()).hexdigest()[:8], 16)


def evaluate(spec, u, v, w):
    """Return (a, phi, mesh_defined) before normalisation."""
    fam, p = parse(spec)
    n = u.size
    one = np.ones(n)
    if fam == "off":
        return np.zeros(n), np.zeros(n), True
    if fam == "uniform":
        return one, np.zeros(n), True
    if fam in ("trav", "stand"):
        k = float(p["k"]); th = math.radians(float(p.get("theta", 0)))
        s = u * math.cos(th) + v * math.sin(th)
        if fam == "trav":
            sign = -1.0 if p.get("dir", "fwd") == "fwd" else 1.0  # fwd: crest moves toward +s
            return one, sign * 2 * math.pi * k * s, True
        ph0 = math.radians(float(p.get("ph0", 0)))
        a = np.cos(2 * math.pi * k * s + ph0)
        return np.abs(a), np.where(a >= 0, 0.0, math.pi), True
    if fam == "seg":
        nseg = int(p["n"]); axis = p.get("axis", "x"); mode = p.get("mode", "alt")
        coord = {"x": u, "y": v * 2, "z": w * 2}[axis]  # y,z span (-1/4,1/4) for aspect 2:1
        j = np.clip(np.floor((coord + 0.5) * nseg), 0, nseg - 1)
        if mode == "alt":
            phi = math.pi * (j % 2)
        else:
            sign = -1.0 if mode == "fwd" else 1.0
            phi = sign * 2 * math.pi * j / nseg
        return one, phi, True
    if fam == "half":
        axis = p.get("axis", "x"); side = p.get("side", "pos")
        coord = {"x": u, "y": v, "z": w}[axis]
        act = coord > 0 if side == "pos" else coord < 0
        return act.astype(float), np.zeros(n), True
    if fam == "helix":
        k = float(p["k"]); m = int(p.get("m", 1))
        ang = np.arctan2(w, v)
        return one, -2 * math.pi * k * u + m * ang, True
    if fam == "dvtrav":  # travelling wave along x, with dorsal and ventral halves in antiphase
        k = float(p["k"])
        return one, -2 * math.pi * k * u + math.pi * (w > 0), True
    if fam == "rsmooth":  # smooth random phase field, mesh-defined
        rng = np.random.default_rng(int(p["seed"])); K = int(p.get("K", 4)); amp = float(p.get("amp", 1.0))
        phi = np.zeros(n)
        for _ in range(K):
            kvec = rng.normal(0, 1.5, 3); psi = rng.uniform(0, 2 * math.pi)
            phi += np.cos(2 * math.pi * (kvec[0] * u + kvec[1] * v + kvec[2] * w) + psi)
        return one, amp * math.pi * phi / math.sqrt(K / 2), True
    if fam == "ramp":  # smooth random AMPLITUDE field, in-phase
        rng = np.random.default_rng(int(p["seed"])); K = int(p.get("K", 3))
        f = np.zeros(n)
        for _ in range(K):
            kvec = rng.normal(0, 1.5, 3); psi = rng.uniform(0, 2 * math.pi)
            f += np.cos(2 * math.pi * (kvec[0] * u + kvec[1] * v + kvec[2] * w) + psi)
        return f - f.min() + 1e-3, np.zeros(n), True
    if fam == "riid":
        rng = np.random.default_rng(int(p["seed"]))
        return one, rng.uniform(0, 2 * math.pi, n), False
    raise SystemExit(f"unknown family {fam}")


def build(spec, level, mirror="none"):
    dims, ix, iy, iz, u, v, w = mesh_coords(level)
    if mirror == "y":
        v = -v
    elif mirror == "x":
        u = -u
    elif mirror != "none":
        raise SystemExit("mirror must be none|x|y")
    fam, p = parse(spec)
    if fam == "riid" and mirror != "none":
        # lattice-defined: mirror by index so the mirrored table is the exact reflection
        dims_, ix0, iy0, iz0, u0, v0, w0 = mesh_coords(level)
        a0, phi0, _ = evaluate(spec, u0, v0, w0)
        nx, ny, nz = dims
        idx = {(a, b, c): i for i, (a, b, c) in enumerate(zip(ix0, iy0, iz0))}
        src = [idx[(a if mirror != "x" else nx - 1 - a, b if mirror != "y" else ny - 1 - b, c)] for a, b, c in zip(ix, iy, iz)]
        a, phi, md = a0[src], phi0[src], False
    else:
        a, phi, md = evaluate(spec, u, v, w)
    ms = float(np.mean(a ** 2))
    if ms > 0:
        a = a / math.sqrt(ms)
    phi = np.mod(phi, 2 * math.pi)
    return dims, ix, iy, iz, a, phi, md


def write(spec, level, mirror, out):
    dims, ix, iy, iz, a, phi, md = build(spec, level, mirror)
    nx, ny, nz = dims
    voxel = BODY_LEN_M / nx
    lines = [f"# {nx} {ny} {nz} {voxel:.12g}"]
    lines += [f"{x} {y} {z} {aa:.12f} {pp:.12f}" for x, y, z, aa, pp in zip(ix, iy, iz, a, phi)]
    body = "\n".join(lines) + "\n"
    with open(out, "w") as f:
        f.write(body)
    meta = {"spec": spec, "mesh_level": level, "mirror": mirror, "dims": [nx, ny, nz], "voxel_m": voxel,
            "seed": int(parse(spec)[1].get("seed", seed_of(spec))), "mesh_defined": md,
            "l2_budget_mean_a2": float(np.mean(a ** 2)), "l1_mean_abs_a": float(np.mean(np.abs(a))),
            "max_a": float(a.max()) if a.size else 0.0,
            "sha256": hashlib.sha256(body.encode()).hexdigest()}
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True); ap.add_argument("--mesh", type=int, default=1)
    ap.add_argument("--mirror", default="none"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    print(json.dumps(write(a.spec, a.mesh, a.mirror, a.out)))
