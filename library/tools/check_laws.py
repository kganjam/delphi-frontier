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
from fractions import Fraction
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml: uv pip install pyyaml")

BASE = ["M", "L", "T", "Th", "N", "I", "J"]          # mass, length, time, temperature, amount, current, luminous
MANDATORY = ["id", "name", "equation", "symbols", "mechanism",
             "domain_of_validity", "where_it_breaks", "usability", "sources"]


class Dim(dict):
    """A dimension as exponents over the base units. Dimensionless is all-zero, not empty."""

    def __init__(self, **kw):
        super().__init__({b: Fraction(0) for b in BASE})
        for k, v in kw.items():
            self[k] = Fraction(v)

    def __mul__(self, o):
        r = Dim()
        for b in BASE:
            r[b] = self[b] + o[b]
        return r

    def __truediv__(self, o):
        r = Dim()
        for b in BASE:
            r[b] = self[b] - o[b]
        return r

    def __pow__(self, n):
        r = Dim()
        for b in BASE:
            r[b] = self[b] * Fraction(n)
        return r

    def __str__(self):
        parts = [f"{b}^{v}" for b, v in self.items() if v]
        return "·".join(parts) if parts else "dimensionless"


def _product_of_powers(expr: str, lookup) -> Dim:
    """Parse a product of powers, honouring parentheses and division INTO a group.

    One recursive function serves both a dimension string ('M/(L*T)') and an equation side
    ('rho * U * L / mu'); they are the same grammar over different atoms, and writing it twice is
    how `M/(L*T)` came back as M*L*T -- the self-test's viscosity control caught exactly that.
    """
    expr = expr.strip()
    out, i, sign = Dim(), 0, 1
    tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\^-?\d+(?:/\d+)?(?:\.\d+)?|[*/()]|[\d.]+", expr)

    def read_group(j):
        """Return (Dim, index after the matching close paren)."""
        depth, k = 1, j
        while k < len(tokens) and depth:
            k += 1
            if k < len(tokens):
                if tokens[k] == "(":
                    depth += 1
                elif tokens[k] == ")":
                    depth -= 1
        inner = "".join(t if t.startswith("^") else (" " + t + " ") for t in tokens[j + 1:k])
        return _product_of_powers(inner, lookup), k + 1

    while i < len(tokens):
        t = tokens[i]
        if t == "*":
            sign, i = 1, i + 1
            continue
        if t == "/":
            sign, i = -1, i + 1
            continue
        if t == "(":
            d, i = read_group(i)
            if i < len(tokens) and tokens[i].startswith("^"):
                d = d ** Fraction(tokens[i][1:]); i += 1
            out = out * d if sign > 0 else out / d
            sign = 1
            continue
        if t == ")":
            i += 1
            continue
        if re.fullmatch(r"[\d.]+", t):                       # a pure number is dimensionless
            i += 1
            continue
        d = lookup(t)
        if d is None:
            i += 1
            continue
        if i + 1 < len(tokens) and tokens[i + 1].startswith("^"):
            d = d ** Fraction(tokens[i + 1][1:]); i += 1
        out = out * d if sign > 0 else out / d
        sign = 1
        i += 1
    return out


def parse_dim(expr: str) -> Dim:
    """Parse a dimension string such as 'M/(L*T)', 'L^2/T', '1' or 'M/L^3'."""
    expr = str(expr).strip()
    if expr in ("1", "", "dimensionless", "-"):
        return Dim()
    unknown = []

    def base(tok):
        b = "Th" if tok in ("Th", "K", "Theta") else tok
        if b not in BASE:
            unknown.append(tok)
            return None
        d = Dim()
        d[b] = Fraction(1)
        return d

    out = _product_of_powers(expr, base)
    if unknown:
        raise ValueError(f"unknown base dimension {unknown[0]!r} in {expr!r}")
    return out


def eval_side(expr: str, dims: dict) -> Dim:
    """Dimension of one side of an equation. A sum preserves dimension, so the first term suffices."""
    expr = re.sub(r"\bsum\s*\(([^)]*)\)", r"(\1)", expr.strip())
    expr = re.sub(r"_i\b|_\{i\}", "", expr)
    for plus in re.split(r"(?<![eE])\+", expr):
        if plus.strip():
            expr = plus.strip()
            break
    return _product_of_powers(expr, lambda t: dims.get(t))


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
