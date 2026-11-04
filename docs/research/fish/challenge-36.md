# Challenge 36: is tail-beat frequency really the binding limit on surface taxiing?

Adversarial review of a claim I did not write. Project `zebrafish-flight`, subproblem S24 (behaviour).

**Claim under review (verbatim):** "Surface taxiing cannot close the launch gap, and the binding
limit is TAIL-BEAT FREQUENCY not thrust force: sustaining 1.95 m/s needs 49-73 Hz (St 0.2-0.3,
A = 0.2 TL) against measured adult maxima of 21 Hz sustained and 52 Hz transient escape."
Recorded evidence level: derived. Recorded value: 73 Hz.

**Source read:** `docs/research/fish/S24-behaviour.md` and `S24_calcs.py` on branch
`claude/s24-surface-taxiing-launch-tsepbn` (commit 02279553). Read-level: full-text.

**Verdict: WEAKENED.** The arithmetic is right. The frequency is not an independent limit, though.
It is a stand-in for a force balance. The St 0.2–0.3 band in the claim corresponds to a thrusting
lobe with a profile-drag coefficient of about 0.15. The source's own §3.3 assumes a laminar lobe
drag about six times smaller. Under that assumption, a measured heaving-foil thrust law gives
**≈ 23–42 Hz** (calc, A = 0.2 TL) to hold 1.95 m/s. That range sits below the 52 Hz escape
maximum. Separately, the claim's opening clause, "cannot close the launch gap", is stronger than
its own source for the 1.95 m/s case. The source says that case is "not refuted, and not shown
feasible".

---

## 1. Independent arithmetic (calc)

f = St·U/A, with U = 1.95 m/s and A = 0.2 × 40 mm = 8 mm peak-to-peak (project TL premise).

- St 0.2: 0.2 × 1.95 / 0.008 = **48.75 Hz**
- St 0.3: 0.3 × 1.95 / 0.008 = **73.1 Hz**

Both match the claim. Conventions are consistent too. The source uses A as the peak-to-peak
amplitude with St = fA/U. Taylor et al. 2003 and Floryan et al. 2017 both use St = f × (peak-to-peak
excursion)/U (Floryan: St = 2fA/U with A the half-amplitude). **No arithmetic fault.**

The 21 Hz and 52 Hz ceilings are quoted correctly from the source table (Kyriakatos et al. 2011,
EMG; the source records full-text; I did not re-read it).

## 2. Proxy: frequency stands in for a force balance

The Strouhal band is not a kinematic law. It describes where steadily swimming animals end up when
thrust balances drag (Taylor, Nudds & Thomas 2003; the source records abstract read-level and
itself calls the band a cruise-efficiency band, §5). What matters for taxiing is **net streamwise
force on the lobe at U = 1.95 m/s**. Frequency enters only through that force.

The measured thrust law for a heaving foil (Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid
Mech.* 822:386; arXiv 1704.07478; **read-level: full-text**, PDF text extracted) is:

> C_T = c1·St² + c2·St²·f*·U* − C_Dh, with fitted c1 = 3.52, c2 = 3.69, C_Dh = 0.15
> (rigid foil, AR 3.5, Re 4780, St tested 0.05–0.4). Here f* = fc/U and U* = 1/√(1+π²St²).
> The authors state that these constants "should not be taken to be universal".

C_T is normalised by ½ρU²S. Multiplied out, the lift-based thrust term is ½ρS·c1·(fA)². To first
order that term **does not depend on U**. Only the drag term grows with U². The speed the fish can
hold is therefore set by thrust ∝ (fA)²·S against drag. The Strouhal "floor" is simply where those
two terms cross. With Floryan's own numbers, self-propulsion of the bare foil (C_T = 0) falls at
St = √(0.15/3.52) ≈ 0.21 (calc, first term only). **That is where St ≈ 0.2 comes from: a profile-drag
coefficient of 0.15.** Change the drag and the "frequency limit" moves with it.

