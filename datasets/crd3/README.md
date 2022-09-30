---
pretty_name: CRD3 (Critical Role Dungeons and Dragons Dataset)
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
source_datasets:
- original
task_categories:
- summarization
- text-generation
- fill-mask
task_ids:
- dialogue-modeling
size_categories:
- 10K<n<100K
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

- **Homepage:** [CRD3 homepage](https://github.com/RevanthRameshkumar/CRD3)
- **Repository:** [CRD3 repository](https://github.com/RevanthRameshkumar/CRD3)
- **Paper:** [Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset](https://www.aclweb.org/anthology/2020.acl-main.459/)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Dataset Summary

Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset.
Critical Role is an unscripted, live-streamed show where a fixed group of people play Dungeons and Dragons, an open-ended role-playing game.
The dataset is collected from 159 Critical Role episodes transcribed to text dialogues, consisting of 398,682 turns. It also includes corresponding
abstractive summaries collected from the Fandom wiki. The dataset is linguistically unique in that the narratives are generated entirely through player
collaboration and spoken interaction. For each dialogue, there are a large number of turns, multiple abstractive summaries with varying levels of detail,
and semantic ties to the previous dialogues.

### Supported Tasks and Leaderboards

`summarization`: The dataset can be used to train a model for abstractive summarization. A [fast abstractive summarization-RL](https://github.com/ChenRocks/fast_abs_rl) model was presented as a baseline, which achieves ROUGE-L-F1 of 25.18.

### Languages

The text in the dataset is in English, as spoken by actors on The Critical Role show, which is a weekly unscripted, live-stream of a fixed group of people playing Dungeons and Dragons, a popular role-playing game.

## Dataset Structure

### Data Instances

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
|default|38,969|   6,327|7,500|

## Dataset Creation

### Curation Rationale

Dialogue understanding and abstractive summarization remain both important and challenging problems for computational linguistics. Current paradigms in summarization modeling have specific failures in capturing semantics and pragmatics, content selection, rewriting, and evaluation in the domain of long, story-telling dialogue. CRD3 offers a linguistically rich dataset to explore these domains.

### Source Data

#### Initial Data Collection and Normalization

Dungeons and Dragons is a popular roleplaying game that is driven by structured storytelling. Critical Role is an unscripted, live-streamed show where a fixed group of people play Dungeons and Dragons. This dataset consists of 159 episodes of the show, where the episodes are transcribed. Inconsistencies (e.g. spelling of speaker names) were manually resolved.

The abstractive summaries were collected from the [Critical Role Fandom wiki](https://criticalrole.fandom.com/)

#### Who are the source language producers?

The language producers are actors on The Critical Role show, which is a weekly unscripted, live-stream of a fixed group of people playing Dungeons and Dragons, a popular role-playing game.

### Annotations

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

[N/A]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

CRTranscript provided transcripts of the show; contributors of the Critical Role Wiki provided the abstractive summaries.

### Licensing Information

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa-4.0]., as corresponding to the Critical Role Wiki https://criticalrole.fandom.com/

### Citation Information

```bibtex
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
