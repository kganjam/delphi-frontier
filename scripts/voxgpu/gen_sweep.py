#!/usr/bin/env python3
"""Generate voxcraft-sim input batches for the claude-voxgpu CDO sweep (pure python3.6, no numpy).

Every body is a .vxd that replaces VXA.VXC.Structure (and, where needed, VXA.VXC.Lattice and
VXA.Simulator.Integration) in a shared base.vxa. Generic soft-voxel parameters, NOT tissue-calibrated:
E = 1e6 Pa, rho = 1000 kg/m^3, nu = 0.35, CTE(active) = 0.01 /deg, TempAmplitude = 10 deg, contraction
only (voxcraft default EnableExpansion=0 clips positive temperature), period 0.25 s, gravity + floor,
Coulomb friction uStatic=1, uDynamic=0.8. The initial centre of mass is re-zeroed after a stated
transient window (ReinitializeInitialPositionAfterThisManySeconds = T_TRANS) via SecondaryExperiment=1.

Batches written (one directory each, each runs as one voxcraft-sim invocation on one GPU):
  endpoints_dt*   reference block 8x4x3 @ 10 mm, all voxels active, equal total actuation; patterns
                  passive_cte0 (all-passive material, actuation reaches no voxel), wave+x, wave-x
                  (mirror), wave+y, wave-y (mirror), sync, checker, split+x / split-x (mirror);
                  3 replicates each (determinism). One batch per DtFrac in {0.9, 0.45, 0.225}.
  endpoints_mesh  same patterns on a 16x8x6 @ 5 mm body (same physical envelope, same mass), DtFrac 0.9.
  pop_*           N random connected bodies in a 6x6x5 box with random active/passive tissue and a random
                  smooth phase field; for each candidate also its passive control (all CTE=0) and its
                  x-mirror (body and phase field reflected x -> -x), and an identical duplicate (noise floor).
                  Seeded: --seed.
"""
import argparse, json, math, os, random, hashlib

T_TRANS = 1.0      # transient window, s (centre of mass re-zeroed after this)
T_END = 6.0        # stop time, s  -> 5 s measured window = 20 actuation cycles
PERIOD = 0.25

MATS = """
        <Material ID="1"><Name>passive</Name><Display><Red>0</Red><Green>0.6</Green><Blue>1</Blue><Alpha>1</Alpha></Display>
            <Mechanical><MatModel>0</MatModel><Elastic_Mod>1e6</Elastic_Mod><Fail_Stress>0</Fail_Stress><Density>1000</Density>
            <Poissons_Ratio>0.35</Poissons_Ratio><CTE>0</CTE><MaterialTempPhase>0</MaterialTempPhase><uStatic>1</uStatic><uDynamic>0.8</uDynamic></Mechanical></Material>
        <Material ID="2"><Name>active</Name><Display><Red>1</Red><Green>0.2</Green><Blue>0.2</Blue><Alpha>1</Alpha></Display>
            <Mechanical><MatModel>0</MatModel><Elastic_Mod>1e6</Elastic_Mod><Fail_Stress>0</Fail_Stress><Density>1000</Density>
            <Poissons_Ratio>0.35</Poissons_Ratio><CTE>0.01</CTE><MaterialTempPhase>0</MaterialTempPhase><uStatic>1</uStatic><uDynamic>0.8</uDynamic></Mechanical></Material>"""


def base_vxa(lattice=0.01, dtfrac=0.9, record=0):
    return f"""<VXA Version="1.1">
<GPU><HeapSize>0.5</HeapSize></GPU>
<Simulator>
    <Integration><DtFrac>{dtfrac}</DtFrac></Integration>
    <Damping><BondDampingZ>1</BondDampingZ><ColDampingZ>0.8</ColDampingZ><SlowDampingZ>0.01</SlowDampingZ></Damping>
    <RecordHistory><RecordStepSize>{record}</RecordStepSize><RecordVoxel>1</RecordVoxel><RecordLink>0</RecordLink></RecordHistory>
    <StopCondition><StopConditionFormula><mtSUB><mtVAR>t</mtVAR><mtCONST>{T_END}</mtCONST></mtSUB></StopConditionFormula></StopCondition>
    <FitnessFunction><mtVAR>x</mtVAR></FitnessFunction>
    <SecondaryExperiment>1</SecondaryExperiment>
    <ReinitializeInitialPositionAfterThisManySeconds>{T_TRANS}</ReinitializeInitialPositionAfterThisManySeconds>
</Simulator>
<Environment>
    <Gravity><GravEnabled>1</GravEnabled><GravAcc>-9.81</GravAcc><FloorEnabled>1</FloorEnabled></Gravity>
    <Thermal><TempEnabled>1</TempEnabled><TempAmplitude>10</TempAmplitude><TempBase>0</TempBase><VaryTempEnabled>1</VaryTempEnabled><TempPeriod>{PERIOD}</TempPeriod></Thermal>
</Environment>
<VXC Version="0.94">
    <Lattice><Lattice_Dim>{lattice}</Lattice_Dim></Lattice>
    <Palette>{MATS}
    </Palette>
    <Structure Compression="ASCII_READABLE"><X_Voxels>1</X_Voxels><Y_Voxels>1</Y_Voxels><Z_Voxels>1</Z_Voxels>
        <Data><Layer><![CDATA[1]]></Layer></Data></Structure>
</VXC>
</VXA>
"""


