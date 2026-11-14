"""Download the keyless bulk Hansard XML published by TheyWorkForYou and OpenAustralia.

    python -m legislag.fetch_bulk [--since 2026-07-01]

Files land in data/raw/<chamber>/. Existing files are skipped, so reruns only
fetch new sitting days.
"""
from __future__ import annotations

import argparse
import re
import sys
import time

import requests

from .config import CHAMBERS, RAW, START_DATE

FILE_RE = re.compile(r'href="([A-Za-z-]*(\d{4}-\d{2}-\d{2})[a-z]?\.xml)"')
UA = {"User-Agent": "legislag/0.1 (research pipeline)"}


def get(url: str, tries: int = 4) -> requests.Response:
    for attempt in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=120)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt == tries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("unreachable")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", default=START_DATE, help="first sitting date, YYYY-MM-DD")
    args = ap.parse_args()

    for ch in CHAMBERS:
        out = RAW / ch.key
        out.mkdir(parents=True, exist_ok=True)
        names = sorted({m.group(1) for m in FILE_RE.finditer(get(ch.bulk_index).text)
                        if m.group(2) >= args.since})
        new = 0
        for name in names:
            dest = out / name
            if dest.exists() and dest.stat().st_size > 0:
                continue
            dest.write_bytes(get(ch.bulk_index + name).content)
            new += 1
        print(f"{ch.key}: {len(names)} files since {args.since}, {new} downloaded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
