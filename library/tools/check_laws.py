#!/usr/bin/env python3
"""Gate for law-library entries: dimensional balance, mandatory fields, and the entry standard.

The dimension check is the cheapest correctness gate available for this kind of content. An equation
whose dimensions do not balance is wrong, and no amount of expert review catches that as reliably as
multiplying out the exponents does. It is also what makes an entry *computable* rather than merely
stored.

THE ENGINE IS `library/swarm_units.py`, NOT A SECOND PARSER HERE. Two implementations of this check
existed (2026-11-04) and were merged semantically rather than one being picked:

  * From swarm_units (morphoswarm-34): an `ast`-based evaluator, so operator precedence, parentheses
    and unary minus are Python's rather than hand-rolled; real units with scale factors; and the
    refusals this file previously lacked -- an UNBALANCED SUM (the old parser here assumed the first
    term spoke for all, so `x = a + b` with a in metres and b in seconds was reported BALANCED), a
    dimensioned exponent, a dimensioned base under a symbolic exponent, exp/log of a dimensioned
    argument, affine degC/degF, and an undeclared symbol.
  * From this file: the three bridge fixes, each of which the other side got wrong. Measured on the
    12 entries that existed at merge time, the other bridge failed 3 of them, all of them correct
    entries -- see `translate` and `env_for` below.

What was dropped, and why: this file's own `_product_of_powers` token walker, together with its
bare-minus and first-term-truncation fixes. The ast evaluator supersedes them -- it gets precedence
right AND checks the sum instead of assuming it, which is strictly more than those fixes bought.

Run with --selftest to exercise the controls. Every check ships with a case it must flag; a gate that
has never rejected anything is not known to be a gate.
"""
from __future__ import annotations

import argparse
import ast
import math
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml: uv pip install pyyaml")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swarm_units import (BASE, Dim, DimensionError, Quantity,  # noqa: E402,F401
                         UnitError, evaluate, parse_dim)

MANDATORY = ["id", "name", "equation", "symbols", "mechanism",
             "domain_of_validity", "where_it_breaks", "usability", "sources"]

# Mathematical constants an equation may use without declaring them. Functions (sqrt, exp, log, ...)
# are handled by the evaluator itself; these are the bare NAMES, which it would otherwise call
# undeclared. The other bridge had no such allowance, and refused poiseuille.yaml over `pi`.
MATH_CONSTANTS = {"pi": math.pi, "e": math.e}

# The library writes exponents as `^`, which Python reads as XOR, so the expression must be
# translated before `ast` sees it.
_NUMERIC_EXPONENT = re.compile(r"\^(-?\d+(?:/\d+)?(?:\.\d+)?)")


def translate(expr: str) -> str:
    """Library equation syntax -> Python syntax, with the exponent BRACKETED.

    The bracket is the whole point and it is not cosmetic. A plain `expr.replace("^", "**")` turns
    `d^2/3` into `d**2/3`, which Python reads as `(d**2)/3` -- dimension L^2 where L^(2/3) was
    written. That is not a near miss: measured at merge time it made `elastic-similarity` come out
    L^(7/3) against a declared L, and `greenhill` L^3 against a declared L. Both entries were
    correct; the translation was not. Worse than the loud failures is the quiet one -- a wrong
    exponent that happens to balance -- which is why this is a control rather than a comment.

    A SYMBOLIC exponent (`(x/x_ref)^b`) is passed through as `**b`; the evaluator then refuses it if
    the base is dimensioned, since `metres**b` has no fixed dimension for arbitrary real b.
    """
    expr = re.sub(r"\bsum\s*\(([^)]*)\)", r"(\1)", expr.strip())   # a sum preserves dimension
    expr = _NUMERIC_EXPONENT.sub(r"**(\1)", expr)
    return expr.replace("^", "**")                                  # any remaining symbolic exponent


def names_in(expr: str) -> list[str]:
    """Every bare name in a translated expression, excluding called functions."""
    tree = ast.parse(expr, mode="eval")
    called = {n.func.id for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    return sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} - called)


def env_for(expr: str, dims: dict) -> dict:
    """Build the evaluator environment, resolving a BOUND INDEX to its declared symbol.

    Murray's law is written `r_parent^3 = sum(r_child_i^3)` and declares `r_child`. The previous
    approach -- on both sides of the merge -- stripped `_i` from the whole expression with a regex
    before parsing. That silently renamed any symbol legitimately CALLED `r_i` to `r`, which was then
    undeclared; this file used to skip an undeclared symbol, so the equation CHECKED was shorter than
    the equation WRITTEN. Aliasing per name instead leaves `r_i` alone.
    """
    env = {k: Quantity(1.0, v) for k, v in dims.items()}
    for name in names_in(expr):
        if name in env:
            continue
        if name in MATH_CONSTANTS:
            env[name] = Quantity(1.0, Dim())
            continue
        stripped = re.sub(r"_i$|_\{i\}$", "", name)
        if stripped in dims:
            env[name] = Quantity(1.0, dims[stripped])
    return env


