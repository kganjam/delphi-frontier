"""Units and dimensional analysis for the swarm: parse quantities, propagate them, refuse what does not balance.

    from swarm_units import Q, check_equation, DimensionError
    Q("3.5 mm") * Q("2 N/m")          # a quantity in SI with its dimension
    (Q("1 N") / Q("2 m^2")).to("Pa")  # 0.5
    check_equation("rho*U*L/mu = 1", {"rho": "kg/m^3", "U": "m/s", "L": "m", "mu": "Pa*s"})  # balanced
    Q("1 m") + Q("1 s")               # raises DimensionError: the point of the module

What this is: exact-exponent dimensional bookkeeping over the seven SI base dimensions, plus
scale factors for common units. What it is not: it does not know whether an equation is PHYSICALLY right
(dimensional balance is necessary, not sufficient), it does not do uncertainty propagation, and it
refuses affine temperature units (degC, degF) rather than guess an offset. Angles are dimensionless
here, so rad vs deg is a scale, and 'N*m' (torque) and 'J' (energy) are the same dimension by construction.

Shared with library/tools/check_laws.py, which uses Dim and parse_dim from here (one grammar, not two:
the earlier duplicate is how 'M/(L*T)' once came back as M*L*T). Run `python library/swarm_units.py` for
the controls; each check ships with a case it must flag.
"""
from __future__ import annotations

import ast
import math
import re
from fractions import Fraction

BASE = ["M", "L", "T", "Th", "N", "I", "J"]   # mass, length, time, temperature, amount, current, luminous


class DimensionError(ValueError):
    """An operation or equation whose dimensions do not balance."""


class UnitError(ValueError):
    """An unknown or unsupported unit."""


class Dim(dict):
    """Exponents over BASE. Dimensionless is all-zero, not empty."""

    def __init__(self, **kw):
        super().__init__({b: Fraction(0) for b in BASE})
        for k, v in kw.items():
            if k not in BASE:
                raise UnitError(f"unknown base dimension {k!r}")
            self[k] = Fraction(v)

    def _comb(self, o, sign):
        r = Dim()
        for b in BASE:
            r[b] = self[b] + sign * o[b]
        return r

    def __mul__(self, o):
        return self._comb(o, 1)

    def __truediv__(self, o):
        return self._comb(o, -1)

    def __pow__(self, n):
        r = Dim()
        for b in BASE:
            r[b] = self[b] * Fraction(n)
        return r

    def __hash__(self):
        return hash(tuple(self[b] for b in BASE))

    @property
    def dimensionless(self):
        return not any(self.values())

    def __str__(self):
        parts = [f"{b}^{v}" for b, v in self.items() if v]
        return "·".join(parts) if parts else "dimensionless"


def _d(**kw):
    return Dim(**kw)


_LENGTH, _TIME, _MASS = _d(L=1), _d(T=1), _d(M=1)
_FORCE = _MASS * _LENGTH / _TIME ** 2
_PRESSURE = _FORCE / _LENGTH ** 2
_ENERGY = _FORCE * _LENGTH

# name -> (scale to SI as an exact Fraction, Dim). Prefixes are generated below, except kg (SI base).
_PRIMARY = {
    "m": (Fraction(1), _LENGTH), "g": (Fraction(1, 1000), _MASS), "s": (Fraction(1), _TIME),
    "K": (Fraction(1), _d(Th=1)), "mol": (Fraction(1), _d(N=1)), "A": (Fraction(1), _d(I=1)),
    "cd": (Fraction(1), _d(J=1)),
    "N": (Fraction(1), _FORCE), "Pa": (Fraction(1), _PRESSURE), "J": (Fraction(1), _ENERGY),
    "W": (Fraction(1), _ENERGY / _TIME), "Hz": (Fraction(1), _TIME ** -1),
    "L": (Fraction(1, 1000), _LENGTH ** 3),
}
_FIXED = {
    "kg": (Fraction(1), _MASS), "min": (Fraction(60), _TIME), "h": (Fraction(3600), _TIME),
    "bar": (Fraction(100000), _PRESSURE), "atm": (Fraction(101325), _PRESSURE),
    "rad": (Fraction(1), Dim()), "deg": (None, Dim()),            # deg scale is pi/180: handled as float
    "percent": (Fraction(1, 100), Dim()), "1": (Fraction(1), Dim()),
    "g0": (Fraction(980665, 100000), _LENGTH / _TIME ** 2),       # standard gravity, exact by definition
}
_PREFIX = {"p": Fraction(1, 10**12), "n": Fraction(1, 10**9), "u": Fraction(1, 10**6), "µ": Fraction(1, 10**6),
           "m": Fraction(1, 1000), "c": Fraction(1, 100), "k": Fraction(1000), "M": Fraction(10**6),
           "G": Fraction(10**9)}
