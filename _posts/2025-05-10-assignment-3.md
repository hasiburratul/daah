---
title: "Assignment 3"
date: 2025-05-10
categories: 
 - assignment
tags:
  - 
  - 
---

## Introduction
In early April I found myself doom‑scrolling through ThisPersonDoesNotExist—a kind of infinite hall of mirrors where every smiling stranger feels plausible until that second glance when the teeth blur or the earrings go missing. Two thoughts collided. First, these faces are improving at a speed that feels exponential. Second, so are the detectors trained to unmask them. What happens, I wondered, when we pit contemporary visual‑AI pipelines against a hand‑curated rogues' gallery of GAN portraits and bona‑fide celebrity photos?

Assignment 3 handed me the perfect sandbox: build a custom corpus, push it through Orange Data Mining, 2D CLIP, and DV Explorer, then write a critical essay. I decided to go all‑in on the face problem, assembling 100 images—fifty "people" who never lived, fifty public‑domain celebrities who definitely did—and to document, in painful detail, how each tool read, clustered, mis‑read, and finally betrayed its own biases. The story that follows is equal parts lab‑notebook and reflective essay, woven together in the cadence you would expect from an HCI heavy course post‑mortem: data, screenshots, but also a healthy dose of "why does this matter?"

## Corpus Construction
### 1. Fake half: scraping a GAN firehose
My fake cohort comes straight from ThisPersonDoesNotExist.com, delivered via a minimalist Python scraper (Listing 1). The code is nothing fancy—requests, a timestamp, and Pillow to delete the tell‑tale one‑centimetre artefact that StyleGAN leaves at the bottom of each JPEG.

Let's talk about the code that did the heavy lifting. My GAN "firehose" was powered by a short Python script (`image.py`) that's equal parts utilitarian and forensic. The logic is simple: hit ThisPersonDoesNotExist.com, grab a face, remove the metadata, and—crucially—crop off the bottom centimeter. Why? Because StyleGAN, for all its wizardry, leaves a faint but telltale band at the base of every image, a kind of digital watermark for the attentive and also a fingerprint in the metadata. My script automates this cleanup: it fetches a fresh face, removes the metadata, saves it with a timestamp, slices off the artifact (about 38 pixels, assuming 96 DPI), and drops the result into a neatly organized folder. Loop this fifty times and you've got a bespoke gallery of "people" who never were, each one just a little harder to spot as a fake. The code is nothing fancy, requests, Pillow, a dash of datetime, but it's the backbone of my dataset, and a reminder that even the most advanced AI leaves fingerprints if you know where to look.

*Full code in Listing 1 below.*

### 2. Real half: Wikipedia's red‑carpet detritus 

The next step was to automate the "who's that face?" game—matching each GAN-generated stranger to their closest celebrity doppelgänger. Enter `image_search.py`, a script that's part detective, part gossip columnist, and all API glue. Here's how it works: for every image in my fake gallery, the script encodes the JPEG in base64, then sends it to OpenAI's vision endpoint with a single, pointed prompt—"Which celebrity does this person most resemble?" The model, channeling its inner tabloid, returns a name ("The celebrity that this person most resembles is...")

The script is built for repeatability and transparency. It checks for your OpenAI API key (helpfully prompting you to create a `.env` file if you forget), loops through every image in the `images/fake` directory, and writes the results—one per face—into a timestamped text file. Each run is a snapshot of the model's current "cultural memory," a time capsule of who's famous, who's forgettable, and how the boundaries of resemblance are drawn by a neural net trained on the world's photo archives.

What's fascinating isn't just the matches (some eerily spot-on, others hilariously off-base), but the way the script operationalizes the question of likeness. It's not about pixel-perfect similarity, but about the latent vectors of fame, archetype, and cultural context. The code is straightforward—requests, os, dotenv, a dash of datetime—but the implications are anything but. Each output line is a micro-essay on what it means to "look like" someone in the age of AI, and a reminder that even the most advanced models are, at heart, products of their training data and the biases baked within.

*Full code in Listing 2 below.*

After I had the list of the celebrity doppelgänger. I relied on the Wikimedia's treasure trove of CC‑BY portraits to build the other real half of the dataset.

