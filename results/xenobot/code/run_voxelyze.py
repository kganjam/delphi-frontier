"""Thin runner around the pinned Voxelyze driver. Shells out, parses the driver's
own JSON, caches by argument hash so a re-run is free."""
import json, os, subprocess, hashlib, shutil

BIN = os.environ.get("SOFT_ACTUATION",
                     "/data/scratch/designspaces/xenobot/build/soft_actuation")
CACHE = os.environ.get("VOX_CACHE", "/data/scratch/designspaces/xenobot/data/voxruns")
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]


def run(cap=True, timeout=7200, **kw):
    os.makedirs(CACHE, exist_ok=True)
    args = sorted((k, str(v)) for k, v in kw.items())
    h = hashlib.sha256(repr(args).encode()).hexdigest()[:16]
    tag = os.path.join(CACHE, h)
    if os.path.exists(tag + ".json"):
        with open(tag + ".json") as f:
            d = json.load(f)
        d["_cached"] = True
        return d
    cmd = ([*CAP] if cap else []) + [BIN] + [f"--{k}={v}" for k, v in args] + [f"--out={tag}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0 or not os.path.exists(tag + ".json"):
        raise RuntimeError(f"rc={p.returncode} {p.stdout[-400:]} {p.stderr[-400:]}")
    with open(tag + ".json") as f:
        d = json.load(f)
    d["_cached"] = False
    d["_cmd"] = " ".join(cmd)
    return d


def bl(d):
    return d["result"]["disp_in_body_lengths"]


def net_m(d):
    return d["result"]["net_disp_m"]