_REFUSED = {"degC": "affine (offset) units are not supported; convert to K first",
            "degF": "affine (offset) units are not supported; convert to K first",
            "C": "ambiguous (coulomb vs celsius); write A*s or K"}
_PREFIXABLE = {"m", "g", "s", "N", "Pa", "J", "W", "Hz", "L", "A", "mol", "K"}


def _unit_atom(name):
    """-> (scale float, Dim). Longest exact match first, then prefix+primary, so 'mm' is milli-metre and 'min' a minute."""
    if name in _REFUSED:
        raise UnitError(f"{name!r}: {_REFUSED[name]}")
    if name in _FIXED:
        s, d = _FIXED[name]
        return (math.pi / 180.0 if name == "deg" else float(s)), d
    if name in _PRIMARY:
        s, d = _PRIMARY[name]
        return float(s), d
    if len(name) > 1 and name[0] in _PREFIX and name[1:] in _PRIMARY and name[1:] in _PREFIXABLE:
        s, d = _PRIMARY[name[1:]]
        return float(_PREFIX[name[0]] * s), d
    raise UnitError(f"unknown unit {name!r}")


class _UnitParser:
    """Product-of-powers grammar:  term (('*'|'/'|'·'|' ') term)* ,  term = atom ('^'|'**' int|frac)? | '(' expr ')' ^?.

    One grammar for unit strings ('kg*m/s^2', 'N m', 'M/(L*T)') and for dimension strings; `atom` is injected.
    '/' binds to the NEXT term only, and a parenthesised group is a single term, so 'M/(L*T)' is M / (L*T).
    Juxtaposition is multiplication ('N m'); a '/' followed by a group divides by the whole group.
    """

    TOK = re.compile(r"\s*(\*\*|[A-Za-zµ_][A-Za-z_0-9µ]*|-?\d+(?:\.\d+)?(?:/\d+)?|[*/()^·])")

    def __init__(self, text, atom, text_for_errors=None):
        self.atom, self.src = atom, text_for_errors or text
        self.toks, pos = [], 0
        text = text.strip()
        while pos < len(text):
            m = self.TOK.match(text, pos)
            if not m:
                raise UnitError(f"cannot parse {self.src!r} at {text[pos:pos + 8]!r}")
            self.toks.append(m.group(1))
            pos = m.end()
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def parse(self):
        v = self.expr()
        if self.peek() is not None:
            raise UnitError(f"unexpected {self.peek()!r} in {self.src!r}")
        return v

    def expr(self):
        s, d = self.term()
        while self.peek() not in (None, ")"):
            op = self.peek()
            if op in ("*", "·"):
                self.i += 1
                s2, d2 = self.term()
                s, d = s * s2, d * d2
            elif op == "/":
                self.i += 1
                s2, d2 = self.term()
                s, d = s / s2, d / d2
            else:                                   # juxtaposition
                s2, d2 = self.term()
                s, d = s * s2, d * d2
        return s, d

    def term(self):
        t = self.peek()
        if t is None:
            raise UnitError(f"empty term in {self.src!r}")
        self.i += 1
        if t == "(":
            s, d = self.expr()
            if self.peek() != ")":
                raise UnitError(f"unbalanced parentheses in {self.src!r}")
            self.i += 1
        elif re.fullmatch(r"-?\d+(?:\.\d+)?(?:/\d+)?", t):
            if t != "1":
                raise UnitError(f"only the number 1 may appear in a unit string, got {t!r} in {self.src!r}")
            s, d = 1.0, Dim()
        else:
            s, d = self.atom(t)
        if self.peek() in ("^", "**"):
            self.i += 1
            e = self.peek()
            if e is None or not re.fullmatch(r"-?\d+(?:\.\d+)?(?:/\d+)?", e):
                raise UnitError(f"bad exponent in {self.src!r}")
            self.i += 1
            ex = Fraction(e)
            s, d = s ** float(ex), d ** ex
        return s, d


