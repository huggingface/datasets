---
---

# Dataset Card for "definite_pronoun_resolution"

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

- **Homepage:** [http://www.hlt.utdallas.edu/~vince/data/emnlp12/](http://www.hlt.utdallas.edu/~vince/data/emnlp12/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.22 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.45 MB

### [Dataset Summary](#dataset-summary)

Composed by 30 students from one of the author's undergraduate classes. These
sentence pairs cover topics ranging from real events (e.g., Iran's plan to
attack the Saudi ambassador to the U.S.) to events/characters in movies (e.g.,
Batman) and purely imaginary situations, largely reflecting the pop culture as
perceived by the American kids born in the early 90s. Each annotated example
spans four lines: the first line contains the sentence, the second line contains
the target pronoun, the third line contains the two candidate antecedents, and
the fourth line contains the correct antecedent. If the target pronoun appears
more than once in the sentence, its first occurrence is the one to be resolved.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### plain_text

- **Size of downloaded dataset files:** 0.22 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.45 MB

An example of 'train' looks as follows.
```
{
    "candidates": ["coreference resolution", "chunking"],
    "label": 0,
    "pronoun": "it",
    "sentence": "There is currently more work on coreference resolution than on chunking because it is a problem that is still far from being solved."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### plain_text
- `sentence`: a `string` feature.
- `pronoun`: a `string` feature.
- `candidates`: a `list` of `string` features.
- `label`: a classification label, with possible values including `0` (0), `1` (1).

### [Data Splits Sample Size](#data-splits-sample-size)

|   name   |train|test|
|----------|----:|---:|
|plain_text| 1322| 564|

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
@inproceedings{rahman2012resolving,
  title={Resolving complex cases of definite pronouns: the winograd schema challenge},
  author={Rahman, Altaf and Ng, Vincent},
  booktitle={Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning},
  pages={777--789},
  year={2012},
  organization={Association for Computational Linguistics}
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.