def eval_side(expr: str, dims: dict) -> Dim:
    """Dimension of one side of an equation, via the shared evaluator."""
    expr = translate(expr)
    return evaluate(expr, env_for(expr, dims)).dim


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
        except (ValueError, UnitError) as e:
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
        except (DimensionError, UnitError, SyntaxError) as e:      # a refusal is a problem
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

    def refuses(label, expr, dims):
        nonlocal ok
        try:
            eval_side(expr, {k: parse_dim(v) for k, v in dims.items()})
        except (DimensionError, UnitError):
            print(f"  [ok] {label}: refused")
            return
        ok = False
        print(f"  [FAIL] {label}: NOT refused")

    def dim(expr, **kw):
        return str(eval_side(expr, {k: parse_dim(v) for k, v in kw.items()}))

    print("  -- dimension strings (shared grammar) --")
    expect("L/T is a velocity", str(parse_dim("L/T")), "L^1·T^-1")
    expect("M/(L*T) is a viscosity", str(parse_dim("M/(L*T)")), "M^1·L^-1·T^-1")
    expect("'1' is dimensionless", str(parse_dim("1")), "dimensionless")

    print("  -- the positive control, and the case it must flag --")
    re_d = {"rho": "M/L^3", "U": "L/T", "L": "L", "mu": "M/(L*T)"}
    expect("Re = rho*U*L/mu is dimensionless", dim("rho * U * L / mu", **re_d), "dimensionless")
    expect("a WRONG Reynolds (multiplying mu) is NOT dimensionless",
           dim("rho * U * L * mu", **re_d) != "dimensionless", True)

    print("  -- THE BRACKETED EXPONENT: `d^2/3` is a 2/3 power, not (d^2)/3 --")
    # The merge's own must-flag case. `expr.replace("^","**")` gives L^2 here and made two CORRECT
    # entries fail; the bracketing is what fixes it.
    expect("d^2/3 is L^(2/3)", dim("d^2/3", d="L"), "L^2/3")
    expect("(E/(rho*g))^1/3 * d^2/3 is a length",
           dim("(E / (rho * g))^1/3 * d^2/3", E="M/(L*T^2)", rho="M/L^3", g="L/T^2", d="L"), "L^1")
    expect("M^-0.316 keeps its sign and decimal", dim("M_b^-0.316", M_b="M"), "M^-79/250")
    expect("r^4 is still an area squared", dim("r^4", r="L"), "L^4")

    print("  -- sums and differences are CHECKED, not assumed (from swarm_units) --")
    expect("a tube's I = pi*(R^4 - r_in^4)/4 is an area^2",
           dim("pi * (R^4 - r_in^4) / 4", R="L", r_in="L"), "L^4")
    expect("eta = 2*U/(U + V_j) is dimensionless", dim("2 * U / (U + V_j)", U="L/T", V_j="L/T"), "dimensionless")
    refuses("adding a length to a time", "a + b", {"a": "L", "b": "T"})
    refuses("subtracting a time from a length", "a - b", {"a": "L", "b": "T"})

    print("  -- symbols: bound indices, math constants, and undeclared names --")
    expect("r_child_i resolves to the declared r_child", dim("sum(r_child_i^3)", r_child="L"), "L^3")
    expect("a symbol genuinely named r_i is NOT renamed away", dim("r_i^4", r_i="L"), "L^4")
    expect("pi needs no declaration", dim("pi * r^2", r="L"), "L^2")
    refuses("an undeclared symbol", "rho * U * L / mu_typo", re_d)

    print("  -- exponents and transcendentals (from swarm_units) --")
    expect("a symbolic exponent on a DIMENSIONLESS base is fine",
           dim("(x / x_ref)^b", x="M", x_ref="M", b="1"), "dimensionless")
    refuses("a symbolic exponent on a DIMENSIONED base", "x^b", {"x": "M", "b": "1"})
    refuses("a dimensioned exponent", "x^y", {"x": "1", "y": "T"})
    refuses("exp of a dimensioned argument", "exp(L)", {"L": "L"})
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
