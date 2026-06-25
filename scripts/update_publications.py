#!/usr/bin/env python3
"""Refresh publication metadata from Crossref.

The site remains reviewable and stable:
1. data/publications.json is the source displayed by the website.
2. The script queries works that Crossref associates with the configured ORCID.
3. New works are appended with metadata from Crossref.
4. Existing manual fields such as status, abstract, featured, and type overrides are preserved.

Crossref records do not always include an author's ORCID. Therefore, review every automated
addition before publishing and keep missing works in data/publications.json manually.
"""

from __future__ import annotations
import html
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ORCID = "0000-0002-1982-9818"
MAILTO = os.environ.get("CROSSREF_MAILTO", "minwookang91@gmail.com")
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "publications.json"
OUTPUT_JS = ROOT / "data" / "publications.js"

def get_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": f"MinwooKangWebsite/1.0 (mailto:{MAILTO})"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def clean(value: str) -> str:
    return html.unescape(value or "").strip()

def year_from(item: dict) -> int:
    for field in ("published-print", "published-online", "issued", "created"):
        parts = item.get(field, {}).get("date-parts")
        if parts and parts[0]:
            return int(parts[0][0])
    return 0

def authors_from(item: dict) -> str:
    rendered = []
    for author in item.get("author", []):
        family = clean(author.get("family", ""))
        given = clean(author.get("given", ""))
        initials = " ".join(part[0] + "." for part in given.replace("-", " ").split() if part)
        name = ", ".join(part for part in [family, initials] if part)
        if author.get("ORCID", "").endswith(ORCID):
            name = f"<strong>{name}</strong>"
        rendered.append(name)
    if len(rendered) > 1:
        return ", ".join(rendered[:-1]) + ", & " + rendered[-1]
    return rendered[0] if rendered else ""

def main() -> None:
    current = json.loads(OUTPUT.read_text(encoding="utf-8"))
    by_doi = {entry["doi"].lower(): entry for entry in current if entry.get("doi")}
    params = urllib.parse.urlencode({
        "filter": f"orcid:{ORCID}",
        "rows": 100,
        "mailto": MAILTO,
        "select": "DOI,title,author,container-title,published-print,published-online,issued,created,type,subtype"
    })
    payload = get_json(f"https://api.crossref.org/works?{params}")
    added = 0

    for item in payload["message"]["items"]:
        doi = clean(item.get("DOI", "")).lower()
        if not doi or doi in by_doi:
            continue
        title_list = item.get("title") or []
        venue_list = item.get("container-title") or []
        crossref_type = item.get("type", "")
        entry = {
            "year": year_from(item),
            "type": "Preprint" if crossref_type == "posted-content" else "Article",
            "title": clean(title_list[0] if title_list else "Untitled"),
            "authors": authors_from(item),
            "venue": clean(venue_list[0] if venue_list else ""),
            "doi": doi
        }
        current.append(entry)
        by_doi[doi] = entry
        added += 1

    current.sort(key=lambda record: (record.get("year", 0), record.get("title", "")), reverse=True)
    serialized = json.dumps(current, indent=2, ensure_ascii=False)
    OUTPUT.write_text(serialized + "\n", encoding="utf-8")
    OUTPUT_JS.write_text("window.PUBLICATIONS = " + serialized + ";\n", encoding="utf-8")
    print(f"Added {added} new Crossref record(s). Review data/publications.json before publishing.")

if __name__ == "__main__":
    main()
