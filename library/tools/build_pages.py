#!/usr/bin/env python3
"""Render law entries to MyST Markdown pages.

The point of this script is a single-source rule. An equation exists in exactly ONE place -- the
`latex` field of the law's YAML -- and every renderer reads it from there: this MyST build for the
standalone library, and the site's KaTeX renderer for the live pages. Writing the equation a second
time in prose is how two copies drift apart and then agree with each other while both are wrong.

Pages are generated, so they are never hand-edited. The YAML is the source; `myst build` is the
renderer; this is the join between them.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml")

HERE = Path(__file__).resolve().parent
LAWS = HERE.parent / "laws"
PAGES = HERE.parent / "pages"
MYST = HERE.parent / "myst.yml"


def fmt_interval(c: dict) -> str:
    v, iv = c.get("value"), c.get("interval")
    s = "unknown" if v is None else f"{v:g}" if isinstance(v, (int, float)) else str(v)
    if iv and len(iv) == 2:
        s += f" (interval {iv[0]:g} to {iv[1]:g})"
    if c.get("units"):
        s += f" {c['units']}"
    return s


def page(doc: dict) -> str:
    lid = doc["id"]
    out = [f"---\ntitle: {doc['name']}\nlabel: law-{lid}\n---\n"]

    use = doc.get("usability")
    badge = {"constraining": "**Constraining** — this law yields a number a design is checked against.",
             "descriptive": "**Descriptive** — this law describes a pattern and does not constrain a design."}
    if use in badge:
        out.append(f":::{{important}}\n{badge[use]}\n:::\n")

    # The equation, from the single source. `latex` if given, else the plain `equation` string.
    tex = doc.get("latex") or doc.get("equation")
    if tex:
        out.append(f"## The law\n\n:::{{math}}\n:label: eq-{lid}\n{tex}\n:::\n")

    syms = doc.get("symbols") or {}
    if syms:
        out.append("### Symbols\n\n| Symbol | Dimension | Units | Meaning |\n|---|---|---|---|")
        for k, m in syms.items():
            m = m or {}
            out.append(f"| `{k}` | {m.get('dimension','?')} | {m.get('units','—')} | {m.get('description','')} |")
        out.append("")

    cons = doc.get("constants") or {}
    if cons:
        out.append("### Measured constants\n\n| Constant | Value | Note |\n|---|---|---|")
        for k, c in cons.items():
            c = c or {}
            out.append(f"| `{k}` | {fmt_interval(c)} | {str(c.get('note','')).strip()} |")
        out.append("")

    if doc.get("mechanism"):
        out.append(f"## Why it holds\n\n{doc['mechanism'].strip()}\n")

    dov = doc.get("domain_of_validity")
    if dov:
        out.append("## Where it holds\n")
        if isinstance(dov, dict):
            for k, v in dov.items():
                out.append(f"- **{k.replace('_',' ')}**: {v}")
        else:
            out.append(str(dov))
        out.append("")

    # The field that makes the library worth having. Rendered as a warning so a reader cannot skim
    # past it on the way to the equation.
    wib = doc.get("where_it_breaks")
    if wib:
        out.append(f":::{{danger}} Where it breaks\n{wib.strip()}\n:::\n")

    ex = doc.get("worked_examples") or []
    if ex:
        out.append("## Worked examples\n")
        for e in ex:
            e = e or {}
            out.append(f"**{e.get('organism','(unnamed)')}**")
            if e.get("computation"):
                out.append(f"\n```\n{e['computation']}\n```")
            for key in ("value", "value_range"):
                if e.get(key) is not None:
                    out.append(f"\n- {key.replace('_',' ')}: `{e[key]}`")
            if e.get("note"):
                out.append(f"\n- {e['note'].strip()}")
            if e.get("evidence"):
                out.append(f"\n- evidence: **{e['evidence']}**")
            out.append("")

    cb = doc.get("contested_by") or []
    if cb:
        out.append(":::{seealso} Contested\n" + "\n".join(f"- {c}" for c in cb) + "\n:::\n")

    src = doc.get("sources") or []
    if src:
        out.append("## Sources\n\n| Citation | Read-level |\n|---|---|")
        for s in src:
            s = s or {}
            out.append(f"| {s.get('citation','?')} | `{s.get('read_level','UNRECORDED')}` |")
        out.append("")

    out.append("\n---\n\n*Generated from "
               f"[`library/laws/{lid}.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/{lid}.yaml). "
               "Do not edit this page; edit the YAML.*\n")
    return "\n".join(out)


def index(docs: list[dict]) -> str:
    out = ["---\ntitle: The law library\n---\n",
           "Biological design laws, each with the conditions where it is measured to hold and — the "
           "field that makes this a library rather than a poster — **where it breaks**.\n",
           "| Law | Usability | Where it breaks |", "|---|---|---|"]
    for d in sorted(docs, key=lambda x: x["id"]):
        wib = (d.get("where_it_breaks") or "").strip().split(".")[0]
        out.append(f"| [{d['name']}](./{d['id']}.md) | `{d.get('usability','?')}` | {wib[:110]} |")
    out.append("\n:::{note}\nEvery page is generated from its YAML entry. The equation is written in "
               "exactly one place and every renderer reads it from there.\n:::\n")
    return "\n".join(out)


def toc(docs: list[dict]) -> str:
    """Rewrite myst.yml's table of contents from the entries that exist.

    A law absent from the toc does not render, and nothing says so -- the build succeeds and the
    page is simply not there. Keeping the toc by hand makes that a matter of remembering. Generating
    it from the same directory listing the pages come from removes the failure mode instead of
    warning about it, which is the house rule for this kind of gap.
    """
    cfg = yaml.safe_load(MYST.read_text())
    cfg["project"]["toc"] = [
        {"file": "pages/index.md"},
        {"title": "Laws",
         "children": [{"file": f"pages/{d['id']}.md"} for d in sorted(docs, key=lambda x: x["id"])]},
    ]
    return yaml.safe_dump(cfg, sort_keys=False, default_flow_style=False, width=100)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if any page is stale")
    a = ap.parse_args()
    PAGES.mkdir(exist_ok=True)
    docs, stale = [], []
    for f in sorted(LAWS.glob("*.yaml")):
        d = yaml.safe_load(f.read_text())
        docs.append(d)
        target = PAGES / f"{d['id']}.md"
        text = page(d)
        if a.check:
            if not target.exists() or target.read_text() != text:
                stale.append(target.name)
        else:
            target.write_text(text)
    idx = PAGES / "index.md"
    itext = index(docs)
    mtext = toc(docs)
    if a.check:
        if not idx.exists() or idx.read_text() != itext:
            stale.append("index.md")
        if MYST.read_text() != mtext:
            stale.append("myst.yml")
        print(f'{{"stale": {stale}}}')
        return 1 if stale else 0
    idx.write_text(itext)
    MYST.write_text(mtext)
    print(f"wrote {len(docs)} law pages + index to {PAGES}, and the toc in {MYST.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
