---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- th
license:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-iapp-wiki-qa-dataset
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
paperswithcode_id: null
pretty_name: IappWikiQaSquad
---

# Dataset Card for `iapp_wiki_qa_squad`

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

- **Homepage:** https://github.com/iapp-technology/iapp-wiki-qa-dataset
- **Repository:** https://github.com/iapp-technology/iapp-wiki-qa-dataset
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/iapp-technology/iapp-wiki-qa-dataset

### Dataset Summary

`iapp_wiki_qa_squad` is an extractive question answering dataset from Thai Wikipedia articles. It is adapted from [the original iapp-wiki-qa-dataset](https://github.com/iapp-technology/iapp-wiki-qa-dataset) to [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format, resulting in 5761/742/739 questions from 1529/191/192 articles.

### Supported Tasks and Leaderboards

extractive question answering

### Languages

Thai

## Dataset Structure

### Data Instances

An example from the dataset:
```
{'article_id': '0U2lA8nJQESIxbZrjZQc',
'question_id': '0U2lA8nJQESIxbZrjZQc_000',
'context': 'นายสุวัฒน์ วรรณศิริกุล (1 พฤศจิกายน พ.ศ. 2476 - 31 กรกฎาคม พ.ศ. 2555) อดีตรองหัวหน้าพรรคพลังประชาชน อดีตประธานสมาชิกสภาผู้แทนราษฎร และประธานภาคกรุงเทพมหานคร พรรคพลังประชาชน อดีตสมาชิกสภาผู้แทนราษฎรกรุงเทพมหานครหลายสมัย ได้รับการเลือกตั้งเป็นสมาชิกสภาผู้แทนราษฎรครั้งแรกในปี พ.ศ. 2529 ในสังกัดพรรคประชากรไทย และสังกัดพรรคพลังประชาชน เป็นพรรคสุดท้าย',
'question': 'สุวัฒน์ วรรณศิริกุล เกิดวันที่เท่าไร',
'answers': {'text': ['1 พฤศจิกายน พ.ศ. 2476'],
 'answer_start': [24],
 'answer_end': [45]},
'title': 'สุวัฒน์ วรรณศิริกุล',
'created_by': 'gmnjGRF0y0g7QRZDd9Qgz3AgiHJ3',
'created_on': '2019-08-18 05:05:51.358000+00:00',
'is_pay': {'date': None, 'status': False}}
{'article_id': '01KZTrxgvC5mOovXFMPJ',
'question_id': '01KZTrxgvC5mOovXFMPJ_000',
'context': 'พัทธ์ธีรา ศรุติพงศ์โภคิน (เกิด 3 ธันวาคม พ.ศ. 2533) หรือชื่อเล่นว่า อร เป็นนักแสดงหญิงชาวไทย สำเร็จมัธยมศึกษาจากCatholic Cathedral College ประเทศนิวซีแลนด์ และปริญญาตรีจากRaffles International College สาขา Business Marketing\n\nเข้าสู่วงการตั้งแต่อายุ 6 ขวบ จากการแสดงละครเวทีกับ ครูชลประคัลภ์ จันทร์เรือง จากนั้นก็เล่นโฆษณาในวัยเด็ก 2- 3 ชิ้น และยังเคยแสดงช่วงละครสั้น ในรายการซุปเปอร์จิ๋ว ประมาณปี 2542\n\nปัจจุบันเป็นทั้ง นักแสดง , พิธีกร และ วีเจ อยู่ที่คลื่น เก็ท 102.5 Bangkok International Hits Music Station และยังเป็นพิธีกรให้กับช่อง ทรู มิวสิก',
'question': 'พัทธ์ธีรา ศรุติพงศ์โภคิน เกิดวันที่เท่าไร',
'answers': {'text': ['3 ธันวาคม พ.ศ. 2533'],
 'answer_start': [31],
 'answer_end': [50]},
'title': 'พัทธ์ธีรา ศรุติพงศ์โภคิน',
'created_by': 'gmnjGRF0y0g7QRZDd9Qgz3AgiHJ3',
'created_on': '2019-08-07 14:00:38.778000+00:00',
'is_pay': {'status': True,
 'total': 2.5,
 'date': '2019-08-13 10:47:28.095000+00:00'}}
```

### Data Fields

```
{
    "question_id": question id
    "article_id": article id
    "title": article title
    "context": article texts
    "question": question
    "answers":
        {
            "text": answer text
            "answer_start": answer beginning position
            "answer_end": answer exclusive upper bound position
        }
    ),
}
```

### Data Splits

|             | train | valid | test |
|-------------|-------|-------|------|
| # questions | 5761  | 742   | 739  |
| # articles  | 1529  | 191   | 192  |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

From the original `iapp-wiki-qa-dataset`, [@cstorm125](https://github.com/cstorm125/) applied the following processing:

- Select questions with one, non-empty answer
- Select questions whose answers match `textDetection` fields
- Select questions whose answers are 100-character long or shorter
- 80/10/10 train-validation-split at article level

#### Who are the source language producers?

Wikipedia authors for contexts and annotators hired by [iApp](https://iapp.co.th/) for questions and answer annotations

### Annotations

#### Annotation process

Annotators hired by [iApp](https://iapp.co.th/) are asked create questions and answers for each article.

#### Who are the annotators?

Annotators hired by [iApp](https://iapp.co.th/)

### Personal and Sensitive Information

All contents are from Wikipedia. No personal and sensitive information is expected to be included.

## Considerations for Using the Data

### Social Impact of Dataset

- open-domain, extractive question answering in Thai

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Original dataset by [iApp](https://iapp.co.th/). SQuAD formattting by [PyThaiNLP](https://github.com/PyThaiNLP/).

### Licensing Information

MIT

### Citation Information

```
@dataset{kobkrit_viriyayudhakorn_2021_4539916,
  author       = {Kobkrit Viriyayudhakorn and
                  Charin Polpanumas},
  title        = {iapp\_wiki\_qa\_squad},
  month        = feb,
  year         = 2021,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.4539916},
  url          = {https://doi.org/10.5281/zenodo.4539916}
}
```

### Contributions

Thanks to [@cstorm125](https://github.com/cstorm125) for adding this dataset.
