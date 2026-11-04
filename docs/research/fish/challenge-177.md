# Challenge 177: adversarial review of S24-D (taxi tail-beat frequency recomputed from Strouhal)

**Claim under review (author's, not mine):** the recorded 132–199 Hz (2.5–3.8× the 52 Hz escape EMG
maximum) requirement for the 3-BL target used Strouhal numbers measured at Re ~7e3. The taxi runs at Re ~7.8e4,
where fish kinematics (Bainbridge 1958 via Seo et al. 2025; Wardle 1975, stride 0.6–0.8 L/beat) give
peak-to-peak St ~0.24–0.27. On that basis the claim puts the requirement at ~61–81 Hz (1.2–1.6×), so the
"wider margin, a fortiori" argument falls. The 3-BL target goes back to "not shown to close, not refuted", and
the 1-BL target (~195 Hz) stays closed. The claim records its evidence level as `derived`.

**My verdict: WEAKENED.** The central move holds. Taking the 132–199 Hz figure away does remove the
"a fortiori" argument, and "not shown to close, not refuted" is the right status for the 3-BL target. Four
problems remain. The 61–81 Hz figure is a floor for steady swimming, but the claim labels it a requirement.
Re explains only part of the gap the claim attributes to it. The 1-BL target is held "closed" without showing
that it does not depend on the same St input that was just discarded. And the stride relation is extrapolated
about 5× beyond the speeds it was measured at.

No S24 source files exist in this repository. I searched every branch and the working tree for
"S24", "taxi", "Strouhal" and "launch gap" and found no matches apart from unrelated phyllotaxis text. So I
could not read the original 132–199 Hz working. Every statement below about that working is inferred from
the numbers in the claim.

## 1. Arithmetic, redone independently (calculated, not observed)

- **Body length implied by the claim.** L = Re·ν/U = 7.8e4 × 1.0e-6 / 1.95 = **0.040 m**. In seawater
  (ν ≈ 1.05e-6) this becomes 0.042 m. So the taxi speed is ≈ **49 BL/s**.
- **Frequency from stride.** f = U/(λL):
  - λ = 0.8 gives 60.9 Hz.
  - λ = 0.7 gives 69.6 Hz.
  - λ = 0.6 gives 81.3 Hz.
  - This matches the claimed 61–81 Hz, which is 1.17–1.56× of 52 Hz. ✔
- **Cross-check with Bainbridge's own fit.** Seo et al. quote U = L(¾f − 1 Hz), which gives
  f = (U/L + 1)/0.75 = **66.3 Hz**. This falls inside the range. ✔
- **Cross-check through St with Bainbridge's peak-to-peak amplitude.** Seo et al. quote A ≈ 0.18 L at
  high speed, so A = 7.2 mm.
  - St = 0.24 gives 65 Hz.
  - St = 0.27 gives 73 Hz.
  - Seo's DNS value at Re_U ≈ 3.6e4 is St = 0.28, which gives 76 Hz.
- **Small internal inconsistency.** With A = 0.18 L, a stride of 0.6–0.8 L implies St = A/(λL) =
  **0.225–0.30**, not 0.24–0.27. The St range and the stride range in the claim do not map onto each other
  under one amplitude. The f range actually comes from the stride. This does not change the verdict.

The arithmetic survives.

## 2. Proxy: steady-swimming stride stands in for a launch (acceleration) requirement

Bainbridge's relation and the high-speed asymptote St → 0.24 describe **steady** swimming, where thrust
equals drag. A taxi toward launch is an acceleration phase. To reach 1.95 m/s within a distance target, thrust
has to exceed drag:

- Under uniform acceleration over 3 BL (0.12 m), a = U²/2d ≈ 16 m/s².
- Over 1 BL it is ≈ 48 m/s².
- Both figures are my calculation, assuming constant acceleration from rest.

Published evidence points the same way:

- **Akanyeti et al. 2017, PNAS 114:13828** (read-level: abstract plus search summary). Accelerating fishes
  consistently use **higher tail-beat amplitude** than steady swimmers. A secondary review, read only as a
  search summary, says amplitude and frequency both rise across 51 species. I could not confirm the frequency
  part from the primary paper.
- **Tytell 2004, J Exp Biol** (eel linear acceleration; read-level: abstract via search summary). St holds
  near 0.32 in steady swimming and **deviates from it during acceleration**. The direction of that deviation
  was not available to me. The full text at sites.harvard.edu could not be accessed because the host is
  blocked by this session's network policy.

**My inference:** 61–81 Hz is a **lower bound** on what the taxi needs, not "the requirement". How much an
acceleration phase adds is `unknown`. If tail amplitude is already near its geometric ceiling (~0.2 L), the
extra thrust has to come from frequency, and the bound rises. This does not rebuild the 132–199 Hz figure,
because nothing I found quantifies the added frequency. It means the figure should be recorded as "≥61–81 Hz
(steady floor)".

## 3. Hidden assumption: the old-versus-new gap is a Reynolds-number effect

The claim attributes the drop from 132–199 Hz to 61–81 Hz (a factor of ~1.6–3.3, ~2.4 at the midpoints) to Re.

Seo et al.'s own DNS of a mackerel-like swimmer (read-level: full text, first 100k characters, arXiv
2507.11665v2) is a computed result, not an observation. It gives:

