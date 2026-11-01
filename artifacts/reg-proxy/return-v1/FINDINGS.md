# Return v1 audit and transport diagnosis (partial_data preserved)

Raw: /data/artifacts/delphi-evolve-rethink/gcp/regulatory-context-v1/frontier-cpu-20261031-02/final-d13aa1b88dd6468f9ada0d9a7654a099/science (hashes in manifest.json). Audit criteria frozen at 67b16d5 before any returned file was read; no network request made.

## Audit (audit.json): verdict consistent, 10 of 10 checks pass
- 330 identities present, none duplicated, missing or extra; geometry matches controls.json.
- Completion recomputed as partial_data (165 usable, 165 library_unavailable); equals results and receipt.
- 181 requests, 89,710,783 charged bytes, max library 18,014,486, elapsed 76.3 s; all within the frozen caps and equal to the receipt.
- 165 response hashes in result rows all link to ok requests; summary recomputes exactly; no score-like keys; no LEN.
- "Consistent" means the files agree with the frozen protocol and each other. It is not biological validation. Fragment counts in audit.json observations are listed, not interpreted here.

## What the data are
Usable: 2dpa2, 4dpa1, 4dpa2, 6dpa1, 6dpa2 (33 windows each). Unavailable: 0dpa1, 0dpa2, 1dpa1, 1dpa2, 2dpa1. So the time course is incomplete: no 0 dpa (uninjured) and no 1 dpa library is usable, and 2 dpa has one of two replicates. The result cannot be called a 0-6 dpa context assay.

## Transport diagnosis (diagnosis.json; from requests.json only)
- 11 failed attempts, all one signature: HTTP 206, 0 body bytes, short_read.
- All 11 are the full-index range request (bytes 0 to size-1 of a .tbi.gz). None of the 165 later window requests failed (0 failed, 165 ok).
- Failures cluster in time: attempts at 0.00 to 26.15 s; first success at 33.43 s (2dpa2 index, second attempt). After that all 5 remaining index requests and all 165 window requests succeeded.
- Both attempts for 5 libraries failed. The second attempt followed the first by 0.1 s for four libraries, by 24.0 s for 1dpa2 (first attempt stalled ~24 s, then empty) and by 7.3 s for 2dpa2 (first attempt ~7 s, then empty; second attempt succeeded).
- Not logged, so not knowable from this return: response headers (Content-Length, Content-Range value, Connection, cache headers), whether the connection closed early or declared length 0, per-request wall time.
- Earlier observation from this session, a different network (this host), not part of the return: the same "headers promised N bytes, 0 delivered" signature occurred on the first request of three of about nine probe requests (the whole .tbi.gz without a Range header twice, and a 1 KiB Range of a fragments file once), and a retry succeeded. So it is not specific to Google, to Range requests, or to the index files. It does not identify a cause.
- Cause: not determined. Competing explanations the data cannot separate: server-side cold-object behaviour with first requests failing; a time-since-start effect; or something about the full-index range request. Eleven attempts, six index requests: this sample cannot tell a failure that persists for seconds from independent random failures at a high rate, so it does not support either.

## Consequence for the code
The failure was classified short_read and handled by the frozen two-attempt rule, so it was recorded and bounded correctly; the repair-time controls simulated an early-closed body but not a 206 whose body is empty from the start. The first failed index made every window of that library library_unavailable, which is why one transport failure became 33 unusable identities.
