---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- 'no'
license:
- unknown
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
paperswithcode_id: null
pretty_name: Norwegian NER
dataset_info:
- config_name: bokmaal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: ADV
          14: INTJ
          15: VERB
          16: AUX
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-OTH
          2: I-OTH
          3: E-OTH
          4: S-OTH
          5: B-ORG
          6: I-ORG
          7: E-ORG
          8: S-ORG
          9: B-PRS
          10: I-PRS
          11: E-PRS
          12: S-PRS
          13: B-GEO
          14: I-GEO
          15: E-GEO
          16: S-GEO
  splits:
  - name: test
    num_bytes: 1212939
    num_examples: 1939
  - name: train
    num_bytes: 9859760
    num_examples: 15696
  - name: validation
    num_bytes: 1475216
    num_examples: 2410
  download_size: 8747760
  dataset_size: 12547915
- config_name: nynorsk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: ADV
          14: INTJ
          15: VERB
          16: AUX
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-OTH
          2: I-OTH
          3: E-OTH
          4: S-OTH
          5: B-ORG
          6: I-ORG
          7: E-ORG
          8: S-ORG
          9: B-PRS
          10: I-PRS
          11: E-PRS
          12: S-PRS
          13: B-GEO
          14: I-GEO
          15: E-GEO
          16: S-GEO
  splits:
  - name: test
    num_bytes: 1006733
    num_examples: 1511
  - name: train
    num_bytes: 9916338
    num_examples: 14174
  - name: validation
    num_bytes: 1257235
    num_examples: 1890
  download_size: 8484545
  dataset_size: 12180306
- config_name: samnorsk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: ADV
          14: INTJ
          15: VERB
          16: AUX
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-OTH
          2: I-OTH
          3: E-OTH
          4: S-OTH
          5: B-ORG
          6: I-ORG
          7: E-ORG
          8: S-ORG
          9: B-PRS
          10: I-PRS
          11: E-PRS
          12: S-PRS
          13: B-GEO
          14: I-GEO
          15: E-GEO
          16: S-GEO
  splits:
  - name: test
    num_bytes: 2219640
    num_examples: 3450
  - name: train
    num_bytes: 22508485
    num_examples: 34170
  - name: validation
    num_bytes: 2732419
    num_examples: 4300
  download_size: 19133049
  dataset_size: 27460544
---

# Dataset Card for Norwegian NER

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

- **Homepage:** [Github](https://github.com/ljos/navnkjenner)
- **Repository:** [Github](https://github.com/ljos/navnkjenner)
- **Paper:**
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

Thanks to [@jplu](https://github.com/jplu) for adding this dataset.