---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- ko
licenses:
- cc-by-nd-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|squad_kor_v1
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: null
---

# Dataset Card for KorQuAD v2.1

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

- [**Homepage**](https://korquad.github.io/)
- [**Repository**](https://github.com/korquad/korquad.github.io/tree/master/dataset)
- [**Paper**](https://korquad.github.io/dataset/KorQuAD_2.0/KorQuAD_2.0_paper.pdf)

### Dataset Summary

KorQuAD 2.0 is a Korean question and answering dataset consisting of a total of 100,000+ pairs. There are three major differences from KorQuAD 1.0, which is the standard Korean Q & A data. The first is that a given document is a whole Wikipedia page, not just one or two paragraphs. Second, because the document also contains tables and lists, it is necessary to understand the document structured with HTML tags. Finally, the answer can be a long text covering not only word or phrase units, but paragraphs, tables, and lists.

### Supported Tasks and Leaderboards

`question-answering`

### Languages

Korean

## Dataset Structure

Follows the standart SQuAD format. There is only 1 answer per question

### Data Instances

An example from the data set looks as follows:
```py
{'answer': {'answer_start': 3873,
  'html_answer_start': 16093,
  'text': '20,890 표'},
 'context': '<!DOCTYPE html>\n<html>\n<head>\n<meta>\n<title>심규언 - 위키백과, 우리 모두의 백과사전</title>\n\n\n<link>\n.....[omitted]',
 'id': '36615',
 'question': '심규언은 17대 지방 선거에서 몇 표를 득표하였는가?',
 'raw_html': '<!DOCTYPE html>\n<html c ...[omitted]',
 'title': '심규언',
 'url': 'https://ko.wikipedia.org/wiki/심규언'}
```

### Data Fields
```py
{'id': Value(dtype='string', id=None),
 'title': Value(dtype='string', id=None),
 'context': Value(dtype='string', id=None),
 'question': Value(dtype='string', id=None),
 'answer': {'text': Value(dtype='string', id=None),
  'answer_start': Value(dtype='int32', id=None),
  'html_answer_start': Value(dtype='int32', id=None)},
 'url': Value(dtype='string', id=None),
 'raw_html': Value(dtype='string', id=None)}
```
### Data Splits

- Train : 83486
- Validation:  10165

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

Wikipedia

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

[CC BY-ND 2.0 KR](https://creativecommons.org/licenses/by-nd/2.0/kr/deed.en)

### Citation Information
```
@article{NODE09353166,
    author={Youngmin Kim,Seungyoung Lim;Hyunjeong Lee;Soyoon Park;Myungji Kim},
    title={{KorQuAD 2.0: Korean QA Dataset for Web Document Machine Comprehension}},
    booltitle={{Journal of KIISE 제47권 제6호}},
    journal={{Journal of KIISE}},
    volume={{47}},
    issue={{6}},
    publisher={The Korean Institute of Information Scientists and Engineers},
    year={2020},
    ISSN={{2383-630X}},
    pages={577-586},
    url={http://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE09353166}}
```

### Contributions

Thanks to [@cceyda](https://github.com/cceyda) for adding this dataset.