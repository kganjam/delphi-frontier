"""Independent audit of a returned GSE261907 control-window run (criteria: return_audit_criteria.json, frozen first).

Reads results.json / receipt.json / requests.json and the pinned controls.json. Makes no network request and imports
nothing from window_count.py: windows, identities, completion status, budgets and the summary are recomputed here."""
import hashlib
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PIN = {"protocol_sha256": "7a2ec7be0132fe77140ad3647e229400affe74698f53d4b059954e35dc723dc5",
       "amendment_sha256": "048e4745f78462a43bf6790a8d7d8a528f4b9c81cb10c0cfbd41d037e5657637",
       "amendment2_sha256": "69e4d1bcb7dbcd16969bda58de962d5db32a3aba1873ee0cb3c04be68d13d5cc"}
FILES = {"results.json", "receipt.json", "requests.json"}
STATUSES = {"ok", "beyond_last_interval", "chrom_absent", "unsorted_refused", "window_byte_cap", "library_byte_cap", "library_unavailable",
            "stopped_on_bound", "truncated_bgzf", "index_file_mismatch", "bad_bgzf", "transport_error", "unsupported_range",
            "range_mismatch", "short_read", "oversized_response"}
USABLE = {"ok", "beyond_last_interval"}
FORBIDDEN_KEYS = {"probability", "confidence", "score", "pvalue", "p_value", "rank", "threshold", "significant"}
HOST = "ftp.ncbi.nlm.nih.gov"


def expected_windows(controls):
    out = []
    for c in controls["controls"]:
        a, b = c["start_1based"] - 1, c["end_1based"]
        out.append((c["name"], c["class"], c["chrom"], a, b))
        for off in (250000, 500000):
            out.append((f"{c['name']}+{off}", "comparison", c["chrom"], a + off, b + off))
    return out


