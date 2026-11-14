# Evidence lag in parliament

**Question.** How stale is the AI evidence that UK and Australian
parliamentarians cite?

**Status.** Pilot complete: 100 speeches coded. The full run has not started.

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

## Decisions needed before the full run

1. **Sampling frame.** A random draw wastes most of its reading on passing
   mentions. Options: code only speeches with three or more AI terms (386 of
   1,182), or only debates with AI in the title (315), or everything.
2. **Scope of the unit.** Keep "capability claims", or widen to any empirical
   AI claim that rests on a source. The widening is where older evidence
   appeared in the pilot.
3. **Incident dating.** Date an incident by when it happened or when it became
   public.
4. **The remaining codebook questions.** Listed in `CODEBOOK.md` section 6.

## Outputs

| File | What it is |
|---|---|
| `site/index.html` | Results page: charts and a browser of every claim. |
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
coders in a Claude session. A standalone script for the full run is the next
step.

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
