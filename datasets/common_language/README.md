---
pretty_name: Common Language
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- ar
- br
- ca
- cnh
- cs
- cv
- cy
- de
- dv
- el
- en
- eo
- es
- et
- eu
- fa
- fr
- fy-NL
- ia
- id
- it
- ja
- ka
- kab
- ky
- lv
- mn
- mt
- nl
- pl
- pt
- rm-sursilv
- ro
- ru
- rw
- sah
- sl
- sv-SE
- ta
- tr
- tt
- uk
- zh-CN
- zh-HK
- zh-TW
licenses:
- cc-by-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|common_voice
task_categories:
- audio-classification
task_ids:
- speaker-language-identification
---

# Dataset Card for common_language

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

- **Homepage:** https://zenodo.org/record/5036977
- **Repository:** https://github.com/speechbrain/speechbrain/tree/develop/recipes/CommonLanguage
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Leaderboard:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Dataset Summary

This dataset is composed of speech recordings from languages that were carefully selected from the CommonVoice database. The total duration of audio recordings is 45.1 hours (i.e., 1 hour of material for each language). The dataset has been extracted from CommonVoice to train language-id systems.

### Supported Tasks and Leaderboards

The baselines for language-id are available in the SpeechBrain toolkit (see recipes/CommonLanguage):
https://github.com/speechbrain/speechbrain

### Languages

List of included languages:
```
Arabic, Basque, Breton, Catalan, Chinese_China, Chinese_Hongkong, Chinese_Taiwan, Chuvash, Czech, Dhivehi, Dutch, English, Esperanto, Estonian, French, Frisian, Georgian, German, Greek, Hakha_Chin, Indonesian, Interlingua, Italian, Japanese, Kabyle, Kinyarwanda, Kyrgyz, Latvian, Maltese, Mongolian, Persian, Polish, Portuguese, Romanian, Romansh_Sursilvan, Russian, Sakha, Slovenian, Spanish, Swedish, Tamil, Tatar, Turkish, Ukranian, Welsh
```

## Dataset Structure

### Data Instances

A typical data point comprises the `path` to the audio file, and its label `language`. Additional fields include `age`, `client_id`, `gender` and `sentence`.

```python
{
  'client_id': 'itln_trn_sp_175',
  'path': '/path/common_voice_kpd/Italian/train/itln_trn_sp_175/common_voice_it_18279446.wav',
  'audio': {'path': '/path/common_voice_kpd/Italian/train/itln_trn_sp_175/common_voice_it_18279446.wav',
		   'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32),
		   'sampling_rate': 48000},
  'sentence': 'Con gli studenti è leggermente simile.',
  'age': 'not_defined',
  'gender': 'not_defined',
  'language': 22
}
```

### Data Fields

`client_id` (`string`): An id for which client (voice) made the recording

`path` (`string`): The path to the audio file

- `audio` (`dict`): A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

`language` (`ClassLabel`): The language of the recording (see the `Languages` section above)

`sentence` (`string`): The sentence the user was prompted to speak

`age` (`string`): The age of the speaker.

`gender` (`string`): The gender of the speaker

### Data Splits

The dataset is already balanced and split into train, dev (validation) and test sets. 

| Name                              | Train  | Dev    | Test  |
|:---------------------------------:|:------:|:------:|:-----:|
| **# of utterances**               | 177552 | 47104  | 47704 |
| **# unique speakers**             | 11189  | 1297   | 1322  |
| **Total duration, hr**            | 30.04  | 7.53   | 7.53  |
| **Min duration, sec**             | 0.86   | 0.98   | 0.89  |
| **Mean duration, sec**            | 4.87   | 4.61   | 4.55  |
| **Max duration, sec**             | 21.72  | 105.67 | 29.83 |
| **Duration per language, min**    | ~40    | ~10    | ~10   |

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

The Mongolian and Ukrainian languages are spelled as "Mangolian" and "Ukranian" in this version of the dataset.

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[Ganesh Sinisetty; Pavlo Ruban; Oleksandr Dymov; Mirco Ravanelli](https://zenodo.org/record/5036977#.YdTZ5hPMJ70)

### Licensing Information

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode)

### Citation Information

```
@dataset{ganesh_sinisetty_2021_5036977,
  author       = {Ganesh Sinisetty and
                  Pavlo Ruban and
                  Oleksandr Dymov and
                  Mirco Ravanelli},
  title        = {CommonLanguage},
  month        = jun,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {0.1},
  doi          = {10.5281/zenodo.5036977},
  url          = {https://doi.org/10.5281/zenodo.5036977}
}
```

### Contributions

Thanks to [@anton-l](https://github.com/anton-l) for adding this dataset.
