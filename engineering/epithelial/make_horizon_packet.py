"""Build the bounded observation-horizon CPU packet from the frozen protocol.

The only change to any model is the declared observation-horizon factor: StopTime 1000 ->
8000, applied as a named edit that must match exactly once against the EXACT model.xml the
previous run used. Every other parameter is carried over untouched, so the extension is an
extension of the recorded run and not a new configuration.

Reproduction pins are the sha256 of each native logger's t<=1000 prefix, extracted by the same
function the packet's checker uses. The native loggers are not shipped.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent / "packet_files_horizon"))
from check_reproduction import prefix_bytes  # noqa: E402

SCRIPTS = ("run_packet.sh", "verify_packet.py", "audit_completeness.py",
           "check_reproduction.py", "analyze_horizon.py")
EDIT = ('<StopTime value="1000"/>', '<StopTime value="8000"/>')

README = """Epithelial observation-horizon study (Morpheus v2.3.9, CPU only)

WHAT IT TESTS
  ONE scoped hypothesis: are the closure thresholds measured at StopTime 1000 unchanged when
  the observation horizon is extended 8x? Nothing here revisits the frozen fixed-horizon FAIL
  on J-scaling, and nothing here can turn it into a pass. A horizon effect found here is a new
  finding about observation horizon, not a revision of that result.

WHY ONLY 30 ARMS
  The minimum feasible spread is max(lo/J) / min(hi/J), so at each gap only two J columns can
  set it: the lowest J sets the numerator, the highest sets the denominator. A longer horizon
  can only turn ARRESTED into CLOSED, which moves a bracket UP. So if the hi-side arm at the
  highest J closes later the spread SHRINKS; if the hi-side arm at the lowest J closes later it
  GROWS. Both directions are in the selected set, so this design can move the result either
  way. The middle J columns cannot set the statistic and are not re-run.

  Per selected cell: the three hi-side arrested arms a longer horizon could flip, the three one
  grid step above them so a flipped bracket keeps an upper edge instead of becoming UNRESOLVED,
  and one already-closed arm as a positive control. Plus one deep-arrested negative control per
  gap at lambda_V 12.8.

HORIZON SCHEDULE
  One trajectory per arm to StopTime 8000, read at horizons 1000, 2000, 4000 and 8000.
  Justified by measurement before freezing: a StopTime 2000 run reproduces the StopTime 1000
  run's logger BYTE-IDENTICALLY for t<=1000, so extending the stop time does not perturb the
  trajectory. log_step stays 10, identical to the original, or the reproduction control cannot
  be evaluated byte-wise.

REPRODUCTION CONTROL  (gates interpretation)
  Every extended arm's logger rows at t<=1000 must be BYTE-IDENTICAL to that arm's native
  logger from the previous CPU run. Columns: time, cell.id, cell.center.x, cell.center.y,
  cell.volume, cell.surface. No numeric tolerance: the solver is deterministic for a fixed seed
  and a pinned binary -- measured before freezing, a local rerun reproduced the VM's native
  logger byte for byte on different hardware -- so a tolerance would hide exactly the
  nondeterminism this control exists to detect. The binary is pinned by sha256; the host is NOT
  asserted identical, and this control is what establishes the difference did not matter.
  One arm failing makes that arm's horizon readings UNINTERPRETABLE. More than one voids the
  trajectory-reuse justification for the whole packet.

CONTROLS
  POSITIVE: four already-closed arms must close again by horizon 1000.
  NEGATIVE: two deep-arrested arms (lambda_V 12.8) must NOT close by the final horizon. If they
  close, arrest is horizon-fragile everywhere and no bracket in the study is interpretable.
  CENSORING: an arm still shrinking at the final horizon is reported as censored. Descriptive
  only -- a finite window bounds nothing about closure beyond it.
  Thresholds stay INTERVALS. UNRESOLVED is never a pass and is never dropped. Non-monotone
  bracket motion is reported as observed. Seeds are classified individually and never pooled
  into a mean before classification.

HOW SUCCESS IS DECIDED
  run_packet.sh never decides its own success. Its exit status is audit_completeness.py's, and
  all four exit codes (job wrapper, reproduction, completeness, horizon analysis) are preserved
  in exit-codes.json. A run is complete only if all 30 declared ids are present, exited 0, and
  produced a logger with every required field, at least two sampled times and finite values.

TIMING GATE
  Before the scientific tree, one SHORT probe (StopTime 500, first arm) runs in the workspace,
  never in the output. It measures the real rate and REFUSES to start if the projected per-arm
  time exceeds the declared 55 s by more than TIMING_GATE_FACTOR (default 2.0), or if the
  projected wall time exceeds the whole-tree bound. Exit 4.

