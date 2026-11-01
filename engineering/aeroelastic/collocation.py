"""Paired collocation study: the fidelity-v1 ladder under cfd04's reviewed panel-consistent collocation repair.

The repair is a labelled diagnostic variant, never the production solver. It moves only each VLM collocation
point, exactly as engineering/cfd3d/vlm_diag.py repair_colloc at b976001, and it is installed per task by
replacing the module names run.setup and fidelity.setup inside the worker, so no production byte changes. Arms,
lattice controls, effects, classification and decisions are the unchanged fidelity-v1 functions; the rules come
from the frozen fidelity-v1 protocol object. Everything is frozen in collocation-paired-v1/protocol.json.

    python -m engineering.aeroelastic.collocation run --out output          # the packet's entry point
    python -m engineering.aeroelastic.collocation preflight --out DIR       # controls + tiny non-ladder arms
    python -m engineering.aeroelastic.collocation analyze --out output
    python -m engineering.aeroelastic.collocation compare --out output      # against the fidelity-v1 return
    python -m engineering.aeroelastic.collocation pack --measured PREFLIGHT_DIR/preflight.json
"""

import argparse
import contextlib
import gzip
import io
import json
import math
import multiprocessing
import platform
import subprocess
import tarfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path

import numpy as np
import scipy

from engineering.cfd3d import vlm

from . import fidelity, model, run
from .controls import run as original_controls
from .model import ART, ROOT, dump

CP = ART / "collocation-paired-v1"
PLANAR = (
    np.zeros(3),
    np.array([0, 1.0, 0]),
    np.array([1.0, 0, 0]),
    np.array([0, 0, 1.0]),
)
RECT = np.array([[-0.5, 0.0], [0.5, 0.0], [0.5, 0.25], [-0.5, 0.25]])
PLATEAU = [(32, 4), (32, 8), (32, 16)]
TIGHT = 1e-12
COLLOCATION_CHECKS = [
    "K1_exact_repair",
    "K2_baseline_unchanged",
    "K3_rectangle_invariance",
    "K4a_law_repaired",
    "K4b_quarter_chord_mutant_rejected",
    "K4c_chord_plateau_discriminates",
]


def cprotocol():
    return json.loads((CP / "protocol.json").read_text())


def references():
    return json.loads((CP / "vlm-references.json").read_text())


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------- the variant
def repair(lattice, origin, e_u, e_w, f=0.75, one_sided=False):
    """cfd04's repair_colloc (b976001), same operation order: collocation at fraction f of the panel's own
    corners, averaged over its two strip edges. Only C changes. one_sided is the K4d mutant (inboard edge only)."""
    uw = lattice[
        "uw"
    ]  # corners: edge i front, edge i+1 front, edge i+1 rear, edge i rear
    um = 0.5 * (uw[:, 0, 0] + uw[:, 1, 0])
    if one_sided:
        wc = uw[:, 0, 1] + f * (uw[:, 3, 1] - uw[:, 0, 1])
    else:
        wc = 0.5 * (
            (uw[:, 0, 1] + f * (uw[:, 3, 1] - uw[:, 0, 1]))
            + (uw[:, 1, 1] + f * (uw[:, 2, 1] - uw[:, 1, 1]))
        )
    return {**lattice, "C": origin + um[:, None] * e_u + wc[:, None] * e_w}


def repaired_setup(ns, nc, **mutant):
    """New fin dicts with repaired lattices; model.setup is lru_cached, so its dicts are never mutated."""
    return {
        name: fin
        | {
            "lattice": repair(
                fin["lattice"],
                fin["geometry"]["O"],
                fin["geometry"]["eu"],
                fin["geometry"]["ew"],
                **mutant,
            )
        }
        for name, fin in model.setup(ns, nc).items()
    }


VARIANTS = {"baseline": model.setup, "repaired": repaired_setup}


@contextlib.contextmanager
def variant(name):
    """Inside the block solve_arm and lattice_controls build lattices with the named variant."""
    saved = run.setup, fidelity.setup
    if saved != (model.setup, model.setup):
        raise RuntimeError("A collocation variant is already installed")
    run.setup = fidelity.setup = VARIANTS[name]
    try:
        yield
    finally:
        run.setup, fidelity.setup = saved


def in_variant(payload):
    """Worker entry: run one fidelity-v1 task function with the named variant installed."""
    name, function, inner = payload
    with variant(name):
        return getattr(fidelity, function)(inner)


