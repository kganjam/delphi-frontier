#!/usr/bin/env python3
"""Execute a subset of the frozen plan with a receipt per run.
usage: mc_job.py --plan plan.jsonl --runner ./mc_runner --out OUTDIR [--ids a,b] [--groups E1,E2] [--jobs N]
Each run writes OUTDIR/<id>.json (engine output), <id>-com.csv, <id>.pattern.txt and <id>.receipt.json.
Runs whose receipt already shows exit 0 are skipped (resumable)."""
import argparse, concurrent.futures as cf, hashlib, json, os, platform, socket, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mc_patterns as P

def sha(path):
    h = hashlib.sha256(); h.update(open(path, "rb").read()); return h.hexdigest()

def one(r, a):
    out = os.path.join(a.out, r["id"]); rec_p = out + ".receipt.json"
    if os.path.exists(rec_p):
        try:
            if json.load(open(rec_p))["exit_code"] == 0: return r["id"], 0, "skip"
        except Exception: pass
    pat = out + ".pattern.txt"
    meta = P.write(r["spec"], r["mesh"], r["mirror"], pat)
    argv = [a.runner, f"--pattern={pat}", f"--out={out}", f"--dtScale={r['dtScale']}", f"--freq={r['freq']}",
            f"--passive={r['passive']}", f"--zetaGlob={r['zetaGlob']}", f"--zetaInt={r['zetaInt']}"]
    for k, v in sorted(r.get("extra", {}).items()):   # exploratory plans only (not the frozen plan)
        argv.append(f"--{k}={v}")
    if r["id"] in a.dump_ids: argv.append("--dumpEvery=1")
    t0 = time.time()
    env = dict(os.environ, OMP_NUM_THREADS="1")
    p = subprocess.run(argv, capture_output=True, text=True, env=env)
    wall = time.time() - t0
    rec = {"schema": "frontier.run-receipt/1", "run": r, "argv": [os.path.basename(argv[0])] + argv[1:],
           "exit_code": p.returncode, "wall_s": round(wall, 3), "stdout_tail": p.stdout[-400:], "stderr_tail": p.stderr[-400:],
           "pattern": meta, "pattern_file_sha256": meta["sha256"], "seed": meta["seed"],
           "runner_sha256": a.runner_sha, "driver_source_sha256": a.src_sha, "plan_sha256": a.plan_sha,
           "engine": {"name": "Voxelyze", "commit": "4287e365e11416dd108f2f361e9ec4c5a011a16c"},
           "host": socket.gethostname(), "platform": platform.platform(), "compiler": a.cc,
           "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if os.path.exists(out + ".json"): rec["output_sha256"] = sha(out + ".json")
    if os.path.exists(out + "-com.csv"): rec["com_csv_sha256"] = sha(out + "-com.csv")
    json.dump(rec, open(rec_p, "w"), indent=1)
    return r["id"], p.returncode, f"{wall:.1f}s"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--runner", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--ids", default=""); ap.add_argument("--groups", default=""); ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--dump", default=""); ap.add_argument("--shard", default="")  # shard "i/n"
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    plan = [json.loads(l) for l in open(a.plan)]
    if a.ids: plan = [r for r in plan if r["id"] in set(a.ids.split(","))]
    if a.groups: plan = [r for r in plan if r["group"] in set(a.groups.split(","))]
    if a.shard:
        i, n = map(int, a.shard.split("/")); plan = [r for k, r in enumerate(plan) if k % n == i]
    # longest first: mesh^4 * steps
    plan.sort(key=lambda r: -(r["mesh"] ** 4) / r["dtScale"] / r["freq"])
    a.dump_ids = set(filter(None, a.dump.split(",")))
    a.runner = os.path.abspath(a.runner); a.runner_sha = sha(a.runner); a.plan_sha = sha(a.plan)
    a.src_sha = sha(os.path.join(HERE, "mc_runner.cpp"))
    a.cc = subprocess.run(["g++", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    print(f"{len(plan)} runs, {a.jobs} workers", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for fut in cf.as_completed([ex.submit(one, r, a) for r in plan]):
            rid, rc, info = fut.result(); print(f"{time.strftime('%H:%M:%S')} {rid} rc={rc} {info}", flush=True)
