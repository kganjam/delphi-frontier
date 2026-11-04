# Challenge 179: adversarial review of S21-D (fast-start margin "~4–7×")

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04 · Reviewer: adversarial challenger
(I did not write the claim)

**Claim under review (author's words, source `harvest:zebrafish-fast-start-velocity-pgqbck`):**
"Directly measured per-fish maximum fast-start speeds of adult zebrafish span ~0.45-1.38 m/s, bracketing
S21's Re-derived 0.842 m/s; the fastest individual is still ~4.2x below 5.84 m/s, so the conclusion holds on
firmer evidence but the margin should read ~4-7x, not ~7x."

- Key number: ~1.38 m/s. That is the fastest of 50 adults. The bulk is ~0.55–1.15 m/s. It was filmed at
  120 fps, which the author calls "likely an underestimate of instantaneous peak".
- Verdict claimed: *strengthens*.
- Recorded evidence level: `unknown`.
- Source doc: `docs/research/fish/S21-deepen.md`, branch `claude/zebrafish-fast-start-velocity-pgqbck`,
  commit `9ae82754`. My read-level: full-text (repo doc).

**Relation to earlier challenges.** Challenge 75 (branch `claude/challenge-75-zebrafish-fast-start-im1x80`)
reviewed the same S21-D numbers and returned SURVIVED. Claim 179 is the harvested form of that claim. It adds
two things challenge 75 did not judge as part of the claim's text:

- the revised margin band, "~4–7×";
- the stated direction of the 120 fps bias, "likely an underestimate".

This review concentrates on those two additions. I did not re-litigate the parts that challenge 75 tested and
passed.

> **Outcome: WEAKENED.**
>
> - **What survives:** the range 0.45–1.38 m/s, "bracketing 0.842", the 4.2× arithmetic and the qualitative
>   conclusion that the gap is not closed.
> - **Defect: the revised "~4–7×" band is mis-anchored, and it contradicts the claim's own caveat.**
>   - The band takes its *lower* end from the fastest fish's 120 fps reading. The same claim says that
>     reading is "likely an underestimate". If that is true, 4.2× is an *upper* bound on the fastest fish's
>     margin, not the floor of the band.
>   - The band takes its *upper* end (~7×) from the bulk median. The question is whether *any* fish reaches
>     the threshold, so the median margin is not a bound on the quantity that matters.
>   - The honest statement is that the fastest-fish margin is ≈4.2× at face value and lower if the
>     underestimate holds. Sibling simulations put it at roughly 2.8–7.0× against 5.84 m/s. Those figures are
>     derived, not measured.
> - **Secondary point: the direction "likely an underestimate" is not established.** Under the measurement
>   model in challenge 130 and S21-D-D-D, tracking noise in max-of-4 forward differencing can make the
>   reading *over*-estimate the peak (simulated bias of up to 1.4–1.66×). The direction depends on t_p and
>   σ_x, both unknown.

---

## 1. Arithmetic, redone independently

These are my own calculations from the stated inputs, done with a one-line Python check in this session.

| U (m/s) | what it is | 5.84 / U | 4.37 / U |
|---|---|---|---|
| 0.45 | slowest fish (digitised) | 12.98 | 9.71 |
| 0.80 | bulk median, approx. (digitised) | 7.30 | 5.46 |
| 0.842 | S21 Re-derived | 6.94 | 5.19 |
| 1.15 | top of bulk (digitised) | 5.08 | 3.80 |
| 1.38 | fastest fish (digitised) | **4.23** | **3.17** |

- 5.84 / 1.38 = 4.23. The claim's "~4.2×" is correct.
- 0.45 ≤ 0.842 ≤ 1.38, so "bracketing" is correct.
- "~7×" matches 5.84 / 0.842 = 6.94 and 5.84 / 0.80 = 7.3. That end of the band is a *central-tendency*
  margin.

**No arithmetic error.** The defect is in what the band's two ends stand for (§3), not in the division.

**The digitisation itself.** I tried to fetch the Europe PMC full-text XML for PMC8025299 to re-check the
figure. The request timed out after 30 s with 0 bytes received, so for me Miln et al. 2021 is
**could-not-access** in this session. I am relying on two prior digitisations that agree (read-level:
full-text repo docs):

- S21-D, from Fig. 1a;
- challenge 75, from Fig. 1a and the independent Fig. 2c.

Both give 0.45–1.38 m/s, and challenge 75 finds that the 1.38 m/s point is a single fish. I have no grounds
to dispute the range.

## 2. Proxy check

- **Quantity measured:** the peak in-water speed of a point at 0.35 BL from the snout, horizontal, in 30 mm
  of water. That is the author's and challenge 75's reading of the Miln Methods; I did not re-read them.
- **Quantity that matters:** airspeed at water exit, compared with a stall or design speed.
- Breaking the surface can only lose speed, so the proxy errs toward feasibility. That is conservative for
  "gap not closed". This is my inference, and it agrees with challenges 75 and 130.
- **Threshold proxy:** 5.84 m/s is a derived design point (1-BL span, AR 5, C_L 0.6). Replicate-24 and
  challenge 5 give 4.37 m/s at C_L,max 1.07, which makes the face-value margin **3.2×**, not 4.2×.
  - The claim names 5.84 explicitly, so this is not an error in the claim as written.
  - It does mean the "~4–7×" band is stale against the project's current threshold. Against 4.37 m/s the
    same construction gives ~3.2–5.5×.

## 3. Hidden assumption: what the two ends of "~4–7×" represent (tested relaxed)

The author's recomputed table (S21-deepen.md §4) sets the band from two rows:

- 4.2×, from the fastest individual's *reading*;
- ~7×, from the bulk median and from S21's 0.842.

The assumption carrying the "~4" floor is that the 120 fps reading of the fastest fish is close to its true
peak. The same sentence of the claim says the reading is "likely an underestimate". Relaxing that assumption
shows the two cannot both stand:

- **If the reading under-reads, as the claim says:** the true fastest peak is above 1.38 m/s, so the margin
  is below 4.2×.
  - The author's own hypothetical 2× under-read row gives 2.1×.
  - Challenge 130 reran the measurement model under central differencing at t_p = 5 ms. It gets a bias of
    0.67×, a true peak of ≈2.07 m/s, and 5.84 / 2.07 = **2.82×** (simulated input, calculated ratio).
- **If the reading over-reads**, because tracking noise in a max-of-4 forward difference inflates it:
  - S21-D-D-D's measured-shape simulation gives an upper bias of 1.66×, a true peak of ≈0.83 m/s, and
    5.84 / 0.83 = **7.0×**. Read-level: listing, via challenge 130.
  - In this case the fastest-fish margin could itself reach ~7×. That is a statement about measurement
    bias, not about the bulk of the population.

So the fastest-fish margin against 5.84 m/s is **≈4.2× at face value, plausibly ≈2.8–7.0× once the
measurement model is relaxed.** That band is derived from a digitised measurement and simulated bias
factors.

The author's "~4–7×" happens to overlap that range numerically, but it puts the floor at 4. On the author's
own stated bias direction, the floor is *below* 4. The upper end comes from a different statistic, the median.
Its meaning is misleading: reading "~4–7×" as "the margin is at least ~4×" is exactly the inference the
caveat forbids.

**The direction of the 120 fps bias is not established.** I did not run a new simulation; this rests on
challenge 130's and S21-D-D-D's simulations, which I did not re-execute.

- Challenge 75 gives worst-case reads of 0.32–0.86× (under-read).
- Challenge 130 gives forward-difference biases of 0.69–1.38× and central-difference biases of 0.42–1.14×.
- S21-D-D-D gives 0.96–1.66×.

These sources disagree on the sign, and I preserve that disagreement. "Likely an underestimate" holds only
for noise-free tracking with short t_p. With Danos & Lauder's ~25 ms time-to-peak (relayed via S21-D-D-D,
read-level listing) and ~1 mm tracking noise, the simulations put the bias near or above 1.

