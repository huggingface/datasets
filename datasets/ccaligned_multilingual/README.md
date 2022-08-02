---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- af
- ak
- am
- ar
- as
- ay
- az
- be
- bg
- bm
- bn
- br
- bs
- ca
- ceb
- ckb
- cs
- cy
- de
- dv
- el
- eo
- es
- fa
- ff
- fi
- fo
- fr
- fy
- ga
- gl
- gn
- gu
- he
- hi
- hr
- hu
- id
- ig
- is
- it
- iu
- ja
- ka
- kac
- kg
- kk
- km
- kn
- ko
- ku
- ky
- la
- lg
- li
- ln
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
- 'no'
- nso
- ny
- om
- or
- pa
- pl
- ps
- pt
- rm
- ro
- ru
- rw
- sc
- sd
- se
- shn
- si
- sk
- sl
- sn
- so
- sq
- sr
- ss
- st
- su
- sv
- sw
- syc
- szl
- ta
- te
- tg
- th
- ti
- tl
- tn
- tr
- ts
- tt
- ug
- uk
- ur
- uz
- ve
- vi
- war
- wo
- xh
- yi
- yo
- zgh
- zh
- zu
- zza
license:
- unknown
multilinguality:
- translation
size_categories:
- n<1K
- 1K<n<10K
- 10K<n<100K
- 100K<n<1M
- 1M<n<10M
- 10M<n<100M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-translation
paperswithcode_id: ccaligned
pretty_name: CCAligned
---

# Dataset Card for ccaligned_multilingual

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

- **Homepage:** http://www.statmt.org/cc-aligned/
- **Repository:** [Needs More Information]
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.480.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

CCAligned consists of parallel or comparable web-document pairs in 137 languages aligned with English. These web-document pairs were constructed by performing language identification on raw web-documents, and ensuring corresponding language codes were corresponding in the URLs of web documents. This pattern matching approach yielded more than 100 million aligned documents paired with English. Recognizing that each English document was often aligned to mulitple documents in different target language, we can join on English documents to obtain aligned documents that directly pair two non-English documents (e.g., Arabic-French). This corpus was created from 68 Commoncrawl Snapshots.


To load a language which isn't part of the config, all you need to do is specify the language code. You can find the valid languages in http://www.statmt.org/cc-aligned/ E.g.
```
dataset = load_dataset("ccaligned_multilingual", language_code="fr_XX", type="documents")
```
or
```
dataset = load_dataset("ccaligned_multilingual", language_code="fr_XX", type="sentences")
```


### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text in the dataset is in (137) multiple languages aligned with english.

## Dataset Structure

### Data Instances

An instance of `documents` type for language `ak_GH`:

