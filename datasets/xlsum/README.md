---
task_categories:
- conditional-text-generation
task_ids:
- summarization
languages:
- am
- ar
- az
- bn
- my
- zh
- en
- fr
- gu
- ha
- hi
- ig
- id
- ja
- rn
- ko
- ky
- mr
- np
- om
- ps
- fa
- pidgin
- pt
- pa
- ru
- gd
- sr
- si
- so
- es
- sw
- ta
- te
- th
- ti
- tr
- uk
- ur
- uz
- vi
- cy
- yo
size_categories:
- 1M<n<10M
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- multilingual
source_datasets:
- original
paperswithcode_id: xl-sum
---

# Dataset Card for "XL-Sum"

## Table of Contents
- [Dataset Card Creation Guide](#dataset-card-creation-guide)
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

- **Repository:** [https://github.com/csebuetnlp/xl-sum](https://github.com/csebuetnlp/xl-sum)
- **Paper:** [XL-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages](https://aclanthology.org/2021.findings-acl.413/)
- **Point of Contact:** [Tahmid Hasan](mailto:tahmidhasan@cse.buet.ac.bd)

### Dataset Summary

We present XLSum, a comprehensive and diverse dataset comprising 1.35 million professionally  annotated article-summary pairs from BBC, extracted using a set of carefully designed heuristics. The dataset covers 45 languages ranging from low to high-resource, for many of which no public dataset is currently available. XL-Sum is highly abstractive, concise, and of high quality, as indicated by human and intrinsic evaluation. 


### Supported Tasks and Leaderboards

[More information needed](https://github.com/csebuetnlp/xl-sum)

### Languages

-  `amharic`
-  `arabic`
-  `azerbaijani`
-  `bengali`
-  `burmese`
-  `chinese_simplified`
-  `chinese_traditional`
-  `english`
-  `french`
-  `gujarati`
-  `hausa`
-  `hindi`
-  `igbo`
-  `indonesian`
-  `japanese`
-  `kirundi`
-  `korean`
-  `kyrgyz`
-  `marathi`
-  `nepali`
-  `oromo`
-  `pashto`
-  `persian`
-  `pidgin`
-  `portuguese`
-  `punjabi`
-  `russian`
-  `scottish_gaelic`
-  `serbian_cyrillic`
-  `serbian_latin`
-  `sinhala`
-  `somali`
-  `spanish`
-  `swahili`
-  `tamil`
-  `telugu`
-  `thai`
-  `tigrinya`
-  `turkish`
-  `ukrainian`
-  `urdu`
-  `uzbek`
-  `vietnamese`
-  `welsh`
-  `yoruba`

## Dataset Structure

### Data Instances

One example from the `English` dataset is given below in JSON format. 
  ```
  {
    "id": "technology-17657859",
    "url": "https://www.bbc.com/news/technology-17657859",
    "title": "Yahoo files e-book advert system patent applications",
    "summary": "Yahoo has signalled it is investigating e-book adverts as a way to stimulate its earnings.",
    "text": "Yahoo's patents suggest users could weigh the type of ads against the sizes of discount before purchase. It says in two US patent applications that ads for digital book readers have been \"less than optimal\" to date. The filings suggest that users could be offered titles at a variety of prices depending on the ads' prominence They add that the products shown could be determined by the type of book being read, or even the contents of a specific chapter, phrase or word. The paperwork was published by the US Patent and Trademark Office late last week and relates to work carried out at the firm's headquarters in Sunnyvale, California. \"Greater levels of advertising, which may be more valuable to an advertiser and potentially more distracting to an e-book reader, may warrant higher discounts,\" it states. Free books It suggests users could be offered ads as hyperlinks based within the book's text, in-laid text or even \"dynamic content\" such as video. Another idea suggests boxes at the bottom of a page could trail later chapters or quotes saying \"brought to you by Company A\". It adds that the more willing the customer is to see the ads, the greater the potential discount. \"Higher frequencies... may even be great enough to allow the e-book to be obtained for free,\" it states. The authors write that the type of ad could influence the value of the discount, with \"lower class advertising... such as teeth whitener advertisements\" offering a cheaper price than \"high\" or \"middle class\" adverts, for things like pizza. The inventors also suggest that ads could be linked to the mood or emotional state the reader is in as a they progress through a title. For example, they say if characters fall in love or show affection during a chapter, then ads for flowers or entertainment could be triggered. The patents also suggest this could applied to children's books - giving the Tom Hanks animated film Polar Express as an example. It says a scene showing a waiter giving the protagonists hot drinks \"may be an excellent opportunity to show an advertisement for hot cocoa, or a branded chocolate bar\". Another example states: \"If the setting includes young characters, a Coke advertisement could be provided, inviting the reader to enjoy a glass of Coke with his book, and providing a graphic of a cool glass.\" It adds that such targeting could be further enhanced by taking account of previous titles the owner has bought. 'Advertising-free zone' At present, several Amazon and Kobo e-book readers offer full-screen adverts when the device is switched off and show smaller ads on their menu screens, but the main text of the titles remains free of marketing. Yahoo does not currently provide ads to these devices, and a move into the area could boost its shrinking revenues. However, Philip Jones, deputy editor of the Bookseller magazine, said that the internet firm might struggle to get some of its ideas adopted. \"This has been mooted before and was fairly well decried,\" he said. \"Perhaps in a limited context it could work if the merchandise was strongly related to the title and was kept away from the text. \"But readers - particularly parents - like the fact that reading is an advertising-free zone. Authors would also want something to say about ads interrupting their narrative flow.\""
}
  ```

### Data Fields
-  'id': A string representing the article ID.
-  'url': A string representing the article URL.
-  'title': A string containing the article title.
-  'summary': A string containing the article summary.
-  'text' : A string containing the article text. 


### Data Splits

We used a 80%-10%-10% split for all languages with a few exceptions. `English` was split 93%-3.5%-3.5% for the evaluation set size to resemble that of `CNN/DM` and `XSum`; `Scottish Gaelic`, `Kyrgyz` and `Sinhala` had relatively fewer samples, their evaluation sets were increased to 500 samples for more reliable evaluation. Same articles were used for evaluation in the two variants of Chinese and Serbian to prevent data leakage in multilingual training. Individual dataset download links with train-dev-test example counts are given below:

Language      | ISO 639-1 Code | BBC subdomain(s) | Train | Dev | Test | Total |
--------------|----------------|------------------|-------|-----|------|-------|
Amharic | am | https://www.bbc.com/amharic | 5761 | 719 | 719 | 7199 |
Arabic | ar | https://www.bbc.com/arabic | 37519 | 4689 | 4689 | 46897 |
Azerbaijani | az | https://www.bbc.com/azeri | 6478 | 809 | 809 | 8096 |
Bengali | bn | https://www.bbc.com/bengali | 8102 | 1012 | 1012 | 10126 |
Burmese | my | https://www.bbc.com/burmese | 4569 | 570 | 570 | 5709 |
Chinese (Simplified) | zh-CN | https://www.bbc.com/ukchina/simp, https://www.bbc.com/zhongwen/simp | 37362 | 4670 | 4670 | 46702 |
Chinese (Traditional) | zh-TW | https://www.bbc.com/ukchina/trad, https://www.bbc.com/zhongwen/trad | 37373 | 4670 | 4670 | 46713 |
English | en | https://www.bbc.com/english, https://www.bbc.com/sinhala `*` | 306522 | 11535 | 11535 | 329592 |
French | fr | https://www.bbc.com/afrique | 8697 | 1086 | 1086 | 10869 |
Gujarati | gu | https://www.bbc.com/gujarati | 9119 | 1139 | 1139 | 11397 |
Hausa | ha | https://www.bbc.com/hausa | 6418 | 802 | 802 | 8022 |
Hindi | hi | https://www.bbc.com/hindi | 70778 | 8847 | 8847 | 88472 |
Igbo | ig | https://www.bbc.com/igbo | 4183 | 522 | 522 | 5227 |
Indonesian | id | https://www.bbc.com/indonesia | 38242 | 4780 | 4780 | 47802 |
Japanese | ja | https://www.bbc.com/japanese | 7113 | 889 | 889 | 8891 |
Kirundi | rn | https://www.bbc.com/gahuza | 5746 | 718 | 718 | 7182 |
Korean | ko | https://www.bbc.com/korean | 4407 | 550 | 550 | 5507 |
Kyrgyz | ky | https://www.bbc.com/kyrgyz | 2266 | 500 | 500 | 3266 |
Marathi | mr | https://www.bbc.com/marathi | 10903 | 1362 | 1362 | 13627 |
Nepali | np | https://www.bbc.com/nepali | 5808 | 725 | 725 | 7258 |
Oromo | om | https://www.bbc.com/afaanoromoo | 6063 | 757 | 757 | 7577 |
Pashto | ps | https://www.bbc.com/pashto | 14353 | 1794 | 1794 | 17941 |
Persian | fa | https://www.bbc.com/persian | 47251 | 5906 | 5906 | 59063 |
Pidgin`**` | n/a | https://www.bbc.com/pidgin | 9208 | 1151 | 1151 | 11510 |
Portuguese | pt | https://www.bbc.com/portuguese | 57402 | 7175 | 7175 | 71752 |
Punjabi | pa | https://www.bbc.com/punjabi | 8215 | 1026 | 1026 | 10267 |
Russian | ru | https://www.bbc.com/russian, https://www.bbc.com/ukrainian `*` | 62243 | 7780 | 7780 | 77803 |
Scottish Gaelic | gd | https://www.bbc.com/naidheachdan | 1313 | 500 | 500 | 2313 |
Serbian (Cyrillic) | sr | https://www.bbc.com/serbian/cyr | 7275 | 909 | 909 | 9093 |
Serbian (Latin) | sr | https://www.bbc.com/serbian/lat | 7276 | 909 | 909 | 9094 |
Sinhala | si | https://www.bbc.com/sinhala | 3249 | 500 | 500 | 4249 |
Somali | so | https://www.bbc.com/somali | 5962 | 745 | 745 | 7452 |
Spanish | es | https://www.bbc.com/mundo | 38110 | 4763 | 4763 | 47636 |
Swahili | sw | https://www.bbc.com/swahili | 7898 | 987 | 987 | 9872 |
Tamil | ta | https://www.bbc.com/tamil | 16222 | 2027 | 2027 | 20276 |
Telugu | te | https://www.bbc.com/telugu | 10421 | 1302 | 1302 | 13025 |
Thai | th | https://www.bbc.com/thai | 6616 | 826 | 826 | 8268 |
Tigrinya | ti | https://www.bbc.com/tigrinya | 5451 | 681 | 681 | 6813 |
Turkish | tr | https://www.bbc.com/turkce | 27176 | 3397 | 3397 | 33970 |
Ukrainian | uk | https://www.bbc.com/ukrainian | 43201 | 5399 | 5399 | 53999 |
Urdu | ur | https://www.bbc.com/urdu | 67665 | 8458 | 8458 | 84581 |
Uzbek | uz | https://www.bbc.com/uzbek | 4728 | 590 | 590 | 5908 |
Vietnamese | vi | https://www.bbc.com/vietnamese | 32111 | 4013 | 4013 | 40137 |
Welsh | cy | https://www.bbc.com/cymrufyw | 9732 | 1216 | 1216 | 12164 |
Yoruba | yo | https://www.bbc.com/yoruba | 6350 | 793 | 793 | 7936 |

`*` A lot of articles in BBC Sinhala and BBC Ukrainian were written in English and Russian respectively. They were identified using [Fasttext](https://arxiv.org/abs/1607.01759) and moved accordingly.

`**` West African Pidgin English

## Dataset Creation

### Curation Rationale

[More information needed](https://github.com/csebuetnlp/xl-sum)

### Source Data

[BBC News](https://www.bbc.co.uk/ws/languages)

#### Initial Data Collection and Normalization

[Detailed in the paper](https://aclanthology.org/2021.findings-acl.413/) 


#### Who are the source language producers?

[Detailed in the paper](https://aclanthology.org/2021.findings-acl.413/) 


### Annotations

[Detailed in the paper](https://aclanthology.org/2021.findings-acl.413/) 


#### Annotation process

[Detailed in the paper](https://aclanthology.org/2021.findings-acl.413/) 

#### Who are the annotators?

[Detailed in the paper](https://aclanthology.org/2021.findings-acl.413/) 

### Personal and Sensitive Information

[More information needed](https://github.com/csebuetnlp/xl-sum)

## Considerations for Using the Data

### Social Impact of Dataset

[More information needed](https://github.com/csebuetnlp/xl-sum)

### Discussion of Biases

[More information needed](https://github.com/csebuetnlp/xl-sum)

### Other Known Limitations

[More information needed](https://github.com/csebuetnlp/xl-sum)

## Additional Information

### Dataset Curators

[More information needed](https://github.com/csebuetnlp/xl-sum)

### Licensing Information

Contents of this repository are restricted to only non-commercial research purposes under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). Copyright of the dataset contents belongs to the original copyright holders.
### Citation Information

If you use any of the datasets, models or code modules, please cite the following paper:
```
@inproceedings{hasan-etal-2021-xl,
    title = "{XL}-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages",
    author = "Hasan, Tahmid  and
      Bhattacharjee, Abhik  and
      Islam, Md. Saiful  and
      Mubasshir, Kazi  and
      Li, Yuan-Fang  and
      Kang, Yong-Bin  and
      Rahman, M. Sohel  and
      Shahriyar, Rifat",
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-acl.413",
    pages = "4693--4703",
}
```


### Contributions

Thanks to [@abhik1505040](https://github.com/abhik1505040) and [@Tahmid](https://github.com/Tahmid04) for adding this dataset.
