---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
- extractive-qa
paperswithcode_id: covidqa
---


# Dataset Card for [covid_qa_castorini]

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

- **Homepage:** https://covidqa.ai
- **Repository:** https://github.com/castorini/pygaggle
- **Paper:** https://arxiv.org/abs/2004.11339
- **Point of Contact:** [Castorini research group @UWaterloo](https://github.com/castorini/)

### Dataset Summary

CovidQA is a question answering dataset specifically designed for COVID-19, built by hand from knowledge gathered 
from Kaggle’s COVID-19 Open Research Dataset Challenge.
The dataset comprises 156 question-article pairs with 27 questions (topics) and 85 unique articles.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

**What do the instances that comprise the dataset represent?**
Each represents a question, a context (document passage from the CORD19 dataset) and an answer.

**How many instances are there in total?**

**What data does each instance consist of?**
Each instance is a query (natural language question and keyword-based), a set of answers, and a document id with its title associated with each answer.

[More Information Needed]

### Data Fields

The data was annotated in SQuAD style fashion, where each row contains:

* **question_query**: Natural language question query
* **keyword_query**: Keyword-based query
* **category_name**: Category in which the queries are part of
* **answers**: List of answers
  * **id**: The document ID the answer is found on
  * **title**: Title of the document of the answer
  * **exact_answer**: Text (string) of the exact answer

### Data Splits

**data/kaggle-lit-review-0.2.json**: 156 question-article pairs with 27 questions (topics) and 85 unique articles from
CORD-19.

[More Information Needed]

## Dataset Creation

The dataset aims to help for guiding research until more substantial evaluation resources become available. Being a smaller dataset,
it can be helpful for evaluating the zero-shot or transfer capabilities of existing models on topics specifically related to COVID-19.

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

[More Information Needed]

### Annotations

Five of the co-authors participated in this annotation effort, applying the aforementioned approach, with one lead 
annotator responsible for approving topics and answering technical questions from the other annotators. Two annotators are
undergraduate students majoring in computer science, one is a science alumna, another is a computer science professor, 
and the lead annotator is a graduate student in computer science—all affiliated with the University of Waterloo.

#### Annotation process

#### Who are the annotators?

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The dataset was intended as a stopgap measure for guiding research until more substantial evaluation resources become available.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

While this dataset, comprising 124 question–article pairs as of the present version 0.1 release, does not have sufficient
examples for supervised machine learning, it can be helpful for evaluating the zero-shot or transfer capabilities
of existing models on topics specifically related to COVID-19.

## Additional Information

The listed authors in the homepage are maintaining/supporting the dataset. 

### Dataset Curators

[More Information Needed]

The covidqa dataset is licensed under 
the [Apache License 2.0](https://github.com/castorini/pygaggle/blob/master/LICENSE)

[More Information Needed]

### Citation Information

```
@article{tang2020rapidly,
  title={Rapidly Bootstrapping a Question Answering Dataset for COVID-19},
  author={Tang, Raphael and Nogueira, Rodrigo and Zhang, Edwin and Gupta, Nikhil and Cam, Phuong and Cho, Kyunghyun and Lin, Jimmy},
  journal={arXiv preprint arXiv:2004.11339},
  year={2020}
}
```

### Contributions

Thanks to [@olinguyen](https://github.com/olinguyen) for adding this dataset.