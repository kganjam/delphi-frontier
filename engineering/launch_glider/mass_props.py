"""Mass, centre of mass and inertia from triangle meshes: closed solids and thin sheets/shells.

Solid: signed-tetrahedron decomposition of a closed, outward-oriented mesh (exact for the polyhedron):
    for tet (0, a, b, c) with volume v = det[a b c]/6,
    int x x^T dV = v/20 * (S S^T + a a^T + b b^T + c c^T),   S = a + b + c
Sheet of uniform areal density: per triangle of area A,
    int x x^T dA = A/12 * (S S^T + a a^T + b b^T + c c^T)
(both recalled; each is checked in the tests against analytic solids and shells).
A sheet's own thickness inertia (t^2/12 terms) is neglected: second order in t / size.
Inertia is reported about the CG in the mesh frame: I = tr(C) 1 - C with C = int (x - x_cg)(x - x_cg)^T dm.
"""
from __future__ import annotations

import struct

import numpy as np


def read_stl(path) -> np.ndarray:
    """(n, 3, 3) float64 triangles from a binary STL, in the file's units."""
    return parse_stl(open(path, "rb").read(), str(path))


def parse_stl(b: bytes, name: str = "stl") -> np.ndarray:
    n = struct.unpack("<I", b[80:84])[0]
    if len(b) != 84 + 50 * n:
        raise ValueError(f"{name}: not a binary STL of {n} triangles ({len(b)} bytes)")
    a = np.frombuffer(b[84:84 + 50 * n], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    return a["v"].reshape(-1, 3, 3).astype(float)


def _second(tri: np.ndarray, w: np.ndarray) -> np.ndarray:
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    S = a + b + c
    outer = (np.einsum("ni,nj->nij", S, S) + np.einsum("ni,nj->nij", a, a)
             + np.einsum("ni,nj->nij", b, b) + np.einsum("ni,nj->nij", c, c))
    return np.einsum("n,nij->ij", w, outer)


def _about_cg(m: float, first: np.ndarray, second: np.ndarray) -> dict:
    cg = first / m
    C = second - m * np.outer(cg, cg)
    inertia = np.trace(C) * np.eye(3) - C
    return {"mass_kg": float(m), "cg_m": cg.tolist(), "inertia_cg_kg_m2": inertia.tolist()}


def solid(tri: np.ndarray, density: float) -> dict:
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    v = np.einsum("ni,ni->n", a, np.cross(b, c)) / 6.0
    V = float(v.sum())
    if V <= 0:
        raise ValueError(f"signed volume {V} <= 0: mesh not closed/outward")
    first = density * np.einsum("n,ni->i", v, a + b + c) / 4.0
    second = density * _second(tri, v) / 20.0
    return {**_about_cg(density * V, first, second), "volume_m3": V, "kind": "solid"}


def sheet(tri: np.ndarray, density: float, thickness: float) -> dict:
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    A = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    sig = density * thickness
    first = sig * np.einsum("n,ni->i", A, a + b + c) / 3.0
    second = sig * _second(tri, A) / 12.0
    return {**_about_cg(sig * A.sum(), first, second), "area_m2": float(A.sum()), "thickness_m": thickness,
            "kind": "sheet"}


def point(mass: float, at) -> dict:
    x = np.asarray(at, float)
    return {"mass_kg": float(mass), "cg_m": x.tolist(), "inertia_cg_kg_m2": np.zeros((3, 3)).tolist(), "kind": "point"}


def combine(parts: list[dict]) -> dict:
    """Parallel-axis sum of parts given about their own CGs."""
    m = sum(p["mass_kg"] for p in parts)
    cg = sum(p["mass_kg"] * np.asarray(p["cg_m"]) for p in parts) / m
    inertia = np.zeros((3, 3))
    for p in parts:
        d = np.asarray(p["cg_m"]) - cg
        inertia += np.asarray(p["inertia_cg_kg_m2"]) + p["mass_kg"] * (d @ d * np.eye(3) - np.outer(d, d))
    return {"mass_kg": float(m), "cg_m": cg.tolist(), "inertia_cg_kg_m2": inertia.tolist()}
