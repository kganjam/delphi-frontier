#!/usr/bin/env python3
"""Enumerate the figures of every open-access paper this project cites, and say which are readable.

WHY. Claim 493 established that this project's blocking magnitudes "live in the figures and the
extraction drops them", and claims 527, 528, 529 and 531 then settled three subproblems by reading
figures that the text could not supply. That worked one paper at a time. This enumerates the whole
cited corpus so the remaining blocked numbers can be found rather than stumbled on.

WHAT IT DOES NOT DO. It does not read the figures. Enumeration is cheap and listing a figure is not
reading it -- the same distinction the research-report read-levels draw. It reports what EXISTS so
a reader can be pointed at the right panel, and it records the ones that are unavailable, because
"this paper's figures are not retrievable" is a finding that stops the next session repeating the
fetch (claim 493's own stated purpose).

Usage:  python3 figure_sweep.py            # all known PMCIDs
        python3 figure_sweep.py PMC9172250 # one
"""
from __future__ import annotations

import json
import re
import time
import subprocess
import sys
import urllib.parse
from pathlib import Path

# DOI -> PMCID for every open-access paper cited in the live claim graph, resolved via the
# NCBI id converter. NO-PMC entries are kept deliberately: an absent paper is a finding.
CORPUS = {
    "10.1016/j.cub.2021.08.054":   ("PMC9172250",  "Daane 2021 Curr Biol - flying-fish phenocopy"),
    "10.1038/s41598-018-28450-6":  ("PMC6039437",  "Daane 2018 Sci Rep - kcnk5b/alf, READ"),
    "10.1371/journal.pbio.3002565": ("PMC10experimental", "Jiang 2024 PLoS Biol - pectoral bud, READ"),
    "10.7554/eLife.60691":         ("PMC8110307",  "Yi 2021 eLife - S345, READ"),
    "10.1016/j.ydbio.2019.08.016": ("PMC7235970",  "Lanni 2019 Dev Biol - schleier/Kcc4a"),
    "10.1111/joa.12785":           ("PMC6480674",  "Murciano 2018 J Anat - inter-ray, READ"),
    "10.1242/dev.204739":          ("PMC13078715", "Development"),
    "10.1093/icb/icz145":          ("PMC6907395",  "Integr Comp Biol"),
    "10.1242/jeb.243180":          ("PMC10658917", "J Exp Biol"),
    "10.1242/jeb.203.2.333":       (None,          "J Exp Biol 2000 - NOT open access"),
    "10.1016/j.ydbio.2017.07.024": (None,          "Koenig 2017 - NOT open access (actinotrichia)"),
    "10.1101/2024.03.27.587111":   (None,          "bioRxiv preprint - no PMC record"),

    # BIOMECHANICS. Added 2026-11-04 after finding the corpus above was almost entirely
    # developmental genetics -- fin-SIZE genes -- while the project's blocking magnitudes had
    # become mechanical: stiffness, power, frequency, elastic storage. The project was asking
    # mechanical questions of a genetics corpus, which is why so many came back "nobody has
    # measured this". Two of these answered critical-path questions within an hour of being
    # found (claims 592, 593), and neither was in the corpus.
    "10.1002/jmor.20161":          (None,          "Flammang 2013 J Morphol - fin ray EI 565e-6 Nm2, claim 592"),
    "10.1098/rspb.2001.1731":      ("PMC1088836",  "Young & Rome 2001 - muscle power vs frequency, claim 593"),
    "10.1098/rsif.2006.0181":      ("PMC2359861",  "Alben 2007 - fin ray force-displacement, >10x active stiffness"),
    "10.1002/jmor.20830":          (None,          "Aiello 2018 J Morphol - fin ray EI across labrids"),
    "10.1242/jeb.046052":          (None,          "Park & Choi 2010 - flying fish gliding, measured L/D and ground effect"),
    "10.1242/jeb.201.10.1505":     (None,          "Wakeling 1998 - fast-start muscle power 142.7 W/kg"),
    "10.1242/jeb.205.2.189":       (None,          "Syme & Shadwick 2002 - tuna red muscle power vs cycle frequency"),
    "10.1146/annurev.physiol.68.040104.105418": (None, "Rome 2006 review - superfast muscle design"),
    "10.1242/jeb.200.11.1549":     (None,          "Walker & Westneat 1997 - labriform flapping kinematics"),
    "10.1242/jeb.205.2.177":       (None,          "Walker & Westneat 2002 - flapping vs rowing performance"),
}

