---
annotations_creators:
- machine-generated
language_creators:
- found
language:
- ar
- bg
- ca
- cs
- da
- de
- el
- en
- es
- et
- fa
- fi
- fr
- he
- hi
- hr
- hu
- id
- it
- ja
- ko
- lt
- lv
- ms
- nl
- 'no'
- pl
- pt
- ro
- ru
- sk
- sl
- sr
- sv
- th
- tl
- tr
- uk
- vi
- zh
license:
- unknown
multilinguality:
- multilingual
pretty_name: Polyglot-NER
size_categories:
- unknown
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: polyglot-ner
---

# Dataset Card for Polyglot-NER

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

- **Homepage:** [https://sites.google.com/site/rmyeid/projects/polylgot-ner](https://sites.google.com/site/rmyeid/projects/polylgot-ner)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 43285.14 MB
- **Size of the generated dataset:** 11958.61 MB
- **Total amount of disk used:** 55243.75 MB

### Dataset Summary

Polyglot-NER
A training dataset automatically generated from Wikipedia and Freebase the task
of named entity recognition. The dataset contains the basic Wikipedia based
training data for 40 languages we have (with coreference resolution) for the task of
named entity recognition. The details of the procedure of generating them is outlined in
Section 3 of the paper (https://arxiv.org/abs/1410.3791). Each config contains the data
corresponding to a different language. For example, "es" includes only spanish examples.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### ar

- **Size of downloaded dataset files:** 1055.74 MB
- **Size of the generated dataset:** 175.05 MB
- **Total amount of disk used:** 1230.78 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "2",
    "lang": "ar",
    "ner": ["O", "O", "O", "O", "O", "O", "O", "O", "LOC", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "PER", "PER", "PER", "PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    "words": "[\"وفي\", \"مرحلة\", \"موالية\", \"أنشأت\", \"قبيلة\", \"مكناسة\", \"الزناتية\", \"مكناسة\", \"تازة\", \",\", \"وأقام\", \"بها\", \"المرابطون\", \"قلعة\", \"..."
}
```

#### bg

- **Size of downloaded dataset files:** 1055.74 MB
- **Size of the generated dataset:** 181.68 MB
- **Total amount of disk used:** 1237.42 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "1",
    "lang": "bg",
    "ner": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    "words": "[\"Дефиниция\", \"Наименованията\", \"\\\"\", \"книжовен\", \"\\\"/\\\"\", \"литературен\", \"\\\"\", \"език\", \"на\", \"български\", \"за\", \"тази\", \"кодифи..."
}
```

#### ca

- **Size of downloaded dataset files:** 1055.74 MB
- **Size of the generated dataset:** 137.09 MB
- **Total amount of disk used:** 1192.82 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "2",
    "lang": "ca",
    "ner": "[\"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O\", \"O...",
    "words": "[\"Com\", \"a\", \"compositor\", \"deixà\", \"un\", \"immens\", \"llegat\", \"que\", \"inclou\", \"8\", \"simfonies\", \"(\", \"1822\", \"),\", \"diverses\", ..."
}
```

#### combined

- **Size of downloaded dataset files:** 1055.74 MB
- **Size of the generated dataset:** 5995.61 MB
- **Total amount of disk used:** 7051.35 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "18",
    "lang": "es",
    "ner": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    "words": "[\"Los\", \"cambios\", \"en\", \"la\", \"energía\", \"libre\", \"de\", \"Gibbs\", \"\\\\\", \"Delta\", \"G\", \"nos\", \"dan\", \"una\", \"cuantificación\", \"de..."
}
```

#### cs

- **Size of downloaded dataset files:** 1055.74 MB
- **Size of the generated dataset:** 149.53 MB
- **Total amount of disk used:** 1205.26 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "3",
    "lang": "cs",
    "ner": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
    "words": "[\"Historie\", \"Symfonická\", \"forma\", \"se\", \"rozvinula\", \"se\", \"především\", \"v\", \"období\", \"klasicismu\", \"a\", \"romantismu\", \",\", \"..."
}
```

### Data Fields

The data fields are the same among all splits.

#### ar
- `id`: a `string` feature.
- `lang`: a `string` feature.
- `words`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

#### bg
- `id`: a `string` feature.
- `lang`: a `string` feature.
- `words`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

#### ca
- `id`: a `string` feature.
- `lang`: a `string` feature.
- `words`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

#### combined
- `id`: a `string` feature.
- `lang`: a `string` feature.
- `words`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

#### cs
- `id`: a `string` feature.
- `lang`: a `string` feature.
- `words`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

### Data Splits

| name     |    train |
|----------|---------:|
| ar       |   339109 |
| bg       |   559694 |
| ca       |   372665 |
| combined | 21070925 |
| cs       |   564462 |

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
@article{polyglotner,
         author = {Al-Rfou, Rami and Kulkarni, Vivek and Perozzi, Bryan and Skiena, Steven},
         title = {{Polyglot-NER}: Massive Multilingual Named Entity Recognition},
         journal = {{Proceedings of the 2015 {SIAM} International Conference on Data Mining, Vancouver, British Columbia, Canada, April 30- May 2, 2015}},
         month     = {April},
         year      = {2015},
         publisher = {SIAM},
}

```


### Contributions

Thanks to [@joeddav](https://github.com/joeddav) for adding this dataset.