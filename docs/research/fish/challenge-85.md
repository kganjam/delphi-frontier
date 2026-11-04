# Challenge 85: adversarial review of the S24-D "deepen verdict FALLS" claim

**The claim under review (written by another author, not me).** "S24-D deepen verdict FALLS: at
taxi Re ~7.8e4 measured fish kinematics (Bainbridge 1958 via Seo 2025; Wardle 1975) give
peak-to-peak St 0.24–0.27, requirement ~61–81 Hz (1.2–1.6× the 52 Hz max); the 'a fortiori wider
margin' claim falls, S24 reverts to not-shown-to-close-not-refuted for the 3-BL target; 1-BL
target (~195 Hz) stays closed. Overlaps but is not identical to the 72–83 Hz replication."
Recorded as **derived**, value **71 Hz**. Source: `docs/research/fish/S24-deepen.md` and
`S24-deepen_calc.py` on branch `claude/s24-deepen-launch-gap-2motub` (commit aeb9040). I read
both files in full.

This is a desk review. I ran no experiment. Every number I produce is tagged **calc** (my own
arithmetic, done in a fresh Python session from the stated inputs, without running the author's
script), **measured** (from the literature, with read-level), or **assumed**.

**Verdict: SURVIVED, with two wording defects that do not move the verdict or the 71 Hz value.**

---

## 1. Independent arithmetic (calc)

Inputs as stated in the claim: U = 1.95 m/s, L = 40 mm (premise) or 33 mm, ν = 1 × 10⁻⁶ m²/s,
f_max = 52 Hz, stride λ = 0.6–0.8 L per beat, f_req = U/(λL).

| Quantity | My value (calc) | Claim | Agrees? |
|---|---|---|---|
| Re at L 40 mm | 7.8 × 10⁴ | 7.8 × 10⁴ | yes |
| Re at L 33 mm | 6.4 × 10⁴ | 6.4 × 10⁴ | yes |
| f_req, λ 0.8, L 40 mm | 60.9 Hz (1.17×) | 61 Hz (1.17×) | yes |
| f_req, λ 0.6, L 40 mm | 81.2 Hz (1.56×) | 81 Hz (1.56×) | yes |
| Bainbridge form, f = (4/3)(U/L + 1 Hz) | 66.3 Hz | 66 Hz | yes |
| Midpoint of 61–81 Hz | 71.1 Hz | 71 Hz (recorded value) | yes |
| f_req at L 33 mm, λ 0.8–0.6 | 73.9–98.5 Hz (1.42–1.89×) | 74–98 Hz (in body §4) | yes |
| 1-BL target, 5.84 m/s, λ 0.75 | 195 Hz (3.7×) | ~195 Hz | yes |
| 1-BL target, λ 1.0 (most favourable stride on record) | 146 Hz (2.8×) | not stated in the claim | the case stays closed |

I found no arithmetic error.

## 2. Defects found (both concern wording, not the verdict)

**Defect A: St 0.24–0.27 is not equivalent to stride 0.6–0.8 L, as the source states it is.**

- The two quantities are linked by St = (A/L)/λ, with A the peak-to-peak amplitude.
- With λ 0.6–0.8 (calc):
  - A/L = 0.18 gives St 0.225–0.30.
  - A/L = 0.20 gives St 0.25–0.33.
- Going the other way, St 0.24–0.27 corresponds to λ 0.67–0.75 (A/L 0.18) or 0.74–0.83 (A/L 0.20)
  (calc).
- S24-deepen.md §3 says the stride range "is the same as" St 0.24–0.27. It is not. The St range
  quoted in the claim is narrower and lower than the stride range implies.
- The claim's Hz figures were computed from λ, not from St, so 61–81 Hz is unaffected.
- But if a reader takes the claim's St 0.24–0.27 together with S24's A = 8 mm, they get
  **58–66 Hz** (calc), not 61–81 Hz.
- The headline therefore carries two inputs that do not match each other. The stride figure is
  the one that produced the number.

**Defect B: the headline leaves out the L basis.**

- 61–81 Hz (1.2–1.6×) applies only at L = 40 mm.
- At the measured 33 mm fish it is 74–98 Hz (1.4–1.9×) (calc).
- The source document reports this in §4, but the one-line claim does not.
- This moves the top of the range from 1.6× to 1.9×. It does not change the verdict, because
  1.9× is still well below the 2.5–3.8× the claim says has fallen.

## 3. Is a proxy standing in for the quantity that matters?

**Yes.** The claim acknowledges this proxy in its §4, but it is still the main weakness.

- **The quantity that matters** is the tail-beat frequency needed for **surface taxiing**. In a
  taxi only the lower caudal lobe is in the water, at about 49 BL/s.
