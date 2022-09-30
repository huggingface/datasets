---
annotations_creators:
- crowdsourced
- expert-generated
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: SciCite
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
- multi-class-classification
paperswithcode_id: scicite
---

# Dataset Card for "scicite"

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

- **Homepage:**
- **Repository:** https://github.com/allenai/scicite
- **Paper:** [Structural Scaffolds for Citation Intent Classification in Scientific Publications](https://arxiv.org/abs/1904.01608)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 22.12 MB
- **Size of the generated dataset:** 4.91 MB
- **Total amount of disk used:** 27.02 MB

### Dataset Summary

This is a dataset for classifying citation intents in academic papers.
The main citation intent label for each Json object is specified with the label
key while the citation context is specified in with a context key. Example:
{
 'string': 'In chacma baboons, male-infant relationships can be linked to both
    formation of friendships and paternity success [30,31].'
 'sectionName': 'Introduction',
 'label': 'background',
 'citingPaperId': '7a6b2d4b405439',
 'citedPaperId': '9d1abadc55b5e0',
 ...
 }
You may obtain the full information about the paper using the provided paper ids
with the Semantic Scholar API (https://api.semanticscholar.org/).
The labels are:
Method, Background, Result

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 22.12 MB
- **Size of the generated dataset:** 4.91 MB
- **Total amount of disk used:** 27.02 MB

An example of 'validation' looks as follows.
```
{
    "citeEnd": 68,
    "citeStart": 64,
    "citedPaperId": "5e413c7872f5df231bf4a4f694504384560e98ca",
    "citingPaperId": "8f1fbe460a901d994e9b81d69f77bfbe32719f4c",
    "excerpt_index": 0,
    "id": "8f1fbe460a901d994e9b81d69f77bfbe32719f4c>5e413c7872f5df231bf4a4f694504384560e98ca",
    "isKeyCitation": false,
    "label": 2,
    "label2": 0,
    "label2_confidence": 0.0,
    "label_confidence": 0.0,
    "sectionName": "Discussion",
    "source": 4,
    "string": "These results are in contrast with the findings of Santos et al.(16), who reported a significant association between low sedentary time and healthy CVF among Portuguese"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `string`: a `string` feature.
- `sectionName`: a `string` feature.
- `label`: a classification label, with possible values including `method` (0), `background` (1), `result` (2).
- `citingPaperId`: a `string` feature.
- `citedPaperId`: a `string` feature.
- `excerpt_index`: a `int32` feature.
- `isKeyCitation`: a `bool` feature.
- `label2`: a classification label, with possible values including `supportive` (0), `not_supportive` (1), `cant_determine` (2), `none` (3).
- `citeEnd`: a `int64` feature.
- `citeStart`: a `int64` feature.
- `source`: a classification label, with possible values including `properNoun` (0), `andPhrase` (1), `acronym` (2), `etAlPhrase` (3), `explicit` (4).
- `label_confidence`: a `float32` feature.
- `label2_confidence`: a `float32` feature.
- `id`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 8194|       916|1859|

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
@inproceedings{cohan-etal-2019-structural,
    title = "Structural Scaffolds for Citation Intent Classification in Scientific Publications",
    author = "Cohan, Arman  and
      Ammar, Waleed  and
      van Zuylen, Madeleine  and
      Cady, Field",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/N19-1361",
    doi = "10.18653/v1/N19-1361",
    pages = "3586--3596",
}
```

### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
