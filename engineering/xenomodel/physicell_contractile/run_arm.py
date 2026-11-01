#!/usr/bin/env python3
"""Run one arm of the PhysiCell contractile-construct protocol and write a receipt.
usage: run_arm.py <binary> <outdir> <dt_mech> KEY=VAL ...   (KEY in XM_* env names)"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
binary, out, dtm = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
env_kv = dict(a.split("=", 1) for a in sys.argv[4:])
out.mkdir(parents=True, exist_ok=True)
here = Path(__file__).resolve().parent
xml = (here / "PhysiCell_settings.xml").read_text()
xml = xml.replace("<folder>output</folder>", f"<folder>{out}</folder>", 1)
xml = xml.replace('<dt_mechanics units="min">0.1</dt_mechanics>', f'<dt_mechanics units="min">{dtm}</dt_mechanics>')
if "XM_MAXTIME" in env_kv:
    xml = xml.replace('<max_time units="min">300</max_time>', f'<max_time units="min">{env_kv["XM_MAXTIME"]}</max_time>')
cfg = out / "settings.xml"; cfg.write_text(xml)
# the binary looks for ./config/cells.csv etc only if enabled; run from build dir
bdir = Path(binary).resolve().parent
env = dict(os.environ, OMP_NUM_THREADS="1", **env_kv)
cmd = ["systemd-run", "--user", "--scope", "-q", "-p", "TasksMax=64", "-p", "MemoryMax=2G", "-p", "MemorySwapMax=0",
       "-p", "RuntimeMaxSec=1800", "--setenv=OMP_NUM_THREADS=1"] + [f"--setenv={k}={v}" for k, v in env_kv.items()] + [str(Path(binary).resolve()), str(cfg)]
t = time.time()
p = subprocess.run(cmd, cwd=bdir, capture_output=True, text=True)
(out / "stdout.log").write_text(p.stdout + p.stderr)
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
rec = {"schema": "claude-xenomodel.physicell-arm-receipt/1", "argv": cmd, "exit": p.returncode, "wall_s": round(time.time() - t, 2),
       "dt_mechanics_min": float(dtm), "params": env_kv, "binary_sha256": sha(binary), "settings_sha256": sha(cfg),
       "custom_cpp_sha256": sha(here / "custom_modules/custom.cpp"), "main_cpp_sha256": sha(here / "main.cpp"),
       "physicell": {"version": "1.14.2", "commit": "dbd3499250141b27600e91e501c54c46f68f2763"},
       "seed": int(env_kv.get("XM_SEED", 0)), "determinism": "no stochastic term is used by this module; OMP_NUM_THREADS=1",
       "com_csv_sha256": sha(out / "xm_com.csv") if (out / "xm_com.csv").exists() else None}
(out / "receipt.json").write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps({"out": str(out), "exit": p.returncode, "wall_s": rec["wall_s"]}))
sys.exit(p.returncode)
