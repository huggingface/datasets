---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
languages:
- fa
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- question-answering
task_ids:
- abstractive-qa
- explanation-generation
- extractive-qa
- machine-translation
- open-domain-qa
- summarization
- text-simplification
---

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/m3hrdadfi/wiki-summary
- **Repository:** https://github.com/m3hrdadfi/wiki-summary
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [Mehrdad Farahani](mailto:m3hrdadphi@gmail.com)

### Dataset Summary

The dataset extracted from Persian Wikipedia into the form of articles and highlights and cleaned the dataset into pairs of articles and highlights and reduced the articles' length (only version 1.0.0) and highlights' length to a maximum of 512 and 128, respectively, suitable for parsBERT. This dataset is created to achieve state-of-the-art results on some interesting NLP tasks like Text Summarization.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in Percy.

## Dataset Structure

### Data Instances

```
{
    'id' :'0598cfd2ac491a928615945054ab7602034a8f4f',
    'link': 'https://fa.wikipedia.org/wiki/انقلاب_1917_روسیه',
    'title': 'انقلاب 1917 روسیه',
    'article': 'نخست انقلاب فوریه ۱۹۱۷ رخ داد . در این انقلاب پس از یک‌سری اعتصابات ، تظاهرات و درگیری‌ها ، نیکولای دوم ، آخرین تزار روسیه از سلطنت خلع شد و یک دولت موقت به قدرت رسید . دولت موقت زیر نظر گئورگی لووف و الکساندر کرنسکی تشکیل شد . اکثر اعضای دولت موقت ، از شاخه منشویک حزب سوسیال دموکرات کارگری روسیه بودند . دومین مرحله ، انقلاب اکتبر ۱۹۱۷ بود . انقلاب اکتبر ، تحت نظارت حزب بلشویک (شاخه رادیکال از حزب سوسیال دموکرات کارگری روسیه) و به رهبری ولادیمیر لنین به پیش رفت و طی یک یورش نظامی همه‌جانبه به کاخ زمستانی سن پترزبورگ و سایر اماکن مهم ، قدرت را از دولت موقت گرفت . در این انقلاب افراد بسیار کمی کشته شدند . از زمان شکست روسیه در جنگ ۱۹۰۵ با ژاپن ، اوضاع بد اقتصادی ، گرسنگی ، عقب‌ماندگی و سرمایه‌داری و نارضایتی‌های گوناگون در بین مردم ، سربازان ، کارگران ، کشاورزان و نخبگان روسیه به‌وجود آمده‌بود . سرکوبهای تزار و ایجاد مجلس دوما نظام مشروطه حاصل آن دوران است . حزب سوسیال دموکرات ، اصلی‌ترین معترض به سیاست‌های نیکلای دوم بود که به‌طور گسترده بین دهقانان کشاورزان و کارگران کارخانجات صنعتی علیه سیاست‌های سیستم تزار فعالیت داشت . در اوت ۱۹۱۴ میلادی ، امپراتوری روسیه به دستور تزار وقت و به منظور حمایت از اسلاوهای صربستان وارد جنگ جهانی اول در برابر امپراتوری آلمان و امپراتوری اتریش-مجارستان شد . نخست فقط بلشویک‌ها ، مخالف ورود روسیه به این جنگ بودند و می‌گفتند که این جنگ ، سبب بدتر شدن اوضاع نابسامان اقتصادی و اجتماعی روسیه خواهد شد . در سال ۱۹۱۴ میلادی ، یعنی در آغاز جنگ جهانی اول ، روسیه بزرگترین ارتش جهان را داشت ، حدود ۱۲ میلیون سرباز و ۶ میلیون سرباز ذخیره ؛ ولی در پایان سال ۱۹۱۶ میلادی ، پنج میلیون نفر از سربازان روسیه کشته ، زخمی یا اسیر شده بودند . حدود دو میلیون سرباز نیز محل خدمت خود را ترک کرده و غالبا با اسلحه به شهر و دیار خود بازگشته بودند . در میان ۱۰ یا ۱۱ میلیون سرباز باقی‌مانده نیز ، اعتبار تزار و سلسله مراتب ارتش و اتوریته افسران بالا دست از بین رفته بود . عوامل نابسامان داخلی اعم از اجتماعی کشاورزی و فرماندهی نظامی در شکستهای روسیه بسیار مؤثر بود . شکست‌های روسیه در جنگ جهانی اول ، حامیان نیکلای دوم در روسیه را به حداقل خود رساند . در اوایل فوریه ۱۹۱۷ میلادی اکثر کارگران صنعتی در پتروگراد و مسکو دست به اعتصاب زدند . سپس شورش به پادگان‌ها و سربازان رسید . اعتراضات دهقانان نیز گسترش یافت . سوسیال دموکرات‌ها هدایت اعتراضات را در دست گرفتند . در ۱۱ مارس ۱۹۱۷ میلادی ، تزار وقت روسیه ، نیکلای دوم ، فرمان انحلال مجلس روسیه را صادر کرد ، اما اکثر نمایندگان مجلس متفرق نشدند و با تصمیمات نیکلای دوم مخالفت کردند . سرانجام در پی تظاهرات گسترده کارگران و سپس نافرمانی سربازان در سرکوب تظاهرکنندگان در پتروگراد ، نیکلای دوم از مقام خود استعفا داد . بدین ترتیب حکم‌رانی دودمان رومانوف‌ها بر روسیه پس از حدود سیصد سال پایان یافت .',
    'highlights': 'انقلاب ۱۹۱۷ روسیه ، جنبشی اعتراضی ، ضد امپراتوری روسیه بود که در سال ۱۹۱۷ رخ داد و به سرنگونی حکومت تزارها و برپایی اتحاد جماهیر شوروی انجامید . مبانی انقلاب بر پایه صلح-نان-زمین استوار بود . این انقلاب در دو مرحله صورت گرفت : در طول این انقلاب در شهرهای اصلی روسیه همانند مسکو و سن پترزبورگ رویدادهای تاریخی برجسته‌ای رخ داد . انقلاب در مناطق روستایی و رعیتی نیز پا به پای مناطق شهری در حال پیشروی بود و دهقانان زمین‌ها را تصرف کرده و در حال بازتوزیع آن در میان خود بودند .'
}
```

### Data Fields

- `id`: Article id
- `link`: Article link
- `title`: Title of the article
- `article`: Full text content in the article
- `highlights`: Summary of the article

### Data Splits

|    Train    |     Test    |  Validation |
|-------------|-------------|-------------| 
|   45,654    |     5,638   |    5,074    |

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

No annotations.

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

The dataset was created by Mehrdad Farahani.

### Licensing Information

[Apache License 2.0](https://github.com/m3hrdadfi/wiki-summary/blob/master/LICENSE)

### Citation Information

```
@misc{Bert2BertWikiSummaryPersian,
  author = {Mehrdad Farahani},
  title = {Summarization using Bert2Bert model on WikiSummary dataset},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/m3hrdadfi/wiki-summary},
}
```

### Contributions

Thanks to [@tanmoyio](https://github.com/tanmoyio) for adding this dataset.