---
annotations_creators:
- expert-generated
language_creators:
- other
language:
- fi
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: finer
pretty_name: Finnish News Corpus for Named Entity Recognition
dataset_info:
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-DATE
          2: B-EVENT
          3: B-LOC
          4: B-ORG
          5: B-PER
          6: B-PRO
          7: I-DATE
          8: I-EVENT
          9: I-LOC
          10: I-ORG
          11: I-PER
          12: I-PRO
  - name: nested_ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-DATE
          2: B-EVENT
          3: B-LOC
          4: B-ORG
          5: B-PER
          6: B-PRO
          7: I-DATE
          8: I-EVENT
          9: I-LOC
          10: I-ORG
          11: I-PER
          12: I-PRO
  config_name: finer
  splits:
  - name: test
    num_bytes: 1327354
    num_examples: 3512
  - name: test_wikipedia
    num_bytes: 1404397
    num_examples: 3360
  - name: train
    num_bytes: 5159550
    num_examples: 13497
  - name: validation
    num_bytes: 387494
    num_examples: 986
  download_size: 3733127
  dataset_size: 8278795
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [Github](https://github.com/mpsilfve/finer-data)
- **Repository:** [Github](https://github.com/mpsilfve/finer-data)
- **Paper:** [Arxiv](https://arxiv.org/abs/1908.04212)
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

Each row consists of the following fields:

* `id`: The sentence id
* `tokens`: An ordered list of tokens from the full text
* `ner_tags`: Named entity recognition tags for each token
* `nested_ner_tags`: Nested named entity recognition tags for each token

Note that by design, the length of `tokens`, `ner_tags`, and `nested_ner_tags` will always be identical.

`ner_tags` and `nested_ner_tags` correspond to the list below:

```
[ "O", "B-DATE", "B-EVENT", "B-LOC", "B-ORG", "B-PER", "B-PRO", "I-DATE", "I-EVENT", "I-LOC", "I-ORG", "I-PER", "I-PRO" ]
```

IOB2 labeling scheme is used.

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

Thanks to [@stefan-it](https://github.com/stefan-it) for adding this dataset.