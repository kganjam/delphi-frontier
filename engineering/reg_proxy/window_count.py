"""Bounded fragment counts in frozen windows of tabix-indexed 10x ATAC fragment files (standard library only).

Reads the .tbi linear index, then byte-ranges BGZF blocks from the tile that holds the window start until the sorted
records pass the window end. The protocol (protocol.json) is frozen; this module only executes it. Counts are
descriptive library counts, not function."""
import hashlib
import http.client
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TILE = 1 << 14
INDEX_MAX_EXPANDED = 64 << 20  # the index is <= 1 MiB compressed; anything expanding past 64 MiB is refused
USABLE = ('ok', 'beyond_last_interval')
EXIT_CODES = {'complete': 0, 'stopped_on_bound': 2, 'partial_data': 3, 'stopped_on_error': 4}  # transport_amendment.json


class Refused(Exception):
    """A transport, format or bound violation; `.status` is recorded in results."""

    def __init__(self, status, detail=""):
        super().__init__(f"{status}: {detail}")
        self.status, self.detail = status, detail


class Budget:
    """Global, per-library and per-window byte ledgers plus request and runtime bounds (transport_amendment.json)."""

    def __init__(self, bounds, clock=time.monotonic):
        self.b, self.clock, self.t0 = bounds, clock, clock()
        self.requests = self.bytes = self.lib_bytes = self.window_bytes = 0

    def new_library(self):
        self.lib_bytes = self.window_bytes = 0

    def new_window(self):
        self.window_bytes = 0

    def check(self):
        if self.clock() - self.t0 > self.b["runtime_hard_s"]:
            raise Refused("stopped_on_bound", "runtime")
        if self.requests >= self.b["total_requests_max"]:
            raise Refused("stopped_on_bound", "requests")

    def precheck(self, n):
        """Refuse a request that could take any ledger over its cap, before it is sent."""
        if self.bytes + n > self.b["total_compressed_max_bytes"]:
            raise Refused("stopped_on_bound", "total_bytes")
        if self.lib_bytes + n > self.b["per_library_compressed_max_bytes"]:
            raise Refused("library_byte_cap", f"{self.lib_bytes}+{n}")
        if self.window_bytes + n > self.b["per_window_compressed_max_bytes"]:
            raise Refused("window_byte_cap", f"{self.window_bytes}+{n}")

    def charge(self, n):
        self.bytes += n
        self.lib_bytes += n
        self.window_bytes += n


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class HttpRange:
    """The one transport. `get(url, start, end)` returns bytes[start..end] inclusive or raises Refused."""

    def __init__(self, proto, budget, allowed_hosts=None, scheme=None, timeout=None, log=None):
        t = proto["transport"]
        self.hosts = allowed_hosts or [t["host"]]
        self.scheme = scheme or t["scheme"]
        self.timeout = timeout or t["timeout_s"]
        self.attempts = t["max_attempts_per_request"]
        self.budget, self.log = budget, log if log is not None else []
        self.opener = urllib.request.build_opener(NoRedirect)

    def get(self, url, start, end, total):
        u = urllib.parse.urlparse(url)
        if u.scheme != self.scheme or u.hostname not in self.hosts and f"{u.hostname}:{u.port}" not in self.hosts:
            raise Refused("host_refused", url)
        expected = end - start + 1
        last = None
        for attempt in range(1, self.attempts + 1):
            self.budget.check()
            self.budget.precheck(expected)  # cap refusals are final: never retried
            self.budget.requests += 1
            rec = {"url": url, "range": f"{start}-{end}", "attempt": attempt, "t": time.time(), "bytes_charged": 0}
            r = None
            try:
                r = self.opener.open(urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"}), timeout=self.timeout)
                rec["http_status"] = r.status
                if r.status != 206:
                    raise Refused("unsupported_range", f"HTTP {r.status}")  # no body byte is read
                if r.headers.get("Content-Range") != f"bytes {start}-{end}/{total}":
                    raise Refused("range_mismatch", str(r.headers.get("Content-Range")))
                body, err = self._bounded_read(r, expected + 1, rec)
                if err:
                    raise Refused("transport_error", err)
                if len(body) > expected:
                    raise Refused("oversized_response", f">{expected}")
                if len(body) != expected:
                    raise Refused("short_read", f"{len(body)} of {expected}")
                rec.update(ok=True, bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
                self.log.append(rec)
                return body
            except Refused as e:
                last = e
                rec.update(ok=False, failure=e.status)
            except (urllib.error.URLError, OSError, http.client.HTTPException) as e:
                last = Refused("transport_error", type(e).__name__)
                rec.update(ok=False, failure=type(e).__name__)
            finally:
                if r is not None:
                    r.close()
            self.log.append(rec)
            if last.status in ("unsupported_range", "range_mismatch", "oversized_response"):
                break  # deterministic server behaviour: a second attempt cannot differ
        raise last

    def _bounded_read(self, r, limit, rec):
        """Read at most `limit` bytes in chunks, charging every byte actually read, even when the read then fails."""
        got, err = [], None
        n = 0
        try:
            while n < limit:
                c = r.read(min(65536, limit - n))
                if not c:
                    break
                got.append(c)
                n += len(c)
                self.budget.charge(len(c))
                rec["bytes_charged"] = n
        except http.client.IncompleteRead as e:
            if e.partial:
                got.append(e.partial)
                self.budget.charge(len(e.partial))
                rec["bytes_charged"] = n + len(e.partial)
            err = "IncompleteRead"
        except (OSError, http.client.HTTPException) as e:
            err = type(e).__name__
        return b"".join(got), err


def bgzf_block(buf, off):
    """Decode the BGZF block starting at buf[off]. Returns (data, compressed_size) or None if buf ends inside it."""
    if len(buf) - off < 18:
        return None
    if buf[off:off + 4] != b"\x1f\x8b\x08\x04":
        raise Refused("bad_bgzf", f"offset {off}")
    xlen = struct.unpack_from("<H", buf, off + 10)[0]
    bsize = None
    p = off + 12
    while p < off + 12 + xlen:
        si, ln = buf[p:p + 2], struct.unpack_from("<H", buf, p + 2)[0]
        if si == b"BC" and ln == 2:
            bsize = struct.unpack_from("<H", buf, p + 4)[0] + 1
        p += 4 + ln
    if bsize is None:
        raise Refused("bad_bgzf", "no BC field")
    if len(buf) - off < bsize:
        return None
    raw = buf[off + 12 + xlen:off + bsize - 8]
    data = zlib.decompress(raw, -15)
    crc, isize = struct.unpack_from("<II", buf, off + bsize - 8)
    if len(data) != isize or zlib.crc32(data) != crc:
        raise Refused("bad_bgzf", "crc/isize")
    return data, bsize


def read_index(blob):
    """Parse a .tbi (optionally still wrapped in an outer gzip, as GEO ships it). Returns names, linear index, format."""
    t = blob
    for _ in range(3):  # GEO ships gzip(BGZF(tbi)); htslib writes BGZF(tbi) directly
        if t[:2] != b"\x1f\x8b":
            break
        t = b"".join(_bgzf_all(t)) if t[3] & 4 and b"BC" in t[10:20] else zlib.decompressobj(31).decompress(t, INDEX_MAX_EXPANDED + 1)
        if len(t) > INDEX_MAX_EXPANDED:
            raise Refused("bad_index", "expanded index too large")
    if t[:4] != b"TBI\x01":
        raise Refused("bad_index", "magic")
    n, fmt, cs, cb, ce, meta, skip, ln = struct.unpack_from("<8i", t, 4)
    names = t[36:36 + ln].split(b"\0")[:n]
    p = 36 + ln
    lin = []
    for _ in range(n):
        nb = struct.unpack_from("<i", t, p)[0]
        p += 4
        for _ in range(nb):
            nc = struct.unpack_from("<xxxxi", t, p)[0]
            p += 8 + 16 * nc
        ni = struct.unpack_from("<i", t, p)[0]
        p += 4
        lin.append(list(struct.unpack_from(f"<{ni}Q", t, p)))
        p += 8 * ni
    if len(t) - p not in (0, 8):  # tabix may append n_no_coor (uint64); anything else is not an index we understand
        raise Refused("bad_index", f"trailing {len(t) - p} bytes")
    return {"names": [x.decode() for x in names], "linear": lin, "format": fmt, "cols": (cs, cb, ce), "meta": meta, "skip": skip}


def _bgzf_all(buf):
    off = size = 0
    while off < len(buf):
        r = bgzf_block(buf, off)
        if r is None:
            raise Refused("bad_index", "truncated bgzf")
        size += len(r[0])
        if size > INDEX_MAX_EXPANDED:
            raise Refused("bad_index", "expanded index too large")
        yield r[0]
        off += r[1]


def count_window(fetch, total, idx, chrom, w0, w1, limits):
    """Count fragments overlapping [w0,w1) on `chrom`. `fetch(start,end)` returns bytes[start..end]. Returns a dict."""
    out = {"status": "ok", "fragment_rows": 0, "dup_count_sum": 0, "distinct_barcodes": 0, "compressed_bytes_read": 0, "responses": []}
    if chrom not in idx["names"]:
        out["status"] = "chrom_absent"
        return out
    lin = idx["linear"][idx["names"].index(chrom)]
    tile = w0 // TILE
    if tile >= len(lin):
        out["status"] = "beyond_last_interval"
        return out
    voff = lin[tile]
    if voff == 0:
        out["status"] = "beyond_last_interval"
        return out
    coff, uoff = voff >> 16, voff & 0xFFFF
    if coff >= total:
        raise Refused("index_file_mismatch", f"index offset {coff} >= file size {total}")
    chunk = limits["range_chunk_bytes"]
    cap = limits["per_window_compressed_max_bytes"]
    buf, base = b"", coff
    text, prev, barcodes, started = b"", -1, set(), False
    while True:
        # decode every whole block in buf, then decide whether more is needed
        pos = 0
        done = False
        while True:
            r = bgzf_block(buf, pos)
            if r is None:
                break
            data, size = r
            pos += size
            if not started:
                data, started = data[uoff:], True
            text += data
            *lines, text = text.split(b"\n")
            for ln in lines:
                if not ln or ln.startswith(b"#"):
                    continue
                f = ln.split(b"\t")
                c, s, e = f[0].decode(), int(f[1]), int(f[2])
                if c != chrom:
                    done = True
                    break
                if s < prev:
                    out["status"] = "unsorted_refused"
                    return out
                prev = s
                if s >= w1:
                    done = True
                    break
                if e > w0:
                    out["fragment_rows"] += 1
                    out["dup_count_sum"] += int(f[4]) if len(f) > 4 else 1
                    barcodes.add(f[3])
            if done:
                break
        if done:
            break
        buf, base = buf[pos:], base + pos
        if base + len(buf) >= total:
            if buf:
                raise Refused("truncated_bgzf", f"{len(buf)} undecodable bytes at end of file")
            break  # clean end of file: the trailing EOF block yields nothing more
        if out["compressed_bytes_read"] >= cap:
            out["status"] = "window_byte_cap"
            return out
        end = min(base + len(buf) + chunk, total) - 1
        got = fetch(base + len(buf), end)
        out["compressed_bytes_read"] += len(got)
        out["responses"].append({"range": f"{base + len(buf)}-{end}", "sha256": hashlib.sha256(got).hexdigest()})
        buf += got
    out["distinct_barcodes"] = len(barcodes)
    return out


def build_windows(controls):
    """Amplicon windows plus the frozen +250000/+500000 comparison windows, with an overlap refusal."""
    wins = []
    for c in controls:
        w0, w1 = c["start_1based"] - 1, c["end_1based"]
        wins.append({"id": c["name"], "kind": c["class"], "chrom": c["chrom"], "start0": w0, "end0": w1, "of": None})
        for off in (250000, 500000):
            wins.append({"id": f"{c['name']}+{off}", "kind": "comparison", "chrom": c["chrom"], "start0": w0 + off, "end0": w1 + off, "of": c["name"]})
    for i, a in enumerate(wins):
        for b in wins[i + 1:]:
            if a["chrom"] == b["chrom"] and a["start0"] < b["end0"] and b["start0"] < a["end0"]:
                raise Refused("windows_overlap", f"{a['id']} {b['id']}")
    return wins


def run(out, proto, controls, make_fetch, clock=time.monotonic, budget=None):
    """make_fetch(url, total, budget) -> fetch(start,end). Writes results.json/receipt.json into the NEW directory `out`.
    completion_status follows transport_amendment.json: complete only when all expected identities are present and usable."""
    if os.path.exists(out):
        raise SystemExit(f"{out} exists: refuse to reuse an output directory")
    os.makedirs(out)
    budget = budget or Budget(proto["bounds"], clock)
    wins = build_windows(controls["controls"])
    expected = [(lib["label"], w["id"]) for lib in controls["libraries"] for w in wins]
    assert len(set(expected)) == len(expected)
    res, stop, error = [], None, None
    try:
        for lib in controls["libraries"]:
            budget.new_library()

            def rowbase(w, lib=lib):
                return {"library": lib["label"], "gsm": lib["gsm"], "window": w["id"], "kind": w["kind"], "chrom": w["chrom"], "start0": w["start0"], "end0": w["end0"]}
            try:
                if lib["index_bytes"] > proto["bounds"]["index_download_max_bytes"]:
                    raise Refused("index_too_large", str(lib["index_bytes"]))
                idx = read_index(make_fetch(lib["index_url"], lib["index_bytes"], budget)(0, lib["index_bytes"] - 1))
                if idx["format"] != 65536:
                    raise Refused("bad_index", f"format {idx['format']}")
                fetch = make_fetch(lib["fragments_url"], lib["fragments_bytes"], budget)
            except Refused as e:
                if e.status == "stopped_on_bound":
                    stop = e.detail
                    break
                res += [rowbase(w) | {"status": "library_unavailable", "detail": e.status} for w in wins]
                continue
            for w in wins:
                budget.new_window()
                row = rowbase(w)
                try:
                    row.update(count_window(fetch, lib["fragments_bytes"], idx, w["chrom"], w["start0"], w["end0"], proto["transport"] | proto["bounds"]))
                except Refused as e:
                    row.update(status=e.status, detail=e.detail)
                    if e.status == "stopped_on_bound":
                        stop = e.detail
                row["window_bytes_charged"] = budget.window_bytes
                res.append(row)
                if stop:
                    break
            if stop:
                break
    except Exception as e:  # an unexpected failure must not be reported as a complete run
        error = type(e).__name__
    present = {(r["library"], r["window"]) for r in res}
    usable = {(r["library"], r["window"]) for r in res if r["status"] in USABLE}
    status = ("stopped_on_error" if error else "stopped_on_bound" if stop else
              "complete" if len(present) == len(expected) == len(usable) and present == set(expected) else "partial_data")
    summary = summarise(res, controls["libraries"])
    doc = {"schema": "frontier.reg-proxy.results/2", "completion_status": status, "windows": res, "summary": summary,
           "claim_limits": "descriptive library counts; accessibility is context, not function; LEN excluded; no test, threshold or rank"}
    p = os.path.join(out, "results.json")
    json.dump(doc, open(p, "w"), indent=1, sort_keys=True)
    rec = {"completion_status": status, "stop_detail": stop, "error": error, "requests": budget.requests, "compressed_bytes": budget.bytes,
           "elapsed_s": round(clock() - budget.t0, 1), "expected_identities": len(expected), "present_identities": len(present),
           "usable_identities": len(usable), "missing_identities": [list(x) for x in expected if x not in present],
           "unusable_identities": [list(x) for x in expected if x in present and x not in usable],
           "protocol_sha256": hashlib.sha256(open(os.path.join(HERE, "protocol.json"), "rb").read()).hexdigest(),
           "amendment_sha256": hashlib.sha256(open(os.path.join(HERE, "transport_amendment.json"), "rb").read()).hexdigest(),
           "results_sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()}
    json.dump(rec, open(os.path.join(out, "receipt.json"), "w"), indent=1, sort_keys=True)
    return doc, rec


def summarise(rows, libraries):
    """Per library and window: count, per-kb, ratio to the median of that window's own two comparison counts (null if 0)."""
    usable = set(USABLE)
    by = {(r["library"], r["window"]): r for r in rows}
    out = []
    for r in rows:
        if r["kind"] == "comparison":
            continue
        s = {"library": r["library"], "window": r["window"], "kind": r["kind"], "status": r["status"]}
        if r["status"] in usable:
            n = r["fragment_rows"]
            kb = (r["end0"] - r["start0"]) / 1000
            comp = [by.get((r["library"], f"{r['window']}+{o}")) for o in (250000, 500000)]
            cc = [c["fragment_rows"] for c in comp if c and c["status"] in usable]
            med = (sorted(cc)[0] + sorted(cc)[-1]) / 2 if len(cc) == 2 else None
            s.update(fragment_rows=n, per_kb=round(n / kb, 4), comparison_counts=cc,
                     ratio_to_comparison_median=round(n / med, 4) if med else None)
        out.append(s)
    return out


def http_fetch_factory(proto, log, allowed_hosts=None, scheme=None):
    def make(url, total, budget):
        h = HttpRange(proto, budget, allowed_hosts, scheme, log=log)
        return lambda a, b: h.get(url, a, b, total)
    return make


def load():
    return (json.load(open(os.path.join(HERE, "protocol.json"))), json.load(open(os.path.join(HERE, "controls.json"))))


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    from engineering.reg_proxy import controls_synth
    if "--preflight" in a:
        r = controls_synth.run_all()
        print(json.dumps(r, indent=1))
        return 0 if all(x["passed"] for x in r["controls"]) else 1
    if "--run" in a:
        out = a[a.index("--out") + 1] if "--out" in a else os.environ.get("COPS_OUT")
        if not out:
            raise SystemExit("--out or $COPS_OUT required")
        pre = controls_synth.run_all()
        if not all(x["passed"] for x in pre["controls"]):
            raise SystemExit("preflight controls failed; refusing to read targets")
        proto, ctl = load()
        log = []
        doc, rec = run(out, proto, ctl, http_fetch_factory(proto, log))
        json.dump(log, open(os.path.join(out, "requests.json"), "w"), indent=1)
        print(json.dumps(rec, indent=1))
        return EXIT_CODES[rec["completion_status"]]
    raise SystemExit("usage: --preflight | --run [--out DIR]")


if __name__ == "__main__":
    sys.exit(main())
