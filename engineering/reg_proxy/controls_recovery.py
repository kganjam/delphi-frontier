"""Controls for the missing-only recovery transport: exact empty-206 fixtures, schedule/runtime behaviour on an injected clock
(no real sleeping, no load), allow-listed header logging, charging, and an end-to-end recovery run against a local Range server.
Same parser, counter and transport classes as the remote run."""
import hashlib
import json
import os
import tempfile

from engineering.reg_proxy import controls_synth as cs
from engineering.reg_proxy import recovery as rc
from engineering.reg_proxy import window_count as wc

HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS = ("SECRET-COOKIE-VALUE", "SECRET-TOKEN", "SECRET-X", "session=")


class FakeClock:
    """Deterministic clock; sleeping advances it and records the wait. Nothing really sleeps."""

    def __init__(self):
        self.t, self.sleeps = 1000.0, []

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


def _ctl(name, fn):
    try:
        return {"control": name, "passed": True, "detail": fn()}
    except AssertionError as e:
        return {"control": name, "passed": False, "detail": f"assertion failed: {e}"}
    except Exception as e:
        return {"control": name, "passed": False, "detail": f"{type(e).__name__}: {e}"}


def run_all():
    proto_r, ctl_real, contract = rc.load()
    recs = cs.synth_records()
    frag, tbi, _ = cs.make_fixture(recs)
    total = len(frag)
    srv = cs.Server({"/a.gz": frag, "/a.tbi.gz": tbi})
    out = []
    WAITS = contract["transport"]["index_schedule"]["wait_before_attempt_s"]

    def http(clock=None, recovery=True, bounds=None, log=None):
        clock = clock or FakeClock()
        pr = proto_r if bounds is None else proto_r | {"bounds": proto_r["bounds"] | bounds}
        bud = wc.Budget(pr["bounds"], clock.now)
        h = wc.HttpRange(pr, bud, [srv.host], "http", log=log if log is not None else [], sleep=clock.sleep, recovery=recovery)
        return h, bud, clock

    def mode(m, n=0):
        srv.mode, srv.empty_first, srv.extra_headers = m, n, False

    try:
        def empty206(m, label):
            def f():
                mode(m)
                log = []
                h, bud, ck = http(log=log)
                try:
                    h.get(srv.url("/a.tbi.gz"), 0, len(tbi) - 1, len(tbi), schedule=WAITS)
                except wc.Refused as e:
                    assert e.status == "empty_206", e.status
                    assert [x["attempt"] for x in log] == [1, 2, 3] and all(x["failure"] == "empty_206" and x["http_status"] == 206 for x in log), log
                    assert bud.bytes == 0 and bud.requests == 3 and ck.sleeps == [15, 45], (bud.bytes, bud.requests, ck.sleeps)
                    assert log[0]["headers"]["Content-Range"] == f"bytes 0-{len(tbi) - 1}/{len(tbi)}", log[0]["headers"]
                    assert log[0]["headers"]["Content-Length"] == ("0" if m.endswith("declared0") else str(len(tbi))), log[0]["headers"]
                    return f"{label}: classified empty_206 on 3 attempts, waits 15 and 45 s on the injected clock, 0 bytes charged, no 4th attempt"
                finally:
                    mode("ok")
                raise AssertionError("empty 206 accepted")
            return f
        out.append(_ctl("exact empty 206: Content-Length N, zero bytes delivered", empty206("empty_206", "headers promise N bytes, none sent")))
        out.append(_ctl("exact empty 206: Content-Length 0", empty206("empty_206_declared0", "headers declare length 0")))

        def short_stays_short():
            mode("short")
            h, bud, ck = http()
            try:
                h.get(srv.url("/a.gz"), 0, 99, total)
            except wc.Refused as e:
                assert e.status == "short_read" and bud.bytes == 198, (e.status, bud.bytes)
                return "a body of N-1 bytes stays short_read (not empty_206); both attempts charged (198)"
            finally:
                mode("ok")
            raise AssertionError("short body accepted")
        out.append(_ctl("only a zero-byte body is empty_206", short_stays_short))

        def schedule_success():
            mode("ok", n=2)
            log = []
            h, bud, ck = http(log=log)
            body = h.get(srv.url("/a.tbi.gz"), 0, len(tbi) - 1, len(tbi), schedule=WAITS)
            mode("ok")
            assert body == tbi and ck.sleeps == [15, 45] and [x["wait_before_s"] for x in log] == [0, 15, 45], (ck.sleeps, log)
            assert [x["ok"] for x in log] == [False, False, True] and bud.bytes == len(tbi)
            return "two empty 206 then success on attempt 3: waits 0/15/45 honoured on the injected clock, only the good body is charged"
        out.append(_ctl("0/15/45 schedule: success on the third attempt", schedule_success))

        def runtime_bound():
            mode("empty_206")
            h, bud, ck = http(bounds={"runtime_hard_s": 50})
            try:
                h.get(srv.url("/a.tbi.gz"), 0, len(tbi) - 1, len(tbi), schedule=WAITS)
            except wc.Refused as e:
                assert e.status == "stopped_on_bound" and ck.sleeps == [15], (e.status, ck.sleeps)  # 15+45 would pass 50: never sleeps past the bound
                return "a wait that would pass the runtime bound is not taken: stopped_on_bound after sleeping 15 s only"
            finally:
                mode("ok")
            raise AssertionError("slept past the runtime bound")
        out.append(_ctl("schedule never sleeps past the runtime bound", runtime_bound))

        def window_unchanged():
            mode("empty_206")
            h, bud, ck = http()
            try:
                h.get(srv.url("/a.gz"), 0, 99, total)
            except wc.Refused as e:
                assert e.status == "empty_206" and bud.requests == 2 and ck.sleeps == [], (bud.requests, ck.sleeps)
                return "window reads keep the frozen 2 attempts with no wait"
            finally:
                mode("ok")
            raise AssertionError("empty window read accepted")
        out.append(_ctl("window attempts are unchanged (2, no wait)", window_unchanged))

        def reservation():
            before = len(srv.paths)
            h, bud, ck = http(bounds={"per_window_compressed_max_bytes": 100})
            try:
                h.get(srv.url("/a.gz"), 0, 99, total, schedule=WAITS)
                raise AssertionError("a 100-byte request was sent against a 100-byte cap")
            except wc.Refused as e:
                assert e.status == "window_byte_cap" and len(srv.paths) == before, (e.status, len(srv.paths) - before)
            mode("short")
            h, bud, ck = http(bounds={"per_library_compressed_max_bytes": 150, "per_window_compressed_max_bytes": 150})
            try:
                before = len(srv.paths)
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total, schedule=WAITS)
                except wc.Refused as e:
                    assert e.status == "library_byte_cap" and len(srv.paths) - before == 1 and bud.bytes == 99, (e.status, len(srv.paths) - before, bud.bytes)
                    return "recovery transport reserves expected+1 per attempt: 100 B vs a 100 B cap is refused unsent; a second attempt that could pass 150 B is refused unsent"
            finally:
                mode("ok")
            raise AssertionError("cap exceeded")
        out.append(_ctl("reservation and failed-byte charging hold in recovery mode", reservation))

        def headers():
            mode("ok")
            srv.extra_headers = True
            log = []
            h, bud, ck = http(log=log)
            try:
                h.get(srv.url("/a.gz"), 0, 99, total)
            finally:
                srv.extra_headers = False
            hd = log[0]["headers"]
            assert set(hd) <= set(wc.ALLOWED_HEADERS) and {"Content-Length", "Content-Range", "ETag", "Last-Modified", "Accept-Ranges", "Content-Type", "Date"} <= set(hd), sorted(hd)
            blob = json.dumps(log)
            assert not any(sct in blob for sct in SECRETS), "a secret header value reached the log"
            assert hd["ETag"] == '"abc123"' and hd["Content-Range"] == f"bytes 0-99/{total}"
            return f"only allow-listed headers logged ({sorted(hd)}), verbatim; Set-Cookie, Authorization and X-Secret values never appear"
        out.append(_ctl("header allow-list (no secrets logged)", headers))

        def v1_compat():
            mode("empty_206")
            log = []
            h, bud, ck = http(log=log, recovery=False)
            try:
                h.get(srv.url("/a.gz"), 0, 99, total)
            except wc.Refused as e:
                assert e.status == "short_read" and "headers" not in log[0] and "elapsed_s" not in log[0], (e.status, log[0])
                return "without recovery mode the frozen v1 behaviour is unchanged (short_read, no extra log fields)"
            finally:
                mode("ok")
            raise AssertionError("accepted")
        out.append(_ctl("v1 transport behaviour unchanged by default", v1_compat))

        def end_to_end():
            ck = FakeClock()
            ctl2 = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [{"gsm": "GSMrA", "label": "rA", "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)},
                                  {"gsm": "GSMrB", "label": "rB", "dpa": 0, "replicate": 2, "fragments_url": srv.url("/b.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/b.tbi.gz"), "index_bytes": len(tbi)}]}
            srv.files["/b.gz"], srv.files["/b.tbi.gz"] = frag, tbi
            mode("ok", n=2)  # library rA's index: two empty 206 then success
            log = []
            bud = wc.Budget(proto_r["bounds"], ck.now)
            # rB is served after rA; make its index permanently empty by switching mode when rA is done
            base = wc.http_fetch_factory(proto_r, log, [srv.host], "http", sleep=ck.sleep, recovery=True)

            def make(url, total_, b):
                if "/b." in url:
                    srv.mode, srv.empty_first = "empty_206", 0
                return base(url, total_, b)
            doc, rec = rc.run_recovery(os.path.join(tempfile.mkdtemp(), "o"), proto_r, ctl2, contract, make, clock=ck.now, budget=bud)
            mode("ok")
            st = {(r["library"], r["window"]): r["status"] for r in doc["windows"]}
            assert st[("rA", "fx")] == "ok" and st[("rB", "fx")] == "library_unavailable", st
            assert rec["completion_status"] == "partial_data" and rec["usable_identities"] == 3 and rec["unusable_identities"] == [["rB", "fx"], ["rB", "fx+250000"], ["rB", "fx+500000"]], rec
            b_paths = [p for p in srv.paths if p.startswith("/b.")]
            assert b_paths == ["/b.tbi.gz"] * 3, b_paths  # three index attempts, no window request for the failed library
            assert ck.sleeps == [15, 45, 15, 45], ck.sleeps
            assert rec["contract_sha256"] == rc.sha("recovery_contract.json") and rec["parent_results_sha256"] == rc.PARENT_RESULTS_SHA and rec["cause_of_original_failure"] == "UNKNOWN"
            return "A recovers on attempt 3 and is counted; B stays library_unavailable after 3 index attempts with no window request; partial_data; receipt pins contract and parent sha, cause UNKNOWN"
        out.append(_ctl("end-to-end recovery keeps a still-failing library unresolved", end_to_end))

        def scope():
            assert [lib["label"] for lib in ctl_real["libraries"]] == ["0dpa1", "0dpa2", "1dpa1", "1dpa2", "2dpa1"]
            assert len(wc.build_windows(ctl_real["controls"])) * len(ctl_real["libraries"]) == 165
            b = proto_r["bounds"]
            assert (b["total_requests_max"], b["total_compressed_max_bytes"], b["runtime_hard_s"]) == (1000, 157286400, 900) and 900 * 0 + b["per_window_compressed_max_bytes"] == 8388608
            assert contract["transport"]["index_schedule"]["wait_before_attempt_s"] == [0, 15, 45]
            assert hashlib.sha256(open(os.path.join(HERE, "protocol.json"), "rb").read()).hexdigest() == "7a2ec7be0132fe77140ad3647e229400affe74698f53d4b059954e35dc723dc5"
            return "scope is exactly the five missing libraries (165 identities); bounds 1000 requests / 157,286,400 B / 900 s; schedule 0/15/45; science protocol hash unchanged"
        out.append(_ctl("recovery scope and bounds equal the contract", scope))
    finally:
        srv.close()
    return {"schema": "frontier.reg-proxy.controls-run/1", "contract_sha256": rc.sha("recovery_contract.json"), "controls": out}


if __name__ == "__main__":
    r = run_all()
    print(json.dumps(r, indent=1))
    raise SystemExit(0 if all(c["passed"] for c in r["controls"]) else 1)
