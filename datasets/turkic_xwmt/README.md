---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- az
- ba
- en
- kaa
- kk
- ky
- ru
- sah
- tr
- uz
license:
- mit
multilinguality:
- translation
pretty_name: turkic_xwmt
size_categories:
- n<1K
task_categories:
- translation
task_ids: []
source_datasets:
- extended|WMT 2020 News Translation Task
configs:
- az-ba
- az-en
- az-kaa
- az-kk
- az-ky
- az-ru
- az-sah
- az-tr
- az-uz
- ba-az
- ba-en
- ba-kaa
- ba-kk
- ba-ky
- ba-ru
- ba-sah
- ba-tr
- ba-uz
- en-az
- en-ba
- en-kaa
- en-kk
- en-ky
- en-ru
- en-sah
- en-tr
- en-uz
- kaa-az
- kaa-ba
- kaa-en
- kaa-kk
- kaa-ky
- kaa-ru
- kaa-sah
- kaa-tr
- kaa-uz
- kk-az
- kk-ba
- kk-en
- kk-kaa
- kk-ky
- kk-ru
- kk-sah
- kk-tr
- kk-uz
- ky-az
- ky-ba
- ky-en
- ky-kaa
- ky-kk
- ky-ru
- ky-sah
- ky-tr
- ky-uz
- ru-az
- ru-ba
- ru-en
- ru-kaa
- ru-kk
- ru-ky
- ru-sah
- ru-tr
- ru-uz
- sah-az
- sah-ba
- sah-en
- sah-kaa
- sah-kk
- sah-ky
- sah-ru
- sah-tr
- sah-uz
- tr-az
- tr-ba
- tr-en
- tr-kaa
- tr-kk
- tr-ky
- tr-ru
- tr-sah
- tr-uz
- uz-az
- uz-ba
- uz-en
- uz-kaa
- uz-kk
- uz-ky
- uz-ru
- uz-sah
- uz-tr
---

# Dataset Card for turkic_xwmt

## Table of Contents
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

