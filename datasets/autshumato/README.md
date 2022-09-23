---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
- tn
- ts
- zu
license:
- cc-by-2.5
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: autshumato
configs:
- autshumato-en-tn
- autshumato-en-ts
- autshumato-en-ts-manual
- autshumato-en-zu
- autshumato-tn
- autshumato-ts
dataset_info:
- config_name: autshumato-en-tn
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tn
  splits:
  - name: train
    num_bytes: 28826392
    num_examples: 159000
  download_size: 9458762
  dataset_size: 28826392
- config_name: autshumato-en-zu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zu
  splits:
  - name: train
    num_bytes: 7188970
    num_examples: 35489
  download_size: 2068891
  dataset_size: 7188970
- config_name: autshumato-en-ts
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ts
  splits:
  - name: train
    num_bytes: 50803849
    num_examples: 450000
  download_size: 15145915
  dataset_size: 50803849
- config_name: autshumato-en-ts-manual
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ts
  splits:
  - name: train
    num_bytes: 10408757
    num_examples: 92396
  download_size: 2876924
  dataset_size: 10408757
- config_name: autshumato-tn
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 5132267
    num_examples: 38206
  download_size: 1599029
  dataset_size: 5132267
- config_name: autshumato-ts
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 3399674
    num_examples: 58398
  download_size: 974488
  dataset_size: 3399674
---

# Dataset Card for autshumato

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

- **Homepage:** [https://repo.sadilar.org/handle/20.500.12185/7/discover]()
- **Repository:** []()
- **Paper:** []()
- **Leaderboard:** []()
- **Point of Contact:** []()

### Dataset Summary

Multilingual information access is stipulated in the South African constitution. In practise, this
is hampered by a lack of resources and capacity to perform the large volumes of translation
work required to realise multilingual information access. One of the aims of the Autshumato
project is to develop machine translation systems for three South African languages pairs.

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

[More Information Needed]

### Dataset Curators

[More Information Needed]

### Licensing Information


### Citation Information

```
@article{groenewald2010processing,
  title={Processing parallel text corpora for three South African language pairs in the Autshumato project},
  author={Groenewald, Hendrik J and du Plooy, Liza},
  journal={AfLaT 2010},
  pages={27},
  year={2010}
}
```

### Contributions

Thanks to [@Narsil](https://github.com/Narsil) for adding this dataset.