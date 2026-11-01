set -euo pipefail
SP=/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad
G=$SP/genome/ncbi_dataset/data/GCA_018398805.1/GCA_018398805.1_Hirundichthys_speculiger_1.0_genomic.fna
MP=$SP/tools/miniprot-0.18/miniprot
OUT=data/kcnh2a_hunt
python3 -I - <<'PY'
import urllib.request, hashlib, pathlib, json
accs={"kcnh2a":"Q108P2"}
recs=[];led=[]
for g,a in accs.items():
    fa=urllib.request.urlopen(f"https://rest.uniprot.org/uniprotkb/{a}.fasta",timeout=60).read().decode()
    s="".join(fa.split("\n")[1:])
    recs.append((g,s)); led.append({"gene":g,"uniprot":a,"len":len(s),"sha256":hashlib.sha256(fa.encode()).hexdigest()})
pathlib.Path("data/kcnh2a_hunt/query.faa").write_text("".join(f">{n}\n{s}\n" for n,s in recs))
pathlib.Path("data/kcnh2a_hunt/query_ledger.json").write_text(json.dumps(led,indent=1)+"\n")
print("query bytes", pathlib.Path("data/kcnh2a_hunt/query.faa").stat().st_size)
PY
# low-stringency, 5 whole-scaffold chunks as before
python3 -I - <<'PY'
import pathlib
G=pathlib.Path("/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad/genome/ncbi_dataset/data/GCA_018398805.1/GCA_018398805.1_Hirundichthys_speculiger_1.0_genomic.fna")
CH=5; out=pathlib.Path("data/kcnh2a_hunt")
hs=[open(out/f"c{i}.fna","w") for i in range(CH)]; sizes=[0]*CH; total=G.stat().st_size; cur=0
for line in open(G):
    if line.startswith(">"): cur=min(int(sum(sizes)/(total/CH)+1e-9),CH-1)
    hs[cur].write(line); sizes[cur]+=len(line)
for h in hs: h.close()
PY
: > $OUT/hunt.paf
for i in 0 1 2 3 4; do
  $MP -t4 -N 20 --outs=0.3 --outc=0.05 --trans $OUT/c$i.fna $OUT/query.faa >> $OUT/hunt.paf
  rm -f $OUT/c$i.fna
done
grep -vc '^##' $OUT/hunt.paf || true
# Receipt: run 2026-11-01, exit 0. Low-stringency whole-assembly search with the kcnh2a query
# alone (-N 20 --outs=0.3 --outc=0.05 --trans), asking whether lowering stringency reveals a
# kcnh2a-like region that the default run missed. It did not reveal any NEW region: the same 7
# kcnh2a-aligning regions appear. Two are already assigned by gene tree / reciprocal test
# (JAGFBZ010001591.1 kcnh2b-like, JAGFBZ010001790.1 kcnh6a-like); the other 5 are the input to
# the second tree (data/tree2/). miniprot 0.18-r281, assembly sha256
# 6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052.
