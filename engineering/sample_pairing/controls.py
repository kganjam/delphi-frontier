"""Focused controls on small SYNTHETIC SOFT fixtures. They run the same parse/pair/fetch/run code used remotely."""
import copy
import os
import tempfile

from engineering.sample_pairing import audit


def soft(gsm, strategy, bio, dpa="1", rep="1", assembly="danRer11", title=None, organism="Danio rerio", extra=""):
    lib = "RNA" if strategy == "RNA-Seq" else "ATAC"
    t = title if title is not None else f"Caudal fin, {dpa}dpa, 10X Multiome sn{lib}, rep{rep}"
    asm = f"!Sample_data_processing = Assembly: {assembly}\n" if assembly else ""
    return (f"^SAMPLE = {gsm}\n!Sample_title = {t}\n!Sample_organism_ch1 = {organism}\n!Sample_characteristics_ch1 = tissue: Caudal fin\n"
            f"!Sample_characteristics_ch1 = time post_amputation_(days): {dpa}\n{asm}!Sample_library_strategy = {strategy}\n"
            f"!Sample_relation = BioSample: https://www.ncbi.nlm.nih.gov/biosample/{bio}\n{extra}")


def recs(*texts):
    proto, _ = audit.load_protocol()
    out = []
    for t in texts:
        acc = t.split("\n", 1)[0].split(" = ")[1]
        out.append(audit.sample_record(acc, audit.parse_soft(t), proto))
    return out


def status_of(*texts):
    pairs, _ = audit.pair(recs(*texts))
    return [p["status"] for p in pairs]


class FakeResp:
    def __init__(self, data, status=200):
        self.data, self.status = data, status

    def read(self, n=-1):
        return self.data if n < 0 else self.data[:n]

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeOpener:
    def __init__(self, pages):
        self.pages, self.seen = pages, []

    def open(self, req, timeout=0):
        acc = req.full_url.split("acc=")[1].split("&")[0]
        self.seen.append(req.full_url)
        return FakeResp(self.pages[acc].encode() if isinstance(self.pages[acc], str) else self.pages[acc])


def series(gsms):
    return "^SERIES = GSE261907\n" + "".join(f"!Series_sample_id = {g}\n" for g in gsms)


def good_site(n=2):
    pages, gsms = {}, []
    for i in range(n):
        r, a = f"GSM9{i:06d}", f"GSM9{i + 500:06d}"
        pages[r] = soft(r, "RNA-Seq", f"SAMN{i}", dpa=str(i), rep="1")
        pages[a] = soft(a, "ATAC-seq", f"SAMN{i}", dpa=str(i), rep="1")
        gsms += [r, a]
    pages["GSE261907"] = series(gsms)
    return pages


def run_with(pages, proto=None, **kw):
    proto = proto or audit.load_protocol()[0]
    op = FakeOpener(pages)
    d = os.path.join(tempfile.mkdtemp(), "out")
    res = audit.run(d, proto, "x", fetcher=lambda acc, p: audit.fetch(acc, p, opener=op), sleep=lambda s: None, **kw)
    return res, op, d


