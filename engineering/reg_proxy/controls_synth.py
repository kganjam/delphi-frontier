"""Same-parser synthetic controls for window_count: generated BGZF + tabix-style fixtures (linear index only), a brute-force
oracle, a local Range server for the real transport class, and the real GSE261907 0dpa1 index bytes as a parse-only fixture.
`run_all()` returns one record per control; the preflight and the remote entry both run it before any target read."""
import hashlib
import http.client
import http.server
import json
import os
import random
import struct
import threading
import zlib

from engineering.reg_proxy import window_count as wc

HERE = os.path.dirname(os.path.abspath(__file__))
REAL_INDEX = os.path.join(HERE, "fixtures", "GSM8153942_0dpa1_atac_fragments.tsv.gz.tbi.gz")
REAL_INDEX_SHA = "f456acb07e507e2d9dbef1bb25e2081b61437aaa495870d0f6d79629e9f92e19"


def bgzf_write(data, block=1500):
    """Encode `data` as BGZF with small blocks; returns (bytes, [(coffset, ustart)]) so callers can form virtual offsets."""
    out, starts, c = [], [], 0
    for u in range(0, max(len(data), 1), block):
        piece = data[u:u + block]
        co = zlib.compressobj(6, zlib.DEFLATED, -15)
        raw = co.compress(piece) + co.flush()
        bs = 12 + 6 + len(raw) + 8
        hdr = b"\x1f\x8b\x08\x04\0\0\0\0\0\xff" + struct.pack("<H", 6) + b"BC" + struct.pack("<HH", 2, bs - 1)
        out.append(hdr + raw + struct.pack("<II", zlib.crc32(piece), len(piece)))
        starts.append((c, u))
        c += bs
    eof = bytes.fromhex("1f8b08040000000000ff0600424302001b0003000000000000000000")
    out.append(eof)
    return b"".join(out), starts


def make_fixture(records, block=1500):
    """records: list of (chrom, start, end, barcode, dup) already in file order. Returns (fragments_bytes, tbi_bytes, text)."""
    text = "".join(f"{c}\t{s}\t{e}\t{b}\t{d}\n" for c, s, e, b, d in records).encode()
    text = b"#fixture header\n" + text
    frag, starts = bgzf_write(text, block)
    names, lin, p = [], {}, len(b"#fixture header\n")
    for c, s, e, b, d in records:
        line = len(f"{c}\t{s}\t{e}\t{b}\t{d}\n".encode())
        k = max(i for i, (_, u) in enumerate(starts) if u <= p)
        voff = (starts[k][0] << 16) | (p - starts[k][1])
        if c not in names:
            names.append(c)
            lin[c] = {}
        for t in range(s >> 14, ((e - 1) >> 14) + 1):
            lin[c].setdefault(t, voff)
        p += line
    body = b"".join(f"{n}\0".encode() for n in names)
    t = b"TBI\x01" + struct.pack("<8i", len(names), 65536, 1, 2, 3, 35, 0, len(body)) + body
    for n in names:
        top = max(lin[n]) + 1
        arr, nxt = [0] * top, 0
        for i in range(top - 1, -1, -1):
            nxt = lin[n].get(i, nxt)
            arr[i] = nxt
        t += struct.pack("<ii", 0, top) + struct.pack(f"<{top}Q", *arr)
    tb, _ = bgzf_write(t, 60000)
    outer = zlib.compressobj(6, zlib.DEFLATED, 31)
    return frag, outer.compress(tb) + outer.flush(), text


def oracle(records, chrom, w0, w1):
    rows = [r for r in records if r[0] == chrom and r[1] < w1 and r[2] > w0]
    return len(rows), sum(r[4] for r in rows), len({r[3] for r in rows})


