#!/usr/bin/env python3
"""Check external URLs referenced by HTML pages (standard library only)."""
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            url = a.get(key, "")
            if urlsplit(url).scheme in ("http", "https"):
                self.urls.append(url)

sources = defaultdict(set)
for page in ROOT.rglob("*.html"):
    if ".git" in page.parts:
        continue
    parser = References()
    parser.feed(page.read_text(encoding="utf-8"))
    for url in parser.urls:
        sources[url].add(str(page.relative_to(ROOT)))

def check(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ArchiveLinkAudit/1.0)",
               "Range": "bytes=0-0"}
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=12) as response:
            return str(response.status), response.geturl(), response.headers.get("Content-Type", "")
    except HTTPError as error:
        return str(error.code), error.geturl(), error.headers.get("Content-Type", "")
    except (URLError, TimeoutError, OSError) as error:
        return "NETWORK_ERROR", url, str(error)[:180]

rows = []
for index, url in enumerate(sorted(sources), 1):
    status, final, kind = check(url)
    if status in ("200", "206"):
        verdict = "OK_HTTP"
    elif status in ("401", "403", "429"):
        verdict = "RESTRICTED_OR_INCONCLUSIVE"
    elif status == "NETWORK_ERROR" or status.startswith("5"):
        verdict = "RETRY_OR_INCONCLUSIVE"
    else:
        verdict = "REVIEW"
    rows.append([verdict, status, url, final, kind, "; ".join(sorted(sources[url]))])
    print(f"[{index}/{len(sources)}] {verdict} ({status}) {url}", flush=True)

destination = ROOT / "docs" / "external-links-audit.csv"
destination.parent.mkdir(parents=True, exist_ok=True)
with destination.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["result", "http_status", "source_url", "final_url", "content_type_or_error", "referenced_by"])
    writer.writerows(rows)

print(f"Checked {len(rows)} URLs; report: {destination.relative_to(ROOT)}")
print("Note: HTTP success does not prove historical accuracy, provenance, or reproduction rights.")
if any(row[0] == "REVIEW" for row in rows):
    sys.exit(1)
