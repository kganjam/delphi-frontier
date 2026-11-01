"""Readable state of the returned paired collocation study: paired comparison, numerical error estimates, figures.

Run after audit_collocation passes. Every number is a returned value, a frozen-rule classification the audit
recomputed and agreed with, or simple arithmetic on those; no threshold is new and nothing decides anything the
frozen rules did not. The paired comparison is the frozen collocation.compare, executed on a copy of the native
summary so the returned tree is never written.

    python -m engineering.aeroelastic.collocation_report numbers --raw RAW_RETURN_DIR   # pinned NumPy
    python -m engineering.aeroelastic.collocation_report figures --raw RAW_RETURN_DIR   # needs matplotlib
"""

import argparse
import json
import shutil
import tempfile
import textwrap
from hashlib import sha256
from pathlib import Path

import numpy as np

from . import collocation, fidelity
from .model import dump

CP = collocation.CP
LADDER = ["main", "fine", "l32x8", "l36x9", "l64x16"]
SHOWN = {
    "CL_rigid": "rigid CL",
    "dCL_one_way_minus_rigid": "ΔCL one-way − rigid (bending)",
    "dCL_two_way_minus_one_way": "ΔCL two-way − one-way (feedback)",
    "dRange_one_way_minus_rigid_m": "Δrange one-way − rigid, m",
}
CHORD_FAMILY = ["32x4", "32x6", "32x8", "32x12", "32x16"]
SPAN_FAMILY = ["16x8", "24x8", "32x8", "48x8", "64x8"]


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def summaries(raw):
    cp = collocation.cprotocol()
    base = cp["variants"]["baseline"]
    v1 = Path(base["fidelity_v1_return"]) / "science/summary.json"
    if digest(v1) != base["fidelity_v1_summary_sha256"]:
        raise ValueError("fidelity-v1 summary changed")
    return json.loads((Path(raw) / "science/summary.json").read_text()), json.loads(
        v1.read_text()
    )


def spread(series):
    values = np.array(list(series.values()))
    return (
        float((values.max() - values.min()) / abs(values.mean()))
        if len(values)
        else None
    )


def triple_rows(effect):
    if not effect:
        return None
    return {
        name: {
            k: t.get(k)
            for k in ["behaviour", "p", "extrapolated", "GCI_abs", "GCI_rel"]
        }
        for name, t in effect["triples"].items()
    }


