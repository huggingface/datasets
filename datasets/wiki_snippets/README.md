---
---

# Dataset Card for "wiki_snippets"

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

- **Homepage:** [https://dumps.wikimedia.org](https://dumps.wikimedia.org)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 35001.08 MB
- **Total amount of disk used:** 35001.08 MB

### [Dataset Summary](#dataset-summary)

Wikipedia version split into plain text snippets for dense semantic indexing.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### wiki40b_en_100_0

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 12268.10 MB
- **Total amount of disk used:** 12268.10 MB

An example of 'train' looks as follows.
```

```

#### wikipedia_en_100_0

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 22732.97 MB
- **Total amount of disk used:** 22732.97 MB

An example of 'train' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### wiki40b_en_100_0
- `_id`: a `string` feature.
- `datasets_id`: a `int32` feature.
- `wiki_id`: a `string` feature.
- `start_paragraph`: a `int32` feature.
- `start_character`: a `int32` feature.
- `end_paragraph`: a `int32` feature.
- `end_character`: a `int32` feature.
- `article_title`: a `string` feature.
- `section_title`: a `string` feature.
- `passage_text`: a `string` feature.

#### wikipedia_en_100_0
- `_id`: a `string` feature.
- `datasets_id`: a `int32` feature.
- `wiki_id`: a `string` feature.
- `start_paragraph`: a `int32` feature.
- `start_character`: a `int32` feature.
- `end_paragraph`: a `int32` feature.
- `end_character`: a `int32` feature.
- `article_title`: a `string` feature.
- `section_title`: a `string` feature.
- `passage_text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|       name       | train  |
|------------------|-------:|
|wiki40b_en_100_0  |17553713|
|wikipedia_en_100_0|30820408|

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
@ONLINE {wikidump,
    author = "Wikimedia Foundation",
    title  = "Wikimedia Downloads",
    url    = "https://dumps.wikimedia.org"
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham), [@yjernite](https://github.com/yjernite) for adding this dataset.