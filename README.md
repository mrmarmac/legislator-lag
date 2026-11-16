# Evidence lag in parliament

**Question.** How stale is the AI evidence that UK and Australian
parliamentarians cite?

**Status.** Full run complete: 613 speeches coded under codebook v0.2, then
reviewed in part by a human. The numbers below include the reviewer's
rulings. An earlier 100-speech pilot under v0.1 is kept for reference.

**Short answer.** Rarely stale. More often, missing. When a parliamentarian
names a source for a claim about AI, it is usually weeks old. But half of all
claims come with no evidence at all.

## What the full run found

The corpus is 1,182 speeches that mention AI, from 1 July 2026 to the latest
sitting day available (12 November for the UK; 29 October for the Australian
House; 15 October for the Senate). The 613 speeches with two or more AI terms
were coded. 282 of them contain at least one factual claim about AI.

| | UK | Australia | Both |
|---|---:|---:|---:|
| Speeches coded | 417 | 196 | 613 |
| Speeches with a claim | 184 | 98 | 282 |
| Claims | 335 | 226 | 561 |
| No evidence offered | 170 | 114 | 284 |
| Vague attribution ("experts say") | 42 | 34 | 76 |
| Personal experience | 13 | 9 | 22 |
| Named source | 110 | 69 | 179 |
| Named source that could be dated | 98 | 63 | 161 |
| Median age of a dated named source | 1.1 months | 8 days | 28 days |

**How old are named sources?** Of the 161 that could be dated:

- 81 (50%) were under a month old, and 55 of those were a week old or less.
- 18 (11%) were more than a year old, and 11 were two years old or more.
- The oldest was a 2014 post, quoted in September 2026 without its date.

**Old is not the same as out of date.** Each claim was also judged on whether
it was still the latest fair account on the day.

| Assessment | Claims |
|---|---:|
| Still current | 309 |
| Dated incident | 124 |
| Contested: overstated or disputed | 74 |
| Unclear: could not be assessed | 30 |
| Forecast | 19 |
| Outdated: overtaken by newer evidence | 3 |
| Never accurate | 2 |

Only three claims had been overtaken by newer evidence. Seventy-four were
overstated or disputed, which is the larger quality problem.

**Incidents.** 124 claims described a specific incident, and 112 could be
dated. The median incident had been public for 1.8 months. In 53 cases the
speaker's account went beyond what reporting supports, or the incident could
not be verified.

**By kind of claim.** Median age of dated named sources: labour 6.2 months,
limitations 4.0, adoption 2.0, economic 1.6, capability 1.0, incidents 0.6,
opinion and risk estimates 0.3. Most kinds have fewer than 20 dated sources,
so treat these as rough.

**UK and Australia.** Australian sources were fresher at the median. The
Australian sample is smaller and ends in October. The gap may reflect which
debates fell in the window, not a lasting difference.

### Human review

One person reviewed three samples on 15 November 2026, using the review page
(`site/review.html`). The packets showed the coders' labels and the speech
text, with no proposed rulings. The verdicts are in
`data/full/review/verdicts.jsonl`.

**Spot-check: 40 claims.** A seeded random draw, stratified by country and
evidence offered.

| Question | Result |
|---|---|
| Is it a claim? | 29 yes, 7 no, 4 unsure |
| Kind of claim | 38 agreed, 2 unsure |
| Evidence offered | 39 agreed, 1 unsure |
| Source and date (25 with a source) | 22 right, 3 could not be verified |
| Date an incident became public (9 incidents) | 2 right, 7 could not be verified |
| Currency on the day | 24 agreed, 2 disagreed, 13 unsure, 1 ruling withdrawn |

Weighted to the corpus, 14% of coded claims were ruled not to be claims. With
40 claims, that estimate is rough. The reviewer read the whole speech in 3 of
40 cases and found one missed claim, so missed claims remain largely
unchecked.

**Adjudication: 60 double-coded speeches.** 31 matched on every field that
changes a reported number. The reviewer ruled on the other 29.

- 16 claims were found by one coder only. 13 were ruled not claims.
- 51 labels differed on matched claims. The reviewer chose the first coder 17
  times, the second 20 times, neither once, and was unsure 13 times.
- 5 speeches differed on relevance. One was ruled on. Four were left unsure.

**The tail: 25 claims.** The 21 named sources over a year old and the 6
outdated or never-accurate claims, 2 of which are in both groups.

- All 6 outdated or never-accurate rulings were confirmed.
- Of the 21 old sources, 18 were confirmed as the right source with the right
  date. Three could not be verified.
