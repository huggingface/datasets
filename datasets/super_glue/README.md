---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- other
license:
- unknown
multilinguality:
- monolingual
paperswithcode_id: superglue
pretty_name: SuperGLUE
size_categories:
- 10K<n<100K
source_datasets:
- extended|other
tags:
- superglue
- NLU
- natural language understanding
task_categories:
- text-classification
- token-classification
- question-answering
task_ids:
- natural-language-inference
- word-sense-disambiguation
- coreference-resolution
- extractive-qa
dataset_info:
- config_name: boolq
  features:
  - name: question
    dtype: string
  - name: passage
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  splits:
  - name: test
    num_bytes: 2107997
    num_examples: 3245
  - name: train
    num_bytes: 6179206
    num_examples: 9427
  - name: validation
    num_bytes: 2118505
    num_examples: 3270
  download_size: 4118001
  dataset_size: 10405708
- config_name: cb
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: contradiction
          2: neutral
  splits:
  - name: test
    num_bytes: 93660
    num_examples: 250
  - name: train
    num_bytes: 87218
    num_examples: 250
  - name: validation
    num_bytes: 21894
    num_examples: 56
  download_size: 75482
  dataset_size: 202772
- config_name: copa
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: choice1
          1: choice2
  splits:
  - name: test
    num_bytes: 60303
    num_examples: 500
  - name: train
    num_bytes: 49599
    num_examples: 400
  - name: validation
    num_bytes: 12586
    num_examples: 100
  download_size: 43986
  dataset_size: 122488
- config_name: multirc
  features:
  - name: paragraph
    dtype: string
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: idx
    struct:
    - name: paragraph
      dtype: int32
    - name: question
      dtype: int32
    - name: answer
      dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  splits:
  - name: test
    num_bytes: 14996451
    num_examples: 9693
  - name: train
    num_bytes: 46213579
    num_examples: 27243
  - name: validation
    num_bytes: 7758918
    num_examples: 4848
  download_size: 1116225
  dataset_size: 68968948
- config_name: record
  features:
  - name: passage
    dtype: string
  - name: query
    dtype: string
  - name: entities
    sequence: string
  - name: entity_spans
    sequence:
    - name: text
      dtype: string
    - name: start
      dtype: int32
    - name: end
      dtype: int32
  - name: answers
    sequence: string
  - name: idx
    struct:
    - name: passage
      dtype: int32
    - name: query
      dtype: int32
  splits:
  - name: test
    num_bytes: 17200575
    num_examples: 10000
  - name: train
    num_bytes: 179232052
    num_examples: 100730
  - name: validation
    num_bytes: 17479084
    num_examples: 10000
  download_size: 51757880
  dataset_size: 213911711
- config_name: rte
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: not_entailment
  splits:
  - name: test
    num_bytes: 975799
    num_examples: 3000
  - name: train
    num_bytes: 848745
    num_examples: 2490
  - name: validation
    num_bytes: 90899
    num_examples: 277
  download_size: 750920
  dataset_size: 1915443
- config_name: wic
  features:
  - name: word
    dtype: string
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: start1
    dtype: int32
  - name: start2
    dtype: int32
  - name: end1
    dtype: int32
  - name: end2
    dtype: int32
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  splits:
  - name: test
    num_bytes: 180593
    num_examples: 1400
  - name: train
    num_bytes: 665183
    num_examples: 5428
  - name: validation
    num_bytes: 82623
    num_examples: 638
  download_size: 396213
  dataset_size: 928399
- config_name: wsc
  features:
  - name: text
    dtype: string
  - name: span1_index
    dtype: int32
  - name: span2_index
    dtype: int32
  - name: span1_text
    dtype: string
  - name: span2_text
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  splits:
  - name: test
    num_bytes: 31572
    num_examples: 146
  - name: train
    num_bytes: 89883
    num_examples: 554
  - name: validation
    num_bytes: 21637
    num_examples: 104
  download_size: 32751
  dataset_size: 143092
