"""Fetch AI debates through the TheyWorkForYou and OpenAustralia APIs.

    export TWFY_API_KEY=...            # https://www.theyworkforyou.com/api/key
    export OPENAUSTRALIA_API_KEY=...   # https://www.openaustralia.org.au/api/key
    python -m legislag.fetch_api [--since 2026-07-01] [--until 2026-11-14]

Writes data/speeches_ai_api.jsonl in the same schema as legislag.parse, with
`source` set to "api". A chamber whose key variable is unset is skipped.

How it works. Both APIs expose getDebates with a `search` argument but no date
argument that combines with it, so the date window goes inside the search
string as `YYYYMMDD..YYYYMMDD`. Search rows may carry only an extract, so each
hit's parent debate is then fetched by `gid` to get full speech text. Speeches
are finally re-filtered with the same AI_PATTERN used on the bulk XML.

STATUS: written from the published API documentation and exercised only
against recorded example payloads. It has not been run against the live APIs,
because no keys were available when it was written. Compare its output with
data/speeches_ai.jsonl on first use.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
from urllib.parse import parse_qs, urlparse

import requests

from .config import API_SEARCH_TERMS, CHAMBERS, DATA, START_DATE, Chamber
from .parse import clean, make_record

UA = {"User-Agent": "legislag/0.1 (research pipeline)"}
TAG = re.compile(r"<[^>]+>")
PARA = re.compile(r"</p\s*>|<br\s*/?>", re.I)
PAGE_SIZE = 100
PAUSE = 0.5  # seconds between calls; both services are run by small charities


class ApiError(RuntimeError):
    pass


def call(ch: Chamber, key: str, **params) -> object:
    query = {"key": key, "type": ch.api_type, "output": "json", **params}
    for attempt in range(4):
        try:
            r = requests.get(ch.api_base, params=query, headers=UA, timeout=120)
            r.raise_for_status()
            payload = r.json()
            break
        except (requests.RequestException, ValueError) as e:
            if attempt == 3:
                # Never include the request URL here: it contains the key.
                raise ApiError(f"{ch.key}: request failed ({type(e).__name__})") from None
            time.sleep(2 ** (attempt + 1))
    time.sleep(PAUSE)
    if isinstance(payload, dict) and payload.get("error"):
        raise ApiError(f"{ch.key}: {payload['error']}")
    return payload


def body_to_text(body: str) -> str:
    """API bodies are HTML fragments. Keep paragraph breaks, drop tags."""
    parts = [clean(html.unescape(TAG.sub(" ", p))) for p in PARA.split(body or "")]
    return "\n\n".join(p for p in parts if p)


def parent_gid(row: dict) -> str | None:
    """The debate a search hit belongs to, read from its `listurl`."""
    url = html.unescape(row.get("listurl") or "")
    ids = parse_qs(urlparse(url).query).get("id")
    return ids[0] if ids else None


def search_hits(ch: Chamber, key: str, since: str, until: str) -> dict[str, dict]:
    """Map parent debate gid -> one representative search row."""
    window = f"{since.replace('-', '')}..{until.replace('-', '')}"
    debates: dict[str, dict] = {}
    for term in API_SEARCH_TERMS:
        page = 1
        while True:
            payload = call(ch, key, search=f"{term} {window}", order="d",
                           num=PAGE_SIZE, page=page)
            rows = payload.get("rows", []) if isinstance(payload, dict) else []
            for row in rows:
                gid = parent_gid(row) or row.get("gid")
                if gid and since <= (row.get("hdate") or since) <= until:
                    debates.setdefault(gid, row)
            info = payload.get("info", {}) if isinstance(payload, dict) else {}
            total = int(info.get("total_results") or 0)
            if not rows or page * PAGE_SIZE >= total:
                break
            page += 1
    return debates


def rows_of(payload: object) -> list[dict]:
    """getDebates?gid= returns a list of rows, or a dict wrapping one."""
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        for k in ("rows", "data"):
            if isinstance(payload.get(k), list):
                return [r for r in payload[k] if isinstance(r, dict)]
    return []


def speeches_in_debate(ch: Chamber, payload: object) -> list[dict]:
    out = []
    heading = subheading = ""
    for row in rows_of(payload):
        htype = str(row.get("htype"))
        text = body_to_text(row.get("body") or "")
        if htype == "10":
            heading, subheading = text, ""
        elif htype == "11":
            subheading = text
        elif htype == "12":
            speaker = row.get("speaker") or {}
            name = clean(" ".join(filter(None, [speaker.get("first_name"),
                                                speaker.get("last_name")]))
                         or speaker.get("name") or "")
            if not name:
                continue
            rec = make_record(ch, row.get("hdate") or "", row.get("gid") or "",
                              name, heading, subheading, text, "api")
            if rec:
                if speaker.get("party"):
                    rec["party"] = speaker["party"]
                out.append(rec)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", default=START_DATE)
    ap.add_argument("--until", default=dt.date.today().isoformat())
    args = ap.parse_args()

    records: dict[str, dict] = {}
    skipped = []
    for ch in CHAMBERS:
        key = os.environ.get(ch.key_env)
        if not key:
            skipped.append(f"{ch.key} ({ch.key_env} not set)")
            continue
        debates = search_hits(ch, key, args.since, args.until)
        print(f"{ch.key}: {len(debates)} debates with search hits")
        for gid in sorted(debates):
            for rec in speeches_in_debate(ch, call(ch, key, gid=gid)):
                if args.since <= rec["date"] <= args.until:
                    records[rec["speech_id"]] = rec
    for s in skipped:
        print("skipped:", s)
    if not records:
        print("no speeches fetched; nothing written")
        return 1 if skipped else 0

    rows = sorted(records.values(), key=lambda r: (r["date"], r["speech_id"]))
    with open(DATA / "speeches_ai_api.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} speeches to data/speeches_ai_api.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