| Re_U | St_A |
|---|---|
| ≈ 5.8e3 | ≈ 0.34 |
| ≈ 3.6e4 | ≈ 0.28 |

Between Re ~7e3 and ~7.8e4, then, Re alone lowers St by a factor of only about **1.2–1.4**. Plugging
St = 0.34 and A = 0.18 L into the taxi gives ~92 Hz, not 132–199 Hz.

**My inference:** the original figure must also have carried a different amplitude convention or St source. For
example, it could have used half-amplitude St with peak-to-peak A, or a low-Re larval St of ~0.5–0.8. That would
have been a defect in its own right. The author's diagnosis ("rests on St measured at Re ~7e3") is therefore
at best **partial**. The conclusion that the old number was too high still holds, but for a reason the claim
has not fully identified.

A further point: Seo et al. distinguish Re_U = UL/ν from an undulation-based Re_L. The claim does not say
which Re the "~7e3" refers to. If the original St source quoted Re_L, the regime mismatch could be smaller or
larger than stated.

## 4. Extrapolation range

- **Bainbridge's data.** Seo et al. say it covers fish of 4–30 cm at **0.5 to just over 10 L/s**. The taxi
  is at ~49 L/s.
- **Wardle 1975.** Read-level: could-not-access. I tried no fetch; the claim cites it and I have not
  verified its stride values.
- **What the extrapolation assumes.** Applying stride 0.6–0.8 L at about 5× the measured relative speed
  assumes stride stays constant all the way up to a muscle limit. That is the premise of Wardle's argument,
  not something measured at 49 L/s for a 4 cm fish.
- **Re overlap.** The Re overlaps: 7.8e4 is inside Seo's estimated range of 2e4 to ~1e6. That part of the
  claim holds.

## 5. Evidence level

`derived` is honest. The kinematics are measured, but St 0.24 is Seo et al.'s computed high-speed limit of
Bainbridge's **fitted** relation, and 61–81 Hz is a calculation. The wording "measured fish kinematics give
St ~0.24–0.27" mixes the two. Only the kinematics were measured; St and f are calculated.

## 6. The 1-BL target "stays closed": not supported by the claim

The 1-BL figure (~195 Hz) sits at the top of the very range the claim has just discarded. If it came from the
same St/Re input, the same correction would scale it down to roughly 80–90 Hz. That is 195/2.45 to 195/2.2,
my calculation, and it would move the 1-BL target from "closed" toward "not shown". The claim gives no reason
why the 1-BL number is independent of the input it rejects. That status should be re-derived, not carried over.
Status: **untested**, not refuted.

## 7. Counter-regime I could not settle

If "taxi" means a surface-piercing run with only part of the caudal fin immersed (as in exocoetid taxiing),
fully submerged stride and St data underestimate the required frequency. The S24 context is not in this repo,
so this is conditional. I searched nothing taxon-specific for taxi tail-beat frequency, and the value is `unknown`.

## Sources

| Source | Read-level | Note |
|---|---|---|
| Seo, Zhou & Mittal 2025, *Scaling Laws for Caudal Fin Swimmers…*, [arXiv:2507.11665v2](https://arxiv.org/html/2507.11665v2) | full-text (first 100k of 175k chars) | Bainbridge fit; St → 0.24; A ≈ 0.18 L; Re 2e4–1e6; DNS St vs Re |
| Akanyeti et al. 2017, PNAS 114:13828 ([PDF listing](https://sites.harvard.edu/glauder/files/2022/03/Akanyeti.etal_.ALL_.2017.pdf)) | abstract / search-summary | Amplitude higher during acceleration |
| Tytell 2004, J Exp Biol ([PMC listing](https://pmc.ncbi.nlm.nih.gov/articles/PMC1691903)) | search-summary; full text could-not-access (host blocked) | St deviates from 0.32 during acceleration; direction unknown |
| Bainbridge 1958 | could-not-access (secondary via Seo) | — |
| Wardle 1975 | could-not-access | Stride 0.6–0.8 L unverified by me |

```swarm-challenge
{"claim_id": 177, "outcome": "weakened", "reason": "The arithmetic (61-81 Hz from stride 0.6-0.8 L at 1.95 m/s, L=4 cm) and the loss of the 'a fortiori' argument both hold, but 61-81 Hz is a steady-swimming floor rather than an acceleration-phase requirement, Re explains only ~1.2-1.4x of the ~2.4x gap per Seo et al.'s DNS, and the 1-BL '~195 Hz stays closed' status is not shown to be independent of the St input the claim rejects.", "corrected_value": ">=61-81 Hz (steady-swimming lower bound at 1.95 m/s, L~0.04 m; acceleration-phase requirement unknown and higher)", "depends_on": ["U = 1.95 m/s and Re = 7.8e4 as stated (implying L ~ 0.040 m)", "Bainbridge 1958 relation U = L(0.75f - 1 Hz) and A ~ 0.18 L peak-to-peak as quoted by Seo, Zhou & Mittal 2025 (arXiv:2507.11665)", "Seo et al. 2025 DNS St_A ~0.34 at Re_U ~5.8e3 and ~0.28 at Re_U ~3.6e4 (computed)", "Akanyeti et al. 2017 abstract: tail-beat amplitude higher during acceleration", "Tytell 2004 abstract: St deviates from steady value during acceleration", "52 Hz escape EMG maximum as recorded in S24"]}
```
