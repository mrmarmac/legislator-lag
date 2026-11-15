"""Check coder output against the codebook's structural rules.

    python -m legislag.validate [--run pilot|full] FILE [FILE...]

Checks that every quote is an exact substring of its speech, enumerated fields
hold allowed values, and dates are well formed. A label file named after a
batch file must also cover exactly that batch. Exits non-zero on any error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .runs import RUNS, load_speeches
from .schema import check_row


def validate_file(path: Path, speeches: dict[str, dict]) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    seen: set[str] = set()
    n_claims = 0
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}:{ln}: invalid JSON ({e})")
            continue
        sid = row.get("speech_id")
        if sid not in speeches:
            errors.append(f"{path.name}:{ln}: unknown speech_id {sid!r}")
            continue
        if sid in seen:
            errors.append(f"{path.name}:{ln}: duplicate {sid}")
        seen.add(sid)
        n_claims += len(row.get("claims") or [])
        errors += [f"{sid}: {e}" for e in check_row(row, speeches[sid]["text"])]

    # A label file named after a batch must cover exactly that batch.
    batch_file = path.parent.parent / "batches" / path.name
    if batch_file.exists():
        expected = {json.loads(l)["speech_id"]
                    for l in batch_file.read_text().splitlines() if l.strip()}
        errors += [f"{path.name}: speech not coded: {s}" for s in sorted(expected - seen)]
        errors += [f"{path.name}: speech not in this batch: {s}" for s in sorted(seen - expected)]
    return len(seen), n_claims, errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", choices=sorted(RUNS), default="pilot")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    speeches = load_speeches(RUNS[args.run])
    bad = 0
    for arg in args.files:
        n, n_claims, errors = validate_file(Path(arg).resolve(), speeches)
        print(f"{arg}: {n} speeches, {n_claims} claims, {len(errors)} errors")
        for e in errors:
            print("  -", e)
        bad += len(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
