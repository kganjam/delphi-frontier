"""Shared receipts and constants for engineering.neuro. Simulated, not observed."""
from __future__ import annotations
import hashlib, json, os, platform, subprocess, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "artifacts" / "neuro"
G = 9.80665
RHO_W, RHO_A, NU_W, NU_A = 1025.0, 1.204, 1.05e-6, 1.516e-5   # sea water ~25 C; air 20 C (handbook values; M3 uses RHO_A like ff-organ r2)
from engineering.simulation.controlled import RHO as RHO_A_GLIDE   # 1.225: the organism glide model's own air density (M1/M2 use it)

# Organism baseline shared with engineering/simulation/video/manifest.json ("baseline (Fish Cypselurus fit, 0.05 kg)")
ORG = {"m_kg": 0.05, "S_m2": 0.005699061581761254, "AR": 7.8629611627900315, "CL_max": 1.2, "CD0": 0.06, "e": 0.8, "h0_m": 1.0}
# Body length is NOT in that manifest: Fulton condition K = 100 W[g] / L[cm]^3 ~ 1.0 (assumption) -> L = 17.1 cm
L_BODY = round((100 * ORG["m_kg"] * 1e3 / 1.0) ** (1 / 3) / 100, 4)
assert 0.15 < L_BODY < 0.19, L_BODY


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(ROOT))


def inputs(paths):
    return {rel(p): {"sha256": sha(p), "bytes": Path(p).stat().st_size} for p in paths}


def code_hashes(mods):
    files = sorted(set([HERE / "common.py", HERE / "sources.json"] + [HERE / f"{m}.py" for m in mods]))
    return {rel(f): sha(f) for f in files}


def git_head():
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return None


def env():
    import scipy, matplotlib
    return {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
            "platform": platform.platform(), "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS")}


def now():
    t = time.time()
    return {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t)),
            "seattle": time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(t)) if os.environ.get("TZ") else None}


def _default(o):
    if isinstance(o, np.generic):
        return o.item()
    if hasattr(o, "tolist"):
        return o.tolist()
    return str(o)


def dump(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=False, default=_default))
    tmp.replace(path)
    return path


def sources():
    return json.loads((HERE / "sources.json").read_text())
