#!/usr/bin/env python3
"""THE GENETIC CHANGE SET: what you would actually do to a zebrafish, and what is missing.

The project holds six genetic levers in `part` and seven revisions in `part_revision`, each with
a long design note. The goal row counts them -- "6 of 6 levers have a part_revision" -- and that
count is the thing most likely to mislead, because a revision can name a published allele whose
molecular lesion nobody holds. A lever with a revision is not a lever you can order.

SO THIS REPORTS BUILDABILITY, NOT COVERAGE, and it reads the distinction off the data rather
than asserting it. `content_sha256` is non-null only when the project holds an actual sequence
change it could hash. FIVE DIFFERENT THINGS MAKE IT NULL and they are not interchangeable:

    FRAMESHIFT     the lesion is known but its PRODUCT is not derivable from protein-level
                   information: a frameshift runs to the next stop in the shifted frame, which
                   needs the nucleotide sequence (col9a1c@zf3676/zf3677)
    JUNCTION       the breakpoints are known but one side of the junction is absent from the
                   reference assembly, so there is no sequence to synthesise against
                   (kcnh2a@longfin-dt2, from Daane et al.)
    REGULATORY     the change is not in any coding sequence, so there is nothing to hash
                   (kcnh2a@longfin-lof^dt2 is a chromosome-2 inversion between 5' prrx1a and
                   5' kcnh2a that upregulates the gene "without affecting the coding region")
    LESION UNKNOWN a named allele with a measured phenotype whose molecular change is not held
                   (slc12a7a@schleier, col9a1c@knockout-nakagawa2022)
    NOT SEQUENCED  a construct that exists in the literature but whose sequence this project
                   has never obtained (follistatin@mylz2-fst1-li2011)

A reader who sees only "NULL" cannot tell a design decision from a gap, which is why each row
below prints which of the three it is. That classification is DECLARED in NULL_REASON, not
inferred from the text.

WHAT THIS DOES NOT DO: it does not claim the set would work. Several levers are supported at
ABSTRACT read level only, one has no measured effect size at all, and the sixth is contested by
this project's own later claims. Those are printed beside each row rather than summarised away.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))

from dbq import q  # noqa: E402

#: Why each hashless revision has no hash. Declared, so a reader can disagree with a row.
#: Keyed by revision name.
NULL_REASON = {
    "longfin-lof-dt2": ("REGULATORY",
                        "a chromosome-2 inversion that upregulates the gene without touching "
                        "either coding region -- there is no coding change to hash"),
    "schleier-het": ("LESION UNKNOWN",
                     "named allele with a full-text measured phenotype; no source held here "
                     "gives the sequence change"),
    "knockout-nakagawa2022-UNNAMED": ("LESION UNKNOWN",
                                      "a published knockout exists; its allele designation and "
                                      "lesion are not held, so the revision cites the paper and "
                                      "refuses to invent a name"),
    "mylz2-fst1-li2011-UNNAMED": ("NOT SEQUENCED",
                                  "the transgenic line exists in the literature; its designation "
                                  "and effect size do not appear in what was read"),
    "col9a1c-zf3676-zf3677-frameshift-null": ("FRAMESHIFT NULL",
                                              "a FOURTH class, added 2026-11-05: the lesion IS "
                                              "held (del10 at nt 505-514, frameshift at aa 169; "
                                              "ins1 at nt 664, frameshift at aa 222) but a "
                                              "frameshift's product is whatever the shifted "
                                              "reading frame yields until the next stop, which "
                                              "needs the NUCLEOTIDE sequence -- the amino-acid "
                                              "position of the shift is not enough. This null "
                                              "records a limit of the protein-level convention, "
                                              "not a gap in the literature"),
    "longfin-dt2-inversion-chr2-23.174-24.075Mb-Zv11": (
        "JUNCTION NOT IN REFERENCE",
        "a FIFTH class, added 2026-11-05: the breakpoints ARE held (~23.174 Mb and ~24.075 Mb "
        "in Zv11, a ~901 kb inversion), so this is no longer 'coordinates unknown'. But Daane "
        "et al. state they 'did not generate contigs representing the wild-type (Zv11) "
        "chromosome organization at these breakpoints' and that one breakpoint lies 'within a "
        "DNA transposon that is not present between these genes in the zebrafish reference "
        "genome'. One side of the junction is absent from the reference, so the coordinates "
        "locate the inversion without specifying a synthesisable junction"),
    "MYH13-Q9UKX3-motor-domain-only": ("NOT SEQUENCED",
                                       "a reviewed accession and a partial expression precedent, "
                                       "but no construct sequence obtained"),
}

#: Claims that bear on whether a lever is still REQUIRED, as opposed to whether it is buildable.
#: Editorial: these are the claims a reader should see beside the row, not a derivation.
CONTESTED = {
    "superfast-myosin": (
        "1126 (protein) narrowed this lever's necessity to a 9 Hz interval: a NON-superfast "
        "muscle, Hyla chrysoscelis external oblique, delivers 54 W/kg at 44 Hz against the "
        "52 W/kg requirement, while every superfast muscle measured sits at 6-14 W/kg. "
        "1124 then showed the non-superfast alternative is ALSO unspecifiable -- the only "
        "published Hyla myosin sequences are 59-60 aa ROD fragments at MYH7 residues 1752-1810, "
        "carrying no motor domain. So neither myosin can currently be ordered, and it is no "
        "longer clear this lever is needed at all."),
}


def read_level(note: str) -> str:
    """The note's OWN declared read level, with an explicit declaration beating a stray mention.

    The first version of this returned "FULL TEXT" whenever the note contained that phrase, and
    it was wrong on FOUR of seven revisions -- including follistatin, whose note says in capitals
    "READ LEVEL: ABSTRACT ONLY" and also mentions full text while discussing a different source.
    The error was visible in this module's own output, which is the only reason it was caught: a
    row that printed FULL TEXT directly above a note saying ABSTRACT ONLY.

    An explicit "read level: X" or "abstract only" is a declaration about THIS source. A bare
    "full text" is usually a comparison to another one. Declarations win.
    """
    low = (note or "").lower()
    if "abstract only" in low or "achieved -- abstract" in low or "read level `abstract`" in low:
        return "ABSTRACT (declared in the note)"
    if "full text" in low or "full-text" in low:
        return "FULL TEXT"
    if "abstract" in low:
        return "ABSTRACT"
    return "read level not stated in the note"


# Where a predicted structure for a lever's gene lives, if this project holds one.
STRUCTURES = {
    "kcnk5b":   "results/fish-proteins/structures/kcnk5b-homodimer-full/model.cif",
    "lat4a":    "results/fish-proteins/structures/slc43a2a_wt/",
    "slc12a7a": "results/nebius/slc12a7a/WT_ESMFold2.cif",
}


def _plddt_at(path: str, pos: int):
    """pLDDT of the CA at one residue, or None. Takes a file or a directory holding one .cif."""
    import pathlib as _p
    f = _p.Path(path)
    if f.is_dir():
        f = next(iter(f.glob("*.cif")), None)
    if f is None or not f.exists():
        return None
    hdr = []
    for line in open(f):
        if line.startswith("_atom_site."):
            hdr.append(line.strip().split(".")[1])
        elif hdr and line.startswith("ATOM"):
            break
    ix = {n: i for i, n in enumerate(hdr)}
    if "B_iso_or_equiv" not in ix:
        return None
    for line in open(f):
        if not line.startswith("ATOM"):
            continue
        r = line.split()
        if r[ix["label_atom_id"]] != "CA":
            continue
        if int(r[ix["label_seq_id"]]) == pos:
            return float(r[ix["B_iso_or_equiv"]])
    return None


def structural_evaluability(buildable) -> None:
    """Say, per lever, whether a structure can speak to its variant -- GENERATED, not asserted.

    WHY. Measured 2026-11-05: the pLDDT at a variant's own residue decides whether any
    structural or sequence-model result about it means anything. lat4a T200K sits at 97.7, where
    four replicate folds agree to sd 0.116 and the ProteinMPNN rank is identical in all four.
    kcnk5b W169L sits at 42.4 and S345E at 34.0, where two chains of the SAME molecule -- 0.09
    pLDDT apart -- disagree on the mutant's rank. At 345, zero of 71 aligned homologues have a
    residue at all, so the low confidence is an honest report of an unconstrained backbone
    rather than a model failure (claims 1396-1399).

    Without this line a reader of the list below sees six orderable constructs and no indication
    that computational evidence exists for one of them and cannot exist for two.
    """
    import re as _re
    print("  CAN A STRUCTURE SPEAK TO THIS VARIANT?")
    for name, _k, _s, _f, rev, _st, _sha, _n in buildable:
        # A substitution token, NOT a fragment of an accession. The loose form [A-Z]\d+[A-Z]
        # read "Q9Y" out of the UniProt accession Q9YHV4 in `fst1-Q9YHV4-ORF` and reported
        # follistatin as a residue-9 substitution. Both flanks must be amino-acid letters and
        # the token must not continue into more alphanumerics.
        m = _re.search(r"(?<![A-Za-z0-9])[ACDEFGHIKLMNPQRSTVWY](\d+)"
                       r"[ACDEFGHIKLMNPQRSTVWY](?![A-Za-z0-9])", rev)
        if not m:
            print(f"     {name} @ {rev}: no single-residue substitution in the label")
            continue
        pos = int(m.group(1))
        path = STRUCTURES.get(name)
        if path is None:
            print(f"     {name} @ {rev}: residue {pos}, NO STRUCTURE held")
            continue
        v = _plddt_at(path, pos)
        if v is None:
            print(f"     {name} @ {rev}: residue {pos}, structure held but residue not in it")
            continue
        verdict = ("YES -- confident backbone" if v >= 70 else
                   "NO -- backbone not determined at this residue")
        print(f"     {name} @ {rev}: residue {pos} pLDDT {v:.1f}  {verdict}")
    print()


def main() -> int:
    rows = q("""select p.name, coalesce(p.kind,''), coalesce(p.scale_id,''),
             replace(coalesce(p.function,''), chr(10), ' '),
             r.rev, coalesce(r.state,''), coalesce(r.content_sha256,''),
             -- BOTH FIELDS. Reading design_note alone missed the declared read level on two of
             -- seven revisions, because alf-W169L and MYH13 state theirs in change_reason. A
             -- detector pointed at one of two fields that may carry the answer reports the
             -- absence of the field, not the absence of the fact.
             replace(left(coalesce(r.design_note,'') || ' ' ||
                          coalesce(r.change_reason,''), 3000), chr(10), ' ')
             from part p join part_revision r on r.part_id = p.id
             order by (r.content_sha256 is null), p.name, r.rev""")
    if not rows:
        print("  no parts with revisions.")
        return 0

    buildable = [r for r in rows if r[6]]
    print("  THE GENETIC CHANGE SET FOR A FLYING ZEBRAFISH")
    print(f"  {len({r[0] for r in rows})} levers, {len(rows)} specified revisions, "
          f"{len(buildable)} carrying an actual sequence change this project holds.\n")

    for name, kind, scale, func, rev, state, sha, note in rows:
        tag = "BUILDABLE" if sha else NULL_REASON.get(rev, ("UNEXPLAINED NULL", ""))[0]
        print(f"  === {name} @ {rev}   [{kind}, {scale}]   {tag}")
        print(f"      does: {func[:110]}")
        if sha:
            print(f"      sequence change held, sha256 {sha[:16]}")
        else:
            why = NULL_REASON.get(rev, ("", "no reason declared in this module -- a null hash "
                                            "with no explanation is a gap, not a design "
                                            "decision"))[1]
            print(f"      NO SEQUENCE: {why[:150]}")
        lvl = read_level(note)
        print(f"      evidence: {lvl}")
        if name in CONTESTED:
            print(f"      CONTESTED: {CONTESTED[name][:230]}")
        print()

    structural_evaluability(buildable)

    print("  WHAT YOU COULD ORDER TOMORROW")
    for name, _k, _s, _f, rev, _st, sha, _n in buildable:
        print(f"     {name} @ {rev}  (sha256 {sha[:12]})")
    # GENERATE THE SUMMARY, DO NOT HAND-WRITE IT. The previous version of this paragraph read
    # "{len(buildable)} of {len(rows)} revisions carry a sequence change. Both are variants of
    # the SAME gene, kcnk5b -- so the design has ONE orderable locus, not six." The count was
    # interpolated and correct; the sentence around it was written when `buildable` held TWO
    # rows, both kcnk5b. It now holds six across five genes, and the prose still said "Both" and
    # "ONE orderable locus" directly beneath a printed list of six constructs. A generated body
    # is re-derived every run and cannot drift; a hand-written headline is written once against
    # the state of the world at that moment and nothing re-checks it, so that is where all the
    # staleness lands.
    genes = sorted({name for name, _k, _s, _f, _rev, _st, _sha, _n in buildable})
    dup = [g for g in genes if sum(1 for b in buildable if b[0] == g) > 1]
    n_hold = len(rows) - len(buildable)
    gene_phrase = (f"{len(genes)} distinct gene(s)"
                   + (f", with {', '.join(dup)} specified more than once" if dup else ""))
    print(f"""
  AND WHAT THAT MEANS. {len(buildable)} of {len(rows)} revisions carry a sequence change this
  project holds, spanning {gene_phrase}. The other {n_hold} revisions name real published alleles
  and constructs, and a wet lab could obtain several of them by writing to the authors, but this
  project does not hold what it would take to synthesise them.

  THE HONEST SUMMARY OF THE SET. One lever (kcnk5b) is specified twice over, once at abstract
  level (W169L) and once at full text with a measured effect size and a specificity control
  (S345E) -- that second one is the best-evidenced specification in the whole design. Two levers
  name published alleles whose lesions are not held. One names a published knockout with no
  allele designation. One names a transgenic line with no effect size. And the sixth, the
  superfast myosin the flapping route was built around, is contested by this project's own later
  claims on BOTH counts -- it may not be necessary, and neither it nor its non-superfast
  alternative can currently be specified.

  SO: the genetic change set is REAL but THIN. It is {len(buildable)} construct(s) across
  {len(genes)} locus/loci that this project holds a sequence for, and {n_hold} more it would have
  to request or sequence. Whether every one of them BELONGS in the design is a separate question
  and the CONTESTED lines above are where it is argued.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
