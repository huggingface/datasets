---
pretty_name: MOCHA
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-generative-reading-comprehension-metric
paperswithcode_id: mocha
---

# Dataset Card for Mocha

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

- **Homepage:[Mocha](https://allennlp.org/mocha)**
- **Repository:[https://github.com/anthonywchen/MOCHA](https://github.com/anthonywchen/MOCHA)**
- **Paper:[MOCHA: A Dataset for Training and Evaluating Generative Reading Comprehension Metrics](https://www.aclweb.org/anthology/2020.emnlp-main.528/)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Posing reading comprehension as a generation problem provides a great deal of flexibility, allowing for open-ended questions with few restrictions on possible answers. However, progress is impeded by existing generation metrics, which rely on token overlap and are agnostic to the nuances of reading comprehension. To address this, we introduce a benchmark for training and evaluating generative reading comprehension metrics: MOdeling Correctness with Human Annotations. MOCHA contains 40K human judgement scores on model outputs from 6 diverse question answering datasets and an additional set of minimal pairs for evaluation. Using MOCHA, we train a Learned Evaluation metric for Reading Comprehension, LERC, to mimic human judgement scores. LERC outperforms baseline metrics by 10 to 36 absolute Pearson points on held-out annotations. When we evaluate robustness on minimal pairs, LERC achieves 80% accuracy, outperforming baselines by 14 to 26 absolute percentage points while leaving significant room for improvement. MOCHA presents a challenging problem for developing accurate and robust generative reading comprehension metrics.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

MOCHA contains 40K human judgement scores on model outputs from 6 diverse question answering datasets and an additional set of minimal pairs for evaluation. MOCHA pairs reading comprehension instances, which consists of a passage, question, and reference, with candidates and human judgement scores.

### Data Fields

- `constituent_dataset`: the original QA dataset which the data instance came from.
- `id`
- `context`: the passage content.
- `question`: the question related to the passage content.
- `reference`: the correct answer for the question.
- `candidate`: the answer generated from the `reference` by `source`
- `score`: the human judgement score for the `candidate`. Not included in test split, defaults to `-1`
- `metadata`: Not included in minimal pairs split.
  - `scores`: list of scores from difference judges, averaged out to get final `score`. defaults to `[]`
  - `source`: the generative model to generate the `candidate`

In minimal pairs, we'll have an additional candidate for robust evaluation.

- `candidate2`
- `score2`

### Data Splits

Dataset Split | Number of Instances in Split
--------------|--------------------------------------------
Train | 31,069
Validation | 4,009
Test | 6,321
Minimal Pairs | 200

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

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

### Citation Information

```bitex
@inproceedings{Chen2020MOCHAAD,
    author={Anthony Chen and Gabriel Stanovsky and Sameer Singh and Matt Gardner},
    title={MOCHA: A Dataset for Training and Evaluating Generative Reading Comprehension Metrics},
    booktitle={EMNLP},
    year={2020}
}
```

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.