---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
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

- **Homepage:** [PIQA homepage](https://yonatanbisk.com/piqa/)
- **Paper:** [PIQA: Reasoning about Physical Commonsense in Natural Language](https://arxiv.org/abs/1911.11641)
- **Leaderboard:** [Official leaderboard](https://yonatanbisk.com/piqa/) *Note that there is a [2nd leaderboard](https://leaderboard.allenai.org/physicaliqa) featuring a different (blind) test set with 3,446 examples as part of the Machine Commonsense DARPA project.*
- **Point of Contact:** [Yonatan Bisk](https://yonatanbisk.com/piqa/)

### Dataset Summary

*To apply eyeshadow without a brush, should I use a cotton swab or a toothpick?*
Questions requiring this kind of physical commonsense pose a challenge to state-of-the-art
natural language understanding systems. The PIQA dataset introduces the task of physical commonsense reasoning
and a corresponding benchmark dataset Physical Interaction: Question Answering or PIQA.

Physical commonsense knowledge is a major challenge on the road to true AI-completeness,
including robots that interact with the world and understand natural language.

PIQA focuses on everyday situations with a preference for atypical solutions.
The dataset is inspired by instructables.com, which provides users with instructions on how to build, craft,
bake, or manipulate objects using everyday materials.

### Supported Tasks and Leaderboards

The underlying task is formualted as multiple choice question answering: given a question `q` and two possible solutions `s1`, `s2`, a model or a human must choose the most appropriate solution, of which exactly one is correct.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

An example looks like this:

```
{
  "goal": "How do I ready a guinea pig cage for it's new occupants?",
  "sol1": "Provide the guinea pig with a cage full of a few inches of bedding made of ripped paper strips, you will also need to supply it with a water bottle and a food dish.",
  "sol2": "Provide the guinea pig with a cage full of a few inches of bedding made of ripped jeans material, you will also need to supply it with a water bottle and a food dish.",
  "label": 0,
}
```

Note that the test set contains no labels. Predictions need to be submitted to the leaderboard.

### Data Fields

List and describe the fields present in the dataset. Mention their data type, and whether they are used as input or output in any of the tasks the dataset currently supports. If the data has span indices, describe their attributes, such as whether they are at the character level or word level, whether they are contiguous or not, etc. If the datasets contains example IDs, state whether they have an inherent meaning, such as a mapping to other datasets or pointing to relationships between data points.

- `goal`: the question which requires physical commonsense to be answered correctly
- `sol1`: the first solution
- `sol2`: the second solution
- `label`: the correct solution. `0` refers to `sol1` and `1` refers to `sol2`

### Data Splits

The dataset contains 16,000 examples for training, 2,000 for development and 3,000 for testing.

## Dataset Creation

### Curation Rationale

The goal of the dataset is to construct a resource that requires concrete physical reasoning.

### Source Data

The authors  provide a prompt to the annotators derived from instructables.com. The instructables website is a crowdsourced collection of instruc- tions for doing everything from cooking to car repair. In most cases, users provide images or videos detailing each step and a list of tools that will be required. Most goals are simultaneously rare and unsurprising. While an annotator is unlikely to have built a UV-Flourescent steampunk lamp or made a backpack out of duct tape, it is not surprising that someone interested in home crafting would create these, nor will the tools and materials be unfamiliar to the average person. Using these examples as the seed for their annotation, helps remind annotators about the less prototypical uses of everyday objects. Second, and equally important, is that instructions build on one another. This means that any QA pair inspired by an instructable is more likely to explicitly state assumptions about what preconditions need to be met to start the task and what postconditions define success.

Annotators were asked to glance at the instructions of an instructable and pull out or have it inspire them to construct two component tasks. They would then articulate the goal (often centered on atypical materials) and how to achieve it. In addition, annotaters were asked to provide a permutation to their own solution which makes it invalid (the negative solution), often subtly.

#### Initial Data Collection and Normalization

During validation, examples with low agreement were removed from the data.

The dataset is further cleaned to remove stylistic artifacts and trivial examples from the data, which have been shown to artificially inflate model performance on previous NLI benchmarks.using the AFLite algorithm introduced in ([Sakaguchi et al. 2020](https://arxiv.org/abs/1907.10641); [Sap et al. 2019](https://arxiv.org/abs/1904.09728)) which is an improvement on adversarial filtering ([Zellers et al, 2018](https://arxiv.org/abs/1808.05326)).

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Annotations are by construction obtained when crowdsourcers complete the prompt.

#### Who are the annotators?

Paid crowdsourcers

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
@inproceedings{Bisk2020,
  author = {Yonatan Bisk and Rowan Zellers and
            Ronan Le Bras and Jianfeng Gao
            and Yejin Choi},
  title = {PIQA: Reasoning about Physical Commonsense in
           Natural Language},
  booktitle = {Thirty-Fourth AAAI Conference on
               Artificial Intelligence},
  year = {2020},
}
```
