---
pretty_name: mC4
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- af
- am
- ar
- az
- be
- bg
- bg-Latn
- bn
- ca
- ceb
- co
- cs
- cy
- da
- de
- el
- el-Latn
- en
- eo
- es
- et
- eu
- fa
- fi
- fil
- fr
- fy
- ga
- gd
- gl
- gu
- ha
- haw
- hi
- hi-Latn
- hmn
- ht
- hu
- hy
- id
- ig
- is
- it
- iw
- ja
- ja-Latn
- jv
- ka
- kk
- km
- kn
- ko
- ku
- ky
- la
- lb
- lo
- lt
- lv
- mg
- mi
- mk
- ml
- mn
- mr
- ms
- mt
- my
- ne
- nl
- "no"
- ny
- pa
- pl
- ps
- pt
- ro
- ru
- ru-Latn
- sd
- si
- sk
- sl
- sm
- sn
- so
- sq
- sr
- st
- su
- sv
- sw
- ta
- te
- tg
- th
- tr
- uk
- und
- ur
- uz
- vi
- xh
- yi
- yo
- zh
- zh-Latn
- zu
licenses:
- odc-by-1.0
multilinguality:
- multilingual
size_categories:
- n<1K
- 1K<n<10K
- 10K<n<100K
- 100K<n<1M
- 1M<n<10M
- 10M<n<100M
- 100M<n<1B
- 1B<n<10B
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: mc4
---

# Dataset Card for mC4

## Table of Contents

