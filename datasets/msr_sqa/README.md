---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- ms-pl
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: null
---

# Dataset Card for Microsoft Research Sequential Question Answering

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

- **Homepage:[Microsoft Research Sequential Question Answering (SQA) Dataset](https://msropendata.com/datasets/b25190ed-0f59-47b1-9211-5962858142c2)**
- **Repository:**
- **Paper:[https://www.microsoft.com/en-us/research/wp-content/uploads/2017/05/acl17-dynsp.pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/05/acl17-dynsp.pdf)**
- **Leaderboard:**
- **Point of Contact:**
  - Scott Wen-tau Yih        scottyih@microsoft.com
  - Mohit Iyyer              m.iyyer@gmail.com
  - Ming-Wei Chang           minchang@microsoft.com

### Dataset Summary

Recent work in semantic parsing for question answering has focused on long and complicated questions, many of which would seem unnatural if asked in a normal conversation between two humans. In an effort to explore a conversational QA setting, we present a more realistic task: answering sequences of simple but inter-related questions.

We created SQA by asking crowdsourced workers to decompose 2,022 questions from WikiTableQuestions (WTQ)*, which contains highly-compositional questions about tables from Wikipedia. We had three workers decompose each WTQ question, resulting in a dataset of 6,066 sequences that contain 17,553 questions in total. Each question is also associated with answers in the form of cell locations in the tables.

- Panupong Pasupat, Percy Liang. "Compositional Semantic Parsing on Semi-Structured Tables" ACL-2015.
  [http://www-nlp.stanford.edu/software/sempre/wikitable/](http://www-nlp.stanford.edu/software/sempre/wikitable/)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- `id` (`str`): question sequence id (the id is consistent with those in WTQ)
- `annotator` (`int`): `0`, `1`, `2` (the 3 annotators who annotated the question intent)
- `position` (`int`): the position of the question in the sequence
- `question` (`str`): the question given by the annotator
- `table_file` (`str`): the associated table
- `table_header` (`List[str]`): a list of headers in the table
- `table_data` (`List[List[str]]`): 2d array of data in the table
- `answer_coordinates` (`List[Dict]`): the table cell coordinates of the answers (0-based, where 0 is the first row after the table header)
  - `row_index`
  - `column_index`
- `answer_text` (`List[str]`): the content of the answer cells

Note that some text fields may contain Tab or LF characters and thus start with quotes.
It is recommended to use a CSV parser like the Python CSV package to process the data.

### Data Splits

[More Information Needed]

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

[More Information Needed]

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.