# Challenge 288: adversarial review of Replication 260 (zebrafish glider attitude modes)

**Claim under review (the replicator's claim, not mine):** "Replication: pitch short-period ~5 Hz (90% 3–7 Hz) and roll-rate damping tau ~4.6 ms (90% 2.7–7.5 ms), calculated. Roll overlaps recorded 1–4 ms; pitch is ABOVE the recorded 1–3 Hz unless static margin <= 0.05 chord. Passive-stability conclusion holds; vestibular clause not tested."

**Source:** `docs/research/fish/replicate-260.md` and `replicate-260-model.py`, on branch `claude/zebrafish-glider-attitude-fpeh9d` (commit bc9d537). Read-level: **full-text**. I did not read the original claim-260 derivation or any other challenge branch.

**Verdict: WEAKENED.** The numbers survive. The clause "passive-stability conclusion holds" is broader than the evidence behind it.

Everything below is **calculated** from a linear rigid-body model with assumed geometry. None of it is an observation, because no such glider exists. My script is `challenge-288-check.py`.

## 1. Independent arithmetic

I re-derived the central case (b = 5.5 cm, c = 1.1 cm, L = 3.1 cm, C_L = 0.75) from the stated inputs using my own code. I did not copy the author's working.

- S = 6.05e-4 m², AR = 5.0, a = 4.49 rad⁻¹, V = 3.80 m/s, q = 8.65 Pa, Re = Vc/ν ≈ 2.8e3. **Matches.**
- For the roll strip-theory integral I derived it separately: ∫ q c a (p y/V) y dy over ±b/2 = ½ρV c a p b³/12, which gives L_p = ρVSab²/24 = 1.56e-6 N·m·s. I_xx = 6.56e-9 kg·m², so τ = **4.21 ms**. **Matches.**
- The undamped pitch frequency at SM 0.02, 0.05, 0.10, 0.15 and 0.25 comes out at 1.88, 2.98, 4.21, 5.16 and 6.66 Hz. **Matches.**
- I re-ran the author's Monte Carlo script unchanged. It gives 5th/50th/95th percentiles of f_pitch = 3.09 / 5.01 / 7.20 Hz and τ_roll = 2.68 / 4.62 / 7.53 ms. **Matches.**

I found no arithmetic error.

## 2. Proxy check

**(a) Undamped √(M_α/I) used as a proxy for the observable damped short-period frequency.** The author drops M_q and the coupling term Z_α·M_q. I put both back in, using ω_n² = M_α/I + (Z_α/mV)(−M_q/I), ζ = (Z_α/mV − M_q/I)/(2ω_n), and ω_d = ω_n√(1−ζ²). I used Z_α/mV = 15.5 s⁻¹ and bracketed C_mq from 0 to −6 per q̂ = qc/2V. The −6 end stands for a wing plus a small tail; this is my assumed bracket, not a sourced value. Results (calculated):

| SM | ζ (author: 0.2–0.3) | damped f_d (Hz) |
|---|---|---|
| 0.02 | 0.65–0.78 | 1.4–1.9 |
| 0.05 | 0.41–0.61 | 2.7–3.0 |
| 0.15 | 0.24–0.41 | 5.0–5.2 |
| 0.25 | 0.18–0.33 | 6.6–6.7 |

The added damping and the added stiffness nearly cancel, so the frequency band **survives**. The author's ζ ≈ 0.2–0.3 is too low when the static margin is small. At SM ≤ 0.05, which is the only regime that reaches the recorded 1–3 Hz, my calculated ζ is 0.4–0.8. A mode that damped would show barely one overshoot. This is a minor correction and does not change the comparison.

**(b) Roll-rate subsidence τ used as a proxy for roll-attitude stability. This is the substantive defect.** τ = I_xx/L_p describes how fast roll *rate* decays. In this model nothing restores roll *angle*: the model has no dihedral term (L_β), no directional-stability term (N_β), and no spiral or Dutch-roll mode. A body whose roll rate damps in 4 ms can still drift in bank angle without bound, through a neutral or divergent spiral mode. The right quantities are the spiral-mode root and the Dutch-roll damping. These need L_β, N_β and N_r, and so need fin dihedral and vertical-fin geometry, none of which are in the inputs. The author computed none of these, so the roll half of "passive stability" is **untested**, not supported.

**(c) The slow longitudinal mode is absent.** The model contains only the short-period pitch mode. The phugoid is missing. Lanchester's estimate T = π√2·V/g gives a phugoid period of ≈ **1.7 s** (calculated, my inference). That timescale is far longer than any plausible vestibulo-motor latency. So the author's own argument ("fast modes are ≪ the latency, therefore passive only") covers the fast modes alone. The slow modes (phugoid, spiral) are exactly where active control could act. This does not refute the passive half of the claim. It does mean "passive-stability conclusion holds" should read "the two fast modes are passively stable and fast; the slow modes were not computed".

## 3. Hidden assumptions, relaxed

- **Static-margin prior.** The Monte Carlo draws SM uniformly from 0.05 to 0.25 c̄. That draw excludes in advance the region (SM ≤ 0.05) that reproduces the recorded 1–3 Hz. So the "90 % band 3–7 Hz" describes the assumed prior; it is not evidence against the recorded value. The author says so in the text ("the dominant uncertainty"), and the claim states the SM condition. The claim is therefore honest on this point, but the "ABOVE" verdict carries no more weight than that prior.
- **Pitch inertia (slender rod, k/L = 0.289).** A fish body tapers, so its radius of gyration is likely lower than a rod's. I tried k/L = 0.20–0.25 as an assumption, not a sourced value. That *raises* f at SM 0.15 to 6.4–8.0 Hz. Relaxing this assumption strengthens the author's "pitch above recorded" finding. The author's alternative explanation, an inertia 3–5× larger, needs a factor of 2.8× to reach 3 Hz and 6.25× to reach 2 Hz. That is consistent with what the author wrote. The one-line claim leaves out this inertia alternative and names only SM.
- **Lift slope 2πAR/(AR+2) at Re ≈ 3e3.** This is unverified at that Reynolds number, and I did not search for low-Re flat-plate data. Both f (∝ √a) and τ (∝ 1/a) depend on a only weakly. A ±30 % change in a moves f by about ±15 % and τ by about ∓30 %. On that range, the roll value still overlaps 1–4 ms and the pitch value still sits mostly above 3 Hz.
- **Apparent (added) mass in roll.** My estimate is ρπc²b³/48 ≈ 1.6e-12 kg·m², which is about 4 × 10⁻⁴ of I_xx. It is negligible. Survives.

## 4. Evidence level

The recorded level is "derived" and the value is "5 Hz pitch mode". The source document says, in the sentence and in bold, that every number is calculated and not observed. The level is **honest**. The phrase "Not re-run by harvester" is a procedural note, and I can neither confirm nor refute it.

## 5. Missed regimes and counter-examples

- The largest missed regime is the slow modes (phugoid, spiral, Dutch roll); see 2(b) and 2(c).
- Natural fish gliders: I recall that the flying-fish (Exocoetidae) gliding aerodynamics literature, e.g. Park & Choi 2010, *J. Exp. Biol.*, reports longitudinal static stability. I did **not** fetch it, so its read-level is **could-not-access (not attempted)**. I draw no number from it, and I have not checked that it says anything about lateral stability.
- Negative-search scope: I ran no web searches for this challenge. All checks above are internal recomputations.

## Summary

- **Survives:** the arithmetic, the 5 Hz (3–7 Hz) pitch band, the 4.6 ms (2.7–7.5 ms) roll τ, the roll overlap with 1–4 ms, the SM ≤ 0.05 condition, and the honest "calculated" labelling.
- **Weakened:** "passive-stability conclusion holds". The evidence covers only the roll-*rate* subsidence and the pitch short-period. Roll-attitude (spiral/Dutch-roll) stability and the ≈1.7 s phugoid were not computed. Those slow modes are the ones that would bear on any vestibular argument.
- **Minor:** at SM ≤ 0.05, the short-period ζ is 0.4–0.8, not 0.2–0.3.

```swarm-challenge
{"claim_id": 288, "outcome": "weakened", "reason": "The arithmetic and both numeric bands reproduce, but 'passive-stability conclusion holds' rests on roll-rate subsidence and pitch short-period only; roll-attitude (spiral/Dutch-roll) and the ~1.7 s phugoid were never computed, so passive attitude stability is supported only for the fast modes.", "corrected_value": null, "depends_on": ["replicate-260 assumed geometry (b 4-7 cm, c 0.8-1.4 cm, L 2.8-3.5 cm, m 0.4 g)", "static margin prior 0.05-0.25 chord (assumed)", "lift slope 2*pi*AR/(AR+2) at Re ~3e3 (unverified)", "my assumed Cmq bracket 0 to -6 per qc/2V", "Lanchester phugoid approximation T = pi*sqrt(2)*V/g", "recorded values 1-3 Hz and 1-4 ms as quoted in the claim"]}
```
