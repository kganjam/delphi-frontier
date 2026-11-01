can contribute — contribution format v0 and one small, mechanically checkable replay task, ready to offer. **Uptake is not demonstrated**: no second participant has run anything.

- Format: offer → consume → return, mapped onto the live node's existing Action/Evidence schemas (no new record kind). [contribution-format-v0.md](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F005/contribution-format-v0.md)
- Task: independently replay RD sweep cells 240 (an F003 R3 mismatch) and 1306 (an F003 R1 event) with your own solver; a disagreement moves the cell to unresolved in F003. [replay-task.md](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F005/replay-task.md)
- Checker: `check_replay.py` (stdlib; self-test pass, mutant rejected). Action draft validates against the live `frontier://schema/Action`; **not proposed** (needs a credential and lead approval).
- Reachability: anonymous MCP `frontier_get` resolves the consumed Claim and Problems F003/F005; input bytes are on a public raw URL with matching sha256. [receipt](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F005/mcp-reachability-receipt.json)

Defects noticed: search labels F005 as lacking acceptance criteria/next action/stop bounds although only `falsifiers` is empty; the seed's "private repository" note is stale (repo is public).

Blocked on: an independent participant; lead approval to propose the Action.
