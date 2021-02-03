---
---

# Dataset Card for "xtreme"

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

- **Homepage:** [https://github.com/google-research/xtreme	https://www.nyu.edu/projects/bowman/xnli/](https://github.com/google-research/xtreme	https://www.nyu.edu/projects/bowman/xnli/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 15143.21 MB
- **Size of the generated dataset:** 1027.42 MB
- **Total amount of disk used:** 16170.64 MB

### [Dataset Summary](#dataset-summary)

The Cross-lingual Natural Language Inference (XNLI) corpus is a crowd-sourced collection of 5,000 test and
2,500 dev pairs for the MultiNLI corpus. The pairs are annotated with textual entailment and translated into
14 languages: French, Spanish, German, Greek, Bulgarian, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese,
Hindi, Swahili and Urdu. This results in 112.5k annotated pairs. Each premise can be associated with the
corresponding hypothesis in the 15 languages, summing up to more than 1.5M combinations. The corpus is made to
evaluate how to perform inference in any language (including low-resources ones like Swahili or Urdu) when only
English NLI data is available at training time. One solution is cross-lingual sentence encoding, for which XNLI
is an evaluation benchmark.
The Cross-lingual TRansfer Evaluation of Multilingual Encoders (XTREME) benchmark is a benchmark for the evaluation of
the cross-lingual generalization ability of pre-trained multilingual models. It covers 40 typologically diverse languages
(spanning 12 language families) and includes nine tasks that collectively require reasoning about different levels of
syntax and semantics. The languages in XTREME are selected to maximize language diversity, coverage in existing tasks,
and availability of training data. Among these are many under-studied languages, such as the Dravidian languages Tamil
(spoken in southern India, Sri Lanka, and Singapore), Telugu and Malayalam (spoken mainly in southern India), and the
Niger-Congo languages Swahili and Yoruba, spoken in Africa.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### MLQA.ar.ar

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.77 MB
- **Total amount of disk used:** 80.98 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.de

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 2.43 MB
- **Total amount of disk used:** 74.64 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.en

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.62 MB
- **Total amount of disk used:** 80.83 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.es

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.12 MB
- **Total amount of disk used:** 75.33 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.hi

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.17 MB
- **Total amount of disk used:** 75.38 MB

An example of 'validation' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### MLQA.ar.ar
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.de
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.en
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.es
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.hi
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|   name   |validation|test|
|----------|---------:|---:|
|MLQA.ar.ar|       517|5335|
|MLQA.ar.de|       207|1649|
|MLQA.ar.en|       517|5335|
|MLQA.ar.es|       161|1978|
|MLQA.ar.hi|       186|1831|

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
  @InProceedings{conneau2018xnli,
  author = {Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin},
  title = {XNLI: Evaluating Cross-lingual Sentence Representations},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing},
  year = {2018},
  publisher = {Association for Computational Linguistics},
  location = {Brussels, Belgium},
}
@article{hu2020xtreme,
      author    = {Junjie Hu and Sebastian Ruder and Aditya Siddhant and Graham Neubig and Orhan Firat and Melvin Johnson},
      title     = {XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization},
      journal   = {CoRR},
      volume    = {abs/2003.11080},
      year      = {2020},
      archivePrefix = {arXiv},
      eprint    = {2003.11080}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@lvwerra](https://github.com/lvwerra), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.