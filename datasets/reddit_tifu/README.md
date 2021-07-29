---
languages:
- en
paperswithcode_id: reddit-tifu
---

# Dataset Card for "reddit_tifu"

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

- **Homepage:** [https://github.com/ctr4si/MMN](https://github.com/ctr4si/MMN)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1279.08 MB
- **Size of the generated dataset:** 219.12 MB
- **Total amount of disk used:** 1498.20 MB

### Dataset Summary

Reddit dataset, where TIFU denotes the name of subbreddit /r/tifu.
As defined in the publication, styel "short" uses title as summary and
"long" uses tldr as summary.

Features includes:
  - document: post text without tldr.
  - tldr: tldr line.
  - title: trimmed title without tldr.
  - ups: upvotes.
  - score: score.
  - num_comments: number of comments.
  - upvote_ratio: upvote ratio.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### long

- **Size of downloaded dataset files:** 639.54 MB
- **Size of the generated dataset:** 87.74 MB
- **Total amount of disk used:** 727.29 MB

An example of 'train' looks as follows.
```

```

#### short

- **Size of downloaded dataset files:** 639.54 MB
- **Size of the generated dataset:** 131.37 MB
- **Total amount of disk used:** 770.92 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### long
- `ups`: a `float32` feature.
- `num_comments`: a `float32` feature.
- `upvote_ratio`: a `float32` feature.
- `score`: a `float32` feature.
- `documents`: a `string` feature.
- `tldr`: a `string` feature.
- `title`: a `string` feature.

#### short
- `ups`: a `float32` feature.
- `num_comments`: a `float32` feature.
- `upvote_ratio`: a `float32` feature.
- `score`: a `float32` feature.
- `documents`: a `string` feature.
- `tldr`: a `string` feature.
- `title`: a `string` feature.

### Data Splits

|name |train|
|-----|----:|
|long |42139|
|short|79740|

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

@misc{kim2018abstractive,
    title={Abstractive Summarization of Reddit Posts with Multi-level Memory Networks},
    author={Byeongchang Kim and Hyunwoo Kim and Gunhee Kim},
    year={2018},
    eprint={1811.00783},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.