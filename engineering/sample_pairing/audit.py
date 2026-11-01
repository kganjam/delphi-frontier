"""GSE261907 RNA/ATAC library-pairing audit from GEO sample metadata. Standard library only.

    python -m engineering.sample_pairing.audit --preflight                 # offline: controls + code/protocol hashes
    python -m engineering.sample_pairing.audit --run --out DIR             # DIR must not exist (or $COPS_OUT)

The rules are frozen in protocol.json before any new retrieval. The same parse/pair/fetch functions run in the
tests, in --preflight and in --run. Cell barcodes are never read; shared barcode strings imply nothing.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_PATH = os.path.join(HERE, "protocol.json")
RESULTS_SCHEMA = "frontier.sample-pairing.results/1"
STRATEGIES = {"RNA-Seq": "rna", "ATAC-seq": "atac"}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def load_protocol(path=PROTOCOL_PATH):
    raw = open(path, "rb").read()
    return json.loads(raw), sha256(raw)


def parse_soft(text):
    """GEO SOFT text -> {field: [values]} for '!Field = value' lines; also the '^ENTITY = acc' header."""
    out, head = {}, None
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("^") and " = " in line:
            head = line[1:].split(" = ", 1)
        elif line.startswith("!") and " = " in line:
            k, v = line[1:].split(" = ", 1)
            out.setdefault(k.strip(), []).append(v.strip())
    return {"head": head, "fields": out}


def _norm_assembly(a, aliases):
    a = a.strip().lower()
    for group in aliases:
        if a in group:
            return group[0]
    return a


def sample_record(acc, parsed, proto):
    """One library's identity fields, with problems split into `missing` and `conflicts` (never guessed)."""
    f = parsed["fields"]
    r = {"gsm": acc, "missing": [], "conflicts": []}
    if not parsed["head"] or parsed["head"][0] != "SAMPLE" or parsed["head"][1] != acc:
        r["missing"].append("header_mismatch")
    one = lambda k: (f.get(k) or [None])[0]  # noqa: E731
    r["title"] = one("Sample_title")
    strat = one("Sample_library_strategy")
    r["strategy"] = STRATEGIES.get(strat)
    if r["strategy"] is None:
        r["missing"].append(f"unsupported_or_absent_library_strategy:{strat}")
    r["organism"] = one("Sample_organism_ch1")
    if r["organism"] != "Danio rerio":
        r["missing"].append(f"organism:{r['organism']}")
    chars = f.get("Sample_characteristics_ch1", [])
    tissue = [c.split(": ", 1)[1] for c in chars if c.lower().startswith("tissue: ")]
    times = [c.split(": ", 1)[1] for c in chars if re.match(r"time post_amputation_\(days\): ", c)]
    r["tissue"] = tissue[0] if len(tissue) == 1 else None
    r["time_dpa"] = times[0] if len(times) == 1 and re.fullmatch(r"\d+", times[0]) else None
    if r["tissue"] is None:
        r["missing"].append("tissue")
    if r["time_dpa"] is None:
        r["missing"].append("time_characteristic")
    t = r["title"] or ""
    rep = re.findall(r"\brep(\d+)\b", t)
    r["rep"] = rep[0] if len(rep) == 1 else None
    if r["rep"] is None:
        r["missing"].append("replicate_token")
    dpa = re.findall(r"(\d+)\s*dpa", t)
    if dpa and r["time_dpa"] is not None and dpa[0] != r["time_dpa"]:
        r["conflicts"].append(f"title_dpa {dpa[0]} != characteristic {r['time_dpa']}")
    bios = sorted({m for v in f.get("Sample_relation", []) for m in re.findall(r"BioSample: https://www\.ncbi\.nlm\.nih\.gov/biosample/(SAMN\d+)$", v)})
    r["biosample"] = bios[0] if len(bios) == 1 else None
    if len(bios) != 1:
        r["missing"].append(f"biosample_count:{len(bios)}")
    asm = sorted({m.lower() for v in f.get("Sample_data_processing", []) for m in re.findall(r"^Assembly:\s*(\S+)$", v)})
    r["assembly_declared"] = asm
    if len(asm) == 1:
        r["assembly"] = _norm_assembly(asm[0], proto["assembly_aliases"])
    else:
        r["assembly"] = None
        r["missing" if not asm else "conflicts"].append(f"assembly_lines:{asm}")
    return r