So the claim's dichotomy, "frequency, not thrust force", is false as stated. The frequency need is
derived from a force balance and has no existence separate from it.

## 3. Hidden assumption, relaxed

The hidden assumption is that the lobe must operate at St ≥ 0.2. That is equivalent to lobe
C_D ≈ 0.15. The source's §3.3, however, computes taxi drag with **two-sided laminar friction** on
the lobe: at Re = 1.95 × 0.006/10⁻⁶ ≈ 11,700, 2 × 1.328/√Re = **C_D ≈ 0.025** (calc, reproduced).
The two sections of the source therefore assume different lobe drags.

I solved for the frequency at which the Floryan thrust law gives net lobe thrust equal to air drag
W/(L/D), with W = 3.92 mN. Inputs are the source's: L/D 4–8, lobe chord 6 mm, lobe area 0.15–0.30
cm² per side. I added a factor 0.5 on c1 and c2 to cover low aspect ratio, surface piercing and Re
mismatch. That factor is an assumption, not a measurement. Script: `challenge-36_calc.py`.

| Lobe C_D | A | c-scale 1.0 | c-scale 0.5 |
|---|---|---|---|
| 0.025 (source's own §3.3) | 0.20 TL (8 mm) | **23–30 Hz** (St 0.09–0.12) | **32–42 Hz** (St 0.13–0.17) |
| 0.025 | 0.15–0.25 TL | 18–40 Hz | 26–55 Hz |
| 0.15 (Floryan rigid foil) | 0.20 TL | 49–52 Hz (St 0.20–0.21) | 68–73 Hz (St 0.28–0.30) |
| 0.15 | 0.15–0.25 TL | 39–68 Hz | 55–95 Hz |

(All calc. Ranges span lobe area 0.15–0.30 cm² and L/D 4–8.)

Results:
- With the C_D = 0.15 row, the claim's **49–73 Hz is reproduced almost exactly**. The claim is
  internally consistent with a thick, rigid-foil drag coefficient.
- With the drag assumption the source itself used, a 0.2 TL tail needs **23–42 Hz** to hold
  1.95 m/s. That is below the 52 Hz measured escape maximum in every corner, and only about
  1.1–2× the 21 Hz sustained ceiling.
- So whether frequency binds depends on the lobe's profile drag and lobe area (f ∝ 1/√S when air
  drag dominates). Those are force-side quantities, and neither is measured. Omitted spray,
  ventilation and wave drag (source §5) would push C_D up and favour the claim. A thin fin at
  higher Re would push it down. **The binding limit is undetermined, not frequency.**

What this does **not** show: it does not show taxiing is feasible. The fit comes from one deeply
submerged rigid foil at AR 3.5, 60 mm/s and Re 4780. Extrapolating it to a ~6 mm, low-AR,
surface-piercing, flexible zebrafish lobe at Re ≈ 12,000 is a large step. Floryan et al. also report
that thrust at fixed St depends on h/c, so St alone is not sufficient. Here h/c ≈ 4/6 ≈ 0.67.
Lateral force, muscle power at 25–40 Hz, and weight support (source §3.5) were not computed here.
The source's 12–46-beat endurance question remains open, now at 25–40 Hz instead of 50–75 Hz.

## 4. Evidence level

- "Derived" is honest for the 49–73 Hz number. It is arithmetic on an assumed St band and an
  assumed amplitude, and the source tags it "calc" in the sentence. No defect there.
- The **claim sentence overstates its source.** "Surface taxiing cannot close the launch gap" holds
  for the 1-BL target (5.84 m/s). For the 3-BL target (1.95 m/s), S24 §4 states "not refuted, not
  shown feasible". The claim as compressed drops that qualifier. That is an evidence-level defect
  in the claim, not in S24.
- The 52 Hz is an EMG frequency during escape, not a kinematic tail-beat frequency (source §5).
  The claim calls it a "measured adult maximum" of tail-beat. The source flags this caveat; the
  claim omits it.

## 5. Regimes and counter-examples

