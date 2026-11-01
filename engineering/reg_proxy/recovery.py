"""One missing-only recovery run for the five libraries whose index request failed in v1 (recovery_contract.json, frozen first).

Same windows, count rule and summary rule as v1; only the index retry schedule, header/timing logging and the empty-206
classification differ. The cause of the v1 failure is unknown and the schedule is an experimental transport repair."""
import hashlib
import json
import os
import sys
import time

from engineering.reg_proxy import window_count as wc

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT_RESULTS_SHA = "f2eb5178787e371cb53f58f4b725feaa8a2f26ae4df5e4c0f2b99b776a31ac8a"  # restated from the contract on purpose


def sha(name):
    return hashlib.sha256(open(os.path.join(HERE, name), "rb").read()).hexdigest()


def load():
    proto, ctl = wc.load()
    contract = json.load(open(os.path.join(HERE, "recovery_contract.json")))
    assert contract["parent"]["results_sha256"] == PARENT_RESULTS_SHA
    labels = contract["scope"]["libraries"]
    libs = [lib for lib in ctl["libraries"] if lib["label"] in labels]
    if [lib["label"] for lib in libs] != labels:
        raise SystemExit("recovery scope does not match controls.json libraries")
    b = contract["bounds"]
    proto_r = proto | {"bounds": proto["bounds"] | {"total_requests_max": b["requests_max"], "total_compressed_max_bytes": b["charged_bytes_max"],
                                                   "per_library_compressed_max_bytes": b["per_library_bytes_max"], "per_window_compressed_max_bytes": b["per_window_bytes_max"],
                                                   "index_download_max_bytes": b["index_max_bytes"], "runtime_hard_s": b["runtime_hard_s"]}}
    return proto_r, ctl | {"libraries": libs}, contract


def run_recovery(out, proto_r, ctl, contract, make_fetch, clock=time.monotonic, budget=None):
    waits = contract["transport"]["index_schedule"]["wait_before_attempt_s"]
    extra = {"schema": "frontier.reg-proxy.recovery-receipt/1", "contract_sha256": sha("recovery_contract.json"), "parent_results_sha256": PARENT_RESULTS_SHA,
             "scope_libraries": [lib["label"] for lib in ctl["libraries"]], "index_schedule_s": waits, "cause_of_original_failure": "UNKNOWN"}
    return wc.run(out, proto_r, ctl, make_fetch, clock=clock, budget=budget, index_schedule=waits, extra_receipt=extra)


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    from engineering.reg_proxy import controls_recovery, controls_synth
    if "--preflight" in a:
        r = {"v1_controls": controls_synth.run_all(), "recovery_controls": controls_recovery.run_all()}
        print(json.dumps(r, indent=1))
        return 0 if all(c["passed"] for k in r.values() for c in k["controls"]) else 1
    if "--run" in a:
        out = a[a.index("--out") + 1] if "--out" in a else os.environ.get("COPS_OUT")
        if not out:
            raise SystemExit("--out or $COPS_OUT required")
        pre = [c for m in (controls_synth, controls_recovery) for c in m.run_all()["controls"]]
        if not all(c["passed"] for c in pre):
            raise SystemExit("preflight controls failed; refusing to read targets")
        proto_r, ctl, contract = load()
        log = []
        doc, rec = run_recovery(out, proto_r, ctl, contract, wc.http_fetch_factory(proto_r, log, recovery=True))
        json.dump(log, open(os.path.join(out, "requests.json"), "w"), indent=1)
        print(json.dumps(rec, indent=1))
        return wc.EXIT_CODES[rec["completion_status"]]
    raise SystemExit("usage: --preflight | --run [--out DIR]")


if __name__ == "__main__":
    sys.exit(main())