COST AND CAPS  (measured, not estimated)
  Basis: 6.85 s and 285,927 bytes per 1000 model-time units, peak RSS 10.8 MB, linear in both,
  measured locally at StopTime 1000 and 2000 on one arm.
  30 arms x StopTime 8000 -> ~55 s/arm, ~1,650 CPU-s, ~68.6 MB of loggers.
  Requested: 4-8 vCPU, <=12 GiB, one thread per arm, JOB_TIMEOUT_S=1800 whole tree,
  OUTPUT_CAP_MB=100. At 8 workers the projection is ~210 s wall.
  Please still wrap arms in MemoryMax/MemorySwapMax=0/TasksMax; MemoryMax alone bounds nothing
  on a host with swap.

EXIT STATUS
  run_packet.sh : 0 complete, 1 incomplete, 3 refused before running, 4 timing gate refused,
                  5 output cap exceeded.
  check_reproduction.py : 0 all reproduced, 1 otherwise.
  analyze_horizon.py : 0 clean, 2 if arms are missing, uninterpretable, or a control failed.

WHAT IS NOT CLAIMED
  Nothing is calibrated to a cell line, a species or a measured tissue. Model-time units are
  not calibrated tissue time. Long-horizon behaviour is unknown until observed, and 8x is not
  "the long run". NO lattice frames are produced and NO movie can be made: centre and volume
  logs do not define cell shapes or a wound boundary, and none will be invented from them.

PROVENANCE
  Each model.xml is the EXACT model.xml of that arm's previous run with one named edit,
  StopTime 1000 -> 8000, required to match exactly once. Verify models/ against SHA256SUMS
  before running; run_packet.sh does that for you with verify_packet.py, refusing duplicates,
  symlinks, path traversal, unlisted files and hash mismatches.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--native-return", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    proto = json.loads(Path(a.protocol).read_text())
    S = Path(a.native_return) / "science"
    out = Path(a.out)
    stage = out.parent / "_horizon_packet"
    if stage.exists():
        shutil.rmtree(stage)
    models = stage / "models"
    models.mkdir(parents=True)

    pins, arms = {}, []
    for spec in proto["arms"]:
        d = S / spec["id"]
        src = (d / "model.xml").read_text()
        if src.count(EDIT[0]) != 1:
            raise SystemExit(f"refused: {spec['id']} StopTime edit matches {src.count(EDIT[0])} times")
        (models / f"{spec['id']}.xml").write_text(src.replace(*EDIT))
        pins[spec["id"]] = hashlib.sha256(prefix_bytes(d / "logger.csv")).hexdigest()
        arms.append(spec)

    (stage / "arms.json").write_text(json.dumps(arms, indent=1))
    (stage / "horizon-protocol.json").write_text(Path(a.protocol).read_text())
    (stage / "reproduction-pins.json").write_text(json.dumps(dict(
        t_max=1000.0, policy="byte-identical, no tolerance",
        extracted_by="check_reproduction.prefix_bytes, the same function the checker uses",
        source="the previous CPU run's native loggers, which are NOT shipped",
        prefix_sha256=pins), indent=1))
    (stage / "README.md").write_text(README)
    here = Path(__file__).parent / "packet_files_horizon"
    shared = Path(__file__).parent / "packet_files"
    for f in SCRIPTS:
        src = here / f if (here / f).exists() else shared / f
        (stage / f).write_bytes(src.read_bytes())

    sums = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(stage)}"
            for p in sorted(stage.rglob("*")) if p.is_file() and p.name != "SHA256SUMS"]
    (stage / "SHA256SUMS").write_text("\n".join(sums) + "\n")

    files = sorted(q for q in stage.rglob("*") if q.is_file() and not q.is_symlink())
    assert len({q.relative_to(stage) for q in files}) == len(files), "duplicate archive member"
    with tarfile.open(out, "w:gz") as tf:
        for q in files:
            ti = tf.gettarinfo(str(q), arcname=str(q.relative_to(stage)))
            assert ti.isfile(), f"refusing non-regular member {ti.name}"
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            with q.open("rb") as fh:
                tf.addfile(ti, fh)
    shutil.rmtree(stage)
    print(f"{out}  {out.stat().st_size} bytes  sha256 {hashlib.sha256(out.read_bytes()).hexdigest()}  "
          f"arms {len(arms)}  members {len(files) + 1}")


if __name__ == "__main__":
    main()
