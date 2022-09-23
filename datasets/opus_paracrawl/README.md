---
annotations_creators:
- found
language_creators:
- found
language:
- bg
- ca
- cs
- da
- de
- el
- en
- es
- et
- eu
- fi
- fr
- ga
- gl
- hr
- hu
- is
- it
- km
- ko
- lt
- lv
- mt
- my
- nb
- ne
- nl
- nn
- pl
- pt
- ro
- ru
- si
- sk
- sl
- so
- sv
- sw
- tl
- uk
- zh
license:
- cc0-1.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1M<n<10M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: OpusParaCrawl
configs:
- de-pl
- el-en
- en-ha
- en-ig
- en-km
- en-so
- en-sw
- en-tl
- es-gl
- fr-nl
dataset_info:
- config_name: el-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - en
  splits:
  - name: train
    num_bytes: 6760375061
    num_examples: 21402471
  download_size: 2317102846
  dataset_size: 6760375061
- config_name: en-ha
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ha
  splits:
  - name: train
    num_bytes: 4618460
    num_examples: 19694
  download_size: 1757433
  dataset_size: 4618460
- config_name: en-ig
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ig
  splits:
  - name: train
    num_bytes: 6709030
    num_examples: 28829
  download_size: 2691716
  dataset_size: 6709030
- config_name: en-km
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - km
  splits:
  - name: train
    num_bytes: 31964493
    num_examples: 65115
  download_size: 9907279
  dataset_size: 31964493
- config_name: en-so
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - so
  splits:
  - name: train
    num_bytes: 5791003
    num_examples: 14880
  download_size: 2227727
  dataset_size: 5791003
- config_name: de-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - pl
  splits:
  - name: train
    num_bytes: 298637031
    num_examples: 916643
  download_size: 106891602
  dataset_size: 298637031
- config_name: fr-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - nl
  splits:
  - name: train
    num_bytes: 862303220
    num_examples: 2687673
  download_size: 319804705
  dataset_size: 862303220
- config_name: en-sw
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sw
  splits:
  - name: train
    num_bytes: 44264442
    num_examples: 132520
  download_size: 18611087
  dataset_size: 44264442
- config_name: en-tl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tl
  splits:
  - name: train
    num_bytes: 82502798
    num_examples: 248689
  download_size: 32933118
  dataset_size: 82502798
- config_name: es-gl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - gl
  splits:
  - name: train
    num_bytes: 582660901
    num_examples: 1879689
  download_size: 236696353
  dataset_size: 582660901
---

# Dataset Card for OpusParaCrawl

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

- **Homepage:** http://opus.nlpl.eu/ParaCrawl.php
- **Repository:** None
- **Paper:** [ParaCrawl: Web-Scale Acquisition of Parallel Corpora](https://aclanthology.org/2020.acl-main.417/)
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

Parallel corpora from Web Crawls collected in the ParaCrawl project.

Tha dataset contains:
- 42 languages, 43 bitexts
- total number of files: 59,996
- total number of tokens: 56.11G
- total number of sentence fragments: 3.13G

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs,
e.g.

```python
dataset = load_dataset("opus_paracrawl", lang1="en", lang2="so")
```

You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/ParaCrawl.php

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- bg
- ca
- cs
- da
- de
- el
- en
- es
- et
- eu
- fi
- fr
- ga
- gl
- hr
- hu
- is
- it
- km
- ko
- lt
- lv
- mt
- my
- nb
- ne
- nl
- nn
- pl
- pt
- ro
- ru
- si
- sk
- sl
- so
- sv
- sw
- tl
- uk
- zh

## Dataset Structure

### Data Instances

```
{
  'id': '0', 
  'translation': {
    "el": "Συνεχίστε ευθεία 300 μέτρα μέχρι να καταλήξουμε σε μια σωστή οδός (ul. Gagarina)? Περπατήστε περίπου 300 μέτρα μέχρι να φτάσετε το πρώτο ορθή οδός (ul Khotsa Namsaraeva)?",
    "en": "Go straight 300 meters until you come to a proper street (ul. Gagarina); Walk approximately 300 meters until you reach the first proper street (ul Khotsa Namsaraeva);"
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

- Creative commons CC0 (no rights reserved)

### Citation Information

```bibtex
@inproceedings{banon-etal-2020-paracrawl,
    title = "{P}ara{C}rawl: Web-Scale Acquisition of Parallel Corpora",
    author = "Ba{\~n}{\'o}n, Marta  and
      Chen, Pinzhen  and
      Haddow, Barry  and
      Heafield, Kenneth  and
      Hoang, Hieu  and
      Espl{\`a}-Gomis, Miquel  and
      Forcada, Mikel L.  and
      Kamran, Amir  and
      Kirefu, Faheem  and
      Koehn, Philipp  and
      Ortiz Rojas, Sergio  and
      Pla Sempere, Leopoldo  and
      Ram{\'\i}rez-S{\'a}nchez, Gema  and
      Sarr{\'\i}as, Elsa  and
      Strelec, Marek  and
      Thompson, Brian  and
      Waites, William  and
      Wiggins, Dion  and
      Zaragoza, Jaume",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.417",
    doi = "10.18653/v1/2020.acl-main.417",
    pages = "4555--4567",
}
```

```bibtex
@InProceedings{TIEDEMANN12.463,
  author = {Jörg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Uğur Doğan and Bente Maegaard and Joseph Mariani and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
}
```

### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.