def pair(records):
    """Pair RNA and ATAC libraries through a shared BioSample. Returns (pairs, record_status)."""
    status, pairs = {}, []
    by_bio = {}
    for r in records:
        if r["conflicts"]:
            status[r["gsm"]] = ("unresolved_conflict", r["conflicts"])
        if r["missing"]:
            status.setdefault(r["gsm"], ("unresolved_missing_identity", r["missing"]))
        elif r["biosample"]:
            by_bio.setdefault(r["biosample"], []).append(r)
    labels = {}
    for r in records:
        if r["strategy"] and r["time_dpa"] is not None and r["rep"] is not None and r["biosample"]:
            labels.setdefault((r["strategy"], r["time_dpa"], r["rep"]), set()).add(r["biosample"])
    reused = {k for k, v in labels.items() if len(v) > 1}
    for bio, rs in sorted(by_bio.items()):
        rna = [r for r in rs if r["strategy"] == "rna"]
        atac = [r for r in rs if r["strategy"] == "atac"]
        entry = {"biosample": bio, "rna": [r["gsm"] for r in rna], "atac": [r["gsm"] for r in atac], "reasons": []}
        if len(rna) > 1 or len(atac) > 1:
            entry["status"] = "unresolved_ambiguous"
            entry["reasons"].append("more than one library of one strategy shares this BioSample")
        elif not rna or not atac:
            entry["status"] = "unresolved_missing_identity"
            entry["reasons"].append("no counterpart library of the other strategy")
        else:
            a, b = rna[0], atac[0]
            diff = [k for k in ("time_dpa", "rep", "tissue", "organism") if a[k] != b[k]]
            lab = [(r["strategy"], r["time_dpa"], r["rep"]) for r in (a, b) if (r["strategy"], r["time_dpa"], r["rep"]) in reused]
            if diff or lab or a["conflicts"] or b["conflicts"]:
                entry["status"] = "unresolved_conflict"
                entry["reasons"] += [f"{k} differs: {a[k]} vs {b[k]}" for k in diff] + [f"label reused across BioSamples: {x}" for x in lab] + a["conflicts"] + b["conflicts"]
            elif a["assembly"] != b["assembly"]:
                entry["status"] = "assembly_mismatch"
                entry["reasons"].append(f"assembly {a['assembly']} vs {b['assembly']}")
            else:
                entry.update(status="matched", time_dpa=a["time_dpa"], rep=a["rep"], tissue=a["tissue"], assembly=a["assembly"])
        for r in rs:
            status[r["gsm"]] = (entry["status"], entry["reasons"])
        pairs.append(entry)
    return pairs, status


