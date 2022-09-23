---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- et
- ht
- id
- it
- qu
- sw
- ta
- th
- tr
- vi
- zh
license:
- cc-by-4.0
multilinguality:
- multilingual
pretty_name: XCOPA
size_categories:
- unknown
source_datasets:
- extended|copa
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: xcopa
dataset_info:
- config_name: et
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 56613
    num_examples: 500
  - name: validation
    num_bytes: 11711
    num_examples: 100
  download_size: 116432
  dataset_size: 68324
- config_name: ht
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 58579
    num_examples: 500
  - name: validation
    num_bytes: 11999
    num_examples: 100
  download_size: 118677
  dataset_size: 70578
- config_name: it
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 65051
    num_examples: 500
  - name: validation
    num_bytes: 13366
    num_examples: 100
  download_size: 126520
  dataset_size: 78417
- config_name: id
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 63331
    num_examples: 500
  - name: validation
    num_bytes: 13897
    num_examples: 100
  download_size: 125347
  dataset_size: 77228
- config_name: qu
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 68711
    num_examples: 500
  - name: validation
    num_bytes: 13983
    num_examples: 100
  download_size: 130786
  dataset_size: 82694
- config_name: sw
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 60675
    num_examples: 500
  - name: validation
    num_bytes: 12708
    num_examples: 100
  download_size: 121497
  dataset_size: 73383
- config_name: zh
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 55276
    num_examples: 500
  - name: validation
    num_bytes: 11646
    num_examples: 100
  download_size: 115021
  dataset_size: 66922
- config_name: ta
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 176254
    num_examples: 500
  - name: validation
    num_bytes: 37037
    num_examples: 100
  download_size: 261404
  dataset_size: 213291
- config_name: th
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 104165
    num_examples: 500
  - name: validation
    num_bytes: 21859
    num_examples: 100
  download_size: 174134
  dataset_size: 126024
- config_name: tr
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 57741
    num_examples: 500
  - name: validation
    num_bytes: 11941
    num_examples: 100
  download_size: 117781
  dataset_size: 69682
- config_name: vi
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 70311
    num_examples: 500
  - name: validation
    num_bytes: 15135
    num_examples: 100
  download_size: 133555
  dataset_size: 85446
- config_name: translation-et
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 57469
    num_examples: 500
  - name: validation
    num_bytes: 11923
    num_examples: 100
  download_size: 116900
  dataset_size: 69392
- config_name: translation-ht
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 58161
    num_examples: 500
  - name: validation
    num_bytes: 12172
    num_examples: 100
  download_size: 117847
  dataset_size: 70333
- config_name: translation-it
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 59078
    num_examples: 500
  - name: validation
    num_bytes: 12424
    num_examples: 100
  download_size: 119605
  dataset_size: 71502
- config_name: translation-id
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 58548
    num_examples: 500
  - name: validation
    num_bytes: 12499
    num_examples: 100
  download_size: 118566
  dataset_size: 71047
- config_name: translation-sw
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 58749
    num_examples: 500
  - name: validation
    num_bytes: 12222
    num_examples: 100
  download_size: 118485
  dataset_size: 70971
- config_name: translation-zh
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 58037
    num_examples: 500
  - name: validation
    num_bytes: 12043
    num_examples: 100
  download_size: 117582
  dataset_size: 70080
- config_name: translation-ta
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 59584
    num_examples: 500
  - name: validation
    num_bytes: 12414
    num_examples: 100
  download_size: 119511
  dataset_size: 71998
- config_name: translation-th
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 54900
    num_examples: 500
  - name: validation
    num_bytes: 11389
    num_examples: 100
  download_size: 113799
  dataset_size: 66289
- config_name: translation-tr
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 57741
    num_examples: 500
  - name: validation
    num_bytes: 11921
    num_examples: 100
  download_size: 117161
  dataset_size: 69662
- config_name: translation-vi
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  - name: idx
    dtype: int32
  - name: changed
    dtype: bool
  splits:
  - name: test
    num_bytes: 55939
    num_examples: 500
  - name: validation
    num_bytes: 11646
    num_examples: 100
  download_size: 115094
  dataset_size: 67585
---

# Dataset Card for "xcopa"

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

- **Homepage:** [https://github.com/cambridgeltl/xcopa](https://github.com/cambridgeltl/xcopa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3.89 MB
- **Size of the generated dataset:** 0.97 MB
- **Total amount of disk used:** 4.86 MB

### Dataset Summary

  XCOPA: A Multilingual Dataset for Causal Commonsense Reasoning
The Cross-lingual Choice of Plausible Alternatives dataset is a benchmark to evaluate the ability of machine learning models to transfer commonsense reasoning across
languages. The dataset is the translation and reannotation of the English COPA (Roemmele et al. 2011) and covers 11 languages from 11 families and several areas around
the globe. The dataset is challenging as it requires both the command of world knowledge and the ability to generalise to new languages. All the details about the
creation of XCOPA and the implementation of the baselines are available in the paper.

Xcopa language et

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

- et
- ht
- id
- it
- qu
- sw
- ta
- th
- tr
- vi
- zh

## Dataset Structure

### Data Instances

#### et

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.42 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### ht

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.42 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### id

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### it

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.08 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

#### qu

- **Size of downloaded dataset files:** 0.35 MB
- **Size of the generated dataset:** 0.08 MB
- **Total amount of disk used:** 0.43 MB

An example of 'validation' looks as follows.
```
{
    "changed": false,
    "choice1": "Ta kallas piima kaussi.",
    "choice2": "Ta kaotas oma isu.",
    "idx": 1,
    "label": 1,
    "premise": "Tüdruk leidis oma helveste seest putuka.",
    "question": "effect"
}
```

### Data Fields

The data fields are the same among all splits.

#### et
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### ht
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### id
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### it
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

#### qu
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.
- `idx`: a `int32` feature.
- `changed`: a `bool` feature.

### Data Splits

|name|validation|test|
|----|---------:|---:|
|et  |       100| 500|
|ht  |       100| 500|
|id  |       100| 500|
|it  |       100| 500|
|qu  |       100| 500|

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

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
  @article{ponti2020xcopa,
  title={{XCOPA: A} Multilingual Dataset for Causal Commonsense Reasoning},
  author={Edoardo M. Ponti, Goran Glava{s}, Olga Majewska, Qianchu Liu, Ivan Vuli'{c} and Anna Korhonen},
  journal={arXiv preprint},
  year={2020},
  url={https://ducdauge.github.io/files/xcopa.pdf}
}

@inproceedings{roemmele2011choice,
  title={Choice of plausible alternatives: An evaluation of commonsense causal reasoning},
  author={Roemmele, Melissa and Bejan, Cosmin Adrian and Gordon, Andrew S},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2011},
  url={https://people.ict.usc.edu/~gordon/publications/AAAI-SPRING11A.PDF},
}

```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.