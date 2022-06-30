---
pretty_name: SberQuAD
annotations_creators:
- crowdsourced
language_creators:
- found
- crowdsourced
language:
- ru
license:
- unknown
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
paperswithcode_id: sberquad
---


# Dataset Card for sberquad

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/sberbank-ai/data-science-journey-2017
- **Paper:** https://arxiv.org/abs/1912.09723
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Sber Question Answering Dataset (SberQuAD) is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.
Russian original analogue presented in Sberbank Data Science Journey 2017.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Russian

## Dataset Structure

### Data Instances
```
{
    "context": "Первые упоминания о строении человеческого тела встречаются в Древнем Египте...",
    "id": 14754,
    "qas": [
        {
            "id": 60544,
            "question": "Где встречаются первые упоминания о строении человеческого тела?",
            "answers": [{"answer_start": 60, "text": "в Древнем Египте"}],
        }
    ]
}
```

### Data Fields

- id: a int32 feature
- title: a string feature
- context: a string feature
- question: a string feature
- answers: a dictionary feature containing:
   - text: a string feature
   - answer_start: a int32 feature

### Data Splits

|   name   |train |validation|test |
|----------|-----:|---------:|-----|
|plain_text|45328 | 5036     |23936|

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

```
@article{DBLP:journals/corr/abs-1912-09723,
  author    = {Pavel Efimov and
               Leonid Boytsov and
               Pavel Braslavski},
  title     = {SberQuAD - Russian Reading Comprehension Dataset: Description and
               Analysis},
  journal   = {CoRR},
  volume    = {abs/1912.09723},
  year      = {2019},
  url       = {http://arxiv.org/abs/1912.09723},
  eprinttype = {arXiv},
  eprint    = {1912.09723},
  timestamp = {Fri, 03 Jan 2020 16:10:45 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1912-09723.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@alenusch](https://github.com/Alenush) for adding this dataset.