def error_estimates(repaired, baseline):
    """Per context and effect: floors, three-grid GCI where monotone, five-lattice spread, scheme sensitivity."""
    rows = []
    for rc in repaired["contexts"]:
        bc = next(
            c
            for c in baseline["contexts"]
            if (c["compliance"], c["speed_m_s"]) == (rc["compliance"], rc["speed_m_s"])
        )
        effects = {}
        for key, series in rc["descriptive_series"].items():
            r_eff = (rc.get("effects") or {}).get(key)
            b_eff = bc["effects"][key]
            b_series = bc["descriptive_series"][key]
            shared = [m for m in LADDER if m in series]
            difference = {m: series[m] - b_series[m] for m in shared}
            t2 = (triple_rows(r_eff) or {}).get("T2") or {}
            finest = series.get("l64x16")
            effects[key] = {
                "status": {
                    "baseline": b_eff["status"],
                    "repaired": r_eff["status"] if r_eff else "not_assessable",
                },
                "floor_at_finest": {
                    "baseline": b_eff["floor_at_finest"],
                    "repaired": rc["floors_at_finest"].get(key),
                },
                "triples": {
                    "baseline": triple_rows(b_eff),
                    "repaired": triple_rows(r_eff),
                },
                "five_lattice_relative_spread": {
                    "baseline": spread(b_series),
                    "repaired": spread(series),
                    "repaired_lattices": shared,
                },
                "repaired_minus_baseline": difference,
                "repaired_minus_baseline_relative_at_l64x16": difference["l64x16"]
                / abs(b_series["l64x16"])
                if b_series["l64x16"]
                else None,
                "scheme_sensitivity_over_repaired_GCI_T2": abs(difference["l64x16"])
                / t2["GCI_abs"]
                if t2.get("GCI_abs")
                else None,
                "T2_minus_T1.5_extrapolated": (
                    r_eff["triples"]["T2"].get("extrapolated")
                    - r_eff["triples"]["T1.5"].get("extrapolated")
                    if r_eff
                    and None
                    not in (
                        r_eff["triples"]["T2"].get("extrapolated"),
                        r_eff["triples"]["T1.5"].get("extrapolated"),
                    )
                    else None
                ),
                "repaired_l64x16_value": finest,
            }
        margins = None
        if (
            rc["assessable"]
            and "bending" in rc["decision"]
            and "relative" in rc["decision"]["bending"]
        ):
            e = rc["effects"]
            bend, rigid = (
                e["dCL_one_way_minus_rigid"]["triples"]["T2"],
                e["CL_rigid"]["triples"]["T2"],
            )
            fb = e["dCL_two_way_minus_one_way"]["triples"]["T2"]
            lo = (abs(bend["extrapolated"]) - bend["GCI_abs"]) / (
                abs(rigid["extrapolated"]) + rigid["GCI_abs"]
            )
            hi = (abs(bend["extrapolated"]) + bend["GCI_abs"]) / (
                abs(rigid["extrapolated"]) - rigid["GCI_abs"]
            )
            margins = {
                "bending_relative": rc["decision"]["bending"]["relative"],
                "bending_relative_GCI_interval": [lo, hi],
                "bending_threshold": 0.01,
                "bending_relative_per_lattice": {
                    m: abs(rc["descriptive_series"]["dCL_one_way_minus_rigid"][m])
                    / rc["descriptive_series"]["CL_rigid"][m]
                    for m in LADDER
                },
                "feedback_ratio": rc["decision"]["feedback"].get("ratio_to_one_way"),
                "feedback_ratio_GCI_upper": (abs(fb["extrapolated"]) + fb["GCI_abs"])
                / (abs(bend["extrapolated"]) - bend["GCI_abs"]),
                "feedback_threshold": 0.10,
                "note": "GCI intervals are numerical (lattice) error only, from the frozen T2 triple; "
                "they say nothing about model-form error, EI, or real fish",
            }
        rows.append(
            {
                "compliance": rc["compliance"],
                "speed_m_s": rc["speed_m_s"],
                "assessable": {
                    "baseline": bc["assessable"],
                    "repaired": rc["assessable"],
                },
                "decisions": {
                    "baseline_production": bc["decision"],
                    "repaired_diagnostic": rc["decision"],
                },
                "decision_margins_repaired": margins,
                "effects": effects,
            }
        )
    return rows


def numbers(raw):
    raw = Path(raw)
    audit = json.loads((CP / "return-audit-report.json").read_text())
    if not audit["audit_passed"] or audit["raw_return"] != str(raw):
        raise ValueError("run audit_collocation on this return first; it must pass")
    with tempfile.TemporaryDirectory() as scratch:
        shutil.copy(raw / "science/summary.json", Path(scratch) / "summary.json")
        collocation.compare(scratch)
        paired = json.loads((Path(scratch) / "paired-comparison.json").read_text())
    repaired, baseline = summaries(raw)
    result = {
        "schema": "frontier.aeroelastic.collocation-numbers/1",
        "status": "posthoc reading of an audited return; frozen rules, no new threshold, no decision beyond the "
        "frozen ones",
        "inputs": [
            {"path": str(p), "sha256": digest(p)}
            for p in [
                raw / "science/summary.json",
                raw / "science/collocation-controls.json",
                CP / "return-audit-report.json",
            ]
        ],
        "code_sha256": {
            "collocation_report": digest(__file__),
            "collocation_compare": digest(collocation.__file__),
        },
        "study_valid": repaired["study_valid"],
        "paired_comparison": paired,
        "numerical_error_estimates": error_estimates(repaired, baseline),
        "domain_exits": [x for x in audit["arms"] if x.get("domain_exit")],
        "production_decisions": repaired["production_decisions"],
        "scope": repaired["scope"],
        "biological_success_probability": None,
    }
    dump(CP / "paired-comparison.json", result)
    return result


