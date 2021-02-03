---
---

# Dataset Card for "qanta"

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

- **Homepage:** [http://www.qanta.org/](http://www.qanta.org/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 162.84 MB
- **Size of the generated dataset:** 140.36 MB
- **Total amount of disk used:** 303.20 MB

### [Dataset Summary](#dataset-summary)

The Qanta dataset is a question answering dataset based on the academic trivia game Quizbowl.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### mode=first,char_skip=25

- **Size of downloaded dataset files:** 162.84 MB
- **Size of the generated dataset:** 140.36 MB
- **Total amount of disk used:** 303.20 MB

An example of 'guessdev' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "Apollo_program",
    "category": "History",
    "char_idx": -1,
    "dataset": "quizdb.org",
    "difficulty": "easy_college",
    "first_sentence": "As part of this program, William Anders took a photo that Galen Rowell called \"the most influential environmental photograph ever taken.\"",
    "fold": "guessdev",
    "full_question": "\"As part of this program, William Anders took a photo that Galen Rowell called \\\"the most influential environmental photograph e...",
    "gameplay": false,
    "id": "127028-first",
    "page": "Apollo_program",
    "proto_id": "",
    "qanta_id": 127028,
    "qdb_id": 126689,
    "raw_answer": "Apollo program [or Project Apollo; accept Apollo 8; accept Apollo 1; accept Apollo 11; prompt on landing on the moon]",
    "sentence_idx": -1,
    "subcategory": "American",
    "text": "As part of this program, William Anders took a photo that Galen Rowell called \"the most influential environmental photograph ever taken.\"",
    "tokenizations": [[0, 137], [138, 281], [282, 412], [413, 592], [593, 675]],
    "tournament": "ACF Fall",
    "year": 2016
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### mode=first,char_skip=25
- `id`: a `string` feature.
- `qanta_id`: a `int32` feature.
- `proto_id`: a `string` feature.
- `qdb_id`: a `int32` feature.
- `dataset`: a `string` feature.
- `text`: a `string` feature.
- `full_question`: a `string` feature.
- `first_sentence`: a `string` feature.
- `char_idx`: a `int32` feature.
- `sentence_idx`: a `int32` feature.
- `tokenizations`: a dictionary feature containing:
  - `feature`: a `int32` feature.
- `answer`: a `string` feature.
- `page`: a `string` feature.
- `raw_answer`: a `string` feature.
- `fold`: a `string` feature.
- `gameplay`: a `bool` feature.
- `category`: a `string` feature.
- `subcategory`: a `string` feature.
- `tournament`: a `string` feature.
- `difficulty`: a `string` feature.
- `year`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|         name          |adversarial|buzzdev|buzztrain|guessdev|guesstrain|buzztest|guesstest|
|-----------------------|----------:|------:|--------:|-------:|---------:|-------:|--------:|
|mode=first,char_skip=25|       1145|   1161|    16706|    1055|     96221|    1953|     2151|

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

@article{Rodriguez2019QuizbowlTC,
  title={Quizbowl: The Case for Incremental Question Answering},
  author={Pedro Rodriguez and Shi Feng and Mohit Iyyer and He He and Jordan L. Boyd-Graber},
  journal={ArXiv},
  year={2019},
  volume={abs/1904.04792}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.