def keys_in(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from keys_in(v)
    elif isinstance(o, list):
        for v in o:
            yield from keys_in(v)


def audit(d, controls=None, host_prefix=f"https://{HOST}/", n_expected=330):
    controls = controls or json.load(open(os.path.join(HERE, "controls.json")))
    checks, obs = [], {}

    def chk(cid, ok, detail):
        checks.append({"id": cid, "passed": bool(ok), "detail": detail})

    names = set(os.listdir(d))
    sizes = sum(os.path.getsize(os.path.join(d, n)) for n in names)
    chk("C1_files", names == FILES and sizes <= 52428800, f"files={sorted(names)} bytes={sizes}")
    if not FILES <= names:
        return {"checks": checks, "verdict": "inconsistent", "observations": obs}
    raw = open(os.path.join(d, "results.json"), "rb").read()
    res, rec = json.loads(raw), json.load(open(os.path.join(d, "receipt.json")))
    reqs = json.load(open(os.path.join(d, "requests.json")))
    rows = res["windows"]

    bad = [k for k, want in PIN.items() if rec.get(k) != want]
    chk("C2_pins", rec.get("results_sha256") == hashlib.sha256(raw).hexdigest() and not bad, f"results hash match={rec.get('results_sha256') == hashlib.sha256(raw).hexdigest()}; pin mismatches={bad}")

    exp_w = expected_windows(controls)
    exp_ids = {(lib["label"], w[0]): w for lib in controls["libraries"] for w in exp_w}
    got = [(r["library"], r["window"]) for r in rows]
    dup = len(got) - len(set(got))
    missing = sorted(set(exp_ids) - set(got))
    extra = sorted(set(got) - set(exp_ids))
    geom = [k for r in rows if (k := (r["library"], r["window"])) in exp_ids and
            (r["chrom"], r["start0"], r["end0"], r["kind"]) != (exp_ids[k][2], exp_ids[k][3], exp_ids[k][4], exp_ids[k][1])]
    chk("C3_identities", len(exp_ids) == n_expected and not dup and not missing and not extra and not geom,
        f"expected={len(exp_ids)} present={len(set(got))} duplicates={dup} missing={len(missing)} extra={len(extra)} geometry_mismatch={len(geom)}")

    problems = []
    for r in rows:
        k = (r["library"], r["window"])
        if r["status"] not in STATUSES:
            problems.append((k, "status", r["status"]))
        elif r["status"] in USABLE:
            n, dd, bc = r.get("fragment_rows"), r.get("dup_count_sum"), r.get("distinct_barcodes")
            if not all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in (n, dd, bc)) or dd < n or bc > n:
                problems.append((k, "counts", (n, dd, bc)))
        elif any(x in r for x in ("fragment_rows", "dup_count_sum", "distinct_barcodes")) and r["status"] not in ("window_byte_cap",):
            problems.append((k, "counts_on_unusable", r["status"]))
    chk("C4_rows", not problems, f"{len(problems)} problems; first={problems[:3]}")

    present, usable = set(got), {(r["library"], r["window"]) for r in rows if r["status"] in USABLE}
    status = ("stopped_on_error" if rec.get("error") else "stopped_on_bound" if rec.get("stop_detail") else
              "complete" if present == set(exp_ids) and usable == present else "partial_data")
    unusable = sorted(present - usable)
    chk("C5_completion", status == res["completion_status"] == rec["completion_status"]
        and (rec["expected_identities"], rec["present_identities"], rec["usable_identities"]) == (len(exp_ids), len(present), len(usable))
        and sorted(map(tuple, rec["unusable_identities"])) == unusable and sorted(map(tuple, rec["missing_identities"])) == missing,
        f"recomputed={status} results={res['completion_status']} receipt={rec['completion_status']}; present={len(present)} usable={len(usable)}")

    url_lib = {}
    sizes_by_url = {}
    for lib in controls["libraries"]:
        for u, n in ((lib["fragments_url"], lib["fragments_bytes"]), (lib["index_url"], lib["index_bytes"])):
            url_lib[u], sizes_by_url[u] = lib["label"], n
    bp, per_lib, tot = [], defaultdict(int), 0
    for q in reqs:
        tot += q.get("bytes_charged", 0)
        if q["url"] in url_lib:
            per_lib[url_lib[q["url"]]] += q.get("bytes_charged", 0)
        if q["url"] not in url_lib or not q["url"].startswith(host_prefix):
            bp.append(("url", q["url"]))
            continue
        a, b = map(int, q["range"].split("-"))
        if not 0 <= a <= b < sizes_by_url[q["url"]]:
            bp.append(("range", q["range"]))
        if q.get("ok"):
            if q.get("http_status") != 206 or q.get("bytes") != b - a + 1 or not q.get("sha256"):
                bp.append(("ok_fields", q["range"]))
        elif not q.get("failure"):
            bp.append(("failure_unrecorded", q["range"]))
    prev = None  # attempts are read in log order: a request starts at 1; attempt 2 only follows a failed attempt 1 of the same url and range
    for q in reqs:
        n = q.get("attempt")
        if n == 1:
            pass
        elif not (n == 2 and prev and prev["attempt"] == 1 and not prev.get("ok") and (prev["url"], prev["range"]) == (q["url"], q["range"])):
            bp.append(("attempts", q["range"], n))
        prev = q
    win_over = [r for r in rows if r.get("window_bytes_charged", 0) > 8388608]
    chk("C6_budget", not bp and len(reqs) == rec["requests"] <= 3000 and tot == rec["compressed_bytes"] <= 419430400
        and max(per_lib.values(), default=0) <= 67108864 and not win_over and rec["elapsed_s"] <= 1200,
        f"requests={len(reqs)} (receipt {rec['requests']}) charged={tot} (receipt {rec['compressed_bytes']}) max_library={max(per_lib.values(), default=0)} "
        f"elapsed_s={rec['elapsed_s']} problems={bp[:3]}")
    oks = {(q["range"], q["sha256"]) for q in reqs if q.get("ok")}
    unlinked = [(r["library"], r["window"], x["range"]) for r in rows for x in r.get("responses", []) if (x["range"], x["sha256"]) not in oks]
    chk("C6b_linkage", not unlinked, f"{sum(len(r.get('responses', [])) for r in rows)} responses; unlinked={len(unlinked)} {unlinked[:2]}")

    by = {(r["library"], r["window"]): r for r in rows}
    want = []
    for r in rows:
        if r["kind"] == "comparison":
            continue
        s = {"library": r["library"], "window": r["window"], "kind": r["kind"], "status": r["status"]}
        if r["status"] in USABLE:
            comp = [by.get((r["library"], f"{r['window']}+{o}")) for o in (250000, 500000)]
            cc = [c["fragment_rows"] for c in comp if c and c["status"] in USABLE]
            mean = (cc[0] + cc[1]) / 2 if len(cc) == 2 else None
            s.update(fragment_rows=r["fragment_rows"], per_kb=round(r["fragment_rows"] / ((r["end0"] - r["start0"]) / 1000), 4),
                     comparison_counts=cc, ratio_to_comparison_median=round(r["fragment_rows"] / mean, 4) if mean else None)
        want.append(s)
    chk("C7_summary", want == res["summary"], f"{len(want)} recomputed summary rows; equal={want == res['summary']}")

    lim = res.get("claim_limits", "")
    badk = sorted(set(keys_in(res)) & FORBIDDEN_KEYS)
    chk("C8_claims", "not function" in lim and not badk, f"claim_limits ok={'not function' in lim}; forbidden keys={badk}")
    chk("C9_scope", not any("LEN" in w[1] or "lepb" in w[1].lower() for w in got) and not any("lepb" in r["window"].lower() or "LEN" in r["window"] for r in rows), "no LEN/lepb identity")

    sc = defaultdict(lambda: defaultdict(int))
    for r in rows:
        sc[r["library"]][r["status"]] += 1
    obs["status_counts_per_library"] = {k: dict(v) for k, v in sc.items()}
    obs["unusable_identities"] = [list(x) for x in unusable]
    obs["positives_with_zero_fragments"] = sorted(f"{r['library']}:{r['window']}" for r in rows if r["kind"] == "reporter_positive" and r.get("fragment_rows") == 0)
    obs["undefined_ratio_windows"] = sum(1 for s in want if s.get("status") in USABLE and s.get("ratio_to_comparison_median") is None)
    obs["fragment_rows_by_library"] = {lib["label"]: {r["window"]: r["fragment_rows"] for r in rows if r["library"] == lib["label"] and r["kind"] != "comparison" and "fragment_rows" in r}
                                       for lib in controls["libraries"]}
    ok = all(c["passed"] for c in checks)
    return {"schema": "frontier.reg-proxy.return-audit/1", "checks": checks, "observations": obs,
            "verdict": "consistent" if ok else "inconsistent",
            "meaning": "consistent = the returned files agree with the frozen protocol and each other; it is not biological validation and not an independent measurement of the counts"}


