---
title: "Assignment 2"
date: 2025-04-21
categories: 
  - assignment
tags:
  - 
---

## Introduction

The main goal of Thick Mapping, as Professor Wrisley mentioned in the guidelines, is to compare different types of geographically specific data by layering multiple geocoded datasets on a map. Before diving into the project of visualizing the Zanzibar Gazette, I want to lay out the groundwork for you. Hopefully, by the end of this exploration, we will have a thick mapping project that truly connects the dots.

I first learned about Zanzibar because of its beaches when my friend shared how excited they were to visit Zanzibar for their J-term course. I had no idea how rich Zanzibar's history was. Beyond the fascinating and extensive collection on Zanzibar's history at the NYUAD Library, what resonated with me on a human level was Professor Wrisley's statement: "Zanzibar was like modern-day Dubai." I quickly understood Zanzibar was definitely a melting pot of different nationality as key trading hub. This was quickly validated as I looked through the Zanzibar Gazette. The presence of different languages in the same newspaper alone could justify Zanzibar's global identity. However, being a trading hub or having different official languages does not make a city a melting pot as much as the nationalities of its inhabitants do.

For this assignment, my goal was to visualize the various nationalities of the people of Zanzibar. To achieve this, I intentionally curated my dataset by selecting tables that would best support this objective. To do so I was inspired by this statement:

> “Not all training data is equivalent” [1]
> 

Just like the training data, my dataset had to be thoughtfully created in order to effectively visualize the claim of Zanzibar's diversity.

## Source Material and Spatial Elements

I chose the **1918 collection of the Zanzibar Gazette**. The key tables I chose to extract were the Trading Licenses Issued at Zanzibar tables, which included different categories of vendors, their nationality, and residences.

To structure my dataset for spatial analysis and thick mapping, I focused on the following key information from the Gazette tables:

- **To whom issued:** The name or entity to whom the trading license was granted. This provides a unique identifier for each record and sometimes hints at the ethnic or community background of the licensee.
- **Nationality:** The stated nationality of the license holder. This is crucial for visualizing the diversity and cosmopolitan nature of Zanzibar at the time, and for mapping the distribution of different nationalities across the city.
- **Residence:** The place of residence of the licensee, which can be geocoded to plot spatial patterns of where business owners lived or operated. This is a primary spatial element for mapping.
- **Type of Business:** The general category of business for which the license was issued (e.g., hawker, broker, money exchanger etc). This allows for analysis of economic activity and occupational diversity.
- **Issue Location:** The name of the location where the license was issued.

By extracting and organizing these columns, I aimed to create a dataset reflects the multicultural makeup of Zanzibar and allows for the visualization of economic activity and business diversity across different neighborhoods. The spatial elements (residences) enable mapping of business locations, while the business type and size offer a lens into the economic landscape and social stratification of the city during this period.

This approach aligns with the idea that “a consideration of a dataset's conceptual characteristics, in addition to its technical characteristics and downstream utility, can improve the transparency and accountability of AI models...” a principle I applied to better reflect the cultural complexity in the data I chose to represent. [1]

## Modeling the Data with Generative AI

