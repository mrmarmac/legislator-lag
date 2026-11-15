"""Draw the paper's figures from the full-run outputs.

    python -m legislag.figures

Reads outputs/full_claims.csv and data/full/review/summary.json. Writes
standalone SVG files and their captions to outputs/figures/:

    fig1_source_age.svg        every dated named source, by age and country
    fig2_evidence_offered.svg  what claims rest on, by country
    fig3_human_review.svg      the reviewer's spot-check verdicts, by question
    captions.md                figure numbers and captions

The figures carry no title; the caption does that job in the paper. To get
PNG copies, run `node legislag/figures_png.js` (needs Playwright).

Colour. Figure 1 uses one hue per country. Figure 2 uses one hue from light
to dark for the three kinds of evidence, and grey for none. Figure 3 uses
blue for agreement, orange for disagreement and grey for unsure. Every
segment is also labelled, so no figure depends on colour alone.
"""
from __future__ import annotations

import csv
import html
import json
import math
import statistics
import sys
from collections import Counter

from .config import DATA, ROOT

OUT = ROOT / "outputs" / "figures"
INK, INK2, MUTED, RULE = "#141a22", "#48525f", "#6f7986", "#dde2e8"
UK, AU = "#2a78d6", "#eb6834"                      # checked for colour-blind separation
GREY_DARK, GREY = "#6b7480", "#aab2bd"
TEAL = ["#a5dbd2", "#3aa697", "#0f5e55"]            # light to dark
FONT = "Inter, 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
W = 900


def text(x, y, s, size=13, fill=INK2, anchor="start", weight=400):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{html.escape(str(s))}</text>')


def svg(h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'font-family="{FONT}" role="img" aria-label="{html.escape(label)}">'
            f'<rect width="{W}" height="{h}" fill="#ffffff"/>{body}</svg>\n')


def legend(items, x, y):
    out = ""
    for label, colour in items:
        out += f'<rect x="{x}" y="{y - 11}" width="12" height="12" rx="2" fill="{colour}"/>' + text(x + 18, y, label)
        x += 44 + len(label) * 7.4
    return out


def source_age(claims):
    """Figure 1: one dot per dated named source, on a log time axis."""
    h, left, right = 340, 96, 30
    def xs(days):
        return left + (W - left - right) * math.log10(days + 1) / math.log10(6000)
    body = ""
    ticks = [(0, "same day"), (7, "1 week"), (30, "1 month"), (90, "3 months"),
             (365, "1 year"), (730, "2 years"), (3650, "10 years")]
    for d, lab in ticks:
        body += f'<line x1="{xs(d):.1f}" x2="{xs(d):.1f}" y1="24" y2="{h - 62}" stroke="{RULE}"/>'
        body += text(xs(d), h - 42, lab, 12, MUTED, "middle")
    body += text((left + W - right) / 2, h - 14, "Age of the source on the day it was cited (log scale)", 12, INK2, "middle")
    medians = {}
    for lane, (code, colour, name) in enumerate([("UK", UK, "UK"), ("AU", AU, "Australia")]):
        cy = 88 + lane * 118
        days = sorted(int(c["cited_lag_days"]) for c in claims if c["cited_lag_days"] and c["country"] == code)
        placed = []
        for d in days:                      # stack dots that would overlap, alternating above and below
            x, k = xs(d), 0
            while True:
                off = (k + 1) // 2 * 9.4 * (1 if k % 2 else -1)
                if all((x - px) ** 2 + (off - po) ** 2 >= 9.2 ** 2 for px, po in placed):
                    break
                k += 1
            placed.append((x, off))
            body += f'<circle cx="{x:.1f}" cy="{cy + off:.1f}" r="4.2" fill="{colour}" stroke="#ffffff" stroke-width="1"/>'
        med = statistics.median(days)
        medians[code] = (med, len(days))
        body += f'<line x1="{xs(med):.1f}" x2="{xs(med):.1f}" y1="{cy - 50}" y2="{cy + 50}" stroke="{INK}" stroke-width="2"/>'
        body += text(xs(med) + 6, cy - 42, f"median {med:g} days", 12, INK, "start", 600)
        body += text(left - 14, cy - 2, name, 14, INK, "end", 600) + text(left - 14, cy + 15, f"{len(days)} sources", 12, MUTED, "end")
    oldest = max((c for c in claims if c["cited_lag_days"]), key=lambda c: int(c["cited_lag_days"]))
    lane = 0 if oldest["country"] == "UK" else 1
    body += text(xs(int(oldest["cited_lag_days"])) - 9, 88 + lane * 118 - 12,
                 f'{oldest["source_date"][:4]} source', 12, INK2, "end")
    cap = (f"Age of every dated source that a speaker named, on the day it was cited. Each dot is one source "
           f"(UK n = {medians['UK'][1]}, Australia n = {medians['AU'][1]}). The horizontal axis is logarithmic. "
           f"Vertical bars mark medians: {medians['UK'][0]:g} days for the UK and {medians['AU'][0]:g} days for Australia.")
    return svg(h, body, "Dot plot of source age by country"), cap