- A primary document link is on record for one source. For the rest, the
  record shows the reviewer's verdict only.

**Primary-document check of the old sources.** After the review above, an AI
subagent (Claude Opus 5.5) looked for the primary document behind each of the
21 old sources. It found one for 16, a partial one for 4, and none for 1. It
opened 13 of the links; 7 come from search results because the site refused
the request. The list is in `data/full/review/tail_primary.md`. The reviewer
then ruled on the four cases it flagged:

- One source was the wrong edition. The figure quoted came from an edition
  published on the day of the debate, so the claim is current, not outdated.
- One figure was credited to a 2024 note but worded as in a 2026 report that
  relays it. It is now dated to the 2026 report.
- One company policy had a newer version in force on the debate day.
- One date was a day out, because the coder had used the news report's date.

Three of the 21 sources are therefore no longer over a year old. These four
rulings are lines in `data/full/adjudication.jsonl` marked
`"by": "tail_verification"`. The reviewer has not yet confirmed the other 17
entries in the list.

**What the review changed.** 16 claims dropped, 1 added from the second
coding, 15 relabelled, and 1 speech's relevance changed. Every change is a
line in `data/full/adjudication.jsonl` marked `"by": "human_review"`.

**What it implies.** Both checks point the same way: the coders included
remarks that are not claims. Only sampled claims were corrected. The other
500 or so were not reviewed, so the claim counts above are probably still too
high. Lags are measured on named, dated sources and are less affected.

### How far to trust this

- **A human checked samples, not every label.** One reviewer, working alone.
  Coding was done by AI coders (Claude Opus 5.5) working from `CODEBOOK.md`
  and `docs/coder_brief.md`.
- **Second coding.** Sixty speeches were coded twice by coders who could not
  see the first coding. They agreed on whether a speech holds any claim in 95%
  of speeches. They found 63 and 54 claims, of which 49 were the same claim.
  On those, they agreed on the kind of claim 98% of the time, on the evidence
  offered 88%, and on currency 84%. Both coders were the same model, so this
  measures consistency, not correctness. These figures describe the coders
  before any review.
- **Which claims get found is the weak point.** A quarter of claims found by
  one coder were not found by the other, and the reviewer ruled most of those
  out. Counts of claims are softer than the lags measured on them.
- **Currency is hard to judge.** The reviewer was unsure on currency for 13 of
  40 spot-checked claims.
- **Source dates.** 139 of 161 were confirmed on a page found by web search,
  usually news coverage or a listing and not the primary document. The check
  of the 21 oldest found 3 that were wrongly old, which suggests other dates
  may also err towards older. 17 rest on
  a date stated in the speech, and 5 on coder recall.
- **Knowledge horizon.** The coders' own knowledge ends before most of these
  debates. "Still current" means current as far as the coder could establish.
  Some of those claims may already have been stale.
- **Earlier review.** Before the human review, the session that ran the coders
  dropped 9 claims from the first 14 batches so they match three rulings made
  mid-run (`CODEBOOK.md` section 7). Those drops are also logged in
  `data/full/adjudication.jsonl`.
- **Left as they are.** One missed claim the reviewer noted was not coded
  (`au-representatives:2026-10-27.113.1`). One currency ruling was withdrawn
  by the reviewer and the coder's label stands
  (`uk-lords:2026-11-12a.411.0#1`). The full run was not recoded under
  codebook v0.3.
- **Frame.** Speeches with a single AI term were not coded.

## The pilot (100 speeches, codebook v0.1)

The corpus is 1,182 speeches that mention AI, from 1 July 2026 to the latest
sitting day available (12 November for the UK; 29 October for the Australian
House; 15 October for the Senate). The pilot coded a random 100 of them, 50
per country.

| | UK | Australia | Both |
|---|---:|---:|---:|
| Speeches coded | 50 | 50 | 100 |
| Speeches with a capability claim | 7 | 9 | 16 |
| Capability claims | 10 | 17 | 27 |
| Claims with no evidence offered | 8 | 11 | 19 |
| Claims naming a datable source | 1 | 4 | 5 |
| Claims describing a dated incident | 5 | 6 | 11 |
| Claims coded outdated | 0 | 0 | 0 |

- **Claims are rare.** 84 of 100 AI-mentioning speeches say nothing about what
  AI can do. None of the 44 speeches with a single AI term held a claim.
  Seven of the 12 speeches with 11 or more AI terms did.
- **Evidence is rarely offered.** 19 of 27 claims were bare assertions.
- **When a source is named, it is recent.** All five named sources were under
  two months old. The median was nine days.
