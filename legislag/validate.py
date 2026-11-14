"""Check coder output against the codebook's structural rules.

    python -m legislag.validate data/pilot/labels/batch_1.jsonl [more files...]

Checks every speech in the matching batch is present, every quote is an exact
substring of its speech, enumerated fields hold allowed values, and dates are
well formed. Exits non-zero if any error is found.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .config import DATA

DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")

ENUMS = {
    "claim_type": {"capability", "limitation", "trajectory", "incident"},
    "domain": {"general", "health", "education", "defence_security", "cyber",
               "child_safety", "deepfakes_misinfo", "creative_copyright", "work",
               "public_services", "science", "finance", "other"},
    "evidence_basis": {"cited_source", "vague_attribution", "personal_experience", "none"},
    "vintage_status": {"current", "outdated", "never_accurate", "dated_event",
                       "forecast", "unclear"},
    "vintage_confidence": {"high", "medium", "low"},
}
NULLABLE_ENUMS = {
    "source_type": {"government", "parliamentary", "academic", "company", "news",
                    "ngo_thinktank", "international_body", "legal",
                    "expert_statement", "book", "other"},
    "source_identified_by": {"named_in_speech", "inferred_by_coder"},
    "source_date_basis": {"stated_in_speech", "web_verified", "coder_recall", "unknown"},
}
RELEVANCE = {"substantive", "passing", "false_positive"}
CLAIM_FIELDS = [
    "quote", "claim", "claim_type", "domain", "named_system", "evidence_basis",
    "source_name", "source_org", "source_type", "source_identified_by",
    "source_date", "source_date_basis", "source_url", "source_notes",
    "vintage_status", "vintage_date", "vintage_rationale", "vintage_confidence",
    "capability_since",
]


def load_speeches() -> dict[str, dict]:
    out = {}
    with open(DATA / "pilot" / "sample.jsonl", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            out[r["speech_id"]] = r
    return out


def check_claim(c: dict, speech: dict) -> list[str]:
    errs = []
    for f in CLAIM_FIELDS:
        if f not in c:
            errs.append(f"missing field {f}")
    if errs:
        return errs
    quote = c["quote"] or ""
    if quote not in speech["text"]:
        errs.append(f"quote is not an exact substring: {quote[:70]!r}")
    if len(quote.split()) > 60:
        errs.append(f"quote longer than 60 words ({len(quote.split())})")
    for f, allowed in ENUMS.items():
        if c[f] not in allowed:
            errs.append(f"{f}={c[f]!r} not allowed")
    for f, allowed in NULLABLE_ENUMS.items():
        if c[f] is not None and c[f] not in allowed:
            errs.append(f"{f}={c[f]!r} not allowed")
    if c["source_date"] is not None and not DATE_RE.match(str(c["source_date"])):
        errs.append(f"source_date={c['source_date']!r} malformed")
    for f in ("vintage_date", "capability_since"):
        if c[f] is not None and not MONTH_RE.match(str(c[f])):
            errs.append(f"{f}={c[f]!r} malformed")
    if c["evidence_basis"] == "cited_source" and not c["source_name"]:
        errs.append("cited_source without source_name")
    if c["vintage_status"] in ("outdated", "dated_event") and not c["vintage_date"]:
        errs.append(f"vintage_status={c['vintage_status']} needs vintage_date")
    if c["vintage_status"] in ("current", "forecast", "never_accurate", "unclear") and c["vintage_date"]:
        errs.append(f"vintage_status={c['vintage_status']} must not set vintage_date")
    if c["source_url"] is not None and not str(c["source_url"]).startswith("http"):
        errs.append("source_url is not a URL")
    return errs


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
        if row.get("ai_relevance") not in RELEVANCE:
            errors.append(f"{sid}: ai_relevance={row.get('ai_relevance')!r} not allowed")
        for i, c in enumerate(row.get("claims") or [], 1):
            n_claims += 1
            for e in check_claim(c, speeches[sid]):
                errors.append(f"{sid} claim {i}: {e}")
        for nm in row.get("near_misses") or []:
            if nm.get("quote") and nm["quote"] not in speeches[sid]["text"]:
                errors.append(f"{sid}: near-miss quote is not an exact substring")

    batch_file = DATA / "pilot" / "batches" / path.name
    if batch_file.exists():
        expected = {json.loads(l)["speech_id"] for l in batch_file.read_text().splitlines() if l.strip()}
        for sid in sorted(expected - seen):
            errors.append(f"{path.name}: speech not coded: {sid}")
        for sid in sorted(seen - expected):
            errors.append(f"{path.name}: speech not in this batch: {sid}")
    return len(seen), n_claims, errors


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    speeches = load_speeches()
    bad = 0
    for arg in argv:
        n, n_claims, errors = validate_file(Path(arg), speeches)
        print(f"{arg}: {n} speeches, {n_claims} claims, {len(errors)} errors")
        for e in errors:
            print("  -", e)
        bad += len(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
