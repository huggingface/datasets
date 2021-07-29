---
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- found
languages:
- de
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
- text-scoring
task_ids:
- sentiment-scoring
- structure-prediction-other-pos-tagging
paperswithcode_id: null
---

# Dataset Card for SentiWS

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

- **Homepage:** https://wortschatz.uni-leipzig.de/en/download
- **Repository:** [Needs More Information]
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2010/pdf/490_Paper.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

SentimentWortschatz, or SentiWS for short, is a publicly available German-language resource for sentiment analysis, opinion mining etc. It lists positive and negative polarity bearing words weighted within the interval of [-1; 1] plus their part of speech tag, and if applicable, their inflections. The current version of SentiWS contains around 1,650 positive and 1,800 negative words, which sum up to around 16,000 positive and 18,000 negative word forms incl. their inflections, respectively. It not only contains adjectives and adverbs explicitly expressing a sentiment, but also nouns and verbs implicitly containing one.

### Supported Tasks and Leaderboards

Sentiment-Scoring, Pos-Tagging

### Languages

German

## Dataset Structure

### Data Instances
For pos-tagging:
```
{ 
"word":"Abbau"
"pos_tag": 0
}
```
For sentiment-scoring:
```
{
"word":"Abbau"
"sentiment-score":-0.058
}
``` 

### Data Fields

SentiWS is UTF8-encoded text.
For pos-tagging:
- word: one word as a string,
- pos_tag: the part-of-speech tag of the word as an integer,
For sentiment-scoring:
- word: one word as a string,
- sentiment-score: the sentiment score of the word as a float between -1 and 1,

The POS tags are ["NN", "VVINF", "ADJX", "ADV"] -> ["noun", "verb", "adjective", "adverb"], and positive and negative polarity bearing words are weighted within the interval of [-1, 1].

### Data Splits

 train: 1,650 negative and 1,818 positive words

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

Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported License

### Citation Information
@INPROCEEDINGS{remquahey2010,
title = {SentiWS -- a Publicly Available German-language Resource for Sentiment Analysis},
booktitle = {Proceedings of the 7th International Language Resources and Evaluation (LREC'10)},
author = {Remus, R. and Quasthoff, U. and Heyer, G.},
year = {2010}
}
### Contributions

Thanks to [@harshalmittal4](https://github.com/harshalmittal4) for adding this dataset.