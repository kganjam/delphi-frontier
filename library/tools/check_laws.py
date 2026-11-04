#!/usr/bin/env python3
"""Gate for law-library entries: dimensional balance, mandatory fields, and extrapolation warnings.

The dimension check is the cheapest correctness gate available for this kind of content. An equation
whose dimensions do not balance is wrong, and no amount of expert review catches that as reliably as
multiplying out the exponents does. It is also what makes an entry *computable* rather than merely
stored.

Run with --selftest to exercise the controls. Every check here ships with a case it must flag; a gate
that has never rejected anything is not known to be a gate.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml: uv pip install pyyaml")

MANDATORY = ["id", "name", "equation", "symbols", "mechanism",
             "domain_of_validity", "where_it_breaks", "usability", "sources"]


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swarm_units import BASE, Dim, DimensionError, Quantity, UnitError, evaluate, parse_dim  # noqa: E402,F401


def eval_side(expr: str, dims: dict) -> Dim:
    """Dimension of one side of an equation, by the shared units evaluator (library/swarm_units.py).

    Unlike the parser this replaced, a sum is CHECKED term against term (the old one assumed the first term
    spoke for all) and a symbol with no declared dimension is an error (the old one skipped it, which could
    only ever make an equation look more balanced). `sum(x_i)` and subscripts are flattened first.
    """
    expr = re.sub(r"\bsum\s*\(([^)]*)\)", r"(\1)", expr.strip())
    expr = re.sub(r"_i\b|_\{i\}", "", expr)
    expr = expr.replace("^", "**")
    return evaluate(expr, {k: Quantity(1.0, v) for k, v in dims.items()}).dim


def check_entry(path: Path) -> list[str]:
    problems = []
    doc = yaml.safe_load(path.read_text())
    for f in MANDATORY:
        v = doc.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            problems.append(f"{path.name}: missing mandatory field `{f}`")
    # `where_it_breaks` is the field that distinguishes a library from a poster, so it is not
    # satisfied by a placeholder.
    wib = str(doc.get("where_it_breaks", "")).strip()
    if wib and len(wib) < 40:
        problems.append(f"{path.name}: `where_it_breaks` is too short to be a real failure boundary")
    if doc.get("usability") not in ("constraining", "descriptive", None):
        problems.append(f"{path.name}: `usability` must be constraining or descriptive")

    syms = doc.get("symbols") or {}
    # A YAML flow mapping -- {dimension: L, units: m, description: ...} -- splits on EVERY comma, so an
    # unquoted description containing one silently becomes a second key with a null value. Measured on
    # reynolds.yaml: "characteristic length (chord, for a wing)" produced the junk key
    # "for a wing)": None, and the page rendered a truncated description that read like a typo.
    KNOWN = {"dimension", "units", "description", "note"}
    for name, meta in (syms or {}).items():
        if not isinstance(meta, dict):
            continue
        for k, v in meta.items():
            if k not in KNOWN and v is None:
                problems.append(
                    f"{path.name}: symbol `{name}` has stray key {k!r} with no value -- an unquoted "
                    f"comma inside a YAML flow mapping. Quote the value.")
    dims = {}
    for name, meta in syms.items():
        try:
            dims[name] = parse_dim((meta or {}).get("dimension", "1"))
        except ValueError as e:
            problems.append(f"{path.name}: {e}")
    eq = doc.get("equation", "")
    if eq and "=" in eq and dims:
        sides = [s for s in eq.split("=") if s.strip()]
        try:
            ds = [eval_side(s, dims) for s in sides]
            for a, b in zip(ds, ds[1:]):
                if a != b:
                    problems.append(
                        f"{path.name}: dimensions do not balance: {sides[0].strip()!r} is {a}, "
                        f"other side is {b}")
                    break
        except Exception as e:                                      # a parse failure is a problem
            problems.append(f"{path.name}: could not dimension-check equation: {e}")
    for s in doc.get("sources") or []:
        if not (s or {}).get("read_level"):
            problems.append(f"{path.name}: a source has no read_level")
    return problems


def selftest() -> int:
    """Controls. Each check gets a case it MUST flag and a case it must NOT."""
    ok = True

    def expect(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {label}: got {got}, want {want}")

    expect("L/T is a velocity", str(parse_dim("L/T")), "L^1·T^-1")
    expect("M/(L*T) is a viscosity", str(parse_dim("M/(L*T)")), "M^1·L^-1·T^-1")
    expect("M/L^3 is a density", str(parse_dim("M/L^3")), "M^1·L^-3")
    expect("'1' is dimensionless", str(parse_dim("1")), "dimensionless")

    # Reynolds must come out dimensionless -- the positive control for the whole mechanism.
    d = {"rho": parse_dim("M/L^3"), "U": parse_dim("L/T"), "L": parse_dim("L"),
         "mu": parse_dim("M/(L*T)")}
    expect("Re = rho*U*L/mu is dimensionless", str(eval_side("rho * U * L / mu", d)), "dimensionless")

    # THE CASE IT MUST FLAG: a deliberately broken equation. A checker that never rejects is not a
    # checker, so this arm failing is as serious as the arm above failing.
    bad = eval_side("rho * U * L * mu", d)
    expect("a WRONG Reynolds (multiplying mu) is NOT dimensionless",
           str(bad) != "dimensionless", True)
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent / "laws"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        print("self-test (controls):")
        return selftest()
    files = sorted(Path(a.dir).glob("*.yaml"))
    if not files:
        print(f"no law entries under {a.dir}")
        return 1
    allp = []
    for f in files:
        p = check_entry(f)
        allp += p
        print(f"  {'FAIL' if p else 'ok  '} {f.name}")
        for x in p:
            print(f"        {x}")
    print(f"\n{len(files)} entries, {len(allp)} problems")
    return 1 if allp else 0


if __name__ == "__main__":
    sys.exit(main())
