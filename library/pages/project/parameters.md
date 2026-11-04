---
title: Parameters
---

Every simulation parameter with its provenance. A parameter is a **posterior**, not a number: the route that produced it, the estimates it rests on, and the structural assumptions that license it are all part of the value.

## The dependency graph

```{mermaid}
graph TD
  CL_max["CL_max"]
  m_body["m"]
  S_wing["S"]
  U_burst["U_b"]
  V_takeoff["V_to"]
  CL_max -->|input to formula| V_takeoff
  m_body -->|input to formula| V_takeoff
  S_wing -->|input to formula| V_takeoff
  m_body -->|proxy for| S_wing
```

*An arrow runs from an input to the estimate that uses it.*

## `CL_max` — Maximum lift coefficient at Re ~3e3

How much lift a thin cambered membrane can make at this Reynolds number. Was the single largest error in the project.

| | |
|---|---|
| Value | **1.07 dimensionless** (range 0.9–1.15, *observed-range*) |
| Derivation | 🔵 borrowed from another system |
| How | Measured thin-plate polars at Re 7e2-1e4 from the low-Re literature. REPLACED an earlier 0.6 taken from a thick NACA 0012 at Re ~2e4 -- a real value applied in the wrong regime, caught by adversarial challenge. |
| Conditions | Thin cambered plate, Re 7e2-1e4, steady attached flow |
| Source | S2 + adversarial challenge *[search-summary]* |

## `m` — Adult zebrafish body mass

Standard adult Danio rerio.

| | |
|---|---|
| Value | **0.0004 kg** (range 0.0003–0.0005, *observed-range*) |
| Derivation | 🟢 measured |
| How | Standard reference value for adult Danio. |
| Conditions | Adult, ~4 cm SL |
| Source | literature *[abstract]* |

## `S` — Wing planform area

Area of the designed pectoral wing. NEVER MEASURED in any enlarged-fin zebrafish -- the central geometric input is an extrapolation.

| | |
|---|---|
| Value | **0.000192 m^2** — **no interval** |
| Derivation | 🟠 assumed |
| How | S = b^2/AR with b = 1 body length (0.031 m) and AR = 5. Both chosen, not measured. |
| Conditions | 1-BL span, AR 5 |
| Source | S28 assumption |

**Rests on:**

- `m_body` (proxy for) — span taken as one body length, which is tied to mass by assumed isometry

:::{warning} Structural assumption: Fin and body proportions scale ISOMETRICALLY when enlarged
**Evidence:** assumed. **Alternatives:** Allometric scaling, in which enlarged fins change proportion; or a hard developmental ceiling on fin size..
**If wrong:** If growth is allometric, the assumed 1-BL span at AR 5 is unreachable and the wing area is wrong at its root.
:::

## `U_b` — Measured adult fast-start peak speed

What the animal can actually do. The denominator of the whole deficit.

| | |
|---|---|
| Value | **0.842 m/s** (range 0.45–1.38, *measured-ci*) |
| Derivation | 🟢 measured |
| How | Two INDEPENDENT routes agreeing: derived from a measured Reynolds number (Danos & Lauder 2012) and measured directly from high-speed video (Miln et al. 2021, n=50). The derived value sits inside the measured range. |
| Conditions | Adult, 120-1000 fps video |
| Source | Danos & Lauder 2012; Miln et al. 2021 *[full-text]* |

## `V_to` — Required water-exit speed

The speed at which the designed wing first carries body weight. The single number the whole flight verdict turns on.

| | |
|---|---|
| Value | **4.37 m/s** (range 4.22–4.69, *sensitivity-bound*) |
| Derivation | 🟡 derived |
| How | V = sqrt(2mg/(rho*S*CL_max)). Recomputed from the corrected CL_max; the interval spans the measured CL_max range 0.93-1.15 rather than any statistical CI. |
| Conditions | Sea-level air, steady flight, 1-body-length span at AR 5 |
| Source | S28-organism.md |

**Rests on:**

- `CL_max` (input to formula) — V scales as CL_max^-0.5, so the 0.6 -> 1.07 correction moved V from 5.84 to 4.37 m/s
- `m_body` (input to formula) — V scales as m^0.5
- `S_wing` (input to formula) — V scales as S^-0.5; S is ASSUMED, so this is the weakest input

:::{warning} Structural assumption: Lift follows the STEADY lift equation L = 0.5*rho*V^2*S*CL
**Evidence:** assumed. **Alternatives:** Unsteady mechanisms -- leading-edge vortex, clap-and-fling, rotational lift -- which at Re ~1e3 can exceed steady CL_max severalfold..
**If wrong:** If unsteady lift is available, the required speed falls and the flight verdict could change. This is the single most consequential structural assumption in the project and it is UNTESTED.
:::

:::{warning} Structural assumption: The wing is treated as RIGID for the lift calculation
**Evidence:** assumed. **Alternatives:** An aeroelastic wing that twists or flutters under load, which S6 suggests is the realistic case for a lepidotrichial ray..
**If wrong:** A compliant wing sheds lift as it deforms, so the computed takeoff speed is a LOWER bound and the real requirement is higher.
:::
