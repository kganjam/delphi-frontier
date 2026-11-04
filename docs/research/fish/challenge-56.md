# Challenge 56: "LAWENTRY gompertz dispatched"

- **Claim:** "LAWENTRY gompertz dispatched".
- **Source session:** `session_01QbcBRXwsw8oX2P7vJAHodk`.
- **Recorded evidence level:** unknown. **Recorded value:** n/a.
- **Verdict:** **SURVIVED**, with notes.

## What the claim is

The claim is operational, not scientific. It says a task to write a `gompertz` law entry was
dispatched. It does not give a number. So it can be broken in two ways: show that no such work was
produced, or show that the produced entry is so faulty that "dispatched" hides a failed job.

## Evidence (from git, fetched 2026-11-04)

- Commit `5bdbed7b`, "Add Gompertz growth entry, with where it departs from von Bertalanffy", is on
  `origin/claude/gompertz-growth-law-kx88sa`.
  - Its `Claude-Session` trailer is `session_01QbcBRXwsw8oX2P7vJAHodk`, the same session as the
    claim.
  - It adds `library/laws/gompertz.yaml` (218 lines) and `library/pages/gompertz.md` (121 lines), and
    adds one row to `library/pages/index.md`.
- **Gate result, measured by me:** I ran `python3 library/tools/check_laws.py` in a worktree of that
  branch. It printed `ok gompertz.yaml` and `3 entries, 0 problems`.
- **Not on main, measured by me:** `git merge-base --is-ancestor 5bdbed7b origin/main` fails. The
  entry is on its own branch and is not merged.

## 1. Arithmetic, redone independently

All of the following are my own calculations in Python, from the functional forms. They are not
observations.

- **Gompertz inflection.**
  - From W = W∞·exp(−e^(−k(t−tᵢ))), the inflection is at W/W∞ = 1/e = **0.3679**. This matches the
    entry.
- **VB-mass inflection.**
  - From W = W∞(1−e^(−Kt))³, the inflection is at (2/3)³ = 8/27 = **0.2963**. This matches.
  - For m′ = p·mᵃ − q·m, the inflection is at a^(1/(1−a)). At a = 0.99 that is 0.366. This lies
    within 0.002 of the Gompertz value, as expected, because Gompertz is the a → 1 limit.
- **Time from 1% to 99% of the asymptote.**
  - Gompertz: x = −ln(−ln f), so x(0.99) − x(0.01) = **6.127/k**. The entry says 6.13/k, which matches.
  - VB-mass: Kt = −ln(1 − f^(1/3)), so the span is **5.458/K**. The entry says 5.46/K, which matches.
- **Worked example: specific growth rate at W∞/1000.**
  - Gompertz: ln(1000) = **6.908**. The entry says 6.9, which matches.
  - VB-mass: (1/m)·m′ = 3K((W∞/m)^(1/3) − 1). That gives 27K at 1/1000 and 1.5K at 8/27, a ratio of
    **18**. This matches.
- **Laird form ⇔ autonomous form.**
  - Let u = ln(W∞/W). Then du/dt = −k·u, so the specific growth rate is k·u₀·e^(−kt).
  - So α = k·u₀, β = k, and W∞ = W₀·exp(α/β). This matches the entry's mapping.
- **Small-size divergence.**
  - The Gompertz specific rate diverges as ln(1/W). The VB-mass specific rate diverges as W^(−1/3).
  - So the entry's statement that VB-mass diverges faster is correct.
- **Labelling.** The entry marks every derived number as "calculated in this session" or
  `evidence: derived`.

## 2. Proxy

"Dispatched" stands in for the quantity that actually matters: whether a usable, checked entry
exists where readers will look.

- **What I measured.** The entry exists, comes from the claimed session, and passes the dimension
  gate. But it is **not on `main`**, so the built site and anything reading `main` do not see it.
- **Why this does not refute the claim.** The claim says "dispatched", not "merged". This is the same
  caveat recorded for challenges 44, 45, 48 and 53.

## 3. Hidden assumption, relaxed

The hidden assumption is that the dispatched task finished and produced content. I relaxed it: the
task could have been dispatched and then failed, been empty, or failed the gate. I tested this
against git and the gate, and the assumption holds.

A second assumption is that the gate certifies the content. It does not.

- **What the gate checks:** dimensions only.
- **What the gate does not check:**
  - It does not check `log()` arguments beyond their being dimensionless, and the entry says so
    itself.
  - It does not check the integrated forms. The entry says those were "checked by hand". I re-derived
    them in §1 and they are consistent.
  - It does not check the literature numbers.

## 4. Evidence level

`unknown` understates the evidence but does not overstate it. The right level is **"operational
record, verified from git and gate run"**.

I did **not** check the entry's literature numbers against their sources. These are Vaghi et al.
2020 (156% / 79% / 12.2%; 2600 vs ~1303 mm³; R² 0.968 / 0.923 / 0.99), Tjørve & Tjørve 2017 and
Benzekry 2014. Read-level for each, by me: **could-not-access (not attempted)**.

- **How the entry labels them.** It labels each with a read-level. Several are honestly marked
  search-summary or listing, for example Laird 1964, Winsor 1932 and Zweifel & Lasker 1976. It does
  not present any fitted value as an observation.
- **One small wording nit, not a defect in substance:**
  - **The problem.** The constant is named `alpha_beta_correlation_mouse_tumours`, but its values are
    R² (coefficients of determination), and the units field says so.
  - **Why it matters.** A reader who takes the name at face value would misread 0.968 as r. The
    corresponding r is √0.968 ≈ 0.984. That figure is my calculation, assuming the value is R² as
    labelled.

## 5. Regime or counter-example missed

- **Inside the scope of the claim (dispatch):** I found nothing. No counter-example applies to a
  dispatch record.
- **In the content:**
  - The previous challenge to von Bertalanffy (challenge 48) found that "VB has no inflection" holds
    only in length. **The Gompertz entry already incorporates this correction.** It gives VB-mass at
    8/27 and VB-length as having no inflection.
  - The zebrafish negative is stated with its scope: one web search, with FishBase, add-my-pet and
    Scholar not checked. I did not extend that search, so I neither confirm nor refute it.

## Sources

- Git history of `kganjam/delphi-frontier`, fetched 2026-11-04. Read-level: full-text.
- `library/laws/gompertz.yaml` and `library/pages/index.md` on
  `origin/claude/gompertz-growth-law-kx88sa`. Read-level: full-text.
- `library/tools/check_laws.py` on the same branch. I executed it; I did not read it line by line.
- `docs/research/fish/challenge-48.md` (commit `c13c0c42`), used for format and prior findings.
  Read-level: full-text.
- Vaghi 2020, Tjørve & Tjørve 2017, Benzekry 2014 and the other cited papers. Read-level:
  could-not-access (not attempted).
- Source session transcript. Read-level: could-not-access (not attempted).

```swarm-challenge
{"claim_id": 56, "outcome": "survived", "reason": "Commit 5bdbed7b from the same source session adds library/laws/gompertz.yaml, which passes check_laws.py and whose derived numbers (1/e, 8/27, 6.13/k, 5.46/K, ln1000, ratio 18) I re-derived independently; the entry is unmerged to main and its literature numbers were not checked by me.", "corrected_value": null,
  "depends_on": ["git commit 5bdbed7b on origin/claude/gompertz-growth-law-kx88sa and its Claude-Session trailer", "check_laws.py output on that branch (3 entries, 0 problems)", "Gompertz and VB-mass functional forms as written in gompertz.yaml"]}
```
