---
annotations_creators:
- other
language:
- ar
- bg
- en
- es
- ro
language_creators:
- found
license:
- unknown
multilinguality:
- multilingual
pretty_name: "QA4MRE: Question Answering for Machine Reading Evaluation"
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- multiple-choice
task_ids:
- multiple-choice-qa
paperswithcode_id: null
---

# Dataset Card for "qa4mre"

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

- **Homepage:** http://nlp.uned.es/clef-qa/repository/qa4mre.php
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [QA4MRE 2011-2013: Overview of Question Answering for Machine Reading Evaluation](https://link.springer.com/chapter/10.1007/978-3-642-40802-1_29)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 5.24 MB
- **Size of the generated dataset:** 46.11 MB
- **Total amount of disk used:** 51.35 MB

### Dataset Summary

QA4MRE dataset was created for the CLEF 2011/2012/2013 shared tasks to promote research in
question answering and reading comprehension. The dataset contains a supporting
passage and a set of questions corresponding to the passage. Multiple options
for answers are provided for each question, of which only one is correct. The
training and test datasets are available for the main track.
Additional gold standard documents are available for two pilot studies: one on
alzheimers data, and the other on entrance exams data.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### 2011.main.DE

- **Size of downloaded dataset files:** 0.21 MB
- **Size of the generated dataset:** 1.67 MB
- **Total amount of disk used:** 1.88 MB

An example of 'train' looks as follows.
```

```

#### 2011.main.EN

- **Size of downloaded dataset files:** 0.19 MB
- **Size of the generated dataset:** 1.50 MB
- **Total amount of disk used:** 1.69 MB

An example of 'train' looks as follows.
```

```

#### 2011.main.ES

- **Size of downloaded dataset files:** 0.21 MB
- **Size of the generated dataset:** 1.62 MB
- **Total amount of disk used:** 1.82 MB

An example of 'train' looks as follows.
```

```

#### 2011.main.IT

- **Size of downloaded dataset files:** 0.20 MB
- **Size of the generated dataset:** 1.59 MB
- **Total amount of disk used:** 1.79 MB

An example of 'train' looks as follows.
```

```

#### 2011.main.RO

- **Size of downloaded dataset files:** 0.21 MB
- **Size of the generated dataset:** 1.66 MB
- **Total amount of disk used:** 1.87 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### 2011.main.DE
- `topic_id`: a `string` feature.
- `topic_name`: a `string` feature.
- `test_id`: a `string` feature.
- `document_id`: a `string` feature.
- `document_str`: a `string` feature.
- `question_id`: a `string` feature.
- `question_str`: a `string` feature.
- `answer_options`: a dictionary feature containing:
  - `answer_id`: a `string` feature.
  - `answer_str`: a `string` feature.
- `correct_answer_id`: a `string` feature.
- `correct_answer_str`: a `string` feature.

#### 2011.main.EN
- `topic_id`: a `string` feature.
- `topic_name`: a `string` feature.
- `test_id`: a `string` feature.
- `document_id`: a `string` feature.
- `document_str`: a `string` feature.
- `question_id`: a `string` feature.
- `question_str`: a `string` feature.
- `answer_options`: a dictionary feature containing:
  - `answer_id`: a `string` feature.
  - `answer_str`: a `string` feature.
- `correct_answer_id`: a `string` feature.
- `correct_answer_str`: a `string` feature.

#### 2011.main.ES
- `topic_id`: a `string` feature.
- `topic_name`: a `string` feature.
- `test_id`: a `string` feature.
- `document_id`: a `string` feature.
- `document_str`: a `string` feature.
- `question_id`: a `string` feature.
- `question_str`: a `string` feature.
- `answer_options`: a dictionary feature containing:
  - `answer_id`: a `string` feature.
  - `answer_str`: a `string` feature.
- `correct_answer_id`: a `string` feature.
- `correct_answer_str`: a `string` feature.

#### 2011.main.IT
- `topic_id`: a `string` feature.
- `topic_name`: a `string` feature.
- `test_id`: a `string` feature.
- `document_id`: a `string` feature.
- `document_str`: a `string` feature.
- `question_id`: a `string` feature.
- `question_str`: a `string` feature.
- `answer_options`: a dictionary feature containing:
  - `answer_id`: a `string` feature.
  - `answer_str`: a `string` feature.
- `correct_answer_id`: a `string` feature.
- `correct_answer_str`: a `string` feature.

#### 2011.main.RO
- `topic_id`: a `string` feature.
- `topic_name`: a `string` feature.
- `test_id`: a `string` feature.
- `document_id`: a `string` feature.
- `document_str`: a `string` feature.
- `question_id`: a `string` feature.
- `question_str`: a `string` feature.
- `answer_options`: a dictionary feature containing:
  - `answer_id`: a `string` feature.
  - `answer_str`: a `string` feature.
- `correct_answer_id`: a `string` feature.
- `correct_answer_str`: a `string` feature.

### Data Splits

|    name    |train|
|------------|----:|
|2011.main.DE|  120|
|2011.main.EN|  120|
|2011.main.ES|  120|
|2011.main.IT|  120|
|2011.main.RO|  120|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@InProceedings{10.1007/978-3-642-40802-1_29,
author="Pe{\~{n}}as, Anselmo
and Hovy, Eduard
and Forner, Pamela
and Rodrigo, {\'A}lvaro
and Sutcliffe, Richard
and Morante, Roser",
editor="Forner, Pamela
and M{\"u}ller, Henning
and Paredes, Roberto
and Rosso, Paolo
and Stein, Benno",
title="QA4MRE 2011-2013: Overview of Question Answering for Machine Reading Evaluation",
booktitle="Information Access Evaluation. Multilinguality, Multimodality, and Visualization",
year="2013",
publisher="Springer Berlin Heidelberg",
address="Berlin, Heidelberg",
pages="303--320",
isbn="978-3-642-40802-1"
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@albertvillanova](https://github.com/albertvillanova), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
