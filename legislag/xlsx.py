"""Write the claims workbook.

    python -m legislag.xlsx

Reads the tables produced by legislag.build and writes
outputs/pilot_claims.xlsx with four sheets: Read me, Summary, Claims, Speeches.
Lags and summary figures are live formulas over the Claims sheet, so edits to
a date or a code flow through.
"""
from __future__ import annotations

import datetime as dt
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.formula import ArrayFormula

from .build import build
from .config import ROOT

OUT = ROOT / "outputs" / "pilot_claims.xlsx"
FONT = "Arial"
HEAD_FILL = PatternFill("solid", start_color="1F2A37")
HEAD_FONT = Font(name=FONT, bold=True, color="FFFFFF", size=10)
BODY = Font(name=FONT, size=10)
BOLD = Font(name=FONT, size=10, bold=True)
TITLE = Font(name=FONT, size=14, bold=True)
NOTE = Font(name=FONT, size=10, italic=True, color="555555")
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")
RULE = Border(bottom=Side(style="thin", color="BBBBBB"))

# (header, source field, width, kind). kind: text | wrap | date | int | formula
CLAIMS = [
    ("Claim ID", "claim_id", 30, "text"),
    ("Country", "country", 9, "text"),
    ("Chamber", "chamber_label", 22, "text"),
    ("Debate date", "date", 12, "date"),
    ("Speaker", "speaker", 22, "text"),
    ("Debate", "heading", 30, "wrap"),
    ("Claim (paraphrase)", "claim", 48, "wrap"),
    ("Quote (verbatim)", "quote", 60, "wrap"),
    ("Claim type", "claim_type", 12, "text"),
    ("Domain", "domain", 16, "text"),
    ("Named system", "named_system", 16, "text"),
    ("Evidence basis", "evidence_basis", 18, "text"),
    ("Source", "source_name", 36, "wrap"),
    ("Source organisation", "source_org", 26, "wrap"),
    ("Source type", "source_type", 16, "text"),
    ("Source identified by", "source_identified_by", 18, "text"),
    ("Source date (as coded)", "source_date", 14, "text"),
    ("Source date basis", "source_date_basis", 16, "text"),
    ("Source date (resolved)", "source_date_resolved", 14, "date"),
    ("Cited lag (days)", None, 12, "formula"),
    ("Cited lag (months)", None, 12, "formula"),
    ("Source URL", "source_url", 36, "text"),
    ("Source notes", "source_notes", 36, "wrap"),
    ("Vintage status", "vintage_status", 15, "text"),
    ("Vintage date (as coded)", "vintage_date", 14, "text"),
    ("Vintage date (resolved)", "vintage_date_resolved", 14, "date"),
    ("Implied lag (days)", None, 12, "formula"),
    ("Implied lag (months)", None, 12, "formula"),
    ("Vintage rationale", "vintage_rationale", 48, "wrap"),
    ("Vintage confidence", "vintage_confidence", 12, "text"),
    ("Capability since", "capability_since", 12, "text"),
    ("Adjudicated", "adjudicated", 11, "text"),
    ("Adjudication reason", "adjudication_reason", 36, "wrap"),
    ("Hansard URL", "url", 40, "text"),
    ("Speech ID", "speech_id", 30, "text"),
]
SPEECHES = [
    ("Speech ID", "speech_id", 32, "text"),
    ("Country", "country", 9, "text"),
    ("Chamber", "chamber_label", 22, "text"),
    ("Debate date", "date", 12, "date"),
    ("Speaker", "speaker", 24, "text"),
    ("Debate", "heading", 34, "wrap"),
    ("Sub-heading", "subheading", 34, "wrap"),
    ("Words", "word_count", 8, "int"),
    ("AI mentions", "ai_mentions", 10, "int"),
    ("AI relevance", "ai_relevance", 14, "text"),
    ("Claims", "n_claims", 8, "int"),
    ("Near misses", "n_near_misses", 11, "int"),
    ("Sampling weight", "weight", 12, "int"),
    ("Coder notes", "coder_notes", 60, "wrap"),
    ("Hansard URL", "url", 44, "text"),
]


def col(spec, header: str) -> str:
    return get_column_letter([h for h, *_ in spec].index(header) + 1)