def vxd(mat, phase, nx, ny, nz):
    """mat[x][y][z] in {0,1,2}; phase[x][y][z] in cycles. voxcraft layer order: k = x + nx*y within layer z."""
    layers, players = [], []
    for z in range(nz):
        s, p = [], []
        for y in range(ny):
            for x in range(nx):
                s.append(str(mat[x][y][z]))
                p.append("%.6f" % (phase[x][y][z] if mat[x][y][z] else 0.0))
        layers.append("<Layer><![CDATA[%s]]></Layer>" % "".join(s))
        players.append("<Layer><![CDATA[%s]]></Layer>" % ",".join(p))
    return ("<VXD>\n<Structure replace=\"VXA.VXC.Structure\" Compression=\"ASCII_READABLE\">"
            f"<X_Voxels>{nx}</X_Voxels><Y_Voxels>{ny}</Y_Voxels><Z_Voxels>{nz}</Z_Voxels>\n"
            "<Data>" + "".join(layers) + "</Data>\n<PhaseOffset>" + "".join(players) + "</PhaseOffset>\n"
            "</Structure>\n</VXD>\n")


def grid(nx, ny, nz, f):
    return [[[f(x, y, z) for z in range(nz)] for y in range(ny)] for x in range(nx)]


def ref_patterns(nx, ny, nz):
    """Patterns on a solid block. All active voxels share amplitude; only phase differs -> equal total actuation.
    Phase is a function of the voxel's normalised centre position u in [0,1) so the 2x mesh is the same field."""
    def u(i, n):  # normalised centre coordinate in [0,1]
        return (i + 0.5) / n
    allact = grid(nx, ny, nz, lambda x, y, z: 2)
    allpas = grid(nx, ny, nz, lambda x, y, z: 1)
    P = {
        "passive_cte0": (allpas, grid(nx, ny, nz, lambda x, y, z: 0.0)),
        "sync":        (allact, grid(nx, ny, nz, lambda x, y, z: 0.0)),
        "wave_px":     (allact, grid(nx, ny, nz, lambda x, y, z: -u(x, nx))),
        "wave_mx":     (allact, grid(nx, ny, nz, lambda x, y, z: -u(nx - 1 - x, nx))),
        "wave_py":     (allact, grid(nx, ny, nz, lambda x, y, z: -u(y, ny))),
        "wave_my":     (allact, grid(nx, ny, nz, lambda x, y, z: -u(ny - 1 - y, ny))),
        "checker":     (allact, grid(nx, ny, nz, lambda x, y, z: 0.5 * ((int(u(x, nx) * 8) + int(u(y, ny) * 4) + int(u(z, nz) * 3)) % 2))),
        "split_px":    (allact, grid(nx, ny, nz, lambda x, y, z: 0.0 if u(x, nx) < 0.5 else 0.25)),
        "split_mx":    (allact, grid(nx, ny, nz, lambda x, y, z: 0.0 if u(nx - 1 - x, nx) < 0.5 else 0.25)),
        "diag_pxpy":   (allact, grid(nx, ny, nz, lambda x, y, z: -(u(x, nx) + u(y, ny)) / 2)),
        "diag_pxmy":   (allact, grid(nx, ny, nz, lambda x, y, z: -(u(x, nx) + u(ny - 1 - y, ny)) / 2)),
    }
    return P


def write_batch(d, base, bodies, manifest, batchname):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "base.vxa"), "w") as f:
        f.write(base)
    for name, (mat, ph, dims, meta) in bodies.items():
        txt = vxd(mat, ph, *dims)
        fn = name + ".vxd"
        with open(os.path.join(d, fn), "w") as f:
            f.write(txt)
        m = dict(meta); m.update(batch=batchname, file=fn, sha256=hashlib.sha256(txt.encode()).hexdigest()[:16],
                                 n_vox=sum(1 for X in mat for Y in X for v in Y if v),
                                 n_active=sum(1 for X in mat for Y in X for v in Y if v == 2))
        manifest.append(m)


def connected(mat, nx, ny, nz):
    vox = [(x, y, z) for x in range(nx) for y in range(ny) for z in range(nz) if mat[x][y][z]]
    if not vox:
        return False
    seen, st = {vox[0]}, [vox[0]]
    S = set(vox)
    while st:
        x, y, z = st.pop()
        for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            q = (x+dx, y+dy, z+dz)
            if q in S and q not in seen:
                seen.add(q); st.append(q)
    return len(seen) == len(S)


