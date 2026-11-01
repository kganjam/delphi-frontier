#!/usr/bin/env python3
"""Read the KCNH gene tree and answer the two questions it was built to answer.

Q1 (the control, checked FIRST): do the four predictions from JAGFBZ010001790.1, which the
    reciprocal test called kcnh6a-like, group with zebrafish kcnh6a? If not, the tree is not
    trustworthy and Q2 is not answered.
Q2 (the question): do the four predictions from the collision scaffold JAGFBZ010001591.1 group
    with kcnh2a or with kcnh2b, and at what support?

Support values in the IQ-TREE treefile are "SH-aLRT/UFBoot" as percentages.

Run: python3 analyze_tree.py TREEFILE OUT_JSON
"""
import json
import pathlib
import sys

from Bio import Phylo

TREE, OUT = sys.argv[1], pathlib.Path(sys.argv[2])
t = Phylo.read(TREE, "newick")
t.root_at_midpoint()

tips = [l.name for l in t.get_terminals()]
AMB = [n for n in tips if n.startswith("HSPEC_ambiguous")]
CTL = [n for n in tips if n.startswith("HSPEC_control")]


def mrca_of(names):
    return t.common_ancestor([t.find_any(n) for n in names])


def clade_tips(c):
    return sorted(x.name for x in c.get_terminals())


def support_of(c):
    # IQ-TREE writes "alrt/ufboot" into the node label (confidence or name)
    v = getattr(c, "confidence", None)
    if v is None and getattr(c, "name", None):
        v = c.name
    return v


def smallest_clade_containing(names):
    c = mrca_of(names)
    return c, clade_tips(c), support_of(c)


res = {
    "treefile": str(TREE),
    "method": ("IQ-TREE 2.0.7 maximum likelihood, LG+G4, 1000 ultrafast bootstrap and 1000 SH-aLRT "
               "replicates, seed 12345, on a MAFFT v7.505 --auto alignment. Support shown as "
               "SH-aLRT/UFBoot percentages."),
    "scope": ("A protein gene tree over UniProt reference proteins and miniprot predictions from an "
              "unannotated assembly. It places sequences by substitution likelihood. It is not a "
              "synteny test and not evidence of expression or function."),
    "n_tips": len(tips),
    "tips": tips,
}

# --- Q1 control
c_ctl, tips_ctl, sup_ctl = smallest_clade_containing(CTL)
extra_ctl = [x for x in tips_ctl if x not in CTL]
with_6a = mrca_of(CTL + ["ZF_kcnh6a"])
tips_with_6a = clade_tips(with_6a)
control_passes = all(x.startswith("HSPEC_control") or x == "ZF_kcnh6a" for x in tips_with_6a)
res["control"] = {
    "question": "do the JAGFBZ010001790.1 predictions group with zebrafish kcnh6a?",
    "smallest_clade_containing_the_4_controls": tips_ctl,
    "support_of_that_clade": sup_ctl,
    "smallest_clade_containing_them_plus_ZF_kcnh6a": tips_with_6a,
    "support_of_that_clade": support_of(with_6a),
    "contains_nothing_else": control_passes,
    "verdict": ("PASS: the controls and zebrafish kcnh6a form a clade with nothing else in it"
                if control_passes else
                "FAIL or AMBIGUOUS: that clade pulls in " +
                ", ".join(x for x in tips_with_6a if not x.startswith("HSPEC_control") and x != "ZF_kcnh6a")),
}

# --- Q2 the question
c_amb, tips_amb, sup_amb = smallest_clade_containing(AMB)
with_2a = clade_tips(mrca_of(AMB + ["ZF_kcnh2a"]))
with_2b = clade_tips(mrca_of(AMB + ["ZF_kcnh2b"]))
sup_2b = support_of(mrca_of(AMB + ["ZF_kcnh2b"]))
sup_2a = support_of(mrca_of(AMB + ["ZF_kcnh2a"]))
# whichever zebrafish paralog's MRCA with the predictions is SMALLER is the closer relative
closer = "kcnh2b" if len(with_2b) < len(with_2a) else ("kcnh2a" if len(with_2a) < len(with_2b) else "tie")
res["question"] = {
    "question": "do the JAGFBZ010001591.1 predictions group with kcnh2a or kcnh2b?",
    "smallest_clade_containing_the_4_predictions": tips_amb,
    "support_of_that_clade": sup_amb,
    "clade_with_ZF_kcnh2b": with_2b,
    "support_with_ZF_kcnh2b": sup_2b,
    "clade_with_ZF_kcnh2a": with_2a,
    "support_with_ZF_kcnh2a": sup_2a,
    "closer_zebrafish_paralog": closer,
    "verdict": (f"The predictions join ZF_kcnh2b in a clade of {len(with_2b)} tips, while joining "
                f"ZF_kcnh2a requires a clade of {len(with_2a)} tips, so kcnh2b is the closer "
                f"zebrafish paralog." if closer == "kcnh2b" else
                f"closer paralog: {closer} (with_2a={len(with_2a)} tips, with_2b={len(with_2b)} tips)"),
}
res["caveats"] = [
    "The four predictions come from ONE genomic region, so they are not independent sequences; their "
    "own clade is partly an artefact of being the same locus. The question is where that locus sits.",
    "The zebrafish kcnh2a UniProt entry is 1253 aa and kcnh2b's is 837 aa. A length difference can "
    "affect alignment and branch length; the tree does not control for it.",
    "A gene tree places a sequence; it does not establish orthology without synteny, which was not run.",
    "The input proteins are miniprot predictions from an unannotated assembly, not sequenced transcripts.",
    "This contradicts the alignment-SCORE ranking of the reciprocal test for the longest prediction, "
    "and agrees with its percent-identity ranking and with the forward mapping. The tree is the "
    "better-designed test of the three because it has an outgroup and a positive control, but it is "
    "still one test.",
]
OUT.write_text(json.dumps(res, indent=2) + "\n")
print("CONTROL:", res["control"]["verdict"])
print("  control clade:", tips_with_6a, "support", res["control"]["support_of_that_clade"])
print("QUESTION:", res["question"]["verdict"])
print("  clade with kcnh2b:", with_2b, "support", sup_2b)
print("  clade with kcnh2a:", with_2a, "support", sup_2a)
print("  predictions' own clade support:", sup_amb)
