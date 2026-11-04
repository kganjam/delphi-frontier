# Replication attempt — claim 76 ("launch margin ~4-7x")

**Outcome: CANNOT TELL. I could not re-derive the value because its inputs are unavailable.**

## The claim as I was given it (answer removed)

> The launch margin should be read as ~4-7x rather than a single ~7x, because the
> measured population spans a factor of three and 120 fps likely underestimates th[...]

The stated location of the inputs is `S21-deepen.md`.

## What I searched, and how far (scope of the negative result)

| Search | Scope | Result |
|---|---|---|
| `git ls-files` filtered for `S21`, `deepen`, `fish` | every tracked file on `claude/replicate-76-launch-margin-bta9gc` | no match |
| `git log --all -- '*S21*'` | full history of every local ref (`claude/replicate-76-...`, `work/frontier-foundation`, and their remotes; 30 commits) | no match |
| `git grep -i "launch margin\|120 ?fps\|C-start\|mauthner\|escape latency"` across `git rev-list --all` | every blob in every commit reachable from those refs | no match |
| GitHub code search `filename:S21-deepen.md` | all repos this session's GitHub access reaches | 0 results |
| GitHub code search `"launch margin" repo:kganjam/delphi-frontier` | the scoped repo | 0 results |
| GitHub code search `S21-deepen` | all reachable repos | 0 results |
| GitHub code search `"launch margin" fish` | all reachable repos | 24 hits, all in unrelated third-party repos outside this session's scope (e.g. a bank-fishing site finder). I did not open them. |

`docs/research/fish/` did not exist before this file. The repo has no fish or
biomechanics material at all. Its findings and results cover protein and variant
problems (ProteinGym, KCNE1, OCA2).

## Why I did not reconstruct the number from the literature

The claim does not say what the "launch margin" is a ratio of. It does not name the
organism, the behaviour (C-start, jump, prey strike, etc.), or the threshold the margin
is measured against. Guessing those, then pulling literature values into the gap, would
mean inventing the inputs. The honesty floor forbids that. Every input below is therefore
`unknown`:

| Input | Value | Source | Read-level |
|---|---|---|---|
| Definition of "launch margin" (numerator and denominator) | unknown | `S21-deepen.md` (not found) | could-not-access |
| Measured population range ("spans a factor of three") | unknown | `S21-deepen.md` (not found) | could-not-access |
| Camera frame rate and the size of its bias (120 fps) | 120 fps is quoted in the claim; the size of the bias is unknown | `S21-deepen.md` (not found) | could-not-access |
| The quantity that 120 fps underestimates | unknown (the claim text is cut off) | — | — |

## Arithmetic

None was possible. The only check I can make uses nothing but the numbers in the claim.
It is an inference of mine, not a derivation from data: if the upper end is ~7x and the
population spans a factor of three, then dividing by 3 gives a lower end of ~2.3x, not ~4x.
A ~4x lower end would need a spread of about 7/4 ≈ 1.75x in the margin. That fits with
"spans a factor of three" only if the margin scales with the population variable
sub-linearly, or if only part of the range applies. I cannot test either without the
source. This is an internal-consistency question for whoever holds `S21-deepen.md`, not
a finding.

## Comparison with the recorded value

The recorded value is not in this repository (searches above), so I could not compare it.
The ~4-7x in the prompt is the claim itself. I did not derive it independently and do not
count it as agreement.

**Verdict: CANNOT TELL.**

To unblock this, add `S21-deepen.md`, or the primary sources it cites, to the repo or the
session, then re-run.

```swarm-replication
{"claim_id": 76, "my_value": "unknown (inputs in S21-deepen.md not accessible)", "agrees": null,
  "note": "S21-deepen.md is absent from every ref of kganjam/delphi-frontier and from GitHub code search, and the claim does not define 'launch margin', so I could not re-derive it without inventing inputs."}
```