def random_body(rng, nx, ny, nz):
    """Smooth random fields from a few random Fourier modes (CPPN-like smoothness, not a CPPN)."""
    def field(nmodes=3):
        modes = [(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5), rng.uniform(0, 2*math.pi), rng.uniform(0.5, 1))
                 for _ in range(nmodes)]
        return lambda x, y, z: sum(a * math.sin(2*math.pi*(kx*x/nx + ky*y/ny + kz*z/nz) + p) for kx, ky, kz, p, a in modes)
    while True:
        occ, tis, ph = field(), field(), field(2)
        thr = rng.uniform(-0.6, 0.4)
        mat = grid(nx, ny, nz, lambda x, y, z: 0 if occ(x, y, z) < thr else (2 if tis(x, y, z) > 0 else 1))
        # keep the largest structure only if fully connected and has floor contact and both tissues
        if not connected(mat, nx, ny, nz):
            continue
        n = sum(1 for X in mat for Y in X for v in Y if v)
        na = sum(1 for X in mat for Y in X for v in Y if v == 2)
        if n < 0.25 * nx*ny*nz or na < 4 or na == n:
            continue
        if not any(mat[x][y][0] for x in range(nx) for y in range(ny)):
            continue
        phase = grid(nx, ny, nz, lambda x, y, z: (ph(x, y, z) / 2.0) % 1.0)
        return mat, phase


def mirror_x(arr, nx):
    return [arr[nx - 1 - x] for x in range(nx)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--npop", type=int, default=1000)
    ap.add_argument("--popbatch", type=int, default=500, help="candidates per batch (x3 sims each)")
    ap.add_argument("--nrep", type=int, default=3)
    ap.add_argument("--skip-endpoints", action="store_true")
    a = ap.parse_args()
    manifest = []
    if not a.skip_endpoints:
        for tag, dtf in (("dt090", 0.9), ("dt045", 0.45), ("dt0225", 0.225)):
            bodies = {}
            for pname, (mat, ph) in ref_patterns(8, 4, 3).items():
                for r in range(a.nrep):
                    bodies[f"ref_{pname}_r{r}"] = (mat, ph, (8, 4, 3), dict(kind="endpoint", pattern=pname, rep=r, dtfrac=dtf, lattice=0.01, dims="8x4x3"))
            write_batch(os.path.join(a.out, "endpoints_" + tag), base_vxa(0.01, dtf), bodies, manifest, "endpoints_" + tag)
        bodies = {}
        for pname, (mat, ph) in ref_patterns(16, 8, 6).items():
            for r in range(a.nrep):
                bodies[f"fine_{pname}_r{r}"] = (mat, ph, (16, 8, 6), dict(kind="endpoint", pattern=pname, rep=r, dtfrac=0.9, lattice=0.005, dims="16x8x6"))
        write_batch(os.path.join(a.out, "endpoints_mesh"), base_vxa(0.005, 0.9), bodies, manifest, "endpoints_mesh")
    rng = random.Random(a.seed)
    nx, ny, nz = 6, 6, 5
    bi = 0
    bodies = {}
    for i in range(a.npop):
        mat, ph = random_body(rng, nx, ny, nz)
        pas = grid(nx, ny, nz, lambda x, y, z: 1 if mat[x][y][z] else 0)
        meta = dict(kind="pop", cand=i, seed=a.seed, dtfrac=0.9, lattice=0.01, dims="6x6x5")
        bodies[f"c{i:05d}_act"] = (mat, ph, (nx, ny, nz), dict(meta, arm="act"))
        bodies[f"c{i:05d}_pas"] = (pas, ph, (nx, ny, nz), dict(meta, arm="pas"))
        bodies[f"c{i:05d}_mir"] = (mirror_x(mat, nx), mirror_x(ph, nx), (nx, ny, nz), dict(meta, arm="mir"))
        # identical duplicate of the actuated arm: run-to-run noise floor for the mirror comparison (argon review)
        bodies[f"c{i:05d}_rep"] = (mat, ph, (nx, ny, nz), dict(meta, arm="rep"))
        if len(bodies) >= 4 * a.popbatch or i == a.npop - 1:
            write_batch(os.path.join(a.out, f"pop_{bi:02d}"), base_vxa(0.01, 0.9), bodies, manifest, f"pop_{bi:02d}")
            bodies = {}; bi += 1
    with open(os.path.join(a.out, "manifest.json"), "w") as f:
        json.dump(dict(seed=a.seed, T_TRANS=T_TRANS, T_END=T_END, PERIOD=PERIOD, n=len(manifest), bodies=manifest), f)
    print("generated", len(manifest), "bodies in", a.out)


if __name__ == "__main__":
    main()
