---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- table-to-text
task_ids: []
paperswithcode_id: null
pretty_name: GREAT
dataset_info:
  features:
  - name: id
    dtype: int32
  - name: source_tokens
    sequence: string
  - name: has_bug
    dtype: bool
  - name: error_location
    dtype: int32
  - name: repair_candidates
    sequence: string
  - name: bug_kind
    dtype: int32
  - name: bug_kind_name
    dtype: string
  - name: repair_targets
    sequence: int32
  - name: edges
    list:
      list:
      - name: before_index
        dtype: int32
      - name: after_index
        dtype: int32
      - name: edge_type
        dtype: int32
      - name: edge_type_name
        dtype: string
  - name: provenances
    list:
    - name: datasetProvenance
      struct:
      - name: datasetName
        dtype: string
      - name: filepath
        dtype: string
      - name: license
        dtype: string
      - name: note
        dtype: string
  splits:
  - name: test
    num_bytes: 7880762248
    num_examples: 968592
  - name: train
    num_bytes: 14705534822
    num_examples: 1798742
  - name: validation
    num_bytes: 1502956919
    num_examples: 185656
  download_size: 23310374002
  dataset_size: 24089253989
---

# Dataset Card for GREAT

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

- **Homepage:** None
- **Repository:** https://github.com/google-research-datasets/great
- **Paper:** https://openreview.net/forum?id=B1lnbRNtwr
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Here are some examples of questions and facts:


### Data Fields

[More Information Needed]

### Data Splits

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

[More Information Needed]

### Citation Information

[More Information Needed]
### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.