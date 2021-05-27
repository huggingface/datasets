---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- en
licenses:
- cc0-1.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-retrieval
task_ids:
- document-retrieval
- entity-linking-retrieval
- explanation-generation
- fact-checking-retrieval
- machine-translation
- summarization
- text-simplification
paperswithcode_id: null
---

# Dataset Card For arXiv Dataset

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

- **Homepage:** [Kaggle arXiv Dataset Homepage](https://www.kaggle.com/Cornell-University/arxiv)
- **Repository:** 
- **Paper:** [On the Use of ArXiv as a Dataset](https://arxiv.org/abs/1905.00075)
- **Leaderboard:** 
- **Point of Contact:** [Matt Bierbaum](mailto:matt.bierbaum@gmail.com)

### Dataset Summary

A dataset of 1.7 million arXiv articles for applications like trend analysis, paper recommender engines, category prediction, co-citation networks, knowledge graph construction and semantic search interfaces.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is English

## Dataset Structure

### Data Instances

This dataset is a mirror of the original ArXiv data. Because the full dataset is rather large (1.1TB and growing), this dataset provides only a metadata file in the json format. An example is given below

```
{'id': '0704.0002',
 'submitter': 'Louis Theran',
 'authors': 'Ileana Streinu and Louis Theran',
 'title': 'Sparsity-certifying Graph Decompositions',
 'comments': 'To appear in Graphs and Combinatorics',
 'journal-ref': None,
 'doi': None,
 'report-no': None,
 'categories': 'math.CO cs.CG',
 'license': 'http://arxiv.org/licenses/nonexclusive-distrib/1.0/',
 'abstract': '  We describe a new algorithm, the $(k,\\ell)$-pebble game with colors, and use\nit obtain a characterization of the family of $(k,\\ell)$-sparse graphs and\nalgorithmic solutions to a family of problems concerning tree decompositions of\ngraphs. Special instances of sparse graphs appear in rigidity theory and have\nreceived increased attention in recent years. In particular, our colored\npebbles generalize and strengthen the previous results of Lee and Streinu and\ngive a new proof of the Tutte-Nash-Williams characterization of arboricity. We\nalso present a new decomposition that certifies sparsity based on the\n$(k,\\ell)$-pebble game with colors. Our work also exposes connections between\npebble game algorithms and previous sparse graph algorithms by Gabow, Gabow and\nWestermann and Hendrickson.\n',
 'update_date': '2008-12-13'}
 ```

### Data Fields

- `id`: ArXiv ID (can be used to access the paper)
- `submitter`: Who submitted the paper
- `authors`: Authors of the paper
- `title`: Title of the paper
- `comments`: Additional info, such as number of pages and figures
- `journal-ref`: Information about the journal the paper was published in
- `doi`: [Digital Object Identifier](https://www.doi.org)
- `report-no`: Report Number
- `abstract`: The abstract of the paper
- `categories`: Categories / tags in the ArXiv system


### Data Splits

The data was not splited.

## Dataset Creation

### Curation Rationale

For nearly 30 years, ArXiv has served the public and research communities by providing open access to scholarly articles, from the vast branches of physics to the many subdisciplines of computer science to everything in between, including math, statistics, electrical engineering, quantitative biology, and economics. This rich corpus of information offers significant, but sometimes overwhelming depth. In these times of unique global challenges, efficient extraction of insights from data is essential. To help make the arXiv more accessible, a free, open pipeline on Kaggle to the machine-readable arXiv dataset: a repository of 1.7 million articles, with relevant features such as article titles, authors, categories, abstracts, full text PDFs, and more is presented to empower new use cases that can lead to the exploration of richer machine learning techniques that combine multi-modal features towards applications like trend analysis, paper recommender engines, category prediction, co-citation networks, knowledge graph construction and semantic search interfaces.

### Source Data

This data is based on arXiv papers.
[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

This dataset contains no annotations.

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

The original data is maintained by [ArXiv](https://arxiv.org/)

### Licensing Information

The data is under the [Creative Commons CC0 1.0 Universal Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/)

### Citation Information

```
@misc{clement2019arxiv,
    title={On the Use of ArXiv as a Dataset},
    author={Colin B. Clement and Matthew Bierbaum and Kevin P. O'Keeffe and Alexander A. Alemi},
    year={2019},
    eprint={1905.00075},
    archivePrefix={arXiv},
    primaryClass={cs.IR}
}
```

### Contributions

Thanks to [@tanmoyio](https://github.com/tanmoyio) for adding this dataset.