- **Homepage:** 
- **Repository:**[Github](https://github.com/turkic-interlingua/til-mt/tree/master/xwmt)
- **Paper:** [https://arxiv.org/abs/2109.04593](https://arxiv.org/abs/2109.04593)
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [turkicinterlingua@gmail.com](mailto:turkicinterlingua@gmail.com)

### Dataset Summary

To establish a comprehensive and challenging evaluation benchmark for Machine Translation in Turkic languages, we translate a test set originally introduced in WMT 2020 News Translation Task for English-Russian. The original dataset is profesionally translated and consists of sentences from news articles that are both English and Russian-centric. We adopt this evaluation set (X-WMT) and begin efforts to translate it into several Turkic languages. The current version of X-WMT includes covers 8 Turkic languages and 88 language directions with a minimum of 300 sentences per language direction.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Currently covered languages are (besides English and Russian):
- Azerbaijani (az)
- Bashkir (ba)
- Karakalpak (kaa)
- Kazakh (kk)
- Kirghiz (ky)
- Turkish (tr)
- Sakha (sah)
- Uzbek (uz)

## Dataset Structure

### Data Instances

A random example from the Russian-Uzbek set:
```
{"translation": {'ru': 'Моника Мутсвангва , министр информации Зимбабве , утверждает , что полиция вмешалась в отъезд Магомбейи из соображений безопасности и вследствие состояния его здоровья .', 'uz': 'Zimbabvening Axborot vaziri , Monika Mutsvanva Magombeyining xavfsizligi va sog'ligi tufayli bo'lgan jo'nab ketishinida politsiya aralashuvini ushlab turadi .'}}
```
### Data Fields

Each example has one field "translation" that contains two subfields: one per language, e.g. for the Russian-Uzbek set:
- **translation**: a dictionary with two subfields:
  - **ru**: the russian text
  - **uz**: the uzbek text
### Data Splits

<details>
  <summary>Click here to show the number of examples per configuration:</summary>
|         |   test |
|:--------|-------:|
| az-ba   |    600 |
| az-en   |    600 |
| az-kaa  |    300 |
| az-kk   |    500 |
| az-ky   |    500 |
| az-ru   |    600 |
| az-sah  |    300 |
| az-tr   |    500 |
| az-uz   |    600 |
| ba-az   |    600 |
| ba-en   |   1000 |
| ba-kaa  |    300 |
| ba-kk   |    700 |
| ba-ky   |    500 |
| ba-ru   |   1000 |
| ba-sah  |    300 |
| ba-tr   |    700 |
| ba-uz   |    900 |
| en-az   |    600 |
| en-ba   |   1000 |
| en-kaa  |    300 |
| en-kk   |    700 |
| en-ky   |    500 |
| en-ru   |   1000 |
| en-sah  |    300 |
| en-tr   |    700 |
| en-uz   |    900 |
| kaa-az  |    300 |
| kaa-ba  |    300 |
| kaa-en  |    300 |
| kaa-kk  |    300 |
| kaa-ky  |    300 |
| kaa-ru  |    300 |
| kaa-sah |    300 |
| kaa-tr  |    300 |
| kaa-uz  |    300 |
| kk-az   |    500 |
| kk-ba   |    700 |
| kk-en   |    700 |
| kk-kaa  |    300 |
| kk-ky   |    500 |
| kk-ru   |    700 |
| kk-sah  |    300 |
| kk-tr   |    500 |
| kk-uz   |    700 |
| ky-az   |    500 |
| ky-ba   |    500 |
| ky-en   |    500 |
| ky-kaa  |    300 |
| ky-kk   |    500 |
| ky-ru   |    500 |
| ky-sah  |    300 |
| ky-tr   |    400 |
| ky-uz   |    500 |
| ru-az   |    600 |
| ru-ba   |   1000 |
| ru-en   |   1000 |
| ru-kaa  |    300 |
| ru-kk   |    700 |
| ru-ky   |    500 |
| ru-sah  |    300 |
| ru-tr   |    700 |
| ru-uz   |    900 |
| sah-az  |    300 |
| sah-ba  |    300 |
| sah-en  |    300 |
| sah-kaa |    300 |
| sah-kk  |    300 |
| sah-ky  |    300 |
| sah-ru  |    300 |
| sah-tr  |    300 |
| sah-uz  |    300 |
| tr-az   |    500 |
| tr-ba   |    700 |
| tr-en   |    700 |
| tr-kaa  |    300 |
| tr-kk   |    500 |
| tr-ky   |    400 |
| tr-ru   |    700 |
| tr-sah  |    300 |
| tr-uz   |    600 |
| uz-az   |    600 |
| uz-ba   |    900 |
| uz-en   |    900 |
| uz-kaa  |    300 |
| uz-kk   |    700 |
| uz-ky   |    500 |
| uz-ru   |    900 |
| uz-sah  |    300 |
| uz-tr   |    600 |
</details>

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

**Translators, annotators and dataset contributors** (in alphabetical order)

Abilxayr Zholdybai  
Aigiz Kunafin  
Akylbek Khamitov  
Alperen Cantez  
Aydos Muxammadiyarov  
Doniyorbek Rafikjonov  
Erkinbek Vokhabov  
Ipek Baris  
Iskander Shakirov  
Madina Zokirjonova  
Mohiyaxon Uzoqova  
Mukhammadbektosh Khaydarov  
Nurlan Maharramli  
Petr Popov  
Rasul Karimov  
Sariya Kagarmanova  
Ziyodabonu Qobiljon qizi 

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

[MIT License](https://github.com/turkic-interlingua/til-mt/blob/master/xwmt/LICENSE)

### Citation Information

```
@inproceedings{mirzakhalov2021large,
  title={A Large-Scale Study of Machine Translation in Turkic Languages},
  author={Mirzakhalov, Jamshidbek and Babu, Anoop and Ataman, Duygu and Kariev, Sherzod and Tyers, Francis and Abduraufov, Otabek and Hajili, Mammad and Ivanova, Sardana and Khaytbaev, Abror and Laverghetta Jr, Antonio and others},
  booktitle={Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing},
  pages={5876--5890},
  year={2021}
}
```

### Contributions

This project was carried out with the help and contributions from dozens of individuals and organizations. We acknowledge and greatly appreciate each and every one of them:

**Authors on the publications** (in alphabetical order)

Abror Khaytbaev  
Ahsan Wahab  
Aigiz Kunafin  
Anoop Babu  
Antonio Laverghetta Jr.  
Behzodbek Moydinboyev  
Dr. Duygu Ataman  
Esra Onal  
Dr. Francis Tyers  
Jamshidbek Mirzakhalov  
Dr. John Licato  
Dr. Julia Kreutzer  
Mammad Hajili  
Mokhiyakhon Uzokova  
Dr. Orhan Firat  
Otabek Abduraufov  
Sardana Ivanova  
Shaxnoza Pulatova  
Sherzod Kariev  
Dr. Sriram Chellappan  

**Translators, annotators and dataset contributors** (in alphabetical order)

Abilxayr Zholdybai  
Aigiz Kunafin  
Akylbek Khamitov  
Alperen Cantez  
Aydos Muxammadiyarov  
Doniyorbek Rafikjonov  
Erkinbek Vokhabov  
Ipek Baris  
Iskander Shakirov  
Madina Zokirjonova  
Mohiyaxon Uzoqova  
Mukhammadbektosh Khaydarov  
Nurlan Maharramli  
Petr Popov  
Rasul Karimov  
Sariya Kagarmanova  
Ziyodabonu Qobiljon qizi  

**Industry supporters**

[Google Cloud](https://cloud.google.com/solutions/education)  
[Khan Academy Oʻzbek](https://uz.khanacademy.org/)  
[The Foundation for the Preservation and Development of the Bashkir Language](https://bsfond.ru/)  

Thanks to [@mirzakhalov](https://github.com/mirzakhalov) for adding this dataset.