def transport_diagnosis(reqs, controls=None):
    """Describe failed attempts from requests.json alone: which files and ranges, status, bytes, timing. States no cause."""
    controls = controls or json.load(open(os.path.join(HERE, "controls.json")))
    idx_urls = {lib["index_url"]: lib["label"] for lib in controls["libraries"]}
    sizes = {lib["index_url"]: lib["index_bytes"] for lib in controls["libraries"]}
    t0 = reqs[0]["t"] if reqs else 0
    fails = [q for q in reqs if not q.get("ok")]
    def full_index(q):
        return q["url"] in idx_urls and q["range"] == f"0-{sizes[q['url']] - 1}"
    ok_after = [q for q in reqs if q.get("ok")]
    return {
        "attempts": len(reqs), "failed_attempts": len(fails),
        "failure_signatures": sorted({(q.get("failure"), q.get("http_status"), q.get("bytes_charged")) for q in fails}, key=str),
        "failed_are_all_full_index_range_requests": all(full_index(q) for q in fails),
        "failed_by_library": {lab: [round(q["t"] - t0, 2) for q in fails if idx_urls.get(q["url"]) == lab] for lab in dict.fromkeys(idx_urls.values())
                              if any(idx_urls.get(q["url"]) == lab for q in fails)},
        "index_outcome_by_library": {lab: ("ok" if any(q.get("ok") and idx_urls.get(q["url"]) == lab for q in reqs) else "failed") for lab in dict.fromkeys(idx_urls.values())},
        "last_failure_s": round(max((q["t"] for q in fails), default=t0) - t0, 2),
        "first_success_s": round(min((q["t"] for q in ok_after), default=t0) - t0, 2),
        "non_index_requests_failed": sum(1 for q in fails if q["url"] not in idx_urls),
        "non_index_requests_ok": sum(1 for q in ok_after if q["url"] not in idx_urls),
        "gap_before_second_attempt_s": [round(b["t"] - a["t"], 2) for a, b in zip(reqs, reqs[1:]) if a["attempt"] == 1 and b["attempt"] == 2],
        "not_logged": ["response headers (Content-Length, Content-Range value, Connection, Age, cache headers)", "whether the connection closed early or declared length 0", "per-request wall time"],
        "cause": "not determined by this log",
    }


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        raise SystemExit("usage: audit_return DIR [--diagnose]")
    if "--diagnose" in a:
        print(json.dumps(transport_diagnosis(json.load(open(os.path.join(a[0], "requests.json")))), indent=1, sort_keys=True))
        return 0
    r = audit(a[0])
    print(json.dumps(r, indent=1, sort_keys=True))
    return 0 if r["verdict"] == "consistent" else 1


if __name__ == "__main__":
    sys.exit(main())
