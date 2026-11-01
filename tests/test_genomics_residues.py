"""Residue reconciliation of the paper's lat4a with Ensembl slc43a2a. Reads only stored files (no network, no PDF); recomputes the claims from the stored FASTA."""

import csv
import datetime
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
D = ROOT / "data" / "genomics"
ART = D / "artifacts"


def J(n):
    return json.loads((D / n).read_text())


A_IDS = ["ENSDARP00000120945", "ENSDARP00000138218"]
B_IDS = [
    "ENSDARP00000156564",
    "ENSDARP00000115460",
    "ENSDARP00000091545",
    "ENSDARP00000144096",
]
# Deliberately typed here, independent of the module: the windows as read from Figures 3C and 2D.
W3C, W3C_NR21, W2D = "YASSAVTFPGIK", "YASSAVKFPGIK", "QSFMRSIFSPIFMLS"


def prot(i):
    return "".join((ART / f"ensembl_protein_{i}.fasta").read_text().split("\n")[1:])


def test_slc43a2a_has_both_windows_at_the_papers_numbering_in_both_isoforms():
    for i in A_IDS:
        s = prot(i)
        assert s.find(W3C) + 1 == 194 and s.count(W3C) == 1, i
        assert s[199] == "T" and s[193:205] == W3C, (
            "T200 is the 7th residue of the window starting at 194"
        )
        assert (
            s.find(W2D) + 1 == 319
            and s.count(W2D) == 1
            and s[318:333] == W2D
            and s[325] == "F"
        ), "F326 is the 8th residue of the window labelled 319-333"
        assert (s[73], s[105]) == ("L", "L"), "L74Rfs6 and L106Rfs39 name leucines"
    assert (len(prot(A_IDS[0])), len(prot(A_IDS[1]))) == (571, 577)


def test_slc43a2b_control_is_distinct_in_all_four_proteins():
    for i in B_IDS:
        s = prot(i)
        assert (
            W3C not in s
            and W2D not in s
            and (s[199], s[325], s[105]) == ("M", "D", "G")
        ), i
        assert 590 <= len(s) <= 600


def test_negative_controls_the_window_search_is_sensitive():
    s = prot(A_IDS[0])
    nr21 = s[:199] + "K" + s[200:]  # the nr21 allele: T200K
    assert W3C not in nr21 and W3C_NR21 in nr21, (
        "the wt window is lost and the nr21 window found after T200K"
    )
    shifted = s[:193] + "C" + s[194:]  # one residue changed inside the window
    assert W3C not in shifted
    assert W2D not in s[:325] + "L" + s[326:], "F326L removes the Figure 2D window"
    assert W3C_NR21 not in s and "PSFMHSVFSPILLLS" not in s, (
        "neither the nr21 row nor the human window is in the zebrafish protein"
    )


def test_refseq_fragment_reconciliation():
    a = prot(A_IDS[0])
    r = "".join((ART / "ncbi_NP_956545.1_slc43a2a.faa").read_text().split("\n")[1:])
    assert len(r) == 153 and a[:139] == r[:139] and a[139] != r[139], (
        "identical to residue 139, then different"
    )
    assert r[105] == "L" and r[73] == "L"
    assert W3C not in r and len(r) < 200, (
        "the fragment ends before residue 200, so it could never show the window"
    )
    rb = "".join((ART / "ncbi_NP_001008585.1_slc43a2b.faa").read_text().split("\n")[1:])
    assert (rb[199], rb[325]) == ("M", "D"), (
        "the older slc43a2b check still agrees with the new proteins"
    )


def test_isoforms_differ_only_by_a_insertion_after_the_positions_used():
    a, b = prot(A_IDS[0]), prot(A_IDS[1])
    assert a[:366] == b[:366] and b[366:372] and len(b) - len(a) == 6, (
        "numbering agrees through 366, so at 74, 106, 200, 326"
    )


def test_hashes_lengths_and_gene_spans_agree_across_sources():
    r = J("lat4a_residues_v1.json")
    for g in r["ensembl"].values():
        for i, p in g["proteins"].items():
            assert (
                hashlib.sha256(
                    (ART / f"ensembl_protein_{i}.fasta").read_bytes()
                ).hexdigest()
                == p["sha256"]
                and len(prot(i)) == p["length"]
            ), i
    z = {x["symbol"]: x for x in csv.DictReader(open(D / "genes.csv"))}
    a = r["ensembl"]["slc43a2a"]
    assert (a["start"], a["end"], str(a["chr"])) == (
        int(z["slc43a2a"]["zfin_gff_start"]),
        int(z["slc43a2a"]["zfin_gff_end"]),
        z["slc43a2a"]["zfin_gff_chr"],
    ), "Ensembl and ZFIN agree on the span"
    assert (
        17_000_000 <= a["start"]
        and a["end"] <= 33_000_000
        and r["findings"]["mapping_interval"]["inside"] is True
    )
    b = r["ensembl"]["slc43a2b"]
    assert str(b["chr"]) == "10" and not (
        17_000_000 <= b["start"] <= 33_000_000 and str(b["chr"]) == "15"
    )