def figures(raw):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    raw = Path(raw)
    repaired, baseline = summaries(raw)
    numbers_ = json.loads((CP / "paired-comparison.json").read_text())
    controls = json.loads((raw / "science/collocation-controls.json").read_text())
    fp = fidelity.fprotocol()
    panels = {m: 4 * np.prod(fidelity.grid(fp, m)) for m in LADDER}
    colours = {"baseline": "#eb6834", "repaired": "#2a78d6"}
    labels = {
        "baseline": "production collocation (fidelity-v1 return)",
        "repaired": "repaired collocation (this return)",
    }
    ink, muted = "#0b0b0b", "#52514e"
    exits = {x["id"] for x in numbers_["domain_exits"]}

    fig, axes = plt.subplots(3, 4, figsize=(18, 12), constrained_layout=True)
    for row, rc in zip(axes, repaired["contexts"], strict=True):
        bc = next(
            c
            for c in baseline["contexts"]
            if (c["compliance"], c["speed_m_s"]) == (rc["compliance"], rc["speed_m_s"])
        )
        context = f"χ {rc['compliance']}, {rc['speed_m_s']:g} m/s"
        for ax, (key, title) in zip(row, SHOWN.items(), strict=True):
            status = {}
            for name, c in [("baseline", bc), ("repaired", rc)]:
                series = c["descriptive_series"][key]
                ms = [m for m in LADDER if m in series]
                ax.plot(
                    [panels[m] for m in ms],
                    [series[m] for m in ms],
                    "-o",
                    lw=2,
                    ms=7,
                    color=colours[name],
                    label=labels[name],
                    mec="white",
                    mew=1.5,
                )
                effect = (c.get("effects") or {}).get(key)
                status[name] = effect["status"] if effect else "not assessable"
                t2 = effect["triples"]["T2"] if effect else None
                if t2 and t2.get("GCI_abs") is not None:
                    ax.errorbar(
                        [panels["l64x16"] * 1.45],
                        [t2["extrapolated"]],
                        yerr=[t2["GCI_abs"]],
                        fmt="D",
                        ms=6,
                        color=colours[name],
                        capsize=4,
                        lw=1.5,
                    )
            missing = [m for m in LADDER if m not in rc["descriptive_series"][key]]
            if missing:
                dead = [
                    f"chi{rc['compliance']}-u{rc['speed_m_s']:g}-{m}" for m in missing
                ]
                assert all(any(x.startswith(d) for x in exits) for d in dead)
                ax.text(
                    0.02,
                    0.04,
                    f"repaired {', '.join(missing)} group excluded: its coupled arms\n"
                    "are model-domain exits (pectoral tip/span 0.1013 > 0.1)",
                    transform=ax.transAxes,
                    fontsize=7,
                    color=ink,
                    va="bottom",
                )
            ax.set_xscale("log")
            ticks = list(panels.values()) + [panels["l64x16"] * 1.45]
            ax.set_xticks(
                ticks,
                [f"{m} ({v})" for m, v in panels.items()] + ["T2 extrap. ± GCI"],
                fontsize=7,
                rotation=90,
                ha="right",
                rotation_mode="anchor",
            )
            ax.minorticks_off()
            ax.margins(x=0.08, y=0.2)
            ax.yaxis.set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.4g}")
            )
            ax.grid(alpha=0.25)
            ax.tick_params(labelsize=8, colors=muted)
            ax.set_title(
                f"{context}: {title}\nnative status: production {status['baseline']}; "
                f"repaired {status['repaired']}",
                fontsize=8.5,
                color=ink,
                loc="left",
            )
        decision = rc["decision"]
        verdict = (
            "not assessable (domain exits)"
            if not rc["assessable"]
            else f"bending {decision['bending']['decision']}, feedback {decision['feedback']['decision']}"
        )
        row[0].set_ylabel(
            f"{context}\nrepaired-variant decision:\n{verdict}", color=ink, fontsize=9
        )
    for ax in axes[-1]:
        ax.set_xlabel("total VLM panels, four fins (lattice)", color=ink)
    axes[0][0].legend(fontsize=8, frameon=False, loc="upper right")
    fig.suptitle(
        f"Paired collocation study: actual values per lattice, frozen fidelity-v1 rules unchanged. "
        f"Repaired {repaired['valid_arms']} of {repaired['declared_arms']} arms valid; study_valid "
        f"{repaired['study_valid']} (all 10 gating controls)\n"
        "Diamonds: frozen T2 Richardson extrapolation ± GCI where the triple is monotone (numerical lattice error "
        "only). Production decisions stay fidelity-v1's (all undetermined).",
        fontsize=10.5,
        color=ink,
    )
    ladder_png = CP / "paired-ladder.png"
    fig.savefig(ladder_png, dpi=110, facecolor="white")
    plt.close(fig)

    computed = controls["computed_CL"]
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
    families = [
        (
            axs[0],
            "F3_four_fins_combined",
            CHORD_FAMILY,
            1,
            "four fins, chordwise panels refined (32 strips)",
        ),
        (
            axs[1],
            "F3_four_fins_combined",
            SPAN_FAMILY,
            0,
            "four fins, span strips refined (8 chordwise)",
        ),
        (
            axs[2],
            "A1_elliptic_AR6_dense",
            ["32x4", "32x8", "32x16"],
            1,
            "elliptic AR 6, chordwise refined",
        ),
    ]
    plateau = controls["chord_plateau_relative_range"]
    for ax, arm, points, axis, title in families:
        for name in ["baseline", "repaired"]:
            x = [int(p.split("x")[axis]) for p in points]
            ax.plot(
                x,
                [computed[name][arm][p] for p in points],
                "-o",
                lw=2,
                ms=7,
                color=colours[name],
                label=labels[name].split(" (")[0],
                mec="white",
                mew=1.5,
            )
        ax.set_xscale("log", base=2)
        ax.set_xticks(x, [str(v) for v in x])
        ax.minorticks_off()
        ax.set_xlabel(("chordwise panels" if axis else "span strips"), color=ink)
        ax.grid(alpha=0.25)
        ax.tick_params(labelsize=8, colors=muted)
        ax.set_title(title, fontsize=9.5, color=ink, loc="left")
    axs[0].set_ylabel("rigid CL, unit fixed-α solve", color=ink)
    axs[0].legend(fontsize=8, frameon=False)
    fig.suptitle(
        "Returned collocation controls (K4c): over 32x4, 32x8 and 32x16 the relative CL range is\n"
        f"fins {plateau['repaired']['fins']:.2g} repaired vs {plateau['baseline']['fins']:.2g} production, "
        f"ellipse {plateau['repaired']['ellipse']:.2g} vs {plateau['baseline']['ellipse']:.2g} "
        "(gate: repaired ≤ 1e-4, production > 1e-3); one-sided mutant (reported, not gating) "
        f"{plateau['one_sided_mutant']['fins']:.3g} / {plateau['one_sided_mutant']['ellipse']:.3g}",
        fontsize=9.5,
        color=ink,
    )
    plateau_png = CP / "collocation-controls.png"
    fig.savefig(plateau_png, dpi=120, facecolor="white")
    plt.close(fig)
    dump(
        CP / "collocation-figures.provenance.json",
        {
            "schema": "frontier.aeroelastic.collocation-figures/1",
            "scope": "Posthoc descriptive plots of actual returned values; statuses and decisions are the native "
            "summaries', recomputed and agreed by the independent audit; no new threshold",
            "inputs": [
                {"path": str(p), "sha256": digest(p)}
                for p in [
                    raw / "science/summary.json",
                    raw / "science/collocation-controls.json",
                    Path(
                        collocation.cprotocol()["variants"]["baseline"][
                            "fidelity_v1_return"
                        ]
                    )
                    / "science/summary.json",
                    CP / "paired-comparison.json",
                ]
            ],
            "code_sha256": digest(__file__),
            "matplotlib": matplotlib.__version__,
            "outputs": [
                {"path": str(p), "sha256": digest(p), "bytes": p.stat().st_size}
                for p in [ladder_png, plateau_png]
            ],
        },
    )
    for line in textwrap.wrap(f"wrote {ladder_png.name}, {plateau_png.name}", 100):
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["numbers", "figures"])
    parser.add_argument("--raw", type=Path, required=True)
    args = parser.parse_args()
    numbers(args.raw) if args.action == "numbers" else figures(args.raw)
