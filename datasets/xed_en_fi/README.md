---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
- fi
licenses:
- cc-by-4.0
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- 'extended|other-OpenSubtitles2016: Extracting Large Parallel Corpora from Movie
  and TV Subtitles'
task_categories:
- text-classification
task_ids:
- intent-classification
- multi-class-classification
- multi-label-classification
- sentiment-classification
---

# Dataset Card for xed_english_finnish

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/Helsinki-NLP/XED
- **Paper:** https://arxiv.org/pdf/2011.01612.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This is the XED dataset. The dataset consists of emotion annotated movie subtitles from OPUS. We use Plutchik's 8 core emotions to annotate. The data is multilabel. The original annotations have been sourced for mainly English and Finnish.
For the English data we used Stanford NER (named entity recognition) (Finkel et al., 2005) to replace names and locations with the tags: [PERSON] and [LOCATION] respectively.
For the Finnish data, we replaced names and locations using the Turku NER corpus (Luoma et al., 2020).


### Supported Tasks and Leaderboards

Sentiment Classification, Multilabel Classification, Multilabel Classification, Intent Classification

### Languages

English, Finnish

## Dataset Structure

### Data Instances

Example (English):
{ "sentence": "A confession that you hired [PERSON] ... and are responsible for my father's murder ."
   "label":	1, 6
}

### Data Fields

The files are formatted as follows:

sentence1\tlabel1,label2
sentence2\tlabel2,label3,label4...

Where the number indicates the emotion in ascending alphabetical order: anger:1, anticipation:2, disgust:3, fear:4, joy:5, sadness:6, surprise:7, trust:8, with neutral:0 where applicable. 

### Data Splits

For English:
Number of unique data points:	17530 + 6420 (neutral)
Number of emotions:	8 (+pos, neg, neu)

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

License: Creative Commons Attribution 4.0 International License (CC-BY)

### Citation Information

[Needs More Information]