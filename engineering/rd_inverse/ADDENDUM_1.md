# Addendum 1 (pre-dispatch, from infra's source-only review; no outcome has been read)

protocol.json is unchanged (sha256 8f6fee6f15856bfeae105bcb73bbeea853e8f52196bf3e59ce80cb938e8ce346, same as the frozen 4a622a4 file). Every frozen criterion stands: targets, bounds, 64 evaluations, scores, gate A, gate B (RMS <= 0.02), failure rule (nonfinite or |field| > 1000), 900 s cap. This addendum changes implementation and retention only.

1. Raw fields retained: independent_fields.npz (true and each selected candidate for all 3 fresh seeds and all 3 N/dt configs, plus base fields) and validation_fields.npz (oracle and negative fields with their parameters).
2. All-failed/empty candidate sets: select returns none; selection.json carries status no_valid_candidate, near-optimal reports count 0; traces retained; never a fabricated success; methods without a selection are listed in independent_checks.json.
3. A nonfinite or >1000 target fails closed: native fields kept in targets.npz, receipt.status invalid_target, search not run, no target replaced. NaN in any JSON is written as null.
4. concentration_stats.json reports raw minima and negative-cell counts for targets, all evaluated candidates, validation controls and independent checks. It is reporting only; the failure rule is not changed and nothing here establishes concentration validity.
5. Near-optimal ranges are descriptive ambiguity among finite sampled candidates, not proven structural nonidentifiability (the protocol key name predates this wording; the wording here governs).
6. CPU step rates are CPU evidence only. GPU runtime is unknown; the bound is the 900 s outer kill (timeout in job.sh, plus the in-run phase check) with durable per-phase outputs and traces_partial.json after each round.
