---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ur
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
- text-scoring
task_ids:
- semantic-similarity-scoring
- topic-classification
paperswithcode_id: counter
pretty_name: COUNTER
---

# Dataset Card for COUNTER

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

- **Homepage:** http://ucrel.lancs.ac.uk/textreuse/counter.php
- **Repository:** [More Information Needed]
- **Paper:** https://link.springer.com/article/10.1007%2Fs10579-016-9367-2
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [UCREL](ucrel@lancaster.ac.uk)

### Dataset Summary

The COrpus ofUrdu News TExt Reuse (COUNTER) corpus contains 1200 documents with realexamples of text reuse from the field of journalism. It has been manually annotatedat document level with three levels of reuse: wholly derived, partially derived andnon derived

### Supported Tasks and Leaderboards

other:text-reuse

### Languages

ur

## Dataset Structure

### Data Instances

Here is one example from the dataset:

```
{"derived": {
"body" :"میر پور(وقت نیوز) بنگلہ دیش نے 5 میچوں کی سیریز کےآ خری میچ میں بھی فتح حاصل کر کے سیریز میں وائٹ واش کر دیا،زمبابوے ایک میچ بھی نہ جیت سکا۔آخری میچ میں زمبابوے کے 129 رنز کا ہدف بنگال ٹائیگرز نے 24.3 اوورز میں 5 وکٹوں کے نقصان پر حاصل کر لیا۔بنگلہ دیش کے شیر بنگلہ سٹیڈیم میر پور میں کھیلے گئے آخری ایک روزہ میچ میں زمبابوے کے کپتان چکمبورا نے ٹاس جیت کے بینٹگ کا فیصلہ کیا جو ان کی ٹیم کیلئے ڈراؤنا خواب ثابت ہوا اور پوری ٹیم 30 اوورز میں 128 رنز بنا کر پویلین لوٹ گئی زمبابوے کی پہلی وکٹ 16 رنز پر گری جب سکندر رضا صرف 9 رنز بنا کر مشرقی مرتضی کی بال پر آؤٹ ہوئے اس کے بعد مساکد ازااور سباندا کی پارٹنرشپنے ٹیم کا سکور95 رنز تک پہنچا دیا ۔مساکدازا 52 رنز بنا کر جبیر الحسن کا شکار بنے جبکہ سباندا نے 37 رنز کی اننگز کھیلی اس کے بعد کئی بھی زمبابوے کا کھلاڑی جم کر نہ کھیل سکا۔بنگال ٹائیگرز کی جانب سے عمدہ باؤلنگ کے نتیجے میں کپتان چکمبورا سمیت 8 کھلاڑی ڈبل فیگر کراس نہ کر سکے ۔بنگلہ دیش کی جانب سے ایک روزہ میچوں میں ڈیبیو کرنے والے تیج السلام نے اپنے پہلے ہی میچ میں ہیٹرک کی اسلام نے 7 اوورز میں صرف 14 رنز دئے اور چار کھلاڑیوں کع آؤٹ کیا جبکہ شکیب الحسن نے 30 رنز دیکر 3 اور جبیر الحسن نے41 رنز دیکر2 کھلاڑیوں کو پویلین کی راہ دکھائی ۔ 128 رنز کے جواب میں بنگال ٹائیگرز نے بیٹنگ شروع کی مشکلات کا سامنا رہا ان کے بھی ابتدائی 3 کھلاڑی 47 رنز پر پویلین لوٹ گئے۔ تمیم اقبال 10، انعام الحق8 رنز بنا کر آؤٹ ہوئے،آل راؤنڈر شکیب الحسن بغیر کوئی رنز بنائیپویلین لوٹ گئے وکٹ کیپر مشفق الرحیم صرف 11 رنز بنا کر چتارہ کا شکار بن گئے۔محمد اللہ نے51 رنز کی میچ وننگ اننگز کھیلی جبکہ صابر رحمٰن13 رنز بنا کر ناٹ آؤٹ رہے۔ زمبابوے کی جانب سے چتارہ نے 3 اور پنیا نگارا نے 2 کھلاڑیوں کو آؤٹ کیا ۔فتح کے ساتھ بنگلہ دیش نے سیریز میں وائٹ واش کر دیا۔زمبابوے کی ٹیم کوئی میچ نہ جیت سکی،تیج السلام کو میچ کا بہترین ایوارڈ دیا گیا جبکہ سیریز کا بہترین کھلاڑی مشفق الرحیم کو قرار دیا گیا۔",
"classification": 1,  # partially_derived
"domain": 1,  # sports
"filename": "0001p.xml",
"headline": "بنگلہ دیش کا زمبابوے کا ون ڈے سیریز میں 5-0 سے وائٹ واش",
 "newsdate": "02.12.14",
"newspaper": "daily_waqt",
"number_of_words_with_swr": 265,
"total_number_of_sentences": 13,
"total_number_of_words": 393},
"source": {
"body": "ڈھاکہ ۔ یکم دسمبر (اے پی پی) بنگلہ دیش نے زمبابوے کو ٹیسٹ کے بعد ون ڈے سیریز میں بھی وائٹ واش کر دیا۔ سیریز کے پانچویں اور آخری ون ڈے میچ میں بنگال ٹائیگرز نے زمبابوے کو 5 وکٹوں سے شکست دے دی، مہمان ٹیم پہلے بیٹنگ کرتے ہوئے 128 رنز پر ڈھیر ہوگئی۔ تیج الاسلام نے کیریئر کے پہلے ون ڈے میچ میں ہیٹ ٹرک کرکے نئی تاریخ رقم کر دی، انہوں نے 4 کھلاڑیوں کو آؤٹ کیا۔ جواب میں بنگلہ دیش نے ہدف 24.3 اوورز میں 5 وکٹوں کے نقصان پر حاصل کر لیا۔ محمد اللہ نے 51 رنز کی ناقابل شکست اننگز کھیلی۔ تفصیلات کے مطابق پیر کو شیر بنگلہ نیشنل سٹیڈیم، میرپور میں پانچویں اور آخری ون ڈے میچ میں زمبابوے کے کپتان ایلٹن چگمبورا نے ٹاس جیت کر پہلے بیٹنگ کا فیصلہ کیا جو غلط ثابت ہوا۔ زمبابوے کی پوری ٹیم ڈیبیو ون ڈے کھیلنے والے نوجوان لیفٹ آرم سپنر تیج الاسلام اور شکیب الحسن کی تباہ کن باؤلنگ کے باعث 30 اوورز میں 128 رنز پر ڈھیر ہوگئی۔ ہیملٹن ماساکڈزا 52 اور ووسی سبانڈا 37 رنز کے ساتھ نمایاں رہے، ان کے علاوہ کوئی بھی بلے باز دوہرا ہندسہ عبور نہ کر سکا۔ اپنا پہلا ون ڈے کھیلنے والے تیج الاسلام نے 11 رنز کے عوض 4 وکٹیں حاصل کیں جس میں شاندار ہیٹ ٹرک بھی شامل ہے، اس طرح وہ ڈیبیو میں ہیٹ ٹرک کرنے والے دنیا کے پہلے باؤلر بن گئے ہیں۔ شکیب الحسن نے تین اور زبیر حسین نے دو وکٹیں حاصل کیں۔ جواب میں بنگلہ دیش نے ہدف 24.3 اوورز میں 5 وکٹوں کے نقصان پر حاصل کر لیا۔ محمد اللہ نے 51 رنز کی ناقابل شکست اننگز کھیل کر ٹیم کی فتح میں اہم کردار ادا کیا۔ زمبابوے کی جانب سے ٹینڈائی چتارا نے تین اور تناشے پینگارا نے دو وکٹیں حاصل کیں۔",
"classification": 1,  # partially_derived
"domain": 1,  # sports
"filename": "0001.xml",
"headline": "بنگال ٹائیگرز نے کمزور زمبابوے کو ٹیسٹ کے بعد ون ڈے سیریز میں بھی وائٹ واش کر دیا، پانچویں اور آخری ون ڈے میچ میں بنگلہ دیش 5 وکٹوں سے فتح یاب، تیج الاسلام نے ڈیبیو ون ڈے میں ہیٹ ٹرک کرکے نئی تاریخ رقم کر دی"
"newsdate": "01.12.14",
"newspaper": "APP",
"number_of_words_with_swr": 245,
"total_number_of_sentences": 15,
"total_number_of_words": 352}}
```
### Data Fields