def summarize(records, pairs, status):
    counts = {}
    for p in pairs:
        counts[p["status"]] = counts.get(p["status"], 0) + 1
    rec_counts = {}
    for r in records:
        s = status.get(r["gsm"], ("unresolved_missing_identity", []))[0]
        rec_counts[s] = rec_counts.get(s, 0) + 1
    return {"libraries_admitted": len(records), "biosample_groups": len(pairs), "pair_status_counts": counts, "library_status_counts": rec_counts,
            "distinct_biosamples_declared": len({r["biosample"] for r in records if r["biosample"]}),
            "matched_biosamples": [p["biosample"] for p in pairs if p["status"] == "matched"],
            "cell_level_pairing": "unresolved: not examined (no barcode file retrieved; shared barcode strings imply nothing)",
            "animal_identity": "unknown: GEO metadata does not state whether replicates are separate animals"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        raise urllib.error.HTTPError(a[0].full_url, a[3], "redirect refused by protocol", a[4], None)


def url_for(acc, proto):
    ok = acc == proto["retrieval"]["series_accession"] or re.fullmatch(proto["retrieval"]["gsm_pattern"], acc)
    assert ok, f"{acc}: not the series and not a GSM accession"
    u = proto["retrieval"]["url_templates"][0].format(ACC=acc)
    assert urllib.parse.urlparse(u).hostname in proto["retrieval"]["allowed_hosts"]
    return u


def fetch(acc, proto, opener=None):
    """One bounded GET. Returns (bytes, status_code). Raises on redirect, oversize or non-allowlisted host."""
    cap = proto["retrieval"]["max_bytes_per_response"]
    op = opener or urllib.request.build_opener(NoRedirect)
    with op.open(urllib.request.Request(url_for(acc, proto), headers={"User-Agent": "frontier-sample-pairing/1"}), timeout=30) as r:
        data = r.read(cap + 1)
        if len(data) > cap:
            raise OverflowError(f"{acc}: response exceeds {cap} bytes")
        return data, r.status


def run(out, proto, proto_sha, fetcher=fetch, clock=time.time, sleep=time.sleep):
    """Retrieve, parse, pair, write. Stops (never expands) on any bound or error and says so in completion_status."""
    if os.path.exists(out):
        raise FileExistsError(f"{out} exists; the collector refuses to overwrite or repeat retrieval")
    os.makedirs(os.path.join(out, "raw"))
    R = proto["retrieval"]
    t0 = clock()
    reqs, errors, records, total, status = [], [], [], 0, "complete"

    def get(acc):
        nonlocal total
        if len(reqs) >= R["max_requests"]:
            raise OverflowError("max_requests reached")
        started = datetime.now(timezone.utc).isoformat()
        data, code = fetcher(acc, proto)
        total += len(data)
        if total > R["max_total_bytes_compressed"] or total > R["max_total_bytes_expanded"]:
            raise OverflowError("total byte bound exceeded")
        open(os.path.join(out, "raw", f"{acc}.soft.txt"), "wb").write(data)
        reqs.append({"accession": acc, "url": url_for(acc, proto), "started_utc": started, "http_status": code, "bytes": len(data), "sha256": sha256(data), "path": f"raw/{acc}.soft.txt"})
        return data

    gsms = []
    try:
        series = get(R["series_accession"])
        gsms = re.findall(r"^!Series_sample_id = (GSM\d+)$", series.decode("utf-8", "replace").replace("\r\n", "\n"), flags=re.M)
        if not gsms:
            status = "series_unavailable"
        if len(gsms) > R["max_gsm"]:
            errors.append(f"series lists {len(gsms)} samples, over max_gsm {R['max_gsm']}")
            status, gsms = "stopped_on_bound", []
        for g in gsms:
            sleep(R["min_delay_s"])
            data = get(g)
            records.append(sample_record(g, parse_soft(data.decode("utf-8", "replace")), proto))
    except (OverflowError, urllib.error.URLError, OSError, AssertionError) as e:
        errors.append(f"{type(e).__name__}: {e}")
        status = "stopped_on_bound" if isinstance(e, OverflowError) else ("series_unavailable" if not reqs else "stopped_on_error")
    if status == "complete" and len(records) != len(gsms):
        status = "stopped_on_error"
    pairs, st = pair(records)
    results = {"schema": RESULTS_SCHEMA, "protocol_sha256": proto_sha, "completion_status": status, "series": R["series_accession"],
               "listed_samples": gsms, "samples": [dict(r, pair_status=st.get(r["gsm"], ("unresolved_missing_identity", []))[0]) for r in records],
               "pairs": pairs, "summary": summarize(records, pairs, st), "errors": errors,
               "non_claims": proto["non_claims"]}
    json.dump(results, open(os.path.join(out, "results.json"), "w"), indent=1, sort_keys=True)
    receipt = {"schema": "frontier.sample-pairing.receipt/1", "protocol_sha256": proto_sha, "code_sha256": sha256(open(__file__, "rb").read()),
               "requests": reqs, "response_bytes": total, "wall_seconds": clock() - t0, "completion_status": status, "errors": errors,
               "python": sys.version.split()[0], "dollars": None}
    json.dump(receipt, open(os.path.join(out, "receipt.json"), "w"), indent=1, sort_keys=True)
    return results


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    proto, psha = load_protocol()
    if a.preflight:
        from engineering.sample_pairing import controls
        res = controls.run_all()
        print(json.dumps({"protocol_sha256": psha, "code_sha256": sha256(open(__file__, "rb").read()), "python": sys.version.split()[0], "controls": res}, indent=1))
        return 0 if all(res.values()) else 1
    if a.run:
        out = a.out or os.environ.get("COPS_OUT")
        if not out:
            print("--out or COPS_OUT required", file=sys.stderr)
            return 2
        res = run(out, proto, psha)
        print(json.dumps({"completion_status": res["completion_status"], "summary": res["summary"]}, indent=1))
        return 0 if res["completion_status"] == "complete" else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
