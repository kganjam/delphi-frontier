"""Residue-level reconciliation of the paper's lat4a with Ensembl's full-length slc43a2a, with slc43a2b as the distinct control. New file: daane2021_supplement.py,
the earlier records and lat4a_resolution_v3.json are not edited.

  PYTHONPATH=. python3 -m connectors.genomics.daane2021_residues

Sources: the author-hosted main PDF (Figures 3C and 2D are IMAGES with no text layer; their sequence windows were read by eye from pages rendered at 400 dpi, then compared
to Ensembl) and the publisher's supplement PDF mmc1 (Figure S2 legend, verbatim text). Neither PDF is stored. The Ensembl responses in data/genomics/artifacts were fetched with
  https://rest.ensembl.org/lookup/id/<ENSDARG>?content-type=application/json;expand=1
  https://rest.ensembl.org/sequence/id/<ENSDARP>?content-type=text/x-fasta;type=protein
and are read back here by hash.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "genomics"
ART = OUT / "artifacts"
MAIN_URL = "https://www.daanelab.org/pdfs/papers/Daane-CurrBio-2021.pdf"
SUPP_URL = "https://ars.els-cdn.com/content/image/1-s2.0-S0960982221011908-mmc1.pdf"
SUPP_SHA = "b83f903946f30865957a50b72763a82b8562a04f61c09c69465921cda28b306b"
NS, ISSUER = "node-a", "genomics-worker"      # created_at is the latest real observation time (PDF retrievals, Ensembl files), never a typed constant
GENES = {"slc43a2a": ("ENSDARG00000036848", ["ENSDARP00000120945", "ENSDARP00000138218"]),
         "slc43a2b": ("ENSDARG00000061120", ["ENSDARP00000156564", "ENSDARP00000115460", "ENSDARP00000091545", "ENSDARP00000144096"])}
# Read by eye from the rendered figure images (no text layer; see the negative control below). The positions are the paper's own column labels.
FIG3C = {"page": 6, "panel": "3C", "wt_window": "YASSAVTFPGIK", "nr21_window": "YASSAVKFPGIK", "substitution": "T200K", "residue": 200, "index_in_window": 7,
         "rows_wt_identical": ["D. rerio (wt)", "O. latipes", "G. gallus", "H. sapiens"]}
FIG2D = {"page": 5, "panel": "2D", "label_first": 319, "label_last": 333, "danio_window": "QSFMRSIFSPIFMLS", "substituted_index_in_window": 8, "substitution": "F326L (flying fishes)", "human_window": "PSFMHSVFSPILLLS"}
LEGEND_QUOTES = {"s2_interval": "chromosome 15 between 17-33Mb", "s2_recomb": "There were 0 recombinants among 145 chromosomes for the lat4a T200K SNP.", "s2_ko": "Truncating frameshift allele (L74Rfs6) in lat4a generated through CRISPR/Cas9."}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"-\n", "", s)).strip()


def pages(pdf: Path, n: int) -> list[str]:
    return [norm(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True, check=True).stdout) for i in range(1, n + 1)]


def fasta(path: Path) -> str:
    return "".join(path.read_text().split("\n")[1:])


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from connectors.genomics import sources as S
    from frontier import models, store
    S.ALLOWED_HOSTS = S.ALLOWED_HOSTS | {"ars.els-cdn.com"}
    pins = json.loads((OUT / "daane2021_pins.json").read_text())
    prev = OUT / "lat4a_residues_v1.json"
    first = json.loads(prev.read_text())["retrieved_at"] if prev.exists() else {}
    got = {}
    with tempfile.TemporaryDirectory() as td:
        for k, url in (("main", MAIN_URL), ("supp", SUPP_URL)):
            raw, rc = S.fetch(url, 25_000_000)
            p = Path(td) / f"{k}.pdf"; p.write_bytes(raw); got[k] = (p, rc)
        if got["main"][1].sha256 != pins["pdf"]["sha256"] or got["supp"][1].sha256 != SUPP_SHA:
            raise SystemExit("a PDF's bytes changed: " + got["main"][1].sha256 + " " + got["supp"][1].sha256)
        mp, sp = pages(got["main"][0], 19), pages(got["supp"][0], 12)
        quote_pages = {}
        for qid, q in LEGEND_QUOTES.items():
            hits = [i + 1 for i, t in enumerate(sp) if q in t]
            if len(hits) != 1:
                raise SystemExit(f"legend quote {qid} found on pages {hits}")
            assert len(q.split()) <= 25
            quote_pages[qid] = hits[0]
        # the figure windows must NOT be in the text layer: that is what fixes their read level at 'image, read by eye'
        textlayer = {w: [i + 1 for i, t in enumerate(mp + sp) if w in t] for w in (FIG3C["wt_window"], FIG3C["nr21_window"], FIG2D["danio_window"], FIG2D["human_window"])}
        assert not any(textlayer.values()), textlayer
        # positive control for that search: a string that IS in the text layer is found
        assert any("Multiple sequence alignment of Lat4a" in t for t in mp), "the page-text search works"
        fs = {k: (first.get(k) or got[k][1].retrieved_at) for k in got}
        shas = {k: got[k][1].sha256 for k in got}
    prot, genes = {}, {}
    for g, (ens, ids) in GENES.items():
        lk = json.loads((ART / f"ensembl_lookup_expand_{ens}.json").read_text())
        genes[g] = {"ensembl_gene": ens, "chr": lk["seq_region_name"], "start": lk["start"], "end": lk["end"], "strand": lk["strand"], "assembly": lk["assembly_name"], "proteins": {}}
        for i in ids:
            f = ART / f"ensembl_protein_{i}.fasta"; s = fasta(f)
            tr = next(t["Translation"]["length"] for t in lk["Transcript"] if (t.get("Translation") or {}).get("id") == i)
            assert tr == len(s), (i, tr, len(s))
            w1, w2 = FIG3C["wt_window"], FIG2D["danio_window"]
            genes[g]["proteins"][i] = {"length": len(s), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "fig3C_window_at": (s.find(w1) + 1) or None, "fig2D_window_at": (s.find(w2) + 1) or None,
                                       "res74": s[73], "res106": s[105], "res200": s[199], "res326": s[325], "res319_333": s[318:333]}
            prot[i] = s
    a_ids, b_ids = GENES["slc43a2a"][1], GENES["slc43a2b"][1]
    for i in a_ids:
        p = genes["slc43a2a"]["proteins"][i]
        assert p["fig3C_window_at"] == 194 and p["fig2D_window_at"] == 319 and p["res200"] == "T" and p["res326"] == "F" and p["res74"] == "L" and p["res106"] == "L" and p["res319_333"] == FIG2D["danio_window"]
        assert prot[i][193 + FIG3C["index_in_window"] - 1] == "T"
    for i in b_ids:
        p = genes["slc43a2b"]["proteins"][i]
        assert p["fig3C_window_at"] is None and p["fig2D_window_at"] is None and (p["res200"], p["res326"]) == ("M", "D"), i
    a0 = prot[a_ids[0]]; rs = fasta(ART / "ncbi_NP_956545.1_slc43a2a.faa")
    k = next(i for i in range(len(rs)) if a0[i] != rs[i])
    a_span = (genes["slc43a2a"]["start"], genes["slc43a2a"]["end"])
    res = {"schema": "lat4a-residues-0.1 (connector-local)", "supersedes_for_the_residue_question": "lat4a_resolution_v2.json residue_check and the problem gx-problem-lat4a-residues, which are kept unchanged",
           "question": "Does a full-length zebrafish slc43a2a carry the paper's residues at the paper's positions, and does slc43a2b not?",
           "retrieved_at": fs, "pdf_sha256": shas,
           "figure_windows_read_by_eye": {"read_level": "figure image, read by eye from pages rendered at 400 dpi; the PDF text layer has none of these strings (checked on all pages of both PDFs, with a positive control)", "fig3C": FIG3C, "fig2D": FIG2D, "text_layer_hits": textlayer},
           "legend_quotes": {k: {"quote": q, "pdf": "mmc1 (publisher supplement)", "pdf_page": quote_pages[k]} for k, q in LEGEND_QUOTES.items()},
           "ensembl": genes,
           "findings": {"slc43a2a_both_isoforms": "contain both paper windows exactly: Figure 3C window at residues 194-205 (T200) and Figure 2D window at 319-333 (F326), the paper's own column labels; residue 74 and residue 106 are L, the residues named by the L74Rfs6 and L106Rfs39 alleles",
                        "slc43a2b_all_four_proteins": "contain neither window (M200, D326, residue 106 G): the control is distinct",
                        "refseq_fragment": {"protein": "NP_956545.1", "length": len(rs), "identical_to_ensembl_1_to_": k, "then": "diverges into a different 14-residue C-terminus: a short isoform, so it ends before residue 200 without any numbering conflict"},
                        "mapping_interval": {"paper_s2": "chromosome 15 between 17-33Mb", "slc43a2a_ensembl_GRCz11": list(a_span), "inside": 17_000_000 <= a_span[0] and a_span[1] <= 33_000_000},
                        "isoforms": "the two Ensembl slc43a2a proteins (571 and 577 aa) differ only by a 6-residue insertion at 367, so their numbering agrees at 74, 106, 200 and 326"},
           "still_not_established": ["which transcript the authors numbered is not stated; the two Ensembl isoforms agree at every position used, so this does not change the result here",
                                     "the windows are 12 and 15 residues of a highly conserved region (the paper's own medaka, chicken and human rows share the 12-mer), so the match supports the paper's protein being slc43a2a and not slc43a2b; it is not by itself a test of orthology to other genes",
                                     "Figure S2 is read at legend level only: the 17-33 Mb interval has no finer coordinates here, and the three SNP genes are named by the authors' labels (med13b, lat4a, si:dkey-285b23.3)",
                                     "this is source alignment and identifier reconciliation: it says nothing about what T200K or F326L does, and no organism-engineering result is claimed"],
           "reading": "lat4a_resolution_v3.json's 'supported' stands and its residue gap is closed at the level above; the status wording is unchanged, the evidence is added."}
    (OUT / "lat4a_residues_v1.json").write_text(json.dumps(res, indent=1, sort_keys=True))
    # ---- append-only records ----
    card = json.loads((OUT / "daane2021_source.json").read_text())
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    def src_main(loc):
        return {"uri": MAIN_URL, "locator": loc, "source_version": card["version"], "content_sha256": shas["main"], "content_available": False,
                "access": "author-hosted PDF, no login; read level: figure image read by eye for these windows, full text elsewhere; licence: none stated in the bytes read; PDF not stored", "license": None}
    def src_supp(loc):
        return {"uri": SUPP_URL, "locator": loc, "source_version": "Current Biology 2021 supplement mmc1.pdf (12 pages), sha256 pinned", "content_sha256": shas["supp"], "content_available": False,
                "access": "publisher CDN download, no login; read level: full-text for the Figure S2 legend; PDF not stored; licence not read", "license": None}
    def src_ens(loc, art):
        return {"uri": "https://rest.ensembl.org/", "locator": loc, "source_version": "Ensembl REST (release not stated in the response)", "content_sha256": sha(ART / art), "content_available": False,
                "access": "public REST GET, no key; responses stored by hash; Ensembl terms not read", "license": None}
    tag = lambda cls, sp: f"[species: {sp}; evidence_class: {cls}; source: Daane 2021 figures + supplement + Ensembl REST] "
    def claim(id_, title, st, ctx, lim, source, origin, assumptions=None):
        return {"namespace": NS, "kind": "Claim", "id": id_, "issuer": ISSUER, "source_uri": "urn:frontier:connector:genomics", "visibility": "public", "predecessor": None,
                "payload": {"title": title, "statement": st, "context": ctx, "assumptions": assumptions or [], "limitations": lim, "source": source, "origin": origin}}
    def aref(path, title, role, media="application/json"):
        b = (ROOT / path).read_bytes(); h = hashlib.sha256(b).hexdigest()
        return {"title": f"{role}: {path} - {title}"[:3000], "uri": "urn:sha256:" + h, "sha256": h, "byte_size": len(b), "media_type": media, "role": role, "availability": "referenced", "license": None}
    def evid(id_, target, rel, source, method, context, arts, lim, indep, when):
        return {"namespace": NS, "kind": "Evidence", "id": id_, "issuer": ISSUER, "source_uri": "urn:frontier:connector:genomics", "visibility": "public", "predecessor": None,
                "payload": {"target": target, "evidence_kind": "source_assessment", "relation": rel, "source": source, "created_time": {"value": when, "basis": "witnessed"}, "retrieved_time": {"value": when, "basis": "witnessed"},
                            "method": method, "context": context, "assumptions": [], "provenance": {"main_pdf_sha256": shas["main"], "supplement_mmc1_sha256": shas["supp"]},
                            "source_dependence": {"declared": True, "independent_of_author": indep, "note": "one operator read the figures and wrote the records; no independent review"},
                            "uncertainty": "Not quantified.", "limitations": lim, "artifacts": [aref(p, t, r, m) if m else aref(p, t, r) for p, t, r, m in arts]}}
    ens_when = __import__("datetime").datetime.fromtimestamp(max((ART / f"ensembl_protein_{i}.fasta").stat().st_mtime for ids in (a_ids, b_ids) for i in ids), __import__("datetime").timezone.utc).isoformat()
    ra = ("data/genomics/lat4a_residues_v1.json", "figure windows, legend quotes with pages, the Ensembl comparison, the slc43a2b control and what is still not established", "output", "application/json")
    C1 = claim("gx-daane-fig3c-2d-s2-residue-windows", "Source statement (Figures 3C and 2D, Figure S2 legend): the paper's Lat4a sequence windows around T200 and F326, and the nr21 mapping interval",
               "Figure 3C aligns YASSAVTFPGIK for zebrafish (wt), medaka, chicken and human and YASSAVKFPGIK for nr21 (T200K); Figure 2D labels residues 319 to 333 and aligns QSFMRSIFSPIFMLS for zebrafish, with F326 replaced by L in flying fishes. "
               "The supplement's Figure S2 legend places the nr21 mapping on chromosome 15 between 17 and 33 Mb, reports 0 recombinants among 145 chromosomes for the lat4a T200K SNP, and names a CRISPR frameshift allele L74Rfs6.",
               tag("source_assessment", "Danio rerio, Beloniformes") + "Windows read by eye from rendered figure images (400 dpi); legend sentences quoted verbatim: [s2_interval] mmc1 p.%d: \"%s\"; [s2_recomb] p.%d: \"%s\"; [s2_ko] p.%d: \"%s\"" % (quote_pages["s2_interval"], LEGEND_QUOTES["s2_interval"], quote_pages["s2_recomb"], LEGEND_QUOTES["s2_recomb"], quote_pages["s2_ko"], LEGEND_QUOTES["s2_ko"]),
               ["The figure windows have no text layer: they were read by eye and could contain a transcription error; they are checked here only by matching a real protein exactly.", "The authors' alignment rows are as drawn; the protein/transcript they numbered is not stated.", "Figure S2 was read at legend level only."],
               src_main("Figure 3C (pdf p.6); Figure 2D (pdf p.5)"), "source_statement")
    C2 = claim("gx-lat4a-ensembl-slc43a2a-carries-the-papers-residues", "Derived: Ensembl's full-length zebrafish slc43a2a carries the paper's windows at the paper's numbering, and slc43a2b does not",
               "Both Ensembl slc43a2a proteins (ENSDARP00000120945, 571 aa; ENSDARP00000138218, 577 aa) contain the Figure 3C window at residues 194-205, so T is residue 200, and the Figure 2D window at 319-333, so F is residue 326; residues 74 and 106 are L, as the L74Rfs6 and L106Rfs39 alleles name. "
               "None of the four slc43a2b proteins (592-598 aa) contains either window (M200, D326, G106). The slc43a2a gene lies at 28.37-28.41 Mb on chromosome 15, inside the Figure S2 interval. The 153-aa RefSeq NP_956545.1 is identical to Ensembl 1-139 and then diverges: a short isoform, not a numbering conflict.",
               tag("source_assessment", "Danio rerio") + "Comparison and control in lat4a_residues_v1.json.",
               ["The windows are 12 and 15 residues of a highly conserved region, so this supports the paper's protein being slc43a2a and not slc43a2b; it does not test anything beyond that.", "The figure windows were read by eye.", "The transcript the authors numbered is not stated; the two isoforms agree at every position used.", "Nothing here says what T200K or F326L does."],
               src_ens("sequence/id/ENSDARP00000120945 (protein)", "ensembl_protein_ENSDARP00000120945.fasta"), "derived", ["The Ensembl sequences are the sequences of the genes named."])
    CREATED_AT = max(list(fs.values()) + [ens_when])    # same-day UTC isoformat strings sort in time order
    made = {d["id"]: models.make_record(models.Draft.model_validate(d), created_at=CREATED_AT) for d in (C1, C2)}
    E = [evid("gx-ev-fig3c-2d-windows", "gx-daane-fig3c-2d-s2-residue-windows", "supports", src_main("Figure 3C (pdf p.6); Figure 2D (pdf p.5)"), "Rendered the two figure pages at 400 dpi, read the alignment windows and the 319/333 column labels by eye, and checked that the PDF text layer has none of them (with a positive control).",
              "The authors' own figures; transcription is mine.", [ra], ["Read by eye from images; no text layer.", "Windows only, not whole proteins."], False, fs["main"]),
         evid("gx-ev-s2-legend", "gx-daane-fig3c-2d-s2-residue-windows", "supports", src_supp("Figure S2 legend (mmc1 pdf p.%d)" % quote_pages["s2_interval"]), "Fetched mmc1.pdf, checked its sha256, extracted the page text and verified the three legend sentences verbatim with their page.",
              "The authors' own legend.", [ra], ["Legend text only; no finer mapping coordinates."], False, fs["supp"]),
         evid("gx-ev-ensembl-proteins", "gx-lat4a-ensembl-slc43a2a-carries-the-papers-residues", "supports", src_ens("sequence/id/ENSDARP00000120945 and the other five proteins (lookup expand=1 for the gene spans)", "ensembl_protein_ENSDARP00000120945.fasta"),
              "Fetched all protein sequences for both genes, stored them by hash, searched for the two windows and read residues 74, 106, 200 and 326; slc43a2b is the distinct control; compared the RefSeq fragment with the Ensembl protein.",
              "An independent database compared with the authors' figures; the match is exact.", [ra] + [(f"data/genomics/artifacts/ensembl_protein_{i}.fasta", f"Ensembl protein {i}", "input", "text/plain") for i in a_ids + b_ids],
              ["Windows are short and conserved.", "The transcript the authors numbered is not stated.", "Ensembl release not stated in the response."], True, ens_when)]
    for e in E:
        e["payload"]["target"] = models.ref(made[e["payload"]["target"]]); made[e["id"]] = models.make_record(models.Draft.model_validate(e), created_at=CREATED_AT)
    recs = list(made.values())
    bad = store._unlicensed_available_content(recs)
    if bad:
        raise SystemExit(f"licence gate: {bad}")
    (OUT / "daane2021_residues_records.json").write_text(json.dumps({"records_schema": "genomics-records-0.1 (connector-local; frontier.models records)", "status": "proposed drafts; nothing submitted, reviewed or accepted", "namespace": NS, "issuer": ISSUER,
        "append_only_note": "adds 5 records. gx-problem-lat4a-residues (daane2021_supplement_records.json) is answered at the level stated here, in status only; it, gx-lat4a-is-slc43a2a-supported and every earlier record keep their versions.",
        "answers_in_status": "gx-problem-lat4a-residues", "records": recs}, indent=1, sort_keys=True))
    print({k: sum(1 for r in recs if r["kind"] == k) for k in ("Claim", "Evidence", "Problem")}, "licence offenders:", len(bad), "| a windows at", [genes["slc43a2a"]["proteins"][i]["fig3C_window_at"] for i in a_ids])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