- **Initial Data Structure:** The Zanzibar Gazette tables originally contained only "To whom issued, Nationality, and Residence, Issue Location" headers. However, I realized this structure wouldn't support my visualization needs. Hence, I structured these using these headers “To whom issued, Nationality, Residence, Type of Business, Issue Location, Residence Latitude, Residence Longitude, Issue Location Longitude, and Issue Location Latitude”
- **AI Tools Used:** For this data extraction from Zanzibar Gazette I used the ChatGPT 4.0, ChatGPT O4-mini, Gemini 2.0, Gemini 2.5 Pro, and Mistral.
- **Data Extraction Process:**
    
    The extraction process started with first identifying the tables that I wanted to extract. After identifying the pages, I exported those specific pages from the PDF with their text layer using the “Print as PDF” option of the Mac’s Preview app. Before putting those pages directly to the LLM’s I first wanted to check their text layer’s text contents.To do so I used the following tool https://www.pdfforge.org/online/en/extract-text. After examining the text layer it was quite clear to me that the text layer is extremely distorted. Few common mistakes were: the table structure were completely invisible and incorrect spellings (Eesidence for Residence etc), ditto sign was not represented in the text layers. 
    
    The format of the text layer was as the below format (singular column):
    
    ```
    THE
    OFFICIAL
    GAZETTE
    [January
    14,
    1918.
    Licences
    issued
    at
    Weti,
    Pemba,
    during
    the
    month
    of
    December,
    1917.
    To
    whom
    issued
    Nationality
    Said
    bin
    Moosa
    Mzee
    ```
    
    And as a result after feeding the page in ChatGPT, it did not work. It generated broken texts that had to contextual relation to the page. However, from my past experience of using OCR library (https://www.nutrient.io/blog/tesseract-python-guide/) in Python coupled with recent updates of ChatGPT calling internal tools, I knew instead of the PDF route if I convert the PDF page to images the LLMs might be able to extract the necessary information. The image quality of the PDFs were actually quite good.
    
    To validate my intuition I quickly took a screen shot of a the same PDF page and feed it to ChatGPT with the same earlier prompt *“extract the table information”.* Below is the response:
    
    ```
    To Whom Issued | Nationality | Residence
    Said bin Moosa | Swahili | Weti, Mgini
    Mzee Waissa | Swahili | Pwana
    Moosa bin Haji | Swahili | (Residence unclear)
    Hamdu bin Hamadi Mgunya | Swahili | Msuka, Matangatwani
    Bakari bin Hassan | Swahili | Finya
    ```
    
    After seeing the accurate generation I was quite optimistic that instead of semi automation I could make the entire process near fully automated using LLMs with prompt engineering. 
    
    As I had already settled down on my table headers for the data, I quickly jumped into the prompting. For prompting I used the [official prompting guidelines from ChatGPT](https://cookbook.openai.com/examples/gpt4-1_prompting_guide). From the guide, I found LLMs perform better with structured prompt for heavy tasks instead of plain text prompt/ small instruction sets. After few iterations between different structured prompts, I found prompt with step by step instruction with the expected data structure information and output format performed better. The prompt I used is below:
    
    ```
    You are a document analysis assistant. Your task is to extract structured information from a historical government record. The input is a scanned image of a Zanzibar Gazette page from 1917.
    
    The goal is to extract each license record into a table with the following columns:
    
    Issue Location (always the name at the top of the page, e.g., "Weti, Pemba")
    
    To whom issued
    
    Nationality
    
    Residence
    
    Type of Business (based on the heading under which names are grouped, e.g., "Gold and Silversmith’s Licenses", "Hawkers Licenses")
    
    Please note:
    
    The Issue Location is the place mentioned at the top of the page.
    
    The columns To whom issued, Nationality, and Residence appear explicitly in the document.
    
    The Type of Business should be derived from the header directly above each group of names.
    
    If nationality or residence is marked by (″) ditto sign, mark it as same as the previous record in the table and fill out the table with the last entry of that column instead of ditto.
    
    Each individual listed under a specific license type is a new row in the table.
    
    Format your output as a table, like this:
    
    Issue Location | To whom issued | Nationality | Residence | Type of Business
    Weti, Pemba | Said bin Moosa | Swahili | Weti, Mgini | Gold and Silversmith's Licenses
    Weti, Pemba | Msoma bin Mbwana | Swahili | Tumbe | Hawkers Licenses (Second Class)
    ...	...	...	...	...
    Begin extraction now. Use careful OCR and logical groupings. Ensure consistency in license types and formatting.
    ```
    

After settling down on the prompt the next step was finalize the model. As mentioned earlier I tested the prompt across ChatGPT 4.0, ChatGPT O4-mini, Gemini 2.0, Gemini 2.5 Pro, and Mistral. I created a sample benchmark for comparison. With the same prompt I used same screenshot for all the 4 models and calculated their accuracy, given below:

| Model Name | Correct entry | Incorrect | Empty | Accuracy Percentage |
| --- | --- | --- | --- | --- |
| ChatGPT 4.0 | 160 | 0 | 15  | 95% |
| ChatGPT O4-mini | 175 | 0 | 0 | 100% |
| Gemini 2.0 | 167 | 8 | 0 | 95% |
| Gemini 2.5 Pro | 173 | 2 | 0 | 98% |
| Mistral | 172 | 3 | 0 | 98% |

ChatGPT models’ performed superior than the other models. ChatGPT 4.0 returned empty entries for the ditto marks instead of filling it out based on the last entry. Based on the results I decided to use the ChatGPT O4-mini model for the extraction. Although there might be concern about the prompt techniques, the prompt worked well across all the different models. 

After finalizing the model my contribution to the extraction process was take screenshot of the tables and put that in the LLMs. After generation of the tables, I copied and pasted the data on my excel sheet. However, for the locations’ coordinates I had to rely on manual work rather than any LLMs as after multiple trial I found out the coordinates are all hallucination. As noted, *“The result is often output that is factually wrong yet linguistically fluent and seemingly coherent—these are the ‘hallucinations’ that have become a topic of research interest and (justifiable) public concern.”* [1]

## Geocoding

The most challenging part of this assignment was the geocoding. As the extraction process went smoothly I had 235 data entry, which all had an Issue Location Coordinates and Residence Coordinates. For the Issue Location Coordinates there were less number of unique instances as these are district location details. However, for the residence, there were 97 unique locations. 

| Category | Total Unique | Geocoded | Not found |
| --- | --- | --- | --- |
| Residence | 97 | 94 | 3 |
| Issue Location | 4 | 4 | 0 |

## Final Dataset

[Google Drive Link](https://docs.google.com/spreadsheets/d/1XDTftVYwqoRorn8n-LuKp_MDE83jnuNAsLVjn3FQzyc/edit?usp=sharing)

## Visualization

After I had my dataset ready, I used ChatGPT to generate the Geojson data for the dataset. Using Kepler I tried visualizing the residential address of the licensed business. My idea was due to limited public transportation like now a days, the inhabitants might have lived closer to their businesses. Hence, their residence address could provide us a glimpse of the business cluster of Zanzibar. 

 
![Map](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/kepler.gl.png)

[Kepler Interactive Map](https://kepler.gl/demo/map?mapUrl=https://dl.dropboxusercontent.com/scl/fi/3gnuu6eevp7fx4znia20n/keplergl_zlftmjv.json?rlkey=arf3ntosqik3cr5iuqnchp25u&dl=0)

Based on the map, several significant patterns emerged. Areas like Tumbe, Miembeni, and Malindi emerged as rising commercial centers, showing the highest concentration of issued licenses.

| Residence | License Count |
| --- | --- |
| Tumbe | 15 |
| Miembeni | 15 |
| Malindi | 15 |
| Kengeja | 11 |
| Kizimbani | 11 |

Although number of new businesses in the city center was less compared to the other part of the Zanzibar, the new bussiness opened in the Zanzibar city were mostly capital heavy businesses. On the other hand on the outskirts of the city the new business as mostly second and third class level small businesses. For details, please refer to the Google Sheets. 

The business landscape revealed interesting clusters, with hawkers, theatrical performers, and gold and silversmiths being predominant occupations, indicating a vibrant mobile trade and artisanal economy, which attest to the trading hub identity of the Zanzibar.

![Nationality Breakdown](https://raw.githubusercontent.com/hasiburratul/daah/gh-pages/assets/images/Count.png)

The nationality data showed that while Swahili nationals made up the majority of license holders, there were distinct professional concentrations among other groups. Arab nationals commonly engaged in money lending, while Indian nationals typically operated in commercial and craft trades. I tried visualizing this data on the map. However, failed attempt. 


## Conlcusion

Looking back, I’m surprised by how much I learned through this project. Exploration of Zanzibar's colonial past, the lives of its residents, and how data can tell human stories. This assignment pushed me to think more carefully about how data is collected, shaped, and visualized. Thick mapping turned out to be less about the map itself and more about the choices behind it. From selecting the right tables to geocoding locations with care, each step was part of building a narrative about migration, identity, and commerce in Zanzibar. There were challenges, especially with distorted text layers and hallucinated coordinates, but each setback helped me refine my process. I also gained a new respect for the effort behind building accurate historical datasets. If I had more time, I would expand the project by adding more years or comparing different types of Gazette data. I am especially curious about how patterns of trade or movement changed over time. This was more than a technical task. It felt like a way to give attention back to people and places that have been buried in administrative records. That, to me, is what digital humanities can do best.


---

### References

1. Klein, Lauren, et al. “Provocations from the humanities for generative ai research.” arXiv preprint arXiv:2502.19190 (2025).