- [Dataset Card for mC4](#dataset-card-for-mc4)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://huggingface.co/datasets/allenai/c4
- **Paper:** https://arxiv.org/abs/1910.10683

### Dataset Summary

A multilingual colossal, cleaned version of Common Crawl's web crawl corpus. Based on Common Crawl dataset: "https://commoncrawl.org".

This is the version prepared by AllenAI, hosted at this address: https://huggingface.co/datasets/allenai/c4

108 languages are available and are reported in the table below.

Note that the languages that end with "-Latn" are simply romanized variants, i.e. written using the Latin script.

| language code   | language name        |
|:----------------|:---------------------|
| af              | Afrikaans            |
| am              | Amharic              |
| ar              | Arabic               |
| az              | Azerbaijani          |
| be              | Belarusian           |
| bg              | Bulgarian            |
| bg-Latn         | Bulgarian (Latin)    |
| bn              | Bangla               |
| ca              | Catalan              |
| ceb             | Cebuano              |
| co              | Corsican             |
| cs              | Czech                |
| cy              | Welsh                |
| da              | Danish               |
| de              | German               |
| el              | Greek                |
| el-Latn         | Greek (Latin)        |
| en              | English              |
| eo              | Esperanto            |
| es              | Spanish              |
| et              | Estonian             |
| eu              | Basque               |
| fa              | Persian              |
| fi              | Finnish              |
| fil             | Filipino             |
| fr              | French               |
| fy              | Western Frisian      |
| ga              | Irish                |
| gd              | Scottish Gaelic      |
| gl              | Galician             |
| gu              | Gujarati             |
| ha              | Hausa                |
| haw             | Hawaiian             |
| hi              | Hindi                |
| hi-Latn         | Hindi (Latin script) |
| hmn             | Hmong, Mong          |
| ht              | Haitian              |
| hu              | Hungarian            |
| hy              | Armenian             |
| id              | Indonesian           |
| ig              | Igbo                 |
| is              | Icelandic            |
| it              | Italian              |
| iw              | former Hebrew        |
| ja              | Japanese             |
| ja-Latn         | Japanese (Latin)     |
| jv              | Javanese             |
| ka              | Georgian             |
| kk              | Kazakh               |
| km              | Khmer                |
| kn              | Kannada              |
| ko              | Korean               |
| ku              | Kurdish              |
| ky              | Kyrgyz               |
| la              | Latin                |
| lb              | Luxembourgish        |
| lo              | Lao                  |
| lt              | Lithuanian           |
| lv              | Latvian              |
| mg              | Malagasy             |
| mi              | Maori                |
| mk              | Macedonian           |
| ml              | Malayalam            |
| mn              | Mongolian            |
| mr              | Marathi              |
| ms              | Malay                |
| mt              | Maltese              |
| my              | Burmese              |
| ne              | Nepali               |
| nl              | Dutch                |
| no              | Norwegian            |
| ny              | Nyanja               |
| pa              | Punjabi              |
| pl              | Polish               |
| ps              | Pashto               |
| pt              | Portuguese           |
| ro              | Romanian             |
| ru              | Russian              |
| ru-Latn         | Russian (Latin)      |
| sd              | Sindhi               |
| si              | Sinhala              |
| sk              | Slovak               |
| sl              | Slovenian            |
| sm              | San Marino           |
| sn              | Shona                |
| so              | Somali               |
| sq              | Albanian             |
| sr              | Serbian              |
| st              | Southern Sotho       |
| su              | Sundanese            |
| sv              | Swedish              |
| sw              | Swahili              |
| ta              | Tamil                |
| te              | Telugu               |
| tg              | Tajik                |
| th              | Thai                 |
| tr              | Turkish              |
| uk              | Ukrainian            |
| und             | Unknown language     |
| ur              | Urdu                 |
| uz              | Uzbek                |
| vi              | Vietnamese           |
| xh              | Xhosa                |
| yi              | Yiddish              |
| yo              | Yoruba               |
| zh              | Chinese              |
| zh-Latn         | Chinese (Latin)      |
| zu              | Zulu                 |

You can load the mC4 subset of any language like this:

```python
from datasets import load_dataset

en_mc4 = load_dataset("mc4", "en")
```

And if you can even specify a list of languages:

```python
from datasets import load_dataset

mc4_subset_with_five_languages = load_dataset("mc4", languages=["en", "fr", "es", "de", "zh"])
```

### Supported Tasks and Leaderboards

mC4 is mainly intended to pretrain language models and word representations.

### Languages

The dataset supports 108 languages.

## Dataset Structure

### Data Instances

An example form the `en` config is:

```
{'timestamp': '2018-06-24T01:32:39Z',
 'text': 'Farm Resources in Plumas County\nShow Beginning Farmer Organizations & Professionals (304)\nThere are 304 resources serving Plumas County in the following categories:\nMap of Beginning Farmer Organizations & Professionals serving Plumas County\nVictoria Fisher - Office Manager - Loyalton, CA\nAmy Lynn Rasband - UCCE Plumas-Sierra Administrative Assistant II - Quincy , CA\nShow Farm Income Opportunities Organizations & Professionals (353)\nThere are 353 resources serving Plumas County in the following categories:\nFarm Ranch And Forest Retailers (18)\nMap of Farm Income Opportunities Organizations & Professionals serving Plumas County\nWarner Valley Wildlife Area - Plumas County\nShow Farm Resources Organizations & Professionals (297)\nThere are 297 resources serving Plumas County in the following categories:\nMap of Farm Resources Organizations & Professionals serving Plumas County\nThere are 57 resources serving Plumas County in the following categories:\nMap of Organic Certification Organizations & Professionals serving Plumas County',
 'url': 'http://www.californialandcan.org/Plumas/Farm-Resources/'}
```

### Data Fields

The data have several fields:

- `url`: url of the source as a string
- `text`: text content as a string
- `timestamp`: timestamp as a string

### Data Splits

To build mC4, the authors used [CLD3](https://github.com/google/cld3) to identify over 100 languages. The resulting mC4 subsets for each language are reported in this table:

| config   | train   | validation   |
|:---------|:--------|:-------------|
| af       | ?       | ?            |
| am       | ?       | ?            |
| ar       | ?       | ?            |
| az       | ?       | ?            |
| be       | ?       | ?            |
| bg       | ?       | ?            |
| bg-Latn  | ?       | ?            |
| bn       | ?       | ?            |
| ca       | ?       | ?            |
| ceb      | ?       | ?            |
| co       | ?       | ?            |
| cs       | ?       | ?            |
| cy       | ?       | ?            |
| da       | ?       | ?            |
| de       | ?       | ?            |
| el       | ?       | ?            |
| el-Latn  | ?       | ?            |
| en       | ?       | ?            |
| eo       | ?       | ?            |
| es       | ?       | ?            |
| et       | ?       | ?            |
| eu       | ?       | ?            |
| fa       | ?       | ?            |
| fi       | ?       | ?            |
| fil      | ?       | ?            |
| fr       | ?       | ?            |
| fy       | ?       | ?            |
| ga       | ?       | ?            |
| gd       | ?       | ?            |
| gl       | ?       | ?            |
| gu       | ?       | ?            |
| ha       | ?       | ?            |
| haw      | ?       | ?            |
| hi       | ?       | ?            |
| hi-Latn  | ?       | ?            |
| hmn      | ?       | ?            |
| ht       | ?       | ?            |
| hu       | ?       | ?            |
| hy       | ?       | ?            |
| id       | ?       | ?            |
| ig       | ?       | ?            |
| is       | ?       | ?            |
| it       | ?       | ?            |
| iw       | ?       | ?            |
| ja       | ?       | ?            |
| ja-Latn  | ?       | ?            |
| jv       | ?       | ?            |
| ka       | ?       | ?            |
| kk       | ?       | ?            |
| km       | ?       | ?            |
| kn       | ?       | ?            |
| ko       | ?       | ?            |
| ku       | ?       | ?            |
| ky       | ?       | ?            |
| la       | ?       | ?            |
| lb       | ?       | ?            |
| lo       | ?       | ?            |
| lt       | ?       | ?            |
| lv       | ?       | ?            |
| mg       | ?       | ?            |
| mi       | ?       | ?            |
| mk       | ?       | ?            |
| ml       | ?       | ?            |
| mn       | ?       | ?            |
| mr       | ?       | ?            |
| ms       | ?       | ?            |
| mt       | ?       | ?            |
| my       | ?       | ?            |
| ne       | ?       | ?            |
| nl       | ?       | ?            |
| no       | ?       | ?            |
| ny       | ?       | ?            |
| pa       | ?       | ?            |
| pl       | ?       | ?            |
| ps       | ?       | ?            |
| pt       | ?       | ?            |
| ro       | ?       | ?            |
| ru       | ?       | ?            |
| ru-Latn  | ?       | ?            |
| sd       | ?       | ?            |
| si       | ?       | ?            |
| sk       | ?       | ?            |
| sl       | ?       | ?            |
| sm       | ?       | ?            |
| sn       | ?       | ?            |
| so       | ?       | ?            |
| sq       | ?       | ?            |
| sr       | ?       | ?            |
| st       | ?       | ?            |
| su       | ?       | ?            |
| sv       | ?       | ?            |
| sw       | ?       | ?            |
| ta       | ?       | ?            |
| te       | ?       | ?            |
| tg       | ?       | ?            |
| th       | ?       | ?            |
| tr       | ?       | ?            |
| uk       | ?       | ?            |
| und      | ?       | ?            |
| ur       | ?       | ?            |
| uz       | ?       | ?            |
| vi       | ?       | ?            |
| xh       | ?       | ?            |
| yi       | ?       | ?            |
| yo       | ?       | ?            |
| zh       | ?       | ?            |
| zh-Latn  | ?       | ?            |
| zu       | ?       | ?            |

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

AllenAI are releasing this dataset under the terms of ODC-BY. By using this, you are also bound by the Common Crawl terms of use in respect of the content contained in the dataset.

### Citation Information

```
@article{2019t5,
    author = {Colin Raffel and Noam Shazeer and Adam Roberts and Katherine Lee and Sharan Narang and Michael Matena and Yanqi Zhou and Wei Li and Peter J. Liu},
    title = {Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer},
    journal = {arXiv e-prints},
    year = {2019},
    archivePrefix = {arXiv},
    eprint = {1910.10683},
}
```

### Contributions

Thanks to [@dirkgr](https://github.com/dirkgr) and [@lhoestq](https://github.com/lhoestq) for adding this dataset.
