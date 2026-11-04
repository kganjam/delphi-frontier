# Replication 288: re-derivation of Replication 260 (passive attitude modes of an engineered 0.4 g zebrafish glider)

## Independence disclosure (read this first)

The task prompt names one place for the inputs: `replicate-260.md` on branch `claude/zebrafish-glider-attitude-fpeh9d`. That file **is** the derivation under test. Its inputs table, its arithmetic and its result all sit on the same page, so I could not read the inputs without also seeing the recorded value. I stopped reading primary content at that point. I did not open any `challenge-*zebrafish*` or `harvest:*` branch, and I did not open the original claim-260 derivation.

Because of this, the derivation below is **not blind**. To get some independence back, I did three things:
1. Re-ran every step of the central-case arithmetic by hand-coded script, which checks the arithmetic only.
2. Re-derived the two governing formulas (short-period stiffness and strip-theory roll damping) from first principles.
3. Built my own Monte Carlo with input choices that differ where I think replication 260 is weak: body pitch inertia, cross-section ranges, and the apparent (added) inertia of the air in roll. Replication 260 omits the added air inertia.

Treat the agreement reported here as weaker evidence than two blind derivations would give.

**Every number below is CALCULATED from a linear rigid-body model with assumed geometry. None of it is an observation.** No zebrafish glider exists, and the fin geometry is a design assumption.

## Inputs

| Input | Value / range I used | Source | Read-level |
|---|---|---|---|
| Mass m | 0.4 g | claim text, via replicate-260.md | full-text (of replicate-260.md) |
| Body length L | 3.0–3.8 cm | My assumption, from general knowledge that adult zebrafish are about 3–4 cm. Replicate-260 cites FishBase W = 0.00977·TL^3.04; I did **not** verify this. | none (my memory) / FishBase: could-not-access (not attempted) |
| Body height h, width w | h = 0.18–0.24 L, w = 0.09–0.13 L | assumption (laterally compressed body) | none |
| Fin span b, chord c | 4–7 cm, 0.8–1.4 cm | design assumption, same ranges as replicate-260 so the two are comparable | none |
| Fin mass fraction | 3–8 % | assumption | none |
| C_L (glide) | 0.5–1.0 | assumption | none |
| Lift slope a | 2πAR/(AR+2) | standard finite-wing approximation, from memory | textbook, not re-read |
| Static margin SM | 0.05–0.25 c | assumption; the dominant uncertainty for pitch | none |
| Pitch inertia I_yy | m L² × k, with k from 1/20 (prolate ellipsoid) to 1.3/12 (rod plus tail add-on) | my choice; replicate-260 used rod ×1.0–1.3 only | none |
| Added air inertia in roll | ρ π c²/4 · b³/12 (flat-plate apparent mass, integrated over span) | standard potential-flow result, from memory | textbook, not re-read |
| ρ, g | 1.2 kg m⁻³, 9.81 m s⁻² | standard | n/a |

Literature-search scope: none. I made no web searches or fetches. Every physical constant and formula comes from memory and is labelled that way above.

## Derivation

**Glide speed.** In trimmed glide, lift equals weight, so q S C_L = W. That gives V = √(2W/(ρ S C_L)). A useful identity follows: q S = W / C_L, which does not depend on the fin area.

**Pitch stiffness.** M_α = q S a · (SM·c) = (W/C_L) · a · c · SM.
The undamped short-period frequency is f = (1/2π)·√(M_α / I_yy).

**Roll damping (strip theory, rectangular fin).** At roll rate p, a strip at span station y sees Δα = p·y/V. Its rolling moment is y·q c a Δα dy. Integrating y² over ±b/2 gives b³/12, so:
L_p = q c a b³ / (12 V) = ρ V S a b² / 24. This matches replicate-260's formula.
The roll-rate time constant is τ = I_xx / L_p.

**Roll inertia.** I_xx is the sum of three terms:
- body: (m − m_f)(h² + w²)/12
- fins: m_f b²/12
- added air: ρ π c²/4 · b³/12

## Arithmetic

### Check of replicate-260's central case

The central case is L = 3.1 cm, b = 5.5 cm, c = 1.1 cm, C_L = 0.75, fin fraction 5 %.

- S = 6.05e-4 m²; AR = 5.0; a = 4.488 /rad
- W = 3.924e-3 N; V = √(7.848e-3 / 5.445e-4) = **3.796 m/s**; q = 8.648 Pa; q S = W/C_L = 5.232e-3 N
- I_yy = 4e-4 × 0.031²/12 × 1.15 = 3.684e-8 kg m²
- At SM = 0.10: M_α = 5.232e-3 × 4.488 × 0.011 × 0.10 = 2.583e-5 N m/rad. ω = √(701) = 26.5 rad/s, so **f = 4.21 Hz**.
  Across SM 0.02 / 0.05 / 0.10 / 0.15 / 0.25: f = 1.88 / 2.98 / 4.21 / 5.16 / 6.66 Hz.
