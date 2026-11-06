#!/usr/bin/env python3
"""Recover the 134 replication blocks the harvester matched and never handled.

The dispatch had three branches -- result, entail, challenge -- and the regex matched four kinds.
Every `swarm-replication` block was parsed, counted as found, and dropped. 17 of them are
independent re-derivations that DISAGREED with the claim they checked.

Re-runnable: the insert is guarded on (claim, voter, kind).
"""
import json, sys
sys.path.insert(0, "/data/swarm")
from harvest import BASE, git, lit, q, BLOCK   # noqa: E402


def main():
    branches = [b.strip() for b in git("branch", "-r", "--sort=-committerdate").split("\n")
                if "origin/claude/" in b]
    seen = agree = dis = skipped = 0
    for b in branches:
        tag = f"harvest:{b.split('/')[-1]}"
        for f in [x for x in git("diff", "--name-only", f"{BASE}...{b}").split("\n")
                  if x.endswith(".md")][:3]:
            try:
                t = git("show", f"{b}:{f}")
            except Exception:
                continue
            for kind, body in BLOCK.findall(t):
                if kind != "replication":
                    continue
                seen += 1
                try:
                    d = json.loads(body)
                except json.JSONDecodeError:
                    skipped += 1; continue
                cid, agrees = d.get("claim_id"), d.get("agrees")
                if not str(cid).isdigit() or agrees is None:
                    skipped += 1; continue
                if not q(f"select 1 from claim where id={int(cid)}"):
                    skipped += 1; continue
                val = 1 if agrees is True else (-1 if agrees is False else 0)
                myv = str(d.get("my_value") or "")[:300]
                note = str(d.get("note") or "")[:900]
                reason = (f"independent re-derivation {'AGREES' if val > 0 else 'DISAGREES'}"
                          + (f"; their value: {myv}" if myv else "")
                          + (f". {note}" if note else ""))
                q(f"""insert into artifact_signal (entity_type, entity_id, kind, dimension,
                         voter_id, voter_kind, value, weight, unit, reason, metadata)
                      select 'claim', {lit(str(cid))}, 'replication', 'reproducibility',
                             {lit(tag)}, 'agent', {val}, 1, 'verdict', {lit(reason[:1400])},
                             {lit(json.dumps({'my_value': myv, 'agrees': agrees}))}
                      where not exists (select 1 from artifact_signal s
                                        where s.entity_type='claim' and s.entity_id={lit(str(cid))}
                                        and s.voter_id={lit(tag)} and s.kind='replication')""")
                if val > 0:
                    agree += 1
                elif val < 0:
                    dis += 1
    print(f"  replication blocks seen: {seen}  recorded: {agree + dis}  skipped: {skipped}")
    print(f"    agreeing: {agree}")
    print(f"    DISAGREEING: {dis}  <- independent re-derivations that did not reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
