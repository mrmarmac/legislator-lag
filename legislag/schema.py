"""Field lists and allowed values for coder output.

One place for what CODEBOOK.md says a label must look like. The validator and
the API coder both read from here, so they cannot drift apart.

Values are a superset across codebook versions. Fields added in v0.2 are
required only on rows that declare `"codebook": "v0.2"`.
"""
from __future__ import annotations

import re

CODEBOOK_VERSION = "v0.2"

CLAIM_TYPES = ["capability", "limitation", "trajectory", "incident", "adoption",
               "economic", "labour", "resource", "opinion", "other"]
DOMAINS = ["general", "health", "education", "defence_security", "cyber",
           "child_safety", "deepfakes_misinfo", "creative_copyright", "work",
           "public_services", "science", "finance", "energy_infrastructure", "other"]
EVIDENCE_BASES = ["cited_source", "vague_attribution", "personal_experience", "none"]
VINTAGE_STATUSES = ["current", "outdated", "contested", "never_accurate",
                    "dated_event", "forecast", "unclear"]
CONFIDENCES = ["high", "medium", "low"]
SOURCE_TYPES = ["government", "parliamentary", "academic", "company", "news",
                "ngo_thinktank", "international_body", "legal", "expert_statement",
                "book", "other"]
SOURCE_IDENTIFIED_BY = ["named_in_speech", "inferred_by_coder"]
SOURCE_DATE_BASES = ["stated_in_speech", "web_verified", "coder_recall", "unknown"]
RELEVANCE = ["substantive", "passing", "procedural", "false_positive"]

ENUMS = {
    "claim_type": CLAIM_TYPES,
    "domain": DOMAINS,
    "evidence_basis": EVIDENCE_BASES,
    "vintage_status": VINTAGE_STATUSES,
    "vintage_confidence": CONFIDENCES,
}
NULLABLE_ENUMS = {
    "source_type": SOURCE_TYPES,
    "source_identified_by": SOURCE_IDENTIFIED_BY,
    "source_date_basis": SOURCE_DATE_BASES,
}

# Every claim, in every codebook version.
CLAIM_FIELDS = [
    "quote", "claim", "claim_type", "domain", "named_system", "evidence_basis",
    "source_name", "source_org", "source_type", "source_identified_by",
    "source_date", "source_date_basis", "source_url", "source_notes",
    "vintage_status", "vintage_date", "vintage_rationale", "vintage_confidence",
    "capability_since",
]
# Added in v0.2.
CLAIM_FIELDS_V2 = [
    "supporting_quote", "other_sources", "event_public_date", "event_occurred_date",
    "incident_loosely_described", "incident_accuracy_note",
]

DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
MAX_QUOTE_WORDS = 60


def check_claim(c: dict, text: str, v2: bool) -> list[str]:
    """Return every way a claim breaks the codebook's structural rules."""
    required = CLAIM_FIELDS + (CLAIM_FIELDS_V2 if v2 else [])
    errs = [f"missing field {f}" for f in required if f not in c]
    if errs:
        return errs

    for f in ("quote", "supporting_quote") if v2 else ("quote",):
        q = c[f]
        if f == "supporting_quote" and q is None:
            continue
        if not isinstance(q, str) or not q.strip():
            errs.append(f"{f} is empty")
        elif q not in text:
            errs.append(f"{f} is not an exact substring of the speech text: {q[:70]!r}")
        elif len(q.split()) > MAX_QUOTE_WORDS:
            errs.append(f"{f} is longer than {MAX_QUOTE_WORDS} words ({len(q.split())})")

    for f, allowed in ENUMS.items():
        if c[f] not in allowed:
            errs.append(f"{f}={c[f]!r} is not one of {allowed}")
    for f, allowed in NULLABLE_ENUMS.items():
        if c[f] is not None and c[f] not in allowed:
            errs.append(f"{f}={c[f]!r} is not one of {allowed} or null")

    date_fields = ["source_date"] + (["event_public_date", "event_occurred_date"] if v2 else [])
    for f in date_fields:
        if c[f] is not None and not DATE_RE.match(str(c[f])):
            errs.append(f"{f}={c[f]!r} must be YYYY, YYYY-MM or YYYY-MM-DD")
    for f in ("vintage_date", "capability_since"):
        if c[f] is not None and not MONTH_RE.match(str(c[f])):
            errs.append(f"{f}={c[f]!r} must be YYYY-MM")

    if c["evidence_basis"] == "cited_source" and not c["source_name"]:
        errs.append("evidence_basis is cited_source but source_name is null")
    if c["source_url"] is not None and not str(c["source_url"]).startswith("http"):
        errs.append("source_url is not a URL")

    status = c["vintage_status"]
    if status == "outdated" and not c["vintage_date"]:
        errs.append("vintage_status outdated needs vintage_date")
    if v2:
        if status != "outdated" and c["vintage_date"]:
            errs.append(f"vintage_status {status} must not set vintage_date")
        is_incident = c["claim_type"] == "incident"
        if is_incident and status != "dated_event":
            errs.append("incident claims take vintage_status dated_event")
        if status == "dated_event" and not is_incident:
            errs.append("dated_event is for incident claims only")
        if not is_incident and (c["event_public_date"] or c["event_occurred_date"]):
            errs.append("event dates are for incident claims only")
        if not isinstance(c["incident_loosely_described"], bool):
            errs.append("incident_loosely_described must be true or false")
        elif c["incident_loosely_described"] and not c["incident_accuracy_note"]:
            errs.append("incident_loosely_described is true but incident_accuracy_note is null")
        if not isinstance(c["other_sources"], list):
            errs.append("other_sources must be a list")
        if c["capability_since"] and c["claim_type"] != "capability":
            errs.append("capability_since is for capability claims only")
    else:
        if status == "dated_event" and not c["vintage_date"]:
            errs.append("vintage_status dated_event needs vintage_date")
        if status in ("current", "forecast", "never_accurate", "unclear") and c["vintage_date"]:
            errs.append(f"vintage_status {status} must not set vintage_date")
    return errs


