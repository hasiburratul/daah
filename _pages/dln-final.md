---
permalink: /dln-final/
title: "Digital Literacy Narrative"
---

## Reflections on Digital Literacy

*A four‑year journey from “I can fix the Wi‑Fi” to “What cultural logics hide in my code?”*

> *“Digital literacy is less about button‑clicking than about understanding the cultural logics that make those buttons matter.”*
> — after **Berry & Fagerjord, 2017**

### 0 · Overture — Why a Third Draft?

Ten days from now I’ll walk across the commencement stage, Computer Science degree in one hand and a second major in **Interactive Media** in the other. And **Introduction to Digital Arts and Humanities** was the most surprising course out of all courses I have taken in 4 years. I started the course thinking digital humanities was just about putting books online or making fancy websites. But the readings, especially Mattingly’s “How to Get Started in Digital Humanities” and Berry’s “What are the Digital Humanities?”, really made me rethink that. I realized digital humanities is about asking new questions and using technology to see patterns and stories we would otherwise miss.

Now wrapping up the entire semester on Digital Literacy does not seem that vauge it seemed in the first version. By this time I had scraped GAN face images, “thick‑mapped” colonial Zanzibar, and color‑coded partisan sentiment across presidential speeches. More importantly, I had learned to ask why an algorithm performs the way it does and who benefits when a dataset becomes a map, a heat‑chart, or a headline



### 1 · What I learnt from the 3 assignments
1. Assignment 1: Politicians wield superlatives (“greatest,” “tremendous”) while ChatGPT default voice uses mid‑register policy jargon. Sentiment radar graphs revealed the gap within minutes.

2. Assignment 2: OCR errors in the Zanzibar Gazette forced manual correction; those errors highlighted multilingual print culture and colonial naming conventions—an invisible layer digital tools alone would miss.

3. Assignment 3: CLIP, Inception, and GPT‑4o all flagged real celebrity photos as authentic because of noise—flash glare, JPEG artefacts, asymmetrical lighting—while flawless GAN faces read as fakes.

> Synthesis: In digital spaces, mess is a reliability signal. Authentic humans misspell, sweat, mis‑light. Algorithms often iron out those wrinkles—then become detectable precisely for their tidiness.

---

### 2 · Platforms in Daily Rotation — Affordances & Friction Points (Updated Table)

| Platform            | Primary Use‑Case             | Affordances Realised                     | Limitations Discovered              | New Insight                                   |
| ------------------- | ---------------------------- | ---------------------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| **Notion**          | Lab notebook, reading logs   | Block‑level drag‑n‑drop, backlink graph  | Markdown export mangles LaTeX       | Using backlinks to trace idea genealogy across CS & DAH courses |
| **Voyant Tools**    | Rapid distant reading        | No install, word clouds in seconds       | Stop‑list editing shallow           | Pair Voyant with *R* for serious cleaning                       |
| **Perplexity AI**   | Lightning‑fast lit scans     | Inline citations, news + papers          | Conflates scopes → must cross‑check | Acts as “plausibility scout,” not oracle                        |
| **R + Posit Cloud** | Textual analysis | Free CPU, tidyverse grammar              |         | Plan to learn data analysis
| **Kepler.gl**       | Thick‑mapping                | Real‑time filters, deck.gl speed         | Narrative framing absent            | Plan to embed Kepler inside scrollytelling site                 |
| **Orange DM**       | Image embeddings             | Drag‑and‑drop, Quick CLIP                | No fine‑tune knobs                  | Good for *exploratory* clustering before custom scripts         |
| **GitHub Pages**    | Public DAH blog              | Version control + markdown               | Build times slow, YAML brittle      | Realised blog commits double as portfolio evidence              |
| **GPT‑4o Vision**      | OCR, reasoning on images            | Reads ditto marks; can generate clean CSV from newspaper scans.            | High token count = high energy; risk of hallucinating coordinates (Blanchette 2011).   | Default to smaller model, escalate only when necessary. |



