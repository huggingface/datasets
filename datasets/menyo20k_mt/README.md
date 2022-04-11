---
annotations_creators:
- expert-generated
- found
language_creators:
- found
languages:
- en
- yo
licenses:
- cc-by-4.0
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
pretty_name: MENYO-20k
---

# Dataset Card for MENYO-20k

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

- **Homepage:** [Homepage for Menyo-20k](https://zenodo.org/record/4297448#.X81G7s0zZPY)
- **Repository:**[Github Repo](https://github.com/dadelani/menyo-20k_MT)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

MENYO-20k is a multi-domain parallel dataset with texts obtained from news articles, ted talks, movie transcripts, radio transcripts, science and technology texts, and other short articles curated from the web and professional translators. The dataset has 20,100 parallel sentences split into 10,070 training sentences, 3,397 development sentences, and 6,633 test sentences (3,419 multi-domain, 1,714 news domain, and 1,500 ted talks speech transcript domain)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Languages are English and YOruba

## Dataset Structure

### Data Instances

The data consists of tab seperated entries

```
{'translation': 
  {'en': 'Unit 1: What is Creative Commons?',
  'yo': '﻿Ìdá 1: Kín ni Creative Commons?'
  }
}

```

### Data Fields

- `en`: English sentence
- `yo`: Yoruba sentence


### Data Splits

Only training dataset available

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

The dataset is open but for non-commercial use because some of the data sources like Ted talks and JW news requires permission for commercial use.

### Citation Information
```
@dataset{david_ifeoluwa_adelani_2020_4297448,
  author       = {David Ifeoluwa Adelani and
                  Jesujoba O. Alabi and
                  Damilola Adebonojo and
                  Adesina Ayeni and
                  Mofe Adeyemi and
                  Ayodele Awokoya},
  title        = {{MENYO-20k: A Multi-domain English - Yorùbá Corpus 
                   for Machine Translation}},
  month        = nov,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.4297448},
  url          = {https://doi.org/10.5281/zenodo.4297448}
}
```
### Contributions

Thanks to [@yvonnegitau](https://github.com/yvonnegitau) for adding this dataset.