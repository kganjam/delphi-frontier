#!/usr/bin/env python3
"""Keep the repo's swarm/ and the live /data/swarm in agreement, and make drift VISIBLE.

THE PROBLEM THIS EXISTS FOR, measured 2026-11-04. /data/swarm is not a git repository: the
dispatcher, generator, harvester and spec checker run from an unversioned disk path, while this
repo carries copies of the same files. Nothing documented the relationship and nothing checked it.
Three of eleven shared files had drifted, IN BOTH DIRECTIONS:

  live ahead  -- harvest.py and swarm.py carried fixes that existed nowhere else and would have
                 been lost with the directory
  repo ahead  -- evidence.py had been fixed to honour SWARM_PROJECT instead of a hardcoded
                 'zebrafish-flight', and the fix was NEVER DEPLOYED, so pointing the pipeline at
                 another project would have scored the fish's claims and reported a clean pass

Both directions matter, which is why this does NOT simply copy the repo over the live path. A
one-way deploy would have destroyed the first case while fixing the second.

WHAT IT DOES. `--check` reports every differing file WITH THE DIRECTION, inferred from git: a file
whose live copy differs from the repo but whose repo copy is unchanged since the last commit is
LIVE-AHEAD and must be committed, not overwritten. `--deploy` copies repo to live, backing up
first, and REFUSES any live-ahead file unless --force is given, because that is the case where
copying loses work.

WHY A CHECKER AND NOT A SYMLINK. Making /data/swarm a symlink into a worktree would couple a
running fleet to whatever an agent has half-edited; the monitor has been running from this path
for 178 iterations. Visibility is the right-sized fix: drift becomes a failing check rather than
an invisible divergence.

Usage:
    python3 swarm/deploy.py --check              # exit 1 if anything differs
    python3 swarm/deploy.py --deploy [--force]   # repo -> live, backing up
    python3 swarm/deploy.py --selftest           # controls, touches nothing
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LIVE = Path("/data/swarm")
REPO_SWARM = Path(__file__).resolve().parent


def repo_dirty(path: Path) -> bool:
    """True if the repo copy has uncommitted changes (so the repo side is itself in flux)."""
    r = subprocess.run(["git", "-C", str(REPO_SWARM.parent), "status", "--porcelain", "--",
                        str(path.relative_to(REPO_SWARM.parent))],
                       capture_output=True, text=True, timeout=60)
    return bool(r.stdout.strip())


# The first version scanned "*.py" only. monitor.sh -- the loop that had been driving the fleet
# for 178 iterations, and which IS tracked in the repo -- fell outside that domain, so drift in it
# would have been invisible to the tool written to make drift visible. Asking what a check's domain
# EXCLUDES is the habit; this is what it caught.
PATTERNS = ("*.py", "*.sh")


def shared() -> list[str]:
    names = {p.name for pat in PATTERNS for p in REPO_SWARM.glob(pat)}
    return sorted(n for n in names if (LIVE / n).exists())


def classify(name: str) -> tuple[str, str]:
    repo, live = REPO_SWARM / name, LIVE / name
    if filecmp.cmp(repo, live, shallow=False):
        return "same", ""
    # Direction. If the repo copy is committed and clean, the live copy is the one carrying
    # unreviewed edits -- that is LIVE-AHEAD and copying over it would destroy them.
    if repo_dirty(repo):
        return "both-moved", "repo copy has uncommitted changes AND differs from live"
    return "live-ahead", (f"live {live.stat().st_size}B vs repo {repo.stat().st_size}B; "
                          "the repo copy is committed and clean, so the live edits are "
                          "unreviewed and unversioned -- COMMIT them, do not overwrite")


def do_check() -> int:
    names = shared()
    drift = []
    print(f"{len(names)} shared file(s) between {REPO_SWARM} and {LIVE}\n")
    for n in names:
        kind, why = classify(n)
        if kind == "same":
            print(f"  same        {n}")
        else:
            drift.append((n, kind, why))
            print(f"  {kind.upper():<11} {n}   {why}")
    only_live = sorted({p.name for pat in PATTERNS for p in LIVE.glob(pat)
                        if not (REPO_SWARM / p.name).exists() and ".bak" not in p.name})
    if only_live:
        print(f"\n  UNVERSIONED (live only, no repo copy): {', '.join(only_live)}")
        drift.append(("<live-only>", "unversioned", ", ".join(only_live)))
    if not drift:
        print("\nno drift")
        return 0
    print(f"\n{len(drift)} file(s) differ. A LIVE-AHEAD file must be COMMITTED, not deployed over.")
    return 1


def do_deploy(force: bool) -> int:
    rc = 0
    for n in shared():
        kind, why = classify(n)
        if kind == "same":
            continue
        if kind in ("live-ahead", "both-moved") and not force:
            print(f"  REFUSING {n}: {why}")
            rc = 1
            continue
        bak = LIVE / f"{n}.bak-deploy"
        shutil.copy2(LIVE / n, bak)
        shutil.copy2(REPO_SWARM / n, LIVE / n)
        print(f"  deployed {n} (previous kept at {bak})")
    if rc:
        print("\nNothing was overwritten for the refused files. Commit them, then re-run.")
    return rc


def do_selftest() -> int:
    """Controls in a scratch tree. A deploy tool that cannot refuse is a deploy tool that
    silently destroys work, so the must-refuse case is tested first and by construction."""
    global LIVE, REPO_SWARM
    ok = 0
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "repo").mkdir()
        (t / "live").mkdir()
        orig_live, orig_repo = LIVE, REPO_SWARM
        LIVE, REPO_SWARM = t / "live", t / "repo"
        try:
            (REPO_SWARM / "run.sh").write_text("echo hi\n")
            (LIVE / "run.sh").write_text("echo hi\n")
            (REPO_SWARM / "same.py").write_text("x = 1\n")
            (LIVE / "same.py").write_text("x = 1\n")
            (REPO_SWARM / "moved.py").write_text("y = 1\n")
            (LIVE / "moved.py").write_text("y = 2\n")
            (LIVE / "orphan.py").write_text("z = 3\n")

            assert shared() == ["moved.py", "run.sh", "same.py"], shared()
            print("  ok  shared() lists files on BOTH sides, INCLUDING shell scripts"); ok += 1
            assert classify("same.py")[0] == "same"
            print("  ok  identical files classify as same"); ok += 1
            k, _ = classify("moved.py")
            assert k in ("live-ahead", "both-moved"), k
            print(f"  ok  differing file classifies as {k}, not as deployable"); ok += 1
            rc = do_deploy(force=False)
            assert rc == 1, "MUST-REFUSE FAILED: deploy did not refuse a drifted file"
            assert (LIVE / "moved.py").read_text() == "y = 2\n", \
                "MUST-REFUSE FAILED: live file was overwritten despite refusal"
            print("  ok  MUST-REFUSE: drifted file not overwritten, exit 1"); ok += 1
            rc = do_deploy(force=True)
            assert (LIVE / "moved.py").read_text() == "y = 1\n", "force did not deploy"
            assert (LIVE / "moved.py.bak-deploy").read_text() == "y = 2\n", "no backup kept"
            print("  ok  --force deploys AND keeps the previous bytes as a backup"); ok += 1
            assert do_check() == 1, "check did not flag the live-only orphan"
            print("  ok  a live-only file is reported as UNVERSIONED"); ok += 1
        finally:
            LIVE, REPO_SWARM = orig_live, orig_repo
    print(f"\n{ok}/6 controls pass, including the must-refuse arm")
    return 0 if ok == 6 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return do_selftest()
    if a.deploy:
        return do_deploy(a.force)
    return do_check()


if __name__ == "__main__":
    sys.exit(main())
