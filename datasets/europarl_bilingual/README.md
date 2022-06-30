---
annotations_creators:
- found
language_creators:
- found
language:
- bg
- cs
- da
- de
- el
- en
- es
- et
- fi
- fr
- hu
- it
- lt
- lv
- nl
- pl
- pt
- ro
- sk
- sl
- sv
license:
- unknown
multilinguality:
- translation
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: europarl-bilingual
---

# Dataset Card for europarl-bilingual

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

- **Homepage:** [Statmt](http://www.statmt.org/europarl/)
- **Repository:** [OPUS Europarl](https://opus.nlpl.eu/Europarl.php)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/L12-1246/)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

A parallel corpus extracted from the European Parliament web site by Philipp Koehn (University of Edinburgh). The main intended use is to aid statistical machine translation research.

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: https://opus.nlpl.eu/Europarl.php
E.g.

`dataset = load_dataset("europarl_bilingual", lang1="fi", lang2="fr")`


### Supported Tasks and Leaderboards

Tasks: Machine Translation, Cross Lingual Word Embeddings (CWLE) Alignment

### Languages

- 21 languages, 211 bitexts
- total number of files: 207,775
- total number of tokens: 759.05M
- total number of sentence fragments: 30.32M

Every pair of the following languages is available:
- bg
- cs
- da
- de
- el
- en
- es
- et
- fi
- fr
- hu
- it
- lt
- lv
- nl
- pl
- pt
- ro
- sk
- sl
- sv


## Dataset Structure

### Data Instances

Here is an example from the en-fr pair:
```
{
  'translation': {
    'en': 'Resumption of the session',
    'fr': 'Reprise de la session'
  }
}
```

### Data Fields

- `translation`: a dictionary containing two strings paired with a key indicating the corresponding language.

### Data Splits

- `train`: only train split is provided. Authors did not provide a separation of examples in `train`, `dev` and `test`.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

The data set comes with the same license
as the original sources.
Please, check the information about the source
that is given on
http://opus.nlpl.eu/Europarl-v8.php

### Citation Information

```
@InProceedings{TIEDEMANN12.463,
  author = {J�rg Tiedemann},
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

Thanks to [@lucadiliello](https://github.com/lucadiliello) for adding this dataset.
