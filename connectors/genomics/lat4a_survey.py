"""Spliced protein-to-genome survey of the lat4a (slc43a2a) and slc43a2b loci and the residues at the paper's positions 74, 106, 200 and 326.

Residues are read from the translated GENOME sequence, never from the query protein, so a query from another species cannot leak its own residue into the call.

  python -m connectors.genomics.lat4a_survey run  GENOME.fa[.gz] QUERIES.faa OUT.json --miniprot PATH [--threads N]
  python -m connectors.genomics.lat4a_survey pin  OUT_accessions.json           (queries NCBI Datasets + md5checksums.txt; network)

The reference numbering is zebrafish Ensembl ENSDARP00000120945 (slc43a2a, 571 aa) and ENSDARP00000156564 (slc43a2b, 598 aa), the proteins whose numbering matches Figures 3C and 2D.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from Bio import Align, SeqIO
from Bio.Align import substitution_matrices
from Bio.Seq import Seq

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "data" / "genomics" / "artifacts"
POSITIONS = (74, 106, 200, 326)
WIN_3C, WIN_2D = (194, 205), (319, 333)
MARGIN = 3.0  # percentage points of identity separating the two paralogs; below it the locus is called ambiguous
MIN_COVERAGE = (
    0.90  # fraction of the reference that must align before a residue is scored
)


def ref_protein(name: str) -> str:
    pid = {"a": "ENSDARP00000120945", "b": "ENSDARP00000156564"}[name]
    return "".join((ART / f"ensembl_protein_{pid}.fasta").read_text().split("\n")[1:])


def aligner() -> Align.PairwiseAligner:
    al = Align.PairwiseAligner()
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    al.open_gap_score, al.extend_gap_score, al.end_gap_score, al.mode = (
        -11,
        -1,
        0,
        "global",
    )
    return al


def parse_gff(text: str) -> list[dict]:
    """miniprot --gff: one mRNA line per alignment with its CDS lines after it."""
    hits, cur = [], None
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        f = line.split("\t")
        if len(f) < 9:
            continue
        attrs = dict(kv.split("=", 1) for kv in f[8].split(";") if "=" in kv)
        if f[2] == "mRNA":
            cur = {
                "contig": f[0],
                "start": int(f[3]),
                "end": int(f[4]),
                "strand": f[6],
                "score": f[5],
                "attrs": attrs,
                "cds": [],
            }
            hits.append(cur)
        elif f[2] == "CDS" and cur is not None:
            cur["cds"].append((int(f[3]), int(f[4])))
    return hits


def spliced(contig_seq: str, hit: dict) -> tuple[str, list[int]]:
    """CDS nucleotides in transcript orientation and the genomic coordinate (1-based) of every base."""
    segs = sorted(hit["cds"])
    nt, pos = [], []
    for s, e in segs:
        nt.append(contig_seq[s - 1 : e])
        pos.extend(range(s, e + 1))
    seq = "".join(nt)
    if hit["strand"] == "-":
        seq = str(Seq(seq).reverse_complement())
        pos = pos[::-1]
    return seq.upper(), pos


def align_to_refs(body: str, refs: dict[str, str], al) -> dict:
    ident = {}
    for k, ref in refs.items():
        a = al.align(ref, body.replace("*", "X"))[0]
        cov = int(
            sum(te - ts for ts, te in a.aligned[0])
        )  # a.aligned holds NumPy ints; keep every number below a Python int/float so it is JSON-native
        same = sum(
            1
            for (ts, te), (qs, qe) in zip(*a.aligned)
            for i in range(te - ts)
            if ref[ts + i] == body[qs + i]
        )
        ident[k] = {
            "identity_pct": round(100 * same / max(cov, 1), 2),
            "coverage_of_reference": round(cov / len(ref), 3),
            "aln": a,
        }
    return ident


def read_protein(body: str, refs: dict[str, str], al=None) -> dict:
    """Residues at the paper's positions from a protein alone (an annotation model). No codons: only a genome read has those."""
    al = al or aligner()
    ident = align_to_refs(body, refs, al)
    best = max(ident, key=lambda k: ident[k]["identity_pct"])
    other = "b" if best == "a" else "a"
    margin = ident[best]["identity_pct"] - ident[other]["identity_pct"]
    a = ident[best]["aln"]

    def col(rp):
        for (ts, te), (qs, qe) in zip(*a.aligned):
            if ts <= rp - 1 < te:
                return qs + (rp - 1 - ts)
        return None

    def win(r0, r1):
        return "".join(
            body[col(p)] if col(p) is not None else "-" for p in range(r0, r1 + 1)
        )

    return {
        "length": len(body),
        "identity_pct": {k: v["identity_pct"] for k, v in ident.items()},
        "paralog_call": f"slc43a2{best}-type" if margin >= MARGIN else "ambiguous",
        "residues": {
            str(rp): (None if col(rp) is None else body[col(rp)]) for rp in POSITIONS
        },
        "window_194_205": win(*WIN_3C),
        "window_319_333": win(*WIN_2D),
    }


