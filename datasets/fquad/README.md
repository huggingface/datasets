---
---

# Dataset Card for "fquad"

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

- **Homepage:** [https://fquad.illuin.tech/](https://fquad.illuin.tech/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3.14 MB
- **Size of the generated dataset:** 6.62 MB
- **Total amount of disk used:** 9.76 MB

### [Dataset Summary](#dataset-summary)

FQuAD: French Question Answering Dataset
We introduce FQuAD, a native French Question Answering Dataset. FQuAD contains 25,000+ question and answer pairs.
Finetuning CamemBERT on FQuAD yields a F1 score of 88% and an exact match of 77.9%.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 3.14 MB
- **Size of the generated dataset:** 6.62 MB
- **Total amount of disk used:** 9.76 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answers_starts": [161, 46, 204],
        "texts": ["La Vierge aux rochers", "documents contemporains", "objets de spéculations"]
    },
    "context": "\"Les deux tableaux sont certes décrits par des documents contemporains à leur création mais ceux-ci ne le font qu'indirectement ...",
    "questions": ["Que concerne principalement les documents ?", "Par quoi sont décrit les deux tableaux ?", "Quels types d'objets sont les deux tableaux aux yeux des chercheurs ?"]
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `context`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a dictionary feature containing:
  - `texts`: a `string` feature.
  - `answers_starts`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|
|-------|----:|---------:|
|default| 4921|       768|

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
@ARTICLE{2020arXiv200206071
       author = {Martin, d'Hoffschmidt and Maxime, Vidal and
         Wacim, Belblidia and Tom, Brendlé},
        title = "{FQuAD: French Question Answering Dataset}",
      journal = {arXiv e-prints},
     keywords = {Computer Science - Computation and Language},
         year = "2020",
        month = "Feb",
          eid = {arXiv:2002.06071},
        pages = {arXiv:2002.06071},
archivePrefix = {arXiv},
       eprint = {2002.06071},
 primaryClass = {cs.CL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.