def test_read_level_is_stated_honestly_and_the_text_layer_check_is_recorded():
    r = J("lat4a_residues_v1.json")
    f = r["figure_windows_read_by_eye"]
    assert (
        f["read_level"].startswith("figure image, read by eye")
        and "text layer has none" in f["read_level"]
    )
    assert all(v == [] for v in f["text_layer_hits"].values()) and set(
        f["text_layer_hits"]
    ) == {W3C, W3C_NR21, W2D, "PSFMHSVFSPILLLS"}
    assert (
        f["fig3C"]["wt_window"] == W3C
        and f["fig2D"]["danio_window"] == W2D
        and (f["fig2D"]["label_first"], f["fig2D"]["label_last"]) == (319, 333)
    )
    lq = r["legend_quotes"]
    assert {k: v["pdf_page"] for k, v in lq.items()} == {
        "s2_interval": 5,
        "s2_recomb": 5,
        "s2_ko": 5,
    } and all(len(v["quote"].split()) <= 25 for v in lq.values())
    assert any(
        "not a test" in x or "not by itself a test" in x
        for x in r["still_not_established"]
    ) and any("no organism-engineering result" in x for x in r["still_not_established"])
    assert not any(p.suffix in (".pdf", ".xlsx") for p in D.rglob("*")), (
        "neither PDF is stored"
    )


def test_records_are_valid_pin_exact_target_versions_and_are_not_future_dated():
    models = pytest.importorskip("frontier.models")
    store = pytest.importorskip("frontier.store")
    recs = J("daane2021_residues_records.json")["records"]
    assert (
        [r["kind"] for r in recs].count("Claim") == 2
        and [r["kind"] for r in recs].count("Evidence") == 3
        and len(recs) == 5
    )
    by = {r["id"]: r for r in recs}
    for r in recs:
        draft = {
            k: r[k]
            for k in (
                "namespace",
                "kind",
                "id",
                "issuer",
                "source_uri",
                "visibility",
                "predecessor",
                "payload",
            )
        }
        assert (
            models.make_record(
                models.Draft.model_validate(draft), created_at=r["created_at"]
            )["version"]
            == r["version"]
        ), r["id"]
        if r["kind"] == "Evidence":
            t = r["payload"]["target"]
            assert t["version"] == by[t["id"]]["version"], (
                "evidence pins its exact target version"
            )
    assert not store._unlicensed_available_content(recs)
    now = datetime.datetime.now(datetime.timezone.utc)
    for r in recs:
        assert datetime.datetime.fromisoformat(r["created_at"]) <= now, (
            "a record must not be stamped in the future"
        )
    old = {
        r["id"]
        for f in ("daane2021_records.json", "daane2021_supplement_records.json")
        for r in J(f)["records"]
    }
    assert not (set(by) & old), "append-only: no id reuse"


def test_claims_carry_the_limits_and_do_not_overclaim():
    recs = {r["id"]: r for r in J("daane2021_residues_records.json")["records"]}
    c2 = recs["gx-lat4a-ensembl-slc43a2a-carries-the-papers-residues"]["payload"]
    text = json.dumps(c2).lower()
    assert (
        "does not test anything beyond that" in text
        and "read by eye" in text
        and "nothing here says what t200k or f326l does" in text
    )
    for r in recs.values():
        assert (
            "confirmed by the authors" not in json.dumps(r["payload"]).lower()
            and "engineering" not in r["payload"].get("statement", "").lower()
        )
    ev = recs["gx-ev-ensembl-proteins"]["payload"]
    assert (
        ev["source_dependence"]["independent_of_author"] is True
        and recs["gx-ev-fig3c-2d-windows"]["payload"]["source_dependence"][
            "independent_of_author"
        ]
        is False
    )
    assert (
        recs["gx-daane-fig3c-2d-s2-residue-windows"]["payload"]["origin"]
        == "source_statement"
        and c2["origin"] == "derived"
    )


def test_earlier_status_and_records_are_untouched():
    assert J("lat4a_resolution_v3.json")["status"].startswith("SUPPORTED")
    sup = {r["id"] for r in J("daane2021_supplement_records.json")["records"]}
    assert (
        "gx-problem-lat4a-residues" in sup
        and J("daane2021_residues_records.json")["answers_in_status"]
        == "gx-problem-lat4a-residues"
    )