FIGCAP = re.compile(r'(?:Fig(?:ure)?\.?\s*\d+[A-Za-z]?\.?\s+)([^<]{20,200})')


# PMC THROTTLES, AND A THROTTLED PAGE IS NOT AN EMPTY PAGE. After a handful of rapid requests
# it serves a ~21 KB stub instead of the ~325 KB article, with no figure images in it. The first
# version of this sweep read that as "no figure images found -- record as not retrievable here"
# for SEVEN papers, two of whose figures had been downloaded by hand minutes earlier. That is the
# empty-set failure with a plausible cover story: the mechanism ran, returned nothing, and the
# nothing was reported as a property of the papers.
STUB_BYTES = 60_000          # a real PMC article page is several hundred KB
PAUSE_S = 6                  # between requests, to stay under the throttle


CAPTCHA_MARKERS = ("RecaptchaChallengePageUi", "preparing to download", "unusual traffic",
                   "Performing security verification", "are you a robot")


def looks_blocked(html: str) -> str:
    """Name WHY a fetch failed. 'Throttled', 'captcha' and 'embargoed' are different facts and
    only one of them is worth retrying soon. The first version of this sweep collapsed all of
    them into 'not retrievable here', which is how an EMBARGOED paper (PMC11911126, released
    2026-11-18) came to be recorded as a fetch problem."""
    low = html.lower()
    if any(m.lower() in low for m in CAPTCHA_MARKERS):
        return "captcha/rate-limited"
    if "will be available in pmc on" in low:
        return "EMBARGOED"
    if len(html) < STUB_BYTES:
        return "stub/throttled"
    return ""


def fetch(url: str, timeout: int = 70, tries: int = 3) -> str:
    out = ""
    for i in range(tries):
        r = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "-A", "Mozilla/5.0", url],
                           capture_output=True, text=True, timeout=timeout + 20)
        out = r.stdout
        if len(out) >= STUB_BYTES:
            return out
        time.sleep(PAUSE_S * (i + 1))      # back off and retry; a stub is transient
    return out


