---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- de
- en
- it
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
- token-classification
- text-classification
task_ids:
- dialogue-modeling
- multi-class-classification
- parsing
paperswithcode_id: wizard-of-oz
pretty_name: Wizard-of-Oz
configs:
- de
- de_en
- en
- it
- it_en
dataset_info:
- config_name: en
  features:
  - name: dialogue_idx
    dtype: int32
  - name: dialogue
    list:
    - name: turn_label
      sequence:
        sequence: string
    - name: asr
      sequence:
        sequence: string
    - name: system_transcript
      dtype: string
    - name: turn_idx
      dtype: int32
    - name: belief_state
      list:
      - name: slots
        sequence:
          sequence: string
      - name: act
        dtype: string
    - name: transcript
      dtype: string
    - name: system_acts
      sequence:
        sequence: string
  splits:
  - name: test
    num_bytes: 537557
    num_examples: 400
  - name: train
    num_bytes: 827189
    num_examples: 600
  - name: validation
    num_bytes: 265684
    num_examples: 200
  download_size: 7529221
  dataset_size: 1630430
- config_name: de
  features:
  - name: dialogue_idx
    dtype: int32
  - name: dialogue
    list:
    - name: turn_label
      sequence:
        sequence: string
    - name: asr
      sequence:
        sequence: string
    - name: system_transcript
      dtype: string
    - name: turn_idx
      dtype: int32
    - name: belief_state
      list:
      - name: slots
        sequence:
          sequence: string
      - name: act
        dtype: string
    - name: transcript
      dtype: string
    - name: system_acts
      sequence:
        sequence: string
  splits:
  - name: test
    num_bytes: 569703
    num_examples: 400
  - name: train
    num_bytes: 881478
    num_examples: 600
  - name: validation
    num_bytes: 276758
    num_examples: 200
  download_size: 7626734
  dataset_size: 1727939
- config_name: de_en
  features:
  - name: dialogue_idx
    dtype: int32
  - name: dialogue
    list:
    - name: turn_label
      sequence:
        sequence: string
    - name: asr
      sequence:
        sequence: string
    - name: system_transcript
      dtype: string
    - name: turn_idx
      dtype: int32
    - name: belief_state
      list:
      - name: slots
        sequence:
          sequence: string
      - name: act
        dtype: string
    - name: transcript
      dtype: string
    - name: system_acts
      sequence:
        sequence: string
  splits:
  - name: test
    num_bytes: 555841
    num_examples: 400
  - name: train
    num_bytes: 860151
    num_examples: 600
  - name: validation
    num_bytes: 269966
    num_examples: 200
  download_size: 7584753
  dataset_size: 1685958
- config_name: it
  features:
  - name: dialogue_idx
    dtype: int32
  - name: dialogue
    list:
    - name: turn_label
      sequence:
        sequence: string
    - name: asr
      sequence:
        sequence: string
    - name: system_transcript
      dtype: string
    - name: turn_idx
      dtype: int32
    - name: belief_state
      list:
      - name: slots
        sequence:
          sequence: string
      - name: act
        dtype: string
    - name: transcript
      dtype: string
    - name: system_acts
      sequence:
        sequence: string
  splits:
  - name: test
    num_bytes: 547759
    num_examples: 400
  - name: train
    num_bytes: 842799
    num_examples: 600
  - name: validation
    num_bytes: 270258
    num_examples: 200
  download_size: 7559615
  dataset_size: 1660816
- config_name: it_en
  features:
  - name: dialogue_idx
    dtype: int32
  - name: dialogue
    list:
    - name: turn_label
      sequence:
        sequence: string
    - name: asr
      sequence:
        sequence: string
    - name: system_transcript
      dtype: string
    - name: turn_idx
      dtype: int32
    - name: belief_state
      list:
      - name: slots
        sequence:
          sequence: string
      - name: act
        dtype: string
    - name: transcript
      dtype: string
    - name: system_acts
      sequence:
        sequence: string
  splits:
  - name: test
    num_bytes: 548979
    num_examples: 400
  - name: train
    num_bytes: 845095
    num_examples: 600
  - name: validation
    num_bytes: 270942
    num_examples: 200
  download_size: 7563815
  dataset_size: 1665016
---

# Dataset Card for Wizard-of-Oz

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

- **Homepage:** [More info needed]
- **Repository:** [GitHub](https://github.com/nmrksic/neural-belief-tracker/tree/master/data/woz)
- **Paper:** [A Network-based End-to-End Trainable Task-oriented Dialogue System](https://arxiv.org/abs/1604.04562)
- **Leaderboard:** [More info needed]
- **Point of Contact:** [More info needed]

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

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.