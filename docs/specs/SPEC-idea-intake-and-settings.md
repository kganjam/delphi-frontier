# SPEC — Idea intake, due diligence, promotion, and project settings

**Status:** normative. Implemented in `designswarm` (`idea`, `idea_check`, `idea_score`, `setting`,
`project_capability`).

---

## 1. The principle: an idea is not a project

Someone types *"design a fish that can fly."* That is an idea. A project is dozens of subproblems,
hundreds of agent-hours and real money.

**Most ideas should die, and the system's job is to kill them cheaply and record why.** The expensive
failure is not rejecting a good idea; it is spending a week discovering that an idea was blocked by
something a twenty-minute check would have found. The second-most expensive is re-investigating the
same idea six months later because nobody recorded the first answer.

So intake has three stages with increasing cost, and nothing skips a stage:

```
  CAPTURE  →  DUE DILIGENCE  →  RANK  →  PROMOTE
  (free)      (~20 min)         (cheap)   (expensive, deliberate)
```

---

## 2. Capture

**REQUIRED:** `body` — what the person typed, **verbatim**. It is never edited, tidied, or replaced
by a cleaner restatement.

**REQUIRED before triage:** `normalised_question` — the design question in a form the system can act
on, written by an agent and stored **separately**. The separation is the point: a normalisation is an
interpretation, and interpretations are wrong often enough that the original wording must survive to
be re-read.

**OPTIONAL:** `target_scales`, `submitted_by`.

**INVALID:** an idea whose `body` has been rewritten, or one promoted without a `normalised_question`.

---

## 3. Due diligence — seven checks, each a row

Each check is its own row so that a partial assessment **looks partial**. A single verdict field
would let four skipped checks and three passes read as "assessed".

| Check | The question | Kills the idea when |
|---|---|---|
| `prior-art` | Has this been done, or definitively ruled out? | It is solved, or a published result closes it |
| `physical-plausibility` | Does any law in the library forbid it outright? | A `constraining` law is violated by orders of magnitude |
| `binding-constraint` | What is the single hardest barrier, with a number? | The barrier has no conceivable route |
| `existing-coverage` | Does another project already answer this? | A `derivation` from existing work suffices |
| `tractability` | Can progress be made with the tools we have? | Every route needs a capability nobody has |
| `ethics-and-safety` | Dual-use, welfare, containment, regulatory? | A real hazard with no mitigation |
| `resource-estimate` | What would it cost to reach a first answer? | The cost exceeds any plausible value |

**`binding-constraint` is the one that earns the most**, and the fish project is the evidence: the
launch-velocity barrier was a ratio computable in one session, and it set the whole project's shape.
An idea whose binding constraint nobody can name has not been assessed, whatever the other six say.

**A `fail` does not automatically reject.** A physically-forbidden idea can still be worth running
*as a refutation* — the negative result is a reusable artifact. The decision is recorded in
`decision_note` with its reason.

---

## 4. Ranking

`idea_score` applies a frozen `rubric`, by a calibrated grader, exactly as
[the design loop](../architecture/the-design-loop.md) specifies.

**The score is a function of the CHECKS, never of the idea's wording or its author.** This is
AGENTS.md §1 rule 3 — never compute a score from anything but the thing being scored — and the
failure it prevents is specific: a well-written idea scoring above a badly-written better one.

**INVALID:** a score recorded before the seven checks have `verdict` set (including `not-run`,
explicitly).

---

## 5. Promotion

**REQUIRED to promote:** all seven checks have a verdict; at least one scored above the rubric's
threshold; a `project` row is created; `idea.project_id` is set and `status` becomes `promoted`.

Promotion is **deliberate and logged**. It is the moment cost starts, and the `decision_note` must
say what the project is expected to settle, so that abandoning it later is a comparison against a
stated expectation rather than a vibe.

**A rejected idea is never deleted.** `status = 'rejected'` with a `decision_note`, so the same idea
arriving again is recognised as `duplicate_of` rather than re-investigated. A rejection with no
reason is worse than no rejection, because it destroys the information without saving the work.

---

## 6. Settings — two levels, and some that cannot be changed

A project setting overrides a system setting of the same key. **Nothing else overrides anything.** A
deeper chain is where configuration stops being auditable, and "which value is actually in force"
becomes a question nobody can answer quickly.

### 6.1 Locked settings

`locked = true` marks a setting an agent may **read but never change**. These are not configuration;
they are the floor.

| Key | Why it is locked |
|---|---|
| `honesty.evidence_required` | Every value carries how it was obtained |
| `honesty.read_level_required` | A search summary is a lead, not evidence |
| `honesty.supersede_never_overwrite` | ASK dimension 4 |
| `honesty.grader_must_be_calibrated` | An uncalibrated grader measures itself |
| `billing.forbid_owner_card` | No action may bill the owner's payment method |
| `billing.forbidden_accounts` | Owner instruction: `api_allen`, `ent_allen` |

**A system that can relax its own standards will**, because relaxing them always makes the next
number look better. The list of locked keys is itself not editable by an agent.

### 6.2 Tunable settings

`swarm.max_concurrent_cloud`, `swarm.nebius_max_in_flight`, allocation policy, rubric thresholds,
budget ceilings. These are operational and are expected to change; each carries a `reason`.

### 6.3 Capabilities

`project_capability` declares what the swarm may use on a project — MCP servers, skills, models,
tools, datasets — **read at dispatch time rather than compiled in**, so a project can be given a
genome browser and denied a payment API without changing any code.

Measured constraints belong here with their evidence, not in a comment: `swarm.nebius_max_in_flight`
is `1` because the server enforces it, which was established by hitting it.

---

## 7. Acceptance

1. Every idea retains its verbatim `body`.
2. No promotion without seven verdicts and a `normalised_question`.
3. No score computed from anything but the checks.
4. Every rejection carries a reason and is retained.
5. No agent writes a `locked` setting.
6. Every capability a project uses is declared in `project_capability`.

---

## 8. What this does not establish

- **No checker enforces any of §7.** The schema permits the invalid states the spec forbids.
- No rubric for idea scoring exists yet, so §4 cannot run.
- One idea has been entered, retrospectively, as a worked example. A pipeline with one item is an
  illustration, not a test.
- `project_capability` is declared but nothing reads it at dispatch; the swarm's capabilities are
  still compiled in.
