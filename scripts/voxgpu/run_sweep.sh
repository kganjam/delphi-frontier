#!/bin/bash
# Runs inside the arm-B job after a PASS build. $1 = build dir holding voxcraft-sim + vx3_node_worker.
# Generates the seeded sweep with /job/gen_sweep.py and runs each batch dir as ONE voxcraft-sim invocation.
set -u
B=$1; O=/out/sweep; mkdir -p $O; cd $B
python3 /job/gen_sweep.py --out $B/sweep_in ${GEN_ARGS:-} > $O/gen.txt 2>&1; echo "gen rc=$?" >> $O/gen.txt
cp $B/sweep_in/manifest.json $O/
echo "VOXGPU_GEN $(cat $O/gen.txt | tr '\n' ' ')" >&3
(cd $B/sweep_in && find . -type f | sort | xargs sha256sum) > $O/inputs.sha256
nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,power.draw --format=csv -l 5 > $O/gpu_telemetry.csv 2>&1 &
TP=$!
for d in $(ls -d $B/sweep_in/*/ | sort); do
  n=$(basename $d)
  t0=$(date +%s.%N)
  timeout ${BATCH_TIMEOUT:-2400} ./voxcraft-sim -i $d -o $O/$n.xml -f > $B/$n.history 2> $O/$n.stderr; rc=$?
  t1=$(date +%s.%N)
  nv=$(ls $d/*.vxd | wc -l)
  echo "BATCH $n n_vxd=$nv rc=$rc wall_s=$(python3 -c "print(round($t1-$t0,2))") report_bytes=$(stat -c %s $O/$n.xml 2>/dev/null || echo 0) diverged=$(grep -c -i diverged $B/$n.history)" | tee -a $O/batches.txt
  grep -i -E "diverged|error" $B/$n.history | head -50 > $O/$n.diverged.txt
  head -c 20000 $B/$n.history > $O/$n.history.head
  # stream this batch's report to the job log now, so a later timeout cannot lose it
  tar czf /tmp/part_$n.tgz -C $O $n.xml $n.stderr $n.diverged.txt batches.txt 2>/dev/null
  echo "VOXGPU_PART_BEGIN $n sha256=$(sha256sum /tmp/part_$n.tgz | cut -d' ' -f1)" >&3
  base64 -w 4000 /tmp/part_$n.tgz >&3; echo "VOXGPU_PART_END $n" >&3
done
kill $TP
