---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- machine-generated
languages:
- sv
licenses:
- unknown
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
---

# Dataset Card for Swedish Machine Translated STS-B 

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

- **Homepage:** [stsb-mt-sv homepage](https://github.com/timpal0l/sts-benchmark-swedish)
- **Repository:** [stsb-mt-sv repository](https://github.com/timpal0l/sts-benchmark-swedish)
- **Paper:** [Why Not Simply Translate? A First Swedish Evaluation Benchmark for Semantic Similarity
](https://arxiv.org/abs/2009.03116)
- **Point of Contact:** [Tim Isbister](mailto:timisbisters@gmail.com)

### Dataset Summary

This dataset is a Swedish machine translated version for semantic textual similarity. 

### Supported Tasks and Leaderboards

This dataset can be used to evaluate text similarity on Swedish.

### Languages

The text in the dataset is in Swedish. The associated BCP-47 code is `sv`.

## Dataset Structure

### Data Instances

What a sample looks like:
```
{'score': '4.2',
 'sentence1': 'Undrar om jultomten kommer i år pga Corona..?',
 'sentence2': 'Jag undrar om jultomen kommer hit i år med tanke på covid-19',
}
```

### Data Fields

- `score`: a float representing the semantic similarity score. Where 0.0 is the lowest score and 5.0 is the highest.
- `sentence1`: a string representing a text
- `sentence2`: another string to compare the semantic with

### Data Splits

The data is split into a training, validation and test set. The final split sizes are as follow:

| Train  | Valid | Test |
| ------ | ----- | ---- |
| 5749   |  1500 | 1379 |

## Dataset Creation

### Curation Rationale

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

### Annotations

#### Annotation process

#### Who are the annotators?

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

The machine translated version were put together by @timpal0l

### Licensing Information

### Citation Information

```
@article{isbister2020not,
  title={Why Not Simply Translate? A First Swedish Evaluation Benchmark for Semantic Similarity},
  author={Isbister, Tim and Sahlgren, Magnus},
  journal={arXiv preprint arXiv:2009.03116},
  year={2020}
}
```
