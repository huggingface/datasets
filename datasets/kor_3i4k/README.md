---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ko
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: null
---

# Dataset Card for 3i4K

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

- **Homepage: [3i4K](https://github.com/warnikchow/3i4k)**
- **Repository: [3i4K](https://github.com/warnikchow/3i4k)**
- **Paper: [Speech Intention Understanding in a Head-final Language: A Disambiguation Utilizing Intonation-dependency](https://arxiv.org/abs/1811.04231)**
- **Point of Contact: [Won Ik Cho](wicho@hi.snu.ac.kr)**

### Dataset Summary

The 3i4K dataset is a set of frequently used Korean words (corpus provided by the Seoul National University Speech Language Processing Lab) and manually created questions/commands containing short utterances. The goal is to identify the speaker intention of a spoken utterance based on its transcript, and whether in some cases, requires using auxiliary acoustic features. The classification system decides whether the utterance is a fragment, statement, question, command, rhetorical question, rhetorical command, or an intonation-dependent utterance. This is important because in head-final languages like Korean, the level of the intonation plays a significant role in identifying the speaker's intention.

### Supported Tasks and Leaderboards

* `intent-classification`: The dataset can be trained with a CNN or BiLISTM-Att to identify the intent of a spoken utterance in Korean and the performance can be measured by its F1 score.

### Languages

The text in the dataset is in Korean and the associated is BCP-47 code is `ko-KR`.

## Dataset Structure

### Data Instances

An example data instance contains a short utterance and it's label:

```
{
  "label": 3,
  "text": "선수잖아 이 케이스 저 케이스 많을 거 아냐 선배라고 뭐 하나 인생에 도움도 안주는데 내가 이렇게 진지하게 나올 때 제대로 한번 조언 좀 해줘보지"
}
```

### Data Fields

* `label`: determines the intention of the utterance and can be one of `fragment` (0), `statement` (1), `question` (2), `command` (3), `rhetorical question` (4), `rhetorical command` (5) and `intonation-depedent utterance` (6).
* `text`: the text in Korean about common topics like housework, weather, transportation, etc.

### Data Splits

The data is split into a training set comrpised of 55134 examples and a test set of 6121 examples.

## Dataset Creation

### Curation Rationale

For head-final languages like Korean, intonation can be a determining factor in identifying the speaker's intention. The purpose of this dataset is to to determine whether an utterance is a fragment, statement, question, command, or a rhetorical question/command using the intonation-depedency from the head-finality. This is expected to improve language understanding of spoken Korean utterances and can be beneficial for speech-to-text applications.

### Source Data

#### Initial Data Collection and Normalization

The corpus was provided by Seoul National University Speech Language Processing Lab, a set of frequently used words from the National Institute of Korean Language and manually created commands and questions. The utterances cover topics like weather, transportation and stocks. 20k lines were randomly selected.

#### Who are the source language producers?

Korean speakers produced the commands and questions.

### Annotations

#### Annotation process

Utterances were classified into seven categories. They were provided clear instructions on the annotation guidelines (see [here](https://docs.google.com/document/d/1-dPL5MfsxLbWs7vfwczTKgBq_1DX9u1wxOgOPn1tOss/edit#) for the guidelines) and the resulting inter-annotator agreement was 0.85 and the final decision was done by majority voting.

#### Who are the annotators?

The annotation was completed by three Seoul Korean L1 speakers.

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

The dataset is curated by Won Ik Cho, Hyeon Seung Lee, Ji Won Yoon, Seok Min Kim and Nam Soo Kim.

### Licensing Information

The dataset is licensed under the CC BY-SA-4.0.

### Citation Information

```
@article{cho2018speech,
	title={Speech Intention Understanding in a Head-final Language: A Disambiguation Utilizing Intonation-dependency},
	author={Cho, Won Ik and Lee, Hyeon Seung and Yoon, Ji Won and Kim, Seok Min and Kim, Nam Soo},
	journal={arXiv preprint arXiv:1811.04231},
	year={2018}
}
```

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.