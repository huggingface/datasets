---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- ar
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: wikiqaar
pretty_name: English-Arabic Wikipedia Question-Answering
dataset_info:
  features:
  - name: question_id
    dtype: string
  - name: question
    dtype: string
  - name: document_id
    dtype: string
  - name: answer_id
    dtype: string
  - name: answer
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
  config_name: plain_text
  splits:
  - name: test
    num_bytes: 7563127
    num_examples: 20632
  - name: train
    num_bytes: 26009979
    num_examples: 70264
  - name: validation
    num_bytes: 3740721
    num_examples: 10387
  download_size: 35226436
  dataset_size: 37313827
---

# Dataset Card for WikiQAar

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [WikiQaAr](https://github.com/qcri/WikiQAar)
- **Repository:** [WikiQaAr](https://github.com/qcri/WikiQAar)
- **Paper:** 
- **Point of Contact:** [Ines Abbes
](abbes.ines@yahoo.com)

### Dataset Summary

Arabic Version of WikiQA by automatic automatic machine translators 
and crowdsourced the selection of the best one to be incorporated into the corpus

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

Each data point contains the question and whether the answer is a valid or not.  

### Data Fields

- `question_id`: the question id.
- `question`: the question text.
- `document_id`: the wikipedia document id.
- `answer_id` : the answer id.
- `answer` : a candidate answer to the question. 
- `label` : 1 if the `answer` is correct or 0 otherwise. 

### Data Splits

The dataset is not split. 

|            |  train | validation |   test |
|------------|-------:|-----------:|-------:|
| Data split | 70,264 |     20,632 | 10,387 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

Translation of WikiQA. 

#### Who are the source language producers?

Translation of WikiQA.   

### Annotations

The dataset does not contain any additional annotations.

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
@InProceedings{YangYihMeek:EMNLP2015:WikiQA,
       author = {{Yi}, Yang and {Wen-tau},  Yih and {Christopher} Meek},
        title = "{WikiQA: A Challenge Dataset for Open-Domain Question Answering}",
      journal = {Association for Computational Linguistics},
         year = 2015,
          doi = {10.18653/v1/D15-1237},
        pages = {2013–2018},
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.