## 4. Evidence level

- The recorded level is `unknown`. That is not dishonest, but it is under-specified.
- **The range 0.45–1.38 m/s is `measured` (figure-digitised, second-hand).** The quantity is a direct
  kinematic measurement by Miln et al. The numbers come from a reviewer's digitisation, and the figshare raw
  data was could-not-access for both S21-D and challenge 75.
- **"~4.2×" and "~4–7×" are `calculated`.** They divide by a *derived* threshold.
- The claim's phrase "directly measured" correctly applies to the speeds, not to the margin. The sentence
  keeps those separate well enough, so there is no defect here beyond the missing label.
- Suggested record: `measured (figure-digitised)` for the key number, and `calculated` for the margin.

## 5. Counter-examples, regimes and taxa

- **Danos & Lauder 2012** (1000 fps, adult zebrafish COM maximum velocity) is the obvious check on whether
  any adult exceeds ~1.4 m/s. S21-D recorded it as abstract-only; S21-D-D-D read it at listing level via its
  own doc. I did not read it. Its per-sequence maximum values are `unknown` to me.
- **Temperature.** The tests ran at 23 °C, against a 28 °C husbandry standard. A warmer fish could be
  faster. This is unquantified, and the author flags it.
- **My search scope:** one attempted fetch of the Europe PMC XML for PMC8025299, which failed (timeout), and
  a cross-branch `git` review of this repository's S21, S21-D, challenge-75, challenge-129, challenge-130 and
  challenge-163 documents. I made **no new literature search**. I found no adult *Danio* fast-start above
  1.38 m/s, but given that scope this is not evidence that none exists.

