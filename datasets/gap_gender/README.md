---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|wikipedia
task_categories:
- structure-prediction
task_ids:
- coreference-resolution
---

# Dataset Card Creation Guide

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

## Dataset Description

- **Repository:** [Github repository](https://github.com/google-research-datasets/gap-coreference)
- **Paper:** [Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns)](https://arxiv.org/abs/1810.05201)
- **Point of Contact:** [gap-coreference@google.com](gap-coreference@google.com)

### Dataset Summary

Coreference resolution is an important task for natural language understanding and the resolution of ambiguous pronouns a longstanding challenge. Nonetheless, existing corpora do not capture ambiguous pronouns in sufficient volume or diversity to accurately indicate the practical utility of models. Furthermore, we find gender bias in existing corpora and systems favoring masculine entities.

GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of (ambiguous pronoun, antecedent name), sampled from Wikipedia and released by Google AI Language for the evaluation of coreference resolution in practical applications.

### Supported Tasks and Leaderboards

The task at hand is coreference resolution.

The metrics are F1 score on Masculine and Feminine examples, Overall and a Bias factor calculated as F/M. Please refer to the [official scorer](https://github.com/google-research-datasets/gap-coreference/blob/master/gap_scorer.py) for more details.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

Provide an JSON-formatted example and brief description of a typical instance in the dataset. If available, provide a link to further examples.

```
{
  'ID': 'validation-11',
  'Text': "This particular government recalled all the Greek officers who participated in the anti-Ottoman revolutionary movements in Thessaly, Epirus and Macedonia to return to Greece while by personal requirement of Kallergis, Otto's adjutants-- Gennaios Kolokotronis, Spyromilios, Ioannis Mamouris and Gardikiotis Grivas--were dismissed, while the hitherto Minister of Military Affairs, Skarlatos Soutsos, was suspended. When he was minister, Kallergis formed for the first time in Greece a fire brigade.",
  'Pronoun': 'he',
  'Pronoun-offset': 418,
  'A': 'Ioannis Mamouris',
  'A-coref': 'FALSE',
  'A-offset': 273,
  'B': 'Kallergis',
  'B-coref': 'TRUE',
  'B-offset': 435,
  'URL': 'http://en.wikipedia.org/wiki/Dimitrios_Kallergis',
}
```

Provide any additional information that is not covered in the other sections about the data here. In particular describe any relationships between data points and if these relationships are made explicit.

### Data Fields

The are eleven columns:
- `ID`: Unique identifer for an example (two pairs)
- `Text`:	Text containing the ambiguous pronoun and two candidate names. About a paragraph in length
- `Pronoun`:	The pronoun, text
- `Pronoun-offset`:	Character offset of Pronoun in Column 2 (Text)
- `A`:	The first name, text
- `A-offset`:	Character offset of A in Column 2 (Text)
- `A-coref`:	Whether A corefers with the pronoun, TRUE or FALSE
- `B`:	The second name, text
- `B-offset`:	Character offset of B in Column 2 (Text)
- `B-coref`:	Whether B corefers with the pronoun, TRUE or FALSE
- `URL`	The URL of the source Wikipedia page

NB: Please note that systems should detect mentions for inference automatically, and access labeled spans only to output predictions.

NB2: Please also note that there are two task settings, *snippet-context* in which the URL column may **not** be used, and *page-context* where the URL, and the denoted Wikipedia page, may be used.

### Data Splits

There are 3 splits:
- *train*: 4,000 pairs, may be used for model development
- *validation*: 908 pairs, may be used for parameter tuning
- *test*: 4,000 pairs, to be used for official evaluation

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

The corpus is extracted from Wikipedia using carefully designed detection patterns, heuristics and filterings.

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

Annotations are provided by a pool of in-house annotators (Google AI). Despite workers not being expert linguists, there is a good agreement both within workers and between workers and an expert.

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

Provide the [BibTex](http://www.bibtex.org/)-formatted reference for the dataset. For example:
```
@inproceedings{webster2018gap,
  title =     {Mind the GAP: A Balanced Corpus of Gendered Ambiguou},
  author =    {Webster, Kellie and Recasens, Marta and Axelrod, Vera and Baldridge, Jason},
  booktitle = {Transactions of the ACL},
  year =      {2018},
  pages =     {to appear},
}
```