def evidence_offered(claims):
    """Figure 2: share of claims by evidence offered, one bar per country."""
    h, left = 220, 110
    span = W - left - 30
    order = [("none", "No evidence", GREY_DARK, "#ffffff"), ("vague_attribution", "Vague attribution", TEAL[0], INK),
             ("personal_experience", "Personal experience", TEAL[1], INK), ("cited_source", "Named source", TEAL[2], "#ffffff")]
    body, parts = "", []
    for i, (code, name) in enumerate([("UK", "UK"), ("AU", "Australia")]):
        y = 24 + i * 68
        count = Counter(c["evidence_basis"] for c in claims if c["country"] == code)
        total = sum(count.values())
        body += text(left - 14, y + 22, name, 14, INK, "end", 600) + text(left - 14, y + 39, f"{total} claims", 12, MUTED, "end")
        x = left
        for key, _, colour, ink in order:
            w = span * count[key] / total
            body += f'<rect x="{x + 1:.1f}" y="{y}" width="{w - 2:.1f}" height="46" rx="3" fill="{colour}"/>'
            pct = round(100 * count[key] / total)
            body += text(x + w / 2, y + 28 if w > 40 else y - 6, f"{pct}%", 14 if w > 40 else 12,
                         ink if w > 40 else INK2, "middle", 600)
            x += w
        parts.append(f"{name}: {round(100 * count['none'] / total)}% none, "
                     f"{round(100 * count['cited_source'] / total)}% named source (n = {total})")
    body += legend([(lab, colour) for _, lab, colour, _ in order], left, 186)
    cap = ("What each claim about AI rests on, as a share of each country's claims. \"Vague attribution\" means a "
           "source was gestured at but not identified, such as \"experts say\". " + ". ".join(parts) + ".")
    return svg(h, body, "Stacked bars of evidence offered by country"), cap


def human_review(summary):
    """Figure 3: the reviewer's spot-check verdicts on each question."""
    s = Counter(summary["spot"])
    rows = [
        ("Is it a claim?", s["is_claim_yes"], s["is_claim_no"], s["is_claim_unsure"]),
        ("Kind of claim", s["claim_type_agree"], s["claim_type_disagree"], s["claim_type_unsure"]),
        ("Evidence offered", s["evidence_basis_agree"], s["evidence_basis_disagree"], s["evidence_basis_unsure"]),
        ("Source and date", s["source_right"], s["source_wrong_source"] + s["source_wrong_date"], s["source_cannot_verify"]),
        ("Date incident became public", s["event_date_right"], s["event_date_wrong"], s["event_date_cannot_verify"]),
        ("Currency on the day", s["vintage_status_agree"], s["vintage_status_disagree"],
         s["vintage_status_unsure"] + s["vintage_status_withdrawn"]),
    ]
    h, left = 300, 220
    span = W - left - 64
    body = ""
    for i, (lab, agree, disagree, unsure) in enumerate(rows):
        y, total, x = 18 + i * 40, agree + disagree + unsure, left
        body += text(left - 12, y + 18, lab, 13, INK, "end")
        for n, colour, ink in ((agree, UK, "#ffffff"), (disagree, AU, INK), (unsure, GREY, INK)):
            w = span * n / total
            if n:
                body += f'<rect x="{x + 1:.1f}" y="{y}" width="{w - 2:.1f}" height="26" rx="3" fill="{colour}"/>'
                if w > 20:
                    body += text(x + w / 2, y + 18, n, 13, ink, "middle", 600)
            x += w
        body += text(W - 56, y + 18, f"of {total}", 12, MUTED)
    body += legend([("Reviewer agreed", UK), ("Disagreed or ruled out", AU), ("Unsure or could not verify", GREY)], left, 276)
    cap = (f"One human reviewer's verdicts on a stratified random sample of {s['sampled']} coded claims. Bars show "
           "counts as a share of each row; rows differ in size because some questions apply only to claims with a "
           "source or to incidents. \"Is it a claim?\" asks whether the coder should have coded the remark at all. "
           "One currency ruling the reviewer later withdrew is counted as unsure.")
    return svg(h, body, "Stacked bars of human review verdicts by question"), cap


def main() -> int:
    claims = list(csv.DictReader(open(ROOT / "outputs" / "full_claims.csv", encoding="utf-8")))
    summary = json.loads((DATA / "full" / "review" / "summary.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    figures = [("fig1_source_age", source_age(claims)), ("fig2_evidence_offered", evidence_offered(claims)),
               ("fig3_human_review", human_review(summary))]
    captions = ["# Figure captions\n"]
    for n, (stem, (drawing, caption)) in enumerate(figures, 1):
        (OUT / f"{stem}.svg").write_text(drawing, encoding="utf-8")
        captions.append(f"**Figure {n}.** {caption}\n\nFiles: `{stem}.svg`, `{stem}.png`\n")
        print(f"wrote outputs/figures/{stem}.svg")
    (OUT / "captions.md").write_text("\n".join(captions), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