- **Exocoetids.** The APS March Meeting 2024 abstract S27.00013, "Flying fish taxiing on the
  water's surface" (Hao-Ping Wang, National Tsing Hua University), reports taxi tail-slapping at
  **13.5 Hz**. **Read-level: search-summary**; the host meetings-archive.aps.org could not be
  resolved from this session. The taxi speed in that study is **unknown** to me, so I cannot
  compute its St. If an exocoetid of ~0.25 m taxis near 10 m/s at 13.5 Hz with A ≈ 0.2 L, St ≈ 0.07.
  That figure is my hypothetical, not a reported value. It would be a direct counter-example to an
  St ≥ 0.15–0.2 thrust floor while taxiing. The other sources disagree: Deng et al. 2019 (bioRxiv
  10.1101/765560) cite 50–70 strokes s⁻¹ and ~41.7 beats s⁻¹ (**read-level: search-summary**). This
  disagreement is preserved, not resolved. The source's exocoetid "consistency check" (60 Hz)
  assumes St 0.3, so it cannot test the St assumption.
- **Surface-piercing foils.** A 2024 JSME abstract (J-STAGE, 2024_2A1-M06; **read-level:
  search-summary**) reports CFD of caudal-fin twisting during taxiing increasing lift 3.5×. That
  concerns vertical force, not thrust, so it is not used. It does indicate that the lobe operates
  in a regime the deep-water St band does not describe.
- **Negative search scope:** two web searches (foil thrust-scaling; flying-fish taxi frequency)
  and one full-text read (Floryan 2017). I did not find a measured thrust-vs-St curve for a
  surface-piercing or low-AR flexible fin at Re ~10⁴. I did not search Web of Science or Google
  Scholar.

## 6. Corrected statement

"Surface taxiing cannot close the 1-BL (5.84 m/s) gap. For 1.95 m/s it is undetermined. The
required tail-beat frequency is a force-balance output, not an independent kinematic ceiling. It
is 49–73 Hz if the lobe has rigid-foil profile drag (C_D ≈ 0.15), and ≈ 23–42 Hz (calc, A = 0.2 TL)
under the laminar lobe drag the source itself assumes. That range is within the 52 Hz escape
maximum but above the 21 Hz sustained ceiling. The decisive unknowns are lobe drag, lobe area,
and how long the fish can hold escape-range frequency."

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-behaviour.md + S24_calcs.py, branch claude/s24-surface-taxiing-launch-tsepbn | full-text | the claim, its inputs, §3.3 lobe drag |
| 2 | Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.* 822:386, arXiv 1704.07478 | full-text | heave thrust law and fitted constants |
| 3 | Wang (H.-P.) et al., APS March Meeting 2024, S27.00013 | search-summary; host could-not-access | 13.5 Hz taxi frequency |
| 4 | Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560 | search-summary | 41.7 and 50–70 beats s⁻¹ (disagreement) |
| 5 | JSME 2024 conference abstract 2A1-M06 (J-STAGE) | search-summary | taxi fin twisting, lift ×3.5 |
| 6 | Taylor, Nudds & Thomas 2003, *Nature* 425:707 | not re-read (abstract per source) | St band definition |
| 7 | Kyriakatos et al. 2011, *J. Neurosci.* | not re-read (full-text per source) | 21 / 52 Hz |

```swarm-challenge
{"claim_id": 36, "outcome": "weakened", "reason": "The 49-73 Hz arithmetic is correct, but the St 0.2-0.3 floor is a force balance that implies lobe drag C_D about 0.15. Under the source's own laminar lobe drag (C_D about 0.025), Floryan et al. 2017's measured heave-thrust law gives about 23-42 Hz, inside the 52 Hz escape maximum. So frequency is not an independent binding limit, and 'cannot close' overstates the source's own 'not refuted' for 1.95 m/s.", "corrected_value": "≈23–42 Hz at A = 0.2 TL under the source's laminar lobe drag (49–73 Hz only if lobe C_D ≈ 0.15); calc"}
```
