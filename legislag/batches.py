"""Split the full-run frame into coding batches of similar reading load.

    python -m legislag.batches [--words 8000] [--reliability 60] [--seed 20261115]

Writes data/full/batches/batch_NNN.jsonl, which together hold every speech in
the frame exactly once, and rel_NN.jsonl, a random subset to be coded a second
time by coders who have not seen the first coding.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys

from .runs import RUNS, load_frame


def pack(speeches: list[dict], target_words: int) -> list[list[dict]]:
    """Longest speech first, each into the batch with the fewest words so far."""
    n = max(1, math.ceil(sum(s["word_count"] for s in speeches) / target_words))
    bins: list[list[dict]] = [[] for _ in range(n)]
    load = [0] * n
    for s in sorted(speeches, key=lambda s: (-s["word_count"], s["speech_id"])):
        i = load.index(min(load))
        bins[i].append(s)
        load[i] += s["word_count"]
    return bins


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--words", type=int, default=8000, help="target words per batch")
    ap.add_argument("--reliability", type=int, default=60, help="speeches to code twice")
    ap.add_argument("--seed", type=int, default=20261115)
    args = ap.parse_args()

    frame = load_frame()
    out = RUNS["full"].labels_dir.parent / "batches"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.jsonl"):
        old.unlink()

    def dump(name: str, rows: list[dict]) -> None:
        with open(out / name, "w", encoding="utf-8") as fh:
            for r in sorted(rows, key=lambda r: (r["date"], r["speech_id"])):
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    main_bins = pack(frame, args.words)
    for i, b in enumerate(main_bins, 1):
        dump(f"batch_{i:03d}.jsonl", b)
    subset = random.Random(args.seed).sample(
        sorted(frame, key=lambda r: r["speech_id"]), min(args.reliability, len(frame)))
    rel_bins = pack(subset, args.words)
    for i, b in enumerate(rel_bins, 1):
        dump(f"rel_{i:02d}.jsonl", b)

    sizes = [len(b) for b in main_bins]
    words = [sum(s["word_count"] for s in b) for b in main_bins]
    print(f"{len(frame)} speeches in {len(main_bins)} batches: "
          f"{min(sizes)}-{max(sizes)} speeches, {min(words)}-{max(words)} words each")
    print(f"{len(subset)} speeches in {len(rel_bins)} reliability batches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