# ---------------------------------------------------------------- collocation controls (rigid unit solves)
def fins_CL(ns, nc, kind="baseline", **mutant):
    fins = (
        model.setup(ns, nc) if kind == "baseline" else repaired_setup(ns, nc, **mutant)
    )
    return fidelity.fixed_area_CL(
        fins, {n: f["lattice"] for n, f in fins.items()}, 20.0
    )[0]


def planar_CL(builder, ns, nc, kind="baseline", **mutant):
    lattice, area = builder(ns, nc)
    if kind != "baseline":
        lattice = repair(lattice, *PLANAR[:3], **mutant)
    return float(vlm.cl_of(lattice, area, 4)[0])


def ellipse(ns, nc):
    return vlm.elliptic(6, ns, nc)


def rectangle(ns, nc):
    return vlm.lattice(RECT, *PLANAR, ns, nc), 0.25


def spread(values):
    values = list(values)
    return (max(values) - min(values)) / abs(sum(values) / len(values))


def law(CL):
    helmbold = 2 * math.pi * 6 / (2 + math.sqrt(6 * 6 + 4))
    error = CL / math.radians(4) / helmbold - 1
    return {
        "CL_alpha_over_Helmbold_minus_1": error,
        "within_3pct": bool(np.isfinite(error) and abs(error) <= 0.03),
    }


def collocation_controls(out):
    """K1-K4 of the frozen protocol; values, references and verdicts are all written out."""
    started = time.monotonic()
    ref = references()["values"]
    builders = {
        "F3_four_fins_combined": None,
        "A1_elliptic_AR6_dense": ellipse,
        "A3_rectangle_AR4": rectangle,
    }
    computed, checks = {}, {}
    for kind in ["baseline", "repaired"]:
        computed[kind] = {}
        for arm, points in ref[kind].items():
            computed[kind][arm] = {}
            for point in points:
                ns, nc = map(int, point.split("x"))
                computed[kind][arm][point] = (
                    fins_CL(ns, nc, kind)
                    if builders[arm] is None
                    else planar_CL(builders[arm], ns, nc, kind)
                )
        errors = {
            f"{arm}.{point}": abs(computed[kind][arm][point] / value - 1)
            for arm, points in ref[kind].items()
            for point, value in points.items()
        }
        checks["K1_exact_repair" if kind == "repaired" else "K2_baseline_unchanged"] = (
            all(e <= TIGHT for e in errors.values())
        )
        computed[kind]["relative_error_to_cfd04"] = errors
    lattice, _ = rectangle(32, 8)
    moved = repair(lattice, *PLANAR[:3])
    rect_C = float(np.max(abs(moved["C"] - lattice["C"])))
    rect_CL = abs(
        computed["repaired"]["A3_rectangle_AR4"]["32x8"]
        / computed["baseline"]["A3_rectangle_AR4"]["32x8"]
        - 1
    )
    checks["K3_rectangle_invariance"] = rect_C <= TIGHT * 0.25 and rect_CL <= TIGHT
    laws = {
        "repaired": {
            p: law(computed["repaired"]["A1_elliptic_AR6_dense"][p])
            for p in ["96x8", "32x24"]
        },
        "quarter_chord_mutant": {
            p: law(planar_CL(ellipse, *map(int, p.split("x")), "repaired", f=0.25))
            for p in ["96x8", "32x24"]
        },
    }
    checks["K4a_law_repaired"] = all(
        x["within_3pct"] for x in laws["repaired"].values()
    )
    checks["K4b_quarter_chord_mutant_rejected"] = not all(
        x["within_3pct"] for x in laws["quarter_chord_mutant"].values()
    )
    plateau = {
        kind: {
            "fins": spread(
                computed[kind]["F3_four_fins_combined"][f"{ns}x{nc}"]
                for ns, nc in PLATEAU
            ),
            "ellipse": spread(
                computed[kind]["A1_elliptic_AR6_dense"][f"{ns}x{nc}"]
                for ns, nc in PLATEAU
            ),
        }
        for kind in ["baseline", "repaired"]
    }
    plateau["one_sided_mutant"] = {
        "fins": spread(
            fins_CL(ns, nc, "repaired", one_sided=True) for ns, nc in PLATEAU
        ),
        "ellipse": spread(
            planar_CL(ellipse, ns, nc, "repaired", one_sided=True) for ns, nc in PLATEAU
        ),
    }
    checks["K4c_chord_plateau_discriminates"] = all(
        v <= 1e-4 for v in plateau["repaired"].values()
    ) and all(v > 1e-3 for v in plateau["baseline"].values())
    power = {k: v > 1e-4 for k, v in plateau["one_sided_mutant"].items()}
    result = {
        "schema": "frontier.aeroelastic.collocation-controls/1",
        "computed_CL": computed,
        "rectangle": {"max_abs_C_change_m": rect_C, "CL_relative_change": rect_CL},
        "law_check": laws,
        "chord_plateau_relative_range": plateau,
        "K4d_one_sided_mutant_rejected_by_plateau": power,
        "checks": checks,
        "passed": all(checks.values()),
        "reported_not_gating": ["K4d_one_sided_mutant_rejected_by_plateau"],
        "wall_seconds": time.monotonic() - started,
    }
    dump(Path(out) / "collocation-controls.json", result)
    return result


