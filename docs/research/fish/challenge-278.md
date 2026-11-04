# Challenge 278: can you recover an operation whose ID was never captured?

**Verdict: WEAKENED.** The narrow interface facts may well be true, but I could not check them. The universal claim ("NO client-side recovery exists") and the evidence label ("measured") both go beyond what a `tools/list` inspection can show.

## The claim as recorded (the author's words, not mine)

> NO CLIENT-SIDE RECOVERY EXISTS for an operation whose ID was not captured. The workbench exposes
> get_operation, cancel_operation and acknowledge_operation, ALL of which require an operation_id, and
> there is NO list tool. acknowledge_operation purges a TERMINAL operation's payload and is destructive,
> not a slot release.

Evidence level recorded: `measured`. Source: "workbench tools/list, 4 operation tools inspected".

## What I tried, and how much I could read

| Source | Read-level | Result |
|---|---|---|
| Workbench `tools/list` | **could-not-access** | No workbench MCP server is connected to this session. I searched for one with ToolSearch ("operation workbench") and found none. |
| This repo, working tree | full-text (grep) | No file mentions `workbench`, `operation_id`, `get_operation`, `cancel_operation`, `acknowledge_operation` or `list_operations`. |
| This repo, all history (`git log --all -S acknowledge_operation`, 30 commits) | full-text (pickaxe) | No hits. |

**Scope of my negative search:** this repository (working tree and all reachable history) and the deferred-tool registry of this session. I did not reach the workbench itself. So I **cannot confirm or refute** these interface facts: the three tools exist, each needs an `operation_id`, and no list tool exists. Those parts are still `unknown` to me. They are not refuted.

## Attack 1: the scope of the negative is wider than the evidence (main finding)

The evidence is one `tools/list` response. From it, the author concludes that *no client-side recovery exists*. That step needs some hidden assumptions, and **these are my inferences, not observations**:

1. **`tools/list` lists tools and nothing else.** An MCP server can also expose `resources/list`, resource templates and prompts. The evidence does not show those surfaces were checked. A resource such as `operations://…` would be a recovery path that `tools/list` cannot show.
2. **Only the four "operation" tools were inspected.** The claim needs every *other* tool to be unable to give back the ID. For example:
   - the submit tool might be idempotent on a client key and return the existing operation;
   - a "slot busy" or quota error might name the operation that holds the slot;
   - a status or health tool might list active work.

   None of this is excluded by inspecting four tools.
3. **"Not captured" is treated as "absent on the client side".** If the submit call returns the ID in its result, then the client *did* receive it. It is in the host's transcript or tool-result log, even if the agent never stored it in a variable. Reading that log is client-side recovery. The claim holds only if the ID never reached the client, for example if submission is fire-and-forget or the ID only comes in a notification that was dropped. The claim does not say which.

Relax any one of these assumptions and "NO recovery exists" turns into "no recovery through the four inspected tools". That narrower statement is the one the evidence actually supports.

## Attack 2: is the evidence level honest?

`tools/list` returns **declared** schemas and description strings. It does not show what the server does. Two parts of the claim are about behaviour:

- "acknowledge_operation **purges** a terminal operation's payload and is **destructive**";
- it is "**not a slot release**".

If these came from reading the description text, they are *documented* behaviour, at listing level. They are not *measured*. To measure them you would have to call `acknowledge_operation` on a terminal operation and then observe two things: whether `get_operation` still returns the payload, and whether a slot-limited submit now succeeds. The recorded source mentions no such call.

Also, "destructive" and "slot release" do not exclude each other. Purging a terminal record could free a slot. Telling them apart needs exactly that behavioural test. **Correction (my inference):** these sub-claims should be labelled `documented (tool description, listing-level)`, not `measured`.

## Attack 3: an internal inconsistency

The source says "**4** operation tools inspected", but the claim names **3** (get, cancel, acknowledge) and says there is no list tool. The fourth tool is unnamed. If it is the submit tool, its return schema matters directly for Attack 1.3, and it should be cited. As recorded, the reader cannot check this.

## Arithmetic

There is none to redo. The claim has no numbers; `value: n/a`.

## What survives

- *Conditional on the inspection being accurate*: the three named tools are keyed by `operation_id`, and `tools/list` contains no enumeration tool. I could not verify this. It is not refuted.

## What does not survive as stated

- "NO CLIENT-SIDE RECOVERY EXISTS". This is a universal negative, but the evidence covers four tools in one listing. It does not cover resources, the other tools' outputs or error payloads, or the client's own transcript.
- The `measured` label on the acknowledge semantics. These come from interface text, not from an observation.

**Suggested restatement:** "Among the workbench's four operation tools (`tools/list`, listing-level), none enumerates operations; get/cancel/acknowledge each require an `operation_id`. Per its description (not tested), acknowledge purges a terminal operation's payload. Resources, other tools' outputs, and the client transcript were not checked as recovery paths."

```swarm-challenge
{"claim_id": 278, "outcome": "weakened", "reason": "The interface facts are unverified but not refuted (workbench could-not-access); the universal 'no client-side recovery' overreaches a tools/list inspection that excludes resources, other tools' outputs/errors and the client's own transcript, and acknowledge's purge/not-slot-release semantics are documented, not measured.", "corrected_value": null, "depends_on": ["workbench tools/list as reported by the claim author (not independently accessed)", "MCP protocol: tools/list does not enumerate resources or prompts", "assumption that the submit tool returns operation_id to the client in its result (unverified)", "repo grep and git pickaxe over delphi-frontier finding no workbench references"]}
```
