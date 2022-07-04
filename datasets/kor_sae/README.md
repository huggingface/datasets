---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- ko
license:
- cc-by-sa-4.0
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
pretty_name: Structured Argument Extraction for Korean
---

# Dataset Card for Structured Argument Extraction for Korean

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

- **Homepage:** [Structured Argument Extraction for Korean](https://github.com/warnikchow/sae4k)
- **Repository:** [Structured Argument Extraction for Korean](https://github.com/warnikchow/sae4k)
- **Paper:** [Machines Getting with the Program: Understanding Intent Arguments of Non-Canonical Directives](https://arxiv.org/abs/1912.00342)
- **Point of Contact:** [Won Ik Cho](wicho@hi.snu.ac.kr)

### Dataset Summary

The Structured Argument Extraction for Korean dataset is a set of question-argument and command-argument pairs with their respective question type label and negativeness label. Often times, agents like Alexa or Siri, encounter conversations without a clear objective from the user. The goal of this dataset is to extract the intent argument of a given utterance pair without a clear directive. This may yield a more robust agent capable of parsing more non-canonical forms of speech.

### Supported Tasks and Leaderboards

* `intent_classification`: The dataset can be trained with a Transformer like [BERT](https://huggingface.co/bert-base-uncased) to classify the intent argument or a question/command pair in Korean, and it's performance can be measured by it's BERTScore. 

### Languages

The text in the dataset is in Korean and the associated is BCP-47 code is `ko-KR`.

## Dataset Structure

### Data Instances

An example data instance contains a question or command pair and its label:

```
{
  "intent_pair1": "내일 오후 다섯시 조별과제 일정 추가해줘"
  "intent_pair2": "내일 오후 다섯시 조별과제 일정 추가하기"
  "label": 4
}
```

### Data Fields

* `intent_pair1`: a question/command pair
* `intent_pair2`: a corresponding question/command pair
* `label`: determines the intent argument of the pair and can be one of `yes/no` (0), `alternative` (1), `wh- questions` (2), `prohibitions` (3), `requirements` (4) and `strong requirements` (5)

### Data Splits

The corpus contains 30,837 examples.

## Dataset Creation

### Curation Rationale

The Structured Argument Extraction for Korean dataset was curated to help train models extract intent arguments from utterances without a clear objective or when the user uses non-canonical forms of speech. This is especially helpful in Korean because in English, the `Who, what, where, when and why` usually comes in the beginning, but this isn't necessarily the case in the Korean language. So for low-resource languages, this lack of data can be a bottleneck for comprehension performance.

### Source Data

#### Initial Data Collection and Normalization

The corpus was taken from the one constructed by [Cho et al.](https://arxiv.org/abs/1811.04231), a Korean single utterance corpus for identifying directives/non-directives that contains a wide variety of non-canonical directives. 

#### Who are the source language producers?

Korean speakers are the source language producers.

### Annotations

#### Annotation process

Utterances were categorized as question or command arguments and then further classified according to their intent argument.

#### Who are the annotators?

The annotation was done by three Korean natives with a background in computational linguistics.

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

The dataset is curated by Won Ik Cho, Young Ki Moon, Sangwhan Moon, Seok Min Kim and Nam Soo Kim.

### Licensing Information

The dataset is licensed under the CC BY-SA-4.0.

### Citation Information

```
@article{cho2019machines,
  title={Machines Getting with the Program: Understanding Intent Arguments of Non-Canonical Directives},
  author={Cho, Won Ik and Moon, Young Ki and Moon, Sangwhan and Kim, Seok Min and Kim, Nam Soo},
  journal={arXiv preprint arXiv:1912.00342},
  year={2019}
}
```

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.
