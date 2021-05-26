---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
paperswithcode_id: null
---

# Dataset Card for Fake News English

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
- **Homepage: https://dl.acm.org/doi/10.1145/3201064.3201100** 
- **Repository: https://github.com/jgolbeck/fakenews/**
- **Paper: https://doi.org/10.1145/3201064.3201100**
- **Leaderboard:**
- **Point of Contact: Jennifer Golbeck (http://www.jengolbeck.com)**

### Dataset Summary
This dataset contains URLs of news articles classified as either fake or satire. The articles classified as fake also have the URL of a rebutting article.

### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
English

## Dataset Structure

### Data Instances
```
{
"article_number": 102 ,
"url_of_article": https://newslo.com/roger-stone-blames-obama-possibility-trump-alzheimers-attacks-president-caused-severe-stress/ ,
"fake_or_satire": 1,  # Fake
"url_of_rebutting_article": https://www.snopes.com/fact-check/donald-trumps-intelligence-quotient/
}
```

### Data Fields
- article_number: An integer used as an index for each row
- url_of_article: A string which contains URL of an article to be assessed and classified as either Fake or Satire
- fake_or_satire: A classlabel for the above variable which can take two values- Fake (1) and Satire (0)
- url_of_rebutting_article: A string which contains a URL of the article used to refute the article in question (present - in url_of_article)

### Data Splits
This dataset is not split, only the train split is available.

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

### Contributions

Thanks to [@MisbahKhan789](https://github.com/MisbahKhan789), [@lhoestq](https://github.com/lhoestq) for adding this dataset.