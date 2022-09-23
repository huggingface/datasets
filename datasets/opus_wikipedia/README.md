---
annotations_creators:
- found
language_creators:
- found
language:
- ar
- bg
- cs
- de
- el
- en
- es
- fa
- fr
- he
- hu
- it
- nl
- pl
- pt
- ro
- ru
- sl
- tr
- vi
license:
- unknown
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
pretty_name: OpusWikipedia
configs:
- ar-en
- ar-pl
- en-ru
- en-sl
- en-vi
dataset_info:
- config_name: ar-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - en
  splits:
  - name: train
    num_bytes: 45207715
    num_examples: 151136
  download_size: 16097997
  dataset_size: 45207715
- config_name: ar-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - pl
  splits:
  - name: train
    num_bytes: 304851676
    num_examples: 823715
  download_size: 104585718
  dataset_size: 304851676
- config_name: en-sl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sl
  splits:
  - name: train
    num_bytes: 30479739
    num_examples: 140124
  download_size: 11727538
  dataset_size: 30479739
- config_name: en-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: train
    num_bytes: 167649057
    num_examples: 572717
  download_size: 57356138
  dataset_size: 167649057
- config_name: en-vi
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - vi
  splits:
  - name: train
    num_bytes: 7571598
    num_examples: 58116
  download_size: 2422413
  dataset_size: 7571598
---

# Dataset Card for OpusWikipedia

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

- **Homepage:** http://opus.nlpl.eu/Wikipedia.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

This is a corpus of parallel sentences extracted from Wikipedia by Krzysztof Wołk and Krzysztof Marasek.

Tha dataset contains 20 languages and 36 bitexts.

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs,
e.g.

```python
dataset = load_dataset("opus_wikipedia", lang1="it", lang2="pl")
```

You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/Wikipedia.php


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- ar
- bg
- cs
- de
- el
- en
- es
- fa
- fr
- he
- hu
- it
- nl
- pl
- pt
- ro
- ru
- sl
- tr
- vi

## Dataset Structure

### Data Instances

```
{
  'id': '0', 
  'translation': {
    "ar": "* Encyclopaedia of Mathematics online encyclopaedia from Springer, Graduate-level reference work with over 8,000 entries, illuminating nearly 50,000 notions in mathematics.",
    "en": "*Encyclopaedia of Mathematics online encyclopaedia from Springer, Graduate-level reference work with over 8,000 entries, illuminating nearly 50,000 notions in mathematics."
  } 
}
```

### Data Fields

- `id` (`str`): Unique identifier of the parallel sentence for the pair of languages.
- `translation` (`dict`): Parallel sentences for the pair of languages.

### Data Splits

The dataset contains a single `train` split.

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

```bibtex
@article{WOLK2014126,
title = {Building Subject-aligned Comparable Corpora and Mining it for Truly Parallel Sentence Pairs},
journal = {Procedia Technology},
volume = {18},
pages = {126-132},
year = {2014},
note = {International workshop on Innovations in Information and Communication Science and Technology, IICST 2014, 3-5 September 2014, Warsaw, Poland},
issn = {2212-0173},
doi = {https://doi.org/10.1016/j.protcy.2014.11.024},
url = {https://www.sciencedirect.com/science/article/pii/S2212017314005453},
author = {Krzysztof Wołk and Krzysztof Marasek},
keywords = {Comparable corpora, machine translation, NLP},
}
```

```bibtex
@InProceedings{TIEDEMANN12.463,
  author = {J{\"o}rg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Ugur Dogan and Bente Maegaard and Joseph Mariani and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
}
```

### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.