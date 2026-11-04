"""Controls for library/swarm_units.py. Run: pytest --noconftest library/tests/test_swarm_units.py"""
import sys
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LIB))
sys.path.insert(0, str(LIB / "tools"))
import check_laws  # noqa: E402
import swarm_units as u  # noqa: E402


def test_selftest_controls_all_pass():
    assert u.selftest() == 0


def test_conversion_values():
    assert u.Q("3.5 mm").to("m") == pytest.approx(0.0035)
    assert u.Q("2 GPa").to("Pa") == pytest.approx(2e9)
    assert (u.Q("1 N") / u.Q("2 m^2")).to("Pa") == pytest.approx(0.5)
    assert u.Q("180 deg").to("rad") == pytest.approx(3.141592653589793)


@pytest.mark.parametrize("f", [
    lambda: u.Q("1 m") + u.Q("1 s"),
    lambda: u.Q("1 m").to("kg"),
    lambda: u.check_equation("w = q*L**3/(8*EI)", {"w": "m", "q": "N/m", "L": "m", "EI": "N*m^2"}),
    lambda: u.evaluate("log(x)", {"x": "2 m"}),
])
def test_unbalanced_is_refused(f):
    with pytest.raises(u.DimensionError):
        f()


def test_check_laws_flags_a_broken_equation_and_unknown_symbol():
    d = {"rho": u.parse_dim("M/L^3"), "U": u.parse_dim("L/T"), "L": u.parse_dim("L"), "mu": u.parse_dim("M/(L*T)")}
    assert check_laws.eval_side("rho*U*L/mu", d).dimensionless
    assert not check_laws.eval_side("rho*U*L*mu", d).dimensionless
    with pytest.raises(u.UnitError):                    # the old parser skipped an undeclared symbol and passed
        check_laws.eval_side("rho*U*Lx/mu", d)
    with pytest.raises(u.DimensionError):               # the old parser let the first term of a sum speak for all
        check_laws.eval_side("L + U", d)


def test_constant_fractional_exponent_on_dimensioned_base():
    """The syntactic-guard bug found by morphoswarm-ed: d**(2/3) was refused as 'symbolic'."""
    assert u.evaluate("d**(2/3)", {"d": "1 m"}).dim == u.parse_dim("L") ** u.Fraction(2, 3)
    with pytest.raises(u.DimensionError):
        u.evaluate("L**b", {"L": "1 m", "b": "1"})


def test_law_bridge_reads_caret_fraction_as_a_power_not_a_quotient():
    """'d^2/3' written in a law entry is d to the 2/3, not (d^2)/3 (ed's bridge catch; my first bridge got it wrong)."""
    d = {"d": u.parse_dim("L")}
    assert check_laws.eval_side("d^2/3", d) == u.parse_dim("L") ** u.Fraction(2, 3)
    assert check_laws.eval_side("d^2/3", d) != u.parse_dim("L") ** 2
