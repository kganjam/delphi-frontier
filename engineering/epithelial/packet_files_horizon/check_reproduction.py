"""Reproduction control: every extended run must reproduce its original StopTime=1000 logger.

The extended arm's logger rows at t <= 1000 must be BYTE-IDENTICAL to the native run's logger
from the previous CPU run. No numeric tolerance: the solver is deterministic for a fixed seed
and a pinned binary, measured before freezing on different hardware, so a tolerance would hide
exactly the nondeterminism this control exists to detect.

The native loggers are not shipped. What is pinned is the sha256 of each native logger's
t <= 1000 prefix, extracted by the same function used here, so the comparison is exact and the
packet stays small.

Exit 0 only if every arm reproduces. A failure does not stop the run; it marks those arms'
horizon readings UNINTERPRETABLE, and more than one failure voids the trajectory-reuse
justification for the whole packet.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

T_REPRO = 1000.0


def prefix_bytes(path: Path, t_max: float = T_REPRO) -> bytes:
    """Header plus every logger row whose time is <= t_max, in file order, concatenated.

    Blank lines are skipped on both sides so a trailing newline cannot change the digest.
    This exact function produced the pinned digests; do not reimplement it differently.
    """
    out = []
    with path.open("rb") as fh:
        for i, raw in enumerate(fh):
            if not raw.strip():
                continue
            if i == 0:
                out.append(raw)
                continue
            try:
                t = float(raw.split(b"\t", 1)[0])
            except ValueError:
                out.append(raw)
                continue
            if t > t_max:
                break
            out.append(raw)
    return b"".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pins", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    pins = json.loads(Path(a.pins).read_text())
    out = Path(a.out)

    per, ok, bad, absent = {}, [], [], []
    for arm, want in sorted(pins["prefix_sha256"].items()):
        log = out / arm / "logger.csv"
        if not log.exists():
            absent.append(arm)
            per[arm] = dict(status="NO LOGGER")
            continue
        got = hashlib.sha256(prefix_bytes(log)).hexdigest()
        per[arm] = dict(status="REPRODUCED" if got == want else "DIVERGED",
                        expected=want, got=got)
        (ok if got == want else bad).append(arm)

    verdict = ("REPRODUCED" if not bad and not absent and ok else
               "PARTIAL" if len(bad) + len(absent) == 1 else "VOID")
    report = dict(
        schema="frontier.epithelial-horizon-reproduction.v1",
        t_max=T_REPRO, policy="byte-identical, no tolerance",
        reproduced=len(ok), diverged=len(bad), missing=len(absent),
        verdict=verdict,
        meaning={
            "REPRODUCED": "every extended run reproduces its original prefix; horizon readings "
                          "may be interpreted",
            "PARTIAL": "one arm failed; that arm's horizon readings are UNINTERPRETABLE and the "
                       "rest stand",
            "VOID": "more than one arm failed, or none ran; the trajectory-reuse justification "
                    "is void for this packet and no horizon conclusion may be drawn from it",
        }[verdict],
        diverged_arms=bad, missing_arms=absent, per_arm=per)
    Path(a.report).write_text(json.dumps(report, indent=1))
    print(f"reproduction: {len(ok)} reproduced, {len(bad)} diverged, {len(absent)} missing -> {verdict}")
    for n in (bad + absent)[:10]:
        print(f"  NOT REPRODUCED {n}")
    raise SystemExit(0 if verdict == "REPRODUCED" else 1)


if __name__ == "__main__":
    main()
