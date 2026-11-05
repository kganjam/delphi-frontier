#!/usr/bin/env python3
"""What the taxi ceiling needs is Reynolds number, and no fin allele supplies it.

WHY THIS EXISTS. Claim 519 settled the launch negatively for the MEASURED-BURST route and said
in its own scope that it "does not touch the spring-loaded or taxi routes". Claim 990 then
established that the published allele pair gives the zebrafish a HYPOCERCAL caudal fin -- the
organ Daane 2021 says "facilitates the initial emergence and take-off from the water". So the
taxi route now has its organ, and the question is whether it closes.

It does not, and analysis/taxi_ceiling.py already contains the reason. One fitted constant c6
serves both rows of the project's U_max table, and the rows predict:

    exocoetid, Re ~3e5   U_max/V_to = 1.3-1.5    taxi EXCEEDS take-off speed
    zebrafish,  Re ~1e4  U_max/V_to = 0.58-0.68  taxi cannot reach it

The two rows share f*A_pp/V_to (0.09-0.10). What differs is the lobe drag coefficient:
0.008-0.012 against 0.06-0.08. That is a Reynolds-number difference, not a morphological one.

THE POINT FOR THE DESIGN. Every genetic lever this project has measured changes fin SIZE or fin
PROPORTION. Claim 987: the best allele gives 2.67x lifting area. Claim 990: the pair gives the
flying-fish body plan including the take-off tail. NONE of them changes Reynolds number, which
depends on body length and speed. So the remaining blocker is not genetic, and the only
morphological lever that touches it is BODY SIZE -- which these alleles do not provide.

WHAT THIS FILE WILL NOT DO. It will not pretend the drag-Reynolds relation is known. The project
holds exactly TWO (Re, C_D) points and they come from a table, not from a measurement made here.
Fitting an exponent to two points and then inverting it is an interpolation dressed as a law, so
the size figure below is printed as an ORDER OF MAGNITUDE with its exponent shown, and the
sensitivity to that exponent is printed beside it rather than hidden.
"""
import sys

# analysis/taxi_ceiling.py ROWS, same source: docs/FINDINGS.md U_max table.
FA_LO, FA_HI = 0.09, 0.10          # f * A_pp / V_to, shared by both rows
EXO = {"re": 3.0e5, "cd_lo": 0.008, "cd_hi": 0.012, "u_lo": 1.3, "u_hi": 1.5}
ZEB = {"re": 1.0e4, "cd_lo": 0.06, "cd_hi": 0.08, "u_lo": 0.58, "u_hi": 0.68}
C6_LO, C6_HI = 1.352, 3.333        # fitted to the exocoetid row by taxi_ceiling.py


def u_ratio(fa, cd, c6):
    return fa * (c6 / cd) ** 0.5


def cd_needed(target, fa, c6):
    """Lobe C_D at which U_max/V_to reaches `target`."""
    return c6 / (target / fa) ** 2


def controls_pass() -> tuple[bool, str]:
    """Reproduce BOTH published rows, and a case the formula must distinguish.

    THE PAIRING MATTERS AND THE FIRST VERSION OF THIS CONTROL GOT IT WRONG. c6 is not an
    independent range: taxi_ceiling fits c6_lo from (u_lo, fa_hi, cd_lo) and c6_hi from
    (u_hi, fa_lo, cd_hi). Combining c6_lo with fa_lo and cd_hi is not a reachable corner, and
    doing so produced a sub-unity exocoetid ratio and an abort. The control was right to fail;
    the error was mine, in the corner I built, not in the formula.
    """
    exo_lo = u_ratio(FA_HI, EXO["cd_lo"], C6_LO)
    exo_hi = u_ratio(FA_LO, EXO["cd_hi"], C6_HI)
    if abs(exo_lo - EXO["u_lo"]) > 0.02 or abs(exo_hi - EXO["u_hi"]) > 0.02:
        return False, (f"exocoetid row not reproduced: got {exo_lo:.3f}-{exo_hi:.3f}, "
                       f"stated {EXO['u_lo']}-{EXO['u_hi']}")
    zeb_lo = u_ratio(FA_LO, ZEB["cd_hi"], C6_LO)
    zeb_hi = u_ratio(FA_HI, ZEB["cd_lo"], C6_HI)
    if zeb_hi < ZEB["u_lo"] or zeb_lo > ZEB["u_hi"]:
        return False, f"zebrafish row not bracketed: predicted {zeb_lo:.3f}-{zeb_hi:.3f}"
    # MUST-DISTINGUISH arm, on a reachable corner: give the zebrafish the exocoetid's lobe
    # drag and the ratio must cross 1.0. If it does not, lobe C_D is not what separates the
    # rows and this whole file's thesis is wrong.
    swapped = u_ratio(FA_HI, EXO["cd_lo"], C6_LO)
    if swapped < 1.0:
        return False, (f"exocoetid drag at zebrafish geometry gives {swapped:.3f} < 1; "
                       f"lobe C_D is NOT what separates the rows")
    return True, (f"exocoetid reproduced {exo_lo:.2f}-{exo_hi:.2f} (stated "
                  f"{EXO['u_lo']}-{EXO['u_hi']}); zebrafish bracketed {zeb_lo:.2f}-{zeb_hi:.2f}; "
                  f"swapping in exocoetid drag gives {swapped:.2f} > 1, so lobe C_D is the "
                  f"discriminating variable")


