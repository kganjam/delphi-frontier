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
PHASE_FMT = "%.6f"   # s1 format; the post-hoc ensemble needs more digits to carry eps

MATS = """
        <Material ID="1"><Name>passive</Name><Display><Red>0</Red><Green>0.6</Green><Blue>1</Blue><Alpha>1</Alpha></Display>
            <Mechanical><MatModel>0</MatModel><Elastic_Mod>1e6</Elastic_Mod><Fail_Stress>0</Fail_Stress><Density>1000</Density>
            <Poissons_Ratio>0.35</Poissons_Ratio><CTE>0</CTE><MaterialTempPhase>0</MaterialTempPhase><uStatic>1</uStatic><uDynamic>0.8</uDynamic></Mechanical></Material>
        <Material ID="2"><Name>active</Name><Display><Red>1</Red><Green>0.2</Green><Blue>0.2</Blue><Alpha>1</Alpha></Display>
            <Mechanical><MatModel>0</MatModel><Elastic_Mod>1e6</Elastic_Mod><Fail_Stress>0</Fail_Stress><Density>1000</Density>
            <Poissons_Ratio>0.35</Poissons_Ratio><CTE>0.01</CTE><MaterialTempPhase>0</MaterialTempPhase><uStatic>1</uStatic><uDynamic>0.8</uDynamic></Mechanical></Material>"""
MAT_CILIA = """
        <Material ID="3"><Name>ciliated</Name><Display><Red>1</Red><Green>0.8</Green><Blue>0</Blue><Alpha>1</Alpha></Display>
            <Mechanical><MatModel>0</MatModel><Elastic_Mod>1e6</Elastic_Mod><Fail_Stress>0</Fail_Stress><Density>1000</Density>
            <Poissons_Ratio>0.35</Poissons_Ratio><CTE>0</CTE><MaterialTempPhase>0</MaterialTempPhase><uStatic>1</uStatic><uDynamic>0.8</uDynamic>
            <Cilia>1</Cilia></Mechanical></Material>"""


LITE = False   # set by --lite: E=1e5, self-collision off, T_END=4 s (population throughput config, disclosed)


def base_vxa(lattice=0.01, dtfrac=0.9, record=0, cilia=False):
    T_END_ = 4.0 if LITE else T_END
    mats = (MATS + (MAT_CILIA if cilia else "")).replace("<Elastic_Mod>1e6</Elastic_Mod>", "<Elastic_Mod>1e5</Elastic_Mod>") if LITE else (MATS + (MAT_CILIA if cilia else ""))
    coll = "<AttachDetach><EnableCollision>0</EnableCollision></AttachDetach>" if LITE else ""
    return f"""<VXA Version="1.1">
<GPU><HeapSize>0.5</HeapSize></GPU>
<Simulator>
    <Integration><DtFrac>{dtfrac}</DtFrac></Integration>
    <Damping><BondDampingZ>1</BondDampingZ><ColDampingZ>0.8</ColDampingZ><SlowDampingZ>0.01</SlowDampingZ></Damping>
    <RecordHistory><RecordStepSize>{record}</RecordStepSize><RecordVoxel>1</RecordVoxel><RecordLink>0</RecordLink></RecordHistory>
    <StopCondition><StopConditionFormula><mtSUB><mtVAR>t</mtVAR><mtCONST>{T_END_}</mtCONST></mtSUB></StopConditionFormula></StopCondition>
    <FitnessFunction><mtVAR>x</mtVAR></FitnessFunction>
    <SecondaryExperiment>1</SecondaryExperiment>{"<EnableCilia>1</EnableCilia>" if cilia else ""}{coll}
    <ReinitializeInitialPositionAfterThisManySeconds>{T_TRANS}</ReinitializeInitialPositionAfterThisManySeconds>
</Simulator>
<Environment>
    <Gravity><GravEnabled>1</GravEnabled><GravAcc>-9.81</GravAcc><FloorEnabled>1</FloorEnabled></Gravity>
    <Thermal><TempEnabled>1</TempEnabled><TempAmplitude>10</TempAmplitude><TempBase>0</TempBase><VaryTempEnabled>1</VaryTempEnabled><TempPeriod>{PERIOD}</TempPeriod></Thermal>
</Environment>
<VXC Version="0.94">
    <Lattice><Lattice_Dim>{lattice}</Lattice_Dim></Lattice>
    <Palette>{mats}
    </Palette>
    <Structure Compression="ASCII_READABLE"><X_Voxels>1</X_Voxels><Y_Voxels>1</Y_Voxels><Z_Voxels>1</Z_Voxels>
        <Data><Layer><![CDATA[1]]></Layer></Data></Structure>
</VXC>
</VXA>
"""