- **Incidents are recent too.** The 11 incidents had a median age of two
  months. The oldest was 22 months.
- **No claim was outdated.** No speaker described an AI that had already been
  surpassed, as far as the coders could tell.
- **Older evidence sat outside the definition.** Coders logged 127 near
  misses. Some cited older sources: a 2024 sector study, an IMF exposure
  estimate, a quotation the coder traced to 2014. These are not capability
  claims under codebook v0.1, so they are not in the counts.

Read this as a signal about method, not as an answer. Twenty-seven claims
cannot support rates, medians, or a comparison between the two parliaments.

### Limits of the pilot

- **No human has checked the labels.** Coding was done by AI coders working
  from `CODEBOOK.md`. The session that ran them read every claim and re-ran
  the searches behind three source dates. It overrode no label.
- **Agreement is untested in any strong sense.** Twenty speeches were coded
  twice, independently. The two codings matched on all six claims and every
  compared field. Both coders were the same model with the same codebook, so
  this shows the codebook is applied consistently. It does not show the
  labels are right.
- **Knowledge horizon.** The coders' own knowledge ends around mid-2026, before
  most of these debates. "Current" means current at that horizon. A claim can
  be current then and stale by the debate, so implied lag is a floor.
- **Source dates come from news coverage.** Coders confirmed dates on pages
  found by search, usually news reports and not the primary document.
- **Recall-based fields.** `capability_since` is from coder recall and is
  exploratory.
- **OpenAustralia links are unverified.** The site blocks automated requests,
  so the Australian speech URLs follow its URL pattern but were not opened.
- **The API fetcher is untested.** See below.

## Decisions taken after the pilot

| Decision | Ruling |
|---|---|
| Sampling frame | Speeches with two or more AI terms: 613 of 1,182. |
| Unit | Any checkable factual claim about AI, not only capability claims. |
| Incident dating | The date an incident became public is the evidence date. The occurrence date is kept as a second field. |
| Twelve codebook gaps | Ruled as listed in `CODEBOOK.md` section 6. |
| After the human review | Codebook v0.3 adds worked examples of remarks that are not claims (section 8). No rule changed, and no speech was recoded. |

The pilot labels stay as coded under v0.1. The full run recoded every speech
in the frame under v0.2, including pilot speeches.

## How the full run was coded

The 613 speeches were split into 49 batches of about 7,900 words
(`python -m legislag.batches`). Each batch was coded by a Claude Opus 5.5
subagent in a Claude Code session, following `docs/coder_brief.md`. A random
60 speeches were coded a second time in 6 further batches. Labels are in
`data/full/labels/`.

## Rerunning the human review

```bash
python -m legislag.review                # build the packets and site/review.html
```

```bash
python -m legislag.review --import DIR   # merge verdict documents saved from the page
```

```bash
python -m legislag.review --apply        # write the rulings into adjudication.jsonl
```

Then rebuild the outputs. The packets are always built from the labels as
they stood before the human review, so the sample does not move.

## Rerunning without a Claude Code session

`legislag/code_api.py` codes the frame with the Claude API. It sends one
request per speech. Claude reads the speech, searches the web to date sources
and incidents, and hands in a coding that is checked by the same rules as
`legislag.validate`. Failed checks go back to Claude to fix.

```bash
export ANTHROPIC_API_KEY=...
```

```bash
python -m legislag.code_api --dry-run     # frame size and cost range, no API calls
```

```bash
python -m legislag.code_api --limit 5     # smoke test
```

```bash
python -m legislag.code_api               # the full run; rerun to resume or retry failures
```

```bash
python -m legislag.code_api --reliability 60   # independent second coding of 60 speeches
```

```bash
python -m legislag.build --run full && python -m legislag.xlsx --run full
```

- **Model.** `claude-opus-5-5` at high effort by default. Change with `--model`
  and `--effort`.
- **Cost.** The dry run prints a rough range. For 613 speeches it is about
  $50 to $190 on the default model. The range is an estimate from token
  counts and an assumed web-search price, not a measurement.
- **Fallbacks.** If the model declines a speech on safety grounds, the API
  reruns it on a fallback model. `--no-fallbacks` turns this off. The model
  that coded each speech is recorded in `coder`.
- **Status.** This script was not used for the published results. Its request
  loop has been tested against a stub client only. It has never been run
  against the live API.

## Outputs

