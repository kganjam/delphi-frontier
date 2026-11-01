"""Orchestrates the lat4a survey over the pinned assemblies: download, md5 check, align, read residues, delete its own download, resume by skipping finished species.

  python -m connectors.genomics.lat4a_survey_job run --accessions A.json --queries Q.faa --shuffled S.faa --miniprot PATH --workdir W --out O [--workers 3] [--threads 2] [--only "Oryzias latipes"]
  python -m connectors.genomics.lat4a_survey_job summarize --accessions A.json --predictions P.json --out O

Only files this job created inside --workdir are deleted. Nothing outside --workdir and --out is written. Public data only.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import resource
import sys
import time
import urllib.request
from pathlib import Path

from connectors.genomics import lat4a_survey as LS


def download(url: str, dest: Path, expect_md5: str) -> dict:
    t0 = time.time()
    md5 = hashlib.md5()
    n = 0
    req = urllib.request.Request(
        url, headers={"User-Agent": "delphi-frontier-survey/0.1"}
    )
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
            md5.update(chunk)
            n += len(chunk)
    if md5.hexdigest() != expect_md5:
        dest.unlink()
        raise RuntimeError(f"md5 mismatch for {url}: {md5.hexdigest()} != {expect_md5}")
    return {"bytes": n, "seconds": round(time.time() - t0, 1), "md5_ok": True}


def one(
    row: dict,
    queries: Path,
    shuffled: Path | None,
    miniprot: str,
    work: Path,
    out: Path,
    threads: int,
    shuffled_control: bool,
) -> dict:
    res_path = out / f"{row['accession']}.json"
    if res_path.exists():
        return {"accession": row["accession"], "skipped": "already done"}
    g = work / f"{row['accession']}.fna.gz"
    rec = {
        "accession": row["accession"],
        "species": row["species"],
        "pinned_md5": row["md5"],
        "url": row["url"],
    }
    try:
        rec["download"] = download(row["url"], g, row["md5"])
        t0 = time.time()
        res = LS.run(g, queries, miniprot, threads)
        rec["align_seconds"] = round(time.time() - t0, 1)
        res["accession"], res["species"], res["download"] = (
            row["accession"],
            row["species"],
            rec["download"],
        )
        res_path.write_text(json.dumps(res, indent=1, sort_keys=True))
        if shuffled_control and shuffled is not None:
            sh = LS.run(g, shuffled, miniprot, threads)
            (out / f"{row['accession']}.shuffled.json").write_text(
                json.dumps(
                    {
                        "accession": row["accession"],
                        "n_alignments": sh["n_alignments"],
                        "loci": sh["loci"],
                    },
                    indent=1,
                    sort_keys=True,
                )
            )
            rec["shuffled_alignments"] = sh["n_alignments"]
        rec["n_loci"] = len(res["loci"])
        rec["maxrss_children_mb"] = round(
            resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
        )  # peak of any child so far in this process: an upper bound for this species
    finally:
        if g.exists() and g.parent == work:
            g.unlink()  # the job's own download, inside its own workdir
    with open(out / "progress.jsonl", "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def summarize(acc_path: Path, pred_path: Path, out: Path) -> dict:
    acc = {r["accession"]: r for r in json.loads(acc_path.read_text())["assemblies"]}
    pred = {p["accession"]: p for p in json.loads(pred_path.read_text())["predictions"]}
    rows, ctl = [], {}
    for a, r in sorted(acc.items(), key=lambda kv: kv[1]["species"]):
        f = out / f"{a}.json"
        if not f.exists():
            rows.append({"species": r["species"], "accession": a, "status": "not run"})
            continue
        d = json.loads(f.read_text())
        L = d["loci"]
        at = [x for x in L if x["call"] == "slc43a2a-type"]
        bt = [x for x in L if x["call"] == "slc43a2b-type"]
        ns = [x for x in L if x["call"] == "not scored"]
        exp = pred[a]["expected_aa_at_326_slc43a2a_type"]
        got = sorted({x["residues"]["326"] for x in at})
        rows.append(
            {
                "species": r["species"],
                "accession": a,
                "family": pred[a]["family"],
                "status": "scored" if at else "no scored a-type locus",
                "a_type_loci": len(at),
                "b_type_loci": len(bt),
                "not_scored_loci": len(ns),
                "a_326": "/".join(got) or None,
                "a_200": "/".join(sorted({x["residues"]["200"] for x in at})) or None,
                "a_codon_326": "/".join(sorted({x["codon_326"] for x in at})) or None,
                "b_200_326": sorted(
                    {x["residues"]["200"] + x["residues"]["326"] for x in bt}
                )
                or None,
                "expected_326": exp,
                "prediction_kind": pred[a]["kind"],
                "as_predicted": (got == [exp]) if at else None,
                "why_not_scored": sorted(
                    {w for x in ns for w in (x["why_not_scored"] or [])}
                )
                or None,
            }
        )
    sh = {
        a: json.loads((out / f"{a}.shuffled.json").read_text())["n_alignments"]
        for a in acc
        if (out / f"{a}.shuffled.json").exists()
    }
    ctl["shuffled_query_alignments"] = sh
    ctl["shuffled_query_clean"] = all(v == 0 for v in sh.values()) if sh else None
    scored = [r for r in rows if r["status"] == "scored"]
    summ = {
        "schema": "lat4a-survey-summary-0.1",
        "n_species_pinned": len(acc),
        "n_run": sum(1 for r in rows if r["status"] != "not run"),
        "n_with_scored_a_type_locus": len(scored),
        "n_as_predicted": sum(1 for r in scored if r["as_predicted"]),
        "deviations": [r["species"] for r in scored if not r["as_predicted"]],
        "controls": ctl,
        "rows": rows,
    }
    (out / "summary.json").write_text(json.dumps(summ, indent=1, sort_keys=True))
    keys = [
        "species",
        "accession",
        "family",
        "status",
        "a_type_loci",
        "b_type_loci",
        "not_scored_loci",
        "a_326",
        "a_200",
        "a_codon_326",
        "b_200_326",
        "expected_326",
        "prediction_kind",
        "as_predicted",
        "why_not_scored",
    ]
    with open(out / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        [
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in keys})
            for r in rows
        ]
    return summ


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    for k in ("--accessions", "--queries", "--miniprot", "--workdir", "--out"):
        r.add_argument(k, required=True)
    r.add_argument("--shuffled")
    r.add_argument("--workers", type=int, default=3)
    r.add_argument("--threads", type=int, default=2)
    r.add_argument("--only", action="append")
    r.add_argument("--shuffled-control-on", type=int, default=2)
    s = sub.add_parser("summarize")
    s.add_argument("--accessions", required=True)
    s.add_argument("--predictions", required=True)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "summarize":
        m = summarize(Path(a.accessions), Path(a.predictions), Path(a.out))
        print(
            {
                k: m[k]
                for k in (
                    "n_species_pinned",
                    "n_run",
                    "n_with_scored_a_type_locus",
                    "n_as_predicted",
                    "deviations",
                )
            }
        )
        return 0
    rows = json.loads(Path(a.accessions).read_text())["assemblies"]
    assert len({x["accession"] for x in rows}) == len(rows), (
        "accessions must be unique: each one owns a download path and a result file"
    )
    if a.only:
        rows = [x for x in rows if x["species"] in a.only]
    work, out = Path(a.workdir), Path(a.out)
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    shuffled = Path(a.shuffled) if a.shuffled else None
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [
            ex.submit(
                one,
                x,
                Path(a.queries),
                shuffled,
                a.miniprot,
                work,
                out,
                a.threads,
                i < a.shuffled_control_on,
            )
            for i, x in enumerate(rows)
        ]
        for f in cf.as_completed(futs):
            try:
                print(f.result())
            except Exception as e:  # one species failing must not stop the others; the failure is recorded
                print("FAILED", repr(e))
                (out / "failures.log").open("a").write(repr(e) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
