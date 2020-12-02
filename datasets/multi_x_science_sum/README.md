---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
---

# Dataset Card for Multi-XScience

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

- **Repository:** [Multi-XScience repository](https://github.com/yaolu/Multi-XScience)
- **Paper:** [Multi-XScience: A Large-scale Dataset for Extreme Multi-document Summarization of Scientific Articles](https://arxiv.org/abs/2010.14235)

### Dataset Summary

Multi-XScience, a large-scale multi-document summarization dataset created from scientific articles. Multi-XScience introduces a challenging multi-document summarization task: writing therelated-work section of a paper based on itsabstract and the articles it references.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English

## Dataset Structure

### Data Instances

{'abstract': 'Author(s): Kuperberg, Greg; Thurston, Dylan P. | Abstract: We give a purely topological definition of the perturbative quantum invariants of links and 3-manifolds associated with Chern-Simons field theory. Our definition is as close as possible to one given by Kontsevich. We will also establish some basic properties of these invariants, in particular that they are universally finite type with respect to algebraically split surgery and with respect to Torelli surgery. Torelli surgery is a mutual generalization of blink surgery of Garoufalidis and Levine and clasper surgery of Habiro.',
 'aid': 'math9912167',
 'mid': '1631980677',
 'ref_abstract': {'abstract': ['This note is a sequel to our earlier paper of the same title [4] and describes invariants of rational homology 3-spheres associated to acyclic orthogonal local systems. Our work is in the spirit of the Axelrod–Singer papers [1], generalizes some of their results, and furnishes a new setting for the purely topological implications of their work.',
   'Recently, Mullins calculated the Casson-Walker invariant of the 2-fold cyclic branched cover of an oriented link in S^3 in terms of its Jones polynomial and its signature, under the assumption that the 2-fold branched cover is a rational homology 3-sphere. Using elementary principles, we provide a similar calculation for the general case. In addition, we calculate the LMO invariant of the p-fold branched cover of twisted knots in S^3 in terms of the Kontsevich integral of the knot.'],
  'cite_N': ['@cite_16', '@cite_26'],
  'mid': ['1481005306', '1641082372']},
 'related_work': 'Two other generalizations that can be considered are invariants of graphs in 3-manifolds, and invariants associated to other flat connections @cite_16 . We will analyze these in future work. Among other things, there should be a general relation between flat bundles and links in 3-manifolds on the one hand and finite covers and branched covers on the other hand @cite_26 .'}

### Data Fields

{`abstract`: text of paper abstract \
 `aid`: arxiv id \
 `mid`: microsoft academic graph id \
 `ref_abstract`: \
   { \
    `abstract`: text of reference paper (cite_N) abstract \
    `cite_N`: special cite symbol, \
    `mid`: reference paper's (cite_N) microsoft academic graph id \
   }, \
 `related_work`: text of paper related work \
 }

### Data Splits

The data is split into a training, validation and test.

| Tain   | Valid | Test |
| ------ | ----- | ---- |
| 30369  |  5066 | 5093 |


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

[More Information Needed]
