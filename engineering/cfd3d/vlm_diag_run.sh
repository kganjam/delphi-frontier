#!/bin/sh
# Extended VLM diagnostic packet (vlmdiag_packet.json): 4 single-thread processes, then a merge.
#   sh engineering/cfd3d/vlm_diag_run.sh OUTDIR      (from the packet root; PYTHON overrides the interpreter)
# Every process rewrites its results.json atomically after each solve and starts no solve after the deadline,
# so a kill keeps the last complete solve; exit codes and logs are kept beside the results.
set -u
OUT=${1:-output}
PY=${PYTHON:-python3}
DL=${VLM_DIAG_DEADLINE:-700}
D=engineering/cfd3d/vlm_diag.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$OUT"
REST="A1_elliptic_AR6_dense,A2_elliptic_AR4_dense,A3_rectangle_AR4,A4_elliptic_AR4_coarse7,A4_elliptic_AR4_coarse16,N2_notched_rectangle,F1_pectoral_L_isolated,F2_pelvic_L_isolated"
"$PY" -I "$D" "$OUT/core-f3" --extended --deadline "$DL" --arms F3_four_fins_combined > "$OUT/core-f3.log" 2>&1 & p1=$!
"$PY" -I "$D" "$OUT/repair-f3" --extended --repair --deadline "$DL" --arms F3_four_fins_combined > "$OUT/repair-f3.log" 2>&1 & p2=$!
"$PY" -I "$D" "$OUT/core-rest" --extended --deadline "$DL" --arms "R0_reproduce_owner07,N1_mutant_collocation_quarter_chord,$REST" > "$OUT/core-rest.log" 2>&1 & p3=$!
"$PY" -I "$D" "$OUT/repair-rest" --extended --repair --deadline "$DL" --arms "$REST" > "$OUT/repair-rest.log" 2>&1 & p4=$!
wait $p1; r1=$?; wait $p2; r2=$?; wait $p3; r3=$?; wait $p4; r4=$?
"$PY" -I "$D" merge "$OUT/merged.json" "$OUT/core-f3" "$OUT/repair-f3" "$OUT/core-rest" "$OUT/repair-rest" > "$OUT/merge.log" 2>&1; rm=$?
printf '{"core_f3": %s, "repair_f3": %s, "core_rest": %s, "repair_rest": %s, "merge": %s}\n' "$r1" "$r2" "$r3" "$r4" "$rm" > "$OUT/exit-codes.json"
for r in $r1 $r2 $r3 $r4 $rm; do [ "$r" -eq 0 ] || exit "$r"; done
exit 0
