---
language:
- en
paperswithcode_id: semeval-2010-task-8
pretty_name: SemEval-2010 Task 8
train-eval-index:
- config: default
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    sentence: text
    relation: target
  metrics:
  - type: accuracy
    name: Accuracy
  - type: f1
    name: F1 macro
    args:
      average: macro
  - type: f1
    name: F1 micro
    args:
      average: micro
  - type: f1
    name: F1 weighted
    args:
      average: weighted
  - type: precision
    name: Precision macro
    args:
      average: macro
  - type: precision
    name: Precision micro
    args:
      average: micro
  - type: precision
    name: Precision weighted
    args:
      average: weighted
  - type: recall
    name: Recall macro
    args:
      average: macro
  - type: recall
    name: Recall micro
    args:
      average: micro
  - type: recall
    name: Recall weighted
    args:
      average: weighted
dataset_info:
  features:
  - name: sentence
    dtype: string
  - name: relation
    dtype:
      class_label:
        names:
          0: Cause-Effect(e1,e2)
          1: Cause-Effect(e2,e1)
          2: Component-Whole(e1,e2)
          3: Component-Whole(e2,e1)
          4: Content-Container(e1,e2)
          5: Content-Container(e2,e1)
          6: Entity-Destination(e1,e2)
          7: Entity-Destination(e2,e1)
          8: Entity-Origin(e1,e2)
          9: Entity-Origin(e2,e1)
          10: Instrument-Agency(e1,e2)
          11: Instrument-Agency(e2,e1)
          12: Member-Collection(e1,e2)
          13: Member-Collection(e2,e1)
          14: Message-Topic(e1,e2)
          15: Message-Topic(e2,e1)
          16: Product-Producer(e1,e2)
          17: Product-Producer(e2,e1)
          18: Other
  splits:
  - name: test
    num_bytes: 357075
    num_examples: 2717
  - name: train
    num_bytes: 1054352
    num_examples: 8000
  download_size: 1964087
  dataset_size: 1411427
---

# Dataset Card for "sem_eval_2010_task_8"

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

- **Homepage:** [https://semeval2.fbk.eu/semeval2.php?location=tasks&taskid=11](https://semeval2.fbk.eu/semeval2.php?location=tasks&taskid=11)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1.87 MB
- **Size of the generated dataset:** 1.35 MB
- **Total amount of disk used:** 3.22 MB

### Dataset Summary

The SemEval-2010 Task 8 focuses on Multi-way classification of semantic relations between pairs of nominals.
The task was designed to compare different approaches to semantic relation classification
and to provide a standard testbed for future research.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 1.87 MB
- **Size of the generated dataset:** 1.35 MB
- **Total amount of disk used:** 3.22 MB

An example of 'train' looks as follows.
```
{
    "relation": 3,
    "sentence": "The system as described above has its greatest application in an arrayed <e1>configuration</e1> of antenna <e2>elements</e2>."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `sentence`: a `string` feature.
- `relation`: a classification label, with possible values including `Cause-Effect(e1,e2)` (0), `Cause-Effect(e2,e1)` (1), `Component-Whole(e1,e2)` (2), `Component-Whole(e2,e1)` (3), `Content-Container(e1,e2)` (4).

### Data Splits

| name  |train|test|
|-------|----:|---:|
|default| 8000|2717|

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
@inproceedings{hendrickx-etal-2010-semeval,
    title = "{S}em{E}val-2010 Task 8: Multi-Way Classification of Semantic Relations between Pairs of Nominals",
    author = "Hendrickx, Iris  and
      Kim, Su Nam  and
      Kozareva, Zornitsa  and
      Nakov, Preslav  and
      {'O} S{'e}aghdha, Diarmuid  and
      Pad{'o}, Sebastian  and
      Pennacchiotti, Marco  and
      Romano, Lorenza  and
      Szpakowicz, Stan",
    booktitle = "Proceedings of the 5th International Workshop on Semantic Evaluation",
    month = jul,
    year = "2010",
    address = "Uppsala, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/S10-1006",
    pages = "33--38",
}

```


### Contributions

Thanks to [@JoelNiklaus](https://github.com/JoelNiklaus) for adding this dataset.