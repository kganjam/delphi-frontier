"""The lat4a survey packet: pins, pre-registered predictions, the residue reader (both strands), the orchestrator's refusals, and the host-sized annotation result."""

import hashlib
import json
import os
import random
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
pytest.importorskip("Bio")
from connectors.genomics import lat4a_survey as LS  # noqa: E402
from connectors.genomics import lat4a_survey_job as JOB  # noqa: E402

D = ROOT / "data" / "genomics"
V = D / "lat4a_survey"


def J(path):
    return json.loads(Path(path).read_text())


def test_pins_are_complete_unique_and_checksummed():
    a = J(V / "accessions.json")
    rows = a["assemblies"]
    assert a["n_reports_in_listing"] == 75 and len(rows) == 23
    assert (
        len({r["species"] for r in rows}) == len({r["accession"] for r in rows}) == 23
    ), "one assembly per species"
    for r in rows:
        assert len(r["md5"]) == 32 and set(r["md5"]) <= set("0123456789abcdef"), r[
            "species"
        ]
        assert r["url"].startswith("https://ftp.ncbi.nlm.nih.gov/genomes/all/") and r[
            "url"
        ].endswith(f"{r['accession']}_{r['assembly_name']}_genomic.fna.gz")
        assert r["accession"] not in r["other_assemblies_of_the_species"]
    assert (
        a["total_bases"] == sum(r["total_length"] for r in rows)
        and 18.0e9 < a["total_bases"] < 19.5e9
    )
    ff = next(r for r in rows if r["species"] == "Hirundichthys speculiger")
    assert (
        ff["accession"] == "GCA_018398805.1" and ff["assembly_level"] == "Scaffold"
    ), "the only flying-fish (Exocoetidae) genome in the listing"
    assert [r["species"] for r in rows if r["refseq"]] == [
        "Cololabis saira",
        "Oryzias latipes",
        "Oryzias melastigma",
    ]


def test_predictions_cover_every_pin_once_and_separate_the_paper_from_extrapolation():
    p = J(V / "predictions.json")
    acc = {r["accession"] for r in J(V / "accessions.json")["assemblies"]}
    got = [x["accession"] for x in p["predictions"]]
    assert sorted(got) == sorted(acc) and p["registered_before_any_survey_run"] is True
    kinds = {x["kind"] for x in p["predictions"]}
    assert kinds == {
        "stated_by_paper",
        "stated_by_paper_for_congener",
        "stated_by_paper_and_prechecked_on_annotation",
        "extrapolated",
    }
    L = [x for x in p["predictions"] if x["expected_aa_at_326_slc43a2a_type"] == "L"]
    assert [x["family"] for x in L] == ["Exocoetidae"] and L[0][
        "species"
    ] == "Hirundichthys speculiger"
    assert all(
        x["expected_aa_at_200_slc43a2a_type"] == "T"
        and x["expected_slc43a2b_type_326_200"] == ["D", "M"]
        for x in p["predictions"]
    )
    assert not any("observed" in x or "result" in x for x in p["predictions"]), (
        "a prediction file holds no results"
    )
    assert (
        "flying halfbeak" in p["how_to_read"].lower()
        and "untestable" in p["how_to_read"]
    )


def test_shuffled_control_keeps_the_composition_and_destroys_the_order():
    ref = LS.ref_protein("a")
    sh = "".join(Path(V / "queries_shuffled.faa").read_text().split("\n")[1:])
    assert (
        sorted(sh) == sorted(ref)
        and sh != ref
        and len(sh) == 571
        and LS.WIN_3C
        and "YASSAVTFPGIK" not in sh
    )


def toy_gene(strand):
    """A synthetic two-exon gene with a known protein, on the requested strand, with GT..AG introns."""
    rng = random.Random(7)
    codon = {
        "M": "ATG",
        "L": "CTG",
        "F": "TTC",
        "T": "ACA",
        "K": "AAG",
        "S": "TCC",
        "G": "GGC",
        "D": "GAC",
        "A": "GCC",
        "V": "GTG",
    }
    prot = "M" + "".join(rng.choice("LFTKSGDAV") for _ in range(59))
    cds = "".join(codon[a] for a in prot)
    e1, e2 = cds[:90], cds[90:]
    intron = "GT" + "ACGT" * 10 + "AG"
    plus = "N" * 50 + e1 + intron + e2 + "N" * 50
    s1, e1_end = 51, 50 + len(e1)
    s2 = e1_end + len(intron) + 1
    segs = [(s1, e1_end), (s2, s2 + len(e2) - 1)]
    if strand == "-":
        from Bio.Seq import Seq

        L = len(plus)
        contig = str(Seq(plus).reverse_complement())
        segs = sorted((L - b + 1, L - a + 1) for a, b in segs)
        return prot, contig, segs
    return prot, plus, segs


