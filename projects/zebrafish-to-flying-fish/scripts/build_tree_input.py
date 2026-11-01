#!/usr/bin/env python3
"""Build the KCNH gene-tree input (analysis G2b) from this project's own artifacts.

The reciprocal best-hit test (RESULTS.md R3) could not decide whether the one kcnh2-like
region in GCA_018398805.1 is kcnh2a-like or kcnh2b-like: alignment score and percent
identity rank the same predicted sequence differently. A gene tree with outgroups is the
test that can separate them, so this assembles exactly that input:

  - the 10 zebrafish KCNH family proteins used in the reciprocal test (UniProt);
  - two human outgroups, KCNH2 and KCNH1, for rooting;
  - the N longest distinct miniprot-predicted proteins from the COLLISION scaffold
    JAGFBZ010001591.1 (the question);
  - the N longest from JAGFBZ010001790.1, which the reciprocal test called kcnh6a-like
    (a POSITIVE CONTROL: a correct tree must place these with kcnh6a, not with kcnh2).

The control is the point. If the tree misplaces the kcnh6a-like sequences, its placement
of the ambiguous ones carries no weight either.

Run: python3 build_tree_input.py RECIPROCAL_JSON OUT_FAA OUT_LEDGER_JSON [N_PER_SCAFFOLD]
"""
import datetime
import hashlib
import json
import pathlib
import sys
import time
import urllib.request

RECIP, OUT_FAA, OUT_LED = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
N = int(sys.argv[4]) if len(sys.argv) > 4 else 4
OUT_FAA.parent.mkdir(parents=True, exist_ok=True)
OUT_LED.parent.mkdir(parents=True, exist_ok=True)

ZF = {"kcnh1a": "Q108P3", "kcnh1b": "K4EHU2", "kcnh2a": "Q108P2", "kcnh2b": "A0AC58ISX0",
      "kcnh3": "A0AC58GGN5", "kcnh4a": "A0A142J9E8", "kcnh5a": "B3DJV7", "kcnh6a": "Q8JH78",
      "kcnh6b": "A0A8M9QEL7", "kcnh7": "A0AB32TVI3"}
OUTGROUPS = {"HUMAN_KCNH2_OUTGROUP": "Q12809", "HUMAN_KCNH1_OUTGROUP": "O95259"}
ROLES = {
    "kcnh": ("HSPEC_ambiguous", "JAGFBZ010001591.1",
             "the collision region: both kcnh2a and kcnh2b queries best-hit it"),
    "kcnh_alt_scaffold": ("HSPEC_control_kcnh6alike", "JAGFBZ010001790.1",
                          "POSITIVE CONTROL: the reciprocal test called this kcnh6a-like, 10/10 predictions"),
}


def fetch(acc):
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    for i in range(4):
        try:
            return url, urllib.request.urlopen(url, timeout=60).read().decode()
        except Exception:
            if i == 3:
                raise
            time.sleep(3)


recip = json.load(open(RECIP))
records, ledger = [], []

for label, acc in list(ZF.items()) + list(OUTGROUPS.items()):
    url, fa = fetch(acc)
    seq = "".join(fa.split("\n")[1:]).replace("*", "")
    name = f"ZF_{label}" if label in ZF else label
    records.append((name, seq))
    ledger.append({"name": name, "kind": "reference_protein", "uniprot": acc, "url": url,
                   "len": len(seq), "sha256": hashlib.sha256(fa.encode()).hexdigest()})

for fam, (prefix, scaffold, why) in ROLES.items():
    blk = recip["families"][fam]
    assert blk["scaffold"] == scaffold, (blk["scaffold"], scaffold)
    preds = sorted(blk["predictions"], key=lambda p: -p["predicted_protein_len"])[:N]
    for i, p in enumerate(preds, 1):
        # the predicted protein itself is not stored in the json; rebuild from the trans file
        pass
    ledger.append({"name": prefix, "kind": "miniprot_prediction_group", "scaffold": scaffold,
                   "why": why, "n_taken": len(preds),
                   "lengths": [p["predicted_protein_len"] for p in preds],
                   "reciprocal_best_each": [p["reciprocal_best"] for p in preds]})

# predicted proteins live in the --trans output files next to the json
trans_dir = pathlib.Path(RECIP).parent
for fam, (prefix, scaffold, why) in ROLES.items():
    txt = (trans_dir / f"{fam}_trans.txt").read_text()
    seen, cur_q = {}, None
    for line in txt.splitlines():
        if line.startswith("##STA"):
            prot = line.split("\t", 1)[1].strip().replace("*", "")
            seen.setdefault(prot, cur_q)
        elif not line.startswith("##"):
            cur_q = line.split("\t")[0]
    ranked = sorted(seen.items(), key=lambda kv: -len(kv[0]))[:N]
    for i, (prot, from_q) in enumerate(ranked, 1):
        name = f"{prefix}_{i}_len{len(prot)}_from_{from_q}"
        records.append((name, prot))
        ledger.append({"name": name, "kind": "miniprot_predicted_protein", "scaffold": scaffold,
                       "predicted_from_query": from_q, "len": len(prot),
                       "sha256": hashlib.sha256(prot.encode()).hexdigest()})

OUT_FAA.write_text("".join(f">{n}\n{s}\n" for n, s in records))
blob = OUT_FAA.read_bytes()
doc = {
    "scope": ("Input assembly for a protein gene tree. Sequences are UniProt reference proteins and "
              "miniprot predictions from an unannotated assembly. A tree over these is a "
              "sequence-similarity phylogeny of predictions, not an orthology proof and not evidence "
              "of expression or function."),
    "built_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "n_sequences": len(records),
    "fasta_bytes": len(blob),
    "fasta_sha256": hashlib.sha256(blob).hexdigest(),
    "question": ("Does the JAGFBZ010001591.1 prediction group fall with zebrafish kcnh2a or kcnh2b?"),
    "positive_control": ("The JAGFBZ010001790.1 group must fall with kcnh6a. If it does not, the tree "
                         "is not trustworthy for the question above."),
    "entries": ledger,
}
OUT_LED.write_text(json.dumps(doc, indent=1) + "\n")
print(f"{len(records)} sequences, {len(blob)} bytes, sha256 {doc['fasta_sha256']}")
for n, s in records:
    print(f"  {n}\t{len(s)}")
