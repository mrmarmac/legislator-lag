# Evidence lag in parliament

**Question.** How stale is the AI evidence that UK and Australian
parliamentarians cite?

**Status.** Pilot complete: 100 speeches coded under codebook v0.1. The full
run is set up under codebook v0.2 and has not been run.

## What the pilot found

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

## Limits

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

The pilot labels stay as coded under v0.1. The full run recodes every speech
in the frame under v0.2, including pilot speeches.

## The full run

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
- **Status.** The request loop has been tested against a stub client only. It
  has not yet been run against the live API.

## Outputs

| File | What it is |
|---|---|
| `site/pilot.html` | Pilot results page: charts and a browser of every claim. |
| `outputs/pilot_claims.xlsx` | Workbook: summary, claims, speeches. Lags are formulas. |
| `outputs/pilot_claims.csv`, `outputs/pilot_speeches.csv` | The same tables as CSV. |
| `outputs/pilot_summary.json` | Headline numbers, claim yield, reliability. |
| `data/pilot/labels/` | Raw coder output, one file per batch. |
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
python -m legislag.build && python -m legislag.xlsx && python -m legislag.site
```

Coding sits between `sample` and `validate`. In the pilot it was done by AI
coders in a Claude session. The full run uses `legislag.code_api`, above.

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
