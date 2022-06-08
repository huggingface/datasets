---
paperswithcode_id: coarse-discourse
pretty_name: Coarse Discourse
---

# Dataset Card for "coarse_discourse"

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

- **Homepage:** [https://github.com/google-research-datasets/coarse-discourse](https://github.com/google-research-datasets/coarse-discourse)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4.42 MB
- **Size of the generated dataset:** 43.34 MB
- **Total amount of disk used:** 47.76 MB

### Dataset Summary

dataset contains discourse annotation and relation on threads from reddit during 2016

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 4.42 MB
- **Size of the generated dataset:** 43.34 MB
- **Total amount of disk used:** 47.76 MB

An example of 'train' looks as follows.
```
{
    "annotations": {
        "annotator": ["fc96a15ab87f02dd1998ff55a64f6478", "e9e4b3ab355135fa954badcc06bfccc6", "31ac59c1734c1547d4d0723ff254c247"],
        "link_to_post": ["", "", ""],
        "main_type": ["elaboration", "elaboration", "elaboration"]
    },
    "id_post": "t1_c9b30i1",
    "in_reply_to": "t1_c9b2nyd",
    "is_first_post": false,
    "is_self_post": true,
    "majority_link": "t1_c9b2nyd",
    "majority_type": "elaboration",
    "post_depth": 2,
    "subreddit": "100movies365days",
    "title": "DTX120: #87 - Nashville",
    "url": "https://www.reddit.com/r/100movies365days/comments/1bx6qw/dtx120_87_nashville/"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `title`: a `string` feature.
- `is_self_post`: a `bool` feature.
- `subreddit`: a `string` feature.
- `url`: a `string` feature.
- `majority_link`: a `string` feature.
- `is_first_post`: a `bool` feature.
- `majority_type`: a `string` feature.
- `id_post`: a `string` feature.
- `post_depth`: a `int32` feature.
- `in_reply_to`: a `string` feature.
- `annotations`: a dictionary feature containing:
  - `annotator`: a `string` feature.
  - `link_to_post`: a `string` feature.
  - `main_type`: a `string` feature.

### Data Splits

| name  |train |
|-------|-----:|
|default|116357|

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
@inproceedings{coarsediscourse, title={Characterizing Online Discussion Using Coarse Discourse Sequences}, author={Zhang, Amy X. and Culbertson, Bryan and Paritosh, Praveen}, booktitle={Proceedings of the 11th International AAAI Conference on Weblogs and Social Media}, series={ICWSM '17}, year={2017}, location = {Montreal, Canada} }

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@jplu](https://github.com/jplu) for adding this dataset.
