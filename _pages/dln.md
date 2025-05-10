---
permalink: /dln/
title: "Digital Literacy Narrative"
---

## Reflections on Digital Literacy

> *“Digital literacy is less about button‑clicking than about understanding the cultural logics that make those buttons matter.”*
> — adapted from **Berry & Fagerjord, 2017**

### Introduction – Why the Concept Keeps Expanding

When I arrived at university four years ago, “being good with computers” meant I could troubleshoot a Wi‑Fi glitch and weave a half‑decent PowerPoint. Since then my coursework—from has shown me that digital literacy is no static checklist. It is a moving horizon that now encompasses **algorithmic literacy, data ethics, critical code studies, and platform epistemology**. My goal in this reflection is three‑fold:

1. **Clarify** the layered skills and mind‑sets that constitute contemporary digital literacy.
2. **Demonstrate relevance** through concrete projects I completed this semester.
3. **Integrate** terminology and readings I have already cited in earlier assignments.


### From Skills to Literacies: A Quick Taxonomy

| Layer                         | Key Competence                               | Example From My Semester                                           |
| ----------------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| **Tool Literacy**             | Operating software for specific tasks        | Voyant Tools                                       |
| **Information Literacy**      | Evaluating sources & metadata                | Zotero workflows that I started using for my capstone  |
| **Algorithmic Literacy**      | Understanding recommender logic & bias       | Think about X/Twitter and read relevant articles
| **Computational Thinking**    | Decomposing problems, pattern generalisation | First assignment on Harris vs. Trump speeches                    |
| **Critical Digital Literacy** | Questioning power, ethics, sustainability    | Blanchette’s materiality critique & Klein et al.’s AI provocations |

This nested model echoes the argument that digital humanities “extend literacy into **critical technical practice**” (Berry & Fagerjord 2017).


### Content Creation & Social Interaction: Beyond Posting

My day now oscillates between **Notion** notes, **Perplexity** quick search, and **Discord/Reddit/X** debates. Each platform performs rhetorical work:

* **Notion** foregrounds *authorship* and *archiving*.
* **Perplexity** foregrounds *AI enabled search*.
* **Discord/Reddit/X** foregrounds *ephemerality*; threads dissolve unless intentionally archived.

Recognising those design philosophies is part of what scholars call **platform epistemology**—the study of how software architectures shape knowledge. It also guided my first assignment: I asked whether ChatGPT’s policy‑heavy prose reflected not just training‑data bias but an *interface constraint* that privileges factual coherence over affective repetition. The result: an R‑based lexical‑diversity index demonstrating that LLM‑generated texts clustered near **policy think‑tank white papers**, not stump speeches.


### Research & Data Management: Metadata Mindfulness

I understood the importance of data management while geocoding 235 license records from the *1918 Zanzibar Gazette*. The spreadsheet carried residential addresses, business types, and nationalities, but each row also needed **provenance fields**: screenshot filename, extraction model (GPT‑4o‑mini), and confidence score. Only then could I defend my claim that Tumbe and Miembeni were emerging commercial hubs.


### Digital Humanities & Computational Thinking: Bridging Qualitative and Quantitative

Reading **Berry & Fagerjord’s** chapter on computational thinking reframed my understanding of *scale*. That ethos influenced my first assignment's analysis. After TF‑IDF surfaced “border,” “freedom,” and “sovereignty” as top discriminators, I resisted quick generalisations. Instead, I ran a sentiment pass to see how often those terms co‑occurred with positive vs. negative valence. Result: Harris paired “freedom” with *family* verbs, while Trump paired “border” with *crisis* nouns. ChatGPT’s right‑wing persona, interestingly, borrowed Trump’s nouns but lacked his superlative‑driven intensifiers (“tremendous,” “incredible”), confirming the LLM’s weakness in **rhetorical amplitude**.


### Ethics, Sustainability & the Myth of Immateriality

One of the semester’s most destabilising readings was **Blanchette 2011**, which dismantles the myth that “the cloud is weightless.” Servers consume megawatts; e‑waste piles up; GPU stacks heat deserts. This lens forced me to recalibrate my enthusiasm for model‑heavy workflows. Running GPT‑4o‑mini on 90 PNG screenshots may be “productive,” but it is not impact‑free. In future iterations I intend to:

1. Batch‑compress images to cut token overhead.
2. Cache interim JSON locally rather than re‑query the API.
3. Publish an energy‑use note in the project datasheet, echoing **Klein et al. 2025** on accountability.

Ethics also surface in **algorithmic bias**. My EdWeek‑sourced definition of digital literacy (Loewus 2017) stresses “find, evaluate, create, and communicate information.” Yet real‑world recommender engines complicate the “evaluate” step: they tilt visibility toward particular ideologies. My personal project on X/Twitter study showed how AI influencers’ engagement with U.S. politics created a feedback loop in which the algorithm inferred that *I* must crave political hot‑takes. Recognising such loops is part of the literacy skill set.


### Limits & Future Growth: Toward Critical Code Studies

Despite gains, my skill graph still has blank nodes:

* **Data Storytelling** – My KeplerGL map impressed visually but lacked narrative scaffolding. Next iteration I will layer scrollytelling panels that guide the reader through Tumbe’s market rise and Malindi’s artisanal cluster.
* **Critical Code Annotation** – As course discussions emphasised, reading software like literature uncovers hidden ideologies; I have yet to annotate a full inference loop.


### Conclusion – Digital Literacy as Reflexive Practice

If the liberal arts excel at anything, it is reminding us that every tool is also a text—open to interpretation, critique, and revision. My speech‑corpus project clarified how linguistic metrics can diagnose (but not fully resolve) AI bias. My Zanzibar thick‑map revealed how OCR pipelines translate colonial ledgers into contemporary spatial logics—and how fragile those translations are. Both projects convinced me that digital literacy is best understood as a **reflexive practice**: one that loops technical skill with cultural analysis in perpetuity.

In the semesters ahead, I will continue to ask: What infrastructures underlie my screen? What histories haunt my dataset? And how can I design with both efficiency and equity in mind? Answering those questions, I believe, will turn mere digital competence into genuinely *humane* digital fluency.


### References

Berry, D. M., & Fagerjord, A. (2017). *Digital Humanities: Knowledge and Critique in a Digital Age*. Polity.

Blanchette, J‑F. (2011). *A Material History of Bits*. *Journal of the American Society for Information Science and Technology*, 62(6), 1042–1057.

Klein, L., Di Salvo, P., Lee, B., Srivastava, S., & Ngô, M. (2025). *Provocations from the Humanities for Generative AI Research* (arXiv:2502.19190).

Loewus, L. (2017). What Is Digital Literacy? *Education Week*. [https://www.edweek.org/teaching-learning/what-is-digital-literacy/2016/11](https://www.edweek.org/teaching-learning/what-is-digital-literacy/2016/11)