@pytest.mark.parametrize("strand", ["+", "-"])
def test_spliced_translation_recovers_a_known_protein_on_both_strands(strand):
    prot, contig, segs = toy_gene(strand)
    nt, pos = LS.spliced(contig, {"strand": strand, "cds": segs})
    from Bio.Seq import Seq

    assert str(Seq(nt).translate()) == prot and len(pos) == len(nt)
    assert contig[pos[0] - 1] in "ACGTN" and (pos[0] > pos[1]) == (strand == "-"), (
        "the coordinate list runs against the contig on the minus strand"
    )


def test_parse_gff_groups_cds_under_their_mrna():
    gff = "##gff-version 3\nc1\tminiprot\tmRNA\t10\t90\t500\t-\t.\tID=MP1;Rank=1;Target=q1 1 30\nc1\tminiprot\tCDS\t10\t40\t.\t-\t0\tParent=MP1\nc1\tminiprot\tCDS\t60\t90\t.\t-\t1\tParent=MP1\nc2\tminiprot\tmRNA\t5\t50\t90\t+\t.\tID=MP2;Target=q2 1 15\nc2\tminiprot\tCDS\t5\t50\t.\t+\t0\tParent=MP2\n"
    h = LS.parse_gff(gff)
    assert [(x["contig"], x["strand"], len(x["cds"])) for x in h] == [
        ("c1", "-", 2),
        ("c2", "+", 1),
    ] and h[0]["attrs"]["Target"].startswith("q1")


def test_validation_slices_read_the_genome_not_the_query_and_match_an_independent_source():
    a, b = (
        J(V / "validation_slice_result.json"),
        J(V / "validation_slice_chr10_result.json"),
    )
    assert (a["n_alignments"], b["n_alignments"]) == (5, 5)
    for res, call, aa, codon, strand in (
        (
            a,
            "slc43a2a-type",
            {"74": "L", "106": "L", "200": "T", "326": "F"},
            "TTC",
            "+",
        ),
        (
            b,
            "slc43a2b-type",
            {"74": "P", "106": "G", "200": "M", "326": "D"},
            "GAC",
            "-",
        ),
    ):
        assert (
            len(res["loci"]) == 1
            and res["loci"][0]["call"] == call
            and res["loci"][0]["strand"] == strand
        )
        assert res["loci"][0]["residues"] == aa and res["loci"][0]["codon_326"] == codon
        for r in res["reads"]:
            assert (
                r["scored"]
                and r["positions_missing"] in ([], ["74"])
                and r["paralog_call"] == call
            ), "every query, including the other paralog's, gets the genome's call"
            for k, v in r["residues"].items():
                if v is not None:
                    assert v["aa"] == v["reference_aa"], (
                        "genome translation == the Ensembl reference protein at every position (an independent source)"
                    )
    assert a["loci"][0]["windows"] == ["YASSAVTFPGIK", "QSFMRSIFSPIFMLS"], (
        "the two figure windows, typed independently of the module"
    )
    assert a["miniprot"] == "0.18-r281"


def test_annotation_result_matches_the_papers_flying_fish_row_and_is_labelled_a_prediction():
    d = J(D / "flyingfish_annotation_lat4a_v1.json")
    m = {x["model"]: x for x in d["models"]}
    assert (
        set(m) == {"GHS15055", "GHS07715"}
        and "annotation (predicted protein)" in d["read_level"]
    )
    g = m["GHS15055"]
    assert (
        g["paralog_call"] == "slc43a2a-type"
        and g["residues"]["326"] == "L"
        and g["residues"]["200"] == "T"
        and g["identity_pct"]["a"] > g["identity_pct"]["b"] + 3
    )
    assert g["window_319_333"] == "QSFMKSILSPIFLLS", (
        "identical to the paper's Cheilopogon furcatus row (read at 400 dpi from Figure 2D), typed here independently"
    )
    assert g["window_194_205"] == "YASSAVTFPGIK"
    b = m["GHS07715"]
    assert b["paralog_call"] == "slc43a2b-type" and (
        b["residues"]["200"],
        b["residues"]["326"],
    ) == ("M", "D")
    faa = {}
    cur = None
    for line in (
        (D / "artifacts" / "flyingfish_selected_proteins.faa").read_text().splitlines()
    ):
        if line.startswith(">"):
            cur = line[1:].split()[0]
            faa[cur] = ""
        else:
            faa[cur] += line.strip()
    assert hashlib.sha256(faa["GHS15055"].encode()).hexdigest() == g["protein_sha256"]
    assert any("assembly-level read is the survey" in x for x in d["limits"])


