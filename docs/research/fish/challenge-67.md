# Challenge 67: "LAWENTRY glide-ratio dispatched"

**Verdict: SURVIVED.** The claim is narrow and the record supports it. Separately, I audited what the
dispatch produced (the glide-ratio entry). That audit found no refuting error. It found three
non-refuting defects in the entry, listed below so they are not lost. They are not grounds against
this claim.

## 1. What the claim says, and what it does not say

The claim is an administrative record. It says that a law-library job for the glide ratio was sent
to a cloud session (`session_01HsfzftZ4uzxNPXv7tEXKWM`). It makes no scientific assertion and has no
numerical value (`value: n/a`). The recorded evidence level is `unknown`.

What I checked (observed in this repository with `git fetch`, `git log` and `git show`, 2026-11-04):

- Branch `origin/claude/glide-ratio-law-d2al63` exists. Its tip is commit `f6dec5c8`, "Law library:
  glide ratio as lift-to-drag, and the sink-rate relation", dated 2026-11-04 08:18 UTC.
- That commit's trailer reads `Claude-Session: https://claude.ai/code/session_01HsfzftZ4uzxNPXv7tEXKWM`.
  This is the claim's source session.
- The commit adds `library/laws/glide-ratio.yaml` (178 lines).
- `swarm/swarm.py` (on the same branch) prints `dispatched <sid> <account> <session_id>` only after a
  successful session creation. A failure raises `SystemExit` instead (lines 97–115). The claim's
  wording matches that log line.

So a session was dispatched and it produced the entry. **Evidence level:** the claim was recorded as
`unknown`. It could honestly be upgraded to *observed*, meaning a commit attributable to the named
session exists. I did not see the dispatch log line itself. I inferred the dispatch from the commit
that the session produced.

### Proxy check

"Dispatched" stands in for "the law entry exists and is sound". Those are different things:

- **Not merged.** `git branch -r --contains f6dec5c8` returns only the entry's own branch. The entry
  is not on this challenge branch's base. Reading "dispatched" as "in the library" would be wrong.
  The claim does not say that, so this does not refute it.
- **The gate's "ok" is a weak proxy for correctness.** I ran `library/tools/check_laws.py` on that
  branch's `library/` tree, with output `ok glide-ratio.yaml … 3 entries, 0 problems`. That check is
  dimensional only. `C_L` and `C_D` are dimensionless, so it cannot detect a wrong exponent on them.
  It also cannot detect that the checked equation string
  `V_s = V_h*F_D/F_L = (2mg/(ρS))^1/2 * C_D/C_L^3/2` states as an exact equality something that is
  only approximate: the second equality drops cos^(3/2)θ. The entry admits this in comments and in
  `where_it_breaks (3)`, but the machine-readable equation still asserts equality. For that reason I
  re-derived the content by hand (§2) instead of trusting the gate.

## 2. Independent arithmetic on the produced entry

All values below are *calculated* by me from the stated inputs. None are observations.

| Item | Inputs | My result | Entry's value |
|---|---|---|---|
| Exact sink-rate relation | L = ½ρV²SC_L = W cosθ, tanθ = C_D/C_L, V_s = V sinθ | V_s = √(2W/ρS)·C_D/C_L^1.5·cos^1.5θ | same |
| Jackdaw V/V_s at min sink | 7.4 / 0.62 | 11.94 (11.89 using the horizontal component, θ = 4.79°) | 11.9 |
| cot of squirrel glide angle | cot 26.8° | 1.980 | 1.98 |
| Small-angle error at G = 3 | θ = 18.43°, cos^1.5 = 0.924 | 7.6 % | "~8 %" |
| Overstatement at G = 1 | cos^1.5 45° = 0.595 | ×1.68 | ×1.68 |
| Zebrafish design check | m = 4e-4 kg, S = 2e-3 m², ρ = 1.225, C_L = 0.8, C_D = 0.2 | √3.203 = 1.790 m/s; C_D/C_L^1.5 = 0.2795; approx. V_s 0.500; θ = 14.04°; exact V_s 0.478 m/s; airspeed 1.97 m/s | 0.50 / 0.48 / ~2.0 |
| Turning sink penalty | L = nW, V ∝ √n, D ∝ n | sink ∝ n^1.5 | n^1.5 |
| Density sensitivity | V_s ∝ ρ^-½, Δρ = 10 % | ≈5 % | ≈5 % |

Every number reproduces. The derivation of the minimum-sink condition (maximise C_L^1.5/C_D) is also
correct, under the small-angle assumption it states.

## 3. Source checks (read-levels stated)

