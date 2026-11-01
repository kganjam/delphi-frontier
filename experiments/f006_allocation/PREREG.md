# F006 preregistration: the decision-maker's objective, acceptance predicates and resource constraints, before any mechanism

Author: `claude-fseries` (Claude Opus 5.5), single reader, not independently reviewed. Written 2026-11-01 Seattle PST, before any allocation
arm below was computed. Issue: kganjam/delphi-frontier#6 (F006). This document does **not** choose a voting or market mechanism; per the
issue's bounded action it fixes what any mechanism would be judged against. Part B is one small arm that can run today; Part A is the
commons-level design that cannot yet (blocked on F005, see the end).

## Part A — commons-level design (frozen definitions)

### A1. Decision-maker and decision
The decision-maker is the **project lead session for a research problem** (today: the lead reviewing F001–F006), who holds a constrained
resource and must decide, at each dispatch point, which pending **task** (a bounded action with a stated acceptance predicate) receives it.
The decision is the ordered choice of tasks to fund until the resource is exhausted. Voting, attention signals or markets are only possible
*inputs* to that choice; the objective below is what the choice is scored on.

### A2. Objective (utility), fixed before mechanisms
U(policy) = Σ over funded tasks of [ accepted(t) · w_accept + decision_change(t) · w_decision ] subject to Σ cost(t) ≤ B, reported
**per unit of the constrained resource**, with w_accept = 1 and w_decision = 1 (two counts reported separately as well as summed; no
weights are tuned after results). Secondary objectives are **constraints**, not weights (A5).

### A3. Acceptance predicates (what counts; the task's own frozen predicate, judged by someone other than the task's author)
* `accepted(t)` = 1 iff the task's preregistered acceptance predicate, frozen before dispatch, is judged satisfied by a reviewer who did not
  author the task and did not see which policy funded it. A COMPLETED provider state, a commit, a vote or a reputational score is **not**
  acceptance.
* A task whose predicate was judged **failed** or whose result is **negative** (the preregistered prediction did not hold) is a valid
  outcome: it counts as `accepted(t) = 1` if its receipts are complete and the failure is correctly reported; it counts 0 only if the
  receipts are incomplete or the claimed outcome is not reproduced. (This is the protection that keeps failed and negative work from
  scoring as waste.)
* `decision_change(t)` = 1 iff the task's result changed a recorded downstream decision: a published number, a category, a claim status,
  a dependency edge or the next action of another problem, with the changed record named. Changes are counted from the record history,
  not from the task author's description.

### A4. Constrained resources (each measured from a receipt, never estimated after the fact)
* GPU-minutes (Nebius provider start→end, CLI-read), CPU core-seconds (`systemd-run` scope accounting or wall × threads), reviewer
  minutes (timestamped review records), and LLM tokens (provider usage receipts). One allocation experiment fixes **one** primary
  constrained resource; the others are reported as costs.
* Cost must be **declared ex ante** (an estimate recorded before dispatch) and **measured ex post**; policies may only use the ex-ante
  declaration. A task without an ex-ante estimate cannot enter a policy comparison (it is listed, not dropped silently).

### A5. Constraints that protect coverage and exploration (fixed now)
* **Coverage floor:** every problem with at least one ready task receives at least one funded task per allocation round, unless the
  round's budget is smaller than the number of such problems (then problems are served in a fixed random order, recorded).
* **Exploration/replication reserve:** 20% of each round's budget is allocated by stratified random choice among ready tasks, regardless
  of any signal; replications and controls are eligible.
* **Negative-work accounting:** failed and negative results are reported with their costs in every table, by policy.
* **Separate signals:** `interest` (who is following; reactions), `resource` (offers, cost estimates), and `blocking` (declared typed
  dependencies: "blocked by this") are three separate inputs; no policy may combine them into one undeclared score, and none may use
  outcomes.

### A6. Baselines (every mechanism is compared against these, at the same budget)
* **Expert order:** the order the lead actually dispatched (from timestamps), or for a replay, an order written down by a domain expert
  before outcomes are visible.
* **Simple allocation rules:** (i) uniform random (≥ 100 seeds, reported as a distribution), (ii) stratified round-robin over problems,
  (iii) cheapest-declared-cost first.