# ---------------------------------------------------------------- execution
def tasks(cp, out, deadline, lattices=None, contexts=None, overrides=None):
    """Heaviest lattice first; repaired ladder and lattice controls, then the baseline equivalence arms."""
    v1 = fidelity.fprotocol()
    lattices = lattices or sorted(v1["lattices"], key=lambda m: -fidelity.panels(v1, m))
    contexts = contexts or cp["contexts"]
    overrides = overrides or {}
    repaired, baseline = Path(out) / "repaired", Path(out) / "baseline-equivalence"
    work = [(collocation_controls, str(out))]
    for mesh in lattices:
        grid = overrides[mesh] if mesh in overrides else fidelity.override(v1, mesh)
        span, chord = (grid["span"], grid["chord"]) if grid else fidelity.grid(v1, mesh)
        for c in contexts:
            payload = (
                c["compliance"],
                c["speed_m_s"],
                mesh,
                grid,
                str(repaired),
                deadline,
            )
            work.append((in_variant, ("repaired", "arm_group", payload)))
        work.append(
            (
                in_variant,
                ("repaired", "lattice_controls", (mesh, span, chord, str(repaired))),
            )
        )
    for item in cp["baseline_references"]:
        compliance, speed, mesh = baseline_context(item)
        if mesh in lattices and not overrides:
            payload = (
                compliance,
                speed,
                mesh,
                fidelity.override(v1, mesh),
                str(baseline),
                deadline,
            )
            if (in_variant, ("baseline", "arm_group", payload)) not in work:
                work.append((in_variant, ("baseline", "arm_group", payload)))
    return work


def baseline_context(item):
    name = Path(item["path"]).parent.name  # chi0.8-u20-l32x8-rigid
    chi, speed, mesh = name.split("-")[:3]
    return float(chi[3:]), float(speed[1:]), mesh


def check_inputs(cp):
    fidelity.check_references(cp | {"references": cp["baseline_references"]})
    pin = cp["criteria"]["fidelity_v1_protocol"]
    if digest(ROOT / pin["path"]) != pin["sha256"]:
        raise ValueError("fidelity-v1 criteria changed")


def receipt(out, started, failure, cp):
    files = [p for p in out.rglob("*") if p.is_file() and p.name != "receipt.json"]
    result = {
        "schema": "frontier.aeroelastic.collocation-receipt/1",
        "collocation_protocol_sha256": digest(CP / "protocol.json"),
        "fidelity_v1_protocol_sha256": digest(fidelity.FID / "protocol.json"),
        "original_protocol_sha256": digest(ART / "protocol.json"),
        "sources": {str(p.relative_to(ROOT)): digest(p) for p in packet_sources()},
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "device": "CPU",
        },
        "wall_seconds": time.monotonic() - started,
        "failure": failure,
        "files": [
            {
                "path": str(p.relative_to(out)),
                "sha256": digest(p),
                "bytes": p.stat().st_size,
            }
            for p in files
        ],
        "dollars": None,
    }
    result["output_bytes"] = sum(x["bytes"] for x in result["files"])
    result["output_cap_exceeded"] = (
        result["output_bytes"] > cp["resources"]["output_cap_bytes"]
    )
    dump(out / "receipt.json", result)
    return result


