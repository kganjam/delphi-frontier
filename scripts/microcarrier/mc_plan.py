#!/usr/bin/env python3
"""Enumerate every run of the microcarrier protocol (endpoints + sweep) as JSON lines.
The plan is part of the frozen protocol: its sha256 is recorded there."""
import json, sys

ZG1, ZI1 = 0.1, 1.0   # damping ratios at mesh 1


def zetas(mesh, policy):
    """Mesh-consistent damping. Voxelyze damping is c = 2*zeta*sqrt(m*E*s) ~ s^2
    (VX_MaterialVoxel.cpp:75), so at constant zeta the global drag per unit volume
    scales as 1/s and the internal (link) viscosity as s. 'consistent' keeps both
    fixed in physical units across mesh levels; 'constant' is the engine-default
    practice and is run as a disclosed supplement."""
    if policy == "constant":
        return ZG1, ZI1
    return ZG1 / mesh, ZI1 * mesh   # s_m = s_1 / m


def run(rid, spec, mesh=1, mirror="none", dt=0.5, freq=10.0, passive=0, group="sweep", policy="consistent"):
    zg, zi = zetas(mesh, policy)
    return {"id": rid, "spec": spec, "mesh": mesh, "mirror": mirror, "dtScale": dt, "freq": freq,
            "passive": passive, "group": group, "zetaGlob": zg, "zetaInt": zi, "damping_policy": policy}

E2A = "trav:k=1,theta=0,dir=bwd"   # retrograde travelling wave, one wavelength per body
E2B = "trav:k=2,theta=0,dir=bwd"   # same direction, two wavelengths per body
E2C = "seg:n=2,axis=x,mode=alt"    # symmetric control: x-reflection == half-period shift, so zero by symmetry
E3M = "trav:k=1,theta=30,dir=fwd"  # oblique wave, mirrored across the y=0 plane
DT_SERIES = [0.5, 0.25, 0.125, 0.0625]
MESH_SERIES = [1, 2, 3]

def endpoints():
    out = []
    # E1 passive control: actuation off. Primary at base resolution, plus refinement checks.
    for m, dt in [(1, 0.5), (1, 0.25), (2, 0.5), (3, 0.5)]:
        out.append(run(f"E1-passive-m{m}-dt{dt}", "off", m, "none", dt, passive=1, group="E1"))
    # E1 supplement (not the gate): symmetric in-phase drive, zero net motion expected by symmetry
    for m in [1, 2]:
        out.append(run(f"E1s-uniform-m{m}-dt0.5", "uniform", m, group="E1s"))
    # E2/E3 refinement series for every pattern the two endpoints compare.
    pats = [("A", E2A, "none"), ("B", E2B, "none"), ("M", E3M, "none"), ("My", E3M, "y"), ("Ax", E2A, "x")]
    for tag, spec, mir in pats:
        grp = "E2" if tag in ("A", "B") else "E3"
        for dt in DT_SERIES:
            out.append(run(f"{grp}-{tag}-m1-dt{dt}", spec, 1, mir, dt, group=grp))
        for m in MESH_SERIES[1:]:
            out.append(run(f"{grp}-{tag}-m{m}-dt0.5", spec, m, mir, 0.5, group=grp))
        out.append(run(f"{grp}-{tag}-m2-dt0.25", spec, 2, mir, 0.25, group=grp))
        for m in MESH_SERIES[1:]:   # supplement: constant-zeta mesh series
            out.append(run(f"{grp}s-{tag}-m{m}-dt0.5-constzeta", spec, m, mir, 0.5, group=grp + "s", policy="constant"))
    # symmetric control C (supplement to E2): prediction |d_C| ~ 0
    for m, dt in [(1, 0.5), (1, 0.25), (2, 0.5)]:
        out.append(run(f"E2s-C-m{m}-dt{dt}", E2C, m, "none", dt, group="E2s"))
    return out

def sweep():
    out = []
    ks = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4]
    for f in [2.5, 5.0, 10.0, 20.0]:
        for k in ks:
            for d in ["fwd", "bwd"]:
                out.append(run(f"S-trav-x-k{k}-{d}-f{f}", f"trav:k={k},theta=0,dir={d}", freq=f))
    for k in [0.5, 1, 2]:
        for th in [15, 30, 45, 60, 75, 90, 120, 150]:
            out.append(run(f"S-trav-k{k}-th{th}", f"trav:k={k},theta={th},dir=fwd"))
    for k in [0.5, 1, 1.5, 2, 3]:
        for ph in [0, 45, 90, 135]:
            out.append(run(f"S-stand-x-k{k}-ph{ph}", f"stand:k={k},theta=0,ph0={ph}"))
    for k in [0.5, 1, 2]:
        for ph in [0, 90]:
            out.append(run(f"S-stand-y-k{k}-ph{ph}", f"stand:k={k},theta=90,ph0={ph}"))
    for n in [2, 3, 4, 5, 6, 8]:
        for mode in ["alt", "fwd", "bwd"]:
            out.append(run(f"S-seg-x-n{n}-{mode}", f"seg:n={n},axis=x,mode={mode}"))
    for ax in ["y", "z"]:
        for n in [2, 4]:
            for mode in ["alt", "fwd"]:
                out.append(run(f"S-seg-{ax}-n{n}-{mode}", f"seg:n={n},axis={ax},mode={mode}"))
    for ax in ["x", "y", "z"]:
        for side in ["pos", "neg"]:
            out.append(run(f"S-half-{ax}-{side}", f"half:axis={ax},side={side}"))
    for k in [0.5, 1, 2]:
        for m in [1, -1, 2]:
            out.append(run(f"S-helix-k{k}-m{m}", f"helix:k={k},m={m}"))
    for k in [0.5, 1, 2]:
        out.append(run(f"S-dvtrav-k{k}", f"dvtrav:k={k}"))
    out.append(run("S-uniform", "uniform"))
    out.append(run("S-off", "off", passive=1))
    for s in range(1, 81):
        out.append(run(f"S-rsmooth-{s}", f"rsmooth:seed={s},K=4"))
    for s in range(1, 31):
        out.append(run(f"S-ramp-{s}", f"ramp:seed={s},K=3"))
    for s in range(1, 61):
        out.append(run(f"S-riid-{s}", f"riid:seed={s}"))
    # mirrored twins (y=0 plane) -- secondary mirror-symmetry evidence across many patterns
    for k in [0.5, 1, 2]:
        for th in [15, 30, 45, 60, 75, 90, 120, 150]:
            out.append(run(f"S-trav-k{k}-th{th}-my", f"trav:k={k},theta={th},dir=fwd", mirror="y"))
    for k in [0.5, 1, 2]:
        for m in [1, -1, 2]:
            out.append(run(f"S-helix-k{k}-m{m}-my", f"helix:k={k},m={m}", mirror="y"))
    for s in range(1, 21):
        out.append(run(f"S-rsmooth-{s}-my", f"rsmooth:seed={s},K=4", mirror="y"))
    # mesh-2 replicates of the structured families at 10 Hz: does the ranking survive refinement?
    m2 = [r for r in out if r["freq"] == 10.0 and r["mirror"] == "none" and
          (r["id"].startswith(("S-trav-x-", "S-seg-x-", "S-stand-x-", "S-half-")) or r["id"] in ("S-uniform",))]
    out += [dict(r, id=r["id"] + "-m2", mesh=2, group="sweep-m2") for r in m2]
    return out

if __name__ == "__main__":
    for r in endpoints() + sweep():
        print(json.dumps(r, sort_keys=True))