The final piece of the pipeline was `celebrity_wiki_images.py`, a script that's equal parts web-crawler, regex wrangler, and Wikipedia superfan. Its job: for every GAN face and its OpenAI-matched celebrity, fetch a bona fide portrait from the wilds of Wikimedia Commons. The process is as methodical as it is brittle. First, the script parses the results file from the previous step, extracting pairs of AI-generated filenames and their celebrity lookalikes. Then, for each celebrity, it constructs a Wikipedia URL, scrapes the page for the canonical infobox image (or, failing that, the first available photo), and downloads it into a neatly organized `images/real` directory, renaming each file to match its GAN counterpart. All filenames follow person_YYYYMMDD_HHMMSS+Name.jpg so that later code can map GAN ↔ celebrity pairs by timestamp. Crucially, I did not correct white‑balance, lens glare, or background chaos; those messy cues, as it turns out, become a primary signal of authenticity. As a result, the pictures were not the best celebrity pictures. 

The code is a study in pragmatic scraping: BeautifulSoup for parsing, urllib for URL gymnastics, and a polite one-second delay between requests to avoid angering Wikipedia's guardians. It's robust enough to handle most edge cases—missing infoboxes, alternate spellings, even the occasional redirect—but not invincible. For four celebrities, the script's best efforts were thwarted by Wikipedia's labyrinthine structure or the absence of a usable image. In those cases, I rolled up my sleeves and added the portraits manually, a reminder that even the best automation sometimes needs a human in the loop. 

What I love about this script is how it operationalizes the idea of "ground truth." Each downloaded image is a little act of citation, a way of anchoring the GAN hallucinations to the real, messy world of public figures and open data. The result is a dataset that's not just synthetic-vs-real, but synthetic-vs-culturally-anchored, with every pairing a microcosm of how AI, APIs, and the web conspire to shape our sense of resemblance and identity. 

*Full code in Listing 3 below.*



## Orange Data Mining

### Workflow architecture
I cloned Professor’s images2.ows and Inception V3.

![ODM](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/odm.png)

### Exploratory image grid

The very first visualization after the image embeddings the, Image Grid, already whispered the answer. Real celebrities clustered top‑left and top‑right, GANs bottom‑left and bottom‑right. The invisible axis? Lighting discipline. Wikipedia shots bristle poor picture quality due to copyright issues. GAN images float in diffuse beige limbo.

![imagegrid](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/image-grid.png)

###  Hierarchical view
Running cosine distances through average‑linkage produced a dendrogram whose root split sits at 0.10. Selecting the largest branch (C1) sent thirty‑six images to an Image Viewer; every single one was a GAN portrait with matte skin and no background entropy. Impett & Offert’s dictum kicks in: in reading the network we are reading back the latent photography grammar baked into ImageNet.

![hierarchical](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/hierarchical.png)

### Binary classification
Feeding embeddings into Logistic Regression yielded a confusion matrix to warm any data‑scientist’s heart: 99 % accuracy. The sole error? A paparazzi still of Meryl Strip, Inception read it as “too perfect” and flipped the label. On image viewer the picture looked too bad to label as AI generated/fake. 

![confusion](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/confusion.png) 


> Interpretation. Far from being “too smart,” Inception simply latched onto photometric signatures. My decision to harvest open‑licence celebrity shots from Wikipedia almost guaranteed an easy win: these images carry varied white‑balance, harsh key‑lights, and JPEG noise—all things StyleGAN still struggles to counterfeit convincingly.

### Why lighting keeps leaking the label
Wikipedia’s media‑contrib guidelines encourage bright, front‑lit, high‑resolution head‑shots, whereas the GAN generator defaults to softly lit, centre‑framed faces on neutral bokeh. Inception therefore encodes:

1. Specular hotspots (flash on foreheads, glossy lips) → real

2. Shadow‑less cheeks and Gaussian‑blur backgrounds → fake

Until GAN pipelines begin synthesising stochastic lighting artefacts—or until we curate a corpus whose photographic conditions truly overlap—classification will remain a near‑trivial exercise.

However, I realized although this is a quite straight forward problem for deterministic model like Inception, will the similar logic hold for Generative Model like ChatGPT? 

## Peeking Through GPT‑4’s Eyes — What the Generator Thinks It Sees

For this section I wanted investigate how ChatGPT processes the images. 

### Experimental frame
This experiment is run by `compare_images.py`, a script that stages a face-off between each GAN-generated portrait and its Wikipedia celebrity counterpart. Its logic is as follows: for every pair of images (matched by timestamped filename), the script encodes both as base64 and sends them to OpenAI's GPT-4 Vision API, along with a carefully crafted prompt. The model is asked to rate their facial similarity (1–10), identify which image is AI-generated, and explain its reasoning—always in a rigid, parseable format.

