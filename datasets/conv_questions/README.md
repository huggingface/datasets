---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en-US
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
- text-generation
- fill-mask
task_ids:
- open-domain-qa
- dialogue-modeling
pretty_name: ConvQuestions
---

# Dataset Card for ConvQuestions

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

- **Homepage:** [ConvQuestions page](https://convex.mpi-inf.mpg.de)
- **Repository:** [GitHub](https://github.com/PhilippChr/CONVEX)
- **Paper:** [Look before you hop: Conversational question answering over knowledge graphs using judicious context expansion](https://arxiv.org/abs/1910.03262)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Philipp Christmann](mailto:pchristm@mpi-inf.mpg.de)

### Dataset Summary

ConvQuestions is the first realistic benchmark for conversational question answering over
knowledge graphs. It contains 11,200 conversations which can be evaluated over Wikidata.
They are compiled from the inputs of 70 Master crowdworkers on Amazon Mechanical Turk,
with conversations from five domains: Books, Movies, Soccer, Music, and TV Series.
The questions feature a variety of complex question phenomena like comparisons, aggregations,
compositionality, and temporal reasoning. Answers are grounded in Wikidata entities to enable
fair comparison across diverse methods. The data gathering setup was kept as natural as
possible, with the annotators selecting entities of their choice from each of the five domains,
and formulating the entire conversation in one session. All questions in a conversation are
from the same Turker, who also provided gold answers to the questions. For suitability to knowledge
graphs, questions were constrained to be objective or factoid in nature, but no other restrictive
guidelines were set. A notable property of ConvQuestions is that several questions are not
answerable by Wikidata alone (as of September 2019), but the required facts can, for example,
be found in the open Web or in Wikipedia. For details, please refer to the CIKM 2019 full paper
(https://dl.acm.org/citation.cfm?id=3358016).

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

en

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
  'domain': 'music',
  'seed_entity': 'https://www.wikidata.org/wiki/Q223495',
  'seed_entity_text': 'The Carpenters', 
  'questions': [
    'When did The Carpenters sign with A&M Records?',
    'What song was their first hit?',
    'When did Karen die?',
    'Karen had what eating problem?',
    'and how did she die?'
  ],
  'answers': [
    [
      '1969'
    ],
    [
      'https://www.wikidata.org/wiki/Q928282'
    ],
    [
      '1983'
    ],
    [
      'https://www.wikidata.org/wiki/Q131749'
    ],
    [
      'https://www.wikidata.org/wiki/Q181754'
    ]
  ],
  'answer_texts': [
    '1969',
    '(They Long to Be) Close to You',
    '1983',
    'anorexia nervosa',
    'heart failure'
  ]
}
```

### Data Fields

- `domain`: a `string` feature. Any of: ['books', 'movies', 'music', 'soccer', 'tv_series']
- `seed_entity`: a `string` feature. Wikidata ID of the topic entity.
- `seed_entity_text`: a `string` feature. Surface form of the topic entity.
- `questions`: a `list` of `string` features. List of questions (initial question and follow-up questions).
- `answers`: a `list` of `lists` of `string` features. List of answers, given as Wikidata IDs or literals (e.g. timestamps or names).
- `answer_texts`: a `list` of `string` features. List of surface forms of the answers.

### Data Splits

|train|validation|tests|
|----:|---------:|----:|
| 6720|      2240| 2240|

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

With insights from a meticulous in-house pilot study with ten students over two weeks, the authors posed the conversation generation task on Amazon Mechanical Turk (AMT) in the most natural setup: Each crowdworker was asked to build a conversation by asking five sequential questions starting from any seed entity of his/her choice, as this is an intuitive mental model that humans may have when satisfying their real information needs via their search assistants.

#### Who are the annotators?

Local students (Saarland Informatics Campus) and AMT Master Workers.

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

The ConvQuestions benchmark is licensed under a Creative Commons Attribution 4.0 International License.

### Citation Information

```
@InProceedings{christmann2019look,
  title={Look before you hop: Conversational question answering over knowledge graphs using judicious context expansion},
  author={Christmann, Philipp and Saha Roy, Rishiraj and Abujabal, Abdalghani and Singh, Jyotsna and Weikum, Gerhard},
  booktitle={Proceedings of the 28th ACM International Conference on Information and Knowledge Management},
  pages={729--738},
  year={2019}
}
```

### Contributions

Thanks to [@PhilippChr](https://github.com/PhilippChr) for adding this dataset.
