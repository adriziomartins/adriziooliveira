#!/usr/bin/env python3
"""Audit local links, anchors and image paths in a static GitHub Pages site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append((tag, key, a[key]))

pages = {}
for path in ROOT.rglob("*.html"):
    if ".git" in path.parts:
        continue
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    pages[path.resolve()] = parser

issues = []
external = set()
for source, parser in pages.items():
    for tag, key, raw in parser.refs:
        parts = urlsplit(raw)
        if parts.scheme or parts.netloc or raw.startswith("//"):
            external.add(raw)
            continue
        if not parts.path and not parts.fragment:
            continue
        target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
        if target.is_dir():
            target = target / "index.html"
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            issues.append((source, raw, "path outside repository"))
            continue
        if not target.is_file():
            issues.append((source, raw, "missing file"))
        elif parts.fragment and target.suffix.lower() == ".html":
            parsed = pages.get(target)
            if parsed and unquote(parts.fragment) not in parsed.ids:
                issues.append((source, raw, "missing anchor"))

print(f"HTML pages: {len(pages)} | External URLs (not HTTP-tested): {len(external)}")
if issues:
    for source, raw, reason in issues:
        print(f"ERROR {source.relative_to(ROOT)} -> {raw}: {reason}")
    sys.exit(1)
print("PASS: all local file links and HTML anchors resolve.")
