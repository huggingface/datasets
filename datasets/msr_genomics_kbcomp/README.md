---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- other-my-license
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-NCI-PID-PubMed Genomics Knowledge Base Completion Dataset
paperswithcode_id: null
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

- **Homepage:** [NCI-PID-PubMed Genomics Knowledge Base Completion Dataset](https://msropendata.com/datasets/80b4f6e8-5d7c-4abc-9c79-2e51dfedd791)
- **Repository:** [NCI-PID-PubMed Genomics Knowledge Base Completion Dataset](NCI-PID-PubMed Genomics Knowledge Base Completion Dataset)
- **Paper:** [Compositional Learning of Embeddings for Relation Paths in Knowledge Base and Text](https://www.aclweb.org/anthology/P16-1136/)
- **Point of Contact:** [Kristina Toutanova](mailto:kristout@google.com)


### Dataset Summary
 
The database is derived from the NCI PID Pathway Interaction Database, and the textual mentions are extracted from cooccurring pairs of genes in PubMed abstracts, processed and annotated by Literome (Poon et al. 2014). This dataset was used in the paper “Compositional Learning of Embeddings for Relation Paths in Knowledge Bases and Text” (Toutanova, Lin, Yih, Poon, and Quirk, 2016). More details can be found in the included README.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

NCI-PID-PubMed Genomics Knowledge Base Completion Dataset

This dataset includes a database of regulation relationships among genes and corresponding textual mentions of pairs of genes in PubMed article abstracts.
The database is derived from the NCI PID Pathway Interaction Database, and the textual mentions are extracted from cooccurring pairs of genes in PubMed abstracts, processed and annotated by Literome. This dataset was used in the paper "Compositional Learning of Embeddings for Relation Paths in Knowledge Bases and Text". 

FILE FORMAT DETAILS

The files train.txt, valid.txt, and test.text contain the training, development, and test set knowledge base (database of regulation relationships) triples used in.
The file text.txt contains the textual triples derived from PubMed via entity linking and processing with Literome. The textual mentions were used for knowledge base completion in.

The separator is a tab character; the relations are Positive_regulation, Negative_regulation, and Family (Family relationships occur only in the training set).

The format is:

| GENE1    | relation   |    GENE2        |

Example:
ABL1    Positive_regulation     CDK2

The separator is a tab character; the relations are Positive_regulation, Negative_regulation, and Family (Family relationships occur only in the training set).

### Data Instances

[More Information Needed]

### Data Fields

The format is:

| GENE1    | relation   |    GENE2        |

### Data Splits

[More Information Needed]

## Dataset Creation

[More Information Needed]

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

[More Information Needed]

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

[More Information Needed]

### Dataset Curators

The dataset was initially created by Kristina Toutanova, Victoria Lin, Wen-tau Yih, Hoifung Poon and Chris Quirk, during work done at Microsoft Research.

### Licensing Information

[More Information Needed]

### Citation Information

```
@inproceedings{toutanova-etal-2016-compositional,
    title = "Compositional Learning of Embeddings for Relation Paths in Knowledge Base and Text",
    author = "Toutanova, Kristina  and
      Lin, Victoria  and
      Yih, Wen-tau  and
      Poon, Hoifung  and
      Quirk, Chris",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1136",
    doi = "10.18653/v1/P16-1136",
    pages = "1434--1444",
}
```

### Contributions

Thanks to [@manandey](https://github.com/manandey) for adding this dataset.