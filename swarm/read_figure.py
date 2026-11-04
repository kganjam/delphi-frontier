#!/usr/bin/env python3
"""Read a number out of a published FIGURE, as a measurement with replicates rather than a glance.

WHY THIS EXISTS. Claim 493 recorded that S5 -- how much fin enlargement a real kcnk5b gain of
function achieves -- CANNOT be settled from PMC full text, because the magnitudes live in figures
and the text extraction drops them. It recommended "the figures themselves". This is that, and
it is the blocking number for S902: S901 now puts the requirement at 4.4x lifting AREA for the
2 cm threshold and 17.4x for lift to equal weight, and Jiang 2024 Fig 2C reports pectoral fin BUD
AREA normalised to eye area, which is the same unit.

A FIGURE READ IS A MEASUREMENT AND IT HAS AN ERROR. One model reading a plot once is a point
estimate with no error bar, which is exactly the failure this repo keeps recording. So the same
crop is read N times independently and the SPREAD ACROSS READS is reported as the uncertainty --
the same move as using four wild-type seeds to get a pLDDT noise floor.

THREE CONTROLS, because a reader that hallucinates plausible numbers looks exactly like one that
reads:
  axis   -- the y-axis bounds are PRINTED on the image and independently checkable
  pvalue -- one significance annotation is PRINTED and independently checkable
  absent -- a group that is NOT in the figure must come back absent, not invented

A read that fails `axis` or invents `absent` is discarded before its data values are used.

Usage:  python3 read_figure.py IMAGE.png --reads 6 [--write OUT.json]
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, "/home/ubuntu/Orchestra")
from orchestra import api_credits  # noqa: E402

TENANTS = ["api_outlook2", "api_outlook1", "api_outlook", "api_gmail"]   # api_allen EXCLUDED
GROUPS = ["AB", "GFP", "KC5", "KC10"]
TIMES = ["32", "48", "56"]

ASK = """This is panel C of a figure from a published zebrafish paper. Read it as carefully as an
analyst extracting data for re-use.

The plot shows "Bud Area/Eye Area Ratio" for four groups (AB, GFP, KC5, KC10) at three timepoints
(32 hpf, 48 hpf, 56 hpf). Each group has scattered black dots and a horizontal RED bar marking the
mean.

Report ONLY what you can see. If something is not in the image, write "absent" -- do not estimate
it from context and do not infer it from the other groups.

