---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1M<n<10M
source_datasets:
- original
task_categories:
- summarization
task_ids:
- summarization-other-patent-summarization
paperswithcode_id: bigpatent
pretty_name: Big Patent
configs:
- a
- all
- b
- c
- d
- e
- f
- g
- h
- y
dataset_info:
- config_name: all
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 1296234391
    num_examples: 67072
  - name: train
    num_bytes: 23363518650
    num_examples: 1207222
  - name: validation
    num_bytes: 1290154487
    num_examples: 67068
  download_size: 6447221554
  dataset_size: 25949907528
- config_name: a
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 185987552
    num_examples: 9675
  - name: train
    num_bytes: 3329778447
    num_examples: 174134
  - name: validation
    num_bytes: 184116486
    num_examples: 9674
  download_size: 6447221554
  dataset_size: 3699882485
- config_name: b
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 140741033
    num_examples: 8974
  - name: train
    num_bytes: 2574594655
    num_examples: 161520
  - name: validation
    num_bytes: 143029380
    num_examples: 8973
  download_size: 6447221554
  dataset_size: 2858365068
- config_name: c
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 149052258
    num_examples: 5614
  - name: train
    num_bytes: 2641973267
    num_examples: 101042
  - name: validation
    num_bytes: 145441704
    num_examples: 5613
  download_size: 6447221554
  dataset_size: 2936467229
- config_name: d
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 8713720
    num_examples: 565
  - name: train
    num_bytes: 160467163
    num_examples: 10164
  - name: validation
    num_bytes: 8667961
    num_examples: 565
  download_size: 6447221554
  dataset_size: 177848844
- config_name: e
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 29843613
    num_examples: 1914
  - name: train
    num_bytes: 535567259
    num_examples: 34443
  - name: validation
    num_bytes: 28549964
    num_examples: 1914
  download_size: 6447221554
  dataset_size: 593960836
- config_name: f
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 71676041
    num_examples: 4754
  - name: train
    num_bytes: 1297707404
    num_examples: 85568
  - name: validation
    num_bytes: 72367466
    num_examples: 4754
  download_size: 6447221554
  dataset_size: 1441750911
- config_name: g
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 310624265
    num_examples: 14386
  - name: train
    num_bytes: 5571186559
    num_examples: 258935
  - name: validation
    num_bytes: 309182447
    num_examples: 14385
  download_size: 6447221554
  dataset_size: 6190993271
- config_name: h
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 274505113
    num_examples: 14279
  - name: train
    num_bytes: 4988365946
    num_examples: 257019
  - name: validation
    num_bytes: 275293153
    num_examples: 14279
  download_size: 6447221554
  dataset_size: 5538164212
- config_name: y
  features:
  - name: description
    dtype: string
  - name: abstract
    dtype: string
  splits:
  - name: test
    num_bytes: 125090828
    num_examples: 6911
  - name: train
    num_bytes: 2263877990
    num_examples: 124397
  - name: validation
    num_bytes: 123505958
    num_examples: 6911
  download_size: 6447221554
  dataset_size: 2512474776
---

# Dataset Card for Big Patent

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

- **Homepage:** [Big Patent](https://evasharma.github.io/bigpatent/)
- **Repository:**
- **Paper:** [BIGPATENT: A Large-Scale Dataset for Abstractive and Coherent Summarization](https://arxiv.org/abs/1906.03741)
- **Leaderboard:**
- **Point of Contact:** [Lu Wang](mailto:wangluxy@umich.edu)

### Dataset Summary

BIGPATENT, consisting of 1.3 million records of U.S. patent documents along with human written abstractive summaries. Each US patent application is filed under a Cooperative Patent Classification (CPC) code. There are nine such classification categories:

- A (Human Necessities)
- B (Performing Operations; Transporting)
- C (Chemistry; Metallurgy)
- D (Textiles; Paper)
- E (Fixed Constructions)
- F (Mechanical Engineering; Lightning; Heating; Weapons; Blasting)
- G (Physics)
- H (Electricity)
- Y (General tagging of new or cross-sectional technology)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

Each instance contains a pair of `description` and `abstract`. `description` is extracted from the Description section of the Patent while `abstract` is extracted from the Abstract section.

### Data Fields

- `description`: detailed description of patent.
- `abstract`: Patent abastract.

### Data Splits

|     |             train |   validation |   test |
|:----|------------------:|-------------:|-------:|
| all | 1207222           |        67068 |  67072 |
| a   |  174134           |         9674 |   9675 |
| b   |  161520           |         8973 |   8974 |
| c   |  101042           |         5613 |   5614 |
| d   |   10164           |          565 |    565 |
| e   |   34443           |         1914 |   1914 |
| f   |   85568           |         4754 |   4754 |
| g   |  258935           |        14385 |  14386 |
| h   |  257019           |        14279 |  14279 |
| y   |  124397           |         6911 |   6911 |

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

```bibtex
@article{DBLP:journals/corr/abs-1906-03741,
  author    = {Eva Sharma and
               Chen Li and
               Lu Wang},
  title     = {{BIGPATENT:} {A} Large-Scale Dataset for Abstractive and Coherent
               Summarization},
  journal   = {CoRR},
  volume    = {abs/1906.03741},
  year      = {2019},
  url       = {http://arxiv.org/abs/1906.03741},
  eprinttype = {arXiv},
  eprint    = {1906.03741},
  timestamp = {Wed, 26 Jun 2019 07:14:58 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1906-03741.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.