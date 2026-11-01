#!/bin/bash
# Negative controls for the F326L finding, using the paper's own lineage distribution.
# PMID 34534441 reports F326L in flying fishes and in the FLYING halfbeaks Oxyporhamphus and
# Euleptorhamphus. Hemiramphus limbatus is a halfbeak but NOT a flying halfbeak; Cololabis saira
# (saury) and Xenentodon cancila (needlefish) are non-gliding Beloniformes. All three should carry
# F, not L. If they carry L, the finding is an artefact of this pipeline rather than a lineage
# signal.
set -euo pipefail
SP=/tmp/claude-1000/-data-worktrees-delphi-frontier-zf2ff/9bdb799e-5bf7-4391-b088-ba1bc8d93bec/scratchpad
MP=$SP/tools/miniprot-0.18/miniprot
declare -A G=(
  [halfbeak]=$SP/halfbeak/ncbi_dataset/data/GCA_056149455.1/GCA_056149455.1_ASM5614945v1_genomic.fna
  [saury]=$(ls $SP/saury/ncbi_dataset/data/GCA_033807715.1/*_genomic.fna)
  [needlefish]=$(ls $SP/needlefish/ncbi_dataset/data/GCA_014839995.1/*_genomic.fna)
)
for sp in halfbeak saury needlefish; do
  OUT=data/f326l_controls/$sp; mkdir -p $OUT
  sha256sum "${G[$sp]}" | cut -d' ' -f1 > $OUT/genome.sha256
  python3 -I - "${G[$sp]}" "$OUT" <<'PY'
import pathlib,sys
G=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
CH=5
hs=[open(out/f"c{i}.fna","w") for i in range(CH)]; sizes=[0]*CH; total=G.stat().st_size; cur=0
for line in open(G):
    if line.startswith(">"): cur=min(int(sum(sizes)/(total/CH)+1e-9),CH-1)
    hs[cur].write(line); sizes[cur]+=len(line)
for h in hs: h.close()
PY
  : > $OUT/slc43.paf
  for i in 0 1 2 3 4; do
    $MP -t4 -N 5 --outs=0.5 --trans $OUT/c$i.fna data/census_slc43/queries.faa >> $OUT/slc43.paf
    rm -f $OUT/c$i.fna
  done
  echo "$sp hits: $(grep -vc '^##' $OUT/slc43.paf)"
done