| File | What it is |
|---|---|
| `site/index.html` | Full-run results page: charts and a browser of every claim. |
| `docs/index.html` | The same page as a standalone document, served by GitHub Pages from `main:/docs`. Rebuilt by `python -m legislag.site --run full`. |
| `outputs/full_claims.xlsx` | Workbook: summary, claims, speeches. Lags are formulas. |
| `outputs/figures/` | Three figures for the paper as SVG and PNG, with captions. Built by `python -m legislag.figures`, then `node legislag/figures_png.js` for the PNGs. |
| `outputs/full_claims.csv`, `outputs/full_speeches.csv` | The same tables as CSV. |
| `outputs/full_summary.json` | Headline numbers, claim yield, reliability. |
| `data/full/labels/` | Raw coder output, one file per batch. `rel_*` files are the second coding. |
| `data/full/adjudication.jsonl` | Every change made on review, with reasons: 9 earlier drops, 33 lines from the human review and 4 from the primary-document check. |
| `site/review.html`, `outputs/full_review.json` | Human review page and its packets: the 40-claim spot-check sample, the double-coded speeches that disagree, and the tail. |
| `data/full/review/` | The reviewer's verdicts and a summary of them. |
| `site/pilot.html`, `outputs/pilot_*`, `data/pilot/` | The same outputs for the pilot. |
| `data/speeches_ai.jsonl` | The corpus: every AI-mentioning speech. |

## Run it

```bash
pip install -r requirements.txt
```

```bash
python -m legislag.fetch_bulk   # download Hansard XML to data/raw/ (about 100 MB)
```

```bash
python -m legislag.parse        # write data/speeches_ai.jsonl
```

```bash
python -m legislag.sample       # draw the pilot sample and coding batches
```

```bash
python -m legislag.validate data/pilot/labels/batch_*.jsonl
```

```bash
python -m legislag.build --run full && python -m legislag.xlsx --run full && python -m legislag.site --run full
```

Drop `--run full` from each command to rebuild the pilot outputs. Coding sits
between batching and `build`: see the two sections above.

### Data source: bulk XML now, APIs when keys exist

Both projects publish the Hansard behind their APIs as keyless bulk XML:
[TheyWorkForYou](https://www.theyworkforyou.com/pwdata/scrapedxml/) and
[OpenAustralia](https://data.openaustralia.org.au/scrapedxml/). The pipeline
uses those.

`legislag/fetch_api.py` fetches the same speeches through the
[TheyWorkForYou API](https://www.theyworkforyou.com/api/) and the
[OpenAustralia API](https://www.openaustralia.org.au/api/). It reads
`TWFY_API_KEY` and `OPENAUSTRALIA_API_KEY` from the environment and skips any
chamber whose key is missing. **It has not been run against the live APIs**,
because no keys were available. It was written from the published API
documentation and exercised on example payloads only. Compare its output with
`data/speeches_ai.jsonl` on first use.

## How a speech enters the corpus

A speech is included if it contains an AI term: "artificial intelligence",
"AI", "machine learning", "large language model", "LLM", "chatbot", "ChatGPT",
"deepfake", "superintelligence", "AGI", "frontier model", "OpenAI",
"Anthropic", or "DeepMind". The pattern is in `legislag/config.py`.

Chambers: House of Commons, Westminster Hall, House of Lords, House of
Representatives, Senate. Written answers and committees are not included.

## Hansard text and licences

Speech text comes from TheyWorkForYou (mySociety) and OpenAustralia
(OpenAustralia Foundation), which republish the official record.

**UK.** Contains Parliamentary information licensed under the
[Open Parliament Licence v3.0](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/).
Data service provided by [TheyWorkForYou](https://www.theyworkforyou.com/).

**Australia.** Australian Hansard is © Commonwealth of Australia, from the
[Parliament of Australia website](https://www.aph.gov.au/), under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/),
obtained through [OpenAustralia](https://www.openaustralia.org.au/). That
licence allows non-commercial sharing of unmodified material. Speeches in
`data/` are reproduced in full and unchanged. The results page quotes them in
part, with the wording of each quote unchanged.

The Australian terms were confirmed on 15 November 2026 from the Parliament
of Australia's
[copyright page](https://www.aph.gov.au/Help/Disclaimer_Privacy_Copyright).
It puts all material on the website under CC BY-NC-ND 4.0, "with the exception
of the Commonwealth Coat of Arms and where otherwise noted", and asks for
attribution as "Parliament of Australia website". It describes the freedom as
copying and communicating material "in its current form" for non-commercial
purposes. Whether short quotations count as the current form is not settled
here.

These licences cover the Hansard text only.

## Licence for this project's own work

- **Code:** MIT. See `LICENSE`.
- **Codebook, labels, verdicts and figures:** CC BY 4.0. See `LICENSE-DATA.md`,
  which also lists what is excluded.
