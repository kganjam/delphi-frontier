"""Controls for the horizon packet. Each runs against a case it must flag and one it must not.

No Morpheus arm is run here except one short reproduction fixture, which exists precisely to
prove that a real extended run reproduces the shipped prefix pin. Nothing writes into the
frozen protocol, the native return or anything under dff5e58.

    python3 engineering/epithelial/test_horizon_controls.py --packet <extracted> --native-return <dir>
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

results: list[tuple[str, bool]] = []


def check(name: str, got, want) -> None:
    ok = got == want
    results.append((name, ok))
    print(f"  {'ok  ' if ok else 'BAD '}{name}: got {got!r}, want {want!r}")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def c_models_differ_only_by_stoptime(packet: Path, native: Path) -> None:
    """The only permitted change is the declared observation-horizon factor."""
    print("\nH1 every model is the native model with one StopTime edit")
    arms = json.loads((packet / "arms.json").read_text())
    bad = []
    for a in arms:
        src = (native / "science" / a["id"] / "model.xml").read_text()
        dst = (packet / "models" / f"{a['id']}.xml").read_text()
        d = [l for l in difflib.unified_diff(src.splitlines(), dst.splitlines(), lineterm="")
             if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        if d != ['-        <StopTime value="1000"/>', '+        <StopTime value="8000"/>']:
            bad.append(a["id"])
    check("H1 models changed only in StopTime", bad, [])
    check("H1 arm count", len(arms), 30)


def c_reproduction(packet: Path, native: Path) -> None:
    """Positive: a real short extended run must match the pin. Negative: one byte must break it."""
    print("\nH2 reproduction pins, against a real run and a mutated one")
    sys.path.insert(0, str(packet))
    from check_reproduction import prefix_bytes  # noqa: E402
    pins = json.loads((packet / "reproduction-pins.json").read_text())
    arm = "S-k4-J560-lamV1.6-s1"
    binary = Path("/data/worktrees/delphi-frontier/epithelial-repair/.scratch/morpheus-2.3.9")
    if not binary.exists():
        check("H2 SKIPPED (no local binary)", True, True)
        return
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "out" / arm
        d.mkdir(parents=True)
        # a cheap extension: past the 1000 boundary, far short of 8000
        (d / "model.xml").write_text(
            (packet / "models" / f"{arm}.xml").read_text()
            .replace('<StopTime value="8000"/>', '<StopTime value="1200"/>'))
        run([str(binary), "-f", "model.xml", "--no-gnuplot", "--num-threads", "1"], cwd=d)
        got = hashlib.sha256(prefix_bytes(d / "logger.csv")).hexdigest()
        check("H2 real extended run matches the shipped pin", got, pins["prefix_sha256"][arm])
        r = run([sys.executable, str(packet / "check_reproduction.py"),
                 "--pins", str(packet / "reproduction-pins.json"),
                 "--out", str(d.parent), "--report", str(Path(td) / "r.json")])
        rep = json.loads((Path(td) / "r.json").read_text())
        check("H2 that arm reads REPRODUCED", rep["per_arm"][arm]["status"], "REPRODUCED")
        check("H2 29 missing arms make the verdict VOID", rep["verdict"], "VOID")
        check("H2 checker exits non-zero on VOID", r.returncode, 1)
        b = (d / "logger.csv").read_bytes()
        i = b.index(b"\n", b.index(b"\n") + 1)
        (d / "logger.csv").write_bytes(b[:i - 3] + b"9" + b[i - 2:])
        run([sys.executable, str(packet / "check_reproduction.py"),
             "--pins", str(packet / "reproduction-pins.json"),
             "--out", str(d.parent), "--report", str(Path(td) / "r2.json")])
        rep2 = json.loads((Path(td) / "r2.json").read_text())
        check("H2 one flipped byte reads DIVERGED", rep2["per_arm"][arm]["status"], "DIVERGED")


def c_no_vacuous_verdict(packet: Path) -> None:
    """A verdict over an empty set, or over a falsifier that was never exercised, is not a verdict."""
    print("\nH3 the analyzer refuses to call an unexercised comparison SUPPORTED")
    proto = json.loads((packet / "horizon-protocol.json").read_text())
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"

    def traj(close_at):
        return hdr + "".join(
            f"{t}\t1\t10\t10\t{40000 if (close_at is not None and t >= close_at) else 37500}\t88.6\n"
            for t in range(0, 8001, 10))

    # (a) reproduction VOID -> UNINTERPRETABLE, whatever the arms say
    # (b) reproduction fine, controls fine, but every hi-side arm is ALREADY closed at the
    #     baseline, so the declared falsifier can never fire -> UNRESOLVED, not SUPPORTED
    for label, verdict, close_at, want in (
            ("reproduction VOID", "VOID", None, "UNINTERPRETABLE"),
            ("falsifier never exercised", "REPRODUCED", 100, "UNRESOLVED")):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            out = td / "out"
            for a in proto["arms"]:
                d = out / a["id"]
                d.mkdir(parents=True)
                # the NEGATIVE controls must never close, or they fail and the run is
                # uninterpretable for that reason instead of the one under test
                c = None if a["role"].startswith("NEGATIVE") else close_at
                (d / "logger.csv").write_text(traj(c))
                (d / "exit.txt").write_text("exit=0\n")
            allarms = [a["id"] for a in proto["arms"]]
            (td / "rep.json").write_text(json.dumps(dict(
                verdict=verdict, diverged_arms=allarms if verdict == "VOID" else [], missing_arms=[])))
            run([sys.executable, str(packet / "analyze_horizon.py"),
                 "--protocol", str(packet / "horizon-protocol.json"), "--out", str(out),
                 "--reproduction", str(td / "rep.json"), "--report", str(td / "h.json")])
            got = json.loads((td / "h.json").read_text())["hypothesis_outcome"].split(":")[0]
            check(f"H3 {label} -> {want}", got, want)


def c_audit_key_and_crash(packet: Path) -> None:
    print("\nH4 the completeness audit accepts both arm-key spellings and refuses neither")
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"
    body = hdr + "0\t1\t10\t10\t625\t88\n10\t1\t11\t11\t620\t88\n"
    for key, want in (("id", 0), ("name", 0), ("bogus", 3)):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            out = td / "out"
            (out / "A").mkdir(parents=True)
            (out / "A" / "logger.csv").write_text(body)
            (out / "A" / "exit.txt").write_text("exit=0\n")
            (td / "arms.json").write_text(json.dumps([{key: "A"}]))
            r = run([sys.executable, str(packet / "audit_completeness.py"), "--arms", str(td / "arms.json"),
                     "--out", str(out), "--job-wrapper-exit", "0", "--report", str(td / "c.json")])
            check(f"H4 arms keyed by {key!r} -> exit {want}", r.returncode, want)
            if want == 0:
                check(f"H4 arms keyed by {key!r} wrote a report", (td / "c.json").exists(), True)


def c_truncation_regression(packet: Path, native: Path) -> None:
    """THE regression. The real 1000-only logs produced rc0 SUPPORTED before the repair."""
    print("\nH5 the demonstrated false pass: real 1000-only logs staged as a finished 8000 run")
    proto = json.loads((packet / "horizon-protocol.json").read_text())
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        out = td / "out"
        for a in proto["arms"]:
            d = out / a["id"]
            d.mkdir(parents=True)
            shutil.copy(native / "science" / a["id"] / "logger.csv", d / "logger.csv")
            (d / "exit.txt").write_text("exit=0\n")
        r1 = run([sys.executable, str(packet / "check_reproduction.py"),
                  "--pins", str(packet / "reproduction-pins.json"), "--out", str(out),
                  "--report", str(td / "rep.json")])
        check("H5 reproduction still passes on these logs (they ARE the native ones)", r1.returncode, 0)
        r2 = run([sys.executable, str(packet / "analyze_horizon.py"),
                  "--protocol", str(packet / "horizon-protocol.json"), "--out", str(out),
                  "--reproduction", str(td / "rep.json"), "--report", str(td / "h.json")])
        h = json.loads((td / "h.json").read_text())
        check("H5 analysis REFUSES (exit 2, was 0)", r2.returncode, 2)
        check("H5 headline is not SUPPORTED", h["hypothesis_outcome"].startswith("UNINTERPRETABLE"), True)
        check("H5 all 30 arms are named as missing the final horizon",
              len(h["coverage"]["arms_missing_the_final_horizon"]), 30)
        check("H5 no arm claims horizon 8000 observed",
              sum(1 for v in h["per_arm"].values() if v["per_horizon"]["8000"]["observed"]), 0)


def c_falsifier_direct(packet: Path) -> None:
    """A hi-side arm closing later must falsify even when its group never brackets."""
    print("\nH6 the per-arm falsifier fires where bracket motion is blind")
    proto = json.loads((packet / "horizon-protocol.json").read_text())
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"

    def traj(close_at):
        out = [hdr]
        for t in range(0, 8001, 10):
            v = 40000 if (close_at is not None and t >= close_at) else 37500
            out.append(f"{t}\t1\t10\t10\t{v}\t88.6\n")
        return "".join(out)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        out = td / "out"
        # pick a hi-side arm in a group that has NO positive control (seed != 1), so the group
        # is UNRESOLVED at baseline; then close BOTH it and its next lambda by the final horizon,
        # so the group is UNRESOLVED again at the end and the bracket tuple never moves.
        target = next(a for a in proto["arms"]
                      if a["role"].startswith("bracket hi-side") and a["seed"] != 1)
        group = [a for a in proto["arms"]
                 if a["gap_k"] == target["gap_k"] and a["J"] == target["J"] and a["seed"] == target["seed"]]
        closing = {a["id"]: 4000 for a in group}
        for a in proto["arms"]:
            d = out / a["id"]
            d.mkdir(parents=True)
            # positive controls close early so the controls pass; the target group closes late
            c = 100 if a["role"].startswith("POSITIVE") else closing.get(a["id"])
            (d / "logger.csv").write_text(traj(c))
            (d / "exit.txt").write_text("exit=0\n")
        target = target["id"]
        (td / "rep.json").write_text(json.dumps(dict(verdict="REPRODUCED", diverged_arms=[], missing_arms=[])))
        r = run([sys.executable, str(packet / "analyze_horizon.py"),
                 "--protocol", str(packet / "horizon-protocol.json"), "--out", str(out),
                 "--reproduction", str(td / "rep.json"), "--report", str(td / "h.json")])
        h = json.loads((td / "h.json").read_text())
        key = [k for k in h["bracket_motion"] if target.split("-lamV")[0].replace("S-", "") in k.replace("-s", "-s")]
        blind = [k for k, v in h["bracket_motion"].items()
                 if v["baseline_1000"]["state"] == "UNRESOLVED" and v["final"]["state"] == "UNRESOLVED"
                 and not v["moved"]]
        check("H6 the target's group is UNRESOLVED at both ends, so tuple motion is blind",
              len(blind) >= 1, True)
        check("H6 the falsifier names the closing hi-side arm", h["falsifier"]["falsified_by"], [target])
        check("H6 headline is NOT SUPPORTED", h["hypothesis_outcome"].startswith("NOT SUPPORTED"), True)
        check("H6 exit 0 (a real scientific verdict, not a refusal)", r.returncode, 0)


def c_failed_control_blocks_headline(packet: Path) -> None:
    print("\nH7 a failed required control removes the headline")
    proto = json.loads((packet / "horizon-protocol.json").read_text())
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"
    neg = [a["id"] for a in proto["arms"] if a["role"].startswith("NEGATIVE")][0]

    def traj(close_at):
        return hdr + "".join(
            f"{t}\t1\t10\t10\t{40000 if (close_at is not None and t >= close_at) else 37500}\t88.6\n"
            for t in range(0, 8001, 10))

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        out = td / "out"
        for a in proto["arms"]:
            d = out / a["id"]
            d.mkdir(parents=True)
            # positive controls close early as required; the NEGATIVE control wrongly closes too
            c = 100 if a["role"].startswith("POSITIVE") else (6000 if a["id"] == neg else None)
            (d / "logger.csv").write_text(traj(c))
            (d / "exit.txt").write_text("exit=0\n")
        (td / "rep.json").write_text(json.dumps(dict(verdict="REPRODUCED", diverged_arms=[], missing_arms=[])))
        r = run([sys.executable, str(packet / "analyze_horizon.py"),
                 "--protocol", str(packet / "horizon-protocol.json"), "--out", str(out),
                 "--reproduction", str(td / "rep.json"), "--report", str(td / "h.json")])
        h = json.loads((td / "h.json").read_text())
        check("H7 the negative control is recorded failed", h["controls_failed"], [neg])
        check("H7 headline is UNINTERPRETABLE", h["hypothesis_outcome"].startswith("UNINTERPRETABLE"), True)
        check("H7 exit 2", r.returncode, 2)


def c_probe_gate(packet: Path) -> None:
    print("\nH8 the timing probe must have worked, not merely finished fast")
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"
    good = hdr + "".join(f"{t}\t1\t10\t10\t37500\t88.6\n" for t in range(0, 501, 10))
    cases = [("healthy probe", 0, good, 0),
             ("failed executable (fast, but rc!=0)", 127, "", 4),
             ("rc 0 but no logger", 0, None, 4),
             ("rc 0 but empty logger", 0, "", 4),
             ("rc 0 but non-finite rows", 0, hdr + "0\t1\t10\t10\tnan\t88.6\n", 4)]
    for label, rc, body, want in cases:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "arms.json").write_text(json.dumps([{"id": f"a{i}"} for i in range(30)]))
            logger = td / "logger.csv"
            if body is not None:
                logger.write_text(body)
            (td / "stdout.log").write_text("probe output")
            r = run([sys.executable, str(packet / "check_probe.py"), "--start", "100.0",
                     "--end", "100.4", "--arms", str(td / "arms.json"), "--factor", "2.0",
                     "--job-timeout", "1800", "--workers", "8", "--probe-exit", str(rc),
                     "--logger", str(logger), "--stdout", str(td / "stdout.log"),
                     "--report", str(td / "g.json")])
            check(f"H8 {label} -> exit {want}", r.returncode, want)
            check(f"H8 {label} left a receipt", (td / "g.json").exists(), True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--native-return", required=True)
    a = ap.parse_args()
    packet, native = Path(a.packet).resolve(), Path(a.native_return).resolve()
    c_models_differ_only_by_stoptime(packet, native)
    c_reproduction(packet, native)
    c_no_vacuous_verdict(packet)
    c_audit_key_and_crash(packet)
    c_truncation_regression(packet, native)
    c_falsifier_direct(packet)
    c_failed_control_blocks_headline(packet)
    c_probe_gate(packet)
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} controls pass")
    for n in bad:
        print(f"  FAILED {n}")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
