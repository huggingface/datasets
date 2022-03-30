---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
pretty_name: Wiki-DPR
paperswithcode_id: null
licenses:
- cc-by-sa-3.0
- gfdl-1.3-or-later
task_categories:
- text-generation
- fill-mask
- other-text-search
task_ids:
- language-modeling
- masked-language-modeling
- other-neural-search
source_datasets:
- original
multilinguality:
- multilingual
size_categories:
- 10M<n<100M
languages:
- en
---

# Dataset Card for "wiki_dpr"

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

- **Homepage:** [https://github.com/facebookresearch/DPR](https://github.com/facebookresearch/DPR)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 406068.98 MB
- **Size of the generated dataset:** 448718.73 MB
- **Total amount of disk used:** 932739.13 MB

### Dataset Summary

This is the wikipedia split used to evaluate the Dense Passage Retrieval (DPR) model.
It contains 21M passages from wikipedia along with their DPR embeddings.
The wikipedia articles were split into multiple, disjoint text blocks of 100 words as passages.

The wikipedia dump is the one from Dec. 20, 2018.


### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

Each instance contains a paragraph of at most 100 words, as well as the title of the wikipedia page it comes from, and the DPR embedding (a 768-d vector).

#### psgs_w100.multiset.compressed

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 145204.14 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{'id': '1',
 'text': 'Aaron Aaron ( or ; "Ahärôn") is a prophet, high priest, and the brother of Moses in the Abrahamic religions. Knowledge of Aaron, along with his brother Moses, comes exclusively from religious texts, such as the Bible and Quran. The Hebrew Bible relates that, unlike Moses, who grew up in the Egyptian royal court, Aaron and his elder sister Miriam remained with their kinsmen in the eastern border-land of Egypt (Goshen). When Moses first confronted the Egyptian king about the Israelites, Aaron served as his brother\'s spokesman ("prophet") to the Pharaoh. Part of the Law (Torah) that Moses received from'],
 'title': 'Aaron',
 'embeddings': [-0.07233893871307373,
   0.48035329580307007,
   0.18650995194911957,
   -0.5287084579467773,
   -0.37329429388046265,
   0.37622880935668945,
   0.25524479150772095,
   ...
   -0.336689829826355,
   0.6313082575798035,
   -0.7025573253631592]}
```

#### psgs_w100.multiset.exact

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 178700.81 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{'id': '1',
 'text': 'Aaron Aaron ( or ; "Ahärôn") is a prophet, high priest, and the brother of Moses in the Abrahamic religions. Knowledge of Aaron, along with his brother Moses, comes exclusively from religious texts, such as the Bible and Quran. The Hebrew Bible relates that, unlike Moses, who grew up in the Egyptian royal court, Aaron and his elder sister Miriam remained with their kinsmen in the eastern border-land of Egypt (Goshen). When Moses first confronted the Egyptian king about the Israelites, Aaron served as his brother\'s spokesman ("prophet") to the Pharaoh. Part of the Law (Torah) that Moses received from'],
 'title': 'Aaron',
 'embeddings': [-0.07233893871307373,
   0.48035329580307007,
   0.18650995194911957,
   -0.5287084579467773,
   -0.37329429388046265,
   0.37622880935668945,
   0.25524479150772095,
   ...
   -0.336689829826355,
   0.6313082575798035,
   -0.7025573253631592]}
```

#### psgs_w100.multiset.no_index

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 142464.62 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{'id': '1',
 'text': 'Aaron Aaron ( or ; "Ahärôn") is a prophet, high priest, and the brother of Moses in the Abrahamic religions. Knowledge of Aaron, along with his brother Moses, comes exclusively from religious texts, such as the Bible and Quran. The Hebrew Bible relates that, unlike Moses, who grew up in the Egyptian royal court, Aaron and his elder sister Miriam remained with their kinsmen in the eastern border-land of Egypt (Goshen). When Moses first confronted the Egyptian king about the Israelites, Aaron served as his brother\'s spokesman ("prophet") to the Pharaoh. Part of the Law (Torah) that Moses received from'],
 'title': 'Aaron',
 'embeddings': [-0.07233893871307373,
   0.48035329580307007,
   0.18650995194911957,
   -0.5287084579467773,
   -0.37329429388046265,
   0.37622880935668945,
   0.25524479150772095,
   ...
   -0.336689829826355,
   0.6313082575798035,
   -0.7025573253631592]}
```

#### psgs_w100.nq.compressed

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 145204.14 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{'id': '1',
 'text': 'Aaron Aaron ( or ; "Ahärôn") is a prophet, high priest, and the brother of Moses in the Abrahamic religions. Knowledge of Aaron, along with his brother Moses, comes exclusively from religious texts, such as the Bible and Quran. The Hebrew Bible relates that, unlike Moses, who grew up in the Egyptian royal court, Aaron and his elder sister Miriam remained with their kinsmen in the eastern border-land of Egypt (Goshen). When Moses first confronted the Egyptian king about the Israelites, Aaron served as his brother\'s spokesman ("prophet") to the Pharaoh. Part of the Law (Torah) that Moses received from'],
 'title': 'Aaron',
 'embeddings': [0.013342111371457577,
   0.582173764705658,
   -0.31309744715690613,
   -0.6991612911224365,
   -0.5583199858665466,
   0.5187504887580872,
   0.7152731418609619,
   ...
   -0.5385938286781311,
   0.8093984127044678,
   -0.4741983711719513]}
```

#### psgs_w100.nq.exact

- **Size of downloaded dataset files:** 67678.16 MB
- **Size of the generated dataset:** 74786.45 MB
- **Total amount of disk used:** 178700.81 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{'id': '1',
 'text': 'Aaron Aaron ( or ; "Ahärôn") is a prophet, high priest, and the brother of Moses in the Abrahamic religions. Knowledge of Aaron, along with his brother Moses, comes exclusively from religious texts, such as the Bible and Quran. The Hebrew Bible relates that, unlike Moses, who grew up in the Egyptian royal court, Aaron and his elder sister Miriam remained with their kinsmen in the eastern border-land of Egypt (Goshen). When Moses first confronted the Egyptian king about the Israelites, Aaron served as his brother\'s spokesman ("prophet") to the Pharaoh. Part of the Law (Torah) that Moses received from'],
 'title': 'Aaron',
 'embeddings': [0.013342111371457577,
   0.582173764705658,
   -0.31309744715690613,
   -0.6991612911224365,
   -0.5583199858665466,
   0.5187504887580872,
   0.7152731418609619,
   ...
   -0.5385938286781311,
   0.8093984127044678,
   -0.4741983711719513]}
```

### Data Fields

The data fields are the same among all splits.

#### psgs_w100.multiset.compressed
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.multiset.exact
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.multiset.no_index
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.nq.compressed
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

#### psgs_w100.nq.exact
- `id`: a `string` feature.
- `text`: a `string` feature.
- `title`: a `string` feature.
- `embeddings`: a `list` of `float32` features.

### Data Splits

|            name             | train  |
|-----------------------------|-------:|
|psgs_w100.multiset.compressed|21015300|
|psgs_w100.multiset.exact     |21015300|
|psgs_w100.multiset.no_index  |21015300|
|psgs_w100.nq.compressed      |21015300|
|psgs_w100.nq.exact           |21015300|

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

@misc{karpukhin2020dense,
    title={Dense Passage Retrieval for Open-Domain Question Answering},
    author={Vladimir Karpukhin and Barlas Oğuz and Sewon Min and Patrick Lewis and Ledell Wu and Sergey Edunov and Danqi Chen and Wen-tau Yih},
    year={2020},
    eprint={2004.04906},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
