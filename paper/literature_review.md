# Literature review

Search date: 15 November 2026. Tools used: WebSearch, WebFetch, Scholar Feed paper search. Reading depth for each reference is tagged in the References section. Where I only had a search record, I say so and do not report figures beyond what the record showed.

---

## 1. Related Work

### 1.1 Evidence use in legislatures

Most work on how legislatures use evidence relies on interviews, surveys and case studies, not on counting what members say. A systematic review of 21 studies found that research evidence in legislatures is used mostly for symbolic or tactical purposes. It also found that most studies were from the United States and that content analysis of debates is underused [1]. In the UK, interviews and surveys of 157 people in Parliament identified credibility, relevance, accessibility and timing as the factors that shape evidence use [2]. Interpretive work on select committees describes the different meanings "evidence" has for MPs and officials [3]. Begley et al. combine interviews with Hansard in three case studies of bills and argue that process, subject and political circumstance shape how often legislators make claims about evidence [4]. Studies that count sources look at documents rather than speech. Australian federal committee reports rarely cite peer-reviewed research [5]. Furnas et al. matched science citations in US congressional committee reports and think-tank documents. According to a secondary summary, Democratic-controlled committees were 1.8 times more likely than Republican ones to cite science and cited slightly older work [7]. Syväterä et al. code which organisations legislators present as scientific authorities in 576 debates on new legislation in Australia, Finland, Kenya and the UK [6]. Two UK audits are close to our evidence categories. Sense about Science's assessment of government policy documents separates "gesturing" at evidence from referencing it, and found that most proposals did not show which points rested on which sources [8, 9]. A report for the UK Statistics Authority counted numerical keywords in Hansard from 1967 to 2017 and found no rise in their use [10]. In US congressional speech, a dictionary-based measure of "evidence-based" language has declined since the mid-1970s [11]. A follow-up applies an LLM-plus-embedding version of the measure to parliaments in seven countries [12]. The Discourse Quality Index, first applied to a House of Commons debate, codes whether a speaker justifies a demand [13].

*Gap.* These studies measure whether evidence is invoked, which types are invoked, or vocabulary. None we found codes individual factual claims in plenary speech for what evidence backs each one and when that evidence was published.

### 1.2 Time lags and how fast information reaches parliament

The time-lag literature measures time from research to use. A review of translational health research put the commonly cited figure at 17 years and noted that measures are not comparable across studies [14]. Hanney et al. found no agreed starting point for measuring lags [15]. Studies based on Overton measure lags from the publication side. For one NIHR unit's 110 articles, the median time from publication to citation in a policy document or guideline was 183 weeks [16]. Overton's own description [17] and a study of 18 million Web of Science publications, which reports a citation delay towards newly published work [18], cover policy documents, not speeches. Agenda-setting research asks how quickly news reaches parliament. In Dutch data, most oral questions can be traced to coverage in the preceding days [19]. Across seven European countries, how strongly media coverage drives parliamentary attention depends on the type of government [20].

*Gap.* Lag studies measure the age of research when a policy document first cites it. Agenda-setting studies measure topic attention. Neither measures how old the named source behind a spoken claim is on the day it is spoken. Our 30-day median is a different quantity, closer to the agenda-setting finding than to the "17 years" figure, and the two should not be compared directly.

### 1.3 How legislators talk about AI, and parliamentary corpora

Work on AI in parliaments is about framing. Suter et al. compare AI frames in four legislatures from 2014 to 2024 (not the UK or Australia) and find a sharp increase in AI debate after ChatGPT's release, driven by ethics and regulation [21]. A comparative discourse analysis of five jurisdictions, including the UK, uses one episode per jurisdiction and does not assess the evidence cited [22]. An exploratory topic analysis of UK Commons AI speeches up to April 2024 is available only as a blog post [23]. Separately, a classifier detects a steady rise in undisclosed LLM-generated text in UK and Swedish parliamentary texts from 2022 [24]. This matters for interpretation: some "speaker" evidence practices may be drafting artefacts. Large corpora exist: ParlaMint (17 parliaments in its first release) [25], ParlSpeech [26] and the LLM-labelled ParlaCAP topic dataset [27]. We did not find an Australian Hansard corpus in our searches.

*Gap.* No study we found examines the factual content of AI debate in the UK or Australian parliaments, or the evidence offered for it.

### 1.4 Claim detection, evidence types and temporal fact-checking

