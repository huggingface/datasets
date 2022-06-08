---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- de
- en
- egy
licenses:
- cc-by-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|wikipedia
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: BbawEgyptian
---

# Dataset Card for "bbaw_egyptian"

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

- **Homepage:** [https://edoc.bbaw.de/frontdoor/index/index/docId/2919](https://edoc.bbaw.de/frontdoor/index/index/docId/2919)
- **Repository:** [Github](https://phiwi.github.io/all.json)
- **Paper:** [Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian Hieroglyph](https://zenodo.org/record/3524924)
- **Point of Contact:** [Philipp Wiesenbach](https://www.cl.uni-heidelberg.de/~wiesenbach/index.html)
- **Size of downloaded dataset files:** 34 MB


### Dataset Summary

This dataset comprises parallel sentences of hieroglyphic encodings, transcription and translation as used in the paper [Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian Hieroglyph](https://zenodo.org/record/3524924). The data triples are extracted from the [digital corpus of Egyptian texts](https://edoc.bbaw.de/frontdoor/index/index/docId/2919) compiled by the project "Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache".

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

The dataset consists of parallel triples of
- `hieroglyphs`: [Encoding of the hieroglyphs with the [Gardiner's sign list](https://en.wikipedia.org/wiki/Gardiner%27s_sign_list)
- `transcription`: Transliteration of the above mentioned hieroglyphs with a [transliteration scheme](https://en.wikipedia.org/wiki/Transliteration_of_Ancient_Egyptian)
- `translation`: Translation in mostly German language (with some English mixed in)

## Dataset Structure

The dataset is not divided into 'train', 'dev' and 'test' splits as it was not built for competitive purposes and we encourage all scientists to use individual partitioning schemes to suit their needs (due to the low resource setting it might be advisable to use cross validation anyway). The only available split 'all' therefore comprises the full 100,708 translation triples, 35,503 of which possess hieroglyphic encodings (the remaining 65,205 triples have empty `hieroglyph` entries).

### Data Instances

An example of a data triple looks the following way:

```
{
    "transcription": "n rḏi̯(.w) gꜣ =j r dbḥ.t m pr-ḥḏ",
    "translation": "I was not let to suffer lack in the treasury with respect to what was needed;",
    "hieroglyphs": "D35 D21 -D37 G1&W11 -V32B A1 D21 D46 -D58 *V28 -F18 *X1 -A2 G17 [? *O2 *?]"
}

```

*Important*: Only about a third of the instance actually cover hieroglyphic encodings (the rest is the empty string `""`) as the leftover encodings have not yet been incorporated into the BBAW's project database.

### Data Fields

#### plain_text
- `transcription`: a `string` feature.
- `translation`: a `string` feature.
- `hieroglyphs`: a `string` feature.


### Data Splits

|   name   |all|
|----------|----:|
|plain_text|100708|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

The data source comes from the project "Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache" which is compiling an extensively annotated digital corpus of Egyptian texts. Their [publication](https://edoc.bbaw.de/frontdoor/index/index/docId/2919) comprises an excerpt of the internal database's contents.

#### Who are the source language producers?

[More Information Needed]


### Annotations

#### Annotation process

The corpus has not been preprocessed as we encourage every scientist to prepare the corpus to their desired needs. This means, that all textcritic symbols are still included in the transliteration and translation. This concerns the following annotations:

- `()`: defective
- `[]`: lost
- `{}`: surplus
- `〈〉`: omitted
- `⸢⸣`: damaged
- `⸮?`: unclear
- `{{}}`: erasure
- `(())`: above
- `[[]]`: overstrike
- `〈〈〉〉`: haplography

Their exists a similar sign list for the annotation of the hieroglyphic encoding. If you wish access to this list, please get in contact with the author.


#### Who are the annotators?

[More Information Needed]

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
Source corpus:
```
@misc{OPUS4-2919,
  title     = {Teilauszug der Datenbank des Vorhabens "Strukturen und Transformationen des Wortschatzes der {\"a}gyptischen Sprache" vom Januar 2018},
  institution = {Akademienvorhaben Strukturen und Transformationen des Wortschatzes der {\"a}gyptischen Sprache. Text- und Wissenskultur im alten {\"A}gypten},
  type      = {other},
  year        = {2018},
}

```

Translation paper:
```
@article{wiesenbach19,
  title = {Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian Hieroglyphs},
  author = {Wiesenbach, Philipp and Riezler, Stefan},
  journal = {Proceedings of the International Workshop on Spoken Language Translation},
  journal-abbrev = {IWSLT},
  year = {2019},
  url = {https://www.cl.uni-heidelberg.de/statnlpgroup/publications/IWSLT2019_v2.pdf}
}
```

### Contributions

Thanks to [@phiwi](https://github.com/phiwi) for adding this dataset.