## 6. Verdict

**WEAKENED.**

- **What survives:**
  - the range ~0.45–1.38 m/s;
  - that this range brackets 0.842 m/s;
  - 5.84 / 1.38 = 4.2×;
  - "gap not closed" against 5.84 m/s, and also against 4.37 m/s (3.2×).
- **What does not survive as stated:** "the margin should read ~4–7×".
  - Its floor is the face-value reading of a fast-start the same claim calls a likely underestimate, so on
    the claim's own terms the floor is below 4×.
  - Its ceiling is a population-median margin, not a margin on the fastest fish.
- **Corrected statement:** the fastest-adult margin to 5.84 m/s is ≈4.2× at face value (calculated). It is
  plausibly ≈2.8–7.0× once 120 fps measurement bias is allowed in either direction (derived: digitised
  measurement and simulated bias). Against the project's current 4.37 m/s threshold it is ≈3.2× at face
  value and ≈2.1–5.3× with the bias allowed.

```swarm-challenge
{"claim_id": 179, "outcome": "weakened", "reason": "Range 0.45-1.38 m/s, bracketing of 0.842 and 5.84/1.38 = 4.2x all reproduce, but the revised '~4-7x' band takes its floor from a 120 fps reading the same claim calls a likely underestimate (so on its own terms the fastest-fish margin is below 4.2x) and its ceiling from the population median, which bounds nothing about the fastest fish; sibling simulations (not re-run by me) put the fastest-fish margin at ~2.8-7.0x against 5.84 m/s, with the bias direction unresolved.", "corrected_value": "fastest-adult margin to 5.84 m/s ~4.2x at face value (calculated), plausibly ~2.8-7.0x allowing 120 fps bias either way (derived); ~3.2x (2.1-5.3x) against the 4.37 m/s threshold", "depends_on": ["Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146) Fig. 1a/2c fastest fish 1.38 m/s, range 0.45-1.38 m/s, as digitised by S21-D and challenge 75 (could-not-access for me this session: Europe PMC timeout)", "S21-deepen.md section 4 table: '~4-7x' built from fastest-fish reading (4.2x) and bulk median/0.842 (~7x)", "5.84 m/s threshold (derived: 1-BL span, AR 5, C_L 0.6)", "4.37 m/s threshold (replicate-24 / challenge 5, C_L,max 1.07)", "challenge-130 simulation: central-difference bias 0.67x at t_p = 5 ms -> true peak ~2.07 m/s (simulated, not re-run by me)", "S21-D-D-D simulation: upper bias 1.66x -> true peak ~0.83 m/s (read-level listing via challenge 130)", "assumption: in-water peak speed is an upper proxy for water-exit speed"]}
```
