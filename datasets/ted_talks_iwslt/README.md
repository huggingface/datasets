---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
language:
- af
- am
- ar
- arq
- art
- as
- ast
- az
- be
- bg
- bi
- bn
- bo
- bs
- ca
- ceb
- cnh
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fil
- fr
- ga
- gl
- gu
- ha
- he
- hi
- hr
- ht
- hu
- hup
- hy
- id
- ig
- inh
- is
- it
- ja
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
- ltg
- lv
- mg
- mk
- ml
- mn
- mr
- ms
- mt
- my
- nb
- ne
- nl
- nn
- oc
- pa
- pl
- ps
- pt
- ro
- ru
- rup
- sh
- si
- sk
- sl
- so
- sq
- sr
- sv
- sw
- szl
- ta
- te
- tg
- th
- tl
- tlh
- tr
- tt
- ug
- uk
- ur
- uz
- vi
- zh
language_bcp47:
- art-x-bork
- fr-CA
- pt-BR
- zh-CN
- zh-TW
license:
- cc-by-nc-nd-4.0
multilinguality:
- translation
size_categories:
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: Web Inventory of Transcribed & Translated(WIT) Ted Talks
configs:
- de_ja_2014
- de_ja_2015
- de_ja_2016
- eu_ca_2014
- eu_ca_2015
- eu_ca_2016
- fr-ca_hi_2014
- fr-ca_hi_2015
- fr-ca_hi_2016
- nl_en_2014
- nl_en_2015
- nl_en_2016
- nl_hi_2014
- nl_hi_2015
- nl_hi_2016
---

# Dataset Card for Web Inventory of Transcribed & Translated(WIT) Ted Talks

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

- **Homepage:** https://wit3.fbk.eu/home
- **Repository:** https://drive.google.com/file/d/1Cz1Un9p8Xn9IpEMMrg2kXSDt0dnjxc4z/view?usp=sharing
- **Paper:** https://www.aclweb.org/anthology/2012.eamt-1.60.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Mauro Cettolo](mailto:cettolo@fbk.eu)
[Roldano Cattoni](mailto:cattoni@fbk.eu)


### Dataset Summary

The Web Inventory Talk is a collection of the original Ted talks and their translated version. The translations are available in more than 109+ languages, though the distribution is not uniform. 

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
E.g.

`dataset = load_dataset("ted_talks_iwslt", language_pair=("it", "pl"), year="2014")`

The full list of languages is: 'af', 'am', 'ar', 'arq', 'art-x-bork', 'as', 'ast', 'az', 'be', 'bg', 'bi', 'bn', 'bo', 'bs', 'ca', 'ceb', 'cnh', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fil', 'fr', 'fr-ca', 'ga', 'gl', 'gu', 'ha', 'he', 'hi', 'hr', 'ht', 'hu', 'hup', 'hy', 'id', 'ig', 'inh', 'is', 'it', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la', 'lb', 'lo', 'lt', 'ltg', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'nb', 'ne', 'nl', 'nn', 'oc', 'pa', 'pl', 'ps', 'pt', 'pt-br', 'ro', 'ru', 'rup', 'sh', 'si', 'sk', 'sl', 'so', 'sq', 'sr', 'srp', 'sv', 'sw', 'szl', 'ta', 'te', 'tg', 'th', 'tl', 'tlh', 'tr', 'tt', 'ug', 'uk', 'ur', 'uz', 'vi', 'zh', 'zh-cn', 'zh-tw'.

The full list of years is: '2014', '2015', '2016'.

### Supported Tasks and Leaderboards

machine learning task, language modeling and generation

### Languages

Ted talks are mostly held in English (`en`). Almost all of the talks have been translated, by volunteers, into Arabic, Bulgarian, Chinese (simplified), French, Italian, Korean, Portuguese (Brazil) and Spanish. For about 70 other languages, the number of translated talks ranges from several hundreds (e.g. such as other Dutch, German, Hebrew, Romanian) to one (e.g. Hausa, Hupa, Bislama, Ingush, Maltese).

The languages in the dataset are:
- af
- am
- ar
- arq
- art
- as
- ast
- az
- be
- bg
- bi
- bn
- bo
- bs
- ca
- ceb
- cnh
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fil
- fr
- ga
- gl
- gu
- ha
- he
- hi
- hr
- ht
- hu
- hup
- hy
- id
- ig
- inh
- is
- it
- ja
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
- ltg
- lv
- mg
- mk
- ml
- mn
- mr
- ms
- mt
- my
- nb
- ne
- nl
- nn
- oc
- pa
- pl
- ps
- pt
- ro
- ru
- rup
- sh
- si
- sk
- sl
- so
- sq
- sr
- srp: Serbian (`sr`)
- sv
- sw
- szl
- ta
- te
- tg
- th
- tl
- tlh
- tr
- tt
- ug
- uk
- ur
- uz
- vi
- zh

## Dataset Structure

### Data Instances

One example from the dataset is:

