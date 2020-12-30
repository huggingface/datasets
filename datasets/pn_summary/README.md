---
annotations_creators:
- other
language_creators:
- other
languages:
- fa
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-classification
task_ids:
- summarization
- text-simplification
- topic-classification
---

# Dataset Card for Persian News Summary (pn_summary)

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

- **Homepage:** https://github.com/hooshvare/pn-summary/
- **Repository:** https://github.com/hooshvare/pn-summary/
- **Paper:** https://arxiv.org/abs/2012.11204
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [Mehrdad Farahani](mailto:m3hrdadfphi@gmail.com)

### Dataset Summary

A well-structured summarization dataset for the Persian language consists of 93,207 records. It is prepared for Abstractive/Extractive tasks (like cnn_dailymail for English). It can also be used in other scopes like Text Generation, Title Generation, and News Category Classification.
It is imperative to consider that the newlines were replaced with the `[n]` symbol. Please interpret them into normal newlines (for ex. `t.replace("[n]", "\n")`) and then use them for your purposes.

### Supported Tasks and Leaderboards

The dataset is prepared for Abstractive/Extractive summarization tasks (like cnn_dailymail for English). It can also be used in other scopes like Text Generation, Title Generation, and News Category Classification.

### Languages

The dataset covers Persian mostly and somewhere a combination with English.

## Dataset Structure

### Data Instances

A record consists of 8 features:

```python
record = ['id','title', 'article', 'summary', 'category', 'categories', 'network', 'link']
```
In the following table, you can a few examples of `pn_summmary`.

|   | id              | title                                            | article                                                                                                                                                                                                                                                                                                                                                                              | summary                                                                                                                                                                                                | category   | categories | network | link                      |
|---|-----------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------|---------|---------------------------|
| 1 | 738e296491f ... | مدیریت فروش نفت در دوران تحریم هوشمندانه عمل کرد | به گزارش شانا، علی کاردر امروز (۲۷ دی ماه) در مراسم تودیع محسن قمصری، مدیر سابق امور بین الملل شرکت ملی نفت ایران و معارفه سعید خوشرو، مدیر جدید امور بین الملل این شرکت، گفت: مدیریت امور بین‎الملل به عنوان یکی از تاثیرگذارترین مدیریت‌های شرکت ملی نفت ایران در دوران تحریم‌های ظالمانه غرب علیه کشورمان بسیار هوشمندانه عمل کرد و ما توانستیم به خوبی از عهده تحریم‌ها برآییم (...) | مدیرعامل شرکت ملی نفت، عملکرد مدیریت امور بین‎الملل این شرکت را در دوران تحریم بسیار هوشمندانه خواند و گفت: امور بین الملل در دوران پس از تحریم‎ها نیز می‌تواند نقش بزرگی در تسریع روند توسعه داشته باشد. | Oil-Energy | نفت        | Shana   | https://www.shana.ir/ ... |
| 2 | 00fa692a17 ...  | سبد محصولات پتروشیمی متنوع می‌شود                 | به گزارش شانا به نقل از شرکت ملی صنایع پتروشیمی، علی‌اصغر گودرزی‌فراهانی با اشاره به اینکه همه طرح‌های در حال اجرای صنعت پتروشیمی براساس پیشرفت فیزیکی و پیش‌بینی زمان راه‌اندازی در قالب طرح‌های جهش دوم و سوم تقسیم‌بندی شده‌اند، اظهار کرد: انتظار داریم که طرح‌های جهش دوم صنعت پتروشیمی که پیشرفت‌های (...)                                                                               | سرپرست مدیریت برنامه‌ریزی و توسعه شرکت ملی صنایع پتروشیمی گفت: تنوع محصولات پتروشیمی ایران با بهره‌برداری از طرح‌های جهش دوم و سوم صنعت پتروشیمی افزایش می‌یابد.                                           | Oil-Energy | پتروشیمی   | Shana   | https://www.shana.ir ...  |


### Data Fields

- `id`: (`string`), id of the news.
- `title`: (`string`), the title of the news.
- `article`: (`string`) the article of the news.
- `summary`: (`string`), the summary of the news.
- `category`: (`classification label`), the category of news in English, with possible values including `Economy`, `Roads-Urban`, `Banking-Insurance`, `Agriculture`, `International`..
- `categories`: (`string`), the category and sub-category of the news in Persian.
- `network`: (`classification label`), the name of the news agency, with possible values including `Tahlilbazaar`, `Imna`, `Shana`, `Mehr`, `Irna`..
- `link`: (`string`), the link of the news.

The category in English includes 18 different article categories from economy to tourism. 

```bash
Economy, Roads-Urban, Banking-Insurance, Agriculture, International, Oil-Energy, Industry, Transportation, Science-Technology, Local, Sports, Politics, Art-Culture, Society, Health, Research, Education-University, Tourism
```

### Data Splits

Training (82,022 records, 8 features), validation (5,592 records, 8 features), and test split (5,593 records and 8 features).

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The dataset comprises numerous articles of various categories that have been crawled from six news agency websites (Tahlilbazaar, Imna, Shana, Mehr, Irna, and Khabaronline).

### Annotations

#### Annotation process

Each record (article) includes the long original text as well as a human-generated summary. The total number of cleaned articles is 93,207 (from 200,000 crawled articles).

#### Who are the annotators?

The dataset was organized by [Mehrdad Farahani](https://github.com/m3hrdadfi), [Mohammad Gharachorloo](https://github.com/baarsaam) and [Mohammad Manthouri](https://github.com/mmanthouri) for this paper [Leveraging ParsBERT and Pretrained mT5 for Persian Abstractive Text Summarization](https://arxiv.org/abs/2012.11204)

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

This dataset was curated by [Mehrdad Farahani](https://github.com/m3hrdadfi), [Mohammad Gharachorloo](https://github.com/baarsaam) and [Mohammad Manthouri](https://github.com/mmanthouri).


### Licensing Information

This dataset is licensed under MIT License.

### Citation Information

```bibtex
@article{pnSummary,
  title={Leveraging ParsBERT and Pretrained mT5 for Persian Abstractive Text Summarization}, 
  author={Mehrdad Farahani, Mohammad Gharachorloo, Mohammad Manthouri},
  year={2020},
  eprint={2012.11204},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```