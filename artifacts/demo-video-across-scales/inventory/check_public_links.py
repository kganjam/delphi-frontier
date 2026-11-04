"""Check the inventory's public links without downloading whole media files."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import json


def check(url):
    try:
        with urlopen(Request(url, method="HEAD", headers={"User-Agent": "Delphi-media-archive-check/1"}), timeout=15) as response:
            return {"url": url, "status": response.status, "resolved_url": response.url,
                    "content_type": response.headers.get("Content-Type", ""),
                    "content_length": response.headers.get("Content-Length", "")}
    except HTTPError as error:
        return {"url": url, "status": error.code, "error": error.reason}
    except (URLError, TimeoutError, OSError) as error:
        return {"url": url, "status": None, "error": str(error)}


def main():
    here = Path(__file__).resolve().parent
    data = json.loads((here / "simulation-inventory.json").read_text())
    urls = sorted({row[key] for row in data["records"] for key in ("video_url", "figure_url", "source_manifest") if row.get(key)})
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, urls))
    output = {
        "checked_at_seattle": datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "method": "HTTP HEAD of each distinct nonempty public media and source-manifest URL; four concurrent requests; 15-second per-request timeout.",
        "scope": "Link availability only. No scientific validation and no guarantee of future availability.",
        "links": results,
    }
    (here / "public-link-checks.json").write_text(json.dumps(output, indent=2) + "\n")
    failed = [row for row in results if row["status"] != 200]
    print(json.dumps({"checked": len(results), "non_200": failed}, indent=2))


if __name__ == "__main__":
    main()
