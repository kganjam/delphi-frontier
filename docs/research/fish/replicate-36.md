# Replicate 36: can surface taxiing close the launch gap, and is tail-beat frequency the binding limit?

Claim under test (answer removed): *Surface taxiing cannot close the launch gap, and the binding
limit is TAIL-BEAT FREQUENCY, not thrust force.* Inputs point to `S24-behaviour.md` and the
Strouhal law entry.

**Everything below is CALCULATED.** I measured nothing, simulated nothing and observed no fish.
The inputs are literature values or repository values, and each one has its read-level stated.

## Process note (independence)

- The task said the inputs were "reproduced here exactly from the Strouhal law entry", but no
  numbers were actually included. I therefore took the law from `library/pages/strouhal.md` on
  branch `origin/claude/strouhal-law-8mv27w` (full-text, repository file). I took the launch
  speed from the repository's replication of claim 1 (`replicate-1.md`, stall-speed branch) and
  the burst speed from replication 21. These are other claims, not claim 36.
- I did **not** open `S24-behaviour.md` (branch `origin/claude/s24-surface-taxiing-launch-tsepbn`)
  until my derivation and numbers below were fixed. After that I grepped it for the result
  (see "Comparison").

## Method

Taxiing means the tail stays in the water and keeps producing thrust while the body speeds up
to the airspeed a wing needs to carry the fish. Whatever force the muscle can supply, the tail
only produces thrust while its kinematics keep up with the forward speed U. I used three
kinematic routes, each of which turns U into a minimum tail-beat frequency f:

1. **Strouhal:** f = St·U/A, with A the peak-to-peak tail amplitude (law entry, eq-strouhal).
2. **Slip / wave speed:** an undulating body makes thrust only if its body wave travels backward
   faster than the fish moves forward, so f·λ > U and f > U/λ. Here λ is the body wavelength,
   which I assume is about 1 L (range 1.0–1.2 L).
3. **Stride length:** U = s·f·L, with s ≈ 0.6–0.7 body lengths per beat. This is a typical value
   for fish at speed. I recall it from the fish-kinematics literature (Bainbridge 1958 is the
   usual citation) but **did not verify it in this session**, so I treat it as an assumption.

