---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for Saudi Newspapers Corpus (SaudiNewsNet)

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
  - [Discussion of Social Impact and Biases](#discussion-of-social-impact-and-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [SaudiNewsNet](https://github.com/parallelfold/SaudiNewsNet)
- **Repository:** [Website](https://github.com/parallelfold/SaudiNewsNet)
- **Paper:** [More Information Needed]
- **Point of Contact:** [Mazen Abdulaziz](mailto:mazen.abdulaziz@gmail.com)

### Dataset Summary

The dataset contains a set of 31,030 Arabic newspaper articles alongwith metadata,
extracted from various online Saudi newspapers and written in MSA. 

The dataset currently contains **31,030** Arabic articles (with a total number of **8,758,976 words**). The articles were extracted from the following Saudi newspapers (sorted by number of articles):

 - [Al-Riyadh](http://www.alriyadh.com/) (4,852 articles)
 - [Al-Jazirah](http://al-jazirah.com/) (3,690 articles)
 - [Al-Yaum](http://alyaum.com/) (3,065 articles)
 - [Al-Eqtisadiya](http://aleqt.com/) (2,964 articles)
 - [Al-Sharq Al-Awsat](http://aawsat.com/) (2,947 articles)
 - [Okaz](http://www.okaz.com.sa/) (2,846 articles)
 - [Al-Watan](http://alwatan.com.sa/) (2,279 articles)
 - [Al-Madina](http://www.al-madina.com/) (2,252 articles)
 - [Al-Weeam](http://alweeam.com.sa/) (2,090 articles)
 - [Ain Alyoum](http://3alyoum.com/) (2,080 articles)
 - [Sabq](http://sabq.org/) (1,411 articles)
 - [Saudi Press Agency](http://www.spa.gov.sa) (369 articles)
 - [Arreyadi](http://www.arreyadi.com.sa/) (133 articles)
 - [Arreyadiyah](http://www.arreyadiyah.com/) (52 articles)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

Example:

```{'author': 'لندن: «الشرق الأوسط أونلاين»', 'content': 'أصدر الرئيس عبدربه منصور هادي رئيس الجمهورية اليمنية، اليوم (الاثنين)، قراراً جمهورياً بتعيين نايف البكري محافظا لعدن، وذلك بعد الانتصارات التي حققتها قوات المقاومة الشعبية في طرد المتمردين الحوثيين من المدينة.\n\n نايف البكري شغل منصب وكيل محافظة عدن لشؤون المديريات من قبل، وله علاقات جيدة مع مختلف القوى السياسية في المدينة، ويعتبر الرجل الأول.\n\n من جهة أخرى، أعلن بدر محمد باسملة وزير النقل اليمني عن إعداد خطة طوارئ للمدينة، مؤكدا أن أولوية الحكومة تشغيل الموانئ وتحسين الخدمات. موضحا ان فريقاً فنياً متخصصاً وصل من الإمارات لإعادة تشغيل المطار خلال أربع وعشرين ساعة واستئناف الرحلات من وإلى عدن خلال الساعات المقبلة. داعيا المنظمات الحقوقية والاعلاميين للقدومِ الى عدن لرصد المآسي التي ارتكبها المتمردون، مؤكداً ان الحكومة ستؤمن لهم رحلات من أي مطار في العالم.\n\n من جانبه، قال المتحدث الرسمي باسم الحكومة اليمنية راجح بادي، إن حجم الدمار في عدن لم يكن متوقعاً، لا سيما الذي طال البنى التحتية؛ فمطار عدن على سبيل المثال، مدمر بشكل شبه كامل، ومحطات توليد الكهرباء والمنشآت النفطية تعرضت هي الأخرى أكثر من مرة للقصف من قبل الحوثيين، حيث كانوا حينها يريدون الضغط على المقاومة الشعبية من خلال منعها من الحصول على المحروقات. وهو ما لم ينجحوا فيه. مبينا انه سيحتاج إعادة تأهيلها لمبالغ كبيرة وأشهر من العمل.', 'date_extracted': '2015-07-21 02:51:33', 'source': 'aawsat', 'title': 'الرئيس هادي يعين نايف البكري محافظا لعدن', 'url': 'http://aawsat.com/home/article/410801/الرئيس-هادي-يعين-نايف-البكري-محافظا-لعدن'}```

### Data Fields

 - **`url`**: The full URL from which the article was extracted.
 - **`date_extracted`**: The timestamp of the date on which the article was extracted. It has the format `YYYY-MM-DD hh:mm:ss`. Notice that this field does not necessarily represent the date on which the article was authored (or made available online), however for articles stamped with a date of extraction after August 1, 2015, this field most probably represents the date of authoring.
 - **`title`**: The title of the article. Contains missing values that were replaced with an empty string.
 - **`author`**: The author of the article. Contains missing values that were replaced with an empty string.
 - **`content`**: The content of the article.

### Data Splits

Only a train split. 

## Dataset Creation

### Curation Rationale

[More Information Needed]

[More Information Needed]

### Source Data

    | String Identifier  | Newspaper |
    | ------------------ | --------- |
    | aawsat | [Al-Sharq Al-Awsat](http://aawsat.com/) |
    | aleqtisadiya | [Al-Eqtisadiya](http://aleqt.com/) |
    | aljazirah | [Al-Jazirah](http://al-jazirah.com/) |
    | almadina | [Al-Madina](http://www.al-madina.com/) |
    | alriyadh | [Al-Riyadh](http://www.alriyadh.com/) |
    | alwatan | [Al-Watan](http://alwatan.com.sa/) |
    | alweeam | [Al-Weeam](http://alweeam.com.sa/) |
    | alyaum | [Al-Yaum](http://alyaum.com/)  |
    | arreyadi | [Arreyadi](http://www.arreyadi.com.sa/) |
    | arreyadiyah | [Arreyadi](http://www.arreyadiyah.com/) |
    | okaz | [Okaz](http://www.okaz.com.sa/) |
    | sabq | [Sabq](http://sabq.org/) |
    | was | [Saudi Press Agency](http://www.spa.gov.sa/) |
    | 3alyoum | [Ain Alyoum](http://3alyoum.com/) |

#### Initial Data Collection and Normalization

The Modern Standard Arabic texts crawled from the Internet.

#### Who are the source language producers?

Newspaper Websites.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

### Citation Information

```
@misc{hagrima2015,
author = "M. Alhagri",
title = "Saudi Newspapers Arabic Corpus (SaudiNewsNet)",
year = 2015,
url = "http://github.com/ParallelMazen/SaudiNewsNet"
}
```
