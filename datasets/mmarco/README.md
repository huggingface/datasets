---
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
languages:
- zh-CN
- en-US
- fr-FR
- de-DE
- id-ID
- it-IT
- pt-BR
- ru-RU
- es-ES
licenses:
- cc-by-4.0
multilinguality:
- multilingual
- translation
pretty_name: mMARCO
size_categories:
- unknown
source_datasets: []
task_categories:
- text-retrieval
task_ids:
- document-retrieval
---

# Dataset Card for mMARCO

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

- **Homepage:** https://github.com/unicamp-dl/mMARCO/
- **Repository:** https://github.com/unicamp-dl/mMARCO/
- **Paper:** https://arxiv.org/abs/2108.13897
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

A multilingual version of MS MARCO Passage Ranking dataset. All passages and queries were machine translated into 8 languages: Chinese, French, German, Indonesian, Italian, Portuguese, Russian, and Spanish.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

| Language name | Language code |
|---------------|---------------|
| English		| english		|
| Chinese		| chinese		|
| French		| french		|
| German		| german		|
| Indonesian	| indonesian	|
| Italian		| italian		|
| Portuguese	| portuguese	|
| Russian		| russian		|
| Spanish		| spanish		|

## Dataset Structure

### Data Instances

#### Training triples

```
>>> dataset = load_dataset('mmarco', 'english')
>>> dataset['train'][1]
{'query': 'what fruit is native to australia', 'positive': 'Passiflora herbertiana. A rare passion fruit native to Australia. Fruits are green-skinned, white fleshed, with an unknown edible rating. Some sources list the fruit as edible, sweet and tasty, while others list the fruits as being bitter and inedible.assiflora herbertiana. A rare passion fruit native to Australia. Fruits are green-skinned, white fleshed, with an unknown edible rating. Some sources list the fruit as edible, sweet and tasty, while others list the fruits as being bitter and inedible.', 'negative': 'The kola nut is the fruit of the kola tree, a genus (Cola) of trees that are native to the tropical rainforests of Africa.'}
```

#### Queries

```
>>> dataset = load_dataset('mmarco', 'queries-spanish')
>>> dataset['train'][1]
{'id': 634306, 'text': '¿Qué significa Chattel en el historial de crédito'}
```

#### Collection

```
>>> dataset = load_dataset('mmarco', 'collection-portuguese')
>>> dataset['collection'][100]
{'id': 100, 'text': 'Antonín Dvorák (1841-1904) Antonin Dvorak era filho de açougueiro, mas ele não seguiu o negócio de seu pai. Enquanto ajudava seu pai a meio tempo, estudou música e se formou na Escola de Órgãos de Praga em 1859.'}
```

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

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

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@lhbonifacio](https://github.com/lhbonifacio) and [@hugoabonizio](https://github.com/hugoabonizio) for adding this dataset.
