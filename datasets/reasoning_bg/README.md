---
annotations_creators:
- found
language_creators:
- found
languages:
- bg
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: null
---
# Dataset Card for reasoning_bg

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

- **Homepage:** https://github.com/mhardalov/bg-reason-BERT
- **Repository:** https://github.com/mhardalov/bg-reason-BERT
- **Paper:** [Beyond English-Only Reading Comprehension: Experiments in Zero-Shot Multilingual Transfer for Bulgarian](https://arxiv.org/abs/1908.01519)
- **Leaderboard:** [N/A]
- **Point of Contact:** [Momchil Hardalov](mailto:hardalov@fmi.uni-sofia.bg)

### Dataset Summary

Recently, reading comprehension models achieved near-human performance on large-scale datasets such as SQuAD, CoQA, MS Macro, RACE, etc. This is largely due to the release of pre-trained contextualized representations such as BERT and ELMo, which can be fine-tuned for the target task. Despite those advances and the creation of more challenging datasets, most of the work is still done for English. Here, we study the effectiveness of multilingual BERT fine-tuned on large-scale English datasets for reading comprehension (e.g., for RACE), and we apply it to Bulgarian multiple-choice reading comprehension. We propose a new dataset containing 2,221 questions from matriculation exams for twelfth grade in various subjects -history, biology, geography and philosophy-, and 412 additional questions from online quizzes in history. While the quiz authors gave no relevant context, we incorporate knowledge from Wikipedia, retrieving documents matching the combination of question + each answer option.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Bulgarian

## Dataset Structure

### Data Instances

A typical data point comprises of  question sentence and 4 possible choice answers and the correct answer.

```
          {
            "id": "21181dda96414fd9b7a5e336ad84b45d",
            "qid": 1,
            "question": "!0<>AB>OB5;=> AJI5AB2C20I8 6828 A8AB5<8 A0:",
            "answers": [
              "28@CA8B5",
              "BJ:0=8B5",
              "<8B>E>=4@88B5",
              "54=>:;5BJG=8B5 >@30=87<8"
            ],
            "correct": "54=>:;5BJG=8B5 >@30=87<8",
            "url": "http://zamatura.eu/files/dzi/biologiq/2010/matura-biologiq-2010.pdf"
          },
```

### Data Fields

- url : A string having the url from which the question has been sourced from
- id: A string question identifier for each example
- qid: An integer which shows the sequence of the question in that particular URL
- question: The title of the question
- answers: A list of each answers
- correct: The correct answer

### Data Splits

The dataset covers the following domains

| Domain | #QA-paris | #Choices | Len Question | Len Options | Vocab Size |
|:-------|:---------:|:--------:|:------------:|:-----------:|:----------:|
| **12th Grade Matriculation Exam** |
| Biology | 437 | 4 | 10.44 | 2.64 | 2,414 (12,922)|
| Philosophy | 630 | 4 | 8.91 | 2.94| 3,636  (20,392) |
| Geography | 612 | 4 | 12.83 | 2.47 | 3,239 (17,668) |
| History | 542 | 4 | 23.74 | 3.64 | 5,466 (20,456) |
| **Online History Quizzes** |
| Bulgarian History | 229 | 4 | 14.05 | 2.80 | 2,287 (10,620) |
| PzHistory | 183 | 3 | 38.89 | 2.44 | 1,261 (7,518) |
| **Total** | 2,633 | 3.93 | 15.67 | 2.89 | 13,329 (56,104) |


## Dataset Creation

### Curation Rationale

The dataset has been curated from matriculation exams and online quizzes. These questions cover a large variety of science topics in biology, philosophy, geography, and history.

### Source Data

#### Initial Data Collection and Normalization

Data has been sourced from the matriculation exams and online quizzes.

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]


### Contributions

Thanks to [@saradhix](https://github.com/saradhix) for adding this dataset.