---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
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

- **Homepage:** [SWAG AF](https://rowanzellers.com/swag/)
- **Repository:** [Github repository](https://github.com/rowanz/swagaf/tree/master/data)
- **Paper:** [SWAG: A Large-Scale Adversarial Dataset for Grounded Commonsense Inference](https://arxiv.org/abs/1808.05326)
- **Leaderboard:** [SWAG Leaderboard](https://leaderboard.allenai.org/swag)
- **Point of Contact:** [Rowan Zellers](https://rowanzellers.com/#contact)

### Dataset Summary

Given a partial description like "she opened the hood of the car,"
humans can reason about the situation and anticipate what might come
next ("then, she examined the engine"). SWAG (Situations With Adversarial Generations)
is a large-scale dataset for this task of grounded commonsense
inference, unifying natural language inference and physically grounded reasoning.

The dataset consists of 113k multiple choice questions about grounded situations
(73k training, 20k validation, 20k test).
Each question is a video caption from LSMDC or ActivityNet Captions,
with four answer choices about what might happen next in the scene.
The correct answer is the (real) video caption for the next event in the video;
the three incorrect answers are adversarially generated and human verified,
so as to fool machines but not humans. SWAG aims to be a benchmark for
evaluating grounded commonsense NLI and for learning representations.

### Supported Tasks and Leaderboards

The dataset introduces the task of grounded commonsense inference, unifying natural language inference and commonsense reasoning.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

The `regular` configuration should be used for modeling. An example looks like this:

```
{
  "video-id": "anetv_dm5WXFiQZUQ",
  "fold-ind": "18419",
  "startphrase", "He rides the motorcycle down the hall and into the elevator. He",
  "sent1": "He rides the motorcycle down the hall and into the elevator."
  "sent2": "He",
  "gold-source": "gold",
  "ending0": "looks at a mirror in the mirror as he watches someone walk through a door.",
  "ending1": "stops, listening to a cup of coffee with the seated woman, who's standing.",
  "ending2": "exits the building and rides the motorcycle into a casino where he performs several tricks as people watch.",
  "ending3": "pulls the bag out of his pocket and hands it to someone's grandma.",
  "label": 2,
}
```

Note that the test are reseved for blind submission on the leaderboard.

The full train and validation sets provide more information regarding the collection process.

### Data Fields

- `video-id`: identification
- `fold-ind`: identification
- `startphrase`: the context to be filled
- `sent1`: the first sentence
- `sent2`: the start of the second sentence (to be filled)
- `gold-source`: generated or comes from the found completion
- `ending0`: first proposition
- `ending1`: second proposition
- `ending2`: third proposition
- `ending3`: fourth proposition
- `label`: the correct proposition

More info concerning the fields can be found [on the original repo](https://github.com/rowanz/swagaf/tree/master/data).

### Data Splits

The dataset consists of 113k multiple choice questions about grounded situations: 73k for training, 20k for validation, and 20k for (blind) test.

## Dataset Creation

### Curation Rationale

The authors seek dataset diversity while minimizing annotation artifacts, conditional stylistic patterns such as length and word-preference biases. To avoid introducing easily “gamed” patterns, they introduce Adversarial Filtering (AF), a generally- applicable treatment involving the iterative refinement of a set of assignments to increase the entropy under a chosen model family. The dataset is then human verified by paid crowdsourcers.

### Source Data

This section describes the source data (e.g. news text and headlines, social media posts, translated sentences,...)

#### Initial Data Collection and Normalization

The dataset is derived from pairs of consecutive video captions from [ActivityNet Captions](https://cs.stanford.edu/people/ranjaykrishna/densevid/) and the [Large Scale Movie Description Challenge](https://sites.google.com/site/describingmovies/). The two datasets are slightly different in nature and allow us to achieve broader coverage: ActivityNet contains 20k YouTube clips containing one of 203 activity types (such as doing gymnastics or playing guitar); LSMDC consists of 128k movie captions (audio descriptions and scripts).

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Annotations are first machine generated and then adversarially filtered. Finally, the remaining examples are human-verified by paid crowdsourcers.

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

Unknown

### Citation Information

```
@inproceedings{zellers2018swagaf,
    title={SWAG: A Large-Scale Adversarial Dataset for Grounded Commonsense Inference},
    author={Zellers, Rowan and Bisk, Yonatan and Schwartz, Roy and Choi, Yejin},
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year={2018}
}
```
