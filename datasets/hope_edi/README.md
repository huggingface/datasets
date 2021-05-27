---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
  english:
  - en
  malayalam:
  - en
  - ml
  tamil:
  - en
  - ta
licenses:
- cc-by-4.0
multilinguality:
  english:
  - monolingual
  malayalam:
  - multilingual
  tamil:
  - multilingual
size_categories:
  english:
  - 10K<n<100K
  malayalam:
  - 1K<n<10K
  tamil:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-hope-speech-classification
paperswithcode_id: hopeedi
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [Hope Speech Detection for Equality, Diversity, and Inclusion-EACL 2021](https://competitions.codalab.org/competitions/27653#learn_the_details)
- **Repository:** [HopeEDI data repository](https://competitions.codalab.org/competitions/27653#participate-get_data)
- **Paper:** [HopeEDI: A Multilingual Hope Speech Detection Dataset for Equality, Diversity, and Inclusion](https://www.aclweb.org/anthology/2020.peoples-1.5/)
- **Leaderboard:** [Rank list](https://competitions.codalab.org/competitions/27653#results)
- **Point of Contact:** [Bharathi Raja Chakravarthi](mailto:bharathiraja.akr@gmail.com)


### Dataset Summary

A Hope Speech dataset for Equality, Diversity and Inclusion (HopeEDI) containing user-generated comments from the social media platform YouTube with 28,451, 20,198 and 10,705 comments in English, Tamil and Malayalam, respectively, manually labelled as containing hope speech or not. To our knowledge, this is the first research of its kind to annotate hope speech for equality, diversity and inclusion in a multilingual setting. 

### Supported Tasks and Leaderboards

To identify hope speech in the comments/posts in social media.

### Languages

English, Tamil and Malayalam

## Dataset Structure

### Data Instances

An example from the English dataset looks as follows:

| text   | label |
| :------ | :----- |
| all lives matter .without that we never have peace so to me forever all lives matter.           | Hope_speech |
| I think it's cool that you give people a voice to speak out with here on this channel.      | Hope_speech |


An example from the Tamil dataset looks as follows:

| text   | label |
| :------ | :----- |
| Idha solla ivalo naala           | Non_hope_speech |
| இன்று தேசிய பெண் குழந்தைகள் தினம்.. பெண் குழந்தைகளை  போற்றுவோம்..அவர்களை பாதுகாப்போம்... | Hope_speech |


An example from the Malayalam dataset looks as follows:

| text   | label |
| :------ | :----- |
| ഇത്രെയും കഷ്ടപ്പെട്ട് വളർത്തിയ ആ അമ്മയുടെ മുഖം കണ്ടപ്പോൾ കണ്ണ് നിറഞ്ഞു പോയി           | Hope_speech |
| snehikunavar aanayalum pennayalum onnichu jeevikatte..aareyum compel cheythitallalooo..parasparamulla ishtathodeyalle...avarum jeevikatte..🥰🥰 | Hope_speech |

### Data Fields

English
- `text`: English comment.
- `label`: list of the possible values: "Hope_speech", "Non_hope_speech", "not-English"

Tamil
- `text`: Tamil-English code mixed comment.
- `label`: list of the possible values: "Hope_speech", "Non_hope_speech", "not-Tamil"

Malayalam
- `text`: Malayalam-English code mixed comment.
- `label`: list of the possible values: "Hope_speech", "Non_hope_speech", "not-malayalam"


### Data Splits


|              | Tain   | Valid |
| -----        | ------: | -----: |
| English      |  22762 |  2843 |
| Tamil        |  16160 |  2018 |
| Malayalam    |  8564  |  1070 |

## Dataset Creation

### Curation Rationale
Hope is considered significant for the well-being, recuperation and restoration of human life by health professionals.
Hate speech or offensive language detection dataset is not available for code-mixed Tamil and code-mixed Malayalam, and it does not take into account LGBTIQ, women in STEM and other minorities. Thus, we cannot use existing hate speech or offensive language detection datasets to detect hope or non-hope for EDI of minorities.

### Source Data

#### Initial Data Collection and Normalization

For English, we collected data on recent topics of EDI, including women in STEM, LGBTIQ issues, COVID-19, Black Lives Matters, United Kingdom (UK) versus China, United States of America (USA) versus China and Australia versus China from YouTube video comments. The data was collected from videos of people from English-speaking countries, such as Australia, Canada, the Republic of Ireland, United Kingdom, the United States of America and New Zealand.

For Tamil and Malayalam, we collected data from India on the recent topics regarding LGBTIQ issues, COVID-19, women in STEM, the Indo-China war and Dravidian affairs.

#### Who are the source language producers?

Youtube users

### Annotations

#### Annotation process

We created Google forms to collect annotations from annotators. Each form contained a maximum of 100 comments, and each page contained a maximum of 10 comments to maintain the quality of annotation.  We collected information on the gender, educational background and the medium of schooling of the annotator to know the diversity of the annotator and avoid bias. We educated annotators by providing them with YouTube videos on EDI. A minimum of three annotators annotated each form.  

#### Who are the annotators?

For English language comments, annotators were from Australia, the Republic of Ireland, the United Kingdom and the United States of America. For Tamil, we were able to get annotations from both people from the state of Tamil Nadu of India and from Sri Lanka. Most of the annotators were graduate or post-graduate students.

### Personal and Sensitive Information

Social media data is highly sensitive, and even more so when it is related to the minority population, such as the LGBTIQ community or women. We have taken full consideration to minimise the risk associated with individual identity in the data by removing personal information from dataset, such as names but not celebrity names. However, to study EDI, we needed to keep information relating to the following characteristics; racial, gender, sexual orientation, ethnic origin and philosophical beliefs. Annotators were only shown anonymised posts and agreed to make no attempts to contact the comment creator. The dataset will only be made available for research purpose to the researcher who agree to follow ethical
guidelines

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

This work is licensed under a [Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0/.)

### Citation Information

```
@inproceedings{chakravarthi-2020-hopeedi,
title = "{H}ope{EDI}: A Multilingual Hope Speech Detection Dataset for Equality, Diversity, and Inclusion",
author = "Chakravarthi, Bharathi Raja",
booktitle = "Proceedings of the Third Workshop on Computational Modeling of People's Opinions, Personality, and Emotion's in Social Media",
month = dec,
year = "2020",
address = "Barcelona, Spain (Online)",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/2020.peoples-1.5",
pages = "41--53",
abstract = "Over the past few years, systems have been developed to control online content and eliminate abusive, offensive or hate speech content. However, people in power sometimes misuse this form of censorship to obstruct the democratic right of freedom of speech. Therefore, it is imperative that research should take a positive reinforcement approach towards online content that is encouraging, positive and supportive contents. Until now, most studies have focused on solving this problem of negativity in the English language, though the problem is much more than just harmful content. Furthermore, it is multilingual as well. Thus, we have constructed a Hope Speech dataset for Equality, Diversity and Inclusion (HopeEDI) containing user-generated comments from the social media platform YouTube with 28,451, 20,198 and 10,705 comments in English, Tamil and Malayalam, respectively, manually labelled as containing hope speech or not. To our knowledge, this is the first research of its kind to annotate hope speech for equality, diversity and inclusion in a multilingual setting. We determined that the inter-annotator agreement of our dataset using Krippendorff{'}s alpha. Further, we created several baselines to benchmark the resulting dataset and the results have been expressed using precision, recall and F1-score. The dataset is publicly available for the research community. We hope that this resource will spur further research on encouraging inclusive and responsive speech that reinforces positiveness.",
}
```
### Contributions

Thanks to [@jamespaultg](https://github.com/jamespaultg) for adding this dataset.