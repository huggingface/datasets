---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-ImageFlickr and SemEval-2012 STS MSR-Video Descriptions
task_categories:
- text-classification
task_ids:
- text-scoring
- natural-language-inference
- semantic-similarity-scoring
paperswithcode_id: null
pretty_name: SemEval 2014 - Task 1
dataset_info:
  features:
  - name: sentence_pair_id
    dtype: int64
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: relatedness_score
    dtype: float32
  - name: entailment_judgment
    dtype:
      class_label:
        names:
          0: NEUTRAL
          1: ENTAILMENT
          2: CONTRADICTION
  splits:
  - name: test
    num_bytes: 592320
    num_examples: 4927
  - name: train
    num_bytes: 540296
    num_examples: 4500
  - name: validation
    num_bytes: 60981
    num_examples: 500
  download_size: 197230
  dataset_size: 1193597
---

# Dataset Card for SemEval 2014 - Task 1

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

- **Homepage:** [SemEval-2014 Task 1](https://alt.qcri.org/semeval2014/task1/)
- **Repository:**
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/S14-2001/)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

### Contributions

Thanks to [@ashmeet13](https://github.com/ashmeet13) for adding this dataset.