Check-worthiness research supplies the claim unit. ClaimBuster labelled 23,533 statements from US presidential debates [28]. Full Fact and colleagues built a claim schema on UK political TV [29]. CheckThat! 2018 ranked debate sentences, and the best English system reached a mean average precision of 0.18 [30]. Claim detection has also been applied to UK election debate speech [31]. AFaCTA defines factual claims by verifiability and uses LLM consistency checks to annotate political speech [32]. Our over-inclusion rate (about 14% of coded "claims" rejected) is a direct test of that kind of definition. Argument mining has a separate evidence-detection strand [33]. Recent annotation of German COVID-19 debate codes justification categories across plenary, committee and press arenas [34]. FactAppeal is the closest scheme to ours. It annotates whether factual claims in news are backed by sources, the source type (for example expert or direct evidence), and whether the source is named [35]. Time-aware evidence ranking uses evidence timestamps to improve verification of time-sensitive claims [36].

*Gap.* Existing schemes code source type and naming but not source date. We add a date field and a check of whether the claim was still current on the day, and apply them to legislative speech.

### 1.5 LLMs as coders, and their limits

Early results favoured LLM annotators over crowd-workers [37, 38]. A 25-benchmark evaluation was more cautious: zero-shot models did not beat fine-tuned ones [39]. Later work stresses validation. Performance varied widely across 27 replicated tasks [40]. Zero-shot codebook-following by open-weight models was limited [41]. In replications of 37 tasks, about 31% of hypotheses reached incorrect conclusions with state-of-the-art models, depending on configuration [42]. Changing the task design lowered agreement from a median κ of 0.91 to 0.76 [43]. High aggregate scores can hide label-level failures [44]. Model knowledge also ages: performance falls on text written after the training period [45, 46], and effective knowledge cutoffs differ from the reported ones [47]. This is relevant because our coders judged whether claims were current, with web search as the remedy.

*Gap.* Our human checks (40 spot-checked claims, 29 adjudicated speeches) are small next to these designs. We did not test prompt or design variation, so instrument uncertainty [43] remains unmeasured.

### 1.6 Tools for epistemics

Forethought's design sketches propose provenance tracing, reliability tracking and rhetoric highlighting [48]. Citation-attribution benchmarks test whether cited text supports a statement. In ALCE, the best models lacked full citation support on ELI5 about half the time [49], and attribution can be judged automatically with mixed success [50]. Domain-level source ratings agree closely across six expert sets [51]. These tools assume a citation exists. In our data, half the claims had none.

*Gap.* We give a baseline for how much provenance and recency information legislative AI claims carry before any tool is applied.

---

## 2. Novelty check

**Closest prior work.**
- Furnas et al. [7]: this study looks at the age and quality of science cited in US congressional committee reports, by party. It is the nearest measure of "age of what legislators cite". It covers written committee reports, not floor speech, scholarly citations only, and one country. I did not open the article; my figures come from a news summary.
- Overton lag studies [16–18]: these measure lags from the publication side, in policy documents.
- Begley et al. [4] and Syväterä et al. [6]: these use Hansard to study claims of evidence and invoked authorities, but qualitatively or by authority type. They do not date sources.
- FactAppeal [35]: this codes whether factual claims are backed by a named source. It is the nearest equivalent to our "share of claims with a source", but it studies news, not legislatures.
- Sense about Science [8]: the "gesturing vs referencing" distinction parallels our "vague attribution" category, but it was applied to government policy documents.
- Aroyehun et al. [11, 12] and the carr report [10]: these measure evidence-related vocabulary or numerical keywords, not sourced claims.

**What I searched and could not find.**
- Any study measuring the publication age of sources named in plenary or floor speeches, in any legislature.
- Any study reporting the share of legislators' factual claims that carry a named source, as opposed to whether speeches contain justification (the DQI [13]) or evidence words.
- Any analysis of evidence or factual accuracy in UK or Australian parliamentary AI debate.
- Any academic study of how MPs cite official statistics, beyond the carr report and Full Fact's campaigning material, which is not systematic.

I did not use Consensus or SciSpace, and I did not search Google Scholar directly. Paywalled journals (Wiley, Science, Springer) refused fetches, so I could not see their reference lists.

**Confidence.**
- Moderate-to-high that no one has measured the age of evidence cited in parliamentary speech.
- Moderate that no one has measured the share of parliamentary claims that carry a source. The deliberation literature (DQI and its applications) and the argumentation-scheme literature may contain claim-level justification counts that a keyword search misses.