The script automates this process for all image pairs, writing results to a CSV: GAN filename, celebrity filename, similarity score, whether the AI-generated image was correctly identified, and the model's explanation. It handles missing files, logs progress, and ensures that the results are reproducible and ready for downstream analysis. 

What’s fascinating is how this code operationalizes a Turing test for faces—not just asking “can you tell real from fake?” but also “what visual cues tip you off?” The explanations, harvested at scale, become a corpus of machine reasoning about photographic authenticity. In this way, `compare_images.py` closes the loop: from synthetic faces, to cultural referents, to machine judgment, and finally to a dataset that lets us study not just what AI sees, but how it explains what it sees.

I ran the code twice one using ChatGPT 4.1-nano model and another time using the  ChatGPT 4.1 model. Although nano is supposedly the smaller version of the 4.1 model does it thinks in the same way?

*Full code in Listing 4 below.*

To analyze the results from the GPT-4.1's face-off, I wrote a Python script (`analyze_results.py`) that loads the CSV output from `compare_images.py` and computes key statistics: overall accuracy, average similarity scores, and how often the model correctly identified AI-generated images. The script generates visualizations (bar charts, pie charts, word clouds) to show patterns in similarity ratings and the explanations given by the model. It also breaks down which visual cues (like "skin texture" or "lighting") are most often cited in the model's reasoning, and explores how similarity scores relate to detection accuracy using confusion matrices and correlation analysis. This helped me see not just how well the model performed, but *why* it made its decisions, and which features it relied on most when judging authenticity.

*Full code in Listing 5 below.*


###  Run #1 — ChatGPT‑4.1‑nano

| Metric                  | Value            |
| ----------------------- | ---------------- |
| Accuracy                | **4 / 50 = 8 %** |
| Avg similarity          | 3.30 / 10        |
| Correlation (sim ↔ acc) | −0.13            |


![4.1-nano](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/comparison_results_20250510_181420_visualizations.png) 


The nano engine talks a good game—its word‑cloud screams skin texture, lighting, ears—yet it fires blanks. It mistakes GAN images with pristine bokeh for reality and calls out George Clooney as fake because “the skin appears overly smooth.” In effect, nano “sees” surface heuristics but lacks the backstage priors that tie those heuristics to probability of genuineness.

Why so blind? Probably Nano’s compressed parameter budget stores a coarse dictionary of anomaly tokens, but the vision encoder that feeds those tokens into the language head resolves only macroscopic cues. Fine‑grained GAN quirks—ear‑rim clipping, sub‑pixel pore noise—pass under its radar.

### Run #2 — ChatGPT‑4.1

| Metric         | Value               |
| -------------- | ------------------- |
| Accuracy       | **50 / 50 = 100 %** |
| Avg similarity | 4.70 / 10           |
| Correlation    | n/a (no error)      |


![4.1](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/comparison_results_20250510_211939_visualizations.png) 


Here the model doesn’t just parrot “skin texture”; it triangulates lighting anomalies (98 % of explanations), background context (86 %), ear geometry (78 %) and even flags “depth‑of‑field too uniform” when a GAN generator blurs background too smoothly. The similarity‑bins chart is telling: perfect detection across the board—from pairs that look like cousins (sim = 6) to pairs that look like strangers (sim = 1).

What is it actually looking at? The explanations hint at a negative ontology: authenticity equals presence of stochastic error. Flash glare, specular hotspots, uneven white‑balance, JPEG mosquito noise—elements that generative models work hard to iron out—become proof of life. In other words, probably, GPT‑4.1’s camera roll of “real” is a library of photographic imperfections.

This is classic anomaly detection rather than face matching. The model is not asking “Do these faces match ImageNet celebrity memories?” but “Does anything here violate my photographic priors?”

> The practical punch‑line? Your phone’s imperfect selfie is a better proof‑of‑life than any AI‑beautified head‑shot. 


## 2D CLIP

Launching the whole corpus into 2D CLIP with no custom axes produced a remarkably tidy quadrantal split. Reading clockwise:

| Quadrant | Dominant faces            | Shared photometric DNA                            |
| -------- | ------------------------- | ------------------------------------------------- |
| **UL**   | *Male, real, celebrity*   | Studio flashes, tux lapels, blue backdrops        |
| **UR**   | *Female, real, celebrity* | Warm spotlight, professional make‑up, bokeh crowd |
| **LR**   | *Female, GAN*             | Powder‑matte skin, neutral beige background       |
| **LL**   | *Male, GAN*               | Even diffuse lighting, forest‑green bokeh         |


