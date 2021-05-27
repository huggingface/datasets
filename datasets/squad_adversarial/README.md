---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|squad
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: null
---

# Dataset Card for 'Adversarial Examples for SQuAD'

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

- [**Homepage**](https://worksheets.codalab.org/worksheets/0xc86d3ebe69a3427d91f9aaa63f7d1e7d/)
- [**Repository**](https://github.com/robinjia/adversarial-squad/)
- [**Paper**](https://www.aclweb.org/anthology/D17-1215/)

### Dataset Summary

Standard accuracy metrics indicate that reading comprehension systems are making rapid progress, but the extent to which these systems truly understand language remains unclear. To reward systems with real language understanding abilities, we propose an adversarial evaluation scheme for the Stanford Question Answering Dataset (SQuAD). Our method tests whether systems can answer questions about paragraphs that contain adversarially inserted sentences, which are automatically generated to distract computer systems without changing the correct answer or misleading humans.

### Supported Tasks and Leaderboards

`question-answering`, `adversarial attack`

### Languages

English

## Dataset Structure

Follows the standart SQuAD format.

### Data Instances

An example from the data set looks as follows:
```py
{'answers': {'answer_start': [334, 334, 334],
  'text': ['February 7, 2016', 'February 7', 'February 7, 2016']},
 'context': 'Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi\'s Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the "golden anniversary" with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as "Super Bowl L"), so that the logo could prominently feature the Arabic numerals 50. The Champ Bowl was played on August 18th,1991.',
 'id': '56bea9923aeaaa14008c91bb-high-conf-turk2',
 'question': 'What day was the Super Bowl played on?',
 'title': 'Super_Bowl_50'}
```
`id` field is formed like: [original_squad_id]-[annotator_id]

### Data Fields
```py
{'id': Value(dtype='string', id=None), # id of example (same as SQuAD) OR SQuAD-id-[annotator_id] for adversarially modified examples
 'title': Value(dtype='string', id=None), # title of document the context is from (same as SQuAD)
 'context': Value(dtype='string', id=None), # the context (same as SQuAD) +adversarially added sentence
 'question': Value(dtype='string', id=None), # the question (same as SQuAD)
 'answers': Sequence(feature={'text': Value(dtype='string', id=None), # the answer (same as SQuAD)
 'answer_start': Value(dtype='int32', id=None)}, length=-1, id=None) # the answer_start index (same as SQuAD)
 }
```
### Data Splits

- AddSent: Has up to five candidate adversarial sentences that don't answer the question, but have a lot of words in common with the question. This adversary is does not query the model in any way.
- AddOneSent: Similar to AddSent, but just one candidate sentences was picked at random. This adversary is does not query the model in any way.

Number of Q&A pairs
- AddSent : 3560
- AddOneSent:  1787

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

SQuAD dev set (+with adversarial sentences added)

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

[MIT License](https://github.com/robinjia/adversarial-squad/blob/master/LICENSE)

### Citation Information
```
@inproceedings{jia-liang-2017-adversarial,
    title = "Adversarial Examples for Evaluating Reading Comprehension Systems",
    author = "Jia, Robin  and
      Liang, Percy",
    booktitle = "Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D17-1215",
    doi = "10.18653/v1/D17-1215",
    pages = "2021--2031",
    abstract = "Standard accuracy metrics indicate that reading comprehension systems are making rapid progress, but the extent to which these systems truly understand language remains unclear. To reward systems with real language understanding abilities, we propose an adversarial evaluation scheme for the Stanford Question Answering Dataset (SQuAD). Our method tests whether systems can answer questions about paragraphs that contain adversarially inserted sentences, which are automatically generated to distract computer systems without changing the correct answer or misleading humans. In this adversarial setting, the accuracy of sixteen published models drops from an average of 75% F1 score to 36%; when the adversary is allowed to add ungrammatical sequences of words, average accuracy on four models decreases further to 7%. We hope our insights will motivate the development of new models that understand language more precisely.",
}
```

### Contributions

Thanks to [@cceyda](https://github.com/cceyda) for adding this dataset.