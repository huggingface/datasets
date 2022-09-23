---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: null
pretty_name: Cryptonite
configs:
- cryptonite
- default
dataset_info:
- config_name: default
  features:
  - name: agent_info
    sequence:
    - name: Bottomline
      dtype: string
    - name: Role
      dtype: string
    - name: Target
      dtype: float32
  - name: agent_turn
    sequence: int32
  - name: dialogue_acts
    sequence:
    - name: intent
      dtype: string
    - name: price
      dtype: float32
  - name: utterance
    sequence: string
  - name: items
    sequence:
    - name: Category
      dtype: string
    - name: Images
      dtype: string
    - name: Price
      dtype: float32
    - name: Description
      dtype: string
    - name: Title
      dtype: string
  splits:
  - name: test
    num_bytes: 1353933
    num_examples: 838
  - name: train
    num_bytes: 8538836
    num_examples: 5247
  - name: validation
    num_bytes: 966032
    num_examples: 597
  download_size: 25373618
  dataset_size: 10858801
- config_name: cryptonite
  features:
  - name: clue
    dtype: string
  - name: answer
    dtype: string
  - name: enumeration
    dtype: string
  - name: publisher
    dtype: string
  - name: date
    dtype: int64
  - name: quick
    dtype: bool
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2908275
    num_examples: 26157
  - name: train
    num_bytes: 52228597
    num_examples: 470804
  - name: validation
    num_bytes: 2901768
    num_examples: 26156
  download_size: 21615952
  dataset_size: 58038640
---

# Dataset Card for Cryptonite

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

- **Homepage:** [Github](https://github.com/aviaefrat/cryptonite)
- **Repository:** [Github](https://github.com/aviaefrat/cryptonite)
- **Paper:** [Arxiv](https://arxiv.org/pdf/2103.01242.pdf)
- **Leaderboard:**
- **Point of Contact:** [Twitter](https://twitter.com/AviaEfrat)

### Dataset Summary

Current NLP datasets targeting ambiguity can be solved by a native speaker with relative ease. We present Cryptonite, a large-scale dataset based on cryptic crosswords, which is both linguistically complex and naturally sourced. Each example in Cryptonite is a cryptic clue, a short phrase or sentence with a misleading surface reading, whose solving requires disambiguating semantic, syntactic, and phonetic wordplays, as well as world knowledge. Cryptic clues pose a challenge even for experienced solvers, though top-tier experts can solve them with almost 100% accuracy. Cryptonite is a challenging task for current models; fine-tuning T5-Large on 470k cryptic clues achieves only 7.6% accuracy, on par with the accuracy of a rule-based clue solver (8.6%).

### Languages

English

## Dataset Structure

### Data Instances

This is one example from the train set.

```python
{
  'clue': 'make progress socially in stated region (5)',
  'answer': 'climb',
  'date': 971654400000,
  'enumeration': '(5)',
  'id': 'Times-31523-6across',
  'publisher': 'Times',
  'quick': False
}
```

### Data Fields

- `clue`: a string representing the clue provided for the crossword
- `answer`: a string representing the answer to the clue
- `enumeration`: a string representing the 
- `publisher`: a string representing the publisher of the crossword
- `date`: a int64 representing the UNIX timestamp of the date of publication of the crossword
- `quick`: a bool representing whether the crossword is quick (a crossword aimed at beginners, easier to solve)
- `id`: a string to uniquely identify a given example in the dataset

### Data Splits

Train (470,804 examples), validation (26,156 examples), test (26,157 examples).

## Dataset Creation

### Curation Rationale

Crosswords from the Times and the Telegraph.

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

Avia Efrat, Uri Shaham, Dan Kilman, Omer Levy

### Licensing Information

`cc-by-nc-4.0`

### Citation Information

```
@misc{efrat2021cryptonite,
      title={Cryptonite: A Cryptic Crossword Benchmark for Extreme Ambiguity in Language}, 
      author={Avia Efrat and Uri Shaham and Dan Kilman and Omer Levy},
      year={2021},
      eprint={2103.01242},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@theo-m](https://github.com/theo-m) for adding this dataset.