A safe framing is: "to our knowledge, the first claim-level measurement of source naming and source age in legislative speech". Credit Furnas et al. [7] for source age in congressional documents and FactAppeal [35] for claim-level source attribution in news.

---

## 3. Corrections to the existing list

- **Rose et al. 2020** is in *Evidence & Policy* 16(4), 619–638. It is an interview, survey and ethnography study of 157 people in Parliament, not an analysis of debates.
- **Syväterä et al.**: the record I found gives the *British Journal of Sociology*, 2023 (authors Syväterä, Rautalin, Magyari). The year "2022" may be the online-first date, but I could not open the page to confirm. It covers 576 debates on new legislation and codes organisations invoked as scientific authorities, not source dates.
- **"Geddes 2024"**: I could not find a 2024 journal article. The closest are Geddes 2021, *Public Administration* ("The webs of belief around 'evidence' in legislatures") [3], and a January 2023 "Good Evidence" fellowship report. Check which one you meant.
- **Ray et al. "2021"**: the issue date is 2022 (*AJPA* 81(2), 279–302), and it was online in August 2021. It analyses committee reports, not debates.
- **Begley et al. 2019** is more relevant than a passing citation suggests. It uses Hansard to study "claims of evidence" during bill scrutiny, so cite it near the evidence-category results.
- **Thomson et al. 2025 and Schlierkamp et al. 2025**: two targeted searches each found nothing. Do not cite them unless you have a link. The search did turn up Tunn and Knight's UKOSS paper (median lag 220.8 weeks), which I saw only as a search snippet and have not listed.
- **Tunn et al. 2025** is correct (*NIHR Open Research* 5:59). It covers one research unit's 110 articles, with a median lag of 183 weeks.
- **Morris et al. 2011 and Hanney et al. 2015** measure lags in translating health research into practice. That is a different quantity from source age at the moment of speaking. Use them only for contrast.
- **ClaimBuster** covers US presidential debates (23,533 statements) and appeared at ICWSM 2020.
- **Konstantinovskiy et al.** appeared in ACM *Digital Threats: Research and Practice*, using UK TV political shows. The abstract gives no inter-annotator agreement figures.
- **Gilardi et al.** appeared in *PNAS* 120(30). It compares ChatGPT with crowd-workers and trained annotators on tweets.
- **Törnberg 2023** is a 5-page arXiv preprint on a single task: party affiliation from tweets. No journal reference is listed, so it is weak support for coding complex claims.
- **Ziems et al.** appeared in *Computational Linguistics*. Its headline finding is less favourable than it is often cited for: LLMs did not beat fine-tuned models on classification.
- **Dhingra et al.** appeared in *TACL* 2022 (arXiv 2021). **Lazaridou et al.** appeared at NeurIPS 2021.
- **Cheng et al. ("Dated Data")** concerns models' own training cutoffs. It is relevant to the AI coders' currency judgments, not to politicians.
- **AFaCTA** appeared at ACL 2024. It is directly relevant to your over-inclusion finding, so cite it there.
- **Aroyehun et al.** is now published: *Nature Human Behaviour* 9(6), 1122–1133, 2025.

---

## 4. References

[1] Ouimet, M., Beaumier, M., Cloutier, A., Côté, A., Montigny, É., Gélineau, F., Jacob, S., Ratté, S. (2023). Use of research evidence in legislatures: a systematic review. *Evidence & Policy*. https://cirst2.openum.ca/s/13656 `[search record only]`

[2] Rose, D. C., Kenny, C., Hobbs, A., Tyler, C. (2020). Improving the use of evidence in legislatures: the case of the UK Parliament. *Evidence & Policy* 16(4), 619–638. https://centaur.reading.ac.uk/88497 `[search record only]`

[3] Geddes, M. (2021). The webs of belief around 'evidence' in legislatures: The case of select committees in the UK House of Commons. *Public Administration*. https://onlinelibrary.wiley.com/doi/10.1111/padm.12687 `[search record only]`

[4] Begley, P., Bochel, C., Bochel, H., Defty, A., Gordon, J., Hinkkainen, K., Kisby, B., McKay, S., Strange, G. (2019). Evidence-informed or value-based? Exploring the scrutiny of legislation in the UK Parliament. *Journal of Legislative Studies* 25(1), 1–20. https://eprints.whiterose.ac.uk/142910 `[abstract]`

