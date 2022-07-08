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
language:
- en
license:
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
  - [Citation Information](#citation-information)
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
   
To study the remaining programmatic tasks, please see the [BIG-bench GitHub repo](https://github.com/google/BIG-bench)

### Languages

Although predominantly English, BIG-bench contains tasks in over 1000 written languages, as well as some synthetic and programming languages. 
See [BIG-bench organized by keywords](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md). Relevant keywords include `multilingual`, `non-english`, `low-resource-language`, `translation`.

For tasks specifically targeting low-resource languages, see the table below:

Task Name | Languages |
--|--|
Conlang Translation Problems | English, German, Finnish, Abma, Apinayé, Inapuri, Ndebele, Palauan|
Kannada Riddles | Kannada|
Language Identification | 1000 languages |
Swahili English Proverbs | Swahili |
Which Wiki Edit | English, Russian, Spanish, German, French, Turkish, Japanese, Vietnamese, Chinese, Arabic, Norwegian, Tagalog|




## Dataset Structure

### Data Instances

Each dataset contains 5 features. For example an instance from the `emoji_movie` task is:

```
{
  "idx": 0,
  "inputs": "Q: What movie does this emoji describe? 👦👓⚡️\n  choice: harry potter\n. choice: shutter island\n. choice: inglourious basterds\n. choice: die hard\n. choice: moonlight\nA:"
  "targets": ["harry potter"],
  "multiple_choice_targets":["harry potter", "shutter island", "die hard", "inglourious basterds", "moonlight"],
  "multiple_choice_scores": [1, 0, 0, 0, 0]
}
```
      
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

BIG-bench tasks were collaboratively submitted through GitHub pull requests. 

Each task went through a review and meta-review process with criteria outlined in the [BIG-bench repository documentation](https://github.com/google/BIG-bench/blob/main/docs/doc.md#submission-review-process).
Each task was required to describe the data source and curation methods on the task README page. 

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

BIG-bench contains a wide range of tasks, some of which are sensitive and should be used with care.

Some tasks are specifically designed to test biases and failures common to large language models, and so may elicit inappropriate or harmful responses.
For a more thorough discussion see the [BIG-bench paper](in progress). 

To view tasks designed to probe pro-social behavior, including alignment, social, racial, gender, religious or political bias; toxicity; inclusion; and other issues please see tasks under the [pro-social behavior keywords](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md#pro-social-behavior) on the BIG-bench repository.


### Social Impact of Dataset

[More Information Needed]


### Discussion of Biases

[More Information Needed]


### Other Known Limitations

[More Information Needed]


## Additional Information

For a more thorough discussion of all aspects of BIG-bench including dataset creation and evaluations see the BIG-bench repository [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench) and paper []

### Dataset Curators

[More Information Needed]


### Licensing Information

[Apache License 2.0](https://github.com/google/BIG-bench/blob/main/LICENSE)

### Citation Information

To be added soon !

### Contributions
For a full list of contributors to the BIG-bench dataset, see the paper.

Thanks to [@andersjohanandreassen](https://github.com/andersjohanandreassen) and [@ethansdyer](https://github.com/ethansdyer) for adding this dataset to HuggingFace.