def write_table(ws, spec, rows, formulas=None):
    for j, (header, _, width, _) in enumerate(spec, 1):
        c = ws.cell(row=1, column=j, value=header)
        c.font, c.fill, c.alignment = HEAD_FONT, HEAD_FILL, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(j)].width = width
    ws.row_dimensions[1].height = 30
    for i, row in enumerate(rows, 2):
        for j, (header, field, _, kind) in enumerate(spec, 1):
            cell = ws.cell(row=i, column=j)
            if kind == "formula":
                cell.value = formulas[header](i)
                cell.number_format = "0" if "days" in header else "0.0"
            else:
                value = row.get(field)
                if kind == "date" and value:
                    value = dt.date.fromisoformat(value)
                    cell.number_format = "yyyy-mm-dd"
                elif isinstance(value, bool):
                    value = "yes" if value else ""
                cell.value = value
                if kind == "text" and isinstance(value, str) and value.startswith("http"):
                    cell.hyperlink = value
                    cell.font = Font(name=FONT, size=10, color="0563C1", underline="single")
                    cell.alignment = TOP
                    continue
            cell.font = BODY
            cell.alignment = WRAP if kind == "wrap" else TOP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(spec))}{max(len(rows) + 1, 2)}"


def main() -> int:
    claims, speeches, summary = build()
    wb = Workbook()

    # ---- Claims ----
    wc = wb.active
    wc.title = "Claims"
    debate, src, vin, status = (col(CLAIMS, h) for h in (
        "Debate date", "Source date (resolved)", "Vintage date (resolved)", "Vintage status"))
    cited_d, implied_d = col(CLAIMS, "Cited lag (days)"), col(CLAIMS, "Implied lag (days)")
    ident = col(CLAIMS, "Source identified by")
    formulas = {
        "Cited lag (days)": lambda r: (
            f'=IF(OR({src}{r}="",{ident}{r}<>"named_in_speech"),"",{debate}{r}-{src}{r})'),
        "Cited lag (months)": lambda r: f'=IF({cited_d}{r}="","",{cited_d}{r}/30.4375)',
        "Implied lag (days)": lambda r: (
            f'=IF({status}{r}="current",0,IF({vin}{r}="","",{debate}{r}-{vin}{r}))'),
        "Implied lag (months)": lambda r: f'=IF({implied_d}{r}="","",{implied_d}{r}/30.4375)',
    }
    write_table(wc, CLAIMS, claims, formulas)

    # ---- Speeches ----
    ws = wb.create_sheet("Speeches")
    write_table(ws, SPEECHES, speeches)

    # ---- Summary (formulas over Claims and Speeches) ----
    sm = wb.create_sheet("Summary", 0)
    last = max(len(claims) + 1, 2)
    slast = max(len(speeches) + 1, 2)

    def rng(header, spec=CLAIMS, sheet="Claims", end=last):
        c = col(spec, header)
        return f"{sheet}!${c}$2:${c}${end}"

    country, basis, vstat = rng("Country"), rng("Evidence basis"), rng("Vintage status")
    cited_m, implied_m = rng("Cited lag (months)"), rng("Implied lag (months)")
    s_country = rng("Country", SPEECHES, "Speeches", slast)
    s_claims = rng("Claims", SPEECHES, "Speeches", slast)

    sm["A1"] = "Evidence lag in parliament: pilot summary"
    sm["A1"].font = TITLE
    sm["A2"] = ("Every figure below is a formula over the Claims and Speeches sheets. "
                "Pilot sample, not the full corpus.")
    sm["A2"].font = NOTE
    for j, h in enumerate(["Measure", "UK", "AU", "Both"], 1):
        c = sm.cell(row=4, column=j, value=h)
        c.font, c.fill = HEAD_FONT, HEAD_FILL

    def count_row(r, label, fn, fmt="0"):
        sm.cell(row=r, column=1, value=label).font = BODY
        for j, cc in enumerate(["UK", "AU", None], 2):
            cell = sm.cell(row=r, column=j, value=fn(cc))
            cell.font, cell.number_format = BODY, fmt
            if isinstance(cell.value, ArrayFormula):
                cell.value.ref = cell.coordinate

    def cif(*pairs):
        return lambda cc: "=COUNTIFS(" + ",".join(
            ([f'{country},"{cc}"'] if cc else []) + [f'{a},"{b}"' for a, b in pairs]
        ) + ")" if (cc or pairs) else f"=COUNTA({country})"

    def median(values, extra=None):
        def fn(cc):
            conds = [f'({country}="{cc}")'] if cc else []
            if extra:
                conds.append(f'({extra[0]}="{extra[1]}")')
            conds.append(f"ISNUMBER({values})")
            test = "*".join(conds)
            return ArrayFormula("A1", f'=IFERROR(MEDIAN(IF({test},{values})),"")')
        return fn

    r = 5
    sm.cell(row=r, column=1, value="Speeches coded").font = BOLD
    for j, cc in enumerate(["UK", "AU", None], 2):
        f = f'=COUNTIF({s_country},"{cc}")' if cc else f"=COUNTA({s_country})"
        sm.cell(row=r, column=j, value=f).font = BODY
    r += 1
    sm.cell(row=r, column=1, value="Speeches with at least one claim").font = BODY
    for j, cc in enumerate(["UK", "AU", None], 2):
        f = (f'=COUNTIFS({s_country},"{cc}",{s_claims},">0")' if cc
             else f'=COUNTIF({s_claims},">0")')
        sm.cell(row=r, column=j, value=f).font = BODY
    r += 1
    count_row(r, "Capability claims", cif()); sm.cell(row=r, column=1).font = BOLD
    r += 2
    sm.cell(row=r, column=1, value="Evidence offered").font = BOLD
    for label, val in [("Named source", "cited_source"), ("Vague attribution", "vague_attribution"),
                       ("Personal experience", "personal_experience"), ("None", "none")]:
        r += 1
        count_row(r, "  " + label, cif((basis, val)))
    r += 2
    sm.cell(row=r, column=1, value="Cited evidence (claims with a dated source)").font = BOLD
    r += 1
    count_row(r, "  Claims with a dated source",
              lambda cc: f'=COUNTIFS({country},"{cc}",{cited_m},">=0")' if cc
              else f'=COUNTIF({cited_m},">=0")')
    r += 1
    count_row(r, "  Median cited lag (months)", median(cited_m), "0.0")
    r += 2
    sm.cell(row=r, column=1, value="Implied vintage").font = BOLD
    for label, val in [("Current", "current"), ("Outdated", "outdated"),
                       ("Dated event (incident)", "dated_event"), ("Forecast", "forecast"),
                       ("Never accurate", "never_accurate"), ("Unclear", "unclear")]:
        r += 1
        count_row(r, "  " + label, cif((vstat, val)))
    r += 1
    count_row(r, "  Median lag of outdated claims (months)",
              median(implied_m, (vstat, "outdated")), "0.0")
    r += 1
    count_row(r, "  Median age of cited incidents (months)",
              median(implied_m, (vstat, "dated_event")), "0.0")
    sm.column_dimensions["A"].width = 46
    for c in "BCD":
        sm.column_dimensions[c].width = 10

    # ---- Read me ----
    rm = wb.create_sheet("Read me", 0)
    corpus = summary["corpus"]
    total_ai = sum(v["ai_speeches"] for v in corpus.values())
    lines = [
        ("Evidence lag in parliament: pilot claims workbook", TITLE),
        (f"Generated {summary['generated']}. Codebook {summary['codebook']}.", NOTE),
        ("", BODY),
        ("What this is", BOLD),
        (f"A pilot coding of {summary['coded_speeches']} speeches sampled from {total_ai} "
         "speeches that mention AI in the UK and Australian parliaments since 1 July 2026.", BODY),
        ("Each row of Claims is one capability claim: a statement about what AI can or "
         "cannot do, how it behaves, or how fast it is changing.", BODY),
        ("", BODY),
        ("Sheets", BOLD),
        ("Summary: headline counts and medians, all formulas.", BODY),
        ("Claims: one row per claim, with its source, dates and lags.", BODY),
        ("Speeches: one row per sampled speech, including speeches with no claims.", BODY),
        ("", BODY),
        ("How the lags are defined", BOLD),
        ("Cited lag = debate date minus the publication date of the source the speaker named. "
         "Sources the coder identified for an unsourced claim are listed but get no cited lag.", BODY),
        ("Implied lag = debate date minus the last month the claim was still a fair "
         "description of AI. Zero when the claim is still current.", BODY),
        ("Partial dates (a month or a year) are placed at the middle of the period. "
         "See 'Source date (resolved)'.", BODY),
        ("", BODY),
        ("Read these limits before quoting a number", BOLD),
        ("Pilot sample: 50 speeches per country. Estimates are indicative only.", BODY),
        ("Coding was done by AI coders against CODEBOOK.md, then reviewed. "
         "It has not been checked by a human coder.", BODY),
        ("Coders' own knowledge ends around mid-2026. 'Current' means current at that "
         "horizon, so implied lag is a floor.", BODY),
        ("'Source date basis' shows whether a date was confirmed on the web or recalled.", BODY),
        ("", BODY),
        ("Editing", BOLD),
        ("Change a resolved date or a status in Claims and the lag and Summary cells update.", BODY),
        ("Data: TheyWorkForYou (UK) and OpenAustralia (AU) bulk Hansard XML.", NOTE),
    ]
    for i, (text, font) in enumerate(lines, 1):
        c = rm.cell(row=i, column=1, value=text)
        c.font, c.alignment = font, Alignment(wrap_text=True, vertical="top")
    rm.column_dimensions["A"].width = 110

    wb.move_sheet("Read me", offset=-wb.index(rm))
    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(claims)} claims, {len(speeches)} speeches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
