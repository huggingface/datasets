---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: clinc150
pretty_name: CLINC150
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

- **Homepage:** [Github](https://github.com/clinc/oos-eval/)
- **Repository:** [Github](https://github.com/clinc/oos-eval/)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/D19-1131)
- **Leaderboard:** [PapersWithCode](https://paperswithcode.com/sota/text-classification-on-clinc-oos)
- **Point of Contact:**

### Dataset Summary

Task-oriented dialog systems need to know when a query falls outside their range of supported intents, but current text classification corpora only define label sets that cover every example. We introduce a new dataset that includes queries that are out-of-scope (OOS), i.e., queries that do not fall into any of the system's supported intents. This poses a new challenge because models cannot assume that every query at inference time belongs to a system-supported intent class. Our dataset also covers 150 intent classes over 10 domains, capturing the breadth that a production task-oriented agent must handle. It offers a way of more rigorously and realistically benchmarking text classification in task-driven dialog systems.

### Supported Tasks and Leaderboards

- `intent-classification`: This dataset is for evaluating the performance of intent classification systems in the presence of "out-of-scope" queries, i.e., queries that do not fall into any of the system-supported intent classes. The dataset includes both in-scope and out-of-scope data. [here](https://paperswithcode.com/sota/text-classification-on-clinc-oos).

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:
```
{
    'text' : 'can you walk me through setting up direct deposits to my bank of internet savings account',
    'label' : 108 
}
```

### Data Fields

- text : Textual data
- label : Corresponding to the 150 intent classes over 10 domains

### Data Splits

- Small : Small, in which there are only 50 training queries per each in-scope intent
- Imbalanced : Imbalanced, in which intents have either 25, 50, 75, or 100 training queries.
- Plus : OOS+, in which there are 250 out-of-scope training examples, rather than 100.


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
@inproceedings{larson-etal-2019-evaluation,
    title = "An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction",
    author = "Larson, Stefan  and
      Mahendran, Anish  and
      Peper, Joseph J.  and
      Clarke, Christopher  and
      Lee, Andrew  and
      Hill, Parker  and
      Kummerfeld, Jonathan K.  and
      Leach, Kevin  and
      Laurenzano, Michael A.  and
      Tang, Lingjia  and
      Mars, Jason",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    url = "https://www.aclweb.org/anthology/D19-1131"
}
```
### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.
