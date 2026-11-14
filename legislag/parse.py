"""Turn raw Hansard XML into one JSON line per AI-mentioning speech.

    python -m legislag.parse

Reads data/raw/<chamber>/*.xml and writes data/speeches_ai.jsonl plus
data/corpus_stats.json. The raw files are treated as data only.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

from .config import AI_PATTERN, CHAMBERS, DATA, RAW, START_DATE, Chamber

NAME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})([a-z]?)\.xml$")
# The chair reading out a list of grouped amendments is not a speech. These
# entries run to tens of thousands of words of legislative text.
AMENDMENT_LIST = "With this it will be convenient to discuss"
WS = re.compile(r"\s+")


def latest_versions(folder: Path) -> list[tuple[str, Path]]:
    """UK files carry a version letter (a, b, c). Keep the last one per day."""
    best: dict[str, tuple[str, Path]] = {}
    for f in folder.glob("*.xml"):
        m = NAME_RE.search(f.name)
        if not m:
            continue
        day, ver = m.group(1), m.group(2)
        if day not in best or ver > best[day][0]:
            best[day] = (ver, f)
    return [(day, best[day][1]) for day in sorted(best)]


def clean(text: str) -> str:
    return WS.sub(" ", text).strip()


def speech_text(el: ET.Element) -> str:
    paras = [clean("".join(p.itertext())) for p in el.iter("p")]
    paras = [p for p in paras if p]
    if not paras:
        paras = [clean("".join(el.itertext()))]
    return "\n\n".join(p for p in paras if p)


def make_record(ch: Chamber, day: str, gid: str, speaker: str, heading: str,
                subheading: str, text: str, source: str) -> dict | None:
    if text.startswith(AMENDMENT_LIST):
        return None
    terms = sorted({m.group(0) for m in AI_PATTERN.finditer(text)})
    if not terms:
        return None
    return {
        "speech_id": f"{ch.key}:{gid}",
        "country": ch.country,
        "chamber": ch.key,
        "chamber_label": ch.label,
        "date": day,
        "speaker": speaker,
        "heading": heading,
        "subheading": subheading,
        "url": ch.web_url.format(gid=gid),
        "word_count": len(text.split()),
        "ai_terms": terms,
        "source": source,
        "text": text,
    }


def parse_file(ch: Chamber, day: str, path: Path) -> tuple[int, list[dict]]:
    root = ET.parse(path).getroot()
    heading = subheading = ""
    total, out = 0, []
    for el in root:
        if el.tag == "major-heading":
            heading, subheading = clean("".join(el.itertext())), ""
        elif el.tag == "minor-heading":
            subheading = clean("".join(el.itertext()))
        elif el.tag == "speech":
            speaker = el.get("speakername") or ""
            if el.get("nospeaker") == "true" or not speaker:
                continue  # procedural text, not a member speaking
            total += 1
            gid = (el.get("id") or "").rsplit("/", 1)[-1]
            rec = make_record(ch, day, gid, speaker, heading, subheading,
                              speech_text(el), "bulk")
            if rec:
                out.append(rec)
    return total, out


def main() -> int:
    records: list[dict] = []
    stats: dict[str, dict] = {}
    for ch in CHAMBERS:
        days = [(d, p) for d, p in latest_versions(RAW / ch.key) if d >= START_DATE]
        s = defaultdict(int)
        for day, path in days:
            total, recs = parse_file(ch, day, path)
            s["sitting_days"] += 1
            s["speeches"] += total
            s["ai_speeches"] += len(recs)
            s["ai_words"] += sum(r["word_count"] for r in recs)
            records.extend(recs)
        s["first_day"] = days[0][0] if days else None
        s["last_day"] = days[-1][0] if days else None
        stats[ch.key] = dict(s)
        print(ch.key, dict(s))

    records.sort(key=lambda r: (r["date"], r["speech_id"]))
    with open(DATA / "speeches_ai.jsonl", "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (DATA / "corpus_stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(f"wrote {len(records)} speeches to data/speeches_ai.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
