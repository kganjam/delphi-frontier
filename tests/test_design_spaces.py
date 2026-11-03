"""Every design space pins its figures by the bytes it copied, and its markdown twin is generated, not written.

Two failure modes are worth a test here. The first is a figure drifting away from the digest the page prints beside it, which
would make the digest decorative. The second is the markdown document and the page disagreeing, which is what happens to every
pair of hand-maintained twins: `--check` is the thing that stops it, so it is exercised in both directions.

These tests are parameterised over whatever design spaces the repository declares rather than naming one, because the point of
the design-space family is that a new one is a data directory. A new design space therefore arrives already tested, and a test
that silently covered nothing would be caught by `test_the_registry_is_not_empty` below -- a parameterised suite over an empty
list passes without running anything, which is this repository's vacuous-acceptance failure in miniature.
"""
import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SNAP = json.loads((ROOT / "site/data/snapshot.json").read_text())
SPACES = SNAP.get("design_spaces") or {}
IDS = sorted(SPACES)


def index_of(ds_id: str) -> dict:
    return json.loads((ROOT / f"results/{ds_id}/index.json").read_text())


def test_the_registry_is_not_empty_and_matches_the_content_directory():
    """The positive control for every parameterised test below: an empty registry would make all of them pass vacuously."""
    declared = sorted(p.stem for p in (ROOT / "site/content/design-spaces").glob("*.json"))
    assert declared, "no design space is declared in site/content/design-spaces/"
    assert IDS == declared, "the snapshot's design spaces and the content directory disagree"


@pytest.mark.parametrize("ds_id", IDS)
def test_the_block_is_built_from_the_authored_files_and_names_both_digests(ds_id):
    block = SPACES[ds_id]
    assert block["id"] == ds_id
    assert block["content_sha256"] == sha256((ROOT / block["content_path"]).read_bytes()).hexdigest()
    assert block["index_sha256"] == sha256((ROOT / block["index_path"]).read_bytes()).hexdigest()
    assert [s["id"] for s in block["studies"]] == [s["id"] for s in index_of(ds_id)["studies"]], "the index decides which studies exist"


@pytest.mark.parametrize("ds_id", IDS)
def test_every_present_figure_matches_the_bytes_the_page_offers(ds_id):
    block = SPACES[ds_id]
    served = ROOT / "site"
    seen = 0
    for study in block["studies"]:
        for fig in study["figures"]:
            if fig["state"] != "present":
                assert fig["href"] is None and fig["sha256"] is None, "an absent figure must not carry a link or a digest"
                continue
            copied = served / fig["href"]
            assert copied.is_file(), f"{fig['href']} is offered by the page and is not in the site tree"
            raw = copied.read_bytes()
            assert sha256(raw).hexdigest() == fig["sha256"] and len(raw) == fig["bytes"]
            source = ROOT / f"results/{ds_id}/figures" / fig["file"]
            assert source.read_bytes() == raw, "the copy served must be the recorded result, byte for byte"
            seen += 1
    assert seen == block["counts"]["figures_present"]


@pytest.mark.parametrize("ds_id", IDS)
def test_a_declared_study_that_is_absent_is_reported_rather_than_dropped(ds_id):
    block = SPACES[ds_id]
    for study in block["studies"]:
        on_disk = (ROOT / study["data_path"]).exists()
        assert study["present"] is on_disk
        if not on_disk:
            assert study["data"] is None and study["data_href"] is None
    assert block["counts"]["studies_declared"] == len(index_of(ds_id)["studies"])


@pytest.mark.parametrize("ds_id", IDS)
def test_every_figure_carries_an_authored_caption_and_alt_text(ds_id):
    for study in index_of(ds_id)["studies"]:
        for fig in study.get("figures", []):
            assert fig.get("caption", "").strip(), f"{ds_id}: {fig['file']} has no caption"
            assert fig.get("alt", "").strip(), f"{ds_id}: {fig['file']} has no alt text"


@pytest.mark.parametrize("ds_id", IDS)
def test_a_schematic_declares_every_pin_against_a_scale_the_page_has(ds_id):
    """A pin pointing at a scale no route uses renders greyed-out by design; a pin pointing at a scale the page never declares is
    a mistake, because its caption line would print a raw key where a label belongs."""
    block = SPACES[ds_id]
    schematic = block.get("schematic")
    if not schematic:
        pytest.skip(f"{ds_id} declares no schematic")
    assert schematic.get("svg"), "a schematic with no drawing would render an empty figure"
    assert schematic.get("desc", "").strip(), "the drawing needs a description for anyone not seeing it"
    keys = {s["key"] for s in block.get("scales", [])}
    for pin in schematic.get("pins", []):
        assert pin["scale"] in keys, f"{ds_id}: pin {pin['name']!r} names scale {pin['scale']!r}, which the page does not declare"


