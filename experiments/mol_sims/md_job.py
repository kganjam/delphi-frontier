"""Runs INSIDE a Nebius AI job container (1x H100). Explicit-solvent OpenMM MD of one predicted structure.

Input: /in/start.pdb.gz.b64 or /in/start.pdb.xz.b64 (heavy-atom PDB from a Boltz-2 model, compressed+base64 so it fits the 64 KiB --inject-file limit).
Prep: PDBFixer adds missing heavy atoms/hydrogens at pH 7; amber14-all + TIP3P-FB, 1.0 nm padding, 0.15 M NaCl.
Protocol: minimise; 100 ps NVT; 200 ps NPT (1 bar); PROD_NS production NPT at 301 K; 2 fs, HBonds, PME 1.0 nm,
LangevinMiddle 1/ps. Seed from argv. CA frames every 10 ps are analysed in-container; the JSON summary and the
final protein-only frame (gz+b64) are printed between markers for retrieval from job logs (no bucket needed).
SIMULATED, not observed.
"""
import base64, gzip, io, json, sys, time

import numpy as np
import openmm as mm
import openmm.app as app
import openmm.unit as u
from pdbfixer import PDBFixer

SEED = int(sys.argv[1]); PROD_NS = float(sys.argv[2]); TAG = sys.argv[3]
T = 301.0 * u.kelvin
t0 = time.time()
import glob, lzma
src = glob.glob("/in/start.pdb.*.b64")[0]
blob = base64.b64decode(open(src).read())
raw = lzma.decompress(blob) if src.endswith(".xz.b64") else gzip.decompress(blob)
open("/tmp/start.pdb", "wb").write(raw)
fx = PDBFixer(filename="/tmp/start.pdb")
fx.findMissingResidues(); fx.missingResidues = {}
fx.findNonstandardResidues(); fx.findMissingAtoms(); fx.addMissingAtoms(); fx.addMissingHydrogens(7.0)
ff = app.ForceField("amber14-all.xml", "amber14/tip3pfb.xml")
mod = app.Modeller(fx.topology, fx.positions)
mod.addSolvent(ff, padding=1.0 * u.nanometer, ionicStrength=0.15 * u.molar, neutralize=True)
system = ff.createSystem(mod.topology, nonbondedMethod=app.PME, nonbondedCutoff=1.0 * u.nanometer, constraints=app.HBonds)
baro = mm.MonteCarloBarostat(1.0 * u.bar, T, 25); baro.setRandomNumberSeed(SEED)
integ = mm.LangevinMiddleIntegrator(T, 1.0 / u.picosecond, 0.002 * u.picoseconds); integ.setRandomNumberSeed(SEED)
plat = mm.Platform.getPlatformByName("CUDA")
sim = app.Simulation(mod.topology, system, integ, plat, {"Precision": "mixed"})
sim.context.setPositions(mod.positions)
e0 = sim.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(u.kilojoule_per_mole)
sim.minimizeEnergy(tolerance=10.0 * u.kilojoule_per_mole / u.nanometer)
e1 = sim.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(u.kilojoule_per_mole)
sim.context.setVelocitiesToTemperature(T, SEED)
sim.step(50000)                                   # 100 ps NVT (barostat not yet added)
system.addForce(baro); sim.context.reinitialize(preserveState=True)
sim.step(100000)                                  # 200 ps NPT
ca = [a.index for a in mod.topology.atoms() if a.name == "CA"]
prot = [a.index for a in mod.topology.atoms() if a.residue.name not in ("HOH", "NA", "CL")]
res_ids = [a.residue.index for a in mod.topology.atoms() if a.name == "CA"]
ca_chain = np.array([a.residue.chain.index for a in mod.topology.atoms() if a.name == "CA"])
ref = np.array(sim.context.getState(getPositions=True).getPositions(asNumpy=True).value_in_unit(u.angstrom))[ca]
frames, energies, tp = [], [], time.time()
nblock = int(round(PROD_NS * 1000 / 10))         # 10 ps blocks
for i in range(nblock):
    sim.step(5000)
    st = sim.context.getState(getPositions=True, getEnergy=True)
    frames.append(np.array(st.getPositions(asNumpy=True).value_in_unit(u.angstrom))[ca])
    energies.append(st.getPotentialEnergy().value_in_unit(u.kilojoule_per_mole))
wall_prod = time.time() - tp


def kabsch(P, Q):
    Pc, Qc = P - P.mean(0), Q - Q.mean(0)
    V, S, W = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(V @ W))
    D = np.diag([1, 1, d])
    return Pc @ (V @ D @ W), Qc


F = np.array(frames)
rmsd = []
for f in F:
    a, b = kabsch(f, ref); rmsd.append(float(np.sqrt(((a - b) ** 2).sum(1).mean())))
half = len(F) // 5                                # discard first 20 % for RMSF
mean = F[half:].mean(0)
al = np.array([kabsch(f, mean)[0] for f in F[half:]])
mc = mean - mean.mean(0)
rmsf = np.sqrt(((al - mc) ** 2).sum(2).mean(0))
contacts = None
if len(set(ca_chain.tolist())) > 1:
    A, B = ca_chain == ca_chain.min(), ca_chain != ca_chain.min()
    d0 = np.linalg.norm(ref[A][:, None] - ref[B][None], axis=-1); pairs0 = d0 < 8.0
    contacts = {"n_initial_ca_pairs_lt8A": int(pairs0.sum()),
                "fraction_initial_pairs_retained_every_10ps": [round(float((np.linalg.norm(f[A][:, None] - f[B][None], axis=-1)[pairs0] < 8.0).mean()), 3) for f in F],
                "min_interchain_ca_distance_A_every_10ps": [round(float(np.linalg.norm(f[A][:, None] - f[B][None], axis=-1).min()), 2) for f in F]}
rg = [float(np.sqrt(((f - f.mean(0)) ** 2).sum(1).mean())) for f in F]
buf = io.StringIO()
pos = sim.context.getState(getPositions=True).getPositions()
sub = app.Modeller(mod.topology, pos); sub.deleteWater(); sub.delete([a for a in sub.topology.atoms() if a.residue.name in ("NA", "CL")])
app.PDBFile.writeFile(sub.topology, sub.positions, buf)
out = {"tag": TAG, "seed": SEED, "prod_ns": PROD_NS, "n_atoms": system.getNumParticles(), "n_ca": len(ca),
       "openmm": mm.__version__, "platform": "CUDA mixed", "E_before_min": e0, "E_after_min": e1,
       "ns_per_day": PROD_NS / (wall_prod / 86400), "wall_s_total": time.time() - t0,
       "rmsd_ca_A_every_10ps": [round(x, 3) for x in rmsd], "rg_ca_A_every_10ps": [round(x, 3) for x in rg],
       "rmsf_ca_A_after_20pct": [round(float(x), 3) for x in rmsf], "potential_kj_mol_every_10ps": [round(x, 1) for x in energies],
       "interface": contacts, "all_finite": bool(np.isfinite(F).all() and np.isfinite(energies).all())}
print("@@SUMMARY_BEGIN@@"); print(json.dumps(out)); print("@@SUMMARY_END@@", flush=True)
b = base64.b64encode(gzip.compress(buf.getvalue().encode())).decode()
print("@@FINAL_PDB_GZ_B64_BEGIN@@")
for i in range(0, len(b), 3000):
    print(b[i:i + 3000])
print("@@FINAL_PDB_GZ_B64_END@@", flush=True)