**Take‑away:** Every tool “thinks” in its own ontology. Digital literacy means noticing when that ontology warps your research question.

---

### 3 · The Learning Graph — What Clicked, What’s Still Loading

#### 3.1 Strength Nodes

* **Code‑Critique Bilingualism.** My CS background let me write speed scrapers (`image.py`, `celebrity_wiki_images.py`) *and* immediately pivot to humanities lens.
* **Pattern Recognition Across Modalities.** From TF‑IDF spikes (“border” ↔ “crisis”) to CLIP quadrant splits, I can jump scale—document ⇌ corpus ⇌ latent space.
* **Provenance Reflex.** Klein et al.’s dataset‑transparency call (2025) turned into habit. 

#### 3.2 Freshly Installed Concepts

| Concept                                | How It Shifted My Thinking                                                    | Source Reading / Demo                  |
| -------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------- |
| **Computational Thinking ≈ Phronesis** | Problem‑decompose like a programmer, but keep reflective “why” of humanities. | Berry & Fagerjord ch. 2 + class debate |
| **Humanities Ground Truth**            | HTR fails without context; experts correct the OCR.                           | Transkribus lab, Week 6                |
| **Thick Mapping**                      | Maps can store *stories*, not just points.                                    | Mattingly, “Thick Mapping 101”         |
| **Distant Viewing**                    | Vision pipelines = lenses that reveal biases.                                 | Arnold & Tilton 2023                   |
| **Platform Epistemology**              | Interface nudges what counts as evidence.                                     | Drucker, “Critique of Visualization”   |




### 4 · How I Feel About Learning With AI

* **Awe.** GPT‑4o reading ditto marks in 1918 ledgers felt like sorcery.
* **Skepticism.** GPT‑4o‑mini’s 8 % face‑detection accuracy + confident prose reminded me models compress by *forgetting nuance*.
* **Responsibility.** Blanchette’s energy critique keep me honest about AI’s carbon cost.


Net emotion = *critical optimism*.


### 5 · Conclusion 

Digital literacy, I’ve learned, is *reflexive practice*: looping between tool mastery and cultural critique. From the corpus of campaign speeches to the map of Zanzibar’s trading streets to the face‑off between GAN strangers and Wikipedia celebrities, the through‑line is simple:

> **Imperfection tells the story.**
> Real humans misspell. Old paper bleeds ink. Celebrity photographers overexpose. GANs iron out every wrinkle—and get caught.

**How this reshaped my platform thinking:** I now pick a tool by first asking *“What does this interface assume about truth?”* For example, Notion’s backlink graph encouraged me to model idea networks; Orange’s no‑code pipelines nudged me toward exploratory, not confirmatory, analysis.


So as I step beyond the campus firewall, my pledge is to keep **coding with one hand and questioning with the other**: surface bias, celebrate noise, and remember that to appear convincingly human—even to a machine—requires leaving a trace of glorious mess.

---

### References

Berry, D. M., & Fagerjord, A. (2017). *Digital Humanities: Knowledge and Critique in a Digital Age*. Polity.
Blanchette, J.‑F. (2011). *A Material History of Bits*. *JASIST*, 62(6), 1042–1057.
Klein, L., Di Salvo, P., Lee, B., Srivastava, S., & Ngô, M. (2025). *Provocations from the Humanities for Generative AI Research* (arXiv:2502.19190).
Loewus, L. (2017). What Is Digital Literacy? *Education Week*.
Arnold, T., & Tilton, L. (2023). *Distant Viewing: Computational Exploration of Digital Images*. MIT Press.
Li, F.‑F. (2015). *How we teach computers to understand pictures* \[TED Talk].
Impett, L., & Offert, F. (2024). There Is a Digital Art History. *Visual Resources*, 38(2).
Karras, T., Laine, S., & Aila, T. (2019). *A Style‑Based Generator Architecture for GANs*. CVPR.
*ThisPersonDoesNotExist.com* (2024). AI‑generated faces.
