---
title: "Assignment 1"
date: 2025-03-05
categories: 
  - assignment
tags:
  - 
  - 
---


## Introduction

Since Elon Musk's take over of the Twitter now X as a regular user I have only came accross two themes of posts on my feed—American Politics and AI. I understood the rationale behind my feed being flooded with AI updates as I only follow AI influentials. So, it took me sometime to understand why all of a sudden I am being flooded with American politics updates. Due to Elon's posts being amplified and his enagement with politics more and more people from the tech community was engaging with American politics posts. Hence, as a likely follower of tech community X algorithm decieded I might be a suitable candidate for American politics posts. Closer to the election the duality of these two themes—American Politics and AI—merged into one. On my feed, I was seeing posts from both sides of the isle, some advocating for the GOP to remove red taping to accelerate AI, and others warning how without proper alignment AI could destroy humanity. And the most important discourse of all was: Is LLM/ChatGPT biased towards specific party/ideology? However, even though I was quite worried about the implications and consequences of the election on the future of AI advancements, my biggest curiosity lay in this question: **If ChatGPT were to run for president, how would it sound, and could it hold a candle to real politicians' rhetorical styles? What would it focus on?** This curiosity led me to the topic of this assignment. For the assignment on working with a corpus, I decided to analyze real speeches from presidential candidates and AI generated speeches. 


## Corpus

Although there were quite a few intense speeches along the presidential campaign, some more influential than the others, I came to the conclusion that national convention speeches could be the most accurate reflection of their campaign, and it would be easier to generate a single speech using ChatGPT mentioning this is for national conventions. I got the entire transcript of both Harris and Trump’s speech from the New York Times. 

