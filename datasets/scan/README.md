---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- en
license:
- bsd
multilinguality:
- monolingual
pretty_name: SCAN
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- other-multi-turn
paperswithcode_id: scan
configs:
- addprim_jump
- addprim_turn_left
- filler_num0
- filler_num1
- filler_num2
- filler_num3
- length
- simple
- template_around_right
- template_jump_around_right
- template_opposite_right
- template_right
---

# Dataset Card for "scan"

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

- **Homepage:** [https://github.com/brendenlake/SCAN](https://github.com/brendenlake/SCAN)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 213.79 MB
- **Size of the generated dataset:** 42.47 MB
- **Total amount of disk used:** 256.26 MB

### Dataset Summary

SCAN tasks with various splits.

SCAN is a set of simple language-driven navigation tasks for studying
compositional learning and zero-shot generalization.

See https://github.com/brendenlake/SCAN for a description of the splits.

Example usage:
data = datasets.load_dataset('scan/length')

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### addprim_jump

- **Size of downloaded dataset files:** 17.82 MB
- **Size of the generated dataset:** 3.86 MB
- **Total amount of disk used:** 21.68 MB

An example of 'train' looks as follows.
```

```

#### addprim_turn_left

- **Size of downloaded dataset files:** 17.82 MB
- **Size of the generated dataset:** 3.90 MB
- **Total amount of disk used:** 21.71 MB

An example of 'train' looks as follows.
```

```

#### filler_num0

- **Size of downloaded dataset files:** 17.82 MB
- **Size of the generated dataset:** 2.72 MB
- **Total amount of disk used:** 20.53 MB

An example of 'train' looks as follows.
```

```

#### filler_num1

- **Size of downloaded dataset files:** 17.82 MB
- **Size of the generated dataset:** 2.99 MB
- **Total amount of disk used:** 20.81 MB

An example of 'train' looks as follows.
```

```

#### filler_num2

- **Size of downloaded dataset files:** 17.82 MB
- **Size of the generated dataset:** 3.28 MB
- **Total amount of disk used:** 21.10 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### addprim_jump
- `commands`: a `string` feature.
- `actions`: a `string` feature.

#### addprim_turn_left
- `commands`: a `string` feature.
- `actions`: a `string` feature.

#### filler_num0
- `commands`: a `string` feature.
- `actions`: a `string` feature.

#### filler_num1
- `commands`: a `string` feature.
- `actions`: a `string` feature.

#### filler_num2
- `commands`: a `string` feature.
- `actions`: a `string` feature.

### Data Splits

|      name       |train|test|
|-----------------|----:|---:|
|addprim_jump     |14670|7706|
|addprim_turn_left|21890|1208|
|filler_num0      |15225|1173|
|filler_num1      |16290|1173|
|filler_num2      |17391|1173|

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
@inproceedings{Lake2018GeneralizationWS,
  title={Generalization without Systematicity: On the Compositional Skills of
         Sequence-to-Sequence Recurrent Networks},
  author={Brenden M. Lake and Marco Baroni},
  booktitle={ICML},
  year={2018},
  url={https://arxiv.org/pdf/1711.00350.pdf},
}
```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