def read_hit(contig_seq: str, hit: dict, refs: dict[str, str], al=None) -> dict:
    al = al or aligner()
    nt, pos = spliced(contig_seq, hit)
    prot = str(Seq(nt[: len(nt) // 3 * 3]).translate())
    body = prot.rstrip("*")
    out = {
        "contig": hit["contig"],
        "start": hit["start"],
        "end": hit["end"],
        "strand": hit["strand"],
        "query": hit["attrs"].get("Target", "").split()[0],
        "miniprot_score": hit["score"],
        "protein_length": len(body),
        "internal_stops": body.count("*"),
        "n_cds": len(hit["cds"]),
    }
    ident = align_to_refs(body, refs, al)
    best = max(ident, key=lambda k: ident[k]["identity_pct"])
    other = "b" if best == "a" else "a"
    margin = ident[best]["identity_pct"] - ident[other]["identity_pct"]
    out["identity_pct"] = {k: v["identity_pct"] for k, v in ident.items()}
    out["coverage_of_reference"] = {
        k: v["coverage_of_reference"] for k, v in ident.items()
    }
    out["paralog_call"] = f"slc43a2{best}-type" if margin >= MARGIN else "ambiguous"
    out["scored"] = bool(
        out["paralog_call"] != "ambiguous"
        and ident[best]["coverage_of_reference"] >= MIN_COVERAGE
        and out["internal_stops"] == 0
    )
    if not out["scored"]:
        out["not_scored_because"] = (
            "ambiguous paralog"
            if out["paralog_call"] == "ambiguous"
            else (
                "internal stop codon(s)"
                if out["internal_stops"]
                else "partial coverage of the reference"
            )
        )
        return out
    a = ident[best]["aln"]
    ref = refs[best]

    def col(
        rp,
    ):  # index in the translated protein aligned to 1-based reference position rp
        for (ts, te), (qs, qe) in zip(*a.aligned):
            if ts <= rp - 1 < te:
                return qs + (rp - 1 - ts)
        return None

    def win(r0, r1):
        return "".join(
            body[col(p)] if col(p) is not None else "-" for p in range(r0, r1 + 1)
        )

    res = {}
    for rp in POSITIONS:
        c = col(rp)
        res[str(rp)] = (
            None
            if c is None
            else {
                "aa": body[c],
                "codon": nt[3 * c : 3 * c + 3],
                "codon_first_base_genomic": pos[3 * c],
                "reference_aa": ref[rp - 1],
            }
        )
    out.update(
        {
            "reference_numbering_of": f"slc43a2{best}",
            "residues": res,
            "window_194_205": win(*WIN_3C),
            "window_319_333": win(*WIN_2D),
            "positions_missing": [rp for rp, v in res.items() if v is None],
        }
    )
    return out


def loci(reads: list[dict]) -> list[dict]:
    """One row per locus. Several queries align to the same locus; keep the read with every position aligned, then the highest identity to its own type.
    A locus with no such read is reported as not scored, never filled in."""
    groups: dict[tuple, list[dict]] = {}
    for r in reads:
        groups.setdefault((r["contig"], r["strand"], r["start"] // 20000), []).append(
            r
        )  # 20 kb bins merge near-identical alignments of one gene
    rows = []
    for key, rs in sorted(groups.items()):
        good = [r for r in rs if r["scored"] and not r["positions_missing"]]
        best = (
            max(good, key=lambda r: max(r["identity_pct"].values())) if good else None
        )
        rows.append(
            {
                "contig": key[0],
                "strand": key[1],
                "n_queries_aligned": len(rs),
                "call": best["paralog_call"] if best else "not scored",
                "residues": {k: v["aa"] for k, v in best["residues"].items()}
                if best
                else None,
                "windows": [best["window_194_205"], best["window_319_333"]]
                if best
                else None,
                "codon_326": best["residues"]["326"]["codon"] if best else None,
                "why_not_scored": None
                if best
                else sorted(
                    {
                        r.get("not_scored_because", "a position was not aligned")
                        for r in rs
                    }
                ),
            }
        )
    return rows


def load_contigs(genome: Path, wanted: set[str]) -> dict[str, str]:
    op = gzip.open if str(genome).endswith(".gz") else open
    got = {}
    with op(genome, "rt") as fh:
        for rec in SeqIO.parse(fh, "fasta"):
            if rec.id in wanted:
                got[rec.id] = str(rec.seq)
                if len(got) == len(wanted):
                    break
    return got


def run(genome: Path, queries: Path, miniprot: str, threads: int = 2) -> dict:
    proc = subprocess.run(
        [miniprot, "-t", str(threads), "--gff", str(genome), str(queries)],
        capture_output=True,
        text=True,
        check=True,
    )
    hits = parse_gff(proc.stdout)
    contigs = load_contigs(genome, {h["contig"] for h in hits})
    refs = {"a": ref_protein("a"), "b": ref_protein("b")}
    al = aligner()
    reads = [read_hit(contigs[h["contig"]], h, refs, al) for h in hits]
    return {
        "genome": str(genome.name),
        "genome_sha256": hashlib.sha256(Path(genome).read_bytes()).hexdigest()
        if Path(genome).stat().st_size < 3_000_000_000
        else None,
        "miniprot": subprocess.run(
            [miniprot, "--version"], capture_output=True, text=True
        ).stdout.strip(),
        "queries": [r.id for r in SeqIO.parse(queries, "fasta")],
        "n_alignments": len(reads),
        "loci": loci(reads),
        "reads": reads,
    }


def pin(out: Path) -> dict:
    """Select one assembly per Beloniformes species (RefSeq first, then scaffold N50, then newest) and pin each genomic.fna.gz by the md5 NCBI publishes."""
    import urllib.request

    def get(url: str, timeout: int = 60) -> bytes:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "delphi-frontier-pin/0.1",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()

    rep = json.loads(
        get(
            "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Beloniformes/dataset_report?page_size=200&filters.exclude_atypical=true"
        )
    )
    reports = rep["reports"]
    assert rep["total_count"] == len(reports), "the listing is complete"
    by_species: dict[str, list[dict]] = {}
    for r in reports:
        by_species.setdefault(r["organism"]["organism_name"], []).append(r)

    def rank(r):
        return (
            r["accession"].startswith("GCF_"),
            int(r.get("assembly_stats", {}).get("scaffold_n50", 0)),
            r["assembly_info"].get("release_date", ""),
        )

    rows = []
    for sp, rs in sorted(by_species.items()):
        r = max(rs, key=rank)
        acc = r["accession"]
        name = r["assembly_info"]["assembly_name"].replace(" ", "_")
        base = f"https://ftp.ncbi.nlm.nih.gov/genomes/all/{acc[:3]}/{acc[4:7]}/{acc[7:10]}/{acc[10:13]}/{acc}_{name}"
        fn = f"{acc}_{name}_genomic.fna.gz"
        md5 = {
            ln.split()[1].lstrip("./"): ln.split()[0]
            for ln in get(base + "/md5checksums.txt").decode().splitlines()
            if ln.strip()
        }
        rows.append(
            {
                "species": sp,
                "accession": acc,
                "assembly_name": name,
                "assembly_level": r["assembly_info"].get("assembly_level"),
                "total_length": int(r["assembly_stats"]["total_sequence_length"]),
                "scaffold_n50": int(r["assembly_stats"].get("scaffold_n50", 0)),
                "release_date": r["assembly_info"].get("release_date"),
                "refseq": acc.startswith("GCF_"),
                "url": f"{base}/{fn}",
                "md5": md5[fn],
                "other_assemblies_of_the_species": sorted(
                    x["accession"] for x in rs if x["accession"] != acc
                ),
            }
        )
    res = {
        "schema": "lat4a-survey-accessions-0.1 (connector-local)",
        "source": "NCBI Datasets v2 genome/taxon/Beloniformes dataset_report + FTP md5checksums.txt",
        "n_reports_in_listing": len(reports),
        "selection_rule": "per species: RefSeq, then largest scaffold N50, then newest release",
        "total_download_note": "sum of total_length is uncompressed bases; the .gz files are smaller",
        "total_bases": sum(r["total_length"] for r in rows),
        "assemblies": rows,
    }
    Path(out).write_text(json.dumps(res, indent=1, sort_keys=True))
    return res


def annotation(out: Path) -> dict:
    """The mirrorwing annotation's SLC43A2-hit models (chosen from the stored SwissProt best-hit table, not by hand) read against the zebrafish references."""
    import csv

    refs = {"a": ref_protein("a"), "b": ref_protein("b")}
    prot = {
        r.id.split()[0]: str(r.seq)
        for r in SeqIO.parse(ART / "flyingfish_selected_proteins.faa", "fasta")
    }
    hits = [
        r
        for r in csv.DictReader(
            open(ART / "flyingfish_swissprot_best_hits_selected.tsv"), delimiter="\t"
        )
        if r["GN"] == "SLC43A2"
    ]
    al = aligner()
    # the proteins are keyed by GHS id in the FASTA and by HsScaf id in the table: join through the FASTA header, which carries both
    hdr = {}
    for line in (ART / "flyingfish_selected_proteins.faa").read_text().splitlines():
        if line.startswith(">"):
            ghs, scaf = line[1:].split()[0], line[1:].split()[1]
            hdr[scaf] = ghs
    res = []
    for h in hits:
        ghs = hdr[h["Query_id"]]
        r = read_protein(prot[ghs], refs, al)
        r.update(
            {
                "model": ghs,
                "scaffold_gene_id": h["Query_id"],
                "swissprot_best_subject": h["Best_subject"],
                "swissprot_identity_pct": float(h["Identity"]),
                "protein_sha256": hashlib.sha256(prot[ghs].encode()).hexdigest(),
            }
        )
        res.append(r)
    d = {
        "schema": "flyingfish-annotation-lat4a-0.1 (connector-local)",
        "species": "Hirundichthys speculiger (Exocoetidae, mirrorwing flyingfish)",
        "source": "figshare 10.6084/m9.figshare.14600634.v1 (CC BY 4.0) predicted proteins, stored selection",
        "method": "global BLOSUM62 alignment to the zebrafish references, read at the reference positions; the call is the paralog with the higher identity (margin >= %.0f points)"
        % MARGIN,
        "read_level": "annotation (predicted protein), not the assembly: residues come from a gene prediction",
        "models": sorted(res, key=lambda r: r["model"]),
        "limits": [
            "gene predictions, not the genome sequence; the assembly-level read is the survey's job",
            "only models with an SLC43A2 SwissProt best hit were read; other loci are not assumed absent",
        ],
    }
    Path(out).write_text(json.dumps(d, indent=1, sort_keys=True))
    return d


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("genome")
    r.add_argument("queries")
    r.add_argument("out")
    r.add_argument("--miniprot", required=True)
    r.add_argument("--threads", type=int, default=2)
    pn = sub.add_parser("pin")
    pn.add_argument("out")
    an = sub.add_parser("annotation")
    an.add_argument("out")
    a = ap.parse_args(argv)
    if a.cmd == "annotation":
        d = annotation(Path(a.out))
        print(
            a.out,
            [
                (m["model"], m["paralog_call"], m["residues"]["326"])
                for m in d["models"]
            ],
        )
        return 0
    if a.cmd == "pin":
        res = pin(Path(a.out))
        print(
            a.out,
            len(res["assemblies"]),
            "species,",
            round(res["total_bases"] / 1e9, 2),
            "Gb",
        )
        return 0
    res = run(Path(a.genome), Path(a.queries), a.miniprot, a.threads)
    Path(a.out).write_text(json.dumps(res, indent=1, sort_keys=True))
    print(a.out, res["n_alignments"], "alignments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