```
{'Domain': 'islamhouse.com', 'Source_URL': 'https://islamhouse.com/en/audios/373088/', 'Target_URL': 'https://islamhouse.com/ak/audios/373088/', 'translation': {'ak_GH': "Ntwatiaa / wɔabɔ no tɔfa wɔ mu no te ase ma Umrah - Arab kasa|Islamhouse.com|Follow us:|facebook|twitter|taepe|Titles All|Fie wibesite|kasa nyina|Buukuu edi adanse ma prente|Nhyehyɛmu|Nyim/sua Islam|Curriculums|Nyina ndeɛma|Nyina ndeɛma (295)|Buukuu/ nwoma (2)|sini / muuvi (31)|ɔdio (262)|Aɛn websideNew!|Kɔ wura kramosom mu seisei|Ebio|figa/kaasɛ|Farebae|AKAkan|Kratafa titriw|kasa interface( anyimu) : Akan|Kasa ma no mu-nsɛm : Arab kasa|ɔdio|Ntwatiaa / wɔabɔ no tɔfa wɔ mu no te ase ma Umrah|play|pause|stop|mute|unmute|max volume|Kasakyerɛ ni :|Farebae:|17 / 11 / 1432 , 15/10/2011|Nhyehyɛmu:|Jurisprudence/ Esum Nimdea|Som|Hajj na Umrah|Jurisprudence/ Esum Nimdea|Som|Hajj na Umrah|Mmira ma Hajj na Umrah|nkyerɛmu|kasamu /sɛntɛns ma te ase na Umrah wɔ ... mu no hann ma no Quran na Sunnah na te ase ma no nana na no kasamu /sɛntɛns ma bi ma no emerging yi adu obusuani|Akenkane we ye di ko kasa bi su (36)|Afar - Qafár afa|Akan|Amhari ne - አማርኛ|Arab kasa - عربي|Assamese - অসমীয়া|Bengali - বাংলা|Maldive - ދިވެހި|Greek - Ελληνικά|English ( brofo kasa) - English|Persian - فارسی|Fula - pulla|French - Français|Hausa - Hausa|Kurdish - كوردی سۆرانی|Uganda ne - Oluganda|Mandinka - Mandinko|Malayalam - മലയാളം|Nepali - नेपाली|Portuguese - Português|Russian - Русский|Sango - Sango|Sinhalese - සිංහල|Somali - Soomaali|Albania ne - Shqip|Swahili - Kiswahili|Telugu - తెలుగు ప్రజలు|Tajik - Тоҷикӣ|Thai - ไทย|Tagalog - Tagalog|Turkish - Türkçe|Uyghur - ئۇيغۇرچە|Urdu - اردو|Uzbeck ne - Ўзбек тили|Vietnamese - Việt Nam|Wolof - Wolof|Chine ne - 中文|Soma kɔ bi kyerɛ adwen kɔ wɛb ebusuapanin|Soma kɔ ne kɔ hom adamfo|Soma kɔ bi kyerɛ adwen kɔ wɛb ebusuapanin|Nsɔwso fael (1)|1|الموجز في فقه العمرة|MP3 14.7 MB|Enoumah ebatahu|Rituals/Esom ajomadie ewu Hajji mmire .. 1434 AH [01] no fapemso Enum|Fiidbak/ Ye hiya wu jun kyiri|Lenke de yɛe|kɔntakt yɛn|Aɛn webside|Qura'an Kro kronkrom|Balagh|wɔ mfinimfin Dowload faele|Yɛ atuu bra Islam mu afei|Tsin de yɛe ewu|Anaa bomu/combine hɛn melin liste|© Islamhouse Website/ Islam dan webi site|×|×|Yi mu kasa|", 'en_XX': 'SUMMARY in the jurisprudence of Umrah - Arabic - Abdul Aziz Bin Marzooq Al-Turaifi|Islamhouse.com|Follow us:|facebook|twitter|QuranEnc.com|HadeethEnc.com|Type|Titles All|Home Page|All Languages|Categories|Know about Islam|All items|All items (4057)|Books (701)|Articles (548)|Fatawa (370)|Videos (1853)|Audios (416)|Posters (98)|Greeting cards (22)|Favorites (25)|Applications (21)|Desktop Applications (3)|To convert to Islam now !|More|Figures|Sources|Curriculums|Our Services|QuranEnc.com|HadeethEnc.com|ENEnglish|Main Page|Interface Language : English|Language of the content : Arabic|Audios|تعريب عنوان المادة|SUMMARY in the jurisprudence of Umrah|play|pause|stop|mute|unmute|max volume|Lecturer : Abdul Aziz Bin Marzooq Al-Turaifi|Sources:|AlRaya Islamic Recoding in Riyadh|17 / 11 / 1432 , 15/10/2011|Categories:|Islamic Fiqh|Fiqh of Worship|Hajj and Umrah|Islamic Fiqh|Fiqh of Worship|Hajj and Umrah|Pilgrimage and Umrah|Description|SUMMARY in jurisprudence of Umrah: A statement of jurisprudence and Umrah in the light of the Quran and Sunnah and understanding of the Ancestors and the statement of some of the emerging issues related to them.|This page translated into (36)|Afar - Qafár afa|Akane - Akan|Amharic - አማርኛ|Arabic - عربي|Assamese - অসমীয়া|Bengali - বাংলা|Maldivi - ދިވެހި|Greek - Ελληνικά|English|Persian - فارسی|Fula - pulla|French - Français|Hausa - Hausa|kurdish - كوردی سۆرانی|Ugandan - Oluganda|Mandinka - Mandinko|Malayalam - മലയാളം|Nepali - नेपाली|Portuguese - Português|Russian - Русский|Sango - Yanga ti Sango|Sinhalese - සිංහල|Somali - Soomaali|Albanian - Shqip|Swahili - Kiswahili|Telugu - తెలుగు|Tajik - Тоҷикӣ|Thai - ไทย|Tagalog - Tagalog|Turkish - Türkçe|Uyghur - ئۇيغۇرچە|Urdu - اردو|Uzbek - Ўзбек тили|Vietnamese - Việt Nam|Wolof - Wolof|Chinese - 中文|Send a comment to Webmaster|Send to a friend?|Send a comment to Webmaster|Attachments (1)|1|الموجز في فقه العمرة|MP3 14.7 MB|The relevant Material|The rituals of the pilgrimage season .. 1434 AH [ 01] the fifth pillar|The Quality of the Accepted Hajj (Piligrimage) and Its Limitations|Easy Path to the Rules of the Rites of Hajj|A Call to the Pilgrims of the Scared House of Allah|More|feedback|Important links|Contact us|Privacy policy|Islam Q&A|Learning Arabic Language|About Us|Convert To Islam|Noble Quran encyclopedia|IslamHouse.com Reader|Encyclopedia of Translated Prophetic Hadiths|Our Services|The Quran|Balagh|Center for downloading files|To embrace Islam now...|Follow us through|Or join our mailing list.|© Islamhouse Website|×|×|Choose language|'}}
```

