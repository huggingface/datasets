---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- sw
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: null
pretty_name: "Swahili : News Classification Dataset"
---

# Dataset Card for Swahili : News Classification Dataset

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

- **Homepage:** [Homepage for Swahili News classification dataset](https://doi.org/10.5281/zenodo.4300293)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Swahili is spoken by 100-150 million people across East Africa. In Tanzania, it is one of two national languages (the other is English) and it is the official language of instruction in all schools. News in Swahili is an important part of the media sphere in Tanzania.

News contributes to education, technology, and the economic growth of a country, and news in local languages plays an important cultural role in many Africa countries. In the modern age, African languages in news and other spheres are at risk of being lost as English becomes the dominant language in online spaces.

 The Swahili news dataset was created to reduce the gap of using the Swahili language to create NLP technologies and help AI practitioners in Tanzania and across Africa continent to practice their NLP skills to solve different problems in organizations or societies related to Swahili language. Swahili News were collected from different websites that provide news in the Swahili language. I was able to find some websites that provide news in Swahili only and others in different languages including Swahili.

The dataset was created for a specific task of text classification, this means each news content can be categorized into six different topics (Local news, International news , Finance news, Health news, Sports news, and Entertainment news). The dataset comes with a specified train/test split. The train set contains 75% of the dataset and test set contains 25% of the dataset.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language used is Swahili

## Dataset Structure

### Data Instances

A data instance:
```
{
  'text': ' Bodi ya Utalii Tanzania (TTB) imesema, itafanya misafara ya kutangaza utalii kwenye miji minne nchini China kati ya Juni 19 hadi Juni 26 mwaka huu.Misafara hiyo itatembelea miji ya Beijing Juni 19, Shanghai Juni 21, Nanjig Juni 24 na Changsha Juni 26.Mwenyekiti wa bodi TTB, Jaji Mstaafu Thomas Mihayo ameyasema hayo kwenye mkutano na waandishi wa habari jijini Dar es Salaam.“Tunafanya jitihada kuhakikisha tunavuna watalii wengi zaidi kutoka China hasa tukizingatia umuhimu wa soko la sekta ya utalii nchini,” amesema Jaji Mihayo.Novemba 2018 TTB ilifanya ziara kwenye miji ya Beijing, Shanghai, Chengdu, Guangzhou na Hong Kong kutangaza vivutio vya utalii sanjari kuzitangaza safari za ndege za Air Tanzania.Ziara hiyo inaelezwa kuzaa matunda ikiwa ni pamoja na watalii zaidi ya 300 kuja nchini Mei mwaka huu kutembelea vivutio vya utalii.',
  'label': 0
}
```

### Data Fields
- `text`: the news articles
- `label`: the label of the news article

### Data Splits

Dataset contains train and test splits.

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

[More Information Needed]

### Licensing Information

Creative Commons Attribution 4.0 International

### Citation Information

```
@dataset{davis_david_2020_5514203,
  author       = {Davis David},
  title        = {Swahili : News Classification Dataset},
  month        = dec,
  year         = 2020,
  note         = {{The news version contains both train and test sets.}},
  publisher    = {Zenodo},
  version      = {0.2},
  doi          = {10.5281/zenodo.5514203},
  url          = {https://doi.org/10.5281/zenodo.5514203}
}
```

### Contributions

Thanks to [@yvonnegitau](https://github.com/yvonnegitau) for adding this dataset.
