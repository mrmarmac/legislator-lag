# Evidence lag in parliament

**Question.** How stale is the AI evidence that UK and Australian
parliamentarians cite?

**Status.** Full run complete: 613 speeches coded under codebook v0.2. An
earlier 100-speech pilot under v0.1 is kept for reference.

**Short answer.** Rarely stale. More often, missing. When a parliamentarian
names a source for a claim about AI, it is usually weeks old. But half of all
claims come with no evidence at all.

## What the full run found

The corpus is 1,182 speeches that mention AI, from 1 July 2026 to the latest
sitting day available (12 November for the UK; 29 October for the Australian
House; 15 October for the Senate). The 613 speeches with two or more AI terms
were coded. 288 of them contain at least one factual claim about AI.

| | UK | Australia | Both |
|---|---:|---:|---:|
| Speeches coded | 417 | 196 | 613 |
| Speeches with a claim | 188 | 100 | 288 |
| Claims | 343 | 233 | 576 |
| No evidence offered | 175 | 119 | 294 |
| Vague attribution ("experts say") | 44 | 34 | 78 |
| Personal experience | 15 | 10 | 25 |
| Named source | 109 | 70 | 179 |
| Named source that could be dated | 97 | 65 | 162 |
| Median age of a dated named source | 1.2 months | 8 days | 29 days |

**How old are named sources?** Of the 162 that could be dated:

- 81 (50%) were under a month old, and 56 of those were under a week old.
- 21 (13%) were more than a year old, and 12 were more than two years old.
- The oldest was a 2014 post, quoted in September 2026 without its date.

**Old is not the same as out of date.** Coders also judged whether each claim
was still the latest fair account on the day.

| Assessment | Claims |
|---|---:|
| Still current | 316 |
| Dated incident | 124 |
| Contested: overstated or disputed | 79 |
| Unclear: could not be assessed | 33 |
| Forecast | 18 |
| Outdated: overtaken by newer evidence | 4 |
| Never accurate | 2 |

Only four claims had been overtaken by newer evidence. Seventy-nine were
overstated or disputed, which is the larger quality problem.

**Incidents.** 124 claims described a specific incident, and 113 could be
dated. The median incident had been public for 1.6 months. In 50 cases the
speaker's account went beyond what reporting supports, or the incident could
not be verified.

**By kind of claim.** Median age of dated named sources: labour 7.2 months,
limitations 4.0, economic 2.6, adoption 2.0, capability 0.8, incidents 0.6,
opinion and risk estimates 0.3. Most kinds have fewer than 20 dated sources,
so treat these as rough.

**UK and Australia.** Australian sources were fresher at the median. The
Australian sample is smaller and ends in October. The gap may reflect which
debates fell in the window, not a lasting difference.

### How far to trust this

- **No human has checked the labels.** All coding was done by AI coders
  (Claude Opus 5.5) working from `CODEBOOK.md` and `docs/coder_brief.md`.
- **Second coding.** Sixty speeches were coded twice by coders who could not
  see the first coding. They agreed on whether a speech holds any claim in 95%
  of speeches. They found 63 and 54 claims, of which 49 were the same claim.
  On those, they agreed on the kind of claim 98% of the time, on the evidence
  offered 88%, and on currency 84%. Both coders were the same model, so this
  measures consistency, not correctness.
- **Which claims get found is the weak point.** A quarter of claims found by
  one coder were not found by the other. Counts of claims are softer than
  the lags measured on them.
- **Source dates.** 140 of 162 were confirmed on a page found by web search,
  usually news coverage or a listing and not the primary document. 17 rest on
  a date stated in the speech, and 5 on coder recall.
- **Knowledge horizon.** The coders' own knowledge ends before most of these
  debates. "Still current" means current as far as the coder could establish.
  Some of those claims may already have been stale.
- **Review.** The session that ran the coders read the outdated and
  never-accurate claims and the oldest sources, and re-ran the search behind
  one outdated claim. It dropped 9 claims from the first 14 batches so they
  match three rulings made mid-run (`CODEBOOK.md` section 7). It changed no
  other label. The drops are logged in `data/full/adjudication.jsonl`.
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

The pilot labels stay as coded under v0.1. The full run recoded every speech
in the frame under v0.2, including pilot speeches.

## How the full run was coded

The 613 speeches were split into 49 batches of about 7,900 words
(`python -m legislag.batches`). Each batch was coded by a Claude Opus 5.5
subagent in a Claude Code session, following `docs/coder_brief.md`. A random
60 speeches were coded a second time in 6 further batches. Labels are in
`data/full/labels/`.

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
| `outputs/full_claims.xlsx` | Workbook: summary, claims, speeches. Lags are formulas. |
| `outputs/full_claims.csv`, `outputs/full_speeches.csv` | The same tables as CSV. |
| `outputs/full_summary.json` | Headline numbers, claim yield, reliability. |
| `data/full/labels/` | Raw coder output, one file per batch. `rel_*` files are the second coding. |
| `data/full/adjudication.jsonl` | The nine claims dropped on review, with reasons. |
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

## Hansard text

Speech text comes from TheyWorkForYou (mySociety) and OpenAustralia
(OpenAustralia Foundation), which republish the official record. Check each
project's licence terms before redistributing the text.
