---
annotations_creators:
- other
language_creators:
- other
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
  discovery:
  - 1M<n<10M
  discoverysmall:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-discourse-marker-prediction
paperswithcode_id: discovery
---


# Dataset Card for Discovery

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

- **Homepage:** https://github.com/synapse-developpement/Discovery
- **Repository:** https://github.com/synapse-developpement/Discovery
- **Paper:** https://www.aclweb.org/anthology/N19-1351/
- **Leaderboard:**
- **Point of Contact:** damien.sileo at kuleuven.be

### Dataset Summary

Discourse marker prediction with 174 markers

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

input : sentence1, sentence2, 
label: marker originally between sentence1 and sentence2

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

Train/Val/Test

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

Aranea english web corpus

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

Self supervised (see paper)

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
@inproceedings{sileo-etal-2019-mining,
    title = "Mining Discourse Markers for Unsupervised Sentence Representation Learning",
    author = "Sileo, Damien  and
      Van De Cruys, Tim  and
      Pradel, Camille  and
      Muller, Philippe",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1351",
    pages = "3477--3486",
    abstract = "Current state of the art systems in NLP heavily rely on manually annotated datasets, which are expensive to construct. Very little work adequately exploits unannotated data {--} such as discourse markers between sentences {--} mainly because of data sparseness and ineffective extraction methods. In the present work, we propose a method to automatically discover sentence pairs with relevant discourse markers, and apply it to massive amounts of data. Our resulting dataset contains 174 discourse markers with at least 10k examples each, even for rare markers such as {``}coincidentally{''} or {``}amazingly{''}. We use the resulting data as supervision for learning transferable sentence embeddings. In addition, we show that even though sentence representation learning through prediction of discourse marker yields state of the art results across different transfer tasks, it{'}s not clear that our models made use of the semantic relation between sentences, thus leaving room for further improvements.",
}
```

### Contributions

Thanks to [@sileod](https://github.com/sileod) for adding this dataset.