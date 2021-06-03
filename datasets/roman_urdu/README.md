---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- ur
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: roman-urdu-data-set
---

# Dataset Card for Roman Urdu Dataset

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

- **Repository:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Roman+Urdu+Data+Set)
- **Point of Contact:** [Zareen Sharf](mailto:zareensharf76@gmail.com)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Urdu

## Dataset Structure

[More Information Needed]

### Data Instances

```
Wah je wah,Positive,
```

### Data Fields

Each row consists of a short Urdu text, followed by a sentiment label. The labels are one of `Positive`, `Negative`, and `Neutral`. Note that the original source file is a comma-separated values file.

* `sentence`: A short Urdu text
* `label`: One of `Positive`, `Negative`, and `Neutral`, indicating the polarity of the sentiment expressed in the sentence

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

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

[More Information Needed]

### Citation Information

```
@InProceedings{Sharf:2018,
  title     = "Performing Natural Language Processing on Roman Urdu Datasets",
  authors   = "Zareen Sharf and Saif Ur Rahman",
  booktitle = "International Journal of Computer Science and Network Security",
  volume    = "18",
  number    = "1",
  pages     = "141-148",
  year      = "2018"
}

@misc{Dua:2019,
  author      = "Dua, Dheeru and Graff, Casey",
  year        = "2017",
  title       = "{UCI} Machine Learning Repository",
  url         = "http://archive.ics.uci.edu/ml",
  institution = "University of California, Irvine, School of Information and Computer Sciences"
}
```

### Contributions

Thanks to [@jaketae](https://github.com/jaketae) for adding this dataset.