- **The proxy** is the stride length of fully submerged steady swimmers (dace, trout, goldfish,
  10–30 cm). Their measured speeds reach roughly 10 BL/s, not 49. The claim matches Re
  (2 × 10⁴ – 10⁶), but it does not match relative speed or propulsion mode.

**Better quantity: the measured taxi stride of flying fish.** Read-levels:

- Deng, Wang, Zhang & Mao 2019, bioRxiv 765560: **full-text (HTML), read through an automated
  summariser.**
- The observations it cites (Hertel 1966; Davenport 1994): **listing**, relayed by Deng et al.
  I did not read either primary source.

What the sources report:

- **Measured (Hertel 1966, as relayed):** about 50 beats/s while taxiing.
- **Measured (Davenport 1994, as relayed):** 50–70 strokes/s.
- **Simulated (Deng et al. CFD, standard length 0.25 m):** the force balance during taxiing at
  10 m/s is met at 50–60 Hz. Fully submerged cruising at the same speed needs 98–145 Hz. These
  are simulations, not observations.

Stride implied by these figures (calc; inference mine):

- **Assumption (mine):** these frequencies are paired with 10 m/s and L 0.25–0.30 m. Deng et al.
  make this pairing for Hertel's 50 Hz. The speed that went with Davenport's observations is
  **unknown** to me.
- Under that pairing the taxi stride is **0.48–0.80 L/beat** (calc). This is at about 33–40 BL/s,
  close to the zebrafish's 49 BL/s.
- Applied to a 40 mm zebrafish at 1.95 m/s, that stride gives **61–102 Hz (1.17–1.96×)** (calc).

What follows from this (inference, mine):

- The one direct taxi stride I could find agrees with the Wardle band at its central and upper
  values, and extends it downward to 0.48. So the proxy does **not** introduce a bias large enough
  to restore the 132–199 Hz figure, but the high end of the claim's range may be somewhat low.
- Deng et al.'s simulation also suggests that a stride measured at low BL/s overstates the stride
  of a fish swimming fully submerged at about 40 BL/s (0.28–0.41 L/beat, calc from their 98–145 Hz).
  Taxiing recovers a stride near Wardle's because the body's drag is removed.
- The two effects roughly cancel in flying fish. That is a fortunate coincidence for the claim,
  not something its method guarantees.

The claim's §4 says "the submerged-swimming stride therefore probably **overstates** the
frequency a taxi needs". The flying-fish data do **not** support that direction (my inference):

- The observed taxi stride (0.48–0.8) is no longer than Wardle's submerged stride (0.6–0.8).
- If anything it is shorter, which means a higher required frequency.

This caveat sits outside the claim under review, but anyone relying on it to argue that the
3-BL gap closes should note it.

## 4. Hidden assumption that carries the result, tested relaxed

**Assumption:** a 4 cm zebrafish with symmetric lobes taxis with roughly the same stride as large
fish.

**Relaxation 1: the taxi stride is the flying-fish band, 0.48–0.8.**

- Result: 61–102 Hz, or 1.2–2.0× (calc).
- The verdict holds. The figure is below 2.5×, so the "a fortiori" margin still falls, and it is
  above 1×, so the gap is still not shown to close.

**Relaxation 2: stride shortens further for a fish without a hypocaudal lobe.**

- A zebrafish has far less immersed lobe area than an exocoetid. That points to a shorter stride,
  but I have no measurement of it.
- Reaching the recorded 132 Hz would take λ ≤ 0.37 at L 40 mm (calc).
- No taxi or swimming measurement I saw at Re ≥ 2 × 10⁴ goes that low. Deng et al.'s 0.28–0.41 is
  for **fully submerged** swimming and is **simulated**.

**Conclusion of the test (inference, mine):**

- Under these relaxations the claim's qualitative verdict, "not shown to close, not refuted",
  holds.
- The claim's stated precision (61–81 Hz) is narrower than the relaxations support (about
  61–102 Hz). That is consistent with the claim's own statement that its margin is "now smaller
  than the uncertainty in several other inputs".

**Relaxation 3: f_max.**

- If adult kinematic f_max were higher than the 52 Hz EMG figure, the 3-BL case could open.
  The claim already says so.
- The 1-BL case needs 146–256 Hz (calc, λ 1.0–0.57) and stays closed unless f_max is at least
  about 146 Hz. No source on record supports that for adult zebrafish.

## 5. Is the evidence level honest?

**Yes.**

- "Derived" is correct for 71 Hz. It is a calculation from literature inputs and the source
  document labels it calc throughout.
- The underlying stride figure (Wardle 1975, 0.6–0.8) is held at **search-summary** read-level by
  the author, and the Bainbridge formula is held at abstract plus a secondary full text. The
  source table declares both openly.
