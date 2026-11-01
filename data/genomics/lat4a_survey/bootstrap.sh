#!/usr/bin/env bash
# lat4a survey: portable bootstrap for a Debian 12 / Ubuntu 22.04+ x86_64 VM (root, e.g. a GCE startup script). Idempotent: finished species are skipped on rerun.
#
# Required environment:
#   BUNDLE_SHA256   sha256 of lat4a-survey-bundle.tar.gz, from PACKET.json / the handoff file (the anchor of everything below)
# One of:
#   BUNDLE          path to the bundle on disk
#   (or the instance metadata attribute lat4a-bundle-b64, read from the GCE metadata server)
# Optional: SELFCHECK_ONLY=1 (verify environment and stop before any genome download)  ROOTDIR (default /var/tmp/lat4a)  OUT (default $ROOTDIR/out)  WORKERS (3)  THREADS (2)  MEM_MAX (24G)  PROBE_MAX_SECONDS (900)  PROBE_MAX_RSS_MB (8000)
#
# Outbound HTTPS needed: pypi.org, files.pythonhosted.org, github.com (release asset), ftp.ncbi.nlm.nih.gov. Public data only; no credentials are read or written.
# The only files deleted are the genome downloads the job itself made inside $ROOTDIR/work.
set -euo pipefail

: "${BUNDLE_SHA256:?set BUNDLE_SHA256}"
ROOTDIR="${ROOTDIR:-/var/tmp/lat4a}"; OUT="${OUT:-$ROOTDIR/out}"; WORK="$ROOTDIR/work"; SRC="$ROOTDIR/src"; VENV="$ROOTDIR/venv"; TOOLS="$ROOTDIR/tools"
WORKERS="${WORKERS:-3}"; THREADS="${THREADS:-2}"; MEM_MAX="${MEM_MAX:-24G}"; PROBE_MAX_SECONDS="${PROBE_MAX_SECONDS:-900}"; PROBE_MAX_RSS_MB="${PROBE_MAX_RSS_MB:-8000}"
MINIPROT_URL="https://github.com/lh3/miniprot/releases/download/v0.18/miniprot-0.18_x64-linux.tar.bz2"
MINIPROT_SHA256="794397d918c85cd55f42cd905350abe0528ceb09f6a1430c3a3d6650309ac28e"
mkdir -p "$ROOTDIR" "$OUT" "$WORK" "$TOOLS"
log() { echo "[lat4a] $*" | tee -a "$OUT/bootstrap.log"; }
stop() { log "STOP: $*"; echo "$*" > "$OUT/STOPPED.txt"; exit 3; }

# 1. OS packages, only if missing
need=""; for c in python3 curl bzip2 tar sha256sum; do command -v "$c" >/dev/null || need="$need $c"; done
python3 -c 'import venv, sys; assert sys.version_info >= (3, 11)' 2>/dev/null || need="$need python3 python3-venv"
if [ -n "$need" ]; then log "installing:$need"; apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 python3-venv curl bzip2 tar ca-certificates coreutils; fi
python3 -c 'import venv, sys; assert sys.version_info >= (3, 11)' || stop "python >= 3.11 with venv is required"

# 2. the source bundle, verified before anything is extracted
B="$ROOTDIR/bundle.tar.gz"
if [ -n "${BUNDLE:-}" ]; then cp "$BUNDLE" "$B"
elif [ ! -s "$B" ]; then
  curl -fsS -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/attributes/lat4a-bundle-b64" | base64 -d > "$B" || stop "no BUNDLE and no lat4a-bundle-b64 metadata attribute"
fi
got="$(sha256sum "$B" | cut -d' ' -f1)"; [ "$got" = "$BUNDLE_SHA256" ] || stop "bundle sha256 $got != expected $BUNDLE_SHA256"
rm -rf "$SRC"; mkdir -p "$SRC"; tar -xzf "$B" -C "$SRC"; (cd "$SRC" && sha256sum -c inputs.sha256 --quiet) || stop "an extracted input does not match inputs.sha256"
log "bundle verified: $got"

# 3. Python environment (the only third-party dependencies)
if [ ! -x "$VENV/bin/python" ]; then python3 -m venv "$VENV"; fi
"$VENV/bin/python" -m pip install -q --disable-pip-version-check biopython==1.88 numpy==2.4.4
"$VENV/bin/python" -c 'import Bio, numpy; assert Bio.__version__ == "1.88" and numpy.__version__ == "2.4.4"' || stop "dependency versions differ from the pins"

