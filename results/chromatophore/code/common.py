"""Shared plotting style and parameter bookkeeping for the programmable-skin design space.

Every number that enters a model is declared here or in the study module as a Param,
carrying its own status (sourced / assumed / nondimensional) and its source string.
The index page prints the sourced:assumed ratio, so inflating `sourced` is a lie with
a visible number attached to it. Where a value is measured in a DIFFERENT tissue of the
same animal (squid mantle or funnel muscle standing in for a chromatophore radial
muscle, which nobody has measured) the status is `assumed` and the source says what the
proxy is. A proxy is not a measurement of the thing being modelled.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGSIZE_WIDE = (10.0, 6.2)
DPI = 110


def style():
    plt.rcParams.update(
        {
            "figure.dpi": DPI,
            "savefig.dpi": DPI,
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.labelsize": 9.5,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


# A colour-blind-safe qualitative set (Okabe-Ito).
OKABE = [
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#F0E442",
    "#000000",
]


@dataclass
class Param:
    name: str
    value: float | int | str | list
    units: str
    status: str  # sourced | assumed | nondimensional
    source: str

    def __post_init__(self):
        if self.status not in ("sourced", "assumed", "nondimensional"):
            raise ValueError(f"bad status {self.status!r} for {self.name}")


def param_block(params: list[Param]) -> dict:
    counts = {"sourced": 0, "assumed": 0, "nondimensional": 0}
    for p in params:
        counts[p.status] += 1
    return {
        "parameters": [asdict(p) for p in params],
        "parameter_counts": counts,
        "parameter_note": (
            "`sourced` means the number appears in a paper we read, measured in the "
            "thing being modelled. A value measured in another tissue or another "
            "species is `assumed`, with the proxy named in `source`."
        ),
    }


def _json_safe(o):
    """Replace non-finite floats with None, recursively.

    Python's json writes NaN and Infinity as bare literals. That is NOT valid
    JSON: a browser's JSON.parse refuses the whole document, and ours carried 16
    bare NaNs, which took down every page on the site rather than only its own.
    Python's own json.load accepts them by default, so the defect is invisible to
    a round-trip test written in Python - it has to be checked with
    `parse_constant`. The NaNs are meaningful here (a retraction that never
    completed within the simulation window) and are kept as null, with the
    surrounding record saying what null means.
    """
    import math
    if isinstance(o, float):
        return None if not math.isfinite(o) else o
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_json_safe(v) for v in o]
    return o


def write_result(path: str, obj: dict):
    safe = _json_safe(obj)
    text = json.dumps(safe, indent=1)
    # Positive control on every write: re-parse with the strictness a browser uses.
    def _boom(x):
        raise ValueError(f"non-finite literal {x!r} survived _json_safe")
    json.loads(text, parse_constant=_boom)
    with open(path, "w") as fh:
        fh.write(text)
    print(f"wrote {path}")


def caption_stamp(ax, text):
    ax.text(
        0.0,
        -0.22,
        text,
        transform=ax.transAxes,
        fontsize=7.5,
        color="#444444",
        va="top",
        wrap=True,
    )


def figure_caption(fig, text, width=170, fontsize=7.0, pad_in=0.18):
    """Place a wrapped caption under the axes, reserving exactly the room it needs.

    Captions were previously placed at a fixed y with `va="top"` and a hand-guessed
    `tight_layout(rect=...)`, which clipped the last line whenever the wrap produced
    one more line than the guess allowed - in four figures, each time silently. This
    computes the height from the line count and the figure's own size instead.
    """
    import textwrap

    wrapped = textwrap.fill(text, width=width)
    n_lines = wrapped.count("\n") + 1
    line_in = fontsize * 1.45 / 72.0
    need_in = n_lines * line_in + pad_in
    frac = min(0.45, need_in / fig.get_figheight())
    fig.tight_layout(rect=(0, frac, 1, 1))
    fig.text(0.006, frac - pad_in * 0.45 / fig.get_figheight(), wrapped,
             fontsize=fontsize, color="#3a3a3a", va="top", linespacing=1.45)
    return {"lines": n_lines, "reserved_fraction": frac}