def parse_unit(text):
    """Unit expression -> (scale to SI, Dim)."""
    text = str(text).strip()
    if text in ("", "1", "-", "dimensionless"):
        return 1.0, Dim()
    return _UnitParser(text, _unit_atom).parse()


def parse_dim(expr):
    """Dimension string over the base letters (M, L, T, Th/K/Theta, N, I, J), e.g. 'M/(L*T)', 'L^2/T', '1'."""
    expr = str(expr).strip()
    if expr in ("1", "", "dimensionless", "-"):
        return Dim()

    def base(tok):
        b = "Th" if tok in ("Th", "K", "Theta") else tok
        if b not in BASE:
            raise ValueError(f"unknown base dimension {tok!r} in {expr!r}")
        d = Dim()
        d[b] = Fraction(1)
        return 1.0, d

    return _UnitParser(expr, base).parse()[1]


class Quantity:
    """A value in SI with a Dim. Addition, subtraction and comparison need equal dimensions; everything else propagates."""

    __slots__ = ("value", "dim")

    def __init__(self, value, dim=None):
        if isinstance(value, str):
            q = parse_quantity(value)
            value, dim = q.value, q.dim
        self.value, self.dim = float(value), (dim if dim is not None else Dim())

    def _need_same(self, o, op):
        o = _as_q(o)
        if self.dim != o.dim:
            raise DimensionError(f"cannot {op}: [{self.dim}] vs [{o.dim}]")
        return o

    def __add__(self, o):
        o = self._need_same(o, "add")
        return Quantity(self.value + o.value, self.dim)

    __radd__ = __add__

    def __sub__(self, o):
        o = self._need_same(o, "subtract")
        return Quantity(self.value - o.value, self.dim)

    def __rsub__(self, o):
        return _as_q(o).__sub__(self)

    def __neg__(self):
        return Quantity(-self.value, self.dim)

    def __abs__(self):
        return Quantity(abs(self.value), self.dim)

    def __mul__(self, o):
        o = _as_q(o)
        return Quantity(self.value * o.value, self.dim * o.dim)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _as_q(o)
        return Quantity(self.value / o.value, self.dim / o.dim)

    def __rtruediv__(self, o):
        return _as_q(o).__truediv__(self)

    def __pow__(self, n):
        if isinstance(n, Quantity):
            if not n.dim.dimensionless:
                raise DimensionError(f"exponent must be dimensionless, got [{n.dim}]")
            n = n.value
        n = Fraction(n).limit_denominator(1000) if not isinstance(n, Fraction) else n
        return Quantity(self.value ** float(n), self.dim ** n)

    def sqrt(self):
        return self ** Fraction(1, 2)

    def _cmp(self, o, f):
        o = self._need_same(o, "compare")
        return f(self.value, o.value)

    def __lt__(self, o):
        return self._cmp(o, lambda a, b: a < b)

    def __le__(self, o):
        return self._cmp(o, lambda a, b: a <= b)

    def __gt__(self, o):
        return self._cmp(o, lambda a, b: a > b)

    def __ge__(self, o):
        return self._cmp(o, lambda a, b: a >= b)

    def isclose(self, o, rel=1e-9):
        o = self._need_same(o, "compare")
        return math.isclose(self.value, o.value, rel_tol=rel, abs_tol=0.0)

    def to(self, unit):
        """Value expressed in `unit`; refuses a unit of another dimension."""
        s, d = parse_unit(unit)
        if d != self.dim:
            raise DimensionError(f"cannot convert [{self.dim}] to {unit!r} [{d}]")
        return self.value / s

    def __repr__(self):
        return f"Quantity({self.value!r} SI, [{self.dim}])"


