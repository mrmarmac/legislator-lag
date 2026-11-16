# Connector literature search: Consensus and SciSpace

Searches run 15 November 2026. Only Consensus (`mcp__Consensus__search`) and SciSpace (`mcp__SciSpace__search`, plus one `mcp__SciSpace__fetch`) were used. No filters were applied. Each paper below is described only from the abstract or snippet the connector returned. Where a number is given, it is what the abstract reports. Citation counts are as each connector returned them on the day, and the two connectors often disagree.

Neither connector was unavailable. Consensus returned a rate-limit error on two of its first three parallel calls; both queries were rerun one at a time later and worked.

---

## 1. Search log

| # | Connector | Query text | Results | Failed? |
|---|---|---|---|---|
| C1 | Consensus | use of research evidence by legislators in parliamentary debates content analysis Hansard | 0 (first attempt) | Yes, rate limit. Rerun as C1b |
| C2 | Consensus | age of evidence cited in policy debate time lag from publication to political use | 15 | No |
| C3 | Consensus | proportion of claims citing sources in political speeches evidence types argument mining | 0 (first attempt) | Yes, rate limit. Rerun as C3b |
| C1b | Consensus | use of research evidence by legislators in parliamentary debates content analysis Hansard (rerun) | 15 | No |
| C3b | Consensus | proportion of claims citing sources in political speeches evidence types argument mining (rerun) | 15 | No |
| C4 | Consensus | artificial intelligence in parliamentary debates discourse analysis legislators | 15 | No |
| C5 | Consensus | media coverage agenda-setting effect on parliamentary questions time lag | 15 | No |
| C6 | Consensus | check-worthy claim detection automated fact-checking political debates large language models | 15 | No |
| C7 | Consensus | large language models as annotators for content analysis reliability validity compared to human coders bias prompt sensitivity | 15 | No |
| C8 | Consensus | unitizing reliability content analysis identifying units claims intercoder agreement | 12 | No |
| C9 | Consensus | language model knowledge cutoff outdated information temporal misalignment detecting stale facts | 15 | No |
| C10 | Consensus | source credibility reliability scoring provenance citation verification tools; AI decision support for legislatures | 15 | No |
| C11 | Consensus | accuracy of factual claims made by politicians in parliament misinformation exaggeration fact-checking legislators | 15 | No |
| C12 | Consensus | references to scientific evidence in parliamentary speeches measured with large language models (follow-up) | 15 | No |
| C13 | Consensus | LLM coders over-identify codes overcoding false positives compared with human content analysis (follow-up) | 12 | No |
| C14 | Consensus | artificial intelligence debates in UK House of Commons, House of Lords or Australian Parliament (follow-up) | 12 | No |
| S1 | SciSpace | How do legislators use research evidence and cite sources in parliamentary debates, based on content analysis of Hansard records? | 20 | No |
| S2 | SciSpace | How old is the evidence that politicians cite in policy debates, and what is the time lag between publication and political use? | 20 | No |
| S3 | SciSpace | What share of politicians' claims in speeches cite a source, and how is evidence type detected through argument mining in political text? | 20 | No |
| S4 | SciSpace | How do parliaments and legislators discuss artificial intelligence in parliamentary debates? Discourse or content analysis of AI in parliament or congress. | 20 | No |
| S5 | SciSpace | How quickly do legislators take up news media coverage in parliamentary questions and speeches? Media agenda-setting effects on parliament. | 20 | No |
| S6 | SciSpace | How well do automated systems detect check-worthy factual claims and fact-check statements in political speeches and parliamentary debates? | 20 | No |
| S7 | SciSpace | How reliable and valid are large language models as annotators for content analysis compared with human coders, including bias, prompt sensitivity and failures? | 20 | No |
| S8 | SciSpace | What are the problems of unitizing and inter-coder reliability when identifying claims or units in content analysis? | 20 | No |
| S9 | SciSpace | Can language models recognize that information is outdated, and how do knowledge cutoffs cause temporal staleness in their answers? | 20 | No |
| S10 | SciSpace | How accurate are politicians' factual claims in parliament, and how common is misinformation or exaggeration in parliamentary debate? | 20 | No |
| S11 | SciSpace | What tools exist for source reliability scoring, provenance tracking and citation verification, including AI decision support for legislatures and government? | 20 | No |
| S12 | SciSpace | How often do politicians attribute factual claims to sources versus making unsupported assertions, measured through content analysis of sourcing or attribution in political speech? (follow-up) | 20 | No |
| S13 | SciSpace | How accurately can large language models extract and identify factual claims from text, and do they over-generate or over-include claims compared with human annotators? (follow-up) | 20 | No |
| S14 | SciSpace | How has the use of scientific evidence or evidence-based language in legislative speeches changed over time, measured computationally? (follow-up) | 20 | No |
| S15 | SciSpace | How many days after news coverage do members of parliament raise an issue in parliamentary questions? Time lag of media effects on parliament. (follow-up) | 20 | No |
| S16 | SciSpace | How do members of the UK or Australian parliament talk about artificial intelligence and generative AI in Hansard debates? (follow-up) | 20 | No |
| S17 | SciSpace (fetch) | Full record for "Who Refers to Science?" (id `who-refers-to-science-understanding-the-salience-of-w69ox9a2bfex`) | 1 record | No |

