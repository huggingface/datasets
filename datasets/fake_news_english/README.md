---
YAML tags:
- copy-paste the tags obtained with the tagging app in tags.json file
---

# Dataset Card for Fake News English

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description
- **Homepage: https://dl.acm.org/doi/10.1145/3201064.3201100** 
- **Repository: https://github.com/jgolbeck/fakenews/raw/master/FakeNewsData.zip**
- **Paper: https://doi.org/10.1145/3201064.3201100 **
- **Leaderboard: **
- **Point of Contact: Jennifer Golbeck (http://www.jengolbeck.com)**

### Dataset Summary
"""Fake news has become a major societal issue and a technical chal- lenge for social media companies 
to identify. This content is difficult to identify because the term "fake news" covers intentionally 
false, deceptive stories as well as factual errors, satire, and sometimes, stories that a person just 
does not like. Addressing the problem requires clear de nitions and examples. In this work, we present 
a dataset of fake news and satire stories that are hand coded, verified, and, in the case of fake news, 
include rebutting stories. We also include a thematic content analysis of the articles, identifying 
major themes that include hyperbolic support or condemnation of a gure, conspiracy theories, racist 
themes, and discrediting of reliable sources. In addition to releasing this dataset for research use, 
we analyze it and show results based on language that are promising for classi cation purposes. 
Overall, our contribution of a dataset and initial analysis are designed to support future work by 
fake news researchers."""

### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
English

## Dataset Structure

### Data Instances
{
"article_number": "102",
"url_of_article": "https://newslo.com/roger-stone-blames-obama-possibility-trump-alzheimers-attacks-president-caused-severe-stress/",
"fake_or_satire": "Fake",
"url_of_rebutting_article": "https://www.snopes.com/fact-check/donald-trumps-intelligence-quotient/"
}

### Data Fields
article_number (Integer)
url_of_article (String)
fake_or_satire (String)
url_of_rebutting_article (String)

### Data Splits
Train

## Dataset Creation

### Curation Rationale
[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators
Golbeck, Jennifer
Everett, Jennine 
Falak, Waleed
Gieringer, Carl
Graney, Jack 
Hoffman, Kelly 
Huth, Lindsay 
Ma, Zhenya 
Jha, Mayanka 
Khan, Misbah 
Kori, Varsha 
Mauriello, Matthew 
Lewis, Elo 
Mirano, George 
IV, William 
Mussenden, Sean 
Nelson, Tammie 
Mcwillie, Sean 
Pant, Akshat 
Cheakalos, Paul

### Licensing Information
[More Information Needed]

### Citation Information
@inproceedings{inproceedings,
author = {Golbeck, Jennifer and Everett, Jennine and Falak, Waleed and Gieringer, Carl and Graney, Jack and Hoffman, Kelly and Huth, Lindsay and Ma, Zhenya and Jha, Mayanka and Khan, Misbah and Kori, Varsha and Mauriello, Matthew and Lewis, Elo and Mirano, George and IV, William and Mussenden, Sean and Nelson, Tammie and Mcwillie, Sean and Pant, Akshat and Cheakalos, Paul},
year = {2018},
month = {05},
pages = {17-21},
title = {Fake News vs Satire: A Dataset and Analysis},
doi = {10.1145/3201064.3201100}
}