I then compare the required f with the highest tail-beat frequency I could find for zebrafish.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Strouhal law, St = fA/U, A peak-to-peak | — | `library/pages/strouhal.md` (law-strouhal) | full-text (repo) |
| Cruising St band | 0.2–0.4 (no central value) | Taylor, Nudds & Thomas 2003, via the law entry | search-summary (as recorded in the law entry) |
| Foil optimum St | 0.25–0.35 | Triantafyllou et al. 1993, via the law entry | search-summary (as recorded) |
| Target launch airspeed U | 6.1 m/s (range 5.8–6.8). This is the stall speed of a 1-BL-span, AR 5, CL 0.6 wing on a 0.4 g fish | `replicate-1.md` (claim 1). **Calculated**, not observed | full-text (repo) |
| Body length L | 3.5 cm central (range 3.3–3.8 cm) | FishBase max SL 3.8 cm (via replicate-1, search-summary); mean TL 33.0 mm (Danos & Lauder 2012, via replicate-21, full-text as relayed) | as stated |
| Tail amplitude A/L | 0.20 (range 0.15–0.25) | **Assumption.** A generic fish value; I did not retrieve an adult zebrafish measurement | — |
| Adult burst speed (context for the gap) | 0.84 m/s | `replicate-21.md`, inverted from Danos & Lauder 2012 Re. **Calculated** | full-text (repo) |
| Zebrafish tail-beat ceiling I found | larval burst 45–75 Hz; larvae at 4–5 dpf up to 95 Hz | arXiv q-bio/0411029 (citing Budick & O'Malley 2000), and a search snippet for larval kinematics | search-summary. **Larval**, not adult |
| Adult zebrafish maximum tail-beat frequency | **unknown** to me | Searches: "adult zebrafish maximum tail beat frequency Hz burst swimming" (standard) and "adult Danio rerio tail beat frequency critical swimming speed Ucrit kinematics" (extended). Neither returned a number | search-summary, negative |
| Flying-fish comparison | taxi 13.5 Hz (APS 2024 abstract); taxi 50–70 Hz (Deng et al. 2019 bioRxiv; CFD uses 50 Hz); leap 21.2 ± 4.6 Hz (Makiguchi et al. 2013) | web search | search-summary. **The sources disagree, and I have not reconciled them** |

## Arithmetic

**Route 1, Strouhal (f = St·U/A):**
- Central: St 0.3, U 6.1 m/s, A = 0.20 × 0.035 = 0.0070 m, so f = 1.83/0.0070 = **261 Hz**
- Most favourable corner: St 0.2, U 5.8, A = 0.25 × 0.038 = 0.0095 m, so f = 1.16/0.0095 = **122 Hz**
- Least favourable corner: St 0.4, U 6.8, A = 0.15 × 0.033 = 0.00495 m, so f = 2.72/0.00495 = **549 Hz**

**Route 2, slip (f > U/λ):**
- λ = L = 0.035 m, U 6.1: f > **174 Hz**
- Most favourable: λ = 1.2 × 0.038 m, U 5.8: f > **127 Hz**

**Route 3, stride (f = U/(s·L)):**
- s 0.65, L 0.035 m, U 6.1: **268 Hz**
- Most favourable: s 0.7, L 0.038 m, U 5.8: **218 Hz**

**Reverse check: the speed reachable at the highest frequency I found (95 Hz, larval), U = f·A/St etc.:**
- Strouhal: central 2.2 m/s, most favourable 4.5 m/s, least favourable 1.2 m/s
- Slip ceiling: 3.3–4.3 m/s
- Stride: 2.2–2.5 m/s

Every case falls short of 5.8 m/s.

**My value:** sustaining thrust up to the 1-BL-wing launch speed needs a tail-beat frequency of
**about 260 Hz (range about 120–550 Hz; calculated)**. That is at least 1.3× and centrally
about 2.7× the highest zebrafish frequency I found (95 Hz). That 95 Hz figure is **larval** and
read at search-summary level. Adults are generally expected to beat more slowly (frequency
scales roughly as 1/L, per Sánchez-Rodríguez, Raufaste & Argentina, arXiv:2301.10466; abstract
read via summariser). If so, the real margin is larger. I did not find an adult figure.

## Is the limit frequency rather than force?

- **Frequency side (calculated):** all three kinematic routes put the requirement above the
  frequency I found, even at the most favourable corner. A cap on frequency caps the speed at
  which any thrust can be made, whatever force is available. This holds under the stated
  assumptions.
- **Force side:** I did **not** quantify available caudal thrust. I found no measured adult
  zebrafish thrust (scope: the two searches above; I did not run a dedicated thrust search). The
  following is only my inference from dimensional reasoning: muscle force scales with L² while
  weight scales with L³, so force per unit weight improves as size falls, whereas the frequency
  needed (U/L) gets worse. That points to frequency as the limit at zebrafish scale. It is an
  argument, not a demonstration.
- **Scope caveat from the law entry itself:** the entry says no St band should be applied to
  launch or other non-steady locomotion (its "Where it breaks" item 3, which is the entry
  author's inference). Route 1 therefore goes beyond the law's stated domain. Routes 2 and 3 do
  not depend on St, and they give the same conclusion.
- **Not checked by me:** whether a lower target speed (for example a larger wing) brings the
  required frequency into reach. My derivation covers the 1-BL-wing case only.

## Comparison with the recorded value (read only after the above)

I grepped `S24-behaviour.md` for "strouhal", "tail-beat freq" and "binding". It records:
- For the 1-BL wing (5.84 m/s): the tail would need to keep producing thrust at **88–292 Hz
  (calc)**, which is 1.7–5.6× the **52 Hz** escape maximum measured in adult zebrafish
  (Kyriakatos et al. 2011, which S24 reads as full-text). The measured sustained ceiling is 21 Hz.
- For a 3-BL wing (1.95 m/s): it needs 49–73 Hz, and S24 calls this "not refuted, not shown
  feasible".
- S24 states that force and power are not the obstacle (calc), and that no adult caudal thrust
  was measured.

**AGREE on the 1-BL case.** My range (122–549 Hz, central 261 Hz) overlaps S24's 88–292 Hz. The
lower floor in S24 comes from its generous St 0.15 assumption, below the 0.2–0.4 band I used.
Both derivations find the requirement above any available tail-beat frequency. S24's adult
ceiling (52 Hz) is stronger evidence than my larval 95 Hz, and both lead to the same verdict.

**Two limits on that agreement:**
1. Both derivations rest on the same St-band reasoning and the same 1-BL stall speed from
   claim 1, so they are not independent in their premises.
2. Neither one measured thrust, so "not thrust force" remains a calculated drag balance in S24
   and only an inference in my version.

I did not independently analyse the 3-BL case, so I **cannot tell** whether the unqualified
claim ("cannot close the launch gap") holds for larger wings. S24 itself does not claim that it
does.

```swarm-replication
{"claim_id": 36, "my_value": "~260 Hz required tail-beat frequency (range ~120-550 Hz; calculated) to keep thrusting to 5.8-6.8 m/s, vs <=95 Hz highest zebrafish frequency found (larval, search-summary)", "agrees": true,
  "note": "Strouhal, slip and stride routes all put the 1-BL-wing taxi requirement above any zebrafish tail-beat frequency, overlapping S24's 88-292 Hz; the 'not force' half and the 3-BL-wing case were not independently established."}
```

## Sources consulted this session

- [arXiv q-bio/0411029: Neurokinematic modeling of larval zebrafish](https://arxiv.org/pdf/q-bio/0411029) (search-summary)
- [Sánchez-Rodríguez, Raufaste & Argentina, arXiv:2301.10466](https://arxiv.org/abs/2301.10466) (abstract, via summariser)
- [Nature Communications version of the same paper](https://www.nature.com/articles/s41467-023-41368-6) (could-not-access: login redirect)
- [Deng et al. 2019 bioRxiv, flying-fish taxiing](https://www.biorxiv.org/content/10.1101/765560.full.pdf) (search-summary)
- [APS March Meeting 2024, flying fish taxiing](https://meetings-archive.aps.org/mar/2024/s27/13) (search-summary)
- [Makiguchi et al. 2013, Aquatic Biology 18:105](https://int-res.com/abstracts/ab/v18/n2/p105-111) (search-summary)
