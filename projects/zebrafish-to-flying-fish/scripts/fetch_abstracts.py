#!/usr/bin/env python3
"""Fetch Europe PMC records (title, abstract, journal, DOI, licence flag) for a fixed id list
or queries, saved verbatim with sha256. Read-level of everything saved is `abstract` at most."""
import json, hashlib, urllib.request, urllib.parse, datetime, sys, time, pathlib
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
JOBS = json.load(open(sys.argv[2]))
led = []
def get(q, name):
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
        {"query": q, "format": "json", "resultType": "core", "pageSize": 8})
    for i in range(4):
        try: b = urllib.request.urlopen(url, timeout=60).read(); break
        except Exception:
            if i == 3: raise
            time.sleep(3)
    (OUT / f"{name}.json").write_bytes(b)
    led.append({"name": name, "query": q, "url": url, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")})
for name, q in JOBS.items(): get(q, name)
(OUT / "ledger.json").write_text(json.dumps(led, indent=1))
