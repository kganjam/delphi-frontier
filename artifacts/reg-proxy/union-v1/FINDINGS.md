# Union v1 + recovery-v1 (partial_data, 271 of 330 identities usable)

Lineage: artifacts/reg-proxy/lineage/{v1,recovery-v1}/ are byte copies of the two raw science directories; manifest.json holds their hashes and the infra manifest hashes. Neither original run is edited. Contract frozen at 8543c5d; one recovery only; no further retry under it.

## Verified (commands run, offline)
- Recovery audit (`audit_return --recovery`): consistent, 10/10 checks. 165 identities present, 106 usable; 165 requests, 57,772,362 charged bytes (receipt equal); 96.0 s; all pins incl. contract and parent results sha; header allow-list respected; index waits 0/15/45 s respected on t_clock; 106 response hashes linked; summary recomputed equal.
- Union (`merge_union`, then `--verify`): completion_status partial_data; 330 identities present, 271 usable (165 from v1 + 106 from recovery-v1), 59 unresolved. No overlap, no input drift, every union row equals its source row. Union sha256 74441883b37c8bd1aa2c07cc499aad74d94026396d983b3348dc4fe78fe2749a. Parent results sha256 f2eb5178…, recovery results sha256 d2d60603….
- Per library after the union: usable 0dpa1, 0dpa2, 1dpa1 (recovered, 33 each) plus 2dpa2, 4dpa1, 4dpa2, 6dpa1, 6dpa2 (from v1); 1dpa2 has 7 of 33 usable identities; 2dpa1 has none (index failed). Unresolved: 1dpa2 26 windows (empty_206), 2dpa1 33 (library_unavailable).

## What the data now are
A 0, 1, 2(partly), 4, 6 dpa descriptive set: uninjured 0 dpa now has both replicates, 1 dpa has one full replicate and 7 identities of the second, 2 dpa has one full replicate (2dpa2). It is still not the planned complete 10-library design. 1dpa2 is mixed (7 usable windows, 26 not) so its per-window ratios exist only where a window and both its comparison windows are usable.

## Transport observation (requests.json; cause UNKNOWN)
- 165 requests: 110 ok, 55 failed. Every failure is HTTP 206, Content-Length equal to the requested length, a matching Content-Range, 0 body bytes, about 0.12 s (empty_206).
- The first 110 requests all succeeded (0dpa1, 0dpa2, 1dpa1 fully, and the first 8 requests of 1dpa2: index plus 7 windows), 57,772,362 bytes in 29.3 s. From request 111 (29.3 s) every later request failed until the run ended at 96.0 s: 26 window reads (2 attempts each = 52 requests) of 1dpa2 and the 2dpa1 index on attempts at 35.6, 50.7 and 95.8 s.
- The 15 s and 45 s waits did not help for 2dpa1: all three index attempts returned empty 206.
- Versus v1: there the first 11 requests failed (0 to 26 s), then every later request succeeded. So failures are episodic, not a fixed per-client byte or request quota (v1 passed 89.7 MB; this run failed after 57.8 MB). Both runs fit server-side episodic behaviour, rate or concurrency effects on a shared object host, or something else; the logs do not separate them. Not logged: any header beyond the seven allow-listed, e.g. connection or cache hints.
- The experimental schedule gave no benefit within its 15/45 s waits in this run; one run is not evidence about longer waits.

## Not claimed
Nothing here validates the counts as regulatory function; no biological interpretation of accessibility; no thresholds or tests; LEN excluded. Counts from the two runs are never merged or rescaled; each library's windows and comparison windows come from one run.
