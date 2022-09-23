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
- ga
- hr
- hu
- it
- lt
- lv
- mt
- nl
- pl
- pt
- ro
- sh
- sk
- sl
- sv
license:
- unknown
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
pretty_name: OpusDgt
configs:
- bg-ga
- bg-hr
- bg-sh
- es-ga
- fi-ga
- ga-nl
- ga-sh
- hr-sk
- hr-sv
- mt-sh
dataset_info:
- config_name: bg-ga
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - ga
  splits:
  - name: train
    num_bytes: 82972428
    num_examples: 179142
  download_size: 15935979
  dataset_size: 82972428
- config_name: bg-hr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - hr
  splits:
  - name: train
    num_bytes: 239828651
    num_examples: 701572
  download_size: 46804111
  dataset_size: 239828651
- config_name: bg-sh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - sh
  splits:
  - name: train
    num_bytes: 498884905
    num_examples: 1488507
  download_size: 97402723
  dataset_size: 498884905
- config_name: fi-ga
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - ga
  splits:
  - name: train
    num_bytes: 61313136
    num_examples: 178619
  download_size: 14385114
  dataset_size: 61313136
- config_name: es-ga
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - ga
  splits:
  - name: train
    num_bytes: 63115666
    num_examples: 178696
  download_size: 14447359
  dataset_size: 63115666
- config_name: ga-sh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ga
        - sh
  splits:
  - name: train
    num_bytes: 28666585
    num_examples: 91613
  download_size: 6963357
  dataset_size: 28666585
- config_name: hr-sk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - sk
  splits:
  - name: train
    num_bytes: 170718371
    num_examples: 689263
  download_size: 42579941
  dataset_size: 170718371
- config_name: mt-sh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - mt
        - sh
  splits:
  - name: train
    num_bytes: 368562443
    num_examples: 1450424
  download_size: 88598048
  dataset_size: 368562443
- config_name: hr-sv
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - sv
  splits:
  - name: train
    num_bytes: 171858392
    num_examples: 696334
  download_size: 41410203
  dataset_size: 171858392
- config_name: ga-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ga
        - nl
  splits:
  - name: train
    num_bytes: 59065574
    num_examples: 170644
  download_size: 13730934
  dataset_size: 59065574
---

# Dataset Card for OpusDgt

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

- **Homepage:** http://opus.nlpl.eu/DGT.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

A collection of translation memories provided by the Joint Research Centre (JRC) Directorate-General for Translation (DGT): https://ec.europa.eu/jrc/en/language-technologies/dgt-translation-memory

Tha dataset contains 25 languages and 299 bitexts.

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs,
e.g.

```python
dataset = load_dataset("opus_dgt", lang1="it", lang2="pl")
```

You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/DGT.php


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
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
- ga
- hr
- hu
- it
- lt
- lv
- mt
- nl
- pl
- pt
- ro
- sh
- sk
- sl
- sv

## Dataset Structure

### Data Instances

```
{
  'id': '0', 
  'translation': {
    "bg": "Протокол за поправка на Конвенцията относно компетентността, признаването и изпълнението на съдебни решения по граждански и търговски дела, подписана в Лугано на 30 октомври 2007 г.",
    "ga": "Miontuairisc cheartaitheach maidir le Coinbhinsiún ar dhlínse agus ar aithint agus ar fhorghníomhú breithiúnas in ábhair shibhialta agus tráchtála, a siníodh in Lugano an 30 Deireadh Fómhair 2007"
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