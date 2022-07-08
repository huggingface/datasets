---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
language:
- en
license:
- unknown
multilinguality:
- multilingual
pretty_name: WikiSnippets
size_categories:
- "10M<n<100M"
source_datasets:
- extended|wiki40b
- extended|wikipedia
task_categories:
- sequence-modeling
- other
task_ids:
- language-modeling
- other-text-search
paperswithcode_id: null
---

# Dataset Card for "wiki_snippets"

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

- **Homepage:** [https://dumps.wikimedia.org](https://dumps.wikimedia.org)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Dataset Summary

Wikipedia version split into plain text snippets for dense semantic indexing.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for 2 configurations of the dataset (with 100 snippet passage length and 0 overlap) in
English:
- wiki40b_en_100_0: Wiki-40B
- wikipedia_en_100_0: Wikipedia

### Data Instances

#### wiki40b_en_100_0

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 12339.25 MB
- **Total amount of disk used:** 12339.25 MB

An example of 'train' looks as follows:
```
{'_id': '{"datasets_id": 0, "wiki_id": "Q1294448", "sp": 2, "sc": 0, "ep": 6, "ec": 610}',
 'datasets_id': 0,
 'wiki_id': 'Q1294448',
 'start_paragraph': 2,
 'start_character': 0,
 'end_paragraph': 6,
 'end_character': 610,
 'article_title': 'Ági Szalóki',
 'section_title': 'Life',
 'passage_text': "Ági Szalóki Life She started singing as a toddler, considering Márta Sebestyén a role model. Her musical background is traditional folk music; she first won recognition for singing with Ökrös in a traditional folk style, and Besh o droM, a Balkan gypsy brass band. With these ensembles she toured around the world from the Montreal Jazz Festival, through Glastonbury Festival to the Théatre de la Ville in Paris, from New York to Beijing.\nSince 2005, she began to pursue her solo career and explore various genres, such as jazz, thirties ballads, or children's songs.\nUntil now, three of her six released albums"}
```

#### wikipedia_en_100_0

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 25184.52 MB
- **Total amount of disk used:** 25184.52 MB

An example of 'train' looks as follows:
```
{'_id': '{"datasets_id": 0, "wiki_id": "Anarchism", "sp": 0, "sc": 0, "ep": 2, "ec": 129}',
 'datasets_id': 0,
 'wiki_id': 'Anarchism',
 'start_paragraph': 0,
 'start_character': 0,
 'end_paragraph': 2,
 'end_character': 129,
 'article_title': 'Anarchism',
 'section_title': 'Start',
 'passage_text': 'Anarchism is a political philosophy and movement that is sceptical of authority and rejects all involuntary, coercive forms of hierarchy. Anarchism calls for the abolition of the state, which it holds to be unnecessary, undesirable, and harmful. As a historically left-wing movement, placed on the farthest left of the political spectrum, it is usually described alongside communalism and libertarian Marxism as the libertarian wing (libertarian socialism) of the socialist movement, and has a strong historical association with anti-capitalism and socialism.  Humans lived in societies without formal hierarchies long before the establishment of formal states, realms, or empires. With the'}
```

### Data Fields

The data fields are the same for all configurations:
- `_id`: a `string` feature.
- `datasets_id`: a `int32` feature.
- `wiki_id`: a `string` feature.
- `start_paragraph`: a `int32` feature.
- `start_character`: a `int32` feature.
- `end_paragraph`: a `int32` feature.
- `end_character`: a `int32` feature.
- `article_title`: a `string` feature.
- `section_title`: a `string` feature.
- `passage_text`: a `string` feature.


### Data Splits

| name               |    train |
|:-------------------|---------:|
| wiki40b_en_100_0   | 17553713 |
| wikipedia_en_100_0 | 33849898 |

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

See licensing information of source datasets.

### Citation Information

Cite source datasets:

- Wiki-40B:
```
@inproceedings{49029,
title = {Wiki-40B: Multilingual Language Model Dataset},
author = {Mandy Guo and Zihang Dai and Denny Vrandecic and Rami Al-Rfou},
year = {2020},
booktitle   = {LREC 2020}
}
```

- Wikipedia:
```
@ONLINE{wikidump,
    author = "Wikimedia Foundation",
    title  = "Wikimedia Downloads",
    url    = "https://dumps.wikimedia.org"
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham), [@yjernite](https://github.com/yjernite) for adding this dataset.