def test_the_markdown_twins_are_current_and_check_can_fail():
    run = lambda *a: subprocess.run([sys.executable, "scripts/designspace_doc.py", *a], cwd=ROOT, capture_output=True, text=True)
    assert run("--check").returncode == 0, "a committed document is stale; run python3 scripts/designspace_doc.py"
    docs = [ROOT / json.loads((ROOT / SPACES[i]["content_path"]).read_text())["doc"] for i in IDS
            if "doc" in json.loads((ROOT / SPACES[i]["content_path"]).read_text())]
    assert docs, "no design space declares a markdown twin, so --check above proved nothing"
    for doc in docs:                          # the positive control, per document: --check must notice one that has drifted
        original = doc.read_bytes()
        try:
            doc.write_bytes(original + b"\ndrifted\n")
            assert run("--check").returncode == 1, f"--check did not notice drift in {doc.name}"
        finally:
            doc.write_bytes(original)
    assert run("--check").returncode == 0


def test_every_served_figure_is_tracked_in_git():
    """A figure can exist in the worktree, pass every other test here, and still 404 in production.

    The deploy ships a `git archive` of a commit, so an untracked build artifact is invisible to it. The browser tests
    cannot catch this: they run against a local server reading the worktree, where the file is present. And a headless
    broken-image count does not catch it either, because a lazy-loaded image that has not loaded reports `complete`
    false and is excluded from the count rather than reported as broken -- which is exactly how four xenobot figures
    reached production as 404s while a live check said zero broken images.

    So this test asks git, not the filesystem. It is cheap and it is the only thing between a green suite and a page of
    missing pictures.
    """
    tracked = set(subprocess.run(["git", "ls-files", "site/artifacts"], cwd=ROOT, capture_output=True, text=True,
                                 check=True).stdout.split())
    assert tracked, "control: `git ls-files site/artifacts` returned nothing, so this test proves nothing"
    missing = []
    for ds_id, block in SPACES.items():
        for study in block["studies"]:
            for fig in study["figures"]:
                if fig["state"] != "present":
                    continue
                path = f"site/{fig['href']}"
                if path not in tracked:
                    missing.append(f"{ds_id}: {path}")
    assert not missing, "served but untracked, so these would 404 in production:\n  " + "\n  ".join(missing)


@pytest.mark.parametrize("ds_id", IDS)
def test_no_prose_asserts_a_control_outcome_its_own_data_contradicts(ds_id):
    """The failure this whole family keeps hitting: a claim about one's own data, restated away from the data.

    It reached production once. A coral study's `control_arm.passed` was False with a failed check named, its headline said
    so correctly -- and the index study SUMMARY, a different field in a different file, still said "Both pre-declared controls
    pass". The page rendered both, contradicting itself, because the integrator checked the field he had been looking at
    rather than every field carrying the claim.

    So this asks the question of every string in the block, not of the one that was wrong last time: if a study's data says a
    control failed, no prose anywhere in that study may say its controls passed.
    """
    import re as _re
    ALL_PASS = _re.compile(r"\b(all|both)\b[^.]{0,60}\bcontrols?\b[^.]{0,20}\bpass", _re.I)
    assert ALL_PASS.search("Both pre-declared controls pass and the sweep moves"), "control: the pattern must match the known-bad sentence"
    assert not ALL_PASS.search("5 of 6 pre-declared controls pass and 1 FAILS"), "control: it must NOT match the corrected sentence"

    for study in SPACES[ds_id]["studies"]:
        data = study.get("data") or {}
        failed = []
        for blk in (v for v in data.values() if isinstance(v, dict)):
            if blk.get("failed_checks"):
                failed += list(blk["failed_checks"])
            if blk.get("passed") is False:
                failed = failed or ["<a control block reports passed: false>"]
        if not failed:
            continue
        def strings(o, path=""):
            if isinstance(o, dict):
                for k, v in o.items(): yield from strings(v, f"{path}.{k}")
            elif isinstance(o, list):
                for i, v in enumerate(o): yield from strings(v, f"{path}[{i}]")
            elif isinstance(o, str):
                yield path, o
        for path, s in strings(study, ds_id + ":" + study["id"]):
            m = ALL_PASS.search(s)
            assert not m, (f"{path} claims all controls pass while the study's own data reports "
                           f"failed checks {failed}: ...{s[max(0, m.start()-60):m.end()+60]}...")