- Z_α/(mV) = g a / (C_L V) = 9.81 × 4.488 / (0.75 × 3.796) = **15.5 s⁻¹**. Replicate-260 wrote "≈14"; my value is about 10 % higher. With ω = 26.5, this term alone gives ζ ≈ 0.29, which is consistent with their ζ ≈ 0.2–0.3.
- L_p = 1.2 × 3.796 × 6.05e-4 × 4.488 × 0.055² / 24 = **1.559e-6 N m s**
- Roll inertia components:
  - I_xx body = 1.522e-9 kg m²
  - I_xx fins = 5.042e-9 kg m²
  - I_xx air (added) = 1.2 × π × 0.011²/4 × 0.055³/12 = **1.581e-9 kg m²**
- τ without added air = 6.563e-9 / 1.559e-6 = **4.21 ms**. This reproduces replicate-260's value.
- τ with added air = 8.144e-9 / 1.559e-6 = **5.22 ms**, which is +24 %.

Re-running replicate-260's own script (seed 1, N = 2e5) reproduces their table exactly: V 3.0 / 3.9 / 5.0 m/s; f 3.1 / 5.0 / 7.2 Hz; τ 2.7 / 4.6 / 7.5 ms. This checks their code, not their physics.

### My Monte Carlo

Uniform draws over my input ranges, N = 2×10⁵, seed 288. All values are calculated.

| Quantity | 5 % | 50 % | 95 % |
|---|---|---|---|
| V (m/s) | 3.04 | 3.87 | 5.01 |
| Pitch short-period f (Hz) | 3.09 | 5.13 | 7.76 |
| Roll-rate τ (ms) | 3.88 | 5.98 | 9.24 |

Script (run with `python3 -I`):

```python
import numpy as np
rho=1.2;g=9.81;m=0.4e-3;W=m*g
rng=np.random.default_rng(288);N=200000
L=rng.uniform(.030,.038,N);b=rng.uniform(.04,.07,N);c=rng.uniform(.008,.014,N)
S=b*c;AR=b*b/S;a=2*np.pi*AR/(AR+2);CL=rng.uniform(.5,1.0,N)
V=np.sqrt(2*W/(rho*S*CL));q=.5*rho*V*V;SM=rng.uniform(.05,.25,N)
Iyy=m*L*L*rng.uniform(1/20,1.3/12,N)
f=np.sqrt(q*S*c*a*SM/Iyy)/2/np.pi
mf=m*rng.uniform(.03,.08,N);h=rng.uniform(.18,.24,N)*L;w=rng.uniform(.09,.13,N)*L
Ixx=(m-mf)*(h*h+w*w)/12+mf*b*b/12+rho*np.pi*c*c/4*b**3/12
tau=Ixx/(rho*V*S*a*b*b/24)
```

## My value (calculated, not observed)

- **Pitch short-period mode ≈ 5.1 Hz (90 % range 3.1–7.8 Hz)** for SM 0.05–0.25 c. It reaches ≤ 3 Hz only if SM ≲ 0.05 c. Using a more realistic ellipsoidal body inertia makes I_yy smaller and so pushes the frequency up, not down.
- **Roll-rate damping time constant ≈ 6.0 ms (90 % range 3.9–9.2 ms).** It is about 25 % higher than replicate-260 because I include the air's added inertia.

## Comparison with the recorded value (replicate-260)

- **Pitch: AGREE.** I get 5.1 Hz (3.1–7.8 Hz) against 5.0 Hz (3.1–7.2 Hz). The arithmetic and formula check out. I also agree with replicate-260's secondary finding that the original claim-260 band of 1–3 Hz needs SM ≲ 0.05 c. That band was quoted in replicate-260; I did not see it in any primary source.
- **Roll: AGREE within uncertainty, with a systematic offset.** I get 6.0 ms (3.9–9.2 ms) against 4.6 ms (2.7–7.5 ms). The ranges overlap broadly. My inference is that replicate-260 understates τ by about 20–25 % because it omits the added air inertia, which is the same order as the fin inertia at this scale. The added air inertia also moves the estimate further from the claim-260 band of 1–4 ms.
- **Vestibular clause:** neither replication tested it. I fetched no latency data.
- **Caveat:** this is not a blind replication (see the disclosure at the top). The pitch agreement is partly guaranteed because both models share the same structure, the same fin ranges and the same formula.

```swarm-replication
{"claim_id": 288, "my_value": "pitch short-period ~5.1 Hz (90% 3.1-7.8 Hz); roll-rate tau ~6.0 ms (90% 3.9-9.2 ms); calculated, not observed", "agrees": true, "note": "Arithmetic and formulas of replicate-260 reproduce exactly and my independent-choice model agrees on pitch, but roll tau runs ~25% higher once air added inertia (omitted in 260) is included, and this check was not blind because the inputs file contained the recorded value."}
```
