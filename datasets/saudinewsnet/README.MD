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
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for SaudiNewsNet

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

The dataset contains a set of 2,972 Arabic newspaper articles alongwith metadata,
extracted from various online Saudi newspapers and written in MSA. 

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

The dataset contains a set of 2,972 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers.

### Data Fields

```{'author': 'لندن: «الشرق الأوسط أونلاين»', 'content': 'أصدر الرئيس عبدربه منصور هادي رئيس الجمهورية اليمنية، اليوم (الاثنين)، قراراً جمهورياً بتعيين نايف البكري محافظا لعدن، وذلك بعد الانتصارات التي حققتها قوات المقاومة الشعبية في طرد المتمردين الحوثيين من المدينة.\n\n نايف البكري شغل منصب وكيل محافظة عدن لشؤون المديريات من قبل، وله علاقات جيدة مع مختلف القوى السياسية في المدينة، ويعتبر الرجل الأول.\n\n من جهة أخرى، أعلن بدر محمد باسملة وزير النقل اليمني عن إعداد خطة طوارئ للمدينة، مؤكدا أن أولوية الحكومة تشغيل الموانئ وتحسين الخدمات. موضحا ان فريقاً فنياً متخصصاً وصل من الإمارات لإعادة تشغيل المطار خلال أربع وعشرين ساعة واستئناف الرحلات من وإلى عدن خلال الساعات المقبلة. داعيا المنظمات الحقوقية والاعلاميين للقدومِ الى عدن لرصد المآسي التي ارتكبها المتمردون، مؤكداً ان الحكومة ستؤمن لهم رحلات من أي مطار في العالم.\n\n من جانبه، قال المتحدث الرسمي باسم الحكومة اليمنية راجح بادي، إن حجم الدمار في عدن لم يكن متوقعاً، لا سيما الذي طال البنى التحتية؛ فمطار عدن على سبيل المثال، مدمر بشكل شبه كامل، ومحطات توليد الكهرباء والمنشآت النفطية تعرضت هي الأخرى أكثر من مرة للقصف من قبل الحوثيين، حيث كانوا حينها يريدون الضغط على المقاومة الشعبية من خلال منعها من الحصول على المحروقات. وهو ما لم ينجحوا فيه. مبينا انه سيحتاج إعادة تأهيلها لمبالغ كبيرة وأشهر من العمل.', 'date_extracted': '2015-07-21 02:51:33', 'source': 'aawsat', 'title': 'الرئيس هادي يعين نايف البكري محافظا لعدن', 'url': 'http://aawsat.com/home/article/410801/الرئيس-هادي-يعين-نايف-البكري-محافظا-لعدن'}```

### Data Splits

Only a train split. 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

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
@misc{hagrima2015, author = "M. Alhagri", title = "Saudi Newspapers Arabic Corpus
(SaudiNewsNet)", year = 2015, url = "http://github.com/ParallelMazen/SaudiNewsNet" }
```
