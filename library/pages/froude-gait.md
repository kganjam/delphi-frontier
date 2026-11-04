---
title: Froude number and the walk-run transition
label: law-froude-gait
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-froude-gait
\mathrm{Fr} = \frac{U^2}{g L}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `Fr` | 1 | dimensionless | ratio of centripetal to gravitational acceleration for an inverted pendulum |
| `U` | L/T | m/s | forward speed |
| `g` | L/T^2 | m/s^2 | gravitational acceleration |
| `L_leg` | L | m | leg length or hip height |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `biped_transition` | 0.5 | Bipeds switch from walking to running at approximately the same Froude number, 0.5, INCLUDING at reduced gravity (Kram, Domingo & Ferris 1997). The reduced-gravity result is what makes this a dynamical constant rather than a speed in disguise. No confidence interval was retrieved. |
| `pendular_walking_ceiling` | 1 | Derived, not measured: at Fr = 1 the centripetal acceleration needed to keep the body on a circular arc over a straight stance leg equals g, so the foot can no longer push. Above it, pendular walking is impossible without changing the mechanics. |
| `quadruped_gait_boundaries` | unknown | Walk-trot near 0.5 and trot-gallop near 2-3 are REMEMBERED, not retrieved. They are not in the retrieved abstract of Alexander & Jayes 1983 and are deliberately given no value here. |

## Why it holds

Dynamic similarity. Alexander & Jayes propose that animals of different size move in geometrically similar fashion when they travel at equal Froude number. The group itself is the ratio of the centripetal acceleration U^2/L required to vault over a straight stance limb to the gravitational acceleration available to supply it, so it falls out of inverted-pendulum walking rather than being fitted to data.

## Where it holds

- **taxa**: cursorial mammals
- **mass min kg**: 5
- **notes**: Alexander & Jayes call the hypothesis tenable for cursorial mammals and note that most mammals above 5 kg are of this type. The transition value 0.5 is retrieved for BIPEDS specifically.


:::{danger} Where it breaks
Non-cursorial and small mammals fall outside the hypothesis by its authors' own statement, so the group does not predict their gait boundaries. Race walkers routinely exceed Fr = 1 by changing the mechanics -- pelvic rotation lowers the centre of mass excursion so the straight-leg vault is no longer the constraint -- which shows the ceiling bounds a MECHANISM, not an animal. Most importantly, equal Froude number gives geometrically similar gait and says nothing whatever about metabolic cost, so it must not be used to infer efficiency or a preferred speed: a design can sit at the right Fr and be energetically absurd. The quadruped boundaries in wide circulation are not supported by any source retrieved here.
:::

## Worked examples

**Homo sapiens, leg length 0.9 m**

```
walk-run transition at Fr = 0.5 : U = sqrt(0.5 * 9.81 * 0.9) = 2.10 m/s
pendular walking ceiling Fr = 1 : U = sqrt(9.81 * 0.9)       = 2.97 m/s
on Mars, g = 3.73 m/s^2, Fr=0.5 : U = sqrt(0.5 * 3.73 * 0.9) = 1.30 m/s

```

- value: `2.1`

- The Mars line is the falsifiable one, and it is the direction Kram et al. tested experimentally under reduced gravity. Leg length 0.9 m and Martian g are remembered inputs.

- evidence: **derived**

:::{seealso} Contested
- Froude number for gait and Froude PROPULSIVE EFFICIENCY share a name and nothing else. They are different quantities with different definitions and different domains; see the separate entry.
:::

## Sources

| Citation | Read-level |
|---|---|
| Alexander RMcN, Jayes AS (1983) J Zool 201:135-152, A dynamic similarity hypothesis for the gaits of quadrupedal mammals, doi 10.1111/j.1469-7998.1983.tb04266.x | `abstract` |
| Kram R, Domingo A, Ferris DP (1997) J Exp Biol 200:821-826, Effect of reduced gravity on the preferred walk-run transition speed, doi 10.1242/jeb.200.4.821 | `abstract` |


---

*Generated from [`library/laws/froude-gait.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/froude-gait.yaml). Do not edit this page; edit the YAML.*
