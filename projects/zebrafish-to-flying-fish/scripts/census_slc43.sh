#!/bin/bash
# Family census for SLC43 (LAT3/LAT4 family), the second locus the flying-fish phylogenomics names.
# The project's open Problem zf2ff-problem-lat4a-identifier asks which UniProt entry the papers'
# "lat4a" is. This maps the whole zebrafish family onto the assembly so the question becomes
# "which SLC43 loci exist here", which is answerable by sequence.
set -euo pipefail
SP=/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad
G=$SP/genome/ncbi_dataset/data/GCA_018398805.1/GCA_018398805.1_Hirundichthys_speculiger_1.0_genomic.fna
MP=$SP/tools/miniprot-0.18/miniprot
OUT=data/census_slc43; mkdir -p $OUT
python3 -I - <<'PY'
import urllib.request, hashlib, json, pathlib, time
ZF={"ZF_slc43a1a":"F2Z4V7","ZF_slc43a1b":"A2RUY1","ZF_slc43a2a_FRAGMENT":"Q7ZUS0",
    "ZF_slc43a2b_LAT4":"Q5PR35","ZF_slc43a3a":"A0AC58JE51","ZF_slc43a3b":"A0ACD6B6L3"}
OL={"OL_slc43a2b":"H2LJX8","OL_slc43a1a":"A0A3B3HA06"}
def fetch(a):
    for i in range(4):
        try: return urllib.request.urlopen(f"https://rest.uniprot.org/uniprotkb/{a}.fasta",timeout=60).read().decode()
        except Exception:
            if i==3: raise
            time.sleep(3)
recs=[];led=[]
for n,a in {**ZF,**OL}.items():
    fa=fetch(a); s="".join(fa.split("\n")[1:]).replace("*","")
    recs.append((n,s))
    led.append({"name":n,"uniprot":a,"len":len(s),"sha256":hashlib.sha256(fa.encode()).hexdigest(),
                "species":"Danio rerio" if n.startswith("ZF_") else "Oryzias latipes (Beloniformes proxy)"})
o=pathlib.Path("data/census_slc43"); o.mkdir(parents=True,exist_ok=True)
(o/"refs.faa").write_text("".join(f">{n}\n{s}\n" for n,s in recs))
(o/"refs_ledger.json").write_text(json.dumps({"note":"ZF_slc43a2a is a 153 aa UniProt FRAGMENT entry, not a full-length protein; it is carried flagged because the papers' 'lat4a' symbol maps to it.","refs":led},indent=1)+"\n")
# queries for the genome scan: zebrafish only
(o/"queries.faa").write_text("".join(f">{n}\n{s}\n" for n,s in recs if n.startswith("ZF_")))
print("refs",len(recs))
PY
python3 -I - <<'PY'
import pathlib
G=pathlib.Path("/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad/genome/ncbi_dataset/data/GCA_018398805.1/GCA_018398805.1_Hirundichthys_speculiger_1.0_genomic.fna")
CH=5; out=pathlib.Path("data/census_slc43")
hs=[open(out/f"c{i}.fna","w") for i in range(CH)]; sizes=[0]*CH; total=G.stat().st_size; cur=0
for line in open(G):
    if line.startswith(">"): cur=min(int(sum(sizes)/(total/CH)+1e-9),CH-1)
    hs[cur].write(line); sizes[cur]+=len(line)
for h in hs: h.close()
PY
: > $OUT/census.paf
for i in 0 1 2 3 4; do
  $MP -t4 -N 10 --outs=0.5 --trans $OUT/c$i.fna $OUT/queries.faa >> $OUT/census.paf
  rm -f $OUT/c$i.fna
done
grep -vc '^##' $OUT/census.paf