- config_name: wsc.fixed
  features:
  - name: text
    dtype: string
  - name: span1_index
    dtype: int32
  - name: span2_index
    dtype: int32
  - name: span1_text
    dtype: string
  - name: span2_text
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  splits:
  - name: test
    num_bytes: 31568
    num_examples: 146
  - name: train
    num_bytes: 89883
    num_examples: 554
  - name: validation
    num_bytes: 21637
    num_examples: 104
  download_size: 32751
  dataset_size: 143088
- config_name: axb
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: not_entailment
  splits:
  - name: test
    num_bytes: 238392
    num_examples: 1104
  download_size: 33950
  dataset_size: 238392
- config_name: axg
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: idx
    dtype: int32
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: not_entailment
  splits:
  - name: test
    num_bytes: 53581
    num_examples: 356
  download_size: 10413
  dataset_size: 53581
---

# Dataset Card for "super_glue"

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

- **Homepage:** [https://github.com/google-research-datasets/boolean-questions](https://github.com/google-research-datasets/boolean-questions)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 55.66 MB
- **Size of the generated dataset:** 238.01 MB
- **Total amount of disk used:** 293.67 MB

### Dataset Summary

SuperGLUE (https://super.gluebenchmark.com/) is a new benchmark styled after
GLUE with a new set of more difficult language understanding tasks, improved
resources, and a new public leaderboard.

BoolQ (Boolean Questions, Clark et al., 2019a) is a QA task where each example consists of a short
passage and a yes/no question about the passage. The questions are provided anonymously and
unsolicited by users of the Google search engine, and afterwards paired with a paragraph from a
Wikipedia article containing the answer. Following the original work, we evaluate with accuracy.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### axb

- **Size of downloaded dataset files:** 0.03 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.26 MB

An example of 'test' looks as follows.
```

```

#### axg

- **Size of downloaded dataset files:** 0.01 MB
- **Size of the generated dataset:** 0.05 MB
- **Total amount of disk used:** 0.06 MB

An example of 'test' looks as follows.
```

```

#### boolq

- **Size of downloaded dataset files:** 3.93 MB
- **Size of the generated dataset:** 9.92 MB
- **Total amount of disk used:** 13.85 MB

An example of 'train' looks as follows.
```

```

#### cb

- **Size of downloaded dataset files:** 0.07 MB
- **Size of the generated dataset:** 0.19 MB
- **Total amount of disk used:** 0.27 MB

An example of 'train' looks as follows.
```

```

#### copa

- **Size of downloaded dataset files:** 0.04 MB
- **Size of the generated dataset:** 0.12 MB
- **Total amount of disk used:** 0.16 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### axb
- `sentence1`: a `string` feature.
- `sentence2`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `not_entailment` (1).

#### axg
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `not_entailment` (1).

#### boolq
- `question`: a `string` feature.
- `passage`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `False` (0), `True` (1).

#### cb
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `contradiction` (1), `neutral` (2).

#### copa
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `choice1` (0), `choice2` (1).

### Data Splits

#### axb

|   |test|
|---|---:|
|axb|1104|

#### axg

|   |test|
|---|---:|
|axg| 356|

#### boolq

|     |train|validation|test|
|-----|----:|---------:|---:|
|boolq| 9427|      3270|3245|

#### cb

|   |train|validation|test|
|---|----:|---------:|---:|
|cb |  250|        56| 250|

#### copa

|    |train|validation|test|
|----|----:|---------:|---:|
|copa|  400|       100| 500|

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
@inproceedings{clark2019boolq,
  title={BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions},
  author={Clark, Christopher and Lee, Kenton and Chang, Ming-Wei, and Kwiatkowski, Tom and Collins, Michael, and Toutanova, Kristina},
  booktitle={NAACL},
  year={2019}
}
@article{wang2019superglue,
  title={SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}

Note that each SuperGLUE dataset has its own citation. Please see the source to
get the correct citation for each contained dataset.

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.