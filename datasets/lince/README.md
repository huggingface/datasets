---
paperswithcode_id: lince
pretty_name: Linguistic Code-switching Evaluation Dataset
dataset_info:
- config_name: lid_spaeng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  splits:
  - name: test
    num_bytes: 1337727
    num_examples: 8289
  - name: train
    num_bytes: 4745003
    num_examples: 21030
  - name: validation
    num_bytes: 739950
    num_examples: 3332
  download_size: 1188861
  dataset_size: 6822680
- config_name: lid_hineng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  splits:
  - name: test
    num_bytes: 456850
    num_examples: 1854
  - name: train
    num_bytes: 1662284
    num_examples: 4823
  - name: validation
    num_bytes: 268930
    num_examples: 744
  download_size: 432854
  dataset_size: 2388064
- config_name: lid_msaea
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  splits:
  - name: test
    num_bytes: 590488
    num_examples: 1663
  - name: train
    num_bytes: 3804156
    num_examples: 8464
  - name: validation
    num_bytes: 490566
    num_examples: 1116
  download_size: 803806
  dataset_size: 4885210
- config_name: lid_nepeng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  splits:
  - name: test
    num_bytes: 620512
    num_examples: 3228
  - name: train
    num_bytes: 2239014
    num_examples: 8451
  - name: validation
    num_bytes: 351649
    num_examples: 1332
  download_size: 545342
  dataset_size: 3211175
- config_name: pos_spaeng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  - name: pos
    sequence: string
  splits:
  - name: test
    num_bytes: 1758626
    num_examples: 10720
  - name: train
    num_bytes: 5467832
    num_examples: 27893
  - name: validation
    num_bytes: 840593
    num_examples: 4298
  download_size: 819657
  dataset_size: 8067051
- config_name: pos_hineng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  - name: pos
    sequence: string
  splits:
  - name: test
    num_bytes: 131192
    num_examples: 299
  - name: train
    num_bytes: 537541
    num_examples: 1030
  - name: validation
    num_bytes: 80886
    num_examples: 160
  download_size: 113872
  dataset_size: 749619
- config_name: ner_spaeng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  - name: ner
    sequence: string
  splits:
  - name: test
    num_bytes: 6530956
    num_examples: 23527
  - name: train
    num_bytes: 9836312
    num_examples: 33611
  - name: validation
    num_bytes: 2980990
    num_examples: 10085
  download_size: 3075520
  dataset_size: 19348258
- config_name: ner_msaea
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: ner
    sequence: string
  splits:
  - name: test
    num_bytes: 367310
    num_examples: 1110
  - name: train
    num_bytes: 3887684
    num_examples: 10103
  - name: validation
    num_bytes: 431414
    num_examples: 1122
  download_size: 938671
  dataset_size: 4686408
- config_name: ner_hineng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  - name: ner
    sequence: string
  splits:
  - name: test
    num_bytes: 185220
    num_examples: 522
  - name: train
    num_bytes: 474639
    num_examples: 1243
  - name: validation
    num_bytes: 121403
    num_examples: 314
  download_size: 141285
  dataset_size: 781262
- config_name: sa_spaeng
  features:
  - name: idx
    dtype: int32
  - name: words
    sequence: string
  - name: lid
    sequence: string
  - name: sa
    dtype: string
  splits:
  - name: test
    num_bytes: 1349407
    num_examples: 4736
  - name: train
    num_bytes: 3587783
    num_examples: 12194
  - name: validation
    num_bytes: 546692
    num_examples: 1859
  download_size: 1031412
  dataset_size: 5483882
---

# Dataset Card for "lince"

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

