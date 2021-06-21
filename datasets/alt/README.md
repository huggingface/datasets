---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- bn
- en
- fil
- hi
- id
- ja
- km
- lo
- ms
- my
- th
- vi
- zh
licenses:
- cc-by-4.0
multilinguality:
- multilingual
- translation
size_categories:
  alt-en:
  - 10K<n<100K
  alt-jp:
  - 10K<n<100K
  alt-km:
  - 10K<n<100K
  alt-my:
  - 10K<n<100K
  alt-my-transliteration:
  - 10K<n<100K
  alt-my-west-transliteration:
  - 100K<n<1M
  alt-parallel:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- structure-prediction
task_ids:
- machine-translation
- parsing
paperswithcode_id: alt
---

# Dataset Card for Asian Language Treebank (ALT)

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

- **Homepage:** https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/
- **Leaderboard:** 
- **Paper:** [Introduction of the Asian Language Treebank](https://ieeexplore.ieee.org/abstract/document/7918974)
- **Point of Contact:** [ALT info](alt-info@khn.nict.go.jp)

### Dataset Summary
The ALT project aims to advance the state-of-the-art Asian natural language processing (NLP) techniques through the open collaboration for developing and using ALT. It was first conducted by NICT and UCSY as described in Ye Kyaw Thu, Win Pa Pa, Masao Utiyama, Andrew Finch and Eiichiro Sumita (2016). Then, it was developed under [ASEAN IVO](https://www.nict.go.jp/en/asean_ivo/index.html) as described in this Web page. 

The process of building ALT began with sampling about 20,000 sentences from English Wikinews, and then these sentences were translated into the other languages.

### Supported Tasks and Leaderboards

Machine Translation, Dependency Parsing


### Languages

It supports 13 languages: 
  * Bengali
  * English
  * Filipino
  * Hindi
  * Bahasa Indonesia
  * Japanese
  * Khmer
  * Lao
  * Malay
  * Myanmar (Burmese)
  * Thai
  * Vietnamese
  * Chinese (Simplified Chinese).

## Dataset Structure

### Data Instances

#### ALT Parallel Corpus 
```
{
    "SNT.URLID": "80188",
    "SNT.URLID.SNTID": "1",
    "url": "http://en.wikinews.org/wiki/2007_Rugby_World_Cup:_Italy_31_-_5_Portugal",
    "bg": "[translated sentence]",
    "en": "[translated sentence]",
    "en_tok": "[translated sentence]",
    "fil": "[translated sentence]",
    "hi": "[translated sentence]",
    "id": "[translated sentence]",
    "ja": "[translated sentence]",
    "khm": "[translated sentence]",
    "lo": "[translated sentence]",
    "ms": "[translated sentence]",
    "my": "[translated sentence]",
    "th": "[translated sentence]",
    "vi": "[translated sentence]",
    "zh": "[translated sentence]"
}
```

#### ALT Treebank 
```
{
    "SNT.URLID": "80188",
    "SNT.URLID.SNTID": "1",
    "url": "http://en.wikinews.org/wiki/2007_Rugby_World_Cup:_Italy_31_-_5_Portugal",
    "status": "draft/reviewed",
    "value": "(S (S (BASENP (NNP Italy)) (VP (VBP have) (VP (VP (VP (VBN defeated) (BASENP (NNP Portugal))) (ADVP (RB 31-5))) (PP (IN in) (NP (BASENP (NNP Pool) (NNP C)) (PP (IN of) (NP (BASENP (DT the) (NN 2007) (NNP Rugby) (NNP World) (NNP Cup)) (PP (IN at) (NP (BASENP (NNP Parc) (FW des) (NNP Princes)) (COMMA ,) (BASENP (NNP Paris) (COMMA ,) (NNP France))))))))))) (PERIOD .))"
}
```

#### ALT Myanmar transliteration
```
{
    "en": "CASINO",
    "my": [
      "ကက်စီနို",
      "ကစီနို",
      "ကာစီနို",
      "ကာဆီနို"
    ]
}
```

### Data Fields


#### ALT Parallel Corpus 
- SNT.URLID: URL link to the source article listed in [URL.txt](https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206/URL.txt)
- SNT.URLID.SNTID: index number from 1 to 20000. It is a seletected sentence from `SNT.URLID`

and bg, en, fil, hi, id, ja, khm, lo, ms, my, th, vi, zh correspond to the target language

#### ALT Treebank
- status: it indicates how a sentence is annotated; `draft` sentences are annotated by one annotater and `reviewed` sentences are annotated by two annotater 

The annotatation is different from language to language, please see [their guildlines](https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/) for more detail.

### Data Splits

|           | train | valid | test  |
|-----------|-------|-------|-------|
| # articles | 1698 |  98   |  97   |
| # sentences | 18088 | 1000  | 1018  |


## Dataset Creation

### Curation Rationale

The ALT project was initiated by the [National Institute of Information and Communications Technology, Japan](https://www.nict.go.jp/en/) (NICT) in 2014. NICT started to build Japanese and English ALT and worked with the University of Computer Studies, Yangon, Myanmar (UCSY) to build Myanmar ALT in 2014. Then, the Badan Pengkajian dan Penerapan Teknologi, Indonesia (BPPT), the Institute for Infocomm Research, Singapore (I2R), the Institute of Information Technology, Vietnam (IOIT), and the National Institute of Posts, Telecoms and ICT, Cambodia (NIPTICT) joined to make ALT for Indonesian, Malay, Vietnamese, and Khmer in 2015. 


### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The dataset is sampled from the English Wikinews in 2014. These will be annotated with word segmentation, POS tags, and syntax information, in addition to the word alignment information by linguistic experts from
* National Institute of Information and Communications Technology, Japan (NICT) for Japanses and English
* University of Computer Studies, Yangon, Myanmar (UCSY) for Myanmar
* the Badan Pengkajian dan Penerapan Teknologi, Indonesia (BPPT) for Indonesian
* the Institute for Infocomm Research, Singapore (I2R) for Malay
* the Institute of Information Technology, Vietnam (IOIT) for Vietnamese
* the National Institute of Posts, Telecoms and ICT, Cambodia for Khmer

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

* National Institute of Information and Communications Technology, Japan (NICT) for Japanses and English
* University of Computer Studies, Yangon, Myanmar (UCSY) for Myanmar
* the Badan Pengkajian dan Penerapan Teknologi, Indonesia (BPPT) for Indonesian
* the Institute for Infocomm Research, Singapore (I2R) for Malay
* the Institute of Information Technology, Vietnam (IOIT) for Vietnamese
* the National Institute of Posts, Telecoms and ICT, Cambodia for Khmer

### Licensing Information

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

Please cite the following if you make use of the dataset:

Hammam Riza, Michael Purwoadi, Gunarso, Teduh Uliniansyah, Aw Ai Ti, Sharifah Mahani Aljunied, Luong Chi Mai, Vu Tat Thang, Nguyen Phuong Thai, Vichet Chea, Rapid Sun, Sethserey Sam, Sopheap Seng, Khin Mar Soe, Khin Thandar Nwet, Masao Utiyama, Chenchen Ding. (2016) "Introduction of the Asian Language Treebank" Oriental COCOSDA.

BibTeX:
```
@inproceedings{riza2016introduction,
  title={Introduction of the asian language treebank},
  author={Riza, Hammam and Purwoadi, Michael and Uliniansyah, Teduh and Ti, Aw Ai and Aljunied, Sharifah Mahani and Mai, Luong Chi and Thang, Vu Tat and Thai, Nguyen Phuong and Chea, Vichet and Sam, Sethserey and others},
  booktitle={2016 Conference of The Oriental Chapter of International Committee for Coordination and Standardization of Speech Databases and Assessment Techniques (O-COCOSDA)},
  pages={1--6},
  year={2016},
  organization={IEEE}
}
```

### Contributions

Thanks to [@chameleonTK](https://github.com/chameleonTK) for adding this dataset.
