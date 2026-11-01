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
    """A verdict over an empty set is not a verdict."""
    print("\nH3 the analyzer refuses to call an empty comparison SUPPORTED")
    proto = json.loads((packet / "horizon-protocol.json").read_text())
    hdr = "time\tcell.id\tcell.center.x\tcell.center.y\tcell.volume\tcell.surface\n"
    body = hdr + "".join(f"{t}\t1\t10\t10\t37500\t88.6\n" for t in range(0, 8001, 10))
    for label, verdict, want in (("reproduction VOID", "VOID", "UNINTERPRETABLE"),
                                 ("reproduction REPRODUCED but nothing evaluable", "REPRODUCED", "UNRESOLVED")):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            out = td / "out"
            for a in proto["arms"]:
                (out / a["id"]).mkdir(parents=True)
                (out / a["id"] / "logger.csv").write_text(body)
                (out / a["id"] / "exit.txt").write_text("exit=0\n")
            allarms = [a["id"] for a in proto["arms"]]
            (td / "rep.json").write_text(json.dumps(dict(
                verdict=verdict,
                diverged_arms=allarms if verdict == "VOID" else [],
                missing_arms=[])))
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
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} controls pass")
    for n in bad:
        print(f"  FAILED {n}")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
