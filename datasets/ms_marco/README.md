---
---

# Dataset Card for "ms_marco"

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

- **Homepage:** [https://microsoft.github.io/msmarco/](https://microsoft.github.io/msmarco/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1481.03 MB
- **Size of the generated dataset:** 4503.32 MB
- **Total amount of disk used:** 5984.34 MB

### [Dataset Summary](#dataset-summary)

Starting with a paper released at NIPS 2016, MS MARCO is a collection of datasets focused on deep learning in search.

The first dataset was a question answering dataset featuring 100,000 real Bing questions and a human generated answer.
Since then we released a 1,000,000 question dataset, a natural langauge generation dataset, a passage ranking dataset,
keyphrase extraction dataset, crawling dataset, and a conversational search.

There have been 277 submissions. 20 KeyPhrase Extraction submissions, 87 passage ranking submissions, 0 document ranking
submissions, 73 QnA V2 submissions, 82 NLGEN submisions, and 15 QnA V1 submissions

This data comes in three tasks/forms: Original QnA dataset(v1.1), Question Answering(v2.1), Natural Language Generation(v2.1).

The original question answering datset featured 100,000 examples and was released in 2016. Leaderboard is now closed but data is availible below.

The current competitive tasks are Question Answering and Natural Language Generation. Question Answering features over 1,000,000 queries and
is much like the original QnA dataset but bigger and with higher quality. The Natural Language Generation dataset features 180,000 examples and
builds upon the QnA dataset to deliver answers that could be spoken by a smart speaker.

version v1.1

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### v1.1

- **Size of downloaded dataset files:** 160.88 MB
- **Size of the generated dataset:** 414.48 MB
- **Total amount of disk used:** 575.36 MB

An example of 'train' looks as follows.
```

```

#### v2.1

- **Size of downloaded dataset files:** 1320.14 MB
- **Size of the generated dataset:** 4088.84 MB
- **Total amount of disk used:** 5408.98 MB

An example of 'validation' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### v1.1
- `answers`: a `list` of `string` features.
- `passages`: a dictionary feature containing:
  - `is_selected`: a `int32` feature.
  - `passage_text`: a `string` feature.
  - `url`: a `string` feature.
- `query`: a `string` feature.
- `query_id`: a `int32` feature.
- `query_type`: a `string` feature.
- `wellFormedAnswers`: a `list` of `string` features.

#### v2.1
- `answers`: a `list` of `string` features.
- `passages`: a dictionary feature containing:
  - `is_selected`: a `int32` feature.
  - `passage_text`: a `string` feature.
  - `url`: a `string` feature.
- `query`: a `string` feature.
- `query_id`: a `int32` feature.
- `query_type`: a `string` feature.
- `wellFormedAnswers`: a `list` of `string` features.

### [Data Splits Sample Size](#data-splits-sample-size)

|name|train |validation| test |
|----|-----:|---------:|-----:|
|v1.1| 82326|     10047|  9650|
|v2.1|808731|    101093|101092|

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

@article{DBLP:journals/corr/NguyenRSGTMD16,
  author    = {Tri Nguyen and
               Mir Rosenberg and
               Xia Song and
               Jianfeng Gao and
               Saurabh Tiwary and
               Rangan Majumder and
               Li Deng},
  title     = {{MS} {MARCO:} {A} Human Generated MAchine Reading COmprehension Dataset},
  journal   = {CoRR},
  volume    = {abs/1611.09268},
  year      = {2016},
  url       = {http://arxiv.org/abs/1611.09268},
  archivePrefix = {arXiv},
  eprint    = {1611.09268},
  timestamp = {Mon, 13 Aug 2018 16:49:03 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/NguyenRSGTMD16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
}

```


### Contributions

Thanks to [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun) for adding this dataset.