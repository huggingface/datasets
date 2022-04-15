---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
paperswithcode_id: wnut-2017-emerging-and-rare-entity
pretty_name: WNUT 17
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
---

# Dataset Card for "wnut_17"

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

- **Homepage:** [http://noisy-text.github.io/2017/emerging-rare-entities.html](http://noisy-text.github.io/2017/emerging-rare-entities.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.76 MB
- **Size of the generated dataset:** 1.66 MB
- **Total amount of disk used:** 2.43 MB

### Dataset Summary

WNUT 17: Emerging and Rare entity recognition

This shared task focuses on identifying unusual, previously-unseen entities in the context of emerging discussions.
Named entities form the basis of many modern approaches to other tasks (like event clustering and summarisation),
but recall on them is a real problem in noisy text - even among annotators. This drop tends to be due to novel entities and surface forms.
Take for example the tweet “so.. kktny in 30 mins?” - even human experts find entity kktny hard to detect and resolve.
This task will evaluate the ability to detect and classify novel, emerging, singleton named entities in noisy text.

The goal of this task is to provide a definition of emerging and of rare entities, and based on that, also datasets for detecting these entities.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

- **Size of downloaded dataset files:** 0.76 MB
- **Size of the generated dataset:** 1.66 MB
- **Total amount of disk used:** 2.43 MB

An example of 'train' looks as follows.
```
{
    "id": "0",
    "ner_tags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
    "tokens": ["@paulwalk", "It", "'s", "the", "view", "from", "where", "I", "'m", "living", "for", "two", "weeks", ".", "Empire", "State", "Building", "=", "ESB", ".", "Pretty", "bad", "storm", "here", "last", "evening", "."]
}
```

### Data Fields

The data fields are the same among all splits:
- `id` (`string`): ID of the example.
- `tokens` (`list` of `string`): Tokens of the example text.
- `ner_tags` (`list` of class labels): NER tags of the tokens (using IOB2 format), with possible values:
  - 0: `O`
  - 1: `B-corporation`
  - 2: `I-corporation`
  - 3: `B-creative-work`
  - 4: `I-creative-work`
  - 5: `B-group`
  - 6: `I-group`
  - 7: `B-location`
  - 8: `I-location`
  - 9: `B-person`
  - 10: `I-person`
  - 11: `B-product`
  - 12: `I-product`

### Data Splits

|train|validation|test|
|----:|---------:|---:|
| 3394|      1009|1287|

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
@inproceedings{derczynski-etal-2017-results,
    title = "Results of the {WNUT}2017 Shared Task on Novel and Emerging Entity Recognition",
    author = "Derczynski, Leon  and
      Nichols, Eric  and
      van Erp, Marieke  and
      Limsopatham, Nut",
    booktitle = "Proceedings of the 3rd Workshop on Noisy User-generated Text",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-4418",
    doi = "10.18653/v1/W17-4418",
    pages = "140--147",
    abstract = "This shared task focuses on identifying unusual, previously-unseen entities in the context of emerging discussions.
                Named entities form the basis of many modern approaches to other tasks (like event clustering and summarization),
                but recall on them is a real problem in noisy text - even among annotators.
                This drop tends to be due to novel entities and surface forms.
                Take for example the tweet {``}so.. kktny in 30 mins?!{''} {--} even human experts find the entity {`}kktny{'}
                hard to detect and resolve. The goal of this task is to provide a definition of emerging and of rare entities,
                and based on that, also datasets for detecting these entities. The task as described in this paper evaluated the
                ability of participating entries to detect and classify novel and emerging named entities in noisy text.",
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@stefan-it](https://github.com/stefan-it), [@lewtun](https://github.com/lewtun), [@jplu](https://github.com/jplu) for adding this dataset.