# 4. miniprot, verified before it is run
MP="$TOOLS/miniprot-0.18_x64-linux/miniprot"
if [ ! -x "$MP" ]; then
  curl -fsSL -o "$TOOLS/miniprot.tar.bz2" "$MINIPROT_URL"
  [ "$(sha256sum "$TOOLS/miniprot.tar.bz2" | cut -d' ' -f1)" = "$MINIPROT_SHA256" ] || stop "miniprot download does not match its pinned sha256"
  tar -xjf "$TOOLS/miniprot.tar.bz2" -C "$TOOLS"
fi
[ "$("$MP" --version)" = "0.18-r281" ] || stop "miniprot version is not 0.18-r281"

# 5. confine the work: one scope for memory, tasks and wall time. Without systemd-run only wall time is bounded, and that is logged.
scope() { local secs="$1"; shift; if command -v systemd-run >/dev/null 2>&1 && [ "$(id -u)" = 0 ]; then systemd-run --scope -q -p MemoryMax="$MEM_MAX" -p MemorySwapMax=0 -p TasksMax=256 -p RuntimeMaxSec="$secs" "$@"; else log "WARNING: no systemd-run scope; only a timeout bounds this step"; timeout "$secs" "$@"; fi; }
cd "$SRC"; export PYTHONPATH="$SRC"; PY="$VENV/bin/python"; V=data/genomics/lat4a_survey

# 6. self-check: the VM must reproduce the host's validation results byte for byte before any genome is downloaded
for pair in "chr15_28360000_28420000 validation_slice_result" "chr10_24365000_24400000 validation_slice_chr10_result"; do
  set -- $pair
  scope 300 "$PY" -m connectors.genomics.lat4a_survey run "$V/validation_slice_zebrafish_$1.fa" "$V/queries.faa" "$WORK/selfcheck_$2.json" --miniprot "$MP" --threads 2 >/dev/null
  cmp -s "$WORK/selfcheck_$2.json" "$V/$2.json" || stop "self-check $2 differs from the host result: the VM's miniprot/Biopython/Python do not reproduce it"
done
log "self-check passed: both validation slices reproduce byte for byte"
[ "${SELFCHECK_ONLY:-}" = 1 ] && { log "SELFCHECK_ONLY=1: stopping before any genome download"; touch "$OUT/SELFCHECK_OK"; exit 0; }

# 7. timing probe on the one assembly that matters most (the flying fish), then a gate
JOB=(-m connectors.genomics.lat4a_survey_job run --accessions "$V/accessions.json" --queries "$V/queries.faa" --shuffled "$V/queries_shuffled.faa" --miniprot "$MP" --workdir "$WORK" --out "$OUT")
scope 1800 "$PY" "${JOB[@]}" --workers 1 --threads 4 --only "Hirundichthys speculiger" || log "probe exited non-zero (see failures.log)"
"$PY" - "$OUT" "$PROBE_MAX_SECONDS" "$PROBE_MAX_RSS_MB" <<'PYEOF' || stop "timing probe gate failed (see $OUT/progress.jsonl): nothing further was started"
import json, sys
out, max_s, max_rss = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
rows = [json.loads(l) for l in open(out + "/progress.jsonl")]
r = next(x for x in rows if x.get("species") == "Hirundichthys speculiger" and "align_seconds" in x)
secs = r["download"]["seconds"] + r["align_seconds"]
print("probe: download %.0fs + align %.0fs, peak child RSS %s MB" % (r["download"]["seconds"], r["align_seconds"], r["maxrss_children_mb"]))
sys.exit(0 if secs <= max_s and r["maxrss_children_mb"] <= max_rss else 1)
PYEOF
log "probe passed the gate"

# 8. the rest; checkpoints are the per-species files in $OUT, so a preempted run resumes by rerunning this script
scope 9000 "$PY" "${JOB[@]}" --workers "$WORKERS" --threads "$THREADS" || log "main run exited non-zero (see failures.log)"
"$PY" -m connectors.genomics.lat4a_survey_job summarize --accessions "$V/accessions.json" --predictions "$V/predictions.json" --out "$OUT"

# 9. checksums over the outputs, for the collector to check after upload
(cd "$OUT" && find . -type f ! -name sha256sums.txt ! -name DONE -print0 | sort -z | xargs -0 sha256sum > sha256sums.txt)
touch "$OUT/DONE"; log "done: $(ls "$OUT"/*.json | wc -l) json files in $OUT"