An instance of `sentences` type for language `ak_GH`:

```
{'LASER_similarity': 1.4549942016601562, 'translation': {'ak_GH': 'Salah (nyamefere) ye Mmerebeia', 'en_XX': 'What he dislikes when fasting (10)'}}
```

### Data Fields

For `documents` type:

- `Domain`: a `string` feature containing the domain.
- `Source_URL`: a `string` feature containing the source URL.
- `Target_URL`: a `string` feature containing the target URL.
- `translation`: a `dictionary` feature with two keys :
  - `en_XX`: a `string` feature containing the content in English.
  - <language_code>: a `string` feature containing the content in the `language_code` specified.

For `sentences` type:

- `LASER_similarity`: a `float32` feature representing the LASER similarity score.
- `translation`: a `dictionary` feature with two keys :
  - `en_XX`: a `string` feature containing the content in English.
  - <language_code>: a `string` feature containing the content in the `language_code` specified.

### Data Splits

Split sizes of some small configurations:

|   name   |train|
|----------|----:|
|documents-zz_TR|41|
|sentences-zz_TR|34|
|documents-tz_MA|4|
|sentences-tz_MA|33|
|documents-ak_GH|249|
|sentences-ak_GH|478|

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

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

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

[Needs More Information]

### Citation Information

```
@inproceedings{elkishky_ccaligned_2020,
 author = {El-Kishky, Ahmed and Chaudhary, Vishrav and Guzm{\'a}n, Francisco and Koehn, Philipp},
 booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)},
 month = {November},
 title = {{CCAligned}: A Massive Collection of Cross-lingual Web-Document Pairs},
 year = {2020}
 address = "Online",
 publisher = "Association for Computational Linguistics",
 url = "https://www.aclweb.org/anthology/2020.emnlp-main.480",
 doi = "10.18653/v1/2020.emnlp-main.480",
 pages = "5960--5969"
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.