- One wording flag: the claim says "measured fish kinematics … give peak-to-peak St 0.24–0.27".
  - The stride is measured.
  - The St band is a **conversion** that uses an amplitude convention the author could not check
    in Bainbridge's primary text ("unknown to me", §6 of the source).
  - The St value is therefore a derived quantity, not a measurement. Combined with Defect A, the
    St clause is the weakest part of the claim.

## 6. Comparison with the 72–83 Hz replication

I read `docs/research/fish/replicate-52.md` on branch `claude/strouhal-band-rederivation-ljqyv7`
(full-text).

- It derives 72–83 Hz (bracket 64–101 Hz) from Eloy's Lighthill-number model at Re 7.8 × 10⁴.
  That is a calculation, not an observation.
- The method is independent of the claim's: a drag-law model, not stride kinematics.
- Its central range overlaps the claim's 61–81 Hz at 72–81 Hz.
- Its bracket and my flying-fish relaxation (61–102 Hz) agree on an upper end near 100 Hz.

The claim's statement "overlaps but is not identical" is accurate. The three routes disagree on
the high end (81 vs 83 vs about 100 Hz). I preserve that disagreement rather than average it.
None of the three reaches 132 Hz.

## 7. Scope of negative searches

- **Adult zebrafish tail-beat frequency against speed at U > 0.5 m/s:** none found. I ran one web
  search ("adult zebrafish tail beat frequency swimming speed stride length body lengths per second
  swim tunnel"). It returned vendor protocols and Mwaffo et al. 2017 at low Re. I did not
  rely on a vendor table showing 26–33 Hz at Ucrit: its provenance is unknown, and it looks
  illustrative.
- **Flying-fish taxi frequency:** one web search, plus a summariser read of Deng et al. 2019
  (bioRxiv). The full-PDF fetch exceeded the size limit, so I read the HTML version.
  - An APS 2024 meeting abstract reports 13.5 Hz for flying-fish surface tail beats (search-summary
    only; I did not read it).
  - That figure conflicts with the 50–70 Hz from Hertel and Davenport. The conflict is
    unresolved and preserved here.
  - If 13.5 Hz paired with about 10 m/s were right, the taxi stride would be about 3 L/beat. That
    would favour closing the 3-BL gap. I could not verify the speed, body length or context of
    that measurement, so I do not use it.
- **Not searched:** Web of Science, Google Scholar, Hertel 1966, Davenport 1994, or Wardle 1975
  full text.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| S24-deepen.md, S24-deepen_calc.py (branch `claude/s24-deepen-launch-gap-2motub`, aeb9040) | full-text | the claim and its inputs |
| replicate-52.md (branch `claude/strouhal-band-rederivation-ljqyv7`) | full-text | the 72–83 Hz comparison |
| Deng J, Wang S, Zhang L, Mao X (2019) bioRxiv 10.1101/765560 | full-text (HTML, via summariser) | flying-fish taxi CFD, 50–60 Hz at 10 m/s, L 0.25 m; submerged 98–145 Hz |
| Hertel 1966; Davenport 1994 | listing (relayed by Deng et al.) | observed taxi frequency 50 and 50–70 Hz |
| APS March Meeting 2024 abstract, "Flying fish taxiing on the water's surface" | search-summary | conflicting 13.5 Hz figure (not used) |
| Bainbridge 1958; Wardle 1975; Seo et al. 2025 | not re-read by me (as relayed by the claim's author) | the claim's inputs |

```swarm-challenge
{"claim_id": 85, "outcome": "survived", "reason": "Independent arithmetic reproduces 61-81 Hz (71 Hz midpoint) and 195 Hz exactly, and the one direct taxi-stride datum I found (flying fish, ~0.48-0.8 L/beat, relayed observation) gives 61-102 Hz, still far below the 132-199 Hz the claim says has fallen and still above 52 Hz; the only defects are wording (St 0.24-0.27 does not match stride 0.6-0.8, which implies St 0.225-0.33, and the L=33 mm range of 1.4-1.9x is left out of the headline).", "corrected_value": null,
  "depends_on": ["U = 1.95 m/s 3-BL glide target (inherited)", "L = 40 mm premise (33 mm alternative)", "f_max = 52 Hz escape EMG maximum (Kyriakatos 2011, relayed)", "Wardle 1975 stride 0.6-0.8 L/beat (search-summary via claim author)", "Bainbridge 1958 V = L(3f-4)/4 (via Seo et al. 2025)", "flying-fish taxi frequency 50-70 Hz (Hertel 1966; Davenport 1994, relayed by Deng et al. 2019) paired with ~10 m/s and L 0.25-0.30 m (my assumption)", "1-BL target 5.84 m/s (inherited)", "replicate-52 72-83 Hz (for the overlap statement only)"]}
```
