---
annotations_creators:
- machine-generated
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: Quizbowl
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-quizbowl
paperswithcode_id: quizbowl
dataset_info:
  features:
  - name: id
    dtype: string
  - name: qanta_id
    dtype: int32
  - name: proto_id
    dtype: string
  - name: qdb_id
    dtype: int32
  - name: dataset
    dtype: string
  - name: text
    dtype: string
  - name: full_question
    dtype: string
  - name: first_sentence
    dtype: string
  - name: char_idx
    dtype: int32
  - name: sentence_idx
    dtype: int32
  - name: tokenizations
    sequence:
      sequence: int32
      length: 2
  - name: answer
    dtype: string
  - name: page
    dtype: string
  - name: raw_answer
    dtype: string
  - name: fold
    dtype: string
  - name: gameplay
    dtype: bool
  - name: category
    dtype: string
  - name: subcategory
    dtype: string
  - name: tournament
    dtype: string
  - name: difficulty
    dtype: string
  - name: year
    dtype: int32
  config_name: mode=first,char_skip=25
  splits:
  - name: adversarial
    num_bytes: 1258844
    num_examples: 1145
  - name: buzzdev
    num_bytes: 1553636
    num_examples: 1161
  - name: buzztest
    num_bytes: 2653425
    num_examples: 1953
  - name: buzztrain
    num_bytes: 19699736
    num_examples: 16706
  - name: guessdev
    num_bytes: 1414882
    num_examples: 1055
  - name: guesstest
    num_bytes: 2997123
    num_examples: 2151
  - name: guesstrain
    num_bytes: 117599750
    num_examples: 96221
  download_size: 170754918
  dataset_size: 147177396
---

# Dataset Card for "qanta"

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

- **Homepage:** [http://www.qanta.org/](http://www.qanta.org/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [Quizbowl: The Case for Incremental Question Answering](https://arxiv.org/abs/1904.04792)
- **Point of Contact:** [Jordan Boyd-Graber](mailto:jbg@umiacs.umd.edu)
- **Size of downloaded dataset files:** 162.84 MB
- **Size of the generated dataset:** 140.36 MB
- **Total amount of disk used:** 303.20 MB

### Dataset Summary

The Qanta dataset is a question answering dataset based on the academic trivia game Quizbowl.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

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

### Data Fields

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

### Data Splits

|         name          |adversarial|buzzdev|buzztrain|guessdev|guesstrain|buzztest|guesstest|
|-----------------------|----------:|------:|--------:|-------:|---------:|-------:|--------:|
|mode=first,char_skip=25|       1145|   1161|    16706|    1055|     96221|    1953|     2151|

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