```
{'translation': {'hi': 'जब मार्च २०१४ में इबोला का प्रकोप छाया, पर्डिस सबेटी और उनकी टीम को वाइरस के जीनोम का अनुक्रमण करना था, सीखना था कि यह कैसे परवतिर्त होते हैं और फैलते हैं। सबेटी ने तुरंत ही अपने अनुसंधान को वेब में जारी किया, ताकि दुनिया भर के वाइरस ट्रैकर्स और वैज्ञानिक इस तत्काल लड़ाई में शामिल हो सकें। इस बातचीत में, वह दिखाती हैं कि सबका सहयोग ही कुंजी है वाइरस को रोकने के लिए--और लड़ने के लिए आगे आने वाले हमलों से। सबेटी ने कहा,"हमने खुले तौर पर काम किया, साझा किया और साथ काम किया"। "हमे दुनिया को एक वाइरस के विनाश से नहीं, पर अरबों दिलों और दिमागों की एकता से परिभाषित करना है"।',
  'nl': 'Toen Ebola in maart 2014 uitbrak, zijn Pardis Sabeti en haar team aan het werk gegaan om het genoom in kaart te brengen. Zo ontdekten ze hoe het virus zich verspreidde en muteerde. Sabeti zette direct haar onderzoek op het internet, zodat wereldwijd virus-jagers en wetenschappers mee konden werken aan de strijd. In deze talk laat ze zien hoe die openheid geholpen heeft bij het stoppen van het virus en hoe het kan helpen bij de strijd tegen het volgende virus. "We moesten transparant werken, delen en samenwerken". Sabeti zegt:"Laat de wereld niet ten onder gaan aan een virus, maar verlicht worden door miljoenen harten en geesten die samenwerken."'}}
```

The original XML files are formatted like this example:


```
<file id="1">
  <head>
    <url>http://www.ted.com/talks/ryan_holladay_to_hear_this_music_you_have_to_be_there_literally.html</url>
    <pagesize>66634</pagesize>
    <dtime>Sun Jan 12 15:17:32 CET 2014</dtime>
    <content-type>text/html; charset=utf-8</content-type>
    <encoding>utf-8</encoding>
    <videourl>http://download.ted.com/talks/RyanHolladay_2013S.mp4</videourl>
    <videopath>talks/RyanHolladay_2013S.mp4</videopath>
    <transcription>
      <seekvideo id="2939">(Music)</seekvideo>
      <seekvideo id="7555">For any of you who have visited or lived in New York City,</seekvideo>
      <seekvideo id="11221">these shots might start to look familiar.</seekvideo>
      <seekvideo id="16116">This is Central Park,</seekvideo>
      .
      .
      .
      <seekvideo id="361992">for people to interact with</seekvideo>
      <seekvideo id="363709">and experience music.</seekvideo>
      <seekvideo id="365451">Thank you.</seekvideo>
      <seekvideo id="367495">(Applause)</seekvideo>
    </transcription>
    <talkid>1903</talkid>
    <title>Ryan Holladay: To hear this music you have to be there. Literally</title>
    <description>The music industry ......segments of sounds that only play when a listener is physically nearby. (Filmed at TED@BCG.)</description>
    <keywords>entertainment,music,technology</keywords>
    <image>http://images.ted.com/images/ted/d98c17773da6f84e9f915895c270c7ffd2de3778_389x292.jpg</image>
    <date>2014/01/12</date>
    <wordnum>885</wordnum>
    <charnum>5051</charnum>
  </head>
  <content>(Music) For any of you who have visited or lived in New York City, these shots might start to look familiar. This is Central Park, ............new ways for people to interact with and experience music. Thank you. (Applause)</content>
</file>
```

### Data Fields
The fields of the dataset are:
- translation:
  - <lang1>: text in <lang1>
  - <lang2>L translated text in <lang2> 

Information about the original data files:

For each language, a single XML file is generated which includes all talks subtitled in 
that language. Each talk is enclosed in tags `<file id="int">` and `</file>` and includes, among other tags: 

| Tags | Description |
|---|:---|
| `<url>`| the address of the original HTML document of the talk |
| `<speaker>` | the name of the talk speaker |
| `<talkid>` | the numeric talk identifier |
| `<transcript>` | talk subtitles split in captions |
| `<date>` | the issue date of the talk |
| `<content>` |  talk subtitles |


### Data Splits

The paper doesn't provide any specific train-test-dev splits. However data can be split by available years (2014, 2015, 2016)


## Dataset Creation

### Curation Rationale

TED Conference, based in California, has been posting all video recordings of its talks together with subtitles in English and their translations in more than 80 languages. Aside from its cultural and social relevance, this content, which is published under the Creative Commons BYNC-ND license, also represents a precious language resource for the machine translation research community, thanks to its size, variety of topics, and covered languages.

### Source Data

#### Initial Data Collection and Normalization

The talks were collected from the [Ted Conference website](http://www.ted.com/)

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

Translation has been contributed by volunteers

### Personal and Sensitive Information

No personal and sensitive information is provided in the dataset. All talks are publicly available

## Considerations for Using the Data

### Social Impact of Dataset

In statistical machine translation, large amount of in-domain parallel data are usually required to properly train translation and reordering models. With more than 900+ Ted talks (as of 2011) and translation in more than 90+ languages. This dataset provides a useful resource for the MT research community. 

In turn, this enables easy access to a vast treasure trove of human knowledge. 

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The original dataset was curated by:
[Mauro Cettolo](mailto:cettolo@fbk.eu)
[Roldano Cattoni](mailto:cattoni@fbk.eu)

Author: 
Christian Girardi

For issues with the HuggingFace Dataset implementation, reach out: [Aakash Gupta](mailto:aakashg80@gmail.com)

### Licensing Information

cc-by-nc-nd-4.0

### Citation Information
```
@inproceedings{cettolo-etal-2012-wit3,
    title = "{WIT}3: Web Inventory of Transcribed and Translated Talks",
    author = "Cettolo, Mauro  and
      Girardi, Christian  and
      Federico, Marcello",
    booktitle = "Proceedings of the 16th Annual conference of the European Association for Machine Translation",
    month = may # " 28{--}30",
    year = "2012",
    address = "Trento, Italy",
    publisher = "European Association for Machine Translation",
    url = "https://www.aclweb.org/anthology/2012.eamt-1.60",
    pages = "261--268",
}

```

### Contributions

Thanks to [@skyprince999](https://github.com/skyprince999) for adding this dataset.
