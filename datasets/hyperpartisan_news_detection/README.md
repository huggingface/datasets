---
annotations_creators:
- crowdsourced
- expert-generated
language:
- en
language_creators:
- found
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: HyperpartisanNewsDetection
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-bias-classification
paperswithcode_id: null
---

# Dataset Card for "hyperpartisan_news_detection"

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

- **Homepage:** [https://pan.webis.de/semeval19/semeval19-web/](https://pan.webis.de/semeval19/semeval19-web/)
- **Repository:** https://github.com/pan-webis-de/pan-code/tree/master/semeval19
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 957.68 MB
- **Size of the generated dataset:** 5354.14 MB
- **Total amount of disk used:** 6311.82 MB

### Dataset Summary

Hyperpartisan News Detection was a dataset created for PAN @ SemEval 2019 Task 4.
Given a news article text, decide whether it follows a hyperpartisan argumentation, i.e., whether it exhibits blind, prejudiced, or unreasoning allegiance to one party, faction, cause, or person.

There are 2 parts:
- byarticle: Labeled through crowdsourcing on an article basis. The data contains only articles for which a consensus among the crowdsourcing workers existed.
- bypublisher: Labeled by the overall bias of the publisher as provided by BuzzFeed journalists or MediaBiasFactCheck.com.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### byarticle

- **Size of downloaded dataset files:** 0.95 MB
- **Size of the generated dataset:** 2.67 MB
- **Total amount of disk used:** 3.63 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "hyperpartisan": true,
    "published_at": "2020-01-01",
    "text": "\"<p>This is a sample article which will contain lots of text</p>\\n    \\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing el...",
    "title": "Example article 1",
    "url": "http://www.example.com/example1"
}
```

#### bypublisher

- **Size of downloaded dataset files:** 956.72 MB
- **Size of the generated dataset:** 5351.47 MB
- **Total amount of disk used:** 6308.19 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "bias": 3,
    "hyperpartisan": false,
    "published_at": "2020-01-01",
    "text": "\"<p>This is a sample article which will contain lots of text</p>\\n    \\n<p>Phasellus bibendum porta nunc, id venenatis tortor fi...",
    "title": "Example article 4",
    "url": "https://example.com/example4"
}
```

### Data Fields

The data fields are the same among all splits.

#### byarticle
- `text`: a `string` feature.
- `title`: a `string` feature.
- `hyperpartisan`: a `bool` feature.
- `url`: a `string` feature.
- `published_at`: a `string` feature.

#### bypublisher
- `text`: a `string` feature.
- `title`: a `string` feature.
- `hyperpartisan`: a `bool` feature.
- `url`: a `string` feature.
- `published_at`: a `string` feature.
- `bias`: a classification label, with possible values including `right` (0), `right-center` (1), `least` (2), `left-center` (3), `left` (4).

### Data Splits

#### byarticle

|         |train|
|---------|----:|
|byarticle|  645|

#### bypublisher

|           |train |validation|
|-----------|-----:|---------:|
|bypublisher|600000|    600000|

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

The collection (including labels) are licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
@article{kiesel2019data,
  title={Data for pan at semeval 2019 task 4: Hyperpartisan news detection},
  author={Kiesel, Johannes and Mestre, Maria and Shukla, Rishabh and Vincent, Emmanuel and Corney, David and Adineh, Payam and Stein, Benno and Potthast, Martin},
  year={2019}
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@ghomasHudson](https://github.com/ghomasHudson) for adding this dataset.
