---
annotations_creators:
- crowdsourced
- expert-generated
- machine-generated
language_creators:
- crowdsourced
- expert-generated
- machine-generated
- other
languages:
- en-US
licenses:
- apache-2.0
multilinguality:
- multilingual
- monolingual
pretty_name: bigbench
size_categories:
- unknown
source_datasets:
- original
task_categories:
- multiple-choice
- question-answering
- text-classification
- text-generation
- zero-shot-classification
- other
task_ids:
- multiple-choice-qa
- extractive-qa
- open-domain-qa
- closed-domain-qa
- fact-checking
- acceptability-classification
- intent-classification
- multi-class-classification
- multi-label-classification
- text-scoring
- hate-speech-detection
- language-modeling
---

# Dataset Card for BIG-bench

## Table of Contents
- [Table of Contents](#table-of-contents)
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
  - [Citation Inform ation](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage/Repository:** [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench)
- **Paper:** In progress
- **Leaderboard:**
- **Point of Contact:** [bigbench@googlegroups.com](mailto:bigbench@googlegroups.com)

### Dataset Summary

The Beyond the Imitation Game Benchmark (BIG-bench) is a collaborative benchmark intended to probe large language models and extrapolate their future capabilities. Tasks included in BIG-bench are summarized by keyword [here](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md), and by task name [here](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/README.md). A paper introducing the benchmark, including evaluation results on large language models, is currently in preparation.

### Supported Tasks and Leaderboards

BIG-Bench consists of both json and programmatic tasks.
This implementation in HuggingFace datasets implements
	- 24 BIG-bench Lite tasks
    - 167 BIG-bench json tasks (includes BIG-bench Lite)
    
To study the remaining programmatic tasks, please see the BIG-bench GitHub [repo](https://github.com/google/BIG-bench)

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Each dataset contains 5 features. For example an instance from the `emoji_movie` task is:

- `idx`:

      0
- `inputs`:

      Q: What movie does this emoji describe? 👦👓⚡️
       choice: harry potter
       choice: shutter island
       choice: inglourious basterds
       choice: die hard
       choice: moonlight
      A:
      
- `targets`:

      ['harry potter']
- `multiple_choice_targets`:

      ['harry potter', 'shutter island', 'die hard', 'inglourious basterds', 'moonlight']
      
- `multiple_choice_scores`:
     
      [1, 0, 0, 0, 0]
      
For tasks that do not have multiple choice targets, the lists are empty.


### Data Fields

Every example has the following fields
  - `idx`: an `int` feature
  - `inputs`: a `string` feature
  - `targets`: a sequence of `string` feature
  - `multiple_choice_targets`: a sequence of `string` features
  - `multiple_choice_scores`: a sequence of `int` features

### Data Splits

Each task has a `default`, `train` and `validation` split.
The split `default` uses all the samples for each task (and it's the same as `all` used in the `bigbench.bbseqio` implementation.)
For standard evaluation on BIG-bench, we recommend using the `default` split, and the `train` and `validation` split is to be used if one wants to train a model on BIG-bench.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Tasks were contributed by the research community through [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench), and [reviewed](https://github.com/google/BIG-bench/blob/main/docs/doc.md#submission-review-process) by members of the collaboration.

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

[Apache License 2.0](https://github.com/google/BIG-bench/blob/main/LICENSE)

### Citation Information

A paper is in progress. Until then, please cite the BIG-bench collaboration and the GitHub [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench).

### Contributions

Thanks to [@andersjohanandreassen](https://github.com/andersjohanandreassen) for adding this dataset.
