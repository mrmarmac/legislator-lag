"""Draw the pilot sample and split it into coding batches.

    python -m legislag.sample [--n 100] [--seed 20261114]

Design: equal allocation by country, proportional by chamber within country,
simple random sampling within chamber. Each record carries `weight`, the number
of corpus speeches it stands for, so pilot estimates can be re-weighted.
A reliability subset is drawn from the sample and coded a second time.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict

from .config import DATA

PILOT = DATA / "pilot"


def allocate(sizes: dict[str, int], n: int) -> dict[str, int]:
    """Largest-remainder proportional allocation."""
    total = sum(sizes.values())
    exact = {k: n * v / total for k, v in sizes.items()}
    out = {k: int(x) for k, x in exact.items()}
    for k in sorted(exact, key=lambda k: exact[k] - out[k], reverse=True)[: n - sum(out.values())]:
        out[k] += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261114)
    ap.add_argument("--batches", type=int, default=5)
    ap.add_argument("--reliability", type=int, default=20)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    by_country: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    with open(DATA / "speeches_ai.jsonl", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            by_country[r["country"]][r["chamber"]].append(r)

    sample: list[dict] = []
    per_country = args.n // len(by_country)
    for country in sorted(by_country):
        chambers = by_country[country]
        alloc = allocate({k: len(v) for k, v in chambers.items()}, per_country)
        for chamber in sorted(chambers):
            pool = sorted(chambers[chamber], key=lambda r: r["speech_id"])
            for r in rng.sample(pool, alloc[chamber]):
                r["weight"] = round(len(pool) / alloc[chamber], 3)
                sample.append(r)
            print(f"{chamber}: {alloc[chamber]} of {len(pool)}")

    # Deal speeches into batches longest-first so each batch has similar reading load.
    sample.sort(key=lambda r: (-r["word_count"], r["speech_id"]))
    batches: list[list[dict]] = [[] for _ in range(args.batches)]
    for i, r in enumerate(sample):
        lap, pos = divmod(i, args.batches)
        b = pos if lap % 2 == 0 else args.batches - 1 - pos
        r["batch"] = b + 1
        batches[b].append(r)

    reliability = []
    per_batch = args.reliability // args.batches
    for b in batches:
        reliability.extend(rng.sample(b, per_batch))

    (PILOT / "batches").mkdir(parents=True, exist_ok=True)

    def dump(path, rows):
        with open(path, "w", encoding="utf-8") as fh:
            for r in sorted(rows, key=lambda r: (r["date"], r["speech_id"])):
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    dump(PILOT / "sample.jsonl", sample)
    for i, b in enumerate(batches, 1):
        dump(PILOT / "batches" / f"batch_{i}.jsonl", b)
        print(f"batch {i}: {len(b)} speeches, {sum(r['word_count'] for r in b)} words")
    dump(PILOT / "batches" / "batch_reliability.jsonl", reliability)
    print(f"reliability batch: {len(reliability)} speeches, "
          f"{sum(r['word_count'] for r in reliability)} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
