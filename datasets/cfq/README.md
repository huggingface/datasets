---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Compositional Freebase Questions
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
- other
task_ids:
- open-domain-qa
- closed-domain-qa
- other-compositionality
paperswithcode_id: cfq
---

# Dataset Card for "cfq"

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

- **Homepage:** [https://github.com/google-research/google-research/tree/master/cfq](https://github.com/google-research/google-research/tree/master/cfq)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** https://arxiv.org/abs/1912.09713
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2041.62 MB
- **Size of the generated dataset:** 345.30 MB
- **Total amount of disk used:** 2386.92 MB

### Dataset Summary

The Compositional Freebase Questions (CFQ) is a dataset that is specifically designed to measure compositional
generalization. CFQ is a simple yet realistic, large dataset of natural language questions and answers that also
provides for each question a corresponding SPARQL query against the Freebase knowledge base. This means that CFQ can
also be used for semantic parsing.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

English (`en`).

## Dataset Structure

### Data Instances

#### mcd1

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 40.91 MB
- **Total amount of disk used:** 296.11 MB

An example of 'train' looks as follows.
```
{
  'query': 'SELECT count(*) WHERE {\n?x0 a ns:people.person .\n?x0 ns:influence.influence_node.influenced M1 .\n?x0 ns:influence.influence_node.influenced M2 .\n?x0 ns:people.person.spouse_s/ns:people.marriage.spouse|ns:fictional_universe.fictional_character.married_to/ns:fictional_universe.marriage_of_fictional_characters.spouses ?x1 .\n?x1 a ns:film.cinematographer .\nFILTER ( ?x0 != ?x1 )\n}',
  'question': 'Did a person marry a cinematographer , influence M1 , and influence M2'
}
```

#### mcd2

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 42.70 MB
- **Total amount of disk used:** 297.91 MB

An example of 'train' looks as follows.
```
{
  'query': 'SELECT count(*) WHERE {\n?x0 ns:people.person.parents|ns:fictional_universe.fictional_character.parents|ns:organization.organization.parent/ns:organization.organization_relationship.parent ?x1 .\n?x1 a ns:people.person .\nM1 ns:business.employer.employees/ns:business.employment_tenure.person ?x0 .\nM1 ns:business.employer.employees/ns:business.employment_tenure.person M2 .\nM1 ns:business.employer.employees/ns:business.employment_tenure.person M3 .\nM1 ns:business.employer.employees/ns:business.employment_tenure.person M4 .\nM5 ns:business.employer.employees/ns:business.employment_tenure.person ?x0 .\nM5 ns:business.employer.employees/ns:business.employment_tenure.person M2 .\nM5 ns:business.employer.employees/ns:business.employment_tenure.person M3 .\nM5 ns:business.employer.employees/ns:business.employment_tenure.person M4\n}',
  'question': "Did M1 and M5 employ M2 , M3 , and M4 and employ a person 's child"
}
```

#### mcd3

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 41.58 MB
- **Total amount of disk used:** 296.78 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### query_complexity_split

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 43.82 MB
- **Total amount of disk used:** 299.02 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### query_pattern_split

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 43.98 MB
- **Total amount of disk used:** 299.19 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

### Data Fields

The data fields are the same among all splits and configurations:
- `question`: a `string` feature.
- `query`: a `string` feature.

### Data Splits

| name                      |  train |  test |
|---------------------------|-------:|------:|
| mcd1                      |  95743 | 11968 |
| mcd2                      |  95743 | 11968 |
| mcd3                      |  95743 | 11968 |
| query_complexity_split    | 100654 |  9512 |
| query_pattern_split       |  94600 | 12589 |
| question_complexity_split |  98999 | 10340 |
| question_pattern_split    |  95654 | 11909 |
| random_split              |  95744 | 11967 |

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

@inproceedings{Keysers2020,
  title={Measuring Compositional Generalization: A Comprehensive Method on
         Realistic Data},
  author={Daniel Keysers and Nathanael Sch"{a}rli and Nathan Scales and
          Hylke Buisman and Daniel Furrer and Sergii Kashubin and
          Nikola Momchev and Danila Sinopalnikov and Lukasz Stafiniak and
          Tibor Tihon and Dmitry Tsarkov and Xiao Wang and Marc van Zee and
          Olivier Bousquet},
  booktitle={ICLR},
  year={2020},
  url={https://arxiv.org/abs/1912.09713.pdf},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@brainshawn](https://github.com/brainshawn) for adding this dataset.
