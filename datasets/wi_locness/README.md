---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
- other-language-learner
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-grammatical-error-correction
---

# Dataset Card for Cambridge English Write & Improve + LOCNESS Dataset

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://www.cl.cam.ac.uk/research/nl/bea2019st/#data
- **Repository:**
- **Paper:** https://www.aclweb.org/anthology/W19-4406/
- **Leaderboard:** https://www.cl.cam.ac.uk/research/nl/bea2019st/#results
- **Point of Contact:**

### Dataset Summary

Write & Improve (Yannakoudakis et al., 2018) is an online web platform that assists non-native English students with their writing. Specifically, students from around the world submit letters, stories, articles and essays in response to various prompts, and the W&I system provides instant feedback. Since W&I went live in 2014, W&I annotators have manually annotated some of these submissions and assigned them a CEFR level.

The LOCNESS corpus (Granger, 1998) consists of essays written by native English students. It was originally compiled by researchers at the Centre for English Corpus Linguistics at the University of Louvain. Since native English students also sometimes make mistakes, we asked the W&I annotators to annotate a subsection of LOCNESS so researchers can test the effectiveness of their systems on the full range of English levels and abilities.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

[More Information Needed]

### Citation Information

```
@inproceedings{bryant-etal-2019-bea,
    title = "The {BEA}-2019 Shared Task on Grammatical Error Correction",
    author = "Bryant, Christopher  and
      Felice, Mariano  and
      Andersen, {\O}istein E.  and
      Briscoe, Ted",
    booktitle = "Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications",
    month = aug,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-4406",
    doi = "10.18653/v1/W19-4406",
    pages = "52--75",
    abstract = "This paper reports on the BEA-2019 Shared Task on Grammatical Error Correction (GEC). As with the CoNLL-2014 shared task, participants are required to correct all types of errors in test data. One of the main contributions of the BEA-2019 shared task is the introduction of a new dataset, the Write{\&}Improve+LOCNESS corpus, which represents a wider range of native and learner English levels and abilities. Another contribution is the introduction of tracks, which control the amount of annotated data available to participants. Systems are evaluated in terms of ERRANT F{\_}0.5, which allows us to report a much wider range of performance statistics. The competition was hosted on Codalab and remains open for further submissions on the blind test set.",
}
```

### Contributions

Thanks to [@aseifert](https://github.com/aseifert) for adding this dataset.