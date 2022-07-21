---
language:
- en
paperswithcode_id: searchqa
pretty_name: SearchQA
---

# Dataset Card for "search_qa"

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

- **Homepage:** [https://github.com/nyu-dl/dl4ir-searchQA](https://github.com/nyu-dl/dl4ir-searchQA)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6163.54 MB
- **Size of the generated dataset:** 14573.76 MB
- **Total amount of disk used:** 20737.29 MB

### Dataset Summary

We publicly release a new large-scale dataset, called SearchQA, for machine comprehension, or question-answering. Unlike recently released datasets, such as DeepMind
CNN/DailyMail and SQuAD, the proposed SearchQA was constructed to reflect a full pipeline of general question-answering. That is, we start not from an existing article
and generate a question-answer pair, but start from an existing question-answer pair, crawled from J! Archive, and augment it with text snippets retrieved by Google.
Following this approach, we built SearchQA, which consists of more than 140k question-answer pairs with each pair having 49.6 snippets on average. Each question-answer-context
 tuple of the SearchQA comes with additional meta-data such as the snippet's URL, which we believe will be valuable resources for future research. We conduct human evaluation
 as well as test two baseline methods, one simple word selection and the other deep learning based, on the SearchQA. We show that there is a meaningful gap between the human
 and machine performances. This suggests that the proposed dataset could well serve as a benchmark for question-answering.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### raw_jeopardy

- **Size of downloaded dataset files:** 3160.84 MB
- **Size of the generated dataset:** 7410.98 MB
- **Total amount of disk used:** 10571.82 MB

An example of 'train' looks as follows.
```

```

#### train_test_val

- **Size of downloaded dataset files:** 3002.69 MB
- **Size of the generated dataset:** 7162.78 MB
- **Total amount of disk used:** 10165.47 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### raw_jeopardy
- `category`: a `string` feature.
- `air_date`: a `string` feature.
- `question`: a `string` feature.
- `value`: a `string` feature.
- `answer`: a `string` feature.
- `round`: a `string` feature.
- `show_number`: a `int32` feature.
- `search_results`: a dictionary feature containing:
  - `urls`: a `string` feature.
  - `snippets`: a `string` feature.
  - `titles`: a `string` feature.
  - `related_links`: a `string` feature.

#### train_test_val
- `category`: a `string` feature.
- `air_date`: a `string` feature.
- `question`: a `string` feature.
- `value`: a `string` feature.
- `answer`: a `string` feature.
- `round`: a `string` feature.
- `show_number`: a `int32` feature.
- `search_results`: a dictionary feature containing:
  - `urls`: a `string` feature.
  - `snippets`: a `string` feature.
  - `titles`: a `string` feature.
  - `related_links`: a `string` feature.

### Data Splits

#### raw_jeopardy

|            |train |
|------------|-----:|
|raw_jeopardy|216757|

#### train_test_val

|              |train |validation|test |
|--------------|-----:|---------:|----:|
|train_test_val|151295|     21613|43228|

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

    @article{DBLP:journals/corr/DunnSHGCC17,
    author    = {Matthew Dunn and
                Levent Sagun and
                Mike Higgins and
                V. Ugur G{"{u}}ney and
                Volkan Cirik and
                Kyunghyun Cho},
    title     = {SearchQA: {A} New Q{\&}A Dataset Augmented with Context from a
                Search Engine},
    journal   = {CoRR},
    volume    = {abs/1704.05179},
    year      = {2017},
    url       = {http://arxiv.org/abs/1704.05179},
    archivePrefix = {arXiv},
    eprint    = {1704.05179},
    timestamp = {Mon, 13 Aug 2018 16:47:09 +0200},
    biburl    = {https://dblp.org/rec/journals/corr/DunnSHGCC17.bib},
    bibsource = {dblp computer science bibliography, https://dblp.org}
    }

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@mariamabarham](https://github.com/mariamabarham), [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
