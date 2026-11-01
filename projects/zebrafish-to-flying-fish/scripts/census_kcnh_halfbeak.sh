#!/bin/bash
# KCNH census in Hemiramphus limbatus (halfbeak), the SISTER FAMILY to Exocoetidae, on a
# CHROMOSOME-LEVEL assembly. This attacks the one named limitation of the kcnh2a result: that it
# rested on two Beloniformes, one of them a scaffold-level draft.
set -euo pipefail
SP=/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad
G=$SP/halfbeak/ncbi_dataset/data/GCA_056149455.1/GCA_056149455.1_ASM5614945v1_genomic.fna
MP=$SP/tools/miniprot-0.18/miniprot
OUT=data/census_halfbeak; mkdir -p $OUT
sha256sum "$G" | cut -d' ' -f1 > $OUT/genome.sha256
cp data/census/queries.faa $OUT/queries.faa   # the same 10 zebrafish KCNH proteins
python3 -I - <<'PY'
import pathlib
G=pathlib.Path("/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad/halfbeak/ncbi_dataset/data/GCA_056149455.1/GCA_056149455.1_ASM5614945v1_genomic.fna")
CH=5; out=pathlib.Path("data/census_halfbeak")
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