```source```: The source document

```derived```: The derived document
For each pair of source and derived documents. we have the following fields:

```filename (str)```: Name of the file in dataset

```headline(str)```: Headline of the news item

```body(str)```: Main text of the news item

```total_number_of_words(int)```: Number of words in document

```total_number_of_sentences(int)```: Number of sentences in document

```number_of_words_with_swr(int)```: Number of words after stop word removal

```newspaper(str)```: The newspaper in which the news item was published

```newsdate(str)```: The date on which the news item is published DD.MM.YY

```domain(int)```: The category of news item from this list: "business", "sports", "national", "foreign", "showbiz".

```classification (int)```: Three classes of reuse from this list: Wholly Derived (WD), Partially Derived (PD) and Non Derived (ND)

### Data Splits

One split train with 600 pairs of documents.

The corpus is composed of two main document types: (1) source documents and (2) derived documents. There are total 1200 documents in the corpus: 600 are newsagency articles (source documents) and 600 are newspapers stories (derived documents). The corpus contains in total 275,387 words (tokens8), 21,426 unique words and 10,841 sentences. The average length of a source document is 227 words while for derived documents it is 254 words.

## Dataset Creation

### Curation Rationale

Our main intention was to develop a standard benchmark resource for the evaluation of existing systems available for text reuse detection in general and specifically for Urdu language. To generate a corpus with realistic examples, we opted for the field of journalism. In journalism, the same news story is published in different newspapers in different forms. It is a standard practice followed by all the newspapers (reporters and editors) to reuse (verbatim or modified) a news story released by the news agency.

