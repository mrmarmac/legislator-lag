"""Build the human review packets and the review page.

    python -m legislag.review [--seed N]

Three packets, all drawn from the full run:

    spot   a stratified random sample of claims for a human spot-check
    adj    the double-coded speeches where the two codings disagree
    tail   named sources over a year old, plus outdated and never-accurate claims

The packets carry the coders' labels and the speech text. They carry no
proposed rulings: every judgement is left to the reviewer.

Outputs
    outputs/full_review.json    the packets
    site/review.html            the review page, with the packets inlined

The page stores each verdict in the artifact's own database, one document
per item under `verdicts/`, keyed by the item's `id`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict

from .build import build, match_claims
from .config import ROOT
from .runs import RUNS, load_labels, load_speeches
from .schema import CLAIM_TYPES, EVIDENCE_BASES, RELEVANCE, VINTAGE_STATUSES
from .site import MARK

SEED = 20261115
SPOT_N = 40
SPOT_MIN_PER_STRATUM = 2
TAIL_DAYS = 365

# Fields a reviewer sees for one coded claim.
SHOWN = [
    "quote", "supporting_quote", "claim", "claim_type", "domain", "named_system",
    "evidence_basis", "source_name", "source_org", "source_type", "source_identified_by",
    "source_date", "source_date_basis", "source_url", "source_notes", "other_sources",
    "event_public_date", "event_occurred_date", "incident_loosely_described",
    "incident_accuracy_note", "vintage_status", "vintage_date", "vintage_rationale",
    "vintage_confidence", "capability_since",
]
# Fields where a split between two coders changes a reported number.
ADJ_FIELDS = ["claim_type", "evidence_basis", "vintage_status", "source_identified_by",
              "source_date", "event_public_date", "incident_loosely_described"]


def item_id(prefix: str, ref: str) -> str:
    return f"{prefix}_{hashlib.sha1(ref.encode()).hexdigest()[:10]}"


def slim(claim: dict) -> dict:
    return {k: claim.get(k) for k in SHOWN}


def speech_meta(sp: dict) -> dict:
    return {k: sp[k] for k in ("speech_id", "country", "chamber_label", "date", "speaker",
                               "heading", "subheading", "url", "word_count")}


# ---------- spot-check sample ----------

def allocate(sizes: dict, n: int, floor: int) -> dict:
    """Proportional allocation with a minimum per stratum, summing to n."""
    total = sum(sizes.values())
    exact = {k: n * v / total for k, v in sizes.items()}
    alloc = {k: min(sizes[k], max(floor, int(exact[k]))) for k in sizes}
    while sum(alloc.values()) != n:
        short = sum(alloc.values()) < n
        # Add to the stratum furthest below its share, or trim the one furthest above.
        pool = [k for k in sizes if (alloc[k] < sizes[k] if short else alloc[k] > floor)]
        k = (max if short else min)(pool, key=lambda k: (exact[k] - alloc[k], str(k)))
        alloc[k] += 1 if short else -1
    return alloc


def spot_sample(claims: list[dict], seed: int) -> tuple[list[dict], list[dict]]:
    """Stratify by country and evidence basis; spread each draw across currency."""
    rng = random.Random(seed)
    strata = defaultdict(list)
    for c in sorted(claims, key=lambda c: c["claim_id"]):
        strata[(c["country"], c["evidence_basis"])].append(c)
    alloc = allocate({k: len(v) for k, v in strata.items()}, SPOT_N, SPOT_MIN_PER_STRATUM)
    picked, table = [], []
    for key in sorted(strata):
        pool = strata[key]
        rng.shuffle(pool)
        pool.sort(key=lambda c: c["vintage_status"])   # stable: random within status
        k = alloc[key]
        step = len(pool) / k
        start = rng.random() * step
        chosen = [pool[int(start + i * step)] for i in range(k)]
        for c in chosen:
            picked.append((c, len(pool) / k))
        table.append({"country": key[0], "evidence_basis": key[1],
                      "claims": len(pool), "sampled": k, "weight": round(len(pool) / k, 2)})
    rng.shuffle(picked)
    return picked, table


# ---------- packets ----------

def packets(seed: int = SEED) -> dict:
    run = RUNS["full"]
    speeches = load_speeches(run)
    main = load_labels(run, run.main)
    second = load_labels(run, run.second)
    claims, _, summary = build("full")
    kept = defaultdict(list)                 # main coding after adjudication drops
    for c in claims:
        kept[c["speech_id"]].append(c)

    texts: dict[str, str] = {}

    def use_text(sid: str) -> None:
        texts[sid] = speeches[sid]["text"]

    # 1. Spot-check
    spot = []
    picked, strata = spot_sample(claims, seed)
    for c, weight in picked:
        sid = c["speech_id"]
        use_text(sid)
        spot.append({
            "id": item_id("s", c["claim_id"]), "kind": "spot", "ref": c["claim_id"],
            "speech": speech_meta(speeches[sid]), "claim": slim(c),
            "cited_lag_months": c["cited_lag_months"],
            "incident_lag_months": c["incident_lag_months"],
            "stratum": [c["country"], c["evidence_basis"]], "weight": round(weight, 2),
            "other_claims": [{"ref": o["claim_id"], "quote": o["quote"], "claim": o["claim"]}
                             for o in kept[sid] if o["claim_id"] != c["claim_id"]],
            "near_misses": main[sid].get("near_misses") or [],
            "coder_notes": main[sid].get("coder_notes") or "",
        })

    # 2. Adjudication. Coders are shown as A and B in an order shuffled per
    # speech, so the reviewer cannot tell which coding is the published one.
    rng = random.Random(seed + 1)
    adj, agreed, splits = [], 0, Counter()
    for sid in sorted(set(main) & set(second)):
        a = [{**slim(c), "key": "main#" + c["claim_id"].rsplit("#", 1)[1]} for c in kept[sid]]
        b = [{**slim(c), "key": f"second#{i}"} for i, c in enumerate(second[sid]["claims"], 1)]
        flip = rng.random() < 0.5
        tag = {"main": "B" if flip else "A", "second": "A" if flip else "B"}
        pairs, used = [], set()
        for x, y in match_claims(a, b):
            used |= {x["key"], y["key"]}
            diff = [f for f in ADJ_FIELDS if x.get(f) != y.get(f)]
            for f in diff:
                splits[f] += 1
            pairs.append({tag["main"]: x, tag["second"]: y, "diff": diff})
        solo = [{"coder": tag["main"], "claim": c} for c in a if c["key"] not in used] + \
               [{"coder": tag["second"], "claim": c} for c in b if c["key"] not in used]
        splits["found_by_one_coder"] += len(solo)
        rel = {tag["main"]: main[sid]["ai_relevance"], tag["second"]: second[sid]["ai_relevance"]}
        if rel["A"] != rel["B"]:
            splits["ai_relevance"] += 1
        if not (solo or rel["A"] != rel["B"] or any(p["diff"] for p in pairs)):
            agreed += 1
            continue
        use_text(sid)
        adj.append({
            "id": item_id("a", sid), "kind": "adj", "ref": sid,
            "speech": speech_meta(speeches[sid]), "relevance": rel,
            "pairs": [p for p in pairs if p["diff"]],
            "agreed_pairs": sum(1 for p in pairs if not p["diff"]),
            "solo": sorted(solo, key=lambda s: s["coder"]),
            "notes": {tag["main"]: main[sid].get("coder_notes") or "",
                      tag["second"]: second[sid].get("coder_notes") or ""},
            "near_misses": {tag["main"]: main[sid].get("near_misses") or [],
                            tag["second"]: second[sid].get("near_misses") or []},
        })

    # 3. The tail
    tail = []
    for c in claims:
        old = (c["cited_lag_days"] or 0) > TAIL_DAYS
        flagged = c["vintage_status"] in ("outdated", "never_accurate")
        if not (old or flagged):
            continue
        sid = c["speech_id"]
        use_text(sid)
        tail.append({
            "id": item_id("t", c["claim_id"]), "kind": "tail", "ref": c["claim_id"],
            "speech": speech_meta(speeches[sid]), "claim": slim(c),
            "old_source": old, "flagged": flagged,
            "cited_lag_months": c["cited_lag_months"],
            "implied_lag_months": c["implied_lag_months"] if flagged else None,
            "coder_notes": main[sid].get("coder_notes") or "",
        })
    tail.sort(key=lambda t: (not t["flagged"], -(t["cited_lag_months"] or 0)))

    return {
        "generated": summary["generated"], "seed": seed, "codebook": summary["codebook"],
        "claims_total": len(claims),
        "enums": {"claim_type": CLAIM_TYPES, "evidence_basis": EVIDENCE_BASES,
                  "vintage_status": VINTAGE_STATUSES, "ai_relevance": RELEVANCE},
        "spot": spot, "spot_strata": strata,
        "adj": adj, "adj_speeches": len(set(main) & set(second)), "adj_agreed": agreed,
        "adj_splits": dict(splits),
        "tail": tail,
        "texts": texts,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()
    data = packets(args.seed)
    payload = json.dumps(data, ensure_ascii=False)
    (ROOT / "outputs" / "full_review.json").write_text(payload + "\n", encoding="utf-8")
    template = (ROOT / "site" / "template_review.html").read_text(encoding="utf-8")
    if MARK not in template:
        print("template has no data marker")
        return 1
    page = template.replace(MARK, payload.replace("</", "<\\/"))
    (ROOT / "site" / "review.html").write_text(page, encoding="utf-8")
    print(f"spot-check {len(data['spot'])} claims; adjudication {len(data['adj'])} of "
          f"{data['adj_speeches']} speeches; tail {len(data['tail'])} claims; "
          f"site/review.html {len(page) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
