---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: gutenberg-poem-dataset
---

# Dataset Card Creation Guide

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

- **Homepage:** N/A
- **Repository:** [GitHub](https://github.com/google-research-datasets/poem-sentiment)
- **Paper:** [Investigating Societal Biases in a Poetry Composition System](https://arxiv.org/abs/2011.02686)
- **Leaderboard:** N/A
- **Point of Contact:** -

### Dataset Summary

Poem Sentiment is a sentiment dataset of poem verses from Project Gutenberg.
This dataset can be used for tasks such as sentiment classification or style transfer for poems.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English (`en`).

## Dataset Structure

### Data Instances
Example of one instance in the dataset.

```{'id': 0, 'label': 2, 'verse_text': 'with pale blue berries. in these peaceful shades--'}```

### Data Fields

- `id`: index of the example
- `verse_text`: The text of the poem verse
- `label`: The sentiment label. Here 
    - 0 = negative
    - 1 = positive
    - 2 = no impact
    - 3 = mixed (both negative and positive)
> Note: The original dataset uses different label indices  (negative = -1, no impact = 0, positive = 1) 

### Data Splits

The dataset is split into a `train`, `validation`, and `test` split with the following sizes:

|                            | Tain   | Valid | Test  |
| -----                      | ------ | ----- | ----- |
| Number of examples         | 892    | 105   | 104   |



[More Information Needed]
## Dataset Creation

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

This work is licensed under a Creative Commons Attribution 4.0 International License

### Citation Information

```
@misc{sheng2020investigating,
      title={Investigating Societal Biases in a Poetry Composition System},
      author={Emily Sheng and David Uthus},
      year={2020},
      eprint={2011.02686},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.