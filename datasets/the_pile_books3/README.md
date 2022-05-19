---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
pretty_name: Books3
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
---

# Dataset Card for the_pile_books3

## Table of Contents
- [Dataset Card for the_pile_books3](#dataset-card-for-the_pile_books3)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [|split|num examples|](#splitnum-examples)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** [GitHub](https://github.com/soskek/bookcorpus/issues/27#issuecomment-716104208)
- **Repository:** [Needs More Information]
- **Paper:** [arXiv](https://arxiv.org/abs/2101.00027)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This dataset is Shawn Presser's work and is part of EleutherAi/The Pile dataset. 

This dataset contains all of bibliotik in plain .txt form, aka 197,000 books processed in exactly  the same way as did for bookcorpusopen (a.k.a. books1). seems to be similar to OpenAI's mysterious  "books2" dataset referenced in their papers. Unfortunately OpenAI will not give details, so we know very little about any differences. People suspect it's "all of libgen", but it's purely conjecture.

|download_size|36.8 Gib|
|dataset_size|100.9 Gib|

### Supported Tasks and Leaderboards

This dataset is used for Language Modeling.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

```
{'title': '07 LEGO Ninjago - The Search For Zane (Scholastic) - Kate Howard (retail)'
'text': '\n\nTITLE PAGE\n\nFROM THE JOURNAL OF SENSEI GARMADON\n\nCHAPTER 1\n\nCHAPTER 2\n\nCHAPTER 3\n\nCHAPTER 4\n\nCHAPTER 5\n\nCHAPTER 6\n\nCHAPTER 7\n\nCHAPTER 8\n\nCHAPTER 9\n\nCOPYRIGHT\n\nThroughout Ninjago", five ninja are well-known for their speed, strength, and  of course  the elemental powers that help them protect our world from evil. But there are others who possess some of the same powers as the ninja. Others who may not always use their powers for good.\n\nBefore now, the ninja believed they were special. They di.......'}
```

### Data Fields

- `title`: title of the book
- `text`: text content of the book

### Data Splits

|split|num examples|
--------------------------------
|train|196640|

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

MIT

### Citation Information

```
@article{pile,
    title={The {P}ile: An 800GB Dataset of Diverse Text for Language Modeling},
    author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and Presser, Shawn and Leahy, Connor},
    journal={arXiv preprint arXiv:2101.00027},
    year={2020}
}
```

### Contributions

Thanks to [@shawwn](https://github.com/shawwn) for creating this dataset.
Thanks to [@richarddwang](https://github.com/richarddwang) for adding this dataset.
