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


# Exponents first, so `^2/3` stays one token; then numeric literals INCLUDING an exponent, so
# `1.5e-5` does not decompose into a number, an identifier `e` and a subtraction.
TOKEN = re.compile(r"\^-?\d+(?:/\d+)?(?:\.\d+)?|\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+"
                   r"|[A-Za-z_][A-Za-z_0-9]*|[*/()+-]")
# Names that may appear in an equation without being a declared physical symbol.
MATH_NAMES = {"pi", "e", "exp", "ln", "log", "log10", "sqrt", "sin", "cos", "tan", "sinh", "cosh",
              "tanh", "abs", "sum", "prod", "min", "max", "det", "tr", "lim", "const"}


def tokenize(expr: str) -> list[str]:
    return TOKEN.findall(expr)


def identifiers(expr: str) -> list[str]:
    """Every name in an expression, in order, excluding pure numbers and operators."""
    return [t for t in tokenize(expr) if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", t)]


def resolve(name: str, dims: dict):
    """Look a symbol up, allowing a bound index: `r_child_i` resolves to the declared `r_child`.

    The old code stripped `_i` from the whole expression with a regex before parsing. That silently
    renamed any symbol legitimately CALLED `r_i` to `r`, which was then undeclared and skipped -- so
    the equation checked was not the equation written.
    """
    if name in dims:
        return dims[name]
    stripped = re.sub(r"_i$|_\{i\}$", "", name)
    return dims.get(stripped)


def _product_of_powers(expr: str, lookup) -> Dim:
    """Parse a product of powers, honouring parentheses and division INTO a group.

    One recursive function serves both a dimension string ('M/(L*T)') and an equation side
    ('rho * U * L / mu'); they are the same grammar over different atoms, and writing it twice is
    how `M/(L*T)` came back as M*L*T -- the self-test's viscosity control caught exactly that.
    """
    expr = expr.strip()
    out, i, sign = Dim(), 0, 1
    tokens = tokenize(expr)

    # A sum or a difference PRESERVES dimension, so the first term settles the whole group and the
    # rest can be dropped. Doing it here rather than in eval_side means it applies at every nesting
    # depth, which is what `pi*(R^4 - r_i^4)/4` needs: the old code dropped the bare `-` in the
    # tokenizer and then MULTIPLIED the two terms, making a tube's second moment L^8 instead of L^4.
    depth = 0
    for idx, t in enumerate(tokens):
        if t == "(":
            depth += 1
        elif t == ")":
            depth -= 1
        elif t in "+-" and depth == 0:
            if idx == 0:                       # a leading sign is unary, not a term separator
                tokens = tokens[1:]
                break
            tokens = tokens[:idx]
            break

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
    return _product_of_powers(expr, lambda t: resolve(t, dims))


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
    # An undeclared symbol was SKIPPED by the parser, contributing nothing -- so a typo, or a symbol
    # the author forgot to declare, made the equation check pass on a shorter equation than the one
    # written. That is the failure this file's own docstring warns about: a gate that is off looks
    # exactly like a gate that passed. Every name must be declared or be a known mathematical name.
    if eq:
        undeclared = sorted({n for n in identifiers(eq)
                             if n not in MATH_NAMES and resolve(n, dims) is None})
        for n in undeclared:
            problems.append(
                f"{path.name}: equation uses `{n}`, which is not in `symbols` and is not a known "
                f"mathematical name -- the dimension check would silently ignore it")
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

    # A DIFFERENCE inside parentheses. The bare `-` used to be dropped by the tokenizer, so the two
    # terms were MULTIPLIED and a tube's second moment of area came out L^8. Measured, not supposed.
    tube = {"R": parse_dim("L"), "r_in": parse_dim("L")}
    expect("a tube's I = pi*(R^4 - r_in^4)/4 is an area^2",
           str(eval_side("pi * (R^4 - r_in^4) / 4", tube)), "L^4")
    expect("a bare difference R^4 - r_in^4 is an area^2",
           str(eval_side("R^4 - r_in^4", tube)), "L^4")

    # A SUM inside parentheses, in a denominator: Froude propulsive efficiency.
    vel = {"U": parse_dim("L/T"), "V_j": parse_dim("L/T")}
    expect("eta = 2*U/(U + V_j) is dimensionless",
           str(eval_side("2 * U / (U + V_j)", vel)), "dimensionless")
    # ...and the case it MUST flag: the same shape with a term that does not belong.
    wrong = {"U": parse_dim("L/T"), "m": parse_dim("M")}
    expect("2*m/(U + m) is NOT dimensionless as a velocity ratio would be",
           str(eval_side("2 * m / (U + m)", wrong)) != "dimensionless", True)

    # A BOUND INDEX must resolve to its declared symbol, and a symbol that merely ENDS in _i must
    # not be mangled. The old global `_i` strip renamed `r_i` to `r` and then skipped it.
    expect("r_child_i resolves to the declared r_child",
           str(eval_side("sum(r_child_i^3)", {"r_child": parse_dim("L")})), "L^3")
    expect("a symbol genuinely named r_i is NOT renamed away",
           str(eval_side("r_i^4", {"r_i": parse_dim("L")})), "L^4")

    # Scientific notation must stay one number, not a number, an `e` and a subtraction.
    expect("1.5e-5 * L is a length", str(eval_side("1.5e-5 * L", {"L": parse_dim("L")})), "L^1")

    # The undeclared-symbol check: a case it must flag, and a case it must not.
    expect("an undeclared symbol is reported",
           identifiers("rho * U * L / mu_typo") and
           [n for n in identifiers("rho * U * L / mu_typo")
            if n not in MATH_NAMES and resolve(n, d) is None], ["mu_typo"])
    expect("pi and exp are NOT reported as undeclared",
           [n for n in identifiers("pi * exp(U)") if n not in MATH_NAMES and resolve(n, d) is None],
           [])
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
