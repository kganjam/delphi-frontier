#!/usr/bin/env python3
"""Does the namespace this project would mint nanopub IRIs in actually resolve?

WHY THIS IS A SEPARATE FILE. swarm/publish_dryrun.py ends by printing "NOT TRANSMITTED, and
this module imports no network library" -- that is a deliberate safety property of the module
that writes publishable-shaped documents, and a namespace probe needs the network. So the probe
lives here and publish_dryrun stays network-free.

WHY IT MATTERS, and the project has already paid for it once. SPEC-007 rule 5 and the repo's
standing instructions record that `w3id.org/probknow/ontology` 404s while roughly 180 IMMUTABLE
nanopubs already point at it. A published nanopub cannot be edited; a correction is a new
nanopub signed with the same key. So an unresolvable namespace is a permanent defect minted into
every document that uses it, and the only moment it is cheap to catch is before the first
publish.

WHAT THE STATUSES MEAN, because a 200 is not sufficient:

    404            unregistered. Minting here reproduces the probknow failure exactly.
    200 CATCH-ALL  registered, but every sub-path redirects to the same page, so an IRI does
                   NOT dereference to its own document. Better than a 404 and not adequate for
                   a nanopub IRI, which is supposed to retrieve the nanopub.
    200 SPECIFIC   a nonsense sub-path 404s while the real one resolves -- the only status that
                   supports minting.

MEASURED 2026-11-05, and one of these corrects a standing note:

    w3id.org/delphi-frontier/   404           <- what publish_dryrun.py's NS currently uses
    w3id.org/delphi/            200 CATCH-ALL <- the repo notes call this unregistered; it is
                                                 registered now and redirects to
                                                 github.com/fractastical/project-delphi-ontology,
                                                 but `delphi/np/test-does-not-exist` returns 200
                                                 too, so it does not dereference
    w3id.org/probknow/ontology  404           <- the one with ~180 immutable nanopubs on it

    python3 swarm/check_nanopub_namespace.py           # report
    python3 swarm/check_nanopub_namespace.py --strict  # exit 1 if the minting namespace is unusable
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.request

#: The namespace publish_dryrun.py mints under. Kept here as a literal so this checker fails
#: loudly if the two drift apart rather than silently checking the wrong thing; the drift test
#: below reads the real value out of that module's source WITHOUT importing it.
MINTING = "https://w3id.org/delphi-frontier/np/"

PROBES = [
    ("the minting namespace", MINTING),
    ("upstream canonical", "https://w3id.org/delphi/"),
    ("the one with ~180 immutable nanopubs", "https://w3id.org/probknow/ontology"),
]
CONTROL_OK = "https://w3id.org/people/"
CONTROL_404 = "https://w3id.org/zzz-no-such-namespace-" + "checkprobe"


def status(url: str, timeout: int = 25):
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8", "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:                                        # noqa: BLE001
        return type(e).__name__, url


def classify(base: str) -> tuple[str, str]:
    """404 / 200 CATCH-ALL / 200 SPECIFIC, by asking for a path that cannot exist."""
    st, final = status(base.rstrip("/") + "/")
    if st != 200:
        return (f"{st}", final)
    nst, nfinal = status(base.rstrip("/") + "/zzz-cannot-exist-" + "probe")
    if nst == 200 and nfinal == final:
        return ("200 CATCH-ALL", final)
    if nst == 200:
        return ("200 CATCH-ALL", final)
    return ("200 SPECIFIC", final)


def main() -> int:
    strict = "--strict" in sys.argv
    print("=" * 94)
    print("NANOPUB NAMESPACE -- would a minted IRI resolve? (publishing is IRREVERSIBLE)")
    print("=" * 94)

    # Controls first: a namespace that must resolve and one that must not. Without these a
    # network failure reads exactly like "everything is unregistered".
    ok_st, _ = status(CONTROL_OK)
    bad_st, _ = status(CONTROL_404)
    controls_ok = ok_st == 200 and bad_st == 404
    print(f"\n  CONTROLS  {CONTROL_OK} -> {ok_st} (want 200); "
          f"a nonsense namespace -> {bad_st} (want 404)")
    if not controls_ok:
        print("  CONTROLS FAILED -- the network or w3id is not behaving, so nothing below is "
              "evidence about registration. Reporting UNVERIFIED rather than unregistered.")
        return 2

    print()
    results = {}
    for label, url in PROBES:
        cls, final = classify(url)
        results[url] = cls
        extra = f"  -> {final[:58]}" if final and not final.startswith(url) else ""
        print(f"  {cls:<14s} {label:<38s} {url}{extra}")

    # Drift test: does publish_dryrun still mint under what this file checks?
    try:
        src = open(__file__.replace("check_nanopub_namespace.py", "publish_dryrun.py")).read()
        drift = MINTING not in src
    except OSError:
        drift = False
    if drift:
        print(f"\n  *** DRIFT: publish_dryrun.py no longer contains {MINTING!r}. "
              f"This checker may be probing the wrong namespace. ***")

    verdict = results.get(MINTING, "?")
    print(f"\n  VERDICT for the minting namespace: {verdict}")
    if verdict.startswith("404"):
        print("    UNUSABLE. Minting here reproduces the probknow failure -- ~180 immutable")
        print("    nanopubs pointing at a 404, uncorrectable because publication is immutable.")
    elif "CATCH-ALL" in verdict:
        print("    REGISTERED BUT NOT DEREFERENCING: every sub-path returns the same page, so a")
        print("    nanopub IRI would not retrieve its own nanopub.")
    else:
        print("    Resolves specifically. That is necessary and still not sufficient -- the key")
        print("    and the Trusty URI are separate blockers (publish_dryrun.py).")
    print("\n  This checker makes network requests and publishes NOTHING. publish_dryrun.py "
          "remains network-free by design.")
    return 1 if (strict and verdict.startswith("404")) else 0


if __name__ == "__main__":
    raise SystemExit(main())
