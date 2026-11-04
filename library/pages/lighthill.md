---
title: Lighthill elongated-body theory
label: law-lighthill
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-lighthill
\eta = \frac{1 + U/V}{2}, \qquad \langle T \rangle = \left\langle \left[ m w \dot{y} - \tfrac{1}{2} m w^2 x' \right]_{s=\mathrm{tail}} \right\rangle, \qquad m = \rho \pi h^2
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `eta` | 1 | dimensionless | small-amplitude Froude efficiency of an undulatory swimmer |
| `U` | L/T | m/s | forward swimming speed |
| `V` | L/T | m/s | speed of the backward-travelling body wave; thrust requires V greater than U |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `lighthill_recommended_speed_ratio` | 0.8 | Lighthill 1960 advises passing a wave down the body at around 5/4 of the desired swimming speed, so U/V = 0.8, giving eta = (1 + 0.8)/2 = 0.90. The 5/4 is retrieved from the abstract; the small-amplitude efficiency formula it is substituted into is a remembered textbook result. |
| `slenderness_criterion` | 5 | The theory applies if the body wavelength exceeds 5 times the tail span s (Lighthill 1970). This is the entry's own domain test and it is checkable from kinematics alone. |
| `elongation_floor` | 0.1 | Eloy 2012: animals with tail-half-span to length ratio h/L below 0.1 -- eels and knifefish -- will not in general meet the criterion. This is the counter-intuitive bound: slender-body theory does NOT suit the most slender animals. |

## Why it holds

In inviscid slender-body theory the water near each cross-section is accelerated laterally as the body passes, and the reaction is carried as added mass m = rho*pi*h^2 per unit length. All the momentum that matters is shed at the trailing edge, so the mean thrust depends only on conditions AT THE TAIL, which is why the theory is so economical: the whole body's motion enters through one station. Thrust requires the body wave to travel backwards faster than the animal moves forwards, V greater than U, and the efficiency formula is the fraction of the imparted energy that does not end up in the wake.

## Where it holds

- **reynolds**: high, inviscid outer flow
- **geometry**: slender body whose cross-section changes slowly along its length
- **kinematics**: wavelength greater than 5 times the tail span
- **amplitude**: The 1960 theory is small-amplitude; Lighthill 1971 extends it to fish motions of arbitrary amplitude.


:::{danger} Where it breaks
It fails at BOTH ends of the shape range, which is the fact most likely to catch a designer out. At the slender end, Eloy shows elongated fish with h/L below 0.1 -- eels and knifefish -- do not meet the slow-variation criterion, contradicting the intuition that slender-body theory suits eels best. At the other end Lighthill 1970 says the theory ceases to be applicable to widened, swept-back lunate tails, and Eloy adds that it fails for scombrids, dolphins and sharks, which all share a large-aspect-ratio tail. So it is clean only for the MIDDLE range of carangiform shapes, and both the eel and the tuna are outside it. Separately, Lighthill 1971 flags substantial enhancement of drag through boundary-layer thinning in a dace comparison: drag on an undulating body is not drag on a rigid one, so an efficiency computed here cannot be combined with a rigid-body drag coefficient. Rays, boxfish and other non-undulatory body plans lie outside its geometric assumptions altogether.
:::

## Worked examples

**Lighthill's own recommendation**

```
V = 1.25*U  ->  U/V = 0.8  ->  eta = (1 + 0.8)/2 = 0.90
```

- value: `0.9`

- evidence: **derived**

**Tursiops truncatus (bottlenose dolphin)**

```
U/V = 0.52 (Eloy table)  ->  eta = (1 + 0.52)/2 = 0.76
```

- value: `0.76`

- ILLUSTRATIVE ONLY. The dolphin's lunate tail puts it outside the theory's domain by the theory's own statement, so this number is an example of the calculation, not a result about dolphins. It is kept rather than dropped because applying the formula where it does not belong is the error the entry exists to prevent, and it is easier to recognise with a worked instance.

- evidence: **derived**

:::{seealso} Contested
- Eloy 2012 argues the domain is narrower than usually assumed at both the slender and the high-aspect-ratio ends; this is a sharpening of the domain rather than a rival theory.
:::

## Sources

| Citation | Read-level |
|---|---|
| Lighthill MJ (1960) J Fluid Mech 9:305-317, Note on the swimming of slender fish, doi 10.1017/S0022112060001110 | `abstract` |
| Lighthill MJ (1970) J Fluid Mech 44:265-301, Aquatic animal propulsion of high hydromechanical efficiency, doi 10.1017/S0022112070001830 | `abstract` |
| Lighthill MJ (1971) Proc R Soc B 179:125-138, Large-amplitude elongated-body theory of fish locomotion, doi 10.1098/rspb.1971.0085 | `abstract` |
| Eloy C (2012) J Fluids Struct 30:205-218, doi 10.1016/j.jfluidstructs.2012.02.008 (eq. 4) | `full-text-preprint` |


---

*Generated from [`library/laws/lighthill.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/lighthill.yaml). Do not edit this page; edit the YAML.*
