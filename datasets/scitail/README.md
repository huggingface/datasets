---
language:
- en
paperswithcode_id: scitail
pretty_name: SciTail
---

# Dataset Card for "scitail"

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

- **Homepage:** [https://allenai.org/data/scitail](https://allenai.org/data/scitail)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 54.07 MB
- **Size of the generated dataset:** 46.82 MB
- **Total amount of disk used:** 100.89 MB

### Dataset Summary

The SciTail dataset is an entailment dataset created from multiple-choice science exams and web sentences. Each question
and the correct answer choice are converted into an assertive statement to form the hypothesis. We use information
retrieval to obtain relevant text from a large text corpus of web sentences, and use these sentences as a premise P. We
crowdsource the annotation of such premise-hypothesis pair as supports (entails) or not (neutral), in order to create
the SciTail dataset. The dataset contains 27,026 examples with 10,101 examples with entails label and 16,925 examples
with neutral label

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### dgem_format

- **Size of downloaded dataset files:** 13.52 MB
- **Size of the generated dataset:** 7.47 MB
- **Total amount of disk used:** 20.99 MB

An example of 'train' looks as follows.
```

```

#### predictor_format

- **Size of downloaded dataset files:** 13.52 MB
- **Size of the generated dataset:** 9.72 MB
- **Total amount of disk used:** 23.24 MB

An example of 'validation' looks as follows.
```

```

#### snli_format

- **Size of downloaded dataset files:** 13.52 MB
- **Size of the generated dataset:** 24.58 MB
- **Total amount of disk used:** 38.10 MB

An example of 'validation' looks as follows.
```

```

#### tsv_format

- **Size of downloaded dataset files:** 13.52 MB
- **Size of the generated dataset:** 5.05 MB
- **Total amount of disk used:** 18.56 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### dgem_format
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a `string` feature.
- `hypothesis_graph_structure`: a `string` feature.

#### predictor_format
- `answer`: a `string` feature.
- `sentence2_structure`: a `string` feature.
- `sentence1`: a `string` feature.
- `sentence2`: a `string` feature.
- `gold_label`: a `string` feature.
- `question`: a `string` feature.

#### snli_format
- `sentence1_binary_parse`: a `string` feature.
- `sentence1_parse`: a `string` feature.
- `sentence1`: a `string` feature.
- `sentence2_parse`: a `string` feature.
- `sentence2`: a `string` feature.
- `annotator_labels`: a `list` of `string` features.
- `gold_label`: a `string` feature.

#### tsv_format
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a `string` feature.

### Data Splits

|      name      |train|validation|test|
|----------------|----:|---------:|---:|
|dgem_format     |23088|      1304|2126|
|predictor_format|23587|      1304|2126|
|snli_format     |23596|      1304|2126|
|tsv_format      |23097|      1304|2126|

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
inproceedings{scitail,
     Author = {Tushar Khot and Ashish Sabharwal and Peter Clark},
     Booktitle = {AAAI},
     Title = {{SciTail}: A Textual Entailment Dataset from Science Question Answering},
     Year = {2018}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
