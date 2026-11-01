"""Bounded, timestamped projection of the queue and resource receipts the System page already depends on. No new telemetry: this module only re-reads committed files.

    project(root, at=None, pins_rel=PINS) -> dict      the projection (schema frontier.system-operations/1)
    build(ins, out, root)                              publisher adapter: stages the projection as a static site file
    python -m frontier.system_operations --pin|--write  re-pin the sources / write the static file

Rules this module enforces, each with a test:
* Every source is read through system_status.read_small (repo-relative, no `..`, no dotfiles, size bound) and pinned by sha256 in deploy/system/operations-pins.json.
  A missing, unparseable or CHANGED file is `unavailable` and its contents are withheld. It is never read as zero jobs or zero utilization.
* A provider job state (COMPLETED, FAILED, ...) is never a scientific result. Planned stage, provider state and sampled utilization are three separate blocks.
* Spend is unknown unless a source carries a billed figure; no figure is estimated, summed or inferred from credits. No active-agent total is published.
* Shared jobs are split team-attributed / earlier-team / unattributed. "Unattributed" means no exact record, not "belongs to someone else". No cancellation authority is claimed.
* Recovery layers (file/source checkpoint, database cutoff, off-host recovery, older application drill) keep their own cutoffs and are never merged into one "restored".
* Never output: environment, tokens, credential material, hosts, storage URIs or local paths.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

from .system_status import ROOT, now_iso, read_small, sha256

SCHEMA = "frontier.system-operations/1"
PINS = "deploy/system/operations-pins.json"
SITE_PATH = "artifacts/system-operations/operations.json"
SOURCES = {                                               # id -> repo-relative path; the allowlist
    "queue": "results/infra/queue.json",
    "usage": "results/resources/hackathon-usage.json",
    "inventory": "results/resources/resource-inventory.json",
    "shared": "results/resources/shared-job-counts.json",
    "ledger": "results/resources/team-job-ownership.json",
    "runtime": "results/resources/terminal-runtime-receipts.json",
    "progress": "results/resources/current-job-progress.json",
    "recovery_base": "results/resources/backup-recovery-20261101.json",
    "recovery_service": "results/resources/backup-recovery-service-20261101.json",
    "recovery_stable": "results/resources/backup-recovery-stable-addons-20261101.json",
    "recovery_films": "results/resources/backup-recovery-four-film-20261101.json",
    "recovery_studies": "results/resources/backup-recovery-studies-20261101.json",
}
DOC = "docs/infra-queue.md"                                # a readable narrative record; linked, not parsed
REPO_BLOB = "https://github.com/kganjam/delphi-frontier/blob/main/"
FORBIDDEN = re.compile(r"s3://|sandbox-\d|\bsb0\d\b|/home/|/data/|BEGIN [A-Z ]*KEY|bearer [A-Za-z0-9]|delphi[- ]evolve", re.I)
HIST_AFTER_S = 3600                                         # a source observed this much before the queue is shown as a historical cutoff


def _c(v, n=240):
    return v[:n] if isinstance(v, str) else v


def _ts(s):
    from datetime import datetime
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None


# ------------------------------------------------------------------ pins and loading
def load_sources(root: Path, pins_rel: str = PINS) -> tuple[dict, list]:
    """Returns ({id: parsed|None}, [source rows]). Status is one of verified, changed, missing, unparseable, not-pinned, pins-invalid."""
    raw, why = read_small(root, pins_rel)
    pins, pins_status = {}, "ok"
    if raw is None:
        pins_status = "pins file " + why
    else:
        try:
            pins = {p["id"]: p for p in json.loads(raw)["pins"]}
        except (ValueError, KeyError, TypeError):
            pins_status = "pins-invalid"
    data, rows = {}, []
    for sid, rel in SOURCES.items():
        pin = pins.get(sid) or {}
        blob, why = read_small(root, rel)
        row = {"id": sid, "path": rel, "href": REPO_BLOB + rel, "pinned_sha256": pin.get("sha256"), "actual_sha256": sha256(blob) if blob is not None else None}
        parsed = None
        if blob is None:
            row["status"] = "missing" if why.startswith("not present") else "unreadable: " + why
        elif pins_status != "ok":
            row["status"] = pins_status
        elif not pin:
            row["status"] = "not-pinned"
        elif row["actual_sha256"] != pin.get("sha256"):
            row["status"] = "changed"
        else:
            try:
                parsed = json.loads(blob)
                row["status"] = "verified" if isinstance(parsed, dict) else "unparseable"
                parsed = parsed if isinstance(parsed, dict) else None
            except ValueError:
                row["status"] = "unparseable"
        data[sid] = parsed
        rows.append(row)
    return data, rows


def observed_at(sid: str, d: dict):
    """The time a source says it describes. Recovery receipts carry several stage times; the newest is the cutoff they cover. None when the file states none."""
    if sid == "inventory":
        return (d.get("observed_at") or {}).get("utc")
    if sid == "ledger":
        return d.get("checked_at_utc")
    if sid == "recovery_base":
        return (d.get("offhost_restore") or {}).get("verified_utc")
    if sid == "recovery_service":
        return (d.get("successful_service_drill") or {}).get("finished_utc")
    if sid == "recovery_studies":
        return ((d.get("final_ui_delta") or {}).get("offhost_restore") or {}).get("verified_utc")
    for k in ("observed_at_utc", "observed_utc", "generated_utc"):
        if isinstance(d.get(k), str):
            return d[k]
    return None


def pin(root: Path, pins_rel: str = PINS) -> dict:
    pins = []
    for sid, rel in SOURCES.items():
        blob, why = read_small(root, rel)
        if blob is None:
            raise SystemExit(f"cannot pin {rel}: {why}")
        pins.append({"id": sid, "path": rel, "sha256": sha256(blob), "bytes": len(blob)})
    doc = {"schema": "frontier.system-operations-pins/1", "note": "Re-pin only after reading what changed. A changed file is shown as unavailable until then.", "pins": pins}
    target = Path(root) / pins_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, indent=1) + "\n")
    return doc


def _unavailable(rows, *needs):
    st = {r["id"]: r["status"] for r in rows}
    bad = {n: st.get(n, "missing") for n in needs if st.get(n) != "verified"}
    return {"status": "unavailable", "reason": "a required receipt is missing, changed since it was pinned, or unreadable; its contents are withheld. This is not zero activity.", "sources": bad} if bad else None


# ------------------------------------------------------------------ sections
def queue_section(d, rows):
    if (u := _unavailable(rows, "queue")):
        return u
    q = d["queue"]
    tasks = [{"job_id": t.get("job_id"), "task": _c(t.get("task"), 120), "owner": _c(t.get("owner"), 90), "provider_state": t.get("provider_state"),
              "provider_state_observed_utc": t.get("provider_state_observed_utc"), "scope": _c(t.get("scope"), 160), "receipt": t.get("receipt") or t.get("completion_receipt")}
             for t in q.get("tasks", [])[:100] if isinstance(t, dict)]
    states: dict = {}
    for t in tasks:
        states[t["provider_state"]] = states.get(t["provider_state"], 0) + 1
    hz = q.get("planning_horizon_utc") or []
    return {"status": "ok", "queue_owner_identity": _c(q.get("owner"), 60), "observed_utc": q.get("observed_at_utc"), "updated_utc": q.get("updated_at_utc"),
            "horizon_utc": hz if len(hz) == 2 else None,
            "horizon_note": "The planning horizon is the window the queue was planned for. It is a plan, not a record of what ran.",
            "tasks": tasks, "task_state_counts": states,
            "tasks_note": f"{len(tasks)} queue rows listed. This is the queue's own task list, not every provider job (see shared jobs), and a provider state is not a scientific outcome.",
            "policies": {k: v for k, v in (q.get("policies") or {}).items() if k != "credentials"}}


def plans_section(d, rows):
    if (u := _unavailable(rows, "queue")):
        return u
    q = d["queue"]
    plan = [{"task": _c(p.get("task"), 120), "owner": _c(p.get("owner"), 90), "priority": p.get("priority"), "recorded_state": _c(p.get("state"), 120),
             "budget": _c(p.get("budget"), 200), "job_id": p.get("job_id")} for p in q.get("preparation", [])[:80] if isinstance(p, dict)]
    nd = q.get("next_ready_dispatch") or {}
    lr = q.get("latest_returns") or {}
    gcp = q.get("gcp") or {}
    prov = {"nebius_allocation": lr.get("allocation_state"), "nebius_active_gpu_jobs": lr.get("active_nebius_gpu_jobs"),
            "running_or_starting_per_queue": {"running": nd.get("running"), "starting": nd.get("starting")},
            "google_compute": {"observed_utc": gcp.get("observed_at_utc"), "global_cpu_limit": gcp.get("global_cpu_limit"), "gpu_quota_granted": gcp.get("gpu_quota_granted"),
                               "active_allocated_vcpus": gcp.get("active_allocated_vcpus"), "active_cpu_vms": gcp.get("active_cpu_vms"), "active_gpu_vms": gcp.get("active_gpu_vms")},
            "meaning": _c((lr.get("allocation_state") or {}).get("interpretation"), 300) or "Requested capacity of nonterminal jobs. RUNNING and IMAGE_PULLING are not utilization."}
    sampled = {"current_gpu_utilization_pct": lr.get("current_gpu_utilization_pct"), "google_cpu_utilization": gcp.get("instantaneous_cpu_utilization"), "windows": []}
    u2 = d.get("usage")
    if u2:
        for w in (u2.get("historical_gpu_telemetry") or [])[:20]:
            sampled["windows"].append({k: w.get(k) for k in ("task_label", "window_utc", "samples", "sample_period_ms", "gpu_utilization_pct_mean", "gpu_utilization_pct_max")})
    sampled["status"] = ("no current sample: utilization is unknown right now" if sampled["current_gpu_utilization_pct"] is None else "a current sample is recorded")
    sampled["note"] = "Windows are historical sampled intervals of finished work. They are not current occupancy, and an unsampled period is unknown, not zero or idle."
    return {"status": "ok", "plans": plan, "plans_note": "Recorded stage text copied from the queue. It mixes planned and finished work; the page does not rank or count it as success.",
            "provider_state": prov, "sampled_utilization": sampled}


def runs_section(d, rows):
    if (u := _unavailable(rows, "runtime")):
        return u
    r = d["runtime"]
    out_rows, groups = [], {"completed": 0, "failed": 0, "partial": 0, "other": 0}
    sec = {"gpu": [0, 0.0], "cpu": [0, 0.0]}
    for x in r.get("rows", [])[:200]:
        partial = bool(x.get("truncated") or x.get("timed_out"))
        st = x.get("provider_state")
        g = "partial" if partial else "completed" if st == "COMPLETED" else "failed" if st == "FAILED" else "other"
        groups[g] += 1
        k = x.get("kind") if x.get("kind") in sec else None
        if k and isinstance(x.get("container_seconds"), (int, float)):
            sec[k][0] += 1
            sec[k][1] += x["container_seconds"]
        out_rows.append({"job_id": x.get("job_id"), "kind": x.get("kind"), "provider_state": st, "group": g, "container_seconds": x.get("container_seconds"),
                         "truncated": x.get("truncated"), "timed_out": x.get("timed_out"), "receipt": x.get("receipt"), "receipt_sha256": x.get("receipt_sha256")})
    stated = r.get("totals") or {}
    recomputed = {k: {"jobs": v[0], "seconds": round(v[1], 1)} for k, v in sec.items()}
    return {"status": "ok", "rows": out_rows, "groups": groups, "recomputed_totals": recomputed, "stated_totals": stated,
            "totals_match": all(recomputed[k] == stated.get(k) for k in recomputed),
            "scope": _c(r.get("scope"), 400),
            "meaning": "Provider job and process completion only. Container seconds include setup and emission; they are not billed time, GPU kernel time or a scientific pass. A failed or partial run stays listed."}


def audits_section(d, rows):
    if (u := _unavailable(rows, "queue")):
        return u
    q = d["queue"]
    items = [{"task": _c(p.get("task"), 120), "recorded_state": _c(p.get("state"), 120), "next_acceptance": _c(p.get("next_acceptance"), 240)}
             for p in q.get("preparation", []) if isinstance(p, dict) and not str(p.get("state", "")).lower().startswith("complete")]
    rr = q.get("regulatory_recovery") or {}
    return {"status": "ok", "not_complete": items,
            "partial": [{"task": "regulatory recovery", "recorded_state": rr.get("state"), "usable": rr.get("usable_union"), "expected": rr.get("expected_union"), "unresolved": rr.get("unresolved")}] if rr else [],
            "note": "The queue has no audit-queue field. These are rows whose recorded state does not begin with `complete`; they are not a count of pending audits, and `complete` rows may still carry a failed or retained result."}


def shared_section(d, rows):
    if (u := _unavailable(rows, "shared")):
        return u
    s = d["shared"]
    own = s.get("ownership_breakdown") or {}
    counts = [c for c in (s.get("counts") or {}).get("all_listed", []) if isinstance(c, dict)]
    by_group: dict = {}
    for c in counts:
        by_group.setdefault(c.get("group"), {}).setdefault(c.get("state"), 0)
        by_group[c.get("group")][c.get("state")] += c.get("jobs", 0)
    ledger = d.get("ledger")
    hist = len(ledger.get("historical_jobs", [])) if ledger else None
    return {"status": "ok", "observed_utc": s.get("observed_at_utc"), "listed_total": s.get("listed_total"),
            "attributed_to_this_team": own.get("current_frontier"), "earlier_team_exact_id_ledger": own.get("historical_team"), "unattributed": own.get("unattributed"),
            "breakdown_sums_to_total": sum(v for v in own.values() if isinstance(v, int)) == s.get("listed_total"),
            "ledger_entries": hist, "ledger_matches_breakdown": (hist == own.get("historical_team")) if hist is not None else None,
            "states_by_group": by_group, "current_gpu_jobs": s.get("current_gpu_jobs"),
            "earliest_listed_creation": s.get("earliest_listed_creation"),
            "meaning": "Unattributed means no exact record attributes the job to this team. It does not say another team owns it. Jobs are counted, not owned: this page claims no authority over others' jobs and offers no cancel control."}


def limits_section(d, rows):
    if (u := _unavailable(rows, "queue")):
        return u
    q, gcp = d["queue"], d["queue"].get("gcp") or {}
    lim = {"gpus_per_job": (q.get("policies") or {}).get("gpus_per_job"), "team_gpu_ceiling": (q.get("policies") or {}).get("team_ceiling"),
           "foreign_waiting_policy": _c((q.get("policies") or {}).get("foreign_waiting"), 80), "google_global_cpu_limit": gcp.get("global_cpu_limit"),
           "google_gpu_quota_granted": gcp.get("gpu_quota_granted")}
    host = None
    if d.get("usage") and d["usage"].get("local_host"):
        h = d["usage"]["local_host"]
        host = {"observed_utc": h.get("observed_at_utc"), "logical_cpus": h.get("logical_cpus"), "load_1_5_15": h.get("load_1_5_15"), "historical": True,
                "note": "Instant reading of the shared build host when recorded; not per-agent use and not current."}
    return {"status": "ok", "limits": lim, "shared_host_reading": host, "note": "Provider quotas and ceilings as recorded in the queue; a limit is not a measure of use."}


def spend_section(d, rows):
    found = []
    for sid, path in (("usage", ("cost",)), ("inventory", ("cost",)), ("queue", ("policies", "provider_cost")), ("queue", ("gcp", "cost"))):
        src = d.get(sid)
        v = src
        for k in path:
            v = v.get(k) if isinstance(v, dict) else None
        found.append({"source": sid, "field": ".".join(path), "recorded": (_c(v if isinstance(v, str) else (v.get("interpretation") if isinstance(v, dict) else None), 200) or "no billed figure recorded") if src else "source unavailable",
                      "billed_figure": (v.get("actual_spend") if isinstance(v, dict) else None) if src else None})
    billed = [f for f in found if isinstance(f["billed_figure"], (int, float))]
    return {"status": "unknown" if not billed else "recorded", "recorded_fields": found, "total": None,
            "meaning": "Actual spend is unknown: no billing meter was queried and no estimate, zero or credit-based figure is inferred. Nothing is summed."
            if not billed else "A source carries a billed figure; each is shown with its source and none is summed."}


def _snap(label, creation, restore, note=None):
    c, r = creation or {}, restore or {}
    return {"label": label, "created_utc": c.get("created_utc"), "files": c.get("file_count"), "capture_errors": c.get("capture_errors"), "archive_sha256": c.get("archive_sha256"),
            "offhost_file_restore_verified_utc": r.get("verified_utc"), "offhost_files_restored": r.get("files_restored"), "offhost_capture_errors": len(r.get("capture_errors") or []) if r else None,
            "note": note}


def recovery_section(d, rows):
    need = ("recovery_base", "recovery_service", "recovery_stable", "recovery_films", "recovery_studies")
    if (u := _unavailable(rows, *need)):
        return u
    b, sv, st, fm, sd = (d[k] for k in need)
    drill = sv.get("successful_service_drill") or {}
    probe = drill.get("application_probe") or {}
    checks = drill.get("checks") or {}
    sdb, delta = sd.get("database") or {}, sd.get("final_ui_delta") or {}
    snaps = [_snap("base file archive", b.get("creation"), b.get("offhost_restore")), _snap("service-drill archive", sv.get("creation"), sv.get("offhost_archive_restore"))]
    snaps += [_snap(f"additive {k}", v.get("creation"), v.get("offhost_restore")) for k, v in (st.get("snapshots") or {}).items()]
    snaps += [_snap(f"additive {k}", v.get("creation"), v.get("offhost_restore")) for k, v in (fm.get("snapshots") or {}).items()]
    snaps += [_snap("additive 0710", sd.get("archive"), sd.get("offhost_restore")), _snap("additive 0720 (static delta)", delta.get("archive"), delta.get("offhost_restore"))]
    snaps.sort(key=lambda s: s["created_utc"] or "")
    src = sd.get("source_recovery") or {}
    preserved = {"service_drill_attempts": len(sv.get("original_failed_attempts_preserved") or []), "stable_failed_captures": len(st.get("failed_captures_preserved") or []),
                 "studies_preparation_failures": len((sd.get("preparation_failures") or {}).get("attempts") or [])}
    remaining = {k: [_c(x, 260) for x in (v.get("remaining") or [])[:8]] for k, v in (("base", b), ("service", sv), ("stable", st))}
    return {"status": "ok",
            "summary": "Not one green state. Files, source commits and the database are restored on a separate host to different cutoffs; the full application was exercised only at an older source and database.",
            "latest_file_and_source_checkpoint": {"snapshot_created_utc": (sd.get("archive") or {}).get("created_utc"), "release_revision": sd.get("release_revision"),
                                                  "off_host_file_restore": {"verified_utc": (sd.get("offhost_restore") or {}).get("verified_utc"), "files_restored": (sd.get("offhost_restore") or {}).get("files_restored"),
                                                                            "capture_errors": len((sd.get("offhost_restore") or {}).get("capture_errors") or [])},
                                                  "off_host_source_recovery": {"verified_utc": src.get("verified_utc"), "required_revision": src.get("required_revision"), "verify_exit": src.get("verify_exit"),
                                                                               "fetch_exit": src.get("fetch_into_separate_recovery_refs_exit")},
                                                  "later_static_delta": {"release_revision": (delta.get("capture_contract") or {}).get("release_revision"),
                                                                         "source_verified_utc": (delta.get("source_recovery") or {}).get("verified_utc"),
                                                                         "files_restored": (delta.get("offhost_restore") or {}).get("files_restored")}},
            "database_cutoff": {"captured_utc": sdb.get("captured_utc"), "record_versions": (sdb.get("table_counts") or {}).get("record_versions"),
                                "event_rows": (sdb.get("table_counts") or {}).get("events"), "raw_restore_counts_identical": sdb.get("raw_restore_counts_identical"),
                                "replay": _c((sd.get("scope") or {}).get("full_service_drill"), 420),
                                "meaning": "Cutoff of the logical database copy. Writes after it are not in that copy."},
            "older_application_drill": {"started_utc": drill.get("started_utc"), "finished_utc": drill.get("finished_utc"), "source_sha": drill.get("source_sha"),
                                        "record_versions_at_that_cutoff": (probe.get("table_counts_before_disposable_write") or {}).get("record_versions"),
                                        "success": drill.get("success"), "checks_passed": sum(1 for v in checks.values() if v is True), "checks_total": len(checks),
                                        "scope": _c(drill.get("scope"), 200), "applies_to_latest_source_or_database": False,
                                        "meaning": "A real application and MCP drill on a separate host, at this older source and database only. It does not cover the later source, records or media."},
            "snapshot_chain": snaps, "failed_attempts_preserved": preserved, "remaining_per_source": remaining,
            "not_established": ["Application restore at the latest source and database", "Restore without fresh credentials", "A public-domain cutover", "Anything written after the cutoffs above"]}


def documents():
    return [{"path": p, "href": REPO_BLOB + p} for p in (DOC, "docs/recovery/README.md", "docs/resource-utilization.md")]


# ------------------------------------------------------------------ the projection
def project(root=ROOT, at: str | None = None, pins_rel: str = PINS) -> dict:
    root = Path(root)
    data, rows = load_sources(root, pins_rel)
    q = data.get("queue") or {}
    shown_at = at or now_iso()
    qobs = _ts(q.get("observed_at_utc"))
    for r in rows:                                          # each source's own observation time and whether it is a historical cutoff
        r["observed"] = observed_at(r["id"], data.get(r["id"]) or {})
        t = _ts(r["observed"])
        r["historical_cutoff"] = bool(qobs and t and (qobs - t).total_seconds() > HIST_AFTER_S) if t else None
    sections = {"queue": queue_section, "plans": plans_section, "runs": runs_section, "audits": audits_section, "shared_jobs": shared_section, "limits": limits_section,
                "spend": spend_section, "recovery": recovery_section}
    out = {"schema": SCHEMA, "projected_at_utc": shown_at, "scope": "A bounded projection of committed queue and receipt files, each pinned by sha256. It measures nothing and starts nothing.",
           "event_scope": "Provider and queue records of this hackathon only.", "sources": rows, "documents": documents(),
           "agents": {"status": "not published", "reason": "No receipt gives a current active-agent total, so none is shown."}}
    for k, fn in sections.items():
        try:
            out[k] = fn(data, rows)
        except Exception:                                   # noqa: BLE001 - a failing section degrades alone and exports no exception text
            out[k] = {"status": "unavailable", "reason": "section could not be built from the receipts"}
    return out


def build(ins, out: dict, root=ROOT) -> dict:
    """Publisher adapter: add the projection as a static site file. `ins` is build_site's Inputs (unused: reads go through the pinned allowlist)."""
    p = project(root)
    out["@" + SITE_PATH] = (json.dumps(p, indent=1, sort_keys=True) + "\n").encode()
    return {"href": SITE_PATH, "status": {k: (p[k] or {}).get("status") for k in ("queue", "runs", "recovery", "shared_jobs")}}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Project the existing queue/receipts for the System Operations tab.")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--at", default=None, help="projection time (UTC ISO); default now")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pin", action="store_true", help="write the pins file from the current source bytes")
    g.add_argument("--write", action="store_true", help=f"write site/{SITE_PATH}")
    a = ap.parse_args(argv)
    if a.pin:
        print(json.dumps({p["id"]: p["sha256"][:12] for p in pin(a.root)["pins"]}, indent=1))
    else:
        target = a.root / "site" / PurePosixPath(SITE_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(project(a.root, a.at), indent=1, sort_keys=True) + "\n")
        print(target)


if __name__ == "__main__":
    main()
