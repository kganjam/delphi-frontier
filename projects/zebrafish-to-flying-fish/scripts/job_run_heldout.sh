#!/bin/bash
set -uo pipefail
nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo "no-gpu-visible"
echo "ZF2FF_JOB=motif-heldout ZF2FF_START=$(date -u +%FT%TZ)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq python3 python3-numpy curl ca-certificates coreutils >/dev/null 2>&1
echo "ZF2FF_APT_RC=$?"
python3 -c 'import numpy,sys; print("ZF2FF_PY="+sys.version.split()[0]+" ZF2FF_NUMPY="+numpy.__version__)'
cd /tmp
base64 -d /input/windows_all.fa.gz.b64 > w.fa.gz && gunzip -f w.fa.gz
echo "ZF2FF_FASTA_SHA256=$(sha256sum w.fa | cut -d' ' -f1)"
JURL=https://jaspar.elixir.no/download/data/2024/CORE/JASPAR2024_CORE_vertebrates_non-redundant_pfms_jaspar.txt
curl -sSL -o jaspar.txt "$JURL"; echo "ZF2FF_JASPAR_CURL_RC=$?"
echo "ZF2FF_JASPAR_SHA256=$(sha256sum jaspar.txt | cut -d' ' -f1)"
python3 /input/motif_heldout.py w.fa jaspar.txt 20 12345
echo "ZF2FF_SCAN_RC=$?"
echo "ZF2FF_DONE=$(date -u +%FT%TZ)"
