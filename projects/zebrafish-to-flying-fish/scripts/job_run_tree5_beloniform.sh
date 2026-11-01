#!/bin/bash
# claude-zf2ff KCNH gene tree (analysis G2b). Deterministic seed, declared controls.
set -uo pipefail
echo "ZF2FF_JOB=beloniform-tree ZF2FF_START=$(date -u +%FT%TZ)"
IN=/input/beloniform_tree_input.faa
echo "ZF2FF_INPUT_SHA256=$(sha256sum $IN | cut -d' ' -f1)"
echo "ZF2FF_INPUT_SEQS=$(grep -c '^>' $IN)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq mafft iqtree coreutils >/dev/null 2>&1
AP=$?
echo "ZF2FF_APT_RC=$AP"
MAFFT_V=$(mafft --version 2>&1 | head -1)
IQ=$(command -v iqtree2 || command -v iqtree)
IQ_V=$("$IQ" --version 2>&1 | head -1)
echo "ZF2FF_MAFFT_VERSION=$MAFFT_V"
echo "ZF2FF_IQTREE_BIN=$IQ"
echo "ZF2FF_IQTREE_VERSION=$IQ_V"
cd /tmp
mafft --auto --thread 4 "$IN" > aln.faa 2> mafft.log
echo "ZF2FF_MAFFT_RC=$?"
echo "ZF2FF_ALN_SHA256=$(sha256sum aln.faa | cut -d' ' -f1)"
echo "ZF2FF_ALN_COLUMNS=$(python3 - <<'PY'
seqs={}
name=None
for line in open('/tmp/aln.faa'):
    line=line.strip()
    if line.startswith('>'): name=line[1:]; seqs[name]=''
    else: seqs[name]+=line
L={len(v) for v in seqs.values()}
print(sorted(L)[0] if len(L)==1 else 'RAGGED:'+str(L))
PY
)"
# ML tree, LG+G, 1000 ultrafast bootstrap replicates and 1000 SH-aLRT replicates, fixed seed.
"$IQ" -s aln.faa -m LG+G4 -B 1000 --alrt 1000 -T 4 --seed 12345 --prefix zf2ff_beloniform -quiet
echo "ZF2FF_IQTREE_RC=$?"
for f in zf2ff_beloniform.treefile zf2ff_beloniform.contree zf2ff_beloniform.iqtree zf2ff_beloniform.log; do
  [ -f "$f" ] && echo "ZF2FF_OUT_SHA256 $f $(sha256sum $f | cut -d' ' -f1) bytes=$(stat -c%s $f)"
done
echo "ZF2FF_TREEFILE_BEGIN"; cat zf2ff_beloniform.treefile; echo "ZF2FF_TREEFILE_END"
echo "ZF2FF_CONTREE_BEGIN"; cat zf2ff_beloniform.contree; echo "ZF2FF_CONTREE_END"
echo "ZF2FF_MODEL_LINES_BEGIN"; grep -E 'Model of substitution|Log-likelihood of the tree|Number of .* sites|Gamma shape' zf2ff_beloniform.iqtree | head -20; echo "ZF2FF_MODEL_LINES_END"
echo "ZF2FF_DONE=$(date -u +%FT%TZ)"