- **Rosen & Hedenström 2001, J Exp Biol 204:1153.** Read level: *abstract*, via the Europe PMC REST
  record. Confirmed: minimum sinking speed 7.4 m/s, sink 0.62 m/s, best glide 8.3 m/s, max L:D 12.6
  at 8.5 m/s, Re 38 000–76 000 over 6–11 m/s. Matches the entry.
- **Bahlman et al. 2013, J R Soc Interface.** Read level: *abstract*, via Europe PMC. Confirmed:
  "do not glide at equilibrium", "continuously changing velocities, forces and force coefficients",
  and that the equilibrium model "may not be realistic for shorter distances between trees". The
  entry's phrasing "more lift than body weight" paraphrases the abstract's "more lift than needed to
  balance body weight". The meaning is the same.
- **Park & Choi 2010, J Exp Biol 213:3269.** Read level: *abstract*, via Europe PMC. Species
  *Cypselurus hiraii*. Forces were measured on **models**. The abstract gives **no numerical L/D**:
  it says only that L/D is maximal near 0° attack and that sea-surface proximity reduces drag and
  raises L/D. This matches the entry, which says it did not obtain the numbers.
- **Vernes 2001, J Mammal 82:1026.** Read level: *search-summary* (one standard web search). The
  summary reports a glide angle of 26.8°, a glide ratio of 1.98 and 100 glides. This matches the entry.

## 4. Non-refuting defects in the produced entry (my inference, for the entry's owner)

1. **A source disagreement the entry missed.** The same search summary reports Scheibe et al. (2006)
   for *G. sabrinus* in Alaska: 168 glides by 82 squirrels, with mean glide angles of about 36–41°.
   My arithmetic gives trajectory ratios of cot 41.3° ≈ 1.14 to cot 36.3° ≈ 1.36. Vernes reports 1.98.
   The entry quotes Vernes alone. Read level for Scheibe: *search-summary*. Full citation not
   verified, and I did not read the paper. The two sources disagree, and the disagreement should be
   recorded as it is, not averaged. It supports the entry's own point that field ratios are not L/D.
2. **Machine-readable equation overstates exactness** (§1). Suggested fix: make the checked equation
   carry the exact form, or split it into two equations with the approximation labelled.
3. **`taxa_with_measured_support` lists *C. hiraii* as "mounted specimens".** The abstract says
   "models", and the entry has no number from that source. The support it gives is qualitative
   (ground effect raises L/D), not a measured L/D. Relatedly, `reynolds_range_with_measured_support`
   names only the jackdaw range. The flying-fish Reynolds number was not given or searched.

None of these makes the claim "LAWENTRY glide-ratio dispatched" false.

## 5. Scope of negative searches

- I searched branches only in this repository (`git branch -r`, 316 remotes), for the substrings
  `glide`, `lawentry` and `67`. I found no other glide-ratio entry or competing dispatch record.
- I did not open the `swarm` database. I did not read the dispatch log line, the `claim` table row or
  the dispatch timestamp. The claim's existence as a row is taken from the challenge prompt.
- Web: four Europe PMC abstract fetches (one returned HTTP 500 and was retried by DOI query) and one
  standard web search for Vernes 2001.

## Why it survived

The claim asserts only that a dispatch occurred. A commit attributable to the named source session
exists and contains the promised entry. The entry's arithmetic reproduces independently, and its
primary numbers match the abstracts I read. I could not find a reading of the claim's actual words
under which it is false. The defects above are real, but they belong to the entry, not to this claim.

```swarm-challenge
{"claim_id": 67, "outcome": "survived", "reason": "A commit (f6dec5c8) carrying the source session's trailer exists on origin/claude/glide-ratio-law-d2al63 and adds library/laws/glide-ratio.yaml, so the dispatch happened and produced the entry, whose arithmetic and abstract-level numbers reproduce independently; the entry is not merged and has non-refuting defects, neither of which the claim denies.",
  "corrected_value": null,
  "depends_on": ["git commit f6dec5c8 on origin/claude/glide-ratio-law-d2al63 with Claude-Session trailer session_01HsfzftZ4uzxNPXv7tEXKWM", "swarm/swarm.py dispatch() semantics (log line printed only on successful session creation)", "library/tools/check_laws.py output on that branch (dimensional gate only)", "Rosen & Hedenstrom 2001 abstract (Europe PMC)", "Bahlman et al. 2013 abstract (Europe PMC)", "Park & Choi 2010 abstract (Europe PMC)", "Vernes 2001 search-summary", "Scheibe et al. 2006 search-summary (unverified citation)"]}
```
