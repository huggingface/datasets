---
languages:
- en
paperswithcode_id: crd3
---

# Dataset Card for "crd3"

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

- **Homepage:** [https://github.com/RevanthRameshkumar/CRD3](https://github.com/RevanthRameshkumar/CRD3)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 279.93 MB
- **Size of the generated dataset:** 4020.33 MB
- **Total amount of disk used:** 4300.25 MB

### Dataset Summary

Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset.
Critical Role is an unscripted, live-streamed show where a fixed group of people play Dungeons and Dragons, an open-ended role-playing game.
The dataset is collected from 159 Critical Role episodes transcribed to text dialogues, consisting of 398,682 turns. It also includes corresponding
abstractive summaries collected from the Fandom wiki. The dataset is linguistically unique in that the narratives are generated entirely through player
collaboration and spoken interaction. For each dialogue, there are a large number of turns, multiple abstractive summaries with varying levels of detail,
and semantic ties to the previous dialogues.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### default

- **Size of downloaded dataset files:** 279.93 MB
- **Size of the generated dataset:** 4020.33 MB
- **Total amount of disk used:** 4300.25 MB

An example of 'train' looks as follows.
```
{
    "alignment_score": 3.679936647415161,
    "chunk": "Wish them a Happy Birthday on their Facebook and Twitter pages! Also, as a reminder: D&D Beyond streams their weekly show (\"And Beyond\") every Wednesday on twitch.tv/dndbeyond.",
    "chunk_id": 1,
    "turn_end": 6,
    "turn_num": 4,
    "turn_start": 4,
    "turns": {
        "names": ["SAM"],
        "utterances": ["Yesterday, guys, was D&D Beyond's first one--", "first one-year anniversary. Take two. Hey guys,", "yesterday was D&D Beyond's one-year anniversary.", "Wish them a happy birthday on their Facebook and", "Twitter pages."]
    }
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `chunk`: a `string` feature.
- `chunk_id`: a `int32` feature.
- `turn_start`: a `int32` feature.
- `turn_end`: a `int32` feature.
- `alignment_score`: a `float32` feature.
- `turn_num`: a `int32` feature.
- `turns`: a dictionary feature containing:
  - `names`: a `string` feature.
  - `utterances`: a `string` feature.

### Data Splits

| name  | train |validation| test  |
|-------|------:|---------:|------:|
|default|2942362|   2942362|2942362|

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

@inproceedings{
title = {Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset},
author = {Rameshkumar, Revanth  and Bailey, Peter},
year = {2020},
publisher = {Association for Computational Linguistics},
conference = {ACL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun) for adding this dataset.