def test_download_refuses_a_wrong_md5_and_leaves_no_file(tmp_path):
    src = tmp_path / "g.fa.gz"
    src.write_bytes(b"not a genome")
    dest = tmp_path / "out.gz"
    with pytest.raises(RuntimeError, match="md5 mismatch"):
        JOB.download(src.resolve().as_uri(), dest, "0" * 32)
    assert not dest.exists()
    ok = JOB.download(
        src.resolve().as_uri(), dest, hashlib.md5(b"not a genome").hexdigest()
    )
    assert ok["md5_ok"] is True and ok["bytes"] == 12 and dest.exists()


def test_run_refuses_duplicate_accessions(tmp_path):
    rows = [
        {"species": "A", "accession": "X1", "url": "file:///x", "md5": "0" * 32},
        {"species": "B", "accession": "X1", "url": "file:///y", "md5": "0" * 32},
    ]
    (tmp_path / "acc.json").write_text(json.dumps({"assemblies": rows}))
    with pytest.raises(AssertionError, match="accessions must be unique"):
        JOB.main(
            [
                "run",
                "--accessions",
                str(tmp_path / "acc.json"),
                "--queries",
                str(V / "queries.faa"),
                "--miniprot",
                "/bin/false",
                "--workdir",
                str(tmp_path / "w"),
                "--out",
                str(tmp_path / "o"),
            ]
        )


def test_summarize_scores_agreement_deviation_and_not_run(tmp_path):
    acc = {
        "assemblies": [
            {"species": s, "accession": a}
            for s, a in (
                ("Sp one", "A1"),
                ("Sp two", "A2"),
                ("Sp three", "A3"),
                ("Sp four", "A4"),
            )
        ]
    }
    pred = {
        "predictions": [
            {
                "accession": a,
                "family": "f",
                "expected_aa_at_326_slc43a2a_type": e,
                "kind": "stated_by_paper",
            }
            for a, e in (("A1", "F"), ("A2", "F"), ("A3", "L"), ("A4", "F"))
        ]
    }
    (tmp_path / "acc.json").write_text(json.dumps(acc))
    (tmp_path / "pred.json").write_text(json.dumps(pred))

    def locus(call, a326, a200="T"):
        return {
            "call": call,
            "residues": {"74": "L", "106": "L", "200": a200, "326": a326},
            "codon_326": "TTC",
            "why_not_scored": None,
            "windows": ["", ""],
        }

    (tmp_path / "A1.json").write_text(
        json.dumps(
            {"loci": [locus("slc43a2a-type", "F"), locus("slc43a2b-type", "D", "M")]}
        )
    )
    (tmp_path / "A2.json").write_text(
        json.dumps({"loci": [locus("slc43a2a-type", "L")]})
    )  # a deviation from the prediction
    (tmp_path / "A3.json").write_text(
        json.dumps(
            {
                "loci": [
                    {
                        "call": "not scored",
                        "residues": None,
                        "codon_326": None,
                        "windows": None,
                        "why_not_scored": ["partial coverage of the reference"],
                    }
                ]
            }
        )
    )
    (tmp_path / "A1.shuffled.json").write_text(json.dumps({"n_alignments": 0}))
    s = JOB.summarize(tmp_path / "acc.json", tmp_path / "pred.json", tmp_path)
    by = {r["species"]: r for r in s["rows"]}
    assert (
        by["Sp one"]["as_predicted"] is True
        and by["Sp two"]["as_predicted"] is False
        and by["Sp three"]["status"] == "no scored a-type locus"
        and by["Sp four"]["status"] == "not run"
    )
    assert by["Sp three"]["as_predicted"] is None and by["Sp three"][
        "why_not_scored"
    ] == ["partial coverage of the reference"], (
        "an unscored locus is reported, never filled in"
    )
    assert (
        s["deviations"] == ["Sp two"]
        and s["n_as_predicted"] == 1
        and s["n_with_scored_a_type_locus"] == 2
        and s["controls"]["shuffled_query_clean"] is True
    )
    assert (
        (tmp_path / "summary.csv")
        .read_text()
        .splitlines()[0]
        .startswith("species,accession,family,status")
    )


MINIPROT = os.environ.get("MINIPROT") or shutil.which("miniprot")