![Initialclustering](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/Initialclustering.png) 


That the network disentangles gender × authenticity with no textual cues is already a lesson in latent bias: Inception/Vit back‑bones that feed CLIP have clearly encoded gendered photographic conventions. 

Zooming the scatter sharpens the story: within each quadrant micro‑islands correspond to head‑pose and background noise. The densest cluster—GAN females—shares a generic LinkedIn‑portrait palette: pastel tops, centre framing, top‑lit catch‑lights. Once again lighting, not craniofacial geometry, does the heavy lifting.

I also tried different keywords in the X and Y axis like Real vs Fake, Celebrity vs Generic etc. Those did not result and telling output. 


## DV Explorer

While 2D CLIP feels like a playful scatter‑paint tool, DV Explorer operates more like a Swiss Army knife for zero‑shot retrieval.

### Zero‑shot query: “human”
Uploading the same 100‑image corpus to DV Explorer’s 5.1 Zero‑Shot module and querying “human” produced an unexpected inversion: all top‑30 hits were GAN faces. Highest cosine score? 0.33.

![dvexplorer.png](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/dvexplorer.png) 

This tells that the GAN pipeline optimises for archetypal humanness. Minimal jewellery, neutral backgrounds, central framing, exactly what the open‑source stable‑diffusion fine‑tunes for.


### Keyword blind spots
Attempting “fake,” “real,” “synthetic” returned a flat similarity field (< 0.05). The model has no anchor for fakeness. In other words, we are smuggling our binary into a space that never asked for it.


### Caption sanity‑check
Running a half‑dozen images through Image Caption deliver anything in terms of authenticity. Again, authenticity is negative space, the caption model speaks photojournalism, not ontological truth.


## Synthesising the Pipelines

Three cross‑tool findings crystallise:

1. Texture = truth. Across dendrograms, CLIP axes, and GPT‑4 explanations, high‑frequency skin detail validates reality.

2. Lighting encodes culture. The difference between flash‑lit and noisy Wikipedia and soft‑lit GANs is more potent than any facial geometry metric.

3. Small models hallucinate. GPT‑4‑nano’s confusion matrix is a cautionary tale: compress the parameter count and you lose the fine‑grained “uncanny detector.”


## Then What Do Machines Actually See?
When Inception sorts faces, it does not start with cheekbone curvature; it starts with light fall‑off, JPEG noise, and accidental background context. When GPT‑4 flags a portrait as fake, it does so because ears are too smooth. Put differently, the detectors’ epistemology is not “realism” but “imperfection.” The absence of a glitch is suspicious.

This has ethical stakes. Social media filters increasingly aim for glitch‑free beauty. Paradoxically, that “improvement” pushes human selfies toward the GAN corner of the latent map, making authentic people look less real to machines. Conversely, GAN researchers are busily injecting stochastic “StyleGAN‑v” imperfections—pores, asymmetry, random chromatic noise—to fool detectors like the full GPT‑4. We are locked in a negative arms race where realism is measured by the quantity of mess.

Here the baggage is a century of photojournalism: flash glare equals authenticity. GANs, trained mostly on high‑key studio shots, swim in a different ocean. The result is a latent space where photography is defined by its errors, not its subjects.

This project began as a curiosity: could I build a miniature Turing test for faces? It ended by reminding me that authenticity is not a binary switch; it is an emergent property of light, texture, and cultural expectation. ODM’s dendrogram, CLIP’s diagonal, DV’s zero‑shot rankings, and GPT‑4’s ear obsession all converge on a simple, unsettling rule: **to look human is to look just a bit broken.**






## Code Listings

- [Listing 1: image.py](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/code/image.py) - Python scraper for ThisPersonDoesNotExist.com
- [Listing 2: image_search.py](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/code/image_search.py) - Script that matches GAN faces to celebrity lookalikes using OpenAI's API
- [Listing 3: celebrity_wiki_images.py](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/code/celebrity_wiki_images.py) - Script that downloads celebrity images from Wikipedia
- [Listing 4: compare_images.py](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/code/compare_images.py) - Script that compares photos using ChatGPT 
- [Listing 5: analyze_results.py](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/code/compare_images.py) - Script that analyze the GPT-4.1 faceoff results





