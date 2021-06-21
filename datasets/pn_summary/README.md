---
annotations_creators:
- found
language_creators:
- found
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
paperswithcode_id: pn-summary
---

# Dataset Card for Persian News Summary (pn_summary)

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
In the following, you can see an example of `pn_summmary`.

```json
{
    "article": "به گزارش شانا، علی کاردر امروز (۲۷ دی ماه) در مراسم تودیع محسن قمصری، مدیر سابق امور بین الملل شرکت ملی نفت ایران و معارفه سعید خوشرو، مدیر جدید امور بین الملل این شرکت، گفت: مدیریت امور بین\u200eالملل به عنوان یکی از تاثیرگذارترین مدیریت\u200cهای شرکت ملی نفت ایران در دوران تحریم\u200cهای ظالمانه غرب علیه کشورمان بسیار هوشمندانه عمل کرد و ما توانستیم به خوبی از عهده تحریم\u200cها برآییم. [n] وی افزود: مجموعه امور بین الملل در همه دوران\u200cها با سختی\u200cها و مشکلات بسیاری مواجه بوده است، به ویژه در دوره اخیر به دلیل مسائل پیرامون تحریم وظیفه سنگینی بر عهده داشت که با تدبیر مدیریت خوب این مجموعه سربلند از آن بیرون آمد. [n] کاردر با قدردانی از زحمات محسن قمصری، به سلامت مدیریت امور بین الملل این شرکت اشاره کرد و افزود: محوریت کار مدیریت اموربین الملل سلامت مالی بوده است. [n] وی بر ضرورت نهادینه سازی جوانگرایی در مدیریت شرکت ملی نفت ایران تاکید کرد و گفت: مدیریت امور بین الملل در پرورش نیروهای زبده و کارآزموده آنچنان قوی عملکرده است که برای انتخاب مدیر جدید مشکلی وجود نداشت. [n] کاردر، حرفه\u200eای\u200eگری و کار استاندارد را از ویژگی\u200cهای مدیران این مدیریت برشمرد و گفت: نگاه جامع، خلاقیت و نوآوری و بکارگیری نیروهای جوان باید همچنان مد نظر مدیریت جدید امور بین الملل شرکت ملی نفت ایران باشد.",
    "categories": "نفت",
    "category": 5,
    "id": "738e296491f8b24c5aa63e9829fd249fb4428a66",
    "link": "https://www.shana.ir/news/275284/%D9%85%D8%AF%DB%8C%D8%B1%DB%8C%D8%AA-%D9%81%D8%B1%D9%88%D8%B4-%D9%86%D9%81%D8%AA-%D8%AF%D8%B1-%D8%AF%D9%88%D8%B1%D8%A7%D9%86-%D8%AA%D8%AD%D8%B1%DB%8C%D9%85-%D9%87%D9%88%D8%B4%D9%85%D9%86%D8%AF%D8%A7%D9%86%D9%87-%D8%B9%D9%85%D9%84-%DA%A9%D8%B1%D8%AF",
    "network": 2,
    "summary": "مدیرعامل شرکت ملی نفت، عملکرد مدیریت امور بین\u200eالملل این شرکت را در دوران تحریم بسیار هوشمندانه خواند و گفت: امور بین الملل در دوران پس از تحریم\u200eها نیز می\u200cتواند نقش بزرگی در تسریع روند توسعه داشته باشد.",
    "title": "مدیریت فروش نفت در دوران تحریم هوشمندانه عمل کرد"
}
```


### Data Fields

- `id (string)`: ID of the news.
- `title (string)`: The title of the news.
- `article (string)`: The article of the news.
- `summary (string)`: The summary of the news.
- `category (int)`: The category of news in English (index of categories), including `Economy`, `Roads-Urban`, `Banking-Insurance`, `Agriculture`, `International`, `Oil-Energy`, `Industry`, `Transportation`, `Science-Technology`, `Local`, `Sports`, `Politics`, `Art-Culture`, `Society`, `Health`, `Research`, `Education-University`, `Tourism`.
- `categories (string)`: The category and sub-category of the news in Persian.
- `network (int)`: The news agency name (index of news agencies), including `Tahlilbazaar`, `Imna`, `Shana`, `Mehr`, `Irna`, `Khabaronline`.
- `link (string)`: The link of the news.

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

### Contributions

Thanks to [@m3hrdadfi](https://github.com/m3hrdadfi) for adding this dataset.