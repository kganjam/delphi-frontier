"""Compile ActuationMotion.lean (must pass) and ActuationMotionNegative.lean (every MUTANT must be rejected, every
CORRECT twin must compile) and write artifacts/xenomodel/lean-receipt.json. Hand-authored statements; see the receipt's
statement_origin. Capped local job: systemd-run MemoryMax=12G MemorySwapMax=0 TasksMax=128 RuntimeMaxSec=3000.
Calls lean directly with LEAN_PATH from the pinned Mathlib project (lake env was observed to stall under host I/O load)."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "engineering/formalize/lean"
PROJECT = Path(os.environ.get("FRONTIER_LEAN_PROJECT", "/data/artifacts/mathlib-probe"))
LEAN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.35.0/bin/lean"
POS, NEG = "ActuationMotion.lean", "ActuationMotionNegative.lean"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def compile_(name):
    lp = ":".join(str(p) for p in sorted((PROJECT / ".lake/packages").glob("*/.lake/build/lib/lean")))
    cmd = ["systemd-run", "--user", "--scope", "-q", "-p", "TasksMax=128", "-p", "MemoryMax=12G", "-p", "MemorySwapMax=0",
           "-p", "RuntimeMaxSec=3000", f"--setenv=LEAN_PATH={lp}", str(LEAN), "-j2", str(HERE / name)]
    t = time.time(); p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return {"argv": [str(LEAN), "-j2", f"engineering/formalize/lean/{name}"], "exit": p.returncode, "seconds": round(time.time() - t, 1),
            "out": (p.stdout + p.stderr).replace(str(ROOT) + "/", "")}

def blocks(src):
    """line ranges of each MUTANT / CORRECT block in the negative file"""
    lines = src.splitlines(); marks = [(i + 1, m.group(1)) for i, l in enumerate(lines) if (m := re.match(r"-- (MUTANT-\d+|CORRECT twin)", l))]
    out = []
    for k, (start, label) in enumerate(marks):
        end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(lines)
        out.append({"label": label if label.startswith("MUTANT") else f"CORRECT@{start}", "lines": [start, end]})
    return out

def main():
    with ThreadPoolExecutor(2) as ex:
        pos, neg = ex.map(compile_, [POS, NEG])
    axioms = re.findall(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]", pos["out"], re.S)
    per = {n: sorted(a.strip() for a in lst.replace("\n", " ").split(",") if a.strip()) for n, lst in axioms}
    pos_errors = [l for l in pos["out"].splitlines() if ": error" in l]
    err_lines = [int(m.group(1)) for l in neg["out"].splitlines() if (m := re.search(rf"{NEG}:(\d+):\d+: error", l))]
    bl = blocks((HERE / NEG).read_text())
    for b in bl:
        b["error_lines"] = [e for e in err_lines if b["lines"][0] <= e <= b["lines"][1]]
        b["rejected"] = bool(b["error_lines"])
    mutants = [b for b in bl if b["label"].startswith("MUTANT")]; twins = [b for b in bl if b["label"].startswith("CORRECT")]
    unattributed = [e for e in err_lines if not any(b["lines"][0] <= e <= b["lines"][1] for b in bl)]
    ok = (pos["exit"] == 0 and not pos_errors and per and all(set(v) <= STANDARD for v in per.values()) and "sorryAx" not in pos["out"]
          and neg["exit"] != 0 and all(m["rejected"] for m in mutants) and not any(t["rejected"] for t in twins) and not unattributed)
    man = json.loads((PROJECT / "lake-manifest.json").read_text())
    rec = {
        "schema": "frontier.actuation-motion-lean-receipt/1", "status": "pass" if ok else "fail",
        "statement_origin": "hand-authored by the claude-xenomodel harness from the derivation in docs/xenomodel/actuation-motion-equations.md; not extracted from a language-model answer; the correspondence to engine code is by the cited source lines only",
        "lean_version": subprocess.run([str(LEAN), "--version"], capture_output=True, text=True).stdout.strip(),
        "mathlib": {"revision": next(p["rev"] for p in man["packages"] if p["name"] == "mathlib"), "manifest_sha256": sha(PROJECT / "lake-manifest.json"),
                    "url": "https://github.com/leanprover-community/mathlib4", "toolchain_file": (PROJECT / "lean-toolchain").read_text().strip()},
        "source": {"path": f"engineering/formalize/lean/{POS}", "sha256": sha(HERE / POS)},
        "mutant_source": {"path": f"engineering/formalize/lean/{NEG}", "sha256": sha(HERE / NEG)},
        "runner": {"path": "engineering/formalize/actuation_motion_lean_run.py", "sha256": sha(Path(__file__))},
        "positive": {"argv": pos["argv"], "exit": pos["exit"], "seconds": pos["seconds"], "errors": pos_errors, "theorems": sorted(per),
                     "n_theorems": len(per), "theorem_axiom_sets": per, "only_standard_axioms": bool(per) and all(set(v) <= STANDARD for v in per.values()),
                     "sorryAx": "sorryAx" in pos["out"], "stdout": pos["out"]},
        "negative": {"argv": neg["argv"], "exit": neg["exit"], "seconds": neg["seconds"], "mutants": mutants, "correct_twins": twins,
                     "all_mutants_rejected": all(m["rejected"] for m in mutants), "no_twin_rejected": not any(t["rejected"] for t in twins),
                     "unattributed_error_lines": unattributed, "stdout": neg["out"]},
        "satisfiability_witnesses": ["absolute_damping_hypotheses_satisfiable (deforming 2-node body, COM fixed)", "crawler_hypotheses_satisfiable (anisotropic substrate, D = 1/2)",
                                     "heterogeneous_mass_breaks_com and arithmetic_centroid_moves_with_heterogeneous_drag (proved counterexamples showing dropped hypotheses matter)"],
        "proves": "A: Voxelyze-form symplectic Euler with homogeneous mass, one -C v damping, internal forces summing to zero, zero external horizontal force and zero initial momentum keeps the horizontal COM fixed for every step (and the contrapositive necessity). B: overdamped linear drag keeps the drag-weighted centroid fixed and forbids net displacement per shape cycle for any actuation. C: two-node direction-dependent-friction crawler: per-step midpoint motion kappa|delta|, pathwise kappa*TV(L), cycle A(xi_m - xi_p)/(xi_p + xi_m), zero iff isotropic, mirror negation, linearity in amplitude.",
        "does_not_prove": ["that Voxelyze link forces are exactly pairwise antisymmetric in floating point (assumed; corroborated by control D)", "the Coulomb-friction mirror argument (Section 5 of the doc is on paper only)",
                           "Theorem 1' (heterogeneous linear damping, periodic orbit) - paper derivation only", "anything about tissue, cilia, Xenopus or a built construct"],
        "caps": "systemd-run --user --scope MemoryMax=12G MemorySwapMax=0 TasksMax=128 RuntimeMaxSec=3000",
    }
    out = ROOT / "artifacts/xenomodel/lean-receipt.json"; out.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"status": rec["status"], "pos_exit": pos["exit"], "n_theorems": len(per), "neg_exit": neg["exit"],
                      "mutants_rejected": [m["label"] for m in mutants if m["rejected"]], "twins_rejected": [t["label"] for t in twins if t["rejected"]], "unattributed": unattributed}))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