def synth_records(seed=7, n=4000):
    rnd = random.Random(seed)
    recs = []
    for chrom, span in (("chr1", 200000), ("chr2", 90000)):
        starts = sorted(rnd.randrange(0, span) for _ in range(n // 2))
        recs += [(chrom, s, s + rnd.choice([30, 80, 200, 20000]), f"BC{rnd.randrange(60)}", rnd.randrange(1, 4)) for s in starts]
    return recs


LIMITS = {"range_chunk_bytes": 4096, "per_window_compressed_max_bytes": 1 << 20}


def local_fetch(blob):
    def f(a, b):
        return blob[a:b + 1]
    return f


class Server:
    """Local Range server with switchable misbehaviour, used to run the real HttpRange class."""

    def __init__(self, files):
        outer = self
        self.files, self.mode, self.fail_first, self.hits, self.sent = files, "ok", 0, 0, 0
        self.empty_first, self.extra_headers, self.paths = 0, False, []

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                outer.hits += 1
                outer.paths.append(self.path)
                blob = outer.files[self.path]
                if outer.mode == "redirect":
                    self.send_response(302)
                    self.send_header("Location", "http://127.0.0.1:1/x")
                    self.end_headers()
                    return
                rng0 = self.headers.get("Range")
                if outer.fail_first > 0 and rng0:
                    outer.fail_first -= 1
                    a0, b0 = map(int, rng0.split("=")[1].split("-"))
                    b0 = min(b0, len(blob) - 1)
                    self.send_response(206)
                    self.send_header("Content-Range", f"bytes {a0}-{b0}/{len(blob)}")
                    self.send_header("Content-Length", str(b0 - a0 + 1))
                    self.end_headers()
                    self.wfile.write(blob[a0:a0 + 7])  # fewer bytes than promised, then close: IncompleteRead
                    return
                if rng0 and (outer.mode in ("empty_206", "empty_206_declared0") or outer.empty_first > 0):
                    if outer.empty_first > 0:
                        outer.empty_first -= 1
                    a0, b0 = map(int, rng0.split("=")[1].split("-"))
                    b0 = min(b0, len(blob) - 1)
                    self.send_response(206)
                    self.send_header("Content-Range", f"bytes {a0}-{b0}/{len(blob)}")
                    self.send_header("Content-Length", "0" if outer.mode == "empty_206_declared0" else str(b0 - a0 + 1))
                    self.end_headers()
                    return  # the headers promise a body and none is sent
                if outer.mode == "chunked_trunc" and rng0:
                    a0, b0 = map(int, rng0.split("=")[1].split("-"))
                    b0 = min(b0, len(blob) - 1)
                    self.send_response(206)
                    self.send_header("Content-Range", f"bytes {a0}-{b0}/{len(blob)}")
                    self.send_header("Transfer-Encoding", "chunked")
                    self.end_headers()
                    self.wfile.write(b"7\r\n" + blob[a0:a0 + 7] + b"\r\n")  # one 7-byte chunk, then the connection closes
                    return
                if outer.mode == "infinite_200":
                    self.send_response(200)
                    self.end_headers()
                    try:
                        while True:
                            self.wfile.write(b"z" * 65536)
                            outer.sent += 65536
                    except OSError:
                        return
                rng = self.headers.get("Range")
                if outer.mode == "ignore_range" or not rng:
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(blob)))
                    self.end_headers()
                    self.wfile.write(blob)
                    return
                a, b = map(int, rng.split("=")[1].split("-"))
                b = min(b, len(blob) - 1)
                body = blob[a:b + 1]
                cr = f"bytes {a}-{b}/{len(blob)}" if outer.mode != "bad_content_range" else f"bytes {a}-{b}/{len(blob) + 1}"
                if outer.mode == "short":
                    body = body[:-1]
                if outer.mode == "oversize":
                    body = blob[a:b + 1] + blob[b + 1:b + 1 + 500]
                    cr = f"bytes {a}-{b}/{len(blob)}"
                self.send_response(206)
                self.send_header("Content-Range", cr)
                self.send_header("Content-Length", str(len(body)))
                if outer.extra_headers:
                    for k, v in (("Set-Cookie", "session=SECRET-COOKIE-VALUE"), ("Authorization", "Bearer SECRET-TOKEN"), ("X-Secret", "SECRET-X"),
                                 ("ETag", '"abc123"'), ("Last-Modified", "Sat, 31 Oct 2026 00:00:00 GMT"), ("Accept-Ranges", "bytes"), ("Content-Type", "application/gzip")):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body)

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.host = f"127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def url(self, path):
        return f"http://{self.host}{path}"

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def _proto():
    return json.load(open(os.path.join(HERE, "protocol.json")))


