# Codebook v0.2

Research question: how stale is the AI evidence that UK and Australian
parliamentarians cite?

This codebook tells a coder how to turn one Hansard speech into zero or more
coded **claims**. Version 0.2 applies the rulings made after the 100-speech
pilot. Section 6 lists what changed. The pilot labels in `data/pilot/` were
coded under v0.1 and are kept as they were.

## 1. Unit of analysis

A **claim** is a checkable factual statement about AI, made or endorsed by the
speaker.

Test for inclusion: *could a well-informed person check this against evidence
from a particular date?* If yes, it is a claim.

### Claim types

| `claim_type` | Meaning | Example |
|---|---|---|
| `capability` | AI can do X, or does X at some level | "AI can now read mammograms as accurately as two radiologists." |
| `limitation` | AI cannot do X, or does X unreliably | "These chatbots simply make things up." |
| `trajectory` | A rate of progress or a forecast of capability, with a number or a source | "Task length is doubling every seven months." |
| `incident` | A specific thing a specific system did, or was used to do | "Grok produced sexualised images of real women on request." |
| `adoption` | Who uses AI, how much, or where it is deployed, with a figure or a result | "A third of small firms now use AI." |
| `economic` | Market, investment, productivity, or growth figures | "AI will add £400 billion to GDP." |
| `labour` | Jobs, tasks, or workers affected | "The IMF estimates 70% of UK workers are in exposed occupations." |
| `resource` | Energy, water, compute, or infrastructure figures | "The data centre would raise the state's energy use by 25 per cent." |
| `opinion` | What experts, builders, or the public believe, including risk estimates and polls | "People put the risk at around 10 per cent." |
| `other` | A checkable factual statement about AI that fits none of the above | "US courts have found training to be fair use." |

### Exclude

- Policy descriptions, announcements, and commitments ("we will legislate…").
- Normative statements ("AI must serve people").
- Rhetorical generalities with nothing to check ("AI is transforming everything").
- **Vague progress remarks.** "This technology is evolving fast" is out unless
  it carries a number or a source.
- **Proposals and hedged possibilities.** "AI could help…", "there is an
  opportunity to use AI…", "we should explore whether AI…" are out. A plain
  "AI can…" is in.
- **Systems the speaker does not call AI.** Recommender algorithms, rules-based
  assessment tools, and "the algorithm" are out unless the speaker describes
  them as AI.
