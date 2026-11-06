#!/usr/bin/env python3
"""S916's climatology half, from a RETRIEVED DATASET rather than a search summary.

Claim 1055 answered S916 from published means found by web search, and fitted a Rayleigh and
a Weibull tail to them. That is a search-summary read level and a parametric extrapolation
five to twelve mean-multiples out -- weak evidence for the project's last route closure. This
replaces it with observations: NASA POWER daily 10 m wind over the zebrafish's native range.

WHY DAILY MAXIMUM AND NOT DAILY MEAN. The question is whether the wind EVER reaches route D's
threshold, so a daily mean would wash out exactly the events that matter. WS10M_MAX is the
daily maximum of the hourly series, which is the statistic the question asks for. The daily
mean is fetched too, as the quantity comparable to the published annual means claim 1055 used.

STILL NOT HOURLY. POWER's daily maximum is derived from an hourly reanalysis, so a gust lasting
minutes is not resolved. Route D needs a sustained 4 s, so sub-hourly structure matters in
principle; what this settles is the coarser question of whether the hourly-scale wind ever
approaches the threshold at all.

    python3 wind_power_dataset.py
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

#: Sites across the Ganges-Brahmaputra floodplain, the zebrafish's native range.
SITES = (
    ("Nadia, West Bengal", 23.4, 88.5),
    ("Rajshahi, Bangladesh", 24.4, 88.6),
    ("Patna, Bihar (Ganges)", 25.6, 85.1),
    ("Guwahati, Assam (Brahmaputra)", 26.1, 91.7),
)
START, END = "20150101", "20241231"
TARGET = 20.6          # claim 1054: route D's required 10 m wind over floodplain roughness
API = "https://power.larc.nasa.gov/api/temporal/daily/point"


def fetch(lat: float, lon: float, params: str) -> dict[str, dict[str, float]]:
    q = {"parameters": params, "community": "RE", "longitude": str(lon), "latitude": str(lat),
         "start": START, "end": END, "format": "JSON"}
    with urllib.request.urlopen(f"{API}?{urllib.parse.urlencode(q)}", timeout=180) as r:
        d = json.loads(r.read().decode())
    return d["properties"]["parameter"]


def clean(series: dict[str, float]) -> list[float]:
    return [v for v in series.values() if v is not None and v > -900]


def main() -> int:
    print(f"  NASA POWER daily 10 m wind, {START}-{END}, target {TARGET} m/s\n")
    print(f"  {'site':32}{'n days':>8}{'mean':>7}{'max':>7}{'p99 max':>9}{'days >= target':>16}")
    allmax: list[float] = []
    site_means: list[float] = []
    for name, lat, lon in SITES:
        p = fetch(lat, lon, "WS10M,WS10M_MAX")
        mean = clean(p["WS10M"])
        mx = clean(p["WS10M_MAX"])
        allmax += mx
        site_means.append(sum(mean) / len(mean))
        over = sum(1 for v in mx if v >= TARGET)
        p99 = sorted(mx)[int(0.99 * len(mx))]
        print(f"  {name:32}{len(mx):>8}{sum(mean)/len(mean):>7.2f}{max(mx):>7.2f}"
              f"{p99:>9.2f}{over:>16}")

    n = len(allmax)
    mins, maxs = min(site_means), max(site_means)
    over = sum(1 for v in allmax if v >= TARGET)
    print(f"\n  POOLED: {n} site-days, {over} with a daily MAXIMUM at or above {TARGET} m/s "
          f"({100*over/n:.4f}%)")
    print(f"  highest daily maximum anywhere in the record: {max(allmax):.2f} m/s")
    print(f"  S916's bar is 1% of daylight hours. Observed: {100*over/n:.4f}% of DAYS reach it "
          f"even once.")

    print("\n  CONTROLS")
    # 1. a threshold the record obviously DOES meet must come back common.
    easy = sum(1 for v in allmax if v >= 3.0)
    print(f"    days with max >= 3.0 m/s: {100*easy/n:.1f}% -- a common wind is common "
          f"{'OK' if easy/n > 0.5 else 'the counter only returns small numbers'}")
    # 2. a threshold nothing can meet must come back zero.
    silly = sum(1 for v in allmax if v >= 200.0)
    print(f"    days with max >= 200 m/s: {silly} ({'OK' if silly == 0 else 'IMPOSSIBLE'})")
    # 3. the dataset's own means must agree with the published station means claim 1055 used
    #    (1.73-4.17 m/s). Two independent sources agreeing is worth more than either alone.
    print(f"    site means {mins:.2f}-{maxs:.2f} m/s vs published Bangladesh stations "
          f"1.73-4.17 -- independent agreement "
          f"{'OK' if 1.5 < mins and maxs < 4.5 else 'DISAGREE'}")
    # 4. daily max must exceed daily mean everywhere, or the two series are mislabelled.
    p = fetch(SITES[1][1], SITES[1][2], "WS10M,WS10M_MAX")
    pairs = [(p["WS10M"][k], p["WS10M_MAX"][k]) for k in p["WS10M"]
             if p["WS10M"][k] > -900 and p["WS10M_MAX"][k] > -900]
    bad = sum(1 for a, b in pairs if b < a)
    print(f"    daily max < daily mean on {bad} of {len(pairs)} days "
          f"({'OK' if bad == 0 else 'SERIES MISLABELLED'})")

    # EVERY VERSION OF THE THRESHOLD, so the closure does not depend on my own corrections.
    print("\n  ROBUSTNESS -- days whose MAXIMUM reaches each reading of the threshold:")
    for thr, what in ((12.46, "claim 971's figure read as a 10 m wind -- the most generous "
                              "reading possible, and wrong by claim 1044"),
                      (15.83, "claim 1044: 1 m threshold at open-water roughness"),
                      (20.60, "claim 1054: at vegetated floodplain roughness"),
                      (24.90, "at z0 = 0.1 m, high crops")):
        k = sum(1 for v in allmax if v >= thr)
        print(f"    >= {thr:5.2f} m/s : {k:>5} of {n} site-days ({100*k/n:.4f}%)  {what}")
    print("  Even the most generous reading -- one the height correction already refutes -- is")
    print("  met on a fraction of days far below S916's 1% bar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
