---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-2.0
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-data-to-text-generation
---

# Dataset Card for Corpus for Knowledge-Enhanced Language Model Pre-training (KELM)

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

- **Homepage:** https://github.com/google-research-datasets/KELM-corpus
- **Repository:** https://github.com/google-research-datasets/KELM-corpus
- **Paper:** https://arxiv.org/abs/2010.12688
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Data-To-Text Generation involves converting knowledge graph (KG) triples of the form (subject, relation, object) into
a natural language sentence(s). This dataset consists of English KG data converted into paired natural language text.
The generated corpus consists of ∼18M sentences spanning ∼45M triples with ∼1500 distinct relations.

### Supported Tasks and Leaderboards

The intended task is data-to-text generation, taking in a knowledge graph tuple and generating a natural language
representation from it. Specifically, the data is in the format the authors used to train a seq2seq language model
with the tuples concatenated into a single sequence.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

Each instance consists of one KG triple paired with corresponding natural language.

### Data Fields

- `triple`: Wikipedia triples of the form `<subject> <relation> <object>` where some subjects have multiple
relations, e.g. `<subject> <relation1> <object1> <relation2> <object2> <relation3> <object3>`. For more details on
how these relations are grouped, please refer to the paper.
- `sentence`: The corresponding Wikipedia sentence.

### Data Splits

The dataset includes a pre-determined train, validation, and test split.

## Dataset Creation

### Curation Rationale

The goal of the dataset's curation and the associated modeling work discussed in the paper is to be able to generate
natural text from a knowledge graph.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The data is sourced from English Wikipedia and it's associated knowledge graph.

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

From the paper:

> Wikipedia has documented ideological, gender6, and racial biases in its text. While the KELM corpus may still
contain some of these biases, certain types of biases may be reduced.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

This dataset has been released under the [CC BY-SA 2.0 license](https://creativecommons.org/licenses/by-sa/2.0/).

### Citation Information

```
@misc{agarwal2020large,
      title={Large Scale Knowledge Graph Based Synthetic Corpus Generation for Knowledge-Enhanced Language Model Pre-training}, 
      author={Oshin Agarwal and Heming Ge and Siamak Shakeri and Rami Al-Rfou},
      year={2020},
      eprint={2010.12688},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
