---
title: Froude propulsive efficiency
label: law-froude-efficiency
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-froude-efficiency
\eta_F = \frac{2U}{U + V_j} = \frac{2}{1 + V_j/U}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `eta_F` | 1 | dimensionless | useful propulsive power divided by total power imparted to the fluid |
| `U` | L/T | m/s | forward speed of the body |
| `V_j` | L/T | m/s | speed of the jet or wake far downstream, in the body frame |

## Why it holds

Actuator-disc momentum theory. Thrust is the rate of momentum addition, mdot*(V_j - U), while the kinetic energy wasted in the wake rises with (V_j - U)^2. Efficiency therefore favours accelerating a LARGE mass of fluid a LITTLE, which is the single most portable result in propulsion and the reason large slow propulsors beat small fast ones at equal thrust. The formula is exact within the theory; it is the theory that is approximate.

## Where it holds

- **flow**: steady, quasi-one-dimensional momentum exchange with a well-defined far wake
- **notes**: Applies to a continuously acting propulsor. Eloy's more general definition, eta = D*U / (D*U + mean shed power), reduces to this one in the steady case and is what is actually used for undulatory swimmers.


:::{danger} Where it breaks
Unsteady and pulsed jets break the premise that there is a steady far wake whose momentum flux can be written as mdot*(V_j - U). Squid and jellyfish propel themselves with discrete vortex rings, which can carry MORE impulse per unit energy than the steady theory allows, so the formula is not merely inaccurate there but can underestimate the achievable efficiency. It also says nothing about how much thrust is available, only about the price of it: a design can sit at eta_F = 0.95 and produce no useful thrust at all. And it is blind to viscous and profile losses on the propulsor itself, so the number it returns is an upper bound on a part of the budget rather than a system efficiency.
:::

## Worked examples

**generic propulsor, two jet-speed ratios**

```
V_j = 1.5*U : eta_F = 2/(1 + 1.5) = 2/2.5 = 0.80
V_j = 3.0*U : eta_F = 2/(1 + 3.0) = 2/4   = 0.50

```

- value: `0.8`

- Doubling the excess jet speed costs 30 efficiency points. This is the whole content of the law as a design check, and it is exact.

- evidence: **derived**

:::{seealso} Contested
- Not contested as mathematics. What is contested in biology is whether a given animal's wake is steady enough for it to apply -- see Lighthill elongated-body theory for the undulatory case, where the shed power is computed rather than assumed.
:::

## Sources

| Citation | Read-level |
|---|---|
| Actuator-disc momentum theory is standard; no primary source was retrieved for it in this compilation. | `remembered` |
| Eloy C (2012) J Fluids Struct 30:205-218, doi 10.1016/j.jfluidstructs.2012.02.008, eq. 12 for the general definition | `full-text-preprint` |


---

*Generated from [`library/laws/froude-efficiency.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/froude-efficiency.yaml). Do not edit this page; edit the YAML.*
