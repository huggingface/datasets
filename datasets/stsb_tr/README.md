---
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
languages:
- tr
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-sts-b
task_categories:
- text-scoring
task_ids:
- semantic-similarity-scoring
pretty_name: Semantic Textual Similarity in Turkish
---

# Dataset Card for stsb_tr

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

- **Homepage:** [https://github.com/verimsu/STSb-TR](https://github.com/verimsu/STSb-TR)
- **Repository:** (STS benchmark Turkish)[https://github.com/verimsu/STSb-TR]
- **Paper:** (Semantic Similarity Based Evaluation for Abstractive News Summarization)[https://aclanthology.org/2021.gem-1.3.pdf]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Figen Beken Fikri](mailto:fbekenfikri@sabanciuniv.edu)

### Dataset Summary

Semantic Textual Similarity benchmark Turkish (STSb-TR) dataset is the machine translated version of [English STS benchmark dataset](https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark) using [Google Cloud Translation API](https://cloud.google.com/translate/docs/basic/translating-text).

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text in the dataset is in Turkish (tr).

## Dataset Structure

### Data Instances

{'score': '1.6',
 'sentence1': 'Bir bebek kaplan bir topla oynuyor.',
 'sentence2': 'Bir bebek bir oyuncak bebekle oynuyor.',
}

### Data Fields

- "genre": a string that represents the genre of the text.
- "dataset": a string that represents the original name of the dataset.
- "year": a string that represents the year of the original dataset.
- "score": a float that represents the semantic similarity score. 0.0 is the lowest and 5.0 is the highest score.
- "sentence1": a string that represents the first sentence.
- "sentence2": a string that represents the second sentence.

### Data Splits

The data has train/validation/test splits having 5749/1500/1379 sentence pairs.

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

[Needs More Information]

### Citation Information

@inproceedings{beken-fikri-etal-2021-semantic,
    title = "Semantic Similarity Based Evaluation for Abstractive News Summarization",
    author = "Beken Fikri, Figen  and Oflazer, Kemal and Yanikoglu, Berrin",
    booktitle = "Proceedings of the 1st Workshop on Natural Language Generation, Evaluation, and Metrics (GEM 2021)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.gem-1.3",
    doi = "10.18653/v1/2021.gem-1.3",
    pages = "24--33",
    abstract = "ROUGE is a widely used evaluation metric in text summarization. However, it is not suitable for the evaluation of abstractive summarization systems as it relies on lexical overlap between the gold standard and the generated summaries. This limitation becomes more apparent for agglutinative languages with very large vocabularies and high type/token ratios. In this paper, we present semantic similarity models for Turkish and apply them as evaluation metrics for an abstractive summarization task. To achieve this, we translated the English STSb dataset into Turkish and presented the first semantic textual similarity dataset for Turkish as well. We showed that our best similarity models have better alignment with average human judgments compared to ROUGE in both Pearson and Spearman correlations.",
}