- **Bare deployment facts** with no figure and no result ("the agency is
  trialling AI").
- **Tabled or incorporated text.** Motions, committee reports, and other
  members' words read into the record by the chair are out. A letter or
  account the speaker reads out and endorses is in.
- Claims the speaker reports only in order to reject them.

Log up to three excluded borderline items per speech under `near_misses`.

### Splitting and merging

- One claim per distinct proposition. A speech may yield several claims.
- A proposition repeated within a speech is coded once.
- A list ("AI can write, code, and draw") is one claim unless items have
  different evidence.

## 2. Speech-level fields

| Field | Values |
|---|---|
| `speech_id` | Copied from the input. |
| `codebook` | `"v0.2"`. |
| `ai_relevance` | `substantive` (AI is a topic of the speech), `passing` (AI is mentioned in a list or aside), `procedural` (the speech only moves, schedules, or administers AI business), `false_positive` (the match is not about artificial intelligence). |
| `claims` | List of claim objects. May be empty. |
| `near_misses` | List of `{ "quote": ..., "reason": ... }`. May be empty. |
| `coder_notes` | Free text. Use it for doubts about the codebook. |

## 3. Claim-level fields

### Identification

| Field | Rule |
|---|---|
| `quote` | Verbatim, contiguous excerpt from the speech `text` that states the claim. At most 60 words. It must be an exact substring: copy, do not retype or fix punctuation. |
| `supporting_quote` | Optional second excerpt, same rules, for context that sits elsewhere in the speech: the system's name, a date, the source. `null` if not needed. |
| `claim` | One neutral sentence restating the proposition. |
| `claim_type` | One of the ten types above. |
| `domain` | One of `general`, `health`, `education`, `defence_security`, `cyber`, `child_safety`, `deepfakes_misinfo`, `creative_copyright`, `work`, `public_services`, `science`, `finance`, `energy_infrastructure`, `other`. |
| `named_system` | The model, product, or company the claim is about, if the speaker names one. Otherwise `null`. |

### Evidence basis

`evidence_basis` records what the speaker offers in support of *this* claim.

| Value | Rule |
|---|---|
| `cited_source` | The speaker names an identifiable source: a report, study, article, organisation, named expert, company announcement, inquiry, or court case. |
| `vague_attribution` | "Experts say", "studies show", "the news today": a source is gestured at but not identified. |
| `personal_experience` | The speaker's own use, or a constituent's or visit's first-hand account. |
| `none` | Bare assertion. |

### Source fields

Fill these when `evidence_basis` is `cited_source`. Also fill them when the
speaker names no source but the coder can identify one with high confidence,
for example a distinctive statistic or a well-known incident. Otherwise set
all to `null`.

| Field | Rule |
|---|---|
| `source_name` | Title of the document or a short description. |
| `source_org` | Publishing organisation or author. |
| `source_type` | `government`, `parliamentary`, `academic`, `company`, `news`, `ngo_thinktank`, `international_body`, `legal`, `expert_statement`, `book`, `other`. |
| `source_identified_by` | `named_in_speech` or `inferred_by_coder`. Only `named_in_speech` sources count toward cited lag. |
| `source_date` | Publication date: `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`. Use the most precise form that is supported. `null` if it cannot be dated. |
| `source_date_basis` | `stated_in_speech`, `web_verified` (a page found by search confirms it), `coder_recall` (from the coder's own knowledge, unverified), or `unknown`. |
| `source_url` | A URL the coder actually retrieved or saw in search results. Never construct or guess a URL. `null` if none. |
| `source_notes` | Anything that affects the date: editions, which edition is meant, doubts. |
| `other_sources` | List of `{ "name": ..., "date": ..., "url": ... }` for further sources behind the same claim. Empty list if none. |

Rules:

- Date the source the speaker *cites*, not the research underneath it. A 2026
  news article about a 2024 study is dated 2026; say so in `source_notes`.
- **Two sources, one claim.** Put the *older* source in the main fields and
  the rest in `other_sources`. Lag is measured to the older one.
- If a source has editions (annual reports, index releases), choose the latest
  edition published before the debate unless the speech indicates another.
- A quotation or figure that has been re-shared is dated to its original
  publication if the speaker presents it without a date. Say so in
  `source_notes`.

### Incident fields

Fill these for `incident` claims. Otherwise `null` (and `false` for the flag).

| Field | Rule |
|---|---|
| `event_public_date` | The date the incident first became public. This is the evidence date. |
| `event_occurred_date` | The date the incident happened, if known and different. |
| `incident_loosely_described` | `true` if the speaker's account goes beyond, or differs from, what reporting supports ("illegal" for a contract breach; "websites" for one portal), or the incident is alleged and not established. |
| `incident_accuracy_note` | One sentence saying how the account differs. `null` if the flag is `false`. |

### Currency

Every claim gets a currency judgement, sourced or not. The question is: **was
this still the latest fair account on the day of the debate?**

| `vintage_status` | Rule | `vintage_date` |
|---|---|---|
| `current` | Still a fair description, or still the latest available figure. | `null` |
| `outdated` | Was once fair, but was superseded before the debate. | Last month in which it was still fair, `YYYY-MM`. |
| `contested` | Broadly true but overstated, or genuinely disputed among informed people. | `null` |
| `never_accurate` | Was not a fair description at any date. | `null` |
| `dated_event` | `incident` claims: the event itself is the evidence. Dates go in the incident fields. | `null` |
| `forecast` | The claim is about the future. Currency does not apply. | `null` |
| `unclear` | Too vague to assess, or outside what the coder can verify. | `null` |

Rules:

- A "can do X" claim stays `current` while X remains true. It becomes
  `outdated` only if the wording asserts a ceiling that has since been passed
  ("the best models can only…", "AI still cannot…").
- A "cannot do X" claim is `outdated` from the month public systems could do X.
- A statistic is `outdated` from the month a newer edition or figure from the
  same source replaced it.
- Judge capability against generally available frontier systems.
- `vintage_rationale`: one or two sentences. For `outdated`, name what
  superseded the claim.
- `vintage_confidence`: `high`, `medium`, `low`.

`capability_since` (`capability` claims only): the earliest month in which the
stated capability was true of public systems, `YYYY-MM`. **When the speaker
names an example, date that example**: "some AI already exceeds humans, such
as AlphaFold" is dated to AlphaFold. It measures how old the news is while the
claim is still true. `null` when it cannot be estimated.

### Knowledge horizon

The debates may run later than the coder's own knowledge. Speeches may mention
models, reports, and events the coder has never seen.

- Never mark something false or outdated because it is unfamiliar. Search.
- If a recent claim cannot be verified, use `unclear`.
- Record the horizon used in `coder_notes` if it affected a judgement.

## 4. Derived measures

Computed in `legislag/build.py`, not by coders.

- **Cited lag** = debate date − `source_date`, for sources with
  `source_identified_by` = `named_in_speech` only.
- **Incident lag** = debate date − `event_public_date`.
- **Implied lag** = debate date − `vintage_date` for `outdated` claims.
  `current` claims have lag zero. This is a floor: a claim can be current at
  the coder's horizon yet stale by the debate.
- A month- or year-precision date is placed at the middle of its period. If
  the debate falls inside that period, the middle of the part before the
  debate is used. Evidence is never dated after the speech that uses it.
- Claims with `forecast`, `contested`, `never_accurate`, or `unclear` status
  have no implied lag and are reported as counts.

## 5. Output format

One JSON object per line, one line per speech, including speeches with no claims.

```json
{
  "speech_id": "uk-lords:2026-07-09b.373.0",
  "codebook": "v0.2",
  "ai_relevance": "substantive",
  "claims": [
    {
      "quote": "…exact words from the speech…",
      "supporting_quote": null,
      "claim": "Frontier models can autonomously complete multi-hour software tasks.",
      "claim_type": "capability",
      "domain": "general",
      "named_system": null,
      "evidence_basis": "cited_source",
      "source_name": "International AI Safety Report 2026",
      "source_org": "International AI Safety Report",
      "source_type": "international_body",
      "source_identified_by": "named_in_speech",
      "source_date": "2026-02",
      "source_date_basis": "web_verified",
      "source_url": "https://…",
      "source_notes": null,
      "other_sources": [],
      "event_public_date": null,
      "event_occurred_date": null,
      "incident_loosely_described": false,
      "incident_accuracy_note": null,
      "vintage_status": "current",
      "vintage_date": null,
      "vintage_rationale": "Consistent with published task-horizon evaluations.",
      "vintage_confidence": "medium",
      "capability_since": "2025-03"
    }
  ],
  "near_misses": [
    { "quote": "…", "reason": "Proposal, not an assertion." }
  ],
  "coder_notes": ""
}
```

The example values illustrate the format only. They are not findings.

## 6. Changes from v0.1

Rulings made after the pilot.

| Area | v0.1 | v0.2 |
|---|---|---|
| Unit | Capability claims only | Any checkable factual claim about AI |
| Claim types | Four | Ten: adds `adoption`, `economic`, `labour`, `resource`, `opinion`, `other` |
| Sampling frame | Any speech with an AI term | Speeches with two or more AI terms |
| Incident date | Occurrence date, in `vintage_date` | Public date is the evidence date; occurrence date kept as a second field |
| Hedged claims | Silent | Proposals out; "can" statements in |
| Risk estimates | Coded as `trajectory` | Coded as `opinion` |
| Vague progress remarks | Silent | Out unless there is a number or a source |
| What counts as AI | Silent | Only what the speaker calls AI |
| Text read into the record | Silent | Endorsed letters in; tabled motions out |
| Unsourced incidents | Inconsistent | Coder's reference kept, no cited lag |
| Old news still true | `current`, age undefined | `current`; `capability_since` dates the named example |
| Two sources | Later one recorded | Both recorded; lag uses the older |
| Contested claims | `unclear` | New `contested` status |
| Incident accuracy | In free text | New flag and note |
| Quote length | One quote, 60 words | Adds an optional `supporting_quote` |
| Relevance | Three values | Adds `procedural` |

## 7. Clarifications made during the full run

Added to the coder brief after the first two batches, where coders raised the
same questions. Batches 001 to 014 were coded before these were written.

- **Data centres.** A data-centre claim is coded only where the speaker ties
  that data centre or figure to AI.
- **Statements read out for someone else** count as endorsed unless the
  speaker distances themselves.
- **General harm claims** with no figure, source or incident are rhetoric and
  are excluded.