def run_all():
    c = {}
    c["matched_pair_accepted"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1"), soft("GSM2", "ATAC-seq", "SAMN1")) == ["matched"]
    c["alias_danRer11_GRCz11_equal"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", assembly="danRer11"), soft("GSM2", "ATAC-seq", "SAMN1", assembly="GRCz11")) == ["matched"]
    c["swapped_replicate_refused"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", rep="1"), soft("GSM2", "ATAC-seq", "SAMN1", rep="2")) == ["unresolved_conflict"]
    c["missing_replicate_unresolved"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", title="Caudal fin, 1dpa, RNA"), soft("GSM2", "ATAC-seq", "SAMN1")) == ["unresolved_missing_identity"]
    c["assembly_mismatch_refused"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", assembly="danRer11"), soft("GSM2", "ATAC-seq", "SAMN1", assembly="danRer10")) == ["assembly_mismatch"]
    c["missing_assembly_refused"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", assembly=None), soft("GSM2", "ATAC-seq", "SAMN1")) == ["unresolved_missing_identity"]
    c["many_to_many_ambiguous"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1"), soft("GSM2", "RNA-Seq", "SAMN1"), soft("GSM3", "ATAC-seq", "SAMN1"), soft("GSM4", "ATAC-seq", "SAMN1")) == ["unresolved_ambiguous"]
    # identical barcode file names / titles under different BioSamples must not pair
    c["shared_barcode_strings_do_not_pair"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", extra="!Sample_supplementary_file_1 = x_barcodes.tsv.gz\n"), soft("GSM2", "ATAC-seq", "SAMN2", extra="!Sample_supplementary_file_1 = x_barcodes.tsv.gz\n")) == ["unresolved_missing_identity", "unresolved_missing_identity"]
    c["label_reused_across_biosamples_conflict"] = "matched" not in status_of(soft("GSM1", "RNA-Seq", "SAMN1"), soft("GSM2", "ATAC-seq", "SAMN1"), soft("GSM3", "RNA-Seq", "SAMN9"), soft("GSM4", "ATAC-seq", "SAMN9"))
    c["wrong_organism_unresolved"] = status_of(soft("GSM1", "RNA-Seq", "SAMN1", organism="Mus musculus"), soft("GSM2", "ATAC-seq", "SAMN1")) == ["unresolved_missing_identity"]
    # run(): complete, byte bound, request bound, over-large series, host allowlist, existing dir
    res, op, d = run_with(good_site(2))
    c["run_complete_keeps_everything"] = (res["completion_status"] == "complete" and res["summary"]["library_status_counts"] == {"matched": 4}
                                          and os.path.exists(os.path.join(d, "raw", "GSE261907.soft.txt")) and len(op.seen) == 5
                                          and all(u.startswith("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=") for u in op.seen))
    big = good_site(2)
    big["GSM9000001"] = "x" * 300000
    res, _, d2 = run_with(big)
    c["byte_bound_refused_partial_kept"] = (res["completion_status"] == "stopped_on_bound" and any("exceeds" in e for e in res["errors"])
                                            and res["summary"]["libraries_admitted"] == 2 and os.path.exists(os.path.join(d2, "raw", "GSM9000000.soft.txt"))
                                            and not os.path.exists(os.path.join(d2, "raw", "GSM9000001.soft.txt")))
    p2 = copy.deepcopy(audit.load_protocol()[0])
    p2["retrieval"]["max_total_bytes_compressed"] = 600
    res, _, _ = run_with(good_site(2), proto=p2)
    c["total_byte_bound_stops"] = res["completion_status"] == "stopped_on_bound"
    res, _, _ = run_with(dict(good_site(2), GSE261907=series([f"GSM{i}" for i in range(21)])))
    c["oversized_series_refused"] = res["completion_status"] == "stopped_on_bound" and res["samples"] == []
    p3 = copy.deepcopy(audit.load_protocol()[0])
    p3["retrieval"]["allowed_hosts"] = ["example.org"]
    try:
        audit.url_for("GSE261907", p3)
        c["host_allowlist_enforced"] = False
    except AssertionError:
        c["host_allowlist_enforced"] = True
    try:
        audit.url_for("GSM1; rm", audit.load_protocol()[0])
        c["non_accession_url_refused"] = False
    except AssertionError:
        c["non_accession_url_refused"] = True
    try:
        audit.run(d, audit.load_protocol()[0], "x")
        c["existing_output_refused"] = False
    except FileExistsError:
        c["existing_output_refused"] = True
    c["unavailable_series_status"] = run_with({"GSE261907": "^SERIES = GSE261907\n"})[0]["completion_status"] == "series_unavailable"
    return c


if __name__ == "__main__":
    r = run_all()
    print(r)
    raise SystemExit(0 if all(r.values()) else 1)
