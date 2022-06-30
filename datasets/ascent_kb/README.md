---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-knowledge-base
paperswithcode_id: ascentkb
pretty_name: Ascent KB
---

# Dataset Card for Ascent KB

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

- **Homepage:** https://ascent.mpi-inf.mpg.de/
- **Repository:** https://github.com/phongnt570/ascent
- **Paper:** https://arxiv.org/abs/2011.00905
- **Point of Contact:** http://tuan-phong.com

### Dataset Summary

This dataset contains 8.9M commonsense assertions extracted  by the Ascent pipeline developed at the [Max Planck Institute for Informatics](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/).
The focus of this dataset is on everyday concepts such as *elephant*, *car*, *laptop*, etc.
The current version of Ascent KB (v1.0.0) is approximately **19 times larger  than ConceptNet** (note that, in this comparison, non-commonsense knowledge in ConceptNet such as lexical relations is excluded).

For more details, take a look at
[the research paper](https://arxiv.org/abs/2011.00905) and
[the website](https://ascent.mpi-inf.mpg.de).

### Supported Tasks and Leaderboards

The dataset can be used in a wide range of downstream tasks such as commonsense question answering or dialogue systems.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances
There are two configurations available for this dataset:
1. `canonical` (default): This part contains `<arg1 ; rel ; arg2>`
  assertions where the relations (`rel`) were mapped to 
  [ConceptNet relations](https://github.com/commonsense/conceptnet5/wiki/Relations)
  with slight modifications:
    - Introducing 2 new relations: `/r/HasSubgroup`, `/r/HasAspect`.
    - All `/r/HasA` relations were replaced with `/r/HasAspect`. 
      This is motivated by the [ATOMIC-2020](https://allenai.org/data/atomic-2020)
      schema, although they grouped all `/r/HasA` and
      `/r/HasProperty` into `/r/HasProperty`.
    - The `/r/UsedFor` relation was replaced with `/r/ObjectUse`
      which is broader (could be either _"used for"_, _"used in"_, or _"used as"_, ect.).
      This is also taken from ATOMIC-2020.
2. `open`: This part contains open assertions of the form
  `<subject ; predicate ; object>` extracted directly from web
  contents. This is the original form of the `canonical` triples. 

In both configurations, each assertion is equipped with 
extra information including: a set of semantic `facets`
(e.g., *LOCATION*, *TEMPORAL*, etc.), its `support` (i.e., number of occurrences),
and a list of `source_sentences`.

An example row in the `canonical` configuration:

```JSON
{
  "arg1": "elephant",
  "rel": "/r/HasProperty",
  "arg2": "intelligent",
  "support": 15,
  "facets": [
    {
      "value": "extremely",
      "type": "DEGREE",
      "support": 11
    }
  ],
  "source_sentences": [
    {
      "text": "Elephants are extremely intelligent animals.",
      "source": "https://www.softschools.com/facts/animals/asian_elephant_facts/2310/"
    },
    {
      "text": "Elephants are extremely intelligent creatures and an elephant's brain can weigh as much as 4-6 kg.",
      "source": "https://www.elephantsforafrica.org/elephant-facts/"
    }
  ]
}
```

### Data Fields

- **For `canonical` configuration**
    - `arg1`: the first argument to the relationship, e.g., *elephant*
    - `rel`: the canonical relation, e.g., */r/HasProperty*
    - `arg2`: the second argument to the relationship, e.g., *intelligence*
    - `support`: the number of occurrences of the assertion, e.g., *15*
    - `facets`: an array of semantic facets, each contains
      - `value`: facet value, e.g., *extremely*
      - `type`: facet type, e.g., *DEGREE*
      - `support`: the number of occurrences of the facet, e.g., *11*
    - `source_sentences`: an array of source sentences from which the assertion was
      extracted, each contains
      - `text`: the raw text of the sentence
      - `source`: the URL to its parent document

- **For `open` configuration**
    - The fields of this configuration are the same as the `canonical`
      configuration's, except that
      the (`arg1`, `rel`, `arg2`) fields are replaced with the
      (`subject`, `predicate`, `object`) fields
      which are free
      text phrases extracted directly from the source sentences
      using an Open Information Extraction (OpenIE) tool.

### Data Splits

There are no splits. All data points come to a default split called `train`.

## Dataset Creation

### Curation Rationale

The commonsense knowledge base was created to assist in development of robust and reliable AI.

### Source Data

#### Initial Data Collection and Normalization

Texts were collected from the web using the Bing Search API, and went through various cleaning steps before being processed by an OpenIE tool to get open assertions.
The assertions were then grouped into semantically equivalent clusters.
Take a look at the research paper for more details.

#### Who are the source language producers?

Web users.

### Annotations

#### Annotation process

None.

#### Who are the annotators?

None.

### Personal and Sensitive Information

Unknown.

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The knowledge base has been developed by researchers at the
[Max Planck Institute for Informatics](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/).

Contact [Tuan-Phong Nguyen](http://tuan-phong.com) in case of questions and comments.

### Licensing Information

[The Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@InProceedings{nguyen2021www,
  title={Advanced Semantics for Commonsense Knowledge Extraction},
  author={Nguyen, Tuan-Phong and Razniewski, Simon and Weikum, Gerhard},
  year={2021},
  booktitle={The Web Conference 2021},
}
```

### Contributions

Thanks to [@phongnt570](https://github.com/phongnt570) for adding this dataset.