[5] Ray, A., Young, A., Grant, W. J. (2022). Analysing the types of evidence used by Australian federal parliamentary committees. *Australian Journal of Public Administration* 81(2), 279–302. https://researchportalplus.anu.edu.au/en/publications/analysing-the-types-of-evidence-used-by-australian-federal-parlia/ `[abstract]`

[6] Syväterä, J., Rautalin, M., Magyari, A. K. (2023). [Organisations as scientific authorities in parliamentary debates; exact title not seen]. *British Journal of Sociology*. https://onlinelibrary.wiley.com/doi/10.1111/1468-4446.12989 `[search record only]`

[7] Furnas, A., LaPira, T., Wang, D. (2025). [Partisan differences in the use of science in policy; exact title not seen]. *Science*. Article page refused fetch; secondary summary: https://journalistsresource.org/home/study-reveals-stark-divide-in-how-democrats-and-republicans-cite-science/ `[search record only; secondary summary read]`

[8] Sense about Science (2016). Transparency of evidence: An assessment of government policy proposals May 2015 to May 2016. https://nuffieldfoundation.org/wp-content/uploads/2019/11/SaS20Transparency20of20Evidence20201620Nov20small1.pdf `[full text, partly read]`

[9] Rutter, J., Gold, J. (2015). Show your workings: Assessing how government uses evidence to make policy. Institute for Government. https://instituteforgovernment.org.uk/publication/report/show-your-workings `[abstract]`

[10] Lodge, M., Norderland, M. (2017). The use of statistics and facts in contemporary political discourse. carr (LSE) report for the UK Statistics Authority. https://www.lse.ac.uk/accounting/assets/Documents/news/carr-report-for-UKSA-final.pdf `[full text, Hansard section]` (the second author's surname is spelled as printed in the PDF)

[11] Aroyehun, S. T., Simchon, A., Carrella, F., Lasser, J., Lewandowsky, S., Garcia, D. (2025). Computational analysis of US congressional speeches reveals a shift from evidence to intuition. *Nature Human Behaviour* 9(6), 1122–1133. https://arxiv.org/abs/2405.07323 ; https://kops.uni-konstanz.de/entities/publication/c4ac2d6b-6ca9-4aa5-856d-b17f57ef1c71/full `[abstract]`

[12] Aroyehun, S., Lewandowsky, S., Garcia, D. (2026). Epistemic orientation in parliamentary discourse is associated with deliberative democracy. arXiv preprint. https://arxiv.org/abs/2604.19699 `[abstract]`

[13] Steenbergen, M. R., Bächtiger, A., Spörndli, M., Steiner, J. (2003). Measuring political deliberation: A Discourse Quality Index. *Comparative European Politics* 1(1), 21–48. https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_60622215 `[search record only]`

[14] Morris, Z. S., Wooding, S., Grant, J. (2011). The answer is 17 years, what is the question: understanding time lags in translational research. *Journal of the Royal Society of Medicine* 104(12), 510–520. https://www.rand.org/pubs/external_publications/EP201100302.html `[search record only; page refused fetch]`

[15] Hanney, S. R., et al. (2015). How long does biomedical research take? Studying the time taken between biomedical and health research and its translation into products, policy and practice. *Health Research Policy and Systems* 13(1). https://bura.brunel.ac.uk/handle/2438/10426?mode=full `[search record only]`

[16] Tunn, R., Alderdice, F., Knight, M. (2025). Evaluating Overton and Altmetric as tools for tracking healthcare research use and impact on policy and practice: a descriptive study. *NIHR Open Research* 5:59. https://openresearch.nihr.ac.uk/articles/5-59 `[abstract]`

[17] Szomszor, M., Adie, E. (2022). Overton: A bibliometric database of policy document citations. arXiv preprint. https://arxiv.org/abs/2201.07643 `[abstract]`

[18] Fang, Z., Dudek, J., Noyons, E., Costas, R. (2024). Science cited in policy documents: Evidence from the Overton database. arXiv preprint. https://arxiv.org/abs/2407.09854 `[abstract]`

[19] Van Aelst, P., Vliegenthart, R. (2014). Studying the tango: an analysis of parliamentary questions and press coverage in the Netherlands. *Journalism Studies* 15(4), 392–410. https://dare.uva.nl/id/284f3d31-cccf-4f53-b533-aece1b5be8cd `[abstract]`