def check_row(row: dict, text: str) -> list[str]:
    """Check one speech-level label row. `text` is the speech it codes."""
    errs = []
    v2 = row.get("codebook") == "v0.2"
    if row.get("ai_relevance") not in RELEVANCE:
        errs.append(f"ai_relevance={row.get('ai_relevance')!r} is not one of {RELEVANCE}")
    if not isinstance(row.get("claims"), list):
        return errs + ["claims must be a list"]
    for i, c in enumerate(row["claims"], 1):
        if not isinstance(c, dict):
            errs.append(f"claim {i}: not an object")
            continue
        errs += [f"claim {i}: {e}" for e in check_claim(c, text, v2)]
    for i, nm in enumerate(row.get("near_misses") or [], 1):
        q = nm.get("quote") if isinstance(nm, dict) else None
        if q and q not in text:
            errs.append(f"near_miss {i}: quote is not an exact substring of the speech text")
    return errs


def _nullable(schema: dict) -> dict:
    return {"anyOf": [schema, {"type": "null"}]}


def submit_tool_schema() -> dict:
    """JSON Schema for the tool the API coder calls to hand in one speech."""
    s = {"type": "string"}
    date = {"type": "string", "description": "YYYY, YYYY-MM or YYYY-MM-DD"}
    month = {"type": "string", "description": "YYYY-MM"}
    claim = {
        "type": "object",
        "additionalProperties": False,
        "required": CLAIM_FIELDS + CLAIM_FIELDS_V2,
        "properties": {
            "quote": {"type": "string", "description": "Exact contiguous substring of the speech text, at most 60 words."},
            "supporting_quote": _nullable(s),
            "claim": s,
            "claim_type": {"type": "string", "enum": CLAIM_TYPES},
            "domain": {"type": "string", "enum": DOMAINS},
            "named_system": _nullable(s),
            "evidence_basis": {"type": "string", "enum": EVIDENCE_BASES},
            "source_name": _nullable(s),
            "source_org": _nullable(s),
            "source_type": _nullable({"type": "string", "enum": SOURCE_TYPES}),
            "source_identified_by": _nullable({"type": "string", "enum": SOURCE_IDENTIFIED_BY}),
            "source_date": _nullable(date),
            "source_date_basis": _nullable({"type": "string", "enum": SOURCE_DATE_BASES}),
            "source_url": _nullable(s),
            "source_notes": _nullable(s),
            "other_sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["name", "date", "url"],
                    "properties": {"name": s, "date": _nullable(date), "url": _nullable(s)},
                },
            },
            "event_public_date": _nullable(date),
            "event_occurred_date": _nullable(date),
            "incident_loosely_described": {"type": "boolean"},
            "incident_accuracy_note": _nullable(s),
            "vintage_status": {"type": "string", "enum": VINTAGE_STATUSES},
            "vintage_date": _nullable(month),
            "vintage_rationale": s,
            "vintage_confidence": {"type": "string", "enum": CONFIDENCES},
            "capability_since": _nullable(month),
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["ai_relevance", "claims", "near_misses", "coder_notes"],
        "properties": {
            "ai_relevance": {"type": "string", "enum": RELEVANCE},
            "claims": {"type": "array", "items": claim},
            "near_misses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["quote", "reason"],
                    "properties": {"quote": s, "reason": s},
                },
            },
            "coder_notes": s,
        },
    }
