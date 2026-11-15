"""Where each coding run keeps its inputs and labels.

    pilot   100 sampled speeches, coded in a Claude session under codebook v0.1
    full    every speech in the sampling frame, coded by legislag.code_api
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .config import AI_PATTERN, DATA

# The full run codes speeches with at least this many AI terms.
MIN_AI_TERMS = 2


@dataclass(frozen=True)
class Run:
    name: str
    speeches: Path          # JSONL of speeches this run draws on
    labels_dir: Path
    main: tuple[str, ...]   # glob patterns (stems) for files holding the first coding
    second: tuple[str, ...]  # patterns for files holding the independent second coding
    label: str              # how the run is described to readers


RUNS = {
    "pilot": Run("pilot", DATA / "pilot" / "sample.jsonl", DATA / "pilot" / "labels",
                 tuple(f"batch_{i}" for i in range(1, 6)), ("batch_reliability",), "Pilot"),
    "full": Run("full", DATA / "speeches_ai.jsonl", DATA / "full" / "labels",
                ("main", "batch_*"), ("reliability", "rel_*"), "Full run"),
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def ai_mentions(speech: dict) -> int:
    return len(AI_PATTERN.findall(speech["text"]))


def load_speeches(run: Run) -> dict[str, dict]:
    return {r["speech_id"]: r for r in read_jsonl(run.speeches)}


def load_frame(min_terms: int = MIN_AI_TERMS) -> list[dict]:
    """Speeches eligible for the full run, in date order."""
    rows = [r for r in read_jsonl(RUNS["full"].speeches) if ai_mentions(r) >= min_terms]
    return sorted(rows, key=lambda r: (r["date"], r["speech_id"]))


def load_labels(run: Run, stems: tuple[str, ...]) -> dict[str, dict]:
    """Label rows keyed by speech. A later row for the same speech wins."""
    rows: dict[str, dict] = {}
    for pattern in stems:
        for path in sorted(run.labels_dir.glob(f"{pattern}.jsonl")):
            for row in read_jsonl(path):
                row["coder"] = row.get("coder") or path.stem
                rows[row["speech_id"]] = row
    return rows
