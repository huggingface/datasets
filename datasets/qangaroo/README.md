---
---

# Dataset Card for "qangaroo"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [http://qangaroo.cs.ucl.ac.uk/index.html](http://qangaroo.cs.ucl.ac.uk/index.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1296.40 MB
- **Size of the generated dataset:** 936.40 MB
- **Total amount of disk used:** 2232.79 MB

### [Dataset Summary](#dataset-summary)

  We have created two new Reading Comprehension datasets focussing on multi-hop (alias multi-step) inference.

Several pieces of information often jointly imply another fact. In multi-hop inference, a new fact is derived by combining facts via a chain of multiple steps.

Our aim is to build Reading Comprehension methods that perform multi-hop inference on text, where individual facts are spread out across different documents.

The two QAngaroo datasets provide a training and evaluation resource for such methods.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### masked_medhop

- **Size of downloaded dataset files:** 324.10 MB
- **Size of the generated dataset:** 107.41 MB
- **Total amount of disk used:** 431.51 MB

An example of 'validation' looks as follows.
```

```

#### masked_wikihop

- **Size of downloaded dataset files:** 324.10 MB
- **Size of the generated dataset:** 373.82 MB
- **Total amount of disk used:** 697.92 MB

An example of 'validation' looks as follows.
```

```

#### medhop

- **Size of downloaded dataset files:** 324.10 MB
- **Size of the generated dataset:** 105.30 MB
- **Total amount of disk used:** 429.40 MB

An example of 'validation' looks as follows.
```

```

#### wikihop

- **Size of downloaded dataset files:** 324.10 MB
- **Size of the generated dataset:** 349.87 MB
- **Total amount of disk used:** 673.97 MB

An example of 'validation' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### masked_medhop
- `query`: a `string` feature.
- `supports`: a `list` of `string` features.
- `candidates`: a `list` of `string` features.
- `answer`: a `string` feature.
- `id`: a `string` feature.

#### masked_wikihop
- `query`: a `string` feature.
- `supports`: a `list` of `string` features.
- `candidates`: a `list` of `string` features.
- `answer`: a `string` feature.
- `id`: a `string` feature.

#### medhop
- `query`: a `string` feature.
- `supports`: a `list` of `string` features.
- `candidates`: a `list` of `string` features.
- `answer`: a `string` feature.
- `id`: a `string` feature.

#### wikihop
- `query`: a `string` feature.
- `supports`: a `list` of `string` features.
- `candidates`: a `list` of `string` features.
- `answer`: a `string` feature.
- `id`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|     name     |train|validation|
|--------------|----:|---------:|
|masked_medhop | 1620|       342|
|masked_wikihop|43738|      5129|
|medhop        | 1620|       342|
|wikihop       |43738|      5129|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.