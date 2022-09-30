---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-scoring
- sentiment-classification
- sentiment-scoring
paperswithcode_id: sst
pretty_name: Stanford Sentiment Treebank
configs:
- default
- dictionary
- ptb
---

# Dataset Card for sst

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

- **Homepage:** https://nlp.stanford.edu/sentiment/index.html
- **Repository:** [Needs More Information]
- **Paper:** [Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank](https://www.aclweb.org/anthology/D13-1170/)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The Stanford Sentiment Treebank is the first corpus with fully labeled parse trees that allows for a complete analysis of the compositional effects of sentiment in language.

### Supported Tasks and Leaderboards

- `sentiment-scoring`: Each complete sentence is annotated with a `float` label that indicates its level of positive sentiment from 0.0 to 1.0. One can decide to use only complete sentences or to include the contributions of the sub-sentences (aka phrases). The labels for each phrase are included in the `dictionary` configuration. To obtain all the phrases in a sentence we need to visit the parse tree included with each example. In contrast, the `ptb` configuration explicitly provides all the labelled parse trees in Penn Treebank format. Here the labels are binned in 5 bins from 0 to 4.
- `sentiment-classification`: We can transform the above into a binary sentiment classification task by rounding each label to 0 or 1.

### Languages

The text in the dataset is in English

## Dataset Structure

### Data Instances

For the `default` configuration:
```
{'label': 0.7222200036048889,
 'sentence': 'Yet the act is still charming here .',
 'tokens': 'Yet|the|act|is|still|charming|here|.',
 'tree': '15|13|13|10|9|9|11|12|10|11|12|14|14|15|0'}
```

For the `dictionary` configuration:
```
{'label': 0.7361099720001221, 
'phrase': 'still charming'}
```

For the `ptb` configuration:
```
{'ptb_tree': '(3 (2 Yet) (3 (2 (2 the) (2 act)) (3 (4 (3 (2 is) (3 (2 still) (4 charming))) (2 here)) (2 .))))'}
```

### Data Fields

- `sentence`: a complete sentence expressing an opinion about a film
- `label`: the degree of "positivity" of the opinion, on a scale between 0.0 and 1.0
- `tokens`: a sequence of tokens that form a sentence
- `tree`: a sentence parse tree formatted as a parent pointer tree
- `phrase`: a sub-sentence of a complete sentence
- `ptb_tree`: a sentence parse tree formatted in Penn Treebank-style, where each component's degree of positive sentiment is labelled on a scale from 0 to 4

### Data Splits

The set of complete sentences (both `default` and `ptb` configurations) is split into a training, validation and test set. The `dictionary` configuration has only one split as it is used for reference rather than for learning.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

Rotten Tomatoes reviewers.

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

```
@inproceedings{socher-etal-2013-recursive,
    title = "Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank",
    author = "Socher, Richard  and
      Perelygin, Alex  and
      Wu, Jean  and
      Chuang, Jason  and
      Manning, Christopher D.  and
      Ng, Andrew  and
      Potts, Christopher",
    booktitle = "Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing",
    month = oct,
    year = "2013",
    address = "Seattle, Washington, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D13-1170",
    pages = "1631--1642",
}
```

### Contributions

Thanks to [@patpizio](https://github.com/patpizio) for adding this dataset.