- **Homepage:** [http://ritual.uh.edu/lince](http://ritual.uh.edu/lince)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 8.67 MB
- **Size of the generated dataset:** 53.81 MB
- **Total amount of disk used:** 62.48 MB

### Dataset Summary

LinCE is a centralized Linguistic Code-switching Evaluation benchmark
(https://ritual.uh.edu/lince/) that contains data for training and evaluating
NLP systems on code-switching tasks.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### lid_hineng

- **Size of downloaded dataset files:** 0.41 MB
- **Size of the generated dataset:** 2.28 MB
- **Total amount of disk used:** 2.69 MB

An example of 'validation' looks as follows.
```
{
    "idx": 0,
    "lid": ["other", "other", "lang1", "lang1", "lang1", "other", "lang1", "lang1", "lang1", "lang1", "lang1", "lang1", "lang1", "mixed", "lang1", "lang1", "other"],
    "words": ["@ZahirJ", "@BinyavangaW", "Loved", "the", "ending", "!", "I", "could", "have", "offered", "you", "some", "ironic", "chai-tea", "for", "it", ";)"]
}
```

#### lid_msaea

- **Size of downloaded dataset files:** 0.77 MB
- **Size of the generated dataset:** 4.66 MB
- **Total amount of disk used:** 5.43 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "idx": 0,
    "lid": ["ne", "lang2", "other", "lang2", "lang2", "other", "other", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "lang2", "other", "lang2", "lang2", "lang2", "ne", "lang2", "lang2"],
    "words": "[\"علاء\", \"بخير\", \"،\", \"معنوياته\", \"كويسة\", \".\", \"..\", \"اسخف\", \"حاجة\", \"بس\", \"ان\", \"كل\", \"واحد\", \"منهم\", \"بييقى\", \"مقفول\", \"عليه\"..."
}
```

#### lid_nepeng

- **Size of downloaded dataset files:** 0.52 MB
- **Size of the generated dataset:** 3.06 MB
- **Total amount of disk used:** 3.58 MB

An example of 'validation' looks as follows.
```
{
    "idx": 1,
    "lid": ["other", "lang2", "lang2", "lang2", "lang2", "lang1", "lang1", "lang1", "lang1", "lang1", "lang2", "lang2", "other", "mixed", "lang2", "lang2", "other", "other", "other", "other"],
    "words": ["@nirvikdada", "la", "hamlai", "bhetna", "paayeko", "will", "be", "your", "greatest", "gift", "ni", "dada", ";P", "#TreatChaiyo", "j", "hos", ";)", "@zappylily", "@AsthaGhm", "@ayacs_asis"]
}
```

#### lid_spaeng

- **Size of downloaded dataset files:** 1.13 MB
- **Size of the generated dataset:** 6.51 MB
- **Total amount of disk used:** 7.64 MB

An example of 'train' looks as follows.
```
{
    "idx": 0,
    "lid": ["other", "other", "lang1", "lang1", "lang1", "other", "lang1", "lang1"],
    "words": ["11:11", ".....", "make", "a", "wish", ".......", "night", "night"]
}
```

#### ner_hineng

- **Size of downloaded dataset files:** 0.13 MB
- **Size of the generated dataset:** 0.75 MB
- **Total amount of disk used:** 0.88 MB

An example of 'train' looks as follows.
```
{
    "idx": 1,
    "lid": ["en", "en", "en", "en", "en", "en", "hi", "hi", "hi", "hi", "hi", "hi", "hi", "en", "en", "en", "en", "rest"],
    "ner": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-PERSON", "I-PERSON", "O", "O", "O", "B-PERSON", "I-PERSON"],
    "words": ["I", "liked", "a", "@YouTube", "video", "https://t.co/DmVqhZbdaI", "Kabhi", "Palkon", "Pe", "Aasoon", "Hai-", "Kishore", "Kumar", "-Vocal", "Cover", "By", "Stephen", "Qadir"]
}
```

### Data Fields

The data fields are the same among all splits.

#### lid_hineng
- `idx`: a `int32` feature.
- `words`: a `list` of `string` features.
- `lid`: a `list` of `string` features.

#### lid_msaea
- `idx`: a `int32` feature.
- `words`: a `list` of `string` features.
- `lid`: a `list` of `string` features.

#### lid_nepeng
- `idx`: a `int32` feature.
- `words`: a `list` of `string` features.
- `lid`: a `list` of `string` features.

#### lid_spaeng
- `idx`: a `int32` feature.
- `words`: a `list` of `string` features.
- `lid`: a `list` of `string` features.

#### ner_hineng
- `idx`: a `int32` feature.
- `words`: a `list` of `string` features.
- `lid`: a `list` of `string` features.
- `ner`: a `list` of `string` features.

### Data Splits

|   name   |train|validation|test|
|----------|----:|---------:|---:|
|lid_hineng| 4823|       744|1854|
|lid_msaea | 8464|      1116|1663|
|lid_nepeng| 8451|      1332|3228|
|lid_spaeng|21030|      3332|8289|
|ner_hineng| 1243|       314| 522|

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
@inproceedings{aguilar-etal-2020-lince,
    title = "{L}in{CE}: A Centralized Benchmark for Linguistic Code-switching Evaluation",
    author = "Aguilar, Gustavo  and
      Kar, Sudipta  and
      Solorio, Thamar",
    booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.223",
    pages = "1803--1813",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

Note that each LinCE dataset has its own citation too. Please see [here](https://ritual.uh.edu/lince/datasets)
for the correct citation on each dataset.

### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf), [@gaguilar](https://github.com/gaguilar) for adding this dataset.