[20] Vliegenthart, R., Walgrave, S., Baumgartner, F. R., et al. (2016). Do the media set the parliamentary agenda? A comparative study in seven countries. *European Journal of Political Research* 55(2), 283–301. https://diposit.ub.edu/items/1783cf18-fff8-4bd6-85e4-a94c56d3d532/full `[abstract]`

[21] Suter, V., Ma, C., Pöhlmann, G., Meckel, M. (2025). When politicians talk AI: Issue-frames in parliamentary debates before and after ChatGPT. *Policy & Internet* 17(3). https://www.alexandria.unisg.ch/entities/publication/520c8670-b638-49b3-a265-e884079e6f26/full `[abstract]`

[22] Beisenbayev, E., Bukharbayev, B., Tolen, Z., Rystina, I., Nurov, M. (2026). Parliamentary discourse and legislative approaches to artificial intelligence regulation: a comparative analysis of five jurisdictions. *Frontiers in Political Science* 8. https://www.frontiersin.org/journals/political-science/articles/10.3389/fpos.2026.1874183/full `[full text, partly read]`

[23] Pretnar Žagar, A. (2024). Exploring parliamentary AI debates with computational text analysis. Blog post, Reimagining Public Values in Algorithmic Futures, University of Helsinki. https://www.helsinki.fi/en/researchgroups/reimagining-public-values-in-algorithmic-futures/whats-new/exploring-parliamentary-ai-debates-with-computational-text-analysis `[full text]`

[24] Suvanto, M., McGlinchey, A., Barclay, P. J., Wahde, M. (2026). Detecting undisclosed LLM-generated content in parliamentary texts. arXiv preprint. https://arxiv.org/abs/2606.14209 `[abstract]`

[25] Erjavec, T., Ogrodniczuk, M., Osenova, P., et al. (2023). The ParlaMint corpora of parliamentary proceedings. *Language Resources and Evaluation* 57(1), 415–448. https://epubl.ktu.edu/object/elaba:119556500/index.html `[abstract]`

[26] Rauh, C., de Wilde, P., Schwalbach, J. (2017). The ParlSpeech data set. Harvard Dataverse. https://fis.leuphana.de/en/datasets/the-parlspeech-data-set-annotated-full-text-vectors-of-39-million/ `[abstract]` (ParlSpeech V2, Rauh and Schwalbach, which covers nine countries and 6.3 million speeches, was seen only in a search record)

[27] Kuzman Pungeršek, T., Rupnik, P., Širinić, D., Ljubešić, N. (2026). Supercharging agenda setting research: The ParlaCAP dataset of 28 European parliaments and a scalable multilingual LLM-based classification. PoliticalNLP workshop at LREC 2026. https://arxiv.org/abs/2602.16516 `[abstract]`

[28] Arslan, F., Hassan, N., Li, C., Tremayne, M. (2020). A benchmark dataset of check-worthy factual claims. ICWSM 2020. https://arxiv.org/abs/2004.14425 `[abstract]`

[29] Konstantinovskiy, L., Price, O., Babakar, M., Zubiaga, A. (2018/2020). Towards automated factchecking: Developing an annotation schema and benchmark for consistent automated claim detection. *ACM Digital Threats: Research and Practice*. https://arxiv.org/abs/1809.08193 `[abstract]`

[30] Atanasova, P., Barrón-Cedeño, A., Elsayed, T., et al. (2018). Overview of the CLEF-2018 CheckThat! Lab on automatic identification and verification of political claims. Task 1: Check-worthiness. CLEF 2018. https://arxiv.org/abs/1808.05542 `[abstract]`

[31] Lippi, M., Torroni, P. (2016). Argument mining from speech: Detecting claims in political debates. AAAI 2016. https://lia.disi.unibo.it/~ml/publications/AAAI2016.pdf `[full text, first page]`

[32] Ni, J., Shi, M., Stammbach, D., Sachan, M., Ash, E., Leippold, M. (2024). AFaCTA: Assisting the annotation of factual claim detection with reliable LLM annotators. ACL 2024. https://arxiv.org/abs/2402.11073 `[abstract]`

[33] Rinott, R., Dankin, L., Alzate Perez, C., Khapra, M. M., Aharoni, E., Slonim, N. (2015). Show me your evidence – an automatic method for context dependent evidence detection. EMNLP 2015, 440–450. https://aclanthology.org/D15-1050/ `[search record only]`

[34] Vikhrova, N., Kühling, J., Haunss, S., Padó, S. (2026). Comparing and modeling argumentation in German political communication across arenas. KONVENS 2026. https://arxiv.org/abs/2608.00288 `[abstract]`

