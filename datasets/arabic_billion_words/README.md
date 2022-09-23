---
annotations_creators:
- found
language_creators:
- found
language:
- ar
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: null
pretty_name: Arabic Billion Words
configs:
- Alittihad
- Almasryalyoum
- Almustaqbal
- Alqabas
- Echoroukonline
- Ryiadh
- Sabanews
- SaudiYoum
- Techreen
- Youm7
dataset_info:
- config_name: Alittihad
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1601790302
    num_examples: 349342
  download_size: 348259999
  dataset_size: 1601790302
- config_name: Almasryalyoum
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1056197870
    num_examples: 291723
  download_size: 242604438
  dataset_size: 1056197870
- config_name: Almustaqbal
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1545659336
    num_examples: 446873
  download_size: 350826797
  dataset_size: 1545659336
- config_name: Alqabas
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 2631729746
    num_examples: 817274
  download_size: 595274646
  dataset_size: 2631729746
- config_name: Echoroukonline
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 464386206
    num_examples: 139732
  download_size: 108184378
  dataset_size: 464386206
- config_name: Ryiadh
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 3101294859
    num_examples: 858188
  download_size: 691264971
  dataset_size: 3101294859
- config_name: Sabanews
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 198019614
    num_examples: 92149
  download_size: 38214558
  dataset_size: 198019614
- config_name: SaudiYoum
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 2723291416
    num_examples: 888068
  download_size: 605537923
  dataset_size: 2723291416
- config_name: Techreen
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1103458209
    num_examples: 314597
  download_size: 252976781
  dataset_size: 1103458209
- config_name: Youm7
  features:
  - name: url
    dtype: string
  - name: head_line
    dtype: string
  - name: date
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 3004689464
    num_examples: 1172136
  download_size: 617708074
  dataset_size: 3004689464
---

# Dataset Card for Arabic Billion Words Corpus

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

- **Homepage:** http://www.abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus
- **Repository:**
- **Paper:** https://arxiv.org/pdf/1611.04033
- **Leaderboard:**
- **Point of Contact:**[Ibrahim Abu El-Khair](iabuelkhair@gmail.com)

### Dataset Summary

Abu El-Khair Corpus is an Arabic text corpus, that includes more than five million newspaper articles.
It contains over a billion and a half words in total, out of which, there are about three million unique words.
The corpus is encoded with two types of encoding, namely: UTF-8, and Windows CP-1256.
Also it was marked with two mark-up languages, namely: SGML, and XML.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Arabic

## Dataset Structure

### Data Instances

This is an example of the "Almasryalyoum" configuration subset:
```python
{
  "url": "http://today.almasryalyoum.com/printerfriendly.aspx?ArticleID=61300",
  "head_line": "رئيس وزراء المجر: عنصرية جماهير أوجبيست جلبت العار للبلاد",
  "date": "19/5/2007",
  "text": """قال متحدث باسم الحكومة المجرية: إن رئيس الوزراء فيرنك جيوركساني رحب بقرار اتحاد كرة القدم المجري بخصم ثلاث نقاط من نادي أوجبيست بسبب السلوك العنصري الذي صدر من جماهيره.
وعاقب الاتحاد المجري فريق أوجبيست بعد أن سخرت جماهيره من إبراهيم سيديبي مهاجم فريق ديبرينسين الأسود أثناء مباراة الفريقين أوائل مايو الجاري.
يذكر أن الاتحاد فرض أيضا غرامة مالية قدرها 20 ألف دولار علي أوجبيست في عام 2005 بعد أن رددت جماهيره شعارات معادية للسامية خلال مباراة بالدوري المجري.
وأوضح جيوركساني في خطاب إلي إيستفان كيستليكي رئيس الاتحاد المجري لكرة القدم، أن هذا السلوك العنصري من الجماهير «جلب العار لكرة القدم وللمجر». يذكر أن المجر بها مجموعة من مشجعي كرة القدم المشاغبين «الهوليجانز»، وشارك الكثير منهم في أعمال شغب معادية للحكومة في العام الماضي.""",
}
```

### Data Fields

The data fields are:
- "url": string, original url of the article,
- "head_line": string, headline of the article,
- "date": string, date of the article,
- "text": string, text content of the article,

### Data Splits

There is only one "training" split for all configuration subsets, containing the following number of examples:

|                | Number of examples |
|:---------------|-------------------:|
| Alittihad      |             349342 |
| Almasryalyoum  |             291723 |
| Almustaqbal    |             446873 |
| Alqabas        |             817274 |
| Echoroukonline |             139732 |
| Ryiadh         |             858188 |
| Sabanews       |              92149 |
| SaudiYoum      |             888068 |
| Techreen       |             314597 |
| Youm7          |            1172136 |

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@article{el20161,
  title={1.5 billion words arabic corpus},
  author={El-Khair, Ibrahim Abu},
  journal={arXiv preprint arXiv:1611.04033},
  year={2016}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) and [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.