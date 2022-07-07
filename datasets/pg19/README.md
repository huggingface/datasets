---
language:
- en
paperswithcode_id: pg-19
pretty_name: PG-19
---

# Dataset Card for "pg19"

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

- **Homepage:** [https://github.com/deepmind/pg19](https://github.com/deepmind/pg19)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 11196.60 MB
- **Size of the generated dataset:** 10978.29 MB
- **Total amount of disk used:** 22174.89 MB

### Dataset Summary

This repository contains the PG-19 language modeling benchmark.
It includes a set of books extracted from the Project Gutenberg books library, that were published before 1919.
It also contains metadata of book titles and publication dates.

PG-19 is over double the size of the Billion Word benchmark and contains documents that are 20X longer, on average, than the WikiText long-range language modelling benchmark.
Books are partitioned into a train, validation, and test set. Book metadata is stored in metadata.csv which contains (book_id, short_book_title, publication_date).

Unlike prior benchmarks, we do not constrain the vocabulary size --- i.e. mapping rare words to an UNK token --- but instead release the data as an open-vocabulary benchmark. The only processing of the text that has been applied is the removal of boilerplate license text, and the mapping of offensive discriminatory words as specified by Ofcom to placeholder tokens. Users are free to model the data at the character-level, subword-level, or via any mechanism that can model an arbitrary string of text.
To compare models we propose to continue measuring the word-level perplexity, by calculating the total likelihood of the dataset (via any chosen subword vocabulary or character-based scheme) divided by the number of tokens --- specified below in the dataset statistics table.
One could use this dataset for benchmarking long-range language models, or use it to pre-train for other natural language processing tasks which require long-range reasoning, such as LAMBADA or NarrativeQA. We would not recommend using this dataset to train a general-purpose language model, e.g. for applications to a production-system dialogue agent, due to the dated linguistic style of old texts and the inherent biases present in historical writing.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 11196.60 MB
- **Size of the generated dataset:** 10978.29 MB
- **Total amount of disk used:** 22174.89 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "publication_date": 1907,
    "short_book_title": "La Fiammetta by Giovanni Boccaccio",
    "text": "\"\\n\\n\\n\\nProduced by Ted Garvin, Dave Morgan and PG Distributed Proofreaders\\n\\n\\n\\n\\nLA FIAMMETTA\\n\\nBY\\n\\nGIOVANNI BOCCACCIO\\n...",
    "url": "http://www.gutenberg.org/ebooks/10006"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `short_book_title`: a `string` feature.
- `publication_date`: a `int32` feature.
- `url`: a `string` feature.
- `text`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|28602|        50| 100|

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
@article{raecompressive2019,
  author = {Rae, Jack W and Potapenko, Anna and Jayakumar, Siddhant M and
            Hillier, Chloe and Lillicrap, Timothy P},
  title = {Compressive Transformers for Long-Range Sequence Modelling},
  journal = {arXiv preprint},
  url = {https://arxiv.org/abs/1911.05507},
  year = {2019},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@lucidrains](https://github.com/lucidrains), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
