---
---

# Dataset Card for "sem_eval_2010_task_8"

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

- **Homepage:** [https://semeval2.fbk.eu/semeval2.php?location=tasks&taskid=11](https://semeval2.fbk.eu/semeval2.php?location=tasks&taskid=11)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1.87 MB
- **Size of the generated dataset:** 1.35 MB
- **Total amount of disk used:** 3.22 MB

### [Dataset Summary](#dataset-summary)

The SemEval-2010 Task 8 focuses on Multi-way classification of semantic relations between pairs of nominals.
The task was designed to compare different approaches to semantic relation classification
and to provide a standard testbed for future research.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 1.87 MB
- **Size of the generated dataset:** 1.35 MB
- **Total amount of disk used:** 3.22 MB

An example of 'train' looks as follows.
```
{
    "relation": 3,
    "sentence": "The system as described above has its greatest application in an arrayed <e1>configuration</e1> of antenna <e2>elements</e2>."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `sentence`: a `string` feature.
- `relation`: a classification label, with possible values including `Cause-Effect(e1,e2)` (0), `Cause-Effect(e2,e1)` (1), `Component-Whole(e1,e2)` (2), `Component-Whole(e2,e1)` (3), `Content-Container(e1,e2)` (4).

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|test|
|-------|----:|---:|
|default| 8000|2717|

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
@inproceedings{hendrickx-etal-2010-semeval,
    title = "{S}em{E}val-2010 Task 8: Multi-Way Classification of Semantic Relations between Pairs of Nominals",
    author = "Hendrickx, Iris  and
      Kim, Su Nam  and
      Kozareva, Zornitsa  and
      Nakov, Preslav  and
      {'O} S{'e}aghdha, Diarmuid  and
      Pad{'o}, Sebastian  and
      Pennacchiotti, Marco  and
      Romano, Lorenza  and
      Szpakowicz, Stan",
    booktitle = "Proceedings of the 5th International Workshop on Semantic Evaluation",
    month = jul,
    year = "2010",
    address = "Uppsala, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/S10-1006",
    pages = "33--38",
}

```


### Contributions

Thanks to [@JoelNiklaus](https://github.com/JoelNiklaus) for adding this dataset.