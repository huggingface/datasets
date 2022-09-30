---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
pretty_name: 'TimeDial: Temporal Commonsense Reasoning in Dialog'
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- text-classification-other-dialog-act-classification
paperswithcode_id: timedial
---

# Dataset Card for TimeDial: Temporal Commonsense Reasoning in Dialog

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [TimeDial](https://github.com/google-research-datasets/timedial)
- **Paper:** [TimeDial: Temporal Commonsense Reasoning in Dialog](https://arxiv.org/abs/2106.04571)
- **Point of Contact:** [Please create an issue in the official repository](https://github.com/google-research-datasets/timedial)

### Dataset Summary

TimeDial presents a crowdsourced English challenge set, for temporal commonsense reasoning, formulated as a multiple choice cloze task with around 1.5k carefully curated dialogs. The dataset is derived from the DailyDialog ([Li et al., 2017](https://www.aclweb.org/anthology/I17-1099/)), which is a multi-turn dialog corpus.

In order to establish strong baselines and provide information on future model development, the authors conducted extensive experiments with state-of-the-art LMs. While humans can easily answer these questions (97.8\%), the best T5 model variant struggles on this challenge set (73\%). Moreover, our qualitative error analyses show that the models often rely on shallow, spurious features (particularly text matching), instead of truly doing reasoning over the context.

Detailed experiments and analyses can be found in their [paper](https://arxiv.org/pdf/2106.04571.pdf).

### Supported Tasks and Leaderboards

To be updated soon.

### Languages

The dataset is in English only.

## Dataset Structure

### Data Instances

```
 {
    "id": 1,
    "conversation": [
      "A: We need to take the accounts system offline to carry out the upgrade . But don't worry , it won't cause too much inconvenience . We're going to do it over the weekend .",
      "B: How long will the system be down for ?",
      "A: We'll be taking everything offline in about two hours ' time . It'll be down for a minimum of twelve hours . If everything goes according to plan , it should be up again by 6 pm on Saturday .",
      "B: That's fine . We've allowed <MASK> to be on the safe side ."
    ],
    "correct1": "forty-eight hours",
    "correct2": "50 hours ",
    "incorrect1": "two hours ",
    "incorrect1_rule": "Rule 1",
    "incorrect2": "12 days ",
    "incorrect2_rule": "Rule 2"
  }
```
### Data Fields

- "id": Unique identifier, as a integer
- "conversation": Dialog context with <MASK> span, as a string
- "correct1": Original <MASK> span, as a string
- "correct2": Additional correct option provided by annotators, as a string
- "incorrect1": Incorrect option #1 provided by annotators, as a string
- "incorrect1_rule": One of phrase matching ("Rule 1"), numeral matching ("Rule 2"), or open ended ("Rule 3"), as a string
- "incorrect2": Incorrect option #2 provided by annotators, as a string
- "incorrect2_rule": One of phrase matching ("Rule 1"), numeral matching ("Rule 2"), or open ended ("Rule 3"), as a string

### Data Splits

TimeDial dataset consists only of a test set of 1,104 dialog instances with 2 correct and 2 incorrect options with the following statistics:
|      | Avg.   |
|-----|-----|
|Turns per Dialog  | 11.7  |
|Words per Turn  | 16.5   |
|Time Spans per Dialog  | 3  |


## Dataset Creation

### Curation Rationale

Although previous works have studied temporal reasoning in natural language, they have either focused on specific time-related concepts in isolation, such as temporal ordering and relation extraction, and/or dealt with limited context, such as single-sentence-based question answering and natural language inference.

In this work, they make the first systematic study of temporal commonsense reasoning in a multi-turn dialog setting. The task involves complex reasoning that requires operations like comparison and arithmetic reasoning over temporal expressions and the need for commonsense and world knowledge.

### Source Data

#### Initial Data Collection and Normalization

The TIMEDIAL dataset is derived from DailyDialog data (Li et al., 2017), which is a multi-turn dialog corpus containing over 13K English dialogs. Dialogs in this dataset consist of turn-taking between two people on topics over 10 broad categories, ranging from daily lives to financial topics.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The data collection process involves two steps: (1) identifying dialogs that are rich in temporal expressions, and (2) asking human annotators to provide correct and incorrect options for cloze instances derived from these dialogs. More details about the two steps:

1) Temporal expression identification: Here, they select dialogs that are rich with temporal information, in order to focus on complex temporal reasoning that arises in natural dialogs. Temporal expressions are automatically identified with SU-Time, an off-the-shelf temporal expression detector. They keep only the dialogs with more than 3 temporal expressions and at least one expression that contains numerals like “two weeks” (as opposed to non-numeric spans, like “summer”, “right now”, and “later”). In their initial experiment, they observe that language models can often correctly predict these non-numerical temporal phrases.

2) Human annotated options: Next, they make spans in the dialogs. For a dialog, they mask out each temporal expression that contains numerals, each resulting in a cloze question that is then sent for human annotation.
This resulted in 1,526 instances for annotation. For each masked span in each dialog, they obtain human annotation to derive a fixed set of correct and incorrect options given the context. Concretely, given a masked dialog and a seed correct answer (i.e., the original text) for the masked span, the annotators were asked to (1) come up with an alternative correct answer that makes sense in the dialog adhering to commonsense, and (2) formulate two incorrect answers that have no possibility of making sense in the dialog context. They highlight all time expressions in the context to make it easier for annotators to select reasonable time expressions.

#### Who are the annotators?

They are English linguists.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Dataset provided for research purposes only. Please check dataset license for additional information.

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

TimeDial dataset is licensed under CC BY-NC-SA 4.0.

### Citation Information

```
@inproceedings{qin-etal-2021-timedial,
    title = "{TimeDial: Temporal Commonsense Reasoning in Dialog}",
    author = "Qin, Lianhui and Gupta, Aditya and Upadhyay, Shyam and He, Luheng and Choi, Yejin and Faruqui, Manaal",
    booktitle = "Proc. of ACL",
    year = "2021"
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.