* A mechanism "improves useful progress" only if it beats **all** baselines on U per unit resource at two preregistered budgets while
  satisfying A5, with the paired comparison and its uncertainty reported; otherwise the result is reported as not improving.

### A7. Pinned task pool (what exists today, and its readiness)
Candidate pool: the team's own Nebius jobs in `results/resources/hackathon-usage.json` (sha256
`d18a9bfd0ce48fc491d3fc3f0c14a3869b5ecfe1749cb7813b9537d93a7c8912`). Part B's `pool_readiness.py` counts, per job, which A3/A4 fields
exist in the repository. A replay on this pool is **not** run here: acceptance judgements by a non-author reviewer blind to policy do not
exist, ex-ante cost estimates are mostly absent, and outcomes were produced under one (the actual) order, so a counterfactual order cannot be
scored without a dependency model.

## Part B — Arm 0, runnable today: allocating scarce numerical-refinement checks across the F003 sweep cells

A bounded, within-project instance of the same question where **ground truth exists for every task**, so a counterfactual allocation can be
scored exactly (no selection problem). It tests the evaluation machinery and the baselines; it is **not** evidence about community
attention, votes or markets.

* **Task pool (pinned):** the 2,520 cells of the frozen nonlinear sweep (`rows.jsonl` sha256 `a32c2bf7…c4882`). A task = "run the
  refinement checks on this cell" (dt/2 and 2T horizon).
* **Constrained resource:** cell-step cost c_i = N_i × T_i / dt (proportional to CPU time of solver A), declared ex ante from the grid
  rule and the horizon rule (both known before any run). Budgets: **10% and 25%** of Σ c_i.
* **Acceptance predicate (ground truth):** `positive(i)` = the cell is not converged under the refinement, i.e. its NCA category or
  patterned dominant mode changes between dt 0.02 and 0.01 (P8-1, recomputed per cell with the NCA category rule, solver B fixed at the frozen rows' field B, from the per-cell GPU arms
  `results/compute/p8/gpu/results/fwarm8-warm-p8-dt-halving/parts/00-frozen-grid-base-dt2/results.jsonl` sha256 `3a12582b8444d5bccfa34c1ea5beab9a1eb64adce4194300db69248f852c6020`;
  the recomputed totals must equal P8-1's published 26 category changes / 28 mode flips, else this input is reported as not reproduced), OR it is `horizon_changed`
  in the F003 2T arm. `decision_change(i)` = the positive cell is a member of an R1, R2 or R3 numerator or of the unresolved mass at dt 0.02,
  T (so its status change moves a published number).
* **Ex-ante signals** (available from the base run at dt 0.02 to T only, before refinement): s1 = spectral peak margin (ratio of the
  second-largest to the largest DCT coefficient of u(T)); s2 = relative amplitude change 0.9T→T; s3 = stationarity residual ‖du/dt‖∞ at T;
  s4 = |ρ − 1|; model. No outcome field is read by any policy.
* **Policies:** `expert` = near-onset first (ascending s4), Brusselator before Schnakenberg, then ascending ε — written now as the expert
  prior (a proxy: no human expert wrote it); `uniform` = random order, 200 seeds; `stratified` = round-robin over (model, ρ, ε) strata,
  random within, 200 seeds; `cheapest` = ascending c_i; `signal` = descending score z(s1) + z(s2) + z(s3) (z = rank-normal over cells),
  per unit cost; `signal+floor` = `signal` with 20% of budget by `stratified`.
* **Reported per policy and budget:** positives found, decision-changing positives found, both per 10^9 cell-steps; coverage = fraction of
  the 42 (model, ρ, ε) strata with ≥ 1 check; negative work = checks that found nothing, with their cost. Random policies as median and
  5–95% range over seeds. No significance test; no weights tuned after results.
* **Predictions (can fail):** B1 `signal` finds more positives per unit cost than `uniform`'s median at both budgets. B2 `signal` alone
  covers fewer strata than `stratified`; `signal+floor` keeps ≥ 80% of `signal`'s positives while covering ≥ 90% of strata. B3 `expert`
  beats `uniform`'s median.

## What remains blocked (Part A)
Running Part A needs: a second, independent reviewer to judge acceptance blind to policy; ex-ante cost declarations on future tasks; and
contributor diversity (F005: one independent participant has not yet been demonstrated). Part B cannot answer F006's question about
attention signals and community allocation.
