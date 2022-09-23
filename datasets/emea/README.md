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
- mt
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
- multilingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: EMEA
configs:
- bg-el
- cs-et
- de-mt
- es-lt
- fr-sk
dataset_info:
- config_name: bg-el
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - el
  splits:
  - name: train
    num_bytes: 296160562
    num_examples: 1044065
  download_size: 54531690
  dataset_size: 296160562
- config_name: cs-et
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - et
  splits:
  - name: train
    num_bytes: 180261167
    num_examples: 1053164
  download_size: 36065651
  dataset_size: 180261167
- config_name: de-mt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - mt
  splits:
  - name: train
    num_bytes: 182976918
    num_examples: 1000532
  download_size: 36665427
  dataset_size: 182976918
- config_name: fr-sk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - sk
  splits:
  - name: train
    num_bytes: 193605247
    num_examples: 1062753
  download_size: 38916074
  dataset_size: 193605247
- config_name: es-lt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - lt
  splits:
  - name: train
    num_bytes: 182623676
    num_examples: 1051370
  download_size: 35329033
  dataset_size: 182623676
---

# Dataset Card for EMEA

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

- **Homepage:** http://opus.nlpl.eu/EMEA.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/EMEA.php
E.g.

`dataset = load_dataset("emea", lang1="en", lang2="nl")`

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Here is an example of the `en-nl` configuration:

```
{'id': '4',
 'translation': {'en': 'EPAR summary for the public',
  'nl': 'EPAR-samenvatting voor het publiek'}}
```

### Data Fields

The data fields are:

- id: id of the sentence pair
- translation: a dictionary of the form {lang1: text_in_lang1, lang2: text_in_lang2}

### Data Splits

Sizes of some language pairs:

|   name   |train|
|----------|----:|
|bg-el|1044065|
|cs-et|1053164|
|de-mt|1000532|
|fr-sk|1062753|
|es-lt|1051370|


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

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.