---
---

# Dataset Card for "newsroom"

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

- **Homepage:** [https://summari.es](https://summari.es)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 5057.49 MB
- **Total amount of disk used:** 5057.49 MB

### [Dataset Summary](#dataset-summary)

NEWSROOM is a large dataset for training and evaluating summarization systems.
It contains 1.3 million articles and summaries written by authors and
editors in the newsrooms of 38 major publications.

Dataset features includes:
  - text: Input news text.
  - summary: Summary for the news.
And additional features:
  - title: news title.
  - url: url of the news.
  - date: date of the article.
  - density: extractive density.
  - coverage: extractive coverage.
  - compression: compression ratio.
  - density_bin: low, medium, high.
  - coverage_bin: extractive, abstractive.
  - compression_bin: low, medium, high.

This dataset can be downloaded upon requests. Unzip all the contents
"train.jsonl, dev.josnl, test.jsonl" to the tfds folder.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 5057.49 MB
- **Total amount of disk used:** 5057.49 MB

An example of 'train' looks as follows.
```
{
    "compression": 33.880001068115234,
    "compression_bin": "medium",
    "coverage": 1.0,
    "coverage_bin": "high",
    "date": "200600000",
    "density": 11.720000267028809,
    "density_bin": "extractive",
    "summary": "some summary 1",
    "text": "some text 1",
    "title": "news title 1",
    "url": "url.html"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `title`: a `string` feature.
- `url`: a `string` feature.
- `date`: a `string` feature.
- `density_bin`: a `string` feature.
- `coverage_bin`: a `string` feature.
- `compression_bin`: a `string` feature.
- `density`: a `float32` feature.
- `coverage`: a `float32` feature.
- `compression`: a `float32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train |validation| test |
|-------|-----:|---------:|-----:|
|default|995041|    108837|108862|

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

@inproceedings{N18-1065,
  author    = {Grusky, Max and Naaman, Mor and Artzi, Yoav},
  title     = {NEWSROOM: A Dataset of 1.3 Million Summaries
               with Diverse Extractive Strategies},
  booktitle = {Proceedings of the 2018 Conference of the
               North American Chapter of the Association for
               Computational Linguistics: Human Language Technologies},
  year      = {2018},
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@yoavartzi](https://github.com/yoavartzi), [@thomwolf](https://github.com/thomwolf) for adding this dataset.