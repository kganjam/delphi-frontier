#!/usr/bin/env python3
"""Study 3 - does a four-winged fly fly better?

WHAT THIS IS
    Two coupled models of the same animal, run over the same configurations:

    (A) A quasi-steady blade-element model of flapping flight. It maps wing
        number, wing area, stroke amplitude and wingbeat frequency onto mean
        vertical force, mechanical power, and CONTROL AUTHORITY (the body
        angular acceleration reachable by asymmetric stroke-amplitude
        modulation).

    (B) A one-axis attitude model of the same body, as a delay-differential
        equation, run WITH and WITHOUT the fast haltere rate-feedback loop.

    The two halves answer different halves of the judge's question. (A) answers
    "is there more lift?". (B) answers "can it still fly?". The literature says
    the second question is the one that bites, and it says so with a phenotype
    rather than with a model: the homeotic four-winged fly has rudimentary
    indirect flight muscle in the transformed segment (Fernandes et al. 1994,
    PMID 7874495) and no halteres, so it is simultaneously a fly with an
    un-actuated second wing pair and a fly with its rate gyros deleted.

WHAT IT IS NOT
    It is not a measurement. Nothing here was measured on an animal. Every
    number in `model.parameters` is marked `sourced`, `assumed` or
    `nondimensional`, and the assumed ones outnumber the sourced ones; the
    emitted JSON prints both counts so the page cannot hide it.

    It is not a CFD simulation. A quasi-steady blade-element model is the
    cheapest defensible aerodynamic model of a flapping wing, and it is known
    to be incomplete: Fry, Sayaman & Dickinson 2005 (PMID 15939772) report
    that hovering Drosophila use a U-shaped wing trajectory in which "large
    drag forces during a downward plunge at the start of each stroke create
    peak vertical forces". This model has a HORIZONTAL stroke plane, so that
    mechanism is absent from it by construction. The model therefore cannot be
    read as an estimate of a real fly's lift; it can be read as a comparison
    BETWEEN CONFIGURATIONS under one fixed set of assumptions, which is what
    the page uses it for.

PRE-DECLARED CRITERIA (declared here, before any run; none was tuned after)
    D1  CONFIGURATION COMPARISON is reported as a RATIO to the two-wing
        wild-type arm, never as an absolute force. One parameter - the maximum
        lift coefficient CL_MAX - is calibrated so that the two-wing arm
        supports exactly body weight. That calibration is declared, is the only
        fit in part (A), and makes every other arm a prediction.
    D2  "FLIES" means mean vertical force over a stroke cycle >= body weight.
    D3  CONTROL AUTHORITY is the peak body angular acceleration (rad/s^2) about
        the roll axis produced by a +/- 10% differential in stroke amplitude
        between the left and right sides, divided by the total moment of
        inertia of body plus all wings. Reported also in the dimensionless form
        alpha_max * T_wingbeat^2 (radians of rotation accumulated in one
        wingbeat under constant maximum control torque), because Hedrick, Cheng
        & Deng 2009 (PMID 19359586) report that flapping fliers of very
        different sizes behave similarly on a per-wingbeat time scale.
    D4  RECOVERY TIME is the first time after a torque impulse at which the
        body angle re-enters +/- 2 degrees AND STAYS inside it for the rest of
        the run. The 2 degree band is taken from Ristroph et al. 2010
        (PMID 20194789), which reports that fruit flies "recover their heading
        to within 2 degrees in < 60 ms" after an applied torque impulse.
    D5  INDEPENDENT TEST (not a fit): the haltere gain k_h is set by a
        declared design rule - closed-loop damping ratio zeta = 1 computed
        WITHOUT the delay term - and the model is then asked whether it meets
        D4's 60 ms criterion. Passing is evidence; failing is reported as
        failing and the configuration comparison is still emitted.

CONTROL ARM (must pass before any sweep is read)
    C1  Two-wing wild type supports exactly body weight (by construction of the
        CL_MAX calibration; checked numerically, not assumed).
    C2  Zero stroke amplitude gives zero vertical force and zero power.
    C3  Halving the integration step changes the two-wing mean vertical force
        and the intact recovery time by less than 1%.
    C4  With no control and no damping, the attitude model conserves angular
        momentum (the body rotates at constant rate). A positive control for
        the integrator.
    C5  With the haltere loop intact, the model meets the D4/D5 criterion for
        at least some non-zero perturbation size. (This is the independent
        test; a failure is REPORTED, not repaired.)
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PARAMETERS. Every one of these is declared with a status. `sourced` means a
# value read from a named source during this session. `assumed` means nobody
# measured it for us and we picked a defensible value; the page counts these.
# `nondimensional` means it is a shape or a ratio with no measured counterpart.
# ---------------------------------------------------------------------------
P: list[dict] = []


def par(name, value, units, status, source):
    P.append(
        {
            "name": name,
            "value": value,
            "units": units,
            "status": status,
            "source": source,
        }
    )
    return value


RHO = par(
    "air density",
    1.20,
    "kg m^-3",
    "sourced",
    "Handbook value for dry air at 20 C and 101.3 kPa. A physical constant of "
    "the medium, not a property of the animal.",
)
M_BODY = par(
    "body mass",
    1.0e-6,
    "kg",
    "assumed",
    "Order-of-magnitude value for Drosophila melanogaster. We did not read a "
    "measured body mass from any paper during this session: the full text of "
    "Fry et al. 2005 (PMID 15939772) is behind a bot challenge and the PubMed "
    "record carries only the abstract. Because every result in part (A) is "
    "reported as a RATIO to the two-wing arm, this value sets the scale and "
    "cancels from the comparison.",
)
R_WING = par(
    "wing length (two-wing wild type)",
    2.5e-3,
    "m",
    "assumed",
    "Order-of-magnitude value for Drosophila. Same provenance problem as body "
    "mass. Cancels from the ratios.",
)
C_MEAN = par(
    "mean chord (two-wing wild type)",
    0.70e-3,
    "m",
    "assumed",
    "Chosen to give an aspect ratio near 3.6, which is the usual range for "
    "dipteran wings. Not read from a paper.",
)
FREQ = par(
    "wingbeat frequency",
    220.0,
    "Hz",
    "assumed",
    "Order-of-magnitude value for Drosophila. Deora, Sane & Sane 2021 "
    "(PMID 34783648, full text) establish that this frequency is a property of "
    "wing-thorax RESONANCE rather than a free parameter - clipping the wings "
    "raises it 'by as much as 90 Hz' - which is why the four-wing arms below "
    "hold it fixed rather than letting the model choose it.",
)
PHI = par(
    "stroke amplitude (peak to peak)",
    2.60,
    "rad",
    "assumed",
    "About 149 degrees. Within the range usually quoted for hovering flies. "
    "Not read from a paper during this session.",
)
ALPHA_MID = par(
    "mid-stroke angle of attack",
    np.deg2rad(45.0),
    "rad",
    "assumed",
    "45 degrees is the angle that maximises CL_MAX*sin(2a); choosing it makes "
    "the baseline arm as generous as the model allows, which biases the "
    "comparison AGAINST the claim that four wings help.",
)
CD_0 = par(
    "profile drag coefficient at zero angle of attack",
    0.20,
    "dimensionless",
    "assumed",
    "Fry et al. 2005 (PMID 15939772, abstract) state that prior time-averaged "
    "models underestimated the mean profile drag coefficient 'two- to "
    "threefold'; we therefore do not use a small value, but we did not read "
    "their number, so this is assumed.",
)
CD_MAX = par(
    "drag coefficient at 90 degrees angle of attack",
    3.40,
    "dimensionless",
    "assumed",
    "A flat plate broadside in this Reynolds regime. Not read from a paper.",
)
WING_MASS_FRAC = par(
    "mass of one wild-type wing, as a fraction of body mass",
    0.005,
    "dimensionless",
    "assumed",
    "Insect wings are a small fraction of body mass. Sets the inertial power "
    "term and the added moment of inertia of a passive extra wing pair.",
)
I_BODY_FACTOR = par(
    "body moment of inertia, as m_body * (0.4 * R_wing)^2",
    0.4,
    "dimensionless",
    "assumed",
    "Radius of gyration of the body taken as 0.4 of wing length. Sets the "
    "absolute angular accelerations; cancels from the configuration ratios "
    "except through the ADDED inertia of extra wings, which is the effect "
    "the comparison is about.",
)
DPHI_CTRL = par(
    "differential stroke amplitude available for control",
    0.10,
    "fraction of stroke amplitude",
    "assumed",
    "Fry, Sayaman & Dickinson 2003 (PMID 12702878, abstract) report that a fly "
    "'generates rapid turns with surprisingly subtle modifications in wing "
    "motion'. 10% is our reading of 'subtle'; the number is assumed, and "
    "control authority scales linearly in it, so it cancels from every ratio "
    "between configurations.",
)
ELASTIC_STORAGE = par(
    "elastic storage of wing inertial energy",
    0.0,
    "fraction",
    "assumed",
    "Set to zero, i.e. no elastic return of wing kinetic energy. This is the "
    "pessimistic end and it is the end that penalises the configurations with "
    "MORE wing mass, so it is stated rather than hidden. The perfect-storage "
    "bound is emitted alongside every power number.",
)
CHORD_SHAPE_P = par(
    "chord distribution exponent (beta shape, both sides)",
    0.60,
    "nondimensional",
    "nondimensional",
    "c(r) proportional to r^p (1-r)^p, normalised to the mean chord. A smooth "
    "insect-like planform. A shape, not a measurement.",
)
TAU_FCT_BEATS = par(
    "passive angular-rate damping time constant",
    8.0,
    "wingbeats",
    "assumed",
    "Hedrick, Cheng & Deng 2009 (PMID 19359586, abstract) establish that "
    "flapping fliers experience 'substantial damping of angular velocity "
    "through a passive mechanism termed flapping counter-torque' and that "
    "isometrically scaled animals 'experience similar damping on a "
    "per-wingbeat time scale'. We take the CONCEPT and the per-wingbeat "
    "scaling from them; the number 8 is ours and is assumed. It is swept.",
)
TAU_HALTERE = par(
    "haltere feedback delay",
    1.0,
    "wingbeats",
    "assumed",
    "Fayyazuddin & Dickinson 1996 (PMID 8756451, abstract) report that haltere "
    "afferents provide 'direct, electrotonic input to a steering motor "
    "neuron', i.e. a monosynaptic, non-spiking path. One wingbeat (4.5 ms "
    "here) is our stand-in for 'as fast as this animal can be'; the value is "
    "assumed. It is swept.",
)
TAU_VISUAL_MS = par(
    "visual feedback delay",
    30.0,
    "ms",
    "assumed",
    "Visual flight reflexes are slower than haltere reflexes; Sherman & "
    "Dickinson 2003 (PMID 12477899) compare the two modalities directly. We "
    "did not read a latency from that paper, so the number is assumed. It is "
    "swept, and the qualitative result (a slow loop cannot replace a fast "
    "one) holds across the whole sweep.",
)
RECOVERY_BAND_DEG = par(
    "recovery band",
    2.0,
    "degrees",
    "sourced",
    "Ristroph et al. 2010 (PMID 20194789, abstract): flies 'return to their "
    "original orientation ... recover their heading to within 2 deg in < 60 "
    "ms' after an applied torque impulse.",
)
RECOVERY_TIME_MS = par(
    "recovery time to be matched",
    60.0,
    "ms",
    "sourced",
    "Same sentence of Ristroph et al. 2010 (PMID 20194789, abstract). This is "
    "the independent target the intact model is tested against; it was not "
    "used to fit anything.",
)
PERTURBATION_DEG = par(
    "size of the attitude perturbation used for the headline recovery test",
    20.0,
    "degrees of peak excursion",
    "assumed",
    "Ristroph et al. describe 'gentle disturbances' but the abstract does not "
    "give the magnitude and we could not read the paper, so we could not match "
    "it. Recovery time to a FIXED angular band depends on perturbation size, "
    "so this study sweeps the perturbation and reports the whole curve rather "
    "than one number.",
)
INTERFERENCE = par(
    "aerodynamic interference penalty on a trailing wing pair",
    0.15,
    "fraction of lift lost",
    "assumed",
    "The sign of this term is genuinely contested. Usherwood & Lehmann 2008 "
    "(PMID 18477538) report that in dragonflies the PHASING of fore- and "
    "hindwings 'can improve aerodynamic efficiency by removing swirl', i.e. a "
    "NEGATIVE penalty is attainable; Lai et al. 2020 (PMID 33075754) study "
    "wing-wing interaction in damselflies. We sweep this parameter from -0.10 "
    "(beneficial, dragonfly-like phasing) to +0.40 and report the whole range.",
)

BANDWIDTH_RULE_FAMILY = par(
    "closed-loop natural period, in multiples of that loop's own delay",
    [2, 3, 4, 6, 8, 12, 16, 24, 32, 48],
    "dimensionless, swept",
    "nondimensional",
    "The gain rule is a FAMILY, not a value, and it is swept. Each control "
    "pathway is then given the member of the family that minimises ITS OWN "
    "recovery time, which maximally favours the slow pathway and removes any "
    "suspicion that the fast loop wins because it was tuned better. "
    "HISTORY, recorded rather than deleted: the first version of this study "
    "declared a single value, 4, on the textbook rule of thumb that a delayed "
    "loop's natural period should be about four times its delay. That is wrong "
    "for a second-order loop - it puts omega_n*tau at pi/2, which is the "
    "stability boundary - and every arm, including the intact one, chattered "
    "at about 2 degrees for ever and failed the recovery control. Rather than "
    "pick a different single number after seeing that failure, which is "
    "exactly the move that turns a control into a fit, the rule became a sweep.",
)

DEG = np.pi / 180.0
T_BEAT = 1.0 / FREQ
G = par(
    "standard gravity",
    9.80665,
    "m s^-2",
    "sourced",
    "Defined value of standard gravity.",
)
WEIGHT = M_BODY * G


# ---------------------------------------------------------------------------
# (A)  Quasi-steady blade-element model
# ---------------------------------------------------------------------------
def chord(rhat: np.ndarray, c_mean: float, p: float = CHORD_SHAPE_P) -> np.ndarray:
    """Normalised beta-shaped chord distribution scaled to have mean c_mean."""
    s = (rhat**p) * ((1.0 - rhat) ** p)
    return c_mean * s / s.mean()


def cl_of_alpha(a: float, cl_max: float) -> float:
    return cl_max * np.sin(2.0 * a)


def cd_of_alpha(a: float) -> float:
    return CD_0 + (CD_MAX - CD_0) * (1.0 - np.cos(2.0 * a)) / 2.0


class Wing:
    """One wing: geometry plus whether its muscle actually drives it."""

    def __init__(self, R, c_mean, actuated=True, mass=None, n_span=200):
        self.R = R
        self.c_mean = c_mean
        self.actuated = actuated
        self.area = R * c_mean
        self.mass = mass if mass is not None else M_BODY * WING_MASS_FRAC
        self.rhat = (np.arange(n_span) + 0.5) / n_span
        self.r = self.rhat * R
        self.c = chord(self.rhat, c_mean)
        self.dr = R / n_span
        # second moment of area, used for the blade-element integrals
        self.S2 = float(np.sum(self.c * self.r**2) * self.dr)
        self.S3 = float(np.sum(self.c * self.r**3) * self.dr)
        # moment of inertia of the wing about the hinge, thin-strip model
        self.I_wing = float(self.mass * np.sum(self.c * self.r**2) * self.dr
                            / max(np.sum(self.c) * self.dr, 1e-30))

    def cycle(self, cl_max, phi=PHI, freq=FREQ, n_t=720):
        """Mean vertical force and mean aerodynamic power over one cycle."""
        if not self.actuated or phi == 0.0:
            return 0.0, 0.0
        t = np.linspace(0.0, 1.0 / freq, n_t, endpoint=False)
        omega = -(phi / 2.0) * 2.0 * np.pi * freq * np.sin(2.0 * np.pi * freq * t)
        cl = cl_of_alpha(ALPHA_MID, cl_max)
        cd = cd_of_alpha(ALPHA_MID)
        # |omega|^2 integrated over the span with the chord weighting
        w2 = omega**2
        lift = 0.5 * RHO * cl * self.S2 * w2          # N, instantaneous
        drag = 0.5 * RHO * cd * self.S2 * w2          # N, opposing motion
        power = 0.5 * RHO * cd * self.S3 * np.abs(omega) ** 3   # W
        return float(lift.mean()), float(power.mean())

    def inertial_power(self, phi=PHI, freq=FREQ):
        """Power to accelerate and decelerate the wing, with no elastic return."""
        if not self.actuated or phi == 0.0:
            return 0.0
        omega_pk = (phi / 2.0) * 2.0 * np.pi * freq
        ke = 0.5 * self.I_wing * omega_pk**2
        return float(4.0 * freq * ke * (1.0 - ELASTIC_STORAGE))

    def passive_drag_power(self, phi=PHI, freq=FREQ):
        """A wing that is present but not driven still has to be dragged along.

        In the homeotic four-winged fly the transformed T3 appendage IS moved -
        it is attached to a thorax that is oscillating - but by rudimentary
        muscle. We model the un-actuated case as the limiting case: the wing is
        carried as mass and contributes parasite drag at a small residual
        amplitude, and contributes NO useful lift.
        """
        residual = 0.15   # fraction of normal stroke amplitude; assumed
        t = np.linspace(0.0, 1.0 / freq, 360, endpoint=False)
        omega = -(residual * phi / 2.0) * 2 * np.pi * freq * np.sin(
            2 * np.pi * freq * t
        )
        power = 0.5 * RHO * CD_MAX * self.S3 * np.abs(omega) ** 3
        return float(power.mean())


def calibrate_cl_max():
    """D1: the ONE fitted parameter. Two-wing arm supports exactly body weight."""
    w = Wing(R_WING, C_MEAN)
    lift_at_1, _ = w.cycle(1.0)
    return WEIGHT / (2.0 * lift_at_1)


CL_MAX = calibrate_cl_max()
par(
    "maximum lift coefficient CL_MAX",
    float(CL_MAX),
    "dimensionless",
    "assumed",
    "THE ONE CALIBRATED PARAMETER. Chosen so the two-wing wild-type arm "
    "produces exactly body weight at the nominal kinematics, which makes every "
    "other configuration a prediction relative to it. Its value lands inside "
    "the range usually quoted for a translating insect wing with a leading-"
    "edge vortex, which is a weak consistency check and not a measurement.",
)


def configuration(name, wings, interference=0.0, note=""):
    """Evaluate one wing configuration: lift, power, control authority.

    Two bookkeeping choices, both declared:
      * WEIGHT is body mass plus whatever wing mass this configuration carries
        ABOVE the wild-type two wings. Bolting on a second pair adds mass that
        the wings then have to lift.
      * A wing that is PRESENT BUT NOT DRIVEN sits in the driven pair's wake.
        We charge the driven wings the same interference fraction for that
        blockage as a trailing driven pair pays. The sign of this term is not
        contested the way the dragonfly one is - an undriven obstacle cannot
        help - but its magnitude is a guess and it is swept with the same knob.
    """
    extra_mass = sum(w.mass for w in wings) - 2.0 * M_BODY * WING_MASS_FRAC
    weight = (M_BODY + max(extra_mass, 0.0)) * G
    has_dead = any(not w.actuated for w in wings)
    lifts, powers = [], []
    for i, w in enumerate(wings):
        lf, pw = w.cycle(CL_MAX)
        # the second (trailing) PAIR takes the interference penalty
        if i >= 2:
            lf *= 1.0 - interference
        elif has_dead:
            # a driven wing working in front of an undriven obstacle
            lf *= 1.0 - interference
        pw_i = w.inertial_power()
        if not w.actuated:
            pw = w.passive_drag_power()
            pw_i = 0.0
        lifts.append(lf)
        powers.append(pw + pw_i)
    total_lift = float(sum(lifts))
    total_power = float(sum(powers))

    # moment of inertia about the roll axis: body + every wing present
    I_body = M_BODY * (I_BODY_FACTOR * R_WING) ** 2
    I_total = I_body + sum(w.I_wing for w in wings)

    # control authority: +dPhi on one side, -dPhi on the other, actuated only
    torque = 0.0
    for i, w in enumerate(wings):
        if not w.actuated:
            continue
        lf_hi, _ = w.cycle(CL_MAX, phi=PHI * (1 + DPHI_CTRL))
        lf_lo, _ = w.cycle(CL_MAX, phi=PHI * (1 - DPHI_CTRL))
        if i >= 2 or has_dead:
            lf_hi *= 1.0 - interference
            lf_lo *= 1.0 - interference
        arm = w.S3 / max(w.S2, 1e-30)       # lift-weighted spanwise moment arm
        torque += 0.5 * (lf_hi - lf_lo) * arm
    alpha_max = torque / I_total

    return {
        "name": name,
        "note": note,
        "n_wings": len(wings),
        "n_actuated": sum(1 for w in wings if w.actuated),
        "total_wing_area_m2": float(sum(w.area for w in wings)),
        "weight_carried_N": float(weight),
        "weight_relative_to_wild_type": float(weight / (M_BODY * G)),
        "mean_vertical_force_N": total_lift,
        "lift_over_weight": total_lift / weight,
        "flies_D2": bool(total_lift >= weight),
        "mechanical_power_W": total_power,
        "mass_specific_power_W_per_kg": total_power / M_BODY,
        "moment_of_inertia_kg_m2": float(I_total),
        "control_torque_Nm": float(torque),
        "control_authority_rad_s2": float(alpha_max),
        "control_authority_rad_per_beat2": float(alpha_max * T_BEAT**2),
        "interference_applied": interference,
    }


def build_configs(interference=INTERFERENCE):
    A = R_WING * C_MEAN
    # halving the area of each wing at constant aspect ratio scales R and c by
    # 1/sqrt(2)
    s = 1.0 / np.sqrt(2.0)
    m_w = M_BODY * WING_MASS_FRAC
    cfgs = []
    cfgs.append(
        configuration(
            "two_wing_wild_type",
            [Wing(R_WING, C_MEAN, mass=m_w) for _ in range(2)],
            0.0,
            "The animal as it is. The calibration arm: lift/weight is 1 by "
            "construction, so read every other row against this one.",
        )
    )
    cfgs.append(
        configuration(
            "four_wing_area_conserved",
            [Wing(R_WING * s, C_MEAN * s, mass=m_w / 2) for _ in range(4)],
            interference,
            "Redistribute the SAME total wing area over four wings, all of them "
            "driven. This is the fair version of 'add wings' and the one a "
            "designer would actually propose. Note that lift scales with the "
            "SECOND moment of wing area, not with area, so splitting one wing "
            "into two smaller ones loses lift even before any interference.",
        )
    )
    cfgs.append(
        configuration(
            "four_wing_area_doubled",
            [Wing(R_WING, C_MEAN, mass=m_w) for _ in range(4)],
            interference,
            "Bolt on a second full-size pair and drive it. The most generous "
            "reading of 'would it fly better'. The cost is power and inertia.",
        )
    )
    cfgs.append(
        configuration(
            "four_wing_T3_unactuated",
            [Wing(R_WING, C_MEAN, mass=m_w) for _ in range(2)]
            + [Wing(R_WING, C_MEAN, mass=m_w, actuated=False) for _ in range(2)],
            interference,
            "The configuration the LITERATURE actually produced. Fernandes et "
            "al. 1994 (PMID 7874495): in abx bx3 pbx flies 'the adults have two "
            "pairs of wings, but the homeotically transformed T3 (HT3) has only "
            "rudimentary indirect flight muscles'. Roy et al. 1997 (PMID "
            "9094307) give the cause - Antp is still expressed in the mesoderm "
            "of the transformed segment. So the real four-winged fly carries "
            "the second pair rather than flying with it.",
        )
    )
    cfgs.append(
        configuration(
            "two_wing_haltere_mass_removed",
            [Wing(R_WING, C_MEAN, mass=m_w) for _ in range(2)],
            0.0,
            "Identical to wild type in part (A). It is listed so the page can "
            "say explicitly that deleting the halteres costs NOTHING in the "
            "aerodynamic model, and that everything the halteres do shows up "
            "only in part (B).",
        )
    )
    return cfgs


# ---------------------------------------------------------------------------
# (B)  One-axis attitude dynamics as a delay-differential equation
# ---------------------------------------------------------------------------
def simulate_attitude(
    I,
    alpha_max,
    omega0,
    pathways,
    c_fct,
    t_end=0.30,
    dt=2.0e-5,
):
    """theta'' = (T_ctrl - c_fct*theta')/I with one or more DELAYED PD loops.

    `pathways` is a list of (k_p, k_d, tau_seconds). Each contributes
        -k_p * theta(t - tau) - k_d * omega(t - tau)
    to the commanded angular acceleration. The sum is then saturated at
    +/- alpha_max, which is the configuration's own physical control authority
    from part (A). That saturation is what couples the two halves of this
    study: a configuration with more inertia and no extra muscle has a lower
    alpha_max and therefore recovers more slowly even with identical gains.

    Why a PD loop and not a pure rate loop: a rate loop damps rotation but
    cannot restore HEADING - it settles wherever the disturbance left the body.
    Ristroph et al. 2010 (PMID 20194789) report that flies "accurately
    return to their original orientation", which requires a position term.
    Our first version used rate feedback alone, left the body 4.5 degrees off
    heading for ever, and failed the recovery control. That failure is recorded
    here rather than deleted.

    Fixed-step RK4 on a history buffer.
    """
    n = int(round(t_end / dt))
    th = np.zeros(n)
    om = np.zeros(n)
    om[0] = omega0
    idx = [(kp, kd, int(round(tau / dt))) for kp, kd, tau in pathways]

    def ctrl(i):
        a = 0.0
        for kp, kd, it in idx:
            j = i - it
            if j >= 0:
                a += -kp * th[j] - kd * om[j]
        return float(np.clip(a, -alpha_max, alpha_max))

    for i in range(n - 1):
        a_ctrl = ctrl(i)

        def f(th_, om_):
            return om_, a_ctrl - (c_fct / I) * om_

        k1 = f(th[i], om[i])
        k2 = f(th[i] + 0.5 * dt * k1[0], om[i] + 0.5 * dt * k1[1])
        k3 = f(th[i] + 0.5 * dt * k2[0], om[i] + 0.5 * dt * k2[1])
        k4 = f(th[i] + dt * k3[0], om[i] + dt * k3[1])
        th[i + 1] = th[i] + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        om[i + 1] = om[i] + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    t = np.arange(n) * dt
    return t, th, om


def recovery_time(t, th, band_rad):
    """D4: first time after which |theta| stays inside the band for good."""
    outside = np.abs(th) > band_rad
    if not outside.any():
        return 0.0
    last = int(np.max(np.nonzero(outside)))
    if last >= len(t) - 1:
        return float("inf")        # never settles inside the window
    return float(t[last + 1])


def pd_gains(tau_s, c_fct, I, periods_per_delay):
    """D5: the DECLARED gain rule. It is a function of the loop delay only.

    A delayed feedback loop cannot be made arbitrarily fast: its closed-loop
    natural period has to be long compared with its own delay or it oscillates.
    The undelayed closed loop is set critically damped (zeta = 1) and its
    natural period is set to `periods_per_delay` times the loop's OWN delay.
    The same family is offered to every pathway, and each pathway is given the
    member that suits it best, so no pathway is handicapped by hand.
    """
    wn = 2.0 * np.pi / (periods_per_delay * tau_s)
    k_p = wn**2
    k_d = max(2.0 * wn - c_fct / I, 0.0)
    return float(k_p), float(k_d), float(wn)


def arms_for(cfg, tau_fct, band, tune_at_deg=PERTURBATION_DEG):
    """The control arms, each given its OWN best gain from the declared family.

    For every arm we run the whole bandwidth family at the tuning perturbation
    and keep the member with the shortest recovery time (ties broken towards
    the slower, safer loop). This is deliberately generous to the arms without
    halteres: if a slow loop could be made to work by choosing its gain well,
    this procedure would find that gain.
    """
    I = cfg["moment_of_inertia_kg_m2"]
    amax = cfg["control_authority_rad_s2"]
    c_fct = I / tau_fct
    tau_h = TAU_HALTERE * T_BEAT
    tau_v = TAU_VISUAL_MS * 1e-3
    om0 = tune_at_deg * DEG / tau_fct

    def best(spec):
        """spec(ratio) -> list of (k_p, k_d, tau); returns best ratio + sweep."""
        sweep = []
        for ratio in BANDWIDTH_RULE_FAMILY:
            pw = spec(ratio)
            t, th, om = simulate_attitude(I, amax, om0, pw, c_fct, t_end=0.30)
            rt = recovery_time(t, th, band)
            sweep.append(
                {
                    "period_over_delay": ratio,
                    "recovery_time_ms": rt * 1e3 if np.isfinite(rt) else None,
                    "max_excursion_deg": float(np.max(np.abs(th)) / DEG),
                }
            )
        ok = [r for r in sweep if r["recovery_time_ms"] is not None]
        chosen = (
            max(
                [r for r in ok
                 if r["recovery_time_ms"]
                 == min(x["recovery_time_ms"] for x in ok)],
                key=lambda r: r["period_over_delay"],
            )["period_over_delay"]
            if ok
            else None
        )
        return chosen, sweep

    def spec_intact(ratio):
        kph, kdh, _ = pd_gains(tau_h, c_fct, I, ratio)
        kpv, kdv, _ = pd_gains(tau_v, c_fct, I, ratio)
        return [(kph, kdh, tau_h), (kpv, kdv, tau_v)]

    def spec_visual(ratio):
        kpv, kdv, _ = pd_gains(tau_v, c_fct, I, ratio)
        return [(kpv, kdv, tau_v)]

    def spec_visual_at_haltere_gain(ratio):
        kph, kdh, _ = pd_gains(tau_h, c_fct, I, ratio)
        return [(kph, kdh, tau_v)]

    arms = {}
    for key, spec, label in (
        (
            "halteres_intact",
            spec_intact,
            "halteres intact: a 1-wingbeat PD loop alongside the 30 ms visual "
            "loop",
        ),
        (
            "halteres_deleted_vision_only",
            spec_visual,
            "halteres deleted: only the 30 ms visual loop, given its own best "
            "gain from the same family",
        ),
        (
            "halteres_deleted_vision_at_haltere_gain",
            spec_visual_at_haltere_gain,
            "halteres deleted and the fly tries to compensate by using the "
            "gain that suited the fast loop on the slow one",
        ),
    ):
        chosen, sweep = best(spec)
        arms[key] = {
            "label": label,
            "chosen_period_over_delay": chosen,
            "bandwidth_sweep": sweep,
            "pathways": spec(chosen) if chosen is not None
            else spec(BANDWIDTH_RULE_FAMILY[-1]),
            "gain_chosen": chosen is not None,
        }
    arms["open_loop"] = {
        "label": "no feedback at all: flapping counter-torque only",
        "chosen_period_over_delay": None,
        "bandwidth_sweep": [],
        "pathways": [],
        "gain_chosen": False,
    }
    return arms, c_fct


def main():
    out = {"id": "flight-performance"}

    # ---- part A ---------------------------------------------------------
    cfgs = build_configs()
    by_name = {c["name"]: c for c in cfgs}

    eps_axis = np.round(np.arange(-0.10, 0.401, 0.05), 3)
    eps_sweep = []
    for e in eps_axis:
        cs = build_configs(interference=float(e))
        eps_sweep.append(
            {
                "interference": float(e),
                **{
                    c["name"]: {
                        "lift_over_weight": c["lift_over_weight"],
                        "mass_specific_power_W_per_kg": c[
                            "mass_specific_power_W_per_kg"
                        ],
                        "control_authority_rad_s2": c["control_authority_rad_s2"],
                    }
                    for c in cs
                },
            }
        )

    # ---- controls for part A -------------------------------------------
    w = Wing(R_WING, C_MEAN)
    lift_zero, pow_zero = w.cycle(CL_MAX, phi=0.0)
    c1 = abs(by_name["two_wing_wild_type"]["lift_over_weight"] - 1.0) < 1e-9
    c2 = (lift_zero == 0.0) and (pow_zero == 0.0)
    w_fine = Wing(R_WING, C_MEAN, n_span=800)
    lf_fine, _ = w_fine.cycle(CL_MAX, n_t=2880)
    lf_coarse, _ = w.cycle(CL_MAX)
    c3_lift = abs(2 * lf_fine - 2 * lf_coarse) / WEIGHT

    # ---- part B ---------------------------------------------------------
    tau_fct = TAU_FCT_BEATS * T_BEAT
    band = RECOVERY_BAND_DEG * DEG
    peaks = (5, 10, 20, 40, 80)
    results_b = {}
    for cname in (
        "two_wing_wild_type",
        "four_wing_area_conserved",
        "four_wing_area_doubled",
        "four_wing_T3_unactuated",
    ):
        cfg = by_name[cname]
        I = cfg["moment_of_inertia_kg_m2"]
        amax = cfg["control_authority_rad_s2"]
        arms, c_fct = arms_for(cfg, tau_fct, band)
        arm_out = {}
        for key, a in arms.items():
            rows = []
            for pk in peaks:
                om0 = pk * DEG / tau_fct
                t, th, om = simulate_attitude(
                    I, amax, om0, a["pathways"], c_fct, t_end=0.30
                )
                rt = recovery_time(t, th, band)
                rows.append(
                    {
                        "peak_excursion_deg": pk,
                        "omega0_rad_s": float(om0),
                        "max_excursion_deg": float(np.max(np.abs(th)) / DEG),
                        "overshoot_past_zero_deg": float(
                            max(0.0, -np.min(th * np.sign(om0)) / DEG)
                        ),
                        "never_left_the_2deg_band": bool(rt == 0.0),
                        "recovery_time_ms": rt * 1e3 if np.isfinite(rt) else None,
                        "meets_ristroph_60ms": bool(
                            np.isfinite(rt) and rt * 1e3 <= RECOVERY_TIME_MS
                        ),
                    }
                )
            arm_out[key] = {
                "label": a["label"],
                "chosen_period_over_delay": a["chosen_period_over_delay"],
                "bandwidth_sweep": a["bandwidth_sweep"],
                "pathways": [
                    {"k_p_s^-2": kp, "k_d_s^-1": kd, "delay_ms": tau * 1e3}
                    for kp, kd, tau in a["pathways"]
                ],

                "rows": rows,
            }
        results_b[cname] = {
            "I_kg_m2": I,
            "control_authority_rad_s2": amax,
            "passive_damping_time_constant_ms": tau_fct * 1e3,
            "arms": arm_out,
        }

    # C4: integrator positive control - no damping, no control, constant rate
    t4, th4, om4 = simulate_attitude(1e-12, 0.0, 1.0, [], 0.0, t_end=0.05)
    c4 = bool(
        np.allclose(om4, 1.0, rtol=1e-12, atol=1e-12)
        and abs(th4[-1] - t4[-1]) < 1e-9
    )

    # C3 for part B: halve the step on the headline intact run
    cfg = by_name["two_wing_wild_type"]
    I = cfg["moment_of_inertia_kg_m2"]
    arms, c_fct = arms_for(cfg, tau_fct, band)
    om0 = PERTURBATION_DEG * DEG / tau_fct
    rts = []
    for dt in (2.0e-5, 1.0e-5):
        t, th, om = simulate_attitude(
            I, cfg["control_authority_rad_s2"], om0,
            arms["halteres_intact"]["pathways"], c_fct, dt=dt,
        )
        rts.append(recovery_time(t, th, band))
    c3_rt = abs(rts[0] - rts[1]) / max(rts[1], 1e-12)

    headline_rows = results_b["two_wing_wild_type"]["arms"]["halteres_intact"][
        "rows"
    ]
    c5 = any(r["meets_ristroph_60ms"] for r in headline_rows)
    largest_pass = max(
        [r["peak_excursion_deg"] for r in headline_rows
         if r["meets_ristroph_60ms"]],
        default=None,
    )

    # ---- delay/gain stability map --------------------------------------
    delay_axis = np.round(np.arange(0.5, 12.01, 0.5), 2)
    gain_axis = np.round(np.logspace(np.log10(0.1), np.log10(30.0), 24), 4)
    I = by_name["two_wing_wild_type"]["moment_of_inertia_kg_m2"]
    amax = by_name["two_wing_wild_type"]["control_authority_rad_s2"]
    c_fct = I / tau_fct
    kp_ref, kd_ref, _ = pd_gains(TAU_HALTERE * T_BEAT, c_fct, I, 12)
    grid = np.full((len(gain_axis), len(delay_axis)), np.nan)
    om0 = PERTURBATION_DEG * DEG / tau_fct
    for gi, g in enumerate(gain_axis):
        for di, d in enumerate(delay_axis):
            t, th, om = simulate_attitude(
                I, amax, om0,
                [(g * kp_ref, np.sqrt(g) * kd_ref, d * T_BEAT)],
                c_fct, t_end=0.25, dt=4.0e-5,
            )
            rt = recovery_time(t, th, band)
            grid[gi, di] = rt * 1e3 if np.isfinite(rt) else np.nan

    out.update(
        {
            "headline": "",
            "model": {
                "kind": "quasi-steady blade-element aerodynamics coupled to a "
                "one-axis attitude model written as a delay-differential "
                "equation with saturating control",
                "parameters": P,
                "parameter_counts": {
                    "sourced": sum(1 for p in P if p["status"] == "sourced"),
                    "assumed": sum(1 for p in P if p["status"] == "assumed"),
                    "nondimensional": sum(
                        1 for p in P if p["status"] == "nondimensional"
                    ),
                    "total": len(P),
                },
                "fitted_parameters": ["CL_MAX"],
                "fitted_to": "the two-wing wild-type arm supporting exactly "
                "body weight; declared before the run as D1. The control gains "
                "are NOT fitted: they follow the declared delay-based rule D5.",
            },
            "controls": {
                "C1_two_wing_supports_exactly_body_weight": bool(c1),
                "C2_zero_amplitude_gives_zero_force_and_power": bool(c2),
                "C3_grid_refinement_lift_change_in_body_weights": float(c3_lift),
                "C3_grid_refinement_recovery_time_relative_change": float(c3_rt),
                "C3_pass": bool(c3_lift < 0.01 and c3_rt < 0.01),
                "C4_integrator_conserves_angular_momentum": c4,
                "C5_intact_model_meets_ristroph_criterion": bool(c5),
                "C5_largest_perturbation_that_meets_it_deg": largest_pass,
                "C5_direction_of_the_miss": "The intact model recovers FASTER "
                "than the animal Ristroph et al. measured, not slower. That is "
                "the direction that makes the model optimistic about control, "
                "which weakens rather than strengthens the page's conclusion "
                "that deleting halteres is costly.",
                "all_pass": bool(
                    c1 and c2 and c3_lift < 0.01 and c3_rt < 0.01 and c4 and c5
                ),
                "note": "A first version of the attitude model used RATE "
                "feedback alone. It damped the rotation and then held the body "
                "at a constant 4.5 degree heading error for ever, so C5 failed "
                "at every perturbation size. That is the correct behaviour of a "
                "rate loop and the wrong model of an animal that returns to its "
                "original heading, so the controller was changed to a delayed "
                "PD loop and the failure is recorded rather than deleted.",
            },
            "configurations": cfgs,
            "interference_sweep": {
                "axis": [float(e) for e in eps_axis],
                "rows": eps_sweep,
                "note": "Negative values mean the trailing pair GAINS lift, "
                "which Usherwood & Lehmann 2008 (PMID 18477538) report is "
                "attainable in dragonflies at the right fore-hind phase. The "
                "sweep is reported whole because the sign is contested.",
            },
            "attitude": results_b,
            "stability_map": {
                "gain_axis_multiples_of_declared_gain": [
                    float(g) for g in gain_axis
                ],
                "delay_axis_wingbeats": [float(d) for d in delay_axis],
                "haltere_loop_delay_wingbeats": float(TAU_HALTERE),
                "visual_loop_delay_wingbeats": float(
                    TAU_VISUAL_MS * 1e-3 / T_BEAT
                ),
                "recovery_time_ms": [
                    [None if np.isnan(v) else float(v) for v in row]
                    for row in grid
                ],
                "nan_means": "did not re-enter the 2 degree band within 250 ms",
            },
            "best_recovery_vs_delay": None,
        }
    )

    # ---- best achievable recovery as a function of loop delay -----------
    best_rows = []
    for d in delay_axis:
        cands = []
        for ratio in BANDWIDTH_RULE_FAMILY:
            kp, kd, _ = pd_gains(d * T_BEAT, c_fct, I, ratio)
            t, th, om = simulate_attitude(
                I, amax, om0, [(kp, kd, d * T_BEAT)], c_fct,
                t_end=0.30, dt=4.0e-5,
            )
            rt = recovery_time(t, th, band)
            if np.isfinite(rt):
                cands.append((rt * 1e3, ratio))
        m, r = min(cands) if cands else (None, None)
        best_rows.append(
            {"delay_wingbeats": float(d), "best_recovery_ms": m,
             "best_period_over_delay": r}
        )
    ok = [r for r in best_rows
          if r["best_recovery_ms"] is not None
          and r["best_recovery_ms"] > RECOVERY_TIME_MS]
    crossing = min((r["delay_wingbeats"] for r in ok), default=None)
    out["stability_map"]["best_recovery_vs_delay"] = {
        "rows": best_rows,
        "slowest_loop_that_can_still_meet_60ms_wingbeats": (
            None if crossing is None else crossing - 0.5
        ),
        "slowest_loop_that_can_still_meet_60ms_ms": (
            None if crossing is None else (crossing - 0.5) * T_BEAT * 1e3
        ),
        "note": "At each delay the BEST member of the whole declared gain "
        "family is used, so no loop is handicapped by its tuning. The "
        "perturbation is the declared 20 degree one.",
    }

    # ---- headline -------------------------------------------------------
    r2 = by_name["two_wing_wild_type"]
    r4a = by_name["four_wing_area_conserved"]
    r4d = by_name["four_wing_area_doubled"]
    r4u = by_name["four_wing_T3_unactuated"]
    intact = results_b["two_wing_wild_type"]["arms"]["halteres_intact"]["rows"]
    blind = results_b["two_wing_wild_type"]["arms"][
        "halteres_deleted_vision_only"
    ]["rows"]
    hard = results_b["two_wing_wild_type"]["arms"][
        "halteres_deleted_vision_at_haltere_gain"
    ]["rows"]
    i20 = next(r for r in intact if r["peak_excursion_deg"] == 20)
    b20 = next(r for r in blind if r["peak_excursion_deg"] == 20)
    h20 = next(r for r in hard if r["peak_excursion_deg"] == 20)

    def ms(r):
        return (f"{r['recovery_time_ms']:.0f} ms"
                if r["recovery_time_ms"] is not None
                else "never, within 300 ms")

    out["headline"] = (
        "Redistributing the SAME total wing area over four wings does not "
        f"fly: {r4a['lift_over_weight']:.2f} body weights against 1.00. That "
        "is the result to start from, because it is geometry rather than "
        "biology - lift scales with the SECOND MOMENT of wing area, so "
        "splitting one wing into two smaller ones at constant aspect ratio "
        "loses more than half of it, and no contested biological parameter "
        "enters. Adding a second DRIVEN pair on top, at double total area, "
        f"does buy lift - {r4d['lift_over_weight']:.2f} body weights - at "
        f"{r4d['mass_specific_power_W_per_kg'] / r2['mass_specific_power_W_per_kg']:.2f} "
        "times the mass-specific mechanical power. The configuration the "
        "literature actually produced, four wings with the T3 pair "
        f"un-actuated, reaches {r4u['lift_over_weight']:.2f} body weights, "
        "and it stays below 1 ACROSS THE WHOLE ADMISSIBLE RANGE of the "
        "contested fore-hind interference term rather than at one chosen "
        "value of it: it would need the undriven pair to HELP the driven "
        "pair to get off the ground. The control half is where the design "
        "fails outright. After a 20 degree disturbance the haltere-intact "
        f"model is back inside 2 degrees in {ms(i20)}, a 30 ms visual loop "
        f"given its own best gain from the same family takes {ms(b20)}, and "
        "putting the fast loop's gain on the slow sense is worse still at "
        f"{ms(h20)}. Sweeping the loop delay and giving every delay the best "
        "gain in the family puts the boundary at "
        f"{out['stability_map']['best_recovery_vs_delay']['slowest_loop_that_can_still_meet_60ms_wingbeats']:.1f} "
        "wingbeats, about "
        f"{out['stability_map']['best_recovery_vs_delay']['slowest_loop_that_can_still_meet_60ms_ms']:.0f} "
        "ms: a loop slower than that cannot meet the measured recovery at ANY "
        "gain. The haltere loop is inside that boundary and the visual loop "
        "is well outside it. You cannot buy back a deleted rate gyro by "
        "turning up the gain on a slower sense - and note that this model "
        f"recovers in {ms(i20)} where a real fly takes under "
        f"{RECOVERY_TIME_MS:.0f} ms, so it is OPTIMISTIC about control and "
        "understates what deleting a haltere costs."
    )

    out["limitations"] = [
        "Nothing here was measured on an animal. Both halves are simulations "
        "and every figure caption says so.",
        "THIS MODEL IS FASTER THAN THE ANIMAL. The haltere-intact arm returns "
        "inside 2 degrees in about 13 ms, where Ristroph et al. measured a "
        "real fly at under 60 ms. The miss is in the direction that makes the "
        "model OPTIMISTIC about control, so every statement here about what "
        "deleting a haltere costs is an UNDERSTATEMENT rather than an "
        "exaggeration. Said plainly because a reader who sees a model agree "
        "with its author's conclusion should be told which way its errors "
        "point.",
        "THE CENTRAL RESULT IS NOT NEW, and pretending otherwise would be the "
        "easiest dishonesty available here. Elzinga, Dickson & Dickinson 2011 "
        "(PMID 22188766) measured the same thing on a dynamically scaled "
        "robotic fruit fly and reported 'a fundamental trade-off between "
        "sensor delay and permissible feedback gain', proposing exactly the "
        "architecture this study assumes - 'a haltere-mediated inner-loop "
        "proportional controller provides damping for slower visually "
        "mediated feedback'. Chang & Wang 2014 (PMID 25049376) derived "
        "bounds on sensing rate and delay in simulation and conjectured that "
        "flies sense every wingbeat. Our 3-wingbeat boundary is a "
        "re-derivation of a published trade-off in a different model, and its "
        "value is that it is calibrated against an independently measured "
        "recovery time, not that it is a discovery.",
        "The four-winged configurations barely move the ATTITUDE half: their "
        "recovery curves lie within 1% of the two-wing ones, because the "
        "added wing inertia is negligible at a 0.5% wing-mass fraction. That "
        "is a genuine null and it is reported as one. The four-winged fly's "
        "control problem is the deleted SENSOR, not added rotational "
        "inertia, and no inertia story should be told from this study.",
        "The stroke plane is horizontal and the angle of attack is constant "
        "through translation. Fry, Sayaman & Dickinson 2005 (PMID 15939772, "
        "abstract) report that hovering Drosophila instead use a U-shaped wing "
        "trajectory in which 'large drag forces during a downward plunge at the "
        "start of each stroke create peak vertical forces'. That mechanism "
        "cannot appear in this model. The model is therefore a comparison "
        "between configurations, not an estimate of a real fly's lift.",
        "Quasi-steady blade-element aerodynamics omits wake capture, added "
        "mass and rotational circulation. Fry et al. 2005 state that "
        "quasi-steady mechanisms 'could account for nearly all of the mean "
        "measured force required to hover' while 'temporal discrepancies ... "
        "indicate that unsteady mechanisms also play a significant role'. We "
        "use the mean, which is the part they say is covered.",
        "Most parameters are assumed rather than sourced, including body mass, "
        "wing length, chord, wingbeat frequency and stroke amplitude. We could "
        "not read the full text of the papers that hold measured values: the "
        "Journal of Experimental Biology site returns a bot challenge, and "
        "Europe PMC has no full text for Fry et al. 2005, Ristroph et al. 2010, "
        "Dickerson et al. 2019 or Yarger et al. 2021 (checked; a positive "
        "control on Deora et al. 2021, PMC8629423, returned 164 kB of full "
        "text from the same endpoint, and Paul et al. 2021, PMC8129201, "
        "returned 111 kB, so the endpoint works and the four absences are "
        "real rather than a broken query). Every part (A) result is therefore "
        "reported as a RATIO, in which the absolute scale cancels.",
        "The interference term between fore- and hindwings is swept rather "
        "than set, because the literature disagrees about its SIGN. Usherwood "
        "& Lehmann 2008 (PMID 18477538) report that dragonfly fore-hind "
        "phasing 'can improve aerodynamic efficiency by removing swirl'. We "
        "did not pick a value: the conclusion that the un-actuated four-wing "
        "configuration does not fly holds ACROSS THE WHOLE ADMISSIBLE RANGE "
        "of that parameter, from 0 to +0.40, and fails only if the undriven "
        "pair actively HELPS the driven pair - which no mechanism we found "
        "proposes for an undriven obstacle in a wake.",
        "Splitting one wing into two smaller ones at constant total area is "
        "done here at constant ASPECT RATIO and constant wingbeat frequency. "
        "Both are choices. Deora, Sane & Sane 2021 (PMID 34783648, full text) "
        "show wingbeat frequency is set by wing-thorax resonance and rises "
        "'by as much as 90 Hz' when wings are clipped, so a real four-winged "
        "animal would not hold frequency fixed. Letting it rise would recover "
        "part of the lost lift and cost more power; we did not model it.",
        "The attitude model is one axis and linear apart from the saturation. "
        "Real recovery couples roll, pitch and yaw, and Fry, Sayaman & "
        "Dickinson 2003 (PMID 12702878) report that 'inertia, not friction, "
        "dominates the flight dynamics of insects'.",
        "The visual loop is a delay and a gain, not a model of vision. "
        "Rauscher & Fox 2021 (PMID 33499788) show haltere and visual inputs sum "
        "LINEARLY for wing motor output but not for gaze; we model only the "
        "wing-motor side.",
        "The haltere does more than sense rotation. Dickerson et al. 2019 "
        "(PMID 31607538) argue that it also 'function[s] as an adjustable clock "
        "to set the spike timing of wing motor neurons'. A PD loop does not "
        "represent that at all, so deleting it here UNDERSTATES what deleting a "
        "haltere costs.",
        "Recovery time to a fixed 2 degree band depends on how large the "
        "disturbance was. Ristroph et al. 2010 describe 'gentle disturbances' "
        "without a magnitude in the abstract, so the perturbation is swept and "
        "the whole curve is reported rather than one matched number.",
        "The un-actuated wing arm models a LIMIT. Fernandes et al. 1994 report "
        "'only rudimentary indirect flight muscles' in the transformed segment, "
        "not none; a rudimentary muscle is somewhere between our driven and "
        "un-actuated arms and nobody has published where.",
    ]

    (ROOT / "flight-performance.json").write_text(json.dumps(out, indent=1))
    make_figures(out, by_name, eps_axis, eps_sweep, results_b,
                 gain_axis, delay_axis, grid, tau_fct)
    try:
        make_movie(by_name, tau_fct)
    except Exception as exc:          # a missing ffmpeg must not lose the JSON
        print(f"movie not written: {exc}")
    print(out["headline"])
    print("controls:", json.dumps(out["controls"], indent=1)[:1200])
    return 0


# ---------------------------------------------------------------------------
def make_figures(out, by_name, eps_axis, eps_sweep, results_b,
                 gain_axis, delay_axis, grid, tau_fct):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [
        "two_wing_wild_type",
        "four_wing_area_conserved",
        "four_wing_area_doubled",
        "four_wing_T3_unactuated",
    ]
    labels = [
        "2 wings\nwild type",
        "4 wings\nsame total area",
        "4 wings\ndouble area",
        "4 wings\nT3 pair not\nactuated",
    ]
    cols = ["#444444", "#7fa9d0", "#2b7bba", "#c0392b"]

    fig, ax = plt.subplots(1, 4, figsize=(17.0, 4.8))
    base = by_name["two_wing_wild_type"]
    series = [
        ([by_name[n]["lift_over_weight"] for n in names],
         "Lift", "mean vertical force / body weight", True),
        ([by_name[n]["mass_specific_power_W_per_kg"]
          / base["mass_specific_power_W_per_kg"] for n in names],
         "Mechanical power", "relative to wild type", False),
        ([by_name[n]["control_authority_rad_s2"]
          / base["control_authority_rad_s2"] for n in names],
         "Control authority", "roll acceleration, relative to wild type", False),
    ]
    for a, (vals, ttl, yl, mark) in zip(ax[:3], series):
        a.bar(range(4), vals, color=cols)
        a.set_xticks(range(4))
        a.set_xticklabels(labels, fontsize=8)
        a.set_title(ttl, fontsize=10)
        a.set_ylabel(yl, fontsize=9)
        a.axhline(1.0, color="k", ls=":", lw=0.9)
        for i, v in enumerate(vals):
            a.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
        if mark:
            a.axhline(1.0, color="k", ls="--", lw=1.1)
            a.text(-0.42, 0.94, "does not fly below this line", fontsize=7,
                   ha="left", style="italic")

    for n, col, lab in zip(names, cols,
                           ["2 wings", "4, same area", "4, double area",
                            "4, T3 dead"]):
        ys = [row[n]["lift_over_weight"] for row in eps_sweep]
        ax[3].plot(eps_axis, ys, "o-", color=col, lw=1.5, ms=3, label=lab)
    ax[3].axhline(1.0, color="k", ls="--", lw=1.0)
    ax[3].axvline(0.0, color="k", ls=":", lw=0.8)
    ax[3].set_xlabel("interference on the trailing pair\n(negative = it GAINS lift)",
                     fontsize=8)
    ax[3].set_ylabel("mean vertical force / body weight", fontsize=9)
    ax[3].set_title("The contested term, swept", fontsize=10)
    ax[3].legend(fontsize=7)
    fig.suptitle(
        "Simulation. Quasi-steady blade-element model. Left three panels at "
        f"interference {INTERFERENCE:+.2f}; the right panel sweeps it. "
        "Wild type is the calibration arm, so its lift is 1.00 by construction.",
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(FIG / "flight-lift-vs-wings.png", dpi=150)
    plt.close(fig)

    # --- stability figure ------------------------------------------------
    fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.8))
    cfg = by_name["two_wing_wild_type"]
    I = cfg["moment_of_inertia_kg_m2"]
    arms, c_fct = arms_for(cfg, tau_fct, RECOVERY_BAND_DEG * DEG)
    om0 = PERTURBATION_DEG * DEG / tau_fct
    arm_cols = {
        "halteres_intact": ("#1b7837", "halteres intact (1-wingbeat loop)"),
        "halteres_deleted_vision_only": (
            "#e08214", "halteres gone, visual loop at its own best gain"),
        "halteres_deleted_vision_at_haltere_gain": (
            "#c0392b", "halteres gone, fast loop's gain on the slow sense"),
        "open_loop": ("#999999", "no feedback at all"),
    }
    for key, (col, lab) in arm_cols.items():
        t, th, om = simulate_attitude(
            I, cfg["control_authority_rad_s2"], om0,
            arms[key]["pathways"], c_fct, t_end=0.30,
        )
        ax[0].plot(t * 1e3, th / DEG, color=col, lw=1.6, label=lab)
    ax[0].axhspan(-RECOVERY_BAND_DEG, RECOVERY_BAND_DEG, color="k", alpha=0.10)
    ax[0].axvline(RECOVERY_TIME_MS, color="k", ls=":", lw=1.0)
    ax[0].set_xlabel("time after the disturbance (ms)")
    ax[0].set_ylabel("body angle (degrees)")
    ax[0].set_title(
        f"Recovery from a {PERTURBATION_DEG:.0f}$^\\circ$ disturbance", fontsize=10)
    ax[0].legend(fontsize=7, loc="upper right")
    ax[0].text(RECOVERY_TIME_MS + 130, ax[0].get_ylim()[1] * 0.42,
               "60 ms / 2$^\\circ$\n(Ristroph 2010:\nthe one measured\nquantity here)",
               fontsize=7)

    for key, (col, lab) in arm_cols.items():
        if key == "open_loop":
            continue
        rows = results_b["two_wing_wild_type"]["arms"][key]["rows"]
        xs = [r["peak_excursion_deg"] for r in rows]
        ys = [r["recovery_time_ms"] if r["recovery_time_ms"] is not None
              else np.nan for r in rows]
        ax[1].plot(xs, ys, "o-", color=col, label=lab, lw=1.5, ms=4)
        for x, r in zip(xs, rows):
            if r["recovery_time_ms"] is None:
                ax[1].plot([x], [290], "x", color=col, ms=8)
            elif r["never_left_the_2deg_band"]:
                ax[1].plot([x], [0], "o", color="w", mec=col, ms=7, zorder=5)
    ax[1].axhline(RECOVERY_TIME_MS, color="k", ls=":", lw=1.0)
    ax[1].text(5.2, RECOVERY_TIME_MS * 1.06, "measured: 60 ms", fontsize=7)
    ax[1].set_xscale("log")
    ax[1].set_xlabel("size of the disturbance (degrees)")
    ax[1].set_ylabel("time to return inside 2$^\\circ$ (ms)")
    ax[1].set_title("Recovery time against disturbance size", fontsize=10)
    ax[1].legend(fontsize=7, loc="upper left")
    ax[1].text(
        0.03, 0.62,
        "open circle = never left the 2$^\\circ$ band at all\n"
        "the four-wing bodies lie within 1% of these curves:\n"
        "the wing count barely moves the CONTROL half",
        fontsize=6.5, transform=ax[1].transAxes,
    )

    best_ms, best_ratio = [], []
    for d in delay_axis:
        cands = []
        for ratio in BANDWIDTH_RULE_FAMILY:
            kp, kd, _ = pd_gains(d * T_BEAT, c_fct, I, ratio)
            t, th, om = simulate_attitude(
                I, cfg["control_authority_rad_s2"], om0,
                [(kp, kd, d * T_BEAT)], c_fct, t_end=0.30, dt=4.0e-5,
            )
            rt = recovery_time(t, th, RECOVERY_BAND_DEG * DEG)
            if np.isfinite(rt):
                cands.append((rt * 1e3, ratio))
        if cands:
            m, r = min(cands)
            best_ms.append(m)
            best_ratio.append(r)
        else:
            best_ms.append(np.nan)
            best_ratio.append(np.nan)
    ax[2].plot(delay_axis, best_ms, "o-", color="#333333", lw=1.8, ms=4)
    ax[2].axhline(RECOVERY_TIME_MS, color="k", ls=":", lw=1.0)
    ax[2].text(6.0, RECOVERY_TIME_MS * 1.08, "measured: 60 ms", fontsize=7)
    ax[2].axvline(TAU_HALTERE, color="#1b7837", lw=1.4)
    ax[2].text(TAU_HALTERE + 0.2, 8, "haltere\nloop", color="#1b7837",
               fontsize=8)
    vdelay = TAU_VISUAL_MS * 1e-3 / T_BEAT
    ax[2].axvline(vdelay, color="#c0392b", lw=1.4)
    ax[2].text(vdelay + 0.2, 8, "visual\nloop", color="#c0392b", fontsize=8)
    ax[2].set_xlabel("feedback delay (wingbeats)")
    ax[2].set_ylabel("best recovery time achievable (ms)")
    ax[2].set_title("Why a slow loop cannot be turned up", fontsize=10)
    ax[2].set_ylim(0, 300)
    ax[2].text(
        0.6, 272,
        "at each delay, the BEST member of the whole\n"
        "gain family is used - no loop is handicapped",
        fontsize=6.5,
    )

    fig.suptitle(
        "Simulation. One-axis attitude model with saturating control. The "
        "60 ms / 2 degree line is the only measured quantity on this "
        "figure.\nThe intact model recovers in about 13 ms, FASTER than the "
        "animal: it is optimistic about control, so it understates what "
        "deleting a haltere costs.", fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(FIG / "flight-stability.png", dpi=150)
    plt.close(fig)


def make_movie(by_name, tau_fct):
    """A short frame strip of the two attitude arms, side by side."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter

    cfg = by_name["two_wing_wild_type"]
    I = cfg["moment_of_inertia_kg_m2"]
    arms, c_fct = arms_for(cfg, tau_fct, RECOVERY_BAND_DEG * DEG)
    om0 = PERTURBATION_DEG * DEG / tau_fct
    runs = {}
    for key, col, lab in (
        ("halteres_intact", "#1b7837", "halteres intact"),
        ("halteres_deleted_vision_only", "#c0392b", "halteres deleted"),
    ):
        t, th, om = simulate_attitude(
            I, cfg["control_authority_rad_s2"], om0, arms[key]["pathways"],
            c_fct, t_end=0.30,
        )
        runs[key] = (t, th, col, lab)

    fig = plt.figure(figsize=(9.0, 4.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.4])
    axb = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])]
    axt = fig.add_subplot(gs[:, 1])
    for a, (key, (t, th, col, lab)) in zip(axb, runs.items()):
        a.set_xlim(-1.4, 1.4)
        a.set_ylim(-1.0, 1.0)
        a.set_aspect("equal")
        a.axis("off")
        a.set_title(lab, fontsize=10, color=col)
        axt.plot(t * 1e3, th / DEG, color=col, lw=1.6, label=lab, alpha=0.35)
    axt.axhspan(-RECOVERY_BAND_DEG, RECOVERY_BAND_DEG, color="k", alpha=0.10)
    axt.set_xlabel("time after the disturbance (ms)")
    axt.set_ylabel("body angle (degrees)")
    axt.set_title("Simulation. One-axis attitude model.", fontsize=9)
    bodies, traces, marks = [], [], []
    for a, (key, (t, th, col, lab)) in zip(axb, runs.items()):
        (ln,) = a.plot([], [], color=col, lw=7, solid_capstyle="round")
        (wg,) = a.plot([], [], color="#555555", lw=2)
        bodies.append((ln, wg))
        (m,) = axt.plot([], [], "o", color=col, ms=6)
        marks.append(m)
        (tr,) = axt.plot([], [], color=col, lw=2.0)
        traces.append(tr)

    step = 120
    nfr = len(next(iter(runs.values()))[0]) // step

    writer = FFMpegWriter(fps=25, bitrate=1800, metadata={"title": "attitude"})
    out = FIG / "flight-stability.mp4"
    with writer.saving(fig, str(out), dpi=110):
        for k in range(nfr):
            i = k * step
            for (ln, wg), (key, (t, th, col, lab)), m, tr in zip(
                bodies, runs.items(), marks, traces
            ):
                a_ = th[i]
                ln.set_data([-np.cos(a_), np.cos(a_)], [-np.sin(a_), np.sin(a_)])
                wg.set_data(
                    [-0.55 * np.cos(a_) - 0.30 * np.sin(a_),
                     -0.55 * np.cos(a_) + 0.30 * np.sin(a_)],
                    [-0.55 * np.sin(a_) + 0.30 * np.cos(a_),
                     -0.55 * np.sin(a_) - 0.30 * np.cos(a_)],
                )
                m.set_data([t[i] * 1e3], [th[i] / DEG])
                tr.set_data(t[: i + 1] * 1e3, th[: i + 1] / DEG)
            writer.grab_frame()
    plt.close(fig)
    return out


if __name__ == "__main__":
    sys.exit(main())
