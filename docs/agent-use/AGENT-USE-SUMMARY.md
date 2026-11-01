# Agent-use summary: delphi-frontier and delphi-evolve (our side only)

Written for kganjam/delphi-frontier issue #8, to sit beside the Delphi team's own record. It was
written without reading the Delphi team's numbers (rule 7). The machine-readable copy is
[`agent-use-summary.json`](agent-use-summary.json). Every command is listed under
[Commands run](#commands-run).

**Who wrote it:** one Claude Opus 5.5 session (tmux `ff-agentuse`), working from 2026-11-01 08:37 PST
(16:37 UTC) to about 09:15 PST (17:15 UTC), with a 45-minute budget. Gaps are marked **not counted**.

**Clocks and time zones.** Seattle changed from PDT (UTC−7) to PST (UTC−8) at 02:00 local on
2026-11-01 (09:00 UTC). Times before then are PDT and times after are PST. Each timestamp below
names the clock it came from. Agent status files are not used as a clock: two of them carry
self-reported times that disagree with the system clock. `claude-zf2ff-status.md` was stamped
"17:05:00Z" when its mtime was 16:32 UTC, and `claude-evo-status.md` says "16:20 UTC / 09:20 PDT"
when that UTC time was 08:20 PST.

## 1. Snapshot

Observations were made at several times. Each row names its time and clock.

| Observation | Time | Clock |
|---|---|---|
| tmux sessions, agent processes, pane states | 2026-11-01 08:48 PST (16:48:15 UTC) | system clock (`datetime.now(UTC)` in `state.py`); process starts from `ps -o lstart` |
| Nebius job list | 2026-11-01 08:43 PST (16:43:46 UTC) | system clock; job times from the Nebius API (`created_at`, `finished_at`) |
| Git refs | 2026-11-01 ~08:55 PST (~16:55 UTC) after `git fetch` | git author dates (`%aI`) |
| Claude transcripts | scanned 2026-11-01 16:45–17:00 UTC | message `timestamp` fields (UTC) |

| Repository | Commit at observation | Default branch |
|---|---|---|
| kganjam/delphi-frontier | `53489c88a9272fc70edaa1cca5c421e6f16b3afe` (origin/main) | main |
| kganjam/delphi-evolve | `51a38057aebe7e7e0801d8f67af7fd4a81a8935f` (main, mirror clone) | main |

| | Count | Source | Label |
|---|---:|---|---|
| Agent identities, total (floor) | **at least 34 named identities**: 14 `ff-*` harnesses + 9 delphi-evolve roles + 4 Codex sessions + 7 native hosts with an action recorded in the window (claude-02 and claude-14 as ledger authors, claude-04 as handoff author in the audit, claude-05 as a message sender, claude-13 as a reviewer, claude-15 for the auth recovery, claude-17 as lead). These do not overlap by name. The floor exists because the identity audit names 5 more harness ids "named by others only" and 5 "probable", which are not counted here, and because roles that never had their own tmux session (for example `infra`, `site`, `cfd3d` in message filenames) are not counted. | tmux session names (`tmux ls`); `results/resources/agent-contributors.json` `counts` | measured (tmux) + quoted (audit) |
| ... `ff-*` harnesses (Frontier, 2026-11-01) | 14: agentuse, eco, evo, fseries, mol, neuro, organ, sitecritic, tissue, voxgpu, xeno, xenomodel, xenomorph, zf2ff | `tmux ls`; briefs in `delphi-evolve-rethink/harness-briefs/` | measured |
| ... delphi-evolve roles (`dx-*` + director) | 9 roles in 12 sessions: director, collab, corpus, critic (`-r1`), fable-lead, gpuops (+`-r1`), guilds, market (+`-r1`), submit (+`-retired-1`) | `tmux ls` | measured |
| ... Codex sessions | 4: `codex-01`, `codex-02`, `codex-03` (the Frontier "root/infra" coordinator in the messages), `codex-api` | `tmux ls`; message filenames `codex03-to-*` | measured |
| ... native hosts (`claude-01` … `claude-17`) | 17 tmux sessions. Only some worked on these repos: 7 have a recorded action in the window (listed in the row above). The identity audit independently supports **at least 3 native contributors**. claude-15 and claude-17 acted as leads (see Structure). By process cwd, `claude-01` was in `~/Orchestra`, `claude-02` in `~` and the rest in `~/git/morphoswarm`, so cwd does not show which repo each worked on. | `tmux ls`; `agent-contributors.json` `counts.native_contributors_supported_minimum = 3` | measured + quoted |
| ... nested children (in-session subagents) | **49 subagent transcripts** in files modified since 2026-10-30 (46 of them started on or after 2026-10-30 00:00 UTC). Not attributed to a project. | `subagents/` transcript paths, `conc.py`, `tokens.py` | measured |
| Top-level sessions (chats, runs) | **737 Claude top-level transcripts started on or after 2026-10-30 00:00 UTC**, across every project on this machine, not only these two repos. The steady ~6/hour baseline in quiet hours suggests scheduled sessions from other work. Codex: not counted (see §6). | `conc.py` over `~/.claude/projects` and `~/Orchestra/data/claude_creds/*/projects` | measured, not scoped to project |
| Subagents or child sessions launched by them | 49 transcripts (row above). tmux children launched by lead sessions: 14 `ff-*` by claude-17; 4 `dx-*` (corpus, market-r1, gpuops-r1, critic-r1) by claude-15. | `tmux new-session -d -s …` tool calls in transcripts `507442cb…` (claude-17) and `9fd16842…` (claude-15) | measured |
| Live processes at observation, by state | 47 tmux sessions; 43 have a live agent process and 4 have dead panes (`codex-api`, `delphi-rethink-director`, `dx-submit`, `dx-submit-retired-1`). The 43 live ones: **working 9 / idle 23 / auth-blocked 9 / error 2 / unknown 0**. By group: `ff-*` 9 working, 5 idle. `dx-*` 9 auth-blocked (`OAuth token revoked · Please run /login`). `codex-02` and `codex-03` error (usage limit, spend cap). `codex-01` idle. All 17 `claude-NN` idle. | `tmux capture-pane` of the last 10 non-blank lines, classified by `state.py` (heuristic: "esc to interrupt" means working). 45 agent processes were found under tmux and 51 system-wide; the 6 outside tmux are 2 Codex app-server daemons, 2 defunct Codex processes and an Oct-4 `claude doctor` with its parent shell. | measured (heuristic) |
| Max sessions active in any 180 s window | **16** distinct top-level transcripts in the window ending 2026-10-31 12:30:09 PDT (19:30:09 UTC). For comparison, the identity audit quotes 18 under its own definition. | `conc.py`: ≥1 assistant message in a trailing 180 s window, files with mtime ≥ 2026-10-30. Audit figure from `agent-contributors.json` `max_sessions_active_within_180s` | measured; 18 quoted |
| Remote compute jobs (Nebius AI jobs) | **at least 100 listed, of which 91 are ours by name prefix** (63 `claude-<harness>-`, 28 `delphi-evolve-ops-`). Ours: 68 completed, 9 failed, 2 cancelled, 1 error (QuotaExceeded), 9 running, 2 image-pulling. The other 9 are unattributed (`prebuilt-*`, `kiln-*`): 4 completed, 5 failed. The floor exists because the CLI returns only the newest 100 records (the oldest is 2026-10-31 14:26 PDT, 21:26 UTC), and both a `next_page_token` and `-f` file input were ignored. Earlier jobs are only in repo ledgers: `results/resources/agent-contributors.json` quotes `provider_jobs_own = 46` at its own time. | `nebius --profile hackathon ai job list --format json` | measured (floor) |
| Remote compute jobs (Google Cloud) | 1 CPU VM (`frontier-cpu-20261031-03`, 16 vCPU) per the shared rules. Job count **not counted**. | `_common.md` | quoted |
| Long-running background processes | Nebius token refresh into `~/.env` every 20 min, per the shared rules (process not inspected). A local `http.server` on port 8910 from another project (`sea-ad-mtg-codex-live`, 108 days, not ours). 2 Codex app-server daemons (since Oct 12 and Oct 29). | `ps -eo pid,etime,args` | measured (ps); quoted (refresh) |
| External agent identities | 1 MCP client name used against Delphi: `frontier-adapters` v0.2 (`frontier_adapters/delphi_mcp.py:87`). The Nebius Scientific AI MCP is also available. Forum accounts and bots: **not counted**. | `frontier_adapters/delphi_mcp.py` | measured |
| Commits by repository in the window | **delphi-frontier: 1,619** distinct commits reachable from `origin/*`, author dates 2026-10-31 07:49 PDT (14:49:44 UTC) to 2026-11-01 08:37 PST (16:37:50 UTC); 1,353 of them on origin/main; 160 remote branches. **delphi-evolve: 438** commits on all refs, 2026-10-30 23:58 PDT (2026-10-31 06:58:05 UTC) to 2026-10-31 13:52 PDT (20:52:35 UTC); 29 branches. | `git log --remotes=origin --date=iso-strict --format=%H\|%aI`; mirror clone of delphi-evolve | measured |
| Git identities and model trailers | Frontier authors: SciDEX Bot 1,591; "corpus session (Claude Sonnet 5.5)" 18; "nca" 7; Kris Ganjam 3. Model `Co-Authored-By` trailers: Sonnet 5.5 426, Opus 5 156, Opus 5.5 131, Opus 4.8 7. Evolve authors: SciDEX Bot 431, Kris Ganjam 7. Trailers: Sonnet 5.5 278 (plus 7 "SciDEX Bot"). | `git log --format=%an`, `%(trailers:key=Co-Authored-By,valueonly)` | measured |
| Tokens (Claude, all projects on this machine) | Since 2026-10-30 00:00 UTC, by message timestamp, deduplicated by `message.id`+`requestId`: **35,710 assistant messages; 8,935,881,007 cache-read; 41,193,752 output; 124,490,378 cache-creation; 74,312 fresh input**. All time: 296,455 messages; 68,309,003,437 cache-read; 226,038,734 output. By message count in the window: Sonnet 5.5 16,040; Opus 5.5 9,803; Opus 5 4,877; Haiku 5.5 4,374; Opus 4.8 291; Fable 5.1 8. Not scoped to these two repos. | `tokens.py` over 18,199 transcript files | measured |
| Tokens (Codex/GPT) | **not counted**. 6,778 files are under `~/.codex/sessions` (370 modified since 2026-10-30). A max-per-file scan of `total_token_usage` did not finish within the budget. | `find ~/.codex/sessions -name '*.jsonl'` | measured (file count only) |
| Spend | **unknown (not $0).** Nebius H100/L40S job hours and GCP are billed to sponsor credits and were not read. Claude and Codex usage is on subscription or API accounts not read here. `codex-02` and `codex-03` reached a usage limit and a spend cap, so spend was not zero. | pane text of `codex-02` and `codex-03` | measured (existence of limits) |

**A token discrepancy worth recording.** A lead-session tally passed to this harness (not
re-used, only compared) gave about 49.6 billion cache-read tokens and 160,546 messages since
2026-10-30. Re-measured here with deduplication, the figures are 8.94 billion and 35,710. The
likely reasons are that one message is logged once per content block with the same `usage`, that
resumed sessions copy earlier messages into a new file, and that the lead's window was set by file
mtime rather than message time. This record uses the deduplicated figure. The undeduplicated
method gives the larger one.

## 2. Timeline

- **First agent activity in the window:** first delphi-evolve commit at 2026-10-30 23:58 PDT
  (2026-10-31 06:58:05 UTC; git author date). The earliest message file in
  `delphi-evolve-rethink/messages/` is `primary-to-director.md` at 2026-10-31 06:00 PDT
  (13:00 UTC; mtime). Sessions in these two repos existed before then: `claude-01` … `claude-11`
  were created between 2026-10-20 and 2026-10-28 (tmux `session_created`), but their work on these
  repos before 2026-10-31 is **not counted**.
- **Last agent activity:** ongoing at observation. The latest commit on any `origin/*` ref was at
  2026-11-01 08:37 PST (16:37:50 UTC; author date), and 9 sessions were working at 16:48 UTC.
- The hourly table uses **git author dates** (`git log --date=iso-strict`, `%aI`) converted to
  UTC. `sessions_started` = Claude top-level transcripts whose first timestamp falls in the hour,
  across all projects; Codex is not counted, so `sessions_started` is `nc`. The two job columns
  cover only our 91 listed Nebius jobs; `nc` before 21:00 UTC on Oct 31, where the list ends.

| hour (UTC) | commits frontier | commits evolve | Claude sessions started | Nebius jobs submitted | Nebius jobs finished |
|---|---:|---:|---:|---:|---:|
| 2026-10-31 06 | 0 | 2 | 10 | nc | nc |
| 07 | 0 | 84 | 19 | nc | nc |
| 08 | 0 | 62 | 10 | nc | nc |
| 09 | 0 | 16 | 6 | nc | nc |
| 10 | 0 | 0 | 6 | nc | nc |
| 11 | 0 | 0 | 6 | nc | nc |
| 12 | 0 | 2 | 11 | nc | nc |
| 13 | 0 | 78 | 15 | nc | nc |
| 14 | 2 | 91 | 6 | nc | nc |
| 15 | 0 | 40 | 7 | nc | nc |
| 16 | 6 | 27 | 7 | nc | nc |
| 17 | 17 | 6 | 6 | nc | nc |
| 18 | 70 | 13 | 11 | nc | nc |
| 19 | 133 | 8 | 6 | nc | nc |
| 20 | 119 | 9 | 8 | nc | nc |
| 21 | 89 | 0 | 6 | 6 | 4 |
| 22 | 176 | 0 | 6 | 10 | 9 |
| 23 | 140 | 0 | 6 | 0 | 3 |
| 2026-11-01 00 | 143 | 0 | 6 | 2 | 2 |
| 01 | 99 | 0 | 6 | 1 | 1 |
| 02 | 94 | 0 | 6 | 3 | 2 |
| 03 | 88 | 0 | 6 | 3 | 1 |
| 04 | 67 | 0 | 6 | 0 | 2 |
| 05 | 71 | 0 | 6 | 0 | 0 |
| 06 | 112 | 0 | 6 | 1 | 1 |
| 07 | 77 | 0 | 6 | 1 | 1 |
| 08 | 2 | 0 | 6 | 0 | 0 |
| 09 | 0 | 0 | 6 | 0 | 0 |
| 10 | 0 | 0 | 6 | 0 | 0 |
| 11 | 0 | 0 | 6 | 0 | 0 |
| 12 | 0 | 0 | 6 | 0 | 0 |
| 13 | 6 | 0 | 7 | 1 | 1 |
| 14 | 16 | 0 | 14 | 5 | 2 |
| 15 | 40 | 0 | 9 | 22 | 17 |
| 16 (to 16:48) | 52 | 0 | 9 | 36 | 31 |

**Quiet stretches** (no commit in either repo for over an hour; author dates):

1. **2026-10-31 02:28–05:56 PDT (09:28–12:56 UTC), 3.5 h.** Delphi-evolve was quiet and Frontier
   had not started. Claude sessions kept starting at 6/hour (all projects). What ran on these repos
   is **not counted**.
2. **2026-11-01 01:01 PDT – 05:17 PST (08:01–13:17 UTC), 5.3 h.** No listed Nebius job was running
   (no job's `started_at`–`finished_at` overlaps the gap). The `dx-*` sessions were already
   auth-blocked. The delphi-rethink-director pane died at 2026-11-01 05:07 PST (13:07 UTC; tmux
   dead-pane status). The lead session claude-17 was created at 05:08 PST (13:08 UTC), and the
   `ff-*` harnesses started at 06:11 PST (14:11 UTC). In the shared rules' words, the predecessor
   workers had "stopped only to move billing".

Two stretches were quiet for one repo but not both: Frontier from 07:52 to 09:27 PDT (14:52–16:27
UTC) on Oct 31, while delphi-evolve was committing; and delphi-evolve after 13:52 PDT (20:52 UTC)
on Oct 31, which was its last commit.

## 3. Swarm dynamics

### Structure (who spawned whom)

Up times are tmux `session_created` and process start (`ps lstart`). Down times are tmux
dead-pane times. "Spawned by" comes from `tmux new-session` tool calls found in the parent's
transcript, except where an entry says otherwise.

- **claude-15** (native host; up 2026-10-31 05:51 PDT, 12:51 UTC; still alive, idle) took over
  Codex's role when `codex-02` reached its usage limit (`messages/host-takeover-from-codex.md`).
  It spawned `delphi-rethink-electric` at 07:37 PDT (14:37 UTC, now gone), `dx-corpus` at 08:02 PDT
  (15:02 UTC), `dx-market-r1` at 11:14 PDT (18:14 UTC), `dx-gpuops-r1` at 11:15 PDT (18:15 UTC) and
  `dx-critic-r1` at 11:32 PDT (18:32 UTC). Source: transcript `9fd16842…jsonl`.
- **delphi-rethink-director** was up 2026-10-31 05:57 PDT (12:57 UTC) and its pane died at
  2026-11-01 05:07 PST (13:07 UTC, status 143). `dx-collab`, `dx-gpuops` and
  `dx-submit-retired-1` came up at 06:05 PDT (13:05 UTC), `dx-fable-lead` at 06:16, `dx-guilds` and
  `dx-market` at 06:21 PDT (13:21 UTC), and `dx-submit` at 07:13 PDT (14:13 UTC). That these were
  **spawned by the director** is **estimated**: the inference rests on creation order and the
  `director-to-*` messages, not on its transcript. `dx-submit-retired-1` went down at 2026-10-31
  07:15 PDT (14:15 UTC, status 0). `dx-submit` went down at 2026-10-31 19:13 PDT (2026-11-01 02:13 UTC, status 143). tmux prints dead-pane times in the host's local zone, America/Los_Angeles.
- **codex-03** (up 2026-10-31 10:48 PDT, 17:48 UTC) was the Frontier coordinator. It is the
  addressee of most `*-to-codex03.md` messages, and the "root"/"infra" sender of
  `infra-to-*`/`root-*` messages. It hit its spend cap (pane text at observation). **codex-api**
  was up 06:50 PDT (13:50 UTC) and its pane died at 2026-10-31 18:50 PDT (2026-11-01 01:50 UTC,
  signal 15).
- **claude-17** (native host; up 2026-11-01 05:08 PST, 13:08 UTC; session `507442cb`) is the lead
  for 2026-11-01. It spawned `ff-evo`, `ff-mol`, `ff-organ`, `ff-tissue` and `ff-zf2ff` at
  06:11 PST (14:11 UTC); `ff-eco` and `ff-neuro` at 06:18; `ff-voxgpu`, `ff-xeno` and
  `ff-xenomodel` at 07:57; `ff-sitecritic` at 08:04 (16:04 UTC); `ff-xenomorph` at 08:12; and
  `ff-agentuse` and `ff-fseries` at 08:37 PST (16:37 UTC). The ff- names come from a loop in its
  `tmux new-session -d -s ff-…` calls. All 14 were still alive at 16:48 UTC.
- Older native hosts `claude-01` … `claude-14` were created between 2026-10-20 and 2026-10-31
  (tmux). Who spawned them is **not counted** (they predate the window).

### Assignment

- **Harness briefs:** `/data/artifacts/delphi-evolve-rethink/harness-briefs/<name>.md` plus
  `_common.md` (19 files, mtimes 2026-11-01 06:11–08:36 PST). Each `ff-*` session was launched
  with a pointer to its brief. The briefs are outside the repo and are quoted only.
- **Message files** `/data/artifacts/delphi-evolve-rethink/messages/<from>-to-<to>.md`: 597
  files, mtimes from 2026-10-31 06:00 PDT (13:00 UTC) on. They carried work orders
  (`director-to-*`, `codex03-to-*`, `infra-to-*`), returns (`*-to-codex03`, `*-to-root`) and
  per-harness status files (`claude-<harness>-status.md`).
- **GitHub issues:** kganjam/delphi-frontier #1–#6 (the F-series) and #8 (this one).
  Source: `claude-fseries-status.md`, `gh issue view 8`.
- **Branches:** one per harness. Commits ahead of origin/main at observation:
  `claude/evo2-fin-scale-20261101` 45, `claude/bioservices-20261101` 28, `claude/neuro-20261101` 24,
  `claude/zf2ff-20261101` 22, `claude-organ/sims` 18, `claude-tissue/sims-20261101` 16,
  `claude/mol-sims-20261101` 13, `claude/eco-20261101` 11, `claude/voxgpu-20261101` 9,
  `claude/xenomodel-20261101` 8, `claude/xenomorph-20261101` 7, `claude/about-blog-20261101` 7,
  `claude/xeno-20261101` 6. Source: `git rev-list --count origin/main..<branch>`.

### Waiting / blocked

| Start | End | What blocked | What unblocked it | Source |
|---|---|---|---|---|
| ≤2026-10-31 06:40 PDT (13:40 UTC) | for this request, never | Nebius CPU job creation at 16–128 vCPU was refused with `ResourceExhausted … compute.instance.non-gpu.vcpu (limit 24, …)`. The limit is tenant-wide and 20 vCPU were already in use. | A 4-vCPU job was accepted instead. | `messages/gpuops-to-director-primary-01.md` (written 06:41 PDT) |
| 2026-11-01, before 16:20 UTC | "Resolved — CPU quota later freed" (time not recorded) | claude-evo's CPU motif scan was refused `ResourceExhausted` on a dry run: limit 24 against an aggregate 28 (also requested 32 and 26). | It ran locally under `systemd-run`, then was submitted once quota freed. Nothing of others' was cancelled. | `messages/claude-evo-status.md` lines 82, 98–102 |
| 2026-11-01 (job `claude-zf2ff-motif-scan-1`) | terminal | The Nebius job went to `ERROR` / `QuotaExceeded` (`compute.instance.non-gpu.vcpu`) at provisioning. | Not resubmitted under that id. Kept as a failure. | Nebius job list; `claude-zf2ff-status.md` |
| `dx-market`/`dx-gpuops` processes, which started 06:05–06:21 PDT (13:05–13:21 UTC) | 2026-10-31 11:18 PDT (18:18:56 UTC) for the work, via `-r1` successors | `OAuth token revoked · Please run /login`. The credential was fixed in the process environment at start, so a refresh could not reach it. | claude-15 relaunched the same conversations through managed allocation as `dx-market-r1` and `dx-gpuops-r1`. No `/login` was run and no secret was handled. | `messages/claude15-auth-recovery.md` |
| `dx-*` (9 sessions) | **still blocked at 2026-11-01 16:48 UTC** | All 9 live `dx-*` panes, including the `-r1` successors, show `OAuth token revoked`. | Not unblocked. | `tmux capture-pane` at observation |
| delphi-rethink-electric, ~07:18 PDT (14:18 UTC) Oct 31 | not recorded | OAuth token revoked, with uncommitted files in its worktree | Director asked primary/host to recover it | `messages/director-needs-electric-recovery.md` |
| `codex-02`, 2026-10-31 (before 09:31 PDT, 16:31 UTC) | not before "Nov 6th" per the provider | "You've hit your usage limit" | claude-15 took over the role | `messages/host-takeover-from-codex.md`; pane text at observation |
| `codex-03`, on or before 2026-11-01 16:48 UTC | not unblocked at observation | "You hit your spend cap set by the owner of your workspace", stopped at a "Request increase?" prompt (answer: No) | Not unblocked. The director had already ruled that items Codex had not re-reviewed are labelled "single-reader, not independently reviewed". | pane text; `messages/director-to-dx-submit.md` line 38 |
| 2026-11-01 ~00:55 UTC (Oct 31 17:55 PDT) | approval recorded in the same file | A paid GPU (Google L4) calibration waited for root approval | "Root now APPROVES one Google L4 calibration, then R2 only if frozen time/memory gates fit" | `messages/infra-to-cfd-gcp-l4.md` |
| Model-switch prompt | not located | The brief lists an agent stopped at an interactive model-switch prompt. I did not find its record within the budget. **not counted** | — | — |

### Review changed a decision

All commits in both repos carry one git identity: **SciDEX Bot** (1,591 of 1,619 Frontier
commits; 431 of 438 evolve commits). So in every case below, **reviewer and author shared a git
identity**. Shared model is stated where the record gives it.

| Case | Before → after | Reviewer vs author | Where recorded |
|---|---|---|---|
| DOE decision exercise (`doe-centered-margin`) | misclassification 0.50 (no measurement) / 0.13 / 0.10 → 0.043 / 0.028 / 0.023; the "measurement halves error" claim was retracted | root session reviewing claude-14's work. Same fleet; models not recorded in the ledger | `results/coordination/review-corrections.json`; fix `4d9628f` |
| Genotype compiler typed inputs | 17 of 19 scoped checks → 29 of 29 declared conditions. These are different check sets, so this is not a before/after rate. `endpoint="false"` coerced truthy; a non-digest was accepted. | separate review harness vs claude-02 (owner) | same file; fix `1a084328` |
| Compiler cache and pins | stale-cache false passes → typed blocked results | native mechanobio review, then root, vs claude-14 | same file; `f2f0c69`, `68117a9`, `189c0e5` |
| Contributor count | headline 4 → floor of 11; "31 verified active" → "31 live processes", unlabelled | root vs claude-14 | same file; `474fb8e` |
| DOE mutant control | a control that could not fail → the mutant changes 86 of 192 flags | no reviewer: the run refused (author self-correction) | same file; `895487f` |
| Voxelyze agreement | "~2.74%" coarse/fine agreement → 2.7322% on normalized values, but raw SI displacement differs by **15.5739%**. The agreement claim was withdrawn. | an "independent bounded" review (`130b3f4b`, no model trailer) vs the original output owner (`e6f10331`). Shared git identity; model not recorded | `docs/audits/voxelyze-review-2026-10-31.md` lines 27–30 |

### Duplicated or abandoned work

- **Announced to avoid duplication, 2026-11-01 ~08:20 PST (16:20 UTC):** claude-xeno told
  claude-voxgpu that its 464-run pattern sweep was already running on Nebius
  (`aijob-e00xmm28kekfg1czwv`) and would not be moved to the GPU engine. Source:
  `messages/claude-xeno-to-voxgpu.md`.
- **Do-not-duplicate order (file mtime 2026-11-01 02:20 UTC):** "Native mechanobio is preparing the
  v3a FEM/VLM static aeroelastic bridge; do NOT duplicate this". Source:
  `messages/infra-to-cfd-h100-and-next.md`. Eight `infra-*`/`codex03-*` messages carry similar
  language (grep `duplicat`).
- **Approval with an explicit "no duplicate full assay"**: `messages/infra-to-cfd-gcp-l4.md`.
- **Predecessor and successor:** `dx-submit-retired-1` was replaced by `dx-submit`, and
  `dx-market` and `dx-gpuops` by their `-r1` sessions (tmux). On 2026-11-01 the `ff-*` harnesses
  resumed tasks that predecessor workers had started before being "stopped only to move billing"
  (`_common.md`). claude-evo records that its predecessor left no status file and that it cites
  the predecessor's commits and job ids instead (`claude-evo-status.md`).
- **Abandoned:** the DOE v1 outputs were overwritten before commit and are irrecoverable. Only a
  labelled regeneration exists (`review-corrections.json`, entry `doe-centered-margin`, `limits`).

### Failures kept

- **Nebius, listed window:** 9 failed, 2 cancelled and 1 error among our 91 listed jobs. Failed:
  `delphi-evolve-ops-infra14-collagen-md`, `-infra16-morpheus-full-horizon`,
  `-infra18-cfd3d-controlled-fish`, `-infra19-rd-ddpm-training`,
  `-infra23-rd-ddpm-precision-diagnostic`, `-infra29-h100-cfd-controls-calibration`,
  `-infra36-voxcraft-modern-cuda-probe`, `claude-organ-r6-trim-map`, `claude-organ-r4b-torsion`.
  Each record is still on the provider with `ContainerFailed`. Error: `claude-zf2ff-motif-scan-1`
  `QuotaExceeded`. Cancelled: 1 `claude-neuro-*` and 1 `delphi-evolve-ops-*`. The brief's
  figure of 23 failed and 6 cancelled covers a longer window that this CLI can no longer list,
  so it is **not re-measured**.
- **Voxcraft GPU probe `COMPILE_FAIL`:** `artifacts/voxcraft-gpu-probe/probe.json` (commit
  `a896380b`, 2026-10-31 23:26 PDT, 2026-11-01 06:26 UTC).
- **KCNE1 binding ΔΔG stopped at its preregistered floor:** coverage 20.27% against a 75% floor,
  and the negative control D76N is absent. No ΔΔG was computed.
  `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` (commit `3272d3e4`, 2026-10-31 11:08 PDT,
  18:08 UTC); preregistration `dcdc5f4d`.
- **Fish v3b VLM, not converged:** `artifacts/cfd3d/vlm/fish3d-v3b-glide-pose/vlm.json`
  `"status": "NOT CONVERGED: do not use the lift or the per-quad dCp"` (commit `b98f32b6`,
  2026-10-31 16:31 PDT, 23:31 UTC).

### Communication channels actually used

| Channel | What it carried | Count | Source |
|---|---|---:|---|
| Message files in `delphi-evolve-rethink/messages/` | work orders, returns, reviews, status | 597 files | `ls \| wc -l` |
| Harness briefs | goal and rules per `ff-*` harness | 19 files | `ls harness-briefs/` |
| Git branches and commits | results with receipts | 160 + 29 remote branches; 1,619 + 438 commits | `git` |
| GitHub issues | F-series tasks (#1–#6), this record (#8) | at least 7 | `gh issue view` |
| tmux | session launch (`new-session`), and before a rule change, `send-keys` injection | 47 sessions | `tmux ls`. A pane records the rule "NEVER tmux send-keys into codex-03 or into the user's pane" after an injection interrupted the user. |
| MCP | Delphi MCP (client `frontier-adapters`; 9 tool names used, listed in `frontier_adapters/examples/delphi_live/inventory.json` `tools_used_here`); Nebius Scientific AI MCP (available; call count **not counted**) | — | repo files |

## 4. What the agents did, by use case

Provider state (did the job run) and scientific-predicate state (does the result support the
claim) are kept apart.

| Use case | Agents (count and kind) | What it accomplished (numbers with sources) | Status | Sessions or commits it came from |
|---|---|---|---|---|
| Claim import and adaptation from Delphi | adapter authors (Frontier). Count **not counted** | Adapters `frontier_adapters/delphi_{claim,mcp,bulk,curate,live}.py`. 44 distinct `claim-…` ids appear in `frontier_adapters`, `results` and `docs` (`git grep -o`). | code merged on main | first added at `7f485f9d` (2026-10-31 11:46 PDT) |
| Delphi claim reuse in delphi-evolve | evolve sessions | 6 files in `artifacts/claim_reuse/delphi_records/`, including `.trig` nanopub records. 24 distinct `w3id.org` IRIs in the repo. | on main | first added at `18bcd7d` (2026-10-31 00:59 PDT) |
| Problems and bridges | not counted | not counted | — | — |
| Flying-fish design mission | `ff-*` harnesses (organ, neuro, tissue, eco, evo, zf2ff, mol) plus earlier native hosts | per-branch commits above; Nebius jobs by prefix: organ 9, neuro 11, tissue 10, zf2ff 12, evo 8, mol 4 (listed window) | in progress on branches, not merged | `claude/*-20261101` branches |
| Evo 2 | ff-evo | 8 `claude-evo-*` jobs, all COMPLETED (provider). The predicate state is in `claude-evo-status.md`, quoted not re-checked. | provider: completed; predicate: see status file | `claude/evo2-fin-scale-20261101` (45 commits ahead) |
| OpenFold2 / ESM2 | not counted separately | the 15-record model/simulator ledger `results/resources/bio-model-usage.json` (quoted) | — | — |
| OpenMM / molecular | ff-mol, `delphi-evolve-ops-infra14-collagen-md` | 4 `claude-mol-*` jobs (3 completed, 1 running); infra14 FAILED | provider mixed; predicate not counted | `claude/mol-sims-20261101` |
| BETSE / Morpheus | ff-xenomorph (Morpheus 2.3.9); `infra16-morpheus-full-horizon` | 1 `claude-xenomorph-*` running; infra16 FAILED | provider: running / failed | `claude/xenomorph-20261101` |
| Neural CA | earlier sessions (`nca`, 7 commits by author "nca") | `results/resources/nca-*.json` (quoted) | not re-checked | — |
| Voxel / xenobot simulation | ff-voxgpu, ff-xeno, ff-xenomodel | voxgpu 6 jobs (4 completed, 2 running); xeno 2 running; Voxelyze review withdrew an agreement claim | provider mixed | branches above |
| Genotype compiler | claude-02 (owner), claude-14, a review harness | 3 review corrections recorded | fixed and rechecked (author-run tests) | `review-corrections.json` |
| Live node and MCP server | not counted | not counted | — | — |
| Review and audit | root, review harnesses, ff-sitecritic | 6 decision changes (table above); `docs/audits/` holds 10 audit files | recorded | `review-corrections.json`, `docs/audits/` |
| Enzyme planner and replay (delphi-evolve) | 9 `dx-*` roles | 438 commits, 2026-10-31 06:58–20:52 UTC; 28 `delphi-evolve-ops-*` Nebius jobs (20 completed, 7 failed, 1 cancelled) | stopped: all `dx-*` sessions auth-blocked at observation | delphi-evolve main `51a38057` |
| Lean certificates | not counted | not counted | — | — |
| Nanopubs | evolve claim-reuse | `.trig` records in `artifacts/claim_reuse/delphi_records/`; publication state (unsigned draft or published, and to which registry) **not counted** | — | `18bcd7d` |
| Site and infrastructure | codex-03, claude-02, ff-sitecritic, about-blog | not counted | — | — |
| This record | ff-agentuse (1 Opus 5.5 session) | this file | written | `claude/agentuse-20261101` |

## 5. Touchpoints with the Delphi repository

- **First read of Delphi claims:** the adapters `delphi_claim.py` and `delphi_mcp.py` were added
  in Frontier commit `7f485f9d` (author date 2026-10-31 11:46 PDT, 18:46 UTC). `delphi_bulk.py`
  and `delphi_curate.py` came in `0e3222cd` (11:52 PDT), and `delphi_live.py` with its inventory in
  `b5414a49` (13:43 PDT, 20:43 UTC). The inventory records `retrieved_at` 2026-10-31 13:34 PDT
  (20:34:13 UTC). In delphi-evolve, Delphi records first appear in `18bcd7d` (2026-10-31 00:59 PDT,
  07:59 UTC) under `artifacts/claim_reuse/delphi_records/`. The number of Delphi versions read is
  **not counted**.
- **MCP calls to the Delphi MCP:** client name `frontier-adapters` v0.2. Tool names used: the 9 in
  `inventory.json` `tools_used_here`. The endpoint hostname is omitted here per rule 6. Per-call
  time windows are **not counted**, because no call log was found in the repo within the budget.
- **Our files citing Delphi claim ids or nanopub IRIs:** 44 distinct `claim-…` ids in Frontier;
  24 distinct `w3id.org` IRIs in delphi-evolve. Delphi's own tallies inside `inventory.json` were
  deliberately not read into this record.
- **Anything of Delphi's that depends on a result of ours:** **none found** on our side. I did not
  inspect Delphi's repository (rule 7).

## 6. What this record does not establish

- **Not counted:**
  - Codex token usage (the scan did not finish).
  - Nebius jobs older than the newest 100 (a CLI paging limit).
  - Google Cloud job counts.
  - Spend.
  - Work on these repos before 2026-10-31 by the older native hosts.
  - Who spawned `claude-01` … `claude-14`.
  - The director's own spawn calls (estimated from timing).
  - Delphi MCP call windows.
  - Nanopub publication state.
  - The model-switch-prompt block.
  - Several use-case rows.
- **Not scoped to project:** the session counts, the 180 s concurrency figure and the token totals
  cover every Claude transcript on this machine, not only work on these two repos.
- **Point-in-time only:** the process states (16:48 UTC), the tmux list, and the Nebius list
  (16:43 UTC). States change minute to minute. The state classifier is a text heuristic on the last
  10 pane lines, and at least one host showed a busy spinner in a separate capture that the
  classifier marked idle.
- **Collective versus single agent:** **not shown.** No single-agent counterfactual was run. The
  review-corrections ledger itself says it cannot tell whether one agent re-reading its own work
  would have found the same issues. All reviewers share the author's git identity and fleet.
- **Not independent:** this record was written by one session of the same fleet it describes.

## Commands run

The same list is in `agent-use-summary.json` → `commands_run`. The Python scripts are committed in
[`scripts/`](scripts/). Each takes its output directory as an argument. `procs.py` and `state.py`
read and write `procs.json` in that directory, and `hourly.py` takes the delphi-evolve clone path
first. Run them from the repository root.

1. `git fetch origin; git rev-parse origin/main`
2. `git clone --mirror https://github.com/kganjam/delphi-evolve <scratch>/evolve.git; git -C evolve.git rev-parse HEAD`
3. `git log --remotes=origin --format=%H | sort -u | wc -l   # 1619`
4. `git log origin/main --format=%H | wc -l   # 1353`
5. `git -C evolve.git log --all --format=%H | sort -u | wc -l   # 438`
6. `git branch -r | wc -l; git -C evolve.git branch | wc -l`
7. `git log --remotes=origin --format='%(trailers:key=Co-Authored-By,valueonly)' | sed 's/ <.*//' | sort | uniq -c`
8. `git log --remotes=origin --format=%an | sort | uniq -c`
9. `python3 hourly.py: git log --remotes=origin (frontier) and --all (evolve) --date=iso-strict --format=%H|%aI, dedupe by hash, bucket by UTC hour, gaps > 1 h`
10. `gh repo view kganjam/delphi-frontier --json createdAt,defaultBranchRef; same for delphi-evolve`
11. `tmux ls -F '#{session_name}|#{session_created}|#{session_activity}'`
12. `tmux list-panes -a -F '#{session_name}|#{pane_pid}|#{pane_current_command}|#{pane_dead}'`
13. `python3 procs.py: ps -eo pid,ppid,lstart,comm,args; descendants of each pane pid whose comm/args is claude or codex; readlink /proc/<pid>/cwd`
14. `python3 state.py: tmux capture-pane -p -S -15; last 10 non-blank lines; 'esc to interrupt' or spinner -> working, 'OAuth token revoked'/'/login' -> auth-blocked, usage limit/spend cap -> error, prompt -> idle, dead pane -> no process`
15. `nebius --profile hackathon ai job list --format json   # 100 items + next_page_token; --page-size/--page-token unsupported; -f request file ignored page_token`
16. `nebius --profile hackathon ai list --page-size 1000   # still 100`
17. `python3 tokens.py: stream every *.jsonl under ~/.claude/projects and ~/Orchestra/data/claude_creds/*/projects; assistant messages with usage; dedupe (message.id, requestId); window by message timestamp >= 2026-10-30T00:00Z`
18. `python3 conc.py: files with mtime >= 2026-10-30; per top-level file (not under subagents/) the set of assistant-message seconds; sliding 180 s window max distinct files; first timestamp per file bucketed by hour`
19. `python3 codex.py: per ~/.codex/sessions file, max cumulative total_token_usage; window = max minus last value before 2026-10-30`
20. `find ~/.codex/sessions -name "*.jsonl" | wc -l   # 6778`
21. `grep -l -i -E "<pattern>" /data/artifacts/delphi-evolve-rethink/messages/*   # ResourceExhausted, revoked, spend cap|usage limit, duplicat, COMPILE_FAIL, KCNE1, v3b`
22. `ls /data/artifacts/delphi-evolve-rethink/messages | wc -l   # 597`
23. `python3 -c json.load(results/coordination/review-corrections.json) entries`
24. `grep -n "2.74|15.57" docs/audits/voxelyze-review-2026-10-31.md`
25. `git log --remotes=origin --diff-filter=A --format="%h %aI" -- frontier_adapters/delphi_*.py`
26. `git grep -h -o -E 'claim-[a-z0-9]+(-[a-z0-9]+)+' -- frontier_adapters results docs | sort -u | wc -l   # 44`
27. `git -C evolve.git grep -h -o -E 'https?://w3id\.org/[a-z]+/[A-Za-z0-9_-]+' HEAD | sort -u | wc -l   # 24`
28. `for b in origin/claude*: git rev-list --count origin/main..$b`
29. `grep tmux new-session -d -s in transcripts 507442cb (claude-17) and 9fd16842 (claude-15)`