### Source Data

#### Initial Data Collection and Normalization

The COUNTER corpus consists of news articles (source documents) released by five news agencies in Pakistan i.e. Associated Press of Pakistan (APP), InternationalNews Network (INN), Independent News Pakistan (INP), News Network International (NNI) and South Asian News Agency (SANA). The corresponding news stories (derived documents) were extracted from nine daily published and large circulation national news papers of the All Pakistan Newspapers Society (APNS), who are subscribed to these news agencies.
These include Nawa-e-Waqt, Daily Dunya, Express, Jang, Daily Waqt, Daily Insaf, Daily Aaj, Daily Islam and DailyPakistan. All of them are part of the mainstream national press, long established dailies with total circulation figures of over four million.7News agency texts (source documents) were provided (in electronic form) by the news agencies on a daily basis when they released the news. Newspaper stories (derived documents) were collected by three volunteers over a period of six months (from July to December 2014).National, Foreign, Business, Sports and Showbiz were the domains targeted for data collection.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The corpus has been annotated at the document level with three classes of reuse i.e.Wholly Derived (WD), Partially Derived (PD) and Non Derived (ND).
The derived collection contains documents with various degrees of text reuse. Some of the newspaper stories (derived documents)are rewritten (either verbatim or paraphrased) from the new agencys text (source document) while others have been written by the journalists independently on their own. For the former case, source-derived document pairs are either tagged as Wholly Derived (WD) or Partially Derived (PD) depending on the volume of text reused from the news agencys text for creating the newspaper article while for the latter case, they are tagged as Non Derived (ND) as the journalists have not reused anything from the news agencys text but based on their own observations and findings, developed and documented the story.

The annotations were carried out in three phases: (1) training phase, (2) annotations, (3)conflict resolving. During the training phase, annotators A and B manually annotated 60 document pairs, following a preliminary version of the annotation guidelines. A detailed meeting was carried out afterwards, discussing the problems and disagreements. It was observed that the highest number of disagreements were between PD and ND cases, as both found it difficult to distinguish between these two classes. The reason being that adjusting the threshold where a text is heavily paraphrased or new information added to it that it becomes independently written(ND). Following the discussion, the annotation guidelines were slightly revised, and the first 60 annotations results were saved. In the annotation phase, the remaining540 document pairs were manually examined by the two annotators (A and B). Both were asked to judge, and classify (at document level) whether a document(newspaper story) depending on the volume of text rewritten from the source (news agency article) falls into one of the following categories:remaining540 document pairs were manually examined by the two annotators (A and B). Both were asked to judge, and classify (at document level) whether a document(newspaper story) depending on the volume of text rewritten from the source (news agency article) falls into one of the following categories:
Wholly Derived (WD)The News agency text is the only source for the reused newspaper text, which means it is a verbatim copy of the source. In this case, most of the reused text is word-to-word copy of the source text.Partially Derived (PD)The Newspaper text has been either derived from more than one news agency or most of the text is paraphrased by the editor when rewriting from news agency text source. In this case, most parts of the derived document contain paraphrased text or new facts and figures added by the journalists own findings. Non Derived (ND)The News agency text has not been used in the production of the newspaper text (though words may still co-occur in both documents), it has completely different facts and figures or is heavily paraphrased from the newsagencys copy. In this case, the derived document is independently written and has a lot more new text.

#### Who are the annotators?

The annotations were performed by three annotators (A, B and C), who were native Urdu language speakers and experts of paraphrasing mechanisms. All three were graduates, experienced in text annotations and having an advanced Urdu level.

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

[More Information Needed]

### Licensing Information

This dataset is licensed under the Creative Common Attribution-NonCommercial-ShareAlike 4.0 International License.
[(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Citation Information

```
@Article{Sharjeel2016,
author="Sharjeel, Muhammad
and Nawab, Rao Muhammad Adeel
and Rayson, Paul",
title="COUNTER: corpus of Urdu news text reuse",
journal="Language Resources and Evaluation",
year="2016",
pages="1--27",
issn="1574-0218",
doi="10.1007/s10579-016-9367-2",
url="http://dx.doi.org/10.1007/s10579-016-9367-2"
}
```

### Contributions

Thanks to [@arkhalid](https://github.com/arkhalid) for adding this dataset.