def figures_of(pmcid: str) -> tuple[list[str], list[str]]:
    """Return (figure image urls, caption snippets) for a PMC article.

    THE TWO LISTS ARE NOT PAIRED AND MUST NOT BE ZIPPED. `urls` is sorted by the CDN hash
    path; `caps` is in document order. Nothing relates element i of one to element i of the
    other, and on PMC9172250 the orders genuinely differ -- zipping them hands you Figure 2's
    image under Figure 4's caption, which is how a figure read of the "double-mutant phenocopy"
    came back showing an evolutionary-rate plot. Use `figures_paired()` when the pairing
    matters, which is whenever a specific figure is wanted. These two are kept for the callers
    that only count or list.
    """
    html = fetch(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/")
    if len(html) < STUB_BYTES:
        # Say THROTTLED, not "no figures". The distinction is the whole point.
        raise RuntimeError(f"throttled: {pmcid} returned {len(html)} bytes "
                           f"(a real article page is >{STUB_BYTES//1000} KB)")
    # PMC serves figure images from cdn.ncbi.nlm.nih.gov/pmc/blobs/<hash>/<pmcid>/<hash>/<name>.
    # The first version of this looked for the OLD "/bin/" path and found ZERO images on every
    # paper -- reporting "not retrievable here" for articles whose figures were sitting in the
    # HTML. A scraper matching a pattern the site no longer uses returns the same empty list as
    # a paywalled article, which is the empty-set failure wearing a plausible explanation.
    urls = sorted(set(re.findall(
        r'https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^"\']+?\.(?:jpg|png)', html)))
    # icons and logos live under the same CDN; keep only per-article blobs
    urls = [u for u in urls if "/blobs/" in u and "favicon" not in u and "logo" not in u]
    if not urls:
        urls = sorted(set(re.findall(r'https://[^"\']*?/bin/[^"\']+?\.(?:jpg|png)', html)))
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    caps = []
    for m in re.finditer(r'(Fig(?:ure)?\s*\d+[A-Za-z]?)[.\s]{1,3}([A-Z][^.]{25,180}\.)', text):
        s2 = f"{m.group(1)}. {m.group(2)}"
        if s2 not in caps:
            caps.append(s2)
    return urls, caps[:12]


FIG_BLOCK = re.compile(r'<figure[^>]*\bclass="[^"]*\bfig\b[^"]*"[^>]*>(.*?)</figure>', re.S)
FIG_HEAD = re.compile(r'<h4[^>]*class="[^"]*obj_head[^"]*"[^>]*>(.*?)</h4>', re.S)
FIG_IMG = re.compile(r'<img[^>]+src="(https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^"]+?'
                     r'\.(?:jpg|png))"', re.S)


def figures_paired(pmcid: str) -> list[dict]:
    """Pair each figure's image with ITS OWN caption, from inside the same <figure> element.

    This exists because the parallel lists above cannot be zipped, and the failure is silent:
    you get a real image and a real caption, both from the right paper, describing different
    figures. Nothing downstream can tell. A figure read then measures the wrong plot and
    reports a number with controls that all pass, because the controls check the reading, not
    the identity of what was read.
    """
    html = fetch(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/")
    if len(html) < STUB_BYTES:
        raise RuntimeError(f"throttled: {pmcid} returned {len(html)} bytes "
                           f"(a real article page is >{STUB_BYTES//1000} KB)")
    out = []
    for block in FIG_BLOCK.findall(html):
        im = FIG_IMG.search(block)
        if not im:
            continue
        hd = FIG_HEAD.search(block)
        head = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', hd.group(1))).strip() if hd else ""
        lab = re.match(r'(Fig(?:ure)?\s*\d+)', head)
        out.append({"label": lab.group(1) if lab else "", "url": im.group(1),
                    "caption": head})
    return out
def main() -> int:
    want = sys.argv[1:] or [v[0] for v in CORPUS.values() if v[0] and v[0].startswith("PMC")]
    label = {v[0]: v[1] for v in CORPUS.values() if v[0]}
    out = {}
    print(f"{len(CORPUS)} cited paper(s); "
          f"{sum(1 for v in CORPUS.values() if v[0] is None)} with no PMC record\n")
    # POSITIVE CONTROL FIRST. PMC9172250's figures were downloaded by hand, so if the sweep
    # reports zero for IT the sweep is broken and every other zero is meaningless. Refuse rather
    # than produce a report nobody can trust.
    try:
        ctrl_urls, _ = figures_of("PMC9172250")
    except RuntimeError as e:
        print(f"  CONTROL FAILED -- {e}")
        print("  Refusing to sweep: a throttled fetch and an article without figures look the "
              "same from here.")
        return 2
    if not ctrl_urls:
        print("  CONTROL FAILED: PMC9172250 is known to carry 4 figures and this sweep found 0.")
        print("  Refusing to report any other zero.")
        return 2
    print(f"  control ok: PMC9172250 -> {len(ctrl_urls)} figure image(s)\n")

    for pmcid in want:
        if not re.fullmatch(r"PMC\d+", pmcid):
            print(f"  SKIP {pmcid}: not a well-formed PMCID (placeholder in the table)")
            continue
        time.sleep(PAUSE_S)
        try:
            urls, caps = figures_of(pmcid)
        except RuntimeError as e:
            print(f"  {pmcid:<13} THROTTLED -- {e}")
            out[pmcid] = {"urls": [], "captions": [], "throttled": True,
                          "label": label.get(pmcid, "")}
            continue
        print(f"  {pmcid:<13} {len(urls):>2} figure image(s)   {label.get(pmcid,'')}")
        for c in caps[:4]:
            print(f"       - {c[:112]}")
        out[pmcid] = {"urls": urls, "captions": caps, "label": label.get(pmcid, "")}
        if not urls:
            print("       (no figure images found at this URL -- record as not retrievable here)")
    print("\n  NOT OPEN ACCESS, recorded so the next session does not refetch:")
    for doi, (p, lab) in CORPUS.items():
        if p is None:
            print(f"    {doi}  {lab}")
    dest = Path(__file__).resolve().parent.parent / "results/figure-reads/corpus-figures.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1))
    print(f"\n  wrote {dest}")
    print("  NOTE: listing a figure is NOT reading it. This says what exists, nothing more.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