def _as_q(x):
    if isinstance(x, Quantity):
        return x
    if isinstance(x, (int, float, Fraction)):
        return Quantity(float(x), Dim())
    raise TypeError(f"not a quantity or number: {x!r}")


_NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def parse_quantity(text):
    """'3.5 mm', '9.80665 m/s^2', '1e-6 N*m^2', '12' (dimensionless) -> Quantity in SI. A bare unit ('mm') means 1 mm."""
    t = str(text).strip()
    m = re.match(rf"^({_NUM})\s*(.*)$", t)
    if m:
        num, unit = float(m.group(1)), m.group(2).strip()
    else:
        num, unit = 1.0, t
    s, d = parse_unit(unit) if unit else (1.0, Dim())
    return Quantity(num * s, d)


Q = Quantity

_FUNCS_DIMENSIONLESS = {"exp": math.exp, "log": math.log, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                        "tanh": math.tanh, "atan": math.atan, "log10": math.log10}


def evaluate(expr, env):
    """Evaluate an arithmetic expression over Quantities in `env` ({name: Quantity or str}). Refuses unbalanced +/-,
    a non-literal or dimensioned exponent, and a transcendental function of a dimensioned argument."""
    env = {k: (v if isinstance(v, Quantity) else parse_quantity(v)) for k, v in env.items()}

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return Quantity(float(n.value))
        if isinstance(n, ast.Name):
            if n.id not in env:
                raise UnitError(f"symbol {n.id!r} has no declared dimension")
            return env[n.id]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            if isinstance(n.op, ast.Pow):
                base = ev(n.left)
                ex = ev(n.right)
                if not ex.dim.dimensionless:
                    raise DimensionError(f"exponent must be dimensionless, got [{ex.dim}]")
                if not base.dim.dimensionless and not isinstance(n.right, (ast.Constant, ast.UnaryOp)):
                    raise DimensionError("a dimensioned base needs a literal exponent (the result's dimension depends on it)")
                return base ** ex.value if base.dim.dimensionless else base ** Fraction(ex.value).limit_denominator(1000)
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            if isinstance(n.op, ast.Mult):
                return a * b
            if isinstance(n.op, ast.Div):
                return a / b
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and len(n.args) == 1 and not n.keywords:
            v = ev(n.args[0])
            if n.func.id == "sqrt":
                return v.sqrt()
            if n.func.id == "abs":
                return abs(v)
            if n.func.id in _FUNCS_DIMENSIONLESS:
                if not v.dim.dimensionless:
                    raise DimensionError(f"{n.func.id}() of a dimensioned argument [{v.dim}]")
                return Quantity(_FUNCS_DIMENSIONLESS[n.func.id](v.value))
        raise UnitError(f"unsupported syntax in {expr!r}: {ast.dump(n)[:60]}")

    return ev(ast.parse(expr.strip(), mode="eval"))


def check_equation(equation, dims):
    """Refuse an equation 'lhs = rhs' whose sides differ in dimension, or any side with an unbalanced sum.

    `dims` maps each symbol to a unit or dimension string ('kg/m^3' or 'M/L^3'). Numbers are dimensionless, so
    'rho*U*L/mu = 1' checks Reynolds. Returns the common Dim; raises DimensionError otherwise."""
    if equation.count("=") != 1 or "==" in equation:
        raise UnitError("write exactly one '=' in an equation")
    env = {}
    for k, v in dims.items():
        try:
            env[k] = Quantity(1.0, parse_unit(v)[1])
        except UnitError:
            env[k] = Quantity(1.0, parse_dim(v))
    lhs, rhs = equation.split("=")
    a, b = evaluate(lhs, env).dim, evaluate(rhs, env).dim
    if a != b:
        raise DimensionError(f"unbalanced: [{a}] = [{b}] in {equation!r}")
    return a


