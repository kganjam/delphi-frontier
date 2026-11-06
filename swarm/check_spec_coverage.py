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
#: THE WHOLE REPOSITORY, not two directories. The first version scanned swarm/ and analysis/
#: only, and reported "16 of 21 specs named by nothing". There are 1,580 Python files outside
#: those two, several of which name a spec directly -- engineering/biodesign_compiler,
#: connectors/biomodels, connectors/bioservices -- and artifacts/genetic-blueprints/ carries its
#: own check.py for SPEC-012. So the figure measured the two directories I happened to look in,
#: which is the "state the domain your search covered" failure in AGENTS.md section 7.
CODE_ROOT = ROOT
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "site-packages"}
#: Every numbered or bulleted line in the spec. COUNTED OVER THE WHOLE FILE, NOT UNDER AN
#: "Acceptance" HEADING, because anchoring on the heading undercounted badly and silently: the
#: first version required a heading STARTING with Acceptance/Checkable/Gate/Requirements, so
#: SPEC-012's "First implementation and acceptance checklist" did not match and its 12 items
#: were reported as 0, as were SPEC-015's 8 and SPEC-017's 27 under "Validation contract
#: attached to a candidate". Three goal-central specs read as having nothing to check.
#:
#: A whole-file count is CRUDER and unbiased: it includes prose bullets that are not acceptance
#: items, so it OVERSTATES what is checkable, where the previous rule understated it. An
#: overstatement in a coverage report is the safer error -- it cannot make an unchecked spec
#: look checked.
ITEM = re.compile(r"^\s*(?:\d+\.|[-*])\s+\S", re.M)


#: THIS FILE IS EXCLUDED FROM ITS OWN SCAN. Measured 2026-11-06, immediately: fixing the item
#: undercount meant naming SPEC-012, SPEC-015 and SPEC-017 in the comment explaining the fix,
#: and the count of specs "named by some checker" rose from 6 to 9 for that reason alone. A
#: checker that mentions a spec marks it covered by itself, which is AGENTS.md section 6b's
#: "a checker that greps for a forbidden string finds it in its own source". The exclusion is
#: by resolved path, so renaming the file cannot reintroduce it.
SELF = pathlib.Path(__file__).resolve()


def code_text() -> str:
    parts = []
    for f in sorted(CODE_ROOT.rglob("*.py")):
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        if f.resolve() == SELF:
            continue
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
        ("listed items are counted", len(ITEM.findall("1. a\n2. b\n- c\n")) == 3),
        ("items count without an Acceptance heading",
         len(ITEM.findall("## First implementation and acceptance checklist\n- a\n- b\n")) == 2),
        ("prose is not an item", len(ITEM.findall("just a sentence\n")) == 0),
        # must-flag: the scan must not read this file, or every spec it discusses counts
        ("this file is excluded from its own scan",
         "SPEC-012-genetic-implementation-blueprints" not in code_text()),
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
    print(f"\n  {len(files)} spec file(s); checking whether "
          f"any Python in the repository names each\n")
    print(f"  {'spec':<46}{'named in code':>14}{'listed items':>18}")
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        items = len(ITEM.findall(txt))
        hit = named_by_code(f.stem, code)
        named += hit
        unnamed += not hit
        orphan_items += 0 if hit else items
        print(f"  {f.stem[:44]:<46}{('yes' if hit else 'NO'):>14}{items:>18}")
    print(f"\n  named by some checker: {named}    named by nothing: {unnamed}")
    print(f"  listed items in specs nothing names: {orphan_items}")
    print("  `listed items` counts every numbered or bulleted line, so it includes prose")
    print("  bullets and OVERSTATES what is checkable. That is the safer error here: it")
    print("  cannot make an unchecked spec look checked.")
    print("  A spec nothing names is certainly unchecked. A spec something names is NOT")
    print("  thereby implemented -- a mention is a mention. This column is a necessary")
    print("  condition and never a sufficient one.")
    return 0 if unnamed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
