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
  en_annotated:
  - 10K<n<100K
  en_neutral:
  - 1K<n<10K
  fi_annotated:
  - 10K<n<100K
  fi_neutral:
  - 10K<n<100K
source_datasets:
- extended|other-OpenSubtitles2016
task_categories:
- text-classification
task_ids:
- intent-classification
- multi-class-classification
- multi-label-classification
- sentiment-classification
paperswithcode_id: xed
---

# Dataset Card for xed_english_finnish

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

- **Homepage:**
- **Repository:** [Github](https://github.com/Helsinki-NLP/XED)
- **Paper:** [Arxiv](https://arxiv.org/abs/2011.01612)
- **Leaderboard:**
- **Point of Contact:**

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

```
{ "sentence": "A confession that you hired [PERSON] ... and are responsible for my father's murder."
   "labels": [1, 6]  # anger, sadness
}
```

### Data Fields

- sentence: a line from the dataset
- labels: labels corresponding to the emotion as an integer

Where the number indicates the emotion in ascending alphabetical order: anger:1, anticipation:2, disgust:3, fear:4, joy:5, sadness:6, surprise:7, trust:8, with neutral:0 where applicable.

### Data Splits

For English:
Number of unique data points: 17528 ('en_annotated' config) + 9675 ('en_neutral' config)
Number of emotions: 8 (+neutral)

For Finnish:
Number of unique data points: 14449 ('fi_annotated' config) + 10794 ('fi_neutral' config)
Number of emotions: 8 (+neutral)

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

License: Creative Commons Attribution 4.0 International License (CC-BY)

### Citation Information

@inproceedings{ohman2020xed,
  title={XED: A Multilingual Dataset for Sentiment Analysis and Emotion Detection},
  author={{\"O}hman, Emily and P{\`a}mies, Marc and Kajava, Kaisla and Tiedemann, J{\"o}rg},
  booktitle={The 28th International Conference on Computational Linguistics (COLING 2020)},
  year={2020}
}

### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@harshalmittal4](https://github.com/harshalmittal4) for adding this dataset.