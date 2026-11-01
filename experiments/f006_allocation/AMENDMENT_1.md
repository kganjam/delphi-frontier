# AMENDMENT 1 to F006 PREREG (written 2026-11-01 09:06 PST, before any Arm 0 policy was scored)

State: the F003 base run (the source of the horizon ground truth and the signals) is still running; no Arm 0 number exists. Only a code
test on one 42-cell scratch group was run (its output was used to fix two labelling bugs, not read for policy results).
Trigger: `gemini-4-argon` critique, verbatim in `review/argon-prereg-critique.txt`. Original definitions stay; items below are added.

1. **Contamination disclosed (argon 1, accepted).** Before writing the `expert` rule I had read PROTOCOL8's published aggregates (25 of 26
   category changes Brusselator; category changes by ρ). The `expert` rule is therefore an *outcome-informed* proxy, not an ex-ante expert;
   it is relabelled `expert_informed`. The signals s1–s3 were chosen as generic convergence diagnostics without per-cell P8 data, but
   absence of influence cannot be shown. Arm 0 is a **retrospective demonstration of the evaluation machinery**, not a test of a mechanism.
   Added: a **horizon-only ground truth** variant (positives = `horizon_changed` only), which no one had seen when the policies were written.
2. **Utility in Part B (argon 2, accepted).** In Part B every check completes with receipts, so A3's `accepted` is 1 for every funded
   task and reduces to a task count (reported as `n_checked`, where `cheapest` wins trivially). Part B's utility is `positives` (an
   unresolved case surfaced) per unit cost; negative checks are reported with their cost. This is a different objective from A2, stated so.
3. **Gaming in Part A (argon 3, accepted, added to A3/A4):** (a) `decision_change` counts only a change of category, status, verdict or
   dependency edge, never a continuous re-estimate; (b) tasks are declared before the round with their predicate, and a reviewer may rule a
   predicate trivial, which voids its acceptance credit; (c) the budget binds on **measured ex-post** cost; overruns are charged to the
   policy that funded the task and reported per policy.
4. **Baselines (argon 4, accepted).** B1 is additionally judged against **all** baselines (A6 rule). Added baselines: single-feature
   `s1/c`, `s2/c`, `s3/c`, and `expert_informed_costaware` (same priority tiers, cheapest first within a tier). Also reported, labelled
   as not a policy: `oracle_upper_bound` (ground truth per unit cost).
5. **Path dependence (argon 5, accepted as a limit).** In Part B each cell's positive is independent of others (no redundancy). In Part A a
   counterfactual replay would need a redundancy/dependency model; this is a further reason the Part A replay is not run.