Reply in EXACTLY this form, one item per line, nothing else:
AXIS_MIN: <the smallest number printed on the y axis>
AXIS_MAX: <the largest number printed on the y axis>
PVALUE_AB_KC5_32: <the significance annotation printed for AB vs KC5 at 32 hpf, verbatim>
KC20_56: <the red mean bar value for a group labelled KC20 at 56 hpf, or "absent">
MEAN_AB_32: <value of the red bar>
MEAN_GFP_32: <value>
MEAN_KC5_32: <value>
MEAN_KC10_32: <value>
MEAN_AB_48: <value>
MEAN_GFP_48: <value>
MEAN_KC5_48: <value>
MEAN_KC10_48: <value>
MEAN_AB_56: <value>
MEAN_GFP_56: <value>
MEAN_KC5_56: <value>
MEAN_KC10_56: <value>
"""


def ask_once(tenant: str, img_b64: str, model: str, ask: str = "") -> tuple[dict, float]:
    content = [
        {"type": "image",
         "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
        {"type": "text", "text": ask or ASK},
    ]
    out = api_credits.call(tenant, content, model=model, max_tokens=900,
                           purpose="figure-read", project="zebrafish-flight")
    text = out.get("text") or ""
    fields = {}
    for line in text.splitlines():
        m = re.match(r"\s*([A-Z0-9_]+)\s*:\s*(.+?)\s*$", line)
        if m:
            fields[m.group(1)] = m.group(2)
    return fields, float(out.get("cost_usd") or 0.0)


def num(s: str | None) -> float | None:
    if not s:
        return None
    m = re.search(r"-?\d+\.?\d*", s.replace(",", ""))
    return float(m.group()) if m else None



def generic(a) -> int:
    """Read any figure, with the controls declared on the command line rather than hard-coded.

    The Jiang path above is kept because it carries its own documented controls; this is the
    same method with the panel-specific parts lifted out, so the next figure does not need a
    new script. A read is USABLE only if every --expect matches and every --absent comes back
    absent. Discarding happens BEFORE any data value is averaged.
    """
    img_b64 = base64.standard_b64encode(Path(a.image).read_bytes()).decode()
    ask = Path(a.ask_file).read_text() if a.ask_file else ASK
    keys = [k.strip() for k in (a.values or "").split(",") if k.strip()]
    expects = [e.split("=", 1) for e in a.expect]
    print(f"image {a.image}  {a.reads} reads on {a.model}")
    print(f"controls: {len(expects)} printed-value, {len(a.absent)} must-be-absent\n")

    reads, spend = [], 0.0
    for i in range(a.reads):
        t_ = TENANTS[i % len(TENANTS)]
        try:
            f, c = ask_once(t_, img_b64, a.model, ask)
        except Exception as e:
            print(f"  read {i+1}: FAILED on {t_}: {str(e)[:110]}")
            continue
        spend += c
        bad = []
        for k, v in expects:
            got = f.get(k)
            if got is None or (num(got) != num(v) if num(v) is not None
                               else v.lower() not in got.lower()):
                bad.append(f"{k}={got!r} want {v!r}")
        for k in a.absent:
            got = (f.get(k) or "").strip().lower()
            if not (got.startswith("absent") or got in ("n/a", "none", "not present", "")):
                bad.append(f"{k} INVENTED as {got!r}")
        ok = not bad
        print(f"  read {i+1} on {t_:<13} {'USABLE' if ok else 'DISCARDED'}  ${c:.4f}"
              + ("" if ok else "   " + "; ".join(bad)[:150]))
        if ok:
            reads.append(f)

    if not reads:
        print("\nNO USABLE READ -- every read failed a control, so there is no measurement "
              "here. Reporting nothing is the correct outcome.")
        return 1

    print(f"\n{len(reads)} usable of {a.reads}\n")
    print(f"  {'field':>22} {'mean':>10} {'sd':>9} {'min':>9} {'max':>9}  n")
    out = {}
    for k in keys:
        vals = [num(r.get(k)) for r in reads]
        vals = [v for v in vals if v is not None]
        if not vals:
            print(f"  {k:>22}  (no usable value in any read)")
            continue
        m = statistics.mean(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        out[k] = (m, sd, len(vals))
        print(f"  {k:>22} {m:>10.4f} {sd:>9.4f} {min(vals):>9.3f} {max(vals):>9.3f}  {len(vals)}")
    if len(reads) > 1 and all(v[1] == 0.0 for v in out.values()):
        print("\n  every read agreed EXACTLY. That is not a zero error bar: repeated reads from")
        print("  one model are not independent. Cross-MODEL agreement is the real check.")
    print(f"\n  total spend ${spend:.4f}")
    if a.write:
        Path(a.write).write_text(json.dumps(
            {"image": a.image, "model": a.model, "reads": reads,
             "fields": {k: v for k, v in out.items()}, "spend_usd": spend}, indent=2))
        print(f"  wrote {a.write}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--reads", type=int, default=6)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--write")
    ap.add_argument("--ask-file", help="question text; default is the Jiang Fig 2C preset")
    ap.add_argument("--expect", action="append", default=[],
                    help="KEY=VALUE control: a PRINTED value the read must return. "
                         "Repeatable. A read missing any of these is DISCARDED.")
    ap.add_argument("--absent", action="append", default=[],
                    help="KEY that must come back 'absent'. A read that invents it is "
                         "DISCARDED -- this is the control that catches a confident "
                         "hallucinator, and it is the one people leave out.")
    ap.add_argument("--values", help="comma-separated KEYs to average across reads")
    a = ap.parse_args()

    if a.ask_file or a.values:
        return generic(a)

    img_b64 = base64.standard_b64encode(Path(a.image).read_bytes()).decode()
    print(f"image {a.image}  ({len(img_b64)*3//4} bytes)  {a.reads} independent reads "
          f"on {a.model}\n")

    reads, spend = [], 0.0
    for i in range(a.reads):
        t = TENANTS[i % len(TENANTS)]
        try:
            f, c = ask_once(t, img_b64, a.model)
        except Exception as e:
            print(f"  read {i+1}: FAILED on {t}: {str(e)[:110]}")
            continue
        spend += c
        ok_axis = (num(f.get("AXIS_MIN")) == 0.10 and num(f.get("AXIS_MAX")) == 0.50)
        pv = (f.get("PVALUE_AB_KC5_32") or "").replace(" ", "").lower()
        ok_pv = "0.00001" in pv
        kc20 = (f.get("KC20_56") or "").strip().lower()
        ok_abs = kc20.startswith("absent") or kc20 in ("n/a", "none", "not present")
        verdict = "USABLE" if (ok_axis and ok_abs) else "DISCARDED"
        print(f"  read {i+1} on {t:<13} axis {'ok' if ok_axis else 'BAD'}  "
              f"pvalue {'ok' if ok_pv else 'BAD'}  absent-group {'ok' if ok_abs else 'INVENTED'}"
              f"  -> {verdict}   ${c:.4f}")
        if verdict == "USABLE":
            reads.append(f)

    if not reads:
        print("\nNO USABLE READ. Every read failed a printed-value control, so nothing here is "
              "a measurement. Reporting no number is the correct outcome.")
        return 1

    print(f"\n{len(reads)} usable read(s) of {a.reads}\n")
    print(f"  {'group':>10} {'mean':>8} {'sd':>7} {'min':>7} {'max':>7}   n")
    table = {}
    for tm in TIMES:
        for g in GROUPS:
            vals = [num(r.get(f"MEAN_{g}_{tm}")) for r in reads]
            vals = [v for v in vals if v is not None]
            if not vals:
                continue
            m = statistics.mean(vals)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            table[(g, tm)] = (m, sd, len(vals))
            print(f"  {g+'@'+tm+'hpf':>10} {m:>8.4f} {sd:>7.4f} {min(vals):>7.3f} "
                  f"{max(vals):>7.3f}  {len(vals)}")

    print("\nFOLD CHANGE IN AREA RATIO against the AB wild-type control at each timepoint:")
    best = (0.0, None)
    for tm in TIMES:
        ab = table.get(("AB", tm))
        if not ab:
            continue
        for g in ("KC5", "KC10"):
            v = table.get((g, tm))
            if not v:
                continue
            fold = v[0] / ab[0]
            # propagate the READ spread, which is the only error this method can state
            rel = ((v[1] / v[0]) ** 2 + (ab[1] / ab[0]) ** 2) ** 0.5 if ab[0] and v[0] else 0.0
            print(f"  {g}/AB at {tm} hpf: {fold:.2f}x  +/- {fold*rel:.2f} (read spread only)")
            if fold > best[0]:
                best = (fold, f"{g} at {tm} hpf")

    print(f"\n  LARGEST AREA INCREASE ANY K+ CHANNEL LINE ACHIEVES HERE: "
          f"{best[0]:.2f}x ({best[1]})")
    print(f"  S901 requires 4.4x area for the 2 cm threshold and 17.4x for lift = weight.")
    print(f"  shortfall against 4.4x : {4.4/best[0]:.1f}x")
    print(f"  shortfall against 17.4x: {17.4/best[0]:.1f}x")
    print("\n  SCOPE, and it limits the conclusion: these are EMBRYONIC pectoral fin BUDS at")
    print("  32-56 hpf, normalised to eye area. They are not the adult pectoral fin that would")
    print("  carry a lift load, and a bud-area ratio is not an absolute area. This bounds the")
    print("  embryonic effect of the strongest intervention in this paper; carrying it to the")
    print("  adult fin is a separate question this figure cannot answer.")
    print(f"\n  total spend ${spend:.4f}")

    if a.write:
        Path(a.write).write_text(json.dumps(
            {"image": a.image, "model": a.model, "reads": reads,
             "table": {f"{g}@{t}": v for (g, t), v in table.items()},
             "best_fold": best[0], "best_where": best[1], "spend_usd": spend}, indent=2))
        print(f"  wrote {a.write}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
