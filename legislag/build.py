"""Turn coder labels into analysis tables.

    python -m legislag.build [--run pilot|full]

Inputs (see legislag/runs.py for each run's paths)
    speeches, coder labels, the independent second coding, and an optional
    adjudication.jsonl of reviewer overrides beside the labels directory

Outputs
    outputs/<run>_claims.csv        one row per claim, with derived lags
    outputs/<run>_speeches.csv      one row per coded speech
    outputs/<run>_summary.json      headline numbers and reliability
    outputs/<run>_site_data.json    compact payload for the browser page

Adjudication lines look like
    {"claim_id": "...#2", "set": {"vintage_status": "current"}, "reason": "..."}
    {"claim_id": "...#3", "drop": true, "reason": "..."}
Coder files are never edited; every reviewer change is recorded there.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import statistics
import sys
from collections import Counter, defaultdict

from .config import AI_PATTERN, DATA, ROOT
from .runs import RUNS, Run, ai_mentions, load_labels, load_speeches, read_jsonl

OUT = ROOT / "outputs"
WORD = re.compile(r"[a-z0-9]+")


# ---------- dates and lags ----------

def resolve(partial: str | None, debate: dt.date) -> tuple[dt.date | None, str | None]:
    """Turn YYYY, YYYY-MM or YYYY-MM-DD into one date, plus its precision.

    A partial date is placed at the middle of the period it names. If the
    debate falls inside that period, the middle of the part before the debate
    is used, so a source can never be dated after the speech that cites it.
    """
    if not partial:
        return None, None
    parts = [int(p) for p in str(partial).split("-")]
    if len(parts) == 3:
        return min(dt.date(*parts), debate), "day"
    if len(parts) == 2:
        start = dt.date(parts[0], parts[1], 1)
        nxt = dt.date(parts[0] + (parts[1] == 12), parts[1] % 12 + 1, 1)
        precision = "month"
    else:
        start, nxt, precision = dt.date(parts[0], 1, 1), dt.date(parts[0] + 1, 1, 1), "year"
    end = min(nxt - dt.timedelta(days=1), debate)
    if end < start:
        return debate, precision
    return start + (end - start) / 2, precision


def months(days: int | None) -> float | None:
    return None if days is None else round(days / 30.4375, 1)


def derive(claim: dict, debate: dt.date) -> dict:
    src, src_prec = resolve(claim.get("source_date"), debate)
    # Cited lag counts only sources the speaker named. A source the coder
    # tracked down for an unsourced claim is kept as a reference, not as
    # evidence the speaker relied on.
    named = claim.get("source_identified_by") == "named_in_speech"
    cited = (debate - src).days if src and named else None

    status = claim.get("vintage_status")
    # Incidents: v0.2 dates them by when they became public. v0.1 labels have
    # only the occurrence date, stored in vintage_date.
    event_raw = claim.get("event_public_date") or (
        claim.get("vintage_date") if status == "dated_event" else None)
    event, _ = resolve(event_raw, debate) if status == "dated_event" else (None, None)
    incident = (debate - event).days if event else None

    vin = None
    implied = None
    if status == "outdated":
        vin, _ = resolve(claim.get("vintage_date"), debate)
        implied = (debate - vin).days if vin else None
    elif status == "current":
        implied = 0

    since, _ = resolve(claim.get("capability_since"), debate)
    return {
        "source_date_resolved": src.isoformat() if src else None,
        "source_date_precision": src_prec,
        "cited_lag_days": cited,
        "cited_lag_months": months(cited),
        "event_date_used": event_raw if status == "dated_event" else None,
        "event_date_resolved": event.isoformat() if event else None,
        "incident_lag_days": incident,
        "incident_lag_months": months(incident),
        "vintage_date_resolved": vin.isoformat() if vin else None,
        "implied_lag_days": implied,
        "implied_lag_months": months(implied),
        "capability_age_months": months((debate - since).days) if since else None,
        "other_sources_json": json.dumps(claim.get("other_sources") or [], ensure_ascii=False)
        if claim.get("other_sources") else None,
    }


# ---------- reliability ----------

def tokens(s: str) -> set[str]:
    return set(WORD.findall((s or "").lower()))


def overlap(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / min(len(ta), len(tb)) if ta and tb else 0.0


def match_claims(a: list[dict], b: list[dict], threshold: float = 0.5):
    """Greedy one-to-one matching of two coders' claims by quote overlap."""
    pairs = sorted(((overlap(x["quote"], y["quote"]), i, j)
                    for i, x in enumerate(a) for j, y in enumerate(b)), reverse=True)
    used_a, used_b, out = set(), set(), []
    for score, i, j in pairs:
        if score < threshold:
            break
        if i in used_a or j in used_b:
            continue
        used_a.add(i), used_b.add(j)
        out.append((a[i], b[j]))
    return out


def kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    n = len(pairs)
    po = sum(x == y for x, y in pairs) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return None if pe == 1 else round((po - pe) / (1 - pe), 2)


def reliability(main: dict, second: dict) -> dict:
    shared = sorted(set(main) & set(second))
    if not shared:
        return {"speeches": 0}
    has = [(bool(main[s]["claims"]), bool(second[s]["claims"])) for s in shared]
    rel = [(main[s]["ai_relevance"], second[s]["ai_relevance"]) for s in shared]
    n_a = sum(len(main[s]["claims"]) for s in shared)
    n_b = sum(len(second[s]["claims"]) for s in shared)
    matched = [p for s in shared for p in match_claims(main[s]["claims"], second[s]["claims"])]
    fields = {}
    for f in ("claim_type", "evidence_basis", "vintage_status"):
        pairs = [(x[f], y[f]) for x, y in matched]
        fields[f] = {
            "agreement": round(sum(x == y for x, y in pairs) / len(pairs), 2) if pairs else None,
            "kappa": kappa(pairs),
        }
    return {
        "speeches": len(shared),
        "any_claim_agreement": round(sum(x == y for x, y in has) / len(has), 2),
        "any_claim_kappa": kappa(has),
        "relevance_agreement": round(sum(x == y for x, y in rel) / len(rel), 2),
        "claims_first_coder": n_a,
        "claims_second_coder": n_b,
        "claims_matched": len(matched),
        # Share of all claims found by either coder that both coders found.
        "claim_overlap": round(len(matched) / (n_a + n_b - len(matched)), 2) if n_a + n_b else None,
        "matched_fields": fields,
    }


# ---------- summary ----------

def quantiles(values: list[float]) -> dict | None:
    if not values:
        return None
    v = sorted(values)
    q = statistics.quantiles(v, n=4, method="inclusive") if len(v) > 1 else [v[0]] * 3
    return {"n": len(v), "median": round(q[1], 1), "p25": round(q[0], 1),
            "p75": round(q[2], 1), "min": v[0], "max": v[-1]}


def summarise(claims: list[dict], speeches: list[dict]) -> dict:
    def block(cs, sp):
        dated = [c for c in cs if c["cited_lag_months"] is not None]
        implied = [c for c in cs if c["vintage_status"] in ("current", "outdated")]
        outdated = [c for c in implied if c["vintage_status"] == "outdated"]
        return {
            "speeches": len(sp),
            "speeches_with_claims": sum(1 for s in sp if s["n_claims"]),
            "relevance": dict(Counter(s["ai_relevance"] for s in sp)),
            "claims": len(cs),
            "claim_type": dict(Counter(c["claim_type"] for c in cs)),
            "evidence_basis": dict(Counter(c["evidence_basis"] for c in cs)),
            "vintage_status": dict(Counter(c["vintage_status"] for c in cs)),
            "claims_with_dated_source": len(dated),
            "cited_lag_months": quantiles([c["cited_lag_months"] for c in dated]),
            "assessable_for_vintage": len(implied),
            "outdated": len(outdated),
            "outdated_lag_months": quantiles([c["implied_lag_months"] for c in outdated]),
            "incident_lag_months": quantiles([c["incident_lag_months"] for c in cs
                                              if c["incident_lag_months"] is not None]),
            "capability_age_months": quantiles([c["capability_age_months"] for c in cs
                                                if c["capability_age_months"] is not None]),
        }

    out = {"all": block(claims, speeches)}
    for country in ("UK", "AU"):
        out[country] = block([c for c in claims if c["country"] == country],
                             [s for s in speeches if s["country"] == country])
    return out


def band(n: int) -> str:
    return "1" if n == 1 else "2" if n == 2 else "3-5" if n <= 5 else "6-10" if n <= 10 else "11+"


BANDS = ["1", "2", "3-5", "6-10", "11+"]


def claim_yield(speeches: list[dict]) -> dict:
    """Where the claims are: yield by how often a speech mentions AI."""
    def tally(rows):
        return {"speeches": len(rows),
                "with_claims": sum(1 for s in rows if s["n_claims"]),
                "claims": sum(s["n_claims"] for s in rows)}
    return {
        "by_mentions": [{"band": b, **tally([s for s in speeches if band(s["ai_mentions"]) == b])}
                        for b in BANDS],
        "by_heading": {"ai_in_heading": tally([s for s in speeches if s["ai_in_heading"]]),
                       "other": tally([s for s in speeches if not s["ai_in_heading"]])},
    }


# ---------- main ----------