def main() -> int:
    ok, why = controls_pass()
    print("=" * 78)
    print("THE TAXI LEVER IS REYNOLDS NUMBER, NOT FIN GENETICS")
    print("=" * 78)
    print(f"  [{'ok' if ok else 'FAIL'}] controls: {why}")
    if not ok:
        print("\n  ABORTING: the formula does not reproduce the table it is built on.")
        return 2

    print(f"\n  the two rows share f*A_pp/V_to = {FA_LO}-{FA_HI}; only lobe C_D differs")
    print(f"    exocoetid  Re {EXO['re']:.0e}  C_D {EXO['cd_lo']}-{EXO['cd_hi']}"
          f"   U_max/V_to {EXO['u_lo']}-{EXO['u_hi']}")
    print(f"    zebrafish  Re {ZEB['re']:.0e}  C_D {ZEB['cd_lo']}-{ZEB['cd_hi']}"
          f"   U_max/V_to {ZEB['u_lo']}-{ZEB['u_hi']}")

    # WITHIN-CORNER, because the alternative is wrong and I published the wrong one first.
    # For a FIXED (c6, fa), ratio = fa*sqrt(c6/C_D), so reaching 1.0 from r0 needs C_D to fall
    # by exactly 1/r0^2 -- c6 and fa cancel and never need to be paired across corners.
    # Claim 991 instead compared the zebrafish's lowest actual C_D against the highest required
    # one and vice versa, giving 1.8x-7.3x. Those two corners carry different c6 and fa, so the
    # pair is not a reachable comparison. It is the same corner-mixing error the control in
    # controls_pass() caught in this file's first draft, repeated in the claim written from it.
    print("\n  LOBE C_D REDUCTION NEEDED FOR U_max/V_to = 1.0 (within corner, exact):")
    reductions = []
    for r0 in (ZEB["u_lo"], ZEB["u_hi"]):
        red = 1.0 / r0 ** 2
        reductions.append(red)
        print(f"    from U_max/V_to = {r0}:  C_D must fall {red:.2f}x")
    print(f"    -> {min(reductions):.2f}x to {max(reductions):.2f}x"
          f"   (claim 991 said 1.8x-7.3x by mixing corners)")

    import math
    re_ratio = EXO["re"] / ZEB["re"]
    n_lo = math.log(ZEB["cd_lo"] / EXO["cd_lo"]) / math.log(re_ratio)
    n_hi = math.log(ZEB["cd_hi"] / EXO["cd_hi"]) / math.log(re_ratio)
    n = (n_lo + n_hi) / 2
    print(f"\n  C_D ~ Re^-n with n = {n_lo:.3f} to {n_hi:.3f} (two tabulated points, mean {n:.3f})")
    re_ratios = [(r ** (1.0 / n)) for r in reductions]
    print(f"  -> Reynolds number must rise {min(re_ratios):.1f}x to {max(re_ratios):.1f}x")

    # Re ~ V_to * L, and V_to ~ sqrt(W/S) ~ sqrt(L) under geometric scaling, so Re ~ L^1.5.
    # f*A_pp/V_to is SIZE-INDEPENDENT under constant Strouhal (f*A = St*U), and the table
    # supports that empirically: both rows carry fa = 0.09-0.10 across a 30x Reynolds range.
    L_ratios = [r ** (2.0 / 3.0) for r in re_ratios]
    print(f"\n  Re ~ L^1.5 (V_to ~ sqrt(L)), and f*A_pp/V_to is size-independent under constant")
    print(f"  Strouhal -- which the table CONFIRMS: both rows share fa = {FA_LO}-{FA_HI} across a")
    print(f"  {re_ratio:.0f}x Reynolds range. So:")
    print(f"    body length must rise {min(L_ratios):.2f}x to {max(L_ratios):.2f}x")
    print(f"    a 4 cm zebrafish becomes {4*min(L_ratios):.1f} to {4*max(L_ratios):.1f} cm")

    lo_x, hi_x = min(re_ratios), max(re_ratios)
    print("\n" + "-" * 78)
    print(f"  READ THIS AS A RANGE, NOT A DESIGN POINT: Reynolds number must rise by")
    print(f"  {lo_x:.1f}x to {hi_x:.1f}x, i.e. {math.log10(lo_x):.1f} to {math.log10(hi_x):.1f} "
          f"orders of magnitude. The exponent comes from")
    print("  two tabulated points; a third would move it, and the required Re ratio is that")
    print("  exponent inverted, which amplifies its error. What the number supports is the")
    print("  DIRECTION and the SCALE -- the gap is a body-size problem, not a few percent of")
    print("  fin area.")
    print("\n  AND NO FIN ALLELE SUPPLIES IT. Re = U*L/nu. The measured genetic levers change")
    print("  fin area (2.67x, claim 987) and fin proportion (claim 990). Neither changes body")
    print("  length or kinematic viscosity. The lever that would is BODY SIZE, and the alleles")
    print("  this project has measured do not provide it -- kcnh2a^lof/+ enlarges fins on a")
    print("  wild-type-sized fish.")
    print("-" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