[Full transcript of Harris's speech NYT](https://www.nytimes.com/2024/08/23/us/politics/kamala-harris-speech-transcript.html) 

[Full transcript of Trump's speech NYT](https://www.nytimes.com/2024/07/19/us/politics/trump-rnc-speech-transcript.html)

I cleaned up both the speech and saved those in seperate text file for Voyant and R analysis for later. 

[Harris's speech](/assets/data/harris.txt)

[Trump's speech](/assets/data/trump.txt)

After this came the tricky part: how to generate a USA presidential convention speech using the ChatGPT. The first time I tried using ChatGPT, I got a red flag that I was violating the community guidelines. I realized this approach would not work. I had the idea of using Perplexity to first comb through the national newspaper and highlight the national issues of the USA. Then I prompted at Perplexity to write an introduction about a fictional country called *“Atlantica”*. 

[Introduction to Atlantica](/assets/data/atlantica.txt)


Skimming through the ChatGPT-generated speech, I felt it was a very policy-driven speech; hence, another idea popped in my head: *what if I ask ChatGPT explicitly to generate speech as if it were a right-wing candidate?* The rationale behind this was an article on [Forbes magazine titled “ChatGPT Has Liberal Bias, Say Researchers”](https://www.forbes.com/sites/emmawoollacott/2023/08/17/chatgpt-has-liberal-bias-say-researchers/).

I wanted to explore how diverse the result would be and was hoping to get some unexpected results in the analysis stage. Therefore, in the end, my corpus was built on these four texts:

- Kamala Harris's speech from DNC.
- Donald Trump's speech from RNC.
- A Default ChatGPT Speech, prompted simply with “You are running for president in Atlantica...”
- A ChatGPT Right-Wing Speech, where I explicitly asked ChatGPT to craft a right-wing presidential candidate speech for Atlantica.


## Analysis

For the analysis, I had three distinct questions in my head. These questions are as follows:

1. How does ChatGPT approach political discourse in the absence of personal experiences or specific instructions about tone?

2. Does ChatGPT generate the distinctive rhetorical styles?

3. Which words, sentiments, and thematic clusters define each speaker, and what do those differences say about authenticity, emotional appeal, and rhetorical technique?


### Voyant Exploration

- Quick Summary of Kamala Harris's speech
<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Summary/?stopList=keywords-e3b12ec4f35735a1f3077e56687569db&corpus=9ae067fa96b9d3da5738b011f7026ee6'></iframe>


<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Cirrus/?stopList=keywords-e3b12ec4f35735a1f3077e56687569db&whiteList=&corpus=9ae067fa96b9d3da5738b011f7026ee6'></iframe>

<br>

- Quick Summary of Donald Trump's speech
<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Summary/?stopList=keywords-84b6c8143c21fd247c33fe3a1cde23f7&corpus=52995135c033f1806c926a0681ff8d4a'></iframe>


<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Cirrus/?stopList=keywords-84b6c8143c21fd247c33fe3a1cde23f7&whiteList=&corpus=52995135c033f1806c926a0681ff8d4a'></iframe>

<br>

- Quick Summary of ChatGPT Default speech
<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Summary/?corpus=10c97dd225f26c128584c109911c2c54'></iframe>


<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Cirrus/?corpus=10c97dd225f26c128584c109911c2c54'></iframe>


<br>

- Quick Summary of ChatGPT Right-wing speech
<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Summary/?corpus=5b6f03d16caa558142eb827bebffab8d'></iframe>

<iframe style='width: 444px; height: 408px;' src='https://voyant-tools.org/tool/Cirrus/?corpus=5b6f03d16caa558142eb827bebffab8d'></iframe>


### R Exploration

In R notebook, I first normalized the texts by removing extraneous punctuation and standardized letter casing. Then I started with the most frequent words analysis of all the texts.

![Most Frequent Words](/assets/images/MFW_Trump.png)

![Most Frequent Words](/assets/images/MFW_Harris.png)

![Most Frequent Words](/assets/images/MFW_ChatGPT.png)

![Most Frequent Words](/assets/images/MFW_ChatGPTR.png)

From looking at the most frequent words few patterns started to emerge. For Example:

- Donald Trump's speech was blend of repeated pronouns indicated direct enagement and had a lot of superlatives.

- Kamala Harris's speech was framed around challening Donald Trump and perhaps highlighted reproductive rights through word choices like mother, freedom, security. 

- For both Harris and Trump border highlighted word.

- ChatGPT default is heavily oriented toward broad-scale issues and policy implications.

- ChatGPT right-wing highlighted values like sovereignty, threat narratives, and national security. 

Although Harris and Trump include direct enagement phrases and emotive words, ChatGPT in both guises leans toward more generic policy or ideological phrases.

Secondly, I explored how in all four texts words were used, highlighting the similarities and differences between their word choices. 

![Words Usage Comparison](/assets/images/WUC_ChatGPT.png)

![Words Usage Comparison](/assets/images/WUC_ChatGPTR.png)

![Words Usage Comparison](/assets/images/WUC_HarrisTrump.png)

![Words Usage Comparison](/assets/images/WUC_ChatGPT&R.png)

After looking at the Word Usage Comparison across all 4 texts, it was evident that there is a little similarity between word usage across all 4 texts. Hence, I decided to also explore the Top Differentially Used Words. With the help of Copilot, I added the extra code blocks for this. The idea behind this was to be able to clearly answer which words appear disproportionately more in one speech than another? 

![Differentially Used Words](/assets/images/DW_HarrisTrump.png)

![Differentially Used Words](/assets/images/DW_Harris.png)

![Differentially Used Words](/assets/images/DW_Trump.png)

![Differentially Used Words](/assets/images/DW_HarrisR.png)

![Differentially Used Words](/assets/images/DW_TrumpR.png)



Even after looking at the raw frequency of different words in the texts, it was clear that a few words that do not carry a lot of meaning are probably overshadowing unique words. My rationale was that both Harris and Trump used the word border, for example, and looking into raw frequency would not give us a clear picture about whether their individual speeches were unique. To understand this, I used perplexity to find out if there was a way to determine what makes a speech unique. I came across this metric called TF-IDF (Term Frequency–Inverse Document Frequency) that highlights words that are particularly important to a given text compared to the entire corpus, so I looked into resources and, with the help of Copilot, easily could modify the R code to visualize this. 


![TFIDF](/assets/images/TFIDF.png)

Looking at this visualization it was clear what each speech uniquely cared about compared to others. 


The next thing that I stumbled upon was what are the themes of individual speeches. From the Voyant tool, I found it was quite interesting to know which words are often used together, so I used Perplexity with the idea that the occurrence of similar words together repeatedly can give us a sense of themes in the speeches. I found two separate tools to visualize this Latent Dirichlet Allocation (LDA) and co-occurance network. These helps us to group words into overarching “topics” that frequently appear together across the entire text

![LDA](/assets/images/LDA_Trump.png)
![LDA](/assets/images/LDA_Harris.png)
![LDA](/assets/images/LDA_ChatGPT.png)
![LDA](/assets/images/LDA_ChatGPTR.png)

To better understand the sequence of words:
![FWC](/assets/images/FWC_Harris.png)
![FWC](/assets/images/FWC_Trump.png)
![FWC](/assets/images/FWC_ChatGPT.png)
![FWC](/assets/images/FWC_ChatGPTR.png)

As Trump’s speech was the longest and looked like a lot of repetition of pronouns, I wanted to check the lexical diversity of the text to understand how each speech was made up. Was it similar words put together again and again to prolong the speech or different words/ideas were proposed? 

![Lexical](/assets/images/Lexical%20Diversity.png)

After looking into these comparisons, the first thing that stuck out to me was the politician's use of word was actively trying to generate emotion among the supporters. Trump's use of superlatives and Kamala’s use of words to relate to the fellow Americans were examples of that. Where’s the both versions of ChatGPT were either talking about policy or ideologies. To check this hypothesis, I wanted to run some sentiment analysis on the text. I went back to the notebook and, with help of Copilot, coded a simple sentiment analysis tool using the R library that would assign a numerical value to each text, reflecting whether its language skews positive, negative, or neutral.

![Sentiment Analysis](/assets/images/sentiment.png)

The emotional coloration of the speech supported my initial hypothesis. ChatGPT severaly lacked to evoke positive sentiment. The real politicians amazingly blended negativity toward opponents with calls for hope and progress—striking an emotional balance that would resonates with voters. 

After looking at differentially used words, sentiment, co-occurrence, and topic modeling, I still wanted a single metric that might capture overall similarity irrespective of the length of the speeches. So, I used Pearson correlation of word frequencies. If two speeches use words in similar proportions across the entire vocabulary, they exhibit a higher correlation.

![cosign](/assets/images/cosign.png)

## Thoughts
Throughtout the exploration and analysis the most recurring theme was ChatGPT's outputs were heavy on policy language but short on the emotional hooks. 

> "The problem is that when you analyze a lot of data you get a lot of false hits or false positives. The messier the data, the more false hits you get. The subtler the questions asked of the data, the more nuanced and even misleading the answers are likely to be." - False Positives: Opportunities and Dangers in Big-Data
Text Analysis

This quote really crystalizes the trade-off between ChatGPT’s impressive breadth (it can mention virtually any policy or slogan) and its inability to capture the “messier,” subtler emotional layers of a live political speech. ChatGPT is unlikely recreate Donald Trump’s repeated “we’re/they’re” appeals. 


> "The central thesis of our book is that [...] complex systems have thermodynamical properties [...] which preclude the collection of data [...] that is representative of that system’s behaviour in the future." - LLMs and practical knowledge: What is intelligence?

Is LLM truly intelligent? In actual campaign speech, politicians balance critiques of their opponents with positivity about their vision or achievements. But ChatGPT latched onto negative phrases like “attack,” “radical,” and “invasion” without adding the uplifting or patriotic language that real candidates use to inspire their base. While ChatGPT can find the “right” keywords for a conservative stump speech, it has no intuitive sense of how to pivot from alarm to hope the way a seasoned politician does and this became clear from the sentiment analysis.

But this is the worst version of ChatGPT we will ever see in our lifetime. Could ChatGPT eventually become good enough to mimic this fine balance like a real politician? It is more likely than not. If AI can even mass-produce semi-believable speeches, it could overshadow real candidate messages or flood voters with confusion about who said what.

I am quite surprised by the unexpectedly low correlation between ChatGPT and real speeches and biggest surprise for me was discovering that ChatGPT Right-Wing correlated more with Harris than with Trump, in terms of total word usage patterns. It underlined that simply sharing ideological themes (e.g., law and order) doesn’t equate to adopting a politician’s rhetorical DNA. But now you might think probably ChatGPT were not trained on any right-wing speech due to bias of tech community. I want to surprise you on that. Following is the last two line of ChatGPT right-wing speech:

> #### *"Together, we will Make Atlantica Great Again. Thank you, and may God bless Atlantica."* ####

I know you can hear the voice. Perhaps the lack of correlation is due to the fact that even probabilistic model like ChatGPT failed to predict the RNC speech!