def selftest():
    """Controls; each check has a case it must flag and one it must not. Returns 0 if all behave."""
    ok = True

    def expect(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {label}: got {got!r}, want {want!r}")

    def raises(label, f, exc):
        nonlocal ok
        try:
            f()
        except exc:
            print(f"  [ok] {label}: refused")
            return
        except Exception as e:                     # wrong exception type is also a failure
            ok = False
            print(f"  [FAIL] {label}: raised {type(e).__name__}, want {exc.__name__}")
            return
        ok = False
        print(f"  [FAIL] {label}: NOT refused")

    expect("M/(L*T) is a viscosity (the old M*L*T bug)", str(parse_dim("M/(L*T)")), "M^1·L^-1·T^-1")
    expect("kg/(m*s) equals Pa*s", parse_unit("kg/(m*s)")[1] == parse_unit("Pa*s")[1], True)
    expect("N = kg*m/s^2", parse_unit("N")[1] == parse_unit("kg*m/s^2")[1], True)
    expect("3.5 mm in m", round(Q("3.5 mm").to("m"), 12), 0.0035)
    expect("mm is milli-metre, min is a minute", (parse_unit("mm")[0], parse_unit("min")[0]), (0.001, 60.0))
    expect("1 g is 1e-3 kg", Q("1 g").to("kg"), 0.001)
    expect("(1 N)/(2 m^2) -> 0.5 Pa", (Q("1 N") / Q("2 m^2")).to("Pa"), 0.5)
    expect("EI in N*m^2 times 1/m^4 stays force/length^2", str((Q("1e-6 N*m^2") / Q("1 m^4")).dim == _PRESSURE), "True")
    expect("sqrt(m^2/s^2) is a speed", (Q("9 m^2/s^2").sqrt()).to("m/s"), 3.0)
    expect("torque and energy share a dimension", Q("2 N*m").dim == Q("2 J").dim, True)
    expect("Reynolds balances", str(check_equation("rho*U*L/mu = 1",
                                                   {"rho": "kg/m^3", "U": "m/s", "L": "m", "mu": "Pa*s"})), "dimensionless")
    expect("tip deflection q L^4/(8 EI) is a length", check_equation(
        "w = q*L**4/(8*EI)", {"w": "m", "q": "N/m", "L": "m", "EI": "N*m^2"}) == parse_dim("L"), True)
    expect("evaluate gives the numbers too", round(evaluate("q*L**4/(8*EI)",
          {"q": "0.153125 N/m", "L": "0.15 m", "EI": "1e-3 N*m^2"}).to("m"), 9), round(0.153125 * 0.15 ** 4 / 8e-3, 9))

    # THE CASES IT MUST FLAG
    raises("m + s", lambda: Q("1 m") + Q("1 s"), DimensionError)
    raises("N compared with Pa", lambda: Q("1 N") < Q("1 Pa"), DimensionError)
    raises("convert m to s", lambda: Q("1 m").to("s"), DimensionError)
    raises("wrong Reynolds (multiplying mu)", lambda: check_equation(
        "rho*U*L*mu = 1", {"rho": "kg/m^3", "U": "m/s", "L": "m", "mu": "Pa*s"}), DimensionError)
    raises("deflection with L^3 (a classic slip)", lambda: check_equation(
        "w = q*L**3/(8*EI)", {"w": "m", "q": "N/m", "L": "m", "EI": "N*m^2"}), DimensionError)
    raises("unbalanced sum inside a side", lambda: check_equation(
        "x = a + b", {"x": "m", "a": "m", "b": "s"}), DimensionError)
    raises("exp of a dimensioned argument", lambda: evaluate("exp(L)", {"L": "1 m"}), DimensionError)
    raises("dimensioned exponent", lambda: evaluate("L**T", {"L": "1 m", "T": "1 s"}), DimensionError)
    raises("degC refused, not guessed", lambda: parse_unit("degC"), UnitError)
    raises("unknown unit", lambda: parse_unit("furlong"), UnitError)
    raises("undeclared symbol", lambda: check_equation("a = b", {"a": "m"}), UnitError)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(selftest())
