import json
import shutil
from pathlib import Path

from frontier import system_operations as so

REAL = Path(__file__).resolve().parents[1]


def sandbox(tmp_path):
    for rel in [*so.SOURCES.values(), so.PINS]:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REAL / rel, tmp_path / rel)
    return tmp_path


def test_committed_pins_match_and_every_section_builds():
    p = so.project(REAL, at="2026-11-01T00:00:00Z")
    assert all(s["status"] == "verified" for s in p["sources"]), [s for s in p["sources"] if s["status"] != "verified"]
    assert all(p[k]["status"] == "ok" for k in ("queue", "plans", "runs", "audits", "shared_jobs", "limits", "recovery"))


def test_changed_receipt_is_unavailable_not_zero_and_only_its_sections_degrade(tmp_path):
    root = sandbox(tmp_path)
    f = root / so.SOURCES["queue"]
    d = json.loads(f.read_text())
    d["tasks"] = []
    f.write_text(json.dumps(d))
    p = so.project(root)
    assert p["queue"]["status"] == "unavailable" and "tasks" not in p["queue"]
    assert next(s for s in p["sources"] if s["id"] == "queue")["status"] == "changed"
    assert p["runs"]["status"] == "ok" and p["shared_jobs"]["status"] == "ok"


def test_missing_and_unpinned_receipts_are_unavailable(tmp_path):
    root = sandbox(tmp_path)
    (root / so.SOURCES["shared"]).unlink()
    pins = json.loads((root / so.PINS).read_text())
    pins["pins"] = [x for x in pins["pins"] if x["id"] != "runtime"]
    (root / so.PINS).write_text(json.dumps(pins))
    p = so.project(root)
    assert p["shared_jobs"]["status"] == "unavailable" and p["shared_jobs"]["sources"]["shared"] == "missing"
    assert p["runs"]["status"] == "unavailable" and p["runs"]["sources"]["runtime"] == "not-pinned"


def test_no_pins_file_makes_everything_unavailable(tmp_path):
    root = sandbox(tmp_path)
    (root / so.PINS).unlink()
    p = so.project(root)
    assert all(p[k]["status"] == "unavailable" for k in ("queue", "runs", "shared_jobs", "recovery"))


def test_spend_unknown_no_agent_total_and_no_forbidden_text():
    p = so.project(REAL, at="2026-11-01T00:00:00Z")
    assert p["spend"]["status"] == "unknown" and p["spend"]["total"] is None
    assert p["agents"]["status"] == "not published" and set(p["agents"]) == {"status", "reason"}
    assert not so.FORBIDDEN.search(json.dumps(p))


def test_runs_recompute_totals_and_keep_failures():
    r = so.project(REAL)["runs"]
    assert r["totals_match"] and r["groups"]["failed"] >= 1
    assert sum(r["groups"].values()) == len(r["rows"])
    assert "a scientific pass" in r["meaning"] and "not billed time" in r["meaning"]


def test_shared_jobs_split_and_claim_no_authority():
    s = so.project(REAL)["shared_jobs"]
    assert s["breakdown_sums_to_total"] and s["ledger_matches_breakdown"]
    assert s["attributed_to_this_team"] + s["earlier_team_exact_id_ledger"] + s["unattributed"] == s["listed_total"]
    assert "no authority" in s["meaning"] and "does not say another team owns" in s["meaning"]


def test_recovery_layers_are_separate_and_older_drill_is_not_applied_to_latest():
    r = so.project(REAL)["recovery"]
    assert r["older_application_drill"]["applies_to_latest_source_or_database"] is False
    assert r["older_application_drill"]["source_sha"] != r["latest_file_and_source_checkpoint"]["release_revision"]
    assert r["database_cutoff"]["captured_utc"] and r["latest_file_and_source_checkpoint"]["off_host_file_restore"]["files_restored"]
    assert "Application restore at the latest source and database" in r["not_established"]
    assert "restored" not in r["summary"].split("Not one green state")[0]


def test_historical_cutoffs_are_flagged():
    cut = {s["id"]: s["historical_cutoff"] for s in so.project(REAL)["sources"]}
    assert cut["recovery_service"] is True and cut["queue"] is False


def test_adapter_stages_only_the_projection_file():
    out = {}
    so.build(Ins(REAL), out, REAL)
    assert list(out) == ["@" + so.SITE_PATH]
    assert json.loads(out["@" + so.SITE_PATH])["schema"] == so.SCHEMA


def test_committed_site_file_equals_projection():
    f = REAL / "site" / so.SITE_PATH
    committed = json.loads(f.read_text())
    assert committed["projected_at_utc"] is None
    assert so.project(REAL, None) == committed


class Ins:
    """Stand-in for build_site.Inputs: reads under `root` and remembers path, sha256 and size."""

    def __init__(self, root):
        self.root, self.seen = Path(root), {}

    def read(self, rel):
        b = (self.root / rel).read_bytes()
        self.seen[rel] = {"sha256": so.sha256(b), "bytes": len(b)}
        return b


def run_build(root):
    ins, out = Ins(root), {}
    so.build(ins, out, root)
    return ins, out["@" + so.SITE_PATH]


def test_build_is_deterministic_and_stamps_no_wall_clock():
    a_ins, a = run_build(REAL)
    _, b = run_build(REAL)
    assert a == b
    p = json.loads(a)
    assert p["projected_at_utc"] is None and p["latest_source_observation_utc"]
    assert a == (REAL / "site" / so.SITE_PATH).read_bytes()          # same bytes as the CLI-written committed file


def test_build_records_every_consumed_input():
    ins, _ = run_build(REAL)
    want = {so.PINS, so.MODULE, *so.SOURCES.values()}
    assert want <= set(ins.seen)
    assert ins.seen[so.MODULE]["sha256"] == so.sha256((REAL / so.MODULE).read_bytes())


def test_changing_a_pinned_source_changes_output_and_is_refused(tmp_path):
    root = sandbox(tmp_path)
    (root / "frontier").mkdir(exist_ok=True)
    shutil.copy(REAL / so.MODULE, root / so.MODULE)
    _, before = run_build(root)
    f = root / so.SOURCES["shared"]
    d = json.loads(f.read_text())
    d["listed_total"] += 1
    f.write_text(json.dumps(d))
    ins, after = run_build(root)
    assert after != before and so.SOURCES["shared"] in ins.seen          # the changed file was still recorded
    p = json.loads(after)
    assert p["shared_jobs"]["status"] == "unavailable" and p["queue"]["status"] == "ok"


def test_inverse_rd_telemetry_is_a_historical_window_not_current():
    s = so.project(REAL)["plans"]["sampled_utilization"]
    w = next(x for x in s["windows"] if "Inverse Schnakenberg" in x["task_label"])
    assert (w["samples"], round(w["gpu_utilization_pct_mean"], 2), w["gpu_utilization_pct_max"]) == (363, 32.27, 37.0)
    assert "not current" in s["note"] or "not current occupancy" in s["note"]


def test_recovery_cutoffs_unchanged_and_in_progress_backup_not_claimed():
    r = so.project(REAL)["recovery"]
    assert r["database_cutoff"]["captured_utc"] == "2026-11-01T07:04:11.807435+00:00"
    assert r["latest_file_and_source_checkpoint"]["release_revision"].startswith("d87e5d1")
    assert "in progress" in r["later_work_note"] and "None is claimed complete" in r["later_work_note"]
