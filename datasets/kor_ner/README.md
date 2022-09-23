---
annotations_creators:
- expert-generated
language_creators:
- other
language:
- ko
license:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: KorNER
dataset_info:
  features:
  - name: text
    dtype: string
  - name: annot_text
    dtype: string
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: SO
          1: SS
          2: VV
          3: XR
          4: VCP
          5: JC
          6: VCN
          7: JKB
          8: MM
          9: SP
          10: XSN
          11: SL
          12: NNP
          13: NP
          14: EP
          15: JKQ
          16: IC
          17: XSA
          18: EC
          19: EF
          20: SE
          21: XPN
          22: ETN
          23: SH
          24: XSV
          25: MAG
          26: SW
          27: ETM
          28: JKO
          29: NNB
          30: MAJ
          31: NNG
          32: JKV
          33: JKC
          34: VA
          35: NR
          36: JKG
          37: VX
          38: SF
          39: JX
          40: JKS
          41: SN
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: I
          1: O
          2: B_OG
          3: B_TI
          4: B_LC
          5: B_DT
          6: B_PS
  splits:
  - name: test
    num_bytes: 476850
    num_examples: 366
  - name: train
    num_bytes: 3948938
    num_examples: 2928
  - name: validation
    num_bytes: 486178
    num_examples: 366
  download_size: 3493175
  dataset_size: 4911966
---

# Dataset Card for KorNER

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

- **Homepage:** [Github](https://github.com/kmounlp/NER)
- **Repository:** [Github](https://github.com/kmounlp/NER)
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

Each row consists of the following fields:

- `text`: The full text, as is
- `annot_text`: Annotated text including POS-tagged information
- `tokens`: An ordered list of tokens from the full text
- `pos_tags`: Part-of-speech tags for each token
- `ner_tags`: Named entity recognition tags for each token

Note that by design, the length of `tokens`, `pos_tags`, and `ner_tags` will always be identical.

`pos_tags` corresponds to the list below:

```
['SO', 'SS', 'VV', 'XR', 'VCP', 'JC', 'VCN', 'JKB', 'MM', 'SP', 'XSN', 'SL', 'NNP', 'NP', 'EP', 'JKQ', 'IC', 'XSA', 'EC', 'EF', 'SE', 'XPN', 'ETN', 'SH', 'XSV', 'MAG', 'SW', 'ETM', 'JKO', 'NNB', 'MAJ', 'NNG', 'JKV', 'JKC', 'VA', 'NR', 'JKG', 'VX', 'SF', 'JX', 'JKS', 'SN']
```

`ner_tags` correspond to the following:

```
["I", "O", "B_OG", "B_TI", "B_LC", "B_DT", "B_PS"]
```

The prefix `B` denotes the first item of a phrase, and an `I` denotes any non-initial word. In addition, `OG` represens an organization; `TI`, time; `DT`, date, and `PS`, person.

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

Thanks to [@jaketae](https://github.com/jaketae) for adding this dataset.