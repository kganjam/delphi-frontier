#!/usr/bin/env python3
"""The one place the design's body and lifting-surface numbers are defined.

WHY THIS FILE EXISTS. The expression

    S = 1.4e-4 * (2.6 / 4.0) ** 2 * 2.65

appeared in NINE analysis modules, re-typed each time, and three of them labelled the result
differently: "1.57 cm2 of fin" (flapping_power_budget), "m2 of lifting surface"
(flapping_flight), "m^2, the 2.65-fold fin" (flight_in_wind). The other six said nothing. There
was no place where the quantity was defined, so there was nowhere for those three definitions to
conflict and nothing to notice they did (claim 1157).

WHAT THE PIECES ARE, each traced rather than asserted:

    1.4e-4 m^2   the WHOLE-BODY DORSAL SILHOUETTE of a ~0.4 g adult, stated in
                 analysis/lift_budget.py:36 as "~1.4 cm^2 whole-body dorsal silhouette" and used
                 in docs/FINDINGS.md as the "available" area against which the design's 26.7 cm^2
                 requirement is 19.1x in area and 4.37x linear. It is NOT a fin area: this
                 project's claims 984 and 986 put wild-type pectoral fin length/SL near 0.22,
                 about 9 mm on a 40 mm fish, for a paired area of order 4e-5 m^2 (claim 1155).
    4.0e-4 kg    the ~0.4 g adult mass the same documents use.
    (2.6/4.0)    a body-length rescale from the 4.0 cm fish those constants describe to the
                 2.6 cm fish the dynamics modules simulate. Areas take the square, masses the cube.
    2.65         THE UNRESOLVED FACTOR. Claim 988 ties it to the achieved fin-area ratio of
                 claims 529 and 542, and claim 1082 derives 2.666 as (fin length / SL) ** 1.33 --
                 an allometry OF THE FIN. Applying it to a BODY SILHOUETTE is a category error
                 unless S is meant as a lumped body-plus-fins lifting surface, which would make
                 a factor near 2.65 a modelling choice rather than a measured ratio. No source
                 in this repository says which. The factor is preserved here EXACTLY as the nine
                 modules had it, because changing it would silently move every result that
                 depends on it; naming the problem is this file's job, fixing it is not.

SO `S_LIFTING` BELOW IS NOT ENDORSED AS "FIN AREA". It is the number those nine modules have
always used, now computed once, with its three incompatible labels replaced by one honest
account of what is known and what is not.
"""

from __future__ import annotations

#: Whole-body dorsal silhouette of the ~0.4 g, 4.0 cm adult (lift_budget.py:36, FINDINGS.md).
SILHOUETTE_4CM_M2 = 1.4e-4
#: The ~0.4 g adult mass those documents use.
MASS_4CM_KG = 4.0e-4
#: Body length the dynamics modules simulate, over the length those constants describe.
LENGTH_RATIO = 2.6 / 4.0
#: See the docstring. A fin allometry applied to a body silhouette; preserved, not endorsed.
FIN_RATIO_UNRESOLVED = 2.65

#: Mass at the simulated body length. Masses scale with the cube of length.
MASS_KG = MASS_4CM_KG * LENGTH_RATIO ** 3
#: The lifting area those nine modules use. Areas scale with the square of length.
S_LIFTING_M2 = SILHOUETTE_4CM_M2 * LENGTH_RATIO ** 2 * FIN_RATIO_UNRESOLVED