Totals: 14 Consensus searches returned results, and 2 more attempts hit the rate limit and were rerun. SciSpace ran 16 searches and 1 fetch.

---

## 2. Shortlist: 30 new papers

"Both" means both connectors returned the paper. In that case both links and both citation counts are given.

### Topic 1: How legislators use research evidence in debate

1. **[Who Refers to Science? Understanding the Salience of Scientific Evidence in Parliamentary Debates](https://scispace.com/papers/who-refers-to-science-understanding-the-salience-of-w69ox9a2bfex?utm_source=claude&utm_medium=tool)**: Daniel Wiesner, 2026. Journal Article (OSF; DOI 10.17605/osf.io/ct62f per the fetched record). No citation count given. *SciSpace* (S1, S2, S3, S14; fetched).
   - Finding: Uses LLMs to code 30,000 speeches (2018–2021) from six European chambers, including the UK, for whether a speech uses scientific evidence and what its main policy issue is. Multilevel models find institutional roles, policy contexts and organisational routines matter more than country or ideology.
   - Relevance: This is the nearest published design to ours: LLM coding of evidence references in floor speeches, including the UK Commons. It works at speech level and asks "science or not", not claim level with a four-way evidence type, and it measures neither source age nor claim currency.

2. **[Uses of Research Evidence in the State Legislative Process to Promote Active Environments in Minnesota](https://consensus.app/papers/details/w:cdb56f6a-0c34-4629-b031-e4f97c5a3a99/?utm_source=claude_desktop)**: Hanna A. Kite et al., 2013. *American Journal of Health Promotion*. 11 citations. *Consensus* (C1b).
   - Finding: Content analysis of 2007–2011 testimony and legislative documents. The abstract reports that 36% of the sample contained research evidence and 88% contained non-research-based information.
   - Relevance: This is a direct prior "sourcing rate" figure for legislative material, though for testimony and documents rather than floor speeches. It is a useful comparator for our 51% no-evidence figure.

3. **[Millä tiedolla päätetään? Tieto Suomen eduskunnan sivistysvaliokunnan liikuntapoliittisessa työssä](https://consensus.app/papers/details/w:fb10d0f1-5e0b-4a3a-8816-e4f48247ff04/?utm_source=claude_desktop)**: Minttu Korsberg, 2026. *Hallinnon Tutkimus*. 0 citations. *Consensus* (C1b).
   - Finding: A quantitative content analysis of 70 expert opinions to a Finnish parliamentary committee. The abstract reports that the vast majority of arguments were presented as "general knowledge" with no explicit source, and only a small proportion drew on research.
   - Relevance: It matches our finding that unsourced claims dominate, but the speakers are expert witnesses, not MPs. The paper is in Finnish.

4. **[Responding to research evidence in Parliament: A case study on selective education policy](https://consensus.app/papers/details/w:a56327e3-3cf5-4b66-b727-3a1be8475005/?utm_source=claude_desktop)**: Alan Bainbridge et al., 2022. *Review of Education*. 7 citations. *Both* (C1b; S1 [SciSpace link](https://scispace.com/papers/responding-to-research-evidence-in-parliament-a-case-study-cnjgldch?utm_source=claude&utm_medium=tool), which lists the venue as "Revista Educación").
   - Finding: NVivo thematic analysis of 11 UK parliamentary debates on grammar schools. Argumentative analysis finds rhetorical tools used to avoid empirical evidence, including a "moral sidestep".
   - Relevance: This is a UK Hansard case study of how claims are warranted. It is qualitative and limited to one policy, so it is a contrast to our cross-topic counts.

### Topic 2: Age, recency and time lag of evidence in policy

5. **[COVID-19 education policy often relied on older research despite available new evidence](https://consensus.app/papers/details/w:2dd24099-d322-410a-9f8c-390b2aa7ee00/?utm_source=claude_desktop)**: Basil Mahfouz et al., 2026. *STAR Protocols*. 2 citations on Consensus, 1 on SciSpace. *Both* (C2; S2 [SciSpace link](https://scispace.com/papers/covid-19-education-policy-often-relied-on-older-research-l3it6jsbnv89?utm_source=claude&utm_medium=tool)).
   - Finding: Uses LM embeddings to find newer studies related to those cited in policy documents. The abstract reports that policy documents often kept citing pre-pandemic research when similar post-2020 studies were already available.
   - Relevance: This is a scalable measure of "currency" for cited evidence in policy documents. It points the opposite way to our short 30-day median, which may reflect speech rather than document genres, or AI's news-driven sourcing.

6. **[Science cited in policy documents: Evidence from the Overton database](https://consensus.app/papers/details/w:0fef8dbd-fe82-45bc-af0d-8936e7f3cef3/?utm_source=claude_desktop)**: Zhichao Fang et al., 2024. *arXiv (Cornell University)*. 22 citations on Consensus, 15 on SciSpace. *Both* (C2; S2 [SciSpace link](https://scispace.com/papers/science-cited-in-policy-documents-evidence-from-the-overton-2m0r33cpxt?utm_source=claude&utm_medium=tool)).
   - Finding: The abstract reports that 3.9% of 18 million publications from 2010–2019 were cited in Overton policy documents, and that policy citations show a citation delay toward newly published work.
   - Relevance: This is a large-scale baseline that policy citation lags publication. Our median of days rather than years cuts against it, so the paper should explain why: news and preprints rather than journals, or AI's pace.

7. **[How recent is recent? Retrospective analysis of suspiciously timeless citations](https://consensus.app/papers/details/w:cf7ea556-dc14-457e-a0cd-23e67a3aa350/?utm_source=claude_desktop)**: Alejandro Díez Vidal et al., 2025. *BMJ*. 5 citations. *Consensus* (C2).
   - Finding: In 1,000 biomedical articles, the abstract reports that studies described as "recent" had a median lag of 4 years (mean 5.53, range 0–37), and that 17.7% were at least 10 years old.
   - Relevance: This is a method template for coding "recent" claims against the actual publication date of the source. It is biomedical, not political, but closely parallels our currency coding.

8. **[Evidence-based policymaking in the legislatures: timeliness and politics of evidence in Finland](https://consensus.app/papers/details/w:c3565be7-e5ac-4200-907a-37ff17be6634/?utm_source=claude_desktop)**: Ville Aula, 2023. *Policy & Politics*. 7 citations on Consensus, 2 on SciSpace. *Both* (C2, C1b; S2 [SciSpace link](https://scispace.com/papers/evidence-based-policymaking-in-the-legislatures-timeliness-a06scvaf?utm_source=claude&utm_medium=tool)).
   - Finding: An interview case study of the Finnish Parliament. It finds that timeliness is dominated by short-term reactions to bills and that the window for timely evidence "can vary from months to days".
   - Relevance: It gives a qualitative mechanism for why legislators reach for very recent sources, which fits our 30-day median.

### Topic 3: Share of political claims that cite a source; evidence types

9. **[Because I Said So: A Functional Theory Analysis of Evidence in Political TV Spots](https://scispace.com/papers/because-i-said-so-a-functional-theory-analysis-of-evidence-3an7qi65xj?utm_source=claude&utm_medium=tool)**: Jayne R. Henson, William L. Benoit, 2010. *Speaker and Gavel*. 6 citations. *SciSpace* (S3, S12).
   - Finding: The abstract reports that 8% of themes in US political TV advertising from 1952–2008 were supported by evidence, defined as identifying a source for a claim, and that 65% of evidenced utterances were attacks.
   - Relevance: This is the clearest prior "share of claims citing a source" figure in political speech, though for campaign ads. It is useful for showing that our 49% with some evidence is high by that standard.

10. **[Computational analysis of US congressional speeches reveals a shift from evidence to intuition](https://consensus.app/papers/details/w:331720a1-4508-4dfa-8a55-b211591bda0a/?utm_source=claude_desktop)**: Segun Taofeek Aroyehun et al., 2025. *Nature Human Behaviour*. 22 citations. *Both* (C12; S12, S14 [SciSpace preprint link](https://scispace.com/papers/computational-analysis-of-us-congressional-speeches-reveals-3k70xk8wdi?utm_source=claude&utm_medium=tool), 2024, 8 citations).
    - Finding: Congressional speeches from 1879 to 2022. The abstract reports that evidence-based language has declined since the mid-1970s, alongside lower legislative productivity and higher polarisation.
    - Relevance: This is a high-profile, lexicon and embedding style measure of evidence orientation in floor speech. It contrasts with our claim-level, source-dated coding and could be cited as the "language-style" alternative.

11. **[Epistemic orientation in parliamentary discourse is associated with deliberative democracy](https://consensus.app/papers/details/w:9705f8f9-ac5f-4f73-8f76-89f5ed81c2af/?utm_source=claude_desktop)**: Segun Aroyehun et al., 2026. *arXiv (Cornell University)*. 3 citations on Consensus, 1 on SciSpace. *Both* (C12; S14 [SciSpace link](https://scispace.com/papers/epistemic-orientation-in-parliamentary-discourse-is-hx9ijmgus1jo?utm_source=claude&utm_medium=tool)).
    - Finding: Applies an Evidence-Minus-Intuition score, derived from LLM ratings and embeddings, to 15 million parliamentary speech segments from 1946–2025 across seven countries. It reports positive associations with deliberative democracy and governance.
    - Relevance: This is an LLM-based measure of evidence in parliamentary speech at very large scale. It is coarser than ours, with no named-source age or currency, but it is the main computational competitor to cite.

12. **[Invoking the News in Parliament: Journalistic Media References as External Discursive Resources in Portuguese Parliamentary Speech, 1976–2025](https://consensus.app/papers/details/w:82f173e1-8286-4acd-b06b-c4f3e4d1215d/?utm_source=claude_desktop)**: Manuel João Cruz et al., 2026. *Journalism and Media*. 0 citations. *Consensus* (C3b).
    - Finding: Rule-based detection across 726,153 plenary interventions, with manual coding of strict cases. It finds explicit journalistic references are rare and declining, and when used are mainly evidentiary or agenda-introducing.
    - Relevance: This is directly about news as a named source in parliamentary speech. Its finding that news references are "rare" may contrast with our recent, news-heavy named sources on AI; worth checking against our source-type mix.

13. **[Pilotstudie zur Faktenintensität und Genauigkeit in Bundestags-Plenardebatten: Eine empirische Anwendung der Rede von Marc Biadacz (CDU/CSU) in der 94. Sitzung der 21. Wahlperiode](https://scispace.com/papers/pilotstudie-zur-faktenintensitat-und-genauigkeit-in-fx1z79lsgo93?utm_source=claude&utm_medium=tool)**: Nils Michalke, 2026. Repository. No citation count given. *SciSpace* (S3, S10, S12).
    - Finding: Applies a Transparency and Evidence Index (verifiable vs. non-verifiable statements; factual correctness, evidence quality, context integrity) to one Bundestag speech. The TL;DR reports 18% evidence density and an 85.19% accuracy score.
    - Relevance: This is conceptually close (evidence density plus accuracy in plenary speech) but is a one-speech, non-peer-reviewed repository item. Cite with caution, if at all.

### Topic 4: How parliaments discuss AI

14. **[When Politicians Talk AI: Issue‐Frames in Parliamentary Debates Before and After ChatGPT](https://consensus.app/papers/details/w:1c1a785d-d10b-46d0-9115-1d969670be47/?utm_source=claude_desktop)**: Viktor Suter et al., 2025. *Policy & Internet*. 12 citations on Consensus, 5 on SciSpace. *Both* (C4, C14; S4, S16 [SciSpace link](https://scispace.com/papers/when-politicians-talk-ai-issue-frames-in-parliamentary-sjfj6jlzoqdn?utm_source=claude&utm_medium=tool)).
    - Finding: A study of AI framing in the US Congress, EU Parliament, Singapore and Swiss assembly from 2014 to 2024. It reports a steep surge after ChatGPT, driven by ethics and regulation, with distinct national priorities.
    - Relevance: This is the standard comparative frame analysis of AI in legislatures. It covers frames, not factual claims or evidence, and does not cover the UK or Australia.

15. **[Perspectives on AI in the British and Slovenian parliament](https://consensus.app/papers/details/w:8ad13e46-43db-4191-aa5e-642fc12a8ad4/?utm_source=claude_desktop)**: Ajda Pretnar Žagar et al., 2025. *Digital Humanities in the Nordic and Baltic Countries Publications*. 1 citation. *Both* (C4, C14; S4, S16 [SciSpace link](https://scispace.com/papers/perspectives-on-ai-in-the-british-and-slovenian-parliament-cmqkn7pmi5zc?utm_source=claude&utm_medium=tool)).
    - Finding: Semantic networks of AI debates from 2015 to 2024. The UK debate is described as more sectoral and business-focused, Slovenia's as linked to EU policy, education and digitisation.
    - Relevance: This is the only returned study of AI debate in UK Hansard. It is descriptive and lexical, with no claim or evidence coding.

16. **[Meeting the Coming Wave: The Emerging Politics of AI and Work across 33 Parliaments](https://consensus.app/papers/details/w:20163a64-667f-4cdd-987f-de921bc9344a/?utm_source=claude_desktop)**: Juliana Chueri et al., 2026. *arXiv (Cornell University)*. 0 citations. *Both* (C14; S4 [SciSpace link](https://scispace.com/papers/meeting-the-coming-wave-the-emerging-politics-of-ai-and-work-um387xkqfp6l?utm_source=claude&utm_medium=tool)).
    - Finding: 1,514,950 speeches from 33 parliaments (2023–2026). The abstract reports compensation at 2.3% of response-frame mentions, enablement and investment at 55.2%, regulation at 21.8% and training at 20.6%.
    - Relevance: This is a recent, large-scale and overlapping period for AI speech. It is useful context for which kinds of AI claims dominate, and a check on whether our claim-type distribution is plausible.

### Topic 5: Media agenda-setting and parliamentary uptake speed

17. **[Studying the Tango](https://consensus.app/papers/details/w:63e90c73-9331-45c4-9c33-b177267c52c6/?utm_source=claude_desktop)**: Peter Van Aelst et al., 2013. *Journalism Studies*. 78 citations on Consensus. SciSpace lists it as 2014 with 51 citations, titled "Studying the tango: an analysis of parliamentary questions and press coverage in the Netherlands". *Both* (C5; S5, S15 [SciSpace link](https://scispace.com/papers/studying-the-tango-an-analysis-of-parliamentary-questions-4mhsktbohk?utm_source=claude&utm_medium=tool)).
    - Finding: Dutch press coverage and parliamentary questions from 1995 to 2010. A micro-analysis shows most oral questions "can be traced back to coverage in the days before", often with media relaying information from other sources.
    - Relevance: This is the best direct prior evidence that parliamentary uptake of news runs on a scale of days. That supports reading our 30-day median as normal news-cycle behaviour rather than special to AI.

18. **[Explicating the Time Factor in Media Agenda-Setting Research](https://consensus.app/papers/details/w:e4bd466a-5a66-45dd-8704-3b915959c6cb/?utm_source=claude_desktop)**: Лэй Гуо et al., 2026. *Communication Research*. 2 citations. *Both* (C5; S15 [SciSpace link](https://scispace.com/papers/explicating-the-time-factor-in-media-agenda-setting-research-ewv39kxgod5f?utm_source=claude&utm_medium=tool), authors listed as L. Guo, Yiyan Zhang, Yi Li).
    - Finding: A systematic review of 1,444 agenda-setting articles from 1972 to 2024. The abstract reports an average of 55 days of media exposure for aggregate effects, 28 days at the individual level, and about a 7-day public response delay.
    - Relevance: It gives a benchmark lag from the literature (weeks) to set against our 30-day median source age, though it concerns public rather than legislator agendas.

### Topic 6: Check-worthy claims and automated fact-checking of political speech

19. **[Automated Fact-Checking of Claims in Argumentative Parliamentary Debates](https://scispace.com/papers/automated-fact-checking-of-claims-in-argumentative-gv9327a4sv?utm_source=claude&utm_medium=tool)**: Nona Naderi, Graeme Hirst, 2018. Proceedings Article. 26 citations. *SciSpace* (S6, S10).
    - Finding: Classifies true, false, stretch and dodge statements in Canadian Parliament question periods using transfer from a US fact-check corpus. The abstract reports dodge detection at up to 82.57% F1 (binary).
    - Relevance: This is rare prior work on veracity labels for Westminster-style parliamentary claims. Its "stretch" class is close to our "overstatement" category.

### Topic 7: LLMs as coders (critical findings)

20. **[Analyzing Nurse Sentiment in a Dutch Regional Newspaper During the COVID-19 Pandemic: Comparative Content Analysis of GPT-5, Gemini 2.5 Pro, and Human Coding](https://consensus.app/papers/details/w:67fe0575-6d63-487c-9ef4-3cede8d04cad/?utm_source=claude_desktop)**: Bram Van den Berkmortel et al., 2026. *Journal of Medical Internet Research*. 0 citations. *Both* (C13; S7 [SciSpace link](https://scispace.com/papers/analyzing-nurse-sentiment-in-a-dutch-regional-newspaper-al2pkjb5s2zs?utm_source=claude&utm_medium=tool)).
    - Finding: In deductive coding, the abstract reports that both models "systematically overcoded" (181 and 183 codes vs 138 human), with α of 0.487 and 0.507 against the human baseline. It argues that LLMs default to semantic presence rather than interpretive significance.
    - Relevance: This independently replicates our main instrument-validity finding, that LLM coders over-include (our about 14%). Cite it directly.

21. **[Benchmarking AI and human text classifications in the context of newspaper frames: A multi-label LLM classification approach](https://consensus.app/papers/details/w:7f9632b7-b697-4f76-ba82-d0b8de003f29/?utm_source=claude_desktop)**: Alexander Tripp, 2025. *Research & Politics*. 6 citations. *Both* (C13; S7 [SciSpace link, 2024 version](https://scispace.com/papers/benchmarking-ai-and-human-text-classifications-in-the-4fjcq92vdb?utm_source=claude&utm_medium=tool)).
    - Finding: Benchmarks ChatGPT and Claude against undergraduate coders on Spanish immigration articles and reports that "LLMs tend toward false positive errors".
    - Relevance: This is a second, political-science-venue confirmation of over-inclusion.

22. **[Self-reflection in Automated Qualitative Coding: Improving Text Annotation through Secondary LLM Critique](https://consensus.app/papers/details/w:0ffa0188-9f42-4590-b7c2-555961e08202/?utm_source=claude_desktop)**: Zackary Okun Dunivin et al., 2026. *arXiv (Cornell University)*. 0 citations. *Consensus* (C13).
    - Finding: A human audit of 360 positive annotations found first-line LLM false-positive rates of 8% to 54% despite test F1 of 0.74–1.00. A second LLM critic improved F1 by 0.04–0.25.
    - Relevance: It shows high validation F1 can mask false positives, which is our problem exactly. It also offers a cheap fix (a critic pass on positives) we could propose or test.

23. **[Agreement Is Not Quality: Blind Expert Verification of Human and LLM Qualitative Coding When Human Consensus Is Not Ground Truth](https://consensus.app/papers/details/w:e9f7535c-3025-448e-a239-ae1823c50e85/?utm_source=claude_desktop)**: Alex Liu et al., 2026. *arXiv (Cornell University)*. 3 citations. *Both* (C13; S7 [SciSpace link](https://scispace.com/papers/agreement-is-not-quality-blind-expert-verification-of-human-5afcp57zfv10?utm_source=claude&utm_medium=tool)).
    - Finding: Human–LLM Jaccard was 0.30 vs human–human 0.52, yet a blind expert preferred human and LLM codes at indistinguishable rates (51.5% vs 48.5%).
    - Relevance: This cuts against treating our single human adjudicator as ground truth. It supports reporting the adjudication protocol as verification rather than agreement.

### Topic 8: Unitizing and claim identification

24. **[Natural Sentences as Valid Units for Coded Political Texts](https://scispace.com/papers/natural-sentences-as-valid-units-for-coded-political-texts-16hirals8f?utm_source=claude&utm_medium=tool)**: Thomas Däubler, Kenneth Benoit, Slava Mikhaylov, 2012. *British Journal of Political Science*. 86 citations. *SciSpace* (S8).
    - Finding: Coder-identified "quasi-sentences" (as in the Manifesto Project) make text analysis fundamentally unreliable. Natural sentences give perfectly reliable unitization with no measurable loss of content validity.
    - Relevance: Our 14% over-inclusion is a unitizing failure. This paper argues for fixed units, which bears directly on whether "claim" should be coder-defined.

### Topic 9: Knowledge cutoffs and staleness in LLMs

25. **[The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations](https://consensus.app/papers/details/w:e35cd189-85bb-48ff-ac47-acd355dcf375/?utm_source=claude_desktop)**: Rania Elbadry et al., 2026. *arXiv (Cornell University)*. 2 citations. *Both* (C9; S9 [SciSpace link](https://scispace.com/papers/the-geometry-of-forgetting-temporal-knowledge-drift-as-an-hyuw5egaq44t?utm_source=claude&utm_medium=tool)).
    - Finding: The abstract reports that LLMs confidently produce outdated answers and that uncertainty-based methods (entropy and others) sit near chance (0.49–0.57) at detecting this. A probe trained on drift labels reaches AUROC 0.83–0.95.
    - Relevance: This directly undermines asking an LLM coder, from its own knowledge, whether a claim is current. Our "currency" coding needs external dated evidence.

26. **[DyKnow: Dynamically Verifying Time-Sensitive Factual Knowledge in LLMs](https://consensus.app/papers/details/w:9ea2c69e-4aa3-4dc0-ae0b-53d4b6a351bf/?utm_source=claude_desktop)**: Seyed Mahed Mousavi et al., 2024. *Findings of the Association for Computational Linguistics: EMNLP (Findings of EMNLP)*. 64 citations. *Both* (C9; S9 returned the same authors' version as ["Is Your LLM Outdated? Benchmarking LLMs & Alignment Algorithms for Time-Sensitive Knowledge"](https://scispace.com/papers/is-your-llm-outdated-benchmarking-llms-alignment-algorithms-4fny3t8npg?utm_source=claude&utm_medium=tool), 2024, 11 citations).
    - Finding: Across 24 LLMs checked against Wikidata, outdatedness is a critical problem, answers vary with slight prompt changes, and knowledge-editing methods barely help.
    - Relevance: It supports the claim that LLM coders cannot be trusted on currency without retrieval. The prompt-sensitivity finding also bears on our coder stability.

### Topic 10: Source reliability, provenance and verification tools

27. **[Accuracy and Political Bias of News Source Credibility Ratings by Large Language Models](https://consensus.app/papers/details/w:e5dbc9df-3c4a-49e7-b270-d0771ee14ed4/?utm_source=claude_desktop)**: Kai-Cheng Yang et al., 2025. *ACM Web Science Conference (WebSci)*. 119 citations. *Consensus* (C10).
    - Finding: Nine LLMs rating news outlets agree with each other (ρ = 0.79) but only moderately with experts (ρ = 0.50). They show a liberal bias by default, and partisan role prompts induce congruent bias.
    - Relevance: If we extend to scoring the reliability of named sources with LLMs, this is the caution to cite. It bears on any "source reliability" add-on for the sprint.

### Topic 11: Accuracy and overstatement of politicians' claims

28. **[Deliberative choices : debating public policy in Congress](https://scispace.com/papers/deliberative-choices-debating-public-policy-in-congress-n53m6zs4ry?utm_source=claude&utm_medium=tool)**: Gary Mucciaroni, Paul J. Quirk, 2006. Book. 40 citations. *SciSpace* (S10).
    - Finding: Analyses House and Senate floor debate. The TL;DR concludes that congressional debate generally trades in half-truths, omissions and sometimes outright falsehoods, as legislators trade off persuasiveness against accuracy.
    - Relevance: This is the classic floor-debate accuracy study. It is a natural anchor for our "overstatement over obsolescence" finding.

29. **[Uncovering anti-politics by counting hyperbole: level, orientation, and ideology of rhetorical exaggeration](https://scispace.com/papers/uncovering-anti-politics-by-counting-hyperbole-level-q2cmhjuf081w?utm_source=claude&utm_medium=tool)**: Lieuwe Kalkhoven, Christ'l De Landtsheer, 2026. *Frontiers in political science*. No citation count given. *SciSpace* (S10).
    - Finding: Tests a framework for identifying and measuring hyperbole in parliamentary debates and examines ideological and government–opposition differences.
    - Relevance: This is a codebook for exaggeration in parliament. It could sharpen our "overstatement" category or serve as a validity comparison.

30. **[Political Fact-Checking Efforts are Constrained by Deficiencies in Coverage, Speed, and Reach](https://consensus.app/papers/details/w:ca8fd85c-d1df-462a-96cb-ee8e7b048ec3/?utm_source=claude_desktop)**: Morgan Wack et al., 2026. *Political Communication*. 15 citations. *Consensus* (C11).
    - Finding: For the 2022 US midterms, the abstract reports that fewer than half of prominent misinformation narratives were fact-checked and that the median fact-check came four days after a narrative appeared.
    - Relevance: It gives a timing benchmark for the checking side. It motivates near-real-time claim checking of Hansard, the decision-support angle of the sprint.

---

## 3. Closest prior work

**Bottom line:** No returned paper measured the publication age of sources cited in parliamentary speech, or whether parliamentary claims were current. Neither connector found a prior estimate for our 30-day median or our currency/obsolescence measure. The sourcing-rate measure has partial precedents, none of them claim-level coding of floor speeches:

- Kite (2013): 36% of legislative materials contained research evidence.
- Korsberg (2026): most committee expert arguments were unsourced.
- Henson and Benoit (2010): 8% of ad themes were sourced.

The papers nearest to ours:

1. **Wiesner (2026), "Who Refers to Science?"** This is the closest overall: LLM coding of 30,000 floor speeches, including the UK Commons, for references to scientific evidence. It overlaps on method (LLM as coder of evidence use in parliament) and partly on country.
   - It differs in unit (speech, not claim), in construct (scientific evidence yes or no, not none / vague / personal / named source), and in having no source dates or currency coding.
   - From the abstract it reports drivers, not a headline share, so it is not clear it gives a number directly comparable to our 51%.
2. **Kite et al. (2013), Minnesota.** A direct sourcing-rate measurement in a legislature: 36% contained research evidence. The units are documents and testimony, not MPs' speeches, and it covers one state and one policy area.
3. **Korsberg (2026), Finnish Education and Culture Committee.** Quantitative content analysis finds most arguments presented as "general knowledge" without a source. This is the closest match to our "no evidence" category, but for expert witnesses to a committee.
4. **Henson and Benoit (2010).** An explicit "claim with an identified source" rate (8%) in political messages. It covers campaign advertising, not parliament, but the operationalisation is very close to ours.
5. **Aroyehun et al. (2025, 2026).** Evidence-orientation scores for floor speeches at very large scale, the second one LLM-assisted. They overlap on the question of how evidence-based parliamentary talk is, but measure linguistic style, not sourcing, age or accuracy.

On evidence age, the nearest are document-level policy citation studies: Mahfouz (2026), Fang (2024), and the known Tunn (2025). All find lags of years, or reliance on older research, in policy documents. None looks at speeches, and their results run against our days-scale median.

---

## 4. Known papers that reappeared

- **Ouimet 2023**, "Use of research evidence in legislatures: a systematic review": both connectors (C2, C1b; S1, S2).
- **Rose 2020**, "Improving the use of evidence in legislatures: the case of the UK Parliament": both (C1b; S1).
- **Syväterä 2022**, "From where do legislators draw scientific knowledge?": both (C1b; S1).
- **Geddes 2024**, "Comparing evidence use in parliaments…": Consensus (C1b).
- **Begley 2019**, "Evidence-informed or value-based?": both (C1b; S1).
- **Ray 2021**, "Analysing the types of evidence used by Australian federal parliamentary committees": Consensus (C1b).
- **Tunn 2025**, "Evaluating Overton and Altmetric…": Consensus (C2).
- **Thomson 2025**, "Does the '17-year gap' tell the right story about implementation science?": Consensus (C2).
- **ClaimBuster**: SciSpace returned the related Hassan, Arslan, Li 2017 KDD paper, "Toward Automated Fact-Checking: Detecting Check-worthy Factual Claims by ClaimBuster" (S6). It is not identical to the known Arslan 2020 dataset paper.
- **Konstantinovskiy**: Consensus returned "Toward Automated Factchecking", 2021, *Digital Threats Research and Practice* (C6). This appears to be the published version of the known 2018 paper.
- **Atanasova 2018, CheckThat!**: SciSpace (S6), alongside the 2019 edition overview.
- **Ni 2024, AFaCTA**: both (C6; S13).
- **Törnberg 2023**: returned as Törnberg 2024, *Social Science Computer Review*, "Large Language Models Outperform Expert Coders…" (C7; S7). This appears to be the published version.
- **Cheng 2024, Dated Data**: both (C9; S9).
- **Dhingra 2021**: both. Consensus returned the 2022 TACL version (C9); SciSpace returned both the 2021 and 2022 versions (S9).
- **Not returned:** Morris 2011, Hanney 2015, Schlierkamp 2025, Gilardi 2023, Ziems 2023, Lazaridou 2021.

---

## 5. Gaps

- **Age of sources cited in parliamentary speech:** No paper from either connector measures publication age (in days or otherwise) of sources named in floor speeches. Age studies were all of policy documents (Overton-based) or biomedical citations.
- **Currency or obsolescence of parliamentary claims:** Nothing coded whether legislators' claims were out of date at the time of speaking. Accuracy work codes true or false, half-truths, or stretch versus dodge, not staleness.
- **Australian Hansard on AI:** Neither connector returned a content analysis of AI debate in the Australian Parliament. There was only a review of automated decision-making legislation (Jobberns 2024) and Australian Hansard datasets and stance tools. UK coverage was limited to the lexical Pretnar Žagar and Moats paper.
- **LLM claim extraction from parliamentary text, validated against humans:** Check-worthiness work is mostly on US debates and TV. LLM over-inclusion evidence came from other genres (newspapers, interviews, emails), not from Hansard.
- **AI tools for collective epistemics or decision support inside legislatures:** Results were frameworks, workshops and taxonomies (for example IPU-guideline analyses and "AI tools in Parliament") with no evaluations. The SciSpace provenance query (S11) returned mostly non-peer-reviewed repository and white-paper items (Zenodo-style "trust engines" and similar), which are of little use.
- **Unitizing in claim-level coding of political speech specifically:** Returned papers on unitizing were general (Krippendorff), on manifestos (Däubler) or on citances (Taşkın). None was on claim units in debates.

---

## 6. Consensus notice

Upgrade to Consensus Pro to include more data like study design and key takeaways for every result.: https://consensus.app/pricing/?utm_source=claude_desktop