CLAIM_COLUMNS = [
    "claim_id", "country", "chamber_label", "date", "speaker", "heading", "subheading",
    "url", "claim", "quote", "claim_type", "domain", "named_system", "evidence_basis",
    "source_name", "source_org", "source_type", "source_identified_by", "source_date",
    "source_date_basis", "source_date_resolved", "source_date_precision",
    "cited_lag_days", "cited_lag_months", "source_url", "source_notes", "other_sources_json",
    "event_public_date", "event_occurred_date", "event_date_used", "event_date_resolved",
    "incident_lag_days", "incident_lag_months", "incident_loosely_described",
    "incident_accuracy_note",
    "vintage_status", "vintage_date", "vintage_date_resolved", "implied_lag_days",
    "implied_lag_months", "vintage_rationale", "vintage_confidence",
    "capability_since", "capability_age_months", "supporting_quote",
    "adjudicated", "adjudication_reason", "coder", "speech_id", "weight",
]
SPEECH_COLUMNS = [
    "speech_id", "country", "chamber_label", "date", "speaker", "heading", "subheading",
    "url", "word_count", "ai_mentions", "ai_in_heading", "ai_relevance", "n_claims",
    "n_near_misses", "coder_notes", "coder", "weight",
]


def write_csv(path, rows, columns):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def build(run_name: str = "pilot") -> tuple[list[dict], list[dict], dict]:
    run: Run = RUNS[run_name]
    sample = load_speeches(run)
    main = load_labels(run, run.main)
    second = load_labels(run, run.second)
    overrides = {a["claim_id"]: a for a in read_jsonl(run.labels_dir.parent / "adjudication.jsonl")}
    versions = sorted({row.get("codebook", "v0.1") for row in main.values()})

    claims, speeches, near_misses = [], [], []
    dropped = 0
    for sid in sorted(main, key=lambda s: (sample[s]["date"], s)):
        sp, row = sample[sid], main[sid]
        meta = {**{k: sp[k] for k in ("country", "chamber_label", "date", "speaker",
                                       "heading", "subheading", "url")},
                "weight": sp.get("weight", 1)}
        debate = dt.date.fromisoformat(sp["date"])
        kept = 0
        for i, c in enumerate(row.get("claims") or [], 1):
            cid = f"{sid}#{i}"
            ov = overrides.get(cid)
            if ov and ov.get("drop"):
                dropped += 1
                continue
            c = dict(c)
            if ov:
                c.update(ov.get("set") or {})
            kept += 1
            claims.append({
                **meta, **c, **derive(c, debate),
                "claim_id": cid, "speech_id": sid, "coder": row["coder"],
                "adjudicated": bool(ov), "adjudication_reason": ov.get("reason") if ov else None,
            })
        for nm in row.get("near_misses") or []:
            near_misses.append({"speech_id": sid, **nm})
        speeches.append({
            **meta, "speech_id": sid, "word_count": sp["word_count"],
            "ai_relevance": row["ai_relevance"], "n_claims": kept,
            "n_near_misses": len(row.get("near_misses") or []),
            "coder_notes": row.get("coder_notes") or "", "coder": row["coder"],
            "ai_mentions": ai_mentions(sp),
            "ai_in_heading": bool(AI_PATTERN.search(sp["heading"] + " " + sp["subheading"])),
        })

    corpus = json.loads((DATA / "corpus_stats.json").read_text())
    summary = {
        "generated": dt.date.today().isoformat(),
        "run": run.name,
        "run_label": run.label,
        "codebook": " and ".join(versions) if versions else None,
        "corpus_speeches": sum(v["ai_speeches"] for v in corpus.values()),
        "eligible_speeches": len(sample) if run.name == "pilot" else sum(
            1 for s in sample.values() if ai_mentions(s) >= 2),
        "coded_speeches": len(speeches),
        "adjudication": {"overrides": len(overrides), "claims_dropped": dropped},
        "near_misses": len(near_misses),
        "summary": summarise(claims, speeches),
        "yield": claim_yield(speeches),
        "reliability": reliability(main, second),
        "corpus": corpus,
    }
    return claims, speeches, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", choices=sorted(RUNS), default="pilot")
    args = ap.parse_args()
    claims, speeches, summary = build(args.run)
    OUT.mkdir(exist_ok=True)
    write_csv(OUT / f"{args.run}_claims.csv", claims, CLAIM_COLUMNS)
    write_csv(OUT / f"{args.run}_speeches.csv", speeches, SPEECH_COLUMNS)
    (OUT / f"{args.run}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    site = {"summary": summary,
            "claims": [{k: c.get(k) for k in CLAIM_COLUMNS if k not in ("weight", "coder")}
                       for c in claims]}
    (OUT / f"{args.run}_site_data.json").write_text(json.dumps(site, ensure_ascii=False) + "\n")
    s = summary["summary"]["all"]
    print(f"{args.run}: {summary['coded_speeches']} speeches, {s['claims']} claims, "
          f"{s['claims_with_dated_source']} with a dated named source, {s['outdated']} outdated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