@pytest.mark.skipif(
    not MINIPROT,
    reason="miniprot not installed; set MINIPROT to run the offline end-to-end check",
)
def test_end_to_end_on_the_two_validation_slices_with_file_urls(tmp_path):
    import gzip

    rows = []
    for acc, fn in (
        ("T_A15", "validation_slice_zebrafish_chr15_28360000_28420000.fa"),
        ("T_B10", "validation_slice_zebrafish_chr10_24365000_24400000.fa"),
    ):
        gz = tmp_path / (fn + ".gz")
        gz.write_bytes(gzip.compress((V / fn).read_bytes(), mtime=0))
        rows.append(
            {
                "species": acc,
                "accession": acc,
                "url": gz.as_uri(),
                "md5": hashlib.md5(gz.read_bytes()).hexdigest(),
            }
        )
    (tmp_path / "acc.json").write_text(json.dumps({"assemblies": rows}))
    (tmp_path / "pred.json").write_text(
        json.dumps(
            {
                "predictions": [
                    {
                        "accession": r["accession"],
                        "family": "t",
                        "expected_aa_at_326_slc43a2a_type": "F",
                        "kind": "t",
                    }
                    for r in rows
                ]
            }
        )
    )
    out, work = tmp_path / "o", tmp_path / "w"
    JOB.main(
        [
            "run",
            "--accessions",
            str(tmp_path / "acc.json"),
            "--queries",
            str(V / "queries.faa"),
            "--shuffled",
            str(V / "queries_shuffled.faa"),
            "--miniprot",
            MINIPROT,
            "--workdir",
            str(work),
            "--out",
            str(out),
            "--workers",
            "1",
            "--threads",
            "1",
        ]
    )
    assert list(work.iterdir()) == [], "the job removed its own downloads"
    assert (
        J(out / "T_A15.shuffled.json")["n_alignments"] == 0
        and J(out / "T_B10.shuffled.json")["n_alignments"] == 0
    )
    s = JOB.summarize(tmp_path / "acc.json", tmp_path / "pred.json", out)
    r = {x["accession"]: x for x in s["rows"]}
    assert (
        r["T_A15"]["a_326"] == "F"
        and r["T_A15"]["a_codon_326"] == "TTC"
        and r["T_A15"]["as_predicted"] is True
        and r["T_B10"]["b_200_326"] == ["MD"]
        and s["controls"]["shuffled_query_clean"] is True
    )
    first = (out / "progress.jsonl").read_text()
    JOB.main(
        [
            "run",
            "--accessions",
            str(tmp_path / "acc.json"),
            "--queries",
            str(V / "queries.faa"),
            "--miniprot",
            MINIPROT,
            "--workdir",
            str(work),
            "--out",
            str(out),
        ]
    )
    assert (out / "progress.jsonl").read_text() == first, (
        "a second run skips finished species"
    )


def test_packet_pins_tools_inputs_and_the_frozen_bundle():
    pk = J(V / "PACKET.json")
    mp = pk["tools"]["miniprot"]
    assert (
        mp["version"] == "0.18"
        and len(mp["x64_linux_sha256"]) == 64
        and len(mp["source_sha256"]) == 64
    )
    boot = (V / "bootstrap.sh").read_text()
    assert mp["x64_linux_sha256"] in boot and mp["x64_linux_url"] in boot, (
        "the bootstrap carries the same pin, written independently of the packet"
    )
    assert (
        "biopython==1.88" in boot
        and "numpy==2.4.4" in boot
        and pk["python"]["packages"] == {"biopython": "1.88", "numpy": "2.4.4"}
    )
    for name, h in pk["inputs"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == h, name
    fs = pk["frozen_source"]
    b = fs["bundle"]
    assert (
        len(fs["commit"]) == 40
        and b["base64_bytes"] < b["metadata_value_limit_bytes"] == 256 * 1024
        and b["contents"] == pk["inputs"]
    )
    assert (
        hashlib.sha256((V / "bootstrap.sh").read_bytes()).hexdigest()
        == fs["bootstrap"]["sha256"]
    )
    rr = pk["resource_request"]
    assert (
        rr["gpu"] == 0
        and "NO new VM" in rr["vm"]
        and rr["vcpu"] <= 8
        and rr["ram_gb_cap"] <= 32
        and "unmeasured" in rr["estimates_are_unmeasured"]
    )


def test_the_bundle_is_reproducible_from_the_frozen_commit():
    import io
    import subprocess
    import tarfile

    from connectors.genomics import lat4a_survey_freeze as FR

    pk = J(V / "PACKET.json")
    commit = pk["frozen_source"]["commit"]
    if (
        subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", commit], capture_output=True
        ).returncode
        != 0
    ):
        pytest.skip("the frozen commit is not in this checkout's history")
    data, hashes = FR.build_bundle(commit)
    assert (
        hashlib.sha256(data).hexdigest() == pk["frozen_source"]["bundle"]["sha256"]
        and FR.build_bundle(commit)[0] == data
    )
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        names = tar.getnames()
        assert names[0] == "inputs.sha256" and sorted(names[1:]) == sorted(
            FR.BUNDLE_FILES
        )
        listed = dict(
            line.split("  ", 1)[::-1]
            for line in tar.extractfile("inputs.sha256").read().decode().splitlines()
        )
        for n in names[1:]:
            assert (
                hashlib.sha256(tar.extractfile(n).read()).hexdigest()
                == listed[n]
                == hashes[n]
            )
        assert all(m.mtime == 0 and m.uid == 0 for m in tar.getmembers()), (
            "no timestamps or owners leak into the bundle"
        )