[35] Mor-Lan, G., Sheafer, T., Shenhav, S. R. (2025/2026). FactAppeal: Identifying epistemic factual appeals in news media. Findings of EACL 2026. https://arxiv.org/abs/2510.10627 `[abstract]`

[36] Allein, L., Augenstein, I., Moens, M.-F. (2021). Time-aware evidence ranking for fact-checking. *Journal of Web Semantics*. https://arxiv.org/abs/2009.06402 `[abstract]`

[37] Gilardi, F., Alizadeh, M., Kubli, M. (2023). ChatGPT outperforms crowd-workers for text-annotation tasks. *PNAS* 120(30), e2305016120. https://arxiv.org/abs/2303.15056 `[abstract]`

[38] Törnberg, P. (2023). ChatGPT-4 outperforms experts and crowd workers in annotating political Twitter messages with zero-shot learning. arXiv preprint. https://arxiv.org/abs/2304.06588 `[abstract]`

[39] Ziems, C., Held, W., Shaikh, O., Chen, J., Zhang, Z., Yang, D. (2024). Can large language models transform computational social science? *Computational Linguistics*. https://arxiv.org/abs/2305.03514 `[abstract]`

[40] Pangakis, N., Wolken, S., Fasching, N. (2023). Automated annotation with generative AI requires validation. arXiv preprint. https://arxiv.org/abs/2306.00176 `[abstract]`

[41] Halterman, A., Keith, K. A. (2026). Codebook LLMs: Evaluating LLMs as measurement tools for political science concepts. *Political Analysis* 34, 188–204. https://arxiv.org/abs/2407.10747 `[abstract]`

[42] Baumann, J., Röttger, P., Urman, A., Wendsjö, A., Plaza-del-Arco, F. M., Gruber, J. B., Hovy, D. (2025). Large language model hacking: Quantifying the hidden risks of using LLMs for text annotation. arXiv preprint. https://arxiv.org/abs/2509.08825 `[abstract]`

[43] Reiter, T., Kern, C., Miasnikov, F., Nikolenko, S., Chew, R., Eckman, S., Kreuter, F. (2026). Reliable but design-sensitive: Instrument uncertainty in LLM annotation. UncertaiNLP workshop at EMNLP 2026. https://arxiv.org/abs/2609.35824 `[abstract]`

[44] Senger, E., Campbell, Y., van der Goot, R., Plank, B. (2026). High scores, hidden failures: Evaluating codebook-based LLM content analysis. Findings of EMNLP 2026. https://arxiv.org/abs/2610.35179 `[abstract]`

[45] Lazaridou, A., Kuncoro, A., Gribovskaya, E., et al. (2021). Mind the gap: Assessing temporal generalization in neural language models. NeurIPS 2021. https://arxiv.org/abs/2102.01951 `[abstract]`

[46] Dhingra, B., Cole, J. R., Eisenschlos, J. M., Gillick, D., Eisenstein, J., Cohen, W. W. (2022). Time-aware language models as temporal knowledge bases. *TACL* 10, 257–273. https://arxiv.org/abs/2106.15110 `[abstract]`

[47] Cheng, J., Marone, M., Weller, O., Lawrie, D., Khashabi, D., Van Durme, B. (2024). Dated data: Tracing knowledge cutoffs in large language models. arXiv preprint. https://arxiv.org/abs/2403.12958 `[abstract]`

[48] Cotton-Barratt, O., Vaintrob, L., Sourbut, O. (2026). AI tools for collective epistemics. Forethought. https://newsletter.forethought.org/p/ai-tools-for-collective-epistemics `[full text, summary level]`

[49] Gao, T., Yen, H., Yu, J., Chen, D. (2023). Enabling large language models to generate text with citations. EMNLP 2023. https://arxiv.org/abs/2305.14627 `[abstract]`

[50] Yue, X., Wang, B., Chen, Z., Zhang, K., Su, Y., Sun, H. (2023). Automatic evaluation of attribution by large language models. Findings of EMNLP 2023. https://arxiv.org/abs/2305.06311 `[abstract]`

[51] Lin, H., Lasser, J., Lewandowsky, S., Cole, R., Gully, A., Rand, D. G., Pennycook, G. (2023). High level of correspondence across different news domain quality rating sets. *PNAS Nexus* 2(9), pgad286. https://pmc.ncbi.nlm.nih.gov/articles/PMC10500312 `[abstract]`