def vxd(mat, phase, nx, ny, nz, cilia=None):
    """mat[x][y][z] in {0,1,2}; phase[x][y][z] in cycles. voxcraft layer order: k = x + nx*y within layer z."""
    layers, players = [], []
    for z in range(nz):
        s, p = [], []
        for y in range(ny):
            for x in range(nx):
                s.append(str(mat[x][y][z]))
                p.append(PHASE_FMT % (phase[x][y][z] if mat[x][y][z] else 0.0))
        layers.append("<Layer><![CDATA[%s]]></Layer>" % "".join(s))
        players.append("<Layer><![CDATA[%s]]></Layer>" % ",".join(p))
    return ("<VXD>\n<Structure replace=\"VXA.VXC.Structure\" Compression=\"ASCII_READABLE\">"
            f"<X_Voxels>{nx}</X_Voxels><Y_Voxels>{ny}</Y_Voxels><Z_Voxels>{nz}</Z_Voxels>\n"
            "<Data>" + "".join(layers) + "</Data>\n<PhaseOffset>" + "".join(players) + "</PhaseOffset>\n"
            + (cilia_xml(mat, cilia, nx, ny, nz) if cilia is not None else "") +
            "</Structure>\n</VXD>\n")


def cilia_xml(mat, f, nx, ny, nz):
    L = []
    for z in range(nz):
        v = []
        for y in range(ny):
            for x in range(nx):
                fx, fy, fz = f[x][y][z]
                v += ["%.9e" % fx, "%.9e" % fy, "%.9e" % fz]
        L.append("<Layer><![CDATA[%s]]></Layer>" % ",".join(v))
    return "<BaseCiliaForce>" + "".join(L) + "</BaseCiliaForce>\n"


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
        txt = vxd(mat, ph, *dims, cilia=meta.pop("_cilia", None))
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
    ap.add_argument("--ensemble", type=int, default=0, help="POST-HOC: N phase-perturbed members per pattern (8x4x3, DtFrac 0.9)")
    ap.add_argument("--lite", action="store_true", help="E=1e5, self-collision off, T_END=4 s; adds endpoints_lite bridge batch")
    ap.add_argument("--pop-start", type=int, default=0, help="first candidate index (same seed stream; for splitting across jobs)")
    ap.add_argument("--cilia", action="store_true", help="Addendum A cilia arm (preregistered before running)")
    ap.add_argument("--eps", type=float, default=1e-7, help="POST-HOC: phase perturbation sd, in cycles")
    a = ap.parse_args()
    manifest = []
    global LITE
    LITE = a.lite
    if LITE:
        bodies = {}
        for pname, (mat, ph) in ref_patterns(8, 4, 3).items():
            for r in range(a.nrep):
                bodies[f"lite_{pname}_r{r}"] = (mat, ph, (8, 4, 3), dict(kind="endpoint_lite", pattern=pname, rep=r, dtfrac=0.9, lattice=0.01, dims="8x4x3"))
        write_batch(os.path.join(a.out, "endpoints_lite"), base_vxa(0.01, 0.9), bodies, manifest, "endpoints_lite")
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
    if a.ensemble:
        # POST-HOC diagnostic (added after E3 failed, on gemini-4-argon's advice): does an O(eps) unmirrored
        # perturbation of the phase field move d by as much as mirroring does? Member 0 is unperturbed.
        global PHASE_FMT
        PHASE_FMT = "%.12e"
        er = random.Random(a.seed + 7)
        for tag, dtf in (("ens_dt090", 0.9),):
            bodies = {}
            for pname, (mat, ph) in ref_patterns(8, 4, 3).items():
                if pname in ("checker", "passive_cte0"):
                    continue
                for m in range(a.ensemble):
                    eps = 0.0 if m == 0 else a.eps
                    php = [[[v + er.gauss(0, eps) for v in Y] for Y in X] for X in ph]
                    bodies[f"ens_{pname}_m{m:03d}"] = (mat, php, (8, 4, 3), dict(kind="ensemble", pattern=pname, member=m, eps=eps, dtfrac=dtf, lattice=0.01, dims="8x4x3"))
            write_batch(os.path.join(a.out, tag), base_vxa(0.01, dtf), bodies, manifest, tag)
        PHASE_FMT = "%.6f"
    if a.cilia:
        nx_, ny_, nz_ = 8, 4, 3
        cm = grid(nx_, ny_, nz_, lambda x, y, z: 3)
        zero = grid(nx_, ny_, nz_, lambda x, y, z: 0.0)
        cr = random.Random(a.seed + 11)
        ang = grid(nx_, ny_, nz_, lambda x, y, z: cr.uniform(0, 2 * math.pi))
        xc, yc = (nx_ - 1) / 2.0, (ny_ - 1) / 2.0
        def fld(F, kind):
            def f(x, y, z):
                if kind == "off": return (0.0, 0.0, 0.0)
                if kind == "px": return (F, 0.0, 0.0)
                if kind == "mx": return (-F, 0.0, 0.0)
                if kind == "py": return (0.0, F, 0.0)
                if kind == "my": return (0.0, -F, 0.0)
                if kind == "dpp": return (F / math.sqrt(2), F / math.sqrt(2), 0.0)
                if kind == "dpm": return (F / math.sqrt(2), -F / math.sqrt(2), 0.0)
                if kind == "swirl":
                    rx, ry = x - xc, y - yc; r = math.hypot(rx, ry); return (-F * ry / r, F * rx / r, 0.0)
                if kind == "rand": a_ = ang[x][y][z]; return (F * math.cos(a_), F * math.sin(a_), 0.0)
                if kind == "randmy": a_ = ang[x][ny_ - 1 - y][z]; return (F * math.cos(a_), -F * math.sin(a_), 0.0)
            return grid(nx_, ny_, nz_, f)
        for tag, dtf in (("cilia_dt090", 0.9), ("cilia_dt045", 0.45)):
            bodies = {}
            for F in (0.005, 0.01, 0.02):
                for kind in ("off", "px", "mx", "py", "my", "dpp", "dpm", "swirl", "rand", "randmy"):
                    if kind == "off" and F != 0.02: continue
                    for r in range(a.nrep):
                        nm = "cil_F%03d_%s_r%d" % (int(F * 1000), kind, r)
                        bodies[nm] = (cm, zero, (nx_, ny_, nz_), dict(kind="cilia", pattern=kind, F=F, rep=r, dtfrac=dtf, lattice=0.01, dims="8x4x3", _cilia=fld(F, kind)))
            write_batch(os.path.join(a.out, tag), base_vxa(0.01, dtf, cilia=True), bodies, manifest, tag)
    rng = random.Random(a.seed)
    nx, ny, nz = 6, 6, 5
    bi = 0
    bodies = {}
    for i in range(a.npop):
        mat, ph = random_body(rng, nx, ny, nz)
        pas = grid(nx, ny, nz, lambda x, y, z: 1 if mat[x][y][z] else 0)
        if i < a.pop_start:
            continue   # candidate i is still drawn from the seeded stream so indices are identical across jobs
        meta = dict(kind="pop", cand=i, seed=a.seed, dtfrac=0.9, lattice=0.01, dims="6x6x5", lite=LITE)
        bodies[f"c{i:05d}_act"] = (mat, ph, (nx, ny, nz), dict(meta, arm="act"))
        bodies[f"c{i:05d}_pas"] = (pas, ph, (nx, ny, nz), dict(meta, arm="pas"))
        bodies[f"c{i:05d}_mir"] = (mirror_x(mat, nx), mirror_x(ph, nx), (nx, ny, nz), dict(meta, arm="mir"))
        # identical duplicate of the actuated arm: run-to-run noise floor for the mirror comparison (argon review)
        bodies[f"c{i:05d}_rep"] = (mat, ph, (nx, ny, nz), dict(meta, arm="rep"))
        if len(bodies) >= 4 * a.popbatch or i == a.npop - 1:
            write_batch(os.path.join(a.out, f"pop_{bi:02d}"), base_vxa(0.01, 0.9), bodies, manifest, f"pop_{bi:02d}")
            bodies = {}; bi += 1
    with open(os.path.join(a.out, "manifest.json"), "w") as f:
        json.dump(dict(seed=a.seed, lite=LITE, T_TRANS=T_TRANS, T_END=(4.0 if LITE else T_END), PERIOD=PERIOD, n=len(manifest), bodies=manifest), f)
    print("generated", len(manifest), "bodies in", a.out)


if __name__ == "__main__":
    main()