def _ctl(name, fn):
    try:
        detail = fn()
        return {"control": name, "passed": True, "detail": detail}
    except AssertionError as e:
        return {"control": name, "passed": False, "detail": f"assertion failed: {e}"}
    except Exception as e:  # a crashing control is a failing control
        return {"control": name, "passed": False, "detail": f"{type(e).__name__}: {e}"}


def run_all():
    proto = _proto()
    ctl = json.load(open(os.path.join(HERE, "controls.json")))
    recs = synth_records()
    frag, tbi, _ = make_fixture(recs)
    idx = wc.read_index(tbi)
    total = len(frag)
    lim = proto["transport"] | proto["bounds"] | LIMITS
    results = []

    def count(chrom, a, b, limits=lim, index=idx, blob=frag):
        return wc.count_window(local_fetch(blob), len(blob), index, chrom, a, b, limits)

    def oracle_agree():
        rnd = random.Random(11)
        wins = [("chr1", 0, 500), ("chr1", 16383, 16385), ("chr1", 16384, 16385), ("chr2", 89000, 91000)]
        wins += [("chr1" if rnd.random() < .6 else "chr2", a, a + rnd.choice([1, 400, 1500, 30000])) for a in (rnd.randrange(0, 90000) for _ in range(60))]
        for c, a, b in wins:
            r = count(c, a, b)
            o = oracle(recs, c, a, b)
            assert r["status"] in ("ok", "beyond_last_interval"), (c, a, b, r["status"])
            assert (r["fragment_rows"], r["dup_count_sum"], r["distinct_barcodes"]) == o, (c, a, b, r["fragment_rows"], o)
        return f"{len(wins)} windows equal the brute-force oracle (rows, dup sum, barcodes), block size 1500 B, 4 KiB ranges"
    results.append(_ctl("counts equal brute-force oracle incl. tile edges and block-spanning lines", oracle_agree))

    def boundary():
        r = [x for x in recs if x[0] == "chr1"][50]
        s, e = r[1], r[2]
        assert count("chr1", e, e + 10)["fragment_rows"] == oracle(recs, "chr1", e, e + 10)[0]
        assert count("chr1", s - 5, s)["fragment_rows"] == oracle(recs, "chr1", s - 5, s)[0]
        return "end==window start excluded; start==window end excluded (half-open), equal to oracle"
    results.append(_ctl("half-open boundary", boundary))

    def zero_vs_missing():
        z = count("chr1", 150000, 150010)
        assert z["status"] in ("ok", "beyond_last_interval")
        a = count("chrX", 0, 100)
        assert a["status"] == "chrom_absent" and a["fragment_rows"] == 0
        return f"empty window status={z['status']} rows={z['fragment_rows']}; absent chrom status=chrom_absent"
    results.append(_ctl("zero count is distinct from absent chromosome", zero_vs_missing))

    def beyond():
        r = count("chr2", 10 ** 7, 10 ** 7 + 100)
        assert r["status"] == "beyond_last_interval" and r["fragment_rows"] == 0
        return "tile past the linear index -> beyond_last_interval, 0"
    results.append(_ctl("window beyond last indexed tile", beyond))

    def unsorted():
        bad = list(recs)
        bad[100], bad[101] = bad[101], bad[100]
        # force a strict inversion
        c, s, e, b, d = bad[100]
        bad[100] = (c, bad[101][1] + 5, e + 5, b, d)
        f2, t2, _ = make_fixture(bad)
        r = wc.count_window(local_fetch(f2), len(f2), wc.read_index(t2), bad[100][0], 0, 10 ** 6, lim)
        assert r["status"] == "unsorted_refused", r["status"]
        return "inverted order refused"
    results.append(_ctl("unsorted fragment file refused", unsorted))

    def cap():
        r = count("chr1", 0, 200000, limits=lim | {"per_window_compressed_max_bytes": 3000})
        assert r["status"] == "window_byte_cap", r["status"]
        return "per-window byte cap -> window_byte_cap, no partial count presented as ok"
    results.append(_ctl("per-window byte cap refused", cap))

    def corrupt():
        bad = bytearray(frag)
        bad[40] ^= 0xFF
        try:
            wc.count_window(local_fetch(bytes(bad)), len(bad), idx, "chr1", 0, 400, lim)
        except (wc.Refused, zlib.error):
            return "flipped byte in a block refused (crc/inflate)"
        raise AssertionError("corrupt block accepted")
    results.append(_ctl("corrupt BGZF block refused", corrupt))

    def bad_crc():
        bad = bytearray(frag)
        bsize = struct.unpack_from("<H", bad, 16)[0] + 1
        bad[bsize - 8] ^= 0x01  # stored CRC32 of block 0 only: the deflate stream itself stays valid
        try:
            wc.count_window(local_fetch(bytes(bad)), len(bad), idx, "chr1", 0, 400, lim)
        except wc.Refused as e:
            assert e.status == "bad_bgzf" and "crc" in e.detail, (e.status, e.detail)
            return "altered stored CRC refused as bad_bgzf (inflate alone would not notice)"
        raise AssertionError("bad CRC accepted")
    results.append(_ctl("BGZF CRC mismatch refused", bad_crc))

    def mismatch():
        short = frag[:3000]  # index still points at offsets far beyond this file
        try:
            wc.count_window(local_fetch(short), len(short), idx, "chr2", 80000, 80100, lim)
        except wc.Refused as e:
            assert e.status == "index_file_mismatch", e.status
            return "index offset past the end of the file refused, not counted as 0"
        raise AssertionError("index/file mismatch accepted")
    results.append(_ctl("index pointing past the file refused", mismatch))

    def real_index():
        blob = open(REAL_INDEX, "rb").read()
        assert hashlib.sha256(blob).hexdigest() == REAL_INDEX_SHA and len(blob) == 492634
        ix = wc.read_index(blob)
        assert ix["format"] == 65536 and len(ix["names"]) == 26 and "chr24" in ix["names"] and "EGFP" in ix["names"]
        lin = ix["linear"][ix["names"].index("chr24")]
        assert len(lin) > 2000 and all(lin[i] <= lin[i + 1] for i in range(len(lin) - 1))
        return f"real GEO 0dpa1 index (sha {REAL_INDEX_SHA[:12]}): 26 sequences, chr24 linear entries={len(lin)}, monotone"
    results.append(_ctl("real GSE261907 index parses", real_index))

    def windows():
        w = wc.build_windows(ctl["controls"])
        assert len(w) == 33 and sum(x["kind"] == "reporter_negative" for x in w) == 1 and sum(x["kind"] == "reporter_positive" for x in w) == 10
        assert all(x["end0"] - x["start0"] == (ctl["controls"][0]["end_1based"] - ctl["controls"][0]["start_1based"] + 1) for x in w[:3])
        bad = [dict(ctl["controls"][0]), dict(ctl["controls"][0], name="dup")]
        try:
            wc.build_windows(bad)
        except wc.Refused as e:
            assert e.status == "windows_overlap"
            return "33 windows (10 positive, 1 negative, 22 comparison); duplicate window refused"
        raise AssertionError("overlap accepted")
    results.append(_ctl("window set is frozen and overlap-free", windows))

    def controls_integrity():
        names = [c["name"] for c in ctl["controls"]]
        assert len(names) == 11 and "lhx2b-ENH2" in names and not any("LEN" in n or "lepb" in n for n in names)
        assert [c["class"] for c in ctl["controls"] if c["name"] == "lhx2b-ENH2"] == ["reporter_negative"]
        assert len(ctl["libraries"]) == 10
        assert len(ctl["source"]["table_sha256"]) == 64
        return "11 controls (1 reporter-negative), no LEN window, 10 libraries, source table hash pinned"
    results.append(_ctl("controls manifest integrity", controls_integrity))

    def htslib_crosscheck():
        d = os.path.join(HERE, "fixtures")
        exp = json.load(open(os.path.join(d, "htslib_expected.json")))
        frag_h, tbi_h = open(os.path.join(d, "htslib_fixture.tsv.gz"), "rb").read(), open(os.path.join(d, "htslib_fixture.tsv.gz.tbi"), "rb").read()
        assert hashlib.sha256(frag_h).hexdigest() == exp["sha256"]["tsv_gz"] and hashlib.sha256(tbi_h).hexdigest() == exp["sha256"]["tbi"]
        ix = wc.read_index(tbi_h)
        assert ix["format"] == 65536 and ix["names"] == ["chr1", "chr2"], ix["names"]
        n = 0
        for w in exp["windows"]:
            r = wc.count_window(local_fetch(frag_h), len(frag_h), ix, w["chrom"], w["start"], w["end"], lim)
            assert r["status"] in ("ok", "beyond_last_interval"), (w, r["status"])
            assert (r["fragment_rows"], r["dup_count_sum"], r["distinct_barcodes"]) == (w["rows"], w["dup"], w["barcodes"]), (w, r["fragment_rows"])
            n += 1
        real = wc.read_index(open(REAL_INDEX, "rb").read())
        assert real["names"] == exp["real_index_contigs_by_htslib"], (real["names"][:3], exp["real_index_contigs_by_htslib"][:3])
        return f"{n} windows counted from an htslib-written index and file equal htslib's own fetch counts ({exp['tool']}); real 0dpa1 index contig list equals htslib's (26)"
    results.append(_ctl("independent htslib cross-check", htslib_crosscheck))

    # ---- real transport class against a local Range server ----
    files = {"/a.gz": frag, "/a.tbi.gz": tbi}
    srv = Server(files)
    try:
        def http_equal():
            log = []
            b = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, b, [srv.host], "http", log=log)
            blob = h.get(srv.url("/a.tbi.gz"), 0, len(tbi) - 1, len(tbi))
            ix = wc.read_index(blob)
            r = wc.count_window(lambda a, e: h.get(srv.url("/a.gz"), a, e, total), total, ix, "chr1", 1000, 3000, lim)
            assert (r["fragment_rows"], r["dup_count_sum"], r["distinct_barcodes"]) == oracle(recs, "chr1", 1000, 3000)
            assert all(x["ok"] for x in log) and b.requests == len(log)
            return f"HTTP Range path equals oracle with {len(log)} logged requests"
        results.append(_ctl("HTTP transport path equals oracle and logs every request", http_equal))

        def refusal(mode, status, attempts_expected):
            def f():
                srv.mode = mode
                log = []
                h = wc.HttpRange(proto, wc.Budget(proto["bounds"]), [srv.host], "http", log=log)
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == status, e.status
                    assert len(log) == attempts_expected, len(log)
                    return f"{mode}: refused as {status} after {len(log)} logged attempt(s)"
                finally:
                    srv.mode = "ok"
                raise AssertionError(f"{mode} accepted")
            return f
        results.append(_ctl("server ignoring Range (HTTP 200) refused", refusal("ignore_range", "unsupported_range", 1)))
        results.append(_ctl("wrong Content-Range refused", refusal("bad_content_range", "range_mismatch", 1)))
        results.append(_ctl("short body refused", refusal("short", "short_read", 2)))
        results.append(_ctl("redirect refused", refusal("redirect", "transport_error", 2)))

        def flaky():
            srv.fail_first = 1
            log = []
            h = wc.HttpRange(proto, wc.Budget(proto["bounds"]), [srv.host], "http", log=log)
            bud = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, bud, [srv.host], "http", log=log)
            body = h.get(srv.url("/a.gz"), 0, 99, total)
            assert body == frag[:100] and [x["ok"] for x in log] == [False, True], log
            assert [x["bytes_charged"] for x in log] == [7, 100] and bud.bytes == 107, (log, bud.bytes)
            return "one IncompleteRead (7 bytes) then success: both attempts logged and the 7 failed bytes are charged (107 total)"
        results.append(_ctl("declared second attempt after IncompleteRead", flaky))

        def host_refused():
            h = wc.HttpRange(proto, wc.Budget(proto["bounds"]), ["ftp.ncbi.nlm.nih.gov"], "https")
            try:
                h.get(srv.url("/a.gz"), 0, 9, total)
            except wc.Refused as e:
                assert e.status == "host_refused"
                return "non-allowlisted host refused before any request"
            raise AssertionError("host accepted")
        results.append(_ctl("host allowlist", host_refused))

        def end_to_end():
            import tempfile
            ctl2 = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [{"gsm": "GSMfx1", "label": "fx1", "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)},
                                  {"gsm": "GSMfx2", "label": "fx2", "dpa": 0, "replicate": 2, "fragments_url": srv.url("/missing"), "fragments_bytes": 10,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)}]}
            log = []
            out = os.path.join(tempfile.mkdtemp(), "o")
            files["/missing"] = b"x" * 10
            doc, rec = wc.run(out, proto, ctl2, wc.http_fetch_factory(proto, log, [srv.host], "http"))
            rows = doc["windows"]
            assert len(rows) == 6, [(r["library"],r["window"],r["status"],r.get("detail")) for r in rows]
            assert rec["completion_status"] == "partial_data", rec["completion_status"]
            assert rec["expected_identities"] == 6 and rec["present_identities"] == 6 and rec["usable_identities"] == 5 and rec["unusable_identities"] == [["fx2", "fx"]], rec
            first = [r for r in rows if r["library"] == "fx1" and r["window"] == "fx"][0]
            assert first["fragment_rows"] == oracle(recs, "chr1", 1000, 2400)[0], first
            bad = [r for r in rows if r["library"] == "fx2"]
            st = {r["window"]: r["status"] for r in bad}
            assert st["fx"] not in ("ok", "beyond_last_interval") and st["fx+250000"] == "beyond_last_interval", st  # indexed-empty windows never touch the bad file
            try:
                wc.run(out, proto, ctl2, wc.http_fetch_factory(proto, log, [srv.host], "http"))
            except SystemExit:
                return "one unreadable window -> partial_data (6 expected, 6 present, 5 usable), the failed row kept; reuse of output dir refused"
            raise AssertionError("output dir reuse accepted")
        results.append(_ctl("end-to-end run keeps every row and refuses output reuse", end_to_end))

        def bound():
            import tempfile
            b = wc.Budget(proto["bounds"] | {"total_requests_max": 1})
            out = os.path.join(tempfile.mkdtemp(), "o")
            ctl2 = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [{"gsm": "GSMfx1", "label": "fx1", "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)}]}
            doc, rec = wc.run(out, proto, ctl2, wc.http_fetch_factory(proto, [], [srv.host], "http"), budget=b)
            assert rec["completion_status"] == "stopped_on_bound", rec
            return f"request bound 1 -> stopped_on_bound after {rec['requests']} requests; {len(doc['windows'])} rows kept"
        results.append(_ctl("request bound stops the run and keeps partial rows", bound))

        def no_body_on_200():
            srv.mode, srv.sent = "infinite_200", 0
            bud = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, bud, [srv.host], "http", timeout=5)
            try:
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == "unsupported_range", e.status
                    assert bud.bytes == 0, bud.bytes
                    return f"HTTP 200 from a server that streams forever: refused on status, 0 body bytes read or charged (server wrote {srv.sent // 1024} KiB into socket buffers)"
                raise AssertionError("200 accepted")
            finally:
                srv.mode = "ok"
        results.append(_ctl("HTTP 200 refused without consuming the body", no_body_on_200))

        def oversize():
            srv.mode = "oversize"
            bud = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, bud, [srv.host], "http")
            try:
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == "oversized_response", e.status
                    assert bud.bytes == 101, bud.bytes  # read limit is expected+1, and those bytes are charged
                    return "206 body longer than its range: read stops at expected+1 (101), refused, 101 bytes charged"
                raise AssertionError("oversized body accepted")
            finally:
                srv.mode = "ok"
        results.append(_ctl("oversized 206 body bounded and charged", oversize))

        def failed_bytes_charged():
            srv.mode = "short"
            bud = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, bud, [srv.host], "http")
            try:
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == "short_read"
                    assert bud.bytes == 198 and bud.requests == 2, (bud.bytes, bud.requests)  # 2 attempts x 99 bytes, both charged
                    return "short body: both attempts charged (198 bytes, 2 requests)"
                raise AssertionError("short body accepted")
            finally:
                srv.mode = "ok"
        results.append(_ctl("failed and retried reads consume budget", failed_bytes_charged))

        def chunked_partial():
            srv.mode = "chunked_trunc"
            bud = wc.Budget(proto["bounds"])
            h = wc.HttpRange(proto, bud, [srv.host], "http")
            try:
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == "transport_error", e.status
                    assert bud.bytes == 14 and bud.requests == 2, (bud.bytes, bud.requests)
                    return "chunked body cut after 7 bytes (http.client IncompleteRead): 7 bytes charged per attempt, 2 attempts, 14 total"
                raise AssertionError("truncated chunked body accepted")
            finally:
                srv.mode = "ok"
        results.append(_ctl("IncompleteRead partial bytes are charged", chunked_partial))

        def precheck():
            for cap, status in (("per_window_compressed_max_bytes", "window_byte_cap"), ("per_library_compressed_max_bytes", "library_byte_cap"),
                                ("total_compressed_max_bytes", "stopped_on_bound")):
                before = srv.hits
                h = wc.HttpRange(proto, wc.Budget(proto["bounds"] | {cap: 50}), [srv.host], "http")
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                except wc.Refused as e:
                    assert e.status == status, (cap, e.status)
                    assert srv.hits == before, "a request was sent that could exceed the cap"
                    continue
                raise AssertionError(f"{cap} not enforced")
            return "a 100-byte request against a 50-byte window, library or total cap is refused before it is sent"
        results.append(_ctl("caps refuse a request before it is sent", precheck))

        def cap_edge():
            # 1. a request of exactly the remaining cap cannot reserve its sentinel byte: refused unsent
            before = srv.hits
            h = wc.HttpRange(proto, wc.Budget(proto["bounds"] | {"per_window_compressed_max_bytes": 100}), [srv.host], "http")
            try:
                h.get(srv.url("/a.gz"), 0, 99, total)
                raise AssertionError("100-byte request accepted against a 100-byte cap")
            except wc.Refused as e:
                assert e.status == "window_byte_cap" and srv.hits == before, (e.status, srv.hits - before)
            # 2. an oversized body against a cap with room for exactly expected+1 never pushes any ledger past its cap
            srv.mode = "oversize"
            try:
                caps = {"per_window_compressed_max_bytes": 101, "per_library_compressed_max_bytes": 101, "total_compressed_max_bytes": 101}
                bud = wc.Budget(proto["bounds"] | caps)
                h = wc.HttpRange(proto, bud, [srv.host], "http")
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                    raise AssertionError("oversized body accepted")
                except wc.Refused as e:
                    assert e.status == "oversized_response", e.status
                assert bud.bytes == bud.lib_bytes == bud.window_bytes == 101, (bud.bytes, bud.lib_bytes, bud.window_bytes)
            finally:
                srv.mode = "ok"
            # 3. retries reserve too: after one 99-byte short read the second attempt (99+101 > 150) is refused unsent
            srv.mode, before = "short", srv.hits
            try:
                bud = wc.Budget(proto["bounds"] | {"per_window_compressed_max_bytes": 150})
                h = wc.HttpRange(proto, bud, [srv.host], "http")
                try:
                    h.get(srv.url("/a.gz"), 0, 99, total)
                    raise AssertionError("short body accepted")
                except wc.Refused as e:
                    assert e.status == "window_byte_cap" and srv.hits - before == 1 and bud.window_bytes == 99 <= 150, (e.status, srv.hits - before, bud.window_bytes)
            finally:
                srv.mode = "ok"
            return "100 B request vs 100 B cap refused unsent; oversized body vs cap 101 charges exactly 101 on all ledgers; retry reservation refuses a second attempt that could exceed the cap"
        results.append(_ctl("cap boundary: sentinel byte and retries reserved", cap_edge))

        def library_ledger():
            import tempfile
            ctl2 = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [{"gsm": "GSMfx1", "label": "fx1", "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)}]}
            small = proto | {"bounds": proto["bounds"] | {"per_library_compressed_max_bytes": len(tbi) + 5}}
            doc, rec = wc.run(os.path.join(tempfile.mkdtemp(), "o"), small, ctl2, wc.http_fetch_factory(small, [], [srv.host], "http"))
            st = {r["window"]: r["status"] for r in doc["windows"]}
            assert st["fx"] == "library_byte_cap", st
            assert rec["completion_status"] == "partial_data", rec["completion_status"]
            return "index bytes count against the library ledger: the next read is refused (library_byte_cap) and the run is partial_data"
        results.append(_ctl("index download is charged to the library", library_ledger))

        def completeness():
            import tempfile
            good = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [{"gsm": f"GSMfx{i}", "label": f"fx{i}", "dpa": 0, "replicate": i, "fragments_url": srv.url("/a.gz"), "fragments_bytes": total,
                                   "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)} for i in (1, 2)]}
            doc, rec = wc.run(os.path.join(tempfile.mkdtemp(), "o"), proto, good, wc.http_fetch_factory(proto, [], [srv.host], "http"))
            assert rec["completion_status"] == "complete" and wc.EXIT_CODES[rec["completion_status"]] == 0, rec
            assert (rec["expected_identities"], rec["present_identities"], rec["usable_identities"]) == (6, 6, 6) and not rec["missing_identities"]

            def boom(url, total_, budget):
                raise ValueError("unexpected")
            d2, r2 = wc.run(os.path.join(tempfile.mkdtemp(), "o"), proto, good, boom)
            assert r2["completion_status"] == "stopped_on_error" and r2["error"] == "ValueError" and wc.EXIT_CODES["stopped_on_error"] == 4, r2
            assert len(r2["missing_identities"]) == 6
            b = wc.Budget(proto["bounds"] | {"total_requests_max": 1})
            d3, r3 = wc.run(os.path.join(tempfile.mkdtemp(), "o"), proto, good, wc.http_fetch_factory(proto, [], [srv.host], "http"), budget=b)
            assert r3["completion_status"] == "stopped_on_bound" and r3["missing_identities"] and wc.EXIT_CODES["stopped_on_bound"] == 2
            real = json.load(open(os.path.join(HERE, "controls.json")))
            assert len(wc.build_windows(real["controls"])) * len(real["libraries"]) == 330
            return "complete only with every identity present and usable (exit 0); error -> stopped_on_error (4); bound -> stopped_on_bound (2) with missing identities listed; real manifest expects 330"
        results.append(_ctl("completion status needs all identities present and usable", completeness))
    finally:
        srv.close()
    return {"schema": "frontier.reg-proxy.controls-run/1", "protocol_sha256": hashlib.sha256(open(os.path.join(HERE, "protocol.json"), "rb").read()).hexdigest(), "controls": results}


if __name__ == "__main__":
    r = run_all()
    print(json.dumps(r, indent=1))
    raise SystemExit(0 if all(x["passed"] for x in r["controls"]) else 1)
