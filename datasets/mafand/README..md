annotations_creators:
- expert-generated
language:
- en
- fr
- am
- bm
- bbj
- ee
- fon
- ha
- ig
- lg
- mos
- ny
- pcm
- rw
- sn
- sw
- tn
- tw
- wo
- xh
- yo
- zu
language_creators:
- expert-generated
license:
- cc-by-nc-4.0
multilinguality:
- translation
- multilingual
pretty_name: mafand
size_categories:
- 1K<n<10K
source_datasets:
- original
tags:
- news, mafand, masakhane
task_categories:
- translation
task_ids: []

# Dataset Card for [Needs More Information]

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://github.com/masakhane-io/lafand-mt
- **Repository:** https://github.com/masakhane-io/lafand-mt
- **Paper:** https://aclanthology.org/2022.naacl-main.223/
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** David Adelani (didelani@lsv.uni-saarland.de)

### Dataset Summary

MAFAND-MT is the largest MT benchmark for African languages in the news domain, covering 21 languages. 

### Supported Tasks and Leaderboards

Machine Translation

### Languages

The languages covered are: 
- Amharic
- Bambara
- Ghomala
- Ewe
- Fon
- Hausa
- Igbo
- Kinyarwanda
- Luganda
- Luo
- Mossi
- Nigerian-Pidgin
- Chichewa
- Shona
- Swahili
- Setswana
- Twi
- Wolof
- Xhosa
- Yoruba
- Zulu

## Dataset Structure

### Data Instances

{"translation": {"src": "--- President Buhari will determine when to lift lockdown  Minister", "tgt": "--- Ààr¹ Buhari ló lè yóhùn padà lórí ètò kónílégbélé  Mínísítà"}}


{"translation": {"en": "--- President Buhari will determine when to lift lockdown  Minister", "yo": "--- Ààr¹ Buhari ló lè yóhùn padà lórí ètò kónílégbélé  Mínísítà"}}


### Data Fields

"translation":  name of the task
"src" : source language e.g en
"tgt":  target language e.g yo

### Data Splits

Train/dev/test split

language| Train| Dev |Test
-|-|-|-
amh |-|899|1037
bam |3302|1484|1600
bbj |2232|1133|1430
ewe |2026|1414|1563
fon |2637|1227|1579
hau |5865|1300|1500
ibo |6998|1500|1500
kin |-|460|1006
lug |4075|1500|1500
luo |4262|1500|1500
mos |2287|1478|1574
nya |-|483|1004
pcm |4790|1484|1574
sna |-|556|1005
swa |30782|1791|1835
tsn |2100|1340|1835
twi |3337|1284|1500
wol |3360|1506|1500|
xho |-|486|1002|
yor |6644|1544|1558|
zul |3500|1239|998|


## Dataset Creation

### Curation Rationale

MAFAND was created from the news domain, translated from English or French to an African language

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Masakhane](https://github.com/masakhane-io/lafand-mt)
[Igbo](https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_en_mt)
[Swahili](https://opus.nlpl.eu/GlobalVoices.php)
[Hausa](https://www.statmt.org/wmt21/translation-task.html)
[Yoruba](https://github.com/uds-lsv/menyo-20k_MT)

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

Masakhane members

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

[CC-BY-4.0-NC](https://creativecommons.org/licenses/by-nc/4.0/)

### Citation Information

@inproceedings{adelani-etal-2022-thousand,
    title = "A Few Thousand Translations Go a Long Way! Leveraging Pre-trained Models for {A}frican News Translation",
    author = "Adelani, David  and
      Alabi, Jesujoba  and
      Fan, Angela  and
      Kreutzer, Julia  and
      Shen, Xiaoyu  and
      Reid, Machel  and
      Ruiter, Dana  and
      Klakow, Dietrich  and
      Nabende, Peter  and
      Chang, Ernie  and
      Gwadabe, Tajuddeen  and
      Sackey, Freshia  and
      Dossou, Bonaventure F. P.  and
      Emezue, Chris  and
      Leong, Colin  and
      Beukman, Michael  and
      Muhammad, Shamsuddeen  and
      Jarso, Guyo  and
      Yousuf, Oreen  and
      Niyongabo Rubungo, Andre  and
      Hacheme, Gilles  and
      Wairagala, Eric Peter  and
      Nasir, Muhammad Umair  and
      Ajibade, Benjamin  and
      Ajayi, Tunde  and
      Gitau, Yvonne  and
      Abbott, Jade  and
      Ahmed, Mohamed  and
      Ochieng, Millicent  and
      Aremu, Anuoluwapo  and
      Ogayo, Perez  and
      Mukiibi, Jonathan  and
      Ouoba Kabore, Fatoumata  and
      Kalipe, Godson  and
      Mbaye, Derguene  and
      Tapo, Allahsera Auguste  and
      Memdjokam Koagne, Victoire  and
      Munkoh-Buabeng, Edwin  and
      Wagner, Valencia  and
      Abdulmumin, Idris  and
      Awokoya, Ayodele  and
      Buzaaba, Happy  and
      Sibanda, Blessing  and
      Bukula, Andiswa  and
      Manthalu, Sam",
    booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jul,
    year = "2022",
    address = "Seattle, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.naacl-main.223",
    doi = "10.18653/v1/2022.naacl-main.223",
    pages = "3053--3070",
    abstract = "Recent advances in the pre-training for language models leverage large-scale datasets to create multilingual models. However, low-resource languages are mostly left out in these datasets. This is primarily because many widely spoken languages that are not well represented on the web and therefore excluded from the large-scale crawls for datasets. Furthermore, downstream users of these models are restricted to the selection of languages originally chosen for pre-training. This work investigates how to optimally leverage existing pre-trained models to create low-resource translation systems for 16 African languages. We focus on two questions: 1) How can pre-trained models be used for languages not included in the initial pretraining? and 2) How can the resulting translation models effectively transfer to new domains? To answer these questions, we create a novel African news corpus covering 16 languages, of which eight languages are not part of any existing evaluation dataset. We demonstrate that the most effective strategy for transferring both additional languages and additional domains is to leverage small quantities of high-quality translation data to fine-tune large pre-trained models.",
}