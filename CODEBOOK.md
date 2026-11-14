# Codebook v0.1 (pilot)

Research question: how stale is the AI evidence that UK and Australian
parliamentarians rely on when they describe what AI can do?

This codebook tells a coder how to turn one Hansard speech into zero or more
coded **capability claims**. It is written for the pilot and is expected to
change after review.

## 1. Unit of analysis

A **capability claim** is an assertion, made or endorsed by the speaker, about
what AI systems can do, cannot do, how well they do it, how they behave, or how
fast their capability is changing.

Test for inclusion: *could a well-informed person say whether this was a fair
description of AI systems at a particular date?* If yes, it is a claim.

### Claim types

| `claim_type` | Meaning | Example |
|---|---|---|
| `capability` | AI can do X, or does X at some level | "AI can now read mammograms as accurately as two radiologists." |
| `limitation` | AI cannot do X, or does X unreliably | "These chatbots simply make things up." |
| `trajectory` | Rate of progress, or a forecast of future capability | "We may have human-level AI within five years." |
| `incident` | A specific thing a specific system did | "Grok produced sexualised images of real women on request." |

### Exclude

- Adoption, usage, market, investment, and economic-impact figures ("a third of
  firms use AI", "AI will add £400 billion to GDP").
- Labour-market forecasts, unless phrased as what AI can do ("AI can already do
  the work of a junior solicitor" is in; "AI will displace 3 million jobs" is out).
- Energy, water, and infrastructure facts.
- Bare deployment facts with no performance content ("the ATO uses AI in audits").
- Policy descriptions, normative statements, and rhetorical generalities
  ("AI is transforming everything").
- Claims the speaker reports only in order to reject them.

Log up to three excluded borderline items per speech under `near_misses`.
These drive codebook revisions.

### Splitting and merging

- One claim per distinct proposition. A speech may yield several claims.
- A proposition repeated within a speech is coded once.
- A list ("AI can write, code, and draw") is one claim unless items have
  different evidence.

## 2. Speech-level fields

| Field | Values |
|---|---|
| `speech_id` | Copied from the input. |
| `ai_relevance` | `substantive` (AI is a topic of the speech), `passing` (AI is mentioned in a list or aside), `false_positive` (the match is not about artificial intelligence). |
| `claims` | List of claim objects. May be empty. |
| `near_misses` | List of `{ "quote": ..., "reason": ... }`. May be empty. |
| `coder_notes` | Free text. Use it for doubts about the codebook. |

## 3. Claim-level fields

### Identification

| Field | Rule |
|---|---|
| `quote` | Verbatim, contiguous excerpt from the speech `text`. At most 60 words. It must be an exact substring: copy, do not retype or fix punctuation. |
| `claim` | One neutral sentence restating the proposition. |
| `claim_type` | `capability`, `limitation`, `trajectory`, `incident`. |
| `domain` | One of `general`, `health`, `education`, `defence_security`, `cyber`, `child_safety`, `deepfakes_misinfo`, `creative_copyright`, `work`, `public_services`, `science`, `finance`, `other`. |
| `named_system` | The model, product, or company the claim is about, if the speaker names one. Otherwise `null`. |

### Evidence basis

`evidence_basis` records what the speaker offers in support of *this* claim.

| Value | Rule |
|---|---|
| `cited_source` | The speaker names an identifiable source: a report, study, article, organisation, named expert, company announcement, inquiry, or court case. |
| `vague_attribution` | "Experts say", "studies show", "we have heard": a source is gestured at but cannot be identified from the speech. |
| `personal_experience` | The speaker's own use, or a constituent's or visit's first-hand account. |
| `none` | Bare assertion. |

### Source fields

Fill these when `evidence_basis` is `cited_source`. Also fill them when the
speaker does not name a source but the coder can identify it with high
confidence (for example a distinctive statistic). Otherwise set all to `null`.

| Field | Rule |
|---|---|
| `source_name` | Title of the document or a short description ("International AI Safety Report 2026"). |
| `source_org` | Publishing organisation or author. |
| `source_type` | `government`, `parliamentary`, `academic`, `company`, `news`, `ngo_thinktank`, `international_body`, `legal`, `expert_statement`, `book`, `other`. |
| `source_identified_by` | `named_in_speech` or `inferred_by_coder`. |
| `source_date` | Publication date: `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`. Use the most precise form that is supported. `null` if it cannot be dated. |
| `source_date_basis` | `stated_in_speech`, `web_verified` (a page found by search confirms it), `coder_recall` (from the coder's own knowledge, unverified), or `unknown`. |
| `source_url` | A URL the coder actually retrieved or saw in search results. Never construct or guess a URL. `null` if none. |
| `source_notes` | Anything that affects the date: multiple editions, which edition is meant, doubts. |

Date the source the speaker *cites*, not the research underneath it. A 2026
news article about a 2024 study is dated 2026; say so in `source_notes`.

If a source has editions (annual reports, index releases), choose the latest
edition published before the debate unless the speech indicates another.

### Implied vintage

Every claim gets a vintage judgement, sourced or not. The question is: **when
was this description of AI last current?**

| `vintage_status` | Rule | `vintage_date` |
|---|---|---|
| `current` | Still a fair description of AI systems at the coder's knowledge horizon. | `null` |
| `outdated` | Was once fair, but was superseded before the debate. | Last month in which it was still fair, `YYYY-MM`. |
| `never_accurate` | Was not a fair description at any date (overclaim, or misunderstanding). | `null` |
| `dated_event` | `incident` claims: the event itself is the evidence. | Date the incident occurred or was first reported. |
| `forecast` | The claim is about the future. Vintage does not apply. | `null` |
| `unclear` | Too vague to assess, or outside what the coder can verify. | `null` |

Rules:

- A "can do X" claim stays `current` while X remains true. It becomes
  `outdated` only if the wording asserts a ceiling that has since been passed
  ("the best models can only…", "AI still cannot…").
- A "cannot do X" claim is `outdated` from the month public systems could do X.
- Judge against generally available frontier systems, not the weakest product.
- `vintage_rationale`: one or two sentences. For `outdated`, name the
  development that superseded the claim.
- `vintage_confidence`: `high`, `medium`, `low`.

`capability_since` (exploratory, `capability` claims only): the earliest month
in which the stated capability was true of public systems, `YYYY-MM`. It
measures how old the "news" is, even when the claim is still true. Use `null`
when it cannot be estimated.

### Knowledge horizon

The debates run later than the coder's training data. Speeches may mention
models, reports, and events the coder has never seen.

- Never mark something false or outdated because it is unfamiliar. Search.
- If a post-horizon claim cannot be verified, use `unclear`.
- Record the horizon used in `coder_notes` if it affected a judgement.

## 4. Derived measures

Computed in `legislag/build.py`, not by coders.

- **Cited lag** = debate date − `source_date`, for sources with
  `source_identified_by` = `named_in_speech` only. A source the coder
  identified for an unsourced claim is kept as a reference and gets no lag. A month- or year-precision date
  is placed at the middle of its period. If the debate falls inside that
  period, the middle of the part before the debate is used. A source is never
  dated after the speech that cites it.
- **Implied lag** = debate date − `vintage_date` for `outdated` and
  `dated_event` claims. `current` claims have lag zero. This is a floor: a
  claim can be current at the coder's horizon yet stale by the debate.
- Claims with `forecast`, `never_accurate`, or `unclear` status have no
  implied lag and are reported as counts.

## 5. Output format

One JSON object per line, one line per speech, including speeches with no claims.

```json
{
  "speech_id": "uk-lords:2026-07-09b.373.0",
  "ai_relevance": "substantive",
  "claims": [
    {
      "quote": "…exact words from the speech…",
      "claim": "Frontier models can autonomously complete multi-hour software tasks.",
      "claim_type": "capability",
      "domain": "general",
      "named_system": null,
      "evidence_basis": "cited_source",
      "source_name": "International AI Safety Report 2026",
      "source_org": "International AI Safety Report (chair: Yoshua Bengio)",
      "source_type": "international_body",
      "source_identified_by": "named_in_speech",
      "source_date": "2026-02",
      "source_date_basis": "web_verified",
      "source_url": "https://…",
      "source_notes": null,
      "vintage_status": "current",
      "vintage_date": null,
      "vintage_rationale": "Consistent with published task-horizon evaluations.",
      "vintage_confidence": "medium",
      "capability_since": "2025-03"
    }
  ],
  "near_misses": [
    { "quote": "…", "reason": "Adoption statistic, not a capability claim." }
  ],
  "coder_notes": ""
}
```

The example values illustrate the format only. They are not findings.

## 6. Open questions from the pilot

Raised by the coders on the 100-speech pilot. None is settled. Each needs a
ruling before the full run.

1. **Scope of the unit.** The definition admits only claims about what AI can
   do. Coders logged 127 near misses. Several carried dated sources: a 2024
   sector study, an IMF exposure estimate, opinion polls, a re-shared 2014
   quotation. Decide whether the unit should widen to any empirical claim
   about AI that rests on a source.
2. **Incident date.** "Occurred or first reported" is ambiguous. One incident
   occurred on 18 June 2026 and was disclosed on 24 September. Coders used
   the occurrence date. The disclosure date is arguably the right one for
   evidence age, since nobody could cite it earlier.
3. **Sources for unsourced incidents.** Coders disagreed on whether to fill
   the source fields when a speaker describes a well-known incident without
   naming a source. The pilot keeps such sources as references and gives them
   no cited lag.
4. **Hedged and presupposed claims.** "AI could help…", "there is an
   opportunity to use AI…", and capabilities presupposed inside a policy
   sentence were mostly excluded. The codebook is silent.
5. **Risk estimates.** Statements about what people believe ("a 10 per cent
   risk", "builders think it could kill us all") were coded as trajectory
   claims. They describe opinion, not systems.
6. **Generic rate-of-progress remarks.** "This technology is evolving fast"
   was excluded as rhetoric. The trajectory definition could admit it.
7. **What counts as AI.** Recommender algorithms and rules-based assessment
   tools were excluded unless the speaker called them AI.
8. **Old news that is still true.** A claim such as "some AI systems already
   exceed human abilities, such as AlphaFold" is `current` under the rules.
   `capability_since` captures its age, but has no threshold and rests on
   coder recall.
9. **Contested claims.** There is no status for "broadly true but overstated".
   One such claim was coded `unclear`.
10. **Two sources, one claim.** The single `source_date` field holds the later
    source.
11. **Incident accuracy.** There is no field for an incident that is alleged
    rather than established, or described loosely by the speaker.
12. **Quote length.** The 60-word contiguous limit is tight for narrated
    incidents, where the system name and the date sit in earlier sentences.
13. **`ai_relevance`.** Needs a value for procedural speeches under an AI
    heading, and a clearer line between `substantive` and `passing`.
14. **Text read into the record.** Motions, letters, and reports read out by a
    speaker are not clearly "made or endorsed by the speaker".