def execute(work, out, workers):
    crashed = []
    with ProcessPoolExecutor(
        max_workers=workers, mp_context=multiprocessing.get_context("spawn")
    ) as pool:
        futures = {
            pool.submit(fn, payload): (fn.__name__, str(payload)[:200])
            for fn, payload in work
        }
        for item in as_completed(futures):
            try:
                item.result()
            except (
                Exception
            ) as exc:  # a crashed task is recorded; the others still return
                crashed.append(
                    {
                        "task": futures[item][0],
                        "payload": futures[item][1],
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                dump(out / "task-failures.json", crashed)
    return crashed


def main_run(out, preflight=False):
    if out.exists():
        raise ValueError("Fresh output directory required")
    out = out.resolve()
    out.mkdir(parents=True)
    cp = cprotocol()
    started = time.monotonic()
    failure = None
    try:
        fidelity.environment_check()
        model.check_inputs()
        check_inputs(cp)
        if not original_controls(out / "controls-original.json")["passed"]:
            raise RuntimeError("Original numerical controls failed")
        deadline = started + cp["resources"]["soft_no_new_work_seconds"]
        if (
            preflight
        ):  # non-ladder 8x2 lattice only, so no ladder result is seen before the run
            work = tasks(
                cp,
                out,
                deadline,
                ["p8x2"],
                cp["contexts"][:1],
                {"p8x2": {"span": 8, "chord": 2}},
            )
            crashed = execute(work, out, 1)
            controls = json.loads((out / "collocation-controls.json").read_text())
            summary = {
                "scope": "local preflight: original controls, K1-K4 collocation controls, one repaired arm group and repaired lattice controls on a NON-ladder 8x2 lattice; no ladder result",
                "collocation_controls_passed": controls["passed"],
                "collocation_controls_seconds": controls["wall_seconds"],
                "crashed": crashed,
            }
            dump(out / "preflight.json", summary)
            if crashed or not controls["passed"]:
                failure = "preflight check failed (results kept)"
        else:
            crashed = execute(tasks(cp, out, deadline), out, cp["resources"]["workers"])
            summary = analyze(out)
            problems = [f"{len(crashed)} task(s) crashed"] if crashed else []
            if not summary["gating_controls_passed"]:
                problems.append("gating control failed or missing")
            if (
                summary["returned_arms"] != summary["declared_arms"]
                or summary["incomplete_arms"]
            ):
                problems.append("incomplete arms")
            failure = "; ".join(problems) + " (all results kept)" if problems else None
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        dump(out / "failure.json", {"error": failure})
    r = receipt(out, started, failure, cp)
    print(
        {
            "failure": failure,
            "bytes": r["output_bytes"],
            "wall_seconds": r["wall_seconds"],
        },
        flush=True,
    )
    return 1 if failure or r["output_cap_exceeded"] else 0


# ---------------------------------------------------------------- analysis (frozen rules)
def contexts_of(arms, cp, v1):
    """fidelity-v1's per-context analysis, verbatim rules, for one variant's arms."""
    rows_out = []
    for c in cp["contexts"]:
        compliance, speed = c["compliance"], c["speed_m_s"]
        rows = {
            m: {
                a: arms.get(fidelity.arm_id(compliance, speed, m, a))
                for a in model.protocol()["parameters"]["arms"]
            }
            for m in v1["lattices"]
        }
        valid = {
            m: all(
                x is not None and x["valid_for_declared_transfer"] for x in g.values()
            )
            for m, g in rows.items()
        }
        per_mesh = {m: fidelity.effects(g) for m, g in rows.items() if valid[m]}
        entry = {
            "compliance": compliance,
            "speed_m_s": speed,
            "statuses": {
                fidelity.arm_id(compliance, speed, m, a): (x or {"status": "missing"})[
                    "status"
                ]
                for m, g in rows.items()
                for a, x in g.items()
            },
            "descriptive_series": {
                k: {m: per_mesh[m][k]["value"] for m in per_mesh} for k in v1["effects"]
            },
            "floors_at_finest": {
                k: per_mesh["l64x16"][k]["floor"] for k in v1["effects"]
            }
            if "l64x16" in per_mesh
            else {},
        }
        if all(valid.values()):
            classified = {
                k: fidelity.classify(
                    {m: per_mesh[m][k]["value"] for m in v1["lattices"]},
                    per_mesh["l64x16"][k]["floor"],
                    v1,
                )
                for k in v1["effects"]
            }
            entry |= {
                "assessable": True,
                "effects": classified,
                "decision": fidelity.decide(classified),
            }
        else:
            entry |= {
                "assessable": False,
                "decision": {
                    k: {"decision": "undetermined", "why": ["not_assessable"]}
                    for k in ["bending", "feedback"]
                },
            }
        rows_out.append(entry)
    return rows_out


def determinism(arms, v1):
    rows = {}
    for mesh in v1["lattices"]:
        a, b = (
            arms.get(fidelity.arm_id(chi, 20.0, mesh, "rigid")) for chi in (0.8, 0.2)
        )
        if a is None or b is None or not a.get("flight") or not b.get("flight"):
            rows[mesh] = False
            continue
        rows[mesh] = fidelity.final(a, "CL_on_fixed_source_area") == fidelity.final(
            b, "CL_on_fixed_source_area"
        ) and all(
            a["flight"][d]["range_m"] == b["flight"][d]["range_m"]
            for d in ["main", "half"]
        )
    return rows


def analyze(out):
    out = Path(out)
    cp, v1 = cprotocol(), fidelity.fprotocol()
    arms, lattice_controls = fidelity.load(out / "repaired")
    baseline, _ = fidelity.load(out / "baseline-equivalence")
    path = out / "collocation-controls.json"
    colloc = (
        json.loads(path.read_text())
        if path.exists()
        else {"passed": False, "checks": {}}
    )
    K5 = {
        m: (
            c is not None
            and all(v for k, v in c["checks"].items() if k != "upstream_force")
        )
        for m, c in ((m, lattice_controls.get(m)) for m in v1["lattices"])
    }
    K6 = determinism(arms, v1)
    K7 = fidelity.reproduction({"references": cp["baseline_references"]}, baseline)
    original = out / "controls-original.json"
    gating = {
        **{k: v for k, v in colloc["checks"].items()},
        "K5_coupled_lattice_controls": all(K5.values()),
        "K6_determinism": all(K6.values()),
        "K7_baseline_equivalence": bool(K7) and all(r["within_roundoff"] for r in K7),
        "original_controls": original.exists()
        and json.loads(original.read_text())["passed"],
    }
    gating_passed = set(colloc["checks"]) == set(COLLOCATION_CHECKS) and all(
        gating.values()
    )
    contexts = contexts_of(arms, cp, v1)
    if not gating_passed:
        for c in contexts:
            c["decision"] = {"INVALID": [k for k, v in gating.items() if not v]}
    summary = {
        "schema": "frontier.aeroelastic.collocation-results/1",
        "variant": "repaired (diagnostic collocation-repair/1; not the production solver)",
        "protocol_sha256": digest(CP / "protocol.json"),
        "declared_arms": len(cp["contexts"]) * len(v1["lattices"]) * 3,
        "returned_arms": len(arms),
        "valid_arms": sum(
            bool(x.get("valid_for_declared_transfer")) for x in arms.values()
        ),
        "status_counts": {
            s: sum(x["status"] == s for x in arms.values())
            for s in sorted({x["status"] for x in arms.values()})
        },
        "incomplete_arms": sorted(
            k
            for k, x in arms.items()
            if x["status"].startswith(("not-started", "partial"))
        ),
        "gating_controls": gating,
        "gating_controls_passed": gating_passed,
        "study_valid": gating_passed,
        "K5_per_lattice": K5,
        "upstream_force_reported": {
            m: c["checks"].get("upstream_force") for m, c in lattice_controls.items()
        },
        "K6_per_lattice": K6,
        "K7_baseline_equivalence": K7,
        "contexts": contexts,
        "production_decisions": "unchanged: fidelity-v1 (all undetermined)",
        "scope": cp["scope"],
        "biological_success_probability": None,
    }
    dump(out / "summary.json", summary)
    return summary


def compare(out):
    """Paired repaired - baseline per context, effect and lattice, against the pinned fidelity-v1 return."""
    out = Path(out)
    cp = cprotocol()
    base = cp["variants"]["baseline"]
    if (
        digest(Path(base["fidelity_v1_return"]) / "collection_receipt.json")
        != base["fidelity_v1_collection_receipt_sha256"]
    ):
        raise ValueError("fidelity-v1 return changed")
    baseline = json.loads(
        (Path(base["fidelity_v1_return"]) / "science/summary.json").read_text()
    )
    repaired = json.loads((out / "summary.json").read_text())
    rows = []
    for rc in repaired["contexts"]:
        bc = next(
            c
            for c in baseline["contexts"]
            if (c["compliance"], c["speed_m_s"]) == (rc["compliance"], rc["speed_m_s"])
        )
        effects = {}
        for key, series in rc["descriptive_series"].items():
            b = bc["descriptive_series"][key]
            effects[key] = {
                m: {
                    "baseline": b[m],
                    "repaired": v,
                    "difference": v - b[m],
                    "relative": (v - b[m]) / abs(b[m]) if b[m] else None,
                }
                for m, v in series.items()
            }
        rows.append(
            {
                "compliance": rc["compliance"],
                "speed_m_s": rc["speed_m_s"],
                "effects": effects,
                "triples": {
                    k: {
                        "baseline": {
                            t: x["behaviour"]
                            for t, x in bc["effects"][k]["triples"].items()
                        },
                        "repaired": {
                            t: x["behaviour"]
                            for t, x in rc["effects"][k]["triples"].items()
                        }
                        if rc.get("effects")
                        else None,
                    }
                    for k in bc["effects"]
                },
                "statuses": {
                    k: {
                        "baseline": bc["effects"][k]["status"],
                        "repaired": rc["effects"][k]["status"]
                        if rc.get("effects")
                        else None,
                    }
                    for k in bc["effects"]
                },
                "decisions": {
                    "baseline_production": bc["decision"],
                    "repaired_diagnostic": rc["decision"],
                },
            }
        )
    result = {
        "schema": "frontier.aeroelastic.collocation-paired-comparison/1",
        "baseline": "audited fidelity-v1 return (production collocation)",
        "repaired": "this study's repaired arms (diagnostic variant)",
        "study_valid": repaired["study_valid"],
        "contexts": rows,
    }
    dump(out / "paired-comparison.json", result)
    return result


# ---------------------------------------------------------------- packet
PACKAGE = ["collocation.py"]


def packet_sources():
    return [
        ROOT / "engineering/aeroelastic" / n for n in fidelity.PACKAGE + PACKAGE
    ] + [ROOT / x for x in fidelity.SHARED_SOURCES]


def pack(measured):
    cp = cprotocol()
    source = packet_sources() + [ROOT / x["path"] for x in model.protocol()["inputs"]]
    source += [
        ART / "protocol.json",
        fidelity.FID / "protocol.json",
        CP / "protocol.json",
        CP / "vlm-references.json",
    ]
    source += [ROOT / x["path"] for x in cp["baseline_references"]]
    payload, files = io.BytesIO(), []
    with (
        gzip.GzipFile(fileobj=payload, mode="wb", filename="", mtime=0) as zipped,
        tarfile.open(fileobj=zipped, mode="w") as archive,
    ):
        for path in sorted(set(source)):
            raw = path.read_bytes()
            info = tarfile.TarInfo(str(path.relative_to(ROOT)))
            info.size, info.mode = len(raw), 0o644
            archive.addfile(info, io.BytesIO(raw))
            files.append(
                {
                    "path": info.name,
                    "sha256": sha256(raw).hexdigest(),
                    "bytes": len(raw),
                }
            )
    archive_path = CP / "collocation-cpu-packet.tar.gz"
    archive_path.write_bytes(payload.getvalue())
    manifest = {
        "schema": "frontier.aeroelastic.collocation-cpu-packet/1",
        "admission_condition": cp["status"],
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "archive_path": str(archive_path.relative_to(ROOT)),
        "archive_sha256": digest(archive_path),
        "archive_bytes": archive_path.stat().st_size,
        "entry_argv": [
            "python",
            "-m",
            "engineering.aeroelastic.collocation",
            "run",
            "--out",
            "output",
        ],
        "requirements": "engineering/aeroelastic/requirements.txt",
        "environment": {
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
        },
        "resources": cp["resources"],
        "runtime_basis": cp["runtime_basis"],
        "local_preflight": json.loads(Path(measured).read_text()),
        "files": files,
        "outputs": [
            "output/controls-original.json",
            "output/collocation-controls.json",
            "output/repaired/{arms,progress,lattice-controls}/...",
            "output/baseline-equivalence/{arms,progress}/...",
            "output/summary.json",
            "output/receipt.json",
            "output/failure.json and output/task-failures.json if any",
        ],
        "input_network_required": False,
        "no_credentials_or_model_inference": True,
    }
    dump(CP / "packet.json", manifest)
    print(
        {k: manifest[k] for k in ["source_commit", "archive_sha256", "archive_bytes"]}
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["run", "preflight", "analyze", "compare", "pack"]
    )
    parser.add_argument("--out", type=Path)
    parser.add_argument("--measured", type=Path, help="local preflight.json for pack")
    args = parser.parse_args()
    if args.command == "pack":
        pack(args.measured)
    elif args.command == "analyze":
        analyze(args.out)
    elif args.command == "compare":
        compare(args.out)
    else:
        raise SystemExit(main_run(args.out, preflight=args.command == "preflight"))
