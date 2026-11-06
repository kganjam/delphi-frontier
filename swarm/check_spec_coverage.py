#!/usr/bin/env python3
"""Which specs does anything actually CHECK?

WHY THIS EXISTS. `swarm/check_specs.py` reports "25 rules: 23 pass, 1 FAIL, 1 UNCHECKED" and
that number has been quoted -- by me, repeatedly -- as the answer to "are you implementing all
the specs". It is not. Its 25 rules cover FOUR specs, the ones in docs/specs/, and the 17
numbered specs in specs/ are mentioned nowhere in it. Reporting coverage of four specs as
coverage of all of them is the same substitution of a measurable proxy for the question asked
that this project found in the quote gate (claim 3186) and in the query prompt (claim 3188).

WHAT IT MEASURES, AND WHAT IT DOES NOT. For each spec file it reports whether any Python under
swarm/ or analysis/ names it, and how many acceptance-style items it contains. A spec that
nothing names is certainly unchecked. A spec that something names is NOT thereby implemented --
a mention is a mention. So the OK column is a necessary condition, never a sufficient one, and
the summary says so rather than letting a reader round it up.

    python3 swarm/check_spec_coverage.py            # report
    python3 swarm/check_spec_coverage.py --control  # must-flag / must-miss cases
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC_DIRS = [ROOT / "specs", ROOT / "docs" / "specs"]
CODE_DIRS = [ROOT / "swarm", ROOT / "analysis"]
#: A numbered item under an Acceptance/Checkable/Gate heading, or a bolded requirement.
ITEM = re.compile(r"^\s*(?:\d+\.|[-*])\s+\S", re.M)
HEAD = re.compile(r"^##+\s*(Acceptance|Checkable|Gate|Requirements)", re.M | re.I)


def code_text() -> str:
    parts = []
    for d in CODE_DIRS:
        if d.is_dir():
            for f in sorted(d.rglob("*.py")):
                try:
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
    return "\n".join(parts)


def spec_files() -> list[pathlib.Path]:
    out = []
    for d in SPEC_DIRS:
        if d.is_dir():
            out += [f for f in sorted(d.glob("SPEC-*.md"))]
    return out


def named_by_code(stem: str, code: str) -> bool:
    """Is this spec named in code? Matches the file stem and the bare SPEC-NNN form."""
    if stem in code:
        return True
    m = re.match(r"(SPEC-[A-Za-z0-9]+)", stem)
    return bool(m and m.group(1) in code)


def control() -> int:
    code = "x = 'SPEC-ASK-artifact-graph' # referenced\n"
    checks = [
        ("a spec named in code is seen", named_by_code("SPEC-ASK-artifact-graph", code) is True),
        ("a spec NOT named is not seen", named_by_code("SPEC-010-launchable-fish-glider",
                                                      code) is False),
        ("the bare SPEC-NNN form counts",
         named_by_code("SPEC-ASK-artifact-graph-extra", code) is True),
        ("acceptance items are counted", len(ITEM.findall("1. a\n2. b\n- c\n")) == 3),
        ("prose is not an item", len(ITEM.findall("just a sentence\n")) == 0),
    ]
    for n, ok in checks:
        print(f"  {'ok  ' if ok else 'FAIL'}  {n}")
    bad = [n for n, ok in checks if not ok]
    print(f"\n  {len(checks) - len(bad)} of {len(checks)} controls pass")
    return 1 if bad else 0


def main() -> int:
    if "--control" in sys.argv:
        return control()
    code = code_text()
    files = spec_files()
    if not files:
        print("  no spec files found -- NOT reporting coverage.")
        return 1
    named = unnamed = 0
    orphan_items = 0
    print(f"\n  {len(files)} spec file(s); checking whether any Python under "
          f"{', '.join(d.name for d in CODE_DIRS)} names each\n")
    print(f"  {'spec':<46}{'named in code':>14}{'acceptance items':>18}")
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        items = len(ITEM.findall(txt)) if HEAD.search(txt) else 0
        hit = named_by_code(f.stem, code)
        named += hit
        unnamed += not hit
        orphan_items += 0 if hit else items
        print(f"  {f.stem[:44]:<46}{('yes' if hit else 'NO'):>14}{items:>18}")
    print(f"\n  named by some checker: {named}    named by nothing: {unnamed}")
    print(f"  acceptance items in specs nothing names: {orphan_items}")
    print("  A spec nothing names is certainly unchecked. A spec something names is NOT")
    print("  thereby implemented -- a mention is a mention. This column is a necessary")
    print("  condition and never a sufficient one.")
    return 0 if unnamed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
